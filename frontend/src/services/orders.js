import api from "../lib/api";

export const createOrder = (payload) => api.post("/api/order/create", payload);
export const getOrderStatus = (order_id) =>
  api.get("/api/order/status", { params: { order_id } });
export const completeOrder = (order_id) =>
  api.post("/api/order/complete", { order_id });
