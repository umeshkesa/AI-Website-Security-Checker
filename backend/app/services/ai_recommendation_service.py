# import json
# import re
# from app.utils.ai_prompt import SYSTEM_PROMPT
# from app.services.ai_client import AIClient
# import hashlib

# ai_client = AIClient()
# AI_CACHE = {}

# def extract_ai_input(scan_result: dict) -> dict:
#     return {
#         "url": scan_result["url"],
#         "overall_severity": scan_result["overall"]["severity"],
#         "server": scan_result["technology"].get("server"),
#         "findings": scan_result["overall"].get("reasons", [])
#     }


# def make_cache_key(scan_result: dict) -> str:
#     key_source = (
#     scan_result["url"]
#     + scan_result["overall"]["severity"]
#     + json.dumps(scan_result["overall"].get("reasons", []), sort_keys=True)
# )


# def _safe_json_parse(text: str) -> dict:
#     """
#     Extract and parse JSON safely from LLM output
#     """
#     try:
#         return json.loads(text)
#     except json.JSONDecodeError:
#         # Try to extract JSON block manually
#         match = re.search(r"\{.*\}", text, re.DOTALL)
#         if match:
#             return json.loads(match.group())
#         raise
    
# def apply_confidence_defaults(ai_data: dict) -> dict:
#     for rec in ai_data.get("recommendations", []):
#         if "confidence" not in rec:
#             priority = rec.get("priority", "Medium")
#             if priority == "High":
#                 rec["confidence"] = 0.9
#             elif priority == "Medium":
#                 rec["confidence"] = 0.75
#             else:
#                 rec["confidence"] = 0.6
#     return ai_data


# def generate_ai_recommendations(scan_result: dict) -> dict:
    
#     cache_key = make_cache_key(scan_result)

#     # ✅ CACHE HIT
#     if cache_key in AI_CACHE:
#         return {
#             "status": "ok",
#             "provider": "cache",
#             "data": AI_CACHE[cache_key]
#         }
#     ai_input = extract_ai_input(scan_result)

#     user_prompt = f"""
# Analyze the following website security scan findings and generate actionable security recommendations.

# Scan context:
# - URL: {ai_input['url']}
# - Overall severity: {ai_input['overall_severity']}
# - Server: {ai_input['server']}

# Findings:
# {json.dumps(ai_input['findings'], indent=2)}

# STRICT OUTPUT RULES:
# - Respond with ONLY valid JSON
# - Do NOT include explanations or markdown
# - Do NOT wrap in ```json

# Required JSON schema:
# {{
#   "summary": "string",
#   "recommendations": [
#     {{
#       "issue": "string",
#       "possible_attack": "string",
#       "impact": "string",
#       "remediation_steps": ["string"],
#       "priority": "Low | Medium | High"
#       "confidence": "number between 0 and 1"
#     }}
#   ]
# }}
# """

#     try:
#         response = ai_client.generate(
#             system_prompt=SYSTEM_PROMPT,
#             user_prompt=user_prompt
#         )

#         parsed = _safe_json_parse(response)
#         parsed = apply_confidence_defaults(parsed)
        
#         AI_CACHE[cache_key] = parsed

#         return {
#             "status": "ok",
#             "provider": "groq",
#             "data": parsed
#         }

#     except Exception as e:
#         # 🔥 NEVER FAIL THE SCAN
#         return {
#             "status": "unavailable",
#             "provider": "groq",
#             "reason": str(e),
#             "fallback": {
#                 "summary": "Automated AI recommendations could not be generated.",
#                 "recommendations": []
#             }
#         }
