from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author', 'body', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

