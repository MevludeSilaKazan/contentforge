"""
Auth Routes
Kullanıcı kayıt ve giriş işlemleri
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from database.supabase_client import get_supabase

router = APIRouter(prefix="/auth", tags=["auth"])


# ============================================================
# ŞEMALAR
# ============================================================

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "kullanici@example.com",
                "password": "güçlü_şifre_123"
            }
        }


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    message: str
    access_token: str | None = None
    user: dict | None = None


# ============================================================
# ENDPOINT'LER
# ============================================================

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """
    Yeni kullanıcı kaydı oluşturur.
    """
    
    supabase = get_supabase()
    
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
        })
        
        if response.user:
            # Profil oluştur
            try:
                supabase.table("profiles").insert({
                    "id": response.user.id,
                    "email": request.email,
                    "plan": "free",
                }).execute()
            except Exception:
                pass  # Profil zaten varsa devam et
            
            return AuthResponse(
                message="Kayıt başarılı",
                access_token=response.session.access_token if response.session else None,
                user={"id": response.user.id, "email": response.user.email}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kayıt oluşturulamadı"
            )
            
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu email zaten kayıtlı"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Kayıt hatası: {error_msg}"
        )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """
    Kullanıcı girişi yapar, JWT token döner.
    """
    
    supabase = get_supabase()
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })
        
        if response.user and response.session:
            return AuthResponse(
                message="Giriş başarılı",
                access_token=response.session.access_token,
                user={"id": response.user.id, "email": response.user.email}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email veya şifre hatalı"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı"
        )


@router.post("/logout")
async def logout():
    """
    Oturumu sonlandırır.
    """
    # Client-side token silme yeterli, 
    # Supabase stateless JWT kullanıyor
    return {"message": "Çıkış başarılı"}
