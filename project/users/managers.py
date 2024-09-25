from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from users.constants import Roles


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password or email)
        user.save()
        return user

    def create_superuser(self, email, password, phone=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "superuser")
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, phone, password, **extra_fields)


class ProfileManager(models.Manager):
    def ito(self):
        queryset = self.get_queryset()
        return queryset.filter(user__role=Roles.ITO_ADMIN)

    def ward_user(self):
        queryset = self.get_queryset()
        return queryset.filter(user__role=Roles.WARD_USER)

    def ward_admin(self):
        queryset = self.get_queryset()
        return queryset.filter(user__role=Roles.WARD_ADMIN)

    def mayor(self):
        queryset = self.get_queryset()
        return queryset.filter(user__role=Roles.MAYOR)

    def others(self):
        queryset = self.get_queryset()
        return queryset.exclude(user__role__in=[Roles.ITO_ADMIN, Roles.MAYOR])
