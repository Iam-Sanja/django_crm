# apps/customers/urls.py
from django.urls import path
from . import views, api_views

app_name = 'customers'

urlpatterns = [
    # Account URLs
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    path('accounts/<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('accounts/<int:pk>/delete/', views.AccountDeleteView.as_view(), name='account_delete'),
    
    # Account API URLs
    path('api/accounts/create/', api_views.create_account, name='api_account_create'),
    path('api/accounts/<int:pk>/update/', api_views.update_account, name='api_account_update'),

    # Contact URLs
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('contacts/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    
    # Contact API URLs
    path('api/contacts/create/', api_views.create_contact, name='api_contact_create'),
    path('api/contacts/<int:pk>/update/', api_views.update_contact, name='api_contact_update'),

    # Default für /customers/ könnte die Account-Liste sein
    path('', views.AccountListView.as_view(), name='index'),
]