from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAcceptable
from rest_framework.decorators import action

from django_filters.rest_framework.backends import DjangoFilterBackend

from templates import models, filters
from templates.utils import generate_issue_number
from templates.api import serializers
from templates import task, validators, services

from users.response import CustomModelViewSet, CustomResponse
from users.constants import Roles
from branches.models import FiscalYear


class BaseViewSet(CustomModelViewSet):
    queryset = models.Paper.objects.all()
    serializer_class = serializers.PaperSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.PaperFilter

    def _organization(self):
        organization = getattr(self.request.user, "organization", None)
        if organization:
            return organization
        raise NotAcceptable(_("User must belong to an organization."))

    def get_queryset(self):
        if self.request.user.role != Roles.ADMIN:
            qs = super().get_queryset()
            qs = qs.filter(created_by__organization=self._organization())
            return qs
        return super().get_queryset()

    def _create_issue_id(self, instance, **kwargs):
        raise NotImplementedError()

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


class PaperViewSet(BaseViewSet):
    queryset = models.Paper.objects.all()
    serializer_class = serializers.PaperSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.PaperFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PaperDetailSerializer
        return super().get_serializer_class()

    def _create_issue_id(self, instance, **kwargs):
        instance.issue_id = generate_issue_number(instance)
        instance.save(**kwargs)

    @action(["GET"], detail=False)
    def sent(self, request, *args, **kwargs):
        queryset = self.get_queryset().exclude(hardcopy_preview=[])
        if not request.user.role == Roles.ADMIN:
            organization = self._organization()
            queryset = queryset.filter(created_by__organization=organization)
        self.queryset = queryset
        return super().list(request)

    @action(["POST"], detail=True)
    def forward(self, request, *args, **kwargs):
        raise NotImplementedError

    @action(["GET"], detail=True, url_path="status")
    def settlement_status(self, request, *args, **kwargs):
        raise NotImplementedError
    
    @action(["GET"], detail=True, url_path="inbox")
    def inbox(self, request, *args, **kwargs):
        ...


class FAQViewset(CustomModelViewSet):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializers
