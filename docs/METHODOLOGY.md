# Methodology

**Sample size.** Two-sided two-proportion formula: n = (z_(1-alpha/2) * sqrt(2 * p_bar * (1 - p_bar)) + z_power * sqrt(p1(1-p1) + p2(1-p2)))^2 / (p2 - p1)^2, where p_bar is the average of the two rates. The result is rounded up and applies to each group.

**Hypothesis test.** Pooled-variance z-test for the difference in proportions. The confidence interval for the lift uses the unpooled standard error.

**Sample-ratio mismatch.** A chi-square test (1 degree of freedom) of observed group sizes against the designed split. The p-value is computed from the normal distribution because chi-square with 1 df equals z squared. A p-value below 0.001 is treated as a validity failure.

**Multiple comparisons.** The Bonferroni correction divides alpha by the number of comparisons. It is simple and conservative.

**Peeking.** The simulation runs A/A tests with no true difference, checks significance at evenly spaced looks, and stops at the first significant one. The share of tests that stop measures the inflated false-positive rate.

**Known limits.** Normal approximation (not for very small counts), binary metrics only, fixed-horizon design only.
