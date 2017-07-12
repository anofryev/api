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


class Composite(object):
    """
    Composite wrapper for permission classes

    Usage:
    Composite(FirstClass) | Composite(SecondClass)

    or with shorthand:
    C(FirstClass) | C(SecondClass)
    """

    def __init__(self, permission_class):
        self.permission_class = permission_class

    def __or__(self, another_permission_class):
        return CompositeOr(self.permission_class, another_permission_class)

    def __ior__(self, another_permission_class):
        return CompositeOr(self.permission_class, another_permission_class)

    def __call__(self, *args, **kwargs):
        return self.permission_class(*args, **kwargs)


# Shorthand
C = Composite
