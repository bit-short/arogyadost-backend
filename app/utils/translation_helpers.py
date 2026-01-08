"""
Helper functions for integrating database translations with API endpoints
"""

from typing import Dict, List, Any, Optional
from fastapi import Request, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.db_translation import db_translation_service
from app.services.user_context import user_context_manager


def get_request_language(request: Request) -> str:
    """
    Get language from request state (set by middleware)
    
    Args:
        request: FastAPI request object
        
    Returns:
        Language code
    """
    return getattr(request.state, 'language', 'en')


def get_current_user_id() -> str:
    """
    Get current user ID from context manager
    
    Returns:
        User ID
    """
    current_user = user_context_manager.get_current_user()
    return current_user.user_id if current_user else "test_user_1"


def translate_response_data(
    data: Dict[str, Any],
    content_type: str,
    fields_to_translate: List[str],
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Translate response data using database translations
    
    Args:
        data: Response data dictionary
        content_type: Type of content for translation caching
        fields_to_translate: List of fields to translate
        request: FastAPI request object
        db: Database session
        
    Returns:
        Translated response data
    """
    language = get_request_language(request)
    user_id = get_current_user_id()
    
    return db_translation_service.translate_user_content(
        user_id=user_id,
        data=data,
        content_type=content_type,
        fields_to_translate=fields_to_translate,
        target_language=language,
        db=db
    )


def translate_response_list(
    data_list: List[Dict[str, Any]],
    content_type: str,
    fields_to_translate: List[str],
    request: Request,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Translate response data list using database translations
    
    Args:
        data_list: List of response data dictionaries
        content_type: Type of content for translation caching
        fields_to_translate: List of fields to translate
        request: FastAPI request object
        db: Database session
        
    Returns:
        Translated response data list
    """
    language = get_request_language(request)
    user_id = get_current_user_id()
    
    return db_translation_service.translate_user_list(
        user_id=user_id,
        data_list=data_list,
        content_type=content_type,
        fields_to_translate=fields_to_translate,
        target_language=language,
        db=db
    )


class TranslationContext:
    """
    Context manager for translation operations
    """
    
    def __init__(self, request: Request, db: Session):
        self.request = request
        self.db = db
        self.language = get_request_language(request)
        self.user_id = get_current_user_id()
    
    def translate_dict(
        self, 
        data: Dict[str, Any], 
        content_type: str, 
        fields: List[str]
    ) -> Dict[str, Any]:
        """Translate dictionary data"""
        return db_translation_service.translate_user_content(
            user_id=self.user_id,
            data=data,
            content_type=content_type,
            fields_to_translate=fields,
            target_language=self.language,
            db=self.db
        )
    
    def translate_list(
        self, 
        data_list: List[Dict[str, Any]], 
        content_type: str, 
        fields: List[str]
    ) -> List[Dict[str, Any]]:
        """Translate list of dictionaries"""
        return db_translation_service.translate_user_list(
            user_id=self.user_id,
            data_list=data_list,
            content_type=content_type,
            fields_to_translate=fields,
            target_language=self.language,
            db=self.db
        )
    
    def translate_text(self, text: str, content_type: str) -> str:
        """Translate single text"""
        return db_translation_service.get_user_translation(
            user_id=self.user_id,
            content=text,
            content_type=content_type,
            target_language=self.language,
            db=self.db
        )


def get_translation_context(request: Request, db: Session = Depends(get_db)) -> TranslationContext:
    """
    Get translation context for the current request
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        TranslationContext instance
    """
    return TranslationContext(request, db)