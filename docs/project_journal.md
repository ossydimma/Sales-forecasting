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

## 2026-06-04
 
Completed feature engineering. Output saved to data/processed/train_features.csv.
 
### Date features (7 new columns)
Extracted Year, Month, Day, Week from Date column.
Added IsWeekend flag (1 if DayOfWeek is 6 or 7).
Added IsMonthStart and IsMonthEnd flags — month boundaries often show sales spikes.
 
### Competition feature (1 new column)
CompetitionOpen — months since nearest competitor opened.
Formula: 12 * (Year - CompetitionOpenSinceYear) + (Month - CompetitionOpenSinceMonth).
Negative values clipped to 0 for stores with no competition data.
Mean competition open duration: 7,731 months. Max: 24,187 months (~2,015 years — very old stores).
 
### Promo2 feature (1 new column)
Promo2Active — 1 if the store is actively running a Promo2 campaign on that date.
Logic: store participates in Promo2, current month is in PromoInterval, and
current date is on or after Promo2SinceYear/Week.
Active rate: 14.96% of open days (126,276 rows).
 
Note: verified that the dataset uses "Sept" (not "Sep") in PromoInterval.
Always check the actual data before assuming standard abbreviations.
 
### Encoding
StoreType: a=0, b=1, c=2, d=3
Assortment: a=0, b=1, c=2
StateHoliday: 0=0, a=1, b=2, c=3
 
### Columns dropped (7)
Date, Open, CompetitionOpenSinceMonth, CompetitionOpenSinceYear,
Promo2SinceWeek, Promo2SinceYear, PromoInterval.
These were either replaced by engineered versions or no longer needed.
 
### Final output
Shape: 844,338 rows × 20 columns. Missing values: 0. File size: 49.8MB.
All dtypes are numeric — ready for modelling.
Saved to: data/processed/train_features.csv.
 
### Next step
Modelling (05_modelling.ipynb).
Start with a mean baseline, then linear regression, then LightGBM.
Evaluation metric: RMSPE.