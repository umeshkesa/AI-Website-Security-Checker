import requests
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "severity": "Medium",
        "recommendation": "Add Content-Security-Policy header to mitigate XSS attacks."
    },
    "X-Frame-Options": {
        "severity": "Medium",
        "recommendation": "Add X-Frame-Options header to prevent clickjacking."
    },
    "X-Content-Type-Options": {
        "severity": "Low",
        "recommendation": "Add X-Content-Type-Options: nosniff to prevent MIME sniffing."
    },
    "Strict-Transport-Security": {
        "severity": "High",
        "recommendation": "Enable HSTS to enforce secure HTTPS connections."
    },
    "Permissions-Policy": {
        "severity": "Low",
        "recommendation": "Add Permissions-Policy to control browser features."
    },
    "Referrer-Policy": {
        "severity": "Low",
        "recommendation": "Add Referrer-Policy to control referrer information."
    },
    "X-XSS-Protection": {
        "severity": "Low",
        "recommendation": "Add X-XSS-Protection header (legacy browsers)."
    }
}


def check_security_headers(url: str) -> dict:
    logger.info(f"Checking security headers for {url}")

    result = {
        "service": "headers",
        "checked": True,
        "missing_headers": [],
        "present_headers": {},
        "severity": "Low",
        "issue": None,
        "recommendations": []
    }

    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            result["issue"] = "Invalid URL"
            result["severity"] = "Medium"
            return result

        # HEAD first (fast)
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=10,
            headers={"User-Agent": "SecurityScanner/1.0"}
        )

        # Fallback to GET if headers are empty
        if not response.headers:
            response = requests.get(url, timeout=10)

        headers = response.headers

        severity_rank = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        highest_severity = "Low"

        for header, meta in SECURITY_HEADERS.items():
            if header in headers:
                result["present_headers"][header] = headers.get(header)
            else:
                result["missing_headers"].append(header)
                result["recommendations"].append(meta["recommendation"])

                if severity_rank[meta["severity"]] > severity_rank[highest_severity]:
                    highest_severity = meta["severity"]

        result["severity"] = highest_severity

        if result["missing_headers"]:
            result["issue"] = "Missing security headers"

        # Extra HSTS validation
        if "Strict-Transport-Security" in headers:
            hsts_value = headers["Strict-Transport-Security"]
            if "preload" not in hsts_value.lower():
                result["recommendations"].append(
                    "HSTS present but missing 'preload' directive"
                )

    except requests.exceptions.Timeout:
        logger.error(f"Header check timed out for {url}")
        result["issue"] = "Header check timed out"
        result["severity"] = "Medium"

    except Exception as e:
        logger.error(f"Header check failed for {url}: {str(e)}")
        result["issue"] = "Header service failed"
        result["severity"] = "Medium"
        result["error_details"] = str(e)

    return result
