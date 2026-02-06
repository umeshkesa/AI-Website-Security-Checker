import logging
from typing import Dict
from app.services.wappalyzer_detector import WappalyzerDetector
from app.services.regex_detector import RegexDetector
from app.services.header_detector import HeaderDetector

logger = logging.getLogger(__name__)


class HybridTechnologyDetector:
    """
    Detects technologies using multiple methods.
    NO vulnerability or risk logic here.
    """

    def __init__(self):
        self.wappalyzer = WappalyzerDetector()
        self.regex = RegexDetector()
        self.header = HeaderDetector()

    def detect(self, url: str, html: str, headers: dict) -> Dict:
        result = {
            "success": False,
            "technologies": {},
            "total_count": 0,
            "detection_summary": {
                "wappalyzer_count": 0,
                "regex_count": 0,
                "header_count": 0,
                "methods_used": []
            },
            "cloudflare_detected": False,
            "error": None
        }

        try:
            all_technologies = {}

            # 1️⃣ Wappalyzer
            wap = self.wappalyzer.detect(url, html, headers)
            if wap.get("success"):
                result["detection_summary"]["wappalyzer_count"] = wap["count"]
                result["detection_summary"]["methods_used"].append("wappalyzer")

                for name, data in wap["technologies"].items():
                    data["detection_methods"] = ["wappalyzer"]
                    all_technologies[name] = data

            # 2️⃣ Regex
            regex = self.regex.detect(url, html, headers)
            if regex.get("success"):
                result["detection_summary"]["regex_count"] = regex["count"]
                result["detection_summary"]["methods_used"].append("regex")

                for name, data in regex["technologies"].items():
                    if name in all_technologies:
                        all_technologies[name]["detection_methods"].append("regex")
                        if not all_technologies[name].get("version"):
                            all_technologies[name]["version"] = data.get("version")
                    else:
                        data["detection_methods"] = ["regex"]
                        all_technologies[name] = data

            # 3️⃣ Headers
            header = self.header.detect(headers)
            if header.get("success"):
                result["detection_summary"]["header_count"] = header["count"]
                result["detection_summary"]["methods_used"].append("headers")
                result["cloudflare_detected"] = header["cloudflare_detected"]

                for name, data in header["technologies"].items():
                    if name in all_technologies:
                        all_technologies[name]["detection_methods"].append("headers")
                        if data.get("version"):
                            all_technologies[name]["version"] = data["version"]
                    else:
                        data["detection_methods"] = ["headers"]
                        all_technologies[name] = data

            result["success"] = True
            result["technologies"] = all_technologies
            result["total_count"] = len(all_technologies)

        except Exception as e:
            logger.error(f"Hybrid detection failed: {e}")
            result["error"] = str(e)

        return result
