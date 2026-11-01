# Senior design review: Shelf — Library screen

> Illustrative synthetic example produced with the `senior-design-review` skill. It demonstrates the structure and rigour of a review; it is not user research and contains no measured product metrics.

- **Review mode:** Single-agent separate pass — not independent peer review. (The example was authored in one context; a runtime with sub-agents should use a fresh-context reviewer.)
- **Evidence read (in order):** tokens [current/tokens.css](current/tokens.css); canonical component — list row in [current/library.html](current/library.html); prior example — none; target — [current/library.html](current/library.html); constraints — [context.md](context.md); proposal — [junior-proposal.md](junior-proposal.md).
- **Not available:** usage analytics, real screenshots from devices, information on how items are added (share sheet vs paste).

## TL;DR

The proposal restyles the screen but does not address either half of the complaint: finding last week's saves, and seeing what is in progress. Replace the type tabs and two-column grid with a status-first list that keeps the existing row component, adds "Continue reading" at the top, date-grouped sections, search and status filters, and visible, undoable actions. Keep the single-column row and the token set; they are sound.

## A. Structural critique

1. **The proposal solves a different problem.** The complaint has two parts — recency ("what I saved last week") and progress ("what I'm halfway through"). The proposed tabs filter by *type* (`All | Articles | Books | Videos | Papers`), which answers neither. **Evidence:** pain-point quote in [junior-proposal.md](junior-proposal.md#pain-points-quoted) vs IA sketch in the same file. **Recommendation:** organise by status and recency; demote type to a secondary filter.
2. **In-progress items deserve their own region.** Two of twelve fixture items are `reading` ([fixture.json](fixture.json)); in the current list they sit at positions 2 and 7, separated by unrelated rows ([current/library.html](current/library.html)). **Recommendation:** a "Continue reading" section pinned above the list, shown only when at least one item is in progress.
3. **Keep a single screen.** No need for a separate "Progress" screen or tab bar; the job is small enough for one scrolling view with filters. This is a deliberate **Keep** of the current one-screen structure.

## B. Information architecture and hierarchy

1. **Recency needs landmarks.** Dates appear as right-aligned meta text (`.meta`, `--font-size-meta`, `--color-text-secondary`) on each row, so "last week" requires reading every date. **Recommendation:** group the list under section headings — "This week", "Last week", "Earlier" — computed relative to today. Headings are real `<h2>` elements so screen-reader users can jump between them.
2. **Two-column grid reduces scannability.** On a phone viewport, two columns halve the title width, and the proposal also truncates titles to one line. Item r5 ("Budgeting for a first flat: …", 95 characters) would show only its first few words. **Evidence:** `.title { white-space: nowrap; text-overflow: ellipsis }` in [current/library.html](current/library.html) already causes this in one column. **Recommendation:** single column, allow titles to wrap to two lines, full title in the detail view.
3. **Search is missing in both versions.** With dozens of saves, recall by keyword ("that tidal energy paper") is the fastest route. **Recommendation:** a search field above the filters, matching title and source.

## C. Action semantics

1. **Unlabelled "+" is the primary action but says nothing.** `.icon-btn` is 32×32 px with a "+" glyph and no accessible name ([current/library.html](current/library.html)). **Recommendation:** a labelled button "Add item" (icon optional), using `--color-accent`.
2. **"Mark done" without undo is risky; delete with a confirmation dialog is heavy.** Both are reversible in principle. **Recommendation:** "Mark as read" and "Remove" both act immediately and show an undo message for a few seconds. Reserve confirmation for irreversible bulk actions (none in scope).
3. **Status changes need three states, not one.** The proposal only offers "done". **Recommendation:** in the detail panel, a segmented status control: "To read", "Reading", "Done".
4. **"⋯" overflow buttons** have no accessible name and hide the only route to actions. **Recommendation:** primary row tap opens detail; actions live in the detail panel with text labels.

## D. Mechanics and gestures

1. **Swipe-only actions are invisible and inaccessible.** Swipe left/right is proposed as the sole route to mark done and delete. **Evidence:** actions table in [junior-proposal.md](junior-proposal.md#actions). **Recommendation:** swipe may be added later as an accelerator, but every action must exist as a visible button in the detail panel and be keyboard-operable. Pattern: "swipe-to-archive with undo snackbar" as used by common email clients, *with* button equivalents.
2. **Edge-swipe conflict.** Horizontal swipes on full-width rows can collide with browser/OS back gestures on some phones. Another reason not to rely on them.
3. **Touch target size.** `.icon-btn` and `.more` are small; size is not measured against a specific guideline here — verify against the target platform's published minimum. Recommendation: make the whole row the target for "open detail".

## E. Visual and motion

1. **Reuse existing tokens; no new colours needed.** `--color-accent`, `--color-success`, `--color-highlight` cover the needs. The proposal's "amber" reading colour is hard-coded as `#d39b2a` in the current CSS and has no token. **Recommendation:** add `--color-progress` to [current/tokens.css](current/tokens.css) or reuse `--color-accent` with a text label; do not introduce more ad-hoc hex values.
2. **Principle "make status pop" with colour is the wrong principle.** See F1. Status gets a text badge; colour is reinforcement only.
3. **Rhythm.** Current spacing (`--space-3` padding, `--space-2` gap) is consistent and readable. **Keep.**
4. **Motion.** Detail panel slides in using `--motion-standard`; undo message fades using `--motion-fast`. Under `prefers-reduced-motion: reduce`, switch to instant show/hide.

## F. Accessibility and internationalisation

1. **Status by colour alone.** Current status is an 8 px coloured dot (`.dot.unread/.reading/.done`) with no text; the proposal swaps it for a coloured border. Both fail the "not by colour alone" principle. **Recommendation:** text badge ("Reading", "Done") plus a progress label for books (e.g. "In progress").
2. **Contrast:** not measured in this review. `--color-text-secondary` on `--color-surface` should be checked with a contrast tool before shipping.
3. **Screen readers:** list rows are `<li>` containing non-interactive spans plus an unnamed button. **Recommendation:** each row is a single button (or link) whose accessible name includes title, status and date group; filter chips are toggle buttons with `aria-pressed`; result count announced via `aria-live="polite"`.
4. **Keyboard:** detail panel moves focus to its heading on open, traps focus while modal on narrow screens, closes with Escape and returns focus to the originating row.
5. **Text expansion:** filter chip labels should wrap or scroll horizontally rather than truncate; allow roughly 30–40% longer strings.
6. **States:**
   - Empty library: explain and offer "Add item".
   - No results for a search/filter: say which filters are active and offer "Clear filters".
   - Add with an invalid URL or empty title: inline error next to the field, focus moved to the first invalid field.
   - Long titles: wrap to two lines in the list; full in detail.
   - Loading: not applicable in the offline prototype; specify a skeleton row for the real app.

## G. Missing questions

1. How are most items added — share sheet, paste URL, or manual entry? This decides whether "Add item" is a primary on-screen action or secondary.
2. Should "Done" items appear in the main list at all, or only under a "Done" filter?
3. Is reading progress (percentage, page) tracked, or only the three statuses?
4. Do people need to tag or collect items into lists, or is search plus status enough for now?
5. What is a typical library size? Grouping by week may need "Earlier this month" if libraries grow large.

## H. Refined specification

### Layout (narrow viewport)

```text
Library                                   [Add item]
[Search title or source…                           ]
Filters: (To read) (Reading) (Done)  Type ▾        12 items
── Continue reading ───────────────────────────────
  A field guide to offline-first sync   [Reading] 22 min
  The patient gardener                  [Reading] book
── This week ──────────────────────────────────────
  Designing calm notifications          [To read]  8 min
  …
── Last week ──────────────────────────────────────
── Earlier ────────────────────────────────────────
                       ┌ Detail panel (sheet on phone, side panel ≥ 768 px)
                       │ Title (full), source, type, added date
                       │ Status: [To read | Reading | Done]
                       │ [Mark as read]  [Remove]
                       └ Close (Esc)
```

### Components and tokens

| Element | Component | Tokens | Notes |
| --- | --- | --- | --- |
| Row | Existing list row, now a button | `--color-surface`, `--color-border`, `--radius-card`, `--space-3` | Title wraps to 2 lines |
| Status badge | New text badge | `--color-accent`, `--color-success`, `--radius-chip` | Text always present |
| Section heading | `<h2>` | `--font-size-meta`, `--font-weight-strong`, `--color-text-secondary` | "This week" etc. |
| Filter chip | Toggle button | `--radius-chip`, `--color-accent` when pressed | `aria-pressed` |
| Add item | Labelled button | `--color-accent`, `--color-accent-contrast` | Opens dialog |
| Undo message | Live region | `--color-text-primary` background | 5 s, dismissible |

### Interactions

| Trigger | Result | Keyboard / screen reader | Reduced motion |
| --- | --- | --- | --- |
| Type in search | List filters live; count updates | Count in `aria-live` | n/a |
| Toggle status chip | Filters list | Enter/Space; `aria-pressed` | n/a |
| Activate row | Opens detail | Enter/Space; focus to detail heading | Instant |
| Change status in detail | Row moves section; message shown | Radio group, arrow keys | Instant |
| Mark as read / Remove | Applies; undo message | Undo button reachable by Tab | Instant |
| Add item | Dialog; validates title and URL | Focus to first field; Escape closes | Instant |

### States

| State | Content | Action available |
| --- | --- | --- |
| Empty library | "Your shelf is empty. Save something to read later." | Add item |
| No results | "No items match 'xyz' with Reading." | Clear filters |
| Invalid add | "Enter a title." / "Enter a web address starting with https://" | Fix and resubmit |
| Long content | Two-line wrap; full title in detail | Open detail |

### Cut / Add / Revise / Keep ledger

| Decision | Item | Reason | Reference |
| --- | --- | --- | --- |
| Keep | Single-screen, single-column list | Fits the job; best for long titles on phones | A3, B2; [current/library.html](current/library.html) |
| Keep | Token set and spacing rhythm | Consistent, sufficient; no new palette needed | E1, E3; [current/tokens.css](current/tokens.css) |
| Add | "Continue reading" section | Directly answers "what I'm halfway through" | A2; complaint in [context.md](context.md) |
| Add | Date-group headings | Answers "what I saved last week"; navigable by heading | B1 |
| Add | Search | Fastest recall for known items | B3 |
| Add | Undo for mark-as-read and remove | Reversible actions should not need confirmation | C2 |
| Revise | Status dot → text badge | Not by colour alone | F1; `.dot` in [current/library.html](current/library.html) |
| Revise | "+" → labelled "Add item" | Accessible name and clear intent | C1 |
| Revise | Type tabs → secondary type filter | Type is not what the complaint is about | A1 |
| Revise | `#d39b2a` → token | Avoid ad-hoc colours | E1 |
| Cut | Two-column grid | Halves title width, hurts scanning | B2 |
| Cut | Swipe as the only action route | Invisible and inaccessible | D1 |
| Cut | Delete confirmation dialog | Replaced by undo | C2 |

### Acceptance criteria

- [ ] With the fixture, "Continue reading" lists exactly the two `reading` items.
- [ ] Items added 2026-10-24 to 2026-10-30 appear under "This week" when today is 2026-10-30 (fixture `today`).
- [ ] Searching "tidal" shows one result and announces "1 item".
- [ ] Filtering to a combination with no matches shows the no-results state with a working "Clear filters".
- [ ] Every status is readable without colour.
- [ ] All actions work with keyboard only; Escape closes the detail and add dialog and returns focus.
- [ ] Submitting the add form with an empty title shows an inline error and focuses the field.
- [ ] With reduced motion enabled, panels appear without sliding.
