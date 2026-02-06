import re
import logging
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Comprehensive regex patterns for technology detection
TECH_PATTERNS = {
    # CMS
    "WordPress": {
        "patterns": [
            r"wp-content|wp-includes",
            r"wordpress[/-](\d+\.\d+(?:\.\d+)?)",
            r"/wp-json/",
            r'<meta name="generator" content="WordPress\s+(\d+\.\d+(?:\.\d+)?)'
        ],
        "category": "CMS",
        "confidence": 90
    },
    "Joomla": {
        "patterns": [
            r"joomla",
            r"/components/com_",
            r"option=com_",
            r'<meta name="generator" content="Joomla!\s+(\d+\.\d+)'
        ],
        "category": "CMS",
        "confidence": 85
    },
    "Drupal": {
        "patterns": [
            r"drupal",
            r"/sites/default/files",
            r'Drupal\s+(\d+)',
            r"/core/misc/drupal"
        ],
        "category": "CMS",
        "confidence": 85
    },
    "Magento": {
        "patterns": [
            r"Mage\.Cookies",
            r"/skin/frontend/",
            r"magento",
            r"/static/version\d+"
        ],
        "category": "E-commerce",
        "confidence": 90
    },
    "Shopify": {
        "patterns": [
            r"cdn\.shopify\.com",
            r"myshopify\.com",
            r"Shopify\.theme",
            r"shopify-features"
        ],
        "category": "E-commerce",
        "confidence": 95
    },
    "Wix": {
        "patterns": [
            r"wix\.com",
            r"parastorage\.com",
            r"wixstatic\.com"
        ],
        "category": "Website Builder",
        "confidence": 95
    },
    "Squarespace": {
        "patterns": [
            r"squarespace",
            r"squarespace\.com",
            r"sqsp\.net"
        ],
        "category": "Website Builder",
        "confidence": 95
    },
    
    # JavaScript Frameworks
    "jQuery": {
        "patterns": [
            r"jquery[/-](\d+\.\d+\.\d+)",
            r'jQuery\s+v(\d+\.\d+\.\d+)',
            r"jquery\.min\.js"
        ],
        "category": "JavaScript Library",
        "confidence": 95
    },
    "React": {
        "patterns": [
            r"react(?:[/-]|\.production\.min\.js\?v=)(\d+\.\d+\.\d+)",
            r"__REACT_DEVTOOLS",
            r"react-dom",
            r"_react"
        ],
        "category": "JavaScript Framework",
        "confidence": 90
    },
    "Vue.js": {
        "patterns": [
            r"vue(?:[/-]|\.)(\d+\.\d+\.\d+)",
            r"__VUE__",
            r"vue\.js",
            r"vue\.runtime"
        ],
        "category": "JavaScript Framework",
        "confidence": 90
    },
    "Angular": {
        "patterns": [
            r"angular(?:[/-]|\.)(\d+\.\d+\.\d+)",
            r"ng-version",
            r"_angular_core",
            r"@angular/core"
        ],
        "category": "JavaScript Framework",
        "confidence": 90
    },
    "Next.js": {
        "patterns": [
            r"__NEXT_DATA__",
            r"_next/static",
            r"next\.js",
            r'"buildId"'
        ],
        "category": "JavaScript Framework",
        "confidence": 95
    },
    "Nuxt.js": {
        "patterns": [
            r"__NUXT__",
            r"_nuxt/",
            r"nuxt\.js"
        ],
        "category": "JavaScript Framework",
        "confidence": 95
    },
    "Svelte": {
        "patterns": [
            r"svelte",
            r"__svelte",
            r"svelte\.js"
        ],
        "category": "JavaScript Framework",
        "confidence": 85
    },
    
    # CSS Frameworks
    "Bootstrap": {
        "patterns": [
            r"bootstrap[/-](\d+\.\d+\.\d+)",
            r"bootstrap\.min\.css",
            r"/css/bootstrap"
        ],
        "category": "CSS Framework",
        "confidence": 90
    },
    "Tailwind CSS": {
        "patterns": [
            r"tailwindcss",
            r"tailwind\.css",
            r"@tailwind"
        ],
        "category": "CSS Framework",
        "confidence": 85
    },
    "Foundation": {
        "patterns": [
            r"foundation[/-](\d+\.\d+)",
            r"foundation\.min\.css"
        ],
        "category": "CSS Framework",
        "confidence": 85
    },
    "Materialize": {
        "patterns": [
            r"materialize[/-](\d+\.\d+)",
            r"materialize\.css"
        ],
        "category": "CSS Framework",
        "confidence": 85
    },
    
    # JavaScript Libraries
    "Lodash": {
        "patterns": [
            r"lodash[/-](\d+\.\d+\.\d+)",
            r"lodash\.min\.js",
            r"_\.VERSION"
        ],
        "category": "JavaScript Library",
        "confidence": 90
    },
    "Moment.js": {
        "patterns": [
            r"moment[/-](\d+\.\d+\.\d+)",
            r"moment\.min\.js"
        ],
        "category": "JavaScript Library",
        "confidence": 90
    },
    "D3.js": {
        "patterns": [
            r"d3[/-](\d+\.\d+\.\d+)",
            r"d3\.min\.js",
            r"d3\.v\d+"
        ],
        "category": "Data Visualization",
        "confidence": 90
    },
    "Chart.js": {
        "patterns": [
            r"chart\.js[/-](\d+\.\d+\.\d+)",
            r"chart\.min\.js"
        ],
        "category": "Data Visualization",
        "confidence": 90
    },
    "Three.js": {
        "patterns": [
            r"three[/-]r(\d+)",
            r"three\.min\.js"
        ],
        "category": "3D Graphics",
        "confidence": 85
    },
    
    # Analytics & Tracking
    "Google Analytics": {
        "patterns": [
            r"google-analytics\.com/analytics\.js",
            r"gtag/js",
            r"googletagmanager\.com/gtag",
            r"ga\('create'",
            r"UA-\d+-\d+",
            r"G-[A-Z0-9]+"
        ],
        "category": "Analytics",
        "confidence": 100
    },
    "Google Tag Manager": {
        "patterns": [
            r"googletagmanager\.com/gtm\.js",
            r"GTM-[A-Z0-9]+",
            r"dataLayer"
        ],
        "category": "Tag Manager",
        "confidence": 100
    },
    "Facebook Pixel": {
        "patterns": [
            r"connect\.facebook\.net/en_US/fbevents\.js",
            r"fbq\('init'",
            r"facebook\.com/tr\?"
        ],
        "category": "Analytics",
        "confidence": 100
    },
    "Hotjar": {
        "patterns": [
            r"static\.hotjar\.com",
            r"hjid",
            r"_hjid"
        ],
        "category": "Analytics",
        "confidence": 95
    },
    
    # CDN Detection
    "Cloudflare": {
        "patterns": [
            r"__cf_bm",
            r"cf-ray",
            r"cloudflare",
            r"cdnjs\.cloudflare\.com"
        ],
        "category": "CDN",
        "confidence": 100
    },
    "Akamai": {
        "patterns": [
            r"akamaihd\.net",
            r"akamai",
            r"edgesuite\.net"
        ],
        "category": "CDN",
        "confidence": 95
    },
    "Fastly": {
        "patterns": [
            r"fastly\.net",
            r"fastly-insights"
        ],
        "category": "CDN",
        "confidence": 95
    },
    "Amazon CloudFront": {
        "patterns": [
            r"cloudfront\.net",
            r"cloudfront"
        ],
        "category": "CDN",
        "confidence": 95
    },
    
    # Payment Processors
    "Stripe": {
        "patterns": [
            r"js\.stripe\.com",
            r"stripe\.com/v3",
            r"Stripe\("
        ],
        "category": "Payment",
        "confidence": 100
    },
    "PayPal": {
        "patterns": [
            r"paypal\.com/sdk/js",
            r"paypalobjects\.com",
            r"paypal-button"
        ],
        "category": "Payment",
        "confidence": 100
    },
    
    # Build Tools
    "Webpack": {
        "patterns": [
            r"webpack",
            r"webpackJsonp",
            r"__webpack"
        ],
        "category": "Build Tool",
        "confidence": 85
    },
    "Vite": {
        "patterns": [
            r"@vite",
            r"vite\.js"
        ],
        "category": "Build Tool",
        "confidence": 85
    }
}


class RegexDetector:
    """
    Fallback technology detector using regex patterns
    Used when Wappalyzer is unavailable or as secondary detection
    """
    
    def __init__(self):
        self.patterns = TECH_PATTERNS
    
    def detect(self, url: str, html: str, headers: dict) -> Dict:
        """
        Detect technologies using regex patterns
        
        Args:
            url: Target URL
            html: HTML content (lowercase for matching)
            headers: HTTP response headers
            
        Returns:
            {
                "success": bool,
                "method": "regex",
                "technologies": {
                    "jQuery": {
                        "version": "3.6.0",
                        "category": "JavaScript Library",
                        "confidence": 95,
                        "detection_method": "regex"
                    },
                    ...
                },
                "count": int,
                "error": str | None
            }
        """
        
        result = {
            "success": False,
            "method": "regex",
            "technologies": {},
            "count": 0,
            "error": None
        }
        
        try:
            html_lower = html.lower()
            
            # Detect from HTML patterns
            for tech_name, tech_info in self.patterns.items():
                patterns = tech_info["patterns"]
                category = tech_info["category"]
                confidence = tech_info.get("confidence", 80)
                
                version = None
                detected = False
                
                for pattern in patterns:
                    match = re.search(pattern, html_lower, re.IGNORECASE)
                    if match:
                        detected = True
                        # Try to extract version if pattern has capturing group
                        if match.groups():
                            version = match.group(1)
                        break
                
                if detected:
                    result["technologies"][tech_name] = {
                        "version": version,
                        "category": category,
                        "confidence": confidence,
                        "detection_method": "regex"
                    }
            
            # Detect from meta tags using BeautifulSoup
            try:
                soup = BeautifulSoup(html, 'html.parser')
                
                # Check generator meta tag
                generator = soup.find("meta", attrs={"name": "generator"})
                if generator:
                    content = generator.get("content", "")
                    # Parse generator content (e.g., "WordPress 6.3")
                    for tech in ["WordPress", "Joomla", "Drupal", "Magento"]:
                        if tech.lower() in content.lower():
                            version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', content)
                            if tech not in result["technologies"]:
                                result["technologies"][tech] = {
                                    "version": version_match.group(1) if version_match else None,
                                    "category": "CMS",
                                    "confidence": 100,
                                    "detection_method": "meta_tag"
                                }
            except Exception as e:
                logger.debug(f"BeautifulSoup parsing failed: {e}")
            
            result["success"] = True
            result["count"] = len(result["technologies"])
            
            logger.info(f"Regex detected {result['count']} technologies for {url}")
            
        except Exception as e:
            logger.error(f"Regex detection failed for {url}: {e}")
            result["error"] = str(e)
        
        return result