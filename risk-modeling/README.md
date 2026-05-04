# Risk Modeling Systems

This folder contains a generalized portfolio project focused on financial risk modeling, loan decisioning, and transaction-level risk analysis.

This project is based on common data analytics patterns used in lending and financial services. All examples are sanitized, generalized, and use synthetic data only.

---

## Project Goal

Build an explainable risk-scoring framework that evaluates borrower behavior using structured loan data and transaction-level signals.

The system is designed to help identify:

- Higher-risk applicants
- Risky transaction patterns
- Early repayment/default risk indicators
- Cases that should be approved, reviewed, or declined

---

## System Overview

The model combines three approaches:

1. **Rule-Based Risk Flags**
   - Detects specific financial behavior categories
   - Examples: gambling, debt relief, payday lending, excessive failed payments

2. **Token-Based Scoring**
   - Assigns weighted scores to transaction descriptions and behavioral signals
   - Produces an interpretable risk score

3. **Vector Similarity Scoring**
   - Uses embeddings to compare transaction descriptions against known risky behavior categories
   - Helps detect similar terms even when exact keywords are not present

---

## Example Decision Flow

1. Ingest applicant and transaction data  
2. Clean and standardize descriptions  
3. Detect risky tokens and categories  
4. Calculate risk scores  
5. Apply business rules and override logic  
6. Output a decision recommendation:

- Approve
- Review
- Decline

---

## Example Output

| Applicant ID | Risk Score | Main Risk Category | Recommendation |
|---|---:|---|---|
| A001 | 22 | Low Risk | Approve |
| A002 | 68 | Debt / Failed Payments | Review |
| A003 | 91 | Gambling / High-Risk Activity | Decline |

---

## Explainability

Each score includes a reason code so the output is interpretable.

Example:

| Risk Factor | Explanation |
|---|---|
| Gambling Activity | Transaction descriptions matched betting-related behavior |
| Failed Payments | Multiple rejected or returned payment attempts |
| Debt Services | Detected activity related to debt relief or loan stacking |

---

## Architecture

```text
Raw Data
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Risk Token Detection
   ↓
Vector Similarity Scoring
   ↓
Hybrid Risk Score
   ↓
Decision Recommendation
   ↓
Explainability Output
