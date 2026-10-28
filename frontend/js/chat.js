import { startSession, sendAnswer, getStatus, getApiBase, setApiBase } from "./api.js";

const DIMS = [["situacion","Situación"],["tarea","Tarea"],["accion","Acción"],["resultado","Resultado"],["claridad_tecnica","Claridad técnica"],["pertinencia","Pertinencia"]];
const $ = (id) => document.getElementById(id);
let sessionId = null, total = 0;

// --- Panel de métricas (RF-04) ---
function renderMetrics(ev) {
  $("dims").innerHTML = DIMS.map(([k, label]) => {
    const v = ev ? ev[k] : 0;
    const cls = !ev ? "" : v >= 4 ? "ok" : v >= 3 ? "mid" : "low";   // umbral RN-03: < 3 = bajo
    return `<div class="dim"><div class="dim-head"><span>${label}</span><span>${ev ? v + "/5" : "–"}</span></div>
            <div class="bar ${cls}" role="img" aria-label="${label} ${v} de 5"><span style="width:${v * 20}%"></span></div></div>`;
  }).join("");
}
function add(text, cls) { const d = document.createElement("div"); d.className = "msg " + cls; d.textContent = text; $("log").append(d); d.scrollIntoView({ block: "end" }); }

// --- Inicio de sesión (RF-01 + RF-02) ---
// --- Conexión con el backend y modelos de Ollama ---
async function refreshStatus() {
  $("api_url").value = getApiBase(); const sel = $("model"), st = $("conn-status");
  try {
    const s = await getStatus();
    if (s.provider === "ollama" && !s.ok) { st.textContent = "Ollama no responde: ábrelo (ollama serve). " + (s.detail || ""); st.className = "error"; sel.innerHTML = '<option value="fake">Demo sin LLM</option>'; return; }
    const opts = s.provider === "ollama" ? s.models.map((m) => `<option ${m === s.default ? "selected" : ""}>${m}</option>`) : [];
    sel.innerHTML = opts.join("") + '<option value="fake">Demo sin LLM (FakeLLM)</option>';
    st.className = "progress"; st.textContent = s.provider === "ollama" ? `Ollama conectado · ${s.models.length} modelo(s) instalado(s)` : `Backend conectado (proveedor: ${s.provider})`;
  } catch (e) { st.textContent = e.message; st.className = "error"; }
}
$("api_url").addEventListener("change", (e) => { setApiBase(e.target.value); refreshStatus(); });
refreshStatus();

$("setup").addEventListener("submit", async (e) => {
  e.preventDefault(); $("setup-error").textContent = "";
  const f = new FormData(e.target);
  try {
    const r = await startSession({ target_role: f.get("target_role"), seniority: f.get("seniority"), cv_text: f.get("cv_text"),
      job_description: f.get("job_description"), num_questions: Number(f.get("num_questions")), model: $("model").value || null });
    sessionId = r.session_id; total = r.total_questions;
    $("setup-card").classList.add("hidden"); $("chat-card").classList.remove("hidden");
    $("progress").textContent = `Pregunta 1 de ${total}`; add(r.question, "bot"); renderMetrics(null);
  } catch (err) { $("setup-error").textContent = err.message; }
});

// --- Envío de respuesta (RF-03) ---
$("composer").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = $("answer").value.trim(); if (!text) return;
  $("send").disabled = true; add(text, "me"); $("progress").textContent = "Evaluando tu respuesta… (los modelos locales pueden tardar)"; $("answer").value = "";
  try {
    const r = await sendAnswer(sessionId, text);
    renderMetrics(r.evaluation);
    $("status").textContent = r.status === "profundizar_pregunta" ? "Profundizando" : r.status === "finalizar_entrevista" ? "Finalizada" : "Siguiente tema";
    $("status").classList.toggle("deepen", r.status === "profundizar_pregunta");
    $("progress").textContent = `Respuestas: ${r.answered_count} de ${r.total_questions}`;
    if (r.report_ready) { add("Terminaste la entrevista. Tu reporte está listo.", "note"); location.href = `report.html?sid=${sessionId}`; }
    else add(r.next_question, "bot");
  } catch (err) { add(err.message, "note"); }   // incluye el mensaje de RF-03 flujo 6A.3
  $("send").disabled = false;
});
renderMetrics(null);
