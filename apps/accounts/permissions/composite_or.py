from rest_framework.permissions import BasePermission


def CompositeOr(*permission_classes):
    class _Permission(BasePermission):
        def has_permission(self, request, view):
            return self.evaluate_permission(
                'has_permission', request, view)

        def has_object_permission(self, request, view, obj):
            return self.evaluate_permission(
                'has_object_permission', request, view, obj)

        def evaluate_permission(self, name, *args, **kwargs):
            for permission_class in permission_classes:
                permission_instance = permission_class()

                if getattr(permission_instance, name)(*args, **kwargs):
                    return True

            return False

    return _Permission
