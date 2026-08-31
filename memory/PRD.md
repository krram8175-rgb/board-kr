# Karnataka Board Exam Pattern & Analytics — PRD

## Product
A React + FastAPI + MongoDB app showing Karnataka II PUC exam patterns, blueprints, sample question papers (PDF via react-pdf) and analytics per subject.

## Architecture
- Backend: `/app/backend/server.py` (FastAPI). Subject/section data is static in `SUBJECTS`, `SUBJECT_PATTERNS`, `DEFAULT_PATTERNS`.
- Frontend pages: `SubjectBoard`, `SubjectDashboard`, `QuestionPatterns`, `Blueprint`, `FullPaper`, `PaperViewer`.
- Sectioned subjects (Kannada, English) use `patterns[].children` — rendered by `QuestionPatterns.jsx` (`activeMeta.children` branch). Other subjects use chapter ranges/question banks.

## Key endpoints
- GET /api/subjects, GET /api/subjects/{id}, GET /api/subjects/{id}/analytics, GET /api/patterns?subject=

## Implemented
- 2026-06: Base app restored from zip; react-pdf paper viewer working.
- 2026-06: **English subject added** (was `active:False`, now `active:True`). Added `SUBJECT_PATTERNS["english"]` — 5 sections, each with `children`, totaling **80 marks** (Part A 20, Part B 30, Part C 9 [comprehension = one 9-mark passage, prose OR poetry internal choice], Part D 16, Part E/Letter 5). Made `QuestionPatterns.jsx` language-aware: marks word ("ಅಂಕ" for Kannada, "marks" otherwise) and conditional `font-kannada` so English renders in Latin.

- 2026-06: **Blueprint data made Physics-only (button kept for all).** Blueprint/Analytics pill stays visible on every subject. Only Physics renders the real blueprint table; other subjects show a "Blueprint coming soon" empty state (`blueprint-empty`) instead of the copied Physics data. Verified via screenshot.

- 2026-06: **Trial vs Locked subject cards.** `SubjectCard.jsx` — Physics/Chemistry/Math show a green "Trial" badge (top-right) and are clickable; all other subjects show a lock symbol top-right, "Locked", and are disabled (`TRIAL_IDS` gate). Verified via testing_agent (iteration_3, 100%).

- 2026-06: **Lock is decorative only.** Reverted the disable behavior — all subject cards are clickable/openable again. Physics/Chemistry/Math keep the green "Trial" badge; other subjects show a RED lock symbol top-right (visual only, still open). Verified via testing_agent (iteration_4, 100%).

- 2026-06: **Subscription paywall for Biology & CS.** `SubscriptionPaywall.jsx` + `SubjectCard.jsx` — tapping the Biology or CS card (PAYWALL_IDS) immediately opens a "Take Subscription" modal instead of navigating. Plans: 1 Month ₹30, 2 Months ₹50 (Popular), 5 Months ₹100 (Best Value); each unlocks all Karnataka Board subjects. Red lock symbol + "<subject> is locked" at the bottom. Subscribe button is a VISUAL MOCK (no real payment). Verified via testing_agent (iteration_5, 100%).

- 2026-06: **Paywall moved inside (Biology & CS).** Reverted card-tap paywall — tapping Biology/CS now opens the dashboard normally. The "Take Subscription" modal now appears only when tapping an option inside: Full Paper, Blueprint/Analytics, any question type-pill, or the LAB pill (`needsSub` gate + `go()` helper in `SubjectDashboard.jsx`). Subscribe button is a VISUAL MOCK. Verified via testing_agent (iteration_6, 100%).

- 2026-06: **Partial paywall for English & Kannada.** `SubjectDashboard.jsx` + `QuestionPatterns.jsx` — English/Kannada dashboard gates ONLY Full Paper + Blueprint (section pills navigate normally into the section page); on the section page, Full Paper + Analytics are gated. Biology/CS keep FULL gating (all options). Physics/Chemistry/Math/Hindi/Sanskrit ungated. Verified via testing_agent (iteration_7, 23/23).

- 2026-06: **Section sub-items tappable → paywall.** In `QuestionPatterns.jsx` the section-breakdown "mains" (e.g. 1–2 Sentence / 60 Words / 100 Words, and Kannada's ಪದ್ಯ/ಪಾಠ/ನಾಟಕ) are now buttons; tapping any of them opens the subscription paywall for gated subjects (English/Kannada). Verified via screenshot.

- 2026-06: **Chemistry & Math blueprints added.** Refactored `Blueprint.jsx` into a per-subject `BLUEPRINTS` config. Extracted official KSEAB blueprint PDFs → Chemistry (code 34, 70 marks, 10 chapters, Parts A–D) and Mathematics (code 35, 80 marks, 13 chapters, Parts A–E). Physics unchanged. Non-config subjects still show the "coming soon" empty state. Verified via screenshot.

- 2026-06: **Blueprint-driven chapter tabs.** Moved blueprint data to `lib/blueprints.js` (shared). In `QuestionPatterns.jsx`, for Physics/Chemistry/Maths each mark tab (via `MARK_TO_PART` on the pattern's `each`) now lists exactly the chapters that carry that Part, with the per-chapter question count from the blueprint. Verified via screenshots (Chem 2M = 4 chapters, Math 3M = 12).

## Backlog
- P0: Custom Papers — teachers combine questions across subjects into one paper.
- P1: Practice Mode — timed test with scoring + performance summary.
- P2: Formula Sheet — quick-open Physics formula drawer.
