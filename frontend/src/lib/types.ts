// Ortak type tanımları

export interface Agent {
  id: string;
  name: string;
  name_en?: string;
  avatar: string;
  color: string;
  description: string;
  tasks: string[];
}

export interface AgentEvent {
  type: 'agent_start' | 'agent_complete' | 'final' | 'saved' | 'error';
  agent?: Agent;
  step?: number;
  total_steps?: number;
  message?: string;
  data?: any;
}

export interface Blog {
  id: string;
  topic: string;
  content: string;
  created_at: string;
  quality?: QualityScore;
}

export interface Usage {
  plan: string;
  used: number;
  limit: number;
  remaining: number;
}

export interface QualityScore {
  overall: {
    score: number;
    level: string;
    level_color: string;
    grade: string;
  };
  readability: {
    score: number;
    level: string;
    level_color: string;
  };
  seo: {
    score: number;
    level: string;
    level_color: string;
  };
  fact_check: {
    score: number;
    level: string;
    level_color: string;
  };
  originality: {
    score: number;
    level: string;
    level_color: string;
  };
}
