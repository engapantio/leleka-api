# journey/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('weeks/current/', csrf_exempt(views.get_current_week), name='current_week'),
    path('weeks/<int:weekNumber>/', csrf_exempt(views.get_week_full_data), name='week_data'),
    path('weeks/<int:weekNumber>/baby/', csrf_exempt(views.get_baby_state), name='baby_state'),
    path('weeks/<int:weekNumber>/mom/', csrf_exempt(views.get_mom_state), name='mom_state'),
]

