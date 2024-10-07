from django_filters import rest_framework as filters
from branches import models


class BranchFilter(filters.FilterSet):
    district_en = filters.CharFilter(lookup_expr="icontains")
    district_np = filters.CharFilter(lookup_expr="icontains")
    name_np = filters.CharFilter(lookup_expr="icontains")
    name_en = filters.CharFilter(lookup_expr="icontains")
    address_np = filters.CharFilter(lookup_expr="icontains")
    address_en = filters.CharFilter(lookup_expr="icontains")
    province_np = filters.CharFilter(lookup_expr="icontains")
    province_en = filters.CharFilter(lookup_expr="icontains")
    phone_np = filters.CharFilter(lookup_expr="icontains")
    phone_en = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Branch
        fields = [
            "district_en",
            "district_np",
            "name_np",
            "name_en",
            "address_np",
            "address_en",
            "province_np",
            "province_en",
            "phone_np",
            "phone_en",
            "email",
        ]

class DepartmentFilter(filters.FilterSet):
    name_en = filters.CharFilter(lookup_expr="icontains")
    name_np = filters.CharFilter(lookup_expr="icontains")
    address_en = filters.CharFilter(lookup_expr="icontains")
    address_np = filters.CharFilter(lookup_expr="icontains")
    province_en = filters.CharFilter(lookup_expr="icontains")
    province_np = filters.CharFilter(lookup_expr="icontains")
    phone_en = filters.CharFilter(lookup_expr="icontains")
    phone_np = filters.CharFilter(lookup_expr="icontains")
    email = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = models.Department
        fields = [
            "name_en",
            "name_np",
            "address_en",
            "address_np",
            "province_en",
            "province_np",
            "phone_en",
            "phone_np",
            "email",
            "branch",
        ]
