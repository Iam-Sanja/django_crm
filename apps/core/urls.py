# apps/core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Tag URLs
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/add/', views.TagCreateView.as_view(), name='tag_add'),
    path('tags/<uuid:pk>/edit/', views.TagUpdateView.as_view(), name='tag_edit'),
    path('tags/<uuid:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    # Autocomplete für Industry-Tags
    path('industry-autocomplete/', views.industry_autocomplete, name='industry_autocomplete'),
    # Autocomplete für allgemeine Tags
    path('tag-autocomplete/', views.tag_autocomplete, name='tag_autocomplete'),
    # Tag erstellen API
    path('create-tag/', views.create_tag, name='create_tag'),
]
