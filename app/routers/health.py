"""
Health check endpoints for Digital Brain Integration.
"""

import logging
from datetime import datetime
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.storage.persistent_storage import persistent_storage
from app.services.user_service import user_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/health", tags=["Health"])


@router.get("/database")
async def database_health():
    """Check database connectivity and basic operations."""
    try:
        # Test basic database operations
        users = user_service.list_users()
        cache_stats = persistent_storage.get_cache_stats()
        
        return {
            "status": "healthy",
            "service": "database",
            "users_count": len(users),
            "cache_stats": cache_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "database",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get("/storage")
async def storage_health():
    """Check storage layer health."""
    try:
        # Test storage operations
        test_user_id = "health_check_test"
        
        # Try to get a non-existent user (should return None, not error)
        result = persistent_storage.get_digital_twin(test_user_id)
        
        return {
            "status": "healthy",
            "service": "storage",
            "cache_enabled": persistent_storage._cache_enabled,
            "cache_size": len(persistent_storage._cache),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Storage health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "storage",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@router.get("/digital-brain")
async def digital_brain_health():
    """Overall health check for digital brain integration."""
    try:
        # Check all components
        database_ok = True
        storage_ok = True
        
        try:
            users = user_service.list_users()
        except Exception as e:
            database_ok = False
            logger.error(f"Database check failed: {e}")
        
        try:
            cache_stats = persistent_storage.get_cache_stats()
        except Exception as e:
            storage_ok = False
            logger.error(f"Storage check failed: {e}")
        
        overall_status = "healthy" if database_ok and storage_ok else "degraded"
        status_code = status.HTTP_200_OK if overall_status == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return JSONResponse(
            status_code=status_code,
            content={
                "status": overall_status,
                "service": "digital_brain",
                "components": {
                    "database": "healthy" if database_ok else "unhealthy",
                    "storage": "healthy" if storage_ok else "unhealthy"
                },
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Digital brain health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "digital_brain",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )