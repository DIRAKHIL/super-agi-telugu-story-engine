# API Endpoints Specification
## Production-Ready Telugu Story Engine API - Complete REST & WebSocket Documentation

### Overview

This document provides comprehensive API specifications for the Super AGI Telugu Story Engine. All endpoints are production-ready, support real AI processing (no mocks), and handle Tinglish (Telugu in English script) content seamlessly.

**Base URL**: `https://api.telugu-story-engine.com/v1`
**WebSocket URL**: `wss://api.telugu-story-engine.com/ws`

---

## Authentication & Security

### API Key Authentication
```http
Authorization: Bearer <api_key>
Content-Type: application/json
X-API-Version: 1.0
```

### Rate Limiting
- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1000 requests/hour  
- **Enterprise**: Unlimited

---

## Core Story Generation Endpoints

### 1. Generate Complete Story

**Endpoint**: `POST /stories/generate`

**Description**: Generate a complete Telugu story using multi-agent AI system with real-time processing.

**Request Body**:
```json
{
  "prompt": "Oru chinna village lo oka brave boy story cheppu",
  "genre": "adventure",
  "length": "medium",
  "cultural_context": {
    "region": "andhra_pradesh",
    "time_period": "contemporary",
    "mythology_elements": ["ramayana", "local_legends"],
    "social_themes": ["family_values", "courage", "friendship"]
  },
  "emotional_arc": {
    "primary_emotion": "courage",
    "intensity_curve": "hero_journey",
    "cultural_emotions": ["vatsalya", "veera", "bhakti"]
  },
  "style_preferences": {
    "narrative_voice": "third_person",
    "dialogue_style": "conversational_tinglish",
    "description_level": "detailed",
    "humor_level": "moderate"
  },
  "constraints": {
    "max_characters": 5,
    "target_audience": "family",
    "content_rating": "U",
    "avoid_themes": ["violence", "adult_content"]
  }
}
```

**Response**:
```json
{
  "story_id": "story_12345",
  "status": "completed",
  "generation_time": 12.5,
  "story": {
    "title": "Ramu - The Village Hero",
    "content": {
      "opening": "Oka chinna village lo, Ramu ane oka 12 years boy undedi...",
      "development": "Ramu ki telisindi village lo oka pedda problem undi ani...",
      "climax": "Finally, Ramu decided to face the challenge with full courage...",
      "resolution": "Village people antha Ramu ni hero la celebrate chesaru..."
    },
    "characters": [
      {
        "name": "Ramu",
        "role": "protagonist",
        "personality": "brave, kind-hearted, intelligent",
        "cultural_archetype": "dharmic_hero"
      }
    ],
    "scenes": [
      {
        "scene_number": 1,
        "setting": "Village square",
        "emotional_tone": "peaceful",
        "cultural_elements": ["traditional_gathering", "elder_respect"]
      }
    ]
  },
  "quality_metrics": {
    "coherence_score": 0.94,
    "cultural_authenticity": 0.91,
    "emotional_impact": 0.88,
    "creativity_score": 0.85,
    "language_quality": 0.92
  },
  "emotional_analysis": {
    "primary_emotions": {
      "courage": 0.85,
      "compassion": 0.72,
      "determination": 0.78
    },
    "cultural_emotions": {
      "veera": 0.88,
      "dharma": 0.75,
      "vatsalya": 0.65
    },
    "emotional_arc_quality": 0.89
  },
  "cultural_analysis": {
    "mythology_integration": 0.82,
    "social_context_accuracy": 0.91,
    "linguistic_authenticity": 0.87,
    "regional_specificity": 0.85
  }
}
```

**Error Responses**:
```json
{
  "error": {
    "code": "INVALID_PROMPT",
    "message": "Prompt must be at least 10 characters long",
    "details": "Received prompt with 5 characters"
  }
}
```

### 2. Interactive Story Generation

**Endpoint**: `POST /stories/interactive`

**Description**: Start an interactive story session with real-time collaboration between user and AI agents.

**Request Body**:
```json
{
  "session_id": "session_abc123",
  "initial_prompt": "Oka mysterious forest lo adventure story start cheyyi",
  "interaction_mode": "collaborative",
  "user_preferences": {
    "decision_points": true,
    "character_customization": true,
    "plot_suggestions": true
  }
}
```

**Response**:
```json
{
  "session_id": "session_abc123",
  "story_segment": {
    "content": "Deep forest lo, sunlight barely trees madhya nundi vasthundi. Meeku oka strange sound vinipisthundi...",
    "current_scene": "forest_entrance",
    "emotional_state": "mysterious_anticipation"
  },
  "decision_points": [
    {
      "id": "decision_1",
      "question": "Ee sound follow cheyala leda safe place ki velala?",
      "options": [
        {
          "id": "follow_sound",
          "text": "Sound follow cheyyi - adventure ki ready",
          "consequences": "high_risk_high_reward"
        },
        {
          "id": "find_shelter",
          "text": "Safe place find cheyyi - careful approach",
          "consequences": "low_risk_steady_progress"
        }
      ]
    }
  ],
  "character_status": {
    "protagonist": {
      "name": "Hero",
      "current_emotion": "curious",
      "energy_level": 0.85,
      "skills": ["observation", "courage"]
    }
  },
  "next_action": "await_user_decision"
}
```

### 3. Story Enhancement

**Endpoint**: `PUT /stories/{story_id}/enhance`

**Description**: Enhance an existing story with improved cultural authenticity, emotional depth, or narrative structure.

**Request Body**:
```json
{
  "enhancement_type": "cultural_depth",
  "focus_areas": [
    "mythology_integration",
    "regional_dialects",
    "traditional_values"
  ],
  "target_improvements": {
    "cultural_authenticity": 0.95,
    "emotional_resonance": 0.90,
    "narrative_coherence": 0.92
  }
}
```

**Response**:
```json
{
  "story_id": "story_12345",
  "enhancement_status": "completed",
  "processing_time": 8.2,
  "improvements": {
    "cultural_authenticity": {
      "before": 0.78,
      "after": 0.94,
      "improvement": 0.16
    },
    "mythology_integration": {
      "added_elements": [
        "Hanuman reference in courage scene",
        "Dharmic values in decision making",
        "Traditional blessing ceremony"
      ]
    }
  },
  "enhanced_content": {
    "modified_scenes": [2, 5, 8],
    "added_cultural_elements": 12,
    "improved_dialogue_segments": 7
  }
}
```

---

## Character Development Endpoints

### 4. Create Character Profile

**Endpoint**: `POST /characters/create`

**Request Body**:
```json
{
  "character_name": "Lakshmi",
  "role": "supporting_character",
  "cultural_background": {
    "region": "telangana",
    "social_class": "middle_class",
    "education": "college_graduate",
    "family_structure": "joint_family"
  },
  "personality_traits": {
    "primary": ["intelligent", "compassionate", "determined"],
    "secondary": ["humorous", "traditional", "modern_thinking"]
  },
  "character_arc": {
    "starting_point": "shy_village_girl",
    "transformation": "confident_leader",
    "growth_catalyst": "family_crisis"
  },
  "dialogue_style": {
    "formality_level": "moderate",
    "tinglish_ratio": 0.7,
    "cultural_expressions": true,
    "humor_style": "situational"
  }
}
```

**Response**:
```json
{
  "character_id": "char_lakshmi_001",
  "profile": {
    "name": "Lakshmi",
    "detailed_background": {
      "age": 24,
      "occupation": "Software Engineer",
      "hometown": "Warangal",
      "family": "Lives with parents and younger brother",
      "education": "B.Tech from JNTU"
    },
    "personality_analysis": {
      "mbti_type": "ENFJ",
      "cultural_archetype": "modern_traditional_balance",
      "core_values": ["family", "education", "social_responsibility"],
      "fears": ["disappointing_family", "losing_cultural_identity"],
      "motivations": ["career_success", "family_happiness", "social_change"]
    },
    "dialogue_patterns": {
      "sample_phrases": [
        "Amma, nenu cheppina vinava?",
        "Office lo work pressure chaala ekkuva undi",
        "Traditional values ni maintain cheyali, but modern thinking kuda important"
      ],
      "speech_characteristics": {
        "uses_telugu_honorifics": true,
        "code_switches_naturally": true,
        "cultural_references": "frequent"
      }
    }
  },
  "ai_model_training": {
    "character_consistency_score": 0.92,
    "cultural_accuracy": 0.89,
    "dialogue_authenticity": 0.91
  }
}
```

### 5. Character Interaction Simulation

**Endpoint**: `POST /characters/interact`

**Request Body**:
```json
{
  "characters": ["char_ramu_001", "char_lakshmi_001"],
  "scenario": {
    "setting": "college_campus",
    "situation": "first_meeting",
    "emotional_context": "nervous_excitement",
    "cultural_context": "traditional_family_backgrounds"
  },
  "interaction_goals": [
    "establish_friendship",
    "show_personality_contrast",
    "cultural_bonding"
  ]
}
```

**Response**:
```json
{
  "interaction_id": "interact_001",
  "dialogue": [
    {
      "character": "Ramu",
      "text": "Hi, nenu Ramu. Meeru kotha student aa?",
      "emotion": "friendly_curiosity",
      "cultural_notes": "Polite introduction with Telugu greeting"
    },
    {
      "character": "Lakshmi",
      "text": "Namaste, nenu Lakshmi. Haan, today first day. Meeru which branch?",
      "emotion": "polite_nervousness",
      "cultural_notes": "Traditional greeting followed by English mixing"
    }
  ],
  "interaction_analysis": {
    "cultural_authenticity": 0.94,
    "character_consistency": 0.91,
    "emotional_believability": 0.88,
    "dialogue_naturalness": 0.92
  }
}
```

---

## Cultural Intelligence Endpoints

### 6. Cultural Validation

**Endpoint**: `POST /cultural/validate`

**Request Body**:
```json
{
  "content": "Ramu temple ki velli Ganesha ni pray chesadu before exam",
  "validation_criteria": {
    "mythology_accuracy": true,
    "social_customs": true,
    "religious_practices": true,
    "regional_specificity": true
  },
  "target_region": "andhra_pradesh"
}
```

**Response**:
```json
{
  "validation_id": "val_001",
  "overall_score": 0.87,
  "detailed_analysis": {
    "mythology_accuracy": {
      "score": 0.92,
      "notes": "Ganesha worship before exams is culturally accurate",
      "suggestions": []
    },
    "social_customs": {
      "score": 0.85,
      "notes": "Temple visit pattern matches regional customs",
      "suggestions": ["Consider adding family blessing element"]
    },
    "language_authenticity": {
      "score": 0.84,
      "notes": "Natural Tinglish mixing",
      "suggestions": ["'pray chesadu' could be 'prayer chesadu' for better flow"]
    }
  },
  "cultural_flags": [],
  "enhancement_suggestions": [
    "Add traditional blessing gesture",
    "Include family involvement in prayer",
    "Mention specific prayer or mantra"
  ]
}
```

### 7. Mythology Integration

**Endpoint**: `POST /cultural/mythology/integrate`

**Request Body**:
```json
{
  "story_context": "Hero facing difficult decision",
  "mythology_source": "ramayana",
  "integration_style": "subtle_reference",
  "character_knowledge_level": "moderate",
  "target_lesson": "dharmic_decision_making"
}
```

**Response**:
```json
{
  "integration_id": "myth_001",
  "suggested_integration": {
    "reference_type": "character_reflection",
    "content": "Ramu ki Rama yudham lo Vibhishana situation gurthochindi. Right thing cheyali, even if it's difficult ani decide chesadu.",
    "cultural_context": "Vibhishana's moral dilemma parallels modern ethical decisions",
    "educational_value": "Teaches dharmic decision-making through familiar mythology"
  },
  "alternative_integrations": [
    {
      "reference": "Arjuna's dilemma in Kurukshetra",
      "application": "When facing family conflict"
    },
    {
      "reference": "Hanuman's devotion",
      "application": "When showing loyalty to friends"
    }
  ],
  "cultural_impact_score": 0.91
}
```

---

## Emotional Intelligence Endpoints

### 8. Emotional Arc Analysis

**Endpoint**: `POST /emotional/analyze-arc`

**Request Body**:
```json
{
  "story_content": "Complete story text here...",
  "analysis_depth": "comprehensive",
  "cultural_context": "telugu_cinema_style",
  "target_emotions": ["courage", "family_love", "triumph"]
}
```

**Response**:
```json
{
  "analysis_id": "emotion_001",
  "emotional_arc": {
    "overall_trajectory": "hero_journey_with_family_values",
    "arc_quality_score": 0.89,
    "emotional_peaks": [
      {
        "scene": 3,
        "emotion": "determination",
        "intensity": 0.85,
        "cultural_resonance": 0.78
      },
      {
        "scene": 7,
        "emotion": "family_pride",
        "intensity": 0.92,
        "cultural_resonance": 0.94
      }
    ]
  },
  "emotion_distribution": {
    "primary_emotions": {
      "courage": 0.82,
      "love": 0.75,
      "determination": 0.78,
      "joy": 0.71
    },
    "cultural_emotions": {
      "vatsalya": 0.88,
      "veera": 0.85,
      "bhakti": 0.62,
      "karuna": 0.58
    }
  },
  "audience_impact_prediction": {
    "engagement_score": 0.87,
    "emotional_satisfaction": 0.84,
    "cultural_connection": 0.91,
    "memorability": 0.79
  },
  "improvement_suggestions": [
    {
      "scene": 5,
      "suggestion": "Increase emotional intensity during family conflict",
      "expected_impact": "Better audience connection"
    }
  ]
}
```

### 9. Emotional Enhancement

**Endpoint**: `PUT /emotional/enhance`

**Request Body**:
```json
{
  "content": "Story segment to enhance...",
  "target_emotion": "family_bonding",
  "intensity_level": 0.85,
  "cultural_style": "telugu_family_values",
  "enhancement_approach": "subtle_deepening"
}
```

**Response**:
```json
{
  "enhancement_id": "enhance_001",
  "enhanced_content": "Enhanced story segment with deeper emotional resonance...",
  "emotional_improvements": {
    "before_score": 0.67,
    "after_score": 0.85,
    "improvement": 0.18
  },
  "techniques_applied": [
    "Added sensory details for emotional connection",
    "Included cultural family traditions",
    "Enhanced dialogue with emotional subtext",
    "Added internal character reflection"
  ],
  "cultural_authenticity": 0.92
}
```

---

## Real-Time WebSocket Endpoints

### 10. Live Story Generation

**WebSocket**: `/ws/stories/live-generate`

**Connection**:
```javascript
const ws = new WebSocket('wss://api.telugu-story-engine.com/ws/stories/live-generate');

// Send generation request
ws.send(JSON.stringify({
  type: 'start_generation',
  prompt: 'Oka adventure story cheppu',
  preferences: {
    real_time_feedback: true,
    interactive_decisions: true
  }
}));

// Receive real-time updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'generation_progress':
      console.log(`Progress: ${data.percentage}%`);
      break;
    case 'story_chunk':
      console.log('New content:', data.content);
      break;
    case 'decision_point':
      console.log('User decision needed:', data.options);
      break;
    case 'generation_complete':
      console.log('Story completed:', data.final_story);
      break;
  }
};
```

**Message Types**:

**Generation Progress**:
```json
{
  "type": "generation_progress",
  "percentage": 45,
  "current_stage": "character_development",
  "estimated_completion": "30 seconds",
  "agent_status": {
    "master_storyteller": "active",
    "emotional_architect": "processing",
    "cultural_consultant": "ready"
  }
}
```

**Story Chunk**:
```json
{
  "type": "story_chunk",
  "chunk_id": "chunk_001",
  "content": "Ramu slowly walked towards the mysterious cave...",
  "emotional_tone": "suspenseful",
  "cultural_elements": ["traditional_courage", "family_values"],
  "next_expected": "character_decision"
}
```

**Decision Point**:
```json
{
  "type": "decision_point",
  "decision_id": "dec_001",
  "context": "Ramu reached the cave entrance",
  "question": "What should Ramu do next?",
  "options": [
    {
      "id": "enter_cave",
      "text": "Cave lo enter avvu - brave ga",
      "emotional_impact": "high_courage",
      "risk_level": "high"
    },
    {
      "id": "call_friends",
      "text": "Friends ni call cheyyi - safe approach",
      "emotional_impact": "friendship_values",
      "risk_level": "low"
    }
  ],
  "timeout": 30
}
```

### 11. Collaborative Story Session

**WebSocket**: `/ws/stories/collaborate`

**Multi-user story creation with real-time synchronization**:

```javascript
// Join collaborative session
ws.send(JSON.stringify({
  type: 'join_session',
  session_id: 'collab_123',
  user_id: 'user_456',
  role: 'contributor'
}));

// Contribute to story
ws.send(JSON.stringify({
  type: 'contribute',
  content: 'Suddenly, Lakshmi appeared with a solution...',
  contribution_type: 'plot_development',
  character_focus: 'lakshmi'
}));

// Receive collaboration updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'contribution_accepted') {
    console.log('Your contribution was integrated');
  } else if (data.type === 'story_updated') {
    console.log('Story updated by another user');
  }
};
```

---

## Analytics & Monitoring Endpoints

### 12. Story Performance Analytics

**Endpoint**: `GET /analytics/stories/{story_id}/performance`

**Response**:
```json
{
  "story_id": "story_12345",
  "performance_metrics": {
    "user_engagement": {
      "completion_rate": 0.87,
      "average_reading_time": 420,
      "user_ratings": {
        "average": 4.3,
        "distribution": {
          "5_star": 45,
          "4_star": 32,
          "3_star": 18,
          "2_star": 4,
          "1_star": 1
        }
      }
    },
    "cultural_impact": {
      "authenticity_feedback": 0.91,
      "cultural_learning_value": 0.84,
      "mythology_appreciation": 0.78
    },
    "emotional_resonance": {
      "emotional_satisfaction": 0.86,
      "character_connection": 0.82,
      "memorable_moments": 7
    }
  },
  "user_feedback": [
    {
      "user_id": "user_789",
      "rating": 5,
      "comment": "Chaala bagundi! Cultural elements perfect ga integrate chesaru",
      "emotional_response": "highly_satisfied"
    }
  ]
}
```

### 13. System Health Monitoring

**Endpoint**: `GET /monitoring/health`

**Response**:
```json
{
  "system_status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "ai_models": {
    "llama_33_70b": {
      "status": "active",
      "response_time": 1.2,
      "memory_usage": "45GB",
      "gpu_utilization": 0.78
    },
    "mistral_7b": {
      "status": "active",
      "response_time": 0.8,
      "memory_usage": "12GB",
      "gpu_utilization": 0.45
    }
  },
  "performance_metrics": {
    "requests_per_second": 45,
    "average_response_time": 2.1,
    "error_rate": 0.002,
    "uptime": "99.97%"
  },
  "cultural_intelligence": {
    "accuracy_score": 0.91,
    "mythology_database_status": "updated",
    "regional_context_coverage": 0.94
  }
}
```

---

## Error Handling & Status Codes

### HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Invalid API key
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - AI models temporarily unavailable

### Error Response Format

```json
{
  "error": {
    "code": "CULTURAL_VALIDATION_FAILED",
    "message": "Content contains culturally inappropriate elements",
    "details": {
      "flagged_elements": [
        "Inappropriate religious reference",
        "Cultural stereotype"
      ],
      "suggestions": [
        "Use respectful religious language",
        "Avoid generalizations about communities"
      ]
    },
    "request_id": "req_12345",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## SDK & Integration Examples

### Python SDK Example

```python
from telugu_story_engine import TeluguStoryAPI

# Initialize client
client = TeluguStoryAPI(api_key="your_api_key")

# Generate story
story = client.generate_story(
    prompt="Oka village lo hero story cheppu",
    genre="adventure",
    cultural_context={
        "region": "andhra_pradesh",
        "mythology_elements": ["ramayana"]
    }
)

print(f"Generated story: {story.content}")
print(f"Cultural score: {story.cultural_analysis.authenticity}")
```

### JavaScript SDK Example

```javascript
import { TeluguStoryEngine } from 'telugu-story-engine-js';

const client = new TeluguStoryEngine({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.telugu-story-engine.com/v1'
});

// Generate interactive story
const session = await client.startInteractiveStory({
  prompt: 'Oka mystery story start cheyyi',
  interactionMode: 'collaborative'
});

// Handle real-time updates
session.onStoryChunk((chunk) => {
  console.log('New content:', chunk.content);
});

session.onDecisionPoint((decision) => {
  // Present options to user
  console.log('Decision needed:', decision.question);
});
```

This comprehensive API specification provides all the endpoints needed for a production-ready Telugu story generation system with real AI processing, cultural intelligence, and emotional depth - all supporting Tinglish content seamlessly.