import subprocess
import re
import logging

logger = logging.getLogger(__name__)

# Ports that usually increase risk if exposed publicly
HIGH_RISK_PORTS = {21, 22, 23, 25, 3306, 5432, 6379, 27017, 9200}

def run_nmap_scan(host: str) -> dict:
    """
    Safe Nmap scan:
    - TCP connect scan
    - Service & version detection
    - OS detection (best effort)
    - No scripts, no brute-force
    """

    try:
        cmd = [
            "nmap",
            "-sT",          # TCP connect (safe)
            "-sV",          # Service/version detection
            "-O",           # OS detection
            "--top-ports", "100",
            host
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=90
        )

        output = result.stdout

        ports = []
        detected_os = None

        # ---- Parse open ports ----
        for line in output.splitlines():
            match = re.match(
                r"(\d+)/tcp\s+open\s+([\w\-]+)\s*(.*)",
                line
            )
            if match:
                port, service, version = match.groups()
                port = int(port)

                ports.append({
                    "port": port,
                    "service": service,
                    "version": version.strip() or None,
                    "risk": _classify_port_risk(port, service)
                })

        # ---- Parse OS detection ----
        for line in output.splitlines():
            if "OS details:" in line:
                detected_os = line.replace("OS details:", "").strip()
            elif "Running:" in line and not detected_os:
                detected_os = line.replace("Running:", "").strip()

        severity = _calculate_nmap_severity(ports)

        return {
            "service": "nmap",
            "host": host,
            "open_ports": ports,
            "total_open_ports": len(ports),
            "detected_os": detected_os,
            "severity": severity,
            "issue": (
                "Open network services detected"
                if ports else None
            )
        }

    except Exception as e:
        logger.error(f"Nmap scan failed: {e}")
        return {
            "service": "nmap",
            "error": "Nmap scan unavailable"
        }


# -------------------------
# Helper functions
# -------------------------

def _classify_port_risk(port: int, service: str) -> str:
    """
    Context-aware port risk
    """
    if port in HIGH_RISK_PORTS:
        return "HIGH"

    if port in {80, 443}:
        return "LOW"   # web ports are expected

    return "MEDIUM"


def _calculate_nmap_severity(ports: list) -> str:
    if not ports:
        return "INFO"

    if any(p["risk"] == "HIGH" for p in ports):
        return "HIGH"

    return "MEDIUM"
