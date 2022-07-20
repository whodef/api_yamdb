from rest_framework import permissions


class OnlyAdminAndSuperuser(permissions.BasePermission):
    """Определяет права на изменения только для Суперпользователя
    или Админа.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):
    """Определяет права на изменения для админа и аутентифицированного
    пользователя или юзера со статусом ReadOnly.
    """

    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or (request.user
                    and request.user.is_authenticated
                    and request.user.role == 'admin'
                    )
                )
