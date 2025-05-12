from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
import json

from .models import Account, Contact

@login_required
@require_http_methods(["POST"])
def create_account(request):
    try:
        data = json.loads(request.body)
        account = Account.objects.create(
            name=data.get('name'),
            website=data.get('website'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            address=data.get('address'),
            industry=data.get('industry'),
            owner=request.user
        )
        if data.get('tags'):
            account.tags.set(data.get('tags'))
        if data.get('assigned_group'):
            account.assigned_group_id = data.get('assigned_group')
            account.save()
            
        return JsonResponse({
            'status': 'success',
            'id': account.id,
            'name': account.name
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
        account = Account.objects.get(pk=pk, owner=request.user)
        
        for field in ['name', 'website', 'phone_number', 'email', 'address', 'industry']:
            if field in data:
                setattr(account, field, data[field])
        
        if 'tags' in data:
            account.tags.set(data['tags'])
        if 'assigned_group' in data:
            account.assigned_group_id = data['assigned_group']
            
        account.save()
        return JsonResponse({
            'status': 'success',
            'id': account.id,
            'name': account.name
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
@require_http_methods(["POST"])
def create_contact(request):
    try:
        data = json.loads(request.body)
        contact = Contact.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            mobile_number=data.get('mobile_number'),
            job_title=data.get('job_title'),
            address=data.get('address'),
            owner=request.user
        )
        
        if data.get('account'):
            account = Account.objects.get(pk=data['account'], owner=request.user)
            contact.account = account
            
        if data.get('tags'):
            contact.tags.set(data.get('tags'))
        if data.get('assigned_group'):
            contact.assigned_group_id = data.get('assigned_group')
            
        contact.save()
        return JsonResponse({
            'status': 'success',
            'id': contact.id,
            'name': f"{contact.first_name} {contact.last_name}"
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
        contact = Contact.objects.get(pk=pk, owner=request.user)
        
        for field in ['first_name', 'last_name', 'email', 'phone_number', 
                     'mobile_number', 'job_title', 'address']:
            if field in data:
                setattr(contact, field, data[field])
        
        if 'account' in data:
            account = Account.objects.get(pk=data['account'], owner=request.user)
            contact.account = account
            
        if 'tags' in data:
            contact.tags.set(data['tags'])
        if 'assigned_group' in data:
            contact.assigned_group_id = data['assigned_group']
            
        contact.save()
        return JsonResponse({
            'status': 'success',
            'id': contact.id,
            'name': f"{contact.first_name} {contact.last_name}"
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
