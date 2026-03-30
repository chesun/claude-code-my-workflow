# JMP Qualtrics Survey Patterns & Architecture

**Source:** `master_supporting_docs/qualtrics/All_treats_diff_prior_June_30_FIXED.qsf` and `Match__Benchmark_July_10.qsf`
**Project:** JMP (belief distortion and discrimination)
**Platform:** Qualtrics + Prolific
**Date analyzed:** 2026-03-29

---

## Survey Architecture

### Overall Flow
Consent → Instructions → Prolific ID → Comprehension Quiz → Part 1 (prior elicitation) → Part 2 (treatment-specific) → Part 3 (wage offers via Loop & Merge) → Attention Check → Demographics

### Two-Stage Randomization (in Survey Flow)
Both files use **BlockRandomizers** in the survey flow (not external assignment):

1. **Worker group** (FL_212, SubSet=1): `worker_group` = `asian` or `hispanic`
   - Each group has different worker names, math test parameters, avatar images
   - Sets: `worker_group`, `worker_group_str`, `mathlink`, `minutes_math`, `math_level`

2. **Treatment arm** (FL_117, SubSet=1): assigns `treat_dfe` (integer) + `treat_str` (short code)
   - File 1 arms: d (DfD), v (Voluntary), f20 (Forced-20), b (Baseline), vc (Voluntary-Commit)
   - File 2 arms: m (Match), fb (Forced Benchmark) — separate QSF for new conditions only

### Two-File Strategy (Not Ideal)
File 1 runs the original 5 treatment arms. File 2 runs only the 2 new arms (Match, Forced Benchmark). This was a necessity from running follow-up treatments after initial data collection — not a best practice. **Ideally, all treatments should be in a single QSF file** with one randomizer for better randomization and simpler data management.

---

## Pattern 1: Custom JS Worker Draw Interface (DB/TB Questions)

**Used in:** QID396 (voluntary), QID485 (forced-20), QID498 (forced-11), QID547 (forced-variable), QID591 (match draws)
**Size:** 5,000–17,000 chars of JS per question

### How It Works
- Question type is **DB/TB (Descriptive Text)** — used as a container for custom HTML + JS
- HTML includes a `<div id="results">` for displaying drawn workers and a `<button id="gamble_btn">` for draws
- JS implements **draw-without-replacement** from hardcoded worker arrays

### Worker Array Structure
```javascript
// [name, race(0=white/1=minority), male(0/1), scoreBin(1-4), age(0/1), color(1-6), exactScore]
asianGroup[0] = ['Emily', 0, 0, 4, 1, 5, 12];
```
- 100 workers per group (asian and hispanic arrays, both defined in every draw question)
- Group selected via `${e://Field/worker_group}` embedded data

### State Persistence (Base64 JSON)
Draw state survives page navigation within loops:
```javascript
// Save state to hidden text input
let newStoredData = {
    resultsHTML: jQuery("#results").html(),
    deckArray: thisGroupArray,
    drawCount: drawCount
};
let encoded = btoa(JSON.stringify(newStoredData));
jQuery(hiddenInputSelector).val(encoded);
```
- Uses a hidden **TE (Text Entry)** question (e.g., `#QID492 input[type='text']`) as storage
- On page load, reads and decodes the stored Base64 JSON to restore state

### Draw Cooldown
```javascript
setTimeout(function() {
    if (drawCount < maxClicks) {
        button.prop('disabled', false);
    }
}, 1000 * parseInt("${e://Field/draw_cooldown_sec}"));
```
- Configurable via `draw_cooldown_sec` embedded data (default: 3 seconds)
- Prevents rapid clicking

### Embedded Data Written by Draw JS
- `draw_count` — number of workers drawn
- `drawn_bins` — comma-separated score bins
- `drawn_races` — comma-separated race indicators
- `drawn_males` — comma-separated gender indicators
- `drawn_workers` — semicolon-separated full worker arrays
- `draw_duration_sec` — total time from first to last draw
- `stored_draws` — HTML of drawn worker results
- `max_draws` — set dynamically in some treatments

---

## Pattern 2: Loop & Merge with JS-Generated Embedded Data

**Used in:** Block 31 (Part 3 wage offers)

### How It Works
1. **QID481 JS** (14,000 chars) runs at Part 3 start: randomly draws `n_profiles` (default 10) worker profiles from the group array
2. JS writes each profile's attributes into embedded data: `profile1_name`, `profile1_age`, `profile1_color`, `profile1_gender`, `profile1_avatar`, `profile1_race`
3. **Loop & Merge** (Static, 10 iterations) uses these embedded fields as merge fields:
   - Field 1: `${e://Field/profile1_name}` (name)
   - Field 2: `${e://Field/profile1_age}` (age string)
   - Field 3: `${e://Field/profile1_color}` (color string)
   - Field 4: `${e://Field/profile1_gender}` (gender string)
   - Field 5: `${e://Field/profile1_avatar}` (HTML img tag)

### Profile Display
QID442 (DB/TB) displays an HTML table with piped L&M fields:
```html
Profile (${lm://CurrentLoopNumber} of ${e://Field/n_profiles})
<table>
  <tr><td>${lm://Field/5}</td></tr>  <!-- avatar image -->
  <!-- name, age, color, gender fields -->
</table>
```
QID538 (TE/SL) asks: "What is your wage offer to this worker? (any integer from 0 to 12)"

---

## Pattern 3: Asset Hosting via External URL

**Used for:** Worker avatars, histogram images

### Avatar URLs (constructed in JS)
```javascript
const thisWorkerAvatarEmbed = '<img src="https://christinasun.net/asset_hosting_service/avatars/'
    + thisGroupStr + '_' + thisWorkerAvatarGender + '_head.jpg"
    height="200" width="200">';
```
- Pattern: `https://christinasun.net/asset_hosting_service/avatars/{group}_{gender}_head.jpg`
- Groups: `asian`, `hispanic`
- Genders: `m`, `f`

### Histogram (set in embedded data)
```
histogram = <img width="500" src="https://christinasun.net/asset_hosting_service/instructions/deg_wtp/assets/thinbar.png">
```

### Why External Hosting
Avoids Qualtrics file upload limits and makes assets reusable across survey versions. Hosted on Christina's GitHub Pages site (`asset_hosting_service` repo).

---

## Pattern 4: Quiz Error Counting JS

**Used in:** QID408, QID410, QID428 (comprehension quiz MC questions)

### How It Works
```javascript
Qualtrics.SurveyEngine.addOnload(function() {
    var question = $(this.questionId);
    $(question).select('.ValidationError').each(function(error) {
        if (error.innerHTML == 'Your answer is incorrect. Please refer to the instructions and try again.') {
            var errors = parseInt(Qualtrics.SurveyEngine.getEmbeddedData("errors_quiz1"));
            errors++;
            Qualtrics.SurveyEngine.setEmbeddedData("errors_quiz1", errors);
        }
    });
});
```
- Uses Qualtrics' built-in validation (force response + correct answer validation)
- JS fires on page load, detects if a validation error message is showing
- Increments `errors_quiz1`, `errors_quiz2`, `errors_quiz3` embedded data counters
- Block 62 ("Quiz Failed") catches participants who fail too many times

---

## Pattern 5: Matched Draw Sequences (Yoking Design)

**Used in:** File 2 only — QID602 (36,826 chars JS)

### How It Works
1. JS contains hardcoded arrays of ~200 real prior participants' draw sequences (with Qualtrics response IDs)
2. Randomly selects one prior participant's sequence
3. Sets `max_draws` to that sequence's length and `matched_sequence` to the bin list
4. QID591 then replays the draw: participant draws the same number of workers, seeing score bins in the matched order

```javascript
const selected = sequencePool[Math.floor(Math.random() * sequencePool.length)];
const matchedDrawSequence = selected.drawn_bins_list;
Qualtrics.SurveyEngine.setEmbeddedData("source_responseid", selected.responseid);
Qualtrics.SurveyEngine.setEmbeddedData("matched_sequence", JSON.stringify(matchedDrawSequence));
Qualtrics.SurveyEngine.setEmbeddedData("max_draws", matchedDrawSequence.length);
```

### Purpose
Yoking ensures the matched participant sees the exact same information as a prior voluntary-draw participant, isolating the effect of choice (endogenous vs exogenous information acquisition).

---

## Embedded Data Summary

### Set in Survey Flow (parameters)
| Field | Default | Purpose |
|-------|---------|---------|
| `participation_fee` | 2 | Base payment ($) |
| `hire_bonus` | 10 | Bonus for hiring task |
| `quiz_bonus` | 10 | Bonus for quiz |
| `totalpoints` | 12 | Max score on math test |
| `n_math` | 12 | Number of math questions |
| `group_size` | 100 | Workers in the group |
| `draw_cooldown_sec` | 3 | Seconds between draws |
| `pct_bonus` | 50 | Bonus percentage |
| `n_profiles` | 10 | Number of wage offer profiles |
| `dfd_force_time_sec` | 120 | Forced viewing time for DfD |
| `part2_force_time_min` | 2 | Min time for Part 2 |
| `expected_duration` | 20 minutes | Shown to participants |
| `histogram` | HTML img tag | Score distribution image |

### Set by Randomizer
| Field | Values | Purpose |
|-------|--------|---------|
| `worker_group` | asian, hispanic | Worker group assignment |
| `treat_dfe` | 0-6 | Treatment code (integer) |
| `treat_str` | d, v, f20, b, vc, m, fb | Treatment code (string) |

### Set by JS (runtime)
| Field | Set by | Purpose |
|-------|--------|---------|
| `draw_count` | Draw JS | Number of workers drawn |
| `drawn_bins` | Draw JS | Comma-sep score bins |
| `drawn_races` | Draw JS | Comma-sep race indicators |
| `drawn_males` | Draw JS | Comma-sep gender indicators |
| `drawn_workers` | Draw JS | Semicolon-sep full arrays |
| `draw_duration_sec` | Draw JS | Time from first to last draw |
| `max_draws` | Draw JS / Match JS | Total draws allowed |
| `stored_draws` | Draw JS | HTML of results |
| `profile1-10_name` | Part 3 JS | Worker profile names |
| `profile1-10_avatar` | Part 3 JS | Worker avatar HTML |
| `profile1-10_race` | Part 3 JS | Worker race (0/1) |
| `profile1-10_gender` | Part 3 JS | Worker gender string |
| `profile1-10_age` | Part 3 JS | Worker age string |
| `profile1-10_color` | Part 3 JS | Worker color string |
| `errors_quiz1-3` | Quiz JS | Incorrect answer counts |
| `source_responseid` | Match JS | Matched prior participant |
| `matched_sequence` | Match JS | Matched draw sequence JSON |

### Captured by Qualtrics
| Field | Source |
|-------|--------|
| `PROLIFIC_PID` | URL parameter from Prolific |
| `countryname` | `${loc://CountryName}` |
| `countrycode` | `${loc://CountryCode}` |
| `test_response` | Flag for test vs real responses |

---

## Question Type Usage

| Type | Code | Count (F1/F2) | Purpose |
|------|------|---------------|---------|
| Descriptive Text | DB/TB | 37/44 | Instructions, draw interfaces, profile displays |
| Page Timer | Timing/PageTimer | 21/25 | Response time on every page |
| Multiple Choice | MC/SAVR | 18/14 | Quiz, prior beliefs, attention checks |
| Text Entry (single line) | TE/SL | 13/15 | Wage offers, draw amounts, numeric inputs |
| Choice Set (vertical) | CS/VRTL | 6/7 | Discrete choice scenarios |
| Matrix (Likert) | Matrix/Likert | 1/1 | Demographics |
| Text Entry (multi-line) | TE/ML | 1/1 | Open-ended feedback |

---

## Pattern 6: Consent Branching with End Survey

### Flow Structure
```
BRANCH: if show_consent == 1
  → Block: Consent
  → BRANCH: if QID285 choice 2 ("No") selected
      → Set embedded: consent = 0
      → END SURVEY
  → Set embedded: consent = 1
```
- Consent is a simple MC (Yes/No) with ForceResponse
- Declining consent immediately terminates the survey
- `consent` embedded data recorded for data cleaning

---

## Pattern 7: Comprehension Quiz with Failure Routing

### Quiz Validation
Quiz questions (QID408, QID410, QID428, QID574) use **CustomValidation**:
- `ForceResponse: ON` + `Type: CustomValidation`
- CustomValidation specifies the correct choice (e.g., `q://QID408/SelectableChoice/4`)
- If wrong answer selected, Qualtrics shows: "Your answer is incorrect. Please refer to the instructions and try again."
- JS on each question detects this validation error and increments `errors_quiz1/2/3` embedded data

### Failure Branching
```
BRANCH: if errors_quiz1 >= 3
  → Set embedded: quiz_failed = 1
  → Block: Quiz Failed (shows termination message)
  → END SURVEY
```
- Threshold: 3 incorrect attempts on any single quiz question triggers failure
- Quiz Failed block (QID439) displays message directing participant back to Prolific
- `quiz_failed` embedded data recorded for tracking

### Scoring Categories
Three scoring categories defined (can be used for conditional branching or data analysis):
- `quiz_hiring_score` — score on hiring-related quiz questions
- `quiz_beliefonly_score` — score on belief-only quiz questions
- `stats_score` — score on statistics questions

### Display Logic for Treatment-Specific Instructions
- QID404 (quiz intro): shows if `treat_dfe != 3` (non-baseline)
- QID585 (quiz intro): shows if `treat_dfe == 3` (baseline only)
- Different instruction text depending on whether participant will do worker draws or logic puzzles

---

## Pattern 8: Attention Checks with Embedded Data Tracking

### Two Attention Checks at Different Survey Points

**Attention Check 1 (QID512)** — after Part 1:
- Text instructs: "You should select twenty no matter what your age is"
- MC with choices: 20, 30, 40, 50, 60
- Flow sets `attention_1_pass` = 0 by default, then:
```
BRANCH: if QID512 choice 1 ("20") selected
  → Set embedded: attention_1_pass = 1
```

**Attention Check 2 (QID513)** — after Part 3 (wage offers):
- Matrix/Likert: "I live in a house made of chocolate"
- Agreement scale; correct answer is disagree
- Flow sets `attention_2_pass` = 0 by default, then:
```
BRANCH: if QID513 choice 1/1 selected (disagree)
  → Set embedded: attention_2_pass = 1
```

### Key Design Choice
Attention check failures do **NOT** terminate the survey — they are recorded as embedded data for post-hoc exclusion. This differs from quiz failures which DO terminate.

---

## Pattern 9: Treatment-Specific Block Routing

### Part 2 Branch Structure
Within the `show_part2 == 1` branch, nested branches route to treatment-specific blocks:
```
BRANCH: if treat_dfe == 0 (DfD)
  → Block: part 2 instructions DfD
  → Block: part 2 posterior DfD

BRANCH: if treat_dfe == 1 (Voluntary)
  → Set embedded: max_draws = 100
  → Block: Part 2 instructions DfE Voluntary
  → Block: Part 2 posterior DfE Voluntary

BRANCH: if treat_dfe == 2 (Forced 20)
  → Set embedded: max_draws = 20
  → Block: Part 2 Instructions forced
  → Block: Part 2 DfEF20

BRANCH: if treat_dfe == 3 (Baseline)
  → Block: Part 2 Baseline

BRANCH: if treat_dfe == 4 (Forced variable/benchmark)
  → Set embedded: max_draws = [value]
  → Block: Part 2 Instructions forced
  → Block: Part 2 draw

BRANCH: if treat_dfe == 5 (Voluntary-Commit)
  → Block: part 2 instructions commit
  → Block: Part 2 commit
  → Set embedded: max_draws = [from commit response]
  → Block: Part 2 draw after commit
```

### Key Patterns
- `max_draws` is set differently per treatment — sometimes hardcoded, sometimes from participant input
- Some treatments reuse the same instruction blocks (e.g., forced treatments share "Part 2 Instructions forced")
- Baseline treatment uses completely different content (logic puzzles instead of worker draws)

---

## Pattern 10: Prior Belief Elicitation (CS/VRTL)

### Histogram-Based Distribution Elicitation
Part 1 uses **Constant Sum (CS/VRTL)** questions to elicit full prior distributions:
- "Out of the 100 workers, how many do you think have a score of..." with 12 bins (scores 1-12)
- Responses must sum to 100 (group_size)
- Same elicitation repeated in Part 2 posterior (after treatment) and in different treatment blocks
- Point estimate also collected: "What do you think is the average score?" (TE/SL with 2 decimal precision)

---

## Pattern 11: Survey-Level Settings for Experiments

### Prolific Integration
- `EOSRedirectURL`: `https://app.prolific.com/submissions/complete?cc=CO1JOJU0`
- `SurveyTermination`: Redirect (sends to Prolific on completion)
- `PROLIFIC_PID` captured as embedded data from URL parameter
- `BallotBoxStuffingPrevention`: true (prevents retakes)
- `RecaptchaV3`: true (bot protection)
- `RelevantID`: true (Qualtrics fraud detection)

### UI Settings
- `BackButton`: false (no going back — critical for experiments)
- `ProgressBarDisplay`: None (no progress bar — prevents strategic behavior)
- `SaveAndContinue`: true (allows resumption if connection drops)
- `SkinLibrary`: ucdavis (institutional branding)
- `ConfirmStart`: true (shows confirmation before starting)

### Custom CSS (in Look & Feel)
```css
/* Gold draw button styling */
button {
    border: none;
    background-color: #cc9900;
    color: #ffffff;
    padding: 5px 10px;
}
button:hover {
    background-color: #FFBF00;
}
button:disabled {
    border: 1px solid #999999;
    background-color: #cccccc;
    color: #666666;
}

/* Hide storage questions from participants */
#QID491 { display: none; }
#QID492 { display: none; }
#QID499 { display: none; }
#QID548 { display: none; }
```
- Custom button colors for the draw interface
- Disabled state styling for cooldown feedback
- **CSS hides the hidden TE storage questions** — these hold Base64 JSON state but must be invisible

---

## Pattern 12: show_* Flags for Modular Testing

### Embedded Data Flags
```
show_consent = 1    # Toggle consent block
show_instr = 1      # Toggle instructions
show_quiz = 1       # Toggle comprehension quiz
show_part1 = 1      # Toggle Part 1 (prior)
show_part2 = 1      # Toggle Part 2 (treatment)
show_part3 = 1      # Toggle Part 3 (wage offers)
show_demo = 1       # Toggle demographics
```
- Each major section wrapped in `BRANCH: if show_X == 1`
- Allows testing individual sections without running the full survey
- Set via embedded data — can be pre-populated from URL parameters
- `test_response` flag (default 0) marks test vs. real responses for data cleaning

---

## Pattern 13: MPL (Multiple Price List) Implementation

**Source:** `DEG_WTP-_MPL_Update_DfE_Voluntary__Forced__DfD.qsf` (earlier JMP version)

### Question Type
Uses **Matrix/Bipolar** question type — two columns (e.g., "HIRE, Receive worker score in dollars" vs "DON'T HIRE, Receive $X"), 12 rows with escalating outside option ($1 to $12).

### Autofill on Switch
Custom JS detects when participant switches from left to right option and **auto-fills all subsequent rows** with the same choice:

```javascript
// Detect switch from previous row
if (prevValue && newValue && prevValue !== newValue) {
    // Auto-fill all subsequent rows
    for (var fillIndex = rowIndex + 1; fillIndex < rows.length; fillIndex++) {
        autoSelectSide(rows[fillIndex], newValue);
    }
}
```

### Single-Switch Enforcement
Custom "Next" button validates that participant switched sides at most once. Multiple switching triggers an alert and blocks advancement:

```javascript
// Count switches between consecutive rows
var switchCount = 0;
for (var i = 0; i < rowSelections.length - 1; i++) {
    if (rowSelections[i] !== null && rowSelections[i+1] !== null) {
        if (rowSelections[i] !== rowSelections[i+1]) {
            switchCount++;
        }
    }
}
if (switchCount > 1) {
    alert("You can only switch sides once as you move down the rows.");
    return false;
}
```

### Switch Point Storage
The switch row (first row where right option is chosen) is stored in embedded data:
```javascript
var switchRow = rowSelections.indexOf("2") + 1;
Qualtrics.SurveyEngine.setEmbeddedData("check" + loop + "_switchrow", switchRow);
```
This gives the WTP/indifference point directly. Used within Loop & Merge (`${lm://CurrentLoopNumber}`) so each profile gets its own switch point.

### Custom Next Button
The built-in Next button is hidden (`this.hideNextButton()`), replaced with a custom button that runs validation before advancing:
```javascript
jQuery("#Buttons").append('<button id="myCustomNextBtn" class="MultiButton">Next</button>');
jQuery("#myCustomNextBtn").on("click", function(e) {
    // validation logic...
    qthis.clickNextButton();  // proceed if valid
});
```

### Bonus Calculation JS
Separate DB/TB question (QID83) calculates payment using embedded data from all rounds:
- Randomly selects a round for payment (`getRandomIntInclusive`)
- Reads switch points and actual scores from embedded data
- Computes bonus and stores in embedded data for display

### Key Design Decisions
- Matrix/Bipolar (not MC or custom HTML) — uses Qualtrics native question type with JS enhancement
- Autofill reduces clicks from 12 to 1 (just click the switch point)
- Single-switch enforcement prevents inconsistent responses (a common MPL issue)
- Works inside Loop & Merge — each worker profile gets a separate MPL

---

## Pattern 14: Input Validation on Response Questions

Three validation types used extensively:

### ContentType: ValidNumber (on TE questions)
```json
{
  "ForceResponse": "ON",
  "Type": "ContentType",
  "ContentType": "ValidNumber",
  "ValidNumber": {"Min": "0", "Max": "12", "NumDecimals": "0"}
}
```
- **Wage offers:** Min=0, Max=12, NumDecimals=0 (integers only)
- **Average score estimates:** Min=0, Max=12, NumDecimals=2 (allows 4.26)
- **Draw amount inputs:** Min=0, Max=100, NumDecimals=0
- Always paired with `ForceResponse: ON` and `MinChars: 1`

### ChoicesTotal (on CS/Constant Sum questions)
```json
{
  "EnforceRange": "ON",
  "Type": "ChoicesTotal",
  "ChoiceTotal": "100"
}
```
- Distribution elicitation: 12 bins must sum to 100 (group size)
- `EnforceRange: ON` prevents negative entries

### CustomValidation (on MC quiz questions)
```json
{
  "ForceResponse": "ON",
  "Type": "CustomValidation",
  "CustomValidation": {"Logic": {"0": {"0": {
    "ChoiceLocator": "q://QID408/SelectableChoice/4",
    "LogicType": "Question",
    "Operator": "Selected"
  }}}}
}
```
- Specifies the correct choice; shows validation error on wrong answer
- Combined with JS error counting (Pattern 4)

---

## Reusable Patterns for Future Surveys

1. **DB/TB as JS container** — use Descriptive Text questions to host complex interactive interfaces
2. **Base64 JSON in hidden TE** — persist complex state across pages within loops; hide with CSS
3. **External asset hosting** — serve images from GitHub Pages (`asset_hosting_service` repo) to avoid Qualtrics upload limits
4. **Embedded data as JS↔Qualtrics bridge** — JS writes to embedded data, L&M and piped text read from it
5. **Quiz error counting** — detect Qualtrics validation errors in JS onload to track attempts; use CustomValidation for correct answers
6. **Yoking via hardcoded sequences** — embed prior participants' data directly in JS for matched designs
7. **Single-file design preferred** — all treatment arms in one QSF with one randomizer for proper randomization. Two-file splits are a workaround for follow-up treatments, not a best practice
8. **Cooldown timers** — parameterized via embedded data for easy adjustment
9. **Loop & Merge with dynamic fields** — JS generates the merge field values at runtime
10. **Consent → End Survey branching** — immediate termination if consent declined, record `consent` embedded data
11. **Quiz failure → End Survey** — threshold-based termination (3 errors), record `quiz_failed` for tracking
12. **Attention checks as data, not gates** — record pass/fail in embedded data for post-hoc exclusion, don't terminate
13. **show_* modular flags** — wrap each section in conditional branch for easy testing
14. **Prolific settings** — redirect URL, no back button, no progress bar, ballot box stuffing prevention, reCAPTCHA
15. **CSS to hide storage questions** — hidden TE questions used for state persistence, made invisible with `display: none`
16. **Treatment routing via nested branches** — randomizer sets treatment code, then branches route to correct blocks
17. **Constant sum for distribution elicitation** — CS/VRTL with constrained sum for full prior/posterior belief distributions
18. **Timing on every page** — PageTimer question in every block for response time analysis
