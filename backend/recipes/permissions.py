from rest_framework import permissions


class AuthorPermission(permissions.BasePermission):
    """Только автор может редактировать объект."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
