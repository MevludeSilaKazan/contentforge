'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface RichContentProps {
  content: string;
}

export default function RichContent({ content }: RichContentProps) {
  // YAML frontmatter'ı ayır
  let displayContent = content;
  let metadata: Record<string, string> = {};
  
  if (content.startsWith('---')) {
    const parts = content.split('---');
    if (parts.length >= 3) {
      const yamlPart = parts[1];
      displayContent = parts.slice(2).join('---').trim();
      
      // Basit YAML parse
      yamlPart.split('\n').forEach(line => {
        const [key, ...valueParts] = line.split(':');
        if (key && valueParts.length) {
          metadata[key.trim()] = valueParts.join(':').trim();
        }
      });
    }
  }
  
  return (
    <div className="rich-content">
      {/* Metadata Header */}
      {metadata.baslik && (
        <div className="mb-6 pb-4 border-b border-gray-200">
          <div className="flex flex-wrap gap-3 text-sm text-gray-500">
            {metadata.okuma_suresi && (
              <span className="flex items-center gap-1">
                ⏱️ {metadata.okuma_suresi}
              </span>
            )}
            {metadata.gorsel_sayisi && (
              <span className="flex items-center gap-1">
                🖼️ {metadata.gorsel_sayisi} görsel
              </span>
            )}
          </div>
          {metadata.anahtar_kelimeler && (
            <div className="mt-2 flex flex-wrap gap-1">
              {metadata.anahtar_kelimeler.replace(/[\[\]]/g, '').split(',').map((tag, i) => (
                <span key={i} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                  {tag.trim()}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
      
      {/* Markdown Content */}
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Başlıklar
          h1: ({ children }) => (
            <h1 className="text-3xl font-bold text-gray-900 mb-6 mt-8 first:mt-0">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-2xl font-bold text-gray-800 mb-4 mt-8 pb-2 border-b border-gray-200">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xl font-semibold text-gray-800 mb-3 mt-6">
              {children}
            </h3>
          ),
          
          // Paragraflar
          p: ({ children }) => (
            <p className="text-gray-700 mb-4 leading-relaxed">
              {children}
            </p>
          ),
          
          // Görseller
          img: ({ src, alt }) => (
            <figure className="my-6">
              <img 
                src={src} 
                alt={alt || ''} 
                className="w-full rounded-lg shadow-md"
              />
              {alt && (
                <figcaption className="text-center text-sm text-gray-500 mt-2 italic">
                  {alt}
                </figcaption>
              )}
            </figure>
          ),
          
          // Alıntılar (Highlight kutuları için)
          blockquote: ({ children }) => {
            const text = String(children);
            
            // Highlight kutusu tespiti
            if (text.includes('📊') || text.includes('Önemli Veri')) {
              return (
                <div className="my-4 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
                  <div className="text-blue-800">{children}</div>
                </div>
              );
            }
            
            // Uzman görüşü kutusu
            if (text.includes('💬') || text.includes('Uzman Görüşü')) {
              return (
                <div className="my-4 p-4 bg-purple-50 border-l-4 border-purple-500 rounded-r-lg">
                  <div className="text-purple-800 italic">{children}</div>
                </div>
              );
            }
            
            // Önemli çıkarım kutusu
            if (text.includes('✅') || text.includes('Önemli Çıkarım')) {
              return (
                <div className="my-4 p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
                  <div className="text-green-800">{children}</div>
                </div>
              );
            }
            
            // Uyarı kutusu
            if (text.includes('⚠️') || text.includes('Dikkat')) {
              return (
                <div className="my-4 p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
                  <div className="text-yellow-800">{children}</div>
                </div>
              );
            }
            
            // Normal alıntı
            return (
              <blockquote className="my-4 p-4 bg-gray-50 border-l-4 border-gray-300 rounded-r-lg italic text-gray-700">
                {children}
              </blockquote>
            );
          },
          
          // Listeler
          ul: ({ children }) => (
            <ul className="my-4 ml-6 space-y-2 list-disc text-gray-700">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="my-4 ml-6 space-y-2 list-decimal text-gray-700">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="leading-relaxed">{children}</li>
          ),
          
          // Tablolar
          table: ({ children }) => (
            <div className="my-6 overflow-x-auto">
              <table className="min-w-full border border-gray-200 rounded-lg overflow-hidden">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-gray-50">{children}</thead>
          ),
          th: ({ children }) => (
            <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 border-b">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-4 py-3 text-sm text-gray-600 border-b">
              {children}
            </td>
          ),
          
          // Kod
          code: ({ children, className }) => {
            const isInline = !className;
            if (isInline) {
              return (
                <code className="px-1.5 py-0.5 bg-gray-100 text-gray-800 text-sm rounded">
                  {children}
                </code>
              );
            }
            return (
              <code className="block p-4 bg-gray-900 text-gray-100 text-sm rounded-lg overflow-x-auto">
                {children}
              </code>
            );
          },
          
          // Linkler
          a: ({ href, children }) => (
            <a 
              href={href} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-800 underline"
            >
              {children}
            </a>
          ),
          
          // Kalın ve italik
          strong: ({ children }) => (
            <strong className="font-semibold text-gray-900">{children}</strong>
          ),
          em: ({ children }) => (
            <em className="italic">{children}</em>
          ),
          
          // Yatay çizgi
          hr: () => (
            <hr className="my-8 border-gray-200" />
          ),
        }}
      >
        {displayContent}
      </ReactMarkdown>
    </div>
  );
}
