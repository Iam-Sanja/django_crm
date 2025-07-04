# apps/opportunities/urls.py
from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.OpportunityListView.as_view(), name='opportunity_list'),
    path('add/', views.OpportunityCreateView.as_view(), name='opportunity_add'),
    path('<uuid:pk>/', views.OpportunityDetailView.as_view(), name='opportunity_detail'),
    path('<uuid:pk>/edit/', views.OpportunityUpdateView.as_view(), name='opportunity_edit'),
    path('<uuid:pk>/delete/', views.OpportunityDeleteView.as_view(), name='opportunity_delete'),
]