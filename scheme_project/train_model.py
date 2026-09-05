"""
train_model.py
Trains:
  1) An eligibility CLASSIFIER (RandomForestClassifier) benchmarked against
     Logistic Regression, Decision Tree, KNN, and Gradient Boosting.
  2) A match-score REGRESSOR (RandomForestRegressor) for ranking eligible
     schemes by relevance.
Saves the trained models + metrics.json (for the report) to models/.
"""
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, r2_score, mean_absolute_error)

from features import generate_citizens, build_training_pairs, encode_features

SCHEMES_PATH = "data/schemes.csv"


def main():
    schemes = pd.read_csv(SCHEMES_PATH)
    states = sorted(schemes.loc[schemes.level == "State", "state"].unique().tolist()) + ["All India"]

    print("Generating synthetic citizen population...")
    citizens = generate_citizens(400, states, seed=7)
    pairs = build_training_pairs(citizens, schemes)
    print(f"Training pairs: {len(pairs)} | eligible rate: {pairs.eligible.mean():.3f}")

    encoded = encode_features(pairs)
    y_class = encoded.pop("eligible")
    y_reg_full = encoded.pop("match_score")
    X = encoded

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_class, test_size=0.2, random_state=42, stratify=y_class)

    # -------------------- Classifier benchmark --------------------
    models = {
        "Logistic Regression": LogisticRegression(max_iter=500),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=7),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=14, random_state=42),
    }

    metrics = {}
    best_model, best_name, best_f1 = None, None, -1
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        metrics[name] = {"accuracy": round(acc, 4), "precision": round(prec, 4),
                          "recall": round(rec, 4), "f1_score": round(f1, 4)}
        print(f"{name:22s} acc={acc:.4f} prec={prec:.4f} rec={rec:.4f} f1={f1:.4f}")
        if f1 > best_f1:
            best_f1, best_model, best_name = f1, model, name

    print(f"\nBest classifier: {best_name} (f1={best_f1:.4f})")

    # -------------------- Match-score regressor (Random Forest) --------------------
    # Train only on eligible pairs (regression target is meaningful there)
    elig_mask = y_class == 1
    Xr = X[elig_mask]
    yr = y_reg_full[elig_mask]
    Xr_train, Xr_test, yr_train, yr_test = train_test_split(Xr, yr, test_size=0.2, random_state=42)

    reg = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)
    reg.fit(Xr_train, yr_train)
    reg_preds = reg.predict(Xr_test)
    r2 = r2_score(yr_test, reg_preds)
    mae = mean_absolute_error(yr_test, reg_preds)
    metrics["Match Score Regressor (Random Forest)"] = {"r2_score": round(r2, 4), "mae": round(mae, 4)}
    print(f"\nMatch score regressor -> R2={r2:.4f}  MAE={mae:.4f}")

    # -------------------- Save artifacts --------------------
    joblib.dump({"model": models["Random Forest"], "columns": list(X.columns)},
                "models/eligibility_classifier.joblib")
    joblib.dump({"model": reg, "columns": list(X.columns)},
                "models/match_score_regressor.joblib")

    with open("models/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("\nSaved models/eligibility_classifier.joblib, "
          "models/match_score_regressor.joblib, models/metrics.json")


if __name__ == "__main__":
    main()
