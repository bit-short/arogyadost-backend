# AI/ML Test Datasets

This directory contains structured test datasets for AI/ML experiments on the Aarogyadost health platform.

## Directory Structure

```
datasets/
├── users/                    # User profile and demographic data
├── biomarkers/              # Lab results and biomarker data
├── lifestyle/               # Activity, sleep, diet tracking
├── medical_history/         # Conditions, medications, family history
├── wearables/              # Device data (steps, heart rate, etc.)
├── ai_interactions/        # Chat history and recommendations
├── interventions/          # Health goals and outcomes
└── synthetic/              # Generated synthetic data for testing
```

## Data Sources

- **OCR Results**: Imported from `test_users/ocr_results/`
- **Manual Entry**: Curated test cases for edge scenarios
- **Synthetic**: Generated data for privacy and scale

## Usage

Each subdirectory contains:
- JSON files with structured data
- CSV files for tabular data
- README with schema documentation
- Sample queries and use cases

## Privacy

All data is anonymized with:
- Redacted PII (names, addresses, phone numbers)
- Synthetic identifiers (user_id format: `test_user_<number>_<age><gender>`)
- No real patient information
