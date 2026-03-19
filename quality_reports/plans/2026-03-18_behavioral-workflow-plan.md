# Behavioral & Experimental Economics Workflow Plan

**Status:** DEFERRED — applied micro workflow takes priority
**Date:** 2026-03-18
**Branch:** `behavioral` (to be created from `main` after applied micro is stable)
**Detailed design:** See `2026-03-17_workflow-adaptation-plan-v2.md` for full Q&A and specifications

---

## Overview

Adapt the applied micro workflow (Hugo base + Pedro infrastructure) for behavioral and experimental economics. This branch adds experiment-specific skills, agents, and rules on top of the shared core.

---

## Key Decisions (from 2026-03-17 Q&A)

| Decision | Detail |
|----------|--------|
| Analysis language | Stata primary (95%), Python secondary, gradual transition |
| LaTeX engine | pdflatex for Beamer (custom templates for both pdflatex and xelatex) |
| Quarto | **Removed entirely** — not used |
| Field experiments | **Removed** — lab and online only |
| Pre-registration | **Core skill** — always pre-register (AsPredicted, OSF) |
| Experimental design weight | **25%** — single most important component |
| Theory weight | 15% — math-heavy (Markov, Bellman, structural) |
| Seminal papers | Claude gathers per subfield → Christina approves → Christina augments |
| `.doh` files | Do helper files, used with `include` to preserve local macros |
| Test projects | JMP (`belief_distortion_discrimination`), BDM (`bdm_bic`) — separate repos |
| Overleaf | BDM: `BDM Incentive and Truth Telling`, JMP: `belief_distortion_discrimination` |
| Subfield categories | 12 categories (Christina edited — see plan v2 Part 5) |

### Confirmed Subfield Categories (for seminal papers)
1. Prospect Theory & Reference Dependence
2. Social Preferences & Cooperation
3. Time Preferences & Present Bias
4. Belief Formation & Updating
5. Discrimination
6. Complexity & Noisy Cognition
7. Attention & Limited Cognition (incl. Rational Inattention)
8. Experimental Methods & Design (incl. Risk Elicitation, Belief Elicitation)
9. Nudges & Choice Architecture
10. Structural Behavioral Estimation
11. Market/Auction Experiments

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

## `/challenge --design` Mode (Most Important Challenge Mode)

Specific adversarial questions for experiment design review:

**Identification & Inference:**
- "You say Treatment A tests mechanism X — but it also changes Y. How do you isolate X?"
- "Your statistical test assumes independence, but subjects interact in the lab."
- "You powered for a 0.3 SD effect — what if the true effect is 0.15?"

**Subject Experience:**
- "Walk me through exactly what a subject sees, screen by screen."
- "You're using a slider for belief elicitation — centering bias will contaminate your data."
- "A median subject takes 25 minutes but the 90th percentile takes 55 — is that a problem?"

**Incentive Compatibility:**
- "Is your BDM implementation actually incentive compatible? (Danz et al. 2022)"
- "Subjects earn $0.50 for a 'correct' belief but $12 show-up fee — are beliefs incentivized?"

**Alternative Designs:**
- "What if you used within-subject instead of between-subject?"
- "Could a strategy method elicit the same information with fewer subjects?"

## `/design experiment` — Inference-First Checklist

The 12-step checklist produced by `/design experiment` (see plan v2 for full specification):
1. Research question (causal/behavioral claim)
2. Theoretical predictions (testable, from model)
3. Statistical tests (specify BEFORE designing treatments)
4. Data structure required
5. Treatment arms (justify each)
6. Interface & elicitation (method + justification + floor/ceiling analysis)
7. Incentive design (payment structure + IC argument)
8. Subject comprehension (instructions, understanding checks, attention checks)
9. Timing & logistics
10. Power analysis
11. Budget
12. Pre-registration draft

## Experiment Design Principles (Constitutional Rule)

Non-negotiable principles for the behavioral branch:
- **Inference-first**: Specify statistical tests before designing treatments
- **Subject comprehension**: Instructions must be clear; understanding checks required
- **Interface intentionality**: Every elicitation choice documented with justification
- **Simplicity**: Shortest experiment that answers the question
- **Incentive compatibility**: Payment structure must align incentives; cite theoretical basis
- **Floor/ceiling awareness**: Analyze bounded variables for compression risk
- **Pre-registration mandatory**: No data collection without registered hypotheses + analysis plan
- **Pilot first**: Run pilot (N=20-30) before full launch
- **No deception**: Standard in econ experiments; if used, must justify

---

## Domain Profile (Behavioral)

See plan v2 for full expanded domain profile including:
- Target journals by tier (Top-5 + 12 field journals)
- Common identification strategies (RCTs, within/between-subject, strategy method, structural estimation)
- Notation conventions (utility, probability weighting, risk aversion, discount factors, etc.)
- Seminal references organized by subfield (60+ papers)
- Field-specific referee concerns (14 common objections)
- Quality tolerance thresholds

---

## Reference

Full detailed design (skills, agents, rules, checklist, domain profile, seminal references) is in:
- `2026-03-17_workflow-adaptation-plan-v2.md` — comprehensive Q&A with Christina
- `2026-03-18_consolidated-decisions-and-applied-micro-plan.md` — resolved decisions
