/**
 * Simple API service for Telugu Story Generator
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:12000/api/v1';

export interface StoryRequest {
  prompt: string;
  genre: string;
  characters: string[];
  setting: string;
  theme: string;
  max_length: number;
  temperature: number;
  top_p: number;
  top_k: number;
}

export interface TaskResponse {
  task_id: string;
  status: string;
  message: string;
}

export interface StoryResponse {
  story: string;
  metadata: {
    word_count: number;
    estimated_reading_time: number;
    genre: string;
    characters: string[];
    setting: string;
    theme: string;
    language: string;
    cultural_elements: string[];
    generation_time: number;
  };
  success: boolean;
  error?: string;
}

export interface EmotionResponse {
  emotions: Record<string, number>;
  sentiment: {
    label: string;
    confidence: number;
    positive_score: number;
    negative_score: number;
    neutral_score: number;
  };
  cultural_emotions: Record<string, any>;
  success: boolean;
  error?: string;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async generateStory(request: StoryRequest): Promise<TaskResponse> {
    const response = await fetch(`${this.baseUrl}/stories/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getStoryTask(taskId: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/stories/task/${taskId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getStoryGenres(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/stories/genres`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getStoryThemes(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/stories/themes`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getStorySettings(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/stories/settings`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async analyzeEmotions(text: string): Promise<EmotionResponse> {
    const response = await fetch(`${this.baseUrl}/emotions/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text, analysis_type: 'comprehensive', cultural_context: true }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getAgentStatistics(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/agents/statistics`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getAgentStatus(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/agents/status`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getTeluguFestivals(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/cultural/festivals`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getActiveWorkflows(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/workflows/active`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getHealthCheck(): Promise<any> {
    const response = await fetch(`${this.baseUrl.replace('/api/v1', '')}/health`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export const apiService = new ApiService();
export default apiService;