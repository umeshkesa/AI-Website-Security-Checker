import { useState } from "react";
import { scanWebsite} from "./api/scanApi";
import type { ScanResponse } from "./api/scanApi";

function App() {
  const [url, setUrl] = useState<string>("");
  const [result, setResult] = useState<ScanResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await scanWebsite(url);
      setResult(data);
    } catch (err) {
      setError("Scan failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Website Security Checker</h1>

      <input
        type="text"
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "320px", marginRight: "10px" }}
      />

      <button onClick={handleScan} disabled={!url || loading}>
        {loading ? "Scanning..." : "Scan Website"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Scan Result</h3>
          <p>
            <strong>Severity:</strong> {result.overall.severity}
          </p>
          <p>
            <strong>Risk Score:</strong> {result.overall.final_score}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
