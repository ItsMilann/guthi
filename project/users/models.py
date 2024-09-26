from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager, ProfileManager
from users.constants import Roles


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=25, null=True)
    role = models.CharField(max_length=25, choices=Roles.choices, default=Roles.OPERATOR)
    organization = models.ForeignKey(
        "branches.Branch",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    department = models.ForeignKey(
        "branches.Department",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    post_en = models.CharField(max_length=255, null=True, blank=True)
    post_np = models.CharField(max_length=255, null=True, blank=True)
    fullname_en = models.CharField(max_length=255, null=True)
    fullname_np = models.CharField(max_length=255, null=True)
    image = models.ImageField(blank=True, null=True)
    phone_en = models.CharField(max_length=255, null=True)
    phone_np = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    objects = ProfileManager()

    class Meta:
        ordering = ("-id",)
