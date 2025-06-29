# apps/customers/models.py
import uuid
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.core.models import Tag

def generate_uuid():
    """Generate UUID4 for primary keys"""
    return str(uuid.uuid4())

class Account(models.Model):
    """Represents a company/organization."""
    id = models.UUIDField(primary_key=True, default=generate_uuid, editable=False)
    name = models.CharField(_("Company Name"), max_length=255, unique=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    phone_number = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    
    # Adressfelder
    street = models.CharField(_("Street"), max_length=255, blank=True, null=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True, null=True)
    city = models.CharField(_("City"), max_length=100, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=100, blank=True, null=True, default="Deutschland")
    
    industry = models.ManyToManyField(Tag, blank=True, related_name="industry_accounts", verbose_name=_('Industry'), limit_choices_to={'type': 'industry'})
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_accounts", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_group = models.ForeignKey(Group, related_name="assigned_accounts", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned Team"))
    tags = models.ManyToManyField(Tag, blank=True, related_name="accounts", verbose_name=_('Tags'), limit_choices_to={'type': 'general'})

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_full_address(self):
        """Returns the complete address as a formatted string"""
        address_parts = []
        if self.street:
            address_parts.append(self.street)
        if self.postal_code and self.city:
            address_parts.append(f"{self.postal_code} {self.city}")
        elif self.city:
            address_parts.append(self.city)
        if self.country and self.country != "Deutschland":
            address_parts.append(self.country)
        return ", ".join(address_parts) if address_parts else None

class Contact(models.Model):
    """Represents an individual person."""
    id = models.UUIDField(primary_key=True, default=generate_uuid, editable=False)
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    email = models.EmailField(_("Email"), blank=True, null=True, unique=True) # Unique kann problematisch sein, wenn mehrere ohne E-Mail existieren sollen
    phone_number = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    mobile_number = models.CharField(_("Mobile"), max_length=50, blank=True, null=True)
    job_title = models.CharField(_("Job Title"), max_length=100, blank=True, null=True)
    
    # Adressfelder
    street = models.CharField(_("Street"), max_length=255, blank=True, null=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True, null=True)
    city = models.CharField(_("City"), max_length=100, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=100, blank=True, null=True, default="Deutschland")
    
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    account = models.ForeignKey(Account, related_name="contacts", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Company")) # CASCADE: Wenn Firma gelöscht, Kontakt auch? Oder SET_NULL?
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_contacts", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_group = models.ForeignKey(Group, related_name="assigned_contacts", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned Team"))
    tags = models.ManyToManyField('core.Tag', blank=True, related_name="contacts", verbose_name=_("Tags"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ['last_name', 'first_name']
        unique_together = [['first_name', 'last_name', 'account']] # Optional, um Duplikate pro Firma zu vermeiden

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_address(self):
        """Returns the complete address as a formatted string"""
        address_parts = []
        if self.street:
            address_parts.append(self.street)
        if self.postal_code and self.city:
            address_parts.append(f"{self.postal_code} {self.city}")
        elif self.city:
            address_parts.append(self.city)
        if self.country and self.country != "Deutschland":
            address_parts.append(self.country)
        return ", ".join(address_parts) if address_parts else None