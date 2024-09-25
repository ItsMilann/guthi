import datetime
from django_filters import rest_framework as filters
from templates import models


class PaperFilter(filters.FilterSet):
    start = filters.DateFilter(method="filter_start", label="from")
    end = filters.DateFilter(method="filter_end", label="to")
    receiving_department = filters.CharFilter(
        field_name="receiving_department", lookup_expr="icontains"
    )
    settlement_branch = filters.CharFilter(
        field_name="settlement_branch", lookup_expr="icontains"
    )
    sender = filters.CharFilter(field_name="sender", lookup_expr="icontains")

    class Meta:
        model = models.Paper
        fields = [
            "serial_number",
            "branch",
            "paper_count",
            "sender",
            "subject",
            "receiving_department",
            "receiving_department_id",
            "settlement_branch",
            "settlement_branch_id",
            "start",
            "end",
            "chalani_number",
            # "fiscal_year",
        ]

    def filter_start(self, queryset, name, value):
        if value:
            value = datetime.datetime.combine(value, datetime.time.min)
            return queryset.filter(created_at__gte=value)
        return queryset

    def filter_end(self, queryset, name, value):
        if value:
            value = datetime.datetime.combine(value, datetime.time.max)
            return queryset.filter(created_at__lte=value)
        return queryset
