# Expected findings baseline: reading-list (`examples/reading-list/`)

A passing `senior-design-review` run on `examples/reading-list/current/library.html` (with `current/tokens.css`, `context.md`, and `junior-proposal.md`) must catch these major issues:

## A. Structure and task fit
- **Type tabs miss the complaint:** Filtering by `All | Articles | Books | Videos | Papers` addresses neither recency ("what I saved last week") nor progress ("what I'm halfway through").
- **In-progress items are buried:** `reading` items sit mixed into the flat list instead of a dedicated "Continue reading" / in-progress region.
- **Substantiated Keep:** Keep the single-screen, single-column list structure rather than splitting into multiple screens or a two-column grid.

## B. Information architecture and hierarchy
- **No recency landmarks:** Dates only appear as per-row `.meta` text instead of scannable date headings (`This week`, `Last week`, `Earlier`).
- **Title truncation / narrow columns:** `.title` truncates to a single line with ellipsis (and a two-column grid halves width on phones), hiding long titles such as `r5` ("Budgeting for a first flat…").
- **Missing search:** No keyword search across title and source.

## C. Action semantics
- **Unlabelled primary button:** `.icon-btn` is a `+` glyph with no accessible name instead of a labelled `Add item` button.
- **Hidden overflow actions:** `.more` (`⋯`) buttons have no accessible name and hide the only route to item actions.
- **Reversible actions need undo, not confirmation:** Mark-as-read and remove should provide an undo action rather than silent completion or a modal delete confirmation.

## D. Mechanics and gestures
- **Swipe-only actions:** Relying solely on horizontal swipe gestures for mark-done/delete is invisible, keyboard-inoperable, and conflicts with mobile edge-swipe back navigation.
- **Small hit targets:** `.icon-btn` and `.more` are `32px × 32px`, below standard mobile touch target minimums (`44×44 pt` / `48×48 dp`).

## E. Visual and motion
- **Ad-hoc colour:** `#d39b2a` in `current/library.html` is hardcoded instead of using a design token (`--color-progress`).
- **Substantiated Keep:** Existing colour/spacing tokens (`current/tokens.css`) and vertical rhythm are sound and should be kept.
- **Reduced motion:** Any panel/toast transition must specify a `prefers-reduced-motion: reduce` alternative.

## F. Accessibility, states, and internationalisation
- **Status by colour alone:** `.dot.unread`, `.dot.reading`, and `.dot.done` (and the proposal's coloured borders) convey status by colour alone without text labels.
- **Row semantics:** List items (`<li>`) contain non-interactive spans and unnamed buttons instead of an accessible interactive control per row.
- **Missing states:** Empty library, no-results filter state, invalid-input/error state, and loading state are unspecified in `current/library.html`.
