from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'issue', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['body', 'author__email']
    raw_id_fields = ['issue', 'author']
