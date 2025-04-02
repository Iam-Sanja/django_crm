# apps/leads/models.py
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
# Import Campaign model später, wenn 'campaigns' App existiert
# from apps.campaigns.models import Campaign

class Lead(models.Model):
    """Represents a potential customer/prospect."""

    class LeadStatus(models.TextChoices):
        NEW = 'NEW', _('New')
        CONTACTED = 'CONTACTED', _('Contacted')
        QUALIFIED = 'QUALIFIED', _('Qualified')
        LOST = 'LOST', _('Lost')
        UNQUALIFIED = 'UNQUALIFIED', _('Unqualified')
        # Füge hier weitere Status hinzu

    first_name = models.CharField(_("First Name"), max_length=100, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=100, blank=True, null=True) # Evtl. verpflichtend machen?
    company_name = models.CharField(_("Company"), max_length=255, blank=True, null=True)
    job_title = models.CharField(_("Job Title"), max_length=100, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone_number = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    status = models.CharField(_("Status"), max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)
    source = models.CharField(_("Source"), max_length=100, blank=True, null=True) # Evtl. auch Choices?
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    owner = models.ForeignKey(User, related_name="owned_leads", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_group = models.ForeignKey(Group, related_name="assigned_leads", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned Team"))
    tags = models.ManyToManyField('core.Tag', blank=True, related_name="leads", verbose_name=_("Tags"))
    notes = models.TextField(_("Notes"), blank=True, null=True)
    # campaign = models.ForeignKey(Campaign, related_name="leads", on_delete=models.SET_NULL, null=True, blank=True) # Später einkommentieren

    class Meta:
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")
        ordering = ['-created_at']

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.company_name:
            return self.company_name
        elif self.email:
            return self.email
        else:
            return f"Lead {self.id}"