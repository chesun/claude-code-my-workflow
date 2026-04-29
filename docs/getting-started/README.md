# Getting started

Pages for new users. The recommended reading order:

1. **[`prerequisites.md`](prerequisites.md)** — what you need to know before installing (git, terminal, Claude Code, LaTeX, primary analysis language). Curated external resources for each, with rough time estimates. Skip if you're already comfortable with the tooling.

2. **[`installation.md`](installation.md)** — fork → clone → branch-pick → CLAUDE.md customize → verify. Plus troubleshooting for the eight most common installation issues.

3. **[`branch-model.md`](branch-model.md)** — decision tree for picking `main` vs `applied-micro` vs `behavioral`. What each overlay adds beyond `main`. Switching between branches.

4. **[`first-session.md`](first-session.md)** — walkthrough of a typical first day. First-prompt template, what plan-mode looks like, agent-dispatch experience, course-correction signals, what gets preserved at end of session.

---

## Overlay-specific walkthrough (this branch)

5. **[`applied-micro.md`](applied-micro.md)** — what the `applied-micro` overlay adds beyond `main`. The three overlay skills (`/strategize`, `/balance`, `/event-study`), the strategist + strategist-critic agent pair, the `air-gapped-workflow.md` rule, and the `identification-checklists.md` reference. Read after `branch-model.md` confirms `applied-micro` is the right pick for your work.

The behavioral overlay's walkthrough lives on the `behavioral` branch — `git checkout behavioral` and read its version of this `getting-started/` directory.

---

## Where to go after getting started

- [`../concepts/`](../concepts/) — why the workflow is shaped the way it is
- [`../reference/`](../reference/) — catalogues of skills, agents, rules, hooks
- [`../customization/`](../customization/) — adapting `CLAUDE.md` and adding project-specific rules / skills / hooks
- [`../faq.md`](../faq.md) — anticipated questions
- [`../README.md`](../README.md) — top-level docs nav hub
