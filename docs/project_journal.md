# Project Journal

## 2026-06-01

Downloaded Rossmann dataset.

Loaded train.csv and store.csv.

Train shape: 1,017,209 rows

Store shape: 1,115 rows

train.csv contains no missing values.

store.csv contains missing values in competition and promotion-related fields.

Initial hypothesis:
Some missing promotion fields may indicate stores not participating in Promo2 rather than incomplete data.

Date column is currently stored as an object and will require conversion to datetime.

Initial observations:
- Sales is the target variable.
- Store information is stored separately.
- Datasets can likely be merged on Store.

---

## 2026-06-02

Completed exploratory data analysis on the Rossmann dataset.

### Data filtering
Discovered 172,817 rows where stores were closed (Open=0) with Sales=0.
Filtered these out before analysis — all EDA performed on 844,392 open-store days only.
This was critical: including closed days was distorting day-of-week averages, especially Sunday.

### Sales distribution
Average sales per open day: 6,955. Range: 0 to 41,551.
Distribution is roughly bell-shaped with a right skew — some stores are very high performers.

### Seasonality findings
December is the strongest month with average sales of 8,609 — 24% above the yearly average.
September is the weakest month at 6,546.
Monday and Sunday are the strongest days (~8,200 average). Saturday is the weakest at 5,875.
The weekly U-shape pattern (strong Mon/Sun, dip mid-week, recover Friday) is consistent across years.

### Promotion impact
Promo days drive 81% higher average sales (7,991 vs 4,406 without promo).
Promo days also bring 58% more customers (820 vs 518).
Important lesson: the heatmap correlation coefficient for Promo vs Sales looked low (~0.3),
but the groupby mean tells the real story. Correlation coefficients understate binary feature importance.
Promo will likely be the strongest feature in the model.

### Store type
Store type B significantly outperforms types A, C, D (avg 10,231 vs ~6,900).
Store type B also has nearly 3x the customer footfall of other types.
StoreType must be included as a feature in modelling.

### Holiday effects
Easter and Christmas state holidays drive the highest sales (9,744–9,888).
School holidays show a modest positive effect (7,200 vs 6,897 on normal days).

### Competition distance
Stores with very close competitors (<500m) do not necessarily underperform.
This is counterintuitive — may reflect that high-footfall locations attract both stores and competition.

### Next step
Move to data cleaning notebook (03_data_cleaning.ipynb).
Handle missing values in store.csv, fix data types, and prepare a clean merged dataframe
ready for feature engineering.

## 2026-06-03

 Cleaning Summary

### train.csv
- No missing values found
- Date converted from object to datetime64
- StateHoliday confirmed as string type
- 54 rows dropped (Open=1, Sales=0) — 0.01% of open days, likely data entry errors
- 172,817 closed-store rows excluded

### store.csv
- CompetitionDistance: 3 missing → filled with median (2,325m)
- CompetitionOpenSinceMonth/Year: 354 missing → filled with 0 (no competitor data)
- Promo2SinceWeek/Year: 544 missing → filled with 0 (stores not in Promo2 scheme)
- PromoInterval: 544 missing → filled with "None" (stores not in Promo2 scheme)

### Merged output
- Shape: (844,338, 18)
- Missing values: 0
- Saved to: data/processed/train_clean.csv