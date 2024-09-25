from rest_framework.decorators import api_view
from templates.utils import get_excel_report, get_pdf_report
from templates.selectors import get_report
from users.response import CustomResponse as Response


def report_api(request, send_stats=True):
    params = request.query_params
    type_ = params.get("type")
    from_date = params.get("from", None)
    to_date = params.get("to", None)
    date_string = f"From {from_date} to {to_date}" if (from_date and to_date) else ""

    try:
        ward_number = request.user.organization.name_np
    except AttributeError:
        ward_number = request.user.ito_profile.nagarpalika.ward_set.values_list(
            "name_np", flat=True
        )
    except Exception:
        ward_number = 0

    if type_ in ["pdf", "excel"]:
        data = get_report(request, params, paper_list=True, template_report=True)
        listing_data = data.pop("listing_data")
        scheme = request.META["wsgi.url_scheme"]
        host = request.META["HTTP_HOST"]
        if type_ == "excel":
            response_ = get_excel_report(data, date_string)
            report_path = f"{scheme}://{host}/api/{response_}"
        else:
            response_ = get_pdf_report(data, listing_data, date_string, ward_number)
            report_path = f"{scheme}://{host}{response_}"
        return {"report": report_path}

    if send_stats:
        data = get_report(request, params)
        return data
    data = get_report(request, params, template_report=True)
    return data["template_report"]


@api_view(["get"])
def report_stats_api(request):
    res = report_api(request)
    return Response(data=res, message="Report stats", status=200)


@api_view(["get"])
def report_list_api(request):
    res = report_api(request, send_stats=False)
    return Response(data=res, message="Report List", status=200)
