from django.db import models
from django.conf import settings


class Project(models.Model):
    status_choice = [
        ('active', 'active'),
        ('Inactive', 'Inactive')
    ]
    """Project model"""
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=50, unique=True)  # Project key like "PROJ", "ISSUE"
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choice, default='active')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.key} - {self.name}"


class ProjectMember(models.Model):
    """Project membership with roles"""
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('maintainer', 'Maintainer'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.project.key} ({self.role})"
