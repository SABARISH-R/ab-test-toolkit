"""Regenerate the figures in docs/images. Run from the repo root:
   PYTHONPATH=src python scripts/make_figures.py   (needs matplotlib)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from abkit.simulate import peeking_false_positive_rate  # noqa: E402
from abkit.stats import sample_size_per_group  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)
NAVY, RED = "#1F3A5F", "#C0392B"

# 1. Peeking inflates false positives (A/A tests, seed 42, 5000 simulations per point)
looks = [1, 2, 3, 5, 10, 20]
rates = [peeking_false_positive_rate(2000, k, sims=5000, seed=42) * 100 for k in looks]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(looks, rates, marker="o", color=RED, linewidth=2, label="Stop at first significant look")
ax.axhline(5, color=NAVY, linestyle="--", label="Intended 5% false-positive rate")
for x, y in zip(looks, rates):
    ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
ax.set_xlabel("Number of times you check the results")
ax.set_ylabel("False-positive rate (%)")
ax.set_title("Peeking at an A/A test inflates false positives")
ax.set_ylim(0, 30)
ax.set_xticks(looks)
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "peeking_false_positive_rate.png", dpi=160)
plt.close(fig)

# 2. Sample size needed vs smallest lift worth detecting (baseline 10%, alpha 0.05, power 0.80)
mdes = [m / 1000 for m in range(5, 51, 1)]
sizes = [sample_size_per_group(0.10, m) for m in mdes]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot([m * 100 for m in mdes], sizes, color=NAVY, linewidth=2)
ax.set_xlabel("Smallest absolute lift to detect (percentage points)")
ax.set_ylabel("Users needed per group")
ax.set_title("Smaller effects need far more users (baseline 10%)")
ax.set_yscale("log")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "sample_size_vs_effect.png", dpi=160)
plt.close(fig)
print("Figures written to", OUT)
