# journey/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_api),
    path('api/weeks/current/', views.get_current_week, name='current_week'),
    path('api/weeks/<int:week_number>/', views.get_week_full_data, name='week_data'),
    path('api/weeks/<int:week_number>/baby/', views.get_baby_state, name='baby_state'),
    path('api/weeks/<int:week_number>/mom/', views.get_mom_state, name='mom_state'),
    path('debug/', views.debug_api),
]

