from django.contrib import admin
from .models import Event, Task, EventReport


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'ministry', 'start_datetime', 'location', 'volunteer_count', 'is_active']
    list_filter = ['event_type', 'is_active', 'start_datetime', 'ministry']
    search_fields = ['title', 'description', 'location']
    filter_horizontal = ['assigned_volunteers']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'assigned_to', 'status', 'due_date', 'assigned_by', 'created_at']
    list_filter = ['status', 'due_date', 'created_at']
    search_fields = ['title', 'description', 'event__title', 'assigned_to__user__first_name', 'assigned_to__user__last_name']
    

@admin.register(EventReport)
class EventReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'submitted_by', 'status', 'attendance_count', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'created_at']
    search_fields = ['title', 'summary', 'event__title', 'submitted_by__first_name', 'submitted_by__last_name']
