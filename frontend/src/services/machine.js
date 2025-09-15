import api from "../lib/api";
export const setMode = (mode) => api.post("/api/machine/set_mode", { mode });
