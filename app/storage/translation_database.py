"""
Translation Database for Pre-computed Multilingual Content
Stores translated content for all supported languages to avoid real-time translation costs.
"""

import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class TranslationDatabase:
    """SQLite database manager for pre-computed translations."""
    
    def __init__(self, db_path: str = "translations.db"):
        self.db_path = Path(db_path)
        self.supported_languages = ['en', 'hi', 'ta']  # English, Hindi, Tamil
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize the translation database schema."""
        try:
            with self._get_connection() as conn:
                # User content translations table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_translations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        content_type TEXT NOT NULL,  -- 'insights', 'recommendations', 'health_status'
                        content_key TEXT NOT NULL,   -- unique identifier for the content
                        language_code TEXT NOT NULL, -- 'en', 'hi', 'ta'
                        original_text TEXT NOT NULL,
                        translated_text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(user_id, content_type, content_key, language_code)
                    )
                """)
                
                # Template translations for common content
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS template_translations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        template_key TEXT NOT NULL,  -- 'no_data_insight', 'upload_recommendation'
                        language_code TEXT NOT NULL,
                        original_text TEXT NOT NULL,
                        translated_text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(template_key, language_code)
                    )
                """)
                
                # Create indexes for better performance
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_user_translations_lookup 
                    ON user_translations(user_id, content_type, language_code)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_template_translations_lookup 
                    ON template_translations(template_key, language_code)
                """)
                
                conn.commit()
                logger.info(f"Translation database initialized at {self.db_path}")
                
                # Initialize template translations
                self._init_template_translations(conn)
                
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize translation database: {e}")
            raise Exception(f"Translation database initialization failed: {e}")
    
    def _init_template_translations(self, conn) -> None:
        """Initialize common template translations."""
        templates = {
            'no_data_insight_1': {
                'en': 'No biological age data available for this user yet.',
                'hi': 'इस उपयोगकर्ता के लिए अभी तक कोई जैविक आयु डेटा उपलब्ध नहीं है।',
                'ta': 'இந்த பயனருக்கு இன்னும் உயிரியல் வயது தரவு இல்லை।'
            },
            'no_data_insight_2': {
                'en': 'Upload health records and biomarker data to calculate biological age.',
                'hi': 'जैविक आयु की गणना के लिए स्वास्थ्य रिकॉर्ड और बायोमार्कर डेटा अपलोड करें।',
                'ta': 'உயிரியல் வயதைக் கணக்கிட உடல்நலம் பதிவுகள் மற்றும் உயிரியல் குறிப்பான் தரவை பதிவேற்றவும்।'
            },
            'no_data_recommendation_1': {
                'en': 'Start by uploading recent lab reports',
                'hi': 'हाल की लैब रिपोर्ट अपलोड करके शुरुआत करें',
                'ta': 'சமீபத்திய ஆய்வக அறிக்கைகளை பதிவேற்றுவதன் மூலம் தொடங்கவும்'
            },
            'no_data_recommendation_2': {
                'en': 'Complete the health questionnaire for baseline assessment',
                'hi': 'आधारभूत मूल्यांकन के लिए स्वास्थ्य प्रश्नावली पूरी करें',
                'ta': 'அடிப்படை மதிப்பீட்டிற்கு உடல்நலம் கேள்வித்தாளை முடிக்கவும்'
            }
        }
        
        try:
            for template_key, translations in templates.items():
                for lang_code, text in translations.items():
                    conn.execute("""
                        INSERT OR REPLACE INTO template_translations 
                        (template_key, language_code, original_text, translated_text)
                        VALUES (?, ?, ?, ?)
                    """, (template_key, lang_code, translations['en'], text))
            
            conn.commit()
            logger.info("Template translations initialized")
            
        except sqlite3.Error as e:
            logger.error(f"Failed to initialize template translations: {e}")
    
    @contextmanager
    def _get_connection(self):
        """Get a database connection with proper error handling."""
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Translation database operation failed: {e}")
            raise Exception(f"Translation database operation failed: {e}")
        finally:
            if conn:
                conn.close()
    
    def store_user_translations(self, user_id: str, content_type: str, 
                              translations: Dict[str, Dict[str, str]]) -> None:
        """
        Store pre-computed translations for a user's content.
        
        Args:
            user_id: User identifier
            content_type: Type of content ('insights', 'recommendations', 'health_status')
            translations: Dict with content_key -> {lang_code: translated_text}
        """
        try:
            with self._get_connection() as conn:
                for content_key, lang_translations in translations.items():
                    original_text = lang_translations.get('en', '')
                    
                    for lang_code, translated_text in lang_translations.items():
                        conn.execute("""
                            INSERT OR REPLACE INTO user_translations 
                            (user_id, content_type, content_key, language_code, 
                             original_text, translated_text, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        """, (user_id, content_type, content_key, lang_code, 
                              original_text, translated_text))
                
                conn.commit()
                logger.info(f"Stored translations for user {user_id}, type {content_type}")
                
        except Exception as e:
            logger.error(f"Failed to store translations for user {user_id}: {e}")
            raise
    
    def get_user_translations(self, user_id: str, content_type: str, 
                            language_code: str) -> Dict[str, str]:
        """
        Get translated content for a user in a specific language.
        
        Returns:
            Dict mapping content_key to translated_text
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT content_key, translated_text
                    FROM user_translations
                    WHERE user_id = ? AND content_type = ? AND language_code = ?
                """, (user_id, content_type, language_code))
                
                return {row['content_key']: row['translated_text'] 
                       for row in cursor.fetchall()}
                
        except Exception as e:
            logger.error(f"Failed to get translations for user {user_id}: {e}")
            return {}
    
    def get_template_translations(self, language_code: str) -> Dict[str, str]:
        """Get all template translations for a language."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT template_key, translated_text
                    FROM template_translations
                    WHERE language_code = ?
                """, (language_code,))
                
                return {row['template_key']: row['translated_text'] 
                       for row in cursor.fetchall()}
                
        except Exception as e:
            logger.error(f"Failed to get template translations for {language_code}: {e}")
            return {}
    
    def has_user_translations(self, user_id: str, content_type: str) -> bool:
        """Check if translations exist for a user's content."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT COUNT(*) as count
                    FROM user_translations
                    WHERE user_id = ? AND content_type = ?
                """, (user_id, content_type))
                
                return cursor.fetchone()['count'] > 0
                
        except Exception as e:
            logger.error(f"Failed to check translations for user {user_id}: {e}")
            return False
    
    def delete_user_translations(self, user_id: str) -> None:
        """Delete all translations for a user."""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    DELETE FROM user_translations WHERE user_id = ?
                """, (user_id,))
                conn.commit()
                logger.info(f"Deleted translations for user {user_id}")
                
        except Exception as e:
            logger.error(f"Failed to delete translations for user {user_id}: {e}")
            raise


# Global translation database instance
translation_db = TranslationDatabase()