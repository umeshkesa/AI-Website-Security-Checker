import requests
import logging
from typing import Dict
from urllib.parse import urlparse
from app.utils.url_validator import validate_url
from app.services.hybrid_detector import HybridTechnologyDetector
from app.config import REQUEST_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)


def detect_technology(url: str) -> dict:
    """
    Main function to detect technologies using hybrid approach
    Works in both local and production environments
    
    Args:
        url: Target URL to scan
        
    Returns:
        {
            "service": "technology",
            "technologies": {...},
            "total_count": int,
            "vulnerabilities": [...],
            "risk_score": int,
            "severity": str,
            "issue": str,
            "recommendations": [...],
            "detection_methods_used": [...],
            "cloudflare_detected": bool
        }
    """
    
    result = {
        "service": "technology",
        "technologies": {},
        "total_count": 0,
        "vulnerabilities": [],
        "risk_score": 0,
        "severity": "Low",
        "issue": None,
        "recommendations": [],
        "detection_methods_used": [],
        "cloudflare_detected": False,
        "server": None,
        "powered_by": None
    }
    
    # Validate URL
    is_valid, error, normalized_url = validate_url(url)
    if not is_valid:
        result["issue"] = error
        result["severity"] = "Medium"
        return result
    
    try:
        # Fetch website
        logger.info(f"Fetching {normalized_url} for technology detection")
        response = requests.get(
            normalized_url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": USER_AGENT},
            verify=True
        )
        
        response.raise_for_status()
        
        html = response.text
        headers = dict(response.headers)
        
        # Store basic server info
        result["server"] = headers.get("Server")
        result["powered_by"] = headers.get("X-Powered-By")
        
        # Initialize hybrid detector
        detector = HybridTechnologyDetector()
        
        # Detect technologies
        detection_result = detector.detect(normalized_url, html, headers)
        
        if detection_result["success"]:
            result["technologies"] = detection_result["technologies"]
            result["total_count"] = detection_result["total_count"]
            result["vulnerabilities"] = detection_result["vulnerabilities"]
            result["risk_score"] = detection_result["risk_score"]
            result["detection_methods_used"] = detection_result["detection_summary"]["methods_used"]
            result["cloudflare_detected"] = detection_result["cloudflare_detected"]
            
            # Determine severity based on vulnerabilities
            # if result["vulnerabilities"]:
            #     severities = [v["severity"] for v in result["vulnerabilities"]]
            #     if "Critical" in severities:
            #         result["severity"] = "Critical"
            #     elif "High" in severities:
            #         result["severity"] = "High"
            #     elif "Medium" in severities:
            #         result["severity"] = "Medium"
            #     else:
            #         result["severity"] = "Low"
                
            #     result["issue"] = f"Found {len(result['vulnerabilities'])} vulnerable technologies"
            # else:
            #     result["severity"] = "Low"
            #     result["issue"] = None
            
            # Generate recommendations
            if result["vulnerabilities"]:
                for vuln in result["vulnerabilities"][:5]:  # Top 5
                    result["recommendations"].append(vuln["recommendation"])
            
            # Add Cloudflare recommendation if detected
            if result["cloudflare_detected"]:
                result["recommendations"].append(
                    "Cloudflare CDN detected - verify origin server IP is not exposed"
                )
            
            # If many technologies detected, suggest review
            if result["total_count"] > 15:
                result["recommendations"].append(
                    f"{result['total_count']} technologies detected - review for unnecessary dependencies"
                )
            
        else:
            result["issue"] = detection_result.get("error", "Technology detection failed")
            result["severity"] = "Medium"
        
    except requests.exceptions.Timeout:
        result["issue"] = "Technology detection timed out"
        result["severity"] = "Medium"
        logger.warning(f"Timeout detecting technologies for {normalized_url}")
    
    except requests.exceptions.RequestException as e:
        result["issue"] = f"Failed to fetch website: {str(e)}"
        result["severity"] = "Medium"
        logger.error(f"Request failed for {normalized_url}: {e}")
    
    except Exception as e:
        result["issue"] = f"Technology detection failed: {str(e)}"
        result["severity"] = "Medium"
        logger.error(f"Unexpected error detecting technologies for {normalized_url}: {e}")
    
    return result