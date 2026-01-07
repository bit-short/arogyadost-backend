# Biomarker Data

## Schema

Structured biomarker data extracted and normalized from OCR results.

```json
{
  "user_id": "string",
  "test_date": "ISO8601",
  "lab_name": "string",
  "test_package": "string",
  "biomarkers": {
    "metabolic": {
      "fasting_glucose": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "hba1c": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    },
    "lipid_profile": {
      "total_cholesterol": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "hdl": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "ldl": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "triglycerides": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "vldl": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    },
    "vitamins": {
      "vitamin_d": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "vitamin_b12": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    },
    "hormones": {
      "testosterone": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "fsh": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "lh": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "prolactin": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "tsh": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "t3": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "t4": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    },
    "kidney_function": {
      "creatinine": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "bun": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "egfr": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "uric_acid": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    },
    "liver_function": {
      "sgot": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "sgpt": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "alkaline_phosphatase": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "bilirubin_total": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "ggt": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    },
    "complete_blood_count": {
      "wbc": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "rbc": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "hemoglobin": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "hematocrit": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "platelet_count": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    },
    "minerals": {
      "iron": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "calcium": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "sodium": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"},
      "chloride": {"value": "number", "unit": "string", "ref_range": "string", "status": "string"}
    }
  },
  "interpretation": {
    "critical_values": ["string"],
    "out_of_range": ["string"],
    "trends": ["string"]
  }
}
```

## Status Values

- `normal` - Within reference range
- `low` - Below reference range
- `high` - Above reference range
- `critical` - Critically out of range

## Files

- `biomarkers_<user_id>.json` - Individual user biomarker history
- `biomarkers_all.json` - All users combined
- `biomarkers_timeseries.csv` - Time series format for trend analysis
