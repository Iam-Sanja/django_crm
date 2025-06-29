# apps/core/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from apps.leads.models import Lead
from apps.activities.models import Activity
from apps.opportunities.models import Opportunity
from apps.customers.models import Account, Contact
from collections import defaultdict
from django.utils.translation import gettext as _

from .models import Tag
from .forms import TagForm

from django.contrib.auth import get_user_model
User = get_user_model()

# --- Dashboard View ---
@login_required
def dashboard(request):
    user = request.user
    today = timezone.now()
    
    # Leads für Statistiken
    user_leads = Lead.objects.filter(owner=user)
    
    # Offene Leads (ohne LOST und UNQUALIFIED)
    open_leads = user_leads.exclude(
        status__in=[Lead.LeadStatus.LOST, Lead.LeadStatus.UNQUALIFIED]
    )
    open_leads_count = open_leads.count()
    
    # Leads nach Status für die Zusammenfassung
    new_leads_count = user_leads.filter(status=Lead.LeadStatus.NEW).count()
    contacted_leads_count = user_leads.filter(status=Lead.LeadStatus.CONTACTED).count()
    qualified_leads_count = user_leads.filter(status=Lead.LeadStatus.QUALIFIED).count()
    unqualified_leads_count = user_leads.filter(status=Lead.LeadStatus.UNQUALIFIED).count()
    lost_leads_count = user_leads.filter(status=Lead.LeadStatus.LOST).count()
    
    # Neueste Leads (für die Liste)
    latest_leads = user_leads.order_by('-created_at')[:5]
    
    # Aktivitäten
    planned_activities_count = Activity.objects.filter(
        Q(assigned_to=user) | 
        Q(account__owner=user) | 
        Q(contact__owner=user) | 
        Q(opportunity__owner=user) | 
        Q(lead__owner=user),
        status='PLANNED',
        activity_date__gte=today
    ).count()
    
    # Anstehende Aktivitäten (für die nächsten 7 Tage)
    upcoming_activities = Activity.objects.filter(
        Q(assigned_to=user) | 
        Q(account__owner=user) | 
        Q(contact__owner=user) | 
        Q(opportunity__owner=user) | 
        Q(lead__owner=user),
        status='PLANNED',
        activity_date__gte=today,
        activity_date__lte=today + timedelta(days=7)
    ).order_by('activity_date')[:5]  # Nur die nächsten 5 anzeigen
    
    # Opportunities
    open_opportunities_count = Opportunity.objects.filter(
        owner=user
    ).exclude(
        stage__in=['CLOSED_WON', 'CLOSED_LOST']
    ).count()
    
    # Accounts
    accounts_count = Account.objects.filter(owner=user).count()
    
    context = {
        'welcome_message': f'Willkommen zurück, {user.get_full_name() or user.email}!',
        'open_leads_count': open_leads_count,
        'new_leads_count': new_leads_count,
        'contacted_leads_count': contacted_leads_count,
        'qualified_leads_count': qualified_leads_count,
        'unqualified_leads_count': unqualified_leads_count,
        'lost_leads_count': lost_leads_count,
        'latest_leads': latest_leads,
        'planned_activities_count': planned_activities_count,
        'upcoming_activities': upcoming_activities,
        'open_opportunities_count': open_opportunities_count,
        'accounts_count': accounts_count,
    }
    return render(request, 'core/dashboard.html', context)

# --- Tag Views ---

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'core/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 10  # Paginierung hinzugefügt

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'core/tag_form.html'
    success_url = reverse_lazy('core:tag_list')

class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'core/tag_form.html'
    success_url = reverse_lazy('core:tag_list')

class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'core/tag_confirm_delete.html'
    success_url = reverse_lazy('core:tag_list')

@require_http_methods(["GET"])
def industry_autocomplete(request):
    q = request.GET.get('q', '')
    tags = Tag.objects.filter(type='industry')
    if q:
        tags = tags.filter(name__icontains=q)
    tags = tags[:10]
    return JsonResponse({
        'results': [
            {'id': str(tag.id), 'text': tag.name, 'color': tag.color or '#3b82f6'}
            for tag in tags
        ]
    })

@require_http_methods(["GET"])
def tag_autocomplete(request):
    q = request.GET.get('q', '')
    tags = Tag.objects.filter(type='general')
    if q:
        tags = tags.filter(name__icontains=q)
    tags = tags[:10]
    return JsonResponse({
        'results': [
            {'id': str(tag.id), 'text': tag.name, 'color': tag.color or '#10b981'}
            for tag in tags
        ]
    })

@csrf_exempt
@require_http_methods(["POST"])
def create_tag(request):
    try:
        data = json.loads(request.body)
        tag_name = data.get('name', '').strip()
        tag_type = data.get('type', 'general')
        
        if not tag_name:
            return JsonResponse({'error': 'Tag-Name ist erforderlich'}, status=400)
        
        # Prüfe ob Tag bereits existiert
        existing_tag = Tag.objects.filter(name=tag_name, type=tag_type).first()
        if existing_tag:
            return JsonResponse({
                'id': str(existing_tag.id),
                'name': existing_tag.name,
                'type': existing_tag.type
            })
        
        # Erstelle neuen Tag
        new_tag = Tag.objects.create(
            name=tag_name,
            type=tag_type,
            color=data.get('color', '#3b82f6')  # Default blau
        )
        
        return JsonResponse({
            'id': str(new_tag.id),
            'name': new_tag.name,
            'type': new_tag.type,
            'color': new_tag.color
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Ungültiges JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

