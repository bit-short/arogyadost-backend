#!/usr/bin/env python3
"""
Pre-compute translations for daily routine content.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.translation_service import translation_service
from app.storage.translation_database import translation_db

def main():
    """Pre-compute translations for daily routine content."""
    
    print("🚀 Pre-computing daily routine translations...")
    
    user_id = "user_001_29f"
    
    # Daily routine content from mock_data
    daily_routine_content = {
        # Step names
        "step_morning_stack": "Morning Longevity Stack",
        "step_exercise": "Exercise & Movement", 
        "step_supplements": "Supplements",
        "step_wellness": "Wellness",
        
        # Product names
        "product_vitamin_d3": "Vitamin D3 + K2",
        "product_omega3": "Omega-3 EPA/DHA",
        "product_zone2_cardio": "Zone 2 Cardio",
        "product_resistance": "Resistance Training",
        "product_magnesium": "Magnesium Glycinate",
        "product_omega3_fish": "Omega-3 Fish Oil",
        "product_probiotic": "Probiotic",
        "product_water": "8 Glasses of Water",
        "product_meditation": "10-Min Meditation",
        "product_walk": "30-Minute Walk",
        
        # Product descriptions
        "desc_vitamin_d3": "2000 IU with breakfast for bone health",
        "desc_omega3": "2g daily for cardiovascular health",
        "desc_zone2": "45min at 180-age heart rate",
        "desc_resistance": "3x/week for muscle maintenance",
        "desc_magnesium": "400mg before bed for sleep quality",
        "desc_omega3_fish": "Take 2 capsules daily",
        "desc_probiotic": "Take 1 capsule before bed",
        "desc_water": "Stay hydrated throughout the day",
        "desc_meditation": "Practice mindfulness daily",
        "desc_walk": "2 of 3 completed this week",
    }
    
    try:
        # Pre-compute translations for all content
        translations = {}
        
        for content_key, english_text in daily_routine_content.items():
            lang_translations = {'en': english_text}
            
            # Translate to Hindi and Tamil
            for lang_code in ['hi', 'ta']:
                translated = translation_service.translate_text(english_text, lang_code)
                lang_translations[lang_code] = translated
                print(f"  {content_key} ({lang_code}): {translated[:50]}...")
            
            translations[content_key] = lang_translations
        
        # Store all translations
        translation_db.store_user_translations(
            user_id, 'daily_routine', translations
        )
        
        print(f"\n✅ Pre-computed {len(translations)} routine translations")
        
        # Verify stored translations
        print("\n🔍 Verifying stored translations:")
        for lang_code in ['en', 'hi', 'ta']:
            stored = translation_db.get_user_translations(user_id, 'daily_routine', lang_code)
            print(f"  {lang_code.upper()}: {len(stored)} items stored")
        
        print("\n🎉 Daily routine translation pre-computation completed!")
        
    except Exception as e:
        print(f"\n❌ Error during pre-computation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()