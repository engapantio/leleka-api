# users/views.py
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes,  permission_classes
from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
import cloudinary.uploader
from .serializers import RegisterSerializer, UserSerializer, UpdateProfileSerializer, LoginSerializer, RefreshSerializer
import secrets
from .models import User
from .auth import CsrfExemptSessionAuthentication

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         login(request, user)

#         # Generate tokens
#         refresh = RefreshToken.for_user(user)

#         # Set tokens in HTTP-only cookies
#         response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
#         response.set_cookie(
#             key='access_token',
#             value=str(refresh.access_token),
#             httponly=True,
#             secure=not settings.DEBUG,
#             samesite='Lax',
#             max_age=60 * 60  # 60 minutes
#         )
#         response.set_cookie(
#             key='refresh_token',
#             value=str(refresh),
#             httponly=True,
#             secure=not settings.DEBUG,
#             samesite='Lax',
#             max_age=60 * 60 * 24 * 7  # 7 days
#         )

#         return response

# class LoginView(TokenObtainPairView):
#     permission_classes = (AllowAny,)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = User.objects.get(email=request.data['email'])

#         refresh = RefreshToken.for_user(user)

#         response = Response(UserSerializer(user).data)
#         response.set_cookie(
#             key='access_token',
#             value=str(refresh.access_token),
#             httponly=True,
#             secure=not settings.DEBUG,
#             samesite='Lax',
#             max_age=60 * 60
#         )
#         response.set_cookie(
#             key='refresh_token',
#             value=str(refresh),
#             httponly=True,
#             secure=not settings.DEBUG,
#             samesite='Lax',
#             max_age=60 * 60 * 24 * 7
#         )

#         return response
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)  # + sessionid
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(64)
        request.session['userId'] = str(user.id)
        request.session['accessToken'] = access_token
        request.session['refreshToken'] = refresh_token
        request.session.save()
        user_data = UserSerializer(user).data
        response=Response({"user": user_data},status=status.HTTP_201_CREATED)
        response.set_cookie('accessToken', access_token, max_age=3600, httponly=True)
        response.set_cookie('refreshToken', refresh_token, max_age=7*86400, httponly=True)
        return response
    email = request.data.get('email')
    if email and User.objects.filter(email=email).exists():
        return Response({'email': 'Email already in use'}, status=status.HTTP_409_CONFLICT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user:
        login(request, user)  # ✅ Sets sessionid cookie
        request.session['userId'] = str(user.id)
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(64)
        request.session['refreshToken'] = refresh_token
        request.session['accessToken'] = access_token
        request.session.save()
        user_data = UserSerializer(user).data
        response=Response({"user": user_data})
        response.set_cookie('accessToken', access_token, max_age=3600, httponly=True)
        response.set_cookie('refreshToken', refresh_token, max_age=7*86400, httponly=True)
        return response
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = Response({'message': 'Logged out'})

    # Delete ALL auth cookies
    response.set_cookie('accessToken', '', max_age=0, expires='Thu, 01 Jan 1970 00:00:00 GMT')
    response.set_cookie('refreshToken', '', max_age=0, expires='Thu, 01 Jan 1970 00:00:00 GMT')
    response.set_cookie('sessionid', '', max_age=0, expires='Thu, 01 Jan 1970 00:00:00 GMT')

    request.session.flush()

    return response


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @method_decorator(csrf_exempt, name='dispatch')
# def logout_view(request):
#     response = Response({'message': 'Logged out successfully'})
#     response.delete_cookie('access_token')
#     response.delete_cookie('refresh_token')
#     return response


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @method_decorator(csrf_exempt, name='dispatch')
# def check_session(request):
#     return Response({'success': True})


@api_view(['GET'])
def check_session(request):
    return Response({'authenticated': request.user.is_authenticated})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PATCH'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(UserSerializer(request.user).data)


@api_view(['PATCH'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def upload_avatar(request):
    print("CONTENT_TYPE:", request.content_type)      # multipart/form-data?
    print("FILES:", request.FILES.keys())             # avatar?
    print("DATA:", request.data)                      # {}

    if 'avatar' not in request.FILES:
        return Response({'error': 'No avatar'}, status=400)

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        request.FILES['avatar'],
        folder="avatars/leleka-app",  # Organize
        transformation=[{'width': 300, 'height': 300, 'crop': 'fill', 'gravity': 'auto'}]
    )

    # Save ONLY URL to User
    request.user.avatarUrl = upload_result['secure_url']
    request.user.save()

    return Response({
        'user': UserSerializer(request.user).data
    })



@api_view(['POST'])
@permission_classes([AllowAny])
def auth_refresh(request):
    # Force session load (modifies → triggers save/load)
    session_key = request.COOKIES.get('sessionid')
    refresh_token_cookie = request.COOKIES.get('refreshToken')

    if not session_key or not refresh_token_cookie:
        return Response({"error": "Missing cookies"}, status=400)

    # TRIGGER LOAD (no DB)
    if not request.session.session_key:
        request.session.modified = True  # Force backend load

    session = request.session
    user_id = session.get('userId')
    stored_refresh = session.get('refreshToken')


    if not user_id or refresh_token_cookie != stored_refresh:
        return Response({"error": "Invalid session/token"}, status=400)

    # NEW SESSION (flush old data)
    request.session.flush()
    request.session['userId'] = user_id
    access_token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(64)
    request.session['accessToken'] = access_token
    request.session['refreshToken'] = refresh_token
    request.session.save()

    response = Response({
        'accessToken': access_token,
        'refreshToken': refresh_token,
        'user': {'id': user_id}
    })
    response.set_cookie('sessionid', request.session.session_key, httponly=True)
    response.set_cookie('accessToken', access_token, max_age=3600, httponly=True, secure=not settings.DEBUG)
    response.set_cookie('refreshToken', refresh_token,max_age=7*86400, httponly=True, secure=not settings.DEBUG)
    return response
