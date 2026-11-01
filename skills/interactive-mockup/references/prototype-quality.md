# Prototype quality gate

Each item is checkable by opening the file in a browser. Record pass, fail or not checked — do not assume.

## Self-contained

- [ ] Opens from `file://` with networking disabled.
- [ ] No `<link>` or `<script src>` to remote hosts; no `@import` of remote CSS; no web fonts.
- [ ] Images are inline SVG, CSS or data URIs.

## Layout

- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">` is present.
- [ ] Usable at a narrow phone width and at a desktop width without horizontal scrolling.
- [ ] Long titles wrap or truncate with access to the full text.

## Interaction

- [ ] Every primary action works (no dead buttons).
- [ ] Filters, selection, detail view and creation (or the scoped equivalents) work with the synthetic data.
- [ ] Empty state is reachable (for example by filtering to nothing) and offers a next action.
- [ ] Error state is reachable (for example invalid input) and explains how to recover.
- [ ] Loading state is shown where the real product would wait, if relevant.

## Accessibility

- [ ] Every control is reachable and operable with the keyboard alone.
- [ ] Focus is always visible.
- [ ] Dialogs move focus in, trap it while open, close with Escape and return focus to the trigger.
- [ ] Controls have accessible names; state changes are announced via `aria-live` where helpful.
- [ ] Status is not conveyed by colour alone.
- [ ] `prefers-reduced-motion: reduce` removes or shortens animation.
- [ ] Contrast: not claimed unless measured; state the method if you did.

## Honesty

- [ ] A visible note says the data is synthetic.
- [ ] The handoff says the prototype is not evidence of native feasibility or production readiness.
- [ ] Nothing was published or uploaded.
