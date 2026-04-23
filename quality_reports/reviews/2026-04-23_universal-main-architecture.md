# Universal Main — Architecture Proposal

**Date:** 2026-04-23
**Goal:** Main is a **universal, paradigm-agnostic** research workflow. `applied-micro` and `behavioral` are thin overlays that add their paradigm-specific content. Universal improvements land on main and propagate.

**Scope:** Advice only. Do not execute.

---

## 1. Classification — what's universal vs paradigm-specific

Derived from the two overlay branches (applied-micro as of `d0313ca`, behavioral as of `e9260cf`).

### Agents (of 23 total distinct)

**Universal (16)** — present on both overlays:

coder, coder-critic, data-engineer, domain-referee, explorer, explorer-critic, librarian, librarian-critic, methods-referee, orchestrator, storyteller, storyteller-critic, tikz-reviewer, verifier, writer, writer-critic

**Applied-micro overlay (2):**

strategist, strategist-critic (identification strategy: DiD/IV/RDD/synthetic control)

**Behavioral overlay (7):**

theorist, theorist-critic (formal models), designer, designer-critic (experimental design), otree-specialist, qualtrics-specialist, editor (journal-editor synthesizer — currently behavioral-only, but conceptually universal; see §3 open question)

### Skills (of 25 total distinct)

**Universal (14)** — present on both:

analyze, challenge, commit, context-status, deep-audit, discover, learn, new-project, review, revise, submit, talk, tools, write

**Applied-micro overlay (3):**

strategize (dispatches strategist), balance (balance tables), event-study (event-study plots)

**Behavioral overlay (5):**

design (dispatches designer), theory (dispatches theorist), otree, qualtrics, preregister (AsPredicted/OSF pre-registration — arguably universal for any empirical work; see §3)

**Applied-micro has three skills behavioral folded into `/tools`** (compile-latex, extract-tikz, validate-bib). For universal main, `/tools` is the cleaner pattern — standalone skills go away; `extract-tikz` parked.

### Rules (of 27 total distinct)

**Universal (18)** — on both overlays with equivalent content:

agents, decision-log, figures, logging, output-length, primary-source-first, python-code-conventions, quality (weights differ — see §3), r-code-conventions, replication-protocol, revision, single-source-of-truth, tables, tikz-visual-quality, todo-tracking, verification-protocol, workflow (references strategist/designer — see §3), working-paper-format

**Naming drift — unify:**

- `stata-conventions.md` (applied) vs `stata-code-conventions.md` (behavioral) — same content, different filename. Recommend `stata-code-conventions.md` to match the `*-code-conventions.md` pattern.

**Applied-micro overlay (3):**

- `air-gapped-workflow.md` — actually universal (any secure-data project needs it). Recommend moving to main.
- `exploration-fast-track.md`, `exploration-folder-protocol.md` — universal. Recommend moving to main.

**Behavioral overlay (5):**

- `experiment-design-principles.md` — behavioral-only.
- `content-standards.md` — behavioral-only (check content; may be universal).
- `meta-governance.md` — universal (governs how to treat the template-vs-project dual nature). Recommend moving to main.
- `orchestrator-protocol.md`, `plan-first-workflow.md`, `session-logging.md` — **duplicates** of content already in `workflow.md` and `logging.md` on behavioral. Should be deleted from behavioral as cleanup, not ported anywhere.

### Hooks, references, state, templates, folders

All universal:

- `.claude/hooks/` — all 10 hooks (primary-source-check, primary-source-audit, primary_source_lib, log-reminder, verify-reminder, context-monitor, notify, pre-compact, post-compact-restore, post-merge, protect-files).
- `.claude/state/primary_source_surnames.txt` — template stub.
- `.claude/references/pdf-chunking.md`.
- `decisions/README.md` — universal ADR template.
- `master_supporting_docs/literature/{papers,reading_notes}/README.md`.

---

## 2. Proposed architecture

### Main (universal base)

```
.claude/
├── agents/
│   ├── coder + coder-critic
│   ├── data-engineer
│   ├── domain-referee
│   ├── explorer + explorer-critic
│   ├── librarian + librarian-critic
│   ├── methods-referee
│   ├── orchestrator
│   ├── storyteller + storyteller-critic
│   ├── tikz-reviewer
│   ├── verifier
│   └── writer + writer-critic
├── skills/
│   ├── /analyze, /challenge, /commit, /context-status, /deep-audit
│   ├── /discover, /learn, /new-project, /review, /revise
│   └── /submit, /talk, /tools, /write
├── rules/
│   ├── (universal — see §1 list)
│   └── (includes meta-governance, air-gapped-workflow, exploration-*)
├── hooks/ (all 10)
├── references/pdf-chunking.md
└── state/primary_source_surnames.txt (empty stub)
decisions/README.md
master_supporting_docs/literature/{papers,reading_notes}/README.md
CLAUDE.md (paradigm-agnostic, heavy placeholder usage)
TODO.md (stub)
```

### Applied-micro overlay

Adds on top of main:

- Agents: `strategist`, `strategist-critic`
- Skills: `/strategize`, `/balance`, `/event-study`
- CLAUDE.md overlay: title = "Applied Microeconomics Research", scope language = observational/administrative data, identification strategies
- Domain profile: `references/domain-profile.md`

### Behavioral overlay

Adds on top of main:

- Agents: `theorist`, `theorist-critic`, `designer`, `designer-critic`, `otree-specialist`, `qualtrics-specialist`
- Skills: `/theory`, `/design`, `/otree`, `/qualtrics`, `/preregister`
- Rules: `experiment-design-principles.md`, `content-standards.md`
- Folders: `theory/`, `experiments/` (designs, protocols, instructions, oTree, qualtrics, comprehension, pilots)
- CLAUDE.md overlay: behavioral/experimental framing
- Domain profile: `references/domain-profile-behavioral.md`

---

## 3. Open design questions

These are judgment calls about what's "universal" vs "paradigm-specific". Worth resolving before construction.

### Q1: Is `editor` universal or behavioral-only?

Currently behavioral-only. The editor agent synthesizes referee reports into a journal-editor decision (Accept / R&R / Reject). That logic applies to any paradigm. **Recommendation:** move editor to main.

### Q2: Is `/preregister` universal or behavioral-only?

Pre-analysis plans are increasingly expected for applied-micro work too (AEA pre-registry). **Recommendation:** move `/preregister` to main.

### Q3: `workflow.md` references `strategist` / `designer` by name. How to abstract?

Options:

- **A. Abstract slot.** Rename the phase "Identification Strategy / Experimental Design" and reference a placeholder: "the overlay's strategy agent." Each overlay's CLAUDE.md declares its agent.
- **B. Both names present.** Main's workflow.md says "dispatches `strategist` OR `designer` depending on paradigm." Both overlays work; neither breaks.
- **C. Parametrize via CLAUDE.md.** CLAUDE.md on each overlay declares `STRATEGY_AGENT = strategist` (applied) or `designer` (behavioral). Workflow rule reads that.

**Recommendation:** B (both names present). Simplest. No abstraction leakage. Overlays don't need to edit workflow.md.

### Q4: `quality.md` weights differ between overlays. How?

Applied-micro weights: literature 10%, data 10%, identification 25%, code 15%, paper 25%, polish 10%, replication 5%.

Behavioral weights: literature 8%, theory 15%, design 25%, implementation 7%, code 10%, paper 20%, polish 10%, replication 5%.

Behavioral has `theory 15%` and `implementation 7%` that applied doesn't have (applied has no theorist and no otree/qualtrics implementation phase).

**Recommendation:** main defines **neutral universal weights** that work when neither theory nor design is present (e.g., same as applied-micro today). Each overlay overrides `quality.md` with its paradigm's weighting. This makes `quality.md` overlay-specific, but the file is small and the override is clean.

Alternative: main defines a **weight computation algorithm** with renormalization when components are missing (already in quality.md §1 "When Components Are Missing"). Then weights are calculated from which agents exist. Cleaner but more complex.

### Q5: CLAUDE.md — one template or overlay-specific?

CLAUDE.md already differs significantly between overlays (framing, folder diagram). It's the natural "per-overlay customization" point. **Recommendation:** each overlay has its own CLAUDE.md. Main ships a neutral CLAUDE.md template (what a clean fork would see).

### Q6: `master_supporting_docs/` subfolders?

- `literature/` — universal (primary-source-first applies to both).
- `supporting_papers/` — universal.
- `experimental_design/`, `otree/`, `preregister/`, `supporting_slides/`, `theory/` (behavioral-only): behavioral overlay.

**Recommendation:** main ships with `literature/` and `supporting_papers/`; behavioral overlay adds its behavioral-specific subtrees.

---

## 4. Construction strategy (two phases)

### Phase 1: Build universal main

1. Branch off applied-micro as the starting point (closest to "universal").
2. Remove applied-specific content:
   - `agents/strategist.md`, `agents/strategist-critic.md`
   - `skills/strategize/`, `skills/balance/`, `skills/event-study/`
   - CLAUDE.md: replace "Applied Microeconomics" framing with paradigm-agnostic.
3. Add content currently only on behavioral that belongs in main:
   - `agents/editor.md` (per Q1)
   - `skills/preregister/` (per Q2)
   - `rules/meta-governance.md`
4. Unify filenames:
   - `stata-conventions.md` → `stata-code-conventions.md`.
5. Update `workflow.md` and `agents.md` to handle strategist OR designer (per Q3-B).
6. Update `quality.md` to universal-neutral weights (per Q4 recommendation).
7. Rewrite README.md — research template, credit Pedro + Hugo as base, describe the two overlays.
8. Verify: all universal skills dispatch correctly (no broken `agents/strategist.md` references).

### Phase 2: Rebuild overlays as thin diffs

**applied-micro overlay:**

1. Starting from new main, add back:
   - `agents/strategist.md`, `agents/strategist-critic.md`
   - `skills/strategize/`, `skills/balance/`, `skills/event-study/`
   - CLAUDE.md: applied-micro framing (replace the template's neutral version)
2. Commit as a single overlay commit.

**behavioral overlay:**

1. Starting from new main, add back:
   - `agents/theorist.md`, `agents/theorist-critic.md`, `agents/designer.md`, `agents/designer-critic.md`, `agents/otree-specialist.md`, `agents/qualtrics-specialist.md`
   - `skills/theory/`, `skills/design/`, `skills/otree/`, `skills/qualtrics/`
   - `rules/experiment-design-principles.md`, `rules/content-standards.md`
   - Folders: `theory/`, `experiments/` (with their subtrees)
   - CLAUDE.md: behavioral framing
   - Override `quality.md` with behavioral weights (per Q4)
   - `.claude/references/domain-profile-behavioral.md`
2. Also **clean up duplicates** on behavioral while rebuilding:
   - Delete `rules/session-logging.md` (superseded by logging.md)
   - Delete `rules/plan-first-workflow.md` (superseded by workflow.md §1)
   - Delete `rules/orchestrator-protocol.md` (superseded by workflow.md §2)

### Phase 3: Preserve archives

- `main-lecture-archive` branch from current main (Pedro's upstream lecture template).
- `applied-micro-pre-universal` branch from current applied-micro (preserves the pre-refactor applied-micro state).
- `behavioral-pre-universal` branch from current behavioral.

Insurance against regression. Cheap to keep.

---

## 5. Workflow going forward

Once this architecture exists:

- **Universal feature** (e.g., new hook, improved logging, better writer-critic checks) → land on main → cherry-pick or rebase into both overlays.
- **Applied-micro-specific** (e.g., new DiD estimator in `/event-study`) → land on applied-micro only.
- **Behavioral-specific** (e.g., new oTree 6.x pattern) → land on behavioral only.
- **Periodic sync from upstream Pedro** → merge `upstream/main` into `main-lecture-archive` → cherry-pick anything useful onto main.

This is the "trunk + overlays" pattern used by many multi-distribution projects (think Debian + Ubuntu + Mint).

---

## 6. Estimated effort

| Phase | Task | Effort |
|---|---|---|
| 1 | Build universal main from applied-micro | 2–3 hours |
| 1 | Rewrite README | 30–60 min |
| 2 | Rebuild applied-micro overlay | 30 min |
| 2 | Rebuild behavioral overlay + duplicate cleanup | 60 min |
| 3 | Archive branches | 5 min |
| — | Verification: hooks fire, skills dispatch, compile works | 30 min |
| **Total** | | **~5 hours** |

Most of the work is Phase 1 (deciding each edge case) and the README rewrite. Phases 2–3 are mechanical.

---

## 7. Decisions to resolve before executing

Before I run Phase 1, I need your call on:

1. **Q1 (editor universal?)** — my vote: yes.
2. **Q2 (/preregister universal?)** — my vote: yes.
3. **Q3 (strategist/designer naming in workflow.md)** — my vote: both names present, no abstraction.
4. **Q4 (quality.md weights)** — my vote: main has applied-micro's weights as neutral default; behavioral overrides.
5. **Q5 (CLAUDE.md neutral template)** — my vote: yes.
6. **Q6 (master_supporting_docs subtree)** — my vote: main has literature + supporting_papers; behavioral adds the rest.
7. **README scope** — full rewrite or adapt Pedro's?
8. **Archive branches** — keep `main-lecture-archive`, `applied-micro-pre-universal`, `behavioral-pre-universal`?

Give me your calls and I'll map them into a concrete execution plan.
