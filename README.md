# KitchenHub: A/B Test & Funnel Analytics

**A simulated case study: should a multi-brand cloud kitchen roll out a new one-tap order flow?**

> **Ringkasan (Bahasa Indonesia):** Studi kasus simulasi untuk "KitchenHub", cloud kitchen fiktif dengan beberapa brand yang berjualan lewat GoFood, GrabFood, dan ShopeeFood. Dua versi alur pesan (A = multi-langkah, B = satu ketukan) diuji pada 8.000 sesi. Secara keseluruhan Variant B menang, tetapi di ShopeeFood justru Variant A yang lebih baik. Rekomendasinya: rollout B hanya di GoFood dan GrabFood, dan pertahankan A di ShopeeFood. Datanya hasil simulasi, jadi project ini menunjukkan **metode analisis**, bukan temuan dunia nyata.

**Tools:** Python (pandas, SciPy), SQL (SQLite)

---

## TL;DR

- **Overall:** Variant B converts better than A (24.9% → 31.5%, p < 0.001).
- **But not everywhere:** on ShopeeFood, B is *worse* (29.5% → 21.4%, still significant after Bonferroni correction).
- **Decision:** roll out B on GoFood and GrabFood only, keep A on ShopeeFood. This earns an estimated **Rp3.28 million more per month** than rolling out B everywhere.

> **This is simulated data.** The data was generated with Python to build a clear business story, including the ShopeeFood pattern. The results show **how an A/B test is analyzed**, not how real customers behave.

---

## 1. Business problem

KitchenHub sells food from several brands on three delivery platforms. The product team built a new order flow and wants to know:

- Does **Variant B** (one-tap order) get more customers to finish their order than **Variant A** (multi-step order)?
- Should B be rolled out to every platform?
- Where do customers drop out of the order funnel?
- How much revenue is at stake?

## 2. About the data

| Item | Detail |
|---|---|
| Size | 8,000 order sessions |
| Period | about 3 months |
| Platforms | GoFood (3,615 sessions), GrabFood (3,147), ShopeeFood (1,238) |
| Brands | 4 fictional brands |
| Variants | A (multi-step order), B (one-tap order), randomly assigned |
| Funnel | browse → add_to_cart → order_start → payment → completed |

Main columns: `order_session_id`, `user_id`, `date`, `variant`, `brand`, `platform`, `funnel_step_reached`, `converted` (1 = completed order), `order_value` (in Rupiah).

## 3. Key findings

### 3.1 The overall average hides the real story

| | Variant A | Variant B |
|---|---|---|
| Sessions | 3,994 | 4,006 |
| Completed orders | 995 | 1,260 |
| Conversion rate | 24.9% | 31.5% |

Overall, B looks better (chi-square = 41.94, p < 0.001). If the analysis stopped here, the conclusion would be "roll out B everywhere". The result is different when split by platform.

### 3.2 Variant B is worse on ShopeeFood

| Platform | A conversion | B conversion | Difference | p-value | p-value (Bonferroni) |
|---|---|---|---|---|---|
| GoFood | 24.8% | 32.8% | +7.9 pts | < 0.001 | < 0.001 |
| GrabFood | 23.1% | 33.7% | +10.6 pts | < 0.001 | < 0.001 |
| **ShopeeFood** | **29.5%** | **21.4%** | **-8.1 pts** | **0.0013** | **0.004** |

Three tests were run (one per platform), so each p-value was multiplied by 3 (Bonferroni). All three results are still significant, including ShopeeFood. The ShopeeFood sample is the smallest (640 and 598 sessions), so this result should be confirmed with more data.

### 3.3 Where customers drop out of the funnel

Share of users who continue from one step to the next (all platforms):

| Variant | browse → cart | cart → order start | order start → payment | payment → completed |
|---|---|---|---|---|
| A | 90.3% | 66.9% | 66.8% | 61.8% |
| B | 96.2% | 70.1% | 69.6% | 67.0% |

- In all six platform-variant combinations, the lowest continuation rate is **payment → completed**. These are users who already reached the payment step.
- In terms of the number of users lost, the biggest loss is **cart → order start**, because more users are still in the funnel at that point.
- On ShopeeFood, Variant B is worse at **every** step. The biggest fall is at the start of the funnel (browse → cart: 95.9% → 85.1%), while GoFood and GrabFood both improve to about 98%. This suggests a problem with the app screen or the one-tap flow on that platform. This is a hypothesis to check, not a conclusion.

### 3.4 Revenue impact

Average order value is almost the same (A: Rp107,067, B: Rp105,404). So Variant B earns more only because **more customers finish their order**, not because orders are bigger.

| Platform | Revenue per session, A | Revenue per session, B | Change |
|---|---|---|---|
| GoFood | Rp26,956 | Rp34,939 | +29.6% |
| GrabFood | Rp24,947 | Rp35,206 | +41.1% |
| ShopeeFood | Rp30,119 | Rp22,268 | -26.1% |

### 3.5 Three rollout scenarios (estimated revenue per month)

| Scenario | Revenue per month | vs. today |
|---|---|---|
| 1. Keep A everywhere | Rp71,878,749 | baseline |
| 2. Roll out B everywhere | Rp89,212,912 | +24.1% |
| **3. Segmented: B on GoFood and GrabFood, A on ShopeeFood** | **Rp92,489,023** | **+28.7%** |

The segmented plan earns **Rp3,276,111 more per month** than rolling out B everywhere. That is the money lost by deciding from the overall average alone.

## 4. Recommendation

1. **Roll out Variant B on GoFood and GrabFood.**
2. **Keep Variant A on ShopeeFood** for now.
3. **Find out why B fails on ShopeeFood.** Ask engineering to check for bugs or slow screens, then run the test again with a larger sample.
4. **Look at the payment step.** Many users who reach payment still do not complete the order.

## 5. Limitations

- **The data is simulated.** The platform pattern was designed into the data, so these findings demonstrate the method only.
- Step-level funnel patterns also come from how the data was generated. With real data, tracking errors should be checked before trusting them.
- Order value was generated independently of the variant, so the conclusion about average order value is true only inside this simulation.
- The revenue projection is simple. It assumes the same traffic and the same revenue per session as in the data, and gives point estimates without confidence intervals.
- ShopeeFood has the smallest sample.
- The test covers one time period. It does not check for novelty effects or random-assignment problems.
- The reason for the ShopeeFood drop is unknown.

## 6. Project structure

| Step | Script | What it does |
|---|---|---|
| 1 | `01_generate_data.py` | Generates the simulated dataset |
| 2 | `02_explore_data.py` | Checks size, column types, missing values, unique values |
| 3 | `03_conversion.py` | Conversion rate per variant |
| 4 | `04_breakdown_platform.py` | Splits the result by platform |
| 5 | `05_statistical.py` | Chi-square test per segment, with Bonferroni check |
| 6 | `06_funnel_analysis.py` | Funnel drop-off, written in **SQL** (SQLite) |
| 7 | `07_revenue_metrics.py` | Revenue, average order value, revenue per session |
| 8 | `08_impact_scenario.py` | Compares 3 rollout scenarios by estimated monthly revenue |

## 7. How to run

```bash
git clone https://github.com/agnesputrii16/kitchenhub-ab-test-analytics.git
cd kitchenhub-ab-test-analytics
pip install -r requirements.txt

# the dataset used for the numbers above is already included.
# To create a new one: python 01_generate_data.py
# (the random seed is fixed, only the dates change with the day you run it)

python 02_explore_data.py
python 03_conversion.py
python 04_breakdown_platform.py
python 05_statistical.py
python 06_funnel_analysis.py
python 07_revenue_metrics.py
python 08_impact_scenario.py
```

## 8. Possible next steps

- Build an interactive dashboard (Tableau or Power BI)
- Add confidence intervals to the revenue estimates
- Test the segment differences by brand as well as by platform

## Author

**Agnes Putri Istiwana**: data analytics, Python, SQL, Power BI.
[LinkedIn](https://linkedin.com/in/agnesputrii16) | [GitHub](https://github.com/agnesputrii16)

Related project: [Ordivo SaaS Analytics](https://github.com/agnesputrii16/ordivo-saas-analytics) (churn and cohort analysis)