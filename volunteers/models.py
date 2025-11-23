from django.db import models
from django.conf import settings

class Volunteer(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    address = models.TextField(blank=True)
    interests = models.TextField(help_text='Volunteer interests and hobbies')
    skills = models.TextField(help_text='Special skills or talents')
    availability = models.TextField(help_text='When the volunteer is available')
    supporting_document = models.FileField(upload_to='volunteer_documents/', blank=True, null=True, help_text='Upload a supporting document (resume, ID, etc.)')
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"
    
    class Meta:
        ordering = ['-date_joined']
