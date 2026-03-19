# Follow-Up Questions — Q11-Q14

**Date:** 2026-03-18
**Instructions:** Add your answers below each question, prefixed with `CS:`. When done, tell Claude to read this file.

---

## Q11: Air-Gapped Server Workflow for TX

You said TX data/code lives on an air-gapped TERC server and you're trying to export do files to work locally. This is a significant workflow constraint. How do you envision Claude helping?

- **(a)** Claude works on local copies of `.do` files (code logic, table formatting, robustness check design) — you manually transfer fixes back to TERC
- **(b)** Claude helps design the replication package structure locally, you populate with outputs from TERC
- **(c)** Claude reviews exported do files for code quality, identifies issues, you fix on TERC
- **(d)** All of the above

This affects what the applied micro workflow optimizes for. If Claude can never see the data or run code, the skills need to be designed differently (more code review/generation, less interactive analysis).

CS: All of the above. I can supply data structure, variable names, summary statistics, etc. But claude will not be able to see the actual data for confidentiality reasons. However, I want the workflow to be general enough that for other applied micro projects that includes interactive analysis, it will be capable. The applied micro workflow is not only for TX project.

## Q12: TX Multi-Paper Structure

You mentioned 3 papers from TX (long run outcomes, political outcomes, 2006 swift raid). Do these share:
- The same repo?
- The same do files / data pipeline?
- The same Overleaf project?

This affects whether the applied micro workflow needs a "multi-paper project" pattern.

CS: The are in the same repo, and the data pipeline is the same up to a point. They use the same data cleaning pipeline, but takes the cleaned data and diverge in how they use it and which sample they use. So think a single lineage then three branches. Same overleaf project at least for long run and political paper. Haven't started drafting for swift project yet. I have been working on the swift project and some debuggin in claude chat, and can give you the relevant memory and output once we set up the workflow.

## Q13: Overleaf Git Sync — Recommendation

Since you have Premium, I recommend **Overleaf git sync** over Dropbox sync. Here's why:

- **Bidirectional**: edit on Overleaf OR locally with Claude, both sync via git
- **Conflict resolution**: git merge vs. Dropbox's "conflicted copy" files
- **Version history**: git log shows exactly what changed and when
- **Claude integration**: Claude can `git pull` from Overleaf, edit, `git push` back

The workflow would be: link each Overleaf project to its GitHub repo's `Paper/` directory. Claude works locally, pushes to GitHub, you pull in Overleaf (or it auto-syncs). You edit in Overleaf, push, Claude pulls.

**One caveat:** Overleaf git sync works at the project level (whole Overleaf project = one git repo). If your paper lives inside a larger project repo, you'd need a subtree or a separate Paper repo linked to Overleaf. Want me to research the best setup?

CS: Yes please research the best setup. Please don't make it too complicated.

## Q14: Self-Updating Stata Package Learning

You want a rule that auto-updates when a new Stata package is used. Two implementation options:

- **(a) Hook-based**: A post-edit hook detects new `ssc install` or package usage in `.do` files, appends to the Stata conventions rule automatically
- **(b) Memory-based**: Claude notices a new package, saves a `[LEARN:stata]` entry to MEMORY.md, and you periodically promote confirmed packages to the Stata conventions rule
- **(c) Both**: Hook flags it, Claude confirms and documents

Which feels right? (b) is simpler and more reliable; (a) is more automated but harder to get right.

CS: Let's do both for failsafe.

---

## Repo Architecture: Revised Recommendation

I'm recommending **two template repos** instead of flavor packs. Here's why and how:

### Why Not Flavor Packs

Claude Code loads *all* rules, skills, and agents from `.claude/`. There's no selective activation. If `/design experiment`, `/qualtrics`, and `/otree` skills exist in `.claude/skills/`, they're available and triggerable even in an applied micro project. This creates:

1. **Noise** — Claude might suggest `/design experiment` when you're working on the TX peer effects paper
2. **Rule conflicts** — behavioral experiment design principles load alongside applied micro conventions, even when irrelevant

### Proposed: Two Template Repos + Shared Maintenance

```
Template repos (you maintain these):
  claude-code-my-workflow/              # Behavioral & experimental template
    .claude/skills/  → design, qualtrics, otree, preregister, theory...
    .claude/agents/  → designer, designer-critic, theorist...
    .claude/rules/   → experiment-design-principles, domain-profile-behavioral...

  claude-code-applied-micro-workflow/   # Applied micro template (NEW)
    .claude/skills/  → did-diagnostics, iv-tools, synth-control, balance-table...
    .claude/agents/  → applied-micro-referee, identification-critic...
    .claude/rules/   → identification-strategy, domain-profile-applied-micro...

Both share (copy at creation, sync periodically):
    .claude/skills/  → commit, compile-latex, lit-review, write, review, submit...
    .claude/agents/  → librarian, coder, writer, verifier...
    .claude/rules/   → workflow, quality, logging, stata-conventions...
```

**How projects fork from templates:**
```
  belief_distortion_discrimination/     # forked from behavioral template
  bdm_bic/                             # forked from behavioral template
  tx_peer_effects/                     # forked from applied micro template
```

**Why this is better:**
- Each project gets exactly the right skills/rules — no noise
- Claude never confuses which domain it's in
- Shared infrastructure (~60%) is copied at fork time; sync improvements occasionally
- Each template evolves independently

**Maintenance burden:** Low. Shared core (workflow engine, quality gates, hooks, session logging, Stata conventions) changes infrequently. When it does, cherry-pick into the other template. Domain-specific skills never need syncing.

Do you agree with this approach, or do you have concerns?

CS: I like this idea. Should we make the behavioral workflow a branch named something like claude-code-behavioral-workflow so that gives us room in the future to pull new commits Pedro makes into the main branch? Please advise. I want to leave room open for incorporating new innovations from Pedro and Hugo.

---

## Proposed Next Steps

Once you answer Q11-Q14:

1. **Revise plan_v2 → v3** for behavioral/experimental workflow (all resolved answers)
2. **Draft plan_v1 for applied micro workflow** (TX-focused, identification strategy skills, air-gapped server patterns, multi-paper structure)
3. **Create the applied micro template repo** (or plan for it)
4. **Consolidate running to-do list** across both workflows
5. **Begin Phase 1 implementation** on whichever workflow you choose first

**Which workflow do you want to implement first — behavioral/experimental (BDM test case) or applied micro (TX test case)?**

CS: I want to implement the applied micro workflow first because I am under time crunch for that project.
