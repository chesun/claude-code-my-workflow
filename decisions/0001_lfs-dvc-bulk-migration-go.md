# ADR-0001 — D6 pilot exit: GO for bulk LFS (+ selective DVC) migration

**Date:** 2026-07-03
**Status:** Decided
**Data quality:** Full context
**Scope:** Infrastructure — data storage & versioning *(outside the research-paradigm scope lists in `decisions/README.md`; this ADR governs the workflow repo's own infrastructure per the dual-nature rule in `.claude/rules/meta-governance.md`)*
**Sources:** `quality_reports/plans/2026-05-05_lfs-dvc-migration-plan.md` §6.6 (exit criteria) + §8 (bulk migration); session logs `2026-06-23_dvc-pilot-push-completion.md` and `2026-07-01_citation-guard-regex-hardening.md` (§ propagation — PDF conversion + ratification); BDD `data/CHANGELOG.md` entries 2026-06-23 and 2026-07-03; BDD commits `eab28aa`, `5f20370`, `5c5da3b`, `ba03924`.

---

## Decision

**GO** for bulk migration of the remaining research repos, per plan §8, with the conditions in § Conditions below:

1. **Git LFS for paper PDFs becomes the standard in every research repo** (ratified by Christina 2026-07-03: "the standard for PDFs going forward"). Conversion method: forward-only `git add --renormalize`-style conversion — no history rewrite, no coauthor-history disruption — as proven in the pilot.
2. **DVC remains selective, not blanket**: enable only in repos meeting the `data-version-control.md` opt-in criteria (evolving data + a real need for version-checkout semantics). Candidate list per plan §8: `belief_distortion_discrimination_audit`, `bdm_bic`, `tx_peer_effects_local`, `va_consolidated`; evaluate each against the criteria at migration time rather than assuming.

## Exit-criteria evaluation (plan §6.6)

The pilot was designed as 7 tracked days; what actually happened was **~8 weeks of untracked normal use** (setup 2026-05-06 → push completion 2026-06-23 → PDF conversion 2026-07-02 → ratification 2026-07-03). Longer exposure, weaker instrumentation — each metric below states its actual evidence per `adversarial-default.md` (no silent PASS).

| Metric | Target | Verdict | Evidence |
|---|---|---|---|
| Hook regressions | 0 | **PASS** | No storage-attributable hook failures or crashes recorded in any BDD session log 2026-05-06 → 2026-07-03. The citation-hook false positives fixed during this window were all regex classes, none storage-related. Working-tree PDFs verified real (smudged) documents via `file(1)` on 2026-07-02. |
| `dvc push` failures | 0 | **PASS, with a process finding** | Zero errors when `dvc push` ran (256 files, "cache and remote in sync", 2026-06-23). But the push *wasn't run* for ~7 weeks after `dvc add` — a committed, origin-pushed pointer had zero blobs behind it (dangling pointer; the data existed only on one machine). Found and closed 2026-06-23. This is the pilot's most important learning; see Conditions. |
| Workflow disruption | avg ≥ 4 of 5, rated daily | **ASSUMED (proxy evidence)** | Daily ratings were never collected — the instrumentation didn't survive the pilot's pause/resume. Proxy: ~8 weeks of normal research work in BDD with LFS active and no disruption attributed to storage in any session log; Christina ratified LFS as the forward standard, which is revealed preference against disruption. |
| LFS bandwidth | < 200 MB/wk | **PASS by bound (counter unchecked)** | Total LFS content is ~149 MB across 63 files (`du -sh .git/lfs/objects`, 2026-07-03) — the one-time conversion upload is the dominant transfer ever made, so steady-state weekly bandwidth is bounded far below 200 MB absent mass fresh-cloning. The exact GitHub-side counter was not queried (repo settings → LFS if ever needed). |
| DVC remote storage | < 5 GB | **PASS** | 1.1 GB measured (`du -sh ~/Dropbox/research-data/belief_distortion_discrimination/dvc-cache`, 2026-07-03). |

## Conditions attached to the GO

1. **Anti-dangling-pointer mitigation is mandatory wherever DVC is enabled.** The pilot's one real failure was the forgotten second push, exactly the failure mode `data-version-control.md` warns about. Every DVC-enabled repo gets: `/tools sync-status` run before declaring a session done, and/or the validated `templates/dvc/dvc-sync-check.sh` guard (29/29 end-to-end checks, 2026-06-23).
2. **Coauthor coordination per `data-version-control.md` § Coauthor onboarding** for any shared repo (notify, tag pre-migration commit, be available post-migration). The pilot repo was effectively single-operator; shared repos are where the fresh-clone caveat (no git-lfs → 132-byte pointers) actually bites.
3. **Forward-only conversion only.** `git lfs migrate import` (history rewrite) stays off the table absent a specific size problem — it is gated by `destructive-actions.md` anyway.

## What this supersedes / relates to

- Resolves the plan's D6 gate (open since 2026-05-05) — the last open decision in that plan.
- The previously approved "soft-migrate 60 BDD PDFs to LFS" intent (2026-05-06) was executed 2026-07-02 and ratified 2026-07-03; recorded in BDD `data/CHANGELOG.md`.
- Bulk-migration execution itself is tracked in `TODO.md` (Backlog → now actionable), not in this ADR.
