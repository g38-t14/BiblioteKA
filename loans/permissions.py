from rest_framework import permissions


class IsLoanOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.loaner == request.user
