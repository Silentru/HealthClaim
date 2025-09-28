# HealthClaim
AI-Native Claims Denial &amp; Rework Reduction (Healthcare)
```markdown
# Denial Risk Starter Pipeline

What this repo provides
- Minimal end-to-end pipeline that:
  1) reads claim rows from CSV,
  2) labels claims by denial reason codes,
  3) preprocesses (categorical grouping + numeric handling),
  4) trains a RandomForest classifier to predict denial (binary),
  5) scores new claims and writes a CSV of risk scores + simple why (feature importances).

Why this is useful
- Matches the structure of the MacHu-GWU repo but uses modern sklearn patterns and is simpler to run.
- Designed as a reproducible prototype you can use in a 12-week pilot to produce denial risk scoring and hipaa-safe outputs.

Quick start
1. Create a Python 3.9+ venv and install deps:
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt

2. Prepare input:
   - Provide a CSV file named `claims.csv` with columns:
     - Denial.Reason.Code (string), Claim.Charge.Amount (numeric), Procedure.Code, Diagnosis.Code, Service.Code, Revenue.Code, Provider.Specialty (optional), Payer
     - See data_reader.py for sample mapping.

3. Generate train/test and train:
   python preprocess.py --input claims.csv --out train.parquet --test-out test.parquet
   python train_model.py --train train.parquet --test test.parquet --model out/model.joblib

4. Score new claims:
   python predict.py --model out/model.joblib --input new_claims.csv --out scored.csv

Next steps to production (exact actionable list)
- Data & Legal
  1. Sign BAA with provider and clearinghouse; obtain de-identified or limited-PHI exports.
  2. Get 6–12 months of historical 837/835/appeal outcomes (or extracted CSVs).
- Data engineering
  1. Implement robust EDI parsing (X12 837/835) or ingestion from clearinghouse export APIs.
  2. Build canonical claim schema and daily incremental feed (SFTP/API).
- Models & rules
  1. Replace RF with gradient boosting (XGBoost/LightGBM) and per-payer/per-specialty models.
  2. Add deterministic payer-rule graph that suggests fixes (non-clinical auto-fixes vs human-in-loop clinical edits).
  3. Add an OCR + EOB denial-reason classifier to handle noisy denial codes.
- System & security
  1. Implement BAA, row-level access, encryption, audit logs, RBAC.
  2. Containerize services, add CI/CD, run security review.
- Pilot integrations & UX
  1. Integrate with one EHR or clearinghouse (Epic App Orchard / Availity).
  2. UI for coder/appeals specialist, prioritized queue by dollars-at-risk.
  3. Human-in-loop approval for code edits, auto-draft appeals.
- Measurement
  1. Baseline denial rate & rework touches.
  2. Run shadow -> A/B pilot as in the 12-week plan in your venture prompt.

If you want I will:
- adapt this pipeline to your specific file columns (give me a sample CSV or the Fill-This-In variables), or
- produce a pilot runbook and data-mapping checklist next.
```