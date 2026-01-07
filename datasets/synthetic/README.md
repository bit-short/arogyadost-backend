# Synthetic Data Generation

## Purpose

Generate synthetic test data for:
- Privacy-safe testing and development
- Edge case scenarios
- Scale testing with large datasets
- ML model training without real patient data

## Generation Scripts

### `generate_users.py`
Creates synthetic user profiles with realistic demographics and health profiles.

### `generate_biomarkers.py`
Generates lab results with:
- Realistic value distributions
- Correlated biomarkers (e.g., high triglycerides with low HDL)
- Temporal trends
- Seasonal variations

### `generate_lifestyle.py`
Creates daily activity, sleep, and nutrition data with:
- Weekly patterns (weekday vs weekend)
- Seasonal variations
- Realistic correlations (exercise → better sleep)

### `generate_interventions.py`
Simulates intervention outcomes with:
- Realistic response curves
- Adherence patterns
- Side effect probabilities

## Usage

```bash
# Generate complete synthetic dataset for N users
python datasets/synthetic/generate_all.py --users 100 --months 12

# Generate specific data type
python datasets/synthetic/generate_biomarkers.py --users 50 --tests-per-user 4

# Generate edge cases
python datasets/synthetic/generate_edge_cases.py
```

## Data Quality

- All synthetic data follows the same schemas as real data
- Statistical distributions match real-world patterns
- Correlations between biomarkers are preserved
- Temporal patterns are realistic

## Privacy

- No real patient data is used
- All identifiers are synthetic
- Safe for sharing and public repositories
