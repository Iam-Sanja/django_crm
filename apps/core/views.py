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

# --- Dashboard View ---
@login_required
def dashboard(request):
    user = request.user
    today = timezone.now()
    
    # Leads für Kanban
    user_leads = Lead.objects.filter(owner=user).exclude(
        status__in=[Lead.LeadStatus.LOST, Lead.LeadStatus.UNQUALIFIED]
    )
    
    # Statistiken
    open_leads_count = user_leads.count()
    
    planned_activities_count = Activity.objects.filter(
        Q(assigned_to=user) | 
        Q(account__owner=user) | 
        Q(contact__owner=user) | 
        Q(opportunity__owner=user) | 
        Q(lead__owner=user),
        status='PLANNED',
        activity_date__gte=today
    ).count()
    
    open_opportunities_count = Opportunity.objects.filter(
        owner=user
    ).exclude(
        stage__in=['CLOSED_WON', 'CLOSED_LOST']
    ).count()
    
    accounts_count = Account.objects.filter(owner=user).count()
    
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
    
    # Kanban Board Daten
    leads_by_status = defaultdict(list)
    for lead in user_leads:
        leads_by_status[lead.status].append(lead)

    # Definiere die gewünschte Reihenfolge der Spalten im Kanban Board
    status_order = [
        Lead.LeadStatus.NEW,
        Lead.LeadStatus.CONTACTED,
        Lead.LeadStatus.QUALIFIED,
        Lead.LeadStatus.LOST,
        Lead.LeadStatus.UNQUALIFIED,
    ]

    # Erstelle eine geordnete Liste von Tupeln (status_display, leads_list, status_key) für das Template
    kanban_columns = []
    status_display_map = dict(Lead.LeadStatus.choices)

    for status_key in status_order:
        display_name = status_display_map.get(status_key, status_key)
        leads_in_status = leads_by_status[status_key]
        kanban_columns.append((display_name, leads_in_status, status_key))

    context = {
                'welcome_message': f'Willkommen zurück, {user.get_full_name() or user.username}!',
        'lead_kanban_columns': kanban_columns,
        'open_leads_count': open_leads_count,
        'planned_activities_count': planned_activities_count,
        'open_opportunities_count': open_opportunities_count,
        'accounts_count': accounts_count,
        'upcoming_activities': upcoming_activities,
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

