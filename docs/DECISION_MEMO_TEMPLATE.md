# Experiment decision memo (template)

Fill this in **from real analysis output only**. Delete this line.

## 1. Hypothesis
We believe [change] will [increase/decrease] [metric] for [users] because [reason].

## 2. Design
- Unit of randomisation, split, start and end dates:
- Primary metric and why:
- Guardrail metrics (must not get worse):
- Minimum detectable effect, alpha, power, planned sample size per group:

## 3. Validity checks
- Sample-ratio check (chi-square p-value):
- Anything that changed during the test (outages, campaigns, bugs):
- Did you stop at the planned sample size? If not, why?

## 4. Results
| Group | Users | Conversions | Rate |
|---|---|---|---|
| Control | | | |
| Treatment | | | |

- Absolute lift with 95% confidence interval:
- Relative lift and p-value:
- Guardrail results:
- Segments checked (and how many, since each extra look raises the chance of a false positive):

## 5. Decision
Ship / do not ship / run longer, and the reasoning in two or three sentences, including what the interval says about the best and worst plausible outcomes.

## 6. Risks and next steps
- What could make this result misleading:
- Follow-up experiment or monitoring plan:
