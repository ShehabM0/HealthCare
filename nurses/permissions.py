from rest_framework import permissions

class IsNurse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'N' and request.user.is_active == True