"""
Blog Routes
İçerik oluşturma ve yönetim + SSE streaming
"""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime, timezone
from api.deps import get_current_user
from database.supabase_client import get_supabase
from agents.blog_agents import run_blog_pipeline, run_blog_pipeline_streaming, get_agents_info, AGENTS
from config.settings import FREE_MONTHLY_LIMIT, PRO_MONTHLY_LIMIT

router = APIRouter(prefix="/blog", tags=["blog"])


# ============================================================
# ŞEMALAR
# ============================================================

class BlogCreateRequest(BaseModel):
    topic: str
    audience: str = "general"  # general, professional, entrepreneur, technical
    tone: str = "friendly"     # formal, friendly, educational, persuasive
    length: str = "medium"     # short (500), medium (1000), long (2000+)
    format_type: str = "standard"  # standard, listicle, howto, comparison, casestudy
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Yapay zeka ve e-ticaret",
                "audience": "entrepreneur",
                "tone": "friendly",
                "length": "medium",
                "format_type": "listicle"
            }
        }


class BlogResponse(BaseModel):
    id: str
    topic: str
    content: str
    created_at: str
    quality: Optional[dict] = None
    

class BlogListResponse(BaseModel):
    blogs: list[BlogResponse]
    total: int


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def get_user_plan(user_id: str) -> str:
    """Kullanıcının planını getirir, profil yoksa oluşturur"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("profiles") \
            .select("plan") \
            .eq("id", user_id) \
            .execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0].get("plan", "free")
        
        # Profil yoksa oluştur
        supabase.table("profiles").insert({
            "id": user_id,
            "email": "",
            "plan": "free",
        }).execute()
        
        return "free"
        
    except Exception:
        return "free"


def get_monthly_usage(user_id: str) -> int:
    """Bu ayki kullanım sayısını getirir"""
    supabase = get_supabase()
    
    # Bu ayın başlangıcı
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    result = supabase.table("contents") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .gte("created_at", month_start.isoformat()) \
        .execute()
    
    return result.count or 0


def check_usage_limit(user_id: str) -> tuple[bool, int, int]:
    """
    Kullanım limitini kontrol eder.
    Returns: (limit_aşıldı_mı, kullanılan, limit)
    """
    plan = get_user_plan(user_id)
    usage = get_monthly_usage(user_id)
    limit = PRO_MONTHLY_LIMIT if plan == "pro" else FREE_MONTHLY_LIMIT
    
    return (usage >= limit, usage, limit)


# ============================================================
# ENDPOINT'LER
# ============================================================

@router.post("/create", response_model=BlogResponse)
async def create_blog(
    request: BlogCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Yeni blog yazısı oluşturur.
    """
    
    user_id = current_user["id"]
    
    # Limit kontrolü
    limit_exceeded, usage, limit = check_usage_limit(user_id)
    
    if limit_exceeded:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Aylık limit doldu ({usage}/{limit}). Pro plana geçin."
        )
    
    try:
        # Blog oluştur - zengin parametrelerle
        results = run_blog_pipeline(
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            length=request.length,
            format_type=request.format_type,
            verbose=True
        )
        content = results["final"]
        quality = results.get("quality")
        
        # Veritabanına kaydet
        supabase = get_supabase()
        
        insert_result = supabase.table("contents").insert({
            "user_id": user_id,
            "topic": request.topic,
            "content": content,
        }).execute()
        
        if not insert_result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="İçerik kaydedilemedi"
            )
        
        saved = insert_result.data[0]
        
        return BlogResponse(
            id=saved["id"],
            topic=saved["topic"],
            content=saved["content"],
            created_at=saved["created_at"],
            quality=quality
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Blog oluşturma hatası: {str(e)}"
        )


@router.get("/history", response_model=BlogListResponse)
async def get_history(
    current_user: dict = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    """
    Kullanıcının blog geçmişini getirir.
    """
    
    user_id = current_user["id"]
    supabase = get_supabase()
    
    try:
        result = supabase.table("contents") \
            .select("*", count="exact") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        
        blogs = [
            BlogResponse(
                id=item["id"],
                topic=item["topic"],
                content=item["content"],
                created_at=item["created_at"]
            )
            for item in result.data
        ]
        
        return BlogListResponse(
            blogs=blogs,
            total=result.count or 0
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Geçmiş alınamadı: {str(e)}"
        )


@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(
    blog_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Tek bir blog yazısını getirir.
    """
    
    user_id = current_user["id"]
    supabase = get_supabase()
    
    try:
        result = supabase.table("contents") \
            .select("*") \
            .eq("id", blog_id) \
            .eq("user_id", user_id) \
            .single() \
            .execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog bulunamadı"
            )
        
        return BlogResponse(
            id=result.data["id"],
            topic=result.data["topic"],
            content=result.data["content"],
            created_at=result.data["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Blog alınamadı: {str(e)}"
        )


@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Blog yazısını siler.
    """
    
    user_id = current_user["id"]
    supabase = get_supabase()
    
    try:
        result = supabase.table("contents") \
            .delete() \
            .eq("id", blog_id) \
            .eq("user_id", user_id) \
            .execute()
        
        return {"message": "Blog silindi"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Silme hatası: {str(e)}"
        )


# ============================================================
# AGENT BİLGİLERİ
# ============================================================

@router.get("/agents")
async def get_agents():
    """
    Kullanılan agent'ların bilgilerini döndürür.
    """
    return {"agents": list(AGENTS.values())}


# ============================================================
# STREAMING BLOG OLUŞTURMA (SSE)
# ============================================================

@router.post("/create-stream")
async def create_blog_stream(
    request: BlogCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    SSE ile blog oluşturur. Her agent aşamasında event gönderir.
    """
    
    user_id = current_user["id"]
    
    # Limit kontrolü
    limit_exceeded, usage, limit = check_usage_limit(user_id)
    
    if limit_exceeded:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Aylık limit doldu ({usage}/{limit}). Pro plana geçin."
        )
    
    async def event_generator():
        """SSE event generator"""
        
        final_content = None
        final_quality = None
        
        try:
            for event in run_blog_pipeline_streaming(
                topic=request.topic,
                audience=request.audience,
                tone=request.tone,
                length=request.length,
                format_type=request.format_type
            ):
                # Event'i SSE formatına çevir
                event_data = json.dumps(event, ensure_ascii=False)
                yield f"data: {event_data}\n\n"
                
                # Final event'te içeriği kaydet
                if event["type"] == "final":
                    final_content = event["data"]["content"]
                    final_quality = event["data"]["quality"]
            
            # Veritabanına kaydet
            if final_content:
                supabase = get_supabase()
                
                insert_result = supabase.table("contents").insert({
                    "user_id": user_id,
                    "topic": request.topic,
                    "content": final_content,
                }).execute()
                
                if insert_result.data:
                    blog_data = insert_result.data[0]
                    
                    # Kaydedildi event'i
                    saved_event = {
                        "type": "saved",
                        "message": "Blog kaydedildi",
                        "data": {
                            "id": blog_data["id"],
                            "topic": request.topic,
                            "content": final_content,
                            "created_at": blog_data["created_at"],
                            "quality": final_quality
                        }
                    }
                    yield f"data: {json.dumps(saved_event, ensure_ascii=False)}\n\n"
        
        except Exception as e:
            error_event = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
