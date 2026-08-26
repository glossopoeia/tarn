# Cleanroom round 27 — quiz answerer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4549 lines, 275,410 bytes; read in full in five contiguous `Read` calls, plus
one `grep -n '^#'` over the same file for a heading index, and one `wc`).

Ran local computation only: a Python CRC-32C implementation and integer
arithmetic in a scratch file I wrote myself
(`.../scratchpad/round27/calc.py`), reading no project files.

No `docs/`, no ADRs, no `conformance/`, no `spec/registry.json`, no
`PLAN.md` / `AGENTS.md` / `README.md`, no git history, no directory
listings, no web access. The path in the brief was exactly where the file
was.

**Unrequested context that appeared before I began.** My runtime placed a
project-instruction pointer (`CLAUDE.md` → `AGENTS.md`) and an index of the
maintainer's auto-memory notes into my context, plus an environment/git
preamble showing recent commit subject lines that mention this round and
its artifacts. I did not open any of it and did not use any of it; every
answer below is derived from `spec/tarn.md` alone. Naming it here per the
brief; not repeating its contents.

**CRC implementation validated against the document's own constants**
before use — CRC-32C(`"123456789"`) = 0xE3069283 (§4.5); CRC of a full
all-sentinel segment = 0xEECB3BB2 (§15.4, Appendix B); §7.4's worked
example, 4 sentinel entries → 0x80A34955 and crc_of_crc_array 0xC4EE982E;
Appendix A's trailer CRC 0xE00938D2. All four reproduce exactly.

---

## Q01 — bytes at [252, 256)

F = committed_file_length = 256, so the live trailer is [F−64, F) = [192, 256)
(§6.2: "The trailer occupies the final 64 bytes of the file"). File offsets
[252, 256) are trailer offsets [60, 64) — the **trailer CRC**, "CRC-32C over
trailer bytes [0, 60)" (§6.2 layout table).

The remaining fields, for a conforming creator emitting under this text:
- flags = 0 — §6.3 `[R-CNT-08]`: "a writer creating a file under this text
  MUST write flags = 0".
- reserved [56, 60) = zero — §6.2 layout table, "Valid values: zero".

Trailer bytes [0, 60), little-endian throughout (§4.1 `[R-ENC-01]`):

```
8A 4E 52 41 54 0D 0A 1A   magic
01 00                     version_major = 1
00 00                     version_minor = 0
00 00 00 00               flags = 0
07 00 00 00 00 00 00 00   generation = 7
80 00 00 00 00 00 00 00   dir_offset = 128
28 00 00 00 00 00 00 00   dir_length = 40
00 01 00 00 00 00 00 00   committed_file_length = 256
78 69 5A 4B 3C 2D 1E 0F   file_id = 0x0F1E2D3C4B5A6978
00 00 00 00               reserved
```

CRC-32C = 0x03ECF55A, stored as a little-endian u32 (§4.5 `[R-ENC-09]`):
bytes `5A F5 EC 03`.

**Answer: `5af5ec03`.** Confidence: high.

Sanity: the trailer field values are all inside their stated valid ranges
(dir_offset ≥ 16; dir_length ≥ 4; 128 + 40 = 168 ≤ F − 64 = 192; F mod 64 = 0;
1 ≤ generation; file_id ≠ 0), so this is a trailer a conforming writer could
actually emit.

---

## Q02 — planar, rank 3, C = 3

§11.2 `[R-GEO-03]`: "the **grid count** Gᵢ is the ceiling division ⌈Eᵢ / Tᵢ⌉ …
The layer's **spatial-tile count** is N = ∏ Gᵢ, and its **sample-position
count per tile** is P = ∏ Tᵢ. The layer's **addressed-tile count** — the
number of its tile-index entries (§15) — is N for an interleaved layer and
C · N for a planar layer … and its **total sample-position count** is N · P."

G = (⌈10/4⌉, ⌈300/128⌉, ⌈1000/256⌉) = (3, 3, 4); N = 36.
P = 4 · 128 · 256 = 131,072.

entry_count = C · N = 3 · 36 = **108** (§7.4: entry_count "equals the
addressed-tile count", `[R-CNT-17]`).
Total sample-position count = N · P = 36 · 131,072 = **4,718,592**.

Note the total sample-position count is *not* multiplied by C — the
document defines it as N · P for the layer, and channels are values per
sample position, not additional positions (§3.1 "sample").

**Answer: `108, 4718592`.** Confidence: high.

---

## Q03 — planar, rank 2, C = 5, coordinate (500, 300), channel 3

G = (⌈600/128⌉, ⌈400/256⌉) = (5, 2); N = 10.

§11.4 `[R-GEO-06]`: tile coordinates tᵢ = xᵢ div Tᵢ → t = (500 div 128,
300 div 256) = (3, 1). Spatial tile ordinal under linearization 1:
s = Σ tᵢ · ∏_{j>i} Gⱼ = 3·G₁ + 1 = 3·2 + 1 = 7.

"The **disk tile ordinal** … is s for an interleaved layer, and **c · N + s**
for a planar layer (§14), where c is the channel's index (§3.1) —
channel-major grouping." The third-declared channel has index c = 2 (§3.1:
"a channel's **index** is its 0-based position in that order").

Disk ordinal = 2 · 10 + 7 = **27**.

§15.1 `[R-IDX-01]`: "The entry for the tile with disk ordinal k (§11.4) is
the k-th entry, at region byte 20·k." → 20 · 27 = **540**.

**Answer: `27, 540`.** Confidence: high.

---

## Q04 — interleaved, rank 3, tile extents (3, 5, 2)

P = 3 · 5 · 2 = 30. Element sizes (§12.1): bool 1, float64 8, uint16 2.
Sample stride Q = Σ Bᵢ = 1 + 8 + 2 = 11; in-sample offsets F_a = 0, F_b = 1,
F_c = 9.

§14.2 `[R-SER-02]` table: interleaved decoded size = P · Q = 30 · 11 = **330**;
offset of value k = (k div C) · Q + F_{k mod C}, and the section's closing
sentence gives the convenient form: "channel c's value at in-tile ordinal u
sits at byte u · Q + Fᶜ". For channel `c` at ordinal 17: 17 · 11 + 9 = 187 + 9
= **196**.

Planar, channel `a` of type bool → §14.3 `[R-SER-03]`: "In a planar tile of a
bool channel the decoded tile image is the tile's P values bit-packed
LSB-first … the decoded size is ⌈P/8⌉ bytes." ⌈30/8⌉ = **4**.

**Answer: `330, 196, 4`.** Confidence: high.

---

## Q05 — filter output of a 2×2 interleaved tile

P = 4, C = 2, B_a = 1 (uint8), B_b = 2 (uint16), Q = 3, decoded size 12.

In-tile ordinals (§11.4, row-major "for every linearization value,
permanently"): u = u₀ · T₁ + u₁ → (0,0)→0, (0,1)→1, (1,0)→2, (1,1)→3.

Value sequence (§14.1 `[R-SER-01]`, interleaved): "value k of the sequence is
channel (k mod C)'s value at in-tile ordinal k div C — each sample's channel
values are adjacent, in declared channel order".

Decoded tile image (little-endian u16 for `b`):
`11 02 01 22 04 03 33 06 05 44 08 07`.

Filter 2 = byte-shuffle. §17.3 `[R-COD-10]`: "The shuffle stride s is the
channel's element size for a planar tile and the sample stride Q for an
interleaved tile" → s = 3; L = 12, n = L/s = 4. "the filtered image places
byte i of group j at offset i · n + j".

Groups: (11 02 01), (22 04 03), (33 06 05), (44 08 07).
i = 0 → 11 22 33 44; i = 1 → 02 04 06 08; i = 2 → 01 03 05 07.

Codec 1 (none) is what receives this, and "The stored bytes are the filtered
image verbatim" (`[R-COD-04]`) — so this is also the stored tile.

**Answer: `11 22 33 44 02 04 06 08 01 03 05 07`.** Confidence: high.

---

## Q06 — packed planar bool tile, fill true

Extents (3, 2), tile extents (3, 3) → G = (⌈3/3⌉, ⌈2/3⌉) = (1, 1), N = 1,
one channel planar → 1 addressed tile. P = 9.

Padding positions (§11.3 `[R-GEO-04]`): dimension 1 has E₁ = 2 < T₁ = 3, so
in-tile positions with u₁ = 2 lie outside the extents. In-tile ordinal
u = u₀ · 3 + u₁:

| ordinal | position | value |
|---|---|---|
| 0 | (0,0) | false |
| 1 | (0,1) | true |
| 2 | (0,2) | **padding → fill = true** |
| 3 | (1,0) | true |
| 4 | (1,1) | false |
| 5 | (1,2) | **padding → true** |
| 6 | (2,0) | false |
| 7 | (2,1) | true |
| 8 | (2,2) | **padding → true** |

§14.5 `[R-SER-05]`: "at every padding position, a writer MUST encode, for
each channel the position carries, that channel's fill value — … the fill bit
in a packed plane. Every pad bit (§14.3) MUST carry the plane's channel's
fill bit."

§14.3 `[R-SER-03]`: "value k occupies bit k mod 8 of byte k div 8 (§4.4),
with 0 = false and 1 = true, and the decoded size is ⌈P/8⌉ bytes." ⌈9/8⌉ = 2.

Byte 0, bits 0–7 = values 0–7 = 0,1,1,1,0,1,0,1 → 2+4+8+32+128 = 174 = 0xAE.
Byte 1, bit 0 = value 8 = 1; bits 1–7 are pad bits (P mod 8 = 1, so positions
1 through 7), each the fill bit = 1 → 0xFF.

**Answer: `AE FF`.** Confidence: high.
(Cross-check against §14.3's own worked example: P = 10, alternating from
true, fill true → `55 FD` — same packing and same pad-bit rule.)

---

## Q07 — crc_of_crc_array for entry_count 3, all unstored

§15.2 `[R-IDX-02]`: sentinel entry is "the 20 bytes `FF ×16 00 ×4`". Three
unstored addressed tiles → 60 bytes of entry array.

§15.1: region = [entry array: entry_count × 20] [segment CRC array:
⌈entry_count / 2¹⁶⌉ × 4] → one segment, one 4-byte CRC.

§15.4 `[R-IDX-04]`: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶,
entry_count)); the s-th u32 of the segment CRC array is the CRC-32C over
exactly those entries' bytes as stored — the final partial segment's CRC
covers only its actual bytes." Segment 0 covers entries [0, 3) = 60 bytes.

`[R-IDX-05]` bars using the 0xEECB3BB2 constant here: it licenses that
constant only "for any **full** segment — one covering exactly 2¹⁶ entries …
a partial segment's CRC MUST be computed."

CRC-32C(60 sentinel bytes) = 0xD171D122 → segment CRC array = `22 D1 71 D1`.

§7.4: crc_of_crc_array is "CRC-32C over the index's segment-CRC array (§15)".
CRC-32C(`22 D1 71 D1`) = 0x34C74AFB → stored little-endian `FB 4A C7 34`.

**Answer: `fb4ac734`.** Confidence: high.

---

## Q08 — extent 0 → 1 under codec 4

Before: E = (1000, 0). ⌈0/65536⌉ = 0, so N = 0 and the layer addresses no
tile (§11.1 `[R-GEO-02]`, §11.2). §17.2's Note: "The cap is quantified over
the layer's *addressed* tiles, so a layer that addresses none … satisfies it
whatever its tile shape declares, and codec 4 is conforming there."

After: E = (1000, 1). G = (1, 1), N = 1, entry_count 1, P = 65536 · 65536 =
2³² = 4,294,967,296. One float64 channel interleaved → Q = 8, decoded size
P · Q = 2³⁵ = 34,359,738,368 bytes.

`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes … and a reader MUST
treat such a declaration as a validity error at layer scope, checkable from
declarations alone." 0x7E000000 = 2,113,929,216 < 2³⁵.

§20.3 step 4 confirms this is exactly the trap it names: a layer storing no
tile "MAY be re-declared freely … and an extent MAY **grow** … provided the
grown geometry stays within every bound the layer's own declarations impose,
`[R-COD-07]`'s lz4 decoded-size cap among them (L44), which an empty layer
escapes only because that cap is quantified over addressed tiles."

Register row L44 (§21.3): outcome **reject-layer**, detector reader, detected
at **layer access**. §19.3 `[R-RDR-03]` puts "the codec declaration bounds
(`[R-COD-07]`)" in the layer-access validation set, "decidable from the
resident directory and F: layer access performs no fetch".

Other candidates checked and rejected: `[R-ENC-04]`'s 2⁶³ − 1 ceiling is not
breached (2³⁵ ≪ 2⁶³); entry_count 1 matches N (no L21/L22 if the region is
re-emitted as obliged); §21.9's 256 MiB tile guarantee is a minimum
guarantee, not a validity cap (`[R-ERR-04]`: "A file exceeding any of these
remains conforming"), so it is not the answer.

**Answer: `reject-layer, layer access`.** Confidence: high.

---

## Q09 — experimental encoding 0x80 with a bad extent CRC

Encoding byte 0x80 is in the experimental range (§10.2 table: metadata
encoding, experimental ≥ 0x80).

(1) The reader's outcome for the record. §7.1 `[R-CNT-25]`: "each way a
user-metadata record's document can be unreadable once its framing has been
read — a failed extent CRC, an unimplemented or invalid encoding, … — is
ignore-record with a SHOULD-report, notwithstanding the owning-scope mapping
of `[R-CNF-08]`." §8.2 `[R-CNT-20]`: "a user-metadata extent's CRC →
ignore-record". §10.3 `[R-EXT-03]` routes the experimental encoding value the
same way. Both grounds converge: **ignore-record**.

(2) The verifier's verdict. `[R-MTA-10]` withdraws only the *document*
content rules at an unassigned encoding, and names what still decides
conformance: "file conformance — a pure predicate on bytes (`[R-CNF-02]`) —
is decided by the structural checks that precede the document alone: the
record's framing and extent slot (`[R-CNT-13]`), the encoding byte's own
value set (`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)."

The extent's terminal CRC fails. That is §21.5 row R2 — "A user-metadata
extent's final 4 bytes do not equal the CRC-32C of the preceding bytes",
governing rule `[R-CNT-20]` (R-CNT-25), detector reader, detected at extent
use — with no encoding qualifier on its instances. §21.5's preamble: "Every
row here is a violation all the same: the outcome bounds a reader's blast
radius and never makes the file conforming (`[R-CNF-12]`)."

§2.3: "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*." So the §21.6 row that
makes an experimental encoding a non-violation does not rescue this file: it
concerns the encoding value only.

Arithmetic check on the framing: extent_length 200 ≥ 5 (so no F22), the slot
is nonzero and inside [16, F − 64) (no F21/F30/F31/F32), inline_length is 1
(no F23). The CRC covers "the preceding bytes" = the first 196 of the 200,
which is what the question negates.

**Answer: `ignore-record, nonconforming`.** Confidence: high.

---

## Q10 — version_major 4, nonzero trailer reserved bytes

The stated conditions: front block correct; trailer magic at F − 64 = 4032
correct (F = 4096, 4096 − 64 = 4032 ✓); trailer CRC over [0, 60) correct;
version_major = 4; trailer bytes [56, 60) = `01 00 00 00` (the reserved
field, nonzero → the condition §21.2 F15 names); nothing else.

`[R-CNF-13]` (§2.3) decides which conditions reach a file declaring another
major: a condition "**reaches** a file declaring a format major other than 1
when, and only when, the invariant it violates is one `[R-CNT-24]` fixes in
every format major version." §21.2's preamble derives the list: "Deriving it
there yields F8, F14, F6 and both of F1's instances … and no other row."

F15 is expressly excluded. §2.3's Note: "F15 does not reach although its
Governing rule cell cites `[R-CNT-24]`: the trailer bytes it requires be zero
are inside the 48 that rule lets a future major redefine."

So of the reaching rows: F6 (front block) passes, F1 (byte-reversed
signature constants) does not apply, F8 (trailer magic) passes, F14 (trailer
CRC) passes. No violation is established. F18 does not apply — version_major
is 4, not 0.

`[R-CNF-13]`: "Every other condition this specification names is one of a
structure this text defines for format major 1 alone; it is not assessed
against a file declaring another major, no violation of it is established
there".

§2.3 on the verdicts: "*cannot establish* — the last where some requirement
is one it is unable to check on a capability or resource ground, as when the
file names a format major version it does not implement… *cannot establish*
is available only to a traversal that established no violation."

**Answer: `cannot establish`.** Confidence: high.

---

## Q11 — slack total

§9.7 `[R-LIF-08]` and §5.2 `[R-CNT-02]`: the claimants are the front block,
the live trailer, the directory region, each record's extent, and each
non-sentinel entry's stored extent. "A record is not a claimant of its own —
its header and inline payload lie inside the directory region"; and "A layer
record's extent slot addresses that layer's tile-index region (§7.4), so the
region enters the walk once, as that record's extent, and is not a second
claimant beside it."

Claimants:

| Structure | Range | Bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored tile 1 | [16, 316) | 300 |
| stored tile 2 | [316, 616) | 300 |
| tile-index region (the layer record's extent) | [1024, 1108) | 84 |
| user-metadata sub-record extent | [2000, 2060) | 60 |
| directory region | [3900, 4000) | 100 |
| live trailer | [4032, 4096) | 64 |

All disjoint; total claimed = 924. The layer record itself and the
sub-record's header/inline payload lie inside the directory region and are
not separate claims.

§5.2 `[R-CNT-21]`: "Every byte the live state does not claim is **slack**"
and "a verifier that reaches a live state MUST report the total number of
slack bytes". The walk completes, so the total is exact, not partial.

Slack = 4096 − 924 = **3172** (this includes the 32-byte pre-trailer pad
[4000, 4032), which §5.2 names as slack explicitly).

**Answer: `3172`.** Confidence: high.

---

## Q12 — dropping MU = 0 / PE = 0 records

§20.4's table, MU = 0, PE = 0 row: "Retain byte-identical, or drop it — its
extent becoming slack. An appender MUST NOT drop it except in a commit that
*independently* changes the scope the record attaches to: for a layer
sub-record, that layer's record, the entry set of its index, or which of its
tiles are stored; for a top-level record, the file's layer set, any layer
record's content, or another *non-layer* top-level record. … Superseding a
stored tile's bytes re-places that layer's index region (§20.3,
`[R-WRT-04]`), moving its extent slot (§7.4) and so modifying that layer's
record, which is such a change: an appender superseding a tile MAY drop a
top-level such record, or such a sub-record of the layer whose tile it
superseded".

(a) Top-level record: the commit supersedes a tile of layer X, which
re-places X's index region and so modifies X's layer record — "any layer
record's content" changed. The sentence licenses it in terms:
"an appender superseding a tile MAY drop a top-level such record." → **yes**.

(b) Sub-record of layer **Y**: the licensing change for a layer sub-record
must be to *that* layer — Y's record, Y's index entry set, or which of Y's
tiles are stored. The commit touches only layer X; Y's record is re-emitted
byte-identically under `[R-WRT-05]`. The text's own gloss confines the
permission to "such a sub-record of the layer whose tile it superseded" —
X, not Y. → **no**.

That the appender implements neither type does not change the analysis:
§20.4 says for an unimplemented type "the stored flags are authoritative",
which is exactly the MU = 0 / PE = 0 row applied above.

**Answer: `yes, no`.** Confidence: high.

---

## Q13 — inline_length and index_encoding offset

§7.4's field order and widths, with §7.4's own worked example as the check
("Name and the nine scalars from layout through channel count occupy 4 + 34
bytes, the dimension entry 18, the channel entry 12, and the trailing fixed
fields 13 — 81 exactly"):

| Field | Bytes | Running |
|---|---|---|
| name `grid` (u8 len + 4) | 5 | 5 |
| layout (u8) | 1 | 6 |
| linearization (u16) | 2 | 8 |
| codec (u16) | 2 | 10 |
| filter (u16) | 2 | 12 |
| alignment A (u64) | 8 | 20 |
| slab S (u64) | 8 | 28 |
| A_slab (u64) | 8 | 36 |
| rank d (u8) | 1 | 37 |
| channel count C (u16) | 2 | 39 |
| dim `row`: 1+3 name + 8 + 8 | 20 | 59 |
| dim `col`: 1+3 name + 8 + 8 | 20 | 79 |
| chan `mask`: 1+4 name + 2 type + 1+1 fill (bool, element size 1) | 9 | 88 |
| chan `val`: 1+3 name + 2 type + 1+4 fill (float32, element size 4) | 11 | 99 |
| index_encoding (u8) | 1 | 100 |
| entry_count (u64) | 8 | 108 |
| crc_of_crc_array (u32) | 4 | 112 |

§7.4 `[R-CNT-18]`: "fields are packed in table order with no alignment or
padding between them"; §7.4 channel-entry row: "fill length equals the
type's element size (`[R-CNT-23]`)". Element sizes from §12.1: bool 1,
float32 4. No sub-records → no residue.

inline_length = **112**; index_encoding lies at payload offset **99**.

(A = 4096 with S = 0 is legal and mutually consistent — `[R-CNT-16]` bars
only A ≠ 0 together with S ≠ 0, and A_slab = 0 is forced by S = 0.)

**Answer: `112, 99`.** Confidence: high.

---

## Q14 — first structure offset under Appendix G

Appendix G item 3 fixes the emission order: "For each layer in ascending
layer-name byte order: its stored tiles in disk-ordinal order, then its
tile-index region; then any remaining record extents in ascending record
order … then the directory." With at least one tile stored, the first
structure is a **stored tile** of the one layer.

Same item: "The first structure begins at 16, directly after the front
signature block, which §5.2 counts as no structure — or, where a declared
alignment admits no structure at 16, at the least position above it the
declaration admits".

The layer declares A = 4096. §16.1 `[R-SLB-01]`: "When declared: every stored
tile's offset satisfies offset mod A = 0." 16 mod 4096 ≠ 0, so the
declaration admits no structure at 16. The least multiple of 4096 above 16
is **4096**.

**Answer: `4096`.** Confidence: high, with the one hinge named: the profile's
fixed order is what makes the first structure a stored tile (and hence
alignment-bound) rather than the index region, which A does not constrain.

---

## Q15 — index region of 200,000 entries

§15.1: region = [entry array: entry_count × 20] [segment CRC array:
⌈entry_count / 2¹⁶⌉ × 4], "with no padding anywhere inside the region";
§7.4 `[R-CNT-17]` states the same length formula.

- entry array = 200,000 × 20 = 4,000,000
- segments = ⌈200,000 / 65,536⌉ = 4 → CRC array = 16 bytes
- (1) total region length = 4,000,000 + 16 = **4,000,016**
- (2) segment CRC array begins at region offset **4,000,000**

(3) §15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count));
the s-th u32 of the segment CRC array is the CRC-32C over exactly those
entries' bytes". Disk ordinal 131,072 → s = 131,072 div 65,536 = 2 (segment 2
covers [131,072, 196,608)). Its CRC is the 3rd u32: 4,000,000 + 2 × 4 =
**4,000,008**.

**Answer: `4000016, 4000000, 4000008`.** Confidence: high.

---

## Underdetermination review

I looked deliberately for slate items the text leaves open and found none I
would call underdetermined. The nearest three, and why each resolves:

- **Q02(2)** — "total sample-position count" could be misread as including
  channels. §11.2 defines the term expressly as N · P, and defines the
  channel multiplier only for the *addressed-tile* count. Determined.
- **Q09** — §21.6's "experimental encoding → the file is conforming" row
  and §21.5's R2 pull in opposite directions on first reading.
  `[R-MTA-10]` resolves it explicitly by naming the extent's terminal CRC
  among the checks that still decide conformance. Determined.
- **Q14** — turns on whether Appendix G's alignment escape-hatch applies,
  which depends on the profile's fixed emission order putting a stored tile
  first. Item 3 states both halves. Determined — though Appendix G is
  non-normative, which is why the question asks what a writer "adopting the
  profile" does rather than what conformance requires; I answered on the
  profile's own terms.
