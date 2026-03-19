# Stata Code Conventions

**Paths:** `**/*.do`, `**/*.doh`

## Version
- Server may use Stata 18 with older package versions — flag compatibility concerns

## Project Structure
- **Master file:** `mainscript.do` or `main.do` — runs all do files via `do ./do/filename.do`
- **Settings:** `settings.do` — globals for paths, machine-specific via `c(hostname)` branching
- **Helpers:** `.doh` extension — included via `include` (preserves local macros)
- **Naming:** `01_clean.do`, `02_analysis.do`, `03_figures.do` (numbered order)
- **Subdirs:** `clean/`, `share/`, `learn/`, `helpers/`

## Required Packages
reghdfe, estout, coefplot, ivreghdfe, palettes, cleanplots, egenmore, regsave, cdfplot, binscatter, binscatter2

When new package used: save `[LEARN:stata] New package: name — purpose` to MEMORY.md.

## Code Style
- `local` for within-file constants; `global` only in settings.do
- `cap log close _all` and `set more off` at top of master
- `preserve`/`restore` for temporary manipulation; `tempfile` for intermediates
- `set seed` once in main.do (reproducibility)
- `log using` for every analysis do file
- Never overwrite raw data

## Table Export
- `texsave` for manual tables; `esttab`/`estout` for regression tables
- Output to both local folder AND Overleaf directory
- Format: `tostring var, force format(%10.3f) replace`
- Stars: manual `replace coef=coef+"*" if pval<.05` or esttab options

## Figures
- `graph export` with `.pdf` and `.png`
- Color palette in `.doh` file; opacity locals: `opmax`, `ophigh`, `opmed`, `oplow`
- `binscatter`/`binscatter2` for binned scatter plots

## Regression
- `reghdfe` for OLS with high-dimensional FE
- `ivreghdfe` for IV with high-dimensional FE
- `regsave` for saving results to datasets
- Cluster SEs at appropriate level (document why)
