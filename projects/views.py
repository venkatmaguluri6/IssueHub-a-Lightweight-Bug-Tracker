from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer
from .permissions import IsProjectMaintainerOrReadOnly, IsProjectMaintainer
from users.models import User


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for Project model"""
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectMaintainerOrReadOnly]

    def get_queryset(self):
        # Return only projects where user is a member
        return Project.objects.filter(
            memberships__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save()
        # Add creator as maintainer
        ProjectMember.objects.create(
            project=project,
            user=self.request.user,
            role='maintainer'
        )

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated, IsProjectMaintainerOrReadOnly])
    def members(self, request, pk=None):
        """Get or add members to the project"""
        project = self.get_object()
        
        if request.method == 'GET':
            members = ProjectMember.objects.filter(project=project)
            return Response(ProjectMemberSerializer(members, many=True).data)
        
        # POST - only maintainers can add members
        if not IsProjectMaintainer().has_object_permission(request, self, project):
            return Response({
                'error': {'code': 403, 'message': 'Only maintainers can add members'}
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectMemberSerializer(data={
            **request.data,
            'project': project.id
        })
        
        if serializer.is_valid():
            # Check if user is already a member
            user_email = request.data.get('user_email')
            if user_email:
                try:
                    user = User.objects.get(email=user_email)
                    member, created = ProjectMember.objects.get_or_create(
                        project=project,
                        user=user,
                        defaults={'role': request.data.get('role', 'member')}
                    )
                    if not created:
                        member.role = request.data.get('role', member.role)
                        member.save()
                    return Response(ProjectMemberSerializer(member).data, status=status.HTTP_201_CREATED)
                except User.DoesNotExist:
                    return Response({
                        'error': {'code': 404, 'message': 'User with this email does not exist'}
                    }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'error': {'code': 400, 'message': 'Validation failed', 'details': serializer.errors}
        }, status=status.HTTP_400_BAD_REQUEST)
