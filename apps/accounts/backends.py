from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailBackend(ModelBackend):
    """Backend für die Authentifizierung mit E-Mail statt Benutzername"""
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """Authentifiziere einen Benutzer anhand seiner E-Mail und seines Passworts"""
        # Wenn username übergeben wird (z.B. vom Standard-Login-Formular), 
        # verwende es als E-Mail
        if 'username' in kwargs and not email:
            email = kwargs.get('username')
            
        if email is None:
            return None
            
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Führe einen Passwort-Hash aus, um Timing-Angriffe zu verhindern
            User().set_password(password)
            return None
            
    def get_user(self, user_id):
        """Hole einen Benutzer anhand seiner ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
