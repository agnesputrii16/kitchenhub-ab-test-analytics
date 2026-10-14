import pandas as pd

df = pd.read_csv("kitchenhub_orders.csv")

print("=== conversion per platform x variant ===\n")

breakdown = df.groupby(["platform", "variant"])["converted"].agg(
    total_order="count",
    total_completed="sum",
    conversion_rate="mean"
)
breakdown["conversion_rate"] = breakdown["conversion_rate"] * 100

print(breakdown)

print("\n\n=== Selisih Conversion Rate (Variant B - Variant A) per Platform ===\n")
pivot = df.groupby(["platform", "variant"])["converted"].mean().unstack() * 100
pivot["selisih (B - A)"] = pivot["B"] - pivot["A"]
pivot["rekomendasi"] = pivot["selisih (B - A)"].apply(
    lambda x: "Rollout Variant B" if x > 0 else "Pertahankan Variant A"
)
print(pivot.round(2))