# apps/opportunities/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Opportunity # OpportunityProduct wird meist über Opportunity angezeigt/bearbeitet
from .forms import OpportunityForm # Annahme: Form existiert
from django.contrib.auth import get_user_model

User = get_user_model()

class OpportunityListView(LoginRequiredMixin, ListView):
    model = Opportunity
    template_name = 'opportunities/opportunity_list.html'
    context_object_name = 'opportunities'
    paginate_by = 10

    def get_queryset(self):
        return Opportunity.objects.filter(owner=self.request.user)

class OpportunityDetailView(LoginRequiredMixin, DetailView):
    model = Opportunity
    template_name = 'opportunities/opportunity_detail.html'
    context_object_name = 'opportunity'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Opportunity not found or permission denied")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Zugehörige Aktivitäten
        context['activities'] = self.object.activities.filter(opportunity__owner=self.request.user)
        return context

class OpportunityCreateView(LoginRequiredMixin, CreateView):
    model = Opportunity
    form_class = OpportunityForm
    template_name = 'opportunities/opportunity_form.html'
    success_url = reverse_lazy('opportunities:opportunity_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OpportunityUpdateView(LoginRequiredMixin, UpdateView):
    model = Opportunity
    form_class = OpportunityForm
    template_name = 'opportunities/opportunity_form.html'
    success_url = reverse_lazy('opportunities:opportunity_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Opportunity not found or permission denied")
        return obj

class OpportunityDeleteView(LoginRequiredMixin, DeleteView):
    model = Opportunity
    template_name = 'opportunities/opportunity_confirm_delete.html'
    success_url = reverse_lazy('opportunities:opportunity_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Opportunity not found or permission denied")
        return obj