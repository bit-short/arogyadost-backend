# AI Interactions Data

## Schema

Chat history, recommendations, and AI-generated insights.

```json
{
  "user_id": "string",
  "session_id": "string",
  "timestamp": "ISO8601",
  "interaction_type": "string",  // chat, recommendation, insight, alert
  "context": {
    "trigger": "string",         // user_query, biomarker_upload, scheduled_check
    "related_data": ["string"]   // References to biomarkers, goals, etc.
  },
  "messages": [
    {
      "role": "string",          // user, assistant
      "content": "string",
      "timestamp": "ISO8601",
      "metadata": {
        "biomarkers_referenced": ["string"],
        "recommendations_made": ["string"],
        "sources_cited": ["string"]
      }
    }
  ],
  "recommendations": [
    {
      "recommendation_id": "string",
      "category": "string",      // supplement, lifestyle, medical_consultation
      "priority": "string",      // high, medium, low
      "title": "string",
      "description": "string",
      "rationale": "string",
      "evidence_level": "string", // strong, moderate, limited
      "action_items": ["string"],
      "status": "string",        // pending, accepted, declined, completed
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    }
  ],
  "insights": [
    {
      "insight_id": "string",
      "type": "string",          // trend, correlation, risk_factor
      "title": "string",
      "description": "string",
      "confidence": "number",    // 0-1
      "supporting_data": ["string"],
      "created_at": "ISO8601"
    }
  ]
}
```

## Files

- `interactions_<user_id>_<session_id>.json` - Individual chat sessions
- `recommendations_summary.json` - All recommendations across users
- `insights_generated.json` - AI-generated insights
