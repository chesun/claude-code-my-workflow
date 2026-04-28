# Adversarial Default — Universal Rule Proposal

**Status:** PROPOSAL (awaiting your approval before implementation)
**Date:** 2026-04-28
**Triggered by:** tx_peer_effects_local code-fix incident — agent assumed inherited Stata code satisfied "no hardcoded paths" convention; reality was many hardcoded paths.

---

## The principle

**Burden of proof is on the asserter, not the critic.**

When evaluating any artifact — code, paper claim, experimental design, identification strategy, data quality, replication compliance — the default assumption is that the artifact has defects. Compliance is a positive claim that requires positive evidence (a grep result, a test output, a formal proof, a deliberate audit). "I read it and it looks fine" is not evidence; it's the absence of evidence.

This inverts the prevailing pattern. Currently, an agent reviewing inherited code says "no issues found" when it doesn't see obvious red flags. Under the proposed rule, the same agent must produce concrete evidence that *each* relevant convention is satisfied, or note where evidence is missing.

**Counterbalance: don't bloat by re-verifying.** Adversarial-default doesn't mean re-running every check on every task. A verified artifact stays verified until it changes. Verification results are cached in a project ledger; agents consult the ledger before running a check. See "Verification ledger" below.

Three close cousins worth borrowing vocabulary from:

- **Engineering — fool-proofing / poka-yoke.** Design for the worst case so that even an inattentive operator can't produce a defect.
- **Security — zero trust.** Never trust, always verify. No artifact is presumed safe by virtue of its origin.
- **Falsifiability.** Claims that can't be falsified are claims you haven't actually checked.

---

## What goes wrong without this rule

| Failure mode | Concrete example |
|---|---|
| Inherited-artifact trust | Stata code written by a collaborator: agent assumes it follows project conventions; misses N hardcoded paths, missing `set seed`, deprecated packages, etc. |
| Convention-checked-by-impression | Reads a `.do` file, sees `cd "$root"`, forms impression "uses globals," misses 17 other places where absolute paths sneak in |
| Strategy assumption | Inherits an identification strategy from a draft section; takes parallel-trends-holding as given because the original author asserted it; never runs the diagnostic |
| Design assumption | Inherits an experimental protocol; takes the IC mechanism as given; never checks whether subjects can game the comprehension check |
| Replication assumption | Inherits replication code; assumes it runs; never executes end-to-end with a fresh clone |
| Bibliography assumption | Inherits a `.bib`; assumes citations resolve; doesn't run `bibtex` to find undefined references |

The pattern: the agent's prior is "default-trust." The rule flips the prior to "default-suspect." Both priors are defeasible — the difference is which direction the evidence has to push.

---

## Proposed implementation

Three layers, in order of necessity:

### Layer 1 (required) — `rules/adversarial-default.md`

A universal rule articulating the principle, the failure modes, and the per-domain checklists. Loaded by every agent. Cited by critics when scoring.

Structure:

1. **The principle.** One paragraph: burden of proof on asserter, etc.
2. **Inherited-artifact protocol.** When working with code/text/data you didn't write in this session, run a pre-flight scan before any claim of compliance. The scan is per-domain (next section).
3. **Per-domain pre-flight checklists.** Six domains, user-confirmed: **code** (Stata, R, Python), **data**, **design** (experimental), **identification**, **replication**, **bibliography**. One block per domain, each listing concrete checks with the specific shell-command-or-equivalent that produces evidence:

   - **Stata code (inherited).** Before claiming compliance with `stata-code-conventions.md`, run:
     - `grep -E '/Users|/home|C:\\\\\\\\' *.do` (hardcoded absolute paths)
     - `grep -c 'set seed' main.do` (seed set exactly once)
     - `grep -E 'cap log close|set more off' main.do` (master-script hygiene)
     - `grep -nE 'reg .*,' *.do | grep -v cluster` (regressions without `cluster()` — flag for review, not auto-fail)
     - Report the count for each. Zero counts of bad patterns + nonzero counts of good patterns = evidence of compliance. Anything else = report the violations.

   - **R code (inherited).** Analogous: `grep` for absolute paths, `set.seed()` presence, `library()` at top vs scattered, `lm()` for panel data (should be `feols()`), missing cluster spec, deprecated `feols(..., se = "cluster")` argument form, etc.

   - **Python code (inherited).** Active venv, pinned dependencies (`requirements.txt` or `pyproject.toml`), `random.seed`/`np.random.seed`/`torch.manual_seed` set once at top, no absolute paths, `pathlib.Path` for paths.

   - **Data (inherited or just-cleaned).** Before claiming a cleaned dataset is ready for analysis:
     - Column dtypes after each `merge`/`reshape` (Stata: `describe`; R: `str()` or `glimpse()`)
     - Duplicate keys: `isid <key>` (Stata) / `anyDuplicated()` (R) — must be 0
     - Missing-value inventory: `mdesc` (Stata) / `summary()` or `naniar::miss_var_summary()` (R)
     - Panel balance: `xtdescribe` (Stata) / `panelview` (R) — document any unbalance
     - Sample-restriction order documented: every restriction shows N before/after
     - Outliers / sentinel values (–999, 9999): explicit handling, not silently coerced

   - **Identification strategy claim.** Before agreeing that "parallel trends hold," look for: pre-trends figure with confidence intervals, formal pre-trends test (Kahn-Lang, Roth, or honest-DiD-style), explicit discussion of why pre-period coefficients should be zero. Absence of these = "assumption asserted but not tested." Analogous checklists for IV (first-stage F, exclusion-restriction argument, monotonicity if LATE), RDD (McCrary density test, bandwidth choice, manipulation argument), and synthetic control (placebo permutation inference).

   - **Experimental design claim.** Before agreeing that a mechanism is incentive-compatible: derive the optimal-deviation payoff and show it weakly worse than truth-telling. Or cite a paper that proves IC. Or run a simulated participant. "Looks IC" is not evidence. Plus: comprehension-check pass rate, randomization integrity (orthogonality of treatment to baseline covariates), pre-registration filed.

   - **Replication claim.** Before agreeing replication is complete: run the master script end-to-end on a fresh clone; capture the runtime; diff the outputs against the targets file. "I read the README" is not evidence.

   - **Bibliography claim.** Before agreeing citations resolve: run `pdflatex + bibtex/biber` on the actual paper; grep the log for "undefined reference" and "Citation … undefined". "All cites look correct" is not evidence.

4. **Verification ledger (non-bloat mechanism).** A project-level cache so checks aren't re-run on unchanged artifacts.

   **File:** `.claude/state/verification-ledger.md` — tracked in git so cross-session and cross-machine. Format: one-row-per-check, sortable, greppable.

   ```markdown
   | Path | Check | Verified At | File hash (sha256[:12]) | Result | Evidence |
   |------|-------|-------------|-------------------------|--------|----------|
   | scripts/01_clean.do | no-hardcoded-paths | 2026-04-28T10:00Z | a1b2c3d4e5f6 | PASS | grep returned 0 matches |
   | scripts/01_clean.do | seed-set-once | 2026-04-28T10:00Z | a1b2c3d4e5f6 | PASS | line 5: `set seed 20260428` |
   | scripts/02_analysis.do | no-hardcoded-paths | 2026-04-28T10:05Z | f7e8d9c0b1a2 | FAIL | line 47: `use "/Users/foo/data.dta"` |
   ```

   **Lookup protocol:**
   - Before running check `C` on path `P`: read the ledger row matching `(P, C)`.
   - If the row exists AND `file hash` matches the current `sha256(P)[:12]` AND result is PASS: use the cached result; skip running the check; cite the ledger entry as evidence.
   - If row exists but file hash differs: stale → re-run the check, update the row.
   - If row doesn't exist: run the check, append a new row.
   - If row exists with FAIL and file unchanged: still FAIL — flag as unresolved violation, not a re-check.

   **Stale invalidation triggers** (force re-run regardless of cached row):
   - The convention itself changed (`stata-code-conventions.md` modified more recently than the ledger entry).
   - User explicitly invokes `/tools verify --force` (a future skill mode).
   - Pre-submission gate (verifier in submission mode rebuilds ledger from scratch — paranoid mode for journal deposit).

   **Cost:** the `sha256` is cheap (one hash per file), the `grep` is cheap when run, the lookup is cheaper than running. Net effect: first check on a new artifact pays the verification cost; subsequent checks on the unchanged artifact pay the lookup cost.

   **Audit:** the ledger is a living receipt. `grep '| FAIL |' .claude/state/verification-ledger.md` lists open violations. `grep '01_clean.do' .claude/state/verification-ledger.md` shows the verification history of one file.

5. **Exception protocol.** When full verification isn't feasible (cost too high, infrastructure unavailable), the agent must explicitly say "Assumed compliant; not independently verified" rather than implying compliance. The ledger row in this case has `Result = ASSUMED` and an Evidence column entry like `Cost-prohibitive: requires HPC re-run` — auditable.

6. **Cross-references.** Lists which other rules this principle reinforces (verification-protocol, replication-protocol, primary-source-first). The rule doesn't replace them — it changes the *stance* with which they're applied.

### Layer 2 (high-value, easy) — agent-prompt updates

The rule above is loaded by every agent automatically (CLAUDE.md instruction or rules/ globbing). But making the rule actually bite requires updating critic agents to demand evidence-of-compliance rather than evidence-of-violation.

Concrete agent edits:

- **coder-critic** — add a "Compliance Evidence" check category. For each domain convention claimed in the script's docstring or implied by the language (Stata/R/Python conventions file), require a grep or test output proving compliance. "No issues found" without evidence triggers a deduction.
- **strategist-critic** — add "Identification Assumptions Tested" check. For each assumption (parallel trends, exclusion restriction, monotonicity, etc.), require either a diagnostic test result or a "not testable; assuming based on …" disclosure.
- **designer-critic** — analogous for experimental design (IC, comprehension, randomization integrity).
- **writer-critic** — for any claim in the paper that's not formally proved, require a citation or a robustness check.
- **verifier** — replication compliance: run the master script end-to-end before passing. (Already mostly does this, but this rule makes it non-optional in submission mode.)

### Layer 3 (optional, harder) — automation / hooks

Some checks can be automated. Examples:

- **Pre-edit hook on `.do` and `.R` files**: when about to Edit or Write to an inherited file (git blame shows non-current-author), inject a reminder: "Inherited file. Adversarial-default applies. Run grep for hardcoded paths, missing seed, etc., before claiming compliance."
- **Repo-wide "audit" command** in `/tools`: runs the per-domain checklists across the project, produces a report. Useful at session start when picking up a project that's not yours.
- **Stop-hook compliance audit**: at turn end, scan recent assistant prose for compliance claims ("the code follows the conventions", "the identification holds", etc.) and check that evidence was produced in the same turn. If not, flag.

The Stop-hook variant is appealing but hard to get right (false positives on innocuous "looks correct" wording). I'd skip Layer 3 in the first cut and revisit after Layer 1+2 have been used in practice.

---

## Tradeoffs

| Pro | Con | Mitigation |
|---|---|---|
| Catches the inherited-paths failure mode and many like it | More verification time per task | Tiered: full evidence for load-bearing artifacts (paper claims, identification, replication); lighter for sandbox / explorations |
| Forces explicit assumptions when verification is skipped | False positives — agent may demand evidence for things that are obviously correct | "Obviously correct" things still take 10 seconds to grep, which is the right cost for the safety. If a particular check is genuinely degenerate, refine the checklist |
| Makes audits possible — every claim has an evidence trail | Verbose review reports | Use compact format: one-line per check with `✓ <evidence>` or `✗ <violation>` |
| Generalizes — same principle across code, design, identification, etc. | Different domains need different checklists | Per-domain blocks in the rule. Keep them concrete |

---

## Naming

I'd go with `adversarial-default.md` because it parallels the existing `agents.md` "Adversarial Pairing" section. Other candidates:

- `assume-defects.md` — direct, but a little blunt
- `trust-zero.md` — borrows from security; might confuse with Anthropic's product features
- `falsifiability-first.md` — emphasizes evidence; longer name
- `fool-proofing.md` — the engineering term you used; less common in software/research discourse

Your call.

---

## Where to ship

This is a universal rule, so it goes on `claude-code-my-workflow@main` with cherry-picks to `applied-micro` and `behavioral`. Then sync to all downstream project repos that use the workflow (va_consolidated, bdm_bic, tx_peer_effects_local, etc.).

---

## Decision points for you

1. **Concept ok?** Or do you want to refine the principle (e.g., scope only to inherited artifacts, not all artifacts).
2. **Layer 1 + Layer 2, or just Layer 1?** Layer 1 alone gives you the rule but without agent-prompt updates the rule may go un-cited. Layer 2 is what makes critics actually demand evidence.
3. **Name?** `adversarial-default.md` is my recommendation.
4. **Skip Layer 3 for now?** I think yes — automate later if Layer 1+2 underdeliver.
5. **Per-domain checklist coverage** — user-confirmed list: code (Stata + R + Python), data, design, identification, replication, bibliography. Anything else to add (talks, theory proofs, …)? My lean: hold the line at six; theory proofs and talks rarely have the "convention compliance" failure mode this rule targets.

Tell me your answers and I'll write the rule, update the agents, ship to main + overlays + downstream repos, and write a session log on the change.
