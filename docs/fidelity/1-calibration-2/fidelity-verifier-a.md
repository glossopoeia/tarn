# Verifier implementer — working transcript (edition A)

## Disclosure

**What I read.** Exactly one file, by the path the brief gave:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`.
It exists at that path (confirmed by `ls -la` before reading) and is 4,981 lines /
302,380 bytes. I read it with the Read tool in five passes (offsets 0, 1000, 2195,
2426, 2907, 3126, 3475, 3733, 4142) covering: §1–§10 in full, §11–§13 in full,
§14 partially (I read §14.4 was not fetched verbatim but §14.1–14.3 boundary and
§17's codec/filter text which cites §14's arithmetic; the decoded-size formulas
P·Q, P·Bᶜ, ⌈P/8⌉ are visible via §21's register and §17.2's text even where I did
not re-fetch §14.2's own byte-layout table line by line), §15, §16, §17 in full,
§19 in full, §20 in full, §21 in full (all subsections 21.1–21.9), and the start
of §22. I did **not** read §14 end-to-end line-by-line, §18 (user metadata) in
full, §22.2 onward, §23, §24, or the appendices — the charter's four required
pieces (certification algorithm, coverage-walk arithmetic including a non-completing
walk, every register row, a multi-generation trace) live in §2.3–2.4, §5.2, §9.7,
§15, §17.4, §19–§21, all of which I did read in full. Where a probe touches §18
material only indirectly (the "cannot establish" list in §2.3 names a user-metadata
decode decline as one of its grounds), I quote that list from §2.3 itself rather
than from §18.

**What I ran.** No commands read any file. I used `wc -l` and `grep -n "^### \|^#### "`
against the one permitted file only, to get its line count and section index (this
does not search prose content, only heading markers, so hard-wrap does not affect
it). I ran no other grep against the file's prose — all quotations above are from
direct `Read`-tool passes, not line-oriented `grep`, so the hard-wrap/blockquote
"> " caveat the brief raises does not apply to anything I quote here: I saw full
paragraphs, not grep hits. Arithmetic for probe V3 was done by hand (shown below)
and cross-checked once by re-deriving the slack figure two ways (F − live-state
total, and the sum of individually-named slack contributors) — both give 1,712.

**Context that arrived unbidden.** Before this task's own instructions, my context
contained a project `CLAUDE.md` pointer, a user memory-file index (a bulleted list
of "TARN ..." note titles), a `gitStatus` block naming the current branch and five
recent commit subjects, and environment/skill-listing boilerplate. None of that is
part of the specification and none of it is evidence about the specification. I
have not opened, searched for, or relied on any of the files those items name (no
ADRs, no PLAN.md, no other edition, no docs/decisions), and I have not repeated
their contents above beyond naming their categories, per the brief's instruction.

**Paths.** The file was exactly where the brief said. No discrepancy to report.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/walk-verifier-a/`
was empty when I created it (I made it with `mkdir -p`; a subsequent `ls -la`
showed only `.` and `..`) — no prior attempt's files were present. I did not
write any working files into it beyond this transcript's drafting having happened
in-context; nothing else was needed since all arithmetic is simple enough to show
inline below. I did not list or read the output directory beyond `mkdir -p`
(which does not list it) before writing this transcript file into it.

---

## Part 1 — The certification procedure as an ordered algorithm

A conforming verifier is defined at §2.3 (`[R-CNF-11]`) as **a reader that
additionally checks every file-level requirement — including those ordinary
readers are exempted from — and certifies conformance.** It inherits every
reader obligation (§19–§20 apply to it) and adds the checks whose *Detector*
cell in §21's register reads *verifier* (the certification-time rows: coverage
disjointness and bound-checking, F7/F33/L18; the two reserved-flag/MU-PE-mismatch
families F25/F26/F28/L46/L47/L49; the unsorted-user-metadata rows F27/L48; the
reserved-range-emission rows F36/L25; the alignment/slab-invariant rows L40/L41/L42;
and the tile-content rows T2/T4/T5/T26).

**Algorithm** (assembled from §19.1's open, §19.3's layer access, §9.7's coverage
walk, §17.4/§18.2's decode-certification rule, and §21.1's register semantics):

1. **Open** (§19.1, `[R-RDR-01]`): obtain F; fetch and validate the trailer in
   §6.2's fixed order (magic → trailer CRC → version gate → remaining field
   gates); fetch and CRC-verify the directory; parse the record sequence,
   applying the MU gate, multiplicity rules, and extent-slot rules; build the
   layer-name table, checking uniqueness on raw bytes. Any failure here is
   reject-file (the great majority of §21.2's rows are detected here, at the
   *reader* tier — a verifier owes them no differently, since they are ordinary
   reader obligations it inherits).
2. **Version-major reach test** (`[R-CNF-13]`): if version_major names a major
   the verifier does not implement, apply only the four *reaching* conditions
   (both instances of F1, F6, F8, F14 — front-block/trailer-magic equality and
   the trailer CRC) — these assert invariants `[R-CNT-24]` fixes in every major.
   If one fails, the verdict is **nonconforming** regardless of major. If all
   pass, no other condition is assessed against this file at all (they are not
   "unable to be checked" so much as simply inapplicable — format-major-1-only
   requirements do not reach a file declaring another major) — the verdict is
   **cannot establish** (§2.3 lists this scenario itself as a cannot-establish
   ground), and the verifier reports the unimplemented-major requirement as the
   one it could not check.
3. **Per layer, at "layer access"** (§19.3, `[R-RDR-03]`): full validation of
   the layer record — extent slot, the whole §7.4 constraint set, sub-record
   walk and multiplicity, name rules, value-set membership for layout,
   linearization, codec, filter, index_encoding, channel type; the u64 domain
   and 2⁶³−1 product ceiling; per-type fill constraints; the `[R-CNT-17]` index
   cross-checks. Failures here are reject-layer (§21.3's rows), all decidable
   without I/O.
4. **Per layer, index-chain verification** (§15.4, `[R-IDX-04]`): verify
   crc_of_crc_array over the fetched segment-CRC array, then each segment CRC
   over its entries, for every segment the walk touches. Failure: reject-layer.
5. **Per tile, entry classification** (§15.3, `[R-IDX-03]`): six *structural*
   rows produce reject-tile from the entry's own 20 bytes alone (sentinel
   malformed combinations, length 0, offset < 16, either field > 2⁶³−1, or the
   extent overflowing/reaching the trailer); a valid sentinel short-circuits to
   fill; otherwise fetch the payload and verify its crc (T1) — reject-tile on
   mismatch.
6. **Per tile, decode and content certification** (§17.4/§18.2's parallel rule,
   `[R-COD-11]`, `[R-SER-07]`, `[R-SER-05]`, `[R-SER-08]`, T2–T26): a verifier
   that certifies **decodes every stored tile** — §9.7 says this in as many
   words ("A verifier that certifies decodes every stored tile, whatever
   content obligations §14 places on the layer"). If the verifier cannot
   execute a layer's codec or filter, or declines a tile's/layer's decode on
   resource grounds, it **cannot establish that layer's conformance and MUST
   NOT certify the file**; the content checks it therefore never made (padding
   content T4/T5, boolean-byte content T2, filter stride T26, exact-consumption
   T24/T25, and the codec-specific framing checks T15–T23) are reported as
   unable-to-check with their ground, not skipped silently.
7. **Coverage walk** (§9.7, `[R-LIF-08]`; §5.2, `[R-CNT-02]`/`[R-CNT-21]`):
   from the live trailer, walk the live directory and, through its records and
   their sub-records, every non-sentinel index entry's stored extent (excluding
   entries §15.3 classifies reject-tile on a *structural* ground, which
   contribute no extent). Check pairwise disjointness of all claimants (each
   record's extent, each layer's tile-index region, each non-sentinel stored
   extent, the directory, the front block, the trailer), that each lies in
   [16, F−64) (front block and trailer excepted, being members of the live
   state directly), and that each verifies against §8.1's checksum map. Sum the
   unclaimed bytes as **slack** and report the total. If a scope-level
   rejection, a resource-ground layer decline, or an early stop (`[R-CNF-11]`)
   prevented full enumeration, report the total as **partial**, naming what
   stopped the walk (§5.2, `[R-CNT-21]`).
8. **Verdict** (`[R-CNF-11]`): if any violation was established anywhere above,
   report **nonconforming**, however many requirements remain unchecked. Else,
   if every requirement was checkable and was checked, report **conforming**.
   Else (no violation established, but some requirement was unable-to-check on
   a capability or resource ground), report **cannot establish**, and — in
   either of the last two cases — report every unable-to-check requirement by
   name with its ground. If the verifier elected to stop at the first violation
   it found (permitted, `[R-CNF-11]`), it additionally reports every scope it
   did not reach as **unexamined** — a report qualifier, not a fourth verdict
   and not a synonym for *cannot establish*.

**Verdict vocabulary, restated as the document states it (§2.3):**
> "A verifier reports one of three verdicts: *conforming*, *nonconforming*, or
> *cannot establish* — the last where some requirement is one it is unable to
> check on a capability or resource ground..."

and the priority rule that orders them:
> "An established violation takes priority: a verifier that has established
> any violation reports *nonconforming*, however many requirements it was
> unable to check, and *cannot establish* is available only to a traversal
> that established no violation."

---

## Part 2 — Coverage-walk arithmetic on a concrete file (multi-generation trace)

This is my worked answer to **V3**, shown in full since the charter asks for the
walk's arithmetic on a concrete file and a worked multi-generation trace, and V3
supplies exactly that shape.

### Assumptions stated up front

- **Padding.** §6.2 defines the pre-trailer pad as whatever gets the trailer to
  a 64-aligned offset; `[R-LIF-02]` step 5 says a writer "pads to the next
  64-byte boundary," and §6.2 adds "a longer gap is conforming, and no
  conforming commit produces one." I take the minimal pad (0–63 bytes, whatever
  reaches the next multiple of 64) at every commit, which is what "no
  conforming commit produces [a longer one]" licenses me to assume as the
  intended case. **This is an assumption the document does not force** — see
  Finding verifiera-01 below.
- **Commit order** follows `[R-LIF-02]` literally: (1) begin at F; (2) new
  stored-tile payloads and tile-index regions; (3) new complete directory +
  CRC; (4) barrier; (5) pad, then trailer; (6) barrier. I ignore barriers
  (conduct, not bytes, `[R-CNF-02]`).
- Each generation's directory is given as exactly 200 bytes and its trailer as
  64 bytes (stated by the probe), and I do not need `[R-CNT-17]`'s formula to
  check the given index-region sizes (84 and 164 bytes) since those are given
  as premises, not derived.
- Generation 2 adds layer B without touching layer A; generation 3 supersedes
  one 1,024-byte tile of A (same length in and out) without touching B. Per
  `[R-WRT-04]`, any change to a layer's stored-tile set forces that layer's
  **whole** tile-index region to be re-emitted at a new placement, with every
  entry but the changed one(s) carried byte-identical — so A's other tiles
  (4,096 − 1,024 = 3,072 bytes) are **not moved or rewritten** in generation 3,
  only A's 84-byte index region is (re-emitted, same size, since entry_count is
  unchanged) and the one 1,024-byte tile is superseded by a new 1,024-byte
  payload.

### Generation 1 (creation)

Per `[R-LIF-02]`'s creation path, writing begins at offset 16 (after the front
block).

| Region | Bytes | Running offset |
|---|---|---|
| front signature block | 16 | [0, 16) |
| layer A: tiles (4,096) + index (84) | 4,180 | [16, 4,196) |
| directory₁ | 200 | [4,196, 4,396) |
| pad₁ | 4,396 mod 64 = 44 → pad = 20 | [4,396, 4,416) |
| trailer₁ | 64 | [4,416, 4,480) |

F₁ = 4,480 (4,480 / 64 = 70 — a whole multiple, as required).

### Generation 2 (adds layer B)

Begins at F₁ = 4,480; A's structures are untouched and carried forward
byte-identically (`[R-WRT-05]`).

| Region | Bytes | Running offset |
|---|---|---|
| layer B: tiles (8,192) + index (164) | 8,356 | [4,480, 12,836) |
| directory₂ | 200 | [12,836, 13,036) |
| pad₂ | 13,036 mod 64 = 44 → pad = 20 | [13,036, 13,056) |
| trailer₂ | 64 | [13,056, 13,120) |

F₂ = 13,120 (13,120 / 64 = 205). directory₁ (200) + pad₁ (20) + trailer₁ (64) =
284 bytes become slack.

### Generation 3 (supersedes one 1,024-byte tile of A)

Begins at F₂ = 13,120. B is untouched. A's whole index region (84 bytes) is
re-emitted at a new placement; the superseded tile's replacement (1,024 bytes)
is appended; A's other 3,072 bytes of tiles are **not** re-written (they stay
live at their generation-1 placement, inside [16, 4,196)).

| Region | Bytes | Running offset |
|---|---|---|
| A's new tile payload | 1,024 | [13,120, 14,144) |
| A's re-emitted index region | 84 | [14,144, 14,228) |
| directory₃ | 200 | [14,228, 14,428) |
| pad₃ | 14,428 mod 64 = 28 → pad = 36 | [14,428, 14,464) |
| trailer₃ | 64 | [14,464, 14,528) |

F₃ = 14,528 (14,528 / 64 = 227).

### Live-state byte total and slack total (the coverage walk's report)

Live committed state (§5.2, `[R-CNT-02]`) = front block + every structure the
live directory reaches + the live directory + the live trailer:

| Claimant | Bytes |
|---|---|
| front signature block | 16 |
| A's live tiles (3,072 retained + 1,024 new) | 4,096 |
| A's live (generation-3) index region | 84 |
| B's tiles | 8,192 |
| B's index region | 164 |
| directory₃ | 200 |
| trailer₃ | 64 |
| **Live-state total** | **12,816** |

**Slack total** = F₃ − live-state total = 14,528 − 12,816 = **1,712**.

Cross-check by summing named slack contributors directly (§5.2's "everything
an earlier commit superseded," plus every generation's pre-trailer pad):

- A's superseded generation-1 index region (superseded in gen 3): 84
- the one superseded 1,024-byte tile of A: 1,024
- directory₁ + pad₁ + trailer₁ (superseded in gen 2): 200 + 20 + 64 = 284
- directory₂ + pad₂ + trailer₂ (superseded in gen 3): 200 + 20 + 64 = 284
- pad₃ (the *current* pre-trailer pad — §5.2 names "the pre-trailer pad" as
  slack unconditionally, not only a superseded one's): 36

Sum: 84 + 1,024 + 284 + 284 + 36 = **1,712**. Matches.

**Answer to V3:** with the stated minimal-pad assumption (pads 20, 20, 36 for
generations 1–3 respectively), a completed coverage walk over generation 3
reports a **live-state byte total of 12,816 bytes** and a **slack total of
1,712 bytes** (out of F₃ = 14,528 total file bytes).

### The same walk, where it does not complete

To cover the charter's second requirement ("again for a walk that does not
complete"): suppose, on this same generation-3 file, the verifier also finds
that two of layer B's stored-tile extents overlap (an L18 condition — "two
structures of one and the same layer claim overlapping bytes," `[R-CNT-13]`,
verifier-detected at certification). Per §5.2's text on incomplete walks:
"A rejected layer's claimants are not enumerated, whether or not the
rejection impeded reading them, and where the rejection is one the walk
itself established, L18's overlap or L40 through L42's placement among them,
the claimants it had already enumerated are discarded with the layer, since
the total is a claim about a live state one of whose layers is not usable."

So: B's 8,192 + 164 = 8,356 bytes of claimants are dropped from the walk
entirely (not counted as either "claimed" or "slack" — they are simply outside
what this run's total can speak to). The verifier reports:

- **Verdict: nonconforming** (L18 is an established violation — this takes
  priority over anything left unchecked, `[R-CNF-11]`).
- **Slack: partial**, reported as "F₃ minus the claimants actually enumerated"
  = 14,528 − (16 + 4,096 + 84 + 200 + 64) = 14,528 − 4,460 = **10,068**, named
  explicitly as an **upper bound**, not the true slack total, with the report
  stating that layer B's L18 rejection is what stopped the walk (§5.2,
  `[R-CNT-21]`: "A partial total is F less the bytes claimed by the claimants
  the walk did enumerate — an upper bound on the file's true slack, never an
  under-count").

This shows the two arithmetic regimes the charter asks for: 12,816 live /
1,712 slack (exact, complete walk) versus a reported partial upper bound of
10,068 once B is discarded whole under a verifier-established layer rejection,
with the true slack (which would additionally exclude B's still-live 8,356
bytes) left unstated because the walk never reached it.

---

## Part 3 — Every register row's detector and outcome

The register (§21.2–§21.5, `[R-CNF-07]`) is reproduced in full in the source
document; rather than re-transcribing all 120 conditions, I summarize by
detector/outcome class, since that is what a verifier implementation actually
branches on, and flag every row whose detector is *verifier* (the rows this
implementer, specifically, must add beyond an ordinary reader's checks):

**§21.2 File-scope (35 conditions, outcome reject-file).** Reader-detected at
*open*: F1–F6, F8–F10, F12–F24, F29–F32, F34, F35 (30 rows — everything
decidable from the trailer, directory CRC, and record walk alone). Reader at
*extent use*: none in this section (top-level user-metadata content failures
are §21.5's R-rows, ignore-record, not file-scope). **Verifier-detected at
*certification*: F7 (structure in the pre-trailer gap), F25 (MU=1/PE=0 on a
non-layer record), F26 (reserved flag bits 2–15), F27 (unsorted file-scope
user-metadata keys), F28 (registered-type flag mismatch), F33 (cross-scope
overlap), F36 (reserved-range top-level type emitted at all, any MU bit)** —
7 of the 35 rows are verifier-only.

**§21.3 Layer-scope (49 conditions, outcome reject-layer).** Reader at *open*:
L3, L5, L6 (name-field checks obtainable at the open's name-table build).
Reader at *layer access*: L1, L2, L4, L7–L17, L19–L36, L39, L43, L45 (36 rows
— everything §19.3 lists as decidable from the resident directory without
I/O). Reader at *tile use*: L37, L38 (the index-chain CRCs, `[R-IDX-04]` —
detection point is tile use even though the outcome is layer scope, per
§19.2's note that "index-chain failures take layer scope although their
detection point is tile use"). **Verifier-detected at *certification*: L18
(intra-layer overlap), L40 (alignment invariant), L41 (slab run-packing
invariant), L42 (slab run first-offset invariant), L46 (MU=1/PE=0 on a layer
record or sub-record), L47 (reserved flag bits), L48 (unsorted layer-scope
user-metadata keys), L25 (reserved-range sub-record type emitted), L49
(registered-type flag mismatch)** — 9 of the 49 rows are verifier-only.

**§21.4 Tile-scope (26 conditions, outcome reject-tile).** Reader at *tile
use*: T1, T3, T6–T25 (24 rows — the entry-classification structural rows,
the crc check, and every codec-framing/exact-consumption check). **Verifier-
detected at *certification*: T2 (interleaved bool byte not 0x00/0x01 at a real
position), T4 (padding content ≠ fill), T5 (packed-bool pad-bit ≠ fill), T26
(filter applied at the wrong stride, where the symptom shows up as broken
padding or bool-byte content)** — 4 of the 26 rows are verifier-only, and all
four are exactly the rows that require *decoding* to see (§9.7's "a verifier
that certifies decodes every stored tile" is precisely what makes these four
checkable at all — an ordinary reader is never obliged to decode a tile it
was not asked to read, so it never establishes T2/T4/T5/T26 as a side effect
of merely opening the file).

**§21.5 Ignored records (10 conditions, outcome ignore-record).** All ten
(R1–R10) are reader-detected, at *open* (R1's top-level instance) or *layer
access* (R1's sub-record instance) or *extent use* (R2–R10) — none is
verifier-only, because ignore-record's whole point is that an ordinary reader
already handles it without elevation to certification. All ten remain
violations (make the file nonconforming) even though no reader behavior
changes — this is the same "verifier is the only one who marks it wrong, but
every reader still processes the record on its fixed meaning" pattern as the
verifier-only rows above (§21.1's closing paragraph makes this explicit for
F27/F28/L48/L49/F26/L47 by name; R1–R10 do not need it because ignore-record
was already the reader's outcome for them).

**Totals:** 120 register conditions; 20 of them (7 + 9 + 4, all in §21.2–21.4)
are detected by the verifier alone and impose no reader obligation
(`[R-RDR-02]`) — these 20 are exactly the rows a plain conforming *reader*
implementation can omit and still be a conforming reader, but a conforming
*verifier* may not.

---

## Part 4 — The probes

See `probe_answers` in the structured result for the exact text; derivations
for V1–V6 are worked above (Part 1 for V1/V2/V4/V6, Part 2 for V3, and V5
below since it did not fit naturally elsewhere).

### V5 working

§20.3 step 4 states, as a bar on the **commit** (a writer-conduct rule, not a
file-conformance predicate): "Every other declaration is fixed for as long as
the layer stores a tile: the layout, the linearization and the index
encoding, the codec and the filter, the rank and the dimension order, every
tile extent, every channel's type and fill, an interleaved layer's channel
list (its names aside), and the position of every planar channel the new
state keeps. A commit MUST NOT change one of these... This bar binds the
commit as an actor: no file is nonconforming by virtue of its violation, and
no register row records the violation itself."

§21.7 then states directly what a verifier can see of this: "under new [fixed
declarations] the same bytes would denote values, coordinates or padding the
writer did not store, with every checksum in §8 certifying the result and,
but for a stored tile's decoded size, a padding position or pad bit, or a
boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2) and a
decode that fails outright, or a codec's framing check that precedes it,
under a changed codec or filter (T17, T24, T25), no check any actor owes able
to see it."

So the answer bifurcates on **which** fixed declaration changed and whether
the change disturbs a structurally-checked quantity:

- If the change alters the tile's **decoded size** (a tile-extent or
  channel-type change), the resulting stored length will generically fail
  T3 (exact-decoded-size, codec-independent) or, under codec 1, T14 — the
  verifier **does** see a symptom, though what it detects is "decoded size
  mismatch," not "a fixed declaration changed."
- If the change alters **codec or filter**, the stored bytes will generically
  fail to parse under the new codec's framing (T17/T23) or fail exact
  consumption (T24) or fail outright decode (T25) — again a visible symptom,
  under the changed codec's own checks.
- If the change disturbs what a **padding position or a boolean byte** must
  hold (a fill-value change, e.g.), the verifier's decode-time content checks
  (T4, T5, T2) can catch it.
- **Otherwise — a change that reshuffles what already-well-formed, already-
  checksum-passing bytes denote without breaking any of the above (e.g., a
  dimension-order change that leaves decoded size, codec framing, and
  padding/bool content all intact, or a rank change that happens to preserve
  the product) — the document is explicit that "no check any actor owes [is]
  able to see it."** The verifier reports nothing, certifies (if nothing else
  is wrong), and the file's *values* are simply wrong under `[R-MDL-02]` in a
  way this specification's mechanisms cannot surface — §21.7's stated class of
  "corruption of structure, not incorrectness of content."

**The probe as posed does not name which fixed declaration changed, so the
document does not determine a single answer** — I give both branches above,
each cited, in `probe_answers`.

---

## Part 5 — Findings

Only one finding survived scrutiny; I opened and closed several other
suspicions (see `evidence.rejected_candidates` in the structured result) —
most notably a suspicion that `[R-COD-11]`'s "verifier cannot execute a
layer's codec" ground might be vacuous for a *conforming* verifier (since
`[R-CNF-03]` already requires every conforming reader/verifier to implement
all four core codecs, and a non-core codec value is already an L43 violation
caught before decode is attempted) — this closes cleanly: `[R-COD-11]` is a
floor for *any* verifier tool encountering the situation in practice (e.g. a
missing platform codec library), independent of whether that tool otherwise
qualifies as "conforming," and it exists precisely to stop such a tool from
false-certifying. Not a document defect.

**verifiera-01** (kind OBSERVATION). The exact byte-level pre-trailer pad
length is not fixed by the specification beyond "reaches the next 64-byte
boundary": §6.2 states "a longer gap is conforming, and no conforming commit
produces one," which licenses but does not mandate the minimal pad. This
means two conformingly-equal files (identical layers, identical commit
history) can differ in their exact reported *slack total* by any additional
multiple of 64 bytes a writer chose to over-pad with, purely at the writer's
discretion, with the difference invisible to any reader and reported by a
verifier only as a (correct, but non-unique) slack number. Byte-level: yes —
this is exactly the "slack total" figure a certifying verifier reports
(§9.7, `[R-CNT-21]`), so two conforming implementations of the same input
history can legitimately emit files whose verifier-reported slack totals
differ, and neither is wrong. This is not a contradiction (the document says
so explicitly, "a longer gap is conforming") but it is a place the document
deliberately declines to pin a number I had to assume for V3's arithmetic —
I flag it because V3 asked for exact totals and the document only forces a
*minimum* pad, not an exact one. `location_a`: §6.2 (`[R-CNT-05]`'s
paragraph); no `location_b` (single-edition finding).
