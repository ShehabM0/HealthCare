from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    message = {'message': 'User is not superuser.'}
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser

class IsPatient(permissions.BasePermission):
    message = {'message': 'User is not a patient.'}
    def has_permission(self, request, view):
        user = request.user
        return user.employee is None

class IsDoctor(permissions.BasePermission):
    message = {'message': 'User is not a doctor.'}
    def has_permission(self, request, view):
        user = request.user
        return user.employee.type == 'D' if user.employee else False

class IsNurse(permissions.BasePermission):
    message = {'message': 'User is not a nurse.'}
    def has_permission(self, request, view):
        user = request.user
        return user.employee.type == 'N' if user.employee else False

class IsHR(permissions.BasePermission):
    message = {'message': 'User is not an HR.'}
    def has_permission(self, request, view):
        user = request.user
        return user.employee.type == 'H' if user.employee else False

class IsPharmacist(permissions.BasePermission):
    message = {'message': 'User is not a Pharmacist.'}
    def has_permission(self, request, view):
        user = request.user
        return user.employee.type == 'P' if user.employee else False

class IsHeadDoctor(permissions.BasePermission):
    message = {'message': 'User is not a Head Doctor.'}
    def has_permission(self, request, view):
        user = request.user
        return user.employee.type == 'HD' if user.employee else False

class IsHeadNurse(permissions.BasePermission):
    message = {'message': 'User is not a Head Nurse.'}
    def has_permission(self, request, view):
        user = request.user
        return user.employee.type == 'HN' if user.employee else False
