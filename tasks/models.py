# tasks/models.py
from django.db import models
from django.conf import settings
from datetime import date
import uuid

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    date = models.CharField(max_length=10, default=date.today())
    isDone = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-createdAt']
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{self.title} - {self.status}"
