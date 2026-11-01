# Strict graft rules

The user chose a direction because of how it looks and is organised. The interactive build must keep that.

## Do

1. **Read the source first.** Open the chosen direction's HTML and work from a copy of it, not from memory.
2. **Preserve markup structure.** Keep element order, landmarks, headings and class names.
3. **Preserve CSS.** Keep existing rules and custom properties. Add new rules after them.
4. **Namespace additions.** Prefix new classes, IDs and data attributes (for example `ix-`) so they cannot collide with the source.
5. **Add behaviour with vanilla JavaScript** in one inline `<script>` at the end of `<body>`.
6. **Make every visible control work.** If a button exists, it does something meaningful or is removed with a ledger entry.
7. **Add missing states** (empty, loading, error) using the source's existing visual language.
8. **Log everything** in the change ledger.

## Do not

- Change colours, typography, spacing or layout "while you are there".
- Swap the IA for another direction's IA.
- Introduce frameworks, CDNs, web fonts or remote images.
- Use real or production data.

## When the chosen direction has a real flaw

Record it in the ledger as "Proposed change — pending approval" and ask. Keep the proposal descriptive until the user explicitly approves implementation. A toggle does not replace approval: implementing a toggled alternative also requires the user's agreement.

## Combining directions

If the user asks for "A with B's filter bar", graft the named part from B into A, namespace it, and record it. Do not average the two designs.
