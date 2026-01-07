# Design Document: Test Dataset Generator

## Overview

The Test Dataset Generator creates a comprehensive, structured dataset of health profiles for AI/ML experimentation. It combines 3 real users from existing OCR-extracted data with at least 10 synthetically generated users, producing clean, parseable data without PDFs or raw OCR text. The system normalizes biomarker data, validates quality, and exports in multiple formats (JSON, CSV, pandas DataFrame).

## Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                   Test Dataset Generator                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │   Ground     │      │  Synthetic   │                     │
│  │   Truth      │──┐   │    User      │                     │
│  │   Parser     │  │   │  Generator   │                     │
│  └──────────────┘  │   └──────────────┘                     │
│                    │           │                             │
│                    └───────────┼─────────────┐               │
│                                │             │               │
│                        ┌───────▼─────────┐   │               │
│                        │   Biomarker     │   │               │
│                        │   Normalizer    │   │               │
│                        └───────┬─────────┘   │               │
│                                │             │               │
│                        ┌───────▼─────────┐   │               │
│                        │  User Profile   │   │               │
│                        │   Builder       │   │               │
│                        └───────┬─────────┘   │               │
│                                │             │               │
│                        ┌───────▼─────────┐   │               │
│                        │  Data Quality   │   │               │
│                        │   Validator     │   │               │
│                        └───────┬─────────┘   │               │
│                                │             │               │
│                        ┌───────▼─────────┐   │               │
│                        │    Dataset      │   │               │
│                        │    Exporter     │   │               │
│                        └─────────────────┘   │               │
│                                               │               │
└───────────────────────────────────────────────┼───────────────┘
                                                │
                                                ▼
                                    ┌───────────────────────┐
                                    │  Output Files:        │
                                    │  - test_dataset.json  │
                                    │  - test_dataset.csv   │
                                    │  - test_dataset.pkl   │
                                    │  - data_quality.json  │
                                    │  - schema.json        │
                                    └───────────────────────┘
```

### Component Responsibilities

1. **Ground Truth Parser**: Reads existing ground_truth_dataset.json and extracts real user data
2. **Synthetic User Generator**: Creates realistic test users with demographics and biomarkers
3. **Biomarker Normalizer**: Standardizes test names, units, and reference ranges
4. **User Profile Builder**: Aggregates biomarkers and metadata into structured profiles
5. **Data Quality Validator**: Checks completeness, outliers, and data consistency
6. **Dataset Exporter**: Writes output in multiple formats with schema documentation

## Components and Interfaces

### 1. Ground Truth Parser

**Purpose**: Parse existing OCR-extracted data from ground_truth_dataset.json

**Interface**:
```python
class GroundTruthParser:
    def parse_file(self, filepath: str) -> List[RawUserData]:
        """Parse ground truth JSON file and extract user data."""
        pass
    
    def extract_demographics(self, user_id: str) -> Demographics:
        """Extract age, gender, name from user identifier like '29F Amanpreet'."""
        pass
    
    def extract_biomarkers(self, report_data: dict) -> List[RawBiomarker]:
        """Extract biomarker list from report data."""
        pass
```

**Data Structures**:
```python
@dataclass
class RawUserData:
    user_id: str  # e.g., "29F Amanpreet"
    demographics: Demographics
    reports: List[ReportData]

@dataclass
class Demographics:
    age: int
    gender: str  # "M" or "F"
    name: str

@dataclass
class ReportData:
    filename: str
    report_date: Optional[date]
    biomarkers: List[RawBiomarker]

@dataclass
class RawBiomarker:
    test_name: str
    value: float
    unit: Optional[str]
    reference_range: Optional[str]
    raw_text: str
```

### 2. Synthetic User Generator

**Purpose**: Generate realistic test users with varied health profiles

**Interface**:
```python
class SyntheticUserGenerator:
    def generate_users(self, count: int, seed: Optional[int] = None) -> List[SyntheticUser]:
        """Generate specified number of synthetic users."""
        pass
    
    def generate_demographics(self) -> Demographics:
        """Generate realistic age, gender, name."""
        pass
    
    def generate_health_profile(self, demographics: Demographics) -> HealthProfile:
        """Generate biomarkers based on health profile type."""
        pass
    
    def generate_biomarker_value(self, test_name: str, profile: HealthProfile) -> float:
        """Generate realistic biomarker value for given health profile."""
        pass
```

**Health Profile Types**:
- Healthy: All biomarkers within normal ranges
- Pre-diabetic: Elevated HbA1c (5.7-6.4%), borderline glucose
- High Cholesterol: Elevated LDL, total cholesterol
- Thyroid Issues: Abnormal TSH, T3, T4
- Vitamin Deficiency: Low Vitamin D, B12
- Mixed: Combination of multiple conditions

**Biomarker Correlations**:
- High triglycerides → Low HDL
- High HbA1c → High fasting glucose
- Low Vitamin D → Low calcium
- High TSH → Low T4 (hypothyroid)

### 3. Biomarker Normalizer

**Purpose**: Standardize biomarker data to consistent format

**Interface**:
```python
class BiomarkerNormalizer:
    def normalize_test_name(self, raw_name: str) -> str:
        """Map raw test name to canonical form."""
        pass
    
    def normalize_unit(self, value: float, unit: str, test_name: str) -> Tuple[float, str]:
        """Convert to standard unit if needed."""
        pass
    
    def parse_reference_range(self, range_str: str) -> ReferenceRange:
        """Parse reference range string to min/max values."""
        pass
    
    def validate_value(self, value: float, test_name: str) -> ValidationResult:
        """Check if value is medically plausible."""
        pass
```

**Canonical Test Names**:
```python
CANONICAL_NAMES = {
    "HbA1c": ["HbA1c", "Hemoglobin A1c", "Glycated Hemoglobin"],
    "Fasting Glucose": ["Fasting Blood Sugar", "FBS", "Glucose Fasting"],
    "Total Cholesterol": ["Cholesterol Total", "Total Cholesterol", "CHOL"],
    "HDL Cholesterol": ["HDL", "HDL-C", "High Density Lipoprotein"],
    "LDL Cholesterol": ["LDL", "LDL-C", "Low Density Lipoprotein"],
    "Triglycerides": ["Triglycerides", "TRIG", "TG"],
    "TSH": ["TSH", "Thyroid Stimulating Hormone", "TSH Ultrasensitive"],
    "Vitamin D": ["25-OH Vitamin D", "Vitamin D Total", "Vitamin D"],
    "Vitamin B12": ["Vitamin B12", "B12", "Cobalamin"],
    # ... more mappings
}
```

**Standard Units**:
```python
STANDARD_UNITS = {
    "HbA1c": "%",
    "Fasting Glucose": "mg/dL",
    "Total Cholesterol": "mg/dL",
    "HDL Cholesterol": "mg/dL",
    "LDL Cholesterol": "mg/dL",
    "Triglycerides": "mg/dL",
    "TSH": "µIU/mL",
    "Vitamin D": "ng/mL",
    "Vitamin B12": "pg/mL",
    # ... more mappings
}
```

### 4. User Profile Builder

**Purpose**: Aggregate biomarkers and metadata into structured user profiles

**Interface**:
```python
class UserProfileBuilder:
    def build_profile(self, user_data: Union[RawUserData, SyntheticUser]) -> UserProfile:
        """Create structured user profile."""
        pass
    
    def aggregate_biomarkers(self, reports: List[ReportData]) -> Dict[str, List[BiomarkerReading]]:
        """Group biomarkers by test name across reports."""
        pass
    
    def generate_user_id(self, demographics: Demographics, is_synthetic: bool) -> str:
        """Generate unique user ID."""
        pass
```

**Data Structures**:
```python
@dataclass
class UserProfile:
    user_id: str  # e.g., "USER_001", "USER_SYNTH_001"
    is_synthetic: bool
    demographics: Demographics
    biomarkers: Dict[str, List[BiomarkerReading]]  # test_name -> readings
    metadata: ProfileMetadata

@dataclass
class BiomarkerReading:
    test_name: str  # Canonical name
    value: float
    unit: str  # Standard unit
    reference_range: ReferenceRange
    report_date: date
    source_filename: Optional[str]  # For real data
    validation_status: ValidationStatus

@dataclass
class ReferenceRange:
    min_value: Optional[float]
    max_value: Optional[float]
    text: str  # Original text like "< 100" or "70-100"

@dataclass
class ProfileMetadata:
    created_at: datetime
    source: str  # "ground_truth" or "synthetic"
    health_profile_type: Optional[str]  # For synthetic users
    report_count: int
    biomarker_count: int
```

### 5. Data Quality Validator

**Purpose**: Validate data quality and generate metrics

**Interface**:
```python
class DataQualityValidator:
    def validate_dataset(self, profiles: List[UserProfile]) -> DataQualityReport:
        """Validate entire dataset and generate report."""
        pass
    
    def check_completeness(self, profile: UserProfile) -> CompletenessMetrics:
        """Calculate biomarker coverage for user."""
        pass
    
    def detect_outliers(self, profile: UserProfile) -> List[OutlierAlert]:
        """Identify biomarker values outside reference ranges."""
        pass
    
    def detect_duplicates(self, profiles: List[UserProfile]) -> List[DuplicateAlert]:
        """Find duplicate users or biomarker readings."""
        pass
```

**Data Structures**:
```python
@dataclass
class DataQualityReport:
    total_users: int
    real_users: int
    synthetic_users: int
    completeness_metrics: Dict[str, float]  # test_name -> % coverage
    outlier_summary: Dict[str, int]  # test_name -> outlier count
    duplicate_alerts: List[DuplicateAlert]
    warnings: List[str]
    generated_at: datetime

@dataclass
class CompletenessMetrics:
    user_id: str
    total_biomarkers: int
    common_biomarkers_present: int  # Out of standard panel
    completeness_percentage: float

@dataclass
class OutlierAlert:
    user_id: str
    test_name: str
    value: float
    reference_range: ReferenceRange
    severity: str  # "mild", "moderate", "severe"
```

### 6. Dataset Exporter

**Purpose**: Export dataset in multiple formats with schema documentation

**Interface**:
```python
class DatasetExporter:
    def export_json(self, profiles: List[UserProfile], output_path: str) -> None:
        """Export as structured JSON."""
        pass
    
    def export_csv(self, profiles: List[UserProfile], output_path: str) -> None:
        """Export as flattened CSV (one row per biomarker reading)."""
        pass
    
    def export_pickle(self, profiles: List[UserProfile], output_path: str) -> None:
        """Export as pandas DataFrame pickle."""
        pass
    
    def export_schema(self, output_path: str) -> None:
        """Export JSON schema documentation."""
        pass
    
    def export_quality_report(self, report: DataQualityReport, output_path: str) -> None:
        """Export data quality report."""
        pass
```

**Output File Structure**:
```
tests/test_data/ml_dataset/
├── test_dataset.json          # Structured user profiles
├── test_dataset.csv           # Flattened biomarker readings
├── test_dataset.pkl           # Pandas DataFrame
├── data_quality.json          # Quality metrics and validation
├── schema.json                # Data schema documentation
└── README.md                  # Dataset documentation
```

## Data Models

### JSON Output Format

```json
{
  "metadata": {
    "version": "1.0",
    "generated_at": "2026-01-07T10:30:00Z",
    "total_users": 13,
    "real_users": 3,
    "synthetic_users": 10,
    "source_files": ["ground_truth_dataset.json"]
  },
  "users": [
    {
      "user_id": "USER_001",
      "is_synthetic": false,
      "demographics": {
        "age": 29,
        "gender": "F",
        "name": "Amanpreet"
      },
      "biomarkers": {
        "HbA1c": [
          {
            "value": 4.7,
            "unit": "%",
            "reference_range": {
              "min": null,
              "max": 5.7,
              "text": "< 5.7"
            },
            "report_date": "2024-07-26",
            "source_filename": "Amanpreet Kaur_Female_29_2024_7.pdf",
            "validation_status": "normal"
          }
        ],
        "Fasting Glucose": [
          {
            "value": 84.07,
            "unit": "mg/dL",
            "reference_range": {
              "min": 70,
              "max": 100,
              "text": "70-100"
            },
            "report_date": "2024-07-26",
            "source_filename": "Amanpreet Kaur_Female_29_2024_7.pdf",
            "validation_status": "normal"
          }
        ]
      },
      "metadata": {
        "created_at": "2026-01-07T10:30:00Z",
        "source": "ground_truth",
        "report_count": 1,
        "biomarker_count": 45
      }
    },
    {
      "user_id": "USER_SYNTH_001",
      "is_synthetic": true,
      "demographics": {
        "age": 42,
        "gender": "M",
        "name": "Rajesh Kumar"
      },
      "biomarkers": {
        "HbA1c": [
          {
            "value": 6.2,
            "unit": "%",
            "reference_range": {
              "min": null,
              "max": 5.7,
              "text": "< 5.7"
            },
            "report_date": "2025-11-15",
            "source_filename": null,
            "validation_status": "elevated"
          }
        ]
      },
      "metadata": {
        "created_at": "2026-01-07T10:30:00Z",
        "source": "synthetic",
        "health_profile_type": "pre-diabetic",
        "report_count": 1,
        "biomarker_count": 35
      }
    }
  ]
}
```

### CSV Output Format

Flattened format with one row per biomarker reading:

```csv
user_id,is_synthetic,age,gender,name,test_name,value,unit,ref_min,ref_max,ref_text,report_date,source_filename,validation_status,health_profile_type
USER_001,false,29,F,Amanpreet,HbA1c,4.7,%,,5.7,< 5.7,2024-07-26,Amanpreet Kaur_Female_29_2024_7.pdf,normal,
USER_001,false,29,F,Amanpreet,Fasting Glucose,84.07,mg/dL,70,100,70-100,2024-07-26,Amanpreet Kaur_Female_29_2024_7.pdf,normal,
USER_SYNTH_001,true,42,M,Rajesh Kumar,HbA1c,6.2,%,,5.7,< 5.7,2025-11-15,,elevated,pre-diabetic
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Complete User Extraction
*For any* valid ground truth JSON file, parsing should extract all user records present in the file, with no users missing or duplicated.
**Validates: Requirements 1.1**

### Property 2: Demographic Parsing Accuracy
*For any* user identifier string in the format "{age}{gender} {name}", parsing should correctly extract age as an integer, gender as "M" or "F", and name as a string.
**Validates: Requirements 1.2, 3.1**

### Property 3: Report Field Completeness
*For any* report data structure, parsing should extract all required fields (filename, text_length, raw_text, biomarkers array) without omission.
**Validates: Requirements 1.3**

### Property 4: Malformed Input Error Handling
*For any* malformed JSON input (invalid syntax, missing required fields, wrong types), the system should return a descriptive error message rather than crashing or producing invalid output.
**Validates: Requirements 1.4**

### Property 5: Test Name Canonicalization
*For any* variant of a test name (e.g., "HbA1c", "Hemoglobin A1c", "Glycated Hemoglobin"), normalization should map it to the same canonical form.
**Validates: Requirements 2.1**

### Property 6: Biomarker Value Validation
*For any* processed biomarker, the value should be numeric and fall within medically plausible ranges for that test type, with out-of-range values flagged appropriately.
**Validates: Requirements 2.2, 5.2, 7.3**

### Property 7: Unit Standardization
*For any* biomarker with a unit, normalization should convert it to the standard medical unit for that test type (e.g., all glucose values in mg/dL).
**Validates: Requirements 2.3**

### Property 8: Reference Range Parsing
*For any* reference range string (formats like "< 100", "70-100", "> 5", "5-10"), parsing should correctly extract min and/or max values.
**Validates: Requirements 2.4**

### Property 9: Invalid Data Flagging
*For any* biomarker with missing required fields or invalid values, the system should set validation_status to indicate the issue.
**Validates: Requirements 2.5**

### Property 10: Multi-Report Aggregation
*For any* user with multiple reports, the user profile should contain all biomarkers from all reports, with no biomarkers lost during aggregation.
**Validates: Requirements 3.2**

### Property 11: Metadata Preservation
*For any* biomarker reading, the system should preserve source metadata (report_date, source_filename) through all processing stages.
**Validates: Requirements 3.3**

### Property 12: Duplicate Biomarker Preservation
*For any* biomarker that appears in multiple reports for the same user, all instances should be preserved with their respective timestamps, not collapsed into a single value.
**Validates: Requirements 3.4**

### Property 13: User ID Uniqueness
*For any* generated dataset, all user IDs should be unique with no collisions between real and synthetic users.
**Validates: Requirements 3.5**

### Property 14: Export Metadata Completeness
*For any* exported dataset (JSON, CSV, or pickle), the output should include metadata fields (export_date, version, source_files).
**Validates: Requirements 4.4**

### Property 15: Completeness Metric Accuracy
*For any* user profile, the calculated completeness percentage should equal (biomarkers_present / total_expected_biomarkers) * 100.
**Validates: Requirements 5.1**

### Property 16: Duplicate Detection
*For any* dataset with duplicate users or biomarker readings, the validation process should flag all duplicates.
**Validates: Requirements 5.3**

### Property 17: Insufficient Data Warnings
*For any* user with fewer than a threshold number of biomarkers (e.g., < 10), the system should generate a warning about insufficient data for ML training.
**Validates: Requirements 5.5**

### Property 18: Dataset Merge Completeness
*For any* two datasets being merged, the resulting dataset should contain all users from both input datasets.
**Validates: Requirements 6.1**

### Property 19: Merge Duplicate Handling
*For any* merge operation where duplicate users or reports exist, the system should detect them and apply the conflict resolution strategy (preserve most recent).
**Validates: Requirements 6.2, 6.3, 6.4**

### Property 20: Changelog Maintenance
*For any* dataset update operation, an entry should be added to the changelog with timestamp and operation details.
**Validates: Requirements 6.5**

### Property 21: Minimum Synthetic User Count
*For any* synthetic user generation request, the system should produce at least 10 users (or the specified minimum count).
**Validates: Requirements 7.1**

### Property 22: Demographic Constraints
*For any* generated synthetic user, age should be between 18-80, gender should be "M" or "F", and name should be a non-empty string.
**Validates: Requirements 7.2**

### Property 23: Biomarker Correlation Maintenance
*For any* synthetic user with correlated biomarkers (e.g., high triglycerides and low HDL), the correlation should be maintained according to medical relationships.
**Validates: Requirements 7.4**

### Property 24: Health Profile Diversity
*For any* set of generated synthetic users, multiple distinct health profile types should be represented (not all users with the same profile).
**Validates: Requirements 7.5**

### Property 25: Common Biomarker Coverage
*For any* generated synthetic user, the profile should include all biomarkers from the common panel (HbA1c, glucose, lipid panel, thyroid, vitamins, CBC).
**Validates: Requirements 7.6**

### Property 26: Report Date Constraints
*For any* generated synthetic user, all report dates should fall within the last 12 months from the generation date.
**Validates: Requirements 7.7**

### Property 27: Synthetic User Marking
*For any* synthetic user in the dataset, the is_synthetic field should be true, and for any real user, it should be false.
**Validates: Requirements 7.8**

### Property 28: Output File Type Constraints
*For any* dataset export operation, the output directory should contain only structured data files (JSON, CSV, pickle) with no PDF files.
**Validates: Requirements 8.1**

### Property 29: Raw Text Exclusion
*For any* exported dataset, no biomarker records should contain raw_text or raw OCR content fields.
**Validates: Requirements 8.2**

### Property 30: Normalized Data Completeness
*For any* biomarker in the exported dataset, it should have a normalized test name, numeric value, standard unit, and parsed reference range.
**Validates: Requirements 8.3**

## Error Handling

### Input Validation Errors
- **Invalid JSON**: Return clear error message with line number and syntax issue
- **Missing Required Fields**: Specify which fields are missing
- **Invalid Data Types**: Specify expected vs actual type
- **Empty Dataset**: Warn if no users found in input

### Processing Errors
- **Unparseable Demographics**: Log warning, use default values, flag user
- **Unknown Test Names**: Log warning, preserve original name, flag for review
- **Invalid Biomarker Values**: Flag with validation_status, include in quality report
- **Missing Reference Ranges**: Use default ranges for test type, flag as estimated

### Export Errors
- **File Write Failures**: Retry once, then fail with clear error message
- **Disk Space Issues**: Check available space before export, fail early if insufficient
- **Permission Errors**: Provide clear message about required permissions

### Data Quality Issues
- **Outliers**: Flag but don't reject, include in quality report
- **Duplicates**: Detect and report, apply resolution strategy
- **Insufficient Data**: Warn but don't reject, include in quality report
- **Correlation Violations**: Log warning for synthetic data, flag for review

## Testing Strategy

### Unit Tests
- Test demographic parsing with various user identifier formats
- Test reference range parsing with different formats ("< 100", "70-100", "> 5")
- Test canonical name mapping for all known test name variants
- Test unit conversion for common conversions (mmol/L to mg/dL)
- Test error handling for malformed JSON inputs
- Test merge conflict resolution with overlapping users
- Test export format validation (valid JSON, CSV, pickle)

### Property-Based Tests
- **Property 1**: Generate random JSON structures with varying user counts, verify all extracted
- **Property 2**: Generate random user identifier strings, verify correct demographic parsing
- **Property 6**: Generate random biomarker values, verify validation and flagging
- **Property 8**: Generate random reference range strings, verify correct parsing
- **Property 10**: Generate users with random numbers of reports, verify all biomarkers aggregated
- **Property 13**: Generate large datasets, verify all user IDs unique
- **Property 18**: Generate random datasets, merge them, verify completeness
- **Property 21**: Generate synthetic users with various counts, verify minimum met
- **Property 23**: Generate synthetic users, verify biomarker correlations maintained
- **Property 30**: Generate and export datasets, verify all biomarkers normalized

### Integration Tests
- End-to-end test: Parse ground truth → normalize → build profiles → validate → export
- Test with real ground_truth_dataset.json file
- Test synthetic user generation with all health profile types
- Test merge operation with real + synthetic users
- Verify all output files created with correct formats
- Verify data quality report accuracy

### Configuration
- All property-based tests should run minimum 100 iterations
- Each test should reference its design document property number
- Tag format: **Feature: test-dataset-generator, Property {number}: {property_text}**
