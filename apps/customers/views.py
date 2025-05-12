# apps/customers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Account, Contact
from apps.core.models import Tag
from django.contrib.auth import get_user_model

User = get_user_model()

# --- Account Views ---

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'customers/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 10  # Zeigt 10 Accounts pro Seite an

    def get_queryset(self):
        # Nur Accounts des angemeldeten Benutzers anzeigen
        return Account.objects.filter(owner=self.request.user)

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'customers/account_detail.html'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        # Objekt holen und Berechtigung prüfen
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Account not found or permission denied")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Zugehörige Kontakte und Opportunities hinzufügen
        context['contacts'] = self.object.contacts.filter(owner=self.request.user)
        context['opportunities'] = self.object.opportunities.filter(owner=self.request.user)
        context['activities'] = self.object.activities.filter(account__owner=self.request.user)
        return context

class AccountCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'customers/account_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class AccountUpdateView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'customers/account_form.html'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Account not found or permission denied")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'customers/account_confirm_delete.html'
    success_url = reverse_lazy('customers:account_list')

    def get_object(self, queryset=None):
        # Objekt holen und Berechtigung prüfen
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Account not found or permission denied")
        return obj

# --- Contact Views ---

class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'customers/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 10  # Zeigt 10 Kontakte pro Seite an

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'customers/contact_detail.html'
    context_object_name = 'contact'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Contact not found or permission denied")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Zugehörige Aktivitäten hinzufügen
        context['activities'] = self.object.activities.filter(contact__owner=self.request.user)
        # Zugehörige Opportunities hinzufügen, falls vorhanden
        context['opportunities'] = self.object.opportunities.filter(owner=self.request.user) if hasattr(self.object, 'opportunities') else []
        return context

class ContactCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'customers/contact_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['accounts'] = Account.objects.filter(owner=self.request.user)
        return super().form_valid(form)

    # Optional: Wenn von Account-Seite erstellt, Account vorbelegen
    def get_initial(self):
        initial = super().get_initial()
        account_id = self.request.GET.get('account')
        if account_id:
            try:
                # Sicherstellen, dass der Account dem User gehört
                account = get_object_or_404(Account, pk=account_id, owner=self.request.user)
                initial['account'] = account
            except Http404:
                pass
        return initial

class ContactUpdateView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'customers/contact_form.html'
    context_object_name = 'object'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Contact not found or permission denied")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['accounts'] = Account.objects.filter(owner=self.request.user)
        return context

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'customers/contact_confirm_delete.html'
    success_url = reverse_lazy('customers:contact_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise Http404("Contact not found or permission denied")
        return obj
