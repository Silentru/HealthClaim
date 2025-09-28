# train_model.py
import os
import argparse
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--test", required=True)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    train = pd.read_parquet(args.train)
    test = pd.read_parquet(args.test)

    # X / y
    X_train = train.drop(columns=["_label"])
    y_train = train["_label"]
    X_test = test.drop(columns=["_label"])
    y_test = test["_label"]

    # Model
    model = RandomForestClassifier(n_estimators=200, max_depth=7, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)

    # --------- Safe predictions / probabilities ----------
    y_pred = model.predict(X_test)
    proba = model.predict_proba(X_test)

    if hasattr(model, "classes_"):
        classes = list(model.classes_)
        if 1 in classes and proba.ndim == 2 and proba.shape[1] > 1:
            pos_idx = classes.index(1)
            y_prob = proba[:, pos_idx]
        else:
            # single-class case
            y_prob = proba[:, 0]
    else:
        if hasattr(model, "decision_function"):
            from sklearn.preprocessing import MinMaxScaler
            y_prob = MinMaxScaler().fit_transform(
                model.decision_function(X_test).reshape(-1, 1)
            ).ravel()
        else:
            y_prob = model.predict(X_test).astype(float)

    # Metrics (skip ROC AUC if test set is single-class)
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)) if len(np.unique(y_test)) > 1 else None,
    }
    print("Metrics:", metrics)

    # Save model (and feature columns)
    os.makedirs(os.path.dirname(args.model) or ".", exist_ok=True)
    joblib.dump({"model": model, "feature_cols": X_train.columns.tolist()}, args.model)
    print("Saved model to:", args.model)

if __name__ == "__main__":
    main()
