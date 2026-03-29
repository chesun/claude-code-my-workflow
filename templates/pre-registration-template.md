# Pre-Registration Template

Choose format based on target registry.

---

## Format A: AsPredicted (11 questions)

Based on AsPredicted v2.00. See [Data Colada #64](http://datacolada.org/64) for guidance on answering these questions.

**Authors:**

| Order | First | Last | Email | Affiliation |
|-------|-------|------|-------|-------------|
| 1 | | | | |
| 2 | | | | |

### 1. Have any data been collected for this study already?
( ) No, no data have been collected for this study yet.
( ) Yes, we already collected the data. *(Note: "Yes" is not an accepted answer.)*
( ) It's complicated. *(Explain in Q8.)*

### 2. What's the main question being asked or hypothesis being tested in this study?

### 3. Describe the key dependent variable(s) specifying how they will be measured.

### 4. How many and which conditions will participants be assigned to?

### 5. Specify exactly which analyses you will conduct to examine the main question/hypothesis.
*(Be precise: regression specification, test statistic, controls, clustering.)*

### 6. Describe exactly how outliers will be defined and handled, and your precise rule(s) for excluding observations.

### 7. How many observations will be collected or what will determine sample size?
*(No need to justify the decision, but be precise about exactly how the number will be determined.)*

### 8. Anything else you would like to pre-register?
*(e.g., secondary analyses, variables collected for exploratory purposes, unusual analyses planned?)*
*(If left blank, this will read: "Nothing else to pre-register.")*

### 9. Give a title for this AsPredicted pre-registration.
*(Suggestion: project name + study description. Max 80 characters.)*

### 10. Type of study
( ) Class project or assignment
( ) Experiment
( ) Survey
( ) Observational/archival study
( ) Other: ___

### 11. Data source
( ) Prolific
( ) MTurk
( ) Cloud Research
( ) University lab
( ) Field experiment / RCT
( ) Other: ___

---

## Format B: OSF Pre-Registration (Coffman & Dreber 7-item PAP)

Based on the Coffman & Dreber (2025) pre-analysis plan structure. For the standard OSF registration form, see [OSF Registrations Guide](https://help.osf.io/article/330-welcome-to-registrations). OSF offers multiple templates; the "OSF Preregistration" is the most comprehensive. The structure below maps to the key fields.

### 1. Experimental Design Description
- Treatment arms and their purpose
- Randomization method
- Platform and subject pool

### 2. Inclusion Criteria for Participants
- Who is eligible
- Comprehension/attention check criteria
- Pre-registered exclusion rules and thresholds

### 3. Variables and Coding
- Primary outcome variable(s): definition and measurement
- Secondary outcome variable(s)
- Treatment indicator(s)
- Control variables (pre-treatment only)

### 4. Exact Analyses
- For each hypothesis: regression specification, test statistic, null
- Structural estimation details (if applicable)
- Software and packages

### 5. Control Variables and Clustering Decisions
- Clustering level and justification
- Covariate adjustment method (e.g., Lin 2013)
- Fixed effects (if any)

### 6. Test Hierarchy
| Priority | Hypothesis | Test | Correction |
|----------|-----------|------|-----------|
| Primary | | | |
| Secondary | | | BH/Romano-Wolf |
| Robustness | | | |
| Exploratory | | | None (labeled) |

### 7. Pilots
- [ ] No pilots conducted
- [ ] Pilot conducted — separate linked PAP at: ___
- [ ] Pilot data NOT used to select parameters (design-hacking check)

---

## Filing Checklist

- [ ] All pre-registered analyses appear in the paper
- [ ] Deviations from pre-registration explicitly noted and justified
- [ ] Exploratory analyses labeled as such
- [ ] Pre-registration ID and date in paper
- [ ] Link to pre-registration in paper and replication package
