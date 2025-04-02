# apps/activities/urls.py
from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='activity_list'),
    path('add/', views.ActivityCreateView.as_view(), name='activity_add'),
    path('<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='activity_edit'),
    path('<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='activity_delete'),
]