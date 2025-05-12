# apps/opportunities/models.py
from django.db import models
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Import Product später
# from apps.products.models import Product
# Import Campaign später
# from apps.campaigns.models import Campaign


class Opportunity(models.Model):
    """Represents a sales deal or potential sale."""

    class OpportunityStage(models.TextChoices):
        QUALIFICATION = 'QUALIFICATION', _('Qualification')
        NEEDS_ANALYSIS = 'NEEDS_ANALYSIS', _('Needs Analysis')
        PROPOSAL = 'PROPOSAL', _('Proposal/Price Quote')
        NEGOTIATION = 'NEGOTIATION', _('Negotiation/Review')
        CLOSED_WON = 'CLOSED_WON', _('Closed Won')
        CLOSED_LOST = 'CLOSED_LOST', _('Closed Lost')
        # Füge hier weitere Phasen hinzu

    name = models.CharField(_("Opportunity Name"), max_length=255)
    account = models.ForeignKey('customers.Account', related_name="opportunities", on_delete=models.CASCADE, verbose_name=_("Account")) # Wenn Account gelöscht, was passiert mit Opportunity? PROTECT?
    primary_contact = models.ForeignKey('customers.Contact', related_name="opportunities", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Primary Contact"))
    amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2, default=0.00) # Oder berechnet aus OpportunityProduct?
    close_date = models.DateField(_("Expected Close Date"))
    stage = models.CharField(_("Stage"), max_length=20, choices=OpportunityStage.choices, default=OpportunityStage.QUALIFICATION)
    probability = models.IntegerField( # Oder FloatField? Integer oft einfacher.
        _("Probability (%)"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True,
        help_text=_("Likelihood of closing the deal (0-100%)")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_opportunities", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_group = models.ForeignKey(Group, related_name="assigned_opportunities", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Assigned Team"))
    tags = models.ManyToManyField('core.Tag', blank=True, related_name="opportunities", verbose_name=_("Tags"))
    # campaign = models.ForeignKey(Campaign, related_name="opportunities", on_delete=models.SET_NULL, null=True, blank=True) # Später einkommentieren

    # ManyToMany zu Product wird über die Zwischentabelle OpportunityProduct definiert
    # products = models.ManyToManyField('products.Product', through='OpportunityProduct', related_name='opportunities_ M2M', blank=True) # Später einkommentieren

    class Meta:
        verbose_name = _("Opportunity")
        verbose_name_plural = _("Opportunities")
        ordering = ['-close_date']

    def __str__(self):
        return f"{self.name} ({self.account.name})"

class OpportunityProduct(models.Model):
    """Intermediate model linking Products to an Opportunity."""
    opportunity = models.ForeignKey(Opportunity, related_name="product_lines", on_delete=models.CASCADE)

    # --- AUSKOMMENTIERT ---
    # TODO: Aktivieren, wenn 'products' App und Product-Modell existieren
    # product = models.ForeignKey('products.Product', related_name="opportunity_lines", on_delete=models.CASCADE)
    # -----------------------

    # product = models.ForeignKey(Product, related_name="opportunity_lines", on_delete=models.CASCADE) # Später einkommentieren
    # product = models.ForeignKey('products.Product', related_name="opportunity_lines", on_delete=models.CASCADE, null=True) # Platzhalter, bis Product App existiert - oder Fehler auslösen?
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    price_per_unit = models.DecimalField(_("Price Per Unit"), max_digits=12, decimal_places=2) # Kann vom Product Standardpreis abweichen
    discount = models.DecimalField(_("Discount (%)"), max_digits=5, decimal_places=2, default=0.00, help_text=_("Percentage discount (e.g., 10.5 for 10.5%)"))
    total_price = models.DecimalField(_("Total Line Price"), max_digits=12, decimal_places=2, blank=True) # Wird berechnet

    class Meta:
        verbose_name = _("Opportunity Product Line")
        verbose_name_plural = _("Opportunity Product Lines")
        # unique_together = [['opportunity', 'product']] # Kann ein Produkt nur einmal pro Opportunity vorkommen?

    def calculate_total_price(self):
        discount_factor = (100 - self.discount) / 100
        return self.quantity * self.price_per_unit * discount_factor

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
        # Optional: Hier die Opportunity.amount Summe aktualisieren (z.B. via Signal oder direkter Methode)

    def __str__(self):
        # return f"{self.quantity} x {self.product.name} for {self.opportunity.name}" # Wenn Product verknüpft ist
        return f"{self.quantity} x Product ID {self.product_id} for Opportunity {self.opportunity.id}" # Platzhalter