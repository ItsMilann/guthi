# pylint: disable=import-outside-toplevel
from templates.api.serializers import PaperDocumentSerializer
from branches import models


def attach_document(request):
    serializer = PaperDocumentSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data


def clean_mob_number(phone):
    try:  # checking non-numerics
        int(phone)
    except ValueError:
        return None
    has_country_code = phone.startswith("+977")
    if has_country_code and len(phone) == 14:
        return f"+{int(phone)}"
    if len(phone) == 10:
        return f"+977{int(phone)}"
    return None

def get_serialnum(instance):
    _branch = instance.__class__
    if fiscalyear is None:
        fiscalyear = models.FiscalYear.active()
    try:
        qs = _branch.objects.get(
            organization=instance.department,
            fiscalyear=instance.fiscalyear)
        object_ = qs.latest("serial_number")
        return object_.serial_number + 1
    except _branch.DoesNotExist:
        return 1
