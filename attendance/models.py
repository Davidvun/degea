from django.db import models
from django.conf import settings

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='attendance_records')
    volunteer = models.ForeignKey('volunteers.Volunteer', on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    notes = models.TextField(blank=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='marked_attendance')
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'volunteer')
        ordering = ['-marked_at']
    
    def __str__(self):
        return f"{self.volunteer} - {self.event.title} ({self.get_status_display()})"
