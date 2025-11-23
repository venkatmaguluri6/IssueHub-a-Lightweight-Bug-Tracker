from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Issue
from .serializers import IssueSerializer
from .permissions import IsIssueReporterOrMaintainer, CanChangeIssueStatus
from projects.models import ProjectMember


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet for Issue model"""
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssueReporterOrMaintainer, CanChangeIssueStatus]

    def get_queryset(self):
        # Check if project_pk is in URL kwargs (nested route)
        project_id = self.kwargs.get('project_pk') or self.request.query_params.get('project_id')
        queryset = Issue.objects.filter(
            project__memberships__user=self.request.user
        ).distinct()

        # Filter by project if provided
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        # Search by title/description
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by priority
        priority_filter = self.request.query_params.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        # Filter by assignee
        assignee_filter = self.request.query_params.get('assignee')
        if assignee_filter:
            queryset = queryset.filter(assignee_id=assignee_filter)

        # Sorting
        sort_by = self.request.query_params.get('sort', '-created_at')
        if sort_by in ['created_at', '-created_at', 'priority', '-priority', 'status', '-status']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def perform_create(self, serializer):
        # Check if project_pk is in URL kwargs (nested route)
        project_id = self.kwargs.get('project_pk')
        if not project_id:
            # Try to get from request data
            project_id = self.request.data.get('project')
        
        if not project_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"project": "Project ID is required"})
        
        # Convert to int if string
        try:
            project_id = int(project_id)
        except (ValueError, TypeError):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"project": "Invalid project ID"})
        
        # Verify user is a member of the project
        if not ProjectMember.objects.filter(
            project_id=project_id,
            user=self.request.user
        ).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You must be a member of the project to create issues")
        
        serializer.save(reporter=self.request.user, project_id=project_id)
