"""Core statistics for conversion-rate experiments (standard library only)."""
from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist

_N = NormalDist()


def sample_size_per_group(p_base: float, mde_abs: float, alpha: float = 0.05,
                          power: float = 0.8, two_sided: bool = True) -> int:
    """Users needed in EACH group to detect an absolute lift of `mde_abs`.

    Uses the standard two-proportion formula (pooled variance under the null,
    unpooled under the alternative).
    """
    p2 = p_base + mde_abs
    if not (0 < p_base < 1 and 0 < p2 < 1):
        raise ValueError("baseline and baseline + MDE must both be strictly between 0 and 1")
    if mde_abs == 0:
        raise ValueError("mde_abs must be non-zero")
    z_alpha = _N.inv_cdf(1 - alpha / (2 if two_sided else 1))
    z_beta = _N.inv_cdf(power)
    p_bar = (p_base + p2) / 2
    numerator = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar))
                 + z_beta * math.sqrt(p_base * (1 - p_base) + p2 * (1 - p2))) ** 2
    return math.ceil(numerator / mde_abs ** 2)


@dataclass(frozen=True)
class TestResult:
    p_control: float
    p_treatment: float
    abs_lift: float
    rel_lift: float
    ci_low: float        # confidence interval for the absolute lift
    ci_high: float
    z: float
    p_value: float
    significant: bool
    alpha: float


def two_proportion_test(x_control: int, n_control: int, x_treatment: int, n_treatment: int,
                        alpha: float = 0.05) -> TestResult:
    """Two-sided z-test for a difference in proportions with a Wald confidence interval."""
    if min(n_control, n_treatment) <= 0:
        raise ValueError("group sizes must be positive")
    p_c, p_t = x_control / n_control, x_treatment / n_treatment
    pooled = (x_control + x_treatment) / (n_control + n_treatment)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / n_control + 1 / n_treatment))
    z = (p_t - p_c) / se_pooled if se_pooled > 0 else 0.0
    p_value = 2 * (1 - _N.cdf(abs(z)))
    se_unpooled = math.sqrt(p_c * (1 - p_c) / n_control + p_t * (1 - p_t) / n_treatment)
    margin = _N.inv_cdf(1 - alpha / 2) * se_unpooled
    diff = p_t - p_c
    return TestResult(
        p_control=p_c, p_treatment=p_t, abs_lift=diff,
        rel_lift=(diff / p_c) if p_c > 0 else float("nan"),
        ci_low=diff - margin, ci_high=diff + margin,
        z=z, p_value=p_value, significant=p_value < alpha, alpha=alpha,
    )


def srm_check(n_control: int, n_treatment: int, expected_control_share: float = 0.5) -> tuple[float, float]:
    """Sample-ratio-mismatch check (chi-square, 1 df). Returns (chi2, p_value).

    A very small p-value (commonly < 0.001) means assignment is not behaving as designed,
    so the experiment result should not be trusted until the cause is found.
    """
    total = n_control + n_treatment
    exp_c = total * expected_control_share
    exp_t = total - exp_c
    chi2 = (n_control - exp_c) ** 2 / exp_c + (n_treatment - exp_t) ** 2 / exp_t
    p_value = 2 * (1 - _N.cdf(math.sqrt(chi2)))  # chi-square with 1 df equals z squared
    return chi2, p_value


def bonferroni_alpha(alpha: float, n_comparisons: int) -> float:
    """Per-comparison significance level that keeps the family-wise error rate at `alpha`."""
    if n_comparisons < 1:
        raise ValueError("n_comparisons must be at least 1")
    return alpha / n_comparisons
