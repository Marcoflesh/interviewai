from app.services.stats import passes_golden_gate, pearson, quadratic_weighted_kappa, spearman


def test_correlations():
    assert round(pearson([1, 2, 3, 4], [2, 4, 6, 8]), 6) == 1.0
    assert round(spearman([1, 2, 3, 4], [1, 4, 9, 16]), 6) == 1.0
    assert round(spearman([1, 2, 3, 4], [4, 3, 2, 1]), 6) == -1.0
    assert quadratic_weighted_kappa([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == 1.0


def test_gate():
    assert passes_golden_gate([1, 2, 3, 4, 5], [1, 2, 3, 5, 4])["approved"]       # rho = 0.9
    assert not passes_golden_gate([1, 2, 3, 4, 5], [3, 1, 2, 5, 4])["approved"]   # rho = 0.5


def test_models_create_all_on_sqlite():
    from sqlalchemy import create_engine, inspect
    from app.db.models import Base
    eng = create_engine("sqlite://")
    Base.metadata.create_all(eng)
    assert {"interview_sessions", "message_turns", "model_evaluations", "user_feedback",
            "golden_dataset", "users", "rubrics", "study_resources"} <= set(inspect(eng).get_table_names())
