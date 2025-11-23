from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Announcement, EmailLog
from .forms import AnnouncementForm

class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'communications/list.html'
    context_object_name = 'announcements'
    paginate_by = 20

class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'communications/detail.html'
    context_object_name = 'announcement'

class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'communications/form.html'
    success_url = reverse_lazy('communications:list')
    
    def test_func(self):
        return self.request.user.can_manage_volunteers()
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'communications/form.html'
    success_url = reverse_lazy('communications:list')
    
    def test_func(self):
        return self.request.user.can_manage_volunteers()

class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = 'communications/confirm_delete.html'
    success_url = reverse_lazy('communications:list')
    
    def test_func(self):
        return self.request.user.can_manage_volunteers()
