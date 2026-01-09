"""
Database-backed translation service for user-specific content
"""

from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
import logging
import hashlib

from app.database import get_db
from app.models.db_models import User, UserTranslation
from app.utils.translation import translation_service

logger = logging.getLogger(__name__)


class DatabaseTranslationService:
    """
    Service for managing user-specific translations stored in database
    """
    
    def __init__(self):
        self.supported_languages = ['en', 'hi', 'ta']
    
    def _generate_content_key(self, content: str, content_type: str) -> str:
        """Generate a unique key for content"""
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
        return f"{content_type}_{content_hash}"
    
    def get_user_translation(
        self, 
        user_id: str, 
        content: str, 
        content_type: str, 
        target_language: str,
        db: Session
    ) -> str:
        """
        Get translation for user content from database or create if not exists
        
        Args:
            user_id: User ID
            content: Original content to translate
            content_type: Type of content (recommendation, insight, etc.)
            target_language: Target language code
            db: Database session
            
        Returns:
            Translated content
        """
        # Return original if English or unsupported language
        if target_language == 'en' or target_language not in self.supported_languages:
            return content
        
        content_key = self._generate_content_key(content, content_type)
        
        # Try to get existing translation from database
        existing_translation = db.query(UserTranslation).filter(
            and_(
                UserTranslation.user_id == user_id,
                UserTranslation.content_key == content_key,
                UserTranslation.language == target_language
            )
        ).first()
        
        if existing_translation:
            logger.debug(f"Found cached translation for user {user_id}, content_type {content_type}")
            return existing_translation.translated_text
        
        # Create new translation using AWS Translate
        try:
            translated_text = translation_service.translate_text(content, target_language)
            
            # Store in database for future use
            new_translation = UserTranslation(
                user_id=user_id,
                content_type=content_type,
                content_key=content_key,
                language=target_language,
                original_text=content,
                translated_text=translated_text
            )
            
            db.add(new_translation)
            db.commit()
            
            logger.info(f"Created new translation for user {user_id}, content_type {content_type}, language {target_language}")
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed for user {user_id}: {e}")
            return content  # Return original on failure
    
    def translate_user_content(
        self, 
        user_id: str, 
        data: Dict[str, Any], 
        content_type: str, 
        fields_to_translate: List[str],
        target_language: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Translate specific fields in user content dictionary
        
        Args:
            user_id: User ID
            data: Dictionary containing data to translate
            content_type: Type of content
            fields_to_translate: List of field names to translate
            target_language: Target language code
            db: Database session
            
        Returns:
            Dictionary with translated fields
        """
        if target_language == 'en':
            return data
        
        translated_data = data.copy()
        
        for field in fields_to_translate:
            if field in translated_data and isinstance(translated_data[field], str):
                translated_data[field] = self.get_user_translation(
                    user_id=user_id,
                    content=translated_data[field],
                    content_type=f"{content_type}_{field}",
                    target_language=target_language,
                    db=db
                )
        
        return translated_data
    
    def translate_user_list(
        self, 
        user_id: str, 
        data_list: List[Dict[str, Any]], 
        content_type: str, 
        fields_to_translate: List[str],
        target_language: str,
        db: Session
    ) -> List[Dict[str, Any]]:
        """
        Translate specific fields in a list of user content dictionaries
        
        Args:
            user_id: User ID
            data_list: List of dictionaries to translate
            content_type: Type of content
            fields_to_translate: List of field names to translate
            target_language: Target language code
            db: Database session
            
        Returns:
            List of dictionaries with translated fields
        """
        if target_language == 'en':
            return data_list
        
        return [
            self.translate_user_content(
                user_id=user_id,
                data=item,
                content_type=content_type,
                fields_to_translate=fields_to_translate,
                target_language=target_language,
                db=db
            )
            for item in data_list
        ]
    
    def precompute_user_translations(
        self, 
        user_id: str, 
        content_items: List[Dict[str, str]], 
        target_languages: List[str],
        db: Session
    ) -> int:
        """
        Precompute translations for a user's content
        
        Args:
            user_id: User ID
            content_items: List of {'content': str, 'content_type': str} items
            target_languages: List of language codes to translate to
            db: Database session
            
        Returns:
            Number of translations created
        """
        translations_created = 0
        
        for item in content_items:
            content = item['content']
            content_type = item['content_type']
            
            for lang in target_languages:
                if lang == 'en':  # Skip English
                    continue
                
                # Check if translation already exists
                content_key = self._generate_content_key(content, content_type)
                existing = db.query(UserTranslation).filter(
                    and_(
                        UserTranslation.user_id == user_id,
                        UserTranslation.content_key == content_key,
                        UserTranslation.language == lang
                    )
                ).first()
                
                if not existing:
                    try:
                        translated_text = translation_service.translate_text(content, lang)
                        
                        new_translation = UserTranslation(
                            user_id=user_id,
                            content_type=content_type,
                            content_key=content_key,
                            language=lang,
                            original_text=content,
                            translated_text=translated_text
                        )
                        
                        db.add(new_translation)
                        translations_created += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to precompute translation for user {user_id}: {e}")
        
        if translations_created > 0:
            db.commit()
            logger.info(f"Precomputed {translations_created} translations for user {user_id}")
        
        return translations_created
    
    def get_user_preferred_language(self, user_id: str, db: Session) -> str:
        """
        Get user's preferred language from database
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Language code (defaults to 'en')
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.preferred_language:
            return user.preferred_language
        return 'en'
    
    def set_user_preferred_language(self, user_id: str, language: str, db: Session) -> bool:
        """
        Set user's preferred language in database
        
        Args:
            user_id: User ID
            language: Language code
            db: Database session
            
        Returns:
            True if successful
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.preferred_language = language
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to set preferred language for user {user_id}: {e}")
            return False
    
    def clear_user_translations(self, user_id: str, content_type: Optional[str] = None, db: Session = None) -> int:
        """
        Clear translations for a user (useful when content changes)
        
        Args:
            user_id: User ID
            content_type: Optional content type filter
            db: Database session
            
        Returns:
            Number of translations deleted
        """
        query = db.query(UserTranslation).filter(UserTranslation.user_id == user_id)
        
        if content_type:
            query = query.filter(UserTranslation.content_type == content_type)
        
        count = query.count()
        query.delete()
        db.commit()
        
        logger.info(f"Cleared {count} translations for user {user_id}")
        return count


# Global instance
db_translation_service = DatabaseTranslationService()