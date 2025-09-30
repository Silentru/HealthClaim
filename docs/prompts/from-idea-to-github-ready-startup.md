# 🔧 “From Idea to GitHub-Ready Startup” — Execution Super-Prompt

**Role:** You are a founding CTO + product lead + GTM strategist in one. Your job is to transform a single startup idea into a **launchable plan** with **architecture, repo scaffolding, code snippets, CI/CD, docs, GTM**, and a **90-day execution schedule**.

**Output format:** Follow the section order below exactly. Use tight, numbered steps and checklists. Include code blocks and command lines where requested. Cite **primary, credible sources** and run an **unbiased, adversarial search** (see Section 2C).

---

## 0) Inputs (fill before you start)

* **Idea (1–2 sentences):**
* **Target user / ICP:**
* **Must-have outcomes for v1 (top 3):**
* **Regulatory/constraints (if any):**
* **Preferred stack (if any):**

---

## 1) One-Page Strategy (clear & falsifiable)

1. **Problem → Why now:** 5 bullets on structural drivers (tech, regulation, macro).
2. **User + Job-to-Be-Done:** primary persona, # of times per month the pain occurs, $$ impact.
3. **Wedge & 10× edge:** what becomes **dramatically** faster/cheaper/safer vs status quo.
4. **Success target (12 months):** revenue, active logos, payback period, NDR.
5. **Kill switch:** measurable conditions that stop the project early.

---

## 2) Evidence Pack (sources + unbiased protocol)

### 2A. Market & compliance facts (≤18 months old)

* **TAM/SAM/SOM with method:** show math and assumptions.
* **Regulatory drivers/mandates** (HIPAA, SOC2, PCI, etc.).
* **Benchmarks:** CAC/payback, price bands, gross margins, sales cycle.

> **Cite at least 3 primary sources:** government/multilateral (e.g., BLS/BEA/World Bank/IMF/OECD), regulator filings (SEC 10-K/S-1), standards bodies (NIST/ISO), tier-1 research (McKinsey/Gartner/BCG). Use inline citations like **(BLS 2025)** and link.

### 2B. Triangulation

* Present a **table** of each critical metric with **2+ independent sources** and explain variances. Choose the **conservative** value for planning.

### 2C. Unbiased & Adversarial Search (mandatory)

* List **counter-hypotheses** (“why this won’t work”).
* Run adversarial queries (e.g., “<market> overestimated”, “price compression”, “API deprecation”).
* Include **one credible dissenting source**, discuss impact, and adjust plan if needed.
* Keep a **limitations** box + **audit log** of excluded sources.

---

## 3) Product Spec (v0 → v1)

1. **Top 3 use cases/workflows** (with start-to-finish steps and acceptance criteria).
2. **Must-have v1 scope** (≤ 6 weeks build): each item has owner, complexity (S/M/L), and testable outcome.
3. **Non-goals** (what we won’t build yet).
4. **Data & privacy:** PII handling, data retention, encryption (at rest/in transit), tenant isolation.
5. **Reliability SLOs:** uptime target, RPO/RTO, rate limits, backoff policies.

---

## 4) System Architecture (clear, shippable)

* **Diagram (describe in text):**

  * Frontend (Next.js/React), API (FastAPI or Node/Express), DB (Postgres), object storage (S3), auth (JWT/OAuth), queue (RQ/Celery or BullMQ), observability (OpenTelemetry), feature flags, and background workers.
* **Core entities & relationships** (list tables/collections + fields).
* **Security model:** authZ roles, secrets mgmt (.env + GitHub Actions), audit logging.

---

## 5) GitHub: Repo, Branching, CI/CD, Issues (step-by-step)

### 5A. Create the repo (commands)

```bash
# 1) Create local repo
mkdir startup && cd startup
git init

# 2) Create monorepo structure
mkdir -p apps/web apps/api packages/ui infra .github/workflows docs
touch README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md
echo "venv/" >> .gitignore && echo "node_modules/" >> .gitignore && echo ".env*" >> .gitignore

# 3) First commit
git add .
git commit -m "chore: init monorepo scaffold"

# 4) Create GitHub repo (via CLI; install gh first)
gh repo create your-org/startup --public --source=. --remote=origin --push
```

### 5B. Branching & PR hygiene

* **Branches:** `main` (protected), `feat/*`, `fix/*`, `chore/*`.
* **PR Template:** requires description, screenshots, tests, rollback plan.
* **CODEOWNERS:** require review by `@core-team` for `/apps/api/**` and `/infra/**`.
* **Status checks required:** unit tests, lint, typecheck, build.

### 5C. GitHub Issue templates (copy/paste)

**.github/ISSUE_TEMPLATE/feature_request.md**

```md
---
name: "Feature request"
about: Propose a user-facing improvement
labels: enhancement
---
**User story**
As a [persona], I need [capability] so that [outcome].

**Acceptance criteria**
- [ ] ...

**Non-goals**
- [ ] ...
```

**.github/ISSUE_TEMPLATE/bug_report.md**

```md
---
name: "Bug report"
about: Something broke or misbehaves
labels: bug
---
**Steps to reproduce**
1.
2.
3.

**Expected vs actual**
**Logs / screenshots**
**Severity** (blocker/major/minor)
```

---

## 6) Code Scaffold (frontend, API, DB, Docker, CI)

### 6A. Minimal Next.js (app router) + Tailwind (apps/web)

```bash
cd apps && npx create-next-app@latest web --typescript --eslint --src-dir --app --no-tailwind
cd web && npx tailwindcss init -p
# Configure tailwind.config.js and globals.css; add a basic page with auth-aware layout.
```

**Example page:** `apps/web/app/page.tsx`

```tsx
export default function Home() {
  return (
    <main className="p-8 max-w-3xl">
      <h1 className="text-2xl font-bold">Welcome</h1>
      <p className="mt-2">Your product’s v1 dashboard placeholder.</p>
    </main>
  );
}
```

### 6B. FastAPI + SQLAlchemy + Postgres (apps/api)

```bash
cd ../ && mkdir -p api && cd api
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn[standard] pydantic-settings sqlalchemy psycopg[binary] alembic python-jose[cryptography] passlib[bcrypt]
```

`apps/api/main.py`

```py
from fastapi import FastAPI, Depends, HTTPException
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
settings = Settings()

app = FastAPI(title="Startup API")

@app.get("/healthz")
def healthz():
    return {"ok": True}
```

`apps/api/models.py` (example: tenants, users, projects)

```py
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import String, ForeignKey
Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id"))
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    tenant = relationship("Tenant")
```

### 6C. Docker & Compose (root)

`Dockerfile.api`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY apps/api/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY apps/api /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`Dockerfile.web`

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY apps/web/package*.json ./
RUN npm ci
COPY apps/web .
RUN npm run build
EXPOSE 3000
CMD ["npm","start"]
```

`docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: postgres
    ports: ["5432:5432"]
  api:
    build: { context: ., dockerfile: Dockerfile.api }
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/postgres
      JWT_SECRET: change-me
    depends_on: [db]
    ports: ["8000:8000"]
  web:
    build: { context: ., dockerfile: Dockerfile.web }
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on: [api]
    ports: ["3000:3000"]
```

### 6D. GitHub Actions CI

**.github/workflows/ci.yml**

```yaml
name: CI
on: [push, pull_request]
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node
        uses: actions/setup-node@v4
        with: { node-version: 20 }
      - name: Web install & build
        working-directory: apps/web
        run: |
          npm ci
          npm run build
      - name: Set up Python
        uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - name: API deps & lint
        working-directory: apps/api
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          python -m compileall .
```

---

## 7) Observability & Security (day-1)

* **Logging:** structured JSON logs; request IDs propagated (FastAPI middleware).
* **Metrics:** basic Prometheus counters (req/sec, p95 latency, error rate).
* **Tracing:** OpenTelemetry SDK; export to OTLP (Jaeger/Tempo).
* **Secrets:** `.env.local` for dev, GitHub **encrypted repo secrets** for CI/CD.
* **AuthZ:** roles: `owner`, `admin`, `member`, `readOnly`; JWT with short TTL + refresh.
* **Backups:** nightly DB snapshot; restore runbook.

---

## 8) Data model (tables + migrations)

* **Tables:** `tenants`, `users`, `projects`, `events`, `billing_subscriptions`, `audit_logs`.
* **Migrations:** initialize with Alembic; require migration PR for any schema change.
* **PII map:** which columns hold PII; masking policy; retention schedule.

---

## 9) Pricing & Billing

* **Plan grid:** Free (usage-cap), Pro (seat-based or usage), Enterprise (SLA + SSO).
* **Metering events:** define `event_name`, dimensions, aggregation window.
* **Stripe integration:** create products/prices; webhook for `invoice.paid` → upgrade feature flags.

---

## 10) GTM & Sales Motion

* **Acquisition:** content that answers high-intent queries; founder-led outreach to 50 design partners.
* **Activation:** in-app onboarding checklist; demo dataset; time-to-first-value < 15 minutes.
* **Pricing page:** clear ROI calculator; SOC2/HIPAA signals if relevant.
* **Sales:** 3-stage pipeline (discovery → pilot → expand); weekly forecast; referenceable wins.

---

## 11) 90-Day Execution Plan (week-by-week)

**Weeks 1–2: Validation**

1. Interview 10–15 ICPs; document workflows & KPIs.
2. Adversarial research + triangulation; fill Evidence Pack; decide go/no-go.
3. Repo init, CI, Docker, health checks, skeleton UI.

**Weeks 3–6: Build v1**
4. Implement top 3 workflows end-to-end.
5. Auth, multi-tenant, basic RBAC, audit logs.
6. Instrument metrics, error tracking, and seeds.
7. Ship to **5 design partners**; capture baseline KPIs.

**Weeks 7–9: Prove value**
8. Iterate weekly on blockers; improve time-to-value.
9. Add metering + Stripe; publish pricing page.
10. Collect retention/usage; target **≥80% monthly logo retention** in pilots.

**Weeks 10–12: Scale readiness**
11. Harden reliability (p95 latency < 400ms; SLO runbook).
12. Security pass (secrets, backups, least privilege).
13. Launch site, case studies, and public roadmap.
14. Set up SDR/Founder outbound to 100 prospects.

---

## 12) Metrics & Review Cadence

* **North Star:** time-to-first-value (TTFV) + weekly active teams.
* **Unit econ:** CAC payback, CLV:CAC, gross margin, churn.
* **Review:** Monday metrics review; Friday ship review; monthly premortem update.

---

## 13) Risks & Mitigations

* **Platform/API dependency →** abstraction layer + multi-provider fallback.
* **Data access throttling →** offline sync + export/import workflows.
* **Regulatory scope creep →** phase gates; keep compliance surface minimal in v1.

---

## 14) Deliverables Checklist (must include)

* [ ] Filled **Evidence Pack** with citations, adversarial notes, limitations, audit log.
* [ ] **Architecture section** + entity list + security model.
* [ ] **GitHub repo** (monorepo), CI pipeline, issue templates, CODEOWNERS.
* [ ] **Runnable dev stack**: `docker-compose up` brings up db/api/web.
* [ ] **Docs**: README (quickstart), CONTRIBUTING, API reference (OpenAPI), Postman/HTTPie examples.
* [ ] **90-day plan** with owners, dates, and success metrics.

---

## 15) README.md (template content to generate)

```md
# <Product Name>
Problem one-liner → Value prop → ICP

## Quickstart
1) `docker-compose up`  
2) API: http://localhost:8000/healthz  
3) Web: http://localhost:3000

## Tech
- Next.js (web) • FastAPI (api) • Postgres (db) • Docker • GitHub Actions

## Env
Copy `.env.example` → `.env.local` (web) and `.env` (api)

## Contributing
- Branch naming, PR rules, tests, code style.

## Security
- Report vuln: security@yourdomain.com
```

---

## 16) Concrete “Do-This-Now” Commands (copy/paste)

```bash
# Run everything locally
docker-compose up --build

# Open services
open http://localhost:3000
open http://localhost:8000/healthz

# Create feature branch and push
git checkout -b feat/onboarding-checklist
git add .
git commit -m "feat: onboarding checklist + demo data"
git push -u origin feat/onboarding-checklist

# Make a PR
gh pr create --fill --base main
```

---

## 17) Hand-off Artifacts to Produce

* Link to GitHub repo and CI passing badge
* Public demo credentials (demo tenant)
* Evidence Pack PDF with citations
* Product walkthrough video (5–7 minutes)
* Spreadsheet: TAM/SAM/SOM math + sensitivity table

---

**End of prompt.**
When you (the model) generate the plan, ensure every section above is present, all checklists are filled, code compiles, commands run locally with Docker, and sources are credible and unbiased per Section 2C.
