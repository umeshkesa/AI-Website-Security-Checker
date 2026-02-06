import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Request settings
# =========================
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
USER_AGENT = os.getenv("USER_AGENT", "SecurityScanner/1.0")

# =========================
# Feature flags
# =========================
WAPPALYZER_ENABLED = os.getenv("WAPPALYZER_ENABLED", "True").lower() == "true"
REGEX_FALLBACK_ENABLED = os.getenv("REGEX_FALLBACK_ENABLED", "True").lower() == "true"
AI_RECOMMENDATIONS_ENABLED = os.getenv("AI_RECOMMENDATIONS_ENABLED", "True").lower() == "true"

# =========================
# Environment
# =========================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# =========================
# CORS
# =========================
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000"
).split(",")

# =========================
# API KEYS
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NVD_API_KEY = os.getenv("NVD_API_KEY")  

# =========================
# CVSS Severity Mapping
# =========================
CVSS_LEVELS = {
    "LOW": (0.1, 3.9),
    "MEDIUM": (4.0, 6.9),
    "HIGH": (7.0, 8.9),
    "CRITICAL": (9.0, 10.0),
}


# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Request settings
# REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
# USER_AGENT = os.getenv("USER_AGENT", "SecurityScanner/1.0")

# # Feature flags
# WAPPALYZER_ENABLED = os.getenv("WAPPALYZER_ENABLED", "True").lower() == "true"
# REGEX_FALLBACK_ENABLED = os.getenv("REGEX_FALLBACK_ENABLED", "True").lower() == "true"

# # Environment
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development or production

# # CORS
# ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")


# AI_RECOMMENDATIONS_ENABLED = os.getenv(
#     "AI_RECOMMENDATIONS_ENABLED", "True"
# ).lower() == "true"


# GROQ_API_KEY = os.getenv("GROQ_API_KEY")



# # Known vulnerable versions database
# VULNERABLE_VERSIONS = {
#     "WordPress": {
#         "threshold": "6.4.0",
#         "severity": "High",
#         "cve_examples": ["CVE-2023-38000", "CVE-2023-39999"],
#         "description": "WordPress versions below 6.4 have critical security vulnerabilities"
#     },
#     "jQuery": {
#         "threshold": "3.5.0",
#         "severity": "High",
#         "cve_examples": ["CVE-2020-11023", "CVE-2020-11022"],
#         "description": "jQuery below 3.5.0 has XSS vulnerabilities"
#     },
#     "PHP": {
#         "threshold": "8.0.0",
#         "severity": "Medium",
#         "cve_examples": ["CVE-2023-0662"],
#         "description": "PHP 7.x reached end of life, multiple security issues"
#     },
#     "Nginx": {
#         "threshold": "1.20.0",
#         "severity": "Medium",
#         "cve_examples": ["CVE-2021-23017"],
#         "description": "Older Nginx versions have DNS resolver vulnerabilities"
#     },
#     "Apache": {
#         "threshold": "2.4.50",
#         "severity": "High",
#         "cve_examples": ["CVE-2021-41773", "CVE-2021-42013"],
#         "description": "Path traversal and RCE vulnerabilities in older Apache versions"
#     },
#     "Bootstrap": {
#         "threshold": "5.0.0",
#         "severity": "Low",
#         "cve_examples": ["CVE-2019-8331"],
#         "description": "Bootstrap 4.x has XSS vulnerabilities"
#     },
#     "React": {
#         "threshold": "17.0.0",
#         "severity": "Medium",
#         "cve_examples": ["CVE-2021-23374"],
#         "description": "Older React versions may have security patches missing"
#     },
#     "Angular": {
#         "threshold": "13.0.0",
#         "severity": "Medium",
#         "cve_examples": [],
#         "description": "Angular versions below 13 lack important security updates"
#     },
#     "Node.js": {
#         "threshold": "18.0.0",
#         "severity": "Medium",
#         "cve_examples": ["CVE-2023-32002"],
#         "description": "Older Node.js versions have multiple vulnerabilities"
#     },
#     "Express": {
#         "threshold": "4.17.0",
#         "severity": "Medium",
#         "cve_examples": ["CVE-2022-24999"],
#         "description": "Express versions below 4.17 have security issues"
#     }
# }

# # Technology categories for better organization
# TECH_CATEGORIES = {
#     "CMS": ["WordPress", "Joomla", "Drupal"],
#     "E-commerce": ["Magento", "Shopify", "WooCommerce"],
#     "JavaScript Framework": ["React", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Svelte"],
#     "CSS Framework": ["Bootstrap", "Tailwind CSS", "Foundation"],
#     "JavaScript Library": ["jQuery", "Lodash", "Moment.js"],
#     "Analytics": ["Google Analytics", "Google Tag Manager", "Facebook Pixel"],
#     "CDN": ["Cloudflare", "Akamai", "Fastly"],
#     "Web Server": ["Nginx", "Apache", "IIS"],
#     "Programming Language": ["PHP", "Python", "Node.js", "Ruby"]
# }