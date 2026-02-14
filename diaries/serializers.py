# diaries/serializers.py
from rest_framework import serializers
from .models import DiaryEntry, Emotion

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'title']

class DiaryEntrySerializer(serializers.ModelSerializer):
    emotions = serializers.PrimaryKeyRelatedField(
        queryset=Emotion.objects.all(),
        many=True,
        write_only=True,  # POST: IDs
        required=False
    )
    userId = serializers.UUIDField(source='user_id', read_only=True)
    # emotions = serializers.SerializerMethodField()  # Override for GET: objects
    class Meta:
        model = DiaryEntry
        fields = ['id', 'userId', 'date', 'title', 'description', 'emotions', 'createdAt', 'updatedAt']
        read_only_fields = ['id', 'userId', 'createdAt', 'updatedAt']
        # extra_kwargs = {'user': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Manually add emotions display after serialization
        data['emotions'] = [{'id': e.id, 'title': e.title} for e in instance.emotions.all()]
        return data

    # def get_emotions(self, obj):
    #     return EmotionSerializer(obj.emotions.all(), many=True).data

    def create(self, validated_data):
        emotions_data = validated_data.pop('emotions', [])
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)  # Create WITHOUT emotions
        if emotions_data:
            instance.emotions.set(emotions_data)  # Set M2M AFTER creation
        return instance

    def update(self, instance, validated_data):
        emotions = validated_data.pop('emotions', None)
        instance = super().update(instance, validated_data)
        if emotions is not None:  # Only if provided in PATCH
            instance.emotions.set(emotions)  # Explicit M2M replace
        return instance

    # def validate_emotions(self, value):
    #     if not value:  # Empty list
    #         raise serializers.ValidationError("At least 1 emotion required.")
    #     return value

    # def to_internal_value(self, data):
    #     print(f"Input data: {data}")  # Debug line
    #     if 'emotions' in data:
    #         emotions_data = data['emotions']
    #         print(f"Emotions data: {emotions_data}")  # Debug
    #         emotion_ids = []
    #         for emotion in emotions_data:
    #             emotion_obj = Emotion.objects.filter(id=emotion).first()
    #             if not emotion_obj:
    #                 print(f"Invalid emotion ID: {emotion}")  # Will show if 7 invalid
    #             else:
    #                 emotion_ids.append(emotion)
    #         data['emotions'] = emotion_ids
    #         print(f"Final emotion_ids: {emotion_ids}")  # Debug
    #     return super().to_internal_value(data)
