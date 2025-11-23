from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['event', 'volunteer', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class BulkAttendanceForm(forms.Form):
    event = forms.ModelChoiceField(queryset=None, required=True)
    
    def __init__(self, *args, **kwargs):
        from events.models import Event
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.filter(is_active=True)
