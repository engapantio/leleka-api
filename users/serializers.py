# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'gender', 'dueDate', 'avatarUrl', 'createdAt', 'updatedAt']
        read_only_fields = ['id', 'createdAt', 'updatedAt']
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'write_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Invalid email/password')
            data['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        return data

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'gender', 'dueDate']

class RefreshSerializer(serializers.Serializer):
    # No fields - all from cookies

    def validate(self, data):
        request = self.context['request']
        refresh_token = request.COOKIES.get('refreshToken')
        session_id = request.COOKIES.get('sessionid')


        if not refresh_token or not session_id:
            raise serializers.ValidationError("Missing refreshToken or sessionid cookies")

        session = request.session
        if not session.get('userId') or session.session_key != session_id:
            raise serializers.ValidationError("Invalid session")

        if not self.validate_refresh_token(refresh_token, session):
            raise serializers.ValidationError("Invalid refresh token")

        data['session'] = session
        data['refresh_token'] = refresh_token
        return data

    def validate_refresh_token(self, token, session):
        return token == session.get('refreshToken')
