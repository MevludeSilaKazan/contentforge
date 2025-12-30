# 🛠️ ContentForge Kurulum Rehberi

Bu rehber, ContentForge'u sıfırdan kurmanızı adım adım anlatır.

## 📋 Gereksinimler

- Python 3.11+
- Node.js 18+
- Git
- Bir kod editörü (VS Code önerilir)

## 🔑 API Key'leri Alma

### 1. Groq API Key (Zorunlu)
1. https://console.groq.com adresine gidin
2. Ücretsiz hesap oluşturun
3. "API Keys" bölümünden yeni key oluşturun
4. Key'i kopyalayın: `gsk_xxxx...`

### 2. Serper API Key (Zorunlu)
1. https://serper.dev adresine gidin
2. Ücretsiz hesap oluşturun (2500 arama/ay)
3. Dashboard'dan API key'i kopyalayın

### 3. Unsplash API Key (Opsiyonel)
1. https://unsplash.com/developers adresine gidin
2. "New Application" oluşturun
3. Access Key'i kopyalayın

### 4. Supabase Projesi (Zorunlu)
1. https://supabase.com adresine gidin
2. Ücretsiz hesap oluşturun
3. "New Project" ile yeni proje oluşturun
4. Project Settings > API bölümünden:
   - `Project URL` → SUPABASE_URL
   - `anon public` key → SUPABASE_ANON_KEY
   - `service_role` key → SUPABASE_KEY

## 🗄️ Supabase Veritabanı Kurulumu

1. Supabase Dashboard'a gidin
2. Sol menüden "SQL Editor" seçin
3. "New Query" tıklayın
4. `backend/database/schema.sql` içeriğini yapıştırın
5. "Run" butonuna tıklayın

## 💻 Local Kurulum

### 1. Repo'yu Klonla
```bash
git clone https://github.com/YOUR_USERNAME/contentforge.git
cd contentforge
```

### 2. Environment Variables
```bash
cp .env.example .env
```

`.env` dosyasını açın ve değerleri doldurun:
```env
GROQ_API_KEY=gsk_xxxxx
SERPER_API_KEY=xxxxx
UNSPLASH_ACCESS_KEY=xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJxxxxx
SUPABASE_ANON_KEY=eyJxxxxx
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxxxx
```

### 3. Hızlı Başlatma (Önerilen)
```bash
chmod +x start.sh
./start.sh
```

### 4. Manuel Başlatma

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 5. Uygulamayı Test Et
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🐳 Docker ile Kurulum

```bash
# .env dosyasını düzenleyin
cp .env.example .env
nano .env

# Docker Compose ile başlatın
docker-compose up -d

# Logları izleyin
docker-compose logs -f
```

## 🌐 Deploy Seçenekleri

### Option 1: Railway (En Kolay)

1. https://railway.app adresine gidin
2. GitHub ile giriş yapın
3. "New Project" > "Deploy from GitHub repo"
4. Repo'nuzu seçin
5. Environment variables ekleyin
6. Deploy!

### Option 2: Vercel + Render

**Frontend (Vercel):**
```bash
cd frontend
npx vercel
```

**Backend (Render):**
1. https://render.com adresine gidin
2. "New" > "Blueprint"
3. Repo'nuzu bağlayın
4. `render.yaml` otomatik algılanacak

### Option 3: Manual VPS

```bash
# Sunucuda
git clone https://github.com/YOUR_USERNAME/contentforge.git
cd contentforge
docker-compose -f docker-compose.yml up -d
```

## ❓ Sık Karşılaşılan Sorunlar

### "Module not found" hatası
```bash
pip install -r requirements.txt --force-reinstall
```

### CORS hatası
Backend `.env`'e ekleyin:
```env
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Supabase bağlantı hatası
1. API key'lerin doğruluğunu kontrol edin
2. Supabase Dashboard'da RLS policy'lerini kontrol edin

### Port kullanımda hatası
```bash
# Mac/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📞 Destek

Sorun mu yaşıyorsunuz?
1. GitHub Issues açın
2. Hata mesajını ve adımları paylaşın
