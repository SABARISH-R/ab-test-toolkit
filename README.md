# A/B Test Toolkit: plan, validate, analyse, decide

Small, readable helpers and a worked notebook for running conversion-rate experiments the way a product team should: decide the sample size first, check the experiment is valid, report an effect with a confidence interval, and write a decision you can defend.

The statistics core uses only the Python standard library. Simulations use NumPy.

## What is in it

| Piece | What it does |
|---|---|
| `abkit.sample_size_per_group` | Users needed per group for a chosen baseline, minimum detectable effect, alpha and power |
| `abkit.two_proportion_test` | Z-test, confidence interval for the lift, relative lift |
| `abkit.srm_check` | Sample-ratio-mismatch test to catch broken assignment |
| `abkit.bonferroni_alpha` | Adjust alpha when comparing several variants or metrics |
| `abkit.simulate` | Monte Carlo checks: does the planned sample size really give 80% power, and how much does peeking inflate false positives? |
| `python -m abkit.cli` | Analyse your own experiment CSV from the command line |
| `notebooks/ab_test_walkthrough.ipynb` | End-to-end walkthrough on **simulated** data |
| `docs/DECISION_MEMO_TEMPLATE.md` | One-page structure for the ship / do-not-ship decision |

## Quick start

```bash
git clone https://github.com/SABARISH-R/ab-test-toolkit.git
cd ab-test-toolkit
pip install -r requirements.txt

PYTHONPATH=src python -m unittest discover -s tests -v     # run the tests
PYTHONPATH=src python -m abkit.simulate                    # reproduce the simulation results below

# analyse a real experiment file (metric column must be 0/1)
PYTHONPATH=src python -m abkit.cli data/experiment.csv \
    --group-col variant --metric-col converted --control A --treatment B
```

## What the simulations show

Reproduced by `python -m abkit.simulate` (seed 42):

- Planning for a 10% to 12% lift at alpha 0.05 and 80% power needs 3,841 users per group, and 5,000 simulated experiments at that size reached significance 79.5% of the time, matching the 80% target.
- In A/A tests with no real difference, the false-positive rate of "stop at the first significant result" was 5.0% with one look, 8.2% with two, 14.0% with five, 19.1% with ten and 25.1% with twenty. Peeking at results and stopping early is the most common way teams ship changes that do nothing.

## Method notes and limitations

- The test assumes a binary metric (converted or not), independent users and a fixed sample size decided in advance.
- It does not cover continuous metrics such as revenue per user, sequential or Bayesian designs, or variance reduction (CUPED). These are natural extensions.
- The notebook's data is simulated so the true effect is known. It is a teaching example, not evidence about any real product.

## Roadmap

- [x] Sample size, z-test with CI, SRM check, multiple-comparison helper, simulations, tests
- [ ] Analyse a real public experiment dataset and write the decision memo
- [ ] Add continuous-metric support (Welch t-test) and CUPED
- [ ] Add a sequential testing option so teams can monitor safely

## License

MIT
