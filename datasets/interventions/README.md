# Health Interventions and Outcomes

## Schema

Track interventions (supplements, lifestyle changes, medications) and their outcomes.

```json
{
  "user_id": "string",
  "intervention_id": "string",
  "intervention_type": "string",  // supplement, medication, lifestyle, diet, exercise
  "name": "string",
  "description": "string",
  "start_date": "ISO8601",
  "end_date": "ISO8601",
  "status": "string",             // active, completed, discontinued
  "protocol": {
    "dosage": "string",
    "frequency": "string",
    "timing": "string",
    "duration_planned": "string"
  },
  "target_biomarkers": [
    {
      "biomarker": "string",
      "baseline_value": "number",
      "target_value": "number",
      "unit": "string"
    }
  ],
  "outcomes": [
    {
      "measurement_date": "ISO8601",
      "biomarker": "string",
      "value": "number",
      "unit": "string",
      "change_from_baseline": "number",
      "change_percentage": "number"
    }
  ],
  "adherence": {
    "compliance_rate": "number",  // 0-100
    "missed_doses": "number",
    "notes": "string"
  },
  "side_effects": [
    {
      "date": "ISO8601",
      "description": "string",
      "severity": "string"
    }
  ],
  "subjective_outcomes": [
    {
      "date": "ISO8601",
      "metric": "string",          // energy, mood, sleep_quality, etc.
      "score": "number",           // 1-10 scale
      "notes": "string"
    }
  ],
  "cost": {
    "monthly_cost": "number",
    "currency": "string"
  }
}
```

## Files

- `interventions_<user_id>.json` - All interventions for a user
- `outcomes_analysis.csv` - Effectiveness analysis across users
