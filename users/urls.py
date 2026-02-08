# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/register', views.RegisterView.as_view(), name='register'),
    path('api/auth/login', views.LoginView.as_view(), name='login'),
    path('api/auth/logout', views.logout_view, name='logout'),
    path('api/auth/check', views.check_session, name='check_session'),
    path('api/users/current', views.current_user, name='current_user'),
    path('api/users', views.update_profile, name='update_profile'),
    path('api/users/avatar', views.upload_avatar, name='upload_avatar'),
]