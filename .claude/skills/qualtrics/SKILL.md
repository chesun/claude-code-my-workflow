---
name: qualtrics
description: |
  Create, validate, and improve Qualtrics surveys for experiments. Modes:
  create (generate QSF from design doc), validate (check exported QSF),
  improve (suggest fixes), export-js (generate custom JS/CSS/HTML).
  Dispatches qualtrics-specialist agent.
argument-hint: "[create | validate | improve | export-js] [design doc or QSF path]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash,Task
---

# Qualtrics

Create, validate, or improve Qualtrics surveys by dispatching the **qualtrics-specialist** agent.

**Input:** `$ARGUMENTS` — mode keyword followed by a design document path or QSF file path.

---

## Modes

### `/qualtrics create [design doc]` — Generate Survey from Design

Translate an experiment design document into a Qualtrics-ready survey specification.

**Agent:** qualtrics-specialist
**Output:** Survey specification + flow diagram + custom JS/CSS if needed

**Workflow:**

1. Read the design document from `quality_reports/designs/`
2. Read the inference-first checklist for elicitation and comprehension requirements
3. Generate survey specification:
   - Block structure (consent → instructions → comprehension → main task → demographics → debrief)
   - Question types mapped to Qualtrics equivalents
   - Embedded data fields for treatment assignment and randomization
   - Display logic and skip logic
   - Piped text for dynamic content
   - Randomizer elements for treatment arms
   - Attention checks (placed per design Step 9)
   - Timing questions for RT collection (design Step 7)
4. Generate custom JS/CSS/HTML where needed:
   - BDM interfaces, sliders with custom labels
   - MPL tables with radio buttons
   - Belief elicitation with visual feedback
   - Custom validation (e.g., probabilities sum to 100)
5. Save specification to `experiments/qualtrics/survey_spec_[topic].md`
6. Save any JS/CSS/HTML to `experiments/qualtrics/custom/`

### `/qualtrics validate [QSF path]` — Validate Exported Survey

Check an exported QSF file for common errors and design compliance.

**Agent:** qualtrics-specialist
**Input:** Path to `.qsf` file (exported from Qualtrics)

**Checks:**

1. **Structure:** All required blocks present (consent, instructions, comprehension, task, demographics, debrief)
2. **Randomization:** Treatment assignment via embedded data, not question randomization
3. **Comprehension:** Checks present and positioned before main task
4. **Attention:** Checks present and pre-treatment (never post-treatment)
5. **Timing:** RT collection enabled on decision screens
6. **Logic:** Display/skip logic consistent, no dead ends
7. **Platform integration:** End-of-survey redirect configured (Prolific completion URL, SONA credit, etc.)
8. **Data quality:** Response validation on numeric fields, forced response where appropriate
9. **Design compliance:** Cross-check against design document if available

Save report to `quality_reports/qualtrics_validation_[topic].md`

### `/qualtrics improve [QSF path or survey spec]` — Suggest Improvements

Review a survey and suggest improvements for clarity, IC, and data quality.

**Agent:** qualtrics-specialist

**Focus areas:**

1. **Question clarity:** Ambiguous wording, double-barreled questions, leading questions
2. **IC compliance:** Elicitation method matches design Step 6 IC requirements
3. **Attention management:** Survey length, cognitive load, question ordering effects
4. **Mobile compatibility:** Screen layout works on phone/tablet if online
5. **Data export quality:** Variable naming, embedded data structure, recoding needs
6. **Pilot readiness:** What to check in a pilot run

Save suggestions to `quality_reports/qualtrics_improvements_[topic].md`

### `/qualtrics export-js [spec]` — Generate Custom JavaScript/CSS

Generate specific custom code for Qualtrics questions.

**Agent:** qualtrics-specialist

**Common patterns:**

- BDM mechanism with slider + confirmation
- MPL table with automatic switching detection
- Belief elicitation with probability pie chart
- Timer with auto-advance
- Custom validation (sum-to-100, range checks)
- Prolific/MTurk completion redirect
- Embedded data manipulation via JS

Save to `experiments/qualtrics/custom/`

---

## Principles

- **Design document is the source.** The survey implements the approved design — don't invent new elements.
- **Comprehension before task.** Always place understanding checks before the main decision screens.
- **Attention checks are pre-treatment.** Never drop subjects based on post-treatment checks (Montgomery et al. 2018).
- **Always collect RT.** Add timing questions to every decision screen (Brocas et al. 2025).
- **Randomize via embedded data.** Treatment assignment should use embedded data + randomizer blocks, not question-level randomization — this makes data export cleaner.
- **Test on mobile.** If running online, the survey must work on phone screens.
- **Platform redirect.** Always configure end-of-survey redirect for the recruiting platform.
