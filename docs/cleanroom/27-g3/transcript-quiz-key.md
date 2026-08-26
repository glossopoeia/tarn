# Round 27 — quiz keyer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4549 lines, read in full in six `Read` calls). No other file in the repo was
read, listed, or grepped. No git history, no web access, no ADRs, no
conformance corpus, no `registry.json`.

Local computation: two Python scripts I wrote myself, in the scratchpad, that
read no files —
`/private/tmp/.../scratchpad/calc.py` (CRC-32C table implementation and the
trailer/index CRCs) and `/private/tmp/.../scratchpad/calc2.py` (grid, ordinal,
stride, packing, and slack arithmetic). Both were written from the spec text
alone.

**CRC implementation validated against the document's own check values before
any answer was derived:**

- CRC-32C(`"123456789"`) = `0xE3069283` ✓ (§4.5 check vector)
- CRC-32C(zero bytes) = `0x00000000` ✓ (§4.5)
- Appendix A trailer bytes [0,60) → `0xE00938D2`, stored `D2 38 09 E0` ✓
- §7.4's 80-byte 4-sentinel entry array → `0x80A34955` ✓
- §7.4's crc_of_crc_array over `55 49 A3 80` → `0xC4EE982E` ✓
- §15.4's full all-sentinel segment (2¹⁶ entries) → `0xEECB3BB2` ✓

Six independent check values reproduce, so the CRC answers below are not
guesses.

**Unrequested context.** A project instruction file (`CLAUDE.md` pointing at
`AGENTS.md`) and an index of the maintainer's memory notes appeared in my
context before I began, along with a git status/recent-commit listing naming
this round. None of it is specification text and none of it was used: I did
not open any file it named, and every answer below is derived from
`spec/tarn.md` and arithmetic. The commit subjects visible in that listing
mention §2.2 and a charter's line counts; no slate question turns on either,
and I did not consult them. Disclosed rather than acted on.

**Paths.** The specification was exactly where the brief said it was. Nothing
to report.

---

## Q01 — trailer CRC bytes at [252, 256)

F = committed_file_length = 256, so the live trailer is [F−64, F) = [192, 256)
(§6.2: "The trailer occupies the final 64 bytes of the file"). File offsets
[252, 256) are trailer offsets [60, 64) — the **trailer CRC** field:

> | 60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes [0, 60) |

Every trailer field is fixed by the question or by a writer requirement:

| off | field | value | source |
|---|---|---|---|
| 0 | magic | `8A 4E 52 41 54 0D 0A 1A` | §6.2 table |
| 8 | version_major | 1 | given |
| 10 | version_minor | 0 | given |
| 12 | flags | 0 | `[R-CNT-08]`: "a writer creating a file under this text MUST write flags = 0" |
| 16 | generation | 7 | given |
| 24 | dir_offset | 128 | given |
| 32 | dir_length | 40 | given |
| 40 | committed_file_length | 256 | given |
| 48 | file_id | 0x0F1E2D3C4B5A6978 | given |
| 56 | reserved | zero | §6.2 table, `[R-CNT-06]` |

Bytes [0,60):

```
8a 4e 52 41 54 0d 0a 1a  01 00  00 00  00 00 00 00
07 00 00 00 00 00 00 00  80 00 00 00 00 00 00 00
28 00 00 00 00 00 00 00  00 01 00 00 00 00 00 00
78 69 5a 4b 3c 2d 1e 0f  00 00 00 00
```

(Consistency: dir_offset + dir_length = 168 ≤ F − 64 = 192 ✓; F mod 64 = 0 ✓.)

CRC-32C = `0x03ECF55A`, stored little-endian (`[R-ENC-09]`: "stored as a
little-endian `u32`") → file bytes `5A F5 EC 03`.

**Answer: `5af5ec03`**

---

## Q02 — planar entry_count and total sample-position count

Extents (10, 300, 1000), tile extents (4, 128, 256), planar, C = 3.

§11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉ → G = (⌈10/4⌉, ⌈300/128⌉, ⌈1000/256⌉) = (3, 3, 4).
N = ∏Gᵢ = 36. P = ∏Tᵢ = 4·128·256 = 131,072.

(1) `[R-GEO-03]`: "its **addressed-tile count** — the number of its tile-index
entries (§15) — is N for an interleaved layer and C · N for a planar layer".
`[R-CNT-17]` requires entry_count to equal that count. C·N = 3·36 = **108**.

(2) Same sentence: "and its **total sample-position count** is N · P."
36 · 131,072 = **4,718,592**.

Note the trap: a planar layer has C·N addressed tiles each carrying P
positions, so there are C·N·P *values*. But the document expressly defines
*total sample-position count* as N·P — a position count, not a value count,
consistent with §3.1's "sample — the tuple of one value per channel at one
coordinate". The express definition governs; I do not treat this as
underdetermined.

**Answer: 108, 4718592**

---

## Q03 — planar disk ordinal and entry offset

Extents (600, 400), tile extents (128, 256), rank 2, C = 5, planar,
linearization 1.

G = (⌈600/128⌉, ⌈400/256⌉) = (5, 2). N = 10.

Coordinate (500, 300). §11.4: tᵢ = xᵢ div Tᵢ → t = (500 div 128, 300 div 256)
= (3, 1).

Spatial tile ordinal under linearization 1: s = Σᵢ tᵢ · ∏_{j>i} Gⱼ
= 3·G₁ + 1 = 3·2 + 1 = 7.

Third-declared channel → 0-based channel index c = 2 (§3.1: "a channel's
**index** is its 0-based position in that order").

> "The **disk tile ordinal**, which orders tile-index entries (§15), is s for
> an interleaved layer, and **c · N + s** for a planar layer" `[R-GEO-06]`

disk ordinal = 2·10 + 7 = **27**.

§15.1: "The entry for the tile with disk ordinal k (§11.4) is the k-th entry,
at region byte 20·k." → 20·27 = **540**.

(Cross-check against §11.4's own worked example, which computes 2·32+10 = 74
and §15.4's follow-on giving region bytes [1,480, 1,500) = 20·74 — same
arithmetic.)

**Answer: 27, 540**

---

## Q04 — interleaved decoded size, in-sample offset, planar bool plane

Rank 3, tile extents (3, 5, 2) → P = ∏Tᵢ = 30.
Channels in order: `a` bool (element size 1, §12.1), `b` float64 (8),
`c` uint16 (2).

§14.2: Q = Σ Bᵢ = 1 + 8 + 2 = 11 (the sample stride), Fᶜ = Σ_{j<c} Bⱼ.

(1) Interleaved decoded size = P · Q = 30 · 11 = **330**.

(2) §14.2's closing example states the convenient form: "channel c's value at
in-tile ordinal u sits at byte u · Q + Fᶜ". For `c` (uint16), F = 1 + 8 = 9.
17·11 + 9 = 187 + 9 = **196**.

(Table form: offset of value k = (k div C)·Q + F_{k mod C}, with
k = u·C + c = 17·3 + 2 = 53 → (53 div 3)·11 + F₂ = 17·11 + 9 = 196. Same.)

(3) Planar, channel `a` is bool → §14.3 governs, not §14.2:

> "In a planar tile of a bool channel the decoded tile image is the tile's P
> values bit-packed LSB-first … and the decoded size is ⌈P/8⌉ bytes."

⌈30/8⌉ = **4**.

**Answer: 330, 196, 4**

---

## Q05 — the filtered image handed to the codec

Rank 2, extents (2,2), tile extents (2,2) → P = 4, no padding positions.
Interleaved, C = 2: `a` uint8 (B=1), `b` uint16 (B=2). Q = 3, decoded size
P·Q = 12.

In-tile ordinal (§11.4) = Σ uᵢ ∏_{j>i} Tⱼ = u₀·2 + u₁:
(0,0)→0, (0,1)→1, (1,0)→2, (1,1)→3.

§14.1 interleaved: "value k of the sequence is channel (k mod C)'s value at
in-tile ordinal k div C — each sample's channel values are adjacent, in
declared channel order". So the decoded tile image is, per ordinal, `a`'s byte
then `b`'s two bytes little-endian (`[R-ENC-01]`):

```
u=0: 11 02 01
u=1: 22 04 03
u=2: 33 06 05
u=3: 44 08 07
```

Decoded image = `11 02 01 22 04 03 33 06 05 44 08 07`.

Filter 2 = byte-shuffle. §17.3: "The shuffle stride s is the channel's element
size for a planar tile and the sample stride Q for an interleaved tile." So
s = Q = 3, L = 12, n = L/s = 4 groups.

> "the filtered image places byte i of group j at offset i · n + j — all first
> bytes in image order, then all second bytes, and so on" `[R-COD-10]`

- byte 0 of groups 0–3: `11 22 33 44`
- byte 1 of groups 0–3: `02 04 06 08`
- byte 2 of groups 0–3: `01 03 05 07`

Codec 1 (none) then stores this verbatim (`[R-COD-04]`), but the question asks
for the filter stage's output, which is the above. Inverse-permutation check
performed in Python: restores the decoded image exactly.

**Answer: `11 22 33 44 02 04 06 08 01 03 05 07`**

---

## Q06 — packed planar bool tile image

Rank 2, extents (3, 2), tile extents (3, 3), planar, one bool channel, fill
`true`. G = (⌈3/3⌉, ⌈2/3⌉) = (1, 1), N = 1, C = 1 → one addressed tile ✓.
P = 3·3 = 9. Decoded size ⌈9/8⌉ = 2 bytes (§14.3).

In-tile ordinal = u₀·3 + u₁. E₁ = 2 < T₁ = 3, so every position with u₁ = 2 is
a **padding position** (§11.3: "sample positions whose coordinate along that
axis would be ≥ Eᵢ"): ordinals 2, 5, 8.

`[R-SER-05]`: "at every padding position, a writer MUST encode, for each
channel the position carries, that channel's fill value — … the fill bit in a
packed plane." Fill is true → bit 1.

| ord | (u₀,u₁) | value |
|---|---|---|
| 0 | (0,0) | false → 0 |
| 1 | (0,1) | true → 1 |
| 2 | (0,2) | padding → fill 1 |
| 3 | (1,0) | true → 1 |
| 4 | (1,1) | false → 0 |
| 5 | (1,2) | padding → fill 1 |
| 6 | (2,0) | false → 0 |
| 7 | (2,1) | true → 1 |
| 8 | (2,2) | padding → fill 1 |

§14.3: "value k occupies bit k mod 8 of byte k div 8".

Byte 0 (bits 0–7 = ordinals 0–7): 2 + 4 + 8 + 32 + 128 = 174 = `0xAE`.

Byte 1: bit 0 = ordinal 8 = 1. P mod 8 = 1 ≠ 0, so bit positions 1 through 7
are **pad bits**, and `[R-SER-05]`: "Every pad bit (§14.3) MUST carry the
plane's channel's fill bit" = 1. Byte 1 = `0xFF`.

(Structurally identical to §14.3's own example, where fill true gave `55 FD`.)

**Answer: `AE FF`**

---

## Q07 — crc_of_crc_array for three unstored tiles

entry_count = 3, index_encoding 1, none stored → three sentinel entries, each
the 20 bytes `FF ×16 00 ×4` (§15.2, `[R-IDX-02]`).

Region (§15.1) = entry array 3×20 = 60 bytes, then segment CRC array
⌈3/2¹⁶⌉ × 4 = 4 bytes.

Segment 0 covers entries [0, min(2¹⁶, 3)) = [0, 3) — a **partial** segment.
`[R-IDX-05]` limits the `0xEECB3BB2` shortcut to a *full* segment: "writers of
sparse layers MAY emit this constant for any **full** segment — one covering
exactly 2¹⁶ entries, final or not — whose entries are all sentinels, without
computing it — a partial segment's CRC MUST be computed." And §15.4: "the
final partial segment's CRC covers only its actual bytes."

CRC-32C over the 60 bytes = `0xD171D122`, stored `22 D1 71 D1`.

§7.4: crc_of_crc_array = "CRC-32C over the index's segment-CRC array (§15)".
CRC-32C over those 4 bytes = `0x34C74AFB`, stored little-endian
`FB 4A C7 34`.

(Method validated: the identical two-step over §7.4's 4-entry example
reproduces `0x80A34955` and `0xC4EE982E` exactly.)

**Answer: `fb4ac734`**

---

## Q08 — growing a zero extent under codec 4

Before: extents (1000, 0). §11.1/§11.2: an extent of 0 gives grid count 0, so
N = 0 and the layer addresses no tile. §17.2's Note makes the pre-commit file
conforming despite codec 4:

> "The cap is quantified over the layer's *addressed* tiles, so a layer that
> addresses none — any dimension extent 0 … — satisfies it whatever its tile
> shape declares, and codec 4 is conforming there."

After: extents (1000, 1). G = (⌈1000/65536⌉, ⌈1/65536⌉) = (1, 1), N = 1,
one addressed tile. Interleaved, one float64 channel → Q = 8,
P = 65536·65536 = 2³², decoded size P·Q = 2³⁵ = 34,359,738,368 bytes.

Cap: `[R-COD-07]` — "Writers MUST NOT declare this codec for a layer any of
whose addressed tiles' decoded size exceeds 0x7E000000 bytes … and a reader
MUST treat such a declaration as a validity error at layer scope, checkable
from declarations alone."

2³⁵ ≫ 0x7E000000 = 2,113,929,216. The same Note names exactly this transition:
"The escape ends exactly when the layer's addressed-tile count rises above 0".
§20.3 step 4 permits the growth only "provided the grown geometry stays within
every bound the layer's own declarations impose, `[R-COD-07]`'s lz4
decoded-size cap among them (L44)" — so the commit produces a file exhibiting
register row L44.

Outcome class (§2.4): validity error at layer scope → **reject-layer**.

Detection point: L44's *Detected* cell reads **layer access**, and §19.3
lists "the codec declaration bounds (`[R-COD-07]`)" among the checks that MUST
precede first access to the layer. §19.2's tier is "at first access to a
layer", which §21.1 names "layer access".

(Nothing fires earlier: P·Q = 2³⁵ is far below `[R-ENC-04]`'s 2⁶³−1 ceiling,
and entry_count/extent_length stay consistent at 1 and 24. The 256 MiB
decoded-tile row of §21.9 is a *minimum guarantee*, not a cap, so exceeding it
is not a violation — `[R-ERR-04]`'s optional resource decline is not a §2.4
outcome class.)

**Answer: reject-layer, layer access**

---

## Q09 — experimental encoding plus a failed extent CRC

Record: top-level user-metadata, inline_length 1 ✓ (`[R-MTA-03]`), encoding
byte 0x80 = experimental range (§10.2: metadata encoding experimental ≥ 0x80),
extent_length 200 ≥ 5 ✓, wholly inside [16, F−64) ✓, no overlap ✓, terminal
4 bytes ≠ CRC-32C of the preceding 196.

(1) **Reader outcome.** Two independent routes, both ignore-record:

- The unassigned encoding: §21.6 — "A user-metadata record declares an
  experimental-range (≥ 0x80) document encoding → Ignored (ignore-record); the
  file is conforming".
- The failed extent CRC: `[R-CNT-20]` — "a user-metadata extent's CRC →
  ignore-record"; register row R2. `[R-CNT-25]`'s quarantine puts it there
  "notwithstanding the owning-scope mapping of `[R-CNF-08]`".

→ **ignore-record**.

(2) **Verifier verdict.** The CRC failure is a *violation*, not a
non-violation. §21.5's preamble: "Every row here is a violation all the same:
the outcome bounds a reader's blast radius and never makes the file
conforming". And `[R-MTA-10]` is explicit that the terminal CRC survives the
withdrawal of the content rules at an unassigned encoding:

> "file conformance … is decided by the structural checks that precede the
> document alone: the record's framing and extent slot (`[R-CNT-13]`), the
> encoding byte's own value set (`[R-MTA-03]`), and the extent's terminal CRC
> (`[R-CNT-20]`)."

So this is an established violation. `[R-CNF-11]`: "An established violation
takes priority: a verifier that has established any violation reports
*nonconforming*". The experimental encoding is expressly *not* a
cannot-establish ground ("A verifier meeting such a record in an otherwise
conforming file has no requirement it is unable to check").

→ **nonconforming**.

**Answer: ignore-record, nonconforming**

---

## Q10 — a major-4 file with nonzero trailer reserved bytes

The four bytes at trailer offsets [56, 60) holding `01 00 00 00` is exactly
register row F15 ("The 4 reserved bytes at trailer offset 56 are not all
zero"). The question is whether that row *reaches* a file declaring
version_major = 4.

`[R-CNF-13]` fixes the test: a condition reaches a foreign-major file "when,
and only when, the invariant it violates is one `[R-CNT-24]` fixes in every
format major version." §21.2 does the derivation and names the answer set:

> "Deriving it there yields F8, F14, F6 and both of F1's instances — each
> asserting an invariant `[R-CNT-24]` fixes in every major — and no other row."

And §2.3's Note settles F15 by name:

> "F15 does not reach although its Governing rule cell cites `[R-CNT-24]`: the
> trailer bytes it requires be zero are inside the 48 that rule lets a future
> major redefine."

All four reaching rows are satisfied by hypothesis: front block correct (F6,
F1), trailer magic correct at F−64 = 4032 (F8, F1), trailer CRC correctly
covers [0,60) (F14). So **no violation is established**:

> "Every other condition this specification names is one of a structure this
> text defines for format major 1 alone; it is not assessed against a file
> declaring another major, no violation of it is established there, and no §21
> row restating it records such a file." `[R-CNF-13]`

The verifier implements only major 1, which §2.3 lists as a
capability ground: "*cannot establish* — the last where some requirement is one
it is unable to check on a capability or resource ground, as when the file
names a format major version it does not implement". With no established
violation, that verdict is available: "*cannot establish* is available only to
a traversal that established no violation."

**Answer: cannot establish**

---

## Q11 — the slack total

F = 4096. §9.7 names the claimants a coverage walk reaches, plus the two
members claimed as part of the live committed state:

| claimant | bytes | range |
|---|---|---|
| front signature block | 16 | [0, 16) |
| stored tile 1 | 300 | [16, 316) |
| stored tile 2 | 300 | [316, 616) |
| tile-index region (the layer record's extent) | 84 | [1024, 1108) |
| user-metadata sub-record extent | 60 | [2000, 2060) |
| directory region | 100 | [3900, 4000) |
| live trailer | 64 | [4032, 4096) |

Two rules keep the layer record itself out of the tally:

> "A record is not a claimant of its own — its header and inline payload lie
> inside the directory region, which is the claimant covering them … A layer
> record's extent slot addresses that layer's tile-index region (§7.4), so the
> region enters the walk once, as that record's extent, and is not a second
> claimant beside it." `[R-LIF-08]`

And the front block and trailer *are* claimed: "The front signature block at
[0, 16) and the live trailer at [F − 64, F) are claimed by the walk as well,
being members of the live committed state".

Claimed = 16 + 300 + 300 + 84 + 60 + 100 + 64 = 924.
Slack = 4096 − 924 = **3172**.

The walk completes, so this is the exact total, not a partial one
(`[R-CNT-21]`): "a verifier that reaches a live state MUST report the total
number of slack bytes". The 32 bytes of pre-trailer pad at [4000, 4032) are
included in it, per §5.2's list ("alignment and slab gaps, the pre-trailer pad,
and everything an earlier commit superseded").

Sanity: 84 = 4·20 + 4 is a well-formed index region for entry_count 4
(`[R-CNT-17]`); the directory ends at 4000 ≤ F − 64 = 4032 ✓; no ranges
overlap ✓.

**Answer: 3172**

---

## Q12 — which MU = 0 / PE = 0 records may be dropped

§20.4's table, MU = 0 / PE = 0 row (stored flags authoritative, since the
appender implements neither type — "For a type the updater does not implement,
the stored flags are authoritative"):

> "An appender MUST NOT drop it except in a commit that *independently*
> changes the scope the record attaches to: for a layer sub-record, that
> layer's record, the entry set of its index, or which of its tiles are
> stored; for a top-level record, the file's layer set, any layer record's
> content, or another *non-layer* top-level record."

**(a) the top-level record.** The commit supersedes a stored tile of layer X.
The table answers this case by name:

> "Superseding a stored tile's bytes re-places that layer's index region (§20.3,
> `[R-WRT-04]`), moving its extent slot (§7.4) and so modifying that layer's
> record, which is such a change: an appender superseding a tile MAY drop a
> top-level such record, or such a sub-record of the layer whose tile it
> superseded".

Layer X's record content changes, which is the "any layer record's content"
trigger for a top-level record. → **yes**.

**(b) the sub-record of layer Y.** The qualifying changes for a layer
sub-record are confined to *that* layer: "that layer's record, the entry set of
its index, or which of its tiles are stored". Nothing about layer Y changes —
§20.4 obliges Y's record to be re-emitted byte-identically (`[R-WRT-05]`), so
its content is unchanged. The permission the table grants is explicitly "such
a sub-record of **the layer whose tile it superseded**" — layer X, not Y.
→ **no**.

**Answer: yes, no**

---

## Q13 — layer record inline_length and index_encoding offset

Fields packed in §7.4 table order, "with no alignment or padding between them"
(`[R-CNT-18]`). Running offsets from the first byte of the inline payload:

| offset | bytes | field |
|---|---|---|
| 0 | 5 | name: `04` + `grid` |
| 5 | 1 | layout 2 |
| 6 | 2 | linearization 1 |
| 8 | 2 | codec 1 |
| 10 | 2 | filter 1 |
| 12 | 8 | alignment A = 4096 |
| 20 | 8 | slab S = 0 |
| 28 | 8 | slab alignment A_slab = 0 |
| 36 | 1 | rank d = 2 |
| 37 | 2 | channel count C = 2 |
| 39 | 20 | dim `row`: `03`+3 name bytes + 8 + 8 |
| 59 | 20 | dim `col`: same |
| 79 | 9 | channel `mask`: `04`+4 name + type u16 + fill (`01` + 1 byte) |
| 88 | 11 | channel `val`: `03`+3 name + type u16 + fill (`04` + 4 bytes) |
| **99** | 1 | **index_encoding** |
| 100 | 8 | entry_count |
| 108 | 4 | crc_of_crc_array |
| 112 | — | end; no sub-records |

Fill lengths come from `[R-CNT-23]`: "fill length equals the type's element
size" — bool 1, float32 4 (§12.1 table).

Cross-check against §7.4's own accounting of its 81-byte example: "Name and the
nine scalars from layout through channel count occupy 4 + 34 bytes, the
dimension entry 18, the channel entry 12, and the trailing fixed fields 13".
Here the nine scalars are the same 34 (1+2+2+2+8+8+8+1+2), the trailing fixed
fields the same 13 (1+8+4), and a 3-byte dimension name gives 20 rather than 18.

inline_length = **112**; index_encoding at byte **99**.

(A = 4096 with S = 0 is permitted — `[R-CNT-16]` bars only both nonzero — and
A_slab = 0 is required when S = 0, `[R-CNT-23]`. Entry_count would be
⌈1000/256⌉² = 16 for a planar single-... — irrelevant here, the field's width is
what matters.)

**Answer: 112, 99**

---

## Q14 — where the first structure begins under Appendix G

Appendix G item 3 fixes both order and origin:

> "For each layer in ascending layer-name byte order: its stored tiles in
> disk-ordinal order, then its tile-index region; then any remaining record
> extents in ascending record order … The first structure begins at 16,
> directly after the front signature block, which §5.2 counts as no structure —
> or, where a declared alignment admits no structure at 16, at the least
> position above it the declaration admits".

The layer stores at least one tile, and stored tiles precede the index region,
so the first structure is a stored tile. §16.1: "When declared: every stored
tile's offset satisfies offset mod A = 0", with A = 4096.

16 mod 4096 ≠ 0, so 16 is not admissible. The least multiple of 4096 above 16
is 4096.

(Item 5 permits a fixed declared alignment — "No declared alignment and no
slab, **or fixed declared values**" — so A = 4096 is inside the profile.)

**Answer: 4096**

---

## Q15 — index region geometry at entry_count 200,000

§15.1 / `[R-CNT-17]`: region = entry array (entry_count × 20) followed by
segment CRC array (⌈entry_count / 2¹⁶⌉ × 4), "with no padding anywhere inside
the region".

⌈200,000 / 65,536⌉ = 4 (3 full segments + one partial of 200,000 − 196,608 =
3,392 entries).

(1) 200,000 × 20 + 4 × 4 = 4,000,000 + 16 = **4,000,016**.

(2) The CRC array begins immediately after the entry array → region byte
**4,000,000**.

(3) §15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)); the
s-th u32 of the segment CRC array is the CRC-32C over exactly those entries'
bytes". Disk ordinal 131,072 = 2 · 2¹⁶, so it is the first entry of segment
s = 2. Its CRC is the 2-nd u32 (0-based) of the array:
4,000,000 + 2·4 = **4,000,008**.

(Method cross-checked against §15.4's own example at entry_count 1,000,000:
16 segments, 64-byte array, region 20,000,064 — the same three formulas.)

**Answer: 4000016, 4000000, 4000008**

---

## Underdetermined questions

None of the fifteen. Each turns on an expressly stated rule, table, or
constant, and in five cases (Q01, Q03, Q07, Q13, Q15) the document supplies a
structurally identical worked example whose numbers my method reproduces.

The two places where I looked hardest for a second reading, and why each
closed:

- **Q02(2)** — "total sample-position count" could plausibly mean the number of
  channel values (C·N·P = 14,155,776) rather than positions. §11.2 defines the
  term expressly as N·P in the same sentence that distinguishes it from the
  addressed-tile count's C·N, and §3.1 makes a sample a tuple of one value per
  channel at *one* position. Express definition governs.
- **Q10** — one could read F15's nonzero reserved bytes as establishing a
  violation regardless of major. §2.3's Note forecloses it by naming F15 as the
  worked counter-example, and §21.2 states the reaching set exhaustively.
