# Cleanroom round 11 — quiz KEY transcript

**Access disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(read in full, in five `sed` chunks, plus targeted `grep`/`python3` passes over that same file).
I read no ADR, no `docs/`, no `conformance/`, no `spec/registry.json`, no `PLAN.md`, `AGENTS.md`,
`README.md`, no git history, no web. I ran local Python (a CRC-32C implementation written from
§4.5's stated parameters, plus arithmetic) and a Python script that parsed §21's register tables out
of that same spec file to count Instances cells. No other files were read or written except my own
scratch (`scratchpad/calc.py`) and this transcript.

**CRC implementation self-check** (§4.5's check vector, reproduced before any answer was computed):
CRC-32C(`"123456789"`) = 0xE3069283 ✓; CRC-32C(zero bytes) = 0x00000000 ✓.
Independent cross-check: CRC-32C of 2^16 sentinel entries = 0xEECB3BB2, matching `[R-IDX-05]` /
Appendix B. My CRC routine is therefore the one this document specifies.

---

## Q01

Layer: rank 2, dims (y,x), E=(3,3), T=(2,2), interleaved, lin 1, channels a:uint8 fill 0x07,
b:uint16 fill 0xBEEF, codec 1, filter 2, index_encoding 1. Tile coords (1,1). F = 65,536,
tile at offset 4096.

Geometry: G = (⌈3/2⌉, ⌈3/2⌉) = (2,2), N = 4, P = ∏Tᵢ = 4, C = 2, Q = ΣBᵢ = 1 + 2 = 3.
Tile (1,1) covers y∈[2,4), x∈[2,4); inside E=(3,3) only (2,2) — matching the stem. Its in-tile
position is (0,0), in-tile ordinal 0·2 + 0 = 0. In-tile ordinals 1,2,3 are padding positions
(§11.3), and `[R-SER-05]` fixes their content: "at every padding position, a writer MUST encode,
for each channel the position carries, that channel's fill value".

Value sequence (`[R-SER-01]`, interleaved): value k is channel (k mod C) at in-tile ordinal k div C.
Decoded tile image (`[R-SER-02]`, decoded size P·Q = 12):
  ord0: a=11, b=0x2233 → `33 22`
  ord1..3: a=07, b=0xBEEF → `EF BE`
  → `11 33 22 | 07 EF BE | 07 EF BE | 07 EF BE`

Filter 2, byte-shuffle (`[R-COD-10]`): stride s = Q = 3 for an interleaved tile; L = 12, n = L/s = 4;
byte i of group j goes to offset i·n + j:
  → `11 07 07 07 | 33 EF EF EF | 22 BE BE BE`

Codec 1 (`[R-COD-04]`): "The stored bytes are the filtered image verbatim." Length 12 = decoded
size, as `[R-COD-04]` requires.

**(a) stored bytes = `11 07 07 07 33 EF EF EF 22 BE BE BE`**

Entry (§15.1): offset u64 4096 = `00 10 00 00 00 00 00 00`; length u64 12 =
`0C 00 00 00 00 00 00 00`; crc u32 = CRC-32C(stored bytes) = 0x729F206D → `6D 20 9F 72`.

**(b) entry = `00 10 00 00 00 00 00 00 0C 00 00 00 00 00 00 00 6D 20 9F 72`** (20 bytes)

Confidence: high. F = 65,536 is a red herring beyond confirming 4096+12 ≤ F−64.

## Q02

Appendix G profile. rank 1, x: E=6, T=3 → G=2, N=2, entry_count = 2 (interleaved). C=1 uint16 →
P = 3, Q = 2, decoded size = P·Q = 6. Codec 1, filter 1 → each stored tile is 6 bytes.

Placement. `[R-LIF-02]` creation path: "the writer first emits the front signature block ... then
performs steps 2–6, writing beginning at offset 16". Appendix G item 3: "For each layer in
ascending layer-name byte order: its stored tiles in disk-ordinal order, then its tile-index
region; ... Each structure begins where the previous one ended, save where alignment forces a gap"
— no alignment or slab declared, so no gap.

  front [0,16); tile 0 [16,22); tile 1 [22,28); tile-index region begins at **28**.

Region length (`[R-CNT-17]`) = 2×20 + ⌈2/2¹⁶⌉×4 = 40 + 4 = 44 → region [28,72).
Segment-CRC array follows the entry array with "no padding anywhere inside the region" (§15.1),
so it begins at 28 + 40 = **68**.

Entry of disk ordinal 1: offset 22 = 0x16, length 6.

**(a) 28  (b) 68  (c) `16 00 00 00 00 00 00 00 06 00 00 00 00 00 00 00`**

Confidence: high.

## Q03

entry_count = 2, both sentinel. Sentinel = `FF ×16 00 ×4` (`[R-IDX-02]`). One segment (2 ≤ 2¹⁶),
covering 40 bytes; `[R-IDX-05]`: "a partial segment's CRC MUST be computed" — 0xEECB3BB2 is only
for a *full* 2¹⁶-entry segment, so it does not apply.

CRC-32C(40 bytes of 2×sentinel) = 0xDE831C12 → stored `12 1C 83 DE`.
crc_of_crc_array = CRC-32C over those 4 stored bytes = 0x78C632C2 → `C2 32 C6 78`.

**(a) `12 1C 83 DE`  (b) `C2 32 C6 78`**

Confidence: high (CRC routine validated on two independent published constants).

## Q04

E = (5,1000,300), T = (2,256,100), planar, C = 4.
G = (⌈5/2⌉, ⌈1000/256⌉, ⌈300/100⌉) = (3,4,3); N = 36.

(a) planar addressed-tile count = C·N = 4×36 = **144**
(b) `[R-CNT-17]`: 144×20 + ⌈144/2¹⁶⌉×4 = 2880 + 4 = **2884**
(c) (z,y,x) = (3,700,250) → t = (1, 2, 2); s = 1·(4·3) + 2·3 + 2 = 20; disk ordinal = c·N + s
    = 2·36 + 20 = **92**
(d) `[R-IDX-01]`: entry k at region byte 20·k = 20×92 = **1840**
(e) u = (3 mod 2, 700 mod 256, 250 mod 100) = (1, 188, 50);
    ordinal = 1·(256·100) + 188·100 + 50 = 25,600 + 18,800 + 50 = **44,450**

Confidence: high.

## Q05

F = 1024. Coverage walk claimants (`[R-LIF-08]`):
 front [0,16) = 16; trailer [960,1024) = 64; directory [704,960) = 256; layer record's extent =
 tile-index region [512,576) = 64 (checks out: 3×20+4 = 64); user-metadata extent [600,700) = 100;
 entry 0's stored extent [128,228) = 100; entry 1 sentinel = no extent; entry 2 offset 8 → §15.3
 "offset < 16 (non-sentinel) | *structural*: reject-tile", so it "contributes no stored extent ...
 and none to `[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed that no other
 claimant claims fall to slack."

Claimed = 16+64+256+64+100+100 = 600. Slack = 1024 − 600 = **424**
(cross-check by runs: [16,128)=112, [228,512)=284, [576,600)=24, [700,704)=4 → 424 ✓).

Partial or exact: `[R-LIF-08]` — "An entry `[R-IDX-03]` classifies reject-tile on a *structural*
ground does not make the walk incomplete: the walk passes over it". No scope-level rejection blocks
enumeration and the verifier does not stop early. → **exact**

Confidence: high.

## Q06

Appended, in `[R-LIF-02]` order, contiguously from F = 8192:
 step 2 payload 5,000 → [8192,13192); step 2 layer A index re-emitted in full (`[R-WRT-04]`:
 "Every layer whose stored-tile set or index content this commit changes has its tile-index region
 re-emitted in full — entry_count entries plus the segment CRC array") = 100×20 + ⌈100/2¹⁶⌉×4 =
 2000 + 4 = **2004** → [13192,15196); layer B untouched, so no second index (`[R-WRT-05]`).
 step 3 directory 300 → [15196,15496).
 step 5 pad to next 64-byte boundary: 15496 = 64·242 + 8 → pad = 64 − 8 = **56** → trailer at
 [15552,15616); committed_file_length = **15616** (= 64·244 ✓).

**(a) 2004  (b) 56  (c) 15616**

Confidence: high.

## Q07

Interleaved, entry_count = 4, S = 4, A_slab = 4096 → one run, ordinals [0,4) (`[R-SLB-02]`).

File A: e0 4096/100, e1 4196/300, e2 4496/200, e3 sentinel; e1's stored bytes fail its crc.
 §15.3: "An entry whose only defect is that its stored bytes fail its crc is well-formed ... its
 extent stands and it keeps its place in the *verifier* rows, in run continuity". So packing holds:
 4096+100 = 4196 ✓; 4196+300 = 4496 ✓; sentinel transparent. First stored tile 4096 mod 4096 = 0 ✓.
 → only **T1** (reject-tile).

File B: e1 offset 8, length 300; all crcs match.
 offset 8 < 16 → §15.3 structural reject-tile → **T8** (reject-tile). Being structural, e1 is
 transparent to run continuity (`[R-SLB-03]`, L41's own parenthetical), so the run's packing
 relation reads e0 → e2: e2.offset must be 4096+100 = 4196, but it is 4496 → gap → **L41**
 (reject-layer). L42 not exercised (first stored tile e0 is 4096-aligned). F33 not exercised: a
 structural entry contributes no extent to the verifier rows, and F33's own text routes a claimant
 reaching the front block to T8.

**File A: T1 — reject-tile.  File B: T8 — reject-tile; L41 — reject-layer.**

Confidence: high (medium on the completeness claim for File B — the transparency chain is the one
non-obvious step, and §15.3/§16.2/L41 all state it identically).

## Q08

version_major = 2, reader/verifier implement major 1 only; trailer magic and CRC good.

(a) §6.2's fixed order — "the trailer magic; the trailer CRC; the version gate (§6.3) — only these
touch fields whose positions are fixed across all majors (`[R-CNT-24]`)". `[R-CNT-07]`: "A reader
MUST reject-file when version_major is 0 ... or is a major it does not implement." → **reject-file**.
The committed_file_length gate is one of the "remaining field gates" reached only after the version
gate passes, and offset 40 is not a position fixed across majors, so it is never reached.

(b) §2.3: *cannot establish* is available "as when the file names a format major version it does not
implement"; and "*cannot establish* is available only to a traversal that established no violation".
`[R-CNF-02]`: "a file declaring another major is neither conforming nor nonconforming under it ...
that refusal is not a finding about its bytes." No violation is established. → **cannot establish**.

(c) §21.6: "Neither is a register row: the register enumerates file-conformance violations (§21.1),
and a file this document declines to judge is not one." The register's rows are format-major-1
violations; this file is not judged under major 1, so the 3-byte length discrepancy attributes to no
row (F17 is never reached and is not a finding about a major-2 file). → **none**.

Confidence: high on (a)/(b); high-but-flagged on (c) — the competing reading is "F17, because the
stem stipulates the field mismatches", which I reject on `[R-CNF-02]`'s "not a finding about its
bytes" plus §6.2's gate ordering plus `[R-CNT-24]`'s fixed-position carve-out.

## Q09

Document: `{"tarn.axes":[{"unit":"m"}],"b":1,"a":2}`, encoding 1, extent CRC verifies.

- `tarn.axes` is a layer-scope standardized key at file scope. §21.6: "A standardized key (§18.4)
  appears outside its listed scope ... | Conforming"; `[R-MTA-07]` obliges the reader to ignore that
  key and read the rest. Not a violation, not a row.
- Member order of the top-level object: keys' UTF-8 first bytes are `t`(0x74), `b`(0x62), `a`(0x61)
  — descending, not ascending. `[R-MTA-05]`: "Writers MUST serialize object members, at every
  nesting depth, in ascending order of their keys' UTF-8 bytes ... unsorted members do not make a
  document unreadable: the file is nonconforming, a verifier MUST report it, and readers process the
  document unchanged." → row **F27** (top-level; detector verifier).
- No duplicate keys, no non-finite numbers, no BOM, well-formed JSON object, keys valid.

(a) **F27**  (b) **nonconforming**  (c) **no**

Confidence: high.

## Q10

(a) §18.2's note: "A file whose document decodes to more than the guarantee stays conforming."
    §21.9: "A file exceeding any of these remains conforming." → **yes**
(b) §18.2 `[R-MTA-09]`: "a reader instead decodes with a bound of its own choosing, no smaller than
    §21.9's user-metadata guarantee, and a document exceeding that bound is ignore-record like any
    other it cannot read." Smallest permitted bound = 16 MiB; 20 MiB > 16 MiB. → **ignore-record**
(c) `[R-MTA-09]`: "A **verifier** that declines to decode a document on the bound above cannot
    establish that document's conformance and MUST NOT certify the file ... it fixes the file's
    verdict as *cannot establish* only where the verifier established no violation elsewhere."
    → **cannot establish**
(d) §18.2's note: "a reader that instead declines on resource grounds under `[R-ERR-04]` does so at
    the whole file, a document having no declared size and so no narrower scope whose declarations
    that rule can measure." → **file**

Confidence: high.

## Q11

§20.4's MU = 0 / PE = 0 row is decisive throughout: "An appender may drop it only in a commit that
*independently* changes the scope the record attaches to: for a layer sub-record, that layer's
record, the entry set of its index, or which of its tiles are stored; for a top-level record, the
file's layer set or another *non-layer* top-level record. Superseding a stored tile's bytes is not
such a change for either kind ... Dropping the record is not itself such a change either ... A
compactor may drop it whenever it rewrites the file."

(a) storing a previously-sentinel tile changes "which of its tiles are stored" → **MAY drop**
(b) supersede only → explicitly excluded → **MUST retain**
(c) amending another non-layer top-level record → named qualifying change → **MAY drop**
(d) the drop is the commit's only effect → explicitly excluded → **MUST retain**
(e) compactor rewriting the whole file → **MAY drop**
(f) MU = 0 / PE = 1 row: "Retain byte-identical, extent content unmodified" — no compactor
    exception in that row (the exception is written only into the PE = 0 row) → **MUST retain**

Confidence: high.

## Q12

(a) version_minor = 7: accepted and ignored — `[R-CNT-07]`, "A reader MUST NOT reject a file for its
    version_minor"; §21.6 "Accepted; minors never gate".
    flags bit 20: ignore lane (bits 16–31) → ignored, `[R-CNT-08]`.
    type 0x8001 (experimental, MU = 0): unknown type → ignore-record, skipped as though absent
    (`[R-CNT-15]`).
    type 0x0003 (reserved range, MU = 0): read the same way — ignore-record; "Readers of both apply
    the MU rule above unchanged" (`[R-CNT-15]`); its PE = 1 binds updaters, not this reader.
(b) **no** — `[R-CNT-15]`: "one from the reserved range is a value this specification has not
    assigned — emitting it is a violation, and a verifier MUST treat a reserved-range record type as
    a validity error at the record's governing scope."
(c) **F36** only. F35 requires MU = 1; here MU = 0. The experimental record, the ignore-lane bit and
    the high minor are all §21.6 non-violations.
(d) `[R-ENC-16]` / §6.2's layout table: version_minor **descriptive** ("`version_minor` the only
    descriptive one"); flags **structural**.

Confidence: high.

## Q13

Machine-checked by parsing the Governing rule column of every register row in §21.2–§21.5.

- `[R-LIF-01]` → **none**. §21.7: "Committed-prefix immutability and the generation sequence
  (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not reconstruct."
- `[R-COD-02]` → **T13**.
- `[R-SLB-04]` → **none**. §16.2's note: "Because this rule's detection *is* `[R-SLB-03]`'s, a stale
  declaration carries no register row of its own."
- `[R-CNT-05]` → **F7**.
- `[R-GEO-06]` → **none**. §21.7: "the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are
  satisfied by a structurally valid tile whatever values it carries".
- `[R-MTA-05]` → **F27, L48**.
- `[R-ENC-06]` → **none**. §21.7: "`[R-ENC-06]`'s fixed field widths are not a state a file can be
  in".
- `[R-CNT-22]` → **F28, L49**.

Confidence: high (grep confirms none of R-LIF-01 / R-SLB-04 / R-GEO-06 / R-ENC-06 appears in any
register row, in the governing-rule position or the parenthetical cross-references).

## Q14

Counting rule (§21.1): "Instances within a cell are separated by semicolons, and a cell reading —
is one instance; the count is therefore mechanical once the cell is written."

Validation of my parser: over §21.2–§21.5 it yields 121 rows and 248 instances, exactly matching
`[R-ERR-02]`'s "121 conditions over 248 instances". Per-subsection: F 36/53, L 49/106, T 26/45,
R 10/44.

(a) §21.5 = R1..R10 = 4+2+2+12+8+4+6+2+2+2 = **44**
(b) R4's cell names 12 instances; `[R-ERR-02]` "one vector per instance", `[R-VEC-03]` "every
    register row has at least one vector for each instance it names" → **12**
(c) T24's cell reads "any codec" — one instance ("a row whose check ranges over a family without the
    condition changing shape states that range as a single instance (T24's *any codec*)") → **1**
(d) `[R-VEC-04]`: the sibling is "another layer, or another tile of the same layer **where that
    layer is one a reader is still permitted to serve**". A reject-layer vector's layer is not
    servable → **no**

Confidence: high.

## Q15

E = (5,5), T = (4,4) → G = (2,2), N = 4, entry_count = 4, all stored. One uint16 channel.

Padding positions (§11.3, Gᵢ·Tᵢ = 8 > 5 on both axes):
 tile (0,0) covers y0–3, x0–3 — all inside → **no** padding;
 tile (0,1) covers x4–7 → padding; tile (1,0) covers y4–7 → padding; tile (1,1) → 15 padding
 positions (this is §14.5's own worked example, with the same extents, tile extents and 0xABCD fill).

`[R-SER-05]`: "at every padding position, a writer MUST encode ... that channel's fill value."
Changing the recorded fill therefore invalidates the stored content of exactly the tiles carrying
padding. §20.3 shape (c): "A fill change on a layer carrying either additionally requires
re-emitting the affected stored tiles, whose content `[R-SER-05]` fixes — which makes it shape (b)."
No pad bits (numeric channel, not a packed bool plane).

(a) **3**
(b) **yes** — the three re-emitted tiles land at new offsets (`[R-LIF-01]` bars reusing the old
    ones), so the index content changes, and `[R-WRT-04]` re-emits the region "in full".
(c) 4×20 + ⌈4/2¹⁶⌉×4 = 80 + 4 = **84**

Confidence: high.
