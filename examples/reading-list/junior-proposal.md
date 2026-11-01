# Initial proposal: Library screen refresh

> Illustrative synthetic example — written deliberately as a plausible first draft with real weaknesses, so the review has something to pressure-test.
> Status: draft for review.

## Problem

People save items to Shelf but struggle to find them again and to see what they are in the middle of.

## Pain points (quoted)

- "I save loads, but I can never find what I saved last week, and I can't tell what I'm halfway through." — source: synthetic feedback in [context.md](context.md)

## Design principles for this change

1. Make the list feel fresh and modern.
2. Show more at once.
3. Use colour to make status pop.

## Information architecture sketch

```text
Library
├── Header: "Library", round "+" button
├── Tabs: All | Articles | Books | Videos | Papers
└── Grid of cards (2 columns on phone)
    ├── Coloured top border by status (blue unread, amber reading, green done)
    ├── Title (one line)
    └── Swipe left to delete, swipe right to mark done
```

## Actions

| Action | Type | Trigger | Undo? |
| --- | --- | --- | --- |
| Add item | Primary | "+" button opens full-screen form | n/a |
| Mark done | Secondary | Swipe right | No |
| Delete | Destructive | Swipe left, then confirm dialog | No |
| Open item | Primary | Tap card | n/a |

## States

- Empty: illustration with "Nothing here yet".
- Loading: spinner.
- Error: toast "Something went wrong".
- Long content: titles truncate to one line.

## Open questions

1. Should the grid be three columns on tablets?
