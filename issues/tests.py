from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from projects.models import Project, ProjectMember
from .models import Issue

User = get_user_model()


class IssueTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            name='Test User',
            password='testpass123'
        )
        self.project = Project.objects.create(name='Test Project', key='TEST')
        ProjectMember.objects.create(project=self.project, user=self.user, role='member')
        self.client.force_authenticate(user=self.user)

    def test_create_issue(self):
        """Test creating an issue"""
        data = {
            'project': self.project.id,
            'title': 'Test Issue',
            'description': 'Test description',
            'priority': 'high',
        }
        response = self.client.post(f'/api/projects/{self.project.id}/issues/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Issue.objects.filter(title='Test Issue').exists())

    def test_list_issues(self):
        """Test listing issues"""
        issue = Issue.objects.create(
            project=self.project,
            title='Test Issue',
            description='Test',
            reporter=self.user
        )
        
        response = self.client.get(f'/api/projects/{self.project.id}/issues/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        issues = response.data['results'] if 'results' in response.data else response.data
        self.assertTrue(len(issues) > 0)

    def test_filter_issues_by_status(self):
        """Test filtering issues by status"""
        Issue.objects.create(
            project=self.project,
            title='Open Issue',
            description='Test',
            reporter=self.user,
            status='open'
        )
        Issue.objects.create(
            project=self.project,
            title='Closed Issue',
            description='Test',
            reporter=self.user,
            status='closed'
        )
        
        response = self.client.get(f'/api/projects/{self.project.id}/issues/?status=open')
        issues = response.data['results'] if 'results' in response.data else response.data
        self.assertTrue(all(issue['status'] == 'open' for issue in issues))
