from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import VolunteerEvaluation, EventFeedback
from .forms import VolunteerEvaluationForm, EventFeedbackForm


class FeedbackListView(LoginRequiredMixin, ListView):
    model = VolunteerEvaluation
    template_name = 'feedback/list.html'
    context_object_name = 'evaluations'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_volunteer_user():
            queryset = queryset.filter(volunteer__user=user)
        elif user.is_coordinator():
            ministry = user.get_managed_ministry()
            if ministry:
                queryset = queryset.filter(volunteer__ministries=ministry)
        elif user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                queryset = queryset.filter(volunteer__ministries=ministry)
        
        return queryset


class EvaluationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VolunteerEvaluation
    form_class = VolunteerEvaluationForm
    template_name = 'feedback/evaluation_form.html'
    success_url = reverse_lazy('feedback:list')
    
    def test_func(self):
        return self.request.user.can_provide_feedback()
    
    def form_valid(self, form):
        form.instance.evaluated_by = self.request.user
        messages.success(self.request, 'Volunteer evaluation submitted successfully.')
        return super().form_valid(form)


class EvaluationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VolunteerEvaluation
    form_class = VolunteerEvaluationForm
    template_name = 'feedback/evaluation_form.html'
    success_url = reverse_lazy('feedback:list')
    
    def test_func(self):
        evaluation = self.get_object()
        return self.request.user.can_provide_feedback() and evaluation.evaluated_by == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Evaluation updated successfully.')
        return super().form_valid(form)


class EvaluationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VolunteerEvaluation
    template_name = 'feedback/evaluation_confirm_delete.html'
    success_url = reverse_lazy('feedback:list')
    
    def test_func(self):
        evaluation = self.get_object()
        return self.request.user.can_provide_feedback() and evaluation.evaluated_by == self.request.user


class EventFeedbackListView(LoginRequiredMixin, ListView):
    model = EventFeedback
    template_name = 'feedback/event_feedback_list.html'
    context_object_name = 'feedback_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_volunteer_user():
            queryset = queryset.filter(volunteer__user=user)
        
        return queryset


class EventFeedbackCreateView(LoginRequiredMixin, CreateView):
    model = EventFeedback
    form_class = EventFeedbackForm
    template_name = 'feedback/event_feedback_form.html'
    success_url = reverse_lazy('feedback:event_feedback_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Event feedback submitted successfully.')
        return super().form_valid(form)
