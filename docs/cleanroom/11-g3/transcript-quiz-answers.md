# Cleanroom round 11 — quiz answerer transcript

**Access disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole document, lines 1–3953, via `sed -n` ranges). I ran two local Python scripts that read
no files: a CRC-32C implementation (validated against the spec's own check vectors) and
geometry/layout arithmetic. I ran `grep`/a Python parse **against that one file only** to
extract the §21 register rows. I read no ADR, no `docs/`, no `conformance/`, no
`spec/registry.json`, no git history, no web resource. No prior knowledge of any other array
or image format was used to settle any answer.

**CRC validation.** My CRC-32C reproduced `CRC-32C("123456789") = 0xE3069283`, `CRC-32C(∅) =
0x00000000` (§4.5), and independently reproduced §15.4's constant `0xEECB3BB2` for a full
2¹⁶-entry all-sentinel segment. Three independent agreements with values the document states.

**Instance-count validation.** My mechanical parse of all 121 register rows summed to 248
instances, matching §21.8's stated "121 conditions over 248 instances" exactly. That confirms
the counting rule I applied to Q14.

---

## Q01

Declarations: rank 2, dims (y,x), E=(3,3), T=(2,2), interleaved, linearization 1,
channels a:uint8 fill 0x07, b:uint16 fill 0xBEEF, codec 1, filter 2, index_encoding 1.

Geometry (§11.2): G_y=⌈3/2⌉=2, G_x=2, N=4, P=∏T=4, C=2, Q=ΣB=1+2=3.
Decoded size = P·Q = 12 (§14.2, interleaved row).

Tile (1,1) covers y∈[2,4), x∈[2,4). Only (2,2) is inside E=(3,3) — matching the question's
stipulation. Its in-tile position is (0,0), in-tile ordinal 0. The other 3 positions are
padding positions (§11.3), whose content §14.5 fixes:

> "at every padding position, a writer MUST encode, for each channel the position carries,
> that channel's fill value" `[R-SER-05]`

Value sequence (§14.1, interleaved): value k = channel (k mod C) at in-tile ordinal k div C.
Decoded tile image:
- ordinal 0: a=11, b=33 22 (0x2233 LE, §4.1)
- ordinals 1–3 (padding): a=07, b=EF BE (0xBEEF LE)

`11 33 22 07 EF BE 07 EF BE 07 EF BE` (12 bytes)

Filter 2 byte-shuffle (§17.3, `[R-COD-10]`): stride s = Q = 3 for an interleaved tile;
L=12, n=L/s=4; byte i of group j → offset i·n + j.
Groups: [11 33 22][07 EF BE][07 EF BE][07 EF BE]
- i=0 → offsets 0–3: 11 07 07 07
- i=1 → offsets 4–7: 33 EF EF EF
- i=2 → offsets 8–11: 22 BE BE BE

Filtered image = `11 07 07 07 33 EF EF EF 22 BE BE BE`.
Codec 1 (§17.2, `[R-COD-04]`): "The stored bytes are the filtered image verbatim." So (a) is
that 12-byte string, and length 12 = decoded size, satisfying `[R-COD-04]`.

Entry (§15.1, 20 bytes): offset u64 4096 = `00 10 00 00 00 00 00 00`; length u64 12 =
`0C 00 00 00 00 00 00 00`; crc u32 = CRC-32C(stored bytes) = 0x729F206D = `6D 20 9F 72`.
(F=65536; 4096+12 ≤ F−64, so §15.3's bounds rows are clear.)

**(a)** `11 07 07 07 33 EF EF EF 22 BE BE BE`
**(b)** `00 10 00 00 00 00 00 00 0C 00 00 00 00 00 00 00 6D 20 9F 72`

## Q02

rank 1, E=6, T=3 → G=2, N=2, entry_count=2 (interleaved, §11.2). P=3, C=1, Q=2,
decoded size = P·Q = 6; codec 1 → stored length 6 each (`[R-COD-04]`).

Appendix G item 3 fixes placement: "For each layer in ascending layer-name byte order: its
stored tiles in disk-ordinal order, then its tile-index region; then any record extents in
ascending record order; then the directory. … Each structure begins where the previous one
ended, save where alignment forces a gap". No alignment/slab declared, so no gap.
§9.2's creation path puts the front block at [0,16) and begins step-2 writing at offset 16.

- tile ordinal 0: [16, 22)
- tile ordinal 1: [22, 28)
- tile-index region: begins at 28. Length (§15.1, `[R-CNT-17]`) = 2×20 + ⌈2/2¹⁶⌉×4 = 44 →
  [28, 72). Entry array [28,68), segment-CRC array [68,72).

**(a) 28  (b) 68**
**(c)** entry 1: offset 22 = `16 00 00 00 00 00 00 00`, length 6 = `06 00 00 00 00 00 00 00`

## Q03

entry_count=2, both sentinel. One segment (⌈2/2¹⁶⌉=1), partial (2 entries, not 2¹⁶), so
§15.4's constant does not apply — "a partial segment's CRC MUST be computed" `[R-IDX-05]`.

Segment bytes = two copies of `FF ×16 00 ×4` (§15.2) = 40 bytes.
CRC-32C(40 bytes) = 0xDE831C12 → stored LE `12 1C 83 DE`.
crc_of_crc_array = CRC-32C over the 4-byte array (§7.4, §8.1) = 0x78C632C2 → `C2 32 C6 78`.

Note entry_count ≠ 0, so `[R-CNT-23]`'s "0 when entry_count = 0" clause does not apply.

**(a)** `12 1C 83 DE`  **(b)** `C2 32 C6 78`

## Q04

G = (⌈5/2⌉, ⌈1000/256⌉, ⌈300/100⌉) = (3, 4, 3); N = 36. Planar, C=4.

(a) entry_count = C·N = 144 (§11.2 `[R-GEO-03]`).
(b) extent_length = 144×20 + ⌈144/2¹⁶⌉×4 = 2880 + 4 = **2884** (`[R-CNT-17]`).
(c) t = (3 div 2, 700 div 256, 250 div 100) = (1,2,2);
    s = Σ tᵢ·∏_{j>i}Gⱼ = 1·(4·3) + 2·3 + 2 = 20;
    disk ordinal = c·N + s = 2·36 + 20 = **92** (`[R-GEO-06]`).
(d) 20·92 = **1840** (§15.1: "The entry for the tile with disk ordinal k is the k-th entry,
    at region byte 20·k").
(e) u = (3 mod 2, 700 mod 256, 250 mod 100) = (1, 188, 50);
    ordinal = Σ uᵢ·∏_{j>i}Tⱼ = 1·(256·100) + 188·100 + 50 = 25600+18800+50 = **44450**.

## Q05

Index region check: 3×20 + 4 = 64 = |[512,576)| ✓.

Coverage walk claimants (§9.7 `[R-LIF-08]`, §5.2 `[R-CNT-02]`):
front block [0,16)=16; entry-0 stored extent [128,228)=100; tile-index region (the layer
record's extent, entering the walk once) [512,576)=64; user-metadata extent [600,700)=100;
directory [704,960)=256; trailer [960,1024)=64. Entry 1 is the sentinel — no extent.
Entry 2 has offset 8 < 16, a *structural* reject-tile row of §15.3, and

> "An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground does not make the
> walk incomplete: the walk passes over it, and the bytes it nominally addresses fall to
> slack (§15.3)." `[R-LIF-08]`

Claimed = 16+100+64+100+256+64 = 600. Slack = 1024 − 600 = **424**.
Cross-check by gaps: [16,128)=112, [228,512)=284, [576,600)=24, [700,704)=4 → 424 ✓.

Partial vs exact: the two triggers for *partial* (`[R-CNT-21]`) are a scope-level rejection
blocking enumeration, or an election to stop at the first violation. Neither holds — the only
defect is tile-scope and expressly non-blocking, and the verifier does not elect to stop.
Walk completes → **exact**.

## Q06

(a) Layer A's whole index region is re-emitted (`[R-WRT-04]`: "Every layer whose stored-tile
set or index content this commit changes has its tile-index region re-emitted in full").
Superseding a tile changes that entry's offset/length/crc → index content changes.
100×20 + ⌈100/2¹⁶⌉×4 = 2000+4 = **2004**. Layer B untouched → keeps its slot, contributes 0.

(b) Layout from F=8192, `[R-LIF-02]` order (step 2 payloads+indexes, step 3 directory+CRC,
step 5 pad+trailer): 8192 + 5000 = 13192; + 2004 = 15196; + 300 = 15496.
15496 mod 64 = 8 → pad to 15552 = **56** bytes.

(c) trailer [15552, 15616); committed_file_length = **15616** (15616 mod 64 = 0 ✓, §6.2).

## Q07

S=4, interleaved → one block [0,4), one run [0,4) (§16.2 `[R-SLB-02]`). A_slab=4096.

**File A.** Entry 1's stored bytes fail its crc → §15.3 row "stored bytes fail the entry's
crc → reject-tile … the entry itself is well-formed; its extent stands" → register row **T1**,
reject-tile. Slab packing (`[R-SLB-03]`): such an entry "is not transparent — its offset and
length stand", so the run reads 4096→(+100)→4196→(+300)→4496; sentinel entry 3 is
transparent. Packing holds; first stored offset 4096 mod 4096 = 0. No L41/L42.

**File B.** Entry 1 offset 8 < 16 → §15.3 "offset < 16 (non-sentinel) → *structural*:
reject-tile — the front block is never payload" → row **T8**, reject-tile. That entry is then
transparent to run continuity (`[R-SLB-03]`: "So are the entries §15.3 classifies reject-tile
on a *structural* ground: they address no usable extent, and the run's stored tiles close over
them"), so the run's stored tiles are entry 0 then entry 2, and entry 2's offset must equal
4096+100 = 4196. It is 4496 → a gap → row **L41**, reject-layer. First stored tile still
4096-aligned, so no L42. Entry 1 contributes no extent to the verifier rows, so no overlap row
(L18/F33) despite its nominal extent reaching the front block.

## Q08

§6.2 fixes the order: "magic; the trailer CRC; the version gate (§6.3)" — only these touch
fields whose positions are fixed across all majors (`[R-CNT-24]`) — and only then the
remaining field gates, committed_file_length among them.

(a) version_major = 2, a major the reader does not implement → `[R-CNT-07]`: "A reader MUST
reject-file when version_major is 0 (invalid) or is a major it does not implement" →
**reject-file**.

(b) §2.3: *cannot establish* is for "some requirement … it is unable to check on a capability
or resource ground, as when the file names a format major version it does not implement". No
violation can have been established, because §2.3 also says "a file declaring another major is
neither conforming nor nonconforming under it". → **cannot establish**.

(c) §21.6: "version_major naming a major this reader does not implement … Neither is a
register row: the register enumerates file-conformance violations (§21.1), and a file this
document declines to judge is not one." The committed_file_length mismatch cannot be an F17
instance, because F17 is a major-1 file-conformance violation and `[R-CNT-24]` reserves only
the magic, version_major/minor and the terminal CRC across majors — the bytes at trailer
offset 40 are not committed_file_length in an unspecified major. → **none**.
(Competing reading noted: someone treating the trailer as a major-1 layout would name F17.
Even then the reader never reaches that gate, the version gate preceding it.)

## Q09

Members of the top-level object, in stored order: `tarn.axes`, `b`, `a`. Ascending UTF-8-byte
order is `a` (0x61), `b` (0x62), `tarn.axes` (0x74…). The stored order is not ascending →
`[R-MTA-05]` violated → row **F27** ("A top-level user-metadata document's object members are
not in ascending order of their keys' UTF-8 bytes", detector verifier, certification).

`tarn.axes` at file scope is out of its listed scope (§18.4 lists it as layer-scope), but
§21.6 records that as a defined non-violation: "A standardized key (§18.4) appears outside its
listed scope … Conforming: placement and value shape are writer guidance". No row.
Nested object `{"unit":"m"}` is a single member; numbers 1 and 2 are finite; no duplicate keys;
keys are valid names; no BOM. Nothing else fires.

(b) The verifier has established a violation → §2.3: "a verifier that has established any
violation reports *nonconforming*" → **nonconforming**.
(c) `[R-MTA-05]`: "unsorted members do not make a document unreadable: the file is
nonconforming, a verifier MUST report it, and readers process the document unchanged" → **no**.

## Q10

(a) §18.2's note: "The 16 MiB figure is a §21.9 minimum guarantee … A file whose document
decodes to more than the guarantee stays conforming" → **yes**.
(b) `[R-MTA-09]`: the reader "decodes with a bound of its own choosing, no smaller than
§21.9's user-metadata guarantee, and a document exceeding that bound is ignore-record like any
other it cannot read" → **ignore-record**.
(c) `[R-MTA-09]`: "A **verifier** that declines to decode a document on the bound above cannot
establish that document's conformance and MUST NOT certify the file … it fixes the file's
verdict as *cannot establish* only where the verifier established no violation elsewhere" →
**cannot establish**.
(d) §18.2 note: "a reader that instead declines on resource grounds under `[R-ERR-04]` does so
at the whole file, a document having no declared size and so no narrower scope whose
declarations that rule can measure" → **file**.

## Q11

Governing text is §20.4's MU = 0 / PE = 0 row: droppable "only in a commit that
*independently* changes the scope the record attaches to: for a layer sub-record, that layer's
record, the entry set of its index, or which of its tiles are stored; for a top-level record,
the file's layer set or another *non-layer* top-level record."

(a) storing a previously-sentinel tile changes **which of its tiles are stored** → **MAY drop**.
(b) "Superseding a stored tile's bytes is not such a change for either kind … so a commit
    whose only change is a supersede MUST retain the record" → **MUST retain**.
(c) amending another non-layer top-level record is expressly listed → **MAY drop**.
(d) "Dropping the record is not itself such a change either, so a commit whose only effect
    would be the drop MUST retain it" → **MUST retain**.
(e) "A compactor may drop it whenever it rewrites the file" → **MAY drop**.
(f) MU = 0 / PE = 1 row: "Retain byte-identical, extent content unmodified"; §20.5's
    compactor output is the live state "less any record §20.4 lets it drop", and §20.4 lets it
    drop only MU=0/PE=0 → **MUST retain**.

## Q12

(a) version_minor = 7: accepted, no gating — `[R-CNT-07]` "A reader MUST NOT reject a file for
its version_minor"; §21.6 "Accepted; minors never gate".
    flags bit 20: ignore-lane (bits 16–31) → ignored, `[R-CNT-08]`.
    0x8001, MU = 0: unknown experimental-range type → ignore-record, skipped as absent
    (`[R-CNT-15]`).
    0x0003, MU = 0: unknown reserved-range type → read the same way, ignore-record
    (`[R-CNT-15]`: "Readers of both apply the MU rule above unchanged").
(b) **no** — `[R-CNT-15]`: "one from the reserved range is a value this specification has not
    assigned — emitting it is a violation, and a verifier MUST treat a reserved-range record
    type as a validity error at the record's governing scope."
(c) **F36** only. F35 is the MU = 1 specialization; MU = 0 here. §21.6 confirms the other
    three conditions are non-violations.
(d) §6.2's layout table and §4.7 `[R-ENC-16]`: version_minor **descriptive** ("`version_minor`
    the only descriptive one"); flags **structural**.

## Q13

Parsed the Governing-rule column of all 121 rows of §21.2–§21.5.

- `[R-LIF-01]` → none (§21.7: "Committed-prefix immutability and the generation sequence
  (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not
  reconstruct").
- `[R-COD-02]` → **T13**.
- `[R-SLB-04]` → none (§16.2 note: "a stale declaration carries no register row of its own").
- `[R-CNT-05]` → **F7**.
- `[R-GEO-06]` → none (§21.7: "the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are
  satisfied by a structurally valid tile whatever values it carries").
- `[R-MTA-05]` → **F27, L48**.
- `[R-ENC-06]` → none (§21.7: "`[R-ENC-06]`'s fixed field widths are not a state a file can be
  in").
- `[R-CNT-22]` → **F28, L49**.

## Q14

Counting rule (§21.1): "Instances within a cell are separated by semicolons, and a cell
reading — is one instance; the count is therefore mechanical once the cell is written."

(a) R1=4, R2=2, R3=2, R4=12, R5=8, R6=4, R7=6, R8=2, R9=2, R10=2 → **44**.
    (Whole-register cross-check: my same mechanical count over all 121 rows gives 248, exactly
    §21.8's "121 conditions over 248 instances".)
(b) §21.8 `[R-ERR-02]` "one vector per instance"; `[R-VEC-03]` "every register row has at
    least one vector for each instance it names". R4 names 12 instances → **12**.
(c) T24's cell is "any codec" — §21.1: "a row whose check ranges over a family without the
    condition changing shape states that range as a single instance (T24's *any codec*)" →
    **1**.
(d) `[R-VEC-04]`: the sibling is "another layer, or another tile of the same layer **where
    that layer is one a reader is still permitted to serve**". Under reject-layer no reader may
    serve the layer → **no**.

## Q15

G = (⌈5/4⌉, ⌈5/4⌉) = (2,2), N = 4, entry_count = 4, P = 16, one uint16 channel.

Which stored tiles carry padding positions (§11.3)? Tile (0,0) covers y,x ∈ 0–3, all inside
E=(5,5) — 0 padding positions. Tiles (0,1), (1,0) each have 12; tile (1,1) has 15 (the
document's own §14.5 example uses exactly this geometry: "one real position, (4, 4), and 15
padding positions"). No packed bool plane, so no pad bits.

§20.3's shape (c): "A change confined to the directory — … or changing a channel's fill value
on a layer with no padding position and no pad bit. A fill change on a layer carrying either
additionally requires re-emitting the affected stored tiles, whose content `[R-SER-05]` fixes
— which makes it shape (b)."

(a) The affected stored tiles are the three carrying padding positions → **3**.
(b) Re-emitting those three tiles changes their entries' offsets and crcs, so the layer's
    index content changes; `[R-WRT-04]` then requires the whole region re-emitted in full at a
    new placement (`[R-LIF-01]` forbidding in-place edit) → **yes**.
(c) 4×20 + ⌈4/2¹⁶⌉×4 = 80 + 4 = **84** bytes (`[R-CNT-17]`).
