# tasks/serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    userId = serializers.UUIDField(source='user_id', read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'userId', 'name', 'date', 'isDone', 'createdAt', 'updatedAt']
        read_only_fields = ['id', 'userId','createdAt', 'updatedAt']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TaskStatusUpdateSerializer(serializers.Serializer):
    isDone = serializers.ChoiceField(choices=[False, True])
