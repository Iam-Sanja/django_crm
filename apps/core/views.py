# apps/core/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from apps.leads.models import Lead
from collections import defaultdict
from django.utils.translation import gettext as _

from .models import Tag
from .forms import TagForm

# --- Dashboard View ---
@login_required
def dashboard(request):
    # Hole alle Leads, die dem aktuellen Benutzer gehören und 'offen' sind
    # (Schließe 'LOST' und 'UNQUALIFIED' aus - passe dies bei Bedarf an)
    user_leads = Lead.objects.filter(owner=request.user).exclude(
        status__in=[Lead.LeadStatus.LOST, Lead.LeadStatus.UNQUALIFIED]
    )

    # Gruppiere Leads nach Status
    leads_by_status = defaultdict(list)
    for lead in user_leads:
        leads_by_status[lead.status].append(lead)

    # Definiere die gewünschte Reihenfolge der Spalten im Kanban Board
    # Nutze die Keys aus LeadStatus
    status_order = [
        Lead.LeadStatus.NEW,
        Lead.LeadStatus.CONTACTED,
        Lead.LeadStatus.QUALIFIED,
        # Füge hier ggf. weitere 'offene' Status in gewünschter Reihenfolge hinzu
    ]

    # Erstelle eine geordnete Liste von Tupeln (status_display, leads_list, status_key) für das Template
    kanban_columns = []
    status_display_map = dict(Lead.LeadStatus.choices) # Mapping von Key zu Display-Name

    for status_key in status_order:
         display_name = status_display_map.get(status_key, status_key) # Hole Klarnamen
         leads_in_status = leads_by_status[status_key]
         # Füge nur Spalten hinzu, die in unserer gewünschten Reihenfolge sind
         kanban_columns.append((display_name, leads_in_status, status_key))

    # Optional: Füge noch Spalten für Status hinzu, die Leads haben, aber nicht in status_order sind (z.B. benutzerdefinierte)
    # Oder handle dies je nach Anforderung.

    # --- Optional: Gleiches für Opportunities ---
    # from apps.opportunities.models import Opportunity
    # user_opportunities = Opportunity.objects.filter(owner=request.user).exclude(
    #     stage__in=[Opportunity.OpportunityStage.CLOSED_WON, Opportunity.OpportunityStage.CLOSED_LOST]
    # )
    # opps_by_stage = defaultdict(list)
    # for opp in user_opportunities:
    #     opps_by_stage[opp.stage].append(opp)
    #
    # stage_order = [
    #     Opportunity.OpportunityStage.QUALIFICATION,
    #     Opportunity.OpportunityStage.NEEDS_ANALYSIS,
    #     Opportunity.OpportunityStage.PROPOSAL,
    #     Opportunity.OpportunityStage.NEGOTIATION,
    # ]
    # opp_kanban_columns = []
    # stage_display_map = dict(Opportunity.OpportunityStage.choices)
    # for stage_key in stage_order:
    #     display_name = stage_display_map.get(stage_key, stage_key)
    #     opps_in_stage = opps_by_stage[stage_key]
    #     opp_kanban_columns.append((display_name, opps_in_stage, stage_key))
    # -----------------------------------------

    context = {
        'welcome_message': f'Willkommen zurück, {request.user.username}!',
        'lead_kanban_columns': kanban_columns,
        # 'opportunity_kanban_columns': opp_kanban_columns, # Wenn Opportunities auch angezeigt werden sollen
        # Füge hier ggf. weitere Daten für andere Dashboard-Bereiche hinzu
    }
    return render(request, 'core/dashboard.html', context)

# --- Tag Views ---

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'core/tag_list.html' # Erwartetes Template
    context_object_name = 'tags'
    # Zeige alle Tags an, keine User-Filterung nötig (oder doch?)
    # queryset = Tag.objects.all() # Standardverhalten

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'core/tag_form.html' # Erwartetes Template
    success_url = reverse_lazy('core:tag_list') # Nach Erfolg zur Liste

    # Hier könntest du Berechtigungen prüfen, wer Tags erstellen darf
    # z.B. mit PermissionRequiredMixin

class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'core/tag_form.html' # Gleiches Template wie Create
    success_url = reverse_lazy('core:tag_list')

    # Hier könntest du Berechtigungen prüfen

class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'core/tag_confirm_delete.html' # Bestätigungs-Template
    success_url = reverse_lazy('core:tag_list')

    # Hier könntest du Berechtigungen prüfen