from app.services.ai_client import AIClient
import json


class AIRiskService:
    def __init__(self):
        try:
            self.ai = AIClient()
        except Exception:
            # If GROQ_API_KEY is missing or AI fails
            self.ai = None

    def contextual_risk_adjustment(self, scan_report: dict) -> dict:
        """
        Adjust severity score using AI reasoning
        """

        if not self.ai:
            return {
                "risk_modifier": 0,
                "confidence": "LOW",
                "reason": "AI disabled or API key not configured"
            }

        system_prompt = (
            "You are a senior cybersecurity expert. "
            "You analyze vulnerability scan results and adjust risk realistically."
        )

        user_prompt = f"""
Scan data:
{scan_report}

Rules:
- Do NOT invent vulnerabilities
- Do NOT change CVSS scores
- Only adjust based on exploitability, exposure, and impact

Return STRICT JSON ONLY:
{{
  "risk_modifier": -20 to 20,
  "confidence": "LOW|MEDIUM|HIGH",
  "reason": "short explanation"
}}
"""

        response = self.ai.generate(system_prompt, user_prompt)

        try:
            return json.loads(response)
        except Exception:
            return {
                "risk_modifier": 0,
                "confidence": "LOW",
                "reason": "AI response could not be parsed"
            }
