from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class LogEntry(models.Model):
    path = models.CharField(max_length=25)
    method = models.CharField(max_length=10)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="log_entries",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.method} {self.path} - User: {self.user if self.user else 'Anonymous'} - Time: {self.created_at}"
