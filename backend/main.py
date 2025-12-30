#!/usr/bin/env python3
"""
ContentForge - AI-Powered Türkçe İçerik Üretim Platformu
Kullanım: python main.py "blog konusu"

Groq API ile ücretsiz çalışır.
"""

import sys
import os
import time

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from agents.blog_agents import run_blog_pipeline, save_blog

# ASCII Banner
BANNER = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      ██████╗ ██████╗ ███╗   ██╗████████╗███████╗███╗   ██╗║
║     ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝████╗  ██║║
║     ██║     ██║   ██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║║
║     ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║║
║     ╚██████╗╚██████╔╝██║ ╚████║   ██║   ███████╗██║ ╚████║║
║      ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝║
║                                                           ║
║               ████████╗ ██████╗ ██████╗  ██████╗ ███████╗ ║
║               ██╔═════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝ ║
║               █████╗   ██║   ██║██████╔╝██║  ███╗█████╗   ║
║               ██╔══╝   ██║   ██║██╔══██╗██║   ██║██╔══╝   ║
║               ██║      ╚██████╔╝██║  ██║╚██████╔╝███████╗ ║
║               ╚═╝       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ║
║                                                           ║
║           AI-Powered Türkçe İçerik Üretim Platformu       ║
║                    ⚡ Powered by Groq                      ║
╚═══════════════════════════════════════════════════════════╝
"""


def create_blog(topic: str) -> str:
    """
    Verilen konu için blog yazısı oluşturur.
    
    Args:
        topic: Blog konusu
    
    Returns:
        Kaydedilen dosya yolu
    """
    
    print(f"\n🚀 Blog oluşturuluyor: '{topic}'")
    print("=" * 55)
    
    start_time = time.time()
    
    # Pipeline'ı çalıştır
    results = run_blog_pipeline(topic, verbose=True)
    
    # Dosyaya kaydet
    filepath = save_blog(results["final"], topic)
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 55)
    print(f"✨ Tamamlandı! ({elapsed:.1f} saniye)")
    print(f"📄 Dosya: {filepath}")
    
    # İçeriğin bir kısmını göster
    print("\n" + "-" * 55)
    print("📖 Önizleme:")
    print("-" * 55)
    preview = results["final"][:500] + "..." if len(results["final"]) > 500 else results["final"]
    print(preview)
    
    return filepath


def interactive_mode():
    """İnteraktif mod - kullanıcıdan konu alır"""
    
    print(BANNER)
    print("\n💡 İpucu: Çıkmak için 'q' veya 'çık' yazın")
    print("📊 Model: Llama 3.3 70B (Groq - Ücretsiz)")
    
    # Web search durumu
    if os.getenv("SERPER_API_KEY"):
        print("🌐 Web Araştırması: Aktif ✓")
    else:
        print("🌐 Web Araştırması: Devre dışı (SERPER_API_KEY ekle)")
    
    print("")
    
    while True:
        try:
            topic = input("📝 Blog konusu girin: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Görüşmek üzere!")
            break
        
        if topic.lower() in ['q', 'quit', 'çık', 'exit', 'kapat']:
            print("\n👋 Görüşmek üzere!")
            break
        
        if not topic:
            print("⚠️  Lütfen bir konu girin.\n")
            continue
        
        try:
            create_blog(topic)
            print("\n")
        except Exception as e:
            print(f"\n❌ Hata oluştu: {e}")
            print("💡 API anahtarınızı kontrol edin.\n")


def main():
    """Ana fonksiyon"""
    
    # API key kontrolü
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Hata: GROQ_API_KEY bulunamadı!")
        print("")
        print("📌 Çözüm:")
        print("   1. https://console.groq.com/keys adresinden ücretsiz key al")
        print("   2. .env dosyası oluştur:")
        print("      cp .env.example .env")
        print("   3. .env dosyasına key'i ekle:")
        print("      GROQ_API_KEY=gsk_xxxxx...")
        print("")
        sys.exit(1)
    
    # Komut satırı argümanları
    if len(sys.argv) > 1:
        # Direkt konu verilmiş
        topic = " ".join(sys.argv[1:])
        create_blog(topic)
    else:
        # İnteraktif mod
        interactive_mode()


if __name__ == "__main__":
    main()
