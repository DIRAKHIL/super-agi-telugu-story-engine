/**
 * Simple API service for Telugu Story Generator
 */

// Ensure API_BASE_URL is properly set
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://work-1-mdgzgjjgwsxwlxtv.prod-runtime.all-hands.dev/api/v1';
console.log('API_BASE_URL:', API_BASE_URL);

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

export interface EmotionAnalysisRequest {
  text: string;
  analysisType: string;
  culturalContext: boolean;
}

export interface EmotionResponse {
  success: boolean;
  emotions: Record<string, number>;
  sentiment: {
    label: string;
    confidence: number;
    positive_score: number;
    negative_score: number;
    neutral_score: number;
  };
  cultural_elements?: string[];
  metadata?: Record<string, any>;
  error?: string;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
    console.log('ApiService initialized with baseUrl:', this.baseUrl);
    
    // Validate the URL to ensure it's properly formed
    try {
      new URL(this.baseUrl);
    } catch (e) {
      console.error('Invalid API URL:', this.baseUrl);
      // Fallback to a known working URL if the configured one is invalid
      this.baseUrl = 'https://work-1-mdgzgjjgwsxwlxtv.prod-runtime.all-hands.dev/api/v1';
      console.log('Falling back to:', this.baseUrl);
    }
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

  async analyzeEmotions(request: EmotionAnalysisRequest): Promise<EmotionResponse> {
    const response = await fetch(`${this.baseUrl}/emotions/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: request.text,
        analysis_type: request.analysisType,
        cultural_context: request.culturalContext
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
  
  async getSupportedEmotions(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/emotions/supported-emotions`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
  
  async getCulturalContexts(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/emotions/cultural-contexts`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
  
  async analyzeEmotionalArc(text: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/emotions/emotional-arc`, {
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