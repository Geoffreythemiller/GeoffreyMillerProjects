# Geoffrey Miller — Data & Risk Analytics Portfolio

Data Analyst specializing in lending, risk modeling, and financial data systems.

I build end-to-end systems that transform raw transactional data into decision-ready insights, including loan approval models, risk scoring frameworks, and automated reporting pipelines.

---

## Projects at a glance

| Area | Folder | What to run / view |
|------|--------|-------------------|
| **Risk CLI** (synthetic lending demo) | [`risk-modeling/`](./risk-modeling) | `cd risk-modeling && pip install -r requirements.txt && python -m src --input data/synthetic_applicants.csv` |
| **Planetoids** (CS 1110 game) | [`school-projects/planetoids/`](./school-projects/planetoids) | `cd school-projects/planetoids && pip install -r requirements.txt && python __main__.py` |
| **College pathway analytics** (INFO 4100) | [`school-projects/info4100-project/`](./school-projects/info4100-project) | Open [report (Word)](./school-projects/info4100-project/info4100.finalproject.docx) · [analysis outline](./school-projects/info4100-project/sample_outputs/analysis-outline.md) |
| **School projects (index)** | [`school-projects/`](./school-projects) | INFO 2950, CS 1300, and other coursework READMEs |

---

## Core Focus

* Risk Modeling — Loan decisioning, transaction risk scoring, default prediction
* Data Engineering — Scalable pipelines for large financial datasets
* Analytics — Origination, conversion, and performance analysis

---

## Featured Projects

### [Risk Modeling Systems](./risk-modeling)

**Status:** Reference architecture + **runnable synthetic CLI** (rules, tokens, reason codes).

A hybrid risk evaluation framework combining:

* Token-based scoring
* Behavioral rule engines
* Vector similarity (embeddings) — optional v2; v1 CLI runs without embeddings

**Try it (synthetic data):**

```bash
cd risk-modeling && pip install -r requirements.txt && python -m src --input data/synthetic_applicants.csv
```

Key features:

* Explainable risk scoring with reason codes
* Decision engine (Approve / Review / Decline)
* [architecture.md](./risk-modeling/architecture.md) + batch CLI on `data/synthetic_applicants.csv`

---

### [Planetoids](./school-projects/planetoids)

**Status:** Complete CS 1110 game — **runnable locally** (Python 3 + Kivy).

Asteroids-style arcade game with physics-based motion, collision detection, and object-oriented entity design (`models.py`, `app.py`).

**Try it:**

```bash
cd school-projects/planetoids && pip install -r requirements.txt && python __main__.py
```

Key features:

* Custom **game2d** / Kivy game loop and sprites
* Wave-based levels (`Data/*.json`) and sound assets
* [README](./school-projects/planetoids/README.md) with layout, stack, and in-repo sprite preview

---

### [College Pathway Analytics](./school-projects/info4100-project)

**Status:** Complete INFO 4100 learning-analytics project — **R statistical models + written report**.

Statistical analysis of course enrollment trends and academic progression patterns (de-identified academic aggregates).

**View it:**

1. [info4100.finalproject.docx](./school-projects/info4100-project/info4100.finalproject.docx) — full methods, figures, and interpretation  
2. [sample_outputs/analysis-outline.md](./school-projects/info4100-project/sample_outputs/analysis-outline.md) — workflow map before opening the report

Key features:

* Cohort-style enrollment and pathway questions
* R-based modeling and visualization (coursework scope)
* [README](./school-projects/info4100-project/README.md) with stack and data disclaimer

---

## Academic Projects

### Sports Performance Prediction (INFO 2950)

**Status:** Complete coursework — **report + notebook**; [README with synthetic preview figures](./school-projects/info2950-project/README.md).

Predictive modeling across NFL, NBA, MLB, and NHL public sports statistics (OLS persistence + bootstrap league comparisons).

* Multi-league aggregation and EDA in Jupyter
* Linear regression on first- vs second-half win rates
* Bootstrap tests for cross-league mean differences

---

### [Bus Site Redesign](./school-projects/cs1300-final-project)

Responsive web interface focused on:

* usability
* accessibility
* improved navigation

---

## Tech Stack

**Demonstrated in this repo**

* Python, Jupyter (INFO 2950), pandas/NumPy
* Regression and classification (INFO 2950), feature engineering and EDA
* HTML, CSS, JavaScript (CS 1300 bus site)
* Kivy + OOP game design (Planetoids)
* R statistical reporting (INFO 4100 learning analytics)

**Coursework / building in portfolio**

* SQL, DuckDB (`risk-modeling/sql/metrics.sql`, optional `scripts/build_features.py`)
* scikit-learn (INFO 2950); synthetic risk CLI in `risk-modeling/` (stdlib scoring + pytest)
* Pipeline and query optimization patterns (target for risk showcase)

---

## What I'm Building Toward

* Scalable loan decisioning systems
* Explainable AI for financial risk
* End-to-end data pipelines (ingestion → modeling → reporting)

---

## Contact

* Email: [geoffreythemiller@gmail.com](mailto:geoffreythemiller@gmail.com)
* LinkedIn: https://www.linkedin.com/in/geoff-miller-150536251
