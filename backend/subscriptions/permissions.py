from rest_framework.permissions import BasePermission

class HasValidSubscription(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request, 'subscription')
