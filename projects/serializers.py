from rest_framework import serializers
from .models import Project, ProjectMember
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    member_count = serializers.SerializerMethodField()
    maintainer_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'key', 'description', 'created_at', 'member_count', 'maintainer_count']
        read_only_fields = ['id', 'created_at']

    def get_member_count(self, obj):
        return obj.memberships.count()

    def get_maintainer_count(self, obj):
        return obj.memberships.filter(role='maintainer').count()


class ProjectMemberSerializer(serializers.ModelSerializer):
    """Serializer for ProjectMember model"""
    user = UserSerializer(read_only=True)
    user_email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'user_email', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user_email = validated_data.pop('user_email', None)
        if user_email:
            from users.models import User
            try:
                user = User.objects.get(email=user_email)
                validated_data['user'] = user
            except User.DoesNotExist:
                raise serializers.ValidationError({"user_email": "User with this email does not exist"})
        return super().create(validated_data)

