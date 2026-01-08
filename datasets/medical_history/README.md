# Medical History Data

## Schema

Comprehensive medical history including conditions, medications, allergies, and family history.

```json
{
  "user_id": "string",
  "last_updated": "ISO8601",
  "conditions": [
    {
      "condition_id": "string",
      "name": "string",
      "icd10_code": "string",
      "diagnosed_date": "ISO8601",
      "status": "string",        // active, resolved, managed
      "severity": "string",      // mild, moderate, severe
      "notes": "string"
    }
  ],
  "medications": [
    {
      "medication_id": "string",
      "name": "string",
      "dosage": "string",
      "frequency": "string",
      "start_date": "ISO8601",
      "end_date": "ISO8601",
      "purpose": "string",
      "prescribing_doctor": "string",
      "status": "string"         // active, discontinued
    }
  ],
  "supplements": [
    {
      "supplement_id": "string",
      "name": "string",
      "dosage": "string",
      "frequency": "string",
      "start_date": "ISO8601",
      "purpose": "string"
    }
  ],
  "allergies": [
    {
      "allergen": "string",
      "type": "string",          // drug, food, environmental
      "severity": "string",      // mild, moderate, severe, life-threatening
      "reaction": "string",
      "diagnosed_date": "ISO8601"
    }
  ],
  "surgeries": [
    {
      "procedure": "string",
      "date": "ISO8601",
      "hospital": "string",
      "surgeon": "string",
      "notes": "string"
    }
  ],
  "family_history": [
    {
      "relation": "string",      // parent, sibling, grandparent
      "condition": "string",
      "age_of_onset": "number",
      "notes": "string"
    }
  ],
  "immunizations": [
    {
      "vaccine": "string",
      "date": "ISO8601",
      "next_due": "ISO8601"
    }
  ],
  "lifestyle_factors": {
    "smoking": {
      "status": "string",        // never, former, current
      "packs_per_day": "number",
      "years": "number"
    },
    "alcohol": {
      "status": "string",        // never, occasional, regular
      "drinks_per_week": "number"
    },
    "diet_type": "string",       // omnivore, vegetarian, vegan, etc.
    "exercise_frequency": "string"
  }
}
```

## Files

- `medical_history_<user_id>.json` - Individual medical history
- `family_history_summary.csv` - Aggregated family history patterns
