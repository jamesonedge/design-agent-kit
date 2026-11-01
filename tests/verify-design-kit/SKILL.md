---
name: verify-design-kit
description: Use after editing senior-design-review or interactive-mockup, to prove both still produce good output on examples/reading-list against the recorded baseline.
---

# verify-design-kit

Proves the kit still works end to end on a fixed target. Run after any edit to either skill. Fully offline.

## Target
- `examples/reading-list/`, using its "before" screen and the complaint stated in the example.
- Don't read the example's existing review, directions or prototype before running, so the run can't copy them.

## Run
1. `python3 scripts/validate.py`, which must pass first.
2. Run `senior-design-review` on the reading-list "before" screen with the example's complaint.
3. Run `interactive-mockup` on the same screen. Ask for three directions, pick B, and build with a strict graft.
4. Save everything under `tests/runs/<date>/`.

## Check against baseline (`tests/baselines/reading-list/`)
Fail on any miss:
- Review has every section A–H, each citing something specific on the reading-list screen, not generic advice.
- Review ends with a Cut / Add / Revise / Keep ledger with at least one row in each column.
- The review catches every major issue the baseline lists in `expected-findings.md`.
- Mockup produced 2–3 directions that differ in structure, not just colour, plus a comparison page.
- Prototype is one HTML file that opens with the network off and has no external requests.
- Prototype matches direction B, and the graft ledger lists every change.
- Output is no weaker than the baseline. Compare section by section and name anything thinner.

## Report
Pass or fail, then one line per failed check with the file and what's missing. Don't edit the skills or the baseline to make a run pass.

## Refreshing the baseline
Only when the reading-list example itself changes, or the user says so. Rerun, review by hand, then copy the run into `tests/baselines/reading-list/` and update `expected-findings.md`.
