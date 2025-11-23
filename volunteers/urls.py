from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('', views.VolunteerListView.as_view(), name='list'),
    path('create/', views.VolunteerCreateView.as_view(), name='create'),
    path('<int:pk>/', views.VolunteerDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.VolunteerUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.VolunteerDeleteView.as_view(), name='delete'),
    path('<int:pk>/approve/', views.VolunteerApproveView.as_view(), name='approve'),
    path('<int:pk>/reject/', views.VolunteerRejectView.as_view(), name='reject'),
]
