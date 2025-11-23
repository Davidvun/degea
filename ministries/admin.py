from django.contrib import admin
from .models import Ministry, Program

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'volunteer_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry', 'start_date', 'end_date', 'coordinator', 'is_active']
    list_filter = ['is_active', 'ministry', 'start_date']
    search_fields = ['name', 'description']
