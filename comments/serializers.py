from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'issue', 'created_at']
        read_only_fields = ['id', 'author', 'issue', 'created_at']
