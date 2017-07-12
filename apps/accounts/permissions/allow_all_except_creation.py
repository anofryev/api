from rest_framework.permissions import BasePermission


class AllowAllExceptCreation(BasePermission):
    def has_permission(self, request, view):
        return request.method != 'POST'
