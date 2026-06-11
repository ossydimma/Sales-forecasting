import pandas as pd
import numpy as np
import joblib

def load_model(model_path='../models/lgbm_v7_final.joblib'):
    return joblib.load(model_path)

def predict_sales(model, input_data: pd.DataFrame) -> np.ndarray:
    """
    input_data: DataFrame with the same features used during training.
    Returns predicted sales values.
    """
    log_preds = model.predict(input_data)
    return np.maximum(np.expm1(log_preds), 0)

if __name__ == '__main__':
    model = load_model()
    print("Model loaded successfully.")
    print(f"Expected features: {model.feature_name()}")