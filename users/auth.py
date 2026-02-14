# from rest_framework.authentication import SessionAuthentication

# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         return  # ← Disable CSRF check
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import User

class CsrfExemptSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.session.get('userId')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                return (user, None)
            except User.DoesNotExist:
                return None
        return None
