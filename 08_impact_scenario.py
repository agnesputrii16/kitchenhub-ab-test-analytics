"""
Bandingkan 3 skenario keputusan
=================================
Q: " varinat mana yang sebaiknya kita rollout, dan
berapa dampaknya ke pendapatan?"

Tiga skenario:
1. Tetap pakai Variant A di semua platform (kondisi sekarang)
2. Pindah ke Variant B di semua platform (keputusan "cepat")
3. Segmentasi: pakai variant TERBAIK di tiap platform

ASUMSI:
- Volume sesi per bulan = total sesi di data dibagi lama periode data
- Revenue per session tiap variant di tiap platform tetap sama seperti
  yang terukur di data (proyeksi sederhana, bukan prediksi pasti)
"""

import pandas as pd

df = pd.read_csv("kitchenhub_orders.csv")
df["date"] = pd.to_datetime(df["date"])

# ------------------------------------------------------------------
# 1. Lama periode data (dalam bulan)
# ------------------------------------------------------------------
bulan = (df["date"].max() - df["date"].min()).days / 30
print(f"Periode data: {df['date'].min().date()} s/d {df['date'].max().date()} (~{bulan:.1f} bulan)\n")

# ------------------------------------------------------------------
# 2. Revenue per session per platform x variant
# ------------------------------------------------------------------
g = df.groupby(["platform", "variant"]).agg(
    revenue=("order_value", "sum"),
    sessions=("order_session_id", "count"),
)
g["rps"] = g["revenue"] / g["sessions"]
rps = g["rps"].unstack()          # kolom: A dan B

# Volume sesi per bulan per platform (A + B digabung, dibagi lama periode)
sesi_per_bulan = df.groupby("platform")["order_session_id"].count() / bulan

# ------------------------------------------------------------------
# 3. Estimasi revenue per bulan untuk tiap skenario, per platform
# ------------------------------------------------------------------
tabel = pd.DataFrame({
    "sesi_per_bulan": sesi_per_bulan,
    "rps_A": rps["A"],
    "rps_B": rps["B"],
})
tabel["revenue_semua_A"] = tabel["sesi_per_bulan"] * tabel["rps_A"]
tabel["revenue_semua_B"] = tabel["sesi_per_bulan"] * tabel["rps_B"]
tabel["varian_terbaik"] = (tabel["rps_B"] > tabel["rps_A"]).map({True: "B", False: "A"})
tabel["revenue_segmentasi"] = tabel[["revenue_semua_A", "revenue_semua_B"]].max(axis=1)

print("=== Estimasi revenue per bulan, per platform ===")
print(tabel.to_string(float_format=lambda x: f"{x:,.0f}"))

# ------------------------------------------------------------------
# 4. Ringkasan 3 skenario (total semua platform)
# ------------------------------------------------------------------
total = {
    "1. Tetap A di semua platform": tabel["revenue_semua_A"].sum(),
    "2. Pindah ke B di semua platform": tabel["revenue_semua_B"].sum(),
    "3. Segmentasi (terbaik per platform)": tabel["revenue_segmentasi"].sum(),
}
baseline = total["1. Tetap A di semua platform"]

print("\n=== Perbandingan 3 skenario (estimasi revenue per bulan) ===")
for nama, nilai in total.items():
    selisih = nilai - baseline
    persen = selisih / baseline * 100
    print(f"{nama:<40} Rp {nilai:>14,.0f}   ({selisih:>+14,.0f} | {persen:>+6.1f}% vs skenario 1)")

# Seberapa besar keuntungan segmentasi dibanding "rollout B ke semua"?
tambahan = total["3. Segmentasi (terbaik per platform)"] - total["2. Pindah ke B di semua platform"]
print(f"\nSegmentasi menambah Rp {tambahan:,.0f} per bulan dibanding rollout B ke semua platform.")