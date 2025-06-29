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
    from apps.accounts.models import CustomUser
    
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