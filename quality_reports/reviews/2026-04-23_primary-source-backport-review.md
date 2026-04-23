# Review: Backport Primary-Source-First from BDM BIC → Claudeflow (behavioral)

**Date:** 2026-04-23
**Source:** `~/github_repos/bdm_bic/`
**Target:** `~/github_repos/claude-code-my-workflow/` (behavioral branch)
**Status:** Review only — no changes yet

---

## What's being backported

The BDM project ships a three-piece primary-source-first enforcement system added on 2026-04-22 after the UJS-conflation incident. It is designed to make four kinds of citation error deterministically blocking rather than relying on the model to remember to open the PDF.

### Inventory (new → target)

| Item | Type | Source path (BDM) | Target path (claudeflow) |
|------|------|-------------------|--------------------------|
| `primary-source-first.md` | Rule spec | `.claude/rules/` | `.claude/rules/` |
| `primary_source_lib.py` | Shared library | `.claude/hooks/` | `.claude/hooks/` |
| `primary-source-check.py` | PreToolUse hook | `.claude/hooks/` | `.claude/hooks/` |
| `primary-source-audit.py` | Stop hook | `.claude/hooks/` | `.claude/hooks/` |
| settings.json entries | Hook wiring | PreToolUse Edit\|Write + Stop | same |

### What the rule enforces

Three deterministic block conditions when a load-bearing file edit (or session prose) cites an external paper:

1. **Notes missing, PDF in repo** → "read the PDF, write notes"
2. **Notes missing, PDF not in repo** → "add the PDF first"
3. **Notes exist, but not Read/Write/Edit-touched this session** → "consult notes before citing"

Escape hatch: `<!-- primary-source-ok: stem1, stem2 -->` in the delta (or in prose for the Stop hook). Auditable via grep.

### Coverage split

- **PreToolUse hook** scans the delta of Edit/Write tool calls on scoped files.
- **Stop hook** scans all assistant text in the session transcript at turn-end — closes the gap where a citation is made only in conversation and never hits a file.

---

## How well does it generalize?

The system is well-engineered — fail-open on exceptions, shared library, stop-loop safety via `stop_hook_active`. But three pieces are tuned to BDM BIC specifically and must be generalized before this lands in a template.

### Must-change for template

1. **`KNOWN_SURNAMES` allowlist** (`primary_source_lib.py`, lines 37-90)
   - BDM hard-codes 80+ surnames (Chakraborty, Kendall, Danz, Vesterlund, …). Works great in BDM; useless for a forker's project.
   - **Fix:** Either (a) drop the allowlist and accept more false positives, or (b) load it from a project-local config file (e.g. `.claude/state/known_surnames.txt`), or (c) derive it on-the-fly from `references.bib` keys.
   - **Recommendation:** (b) — a project-local config file. Template ships empty or with a `# one surname per line, lowercase` stub. Each forker adds their own papers.

2. **`ENFORCEABLE_PATTERNS`** (`primary_source_lib.py`, lines 25-32)
   - Includes `bdm_bic_paper/paper/.*\.tex$` — that path only exists in BDM.
   - **Fix:** Replace with generic paths matching the template's folder structure. Template uses `[OVERLEAF_PATH]/paper/`, not an in-repo paper path.
   - **Recommendation:** Scope to in-repo load-bearing artifacts only: `experiments/designs/decisions/**`, `quality_reports/plans/**`, `quality_reports/session_logs/**`, `quality_reports/*_analysis.md`, `theory/**/*.tex`, `experiments/designs/**/*.md`. Overleaf paper `.tex` files live outside the repo so PreToolUse won't see them anyway.

3. **Rule doc's "Why this exists" sections** reference the UJS-specific incident and `bdm_bic_2026-03.md`.
   - **Fix:** In the template rule, keep the *mechanism* explanation but convert the incident to a generic example or move incident narrative to BDM's own decision-log / session log.

### OK as-is

- Reading-notes directory path (`master_supporting_docs/literature/reading_notes/`) — this is a template convention that forkers inherit.
- Paper directory path (`master_supporting_docs/literature/papers/`) — same.
- The three failure modes, the escape hatch, the stop-loop safety — all generic.
- The README template for reading-notes files — generic, should also be backported.

### Potentially template-shippable extras

The BDM project also has:
- `master_supporting_docs/literature/reading_notes/README.md` — the canonical structure doc
- `.claude/rules/decision-log.md` — ADR-style decision log rule (not requested, but related)

Both would benefit forkers but are out of scope for this backport. Flag for a later TODO item.

---

## Dependencies and side-effects

### New directories required

Claudeflow's `master_supporting_docs/` currently has: `experimental_design/`, `otree/`, `preregister/`, `supporting_papers/`, `supporting_slides/`, `theory/`. There is no `literature/papers/` or `literature/reading_notes/` directory.

**Decision needed:** Do we (a) add `literature/papers/` and `literature/reading_notes/` subdirectories to the template structure, or (b) rename `supporting_papers/` to `literature/papers/` to match, or (c) make the hook path configurable?

**Recommendation:** (a) add `literature/` parallel to `supporting_papers/`. Keep `supporting_papers/` for now to avoid breaking existing forks; document `literature/papers/` + `literature/reading_notes/` as the canonical location for cited primary sources. Note the distinction in CLAUDE.md.

### Settings.json changes

Adds one PreToolUse hook (Edit|Write matcher, timeout 10) and one Stop hook (timeout 15). Both run after existing hooks; no ordering conflict.

### CLAUDE.md / rule index

`CLAUDE.md` should reference the new rule under Core Principles or a new "Citation discipline" subsection. Also update `TODO.md` when done.

### Compatibility with existing Stop hook

Claudeflow already has `log-reminder.py` as a Stop hook (THRESHOLD=10). BDM raised it to 15. The BDM project runs both `log-reminder.py` and `primary-source-audit.py` as Stop hooks. Both return blocks independently; if both fire, Claude sees the first non-zero exit and blocks on that one. Order matters only cosmetically — the user experience is one block at a time. **No conflict.**

---

## Risks

1. **False positives on prose.** The Stop hook scans *every* assistant message in the transcript. If Claude mentions "Angrist & Pischke 2009" in an explanatory tangent with no intent to cite, the audit fires. The allowlist mitigates this in BDM; a template with an empty allowlist would fire on every capitalized-name-plus-year pattern. **This is the primary risk.**
   - Mitigation: ship the allowlist mechanism, but with a sensible default (probably empty). Document clearly that forkers must populate it before the audit hook becomes useful. Or: ship a `DISABLE_AUDIT = True` flag in the template that forkers flip on once they've populated the allowlist.

2. **Block fatigue.** If Claude hits the block during normal work (e.g. citing a paper in a plan draft before the PDF is added), it may learn to avoid load-bearing paths. Escape hatch + allowlist both mitigate, but the friction is real.

3. **Session-read check is strict.** A paper referenced in ten consecutive turns requires the notes file to be opened at least once per session. This is the point — but it means the first citation in every fresh session costs a Read. Acceptable overhead.

---

## Recommended backport plan — universal across both claudeflows

**Goal:** Ship primary-source-first as a universal feature of the claudeflow template — present on `main` (so both `behavioral` and `applied-micro` inherit it), with `literature/papers/` + `literature/reading_notes/` added to the universal folder structure.

**Branch strategy:**
- Build and test on `behavioral` (current branch).
- After verification, PR to `main`.
- Rebase `applied-micro` onto updated `main` so it picks up the same infrastructure.

### Phase 1: Generalize the library (required before anything ships)

1. **Externalize `KNOWN_SURNAMES`.** Move the allowlist out of `primary_source_lib.py` into a project-local config file: `.claude/state/primary_source_surnames.txt` (one lowercase surname per line, `#` comments allowed). Library reads it at import time; if file is missing or empty, **allowlist is skipped entirely** — every Author-Year match counts. This is the important semantic change: the template ships with no allowlist, and each project populates its own.
   - Rationale: "applied micro" projects will have a completely different author set (Chetty, Angrist, Card, …) than "behavioral" projects (Kahneman, Thaler, Fehr, …). Hardcoding either is wrong. An optional file lets each project opt in to the noise-reduction.
   - Add `.claude/state/primary_source_surnames.txt` (empty stub with header comments) to both claudeflows.

2. **Generalize `ENFORCEABLE_PATTERNS`.** Replace BDM paths with template-generic in-repo paths only:
   ```
   experiments/designs/decisions/.*\.md$
   experiments/designs/.*\.md$
   theory/.*\.(tex|md)$
   quality_reports/advisor_meeting_[^/]+/.*\.(tex|md)$
   quality_reports/session_logs/.*\.md$
   quality_reports/plans/.*\.md$
   quality_reports/reviews/.*\.md$
   quality_reports/[^/]+_analysis\.md$
   ```
   Overleaf paper `.tex` lives outside the repo, so the PreToolUse hook will never see it — don't include. Applied-micro and behavioral share these paths.

3. **Rewrite the rule doc.** Keep the mechanism, the three failure modes, the escape hatch, the two accepted notes formats. Drop the UJS-specific "Why this exists" — move to an `examples/` block or cite as a generic case study. Rename file can stay `primary-source-first.md`.

### Phase 2: Universal folder structure

4. **Add `master_supporting_docs/literature/` to both claudeflows** (`behavioral` first, then merged to `main`):
   - `master_supporting_docs/literature/papers/` — PDFs of cited primary sources (surname-year naming)
   - `master_supporting_docs/literature/reading_notes/` — one `.md` per paper (or compiled batch files)
   - `master_supporting_docs/literature/reading_notes/README.md` — generalized copy of BDM's canonical-structure doc
   - Add `.gitkeep` in both empty directories.
   - **Relationship to existing `supporting_papers/`:** leave `supporting_papers/` alone for now (it holds reference material, not necessarily cited primary sources). Document the distinction in `CLAUDE.md`:
     - `supporting_papers/` — reference material, methodology guides, textbook chapters
     - `literature/papers/` + `literature/reading_notes/` — papers cited in load-bearing artifacts (gated by primary-source-first)
   - A future cleanup can consolidate; not blocking.

5. **Update `CLAUDE.md` folder-structure diagram** to include `literature/` under `master_supporting_docs/`. Add a "Citation discipline" subsection under Core Principles pointing at the rule.

### Phase 3: Install the hooks on behavioral

6. Copy `primary_source_lib.py`, `primary-source-check.py`, `primary-source-audit.py` to `.claude/hooks/` (with Phase 1 edits applied).
7. Update `.claude/settings.json`:
   - PreToolUse `Edit|Write` — add `primary-source-check.py` after `protect-files.sh`.
   - Stop — add `primary-source-audit.py` after `log-reminder.py`.
8. Add `primary-source-first.md` to `.claude/rules/`.
9. Reference the rule in `CLAUDE.md` under Core Principles.

### Phase 4: Verify on behavioral

10. Trigger a test block: edit a scoped file citing a made-up paper ("Smith and Jones 2024") with no notes — confirm PreToolUse blocks.
11. Add the surname to `.claude/state/primary_source_surnames.txt`, retry — confirm still blocks.
12. Create a stub notes file matching the stem — confirm still blocks (notes not read this session).
13. Read the notes file, retry — confirm passes.
14. Test escape hatch.
15. Test Stop audit by citing in prose without notes.
16. Test permissive mode: empty allowlist, verify extractor catches everything (with lots of false positives as expected).

### Phase 5: Propagate to main and applied-micro

17. Update `TODO.md` on behavioral — move item to Done.
18. Commit on behavioral, push.
19. Open PR behavioral → main.
20. After merge, rebase `applied-micro` onto main (picks up the infrastructure automatically).
21. On applied-micro: add a project-specific `primary_source_surnames.txt` if desired (applied-micro canonical authors differ from behavioral).
22. Sync to `claude-config` repo per the global rule (rules/, settings.json changes).

### Out of scope (flag for follow-up TODOs)

- Decision-log rule from BDM.
- THRESHOLD change in log-reminder.py (15 vs 10 — BDM-specific tuning).
- Automated extraction of surnames from `references.bib` to prepopulate the allowlist.
- Consolidating `supporting_papers/` into `literature/papers/`.

---

## Remaining decision needed

**Surname allowlist default in the template:** I've planned for empty (most universal — catches every capitalized-name+year pattern, producing false positives that the user manages by populating the allowlist). Alternative is to ship a small curated seed list of very-common econ authors (Angrist, Card, Chetty, Kahneman, Thaler, …). My vote: empty, because any seed list biases toward one subfield. You decide.

---

## Estimated effort

- ~60 min to generalize library (config-file allowlist + path refactor + rule rewrite)
- ~15 min to add `literature/` directories and README.md to both flows
- ~15 min to install hooks on behavioral + settings.json edits
- ~20 min to verify (6 test cases above)
- ~15 min PR behavioral → main, rebase applied-micro, sync claude-config
- **Total: ~2 hours**

No destructive changes. Adds files + one settings.json diff + one folder-structure extension. Safe to proceed after decision on allowlist default.
