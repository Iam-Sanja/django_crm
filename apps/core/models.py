# apps/core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class Tag(models.Model):
    """Model for tags/keywords."""
    name = models.CharField(_("Tag Name"), max_length=100, unique=True)
    color = models.CharField(_("Color"), max_length=7, blank=True, null=True, help_text=_("Optional Hex Color Code, e.g., #FFFFFF"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']

    def __str__(self):
        return self.name

class Note(models.Model):
    """Model for generic notes related to other objects."""
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="notes_created", on_delete=models.SET_NULL, null=True, blank=True)

    # Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.created_by} on {self.created_at.strftime('%Y-%m-%d')}"

class Attachment(models.Model):
    """Model for file attachments related to other objects."""
    file = models.FileField(_("File"), upload_to='attachments/%Y/%m/%d/') # Struktur für Upload-Pfad
    file_name = models.CharField(_("File Name"), max_length=255, blank=True) # Wird oft automatisch gesetzt
    mime_type = models.CharField(_("MIME Type"), max_length=100, blank=True) # Wird oft automatisch gesetzt
    size = models.PositiveIntegerField(_("Size (Bytes)"), blank=True, null=True) # Kann beim Speichern berechnet werden
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, related_name="attachments_uploaded", on_delete=models.SET_NULL, null=True, blank=True)

    # Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if not self.file_name:
            self.file_name = self.file.name
        # Hier könnte man auch mime_type und size ermitteln, falls nicht schon geschehen
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name or f"Attachment {self.id}"