
# backend/app/services/severity_service.py

SEVERITY_ORDER = {
    "INFO": 0,
    "UNKNOWN": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}


def calculate_overall_severity(results: list) -> dict:
    """
    Aggregates all scan results and determines final severity
    (GROUPED, CLEAN, REAL-WORLD STYLE)
    """

    max_severity = "INFO"
    reasons = []
    risk_score = 0

    for result in results:
        if not isinstance(result, dict):
            continue

        # 1️⃣ Direct issues (SSL, headers, etc.)
        issue = result.get("issue")
        severity = result.get("severity")

        if severity:
            max_severity = _max_severity(max_severity, severity)

        if issue:
            reasons.append(issue)
            risk_score += 15

        # 2️⃣ Vulnerability aggregation (GROUPED)
        if "vulnerabilities" in result:
            vuln_sev, vuln_reasons, vuln_score = _analyze_vulnerabilities(
                result["vulnerabilities"]
            )
            max_severity = _max_severity(max_severity, vuln_sev)
            reasons.extend(vuln_reasons)
            risk_score += vuln_score
        
        # Nmap risk handling
        if result.get("service") == "nmap":
          open_ports = result.get("open_ports", [])
          if open_ports:
            max_severity = _max_severity(max_severity, "HIGH")
            reasons.append(
            f"{len(open_ports)} open network ports detected"
           )


    return {
        "severity": max_severity,
        "risk_score": min(100, risk_score),
        "reasons": reasons
    }


# -------------------------
# Internal helpers
# -------------------------

def _analyze_vulnerabilities(vulnerabilities: list):
    """
    GROUP vulnerabilities per technology instead of per CVE
    """
    highest = "INFO"
    reasons = []
    score = 0

    for item in vulnerabilities:
        vulns = item.get("vulnerabilities")
        if not vulns:
            continue

        tech = item.get("technology", "Unknown")
        version = item.get("version") or "unknown"

        counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "UNKNOWN": 0
        }

        tech_max = "INFO"

        for vuln in vulns:
            sev = vuln.get("severity", "UNKNOWN")
            counts[sev] += 1
            tech_max = _max_severity(tech_max, sev)

        # Update global severity
        highest = _max_severity(highest, tech_max)

        # ONE clean reason per technology
        reasons.append(
            f"{tech} ({version}) has known vulnerabilities "
            f"({counts['CRITICAL']} CRITICAL, "
            f"{counts['HIGH']} HIGH, "
            f"{counts['MEDIUM']} MEDIUM)"
        )

        # Score per technology (not per CVE)
        score += {
            "CRITICAL": 25,
            "HIGH": 20,
            "MEDIUM": 10,
            "LOW": 5,
            "UNKNOWN": 2
        }.get(tech_max, 0)

    return highest, reasons, score


def _max_severity(current: str, new: str) -> str:
    """
    Returns higher severity between two
    """
    if SEVERITY_ORDER.get(new, 0) > SEVERITY_ORDER.get(current, 0):
        return new
    return current

