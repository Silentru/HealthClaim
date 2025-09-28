"""
preprocess.py

A simple preprocessing pipeline:
 - groups categorical keys into: high_prob, low_prob, rare
 - encodes grouped categories as ints
 - fills numeric nulls
 - writes train/test parquet files

Usage:
  python preprocess.py --input claims.csv --out train.parquet --test-out test.parquet
"""
import argparse
import pandas as pd
import numpy as np
import joblib
from data_reader import load_claims, make_class_label

GROUP_THRESH_HIGH = 0.01  # fraction threshold for high-probability group
GROUP_THRESH_LOW = 0.0005

def group_keys(series: pd.Series, label: pd.Series):
    """
    Return an integer-coded series:
      1 = high prob group (P(label=1) >= threshold)
      2 = low prob group (P(label=1) < threshold but seen)
      3 = rare/zero
    Heuristic inspired by the MacHu repo grouping.
    """
    counts = series.value_counts(dropna=False)
    # compute empirical P(label=1 | key)
    stats = {}
    for key, ct in counts.items():
        idx = series == key
        if idx.sum() == 0:
            stats[key] = 3
            continue
        p = label[idx].mean()
        if p >= GROUP_THRESH_HIGH:
            stats[key] = 1
        elif p >= GROUP_THRESH_LOW:
            stats[key] = 2
        else:
            stats[key] = 3
    return series.map(stats).fillna(3).astype(int)

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    # select features
    feat = pd.DataFrame(index=df.index)
    # numeric
    feat["charge"] = df.get("Claim.Charge.Amount", 0.0).astype(float).fillna(0.0)
    # group categorical codes
    for col in ["Procedure.Code", "Diagnosis.Code", "Service.Code", "Revenue.Code"]:
        if col in df.columns:
            feat[col + "_grp"] = group_keys(df[col].astype(str), df["_label"])
        else:
            feat[col + "_grp"] = 3
    # provider specialty and payer as categorical simplified
    if "Provider.Specialty" in df.columns:
        feat["specialty_grp"] = group_keys(df["Provider.Specialty"].astype(str), df["_label"])
    else:
        feat["specialty_grp"] = 3
    if "Payer" in df.columns:
        feat["payer_grp"] = group_keys(df["Payer"].astype(str), df["_label"])
    else:
        feat["payer_grp"] = 3
    feat["_label"] = df["_label"].astype(int)
    return feat

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--test-out", required=True)
    parser.add_argument("--test-fraction", type=float, default=0.2)
    args = parser.parse_args()

    df = load_claims(args.input)
    # example codes set; adjust to your needs or pass externally
    codes = ["F13", "J8G", "JO5", "JB8", "JE1", "JC9", "JF1", "JF9", "JG1", "JPA", "JES"]
    df = make_class_label(df, codes)
    feat = build_features(df)
    # split
    test = feat.sample(frac=args.test_fraction, random_state=42)
    train = feat.drop(test.index)
    train.to_parquet(args.out)
    test.to_parquet(args.test_out)
    print("Wrote train:", args.out, "test:", args.test_out)

if __name__ == "__main__":
    main()