from fastapi import APIRouter
from pydantic import BaseModel

from app.services.scan_service import run_all_scans
from app.services.ai_recommendation_service import generate_ai_recommendations
from app.config import AI_RECOMMENDATIONS_ENABLED

router = APIRouter(
    prefix="/scan",
    tags=["Scan"]
)


# ✅ Request schema
class ScanRequest(BaseModel):
    url: str


@router.post("/")
def scan_url(payload: ScanRequest):
    print("🔥 SCAN ROUTE HIT")
    # 1️⃣ Run core scan
    scan_result = run_all_scans(payload.url)

    # 2️⃣ Attach AI recommendations (optional)
    if AI_RECOMMENDATIONS_ENABLED:
        try:
            print("🤖 AI ENABLED – CALLING AI")
            scan_result["ai_recommendations"] = generate_ai_recommendations(
                scan_result
            )
        except Exception as e:
            scan_result["ai_recommendations"] = {
                "status": "unavailable",
                "reason": str(e)
            }

    # 3️⃣ Return full scan + AI
    return scan_result


# @router.post("/test-ai")
# def test_ai():
#     fake_scan = {
#         "url": "https://example.com",
#         "overall": {
#             "overall_severity": "High",
#             "findings": [
#                 {
#                     "service": "headers",
#                     "severity": "High",
#                     "issue": "Missing security headers"
#                 }
#             ]
#         },
#         "technology": {
#             "server": "cloudflare"
#         }
#     }

#     return generate_ai_recommendations(fake_scan)
