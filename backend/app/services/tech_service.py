import requests
import logging
from app.utils.url_validator import validate_url
from app.services.hybrid_detector import HybridTechnologyDetector
from app.services.nvd_fallback_service import nvd_fallback_by_product
from app.config import REQUEST_TIMEOUT, USER_AGENT

logger = logging.getLogger(__name__)


def detect_technology(url: str) -> dict:
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

        result["server"] = headers.get("Server")
        result["powered_by"] = headers.get("X-Powered-By")

        # Detect technologies
        detector = HybridTechnologyDetector()
        detection_result = detector.detect(normalized_url, html, headers)

        if not detection_result["success"]:
            result["issue"] = detection_result.get("error", "Technology detection failed")
            result["severity"] = "Medium"
            return result

        # Populate base results
        result["technologies"] = detection_result["technologies"]
        result["total_count"] = detection_result["total_count"]
        result["detection_methods_used"] = detection_result["detection_summary"]["methods_used"]
        result["cloudflare_detected"] = detection_result["cloudflare_detected"]

        # ---------------- NVD FALLBACK (SANITIZED) ----------------
        for tech_name, tech in result["technologies"].items():
            nvd_info = nvd_fallback_by_product(tech_name)

            # Potential risk
            if nvd_info.get("status") == "potential":
                result["vulnerabilities"].append({
                    "technology": tech_name,
                    "confidence": "Potential",
                    "affected_versions": nvd_info.get("affected_versions", []),
                    "reference_cves": nvd_info.get("cves", []),
                    "message": (
                        f"Historical vulnerabilities exist for {tech_name}. "
                        "Verify the deployed version."
                    ),
                    "recommendation": (
                        f"Verify the {tech_name} version and update "
                        "to the latest secure release if outdated."
                    )
                })

            # Informational (default & safe)
            if nvd_info.get("status") == "potential":
                 result["vulnerabilities"].append({
                    "technology": tech_name,
                    "confidence": "potential",
                    "message": "No confirmed CVEs available from public databases.",
                    "recommendation": "No immediate action required."
                })

        # ---------------- RECOMMENDATIONS ----------------
        for vuln in result["vulnerabilities"][:5]:
            if vuln.get("recommendation"):
                result["recommendations"].append(vuln["recommendation"])

        if result["cloudflare_detected"]:
            result["recommendations"].append(
                "Cloudflare CDN detected – verify origin server IP is not exposed."
            )

        if result["total_count"] > 15:
            result["recommendations"].append(
                f"{result['total_count']} technologies detected – review unnecessary dependencies."
            )

        # Severity adjustment
        if any(v["confidence"] == "Potential" for v in result["vulnerabilities"]):
            result["severity"] = "Medium"

    except requests.exceptions.Timeout:
        result["issue"] = "Technology detection timed out"
        result["severity"] = "Medium"

    except requests.exceptions.RequestException:
        result["issue"] = "Failed to fetch website"
        result["severity"] = "Medium"

    except Exception:
        result["issue"] = "Technology detection failed"
        result["severity"] = "Medium"

    return result
