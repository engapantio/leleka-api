# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListCreateView.as_view(), name='tasks_list_create'),
    path('tasks/<uuid:task_id>/status/', views.update_task_status, name='update_task_status'),
]
