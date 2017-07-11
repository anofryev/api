from rest_framework.permissions import BasePermission


class ForbidCreation(BasePermission):
    def has_permission(self, request, view):
        return request.method != 'POST'
