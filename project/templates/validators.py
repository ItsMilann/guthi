from django.db.models import Model
from rest_framework.exceptions import ValidationError

from branches.models import Branch


def validate_all_ids_exist(model_class: type[Model], ids: list[int]):
    initial_count = len(ids)
    ids = list(set(ids))
    if initial_count != len(ids):
        raise ValidationError("IDs are duplicated")
    final_count = model_class.objects.filter(id__in=ids).count()
    if initial_count != final_count:
        raise ValidationError("Object with id may not exist")


def validate_orgs_exist(ids: list[int]):
    validate_all_ids_exist(Branch, ids)
