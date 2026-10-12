import pandas as pd
df = pd.read_csv("D:/kitchen_analysis/kitchenhub_orders.csv")

# Langkah 1 - Cara Manual
# pisahkan variant A dan B
data_a = df[df["variant"] == "A"]
data_b = df[df["variant"] == "B"]

# Hitung total order
total_a = len(data_a)
total_b = len(data_b)

completed_a = data_a["converted"].sum()
completed_b = data_b["converted"].sum()

conv_rate_a = (completed_a / total_a) * 100
conv_rate_b = (completed_b / total_b) * 100

print("=== Hasil Manual ===")
print(f"Variant A: {completed_a} completed dari {total_a} order -> Conversion Rate = {conv_rate_a:.2f}%")
print(f"Variant B: {completed_b} completed dari {total_b} order -> Conversion Rate = {conv_rate_b:.2f}%")

# --- langkah 2. pakai groupby ---
print("\n=== Hasil groupby() ===")

summary = df.groupby("variant")["converted"].agg(
    total_order="count",
    total_completed="sum",
    conversion_rate="mean" # rata-rata dari kolom 0/1 = otomatis jadi conversion rate (dalam desimal)
)

summary["conversion_rate"] = summary["conversion_rate"] * 100
print(summary)