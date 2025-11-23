from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'created_at']
    search_fields = ['email', 'name']
    ordering = ['email']
