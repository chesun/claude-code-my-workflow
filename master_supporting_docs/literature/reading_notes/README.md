# Reading Notes — Canonical Structure

**Purpose.** Reading-notes files are the project's record of primary-source engagement. The PreToolUse hook at `.claude/hooks/primary-source-check.py` checks this directory before allowing edits to load-bearing files that cite external papers. Having a notes file = the paper has been read. No notes file + PDF in repo = edit blocked.

**Rule:** `.claude/rules/primary-source-first.md`.

## Two accepted formats

### 1. Per-paper file (preferred for load-bearing references)

Filename: `{surname1}_{surname2}_{year}.md`, lowercase, underscore-separated. Examples:

- `angrist_pischke_2009.md`
- `card_krueger_1994.md`
- `kahneman_tversky_1979.md`
- `chetty_friedman_hendren_2018.md`

### 2. Compiled batch file (acceptable for reading sprints)

A single `.md` file containing multiple papers, each section introduced by a `**Citation:**` metadata line that names the surnames and year:

```markdown
## Angrist & Pischke (2009) — Mostly Harmless Econometrics

**Citation:** Angrist, J. D., & Pischke, J.-S. (2009). Mostly Harmless Econometrics...

...notes...

## Card & Krueger (1994) — Minimum Wages and Employment

**Citation:** Card, D., & Krueger, A. B. (1994). Minimum Wages and Employment...
```

The hook matches on the `**Citation:**` line specifically — section headers alone are not enough. This is intentional: conceptual memos and README files may mention a paper in a header without being notes about it.

## Required sections (per-paper file template)

```markdown
---
citation: [Full citation with journal, volume, pages]
bibtex_key: [key used in references.bib]
primary_source: master_supporting_docs/literature/papers/[filename].pdf
date_read: YYYY-MM-DD
reader: [Name | Claude | librarian]
---

# [Authors] ([Year]) — [Short title]

## Summary

One paragraph. What does the paper do?

## Core claims this paper makes

Bulleted list. Each claim in its own bullet, concrete enough to cite.

## Definitions I should cite verbatim

Direct quotes of the paper's key definitions. Load-bearing in downstream work — paraphrasing loses precision.

## What this paper is NOT claiming (common misreadings)

**This section is load-bearing for preventing derivative-doc drift.**

Anticipate or record ways the paper gets misread. If downstream docs (ADRs, analysis memos, hypotheses, session logs) have previously misframed the paper, record the correction here. Future readers should see the misreading and the corrected reading side-by-side.

Example format:
- *Misreading:* [Common distortion of the paper's claim, as it appears in derivative docs.]
- *Correction:* [What the paper actually says, ideally with a page reference.]

## Method

Experimental design, data, identification strategy. One paragraph.

## Key numerical results

Bulleted. Direction, size, confidence bounds if reported.

## Relevance to our project

Which hypotheses / design decisions / ADRs does this paper bear on? Cite ADR numbers.

## Open questions flagged by this paper (for our work)

Bulleted.

## Passages worth quoting

Direct quotes with page numbers. Use when the paraphrase risks losing precision.
```

## Filling in for Claude-read papers

If Claude reads a paper in-session (e.g., via the `pdf-learnings` skill), the output should land here with `reader: Claude` and the session-log reference in the frontmatter. A Claude-produced notes file is no lower-status than a human-produced one — both count toward the hook's check.

## When a paper is superseded or revised

Keep the original notes file. If a newer version changes the claims, write a new notes file with the updated citation date. Both remain readable.

## Escape hatch

If you need to edit around an existing citation without making a new framing claim (e.g., typo fix, renumbering), include an escape comment in the delta:

```
<!-- primary-source-ok: smith_jones_2024 -->
```

Abuse of the escape hatch is auditable: `grep -R "primary-source-ok" quality_reports/ experiments/ theory/`.
