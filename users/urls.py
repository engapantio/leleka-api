# users/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/register/', views.register_view),
    path('auth/login/', views.login_view),
    path('auth/refresh/', views.auth_refresh, name='refresh'),
    path('auth/logout/', csrf_exempt(views.logout_view)),
    path('auth/check/', views.check_session),
    path('users/current/', csrf_exempt(views.current_user), name='current_user'),
    path('users/', csrf_exempt(views.update_profile), name='update_profile'),
    path('users/avatar/', csrf_exempt(views.upload_avatar), name='upload_avatar'),
]
