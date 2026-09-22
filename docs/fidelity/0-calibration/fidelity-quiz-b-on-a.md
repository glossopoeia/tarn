# Quiz taker transcript — quiz-b-on-a

## Disclosure

**Scratch directory.** My scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/quiz-b-on-a/`)
was empty when I began (checked with `ls -la`; zero entries besides `.`
and `..`). No prior attempt's files were present.

**File read.** I read exactly one file:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`,
in full, sequentially, in six `Read` calls covering lines 1–1000,
1000–2000, 2000–3000, 3000–3700, 3700–4300, and 4300–4981 (end of
file). I confirmed its size (302,380 bytes / 4,981 lines) with `ls -la`
and `wc -l` before reading, and did not `ls` or otherwise inspect any
other path, including the output directory
(`/private/tmp/claude-501/.../fidelity-1/out/`), the scratch parent, or
any other copy of this specification that may exist in this
repository. I did not read PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, CONTRIBUTING.md, any ADR, conformance/, or spec/registry.json.
I ran no git commands and did no web search or fetch. The path given to
me matched the path stated in the brief exactly; there was no
discrepancy to report.

**Computation.** I ran one local Python calculation (via Bash,
reading no files) to check arithmetic for quizb-01, quizb-03, and
quizb-04: grid/tile-size products, the lz4 decoded-size cap
comparison, the interleaved byte-offset formula, and the
index-encoding-1 extent_length formula. No file I/O occurred in that
calculation.

**Context that arrived unrequested.** Before I began, my runtime
context included a project instruction file pointing to an AGENTS.md,
a user memory index of prior-session notes about this same TARN
project, and a git-status block naming several recent commit subjects
(ADR-0132/ADR-0133 related). None of that is part of the
specification and none of it is evidence about the specification's
content; I have not opened, searched for, or relied on any of it in
forming the answers below, and I am not repeating its contents here
beyond this acknowledgment. My answers rest solely on the one file
named above.

**Hard-wrap caution.** I treated the document as hard-wrapped
(confirmed visually: prose lines break at ~72–76 columns, and
blockquote lines carry a literal `> ` prefix per wrapped line). Because
I read the file sequentially in full rather than via line-oriented
grep for the quiz answers, the hard-wrap risk the brief warns about
(a grep for a phrase spanning a line break silently returning zero)
did not arise for my method; where I did use `grep` below it was only
to double-check exact stored constants (e.g. `0x7E000000`), which do
not wrap across lines in this document, and I additionally verified
each such search by re-deriving the same fact from the prose I had
already read in full.

---

## Working notes, per question

### quizb-01
- §14.2 gives decoded size for a planar numeric channel c as **P · Bᶜ**.
- §11.2: P = ∏ Tᵢ. Here T = (1024, 1024, 256) (dims equal their tile
  extents, so extents don't further constrain P — each dim addresses
  exactly one tile, ⌈1024/1024⌉ = ⌈256/256⌉ = 1, consistent with "the
  layer addresses exactly one tile").
- P = 1024 × 1024 × 256 = 268,435,456.
- Bᶜ = 8 (float64, §12.1).
- Decoded size = 268,435,456 × 8 = 2,147,483,648 bytes (= 0x80000000).
- §17.2 `[R-COD-07]`: codec 4 (lz4) is barred on a layer "any of whose
  addressed tiles' decoded size exceeds 0x7E000000 bytes ... in a
  planar layer each channel's plane carries its own decoded size ...
  and the largest governs." 0x7E000000 = 2,113,929,216.
  2,147,483,648 > 2,113,929,216, so this is a violation.
- Register row L44 (§21.3), outcome reject-layer (layer-scope
  violations table, "Outcome: reject-layer").
- Verified arithmetic in Python (no file I/O): P=268435456,
  decoded=2147483648=0x80000000, cap=2113929216, decoded>cap → True.

### quizb-02
- §6.1 `[R-CNT-04]`: front block [0,16) is "resident" only for "a
  local file read whole, a memory mapping, a speculative suffix window
  that reached offset 0, or any transport already holding them."
- The described reader fetched a *suffix range* [9700, 10000) only —
  a 300-byte window that does **not** reach offset 0. So [0,16) is not
  resident.
- Per `[R-CNT-04]`: "A reader that would have to issue a further range
  request to obtain those bytes MAY defer or omit the check."
- Also stated at open-algorithm step 1 (§19.1): a reader "whose open
  leaves bytes [0, 16) resident ... MUST verify the front signature
  block by byte equality before other processing ... one that would
  have to issue a further range request for them MAY defer or omit
  the check."

### quizb-03
- §7.4 / `[R-CNT-17]`: "Under index_encoding 1, extent_length MUST
  equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4."
- entry_count = 1: 1×20 + ⌈1/65536⌉×4 = 20 + 1×4 = 24.
- Given extent_length = 40 ≠ 24 → mismatch.
- Register row L22 (§21.3): "Under index_encoding 1, extent_length ≠
  entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 ..." governing rule
  `[R-CNT-17]`.

### quizb-04
- §11.4 `[R-GEO-06]`: tile coords tᵢ = xᵢ div Tᵢ, in-tile position
  uᵢ = xᵢ mod Tᵢ; in-tile ordinal = Σᵢ uᵢ · ∏_{j>i} Tⱼ (permanent,
  every linearization).
- y=130, T_y=128 → u_y = 130 mod 128 = 2 (t_y = 1).
  x=260, T_x=128 → u_x = 260 mod 128 = 4 (t_x = 2).
  Dimension order is (y, x), so in-tile ordinal u = u_y·T_x + u_x
  = 2×128 + 4 = 260 (x is last-declared, "varies fastest" — matches
  §11.4's note).
- §14.2 `[R-SER-02]`, interleaved layout: "channel c's value at
  in-tile ordinal u sits at byte u · Q + Fᶜ," where Q = Σ Bᵢ over all
  channels (sample stride) and Fᶜ = Σ Bⱼ over channels j < c.
- Channels: a = int16 (B=2, index 0), b = uint8 (B=1, index 1).
  Q = 2 + 1 = 3. F_b = B_a = 2.
- Offset = u·Q + F_b = 260×3 + 2 = 780 + 2 = 782.
- Verified in Python: 260*3+2 = 782.

### quizb-05
- §11.2: G = ⌈7/5⌉ = 2 per axis. Tile (1,1) covers coordinate range
  [5,10) on each axis (tile extent 5, starting at 1×5=5).
- Extents are 7, so within the tile, in-tile position u is "real"
  exactly when 5+u < 7, i.e. u ∈ {0,1} — 2 of 5 positions per axis.
- Real positions in the tile = 2×2 = 4; total tile positions =
  5×5 = 25. Padding positions = 25 − 4 = 21.
- §14.5 `[R-SER-05]`: "at every padding position, a writer MUST
  encode ... that channel's fill value — the recorded fill bytes for a
  numeric channel." §12.1: uint16 is little-endian (`[R-ENC-01]`).
- Fill 0xBEEF as u16, little-endian stored bytes: low byte first =
  `EF`, high byte = `BE` → stored as `EF BE` (matches the pattern of
  §14.5's own worked example, which stores fill 0xABCD as `CD AB`).

### quizb-06
- §13.3 `[R-TYP-08]`: in a planar layer, "exactly the entry's channel
  reads as fill there, and a single sample can mix decoded and fill
  channels."
- r stored, decodes 200 → r = 200 (decoded value, returned bit-exact
  per `[R-MDL-02]`/`[R-TYP-04]`).
- g unstored (sentinel) → g = its recorded fill = 20 (`[R-TYP-06]`,
  `[R-TYP-08]`).
- b stored, decodes 5 → b = 5.
- Answer, in declared order (r, g, b): (200, 20, 5). This matches the
  shape of §13.3's own worked example (planar r/g stored, b sentinel →
  "decoded r, decoded g, and b = 0").

### quizb-07
- §17.3: "the shuffle stride s is the channel's element size for a
  planar tile and the sample stride Q for an interleaved tile ...
  **for a packed boolean plane s = 1 and the filter is the
  identity.**"
- So stride s = 1; effect: identity — grouping into n = L/1 = L groups
  of 1 byte each and placing byte i of group j at i·n+j reduces (with
  s=1) to no permutation at all, i.e. the stored bytes are unchanged.

### quizb-08
- §2.3 `[R-CNF-11]`: "cannot establish" applies "where some
  requirement is one it is unable to check on a capability or resource
  ground, as ... when it declines a layer's or a tile's decode on
  resource grounds and so cannot check §14's decoded-content
  obligations (`[R-ERR-04]`, ...)." "An established violation takes
  priority: a verifier that has established any violation reports
  nonconforming ... and cannot establish is available only to a
  traversal that established no violation."
- Here the verifier establishes no violation anywhere else, and
  declines one layer's decode purely on resource grounds → verdict:
  **cannot establish**.
- §5.2 `[R-CNT-21]` / §9.7 `[R-LIF-08]`: "Where the walk does not
  complete — ... the verifier declines a layer on resource grounds
  and so never enumerates its claimants (`[R-ERR-04]`) ... — the sum
  is reported as partial." So the slack total: **partial**.

### quizb-09
- §15.3 `[R-IDX-03]` entry-validity table, row: "offset = S ∧
  length ≠ S, or offset ≠ S ∧ length = S | *structural*: reject-tile."
  Here offset = S (sentinel), length = 100 ≠ S → this row applies
  regardless of crc's value (crc isn't part of this row's test).
- Outcome class: **reject-tile**. Marked *structural* in the table
  (one of the "Six rows ... marked *structural*: they classify an
  entry whose own 20 bytes yield no usable extent").
- `[R-IDX-03]`: "Such an entry contributes no stored extent to the
  *verifier* rows ... and none to `[R-LIF-08]`'s coverage walk, so any
  bytes it nominally addressed that no other claimant claims fall to
  slack." → **falls to slack** (not "contributes a claimant").

### quizb-10
- Layer stored ≥1 tile in the superseded generation, so §20.3 step 4's
  fixed-declaration bar applies: "a planar layer's channel list MAY be
  extended at its end or shortened from its end ... Every other
  declaration is fixed ... A commit MUST NOT change one of these."
- The list of what the line "gives up" explicitly includes: "a planar
  channel inserted or removed anywhere but the end of the list ... are
  rewrites even where a particular file would survive them in place."
- Inserting 's' between 'q' and 'r' is exactly this case (not at the
  end of the list).
- Answer: **not permitted — requires a new layer or a rewrite.**

### quizb-11
- §20.5 `[R-WRT-06]`: "It MUST mint a fresh file_id for the output —
  a new draw under §9.3's randomness advice, not merely a value
  compared against the input's ... and reusing the input's would break
  the (file_id, range) cache contract of `[R-LIF-03]`, since relocation
  puts different bytes at the same ranges."
- This applies even to "compaction, which carries every structure
  forward and changes nothing but placement" (§20.5's own definition
  of compaction as one of the three named rewrites, all of which are
  rewrites bound by `[R-WRT-06]`).
- Answer: **False.**

### quizb-12
- §6.2 `[R-CNT-06]`: "A reader MUST validate, in order: the trailer
  magic; the trailer CRC; the version gate (§6.3) — only these touch
  fields whose positions are fixed across all majors (`[R-CNT-24]`) —
  and then, those gates passed, MUST validate all of the following
  before acting on the fields involved: the flag gates ...; dir_offset
  ...; dir_length ...; dir_offset + dir_length ≤ F − 64 ...."
- §19.1 step 2 (open algorithm): "Trailer. Fetch bytes [F − 64, F) and
  validate them in §6.2's fixed order — magic, trailer CRC, version
  gate, then the remaining field gates." Step 3 (Directory) comes
  after step 2 is complete.
- §6.3 `[R-CNT-07]`: "A reader MUST reject-file when version_major is
  0 (invalid) or is a major it does not implement."
- version_major = 2 here, an unimplemented major (not 0). The reader
  hits the version gate — which is validated before the
  "remaining field gates" (dir_offset/dir_length/etc.) and long before
  step 3's directory fetch — and rejects the file there.
- Since the directory region's CRC is only fetched/verified in step 3,
  and the reader never reaches step 3 (having already rejected at the
  version gate within step 2), the reader never verifies the directory
  CRC, regardless of the fact that it happens to be correct.
- Answer: **No** — stops at **the version gate (§6.3, `[R-CNT-07]`),
  during trailer validation (§19.1 step 2 / §6.2's fixed order), before
  the directory step (§19.1 step 3) is ever reached.**

### quizb-13
- §16.2 `[R-SLB-03]`: "Sentinel tiles are transparent to run
  continuity: they occupy no bytes and do not break packing. So are
  the entries §15.3 classifies reject-tile on a *structural* ground:
  they address no usable extent, and the run's stored tiles close over
  them. An entry whose only defect is that its stored bytes fail its
  crc is not transparent."
- Also register row L41 (§21.4 note under the layer-scope table, in
  §21.3's L41 row for slab continuity): "sentinels and entries §15.3
  classifies reject-tile on a structural ground are transparent, an
  entry failing only its stored bytes' crc is not."
- Ordinal 42's entry has length = 0 (non-sentinel) → per §15.3's
  table, "length = 0 (non-sentinel) | *structural*: reject-tile" — this
  is a *structural*-ground classification, hence transparent to run
  continuity.
- So ordinal 42's entry, being structurally invalid (not merely a
  crc failure on otherwise-valid bytes), does **not** by itself break
  run continuity — the run's stored tiles (40,41,43,45,46,47, with 42
  and 44 both transparent — 44 as a valid sentinel, 42 as a
  structural-ground invalid entry) simply "close over" it.
- Answer: **No.**

### quizb-14
- §20.3 `[R-WRT-03]`: "An updater's verification depth follows
  reliance ... the trailer and the full directory always ... plus
  §19.3's layer validation for every layer whose record, index, or
  extents the commit modifies, and the §19.4 index chain for every
  segment whose entries the commit reuses (`[R-IDX-04]`). Structures
  the commit neither modifies nor relies on impose no further
  obligation."
- Here the commit changes the layer's stored-tile set (superseding one
  tile), so per §20.3 step 4 / `[R-WRT-04]`, "Every layer whose
  stored-tile set or index content this commit changes has its
  tile-index region re-emitted in full ... necessarily at a new
  placement," with "every other entry byte-identical at its
  disk-ordinal position." Segment 0's entries — untouched in value —
  are nonetheless copied forward into the new tile-index region: the
  commit **reuses** them (reads and re-emits them byte-identically),
  even though it does not modify them.
- `[R-WRT-03]`'s rule keys verification depth to *reliance* — "the
  §19.4 index chain for every segment whose entries the commit
  reuses" — not to whether the segment's *values* changed. Segment 0's
  entries are reused (carried forward) as part of re-emitting the
  whole tile-index region, so the appender relies on them and owes
  `[R-IDX-04]`'s check: "To use entry k, a reader MUST verify, in
  dependency order, crc_of_crc_array over the fetched CRC array and
  the segment CRC over the fetched segment containing k."
- Answer: **Yes** — segment 0's crc_of_crc_array cross-check and its
  own segment CRC must be verified before the appender re-emits its
  entries, because those entries are being reused/copied forward, and
  `[R-WRT-03]` ties verification depth to reliance/reuse rather than
  to whether the entries' values change.

### quizb-15
- §10.2 `[R-EXT-02]` table: every space but one has an experimental
  range; "channel layout (§14.1) | u8 | 1, 2 | 3–255 | none". Text
  confirms: "One space carries no experimental range: channel layout,
  whose `u8` field is too narrow to spare one, 3 through 255 staying
  reserved to this specification."
- So the space with no experimental range at all is **channel
  layout**.
- A channel-layout value of 200 falls in 3–255, which the table marks
  **Reserved** (not experimental, since none exists for this space).
- Answer: **channel layout**; **reserved**.

---

## Answers (final)

1. **quizb-01:** Decoded tile size = **2,147,483,648 bytes** (2^31 =
   P·B = 268,435,456 × 8). Declaring codec 4 on this layer is a
   **validity error**: outcome class **reject-layer** (register row
   L44, `[R-COD-07]`), owning scope **layer** — the decoded size
   0x80000000 exceeds the lz4 cap 0x7E000000.

2. **quizb-02:** (a) **not resident** — the fetched suffix [9700,10000)
   does not reach offset 0. (b) **MAY defer or omit** the front-block
   check (`[R-CNT-04]`).

3. **quizb-03:** **No.** Correct extent_length = **24**
   (1×20 + ⌈1/65536⌉×4). Register row **L22**.

4. **quizb-04:** **782**.

5. **quizb-05:** **21** padding positions; stored bytes **EF BE**
   (little-endian encoding of fill 0xBEEF).

6. **quizb-06:** **(200, 20, 5)**.

7. **quizb-07:** Stride **s = 1**; effect: **identity — the bytes are
   unchanged**.

8. **quizb-08:** **cannot establish**; slack total reported as
   **partial**.

9. **quizb-09:** Outcome class **reject-tile**; **structural**;
   the bytes it nominally addresses **fall to slack**.

10. **quizb-10:** **Not permitted — requires a new layer or a
    rewrite.**

11. **quizb-11:** **False.**

12. **quizb-12:** **No** — stops at **the version gate, during
    trailer validation (§6.2/§6.3, `[R-CNT-07]`), before the directory
    step** (§19.1 step 3) is reached.

13. **quizb-13:** **No.**

14. **quizb-14:** **Yes.**

15. **quizb-15:** **channel layout**; a value of 200 is classified as
    **reserved**.
