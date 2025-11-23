from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('priest', 'Priest'),
        ('coordinator', 'Coordinator'),
        ('volunteer', 'Volunteer'),
    )
    
    APPROVAL_STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='approved')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    assigned_ministry = models.ForeignKey('ministries.Ministry', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_staff', help_text='Ministry assigned to Priest or Coordinator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_suspended = models.BooleanField(default=False, help_text='Suspended users cannot log in')
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def is_administrator(self):
        return self.role == 'administrator'
    
    def is_priest(self):
        return self.role == 'priest'
    
    def is_coordinator(self):
        return self.role == 'coordinator'
    
    def is_volunteer_user(self):
        return self.role == 'volunteer'
    
    def can_manage_volunteers(self):
        return self.role in ['administrator', 'coordinator', 'priest']
    
    def can_manage_all_users(self):
        return self.role == 'administrator'
    
    def can_assign_roles(self):
        return self.role in ['administrator', 'priest']
    
    def can_approve_volunteers(self):
        return self.role in ['administrator', 'priest']
    
    def can_schedule_events(self):
        return self.role in ['administrator', 'priest', 'coordinator']
    
    def can_assign_volunteers_to_events(self):
        return self.role in ['administrator', 'priest', 'coordinator']
    
    def can_track_attendance(self):
        return self.role in ['administrator', 'priest', 'coordinator']
    
    def can_send_communications(self):
        return self.role in ['administrator', 'priest', 'coordinator']
    
    def can_view_reports(self):
        return self.role in ['administrator', 'priest', 'coordinator']
    
    def can_export_reports(self):
        return self.role in ['administrator', 'priest']
    
    def can_view_audit_logs(self):
        return self.role == 'administrator'
    
    def can_manage_ministries(self):
        return self.role == 'administrator'
    
    def can_assign_priests(self):
        return self.role == 'administrator'
    
    def can_make_coordinator(self):
        return self.role in ['administrator', 'priest']
    
    def can_provide_feedback(self):
        return self.role in ['administrator', 'priest', 'coordinator']
    
    def get_managed_ministry(self):
        if self.is_priest() or self.is_coordinator():
            return self.assigned_ministry
        return None
    
    def get_ministry_volunteers(self):
        ministry = self.get_managed_ministry()
        if ministry:
            return ministry.volunteers.all()
        return None
    
    def is_approved(self):
        return self.approval_status == 'approved'
    
    def is_pending_approval(self):
        return self.approval_status == 'pending'
    
    def can_login(self):
        return self.is_active and not self.is_suspended and self.is_approved()
