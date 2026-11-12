"""abkit: small, dependency-light helpers for planning and analysing A/B tests."""
from .stats import (  # noqa: F401
    TestResult, bonferroni_alpha, sample_size_per_group, srm_check, two_proportion_test,
)

__version__ = "0.1.0"
