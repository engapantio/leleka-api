# tasks/views.py
from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def tasks_list_create(request):
#     """
#     GET: /api/tasks - Get all user's tasks
#     POST: /api/tasks - Create new task
#     """
#     if request.method == 'GET':
#         tasks = Task.objects.filter(user=request.user)
#         serializer = TaskSerializer(tasks, many=True)
#         return Response({'tasks': serializer.data})

#     elif request.method == 'POST':
#         serializer = TaskSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']  # Enables ?date=YYYY-MM-DD filtering

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    """
    PATCH: /api/tasks/{task_id}/status - Toggle task status (checkbox)
    """
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskStatusUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Toggle checkbox logic
    new_status = serializer.validated_data['isDone']
    task.isDone = new_status
    task.save()

    return Response(TaskSerializer(task).data)
