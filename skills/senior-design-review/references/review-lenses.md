# Review lenses

Guidance for each section of the review. Use it as a lens, not a checklist to recite.

## A. Structural critique

- Does the screen exist for one clear job? If it serves three, which one wins?
- Could the task be done in-context (sheet, inline edit) rather than a new screen?
- Is the proposal solving the quoted pain point, or a nearby problem that is easier to draw?
- A justified **Keep** of the current structure is a valid outcome. Say why it works.

## B. Information architecture and hierarchy

- What must the user see in the first second? Is it the most prominent thing?
- Group by user intent, not by data model.
- Check that progressive disclosure hides only what is genuinely secondary.
- Compare hierarchy to the canonical component: deviations need a reason.

## C. Action semantics

- One primary action per view. If there are two, the design is undecided.
- Labels are verbs that describe the result ("Mark as read", not "OK").
- Prefer undo over confirmation for reversible actions; confirm only destructive, irreversible ones.
- Destructive actions are separated spatially and not styled as primary.

## D. Mechanics and gestures

- Every gesture has a visible, tappable or keyboard equivalent. Swipe-only actions are invisible to many users.
- Touch targets follow the platform's documented minimum; cite the platform guideline rather than inventing a number.
- Avoid gesture conflicts with system navigation (edge swipes, pull-to-refresh).
- Long lists need a way to jump, filter or search.

## E. Visual and motion

- Use existing tokens. A new token needs a reason and a name.
- Spacing rhythm should be consistent with the canonical component.
- Motion explains a change of state or place; decorative motion is a cut candidate.
- Provide a reduced-motion alternative (cross-fade or instant change).

## F. Accessibility and internationalisation

See [accessibility-i18n.md](accessibility-i18n.md).

## G. Missing questions

Good questions change the design depending on the answer. "What is the brand colour?" is rarely one; "Can a reading item belong to more than one list?" often is.

## H. Refined specification and ledger

- The specification must be buildable without a follow-up meeting: layout, components, tokens, interactions, states, acceptance criteria.
- Every ledger row has a decision, an item, a reason and a reference.
- Order the ledger by impact, not by decision type, if that reads better.

## Named reference patterns

Citing a well-known pattern is valid evidence when you name it precisely, for example:

- "Segmented control as filter (iOS Settings › Notifications style)"
- "Bottom sheet with detents (Apple Maps place card)"
- "Swipe-to-archive with undo snackbar (common email clients)"
- "Master–detail split on wide viewports"

Do not claim a specific product currently behaves a certain way unless you have checked.

## Acceptance checks

A review passes when:

- [ ] Review mode is stated honestly (independent vs single-agent separate pass).
- [ ] Every finding cites a file, token, component, screenshot region or named pattern.
- [ ] No unmeasured contrast ratios, WCAG levels or metrics are presented as fact.
- [ ] Empty, loading, error and long-content states are specified.
- [ ] Every action has a keyboard and screen-reader path.
- [ ] Every animation has a reduced-motion alternative.
- [ ] The ledger contains at least one substantiated Keep, or explains why nothing should be kept.
- [ ] Section H could be handed to an engineer without further clarification, apart from the listed open questions.
