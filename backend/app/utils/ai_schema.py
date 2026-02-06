AI_RESPONSE_SCHEMA = {
    "ai_summary": "string",
    "recommendations": [
        {
            "service": "string",
            "issue": "string",
            "severity": "string",
            "explanation": "string",
            "possible_attack": "string",
            "impact": "string",
            "remediation_steps": ["string"],
            "configuration_examples": {
                "nginx": "string",
                "apache": "string"
            },
            "priority": "string"
        }
    ]
}
