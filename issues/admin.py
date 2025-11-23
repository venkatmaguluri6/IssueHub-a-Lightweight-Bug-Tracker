from django.contrib import admin
from .models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'title', 'status', 'priority', 'reporter', 'assignee', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['project', 'reporter', 'assignee']
