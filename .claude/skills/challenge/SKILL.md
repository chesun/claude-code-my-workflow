---
name: challenge
description: |
  Adversarial challenge of experimental designs, theoretical models, papers,
  or ideas. Asks the hard questions a skeptical referee, seminar audience,
  or coauthor would ask. Four modes: --design, --theory, --paper, --fresh.
  Use when: user wants to stress-test a design, model, paper, or idea before
  committing resources or submitting.
argument-hint: "[--design | --theory | --paper | --fresh] [file or topic]"
allowed-tools: Read,Grep,Glob,Write,Bash,Task,WebSearch,WebFetch
---

# /challenge — Adversarial Challenge

Stress-test an experimental design, theoretical model, paper, or idea by asking the hard questions that a skeptical referee, seminar audience, or coauthor would ask.

**Input:** `$ARGUMENTS` — a mode flag and a file path or topic description.

---

## Routing Logic

Parse `$ARGUMENTS` for the mode flag:

| Flag | Mode | Target |
|------|------|--------|
| `--design` | Experiment Design Challenge | Design doc, checklist, or topic description |
| `--theory` | Model Challenge | `.tex` file with model, or topic description |
| `--paper` | Paper Challenge | `.tex` manuscript |
| `--fresh` | Fresh Eyes Review | `.tex` manuscript (read cold) |
| *(no flag)* | Auto-detect | `.tex` in `paper/` → `--paper`; design doc → `--design`; model file → `--theory` |

---

## Mode: `--design` (Experiment Design Challenge)

**Purpose:** Find fatal flaws in an experimental design BEFORE running the experiment. This is the most important mode — a bad design wastes months and thousands of dollars.

**Read first:** If `.claude/references/inference-first-checklist.md` exists, load it. Also check `quality_reports/paper_learnings/experimental-design-learnings.md` and `quality_reports/paper_learnings/handbook-experimental-methodology-learnings.md` if they exist.

**Challenge categories (work through ALL of them):**

### 1. Identification & Inference
- "You say Treatment A tests mechanism X — but it also changes Y. How do you isolate X?"
- "Your statistical test assumes independence, but subjects interact in the lab. What's your clustering strategy?"
- "You powered for a 0.3 SD effect — what if the true effect is 0.15?"
- Check: one-factor-at-a-time violated? Multiple changes between treatments?
- Check: test selection appropriate per Moffatt guide?
- Check: clustering at session/group level? (OLS without clustering has size 0.46)

### 2. Subject Experience
- "Walk me through exactly what a subject sees, screen by screen. Where do they get confused?"
- "You're using a slider for belief elicitation — centering bias will contaminate your data. Why not an input box?"
- "Your instructions mention 'other participants' decisions' — this introduces social desirability bias"
- "A median subject takes 25 minutes on your pilot. The 90th percentile takes 55 minutes. Your slowest subjects are your most confused — is that a problem?"
- Check: instructions under 3 pages? Pretested with non-experts?
- Check: attention/comprehension checks present and pre-treatment?

### 3. Incentive Compatibility
- "Is your BDM implementation actually incentive compatible?"
- "Subjects earn $0.50 for a 'correct' belief but $12 show-up fee — are beliefs even incentivized?"
- "Your payment is capped at $20 — subjects near the cap have no marginal incentive"
- Check: payment scheme theoretically justified?
- Check: random round payment — does monotonicity assumption hold?
- Check: stakes comparable across treatments/domains?

### 4. Alternative Designs
- "What if you used within-subject instead of between-subject? What do you gain/lose?"
- "Could a strategy method elicit the same information with fewer subjects?"
- "Have you considered a 2x2 factorial? It would let you test for interaction effects"

### 5. Parameter Selection (Snowberg & Yariv 2025)
- "Your parameters maximize model discrimination, but does the reward function become flat there? Flat incentives = noisy data."
- "At these parameter values, is behavior robust to small misperceptions? Or does a 5% perception error flip the optimal action?"
- "You chose parameters near 0 — noise will compress responses toward the center. Can you move the interesting region to interior values?"
- "Is equilibrium unique at these parameters? If not, you're confounding your treatment effect with a coordination problem."
- "Are your results robust to other parameter values, or did you select these from unreported pilots (design-hacking)?"

### 6. Elicitation (Healy & Leo + Chapman & Fisher)
- "You're using an MPL for belief elicitation — have you checked for centering bias? 16% of Holt-Laury subjects show multiple switching."
- "Your belief elicitation uses a dollar-denominated scoring rule. That assumes risk-neutral EU. Switch to BQSR or MPL."
- "You're eliciting mean beliefs, but that requires EU. Since you're studying probability weighting, elicit the mode instead."
- "30-50% of variance in elicited preferences is measurement error. Are you using ORIV, or treating single elicitations as ground truth?"
- Check: IC assumption hierarchy — is the method's IC assumption justified?
- Check: floor/ceiling risk for bounded variables?
- Check: focal value response risk (60-70% at focal values)?

### 7. Process Measurement (Brocas et al. 2025)
- "Are you collecting response times? They're free and would let you estimate a DDM."
- "Your mouse-tracking data uses trackpads and mice — hardware produces different trajectories. Are you controlling for this?"

### 8. Power & Sample
- Check: power analysis present with justified effect size?
- Check: optimal allocation used (unequal variance, costs, clusters)?
- Check: "30 per cell" myth avoided?
- Check: covariate adjustment planned (Lin 2013)?
- Check: multiple testing correction specified?

**Output format:**

For each challenge, state:
1. The question (adversarial, specific)
2. Why it matters (what goes wrong if ignored)
3. Severity: **FATAL** (stops the experiment) / **SERIOUS** (must address) / **WORTH CONSIDERING**
4. Suggested fix (concrete, not vague)

Save report to `quality_reports/challenges/YYYY-MM-DD_design_challenge.md`

---

## Mode: `--theory` (Model Challenge)

**Purpose:** Stress-test a formal model's assumptions, proofs, and predictions.

**Read first:** If `quality_reports/paper_learnings/theory-writing-learnings.md` exists, load it.

**Challenge categories:**

### 1. Assumptions & Boundary Conditions
- "Your model assumes common knowledge of rationality — but your experiment tests bounded rationality. Contradiction?"
- "Equilibrium is unique only when parameter X > 0. What if X = 0 in your experiment?"
- "Your comparative static prediction requires lambda > 1 — how sensitive is your prediction to lambda?"
- Check: each assumption independently needed?
- Check: boundary examples provided for definitions?
- Check: examples satisfying all assumptions exist (non-vacuous)?

### 2. Architecture & Presentation (Board & Meyer-ter-Vehn)
- "Your theorem statement is 4 lines of notation. Theorems should be English-language takeaways that are also mathematically true. Can you rephrase?"
- "You have 10 theorems. If I forced you to cut to 3, which survive? Those are your paper."
- "Your model takes 4 pages to state. Can you start with a 2-agent, 2-good example?" (Varian KISS)
- Check: main result by page 15?
- Check: fewer footnotes than pages?
- Check: one paper, one model?

### 3. Rubinstein's 4 Dilemmas
- "Where does your model produce absurd results? All models do somewhere — have you probed the boundary conditions?"
- "You're evaluating your model by empirical fit. Rubinstein argues models clarify mechanisms, not predict. What mechanism does yours isolate?"
- "Could you have found this regularity just by looking at the data with no model? When is the model doing real work?"
- "Your formal presentation may obscure moral complexity. What does your model have to say about this practical question — honestly?"

### 4. Proof Quality (Knuth + Halmos)
- Check: direct proofs preferred over contradiction?
- Check: proof steps synchronized with reader expectations?
- Check: quantifiers unambiguous?
- Check: "clearly" and "obviously" claims actually verified?
- Check: math-to-English ratio reasonable for proofs?
- Check: notation introduced before use, no single-use notation?

### 5. Predictions & Testability
- "Which predictions are unique to your model vs. alternatives?"
- "Can your model be falsified? What data pattern would reject it?"
- "Your model predicts X — but so does [standard model]. What's the distinguishing test?"

**Output format:** Same severity scale as `--design`.

Save report to `quality_reports/challenges/YYYY-MM-DD_theory_challenge.md`

---

## Mode: `--paper` (Paper Challenge)

**Purpose:** Challenge contribution framing, identification/design threats, and referee objections. Think like a hostile referee looking for reasons to recommend rejection.

Read `.claude/references/domain-profile-behavioral.md` if it exists for field-specific referee concerns.

**Generate 5-7 challenges from:**

1. **Contribution challenge:** "What does this add beyond [closest existing paper]? Be specific."
2. **Identification/design challenge:** "Your identifying variation comes from X — but what if X is endogenous to Y?" (For experiments: "Your treatment confounds mechanism A with mechanism B.")
3. **Mechanism challenge:** "You show an effect but can't distinguish mechanism A from mechanism B."
4. **External validity challenge:** "Your sample is [specific population] — why should we believe this generalizes?"
5. **Magnitude challenge:** "Your effect size is [X SD] — is that economically meaningful? Back-of-envelope."
6. **Alternative explanation:** "Could [confounder] explain your entire result?"
7. **Missing analysis:** "A referee will ask for [specific robustness check] and you don't have it."

**If the paper contains a formal model, also challenge:**
8. **Theory-experiment alignment:** "Your model predicts X under assumption A — but your experiment violates A. Does the prediction still hold?"
9. **Model necessity:** "Could you have found this result without the model? When is the model doing real work vs. window dressing?"
10. **Prediction uniqueness:** "Your model predicts this effect — but so does [standard model]. What's the distinguishing test?"
11. **Boundary conditions:** "Where does your model produce absurd results? All models do somewhere." (Rubinstein)

**If the paper reports an experiment, also challenge:**
12. **Design confounds:** "Your treatment changes two things at once — how do you isolate the mechanism?"
13. **Incentive compatibility:** "Is your elicitation method actually IC? What assumption does it require?" (Healy & Leo hierarchy)
14. **Demand effects:** "Could subjects be responding to what they think you want, rather than their true preferences?"
15. **Power adequacy:** "You have N subjects — are you powered to detect a plausible effect size, or just a large one?"
16. **Measurement error:** "30-50% of variance in elicited preferences is measurement error. How does this affect your conclusions?"

**Writing quality checks (all papers):**
- McCloskey anti-patterns: "This paper..." openings, passive voice, hedging
- Cochrane violations: punchline buried, intro too long, too many decimal places
- Experimental reporting: N, demographics, exclusions, instructions described?

Save report to `quality_reports/challenges/YYYY-MM-DD_paper_challenge.md`

---

## Mode: `--fresh` (Fresh Eyes Review)

**Purpose:** Cold read — pretend you have never seen this paper. No access to conversation history or prior context. Simulates a referee opening the PDF for the first time.

**Protocol:**

1. Do NOT read any design docs, checklists, or prior reviews first
2. Read the paper from beginning to end, in order
3. State in one sentence what the paper claims to show
4. At each point where you're confused, lost, or unconvinced, note it immediately
5. After finishing, report:
   - **Top 3 concerns** as a first-time reader
   - **Single biggest weakness**
   - **"Desk reject or send to referees?"** recommendation with reasoning

### Note Categories
- **Lost me here:** Points where the argument becomes unclear
- **Why should I care?** Motivation gaps — where the paper fails to convince you this matters
- **I don't believe this:** Claims that feel unsupported or hand-wavy
- **Too much / too little:** Sections that are over- or under-developed relative to their importance
- **Notation/terminology:** Symbols or terms used before definition, or used inconsistently
- **Missing context:** Background knowledge assumed that a generalist referee wouldn't have
- **Model red flags:** (if theory present) Assumptions that seem too strong, proofs that skip steps, predictions that don't follow from the model
- **Design red flags:** (if experiment present) Confounds you noticed, incentive issues, missing controls, power concerns, things that would make you skeptical of the results

**Output format:** Chronological (in order of appearance). For each note:
1. Location (section, page, or paragraph description)
2. What you were thinking at that point
3. Severity: **BLOCKING** (would stop reading) / **DISTRACTING** / **MINOR**
4. What would help (concrete suggestion)

Save report to `quality_reports/challenges/YYYY-MM-DD_fresh_eyes.md`

---

## Output Template (all modes except `--fresh`)

```markdown
# Devil's Advocate: [Paper/Design/Model Title]
**Mode:** [design | theory | paper | fresh]
**Date:** [YYYY-MM-DD]

## Challenges

### Challenge 1: [Category] — [Short title]
**Question:** [The specific adversarial question]
**Why it matters:** [What could go wrong / why a referee would raise this]
**Suggested response:** [How you might address this — if you can]
**Severity:** [Fatal / Serious / Manageable]

[Repeat for 5-8 challenges]

## Summary Verdict
**Biggest weakness:** [The one thing that keeps you up at night]
**Strengths to emphasize:** [2-3 things done well]
**Before proceeding:** [0-3 must-fix items]
```

---

## General Principles

- **Be specific.** "Your design has confounds" is useless. "Treatment A changes both the information structure AND the payoff structure — you can't tell which drives the result" is useful.
- **Be adversarial but constructive.** The goal is to find problems while they're still fixable, not to discourage.
- **Cite evidence.** When challenging a design choice, reference the specific paper or finding that supports your concern.
- **Prioritize.** Lead with fatal/fundamental issues. Don't bury the big problem under 20 minor ones.
- **Acknowledge strengths.** Note what's well-done before diving into problems. A good challenge validates good choices too.
- **No hedging:** "This is a problem" not "This might be a concern."
- **Think like a hostile referee:** What would make you recommend rejection?
- **Save the report.** Always write to `quality_reports/challenges/`. Create the directory if it doesn't exist.
