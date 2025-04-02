from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('customers/', include('apps.customers.urls')),
    path('leads/', include('apps.leads.urls')),
    path('activities/', include('apps.activities.urls')),
    path('opportunities/', include('apps.opportunities.urls')),
]
