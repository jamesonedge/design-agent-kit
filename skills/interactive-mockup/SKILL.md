---
name: interactive-mockup
description: Produce two or three genuinely distinct design directions as static HTML, let the user choose, then build a working, self-contained offline HTML/CSS/vanilla-JS prototype by strictly grafting interactions onto the chosen direction. Use when asked to mock up, prototype, explore directions, or make a clickable demo of a screen or flow. Do not use for pure critique without building (use a design review), for production code, or for tiny visual tweaks.
license: MIT
metadata:
  version: "0.1.0"
---

# Interactive mockup

Explore real alternatives, let the user pick, then make the pick work in a browser — without quietly redesigning it.

## When to use

- "Mock up", "prototype", "show me some directions", "make this clickable".
- A design review has produced a specification and the user wants to feel it.
- Greenfield screens where the information architecture is still open.

## When not to use

- Critique only, with no build — use a design review workflow.
- Production implementation in the app's real framework.
- A single padding, colour or copy change.
- Anything needing real user or production data. Prototypes use synthetic data only.

## Inputs

- The task and constraints (platform, viewport, tokens if available).
- Representative **synthetic** data. Label it as synthetic in the UI. Never paste production or personal data.
- Optional: a design review or specification to honour.
- Optional: a direction the user has already chosen. If so, **skip divergence** and go straight to step 3.

## Workflow

### 1. Diverge: two or three direction briefs

Write a brief per direction using [templates/direction-brief.md](templates/direction-brief.md). Every direction shares the **same constraints, data and task**. They must differ in information architecture or interaction model — for example list-first vs focus-mode vs board — not merely in colour scheme.

- If your runtime supports genuinely independent workers (sub-agents or separate sessions), generate directions independently and say so.
- Otherwise generate them serially and label them: **"Directions produced serially by one agent."**

Build each as a static, self-contained HTML file from [templates/direction.html](templates/direction.html). Static means representative layout and states; interactions are not required yet.

### 2. Compare and let the user choose

Create a comparison page from [templates/comparison.html](templates/comparison.html) that links each direction and states the meaningful trade-offs (what each optimises, what it sacrifices, who it suits). **Stop and ask the user to choose.** Do not build the interactive version before they choose, unless they explicitly delegate the choice.

### 3. Strict graft: build the interactive prototype

Follow [references/graft-rules.md](references/graft-rules.md). In short:

1. Read the chosen direction's HTML source.
2. Preserve its markup structure, CSS and visual decisions.
3. Namespace any new classes or IDs that could collide.
4. Add working interactions with vanilla JavaScript.
5. Record every change in a ledger using [templates/change-ledger.md](templates/change-ledger.md). Anything that is not a pure addition needs a reason.

No silent redesign. If the chosen direction has a flaw, record it in the ledger and ask before changing it.

### 4. Quality gate

Check the prototype against [references/prototype-quality.md](references/prototype-quality.md): offline, viewport meta, responsive, keyboard, visible focus, reduced motion, empty/loading/error states, no dead primary actions, synthetic data labelled.

## Defaults

- One self-contained `.html` file per artefact: inline CSS and JS, no CDN, no web fonts, no external images (use inline SVG or CSS).
- System font stack.
- Works from `file://` with no server.
- Never publish, deploy or upload automatically.

## Outputs

```text
<output-dir>/
├── directions/
│   ├── a-<name>.html
│   ├── b-<name>.html
│   └── c-<name>.html   (optional)
├── comparison.html
├── prototype.html
└── change-ledger.md
```

## Honesty

A prototype demonstrates interaction and layout. It is **not** evidence of native feasibility, performance, accessibility conformance or production readiness. Say so in the handoff.


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
