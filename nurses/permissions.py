from rest_framework import permissions

class IsNurse(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.employee.type == 'N'