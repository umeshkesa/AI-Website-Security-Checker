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
    "ALLOWED_ORIGINS"," http://localhost:5173/"
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

