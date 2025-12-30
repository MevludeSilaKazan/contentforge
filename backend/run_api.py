#!/usr/bin/env python3
"""
ContentForge API Server
Kullanım: python run_api.py
"""

import uvicorn
import os
import sys

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def check_env():
    """Gerekli environment variable'ları kontrol et"""
    
    required = ["GROQ_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print("❌ Eksik environment variable'lar:")
        for var in missing:
            print(f"   - {var}")
        print("\n📌 .env dosyasını kontrol edin.")
        sys.exit(1)
    
    # Opsiyonel uyarılar
    if not os.getenv("SERPER_API_KEY"):
        print("⚠️  SERPER_API_KEY yok - Web araştırması devre dışı")
    
    print("✅ Environment kontrol tamam")


def main():
    """API sunucusunu başlat"""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║              ContentForge API Server                       ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    check_env()
    
    print("\n🚀 API başlatılıyor...")
    print("📍 http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("\n" + "=" * 50 + "\n")
    
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Geliştirme için auto-reload
    )


if __name__ == "__main__":
    main()
