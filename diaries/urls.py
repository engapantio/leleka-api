# diaries/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('diaries/', views.DiaryListCreateView.as_view(), name='diary_list_create'),
    path('diaries/<uuid:entry_id>/', views.diary_detail, name='diary_detail'),
    path('emotions/', views.get_emotions_list, name='emotions_list'),
]
