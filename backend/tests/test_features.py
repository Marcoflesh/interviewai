import pytest
from app.services.features import extract_features


@pytest.mark.parametrize("text,expected", [
    ("Reduje el tiempo en 35%", True),
    ("Ahorre $1,500 al mes", True),
    ("Atendi a 120 usuarios", True),
    ("Fue en 2024 y me fue bien", False),      # anios no cuentan como metrica
    ("Trabaje mucho y aprendi bastante", False),
    ("", False),
])
def test_metric_detection(text, expected):
    assert extract_features(text).has_metrics is expected


def test_lengths():
    f = extract_features("uno dos tres")
    assert (f.length_words, f.length_chars) == (3, 12)
