# Plan: Universal .gitignore Across Template + Test Repos

**Status:** APPROVED
**Date:** 2026-04-21
**Session log:** `quality_reports/session_logs/2026-04-21_sync-test-repos-and-upstreams.md` (section A.2)

---

## Goal

Establish one canonical universal `.gitignore` at the root of the template repo, propagated through `main` → both workflow branches → both test repos. Covers LaTeX aux, Python venv, local settings, OS/IDE noise, Quarto, and workflow-specific artifacts. Explicit anti-rules protect Python dependency manifests.

## Decisions (locked)

- **D1** — LaTeX `*.log` is scoped to LaTeX folders only (`paper/**/*.log`, `talks/**/*.log`, `slides/**/*.log`, `supplementary/**/*.log`). Bare `*.log` is **not** used, to preserve Stata log files at repo root and in other locations.
- **D2** — `docs/` is dropped from behavioral branch (Hugo guide-site artifact, not used by Christina's projects).
- **D3** — `CLAUDE.local.md` is added to behavioral branch (currently only on main/applied-micro). Universal per-machine notes pattern.
- **D4** — Deploy steps include `git rm --cached` for any now-ignored files that are currently tracked (mirrors TX commit `08ddad0` and BDM commits `ff925cc` / `7f0be14`).

## Canonical Universal `.gitignore` Content

```gitignore
# ==============================================================================
# .gitignore — Academic Claude Code Projects
# ==============================================================================

# --- LaTeX build artifacts (scoped to LaTeX dirs to preserve Stata logs elsewhere) ---
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.lof
*.lot
*.nav
*.out
*.run.xml
*.snm
*.synctex.gz
*.toc
*.vrb
*-blx.bib
paper/**/*.log
talks/**/*.log
slides/**/*.log
supplementary/**/*.log

# --- Python ---
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
venv/
env/
.ipynb_checkpoints/

# Always track dependency manifests (anti-rules — never ignore these)
!requirements.txt
!requirements-*.txt
!environment.yml
!pyproject.toml

# --- R ---
.Rproj.user/
.Rhistory
.RData
.Rdata
.Ruserdata

# --- OS ---
.DS_Store
Thumbs.db

# --- Claude Code (local-only, not shared across machines) ---
.claude/settings.local.json
.claude/state/
.claude/worktrees/
CLAUDE.local.md

# --- IDE / editor noise ---
.vscode/
.idea/
*.swp
*.swo
*~

# --- Quarto ---
/.quarto/

# --- Compiled PDFs (uncomment per project to track specific outputs) ---
# *.pdf

# --- Output artifacts (uncomment per project) ---
# *.rds
# output/**/*.rds
```

### Behavioral branch addition (appended at end)

```gitignore

# --- Behavioral: Qualtrics survey files ---
# Default-ignore so reference/learning QSFs in master_supporting_docs/,
# survey_design/, explorations/, etc. don't leak into the repo.
# Track only actual experiment implementations under experiments/qualtrics/.
*.qsf
!experiments/qualtrics/**/*.qsf
```

**Revision history:**

- **Initial rule (2026-04-21 first pass):** blanket `*.qsf` — treated all QSFs as ignore-by-default.
- **Revised rule (2026-04-21, same day):** default-ignore + allowlist for `experiments/qualtrics/`. User flagged that reference QSFs in `master_supporting_docs/` (learning) should stay ignored, but actual experiment implementations in `experiments/qualtrics/` should be tracked. The behavioral CLAUDE.md already designates `experiments/qualtrics/` as the canonical experiment-code location.

**Why default-ignore + allowlist:** conservative by default. A new learning-material directory added in the future won't accidentally track its `*.qsf` files without an explicit gitignore change. Single canonical location is self-documenting in the rule.

### Applied-micro branch addition

None.

## Execution Order

Each step = one commit. Five commits total across three repos.

### Step 1 — Template `main` branch: canonical universal

**Delta vs current main:**

- Add `.venv/`, `venv/`, `env/`, `.ipynb_checkpoints/`, `*.pyd` to Python block.
- Add anti-rules block for dependency manifests.
- Add `.claude/worktrees/` to Claude-local block.
- Scope LaTeX logs: add `paper/**/*.log`, `talks/**/*.log`, `slides/**/*.log`, `supplementary/**/*.log`; keep bare `*.log` removed (it wasn't on main, good).
- Wait — main currently has bare `*.log` under LaTeX. **Must remove** bare `*.log` from main's LaTeX block.

Working from main's current content (lines confirmed earlier).

Commit message: `chore: canonical universal .gitignore (scoped LaTeX logs, venv, anti-rules for deps)`

### Step 2 — Template `applied-micro` branch: sync to main + drop drift

**Delta vs current applied-micro:**

- Replace full file with main's canonical content.
- Drop the drifted `master_supporting_docs/qualtrics/` line (leftover from behavioral merge).
- No applied-micro-specific additions.

Commit message: `chore: sync .gitignore with main universal standard`

### Step 3 — Template `behavioral` branch: sync to main + behavioral additions

**Delta vs current behavioral:**

- Replace full file with main's canonical content.
- Drop `docs/` (D2 — Hugo guide-site artifact).
- Add `CLAUDE.local.md` to Claude-local block (D3).
- Keep `*.qsf` in behavioral-specific block.
- Drop stray `master_supporting_docs/qualtrics/` if present.

Commit message: `chore: sync .gitignore with main universal standard + qualtrics exports`

### Step 4 — TX repo: deploy from applied-micro

**Delta vs current TX:**

- Replace `.gitignore` with applied-micro's canonical content.
- Check for now-ignored files that are currently tracked (D4): run `git ls-files --cached -i --exclude-standard` to find them; run `git rm --cached` on each.

Commit message: `chore: adopt canonical universal .gitignore from applied-micro template`

### Step 5 — BDM repo: deploy from behavioral

**Delta vs current BDM:**

- Replace `.gitignore` with behavioral's canonical content.
- Run `git ls-files --cached -i --exclude-standard` + `git rm --cached` on newly-ignored tracked files (D4).

Commit message: `chore: adopt canonical universal .gitignore from behavioral template`

## Verification Steps

After each commit:

1. `git status` — working tree clean (aside from the session log).
2. `git ls-files --cached -i --exclude-standard` — empty (no tracked files match ignore patterns).
3. Spot-check: `echo "x" > test.aux && git check-ignore -v test.aux && rm test.aux` — confirms LaTeX pattern matches.
4. Spot-check: touch a dummy `requirements.txt` in a `.venv/`-ignored context and confirm `git check-ignore` does NOT match it (anti-rule works).

## Files That May Need `git rm --cached`

Predicting what's likely tracked but will become ignored. I'll run the `ls-files` check in each repo to confirm before any removals.

- **Template repo:** unlikely any — the template has been careful. Possible: `.DS_Store` in any subfolder if one slipped in.
- **TX repo:** likely `.DS_Store` somewhere (TX did `08ddad0` but new ones may have appeared); possibly IDE files (`.vscode/`), no Quarto/R artifacts expected.
- **BDM repo:** more likely to have ignored-but-tracked files since BDM's current gitignore is sparsest. Possible: `.DS_Store`, `__pycache__/`, `.Rproj.user/`, `.venv/` files, IDE files.

Running the check mechanically avoids guesswork.

## What This Plan Does NOT Include

- Does not propagate `.gitignore` to new projects automatically (would need a change to `/new-project` skill — out of scope for this session).
- Does not touch `Bibliography_base.bib` handling, data-file gitignores (`data/raw/`), or any project-specific patterns — only universal.
- Does not re-examine upstream (Pedro/Hugo) `.gitignore` changes — out of scope (listed under Section D of session log as deferred).

## Rollback

Each step is a single commit on a clean tree. Rollback is `git revert <hash>` for any step, or `git reset --hard HEAD~1` before push.

## Post-Execution

Update session log Section A with item A.2 complete + commit hashes.
