from django.db import models
from django.conf import settings

class VolunteerEvaluation(models.Model):
    RATING_CHOICES = (
        (1, 'Poor'),
        (2, 'Below Average'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    )
    
    volunteer = models.ForeignKey('volunteers.Volunteer', on_delete=models.CASCADE, related_name='evaluations')
    event = models.ForeignKey('events.Event', on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations')
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_evaluations')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Evaluation for {self.volunteer} - Rating: {self.rating}/5"

class EventFeedback(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='feedback')
    volunteer = models.ForeignKey('volunteers.Volunteer', on_delete=models.CASCADE, related_name='event_feedback')
    feedback = models.TextField()
    suggestions = models.TextField(blank=True)
    would_participate_again = models.BooleanField(default=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'volunteer')
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Feedback for {self.event.title} by {self.volunteer}"
