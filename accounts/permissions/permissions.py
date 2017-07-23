from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    When a new user is creating a candidate or employer, this permission confirms the user is the one making their account
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user