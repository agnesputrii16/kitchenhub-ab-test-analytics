import pandas as pd

#load data 
df = pd.read_csv("kitchenhub_orders.csv")

# 1. cek ukuran data - berapa baris? berapa kolom?
print("=== Ukuran Data ===")
print(f"Jumlah baris: {df.shape[0]}")
print(f"Jumlah kolom: {df.shape[1]}")

# 2. lihat 5 baris pertama
print("\n=== 5 baris pertama ===")
print(df.head())

# 3. cek tipe data
print("\n=== Info Kolom & tipe data ===")
print(df.info())

# 4. cek missing values - apakah ada data kosong?
print("\n=== Cek data kosong ===")
print(df.isnull().sum())

# 5. lihat nilai unik
print("\n=== nilai unik di kolom kategori ===")
print("Variant:", df["variant"].unique())
print("Platform:", df["platform"].unique())
print("Brand:", df["brand"].unique())
print("Funnel step:", df["funnel_step_reached"].unique())