# Accessibility and internationalisation checklist

Use this for section F. Report what you checked and how. If you did not measure something, say "not measured".

## Perception

- [ ] Status, selection and errors are conveyed by text, icon or shape as well as colour.
- [ ] Contrast: either computed (state the two colour values and the method) or marked "not measured — verify with a contrast checker". Never guess a ratio.
- [ ] Text scales with system or browser settings without clipping or overlapping.
- [ ] Icons that carry meaning have accessible names.

## Operation

- [ ] Every action is reachable by keyboard (web/desktop) or by screen-reader actions (mobile).
- [ ] Focus order follows visual reading order.
- [ ] Focus is visible on every interactive element.
- [ ] Custom gestures (swipe, drag, long-press) have an alternative control.
- [ ] Opening a dialog or sheet moves focus into it; closing returns focus to the trigger.
- [ ] No time limits without a way to extend.

## Understanding

- [ ] Labels describe outcomes ("Delete list", not "Confirm").
- [ ] Errors say what went wrong and how to fix it, next to the relevant field.
- [ ] Empty states explain why it is empty and offer the next action.

## Motion

- [ ] Every animation respects reduced-motion preferences (`prefers-reduced-motion` on the web; the OS setting on mobile).
- [ ] No flashing content.

## Internationalisation

- [ ] Layout tolerates text roughly 30–40% longer than English (a common planning allowance, not a guarantee).
- [ ] No text baked into images.
- [ ] Dates, numbers and plurals use locale-aware formatting.
- [ ] Right-to-left mirroring considered where the product supports RTL languages.
- [ ] Truncation has a way to reveal the full string.

## States

- [ ] Empty
- [ ] Loading (skeleton or progress; announced to screen readers if it takes noticeable time)
- [ ] Error (recoverable, with retry)
- [ ] Offline, if relevant
- [ ] Long content (very long titles, many items)
- [ ] Minimal content (one item, one-word title)
