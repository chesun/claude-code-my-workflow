# Workflow Adaptation Plan: Behavioral & Experimental Economics

**Status:** DRAFT — awaiting user feedback
**Date:** 2026-03-17
**Author:** Christina Sun (with Claude)

---

## Part 1: Comparative Analysis — Pedro vs. Hugo

### What Stays the Same (Core Infrastructure)

Both repos share a foundational layer that should be preserved as-is:

| Component | Description | Verdict |
|-----------|-------------|---------|
| **Plan-first workflow** | Enter plan mode → spec → plan → approval → orchestrate | Keep verbatim |
| **Contractor/orchestrator loop** | Implement → Verify → Review → Fix → Re-verify → Score | Keep verbatim |
| **Quality gates** (80/90/95) | Threshold-gated commits/PRs/submission | Keep verbatim |
| **Context survival** | Plans/logs/specs on disk, pre-compact hooks, MEMORY.md | Keep verbatim |
| **Session logging** (3 triggers) | Post-plan, incremental, end-of-session | Keep verbatim |
| **Hooks infrastructure** | pre-compact, post-compact, verify-reminder, context-monitor, protect-files, log-reminder | Keep verbatim |
| **Two-tier memory** | MEMORY.md (generic, committed) + personal-memory.md (local, gitignored) | Keep verbatim |
| **Meta-governance** | Generic vs. specific content separation | Keep verbatim |
| **Git worktree pattern** | Branch isolation for risky work | Keep verbatim |
| **Exploration folder** | `explorations/` sandbox with 60/100 threshold, archive lifecycle | Keep verbatim |
| **`/commit`** | Stage, PR, merge workflow | Keep verbatim |
| **`/learn`** | Extract discovery into reusable skill | Keep verbatim |
| **`/context-status`** | Session health monitoring | Keep verbatim |
| **Templates** | session-log, quality-report, requirements-spec, exploration-readme, skill-template | Keep verbatim |

### What Pedro Has That Hugo Doesn't Need (Lecture-Specific)

These are **lecture slide production** features. Christina likely doesn't need them unless teaching:

| Component | Pedro's Purpose | Keep? |
|-----------|----------------|-------|
| Beamer → Quarto sync | Single source of truth for slides | **Remove** (no lectures) |
| `/compile-latex` (slide version) | 3-pass XeLaTeX for Beamer slides | **Adapt** to paper compilation |
| `/deploy` | Quarto → GitHub Pages | **Remove** unless hosting results |
| `/extract-tikz` | TikZ → SVG for web slides | **Remove** |
| `/translate-to-quarto` | Beamer → Quarto translation | **Remove** |
| `/qa-quarto` | Adversarial Quarto vs Beamer | **Remove** |
| `/slide-excellence` | Multi-agent slide review | **Replace** with paper review |
| `/create-lecture` | Full lecture creation | **Remove** |
| `/pedagogy-review` | 13-pattern teaching check | **Remove** (unless teaching) |
| `/visual-audit` (slide version) | Slide layout audit | **Remove** |
| `no-pause-beamer.md` rule | Ban overlay commands | **Remove** |
| `beamer-quarto-sync.md` rule | Auto-sync slides | **Remove** |
| `tikz-visual-quality.md` rule | TikZ standards | **Remove** |
| slide-auditor agent | Visual layout expert | **Remove** |
| pedagogy-reviewer agent | Teaching quality expert | **Remove** |
| quarto-critic / quarto-fixer agents | Adversarial QA for slides | **Remove** |
| beamer-translator agent | Slide translation | **Remove** |

### What Hugo Adds That Pedro Lacks (Research Paper Production)

Hugo's key innovations, all relevant to Christina's needs:

| Innovation | Description | Relevance |
|------------|-------------|-----------|
| **Worker-critic pairing** | Every creator paired with adversarial critic who can't edit files | **HIGH** — prevents self-review bias |
| **Separation of powers** | Critics score but don't fix; workers fix but don't self-score | **HIGH** — quality enforcement |
| **Three-strikes escalation** | If pair can't converge in 3 rounds → escalate | **HIGH** — prevents infinite loops |
| **Journal-calibrated peer review** | 15 journal profiles, domain + methods referees | **HIGH** — directly useful |
| **Weighted aggregate scoring** | Component weights (lit 10%, identification 25%, etc.) | **MEDIUM** — adapt weights for behavioral/experimental |
| **Severity gradient by phase** | Critics harsher in later phases | **HIGH** — matches research reality |
| **Consolidated commands** (20+ → 10) | Fewer commands, more flags | **HIGH** — better UX |
| **Cross-language replication** | `--dual r,python` | **LOW** — nice but not priority |
| **Anti-hedging enforcement** | Strips AI writing patterns | **HIGH** — essential for papers |
| **Working paper format rule** | Standard econ paper format (12pt, booktabs, etc.) | **HIGH** — adapt for experimental econ |
| **Data-engineer agent** | Raw → cleaned data specialist | **HIGH** — essential for experiments |
| **Storyteller agent** | Paper → talk conversion (4 formats) | **MEDIUM** — useful for job talks, seminars |
| **AEA replication package** | Submission-mode verification | **MEDIUM** — needed at submission time |

### What Pedro Has That Hugo Should Have Kept

Pedro's **Devil's Advocate pattern** (5.8) and **fresh-context critique** are powerful and somewhat underutilized in Hugo's version:

| Pedro Feature | Hugo Equivalent | Gap |
|---------------|----------------|-----|
| `/devils-advocate` skill | Absorbed into critic agents | **Loss of standalone invocability** — you can't just say "challenge this idea" without invoking the full pipeline |
| Fresh-context critique | Worker-critic pairs | **Partial** — critic agents aren't truly fresh context (they share session). Pedro's "spawn new agent with NO access to conversation" is stronger |
| Agent debates (3 agents, each advocating) | Not explicitly preserved | **Loss** — Hugo's referees review, but don't *debate* each other |

---

## Part 2: Adaptation Plan for Behavioral & Experimental Economics

### Your Domain Profile

**Field:** Behavioral and Experimental Economics
**Key activities:**
1. Literature review and synthesis
2. Research idea brainstorming and formalization
3. Theory development and mathematical modeling
4. Experimental design (lab, field, online)
5. Survey development (Qualtrics, oTree)
6. Implementation and data collection
7. Data analysis and coding (R, possibly Python/Stata)

### Proposed Folder Structure

```
christina-workflow/
├── CLAUDE.md                    # Project configuration
├── MEMORY.md                    # Cross-session learning
├── Bibliography_base.bib        # Centralized bibliography
│
├── Paper/                       # Main manuscript (SOURCE OF TRUTH)
│   ├── main.tex
│   └── sections/                # Modular section files
│
├── Experiments/                  # NEW: Experiment-specific materials
│   ├── designs/                 # Pre-registration docs, power analyses
│   ├── protocols/               # IRB protocols, experimenter scripts
│   ├── oTree/                   # oTree experiment code
│   ├── qualtrics/               # Qualtrics survey exports, flow docs
│   └── instructions/            # Participant instructions (LaTeX/PDF)
│
├── Data/
│   ├── raw/                     # Untouched data
│   ├── cleaned/                 # Processed data
│   └── simulated/               # NEW: Simulated/pilot data for power analysis
│
├── Figures/                     # Publication-quality figures
├── Tables/                      # Publication-quality .tex tables
├── Supplementary/               # Online appendix
│
├── Talks/                       # Derivative presentations
│   ├── job_market_talk.tex
│   ├── seminar_talk.tex
│   └── short_talk.tex
│
├── Replication/                 # Replication package
├── scripts/
│   ├── R/                       # Primary analysis language
│   ├── python/                  # oTree backend, text analysis
│   └── stata/                   # If needed for specific estimators
│
├── explorations/                # Research sandbox (60/100 quality)
├── master_supporting_docs/      # Reference papers, existing slides
├── quality_reports/             # Plans, specs, reviews, session logs
│   ├── plans/
│   ├── specs/
│   ├── session_logs/
│   ├── reviews/
│   └── merges/
│
├── .claude/
│   ├── settings.json
│   ├── WORKFLOW_QUICK_REF.md
│   ├── skills/                  # ~15 skills (see below)
│   ├── agents/                  # ~14 agents (see below)
│   ├── rules/                   # ~10 rules (see below)
│   └── hooks/                   # 7 hooks (from Pedro)
│
├── guide/                       # Documentation
├── docs/                        # Generated HTML
├── scripts/                     # Utility scripts
└── templates/                   # Reusable templates
```

### Proposed Skills (15 Commands)

Consolidating Pedro's granularity with Hugo's flag-based UX, plus new experimental economics skills:

#### Research Discovery & Ideation (3)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/discover interview [topic]` | — | Interactive structured interview to formalize research idea (from Pedro's `/interview-me`) |
| `/discover lit [topic]` | `--behavioral`, `--experimental`, `--neuro` | Literature search + synthesis + gap identification |
| `/discover ideate [topic]` | — | Generate 3-5 research questions with hypotheses and strategies |

#### Theory & Design (3) — **NEW**

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/theory [mode]` | `develop`, `review`, `formalize` | Develop theoretical model, review mathematical derivations, or formalize verbal arguments into math |
| `/design [mode]` | `experiment`, `survey`, `power` | Design lab/field/online experiment, develop survey instrument, or run power analysis |
| `/preregister [study]` | `--aea`, `--osf`, `--aspredicted` | Generate pre-registration document from experiment design |

#### Execution (2)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/analyze [dataset]` | `--dual r,python` | End-to-end data analysis (from Hugo, adapted) |
| `/write [section]` | `intro`, `theory`, `design`, `results`, `conclusion`, `abstract`, `full`, `humanize` | Draft paper sections with anti-hedging enforcement |

#### Review (2)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/review [target]` | `--peer [journal]`, `--methods`, `--code`, `--proofread`, `--all` | Journal-calibrated peer review (from Hugo) |
| `/challenge [target]` | `--design`, `--theory`, `--paper`, `--fresh` | **Devil's Advocate** — standalone challenge skill (see detailed design below) |

#### Submission & Presentation (2)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/talk [mode] [format]` | `create`, `audit`, `compile` | Create/audit/compile Beamer talks |
| `/submit [mode]` | `target`, `package`, `audit`, `final` | Target journal, package replication, audit, submit |

#### Infrastructure (3)

| Command | Modes/Flags | What It Does |
|---------|------------|--------------|
| `/commit [msg]` | — | Stage, commit, PR, merge (from Pedro) |
| `/tools [sub]` | `compile`, `validate-bib`, `context-status`, `learn`, `deep-audit` | Utility subcommands |
| `/revise [report]` | — | Address referee comments (from Hugo) |

### Proposed Agents (14)

Adopting Hugo's worker-critic pairing with behavioral/experimental economics specializations:

#### Discovery Phase
1. **librarian** — Literature search specialist (behavioral econ journals: JEEA, EJ, Games & Economic Behavior, JEBO, Experimental Economics, etc.)
2. **librarian-critic** — Evaluates coverage, flags missing seminal references

#### Theory Phase — **NEW**
3. **theorist** — Develops formal models (game theory, decision theory, mechanism design), writes proofs, checks mathematical consistency
4. **theorist-critic** — Checks derivations, assumptions, edge cases; asks "what if players deviate?" and "is this equilibrium unique?"

#### Design Phase — **NEW**
5. **designer** — Creates experiment protocols, randomization schemes, treatment arms, survey instruments, oTree/Qualtrics implementations
6. **designer-critic** — Checks for demand effects, experimenter bias, confounds, attrition, ethical concerns, power adequacy

#### Execution Phase
7. **data-engineer** — Raw → cleaned data, handles experimental data quirks (session IDs, round numbers, role assignments)
8. **coder** — Analysis implementation in R (primary), with experimental econ conventions (clustering by session, permutation tests, etc.)
9. **coder-critic** — Code quality, reproducibility, domain correctness
10. **writer** — Paper drafting with anti-hedging, enforces experimental reporting standards (participant counts, exclusion criteria, etc.)
11. **writer-critic** — Evaluates clarity, structure, APA/journal compliance

#### Review Phase
12. **domain-referee** — Calibrated to behavioral/experimental econ journals
13. **methods-referee** — Focuses on experimental validity, statistical inference, multiple hypothesis testing

#### Infrastructure
14. **verifier** — Compilation, script execution, file integrity, replication package audit

### The `/challenge` Skill — Expanded Devil's Advocate

This is where Pedro's Pattern 8 gets significantly expanded for your domain. The key insight: **the Devil's Advocate pattern should work for research design, not just slide design.**

#### Design

```
/challenge [target] --mode
```

**Modes:**

1. **`--design`** — Challenge an experiment design
   - "What if subjects figure out the hypothesis?"
   - "How do you handle attrition in this between-subjects design?"
   - "Is your control group truly receiving zero treatment?"
   - "What demand effects could drive your results?"
   - "Does your randomization actually achieve balance on X?"
   - "What happens if the effect size is half what you powered for?"
   - "Could a simpler design answer the same question?"

2. **`--theory`** — Challenge a theoretical model
   - "Is this equilibrium unique, or are there others you're ignoring?"
   - "What happens when you relax assumption X?"
   - "Does this model nest the alternative explanation?"
   - "Can you sign the comparative static without functional form?"
   - "Would a behavioral agent (reference-dependent, present-biased) behave differently?"
   - "Is this mechanism observationally distinct from [alternative]?"

3. **`--paper`** — Challenge a paper draft (extends Pedro's original)
   - "What would Referee 2 say about your identification?"
   - "Is your sample representative enough for the claims you make?"
   - "How do you rule out [alternative mechanism]?"
   - "Your confidence intervals are wide — are you underpowered?"
   - "This result contradicts [well-known finding] — address it"
   - "The framing suggests causality but the design only identifies correlation"
   - "Your pre-registration says X but you report Y — explain the deviation"

4. **`--fresh`** — Fresh-context critique (from Pedro's callout box)
   - Spawns a **new agent with NO access to conversation**
   - Gives agent ONLY the artifact + a harsh critique prompt
   - Agent has no sunk cost in the work → ruthless evaluation
   - "Find the 5 weakest points and explain how a hostile referee would attack each"

#### Implementation Detail

```markdown
# /challenge SKILL.md

---
name: challenge
description: >
  Devil's advocate for research. Challenges experiment designs, theoretical models,
  and paper drafts with domain-specific adversarial questions.
  Modes: --design, --theory, --paper, --fresh
argument-hint: "[filename or topic] --mode"
allowed-tools: ["Read", "Grep", "Glob", "Agent"]
---

## Step 1: Determine mode from $ARGUMENTS
- --design → Experiment design challenge
- --theory → Theory/model challenge
- --paper → Paper draft challenge
- --fresh → Spawn fresh-context agent (no conversation access)

## Step 2: Read target artifact
- Read the file or section being challenged
- Read domain-profile.md for field conventions
- Read adjacent files for context (e.g., pre-registration if challenging results)

## Step 3: Generate 5-7 challenges (mode-specific)
[Category-specific questions as above]

## Step 4: For each challenge, provide:
- **The question** (specific, referencing exact claims/sections)
- **Why it matters** (what goes wrong if ignored)
- **How a referee would phrase it** (adversarial framing)
- **Suggested resolution** (concrete fix)
- **Severity** (Critical / Major / Minor)

## Step 5: Summary verdict
- Strengths (2-3)
- Critical changes before proceeding (0-2)
- Suggested improvements (2-3)

## Step 6 (--fresh mode only):
Spawn Agent with subagent_type="general-purpose":
- Give it ONLY the artifact file path
- Give it ONLY the critique prompt (no conversation context)
- Ask for 5 weakest points + hostile referee attacks
```

### Proposed Rules (~10)

#### Always-On (4) — Preserved from Pedro/Hugo
1. **workflow.md** — Plan-first + orchestrator loop + dependency graph
2. **agents.md** — Worker-critic pairing, separation of powers, three-strikes escalation
3. **quality.md** — Weighted scoring, thresholds, severity gradient by phase
4. **logging.md** — Session logs, research journal, merge-time quality reports

#### Path-Scoped (6)

5. **content-standards.md** — Writing, coding, table/figure standards (paths: `**/*.R`, `**/*.tex`, `Tables/**`, `Figures/**`)
6. **experiment-protocol.md** — **NEW** Experimental design standards (paths: `Experiments/**`, `designs/**`)
   - Pre-registration required before data collection
   - Power analysis required before running experiment
   - IRB protocol documented
   - Randomization method specified and reproducible
   - Participant payment and deception policy
   - oTree/Qualtrics coding standards
7. **working-paper-format.md** — Standard econ paper format (paths: `Paper/**/*.tex`)
8. **r-code-conventions.md** — R coding standards for experimental data (paths: `**/*.R`)
   - Cluster SEs by session/group
   - Report permutation p-values for small samples
   - Handle multiple hypothesis testing (Bonferroni, BH, Romano-Wolf)
   - Experimental data conventions (session/round/role structure)
9. **domain-profile.md** — Behavioral & experimental economics profile
10. **journal-profiles.md** — Adapted for behavioral/experimental journals

### Journal Profiles to Add

Beyond Hugo's 15 (which focus on applied/causal econometrics), add:

| Journal | Why |
|---------|-----|
| **Experimental Economics** | Primary experimental outlet |
| **Journal of the European Economic Association (JEEA)** | Strong experimental section |
| **Games and Economic Behavior** | Theory + experiments |
| **Journal of Economic Behavior & Organization (JEBO)** | Behavioral focus |
| **Management Science** | Behavioral/experimental economics at B-schools |
| **Journal of Behavioral and Experimental Economics** | Specialist outlet |
| **American Economic Review** | Already in Hugo's, keep |
| **Quarterly Journal of Economics** | Already in Hugo's, keep |
| **Review of Economic Studies** | Already in Hugo's, keep |
| **AEJ: Microeconomics** | Add to Hugo's list |
| **Journal of Political Economy: Micro** | New outlet, relevant |
| **Econometrica** | For theory-heavy experimental work |

### Weighted Scoring — Adapted for Experimental Economics

Hugo's weights assume observational causal inference is central. For behavioral/experimental economics, rebalance:

| Component | Hugo's Weight | Christina's Weight | Rationale |
|-----------|--------------|-------------------|-----------|
| Literature coverage | 10% | 10% | Same |
| Data quality | 10% | 5% | Experimental data is cleaner by design |
| Identification validity | 25% | 10% | Experiments handle identification by design |
| **Experimental design** | — | **20%** | **NEW**: The experiment IS the identification |
| **Theory/model** | — | **15%** | **NEW**: Behavioral models matter |
| Code quality | 15% | 10% | Same concern, lower weight |
| Paper quality | 25% | 20% | Still important |
| Manuscript polish | 10% | 5% | Less weight |
| Replication readiness | 5% | 5% | Same |

### Domain Profile Template — Behavioral & Experimental Economics

```markdown
# Domain Profile: Behavioral & Experimental Economics

## Field
- Primary: Behavioral Economics, Experimental Economics
- Adjacent: Decision Theory, Game Theory, Psychology & Economics, Neuroeconomics

## Target Journals (by tier)
- Top-5: AER, Econometrica, JPE, QJE, REStud
- Top Field: AEJ:Micro, Experimental Economics, JEEA, Games & Economic Behavior
- Strong Field: JEBO, Management Science, J Behavioral & Experimental Economics
- Specialty: Journal of Risk and Uncertainty, J Economic Psychology

## Common Data Sources
- Lab experiments (zTree, oTree)
- Online experiments (Prolific, MTurk, CloudResearch)
- Field experiments (partner organizations)
- Survey experiments (Qualtrics)
- Administrative data (when available)

## Common Identification Strategies
- Randomized controlled experiments (lab, field, online)
- Within-subject vs. between-subject designs
- Strategy method vs. direct response
- Structural estimation of behavioral models
- Instrumental variables (for field experiments with imperfect compliance)

## Field Conventions
- Report session-level clustering for lab experiments
- Report exact p-values, not stars
- Pre-registration increasingly expected (AEA RCT Registry, OSF)
- Multiple hypothesis testing correction required
- Power analysis expected (ex ante or ex post)
- Deception policy varies by subfield (generally avoided in econ experiments)

## Notation Conventions
- Utility: u(·) or U(·)
- Probability weighting: w(p) or π(p)
- Risk aversion: r or ρ
- Discount factor: δ or β (for present bias: βδ)
- Reference point: r or x*
- Loss aversion: λ
- Treatment indicator: T or D
- Outcome: Y
- Treatment effect: τ or ATE

## Seminal References (cite if relevant)
- Kahneman & Tversky (1979) — Prospect Theory
- Thaler (1980) — Mental Accounting
- Fehr & Schmidt (1999) — Inequality Aversion
- Charness & Rabin (2002) — Social Preferences
- Andreoni (1990) — Warm Glow
- Gneezy & Rustichini (2000) — Pay Enough or Don't Pay at All
- DellaVigna (2009) — Psychology and Economics survey
- Levitt & List (2007) — Field experiments
- Camerer (2003) — Behavioral Game Theory

## Field-Specific Referee Concerns
- "Is this a real phenomenon or a lab artifact?"
- "How do you rule out experimenter demand effects?"
- "Can you distinguish your mechanism from [alternative]?"
- "What about external validity beyond your subject pool?"
- "Were subjects incentivized appropriately?"
- "How do you handle hypothetical bias?" (if survey-based)
- "Did you pre-register? If not, how do we know this isn't p-hacking?"
- "Multiple testing problem — how many comparisons did you run?"

## Quality Tolerance Thresholds
- Treatment effect: exact replication within 0.01 SD
- p-values: within 0.001
- Power calculations: within 1% of simulated power
- Cross-language replication: R vs Stata within 1e-6 for point estimates
```

---

## Part 3: Implementation Roadmap

### Phase 1: Foundation (Day 1)
- [ ] Fork Pedro's repo (or adapt current)
- [ ] Customize CLAUDE.md with project metadata
- [ ] Create folder structure (Paper/, Experiments/, Data/, etc.)
- [ ] Keep all shared infrastructure (hooks, templates, core rules)
- [ ] Remove lecture-specific skills/agents/rules (list above)
- [ ] Create `domain-profile.md` with behavioral econ profile
- [ ] Create `CLAUDE.local.md` for machine-specific settings

### Phase 2: Core Skills (Day 2-3)
- [ ] Adapt Hugo's consolidated command structure (10 → 15 commands)
- [ ] Create `/challenge` skill (expanded Devil's Advocate)
- [ ] Create `/theory` skill (theory development + review)
- [ ] Create `/design` skill (experiment + survey + power analysis)
- [ ] Create `/preregister` skill
- [ ] Adapt `/discover`, `/analyze`, `/write`, `/review` from Hugo
- [ ] Adapt `/talk`, `/submit`, `/revise` from Hugo

### Phase 3: Agents (Day 3-4)
- [ ] Create theorist + theorist-critic pair
- [ ] Create designer + designer-critic pair
- [ ] Adapt Hugo's librarian, data-engineer, coder, writer pairs
- [ ] Adapt domain-referee and methods-referee for behavioral/experimental journals
- [ ] Add journal profiles for experimental economics journals
- [ ] Create verifier with experiment-specific checks

### Phase 4: Rules & Quality (Day 4-5)
- [ ] Create experiment-protocol.md rule
- [ ] Adapt r-code-conventions.md for experimental data
- [ ] Create working-paper-format.md
- [ ] Set up weighted scoring with experimental economics weights
- [ ] Create journal-profiles.md with 12+ journals
- [ ] Create content-standards.md adapted for your conventions

### Phase 5: Testing & Refinement (Day 5+)
- [ ] Run `/deep-audit` to check consistency
- [ ] Test each skill on a real or mock project
- [ ] Iterate on agent prompts based on output quality
- [ ] Build up MEMORY.md with [LEARN] entries
- [ ] Refine domain profile based on actual usage

---

## Part 4: Open Questions for Christina

1. **Teaching component?** Do you also teach courses, or is this purely research? If you teach, we should keep some of Pedro's lecture skills (pedagogy-review, slide-excellence).
   - CS: I don't teach currently but anticipate delivering lectures and seminars occassionally. Keep all latex beamer relevant skills. I do not use quarto so we can get rid of quarto stuff. I used to use xelatex but have mostly switched to pdflatex for beamer just for simplicity. I have a custom beamer template for each of xelatex and pdflatex that we can improve later. I also use tikz in slides so tikz quality control is important.
2. **Primary analysis language?** The plan assumes R primary. Do you also use Stata or Python regularly? This affects coder agent design and cross-language replication setup.
   - CS: my primary is Stata with some python. I am planning to switch over to python gradually. However currently 95% of my codebase is stata. 

3. **oTree expertise level?** Should the `/design` skill include oTree code generation (writing the actual experiment), or just protocol/design documents that you then implement manually?
   - CS: I am an otree beginner, have not developed any experiments in otree yet, been using qualtrics exclusively. There should be a specialized otree skill and a specialized qualtrics skill.

4. **Qualtrics workflow?** Do you design surveys in Qualtrics GUI and export, or do you want Claude to generate Qualtrics survey flow specifications that you import?
   - CS: so far I have been designing in GUI and deploying via links. I want Claude to have advanced capability in both designing qualtrics survey that I can import, and validating and impropving surveys I manually design and export. I heavily use custom CSS/html/javascript code in my qualtrics surveys for GUI customization and interactivity. Think buttons, embedded pictures, RNGs, etc.

5. **Coauthors?** Do you work with coauthors who would use this same repo? If so, the git workflow and permissions model may need adjustment.
   - CS: No.

6. **Theory intensity?** How math-heavy is your typical paper? This determines how sophisticated the theorist agent needs to be (simple utility maximization vs. mechanism design proofs).
   - CS: The model's primary purpose is to clarify thinking about behavioral mechanisms and provide underpinning for experimental design (identifying mechanisms and prove/disprove model by checking testable predictions, or estimating structural parameters). It can get math heavy, and the agent should have very advanced capability with mathematical rigor. Heavy duty proofs may be involved. Currently I have a project that utilizes markov processes with bellman recursion, for example. I may also want to structurally estimate model parameters in future projects.
7. **Pre-registration practice?** Do you currently pre-register all studies? This affects whether `/preregister` is a core or optional skill.
   - CS: I pre-register all studies. Currently using aspredicted mostly, may start using OSF.

8. **Existing papers/projects?** Do you have a current paper or project we should use as a test case for the initial setup? This would help us validate the workflow against real work.
   - CS: Yes. My JMP project and BDM belief elicitation project are both behavioral projects we can test. JMP is mostly finished and BDM is halfway, currently in literature review stage to identify current gaps since I have not worked on the project in a few years.

9. **CS: Domain specific notes**
   - I want to expand seminal papers to include seminal work in most of the subfields of behavioral and experimental economics. 
   - I also want to include key papers in recent developments of behavioral/experimental economics. For example, Danz et al. 2022 for behavioral incentive compatibility (domain of BDM project), work by Oprea and coauthors on complexity, and work by Ferdinand Vieider & Ryan Oprea & others on noisy cognition, e.g. Khaw, Li & Woodford, oprea & Vieider minding the gap.
   - Another important domain specific concern is whether subjects understand the instructions and the tasks. We can ensure subject understanding by using simple and clear instructions, reduce complexity of tasks, and implement understanding and attention checks, or learning phases. 
   - I also want to develop a set of standards for experimental design, and/or a set of key principles of good experimental design. When designing the experiement, we should also be thinking about what inference strategy and tests will be appropriate given the data produced (e.g. KS tests, fisher exact, regression, etc.). Not sure the best way to approach this, give me your suggestions. Bottom line is before we even think about running the experiment, we need to be crystal clear and confident about our identification strategy and inference methods post data collection. This will also help us improve experimental design.
   - The experimental design phase is the most important phase. I want to up the weight to at least 25%
   - During experimental design, we should be thinking about the actual instructions and interface the subject sees, and make all design choices with intention. Same with implementation. Because small deviations in interface, for example, using a slider vs. input box, can result in drastic differences in distribution of data. We also need to be thinking about floor and ceiling effects.
   - Incentive design for subjects is also a key part of experimental design.
   - We also need a way to predict average subject compensation for budgeting reasons.This can be tested using pilots, but we need to start with a reliable ballpark.
   - Additionally, the length of the experiment and the expected time it takes a median subject to complete the experiment is important. We want experiments as short as possible. This relates back to the simplicity principle.
   - I am not planning on running field experiments so we can omit that for now.