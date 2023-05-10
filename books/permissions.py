from rest_framework import permissions
from users.models import UserRole


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.role == UserRole.EMPLOYEE
