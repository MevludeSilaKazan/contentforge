"""
User Routes
Kullanıcı profil ve kullanım bilgisi
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime, timezone
from api.deps import get_current_user
from database.supabase_client import get_supabase
from config.settings import FREE_MONTHLY_LIMIT, PRO_MONTHLY_LIMIT

router = APIRouter(prefix="/user", tags=["user"])


# ============================================================
# ŞEMALAR
# ============================================================

class UsageResponse(BaseModel):
    plan: str
    used: int
    limit: int
    remaining: int
    reset_date: str


class ProfileResponse(BaseModel):
    id: str
    email: str
    plan: str
    created_at: str | None = None


# ============================================================
# ENDPOINT'LER
# ============================================================

@router.get("/usage", response_model=UsageResponse)
async def get_usage(current_user: dict = Depends(get_current_user)):
    """
    Kullanıcının aylık kullanım bilgisini getirir.
    """
    
    user_id = current_user["id"]
    supabase = get_supabase()
    
    try:
        # Plan bilgisi
        profile = supabase.table("profiles") \
            .select("plan") \
            .eq("id", user_id) \
            .single() \
            .execute()
        
        plan = profile.data.get("plan", "free") if profile.data else "free"
        limit = PRO_MONTHLY_LIMIT if plan == "pro" else FREE_MONTHLY_LIMIT
        
        # Bu ayki kullanım
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        usage = supabase.table("contents") \
            .select("id", count="exact") \
            .eq("user_id", user_id) \
            .gte("created_at", month_start.isoformat()) \
            .execute()
        
        used = usage.count or 0
        
        # Sonraki ayın başlangıcı (reset tarihi)
        if now.month == 12:
            reset_date = now.replace(year=now.year + 1, month=1, day=1)
        else:
            reset_date = now.replace(month=now.month + 1, day=1)
        
        return UsageResponse(
            plan=plan,
            used=used,
            limit=limit,
            remaining=max(0, limit - used),
            reset_date=reset_date.strftime("%Y-%m-%d")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kullanım bilgisi alınamadı: {str(e)}"
        )


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Kullanıcı profil bilgisini getirir.
    """
    
    user_id = current_user["id"]
    supabase = get_supabase()
    
    try:
        result = supabase.table("profiles") \
            .select("*") \
            .eq("id", user_id) \
            .single() \
            .execute()
        
        if not result.data:
            # Profil yoksa oluştur
            supabase.table("profiles").insert({
                "id": user_id,
                "email": current_user["email"],
                "plan": "free",
            }).execute()
            
            return ProfileResponse(
                id=user_id,
                email=current_user["email"],
                plan="free"
            )
        
        return ProfileResponse(
            id=result.data["id"],
            email=result.data["email"],
            plan=result.data["plan"],
            created_at=result.data.get("created_at")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profil alınamadı: {str(e)}"
        )


@router.patch("/upgrade")
async def upgrade_to_pro(current_user: dict = Depends(get_current_user)):
    """
    Kullanıcıyı Pro plana yükseltir.
    NOT: Gerçek ödeme entegrasyonu sonra eklenecek.
    """
    
    user_id = current_user["id"]
    supabase = get_supabase()
    
    try:
        supabase.table("profiles") \
            .update({"plan": "pro"}) \
            .eq("id", user_id) \
            .execute()
        
        return {"message": "Pro plana yükseltildi", "plan": "pro"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Yükseltme hatası: {str(e)}"
        )
