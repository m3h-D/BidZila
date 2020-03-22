from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOfComment(BasePermission):
    """baraye edit kardane comment ha to blog be dard mikhure"""
    message = 'شما باید صاحب این کامنت باشید'

    def has_object_permission(self, request, view, obj):
        # user_safe_method = ['GET', 'PUT', 'PATCH']
        # if request.method in user_safe_method:
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
