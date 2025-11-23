from django.contrib import admin
from .models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['key', 'name', 'created_at']
    search_fields = ['name', 'key']
    list_filter = ['created_at']


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['project__name', 'user__email']
