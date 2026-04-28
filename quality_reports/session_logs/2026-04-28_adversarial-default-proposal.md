# Session Log: 2026-04-28 — Adversarial-default rule proposal + workflow ship to tx

**Status:** IN PROGRESS — proposal drafted, awaiting user decisions before implementation.

## Workflow-relevant work in this session (claude-code-my-workflow)

| Date / time | Event |
|---|---|
| 2026-04-26 | Drafted `quality_reports/plans/2026-04-26_first-github-release-plan.md` (v0.1.0 release walkthrough). Committed `ee9d234`, then untracked at user's request via `eec6f0a`. File still in git history. |
| 2026-04-27 | Drafted `quality_reports/plans/2026-04-27_dissertation-architecture-advisory.md`. Never committed; deleted from working tree at user's request because it contained personal dissertation planning content. |
| 2026-04-28 | Drafted `quality_reports/plans/2026-04-28_adversarial-default-rule-proposal.md` (this session). Currently untracked. Proposes new universal rule `rules/adversarial-default.md` plus critic-agent prompt updates to invert the burden-of-proof default. Triggered by tx_peer_effects_local code-fix incident: agent assumed inherited Stata code satisfied "no hardcoded paths" convention; reality was many violations. |

## Cross-repo work (logged in their own repos)

- `tx_peer_effects_local@40cda4b` — synced `applied-micro@6d7b910`'s `.claude/` (17 new files, 28 drift updates, 5 superseded files removed). Brings ADR / decision-log rule, primary-source-first hooks, replication-protocol, single-source-of-truth, verification-protocol, python/R conventions, editor agent, pdf-chunking ref. Session log in tx repo at `quality_reports/session_logs/2026-04-28_sync-applied-micro-workflow.md`.
- `dissertation_template`: imported behavioral workflow → reverted (Overleaf-sync conflict); stripped Kalyani Chaudhuri's content to UC Davis template skeleton at `7662ad4`. All session logs in that repo's history; reverts preserved via `git revert` (no force-push).

## Adversarial-default proposal — open decision points

Awaiting user answers in the proposal doc on:

1. Concept scope (all artifacts vs inherited only)
2. Layer 1 alone (rule) or Layer 1+2 (rule + critic prompts)
3. Name (`adversarial-default.md` recommended; alternates listed)
4. Skip Layer 3 (hook automation) for now — my lean: yes
5. Per-domain checklist coverage — proposed Stata, R, identification, design, replication, bibliography; user can extend

## Next step

User decisions on the 5 points → write the rule, update agents, ship to main + applied-micro + behavioral + downstream repos.

## Reference

- Tx incident that triggered this: agent missed hardcoded paths in inherited Stata code. Specific commit / files not pinpointed in this session; proposal addresses the failure pattern, not the specific file.
- Proposal doc: `quality_reports/plans/2026-04-28_adversarial-default-rule-proposal.md`
