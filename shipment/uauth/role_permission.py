from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for unauthenticated users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsSystemAdministrator(permissions.BasePermission):
    """
    Allow access only for System Administrators.
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name == "System Administrator"
        return False


class IsClientAdministrator(permissions.BasePermission):
    """
    Allow access only for Client Administrators.
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name == "Client Administrator"
        return False


class IsClientUserReadOnly(permissions.BasePermission):
    """
    Allow access for Client Users with read-only permissions.
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name == "Client User (Read Only)"
        return False


class IsClientUserEditAndRead(permissions.BasePermission):
    """
    Allow access for Client Users with read and edit permissions.
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name == "Client User (Edit and Read)"
        return False


class IsSystemOrClientAdmin(permissions.BasePermission):
    """
    Allow access for System Administrators or Client Administrators.
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name in [
                "System Administrator",
                "Client Administrator"
            ]
        return False


class IsAnyClientUser(permissions.BasePermission):
    """
    Allow access for any Client User (Read Only or Edit and Read).
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name in [
                "Client User (Read Only)",
                "Client User (Edit and Read)"
            ]
        return False


class IsAuthenticatedUserWithRole(permissions.BasePermission):
    """
    Generic check to ensure the user has any defined role.
    """
    allowed_roles = [
        "System Administrator",
        "Client Administrator",
        "Client User (Read Only)",
        "Client User (Edit and Read)"
    ]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name in self.allowed_roles
        return False

class IsUser(permissions.BasePermission):
    """
    Allow access for Client Users with read-only permissions.
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.role and user.role.role_name == "User"
        return False

# [ 18/FEB/25 ]
class IsSuperAdmin(permissions.BasePermission):
    """
    Allow access only for Super Admins.
    Super Admins can view and manage all client data.
    """
    def has_permission(self, request, view):
        user = request.user
        # if user and user.is_authenticated:
        #     return user.is_admin or (user.role and user.role.role_name == "Super Admin")
        # return False
        if user.is_admin:
            return True
        return user.client_id is not None