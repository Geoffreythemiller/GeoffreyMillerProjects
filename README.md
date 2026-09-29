# Geoffrey Miller — Data & Risk Analytics Portfolio

Data Analyst specializing in lending, risk modeling, and financial data systems.

I build end-to-end systems that transform raw transactional data into decision-ready insights, including loan approval models, risk scoring frameworks, and automated reporting pipelines.

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

## Academic Projects

### [Planetoids Game](./school-projects/planetoids)

Asteroids-style game built in Python with:

* Physics-based motion
* Collision detection
* Object-oriented design

---

### Sports Performance Prediction (INFO 2950)

Report + notebook: [PDF](./school-projects/info2950-project/project-report.pdf) · [final_analysis.ipynb](./school-projects/info2950-project/final_analysis.ipynb)

Predictive modeling across NFL, NBA, MLB, and NHL datasets.

* Regression and classification models
* Feature analysis of performance drivers

---

### [College Pathway Analytics](./school-projects/info4100.finalproject.docx)

Statistical modeling in R analyzing course enrollment trends and academic progression.

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

**Coursework / building in portfolio**

* R (INFO 4100 report)
* SQL, DuckDB (planned risk MVP)
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

