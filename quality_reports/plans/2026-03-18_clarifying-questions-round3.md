# Clarifying Questions — Round 3

**Date:** 2026-03-18
**Instructions:** Add your answers below each question, prefixed with `CS:`. When done, tell Claude to read this file.

---

## A. Behavioral/Experimental Workflow

### Q1: Overleaf Integration Strategy

You mentioned paper drafts live on Overleaf. Three options:

- **(a) Git sync**: Overleaf supports linking to a GitHub repo. You'd work locally with Claude, push, and Overleaf pulls. Edits on Overleaf push back. Cleanest, but requires Overleaf Premium.
- **(b) Local-first, manual sync**: Do heavy Claude-assisted writing locally, then copy to Overleaf for polishing/formatting. Overleaf is the "final mile."
- **(c) Overleaf-first, pull locally**: Keep Overleaf as primary, pull via Dropbox sync when you want Claude to work on it.

Which fits your workflow? Do you have Overleaf Premium (for git integration)? Or do you rely on the Dropbox sync you already have?

CS: I already have overleaf premium, but have been only using dropbox sync. Happy to try git integration if it is better.

### Q2: Scattered JMP Repos

You have 3 repos for JMP (main + endogenous_info + jmp_sample_behavior). Should the workflow assume this multi-repo pattern is normal for your projects, or was this a one-off? This affects whether we design skills to work across multiple repos.

CS: This is a one off and a bad idea. I want to consolidate and just work within one repo.

### Q3: Stata Packages

Listed as should-do but helps write better Stata conventions. Do you use `reghdfe`, `estout`/`esttab`, `coefplot`, `randtreat`? Any others you rely on heavily? (Can answer later if not blocking.)

CS: I use reghdfe, estout, coefplot, ivreghdfe, palettes, cleanplots, egenmore, regsave, cdfplot, binscatter, binscatter2. I also want it set up so that everytime we use a new package, the skill will be updated to learn that new package. Basically, a self update learning rule.

---

## B. Applied Micro Workflow (TX Project)

### Q4: What is the TX Project?

Is it applied micro using observational/admin data (DiD, IV, RDD), or does it also involve experiments? This determines which identification strategy tools to prioritize.

CS: Studying peer effects of immigrant kids using admin data from Texas ERC. Main identification strategy is family fixed effects with within school-grade across cohort variation in immigrant peer exposure. The overleaf dir is /Users/christinasun/Library/CloudStorage/Dropbox/Apps/Overleaf/Immigrant_PoliticalAffiliation_Jan2022 and the current draft on long run outcomes is SOLE_draft. We are working on multiple papers for this project, and currently nearing the submission stage for the long run paper, we have another paper in the works studying political outcomes, and another paper studying the 2006 swift raid. 

### Q5: TX Project Stage

What stage is TX at? (Idea → data exploration → draft → R&R?)

CS: Draft. The data and code lives on an air gapped server at TERC, currently trying to export do files and do coding fixes locally, and create replication package after we are confident in the code. 

### Q6: TX Data Sources

What data does TX use? Observational/admin data? Survey data? Panel data? This determines whether we need DiD diagnostics (Callaway-Sant'Anna, Sun-Abraham), IV tools, RDD tools, etc.

CS: admin panel data. Another paper for the project on 2006 swift raid uses synthetic control and DiD. We estimate a transition matrix for an IV strategy for the long run paper. Can provide details on this.

### Q7: TX Analysis Language

Primary analysis language for TX? Still Stata, or more R/Python?

CS: For Tx, stata.

---

## C. Repo Architecture

### Q8: One Template or Two?

Options: 

- **(a) Single template repo** (this one) with domain-specific "flavor packs" — a behavioral/experimental flavor and an applied micro flavor. You'd fork and pick your flavor.
- **(b) Two template repos** — `claude-code-behavioral-workflow` and `claude-code-applied-micro-workflow`, each with their own skills/agents/rules, sharing ~60% core infrastructure.
- **(c) One template repo with project-type branches** — `main` has shared core, `behavioral-experimental` and `applied-micro` branches have domain-specific additions. Fork the branch you need.

My instinct is **(a)** — one repo with flavor packs — because the core infrastructure (workflow engine, quality gates, context survival, git workflow, session logging) is identical. The differences are mostly in domain profiles, specific skills, and agent prompts.

CS: Please explain how this would work in practice. how does claude know which flavor pack is in effect? would there be confusion, or overlooking rules as a result?

### Q9: Applied Micro Skills Needed

The agent identified these as likely needed for applied micro. Does this match your TX project needs?

- DiD workflow (parallel trends, event study plots, staggered adoption)
- IV/2SLS diagnostics (first stage, weak instruments)
- RDD tools (bandwidth selection, McCrary test, placebo cutoffs)
- Balance table generation
- Sensitivity analysis (Oster bounds, Rambachan-Roth)
- Treatment effect heterogeneity (CATE estimation)

CS: Agreed. Add synthetic control

### Q10: Shared vs. Domain-Specific Skills

These seem common to both workflows:
- `/lit-review`, `/write`, `/review`, `/commit`, `/submit`, `/revise`, `/talk`, `/compile-latex`, `/validate-bib`

These seem behavioral-only:
- `/theory`, `/design experiment`, `/qualtrics`, `/otree`, `/preregister`

These seem applied-micro-only:
- DiD/IV/RDD/panel data diagnostic tools

Does this split feel right? Any skills you'd want in both?

CS: Agreed.

---

## D. Additional Questions (from you)

Add any questions or topics you want to discuss here:

CS: Not at the moment.
