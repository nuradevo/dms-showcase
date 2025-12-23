import axios from "axios";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export function apiClient(token?: string) {
  const instance = axios.create({
    baseURL: apiBase,
    headers: { "Content-Type": "application/json" },
  });
  if (token) instance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  return instance;
}