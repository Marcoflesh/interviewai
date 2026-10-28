import { getReport, sendFeedback } from "./api.js";
const sid = new URLSearchParams(location.search).get("sid");
const LABEL = { situacion:"Situación", tarea:"Tarea", accion:"Acción", resultado:"Resultado", claridad_tecnica:"Claridad técnica", pertinencia:"Pertinencia" };
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));

try {
  const r = await getReport(sid);
  const evo = r.score_evolution_rate == null ? "Primera sesión" : `${r.score_evolution_rate.toFixed(1)}% vs. tus sesiones anteriores`;
  document.getElementById("report").innerHTML = `
    <div class="card"><div class="score">${r.session_score} / 5</div><p>${evo}</p></div>
    <div class="card"><h2>Promedio por dimensión</h2>${Object.entries(r.dimension_averages).map(([k, v]) => `<p>${LABEL[k]}: <strong>${v}</strong></p>`).join("")}</div>
    <h2>Tus dos respuestas más débiles</h2>
    <div class="compare">${r.weakest_answers.map((w) => `<div class="card"><h3>Tu respuesta</h3><p>${esc(w.answer)}</p>
      <h3>Cómo mejorarla</h3><p>${w.ejemplo_mejorado ? esc(w.ejemplo_mejorado) : "No pudimos generar el ejemplo. Intenta de nuevo más tarde."}</p></div>`).join("")}</div>
    <div class="card"><h2>Plan de acción</h2><p>Enfócate en: ${r.action_plan.focus_dimensions.map((d) => LABEL[d]).join(" y ")}.</p>
      <ul>${r.action_plan.resources.map((x) => `<li><a href="${esc(x.url)}">${esc(x.title)}</a></li>`).join("") || "<li>Aún no hay recursos curados (RF-08).</li>"}</ul></div>`;
} catch (e) { document.getElementById("report").innerHTML = `<p class="error">${esc(e.message)}</p>`; }

document.getElementById("pdf").addEventListener("click", () => window.print());     // TODO T-402: PDF desde el backend
document.getElementById("csat").addEventListener("submit", async (e) => {            // RF-06
  e.preventDefault();
  await sendFeedback(sid, Number(new FormData(e.target).get("csat")), new FormData(e.target).get("comment"));
  e.target.innerHTML = "<p>Gracias por tu opinión.</p>";
});
