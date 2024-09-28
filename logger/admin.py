from django.contrib import admin
from .models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("path", "user", "created_at")


admin.site.register(LogEntry, LogEntryAdmin)
