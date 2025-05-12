from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib import messages

class EmailAuthenticationForm(AuthenticationForm):
    """Angepasstes Authentifizierungsformular für E-Mail-Login"""
    username = forms.EmailField(
        label='E-Mail', 
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'})
    )
    
    password = forms.CharField(
        label='Passwort',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'E-Mail'

class LoginView(FormView):
    """View für den Login mit E-Mail"""
    form_class = EmailAuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('core:dashboard')  # Passe dies an deine URL an
    
    def form_valid(self, form):
        """Wenn das Formular gültig ist, logge den Benutzer ein"""
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Willkommen zurück, {user.get_full_name() or user.email}!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Ungültige E-Mail oder Passwort.")
            return self.form_invalid(form)
    
    def get_success_url(self):
        """Bestimme die Weiterleitungs-URL nach erfolgreichem Login"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

class LogoutView(View):
    """View für den Logout"""
    def get(self, request):
        """Logge den Benutzer aus und leite zur Login-Seite weiter"""
        logout(request)
        messages.info(request, "Du wurdest erfolgreich abgemeldet.")
        return redirect('accounts:login')
        
    def post(self, request):
        """Logge den Benutzer aus und leite zur Login-Seite weiter (für POST-Anfragen)"""
        logout(request)
        messages.info(request, "Du wurdest erfolgreich abgemeldet.")
        return redirect('accounts:login')


class CustomPasswordResetView(PasswordResetView):
    """View für das Anfordern eines Passwort-Reset-Links"""
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def form_valid(self, form):
        """Wenn das Formular gültig ist, zeige eine Erfolgsmeldung an"""
        messages.info(self.request, "Wenn ein Konto mit dieser E-Mail existiert, wurde eine E-Mail mit Anweisungen zum Zurücksetzen des Passworts gesendet.")
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    """View für die Bestätigungsseite nach dem Anfordern eines Passwort-Reset-Links"""
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """View für das Setzen eines neuen Passworts"""
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """View für die Bestätigungsseite nach dem erfolgreichen Zurücksetzen des Passworts"""
    template_name = 'accounts/password_reset_complete.html'