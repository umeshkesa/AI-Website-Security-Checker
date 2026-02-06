import axios from "axios";

const API_BASE = "http://localhost:8000";

export interface ScanResponse {
  url: string;
  overall: {
    severity: string;
    final_score: number;
  };
}

export const scanWebsite = async (url: string): Promise<ScanResponse> => {
  const response = await axios.post(`${API_BASE}/scan`, {
    url,
  });
  return response.data;
};
