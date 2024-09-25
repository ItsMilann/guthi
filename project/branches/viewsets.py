# from rest_framework import viewsets
import itertools
from django.db.models import Sum
from rest_framework import decorators, exceptions
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS

from django_filters.rest_framework.backends import DjangoFilterBackend
from branches import serializers
from branches import models, filters
from templates.models import Paper
from users.response import CustomModelViewSet as ModelViewSet
from users.response import CustomResponse as Response


class BranchViewSet(ModelViewSet):
    queryset = models.Branch.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BranchSerializer
    filterset_class = filters.BranchFilter
    filter_backends = [DjangoFilterBackend]

    @decorators.action(["GET"], detail=False)
    def nested(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        values = ("type", "id", "name_np", "name_en", "fullname_np", "fullname_en")
        queryset = queryset.order_by("type").values(*values)
        grouped_data = itertools.groupby(queryset, key=lambda x: x["type"])
        data = {k: list(v) for k, v in grouped_data}
        return Response(data, status=200)

class SakhaViewSet(ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = []
    filterset_class = filters.DepartmentFilter
    filter_backends = [DjangoFilterBackend]


class FiscalYearViewSet(ModelViewSet):
    queryset = models.FiscalYear.objects.all()
    serializer_class = serializers.FiscalYearSerializer
    permission_classes = [IsAuthenticated]

    @decorators.action(["GET"], detail=False)
    def active(self, request, *args, **kwargs):
        self.get_object = models.FiscalYear.active
        return super().retrieve(request, *args, **kwargs)


@decorators.api_view(["GET"])
def dashboard(request):
    paper = Paper.objects.all()
    if request.user.role == "superuser":
        stats = {}
        total_paper = paper.count()
        total_branches = models.Branch.objects.count()
        total_departments = models.Department.objects.count()
        stats["total_branches"] = total_branches
        stats["total_departments"] = total_departments
        stats["total_paper"] = total_paper
        return Response(data=stats, message="Stats for ito admin dashboard", status=200)
    try:
        branch = request.user.organization
    except AttributeError as e:
        msg = "User is not associated with any branch"
        raise exceptions.NotAcceptable(msg) from e
    kw = {"branch": branch}
    papers = paper.filter(**kw)
    paper_count = papers.count()
    departments  = branch.departments.count()
    data = {"applicants": 0, "departments": departments, "papers": paper_count}
    return Response(data, status=200)


@decorators.api_view(["GET"])
def settings_stats(request):
    data = {}
    return Response(data, status=200)


@decorators.api_view(["GET"])
def active_fiscal_year(request):
    data = models.FiscalYear.active()
    serializer = serializers.FiscalYearSerializer(data)
    return Response(serializer.data, status=200)


@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated])
def ito_admin_graph_api(request):
    choice = request.query_params.get("choice", "category")
    data = {}
    return Response(data=data, message=f"{choice} wise graph data", status=200)


class FeatureViewSet(ModelViewSet):
    queryset = models.Feature.objects.all()
    serializer_class = serializers.FeatureSerializer
    permission_classes = []

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]
        return super().get_permissions()

    @decorators.action(["GET"], detail=False)
    def flags(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        values = queryset.values("name", "enabled")
        data = {obj["name"]: obj["enabled"] for obj in values}
        return Response(data, status=200)
