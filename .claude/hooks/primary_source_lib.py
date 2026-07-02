"""
Shared logic for the primary-source-first enforcement hooks.

Two hooks use this:

- primary-source-check.py (PreToolUse on Edit|Write): blocks edits to
  load-bearing files that cite papers lacking reading-notes evidence.
- primary-source-audit.py (Stop): scans assistant text in the session
  transcript and blocks the turn-end if citations in prose lack notes
  evidence.

Both rely on the same citation-detection, notes-existence, and
session-read-verification logic, which lives here.

Project-agnostic. The surname allowlist is loaded at import time from
`.claude/state/primary_source_surnames.txt` (one lowercase surname per
line). If the file is missing or empty, the allowlist is skipped and
every Author-Year match is accepted. An org skip-list is loaded the same
way from `.claude/state/primary_source_orgs.txt` (mixed-case corporate/
data authors to skip). See `.claude/rules/primary-source-first.md`.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from pathlib import Path
from typing import Iterable


# File paths where primary-source enforcement applies. Template-generic —
# scoped to in-repo load-bearing artifacts. Overleaf paper .tex files live
# outside the repo and are not reachable by the PreToolUse hook.
ENFORCEABLE_PATTERNS = [
    r"decisions/.*\.md$",
    r"experiments/designs/decisions/.*\.md$",
    r"experiments/designs/.*\.md$",
    r"theory/.*\.(tex|md)$",
    r"quality_reports/advisor_meeting_[^/]+/.*\.(tex|md)$",
    r"quality_reports/session_logs/.*\.md$",
    r"quality_reports/plans/.*\.md$",
    r"quality_reports/reviews/.*\.md$",
    r"quality_reports/[^/]+_analysis\.md$",
]


def _load_state_wordlist(filename: str) -> set[str]:
    """Load a lowercase one-name-per-line word list from `.claude/state/`.

    Looks up the file under CLAUDE_PROJECT_DIR if set, otherwise relative
    to this library file. Returns an empty set if the file is missing or
    empty — callers treat empty as "mechanism inactive". Lines starting
    with `#` are comments.
    """
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        path = Path(project_dir) / ".claude" / "state" / filename
    else:
        path = Path(__file__).resolve().parent.parent / "state" / filename
    if not path.is_file():
        return set()
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return set()
    words: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        words.add(line.lower())
    return words


# Surname allowlist: when non-empty, only Author-Year matches whose leading
# surname appears here are accepted. Empty (the day-one default) = accept
# all matches that pass the other filters.
KNOWN_SURNAMES = _load_state_wordlist("primary_source_surnames.txt")

# Org skip-list: mixed-case corporate/data authors to skip ("Gallup", "Pew",
# Nielsen-the-company). These can't go in NEVER_SURNAMES safely (Nielsen is
# a common surname), so the skip is per-project state — one project's data
# vendor is another project's cited author. Missing/empty file = no skipping.
ORG_SKIPLIST = _load_state_wordlist("primary_source_orgs.txt")

# Author-Year regex. Matches:
#   Chakraborty and Kendall (2025)
#   Chakraborty & Kendall 2025
#   Danz, Vesterlund, and Wilson (2024)
#   Karni (2009)
#   Brown et al. (2025)
#
# Two coupled constraints prevent the original "shorthand-coalescing" misparse:
#
# 1. **Surname char class ends in a letter.** `[A-Z][A-Za-z\-']*[A-Za-z]`
#    instead of the laxer `[A-Z][A-Za-z\-']+`. Real surnames never end in
#    `-` or `'`. Without the trailing-letter anchor, greedy matching captured
#    `second = "Eyting-"` (trailing hyphen) from inputs like `Eyting-2024`
#    or quoted hook output like `Eyting- (2024)`. Anchoring on a letter at
#    the end forces `second = "Eyting"` and leaves the stray punctuation
#    for the year-separator check to reject.
#
# 2. **Year requires explicit separator before it.** `(?:\s+\(?|\(|,\s*\(?)`
#    before `year` — at least one of whitespace, open-paren, or comma. Real
#    citations always have one of these (`Smith (2020)`, `Smith 2020`,
#    `Smith, 2020`); the inline shorthand `Smith-2020` does not.
#
# Together, these block the original false-positive case
# (`Cameron-Miller, Eyting-2024` → stem `cameron-miller_eyting-_2024`)
# AND the residual case where my own prose quoted the hook's parsed string
# `Cameron-Miller and Eyting- (2024)` (which after the year-separator fix
# alone still parsed because ` (` is a valid separator). Constraint 1
# prevents `Eyting-` from being captured at all.
#
# 3. **Year must not open a full date or range.** `(?![-–—/]\d)` after the
#    year digits rejects matches where the "year" is really the leading
#    component of an ISO date (`Kickoff 2026-09-01`), a slashed date
#    (`2026/07/15`), or a dash range (`2019–2021`). Real citation years are
#    never immediately followed by dash/slash + digit. This kills the whole
#    "CapitalizedWord YYYY-MM-DD" false-positive class structurally —
#    including words no blocklist will ever enumerate.
#
# 4. **Author list is a single repeated group, split in Python.** The old
#    pattern had exactly three author slots (`first`/`second`/`third`) with
#    the third requiring an Oxford `", and"`. Comma-only lists
#    (`Bohren, Imas, Rosenberg (2019)`) and the AEA 4-author form
#    (`Smith, Jones, Brown, and Lee (2024)`) didn't fit, so the match
#    anchored at the lead author FAILED and the regex restarted mid-list —
#    silently dropping the lead author (`imas_rosenberg_2019`,
#    `jones_brown_lee_2024`). Capturing the whole list as one span and
#    splitting on `,`/`and`/`&` in `extract_citations` handles any author
#    count and keeps the lead author as the head that filters apply to.
#
# 5. **Possessive and "and colleagues" forms reach the year.** `et al.` may
#    carry a possessive (`Smith et al.'s (2020)` — curly apostrophes are
#    folded to ASCII before the regex runs), and `Author and colleagues
#    (year)` / `Author and coauthors (year)` are standard prose citation
#    forms. Without these alternations the lowercase word after `and` (or
#    the `'s` after `al.`) broke the year-separator path and a load-bearing
#    framing claim escaped the hook entirely. Bare-name possessives
#    (`Chetty's (2014)`) already match via the surname char class (they end
#    in the letter `s`) and are stripped in `extract_citations`.
AUTHOR_YEAR = re.compile(
    r"""
    \b
    (?P<authors>
        [A-Z][A-Za-z\-']*[A-Za-z]
        (?:(?:\s*,\s*(?:and\s+)?|\s+and\s+|\s*&\s*)[A-Z][A-Za-z\-']*[A-Za-z])*
    )
    (?:\s+et\s+al\.?(?:'s)?|\s+and\s+(?:colleagues|coauthors))?
    (?:\s+\(?|\(|,\s*\(?)(?P<year>(?:19|20)\d{2})(?![-–—/]\d)[a-z]?\)?
    """,
    re.VERBOSE,
)

# Splits a captured author-list span into individual surname tokens.
# Mirrors the separator alternation inside AUTHOR_YEAR.
AUTHOR_SEP = re.compile(r"\s*(?:,\s*(?:and\s+)?|\s+and\s+|\s*&\s*)\s*")

# Escape hatch: <!-- primary-source-ok: stem1, stem2 -->
# Use non-greedy `.+?` with the explicit `-->` terminator so stems containing
# hyphens (e.g., `chetty-friedman-rockoff_2014`) are not truncated. The earlier
# `[^-]+` pattern stopped at the first hyphen, silently dropping any stems
# listed after a hyphen-containing one.
ESCAPE_HATCH = re.compile(
    r"<!--\s*primary-source-ok:\s*(?P<stems>.+?)\s*-->",
    re.IGNORECASE | re.DOTALL,
)

# Sentence-boundary detector. A capitalized first word right after a sentence
# terminator is almost never a surname citation; it's just the next sentence.
#
# Markdown-aware: the documents this hook scopes (session logs, plans,
# reviews, TODO tables) are full of person-name + year in structural slots
# the old `.?!:;` + blank-line pattern could not see — table cells
# (`| Kramer 2026 | done |`), bullet items (`- Kramer (2026) reviewed`),
# headings (`## Kramer 2026 review`), blockquotes (`> Sun (2026) approved`),
# and plain line starts after a single newline. Those positions now count
# as sentence-start too, so they require the surname allowlist to extract —
# the same tradeoff sentence-start already makes, and real prose citations
# are overwhelmingly mid-sentence. Recognized boundaries:
#   - sentence terminator + whitespace (unchanged)
#   - line start (single `\n` or start-of-string) followed by any run of
#     markdown decorations: bullets (- * +), numbered-list markers
#     (`1.` / `1)`), heading #s, blockquote >, table pipes, bold/emphasis
#     markers (* _ ~)
#   - a mid-line table-cell pipe (`| `)
SENTENCE_BOUNDARY = re.compile(
    r"""(?:
        [.?!:;]\s+
      | (?:\n|\A)[ \t]*
        (?:(?:[-*+>#|]+|\d{1,3}[.)])[ \t]*|[*_~]{1,3})*
      | \|[ \t]*
    )\s*$""",
    re.VERBOSE,
)

# Preceding-token cue: some false-positive classes are marked not by the
# matched head token (which may be a real or unenumerable name — "Katrina",
# "Grant", "Rotterdam") but by the word immediately BEFORE it:
#
#   Hurricane Katrina (2005)     — named-storm natural-experiment phrasing
#   NSF Grant 2026               — funding acknowledgment ("Grant" is a real
#                                  surname, so blocklisting it is unsafe)
#   EEA-ESEM Rotterdam 2026      — conference acronym + host city
#
# When the token directly preceding the author match (separated by plain
# spaces/tabs only — any intervening punctuation like `(` or `,` breaks the
# cue, so parenthetical citations after acronyms, e.g. "IPUMS USA (Ruggles
# et al. 2024)", are untouched) is either a named-entity cue word or an
# all-caps acronym, the match is skipped. Like the sentence-start filter,
# an explicit allowlist entry for the head surname overrides the skip.
NAMED_ENTITY_CUES = frozenset({
    "hurricane", "typhoon", "cyclone", "storm", "tropical",
})

# Token (plus trailing space/tab run) immediately before the match start.
_CUE_BEFORE = re.compile(r"(\S+)[ \t]+$")

# All-caps acronym shape: 2+ chars, uppercase letters/digits, internal
# hyphens/ampersands allowed ("NSF", "UK", "EEA-ESEM", "AT&T"). A trailing
# period or comma on the preceding token deliberately fails the match —
# sentence-final acronyms are handled by the sentence-start filter instead.
_ACRONYM_TOKEN = re.compile(r"^[A-Z][A-Z0-9&-]*[A-Z0-9]$")

# Words that are *never* surnames. Applied independent of the project allowlist
# so the hook is reasonable on day one (when the allowlist is empty). Keep this
# list conservative — only words with effectively zero chance of being a real
# surname in academic prose.
NEVER_SURNAMES = frozenset({
    # Articles, demonstratives, copulae
    "the", "a", "an", "this", "these", "those", "that",
    # Prepositions
    "in", "on", "at", "from", "for", "to", "by", "with", "of",
    # Pronouns
    "we", "our", "us", "i", "you", "your", "he", "she", "they", "their", "it", "its",
    # Quantifiers
    "all", "some", "most", "both", "each", "every", "any", "no", "none",
    # Adverbs / discourse markers
    "only", "also", "even", "still", "yet", "however", "moreover",
    "additionally", "furthermore", "thus", "therefore", "hence",
    "meanwhile", "instead", "rather", "indeed",
    # Adjectives commonly capitalized at sentence start
    "available", "important", "notable", "key", "main", "primary",
    "significant", "relevant", "specific", "general",
    # Question / subordinator words
    "when", "where", "why", "how", "what", "which", "who", "whose",
    "if", "unless", "until", "while", "since", "because", "although",
    "despite", "given", "based", "using", "according", "see",
    "though", "before", "after",
    # Seasons
    "spring", "summer", "fall", "autumn", "winter",
    # Days of the week
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    # Months
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    # Document-structure words
    "table", "figure", "panel", "column", "row", "section", "appendix",
    "chapter", "footnote", "equation", "model", "specification",
    "step", "stage", "phase", "round", "wave", "cohort", "year", "yr",
    "note", "notes",
    # Role-words used as placeholders in citation-style examples
    # ("Author and Author (year)", "Coauthor (year)", etc.)
    "author", "authors", "coauthor", "coauthors", "co-author", "co-authors",
    "editor", "editors", "name", "names", "surname", "surnames",
    # Book/series-title nouns that frequently appear capitalized adjacent to
    # a year and false-positive as surnames. Common pattern: "Handbook of
    # Experimental Methodology, 2025" or "Annual Review of Economics 2024".
    "methodology", "methodologies", "handbook", "handbooks", "encyclopedia",
    "review", "reviews", "annual", "bulletin", "bulletins",
    "journal", "journals", "volume", "volumes", "issue", "issues",
    # ADR / workflow status words. These appear capitalized right before an
    # ISO date ("Decided 2026-06-03", "Superseded by #0020 (2026)") in ADR
    # headers and in prose that quotes them. The all-caps filter catches
    # COMPLETED/DRAFT-style markers but not these mixed-case status words.
    "decided", "proposed", "superseded", "supersedes", "pending",
    "resolved", "updated", "revised", "committed", "delivered", "drafted",
    "status", "deferred", "open",
    # Changes-table verbs. Table cells and changelog lines routinely open
    # with a capitalized verb followed by a date-like string ("Added
    # 2026-07-01", "Fixed (2026)"). The ISO-date guard in AUTHOR_YEAR
    # catches the full-date forms; these entries catch the bare-year forms.
    "added", "new", "fixed", "removed", "inserted", "replaced", "changed",
    "extended", "deleted", "dropped", "copied", "merged", "patched",
    # Software / platform / tool / product names (mixed-case, so the
    # all-caps filter can't catch them). "Stata (2023)", "RStudio (2023)",
    # "Windows 2000", "Claude (2025)" — tool-vintage attributions, never
    # surnames in academic prose.
    "stata", "matlab", "python", "qualtrics", "prolific", "overleaf",
    "github", "dropbox", "beamer", "latex", "excel", "rstudio", "tableau",
    "windows", "office", "unicode", "claude", "gemini",
    "zotero", "mendeley", "jupyter", "docker",
    "photoshop", "illustrator", "powerpoint",
    # Document-lifecycle nouns. The changes-table cluster above has the
    # *verbs*; these are the nouns ("Draft (2026)", "Version (2026)",
    # "Meeting (2026)", "NBER Summer Institute 2025").
    "draft", "version", "release", "update", "plan", "memo", "meeting",
    "seminar", "conference", "workshop", "agenda", "milestone",
    "deliverable", "submission", "deadline",
    # Institutions, programs, legislation, surveys, datasets, rooms.
    # "CARES Act (2020)", "World Bank (2024)", "Medicaid (2022)",
    # "American Community Survey (2022)", "Head Start (2019)", "Suite
    # 2026", "Compustat (2024)". "Dodd-Frank" is the two-part hyphenated
    # statute name filter 4 preserves as a single surname. Deliberately
    # NOT blocklisted (real surnames): Grant, Law, Bill, Nielsen.
    "university", "institute", "center", "committee", "congress", "census",
    "medicare", "medicaid", "act", "bank", "reserve", "survey", "study",
    "start", "room", "suite", "form", "dodd-frank", "compustat",
    "datastream", "refinitiv",
    # Institution / title tail nouns in the same never-a-surname cluster
    # ("European Commission (2023)", "Census Bureau (2024)", "Panel Study
    # of Income Dynamics (2021)", "World Development Indicators (2023)").
    "commission", "council", "agency", "bureau", "administration",
    "department", "foundation", "association", "organization",
    "dynamics", "indicators",
    # Calendar / event / award nouns adjacent to years: "Spring Quarter
    # 2026", "Labor Day 2026", "UK Budget 2026", "World Cup (2022)",
    # "Euro 2024", "Nobel Prize (2023)", "Sloan Fellowship (2024)",
    # "Brexit (2016)". Weekday names are blocked above but bare "Day"
    # ("Labor Day 2026") was not.
    "quarter", "day", "days", "budget", "cup", "euro", "prize",
    "fellowship", "brexit", "covid", "omicron",
    "semester", "trimester", "medal",
    "thanksgiving", "christmas", "easter", "halloween",
})


def _is_sentence_start(text: str, pos: int) -> bool:
    """True if `pos` is at start-of-document or right after a sentence terminator."""
    if pos == 0:
        return True
    return bool(SENTENCE_BOUNDARY.search(text[:pos]))


def _stem_token(token: str) -> str:
    """Lowercase and strip apostrophes for stem-building and list lookups.

    Reading-notes filenames are conventionally apostrophe-free
    (`obrien_2020.md`), and `paper_pdf_exists_for` tokenizes filenames on
    non-alphanumerics, so a stem containing `'` (`o'brien_2020`) could
    never match a filename token — PDF lookup unfixably failed. Stripping
    at stem-build time (and symmetrically in the lookup functions) makes
    both ends agree.
    """
    return token.lower().replace("'", "")


def _split_hyphenated_surname(token: str) -> list[str]:
    """If token has 3+ hyphen-separated capitalized name-like parts, split it.

    Used to handle method-name compounds like `Chetty-Friedman-Rockoff` that
    appear as a single hyphenated token but represent multiple surnames. A
    properly-named reading-notes file uses underscores, so the split lets the
    extractor build the right stem.

    Returns a single-element list (the original token) if the heuristic
    doesn't apply.
    """
    parts = token.split("-")
    if len(parts) < 3:
        return [token]
    if all(p[:1].isupper() and p[1:].isalpha() and len(p) >= 2 for p in parts):
        return parts
    return [token]

# Markdown section-header / citation-metadata line patterns for matching
# compiled reading-notes files.
HEADER_LINE = re.compile(r"^\s*#{1,6}\s+")
CITATION_LINE = re.compile(r"^\s*\*\*Citation", re.IGNORECASE)


def is_enforceable(rel_path: str) -> bool:
    """True if the file path is load-bearing for primary-source enforcement."""
    return any(re.search(p, rel_path) for p in ENFORCEABLE_PATTERNS)


# Precomposed Latin letters with no combining-mark NFD decomposition.
# Covers the cases that matter for academic econ citations (Polish stroke,
# Nordic ø, German ß, French/Old English ligatures, Icelandic eth/thorn).
_PRECOMPOSED_MAP = str.maketrans({
    "ł": "l", "Ł": "L",
    "ø": "o", "Ø": "O",
    "ß": "ss",
    "æ": "ae", "Æ": "Ae",
    "œ": "oe", "Œ": "Oe",
    "ð": "d", "Ð": "D",
    "þ": "th", "Þ": "Th",
})

# Typographic characters that break the ASCII-only regex char classes or the
# stem conventions. Curly apostrophes abort a match mid-name ("O’Brien
# (2020)" parsed as brien_2020 — wrong author); en/em-dashes break the
# hyphenated-compound handling ("Goldsmith–Pinkham (2020)" dropped the lead
# surname); NBSP masquerades as a space the char classes can't see. Folding
# to ASCII keeps the ISO-date guard effective — it already keys on the ASCII
# hyphen (and retains the en/em-dash forms as defense in depth).
_TYPOGRAPHIC_MAP = str.maketrans({
    "‘": "'", "’": "'",  # curly single quotes / apostrophe
    "“": '"', "”": '"',  # curly double quotes
    "–": "-", "—": "-",  # en-dash, em-dash
    " ": " ",                 # no-break space
})


def _ascii_fold(text: str) -> str:
    """NFD-decompose, strip combining marks, then map precomposed letters.

    "Székely" → "Szekely", "García-Pérez" → "Garcia-Perez", "Müller" →
    "Muller", "Łukasz" → "Lukasz". The AUTHOR_YEAR char classes are
    ASCII-only, so an accented character mid-name previously aborted the
    match and the regex restarted after it — "Székely-Rizzo 2013" parsed
    as rizzo_2013 (wrong author, wrong stem), and the hook then demanded
    a notes file that will never exist. Reading-notes filenames already
    use ASCII stems, so folding before extraction makes both ends agree.

    Also folds typographic characters (curly quotes → ASCII apostrophe,
    en/em-dash → hyphen, NBSP → space) via _TYPOGRAPHIC_MAP — see the
    comment there for the wrong-author bugs this fixes.
    """
    nfd = unicodedata.normalize("NFD", text)
    stripped = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return stripped.translate(_PRECOMPOSED_MAP).translate(_TYPOGRAPHIC_MAP)


def _mask_code_spans(text: str) -> str:
    """Replace inline-code and code-fenced content with same-length whitespace.

    Citations inside backticks are pedagogical examples — citation-form syntax
    in style guides, rule documentation, and tutorial prose — not framing
    claims about real papers. The convention in Markdown is that backtick-
    wrapped content is code or syntax, not a claim about external work.
    Skipping them eliminates a large recurring class of false positives.

    Same-length whitespace preserves character offsets so the sentence-start
    filter's `match.start()` still resolves correctly against the original
    text positions.

    Two forms are masked:
    - Triple-backtick code fences (``````...``````) including any internal
      newlines (DOTALL).
    - Single-backtick inline-code spans (`...`) within a single line.

    Real citations are written in flowing prose without backticks; this mask
    does not affect them.
    """
    def _whitespace_replacement(m: "re.Match[str]") -> str:
        # Preserve newlines so line-based sentence-boundary heuristics still work
        return "".join(c if c == "\n" else " " for c in m.group(0))

    text = re.sub(r"```.*?```", _whitespace_replacement, text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", _whitespace_replacement, text)
    return text


def extract_citations(text: str) -> list[tuple[str, str]]:
    """Return list of (stem, display) tuples for citations in text.

    Applies six filters in order:

    0. **Code-span mask** — content inside Markdown inline-code (`...`) or
       code fences (``````...``````) is replaced with same-length whitespace
       before the regex runs. Style-guide examples like `` `Smith (2020)` ``
       are pedagogical, not framing claims, so they should not trigger the
       audit.
    1. **NEVER_SURNAMES blocklist** — words that are never surnames
       (function words, seasons, months, table/figure/etc.). Drops the
       match regardless of allowlist state.
    1a. **All-caps token filter** — captured surnames written in all
       uppercase (length >= 2) are rejected. Real surnames in academic
       prose are written `Smith`, never `SMITH`. This catches status
       markers (`COMPLETED (2026)`, `DRAFT (2025)`, `DONE (2024)`,
       `BLOCKED (2026)`, `ACTIVE (2026)`, `TODO (2026)`, `FIXME (2026)`,
       `WIP (2026)`, `PENDING (2025)`) and acronym corporate authors
       (`BLS (2024)`, `OECD (2023)`, `USDA (2025)`, `EU (2024)`,
       `AY 2026`). Corporate-author data citations are not framing
       claims about research papers, so they don't require reading
       notes. Real two-letter surnames (`Ng`, `Wu`, `Li`) are written
       mixed-case in prose, never `NG`, so the length-2 floor is safe.
    1b. **Org skip-list** — mixed-case corporate/data authors the project
       has declared non-paper sources (`.claude/state/
       primary_source_orgs.txt`: "Gallup", "Pew"). Same mechanics as the
       surname allowlist, opposite polarity. Missing/empty file = no
       skipping.
    1c. **Preceding-token cue** — a named-entity cue word ("Hurricane
       Katrina (2005)") or an all-caps acronym ("NSF Grant 2026",
       "EEA-ESEM Rotterdam 2026") immediately before the head token,
       separated by whitespace only, marks the match as a named entity.
       Skipped unless the head surname is explicitly allowlisted.
    2. **Hyphenated-name decomposition** — if the captured `first` group
       is a 3+ part hyphenated capitalized token (e.g.,
       "Chetty-Friedman-Rockoff"), split it and treat each part as a
       surname. Builds an underscore-joined stem matching reading-notes
       filename conventions. Runs before the sentence-start check so
       that sentence-start hyphenated compounds can be tested against
       the allowlist using the decomposed head.
    3. **Sentence-start filter** — a capitalized first word right after a
       sentence terminator OR a markdown structural boundary (line start,
       bullet, numbered item, heading, blockquote, table cell — see
       SENTENCE_BOUNDARY) is dropped unless the project allowlist
       explicitly contains the (possibly-decomposed) head. Sentence-
       start function-word + year is almost never a citation, and
       person-name + year in structural slots (TODO tables, standup
       bullets) is almost never a citation either.
    4. **Allowlist filter** — if KNOWN_SURNAMES is non-empty, the leading
       surname must appear in it. If empty (default for new projects),
       all matches that pass filters 1–3 are accepted.

    Captured tokens are possessive-normalized (`Chetty's` → `Chetty`) and
    stems are apostrophe-normalized (`O'Brien` → `obrien`) so that stems
    always match the apostrophe-free reading-notes filename convention.
    """
    text = _mask_code_spans(_ascii_fold(text))
    citations: list[tuple[str, str]] = []
    seen: set[str] = set()
    allowlist_active = bool(KNOWN_SURNAMES)

    for match in AUTHOR_YEAR.finditer(text):
        authors_span = match.group("authors") or ""
        year = match.group("year") or ""

        # Defense in depth: strip possessives and trailing hyphens/apostrophes
        # from surname captures. Real surnames don't end in `-` or `'`, and a
        # possessive (`Chetty's (2014)`) would otherwise swallow the `'s` into
        # the stem so a correctly-named `chetty_2014.md` no longer matches the
        # startswith check — a spurious block on a legitimate citation.
        names: list[str] = []
        for n in AUTHOR_SEP.split(authors_span):
            if not n:
                continue
            if n.endswith("'s"):
                n = n[:-2]
            n = n.rstrip("-'")
            if n:
                names.append(n)
        if not names:
            continue
        first, rest = names[0], names[1:]

        # Filter 1: hard-coded blocklist — independent of allowlist
        if _stem_token(first) in NEVER_SURNAMES:
            continue

        # Filter 1a: all-caps tokens (length >= 2) are status markers
        # (COMPLETED, DRAFT, DONE, BLOCKED, PENDING, ACTIVE, TODO, FIXME, WIP)
        # or acronym corporate authors (BLS, OECD, USDA, EU, AY). Real
        # surnames in academic prose are never written ALL-CAPS (two-letter
        # surnames appear as `Ng`, never `NG`); corporate-author citations
        # are data attributions, not framing claims about research papers,
        # so they don't require reading notes.
        if len(first) >= 2 and first.isupper():
            continue

        # Filter 1b: project org skip-list — mixed-case corporate/data
        # authors ("Gallup", "Pew") that the project has declared non-paper
        # sources. Skips regardless of position; empty/missing file = off.
        if _stem_token(first) in ORG_SKIPLIST:
            continue

        # Filter 1c: preceding-token cue — named-entity cue words
        # ("Hurricane Katrina (2005)") and all-caps acronym precursors
        # ("NSF Grant 2026", "EEA-ESEM Rotterdam 2026") mark the head token
        # as part of a named entity, not a citation. Whitespace-only
        # separation required; an explicit allowlist entry for the head
        # surname overrides (same escape as the sentence-start filter).
        prev = _CUE_BEFORE.search(text[: match.start()])
        if prev is not None:
            prev_token = prev.group(1)
            if prev_token.lower() in NAMED_ENTITY_CUES or (
                len(prev_token) >= 2 and _ACRONYM_TOKEN.match(prev_token)
            ):
                if not (allowlist_active and _stem_token(first) in KNOWN_SURNAMES):
                    continue

        # Filter 2: hyphenated-name decomposition (handles method compounds)
        # Runs BEFORE the sentence-start check so that sentence-start hyphenated
        # compounds like "Chetty-Friedman-Rockoff (2014)" can be tested against
        # the allowlist using the decomposed head, not the full hyphenated form.
        first_parts = _split_hyphenated_surname(first)

        # Filter 3: sentence-start positions require explicit allowlist match
        # on the head of the (possibly-decomposed) compound.
        if _is_sentence_start(text, match.start()):
            head = _stem_token(first_parts[0])
            if not (allowlist_active and head in KNOWN_SURNAMES):
                continue

        # Filter 4: allowlist + surname collection
        if len(first_parts) > 1:
            # Decomposed compound; treat each part as a surname slot
            all_parts = first_parts + rest
            if allowlist_active:
                if _stem_token(first_parts[0]) not in KNOWN_SURNAMES:
                    continue
                surnames = [p for p in all_parts if _stem_token(p) in KNOWN_SURNAMES]
            else:
                surnames = all_parts
        else:
            # Standard allowlist filter
            if allowlist_active:
                if _stem_token(first) not in KNOWN_SURNAMES:
                    continue
                surnames = [s for s in [first] + rest if _stem_token(s) in KNOWN_SURNAMES]
            else:
                surnames = [first] + rest

        if not surnames:
            continue

        # Apostrophe-normalized stem (`O'Brien` -> obrien) — see _stem_token.
        stem = "_".join(_stem_token(s) for s in surnames) + "_" + year
        # Use comma+and form so the display string round-trips through this
        # same extractor: a space-joined "Chetty Friedman Rockoff (2014)"
        # would be re-parsed as "Rockoff (2014)" alone (the regex doesn't
        # recognize space as a multi-author separator). Comma+and is what
        # the regex's `,/and/&` separator alternation actually accepts.
        if len(surnames) == 1:
            display = f"{surnames[0]} ({year})"
        elif len(surnames) == 2:
            display = f"{surnames[0]} and {surnames[1]} ({year})"
        else:
            display = ", ".join(surnames[:-1]) + f", and {surnames[-1]} ({year})"

        if stem not in seen:
            seen.add(stem)
            citations.append((stem, display))
    return citations


def extract_escaped_stems(text: str) -> set[str]:
    """Return lower-cased citation stems named in escape-hatch comments."""
    escaped: set[str] = set()
    for match in ESCAPE_HATCH.finditer(text):
        raw = match.group("stems")
        for stem in (s.strip().lower() for s in raw.split(",")):
            if stem:
                escaped.add(stem)
    return escaped


def matching_notes_files(stem: str, reading_notes_dir: Path) -> list[Path]:
    """Return all reading-notes files that match the citation stem.

    Match conditions:
    1. Filename starts with the citation stem (case-insensitive) — a
       dedicated per-paper file like `chakraborty_kendall_2025.md`.
    2. A citation-metadata line in the file references all of the stem's
       surnames and the year. Recognized citation-metadata forms:
       - Markdown: lines starting with `**Citation:**` or `**Citation:** ...`
       - YAML frontmatter: lines starting with `citation:` in the top block

    Section-header matching alone (e.g., `## 9. Chakraborty & Kendall 2025`)
    is NOT accepted, because documents like the reading-notes README or
    conceptual memos may mention the paper in a header without being notes
    about it. The `**Citation:**` line is the stronger signal of "this is
    reading notes for this paper."
    """
    if not reading_notes_dir.is_dir():
        return []

    # Apostrophe normalization: stems built by extract_citations are already
    # apostrophe-free, but escape-hatch stems or older callers may pass
    # `o'brien_2020`. Strip on both sides (stem here, filename/citation-line
    # below) so either convention resolves.
    stem_lower = stem.lower().replace("'", "")
    # Hyphen→underscore fallback: a 2-part hyphenated dual-author citation
    # (`szekely-rizzo_2013`) conventionally maps to an underscore-separated
    # filename (`szekely_rizzo_2013.md`). Accept either form on the filename
    # check, and split surname tokens on both separators so the citation-line
    # pattern matches regardless of which convention the notes file uses.
    # If a project has BOTH `goldsmith-pinkham_2020.md` and
    # `goldsmith_pinkham_2020.md`, both match — the hook only needs existence.
    stem_underscored = stem_lower.replace("-", "_")
    parts = stem_lower.split("_")
    if len(parts) < 2:
        return []
    year = parts[-1]
    surnames = [t for s in parts[:-1] for t in s.split("-") if t]
    if not surnames:
        return []

    surname_pattern = r"\b" + r"\b.*\b".join(re.escape(s) for s in surnames) + r"\b"
    citation_match_pattern = re.compile(
        surname_pattern + r".*" + re.escape(year),
        re.IGNORECASE,
    )

    matches: list[Path] = []
    for f in reading_notes_dir.glob("*.md"):
        if f.name.lower().replace("'", "").startswith((stem_lower, stem_underscored)):
            matches.append(f)
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            if not CITATION_LINE.match(line):
                continue
            # Fold the line so accented citation metadata ("**Citation:**
            # Székely-Rizzo (2013)") matches the ASCII surname pattern, and
            # strip apostrophes so "O'Brien" matches the apostrophe-free
            # stem surname `obrien`.
            if citation_match_pattern.search(_ascii_fold(line).replace("'", "")):
                matches.append(f)
                break
    return matches


def notes_exist_for(stem: str, reading_notes_dir: Path) -> bool:
    """True if at least one reading-notes file matches the citation stem."""
    return bool(matching_notes_files(stem, reading_notes_dir))


def paper_pdf_exists_for(stem: str, papers_dir: Path) -> bool:
    """True if a PDF matching the citation stem is in the papers dir.

    Matches by tokenizing filenames on non-alphanumeric characters. A
    filename matches if all of the stem's surnames and the year appear
    as distinct tokens. This is robust to filename conventions that use
    underscores (which would defeat \\b word boundaries because `_` is a
    word character in regex).
    """
    if not papers_dir.is_dir():
        return False

    # Apostrophe normalization — same reasoning as matching_notes_files.
    stem_lower = stem.lower().replace("'", "")
    parts = stem_lower.split("_")
    if len(parts) < 2:
        return False
    year = parts[-1]
    # Split surnames on hyphens too: filename tokens are split on all
    # non-alphanumerics, so a hyphenated stem surname (`szekely-rizzo`)
    # could never equal a single filename token.
    surnames = {t for s in parts[:-1] for t in s.split("-") if t}
    if not surnames:
        return False

    for f in papers_dir.glob("*.pdf"):
        # Strip apostrophes before tokenizing so `o'brien_2021.pdf` yields
        # the token `obrien`, not `o` + `brien`.
        tokens = set(re.split(r"[^a-z0-9]+", _ascii_fold(f.name.lower()).replace("'", "")))
        tokens.discard("")
        if year in tokens and surnames.issubset(tokens):
            return True
    return False


# ---------------------------------------------------------------------------
# Session-transcript inspection
# ---------------------------------------------------------------------------


def iter_transcript_events(transcript_path: Path) -> Iterable[dict]:
    """Yield each JSONL event from the session transcript (fail-safe)."""
    if not transcript_path.is_file():
        return
    try:
        with transcript_path.open(encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


TOUCH_TOOLS = {"Read", "Write", "Edit"}


def notes_touched_in_session(transcript_path: Path) -> set[str]:
    """Return the set of absolute file paths touched (Read/Write/Edit) this session.

    Writing or editing a file counts as having consulted it — the author
    knows its contents at least as well as a reader does. Only Read is
    required for passive consultation.
    """
    touched: set[str] = set()
    for event in iter_transcript_events(transcript_path):
        msg = event.get("message", {}) or {}
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use":
                continue
            if block.get("name") not in TOUCH_TOOLS:
                continue
            file_path = (block.get("input", {}) or {}).get("file_path", "") or ""
            if file_path:
                try:
                    touched.add(str(Path(file_path).resolve()))
                except (ValueError, OSError):
                    continue
    return touched


def notes_read_in_session(
    stem: str,
    reading_notes_dir: Path,
    transcript_path: Path,
) -> bool:
    """True iff a reading-notes file matching the citation was touched this session.

    "Touched" = Read, Write, or Edit on the notes file. Writing a notes file
    is equivalent to having read it (author knows the content).
    """
    if not transcript_path.is_file():
        return False
    matches = matching_notes_files(stem, reading_notes_dir)
    if not matches:
        return False
    touched = notes_touched_in_session(transcript_path)
    return any(str(f.resolve()) in touched for f in matches)


def extract_assistant_text(transcript_path: Path) -> str:
    """Concatenate all assistant-message text in the session transcript."""
    texts: list[str] = []
    for event in iter_transcript_events(transcript_path):
        if event.get("type") != "assistant":
            continue
        msg = event.get("message", {}) or {}
        content = msg.get("content", [])
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    texts.append(block.get("text", "") or "")
        elif isinstance(content, str):
            texts.append(content)
    return "\n".join(texts)


def extract_tool_use_inputs(transcript_path: Path) -> str:
    """Concatenate the string-valued fields of all tool_use inputs in the transcript.

    Escape-hatch comments placed inside a file edit (Edit's new_string,
    Write's content) appear in the transcript as part of a tool_use block,
    not an assistant text block. Scanning here makes them visible to the
    audit hook, so a user who scoped the escape hatch to the edit does not
    also have to repeat it in prose.
    """
    texts: list[str] = []
    for event in iter_transcript_events(transcript_path):
        if event.get("type") != "assistant":
            continue
        msg = event.get("message", {}) or {}
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use":
                continue
            tool_input = block.get("input", {}) or {}
            if not isinstance(tool_input, dict):
                continue
            for value in tool_input.values():
                if isinstance(value, str):
                    texts.append(value)
    return "\n".join(texts)


# ---------------------------------------------------------------------------
# Block-message construction
# ---------------------------------------------------------------------------


def describe_missing_status(
    stem: str,
    reading_notes_dir: Path,
    papers_dir: Path,
    transcript_path: Path | None,
) -> str | None:
    """Return a one-line status string for a missing citation, or None if OK.

    Three possible statuses:
    - "MISSING_NOTES_NO_PDF": paper not in repo at all.
    - "MISSING_NOTES_PDF_EXISTS": PDF is present but no notes written.
    - "NOTES_NOT_READ_IN_SESSION": notes exist but weren't opened this session.
    - None: the citation is satisfied.
    """
    if not notes_exist_for(stem, reading_notes_dir):
        if paper_pdf_exists_for(stem, papers_dir):
            return "MISSING_NOTES_PDF_EXISTS"
        return "MISSING_NOTES_NO_PDF"
    if transcript_path is not None:
        if not notes_read_in_session(stem, reading_notes_dir, transcript_path):
            return "NOTES_NOT_READ_IN_SESSION"
    return None


def build_block_message(
    context_description: str,
    missing: list[tuple[str, str, str]],
    rule_path: str = ".claude/rules/primary-source-first.md",
) -> str:
    """Build the human-readable block message from a list of missing citations.

    `missing` is a list of (stem, display, status) tuples where status is
    one of the strings returned by describe_missing_status.
    """
    lines = [
        "PRIMARY-SOURCE-FIRST: blocking.",
        "",
        context_description,
        "",
    ]

    by_status: dict[str, list[tuple[str, str]]] = {}
    for stem, display, status in missing:
        by_status.setdefault(status, []).append((stem, display))

    if by_status.get("MISSING_NOTES_PDF_EXISTS"):
        lines.extend(
            [
                "The following papers have PDFs in master_supporting_docs/literature/papers/",
                "but no corresponding reading-notes file in master_supporting_docs/literature/reading_notes/:",
                "",
            ]
        )
        for stem, display in by_status["MISSING_NOTES_PDF_EXISTS"]:
            lines.append(f"  - {display}  (expected notes stem: {stem})")
        lines.extend(
            [
                "",
                "Fix: read each PDF (use the pdf-learnings skill for long papers),",
                "then produce a reading-notes file following the template in",
                "master_supporting_docs/literature/reading_notes/README.md",
                "",
            ]
        )

    if by_status.get("MISSING_NOTES_NO_PDF"):
        lines.extend(
            [
                "The following papers are cited but have neither a PDF in",
                "master_supporting_docs/literature/papers/ nor a reading-notes file:",
                "",
            ]
        )
        for stem, display in by_status["MISSING_NOTES_NO_PDF"]:
            lines.append(f"  - {display}  (expected stem: {stem})")
        lines.extend(
            [
                "",
                "Fix: add the PDF to master_supporting_docs/literature/papers/ (name it",
                "with the surname(s) and year so the hook can find it, e.g.",
                "Smith_Jones_2024_something.pdf), then read it and produce a",
                "reading-notes file. A citation you cannot ground in a primary source",
                "does not belong in a load-bearing project artifact.",
                "",
            ]
        )

    if by_status.get("NOTES_NOT_READ_IN_SESSION"):
        lines.extend(
            [
                "The following papers have reading-notes files that exist but were",
                "NOT opened with the Read tool in this session:",
                "",
            ]
        )
        for stem, display in by_status["NOTES_NOT_READ_IN_SESSION"]:
            lines.append(f"  - {display}  (stem: {stem})")
        lines.extend(
            [
                "",
                "Fix: open the corresponding reading-notes file in",
                "master_supporting_docs/literature/reading_notes/ with the Read tool",
                "before making this claim. Cached context from prior sessions or",
                "derivative docs is not a substitute — the session-scoped Read is the",
                "mechanism by which this hook verifies you actually consulted the notes.",
                "",
            ]
        )

    lines.extend(
        [
            "Escape hatch (only when editing around an existing citation without",
            "making a new framing claim about it): add a comment to the delta or",
            "to a recent message:",
            "    <!-- primary-source-ok: stem1, stem2 -->",
            "",
            f"Rule: {rule_path}",
        ]
    )

    return "\n".join(lines)
