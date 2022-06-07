from rest_framework import permissions
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, BasePermission)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class AuthorStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in 'GET'
            or request.user.is_moderator or request.user.is_admin
            or request.user == obj.author
        )

      
class IsAuthorOrModeratorOrAdminOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly
):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in 'GET'
            or request.user.is_moderator or request.user.is_admin
            or request.user == obj.author
        )


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in 'GET'
            or request.user.is_authenticated
            and request.user.is_admin
        )