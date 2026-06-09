"""
ml_model.py
Part 4 - Machine Learning:
  - Feature encoding and scaling
  - Linear, Ridge, Lasso, Random Forest Regression
  - Evaluation: MAE, MSE, RMSE, R2
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_csv


# ── 1. Load & Prepare Data ────────────────────────────────────────────────────
def prepare_data(rows):
    df = pd.DataFrame(rows)

    # Cast numeric columns
    df["Sales"]    = pd.to_numeric(df["Sales"])
    df["Profit"]   = pd.to_numeric(df["Profit"])
    df["Discount"] = pd.to_numeric(df["Discount"])
    df["Quantity"] = pd.to_numeric(df["Quantity"])

    # ── Feature Encoding ──────────────────────────────────────────────────────
    # Convert categorical columns to numbers using LabelEncoder
    le = LabelEncoder()
    df["Category_enc"] = le.fit_transform(df["Category"])
    df["Region_enc"]   = le.fit_transform(df["Region"])
    df["Segment_enc"]  = le.fit_transform(df["Segment"])
    df["ShipMode_enc"] = le.fit_transform(df["Ship Mode"])

    print("   Encoded columns:")
    print(f"   Category : {df['Category'].unique()} → {df['Category_enc'].unique()}")
    print(f"   Region   : {df['Region'].unique()} → {df['Region_enc'].unique()}")
    print(f"   Segment  : {df['Segment'].unique()} → {df['Segment_enc'].unique()}")

    # ── Features & Target ─────────────────────────────────────────────────────
    features = ["Quantity", "Discount", "Profit",
                "Category_enc", "Region_enc", "Segment_enc", "ShipMode_enc"]

    X = df[features]
    y = df["Sales"]

    print(f"\n   Features : {features}")
    print(f"   Target   : Sales")
    print(f"   Dataset  : {X.shape[0]} rows × {X.shape[1]} features")

    return X, y, features


# ── 2. Feature Scaling ────────────────────────────────────────────────────────
def scale_features(X_train, X_test):
    """StandardScaler: mean=0, std=1 for each feature."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


# ── 3. Evaluate Model ─────────────────────────────────────────────────────────
def evaluate(name, y_test, y_pred):
    mae  = mean_absolute_error(y_test, y_pred)
    mse  = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2   = r2_score(y_test, y_pred)

    print(f"\n   {'─'*40}")
    print(f"   Model : {name}")
    print(f"   MAE   : {mae:.2f}")
    print(f"   MSE   : {mse:.2f}")
    print(f"   RMSE  : {rmse:.2f}")
    print(f"   R²    : {r2:.4f}")

    return {"model": name, "MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2,
            "y_pred": y_pred}


# ── 4. Train All Models ───────────────────────────────────────────────────────
def train_models(X, y, features):
    # Train/test split — 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\n   Train size : {len(X_train)} rows")
    print(f"   Test size  : {len(X_test)} rows")

    # Scale features
    X_train_sc, X_test_sc, scaler = scale_features(X_train, X_test)

    results = []

    # ── Linear Regression ─────────────────────────────────────────────────────
    lr = LinearRegression()
    lr.fit(X_train_sc, y_train)
    y_pred_lr = lr.predict(X_test_sc)
    results.append(evaluate("Linear Regression", y_test, y_pred_lr))

    # ── Ridge Regression ──────────────────────────────────────────────────────
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train_sc, y_train)
    y_pred_ridge = ridge.predict(X_test_sc)
    results.append(evaluate("Ridge Regression", y_test, y_pred_ridge))

    # ── Lasso Regression ──────────────────────────────────────────────────────
    lasso = Lasso(alpha=1.0)
    lasso.fit(X_train_sc, y_train)
    y_pred_lasso = lasso.predict(X_test_sc)
    results.append(evaluate("Lasso Regression", y_test, y_pred_lasso))

    # ── Random Forest ─────────────────────────────────────────────────────────
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)   # RF doesn't need scaling
    y_pred_rf = rf.predict(X_test)
    results.append(evaluate("Random Forest", y_test, y_pred_rf))

    # Feature importances from Random Forest
    importances = dict(zip(features, rf.feature_importances_))

    return results, y_test, importances


# ── 5. Summary Table ──────────────────────────────────────────────────────────
def print_summary(results):
    print(f"\n\n{'='*55}")
    print(f"  MODEL COMPARISON SUMMARY")
    print(f"{'='*55}")
    print(f"  {'Model':<25} {'MAE':>8} {'RMSE':>8} {'R²':>8}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8}")
    for r in results:
        print(f"  {r['model']:<25} {r['MAE']:>8.2f} {r['RMSE']:>8.2f} {r['R2']:>8.4f}")

    best = max(results, key=lambda x: x["R2"])
    print(f"\n  ✅ Best model: {best['model']} (R² = {best['R2']:.4f})")
    print(f"{'='*55}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("📂 Loading data...")
    rows = load_csv()

    print("\n🔧 Preparing features...")
    X, y, features = prepare_data(rows)

    print("\n🤖 Training models...")
    results, y_test, importances = train_models(X, y, features)

    print_summary(results)

    print("\n🌲 Random Forest Feature Importances:")
    for feat, imp in sorted(importances.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(imp * 50)
        print(f"   {feat:<15} {bar} {imp:.4f}")

    # Save results for visualizations
    import pickle
    with open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "reports", "ml_results.pkl"), "wb") as f:
        pickle.dump({"results": results, "y_test": y_test,
                     "importances": importances}, f)
    print("\n💾 Results saved to reports/ml_results.pkl")