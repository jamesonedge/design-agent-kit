# Example: "Shelf" reading list

> **Illustrative synthetic example.** "Shelf" is a fictional app. The complaint, titles, sources and dates are invented to show the workflow. Nothing here is user research, a usability result or a product metric. The files were prepared in advance by one agent working serially; they are sample output, not evidence that any runtime loaded the skills.

## The sequence

| Step | Skill | File |
| --- | --- | --- |
| 1. Context and synthetic data | — | [context.md](context.md), [fixture.json](fixture.json) |
| 2. "Before" screen | — | [current/library.html](current/library.html), [current/tokens.css](current/tokens.css) |
| 3. A junior proposal to pressure-test | — | [junior-proposal.md](junior-proposal.md) |
| 4. Senior review: critique A–H, refined spec, ledger | `senior-design-review` | [review.md](review.md) |
| 5. Three distinct static directions | `interactive-mockup` | [directions/a-sections.html](directions/a-sections.html), [directions/b-next-up.html](directions/b-next-up.html), [directions/c-board.html](directions/c-board.html) |
| 6. Comparison and choice | `interactive-mockup` | [comparison.html](comparison.html) |
| 7. Strict graft of the chosen direction | `interactive-mockup` | [prototype.html](prototype.html), [change-ledger.md](change-ledger.md) |

Open the HTML files directly in a browser. They need no server, network or build step.

## What improves, and why

- The review keeps what already works (single list, existing tokens) instead of forcing a redesign, and cuts the two-column grid and swipe-only actions with reasons.
- Status is shown as text, not only colour; "+" becomes "Add item".
- The directions differ in structure (sections, a single recommendation, a board), not just colour, so the choice is a real trade-off.
- The prototype grafts Direction A without restyling it, and every addition is listed in the ledger.

## Manual acceptance checks

Use [prototype.html](prototype.html) in a current desktop browser and at a narrow (about 375 px) width.

1. "Continue reading" lists exactly two items, both badged "Reading".
2. Type `tidal` in search: one item is shown and the count reads "1 item".
3. Press "Done", then choose "Books" in the type filter: the no-results message appears; "Clear filters" restores all 12 items and returns focus to search.
4. Activate a row with Enter: the detail dialog opens with focus on its title. Choose "Reading" with the arrow keys; the row moves to "Continue reading" and an undo message appears. Press Escape: focus returns to the row.
5. Open a row, choose "Remove", then "Undo" within five seconds: the item returns.
6. Choose "Add item" and submit empty: "Enter a title." appears and focus moves to Title. Enter `ftp://x` as the address: the web-address error appears. Fix both and save: the item appears under "This week".
7. Set "Demo data state" to "Empty library": the empty message and a working "Add item" appear. Set it to "Load error": the error message and a working "Try again" appear.
8. The long "Budgeting for a first flat…" title wraps to two lines in the list and shows in full in the detail dialog.
9. With reduced motion enabled in the operating system, dialogs appear without animation.
10. Tab through the page: every control is reachable, has a visible focus ring and does something.

Further regression checks for the detail layout, undo after Add, address validation and hit targets are in [tests/browser-checks.md](../../tests/browser-checks.md).

These are manual checks. Their results are not recorded in this repository; record your own if you rely on them.

## Not shown

Persistence, large libraries and right-to-left text. See [change-ledger.md](change-ledger.md#known-gaps).
