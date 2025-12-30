"""
ContentForge Blog Agents - V10 Deep Research Edition
Gelişmiş çok katmanlı araştırma sistemi

Araştırma Katmanları:
1. 🌐 Genel Bilgi - Temel kavramlar ve tanımlar
2. 📊 İstatistik & Veri - Rakamlar, yüzdeler, trendler
3. 📰 Güncel Haberler - Son gelişmeler
4. 🎓 Uzman Görüşleri - Akademik ve profesyonel kaynaklar
5. 💼 Vaka Çalışmaları - Gerçek örnekler ve başarı hikayeleri
6. 🌍 Global Kaynaklar - İngilizce araştırma
7. ❓ SSS & Sorunlar - Sık sorulan sorular ve çözümler
"""

from groq import Groq
from typing import List, Dict, Optional, Generator, Any
import os
import re
import json
import requests
from datetime import datetime
from config.settings import DEFAULT_MODEL, SERPER_API_KEY


# ============================================================
# AGENT TANIMLARI
# ============================================================

AGENTS = {
    "researcher": {
        "id": "researcher",
        "name": "Araştırmacı",
        "name_en": "Deep Researcher",
        "avatar": "🔍",
        "color": "#3B82F6",
        "description": "7 katmanlı derinlemesine araştırma yapıyor",
        "tasks": ["Çoklu kaynak", "İstatistik toplama", "Global araştırma"]
    },
    "visual_curator": {
        "id": "visual_curator",
        "name": "Görsel Uzmanı",
        "name_en": "Visual Curator",
        "avatar": "🖼️",
        "color": "#8B5CF6",
        "description": "En uygun görselleri seçiyor",
        "tasks": ["Görsel arama", "Uygunluk kontrolü", "Lisans kontrolü"]
    },
    "writer": {
        "id": "writer",
        "name": "Yazar",
        "name_en": "Writer",
        "avatar": "✍️",
        "color": "#10B981",
        "description": "İçeriği oluşturuyor",
        "tasks": ["Yapı oluşturma", "İçerik yazma", "Örnekler ekleme"]
    },
    "editor": {
        "id": "editor",
        "name": "Editör",
        "name_en": "Editor",
        "avatar": "✨",
        "color": "#F59E0B",
        "description": "İçeriği düzenliyor ve iyileştiriyor",
        "tasks": ["Dil kontrolü", "SEO optimizasyonu", "Format düzenleme"]
    },
    "quality_analyst": {
        "id": "quality_analyst",
        "name": "Kalite Analisti",
        "name_en": "Quality Analyst",
        "avatar": "📊",
        "color": "#EF4444",
        "description": "Kalite skorlarını hesaplıyor",
        "tasks": ["Okunabilirlik", "SEO skoru", "Özgünlük analizi"]
    }
}


# ============================================================
# ARAŞTIRMA KATEGORİLERİ
# ============================================================

RESEARCH_CATEGORIES = {
    "general": {
        "icon": "🌐",
        "name": "Genel Bilgi",
        "description": "Temel kavramlar ve tanımlar",
        "priority": 1
    },
    "statistics": {
        "icon": "📊",
        "name": "İstatistik & Veri",
        "description": "Rakamlar, yüzdeler, pazar verileri",
        "priority": 2
    },
    "news": {
        "icon": "📰",
        "name": "Güncel Haberler",
        "description": "Son gelişmeler ve trendler",
        "priority": 3
    },
    "expert": {
        "icon": "🎓",
        "name": "Uzman Görüşleri",
        "description": "Akademik ve profesyonel kaynaklar",
        "priority": 4
    },
    "cases": {
        "icon": "💼",
        "name": "Vaka Çalışmaları",
        "description": "Gerçek örnekler ve başarı hikayeleri",
        "priority": 5
    },
    "global": {
        "icon": "🌍",
        "name": "Global Kaynaklar",
        "description": "Uluslararası araştırma",
        "priority": 6
    },
    "faq": {
        "icon": "❓",
        "name": "SSS & Sorunlar",
        "description": "Sık sorulan sorular",
        "priority": 7
    }
}


# ============================================================
# UNSPLASH API
# ============================================================

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

def search_images(query: str, count: int = 3) -> List[Dict]:
    if not UNSPLASH_ACCESS_KEY:
        return []
    
    try:
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "per_page": count, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        images = []
        for photo in data.get("results", []):
            images.append({
                "url": photo["urls"]["regular"],
                "thumb": photo["urls"]["thumb"],
                "alt": photo.get("alt_description", query),
                "credit": photo["user"]["name"],
                "credit_link": photo["user"]["links"]["html"]
            })
        return images
    except:
        return []


def get_images_for_topic(topic: str, sections: List[str] = None) -> Dict[str, Dict]:
    images = {}
    
    hero_images = search_images(topic, count=1)
    if hero_images:
        images["hero"] = hero_images[0]
    
    if sections:
        for section in sections[:5]:
            section_images = search_images(f"{section} {topic}", count=1)
            if section_images:
                images[section] = section_images[0]
    
    return images


# ============================================================
# GELİŞMİŞ WEB ARAMA SİSTEMİ
# ============================================================

def web_search(query: str, num_results: int = 10, language: str = "tr", 
               search_type: str = "search", time_range: str = None) -> List[Dict]:
    """
    Gelişmiş web arama fonksiyonu
    
    Args:
        query: Arama sorgusu
        num_results: Sonuç sayısı
        language: Dil (tr/en)
        search_type: Arama tipi (search/news)
        time_range: Zaman aralığı (d=gün, w=hafta, m=ay, y=yıl)
    """
    if not SERPER_API_KEY:
        return []
    
    try:
        # Endpoint belirleme
        endpoint = "https://google.serper.dev/search"
        if search_type == "news":
            endpoint = "https://google.serper.dev/news"
        
        # Request parametreleri
        params = {
            "q": query,
            "gl": "tr" if language == "tr" else "us",
            "hl": language,
            "num": num_results
        }
        
        # Zaman filtresi
        if time_range:
            params["tbs"] = f"qdr:{time_range}"
        
        response = requests.post(
            endpoint,
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json=params,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        # Organik sonuçlar
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "date": item.get("date", ""),
                "source": extract_domain(item.get("link", ""))
            })
        
        # News sonuçları
        for item in data.get("news", []):
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", ""),
                "date": item.get("date", ""),
                "source": item.get("source", "")
            })
        
        # Knowledge Graph
        if "knowledgeGraph" in data:
            kg = data["knowledgeGraph"]
            kg_result = {
                "title": kg.get("title", ""),
                "snippet": kg.get("description", ""),
                "link": kg.get("website", ""),
                "source": "Knowledge Graph",
                "is_kg": True,
                "attributes": kg.get("attributes", {})
            }
            results.insert(0, kg_result)
        
        # Answer Box
        if "answerBox" in data:
            ab = data["answerBox"]
            answer_result = {
                "title": ab.get("title", "Doğrudan Cevap"),
                "snippet": ab.get("answer", ab.get("snippet", "")),
                "link": ab.get("link", ""),
                "source": "Answer Box",
                "is_answer": True
            }
            results.insert(0, answer_result)
        
        # People Also Ask
        if "peopleAlsoAsk" in data:
            for paa in data["peopleAlsoAsk"][:3]:
                results.append({
                    "title": paa.get("question", ""),
                    "snippet": paa.get("snippet", ""),
                    "link": paa.get("link", ""),
                    "source": "İlgili Soru",
                    "is_question": True
                })
        
        return results
        
    except Exception as e:
        print(f"Arama hatası: {e}")
        return []


def extract_domain(url: str) -> str:
    """URL'den domain çıkarır"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain
    except:
        return ""


def extract_statistics(text: str) -> List[str]:
    """Metinden istatistikleri çıkarır"""
    stats = []
    
    # Yüzde kalıpları
    percentages = re.findall(r'%\s*\d+[\.,]?\d*|\d+[\.,]?\d*\s*%', text)
    stats.extend([f"📈 {p.strip()}" for p in percentages])
    
    # Büyük sayılar (milyon, milyar, trilyon)
    big_numbers = re.findall(r'\d+[\.,]?\d*\s*(milyon|milyar|trilyon|million|billion|trillion)', text, re.IGNORECASE)
    stats.extend([f"💰 {n[0]} {n[1]}" if isinstance(n, tuple) else f"💰 {n}" for n in big_numbers])
    
    # Para birimleri
    money = re.findall(r'[\$€₺]\s*\d+[\.,]?\d*\s*(milyon|milyar|bin|K|M|B)?', text, re.IGNORECASE)
    
    # Yıl bazlı veriler
    year_data = re.findall(r'20\d{2}\s*[-–]\s*20\d{2}|20\d{2}\s+yılında', text)
    stats.extend([f"📅 {y}" for y in year_data])
    
    return list(set(stats))[:10]  # Maksimum 10 istatistik


def extract_quotes(text: str) -> List[str]:
    """Metinden alıntıları çıkarır"""
    quotes = []
    
    # Tırnak içindeki metinler (çeşitli tırnak stilleri)
    # Standart çift tırnak
    quoted = re.findall(r'"([^"]{20,200})"', text)
    # Tek tırnak
    quoted += re.findall(r"'([^']{20,200})'", text)
    # Guillemet tırnaklar
    quoted += re.findall(r'«([^»]{20,200})»', text)
    
    for q in quoted[:5]:
        quotes.append(f'💬 "{q}"')
    
    return quotes


# ============================================================
# 7 KATMANLI ARAŞTIRMA SİSTEMİ
# ============================================================

def deep_research(topic: str, format_type: str = "standard") -> Dict[str, Any]:
    """
    7 katmanlı derinlemesine araştırma sistemi
    
    Returns:
        {
            "layers": {...},
            "statistics": [...],
            "quotes": [...],
            "sources_count": int,
            "compiled_research": str
        }
    """
    
    research_data = {
        "layers": {},
        "statistics": [],
        "quotes": [],
        "sources": [],
        "sources_count": 0
    }
    
    # ═══════════════════════════════════════════════════════
    # KATMAN 1: GENEL BİLGİ
    # ═══════════════════════════════════════════════════════
    
    general_queries = [
        f"{topic} nedir",
        f"{topic} tanımı ve önemi",
        f"{topic} temel kavramlar"
    ]
    
    layer_results = []
    for query in general_queries:
        results = web_search(query, num_results=5, language="tr")
        layer_results.extend(results)
    
    research_data["layers"]["general"] = {
        "category": RESEARCH_CATEGORIES["general"],
        "results": layer_results[:8],
        "query_count": len(general_queries)
    }
    
    # ═══════════════════════════════════════════════════════
    # KATMAN 2: İSTATİSTİK & VERİ
    # ═══════════════════════════════════════════════════════
    
    stats_queries = [
        f"{topic} istatistikleri 2024",
        f"{topic} pazar büyüklüğü",
        f"{topic} araştırma verileri",
        f"{topic} yüzde oran rakamlar"
    ]
    
    layer_results = []
    for query in stats_queries:
        results = web_search(query, num_results=5, language="tr")
        layer_results.extend(results)
        
        # İstatistik çıkarma
        for r in results:
            stats = extract_statistics(r.get("snippet", ""))
            research_data["statistics"].extend(stats)
    
    research_data["layers"]["statistics"] = {
        "category": RESEARCH_CATEGORIES["statistics"],
        "results": layer_results[:8],
        "query_count": len(stats_queries)
    }
    
    # ═══════════════════════════════════════════════════════
    # KATMAN 3: GÜNCEL HABERLER
    # ═══════════════════════════════════════════════════════
    
    news_queries = [
        f"{topic} son gelişmeler",
        f"{topic} 2024 haberleri"
    ]
    
    layer_results = []
    for query in news_queries:
        # Son 1 aylık haberler
        results = web_search(query, num_results=5, language="tr", search_type="news", time_range="m")
        layer_results.extend(results)
    
    research_data["layers"]["news"] = {
        "category": RESEARCH_CATEGORIES["news"],
        "results": layer_results[:6],
        "query_count": len(news_queries)
    }
    
    # ═══════════════════════════════════════════════════════
    # KATMAN 4: UZMAN GÖRÜŞLERİ
    # ═══════════════════════════════════════════════════════
    
    expert_queries = [
        f"{topic} uzman görüşü",
        f"{topic} profesyonel tavsiye",
        f'"{topic}" CEO açıklama'
    ]
    
    layer_results = []
    for query in expert_queries:
        results = web_search(query, num_results=5, language="tr")
        layer_results.extend(results)
        
        # Alıntı çıkarma
        for r in results:
            quotes = extract_quotes(r.get("snippet", ""))
            research_data["quotes"].extend(quotes)
    
    research_data["layers"]["expert"] = {
        "category": RESEARCH_CATEGORIES["expert"],
        "results": layer_results[:6],
        "query_count": len(expert_queries)
    }
    
    # ═══════════════════════════════════════════════════════
    # KATMAN 5: VAKA ÇALIŞMALARI
    # ═══════════════════════════════════════════════════════
    
    case_queries = [
        f"{topic} başarı hikayesi",
        f"{topic} örnek şirket",
        f"{topic} vaka çalışması case study"
    ]
    
    layer_results = []
    for query in case_queries:
        results = web_search(query, num_results=5, language="tr")
        layer_results.extend(results)
    
    research_data["layers"]["cases"] = {
        "category": RESEARCH_CATEGORIES["cases"],
        "results": layer_results[:6],
        "query_count": len(case_queries)
    }
    
    # ═══════════════════════════════════════════════════════
    # KATMAN 6: GLOBAL KAYNAKLAR (İNGİLİZCE)
    # ═══════════════════════════════════════════════════════
    
    # Türkçe konuyu İngilizceye çevir (basit yaklaşım)
    topic_en = topic  # İleride çeviri API eklenebilir
    
    global_queries = [
        f"{topic_en} statistics 2024",
        f"{topic_en} trends research",
        f"{topic_en} best practices"
    ]
    
    layer_results = []
    for query in global_queries:
        results = web_search(query, num_results=5, language="en")
        layer_results.extend(results)
        
        # İngilizce istatistikler
        for r in results:
            stats = extract_statistics(r.get("snippet", ""))
            research_data["statistics"].extend(stats)
    
    research_data["layers"]["global"] = {
        "category": RESEARCH_CATEGORIES["global"],
        "results": layer_results[:6],
        "query_count": len(global_queries)
    }
    
    # ═══════════════════════════════════════════════════════
    # KATMAN 7: SSS & SORUNLAR
    # ═══════════════════════════════════════════════════════
    
    faq_queries = [
        f"{topic} sık sorulan sorular",
        f"{topic} sorunları çözümleri",
        f"{topic} nasıl yapılır"
    ]
    
    layer_results = []
    for query in faq_queries:
        results = web_search(query, num_results=5, language="tr")
        layer_results.extend(results)
    
    research_data["layers"]["faq"] = {
        "category": RESEARCH_CATEGORIES["faq"],
        "results": layer_results[:6],
        "query_count": len(faq_queries)
    }
    
    # ═══════════════════════════════════════════════════════
    # FORMAT BAZLI EK ARAŞTIRMA
    # ═══════════════════════════════════════════════════════
    
    format_extra_queries = {
        "listicle": [f"{topic} en iyi yolları", f"{topic} ipuçları listesi"],
        "howto": [f"{topic} adım adım rehber", f"{topic} başlangıç kılavuzu"],
        "comparison": [f"{topic} karşılaştırma", f"{topic} alternatifleri vs"],
        "casestudy": [f"{topic} ROI sonuçlar", f"{topic} dönüşüm metrikleri"]
    }
    
    if format_type in format_extra_queries:
        extra_results = []
        for query in format_extra_queries[format_type]:
            results = web_search(query, num_results=5, language="tr")
            extra_results.extend(results)
        
        research_data["layers"]["format_specific"] = {
            "category": {"icon": "🎯", "name": f"{format_type.title()} Özel", "description": "Format bazlı araştırma"},
            "results": extra_results[:6],
            "query_count": len(format_extra_queries[format_type])
        }
    
    # ═══════════════════════════════════════════════════════
    # SONUÇLARI DERLİME
    # ═══════════════════════════════════════════════════════
    
    # Toplam kaynak sayısı
    total_sources = 0
    for layer_name, layer_data in research_data["layers"].items():
        total_sources += len(layer_data["results"])
        for result in layer_data["results"]:
            if result.get("source") and result["source"] not in research_data["sources"]:
                research_data["sources"].append(result["source"])
    
    research_data["sources_count"] = total_sources
    
    # İstatistikleri benzersizleştir
    research_data["statistics"] = list(set(research_data["statistics"]))[:15]
    
    # Alıntıları benzersizleştir
    research_data["quotes"] = list(set(research_data["quotes"]))[:8]
    
    # Derlenmiş araştırma metni oluştur
    research_data["compiled_research"] = compile_research_text(research_data)
    
    return research_data


def compile_research_text(research_data: Dict) -> str:
    """Araştırma verilerini derlenmiş metin haline getirir"""
    
    sections = []
    
    # Başlık
    sections.append("# 📚 DERİNLEMESİNE ARAŞTIRMA RAPORU\n")
    sections.append(f"**Toplam Kaynak:** {research_data['sources_count']} | **Benzersiz Site:** {len(research_data['sources'])}\n")
    
    # İstatistik özeti
    if research_data["statistics"]:
        sections.append("\n## 📊 BULUNAN İSTATİSTİKLER")
        for stat in research_data["statistics"][:10]:
            sections.append(f"- {stat}")
    
    # Alıntılar
    if research_data["quotes"]:
        sections.append("\n## 💬 UZMAN ALINTILARI")
        for quote in research_data["quotes"][:5]:
            sections.append(f"- {quote}")
    
    # Her katmandan bilgiler
    for layer_name, layer_data in research_data["layers"].items():
        category = layer_data["category"]
        results = layer_data["results"]
        
        if results:
            sections.append(f"\n## {category['icon']} {category['name'].upper()}")
            sections.append(f"*{category['description']}*\n")
            
            for r in results[:5]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                link = r.get("link", "")
                source = r.get("source", "")
                date = r.get("date", "")
                
                if title and snippet:
                    sections.append(f"**{title}**")
                    sections.append(f"{snippet}")
                    if date:
                        sections.append(f"📅 {date}")
                    if source:
                        sections.append(f"🔗 Kaynak: {source}")
                    if link:
                        sections.append(f"📎 {link}")
                    sections.append("")
    
    return "\n".join(sections)


# ============================================================
# ESKİ FONKSİYON - GERİYE UYUMLULUK
# ============================================================

def research_for_format(topic: str, format_type: str) -> str:
    """
    Geriye uyumlu araştırma fonksiyonu
    Yeni deep_research sistemini kullanır
    """
    research_data = deep_research(topic, format_type)
    return research_data["compiled_research"]


# ============================================================
# AYARLAR
# ============================================================

AUDIENCE_CONFIG = {
    "general": {"desc": "Genel okuyucu", "style": "Basit dil, günlük örnekler"},
    "professional": {"desc": "Profesyonel", "style": "Teknik terimler, derinlemesine analiz"},
    "entrepreneur": {"desc": "Girişimci", "style": "ROI odaklı, iş değeri vurgula"},
    "technical": {"desc": "Teknik uzman", "style": "Detaylı metodoloji, teknik derinlik"}
}

TONE_CONFIG = {
    "formal": "Resmi, akademik, profesyonel",
    "friendly": "Samimi, sıcak, sohbet havası",
    "educational": "Eğitici, adım adım, öğretici",
    "persuasive": "İkna edici, faydaları vurgula"
}

LENGTH_CONFIG = {
    "short": {"words": "800-1000", "sections": 4},
    "medium": {"words": "1500-1800", "sections": 6},
    "long": {"words": "2500-3000", "sections": 8}
}

FORMAT_CONFIG = {
    "standard": {"name": "Standart Blog", "description": "Klasik blog yazısı", "icon": "📝"},
    "listicle": {"name": "Listicle", "description": "\"10 Yol\" formatı", "icon": "📋"},
    "howto": {"name": "Nasıl Yapılır", "description": "Adım adım rehber", "icon": "🔧"},
    "comparison": {"name": "Karşılaştırma", "description": "X vs Y analizi", "icon": "⚖️"},
    "casestudy": {"name": "Vaka Çalışması", "description": "Detaylı analiz", "icon": "🔬"}
}


# ============================================================
# LLM ÇAĞRISI
# ============================================================

def call_llm(client: Groq, system: str, user: str, temp: float = 0.7) -> str:
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=temp,
        max_tokens=6000,
    )
    return response.choices[0].message.content


# ============================================================
# FORMAT YAZIM FONKSİYONLARI
# ============================================================

def _format_images(images: Dict) -> str:
    if not images:
        return "Görsel bulunamadı."
    
    lines = []
    for section, img in images.items():
        lines.append(f"- {section}: ![{img['alt']}]({img['url']})")
        lines.append(f"  Fotoğraf: {img['credit']}")
    return "\n".join(lines)


def _format_statistics(statistics: List[str]) -> str:
    """İstatistikleri prompt için formatlar"""
    if not statistics:
        return "İstatistik bulunamadı."
    return "\n".join([f"- {s}" for s in statistics[:10]])


def _format_quotes(quotes: List[str]) -> str:
    """Alıntıları prompt için formatlar"""
    if not quotes:
        return "Alıntı bulunamadı."
    return "\n".join([f"- {q}" for q in quotes[:5]])


def write_standard(client: Groq, topic: str, research: str, images: Dict,
                   audience: str, tone: str, length: str,
                   statistics: List[str] = None, quotes: List[str] = None) -> str:
    lng = LENGTH_CONFIG[length]
    aud = AUDIENCE_CONFIG[audience]
    image_md = _format_images(images)
    stats_md = _format_statistics(statistics or [])
    quotes_md = _format_quotes(quotes or [])
    
    system = f"""Sen profesyonel bir blog yazarısın. Araştırma verilerini kullanarak kapsamlı blog yazısı yaz.

HEDEF: {lng['words']} kelime, {lng['sections']} bölüm
TON: {TONE_CONFIG[tone]}
KİTLE: {aud['desc']} - {aud['style']}

KRİTİK KURALLAR:
1. Aşağıdaki istatistikleri MUTLAKA kullan ve kaynak göster
2. Uzman alıntılarını içeriğe entegre et
3. Her bölümde somut veri olsun
4. Güncel örnekler ve trendleri dahil et
5. SEO için anahtar kelimeleri doğal kullan

KULLANILACAK İSTATİSTİKLER:
{stats_md}

KULLANILACAK ALINTILAR:
{quotes_md}

GÖRSELLER:
{image_md}

Highlight kutuları, bilgi kutuları ve çağrı kutularını kullan."""

    user = f"""KONU: {topic}

ARAŞTIRMA VERİLERİ:
{research[:6000]}

Bu verileri kullanarak profesyonel, veri destekli blog yazısı yaz. Her iddiayı araştırma verileriyle destekle."""

    return call_llm(client, system, user, temp=0.6)


def write_listicle(client: Groq, topic: str, research: str, images: Dict,
                   audience: str, tone: str, length: str,
                   statistics: List[str] = None, quotes: List[str] = None) -> str:
    lng = LENGTH_CONFIG[length]
    list_count = {"short": 5, "medium": 7, "long": 10}[length]
    image_md = _format_images(images)
    stats_md = _format_statistics(statistics or [])
    
    system = f"""Sen listicle uzmanısın. "{list_count} Yol/Strateji/İpucu" formatında yaz.

HEDEF: {lng['words']} kelime, {list_count} madde
TON: {TONE_CONFIG[tone]}

HER MADDE İÇİN:
1. Dikkat çekici başlık (emoji ile)
2. 2-3 paragraf açıklama
3. Somut örnek veya istatistik (ZORUNLU)
4. Pro Tip kutusu

KULLANILACAK İSTATİSTİKLER:
{stats_md}

GÖRSELLER: {image_md}"""

    user = f"""KONU: {topic}

ARAŞTIRMA:
{research[:5000]}

Her maddede araştırmadan veri kullan."""

    return call_llm(client, system, user, temp=0.7)


def write_howto(client: Groq, topic: str, research: str, images: Dict,
                audience: str, tone: str, length: str,
                statistics: List[str] = None, quotes: List[str] = None) -> str:
    lng = LENGTH_CONFIG[length]
    step_count = {"short": 5, "medium": 7, "long": 10}[length]
    image_md = _format_images(images)
    
    system = f"""Sen teknik rehber yazarısın. Adım adım uygulama rehberi yaz.

HEDEF: {lng['words']} kelime, {step_count} adım

HER ADIM İÇİN:
- ⏱️ Tahmini süre
- 📊 Zorluk seviyesi (Kolay/Orta/Zor)
- Detaylı açıklama
- 💡 İpucu kutusu
- ⚠️ Uyarı kutusu (gerekirse)

EKSTRA BÖLÜMLER:
- Gereksinimler listesi (başta)
- Sık yapılan hatalar (sonda)
- Sorun giderme bölümü

GÖRSELLER: {image_md}"""

    user = f"""KONU: {topic}

ARAŞTIRMA:
{research[:5000]}

Pratik, uygulanabilir rehber yaz."""

    return call_llm(client, system, user, temp=0.5)


def write_comparison(client: Groq, topic: str, research: str, images: Dict,
                     audience: str, tone: str, length: str,
                     statistics: List[str] = None, quotes: List[str] = None) -> str:
    lng = LENGTH_CONFIG[length]
    image_md = _format_images(images)
    stats_md = _format_statistics(statistics or [])
    
    system = f"""Sen karşılaştırma analisti yazarısın. Detaylı X vs Y analizi yaz.

HEDEF: {lng['words']} kelime

YAPI:
1. Hızlı karşılaştırma tablosu (başta)
2. Her kriter için detaylı analiz
3. Yıldız derecelendirmesi (★★★★☆)
4. Artı/Eksi listeleri
5. Her kriterde kazanan belirt
6. Sonuç: Kim neyi seçmeli

KULLANILACAK VERİLER:
{stats_md}

GÖRSELLER: {image_md}"""

    user = f"""KONU: {topic}

ARAŞTIRMA:
{research[:5000]}

Objektif, veri destekli karşılaştırma yaz."""

    return call_llm(client, system, user, temp=0.5)


def write_casestudy(client: Groq, topic: str, research: str, images: Dict,
                    audience: str, tone: str, length: str,
                    statistics: List[str] = None, quotes: List[str] = None) -> str:
    lng = LENGTH_CONFIG[length]
    image_md = _format_images(images)
    stats_md = _format_statistics(statistics or [])
    quotes_md = _format_quotes(quotes or [])
    
    system = f"""Sen vaka analisti yazarısın. Detaylı vaka çalışması yaz.

HEDEF: {lng['words']} kelime

YAPI:
1. Özet metrikleri tablosu (Önce/Sonra)
2. Şirket/Kişi profili
3. Problem tanımı
4. Çözüm aşamaları (timeline)
5. Sonuçlar (rakamlarla)
6. Öğrenilen dersler
7. Uygulanabilir adımlar

KULLANILACAK VERİLER:
{stats_md}

KULLANILACAK ALINTILAR:
{quotes_md}

GÖRSELLER: {image_md}"""

    user = f"""KONU: {topic}

ARAŞTIRMA:
{research[:5000]}

Gerçekçi, veri destekli vaka çalışması yaz."""

    return call_llm(client, system, user, temp=0.6)


def run_final_editor(client: Groq, content: str, topic: str, format_type: str) -> str:
    format_info = FORMAT_CONFIG.get(format_type, FORMAT_CONFIG["standard"])
    
    system = f"""Sen baş editörsün. {format_info['name']} formatını son kez düzenle.

GÖREVLER:
1. Yazım ve dilbilgisi hatalarını düzelt
2. Cümle akışını iyileştir
3. SEO için başlıkları optimize et
4. Meta description yaz
5. Anahtar kelimeleri belirle

ÇIKTI BAŞINDA:
---
baslik: [SEO uyumlu başlık]
aciklama: [155 karakter meta description]
anahtar_kelimeler: [5-7 anahtar kelime]
okuma_suresi: [X dakika]
format: {format_type}
---

Ardından düzenlenmiş içerik."""

    user = f"""KONU: {topic}

İÇERİK:
{content}

Final düzenleme yap, SEO optimize et."""

    return call_llm(client, system, user, temp=0.2)


# ============================================================
# KALİTE HESAPLAMA
# ============================================================

def calculate_readability_score(content: str) -> Dict:
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = content.split()
    
    if not sentences or not words:
        return {"score": 50, "level": "Orta", "level_color": "yellow"}
    
    avg_sentence_length = len(words) / len(sentences)
    long_words = sum(1 for w in words if len(w) > 12)
    long_word_ratio = long_words / len(words) * 100
    paragraphs = content.split('\n\n')
    avg_para_length = len(words) / max(len(paragraphs), 1)
    
    score = 100
    if avg_sentence_length > 25: score -= 20
    elif avg_sentence_length > 20: score -= 10
    if long_word_ratio > 15: score -= 15
    elif long_word_ratio > 10: score -= 8
    if avg_para_length > 100: score -= 10
    
    score = max(0, min(100, score))
    
    if score >= 80: level, color = "Çok İyi", "green"
    elif score >= 60: level, color = "İyi", "blue"
    elif score >= 40: level, color = "Orta", "yellow"
    else: level, color = "Zor", "red"
    
    return {"score": score, "level": level, "level_color": color}


def calculate_seo_score(content: str, topic: str) -> Dict:
    score = 50
    topic_lower = topic.lower()
    content_lower = content.lower()
    
    keyword_count = content_lower.count(topic_lower)
    if keyword_count >= 5: score += 20
    elif keyword_count >= 3: score += 15
    elif keyword_count >= 1: score += 8
    
    if content_lower[:500].find(topic_lower) != -1: score += 10
    
    headers = re.findall(r'^#{1,3}\s+.+', content, re.MULTILINE)
    if len(headers) >= 5: score += 10
    elif len(headers) >= 3: score += 5
    
    if re.search(r'!\[.+\]\(.+\)', content): score += 10
    if re.search(r'\[.+\]\(.+\)', content): score += 5
    
    # Veri kullanımı bonusu
    if re.search(r'\d+%|\d+\s*(milyon|milyar)', content): score += 5
    
    score = max(0, min(100, score))
    
    if score >= 80: level, color = "Mükemmel", "green"
    elif score >= 60: level, color = "İyi", "blue"
    elif score >= 40: level, color = "Orta", "yellow"
    else: level, color = "Zayıf", "red"
    
    return {"score": score, "level": level, "level_color": color}


def calculate_fact_score(client: Groq, content: str, research: str) -> Dict:
    score = 60
    
    # Araştırma kullanımı
    if research and len(research) > 1000: score += 15
    elif research and len(research) > 500: score += 10
    
    # Veri kullanımı
    stats_count = len(re.findall(r'\d+%|\d+\s*(milyon|milyar|bin)', content))
    if stats_count >= 5: score += 15
    elif stats_count >= 3: score += 10
    elif stats_count >= 1: score += 5
    
    # Kaynak referansları
    if re.search(r'(araştırma|rapor|çalışma|anket)', content.lower()): score += 5
    
    # Alıntı kullanımı
    quote_count = len(re.findall(r'"[^"]{20,}"', content))
    if quote_count >= 2: score += 5
    
    score = min(100, score)
    
    if score >= 80: level, color = "Güvenilir", "green"
    elif score >= 60: level, color = "Kabul Edilebilir", "blue"
    else: level, color = "Dikkatli Olun", "yellow"
    
    return {"score": score, "level": level, "level_color": color}


def calculate_originality_score(client: Groq, content: str, topic: str) -> Dict:
    score = 70
    
    if re.search(r'örneğin|mesela', content.lower()): score += 10
    if re.search(r'kendi deneyim|tecrübe', content.lower()): score += 5
    if len(content.split()) > 0 and len(set(content.split())) / len(content.split()) > 0.6: score += 10
    
    # Özgün bakış açısı
    if re.search(r'bence|kanımca|görüşüme göre', content.lower()): score += 5
    
    score = min(100, score)
    
    if score >= 80: level, color = "Özgün", "green"
    elif score >= 60: level, color = "İyi", "blue"
    else: level, color = "Geliştirilebilir", "yellow"
    
    return {"score": score, "level": level, "level_color": color}


def calculate_overall_quality(readability, seo, fact, originality) -> Dict:
    avg = (readability["score"] + seo["score"] + fact["score"] + originality["score"]) / 4
    
    if avg >= 80: level, color, grade = "Mükemmel", "green", "A"
    elif avg >= 70: level, color, grade = "Çok İyi", "blue", "B+"
    elif avg >= 60: level, color, grade = "İyi", "blue", "B"
    elif avg >= 50: level, color, grade = "Orta", "yellow", "C"
    else: level, color, grade = "Geliştirilebilir", "red", "D"
    
    return {"score": round(avg), "level": level, "level_color": color, "grade": grade}


# ============================================================
# STREAMING PIPELINE
# ============================================================

def run_blog_pipeline_streaming(
    topic: str,
    audience: str = "general",
    tone: str = "friendly",
    length: str = "medium",
    format_type: str = "standard"
) -> Generator[Dict[str, Any], None, None]:
    """
    Streaming blog pipeline - Her aşamada event döndürür
    """
    
    client = Groq()
    format_info = FORMAT_CONFIG.get(format_type, FORMAT_CONFIG["standard"])
    
    results = {
        "topic": topic,
        "format": format_type,
        "research": "",
        "research_data": None,
        "images": {},
        "draft": "",
        "final": "",
        "quality": None,
    }
    
    total_steps = 5
    
    # ═══════════════════════════════════════════════════════
    # AGENT 1: DERİN ARAŞTIRMACI
    # ═══════════════════════════════════════════════════════
    
    yield {
        "type": "agent_start",
        "agent": AGENTS["researcher"],
        "step": 1,
        "total_steps": total_steps,
        "message": "7 katmanlı derin araştırma başlatılıyor..."
    }
    
    if SERPER_API_KEY:
        research_data = deep_research(topic, format_type)
        results["research"] = research_data["compiled_research"]
        results["research_data"] = research_data
        
        yield {
            "type": "agent_complete",
            "agent": AGENTS["researcher"],
            "step": 1,
            "total_steps": total_steps,
            "message": f"{research_data['sources_count']} kaynak, {len(research_data['statistics'])} istatistik bulundu",
            "data": {
                "sources_found": research_data["sources_count"],
                "statistics_count": len(research_data["statistics"]),
                "quotes_count": len(research_data["quotes"]),
                "layers": list(research_data["layers"].keys())
            }
        }
    else:
        yield {
            "type": "agent_complete",
            "agent": AGENTS["researcher"],
            "step": 1,
            "total_steps": total_steps,
            "message": "Araştırma atlandı (API key yok)",
            "data": {"sources_found": 0}
        }
    
    # ═══════════════════════════════════════════════════════
    # AGENT 2: GÖRSEL UZMANI
    # ═══════════════════════════════════════════════════════
    
    yield {
        "type": "agent_start",
        "agent": AGENTS["visual_curator"],
        "step": 2,
        "total_steps": total_steps,
        "message": "Görseller aranıyor..."
    }
    
    if UNSPLASH_ACCESS_KEY:
        results["images"] = get_images_for_topic(topic, [topic])
        yield {
            "type": "agent_complete",
            "agent": AGENTS["visual_curator"],
            "step": 2,
            "total_steps": total_steps,
            "message": f"{len(results['images'])} görsel bulundu",
            "data": {"images_found": len(results["images"])}
        }
    else:
        yield {
            "type": "agent_complete",
            "agent": AGENTS["visual_curator"],
            "step": 2,
            "total_steps": total_steps,
            "message": "Görsel arama atlandı",
            "data": {"images_found": 0}
        }
    
    # ═══════════════════════════════════════════════════════
    # AGENT 3: YAZAR
    # ═══════════════════════════════════════════════════════
    
    yield {
        "type": "agent_start",
        "agent": AGENTS["writer"],
        "step": 3,
        "total_steps": total_steps,
        "message": f"{format_info['name']} formatında veri destekli yazılıyor..."
    }
    
    format_writers = {
        "standard": write_standard,
        "listicle": write_listicle,
        "howto": write_howto,
        "comparison": write_comparison,
        "casestudy": write_casestudy,
    }
    
    # İstatistik ve alıntıları al
    statistics = []
    quotes = []
    if results["research_data"]:
        statistics = results["research_data"].get("statistics", [])
        quotes = results["research_data"].get("quotes", [])
    
    writer_func = format_writers.get(format_type, write_standard)
    results["draft"] = writer_func(
        client, topic, results["research"], results["images"],
        audience, tone, length, statistics, quotes
    )
    
    word_count = len(results["draft"].split())
    
    yield {
        "type": "agent_complete",
        "agent": AGENTS["writer"],
        "step": 3,
        "total_steps": total_steps,
        "message": f"Taslak hazır ({word_count} kelime)",
        "data": {"word_count": word_count}
    }
    
    # ═══════════════════════════════════════════════════════
    # AGENT 4: EDITÖR
    # ═══════════════════════════════════════════════════════
    
    yield {
        "type": "agent_start",
        "agent": AGENTS["editor"],
        "step": 4,
        "total_steps": total_steps,
        "message": "Final düzenleme ve SEO optimizasyonu yapılıyor..."
    }
    
    results["final"] = run_final_editor(client, results["draft"], topic, format_type)
    
    yield {
        "type": "agent_complete",
        "agent": AGENTS["editor"],
        "step": 4,
        "total_steps": total_steps,
        "message": "Düzenleme tamamlandı",
        "data": {}
    }
    
    # ═══════════════════════════════════════════════════════
    # AGENT 5: KALİTE ANALİSTİ
    # ═══════════════════════════════════════════════════════
    
    yield {
        "type": "agent_start",
        "agent": AGENTS["quality_analyst"],
        "step": 5,
        "total_steps": total_steps,
        "message": "Kalite analizi yapılıyor..."
    }
    
    readability = calculate_readability_score(results["final"])
    seo = calculate_seo_score(results["final"], topic)
    fact = calculate_fact_score(client, results["final"], results["research"])
    originality = calculate_originality_score(client, results["final"], topic)
    overall = calculate_overall_quality(readability, seo, fact, originality)
    
    results["quality"] = {
        "overall": overall,
        "readability": readability,
        "seo": seo,
        "fact_check": fact,
        "originality": originality
    }
    
    yield {
        "type": "agent_complete",
        "agent": AGENTS["quality_analyst"],
        "step": 5,
        "total_steps": total_steps,
        "message": f"Kalite skoru: {overall['score']}/100 ({overall['grade']})",
        "data": {"quality": results["quality"]}
    }
    
    # ═══════════════════════════════════════════════════════
    # FINAL
    # ═══════════════════════════════════════════════════════
    
    yield {
        "type": "final",
        "message": "Blog tamamlandı!",
        "data": {
            "content": results["final"],
            "quality": results["quality"],
            "format": format_type,
            "word_count": len(results["final"].split()),
            "research_stats": {
                "sources": results["research_data"]["sources_count"] if results["research_data"] else 0,
                "statistics": len(results["research_data"]["statistics"]) if results["research_data"] else 0,
                "quotes": len(results["research_data"]["quotes"]) if results["research_data"] else 0
            }
        }
    }


# ============================================================
# NORMAL PIPELINE
# ============================================================

def run_blog_pipeline(
    topic: str,
    audience: str = "general",
    tone: str = "friendly",
    length: str = "medium",
    format_type: str = "standard",
    verbose: bool = True
) -> dict:
    """Normal (non-streaming) pipeline"""
    
    result = None
    for event in run_blog_pipeline_streaming(topic, audience, tone, length, format_type):
        if verbose:
            if event["type"] == "agent_start":
                print(f"\n{event['agent']['avatar']} {event['agent']['name']}: {event['message']}")
            elif event["type"] == "agent_complete":
                print(f"   ✓ {event['message']}")
        
        if event["type"] == "final":
            result = {
                "topic": topic,
                "format": format_type,
                "final": event["data"]["content"],
                "quality": event["data"]["quality"]
            }
    
    return result


def get_agents_info() -> Dict:
    """Agent bilgilerini döndür"""
    return AGENTS


def save_blog(content: str, topic: str) -> str:
    safe_topic = "".join(c if c.isalnum() or c in (' ', '-') else '' for c in topic)
    safe_topic = safe_topic.replace(' ', '-').lower()[:40]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/{safe_topic}_{timestamp}.md"
    
    os.makedirs("outputs", exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filename
