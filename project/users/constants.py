import enum
from django.db.models import TextChoices


class Roles(TextChoices):
    ITO_ADMIN = "ito_admin", "ito_admin"
    WARD_USER = "ward_user", "ward_user"
    WARD_ADMIN = "ward_admin", "ward_admin"
    WARD_KAWA = "ward_kawa", "ward_kawa"
    WARD_PAPER_ISSUER = "ward_paper_issuer", "ward_paper_issuer"
    MAYOR = "mayor", "mayor"
    UPA_MAYOR = "upa_mayor", "upa_mayor"
    WARD_SECRETARY = "ward_secretary", "ward_secretary"
    SUPERUSER = "superuser", "superuser"


class ProfileTypes(enum.Enum):
    ITO = "ito"
    WARD_USER = "ward-user"
    MAYOR = "mayor"
