# Browser regression checks: reading-list prototype

Manual checks for [examples/reading-list/prototype.html](../examples/reading-list/prototype.html). The kit has no browser test library, so these are not automated, and nothing here is evidence that they have been run. Record your own results if you rely on them.

Run at a phone viewport (about 390 × 844) and at a width of 768 px or more, unless a check says otherwise.

1. **Undo after Add.** With the fixture (12 items), add a valid item. The count reads "13 items" and the undo message appears. Choose "Undo" within five seconds: the count returns to "12 items", the new item is gone, and focus is on "Add item".
2. **Undo after Add from the error state.** Set "Demo data state" to "Load error", add a valid item, then choose "Undo": the load-error state returns.
3. **Undo is cleared by a state change.** Remove an item, then change "Demo data state" before the message times out: the undo message disappears and nothing is restored. Choose "Synthetic fixture" again: 12 items, no undo message.
4. **Malformed address.** In Add item, enter `https://a.b:bad` with a title and save: the web-address error appears on the field, focus moves to it, and no script error appears in the console. Repeat with `http://example.org` and `ftp://x`: same error. `https://example.org/page` saves, with `example.org` as the source.
5. **Detail on a phone.** Below 768 px, activate a row: the detail opens as a sheet attached to the bottom edge, full width, with no horizontal scroll. Long content scrolls inside the sheet.
6. **Detail from 768 px.** Activate a row: the detail opens as a full-height panel on the right. Escape closes it and focus returns to the row.
7. **Add dialog stays centred.** At both widths, "Add item" opens a centred dialog.
8. **Reduced motion.** With reduced motion enabled, the sheet and panel appear without sliding.
9. **Hit targets.** In developer tools, the status chips, the type filter, the demo-state select, the Add dialog fields and the "Undo" button are each at least 44 px tall.
10. **No overflow.** At 390 px, the page, the open sheet and the Add dialog have no horizontal scroll.
