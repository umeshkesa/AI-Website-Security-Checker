import requests

OSV_API = "https://api.osv.dev/v1/query"

class OSVClient:
    def query(self, ecosystem, package, version):
        payload = {
            "package": {
                "name": package,
                "ecosystem": ecosystem
            },
            "version": version
        }

        response = requests.post(OSV_API, json=payload, timeout=10)
        response.raise_for_status()

        return self._parse(response.json())

    def _parse(self, data):
        vulns = []

        for v in data.get("vulns", []):
            vulns.append({
                "id": v["id"],
                "summary": v.get("summary"),
                "details": v.get("details"),
                "source": "OSV"
            })

        return vulns
