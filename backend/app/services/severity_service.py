# backend/app/services/severity_service.py

SEVERITY_ORDER = {
    "INFO": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}


def calculate_overall_severity(results: list) -> dict:
    """
    Aggregates all scan results and determines final severity
    """

    max_severity = "INFO"
    reasons = []

    for result in results:
        if not isinstance(result, dict):
            continue

        # 1️⃣ Aggregate severity
        severity = result.get("severity")
        if isinstance(severity, str):
            severity = severity.upper()
        if severity:
            max_severity = _max_severity(max_severity, severity)

        # 2️⃣ Prefer human-readable issue text
        issue = result.get("issue")
        if issue:
            reasons.append(issue)

        # 3️⃣ Vulnerability aggregation
        if "vulnerabilities" in result:
            vuln_severity, vuln_reasons = _analyze_vulnerabilities(
                result["vulnerabilities"]
            )
            max_severity = _max_severity(max_severity, vuln_severity)
            reasons.extend(vuln_reasons)

    return {
        "severity": max_severity,
        "risk_score": SEVERITY_ORDER[max_severity] * 25,
        "reasons": list(dict.fromkeys(reasons))  # preserve order, remove dups
    }


# -------------------------
# Internal helpers
# -------------------------

def _analyze_vulnerabilities(vulnerabilities: list):
    """
    Determines severity based on CVEs
    """
    highest = "INFO"
    reasons = []

    for item in vulnerabilities:
        # Skip failed / error-only entries
        if "vulnerabilities" not in item:
            continue

        tech = item.get("technology", "Unknown")

        for vuln in item.get("vulnerabilities", []):
            sev = vuln.get("severity", "INFO")
            highest = _max_severity(highest, sev)

            cve_id = vuln.get("id")
            if cve_id:
                reasons.append(
                    f"{tech} affected by {cve_id} ({sev})"
                )

    return highest, reasons


def _max_severity(current: str, new: str) -> str:
    """
    Returns higher severity between two
    """
    if SEVERITY_ORDER.get(new, 0) > SEVERITY_ORDER.get(current, 0):
        return new
    return current
