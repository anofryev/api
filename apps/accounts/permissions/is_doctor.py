from rest_framework.permissions import IsAuthenticated

class IsDoctor(IsAuthenticated):
    def has_permission(self, request, view):
        if not super(IsDoctor, self).has_permission(request, view):
            return False

        return hasattr(request.user, 'doctor_role')
