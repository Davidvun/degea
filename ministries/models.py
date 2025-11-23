from django.db import models
from django.conf import settings

class Ministry(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_ministries')
    volunteers = models.ManyToManyField('volunteers.Volunteer', related_name='ministries', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Ministries'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def volunteer_count(self):
        return self.volunteers.count()

class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='programs')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    coordinator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='coordinated_programs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} - {self.ministry.name}"
