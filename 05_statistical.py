"""
STEP 5: Statistical test (Chi-Square)
=======================================
Is the difference between Variant A and B real, or just random noise?

Rule of thumb: p-value < 0.05 -> statistically significant.
Because we run one test per platform (3 tests), we also show the
Bonferroni-adjusted threshold: 0.05 / number of tests.
"""

import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv("kitchenhub_orders.csv")


def significance_test(data, name):
    table = pd.crosstab(data["variant"], data["converted"])
    chi2_stat, p_value, dof, expected = chi2_contingency(table)

    print(f"--- {name} ---")
    print("Contingency table:")
    print(table)
    print(f"Chi-square statistic: {chi2_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    if p_value < 0.05:
        print(">> SIGNIFICANT (p < 0.05)\n")
    else:
        print(">> NOT significant (p >= 0.05)\n")
    return p_value


significance_test(df, "OVERALL (all platforms)")

platform_p = {}
for platform in df["platform"].unique():
    platform_p[platform] = significance_test(df[df["platform"] == platform], platform)

alpha_bonferroni = 0.05 / len(platform_p)
print(f"=== Bonferroni check (3 platform tests, adjusted alpha = {alpha_bonferroni:.4f}) ===")
for platform, p in platform_p.items():
    status = "still significant" if p < alpha_bonferroni else "NOT significant"
    print(f"{platform:<12} p = {p:.6f} -> {status}")