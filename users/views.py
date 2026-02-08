# users/views.py
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes,  permission_classes
from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
import cloudinary.uploader
from django.conf import settings
from .serializers import RegisterSerializer, UserSerializer, UpdateProfileSerializer, LoginSerializer
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
        login(request, user)  # ✅ Auto-login + sessionid
        return Response({'message': 'Registered + logged in'})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user:
        login(request, user)  # ✅ Sets sessionid cookie
        return Response({'message': 'Login successful', 'user': {'email': user.email}})
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    logout(request)  # ✅ Clears sessionid
    return Response({'message': 'Logged out'})


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
    request.user.avatar_url = upload_result['secure_url']
    request.user.save()

    return Response({
        'user': UserSerializer(request.user).data
    })
