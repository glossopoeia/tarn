# Cleanroom round 17 — quiz answerer transcript

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole document, lines 1–4318, in five `Read` calls). Ran three `grep`/`sed`
invocations against that same file only, to pull exact quotations. Ran three
Python scripts I wrote myself in the scratchpad (`calc.py`, `q01.py`,
`rest.py`) that read no files — CRC-32C, ceiling division, struct packing.
No ADRs, no `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`/`AGENTS.md`/`README.md`, no git history, no web, no directory
listing, no reading of the output directory.

## Tool validation before any answer

My CRC-32C (Castagnoli 0x1EDC6F41, reflected, init/final 0xFFFFFFFF)
reproduces every constant §4.5, §7.4, §15.4 and Appendix A publish:

| Input | Computed | Spec |
|---|---|---|
| `"123456789"` | 0xE3069283 | §4.5 |
| zero bytes | 0x00000000 | §4.5 |
| 4 sentinel entries (80 B) | 0x80A34955 | §7.4 example |
| `55 49 A3 80` | 0xC4EE982E | §7.4 example |
| 2¹⁶ sentinel entries | 0xEECB3BB2 | §15.4, Appendix B |
| Appendix A trailer [0,60) | 0xE00938D2 | Appendix A |

The last also validates my little-endian field packing for the trailer.

---

## Q01 — directory terminal CRC of a one-record file

Layout given: front [0,16); record extent [16,22); directory [22,51);
pad [51,64); trailer [64,128); F = 128.

**The extent.** §7.1 `[R-CNT-25]`: a user-metadata record "carries its
document in its extent — never inline". §8.1: the user-metadata extent's
checksum is its "final 4 bytes", covering "the preceding bytes". So
extent = `7B 7D` + CRC-32C(`7B 7D`) = `7b 7d aa d0 7b 29`, 6 bytes,
matching [16,22). extent_length 6 ≥ 5 (§7.1). ✓

**The directory.** dir_length = 29; §7.1: "Its final 4 bytes are a CRC-32C
over the preceding dir_length − 4 bytes". So the record sequence is
[22,47) = 25 bytes, and the answer sits at [47,51).

**The record** (§7.2 framing, 24-byte header + inline_length):

- type = 0x0002 (user metadata, §7.3) → `02 00`
- flags: §7.3 fixes MU = 0, PE = 1 for type 0x0002, and `[R-CNT-22]`
  makes that mandatory on writers ("writers MUST emit exactly the flag
  values fixed in the table above"). bit 0 = MU = 0, bit 1 = PE = 1
  (§4.4: bit 0 is LSB) → value 2 → `02 00`
- inline_length: §18.2 `[R-MTA-03]` — "A user-metadata record's inline
  payload is exactly one byte" → 1 → `01 00 00 00`
- extent_offset = 16 → `10 00 …`
- extent_length = 6 → `06 00 …`
- inline payload: encoding u8 = 1 (none, declared) → `01`

25 bytes: `02000200010000001000000000000000060000000000000001`

CRC-32C = 0x8A5046B3, stored little-endian (§4.5 `[R-ENC-09]`).

**Answer: `b346508a`**

Cross-checks: dir_offset 22 ≥ 16 ✓; dir_length 29 ≥ 4 ✓;
22 + 29 = 51 ≤ F − 64 = 64 ✓; F mod 64 = 0 ✓; pad [51,64) is exactly
`[R-LIF-02]` step 5's pad to the next 64-byte boundary ✓.

---

## Q02 — inline_length of the `ocean` layer record

§7.4's payload table, in table order, packed "with no alignment or padding
between them" (`[R-CNT-18]`):

| Part | Bytes |
|---|---|
| name `ocean` (u8 len + 5) | 6 |
| layout u8, linearization u16, codec u16, filter u16, A u64, S u64, A_slab u64, rank u8, C u16 | 34 |
| 3 dimension entries, each 1 + 1 + 8 + 8 | 54 |
| channel `u` float64: 1+1+2+1+8 | 13 |
| channel `v` int16: 1+1+2+1+2 | 7 |
| index_encoding u8 + entry_count u64 + crc_of_crc_array u32 | 13 |
| sub-records | 0 |

Fill lengths follow `[R-CNT-23]`: "fill length equals the type's element
size" — float64 = 8, int16 = 2 (§12.1 table).

6 + 34 + 54 + 13 + 7 + 13 = **127**

Sanity: §7.4's own worked example accounts identically — "Name and the nine
scalars from layout through channel count occupy 4 + 34 bytes … the
trailing fixed fields 13". Here the name is 6 rather than 4, rank 3 rather
than 1, and two channels rather than one.

The declared values (planar, zstd, byte-shuffle, A = 0, S = 16,
A_slab = 4096) change no field width — `[R-ENC-06]`: "No field's width is
ever a writer choice".

**Answer: 127**

---

## Q03 — decoded tile image of a packed bool plane

Planar + bool → §14.3 `[R-SER-03]`: "the decoded tile image is the tile's
P values bit-packed LSB-first: value k occupies bit k mod 8 of byte
k div 8 … and the decoded size is ⌈P/8⌉ bytes."

P = ∏Tᵢ = 4 × 4 = 16 (§11.2). Decoded size = ⌈16/8⌉ = 2 bytes.
P mod 8 = 0, so there are **no pad bits** (§14.3).

Tile (t_y,t_x) = (1,1) covers y ∈ [4,8), x ∈ [4,8). In-tile ordinal
= u_y·T_x + u_x = u_y·4 + u_x (§11.4, row-major in-tile ordinal
Σ uᵢ·∏_{j>i} Tⱼ, permanent for every linearization).

Real positions (E_y = 5, E_x = 7): y = 4 only, x ∈ {4,5,6}:

- (4,4) → ordinal 0 → false → bit 0
- (4,5) → ordinal 1 → true → bit 1
- (4,6) → ordinal 2 → false → bit 0

Ordinal 3 is (y,x) = (4,7), x ≥ 7 — padding. Ordinals 4–15 have u_y ≥ 1,
so y ≥ 5 — padding. §14.5 `[R-SER-05]`: at every padding position a writer
"MUST encode … the fill bit in a packed plane". Fill = 0x01 = true → 1.

Bits 0–15 = 0,1,0, then thirteen 1s.
Byte 0 = 0b11111010 = 0xFA. Byte 1 = 0xFF.

**Answer: `faff`**

---

## Q04 — compactor rewriting a length-0 entry

**Ordinal.** G_y = ⌈100/32⌉ = 4, G_x = ⌈200/64⌉ = 4, N = 16 (§11.2).
(70,130) → t = (2,2) → s = 2·4 + 2 = 10 (§11.4, row-major).
Planar disk ordinal = c·N + s = 2·16 + 10 = 42 (`[R-GEO-06]`).

**Byte offset.** §15.1 `[R-IDX-01]`: "The entry for the tile with disk
ordinal k … is the k-th entry, at region byte 20·k" → 20 × 42 = **840**.
The compactor does not renumber ordinals: geometry is unchanged.

**The 20 bytes.** length = 0 with a non-sentinel offset is §15.3's row
"length = 0 (non-sentinel) | *structural*: reject-tile". §20.5
`[R-WRT-07]` states this case verbatim: "an entry §15.3 classifies
reject-tile on a structural ground is reproduced with its offset and
length exactly as they stand, there being no live extent for a
re-pointing to target … and the violation travels with it into the
output". Entry crcs are likewise "unchanged".

And the compactor is not obliged to refuse: "`[R-WRT-09]`'s checks reach
the index chain and each stored tile's entry crc, not an entry's own value
domain, so such an entry is not one `[R-WRT-06]` obliges a compactor to
refuse."

offset 3000 = `b8 0b 00 00 00 00 00 00`; length 0 = eight zero bytes;
crc 0x12345678 = `78 56 34 12` (little-endian, `[R-ENC-09]`).

**Answer: `840; b80b000000000000000000000000000078563412`**

---

## Q05 — verdict, and the outcome for encoding 0x05

Encoding 0x85 ≥ 0x80 → experimental range (§10.2, §18.2). §21.6:
"A user-metadata record declares an experimental-range (≥ 0x80) document
encoding | Ignored (ignore-record); the file is conforming … a verifier
certifies, reporting the record it ignored". Not a violation, and not a
cannot-establish ground (`[R-MTA-10]`: "the record is not among
`[R-CNF-11]`'s cannot-establish grounds, and certification is
unaffected").

Encoding 0x05 is in the reserved range 3–0x7F. §21.5 row R1: "A
user-metadata record declares a document encoding of 0, or a
reserved-range value (3-0x7F)" — a violation, outcome ignore-record.
§21.5's preamble: "Every row here is a violation all the same: the outcome
bounds a reader's blast radius and never makes the file conforming."
§21.5 also says expressly: "Encoding 0 and a reserved-range value are
unassigned too, and R1 registers both as violations: what `[R-MTA-10]`
withdraws is the document's content rules, never the encoding byte's own
value set."

So the verifier establishes exactly one violation. §2.3: "An established
violation takes priority: a verifier that has established any violation
reports *nonconforming*." Nothing is left unchecked — under an unassigned
encoding "no content rule attaches" (`[R-MTA-10]`), so there is no
`[R-MTA-09]` decline either.

**Answer: `nonconforming; ignore-record`**

---

## Q06 — verifier declining a 32 MiB window

The file is conforming: window 32 MiB ≤ decoded size 64 MiB, so
`[R-COD-06]`'s window rule (and T21) is satisfied; 64 MiB is within
§21.9's 256 MiB tile guarantee. §17.2 anticipates exactly this: "Writers
SHOULD keep the declared window within §21.9's 8 MiB `Window_Size`
guarantee even for a larger tile; a wider window is conforming and merely
permits a conforming reader to decline the tile or the layer on resource
grounds (`[R-ERR-04]`)."

The layer has edge-padding positions, so §14.5 `[R-SER-05]`'s content
obligation attaches and requires decoding — and §9.7 makes decoding every
stored tile a verifier duty in any case.

§2.3 lists this precisely as a cannot-establish ground: a verifier reports
*cannot establish* "when it declines a layer's or a tile's decode on
resource grounds and so cannot check §14's decoded-content obligations
(`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`)". It established no violation
elsewhere, so the reservation clause is satisfied: "*cannot establish* is
available only to a traversal that established no violation."

`[R-ERR-04]` also requires the refusal be reported as a resource limit,
not a validity error — but that constrains the report, not the verdict.

**Answer: `cannot establish`**

---

## Q07 — two experimental MU = 0 / PE = 0 records across an add-a-layer commit

Both types are ≥ 0x8000 → experimental range (§10.2), unimplemented by
this appender, so §20.4's "For a type the updater does not implement, the
stored flags are authoritative" applies, MU = 0 / PE = 0 row:

> "An appender may drop it only in a commit that *independently* changes
> the scope the record attaches to: for a layer sub-record, that layer's
> record, the entry set of its index, or which of its tiles are stored;
> for a top-level record, the file's layer set — which a commit changes by
> adding or removing a layer and equally by modifying any layer's record —
> or another *non-layer* top-level record."

- **Layer-`a` sub-record.** Its scope is layer `a`. The question stipulates
  nothing about `a` changes — not its record, not its index entry set, not
  its stored-tile set. No independent change → the permission does not
  open → **retain**.
- **Top-level record.** Its scope is the file's layer set. Adding layer
  `c` is named in the rule as exactly such a change → **may-drop**
  (and `SHOULD report the loss`).

**Answer: `retain, may-drop`**

---

## Q08 — unstore everything, then re-type the channel

§20.3 step 4 `[R-WRT-04]`:

> "A commit MUST NOT change a layer's declarations in a way that alters,
> for any tile that layer stores **in the generation this commit
> supersedes**, what §14 fixes for its stored bytes or how they decode —
> … the decoded size, the byte offset of any sample within the decoded
> tile image …"

Generation 7 (the superseded generation) stores all four tiles.
uint8 → uint16 changes Q from 1 to 2 (§14.2), so decoded size goes
P·Q = 16·1 = 16 → 32 bytes, and every sample offset moves.

The commit's simultaneous unstoring does not rescue it — the spec
forecloses this exact manoeuvre twice: "The tense is the prior
generation's … so a commit does not escape this by unstoring in the same
breath: superseding every tile of a layer and re-declaring it are one
operation, and this bars it"; and on the free-redeclaration permission,
"the tense is the bar's, so a commit does not earn this permission by
emptying the layer as it re-declares it."

Noted oddity (not a hedge): §21.7 records that this is precisely where the
bar has no witness — "a commit that supersedes every tile it would have
damaged leaves the live state clean, so the bar is unwitnessed there". The
commit is barred and undetectable; the question asks about permission, and
permission is denied.

**Answer: `barred`**

---

## Q09 — front block after a 200 response the reader keeps

`[R-CNT-10]` licenses the accept: a remote reader "MUST handle a 200
response to a range request (abort or accept the full body deliberately)".
Having accepted, the reader holds all 40,960 bytes — bytes [0,16)
included.

`[R-CNT-04]` turns the obligation on residency, not transport:

> "A reader whose open leaves bytes [0, 16) **resident** — a local file
> read whole, a memory mapping, a speculative suffix window that reached
> offset 0, or any transport already holding them — MUST verify the full
> block by byte equality before other processing, and MUST treat any
> mismatch as reject-file."

"any transport already holding them" covers this exactly, and the
deferral clause is expressly limited to "a reader that would have to issue
a further range request to obtain those bytes" — this one would not. The
section adds: "The test is residency, not transport."

**Answer: `MUST verify`**

---

## Q10 — extent_length from geometry

Grid counts (§11.2, ceiling division): G_t = ⌈1000/256⌉ = 4;
G_u = ⌈1/4⌉ = 1 (§11.1: "where 0 < Eᵢ < Tᵢ the grid is then a single
padded tile along that axis"); G_w = ⌈3/2⌉ = 2.

N = 4 · 1 · 2 = 8. Planar → addressed-tile count = C·N = 3 · 8 = 24, and
`[R-CNT-17]` requires entry_count to equal it.

`[R-CNT-17]`: "Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4".

24 × 20 + ⌈24/65536⌉ × 4 = 480 + 4 = **484**

(Consistent with §15.1's region layout: 24 entries × 20 B, then a
single-segment CRC array of 4 B.)

**Answer: 484**

---

## Q11 — lz4 on a 2.4 GB plane

Planar layer, so each channel's plane carries its own decoded size
(§14.2, §14.3). G_n = ⌈300,000,000/300,000,000⌉ = 1, N = 1,
P = ∏Tᵢ = 300,000,000.

- channel `d`, float64 (B = 8): P·B = 2,400,000,000 bytes
- channel `m`, bool planar → packed: ⌈P/8⌉ = 37,500,000 bytes

`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of
whose addressed tiles' decoded size exceeds 0x7E000000 bytes … in a planar
layer each channel's plane carries its own decoded size (§14.2, §14.3),
and the largest governs — and a reader MUST treat such a declaration as a
validity error at layer scope, checkable from declarations alone."

0x7E000000 = 2,113,929,216 < 2,400,000,000. Violation.

Register row L44 (§21.3, outcome reject-layer): "Codec 4 (lz4) declared on
a layer any of whose addressed tiles' decoded size exceeds 0x7E000000
bytes — in a planar layer the largest channel plane governs | … | reader |
**layer access** | `[R-COD-07]`". §19.3 also lists "the codec declaration
bounds (`[R-COD-07]`)" among first-access checks.

The layer does address a tile (E = 300,000,000 > 0), so §17.2's empty-layer
escape does not apply.

**Answer: `reject-layer; layer access`**

---

## Q12 — slab invariants over a crc-failing tile

Interleaved → one block [0, N) = [0,6) (`[R-SLB-02]`). S = 3 → run 0 =
ordinals [0,3), run 1 = ordinals [3,6).

`[R-SLB-03]`: sentinels are transparent; entries §15.3 classifies
reject-tile on a *structural* ground are transparent; but "An entry whose
only defect is that its stored bytes fail its crc is not transparent — its
offset and length stand, and the packing relation reads them as it does
any other stored tile's". Ordinal 3 is well-formed (offset 2048 ≥ 16,
length 30 ≠ 0, neither field sentinel); §15.3's own row says so: "the
entry itself is well-formed; its extent stands."

Run 0: stored = ordinals 0, 2 (1 is a transparent sentinel).
First stored offset 4096; 4096 mod 512 = 0 ✓.
Packing: 4096 + 200 = 4296 = ordinal 2's offset ✓.

Run 1: stored = ordinals 3, 5 (4 transparent).
First stored offset 2048; 2048 mod 512 = 0 ✓.
Packing: 2048 + 30 = 2078 = ordinal 5's offset ✓.

Run 1 lying at lower offsets than run 0 is fine: "The runs themselves are
not mutually ordered or joined: between runs, placement freedom
(`[R-SLB-05]`) governs" (§16.2).

Both runs satisfy L41 and L42. The crc failure is T1 (reject-tile), not a
§16 matter.

**Answer: `none`**

---

## Q13 — Appendix G emission order

Item 3, "A total emission order, contiguously":

> "For each layer in ascending layer-name byte order: its stored tiles in
> disk-ordinal order, then its tile-index region; then any record extents
> in ascending record order — all of them after every layer's tiles and
> index region, not interleaved with them; then the directory. That order
> runs over top-level records first, then, within each layer record, its
> sub-records."

`alpha` < `beta` in byte order.

1. alpha's stored tiles → **E**
2. alpha's tile-index region → **C**
3. beta's stored tiles → **A**
4. beta's tile-index region → **G**
5. record extents, top-level first → the top-level user-metadata extent
   → **D**
6. then within layer records, sub-records → beta's sub-record extent
   → **F**
7. the directory → **B**

(Tile-index regions are record extents in §5.2's taxonomy, but item 3
places them explicitly with their layer, ahead of the "any record extents"
clause; and item 3 fixes the first structure at offset 16.)

**Answer: `E, C, A, G, D, F, B`**

---

## Q14 — a segment CRC failure after fill has already been returned

**(a) Outcome class.** §15.4 `[R-IDX-04]`: "To use entry k, a reader MUST
verify, in dependency order, crc_of_crc_array over the fetched CRC array
and the segment CRC over the fetched segment containing k … any mismatch
or cross-check failure (`[R-CNT-17]`) is **reject-layer**." §8.2
`[R-CNT-20]` agrees: "any of a layer's index cross-checks (`[R-CNT-17]`),
CRC array, or segments → reject-layer." Register row L38 is the row, its
outcome reject-layer (§21.3). §19.2 notes the timing wrinkle explicitly:
"index-chain failures take layer scope (`[R-IDX-04]`) although their
detection point is tile use."

Segment arithmetic checks out as the question describes: ordinal 100 is in
segment 0, ordinal 150,000 in segment 2 (150,000 div 65,536 = 2), so these
are genuinely different segments each needing its own verification, while
the crc_of_crc_array verification is shared.

**(b) Retract or stand.** §2.4's reject-layer row: "The outcome is
prospective: it bars further service from the layer, and does not
retroactively invalidate content already returned under §19.2's validation
timing (`[R-RDR-02]`)." §19.4 step 8 says the same thing for this precise
situation — a layer-scope failure arising mid-request:

> "A failure inside the same request that takes layer scope instead —
> step 3's index-chain failure (`[R-IDX-04]`) — bars the request's
> remaining entries and all further service from the layer; the bar is
> prospective, so values the reader has already returned under §19.2's
> timing stand (§2.4)."

The fill for entry 100 was returned lawfully: entry 100's own chain
(crc_of_crc_array plus segment 0's CRC) verified, and `[R-TYP-09]` is
satisfied — "Fill is produced by exactly one condition: a sentinel entry
read from a verified index chain". So it stands.

**Answer: `reject-layer; stand`**

---

## Q15 — one commit adding §7.4's `sst` layer to Appendix A's file

Appendix A: F = 128, generation 1.

**Index region.** entry_count = 4; no tile stored, so all four entries are
the sentinel. §15.1 / `[R-CNT-17]`: length = 4 × 20 + ⌈4/65536⌉ × 4 = 84
— which §7.4's example states outright ("an extent slot of length
4 × 20 + ⌈4 / 2¹⁶⌉ × 4 = 84"). Written first, "beginning at the file's
committed file length" = 128 → [128, 212).

**Directory.** First byte immediately follows → dir_offset = 212.
Record sequence = one layer record = 24-byte header (§7.2) +
inline_length 81 (§7.4's example) = 105 bytes; plus the terminal CRC-32C
(§7.1) → dir_length = 109. Directory occupies [212, 321).

**Pad and trailer.** `[R-LIF-02]` step 5: "append the pad to the next
64-byte boundary … and the new trailer". Directory ends at 321; next
64-byte boundary is 384 (63 pad bytes, the only gap the specification
requires). Trailer [384, 448).

committed_file_length = **448**. Checks: 448 mod 64 = 0 (§6.2) ✓;
dir_offset + dir_length = 321 ≤ F − 64 = 384 ✓; dir_offset 212 ≥ 16 ✓;
dir_length 109 ≥ 4 ✓; no structure between directory end and trailer
(`[R-CNT-05]`) ✓.

**Trailer [24,40)** = dir_offset u64 then dir_length u64 (§6.2 layout),
little-endian:
212 = 0xD4 → `d4 00 00 00 00 00 00 00`;
109 = 0x6D → `6d 00 00 00 00 00 00 00`.

**Answer: `448; d4000000000000006d00000000000000`**

---

## Underdetermined questions

None of the fifteen. Every one resolved to a single reading with a
decisive sentence; the two that looked most likely to fork — Q04's
structural entry under compaction and Q12's crc-failing tile in a slab
run — are each addressed by an explicit clause written for that case
(`[R-WRT-07]`'s parenthesis and `[R-SLB-03]`'s "is not transparent"
sentence). Q08 is a case the document declares barred *and* undetectable
(§21.7); that is an oddity of the register's coverage, not an
underdetermination of the rule.
