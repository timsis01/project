from django.db import models
from django.conf import settings
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=500)
    is_done = models.BooleanField(default=False)
    date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['is_done', '-created_at']
