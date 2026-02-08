# diaries/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/diaries', views.diary_list_create, name='diary_list_create'),
    path('api/diaries/<uuid:entry_id>', views.diary_detail, name='diary_detail'),
]