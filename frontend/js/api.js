// Cliente HTTP. Los nombres de campos vienen de backend/app/schemas/api.py (mantener sincronizados).
export const API_BASE = window.API_BASE || "http://localhost:8000";
const headers = { "Content-Type": "application/json", "X-Role": "student" }; // stub dev (T-114)

async function call(path, options = {}) {
  const res = await fetch(API_BASE + path, { headers, ...options });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail || `Error ${res.status}`);
  return body;
}
export const startSession = (data) => call("/api/sessions", { method: "POST", body: JSON.stringify(data) });
export const sendAnswer = (id, answer) => call(`/api/sessions/${id}/answer`, { method: "POST", body: JSON.stringify({ answer }) });
export const getReport = (id) => call(`/api/sessions/${id}/report`);
export const sendFeedback = (id, csat, comment) => call(`/api/sessions/${id}/feedback`, { method: "POST", body: JSON.stringify({ csat, comment }) });
