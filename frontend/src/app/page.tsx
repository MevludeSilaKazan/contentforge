'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, Zap, Search, FileText, ArrowRight, CheckCircle, Star } from 'lucide-react';

// AI Agent tanımları
const AI_AGENTS = [
  {
    id: 'researcher',
    name: 'Araştırmacı',
    avatar: '🔍',
    color: '#3B82F6',
    role: 'Web Araştırma Uzmanı',
    description: 'İnternette kapsamlı araştırma yapar, güncel veriler ve istatistikler toplar.',
    tasks: ['Kaynak tarama', 'Veri toplama', 'İstatistik bulma']
  },
  {
    id: 'visual',
    name: 'Görsel Uzmanı',
    avatar: '🖼️',
    color: '#8B5CF6',
    role: 'Görsel Seçim Uzmanı',
    description: 'Blog yazınız için en uygun, telif hakkı güvenli görselleri seçer.',
    tasks: ['Görsel arama', 'Uygunluk kontrolü', 'Lisans doğrulama']
  },
  {
    id: 'writer',
    name: 'Yazar',
    avatar: '✍️',
    color: '#10B981',
    role: 'İçerik Yazarı',
    description: 'Araştırma verilerini kullanarak akıcı, etkileyici içerik oluşturur.',
    tasks: ['Yapı oluşturma', 'İçerik yazma', 'Örnek ekleme']
  },
  {
    id: 'editor',
    name: 'Editör',
    avatar: '✨',
    color: '#F59E0B',
    role: 'Baş Editör',
    description: 'İçeriği düzenler, dil hatalarını düzeltir ve SEO optimize eder.',
    tasks: ['Dil kontrolü', 'SEO optimizasyonu', 'Format düzenleme']
  },
  {
    id: 'analyst',
    name: 'Kalite Analisti',
    avatar: '📊',
    color: '#EF4444',
    role: 'Kalite Kontrol Uzmanı',
    description: 'Blog kalitesini analiz eder, okunabilirlik ve özgünlük skorları hesaplar.',
    tasks: ['Okunabilirlik', 'SEO skoru', 'Özgünlük analizi']
  }
];

export default function Home() {
  const [activeAgent, setActiveAgent] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);

  // Agent döngüsü animasyonu
  useEffect(() => {
    if (!isAnimating) return;
    
    const interval = setInterval(() => {
      setActiveAgent((prev) => (prev + 1) % AI_AGENTS.length);
    }, 3000);

    return () => clearInterval(interval);
  }, [isAnimating]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Sparkles className="w-8 h-8 text-primary-600" />
            <span className="text-xl font-bold">ContentForge</span>
          </div>
          <div className="flex gap-3">
            <Link
              href="/login"
              className="px-4 py-2 text-gray-600 hover:text-gray-900"
            >
              Giriş Yap
            </Link>
            <Link
              href="/register"
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
            >
              Ücretsiz Başla
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 overflow-hidden">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 text-primary-700 rounded-full text-sm mb-6">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary-500"></span>
              </span>
              5 AI Agent Birlikte Çalışıyor
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              <span className="bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
                AI Ekibiniz
              </span>
              <br />
              Blog Yazıyor
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              5 uzman yapay zeka agent'ı sizin için araştırma yapar, yazar, düzenler ve kalite kontrol eder. Profesyonel blog içeriği dakikalar içinde hazır.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/register"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-primary-600 text-white text-lg font-medium rounded-xl hover:bg-primary-700 transition shadow-lg shadow-primary-200"
              >
                Ücretsiz Deneyin
                <ArrowRight className="w-5 h-5" />
              </Link>
              <a
                href="#ai-team"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-white text-gray-700 text-lg font-medium rounded-xl hover:bg-gray-50 transition border border-gray-200"
              >
                Ekibi Tanıyın
              </a>
            </div>
            
            <p className="mt-6 text-gray-500 flex items-center justify-center gap-4">
              <span className="flex items-center gap-1">
                <CheckCircle className="w-4 h-4 text-green-500" />
                Kredi kartı gerekmez
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle className="w-4 h-4 text-green-500" />
                3 blog ücretsiz
              </span>
            </p>
          </div>

          {/* Animated Agent Showcase */}
          <div className="relative max-w-4xl mx-auto">
            {/* Background Glow */}
            <div 
              className="absolute inset-0 blur-3xl opacity-20 transition-colors duration-1000"
              style={{ backgroundColor: AI_AGENTS[activeAgent].color }}
            />
            
            {/* Agent Cards Circle */}
            <div className="relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 shadow-2xl">
              {/* Top Agents Row */}
              <div className="flex justify-center gap-4 mb-6">
                {AI_AGENTS.slice(0, 3).map((agent, idx) => (
                  <div
                    key={agent.id}
                    onClick={() => { setActiveAgent(idx); setIsAnimating(false); }}
                    className={`cursor-pointer transition-all duration-500 ${
                      activeAgent === idx 
                        ? 'scale-110 z-10' 
                        : 'scale-90 opacity-60 hover:opacity-80'
                    }`}
                  >
                    <div 
                      className={`w-20 h-20 rounded-2xl flex items-center justify-center text-4xl shadow-lg transition-all duration-500 ${
                        activeAgent === idx ? 'animate-bounce' : ''
                      }`}
                      style={{ 
                        backgroundColor: `${agent.color}30`,
                        boxShadow: activeAgent === idx ? `0 0 30px ${agent.color}50` : 'none'
                      }}
                    >
                      {agent.avatar}
                    </div>
                  </div>
                ))}
              </div>

              {/* Bottom Agents Row */}
              <div className="flex justify-center gap-4 mb-8">
                {AI_AGENTS.slice(3, 5).map((agent, idx) => (
                  <div
                    key={agent.id}
                    onClick={() => { setActiveAgent(idx + 3); setIsAnimating(false); }}
                    className={`cursor-pointer transition-all duration-500 ${
                      activeAgent === idx + 3 
                        ? 'scale-110 z-10' 
                        : 'scale-90 opacity-60 hover:opacity-80'
                    }`}
                  >
                    <div 
                      className={`w-20 h-20 rounded-2xl flex items-center justify-center text-4xl shadow-lg transition-all duration-500 ${
                        activeAgent === idx + 3 ? 'animate-bounce' : ''
                      }`}
                      style={{ 
                        backgroundColor: `${agent.color}30`,
                        boxShadow: activeAgent === idx + 3 ? `0 0 30px ${agent.color}50` : 'none'
                      }}
                    >
                      {agent.avatar}
                    </div>
                  </div>
                ))}
              </div>

              {/* Active Agent Info */}
              <div 
                className="p-6 rounded-2xl border-2 transition-all duration-500"
                style={{ 
                  borderColor: AI_AGENTS[activeAgent].color,
                  backgroundColor: `${AI_AGENTS[activeAgent].color}10`
                }}
              >
                <div className="flex items-start gap-4">
                  <div 
                    className="w-16 h-16 rounded-xl flex items-center justify-center text-3xl flex-shrink-0"
                    style={{ backgroundColor: `${AI_AGENTS[activeAgent].color}30` }}
                  >
                    {AI_AGENTS[activeAgent].avatar}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-white font-bold text-xl">{AI_AGENTS[activeAgent].name}</h3>
                      <span 
                        className="px-2 py-0.5 rounded text-xs font-medium"
                        style={{ 
                          backgroundColor: `${AI_AGENTS[activeAgent].color}30`,
                          color: AI_AGENTS[activeAgent].color
                        }}
                      >
                        {AI_AGENTS[activeAgent].role}
                      </span>
                    </div>
                    <p className="text-gray-400 text-sm mb-3">{AI_AGENTS[activeAgent].description}</p>
                    <div className="flex flex-wrap gap-2">
                      {AI_AGENTS[activeAgent].tasks.map((task, i) => (
                        <span 
                          key={i}
                          className="px-3 py-1 bg-white/10 rounded-full text-xs text-gray-300"
                        >
                          {task}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Pipeline Flow */}
              <div className="mt-6 flex items-center justify-center gap-2">
                {AI_AGENTS.map((agent, idx) => (
                  <div key={agent.id} className="flex items-center">
                    <div 
                      className={`w-8 h-8 rounded-lg flex items-center justify-center text-lg transition-all duration-300 ${
                        idx <= activeAgent ? 'opacity-100' : 'opacity-30'
                      }`}
                      style={{ backgroundColor: `${agent.color}30` }}
                    >
                      {agent.avatar}
                    </div>
                    {idx < AI_AGENTS.length - 1 && (
                      <div 
                        className={`w-8 h-0.5 mx-1 transition-all duration-300 ${
                          idx < activeAgent ? 'bg-green-500' : 'bg-gray-600'
                        }`}
                      />
                    )}
                  </div>
                ))}
              </div>
              
              <p className="text-center text-gray-500 text-sm mt-4">
                Her blog yazısı bu 5 agent'ın işbirliğiyle oluşturulur
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* AI Team Section */}
      <section id="ai-team" className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              AI Ekibinizle Tanışın
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Her biri kendi uzmanlık alanında çalışan 5 yapay zeka agent'ı, mükemmel içerik için birlikte çalışır.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {AI_AGENTS.map((agent, idx) => (
              <div 
                key={agent.id}
                className="relative group bg-white rounded-2xl p-6 border border-gray-200 hover:border-transparent hover:shadow-xl transition-all duration-300"
              >
                <div className="flex items-start gap-4">
                  <div 
                    className="w-14 h-14 rounded-xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300"
                    style={{ backgroundColor: `${agent.color}20` }}
                  >
                    {agent.avatar}
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-gray-900">{agent.name}</h3>
                    <p 
                      className="text-sm font-medium"
                      style={{ color: agent.color }}
                    >
                      {agent.role}
                    </p>
                  </div>
                </div>
                <p className="text-gray-600 mt-4 text-sm">{agent.description}</p>
                <div className="flex flex-wrap gap-2 mt-4">
                  {agent.tasks.map((task, i) => (
                    <span 
                      key={i}
                      className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600"
                    >
                      {task}
                    </span>
                  ))}
                </div>
                
                {/* Step Number */}
                <div 
                  className="absolute top-4 right-4 w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{ backgroundColor: agent.color }}
                >
                  {idx + 1}
                </div>
              </div>
            ))}
            
            {/* Result Card */}
            <div className="bg-gradient-to-br from-primary-600 to-purple-600 rounded-2xl p-6 text-white">
              <div className="w-14 h-14 rounded-xl bg-white/20 flex items-center justify-center text-2xl mb-4">
                ✅
              </div>
              <h3 className="font-bold text-lg mb-2">Sonuç: Mükemmel Blog</h3>
              <p className="text-white/80 text-sm mb-4">
                5 agent'ın işbirliğiyle oluşturulan, araştırma destekli, SEO uyumlu, kalite skorlu profesyonel blog yazısı.
              </p>
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  Gerçek zamanlı web araştırması
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  Otomatik görsel seçimi
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  SEO optimizasyonu
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  Kalite skoru analizi
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Nasıl Çalışır?</h2>
            <p className="text-xl text-gray-600">3 basit adımda profesyonel blog içeriği</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="relative">
              <div className="bg-white rounded-2xl p-8 border border-gray-200 h-full">
                <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center text-primary-600 font-bold text-xl mb-4">
                  1
                </div>
                <h3 className="text-xl font-bold mb-3">Konunuzu Yazın</h3>
                <p className="text-gray-600">
                  Blog konunuzu girin. Format, ton ve uzunluk seçeneklerini belirleyin.
                </p>
                <div className="mt-4 p-3 bg-gray-50 rounded-lg text-sm text-gray-500 italic">
                  "E-ticarette yapay zeka kullanımı ve geleceği"
                </div>
              </div>
              {/* Arrow */}
              <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                <ArrowRight className="w-8 h-8 text-gray-300" />
              </div>
            </div>

            <div className="relative">
              <div className="bg-white rounded-2xl p-8 border border-gray-200 h-full">
                <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center text-primary-600 font-bold text-xl mb-4">
                  2
                </div>
                <h3 className="text-xl font-bold mb-3">AI Ekibi Çalışır</h3>
                <p className="text-gray-600">
                  5 AI agent sırayla görevlerini yerine getirir. İlerlemeyi canlı izleyin.
                </p>
                <div className="mt-4 flex -space-x-2">
                  {AI_AGENTS.map((agent) => (
                    <div 
                      key={agent.id}
                      className="w-10 h-10 rounded-full flex items-center justify-center text-lg border-2 border-white"
                      style={{ backgroundColor: `${agent.color}30` }}
                    >
                      {agent.avatar}
                    </div>
                  ))}
                </div>
              </div>
              {/* Arrow */}
              <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                <ArrowRight className="w-8 h-8 text-gray-300" />
              </div>
            </div>

            <div>
              <div className="bg-white rounded-2xl p-8 border border-gray-200 h-full">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center text-green-600 font-bold text-xl mb-4">
                  ✓
                </div>
                <h3 className="text-xl font-bold mb-3">Blog Hazır!</h3>
                <p className="text-gray-600">
                  Görsellerle zenginleştirilmiş, SEO uyumlu, kalite skorlu blog yazınız hazır.
                </p>
                <div className="mt-4 flex items-center gap-2">
                  <div className="flex">
                    {[1,2,3,4,5].map((star) => (
                      <Star key={star} className="w-4 h-4 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <span className="text-sm text-gray-500">Kalite Skoru: 85/100</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Fiyatlandırma</h2>
            <p className="text-xl text-gray-600">Hemen ücretsiz başlayın</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Free */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 shadow-sm">
              <h3 className="text-xl font-bold mb-2">Ücretsiz</h3>
              <p className="text-4xl font-bold mb-6">₺0 <span className="text-lg text-gray-500 font-normal">/ay</span></p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>3 blog / ay</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>5 AI Agent</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>Web araştırması</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>Görsel ekleme</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>Kalite analizi</span>
                </li>
              </ul>
              <Link
                href="/register"
                className="block w-full py-3 text-center bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition font-medium"
              >
                Ücretsiz Başla
              </Link>
            </div>

            {/* Pro */}
            <div className="bg-gradient-to-br from-primary-600 to-purple-600 text-white rounded-2xl p-8 relative shadow-xl">
              <div className="absolute top-4 right-4 bg-yellow-400 text-yellow-900 text-xs px-3 py-1 rounded-full font-medium">
                Popüler
              </div>
              <h3 className="text-xl font-bold mb-2">Pro</h3>
              <p className="text-4xl font-bold mb-6">₺299 <span className="text-lg opacity-80 font-normal">/ay</span></p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5" />
                  <span>30 blog / ay</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5" />
                  <span>5 AI Agent</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5" />
                  <span>Gelişmiş araştırma</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5" />
                  <span>Sınırsız görsel</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5" />
                  <span>Öncelikli destek</span>
                </li>
              </ul>
              <button
                className="block w-full py-3 text-center bg-white text-primary-600 rounded-xl hover:bg-gray-100 transition font-medium"
              >
                Yakında
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            AI Ekibiniz Sizi Bekliyor
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Hemen ücretsiz başlayın ve 5 AI agent'ın sizin için nasıl çalıştığını görün.
          </p>
          <Link
            href="/register"
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-primary-600 text-white text-lg font-medium rounded-xl hover:bg-primary-700 transition shadow-lg shadow-primary-200"
          >
            Ücretsiz Deneyin
            <ArrowRight className="w-5 h-5" />
          </Link>
          
          <div className="mt-8 flex items-center justify-center gap-6 text-sm text-gray-500">
            <div className="flex -space-x-2">
              {AI_AGENTS.map((agent) => (
                <div 
                  key={agent.id}
                  className="w-8 h-8 rounded-full flex items-center justify-center text-sm border-2 border-white"
                  style={{ backgroundColor: `${agent.color}30` }}
                >
                  {agent.avatar}
                </div>
              ))}
            </div>
            <span>5 AI Agent hazır</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t bg-white">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-primary-600" />
            <span className="font-bold">ContentForge</span>
          </div>
          <p className="text-gray-500 text-sm">© 2024 ContentForge. Tüm hakları saklıdır.</p>
        </div>
      </footer>
    </div>
  );
}
