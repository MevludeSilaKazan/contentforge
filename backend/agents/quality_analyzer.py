"""
ContentForge Quality Analyzer
İçerik kalitesi analiz sistemi

Skorlar:
1. Readability Score - Okunabilirlik
2. SEO Score - Arama motoru optimizasyonu
3. Fact Check Score - İddia doğrulama
4. Originality Score - Özgünlük
"""

import re
import math
from typing import Dict, List, Tuple
from groq import Groq
import requests
from config.settings import DEFAULT_MODEL, SERPER_API_KEY


# ============================================================
# READABILITY SCORE - OKUNABİLİRLİK ANALİZİ
# ============================================================

def calculate_readability(content: str) -> Dict:
    """
    Türkçe içerik için okunabilirlik analizi
    
    Metrikler:
    - Ortalama cümle uzunluğu (ideal: 15-20 kelime)
    - Ortalama kelime uzunluğu (ideal: 5-7 harf)
    - Paragraf uzunluğu (ideal: 3-5 cümle)
    - Karmaşık kelime oranı (3+ hece)
    """
    
    # Markdown ve özel karakterleri temizle
    clean_text = re.sub(r'[#*>`\[\]()|\-]', '', content)
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', clean_text)  # Görselleri kaldır
    clean_text = re.sub(r'https?://\S+', '', clean_text)  # Linkleri kaldır
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Cümleleri ayır
    sentences = re.split(r'[.!?]+', clean_text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    if not sentences:
        return {"score": 0, "grade": "N/A", "details": {}}
    
    # Kelimeleri say
    words = clean_text.split()
    total_words = len(words)
    total_sentences = len(sentences)
    
    # Paragrafları say (çift newline ile ayrılmış)
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 20]
    total_paragraphs = max(len(paragraphs), 1)
    
    # Metrikler
    avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
    avg_word_length = sum(len(w) for w in words) / total_words if total_words > 0 else 0
    avg_paragraph_sentences = total_sentences / total_paragraphs
    
    # Karmaşık kelimeler (3+ hece - Türkçe için basit tahmin: 7+ harf)
    complex_words = [w for w in words if len(w) >= 7]
    complex_word_ratio = len(complex_words) / total_words if total_words > 0 else 0
    
    # Skor hesaplama (0-100)
    score = 100
    issues = []
    suggestions = []
    
    # Cümle uzunluğu değerlendirmesi
    if avg_sentence_length > 25:
        penalty = min((avg_sentence_length - 25) * 2, 20)
        score -= penalty
        issues.append(f"Cümleler çok uzun (ort. {avg_sentence_length:.1f} kelime)")
        suggestions.append("Cümleleri 15-20 kelimeye kısaltın")
    elif avg_sentence_length < 10:
        penalty = min((10 - avg_sentence_length) * 2, 15)
        score -= penalty
        issues.append(f"Cümleler çok kısa (ort. {avg_sentence_length:.1f} kelime)")
        suggestions.append("Cümleleri biraz genişletin")
    
    # Kelime uzunluğu değerlendirmesi
    if avg_word_length > 8:
        penalty = min((avg_word_length - 8) * 3, 15)
        score -= penalty
        issues.append("Çok fazla uzun/teknik kelime")
        suggestions.append("Daha basit kelimeler kullanın")
    
    # Karmaşık kelime oranı
    if complex_word_ratio > 0.3:
        penalty = min((complex_word_ratio - 0.3) * 50, 20)
        score -= penalty
        issues.append(f"Karmaşık kelime oranı yüksek (%{complex_word_ratio*100:.0f})")
        suggestions.append("Daha anlaşılır kelimeler tercih edin")
    
    # Paragraf uzunluğu
    if avg_paragraph_sentences > 6:
        score -= 10
        issues.append("Paragraflar çok uzun")
        suggestions.append("Paragrafları 3-5 cümleye bölün")
    
    # Skor sınırlandırma
    score = max(0, min(100, score))
    
    # Grade belirleme
    if score >= 80:
        grade = "A"
        grade_text = "Çok Kolay"
    elif score >= 65:
        grade = "B"
        grade_text = "Kolay"
    elif score >= 50:
        grade = "C"
        grade_text = "Orta"
    elif score >= 35:
        grade = "D"
        grade_text = "Zor"
    else:
        grade = "F"
        grade_text = "Çok Zor"
    
    return {
        "score": round(score),
        "grade": grade,
        "grade_text": grade_text,
        "details": {
            "total_words": total_words,
            "total_sentences": total_sentences,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_word_length": round(avg_word_length, 1),
            "complex_word_ratio": round(complex_word_ratio * 100, 1),
        },
        "issues": issues,
        "suggestions": suggestions
    }


# ============================================================
# SEO SCORE - ARAMA MOTORU OPTİMİZASYONU
# ============================================================

def calculate_seo_score(content: str, topic: str) -> Dict:
    """
    SEO kalite analizi
    
    Kontroller:
    - Başlık uzunluğu ve anahtar kelime
    - Meta açıklama
    - Başlık hiyerarşisi (H1, H2, H3)
    - Anahtar kelime yoğunluğu
    - Görsel alt text
    - İç/dış linkler
    - İçerik uzunluğu
    """
    
    score = 100
    checks = []
    issues = []
    suggestions = []
    
    # Anahtar kelimeleri çıkar (topic'ten)
    keywords = [w.lower() for w in topic.split() if len(w) > 2]
    content_lower = content.lower()
    
    # 1. Başlık kontrolü (H1)
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        h1_title = h1_match.group(1)
        h1_length = len(h1_title)
        
        if 30 <= h1_length <= 60:
            checks.append(("✅", "Başlık uzunluğu ideal", f"{h1_length} karakter"))
        elif h1_length < 30:
            score -= 10
            checks.append(("⚠️", "Başlık çok kısa", f"{h1_length} karakter"))
            suggestions.append("Başlığı 30-60 karakter arasına getirin")
        else:
            score -= 10
            checks.append(("⚠️", "Başlık çok uzun", f"{h1_length} karakter"))
            suggestions.append("Başlığı 60 karakterin altına indirin")
        
        # Anahtar kelime başlıkta mı?
        keyword_in_title = any(kw in h1_title.lower() for kw in keywords)
        if keyword_in_title:
            checks.append(("✅", "Anahtar kelime başlıkta var", ""))
        else:
            score -= 15
            checks.append(("❌", "Anahtar kelime başlıkta yok", ""))
            suggestions.append(f"'{topic}' ifadesini başlığa ekleyin")
    else:
        score -= 20
        checks.append(("❌", "H1 başlık bulunamadı", ""))
        issues.append("Ana başlık (H1) eksik")
    
    # 2. Meta açıklama (YAML frontmatter'dan)
    meta_match = re.search(r'aciklama:\s*(.+)', content)
    if meta_match:
        meta_desc = meta_match.group(1)
        meta_length = len(meta_desc)
        
        if 120 <= meta_length <= 160:
            checks.append(("✅", "Meta açıklama ideal", f"{meta_length} karakter"))
        elif meta_length < 120:
            score -= 10
            checks.append(("⚠️", "Meta açıklama kısa", f"{meta_length} karakter"))
        else:
            score -= 5
            checks.append(("⚠️", "Meta açıklama uzun", f"{meta_length} karakter"))
    else:
        score -= 15
        checks.append(("❌", "Meta açıklama yok", ""))
        suggestions.append("150 karakterlik meta açıklama ekleyin")
    
    # 3. Başlık hiyerarşisi
    h2_count = len(re.findall(r'^##\s+', content, re.MULTILINE))
    h3_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
    
    if h2_count >= 3:
        checks.append(("✅", f"{h2_count} alt başlık (H2)", ""))
    else:
        score -= 10
        checks.append(("⚠️", f"Sadece {h2_count} alt başlık", ""))
        suggestions.append("En az 3-4 alt başlık ekleyin")
    
    if h3_count >= 2:
        checks.append(("✅", f"{h3_count} alt-alt başlık (H3)", ""))
    
    # 4. Anahtar kelime yoğunluğu
    word_count = len(content.split())
    keyword_count = sum(content_lower.count(kw) for kw in keywords)
    keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0
    
    if 1 <= keyword_density <= 3:
        checks.append(("✅", f"Anahtar kelime yoğunluğu ideal", f"%{keyword_density:.1f}"))
    elif keyword_density < 1:
        score -= 10
        checks.append(("⚠️", "Anahtar kelime az kullanılmış", f"%{keyword_density:.1f}"))
        suggestions.append(f"'{topic}' ifadesini daha sık kullanın")
    else:
        score -= 10
        checks.append(("⚠️", "Anahtar kelime fazla kullanılmış", f"%{keyword_density:.1f}"))
    
    # 5. Görsel kontrolü
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    if images:
        checks.append(("✅", f"{len(images)} görsel mevcut", ""))
        
        # Alt text kontrolü
        images_with_alt = [img for img in images if img[0].strip()]
        if len(images_with_alt) == len(images):
            checks.append(("✅", "Tüm görsellerde alt text var", ""))
        else:
            score -= 5
            checks.append(("⚠️", "Bazı görsellerde alt text yok", ""))
    else:
        score -= 10
        checks.append(("⚠️", "Görsel yok", ""))
        suggestions.append("En az 1-2 görsel ekleyin")
    
    # 6. Link kontrolü
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    external_links = [l for l in links if l[1].startswith('http')]
    
    if external_links:
        checks.append(("✅", f"{len(external_links)} dış link", ""))
    else:
        score -= 5
        checks.append(("⚠️", "Dış link yok", ""))
    
    # 7. İçerik uzunluğu
    if word_count >= 1500:
        checks.append(("✅", f"İçerik uzunluğu ideal", f"{word_count} kelime"))
    elif word_count >= 800:
        checks.append(("⚠️", f"İçerik biraz kısa", f"{word_count} kelime"))
        score -= 5
    else:
        checks.append(("❌", f"İçerik çok kısa", f"{word_count} kelime"))
        score -= 15
        suggestions.append("En az 1000 kelimelik içerik hedefleyin")
    
    # Skor sınırlandırma
    score = max(0, min(100, score))
    
    # Grade belirleme
    if score >= 80:
        grade = "A"
    elif score >= 65:
        grade = "B"
    elif score >= 50:
        grade = "C"
    elif score >= 35:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "score": round(score),
        "grade": grade,
        "checks": checks,
        "issues": issues,
        "suggestions": suggestions,
        "details": {
            "word_count": word_count,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "image_count": len(images),
            "link_count": len(external_links),
            "keyword_density": round(keyword_density, 1)
        }
    }


# ============================================================
# FACT CHECK SCORE - İDDİA DOĞRULAMA
# ============================================================

def extract_claims(client: Groq, content: str) -> List[str]:
    """İçerikten doğrulanabilir iddiaları çıkar"""
    
    system = """İçerikten DOĞRULANABILIR iddiaları çıkar. Sadece:
- İstatistikler ve rakamlar
- Tarihsel olaylar
- Şirket/kişi hakkında somut bilgiler
- Araştırma sonuçları

Her satıra bir iddia yaz. Maksimum 5 iddia.
Genel görüşleri veya öznel ifadeleri ALMA."""

    user = f"İçerik:\n{content[:3000]}"
    
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            temperature=0.2,
            max_tokens=500,
        )
        
        claims = response.choices[0].message.content.strip().split('\n')
        claims = [c.strip('- ').strip() for c in claims if c.strip() and len(c.strip()) > 10]
        return claims[:5]
    except:
        return []


def verify_claim(claim: str) -> Dict:
    """Bir iddiayı web aramasıyla doğrula"""
    
    if not SERPER_API_KEY:
        return {"verified": None, "confidence": 0, "source": None}
    
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": claim, "gl": "tr", "hl": "tr", "num": 3},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        results = data.get("organic", [])
        if not results:
            return {"verified": None, "confidence": 0, "source": None}
        
        # Basit eşleşme kontrolü
        claim_words = set(claim.lower().split())
        best_match = 0
        best_source = None
        
        for r in results:
            snippet = r.get("snippet", "").lower()
            snippet_words = set(snippet.split())
            
            # Ortak kelime oranı
            common = len(claim_words & snippet_words)
            match_ratio = common / len(claim_words) if claim_words else 0
            
            if match_ratio > best_match:
                best_match = match_ratio
                best_source = r.get("link", "")
        
        if best_match > 0.5:
            return {"verified": True, "confidence": round(best_match * 100), "source": best_source}
        elif best_match > 0.3:
            return {"verified": None, "confidence": round(best_match * 100), "source": best_source}
        else:
            return {"verified": False, "confidence": round(best_match * 100), "source": None}
    
    except:
        return {"verified": None, "confidence": 0, "source": None}


def calculate_fact_check_score(client: Groq, content: str) -> Dict:
    """
    Fact-check analizi
    
    1. İçerikten iddiaları çıkar
    2. Her iddiayı web'de ara
    3. Doğrulama skoru hesapla
    """
    
    # İddiaları çıkar
    claims = extract_claims(client, content)
    
    if not claims:
        return {
            "score": 85,  # İddia yoksa varsayılan skor
            "grade": "B",
            "claims_checked": 0,
            "verified": 0,
            "unverified": 0,
            "uncertain": 0,
            "details": [],
            "note": "Doğrulanabilir somut iddia bulunamadı"
        }
    
    # Her iddiayı doğrula
    results = []
    verified = 0
    unverified = 0
    uncertain = 0
    
    for claim in claims:
        result = verify_claim(claim)
        results.append({
            "claim": claim[:100],
            "verified": result["verified"],
            "confidence": result["confidence"],
            "source": result["source"]
        })
        
        if result["verified"] is True:
            verified += 1
        elif result["verified"] is False:
            unverified += 1
        else:
            uncertain += 1
    
    # Skor hesaplama
    total = len(claims)
    if total > 0:
        score = ((verified * 100) + (uncertain * 60) + (unverified * 20)) / total
    else:
        score = 85
    
    score = max(0, min(100, round(score)))
    
    # Grade
    if score >= 80:
        grade = "A"
    elif score >= 65:
        grade = "B"
    elif score >= 50:
        grade = "C"
    elif score >= 35:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "score": score,
        "grade": grade,
        "claims_checked": total,
        "verified": verified,
        "unverified": unverified,
        "uncertain": uncertain,
        "details": results
    }


# ============================================================
# ORIGINALITY SCORE - ÖZGÜNLÜK ANALİZİ
# ============================================================

def calculate_originality_score(content: str) -> Dict:
    """
    Özgünlük analizi (basit versiyon)
    
    - Cümle benzersizliği kontrolü
    - Klişe/kalıp ifade tespiti
    - Özgün ifade oranı
    """
    
    # Yaygın klişeler
    cliches = [
        "günümüzde", "modern dünyada", "hızla değişen",
        "önemli bir rol", "büyük bir öneme sahip",
        "son yıllarda", "giderek artan", "vazgeçilmez",
        "kritik öneme sahip", "hayati önem", "dijital çağda",
        "bir adım önde", "fark yaratmak", "başarının anahtarı",
        "sonuç olarak", "özetle", "tüm bunlar gösteriyor ki"
    ]
    
    # Markdown temizle
    clean_text = re.sub(r'[#*>`\[\]()|\-]', '', content)
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', clean_text)
    clean_text = re.sub(r'https?://\S+', '', clean_text)
    clean_text = clean_text.lower()
    
    # Klişe sayısı
    cliche_count = 0
    found_cliches = []
    for cliche in cliches:
        count = clean_text.count(cliche)
        if count > 0:
            cliche_count += count
            found_cliches.append(cliche)
    
    # Cümleleri kontrol et
    sentences = re.split(r'[.!?]+', clean_text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    total_sentences = len(sentences)
    
    # Benzersiz cümle oranı (tekrar eden cümleler)
    unique_sentences = len(set(sentences))
    uniqueness_ratio = unique_sentences / total_sentences if total_sentences > 0 else 1
    
    # Skor hesaplama
    score = 100
    issues = []
    suggestions = []
    
    # Klişe cezası
    word_count = len(clean_text.split())
    cliche_ratio = cliche_count / (word_count / 100) if word_count > 0 else 0
    
    if cliche_ratio > 3:
        penalty = min(cliche_ratio * 5, 30)
        score -= penalty
        issues.append(f"{cliche_count} klişe ifade bulundu")
        suggestions.append(f"Şu ifadeleri değiştirin: {', '.join(found_cliches[:3])}")
    elif cliche_ratio > 1.5:
        score -= 10
        issues.append(f"{cliche_count} klişe ifade var")
    
    # Tekrar cezası
    if uniqueness_ratio < 0.9:
        penalty = (1 - uniqueness_ratio) * 50
        score -= penalty
        issues.append("Tekrar eden cümleler var")
        suggestions.append("Benzer cümleleri farklı şekilde ifade edin")
    
    score = max(0, min(100, round(score)))
    
    # Grade
    if score >= 85:
        grade = "A"
        grade_text = "Yüksek Özgünlük"
    elif score >= 70:
        grade = "B"
        grade_text = "İyi Özgünlük"
    elif score >= 55:
        grade = "C"
        grade_text = "Orta Özgünlük"
    elif score >= 40:
        grade = "D"
        grade_text = "Düşük Özgünlük"
    else:
        grade = "F"
        grade_text = "Çok Düşük"
    
    return {
        "score": score,
        "grade": grade,
        "grade_text": grade_text,
        "details": {
            "cliche_count": cliche_count,
            "found_cliches": found_cliches[:5],
            "unique_sentence_ratio": round(uniqueness_ratio * 100, 1)
        },
        "issues": issues,
        "suggestions": suggestions
    }


# ============================================================
# ANA ANALİZ FONKSİYONU
# ============================================================

def analyze_content_quality(content: str, topic: str, deep_check: bool = True) -> Dict:
    """
    Tüm kalite metriklerini hesapla
    
    Args:
        content: Blog içeriği
        topic: Blog konusu
        deep_check: Fact-check yapılsın mı (API kullanır)
    
    Returns:
        Tüm skorları içeren dict
    """
    
    # 1. Okunabilirlik
    readability = calculate_readability(content)
    
    # 2. SEO
    seo = calculate_seo_score(content, topic)
    
    # 3. Özgünlük
    originality = calculate_originality_score(content)
    
    # 4. Fact-check (opsiyonel)
    if deep_check and SERPER_API_KEY:
        try:
            client = Groq()
            fact_check = calculate_fact_check_score(client, content)
        except:
            fact_check = {"score": 0, "grade": "N/A", "note": "Analiz yapılamadı"}
    else:
        fact_check = {"score": 0, "grade": "N/A", "note": "Devre dışı"}
    
    # Genel skor (ağırlıklı ortalama)
    weights = {
        "readability": 0.25,
        "seo": 0.30,
        "originality": 0.25,
        "fact_check": 0.20
    }
    
    scores = {
        "readability": readability["score"],
        "seo": seo["score"],
        "originality": originality["score"],
        "fact_check": fact_check["score"] if fact_check["score"] > 0 else 75  # Default
    }
    
    overall_score = sum(scores[k] * weights[k] for k in weights)
    overall_score = round(overall_score)
    
    # Genel grade
    if overall_score >= 80:
        overall_grade = "A"
    elif overall_score >= 65:
        overall_grade = "B"
    elif overall_score >= 50:
        overall_grade = "C"
    elif overall_score >= 35:
        overall_grade = "D"
    else:
        overall_grade = "F"
    
    return {
        "overall": {
            "score": overall_score,
            "grade": overall_grade
        },
        "readability": readability,
        "seo": seo,
        "originality": originality,
        "fact_check": fact_check
    }


# ============================================================
# QUALITY REPORT GENERATOR
# ============================================================

def generate_quality_report(quality_data: Dict) -> str:
    """Kalite raporunu markdown formatında oluştur"""
    
    overall = quality_data["overall"]
    
    report = f"""
## 📊 İçerik Kalite Raporu

### Genel Skor: {overall['score']}/100 ({overall['grade']})

| Metrik | Skor | Grade |
|--------|------|-------|
| 📖 Okunabilirlik | {quality_data['readability']['score']} | {quality_data['readability']['grade']} |
| 🔍 SEO | {quality_data['seo']['score']} | {quality_data['seo']['grade']} |
| ✨ Özgünlük | {quality_data['originality']['score']} | {quality_data['originality']['grade']} |
| ✅ Doğruluk | {quality_data['fact_check']['score']} | {quality_data['fact_check']['grade']} |

"""
    
    # İyileştirme önerileri
    all_suggestions = []
    all_suggestions.extend(quality_data['readability'].get('suggestions', []))
    all_suggestions.extend(quality_data['seo'].get('suggestions', []))
    all_suggestions.extend(quality_data['originality'].get('suggestions', []))
    
    if all_suggestions:
        report += "### 💡 İyileştirme Önerileri\n"
        for i, suggestion in enumerate(all_suggestions[:5], 1):
            report += f"{i}. {suggestion}\n"
    
    return report
