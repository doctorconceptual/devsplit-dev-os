# Task: 001 - Build the CRO Audit Agent

**Project:** cro-audit-agent
**Task ID:** 001
**Created:** 2026-09-23
**Priority:** High
**Status:** Not Started

---

## Agent / Model Context

Agent: Hermes
Model: [model name/version currently in use]

This task file is written to be followed literally. Do not infer intent beyond
what is written. If any instruction below is ambiguous, incomplete, or
conflicts with something you find in the codebase, **stop and ask** rather
than assume or fill the gap yourself.

---

## Required Reading (load before starting)

- `.devos/constitution/company.md`
- `.devos/constitution/engineering-standards.md`
- `.devos/departments/engineering/senior-fullstack-engineer.md`
- `projects/cro-audit-agent/cro-audit-checklist.xlsx` — the 92-point checklist
  this agent is built to run. It is the specification. Route each check by its
  `Method` column (DOM / Vision / API / Manual).
- `projects/cro-audit-agent/sites-to-audit.xlsx` — INPUT: the list of store URLs
  to audit. Audit each row where `Status = Pending`, starting with the first.
- `projects/cro-audit-agent/README.md` — project overview.
- HERMES.md (workspace root), if present

If a document referenced above doesn't exist, say so explicitly rather than
proceeding as if it does.

---

## Objective

DevSplit runs CRO-focused cold outreach to ecommerce store owners. Each pitch
depends on one real, verified conversion problem observed on the prospect's own
site. Doing that by hand is ~30 minutes per store and does not scale. This task
builds an agent that takes a store URL, runs it against the 92-point CRO
checklist, and returns one result row per check (Y/N/NA + confidence +
evidence), matching the checklist's column format so the team reviews output in a
tool they already know. The agent removes the grunt work; a human still confirms
the chosen observation before it enters an email.

This is **build-and-calibrate, not model training.** No fine-tuning, no labelled
dataset. The checklist is the spec. The agent knows it as instructions; you tune
those instructions against a golden reference until agreement is high.

---

## Before Doing Anything Else

1. Restate any URLs, IDs, or file paths referenced in this task file back to me
   **verbatim**, before using them.
2. This is a greenfield tool. If no `code/` exists for this project yet, create
   the project scaffold per the stack in "Scope of Work" below and confirm it
   runs before implementing checks.
3. Bring up the local environment and confirm status (browser automation
   dependencies installed, PageSpeed API key present).
4. Read `sites-to-audit.xlsx` and state the first `Pending` store URL you will
   run against (record 1 is https://loandcointeriors.com/ — restate it verbatim).
   Confirm it is public and safe to hit.
5. Pull latest `main` and create branch: `feature/001-cro-audit-agent`

Do not guess credentials, API keys, URLs, or file paths. If something referenced
here is missing, wrong, or unclear once you look at the actual project, stop and
ask — do not substitute your own assumption.

---

## Credentials / Access (if applicable)

> Avoid pasting live credentials into this file — it is git-tracked. Use a
> **gitignored** `credentials.local.md` (or `.env`) in the project root and
> reference it here.

- PageSpeed Insights API key: [reference where it lives — .env]
- Vision model API key: [reference where it lives — .env]
- Proxy provider credentials (Phase 3 only): [reference]
- Scope: read-only against public store URLs. Never submit real orders or
  personal data on any prospect's site.

---

## Scope of Work

### Phase 1 — Single-site prototype
- [ ] The `Method` column already exists in `cro-audit-checklist.xlsx` (all 92
      rows tagged DOM / Vision / API / Manual). Read it and route each check by
      it. Do not re-tag unless you find an error — if you do, flag it, don't
      silently change it.
- [ ] Read the first `Pending` row from `sites-to-audit.xlsx`
      (https://loandcointeriors.com/) and audit that store. Write `Status`,
      `Date Audited`, and `Output File / Link` back to the input file when done.
- [ ] Scaffold the project (recommended stack: Node + Playwright, or Python +
      Playwright — engineer's choice, state which and why).
- [ ] Playwright loader: render each store at desktop AND mobile viewports, wait
      for the page to settle, capture screenshots for both.
- [ ] Implement `DOM` checks (~55 rows): read the rendered DOM for element
      presence/position (review widget, size guide, breadcrumbs, search, filters,
      payment badges, image gallery, etc.).
- [ ] Implement `API` checks (4 rows): call Google PageSpeed Insights and read
      Core Web Vitals. Speed is never "felt" by the agent.
- [ ] Implement `Vision` checks (~22 rows): send screenshots to the vision model,
      one tight instruction per check, forced structured JSON output, in small
      batches (never all 22 in one prompt).
- [ ] Assemble output: one row per check → `Exists?` (Y/N/NA/unsure),
      `Confidence`, `Evidence`, `Method`, and the pre-written `Email line` when
      `Exists? = Y`. Write to the checklist's `.xlsx`/sheet format.

### Phase 2 — Calibration
- [ ] Manually audit 3–5 stores across different niches (the golden reference).
- [ ] Run the agent on the same stores; diff the answers.
- [ ] Fix the rule or prompt behind each disagreement.
- [ ] Stop when agreement is consistently ≥85% on DOM + Vision checks.

### Phase 3 — Batch runner
- [ ] Wrap single-site logic in a queue (one job per URL).
- [ ] Concurrency limits, retries with backoff, per-site timeouts.
- [ ] Residential proxy pool; handle blocked/failed sites as `could not audit`
      (never crash the batch).
- [ ] Run the full URL list; review output.

---

## Out of Scope / Do Not Touch

- Do not automate live checkout submission at scale. Checkout-flow checks stay in
  the `Manual` bucket unless explicitly re-scoped.
- Do not submit forms, create accounts, or place orders on any prospect's site.
- Do not modify the checklist's existing 92 observations or their email lines;
  only ADD the `Method` column and the output columns.
- Do not touch other DevOS projects.

---

## Guardrails (mandatory — these are the failure modes to prevent)

- **Never fabricate an observation.** A check that cannot be verified (page
  failed to load, element ambiguous) outputs `unsure` — never a guessed Y/N. A
  false observation in a cold email is worse than a missing one: it tells the
  prospect you did not actually look. Any run with fabricated or unverifiable
  rows fails QA.
- **Physically interact with the site.** DOM checks read the *rendered* DOM after
  the page settles; cart checks actually add an item and open the cart. Do not
  infer presence from raw source HTML or from platform assumptions.
- **Speed comes from the API, not a guess.** The 4 speed checks use PageSpeed
  output. No estimated or "feels slow" values.
- **Evidence is required on every non-NA row.** No evidence string = the row is
  not done.
- **Distinguish assumptions from verified facts** in all output and summaries.

---

## Acceptance Criteria / Manual QA Steps

1. `Method` column added and all 92 rows tagged (DOM/Vision/API/Manual).
2. A single-site run produces all 92 rows in the checklist's format.
3. Spot-check 10 rows by hand against the live site (DOM, Vision, and API each
   represented) — every one matches reality.
4. Every `Y` row carries a real evidence note and the correct email line.
5. Mobile-only checks (sticky Add to Cart, tap targets, mobile layout) are
   evaluated at the mobile viewport, not desktop.
6. A deliberately broken URL yields `could not audit`, not a crash.
7. Calibration: ≥85% agreement with the golden reference on DOM + Vision checks.
8. Batch runner handles blocked/failed sites gracefully.

---

## General Instructions

- Read every affected file before making changes.
- Do not break any existing functionality.
- Actually run the pipeline end to end against a real store and read the produced
  rows. "No errors thrown" is not sufficient — verify the values match the live
  site.
- Actually interact with each site (render, scroll, add to cart where a check
  requires it). A check inferred without interaction is not done.
- Keep secrets in a gitignored `.env` / `credentials.local.md`, never in code or
  this task file.
- Follow DevOS engineering standards (see Required Reading).
- Make the smallest reasonable change that satisfies the objective.

---

## Escalate / Stop and Ask If

- Any credential, URL, API key, or path referenced here doesn't match what you
  find.
- The work requires an architecture change beyond what's described.
- A prospect site actively blocks automated access and no proxy is configured
  (Phase 1/2).
- Multiple valid approaches have significant trade-offs (e.g. vision model
  choice, output target).
- Anything in this file conflicts with a DevOS document.

---

## Open Decisions (confirm with Talal before Phase 1)

- [ ] Vision model: Claude / GPT-4o-class / open-weight.
- [ ] Output target: existing `.xlsx` / Google Sheet, or a DB + review UI.
- [ ] Checkout checks: leave all `Manual` for now, or automate the safe ones.
- [ ] Proxy provider (biggest reliability + cost factor at scale).
- [ ] Build scope: internal DevSplit tool vs. reusable/productized asset.

---

## Definition of Done

- [ ] Objective met
- [ ] `Method` column added; all 92 rows tagged
- [ ] Single-site run produces all 92 rows in checklist format
- [ ] ≥85% agreement with golden reference on DOM + Vision checks
- [ ] No fabricated observations (verified by QA spot-check)
- [ ] Speed sourced from PageSpeed API; manual-tier checks output `review`
- [ ] Batch runner handles blocked/failed sites gracefully
- [ ] Secrets kept out of git
- [ ] Branch created and changes committed locally (do not push unless told)
- [ ] Summary of changes written to `output/001-summary.md`

---

*Full design spec (architecture, per-category method breakdown, scaling,*
*accuracy, cost): CRO Audit Agent — Build Spec —*
*https://claude.ai/artifact/dd777661-8cf0-4887-adad-0c487786b598*
