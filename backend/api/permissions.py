from rest_framework.permissions import BasePermission

class IsSolicitante(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Requesters').exists()

class IsTecnico(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Technicians').exists()

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.groups.filter(name='Admins').exists()

class IsOwnerOrAssignedOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.groups.filter(name='Admins').exists():
            return True
        if request.user.groups.filter(name='Requesters').exists():
            return obj.created_by == request.user
        if request.user.groups.filter(name='Technicians').exists():
            return obj.assigned_to == request.user
        return False
