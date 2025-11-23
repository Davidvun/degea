from django.contrib import admin
from .models import VolunteerEvaluation, EventFeedback

@admin.register(VolunteerEvaluation)
class VolunteerEvaluationAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'event', 'rating', 'evaluated_by', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['volunteer__user__first_name', 'volunteer__user__last_name', 'comments']

@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ['event', 'volunteer', 'would_participate_again', 'submitted_at']
    list_filter = ['would_participate_again', 'submitted_at']
    search_fields = ['event__title', 'volunteer__user__first_name', 'feedback']
