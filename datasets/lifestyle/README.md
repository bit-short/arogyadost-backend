# Lifestyle Data

## Schema

Daily tracking data for activity, sleep, diet, and stress.

```json
{
  "user_id": "string",
  "date": "ISO8601",
  "activity": {
    "steps": "number",
    "distance_km": "number",
    "active_minutes": "number",
    "calories_burned": "number",
    "exercise_sessions": [
      {
        "type": "string",        // running, cycling, strength, yoga, etc.
        "duration_minutes": "number",
        "intensity": "string",   // low, moderate, high
        "calories": "number"
      }
    ]
  },
  "sleep": {
    "duration_hours": "number",
    "quality_score": "number",   // 0-100
    "deep_sleep_hours": "number",
    "rem_sleep_hours": "number",
    "light_sleep_hours": "number",
    "awake_time_hours": "number",
    "sleep_start": "ISO8601",
    "sleep_end": "ISO8601"
  },
  "nutrition": {
    "calories_consumed": "number",
    "protein_g": "number",
    "carbs_g": "number",
    "fat_g": "number",
    "fiber_g": "number",
    "water_ml": "number",
    "meals": [
      {
        "type": "string",        // breakfast, lunch, dinner, snack
        "time": "ISO8601",
        "calories": "number",
        "description": "string"
      }
    ]
  },
  "stress": {
    "level": "number",           // 1-10 scale
    "hrv_ms": "number",          // Heart rate variability
    "resting_hr": "number",
    "meditation_minutes": "number",
    "notes": "string"
  },
  "vitals": {
    "weight_kg": "number",
    "body_fat_percentage": "number",
    "blood_pressure": {
      "systolic": "number",
      "diastolic": "number"
    },
    "resting_heart_rate": "number",
    "body_temperature_c": "number"
  }
}
```

## Files

- `lifestyle_<user_id>_<YYYY-MM>.json` - Monthly data per user
- `lifestyle_summary.csv` - Aggregated statistics
