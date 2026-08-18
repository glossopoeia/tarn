# Cleanroom round 10 — quiz key transcript

## Disclosure

Files read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only, in full
(3,919 lines), via `sed -n` ranges, plus one `awk` pass and one `grep` pass over that
same file. No ADRs, no `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md` / `AGENTS.md` / `README.md`, no git history, no web access, no directory
listings. Local computation: two Python scripts I authored in the scratchpad
(`crc.py`, `chk.py`) implementing CRC-32C and the geometry arithmetic; `chk.py` reads
`crc.py`, both of which I wrote myself in this session. No other file was read.

CRC implementation validated against three constants the document itself states
before being used for any answer:
- CRC-32C("123456789") = 0xE3069283 ✓ (§4.5 check vector)
- CRC-32C(zero bytes) = 0x00000000 ✓ (§4.5)
- CRC-32C(2^16 sentinel entries) = 0xEECB3BB2 ✓ (§15.4, `[R-IDX-05]`)
- and, as an end-to-end check of the trailer layout, Appendix A's trailer CRC
  0xE00938D2 reproduced exactly from the layout table of §6.2.

---

## Q01 — final 16 bytes of a 320-byte file

F = 320, so the trailer occupies [256, 320) (§6.2: "The trailer occupies the final 64
bytes of the file"). The final 16 file bytes are trailer bytes [48, 64): file_id
(offset 48, u64), reserved (offset 56, 4 bytes), trailer CRC (offset 60, u32).

Trailer bytes [0, 60) assembled from §6.2's layout table (all little-endian,
`[R-ENC-01]`):

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                     version_major = 1
03 00                     version_minor = 3
00 00 01 00               flags = 0x00010000
04 00 00 00 00 00 00 00   generation = 4
10 00 00 00 00 00 00 00   dir_offset = 16
54 00 00 00 00 00 00 00   dir_length = 84
40 01 00 00 00 00 00 00   committed_file_length = 320
ff 00 ff 00 ff 00 ff 00   file_id = 0x00FF00FF00FF00FF
00 00 00 00               reserved
```

§6.2: "| 60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes [0, 60) |".
Computed: 0x1F74BD23, stored little-endian as `23 bd 74 1f`.

Consistency of the stated file: F mod 64 = 0 (320 = 5·64) ✓; dir_offset 16 ≥ 16 ✓;
dir_length 84 ≥ 4 ✓; 16 + 84 = 100 ≤ F − 64 = 256 ✓; flags 0x00010000 sets only
bit 16, an ignore-lane bit, which §6.3 makes conforming.

**Answer:** `ff 00 ff 00 ff 00 ff 00 00 00 00 00 23 bd 74 1f`

---

## Q02 — planar bool tile image

Planar, C = 1 bool channel, fill byte 0x01 = true (§13.2: bool fill is `0x00` (false)
or `0x01` (true)). d = 2, E = (3, 2), T = (3, 3), linearization 1.

G₀ = ⌈3/3⌉ = 1, G₁ = ⌈2/3⌉ = 1, N = 1, P = ∏Tᵢ = 9. entry_count = C·N = 1.

Planar bool ⇒ §14.3 packed plane: decoded size ⌈P/8⌉ = ⌈9/8⌉ = 2 bytes.

In-tile ordinal (§11.4): k = u₀·T₁ + u₁ = 3u₀ + u₁. Positions with u₁ = 2 have
coordinate x₁ = 2 ≥ E₁ = 2, so they are padding positions (§11.3). `[R-SER-05]`:
"at every padding position, a writer MUST encode, for each channel the position
carries, that channel's fill value — … the fill bit in a packed plane. Every pad bit
(§14.3) MUST carry the plane's channel's fill bit."

| k | (u₀,u₁) | in extents? | bit |
|---|---|---|---|
| 0 | (0,0) | yes | 0 (false) |
| 1 | (0,1) | yes | 0 |
| 2 | (0,2) | padding | 1 (fill=true) |
| 3 | (1,0) | yes | 0 |
| 4 | (1,1) | yes | 0 |
| 5 | (1,2) | padding | 1 |
| 6 | (2,0) | yes | 0 |
| 7 | (2,1) | yes | 0 |
| 8 | (2,2) | padding | 1 |

LSB-first packing (§14.3: "value k occupies bit k mod 8 of byte k div 8"):
byte 0 = bits {2,5} set = 0x04 + 0x20 = 0x24.
byte 1 = bit 0 (k=8) set = 0x01; P mod 8 = 1, so pad bits are positions 1–7, each
carrying the fill bit 1 → 0xFE. Byte 1 = 0x01 | 0xFE = 0xFF.

**Answer:** `24 ff`

---

## Q03 — interleaved decoded size and bytes 6–8

Interleaved, d = 2, E = (2, 2), T = (2, 3). Channels: a uint8 (B=1, fill 0x07),
b int16 (B=2, fill `fe ff`).

P = ∏Tᵢ = 6. Q = ΣBᵢ = 1 + 2 = 3. §14.2: interleaved decoded size = P · Q = 18.

Byte 6 begins in-tile ordinal u = 6/Q = 2 (§14.2's closing note: "channel c's value at
in-tile ordinal u sits at byte u · Q + Fᶜ"). F_a = 0, F_b = 1, so byte 6 = channel a,
bytes 7–8 = channel b.

Ordinal 2 → u₀ = 2 div 3 = 0, u₁ = 2 mod 3 = 2. Coordinate x₁ = 2 ≥ E₁ = 2, so this
is a padding position. `[R-SER-05]` requires each channel's recorded fill there:
a → 0x07; b → `fe ff` (recorded bytes, returned/stored bit-exactly, `[R-TYP-04]`).

**Answer:** 18, then `07 fe ff`

---

## Q04 — planar geometry, five integers

E = (7, 100, 250), T = (4, 32, 64), C = 5, planar, linearization 1, index_encoding 1.

§11.2: G₀ = ⌈7/4⌉ = 2, G₁ = ⌈100/32⌉ = 4, G₂ = ⌈250/64⌉ = 4. N = 2·4·4 = 32.

1. entry_count: planar ⇒ addressed-tile count = C·N = 5·32 = **160** (§11.2,
   `[R-CNT-17]`).
2. `[R-CNT-16]`/`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
   = 160·20 + 1·4 = 3200 + 4 = **3204**.
3. Coordinate (5, 40, 200): tᵢ = xᵢ div Tᵢ = (1, 1, 3). §11.4:
   s = Σ tᵢ · ∏_{j>i} Gⱼ = 1·(4·4) + 1·4 + 3 = 16 + 4 + 3 = 23.
   Planar disk ordinal = c·N + s = 3·32 + 23 = **119**.
4. §15.1: "The entry for the tile with disk ordinal k is the k-th entry, at region
   byte 20·k" ⇒ 20 · 119 = **2380**.
5. uᵢ = xᵢ mod Tᵢ = (1, 8, 8). §11.4: in-tile ordinal = Σ uᵢ · ∏_{j>i} Tⱼ
   = 1·(32·64) + 8·64 + 8 = 2048 + 512 + 8 = **2568**.

**Answer:** 160, 3204, 119, 2380, 2568

---

## Q05 — three sentinel entries

1. entry_count = 3 ⇒ extent_length = 3·20 + ⌈3/2¹⁶⌉·4 = 60 + 4 = **64**.
2. One segment (segment 0 covers entries [0, 3), §15.4). The sentinel entry is
   `FF ×16 00 ×4` (§15.2). `[R-IDX-05]` restricts the 0xEECB3BB2 shortcut to a
   **full** segment: "writers of sparse layers MAY emit this constant for any **full**
   segment — one covering exactly 2¹⁶ entries, final or not — whose entries are all
   sentinels … a partial segment's CRC MUST be computed."
   CRC-32C over the 60 bytes = 0xD171D122, stored little-endian: `22 d1 71 d1`.
3. crc_of_crc_array = CRC-32C over the 4-byte segment-CRC array as stored
   (§7.4, §8.1) = 0x34C74AFB → `34c74afb`.

**Answer:** 64; `22 d1 71 d1`; `34c74afb`

---

## Q06 — two verifier verdicts

File X. Layer B declares linearization = 2. `[R-GEO-05]`: "A reader MUST treat any
linearization value other than 1 as a validity error at layer scope — this includes 0,
all reserved values…". Register row L33. That is an *established* violation.
§2.3, `[R-CNF-11]`: "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements it was
unable to check, and *cannot establish* is available only to a traversal that
established no violation." The zstd inability (layer A) is one of the unchecked
requirements it must report, but it does not change the verdict. ⇒ **nonconforming**.

File Y. `[R-MTA-09]`: "A **verifier** that declines to decode a document cannot
establish that document's conformance and MUST NOT certify the file… the decline is
not a finding that the file is nonconforming and a verifier MUST NOT report it as one.
… it fixes the file's verdict as *cannot establish* only where the verifier
established no violation elsewhere". No violation elsewhere ⇒ **cannot establish**.

**Answer:** nonconforming, cannot establish

---

## Q07 — two ill-formed, byte-identical layer names

§19.1 step 4 is decisive: "A duplicate layer name is a validity error at file scope,
here, at open (`[R-ENC-15]`, §19.2). … Uniqueness is decided first, and over the raw
name bytes whether or not each name is itself well-formed — `[R-ENC-13]` makes name
comparison a byte comparison, which needs no valid name — so two layers whose name
fields are byte-identical are a duplicate even when neither name is valid."

Both name fields lie within inline_length (stipulated), so both are obtainable and
contribute to the namespace. `[R-ENC-15]`: "a duplicate layer name is a file-scope
error (reject-file)".

Register row: F4 — "Two layer records in the live directory carry byte-identical name
fields, both obtainable within their records' inline_length (comparison is raw bytes,
no normalization)". (L3, ill-formed layer-record name / reject-layer, is also
exhibited, but uniqueness is decided first.)

**Answer:** reject-file, F4

---

## Q08 — front-block check obligation

`[R-CNT-04]`: "A reader whose open leaves bytes [0, 16) **resident** — a local file, a
memory mapping, a speculative suffix window that reached offset 0, or any transport
already holding them — and a content sniffer MUST verify the full block by byte
equality before other processing… A reader that would have to issue a further range
request to obtain those bytes MAY defer or omit the check… The test is residency, not
transport."

- Reader 1: memory-mapped local file, 4,096 bytes — bytes [0,16) resident ⇒ **MUST**.
- Reader 2: suffix window [983,040, 1,048,576) of a 1,048,576-byte file — does not
  reach offset 0; bytes [0,16) would need a further request ⇒ **MAY-OMIT**.
- Reader 3: 65,536-byte suffix window over a 40,000-byte file, transport returns the
  whole file — the window reached offset 0 and the reader holds [0,16) ⇒ **MUST**.
  (Appendix A makes the same point on the 128-byte file: "as a remote reader does too
  whenever its speculative suffix window reaches offset 0".)

**Answer:** MUST, MAY-OMIT, MUST

---

## Q09 — recovery probe on a 1,000-byte file

`[R-LIF-06]`: "The probe begins at the largest 64-aligned offset o with
o + 64 ≤ the physical file length"; and "on a match, require the trailer CRC to verify
and committed_file_length = o + 64".

o ≤ 936; largest multiple of 64 that is ≤ 936 is 896 (14·64 = 896; 15·64 = 960 gives
960 + 64 = 1024 > 1000). So o = 896, and the required committed_file_length is
896 + 64 = 960.

**Answer:** 896, 960

---

## Q10 — compactor output trailer

1. version_minor. `[R-WRT-06]`: the output trailer "carries the greater of
   `[R-CNT-26]`'s floor and the input's version_minor — a compactor cannot know which
   minor version defined an ignore-lane bit it does not implement, so it does not
   lower the floor beneath one." Floor for a file expressible under this text = 0
   (`[R-CNT-26]`); input = 5; greater = **5**.
2. generation. `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and
   generation 1". ⇒ **1**.
3. flags. §6.3: "A compactor, though its output is a new file, carries the input's
   unknown ignore-lane bits into its output trailer rather than writing flags = 0."
   The compactor implements no flag bits, so bits 16 and 18 (0x0005 in the high half)
   are both unknown ignore-lane bits and are copied; incompat lane is zero.
   ⇒ **`00050000`**.
4. file_id. `[R-WRT-06]`: "It MUST mint a fresh file_id for the output — a new draw
   under §9.3's randomness advice, not merely a value compared against the input's …
   reusing the input's would break the (file_id, range) cache contract." ⇒ **no**.

**Answer:** 5, 1, `00050000`, no

---

## Q11 — experimental sub-record type 0x8001 with MU = 1

0x8001 ≥ 0x8000 ⇒ experimental range (§10.2's record-type row).

1. `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer — never
   reject-file — and with MU = 0 is ignore-record." ⇒ **reject-layer**.
2. `[R-WRT-06]`: "A compactor MUST refuse to compact a file carrying any record whose
   type it does not implement with MU = 1: such a type can define references this
   specification does not (§7.2), so its bytes cannot be safely relocated." ⇒ **no**.
3. §21.6: "The second is an **experimental-range record type carrying MU = 1** (§10.2,
   §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file
   conforming all the same, since the prohibition on publishing experimental values
   binds a writer's conduct and not the bytes." ⇒ **yes**.
   (Taking the file at its stipulated word that everything else satisfies every
   requirement, so PE = 1 — MU = 1 with PE = 0 would be L46.)

**Answer:** reject-layer, no, yes

---

## Q12 — §21.4 instance total

§21.1's rule: "Instances within a cell are separated by semicolons, and a cell reading
— is one instance; the count is therefore mechanical once the cell is written."
Also: "a row whose check ranges over a family without the condition changing shape
states that range as a single instance (T24's *any codec*)".

Per-row counts (semicolon-split, `—` = 1, "any codec" = 1):

T1 1, T2 1, T3 6, T4 4, T5 1, T6 1, T7 2, T8 1, T9 1, T10 1, T11 2, T12 1, T13 2,
T14 1, T15 2, T16 1, T17 1, T18 4, T19 1, T20 1, T21 1, T22 1, T23 1, T24 1, T25 3,
T26 3.

Sum = **45**.

Cross-check: the same mechanical count over §21.2–§21.5 gives F = 53, L = 106, T = 45,
R = 44, total 248, and 36 + 49 + 26 + 10 = 121 conditions — exactly the figures
`[R-ERR-02]` states: "Every row of §21.2 through §21.5 — 121 conditions over 248
instances". That the whole sums to the document's own published total is strong
evidence the §21.4 share of 45 is the intended reading.

**Answer:** 45

---

## Q13 — the checksum chain above one entry's crc field

§4.5: "Interior checksum fields — each segment CRC array, each tile-index entry's crc
field, and each layer record's crc_of_crc_array — are both comparison-verified and
covered by exactly one further checksum, as §8.1 maps." And: "the terminal checksum
fields of §8.1's map — the trailer, directory-region, and user-metadata checksum
fields — … are verified by comparison and covered by no further checksum."

§8.1's map: tile-index region ← "the per-segment CRC array, itself covered by the
layer record's crc_of_crc_array"; directory region ← "final 4 bytes of the region",
covering "the preceding dir_length − 4 bytes (the raw record sequence)" — which
contains the layer record and hence its crc_of_crc_array field.

Chain, innermost first:
1. **the segment CRC** — the s-th u32 of that layer's tile-index-region segment CRC
   array, for the segment containing that entry (§15.4: it covers "exactly those
   entries' bytes as stored", the entry's 20 bytes including its crc field);
2. **the layer record's `crc_of_crc_array` field** (§7.4, §8.1);
3. **the directory region's terminal CRC** — the final 4 bytes of the directory
   region (§7.1, §8.1). Terminal: covered by no further checksum (§4.5). The trailer
   CRC covers only trailer bytes [0, 60) and does not reach it, so the chain stops
   here.

**Answer:** segment CRC (in the tile-index region's segment CRC array) → the layer
record's crc_of_crc_array field → the directory region's terminal CRC (final 4 bytes
of the directory region; terminal).

---

## Q14 — 448-byte file with wide gaps

1. Conforming? Every stated trailer gate passes; F = 448 = 7·64 is a multiple of 64
   (`[R-CNT-01]`, §6.2); dir_offset 128 ≥ 16; dir_length 4 ≥ 4; 128 + 4 = 132
   ≤ F − 64 = 384; the directory's 4 bytes are the correct CRC over zero preceding
   bytes (§7.1, §4.5 — CRC-32C of zero bytes is 0x00000000), and zero records is a
   valid directory (`[R-CNT-14]`, §21.6 "The file contains zero layers → A conforming
   file with an empty directory"). The 252-byte gap between the directory's end and
   the trailer is the pre-trailer pad, and `[R-CNT-05]` settles it explicitly: "this
   specification does not constrain their content, and bounds their number only
   through step 5 of the commit protocol … **a longer gap is conforming**, and no
   conforming commit produces one. A verifier MUST treat a *structure* in that gap as
   a validity error at file scope" — and no structure lies there. The 112 bytes
   between the front block and the directory are likewise slack (§5.2: "Slack has no
   internal structure this specification defines, its content is unconstrained, and no
   conformance requirement applies to it"). File conformance is a pure predicate on
   bytes (`[R-CNF-02]`), so the fact that no conforming commit *produces* this layout
   does not make the bytes nonconforming. ⇒ **yes**.
2. Slack. §9.7: the walk claims the front block [0, 16), the live directory, the live
   trailer, plus record extents / index regions / stored tiles — of which there are
   none here. Claimed = 16 + 4 + 64 = 84. Slack = 448 − 84 = **364**
   (= 112 + 252). A completed walk reports the total, not a partial (`[R-CNT-21]`).

**Answer:** yes, 364

---

## Q15 — extreme file_id and generation values

§6.2's trailer table: `file_id | u64 | semantic | ≠ 0`; `generation | u64 | semantic |
1 ≤ generation ≤ 2⁶³ − 1 ([R-ENC-03])`.

`[R-ENC-03]` scopes its 2⁶³ − 1 domain to "every offset, length, extent, and count
this specification defines — entry counts and slab run lengths included". file_id is
none of these; it is an identifier (§9.3, §23.2: "a stable 64-bit identifier"). Register
row F2 confirms by enumeration: its Instances cell lists dir_offset; dir_length;
committed_file_length; generation; non-layer top-level record extent_offset;
extent_length — file_id is not among them. Appendix G item 2 further contemplates
file_id drawn from a cryptographic hash, which routinely has bit 63 set.

- **File P**: file_id = 0xFFFFFFFFFFFFFFFF ≠ 0 ✓; generation = 0x7FFFFFFFFFFFFFFF
  = 2⁶³ − 1, the top of the valid range ✓. §9.3's note observes such a file "admits no
  further commit", which is a statement about future commits, not about conformance.
  ⇒ **yes**.
- **File Q**: file_id = 1 ≠ 0 ✓; generation = 0x8000000000000000 = 2⁶³ > 2⁶³ − 1,
  outside `[R-CNT-06]`'s stated range and F2's domain row ⇒ reject-file ⇒ **no**.

**Answer:** yes, no
