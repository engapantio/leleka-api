# users/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('api/auth/register/', views.register_view),
    path('api/auth/login/', views.login_view),
    path('api/auth/logout/', csrf_exempt(views.logout_view)),
    path('api/auth/check/', views.check_session),
    path('api/users/current/', csrf_exempt(views.current_user), name='current_user'),
    path('api/users/', csrf_exempt(views.update_profile), name='update_profile'),
    path('api/users/avatar/', csrf_exempt(views.upload_avatar), name='upload_avatar'),
]
