# diaries/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import DiaryEntry, Emotion
from .serializers import DiaryEntrySerializer

# @extend_schema(
#     responses={200: OpenApiTypes.OBJECT},  # {'entries': DiaryEntrySerializer(many=True)}
#     examples=[
#         OpenApiExample('Empty', value={'entries': []}, status_code=200),
#     ]
# )
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def diary_list_create(request):
    if request.method == 'GET':
        entries = DiaryEntry.objects.filter(user=request.user)
        serializer = DiaryEntrySerializer(entries, many=True)
        return Response({'entries': serializer.data})

    elif request.method == 'POST':
        serializer = DiaryEntrySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# @extend_schema(
#     request=DiaryEntrySerializer,  # Request schema
#     responses={200: DiaryEntrySerializer}
# )
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def diary_detail(request, entry_id):
    try:
        entry = DiaryEntry.objects.get(id=entry_id, user=request.user)
    except DiaryEntry.DoesNotExist:
        return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DiaryEntrySerializer(entry)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = DiaryEntrySerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # EXPLICIT M2M UPDATE - This is the key fix
        emotions_data = request.data.get('emotions', [])
        if emotions_data:  # Only if provided
            valid_emotions = []
            for emotion_id in emotions_data:
                try:
                    emotion = Emotion.objects.get(id=emotion_id)
                    valid_emotions.append(emotion)
                except Emotion.DoesNotExist:
                    return Response({'error': f'Emotion {emotion_id} not found'}, status=400)
            entry.emotions.set(valid_emotions)  # FORCE M2M update

        # Update other fields
        for field, value in serializer.validated_data.items():
            if field != 'emotions':  # Skip emotions (handled above)
                setattr(entry, field, value)

        entry.save()
        entry.refresh_from_db()

        serializer = DiaryEntrySerializer(entry)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @extend_schema(responses={200: OpenApiTypes.OBJECT})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_emotions_list(request):
    """Return all available emotions"""
    from .models import Emotion
    emotions = Emotion.objects.values('id', 'title')
    return Response({'emotions': list(emotions)})
