# Changelog

All notable changes to the Clo-Author are documented here.

---

## [3.1.0] — 2026-03-23

### Skill Detail Restoration — v1.0 Depth Returns to v3.0

The v2.0→v3.0 consolidation accidentally stripped practical detail from 6 skills. This release restores all 22 lost items while keeping the v3.0 structure.

**`/discover`:**
- Restored proximity scoring (1-5 scale) for literature papers
- Restored citation chains as explicit search vector (forward + backward)
- Restored feasibility grades (A/B/C/D) for datasets
- Restored data rejection table format
- Restored 5-point explorer-critic data critique (measurement validity, sample selection, external validity, identification compatibility, known issues)
- Restored `% UNVERIFIED` citation marking convention

**`/strategize`:**
- Restored interactive PAP interview (6-question guided flow)
- Restored platform-specific PAP templates (AEA RCT Registry, OSF, EGAP)
- Restored observational study PAP adaptation protocol
- Restored optional strategist-critic review after PAP creation
- Restored `[ASSUMED]` placeholder safety flags with pre-registration checklist

**`/analyze`:**
- Restored R script skeleton template (6-section structure)
- Restored `results_summary.md` as mandatory artifact (handoff to writer)
- Restored full 12-category code review checklist (explicit categories 1-12)
- Restored saveRDS serialization guidance
- Restored Scott Cunningham replication tolerance thresholds for `--dual` mode

**`/review`:**
- Restored 4-phase econometrics protocol (claim → validity → inference → polish)
- Restored early stopping rule (CRITICAL Phase 2 issues → focus there)
- Restored severity calibration examples (9 examples with Major/Minor ratings)
- Restored Verifier pass/fail definition (paper, code, replication package)
- Restored "design-opinionated, package-flexible" principle

**`/write`:**
- Restored 7-item context gathering checklist
- Restored quality self-check before presenting (7 items)
- Restored TBD/VERIFY/PLACEHOLDER flagging system
- Restored LaTeX conventions (`\citet` vs `\citep`, booktabs, notation protocol)

**`/talk`:**
- Restored "figures over tables; tables in backup" design principle
- Restored 5-category review detail with full descriptions
- Restored audience calibration principle

### Referee Pet Peeves Expansion
- **27 critical pet peeves** (was 12) — added Oster bounds, leave-one-out, power obsession, balance tables, ML variable selection, first-stage F, Bonferroni, and more
- **24 constructive pet peeves** (was 12) — added event study appreciation, null result honesty, institutional detail, code availability, brevity rewards, contradictory findings engagement, and more
- More variety = less predictable referees = more realistic simulation

---

## [3.0.0] — 2026-03-20

### Scope Expansion: Empirical Social Science
- clo-author now targets all empirical social science fields: economics, finance, marketing, management, accounting, public policy
- Updated meta-governance to reflect this scope (no longer claims biology/physics/CS generality)
- Institution updated from Emory to UAB

### Peer Review Simulation — Complete Redesign
- **New `editor` agent** — desk reviews papers before sending to referees, verifies novelty claims via WebSearch, selects referee dispositions based on journal culture, makes independent editorial decisions (not score averaging)
- **Referee dispositions** — 6 intellectual priors (Structuralist, Credibility, Measurement, Policy, Theory, Skeptic) assigned by the editor based on journal culture
- **Referee pet peeves** — each referee gets 1 critical and 1 constructive pet peeve, creating realistic variation across reviews
- **Journal-driven referee selection** — new `Referee pool` field in journal profiles weights which dispositions the editor draws from (e.g., Econometrica skews Structuralist/Theory, QJE skews Credibility/Policy)
- **"What would change my mind"** — every major referee comment must include specific evidence or analysis that would resolve the concern
- **Desk reject** — editor can reject without sending to referees (wrong fit, no contribution, already published)
- **FATAL/ADDRESSABLE/TASTE classification** — editorial decisions classify each concern, producing MUST/SHOULD/MAY action items
- **R&R memory** — `--r2` flag reloads prior referee reports; referees check whether each concern was addressed (Resolved/Partially/Not addressed)
- **Round escalation** — Round 2 allows Major Revisions if new issues surface; Round 3 is Accept/Minor/Reject only; max 3 rounds
- **Hostile stress test** — `--stress [journal]` assigns adversarial dispositions, doubles critical pet peeves, pre-submission battle testing
- **Literature verification** — editor uses WebSearch during desk review to verify novelty claims against published work

### Journal Profiles Expansion
- Added 15 new A* journal profiles across 4 fields:
  - **Finance:** JF, JFE, RFS, JFQA
  - **Accounting:** JAR, JAE, TAR, CAR
  - **Marketing:** JMR, Marketing Science, JCR
  - **Management:** Management Science, SMJ, ASQ
- All profiles include `Referee pool` disposition weights calibrated to each journal's review culture
- Journal profiles moved from rules to `.claude/references/` — loaded on demand, zero per-session overhead

### Context Reduction: 66% Less Per-Session Overhead
- **Before:** ~3,518 lines of rules loaded every session
- **After:** ~1,198 lines loaded per session
- Deleted `archive/` directory (22 duplicate rule files, ~1,769 lines)
- Trimmed `meta-governance.md` from 252 to 20 lines
- Moved `journal-profiles.md` to on-demand reference (299 lines saved per session)
- Merged `tables.md` and `figures.md` into path-scoped `content-standards.md`

### Content Standards Improvements
- Added figure standards: PDF vector output, colorblind-friendly palettes, grayscale independence (shape + linetype redundancy), figure width guidance
- Restored `threeparttable` requirement for tables (lost in prior merge)
- Consolidated all content rules in one path-scoped file
- Added 5 table type templates: descriptive statistics, regression results, multi-outcome panels, balance tables, robustness

### Folder Structure Reorganization
- Figures, tables, talks, and Quarto presentations now live inside `Paper/` (self-contained paper directory)
- Added `Data/raw/` and `Data/cleaned/` directories
- Deleted `Slides/` (legacy from lecture workflow)
- Quarto RevealJS presentation support added (`/talk create [format] --quarto`)

### Other Changes
- Replaced `[LEARN]` tags with Claude Code's built-in auto-memory system
- Added `[YOUR FIELD]` placeholder to CLAUDE.md and starter prompt
- Agent prompts made field-neutral — read field from `.claude/references/domain-profile.md` (defaults to economics)
- Deleted archived agents (16 files) and archived skills (20+ files)
- Guide and documentation fully updated for v3.0

---

## [2.0.3] — 2026-03-07

### Working Paper Format Rule

- **`working-paper-format.md`** — new always-on rule: enforces standard economics working paper format (12pt article, 1in margins, double-spaced body, single-spaced abstract, `titling` package for proper title/author font sizes, `\quad` author spacing, `booktabs` tables, `threeparttable` notes, `aer` bibliography style)
- Writer-critic deduction rubric included (e.g., -5 for wrong document class, -3 for `\textbf{}` on title, -5 for missing JEL codes)
- Ensures title page fits on one page: title + authors + abstract + JEL + keywords

---

## [2.0.2] — 2026-03-07

### Figures & Tables Rules

- **`figures.md`** — new always-on rule: no embedded ggplot titles, descriptive filenames, LaTeX `\caption{}` as authoritative title, serif fonts, publication-quality axis labels, show all years on x-axis (≤20 ticks)
- **`tables.md`** — new always-on rule: no embedded titles in generated `.tex` files, `threeparttable` + `booktabs`, notes in paper not R output
- These complement `content-standards.md` (path-scoped, comprehensive) with concise always-on reminders

---

## [2.0.1] — 2026-03-05

### Cross-Language Replication

- **`/analyze --dual r,python`** — run the same analysis in two languages in parallel, compare results within tolerance
- **`/review --replicate python`** — re-implement existing code in a different language, compare outputs
- Both use `domain-profile.md` Quality Tolerance Thresholds for pass/fail
- Coder agent updated with cross-language replication mode and common divergence sources
- Inspired by Scott Cunningham's approach to cross-language validation

---

## [2.0.0] — 2026-03-05

**The Great Restructure.** 16-agent worker-critic system, journal-calibrated referees, consolidated rules, 6-page guide with command reference dictionary.

### Architecture

- **16 specialized agents** in 7 worker-critic pairs + 2 blind referees + orchestrator + verifier
- **New agents:** data-engineer, coder-critic, writer-critic, strategist-critic, librarian-critic, explorer-critic, storyteller-critic, domain-referee, methods-referee
- **Retired agents:** Debugger, Proofreader, Econometrician, Editor, Surveyor, Discussant, Referee (replaced by specialized critic/referee counterparts)
- Worker-critic separation of powers: critics never edit files, creators never self-score

### Journal-Calibrated Peer Review

- `/review --peer JHR` makes referees emulate that journal's review culture
- 15 pre-populated journal profiles (Top-5 + top field + strong field)
- 3-tier fallback: pre-populated → unknown journal + domain profile → user-added custom
- Custom template at bottom of `journal-profiles.md` for adding your own journals

### Skills Consolidation

- **10 slash commands** (down from 20+), each with flags/modes instead of separate skills
- `/discover` replaces `/lit-review`, `/find-data`, `/research-ideation`, `/interview-me`
- `/review` replaces `/review-paper`, `/review-r`, `/econometrics-check`, `/proofread`, `/visual-audit`
- `/write` replaces `/draft-paper`, `/humanizer`
- `/talk` replaces `/create-talk`, `/compile-latex` (for talks)
- `/submit` replaces `/target-journal`, `/data-deposit`, `/audit-replication`, `/deploy`
- `/tools` replaces `/commit`, `/compile-latex`, `/validate-bib`, `/journal`, `/context-status`, `/learn`
- `/revise` replaces `/respond-to-referee`
- `/strategize` replaces `/identify`, `/pre-analysis-plan`
- `/analyze` replaces `/data-analysis`

### Rules Consolidation

- 18 single-topic rule files → 5 consolidated files:
  - `agents.md` — pairing, separation of powers, escalation
  - `workflow.md` — planning, orchestration, dependencies, standalone access
  - `quality.md` — scoring, thresholds, severity gradient
  - `logging.md` — sessions, reports, research journal
  - `content-standards.md` — writing, coding, formatting
- Old rule files archived to `.claude/rules/archive/`
- New: `journal-profiles.md` — 15 economics journal review profiles

### Guide Website

- **6 pages** (up from 3): Quick Start, User Guide, Agents, Architecture, Customization, Reference
- New **Command Reference** page: every command, flag, and subcommand in one scannable page
- New **Meet the Agents** page: all 16 agents with roles, what they create/check
- New **Customization Guide**: domain profile, journal profiles, rules, skills, agents, hooks
- Pipeline diagram with backward arrows (Peer Review → Discovery/Strategy/Execution)
- Cyberpunk neon theme throughout all Mermaid diagrams

### Other

- Pipeline diagram shows 3 feedback loops from Peer Review (missing lit, flawed ID, more checks)
- Archived old skills, agents, hooks, and rules (preserved in `archive/` directories)
- Updated README.md with 16-agent table and 10-command reference

---

## [1.0.1] — 2026-02-25–26

### Adversarial Architecture

- Worker-critic pairing: every creator has a paired reviewer
- Separation of powers: critics can't edit, creators can't self-score
- Three-strikes escalation protocol
- Dependency-driven orchestration (phases activate by dependency, not sequence)
- Cyberpunk neon theme for guide website
- 3-page Quarto website: Quick Start, User Guide, Architecture
- Reoriented from lecture production to applied econometrics research

---

## [1.0.0] — 2026-02-08–15

### Research Workflow

- Research skills: `/lit-review`, `/find-data`, `/identify`, `/draft-paper`, `/review-paper`
- Smart hooks: pre-compact context survival, post-session logging
- Skill creation template and two-tier memory system (MEMORY.md + personal)
- Meta-governance: dual nature of repo (working project + public template)
- Requirements specification phase with MUST/SHOULD/MAY framework
- Constitutional governance template

### Infrastructure

- Orchestrator/contractor protocol with dependency graph
- Plan-first workflow with context preservation
- Quality gates: 80 (commit), 90 (PR), 95 (submission)
- Figure and table generator rules (AER/QJE/Econometrica standards)
- Claude Pilot features integration

---

## [0.1.0] — 2026-02-06–07

### Initial Release

- Forked from [Pedro Sant'Anna's claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)
- Plan-first workflow, context preservation, session logging
- Contractor/orchestrator protocol
- Hooks, MEMORY.md, responsive guide
- Parallel agents pattern, `/commit` skill
- Fork-first onboarding flow

---

[2.0.2]: https://github.com/hugosantanna/clo-author/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/hugosantanna/clo-author/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/hugosantanna/clo-author/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/hugosantanna/clo-author/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/hugosantanna/clo-author/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/hugosantanna/clo-author/commits/v0.1.0
