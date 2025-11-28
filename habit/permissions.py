from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Разрешение, позволяющее просматривать объект только админу"""

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Если пользователь администратор, доступ разрешен
        if user.is_staff or user.is_superuser:
            return True


class IsOwner(BasePermission):
    """Разрешение, позволяющее просматривать объект только владельцу"""

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Если пользователь является владельцем привычки, доступ разрешен
        return obj.owner == user


class IsPublishedOrAuthenticated(BasePermission):
    """
    Разрешение, позволяющее просматривать объект всем авторизованным пользователям,
    если объект опубликован.
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_published
