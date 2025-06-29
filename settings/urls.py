from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views as core_views  # Dashboard-View importieren

urlpatterns = [
    path('', core_views.dashboard, name='home'),  # Startseite zeigt auf Dashboard
    path('admin/', admin.site.urls),
    path('core/', include('apps.core.urls', namespace='core')),
    path('accounts/', include('apps.accounts.urls')),
    path('customers/', include('apps.customers.urls')),
    path('leads/', include('apps.leads.urls')),
    path('opportunities/', include('apps.opportunities.urls')),
    path('activities/', include('apps.activities.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
