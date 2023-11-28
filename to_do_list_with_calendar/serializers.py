from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task class.
    """

    class Meta:
        model = Task
        fields = '__all__'

    def validate_datetime(self, value):
        """
        Custom validation for the datetime field.
        """
        if value < timezone.now():
            raise serializers.ValidationError('Invalid date or time.')
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User class.
    """

    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'password',
            'email',
            'tasks',
            'validated',
            'is_superuser',
        ]

    def create(self, validated_data):
        """
        Correct creation of a new user encrypting password in serialization.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
