# Getting started

Pages for new users. The recommended reading order:

1. **[`prerequisites.md`](prerequisites.md)** — what you need to know before installing (git, terminal, Claude Code, LaTeX, primary analysis language). Curated external resources for each, with rough time estimates. Skip if you're already comfortable with the tooling.

2. **[`installation.md`](installation.md)** — fork → clone → branch-pick → CLAUDE.md customize → verify. Plus troubleshooting for the eight most common installation issues.

3. **[`branch-model.md`](branch-model.md)** — decision tree for picking `main` vs `applied-micro` vs `behavioral`. What each overlay adds beyond `main`. Switching between branches.

4. **[`first-session.md`](first-session.md)** — walkthrough of a typical first day. First-prompt template, what plan-mode looks like, agent-dispatch experience, course-correction signals, what gets preserved at end of session.

---

## Overlay-specific walkthroughs (live on overlay branches)

- **`applied-micro.md`** — walkthrough of the applied-micro overlay's three skills (`/strategize`, `/balance`, `/event-study`), the strategist + critic agent pair, the air-gapped-workflow rule, and the identification-checklists reference. Lives on the `applied-micro` branch — `git checkout applied-micro` to read it.
- **`behavioral.md`** — walkthrough of the behavioral overlay's five skills (`/design`, `/theory`, `/preregister`, `/otree`, `/qualtrics`), the four creator–critic agent pairs, the 13 design principles, and the 14-step inference-first checklist. Lives on the `behavioral` branch — `git checkout behavioral`.

The overlay-specific docs are intentionally not on `main` because they describe content that doesn't exist on `main`. Stay on `main` for the universal pages above; check out the overlay when you've decided which paradigm fits.

---

## Where to go after getting started

- [`../concepts/`](../concepts/) — why the workflow is shaped the way it is
- [`../reference/`](../reference/) — catalogues of skills, agents, rules, hooks
- [`../customization/`](../customization/) — adapting `CLAUDE.md` and adding project-specific rules / skills / hooks
- [`../faq.md`](../faq.md) — anticipated questions
- [`../README.md`](../README.md) — top-level docs nav hub
