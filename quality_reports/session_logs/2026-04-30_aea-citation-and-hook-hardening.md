# Session Log: 2026-04-30 — AEA citation standardization + primary-source-first hook hardening

**Status:** COMPLETED

## Objective

Two interleaved threads:

1. **Standardize project citation style on AEA / Chicago author-date** (anchored on the AER style guide + AEA reference style pages). Make this universal — apply to all load-bearing artifacts and align the writer-critic deduction rubric, the LaTeX preamble, and the in-text convention.

2. **Harden the `primary-source-first` hook regex** against three classes of false-positive that surfaced during the citation work:
   - Hyphenated-shorthand misparse: `Cameron-Miller, Eyting-2024` coalescing into a fictitious co-author citation.
   - Trailing-punctuation residual: `Cameron-Miller and Eyting- (2024)` (a quoted hook-output line) capturing `Eyting-` greedy-with-hyphen, then post-strip producing a still-wrong stem.
   - Pedagogical-example overfire: style guides and rule docs using backtick-wrapped placeholder citations like `` `Smith (2020)` `` triggering the audit on what are clearly syntactic examples, not framing claims.

## Diagnosis & changes

### Hook hardening — three patches

| Commit | Constraint added | What it fixes |
|---|---|---|
| `8974236` | Year regex requires explicit separator (whitespace, paren, or comma) before the year | Blocks shorthand `Smith-2020`-style coalescing |
| `67bf5c2` | Surname char class anchored on a final letter: `[A-Z][A-Za-z\-']*[A-Za-z]` | Prevents capturing a surname that ends in `-` or `'`; closes the residual `Eyting-` case |
| `82b7257` | `extract_citations` pre-masks Markdown inline-code (`` `...` ``) and code-fenced blocks with same-length whitespace before running the regex | Skips pedagogical example citations in style guides; prevents recurring false-positive class on rule documentation |

All three are universal — landed on main, cherry-picked clean to applied-micro and behavioral.

### AEA citation standardization — `72d40ec`

Three correlated changes:

1. **`primary-source-first.md`** — replaced the prior two-coauthor-only convention with a full AEA / Chicago author-date table covering 1, 2, 3, 4, 5+ authors. AER-specific et al. thresholds called out: in-text 5+ truncates to et al.; reference list 11+ truncates to first seven + et al. Documents Oxford comma, no comma between author and year (Chicago, not APA), semicolon-separated multi-cites, suffix disambiguation for same-year, corporate / forthcoming / anonymous handling. Reference-list form examples added for journal article, book, working paper, edited volume chapter, dataset.

2. **`working-paper-format.md`** — corrected three AEA non-compliances in the standard preamble that had been there since the template was forked from upstream:
   - `maxcitenames=3` → `maxcitenames=4` (was producing et al. at 4+ authors; AER specifies 5+)
   - `maxbibnames=99` → `maxbibnames=10, minbibnames=7` (matches AER's "1-10 list all; 11+ first seven + et al." reference rule)
   - `\nameyeardelim={\addcomma\space}` → `\nameyeardelim={\addspace}` — the old setting was producing `(Smith, 2020)` APA form; AEA / Chicago uses `(Smith 2020)` with no comma

3. **`writer-critic.md`** — added five deduction rows for AEA citation form violations (-3 per, max -15 each): `&` between authors, missing Oxford comma, comma between author and year in parenthetical, et al. used at ≤4 authors, missing year-suffix on same-author same-year cites.

The Author-Year regex is intentionally NOT tightened to enforce AEA form. It stays permissive on detection (`&`-form and comma-form citations still trigger primary-source-first audits) so no real citation slips past the audit. Style enforcement is the writer-critic's job; the hook is for detection-and-grounding.

## Affected repositories

Each of the four commits propagated to all 9 surfaces. Final state:

| Repo / branch | Hook hardening 1 (year sep) | Hook hardening 2 (trailing letter) | AEA citation | Code-span mask |
|---|---|---|---|---|
| claude-research-workflow main | `8974236` | `67bf5c2` | `72d40ec` | `82b7257` |
| claude-research-workflow applied-micro | `0833612` | `c41980c` | `a1a631a` | `a4b6974` |
| claude-research-workflow behavioral | `297d4b6` | `8e8ae77` | `36d964d` | `8b98fb0` |
| va_consolidated | `4d63a53` | `29fe3c1` | `0d32cbc` | `91bb73d` |
| tx_peer_effects_local | `4aee4ed` | `3976411` | `b574b81` | `5044e41` |
| csac | `f917a3b` | `eb2ab25` | `70c7717` | `f7a4639` |
| csac2025 | `03acb37` | `dd1de0d` | `e32c513` | `ff8251c` |
| bdm_bic | `3c37128` | `d85575f` | `44ec240` | `73e422b` |
| belief_distortion_discrimination | `bf7c355` | `aed105e` | `3cfb95f` | `8adbcfc` |

Total: 36 commits across 9 repos. All pushed to origin.

## Design Decisions

| Decision | Alternatives | Rationale |
|---|---|---|
| Hook regex stays permissive on `&`-form and comma-form citations | Tighten regex to AEA only; reject malformed forms at parse time | The hook's job is detection (does this prose claim about a paper need notes?). Style enforcement is the writer-critic's job. Permissive parsing means malformed legacy prose still triggers the audit — defensive on the side of catching real citations even if they're badly written. |
| Code-span mask uses same-length whitespace, not removal | Strip the code spans entirely | Position preservation matters for the sentence-start filter, which uses `match.start()` to detect `[.?!:;]` immediately before the match. Removing characters would shift offsets and break that filter. |
| Three separate hook commits rather than one | Bundle all three regex hardening fixes into one commit | Each fix has a different failure mode and rationale; bundling would obscure the per-failure reasoning. Future archaeology benefits from per-bug commits with their own test cases. |
| Mask Markdown backticks but not double-quoted prose | Also mask `"..."` content as code | Double quotes are used legitimately in flowing prose (quoted speech, titles). Markdown backticks are unambiguous code-or-example markers. Conservative scope avoids hiding real citations. |
| Update biblatex `\nameyeardelim` despite preamble being generic | Leave as-is; let users override | The previous `\addcomma\space` is APA, not AEA. Leaving it would silently produce non-compliant output. AEA-conformant by default is the right standard for an empirical-econ template. |

## Verification Results

| Check | Result | Status |
|---|---|---|
| All 31 primary_source_lib unit tests pass | All PASS | PASS |
| Three style docs (`primary-source-first.md`, `working-paper-format.md`, `anti-ai-prose.md`) extract zero citations under the masked regex | 0 citations from all three | PASS |
| Cherry-pick clean onto applied-micro and behavioral for all four commits | No conflicts | PASS |
| All 36 origin pushes succeed | Each `git push` reports old..new | PASS (one BDD push needed `http.postBuffer=524288000` due to user's audit-sprint payload) |
| LaTeX preamble in working-paper-format.md still compiles cleanly with biblatex | Preamble syntax check passes; not yet tested in a live document | PARTIAL — recommend a live compilation test on first AEA-targeted submission |

## Learnings & Corrections

- [LEARN:hook-regex] Author-Year regexes need three independent guards to be robust: (1) explicit separator before year, (2) surname must end in a letter (no trailing punctuation), (3) code-span masking. Each one alone is insufficient against the misparse classes encountered today. Future hook hardening should anticipate that adversarial prose (e.g., quoting prior hook output) creates regress patterns the original author didn't anticipate.
- [LEARN:rule-self-enforcement] When a rule file's prose uses pedagogical example citations, the audit hook sees those examples as real citations unless they're in backticks. The convention "code = example, prose = claim" needs to be reflected in the regex preprocessing, not just in the rule's escape-hatch documentation. Otherwise every style-guide author rediscovers this trap.
- [LEARN:upstream-noncompliance] The biblatex preamble inherited from upstream was producing APA-form citations (`(Smith, 2020)`) despite being labeled AEA-aligned. Three settings were wrong. Lesson: when a downstream project claims compliance with an external standard, periodically run a side-by-side check against a live example from that standard rather than trusting inherited config.

## Open Questions / Blockers

- **Live LaTeX compilation test not yet performed.** The biblatex preamble changes (`maxcitenames`, `maxbibnames`, `\nameyeardelim`) should be verified end-to-end on at least one paper before assuming the AEA-form output renders correctly. Recommend running through a paper draft with `\citet` and `\citep` of varying author counts and inspecting the PDF.
- **Reading-notes infrastructure still empty in most projects.** The hook works correctly; the underlying corpus is what's missing. Each downstream project should populate `master_supporting_docs/literature/papers/` with the PDFs and `reading_notes/` with the per-paper notes for the load-bearing citations actually used.

## Next Steps

- None blocking. Hook is robust against three known false-positive classes. Citation style is AEA-compliant in the rule, the preamble, and the writer-critic rubric.
