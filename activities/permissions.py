from constance import config
from rest_framework import permissions


class SendPushPermission(permissions.BasePermission):
    """
    Global permission check for user to send push messages
    """
    def has_permission(self, request, view):
        user = request.user
        roles = user.role.all()
        for role in roles:
            if config.ROLE_AUTHORIZED == role.name:
                return True
