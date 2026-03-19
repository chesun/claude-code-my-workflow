# TX Project Memory Block — Proposed Revision

**Instructions:** Review the revised memory block below. Edit directly or add `CS:` comments. This replaces the chat memory block in the consolidated plan.

---

## Proposed Revised Memory Block

```markdown
## Purpose & Context

Christina is an academic researcher studying (1) long-run peer effects of immigrant children on native students, (2) political outcomes of immigrant peer exposure, and (3) immigration enforcement and long-run human capital outcomes. All three papers use Texas Education Research Center (TERC) student-level administrative data (1990–2024+) with various linkages.

### Data Infrastructure (Shared Across All Papers)
- **TERC**: Student-level K-12 enrollment and achievement records
- **TWC**: Texas Workforce Commission quarterly wage records (labor market outcomes)
- **THECB**: Texas Higher Education Coordinating Board post-secondary records (college outcomes)
- **TBI**: Texas Birth Index — used to link siblings within families (enables family FE)
- **L2**: Voter registration data (political paper only)
- All data accessed on air-gapped TERC server via NoMachine remote desktop
- Stata (server has older reghdfe/ivreghdfe versions)

### Paper 1: Long-Run Peer Effects (Near Submission)
- **Question:** What are the long-run effects of immigrant peer exposure on native students' education and labor market outcomes?
- **Coauthors:** Briana Ballis (UC Merced), Derek Rury (Oregon State)
- **Identification:** Family FE with within school-grade across cohort variation in immigrant peer exposure. IV: predicted exposure from a transition matrix instrumenting for actual exposure.
- **FE specs:** (1) grade×year + campus×year + family FE; (2) grade×year + campus×year + family×year FE (3) currently testing gradexyear + familyxinitial_campus for IV, following Figlio et al. (2024) Diversity in Schools ReStud
- **Outcomes:** Test scores, college enrollment, adult employment and earnings
- **Stage:** Near submission. Finalizing regression sample, producing main IV results across outcome groups.
- **Overleaf:** /Users/christinasun/Library/CloudStorage/Dropbox/Apps/Overleaf/Immigrant_PoliticalAffiliation_Jan2022 (current draft: SOLE_draft)

### Paper 2: Political Outcomes
- **Question:** Does childhood immigrant peer exposure affect political participation and attitudes in adulthood?
- **Coauthors:** Briana Ballis (UC Merced), Derek Rury (Oregon State)
- **Identification:** Same IV/FE framework as Paper 1, applied to political outcomes
- **Additional data:** L2 voter registration records
- **Stage:** In progress
- **Overleaf:** Same project as Paper 1

### Paper 3: Swift Raid (Early Stage)
- **Question:** Does childhood exposure to immigration enforcement cause permanently lower adult outcomes?
- **Coauthors:** Briana Ballis (UC Merced), Derek Rury (Oregon State), Emily Dieckmann (UC Merced)
- **Identification:** Synthetic control + DiD around December 12, 2006 Operation Wagon Train raid in Cactus, TX (~297 workers arrested, ~3,000 population town)
- **Key contribution:** Fills 4 gaps in causal economics literature:
  1. No existing paper traces childhood enforcement exposure to adult earnings
  2. No study uses individual-level linked education-to-employment admin data
  3. Swift/Cactus raid is entirely unstudied quantitatively
  4. 17+ year follow-up vs. ~5-year maximum in prior work
- **Key risks:** Single-event case study, small treated population, selective attrition, confounding events over 17-year window
- **Stage:** Early — literature review complete (see swift_lit_review_output.md), identification strategy planned
- **Rejected alternative strategies:** Secure Communities (crowded), Load Trail (already studied), 287(g) (too recent), TRAC shift-share (data too coarse)

### Shared Data Pipeline
```
TERC enrollment → data cleaning → cleaned dataset
  ├── Paper 1: sample selection → transition matrix merge → IV/FE regressions
  ├── Paper 2: sample selection → voter registration linkage → political outcome analysis
  └── Paper 3: Cactus/Moore County sample → pre/post raid → synthetic control + DiD
```
Merge pipeline: enrollment linked to transition matrix via campus, year, grade, grade_0 (starting grade). All merge keys converted to string (prior bug fix recovered ~30M records). Grade repeaters/skippers excluded.

### Technical Lessons Learned
- Variable type mismatches are a high-priority hypothesis when Stata merge rates drop dramatically
- e(sample) must be captured immediately after estimation; sample() option unavailable on older reghdfe versions
- Dropbox + Git is structurally incompatible; sync operations corrupt .git internals
- Git stashes are LIFO; selective restoration requires `git checkout stash@{N} -- filepath`
- NoMachine lag on Mac caused by Retina display scaling; fix by capping resolution
- Singleton observations are a concern given small campus sizes and family structure

### Key Literature
**Paper 1 (Peer Effects):**
- Primary reference: Figlio et al. (2024) "Diversity in Schools" ReStud — closely following this paper; they study short run in Florida, we extend to long run in Texas
- Peer effects canon: Sacerdote (2001), Hoxby (2000), Angrist & Lang (2004), Lavy et al. (2012), Figlio & Ozek (2019)

**Paper 3 (Swift Raid):**
- Causal econ: Amuedo-Dorantes & Lopez (2015, 2017), Amuedo-Dorantes et al. (2018), East et al. (2023), Bansak et al. (2024), Dee & Murphy (2020), Bellows (2019, 2021), Bennett et al. (2025), Tomé et al. (2021), Novak et al. (2017)
- Causal other: Heinrich et al. (2023), Kirksey & Sattin-Bajaj (2023, 2025), Avila (2024), Weber (2022)
- Full classification: swift_lit_review_output.md (25 papers)

### Infrastructure
- Air-gapped TERC server (NoMachine remote desktop, no internet during analysis)
- Stata-mp or Stata-se (server version with older package versions)
- Git for version control (migrating away from Dropbox for repos)
- Dropbox for coauthor file sharing (non-code assets only)
- Claude Code for local code drafting (outside shared Dropbox folders)
```

---

## Questions for Christina

1. **Paper 1 vs Paper 2 identification:** Is Paper 2 using the exact same IV/FE strategy as Paper 1, just with political outcomes instead of education/labor? Or is there a different identification approach?

CS: Exact same. Just different outcomes.

2. **Paper 1 title/framing:** The Overleaf project is called "Immigrant_PoliticalAffiliation" but the paper near submission is about long-run peer effects on education/labor outcomes. Is this just an old project name, or is the framing different from what I described?

CS: old project name.

3. **Swift paper data:** Does the swift paper use the same transition matrix / IV approach as Paper 1, or is it purely synthetic control + DiD (no IV)?

CS: No. Purely synthetic control and DID for now. May change later.

4. **Peer effects literature for Paper 1:** The chat memory focused on enforcement literature (for swift). For Paper 1, should I note key peer effects references? (e.g., Sacerdote 2001, Hoxby 2000, Angrist & Lang 2004, Lavy et al. 2012, Figlio & Ozek 2019)

CS: Yes. The key reference is Figlio et al 2024, Diversity in Schools, in ReStud. We are following this paper pretty closely. They only study short run and is in Florida.

5. **Anything else missing or wrong in the revised memory block?**

CS: I revised some parts of the memory block. Everything else looks good.
