from django.db.models import F
from rest_framework import serializers
from branches import models
from users.models import Profile


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = "__all__"


class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FiscalYear
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    parent_name_en = serializers.ReadOnlyField(source="parent.name_en")
    parent_name_np = serializers.ReadOnlyField(source="parent.name_np")
    parent_fullname_en = serializers.ReadOnlyField(source="parent.fullname_en")
    parent_fullname_np = serializers.ReadOnlyField(source="parent.fullname_np")

    class Meta:
        model = models.Branch
        fields = "__all__"

    def __get_organization_users(self, organization):
        users_id = organization.user_set.values_list("id", flat=True)
        qs = Profile.objects.annotate(email=F("user__email"))
        qs = qs.filter(user__id__in=users_id)
        return qs.values(
            "id",
            "email",
            "fullname_en",
            "fullname_np",
            "is_active",
            "phone_en",
            "phone_np",
            "post_en",
            "post_np",
            "user_id",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["users"] = self.__get_organization_users(instance)
        return data


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feature
        fields = "__all__"
