from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackListView.as_view(), name='list'),
    path('evaluation/create/', views.EvaluationCreateView.as_view(), name='evaluation_create'),
    path('evaluation/<int:pk>/edit/', views.EvaluationUpdateView.as_view(), name='evaluation_edit'),
    path('evaluation/<int:pk>/delete/', views.EvaluationDeleteView.as_view(), name='evaluation_delete'),
    path('event-feedback/', views.EventFeedbackListView.as_view(), name='event_feedback_list'),
    path('event-feedback/create/', views.EventFeedbackCreateView.as_view(), name='event_feedback_create'),
]
