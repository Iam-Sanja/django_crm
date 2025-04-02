# apps/activities/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Activity(models.Model):
    """Logs interactions like calls, meetings, tasks."""

    class ActivityType(models.TextChoices):
        CALL = 'CALL', _('Call')
        MEETING = 'MEETING', _('Meeting')
        EMAIL = 'EMAIL', _('Email')
        TASK = 'TASK', _('Task')
        NOTE = 'NOTE', _('Note Added') # Falls einfache Notizen auch als Aktivität geloggt werden sollen
        # Füge hier weitere Typen hinzu

    class ActivityStatus(models.TextChoices):
        PLANNED = 'PLANNED', _('Planned')
        HELD = 'HELD', _('Held')
        COMPLETED = 'COMPLETED', _('Completed')
        NOT_HELD = 'NOT_HELD', _('Not Held')
        CANCELED = 'CANCELED', _('Canceled')
        # Füge hier weitere Status hinzu (insb. für Tasks)

    type = models.CharField(_("Type"), max_length=20, choices=ActivityType.choices)
    subject = models.CharField(_("Subject"), max_length=255)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    activity_date = models.DateTimeField(_("Activity Date / Due Date"), default=timezone.now)
    status = models.CharField(_("Status"), max_length=20, choices=ActivityStatus.choices, default=ActivityStatus.PLANNED)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    assigned_to = models.ForeignKey(User, related_name="activities", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned To"))

    # Optional relations to other objects
    account = models.ForeignKey('customers.Account', related_name="activities", on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey('customers.Contact', related_name="activities", on_delete=models.CASCADE, null=True, blank=True)
    opportunity = models.ForeignKey('opportunities.Opportunity', related_name="activities", on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey('leads.Lead', related_name="activities", on_delete=models.CASCADE, null=True, blank=True)
    # case = models.ForeignKey('cases.Case', related_name="activities", on_delete=models.CASCADE, null=True, blank=True) # Später einkommentieren

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        ordering = ['-activity_date']

    def __str__(self):
        return f"{self.get_type_display()}: {self.subject} ({self.activity_date.strftime('%Y-%m-%d')})"