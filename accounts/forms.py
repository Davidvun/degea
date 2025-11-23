from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from volunteers.models import Volunteer


class VolunteerSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    
    gender = forms.ChoiceField(choices=Volunteer.GENDER_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-input'}))
    age = forms.IntegerField(min_value=1, max_value=120, required=True, widget=forms.NumberInput(attrs={'class': 'form-input'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}), required=False)
    interests = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}), required=True, help_text='Your interests and hobbies')
    skills = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}), required=True, help_text='Special skills or talents')
    availability = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}), required=True, help_text='When are you available?')
    supporting_document = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-input'}), help_text='Upload a supporting document (resume, ID, etc.)')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})


class UserManagementForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-input'}))
    assigned_ministry = forms.ModelChoiceField(queryset=None, required=False, widget=forms.Select(attrs={'class': 'form-input'}), help_text='Assign ministry for Priest or Coordinator')
    approval_status = forms.ChoiceField(choices=User.APPROVAL_STATUS_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-input'}))
    is_active = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    is_suspended = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'assigned_ministry', 'approval_status', 'is_active', 'is_suspended', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ministries.models import Ministry
        self.fields['assigned_ministry'].queryset = Ministry.objects.filter(is_active=True)
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})


class UserEditForm(forms.ModelForm):
    assigned_ministry = forms.ModelChoiceField(queryset=None, required=False, widget=forms.Select(attrs={'class': 'form-input'}), help_text='Assign ministry for Priest or Coordinator')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'assigned_ministry', 'approval_status', 'is_active', 'is_suspended', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'role': forms.Select(attrs={'class': 'form-input'}),
            'approval_status': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_suspended': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ministries.models import Ministry
        self.fields['assigned_ministry'].queryset = Ministry.objects.filter(is_active=True)
