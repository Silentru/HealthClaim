"""
data_reader.py

Small utilities to read a CSV of claims and generate a binary class label
based on Denial.Reason.Code like the sample repo.

Expected input columns (at minimum):
 - Denial.Reason.Code (string)
 - Claim.Charge.Amount (numeric)
 - Procedure.Code, Diagnosis.Code, Service.Code, Revenue.Code (strings)
 - Payer, Provider.Specialty (optional)

Usage:
  from data_reader import load_claims, make_class_label
  df = load_claims("claims.csv")
  df = make_class_label(df, codes_of_interest=["F13","J8G",...])
"""
import pandas as pd
from typing import List

def load_claims(path: str) -> pd.DataFrame:
    """Load CSV into DataFrame with safe dtypes."""
    df = pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""])
    # attempt to coerce numeric fields
    if "Claim.Charge.Amount" in df.columns:
        df["Claim.Charge.Amount"] = pd.to_numeric(df["Claim.Charge.Amount"], errors="coerce").fillna(0.0)
    # unify column names if needed
    return df

def make_class_label(df: pd.DataFrame, codes_of_interest: List[str]) -> pd.DataFrame:
    """Create _label column: 1 if Denial.Reason.Code in codes_of_interest else 0"""
    if "Denial.Reason.Code" not in df.columns:
        raise ValueError("Input CSV must have Denial.Reason.Code column for labeling.")
    df["_label"] = df["Denial.Reason.Code"].apply(lambda x: 1 if x in set(codes_of_interest) else 0)
    return df

if __name__ == "__main__":
    # simple CLI test
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "claims.csv"
    df = load_claims(path)
    print("Loaded", len(df), "rows. Columns:", list(df.columns)[:10])