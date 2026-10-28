// Cliente HTTP. Campos de backend/app/schemas/api.py (mantener sincronizados).
// La URL del backend se guarda en localStorage: en GitHub Pages apunta a TU localhost.
const KEY = "interviewai_api";
export const getApiBase = () => localStorage.getItem(KEY) || window.API_BASE || "http://localhost:8000";
export const setApiBase = (url) => localStorage.setItem(KEY, url.replace(/\/+$/, ""));
const headers = { "Content-Type": "application/json", "X-Role": "student" }; // stub dev (T-114)

async function call(path, options = {}) {
  let res;
  try { res = await fetch(getApiBase() + path, { headers, ...options }); }
  catch { throw new Error(`No se pudo conectar con el backend en ${getApiBase()}. ¿Está corriendo uvicorn?`); }
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail || `Error ${res.status}`);
  return body;
}
export const getStatus = () => call("/api/llm/status");
export const startSession = (data) => call("/api/sessions", { method: "POST", body: JSON.stringify(data) });
export const sendAnswer = (id, answer) => call(`/api/sessions/${id}/answer`, { method: "POST", body: JSON.stringify({ answer }) });
export const getReport = (id) => call(`/api/sessions/${id}/report`);
export const sendFeedback = (id, csat, comment) => call(`/api/sessions/${id}/feedback`, { method: "POST", body: JSON.stringify({ csat, comment }) });
