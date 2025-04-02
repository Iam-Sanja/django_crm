# apps/opportunities/forms.py
from django import forms
from .models import Opportunity # OpportunityProduct wird meist separat behandelt (Inline Formsets)

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            'name',
            'account',
            'primary_contact',
            'amount',
            'close_date',
            'stage',
            'probability',
            'tags',
            'assigned_group',
            # 'campaign' # Später hinzufügen
        ]
        widgets = {
            'close_date': forms.DateInput(attrs={'type': 'date'}), # HTML5 Datums-Picker
            'tags': forms.SelectMultiple(attrs={'size': 5}),
            'probability': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }
        labels = {
             'account': 'Firma',
             'primary_contact': 'Primärer Kontakt',
             'close_date': 'Voraussichtl. Abschlussdatum',
             'stage': 'Phase',
             'probability': 'Wahrscheinlichkeit (%)',
             'assigned_group': 'Zuständiges Team',
        }

    # Optional: Queryset für primary_contact dynamisch basierend auf Account anpassen
    # Dies erfordert oft JavaScript oder zusätzliche Bibliotheken wie django-smart-selects.
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         self.fields['account'].queryset = Account.objects.filter(owner=user)
    #         # Filterung für primary_contact ist komplexer