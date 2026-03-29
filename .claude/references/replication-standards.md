# Replication Standards for Experimental Economics

Based on AEA Data Editor requirements and Coffman & Dreber (2025).

---

## What Must Be Included

### 1. Data
- **Cleaned de-identified data:** Analysis-ready datasets with PII stripped (no Prolific IDs, MTurk worker IDs, IP addresses). Clean data without PII can typically be shared.
- **Raw data:** Do NOT include raw platform exports — they contain confidential information. The cleaning code documents the transformation from raw to clean.
- **Codebook:** Variable definitions, coding, units for all included datasets

### 2. Code
- **Cleaning code:** Transforms raw → cleaned (every step documented)
- **Analysis code:** Produces every number, table, and figure in the paper
- **Master script:** `main.do` or equivalent that runs everything in order
- **Package dependencies:** List with versions (`requirements.txt`, package install commands)

### 3. Experimental Materials
- **Instructions:** Full text shown to subjects (PDF or LaTeX source)
- **Screenshots:** Key decision screens
- **QSF file:** Qualtrics survey export (if applicable)
- **oTree code:** Full oTree project (if applicable)
- **IRB approval:** Protocol number and approval letter

### 4. Documentation
- **README:** Written with "computational empathy" (Vilhuber) — assume a stranger needs to understand
  - What software and versions are needed
  - How to run the code (step by step)
  - Expected runtime
  - What outputs are produced and where
  - Map from code outputs → paper tables/figures
- **Codebook:** Variable definitions, coding, units

---

## Code Quality Standards

- Extensive comments explaining WHY, not just WHAT
- No hardcoded absolute paths
- Relative paths from project root
- `set seed` for any stochastic operations
- Code runs end-to-end without manual intervention
- Output matches paper exactly (within floating-point tolerance)

---

## Pre-Registration Cross-Check

The replication package must be consistent with the pre-registration:
- All pre-registered analyses must appear in the paper (main text or appendix)
- Deviations from pre-registration must be explicitly noted and justified
- Exploratory analyses must be labeled as such

---

## Journal Requirements (as of 2024)

All top economics journals require data and code deposits. Key specifics:

| Journal | Deposit Location | Special Requirements |
|---------|-----------------|---------------------|
| AER family | AEA Data & Code Repository (openICPSR) | Automated reproducibility checks |
| Econometrica | Econometric Society repository | Supplementary materials separate |
| QJE, JPE, REStud | Journal-specific repositories | Check current guidelines |
| Experimental Economics | SpringerNature repository | Experimental materials required |
