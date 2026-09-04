# Cleanroom round 31 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 30's
charter: ADR-0119's fourteen repairs, the three decisions of ADR-0120, ADR-0121
and ADR-0122, and the pre-round-31 audit's sixteen repairs — seventeen
passages, 30 hunks over 5 commits. Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level flag, new, in §20.3 step 4 — and the second half of G3's
criterion is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** — twenty-fifth round running (one answer differed only in how the key annotated the same value; hand-graded) |
| Findings | **24**, from 7 reporters |
| Distinct defects | **20** by union-find, and the three passes agreed on the partition as well as the count — the second round running |
| Self-flagged byte-level | **1** |
| Upheld by any triage pass | **1** — by all three, unanimously |
| Refute phase | **fired on nothing**: no downgrade, no split, and a unanimous uphold suppresses the zero-trigger; the hand-check stood in its place |
| Surviving the hand-check as a *new* byte-level ambiguity | **1** |
| Harness | 12 agents returned of 12 that ran; every one on Opus; the two refuters configured on Sonnet never launched |
| Coverage | **opus-grade** — see *Harness integrity* |

Byte-level history: … → 2 flagged, 0 new → **1 flagged, 1 new**.

**The flag is a commit that permutes a layer's tile extents.** A directory-only
commit that swaps a rank-2 layer's two tile extents, at constant product and
with no padding position either way, moves nothing the §14 bar's list names,
changes no index entry, and transposes the array over stored bytes the writer
never stored that way. The bar's subject is *"what §14 fixes for its stored
bytes or how they decode"*; the coordinate a stored byte denotes is §11.4's,
which §14.1 cites and does not state; and §20 never mentions tile extents. One
updater re-tiles in place and emits a conforming file, another refuses and
writes a new layer or a fresh-file_id rewrite — the discriminating question's
second limb exactly, and the writer, all three passes and the hand-check agree.
The same fork reaches a reordering of the dimension entries.

It is new — no ledger entry, no ADR, and no round has asked it; Q-B6 and
ADR-0113/0114 settled the sample type and the channel order and left the
geometry that fixes a coordinate unnamed — and it is in §20.3 step 4, the
passage this round was chartered to read hardest. The sentence it turns on was
not rewritten in this surface; the step around it was, in three places, and the
criterion is stated outright: zero byte-level ambiguities, surviving the refute
phase and the hand-check. So the round that read round 30's repairs and the
three decisions did not return zero. The repair is made under ADR-0123 on the
principle the trail already records — ADR-0081 and ADR-0114: a declaration
change that reinterprets stored bytes is not an appender's operation — and the
maintainer is asked to confirm it. Round 32 reads it.

## The byte-level flag, and how it was settled

### `tile-extent-permutation` — `writer-01`, §20.3 step 4 `[R-WRT-04]`, §11.4 `[R-GEO-06]`, §14.1 `[R-SER-01]`

The construction, recomputed by hand from the document rather than taken from
the reporter or the passes: an interleaved layer, rank 2, extents (4, 4), one
uint8 channel, codec 1, filter 1, tile extents changed from (4, 1) to (1, 4).

| | T = (4, 1) | T = (1, 4) |
|---|---|---|
| grid G = ⌈Eᵢ/Tᵢ⌉ | (1, 4) | (4, 1) |
| N, P, Q | 4, 4, 1 | 4, 4, 1 |
| decoded size P·Q | 4 | 4 |
| entry_count; `[R-CNT-17]` extent_length | 4; 84 | 4; 84 |
| padding positions (4 mod 4, 4 mod 1) | none | none |
| byte offset and type of value k | k, uint8 | k, uint8 |
| disk-ordinal set | {0, 1, 2, 3} | {0, 1, 2, 3} |
| byte k of the tile at ordinal s denotes | coordinate (k, s) | coordinate (s, k) |

Every quantity the bar enumerates is unchanged, the stored-tile set and every
index byte are unchanged — so step 4's re-emission clause does not even fire
and this is a shape-(c) directory-only commit rewriting sixteen bytes of one
layer record — and twelve of the sixteen positions move. The output is an
ordinary conforming appended file: every register row is satisfied, every
checksum verifies, and §21.7 leaves the wrong content unwitnessed, since the
file is byte-indistinguishable from one whose bytes really were stored under
the new tiling.

**What was opened in the direction that would have cleared the gate.** §3.2
`[R-MDL-01]` defines the reference array from the live declarations and the
stored tiles, and so denotes the transpose as readily as the original. §11.4
`[R-GEO-06]` is where the coordinate ↔ (tile, in-tile position) map lives;
§14's opening sentence fixes its subject as *"the decoded tile image"* and
§14.1 fixes *value k* by channel and in-tile ordinal, citing §11.4 for the
positions rather than stating them. §20.1 `[R-WRT-01]` lists what an appender
does without closing the list. §20.3 step 4 whole: the re-emission clause
contemplates *"a geometry change"* only as an occasion for renumbering; the
bar's own gloss — *"a change that leaves every one of those tiles' stored bytes
meaning exactly what they meant … is not what this bars"* — states a sufficient
condition for permission and never its contrapositive; the sample-type
paragraph runs the argument that decides this case, *"the type is what fixes the
value a stored bit pattern denotes, so under a new one the same bytes denote
different values"*, for the type alone; growth and shrink are the geometry
changes the step permits and neither is this. §20.5 `[R-WRT-07]`'s
reference-array preservation binds a compactor. §21.7 is a test of detection,
not of permission. §23.1's operation list *"is not offered as closed"*.
Appendix G item 5 knows the tile extents *"fix every tile's shape"* and is
non-normative. The skeptic's route — reading *"the byte offset … of any value"*
as coordinate-indexed — is an argument, and §14.1's own vocabulary is
ordinal-indexed. Nothing decides it.

**Byte-level, new, and in chartered text.** The disputed file is conforming and
only one reading lets a conforming updater produce it. It is not a known ledger
question. §20.3 is one of the seventeen passages, step 4 was edited in three
places in this surface, and the criterion is outright.

**Repaired — ADR-0123.** The bar's subject now names the coordinate §11.4
assigns; its list names *"the coordinate (`[R-GEO-06]`) each value in the image
denotes"*; its gloss says what *meaning* is — *"the value each denotes, at the
coordinate it denotes it"*; and a paragraph on the sample-type paragraph's model
names the tile extents and the dimension order as declarations the bar reaches
wherever the layer stores any tile, with the re-type's escape. §11.1's Rationale
names the case beside re-typing. The ground is ADR-0081's and ADR-0114's, not a
new one — which is why it is a repair in this ADR and not a ledger entry — and
the maintainer's confirmation is asked for, the alternative (a directory-only
commit may transpose an array, deliberately, with every checksum certifying it)
being stated so it can be chosen instead.

**The refute phase could not have reached it, and that is the harness finding
of this round.** The phase attacks downgrades, splits and zeros — every shape in
which an agent's verdict *clears* the gate — and a unanimous uphold is the one
shape it never tests. Round 32's harness should attack a unanimous uphold too,
with the refuter told to find the sentence that decides it; this round the
driver's hand-check did that work, and found none.

## Harness integrity

- **12 agents returned of 12 that ran, every one on Opus** — the runtime's
  progress record names `claude-opus-5[1m]` for each, and every agent's
  metadata file says `opus`. No `[reasoning_extraction]` refusal occurred: the
  quiz author, refused twice by the driver in round 30, ran on Opus at the first
  attempt. The refuters were configured on Sonnet and never launched, the phase
  having nothing to attack. 84 minutes, 255 tool calls.
- **Coverage is opus-grade, by the maintainer's model policy for this round,
  and the counts are recorded beside the one measurement on record rather than
  beside the driver-grade rounds' calibration line.** That measurement: on
  identical hunks, the Sonnet fallback returned 2 findings where the driver
  returned 8. Opus has not been measured against the driver. This round
  returned 24 findings and 20 distinct defects where round 30, on the driver,
  returned 19 and 14 over a comparable surface — a count that says nothing about
  what an Opus lane missed, and is not read as a clean passage anywhere.
- **Every walk's transcript matches its structured return**, by independent
  id-scrape: reader 1, writer 3, verifier 2, diagrams 6, register 3, adversary
  5, each equal to its own `transcript_finding_count`; the quiz author's 4 make
  24.
- **All three triage passes CLEAN on mechanical coverage** — 24 of 24 ids each,
  by set difference — and the three partitions agree exactly: 20 groups each,
  union-find 20.
- **The quiz slate is Opus-grade for the first time**, and graded 15/15; its
  author re-derived §21.8's 120 / 277 count subsection by subsection
  (56 + 116 + 55 + 50) and reproduced all four stated CRC constants.
- **No pass ran a directory listing**, and no pass opened a walk transcript.

### Disclosures

Every spec-reading agent disclosed injected context — the project-instruction
pointer, an index of memory-note titles, and for four agents a git-status block
naming five recent commit subjects that describe the very changes under
review; the adversary and the quiz keyer each flagged that those subjects could
have steered them and said what they did about it — and used none of it. Two
triage passes disclosed the persisted-output form found in round 30: a `sed`
range over the spec exceeded the inline cap and the runtime saved it to a file
outside the spec; the implementer says it read part of §21 *"partly via
persisted tool output"* and then re-read the same ranges narrower, the skeptic
that it re-read its two overflowed ranges at narrower width. Both files carried
spec text and nothing else, and both passes named them. The verifier found its
own phrase search returning a false zero on a bold-marked phrase and rebuilt it
over a normalised copy before resting anything on a zero — round 29's quiz
author's shape, handled the same way. Six agents wrote and validated a CRC
script against §4.5's check vector before trusting it, which is the round-28
breach class handled as the charter asks.

## Disposition

**Zero findings are left without a disposition.**

### Repaired — ADR-0123

| Defect | Reporters | Repair |
|---|---|---|
| The §14 bar does not name the tile extents or the dimension order, and a permutation of either transposes the array over unchanged bytes — **byte-level** | writer-01 | the bar's subject and list name the coordinate §11.4 assigns; a paragraph on the sample-type model names both declarations; §11.1's Rationale names the case |
| `[R-CNF-03]`'s exclusion says *record* where §21.6 calls *top-level* load-bearing; §21.9 repeats the unqualified form | reader-01, writer-03, adversary-01, quiz-02 | *top-level record* in `[R-CNF-03]`; *an unimplemented top-level MU = 1 type* in `[R-ERR-04]` |
| The growth paragraph describes the two-limbed carve-out as one limb | writer-02, verifier-01 | *its padding limb covers* |
| Both partial-slack-total statements name two causes of an incomplete walk; a resource decline is a third | verifier-02 | the third cause added at §5.2 `[R-CNT-21]` and §9.7 `[R-LIF-08]` |
| The carve-out is stated over a stored *byte*; a packed plane's padding position is a bit | diagrams-01 | *or bit in a packed plane* at the three §20.3 sites, §11.1's Rationale and §23.1 |
| §6.2's Valid-values cell for `flags` states no value | diagrams-02 | the cell states both lanes' admissible values |
| §21.6's zero-layers cell fuses `[R-CNT-14]`'s two statements | diagrams-03 | the cell no longer requires an empty directory |
| §13.3's sparse-writing Note keys re-emission to growth alone | diagrams-04 | keyed to the stored-tile set or the index content, as `[R-WRT-04]` is |
| Shape (c) of the three-shapes Example does not name a drop-only commit | diagrams-05 | one clause names the drop; no fourth shape |
| Appendix H's writer and updater checklists carry no `flags` obligation | diagrams-06 | one clause each |
| `[R-ERR-04]` enumerates whole-file-or-narrowest; `[R-COD-06]` and `[R-CNF-11]` grant a layer-scope decline over a tile's frame | register-01 | the enumeration is a floor: *or at any scope containing that one* — the reading the two citing rules already take |
| §21.9's hard-limit restatement of the lz4 cap drops both of `[R-COD-07]`'s qualifiers | register-02 | both restored |
| §21.6's experimental-type entry reaches sub-records and cites `[R-CNT-15]` only | register-03 | `[R-CNT-18]` added |
| §11.1's Rationale omits §20.3's express growth permission | adversary-02 | one clause |
| The renumbering parenthetical and the ordinal bar's *only stated occasion* name a geometry change alone, after ADR-0122 made a channel removal an operation | adversary-03 | both name a permitted change to a planar layer's channel declarations |
| *such a tile* in ADR-0122's erratum sentence has no coherent antecedent | adversary-04 | the antecedent spelled out, as the shrink paragraph has it |
| `[R-SER-08]` says *report* where §19.4 says it fixes what a reader *returns*; *the one byte* at two sites | adversary-05 | *MUST return … the value, encoded 0x00 or 0x01 … and not the stored byte*; *the one case* |
| *relies on* carries two senses: `[R-WRT-03]`'s verification depth and step 2's shelter | quiz-01 | step 2 says *carries forward unmodified*, and that validating to `[R-WRT-03]`'s depth is not authoring |
| §20.4's table is headed *Stored flags*, one of the three flag sources its lead sentence names | quiz-03 | *Governing flags*, and the introducing clause reaches all three |
| §22.3's third residue states the re-verification trigger twice, once dangling | quiz-04 | *before any use* struck; the restatement folded in |

### Deferred

None. Two repairs ask for the maintainer's confirmation and ADR-0123's
*Confirm* line names them: the geometry paragraph of the §14 bar, and
`[R-ERR-04]`'s enumeration read as a floor. Q-C7 carries a round-31 note that
the third cause of a partial total is repaired and its own question is not.

### Declined

The skeptic's suggestion, beside `writer-02`, to widen the carve-out's filter
limb to a single-group image: *"a filter whose mandated stride makes it the
identity"* is a property, satisfied wherever the identity holds, and names no
mechanism to widen. `diagrams-05`'s fourth shape: shape (c) already covers the
drop, as all three passes found.

## What the round says about the surface it read

Of the twenty distinct defects, **four sit in sentences this surface rewrote**:
§11.1's Rationale list, ADR-0122's erratum sentence, `[R-SER-08]`'s rewritten
antecedent, and §22.3's residue paragraph. **Four more sit in text a decision
left leaning on the rule it replaced** — the twelfth shape the charter named:
the three-shapes Example under ADR-0120's licence, Appendix H under ADR-0121's
four-place bar, the renumbering occasions under ADR-0122's channel removal, and
§20.4's table heading under the very distinction ADR-0120's erratum drew. Two
are partly so, `[R-ERR-04]`'s unqualified *MU = 1 type* that the audit's own
edit passed over, and its enumeration beside ADR-0119's new §21.6 entry. The
byte-level one is in a sentence the surface did not touch, in the step it
touched most. The remaining nine are in text no recent round had touched.

Two of the sixteen pre-round-31 audit edits drew a finding on their own text —
the erratum's *such a tile* and `[R-ERR-04]`'s passed-over qualifier — where
round 30's eighteen drew none.
