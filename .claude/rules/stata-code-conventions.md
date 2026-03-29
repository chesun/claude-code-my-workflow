# Stata Code Conventions

**Scope:** `**/*.do`, `**/*.doh`
**Stata version:** 17 (no `dtable`, no `frames` — those require v18)

---

## Project Structure

- `main.do` or `doall.do` — master file, runs everything in order
- `settings.do` — global macros for paths, settings, project-wide parameters
- Numbered scripts: `01_clean.do`, `02_analysis.do`, `03_figures.do`
- `.doh` files — do helper files, used with `include` to preserve local macros
- `helpers/` subfolder for reusable `.doh` routines

## Script Header

Every `.do` file starts with:
```stata
* ============================================================
* [Script name] — [Brief description]
* Project: [Project name]
* Author: [Name]
* Date: [YYYY-MM-DD]
* ============================================================
```

## Settings and Paths

- All paths defined in `settings.do` via global macros
- No hardcoded absolute paths in analysis scripts
- Use `$raw`, `$cleaned`, `$figures`, `$tables` globals
- Point Overleaf paths to Dropbox-synced directories

## Packages

Key packages (install via `ssc install` or `net install`):
- **Regression:** reghdfe, ivreghdfe
- **Output:** estout (esttab, eststo, estadd)
- **Figures:** coefplot, palettes, cleanplots, binscatter, binscatter2, cdfplot
- **Data:** egenmore, regsave
- **Experimental:** (as needed) permute, ritest, wyoung, rwolf

## Experimental Data Conventions

- Cluster standard errors at session/group level by default (Moffatt: OLS without clustering has size 0.46)
- Non-parametric tests for between-subject: `ranksum`, `ksmirnov`, `escftest`
- Non-parametric tests for within-subject: `signrank`, `signtest`
- Exact tests: `ttest ... , by() unequal` for t-tests; Fisher exact for small samples
- Multiple hypothesis testing: `wyoung` (Romano-Wolf), `qqvalue` (Benjamini-Hochberg)
- Structural estimation: `ml` for CRRA, `intreg`/`fmm` for heterogeneous agents, `asclogit` for social preferences

## Table Output

- Use `estout`/`esttab` for all regression tables
- Output bare `.tex` tabular (no `\begin{table}`, no `\caption`)
- The paper wraps tables in `threeparttable` with notes
- Use `booktabs` style: `\toprule`, `\midrule`, `\bottomrule` (never `\hline`)
- Standard stars: `* p<0.10, ** p<0.05, *** p<0.01`

## Figure Output

- Export as `.pdf` for paper, `.png` for slides (both when possible)
- Use `graph export` with appropriate dimensions
- Apply `cleanplots` or consistent scheme across all figures
- Label all axes, include units
- Use `palettes` for consistent color schemes

## Code Style

- `set seed` once at top of master file if any stochastic operations
- Comments explain WHY, not WHAT
- Use `tempvar`, `tempname`, `tempfile` for temporary objects
- `capture drop` before generating variables in iterative scripts
- `preserve`/`restore` when making destructive transformations
- `assert` for data integrity checks after merges and reshapes
