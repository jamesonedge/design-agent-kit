# Prompts

Copy, paste, and replace the `<angle-bracket>` fields. Each prompt lists the context it needs and what a good result looks like.

**Invocation.** Natural language works everywhere ("Use the senior-design-review skill…"). Where the runtime supports native names: Claude Code `/senior-design-review` and `/interactive-mockup`; Codex `$senior-design-review` and `$interactive-mockup`; Hermes natural language, or `/senior-design-review` when installed. Automatic triggering is probabilistic, so naming the skill is the most reliable option. See [compatibility.md](compatibility.md).

## Context fields used below

| Field | Meaning | If missing |
| --- | --- | --- |
| Target | File paths and/or screenshots of the screen or flow | The agent asks |
| Complaint | The user's problem, ideally verbatim | Listed as an open question |
| Tokens | Design token file(s) | Agent searches the repo; reports if none |
| Canonical component | The existing component this should resemble | Agent proposes one and asks |
| Constraints | Platform, navigation, scope limits | Agent states assumptions |
| Output path | Where to write artefacts | Agent proposes and asks |

The full optional form is in [project-design-context.md](project-design-context.md).

---

## 1. Bootstrap

Use the prompt in the [README quick start](../README.md#quick-start). Acceptance: the agent reports the pinned commit, installed paths with hashes, whether skills are loaded, that nothing has been applied yet, and asks for a target.

## 2. Review an existing screen

```text
Use senior-design-review on <target paths or screenshots>.
Complaint: "<verbatim complaint>".
Tokens: <path>. Canonical component: <path>. Constraints: <platform, scope>.
Draft the initial proposal first, then review it as a fresh pass (state whether it is independent or a single-agent separate pass).
Write proposal.md and review.md to <output path>. Do not change code.
```

Acceptance: TL;DR plus sections A–H; every finding cites a file, token, screenshot region or named pattern; states covered; ledger rows each have a reason and reference; no unmeasured contrast figures.

## 3. Critique a junior proposal

```text
Use senior-design-review to pressure-test this proposal: <path to proposal>.
Read tokens <path>, canonical component <path> and the current implementation <path> before reading the proposal.
Do not rubber-stamp. Keep what is genuinely right with a reason. Produce review.md with the Cut/Add/Revise/Keep ledger at <output path>.
```

Acceptance: at least one substantive disagreement or a justified statement that none is warranted; at least one substantiated Keep; open questions that would change the design.

## 4. Greenfield: three directions

```text
Use interactive-mockup for a new <screen/flow> on <platform>.
Task: <what the user must accomplish>. Constraints: <tokens, viewport, must-haves>.
Use synthetic data only and label it. Produce 3 static directions that differ in information architecture or interaction model, not just colour, plus comparison.html, in <output path>.
Then stop and ask me to choose.
```

Acceptance: three self-contained HTML files that open offline; a comparison page with real trade-offs; the agent states whether directions were produced independently or serially; it waits for a choice.

## 5. Picked direction: strict graft

```text
I choose direction <letter> (<optional: "with the filter bar from B">).
Use interactive-mockup in strict graft mode: read directions/<file>.html, preserve its markup and CSS, namespace additions, and add working interactions for <filters, selection, detail, add, ...>.
Include empty and error states, keyboard support, visible focus and reduced motion. Write prototype.html and change-ledger.md to <output path>.
```

Acceptance: every visible control works; the ledger lists each non-additive change with a reason; visual design matches the chosen direction.

## 6. Screenshot-led mobile whole-flow correction

```text
Use senior-design-review on this mobile flow: <screenshot 1>, <screenshot 2>, <screenshot 3> (in order).
Platform: <iOS/Android>. Complaint: "<verbatim>".
Review the flow as a whole — where users get lost between screens, not just per-screen polish. Cover gestures and their visible alternatives, back navigation, and empty/error/loading states.
Then, if I approve, use interactive-mockup to prototype the corrected flow at phone width.
```

Acceptance: section A addresses the flow structure; each screenshot is referenced by name and region; the prototype step waits for approval.

## 7. Implementation handoff

```text
Turn section H of <review.md> (and <prototype.html> if present) into an implementation handoff for <framework>.
List components to reuse with paths, tokens per element, interaction table, states, accessibility requirements and falsifiable acceptance criteria.
Mark anything the prototype does not prove (native feasibility, performance) as unverified. Do not write production code yet.
```

Acceptance: an engineer can estimate and build from it; unverified items are explicitly labelled.

## 8. Smallest fix — must not trigger a full review

```text
In <file>, increase the vertical padding of the list rows from <token A> to <token B> and change the button label "Submit" to "Save changes". Nothing else. No design review.
```

Acceptance: a minimal diff touching only those lines. If the agent starts a full review, the trigger rules are being misread — tell it to stop.
