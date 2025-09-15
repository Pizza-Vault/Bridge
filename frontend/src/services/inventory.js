import api from "../lib/api";
export const getInventory = () => api.get("/api/inventory/status");
