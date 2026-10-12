"""
Funnel Analysis pakai SQL
===================================
Tujuan: Cari tahu di tahap mana user paling banyak "bocor" (drop-off)
sepanjang funnel: browse -> add_to_cart -> order_start -> payment -> completed

Cara kerja:
1. Load CSV ke pandas
2. Masukkan ke database SQLite (in-memory, jadi nggak perlu install apa-apa)
3. Query pakai SQL
4. Hitung persentase lanjut/drop-off antar tahap pakai pandas
"""

import sqlite3
import pandas as pd

df = pd.read_csv("kitchenhub_orders.csv")

# Bikin database SQLite sementara di memori, lalu isi tabel "orders"
conn = sqlite3.connect(":memory:")
df.to_sql("orders", conn, index=False)

# ------------------------------------------------------------------
# QUERY 1: Jumlah order yang SAMPAI di tiap tahap funnel, per variant
# ------------------------------------------------------------------
# funnel_step_reached = tahap TERJAUH yang dicapai user.
# Jadi untuk tahu berapa yang "sampai di tahap X", kita hitung semua
# yang tahap terjauhnya >= X. Makanya tiap tahap diberi nomor urut dulu.

query_per_variant = """
WITH ranked AS (
    SELECT
        variant,
        CASE funnel_step_reached
            WHEN 'browse'      THEN 1
            WHEN 'add_to_cart' THEN 2
            WHEN 'order_start' THEN 3
            WHEN 'payment'     THEN 4
            WHEN 'completed'   THEN 5
        END AS step_rank
    FROM orders
)
SELECT
    variant,
    COUNT(*)                                          AS browse,
    SUM(CASE WHEN step_rank >= 2 THEN 1 ELSE 0 END)   AS add_to_cart,
    SUM(CASE WHEN step_rank >= 3 THEN 1 ELSE 0 END)   AS order_start,
    SUM(CASE WHEN step_rank >= 4 THEN 1 ELSE 0 END)   AS payment,
    SUM(CASE WHEN step_rank >= 5 THEN 1 ELSE 0 END)   AS completed
FROM ranked
GROUP BY variant
ORDER BY variant;
"""

funnel = pd.read_sql_query(query_per_variant, conn)
print("=== Jumlah order yang sampai di tiap tahap (per variant) ===")
print(funnel.to_string(index=False))

# ------------------------------------------------------------------
# Hitung "% yang lanjut" dari tahap sebelumnya ke tahap berikutnya
# ------------------------------------------------------------------
steps = ["browse", "add_to_cart", "order_start", "payment", "completed"]

print("\n=== % user yang LANJUT dari satu tahap ke tahap berikutnya ===")
rows = []
for _, r in funnel.iterrows():
    row = {"variant": r["variant"]}
    for i in range(len(steps) - 1):
        dari, ke = steps[i], steps[i + 1]
        row[f"{dari} -> {ke}"] = round(r[ke] / r[dari] * 100, 1)
    rows.append(row)
print(pd.DataFrame(rows).to_string(index=False))

# ------------------------------------------------------------------
# QUERY 2: Funnel yang sama, tapi dipecah per platform x variant
# ------------------------------------------------------------------
query_per_platform = query_per_variant.replace(
    "variant,\n        CASE", "platform, variant,\n        CASE"
).replace(
    "SELECT\n    variant,", "SELECT\n    platform, variant,"
).replace(
    "GROUP BY variant\nORDER BY variant;", "GROUP BY platform, variant\nORDER BY platform, variant;"
)

funnel_platform = pd.read_sql_query(query_per_platform, conn)
print("\n\n=== Jumlah order di tiap tahap (per platform x variant) ===")
print(funnel_platform.to_string(index=False))

print("\n=== % LANJUT antar tahap (per platform x variant) ===")
rows = []
for _, r in funnel_platform.iterrows():
    row = {"platform": r["platform"], "variant": r["variant"]}
    for i in range(len(steps) - 1):
        dari, ke = steps[i], steps[i + 1]
        row[f"{dari} -> {ke}"] = round(r[ke] / r[dari] * 100, 1)
    rows.append(row)
print(pd.DataFrame(rows).to_string(index=False))

conn.close()