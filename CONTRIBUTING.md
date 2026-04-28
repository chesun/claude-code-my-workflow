# Contributing

This is a personal-use research workflow that's been made public so others can fork and adapt. It's not seeking to become a sprawling community project. The contribution policy reflects that — engagement is welcome on specific, narrow surfaces.

---

## What welcomes contributions

**Issues for bugs and typos.** If a hook misfires, a rule contradicts itself, a skill produces broken output, or a doc has a mistake — please open an issue. Include:

- Exact branch (`main`, `applied-micro`, `behavioral`) and commit hash (`git rev-parse HEAD`).
- What you expected to happen.
- What actually happened (logs, error output, screenshots if relevant).
- Minimal reproduction if possible.

**Issues that ask "is this intentional?"** — sometimes a rule or convention seems wrong but is intentional and undocumented. Asking surfaces it; we add documentation either way.

**Pull requests case-by-case.** PRs are welcome but reviewed against a high bar:

- **Bug fixes** (hook regex false-positives, broken slash command, typo) — generally accepted with verification.
- **Documentation improvements** (clarifications, fixed broken links, missing sections) — generally accepted.
- **New rules / skills / agents** — case-by-case; please open an issue first to discuss scope and fit. The workflow has an opinionated architecture; additions need to compose with existing rules without duplication.
- **Renaming / restructuring** — please don't open these as drive-by PRs. The naming is consistent across rule files, agent prompts, and docs; piecemeal renames create silent inconsistencies. Open an issue first.

---

## What's out of scope (here — fork instead)

- Adapting the workflow for a non-empirical-research domain (humanities, ML/AI papers, theoretical-only, etc.). Fork and rebuild for your domain rather than asking this fork to generalize. The opinionated narrowness is a feature.
- Adding integrations with proprietary services (specific cloud platforms, paid APIs, etc.) unless they're broadly useful to the empirical-research audience.
- Changing the MIT license terms.

---

## Forks are encouraged

If you're using this workflow for your own lab or research group, **fork it and make it yours**. The four-rule epistemic stack, the worker-critic pairing, the verification ledger, the quality scoring — all of these are intentionally opinionated. Your fork should have your opinions. Rename rules. Drop ones you don't use. Add ones we don't have. The architecture is designed for forking.

If your fork develops a useful pattern, opening an issue here to flag it is welcome — even if the pattern isn't suitable for upstream merge, others looking for a similar adaptation might benefit from a pointer to your fork.

---

## Attribution policy

This fork descends from two upstreams:

- **Pedro Sant'Anna**, [`pedrohcgs/claude-code-my-workflow`](https://github.com/pedrohcgs/claude-code-my-workflow) — original lecture/slide template.
- **Hugo Sant'Anna**, [`hugosantanna/clo-author`](https://github.com/hugosantanna/clo-author) — academic-writing adaptation.

If you fork *this* repo, please credit the chain in your own README. The relevant boilerplate:

> Forked from [chesun/claude-research-workflow](https://github.com/chesun/claude-research-workflow), which itself adapts [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) (Pedro Sant'Anna) and [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author) (Hugo Sant'Anna).

If you cite the workflow in a paper or talk, citing the relevant rule or skill file by path is sufficient (e.g., `derive-dont-guess.md, claude-research-workflow v0.1.0`).

---

## Ground rules for any contribution

- **Respect the four-rule epistemic stack.** PRs that add rules should not reintroduce failure modes the existing four rules guard against (fabricated user intent, ungrounded paper citations, fabricated repo facts, unverified compliance claims).
- **No silent renames.** Rule files are referenced by name from agent prompts, other rules, and docs. Renaming a rule requires updating every reference.
- **Tests for hooks.** If a PR modifies `.claude/hooks/`, include tests in `.claude/hooks/test_*.py`. The existing primary-source hook has 27 regression tests; new hooks should follow that pattern.
- **Conventional Commits style** for commit messages: `feat(scope):`, `fix(scope):`, `docs(scope):`, `test(scope):`, `refactor(scope):`. The scope is `workflow`, `applied-micro`, `behavioral`, `hooks`, `rules`, `agents`, `skills`, or `docs`.

---

## Reporting security issues

If you find a security issue (e.g., a hook that could be tricked into executing arbitrary commands, a permission rule in `settings.json` that creates a vulnerability), please report it privately by emailing the maintainer rather than opening a public issue.

---

## License

[MIT](LICENSE). By submitting a contribution, you agree that your contribution is licensed under the same terms.
