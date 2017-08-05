from rest_framework.permissions import BasePermission
from accounts.models import UserType

class IsOwner(BasePermission):
    """
    When a new user is creating a candidate or employer, this permission confirms the user is the one making their account
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsCandidateOrNeither(BasePermission):
    """
    Permission class which determines if the user is a candidate or neither, to prevent employers from looking at canidate information
    """
    def has_permission(self, request, view):
        userType = UserType.objects.get(user=request.user)
        if userType.isCandidate == True or (userType.isCandidate == False and userType.isEmployer == False):
            return True
        else:
            return False