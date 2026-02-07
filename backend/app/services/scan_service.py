from datetime import datetime, timezone
import requests

from app.services.ssl_service import check_ssl
from app.services.header_service import check_security_headers
from app.services.hybrid_detector import HybridTechnologyDetector
from app.services.severity_service import calculate_overall_severity
from app.services.vulnerability_service import VulnerabilityService
from app.services.ai_risk_service import AIRiskService
from app.services.ai_explanation_service import AIExplanationService
from app.services.ai_owasp_service import AIOWASPService
    


def run_all_scans(url: str) -> dict:
    """
    Runs all security checks and returns a unified scan report
    """

    # 1️⃣ Fetch website content
    response = requests.get(url, timeout=15)
    html = response.text
    headers = dict(response.headers)

    # 2️⃣ Run individual security checks
    ssl_result = check_ssl(url)
    headers_result = check_security_headers(url)

    tech_detector = HybridTechnologyDetector()
    technology_result = tech_detector.detect(url=url, html=html, headers=headers)

    # 3️⃣ Vulnerability scanning (FIXED + ENHANCED)
    vuln_service = VulnerabilityService()
    ai_explainer = AIExplanationService()

    SKIP_VULN_CATEGORIES = {"CDN", "WAF", "DNS", "SaaS"}
    vulnerabilities = []

    for name, tech_data in technology_result.get("technologies", {}).items():
        categories = set(tech_data.get("categories", []))

        # ✅ Skip Cloudflare, Akamai, etc.
        if categories & SKIP_VULN_CATEGORIES:
            continue

        version = tech_data.get("version")

        try:
            vulns = vuln_service.check_web_technology(name=name, version=version)

            if vulns:
                # Optional: add AI explanation per CVE
                for v in vulns:
                    v["ai_explanation"] = ai_explainer.explain_vulnerability(
                        cve=v,
                        context={
                            "technology": name,
                            "version": version,
                            "url": url,
                        },
                    )

                vulnerabilities.append(
                    {
                        "technology": name,
                        "version": version,
                        "vulnerabilities": vulns,
                    }
                )

        except Exception as e:
            vulnerabilities.append(
                {
                    "technology": name,
                    "version": version,
                    "error": str(e),
                }
            )

    # 4️⃣ Calculate overall severity & risk
    overall = calculate_overall_severity(
        [
            ssl_result,
            headers_result,
            technology_result,
            {"vulnerabilities": vulnerabilities},
        ]
    )

    # 5️⃣ AI contextual risk adjustment
    ai_risk = AIRiskService()
    ai_adjustment = ai_risk.contextual_risk_adjustment(
        {
            "url": url,
            "technology": technology_result,
            "vulnerabilities": vulnerabilities,
            "ssl": ssl_result,
            "headers": headers_result,
        }
    )

    overall["final_score"] = max(
        0, min(100, overall["risk_score"] + ai_adjustment["risk_modifier"])
    )
    overall["ai"] = ai_adjustment


    
    owasp_service = AIOWASPService()
    owasp_mapping = owasp_service.map_to_owasp({
        "url": url,
        "ssl": ssl_result,
        "headers": headers_result,
        "technology": technology_result,
        "vulnerabilities": vulnerabilities,
        "overall": overall
    })
    
    for i, vuln_group in enumerate(vulnerabilities):
        tech_name = vuln_group["technology"]
        if tech_name in ai_analysis["vulnerability_explanations"]:
            vulnerabilities[i]["ai_insights"] = ai_analysis["vulnerability_explanations"][tech_name]
    
    # 6️⃣ Unified scan report
    return {
        "url": url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ssl": ssl_result,
        "headers": headers_result,
        "technology": technology_result,
        "vulnerabilities": vulnerabilities,
        "overall": overall,
        "owasp": owasp_mapping 
    }

