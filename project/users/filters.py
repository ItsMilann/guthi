from django_filters import rest_framework as filters
from users import models


class ProfileFilter(filters.FilterSet):
    fullname_en = filters.CharFilter(lookup_expr="icontains")
    fullname_np = filters.CharFilter(lookup_expr="icontains")
    phone_np = filters.CharFilter(lookup_expr="icontains")
    phone_en = filters.CharFilter(lookup_expr="icontains")
    branch = filters.NumberFilter(field_name="user__organization")
    department = filters.NumberFilter(field_name="user__department")
    class Meta:
        model = models.Profile
        fields = [
            "fullname_en",
            "fullname_np",
            "phone_np",
            "phone_en",
            "branch",
            "department",
        ]
