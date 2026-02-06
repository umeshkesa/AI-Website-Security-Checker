from urllib.parse import urlparse
from typing import Tuple

def validate_url(url: str) -> Tuple[bool, str, str]:
    """
    Validates URL and returns (is_valid, error_message, normalized_url)
    
    Args:
        url: URL string to validate
        
    Returns:
        Tuple of (is_valid: bool, error: str, normalized_url: str)
    """
    
    if not url or not isinstance(url, str):
        return False, "URL is required and must be a string", ""
    
    url = url.strip()
    
    # Add https:// if no scheme provided
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    
    try:
        parsed = urlparse(url)
        
        if not parsed.scheme:
            return False, "URL must include http:// or https://", ""
        
        if parsed.scheme not in ["http", "https"]:
            return False, "Only HTTP/HTTPS URLs are supported", ""
        
        if not parsed.netloc:
            return False, "Invalid URL format - missing domain", ""
        
        # Check for localhost/private IPs in production
        from app.config import ENVIRONMENT
        if ENVIRONMENT == "production":
            blocked_hosts = ["localhost", "127.0.0.1", "0.0.0.0", "::1"]
            if any(blocked in parsed.netloc.lower() for blocked in blocked_hosts):
                return False, "Scanning localhost is not allowed in production", ""
        
        return True, "", url
        
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}", ""


def extract_hostname(url: str) -> str:
    """Extract hostname from URL"""
    try:
        parsed = urlparse(url)
        return parsed.hostname or ""
    except:
        return ""