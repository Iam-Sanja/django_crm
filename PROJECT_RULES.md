# Django Project Rules & Best Practices

## Projektstruktur (Best Practice)

```
project_root/
├── apps/                    # Alle Django Apps hier
│   ├── authentication/      # Benutzerauthentifizierung
│   ├── core/               # Kernfunktionalitäten
│   └── __init__.py
├── templates/               # Alle Templates
│   ├── base.html
│   ├── authentication/
│   └── core/
├── static/                  # Statische Dateien
├── media/                   # Benutzer-Uploads
├── tests/                   # Test-Dateien
│   ├── conftest.py
│   ├── authentication/
│   └── core/
├── core_project/            # Projekt-Einstellungen
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md
```

## Apps-Konfiguration

### Apps-Verzeichnis Setup
- Erstelle ein `apps/` Verzeichnis im Projekt-Root
- Alle Django Apps in `apps/` platzieren
- Korrekte `sys.path` Konfiguration in `manage.py` und `wsgi.py`/`asgi.py`

```python
# manage.py
import os
import sys
from pathlib import Path

def main():
    # Add apps directory to Python path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR / 'apps'))
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
    # ... rest of manage.py
```

### App-Registrierung
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'corsheaders',
    'ninja',
    
    # Local apps
    'apps.authentication',
    'apps.core',
]
```

## Custom User Model

### User Model Best Practices
- Verwende E-Mail als primären Identifier (kein Username-Feld)
- Erbe von `AbstractBaseUser` und `PermissionsMixin`
- Implementiere CustomUserManager

```python
# apps/authentication/models.py
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
```

## Settings-Konfiguration

### Strukturierte Settings
```python
# core_project/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'corsheaders',
    'ninja',
    
    # Local apps
    'apps.authentication',
    'apps.core',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core_project.wsgi.application'

# Database
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Model
AUTH_USER_MODEL = 'authentication.CustomUser'

# Internationalization
LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# CORS settings
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'] if DEBUG else ['file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'] if DEBUG else ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## Django Ninja API Setup

### API-Konfiguration
```python
# core_project/api.py
from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.conf import settings
import jwt
from apps.authentication.models import CustomUser

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            if user.is_active:
                return user
        except (jwt.InvalidTokenError, CustomUser.DoesNotExist):
            return None

api = NinjaAPI(
    title="Django API",
    version="1.0.0",
    description="API Documentation",
    auth=AuthBearer(),
)
```

### API Router
```python
# apps/authentication/api.py
from ninja import Router
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

router = Router()

class UserSchema(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""

@router.post("/register", response=UserSchema)
def register(request, data: RegisterSchema):
    from apps.authentication.models import CustomUser
    
    if CustomUser.objects.filter(email=data.email).exists():
        return {"error": "Benutzer existiert bereits"}
    
    user = CustomUser.objects.create_user(
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    
    return UserSchema(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )

@router.post("/login")
def login(request, data: LoginSchema):
    user = authenticate(email=data.email, password=data.password)
    if not user:
        return {"error": "Ungültige Anmeldedaten"}
    
    payload = {
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    return {"token": token, "user": UserSchema(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )}

@router.get("/me", response=UserSchema)
def get_user_info(request):
    return UserSchema(
        id=str(request.user.id),
        email=request.user.email,
        first_name=request.user.first_name,
        last_name=request.user.last_name
    )
```

## Testing Setup

### Pytest-Konfiguration
```ini
# pytest.ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = core_project.settings
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

### Test-Konfiguration
```python
# tests/conftest.py
import pytest
from ninja.testing import TestClient
from django.test import Client
from apps.authentication.models import CustomUser

@pytest.fixture
def api_client():
    from core_project.api import api
    return TestClient(api)

@pytest.fixture
def django_client():
    return Client()

@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def admin_user():
    return CustomUser.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123'
    )
```

### API-Tests
```python
# tests/authentication/test_api.py
import pytest
from ninja.testing import TestClient
from apps.authentication.models import CustomUser

def test_register_user(api_client):
    response = api_client.post("/auth/register", json={
        "email": "new@example.com",
        "password": "testpass123",
        "first_name": "New",
        "last_name": "User"
    })
    
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
    assert CustomUser.objects.filter(email="new@example.com").exists()

def test_login_user(api_client, user):
    response = api_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    assert "token" in response.json()

def test_get_user_info(api_client, user):
    # First login to get token
    login_response = api_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = login_response.json()["token"]
    
    # Use token to get user info
    response = api_client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```

## Models & Database

### Primary Keys
- **Verwende UUID4** für Primary Keys
- Verwende `generate_uuid()` Funktion für UUID-Generierung

### Feld-Konventionen
- **Variablennamen:** Immer Englisch
- **verbose_name:** Immer Deutsch für Benutzer-Labels
- **help_text:** Immer Deutsch
- **choices:** Verwende englische Keys, deutsche Werte

```python
class ExampleModel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Name",
        help_text="Geben Sie einen Namen ein"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Aktiv'),
            ('inactive', 'Inaktiv'),
        ],
        verbose_name="Status"
    )

    class Meta:
        verbose_name = "Beispiel"
        verbose_name_plural = "Beispiele"
        ordering = ['name']
```

## Views & URLs

### View-Konventionen
- **Funktionsnamen:** Immer Englisch
- **Variablennamen:** Immer Englisch
- **Kommentare:** Deutsch für Business-Logik, Englisch für technische Details
- **Django Forms erlaubt:** Verwende Django Forms für komplexe Formularverarbeitung

### URL-Patterns
- Verwende englische Namen für URL-Patterns
- Verwende beschreibende Namen
- Gruppiere verwandte URLs

```python
# urls.py
app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_item, name='create'),
    path('item/<uuid:item_id>/', views.item_detail, name='detail'),
    path('item/<uuid:item_id>/edit/', views.edit_item, name='edit'),
]
```

## Templates

### Template-Struktur
- Alle Templates erweitern `base.html`
- Verwende Bootstrap 5 für Styling
- Verwende Font Awesome für Icons
- Deutscher Text-Inhalt
- Englische Variablennamen

### Template-Konventionen
```html
{% extends 'base.html' %}

{% block title %}Beispiel{% endblock %}

{% block content %}
<div class="container">
    <h1>Beispiel-Titel</h1>
    
    <form method="post">
        {% csrf_token %}
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        
        <button type="submit" class="btn btn-primary">
            <i class="fas fa-save me-2"></i>Speichern
        </button>
    </form>
</div>
{% endblock %}
```

## Admin-Konfiguration

### Admin-Konventionen
- Deutsche verbose names
- Englische Feldnamen
- Angemessene List-Displays und Filter

```python
# apps/authentication/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Persönliche Informationen', {'fields': ('first_name', 'last_name')}),
        ('Berechtigungen', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Wichtige Daten', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
```

## Sicherheit

### Authentifizierung
- Verwende Django's eingebaute Authentifizierung
- Custom User Model mit E-Mail
- Angemessene Berechtigungsprüfungen in Views

### Datenvalidierung
- Validiere alle Benutzereingaben in Views
- Verwende Django's eingebaute Validatoren
- Custom Validierungsfunktionen bei Bedarf

## Dependencies

### Erforderliche Pakete
```
Django>=5.0
django-ninja>=1.0
python-dotenv>=1.0
PyJWT>=2.8
psycopg2-binary>=2.9  # Für PostgreSQL (Produktion)
django-cors-headers>=4.0
```

### Entwicklungs-Pakete
```
pytest-django>=4.5
factory-boy>=3.2
black>=23.0  # Code-Formatierung
flake8>=6.0  # Linting
```

## Umgebungsvariablen

### .env.example
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Production)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
```

## Deployment

### Umgebungsvariablen
- Verwende python-dotenv für Konfiguration
- Committe niemals sensible Daten
- Verwende .env-Dateien für lokale Entwicklung

### Statische Dateien
- Verwende Django's statische Dateiverwaltung
- Konfiguriere angemessene statische Datei-Bereitstellung in Produktion
- Verwende CDN für externe Ressourcen

## Performance

### Datenbank
- Verwende select_related() und prefetch_related()
- Optimiere Queries in Views
- Verwende Datenbank-Indizes für häufig abgefragte Felder

### Caching
- Verwende Django's Caching-Framework
- Cache teure Operationen
- Verwende angemessene Cache-Timeouts

## Monitoring

### Logging
- Konfiguriere angemessene Logging-Levels
- Logge wichtige Business-Events
- Verwende strukturiertes Logging

### Fehlerbehandlung
- Verwende try-except Blöcke angemessen
- Logge Fehler mit Kontext
- Biete benutzerfreundliche Fehlermeldungen

## Code-Style

### Python
- Folge PEP 8
- Verwende Type Hints wo angemessen
- Deutsche Kommentare für Business-Logik
- Englische Kommentare für technische Details

### JavaScript
- Verwende moderne ES6+ Syntax
- Deutsche Kommentare für benutzerorientierte Logik
- Englische Variablen- und Funktionsnamen

### CSS
- Verwende Bootstrap-Klassen wenn möglich
- Custom CSS in komponentenspezifischen Dateien
- Deutsche Kommentare für Styling-Entscheidungen

## Migration Guidelines

### Migrationen erstellen
- Überprüfe immer generierte Migrationen
- Teste Migrationen mit Entwicklungsdaten
- Verwende beschreibende Migrationsnamen

### Daten-Migrationen
- Erstelle Daten-Migrationen für komplexe Änderungen
- Teste mit produktionsähnlichen Daten
- Dokumentiere Migrationsschritte

## Frontend/UI – Tagging-Felder

- Es wird **kein Bootstrap** und **kein Bootstrap-Tagsinput** verwendet.
- Für Tagging-Felder wird ein modernes, leichtgewichtiges JavaScript-Tagging-Input genutzt (z.B. [Tagify](https://github.com/yairEO/tagify) oder eine eigene Alpine.js-Komponente).
- Die Tag-Komponente muss:
  - Farben pro Tag unterstützen (z.B. aus der Datenbank)
  - Kompakt, barrierefrei und Tailwind-kompatibel sein
  - Einfaches Hinzufügen, Entfernen und Bearbeiten von Tags ermöglichen
- Die Integration und das Styling erfolgen ausschließlich mit Tailwind CSS und Custom CSS.

---

**Wichtig:** Diese Regeln gewährleisten Konsistenz im Projekt und erleichtern es Teammitgliedern, den Codebase zu verstehen und zu warten. 