from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = {
        "error": "object not found",
        "data": {},
        "message": "something went wrong",
    }
    default_code = "not_found"


def _get_queryset(klass):
    if hasattr(klass, "_default_manager"):
        return klass._default_manager.all()
    return klass


def get_object_or_not_found(klass, *ar, **kw):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*ar, **kw)
    except queryset.model.DoesNotExist:
        raise NotFound(f"object does not exists")


def get_key_or_raise_exception(data, key, error=None):
    try:
        return data[key]
    except KeyError:
        raise ValidationError(error or f"missing required field {key}")


def clear_cache():
    from django_redis import get_redis_connection

    get_redis_connection("default").flushall()


def get_base_path(request, path):
    scheme = request.META["UWSGI_ROUTER"]
    host = request.META["HTTP_HOST"]
    url = f"{scheme}://{host}{path}/"
    return url


def get_nepali_number(eng_number):
    eng = str(eng_number)
    dic = {
        "1": "१",
        "2": "२",
        "3": "३",
        "4": "४",
        "5": "५",
        "6": "६",
        "7": "७",
        "8": "८",
        "9": "९",
        "0": "०",
        "/": "/",
        "-": "-",
    }
    try:
        return "".join(dic[i] for i in eng)
    except:
        return eng_number


def validate_size(file, size_in_MB):
    try:
        if file.size > size_in_MB * 1024 * 1024:
            raise ValidationError(f"file size should be less than {size_in_MB} MB")
    except FileNotFoundError:
        return None
    return file


def process_img(img, valid_size_in_MB, height=1200, width=1200):
    import sys
    from io import BytesIO
    from django.core.files.uploadedfile import InMemoryUploadedFile
    from PIL import Image

    file = validate_size(img, valid_size_in_MB)
    if not file:
        return None
    elif img.name.split(".")[1] == "png":
        return InMemoryUploadedFile(
            img,
            None,
            img.name,
            "image/%s" % img.name.split(".")[1],
            sys.getsizeof(img),
            None,
        )
    try:
        size = (height, width)
        output = BytesIO()
        im = Image.open(img)
        im = im.convert("RGB")
        im.thumbnail(size)
        im.save(output, "JPEG", quality=90)
        output.seek(0)
        return InMemoryUploadedFile(
            output,
            "ImageField",
            "%s.jpg" % img.name.split(".")[0],
            "image/jpeg",
            sys.getsizeof(output),
            None,
        )

    except OSError:
        return InMemoryUploadedFile(
            img,
            None,
            img.name,
            "image/%s" % img.name.split(".")[1],
            sys.getsizeof(img),
            None,
        )


def paginate(request, original_data, length=10):
    base_path = request.META.get("PATH_INFO")
    page = request.query_params.get("page") or 1
    try:
        page = int(page)
    except ValueError:
        page = 1
    if page == 0:
        page = 1

    paginated_data = [
        original_data[i : i + length] for i in range(0, len(original_data), length)
    ]
    next_, prev = None, None
    if len(original_data) > page * length:
        next_ = request.build_absolute_uri(f"{base_path}?page={page+1}")
    if length * page > length:
        prev = request.build_absolute_uri(f"{base_path}?page={page-1}")
    try:
        rv = paginated_data[page - 1]
    except IndexError:
        return {"message": "page not found"}, 404
    data = {"count": len(original_data), "next": next_, "previous": prev, "results": rv}
    return data, 200
