from django.urls import path
from . import views

app_name = 'ministries'

urlpatterns = [
    path('', views.MinistryListView.as_view(), name='list'),
    path('create/', views.MinistryCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MinistryDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.MinistryUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.MinistryDeleteView.as_view(), name='delete'),
]
