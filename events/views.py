from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from .models import Event, Task, EventReport
from .forms import EventForm, TaskForm, EventReportForm, AddVolunteerToEventForm

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 20

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    success_url = reverse_lazy('events:list')
    
    def test_func(self):
        user = self.request.user
        if not user.is_priest():
            return False
        if not user.assigned_ministry:
            return False
        return True
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_priest() and not self.request.user.assigned_ministry:
            messages.error(self.request, 'You must be assigned to a ministry to create events.')
        return super().handle_no_permission()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.ministry = self.request.user.assigned_ministry
        messages.success(self.request, 'Event created successfully.')
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    success_url = reverse_lazy('events:list')
    
    def test_func(self):
        user = self.request.user
        event = self.get_object()
        
        if not user.is_priest():
            return False
        
        if not user.assigned_ministry:
            return False
        
        return event.ministry == user.assigned_ministry
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully.')
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events:list')
    
    def test_func(self):
        user = self.request.user
        event = self.get_object()
        
        if not user.is_priest():
            return False
        
        if not user.assigned_ministry:
            return False
        
        return event.ministry == user.assigned_ministry


class CoordinatorEventDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Event
    template_name = 'events/coordinator_detail.html'
    context_object_name = 'event'
    
    def test_func(self):
        user = self.request.user
        event = self.get_object()
        return user.is_coordinator() and event.coordinator == user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['tasks'] = event.tasks.all()
        context['reports'] = event.reports.filter(submitted_by=self.request.user)
        context['add_volunteer_form'] = AddVolunteerToEventForm(event=event, user=self.request.user)
        return context


class AddVolunteerToEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        user = self.request.user
        return user.is_coordinator() and event.coordinator == user
    
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = AddVolunteerToEventForm(request.POST, event=event, user=request.user)
        
        if form.is_valid():
            volunteers = form.cleaned_data['volunteers']
            for volunteer in volunteers:
                event.assigned_volunteers.add(volunteer)
            messages.success(request, f'{volunteers.count()} volunteer(s) added to event.')
        else:
            messages.error(request, 'Error adding volunteers to event.')
        
        return redirect('events:coordinator_detail', pk=pk)


class RemoveVolunteerFromEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        user = self.request.user
        return user.is_coordinator() and event.coordinator == user
    
    def post(self, request, event_pk, volunteer_pk):
        event = get_object_or_404(Event, pk=event_pk)
        volunteer = get_object_or_404(event.assigned_volunteers, pk=volunteer_pk)
        event.assigned_volunteers.remove(volunteer)
        messages.success(request, f'{volunteer.user.get_full_name()} removed from event.')
        return redirect('events:coordinator_detail', pk=event_pk)


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'events/task_form.html'
    
    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        user = self.request.user
        return user.is_coordinator() and event.coordinator == user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        kwargs['event'] = event
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        form.instance.event = event
        form.instance.assigned_by = self.request.user
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('events:coordinator_detail', kwargs={'pk': self.kwargs['event_pk']})


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'events/task_form.html'
    
    def test_func(self):
        task = self.get_object()
        user = self.request.user
        return user.is_coordinator() and task.event.coordinator == user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task = self.get_object()
        kwargs['event'] = task.event
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('events:coordinator_detail', kwargs={'pk': self.object.event.pk})


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'events/task_confirm_delete.html'
    
    def test_func(self):
        task = self.get_object()
        user = self.request.user
        return user.is_coordinator() and task.event.coordinator == user
    
    def get_success_url(self):
        return reverse_lazy('events:coordinator_detail', kwargs={'pk': self.object.event.pk})


class EventReportCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EventReport
    form_class = EventReportForm
    template_name = 'events/report_form.html'
    
    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        user = self.request.user
        return user.is_coordinator() and event.coordinator == user
    
    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        form.instance.event = event
        form.instance.submitted_by = self.request.user
        
        if form.instance.status not in ['draft', 'submitted']:
            form.instance.status = 'draft'
        
        if form.instance.status == 'submitted' and not form.instance.submitted_at:
            form.instance.submitted_at = timezone.now()
        
        messages.success(self.request, 'Event report saved successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('events:coordinator_detail', kwargs={'pk': self.kwargs['event_pk']})


class EventReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EventReport
    form_class = EventReportForm
    template_name = 'events/report_form.html'
    
    def test_func(self):
        report = self.get_object()
        user = self.request.user
        return user.is_coordinator() and report.submitted_by == user and report.status != 'reviewed'
    
    def form_valid(self, form):
        if form.instance.status not in ['draft', 'submitted']:
            form.instance.status = 'draft'
        
        if form.instance.status == 'submitted' and not form.instance.submitted_at:
            form.instance.submitted_at = timezone.now()
        
        messages.success(self.request, 'Event report updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('events:coordinator_detail', kwargs={'pk': self.object.event.pk})


class EventReportDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = EventReport
    template_name = 'events/report_detail.html'
    context_object_name = 'report'
    
    def test_func(self):
        report = self.get_object()
        user = self.request.user
        return (user.is_coordinator() and report.submitted_by == user) or \
               (user.is_priest() and report.event.ministry == user.assigned_ministry) or \
               user.is_administrator()
