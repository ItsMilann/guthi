#pylint:disable=W0201
from rest_framework import decorators
from rest_framework.permissions import IsAuthenticated
from users.response import CustomModelViewSet as ModelViewSet

from users import models
from users.api import serializers


class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    @decorators.action(["POST", "GET"], detail=False)
    def info(self, request, *args, **kwargs):
        instance, _ = models.Profile.objects.get_or_create(user=request.user)
        self.get_object = lambda: instance
        if self.action == "GET":
            return super().retrieve(request)
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
