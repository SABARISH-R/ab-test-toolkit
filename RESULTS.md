# Results

Produced on 2026-11-16 with Python 3.12.3 (seed 42). Re-run to reproduce.

## Unit tests
`PYTHONPATH=src python -m unittest discover -s tests`

```
----------------------------------------------------------------------
Ran 9 tests in 0.183s

OK
```

## Simulations
`PYTHONPATH=src python -m abkit.simulate`

```
Empirical power at the planned sample size (target 0.80):
  n per group = 3841, power = 0.795
False-positive rate of an A/A test when you stop at the first significant look:
   1 looks -> 0.050
   2 looks -> 0.082
   5 looks -> 0.140
  10 looks -> 0.191
  20 looks -> 0.251
```

Interpretation: at the planned sample size, simulated experiments with a true lift reached significance about as often as the 80% power target. In A/A tests with no real difference, stopping at the first significant look raised the false-positive rate well above the nominal 5%, and the rate grew with the number of looks.

## Real experiment: Cookie Cats
90,189 players, first gate at level 30 (control) vs level 40. Data source and download: `data/real/README.md`. Full write-up: [`reports/cookie_cats/DECISION_MEMO.md`](reports/cookie_cats/DECISION_MEMO.md). Raw output: `reports/cookie_cats/cli_output.txt`.

| Metric | Gate 30 | Gate 40 | Difference (95% CI) | p |
|---|---|---|---|---|
| Day-1 retention | 44.82% | 44.23% | −0.59 pts (−1.24 to +0.06) | 0.074 |
| Day-7 retention | 19.02% | 18.20% | −0.82 pts (−1.33 to −0.31) | 0.0016 |

Sample-ratio check: 44,700 vs 45,489, p = 0.0086 (flagged, below the 0.001 block threshold). Decision: do not ship.

![Bootstrap](reports/cookie_cats/bootstrap_retention_diff.png)

## Not done yet
- Continuous-metric tests and variance reduction

## Figures
Regenerate with `PYTHONPATH=src python scripts/make_figures.py` (needs matplotlib).

![Peeking inflates false positives](docs/images/peeking_false_positive_rate.png)

![Sample size versus effect size](docs/images/sample_size_vs_effect.png)
