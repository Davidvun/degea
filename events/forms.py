from django import forms
from .models import Event, Task, EventReport
from volunteers.models import Volunteer
from django.contrib.auth import get_user_model

User = get_user_model()

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'ministry', 'start_datetime', 
                  'end_datetime', 'location', 'coordinator', 'assigned_volunteers', 
                  'max_volunteers', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'assigned_volunteers': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_priest() and user.assigned_ministry:
            ministry = user.assigned_ministry
            
            self.fields['ministry'].widget = forms.HiddenInput()
            self.fields['ministry'].initial = ministry
            self.fields['ministry'].disabled = True
            
            self.fields['coordinator'].queryset = User.objects.filter(
                role='coordinator',
                assigned_ministry=ministry
            )
            
            self.fields['assigned_volunteers'].queryset = Volunteer.objects.filter(
                ministries=ministry
            )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if event and user:
            if user.is_coordinator() and user.assigned_ministry:
                self.fields['assigned_to'].queryset = Volunteer.objects.filter(
                    ministries=user.assigned_ministry
                )
            elif event.ministry:
                self.fields['assigned_to'].queryset = Volunteer.objects.filter(
                    ministries=event.ministry
                )


class EventReportForm(forms.ModelForm):
    class Meta:
        model = EventReport
        fields = ['title', 'summary', 'attendance_count', 'volunteer_performance', 
                  'challenges', 'recommendations', 'status']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'volunteer_performance': forms.Textarea(attrs={'rows': 3}),
            'challenges': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
        ]


class AddVolunteerToEventForm(forms.Form):
    volunteers = forms.ModelMultipleChoiceField(
        queryset=Volunteer.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Select Volunteers"
    )
    
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if event and user and user.assigned_ministry:
            current_volunteers = event.assigned_volunteers.all()
            self.fields['volunteers'].queryset = Volunteer.objects.filter(
                ministries=user.assigned_ministry
            ).exclude(id__in=current_volunteers.values_list('id', flat=True))
