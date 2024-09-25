from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework import status


def server_error_handler(request, *ar, **kw):
    data = {
        'message': "Something went wrong",
        'error': {
            "non_field_error": ['Internal server error occured']
        },
        "data": {}
    }
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def page_not_found(request, *ar, **kw):
    data = {
        'message': "Something went wrong",
        'error': {
            "non_field_error": ["page not found"]
        },
        "data": {}
    }
    return JsonResponse(data, status=404)


def forbidden(request, *ar, **kw):
    data = {
        'message': "Something went wrong",
        'error': {
            "non_field_error": ["invalid authentication credentials"]
        },
        "data": {}
    }
    return JsonResponse(data, status=404)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        data = response.data
        response.data = {
            'message': "Something went wrong",
            'error': {},
            "data": {}
        }
        try:
            detail = data["detail"]
            message = [str(detail)]
            response.data['error'] = {"non_field_error": message}
        except:
            response.data['error'] = data
    return response
