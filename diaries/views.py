# diaries/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer

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

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def diary_detail(request, entry_id):
    try:
        entry = DiaryEntry.objects.get(id=entry_id, user=request.user)
    except DiaryEntry.DoesNotExist:
        return Response({'error': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DiaryEntrySerializer(entry)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = DiaryEntrySerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)