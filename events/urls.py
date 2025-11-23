from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),
    
    path('<int:pk>/coordinator/', views.CoordinatorEventDetailView.as_view(), name='coordinator_detail'),
    path('<int:pk>/add-volunteers/', views.AddVolunteerToEventView.as_view(), name='add_volunteers'),
    path('<int:event_pk>/remove-volunteer/<int:volunteer_pk>/', views.RemoveVolunteerFromEventView.as_view(), name='remove_volunteer'),
    
    path('<int:event_pk>/tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    path('<int:event_pk>/reports/create/', views.EventReportCreateView.as_view(), name='report_create'),
    path('reports/<int:pk>/edit/', views.EventReportUpdateView.as_view(), name='report_edit'),
    path('reports/<int:pk>/', views.EventReportDetailView.as_view(), name='report_detail'),
]
