---
name: senior-design-review
description: Pressure-test a UI design proposal or existing screen with an evidence-based senior design critique, then produce an implementable refined specification and a Cut/Add/Revise/Keep ledger. Use when asked to review, critique, or rethink a screen, flow, or design proposal. Do not use for single padding, colour, or copy tweaks, for building prototypes (use an interactive mockup workflow instead), or for code review unrelated to UI.
license: MIT
metadata:
  version: "0.1.0"
---

# Senior design review

Turn a vague "make this better" into a falsifiable design decision. The output is a structured critique that cites real files, tokens and reference patterns, followed by a specification an engineer can build.

## When to use

Use this skill when the user asks to:

- review, critique or "pressure-test" an existing screen, flow or component;
- assess a proposal written by someone else (for example a junior designer or another agent);
- decide what to cut, add, revise or keep before implementation;
- correct a mobile flow from screenshots.

## When not to use

- **Small, local fixes** such as "increase the padding on this card" or "change this label to 'Save'". Make the change directly; a full review is noise.
- **Building an interactive prototype.** Use an interactive mockup workflow; this skill may feed it.
- **Non-UI code review**, performance tuning or back-end design.
- **Brand or marketing strategy** with no concrete interface.

## Inputs

Gather what the repository or user can safely supply. Missing inputs are listed as open questions, never invented.

1. Design tokens (colour, type, spacing, radius, motion) — file paths.
2. The canonical existing component(s) the target should resemble.
3. A prior approved example of similar work, if one exists (optional, useful).
4. The target implementation and/or screenshots.
5. Known platform constraints (navigation model, OS conventions, minimum targets).
6. The user's complaint, quoted verbatim where possible.

A fill-in context form is in [templates/context.md](templates/context.md).

## Workflow

### 1. Draft an explicit initial proposal

Before any critique, write the proposal down using [templates/proposal.md](templates/proposal.md): problem, quoted pain points, design principles, an information-architecture sketch, actions, and open questions. If the user supplied a proposal, use theirs unchanged as the input.

### 2. Run the review as a fresh pass

The reviewer reads, in this order: tokens, canonical component, prior example, target implementation/screenshots, platform constraints, and only then the proposal. Reading the evidence first prevents anchoring on the proposal's framing.

- If your runtime can start a genuinely separate context (a sub-agent or new session with no shared history), use it and say so.
- If not, run a separate pass yourself and label it honestly: **"Single-agent separate pass — not independent peer review."**

The reviewer persona is a *quality lens* (a demanding senior product designer). Never claim employment history, credentials or years of experience on behalf of the persona.

### 3. Write the review

Use [templates/review.md](templates/review.md). Sections:

- **TL;DR** — three to five lines: verdict and the most important change.
- **A. Structural critique** — is this the right screen/flow at all?
- **B. Information architecture and hierarchy**
- **C. Action semantics** — primary, secondary, destructive, undo, naming.
- **D. Mechanics and gestures** — taps, swipes, drag, keyboard, discoverability.
- **E. Visual and motion** — tokens, rhythm, density, transitions.
- **F. Accessibility and internationalisation**
- **G. Missing questions** — aim for five, but only include meaningful ones.
- **H. Refined specification** plus the **Cut / Add / Revise / Keep ledger**.

Detailed guidance for each lens is in [references/review-lenses.md](references/review-lenses.md). The accessibility and i18n checklist is in [references/accessibility-i18n.md](references/accessibility-i18n.md).

## Rules that make the review worth reading

- **Pressure-test; do not rubber-stamp.** Every claim needs a specific reference: a file path, token name, component name, screenshot region or a named reference pattern (for example "iOS Mail swipe-to-archive").
- **No platitudes.** "Improve visual hierarchy" is not a finding. "The 'Due' date uses `text.secondary` at the same size as the title, so the deadline is invisible at a glance" is.
- **No forced cuts.** If the current structure is right, say so and record a substantiated **Keep**. Change for its own sake is a defect.
- **No invented measurements.** Do not state contrast ratios, WCAG pass/fail levels or performance figures unless you computed or measured them, and show how. Otherwise write "not measured — verify with a contrast tool".
- **Cover states.** Empty, loading, error, offline, long content, and very short content.
- **Non-colour signals.** Status must never rely on colour alone.
- **Keyboard and screen reader** paths for every action, including custom gestures.
- **Text expansion** (allow roughly 30–40% longer strings for many languages) and right-to-left layout where relevant.
- **Reduced motion** alternative for every animation.

## Optional: compare with prior work

If a prior approved example exists, add a short "Consistency with prior work" note under E or H. This is useful, not mandatory.

## Outputs

- `proposal.md` (if you drafted it)
- `review.md` containing TL;DR, A–H and the ledger
- A short summary to the user: verdict, top three changes, and the open questions that block implementation

## Acceptance checks

See [references/review-lenses.md#acceptance-checks](references/review-lenses.md#acceptance-checks). A review fails if any ledger row lacks a reason and a reference, or if it states unmeasured numbers as fact.


## Licence notice

The following notice travels with this standalone skill and its supporting files.

```text
MIT License

Copyright (c) 2026 jamesonedge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
