import json
import logging
from app.services.ai_client import AIClient

logger = logging.getLogger(__name__)


class AIAnalysisService:
    def __init__(self):
        self.client = AIClient()

    def analyze(self, scan_summary: dict) -> dict:
        system_prompt = "You are a cybersecurity expert."

        user_prompt = f"""
Given the following website security findings, do ALL of the following:

1. Map findings to OWASP Top 10 (2021)
2. Assess overall risk level
3. Open ports and exposed services increase attack surface
4. SSH, databases, and admin services significantly increase risk
5. Provide security recommendations
6. Give a short human-readable explanation


Rules:
- Use ONLY provided data
- Do NOT invent vulnerabilities
- Return STRICT JSON only
- No markdown, no explanations outside JSON

Scan Data:
{json.dumps(scan_summary, indent=2)}

Return JSON in this format:
{{
  "owasp": {{ }},
  "risk": {{ }},
  "recommendations": [],
  "explanation": "string"
}}
"""

        raw = self.client.generate(system_prompt, user_prompt)

        if not raw or not raw.strip():
            logger.error("AI returned empty response")
            return self._fallback()

        raw = raw.strip()

        # 1️⃣ Remove markdown if present
        if raw.startswith("```"):
            raw = raw.strip("`")
            raw = raw.replace("json", "", 1).strip()

        # 2️⃣ Try direct JSON parse
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # 3️⃣ Try extracting JSON block
        try:
            start = raw.index("{")
            end = raw.rindex("}") + 1
            return json.loads(raw[start:end])
        except Exception:
            logger.error("AI returned invalid JSON")
            return self._fallback()

    def _fallback(self) -> dict:
        """
        Safe fallback if AI fails
        """
        return {
            "owasp": {
                "status": "informational",
                "message": "OWASP analysis unavailable"
            },
            "risk": {
                "confidence": "LOW",
                "reason": "AI response could not be parsed"
            },
            "recommendations": [],
            "explanation": "AI analysis could not be generated for this scan."
        }
