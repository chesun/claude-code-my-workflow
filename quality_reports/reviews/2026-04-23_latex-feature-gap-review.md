# LaTeX Feature Gap Review — Behavioral vs Applied-Micro

**Date:** 2026-04-23
**Scope:** LaTeX-adjacent agents, skills, and rules on `applied-micro` that are absent from `behavioral`
**Question:** What should we port from applied-micro's LaTeX surface to behavioral?

---

## Summary

| Category | Gap | Priority | Recommendation |
|---|---|---|---|
| writer-critic `Critical Rules` block | HIGH | Port | Ignore commented LaTeX; regression tables as source of truth for results |
| `tikz-reviewer` agent | HIGH | Port | Behavioral uses TikZ for experimental mechanisms, game trees, timelines |
| `tikz-visual-quality.md` rule | HIGH | Port | Companion to tikz-reviewer |
| `extract-tikz` skill | LOW | Hold | Beamer→Quarto SVG pipeline — only useful if Quarto is an active workflow on behavioral |
| `compile-latex` skill | — | None | Already folded into `/tools compile` on behavioral |
| `validate-bib` skill | — | None | Already folded into `/tools validate-bib` on behavioral |

**No regressions in the other direction worth worrying about** — behavioral's writer-critic and writer are actually more detailed than applied-micro's (McCloskey/Cochrane/Knuth checklists, experimental reporting completeness). Its working-paper-format rule ships a much more concrete reference preamble (biblatex+biber, full theorem environments) than applied-micro's abstract package list.

---

## 1. writer-critic Critical Rules (HIGH — port)

Applied-micro's `agents/writer-critic.md` has a `## Critical Rules` block that behavioral's version lacks:

```markdown
## Critical Rules

1. **IGNORE all commented-out LaTeX.** Lines starting with `%`,
   `\iffalse...\fi` blocks, and `\begin{comment}...\end{comment}`
   are old drafts or notes — never treat them as current paper
   content. Do not flag issues in commented text.

2. **Regression tables are the source of truth for results.** When
   the prose describes coefficients, significance levels, or
   magnitudes, cross-check against the actual `\begin{table}`
   content in the paper. The text may be stale from a prior draft.
   Flag every discrepancy between text and tables as a CRITICAL
   issue.
```

**Why it matters for behavioral:**

- Christina's own `feedback_latex_review.md` memory encodes exactly this preference: "Ignore commented-out LaTeX; use regression tables as source of truth over prose."
- Behavioral papers have the same table/prose drift risk as applied-micro — the rule is paradigm-agnostic.

**Port target:** `agents/writer-critic.md` on behavioral. Insert immediately after the `## Your Task` intro, before the 6-category check list. Also add a corresponding deduction line to the scoring table:

```
| Prose-table discrepancy (CRITICAL) | -25 |
```

---

## 2. tikz-reviewer agent (HIGH — port)

Applied-micro ships `agents/tikz-reviewer.md` — a harsh visual critic for TikZ diagrams. Behavioral doesn't have it.

**Why it matters for behavioral:**

TikZ is heavily used in behavioral/experimental economics for:

- Experimental timelines (stages, information flow, within-subject vs between-subject structure)
- Game trees and extensive-form diagrams
- Mechanism illustrations (BDM, MPL, belief elicitation layouts)
- Signal structure diagrams (Bayesian persuasion, inference)
- Equilibrium-selection diagrams
- Bracket/scope diagrams illustrating treatment assignment

**What the agent checks:**

- Label overlaps with curves, lines, dots, braces, other labels
- Geometric accuracy (parallel lines actually parallel, dot alignment, brace endpoints)
- Visual semantics (solid=observed, dashed=counterfactual; filled vs hollow dots)
- Spacing, proportion, aesthetic polish
- Iterative APPROVED / NEEDS REVISION / REJECTED verdict

**Port target:** copy `agents/tikz-reviewer.md` to behavioral as-is. The agent is paradigm-agnostic.

**Integration:** storyteller-critic on behavioral should reference tikz-reviewer when a talk contains TikZ — dispatching tikz-reviewer as a sub-review when TikZ blocks are present. Add a one-line pointer in storyteller-critic's compilation check: "If slides contain `\begin{tikzpicture}` blocks, dispatch `tikz-reviewer` for each."

---

## 3. tikz-visual-quality rule (HIGH — port)

Applied-micro ships `rules/tikz-visual-quality.md` — the concrete standard that `tikz-reviewer` scores against. Behavioral doesn't have it.

**What it codifies:**

- Label positioning: never overlap curves/lines/dots/braces/other labels; stagger near-vertical labels; consistent anchors
- Visual semantics: solid=observed, hollow=counterfactual; consistent color meaning; line weights (axes `thick`, data `thick`, annotations `thick`, grid `dashed, gray!40`)
- Spacing: standard scale `[scale=1.1]`; dot radius `4pt`; min 0.2 units between label and nearest graphical element; axes extend beyond data
- Checklist for self-review
- SSOT rule: Beamer `.tex` is authoritative for TikZ; `extract_tikz.tex` is derived

**Port target:** copy `rules/tikz-visual-quality.md` to behavioral as-is.

---

## 4. extract-tikz skill (LOW — hold)

Applied-micro ships `skills/extract-tikz/SKILL.md` — a 7-step Beamer→PDF→SVG pipeline so TikZ diagrams from Beamer decks can be embedded in Quarto slides.

**Why it's lower priority for behavioral:**

- Behavioral's `/talk` skill supports Quarto RevealJS as a `--quarto` flag, but Beamer is the default — Quarto is secondary.
- If behavioral rarely renders Quarto talks, this skill is dead weight.
- If behavioral users start using Quarto for seminars, this becomes useful.

**Recommendation:** HOLD. Port only if/when Christina starts rendering Quarto talks from behavioral projects. Otherwise, add as a backlog TODO: "Port extract-tikz skill if Quarto becomes an active talk workflow."

---

## 5. Skills already consolidated (no action)

- **compile-latex** — applied-micro has a standalone skill. Behavioral has `/tools compile` subcommand covering the same workflow (paper 3-pass + bibtex/biber, talks with TEXINPUTS). No gap.
- **validate-bib** — applied-micro has standalone skill. Behavioral has `/tools validate-bib`. No gap.

---

## Reverse direction (applied-micro is missing, behavioral has — flagged for awareness)

These aren't the question asked, but worth noting so they're not accidentally lost when going the other way:

- Behavioral's `writer-critic` has McCloskey/Cochrane/Knuth anti-pattern checklists + Experimental Reporting Completeness checks that applied-micro's lacks. Specifically: naked-"this" flagging, sentence-starting-with-symbol detection, consecutive-displayed-equation detection, decimal-excess rule.
- Behavioral's `writer` enforces Cochrane introduction structure (first sentence states contribution; never open with "This paper...") more aggressively.
- Behavioral's `working-paper-format.md` has a concrete reference preamble block (biblatex+biber, lmodern, microtype, full theorem envs, custom colors) vs. applied-micro's abstract package list.

These would be worth back-porting to applied-micro in a separate pass, but that's not today's scope.

---

## Recommended port order

1. **writer-critic Critical Rules** — smallest patch, highest value (matches a stored user preference).
2. **tikz-reviewer agent + tikz-visual-quality rule** — pair, port together. Low risk (agent is paradigm-agnostic; rule is just TikZ standards).
3. **Add pointer in storyteller-critic** — one-line note that tikz-reviewer should be dispatched when slides contain `\begin{tikzpicture}`.
4. **Backlog:** extract-tikz skill, pending Quarto-talk workflow adoption.

**Total effort:** ~20 min for items 1–3. One commit on behavioral, push. claude-config sync not applicable (project-scoped).
