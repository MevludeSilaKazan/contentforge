'use client';

import { useEffect, useState } from 'react';

interface Agent {
  id: string;
  name: string;
  name_en: string;
  avatar: string;
  color: string;
  description: string;
  tasks: string[];
}

interface AgentEvent {
  type: 'agent_start' | 'agent_complete' | 'final' | 'saved' | 'error';
  agent?: Agent;
  step?: number;
  total_steps?: number;
  message: string;
  data?: any;
}

interface AgentProgressProps {
  events: AgentEvent[];
  isComplete: boolean;
}

export default function AgentProgress({ events, isComplete }: AgentProgressProps) {
  const [activeAgent, setActiveAgent] = useState<Agent | null>(null);
  const [completedAgents, setCompletedAgents] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [totalSteps, setTotalSteps] = useState(5);
  const [messages, setMessages] = useState<{ agent: Agent; message: string; isComplete: boolean }[]>([]);
  
  useEffect(() => {
    if (events.length === 0) return;
    
    const lastEvent = events[events.length - 1];
    
    if (lastEvent.type === 'agent_start' && lastEvent.agent) {
      setActiveAgent(lastEvent.agent);
      setCurrentStep(lastEvent.step || 0);
      setTotalSteps(lastEvent.total_steps || 5);
      setMessages(prev => [...prev, { 
        agent: lastEvent.agent!, 
        message: lastEvent.message, 
        isComplete: false 
      }]);
    }
    
    if (lastEvent.type === 'agent_complete' && lastEvent.agent) {
      setCompletedAgents(prev => [...prev, lastEvent.agent!.id]);
      setMessages(prev => {
        const newMessages = [...prev];
        const lastIdx = newMessages.length - 1;
        if (lastIdx >= 0 && newMessages[lastIdx].agent.id === lastEvent.agent!.id) {
          newMessages[lastIdx] = {
            ...newMessages[lastIdx],
            message: lastEvent.message,
            isComplete: true
          };
        }
        return newMessages;
      });
    }
  }, [events]);
  
  const progress = (currentStep / totalSteps) * 100;
  
  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-6 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-white font-semibold flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            {!isComplete && (
              <>
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </>
            )}
            {isComplete && (
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            )}
          </span>
          {isComplete ? 'Tamamlandı!' : 'AI Ekibi Çalışıyor...'}
        </h3>
        <span className="text-gray-400 text-sm">
          {currentStep}/{totalSteps} adım
        </span>
      </div>
      
      {/* Progress Bar */}
      <div className="relative h-2 bg-gray-700 rounded-full mb-6 overflow-hidden">
        <div 
          className="absolute h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        />
        <div 
          className="absolute h-full bg-white/20 rounded-full animate-pulse"
          style={{ width: `${progress}%` }}
        />
      </div>
      
      {/* Active Agent Card */}
      {activeAgent && !isComplete && (
        <div 
          className="mb-6 p-4 rounded-xl border-2 transition-all duration-300"
          style={{ 
            borderColor: activeAgent.color,
            backgroundColor: `${activeAgent.color}15`
          }}
        >
          <div className="flex items-start gap-4">
            {/* Avatar */}
            <div 
              className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl shadow-lg animate-bounce"
              style={{ backgroundColor: `${activeAgent.color}30` }}
            >
              {activeAgent.avatar}
            </div>
            
            {/* Info */}
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h4 className="text-white font-bold text-lg">{activeAgent.name}</h4>
                <span className="text-gray-500 text-sm">({activeAgent.name_en})</span>
              </div>
              <p className="text-gray-400 text-sm mt-1">{activeAgent.description}</p>
              
              {/* Tasks Animation */}
              <div className="mt-3 flex flex-wrap gap-2">
                {activeAgent.tasks.map((task, idx) => (
                  <span 
                    key={idx}
                    className="px-2 py-1 bg-white/10 rounded text-xs text-gray-300 animate-pulse"
                    style={{ animationDelay: `${idx * 200}ms` }}
                  >
                    {task}
                  </span>
                ))}
              </div>
            </div>
            
            {/* Spinner */}
            <div className="w-8 h-8">
              <svg className="animate-spin" viewBox="0 0 24 24" fill="none">
                <circle 
                  className="opacity-25" 
                  cx="12" cy="12" r="10" 
                  stroke="currentColor" 
                  strokeWidth="4"
                  style={{ stroke: activeAgent.color }}
                />
                <path 
                  className="opacity-75" 
                  fill={activeAgent.color}
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            </div>
          </div>
        </div>
      )}
      
      {/* Agent Timeline */}
      <div className="space-y-3">
        {messages.map((msg, idx) => (
          <div 
            key={idx}
            className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 ${
              msg.isComplete 
                ? 'bg-gray-800/50' 
                : 'bg-gray-700/30'
            }`}
          >
            {/* Avatar */}
            <div 
              className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl transition-all duration-300 ${
                msg.isComplete ? 'scale-90 opacity-70' : 'scale-100'
              }`}
              style={{ backgroundColor: `${msg.agent.color}30` }}
            >
              {msg.agent.avatar}
            </div>
            
            {/* Message */}
            <div className="flex-1">
              <span className="text-gray-400 text-sm">{msg.agent.name}:</span>
              <span className="text-white text-sm ml-2">{msg.message}</span>
            </div>
            
            {/* Status Icon */}
            <div className="w-6 h-6">
              {msg.isComplete ? (
                <svg className="w-6 h-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <div 
                  className="w-5 h-5 border-2 border-t-transparent rounded-full animate-spin"
                  style={{ borderColor: `${msg.agent.color} transparent transparent transparent` }}
                />
              )}
            </div>
          </div>
        ))}
      </div>
      
      {/* Completion Message */}
      {isComplete && (
        <div className="mt-6 p-4 bg-gradient-to-r from-green-500/20 to-emerald-500/20 rounded-xl border border-green-500/30">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-green-500/30 rounded-xl flex items-center justify-center text-2xl">
              ✅
            </div>
            <div>
              <h4 className="text-green-400 font-bold">Blog Hazır!</h4>
              <p className="text-gray-400 text-sm">Tüm agentlar görevlerini tamamladı.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
