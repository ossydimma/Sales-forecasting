import joblib
import pandas as pd
import numpy as np


def load_model(model_path="models/lgbm_v7_final.joblib"):
    """Load the trained LightGBM model from disk."""
    return joblib.load(model_path)


def predict_sales(model, input_df: pd.DataFrame) -> np.ndarray:
    """
    Predict daily sales for one or more store-days.

    Parameters
    ----------
    model : loaded LightGBM model
    input_df : pd.DataFrame with the following columns:
        Store, DayOfWeek, Promo, StateHoliday, SchoolHoliday,
        StoreType, Assortment, CompetitionDistance, Promo2,
        Year, Month, Day, Week, IsWeekend, IsMonthStart,
        IsMonthEnd, CompetitionOpen, Promo2Active,
        StoreMeanSales, StoreDowMean, DaysToEaster

    Returns
    -------
    np.ndarray of predicted sales values (original scale, not log)
    """
    log_preds = model.predict(input_df)
    return np.maximum(np.expm1(log_preds), 0)


if __name__ == "__main__":
    model = load_model()
    print("Model loaded successfully.")
    print(f"Expected features ({len(model.feature_name())}):")
    print(model.feature_name())

    # Example: run on a sample row to verify end-to-end
    sample = pd.DataFrame([{
        "Store": 1, "DayOfWeek": 5, "Promo": 1,
        "StateHoliday": 0, "SchoolHoliday": 1,
        "StoreType": 2, "Assortment": 0,
        "CompetitionDistance": 1270.0, "Promo2": 0,
        "Year": 2015, "Month": 7, "Day": 31,
        "Week": 31, "IsWeekend": 0,
        "IsMonthStart": 0, "IsMonthEnd": 1,
        "CompetitionOpen": 82.0, "Promo2Active": 0,
        "StoreMeanSales": 5200.0, "StoreDowMean": 4800.0,
        "DaysToEaster": 117
    }])

    prediction = predict_sales(model, sample)
    print(f"\nSample prediction: £{prediction[0]:,.0f} predicted sales")