# Where this workflow fits — and where your judgment is irreplaceable

Read this before you start using the workflow on real research. It's the most important page in the docs and the one most likely to save you from bad decisions.

---

## The capable-RA analogy

Think of Claude (the underlying model that runs this workflow) as **a capable first- or second-year graduate student RA**. Specifically:

- **Technically proficient.** Can write Stata, R, and Python code that runs. Can format LaTeX. Can produce balance tables, event studies, regression specifications, paper drafts. Can read and summarize papers. Can debug. The mechanics are not the failure mode.
- **Limited subject-matter expertise.** Knows the textbook material in your subfield. Knows the canonical methods. Can recite the standard motivations. But has not spent five years thinking about *your* specific question, the literature gaps you've found, the methodological wrinkles that matter for *this* paper, or the unwritten conventions of your subfield's senior referees.
- **Confident regardless.** Will produce plausible-sounding output for cutting-edge questions where it doesn't know the literature deeply. Without the four-rule epistemic stack pushing back, it will fill in plausible answers when asked. With the stack, it will produce *less* unverified content but cannot generate the missing knowledge.

The workflow's design takes this seriously. Every adversarial critic, every primary-source-first hook, every "derive don't guess" requirement exists because the underlying model — like a capable RA — is willing to give you something that looks right when you ask. The infrastructure forces evidence and grounding so you catch the gaps the RA wouldn't catch on their own.

But infrastructure can't substitute for the missing knowledge. **Your role is the senior researcher.** The workflow handles execution; you handle judgment.

---

## What you keep doing yourself

Three things the workflow cannot replace, no matter how much agent infrastructure surrounds it:

### 1. Knowledge of your literature

You read the papers. You know which ones are foundational, which are methodologically suspect, which referees demand to see cited, which the field has moved past, which are about to flip from minority to consensus. The workflow can `/discover lit` your subfield, but the output is a starting point — a list of candidates for you to evaluate against what you already know.

If Claude makes a framing claim about a paper, the `primary-source-first.md` rule forces it to ground that claim in a tracked reading-notes file. But *whether the framing claim is correct* — whether it captures the paper's actual contribution as your subfield reads it — is a judgment call only you can make. Two people can read the same paper and disagree about what it shows. Claude's reading is one reading.

### 2. Subject-matter expertise

You know which mechanisms are plausible in your setting and which are exotic. You know which model assumptions are reasonable for your population and which are silently false. You know which control variables matter, which are colliders, which are bad controls. You know what "incentive-compatible" means in practice for your specific elicitation environment, not just the abstract definition.

The workflow's overlays codify a lot of this — the behavioral overlay's 13 design principles, the applied-micro overlay's identification checklists — but they're abstractions. Applying them to your actual question requires expertise the workflow does not have.

### 3. Quality control and judgment calls

Every output the workflow produces should be reviewed by you before it goes anywhere serious. Not because the workflow is unreliable as code (it's reasonably reliable), but because *your bar* for what's good enough matters and is not encoded in the workflow.

This includes — but is not limited to — checking that:

- The strategy memo's identification claims are actually what you want to argue, not a textbook version of what your kind of paper usually argues.
- The paper's framing of related work matches how your subfield reads those papers, not how a general literature search summarizes them.
- The robustness checks are the ones referees in *your* outlet will care about, not the generic ones.
- The numerical estimates make sense given what you know about the data, not just that they're "statistically significant."
- The experimental design's mechanism is novel-and-correct, not novel-and-confounded.

The workflow's quality scoring catches mechanical defects (compile errors, missing controls, fabricated paths). It does not catch *substantive* defects (a misframed contribution, a misunderstood literature, a confounded mechanism). Those are yours.

---

## The applied-micro vs behavioral asymmetry

The amount of human judgment required varies systematically across overlays. This is worth being explicit about.

### Applied micro (lower judgment surface)

The methodology is largely settled. DiD, IV, RDD, synthetic control — these have established assumptions, established diagnostics, established failure modes. Top-of-mind threats (parallel trends, weak instruments, manipulation in the running variable, donor-pool selection) are well-documented. The workflow's `applied-micro` overlay codifies most of this:

- The strategist-critic checks parallel-trends tests, IV first-stage F, RDD McCrary, synthetic-control permutation inference — and each check has a literature-anchored PASS criterion.
- Most "is this design valid?" questions can be answered by running the diagnostic the rule says to run.
- Cutting-edge identification (e.g., novel applications of new estimators) still requires expertise, but the substrate is shared.

In practice: you can lean on the workflow more heavily for applied-micro work, because the methodology has been chewed over thoroughly enough that the workflow's encoded checks cover most of the failure space.

### Behavioral (higher judgment surface)

Experimental design is much less settled, especially when you're testing a new mechanism or theory. The workflow's `behavioral` overlay codifies what the field's senior practitioners flag in their own writing — the inference-first 14-step checklist (`.claude/references/inference-first-checklist.md`), the 13 design principles (`.claude/rules/experiment-design-principles.md`) — but those are *general* design principles. They cannot tell you whether *your specific design* identifies the mechanism you think it does, or whether the IC argument that holds in textbook cases breaks down in your specific elicitation, or whether the existing literature has tried-and-failed an approach you're about to propose.

Claude can pattern-match your design against textbook templates and against the codified principles. It cannot tell you that the senior referee in your subfield has spent twenty years pushing back on the very mechanism you're proposing to test, or that a paper currently in the workshop circuit (not yet published) has already shown your manipulation doesn't work.

In practice: for behavioral work, especially experiments that are genuinely novel, treat workflow output as a *first draft* of your reasoning, not as a verification. The four-rule stack catches fabrication; it doesn't catch "this idea has already been disproven by someone the model hasn't read."

---

## When to trust, when to verify

A rough heuristic — not a hard rule, but a useful default:

| Situation | Workflow output is | Your job |
|---|---|---|
| Translating a known method to your data | Often correct | Spot-check; review for project-specific conventions |
| Producing a balance table, event-study plot, summary stats | Almost always correct | Verify variable definitions and sample restrictions |
| Drafting paper sections from an approved strategy memo | First-draft quality | Heavy revision; voice / framing / contribution paragraph rewrites |
| Designing a brand-new experiment for a novel mechanism | Pattern-matched to textbooks; possibly missing the point of *your* mechanism | Hard skepticism; expect to throw out and rework |
| Citing the literature on a niche subfield question | Risky — likely missing recent developments and paper rivalries | Verify every cite against your own reading; don't trust without grounding |
| Identifying which referee objections matter for your outlet | Generic; doesn't know your editor | Substitute your knowledge of the outlet |

The asymmetry above is a default. Specific projects will move points around — a "translating known method" task on weird non-standard data is risky; a "new experiment" task that's a clean variation on a published design is safer.

---

## The bottom line

This workflow is designed to multiply your throughput, not replace your judgment. It handles the mechanical parts of research production (code, drafts, formatting, citation grounding, replication packaging) reliably. The intellectual parts — what's interesting, what's correct, what's novel, what's worth your time — remain yours.

Forkers who use the workflow as a thinking-substitute will produce mediocre research very efficiently. Forkers who use it as a leverage tool — letting it handle execution while they do the substantive work — will get to better research faster than they would alone.

Subject matter expertise and knowledge of the literature are irreplaceable. Quality control is your job. The infrastructure helps; it does not absolve.

---

## See also

- [`epistemic-rules.md`](epistemic-rules.md) — the four rules that catch *fabrication* (mechanical defects of the model). They don't catch substantive defects of the research; that's where you come in.
- [`../getting-started/branch-model.md`](../getting-started/branch-model.md) — the practical implication of the applied-micro vs behavioral asymmetry: pick the overlay that fits, but expect different ratios of agent-output-to-human-revision in each.
- The [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) line "**Forks are encouraged. Your fork should have your opinions.**" applies here too: the workflow's defaults are starting points for your judgment, not substitutes for it.
