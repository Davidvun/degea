from django.contrib import admin
from .models import Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'age', 'date_joined', 'is_active']
    list_filter = ['gender', 'is_active', 'date_joined']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'skills', 'interests']
