from django import forms
from .models import VolunteerEvaluation, EventFeedback

class VolunteerEvaluationForm(forms.ModelForm):
    class Meta:
        model = VolunteerEvaluation
        fields = ['volunteer', 'event', 'rating', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

class EventFeedbackForm(forms.ModelForm):
    class Meta:
        model = EventFeedback
        fields = ['event', 'volunteer', 'feedback', 'suggestions', 'would_participate_again']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
            'suggestions': forms.Textarea(attrs={'rows': 3}),
        }
