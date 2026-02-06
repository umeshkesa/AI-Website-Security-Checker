from app.services.ai_client import AIClient


class AIExplanationService:
    def __init__(self):
        try:
            self.ai = AIClient()
        except Exception:
            # If GROQ_API_KEY is missing or AI init fails
            self.ai = None

    def explain_vulnerability(self, cve: dict, context: dict) -> str:
        """
        Explain a vulnerability in simple human language
        """

        # Fallback if AI is unavailable
        if not self.ai:
            return (
                "This vulnerability may allow attackers to compromise the system "
                "if it is exploited."
            )

        system_prompt = (
            "You are a cybersecurity expert explaining vulnerabilities "
            "to non-security developers in simple terms."
        )

        user_prompt = f"""
Vulnerability:
{cve}

Website context:
{context}

Explain:
- What the vulnerability is
- How it can be exploited
- Why it matters for this website

Rules:
- Max 3 lines
- Simple language
- No speculation
"""

        try:
            return self.ai.generate(system_prompt, user_prompt)
        except Exception:
            return (
                "This vulnerability could pose a security risk to the website "
                "if an attacker exploits it."
            )
