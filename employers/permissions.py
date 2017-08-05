from rest_framework.permissions import BasePermission
from accounts.models import UserType

class IsEmployerOrNeither(BasePermission):
    """
    This permission class is used to determine if a user is either a employer (or an unassigned user)
    This is to prevent candidates from accessing information about employers
    """
    def has_permission(self, request, view):
        userType = UserType.objects.get(user=request.user)
        if userType.isEmployer == True or (userType.isEmployer == False and userType.isCandidate == False):
            return True
        else:
            return False
