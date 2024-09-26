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

    @action(["POST"], detail=False, url_path="send")
    def perform_send(self, request, *args, **kwargs):
        data = request.data.copy()
        receivers = request.data.get("receiver", [])
        validators.validate_orgs_exist(receivers)
        print_ = request.data.get("__save_and_print")
        data = task.forward_to_multiple_organizations(
            data, receivers, user=request.user, darta=print_
        )
        message = _("Paper forwarding in background")
        return CustomResponse(data, message=message, status=201)

    @action(["GET"], detail=False, url_path="darta")
    def list_darta_pending_paper(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().exclude(darta_number=None)
        return super().list(request)

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
        paper = self.get_object()
        org = self._organization()
        serializer = serializers.PaperForwardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(paper=paper, forwarder=org)
        serializer = serializers.PaperForwardListSerializer(instance)
        return CustomResponse(serializer.data, status=201)

    @action(["POST"], detail=True, url_path="upload-hardcopy")
    def upload_hardcopy(self, request, *args, **kwargs):
        """User prints preview of paper and uploads it here."""
        instance = self.get_object()
        file = request.data.get("file")
        instance.hardcopy_preview = file
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    @action(["GET"], detail=True, url_path="status")
    def settlement_status(self, request, *args, **kwargs):
        obj = self.get_object()
        qs = obj.forwared.filter(parent=None)
        fields = (
            "settled",
            "forwarder_id",
            "forwarder__name_en",
            "forwarder__name_np",
            "forwarder__fullname_en",
            "forwarder__fullname_np",
            "receiver_id",
            "receiver__name_en",
            "receiver__name_np",
            "receiver__fullname_en",
            "receiver__fullname_np",
            "roll_number",
            "settlement_remarks",
            "created_at",
        )
        data = qs.values(*fields)
        return CustomResponse(data, status=200)

    @action(["POST"], detail=False, url_path="pin")
    def perform_pin(self, request, *args, **kwargs):
        """Pin papers, with received IDs"""
        paper_ids = request.data.get("papers", [])
        self.queryset = services.pin_multiple_sent_mails(paper_ids)
        return super().list(request)

    @action(["POST"], detail=False, url_path="unpin")
    def perform_unpin(self, request, *args, **kwargs):
        """Unpin papers, with received IDs"""
        paper_ids = request.data.get("papers", [])
        self.queryset = services.unpin_multiple_sent_mails(paper_ids)
        return super().list(request)


class FAQViewset(CustomModelViewSet):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializers
