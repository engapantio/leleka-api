# diaries/models.py
from django.db import models
from django.conf import settings
import uuid

class DiaryEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diary_entries')
    title = models.CharField(max_length=255)
    description = models.TextField()
    emotions = models.JSONField(default=list)  # Store as array
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Diary entries'
    
    def __str__(self):
        return f"{self.user.name} - {self.title}"

class Emotion(models.Model):
    title = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.title