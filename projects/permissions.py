from rest_framework import permissions
from .models import ProjectMember


class IsProjectMember(permissions.BasePermission):
    """Permission to check if user is a member of the project"""
    def has_object_permission(self, request, view, obj):
        return ProjectMember.objects.filter(
            project=obj,
            user=request.user
        ).exists()


class IsProjectMaintainer(permissions.BasePermission):
    """Permission to check if user is a maintainer of the project"""
    def has_object_permission(self, request, view, obj):
        return ProjectMember.objects.filter(
            project=obj,
            user=request.user,
            role='maintainer'
        ).exists()


class IsProjectMaintainerOrReadOnly(permissions.BasePermission):
    """Permission to allow maintainers to edit, others to read"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return ProjectMember.objects.filter(
                project=obj,
                user=request.user
            ).exists()
        return ProjectMember.objects.filter(
            project=obj,
            user=request.user,
            role='maintainer'
        ).exists()

