from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Ministry, Program
from .forms import MinistryForm, ProgramForm

class MinistryListView(LoginRequiredMixin, ListView):
    model = Ministry
    template_name = 'ministries/list.html'
    context_object_name = 'ministries'
    paginate_by = 20

class MinistryDetailView(LoginRequiredMixin, DetailView):
    model = Ministry
    template_name = 'ministries/detail.html'
    context_object_name = 'ministry'

class MinistryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/form.html'
    success_url = reverse_lazy('ministries:list')
    
    def test_func(self):
        return self.request.user.can_manage_volunteers()

class MinistryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/form.html'
    success_url = reverse_lazy('ministries:list')
    
    def test_func(self):
        return self.request.user.can_manage_volunteers()

class MinistryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ministry
    template_name = 'ministries/confirm_delete.html'
    success_url = reverse_lazy('ministries:list')
    
    def test_func(self):
        return self.request.user.is_administrator()
