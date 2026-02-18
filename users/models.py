# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('boy', 'Boy'),
        ('girl', 'Girl'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES, null=True, blank=True)
    dueDate = models.DateField(null=True, blank=True)
    avatarUrl = models.URLField(max_length=500, default='https://ac.goit.global/fullstack/react/default-avatar.jpg', null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    @property
    def current_week(self):
        """Calculate pregnancy week based on due date"""
        if not self.dueDate:
            return None
        from datetime import date
        today = date.today()
        days_until_due = (self.dueDate - today).days
        pregnancy_days = 280 - days_until_due  # 40 weeks = 280 days
        return max(1, min(40, pregnancy_days // 7 + 1))
