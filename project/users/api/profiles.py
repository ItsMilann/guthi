from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from users.response import CustomModelViewSet as ModelViewSet

from users import models
from users.api import serializers
from users import permissions


class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(["POST", "GET"], detail=False)
    def info(self, request, *args, **kwargs):
        instance, _ = models.Profile.objects.get_or_create(user=request.user)
        self.get_object = lambda: instance
        if self.action == "GET":
            return super().retrieve(request)
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)


class ITOProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.ito()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]


class WardUserProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.others()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # TODO user django_filter
        qs = super().get_queryset()
        params = getattr(self.request, "query_params", {})
        ward = params.get("ward")
        role = params.get("role")
        if ward:
            qs = qs.filter(user__organization=ward)
        if role:
            qs = qs.filter(user__role=role)
        return qs


class MayorProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.mayor()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated, permissions.IsITOAdmin]


@api_view(["POST"])
@permission_classes([IsAuthenticated, permissions.IsAdminOrITO])
def update_kawa_status(request):
    status = request.data.get("status")
    id_ = request.data.get("profile_id")
    kawa = get_object_or_404(models.Profile, id=id_)
    kawa.is_active = status == "active"
    kawa.save()
