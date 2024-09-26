import enum
from django.db.models import TextChoices


class Roles(TextChoices):
    ADMIN = "admin", "admin"
    OPERATOR = "operator", "operator"
    SUPERUSER = "superuser", "superuser"


class ProfileTypes(enum.Enum):
    ADMIN = "admin", "admin"
    OPERATOR = "operator", "operator"
    SUPERUSER = "superuser", "superuser"
