"""
Translation middleware for FastAPI to handle multilingual support.
Extracts language from Accept-Language header and adds to request state.
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class TranslationMiddleware:
    def __init__(self, app):
        self.app = app
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation files from backend translations directory"""
        translations_dir = Path(__file__).parent / "translations"
        
        if not translations_dir.exists():
            print("⚠️ Translations directory not found, creating with default translations")
            translations_dir.mkdir(exist_ok=True)
            self.create_default_translations(translations_dir)
        
        # Load translation files
        for lang_file in translations_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
                print(f"✅ Loaded translations for {lang_code}")
            except Exception as e:
                print(f"❌ Failed to load translations for {lang_code}: {e}")
    
    def create_default_translations(self, translations_dir: Path):
        """Create default translation files"""
        
        # English (default)
        en_translations = {
            "health": {
                "categories": {
                    "cardiovascular": "Cardiovascular",
                    "metabolic": "Metabolic",
                    "inflammatory": "Inflammatory",
                    "hormonal": "Hormonal",
                    "nutritional": "Nutritional",
                    "lifestyle": "Lifestyle"
                },
                "biomarkers": {
                    "bloodPressure": "Blood Pressure",
                    "cholesterol": "Cholesterol",
                    "bloodSugar": "Blood Sugar",
                    "bmi": "BMI",
                    "heartRate": "Heart Rate"
                },
                "status": {
                    "excellent": "Excellent",
                    "good": "Good",
                    "fair": "Fair",
                    "poor": "Poor",
                    "normal": "Normal",
                    "high": "High",
                    "low": "Low"
                },
                "recommendations": {
                    "exercise": "Regular exercise is recommended",
                    "diet": "Consider dietary improvements",
                    "sleep": "Improve sleep quality",
                    "stress": "Manage stress levels"
                }
            },
            "chat": {
                "greeting": "Hello! I'm your AI health assistant. How can I help you today?",
                "analyzing": "Analyzing your health data...",
                "disclaimer": "This is AI-generated advice. Please consult your doctor for medical decisions."
            }
        }
        
        # Hindi translations
        hi_translations = {
            "health": {
                "categories": {
                    "cardiovascular": "हृदय संबंधी",
                    "metabolic": "चयापचय",
                    "inflammatory": "सूजन संबंधी",
                    "hormonal": "हार्मोनल",
                    "nutritional": "पोषण संबंधी",
                    "lifestyle": "जीवनशैली"
                },
                "biomarkers": {
                    "bloodPressure": "रक्तचाप",
                    "cholesterol": "कोलेस्ट्रॉल",
                    "bloodSugar": "रक्त शर्करा",
                    "bmi": "बीएमआई",
                    "heartRate": "हृदय गति"
                },
                "status": {
                    "excellent": "उत्कृष्ट",
                    "good": "अच्छा",
                    "fair": "ठीक",
                    "poor": "खराब",
                    "normal": "सामान्य",
                    "high": "उच्च",
                    "low": "कम"
                },
                "recommendations": {
                    "exercise": "नियमित व्यायाम की सिफारिश की जाती है",
                    "diet": "आहार में सुधार पर विचार करें",
                    "sleep": "नींद की गुणवत्ता में सुधार करें",
                    "stress": "तनाव के स्तर को प्रबंधित करें"
                }
            },
            "chat": {
                "greeting": "नमस्ते! मैं आपका AI स्वास्थ्य सहायक हूँ। आज मैं आपकी कैसे मदद कर सकता हूँ?",
                "analyzing": "आपके स्वास्थ्य डेटा का विश्लेषण कर रहा हूँ...",
                "disclaimer": "यह AI-जनरेटेड सलाह है। चिकित्सा निर्णयों के लिए कृपया अपने डॉक्टर से सलाह लें।"
            }
        }
        
        # Tamil translations
        ta_translations = {
            "health": {
                "categories": {
                    "cardiovascular": "இதய நோய்",
                    "metabolic": "வளர்சிதை மாற்றம்",
                    "inflammatory": "அழற்சி",
                    "hormonal": "ஹார்மோன்",
                    "nutritional": "ஊட்டச்சத்து",
                    "lifestyle": "வாழ்க்கை முறை"
                },
                "biomarkers": {
                    "bloodPressure": "இரத்த அழுத்தம்",
                    "cholesterol": "கொலஸ்ட்ரால்",
                    "bloodSugar": "இரத்த சர்க்கரை",
                    "bmi": "பிஎம்ஐ",
                    "heartRate": "இதய துடிப்பு"
                },
                "status": {
                    "excellent": "சிறந்த",
                    "good": "நல்ல",
                    "fair": "சரியான",
                    "poor": "மோசமான",
                    "normal": "சாதாரண",
                    "high": "உயர்ந்த",
                    "low": "குறைந்த"
                },
                "recommendations": {
                    "exercise": "வழக்கமான உடற்பயிற்சி பரிந்துரைக்கப்படுகிறது",
                    "diet": "உணவு முறையில் மேம்பாடுகளை கருத்தில் கொள்ளுங்கள்",
                    "sleep": "தூக்கத்தின் தரத்தை மேம்படுத்துங்கள்",
                    "stress": "மன அழுத்த அளவுகளை நிர்வகிக்கவும்"
                }
            },
            "chat": {
                "greeting": "வணக்கம்! நான் உங்கள் AI உடல்நல உதவியாளர். இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?",
                "analyzing": "உங்கள் உடல்நல தரவை பகுப்பாய்வு செய்கிறேன்...",
                "disclaimer": "இது AI-உருவாக்கிய ஆலோசனை. மருத்துவ முடிவுகளுக்கு தயவுசெய்து உங்கள் மருத்துவரை அணுகவும்."
            }
        }
        
        # Save translation files
        translations = {
            'en': en_translations,
            'hi': hi_translations,
            'ta': ta_translations
        }
        
        for lang_code, content in translations.items():
            file_path = translations_dir / f"{lang_code}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"✅ Created default translations for {lang_code}")
    
    def get_language_from_header(self, accept_language: str) -> str:
        """Extract language code from Accept-Language header"""
        if not accept_language:
            return 'en'
        
        # Parse Accept-Language header (e.g., "en-US,en;q=0.9,hi;q=0.8")
        languages = []
        for lang_part in accept_language.split(','):
            lang_part = lang_part.strip()
            if ';' in lang_part:
                lang, quality = lang_part.split(';', 1)
                try:
                    q = float(quality.split('=')[1])
                except:
                    q = 1.0
            else:
                lang, q = lang_part, 1.0
            
            # Extract language code (e.g., "en" from "en-US")
            lang_code = lang.split('-')[0].lower()
            languages.append((lang_code, q))
        
        # Sort by quality score
        languages.sort(key=lambda x: x[1], reverse=True)
        
        # Return first supported language
        for lang_code, _ in languages:
            if lang_code in self.translations:
                return lang_code
        
        return 'en'  # Default fallback
    
    def translate(self, key: str, language: str = 'en', **kwargs) -> str:
        """Translate a key to the specified language"""
        if language not in self.translations:
            language = 'en'
        
        # Navigate nested keys (e.g., "health.categories.cardiovascular")
        keys = key.split('.')
        value = self.translations[language]
        
        try:
            for k in keys:
                value = value[k]
            
            # Handle string formatting if kwargs provided
            if kwargs and isinstance(value, str):
                return value.format(**kwargs)
            
            return value
        except (KeyError, TypeError):
            # Fallback to English if key not found
            if language != 'en':
                return self.translate(key, 'en', **kwargs)
            return key  # Return key itself if not found
    
    async def __call__(self, request: Request, call_next):
        # Extract language from Accept-Language header
        accept_language = request.headers.get('accept-language', '')
        language = self.get_language_from_header(accept_language)
        
        # Add language and translation function to request state
        request.state.language = language
        request.state.translate = lambda key, **kwargs: self.translate(key, language, **kwargs)
        request.state.t = request.state.translate  # Shorthand alias
        
        # Process request
        response = await call_next(request)
        
        # Add language header to response
        if hasattr(response, 'headers'):
            response.headers['Content-Language'] = language
        
        return response

# Helper function to get translation function from request
def get_translator(request: Request):
    """Get translation function from request state"""
    return getattr(request.state, 'translate', lambda key, **kwargs: key)

def get_language(request: Request) -> str:
    """Get current language from request state"""
    return getattr(request.state, 'language', 'en')
