# apps/leads/forms.py
from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'first_name',
            'last_name',
            'company_name',
            'email',
            'phone_number',
            'status',
            'source',
            'tags',
            'assigned_group',
            # 'campaign' # Später hinzufügen
        ]
        widgets = {
            'tags': forms.SelectMultiple(attrs={'size': 5}),
        }
        labels = {
             'company_name': 'Firma',
             'assigned_group': 'Zuständiges Team',
        }