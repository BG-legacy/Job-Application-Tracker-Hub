from rest_framework import permissions

class IsTeamAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow team admins to edit.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is a team admin
        return obj.members.filter(
            user=request.user,
            role='Admin'
        ).exists()

class IsTeamMemberOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow team members or admins to access.
    """
    def has_object_permission(self, request, view, obj):
        return obj.members.filter(user=request.user).exists() 