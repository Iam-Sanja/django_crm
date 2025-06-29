from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json

from .models import Account, Contact
from apps.core.models import Tag

@login_required
@require_http_methods(["POST"])
def create_account(request):
    try:
        data = json.loads(request.body)
        
        # Account erstellen
        account = Account.objects.create(
            name=data.get('name'),
            website=data.get('website'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            street=data.get('street'),
            postal_code=data.get('postal_code'),
            city=data.get('city'),
            country=data.get('country'),
            owner=request.user
        )
        
        # Assigned Group setzen
        if data.get('assigned_group'):
            account.assigned_group_id = data.get('assigned_group')
            account.save()
        
        # Industry Tags verarbeiten
        industry_tags = data.get('industry_tags', '')
        if industry_tags:
            tag_names = [name.strip() for name in industry_tags.split(',') if name.strip()]
            industry_tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name, 
                    type='industry',
                    defaults={'color': '#3b82f6'}
                )
                industry_tag_objects.append(tag)
            account.industry.set(industry_tag_objects)
        
        # General Tags verarbeiten
        general_tags = data.get('general_tags', '')
        if general_tags:
            tag_names = [name.strip() for name in general_tags.split(',') if name.strip()]
            general_tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name, 
                    type='general',
                    defaults={'color': '#10b981'}
                )
                general_tag_objects.append(tag)
            account.tags.set(general_tag_objects)
            
        return JsonResponse({
            'status': 'success',
            'id': str(account.id),
            'name': account.name,
            'redirect_url': '/customers/accounts/'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def update_account(request, pk):
    try:
        data = json.loads(request.body)
        account = get_object_or_404(Account, pk=pk, owner=request.user)
        
        # Felder aktualisieren
        for field in ['name', 'website', 'phone_number', 'email', 'street', 'postal_code', 'city', 'country']:
            if field in data:
                setattr(account, field, data[field])
        
        # Assigned Group setzen
        if 'assigned_group' in data:
            account.assigned_group_id = data['assigned_group']
            
        account.save()
        
        # Industry Tags verarbeiten
        industry_tags = data.get('industry_tags', '')
        if industry_tags:
            tag_names = [name.strip() for name in industry_tags.split(',') if name.strip()]
            industry_tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name, 
                    type='industry',
                    defaults={'color': '#3b82f6'}
                )
                industry_tag_objects.append(tag)
            account.industry.set(industry_tag_objects)
        else:
            account.industry.clear()
        
        # General Tags verarbeiten
        general_tags = data.get('general_tags', '')
        if general_tags:
            tag_names = [name.strip() for name in general_tags.split(',') if name.strip()]
            general_tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name, 
                    type='general',
                    defaults={'color': '#10b981'}
                )
                general_tag_objects.append(tag)
            account.tags.set(general_tag_objects)
        else:
            account.tags.clear()
        
        return JsonResponse({
            'status': 'success',
            'id': str(account.id),
            'name': account.name,
            'redirect_url': '/customers/accounts/'
        })
    except Account.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Account not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["GET"])
def get_account_data(request, pk):
    """API-Endpunkt zum Laden der Account-Daten für das Bearbeiten"""
    try:
        account = get_object_or_404(Account, pk=pk, owner=request.user)
        
        # Industry Tags als Array von Objekten
        industry_tags = [
            {'name': tag.name, 'color': tag.color or '#3b82f6'}
            for tag in account.industry.all()  # Das ist korrekt
        ]
        general_tags = [
            {'name': tag.name, 'color': tag.color or '#10b981'}
            for tag in account.tags.all()  # Das ist auch korrekt
        ]
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'name': account.name,
                'website': account.website or '',
                'phone_number': account.phone_number or '',
                'email': account.email or '',
                'street': account.street or '',
                'postal_code': account.postal_code or '',
                'city': account.city or '',
                'country': account.country or '',
                'assigned_group': account.assigned_group.id if account.assigned_group else None,
                'industry_tags': industry_tags,
                'general_tags': general_tags
            }
        })
    except Account.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Account not found'
        }, status=404)

@login_required
@require_http_methods(["POST"])
def create_contact(request):
    try:
        data = json.loads(request.body)
        
        # Contact erstellen
        contact = Contact.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            mobile_number=data.get('mobile_number'),
            job_title=data.get('job_title'),
            street=data.get('street'),
            postal_code=data.get('postal_code'),
            city=data.get('city'),
            country=data.get('country'),
            owner=request.user
        )
        
        # Account zuweisen
        if data.get('account'):
            account = get_object_or_404(Account, pk=data['account'], owner=request.user)
            contact.account = account
        
        # Assigned Group setzen
        if data.get('assigned_group'):
            contact.assigned_group_id = data.get('assigned_group')
            
        contact.save()
        
        # Tags verarbeiten
        tags = data.get('tags', '')
        if tags:
            tag_names = [name.strip() for name in tags.split(',') if name.strip()]
            tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name, 
                    type='general',
                    defaults={'color': '#10b981'}
                )
                tag_objects.append(tag)
            contact.tags.set(tag_objects)
            
        return JsonResponse({
            'status': 'success',
            'id': str(contact.id),
            'name': f"{contact.first_name} {contact.last_name}",
            'redirect_url': '/customers/contacts/'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def update_contact(request, pk):
    try:
        data = json.loads(request.body)
        contact = get_object_or_404(Contact, pk=pk, owner=request.user)
        
        # Felder aktualisieren
        for field in ['first_name', 'last_name', 'email', 'phone_number', 
                     'mobile_number', 'job_title', 'street', 'postal_code', 'city', 'country']:
            if field in data:
                setattr(contact, field, data[field])
        
        # Account zuweisen
        if 'account' in data:
            account = get_object_or_404(Account, pk=data['account'], owner=request.user)
            contact.account = account
            
        # Assigned Group setzen
        if 'assigned_group' in data:
            contact.assigned_group_id = data['assigned_group']
            
        contact.save()
        
        # Tags verarbeiten
        tags = data.get('tags', '')
        if tags:
            tag_names = [name.strip() for name in tags.split(',') if name.strip()]
            tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name, 
                    type='general',
                    defaults={'color': '#10b981'}
                )
                tag_objects.append(tag)
            contact.tags.set(tag_objects)
        else:
            contact.tags.clear()
        
        return JsonResponse({
            'status': 'success',
            'id': str(contact.id),
            'name': f"{contact.first_name} {contact.last_name}",
            'redirect_url': '/customers/contacts/'
        })
    except Contact.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Contact not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["GET"])
def get_contact_data(request, pk):
    """API-Endpunkt zum Laden der Contact-Daten für das Bearbeiten"""
    try:
        contact = get_object_or_404(Contact, pk=pk, owner=request.user)
        
        # Tags als String
        tags = ', '.join([tag.name for tag in contact.tags.all()])
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email or '',
                'phone_number': contact.phone_number or '',
                'mobile_number': contact.mobile_number or '',
                'job_title': contact.job_title or '',
                'street': contact.street or '',
                'postal_code': contact.postal_code or '',
                'city': contact.city or '',
                'country': contact.country or '',
                'account': str(contact.account.id) if contact.account else None,
                'assigned_group': contact.assigned_group.id if contact.assigned_group else None,
                'tags': tags
            }
        })
    except Contact.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Contact not found'
        }, status=404)

@login_required
@require_http_methods(["DELETE"])
def delete_account(request, pk):
    try:
        account = get_object_or_404(Account, pk=pk, owner=request.user)
        account.delete()
        return JsonResponse({'status': 'success', 'redirect_url': '/customers/accounts/'})
    except Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
