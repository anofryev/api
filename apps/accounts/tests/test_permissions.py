from django.test import TestCase, mock
from rest_framework.permissions import BasePermission

from apps.accounts.permissions.composite import CompositeOr, Composite


class AlwaysFalsePermission(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class AlwaysTruePermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class CompositePermissionTestCase(TestCase):
    def test_composite_or_for_always_false(self):
        permission_class = CompositeOr(
            AlwaysFalsePermission, AlwaysFalsePermission)
        self.assertFalse(
            permission_class().has_permission(
                mock.Mock(), mock.Mock()))
        self.assertFalse(
            permission_class().has_object_permission(
                mock.Mock(), mock.Mock(), mock.Mock()))

    def test_composite_or_for_both_left(self):
        permission_class = CompositeOr(
            AlwaysFalsePermission, AlwaysTruePermission)
        self.assertTrue(
            permission_class().has_permission(
                mock.Mock(), mock.Mock()))
        self.assertTrue(
            permission_class().has_object_permission(
                mock.Mock(), mock.Mock(), mock.Mock()))

    def test_composite_or_for_both_right(self):
        permission_class = CompositeOr(
            AlwaysTruePermission, AlwaysFalsePermission)
        self.assertTrue(
            permission_class().has_permission(
                mock.Mock(), mock.Mock()))
        self.assertTrue(
            permission_class().has_object_permission(
                mock.Mock(), mock.Mock(), mock.Mock()))

    def test_composite_wrapper(self):
        permission_class = Composite(AlwaysFalsePermission)
        self.assertFalse(permission_class().has_permission(
            mock.Mock(), mock.Mock()))
        self.assertFalse(permission_class().has_object_permission(
            mock.Mock(), mock.Mock(), mock.Mock()))

        permission_class = Composite(AlwaysTruePermission)
        self.assertTrue(permission_class().has_permission(
            mock.Mock(), mock.Mock()))
        self.assertTrue(permission_class().has_object_permission(
            mock.Mock(), mock.Mock(), mock.Mock()))

    def test_composite_wrapper_or_left(self):
        permission_class = Composite(AlwaysFalsePermission) | \
                           Composite(AlwaysTruePermission)

        self.assertTrue(permission_class().has_permission(
            mock.Mock(), mock.Mock()))
        self.assertTrue(permission_class().has_object_permission(
            mock.Mock(), mock.Mock(), mock.Mock()))

    def test_composite_wrapper_or_right(self):
        permission_class = Composite(AlwaysTruePermission) | \
                           Composite(AlwaysFalsePermission)

        self.assertTrue(permission_class().has_permission(
            mock.Mock(), mock.Mock()))
        self.assertTrue(permission_class().has_object_permission(
            mock.Mock(), mock.Mock(), mock.Mock()))
