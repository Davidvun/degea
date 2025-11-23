from django import forms
from .models import Ministry, Program

class MinistryForm(forms.ModelForm):
    class Meta:
        model = Ministry
        fields = ['name', 'description', 'leader', 'volunteers', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'volunteers': forms.CheckboxSelectMultiple(),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'description', 'ministry', 'start_date', 'end_date', 'coordinator', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
