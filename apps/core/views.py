# apps/core/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q

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
        'welcome_message': f'Willkommen zurück, {user.get_full_name() or user.username}!',
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

