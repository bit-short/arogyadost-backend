# Wearable Device Data

## Schema

High-frequency data from fitness trackers and smartwatches.

```json
{
  "user_id": "string",
  "device_type": "string",       // apple_watch, fitbit, garmin, whoop, oura
  "device_id": "string",
  "sync_timestamp": "ISO8601",
  "data_period": {
    "start": "ISO8601",
    "end": "ISO8601"
  },
  "heart_rate": [
    {
      "timestamp": "ISO8601",
      "bpm": "number",
      "context": "string"        // resting, active, sleeping
    }
  ],
  "heart_rate_variability": [
    {
      "timestamp": "ISO8601",
      "hrv_ms": "number",
      "measurement_type": "string" // sdnn, rmssd
    }
  ],
  "activity": {
    "steps": "number",
    "distance_meters": "number",
    "floors_climbed": "number",
    "active_calories": "number",
    "total_calories": "number",
    "active_minutes": {
      "light": "number",
      "moderate": "number",
      "vigorous": "number"
    }
  },
  "sleep": {
    "sleep_score": "number",
    "total_sleep_minutes": "number",
    "sleep_stages": [
      {
        "stage": "string",       // awake, light, deep, rem
        "start": "ISO8601",
        "end": "ISO8601",
        "duration_minutes": "number"
      }
    ],
    "sleep_efficiency": "number",
    "restlessness": "number",
    "respiratory_rate": "number"
  },
  "stress": {
    "stress_score": "number",    // 0-100
    "recovery_score": "number",  // 0-100
    "readiness_score": "number"  // 0-100
  },
  "spo2": [
    {
      "timestamp": "ISO8601",
      "percentage": "number"
    }
  ],
  "skin_temperature": [
    {
      "timestamp": "ISO8601",
      "temperature_c": "number",
      "deviation_from_baseline": "number"
    }
  ],
  "vo2_max": {
    "value": "number",
    "unit": "string",            // mL/kg/min
    "estimated_date": "ISO8601",
    "fitness_age": "number"
  }
}
```

## Files

- `wearables_<user_id>_<YYYY-MM-DD>.json` - Daily device data
- `wearables_aggregated.csv` - Summary statistics
