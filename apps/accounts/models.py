import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

def generate_uuid():
    """Generate UUID4 for primary keys"""
    return str(uuid.uuid4())

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('E-Mail-Adresse ist erforderlich')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=generate_uuid, editable=False)
    email = models.EmailField(unique=True, verbose_name="E-Mail-Adresse")
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Vorname")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Nachname")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_staff = models.BooleanField(default=False, verbose_name="Mitarbeiter")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Registriert am")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Benutzer"
        verbose_name_plural = "Benutzer"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name
