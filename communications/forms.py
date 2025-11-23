from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message', 'priority', 'target_roles', 'target_ministries', 
                  'is_active', 'expires_at']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'target_ministries': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'target_roles': 'Enter comma-separated roles (e.g., administrator,priest,coordinator,volunteer)'
        }
