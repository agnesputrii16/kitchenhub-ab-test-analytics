"""
Hitung Metrik Revenue per Variant & Platform
========================================================
Tujuan: Sebelum estimasi dampak bisnis, kita perlu tahu dulu
berapa uang yang masuk dari tiap variant.

Tiga metrik utama:
1. Total revenue        = jumlah seluruh order_value
2. AOV                  = rata-rata nilai SATU pesanan yang berhasil
                          (revenue / jumlah order completed)
3. Revenue per session  = revenue / SEMUA sesi (termasuk yang tidak beli)
                          -> metrik paling adil buat bandingin variant,
                             karena gabungan conversion rate + nilai pesanan
"""

import pandas as pd

pd.options.display.float_format = "{:,.0f}".format

df = pd.read_csv("kitchenhub_orders.csv")

# ------------------------------------------------------------------
# 1. Metrik per VARIANT (semua platform digabung)
# ------------------------------------------------------------------
per_variant = df.groupby("variant").agg(
    sessions=("order_session_id", "count"),
    completed=("converted", "sum"),
    revenue=("order_value", "sum"),
)
per_variant["AOV"] = per_variant["revenue"] / per_variant["completed"]
per_variant["revenue_per_session"] = per_variant["revenue"] / per_variant["sessions"]

print("=== Metrik Revenue per Variant (keseluruhan) ===")
print(per_variant)

# ------------------------------------------------------------------
# 2. Metrik per PLATFORM x VARIANT
# ------------------------------------------------------------------
per_platform = df.groupby(["platform", "variant"]).agg(
    sessions=("order_session_id", "count"),
    completed=("converted", "sum"),
    revenue=("order_value", "sum"),
)
per_platform["AOV"] = per_platform["revenue"] / per_platform["completed"]
per_platform["revenue_per_session"] = per_platform["revenue"] / per_platform["sessions"]

print("\n=== Metrik Revenue per Platform x Variant ===")
print(per_platform)

# ------------------------------------------------------------------
# 3. Perubahan revenue per session: Variant B dibanding Variant A
# ------------------------------------------------------------------
rps = per_platform["revenue_per_session"].unstack()   # kolom A dan B
rps["selisih (Rp)"] = rps["B"] - rps["A"]
rps["perubahan (%)"] = (rps["B"] - rps["A"]) / rps["A"] * 100

print("\n=== Revenue per Session: B dibanding A ===")
print(rps.to_string(float_format=lambda x: f"{x:,.1f}"))