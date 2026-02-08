# journey/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('api/weeks/current/', csrf_exempt(views.get_current_week), name='current_week'),
    path('api/weeks/<int:week_number>/', csrf_exempt(views.get_week_full_data), name='week_data'),
    path('api/weeks/<int:week_number>/baby/', csrf_exempt(views.get_baby_state), name='baby_state'),
    path('api/weeks/<int:week_number>/mom/', csrf_exempt(views.get_mom_state), name='mom_state'),
]

