from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from projects.models import ProjectMember


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_pk')
        if issue_id:
            return Comment.objects.filter(issue_id=issue_id)
        return Comment.objects.none()

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_pk')
        # Verify user is a member of the project
        from issues.models import Issue
        try:
            issue = Issue.objects.get(id=issue_id)
            if not ProjectMember.objects.filter(
                project=issue.project,
                user=self.request.user
            ).exists():
                raise PermissionError("You must be a member of the project to comment")
            serializer.save(author=self.request.user, issue=issue)
        except Issue.DoesNotExist:
            raise ValueError("Issue not found")
