# 🚀 ContentForge

**AI-Powered Turkish Blog Generator** - 5 yapay zeka agent'ı ile profesyonel blog içeriği oluşturun.

![ContentForge Demo](https://contentforge-frontend-ezis.onrender.com)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)

## ✨ Özellikler

- 🔍 **7 Katmanlı Derin Araştırma** - Web'den kapsamlı veri toplama
- 🤖 **5 AI Agent** - Araştırmacı, Görsel Uzmanı, Yazar, Editör, Kalite Analisti
- 📊 **Gerçek Zamanlı İlerleme** - Agent'ların çalışmasını canlı izleyin
- 🎨 **5 Blog Formatı** - Standard, Listicle, How-to, Comparison, Case Study
- 📈 **Kalite Skorları** - Okunabilirlik, SEO, Doğruluk, Özgünlük analizi
- 🖼️ **Otomatik Görsel** - Unsplash entegrasyonu ile telif-ücretsiz görseller
- 🇹🇷 **Türkçe Optimize** - Türkçe içerik üretimi için özelleştirilmiş

## 🛠️ Teknolojiler

### Backend
- **FastAPI** - Modern Python web framework
- **Groq** - Ultra-hızlı LLM inference
- **Serper API** - Google arama entegrasyonu
- **Supabase** - Auth & PostgreSQL database

### Frontend
- **Next.js 14** - React framework
- **Tailwind CSS** - Utility-first CSS
- **TypeScript** - Type-safe JavaScript

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.11+
- Node.js 18+
- Groq API Key ([Ücretsiz al](https://console.groq.com))
- Serper API Key ([Ücretsiz al](https://serper.dev))
- Supabase Projesi ([Oluştur](https://supabase.com))

### 1. Repo'yu Klonla

```bash
git clone https://github.com/YOUR_USERNAME/contentforge.git
cd contentforge
```

### 2. Environment Variables

```bash
cp .env.example .env
```

`.env` dosyasını düzenle:

```env
# Backend
GROQ_API_KEY=gsk_xxxxx
SERPER_API_KEY=xxxxx
UNSPLASH_ACCESS_KEY=xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=xxxxx

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxxxx
```

### 3. Backend Kurulum

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_api.py
```

### 4. Frontend Kurulum

```bash
cd frontend
npm install
npm run dev
```

### 5. Uygulamayı Aç

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🐳 Docker ile Çalıştırma

```bash
# Tüm servisleri başlat
docker-compose up -d

# Logları izle
docker-compose logs -f

# Durdur
docker-compose down
```

## 📁 Proje Yapısı

```
contentforge/
├── backend/
│   ├── agents/
│   │   ├── blog_agents.py    # 5 AI agent + 7 katmanlı araştırma
│   │   └── quality_analyzer.py
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py       # Supabase auth
│   │       ├── blog.py       # Blog CRUD + SSE streaming
│   │       └── user.py
│   ├── config/
│   ├── database/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx      # Landing page
│   │   │   ├── dashboard/    # Ana dashboard
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── components/
│   │   │   ├── AgentProgress.tsx  # Canlı ilerleme
│   │   │   ├── QualityDisplay.tsx
│   │   │   └── RichContent.tsx
│   │   └── lib/
│   │       └── api.ts        # API client + SSE
│   ├── package.json
│   └── tailwind.config.js
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🤖 AI Agent Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│     🔍      │     │     🖼️      │     │     ✍️      │
│ Araştırmacı │ ──▶ │Görsel Uzmanı│ ──▶ │   Yazar     │
│  7 katman   │     │  Unsplash   │     │  5 format   │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                    ┌─────────────┐     ┌─────┴───────┐
                    │     📊      │     │     ✨      │
                    │Kalite Analiz│ ◀── │   Editör    │
                    │  4 metrik   │     │ SEO + Dil   │
                    └─────────────┘     └─────────────┘
```

## 🌐 Deploy

### Railway (Önerilen)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/xxxxx)

1. Railway hesabı oluştur
2. "Deploy on Railway" butonuna tıkla
3. Environment variables ekle
4. Deploy!

### Vercel + Render

**Frontend (Vercel):**
```bash
cd frontend
vercel
```

**Backend (Render):**
1. render.com'da yeni Web Service oluştur
2. Repo'yu bağla
3. Root Directory: `backend`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn api.app:app --host 0.0.0.0 --port $PORT`

## 📝 API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/auth/register` | Kayıt ol |
| POST | `/api/auth/login` | Giriş yap |
| GET | `/api/blog/list` | Blog listesi |
| POST | `/api/blog/create-stream` | Blog oluştur (SSE) |
| GET | `/api/blog/agents` | Agent bilgileri |
| GET | `/api/blog/{id}` | Blog detayı |
| DELETE | `/api/blog/{id}` | Blog sil |

## 🔧 Yapılandırma

### Blog Formatları

| Format | Açıklama |
|--------|----------|
| `standard` | Klasik blog yazısı |
| `listicle` | "10 Yol" formatı |
| `howto` | Adım adım rehber |
| `comparison` | X vs Y karşılaştırma |
| `casestudy` | Detaylı vaka analizi |

### Hedef Kitle

| Kitle | Stil |
|-------|------|
| `general` | Basit dil, günlük örnekler |
| `professional` | Teknik terimler, derinlemesine |
| `entrepreneur` | ROI odaklı, iş değeri |
| `technical` | Detaylı metodoloji |

## 🤝 Katkıda Bulunma

1. Fork'la
2. Feature branch oluştur (`git checkout -b feature/amazing`)
3. Commit'le (`git commit -m 'Add amazing feature'`)
4. Push'la (`git push origin feature/amazing`)
5. Pull Request aç

## 📄 Lisans

MIT License - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Groq](https://groq.com) - Ultra-hızlı LLM inference
- [Serper](https://serper.dev) - Google Search API
- [Unsplash](https://unsplash.com) - Ücretsiz görseller
- [Supabase](https://supabase.com) - Backend as a Service

---

<p align="center">
  Made with ❤️ in Turkey
</p>
