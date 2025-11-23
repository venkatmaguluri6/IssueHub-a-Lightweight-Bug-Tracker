from rest_framework import permissions
from projects.models import ProjectMember


class IsIssueReporterOrMaintainer(permissions.BasePermission):
    """Permission to allow issue reporter or project maintainer to edit"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Anyone who is a project member can view
            return ProjectMember.objects.filter(
                project=obj.project,
                user=request.user
            ).exists()
        
        # For updates/deletes, check if user is reporter or maintainer
        is_reporter = obj.reporter == request.user
        is_maintainer = ProjectMember.objects.filter(
            project=obj.project,
            user=request.user,
            role='maintainer'
        ).exists()
        
        return is_reporter or is_maintainer


class CanChangeIssueStatus(permissions.BasePermission):
    """Permission to allow only maintainers to change issue status/assignee"""
    def has_object_permission(self, request, view, obj):
        # Only maintainers can change status and assignee
        if 'status' in request.data or 'assignee_id' in request.data:
            return ProjectMember.objects.filter(
                project=obj.project,
                user=request.user,
                role='maintainer'
            ).exists()
        return True

