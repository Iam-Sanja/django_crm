# apps/leads/views.py
from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Lead
from .forms import LeadForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 10

    def get_queryset(self):
        return Lead.objects.filter(owner=self.request.user)

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Lead not found or permission denied")
        return obj

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         # Zugehörige Aktivitäten hinzufügen
         context['activities'] = self.object.activities.filter(lead__owner=self.request.user) # Aktivitäten des Leads anzeigen
         return context

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead_form.html'
    success_url = reverse_lazy('leads:lead_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/lead_form.html'
    success_url = reverse_lazy('leads:lead_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Lead not found or permission denied")
        return obj

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    template_name = 'leads/lead_confirm_delete.html'
    success_url = reverse_lazy('leads:lead_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Lead not found or permission denied")
        return obj
    

@login_required
def lead_pipeline_view(request):
    user = request.user
    
    # Alle Leads des Benutzers holen (auch LOST und UNQUALIFIED für die vollständige Pipeline)
    user_leads = Lead.objects.filter(owner=request.user)
    
    # Gruppiere Leads nach Status
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
        'lead_kanban_columns': kanban_columns,
        'page_title': 'Lead-Pipeline'
    }
    
    return render(request, 'leads/lead_pipeline.html', context)
    

@require_POST # Nur POST-Requests erlauben
@login_required # Sicherstellen, dass der User angemeldet ist
def update_lead_status_api(request, pk):
    try:
        # Stelle sicher, dass der Lead existiert und dem User gehört (Sicherheitsaspekt!)
        lead = get_object_or_404(Lead, pk=pk, owner=request.user)

        data = json.loads(request.body)
        new_status = data.get('status')

        # Validierung: Ist der neue Status gültig?
        valid_statuses = [choice[0] for choice in Lead.LeadStatus.choices]
        if new_status not in valid_statuses:
            return JsonResponse({'success': False, 'error': 'Ungültiger Status'}, status=400)

        # Status aktualisieren und speichern
        lead.status = new_status
        lead.save()

        return JsonResponse({
            'success': True,
            'message': 'Lead-Status aktualisiert.',
            'new_status': lead.get_status_display(), # Optional: neuen Display-Namen zurückgeben
            'updated_at': lead.updated_at.strftime('%d.%m.%Y %H:%M') # Optional
         })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Ungültige JSON-Daten'}, status=400)
    except Lead.DoesNotExist:
         return JsonResponse({'success': False, 'error': 'Lead nicht gefunden oder keine Berechtigung'}, status=404)
    except Exception as e:
        # Logging des Fehlers wäre hier gut
        print(f"Error updating lead status: {e}")
        return JsonResponse({'success': False, 'error': 'Ein interner Fehler ist aufgetreten.'}, status=500)