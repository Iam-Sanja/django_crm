# apps/core/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin # Für Class-Based Views
from django.http import Http404 # Vergessen zu importieren? Evtl. nicht nötig für Tag

from .models import Tag
from .forms import TagForm

# --- Dashboard View ---
@login_required
def dashboard(request):
    context = {
        'welcome_message': f"Willkommen zurück, {request.user.first_name or request.user.username}!"
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