from django.db import models
from django.conf import settings


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('mass', 'Mass'),
        ('meeting', 'Meeting'),
        ('outreach', 'Outreach Program'),
        ('fundraiser', 'Fundraiser'),
        ('celebration', 'Celebration'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    ministry = models.ForeignKey('ministries.Ministry', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=300)
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='coordinated_events')
    assigned_volunteers = models.ManyToManyField('volunteers.Volunteer', related_name='assigned_events', blank=True)
    max_volunteers = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_datetime']
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime.date()}"
    
    def volunteer_count(self):
        return self.assigned_volunteers.count()


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey('volunteers.Volunteer', on_delete=models.CASCADE, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='tasks_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.assigned_to.user.get_full_name()}"


class EventReport(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
    )
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reports')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_reports')
    title = models.CharField(max_length=200)
    summary = models.TextField(help_text="Brief summary of the event")
    attendance_count = models.PositiveIntegerField(help_text="Number of attendees")
    volunteer_performance = models.TextField(help_text="Notes on volunteer performance")
    challenges = models.TextField(blank=True, help_text="Challenges encountered during the event")
    recommendations = models.TextField(blank=True, help_text="Recommendations for future events")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report: {self.event.title} by {self.submitted_by.get_full_name()}"
