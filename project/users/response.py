from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers, status
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from utilities.utils import clear_cache


class CustomResponse(Response):

    def __init__(self, data=None, status=None, error={}, message=None, object=None):
        self.data = data
        self.status = status
        self.message = message
        self.error = error
        self.obj = object
        data = {}
        assert self.status, "missing required parameter, 'status'"
        if self.status >= 200 and self.status < 300:
            data["message"] = self.message or "request success"
        else:
            data["message"] = self.message or "something went wrong"
        data["error"] = self.error
        data["data"] = self.data
        return super().__init__(data=data, status=self.status)


class CustomModelViewSet(ModelViewSet):

    def create(self, request, *args, **kwargs):
        data, message, status, error = {}, "Something went wrong", 201, {}
        serializer = self.get_serializer(data=request.data)
        obj = super().get_serializer_class()
        if serializer.is_valid():
            self.perform_create(serializer)
            message = f'{obj.Meta.model.__name__} created'
            data = serializer.data
        else:
            error = serializer.errors
            try:
                _ = error["non_field_errors"]
            except KeyError:
                error["non_field_errors"] = []
            status = 400
        # clear_cache() # NOTE temporary solution
        return CustomResponse(
            data=data,
            error=error,
            message=message,
            object=obj,
            status=status
        )

    # @method_decorator(cache_page(60*30))
    # @method_decorator(vary_on_headers("Authorization",))
    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        serializer_class = super().get_serializer_class()
        obj = serializer_class
        return CustomResponse(data, message=f"{obj.Meta.model.__name__}'s list", object=obj, status=status.HTTP_200_OK)
    
    # @method_decorator(cache_page(60*30))
    # @method_decorator(vary_on_headers("Authorization",))
    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        serializer_class = super().get_serializer_class()
        obj = serializer_class
        return CustomResponse(data, message=f"{obj.Meta.model.__name__}'s detail", object=obj, status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
        data, message, status, error = {}, "Something went wrong", 201, {}
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        obj = super().get_serializer_class()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            data = serializer.data
            message = f'{obj.Meta.model.__name__} updated'
            status = 200
        else:
            error = serializer.errors
            try:
                _ = error["non_field_errors"]
            except KeyError:
                error["non_field_errors"] = []
            status = 400
        # clear_cache()  # NOTE temporary solution
        return CustomResponse(
            data=data,
            error=error,
            message=message,
            object=obj,
            status=status)

    def destroy(self, request, *args, **kwargs):
        data = super().destroy(request, *args, **kwargs).data
        serializer_class = super().get_serializer_class()
        obj = serializer_class
        # clear_cache()
        return CustomResponse(
            data,
            message=f"{obj.Meta.model.__name__} deleted",
            object=obj,
            status=200)
