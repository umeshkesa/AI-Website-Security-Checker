import requests

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

class NVDClient:
    def __init__(self, api_key=None, timeout=15):
        self.headers = {}
        self.timeout = timeout

        if api_key:
            self.headers["apiKey"] = api_key

    def search(self, product, version=None, limit=10):
        params = {
            "keywordSearch": product,
            "resultsPerPage": limit
        }

        response = requests.get(
            NVD_API_URL,
            headers=self.headers,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return self._parse(response.json())

    def _parse(self, data):
        results = []

        for item in data.get("vulnerabilities", []):
            cve = item["cve"]
            metrics = cve.get("metrics", {})

            score = None
            if "cvssMetricV31" in metrics:
                score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]

            results.append({
                "id": cve["id"],
                "description": cve["descriptions"][0]["value"],
                "cvss": score,
                "source": "NVD"
            })

        return results
