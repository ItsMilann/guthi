from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAcceptable
from rest_framework.decorators import action

from django_filters.rest_framework.backends import DjangoFilterBackend

from templates import models, filters
from templates.utils import generate_issue_number
from templates.api import serializers
from users.response import CustomModelViewSet, CustomResponse
from branches.models import FiscalYear


class PaperViewSet(CustomModelViewSet):
    queryset = models.Paper.objects.all()
    serializer_class = serializers.PaperSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.PaperFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PaperDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        branch = getattr(self.request.user, "branch", None)
        qs = super().get_queryset()
        if branch is None:
            raise NotAcceptable("User must belong to a branch.")
        qs = models.Paper.objects.filter(created_by__organization=branch)
        return qs

    def _create_issue_id(self, instance, **kwargs):
        instance.issue_id = generate_issue_number(instance)
        instance.save(**kwargs)

    def perform_create(self, serializer):
        fiscal_year = FiscalYear.active()
        instance = serializer.save(
            created_by=self.request.user,
            fiscal_year=fiscal_year,
            updated_by=self.request.user,
        )
        self._create_issue_id(instance)

    def perform_update(self, serializer):
        instance = serializer.instance
        self._create_issue_id(instance)
        serializer.save(updated_by=self.request.user)

    @action(["GET"], detail=False)
    def inbox(self, request, *args, **kwargs):
        related_deps = models.RelatedBranch.objects.filter(department=request.user.department)
        paper_ids = related_deps.values_list("paper__id", flat=True)
        self.queryset = models.Paper.objects.filter(id__in=paper_ids)
        return super().list(request, *args, **kwargs)

    @action(["POST"], detail=True)
    def forward(self, request, *args, **kwargs):
        paper = self.get_object()
        receiving_department = request.data["receiving_department"]
        related_branch = models.RelatedBranch()
        related_branch.paper = paper
        related_branch.department = receiving_department
        related_branch.fiscal_year = paper.fiscal_year
        related_branch.active = True
        related_branch.save()
        serializer = serializers.RelatedBranchSerializer(related_branch)
        return CustomResponse(serializer.data, status=200)


class FAQViewset(CustomModelViewSet):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializers
