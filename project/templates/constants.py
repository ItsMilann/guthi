"""Constants for template application."""
from django.db import models


class EntityType(models.TextChoices):
    """
    choices for template/catergory entity
    private: authenticated user (ward_admin/ito) le matrai herna paune
    general: authenticated/unauthenticated sabai user le herna paune.
    """

    PRIVATE = "private", "private"
    GENERAL = "general", "general"



class APIKeyType(models.TextChoices):
    """
    choices for apikeys
    """

    MOBILE = "mobile", "mobile"
    WEB = "web", "web"
    EXTERNAL = "external", "external"
    PUBLIC = "public", "public"
