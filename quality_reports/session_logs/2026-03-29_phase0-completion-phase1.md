# Session Log: 2026-03-29 -- Phase 0 Completion + Phase 1 Rules & References

**Status:** IN PROGRESS
**Branch:** `behavioral`

## Objective
Continue behavioral workflow implementation: complete remaining Phase 0 tasks, then proceed through Phase 1 (rules and reference files).

## Changes Made

| File | Change | Reason |
|------|--------|--------|
| `.claude/skills/challenge/SKILL.md` | Created `/challenge` skill with 4 modes (--design, --theory, --paper, --fresh) | Phase 0 task #7 |
| `CLAUDE.md` | Rewrote for behavioral workflow: pdflatex, Stata 17, Overleaf split, behavioral skills table | Phase 0 task #8 |
| `.claude/rules/experiment-design-principles.md` | Created 13-principle "constitution" for experiment design | Phase 1 — highest impact new rule |
| `.claude/rules/stata-code-conventions.md` | Created Stata 17 conventions with experimental data patterns | Phase 1 |
| `.claude/rules/python-code-conventions.md` | Created Python conventions (secondary language) | Phase 1 |
| `.claude/rules/quality.md` | Adapted scoring weights: design 25%, theory 15%, paper 20% | Phase 1 |
| `.claude/rules/workflow.md` | Added behavioral dependency graph, /preregister gate, new agent dispatch | Phase 1 |
| `.claude/rules/content-standards.md` | Added experimental reporting standards, Stata table/figure conventions | Phase 1 |
| `.claude/rules/working-paper-format.md` | Changed xelatex → pdflatex compilation | Phase 1 |
| `.claude/references/domain-profile-behavioral.md` | Created behavioral econ domain profile | Phase 1 |
| `.claude/references/inference-first-checklist.md` | Created portable 14-step checklist | Phase 1 |
| `.claude/references/replication-standards.md` | Created AEA replication standards for experimental papers | Phase 1 |
| `.claude/references/seminal-papers-by-subfield.md` | Created starter list (11 categories, needs Christina review) | Phase 1 |
| `templates/experiment-design-checklist.md` | Created blank 14-step checklist template | Phase 1 |
| `templates/pre-registration-template.md` | Created AsPredicted + OSF PAP templates | Phase 1 |
| `templates/subject-instructions-template.tex` | Created LaTeX template for participant instructions | Phase 1 |
| `quality_reports/plans/...` | Updated plan: checked off Phase 0 + Phase 1 tasks, updated folder structure for Overleaf split | Tracking |

## Design Decisions

| Decision | Alternatives Considered | Rationale |
|----------|------------------------|-----------|
| TikZ deferred to Phase 2 | Create tikz-reviewer now | Package loads fine; reviewer agent belongs with other agent work |
| No separate tables.md/figures.md | Create standalone scoped rules | Content already in content-standards.md and stata-code-conventions.md; separate files would duplicate |
| Folder structure split: git repo + Overleaf | All in one repo | Christina's actual workflow uses Overleaf via Dropbox for paper/slides, git repo for code/data/experiments |
| Each talk in its own folder under Slides/ | Single slides/ directory | Matches Christina's existing practice |
| Replication package in git repo, not Overleaf | Put in Overleaf | Replication involves code, which belongs in the git repo |
| --paper and --fresh modes based on applied-micro | Write from scratch | Applied-micro already had well-tested versions; added behavioral theory/design challenges on top |
| JET removed, JEBO to top field, JEEA added, ExpEcon to strong field | Keep Hugo's default tiers | Christina's correction — she doesn't write pure theory, JEBO is higher tier for her work |

## Incremental Work Log

- Verified TikZ infrastructure — package loads, deferred agent/rule to Phase 2
- Created /challenge skill with full spec from plan Section 10
- Updated --paper and --fresh modes with applied-micro base + behavioral additions (theory + design challenges)
- Rewrote CLAUDE.md for behavioral: Overleaf path, split folder structure, behavioral skills
- Fixed replication/ location (git repo, not Overleaf) per Christina's feedback
- Created 3 new rules: experiment-design-principles, stata-code-conventions, python-code-conventions
- Adapted 4 existing rules: quality.md, workflow.md, content-standards.md, working-paper-format.md
- Created 4 reference files: domain-profile-behavioral, inference-first-checklist, replication-standards, seminal-papers-by-subfield
- Created 3 templates: experiment-design-checklist, pre-registration-template, subject-instructions-template
- Fixed journal tiers per Christina's feedback

## Learnings & Corrections

- Christina does not write pure theory papers — JET not a target journal
- JEBO is top field for behavioral, not just strong field
- JEEA frequently publishes good experimental work
- Experimental Economics is strong field, not top field
- Session logging should be proactive from session start, not batched at end

## Open Questions / Blockers

- [ ] Seminal papers list needs Christina's review and augmentation from Mendeley
- [ ] Journal profiles reference file not yet created (needs more detail than domain profile)
- [ ] Subfield categories (11) — confirm no changes from Christina's edited list

## Post-Phase 1 Corrections

- **Inference-first reframing:** Christina corrected that "specify tests BEFORE designing treatments" is too rigid. Papers (Niederle "dream outcome test," List et al., Snowberg & Yariv) describe co-design: inference needs drive design, but tests and treatments evolve together. Updated language in: CLAUDE.md, experiment-design-principles.md, inference-first-checklist.md, plan Sections 5-6.
- **AsPredicted template fixed:** Had wrong Q1 options, wrong Q9, missing Q10-Q11. Corrected from actual AsPredicted v2.00 HTML form (11 questions, not 9).
- **Journal tiers corrected:** JET removed (Christina doesn't write pure theory), JEBO to top field, JEEA added, Experimental Economics to strong field.

## Phase 2: Agents (completed 2026-03-29)

**Created 6 new agents:** designer, designer-critic, theorist, theorist-critic, qualtrics-specialist, otree-specialist
**Adapted 12 existing agents:** librarian pair (behavioral journals + psychology crossover), explorer pair (experimental data quality), coder pair (Stata 17 primary), writer pair (McCloskey/Cochrane/Knuth + experimental reporting), data-engineer (experimental pipeline), domain-referee (behavioral calibration), methods-referee (5 dimensions for experiments), orchestrator (behavioral dependency graph + preregister gate), verifier (pdflatex + Stata 17), strategist pair (routing note only)
**Kept as-is:** storyteller pair, editor
**Total:** 24 agents

## Phase 3: Skills (in progress 2026-03-29)

Completed so far (7 of 14):
1. `/strategize` → renamed to `/design` with `experiment` and `power` modes
2. `/discover` — adapted interview, lit search (behavioral journals), data discovery (experimental)
3. `/analyze` — Stata 17 primary, non-parametric tests, structural estimation, Overleaf paths
4. `/write` — theory + design sections, McCloskey/Cochrane/Knuth rules, experimental reporting checklist
5. `/review` — strategist-critic → designer-critic routing throughout
6. `/theory` — new skill (develop + review modes, dispatches theorist pair)
7. `/preregister` — new skill (AsPredicted v2.00 + OSF PAP, hard gate, interactive mode)

Completed since last log update:
8. `/qualtrics` — new (create, validate, improve, export-js modes)
9. `/otree` — new (create, review, explain modes; updated to 5.x/6.x with 6.0 features)
10. `/submit` — adapted (experimental replication package, pre-reg compliance, de-identified data)
11. `/talk` — adapted (pdflatex, Overleaf Slides/ paths, unique talk names)
12. `/new-project` — adapted (8-phase behavioral pipeline, pre-reg gate, behavioral folder scaffold)

Also fixed:
- settings.json: added Notification hook for desktop notifications (was missing from behavioral branch)
- settings.json: corrected hook event assignments to match main branch
- oTree agent + skill updated to 5.x/6.x with 6.0 features from version history
- replication-standards.md: raw data with PII should NOT be included; clean de-identified data can be shared

Completed:
13. `/revise` — adapted (Overleaf path, Stata scripts, pre-registration compliance check)
14. `/tools` — adapted (pdflatex compilation, Overleaf paths, full 3-pass for talks)

**Phase 3 complete.** All 14 skills adapted or created.

## Corrections
- notify.sh hook exists but was never wired into settings.json (Hugo's config doesn't have it either)
- No Claude Code hook event for "waiting for permission" — needs terminal-level notification config

## Next Steps

- [ ] Continue Phase 3 skills
- [ ] Phase 4: Testing with BDM project
- [ ] Phase 5: Testing with JMP project
