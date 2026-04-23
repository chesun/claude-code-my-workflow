# Claude Code Research Workflow

> **Work in progress.** A fork-and-adapt foundation for AI-assisted empirical research — identification, analysis, manuscript, talks, peer review, and submission. Based on Pedro Sant'Anna's [claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) and Hugo Sant'Anna's clo-author template, re-targeted from lecture/slide production to research-paper production.

**Last Updated:** 2026-04-23

You describe what you want — an identification strategy, a data analysis, a paper draft, a replication package, a conference talk — and Claude plans the approach, runs specialized agents, fixes issues, verifies quality, and presents results. Like a contractor who handles the job end-to-end.

---

## Three branches, three surfaces

- **`main` (universal).** Paradigm-agnostic research template. 17 agents, 14 skills, ~18 rules. Everything a general empirical project needs: discovery, data engineering, analysis, writing, peer review, submission.
- **`applied-micro`** (overlay). Adds identification-strategy tooling for observational/administrative-data research: `strategist` + `strategist-critic` agents, `/strategize`, `/balance`, `/event-study` skills, `air-gapped-workflow` rule.
- **`behavioral`** (overlay). Adds experimental-economics and formal-theory tooling: `theorist`, `designer`, `otree-specialist`, `qualtrics-specialist` agents, `/theory`, `/design`, `/otree`, `/qualtrics`, `/preregister` skills, `experiment-design-principles` rule, experiments/theory folder trees.

Main is the trunk. The two overlays are thin diffs maintained on their own branches. Universal improvements land on main and flow to both overlays via rebase.

---

## Quick Start (5 minutes)

### 1. Fork & Clone

```bash
# Fork this repo on GitHub (click "Fork" on the repo page), then:
git clone https://github.com/YOUR_USERNAME/claude-code-my-workflow.git my-project
cd my-project
```

### 2. Pick your branch

Stay on `main` for general empirical work, or:

```bash
git checkout applied-micro      # identification-strategy research
git checkout behavioral         # experimental/theoretical research
```

### 3. Start Claude Code and adapt

```bash
claude
```

Paste a starter prompt like:

> I am starting work on **[PROJECT NAME]**. **[2–3 sentences on the project.]** Read `CLAUDE.md`, fill in my project name and institution, and enter plan mode to adapt the template for my project.

Claude reads the config, adapts placeholders, and enters contractor mode — planning, implementing, reviewing, verifying.

---

## How It Works

### Contractor Mode

You approve a plan. Claude takes over: implements, runs critics, fixes issues, re-verifies, and reports quality scores. The orchestrator manages the dependency graph: Discovery → Strategy/Design → Code → Writing → Peer Review → Submission, with parallel dispatch where phases are independent.

### Specialized Agents (worker + critic pairs)

Every creator has a paired critic. Critics never edit files — they score and report. Worker-critic pairs converge in at most 3 rounds before escalating.

- `librarian` + `librarian-critic` — literature coverage and gaps
- `explorer` + `explorer-critic` — data feasibility and fit
- `data-engineer` + `coder-critic` — data pipeline quality
- `coder` + `coder-critic` — analysis code (Stata / R / Python)
- `writer` + `writer-critic` — manuscript drafting and polish
- `storyteller` + `storyteller-critic` — talks (narrative + visual quality)
- `tikz-reviewer` — merciless TikZ diagram audit
- `domain-referee` + `methods-referee` — simulated peer review
- `editor` — synthesizes referee reports into an editorial decision
- `orchestrator` — dispatches agents, manages escalation, tracks scores
- `verifier` — LaTeX compile, script execution, AEA replication audit

Overlays add: `strategist` (applied), `designer`/`theorist`/`otree-specialist`/`qualtrics-specialist` (behavioral).

### Quality Gates

Weighted aggregate score across components (literature, data, identification/design, code, paper, polish, replication). Thresholds:

- **80** — commit gate
- **90** — PR gate
- **95** — submission gate (plus every component ≥ 80)

See `.claude/rules/quality.md` for the full rubric and per-target deduction tables.

### Primary-Source-First (hook-enforced)

Load-bearing files (decisions, analysis memos, session logs, plans, reviews) cannot cite a paper unless reading notes for that paper exist in `master_supporting_docs/literature/reading_notes/` AND were opened in the current session. The `primary-source-check` PreToolUse hook and `primary-source-audit` Stop hook enforce this deterministically. Escape hatch: `<!-- primary-source-ok: stem -->` in the delta.

### Decision Log (ADRs)

Substantive decisions live in `decisions/NNNN_slug.md` — append-only, immutable once Decided, supersession via new ADRs. Analysis docs hold reasoning; ADRs hold the record.

### Context Survival

Pre-compact hook saves state to disk. Session logs capture incremental progress. ADRs preserve decisions. A new session can pick up from `CLAUDE.md` + most recent plan + `git log` and know where it is.

---

## What's Included

### Agents (`.claude/agents/` — 17 universal)

Creators: librarian, explorer, data-engineer, coder, writer, storyteller
Critics: librarian-critic, explorer-critic, coder-critic, writer-critic, storyteller-critic, tikz-reviewer
Peer review: domain-referee, methods-referee, editor
Infrastructure: orchestrator, verifier

Overlays add their own paradigm-specific agents.

### Skills (`.claude/skills/` — 14 universal)

Pipeline: `/new-project`, `/discover`, `/analyze`, `/write`, `/review`, `/revise`, `/talk`, `/submit`
Utilities: `/commit`, `/context-status`, `/learn`, `/challenge`, `/deep-audit`, `/tools`

`/tools` is a multi-subcommand router (compile, validate-bib, journal, deploy, learn, upgrade).

### Rules (`.claude/rules/`)

- **Workflow:** agents, workflow, quality, logging, revision
- **Writing:** working-paper-format, figures, tables, tikz-visual-quality, single-source-of-truth, replication-protocol, verification-protocol
- **Code:** stata-code-conventions, r-code-conventions, python-code-conventions
- **Discipline:** primary-source-first, decision-log, todo-tracking, output-length, meta-governance
- **Sandbox:** exploration-folder-protocol, exploration-fast-track

### Hooks (`.claude/hooks/`)

- `primary-source-check` (PreToolUse) + `primary-source-audit` (Stop) — citation-grounding enforcement
- `log-reminder` (Stop) — hard-cap reminder to write session logs
- `verify-reminder` (PostToolUse) — prompts verification after edits
- `context-monitor`, `pre-compact`, `post-compact-restore` — context survival
- `protect-files` (PreToolUse) — guard against accidental writes to sensitive files

---

## Prerequisites

- **Claude Code CLI** (see [anthropic.com/claude/code](https://www.anthropic.com/claude/code))
- **LaTeX distribution** (MacTeX, TeX Live, MiKTeX) with `pdflatex` + `biber`
- **Primary analysis language** (Stata 17, R ≥ 4.0, or Python ≥ 3.10)
- **Ghostscript** (optional — for PDF chunking fallback; see `.claude/references/pdf-chunking.md`)

Optional per overlay:

- `applied-micro`: Stata packages `reghdfe`, `ivreghdfe`, `estout`, `did_multiplegt`, `csdid` (as relevant)
- `behavioral`: oTree 5.x/6.x, Qualtrics account, R for `did`/`fixest`/power simulations

---

## Adapting for Your Field

1. Edit `CLAUDE.md` — project name, institution, language, LaTeX engine.
2. Populate `.claude/state/primary_source_surnames.txt` with authors you cite frequently (reduces false positives from the primary-source hook).
3. Drop relevant reference material into `master_supporting_docs/` (field-specific style guides, journal notes).
4. If your field is well-served by an overlay, check out the overlay branch. Otherwise keep `main` and customize as needed.

---

## Origin & Credits

- Foundation: Pedro Sant'Anna, [`pedrohcgs/claude-code-my-workflow`](https://github.com/pedrohcgs/claude-code-my-workflow) — originally a lecture/slide production template.
- Research-adaptation base: Hugo Sant'Anna, [`hugosantanna/clo-author`](https://github.com/hugosantanna/clo-author).
- This fork: reoriented to research-paper production with paradigm-specific overlays for applied micro and behavioral/experimental economics.

---

## License

MIT (see `LICENSE`).
