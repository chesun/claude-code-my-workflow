# 2026-07-01 — Citation-guard regex hardening + agenda refresh

## Goal

Catch-up + agenda session, then execute the citation-guard regex hardening umbrella (TODO Up Next item, added this session). User: "the primary-source citation hook fires on false positives too often."

## Part 1 — Catch-up + agenda (done, pushed)

- `26c0332` — TODO.md synced with the 2026-06-23 sessions (pilot push done, lab-guide infra, csac2026 port); lab DVC effort closed (hub updated by Christina); 4 new agenda items added: citation-guard hardening (umbrella merging NEVER_SURNAMES extension + unicode proposal), automated housekeeping w/ commit+push, econ academic voice profiles (applied micro + behavioral), atomic commits by default.
- Memory: commit-discipline preferences saved; **9 orphaned memories migrated** from the pre-rename project path (claude-code-my-workflow → claude-research-workflow) — synced to claude-config (`9bc32eb`, pushed).
- Noted: TODO.md heading still says old repo name; old-path memory dirs left in place.

## Part 2 — Citation-guard fixes (in `.claude/hooks/primary_source_lib.py`)

| Fix | Status | Commit |
|---|---|---|
| ADR status words → NEVER_SURNAMES (mirrors bdm_bic `a68fece`) | DONE, pushed | `aaba644` (+ TODO note `6c3b272`) |
| **ISO-date/range guard** — `(?![-–—/]\d)` after year in AUTHOR_YEAR; kills "Word YYYY-MM-DD" class structurally | DONE, committed | `53c0a99` |
| Blocklist cluster 2: `deferred`, `open` + changes-table verbs (added/new/fixed/removed/inserted/replaced/changed/extended/deleted/dropped/copied/merged/patched) | DONE, committed (9 tests) | `48bd093` |
| **Comma-list lead-author drop** (user-reported mid-session): 3-slot regex restarted mid-list — `Bohren, Imas, Rosenberg (2019)` → `imas_rosenberg_2019` (test string, not a framing claim); AEA 4-author form also affected. Fixed: single repeated `authors` group + `AUTHOR_SEP` split in Python; handles any author count. Diagnosis row in verification ledger. | DONE, committed (5 tests) | `c40a3ec` |
| Unicode proposal implemented: `_ascii_fold` (NFD + precomposed map) before extraction; hyphen→underscore fallback in `matching_notes_files` + `paper_pdf_exists_for`; citation-metadata lines folded. Verified: 116-check suite (16 new), stop-hooks 22/22, py_compile, end-to-end PreToolUse run blocks accented citation with folded stem `muller_2020` (previously a silent enforcement MISS — accents aborted the match entirely) | DONE, committed | `a4084f1` |
| Rule-doc updates (`primary-source-first.md`): blocklist categories + structural-guards subsection + unicode paragraph | DONE, committed | `1eb45b3` |
| Housekeeping: TODO umbrella updated, proposal marked IMPLEMENTED | DONE | (this commit) |

## Umbrella outcome (2026-07-01)

All four fix classes landed 2026-07-01. Suite: 116 checks + 22 stop-hooks, all green.

## Workflow round (2026-07-02) — stress → implement → independently verify

FP analysis (`quality_reports/reviews/2026-07-01_primary-source-hook-fp-analysis.md`, probe-verified) then a dynamic workflow (`wf_cf898e8f-8ec`, 9 agents, ~1.0M subagent tokens, 2 implement/verify rounds): 3 stress agents confirmed **54 cases** by execution; implementer landed the P1/P2/P3 roadmap; independent verifiers re-ran everything + fresh same-class probes. TP verifier PASSed both rounds (34/34 legitimate AEA forms, allowlist rescue of structural positions, e2e hook correct). FP verifier FAILed round 2 only on **enumeration-gap siblings** (Photoshop/Datastream/semester/medal/Thanksgiving) — closed in the main session with tests. Final: **47/54 fixed, 7 designed residue** (bare place+year, surname-identical titles, particle surnames — citation-line lookup mitigates; mixed-case orgs — skip-list).

**Mechanisms landed** (`57e8e0e`): markdown-aware SENTENCE_BOUNDARY (tables/bullets/headings/blockquotes/line starts need allowlist — the dominant FP class); typographic fold (curly quotes, en/em-dash, NBSP — fixes wrong-author stem bugs); possessive normalization + `et al.'s` + `and colleagues` forms (closed 4 false NEGATIVES); apostrophe-free stems + symmetric lookups; preceding-token cue filter (storm cues, all-caps acronym precursors); org skip-list state file `primary_source_orgs.txt`; all-caps floor 3→2; large NEVER_SURNAMES clusters (collision surnames excluded). Suite 116 → **209 checks**. Rule doc rewritten to match (filter stack 1/1b/1c/2–5, typographic handling, known residue).

**Open:** propagate all 8 hook commits (`aaba644`…`57e8e0e` + docs) to overlays + consumers; BDD override cleanup after propagation; P3-c telemetry (block logging) not yet implemented — still in TODO.

## Key implementation facts (for continuation)

- Test suite is **script-style**, not pytest: `python3 .claude/hooks/test_primary_source_lib.py` (pytest collects 0). Exits on first FAIL; ends "All tests passed."
- `NEVER_SURNAMES` frozenset at `primary_source_lib.py:134`; status-word block appended at end (before `})`).
- AUTHOR_YEAR regex ~line 104-125 (VERBOSE); date guard sits between `(?P<year>...)` and `[a-z]?\)?`.
- `matching_notes_files` (line ~387): filename `startswith(stem_lower)` — needs also trying `stem.replace('-','_')`; surname regex built from `stem.split('_')` — hyphenated surname parts (e.g. `szekely-rizzo`) should split on `[_-]` too.
- `paper_pdf_exists_for` (line ~443): surnames from `split('_')`; filename tokens split on non-alphanumeric — hyphenated stem surname never matches; split stem on `[_-]`.
- Propagation NOT yet done for any of today's hook commits (Class A file; bdm_bic has the status-word fix natively). Decide at end: propagate now vs. after umbrella completes (user leaned "more fixes first").

## Decisions

- Atomic commits + push after each housekeeping pass = session-wide discipline (user-set, in memory + TODO).
- Date guard chosen as structural fix over enumerating more blocklist words.
