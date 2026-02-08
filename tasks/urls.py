# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/tasks', views.tasks_list_create, name='tasks_list_create'),
    path('api/tasks/<uuid:task_id>/status', views.update_task_status, name='update_task_status'),
]