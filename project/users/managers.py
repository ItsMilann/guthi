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
    def admin(self):
        queryset = self.get_queryset()
        return queryset.filter(user__role=Roles.ADMIN)

    def operator(self):
        queryset = self.get_queryset()
        return queryset.filter(user__role=Roles.OPERATOR)
