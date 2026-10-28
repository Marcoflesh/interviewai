"""Demo en terminal del flujo completo con FakeLLM (sin red). Uso: cd backend && python -m app.cli_demo"""
from app.agents.graph import build_graph
from app.services.llm_client import FakeLLM
from app.services.report import build_report


def main() -> None:
    g = build_graph(FakeLLM())
    s = g.invoke({"target_role": "Backend", "seniority": "junior", "cv_text": "", "job_description": "", "max_turns": 5})
    while s["status"] != "finalizar_entrevista":
        print(f"\nEntrevistador: {s['current_question']}")
        s = g.invoke({**s, "current_answer": input("Tu respuesta: ")})
        e = s["evaluation"]
        print(f"  [S{e['situacion']} T{e['tarea']} A{e['accion']} R{e['resultado']}] -> {s['status']}")
    print("\nReporte:", build_report(FakeLLM(), turns=s["history"], previous_scores=[], resource_catalog=[]))


if __name__ == "__main__":
    main()
