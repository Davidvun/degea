from django.contrib import admin
from .models import Announcement, EmailLog

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'created_by', 'is_active', 'created_at', 'expires_at']
    list_filter = ['priority', 'is_active', 'created_at']
    search_fields = ['title', 'message']
    filter_horizontal = ['target_ministries']

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sent_by', 'sent_at', 'success']
    list_filter = ['success', 'sent_at']
    search_fields = ['subject', 'recipients']
