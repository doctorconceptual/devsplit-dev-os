# CRO Audit Agent

An agent that takes an ecommerce store URL, runs it against a 92-point CRO
(conversion-rate optimization) checklist, and returns one result row per check —
`Exists? (Y/N/NA)` plus a confidence flag and an evidence note. It turns a
~30-minute manual site audit into a ~2-minute review-and-correct, so DevSplit's
cold outreach can pitch each prospect one real, verified conversion problem
found on their own site.

This is **build-and-calibrate, not model training.** No fine-tuning, no labelled
dataset. The checklist is the specification; the agent knows it as instructions,
and you tune those instructions against a golden reference until agreement is
high. A human always confirms the chosen observation before it enters an email.

---

## Folder contents

```
projects/cro-audit-agent/
├── README.md                     # this file
├── task-001-cro-audit-agent.md   # the task Hermes executes (DevOS task format)
├── cro-audit-checklist.xlsx      # the 92 checks + email lines + Method column (the spec)
└── sites-to-audit.xlsx           # INPUT: the list of store URLs to audit
```

**Full design spec** (architecture, per-category method breakdown, scaling,
accuracy, cost): CRO Audit Agent — Build Spec —
https://claude.ai/artifact/dd777661-8cf0-4887-adad-0c487786b598

---

## How it works

A hybrid pipeline routes each check to the method that can actually answer it.
The `Method` column in `cro-audit-checklist.xlsx` tells the agent which to use:

- **DOM** (61 checks) — a fact in the rendered HTML. Deterministic, reliable.
- **Vision** (20 checks) — a judgment from a screenshot (buried reviews,
  cluttered hero, mobile layout break).
- **API** (4 checks) — the site-speed checks, from Google PageSpeed Insights.
- **Manual** (7 checks) — needs a live checkout flow or a subjective call;
  output is marked `review`, never guessed.

```
Store URL
  ├─> Headless browser (Playwright): render desktop + mobile, screenshot both
  │     ├─> DOM extractor        -> DOM checks
  │     └─> Screenshots -> Vision model -> Vision checks
  ├─> PageSpeed Insights API      -> Speed checks
  └─> Result assembler -> 92-row output (Y/N/NA + confidence + evidence + method)
        └─> Human review (confirm + pick the email line)
```

Each store is loaded **twice** — desktop and mobile viewport. Many checks
(sticky Add to Cart, tap targets, mobile layout) only exist on mobile.

---

## Input / output

- **Input:** `sites-to-audit.xlsx`. One store per row: `Store URL`, `Niche`,
  and `Status = Pending`. The agent audits every Pending row and updates its
  `Status`, `Date Audited`, and `Output File / Link`.
- **Output:** one 92-row result per store, in the `cro-audit-checklist.xlsx`
  column format, with `Exists?`, `Confidence`, `Evidence`, and the pre-written
  `Email line` (when `Exists? = Y`).

---

## Build phases

1. **Phase 1 — Single-site prototype.** Scaffold, load site desktop+mobile,
   implement DOM checks, add PageSpeed for speed, add the vision layer, output
   92 rows for one store. (First run: Lo & Co Interiors, already in the input.)
2. **Phase 2 — Calibration.** Manually audit 3–5 stores across niches (golden
   reference); diff the agent's answers; fix rules/prompts until ≥85% agreement
   on DOM + Vision checks.
3. **Phase 3 — Batch runner.** Queue one job per URL, add retries/timeouts and a
   residential proxy pool, handle blocked sites as `could not audit`, run the
   full list.

---

## Guardrails (non-negotiable)

- **Never fabricate an observation.** A check that can't be verified outputs
  `unsure`, never a guessed Y/N. A false observation in a cold email is worse
  than a missing one.
- **Physically interact with the site.** DOM checks read the *rendered* DOM
  after settle; cart checks actually add an item and open the cart.
- **Speed from the API, not a guess.** The 4 speed checks use PageSpeed output.
- **Evidence required on every non-NA row.**

---

## Running it (once built)

See `task-001-cro-audit-agent.md` for the full task, branching, acceptance
criteria, and open decisions. Secrets (PageSpeed key, vision-model key, proxy
credentials) live in a gitignored `.env` / `credentials.local.md`, never in
this repo.
