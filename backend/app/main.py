import os
import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import ALLOWED_ORIGINS, ENVIRONMENT
from app.services.ssl_service import check_ssl
from app.services.header_service import check_security_headers
from app.services.tech_service import detect_technology
from app.services.severity_service import calculate_overall_severity
from app.routes.scan import router as scan_router
from app.services.ai_recommendation_service import generate_ai_recommendations
from app.config import AI_RECOMMENDATIONS_ENABLED


# ---------------- App Init ----------------
app = FastAPI(
    title="Security Scanner API",
    description="Comprehensive website security scanning tool",
    version="1.0.0"
)

# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app.include_router(scan_router)





# ---------------- Rate Limiting ----------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- Models ----------------
class ScanRequest(BaseModel):
    url: str


# ---------------- Routes ----------------
@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "Security Scanner API",
        "environment": ENVIRONMENT
    }


@app.get("/health")
async def health():
    """Feature availability check"""

    try:
        from app.services.wappalyzer_detector import is_wappalyzer_available
        wappalyzer = is_wappalyzer_available()
    except Exception:
        wappalyzer = False

    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "features": {
            "ssl_check": True,
            "header_check": True,
            "tech_detection": True,
            "wappalyzer": wappalyzer
        }
    }


# @app.post("/api/scan")
# @limiter.limit("5/minute")
# async def scan_website(request: Request, scan_request: ScanRequest):
#     """
#     Main scan endpoint
#     """

#     url = scan_request.url
#     logger.info(f"Received scan request for: {url}")

#     try:
#         # --- Run services ---
#         ssl_result = check_ssl(url)
#         headers_result = check_security_headers(url)
#         tech_result = detect_technology(url)

#         # --- Severity aggregation ---
#         overall_result = calculate_overall_severity(
#             [ssl_result, headers_result, tech_result]
#         )

#         response = {
#             "url": url,
#             "timestamp": datetime.now(timezone.utc).isoformat(),
#             "ssl": ssl_result,
#             "headers": headers_result,
#             "technology": tech_result,
#             "overall": overall_result
#         }

#         logger.info(
#             f"Scan complete for {url} | "
#             f"Overall Severity: {overall_result['overall_severity']}"
#         )
#         if AI_RECOMMENDATIONS_ENABLED:
#          try:
#            response["ai_recommendations"] = generate_ai_recommendations(response)
#          except Exception as e:
#            response["ai_recommendations"] = {
#             "status": "unavailable",
#             "reason": str(e)
#         }

#         return response

    # except Exception as e:
    #     logger.error(f"Scan failed for {url}: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Scan failed")


# ---------------- Local / Prod Run ----------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
