# apps/customers/forms.py
from django import forms
from .models import Account, Contact

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        # Felder, die im Formular erscheinen sollen
        fields = [
            'name',
            'website',
            'phone_number',
            'address',
            'industry',
            'tags',
            'assigned_group',
        ]
        # Optional: Widgets anpassen für bessere Darstellung
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}), # Mehrzeilig für Adresse
            'tags': forms.SelectMultiple(attrs={'size': 5}), # Standard-Mehrfachauswahl
        }
        # Optional: Labels anpassen (Standard ist meist gut)
        labels = {
            'assigned_group': 'Zuständiges Team',
        }
        # Optional: Hilfe-Texte
        help_texts = {
            'website': 'Bitte vollständige URL eingeben (z.B. https://beispiel.de)',
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'job_title',
            'account', # Verknüpfung zur Firma
            'tags',
            'assigned_group',
        ]
        widgets = {
            'tags': forms.SelectMultiple(attrs={'size': 5}),
        }
        labels = {
             'account': 'Firma',
             'assigned_group': 'Zuständiges Team',
        }
        help_texts = {
            'account': 'Zu welcher Firma gehört dieser Kontakt?',
        }

    # Optional: Queryset für Account-Feld anpassen (z.B. nach User filtern)
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None) # User aus View übergeben
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         self.fields['account'].queryset = Account.objects.filter(owner=user)
    #         self.fields['assigned_group'].queryset = user.groups.all() # Nur Gruppen des Users?