---
description: Product discovery interview for any app or software idea. No code, no installs. Ends with an approved spec written to docs/.
---

Run product discovery for this idea: $ARGUMENTS

## Mode rules (DISCOVERY MODE)
- Do NOT write application code, install packages, scaffold the project or
  change config during discovery. The only files you may write are the
  `docs/` files listed under "After approval", and only after I approve.
- Ask 1–3 focused questions at a time, highest value first, and wait. If a
  question has a small set of sensible answers, offer them as lettered
  options so I can reply with one character. Never send a long questionnaire.
- If I don't know an answer, explain the practical options, recommend one,
  and label it RECOMMENDATION. Never silently turn a suggestion into a
  requirement.
- Before asking anything, read everything in `reference/` (documents, notes,
  screenshots, design exports such as `DESIGN.md`, `code.html`, `screen.png`)
  and any existing `docs/` or README. List what you found in 3–5 lines and say
  what it already answers. Then ask only what is missing. If `reference/`
  does not exist, say so and ask whether I have material to add.

## Topics (cover as relevant, skip what doesn't apply)
1. Users and use cases — who, how many, what job they hire this for, what
   currently frustrates them; personal tool vs commercial product.
2. Core objects and data — what the product stores, who owns it, sharing.
3. Core workflows — the 3–5 journeys that must work on day one.
4. Platform — web, iOS, Android, desktop, tablet; responsive vs native;
   offline needs; device permissions (location, camera, notifications).
5. Accounts, roles and privacy — auth method, roles, retention, export,
   deletion, regulated or sensitive data.
6. Integrations and content — external services, data sources, notifications,
   payments, any guidance/advice text that needs a trusted source.
7. AI features — include, defer or exclude, and what must never be claimed.
8. Accessibility, language, usability standards; and whether a UI design
   already exists (Antigravity/Stitch/Figma export) to build from.
9. Business model and future scope — free/paid/subscription; multi-user,
   teams, admin; what is deliberately deferred.
10. Scope — minimum useful first release; what would make me use it
    regularly; what is explicitly excluded.

## Running register (show a compact version every few turns)
Confirmed decisions · Open questions · Assumptions · Deferred features ·
Risks and external dependencies.

## Draft for approval
When you have enough, present a concise draft (in chat, not files):
overview and users; problems and goals; first-release features; deferred and
excluded; core user journeys; data stored; platform/offline/notification/
permission/backup/privacy/accessibility requirements; monetisation
assumptions; acceptance criteria per first-release feature (observable and
testable); open questions, assumptions, dependencies, risks; and a proposed
phased plan where each phase is independently testable.

Never claim the product can do what it cannot (diagnosis, guaranteed
schedules, legal/medical/financial certainty). If it gives guidance, say how
uncertainty is shown and which content needs expert review.

## After I explicitly approve the draft
1. Copy `~/.claude/templates/build/docs/` into `./docs/` (skip files that
   already exist) and fill PRODUCT-SPEC.md, USER-FLOWS.md,
   ACCEPTANCE-CRITERIA.md and RISKS.md from the approved draft, marking
   anything unconfirmed `ASSUMPTION:` or `OPEN:`. Set the project name in
   every copied file, including the empty `BACKLOG.md`.
2. If the product gives domain guidance or copy needing review, create
   `docs/CONTENT-REVIEW.md` (domain, trusted sources, required disclaimers,
   house style).
3. Commit `docs: add approved product specification`.
4. Tell me the next step is `/setup-build` and stop.
