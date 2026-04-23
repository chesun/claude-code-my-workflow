# Promoting Applied-Micro to Main — Proposal

**Date:** 2026-04-23
**Question:** Main is currently a dumping ground for the initial planning docs on top of an upstream lecture template. What's the best way to promote `applied-micro` to become the primary branch?

---

## Current state

### Three branches, three purposes

| Branch | What it is | Last commit |
|---|---|---|
| `main` | Pedro Sant'Anna's upstream clo-author **lecture template** (Quarto slides, pedagogy-reviewer, slide-auditor, extract-tikz → SVG for Quarto) + Christina's 6 planning commits on top | `d4d4baf` (gitignore) |
| `applied-micro` | Christina's **research workflow** for applied micro (Stata-primary, observational data, identification). Full research pipeline agents (librarian, explorer, strategist, coder, writer, storyteller, referees) | `d0313ca` (prose port) |
| `behavioral` | Christina's **research workflow** for behavioral/experimental econ. Superset of applied-micro + theory, design, oTree, Qualtrics specialists, preregistration, domain-profile-behavioral | `e9260cf` (TODO cleanup) |

### What's on main that's NOT in applied-micro (paradigm mismatch)

- `guide/` + `docs/` — Quarto source + rendered HTML for Pedro's public guide site (`psantanna.com/claude-code-my-workflow`).
- `Quarto/`, `Figures/`, `Preambles/` — uppercase lecture convention.
- Lecture-oriented agents: `pedagogy-reviewer`, `slide-auditor`, `quarto-critic`, `quarto-fixer`, `beamer-translator`, `r-reviewer`, `proofreader`, `domain-reviewer`. All archived on applied-micro.
- Lecture-oriented skills: `create-lecture`, `translate-to-quarto`, `qa-quarto`, `pedagogy-review`, `slide-excellence`, `visual-audit`, `deploy` (Quarto → GitHub Pages).
- Lecture-oriented rules: `beamer-quarto-sync`, `knowledge-base-template`, `no-pause-beamer`, `pdf-processing`, `proofreading-protocol`.
- README — Pedro's branding + link to his live site; written for a lecture-workflow audience.
- `Bibliography_base.bib` at repo root (applied-micro uses `references.bib` in `paper/`).

### Divergence statistics

- Merge base: `396dc4e` (Christina's planning-pivot commit).
- main is **4 commits ahead** of merge base (all docs/chore on Christina's planning).
- applied-micro is **26 commits ahead** of merge base (full rebuild from Hugo's clo-author fork + all subsequent workflow development).

### Christina's fork context

- Repo is `chesun/claude-code-my-workflow` (Christina's own fork).
- Upstream: `pedrohcgs/claude-code-my-workflow` (Pedro's lecture template, actively developed — 10+ commits ahead of Christina's main).
- **GitHub Pages is not active** on Christina's fork (checked via `gh api /pages` → 404). Replacing main will NOT break any live site.
- Christina has no PRs merged into Pedro's upstream; her branches are her own.

---

## Goal

"Make main the primary research workflow." Specifically, main should be what a forker lands on, and that landing surface should be the research workflow — not Pedro's lecture template.

Open sub-questions (to decide before executing):

- **Should main be applied-micro-identical, or a stripped-down "universal research template" from which both applied-micro and behavioral derive?** Today applied-micro and behavioral differ only in paradigm-specific adds (theorist, designer, oTree, qualtrics, etc. for behavioral). A universal main would need to abstract these out, which is more work.
- **Do you want to keep receiving Pedro's upstream updates?** If main diverges fully, pulling from `upstream/main` becomes an exercise in cherry-picking rather than merging.
- **Should behavioral also become "primary"?** Or remain a specialized overlay branch?

---

## Five options

### Option A — Hard replace main with applied-micro (recommended)

Force-reset main to applied-micro's tree. Archive current main on a side branch for reference / future upstream merges.

```bash
# Step 1: preserve Pedro's lecture template for posterity
git checkout main
git branch main-lecture-archive     # snapshot before we overwrite

# Step 2: reset main to applied-micro
git reset --hard applied-micro

# Step 3: force-push both
git push origin main --force-with-lease
git push origin main-lecture-archive
```

**Pros:**

- Simple. Main is the research template.
- `main-lecture-archive` preserves the upstream state — if Pedro ships a useful feature, you can still cherry-pick from there or from `upstream/main` onto the archive branch and selectively port.
- Clean history from the research-workflow perspective.
- Forkers landing on main see the research template immediately.

**Cons:**

- Destructive to main's history (force-push). Since this is Christina's fork only (no downstream collaborators), this is recoverable but still warrants the archive branch as a safety net.
- Future upstream merges from Pedro become manual cherry-picks rather than clean merges.
- Pedro's README branding on main gets replaced. You'll want to rewrite README with Christina's framing (see below).

### Option B — Merge applied-micro into main (preserves history)

Standard flow: PR from applied-micro → main, resolve conflicts, merge.

**Problem:** applied-micro removes ~90% of what's on main (Quarto, guide, lecture agents/skills/rules, uppercase folders). A standard merge would produce a commit that deletes that content. It's viable but verbose.

Practical shortcut using `-s ours` or `-X theirs`:

```bash
git checkout main
git merge applied-micro -X theirs    # prefer applied-micro on any conflict
# then manually stage file deletions for content that should go
```

**Pros:**

- Preserves linear history on main.
- No force-push required.

**Cons:**

- Merge commit becomes a massive "rewrote everything" diff — less readable than Option A's archive-branch-plus-reset.
- Still loses Pedro's README/guide integrity; you end up with a zombie merge commit.
- Conflict resolution for ~90% of files is tedious.

### Option C — Make main a minimal router; keep branches as primaries

Replace main's content with a tiny README that says:

> This template has two variants: `applied-micro` (observational data, identification) and `behavioral` (experiments, theory, preregistration). Pick your branch.

Plus a `.gitignore` and LICENSE. Everything else lives on the two branches.

**Pros:**

- Honest: there isn't a single universal research template today — it's really two.
- Minimal force-push blast.

**Cons:**

- Forkers land on an empty-ish main and have to choose a branch before they see anything useful.
- Breaks the fork-and-go model Pedro's README promotes.
- Probably more friction than value.

### Option D — Re-fork: this repo becomes research-only

Create a separate repo for any lecture work (copy current main → a new `claude-code-lecture-template` repo), then hard-replace main here with applied-micro.

**Pros:**

- Cleanest separation. If you ever care about the lecture template, it has its own home.

**Cons:**

- Requires managing two repos.
- Overkill if you don't actively do lecture work (which, given you haven't touched main's lecture content and main has no live Pages site, looks like the case).

### Option E — Rename applied-micro → main; keep main as an archive

Delete `main` branch and rename `applied-micro` → `main`:

```bash
git branch -m applied-micro main
git push -d origin applied-micro
git push -u origin main --force-with-lease
```

**Pros:**

- Fast.
- `applied-micro` disappears as a branch (no redundancy).

**Cons:**

- Forkers who had tracked `applied-micro` get surprised (not applicable here — no downstream forkers).
- Cross-branch work between applied-micro and behavioral loses its natural name-pair.
- You'd need to re-create `applied-micro` as a separate overlay branch anyway if you plan continued per-paradigm divergence.

---

## Recommendation

**Option A + README rewrite**, in that order:

1. Archive current main: `git branch main-lecture-archive` (no force-push needed yet).
2. Reset main to applied-micro: `git reset --hard applied-micro` + `git push --force-with-lease`.
3. Rewrite README on main to reflect Christina's framing — what the template is, who it's for (empirical social-science researchers), how to choose between behavioral and applied-micro overlays, credit Pedro + Hugo as base template sources.
4. Keep `applied-micro` and `behavioral` as overlay branches. Going forward, work on the overlay branches for paradigm-specific changes; universal improvements land on main and get merged/rebased into both overlays.
5. Optionally: merge `upstream/main` → `main-lecture-archive` occasionally to keep track of Pedro's upstream in case anything useful appears there (e.g., new Claude Code feature incorporation).

Why Option A over B/C/D/E:

- Clean, understandable result. Forkers land on the research template.
- Archive branch is a cheap insurance policy against losing anything useful from Pedro's upstream.
- Doesn't force a tooling split (Option D) or a confusing router-main (Option C).
- Retains `applied-micro` as a named branch (unlike E) for future paradigm-specific work.

---

## Things to resolve before executing

1. **README rewrite scope.** Do you want to (a) write a completely new research-workflow README, (b) adapt Pedro's and replace lecture-specific sections with research-workflow sections, or (c) leave the existing README for now and update later?
2. **Keep `main-lecture-archive`, or fully delete main's old history?** My default: keep the archive branch (costless, salvageable).
3. **What to do with the planning-doc commits on main** (`80d5daa`, `396dc4e`, `0131495`, `45613d5`, `48c970e`, `d4d4baf`)? They're currently on main and would be lost unless cherry-picked onto the archive. These are mostly superseded (plans executed, gitignore already in applied-micro). My default: drop — they live in reflog if ever needed.
4. **Keep following `upstream/main` (Pedro)?** Worth deciding explicitly. If yes, you occasionally want to cherry-pick from `upstream/main` onto the archive and back to main. If no, set `upstream` remote to disabled / stale.
5. **Behavioral as a named overlay or also promoted?** My default: keep behavioral as a named overlay branch. If you want a single-paradigm setup you can always rename it later.

---

## Estimated effort

- ~5 min: branch archive + reset + force-push
- ~20–40 min: README rewrite (depending on scope — option (c) is 0 min)
- ~10 min: verify behavioral still rebases cleanly onto the new main (it should; behavioral's recent commits are all additive or applied to files that will now exist identically on main)
- **Total:** ~20 min minimum (skip README), ~60 min max (full README rewrite)

Safe to proceed after decisions on the 5 questions above.
