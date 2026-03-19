# Behavioral & Experimental Economics Workflow Plan

**Status:** DEFERRED — applied micro workflow takes priority
**Date:** 2026-03-18
**Branch:** `behavioral` (to be created from `main` after applied micro is stable)
**Detailed design:** See `2026-03-17_workflow-adaptation-plan-v2.md` for full Q&A and specifications

---

## Overview

Adapt the applied micro workflow (Hugo base + Pedro infrastructure) for behavioral and experimental economics. This branch adds experiment-specific skills, agents, and rules on top of the shared core.

---

## What the Behavioral Branch Adds (Beyond Applied Micro)

### Additional Skills
| Skill | What It Does |
|-------|-------------|
| `/design experiment` | Full experiment design using inference-first checklist |
| `/design survey` | Design survey instrument (Qualtrics, oTree) |
| `/design power` | Power analysis (simulation or analytical) |
| `/qualtrics [mode]` | Create/validate/improve QSF, generate custom JS/CSS |
| `/otree [mode]` | Generate/review/explain oTree app code |
| `/preregister` | Generate pre-registration (AsPredicted, OSF) |
| `/theory develop` | Formal model development |
| `/theory review` | Review mathematical derivations and proofs |
| `/challenge --design` | Adversarial experiment design review |

### Additional Agents
| Agent | Role |
|-------|------|
| designer + designer-critic | Experiment design + adversarial review |
| theorist + theorist-critic | Formal model development + proof verification |
| qualtrics-specialist | QSF generation, custom JS/CSS/HTML |
| otree-specialist | oTree app scaffolding and review |
| methods-referee (behavioral) | Calibrated to experimental econ standards |

### Additional Rules
| Rule | Content |
|------|---------|
| `experiment-design-principles.md` | Inference-first, subject comprehension, incentive compatibility |

### Additional Reference Files
| File | Content |
|------|---------|
| `domain-profile-behavioral.md` | Behavioral econ field profile, notation, seminal references |
| `journal-profiles-behavioral.md` | Experimental Economics, JEBO, Games & Economic Behavior, etc. |

### Additional Templates
| Template | Content |
|----------|---------|
| `experiment-design-checklist.md` | 12-step inference-first design checklist |
| `pre-registration-template.md` | AsPredicted + OSF formats |
| `subject-instructions-template.tex` | LaTeX template for subject instructions |

---

## Test Projects

- **BDM** (`bdm_bic`) — halfway through, lit review stage
- **JMP** (`belief_distortion_discrimination`) — mostly finished, good for retrospective testing

---

## Running To-Do List (Behavioral-Specific)

### Must-Do Before Implementation
- [ ] Create `behavioral` branch from `main` (after applied micro is stable)
- [ ] Provide sample `.doh` file (if not visible in test repos)
- [ ] Export QSF from existing Qualtrics survey (for `/qualtrics` skill)
- [ ] Share custom Beamer templates (pdflatex + xelatex)

### Should-Do
- [ ] Gather seminal papers by behavioral econ subfield (12 categories from plan v2)
- [ ] Set up Overleaf git sync for BDM and JMP papers
- [ ] Consolidate JMP satellite repos into single repo
- [ ] Customize notation conventions per paper

### Nice-to-Have
- [ ] Review and refine journal profiles after testing `/review --peer`
- [ ] Identify additional referee concerns from real reviews
- [ ] Test `/design experiment` on BDM experimental design
- [ ] Test `/challenge --design` on BDM experiment
- [ ] Test `/qualtrics validate` on existing BDM Qualtrics survey

---

## Scoring Weights (Behavioral)

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Literature coverage | 8% | Important but not the bottleneck |
| Theory/model quality | 15% | Math must be rigorous |
| **Experimental design** | **25%** | **The experiment IS the paper** |
| Implementation quality | 7% | Survey/code must work |
| Code quality | 10% | Reproducibility |
| Paper quality | 20% | Clarity and argumentation |
| Manuscript polish | 10% | Professional presentation |
| Replication readiness | 5% | AEA compliance |

---

## Reference

Full detailed design (skills, agents, rules, checklist, domain profile, seminal references) is in:
- `2026-03-17_workflow-adaptation-plan-v2.md` — comprehensive Q&A with Christina
- `2026-03-18_consolidated-decisions-and-applied-micro-plan.md` — resolved decisions
