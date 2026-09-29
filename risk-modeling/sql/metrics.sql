-- DuckDB metrics for synthetic_applicants.csv (demonstration only; not production rules).
--
-- CSV schema (header row):
--   applicant_id                  VARCHAR  synthetic key (e.g. SYN-001)
--   avg_monthly_inflow_usd        DOUBLE   average monthly credits
--   avg_monthly_outflow_usd       DOUBLE   average monthly debits
--   failed_payment_count_90d      INTEGER  returned/failed payment attempts (90d)
--   nsf_event_count_90d           INTEGER  NSF/overdraft events (90d)
--   unique_merchant_count_30d     INTEGER  distinct merchants (30d)
--   high_risk_merchant_hits_90d   INTEGER  matches to illustrative high-risk categories
--   cash_withdrawal_ratio         DOUBLE   cash withdrawals / outflow (0–1)
--   income_volatility_index       DOUBLE   income stability proxy (0–1, higher = more volatile)
--   days_since_last_overdraft     INTEGER  days since last overdraft signal
--   recurring_income_flag         INTEGER  1 if recurring payroll-like income detected
--   narrative_tokens              VARCHAR  pipe-separated behavior tokens for token scoring
--
-- Run from risk-modeling/ (paths relative to that folder), e.g.:
--   duckdb -c ".read sql/metrics.sql"
-- Or use scripts/build_features.py for an exported feature table.

CREATE OR REPLACE VIEW raw_applicants AS
SELECT *
FROM read_csv_auto(
    'data/synthetic_applicants.csv',
    header := true,
    types := {
        'applicant_id': 'VARCHAR',
        'avg_monthly_inflow_usd': 'DOUBLE',
        'avg_monthly_outflow_usd': 'DOUBLE',
        'failed_payment_count_90d': 'INTEGER',
        'nsf_event_count_90d': 'INTEGER',
        'unique_merchant_count_30d': 'INTEGER',
        'high_risk_merchant_hits_90d': 'INTEGER',
        'cash_withdrawal_ratio': 'DOUBLE',
        'income_volatility_index': 'DOUBLE',
        'days_since_last_overdraft': 'INTEGER',
        'recurring_income_flag': 'INTEGER',
        'narrative_tokens': 'VARCHAR'
    }
);

-- Engineered features aligned with rule thresholds in src/score.py (illustrative).
CREATE OR REPLACE VIEW applicant_features AS
SELECT
    applicant_id,
    avg_monthly_inflow_usd,
    avg_monthly_outflow_usd,
    failed_payment_count_90d,
    nsf_event_count_90d,
    unique_merchant_count_30d,
    high_risk_merchant_hits_90d,
    cash_withdrawal_ratio,
    income_volatility_index,
    days_since_last_overdraft,
    recurring_income_flag,
    narrative_tokens,
    avg_monthly_inflow_usd - avg_monthly_outflow_usd AS net_monthly_cashflow_usd,
    CASE
        WHEN avg_monthly_outflow_usd > 0
        THEN avg_monthly_inflow_usd / avg_monthly_outflow_usd
        ELSE NULL
    END AS inflow_to_outflow_ratio,
    failed_payment_count_90d + nsf_event_count_90d AS payment_stress_events_90d,
    CASE WHEN avg_monthly_outflow_usd > 0 AND avg_monthly_inflow_usd < avg_monthly_outflow_usd * 1.1
        THEN 1 ELSE 0 END AS negative_cashflow_flag,
    CASE WHEN failed_payment_count_90d >= 3 THEN 1 ELSE 0 END AS fp_high_flag,
    CASE WHEN nsf_event_count_90d >= 2 THEN 1 ELSE 0 END AS nsf_pattern_flag,
    CASE WHEN high_risk_merchant_hits_90d >= 4 THEN 1 ELSE 0 END AS merchant_risk_flag,
    CASE WHEN cash_withdrawal_ratio > 0.5 THEN 1 ELSE 0 END AS cash_heavy_flag,
    CASE WHEN recurring_income_flag = 0 THEN 1 ELSE 0 END AS low_recurring_income_flag,
    CASE WHEN income_volatility_index > 0.65 THEN 1 ELSE 0 END AS volatile_income_flag,
    CASE WHEN days_since_last_overdraft < 45 THEN 1 ELSE 0 END AS recent_overdraft_flag,
    len(string_split(narrative_tokens, '|')) AS narrative_token_count
FROM raw_applicants;

-- Portfolio rollups for quick QA on synthetic cohorts.
CREATE OR REPLACE VIEW cohort_summary AS
SELECT
    COUNT(*) AS applicant_count,
    ROUND(AVG(net_monthly_cashflow_usd), 2) AS avg_net_cashflow_usd,
    ROUND(AVG(payment_stress_events_90d), 2) AS avg_payment_stress_events,
    SUM(fp_high_flag) AS fp_high_count,
    SUM(nsf_pattern_flag) AS nsf_pattern_count,
    SUM(merchant_risk_flag) AS merchant_risk_count,
    SUM(negative_cashflow_flag) AS negative_cashflow_count
FROM applicant_features;

-- Applicants sorted by payment stress (useful for manual review demos).
-- SELECT * FROM applicant_features ORDER BY payment_stress_events_90d DESC, applicant_id;

-- Default preview when sourcing this file interactively:
SELECT * FROM cohort_summary;
