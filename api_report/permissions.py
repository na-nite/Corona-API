from rest_framework import permissions


class IsVisitor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 1

class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 2
