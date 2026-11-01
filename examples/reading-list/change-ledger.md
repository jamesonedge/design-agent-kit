# Change ledger: Direction A (Sections) → prototype

- **Source:** [directions/a-sections.html](directions/a-sections.html)
- **Output:** [prototype.html](prototype.html)
- **Graft mode:** strict, with the explicit hit-target correction in entry 11. Other Direction A tokens, CSS rules and markup structure are preserved; new classes use the `.pt-` prefix; unprefixed additions are `--color-danger` and an `[aria-invalid]` border rule.
- **Data:** the 12 items in [fixture.json](fixture.json), embedded in the page so it opens from a local file. Synthetic.

| # | Type | Element or rule | Reason | User approved? |
| --- | --- | --- | --- | --- |
| 1 | Changed | Static rows → rows rendered from data, grouped by section | Needed for search, filters and status changes; markup per row is identical to the source | n/a (same markup) |
| 2 | Added | Behaviour for search, status chips and item count (`aria-live`) | Review H: interactions table | n/a (addition) |
| 3 | Added | Type filter (`select.pt-type`) beside the chips | Review H: "Type ▾" secondary filter; not drawn in Direction A | assumed approved in this synthetic scenario, not a real user approval |
| 4 | Added | Detail dialog with status radio group, Mark as read, Remove, Close | Review H: detail panel | assumed approved in this synthetic scenario, not a real user approval |
| 5 | Added | Add item dialog with inline validation | Review H: add dialog and invalid-add state | assumed approved in this synthetic scenario, not a real user approval |
| 6 | Added | Undo message (`.pt-toast`, 5 seconds) | Review C2: undo replaces confirmation | assumed approved in this synthetic scenario, not a real user approval |
| 7 | Added | Empty, no-results and load-error states | Review H: states table; load error added so the error path can be demonstrated | n/a (addition) |
| 8 | Added | "Demo data state" selector | Prototype-only control to reach empty and error states; not part of the design | n/a (prototype tool) |
| 9 | Added | `--color-danger` token | Taken from [current/tokens.css](current/tokens.css) for Remove and errors | n/a (existing token) |
| 10 | Changed | Banner text | States that it is an interactive prototype and changes reset on reload | n/a |
| 11 | Changed | `.chip` `min-height` 36px → 44px, in both [directions/a-sections.html](directions/a-sections.html) and the prototype | Matches the 44px minimum Direction A already sets on `.btn`; not measured against a platform guideline | n/a (source revised to match) |
| 12 | Changed | `.pt-type`, `.pt-toast .btn`, the demo-state select and Add dialog fields: `min-height` 44px | Same hit-target minimum as `.btn` | n/a (prototype additions) |
| 13 | Changed | Detail dialog (`#detail.pt-side`): bottom sheet below 768px, right-side panel (up to 400px wide, full height) from 768px; slides in unless reduced motion is set. The Add dialog stays centred | Review H: "sheet on phone, side panel ≥ 768 px"; E4 motion | assumed approved in this synthetic scenario, not a real user approval |
| 14 | Changed | Add item can be undone; undo restores the previous list and demo state and returns focus to "Add item". Changing the demo data state clears any pending undo | The undo message after Add previously had no snapshot behind it | n/a (fix) |
| 15 | Changed | Web address check parses the value and requires `https:` and a host name; malformed values show the field error | The earlier pattern accepted some values that then failed to parse. This is a format check only; nothing is fetched | n/a (fix) |

Apart from entry 11, no Direction A rule was removed or restyled. Directions B and C were not changed.

## Known gaps

- The detail sheet and panel are modal, so the page behind is inert. An undo message raised from inside the detail can only be used after closing it, and on phones the sheet covers it while open.
- Data is not saved; reload resets it. Reading minutes for added items are placeholders.
- "Continue reading" is not paginated; behaviour with hundreds of items is not shown.
- Text expansion and right-to-left layouts have not been checked.

## Not evidence of

Native feasibility, performance, accessibility conformance or production readiness. No contrast ratios or usability results were measured.
