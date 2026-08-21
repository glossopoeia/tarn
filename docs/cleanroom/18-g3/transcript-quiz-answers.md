# Round 18 — quiz answerer transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(via `grep -n '^#'` for the heading list, then the Read tool over lines 94–4340 in
chunks; §1 lines 1–93 unread, §22–§23 lines 3705–3876 unread — neither bears on the
slate). I ran one local Python script (`calc.py`, in this scratchpad) implementing
CRC-32C and the byte-shuffle filter; it reads no files. No ADRs, no `docs/`, no
`conformance/`, no `registry.json`, no git history, no web.

**Tool self-validation.** Before using my CRC-32C implementation for any answer I
reproduced five constants the specification itself states, plus the Appendix A trailer:

| Check | Computed | Spec (§4.5 / §7.4 / §15.4 / App. A) |
|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` | `0xE3069283` ✓ |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` ✓ |
| CRC over 4 sentinel entries (80 B) | `0x80A34955` | `0x80A34955` ✓ |
| CRC over `55 49 A3 80` | `0xC4EE982E` | `0xC4EE982E` ✓ |
| CRC over 2¹⁶ sentinel entries | `0xEECB3BB2` | `0xEECB3BB2` ✓ |
| Appendix A trailer CRC | `0xE00938D2` | `0xE00938D2` ✓ |

The Appendix A reproduction is byte-exact across the whole 64-byte trailer, so my field
packing for §6.2 is validated, not merely my polynomial. My byte-shuffle routine was
likewise validated against §17.3's worked example (three float32 → `00 00 00 00 00 00 80
00 40 3F 40 40`), reproduced exactly.

---

## Q01 — the 64-byte trailer

§6.2's layout table gives offsets 0/8/10/12/16/24/32/40/48/56/60. Bit numbering: §4.4
`[R-ENC-08]` — "bit 0 is the least significant bit". Bit 18 alone ⇒ flags = 0x00040000,
stored little-endian (`[R-ENC-01]`) as `00 00 04 00`. Reserved: §6.2's table, "zero".

```
[0,8)   8A 4E 52 41 54 0D 0A 1A   trailer magic
[8,10)  01 00                     version_major 1
[10,12) 00 00                     version_minor 0
[12,16) 00 00 04 00               flags = 0x00040000 (bit 18)
[16,24) 02 00 ...                 generation 2
[24,32) 10 00 ...                 dir_offset 16
[32,40) 04 00 ...                 dir_length 4
[40,48) C0 00 ...                 committed_file_length 192 (0xC0; 192 mod 64 = 0)
[48,56) EF CD AB 89 67 45 23 01   file_id 0x0123456789ABCDEF LE
[56,60) 00 00 00 00               reserved
[60,64) 27 50 94 A8               CRC-32C over [0,60) = 0xA8945027, stored LE
```

**Answer (128 hex chars):**
`8a4e5241540d0a1a0100000000000400020000000000000010000000000000000400000000000000c000000000000000efcdab896745230100000000275094a8`

Decisive: §6.2 layout table; `[R-ENC-08]`; `[R-ENC-09]`.

## Q02 — 3 sentinel entries

(a) §15.1 `[R-IDX-01]`: region = entry_count×20 + ⌈entry_count/2¹⁶⌉×4 = 3·20 + 1·4 = **64**
(also `[R-CNT-17]`'s extent_length formula, same number).

(b) §15.4 `[R-IDX-04]`: "the s-th u32 … is the CRC-32C over exactly those entries' bytes
as stored — the final partial segment's CRC covers only its actual bytes." Segment 0
covers 3 entries = 60 bytes = `FF×16 00×4` three times. CRC-32C = **0xd171d122**.

Trap avoided: `[R-IDX-05]`'s all-sentinel constant `0xEECB3BB2` licenses only a **full**
segment (exactly 2¹⁶ entries); "a partial segment's CRC MUST be computed."

(c) §7.4 / §8.1: crc_of_crc_array is CRC-32C over the segment-CRC array as stored, i.e.
over the 4 bytes `22 D1 71 D1`. = **0x34c74afb**.

## Q03 — planar bool edge tile

Planar bool ⇒ §14.3 `[R-SER-03]`: packed LSB-first, ⌈P/8⌉ bytes. P = ∏Tᵢ = 4·4 = 16 ⇒ 2
bytes; P mod 8 = 0 ⇒ **no pad bits**.

Tile (1,1) covers coordinates 4–7 on both axes; extents (5,5) ⇒ only (4,4) is inside.
In-tile position (0,0) (§11.4: uᵢ = xᵢ mod Tᵢ) ⇒ in-tile ordinal 0. It holds false ⇒ bit 0
of byte 0 = 0.

The other 15 positions are padding positions (§11.3). §14.5 `[R-SER-05]`: "at every
padding position, a writer MUST encode … the fill bit in a packed plane." Fill byte 0x01
= true ⇒ fill bit 1.

bits 0..15 = 0,1,1,1,1,1,1,1 | 1,1,1,1,1,1,1,1 ⇒ byte 0 = 0xFE, byte 1 = 0xFF.
Filter 1 = identity; codec 1 = "stored bytes are the filtered image verbatim"
(`[R-COD-04]`; length 2 = decoded size 2 ✓).

**Answer: `FE FF`**

## Q04 — interleaved, byte-shuffle

C = 2, B_a = 1, B_b = 2 ⇒ Q = 3 (§14.2 `[R-SER-02]`). P = 2·3 = 6 ⇒ decoded size 18.
Decoded image, channel c at ordinal u sitting at byte u·Q + Fᶜ (F_a = 0, F_b = 1):

`01 22 11 | 02 44 33 | 03 66 55 | 04 88 77 | 05 AA 99 | 06 CC BB`

§17.3 `[R-COD-10]`: interleaved ⇒ stride s = Q = 3; n = 18/3 = 6; byte i of group j moves
to offset i·n + j. Groups are the six samples.

i=0 → `01 02 03 04 05 06`; i=1 → `22 44 66 88 AA CC`; i=2 → `11 33 55 77 99 BB`.

Codec 1 stores the filtered image verbatim.

**Answer: `01 02 03 04 05 06 22 44 66 88 AA CC 11 33 55 77 99 BB`**

## Q05 — entry_count 65,537

(a) `[R-CNT-17]`: 65537×20 + ⌈65537/65536⌉×4 = 1,310,740 + 2·4 = **1,310,748**.
(b) Entry array occupies [0, 1,310,740); the CRC array follows contiguously with no
padding (§15.1). Segment 1's CRC is the array's u32 index 1 ⇒ 1,310,740 + 4 = **1,310,744**.
(c) §15.4: segment 1 covers [1·2¹⁶, min(2·2¹⁶, 65537)) = [65536, 65537) ⇒ **1** entry.

## Q06 — one-layer file

Layer's extent_length = 4·20 + 1·4 = 84 (`[R-CNT-17]`; §7.4's example states 84).
Index region [16, 100). Directory begins immediately after ⇒ **dir_offset = 100**.

Directory = record sequence + terminal CRC (§7.1). One record: 24-byte header (§7.2) +
inline_length 81 = 105 bytes; +4 ⇒ **dir_length = 109**. Directory ends at 209.

`[R-LIF-02]` step 5: "append the pad to the next 64-byte boundary … and the new trailer."
Next 64-boundary above 209 is 256 (47 pad bytes). Trailer [256, 320).
**committed_file_length = 320** (320 mod 64 = 0 ✓; 209 ≤ 320 − 64 = 256 ✓; ≥128 ✓).

## Q07 — Appendix G placement

Item 3: "The first structure begins at 16 … each later structure begins where the previous
one ended", gaps only where a declared alignment or the 64-byte trailer alignment forces
one. No alignment declared here.

Order: "For each layer in ascending layer-name byte order: its stored tiles in
disk-ordinal order, then its tile-index region; then any remaining record extents in
ascending record order — all of them after every layer's tiles and index region … then
the directory."

`alpha` (0x61…) < `beta` (0x62…).

- alpha, interleaved, C=1 uint8: P = 4, Q = 1 ⇒ decoded size 4; codec 1, filter 1 ⇒ stored
  length 4. Tile at **[16, 20)**.
- alpha's index: G = ⌈4/4⌉ = 1, N = 1, interleaved ⇒ entry_count 1 ⇒ 1·20 + 1·4 = 24 bytes
  at **[20, 44)**.
- beta: extent 0 ⇒ G = 0, N = 0 (`[R-GEO-02]`, §11.2) ⇒ entry_count 0 ⇒ extent slot (0,0),
  no region (§15.4's closing example: "At entry_count = 0 there is no region at all"), and
  no stored tiles. Contributes nothing.
- remaining record extent: the user-metadata extent, 40 bytes ⇒ **(a) 44**, occupying
  [44, 84).
- directory begins at **(b) 84**.

## Q08 — slab run continuity

`[R-SLB-03]`: "each stored tile's offset equals the previous stored tile's offset plus its
length"; "Sentinel tiles are transparent … So are the entries §15.3 classifies reject-tile
on a *structural* ground … An entry whose only defect is that its stored bytes fail its crc
is **not** transparent — its offset and length stand, and the packing relation reads them
as it does any other stored tile's."

Ordinal 0 at 4096 (4096 mod 1024 = 0 ✓), len 200 ⇒ next stored at 4296. Ordinal 1 sentinel,
transparent.

(a) Ordinal 2 is stored, offset 4296, len 300, crc-mismatched-bytes only ⇒ **not**
transparent, it is the previous stored tile ⇒ ordinal 3 offset = 4296 + 300 = **4596**.

(b) Ordinal 2 offset 0, length 50: non-sentinel with offset < 16 ⇒ §15.3 row "offset < 16
(non-sentinel) | *structural*: reject-tile" ⇒ transparent. Previous stored tile is ordinal
0 ⇒ ordinal 3 offset = 4096 + 200 = **4296**.

## Q09 — trailer CRC vs. foreign major

`[R-CNT-06]`: "A reader MUST validate, in order: the trailer magic; the trailer CRC; the
version gate (§6.3)". The CRC check precedes the version gate, so version_major = 5 is
never reached.

Front block is byte-identical ⇒ F6/F1's front instance clear. Magic is exact ⇒ F8/F1's
magic instance clear. F14: "The u32 at trailer offset 60 does not equal the CRC-32C of
trailer bytes [0,60)" — fires.

§21.2's preamble confirms F14 reaches a foreign-major file: "Four rows are outside that
reasoning and do reach it … F8 and F1's trailer-magic instance, F14's trailer CRC — the two
checks §6.2 places before the gate".

**(a) F14  (b) reject-file** (§21.2 "Outcome: reject-file"; `[R-CNT-06]` "Any failure is
reject-file").

Note the oddity the question probes: the reader never learns the file is a major it cannot
implement; the register row it records is corruption, not capability.

## Q10 — encoding 0x03 vs 0x85

File A (0x03): reserved range 3–0x7F. §21.5 **R1**: "A user-metadata record declares a
document encoding of 0, or a reserved-range value (3-0x7F)" — a registered violation.
§21.5 preamble: "Every row here is a violation all the same: the outcome bounds a reader's
blast radius and never makes the file conforming." A verifier that establishes a violation
reports **nonconforming** (`[R-CNF-11]`).

File B (0x85): experimental range ≥ 0x80. §21.6: "A user-metadata record declares an
experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the file is
conforming … No document rule attaches at such an encoding, so a verifier certifies,
reporting the record it ignored" (`[R-MTA-10]`). Verdict **conforming**.

## Q11 — 40 MiB document + reserved-range type

Type 0x0005 lies in the reserved record-type range 0x0003–0x7FFF (§10.2). §21.2 **F36**:
"A top-level record carries a type value from the reserved range 0x0003-0x7FFF … emitting
one is a violation **whatever its MU bit**" — detector verifier, at certification. (F35
needs MU = 1 and does not fire.)

The 16 MiB decline is a `[R-MTA-09]` cannot-establish ground, but `[R-CNF-11]`: "An
established violation takes priority: a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check, and *cannot establish*
is available only to a traversal that established no violation."

**Verdict: nonconforming.**

## Q12 — what an appender may omit

(iii) type 0x0002 is registry-fixed PE = 1; §20.4: "both registered types carry PE = 1, so
neither can be dropped"; "No commit therefore removes a layer record, or a user-metadata
record at either scope." Not omittable.

(i) and (ii) are MU = 0 / PE = 0 of unimplemented types ⇒ stored flags authoritative ⇒
§20.4's third row: droppable only "in a commit that *independently* changes the scope the
record attaches to: for a layer sub-record, that layer's record, the entry set of its
index, or which of its tiles are stored; for a top-level record, the file's layer set, any
layer record's content, or another *non-layer* top-level record."

The commit supersedes a tile of layer A ⇒ layer A's index region is re-placed, moving its
extent slot ⇒ layer A's record content changes. The table spells the consequence out: "an
appender superseding a tile MAY drop a top-level such record, **or such a sub-record of the
layer whose tile it superseded**."

(i) qualifies ("any layer record's content"). (ii) is a sub-record of layer **B**, which
the commit does not touch ⇒ must be retained.

**Answer: (i)**

## Q13 — compactor meets a half-sentinel entry

offset = S, length ≠ S ⇒ §15.3 row "offset = S ∧ length ≠ S … *structural*: reject-tile"
(register row T7).

§20.5 `[R-WRT-07]`/`[R-WRT-06]`: "An entry §15.3 classifies reject-tile on a structural
ground is neither — `[R-IDX-03]` gives it no stored extent for a re-pointing to target — so
regenerating the region cannot proceed without meeting it, and the violation is thereafter
one the compactor has detected. `[R-WRT-06]` then obliges refusal: the compactor can
neither reproduce the entry nor invent a replacement, and no drop is available, a
tile-index entry being no record §20.4's table licenses dropping."

**Answer: (d)** — refuse to compact.

## Q14 — compactor output trailer

(a) Bits 18 and 20 are ignore-lane (16–31, §6.3). `[R-WRT-06]`: "The output trailer copies
the input's unknown ignore-lane flag bits forward (`[R-CNT-08]`)". 0x40000 | 0x100000 =
**00140000**.

(b) `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and generation 1". ⇒ **1**.

(c) `[R-WRT-06]`: "carries the greater of `[R-CNT-26]`'s floor and the input's
version_minor". Floor for a file expressible under this text is 0; input is 7 ⇒ **7**.

## Q15 — filter 2 → filter 1 with tiles carried forward

Geometry: G = (⌈16/8⌉, ⌈16/8⌉) = (2,2), N = 4, C = 1 planar ⇒ entry_count = 4;
P = 64; decoded size = P·Bᶜ = 64·4 = 256; extent_length = 4·20 + 4 = 84.

The commit is barred by §20.3 step 4 (`[R-WRT-04]`): it changes "the codec and filter that
produced the stored bytes" for tiles stored in the superseded generation, and the shuffle
is not the identity here (stride 4 over 256 bytes, n = 64).

But the question asks what the **file exhibits**, and §21.7 `[R-ERR-01]` states exactly
when that bar has a witness: "§20.3 step 4's bar on a declaration change is witnessed only
where the affected tiles remain stored *and* the change reaches a byte §14 structurally
constrains — a padding position, a pad bit, or a boolean byte — where §21.4's content rows
fire; a change that reaches the decoded size instead is witnessed by T3 or T14 …; a change
that reaches the codec is witnessed by the rows for the codec now declared … or by T14
where the new declaration is codec 1".

Check each escape:
- Padding positions: Gᵢ·Tᵢ = 2·8 = 16 = Eᵢ on both axes ⇒ **none** (§11.3). T4 cannot fire.
- Pad bits: float32, not a packed bool plane ⇒ **none**. T5 cannot fire.
- Boolean bytes: no bool channel ⇒ T2 cannot fire.
- Decoded size: byte-shuffle is length-preserving (`[R-COD-10]`: "Length is unchanged")
  ⇒ still 256. T3 and T14 cannot fire.
- Codec: unchanged (1, both generations).
- T26 requires filter **2** declared; filter is now 1.
- Index chain, entry crcs, entry_count/extent_length cross-checks, layer record value sets:
  all carried forward unchanged and all valid. Coverage partitions (gen 9's directory, pad
  and trailer become slack, `[R-CNT-21]`).

Every remaining consequence is wrong sample content, which §21.7 places squarely outside
the register: "this format detects *corruption of structure*, not *incorrectness of
content*."

**Answer: none.**
