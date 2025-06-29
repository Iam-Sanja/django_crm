# apps/customers/urls.py
from django.urls import path
from . import views, api_views

app_name = 'customers'

urlpatterns = [    # Account URLs
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    path('accounts/create/', views.AccountCreateView.as_view(), name='account_create'),
    path('accounts/<uuid:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('accounts/<uuid:pk>/update/', views.AccountUpdateView.as_view(), name='account_update'),
    path('accounts/<uuid:pk>/delete/', views.AccountDeleteView.as_view(), name='account_delete'),
    
    # Account API URLs
    path('api/accounts/create/', api_views.create_account, name='api_account_create'),
    path('api/accounts/<uuid:pk>/update/', api_views.update_account, name='api_account_update'),
    path('api/accounts/<uuid:pk>/data/', api_views.get_account_data, name='api_account_data'),
    path('api/accounts/<uuid:pk>/delete/', api_views.delete_account, name='api_account_delete'),

    # Contact URLs
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),
    path('contacts/create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('contacts/<uuid:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('contacts/<uuid:pk>/update/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/<uuid:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    
    # Contact API URLs
    path('api/contacts/create/', api_views.create_contact, name='api_contact_create'),
    path('api/contacts/<uuid:pk>/update/', api_views.update_contact, name='api_contact_update'),
    path('api/contacts/<uuid:pk>/data/', api_views.get_contact_data, name='api_contact_data'),

    # Default für /customers/ könnte die Account-Liste sein
    path('', views.AccountListView.as_view(), name='index'),
]