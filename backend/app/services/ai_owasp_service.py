# import logging
# import json
# from app.services.ai_client import AIClient
# from app.data.owasp_remediation import OWASP_REMEDIATION

# logger = logging.getLogger(__name__)


# class AIOWASPService:
#     def __init__(self):
#         self.ai_client = AIClient()

#     def map_to_owasp(self, scan_results: dict) -> dict:
#         """
#         Maps scan findings to OWASP Top 10 (2021) using AI reasoning
#         """
#         reduced_scan = {
#     "ssl": scan_results.get("ssl"),
#     "headers": scan_results.get("headers"),
#     "technology_vulnerabilities": scan_results.get("technology", {}).get("vulnerabilities", []),
#     "overall": scan_results.get("overall"),
#       }
#         prompt = f"""
# You are a cybersecurity expert.

# Given the following website security scan results, map the findings to
# OWASP Top 10 (2021) categories.

# Rules:
# - Use ONLY the provided scan data
# - Do NOT invent vulnerabilities
# - If evidence is weak, mark as "Potential"
# - Keep explanations concise and professional

# Scan Results:
# {reduced_scan}

# Return STRICT JSON in the following format:
# {{
#   "categories_affected": [
#     {{
#       "owasp_id": "A05:2021",
#       "name": "Security Misconfiguration",
#       "confidence": "Confirmed | Potential | Informational",
#       "reason": "Short explanation"
#     }}
#   ],
#   "compliance_score": 0-10,
#   "ai_summary": "Overall OWASP posture summary",
#   "mapping_details": [
#     {{
#       "finding": "Missing X-Frame-Options header",
#       "mapped_to": "A05:2021",
#       "confidence": "Confirmed"
#     }}
#   ]
# }}
# """

#         try:
#             ai_raw = self.ai_client.generate(prompt)

#             try:
#                 ai_raw = ai_raw.strip()
#                 if ai_raw.startswith("```json"):
#                     ai_raw = ai_raw[7:-3].strip()
#                 elif ai_raw.startswith("```"):
#                     ai_raw = ai_raw[3:-3].strip()  
#                 ai_response = json.loads(ai_raw)
#             except Exception:
#                 logger.error("OWASP AI returned invalid JSON")
#                 return {
#                     "status": "informational",
#                     "message": "OWASP mapping unavailable for this scan."
#                 }

#             final_result = self.enrich_with_remediation(ai_response)
#             finding_links = self.link_findings_to_owasp(scan_results)

#             return {
#                 "status": "ok",
#                 "owasp_mapping": final_result,
#                 "finding_to_owasp_links": finding_links
#             }

#         except Exception as e:
#             logger.error(f"OWASP AI mapping failed: {e}")
#             return {
#                 "status": "informational",
#                 "message": "OWASP mapping could not be generated."
#             }

#     # ---------- Helper methods BELOW ----------

#     def link_findings_to_owasp(self, scan_results: dict) -> list:
#         links = []

#         for header in scan_results.get("headers", {}).get("missing_headers", []):
#             links.append({
#                 "finding": f"Missing {header}",
#                 "owasp": "A05:2021",
#                 "reason": "Security misconfiguration"
#             })

#         for vuln in scan_results.get("technology", {}).get("vulnerabilities", []):
#             links.append({
#                 "finding": vuln.get("technology"),
#                 "owasp": "A06:2021",
#                 "reason": "Potential vulnerable or outdated component"
#             })

#         ssl = scan_results.get("ssl", {})
#         if ssl.get("severity") in ["Medium", "High"]:
#             links.append({
#                 "finding": "SSL/TLS configuration issue",
#                 "owasp": "A02:2021",
#                 "reason": "Cryptographic failure"
#             })

#         return links

#     def enrich_with_remediation(self, owasp_result: dict) -> dict:
#         for category in owasp_result.get("categories_affected", []):
#             owasp_id = category.get("owasp_id")
#             remediation = OWASP_REMEDIATION.get(owasp_id)

#             if remediation:
#                 category["remediation"] = remediation["remediation"]

#         return owasp_result
