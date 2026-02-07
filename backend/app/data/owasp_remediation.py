OWASP_REMEDIATION = {
    "A05:2021": {
        "name": "Security Misconfiguration",
        "remediation": [
            "Add missing security headers (X-Frame-Options, CSP, HSTS).",
            "Disable unnecessary services and features.",
            "Ensure secure default configurations."
        ]
    },
    "A06:2021": {
        "name": "Vulnerable and Outdated Components",
        "remediation": [
            "Identify exact component versions in use.",
            "Upgrade to the latest secure versions.",
            "Monitor official security advisories and CVE feeds."
        ]
    },
    "A02:2021": {
        "name": "Cryptographic Failures",
        "remediation": [
            "Use TLS 1.2 or higher.",
            "Replace weak ciphers and certificates.",
            "Ensure certificates are valid and not expired."
        ]
    }
}
