from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'event', 'status', 'marked_by', 'marked_at']
    list_filter = ['status', 'marked_at']
    search_fields = ['volunteer__user__first_name', 'volunteer__user__last_name', 'event__title']
