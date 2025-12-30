'use client';

interface QualityScore {
  overall: {
    score: number;
    level: string;
    grade: string;
  };
  readability: {
    score: number;
    level: string;
  };
  seo: {
    score: number;
    level: string;
    checks?: Array<[string, string, string]>;
  };
  fact_check: {
    score: number;
    level: string;
  };
  originality: {
    score: number;
    level: string;
  };
}

interface QualityDisplayProps {
  quality: QualityScore | null;
  compact?: boolean;
}

function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-blue-600';
  if (score >= 40) return 'text-yellow-600';
  return 'text-red-600';
}

function getScoreBg(score: number): string {
  if (score >= 80) return 'bg-green-100';
  if (score >= 60) return 'bg-blue-100';
  if (score >= 40) return 'bg-yellow-100';
  return 'bg-red-100';
}

function getProgressColor(score: number): string {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-blue-500';
  if (score >= 40) return 'bg-yellow-500';
  return 'bg-red-500';
}

function ScoreCircle({ score, label, icon }: { score: number; label: string; icon: string }) {
  const circumference = 2 * Math.PI * 40;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-24 h-24">
        <svg className="w-24 h-24 transform -rotate-90">
          {/* Background circle */}
          <circle
            cx="48"
            cy="48"
            r="40"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="8"
          />
          {/* Progress circle */}
          <circle
            cx="48"
            cy="48"
            r="40"
            fill="none"
            stroke={score >= 80 ? '#22c55e' : score >= 60 ? '#3b82f6' : score >= 40 ? '#eab308' : '#ef4444'}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className="transition-all duration-500"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-lg">{icon}</span>
          <span className={`text-xl font-bold ${getScoreColor(score)}`}>{score}</span>
        </div>
      </div>
      <span className="mt-1 text-xs text-gray-600 text-center">{label}</span>
    </div>
  );
}

function ScoreBar({ score, label, icon }: { score: number; label: string; icon: string }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-lg w-6">{icon}</span>
      <div className="flex-1">
        <div className="flex justify-between text-xs mb-1">
          <span className="text-gray-600">{label}</span>
          <span className={`font-medium ${getScoreColor(score)}`}>{score}/100</span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className={`h-full rounded-full transition-all duration-500 ${getProgressColor(score)}`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>
    </div>
  );
}

export default function QualityDisplay({ quality, compact = false }: QualityDisplayProps) {
  if (!quality) {
    return null;
  }

  const { overall, readability, seo, fact_check, originality } = quality;

  if (compact) {
    // Kompakt görünüm - sadece genel skor
    return (
      <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full ${getScoreBg(overall.score)}`}>
        <span>{overall.grade}</span>
        <span className={`font-semibold ${getScoreColor(overall.score)}`}>
          {overall.score}/100
        </span>
        <span className="text-xs text-gray-600">{overall.level}</span>
      </div>
    );
  }

  // Tam görünüm
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
        📊 İçerik Kalite Analizi
      </h3>

      {/* Genel Skor */}
      <div className={`mb-6 p-4 rounded-lg ${getScoreBg(overall.score)}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{overall.grade}</span>
            <div>
              <div className={`text-2xl font-bold ${getScoreColor(overall.score)}`}>
                {overall.score}/100
              </div>
              <div className="text-sm text-gray-600">{overall.level}</div>
            </div>
          </div>
          <div className="text-right text-sm text-gray-500">
            Genel Kalite
          </div>
        </div>
      </div>

      {/* Daire Grafikler */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <ScoreCircle score={readability.score} label="Okunabilirlik" icon="📖" />
        <ScoreCircle score={seo.score} label="SEO" icon="🎯" />
        <ScoreCircle score={fact_check.score} label="Doğruluk" icon="✓" />
        <ScoreCircle score={originality.score} label="Özgünlük" icon="💎" />
      </div>

      {/* Çubuk Grafikler */}
      <div className="space-y-3">
        <ScoreBar score={readability.score} label="Okunabilirlik" icon="📖" />
        <ScoreBar score={seo.score} label="SEO Uyumluluğu" icon="🎯" />
        <ScoreBar score={fact_check.score} label="İçerik Doğruluğu" icon="✓" />
        <ScoreBar score={originality.score} label="Özgünlük" icon="💎" />
      </div>

      {/* Seviye Açıklamaları */}
      <div className="mt-6 pt-4 border-t border-gray-100">
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-green-500"></span>
            <span className="text-gray-600">80+ Mükemmel</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-blue-500"></span>
            <span className="text-gray-600">60-79 İyi</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
            <span className="text-gray-600">40-59 Orta</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-red-500"></span>
            <span className="text-gray-600">0-39 Geliştir</span>
          </div>
        </div>
      </div>
    </div>
  );
}
