# Context: "Shelf" reading list — Library screen

> Illustrative synthetic example. "Shelf" is a fictional app; the complaint and data are invented to demonstrate the workflow. Nothing here is user research or a product metric.

| Field | Value |
| --- | --- |
| Product and task | Save articles, books, videos and papers to read later; pick the next thing to read. |
| Platform | Responsive web, used mostly on phones (narrow viewport first). |
| User complaint (verbatim, synthetic) | "I save loads, but I can never find what I saved last week, and I can't tell what I'm halfway through." |
| Boundaries | Library screen and its add/detail interactions only. No account, sync or recommendations work. |
| Design tokens | [current/tokens.css](current/tokens.css) |
| Canonical component | The list row in [current/library.html](current/library.html) (the only existing list pattern). |
| Prior approved example | None. |
| Target implementation | [current/library.html](current/library.html) (static "before" screen). |
| Platform constraints | Must work with keyboard and screen readers; touch targets follow platform guidance; works offline from a single file. |
| Data states | Empty library, no filter results, invalid add, long titles, items in progress. |
| Data | [fixture.json](fixture.json) — 12 synthetic items. |
| Output location | This folder. |
| Allowed changes | Review, directions and prototype only. |
| Approval | Product owner (role) chooses the direction. |
