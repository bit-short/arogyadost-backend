"""
Amazon Translate service for multilingual support
Cost-effective translation using AWS Translate API
"""

import boto3
import json
import os
from typing import Dict, Optional, List
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        """Initialize Amazon Translate client"""
        try:
            # Initialize AWS Translate client
            self.translate_client = boto3.client(
                'translate',
                region_name='ap-south-1'  # Mumbai region for better latency
            )
            
            # Supported languages
            self.supported_languages = {
                'en': 'English',
                'hi': 'Hindi', 
                'ta': 'Tamil'
            }
            
            # Cache for translations to reduce API calls
            self._translation_cache = {}
            
        except Exception as e:
            logger.error(f"Failed to initialize translation service: {e}")
            self.translate_client = None
    
    @lru_cache(maxsize=1000)
    def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """
        Translate text using Amazon Translate with caching
        
        Args:
            text: Text to translate
            target_language: Target language code (hi, ta, en)
            source_language: Source language code (default: en)
            
        Returns:
            Translated text or original text if translation fails
        """
        # Return original text if same language or translation not needed
        if source_language == target_language or target_language == 'en':
            return text
            
        # Check if translation service is available
        if not self.translate_client:
            logger.warning("Translation service not available, returning original text")
            return text
            
        # Create cache key
        cache_key = f"{source_language}:{target_language}:{text}"
        
        # Check cache first
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]
            
        try:
            # Call Amazon Translate
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language
            )
            
            translated_text = response['TranslatedText']
            
            # Cache the result
            self._translation_cache[cache_key] = translated_text
            
            logger.info(f"Translated '{text[:50]}...' from {source_language} to {target_language}")
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed for '{text}': {e}")
            return text  # Return original text on failure
    
    def translate_dict(self, data: Dict, target_language: str, fields_to_translate: List[str]) -> Dict:
        """
        Translate specific fields in a dictionary
        
        Args:
            data: Dictionary containing data to translate
            target_language: Target language code
            fields_to_translate: List of field names to translate
            
        Returns:
            Dictionary with translated fields
        """
        if target_language == 'en':
            return data
            
        translated_data = data.copy()
        
        for field in fields_to_translate:
            if field in translated_data and isinstance(translated_data[field], str):
                translated_data[field] = self.translate_text(
                    translated_data[field], 
                    target_language
                )
                
        return translated_data
    
    def translate_list_of_dicts(self, data_list: List[Dict], target_language: str, fields_to_translate: List[str]) -> List[Dict]:
        """
        Translate specific fields in a list of dictionaries
        
        Args:
            data_list: List of dictionaries to translate
            target_language: Target language code
            fields_to_translate: List of field names to translate
            
        Returns:
            List of dictionaries with translated fields
        """
        if target_language == 'en':
            return data_list
            
        return [
            self.translate_dict(item, target_language, fields_to_translate)
            for item in data_list
        ]
    
    def get_language_from_header(self, accept_language_header: str) -> str:
        """
        Extract language preference from Accept-Language header
        
        Args:
            accept_language_header: HTTP Accept-Language header value
            
        Returns:
            Language code (en, hi, ta) - defaults to 'en'
        """
        if not accept_language_header:
            return 'en'
            
        # Parse Accept-Language header (simplified)
        # Format: "hi,en-US;q=0.9,en;q=0.8"
        languages = accept_language_header.lower().split(',')
        
        for lang in languages:
            # Extract language code (before any semicolon)
            lang_code = lang.split(';')[0].strip()
            
            # Map common language codes
            if lang_code.startswith('hi'):
                return 'hi'
            elif lang_code.startswith('ta'):
                return 'ta'
            elif lang_code.startswith('en'):
                return 'en'
                
        return 'en'  # Default to English
    
    def is_translation_available(self) -> bool:
        """Check if translation service is available"""
        return self.translate_client is not None

# Global translation service instance
translation_service = TranslationService()