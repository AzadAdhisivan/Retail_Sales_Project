"""
ml_visualizations.py
Part 4 - ML Visualization:
  - Actual vs Predicted plots for all models
  - Feature Importance chart
"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120


# ── Load saved results ────────────────────────────────────────────────────────
def load_results():
    path = os.path.join(REPORTS_DIR, "ml_results.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError("Run ml_model.py first to generate results.")
    with open(path, "rb") as f:
        return pickle.load(f)


# ── 1. Actual vs Predicted — all 4 models in one figure ──────────────────────
def plot_actual_vs_predicted(results, y_test):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Actual vs Predicted Sales", fontsize=16, fontweight="bold", y=1.01)

    axes = axes.flatten()

    for i, r in enumerate(results):
        ax      = axes[i]
        y_pred  = r["y_pred"]
        name    = r["model"]
        r2      = r["R2"]

        ax.scatter(y_test, y_pred, alpha=0.3, s=10, color="#4C72B0")

        # Perfect prediction line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val],
                color="red", linewidth=1.5, linestyle="--", label="Perfect fit")

        ax.set_title(f"{name}\nR² = {r2:.4f}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Actual Sales ($)")
        ax.set_ylabel("Predicted Sales ($)")
        ax.legend(fontsize=8)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "actual_vs_predicted.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved: actual_vs_predicted.png")


# ── 2. Feature Importance ─────────────────────────────────────────────────────
def plot_feature_importance(importances):
    features = list(importances.keys())
    values   = list(importances.values())

    # Sort descending
    sorted_pairs = sorted(zip(features, values), key=lambda x: x[1])
    features_sorted = [p[0] for p in sorted_pairs]
    values_sorted   = [p[1] for p in sorted_pairs]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(features_sorted, values_sorted,
                   color=sns.color_palette("Blues_d", len(features_sorted)))

    ax.set_title("Feature Importance — Random Forest", fontsize=14, fontweight="bold")
    ax.set_xlabel("Importance Score")

    for bar in bars:
        ax.text(bar.get_width() + 0.002,
                bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.4f}",
                va="center", fontsize=9)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "feature_importance.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved: feature_importance.png")


# ── 3. Model Comparison Bar Chart ────────────────────────────────────────────
def plot_model_comparison(results):
    models = [r["model"] for r in results]
    mae    = [r["MAE"]   for r in results]
    rmse   = [r["RMSE"]  for r in results]
    r2     = [r["R2"]    for r in results]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Model Comparison", fontsize=14, fontweight="bold")

    colors = sns.color_palette("muted", len(models))

    for ax, metric, values, label in zip(
        axes,
        ["MAE", "RMSE", "R²"],
        [mae, rmse, r2],
        ["Mean Absolute Error", "Root Mean Squared Error", "R² Score"]
    ):
        bars = ax.bar(models, values, color=colors)
        ax.set_title(metric, fontsize=12, fontweight="bold")
        ax.set_ylabel(label)
        ax.set_xticklabels(models, rotation=15, ha="right", fontsize=8)

        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(values) * 0.01,
                    f"{bar.get_height():.2f}",
                    ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    path = os.path.join(REPORTS_DIR, "model_comparison.png")
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"   ✅ Saved: model_comparison.png")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("📊 Loading ML results...")
    data = load_results()

    results     = data["results"]
    y_test      = data["y_test"]
    importances = data["importances"]

    print("\n🎨 Generating visualizations...")
    plot_actual_vs_predicted(results, y_test)
    plot_feature_importance(importances)
    plot_model_comparison(results)

    print(f"\n✅ All ML charts saved to reports/")