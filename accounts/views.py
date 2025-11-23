from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from volunteers.models import Volunteer
from .forms import VolunteerSignupForm, UserManagementForm, UserEditForm
from .models import User


def volunteer_signup(request):
    if request.method == 'POST':
        form = VolunteerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.role = 'volunteer'
                    user.approval_status = 'pending'
                    user.is_active = False
                    user.save()
                    
                    Volunteer.objects.create(
                        user=user,
                        gender=form.cleaned_data['gender'],
                        age=form.cleaned_data['age'],
                        address=form.cleaned_data.get('address', ''),
                        interests=form.cleaned_data['interests'],
                        skills=form.cleaned_data['skills'],
                        availability=form.cleaned_data['availability'],
                        supporting_document=form.cleaned_data.get('supporting_document')
                    )
                    
                    messages.success(request, 'Your volunteer account has been created successfully! Please wait for admin approval before you can log in.')
                    return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VolunteerSignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.can_manage_all_users()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        role = self.request.GET.get('role')
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if role:
            queryset = queryset.filter(role=role)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from ministries.models import Ministry
        context['ministries'] = Ministry.objects.filter(is_active=True).order_by('name')
        return context


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserManagementForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def test_func(self):
        return self.request.user.can_manage_all_users()
    
    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.username} created successfully.')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def test_func(self):
        return self.request.user.can_manage_all_users()
    
    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.username} updated successfully.')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def test_func(self):
        user = self.get_object()
        return self.request.user.can_manage_all_users() and user.id != self.request.user.id
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'User deleted successfully.')
        return super().delete(request, *args, **kwargs)


class UserSuspendView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.can_manage_all_users()
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.id == request.user.id:
            messages.error(request, 'You cannot suspend yourself.')
            return redirect('accounts:user_list')
        
        user.is_suspended = not user.is_suspended
        user.save()
        
        status = 'suspended' if user.is_suspended else 'unsuspended'
        messages.success(request, f'{user.get_full_name()} has been {status}.')
        return redirect('accounts:user_list')


class AssignRoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.can_assign_roles()
    
    def post(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)
        new_role = request.POST.get('role')
        current_user = request.user
        
        if new_role not in dict(User.ROLE_CHOICES):
            messages.error(request, 'Invalid role selected.')
            return redirect('accounts:user_list')
        
        if current_user.is_administrator():
            target_user.role = new_role
            target_user.save()
            messages.success(request, f'{target_user.get_full_name()} role changed to {target_user.get_role_display()}.')
        
        elif current_user.is_priest():
            ministry = current_user.get_managed_ministry()
            if not ministry:
                messages.error(request, 'You must be assigned to a ministry to change roles.')
                return redirect('accounts:user_list')
            
            if target_user.role != 'volunteer':
                messages.error(request, 'Priests can only promote volunteers to coordinators.')
                return redirect('accounts:user_list')
            
            if new_role != 'coordinator':
                messages.error(request, 'Priests can only assign the coordinator role.')
                return redirect('accounts:user_list')
            
            if not hasattr(target_user, 'volunteer_profile'):
                messages.error(request, 'Target user must have a volunteer profile.')
                return redirect('accounts:user_list')
            
            if not target_user.volunteer_profile.ministries.filter(id=ministry.id).exists():
                messages.error(request, 'You can only promote volunteers within your ministry.')
                return redirect('accounts:user_list')
            
            target_user.role = new_role
            target_user.assigned_ministry = ministry
            target_user.save()
            messages.success(request, f'{target_user.get_full_name()} promoted to Coordinator of {ministry.name}.')
        else:
            messages.error(request, 'You do not have permission to assign roles.')
        
        return redirect('accounts:user_list')


class AssignMinistryView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_administrator()
    
    def post(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)
        ministry_id = request.POST.get('ministry')
        
        if ministry_id:
            from ministries.models import Ministry
            ministry = get_object_or_404(Ministry, pk=ministry_id)
            target_user.assigned_ministry = ministry
            target_user.save()
            messages.success(request, f'{target_user.get_full_name()} has been assigned to {ministry.name}.')
        else:
            target_user.assigned_ministry = None
            target_user.save()
            messages.success(request, f'{target_user.get_full_name()} has been removed from their ministry.')
        
        return redirect('accounts:user_list')
