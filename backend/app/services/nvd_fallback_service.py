import requests
import logging
from functools import lru_cache
from app.config import NVD_API_KEY

logger = logging.getLogger(__name__)

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

SKIP_NVD_PRODUCTS = {
    "Google Analytics",
    "Google Tag Manager",
    "Google Font API",
    "Cloudflare",
}

@lru_cache(maxsize=100)
def nvd_fallback_by_product(product_name: str, max_results: int = 5):
    headers = {}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY

    try:
        response = requests.get(
            NVD_API_URL,
            params={
                "keywordSearch": product_name.replace(" ", "+"),
                "resultsPerPage": max_results
            },
            headers=headers,
            timeout=10
        )
        
        # 🚫 Never expose HTTP failure
        if response.status_code != 200:
            logger.info(f"NVD unavailable for {product_name}")
            return {
                "status": "informational",
                "message": "No confirmed CVEs available from NVD."
            }

        data = response.json()
        vulns = data.get("vulnerabilities", [])
        
        if product_name in SKIP_NVD_PRODUCTS:
         return {
             "status": "informational",
             "message": "Vulnerability scanning not applicable for this technology."
         }
        # ✅ Valid response but no CVEs
        if not vulns:
            return {
                "status": "informational",
                "message": "No known CVEs listed for this technology."
            }

        affected_versions = set()
        cves = []

        for item in vulns:
            cve = item.get("cve", {})
            cves.append(cve.get("id"))

            for config in cve.get("configurations", []):
                for node in config.get("nodes", []):
                    for match in node.get("cpeMatch", []):
                        # ⚠️ Only vulnerable entries
                        if not match.get("vulnerable", False):
                            continue

                        version_end = (
                            match.get("versionEndIncluding")
                            or match.get("versionEndExcluding")
                        )
                        if version_end:
                            affected_versions.add(version_end)

        return {
            "status": "potential",
            "affected_versions": sorted(affected_versions),
            "cves": cves[:5]
        }

    except Exception:
        # 🚫 Never leak exception details
        logger.info(f"NVD lookup skipped for {product_name}")
        return {
            "status": "informational",
            "message": "Vulnerability data unavailable."
        }
