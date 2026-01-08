"""
Translation middleware for FastAPI
Extracts language preference from Accept-Language header
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.translation_service import translation_service
import logging

logger = logging.getLogger(__name__)

class TranslationMiddleware(BaseHTTPMiddleware):
    """Middleware to extract and store language preference from requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Extract language from Accept-Language header
        accept_language = request.headers.get('accept-language', '')
        language = translation_service.get_language_from_header(accept_language)
        
        # Store language in request state for use in endpoints
        request.state.language = language
        
        # Log language detection for debugging
        if language != 'en':
            logger.info(f"Detected language: {language} from header: {accept_language}")
        
        # Process the request
        response = await call_next(request)
        
        return response