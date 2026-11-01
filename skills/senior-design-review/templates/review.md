# Senior design review: <screen or flow name>

- **Review mode:** <Independent fresh-context reviewer | Single-agent separate pass — not independent peer review>
- **Evidence read (in order):** tokens `<path>`, canonical component `<path>`, prior example `<path or none>`, target `<path / screenshots>`, constraints `<source>`, proposal `<path>`
- **Not available:** <list anything missing>

## TL;DR

<Verdict in one sentence.> <The single most important change.> <What to keep.>

## A. Structural critique

Is this the right screen, in the right place in the flow? Should anything merge, split or disappear?

- **Finding:** … **Evidence:** `<file:line>` / screenshot region / named pattern. **Recommendation:** …

## B. Information architecture and hierarchy

- **Finding:** … **Evidence:** … **Recommendation:** …

## C. Action semantics

Primary vs secondary vs destructive; naming; confirmation vs undo.

- **Finding:** … **Evidence:** … **Recommendation:** …

## D. Mechanics and gestures

Tap targets, swipe, drag, long-press, keyboard equivalents, discoverability.

- **Finding:** … **Evidence:** … **Recommendation:** …

## E. Visual and motion

Tokens, rhythm, density, emphasis, transitions.

- **Finding:** … **Evidence:** … **Recommendation:** …

## F. Accessibility and internationalisation

Non-colour signals, focus order, screen-reader labels, text expansion, RTL, reduced motion, states (empty/loading/error/long content). State "not measured" for any contrast or size figure you did not compute.

- **Finding:** … **Evidence:** … **Recommendation:** …

## G. Missing questions

Up to five; only those that would change the design.

1.

## H. Refined specification

### Layout

```text
<IA sketch of the refined design>
```

### Components and tokens

| Element | Component | Tokens | Notes |
| --- | --- | --- | --- |
| | | | |

### Interactions

| Trigger | Result | Keyboard / screen reader equivalent | Reduced motion |
| --- | --- | --- | --- |
| | | | |

### States

| State | Content | Action available |
| --- | --- | --- |
| Empty | | |
| Loading | | |
| Error | | |
| Long content | | |

### Cut / Add / Revise / Keep ledger

| Decision | Item | Reason | Reference |
| --- | --- | --- | --- |
| Keep | | | |
| Revise | | | |
| Add | | | |
| Cut | | | |

### Acceptance criteria

- [ ] <falsifiable check, e.g. "With 'Large' system text, the title wraps to two lines and the due date remains visible">
