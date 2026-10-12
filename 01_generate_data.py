import pandas as pd
import numpy as np
from faker import Faker
import random

np.random.seed(42)
random.seed(42)
fake = Faker()
fake.seed_instance(42)

N_ORDERS = 8000

brands = ["Ayam Geprek Juara","Bento Sehat","Mie Kece","Kopi Santuy"]
platforms = ["GoFood","GrabFood","ShopeeFood"]
order_funnel = ["browse","add_to_cart","order_start","payment","completed"]

rows = []

for i in range(N_ORDERS):
    order_session_id = f"ORD{i+1:05d}"
    user_id = f"USR{random.randint(1, 6000):05d}"
    variant = random.choice(["A", "B"])
    brand = random.choice(brands)
    platform = random.choices(platforms, weights=[0.45, 0.40, 0.15])[0]
    date = fake.date_between(start_date="-90d", end_date="today")

    if platform == "ShopeeFood":
        p_complete = 0.30 if variant == "A" else 0.21
    else:
        p_complete = 0.24 if variant == "A" else 0.33

    rand_val = np.random.rand()
    if rand_val < p_complete:
        step_reached = "completed"
    elif rand_val < p_complete + 0.15:
        step_reached = "payment"    
    elif rand_val < p_complete + 0.35:
        step_reached = "order_start"   
    elif rand_val < p_complete + 0.65:
        step_reached = "add_to_cart"    
    else:
        step_reached = "browse" 

    converted = 1 if step_reached == "completed" else 0
    order_value = round(np.random.uniform(35000, 180000), 0) if converted else 0   

    rows.append({
        "order_session_id": order_session_id,
        "user_id": user_id,
        "date": date,
        "variant": variant,
        "brand": brand,
        "platform": platform,
        "funnel_step_reached": step_reached,
        "converted": converted,
        "order_value": order_value
    })     

    df = pd.DataFrame(rows)
    df.to_csv("D:/kitchen_analysis/kitchenhub_orders.csv", index=False)

    print("Data berhasil dibuat!")       
    print(f"Total baris: {len(df)}")
    print("\nContoh 5 baris pertama:")
    print(df.head())
    print("\nRingkasan cepat per variant (overall):")
    print(df.groupby("variant")["converted"].agg(["count", "sum", "mean"]))
    print("\nRingkasan per variant x platform:")
    print(df.groupby(["platform", "variant"])["converted"].mean())