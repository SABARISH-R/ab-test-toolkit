"""Analyse a CSV of experiment results.

  PYTHONPATH=src python -m abkit.cli data/experiment.csv \
      --group-col variant --metric-col converted --control A --treatment B
The metric column must be 0/1 (did the user convert?).
"""
from __future__ import annotations

import argparse

import pandas as pd

from .stats import srm_check, two_proportion_test


def main() -> None:
    p = argparse.ArgumentParser(description="Analyse an A/B test with a binary metric.")
    p.add_argument("input")
    p.add_argument("--group-col", default="group")
    p.add_argument("--metric-col", default="converted")
    p.add_argument("--control", default="control")
    p.add_argument("--treatment", default="treatment")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--expected-control-share", type=float, default=0.5)
    a = p.parse_args()

    df = pd.read_csv(a.input)
    for col in (a.group_col, a.metric_col):
        if col not in df.columns:
            raise SystemExit(f"Column '{col}' not found. Available: {list(df.columns)}")
    if not set(df[a.metric_col].dropna().unique()) <= {0, 1}:
        raise SystemExit("Metric column must contain only 0/1 values.")

    c = df[df[a.group_col] == a.control][a.metric_col]
    t = df[df[a.group_col] == a.treatment][a.metric_col]
    if c.empty or t.empty:
        raise SystemExit(f"No rows found for control '{a.control}' or treatment '{a.treatment}'.")

    chi2, srm_p = srm_check(len(c), len(t), a.expected_control_share)
    print(f"Control: {len(c)} users | Treatment: {len(t)} users")
    print(f"Sample-ratio check: chi2={chi2:.2f}, p={srm_p:.4f}")
    if srm_p < 0.001:
        print("WARNING: sample-ratio mismatch. Do not trust this result until assignment is investigated.")
        return

    r = two_proportion_test(int(c.sum()), len(c), int(t.sum()), len(t), a.alpha)
    print(f"Control rate: {r.p_control:.2%} | Treatment rate: {r.p_treatment:.2%}")
    print(f"Absolute lift: {r.abs_lift:+.2%} ({(1 - a.alpha):.0%} CI {r.ci_low:+.2%} to {r.ci_high:+.2%})")
    print(f"Relative lift: {r.rel_lift:+.1%} | z={r.z:.2f} | p={r.p_value:.4f}")
    if r.ci_low > 0:
        print("Reading: statistically significant improvement. Check guardrail metrics before shipping.")
    elif r.ci_high < 0:
        print("Reading: statistically significant decline. Do not ship.")
    else:
        print("Reading: inconclusive. The interval includes zero; do not claim a win.")


if __name__ == "__main__":
    main()
