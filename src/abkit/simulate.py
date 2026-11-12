"""Monte Carlo helpers that show WHY the statistics behave as they do."""
from __future__ import annotations

import numpy as np
from statistics import NormalDist

_N = NormalDist()


def _z_stats(x_c, n_c, x_t, n_t):
    p_c, p_t = x_c / n_c, x_t / n_t
    pooled = (x_c + x_t) / (n_c + n_t)
    se = np.sqrt(np.clip(pooled * (1 - pooled), 1e-12, None) * (1 / n_c + 1 / n_t))
    return (p_t - p_c) / se


def empirical_power(n_per_group: int, p_base: float, mde_abs: float,
                    alpha: float = 0.05, sims: int = 5000, seed: int = 42) -> float:
    """Share of simulated experiments (with a real lift) that reach significance."""
    rng = np.random.default_rng(seed)
    x_c = rng.binomial(n_per_group, p_base, sims)
    x_t = rng.binomial(n_per_group, p_base + mde_abs, sims)
    z = _z_stats(x_c, n_per_group, x_t, n_per_group)
    crit = _N.inv_cdf(1 - alpha / 2)
    return float((np.abs(z) > crit).mean())


def peeking_false_positive_rate(n_per_group: int, looks: int, p: float = 0.10,
                                alpha: float = 0.05, sims: int = 5000, seed: int = 42) -> float:
    """A/A test (no real difference) where you stop at the first significant look.

    With looks=1 this should be close to alpha. More looks inflate the false-positive rate.
    """
    rng = np.random.default_rng(seed)
    a = rng.random((sims, n_per_group)) < p
    b = rng.random((sims, n_per_group)) < p
    ca, cb = a.cumsum(axis=1), b.cumsum(axis=1)
    idx = np.unique(np.linspace(n_per_group / looks, n_per_group, looks).astype(int)) - 1
    crit = _N.inv_cdf(1 - alpha / 2)
    fired = np.zeros(sims, dtype=bool)
    for i in idx:
        n = i + 1
        z = _z_stats(ca[:, i], n, cb[:, i], n)
        fired |= np.abs(z) > crit
    return float(fired.mean())


def main() -> None:
    print("Empirical power at the planned sample size (target 0.80):")
    from .stats import sample_size_per_group
    n = sample_size_per_group(0.10, 0.02)
    print(f"  n per group = {n}, power = {empirical_power(n, 0.10, 0.02):.3f}")
    print("False-positive rate of an A/A test when you stop at the first significant look:")
    for looks in (1, 2, 5, 10, 20):
        rate = peeking_false_positive_rate(2000, looks)
        print(f"  {looks:>2} looks -> {rate:.3f}")


if __name__ == "__main__":
    main()
