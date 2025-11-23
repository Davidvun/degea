from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from .models import Volunteer
from .forms import VolunteerForm

class VolunteerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Volunteer
    template_name = 'volunteers/list.html'
    context_object_name = 'volunteers'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.can_manage_volunteers() or self.request.user.can_view_reports()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                queryset = queryset.filter(ministries=ministry)
            else:
                queryset = queryset.none()
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(skills__icontains=search)
            )
        return queryset

class VolunteerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Volunteer
    template_name = 'volunteers/detail.html'
    context_object_name = 'volunteer'
    
    def test_func(self):
        user = self.request.user
        volunteer = self.get_object()
        
        if user.is_administrator():
            return True
        
        if user.is_volunteer_user():
            return volunteer.user == user
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                return volunteer.ministries.filter(id=ministry.id).exists()
        
        return False

class VolunteerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Volunteer
    form_class = VolunteerForm
    template_name = 'volunteers/form.html'
    success_url = reverse_lazy('volunteers:list')
    
    def test_func(self):
        return self.request.user.can_manage_volunteers()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                from ministries.models import Ministry
                form.fields['ministries'].queryset = Ministry.objects.filter(id=ministry.id)
            else:
                from ministries.models import Ministry
                form.fields['ministries'].queryset = Ministry.objects.none()
        
        return form
    
    def form_valid(self, form):
        user = self.request.user
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if not ministry:
                messages.error(self.request, 'You must be assigned to a ministry to create volunteers.')
                return self.form_invalid(form)
            
            selected_ministries = form.cleaned_data.get('ministries', [])
            for selected_ministry in selected_ministries:
                if selected_ministry.id != ministry.id:
                    messages.error(self.request, 'You can only assign volunteers to your own ministry.')
                    return self.form_invalid(form)
        
        return super().form_valid(form)

class VolunteerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Volunteer
    form_class = VolunteerForm
    template_name = 'volunteers/form.html'
    success_url = reverse_lazy('volunteers:list')
    
    def test_func(self):
        user = self.request.user
        volunteer = self.get_object()
        
        if user.is_administrator():
            return True
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                return volunteer.ministries.filter(id=ministry.id).exists()
        
        return False
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                from ministries.models import Ministry
                form.fields['ministries'].queryset = Ministry.objects.filter(id=ministry.id)
            else:
                from ministries.models import Ministry
                form.fields['ministries'].queryset = Ministry.objects.none()
        
        return form
    
    def form_valid(self, form):
        user = self.request.user
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if not ministry:
                messages.error(self.request, 'You must be assigned to a ministry.')
                return self.form_invalid(form)
            
            selected_ministries = form.cleaned_data.get('ministries', [])
            for selected_ministry in selected_ministries:
                if selected_ministry.id != ministry.id:
                    messages.error(self.request, 'You can only assign volunteers to your own ministry.')
                    return self.form_invalid(form)
        
        return super().form_valid(form)

class VolunteerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Volunteer
    template_name = 'volunteers/confirm_delete.html'
    success_url = reverse_lazy('volunteers:list')
    
    def test_func(self):
        user = self.request.user
        volunteer = self.get_object()
        
        if user.is_administrator():
            return True
        
        if user.is_coordinator() or user.is_priest():
            ministry = user.get_managed_ministry()
            if ministry:
                return volunteer.ministries.filter(id=ministry.id).exists()
        
        return False

class VolunteerApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.can_approve_volunteers()
    
    def post(self, request, pk):
        volunteer = get_object_or_404(Volunteer, pk=pk)
        user = request.user
        
        if user.is_priest():
            ministry = user.get_managed_ministry()
            if not ministry or not volunteer.ministries.filter(id=ministry.id).exists():
                messages.error(request, 'You can only approve volunteers within your ministry.')
                return redirect('volunteers:list')
        
        volunteer.user.approval_status = 'approved'
        volunteer.user.is_active = True
        volunteer.user.save()
        messages.success(request, f'{volunteer.user.get_full_name()} has been approved and can now log in.')
        return redirect('volunteers:list')

class VolunteerRejectView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.can_approve_volunteers()
    
    def post(self, request, pk):
        volunteer = get_object_or_404(Volunteer, pk=pk)
        user = request.user
        
        if user.is_priest():
            ministry = user.get_managed_ministry()
            if not ministry or not volunteer.ministries.filter(id=ministry.id).exists():
                messages.error(request, 'You can only reject volunteers within your ministry.')
                return redirect('volunteers:list')
        
        volunteer.user.approval_status = 'rejected'
        volunteer.user.is_active = False
        volunteer.user.save()
        messages.warning(request, f'{volunteer.user.get_full_name()} has been rejected.')
        return redirect('volunteers:list')
