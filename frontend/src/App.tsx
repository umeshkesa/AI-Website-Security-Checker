import { useState } from "react";
import { scanWebsite } from "./services/api";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    setLoading(true);
    try {
      const data = await scanWebsite(url);
      setResult(data);
    } catch (err) {
      alert("Scan failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Security Scanner</h1>

      <input
        type="text"
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button onClick={handleScan} disabled={loading}>
        {loading ? "Scanning..." : "Scan"}
      </button>

      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}

export default App;
