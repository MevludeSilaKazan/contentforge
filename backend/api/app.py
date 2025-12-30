"""
ContentForge API
FastAPI uygulaması
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth_router, blog_router, user_router

# ============================================================
# APP OLUŞTUR
# ============================================================

app = FastAPI(
    title="ContentForge API",
    description="AI-Powered Türkçe İçerik Üretim Platformu",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
)


# ============================================================
# CORS (Frontend erişimi için)
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Next.js dev
        "http://localhost:5173",      # Vite dev
        "https://contentforge-frontend-ezis.onrender.com",   # Production (sonra güncelle)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(auth_router, prefix="/api")
app.include_router(blog_router, prefix="/api")
app.include_router(user_router, prefix="/api")


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "ContentForge API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
