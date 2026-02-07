import requests
import logging
from app.config import NVD_API_KEY, REQUEST_TIMEOUT
from functools import lru_cache

logger = logging.getLogger(__name__)

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

@lru_cache(maxsize=100)  # Cache last 100 products
def nvd_fallback_by_product(product_name: str, max_results: int = 5):
    headers = {}  # Initialize headers
    
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY
    try:
        response = requests.get(
            NVD_API_URL,
            params={
                "keywordSearch": product_name,
                "resultsPerPage": max_results
            },
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            logger.warning(f"NVD returned {response.status_code} for {product_name}")
            return {
                "status": "unavailable",
                "reason": "NVD data unavailable"
            }

        data = response.json()
        

        affected_versions = set()
        cves = []

        for item in data.get("vulnerabilities", []):
            cve = item.get("cve", {})
            cves.append(cve.get("id"))

            for config in cve.get("configurations", []):
                for node in config.get("nodes", []):
                    for match in node.get("cpeMatch", []):
                        version_end = (
                            match.get("versionEndIncluding")
                            or match.get("versionEndExcluding")
                        )
                        if version_end:
                            affected_versions.add(version_end)

        return {
            "status": "ok",
            "affected_versions": sorted(affected_versions),
            "cves": cves[:5]
        }

    except Exception as e:
        logger.error(f"NVD fallback failed for {product_name}: {e}")
        return {
            "status": "unavailable",
            "reason": "NVD lookup failed"
        }
