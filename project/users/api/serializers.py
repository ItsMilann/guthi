from uuid import uuid4
from django.conf import settings
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from branches.serializers import BranchSerializer, DepartmentSerializer
from users import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True, required=False)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "password",
            "role",
            "organization",
        ]
        extra_kwargs = {"phone": {"required": False, "default": "NA"}}

    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        password = validated_data.get("password", uuid4().hex)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if settings.FEATURES["PROTECT_EMAIL"]:
            validated_data.pop("email", None)
        user = super().update(instance, validated_data)
        password = validated_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return instance

    def __branch_info(self, branch):
        serializer = BranchSerializer(branch)
        return serializer.data
    def __department_info(self, department):
        serializer = DepartmentSerializer(department)
        return serializer.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["branch"] = self.__branch_info(instance.organization)
        data["department"] = self.__department_info(instance.department)
        return data


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        assert isinstance(self.user, models.User)
        data["email"] = self.user.email
        data["phone"] = self.user.phone
        data["role"] = self.user.role
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="user.email")
    role = serializers.ReadOnlyField(source="user.role")
    user = UserSerializer(required=False)

    class Meta:
        model = models.Profile
        fields = "__all__"

    def validate_user(self, value):
        return value

    def __create_user(self, data):
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def __update_user(self, instance, data):
        serializer = UserSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        user = self.__create_user(request.data)
        validated_data["user"] = user
        return self.Meta.model.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context["request"]
        self.__update_user(instance.user, request.data)
        return super().update(instance, validated_data)
