import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from health_score import MAX_POINTS, label, score_table  # noqa: E402

FIN = pd.read_csv(ROOT / "data" / "sample" / "financials.csv")


def test_scores_within_bounds():
    t = score_table(FIN)
    assert t["score"].between(0, 100).all()
    for col, cap in MAX_POINTS.items():
        assert (t[col] <= cap + 1e-9).all() and (t[col] >= 0).all()


def test_every_company_scored_once():
    assert set(score_table(FIN).index) == set(FIN["symbol"])


def test_labels_match_bands():
    assert label(90) == "EXCELLENT" and label(70) == "GOOD" and label(50) == "AVERAGE"
    assert label(35) == "WEAK" and label(10) == "POOR"


def test_debt_free_company_gets_full_leverage_points():
    t = score_table(FIN)
    assert t.loc["TCS", "leverage"] == 20


def test_highly_levered_company_gets_zero_leverage_points():
    t = score_table(FIN)
    assert t.loc["ADANIPOWER", "leverage"] == 0
