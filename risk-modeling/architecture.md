                ┌──────────────────────────┐
                │   Raw Applicant Data     │
                │  (Loan + Transactions)   │
                └────────────┬─────────────┘
                             ↓
                ┌──────────────────────────┐
                │ Data Cleaning & Parsing  │
                │ - Normalize formats      │
                │ - Handle missing values  │
                └────────────┬─────────────┘
                             ↓
                ┌──────────────────────────┐
                │ Feature Engineering      │
                │ - Transaction patterns   │
                │ - Payment behavior       │
                │ - Frequency metrics      │
                └────────────┬─────────────┘
                             ↓
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
┌───────────────┐   ┌──────────────────┐   ┌────────────────────┐
│ Token Risk    │   │ Behavioral Rules │   │ Vector Similarity  │
│ Detection     │   │ Engine           │   │ (Embeddings)       │
│ (keywords)    │   │ (heuristics)     │   │ (pattern matching) │
└──────┬────────┘   └────────┬─────────┘   └─────────┬──────────┘
       └──────────────┬──────┴──────────────┬────────┘
                      ↓                     ↓
              ┌──────────────────────────────────┐
              │      Hybrid Risk Scoring         │
              │ - Weighted signals              │
              │ - Aggregated risk factors       │
              └──────────────┬──────────────────┘
                             ↓
              ┌──────────────────────────────────┐
              │       Decision Engine            │
              │ - Threshold-based decisions      │
              │ - Override logic                │
              └──────────────┬──────────────────┘
                             ↓
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
   ┌──────────┐        ┌──────────┐        ┌──────────┐
   │ Approve  │        │ Review   │        │ Decline  │
   └──────────┘        └──────────┘        └──────────┘
                             ↓
              ┌──────────────────────────────────┐
              │     Explainability Layer         │
              │ - Risk categories               │
              │ - Reason codes                 │
              │ - Decision transparency        │
              └──────────────────────────────────┘
