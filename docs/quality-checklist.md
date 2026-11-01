# Quality checklist

Use these gates to decide whether the output is worth acting on. Each item is falsifiable: someone else can check it and get the same answer.

## Evidence labels

Mark every claim in a handoff with one of:

| Label | Meaning |
| --- | --- |
| **Verified** | Observed or computed, with the method stated (e.g. "opened in a browser at 375 px width; filters work"). |
| **Unverified** | Plausible but not checked (e.g. "should be feasible natively"). |
| **Assumption** | Chosen for lack of information; listed in open questions. |

Never present an unverified item as verified.

## Meaningful review gate

- [ ] Review mode stated: independent fresh-context reviewer, or single-agent separate pass (not independent peer review).
- [ ] Evidence read before the proposal is listed by path.
- [ ] Each finding names a file, token, component, screenshot region or named reference pattern.
- [ ] No platitudes ("improve hierarchy") without a concrete change.
- [ ] No invented contrast ratios, WCAG levels or metrics.
- [ ] States: empty, loading, error, long content.
- [ ] Keyboard and screen-reader paths for every action; alternatives for gestures.
- [ ] Reduced-motion behaviour for every animation.
- [ ] Text expansion and (where relevant) right-to-left considered.
- [ ] Ledger: each row has decision, item, reason and reference; Keeps are substantiated; no change for its own sake.
- [ ] Section H is implementable; acceptance criteria are testable.

## Working prototype gate

- [ ] Opens from `file://` with the network off; no external resources.
- [ ] Viewport meta present; usable at phone and desktop widths.
- [ ] Every visible primary action works.
- [ ] Empty and error states reachable from the UI.
- [ ] Keyboard-only operation; visible focus; dialogs manage focus and close with Escape.
- [ ] `prefers-reduced-motion` respected.
- [ ] Synthetic data labelled on screen.
- [ ] Change ledger present if grafted from a direction; no unlisted redesign.
- [ ] Handoff states the prototype is not proof of native feasibility or production readiness.
- [ ] Nothing published automatically.

## Directions gate

- [ ] Two or three directions share the same task, constraints and data.
- [ ] They differ in IA or interaction model, not only colour.
- [ ] Comparison page states trade-offs and who each suits.
- [ ] Production mode stated (independent or serial).
- [ ] The agent waited for the user's choice.
