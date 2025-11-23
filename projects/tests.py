from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project, ProjectMember

User = get_user_model()


class ProjectTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            name='Test User',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        """Test creating a project"""
        data = {
            'name': 'Test Project',
            'key': 'TEST',
            'description': 'Test description',
        }
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(key='TEST').exists())
        
        # Check that creator is added as maintainer
        project = Project.objects.get(key='TEST')
        membership = ProjectMember.objects.get(project=project, user=self.user)
        self.assertEqual(membership.role, 'maintainer')

    def test_list_projects(self):
        """Test listing user's projects"""
        project = Project.objects.create(name='Test Project', key='TEST')
        ProjectMember.objects.create(project=project, user=self.user, role='member')
        
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results'] if 'results' in response.data else response.data), 1)

    def test_add_project_member(self):
        """Test adding a member to a project"""
        project = Project.objects.create(name='Test Project', key='TEST')
        ProjectMember.objects.create(project=project, user=self.user, role='maintainer')
        
        other_user = User.objects.create_user(
            email='member@example.com',
            username='member',
            name='Member User',
            password='testpass123'
        )
        
        response = self.client.post(f'/api/projects/{project.id}/members/', {
            'user_email': 'member@example.com',
            'role': 'member',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProjectMember.objects.filter(project=project, user=other_user).exists())
