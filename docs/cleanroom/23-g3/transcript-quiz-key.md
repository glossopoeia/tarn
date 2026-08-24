# Round 23 — quiz keyer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole file, lines 1–4426, in five `Read` calls). Ran two local Python
scripts in the scratchpad: one computing CRC-32C values and the quiz
arithmetic (reads no files), one that parses the register tables **of that
same permitted spec file** to count Instances cells mechanically. No other
file, no directory listing, no git, no web.

My CRC-32C implementation was validated against three independent check
values the document itself publishes before I used it for anything:
CRC-32C("123456789") = 0xE3069283 (§4.5), CRC-32C(zero bytes) = 0x00000000
(§4.5), and CRC-32C of a full 2^16-entry all-sentinel segment = 0xEECB3BB2
(§15.4). All three reproduced.

The instance-counting script was validated against §21.8's own published
totals: it returned 121 rows over 277 instances, matching
"121 conditions over 277 instances" exactly, with the per-scope split
F 36 rows / 58 instances, L 49 / 116, T 26 / 55, R 10 / 48. The row counts
also match §21.2's "36 conditions", §21.3's "49 conditions", §21.4's
"26 conditions", §21.5's "10 conditions".

**Context I did not ask for.** Before I began, my runtime placed material
in context: a project-instruction pointer (CLAUDE.md → AGENTS.md) and an
index of the maintainer's auto-memory notes with several one-line
descriptions of TARN working practice. I did not open any of it and did not
rely on it. Naming that it appeared, not its contents, per the brief.

---

## Q01 — encoding-2 document, FCS 1048576, decodes to 1048570

The frame is well formed in every respect the question lists except that
its Frame_Content_Size (1048576) does not equal the decoded document's byte
length (1048570).

§18.2 `[R-MTA-09]`: "The frame's content-size field, unlike the decoded
size and the window, is *not* left to the reader: it MAY be present, and
when present it MUST equal the byte length of the decoded document. A
mismatch is one of the frame constraints R4 registers, not a failure to
decode under R3: the bytes decode, and what is wrong is what the header
said about them."

R4's Instances cell confirms the exact instance: "the content-size field
declared larger than the decoded length, top-level extent". The record is
top-level, so that is the instance.

(a) **R4**.

(b) §21.5 heading: "Outcome: ignore-record — the record is skipped as
though absent and decoding of stored data is unaffected." Also
`[R-MTA-09]`'s closing: "Any violation here is ignore-record, never the
tile-scope outcome §17.2 assigns." → **ignore-record**.

(c) §21.5: "Every row here is a violation all the same: the outcome bounds
a reader's blast radius and never makes the file conforming
(`[R-CNF-12]`)." → **nonconforming**.

Sanity checks that no other row fires: document 1048570 B ≈ 1 MiB, under
§21.9's 16 MiB guarantee; members sorted, so no F27; extent CRC verifies,
so no R2; the bytes decode, so no R3.

---

## Q02 — Single_Segment_Flag frame, FCS = decoded length = 12582912

FCS present and equal to the decoded document length (12582912 = 12582912),
so no R4 content-size instance. Magic, single frame, no skippable frame,
Dictionary_ID 0, content-checksum clear, frame occupies the extent before
the terminal CRC, CRC verifies — every carried-over `[R-COD-06]` constraint
§18.2 names is satisfied.

§18.2 removes the window constraint entirely for a document: the frame
constraints apply "save two: what it states against a tile's declared
decoded size, and what it states about the frame's declared `Window_Size`.
This section replaces both". And: "The frame's declared `Window_Size` is
unconstrained here for the same reason ... and no violation: the file
exceeds a §21.9 guarantee and so remains conforming while the reader MAY
decline it (`[R-ERR-04]`)."

(a) **conforming**.

(b) With Single_Segment_Flag set, §18.2 says: "Where the frame sets
Single_Segment_Flag there is no Window_Descriptor and RFC 8878 makes the
frame's `Window_Size` its content-size field, which this section pins below
to the decoded document's byte length: a document larger than that
guarantee, framed that way, exceeds a §21.9 row ... §21.9's user-metadata
row bounds a document's decoded size; it does not relieve the frame
carrying it of the `Window_Size` row."

So Window_Size = 12582912 B = 12 MiB > the 8 MiB guarantee → that row is
exceeded. The document row (16 MiB) is *not* exceeded: 12 MiB < 16 MiB. No
tile exists whose decoded size could exceed 256 MiB (no compressed tile
payload, and in any case that row is about tiles). rank/C/entry_count/
layers/dir_length are all ordinary.

§21.9's table row, verbatim: "| zstd frame `Window_Size` | 8 MiB |".

(b) **zstd frame `Window_Size`** — exactly one row.

---

## Q03 — declined document plus a set reserved flag bit

Item (ii) is a violation the verifier has *established*: §21.2 row F26,
"Any of a non-layer top-level record's reserved flag bits 2-15 is set",
detector verifier, detected at certification, governing `[R-CNT-12]`.
§7.2: "Reserved flag bits: writers MUST emit zero; readers MUST ignore
them. ... a verifier MUST treat a nonzero reserved flag bit ... as a
validity error at the record's governing scope."

Item (i) is a decline, not a violation. The verifier's window bound is
8 MiB (exactly §21.9's guarantee, which is the floor `[R-MTA-09]` permits),
and the frame declares 16 MiB. §18.2: a frame "declaring more than the
reader admits is ignore-record on that ground — the reader's capability,
not a failure to decode within the meaning of R3, and no violation".

(a) §2.3 `[R-CNF-11]`: "An established violation takes priority: a verifier
that has established any violation reports *nonconforming*, however many
requirements it was unable to check, and *cannot establish* is available
only to a traversal that established no violation." → **nonconforming**.

(b) §2.3: "A verifier MUST report each requirement it was unable to check
on a capability or resource ground, naming the requirement and the ground,
whichever of the three verdicts it reports; that per-requirement report
constrains the report and not the verdict". §18.2 confirms the decline is
of that kind: "The decline is one of the unchecked requirements
`[R-CNF-11]` obliges the verifier to report". The window decline "takes the
same treatment" as the size-bound decline, per §18.2's own words, and §2.3
lists "when it declines to decode a user-metadata document (`[R-MTA-09]`)"
among the grounds. → **yes**.

Note the deliberate shape: the "whichever of the three verdicts it reports"
clause is what makes (b) yes even though (a) is nonconforming rather than
cannot-establish.

---

## Q04 — inline encoding byte 0x00 / 0x7F / 0x80

§18.2 `[R-MTA-03]` value set: "0 is invalid; 1 = none and 2 = zstd are
assigned; 3 through 0x7F are reserved; values ≥ 0x80 are the experimental
range (§10)."

- File 1 (0x00): §21.5 row R1 — "A user-metadata record declares a document
  encoding of 0, or a reserved-range value (3-0x7F)". §21.5's preamble:
  "Every row here is a violation all the same". → **nonconforming**.
- File 2 (0x7F = 127): reserved range 3–0x7F → same row R1 →
  **nonconforming**.
- File 3 (0x80 = 128): §21.6, "A user-metadata record declares an
  experimental-range (≥ 0x80) document encoding | Ignored (ignore-record);
  the file is conforming — §10.3's prohibition binds a writer's conduct,
  not the bytes." → **conforming**.

§21.5's preamble also anticipates exactly this boundary: "Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as
violations: what `[R-MTA-10]` withdraws is the document's content rules,
never the encoding byte's own value set".

Answer: **nonconforming, nonconforming, conforming**.

---

## Q05 — instance arithmetic

Counting rule, §21.1: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written."

I applied that literally with a script over the four register tables. It
returned 121 rows / 277 instances, matching §21.8's "121 conditions over
277 instances" — so the rule as I applied it is the rule the document
applied.

(a) R4's cell holds 8 conditions × 2 containers = **16** semicolon-separated
items: missing frame magic; a skippable frame; a second frame; a nonzero
dictionary ID; the content-checksum flag set; bytes remaining after the
frame; content-size declared larger; content-size declared smaller — each
in "top-level extent" and "layer sub-record extent".

(b) R1 4 + R2 2 + R3 2 + R4 16 + R5 8 + R6 4 + R7 6 + R8 2 + R9 2 + R10 2
= **48**.

Arithmetic: 4+2+2 = 8; 8+16 = 24; 24+8 = 32; 32+4 = 36; 36+6 = 42;
42+2+2+2 = 48. Script agrees.

Note two counting subtleties the cells already resolve, so no judgement was
needed: R4's two content-size directions are enumerated because §21.1 says
"Where the condition compares two **magnitudes** either of which can be the
greater ... the two directions are likewise enumerated"; and R8/R9/R10 give
only the two containers, the condition not changing shape within them.

---

## Q06 — empty layer declaring codec 4 at a 2 GiB tile shape

Geometry: G_y = ⌈0/16384⌉ = 0; G_x = ⌈4096/16384⌉ = 1; N = 0·1 = 0.
Interleaved ⇒ addressed-tile count = N = 0. entry_count = 0 ✓ (`[R-CNT-17]`).
extent_length under index_encoding 1 must be 0 when entry_count is 0 ⇒ slot
(0,0) ✓. crc_of_crc_array = 0 when entry_count = 0 ✓ (`[R-CNT-23]`).

§11.1 `[R-GEO-02]`: "A dimension with extent 0 is valid: its grid count is
0, the layer has zero addressed tiles, its tile index has zero entries, and
its reference array is empty. Readers MUST accept such a layer".

Codec 4: P = 16384·16384 = 268,435,456; Q = 8 (one float64); P·Q =
2,147,483,648 = 2 GiB, well above `[R-COD-07]`'s 0x7E000000 = 2,113,929,216.
But §17.2's Note: "The cap is quantified over the layer's *addressed*
tiles, so a layer that addresses none — any dimension extent 0
(`[R-GEO-02]`, §21.6) — satisfies it whatever its tile shape declares, and
codec 4 is conforming there." The row L44 is likewise "Codec 4 (lz4)
declared on a layer any of whose **addressed** tiles' decoded size exceeds
0x7E000000".

`[R-ENC-04]`'s ceiling *is* checked here (same Note: "P·Q and P·Bᶜ are
checked in an empty layer even though this cap is not") — P·Q = 2^31 is far
below 2^63 − 1, so no L2.

(a) **conforming**.

(b) §21.9: "*Decoded size of one tile* ranges over a layer's **addressed**
tiles, stored or not ... A layer addressing no tile (§11.2) therefore has
no tile whose decoded size the table bounds." So the 256 MiB row is not
exceeded, and neither is any other (d = 2 ≤ 32; C = 1 ≤ 4096;
entry_count 0 ≤ 2^32; 1 layer ≤ 65,536; a small directory; no user-metadata
document; no zstd frame).

`[R-ERR-04]`: "Software that declines **on that ground** a file whose every
quantity lies within the table is not a conforming reader (`[R-CNF-03]`)".
→ **no**.

This is the odd-looking answer, and it is what the text says: the layer's
declarations *imply* a 2 GiB tile image, but no tile is addressed, so no
§21.9 quantity is exceeded and the acceptance duty bites.

---

## Q07 — codec 3 → codec 1 with the stored bytes unchanged

§21.7 `[R-ERR-01]`: "a change that reaches the codec is witnessed by the
rows for the codec now declared, which test the stored bytes as a stream of
it (T15, T17, T23, T25), or by T14 where the new declaration is codec 1".

T14 is "Codec 1 (none) declared and a non-sentinel index entry's length
differs from the tile's decoded size" (`[R-COD-04]`).

Answer: **T14**.

---

## Q08 — planar bool tile, byte-shuffle, tile (0,0)

Geometry: T = (2, 5), P = 2·5 = 10. E = (3, 3), so G_y = ⌈3/2⌉ = 2,
G_x = ⌈3/5⌉ = 1. Tile (0,0) covers y ∈ [0,2), x ∈ [0,5); x = 3 and x = 4 are
padding positions (§11.3).

In-tile ordinal (§11.4) = u_y · T_x + u_x = u_y·5 + u_x:

| ord | (u_y,u_x) | value | source |
|---|---|---|---|
| 0 | (0,0) | true | given |
| 1 | (0,1) | false | given |
| 2 | (0,2) | true | given |
| 3 | (0,3) | true | padding → fill 0x01 (`[R-SER-05]`) |
| 4 | (0,4) | true | padding → fill |
| 5 | (1,0) | false | given |
| 6 | (1,1) | true | given |
| 7 | (1,2) | false | given |
| 8 | (1,3) | true | padding → fill |
| 9 | (1,4) | true | padding → fill |

§14.3 `[R-SER-03]`: "value k occupies bit k mod 8 of byte k div 8 (§4.4),
with 0 = false and 1 = true, and the decoded size is ⌈P/8⌉ bytes." ⌈10/8⌉ = 2.

Byte 0 = bits 0..7 = 1,0,1,1,1,0,1,0 → 0x01+0x04+0x08+0x10+0x40 = 0x5D.
Byte 1 = bits 0,1 = 1,1 → 0x03; P mod 8 = 2, so pad bits are positions 2–7,
and §14.5 `[R-SER-05]` fixes each to the plane's fill bit = 1 → 0xFC.
Byte 1 = 0x03 | 0xFC = 0xFF.

Filter 2: `[R-COD-10]` — "for a packed boolean plane s = 1 and the filter is
the identity". Image unchanged.

Codec 1: `[R-COD-04]` — "The stored bytes are the filtered image verbatim."

Answer: **5d ff**.

---

## Q09 — interleaved tile (1,1), ordinal 15

Q = ΣB = 1 (bool m) + 8 (float64 v) + 2 (uint16 q) = 11. P = 4·4 = 16.
Decoded size = P·Q = 176.

§14.2's closing example states the form directly: "channel c's value at
in-tile ordinal u sits at byte u · Q + Fᶜ". F_q = B_m + B_v = 1 + 8 = 9.

(a) 15·11 + 9 = 165 + 9 = **174**.

(b) Ordinal 15 → u_y = 15 div 4 = 3, u_x = 15 mod 4 = 3. Tile coords (1,1),
T = (4,4), so real coordinates are y = 4·1 + 3 = 7, x = 7. Extents are
(5,5), so both are ≥ E: this is a padding position (§11.3).

§14.5 `[R-SER-05]`: "at every padding position, a writer MUST encode, for
each channel the position carries, that channel's fill value — the recorded
fill bytes for a numeric channel, the recorded fill byte for an interleaved
bool channel".

Sample occupies bytes [165, 176): m at 165, v at 166–173, q at 174–175.

Answer: **01 00 00 00 00 00 00 f8 3f cd ab** (11 bytes).

---

## Q10 — entry_count 131072, all sentinel

(a) `[R-CNT-17]`: "extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4".
131072·20 = 2,621,440; ⌈131072/65536⌉ = 2; 2·4 = 8.
→ **2621448**.

(b) 131072 = 2 × 65536, so both segments are *full* and both are entirely
sentinels. §15.4 `[R-IDX-05]`: "The CRC-32C of a segment consisting of 2¹⁶
sentinel entries is `0xEECB3BB2`". I recomputed it from the sentinel bytes
(§15.2, `FF ×16 00 ×4`) and got 0xEECB3BB2, confirming both my CRC routine
and the constant.

The segment CRC array is two little-endian u32s (`[R-ENC-09]`):
`b2 3b cb ee b2 3b cb ee`. crc_of_crc_array = CRC-32C over that 8-byte
array (§7.4, §8.1) = 0xD7926B78, stored little-endian.

→ **78 6b 92 d7**.

---

## Q11 — 200-byte file with a valid-looking trailer at [64, 128)

§19.1 step 1 obtains the transport-authoritative F = 200 (`[R-CNT-10]`;
"MUST NOT substitute the trailer's committed_file_length for the transport
size"). Step 2 fetches bytes [F − 64, F) = [136, 200), which are all 0x00.

§9.5 `[R-LIF-05]`: "a reader that finds no valid trailer in the final 64
bytes MUST report the file torn or invalid and MUST NOT scan backward." So
the trailer at [64, 128) is never consulted.

§6.2's order: "A reader MUST validate, in order: the trailer magic; the
trailer CRC; the version gate ... Any failure is reject-file."

First check failed: the 8 bytes at F − 64 are not the trailer magic.

(a) **reject-file**.
(b) F8 — "The 8 bytes at F-64 are not exactly the trailer magic
8A 4E 52 41 54 0D 0A 1A", reader, open, `[R-CNT-06]`. Not F1, whose
trailer-magic instance requires the constant "stored byte-reversed"
(zeros are not); F1 is a strict specialization of F8 per §21.1, and this
file exhibits only the general row. Not F17 (committed_file_length vs
transport size) or F5, both of which sit later in §6.2's order than the
magic. → **F8**.

§9.5's own Note names exactly this: "A reader meets it as a trailer that
fails its gates — the magic, the CRC, or committed_file_length against the
transport size, each of which §21.2 already registers."

---

## Q12 — slab run packing with a mixed set of entry defects

S = 4, interleaved ⇒ a single block [0, 8) (§16.2 `[R-SLB-02]`), so run 0 is
ordinals [0, 4) — entries 0, 1, 2, 3.

Entry classification (§15.3, `[R-IDX-03]`):
- Entry 0: stored, well formed. offset 8192, length 300.
- Entry 1: offset = length = S with crc ≠ 0 → row "offset = S ∧ length = S ∧
  crc ≠ 0 | *structural*: reject-tile" (register row T6). §16.2: "So are the
  entries §15.3 classifies reject-tile on a *structural* ground: they
  address no usable extent, and the run's stored tiles close over them." →
  **transparent**.
- Entry 2: crc mismatch only. §16.2: "An entry whose only defect is that its
  stored bytes fail its crc is not transparent — its offset and length
  stand, and the packing relation reads them as it does any other stored
  tile's." → **participates**.
- Entry 3: stored, well formed → participates.

§16.2 `[R-SLB-03]`: "the run's stored tiles are contiguous and packed in
ordinal order — each stored tile's offset equals the previous stored tile's
offset plus its length — and the first stored tile's offset satisfies
offset mod A_slab = 0."

First stored tile: 8192 mod 4096 = 0 ✓ (already satisfied, nothing to solve).
X = 8192 + 300 = 8492.
Y = 8492 + 100 = 8592.

Answer: **X = 8492, Y = 8592**.

(The trap is entry 1: had it been treated as a stored tile the chain would
break, and had entry 2 been treated as transparent, Y would be 8492.)

---

## Q13 — slack total

§9.7 `[R-LIF-08]` names the claimants: the directory, each record's extent,
the stored extent of each non-sentinel index entry, plus the front block
[0,16) and the live trailer [F−64, F).

| Claimant | Range | Bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| layer A's stored tile (entry 0) | [16, 116) | 100 |
| layer A's extent = its index region | [128, 152) | 24 |
| layer B's extent = its index region | [160, 204) | 44 |
| user-metadata record extent | [256, 320) | 64 |
| directory region | [384, 896) | 512 |
| live trailer | [960, 1024) | 64 |

Cross-checks: `[R-CNT-17]` for A, 1·20 + ⌈1/2¹⁶⌉·4 = 24 ✓; for B,
2·20 + 1·4 = 44 ✓. §9.7: "A layer record's extent slot addresses that
layer's tile-index region (§7.4), so the region enters the walk once, as
that record's extent, and is not a second claimant beside it."

Layer B's entry 0 is a sentinel — no extent. Entry 1 is offset = length =
all-ones with crc = 5 → structural reject-tile, and §9.7: "an entry
`[R-IDX-03]` classifies reject-tile on a *structural* ground contributes no
stored extent to the walk". So B contributes no stored-tile bytes.

Claimed = 16 + 100 + 24 + 44 + 64 + 512 + 64 = 824.
Slack = F − claimed = 1024 − 824 = **200**.

Residual check: [116,128) = 12, [152,160) = 8, [204,256) = 52, [320,384) =
64, [896,960) = 64 → 12+8+52+64+64 = 200 ✓. (The last of these is the
pre-trailer pad; no structure sits there, so no F7.)

(b) §9.7's closing sentence is decisive: "An entry `[R-IDX-03]` classifies
reject-tile on a *structural* ground does not make the walk incomplete: the
walk passes over it, and the bytes it nominally addresses fall to slack
(§15.3)." No scope-level rejection ended an enumeration (no layer is
rejected), and the verifier did not elect to stop early. §5.2's two
triggers for a partial total are therefore both absent. → **complete**.

---

## Q14 — layer record sizes

(a) inline_length, from §7.4's payload table (fields "packed in table order
with no alignment or padding between them"):

| Field | Bytes |
|---|---|
| name `grid` (u8 len + 4) | 5 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| A u64 | 8 |
| S u64 | 8 |
| A_slab u64 | 8 |
| rank d u8 | 1 |
| channel count C u16 | 2 |
| 2 dimension entries, each (1+1) + 8 + 8 = 18 | 36 |
| channel r uint8: (1+1) + 2 + (1+1) | 6 |
| channel g uint16: (1+1) + 2 + (1+2) | 7 |
| channel b float32: (1+1) + 2 + (1+4) | 9 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |

5 + 34 (the nine scalars) + 36 + 22 + 13 = **110**.

Calibrated against §7.4's worked example, which decomposes its 81-byte
payload as "4 + 34 bytes, the dimension entry 18, the channel entry 12, and
the trailing fixed fields 13". My 34 / 18 / 13 match; the channel entries
differ only by fill length, which `[R-CNT-23]` ties to the element size:
uint8 → 1, uint16 → 2, float32 → 4.

No sub-records, so nothing follows.

(b) Layout 2 = planar. G_y = ⌈10/4⌉ = 3, G_x = ⌈10/4⌉ = 3, N = 9. §11.2
`[R-GEO-03]`: the addressed-tile count "is N for an interleaved layer and
C · N for a planar layer". C = 3 → entry_count = 27.

`[R-CNT-17]`: 27·20 + ⌈27/65536⌉·4 = 540 + 4 = **544**.

---

## Q15 — two layer records with identical ill-formed names

Two violations are present: F4 (byte-identical layer name fields) and L3
(a layer record's name bytes are not well-formed UTF-8), the latter twice.

§19.1 step 4 settles the ordering explicitly: "A duplicate layer name is a
validity error at file scope, here, at open (`[R-ENC-15]`, §19.2). ...
Uniqueness is decided first, and over the raw name bytes whether or not
each name is itself well-formed — `[R-ENC-13]` makes name comparison a byte
comparison, which needs no valid name — so two layers whose name fields are
byte-identical are a duplicate even when neither name is valid."

F4's own condition text confirms the fit: "Two layer records in the live
directory carry byte-identical name fields, both obtainable within their
records' inline_length (comparison is raw bytes, no normalization)" —
reader, open, `[R-ENC-15]` (R-ENC-13). The payloads lie wholly within
inline_length, so both names are obtainable.

(a) §21.2 heading: "Outcome: reject-file." Also `[R-ENC-15]`: "a duplicate
layer name is a file-scope error (reject-file)". → **reject-file**.
(b) → **F4**.

(L3 is reject-layer and detected at open too, but the open algorithm
requires uniqueness be decided *first*, and F4's file-scope outcome
subsumes it.)

---

## Underdetermination

I found none of the fifteen genuinely underdetermined. The closest calls,
and why each resolved:

- **Q03(b).** §18.2's "A **verifier** that declines to decode a document on
  the bound above" could be read as reaching only the *size* bound, since
  the window paragraph is interposed. But that paragraph says the window
  bound "takes the same treatment", and §2.3's cannot-establish list cites
  `[R-MTA-09]` wholesale ("when it declines to decode a user-metadata
  document"). Under either reading (b) is yes, because §2.3's reporting duty
  runs to "each requirement it was unable to check on a capability or
  resource ground" independently of §18.2's sentence. Resolved.
- **Q03(a).** "a type the specification does not register" leaves reserved
  vs. experimental open. If reserved, F36 is a second violation; either way
  the verdict is nonconforming, so the ambiguity does not reach the answer.
- **Q06(b).** The surprising direction. A reader could plead that a 2 GiB
  implied tile image is a resource it cannot serve. But §21.9 individuates
  the tile row over *addressed* tiles and says in terms that "A layer
  addressing no tile (§11.2) therefore has no tile whose decoded size the
  table bounds", and `[R-ERR-04]` then denies conforming-reader status to
  software declining a file whose every quantity lies within the table.
  Resolved against the intuitive answer.
