import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000",
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  config.headers["Authorization"] = "Bearer demo-token";
  config.headers["X-Timestamp"] = new Date().toISOString();
  config.headers["X-Nonce"] =
    self.crypto?.randomUUID?.() || Math.random().toString(36).slice(2);
  return config;
});

export default api;
