const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function scanWebsite(url: string) {
  const response = await fetch(`${API_BASE_URL}/scan/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url })
  });

  if (!response.ok) {
    throw new Error("Scan failed");
  }

  return response.json();
}
