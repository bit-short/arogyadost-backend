# Design Document: API Internationalization

## Overview

This design document outlines the implementation of multi-language support (English, Hindi, Tamil) for the Aarogyadost health application API. The solution uses a middleware-based approach with JSON translation files, ensuring backward compatibility while providing comprehensive localization of user-facing content.

The design prioritizes performance through in-memory caching, maintainability through structured translation files, and developer experience through clear APIs and comprehensive fallback mechanisms.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│  Client Request │
│  (Accept-Lang)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Language Detection     │
│  Middleware             │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  API Route Handler      │
│  (Business Logic)       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Response Formatter     │
│  (Translation Service)  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Localized Response     │
│  (JSON with locale)     │
└─────────────────────────┘
```

### Component Interaction

1. **Language Detection Middleware**: Intercepts requests, extracts language preference from headers/query params
2. **Translation Service**: Loads and caches translations, provides lookup with fallback
3. **Response Formatter**: Transforms API responses by replacing translatable strings
4. **Locale Context**: Thread-local storage for current request's locale

## Components and Interfaces

### 1. Translation Service

**Purpose**: Manage translation data and provide efficient lookup

**Location**: `app/services/i18n/translation_service.py`

```python
class TranslationService:
    """
    Manages translation data for multiple locales.
    Loads translations at startup and provides efficient lookup.
    """
    
    def __init__(self, translations_dir: str = "app/translations"):
        self.translations_dir = translations_dir
        self.translations: Dict[str, Dict[str, str]] = {}
        self.supported_locales = ["en-IN", "hi-IN", "ta-IN"]
        self.default_locale = "en-IN"
        
    def load_translations(self) -> None:
        """Load all translation files into memory"""
        
    def get_translation(self, key: str, locale: str, **kwargs) -> str:
        """
        Get translation for a key in specified locale.
        Falls back to English if key not found.
        Supports variable interpolation.
        """
        
    def translate_dict(self, data: Dict, locale: str, keys_to_translate: List[str]) -> Dict:
        """
        Recursively translate specified keys in a dictionary.
        Preserves structure and non-translatable fields.
        """
        
    def is_supported_locale(self, locale: str) -> bool:
        """Check if locale is supported"""
        
    def get_best_match_locale(self, accept_language: str) -> str:
        """Parse Accept-Language header and return best matching locale"""
```

### 2. Language Detection Middleware

**Purpose**: Extract language preference from requests

**Location**: `app/middleware/language_middleware.py`

```python
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar

# Thread-safe context variable for current locale
current_locale: ContextVar[str] = ContextVar('current_locale', default='en-IN')

class LanguageMiddleware(BaseHTTPMiddleware):
    """
    Middleware to detect and set language preference for each request.
    Priority: query param > Accept-Language header > default
    """
    
    async def dispatch(self, request: Request, call_next):
        # 1. Check query parameter
        locale = request.query_params.get('lang')
        
        # 2. Check Accept-Language header
        if not locale:
            accept_language = request.headers.get('Accept-Language', '')
            locale = translation_service.get_best_match_locale(accept_language)
        
        # 3. Validate and set locale
        if not translation_service.is_supported_locale(locale):
            locale = translation_service.default_locale
            
        # Set in context for this request
        token = current_locale.set(locale)
        
        try:
            response = await call_next(request)
            # Add locale to response headers
            response.headers['Content-Language'] = locale
            return response
        finally:
            current_locale.reset(token)
```

### 3. Response Formatter

**Purpose**: Transform API responses with localized content

**Location**: `app/services/i18n/response_formatter.py`

```python
class ResponseFormatter:
    """
    Formats API responses with localized content.
    Handles different response types and preserves structure.
    """
    
    def __init__(self, translation_service: TranslationService):
        self.translation_service = translation_service
        
    def format_health_categories(self, categories: List[Dict], locale: str) -> List[Dict]:
        """Translate health category names and status"""
        
    def format_recommendations(self, recommendations: List[Dict], locale: str) -> List[Dict]:
        """Translate recommendation titles, categories, and reasons"""
        
    def format_biomarker_details(self, biomarker: Dict, locale: str) -> Dict:
        """Translate biomarker names and recommendations"""
        
    def format_error_message(self, error: Dict, locale: str) -> Dict:
        """Translate error messages"""
        
    def add_locale_metadata(self, response: Dict, locale: str) -> Dict:
        """Add locale information to response"""
```

### 4. Localization Decorator

**Purpose**: Simplify applying localization to route handlers

**Location**: `app/services/i18n/decorators.py`

```python
from functools import wraps

def localized_response(response_type: str):
    """
    Decorator to automatically localize API responses.
    
    Usage:
        @localized_response('health_categories')
        async def get_biomarkers():
            return data
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current locale from context
            locale = current_locale.get()
            
            # Call original function
            result = await func(*args, **kwargs)
            
            # Format response based on type
            formatter = ResponseFormatter(translation_service)
            if response_type == 'health_categories':
                result = formatter.format_health_categories(result, locale)
            elif response_type == 'recommendations':
                result = formatter.format_recommendations(result, locale)
            # ... other types
            
            # Add locale metadata
            if isinstance(result, dict):
                result = formatter.add_locale_metadata(result, locale)
                
            return result
        return wrapper
    return decorator
```

## Data Models

### Translation File Structure

**Location**: `app/translations/{locale}.json`

```json
{
  "health_categories": {
    "metabolic": "Metabolic Health",
    "cardiovascular": "Heart Health",
    "hormonal": "Hormonal Balance",
    "inflammation": "Inflammation Markers",
    "liver": "Liver Function",
    "kidney": "Kidney Function"
  },
  "status": {
    "good": "Good",
    "excellent": "Excellent",
    "attention": "Needs Attention",
    "borderline": "Borderline",
    "low": "Low",
    "normal": "Normal",
    "deficient": "Deficient"
  },
  "recommendations": {
    "categories": {
      "fitness": "Fitness",
      "lifestyle": "Lifestyle",
      "nutrition": "Nutrition"
    },
    "priority": {
      "high": "High Priority",
      "medium": "Medium Priority",
      "low": "Low Priority"
    }
  },
  "biomarkers": {
    "hba1c": "HbA1c",
    "total_cholesterol": "Total Cholesterol",
    "hdl": "HDL Cholesterol",
    "ldl": "LDL Cholesterol",
    "triglycerides": "Triglycerides",
    "vitamin_d": "Vitamin D",
    "vitamin_b12": "Vitamin B12",
    "crp": "C-Reactive Protein",
    "testosterone": "Testosterone",
    "vo2_max": "VO2 Max",
    "resting_hr": "Resting Heart Rate",
    "grip_strength": "Grip Strength",
    "body_fat": "Body Fat Percentage",
    "muscle_mass": "Muscle Mass",
    "bone_density": "Bone Density T-Score"
  },
  "errors": {
    "not_found": "Resource not found",
    "invalid_request": "Invalid request",
    "server_error": "Internal server error",
    "unauthorized": "Unauthorized access"
  },
  "common": {
    "age": "Age",
    "value": "Value",
    "unit": "Unit",
    "status": "Status",
    "optimal": "Optimal",
    "date": "Date",
    "trend": "Trend"
  }
}
```

### Hindi Translation Example (`hi-IN.json`)

```json
{
  "health_categories": {
    "metabolic": "चयापचय स्वास्थ्य",
    "cardiovascular": "हृदय स्वास्थ्य",
    "hormonal": "हार्मोनल संतुलन",
    "inflammation": "सूजन संकेतक",
    "liver": "यकृत कार्य",
    "kidney": "गुर्दे का कार्य"
  },
  "status": {
    "good": "अच्छा",
    "excellent": "उत्कृष्ट",
    "attention": "ध्यान देने की आवश्यकता",
    "borderline": "सीमा रेखा",
    "low": "कम",
    "normal": "सामान्य",
    "deficient": "कमी"
  }
}
```

### Tamil Translation Example (`ta-IN.json`)

```json
{
  "health_categories": {
    "metabolic": "வளர்சிதை மாற்ற ஆரோக்கியம்",
    "cardiovascular": "இதய ஆரோக்கியம்",
    "hormonal": "ஹார்மோன் சமநிலை",
    "inflammation": "வீக்க குறிப்பான்கள்",
    "liver": "கல்லீரல் செயல்பாடு",
    "kidney": "சிறுநீரக செயல்பாடு"
  },
  "status": {
    "good": "நல்லது",
    "excellent": "சிறந்தது",
    "attention": "கவனம் தேவை",
    "borderline": "எல்லைக்கோடு",
    "low": "குறைவு",
    "normal": "இயல்பானது",
    "deficient": "பற்றாக்குறை"
  }
}
```

### Response Format with Locale

```json
{
  "locale": "hi-IN",
  "data": {
    "id": "metabolic",
    "name": "चयापचय स्वास्थ्य",
    "status": "अच्छा",
    "score": 82
  }
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Locale Support Completeness
*For any* supported locale (en-IN, hi-IN, ta-IN), the translation service should be able to retrieve translations for that locale and return valid translation data.
**Validates: Requirements 1.1**

### Property 2: Unsupported Locale Fallback
*For any* unsupported or invalid locale string, the system should default to English (en-IN) for all API responses.
**Validates: Requirements 1.3, 2.3**

### Property 3: Medical Terminology Preservation
*For any* medical term without standard translation (HbA1c, VO2 Max, etc.), the value should remain identical across all supported locales.
**Validates: Requirements 1.5**

### Property 4: Accept-Language Header Parsing
*For any* valid Accept-Language header string, the system should correctly parse it and select the highest priority supported language.
**Validates: Requirements 2.1, 2.2**

### Property 5: Query Parameter Precedence
*For any* combination of Accept-Language header and lang query parameter, the query parameter should always take precedence in locale selection.
**Validates: Requirements 2.5**

### Property 6: Response Translation Completeness
*For any* API response containing translatable content (health categories, recommendations, biomarkers, errors), all translatable fields should be translated to the requested locale while preserving non-translatable fields.
**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

### Property 7: Numeric and Date Preservation
*For any* API response, numeric values, dates, timestamps, and medical codes should remain identical across all supported locales.
**Validates: Requirements 3.5**

### Property 8: Translation Fallback Consistency
*For any* missing translation key in a non-English locale, the system should return the English translation for that key.
**Validates: Requirements 4.2**

### Property 9: Backward Compatibility
*For any* existing API endpoint called without language specification, the response should be in English and maintain the original response structure.
**Validates: Requirements 5.2**

### Property 10: Locale Metadata Inclusion
*For any* API response when language is specified, the response should include a locale field indicating the language used.
**Validates: Requirements 6.3**

### Property 11: Response Structure Invariance
*For any* API endpoint and request data, the response structure (keys, nesting, data types) should be identical across all supported locales, with only values changing.
**Validates: Requirements 6.5**

### Property 12: Translation File Key Consistency
*For any* translation key present in the English translation file, that key should exist in all other locale translation files (Hindi and Tamil).
**Validates: Requirements 9.3**

## Error Handling

### Translation Errors

**Missing Translation Keys**:
- Log warning with key name and locale
- Fall back to English translation
- Continue processing without throwing exception
- Include fallback indicator in development mode

**Invalid Locale Format**:
- Log warning with invalid locale string
- Default to English (en-IN)
- Continue processing normally
- Return valid response with default locale

**Translation File Loading Errors**:
- Log error with file path and error details
- Attempt to load English translations as minimum
- If English fails, raise startup exception
- Prevent application from starting with no translations

### API Request Errors

**Malformed Accept-Language Header**:
- Parse what's possible
- Default to English for unparseable parts
- Log warning in development mode
- Continue with best-effort locale selection

**Invalid Query Parameter**:
- Treat as unsupported locale
- Default to English
- Log warning
- Continue processing

### Response Formatting Errors

**Translation Service Unavailable**:
- Return untranslated response
- Log critical error
- Add error indicator to response metadata
- Ensure API remains functional

**Circular Reference in Translation**:
- Detect during translation file validation
- Log error with key path
- Use fallback translation
- Prevent infinite loops

## Testing Strategy

### Unit Tests

Unit tests will verify specific examples and edge cases for the internationalization system:

**Translation Service Tests**:
- Test loading translations from JSON files
- Test translation lookup with valid keys
- Test fallback to English for missing keys
- Test locale validation and normalization
- Test variable interpolation in translations

**Language Middleware Tests**:
- Test Accept-Language header parsing
- Test query parameter extraction
- Test locale precedence rules
- Test context variable setting
- Test response header addition

**Response Formatter Tests**:
- Test formatting health categories
- Test formatting recommendations
- Test formatting biomarker details
- Test formatting error messages
- Test preservation of non-translatable fields

**Edge Cases**:
- Empty Accept-Language header
- Malformed Accept-Language header
- Missing translation files
- Empty translation files
- Circular translation references

### Property-Based Tests

Property-based tests will verify universal properties across all inputs using the Hypothesis library (as specified in the tech stack). Each test will run a minimum of 100 iterations.

**Property Test Configuration**:
- Library: Hypothesis (Python)
- Minimum iterations: 100 per test
- Random seed: Configurable for reproducibility
- Shrinking: Enabled for minimal failing examples

**Test Implementation**:

```python
from hypothesis import given, strategies as st
import pytest

# Property 1: Locale Support Completeness
@given(locale=st.sampled_from(['en-IN', 'hi-IN', 'ta-IN']))
def test_supported_locale_has_translations(locale):
    """
    Feature: api-internationalization, Property 1: Locale Support Completeness
    For any supported locale, translations should be available
    """
    translations = translation_service.get_translations(locale)
    assert translations is not None
    assert len(translations) > 0
    assert 'health_categories' in translations

# Property 2: Unsupported Locale Fallback
@given(locale=st.text().filter(lambda x: x not in ['en-IN', 'hi-IN', 'ta-IN']))
def test_unsupported_locale_defaults_to_english(locale):
    """
    Feature: api-internationalization, Property 2: Unsupported Locale Fallback
    For any unsupported locale, system should default to English
    """
    result_locale = translation_service.get_best_match_locale(locale)
    assert result_locale == 'en-IN'

# Property 3: Medical Terminology Preservation
@given(
    medical_term=st.sampled_from(['HbA1c', 'VO2 Max', 'LDL', 'HDL', 'BMI']),
    locale=st.sampled_from(['en-IN', 'hi-IN', 'ta-IN'])
)
def test_medical_terms_not_translated(medical_term, locale):
    """
    Feature: api-internationalization, Property 3: Medical Terminology Preservation
    For any medical term, value should be identical across locales
    """
    # Medical terms should not have translations
    translation = translation_service.get_translation(
        f'medical_terms.{medical_term}', 
        locale
    )
    # Should return the original term (fallback to key)
    assert medical_term in translation

# Property 7: Numeric and Date Preservation
@given(
    numeric_value=st.floats(min_value=0, max_value=1000),
    locale=st.sampled_from(['en-IN', 'hi-IN', 'ta-IN'])
)
def test_numeric_values_preserved(numeric_value, locale):
    """
    Feature: api-internationalization, Property 7: Numeric and Date Preservation
    For any numeric value, it should remain unchanged across locales
    """
    response = {'value': numeric_value, 'name': 'test_metric'}
    formatted = response_formatter.format_health_metric(response, locale)
    assert formatted['value'] == numeric_value

# Property 11: Response Structure Invariance
@given(
    locale1=st.sampled_from(['en-IN', 'hi-IN', 'ta-IN']),
    locale2=st.sampled_from(['en-IN', 'hi-IN', 'ta-IN'])
)
def test_response_structure_identical_across_locales(locale1, locale2):
    """
    Feature: api-internationalization, Property 11: Response Structure Invariance
    For any endpoint, response structure should be identical across locales
    """
    # Get same data in two different locales
    response1 = response_formatter.format_health_categories(mock_data, locale1)
    response2 = response_formatter.format_health_categories(mock_data, locale2)
    
    # Structure should be identical
    assert response1.keys() == response2.keys()
    assert type(response1) == type(response2)
    if isinstance(response1, list):
        assert len(response1) == len(response2)
```

**Additional Property Tests**:
- Property 4: Accept-Language header parsing with random valid headers
- Property 5: Query parameter precedence with random combinations
- Property 6: Response translation completeness with random API responses
- Property 8: Translation fallback with random missing keys
- Property 10: Locale metadata inclusion with random requests
- Property 12: Translation file key consistency across all locales

### Integration Tests

Integration tests will verify end-to-end functionality:

**API Endpoint Tests**:
- Test each major endpoint with all three locales
- Verify Accept-Language header handling
- Verify lang query parameter handling
- Verify response structure and content
- Verify locale metadata in responses

**Middleware Integration**:
- Test middleware with various request patterns
- Verify context variable propagation
- Verify response header addition
- Test error handling in middleware

**Translation File Validation**:
- Validate all translation files are valid JSON
- Verify key consistency across locales
- Check for missing translations
- Validate translation file structure

### Test Data

**Sample Translation Keys**:
```python
SAMPLE_KEYS = [
    'health_categories.metabolic',
    'health_categories.cardiovascular',
    'status.good',
    'status.excellent',
    'recommendations.categories.fitness',
    'biomarkers.hba1c',
    'errors.not_found'
]
```

**Sample API Responses**:
```python
SAMPLE_HEALTH_CATEGORY = {
    'id': 'metabolic',
    'name': 'Metabolic Health',
    'status': 'good',
    'score': 82
}

SAMPLE_RECOMMENDATION = {
    'id': 1,
    'title': 'Start Zone 2 cardio training',
    'category': 'fitness',
    'priority': 'high',
    'reason': 'Improve mitochondrial function'
}
```

### Test Coverage Goals

- Unit test coverage: >90% for i18n components
- Property test coverage: All 12 correctness properties
- Integration test coverage: All major API endpoints
- Edge case coverage: All identified error conditions

### Continuous Testing

- Run unit tests on every commit
- Run property tests in CI/CD pipeline
- Run integration tests before deployment
- Monitor translation coverage in production
- Alert on missing translation keys
