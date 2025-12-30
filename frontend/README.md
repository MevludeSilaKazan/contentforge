# ContentForge Frontend 🎨

Next.js 14 ile oluşturulmuş ContentForge kullanıcı arayüzü.

## ✨ Özellikler

- 🤖 AI Agent progress gösterimi (SSE)
- 📝 5 blog formatı seçimi
- 📊 Kalite skoru görüntüleme
- 🎨 Modern, responsive tasarım
- 🔐 Supabase Auth entegrasyonu

## 🚀 Kurulum

```bash
npm install
cp .env.example .env.local
```

`.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🏃 Çalıştırma

```bash
npm run dev
```

## 📁 Yapı

```
src/
├── app/
│   ├── page.tsx           # Landing (AI Team)
│   ├── login/             # Giriş
│   ├── register/          # Kayıt
│   └── dashboard/         # Dashboard
├── components/
│   ├── AgentProgress.tsx  # Agent gösterimi
│   ├── RichContent.tsx    # Markdown
│   └── QualityDisplay.tsx # Kalite
└── lib/
    └── api.ts             # API client
```

## 🛠️ Teknolojiler

- Next.js 14 + TypeScript
- Tailwind CSS
- Lucide Icons
- react-markdown

## 📄 Lisans

MIT
