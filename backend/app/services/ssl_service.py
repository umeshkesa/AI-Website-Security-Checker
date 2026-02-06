import ssl
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


def check_ssl(url: str) -> dict:
    logger.info(f"Checking SSL for {url}")

    result = {
        "service": "ssl",
        "enabled": False,
        "valid": False,
        "expiry_date": None,
        "issuer": None,
        "tls_version": None,
        "severity": "Low",
        "issue": None
    }

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname

        # Validate URL
        if not hostname:
            result["issue"] = "Invalid URL"
            result["severity"] = "Medium"
            return result

        if parsed.scheme != "https":
            result["issue"] = "HTTPS not enabled"
            result["severity"] = "High"
            return result

        result["enabled"] = True

        context = ssl.create_default_context()

        # Open TLS connection
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

                result["valid"] = True
                result["tls_version"] = ssock.version()
                result["issuer"] = dict(x[0] for x in cert.get("issuer", []))

                expiry = cert.get("notAfter")
                if expiry:
                    expiry_date = datetime.strptime(
                        expiry, "%b %d %H:%M:%S %Y %Z"
                    ).replace(tzinfo=timezone.utc)

                    result["expiry_date"] = expiry_date.isoformat()

                    if expiry_date < datetime.now(timezone.utc):
                        result["issue"] = "SSL certificate expired"
                        result["severity"] = "Critical"
                    else:
                        result["severity"] = "Low"

    except ssl.SSLError as e:
        logger.error(f"SSL error for {url}: {str(e)}")
        result["issue"] = "Invalid or misconfigured SSL certificate"
        result["severity"] = "High"

    except socket.timeout:
        logger.error(f"SSL timeout for {url}")
        result["issue"] = "SSL connection timed out"
        result["severity"] = "Medium"

    except Exception as e:
        logger.error(f"SSL check failed for {url}: {str(e)}")
        result["issue"] = "SSL check failed"
        result["severity"] = "Medium"
        result["error_details"] = str(e)

    return result
