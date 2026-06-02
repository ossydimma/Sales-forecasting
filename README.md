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

**Target variable:** `Sales` — daily revenue per store

---

## Project Structure

```
rossmann-sales-forecasting/
│
├── data/
│   ├── raw/                        # Original unmodified CSVs (not tracked by git)
│   └── processed/                  # Cleaned data outputs (not tracked by git)
│
├── docs/
│   ├── data_dictionary.md          # Column definitions and notes
│   └── project_journal.md          # Day-by-day decisions and learnings
│
├── images/                         # Charts and visuals saved from notebooks
│
├── models/                         # Saved model files (not tracked by git)
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_modelling.ipynb
│   └── 06_evaluation.ipynb
│
├── reports/                        # Final summary outputs
├── src/                            # Reusable Python scripts (functions, helpers)
├── .gitignore
└── README.md
```

---

## Key Findings from EDA

Before building any model, the data revealed several strong business patterns:

- **Promotions drive 81% higher sales** (7,991 avg with promo vs 4,406 without)
- **December peaks 24% above the yearly average** — clear holiday seasonality
- **Store type B outperforms all others** with average sales of 10,231 vs ~6,900 for types A, C, D
- **Monday and Sunday are the strongest trading days** (~8,200 avg); Saturday is weakest (5,875)
- **Easter and Christmas state holidays** drive the highest single-day sales (~9,700–9,900)
- **172,817 closed-store days** were identified and excluded from analysis — a critical data quality step

---

## Workflow

| Phase | Notebook | Status |
|-------|----------|--------|
| Data understanding | 01_data_understanding.ipynb | ✅ Complete |
| Exploratory analysis | 02_eda.ipynb | ✅ Complete |
| Data cleaning | 03_data_cleaning.ipynb | 🔄 In progress |
| Feature engineering | 04_feature_engineering.ipynb | ⏳ Pending |
| Modelling | 05_modelling.ipynb | ⏳ Pending |
| Evaluation | 06_evaluation.ipynb | ⏳ Pending |

---

## Evaluation Metric

**RMSPE — Root Mean Square Percentage Error**

The competition metric penalises percentage errors rather than absolute ones,
which treats a 10% miss on a small store equally to a 10% miss on a large store.

---

## Tools and Libraries

- Python 3.13
- pandas, numpy
- matplotlib, seaborn
- scikit-learn
- LightGBM (planned)

---

## Author

Built in public as a portfolio project while transitioning into data science.
Follow the build on [LinkedIn](https://www.linkedin.com/in/osita-jerry)

GitHub: [github.com/ossydimma/Sales-forecasting](https://github.com/ossydimma/Sales-forecasting)
