# Getting started

Pages for new users. The recommended reading order:

1. **[`prerequisites.md`](prerequisites.md)** — what you need to know before installing (git, terminal, Claude Code, LaTeX, primary analysis language). Curated external resources for each, with rough time estimates. Skip if you're already comfortable with the tooling.

2. **[`installation.md`](installation.md)** — fork → clone → branch-pick → CLAUDE.md customize → verify. Plus troubleshooting for the eight most common installation issues.

3. **[`branch-model.md`](branch-model.md)** — decision tree for picking `main` vs `applied-micro` vs `behavioral`. What each overlay adds beyond `main`. Switching between branches.

4. **[`first-session.md`](first-session.md)** — walkthrough of a typical first day. First-prompt template, what plan-mode looks like, agent-dispatch experience, course-correction signals, what gets preserved at end of session.

---

## Overlay-specific walkthrough (this branch)

5. **[`behavioral.md`](behavioral.md)** — what the `behavioral` overlay adds beyond `main`. The five overlay skills (`/design`, `/theory`, `/preregister`, `/otree`, `/qualtrics`), the four creator–critic agent pairs (designer + critic, theorist + critic, otree-specialist, qualtrics-specialist), the 13 design principles in `experiment-design-principles.md`, the 14-step inference-first checklist. Read after `branch-model.md` confirms `behavioral` is the right pick. **And read [`../concepts/appropriate-use.md`](../concepts/appropriate-use.md) before using these skills on real research** — the applied-micro vs behavioral judgment-asymmetry it discusses is most acute here.

The applied-micro overlay's walkthrough lives on the `applied-micro` branch — `git checkout applied-micro` and read its version of this `getting-started/` directory.

---

## Where to go after getting started

- [`../concepts/`](../concepts/) — why the workflow is shaped the way it is
- [`../reference/`](../reference/) — catalogues of skills, agents, rules, hooks
- [`../customization/`](../customization/) — adapting `CLAUDE.md` and adding project-specific rules / skills / hooks
- [`../faq.md`](../faq.md) — anticipated questions
- [`../README.md`](../README.md) — top-level docs nav hub
