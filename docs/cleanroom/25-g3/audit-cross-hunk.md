# Cross-hunk consistency audit — round 25

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (whole file, in
slices), `hunk-01.diff`, `hunk-02.diff`. Did NOT read `full.diff`, `docs/`,
`conformance/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`spec/registry.json`, git history, or the web. Did not list the r25audit
directory (I globbed `hunk-*.diff` to learn how many hunk files were mine; that
returned two names and nothing else).

Unrequested context appeared in my prompt before I began: a project instruction
file pointer (CLAUDE.md → AGENTS.md), an index of the maintainer's private
memory notes with titles naming this project's cadence and prior failure
shapes, a git status block with recent commit subject lines, and a skills
listing. I did not open any of it and drew no conclusion from it. The commit
subject lines were visible in the status block; I did not use them to locate or
characterise the repairs — every claim below is sourced to spec text or hunk
text I quote.

## Step 1 — grouping

I was given two of the cycle's repairs. Grouped by the rule they touch rather
than by section:

**Group A — "where is a rule established, and what does its absence leave
open".** BOTH hunks are in this group. Hunk 1 closes with "which is why the
rule is stated here and not left to the rows" (the shrink bar lives in §20.3
prose, not in §21's register, because §21.7 says it has no witness). Hunk 2
opens with "`[R-LIF-02]`'s commit protocol does not bind a compactor … where
§20.2 binds a creator to that path by name and §20.3 step 6 binds an appender,
this section deliberately does not", and then reasons from the absence to two
consequences, one of which it also parks on §21.7's authority via the
pre-existing "Neither obligation has a witness in the output alone (§21.7)".

The shared principle the two repairs jointly adopt:

> A rule reaches only the operation or tier the text names, and a rule with no
> file-level witness must be carried by the prose of the tier it binds, with
> §21.7 as the standing account of why no register row exists.

Group A's joint test is therefore: do both repairs leave §21.7 an accurate
account, and do both use "commit" to mean the same thing? Answer below: no on
both counts (findings X-05, X-07, X-04).

There is no second group among my two hunks. Neither makes a completeness claim
about register rows (hunk 2's `§21.6`/`§10.1`/`§10.2` row inventory is in the
paragraph *below* its insertion and is untouched by it — I checked the diff
context: those lines carry no `+`).

## Step 2 — the rule each repair makes true

### Hunk 1 (§20.3 step 4, shrink paragraph)

Repaired text:

> "…the quantifier is the superseded generation's, so a shrink that alters what
> §14 fixes for a tile stored there is barred whether or not the new state still
> stores it. What counts as such an alteration is the bar above and nothing
> else, its carve-out included — a new padding position whose stored byte
> already holds the fill `[R-SER-05]` fixes is not one, so a shrink producing
> only those is permitted here exactly as it is there, and this sentence answers
> the rescue question rather than restating the test."

Superseded text:

> "…so a shrink that turns real positions into padding of a tile stored there is
> barred whether or not the new state still stores it."

Rule adopted: an extent shrink is permitted iff it alters nothing §14 fixes for
a tile stored in the superseded generation, and the step-4 bar's **carve-out**
travels with the test — so a shrink that converts real sample positions into
padding positions is **permitted** provided every such position's stored byte
already holds the channel's fill. That is a genuine widening: the old sentence
barred that class flatly.

Worked instance used throughout: layer, one uint16 channel, T = 256, E shrinks
1000 → 900. G = ⌈E/T⌉ = 4 before and after — **no tile leaves the addressed
set**, entry_count is unchanged. Tile 3 covers [768, 1024); padding was
[1000, 1024) and becomes [900, 1024). Positions [900, 1000) were real and are
now padding. If their stored bytes already hold `0xCD 0xAB` (the fill), the
repair permits the commit; the old sentence barred it.

### Hunk 2 (§20.5, compactor obligations)

Repaired text (new paragraph in full — it is all `+`):

> "`[R-LIF-02]`'s commit protocol does not bind a compactor. That protocol is
> stated for a commit, and `[R-LIF-01]` makes a compaction a whole-file rewrite
> under a new file_id rather than a commit, so neither its barrier ordering nor
> its step 5 pad reaches this tier … Two consequences follow and are intended.
> **The output's pre-trailer gap is fixed by nothing.** … **And no barrier
> ordering is owed within the output.** … A compactor SHOULD make its output
> durable before anything discards the input…"

Rule adopted: a compactor is bound by no step of `[R-LIF-02]`. Consequences it
draws: (a) the output's pre-trailer gap has no upper bound, so two conforming
compactors on one input may emit files of different length; (b) no barrier is
owed between the output's body and its trailer; (c) a SHOULD replaces the
barriers with an ordering against whatever discards the input.

## Step 3 — searches run

The document is hard-wrapped, so I normalised whitespace in Python (collapse
every run of whitespace to one space, keeping a char→line map) and searched the
flattened string. Script re-run per term; results abridged to hits I used.

`shrink` — 8 hits: L1487 (§11.1 Rationale, inside `>`), L3033/3034/3043/3048/3053
(§20.3 step 4, the repaired paragraph), L3938/3945 (§23.1, `[R-PRV-01]`).

`addressed set` — 2 hits: L1489 (§11.1 Rationale), L3037 (§20.3).

`de-address` — 2 hits: L3053 (§20.3), L3938 (§23.1).

`pre-trailer` — 10 hits: L153 (`[R-CNF-02]`), L566 (`[R-CNT-01]`), L631/L661
(`[R-CNT-02]`/`[R-CNT-03]`), L755 (`[R-CNT-05]`), L837 (`[R-CNT-09]`), L1981
(§14.5 Note), L3231 (the repair), L3446 (F5 row), L3618 (§21.6 slack row),
L4089/L4108 (Appendix A), L4334 (Appendix G item 3).

`barrier` — 9 hits: L783, L1174/L1183/L1193 (`[R-LIF-02]` and its Notes),
L2927–2929 (`[R-WRT-02]`), L3071/3074 (§20.3 step 6, `[R-WRT-04]`), L3225/L3234
(the repair), **L4432 (Appendix H, "Conforming writer" checklist)**.

`durab` — L1174/L1180/L1183, L2929, L3239 (the repair's new SHOULD), L2332.

`compactor` / `compaction` — §20.1, §20.5 throughout, `[R-CNT-08]`, `[R-CNT-21]`,
§21.7, `[R-PRV-02]`, Appendix G item 8.

Sections read in full for the "whole structure the repair landed in" check:
§2.1–§2.5, §3.1, §5.1–§5.2, §6.1–§6.4, §9.1–§9.5, §11.1–§11.4, §13.1 fill,
§14.4–§14.5, §20.1–§20.5, §21.1, §21.6, §21.7, §23.1, Appendix G items 3–10,
Appendix H. Also read `[R-CNT-17]`/`[R-CNT-23]`'s layer-record table (L1015–1050)
and register rows L21, L22, T4, T5, T26.

## Step 4 — citation ledger

Hunk 1:

| Cited | Claim made about it | Verdict |
|---|---|---|
| §14 | "alters nothing §14 fixes" | PASS. §14.5/`[R-SER-05]` fixes padding content; §14 also fixes decoded size, sample offset, codec/filter — matching step 4's own list. |
| §11.2 | "§11.2's grid count falls" | PASS. §11.2 defines Gᵢ = ⌈Eᵢ/Tᵢ⌉. |
| `[R-SER-05]` | "the fill `[R-SER-05]` fixes" at a "stored **byte**" | PARTIAL — see X-03. `[R-SER-05]` fixes three vehicles: "the recorded fill bytes for a numeric channel, the recorded fill byte for an interleaved bool channel, **the fill bit in a packed plane**." The repair names only a byte. |
| §21.7 | "records the consequence — that this is precisely where the bar has no witness, the live state being clean" | PARTIAL — see X-04. §21.7's sentence is "a commit that **supersedes** every tile it would have damaged leaves the live state clean". §3.1 and §20.3 step 4 both distinguish superseding from unstoring and from de-addressing; the repair's rescue case is the latter two. |
| `[R-CNT-21]`, `[R-CNT-17]` (trailing sentence) | consequences of a permitted shrink | FAIL as a universal — see X-02. |

Hunk 2:

| Cited | Claim made about it | Verdict |
|---|---|---|
| `[R-LIF-02]` | "That protocol is stated for a commit" | PASS. "A writer performing a **commit** MUST, in order: …". |
| `[R-LIF-01]` | "makes a compaction a whole-file rewrite under a new file_id rather than a commit" | PARTIAL — see X-07. `[R-LIF-01]`: "every conforming **mutation of a file** is either a commit (§9.2) or a whole-file rewrite under a new file_id (compaction, §20)". Its subject is mutations of an existing file. |
| §20.2 | "binds a creator to that path by name" | PASS. `[R-WRT-02]`: "A creator MUST follow `[R-LIF-02]`'s creation path… (`[R-LIF-02]` steps 4–6 — both barriers, not one)." |
| §20.3 step 6 | "binds an appender" | PASS. "6. **Commit** (`[R-LIF-02]` steps 4–6): barrier; pad; trailer…; barrier. `[R-WRT-04]`" |
| §6.2 | "requires the trailer to occupy the file's final 64 bytes and bounds the gap ahead of it only through step 5" | PASS, verbatim. `[R-CNT-05]`: "bounds their number only through step 5 of the commit protocol, which pads to the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is conforming, and no conforming commit produces one." |
| §2.3 | "one of the writer obligations §2.3 names as no file-conformance violation" | PASS on the naming. `[R-CNF-02]` names "§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad" as one of exactly two. Note the tension: §2.3 says such an obligation "binds the actor in the same way" — it presupposes an actor who *is* bound. |
| §21.7 (pre-existing sentence in the same block) | "Neither obligation has a witness in the output alone" | PASS for the two it names; the block now carries a third un-witnessed obligation — X-05. |

## Step 5 — check 7, analogies compared verb-for-verb

**Hunk 1's analogy: "permitted here exactly as it is there".**

- Repair's governing verb: "a shrink **producing only those** is **permitted**"
  — ranges over the set of new padding positions a shrink produces.
- Cited rule's governing verb (§20.3 step 4's carve-out): "a change that
  **leaves every one of those tiles' stored bytes meaning exactly what they
  meant** — … or a new padding position whose stored byte already holds the fill
  `[R-SER-05]` fixes — **is not what this bars**."

Both are quantified over *the whole change*, across every tile stored in the
superseded generation ("every one of those tiles'" ↔ "only those"). The
quantifiers match. The analogy PASSES on the quantifier.

But the carve-out it transposes has **two** members ("a filter whose mandated
stride makes it the identity (`[R-COD-10]`), or a new padding position…") and
the repair carries only one. I tested the other separately per the charter: a
pure extent shrink cannot change a filter's mandated stride (§17.3's stride is a
function of element size / sample stride Q / s = 1, none of which an extent
touches), so the identity-filter member is inert for shrinks and its omission
is not a defect. Reported as passing.

**Hunk 2's analogy: "That protocol is stated for a commit, and `[R-LIF-01]`
makes a compaction … rather than a commit."**

- Repair's governing verb: "`[R-LIF-01]` **makes** a compaction a whole-file
  rewrite under a new file_id **rather than** a commit."
- Cited rule's governing verb: "every conforming mutation of a file **is
  either** a commit (§9.2) **or** a whole-file rewrite under a new file_id
  (compaction, §20)."

"makes … rather than" vs "is either … or", over "a compaction" vs "every
conforming **mutation of a file**". These do not range over the same set, and
the repair's own next paragraph is what proves it: "A compaction **leaves its
input intact**." A compaction is therefore not a mutation of a file at all, so
`[R-LIF-01]`'s disjunction never reaches it and cannot place it on the
non-commit side. FAILS — X-07. The consequence is X-06, because the only other
thing standing between a compactor and `[R-WRT-02]` is an argument from silence.

## Step 6 — check 6, what each repair left unconstrained

**Hunk 1. Structure governed: a layer's declared geometry as a shrink changes
it, and the stored tiles that survive it.** Quantities a shrink can move:

| Quantity | Fixed by? |
|---|---|
| the set of padding positions of a surviving stored tile | the repair, via the carve-out — but only in its *byte* vehicle. **Unpinned in the packed-planar-bool bit vehicle** → X-03 |
| the content of those positions | `[R-SER-05]`, cited |
| pad bits (§14.3) at the end of a packed plane | fixed: their count is P mod 8 and P = ∏Tᵢ, which a shrink does not touch. OK |
| decoded size, sample byte offset | fixed by tile shape, which a shrink does not touch. OK |
| codec, filter | untouched by a shrink. OK |
| grid count, entry_count, extent_length | `[R-CNT-17]` — but the passage asserts they always fall → X-02 |
| the layer's index-region placement | §20.3 step 4 ¶1 ("keeps its extent slot… relocating a live index region is compaction's operation, not an appender's") — collides with the trailing sentence → X-02 |
| slab / alignment invariant | the paragraph's own tail (`[R-SLB-01]`, `[R-CNF-05]`). OK |
| reachability of the samples the shrink hides | `[R-PRV-01]` — whose enumeration does not reach this class → X-11 |

**Hunk 2. Structure governed: the compacted output file, and `[R-LIF-02]`'s six
steps as they fail to reach it.** I enumerated every step and asked what else
fixes it:

| Step | Otherwise fixed? |
|---|---|
| 1 begin at exactly F | inapplicable (new file) |
| 2 placement / coverage classes | `[R-CNT-02]`, and §20.5 restates it ("free to place structures anywhere §5.2 admits") |
| 3 complete directory + CRC | §7.1 and §20.4 |
| 4 barrier | nothing — named as consequence (b) |
| 5 pad length | nothing — named as consequence (a) |
| 5 generation | §20.5 states "and generation 1" |
| 5 committed_file_length | `[R-CNT-06]` |
| 6 barrier | nothing — folded into consequence (b) |
| front signature block | §6.1's "Writers MUST emit exactly these 16 bytes" |

"Two consequences follow" survives this test — the enumeration is right. The
gap in hunk 2 is not a missed step; it is that the pad's length is *not*
unconstrained (X-08) and that the whole argument rests on a warrant that does
not carry it (X-06/X-07).

## Step 7 — findings, with direction

X-01 §11.1 Rationale states the narrow shrink rule. Direction: the Rationale
changes; §20.3 is the normative statement and the Rationale itself says so
("§20.3 states normatively, and governs").

X-02 §20.3's own trailing consequence sentence. Direction: the sentence
changes; the widening is the repair's evident intent and §20.3 ¶1 backs it.

X-03 the "stored byte" vehicle. Direction: §20.3 changes, to track
`[R-SER-05]`'s three vehicles.

X-06/X-07 the compactor's warrant. Direction: §20.5 changes. Either it states
positively which path binds the output emission, or §20.1/§20.2 state that
`[R-WRT-02]` binds the creator tier only. As it stands the text supports both
readings and the pad length forks.

X-11 `[R-PRV-01]`'s "two ways". Direction: §23.1 changes — but only if X-02's
widening stands; if the maintainer decides the widening was overshot, X-01,
X-02 and X-11 all resolve the other way at once. **That is the decision this
audit is asking for: the widening in hunk 1 is either right and three
restatements are stale, or it is an overshoot. It cannot be both.**

X-05 §21.7's account of §20.5. Direction: §21.7 changes.

X-10 Appendix G item 4 and Appendix H's writer checklist. Direction: the
appendices change.
