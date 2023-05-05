from rest_framework.permissions import BasePermission


class PermissionByAction(BasePermission):

    def __init__(self, allowed_actions):
        self.allowed_actions = allowed_actions

    def has_permission(self, request, view):
        action = view.action

        if action in self.allowed_actions:
            return True

        return False
