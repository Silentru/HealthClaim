# predict.py
"""
Load saved model and score new claims. Output CSV with risk score + suggestion.

Usage:
  python predict.py --model out/model.joblib --input new_claims.csv --out scored.csv
"""
import argparse
import pandas as pd
import joblib

from data_reader import load_claims, make_class_label  # make_class_label may be unused here
from preprocess import build_features

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    # Load model (dict or raw)
    saved = joblib.load(args.model)
    if isinstance(saved, dict) and "model" in saved:
        model = saved["model"]
        feature_cols = saved.get("feature_cols")
    else:
        model = saved
        feature_cols = None

    # Load raw input claims and build features
    df_raw = load_claims(args.input)

    # If input lacks the denial code (normal for production), create a dummy column
    if "_label" not in df_raw.columns:
        df_raw["_label"] = 0  # placeholder so build_features can run uniformly

    feat = build_features(df_raw)

    # Align columns to what the model expects
    if feature_cols is not None:
        missing = [c for c in feature_cols if c not in feat.columns]
        for c in missing:
            feat[c] = 0
        X = feat[feature_cols]
    else:
        X = feat

    # --------- Safe probability extraction ----------
    if hasattr(model, "predict_proba"):
        proba_all = model.predict_proba(X)
        if hasattr(model, "classes_"):
            classes = list(model.classes_)
            if 1 in classes and proba_all.ndim == 2 and proba_all.shape[1] > 1:
                pos_idx = classes.index(1)
                proba = proba_all[:, pos_idx]
            else:
                proba = proba_all[:, 0]
        else:
            proba = proba_all[:, 0]
    else:
        # Fallbacks if predict_proba is not available
        if hasattr(model, "decision_function"):
            from sklearn.preprocessing import MinMaxScaler
            proba = MinMaxScaler().fit_transform(
                model.decision_function(X).reshape(-1, 1)
            ).ravel()
        else:
            proba = model.predict(X).astype(float)

    # Compose output
    df_out = df_raw.copy()
    df_out["denial_risk"] = proba
    df_out["suggestion"] = df_out["denial_risk"].apply(
        lambda p: "Attach missing auth" if p >= 0.7 else ("Review coding" if p >= 0.4 else "No action")
    )
    df_out.to_csv(args.out, index=False)
    print("Wrote scored claims to", args.out)

if __name__ == "__main__":
    main()
