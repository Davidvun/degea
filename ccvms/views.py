from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from volunteers.models import Volunteer
from ministries.models import Ministry
from events.models import Event, EventReport
from attendance.models import Attendance
from communications.models import Announcement
from feedback.models import VolunteerEvaluation


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        user = self.request.user
        if user.is_administrator():
            return ['dashboards/admin_dashboard.html']
        elif user.is_priest():
            return ['dashboards/priest_dashboard.html']
        elif user.is_coordinator():
            return ['dashboards/coordinator_dashboard.html']
        elif user.is_volunteer_user():
            return ['dashboards/volunteer_dashboard.html']
        return ['dashboard.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['total_volunteers'] = Volunteer.objects.filter(is_active=True).count()
        context['total_ministries'] = Ministry.objects.filter(is_active=True).count()
        context['total_events'] = Event.objects.filter(is_active=True).count()
        context['total_attendance'] = Attendance.objects.count()
        
        if user.is_coordinator():
            context['coordinated_events'] = Event.objects.filter(
                coordinator=user,
                is_active=True,
                start_datetime__gte=timezone.now()
            ).order_by('start_datetime')[:10]
            context['my_reports'] = EventReport.objects.filter(submitted_by=user).order_by('-created_at')[:5]
        
        if user.is_volunteer_user() and hasattr(user, 'volunteer_profile'):
            volunteer = user.volunteer_profile
            context['my_events'] = Event.objects.filter(
                assigned_volunteers=volunteer, 
                is_active=True,
                start_datetime__gte=timezone.now()
            ).order_by('start_datetime')[:5]
            context['my_attendance'] = Attendance.objects.filter(volunteer=volunteer).count()
            context['my_ministries'] = volunteer.ministries.filter(is_active=True)
        
        context['recent_communications'] = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
        context['upcoming_events'] = Event.objects.filter(
            is_active=True, 
            start_datetime__gte=timezone.now()
        ).order_by('start_datetime')[:5]
        context['recent_feedback'] = VolunteerEvaluation.objects.order_by('-created_at')[:5]
        
        return context
