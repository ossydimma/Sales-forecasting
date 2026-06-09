# Rossmann Store Sales Forecasting

## Business Problem

Retailers struggle to estimate future demand accurately.
Overestimating leads to excess inventory and wasted cost.
Underestimating leads to stock shortages and lost revenue.

This project builds a machine learning model to forecast daily sales for Rossmann stores
using historical sales data, store characteristics, and promotional information.
The goal is to give store managers and planners a reliable demand signal they can act on.

---

## Dataset

**Source:** [Rossmann Store Sales — Kaggle Competition](https://www.kaggle.com/competitions/rossmann-store-sales)

| File | Rows | Description |
|------|------|-------------|
| train.csv | 1,017,209 | Daily sales per store (2013–2015) |
| store.csv | 1,115 | Store-level attributes |
| test.csv | 41,088 | Stores and dates to predict |

> **Note:** Raw data files are not tracked in this repository.
> Download the dataset from Kaggle and place CSVs in `data/raw/`.

**Target variable:** `Sales` — daily revenue per store

---

## Project Structure

```
rossmann-sales-forecasting/
│
├── data/
│   ├── raw/                        # Original CSVs (not tracked by git)
│   └── processed/                  # Cleaned outputs (not tracked by git)
│
├── docs/
│   ├── data_dictionary.md
│   └── project_journal.md          # Day-by-day decisions and learnings
│
├── images/                         # Charts saved from notebooks
├── models/                         # Saved model files (not tracked by git)
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_modelling.ipynb
│   ├── 06_evaluation.ipynb
│   ├── 07_modelling_v2.ipynb       # Iterative improvement: 0.1852 → 0.1140
│   └── 08_tuning.ipynb             # Optuna hyperparameter search → 0.1148
│
├── .gitignore
└── README.md
```

---

## Final Model Results

| Model | RMSPE | vs Baseline |
|-------|-------|-------------|
| Mean Baseline | 0.5445 | — |
| Linear Regression | 0.4613 | −15.3% |
| LightGBM v1 | 0.1852 | −66.0% |
| LightGBM v7 (manual) | 0.1140 | −79.1% |
| **LightGBM tuned (Optuna)** | **0.1148** | **−78.9%** |

> V7 manual remains the best single model. Optuna confirmed the feature set is near-optimal.

### Improvement breakdown (07_modelling_v2.ipynb)

| Version | Change | RMSPE | Delta |
|---------|--------|-------|-------|
| Original | 998 rounds, base features | 0.1852 | — |
| V1 | Fixed rounds — converged at 3581 | 0.1606 | −0.025 |
| V2 | + StoreMeanSales | 0.1414 | −0.019 |
| V3 | + StoreDowMean | 0.1372 | −0.004 |
| StorePromoLift | Tested — no gain, dropped | 0.1372 | 0.000 |
| V4 | + DaysToEaster | 0.1162 | −0.021 |
| V5 | Log-transform target | 0.1146 | −0.002 |
| V6 | lr=0.02, num_leaves=127 | 0.1149 | — |
| **V7** | **lr=0.01, min_child_samples=40** | **0.1140** | **−0.071 total** |

### Top 5 features by importance
1. **Store** — individual store identity dominates all other signals
2. **DaysToEaster** — floating holiday feature engineered from domain knowledge
3. **StoreMeanSales** — per-store baseline encoded from training data
4. **CompetitionDistance** — proximity to competitor is highly predictive
5. **Promo** — daily promotions are the strongest actionable lever

---

## Key Findings from EDA

- **Promotions drive 81% higher sales** (7,991 avg with promo vs 4,406 without)
- **December peaks 24% above the yearly average** — clear holiday seasonality
- **Store type B outperforms all others** — avg 10,231 vs ~6,900 for types A, C, D
- **Monday and Sunday are the strongest trading days** (~8,200 avg); Saturday is weakest
- **Easter and Christmas** drive the highest single-day sales (~9,700–9,900)
- **172,817 closed-store days** identified and excluded before any analysis

---

## Data Cleaning Summary

| Column | Issue | Strategy |
|--------|-------|----------|
| CompetitionDistance | 3 missing (0.27%) | Filled with median (2,325m) |
| CompetitionOpenSinceMonth/Year | 354 missing (31.75%) | Filled with 0 — no competitor data |
| Promo2SinceWeek/Year | 544 missing (48.79%) | Filled with 0 — stores not in Promo2 |
| PromoInterval | 544 missing (48.79%) | Filled with "None" — stores not in Promo2 |
| Open=1, Sales=0 | 54 rows (0.01%) | Dropped — likely data entry errors |

**Clean dataset:** 844,338 rows × 18 columns, zero missing values

---

## Feature Engineering Summary

| Feature | Type | Description |
|---------|------|-------------|
| Year, Month, Day, Week | Date | Extracted from Date column |
| IsWeekend | Date | 1 if DayOfWeek is Saturday or Sunday |
| IsMonthStart, IsMonthEnd | Date | Flags for month boundaries |
| CompetitionOpen | Competition | Months since nearest competitor opened |
| Promo2Active | Promotion | 1 if store is actively in a Promo2 cycle on that date |
| StoreMeanSales | Store | Per-store mean sales — calculated from training data only |
| StoreDowMean | Store | Per-store per-day-of-week mean — calculated from training data only |
| DaysToEaster | Holiday | Days to nearest Easter — fixes floating holiday problem in April |

---

## Workflow

| Phase | Notebook | Status |
|-------|----------|--------|
| Data understanding | 01_data_understanding.ipynb | ✅ Complete |
| Exploratory analysis | 02_eda.ipynb | ✅ Complete |
| Data cleaning | 03_data_cleaning.ipynb | ✅ Complete |
| Feature engineering | 04_feature_engineering.ipynb | ✅ Complete |
| Modelling (baseline) | 05_modelling.ipynb | ✅ Complete |
| Evaluation | 06_evaluation.ipynb | ✅ Complete |
| Iterative improvement | 07_modelling_v2.ipynb | ✅ Complete |
| Hyperparameter tuning | 08_tuning.ipynb | ✅ Complete |

---

## Tools and Libraries

- Python 3.13 · pandas · numpy · matplotlib · seaborn
- scikit-learn · LightGBM · SHAP · Optuna

---

## Author

Built in public as a portfolio project while transitioning into data science.
Follow the build on [LinkedIn](https://www.linkedin.com/in/osita-jerry)

GitHub: [github.com/ossydimma/Sales-forecasting](https://github.com/ossydimma/Sales-forecasting)