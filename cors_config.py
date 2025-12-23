"""
CORS Configuration for Aarogyadost API
Centralized CORS settings for easier management and updates
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response

# Allowed origins for CORS
ALLOWED_ORIGINS = [
    # Local development
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # Vite dev server
    
    # Development environment
    "https://dev.dpkvrxcu2ycyl.amplifyapp.com",
    "https://m2.arogyadost.in",
    
    # Production environment
    "https://main.dpkvrxcu2ycyl.amplifyapp.com",
    "https://m.arogyadost.in",
    
    # API documentation access
    "https://api-dev.arogyadost.in",
    "https://api.arogyadost.in",
    
    # Elastic Beanstalk URLs (HTTP and HTTPS)
    "http://aarogyadost-dev.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
    "https://aarogyadost-dev.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
    "http://aarogyadost-prod.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
    "https://aarogyadost-prod.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
    
    # Lovable development environment
    "https://id-preview--a7c71287-89db-4b36-9f19-46fd1ab30599.lovable.app",
    
    # Additional common development ports
    "http://localhost:3001",
    "http://localhost:4000",
    "http://localhost:5000",
    "http://localhost:8081",
    
    # For local file testing
    "null",  # For file:// protocol requests
]

# Allowed methods
ALLOWED_METHODS = [
    "GET",
    "POST", 
    "PUT",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "PATCH"
]

# Allowed headers
ALLOWED_HEADERS = [
    "Accept",
    "Accept-Language",
    "Content-Language", 
    "Content-Type",
    "Authorization",
    "X-Requested-With",
    "Origin",
    "Access-Control-Request-Method",
    "Access-Control-Request-Headers",
    "Cache-Control",
    "Pragma",
    "Referer",
    "User-Agent",
    "Sec-Ch-Ua",
    "Sec-Ch-Ua-Mobile",
    "Sec-Ch-Ua-Platform",
    "Sec-Fetch-Dest",
    "Sec-Fetch-Mode", 
    "Sec-Fetch-Site",
    "*"
]

# Exposed headers
EXPOSED_HEADERS = ["*"]

# CORS settings
CORS_SETTINGS = {
    "allow_origins": ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ALLOWED_METHODS,
    "allow_headers": ALLOWED_HEADERS,
    "expose_headers": EXPOSED_HEADERS,
    "max_age": 86400,  # Cache preflight for 24 hours
}

def setup_cors(app: FastAPI) -> None:
    """
    Setup CORS middleware for the FastAPI application
    
    Args:
        app: FastAPI application instance
    """
    app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

def create_cors_preflight_handler(app: FastAPI) -> None:
    """
    Create explicit CORS preflight handler for all routes
    
    Args:
        app: FastAPI application instance
    """
    @app.options("/{full_path:path}")
    async def options_handler(full_path: str):
        response = Response(content='{"message": "OK"}', media_type="application/json")
        response.headers["Access-Control-Allow-Methods"] = ", ".join(ALLOWED_METHODS)
        response.headers["Access-Control-Allow-Headers"] = ", ".join([h for h in ALLOWED_HEADERS if h != "*"])
        response.headers["Access-Control-Max-Age"] = "86400"
        return response

def add_origin_to_whitelist(origin: str) -> None:
    """
    Dynamically add an origin to the CORS whitelist
    
    Args:
        origin: The origin URL to add
    """
    if origin not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(origin)
        print(f"Added {origin} to CORS whitelist")

def remove_origin_from_whitelist(origin: str) -> None:
    """
    Remove an origin from the CORS whitelist
    
    Args:
        origin: The origin URL to remove
    """
    if origin in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.remove(origin)
        print(f"Removed {origin} from CORS whitelist")

def get_cors_info() -> dict:
    """
    Get current CORS configuration information
    
    Returns:
        Dictionary with CORS configuration details
    """
    return {
        "total_origins": len(ALLOWED_ORIGINS),
        "origins": ALLOWED_ORIGINS,
        "methods": ALLOWED_METHODS,
        "headers": ALLOWED_HEADERS,
        "max_age": CORS_SETTINGS["max_age"],
        "credentials": CORS_SETTINGS["allow_credentials"]
    }

# Environment-specific origin groups for easier management
ORIGIN_GROUPS = {
    "local": [
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3001",
        "http://localhost:4000",
        "http://localhost:5000",
        "http://localhost:8081",
    ],
    "development": [
        "https://dev.dpkvrxcu2ycyl.amplifyapp.com",
        "https://m2.arogyadost.in",
        "https://api-dev.arogyadost.in",
        "https://aarogyadost-dev.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
        "http://aarogyadost-dev.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
    ],
    "production": [
        "https://main.dpkvrxcu2ycyl.amplifyapp.com",
        "https://m.arogyadost.in",
        "https://api.arogyadost.in",
        "https://aarogyadost-prod.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
        "http://aarogyadost-prod.eba-uxpnifkq.ap-south-1.elasticbeanstalk.com",
    ],
    "lovable": [
        "https://id-preview--a7c71287-89db-4b36-9f19-46fd1ab30599.lovable.app",
    ],
    "special": [
        "null",  # For file:// protocol
    ]
}