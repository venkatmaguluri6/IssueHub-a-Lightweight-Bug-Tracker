from rest_framework import serializers
from .models import Issue
from users.serializers import UserSerializer


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for Issue model"""
    reporter = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    project_key = serializers.CharField(source='project.key', read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'project', 'project_key', 'title', 'description',
            'status', 'priority', 'reporter', 'assignee', 'assignee_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reporter', 'created_at', 'updated_at']

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        if assignee_id:
            from users.models import User
            try:
                validated_data['assignee'] = User.objects.get(id=assignee_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"assignee_id": "User with this ID does not exist"})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        if assignee_id is not None:
            if assignee_id:
                from users.models import User
                try:
                    validated_data['assignee'] = User.objects.get(id=assignee_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError({"assignee_id": "User with this ID does not exist"})
            else:
                validated_data['assignee'] = None
        return super().update(instance, validated_data)

