from rest_framework import permissions
from users.models import UserRole


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user.is_authenticated and request.user.role == UserRole.EMPLOYEE
            )

        return True
