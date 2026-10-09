"""Compute the B100 composite financial-health score from the financials table.

Usage:
    python scripts/health_score.py                       # prints leaderboard
    python scripts/health_score.py --out data/sample/health_scores.csv

Scoring model (100 points):
    Profitability  25  percentile rank of mean(OPM%, net margin%, ROE%)
    Revenue growth 20  3-year sales CAGR (0 if <=0; 0-5 pts below 5%; capped at 20)
    Leverage       20  20 if D/E <= 0.1, 0 if D/E >= 2, linear in between
    Cash flow      15  5-year mean of operating cash flow / net profit (1.2x = full marks)
    Dividend       10  5-year mean payout (30% = full marks)
    Trend          10  mean normalised slope of sales and profit over 5 years (10%/yr = full marks)
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_IN = Path(__file__).resolve().parents[1] / "data" / "sample" / "financials.csv"
MAX_POINTS = {"profitability": 25, "growth": 20, "leverage": 20, "cash_flow": 15, "dividend": 10, "trend": 10}
BANDS = [(85, "EXCELLENT"), (70, "GOOD"), (50, "AVERAGE"), (35, "WEAK"), (0, "POOR")]


def label(score: float) -> str:
    return next(name for floor, name in BANDS if score >= floor)


def _slope(values: np.ndarray) -> float:
    x = np.arange(len(values))
    return float(np.polyfit(x, values, 1)[0])


def _cagr(series: pd.Series, years: int) -> float:
    return float((series.iloc[-1] / series.iloc[-1 - years]) ** (1 / years) - 1)


def company_features(df: pd.DataFrame) -> dict:
    d = df.sort_values("fiscal_year")
    last5 = d.tail(5)
    growth = _cagr(d["sales"], 3) * 100
    ocf_conv = float((last5["operating_cf"] / last5["net_profit"]).mean())
    trend = (
        _slope(last5["sales"].to_numpy()) / last5["sales"].mean()
        + _slope(last5["net_profit"].to_numpy()) / last5["net_profit"].mean()
    ) / 2 * 100
    latest = d.iloc[-1]
    return {
        "profit_raw": (latest["opm_pct"] + latest["npm_pct"] + latest["roe_pct"]) / 3,
        "growth_pct": growth,
        "de": float(latest["debt_to_equity"]),
        "ocf_conv": ocf_conv,
        "payout": float(last5["dividend_payout_pct"].mean()),
        "trend_pct": trend,
    }


def score_table(fin: pd.DataFrame) -> pd.DataFrame:
    feats = pd.DataFrame({sym: company_features(g) for sym, g in fin.groupby("symbol")}).T
    n = len(feats)
    # percentile rank, 0..1 (ties get the lowest rank, matching the dashboard)
    ranks = feats["profit_raw"].rank(method="min") - 1
    out = pd.DataFrame(index=feats.index)
    out["profitability"] = ranks / (n - 1) * 25
    g = feats["growth_pct"]
    out["growth"] = np.where(g <= 0, 0.0, np.where(g < 5, g, np.minimum(20, 5 + (g - 5))))
    de = feats["de"]
    out["leverage"] = np.where(de <= 0.1, 20.0, np.where(de >= 2, 0.0, 20 * (2 - de) / 1.9))
    out["cash_flow"] = np.minimum(15, feats["ocf_conv"] / 1.2 * 15)
    out["dividend"] = np.minimum(10, feats["payout"] / 30 * 10)
    t = feats["trend_pct"]
    out["trend"] = np.where(t <= 0, 0.0, np.minimum(10, t))
    out["score"] = out[list(MAX_POINTS)].sum(axis=1)
    out["label"] = out["score"].map(label)
    return out.sort_values("score", ascending=False).round(2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=DEFAULT_IN)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    table = score_table(pd.read_csv(args.input))
    print(table.to_string())
    if args.out:
        table.to_csv(args.out, index_label="symbol")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
