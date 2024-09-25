from branches.models import FiscalYear, Branch
from templates.models import Paper, Template


def get_template_count(filters=None):
    qs_count = Template.objects.count()
    return qs_count


def get_paper_count(filters=None):
    qs = Paper.objects.all()
    if filters:
        qs = qs.filter(**filters)
    return qs.count()


def get_settings_count(request, filters):
    data = {
        "fiscal_year": FiscalYear.objects.count(),
        "branches": Branch.objects.wards().count(),
        "template": Template.objects.count(),
        "application": Paper.objects.count(),
    }
    return data
