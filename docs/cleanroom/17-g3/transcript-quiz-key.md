# Cleanroom round 17 — quiz key transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4317 lines, in five `Read` calls). I ran two Python scripts I wrote myself
in the scratchpad (`calc.py`, `q.py`) that read no files — a CRC-32C
implementation plus the geometry/packing/placement arithmetic. I read no ADR,
no `docs/`, no `conformance/`, no `registry.json`, no `PLAN.md`/`AGENTS.md`,
no git history, no web. I did not list the output directory.

**CRC implementation validation.** Before using it for any answer I checked my
CRC-32C against every constant the document states:

- CRC-32C(`"123456789"`) = `0xE3069283` ✓ (§4.5 check vector)
- CRC-32C(zero bytes) = `0x00000000` ✓ (§4.5)
- CRC-32C of 80 sentinel bytes = `0x80A34955` ✓ (§7.4 worked example)
- crc_of_crc_array over `55 49 A3 80` = `0xC4EE982E` ✓ (§7.4)
- CRC-32C of a full all-sentinel segment = `0xEECB3BB2` ✓ (§15.4, `[R-IDX-05]`)
- Appendix A trailer CRC over trailer bytes [0,60) = `0xE00938D2` ✓

Six independent hits, including two the document derives itself. The
implementation is this specification's checksum.

---

## Q01 — directory terminal CRC-32C at [47,51)

**Answer: `b346508a`**

Layout given: directory region [22,51) = 29 bytes. §7.1 `[R-CNT-11]`: "Its final
4 bytes are a CRC-32C over the preceding dir_length − 4 bytes; those covered
bytes are the record sequence itself". So the record sequence is [22,47) = 25
bytes, and the CRC lands at [47,51).

One record, 24-byte header + inline payload (§7.2). §18.2 `[R-MTA-03]`: "A
user-metadata record's inline payload is exactly one byte" — so inline_length = 1
and 24 + 1 = 25 exactly, no residue (`[R-CNT-12]`). Every field is forced:

| Field | Value | Fixed by | Bytes |
|---|---|---|---|
| type | 0x0002 | §7.3 (user metadata) | `02 00` |
| flags | 0x0002 | §7.3 registry: MU = 0, PE = 1; §7.2 bit 0 = MU, bit 1 = PE; reserved bits 2–15 zero | `02 00` |
| inline_length | 1 | `[R-MTA-03]` | `01 00 00 00` |
| extent_offset | 16 | layout: extent is [16,22) | `10 00 …` |
| extent_length | 6 | layout: 22 − 16 | `06 00 …` |
| payload | 1 = none | §18.2 "1 = none" | `01` |

All little-endian (`[R-ENC-01]`). Extent sanity: §8.1 puts the terminal CRC in
the extent's final 4 bytes over "the encoded bytes exactly as stored" — document
`7B 7D` (2 bytes) + 4-byte CRC = 6, and 6 ≥ 5 as §7.1 requires.

Record sequence bytes:
`02 00 02 00 01 00 00 00 10 00 00 00 00 00 00 00 06 00 00 00 00 00 00 00 01`

CRC-32C = `0x8A5046B3`; §4.5 stores it as a little-endian u32 → `B3 46 50 8A`.

Decisive quote (§7.1): "Its final 4 bytes are a CRC-32C over the preceding
dir_length − 4 bytes; those covered bytes are the record sequence itself".

Confidence: high. Determined.

---

## Q02 — layer record inline_length

**Answer: 127**

§7.4's table gives the packed field order; §7.4 `[R-CNT-18]`: "fields are packed
in table order with no alignment or padding between them".

- name `ocean`: u8 len + 5 = **6**
- layout u8 1, linearization u16 2, codec u16 2, filter u16 2, A u64 8, S u64 8,
  A_slab u64 8, rank u8 1, C u16 2 = **34**
  (cross-check: §7.4's example says "the nine scalars from layout through
  channel count occupy 4 + 34 bytes" with a 4-byte name — same 34.)
- 3 dimension entries, each `name(1+1) · extent u64 · tile extent u64` = 18 →
  **54** (example: "the dimension entry 18" ✓)
- channel `u` float64: name(1+1) + type u16(2) + fill(1 + 8) = **13**
  channel `v` int16: name(1+1) + type u16(2) + fill(1 + 2) = **7**
  (fill length equals the type's element size, `[R-CNT-23]`; §12.1 gives
  float64 = 8, int16 = 2. Example: `temp` float32 with a 4-byte name = 12 ✓)
- index_encoding u8 1 + entry_count u64 8 + crc_of_crc_array u32 4 = **13**

6 + 34 + 54 + 13 + 7 + 13 = **127**. No sub-records, so the payload ends there
and inline_length = 127.

The slab/alignment values (A = 0, S = 16, A_slab = 4096) are legal and do not
change widths — the fields are u64 regardless. Geometry (N = 10·2·2 = 40,
planar C = 2 → entry_count = 80) likewise does not affect inline_length.

Confidence: high. Determined.

---

## Q03 — decoded tile image

**Answer: `faff`**

Planar bool channel → §14.3 `[R-SER-03]`: "the decoded tile image is the tile's
P values bit-packed LSB-first: value k occupies bit k mod 8 of byte k div 8 …
and the decoded size is ⌈P/8⌉ bytes."

P = ∏Tᵢ = 4 · 4 = 16 (§11.2), decoded size = 2 bytes, P mod 8 = 0 so **no pad
bits** (§14.3).

Tile (1,1) covers y ∈ [4,8), x ∈ [4,8). Extents are E_y = 5, E_x = 7, so the
real positions are (4,4), (4,5), (4,6) — as the question states. In-tile
position uᵢ = xᵢ mod Tᵢ (§11.4); in-tile ordinal = u_y·T_x + u_x (row-major,
"for every linearization value, permanently").

| ordinal | (u_y,u_x) | (y,x) | status | bit |
|---|---|---|---|---|
| 0 | (0,0) | (4,4) | real, false | 0 |
| 1 | (0,1) | (4,5) | real, true | 1 |
| 2 | (0,2) | (4,6) | real, false | 0 |
| 3 | (0,3) | (4,7) | padding (x ≥ 7) | fill = 1 |
| 4–15 | u_y ≥ 1 | y ≥ 5 | padding (y ≥ 5) | fill = 1 |

§14.5 `[R-SER-05]`: "at every padding position, a writer MUST encode … that
channel's fill value — … the fill bit in a packed plane". Recorded fill is
`0x01` = true (§13.2), so every padding bit is 1.

Byte 0 = bits 0–7 = 0,1,0,1,1,1,1,1 = 0b11111010 = **0xFA**.
Byte 1 = bits 0–7 = values 8–15, all padding = **0xFF**.

Confidence: high. Determined.

---

## Q04 — compactor's regenerated entry

**Answer: `840; b80b000000000000000000000000000078563412`**

*(a) Offset.* G_y = ⌈100/32⌉ = 4, G_x = ⌈200/64⌉ = 4, N = 16 (§11.2). Sample
(70,130) → tile coords (70 div 32, 130 div 64) = (2,2); spatial ordinal
s = Σ tᵢ·∏_{j>i} Gⱼ = 2·4 + 2 = 10 (§11.4). Planar disk ordinal = c·N + s =
2·16 + 10 = **42**. §15.1 `[R-IDX-01]`: "The entry for the tile with disk ordinal
k is the k-th entry, at region byte 20·k" → 20 · 42 = **840**. Compaction
preserves geometry, so the ordinal and its position are unchanged.

*(b) The 20 bytes.* length = 0 with a non-sentinel offset is §15.3's row
"length = 0 (non-sentinel) | *structural*: reject-tile" (register row T10).
§20.5 `[R-WRT-07]` states the compactor's handling verbatim: "an entry §15.3
classifies reject-tile on a structural ground is reproduced with its offset and
length exactly as they stand, there being no live extent for a re-pointing to
target … and the violation travels with it into the output". Entry crcs are
likewise "unchanged".

The same passage forecloses the competing reading that the compactor must
refuse: "`[R-WRT-09]`'s checks reach the index chain and each stored tile's
entry crc, not an entry's own value domain, so such an entry is not one
`[R-WRT-06]` obliges a compactor to refuse".

offset u64 3000 = 0x0BB8 → `b8 0b 00 00 00 00 00 00`
length u64 0 → `00` ×8
crc u32 0x12345678 → `78 56 34 12`

Confidence: high. Determined — the document addresses this exact case expressly.

---

## Q05 — verdict and outcome class

**Answer: `nonconforming; ignore-record`**

*(a)* Encoding byte 0x05 is in the **reserved** range. §21.5 row R1: "A
user-metadata record declares a document encoding of 0, or a reserved-range
value (3-0x7F)" — and §21.5's preamble: "Every row here is a violation all the
same: the outcome bounds a reader's blast radius and never makes the file
conforming". So a violation is *established*.

§2.3: "An established violation takes priority: a verifier that has established
any violation reports *nonconforming*, however many requirements it was unable
to check, and *cannot establish* is available only to a traversal that
established no violation."

The 0x85 top-level record is the *experimental* range and is expressly **not** a
cannot-establish ground — §2.3: "A user-metadata document under an encoding this
specification does not assign is not such a ground: no content rule attaches
there, so nothing is left unchecked, and certification is unaffected
(`[R-MTA-10]`, §21.6)." It is reported, not counted against the verdict. Nor is
declining to decode 0x05 a decline ground: `[R-MTA-09]` — "The decline
presupposes an encoding this specification assigns".

So the verdict is **nonconforming**, driven solely by the 0x05 sub-record.

*(b)* §7.1 `[R-CNT-25]`: "An encoding value of 0, or one the reader does not
implement, makes that record unreadable, with the same outcome as a failed CRC —
ignore-record". §10.3 `[R-EXT-03]` confirms: "for the metadata-encoding space of
§18.2, ignore-record under the quarantine (`[R-CNT-25]`), never a scope-level
rejection." The verifier implements only *assigned* encodings, and 0x05 is
unassigned. → **ignore-record**, notwithstanding that the record sits at layer
scope (§18.1 `[R-MTA-02]`: "the outcome of every failure to read its **document**
is ignore-record whatever the scope").

Confidence: high. Determined.

---

## Q06 — verdict on a resource decline

**Answer: `cannot establish`**

Window 32 MiB ≤ decoded size 64 MiB, so `[R-COD-06]`'s "MUST NOT declare a window
size exceeding the tile's decoded size" is satisfied — the file really is clean,
as stipulated. 32 MiB exceeds §21.9's 8 MiB `Window_Size` minimum guarantee, and
`[R-COD-06]` expressly licenses the decline: "a wider window is conforming and
merely permits a conforming reader to decline the tile or the layer on resource
grounds (`[R-ERR-04]`)."

The layer "has edge-padding positions", so §14.5 `[R-SER-05]`'s padding-content
obligation genuinely attaches, and §9.7 `[R-LIF-08]` obliges the verifier to
decode: "A verifier decodes every stored tile, whatever content obligations §14
places on the layer … a verifier MUST NOT certify past a violation it has not
looked for."

§2.3 names this exact ground: a verdict of *cannot establish* is for "where some
requirement is one it is unable to check on a capability or resource ground …
when it declines a layer's or a tile's decode on resource grounds and so cannot
check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`,
`[R-SER-08]`)".

And §17.4 `[R-COD-11]`: "it fixes the file's verdict as *cannot establish* only
where the verifier established no violation elsewhere" — which is the stipulated
case. Not *conforming*: "a verifier MUST NOT certify a file it reports that way".
Not *nonconforming*: "*Cannot establish* is not a finding that the file is
nonconforming."

Confidence: high. Determined.

---

## Q07 — retain or may-drop

**Answer: `retain, may-drop`**

Both records are experimental-range types (≥ 0x8000) the appender does not
implement, MU = 0 / PE = 0. §20.4: "For a type the updater does not implement,
the stored flags are authoritative", and the MU = 0, PE = 0 row governs:

> "Retain byte-identical, or drop it — its extent becoming slack. An appender may
> drop it only in a commit that *independently* changes the scope the record
> attaches to: for a layer sub-record, that layer's record, the entry set of its
> index, or which of its tiles are stored; for a top-level record, the file's
> layer set — which a commit changes by adding or removing a layer and equally by
> modifying any layer's record — or another *non-layer* top-level record."

**Layer `a`'s sub-record → retain.** The three qualifying changes are all about
layer `a`: its record, its index entry set, its stored-tile set. The question
stipulates "Nothing about layer `a` or layer `b` — record content, index entry
set, or stored-tile set — changes." Adding layer `c` does not touch layer `a`'s
scope. No independent change → the drop is unavailable → retain byte-identically.

**Top-level record → may-drop.** Its trigger is "the file's layer set — which a
commit changes by adding or removing a layer". This commit adds layer `c`. The
independent change exists, so the appender may drop it (or retain it — "may
drop" is a permission, and the question asks whether the spec obliges retention;
it does not).

Confidence: high. Determined — the table anticipates precisely this asymmetry.

---

## Q08 — permitted or barred

**Answer: `barred`**

§20.3 step 4 `[R-WRT-04]`:

> "A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions …
> the decoded size, the byte offset of any sample within the decoded tile image,
> or the codec and filter that produced the stored bytes. The tense is the prior
> generation's (§3.1 defines *stored* against a generation), so a commit does not
> escape this by unstoring in the same breath: superseding every tile of a layer
> and re-declaring it are one operation, and this bars it."

The superseded generation is 7, in which all four tiles are stored. uint8 →
uint16 changes the interleaved decoded size (§14.2: P·Q, with P = 16, Q = 1 → 16
bytes, becoming Q = 2 → 32 bytes) and every sample's byte offset. That reaches
tiles stored in generation 7.

The escape hatch is closed in the same tense: "A layer that stores no tile **in
the generation this commit supersedes** MAY be re-declared freely … the tense is
the bar's, so a commit does not earn this permission by emptying the layer as it
re-declares it."

The question's stipulation that the generation-8 bytes are internally consistent
is beside the point — §21.7 notes this is exactly the case where the bar has no
live-state witness ("a commit that supersedes every tile it would have damaged
leaves the live state clean, so the bar is unwitnessed there"). Unwitnessed is
not permitted: the question asks whether the specification *permits* the commit,
and `[R-WRT-04]` says MUST NOT.

Confidence: high. Determined.

---

## Q09 — front block obligation

**Answer: `MUST verify`**

The suffix window (final 65,536 bytes of a 40,960-byte resource) necessarily
reaches offset 0, and the reader deliberately accepted the full body and holds
all 40,960 bytes — so bytes [0,16) are **resident**.

§6.1 `[R-CNT-04]`:

> "A reader whose open leaves bytes [0, 16) **resident** — a local file read
> whole, a memory mapping, a speculative suffix window that reached offset 0, or
> any transport already holding them — MUST verify the full block by byte
> equality before other processing … A reader that would have to issue a further
> range request to obtain those bytes MAY defer or omit the check … The test is
> residency, not transport."

This reader would not have to issue any further request, so the MAY does not
reach it. §19.1 step 1 restates it: "A reader whose open leaves bytes [0, 16)
resident — a speculative suffix window that reached offset 0 included — MUST
verify the front signature block by byte equality before other processing".

The 200-response handling is separately sanctioned by `[R-CNT-10]` ("abort or
accept the full body deliberately"), and Appendix A's closing paragraph confirms
the reading: a remote reader verifies "whenever its speculative suffix window
reaches offset 0". The content length 40,960 is transport-authoritative
(`[R-CNT-10]`: "a full-response content length").

Confidence: high. Determined.

---

## Q10 — extent_length

**Answer: 484**

Grid counts (§11.2, ceiling division): G_t = ⌈1000/256⌉ = 4, G_u = ⌈1/4⌉ = 1
(§11.1: "where 0 < Eᵢ < Tᵢ the grid is then a single padded tile along that
axis"), G_w = ⌈3/2⌉ = 2. N = ∏Gᵢ = 8.

Planar → addressed-tile count = C · N = 3 · 8 = 24 (§11.2 `[R-GEO-03]`), and
`[R-CNT-17]` ties entry_count to it.

§7.4 `[R-CNT-17]`: "Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4".

24 × 20 + ⌈24/65536⌉ × 4 = 480 + 1 × 4 = **484**.

(Cross-check against §15.1's region layout: 24 entries × 20 = 480 bytes of entry
array + one segment CRC of 4 bytes = 484, "with no padding anywhere inside the
region".)

Confidence: high. Determined.

---

## Q11 — outcome class and Detected column

**Answer: `reject-layer; layer access`**

G_n = ⌈300,000,000 / 300,000,000⌉ = 1, N = 1, planar C = 2 → entry_count = 2.
P = ∏Tᵢ = 300,000,000.

Decoded sizes (§14.2, §14.3): channel `d` float64 planar → P · B = 300,000,000 ×
8 = **2,400,000,000** bytes; channel `m` bool planar → packed, ⌈P/8⌉ =
37,500,000 bytes.

§17.2 `[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes … in a planar layer each
channel's plane carries its own decoded size (§14.2, §14.3), and the largest
governs — and a reader MUST treat such a declaration as a validity error at layer
scope, checkable from declarations alone."

0x7E000000 = 2,113,929,216 < 2,400,000,000. Violation.

*(a)* §21.3's heading: "Outcome: reject-layer". → **reject-layer**.
*(b)* Row L44's *Detected* cell reads **layer access** — consistent with §19.3
`[R-RDR-03]`, which lists "the codec declaration bounds (`[R-COD-07]`)" among the
checks due at first access to a layer.

The layer's tiles also exceed §21.9's 256 MiB tile guarantee, but that is a
minimum guarantee, not a validity limit — a resource decline under `[R-ERR-04]`
would be reported "as a resource limit and not as a validity error", and does not
displace the established L44 violation.

Confidence: high. Determined.

---

## Q12 — slab invariants

**Answer: `none`**

§16.2 `[R-SLB-02]`: interleaved → "the single block [0, N)". N = 6 (6 addressed
tiles, interleaved). "Run r of a block starts at ordinal block_start + r·S" with
S = 3 → run 0 = ordinals [0,3), run 1 = ordinals [3,6).

`[R-SLB-03]`: "the run's stored tiles are contiguous and packed in ordinal order
— each stored tile's offset equals the previous stored tile's offset plus its
length — and the first stored tile's offset satisfies offset mod A_slab = 0."

**Run 0** (ordinals 0, 1, 2). Ordinal 1 is a sentinel: "Sentinel tiles are
transparent to run continuity: they occupy no bytes and do not break packing."
Stored: (4096, 200) then (4296, 100). First offset 4096 mod 512 = 0 ✓. Packing:
4096 + 200 = 4296 ✓.

**Run 1** (ordinals 3, 4, 5). Ordinal 4 is a sentinel — transparent. Ordinal 3's
only defect is that its stored bytes fail its crc, and §16.2 is explicit: "An
entry whose only defect is that its stored bytes fail its crc is not transparent
— its offset and length stand, and the packing relation reads them as it does any
other stored tile's". §15.3 agrees: "its extent stands and it keeps its place in
the *verifier* rows, in run continuity, and in the coverage walk." Stored:
(2048, 30) then (2078, 60). First offset 2048 mod 512 = 0 ✓. Packing:
2048 + 30 = 2078 ✓.

Run 1 sitting at lower offsets than run 0 is fine: "The runs themselves are not
mutually ordered or joined: between runs, placement freedom (`[R-SLB-05]`)
governs."

Both runs satisfy L40's inapplicable (A = 0), L41's packing and L42's alignment.
→ **none**. (The crc failure on ordinal 3 is a separate reject-tile under T1 /
`[R-CNT-20]`, but the question asks only about §16's invariants.)

Confidence: high. Determined. This question is engineered so that the "an entry
failing only its crc is not transparent" clause is load-bearing — and it points
*toward* satisfaction here, since treating entry 3 as transparent would leave
ordinal 5 as run 1's first stored tile (2078 mod 512 = 30 ≠ 0, a L42 violation).
I checked that inverted reading explicitly and the text forecloses it twice.

---

## Q13 — Appendix G emission order

**Answer: `E, C, A, G, D, F, B`**

Appendix G item 3: "For each layer in ascending layer-name byte order: its stored
tiles in disk-ordinal order, then its tile-index region; then any record extents
in ascending record order — all of them after every layer's tiles and index
region, not interleaved with them; then the directory. That order runs over
top-level records first, then, within each layer record, its sub-records".

`alpha` < `beta` in byte order, so:

1. **E** — alpha's stored tiles
2. **C** — alpha's tile-index region
3. **A** — beta's stored tiles
4. **G** — beta's tile-index region
5. **D** — the top-level user-metadata record's extent (top-level records first)
6. **F** — beta's user-metadata sub-record's extent (then each layer's sub-records)
7. **B** — the directory region

The layer records' own extents *are* the tile-index regions (§7.4), and item 3
places those with their layers rather than in the record-extent group — the
clause "all of them after every layer's tiles and index region" distinguishes the
two groups. Both D and F are type 0x0002, so the type ordering does not separate
them; the top-level-then-sub-records clause does.

"The first structure begins at 16, directly after the front signature block …
each later structure begins where the previous one ended" — contiguous, as the
question's "beginning at file offset 16" reflects.

Confidence: high. Determined.

---

## Q14 — segment CRC failure

**Answer: `reject-layer; stand`**

*(a)* §15.4 `[R-IDX-04]`: "To use entry k, a reader MUST verify, in dependency
order, crc_of_crc_array over the fetched CRC array and the segment CRC over the
fetched segment containing k …; any mismatch or cross-check failure
(`[R-CNT-17]`) is **reject-layer**." §8.2 `[R-CNT-20]` agrees: "any of a layer's
index cross-checks, CRC array, or segments → reject-layer". Register row L38.
(Detection point is *tile use*, but §19.2: "Failure at any point takes the
violated rule's own outcome and scope — in particular, index-chain failures take
layer scope (`[R-IDX-04]`) although their detection point is tile use.")

*(b)* §2.4's reject-layer row: "The outcome is prospective: it bars further
service from the layer, and does not retroactively invalidate content already
returned under §19.2's validation timing (`[R-RDR-02]`)."

§19.4 step 8 states it for this exact shape of request: "A failure inside the
same request that takes layer scope instead — step 3's index-chain failure
(`[R-IDX-04]`) — bars the request's remaining entries and all further service
from the layer; the bar is prospective, so values the reader has already returned
under §19.2's timing **stand** (§2.4)."

The already-returned fill was legitimate: entry 100 was a valid sentinel read
from a verified chain, which §13.3 `[R-TYP-09]` names as "exactly one condition"
producing fill. → **stand**.

Confidence: high. Determined.

---

## Q15 — new trailer

**Answer: `448; d4000000000000006d00000000000000`**

Starting F₀ = 128 (Appendix A). `[R-LIF-02]` step 1: "begin writing at exactly F".

**Tile-index region.** entry_count = 4 (§7.4's example: "The grid count is
⌈100 / 32⌉ = 4 … so entry_count = 4"). `[R-CNT-17]`: 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 —
the example states this figure itself. Region occupies **[128, 212)**.

**Directory.** Begins at 212 as stipulated. Record sequence = one layer record =
24-byte header (§7.2) + inline_length 81 (§7.4's example: "The inline payload is
81 bytes") = **105**. §7.1: the region is the record sequence followed by its
4-byte CRC → dir_length = **109**, region **[212, 321)**.

**Pad and trailer.** `[R-LIF-02]` step 5: "append the pad to the next 64-byte
boundary … and the new trailer, with … committed_file_length equal to the new
end". Directory ends at 321; the next 64-byte boundary is 384 (64 × 6). Pad =
[321, 384), 63 bytes — the only gap the specification requires. Trailer occupies
[384, 448).

*(a)* committed_file_length = **448**. Checks: 448 mod 64 = 0 ✓ (§6.2);
dir_offset 212 ≥ 16 ✓; dir_length 109 ≥ 4 ✓; dir_offset + dir_length = 321 ≤
F − 64 = 384 ✓; §6.2 `[R-CNT-05]`: no structure between the directory's end and
the trailer ✓.

*(b)* Trailer offsets 24 and 32 are dir_offset and dir_length, both u64
little-endian (§6.2 layout table):

- dir_offset 212 = 0xD4 → `d4 00 00 00 00 00 00 00`
- dir_length 109 = 0x6D → `6d 00 00 00 00 00 00 00`

Confidence: high. Determined.

---

## Summary

| Q | Answer |
|---|---|
| Q01 | `b346508a` |
| Q02 | 127 |
| Q03 | `faff` |
| Q04 | `840; b80b000000000000000000000000000078563412` |
| Q05 | `nonconforming; ignore-record` |
| Q06 | `cannot establish` |
| Q07 | `retain, may-drop` |
| Q08 | `barred` |
| Q09 | `MUST verify` |
| Q10 | 484 |
| Q11 | `reject-layer; layer access` |
| Q12 | `none` |
| Q13 | `E, C, A, G, D, F, B` |
| Q14 | `reject-layer; stand` |
| Q15 | `448; d4000000000000006d00000000000000` |

**Underdetermined: none.** I looked for genuine ambiguity at each question and
did not find any I could sustain against the text. The two places where I
expected to find it — Q04 (may a compactor emit a known-defective entry?) and
Q12 (is a crc-failing entry transparent to run continuity?) — are each addressed
by an explicit sentence added for exactly that case. I record that as a finding
about the document, not as confidence in myself: I am reporting no
underdetermination because the text resolved every case I probed, not because
zero is a target.

**One oddity worth naming, not an ambiguity.** Q08's commit is barred by
`[R-WRT-04]` while §21.7 concedes it has no live-state witness — "a commit that
supersedes every tile it would have damaged leaves the live state clean, so the
bar is unwitnessed there". A verifier handed the generation-8 file would certify
it. The rule and the register are consistent (§21's completeness clause is
scoped to *detectable* violations, and §21.7 is the account of what fails that
gate), but a reader of the register alone could mistake the absence of a row for
permission. The question asks what the specification permits, and it does not
permit this.
