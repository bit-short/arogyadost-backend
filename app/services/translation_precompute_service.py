"""
Translation Pre-computation Service
Generates and stores translations for user content to avoid real-time translation costs.
"""

import logging
from typing import Dict, List, Optional
from app.services.translation_service import translation_service
from app.storage.translation_database import translation_db

logger = logging.getLogger(__name__)


class TranslationPrecomputeService:
    """Service for pre-computing and storing user content translations."""
    
    def __init__(self):
        self.supported_languages = ['en', 'hi', 'ta']
    
    def precompute_biological_age_translations(self, user_id: str, 
                                             insights: List[str], 
                                             recommendations: List[str]) -> None:
        """
        Pre-compute translations for biological age insights and recommendations.
        
        Args:
            user_id: User identifier
            insights: List of insight texts in English
            recommendations: List of recommendation texts in English
        """
        try:
            # Pre-compute insight translations
            if insights:
                insight_translations = {}
                for i, insight in enumerate(insights):
                    content_key = f"insight_{i}"
                    lang_translations = {'en': insight}  # Original English
                    
                    # Translate to other languages
                    for lang_code in self.supported_languages:
                        if lang_code != 'en':
                            translated = translation_service.translate_text(insight, lang_code)
                            lang_translations[lang_code] = translated
                    
                    insight_translations[content_key] = lang_translations
                
                # Store insight translations
                translation_db.store_user_translations(
                    user_id, 'insights', insight_translations
                )
            
            # Pre-compute recommendation translations
            if recommendations:
                recommendation_translations = {}
                for i, recommendation in enumerate(recommendations):
                    content_key = f"recommendation_{i}"
                    lang_translations = {'en': recommendation}  # Original English
                    
                    # Translate to other languages
                    for lang_code in self.supported_languages:
                        if lang_code != 'en':
                            translated = translation_service.translate_text(recommendation, lang_code)
                            lang_translations[lang_code] = translated
                    
                    recommendation_translations[content_key] = lang_translations
                
                # Store recommendation translations
                translation_db.store_user_translations(
                    user_id, 'recommendations', recommendation_translations
                )
            
            logger.info(f"Pre-computed translations for user {user_id}: "
                       f"{len(insights)} insights, {len(recommendations)} recommendations")
            
        except Exception as e:
            logger.error(f"Failed to pre-compute translations for user {user_id}: {e}")
            # Don't raise - this is a background operation
    
    def get_translated_content(self, user_id: str, content_type: str, 
                             original_content: List[str], language_code: str) -> List[str]:
        """
        Get translated content for a user, falling back to original if not available.
        
        Args:
            user_id: User identifier
            content_type: 'insights' or 'recommendations'
            original_content: Original English content
            language_code: Target language code
            
        Returns:
            List of translated content
        """
        # If requesting English, return original
        if language_code == 'en':
            return original_content
        
        try:
            # Try to get pre-computed translations
            translations = translation_db.get_user_translations(
                user_id, content_type, language_code
            )
            
            if translations:
                # Return translations in order
                translated_content = []
                for i in range(len(original_content)):
                    content_key = f"{content_type[:-1]}_{i}"  # 'insights' -> 'insight_0'
                    if content_key in translations:
                        translated_content.append(translations[content_key])
                    else:
                        # Fallback to original if translation missing
                        translated_content.append(original_content[i])
                
                return translated_content
            
            # If no pre-computed translations, return original content
            logger.warning(f"No pre-computed translations found for user {user_id}, "
                          f"content_type {content_type}, language {language_code}")
            return original_content
            
        except Exception as e:
            logger.error(f"Failed to get translated content for user {user_id}: {e}")
            return original_content
    
    def get_template_content(self, template_keys: List[str], language_code: str) -> List[str]:
        """
        Get translated template content (for users without data).
        
        Args:
            template_keys: List of template keys
            language_code: Target language code
            
        Returns:
            List of translated template content
        """
        if language_code == 'en':
            # Return English templates from database
            templates = translation_db.get_template_translations('en')
            return [templates.get(key, key) for key in template_keys]
        
        try:
            templates = translation_db.get_template_translations(language_code)
            return [templates.get(key, key) for key in template_keys]
            
        except Exception as e:
            logger.error(f"Failed to get template translations for {language_code}: {e}")
            # Fallback to English templates
            templates = translation_db.get_template_translations('en')
            return [templates.get(key, key) for key in template_keys]
    
    def ensure_user_translations_exist(self, user_id: str, insights: List[str], 
                                     recommendations: List[str]) -> None:
        """
        Ensure translations exist for a user, creating them if missing.
        
        Args:
            user_id: User identifier
            insights: Current insights in English
            recommendations: Current recommendations in English
        """
        try:
            # Check if translations already exist
            has_insights = translation_db.has_user_translations(user_id, 'insights')
            has_recommendations = translation_db.has_user_translations(user_id, 'recommendations')
            
            # Pre-compute missing translations
            if not has_insights and insights:
                logger.info(f"Pre-computing insight translations for user {user_id}")
                self.precompute_biological_age_translations(user_id, insights, [])
            
            if not has_recommendations and recommendations:
                logger.info(f"Pre-computing recommendation translations for user {user_id}")
                self.precompute_biological_age_translations(user_id, [], recommendations)
            
        except Exception as e:
            logger.error(f"Failed to ensure translations exist for user {user_id}: {e}")


# Global pre-compute service instance
translation_precompute_service = TranslationPrecomputeService()