from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAdminOrITO(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_ito_admin


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser


class IsWardUserOrITO(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_authenticated:
                return False
            return True
        return request.user.is_superuser


class IsWardAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "ito_admin":
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if request.method == "DELETE":
            return request.user.role == "ito_admin"
        try:
            return request.user.organization == obj
        except AttributeError:
            return False


class CanUpdatePaper(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "ito_admin":
            return True
        if request.user.is_superuser:
            return True
        try:
            return request.user.organization == obj.ward
        except AttributeError:
            return False


class IsITOAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_ito_admin

    def has_object_permission(self, request, view, obj):
        if obj.__class__.__name__ == "Nagarpalika":
            return request.user.ito_profile.nagarpalika == obj
        return request.user.is_ito_admin


class CanCreatePaper(permissions.BasePermission):
    def has_permission(self, request, view):
        roles = ["ito_admin", "ward_admin"]
        if request.method not in permissions.SAFE_METHODS:
            return not request.user.role in roles
        else:
            return True


def can_create_user(current, level):
    return current.level < level


def can_increase_count(user, obj):
    if user.organization == obj.ward:
        return True
    raise PermissionDenied()


class HasApiKey(permissions.BasePermission):

    def has_permission(self, request, view):
        return False


# TODO: Ward/Nagarpalika etc create huda user faldine > response ma
# TODO: serializer bata pani object tanna milne raixa, tyo milaunu paryo > services ma.
