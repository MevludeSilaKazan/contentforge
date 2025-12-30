/**
 * ContentForge API Client
 */

import { AgentEvent } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Token yönetimi
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

export function setToken(token: string): void {
  localStorage.setItem('token', token);
}

export function removeToken(): void {
  localStorage.removeItem('token');
}

// API çağrısı helper
async function apiCall(
  endpoint: string,
  options: RequestInit = {}
): Promise<any> {
  const token = getToken();
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Bir hata oluştu');
  }

  return data;
}

// ============================================================
// AUTH
// ============================================================

export async function register(email: string, password: string) {
  const data = await apiCall('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  
  if (data.access_token) {
    setToken(data.access_token);
  }
  
  return data;
}

export async function login(email: string, password: string) {
  const data = await apiCall('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  
  if (data.access_token) {
    setToken(data.access_token);
  }
  
  return data;
}

export function logout() {
  removeToken();
}

// ============================================================
// BLOG
// ============================================================

export async function createBlog(
  topic: string,
  audience: string = 'general',
  tone: string = 'friendly',
  length: string = 'medium',
  format_type: string = 'standard'
) {
  return apiCall('/api/blog/create', {
    method: 'POST',
    body: JSON.stringify({ topic, audience, tone, length, format_type }),
  });
}

// Streaming blog oluşturma - SSE ile
export function createBlogStream(
  topic: string,
  audience: string = 'general',
  tone: string = 'friendly',
  length: string = 'medium',
  format_type: string = 'standard',
  onEvent: (event: AgentEvent) => void,
  onError: (error: Error) => void,
  onComplete: () => void
): () => void {
  const token = getToken();
  
  const controller = new AbortController();
  
  fetch(`${API_URL}/api/blog/create-stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ topic, audience, tone, length, format_type }),
    signal: controller.signal
  })
  .then(async (response) => {
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Blog oluşturulamadı');
    }
    
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    
    if (!reader) {
      throw new Error('Stream reader oluşturulamadı');
    }
    
    let buffer = '';
    
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        onComplete();
        break;
      }
      
      buffer += decoder.decode(value, { stream: true });
      
      // SSE formatını parse et
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6)) as AgentEvent;
            onEvent(data);
          } catch (e) {
            console.error('Event parse hatası:', e);
          }
        }
      }
    }
  })
  .catch((error) => {
    if (error.name !== 'AbortError') {
      onError(error);
    }
  });
  
  // Abort fonksiyonu döndür
  return () => controller.abort();
}

// Agent bilgilerini al
export async function getAgents() {
  return apiCall('/api/blog/agents');
}

export async function getBlogHistory(limit = 10, offset = 0) {
  return apiCall(`/api/blog/history?limit=${limit}&offset=${offset}`);
}

export async function getBlog(id: string) {
  return apiCall(`/api/blog/${id}`);
}

export async function deleteBlog(id: string) {
  return apiCall(`/api/blog/${id}`, {
    method: 'DELETE',
  });
}

// ============================================================
// USER
// ============================================================

export async function getUsage() {
  return apiCall('/api/user/usage');
}

export async function getProfile() {
  return apiCall('/api/user/profile');
}
