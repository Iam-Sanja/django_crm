# apps/activities/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import Activity
from .forms import ActivityForm # Annahme: Form existiert
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 10

    def get_queryset(self):
        # Zeige Aktivitäten, die dem User zugewiesen sind ODER
        # die zu einem Objekt gehören, dessen Owner der User ist.
        user = self.request.user
        return Activity.objects.filter(
            Q(assigned_to=user) |
            Q(account__owner=user) |
            Q(contact__owner=user) |
            Q(opportunity__owner=user) |
            Q(lead__owner=user) #|
            # Q(case__owner=user) # Wenn Case-App existiert
        ).distinct().order_by('-activity_date') # distinct, falls mehrfach matcht

class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'
    context_object_name = 'activity'

    def get_object(self, queryset=None):
        # Hole Objekt zuerst, prüfe Rechte danach
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        can_view = False
        if obj.assigned_to == user:
            can_view = True
        elif obj.account and obj.account.owner == user:
            can_view = True
        elif obj.contact and obj.contact.owner == user:
             can_view = True
        elif obj.opportunity and obj.opportunity.owner == user:
             can_view = True
        elif obj.lead and obj.lead.owner == user:
             can_view = True
        # elif obj.case and obj.case.owner == user: # Wenn Case-App existiert
        #     can_view = True

        if not can_view:
            # Hier 403 statt 404, da das Objekt existiert, aber der Zugriff verweigert wird
            raise PermissionDenied("You do not have permission to view this activity.")
        return obj

class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:activity_list')

    def form_valid(self, form):
        # Zuweisung standardmäßig zum Ersteller? Oder aus Formular?
        if not form.instance.assigned_to:
             form.instance.assigned_to = self.request.user
        # Hier müsste Logik rein, um sicherzustellen, dass nur *ein* Bezug gesetzt wird
        # und der Benutzer Zugriff auf diesen Bezug hat. Das Formular sollte das steuern.
        return super().form_valid(form)

    # TODO: Initialwerte für Bezugsobjekt setzen, wenn von Detailseite aufgerufen

class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activities:activity_list')

    def get_object(self, queryset=None):
        # Nutzt die gleiche Logik wie DetailView zur Rechteprüfung
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        can_edit = False # Strengere Prüfung für Bearbeitung? Evtl. nur assigned_to? Oder Owner des Objekts?
        if obj.assigned_to == user:
            can_edit = True
        elif obj.account and obj.account.owner == user: # Owner des Bezugsobjekts darf evtl. auch bearbeiten?
            can_edit = True
        # ... ähnliche Checks für andere Bezüge ...

        if not can_edit:
             raise PermissionDenied("You do not have permission to edit this activity.")
        return obj


class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'activities/activity_confirm_delete.html'
    success_url = reverse_lazy('activities:activity_list')

    def get_object(self, queryset=None):
         # Nutzt die gleiche Logik wie DetailView/UpdateView zur Rechteprüfung
        obj = super().get_object(queryset=queryset)
        user = self.request.user
        can_delete = False # Wer darf löschen? Nur assigned_to? Nur Owner des Bezugs?
        if obj.assigned_to == user:
            can_delete = True
        elif obj.account and obj.account.owner == user:
             can_delete = True
        # ... ähnliche Checks für andere Bezüge ...

        if not can_delete:
            raise PermissionDenied("You do not have permission to delete this activity.")
        return obj