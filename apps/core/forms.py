# apps/core/forms.py
from django import forms
from .models import Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            # Optional: Verwende einen HTML5-Farbwähler
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
        help_texts = {
            'color': 'Optional: Wähle eine Farbe für das Tag.',
        }