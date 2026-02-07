from fastapi import APIRouter
from pydantic import BaseModel

from app.services.scan_service import run_all_scans
from app.services.ai_recommendation_service import generate_ai_recommendations
from app.services.ai_owasp_service import AIOWASPService
from app.config import AI_RECOMMENDATIONS_ENABLED

router = APIRouter(
    prefix="/scan",
    tags=["Scan"]
)

class ScanRequest(BaseModel):
    url: str


@router.post("/")
def scan_url(payload: ScanRequest):
    print("🔥 SCAN ROUTE HIT")

    
    scan_result = run_all_scans(payload.url)

    
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

    
    try:
        owasp_service = AIOWASPService()
        scan_result["owasp"] = owasp_service.map_to_owasp(scan_result)
    except Exception as e:
        scan_result["owasp"] = {
            "status": "unavailable",
            "reason": str(e)
        }

   
    return scan_result
