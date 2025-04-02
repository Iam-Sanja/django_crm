# apps/activities/forms.py
from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'type',
            'subject',
            'notes',
            'activity_date',
            'status',
            'assigned_to',
            'account',
            'contact',
            'opportunity',
            'lead',
            # 'case' # Später hinzufügen
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
            'activity_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), # HTML5 Datetime-Picker
        }
        labels = {
             'activity_date': 'Datum/Fälligkeit',
             'assigned_to': 'Zugewiesen an',
             'account': 'Bezug: Firma',
             'contact': 'Bezug: Kontakt',
             'opportunity': 'Bezug: Opportunity',
             'lead': 'Bezug: Lead',
        }
        help_texts = {
             'account': 'Optional: Wenn sich die Aktivität auf eine Firma bezieht.',
             'contact': 'Optional: Wenn sich die Aktivität auf einen Kontakt bezieht.',
             'opportunity': 'Optional: Wenn sich die Aktivität auf eine Opportunity bezieht.',
             'lead': 'Optional: Wenn sich die Aktivität auf einen Lead bezieht.',
        }

    # Custom Validation: Sicherstellen, dass maximal *ein* Bezug ausgewählt ist
    def clean(self):
        cleaned_data = super().clean()
        related_objects = [
            cleaned_data.get('account'),
            cleaned_data.get('contact'),
            cleaned_data.get('opportunity'),
            cleaned_data.get('lead'),
            # cleaned_data.get('case'), # Später hinzufügen
        ]
        # Zählt, wie viele der Bezugsfelder nicht leer (None) sind
        related_count = sum(1 for obj in related_objects if obj is not None)

        # Erlaube 0 oder 1 Bezug. Wenn 0 erlaubt ist, kann eine Aktivität
        # auch "allgemein" sein oder nur einem Benutzer zugewiesen sein.
        # Wenn immer ein Bezug nötig ist, prüfe auf `related_count != 1`.
        if related_count > 1:
            raise forms.ValidationError(
                "Bitte wählen Sie maximal einen Bezug aus (Firma, Kontakt, Opportunity oder Lead)."
            )
            # Man könnte auch spezifischere Fehler pro Feld hinzufügen, aber das ist einfacher.

        # TODO: Hier könnte man auch prüfen, ob der User Zugriff auf das gewählte Bezugsobjekt hat.
        # Dies ist aber oft einfacher in der View zu handhaben.

        return cleaned_data

    # Optional: Querysets für Bezugsfelder filtern
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         # Beispiel: Nur Accounts anzeigen, die dem User gehören
    #         self.fields['account'].queryset = Account.objects.filter(owner=user)
    #         # Ähnlich für Contact, Opportunity, Lead...
    #         # Für 'assigned_to' vielleicht nur User aus den eigenen Gruppen?
    #         self.fields['assigned_to'].queryset = User.objects.filter(is_active=True) # Alle aktiven User