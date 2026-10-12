"""
Uji Statistik - Chi-Square Test
==========================================
Tujuan: Membuktikan secara matematis, apakah selisih conversion rate
yang kita lihat itu BENERAN SIGNIFIKAN, atau cuma kebetulan random.

Aturan: p-value < 0.05 -> signifikan (bisa dipercaya)
        p-value >= 0.05 -> belum bisa dipastikan (mungkin cuma kebetulan)
"""

import pandas as pd
from scipy.stats import chi2_contingency # scipy - library python untuk perhitungan statistik

df = pd.read_csv("D:/kitchen_analysis/kitchenhub_orders.csv")

def uji_signifikansi(data, nama_platform):
    # Tabel kontingensi: baris = variant, kolom = converted (0/1)
    tabel = pd.crosstab(data["variant"], data["converted"])

    # Jalankan chi-square test
    chi2_stat, p_value, dof, expected = chi2_contingency(tabel)

    print(f"--- {nama_platform} ---")
    print("Tabel kontingensi:")
    print(tabel)
    print(f"Chi-square statistic: {chi2_stat:.4f}")
    print(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        print(">> SIGNIFIKAN (p < 0.05): Perbedaan ini kemungkinan besar NYATA, bukan kebetulan.")
    else:
        print(">> TIDAK SIGNIFIKAN (p >= 0.05): Belum cukup bukti untuk bilang ini beda nyata.")
    print()


# 1. Test untuk keseluruhan data (semua platform digabung)
uji_signifikansi(df, "KESELURUHAN (semua platform)")

# 2. Test untuk tiap platform secara terpisah
for platform in df["platform"].unique():
    data_platform = df[df["platform"] == platform]
    uji_signifikansi(data_platform, platform)