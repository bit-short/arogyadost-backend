# User Profile Data

## Schema

```json
{
  "user_id": "string",           // Format: test_user_<n>_<age><gender>
  "demographics": {
    "age": "number",
    "gender": "string",          // M, F, Other
    "location": {
      "city": "string",
      "country": "string"
    }
  },
  "health_profile": {
    "height_cm": "number",
    "weight_kg": "number",
    "bmi": "number",
    "blood_type": "string",
    "biological_age": "number"   // Estimated
  },
  "goals": [
    {
      "goal_id": "string",
      "type": "string",            // longevity, weight_loss, fitness, etc.
      "target": "string",
      "start_date": "ISO8601",
      "target_date": "ISO8601",
      "status": "string"           // active, completed, abandoned
    }
  ],
  "preferences": {
    "units": "string",             // metric, imperial
    "notifications": "boolean",
    "data_sharing": "boolean"
  },
  "created_at": "ISO8601",
  "last_active": "ISO8601"
}
```

## Files

- `users.json` - All user profiles
- `users.csv` - Tabular format for analysis
