# Workflow Adaptation Plan v2: Behavioral & Experimental Economics

**Status:** DRAFT v2.1 — incorporates all Q&A rounds
**Date:** 2026-03-17
**Author:** Christina Sun (with Claude)
**Test projects:** JMP (mostly finished), BDM belief elicitation (halfway, lit review stage)
**Stata version:** 17 (SE or MP — no `dtable`, no `frames` from v18)
**Stata conventions:** `main.do`/`doall.do` + `settings.do` (global macros for paths) + `.doh` reusable routines

---

## Key Changes from v1

| Aspect | v1 Plan | v2 Plan (Revised) |
|--------|---------|-------------------|
| Analysis language | R primary | **Stata primary (95%), Python secondary, gradual Python transition** |
| LaTeX engine | xelatex | **pdflatex for Beamer** (custom templates for both pdflatex and xelatex) |
| Quarto | Keep some | **Remove entirely** — not used |
| Qualtrics | Mentioned | **Dedicated advanced skill** — import/export, custom CSS/HTML/JS |
| oTree | Mentioned | **Dedicated beginner skill** — code generation, scaffolding |
| Experimental design weight | 20% | **25%** (single most important component) |
| Theory weight | 15% | 15% (kept — math-heavy, Markov/Bellman/structural) |
| Field experiments | Included | **Removed** — lab and online only |
| R code conventions | Included | **Replaced with Stata conventions** |
| Seminal papers | Basic list | **Expanded across subfields + recent developments** |
| Pre-registration | Optional skill | **Core skill** — always pre-register (AsPredicted, OSF) |

---

## Part 1: Revised Architecture

### Folder Structure

```
christina-workflow/
├── CLAUDE.md                    # Project configuration
├── CLAUDE.local.md              # Machine-specific overrides (gitignored)
├── MEMORY.md                    # Cross-session learning
├── Bibliography_base.bib        # Centralized bibliography
│
├── Paper/                       # Main manuscript (SOURCE OF TRUTH)
│   ├── main.tex
│   └── sections/                # Modular section files
│
├── Theory/                      # NEW: Formal models
│   ├── model.tex                # Main model writeup
│   ├── proofs/                  # Detailed proofs (appendix material)
│   └── notes/                   # Working notes, derivations
│
├── Experiments/                  # Experiment materials
│   ├── designs/                 # Design documents, checklists
│   ├── protocols/               # IRB protocols, consent forms
│   ├── instructions/            # Subject instructions (LaTeX → PDF)
│   ├── oTree/                   # oTree project code
│   ├── qualtrics/               # QSF exports, custom JS/CSS, flow docs
│   ├── comprehension/           # Understanding checks, attention checks
│   └── pilots/                  # Pilot data, budget estimates, timing
│
├── Data/
│   ├── raw/                     # Untouched data
│   ├── cleaned/                 # Processed data
│   └── simulated/               # Simulated data for power analysis
│
├── Figures/                     # Publication-quality figures
├── Tables/                      # Publication-quality .tex tables
├── Supplementary/               # Online appendix
│
├── Slides/                      # Beamer presentations (KEPT)
│   ├── job_market_talk.tex
│   ├── seminar_talk.tex
│   └── short_talk.tex
│
├── Preambles/                   # LaTeX headers (KEPT)
│   ├── header_pdflatex.tex      # pdflatex Beamer template
│   └── header_xelatex.tex       # xelatex Beamer template (backup)
│
├── Replication/                 # Replication package
├── scripts/
│   ├── stata/                   # PRIMARY: .do files
│   │   ├── main.do              # Master file (runs everything in order)
│   │   ├── settings.do          # Global macros for paths and settings
│   │   ├── 01_clean.do          # Data cleaning
│   │   ├── 02_analysis.do       # Main analysis
│   │   ├── 03_figures.do        # Figure generation
│   │   └── helpers/             # .doh reusable routines
│   └── python/                  # SECONDARY: .py files (growing)
│
├── explorations/                # Research sandbox (60/100 quality)
├── master_supporting_docs/      # Reference papers
├── quality_reports/             # Plans, specs, reviews, session logs
│
├── .claude/
│   ├── settings.json
│   ├── WORKFLOW_QUICK_REF.md
│   ├── skills/                  # ~17 skills
│   ├── agents/                  # ~16 agents
│   ├── rules/                   # ~12 rules
│   └── hooks/                   # 7 hooks (from Pedro)
│
├── templates/                   # Reusable templates
│   ├── session-log.md
│   ├── quality-report.md
│   ├── requirements-spec.md
│   ├── experiment-design-checklist.md   # NEW
│   ├── pre-registration-template.md     # NEW
│   ├── subject-instructions-template.tex # NEW
│   └── skill-template.md
│
└── guide/                       # Documentation
```

### Proposed Skills (17 Commands)

#### Research Discovery & Ideation (3)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/discover interview [topic]` | — | Interactive structured interview to formalize research idea |
| `/discover lit [topic]` | `--behavioral`, `--experimental`, `--neuro`, `--decision-theory` | Literature search + synthesis + gap identification |
| `/discover ideate [topic]` | — | Generate 3-5 research questions with hypotheses and strategies |

#### Theory & Formal Modeling (2)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/theory develop [topic]` | — | Develop formal model: assumptions → setup → equilibrium → comparative statics → testable predictions |
| `/theory review [file]` | `--proofs`, `--assumptions`, `--predictions` | Review mathematical derivations, check proofs, verify testable predictions follow from model |

**Agent capability:** Must handle utility maximization, game theory (Nash, SPE, PBE), dynamic programming (Bellman), Markov processes, reference-dependent preferences (Kőszegi-Rabin), structural estimation setups, prospect theory calculations, mechanism design. Proofs should be rigorous — verify every step, flag gaps, check boundary conditions.

#### Experimental Design (3) — **CORE PHASE**

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/design experiment [topic]` | `--lab`, `--online` | Full experiment design using inference-first checklist (see below) |
| `/design survey [topic]` | `--qualtrics`, `--otree` | Design survey instrument or experimental interface |
| `/design power [spec]` | `--simulate`, `--analytical` | Power analysis via simulation or analytical formula |

**The Inference-First Design Checklist** (produced by `/design experiment`):

```
1. RESEARCH QUESTION
   What causal/behavioral claim are you testing?

2. THEORETICAL PREDICTIONS
   What does the model predict? List each testable prediction.

3. STATISTICAL TESTS (specify BEFORE designing treatments)
   For each prediction: exact test (KS, Fisher exact, Mann-Whitney,
   permutation, regression with clustering, structural estimation).
   What is the estimand? What is the null?

4. DATA STRUCTURE REQUIRED
   What data do those tests need? (e.g., paired observations,
   independent samples, panel, choice lists, belief distributions)

5. TREATMENT ARMS
   Design treatments that produce the required data structure.
   Justify each arm. What does comparison of arms A vs B identify?

6. INTERFACE & ELICITATION
   For every choice subjects make:
   - Elicitation method (slider vs. input box vs. button vs. list)
   - WHY this method (cite evidence for/against alternatives)
   - Floor/ceiling risk analysis
   - Screen layout mockup

7. INCENTIVE DESIGN
   - Payment structure (flat fee + bonus, or piece rate, or lottery)
   - Incentive compatibility argument
   - Expected average payment calculation
   - Payment range (min/max possible)
   - IRB-compliant payment justification

8. SUBJECT COMPREHENSION
   - Instructions clarity review (reading level, jargon check)
   - Understanding checks (quiz questions with criteria for exclusion)
   - Attention checks (placement and frequency)
   - Practice/learning rounds (if applicable)
   - Feedback during task (if applicable)

9. TIMING & LOGISTICS
   - Expected median completion time
   - Time per screen/task estimate
   - Total experiment length target (shorter = better)
   - Session structure (if lab: how many per session, simultaneous?)

10. POWER ANALYSIS
    - Effect size assumption (justify from theory, pilots, or literature)
    - Sample size calculation
    - Minimum detectable effect given budget constraint

11. BUDGET
    - Per-subject expected payment
    - Platform fees (Prolific, lab overhead)
    - Total budget for target N
    - Budget sensitivity: what if N needs to increase 50%?

12. PRE-REGISTRATION DRAFT
    - Hypotheses
    - Primary and secondary outcomes
    - Exclusion criteria (pre-specified)
    - Analysis plan (exact specifications from step 3)
    - Multiple testing correction method
```

#### Qualtrics (1) — **Dedicated Advanced Skill**

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/qualtrics [mode]` | `create`, `validate`, `improve`, `export-js` | Create importable QSF, validate exported QSF, improve existing survey, generate custom JS/CSS |

**Capabilities:**
- **create**: Generate complete QSF (JSON) importable into Qualtrics — question blocks, flow logic, embedded data, display logic, randomization, custom CSS/HTML/JS
- **validate**: Read exported QSF, check for: skip logic errors, missing display conditions, broken JS, inaccessible branches, randomization balance, timing issues
- **improve**: Suggest improvements to existing survey — question wording, response scales, layout, comprehension, accessibility
- **export-js**: Generate standalone JS snippets for: custom buttons, embedded images, RNG-driven randomization, dynamic content, slider customization, input validation, progress bars, conditional display
- Understands Qualtrics-specific: embedded data fields, piped text, survey flow branching, quotas, web service calls, end-of-survey redirects

#### oTree (1) — **Dedicated Beginner-Friendly Skill**

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/otree [mode]` | `create`, `review`, `explain` | Generate oTree app code, review existing oTree code, explain oTree concepts |

**Capabilities:**
- **create**: Generate complete oTree app from experiment design document — `__init__.py`, templates, pages, models, custom JS
- **review**: Check oTree code for bugs, best practices, session configuration issues
- **explain**: Explain oTree concepts (pages, groups, subsessions, participant fields, live pages, custom data export)
- Scaffolds from design document → working oTree code
- Handles: real-effort tasks, belief elicitation, public goods, dictator, ultimatum, auctions, matching protocols
- Generates appropriate `settings.py` configuration

#### Execution (2)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/analyze [dataset]` | `--dual stata,python` | End-to-end data analysis (Stata primary, Python secondary) |
| `/write [section]` | `intro`, `theory`, `design`, `results`, `conclusion`, `abstract`, `full`, `humanize` | Draft paper sections with anti-hedging enforcement |

#### Review (2)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/review [target]` | `--peer [journal]`, `--methods`, `--code`, `--proofread`, `--all` | Journal-calibrated peer review |
| `/challenge [target]` | `--design`, `--theory`, `--paper`, `--fresh` | Devil's Advocate (see detailed design in v1, unchanged) |

#### Pre-Registration (1) — **Core Skill**

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/preregister [study]` | `--aspredicted`, `--osf` | Generate pre-registration from experiment design checklist |

**Capabilities:**
- Reads completed design checklist → produces pre-registration in target format
- AsPredicted: 9-question format (hypothesis, DV, conditions, analyses, sample size, other, exclusions, secondary, instruction)
- OSF: Full pre-registration with analysis plan, study design, sampling plan, variables, analysis plan
- Flags any design checklist gaps that must be resolved before registering
- Cross-checks: does the pre-registered analysis match the design checklist step 3?

#### Submission & Presentation (2)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/talk [mode]` | `create`, `audit`, `compile` | Create/audit/compile Beamer talks (pdflatex, with TikZ) |
| `/submit [mode]` | `target`, `package`, `audit`, `final` | Target journal, package replication, audit, submit |

#### Infrastructure (3)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/commit [msg]` | — | Stage, commit, PR, merge |
| `/tools [sub]` | `compile-latex`, `validate-bib`, `context-status`, `learn`, `deep-audit` | Utility subcommands |
| `/revise [report]` | — | Address referee comments |

### Proposed Agents (16)

#### Discovery Phase
1. **librarian** — Literature search (behavioral/experimental econ journals + top-5 + psychology)
2. **librarian-critic** — Coverage evaluation, missing seminal references, recency check

#### Theory Phase
3. **theorist** — Formal model development
   - Game theory: Nash, SPE, PBE, mechanism design
   - Decision theory: EU, prospect theory, reference-dependent preferences (Kőszegi-Rabin)
   - Dynamic: Bellman recursion, Markov processes, optimal stopping
   - Behavioral: present bias (βδ), loss aversion, probability weighting, limited attention
   - Structural: set up estimation (MLE, MSM, indirect inference)
   - Output: Model document with assumptions, propositions, proofs, testable predictions
4. **theorist-critic** — Proof verification, assumption stress-testing
   - Checks every derivation step
   - Tests boundary conditions and edge cases
   - Asks: "Is equilibrium unique?", "What if you relax assumption X?", "Does this nest [alternative]?"
   - Verifies testable predictions actually follow from the model
   - Checks notation consistency across paper

#### Experimental Design Phase (HIGHEST WEIGHT)
5. **designer** — Experiment design specialist
   - Produces inference-first design checklist
   - Interface/elicitation method expertise (slider effects, order effects, anchoring)
   - Incentive compatibility analysis
   - Power analysis (simulation-based and analytical)
   - Budget and timing estimates
   - Subject comprehension checks
   - Knows: BDM, MPL, strategy method, direct elicitation, belief elicitation (Schotter & Trevino), allocation tasks
6. **designer-critic** — Adversarial design review
   - Demand effects: "Could subjects guess the hypothesis?"
   - Confounds: "Treatment A differs from B in TWO ways, not one"
   - Comprehension: "Would a median MTurk worker understand this?"
   - Interface effects: "A slider here introduces centering bias"
   - Floor/ceiling: "Your DV is bounded — what if everyone hits the cap?"
   - Incentive issues: "Is this actually incentive-compatible? (cite Danz et al. 2022 if relevant)"
   - External validity: "Your lab sample is undergrads — does this matter for your claim?"
   - Multiple testing: "You have 6 treatment arms — what's your correction plan?"
   - Ethics: "This deception may not pass IRB at some institutions"

#### Implementation Phase
7. **qualtrics-specialist** — Qualtrics survey implementation
   - QSF generation, custom JS/CSS/HTML, survey flow, embedded data
   - Validation of exported surveys
   - Knows: piped text, display logic, quotas, randomizers, web services, end-of-survey redirects
8. **otree-specialist** — oTree experiment implementation
   - App scaffolding, pages, models, templates, live pages
   - Session configuration, group matching, role assignment
   - Custom JS for interactive elements

#### Execution Phase
9. **data-engineer** — Raw → cleaned experimental data
   - Session/round/role structure for lab data
   - Attention/comprehension check filtering
   - Exclusion criteria application (pre-registered)
   - Merge across experiment phases
10. **coder** — Analysis implementation (Stata primary, Python secondary)
    - Experimental data conventions: cluster by session, permutation tests for small samples
    - Non-parametric tests (KS, Mann-Whitney, Fisher exact, Wilcoxon)
    - Regression with appropriate clustering and controls
    - Structural estimation (MLE, MSM)
    - Multiple hypothesis testing corrections (Bonferroni, BH, Romano-Wolf)
    - Publication-quality output (estout/esttab for Stata, matplotlib/seaborn for Python)
11. **coder-critic** — Code quality and reproducibility
12. **writer** — Paper drafting with experimental reporting standards
    - Subject pool description (N, demographics, recruitment, payment)
    - Exclusion criteria and counts
    - Treatment descriptions with exact instructions shown to subjects
    - Anti-hedging enforcement
13. **writer-critic** — Clarity, structure, journal compliance

#### Review Phase
14. **domain-referee** — Calibrated to behavioral/experimental econ journals
15. **methods-referee** — Experimental validity, inference, design critique

#### Infrastructure
16. **verifier** — Compilation (pdflatex), script execution, replication package audit

### Revised Scoring Weights

| Component | Weight | Scored By | Rationale |
|-----------|--------|-----------|-----------|
| Literature coverage | 8% | librarian-critic | Important but not the bottleneck |
| Theory/model quality | 15% | theorist-critic | Math must be rigorous, predictions must be testable |
| **Experimental design** | **25%** | **designer-critic** | **The experiment IS the paper. Bad design = bad paper.** |
| Implementation quality | 7% | qualtrics/otree specialist review | Survey/code must work correctly |
| Code quality | 10% | coder-critic | Reproducibility matters |
| Paper quality | 20% | domain-referee + methods-referee (avg) | Clarity and argumentation |
| Manuscript polish | 10% | writer-critic | Professional presentation |
| Replication readiness | 5% | verifier | AEA compliance |
| **Total** | **100%** | | |

**Per-component minimum for submission:** 80 on every component (no "great paper, broken design").

**Severity gradient** (inherited from Hugo):

| Phase | Critic Stance | Example |
|-------|--------------|---------|
| Discovery/Ideation | Encouraging | Missing citation: -2 |
| Theory development | Constructive | Assumption gap: -5 |
| Experimental design | **Strict** | Missing power analysis: -15 |
| Implementation | Strict | QSF validation error: -10 |
| Execution/Analysis | Strict | Wrong clustering: -10 |
| Peer Review | **Adversarial** | Design confound: -20 |

### Proposed Rules (~12)

#### Always-On (4) — Core Infrastructure
1. **workflow.md** — Plan-first + orchestrator loop + dependency graph
2. **agents.md** — Worker-critic pairing, separation of powers, three-strikes escalation
3. **quality.md** — Weighted scoring (above), thresholds, severity gradient
4. **logging.md** — Session logs, research journal, merge-time quality reports

#### Path-Scoped (8)

5. **experiment-design-principles.md** (paths: `Experiments/**`, `designs/**`)
   The "constitution" for experiments. Non-negotiable principles:
   - **Inference-first**: Specify statistical tests before designing treatments
   - **Subject comprehension**: Instructions must be clear; understanding checks required
   - **Interface intentionality**: Every elicitation choice documented with justification
   - **Simplicity**: Shortest experiment that answers the question
   - **Incentive compatibility**: Payment structure must align incentives; cite theoretical basis
   - **Floor/ceiling awareness**: Analyze bounded variables for compression risk
   - **Pre-registration mandatory**: No data collection without registered hypotheses + analysis plan
   - **Budget realism**: Expected payment × N × platform fee calculated before launch
   - **Pilot first**: Run pilot (N=20-30) before full launch for timing, comprehension, budget calibration

6. **content-standards.md** (paths: `**/*.do`, `**/*.py`, `**/*.tex`, `Tables/**`, `Figures/**`)
   - Writing standards, table/figure formatting
   - Experimental reporting standards (N, demographics, exclusions, instructions)
   - Anti-hedging enforcement

7. **stata-code-conventions.md** (paths: `**/*.do`, `**/*.doh`)
   - **Stata 17** — do not use v18+ features (`dtable`, `frames`)
   - Master file: `main.do` or `doall.do` runs everything
   - `settings.do`: global macros for all file paths and project settings (sourced by main.do)
   - `.doh` files: reusable routines, ad hoc settings, helper programs (sourced via `do` or `include`)
   - Header block: author, date, purpose, input/output files
   - `set seed` once in main.do or settings.do
   - `log using` for every analysis .do file
   - Relative paths via globals defined in `settings.do` (e.g., `global raw "$root/Data/raw"`)
   - `eststo` / `esttab` for table export (LaTeX format)
   - Cluster SEs by session for lab data
   - Comment conventions: section dividers, variable labels
   - Version control: never overwrite raw data
   - `graph export` with `.pdf` and `.png`
   - Naming: `01_clean.do`, `02_analysis.do`, `03_figures.do` (numbered for execution order)
   - Claude should read existing `settings.do` and `.doh` files in project repos to learn Christina's exact patterns

8. **python-code-conventions.md** (paths: `**/*.py`)
   - Type hints encouraged (gradual adoption)
   - `requirements.txt` or `pyproject.toml` for dependencies
   - Jupyter notebooks for exploration only — production code in `.py`
   - `random.seed()` / `np.random.seed()` set once
   - Figures: matplotlib/seaborn with consistent style

9. **working-paper-format.md** (paths: `Paper/**/*.tex`)
   - Standard econ working paper: 12pt, 1in margins, double-spaced
   - `booktabs` tables, `threeparttable` for notes
   - `aer` bibliography style
   - JEL codes and keywords required
   - **pdflatex** compilation (not xelatex)

10. **domain-profile.md** — Behavioral & experimental economics (see expanded version below)

11. **journal-profiles.md** — 15+ journals (see expanded list below)

12. **tikz-visual-quality.md** (paths: `**/*.tex`)
    - TikZ diagram standards for slides
    - Label positioning, overlap prevention
    - Consistent styling across figures
    - Color accessibility

### Expanded Domain Profile

```markdown
# Domain Profile: Behavioral & Experimental Economics

## Field
- Primary: Behavioral Economics, Experimental Economics
- Adjacent: Decision Theory, Game Theory, Psychology & Economics,
  Neuroeconomics, Bounded Rationality, Market Design

## Target Journals (by tier)
- Top-5: AER, Econometrica, JPE, QJE, REStud
- Top Field: AEJ:Micro, Experimental Economics, JEEA,
  Games & Economic Behavior, Management Science
- Strong Field: JEBO, J Behavioral & Experimental Economics,
  J Risk and Uncertainty, J Economic Psychology
- Specialty: Judgment & Decision Making, Cognitive Psychology

## Common Data Sources
- Lab experiments (oTree, zTree)
- Online experiments (Prolific, CloudResearch)
- Survey experiments (Qualtrics)
- Administrative data (when complementary)

## Common Identification Strategies
- Randomized controlled experiments (lab, online)
- Within-subject vs. between-subject designs
- Strategy method vs. direct response
- Structural estimation of behavioral parameters
- Belief elicitation (BDM, quadratic scoring rule, matching probabilities)

## Field Conventions
- Report session-level clustering for lab experiments
- Report exact p-values (not just stars)
- Pre-registration required (AsPredicted, OSF)
- Multiple hypothesis testing correction required
- Power analysis expected
- No deception (standard in econ experiments; if used, must justify)
- Incentive compatibility argument required for all elicitation methods
- Report exclusion criteria and counts
- Report median completion time and payment

## Notation Conventions
- Utility: u(·) or U(·)
- Probability weighting: w(p) or π(p)
- Risk aversion coefficient: r or ρ
- CRRA utility: u(x) = x^(1-r)/(1-r)
- Discount factor: δ; present bias: β (quasi-hyperbolic: βδ^t)
- Reference point: r or x*
- Loss aversion: λ
- Treatment indicator: T or D
- Outcome: Y
- Treatment effect: τ or ATE
- Belief: μ or b
- Signal: s
- Type: θ
- Value function (PT): v(x) with v(x) = x^α for gains, -λ(-x)^β for losses
- Strategy: σ
- Payoff: π
- Nash equilibrium: NE; Subgame perfect: SPE; Perfect Bayesian: PBE
- Bellman equation: V(s) = max_a {u(s,a) + δ E[V(s')|s,a]}

## Seminal References — Core Behavioral Economics
- Kahneman & Tversky (1979) — Prospect Theory
- Tversky & Kahneman (1992) — Cumulative Prospect Theory
- Thaler (1980, 1985) — Mental Accounting
- Thaler & Sunstein (2008) — Nudge
- Rabin (2000) — Risk Aversion in the Small
- Kőszegi & Rabin (2006, 2007) — Reference-Dependent Preferences
- O'Donoghue & Rabin (1999) — Present Bias
- Laibson (1997) — Golden Eggs (hyperbolic discounting)

## Seminal References — Social Preferences & Cooperation
- Fehr & Schmidt (1999) — Inequality Aversion
- Bolton & Ockenfels (2000) — ERC
- Charness & Rabin (2002) — Social Preferences
- Andreoni (1990) — Warm Glow
- Rabin (1993) — Fairness in Games
- Fehr & Gächter (2000) — Punishment and Cooperation
- Dana, Weber & Kuang (2007) — Moral Wiggle Room

## Seminal References — Experimental Methods
- Smith (1976, 1982) — Induced Value Theory, Experimental Economics Methods
- Gneezy & Rustichini (2000) — Pay Enough or Don't Pay at All
- Levitt & List (2007) — Lab vs Field
- Camerer (2003) — Behavioral Game Theory
- Kagel & Roth (1995, 2016) — Handbook of Experimental Economics
- Schotter & Trevino (2014) — Belief Elicitation Survey
- Charness, Gneezy & Kuhn (2012) — Experimental Methods Survey

## Seminal References — Decision Theory & Cognition
- Holt & Laury (2002) — Risk Elicitation
- Echenique & Saito (2015) — Savage in the Market
- Machina (1982) — Expected Utility without Independence
- Gilboa & Schmeidler (1989) — Maxmin Expected Utility

## Recent Key References — Behavioral/Experimental Frontiers
- Danz, Vesterlund & Wilson (2022) — Behavioral Incentive Compatibility (BDM domain)
- Oprea (2022, 2024) — Complexity and Decision Making
- Vieider & Oprea — Minding the Gap (noisy cognition)
- Khaw, Li & Woodford (2021) — Cognitive Imprecision
- Enke & Graeber (2023) — Cognitive Uncertainty
- Ambuehl, Bernheim & Lusardi (2022) — Complexity and Financial Decisions
- Agranov & Ortoleva (2017, 2023) — Stochastic Choice
- Frydman & Nave (2024) — Neuroscience of Economic Choice

## Seminal References — Belief Elicitation
- Becker, DeGroot & Marschak (1964) — BDM Mechanism
- Offerman et al. (2009) — Proper Scoring Rules
- Hossain & Okui (2013) — Incentivized Belief Elicitation
- Schlag, Tremewan & van der Weele (2015) — Penny for Thoughts

## Field-Specific Referee Concerns
- "Is this a real phenomenon or a lab artifact?"
- "How do you rule out experimenter demand effects?"
- "Can you distinguish your mechanism from [alternative]?"
- "What about external validity beyond your subject pool?"
- "Were subjects incentivized appropriately?"
- "Is your elicitation method incentive-compatible? (cite Danz et al. if BDM)"
- "Did you pre-register? Deviations from pre-registration?"
- "Multiple testing — how many comparisons?"
- "Could noisy cognition explain your results? (cite Khaw-Li-Woodford, Oprea)"
- "Do subjects understand the task? (comprehension check results)"
- "Your interface choice (slider/input box/list) may drive the result"
- "Sample size — are you adequately powered?"
- "What's your structural model? Can you estimate parameters?"
- "Would these results replicate on a different platform/population?"

## Quality Tolerance Thresholds
- Treatment effect replication: within 0.01 SD
- p-values: within 0.001
- Power calculations: within 1% of simulated power
- Cross-language replication (Stata vs Python): within 1e-6 for point estimates
- Structural parameter estimates: within 1e-4
```

### LaTeX Compilation — Revised for pdflatex

```bash
# Beamer slides (3-pass, pdflatex)
cd Slides && TEXINPUTS=../Preambles:$TEXINPUTS pdflatex -interaction=nonstopmode file.tex
BIBINPUTS=..:$BIBINPUTS bibtex file
TEXINPUTS=../Preambles:$TEXINPUTS pdflatex -interaction=nonstopmode file.tex
TEXINPUTS=../Preambles:$TEXINPUTS pdflatex -interaction=nonstopmode file.tex

# Paper (3-pass, pdflatex)
cd Paper && pdflatex -interaction=nonstopmode main.tex
BIBINPUTS=..:$BIBINPUTS bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

---

## Part 2: The `/challenge` Skill — Expanded Devil's Advocate

Unchanged from v1 plan, with one addition for experimental economics:

### Mode: `--design` (Experiment Design Challenge)

This is the **most important** `/challenge` mode. Specific questions it generates:

**Identification & Inference:**
- "You say Treatment A tests mechanism X — but it also changes Y. How do you isolate X?"
- "Your statistical test assumes independence, but subjects interact in the lab. What's your clustering strategy?"
- "You powered for a 0.3 SD effect — what if the true effect is 0.15?"

**Subject Experience:**
- "Walk me through exactly what a subject sees, screen by screen. Where do they get confused?"
- "You're using a slider for belief elicitation — centering bias will contaminate your data. Why not an input box?"
- "Your instructions mention 'other participants' decisions' — this introduces social desirability bias"
- "A median subject takes 25 minutes on your pilot. The 90th percentile takes 55 minutes. Your slowest subjects are your most confused — is that a problem for your results?"

**Incentive Compatibility:**
- "Is your BDM implementation actually incentive compatible? (What does Danz et al. 2022 say about this?)"
- "Subjects earn $0.50 for a 'correct' belief but $12 show-up fee — are beliefs even incentivized?"
- "Your payment is capped at $20 — subjects near the cap have no marginal incentive"

**Alternative Designs:**
- "What if you used within-subject instead of between-subject? What do you gain/lose?"
- "Could a strategy method elicit the same information with fewer subjects?"
- "Have you considered a 2×2 factorial? It would let you test for interaction effects"

---

## Part 3: Revised Implementation Roadmap

### Phase 1: Foundation (Day 1)
- [ ] Customize CLAUDE.md with project metadata
- [ ] Create folder structure (Paper/, Theory/, Experiments/, Data/, Slides/, scripts/stata/)
- [ ] Keep all shared infrastructure (hooks, templates, core rules)
- [ ] **Remove** all Quarto-related skills/agents/rules
- [ ] **Remove** all Quarto-related scripts (sync_to_docs.sh, etc.)
- [ ] Create `domain-profile.md` with expanded behavioral econ profile
- [ ] Create `CLAUDE.local.md` for machine-specific paths
- [ ] Update compilation commands to pdflatex

### Phase 2: Core Rules (Day 2)
- [ ] Create `experiment-design-principles.md` (the experiment "constitution")
- [ ] Create `stata-code-conventions.md`
- [ ] Create `python-code-conventions.md`
- [ ] Adapt `working-paper-format.md` for pdflatex
- [ ] Create `journal-profiles.md` with 15+ behavioral/experimental journals
- [ ] Create `content-standards.md` with experimental reporting standards
- [ ] Keep `tikz-visual-quality.md` for slides

### Phase 3: Core Skills (Day 3-4)
- [ ] Create `/theory` skill (develop + review modes)
- [ ] Create `/design` skill with inference-first checklist
- [ ] Create `/qualtrics` skill (create, validate, improve, export-js)
- [ ] Create `/otree` skill (create, review, explain)
- [ ] Create `/preregister` skill (AsPredicted + OSF)
- [ ] Create `/challenge` skill (--design, --theory, --paper, --fresh)
- [ ] Adapt `/discover`, `/analyze`, `/write`, `/review` from Hugo
- [ ] Adapt `/talk` for pdflatex Beamer
- [ ] Adapt `/submit`, `/revise`, `/commit`, `/tools`
- [ ] Create `templates/experiment-design-checklist.md`
- [ ] Create `templates/pre-registration-template.md`

### Phase 4: Agents (Day 4-5)
- [ ] Create theorist + theorist-critic pair
- [ ] Create designer + designer-critic pair
- [ ] Create qualtrics-specialist agent
- [ ] Create otree-specialist agent
- [ ] Adapt librarian pair for behavioral/experimental econ
- [ ] Adapt coder pair for Stata primary + Python secondary
- [ ] Adapt data-engineer for experimental data structure
- [ ] Adapt writer pair for experimental reporting standards
- [ ] Adapt domain-referee and methods-referee
- [ ] Create verifier with pdflatex + Stata checks

### Phase 5: Testing with BDM Project (Day 5+)
- [ ] Test `/discover lit` on BDM belief elicitation literature
- [ ] Test `/theory review` on existing BDM model (if any)
- [ ] Test `/design experiment` on BDM experimental design
- [ ] Test `/challenge --design` on BDM experiment
- [ ] Test `/qualtrics validate` on existing BDM Qualtrics survey
- [ ] Test `/preregister` on BDM study
- [ ] Run `/deep-audit` to check consistency
- [ ] Iterate agent prompts based on output quality
- [ ] Build up MEMORY.md with [LEARN] entries

---

## Part 4: Dependency Graph — Research Pipeline

```
/discover interview ─────┐
                         ├──→ /discover lit ──→ /theory develop
/discover ideate ────────┘         │                    │
                                   │                    ▼
                                   │            /theory review
                                   │                    │
                                   ▼                    ▼
                          /design experiment ←── testable predictions
                                   │
                          ┌────────┼────────┐
                          ▼        ▼        ▼
                  /design power  /qualtrics  /otree
                          │        │        │
                          ▼        ▼        ▼
                     /preregister (gates data collection)
                               │
                               ▼
                          COLLECT DATA
                               │
                          ┌────┴────┐
                          ▼         ▼
                     /analyze    /write
                          │         │
                          ▼         ▼
                     /review --peer [journal]
                               │
                          ┌────┴────┐
                          ▼         ▼
                     /revise     /talk
                          │
                          ▼
                     /submit
```

**Key insight:** `/preregister` is a **gate** — no data collection without it. Theory produces testable predictions that feed directly into experiment design. The design checklist's step 3 (statistical tests) feeds directly into the pre-registration analysis plan and eventually into `/analyze`.

**Mid-pipeline entry points:**
- Have data already? → Start at `/analyze`
- Have a draft? → Start at `/review`
- Have a design but no theory? → Start at `/design`, flag that theory is missing
- Have theory but no design? → Start at `/theory review`, then `/design`

---

## Part 5: Christina's To-Dos (Before Implementation Begins)

These items require Christina's input before Claude can proceed with implementation.

### Must-Do (Blocks Implementation)

- [ ] **Provide test project repo paths** — Point Claude to JMP and/or BDM repos so Claude can read existing `main.do`, `settings.do`, `.doh` patterns and learn actual Stata conventions
   - CS: JMP project repo: /Users/christinasun/github_repos/belief_distortion_discrimination
      - Caveat: currently the JMP setup is a little scattered. the above is the main repo, but I also set up smaller separate repos for specific functions: /Users/christinasun/github_repos/endogenous_info for text classification and machine learning of some open response questions, and /Users/christinasun/github_repos/jmp_sample_behavior for sampling behavior (stopping rule models)
      - additional caveat: currently all my paper drafts are separately hosted on overleaf because I like the interface. I want you to think about how to take this into account in my workflow. For example, do we sync repo paper changes to overleaf? Sync overleaf changes back? Work locally and polish on overleaf? Give me your suggestions. The overleaf paper/slides directory is /Users/christinasun/Library/CloudStorage/Dropbox/Apps/Overleaf/belief_distortion_discrimination
- [ ] **Provide seminal papers list** — Christina curates her core list; Claude proposes additions organized by subfield (categories below). This populates the domain-profile.md reference section.
  - Proposed subfield categories:
    1. Prospect Theory & Reference Dependence
    2. Social Preferences & Cooperation
    3. Time Preferences & Present Bias
    4. Belief Formation & Updating
    5. Discrimination
    7. Complexity & Noisy Cognition
    8. Attention & Limited Cognition
      - Rational Inattention
    9. Experimental Methods & Design
      - Risk Elicitation & Measurement
      - Belief Elicitation Methods
    10. Nudges & Choice Architecture
    11. Structural Behavioral Estimation
    12. Market/Auction Experiments
   - CS: Edited subfields and moved some to be subsumed by a broader topic (e.g. belief elicitation belongs under experimental methods). Review and propose edits. I want you to first gather seminal papers in each field once we settle on the subfields, then give them for me to approve. I will then add what you didn't find. Search my mendeley library and other online research databases like AEA, SSRN, Google Scholar, etc. 
- [ ] **Confirm or adjust subfield categories** — Are the 13 above the right breakdown? Any to add/remove/merge?
   - CS: see above
- [ ] **Decide repo structure for projects** — Do JMP and BDM live in separate repos, or inside this workflow repo (e.g., under `explorations/` or as top-level project folders)?
   - Separate repos. See previous for location of JMP repos.
   - BDM repo: /Users/christinasun/github_repos/bdm_bic
      - overleaf dir for BDM paper and slides: '/Users/christinasun/Library/CloudStorage/Dropbox/Apps/Overleaf/BDM Incentive and Truth Telling'

### Should-Do (Improves Quality, Not Blocking)

- [ ] **Export a QSF from an existing Qualtrics survey** — So Claude can study the structure and build the `/qualtrics` skill against a real example
- [ ] **Share custom Beamer templates** — The pdflatex and xelatex templates, so Claude can write the compilation rule correctly and understand your slide conventions
- [ ] **Provide a sample `.doh` file** — So Claude understands your reusable routine pattern (if not visible in test repos)
- [ ] **List any Stata packages you regularly use** — (`reghdfe`, `estout`, `coefplot`, `randtreat`, etc.) — affects coder agent and Stata conventions rule
- [ ] **Clarify Stata license type** — SE vs MP vs BE? (Affects parallelization advice and matrix size limits)

### Nice-to-Have (Can Do Later)

- [ ] **Review and refine journal profiles** — After initial setup, test `/review --peer [journal]` and adjust journal profiles based on quality of simulated reviews
- [ ] **Identify additional referee concerns** — As you use `/challenge`, add new domain-specific adversarial questions that come up in real reviews
- [ ] **Customize notation conventions** — The current list is generic behavioral econ; adjust symbols to match your specific notation preferences across papers

---

## Part 6: Open Questions (Awaiting Answers — Round 3)

1. **Test project repos** — Which repo(s) should Claude read for your Stata conventions? (paths or GitHub URLs)
   - CS: see part 5
2. **Seminal papers subfield categories** — Are the 13 proposed categories above right? Anything to add/remove?
   - CS: see part 5
3. **`.doh` convention** — Is `.doh` your convention for "do-file header" / reusable include files? (Confirming so the Stata rule documents it correctly)
   - CS: it is a do helper file. use your stata skill to check documentation, if you cannot find it, check statalist. I use `include` command with .doh files because it preserves local macros defined in the doh file.
4. **JMP and BDM repo structure** — Separate repos, or inside this workflow repo?
   - CS: See part 5.

## CS: Additional Notes

- Retain the nice to have items and should do items and anything else I did not address and create a running to do list for me.