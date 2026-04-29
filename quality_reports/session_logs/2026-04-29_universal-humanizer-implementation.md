# Session Log: 2026-04-29 — Universal anti-AI-prose rule + /humanize skill (lean v1)

**Status:** COMPLETED

## Objective

User asked for a universal feature that strips AI writing patterns from external-facing documents (papers, slides, READMEs, blog posts, cover letters), and explicitly raised the concern of rule/agent bloat. Goal: implement the universal feature without inflating the workflow's surface area.

## Diagnosis

Pre-flight survey of existing infrastructure:

- `writer.md` already had a "Humanizer Pass" section (24 patterns, 4 categories) — but paper-only and embedded in the agent file (not reusable).
- `/write humanize` skill mode wrapped it for paper TeX files only.
- `storyteller`, `writer-critic`, `storyteller-critic` had no anti-AI-prose layer; storyteller-critic had no anti-prose-pattern checks at all.
- Nothing applied to README, cover letter, response letter, or blog drafts.

Community survey (5 resources, full report archived in conversation):

| Resource | Borrow |
|---|---|
| Aboudjem/humanizer-skill | 37-pattern taxonomy + voice profiles + burstiness checks |
| adenaufal/anti-slop-writing | Universal-system-prompt distribution pattern |
| Wikipedia "Signs of AI writing" | Structural patterns (symmetric sectioning, promotional tone, over-explanation) |
| lmmx AI tells rubric | Severity-weighted rubric format |
| sam-paech/antislop-sampler | Empirical pattern derivation (deferred to Phase 3) |

User explicitly worried about bloat. Honest assessment: original 5-layer proposal had bloat (new agent, Phase 2 hooks). Lean v1 trimmed to: 1 rule + 1 skill + critic deduction-table additions. No new agent, no new hooks. Phases 2 and 3 deferred.

## Changes Made

Single feature commit on each of three template branches: main (`7c55ae8`), applied-micro (`391d070`), behavioral (`fe73c33`). 13 files / +448, −32 per branch. All pushed to origin (`chesun/claude-research-workflow`). Cherry-pick onto overlays required CLAUDE.md conflict resolution to preserve paradigm-specific skills tables (`/strategize`, `/balance`, `/event-study` on applied-micro; `/design`, `/theory`, `/preregister`, `/qualtrics`, `/otree` on behavioral).

| Surface | Change | What |
|---|---|---|
| `.claude/rules/anti-ai-prose.md` | NEW | Rule with ~35 patterns (6 categories: lexical, syntactic, structural, rhetorical, content, communication), severity tiers, file-glob scope (excludes internal artifacts), 5 voice profiles (academic / slide / correspondence / blog / docs), escape comment syntax, cross-references. |
| `.claude/skills/humanize/SKILL.md` | NEW | Universal `/humanize [path] [--profile] [--audit/apply]` skill. Voice profile inferred from path. Dispatches writer (paper/.tex), storyteller (talks/.tex), or generic-prose mode (.md). |
| `.claude/skills/write/SKILL.md` | MOD | Removed the `humanize` mode (now lives at `/humanize`). Backward-compat alias preserved. |
| `.claude/agents/writer.md` | MOD | Replaced inline 24-pattern Humanizer Pass section with reference to the rule. Catalog now lives in the rule, not the agent. |
| `.claude/agents/storyteller.md` | MOD | Added a Humanizer Pass section pointing at the rule with the slide voice profile. Net-new — slides previously had no anti-AI-prose layer. |
| `.claude/agents/writer-critic.md` | MOD | Added "Anti-AI-prose deductions" subsection scoring against the rule's catalog (capped at -30). Non-overlapping with existing McCloskey/Cochrane checks. |
| `.claude/agents/storyteller-critic.md` | MOD | Added slide-scoped anti-AI-prose deductions (capped at -15, advisory). |
| `.claude/rules/quality.md` | MOD | Anti-AI-prose row added to Paper LaTeX and Talks deduction tables. |
| `.claude/rules/workflow.md` | MOD | `/humanize` added to skills table. |
| `CLAUDE.md` | MOD | `/humanize` added to Skills Quick Reference. (Required manual conflict resolution on each overlay branch to preserve paradigm-specific rows.) |
| `docs/reference/skills.md` | MOD | `/humanize` row added with dispatch detail. |
| `docs/concepts/upstream-differences.md` | MOD | Documented universal anti-AI-prose rule as a fork contribution beyond Hugo's paper-only inline humanizer. |
| `quality_reports/plans/2026-04-29_universal-humanizer-feature.md` | NEW | Approved plan documenting the proposal, lean v1 scope, decisions, and deferred Phase 2/3. |

## Design Decisions

| Decision | Alternatives | Rationale |
|---|---|---|
| Promote catalog to a rule rather than keeping it inline in `writer.md` | Cross-reference between `writer.md` and `storyteller.md` instead | The catalog now serves writer + storyteller + future external-facing surfaces. A rule is the project's idiom for cross-cutting standards (`figures.md`, `tables.md`, `working-paper-format.md` are all style catalogs as rules). 27 rules vs 26 isn't where bloat bites; redundant or overlapping rules is. |
| No new humanizer agent | Standalone agent with full pattern catalog as system prompt | Writer + writer-critic + storyteller + storyteller-critic already cover the artifact-types. Adding a 10th agent splits responsibility on the same artifact and creates a layer Claude won't naturally invoke. The rule is the catalog; existing agents reference it. |
| No new hooks (defer Phase 2) | PostToolUse warn hook + Stop-hook prose audit on edit | Anti-AI-prose is stylistic — `delve` and em-dashes have legitimate uses. Hooks here would overfire on real prose, erode trust in the hook system (which the 4-rule epistemic stack hooks rely on for their authority), and be redundant with critic deductions. Revisit only if patterns persistently slip through. |
| Severity tiers (Critical / Major / Minor) with caps (-30 paper, -15 talk) | Single per-pattern deduction | Tiered + capped prevents the anti-AI-prose deductions from dominating the writer-critic score, which has other load-bearing checks (claims–evidence, identification fidelity, McCloskey/Cochrane). |
| `<!-- anti-ai-ok: <reason> -->` escape comment | Hard-ban with no override | Patterns are rebuttable presumptions. Sometimes "robust" is the right word; sometimes a paper *about* AI prose needs to quote AI prose. Escape comment is auditable (`grep -R "anti-ai-ok"`) — same architecture as `primary-source-ok` in the primary-source-first rule. |
| Cherry-pick onto applied-micro and behavioral | Apply manually to each branch | Cherry-pick is the cleanest mechanism for overlay-agnostic changes. CLAUDE.md needed manual conflict resolution on each overlay (paradigm-specific skills tables differ); otherwise the cherry-pick was clean. |

## Verification Results

| Check | Result | Status |
|---|---|---|
| New rule passes `MEMORY.md` blank-line-before-list and `\$` escape conventions | All lists preceded by blank lines; no currency `$` characters in body | PASS |
| `/humanize` skill auto-registered by harness | Showed in `available skills` list after Write | PASS |
| Writer-critic deduction subsection compiles as valid markdown | Visual scan — all table rows aligned | PASS |
| Cherry-pick onto applied-micro succeeds | Conflict in CLAUDE.md only (skills table) — resolved preserving applied-micro's paradigm-specific rows | PASS |
| Cherry-pick onto behavioral succeeds | Same — preserved `/design`, `/theory`, `/preregister`, `/qualtrics`, `/otree` paradigm-specific rows | PASS |
| All 3 branch HEADs reference the new commit | main `7c55ae8`, applied-micro `391d070`, behavioral `fe73c33` | PASS |
| All 3 origins pushed | `2c9204a..7c55ae8 main`, `6ce8544..391d070 applied-micro`, `b8c4f88..fe73c33 behavioral` | PASS |
| No leftover stale references to "/write humanize" or "24 patterns" | Grep across `.claude/`, `docs/`, `CLAUDE.md`, `README.md` returns only the expected pointers (deprecation alias in `/write`, the rule itself, the new skill) | PASS |

## Learnings & Corrections

- [LEARN:bloat-check] Before adding a new agent: ask whether existing worker-critic pairs already cover the artifact type. If yes, add the catalog/rule and have existing agents reference it — don't add a 10th agent that splits responsibility on the same artifact.
- [LEARN:hook-discipline] Hooks are load-bearing for binary-correct concerns (factual fabrication, replication failure). Stylistic concerns are rebuttable; hooks there overfire on legitimate prose and erode hook-system credibility. Use rules + critic deductions for style; reserve hooks for binary checks.
- [LEARN:cherry-pick-overlay] When cherry-picking universal changes onto paradigm-specific overlay branches (applied-micro, behavioral), expect CLAUDE.md conflicts in the Skills Quick Reference table. Resolve by keeping the overlay's paradigm-specific rows and threading the universal additions in. Other files usually merge cleanly.

## Open Questions / Blockers

- **Ship to downstream project repos?** csac, csac2025, va_consolidated, tx_peer_effects_local don't yet have the rule, skill, or critic-deduction additions. Pattern is to selectively cherry-pick from template after a feature lands. Held pending user direction.
- **Phase 2 hooks?** Deferred. Should re-evaluate after a few documents have run through `/humanize` to see if the rule + critic alone catches enough.
- **Voice-profile coverage?** v1 has 5 profiles (academic, slide, correspondence, blog, docs). Cover-letter and response-letter are folded into `correspondence` — may want to split them later if the registers diverge in practice.

## Next Steps

- None blocking. Rule + skill + critic deductions are the universal v1; the workflow now treats anti-AI-prose as a project-wide concern with a single source of truth.
