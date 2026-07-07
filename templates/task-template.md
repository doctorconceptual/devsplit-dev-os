# Task: [0XX] - [Short Title]

**Project:** [project-name]
**Task ID:** 0XX
**Created:** [YYYY-MM-DD]
**Priority:** [Low / Medium / High]
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
- `.devos/knowledge/laravel/` — architecture.md, project-structure.md, and any
  file directly relevant to the layer(s) this task touches
- `docs/` and `notes/` in this project, if present
- HERMES.md (workspace root)

If a document referenced above doesn't exist, say so explicitly rather than
proceeding as if it does.

---

## Objective

[One paragraph, plain language: what business problem this solves and why it matters.]

---

## Before Doing Anything Else

1. Restate any credentials, URLs, IDs, or file paths referenced in this task
   file back to me **verbatim**, before using them.
2. If `code/` has not been cloned yet, follow the HERMES.md first-time setup
   sequence.
3. Bring up the local environment (containers/services) and confirm status.
4. State the exact local URL(s) you will be testing against.
5. If this task depends on a prior task's work, confirm whether that prior
   task's branch has already merged into `main`. If it has, pull latest
   `main` and branch from it as normal below. If it has **not**, branch from
   the prior task's branch instead — do not assume `main` is current just
   because it's the default. If unsure which applies, stop and ask.
6. Pull latest `main` (or the correct base branch per the step above) and
   create branch: `feature/0XX-[slug]`

Do not guess credentials, URLs, ports, or file paths. If something referenced
here is missing, wrong, or unclear once you look at the actual project, stop
and ask — do not substitute your own assumption.

---

## Credentials / Access (if applicable)

> Note: avoid pasting live/production credentials directly into this file.
> Task files live in a git-tracked repo — plaintext secrets here persist in
> history even if later removed. Prefer a **gitignored** `credentials.local.md`
> in this project's root and reference it from here instead.

- Reference: [where the credentials actually live]
- Scope: [read-only / staging / production — state explicitly]

---

## Scope of Work

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

---

## Out of Scope / Do Not Touch

- [List explicitly — files, features, or areas this task should not touch]

---

## Acceptance Criteria / Manual QA Steps

1. [Step]
2. [Step]
3. [Step]

---

## General Instructions

- Read every affected file before making changes.
- Do not break any existing functionality.
- Run `php artisan migrate:status`. If any migration is pending, run
  `php artisan migrate` before considering this task complete — do not
  decide on your own that it "isn't needed." Verify, don't assume.
- Clear caches after changes:
  `php artisan cache:clear && php artisan view:clear && php artisan config:clear && php artisan route:clear`
- Confirm the local server/environment runs with no errors after all changes.
- Actually view every screen/state this task touches in the browser and read
  the rendered output. "No errors thrown" is not sufficient — check for
  leaked template syntax, unconverted variable references, or
  `undefined`/`null`/`NaN` appearing as visible text.
- Actually click/tap and type into every interactive element this task adds
  or touches (buttons, inputs, links). A visible element that doesn't
  respond to interaction is not done — do not hand off work where this
  hasn't been physically confirmed.
- Follow DevOS engineering standards (see Required Reading above).
- Make the smallest reasonable change that satisfies the objective.

---

## Escalate / Stop and Ask If

- Any credential, URL, or path referenced here doesn't match what you find.
- The work requires an architecture change beyond what's described.
- Existing tests fail and the cause isn't clearly related to this task.
- Anything in this file conflicts with a DevOS document.
- A referenced DevOS document, playbook, or checklist doesn't exist.

---

## Definition of Done

- [ ] Objective met
- [ ] Existing functionality preserved
- [ ] All acceptance criteria pass
- [ ] `php artisan migrate:status` shows no pending migrations
- [ ] Caches cleared, environment verified running
- [ ] Branch created and changes committed locally (do not push unless told)
- [ ] Summary of changes written to `output/0XX-summary.md`
