from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from .models import Attendance
from .forms import AttendanceForm, BulkAttendanceForm
from events.models import Event
from volunteers.models import Volunteer


class AttendanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Attendance
    template_name = 'attendance/list.html'
    context_object_name = 'attendance_records'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.can_track_attendance()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        event_id = self.request.GET.get('event')
        status = self.request.GET.get('status')
        
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        if status:
            queryset = queryset.filter(status=status)
        
        user = self.request.user
        if user.is_coordinator():
            ministry = user.get_managed_ministry()
            if ministry:
                queryset = queryset.filter(event__ministry=ministry)
        elif user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                queryset = queryset.filter(event__ministry=ministry)
        
        return queryset


class AttendanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/form.html'
    success_url = reverse_lazy('attendance:list')
    
    def test_func(self):
        return self.request.user.can_track_attendance()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                form.fields['event'].queryset = Event.objects.filter(ministry=ministry, is_active=True)
                form.fields['volunteer'].queryset = Volunteer.objects.filter(ministries=ministry, is_active=True)
            else:
                form.fields['event'].queryset = Event.objects.none()
                form.fields['volunteer'].queryset = Volunteer.objects.none()
        
        return form
    
    def form_valid(self, form):
        user = self.request.user
        event = form.cleaned_data['event']
        volunteer = form.cleaned_data['volunteer']
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if not ministry or event.ministry != ministry:
                messages.error(self.request, 'You can only mark attendance for events in your ministry.')
                return self.form_invalid(form)
            
            if not volunteer.ministries.filter(id=ministry.id).exists():
                messages.error(self.request, 'You can only mark attendance for volunteers in your ministry.')
                return self.form_invalid(form)
        
        if not event.assigned_volunteers.filter(id=volunteer.id).exists():
            messages.error(self.request, 'The volunteer must be assigned to this event.')
            return self.form_invalid(form)
        
        form.instance.marked_by = self.request.user
        messages.success(self.request, 'Attendance recorded successfully.')
        return super().form_valid(form)


class AttendanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/form.html'
    success_url = reverse_lazy('attendance:list')
    
    def test_func(self):
        user = self.request.user
        attendance = self.get_object()
        
        if not user.can_track_attendance():
            return False
        
        if user.is_administrator():
            return True
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry and attendance.event.ministry == ministry:
                return True
        
        return False
    
    def form_valid(self, form):
        messages.success(self.request, 'Attendance updated successfully.')
        return super().form_valid(form)


class AttendanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Attendance
    template_name = 'attendance/confirm_delete.html'
    success_url = reverse_lazy('attendance:list')
    
    def test_func(self):
        user = self.request.user
        attendance = self.get_object()
        
        if not user.can_track_attendance():
            return False
        
        if user.is_administrator():
            return True
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry and attendance.event.ministry == ministry:
                return True
        
        return False


class BulkAttendanceView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'attendance/bulk_mark.html'
    
    def test_func(self):
        return self.request.user.can_track_attendance()
    
    def _can_access_event(self, event):
        user = self.request.user
        if user.is_administrator():
            return True
        
        if user.is_priest() or user.is_coordinator():
            ministry = user.get_managed_ministry()
            if ministry and event.ministry == ministry:
                return True
        
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.request.GET.get('event')
        user = self.request.user
        
        if event_id:
            event = get_object_or_404(Event, id=event_id)
            
            if not self._can_access_event(event):
                messages.error(self.request, 'You do not have permission to mark attendance for this event.')
                context['events'] = self._get_allowed_events()
                return context
            
            context['event'] = event
            context['volunteers'] = event.assigned_volunteers.all()
            context['attendance_records'] = {
                record.volunteer_id: record 
                for record in Attendance.objects.filter(event=event)
            }
        
        context['events'] = self._get_allowed_events()
        return context
    
    def _get_allowed_events(self):
        user = self.request.user
        queryset = Event.objects.filter(is_active=True)
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                queryset = queryset.filter(ministry=ministry)
            else:
                queryset = queryset.none()
        
        return queryset.order_by('-start_datetime')[:20]
    
    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, id=event_id)
        
        if not self._can_access_event(event):
            messages.error(request, 'You do not have permission to mark attendance for this event.')
            return redirect('attendance:bulk_mark')
        
        updated_count = 0
        for volunteer in event.assigned_volunteers.all():
            status = request.POST.get(f'status_{volunteer.id}')
            notes = request.POST.get(f'notes_{volunteer.id}', '')
            
            if status:
                Attendance.objects.update_or_create(
                    event=event,
                    volunteer=volunteer,
                    defaults={
                        'status': status,
                        'notes': notes,
                        'marked_by': request.user
                    }
                )
                updated_count += 1
        
        messages.success(request, f'Attendance marked for {updated_count} volunteers.')
        return redirect('attendance:bulk_mark')
