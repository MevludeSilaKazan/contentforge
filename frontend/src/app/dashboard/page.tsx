'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Sparkles, LogOut, Plus, FileText, Copy, Check, Trash2, Users, MessageSquare, FileBarChart } from 'lucide-react';
import { getToken, logout, createBlogStream, getBlogHistory, getUsage, deleteBlog } from '@/lib/api';
import { Blog, Usage, AgentEvent } from '@/lib/types';
import RichContent from '@/components/RichContent';
import AgentProgress from '@/components/AgentProgress';
import QualityDisplay from '@/components/QualityDisplay';

// Seçenekler
const AUDIENCE_OPTIONS = [
  { value: 'general', label: 'Genel', desc: 'Herkes için' },
  { value: 'professional', label: 'Profesyonel', desc: 'Sektör çalışanları' },
  { value: 'entrepreneur', label: 'Girişimci', desc: 'İş sahipleri' },
  { value: 'technical', label: 'Teknik', desc: 'Uzmanlar' },
];

const TONE_OPTIONS = [
  { value: 'friendly', label: 'Samimi', desc: 'Sıcak ve yakın' },
  { value: 'formal', label: 'Resmi', desc: 'Kurumsal' },
  { value: 'educational', label: 'Eğitici', desc: 'Öğretici' },
  { value: 'persuasive', label: 'İkna Edici', desc: 'Satış odaklı' },
];

const LENGTH_OPTIONS = [
  { value: 'short', label: 'Kısa', desc: '~800 kelime' },
  { value: 'medium', label: 'Orta', desc: '~1500 kelime' },
  { value: 'long', label: 'Uzun', desc: '~2500 kelime' },
];

const FORMAT_OPTIONS = [
  { value: 'standard', label: 'Standart', desc: 'Klasik blog', icon: '📝' },
  { value: 'listicle', label: 'Listicle', desc: '\"10 Yol\" formatı', icon: '📋' },
  { value: 'howto', label: 'Nasıl Yapılır', desc: 'Adım adım rehber', icon: '🔧' },
  { value: 'comparison', label: 'Karşılaştırma', desc: 'X vs Y analizi', icon: '⚖️' },
  { value: 'casestudy', label: 'Vaka Çalışması', desc: 'Detaylı analiz', icon: '🔬' },
];

export default function DashboardPage() {
  const router = useRouter();
  
  // Form state
  const [topic, setTopic] = useState('');
  const [audience, setAudience] = useState('general');
  const [tone, setTone] = useState('friendly');
  const [length, setLength] = useState('medium');
  const [formatType, setFormatType] = useState('standard');
  
  // UI state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [blogs, setBlogs] = useState<Blog[]>([]);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [selectedBlog, setSelectedBlog] = useState<Blog | null>(null);
  const [copied, setCopied] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Agent Progress state
  const [agentEvents, setAgentEvents] = useState<AgentEvent[]>([]);
  const [showAgentProgress, setShowAgentProgress] = useState(false);
  const [isGenerationComplete, setIsGenerationComplete] = useState(false);

  // Auth kontrolü
  useEffect(() => {
    if (!getToken()) {
      router.push('/login');
      return;
    }
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [historyData, usageData] = await Promise.all([
        getBlogHistory(),
        getUsage(),
      ]);
      setBlogs(historyData.blogs);
      setUsage(usageData);
    } catch (err) {
      console.error('Veri yükleme hatası:', err);
    } finally {
      setInitialLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setError('');
    setLoading(true);
    setAgentEvents([]);
    setShowAgentProgress(true);
    setIsGenerationComplete(false);
    setSelectedBlog(null);

    createBlogStream(
      topic,
      audience,
      tone,
      length,
      formatType,
      // onEvent
      (event) => {
        setAgentEvents(prev => [...prev, event]);
        
        if (event.type === 'final') {
          setIsGenerationComplete(true);
        }
        
        if (event.type === 'saved' && event.data) {
          const newBlog: Blog = {
            id: event.data.id,
            topic: event.data.topic,
            content: event.data.content,
            created_at: event.data.created_at,
            quality: event.data.quality
          };
          
          setBlogs(prev => [newBlog, ...prev]);
          setSelectedBlog(newBlog);
          setTopic('');
          
          if (usage) {
            setUsage({
              ...usage,
              used: usage.used + 1,
              remaining: usage.remaining - 1,
            });
          }
          
          // 2 saniye sonra progress panelini kapat
          setTimeout(() => {
            setShowAgentProgress(false);
            setLoading(false);
          }, 2000);
        }
      },
      // onError
      (error) => {
        setError(error.message || 'Blog oluşturulamadı');
        setLoading(false);
        setShowAgentProgress(false);
      },
      // onComplete
      () => {
        // Stream tamamlandı
      }
    );
  };

  const handleCopy = async () => {
    if (!selectedBlog) return;
    await navigator.clipboard.writeText(selectedBlog.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bu blogu silmek istediğinize emin misiniz?')) return;
    
    try {
      await deleteBlog(id);
      setBlogs(blogs.filter(b => b.id !== id));
      if (selectedBlog?.id === id) {
        setSelectedBlog(null);
      }
    } catch (err) {
      console.error('Silme hatası:', err);
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  if (initialLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner w-8 h-8"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/dashboard" className="flex items-center gap-2">
            <Sparkles className="w-8 h-8 text-primary-600" />
            <span className="text-xl font-bold">ContentForge</span>
          </Link>
          
          <div className="flex items-center gap-4">
            {usage && (
              <div className="text-sm text-gray-600">
                <span className="font-medium">{usage.remaining}</span> / {usage.limit} kalan
                <span className="ml-2 px-2 py-0.5 bg-primary-100 text-primary-700 rounded text-xs uppercase">
                  {usage.plan}
                </span>
              </div>
            )}
            <button
              onClick={handleLogout}
              className="flex items-center gap-1 text-gray-600 hover:text-gray-900"
            >
              <LogOut className="w-4 h-4" />
              Çıkış
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Sol Panel - Oluşturma + Liste */}
          <div className="lg:col-span-1 space-y-6">
            {/* Blog Oluştur */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Plus className="w-5 h-5" />
                Yeni Blog Oluştur
              </h2>

              {error && (
                <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Konu */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Konu
                  </label>
                  <textarea
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="Blog konusu girin...&#10;Örn: Yapay zeka ve e-ticaret"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                    rows={2}
                    disabled={loading || (usage?.remaining === 0)}
                  />
                </div>

                {/* Gelişmiş Seçenekler Toggle */}
                <button
                  type="button"
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
                >
                  {showAdvanced ? '▼' : '▶'} Gelişmiş Seçenekler
                </button>

                {showAdvanced && (
                  <div className="space-y-4 pt-2">
                    {/* Hedef Kitle */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-1">
                        <Users className="w-4 h-4" />
                        Hedef Kitle
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        {AUDIENCE_OPTIONS.map((opt) => (
                          <button
                            key={opt.value}
                            type="button"
                            onClick={() => setAudience(opt.value)}
                            className={`p-2 text-left rounded-lg border transition ${
                              audience === opt.value
                                ? 'border-primary-500 bg-primary-50 text-primary-700'
                                : 'border-gray-200 hover:border-gray-300'
                            }`}
                          >
                            <div className="text-sm font-medium">{opt.label}</div>
                            <div className="text-xs text-gray-500">{opt.desc}</div>
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Ton */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-1">
                        <MessageSquare className="w-4 h-4" />
                        Yazı Tonu
                      </label>
                      <div className="grid grid-cols-2 gap-2">
                        {TONE_OPTIONS.map((opt) => (
                          <button
                            key={opt.value}
                            type="button"
                            onClick={() => setTone(opt.value)}
                            className={`p-2 text-left rounded-lg border transition ${
                              tone === opt.value
                                ? 'border-primary-500 bg-primary-50 text-primary-700'
                                : 'border-gray-200 hover:border-gray-300'
                            }`}
                          >
                            <div className="text-sm font-medium">{opt.label}</div>
                            <div className="text-xs text-gray-500">{opt.desc}</div>
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Uzunluk */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-1">
                        <FileBarChart className="w-4 h-4" />
                        Uzunluk
                      </label>
                      <div className="grid grid-cols-3 gap-2">
                        {LENGTH_OPTIONS.map((opt) => (
                          <button
                            key={opt.value}
                            type="button"
                            onClick={() => setLength(opt.value)}
                            className={`p-2 text-center rounded-lg border transition ${
                              length === opt.value
                                ? 'border-primary-500 bg-primary-50 text-primary-700'
                                : 'border-gray-200 hover:border-gray-300'
                            }`}
                          >
                            <div className="text-sm font-medium">{opt.label}</div>
                            <div className="text-xs text-gray-500">{opt.desc}</div>
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Format */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        📄 Blog Formatı
                      </label>
                      <div className="space-y-2">
                        {FORMAT_OPTIONS.map((opt) => (
                          <button
                            key={opt.value}
                            type="button"
                            onClick={() => setFormatType(opt.value)}
                            className={`w-full p-3 text-left rounded-lg border transition ${
                              formatType === opt.value
                                ? 'border-primary-500 bg-primary-50'
                                : 'border-gray-200 hover:border-gray-300'
                            }`}
                          >
                            <div className="flex items-center gap-2">
                              <span className="text-lg">{opt.icon}</span>
                              <div>
                                <div className={`text-sm font-medium ${formatType === opt.value ? 'text-primary-700' : ''}`}>
                                  {opt.label}
                                </div>
                                <div className="text-xs text-gray-500">{opt.desc}</div>
                              </div>
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Submit */}
                <button
                  type="submit"
                  disabled={loading || !topic.trim() || (usage?.remaining === 0)}
                  className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <div className="spinner"></div>
                      Oluşturuluyor... (15-30 sn)
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      Blog Oluştur
                    </>
                  )}
                </button>

                {usage?.remaining === 0 && (
                  <p className="mt-2 text-sm text-red-600">
                    Aylık limitiniz doldu. Pro plana geçin.
                  </p>
                )}
              </form>
            </div>

            {/* Blog Geçmişi */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Geçmiş ({blogs.length})
              </h2>

              {blogs.length === 0 ? (
                <p className="text-gray-500 text-sm">Henüz blog oluşturmadınız.</p>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {blogs.map((blog) => (
                    <div
                      key={blog.id}
                      className={`p-3 rounded-lg cursor-pointer flex items-start justify-between group ${
                        selectedBlog?.id === blog.id
                          ? 'bg-primary-50 border border-primary-200'
                          : 'hover:bg-gray-50 border border-transparent'
                      }`}
                      onClick={() => setSelectedBlog(blog)}
                    >
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm truncate">{blog.topic}</p>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="text-xs text-gray-500">
                            {new Date(blog.created_at).toLocaleDateString('tr-TR')}
                          </span>
                          {blog.quality?.overall && (
                            <span className={`text-xs px-1.5 py-0.5 rounded ${
                              blog.quality.overall.score >= 80 ? 'bg-green-100 text-green-700' :
                              blog.quality.overall.score >= 60 ? 'bg-blue-100 text-blue-700' :
                              blog.quality.overall.score >= 40 ? 'bg-yellow-100 text-yellow-700' :
                              'bg-red-100 text-red-700'
                            }`}>
                              {blog.quality.overall.badge} {blog.quality.overall.score}
                            </span>
                          )}
                        </div>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(blog.id);
                        }}
                        className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-600 transition"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Sağ Panel - İçerik Görüntüleme */}
          <div className="lg:col-span-2">
            {/* Agent Progress Panel */}
            {showAgentProgress && (
              <div className="mb-6">
                <AgentProgress 
                  events={agentEvents} 
                  isComplete={isGenerationComplete} 
                />
              </div>
            )}
            
            <div className="bg-white rounded-xl shadow-sm p-6 min-h-[600px]">
              {selectedBlog ? (
                <>
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">{selectedBlog.topic}</h2>
                    <button
                      onClick={handleCopy}
                      className="flex items-center gap-1 px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition"
                    >
                      {copied ? (
                        <>
                          <Check className="w-4 h-4 text-green-600" />
                          Kopyalandı
                        </>
                      ) : (
                        <>
                          <Copy className="w-4 h-4" />
                          Kopyala
                        </>
                      )}
                    </button>
                  </div>
                  
                  {/* Kalite Skoru */}
                  {selectedBlog.quality && (
                    <div className="mb-6">
                      <QualityDisplay quality={selectedBlog.quality} />
                    </div>
                  )}
                  
                  <div className="prose prose-sm max-w-none overflow-auto max-h-[600px] pr-4">
                    <RichContent content={selectedBlog.content} />
                  </div>
                </>
              ) : (
                <div className="h-full flex items-center justify-center text-gray-400">
                  <div className="text-center">
                    <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <p>Blog seçin veya yeni oluşturun</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
