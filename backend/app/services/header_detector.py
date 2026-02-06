import logging
import re
from typing import Dict

logger = logging.getLogger(__name__)


class HeaderDetector:
    """
    Detects technologies from HTTP response headers
    Useful for server-side technologies and infrastructure
    """
    
    def __init__(self):
        # Patterns for header-based detection
        self.server_patterns = {
            "Nginx": {
                "pattern": r"nginx/?(\d+\.\d+(?:\.\d+)?)?",
                "category": "Web Server"
            },
            "Apache": {
                "pattern": r"Apache/?(\d+\.\d+(?:\.\d+)?)?",
                "category": "Web Server"
            },
            "Microsoft-IIS": {
                "pattern": r"Microsoft-IIS/?(\d+\.\d+)?",
                "category": "Web Server"
            },
            "LiteSpeed": {
                "pattern": r"LiteSpeed/?(\d+\.\d+(?:\.\d+)?)?",
                "category": "Web Server"
            },
            "Cloudflare": {
                "pattern": r"cloudflare",
                "category": "CDN"
            }
        }
        
        self.powered_by_patterns = {
            "PHP": {
                "pattern": r"PHP/?(\d+\.\d+\.\d+)?",
                "category": "Programming Language"
            },
            "Express": {
                "pattern": r"Express/?(\d+\.\d+\.\d+)?",
                "category": "Web Framework"
            },
            "ASP.NET": {
                "pattern": r"ASP\.NET/?(\d+\.\d+)?",
                "category": "Web Framework"
            }
        }
    
    def detect(self, headers: dict) -> Dict:
        """
        Detect technologies from HTTP headers
        
        Args:
            headers: Dictionary of HTTP response headers
            
        Returns:
            {
                "success": bool,
                "method": "headers",
                "technologies": {
                    "Nginx": {
                        "version": "1.21.0",
                        "category": "Web Server",
                        "confidence": 100,
                        "detection_method": "server_header"
                    },
                    ...
                },
                "count": int,
                "cloudflare_detected": bool,
                "error": str | None
            }
        """
        
        result = {
            "success": False,
            "method": "headers",
            "technologies": {},
            "count": 0,
            "cloudflare_detected": False,
            "error": None
        }
        
        try:
            # Normalize header keys to lowercase
            headers_lower = {k.lower(): v for k, v in headers.items()}
            
            # Check Server header
            server_header = headers_lower.get("server", "")
            if server_header:
                for tech_name, tech_info in self.server_patterns.items():
                    match = re.search(tech_info["pattern"], server_header, re.IGNORECASE)
                    if match:
                        version = match.group(1) if match.groups() and match.group(1) else None
                        result["technologies"][tech_name] = {
                            "version": version,
                            "category": tech_info["category"],
                            "confidence": 100,
                            "detection_method": "server_header"
                        }
            
            # Check X-Powered-By header
            powered_by = headers_lower.get("x-powered-by", "")
            if powered_by:
                for tech_name, tech_info in self.powered_by_patterns.items():
                    match = re.search(tech_info["pattern"], powered_by, re.IGNORECASE)
                    if match:
                        version = match.group(1) if match.groups() and match.group(1) else None
                        result["technologies"][tech_name] = {
                            "version": version,
                            "category": tech_info["category"],
                            "confidence": 100,
                            "detection_method": "powered_by_header"
                        }
            
            # Check for Cloudflare-specific headers
            cloudflare_headers = ["cf-ray", "cf-cache-status", "cf-request-id"]
            for cf_header in cloudflare_headers:
                if cf_header in headers_lower:
                    result["cloudflare_detected"] = True
                    if "Cloudflare" not in result["technologies"]:
                        result["technologies"]["Cloudflare"] = {
                            "version": None,
                            "category": "CDN",
                            "confidence": 100,
                            "detection_method": "cf_header"
                        }
                    break
            
            # Check X-Generator header (some CMSs use this)
            x_generator = headers_lower.get("x-generator", "")
            if x_generator:
                if "drupal" in x_generator.lower():
                    version_match = re.search(r'(\d+\.\d+)', x_generator)
                    result["technologies"]["Drupal"] = {
                        "version": version_match.group(1) if version_match else None,
                        "category": "CMS",
                        "confidence": 100,
                        "detection_method": "x_generator_header"
                    }
            
            result["success"] = True
            result["count"] = len(result["technologies"])
            
            logger.info(f"Header detector found {result['count']} technologies")
            
        except Exception as e:
            logger.error(f"Header detection failed: {e}")
            result["error"] = str(e)
        
        return result