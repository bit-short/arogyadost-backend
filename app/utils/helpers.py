"""
Common utility functions for the application
"""

from typing import Any, Dict, List, Optional
import re
from datetime import datetime, timezone


def sanitize_string(text: str) -> str:
    """
    Sanitize string for safe usage in APIs
    
    Args:
        text: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def format_biomarker_value(value: Any, unit: str = "") -> str:
    """
    Format biomarker values for display
    
    Args:
        value: Biomarker value (number or string)
        unit: Unit of measurement
        
    Returns:
        Formatted string
    """
    if value is None:
        return "N/A"
    
    if isinstance(value, (int, float)):
        if unit:
            return f"{value} {unit}"
        return str(value)
    
    return str(value)


def calculate_age_from_dob(date_of_birth: str) -> Optional[int]:
    """
    Calculate age from date of birth string
    
    Args:
        date_of_birth: Date string in YYYY-MM-DD format
        
    Returns:
        Age in years or None if invalid date
    """
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except (ValueError, TypeError):
        return None


def extract_numeric_value(text: str) -> Optional[float]:
    """
    Extract numeric value from text string
    
    Args:
        text: Text containing numeric value
        
    Returns:
        Extracted numeric value or None
    """
    if not text:
        return None
    
    # Find first number in the string
    match = re.search(r'-?\d+\.?\d*', str(text))
    if match:
        try:
            return float(match.group())
        except ValueError:
            pass
    
    return None


def get_health_status_color(status: str) -> str:
    """
    Get color code for health status
    
    Args:
        status: Health status (excellent, good, fair, poor)
        
    Returns:
        Color code
    """
    status_colors = {
        'excellent': '#22c55e',  # Green
        'good': '#84cc16',       # Light green
        'fair': '#f59e0b',       # Orange
        'poor': '#ef4444',       # Red
        'normal': '#22c55e',     # Green
        'high': '#ef4444',       # Red
        'low': '#f59e0b'         # Orange
    }
    
    return status_colors.get(status.lower(), '#6b7280')  # Default gray


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format
    
    Returns:
        ISO formatted timestamp string
    """
    return datetime.now(timezone.utc).isoformat()


def deep_merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result