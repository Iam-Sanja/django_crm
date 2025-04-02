# apps/leads/urls.py
from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead_list'),
    path('add/', views.LeadCreateView.as_view(), name='lead_add'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='lead_edit'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead_delete'),
    path('pipeline/', views.lead_pipeline_view, name='lead_pipeline'),

    path('api/leads/<int:pk>/update_status/', views.update_lead_status_api, name='api_lead_update_status'),
]