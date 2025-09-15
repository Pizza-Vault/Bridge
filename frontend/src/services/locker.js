import api from "../lib/api";
export const openLocker = (locker_id) =>
  api.post("/api/locker/open", { locker_id });
