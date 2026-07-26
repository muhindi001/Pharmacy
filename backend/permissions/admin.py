from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):

    required_permission = None

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        role = request.user.role

        if role is None:
            return False

        return role.permissions.filter(
            code=self.required_permission
        ).exists()