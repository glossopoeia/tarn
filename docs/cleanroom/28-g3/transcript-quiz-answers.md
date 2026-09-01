# Cleanroom round 28 — quiz answerer transcript

## Access record

Read exactly one specification file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4648 lines, 281,820 bytes). It was where the brief said it would be.

Reading method: `sed -n '1,620p'` (whose stdout the harness auto-persisted to
`~/.claude/projects/.../tool-results/bqyvfw94k.txt` — a verbatim copy of lines
1–620 of the spec, which I then read; not a second source), then the `Read` tool
at offsets 620, 1190, 1589, 2059, 2548, 3038, 3487, 4254. Together these cover
§1 through §21.9 plus Appendices A–C. I did not read Appendix D–H or §22–§24
line-by-line; nothing in the slate turned on them, and Appendix A/B were used
only as cross-checks on my CRC implementation.

Computation: local Python only (CRC-32C table, trailer byte assembly, an
instance-counting script over the register tables in the one spec file). No
other file read. No git, no web, no `docs/`, no `conformance/`, no
`registry.json`, no directory listings.

Contamination that arrived unbidden — see `disclosure`.

---

## CRC implementation validation

Before trusting any CRC arithmetic I reproduced four constants the document
itself fixes:

| Constant | Spec | Computed |
|---|---|---|
| CRC-32C("123456789") (§4.5) | 0xE3069283 | 0xE3069283 |
| CRC-32C(zero bytes) (§4.5) | 0x00000000 | 0x00000000 |
| 80-byte all-sentinel entry array (§7.4 example) | 0x80A34955 | 0x80A34955 |
| crc_of_crc_array of that (§7.4 example) | 0xC4EE982E | 0xC4EE982E |
| 2^16 sentinel entries (§15.4) | 0xEECB3BB2 | 0xEECB3BB2 |
| Appendix A trailer CRC | 0x402F157E | 0x402F157E |

All six match. The pipeline (poly 0x1EDC6F41 reflected → 0x82F63B78, init
0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian) is the document's.

---

## Q01 — trailer checksum field bytes

§6.2's layout table: magic [0,8); version_major u16 @8; version_minor u16 @10;
flags u32 @12; dir_offset u64 @16; dir_length u64 @24; committed_file_length
u64 @32; file_id u64 @40; reserved 12 bytes @48; trailer CRC u32 @60 =
"CRC-32C over trailer bytes [0, 60)". §4.1/[R-ENC-01]: all multi-byte values
little-endian. §4.5/[R-ENC-09]: "stored as a little-endian `u32`".

Assembled bytes [0,60):

```
8a4e5241540d0a1a 0100 0000 00000000
4000000000000000 6400000000000000 0001000000000000
bebafeca00000000 000000000000000000000000
```

(dir_offset 64 = 0x40; dir_length 100 = 0x64; committed_file_length 256 =
0x0100; file_id 0x00000000CAFEBABE → `BE BA FE CA 00 00 00 00`.)

CRC-32C = 0x9C67F80D. Stored little-endian → bytes `0D F8 67 9C`.

**Answer: `0df8679c`**

Note the answer form asks for "the four bytes ... in the order they appear in
the file", so this is the byte order, not the numeric value 9c67f80d.

## Q02 — a bfloat16 channel entry

§7.4 channel entry: `name (u8 len + bytes) · type u16 (0 invalid) · fill (u8
len + bytes)`, "fill length equals the type's element size ([R-CNT-23])".
§12.1: bfloat16 is ID **11**, element size **2**.

[R-TYP-02]: "A bfloat16 bit pattern b denotes exactly the value that the IEEE
754 binary32 bit pattern b × 2¹⁶ (b in the high 16 bits, low 16 bits zero)
denotes." Given binary32 0xC0000000 (= −2.0), b × 2¹⁶ = 0xC0000000 ⟹
b = 0xC000. Unique, since the low 16 bits of 0xC0000000 are already zero.

Little-endian storage → fill bytes `00 C0`.

```
01        name length 1
77        'w'
0B 00     type 11 = bfloat16, u16 LE
02        fill length 2 = element size
00 C0     fill 0xC000 LE
```

Cross-checked against §12.3's worked `temp` entry
`04 74 65 6D 70 0C 00 04 00 00 C0 7F` — same field order.

**Answer: `01770b000200c0`** (7 bytes)

## Q03 — interleaved tile, byte-shuffle, codec none

Geometry: rank 2, T = (2,3), P = ∏Tᵢ = 6; extents equal tile extents, so no
padding position. Channels `a` uint8 (B=1) then `b` uint16 (B=2).
§14.2: Q = ΣBᵢ = 3, decoded size P·Q = 18, offset of channel c at in-tile
ordinal u is u·Q + Fᶜ (F_a = 0, F_b = 1). This is exactly §14.2's worked
example ("channels `a` (uint8) and `b` (uint16): Q = 3, decoded size 18").

Decoded tile image (k = 0…5, a = 0xA0+k, b = 0x8000+k little-endian = `k 80`):

```
A0 00 80 | A1 01 80 | A2 02 80 | A3 03 80 | A4 04 80 | A5 05 80
```

§17.1/[R-COD-01]: filter first, then codec; the reader reverses. Filter 2 =
byte-shuffle. [R-COD-10]: stride s = Q = 3 for an interleaved tile; n = L/s =
18/3 = 6; "the filtered image places byte i of group j at offset i · n + j".

- i=0 → offsets 0–5: A0 A1 A2 A3 A4 A5
- i=1 → offsets 6–11: 00 01 02 03 04 05
- i=2 → offsets 12–17: 80 80 80 80 80 80

Direction verified against §17.3's own example (1.0/2.0/3.0 float32 →
`00 00 00 00 00 00 80 00 40 3F 40 40`) — my transform reproduces it exactly.

Codec 1 = none: "The stored bytes are the filtered image verbatim"
([R-COD-04]); length 18 = decoded size, as that rule requires.

**Answer: `a0a1a2a3a4a5000102030405808080808080`** (18 bytes)

## Q04 — decoded tile image, one true bool, interleaved vs planar

P = 1. Fill byte 0x01 = true ([R-TYP-07]).

Interleaved: §14.2 — a bool value is "a single byte, 0x00 = false, 0x01 = true,
with element size 1". Q = 1, decoded size P·Q = 1. Value true → `01`.

Planar: §14.3/[R-SER-03] — a planar **bool** plane is bit-packed; value k
occupies bit k mod 8 of byte k div 8; decoded size ⌈P/8⌉ = 1. Value 0 = true →
bit 0 set. Pad bits are "bit positions P mod 8 through 7" = bits 1–7, and
[R-SER-05] fixes every pad bit to "the plane's channel's fill bit" = true = 1.
So all eight bits set → `FF`.

§14.4's Note confirms the reading: "At P = 1 the two are the same length and
[R-SER-05] fixes the planar pad bits to the channel's fill, so the images
coincide exactly when that fill is false." Here the fill is true, so they must
differ — 01 vs ff.

**Answer: `01 ff`**

## Q05 — major 3, byte-reversed front block

§21.2's preamble derives which rows reach a foreign major: "Deriving it there
yields F8, F14, F6 and both of F1's instances — each asserting an invariant
[R-CNT-24] fixes in every major — and no other row."

The trailer magic is correct and the trailer CRC verifies, so F8 and F14 pass.
The front block is `1A 0A 0D 4E 52 41 54 89` — the constant stored
byte-reversed. That is **F1**'s front-block instance ("A signature constant is
stored byte-reversed"; §21.1 notes F1's front-block instance is the strict
specialization of F6, so the file is recorded against F1). F1's front-block
instance "binds only a reader holding bytes [0, 16) resident ([R-CNT-04])" —
and this reader's open leaves them resident, so it binds.

(a) [R-ENC-02]: "a reader encountering what appears to be a byte-swapped
signature (§6) MUST treat the file as invalid (reject-file), never as a
foreign-endian file to be adapted." Outcome class: **reject-file**.

(b) [R-CNF-13]: a reader "MUST treat its failure as reject-file on the ground
of the requirement stating it rather than on capability grounds; the distinct
diagnostic [R-CNT-07] asks for is owed where every reaching condition is
satisfied and the declared major is one the reader does not implement." Here a
reaching condition is *not* satisfied, so the refusal is not on capability
grounds. **no**

(c) [R-CNF-13]: "A verifier that establishes such a failure reports
*nonconforming*, whatever major the file declares and whether or not it
implements that major." **nonconforming**

**Answer: reject-file; no; nonconforming**

## Q06 — encoding byte 0x03 vs 0x83

§10.2's metadata-encoding space: assigned 1, 2; **reserved 3–0x7F**;
**experimental ≥ 0x80**.

File P (0x03, reserved range): §21.5 row **R1** — "A user-metadata record
declares a document encoding of 0, or a reserved-range value (3-0x7F)" —
outcome ignore-record, detector reader, governing [R-CNT-25]. §21.5's preamble:
"Every row here is a violation all the same: the outcome bounds a reader's
blast radius and never makes the file conforming ([R-CNF-12])." A verifier that
establishes any violation reports *nonconforming* ([R-CNF-11]).
→ **ignore-record, nonconforming**

File Q (0x83, experimental range): §21.6's non-violation table — "A
user-metadata record declares an experimental-range (≥ 0x80) document encoding
| Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a
writer's conduct, not the bytes. No document rule attaches at such an encoding,
so a verifier certifies, reporting the record it ignored." Reinforced by
[R-MTA-10] and [R-CNF-11] ("A user-metadata document under an encoding this
specification does not assign is not such a ground ... certification is
unaffected").
→ **ignore-record, conforming**

The record's other framing is stipulated well formed (inline_length 1, extent
slot with extent_length 40 ≥ 5, terminal CRC verifies), so none of F21/F22/F23,
L10/L11/L12, or R2 fires in either file.

**Answer: ignore-record, nonconforming, ignore-record, conforming**

## Q07 — unknown sub-record type 0x9000, MU = 1

Type 0x9000 ≥ 0x8000 = the record-type experimental range (§10.2).

(a) [R-CNT-18]: "an unknown sub-record type with MU = 1 is reject-layer, and
where the file is otherwise conforming a reader MUST NOT reject the file for
it". → **reject-layer**

(b) §21.6's closing structural discussion: "an **experimental-range top-level
record type carrying MU = 1** ... [R-CNT-15] obliges the reader to reject, and
[R-CNF-02] makes the file conforming all the same. The qualifier is
load-bearing — the same type as a layer sub-record is reject-layer and never a
ground to refuse the file ([R-CNT-18]) ... since the prohibition on publishing
experimental values binds a writer's conduct and not the bytes." MU = 1 with
PE = 1 is the permitted pairing ([R-CNT-12] bars only MU = 1 / PE = 0). The
file exhibits no register row. → **yes**

(c) [R-CNF-11]: a verifier reports *cannot establish* "where some requirement
is one it is unable to check on a capability or resource ground, ... when a
record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)".
No violation was established anywhere, and "*cannot establish* is available
only to a traversal that established no violation" — which is satisfied.
→ **cannot establish**

**Answer: reject-layer; yes; cannot establish**

## Q08 — sentinel offset/length with nonzero crc

§15.3's classification table, row 2: "offset = S ∧ length = S ∧ crc ≠ 0 |
*structural*: reject-tile".

(a) §21.4 row **T6**: "A tile-index entry has offset and length both
0xFFFF_FFFF_FFFF_FFFF but crc ≠ 0" — detector reader, detected at tile use,
governing [R-IDX-03]. (§15.2's Rationale names precisely this: "an all-0xFF
region (erased flash) is invalid too, since a sentinel's crc field is 0.")

(b) **reject-tile**

(c) [R-TYP-09]: "A reader MUST NOT return fill for a tile whose entry is
malformed (§15.3) ... those conditions reject their scopes, and a rejection is
never satisfied by returning fill ([R-CNF-09])." [R-CNF-09] likewise: "a read
of a rejected tile MUST NOT silently return fill." → **no**

**Answer: T6; reject-tile; no**

## Q09 — planar geometry arithmetic

§11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉.
- G_y = ⌈1000/256⌉ = 4 (1000 = 3·256 + 232)
- G_x = ⌈300/128⌉ = 3 (300 = 2·128 + 44)
- N = ∏Gᵢ = 12

"its **addressed-tile count** ... is N for an interleaved layer and C · N for a
planar layer" → 5 · 12 = **60**. [R-CNT-17]: entry_count "equals the
addressed-tile count".

(2) [R-CNT-17]: "Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4" = 60·20 + 1·4 = 1200 + 4 =
**1204**.

(3) [R-GEO-06]: tᵢ = xᵢ div Tᵢ → t_y = 700 div 256 = 2, t_x = 200 div 128 = 1.
"the **spatial tile ordinal** ... is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ" = 2·G_x + 1·1 =
2·3 + 1 = 7. "The **disk tile ordinal** ... is s for an interleaved layer, and
**c · N + s** for a planar layer" = 3·12 + 7 = **43**.
(Shape-checked against §11.4's worked example: C = 4, N = 32, s = 10,
channel 2 → 2·32 + 10 = 74.)

(4) [R-IDX-01]: "The entry for the tile with disk ordinal k (§11.4) is the k-th
entry, at region byte 20·k" = 20 · 43 = **860**.
(§15.4's example: disk ordinal 74 → region bytes [1,480, 1,500) = 20·74. Same
rule.)

**Answer: 60, 1204, 43, 860**

## Q10 — interleaved decoded size and in-image offset

P = ∏Tᵢ = 2·3·4 = 24 (§11.2). Element sizes (§12.1): bool 1, float64 8,
uint16 2. §14.2: bool in an interleaved layer is "a single byte ... with
element size 1 in the arithmetic below".

Q = ΣBᵢ = 1 + 8 + 2 = 11. Decoded size = P·Q = 24 · 11 = **264**.

In-tile ordinal of (1,2,3) — [R-GEO-06], "Σᵢ uᵢ · ∏_{j>i} Tⱼ", row-major for
every linearization: u = 1·(3·4) + 2·(4) + 3 = 12 + 8 + 3 = 23.

F_r (channel `r`'s in-sample offset) = Σ Bⱼ over channels j < r = 1 + 8 = 9.
§14.2's closing form: "channel c's value at in-tile ordinal u sits at byte
u · Q + Fᶜ" = 23 · 11 + 9 = 253 + 9 = **262**.

**Answer: 264, 262**

## Q11 — smallest new committed_file_length

[R-LIF-02]: "A commit's committed_file_length is strictly greater than the
prior trailer's, **by at least 128**, so the committed file length orders a
file's generations". [R-CNT-06] also requires it be a multiple of 64.

4096 + 128 = **4224**, which is 66·64.

§9.2's second Note derives the 128 rather than asserting it, and the derivation
confirms 4224 is reachable: writing begins at exactly F = 4096; dir_offset ≥
4096; dir_length ≥ 4; dir_offset + dir_length ≤ new F − 64. Minimum: directory
at [4096, 4100), pad to 4160, trailer [4160, 4224), F = 4224; check
4100 ≤ 4224 − 64 = 4160. ✓

**Answer: 4224**

## Q12 — instance count of the ignored-record table

§21.5 is the ignore-record table (10 conditions, R1–R10). §21.1's reading
instructions: "Instances within a cell are separated by semicolons, and a cell
reading — is one instance; the count is therefore mechanical once the cell is
written."

Counted mechanically (script over the table rows in the one spec file):

| Row | Instances |
|---|---|
| R1 | 4 |
| R2 | 2 |
| R3 | 2 |
| R4 | 16 |
| R5 | 8 |
| R6 | 4 |
| R7 | 6 |
| R8 | 2 |
| R9 | 2 |
| R10 | 2 |
| **Total** | **48** |

No §21.5 cell is an em dash, so that clause does not bite here.

Method validated: the same script over §21.2–§21.5 yields 35 + 49 + 26 + 10 =
120 rows and 56 + 116 + 55 + 48 = **275** instances — exactly §21.8's "120
conditions over 275 instances". That the totals reconcile is strong evidence
the per-cell counting matches the document's own arithmetic.

**Answer: 48**

## Q13 — compactor's output flags and version_minor

flags = 0x00030000: bits 16 and 17 set, both in the **ignore lane** (bits
16–31, §6.3); the incompat lane is clear, as stipulated. This compactor
implements only what this text defines, and "In this specification's text no
flag bits are defined" — so both set bits are *unknown* ignore-lane bits.

(1) [R-WRT-06]: "The output trailer MUST copy the input's unknown ignore-lane
flag bits forward, in place of the flags = 0 §6.3 requires of a file created
under this text ([R-CNT-08])." §6.3 says the same: "A compactor, though its
output is a new file, carries the input's unknown ignore-lane bits into its
output trailer rather than writing flags = 0". Nothing sets any other bit.
→ **00030000**

(2) [R-WRT-06]: "Where the output carries a feature a later minor defines and
this compactor does not — on a conforming input a carried ignore-lane bit
(§6.3) or an unrecognized `tarn.` key ... — the output's version_minor SHOULD
be at least the input's: a compactor cannot know which minor version defined a
feature it does not implement". The input's minor is 2, and this output does
carry such a feature (the two ignore-lane bits). So the SHOULD floor is 2, and
the smallest permitted value is **2**. ([R-CNT-26]'s own floor would be 0 for a
file expressible under this text, but [R-WRT-06] raises it here.)

**Answer: `00030000`, 2**

## Q14 — may the commit drop each MU = 0 / PE = 0 sub-record?

§20.4's table, MU = 0 / PE = 0 row (the stored flags govern, since the updater
does not implement the type): "An appender MUST NOT drop it except in a commit
that *independently* changes the scope the record attaches to: for a layer
sub-record, that layer's record, the entry set of its index, or which of its
tiles are stored."

Layer A: "Superseding a stored tile's bytes re-places that layer's index region
(§20.3, [R-WRT-04]), moving its extent slot (§7.4) and so modifying that
layer's record, which is such a change: an appender superseding a tile MAY drop
a top-level such record, **or such a sub-record of the layer whose tile it
superseded**." → **yes**

Layer B: nothing about layer B's record, index entry set, or stored-tile set
changes. Its record is re-emitted byte-identically ([R-WRT-05]), which is
preservation, not modification. The commit's only other effects — none — are
excluded by "Dropping the record, or dropping another record in the same
commit, is not itself such a change". → **no**

**Answer: yes, no**

## Q15 — a 1372-byte pre-trailer gap

Directory region is [512, 612); trailer is [1984, 2048). The bytes
[612, 1984) are unclaimed — the pre-trailer pad, 1372 bytes.

(a) [R-CNT-05]: "Writers MUST place the directory so that no structure lies
between its end and the trailer. Those bytes — the **pre-trailer pad** — are
slack (§5.2) ... and bounds their number only through step 5 of the commit
protocol, which pads to the next 64-byte boundary ([R-LIF-02]) — **a longer gap
is conforming**, and no conforming commit produces one." No structure occupies
the gap, so the verifier's file-scope check (F7) does not fire; the bytes are
simply slack, whose content "is unconstrained, and no conformance requirement
applies to it" ([R-CNT-21]). → **yes**

(b) The same sentence: "**no conforming commit produces one**." [R-LIF-02] step
5 appends "the pad to the next 64-byte boundary ... and the new trailer" — from
a directory ending at 612 that is 640, putting the trailer at [640, 704) and
F = 704, not 2048. The creation path and compaction ([R-WRT-06]: "A compactor
MUST follow [R-LIF-02]'s **creation path**") are the same step 5. [R-CNF-02]
names this case explicitly: "§6.2's pre-trailer gap longer than [R-LIF-02] step
5's pad" is a writer obligation "whose violation this specification expressly
declares not to be a file-conformance violation" — it "binds the actor" while
"the predicate binds the bytes". → **no**

**Answer: yes, no**

---

## Underdetermined questions

None. Every question resolved to a single reading with a decisive sentence. I
looked hardest for ambiguity at Q05 (whether F1's front-block instance reaches
a foreign major — §21.2's preamble settles it by name), Q07(c) (whether the
sub-record placement changes the cannot-establish ground — [R-CNF-11] states
the ground over "a record", not a top-level record, and §21.6 distinguishes
placement only for the *reader's* outcome), Q13(2) (whether [R-CNT-26]'s floor
of 0 or [R-WRT-06]'s "at least the input's" governs — [R-WRT-06] is the
special rule and its premise is satisfied), and Q15 (whether "conforming" and
"a conforming writer could produce it" come apart — [R-CNF-02] says in terms
that they do, and names this as one of exactly two such cases).
