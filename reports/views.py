from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from volunteers.models import Volunteer
from ministries.models import Ministry
from events.models import Event
from attendance.models import Attendance

class ReportsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'reports/dashboard.html'
    
    def test_func(self):
        return self.request.user.can_view_reports()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_volunteers'] = Volunteer.objects.filter(is_active=True).count()
        context['total_ministries'] = Ministry.objects.filter(is_active=True).count()
        context['total_events'] = Event.objects.filter(is_active=True).count()
        context['total_attendance'] = Attendance.objects.count()
        
        context['active_volunteers'] = Volunteer.objects.filter(is_active=True).count()
        context['inactive_volunteers'] = Volunteer.objects.filter(is_active=False).count()
        
        context['gender_stats'] = Volunteer.objects.values('gender').annotate(count=Count('id'))
        
        context['recent_events'] = Event.objects.filter(is_active=True).order_by('-start_datetime')[:5]
        
        return context
