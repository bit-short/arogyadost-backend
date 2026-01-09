#!/usr/bin/env python3
"""
Test script for Amazon Translate integration
Run this to verify translation is working
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.translation_service import translation_service

async def test_translation():
    """Test the translation service with sample supplement data"""
    
    print("🧪 Testing Amazon Translate Integration")
    print("=" * 50)
    
    # Check if translation service is available
    if not translation_service.is_translation_available():
        print("❌ Translation service not available. Check AWS credentials.")
        return False
    
    print("✅ Translation service initialized successfully")
    
    # Test data - supplement information
    test_supplements = [
        "Vitamin D3 + K2",
        "2000 IU with breakfast for bone health",
        "Omega-3 EPA/DHA", 
        "2g daily for cardiovascular health",
        "Magnesium Glycinate",
        "400mg before bed for sleep quality"
    ]
    
    # Test Hindi translation
    print("\n🇮🇳 Testing Hindi Translation:")
    print("-" * 30)
    
    for text in test_supplements:
        try:
            translated = translation_service.translate_text(text, 'hi')
            print(f"EN: {text}")
            print(f"HI: {translated}")
            print()
        except Exception as e:
            print(f"❌ Failed to translate '{text}': {e}")
            return False
    
    # Test Tamil translation
    print("\n🇮🇳 Testing Tamil Translation:")
    print("-" * 30)
    
    for text in test_supplements:
        try:
            translated = translation_service.translate_text(text, 'ta')
            print(f"EN: {text}")
            print(f"TA: {translated}")
            print()
        except Exception as e:
            print(f"❌ Failed to translate '{text}': {e}")
            return False
    
    # Test routine data structure
    print("\n📋 Testing Routine Data Translation:")
    print("-" * 40)
    
    sample_routine = [
        {
            "step": "Morning Longevity Stack",
            "products": [
                {
                    "name": "Vitamin D3 + K2",
                    "description": "2000 IU with breakfast for bone health",
                    "image": "/src/assets/products/vitamins.jpg"
                }
            ]
        }
    ]
    
    # Test translating the routine structure
    translated_routine_hi = []
    for step in sample_routine:
        translated_step = {
            "step": translation_service.translate_text(step["step"], 'hi'),
            "products": []
        }
        
        for product in step["products"]:
            translated_product = {
                "name": translation_service.translate_text(product["name"], 'hi'),
                "description": translation_service.translate_text(product["description"], 'hi'),
                "image": product["image"]
            }
            translated_step["products"].append(translated_product)
        
        translated_routine_hi.append(translated_step)
    
    print("Original routine:")
    print(sample_routine[0])
    print("\nTranslated to Hindi:")
    print(translated_routine_hi[0])
    
    print("\n✅ All translation tests passed!")
    print("\n💡 Usage Tips:")
    print("- Translations are cached to reduce API costs")
    print("- Set Accept-Language header to 'hi' or 'ta' in requests")
    print("- English (en) returns original text without translation")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_translation())
    sys.exit(0 if success else 1)