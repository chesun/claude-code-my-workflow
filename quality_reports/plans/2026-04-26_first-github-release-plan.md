# First GitHub Release Plan — `claude-code-my-workflow`

**Status:** DRAFT (awaiting your approval)
**Date:** 2026-04-26
**Repo:** `chesun/claude-code-my-workflow`
**Target version:** `v0.1.0` (pre-release)

---

## TL;DR — recommended approach

**One release, tagged on `main`, marked as pre-release.**

- Tag: `v0.1.0` on `main`
- Release title: `v0.1.0 — Claude Code research workflow (preview)`
- Release type: pre-release (checkbox in GitHub UI), since this is the first public version and the API may evolve
- Overlays (`applied-micro`, `behavioral`) are documented in the release notes as branches users `git checkout` after cloning. They do NOT get separate releases at this stage.

Why this and not three releases: a "release" in GitHub is fundamentally a tagged snapshot of one commit. Three releases of the same version would just create UI confusion ("Latest" badge will pick whichever sorts last). Branches are how overlays are already designed — point users at them in the README + release notes. If you later want overlay snapshots, you can add `v0.1.0-applied-micro` / `v0.1.0-behavioral` tags and let GitHub auto-create releases for them, but don't do that for the first release.

---

## Why a release at all

You have a working workflow that other researchers can fork. A GitHub Release does three things:

1. **Pins a known-good snapshot.** "v0.1.0" is forever — even if `main` keeps moving, anyone can `git checkout v0.1.0` and get the exact tree you released.
2. **Gives a landing page.** GitHub renders a Release page with notes, downloads, and a stable URL you can share (in papers, emails, slides).
3. **Generates downloadable archives** (`.zip`, `.tar.gz`) automatically, so non-git users can just download.

If you don't want a landing page yet — if this is mostly a personal config you happen to keep in public — skip releases entirely and just keep pushing to `main`. Releases are for when you want to communicate "this is a published thing."

---

## Step-by-step (CLI route — recommended for reproducibility)

These steps assume you already have `gh` (GitHub CLI) installed and authenticated. If not: `brew install gh && gh auth login`.

### 1. Decide the version

`v0.1.0` is right for a first preview. Reasoning: SemVer says `0.x.y` = "no API stability promise." Save `v1.0.0` for when you're confident the rule/skill/agent contracts won't change in a breaking way for users who have forked. Don't start at `v1.0.0` — it sets a stability expectation you don't yet want to commit to.

### 2. Decide the commit to tag

Tag the current `main` HEAD: `3064d9d`. That includes all the recent hook fixes. If you want to wait for any other in-flight changes, tag later.

### 3. Tag locally

```bash
cd ~/github_repos/claude-code-my-workflow
git checkout main
git tag -a v0.1.0 -m "v0.1.0 — first preview release"
```

`-a` makes it an annotated tag (has author + date + message). Lightweight tags are valid but not idiomatic for releases.

### 4. Push the tag

```bash
git push origin v0.1.0
```

This is what makes the tag visible on GitHub. Without this push, the tag exists only locally.

### 5. Write release notes

I've drafted release notes below — they go in step 6. Tweak as needed. Save them to a file (e.g. `/tmp/release-notes-v0.1.0.md`) so you can reference them in the `gh` command.

### 6. Create the release

```bash
gh release create v0.1.0 \
  --repo chesun/claude-code-my-workflow \
  --title "v0.1.0 — Claude Code research workflow (preview)" \
  --notes-file /tmp/release-notes-v0.1.0.md \
  --prerelease
```

`--prerelease` is the "this is a preview, not a stable release" flag. Drop it for `v1.0.0` later.

### 7. Verify on GitHub

Visit `https://github.com/chesun/claude-code-my-workflow/releases`. You should see the v0.1.0 entry with the notes you wrote and auto-generated `Source code (zip)` and `Source code (tar.gz)` download buttons.

---

## Step-by-step (web UI route — same outcome, more clicking)

If you'd rather use the website:

1. Push the tag locally first (steps 1–4 above).
2. Go to `https://github.com/chesun/claude-code-my-workflow/releases`.
3. Click **Draft a new release**.
4. **Choose a tag:** pick `v0.1.0` (the one you just pushed).
5. **Target:** `main` (auto-filled because the tag is on main).
6. **Release title:** `v0.1.0 — Claude Code research workflow (preview)`.
7. **Describe this release:** paste the release notes (below).
8. Check **Set as a pre-release**.
9. Click **Publish release**.

---

## Draft release notes (copy into GitHub)

```markdown
# v0.1.0 — Claude Code research workflow (preview)

A Claude Code workflow for empirical economics research. Plan-first
implementation, paired worker–critic agents, primary-source-first hooks,
and a single-source-of-truth paper-centric protocol.

This is a **preview release** (`0.x` = no API-stability promise).
Expect changes to rule scopes, skill names, and agent contracts before
`v1.0.0`. Forking is welcome; pinning to this tag will give you a
known-good snapshot you can rely on while the trunk evolves.

## Branches and overlays

The workflow ships in three flavors. Pick the one that matches your
research style after cloning:

| Branch          | Use when                                                 |
|-----------------|----------------------------------------------------------|
| `main`          | General-purpose / cross-paradigm work (default)          |
| `applied-micro` | Observational-data identification-strategy research      |
| `behavioral`    | Experimental, theoretical, or behavioral research        |

```bash
git clone https://github.com/chesun/claude-code-my-workflow.git
cd claude-code-my-workflow
git checkout applied-micro   # or behavioral, or stay on main
```

Overlays add paradigm-specific skills (`/strategize`, `/balance`,
`/event-study` on `applied-micro`; `/design`, `/theory`, `/preregister`
on `behavioral`) on top of the universal trunk.

## What's included

- **Skills** (`.claude/skills/`): `/discover`, `/analyze`, `/write`,
  `/review`, `/revise`, `/talk`, `/submit`, `/challenge`, `/tools`, plus
  paradigm-specific skills on overlays.
- **Agents** (`.claude/agents/`): worker–critic pairs (writer +
  writer-critic, coder + coder-critic, etc.) plus orchestrator + verifier.
- **Rules** (`.claude/rules/`): single-source-of-truth, primary-source-first,
  quality scoring (>= 80 to commit, >= 95 to submit), figure/table
  conventions for AER/QJE/Econometrica visual standards.
- **Hooks** (`.claude/hooks/`): primary-source-check, primary-source-audit,
  context-monitor (with PreCompact auto-compact-bypass fallback —
  see [#14111](https://github.com/anthropics/claude-code/issues/14111)),
  log-reminder, verify-reminder.
- **Templates** (`templates/`): session log, quality report,
  requirements spec.

## Requirements

- Claude Code (tested with `2.1.119`).
- Python 3.10+ for hook scripts.
- LaTeX (pdflatex or xelatex) for paper compilation; `biber` for biblatex.
- Stata 17+, R, or Python — depending on which language you use.

## Quick start

1. Fork or clone this repo.
2. Pick a branch (see table above).
3. Fill in the `[BRACKETED PLACEHOLDERS]` in `CLAUDE.md`.
4. Run `/discover interview [topic]` to scope a research project, or
   `/new-project [topic]` for the orchestrated full pipeline.

## Acknowledgements

Forked from [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow).

## Known limitations

- Claude Code's `PreCompact` hook can silently bypass on auto-compact
  when MCP servers are loaded ([anthropics/claude-code#14111](https://github.com/anthropics/claude-code/issues/14111)).
  This release works around it via a `context-monitor.py` PostToolUse
  fallback that snapshots state at 90% context.
- `MAX_TOOL_CALLS=500` heuristic in `context-monitor.py` is calibrated
  for Opus 4.7 1M-context. Set
  `CONTEXT_MONITOR_MAX_TOOL_CALLS` to override per project.
```

---

## What NOT to do for a first release

- **Don't** also create `v0.1.0-applied-micro` and `v0.1.0-behavioral` tags. It clutters the Releases page; the branch model already covers overlay distribution. Add overlay tags only if you later see actual demand.
- **Don't** ship `v1.0.0` as the first version. SemVer says `1.0.0` is a stability commitment.
- **Don't** attach binary assets you'd have to maintain by hand. Let GitHub auto-generate the source-code archives — that's all you need.
- **Don't** push the tag *before* you're sure the tagged commit is what you want — tags are pushed by name and rewriting them after release is awkward (you have to delete locally + on remote, retag, repush, and downstream forkers don't see the update).
- **Don't** forget the `--prerelease` flag (or the equivalent checkbox) on the first release. Drop it once you're comfortable freezing the API around v1.0.0.

---

## After release: maintenance pattern

Going forward, the natural pattern is:

| Trigger | Bump |
|---|---|
| Bug fix in a rule/skill/agent | patch (`v0.1.1`) |
| New skill or new rule | minor (`v0.2.0`) |
| Breaking change to existing rule/skill/agent contract | minor while in `0.x.y` (`v0.3.0`); major once at `v1.0.0` |

Each bump = a new tag + a new GitHub Release with notes describing what changed. Keep release notes user-facing ("the `/review` skill now accepts `--code` for code-only mode") rather than commit-list-y.

---

## Decision points for you

Before I do anything, please confirm:

1. **Are you OK releasing a fork publicly?** Your remotes show `upstream = pedrohcgs/claude-code-my-workflow`. The release notes credit the upstream, which is the right thing — but if you intended this fork to stay personal, no release is needed.
2. **Tag commit confirmed as `3064d9d` (current main HEAD)?** Or do you want any in-progress work landed first?
3. **Pre-release flag — yes/no?** I recommend yes. If you'd rather it show up as the project's "Latest" badge on GitHub, we omit `--prerelease`.
4. **Do you want me to execute steps 3–6 once you say go?** Or do you want to run them yourself for the learning experience?

---

## Verification after release

Once published, sanity-check:

- [ ] Tag visible at `github.com/chesun/claude-code-my-workflow/tags`
- [ ] Release page renders notes correctly
- [ ] `Source code (zip)` download contains `.claude/`, `templates/`, `CLAUDE.md`
- [ ] Cloning and `git checkout v0.1.0` lands on commit `3064d9d`
- [ ] README on `main` (if any) links to the Releases page
