# Primary-Source-First

**Scope (file-level):** `decisions/**/*.md`, `experiments/designs/**/*.md`, `theory/**/*.{tex,md}`, `quality_reports/advisor_meeting_*/**`, `quality_reports/session_logs/**`, `quality_reports/plans/**`, `quality_reports/reviews/**`, `quality_reports/*_analysis.md`

**Scope (prose):** all assistant conversation text in the session

**Enforcement:**

- `.claude/hooks/primary-source-check.py` (PreToolUse, `Edit|Write`) — blocks edits to scoped files.
- `.claude/hooks/primary-source-audit.py` (Stop) — blocks turn-end when session prose contains un-grounded citations.

Before making a framing claim about an external paper — in a file edit OR in conversation text — consult the primary source. Derivative docs and paraphrases lose precision; downstream claims propagate the error silently.

## Three enforced failure modes

1. **Notes don't exist AND the PDF is in the repo.** Blocks with "read the PDF, write notes." The remediation is to use the `pdf-learnings` skill on long papers or the `Read` tool with `pages=` on short ones, then produce a notes file per `master_supporting_docs/literature/reading_notes/README.md`. If `pdf-learnings` fails on an unusually long or problematic file, see `.claude/references/pdf-chunking.md` for a Ghostscript-based fallback recipe.

2. **Notes don't exist AND the PDF is NOT in the repo.** Blocks with "add the PDF first." A citation you cannot ground in a primary source does not belong in a load-bearing artifact. The remediation is to add the PDF to `master_supporting_docs/literature/papers/` (naming it with the surname-year convention so the hook can find it), then produce notes.

3. **Notes exist but were not touched in this session.** Blocks with "Read the notes file before citing." This is the guard against working from cached context. Touching (Read / Write / Edit) a notes file in the current session is the evidence; a prior session's Read does not persist — sessions are fresh contexts.

## Where the two hooks apply

- **PreToolUse hook** — scans the *delta* (new_string for Edit, content for Write) of every Edit/Write to a scoped file path. Fires on each tool call; blocks the call.
- **Stop hook** — scans *all assistant prose* in the session transcript at turn-end. Fires on Stop; blocks the turn-end. Catches claims made in conversation that never went to a tool call. Respects `stop_hook_active` to avoid loops (blocks at most once per turn).

Both hooks share citation-detection and notes-verification logic in `.claude/hooks/primary_source_lib.py`.

## What counts as a reading-notes file

Either form is accepted by the hook:

1. A **per-paper file** named with the citation stem: `smith_jones_2024.md`, `angrist_pischke_2009.md`, etc.
2. A **section inside a compiled reading-notes file** that includes a `**Citation:** ...` metadata line naming the paper's authors and year. The hook matches on the citation line specifically, so compiled files must use this format for the hook to recognize them.

Per-paper files are preferred for load-bearing references. Compiled files are acceptable for batch reading sprints.

**Why citation-line-only (not section-header) matching:** documents like the reading-notes README or conceptual memos may mention a paper in a header without being notes about it. The `**Citation:** Author (Year)...` line is the reliable signal that "this section is reading notes for this paper."

## Required sections in a reading-notes file

The `README.md` in `master_supporting_docs/literature/reading_notes/` specifies the canonical structure. The load-bearing section for preventing derivative-doc drift is:

> **What this paper is NOT claiming (common misreadings)**

Use this section to head off future conflation errors. When downstream docs (ADRs, analysis memos, hypotheses, session logs) have previously misframed the paper, record the misreading and the corrected reading side-by-side.

## Citation extraction — the filter stack

The hook extracts citations via an Author-Year regex, then applies a filter stack in order:

1. **Built-in blocklist (`NEVER_SURNAMES`).** Hard-coded set of words that are *never* surnames in academic prose: function words ("the", "in", "from"), seasons, months, days of the week, document-structure words ("table", "figure", "section", "panel", "cohort"), pronouns, role-placeholder words used in citation-style examples ("Author", "Coauthor", "Editor"), book/series-title nouns ("Handbook", "Journal", "Review", "Volume"), mixed-case ADR/workflow status words ("Decided", "Superseded", "Pending", ...), changes-table verbs ("Added", "Fixed", "Merged", ...), software/tool/product names ("Stata", "Qualtrics", "Overleaf", "Photoshop", ...), document-lifecycle nouns ("Draft", "Version", "Meeting", ...), institution/program/legislation/dataset nouns ("Census", "Medicaid", "Act", "Bank", "Commission", "Compustat", "Datastream", ...), and calendar/event/award nouns ("Quarter", "Semester", "Cup", "Prize", "Medal", holidays, ...). These drop regardless of allowlist state. Collision-risk words that ARE real surnames ("Grant", "Law", "Bill", "Nielsen") are deliberately excluded — they are handled by the org skip-list or escape hatch instead.

1b. **Org skip-list (`.claude/state/primary_source_orgs.txt`).** Optional per-project list (same loader/format as the surname allowlist) of mixed-case corporate/data authors to skip ("Gallup", "Pew", Nielsen-the-company). These can't go in `NEVER_SURNAMES` safely because one project's data vendor is another project's cited author. Missing/empty file = no skipping.

1c. **Preceding-token cue filter.** A named-entity cue word ("Hurricane Katrina (2005)") or an all-caps acronym immediately before the head token ("NSF Grant 2026", "EEA-ESEM Rotterdam 2026"), separated by whitespace only, marks the match as a named entity and skips it — unless the head surname is explicitly allowlisted. Punctuation between acronym and name breaks the cue, so `IPUMS USA (Ruggles et al. 2024)` still extracts.

2. **All-caps token filter.** A captured surname written entirely in uppercase (length ≥ 2) is rejected. Real surnames in academic prose are written `Smith`, never `SMITH`; real two-letter surnames (`Ng`, `Wu`, `Li`) are written mixed-case. Catches status markers (`COMPLETED (2026)`, `WIP (2026)`) and acronym corporate authors (`BLS (2024)`, `OECD (2023)`, `EU (2024)`, `AY 2026`). Corporate-author citations are *data* attributions, not framing claims about research papers, so they don't require reading notes. Mixed-case surnames (`McGregor`, `DeAngelo`, `O'Brien`) still match.

3. **Sentence-start / structural-boundary filter.** A capitalized first word right after a sentence terminator (`.?!:;` or paragraph break) **or at a markdown structural boundary — line start, bullet, numbered item, heading, blockquote, table cell —** is dropped *unless* it appears in the project allowlist. This kills the dominant false-positive class in workflow docs (person + year in TODO tables, standup bullets, session-log lines) while a real citation in those positions still extracts once the surname is allowlisted. Mid-sentence prose citations are unaffected.

4. **Hyphenated-name decomposition.** A 3+ part hyphenated capitalized token (e.g., `Chetty-Friedman-Rockoff`) is split into separate surnames and the stem is built with underscores (`chetty_friedman_rockoff_2014`). This matches reading-notes filename conventions. Two-part hyphenated tokens (`Goldsmith-Pinkham`) are preserved as single hyphenated surnames since real hyphen-containing surnames are common.

5. **Project allowlist (`.claude/state/primary_source_surnames.txt`).** Optional, one lowercase surname per line. When the file is empty or missing, all matches that pass the earlier filters are accepted. Populated allowlists tighten the filter further — only Author-Year matches whose leading surname is in the allowlist extract — and rescue real citations at structural boundaries (filter 3) and after cue tokens (filter 1c). Recommended: populate as you accumulate cited authors.

### Structural guards in the regex itself (before any filter)

- **ISO-date/range guard.** A year immediately followed by dash/slash + digit is the leading component of a date or range, not a citation year — `Kickoff 2026-09-01`, `Snapshot 2026/07/15`, `Coverage 2019–2021` never extract. This kills the "CapitalizedWord YYYY-MM-DD" class generically, including words no blocklist enumerates.
- **Full author-list capture.** The author list is captured as one repeated span and split in Python, so comma-only lists (`Bohren, Imas, Rosenberg (2019)`) and the AEA 4-author form (`Smith, Jones, Brown, and Lee (2024)`) extract with the lead author intact at any author count. (The earlier 3-slot pattern restarted mid-list and silently dropped the lead author.)

### Unicode and typographic handling

The extractor ASCII-folds text before matching (NFD-decompose + strip combining marks, plus a precomposed-letter map for `ł ø ß æ œ ð þ`), so accented surnames (`Székely`, `García`, `Müller`, `Bénabou`, `Łukasz`) match as their ASCII forms. Typographic characters are folded too: curly quotes/apostrophes → ASCII apostrophe, en/em-dash → hyphen, NBSP → space — so curly-apostrophe surnames and en-dash compounds no longer mis-parse to the wrong author. Possessives are normalized (`Chetty's (2014)` → `chetty_2014`; `Smith et al.'s (2020)` and `Smith and colleagues (2020)` extract), and stems are apostrophe-free (`O'Brien` → `obrien_2020`) to match filename conventions. Reading-notes filenames should use ASCII, apostrophe-free stems — `szekely_rizzo_2013.md`, `obrien_2020.md`. The notes/PDF lookups also try a hyphen→underscore stem fallback, so a 2-part hyphenated dual-author citation (stem `szekely-rizzo_2013`) resolves to the conventional underscore filename, and accented `**Citation:**` metadata lines are folded before matching.

### Known residue (by design)

Bare place-name + year (`Tokyo 2020`), titles that are also surnames, and mixed-case polling orgs are irreducible by syntax — the org skip-list or escape hatch handles them. Particle surnames (`van Reenen`, `de Chaisemartin`) build stems without the lowercase particles; name the notes file by the extracted stem or rely on the `**Citation:**`-line match, which resolves regardless of filename.

## Escape hatch

If you need to cite a paper *without* making a new framing claim (e.g., fixing a typo in an existing sentence that happens to cite the paper; referring to a paper as a test case or example without claiming anything about its content), include an override comment:

```
<!-- primary-source-ok: smith_jones_2024, angrist_pischke_2009 -->
```

Hyphenated stems (e.g., `chetty-friedman-rockoff_2014`) are supported — the parser uses a non-greedy match terminated by `-->` so hyphens inside stems don't truncate the list. Comments may also span multiple lines:

```
<!-- primary-source-ok:
  smith_jones_2024,
  chetty-friedman-rockoff_2014,
  goldsmith-pinkham_2020
-->
```

- For PreToolUse (file edits): include the comment in the delta.
- For the Stop audit (conversation prose): include the comment in the same assistant message as the citation.

The comment only applies to the scope where it appears — it is not session-wide. Abuse is auditable: `grep -R "primary-source-ok" master_supporting_docs/ quality_reports/ experiments/ theory/` surfaces every use.

## Citation-style convention (AEA / Chicago author-date)

The project uses the AEA reference style. Per the AER style guide, "Text citations and reference list entries should follow author-date style (see *Chicago Manual of Style*)." AER specifies the et al. threshold; everything else inherits from Chicago author-date. This applies to all in-text citations in load-bearing artifacts: paper, talks, ADRs, plans, reviews, session logs, response letters, and any external-facing prose.

References: https://www.aeaweb.org/journals/aer/style-guide (AER style — et al. thresholds), https://www.aeaweb.org/journals/policies/sample-references (sample reference entries), https://www.aeaweb.org/journals/data/references (data citations).

### In-text citation form

AER explicitly states: "1–4 authors: include all author names" and "5+ authors: list only the name of the first author followed by 'et al.'"

| Authors | Form | Examples |
|---|---|---|
| 1 | `Author (year)` or `(Author year)` | `Smith (2020)`; `(Smith 2020)` |
| 2 | `Author and Author (year)` — never `&`, never comma-separated | `Roth and List (2022)`; `Healy and Leo (2024)`; `(Romer and Romer 2010)` |
| 3 | `Author, Author, and Author (year)` — Oxford comma required | `Gaduh, Hanna, and Olken (2021)`; `Smith, Jones, and Brown (2020)` |
| 4 | `Author, Author, Author, and Author (year)` — all four listed, Oxford comma | `Smith, Jones, Brown, and Lee (2024)` |
| 5+ | `First-author et al. (year)` from first cite onward; reference list shows more (see below) | `Smith et al. (2024)` |
| Same author, same year | suffix-disambiguate with lowercase letter | `Smith (2020a)`, `Smith (2020b)` — order matches the reference list |

### Multiple works in one parenthetical

Use semicolons between works; chronological order within author, alphabetical between authors:

- `(Smith 2020; Jones 2021; Brown 2022)`
- `(Smith 2020a, 2020b; Jones 2021)` — same-author works comma-separated within their cluster

### Punctuation and form details

- Always `and` between names; never `&` in running text. The ampersand belongs in tables and footnotes only when journal style permits, and AEA does not.
- Always include the period in `et al.` (Latin abbreviation requires it).
- Year in parentheses when the author is part of the running sentence (`Smith (2020) shows...`); year inside the parenthetical when the whole citation is parenthetical (`...is shown elsewhere (Smith 2020).`).
- No comma between author and year in the parenthetical form: `(Smith 2020)`, not `(Smith, 2020)`. Chicago author-date omits the author-year comma; this distinguishes it from APA.

### Reference list form (AEA / Chicago)

The reference list itself is rendered by `biblatex` with `style=authoryear` per `working-paper-format.md`. AER specifies: "Reference list entries with one to ten authors should include all author names; for eleven or more authors, list the first seven, followed by a comma and 'et al.'" Note this is laxer than the in-text et al. threshold — the reference list shows up to 10 authors before truncating, while in-text uses et al. at 5+.

Manual reference entries follow Chicago author-date form:

- **Journal article:** `Author, FirstName M., and FirstName M. Author. Year. "Title of Article." Journal Name Volume (Issue): Pages.`
- **Book:** `Author, FirstName M. Year. Title in Italics. City: Publisher.`
- **Working paper:** `Author, FirstName M. Year. "Title." Series Name Working Paper No. NNNN.`
- **Edited volume chapter:** `Author, FirstName M. Year. "Chapter Title." In Volume Title, edited by FirstName M. Editor, pages. City: Publisher.`
- **Dataset:** `Author. Year. Title in Italics, Version. Database. Publisher. URL or DOI (accessed date).`

Authors after the first list given-name first within a single entry: `Smith, John A., Jane Doe, and Mary Roe.` (Oxford comma between Doe and Roe).

### Why this matters for the hook

The Author-Year regex in `primary_source_lib.py` is permissive on the parser side — it still detects `&`-form, comma-form, and various malformed citations so that no real citation slips past the audit. But the writing convention is strict: prose that follows AEA form produces no false positives, never invokes the escape hatch, and ports cleanly to AEA submission without retroactive rewrites. The writer-critic enforces AEA form via deduction rows (see `agents/writer-critic.md`).

### One-author and corporate-author cases

- **Single author:** `Author (year)` or `(Author year)`.
- **Corporate / institutional author:** spell out on first mention, abbreviate thereafter — `(Bureau of Labor Statistics 2024)`, then `(BLS 2024)` with the abbreviation introduced parenthetically on first use.
- **Anonymous / no author:** use a short form of the title in italics — `(Title in Italics 2020)`.
- **Forthcoming:** use `forthcoming` in place of the year — `Smith (forthcoming)`.

## Why this exists

Claude has, in prior projects, propagated an incorrect framing claim about a paper through multiple load-bearing documents — a decision log, an identification analysis, a session log, and a slide review — without ever opening the PDF despite it being in the repo the whole time. The error originates in a paraphrase, gets amplified across derivative docs, and each downstream claim inherits and amplifies the distortion.

The rule exists to make this failure mode deterministically catchable rather than relying on the model to remember to open the primary source. Three failure modes — missing notes with PDF present, missing notes with no PDF, existing notes not consulted in-session — are each paths the failure could have been caught; the hooks make all three deterministically blocking.

## Intended behavior

When content cites a paper — whether in a file edit or in conversation prose — the hooks either:

- Allow (notes exist AND were consulted this session), or
- Block with a clear remediation path: read the PDF (or add it first if missing), produce notes, touch the notes file in this session, re-run.

The rule is not a suggestion. It fires deterministically. The only way through without notes is the escape hatch, which is auditable.
