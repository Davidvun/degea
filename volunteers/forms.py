from django import forms
from .models import Volunteer
from accounts.models import User
from ministries.models import Ministry

class VolunteerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    username = forms.CharField(max_length=150, required=True)
    ministries = forms.ModelMultipleChoiceField(
        queryset=Ministry.objects.filter(is_active=True),
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = Volunteer
        fields = ['gender', 'age', 'address', 'interests', 'skills', 'availability', 'ministries', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'availability': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance and instance.user:
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name
            self.fields['email'].initial = instance.user.email
            self.fields['phone'].initial = instance.user.phone
            self.fields['username'].initial = instance.user.username
    
    def save(self, commit=True):
        volunteer = super().save(commit=False)
        if not volunteer.user_id:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='volunteer'
            )
            user.phone = self.cleaned_data.get('phone', '')
            user.save()
            volunteer.user = user
        else:
            user = volunteer.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data.get('phone', '')
            user.save()
        
        if commit:
            volunteer.save()
            volunteer.ministries.set(self.cleaned_data['ministries'])
        return volunteer
