# API Endpoints

This document describes the API endpoints for the AI Emotional Engine for Telugu Story Creation.

## Base URL

All API endpoints are prefixed with `/api/v1`.

## Authentication

Authentication is not currently implemented. In a production environment, API keys or OAuth2 should be used.

## Endpoints

### Generate Story

Generate a story based on provided parameters.

**URL**: `/stories`

**Method**: `POST`

**Request Body**:

```json
{
  "parameters": {
    "length": 5000,
    "genre": "drama",
    "emotional_arc": "family_restoration",
    "characters": [
      {
        "name": "రాజు",
        "age": 30,
        "traits": ["brave", "loyal", "impulsive"],
        "background": "Born in coastal village, left to city for work"
      },
      {
        "name": "లక్ష్మి",
        "age": 28,
        "traits": ["intelligent", "determined", "compassionate"],
        "background": "Teacher from rural background"
      }
    ],
    "setting": {
      "location": "Coastal Andhra Pradesh",
      "time_period": "Contemporary",
      "social_context": "Rural fishing community"
    },
    "theme": "Family reconciliation after long separation",
    "language_style": "Simple and direct with regional dialect"
  }
}
```

**Response**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Family reconciliation after long separation - A drama Story",
  "content": "# Family reconciliation after long separation\n\n## Scene 1: Exposition\n\nThis scene represents the exposition of the story.\n\n...",
  "metadata": {
    "word_count": 5123,
    "generation_time": 12.34,
    "parameters": {
      "length": 5000,
      "genre": "drama",
      "emotional_arc": "family_restoration",
      "characters": [...],
      "setting": {...},
      "theme": "Family reconciliation after long separation",
      "language_style": "Simple and direct with regional dialect"
    }
  }
}
```

**Status Codes**:

- `200 OK`: Story generated successfully
- `400 Bad Request`: Invalid parameters
- `500 Internal Server Error`: Server error

### Health Check

Check the health of the API server.

**URL**: `/health`

**Method**: `GET`

**Response**:

```json
{
  "status": "healthy"
}
```

**Status Codes**:

- `200 OK`: Server is healthy

## Request Parameters

### Story Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| length | integer | Yes | Story length in words (100-10000) |
| genre | string | Yes | Story genre (drama, comedy, thriller, romance, etc.) |
| emotional_arc | string | No | Emotional arc of the story |
| characters | array | Yes | Array of character objects |
| setting | object | Yes | Setting information |
| theme | string | Yes | Main theme of the story |
| language_style | string | No | Language style for the story |

### Character Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Character name |
| age | integer | Yes | Character age |
| traits | array | Yes | Array of character traits |
| background | string | No | Character background |

### Setting Object

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| location | string | Yes | Story location |
| time_period | string | Yes | Time period of the story |
| social_context | string | No | Social context of the setting |

## Error Handling

Errors are returned in the following format:

```json
{
  "detail": "Error message"
}
```

Common error messages:

- `"Missing required parameter: [parameter]"`: A required parameter is missing
- `"Story length must be between 100 and 10000 words"`: Invalid story length
- `"At least one character must be defined"`: No characters provided