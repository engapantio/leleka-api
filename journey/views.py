# journey/views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import WeekData
from .serializers import BabyDataSerializer, MomDataSerializer, FullWeekDataSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_week(request):
    """Get current week based on user's due date"""
    current_week = request.user.current_week
    if not current_week:
        return Response({'error': 'Due date not set'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        week_data = WeekData.objects.prefetch_related(
            'comfortTips', 'momFeelings'
        ).get(weekNumber=current_week)
        serializer = FullWeekDataSerializer(week_data)
        data = serializer.data

        # Ensure exact structure
        response_data = {
            "weekNumber": data['weekNumber'],
            "daysToChildbirth": data['daysToChildbirth'],
            "baby": data['baby'],
            "momTip": data['momTip']
        }
        return Response(response_data)
    except WeekData.DoesNotExist:
        return Response({'error': f'Week {current_week} data not found'}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_week_full_data(request, weekNumber):
    """Get complete week data (public endpoint for demo)"""
    try:
        week_data = WeekData.objects.prefetch_related('comfortTips', 'momFeelings').get(weekNumber=weekNumber)
        serializer = FullWeekDataSerializer(week_data)
        return Response(serializer.data)
    except WeekData.DoesNotExist:
        return Response({'error': 'Week not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_baby_state(request, weekNumber):
    """Get baby development data for specific week"""
    try:
        week_data = WeekData.objects.get(weekNumber=weekNumber)
        serializer = BabyDataSerializer(week_data)
        return Response(serializer.data)
    except WeekData.DoesNotExist:
        return Response({'error': 'Week not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mom_state(request, weekNumber):
    """Get mom tips and feelings for specific week"""
    try:
        week_data = WeekData.objects.prefetch_related('comfortTips', 'momFeelings').get(weekNumber=weekNumber)
        serializer = MomDataSerializer(week_data)
        return Response(serializer.data)
    except WeekData.DoesNotExist:
        return Response({'error': 'Week not found'}, status=status.HTTP_404_NOT_FOUND)

