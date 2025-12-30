"""
API Dependencies
Kimlik doğrulama ve ortak bağımlılıklar
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.supabase_client import get_supabase

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    JWT token'dan kullanıcı bilgisini alır.
    Her korumalı endpoint'te kullanılır.
    """
    
    token = credentials.credentials
    supabase = get_supabase()
    
    try:
        # Supabase token'ı doğrular ve kullanıcıyı döner
        response = supabase.auth.get_user(token)
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz veya süresi dolmuş token"
            )
        
        return {
            "id": response.user.id,
            "email": response.user.email,
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kimlik doğrulama başarısız"
        )
