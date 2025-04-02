# apps/customers/models.py
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

class Account(models.Model):
    """Represents a company/organization."""
    name = models.CharField(_("Company Name"), max_length=255, unique=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    phone_number = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    address = models.TextField(_("Address"), blank=True, null=True)
    industry = models.CharField(_("Industry"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    owner = models.ForeignKey(User, related_name="owned_accounts", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_group = models.ForeignKey(Group, related_name="assigned_accounts", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned Team"))
    tags = models.ManyToManyField('core.Tag', blank=True, related_name="accounts", verbose_name=_("Tags"))

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ['name']

    def __str__(self):
        return self.name

class Contact(models.Model):
    """Represents an individual person."""
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email"), blank=True, null=True, unique=True) # Unique kann problematisch sein, wenn mehrere ohne E-Mail existieren sollen
    phone_number = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    job_title = models.CharField(_("Job Title"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    account = models.ForeignKey(Account, related_name="contacts", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Company")) # CASCADE: Wenn Firma gelöscht, Kontakt auch? Oder SET_NULL?
    owner = models.ForeignKey(User, related_name="owned_contacts", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_group = models.ForeignKey(Group, related_name="assigned_contacts", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned Team"))
    tags = models.ManyToManyField('core.Tag', blank=True, related_name="contacts", verbose_name=_("Tags"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['last_name', 'first_name']
        unique_together = [['first_name', 'last_name', 'account']] # Optional, um Duplikate pro Firma zu vermeiden

    def __str__(self):
        return f"{self.first_name} {self.last_name}"