"""
Seed script to create demo data for IssueHub
Run with: python manage.py shell < seed_data.py
Or: python manage.py shell, then exec(open('seed_data.py').read())
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'issuehub_backend.settings')
django.setup()

from users.models import User
from projects.models import Project, ProjectMember
from issues.models import Issue
from comments.models import Comment
import random

# Clear existing data (optional - comment out if you want to keep existing data)
# User.objects.exclude(is_superuser=True).delete()
# Project.objects.all().delete()

# Create users
print("Creating users...")
users = []
for i in range(1, 6):
    email = f"user{i}@example.com"
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'name': f'User {i}',
            'username': f'user{i}'
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    users.append(user)
    print(f"  Created/Found user: {user.email}")

# Create projects
print("\nCreating projects...")
projects = []
project_data = [
    {'name': 'Web Application', 'key': 'WEBAPP'},
    {'name': 'Mobile App', 'key': 'MOBILE'},
]

for p_data in project_data:
    project, created = Project.objects.get_or_create(
        key=p_data['key'],
        defaults={'name': p_data['name'], 'description': f'Description for {p_data["name"]}'}
    )
    projects.append(project)
    print(f"  Created/Found project: {project.key} - {project.name}")
    
    # Add maintainer (first user)
    ProjectMember.objects.get_or_create(
        project=project,
        user=users[0],
        defaults={'role': 'maintainer'}
    )
    
    # Add some members
    for user in users[1:3]:
        ProjectMember.objects.get_or_create(
            project=project,
            user=user,
            defaults={'role': 'member'}
        )

# Create issues
print("\nCreating issues...")
statuses = ['open', 'in_progress', 'resolved', 'closed']
priorities = ['low', 'medium', 'high', 'critical']
issue_titles = [
    'Fix login button styling',
    'Add user profile page',
    'Implement dark mode',
    'Fix API rate limiting',
    'Add email notifications',
    'Improve search functionality',
    'Fix memory leak in dashboard',
    'Add unit tests for auth',
    'Update documentation',
    'Fix responsive layout on mobile',
    'Add export to CSV feature',
    'Implement file upload',
    'Fix password reset flow',
    'Add two-factor authentication',
    'Optimize database queries',
    'Fix CORS issues',
    'Add activity log',
    'Implement pagination',
    'Fix date picker bug',
    'Add keyboard shortcuts',
]

issue_descriptions = [
    'The login button needs better styling to match the design system.',
    'Users should be able to view and edit their profiles.',
    'Dark mode support would improve user experience.',
    'API rate limiting is not working correctly.',
    'Users should receive email notifications for important events.',
    'Search functionality needs improvement for better results.',
    'There is a memory leak in the dashboard component.',
    'We need comprehensive unit tests for authentication.',
    'Documentation needs to be updated with latest changes.',
    'Layout breaks on mobile devices.',
    'Users want to export data to CSV format.',
    'File upload feature is missing.',
    'Password reset flow has some issues.',
    'Two-factor authentication would improve security.',
    'Database queries need optimization.',
    'CORS issues are preventing API calls.',
    'Activity log would help track user actions.',
    'Pagination is needed for large lists.',
    'Date picker has a bug with timezone handling.',
    'Keyboard shortcuts would improve productivity.',
]

issue_count = 0
for project in projects:
    for i, title in enumerate(issue_titles[:10]):  # 10 issues per project
        issue = Issue.objects.create(
            project=project,
            title=title,
            description=issue_descriptions[i],
            status=random.choice(statuses),
            priority=random.choice(priorities),
            reporter=random.choice(users),
            assignee=random.choice(users) if random.random() > 0.3 else None,
        )
        issue_count += 1
        
        # Add some comments to issues
        if random.random() > 0.5:
            Comment.objects.create(
                issue=issue,
                author=random.choice(users),
                body=f'This is a comment on issue {issue.title}. Let me know if you need any clarification.'
            )
            if random.random() > 0.7:
                Comment.objects.create(
                    issue=issue,
                    author=random.choice(users),
                    body='Thanks for the update! I will review this soon.'
                )

print(f"  Created {issue_count} issues")

# Summary
print("\n" + "="*50)
print("Seed data created successfully!")
print("="*50)
print(f"Users: {User.objects.count()}")
print(f"Projects: {Project.objects.count()}")
print(f"Project Members: {ProjectMember.objects.count()}")
print(f"Issues: {Issue.objects.count()}")
print(f"Comments: {Comment.objects.count()}")
print("\nTest credentials:")
print("  Email: user1@example.com")
print("  Password: password123")

