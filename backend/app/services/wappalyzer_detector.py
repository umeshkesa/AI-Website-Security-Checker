import logging
from typing import Dict
from app.config import WAPPALYZER_ENABLED

logger = logging.getLogger(__name__)

# Try to import Wappalyzer
WAPPALYZER_AVAILABLE = False
try:
    from Wappalyzer import Wappalyzer, WebPage
    WAPPALYZER_AVAILABLE = True
    logger.info("Wappalyzer loaded successfully")
except ImportError:
    logger.warning("Wappalyzer not installed. Regex fallback will be used.")


class WappalyzerDetector:
    """
    Uses Wappalyzer library for comprehensive technology detection
    Detects 3000+ technologies with version information
    """
    
    def __init__(self):
        self.enabled = WAPPALYZER_ENABLED and WAPPALYZER_AVAILABLE
        self.wappalyzer = None
        
        if self.enabled:
            try:
                self.wappalyzer = Wappalyzer.latest()
                logger.info("Wappalyzer initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Wappalyzer: {e}")
                self.enabled = False
    
    def detect(self, url: str, html: str, headers: dict) -> Dict:
        """
        Detect technologies using Wappalyzer
        
        Args:
            url: Target URL
            html: HTML content
            headers: HTTP response headers
            
        Returns:
            {
                "success": bool,
                "method": "wappalyzer",
                "technologies": {
                    "WordPress": {
                        "version": "6.3.0",
                        "versions": ["6.3.0"],
                        "categories": ["CMS"],
                        "confidence": 100
                    },
                    ...
                },
                "count": int,
                "error": str | None
            }
        """
        
        result = {
            "success": False,
            "method": "wappalyzer",
            "technologies": {},
            "count": 0,
            "error": None
        }
        
        if not self.enabled:
            result["error"] = "Wappalyzer not enabled or not available"
            return result
        
        try:
            # Create WebPage object
            webpage = WebPage(url, html, headers)
            
            # Analyze with versions and categories
            detected = self.wappalyzer.analyze_with_versions_and_categories(webpage)
            
            # Format results
            for tech_name, details in detected.items():
                versions = details.get('versions', [])
                categories = details.get('categories', [])
                
                result["technologies"][tech_name] = {
                    "version": versions[0] if versions else None,
                    "all_versions": versions,
                    "categories": [cat for cat in categories],
                    "confidence": 100,  # Wappalyzer doesn't provide confidence scores
                    "detection_method": "wappalyzer"
                }
            
            result["success"] = True
            result["count"] = len(result["technologies"])
            
            logger.info(f"Wappalyzer detected {result['count']} technologies for {url}")
            
        except Exception as e:
            logger.error(f"Wappalyzer detection failed for {url}: {e}")
            result["error"] = str(e)
        
        return result
    
    def is_available(self) -> bool:
        """Check if Wappalyzer is available and enabled"""
        return self.enabled


def is_wappalyzer_available() -> bool:
    """Module-level function to check Wappalyzer availability"""
    return WAPPALYZER_AVAILABLE and WAPPALYZER_ENABLED