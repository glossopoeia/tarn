# Round 20 — Writer implementer walk

**Access.** I read exactly one file, `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,369 lines), plus `grep`/`awk` over that same file and local Python I wrote
myself in a scratch directory. No `docs/`, no ADRs, no `conformance/`, no
`registry.json`, no git history, no web. My runtime did place material in my
context before I began — a project instruction file and an index of the
maintainer's notes naming this round's position and prior work. I have
disregarded it and do not repeat its contents; nothing below derives from it.

I built a conforming writer and updater on paper *and* in Python: an actual
128-byte-minimum check, an actual multi-layer file, two appends, and a
compaction, all with real CRC-32C arithmetic and a real reader that walks the
result. Where the document decided something, I say so; where I had to guess,
I say so.

---

## 0. Calibrating the checksum before anything else

§4.5 gives a check vector, and §4.5/§15.4/§7.4/Appendix A give four more
constants. My CRC-32C (reflected, poly 0x82F63B78 reflected form, init
0xFFFFFFFF, final XOR 0xFFFFFFFF) reproduces all five:

| Input | Document | Mine |
|---|---|---|
| `"123456789"` | `0xE3069283` (§4.5) | `0xe3069283` |
| zero bytes | `0x00000000` (§4.5) | `0x0` |
| 4 sentinel entries (80 bytes) | `0x80A34955` (§7.4 example) | `0x80a34955` |
| the 4-byte array `55 49 A3 80` | `0xC4EE982E` (§7.4 example) | `0xc4ee982e` |
| 2¹⁶ sentinel entries | `0xEECB3BB2` (§15.4, Appendix B) | `0xeecb3bb2` |

I then rebuilt Appendix A's minimal file's trailer from §6.2's layout table
alone and got `0xE00938D2` — Appendix A's stored `D2 38 09 E0`. That single
result confirms field order, widths, offsets and endianness of the trailer
without my having to trust my reading of the table. **§6.2 fixed every byte of
the trailer for me; nothing there was my choice except `file_id` and
`version_minor`.**

I also verified the register's own bookkeeping mechanically: parsing §21.2–§21.5
gives 36 + 49 + 26 + 10 = **121 rows** and, counting semicolon-separated
instances with a bare `—` counting as one, **273 instances** — exactly what
§21.8 claims ("121 conditions over 273 instances"). No discrepancy.

And I checked every worked numeric example in §11.2, §11.4, §14.2, §14.3,
§14.5, §15.4 (both), §17.3 and §21.9's note by hand. All correct, including
the byte-shuffle example (`00 00 00 00 00 00 80 00 40 3F 40 40`) and the
1,000,000-entry index arithmetic (16 segments, 15 full, last 16,960 entries,
region 20,000,064 bytes, segment 15 at [19,660,800, 20,000,000)).

---

## 1. Creation: a file, byte by byte

### 1.1 What I chose and what the document chose

I built a two-layer file with a file-scope user-metadata record.

**Layer `alpha`** — rank 2, dims `y` (E=5, T=4) and `x` (E=5, T=4);
interleaved; channels `a` (uint8, fill `00`) and `b` (uint16, fill `CD AB` =
0xABCD); codec 1, filter 1; A = 0, S = 0, A_slab = 0. Grid 2×2, N = 4, P = 16,
Q = 3, decoded size 48. Tiles 0 and 3 stored, 1 and 2 sentinel.

**Layer `mask`** — rank 1, dim `x` (E=10, T=5); planar; one bool channel `m`,
fill `00`. G = 2, N = 2, C = 1, addressed = C·N = 2, P = 5, decoded size
⌈5/8⌉ = 1. Both tiles stored.

Free to me (`[R-CNF-05]`, §11.3's Note, `[R-SLB-05]`): tile extents, layout,
codec, filter, which tiles to store, alignment/slab declarations, structure
order and placement, record order, `file_id`, and slack content.

Fixed by the document: everything else. In particular —

- **§7.4's inline-payload field order**, packed with "no alignment or padding
  between them". I cross-checked my parser against §7.4's worked `sst`
  example: name 4 + nine scalars 34 + one dimension entry 18 + one channel
  entry 12 + trailing 13 = 81 bytes. Exactly as stated. My `alpha` payload is
  102 bytes (5+1 name, 34 scalars, 2×18 dims, 12+13 channels, 13 trailing) and
  `mask`'s is 76.
- **§15.1's region shape**: `entry_count × 20` then `⌈entry_count/2¹⁶⌉ × 4`,
  "with no padding anywhere inside the region", and `[R-CNT-17]`'s
  `extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`. alpha: 4·20+4 =
  84. mask: 2·20+4 = 44.
- **§15.2's sentinel**: `FF ×16 00 ×4`. Not my choice; not `00 ×20`.
- **`[R-SER-05]`'s padding content.** alpha's tile 3 is the edge tile at tile
  coordinates (1,1), covering y,x ∈ [4,8): one real position (4,4) and fifteen
  padding positions. Every one of those fifteen carries `00 CD AB` — channel
  `a`'s fill byte then channel `b`'s fill bytes. This is the single most
  writer-visible content rule in the document and it is unambiguous.
- **`[R-SER-03]`'s pad bits.** mask's planes have P = 5, so bits 5–7 of the
  single decoded byte are pad bits and `[R-SER-05]` fixes them to the
  channel's fill bit — false — so tile 0's decoded byte is `0x15`
  (`T F T F T` in bits 0–4, zeros above), not `0xF5`.
- **`[R-COD-04]`**: codec 1 forces each entry's `length` to equal the decoded
  size. 48, 48, 1, 1.

### 1.2 The emission order and the actual offsets

`[R-LIF-02]`'s creation path: front block, then steps 2–6 "writing beginning at
offset 16". `[R-WRT-02]` makes that a MUST for a creator. §5.2 lets me place
structures in any order. I packed contiguously:

```
[0,16)      front signature block          89 54 41 52 4E 0D 0A 1A + 8 zero
[16,64)     alpha tile 0 (48 B)            10 00 00 01 01 10 02 02 10 ...
[64,112)    alpha tile 3 (48 B)            77 02 01 | 00 CD AB × 15
[112,113)   mask tile 0 (1 B)              15
[113,114)   mask tile 1 (1 B)              0C
[114,198)   alpha index region (84 B)      4 entries + 1 segment CRC 7D5B184A
[198,242)   mask  index region (44 B)      2 entries + 1 segment CRC 627EEF84
[242,267)   user-metadata extent (25 B)    {"tarn.title":"demo"} + CRC 1273F874
[267,522)   directory region (255 B)       recA(126) recB(100) recM(25) + CRC
[522,576)   pre-trailer pad (54 B, zero)   slack
[576,640)   trailer (64 B)                 gen 1, F = 640
```

alpha's entry array, verbatim from the file at 0x0072:

```
0072  10 00 00 00 00 00 00 00  30 00 00 00 00 00 00 00  4E CD 04 06   entry 0: [16,64) crc 0x0604CD4E
0086  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  00 00 00 00   entry 1: sentinel
009A  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  00 00 00 00   entry 2: sentinel
00AE  40 00 00 00 00 00 00 00  30 00 00 00 00 00 00 00  B4 5C 18 2E   entry 3: [64,112) crc 0x2E185CB4
00C2  4A 18 5B 7D                                                     segment 0 CRC 0x7D5B184A
```

and `crc_of_crc_array` = CRC-32C(`4A 18 5B 7D`) = `0x45805372`, stored in the
layer record's last four bytes.

**F.** dir end = 267 + 255 = 522. `[R-LIF-02]` step 5 pads "to the next 64-byte
boundary" → 576, plus the 64-byte trailer → **F = 640**, a multiple of 64 as
§6.2 requires. Pad = 54 bytes. Nothing here was my choice once I had fixed the
directory's placement: the pad length is a function of the directory's end.

**Trailer.** magic; version_major 1; version_minor 0 (`[R-CNT-26]`'s floor,
a SHOULD); flags 0 (`[R-CNT-08]` makes this a MUST for a creator under this
text — not, as Appendix G item 8 implies, a profile addition); generation 1;
dir_offset 267; dir_length 255; committed_file_length 640; file_id
0xD3A17C5B9E2F4801 (nonzero, and §9.3 SHOULDs a cryptographically random draw);
reserved zero; CRC 0xEB3E24C8.

### 1.3 Reading it back

I wrote an independent reader implementing §19.1's four-step open, §19.3's
layer validation, §15.4's two-link index verification, §15.3's entry
classification, `[R-COD-04]`'s length equality, and §9.7's coverage walk. It
accepts the file. Every CRC verifies; the claimant set partitions; slack = 54
bytes = the pre-trailer pad exactly.

My coverage walk had a bug on the first run: I claimed each layer's index
region twice, once as the layer record's extent and once as "the index region".
§9.7 anticipates precisely this — *"A layer record's extent slot addresses that
layer's tile-index region (§7.4), so the region enters the walk once, as that
record's extent, and is not a second claimant beside it."* That sentence earns
its place; it caught my defect for me.

---

## 2. The append procedure

### 2.1 Generation 2 — a new layer (§20.3's shape (a))

Steps actually executed, in `[R-LIF-02]`/`[R-WRT-04]` order:

1. **Establish F.** Validated the trailer at the physical end: F = 640. Had
   that failed, `[R-LIF-04]` forbids appending and pushes me to §9.6's
   deliberate recovery.
2. **Open.** §19.1's four steps. This gives me the layer-name namespace
   (`alpha`, `mask`) so I can check `[R-ENC-15]` for my new name.
3. **Validate what the commit touches.** `[R-WRT-03]`: *"the trailer and the
   full directory always — re-emission (§20.4) relies on every directory byte
   — plus §19.3's layer validation for every layer whose record, index, or
   extents the commit modifies, and the §19.4 index chain for every segment
   whose entries the commit reuses."* Adding a layer touches no existing
   layer, so I owe framing and names only. I did not have to verify alpha's or
   mask's index chains. This is a genuinely cheap commit and the rule says so.
4. **Write payloads and indexes**, beginning at exactly F = 640:
   beta's two 8-byte tiles at [640,648) and [648,656), beta's 44-byte index at
   [656,700).
5. **Re-emit the directory** at 700: recA, recB, recM **byte-identical**
   (`[R-WRT-05]`), then recBeta, then the CRC. dir_length 358.
6. **Commit**: barrier; pad 30 bytes to 1088; trailer generation 2, *same*
   file_id, flags copied forward (`[R-CNT-08]`), version_minor
   max(floor, prior) = 0 (`[R-CNT-26]`); barrier.

F₂ = 1152. The commit appended 512 bytes and turned 373 bytes to slack: the
gen-1 directory (255), its pad (54) and its trailer (64). My verifier's slack
total after gen 2 is 403 = 373 + the new 30-byte pad. That matches §20.3's
example (a) exactly: *"The slack is the old directory, pad and trailer — sized
by the file's layer count, never by any layer's data."*

beta is a good edge case: dim `i` has E = 3, T = 2, so G = 2 and tile 1 covers
positions 2 and 3, of which 3 is padding. Its stored bytes are
`09 00 00 00 | 00 00 00 00` — the real sample then the int32 fill,
`[R-SER-05]` again.

### 2.2 Generation 3 — superseding a tile (§20.3's shape (b))

I stored alpha's tile 1 (previously sentinel). `[R-WRT-04]` step 4 is explicit
about what this costs:

> Every layer whose stored-tile set or index content this commit changes has
> its tile-index region re-emitted in full — entry_count entries plus the
> segment CRC array — necessarily at a new placement (`[R-LIF-01]`), with
> entries for tiles this commit stores or supersedes written to their new
> state, entries for tiles that become unstored written as the sentinel,
> entries new to this generation (added tiles, grown extents) emitted per §15,
> and every other entry byte-identical at its disk-ordinal position

So: new payload at [1152,1200); alpha's whole 84-byte region re-emitted at
[1200,1284) with entry 1 re-pointed and entries 0, 2, 3 byte-identical;
recomputed segment CRC; recomputed `crc_of_crc_array`; alpha's record re-emitted
with only those two fields changed. dir at 1284, F₃ = 1728, slack 931.

I checked the 931 by hand: 255 + 54 + 64 (gen-1 dir/pad/trailer) + 84 (alpha's
old region) + 358 + 30 + 64 (gen-2 dir/pad/trailer) + 22 (gen-3 pad) = 931. My
verifier agrees. **Nothing here was underdetermined.**

### 2.3 The three shapes and what becomes slack

| Commit shape | Bytes that become slack | Counted by | Permitted content |
|---|---|---|---|
| Add a layer (shape a) | prior directory + its pad + its trailer | verifier, `[R-CNT-21]` | unconstrained; writers SHOULD zero their own gaps (`[R-CNT-03]`) |
| Add/supersede tiles (shape b) | the above + that layer's whole prior index region + every superseded payload | verifier | unconstrained |
| Directory-only edit (shape c) | the above only | verifier | unconstrained |
| Extent shrink (§20.3 step 4) | the above + the de-addressed tiles' extents | verifier | unconstrained |
| Compaction | nothing in the input (it is untouched and persists, §23.1); the *output* has its own alignment gaps and pre-trailer pad | verifier of the output | unconstrained |
| Abandoned partial write | **none, while torn.** `[R-CNT-21]`: *"Where §6.2's ordered validation rejects the file before a live trailer is established there is no F and no live state to walk, so the total is not owed at all."* After the next writer overwrites from F, any of those bytes it does not overwrite and that fall inside the new F are ordinary slack, with stale content. |

Two things the document gets right that I would have got wrong on my own:
the slack total is bounded by **F**, not by the physical length; and a
verifier whose walk does not complete reports a **partial** total that is an
upper bound, naming what stopped it (`[R-CNT-21]`).

### 2.4 Appending to a file whose records I do not all understand

Walking every flag combination §7.2 defines, for a type my updater does not
implement (so `[R-CNT-22]`'s "stored flags are authoritative" applies):

| Stored MU / PE | Placement | What my updater is permitted to do |
|---|---|---|
| 1 / 1 | top-level | **Nothing.** `[R-CNT-15]` makes it reject-file; §20.4: *"At file scope no commit is available at all."* I refuse before touching a byte. Note this can be a *conforming* file (§21.6's second structural case). |
| 1 / 0 | top-level | Identical: `[R-CNT-12]` makes me read it as PE = 1. Separately a verifier-detected violation (F25). |
| 0 / 1 | top-level | Retain byte-identical, extent content unmodified. I may commit anything else. I may **not** relocate its extent: `[R-WRT-08]` allows relocation only "under §20.5", i.e. for a compactor. |
| 0 / 0 | top-level | Retain, **or** drop iff this commit independently changes the file's layer set, any layer record's content, or another non-layer top-level record. Dropping it, or dropping another record in the same commit, does not qualify. SHOULD report the loss. |
| 1 / 1 | sub-record of layer L | Retain byte-identical; MUST NOT modify L; other layers stay editable. Compaction of the whole file is barred (`[R-WRT-06]`, last sentence — it says "any record", so sub-records count). |
| 1 / 0 | sub-record | Same, read as PE = 1. |
| 0 / 1 | sub-record of L | Retain byte-identical, extent unmodified. |
| 0 / 0 | sub-record of L | Retain, or drop iff this commit independently changes L's record, L's index entry set, or which of L's tiles are stored. |
| any, with a reserved bit 2–15 set | either | Retain byte-identical and carry the violation forward (§20.3 step 2: MUST NOT repair). SHOULD report. |

I checked the drop conditions against a case that looked like a loophole:
superseding one tile of layer L re-places L's index region, which moves L's
extent slot, which modifies L's record — so it qualifies as "any layer record's
content" and licenses dropping a top-level PE = 0 record. §20.4 says exactly
that in terms, and then closes the self-reference: *"Dropping the record, or
dropping another record in the same commit, is not itself such a change, so a
commit whose only effect would be the drop MUST retain it."* That is airtight.

**Write order, durability, commit point.** `[R-LIF-02]`: payloads/indexes/extents
(step 2) then the complete directory and its CRC (step 3) must all be durable
(step 4) *before* the pad and trailer are written (step 5), and the trailer
must then be made durable (step 6). §20.2 stresses "both barriers, not one".
The commit point is the moment the new trailer occupies the final 64 bytes of
the physical file: from then on a fresh reader takes it as its snapshot (§9.5).
Everything before that is invisible to a reader on the default path, and
everything after is immutable (`[R-LIF-01]`).

---

## 3. Torn-write recovery — five crash points

| Crash point | What the next reader sees | What the next updater does | Conforming meanwhile? |
|---|---|---|---|
| **(i)** mid step 2 (payloads written, no directory) | Final 64 bytes are payload junk → trailer magic fails (F8), or magic passes by accident and the CRC (F14) or committed_file_length-vs-size (F17) fails. Reports the file torn; `[R-LIF-05]` forbids scanning backward. | `[R-LIF-04]`: MUST NOT append. §9.6's probe from the largest 64-aligned o with o+64 ≤ physical length walks down and finds trailₙ at Fₙ−64 (Fₙ is a multiple of 64, so it is on the probe's grid); requires CRC + committed_file_length = o+64; truncate; re-verify whole. | **No.** F8/F14/F17. |
| **(ii)** after step 3, before step 5 | Identical to (i) — the directory is written but nothing points at it. | Identical. | No. |
| **(iii)** mid step 5, trailer partly written | If the magic landed and the CRC did not, F14. If the write was torn in the middle, F14 again. If the whole 64 bytes landed but *earlier* bytes did not (weak barrier), the trailer validates and the chain fails below — directory CRC (F20) → reject-file, or a segment CRC (L38) → reject-layer, or a tile CRC (T1) → reject-tile. §9.2's Note owns this case: safety degrades from "invisible" to "detected". | Same recovery. | No (or: yes-shaped but with a broken chain, which is still nonconforming). |
| **(iv)** after step 5, before step 6's barrier | Whatever the storage actually persisted. If the trailer is there, this is a completed commit. | Nothing special. | Yes, if the trailer is durable. |
| **(v)** `[R-LIF-04]`'s overwrite path: new trailer written at newF−64 but the physical file not yet truncated from an older, longer length | The physical tail is stale residue, so the reader is at (i) again. §9.5's Note names this exactly: *"What the residue violates is `[R-LIF-04]`'s writer obligation to truncate or overwrite, and the state a reader can observe is already named."* | §9.6's probe finds the new trailer (its committed_file_length = o+64 discriminates it from the older one further down) and truncates. | No — F17. |

I checked the probe's grid arithmetic on my own file: with F = 640 and a
physical length of 700, the largest 64-aligned o with o+64 ≤ 700 is 576 = F−64,
so the probe hits the live trailer on its first candidate. The probe cannot
miss a trailer, because every committed F is a multiple of 64.

Two writer duties I want to record as *not* underdetermined but easy to get
wrong: the trailer at F−64 is on the probe grid **because** F mod 64 = 0, and
`[R-LIF-04]`'s "no later than step 6" truncation is what keeps the next
reader from meeting case (v).

---

## 4. Compaction

I compacted gen 3. Output: fresh file_id 0x5F2E9C31A7B04D68, generation 1,
1728 bytes → **832 bytes**, slack 931 → **35** (the pre-trailer pad alone).
Every stored tile's bytes copied verbatim; every index entry's `crc` and every
sentinel unchanged; entry offsets new; segment CRCs recomputed;
`crc_of_crc_array` updated; the user-metadata extent copied verbatim with its
slot re-pointed. My reader accepts the output and its reference arrays are
identical, as `[R-WRT-07]` requires.

`[R-WRT-09]` obliged me to verify each stored tile's entry crc before emitting
its bytes, which I did in the copy loop. §20.5's paragraph on regenerating a
region is unusually careful and I found it correct: a structurally-rejected
entry gives me *no stored extent to re-point*, so I cannot regenerate the
region without meeting it, and `[R-WRT-06]` then obliges refusal — a tile-index
entry being no record §20.4 licenses dropping.

The newly-tightened sentence bounding a compactor's placement freedom is the
one I leaned on hardest:

> A compactor MUST preserve content, and preserves no placement — placement is
> not among the things it carries forward, and it is free to place structures
> anywhere §5.2 admits and every declared layout invariant permits
> (`[R-SLB-01]`, `[R-SLB-03]`)

I tested it against the case that would otherwise be open: a slab-declared
layer. A compactor *changes* every run's byte placement by construction. It
cannot take `[R-SLB-04]`'s escape hatch of clearing the declaration, because
§20.5 lets it change only the extent slot and `crc_of_crc_array` of a layer
record. So it must re-establish `[R-SLB-03]`'s packing and A_slab alignment in
the output — which is exactly what this clause now says. Same for `[R-SLB-01]`:
under a declared A the compactor must A-align every relocated tile, which can
make the output *larger* than a naive pack, and is conforming. I could not
break it.

I also checked that "so slack is never carried" earlier in §20.5 does not
contradict this: it can only mean the *input's* slack is not carried, since the
output's pre-trailer pad is slack in every file (35 bytes in mine). No defect.

---

## 5. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options. Every
legitimate way their bytes may differ, and whether Appendix G closes it:

| # | Degree of freedom | Where the core leaves it open | Closed by Appendix G? |
|---|---|---|---|
| 1 | Encoder output for codecs 2–4 (including a raw DEFLATE stream's final-byte unused bits, §17.2's Note) | `[R-CNF-05]`; RFC 1951/8878 constrain decoders | **Yes**, item 1, by pinning the implementation, version and settings. Item 1 is honest that byte-identity across *implementations* is unattainable here. |
| 2 | `file_id` | §9.3 (SHOULD random) | **Yes**, item 2 — and item 2 correctly excludes compactors, whose `[R-WRT-06]` fresh draw is no function of content. |
| 3 | Structure placement and order | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **Yes**, item 3. |
| 4 | Gap *extent* | `[R-SLB-05]` | **Yes**, item 3 (contiguous save where alignment forces a gap). |
| 5 | Gap *content* | `[R-CNT-03]` (SHOULD) | **Yes**, item 3 ("every byte of every such gap is zero", advice taken as requirement). |
| 6 | Record and sub-record order in the directory | `[R-CNT-14]` | **Yes**, item 3's ordering key. The `extent_offset`-masking rationale is correct: an unmasked key would be self-referential. |
| 7 | Number of generations | §9 constrains none | **Yes**, item 4. |
| 8 | Declared alignment / slab | §16 leaves both to the writer | **Yes**, item 5. |
| 9 | Filter value | §17.3 leaves it to the writer | **Yes**, item 5. |
| 10 | Whether an all-fill tile is stored or sentinel | no rule either way | **Yes**, item 6. |
| 11 | Fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) | **Yes**, item 7 — and item 7 correctly notes it reaches further than eight bytes, because item 6 makes storedness depend on fill. |
| 12 | `version_minor` | `[R-CNT-26]` (SHOULD) | **Yes**, item 8. |
| 13 | `flags` | — | **Already closed by the core.** `[R-CNT-08]` MUSTs flags = 0 for a creator; `[R-WRT-06]` MUSTs carry-forward for a compactor. Item 8's flags clause adds nothing. G's own closing paragraph knows this: it lists only `version_minor` for item 8. Not a defect, just redundancy. |
| 14 | User-metadata JSON serialization (number formatting, whitespace) and its zstd framing | `[R-MTA-05]` explicitly does not make two writers identical | **Yes**, item 9. |
| 15 | NFC vs. NFD names | `[R-ENC-14]` (SHOULD) | **Yes**, item 10. |
| 16 | Padding-position content, pad bits, interleaved bool bytes | — | **Already mandatory**: `[R-SER-05]`, `[R-SER-08]`. G says so. |
| 17 | **Tile extents** | §11.3's Note: *"Tile extents are a writer's choice, and this specification imposes none"* | **No item pins them.** See finding writer-03. |
| 18 | **Channel layout (interleaved vs. planar)** | §7.4's layout field; `[R-SER-06]` leaves the writer both values; §14.4's Note observes a single-channel bool layer's tiles differ between them | **No item pins it.** See finding writer-03. |

Everything in rows 1–16 I could classify as legitimate-and-closed. Rows 17–18
are legitimate and **not** closed, on the profile's own criterion. That is
finding writer-03.

One divergence I could not classify cleanly as legitimate or forbidden — an
appender relocating a live index region — is finding writer-01.

---

## 6. Findings

### writer-01 — AMBIGUITY. Whether an appender may relocate a live index region turns on an undefined term and a keyword-free clause

**Location.** §20.3 step 4 (`[R-WRT-04]`); §20.4 (`[R-WRT-05]`); §20.5
(`[R-WRT-07]`).

**Quotation.** §20.3 step 4:

> A layer whose record alone changes keeps its extent slot, pointing at the
> existing region, as does a layer the commit leaves untouched (`[R-WRT-05]`);
> relocating a live index region is compaction's operation (§20.5,
> `[R-WRT-07]`), not an appender's.

and §20.4:

> In the new complete directory, an updater MUST re-emit byte-identically —
> header, inline payload, and extent slot — every record it retains and does
> not logically modify, whether or not it implements the record's type; a
> record it modifies is new output under its writer obligations
> (`[R-CNF-05]`). `[R-WRT-05]`

**The problem.** "relocating a live index region is … not an appender's"
carries no BCP 14 keyword. §2.1 binds the keywords "when, and only when, they
appear in all capitals", so on its face this clause has no force of its own.
Whether relocation is nonetheless barred therefore falls entirely to
`[R-WRT-05]`, whose duty is keyed on the phrase **"does not logically
modify"** — a term that appears exactly once in the document (I grepped) and
is nowhere defined.

**The permitted readings.**

*Reading A — re-pointing an extent slot is not a "logical" modification.* Then
`[R-WRT-05]`'s MUST binds an updater that retains a record and merely moves its
extent, and an appender may not relocate an untouched layer's index region.
§20.5's carve-out is evidence for this reading: a compactor needs an express
exception — *"except that relocation re-points extent slots"* — which would be
unnecessary if re-pointing were already a "logical modification" taking the
record outside `[R-WRT-05]`. **But Reading A leaves the case of a layer whose
record the commit *does* logically modify wide open**: rename a layer, change
its fill on a layer that stores no tile, or clear a slab declaration (§20.3's
shape (c) names all three), and `[R-WRT-05]` no longer binds — at which point
nothing with a keyword stops the appender from also re-emitting that layer's
index region at a new placement and leaving the old one as slack.

*Reading B — "logically modify" means any change to the emitted bytes,
re-pointing included.* Then `[R-WRT-05]` never bars relocation for any layer,
§20.5's carve-out is belt-and-braces, and the keyword-free clause is the only
thing standing between an appender and free relocation — which, under §2.1, is
nothing.

**What I picked.** Reading A, plus a conservative extension of the
keyword-free clause: my appender never relocates a live index region, and never
copies a live record extent to a new offset, whatever else it changes about the
record. I picked it because §20.5's example figure and §5.1's example both draw
untouched regions as never moving, and because the conservative choice cannot
produce a nonconforming file.

**What an implementer does wrong without this.** Under Reading B a writer that
renames a layer, or clears its slab declaration, may also re-pack that layer's
index region "while it is there" — a natural optimisation. It emits a
**conforming** file that differs in F, in the layer record's extent slot, and
in ~n·20 bytes of placement from what a Reading-A appender emits for the same
requested change. Nothing in §21 catches it, because a relocated region is
byte-indistinguishable from a freshly emitted one and no single file records
where the region was in the prior generation. §21.7 does not name this
obligation among the ones with no witness, which is itself a signal that it was
not meant to be an obligation.

**Byte-level: no.** Both outputs are conforming files, so no verifier verdict
and no reader's accept/reject changes, and the set of emittable *files* is
unchanged. What changes is which of two conforming files a conforming
*appender* may produce — a conduct question. §2.3 says conduct-only writer
rules are those "expressly declared not to be a file-conformance violation" and
names exactly two ("§6.3's flags = 0 against a set ignore-lane bit and §6.2's
pre-trailer gap"); this clause is not one of them, which is why I think the
clause is descriptive rather than normative and the divergence legitimate.

**Cheapest repair.** Either give the clause its keyword — "an appender MUST NOT
relocate a live index region" — and add it to §21.7's list of obligations with
no single-file witness, or delete it and say plainly that an appender that
modifies a layer record MAY re-place that layer's index region.

---

### writer-02 — AMBIGUITY. §20.3 step 2's "MUST NOT drop the record" reads across §20.4's conditional drop licence

**Location.** §20.3 step 2 (`[R-WRT-04]`); §20.4's preservation table.

**Quotation.** §20.3 step 2:

> Against any other structure the appender carries forward, it MUST NOT repair
> the defect — `[R-LIF-01]` freezes the committed prefix — and MUST NOT drop
> the record (§20.4).

against §20.4's MU = 0 / PE = 0 row:

> Retain byte-identical, or drop it — its extent becoming slack. An appender
> MUST NOT drop it except in a commit that *independently* changes the scope
> the record attaches to…

**The problem.** Set up the case my updater actually met while walking the flag
combinations: a top-level record of a type I do not implement, MU = 0, PE = 0,
carrying a set reserved flag bit (an F26 violation), in a commit that
independently adds a layer. §20.4's row licenses the drop; §20.3 step 2 says
"MUST NOT drop the record".

**The permitted readings.**

*Reading A — the step-2 prohibition is absolute for a record whose defect the
appender has met.* Then I must retain it, and my output is a nonconforming file
(it still carries F26). §20.3 step 2 expressly tolerates that outcome
("Reproducing a structure's bytes unchanged is not authoring them… a violation
latent in a structure it neither modifies nor relies on travels with that
structure"), so Reading A is coherent.

*Reading B — step 2's clause is a pointer, not an independent prohibition:*
its whole subject is "any other structure the appender **carries forward**",
and a record it drops is by definition not carried forward; the parenthetical
"(§20.4)" directs the reader to where dropping is governed, and §20.4's licence
is untouched. Then I may drop it, and my output is **conforming**.

**What I picked.** Reading B, on the strength of the sentence's own subject
("structure the appender carries forward") and the citation. I dropped the
record and reported the loss as §20.4 SHOULDs.

**What an implementer does wrong without this.** The two readings put opposite
verifier verdicts on the same appender's output from the same input and the
same requested change: Reading A yields a nonconforming file, Reading B a
conforming one. An operator running a pipeline that verifies after every
append gets a red light or a green one depending on which reading its updater
took.

**Byte-level: no.** Both bytestreams are ones *some* conforming tool may
produce — the drop is licensed for a compactor unconditionally, and for an
appender under Reading B — so no file moves in or out of the conforming set,
and no reader's accept/reject verdict on a given file changes. The divergence
is again in what a conforming *appender* may emit. I grade it honestly rather
than reaching: the cost to an implementer is a coin-flip on whether its own
output certifies, which is real but is not a fork in the emittable set.

**Cheapest repair.** "…and MUST NOT drop the record except as §20.4 licenses."

---

### writer-03 — AMBIGUITY. Appendix G pins the filter, alignment and slab on an argument that reaches tile extents and channel layout, and pins neither

**Location.** Appendix G, items 1 and 5 and the closing paragraph; §11.3's
Note; §14.1/`[R-SER-06]`.

**Quotation.** Appendix G item 5:

> **A fixed filter value** likewise: §17.3 leaves the choice to the writer, it
> changes the stored bytes of every tile it touches, and no content implies it,
> so two writers agreeing on everything else still disagree on bytes without it
> pinned.

against §11.3's Note:

> Tile extents are a writer's choice, and this specification imposes none

**The problem.** Item 5 states a three-part test for what the profile must
close: the specification leaves the choice to the writer; the choice changes
the stored bytes of every tile it touches; no content implies it. **Tile
extents satisfy all three verbatim** — §11.3 says so in the same words — and so
does **channel layout**, which `[R-SER-06]` leaves the writer as a free choice
between 1 and 2 and which §14.4's Note observes produces different tile images
for a bool channel (⌈P/8⌉ packed planar versus P bytes interleaved). Items 1–10
pin the codec (item 1), the filter, alignment and slab (item 5), the fill
default (item 7), the sentinel policy (item 6), placement and order (item 3),
generation count (item 4), `file_id` (item 2), `version_minor` (item 8),
metadata serialization (item 9) and name normalization (item 10). Neither tile
extents nor layout appears in any item, and neither appears in the closing
paragraph's enumeration of what the items add.

**The permitted readings.**

*Reading A — tiling and layout are part of the caller's input, not writer
choices, so the profile is complete.* Item 2's rationale supports this: *"this
format fixes no canonical serialization of logical content, and two files
carrying the same arrays can legitimately differ in tiling, layout, and
codec."* But that sentence groups **codec** with tiling and layout — and item 1
pins the codec anyway ("Codec 1 (none), or a named codec implementation…"), so
membership in that list plainly does not exempt a choice from being pinned.

*Reading B — the profile's list is incomplete.* Then two writers that adopt
Appendix G in full, given the same arrays, may still emit different files: one
tiles 256×256 interleaved, the other 512×512 planar, both profile-conforming.
The profile's own opening claim — that it "closes the degrees of freedom this
format deliberately leaves open" — is then falsified by its own item-5 test.

**What I picked.** Reading A, but only because I could not make Reading B's
profile useful: I treated tiling, layout, dimension order and channel order as
part of the caller's stated options, so my reproducible writer takes them as
input. I record that this is a guess, and that item 1's treatment of the codec
cuts directly against it.

**What an implementer does wrong without this.** Two vendors both certify
"Appendix G profile" for a content-addressed store and get different digests
for the same arrays, because one of them read "the profile closes the degrees
of freedom this format deliberately leaves open" as covering tiling. The
failure is silent and shows up as a cache miss rate, not as an error. The fix
in the document is one clause: either add tile extents, layout and declaration
order to item 5's list, or state at the head of the appendix that the profile
takes the layer's declarations — geometry, tiling, layout, channel order, codec
and fill — as given input and closes only what remains.

**Byte-level: no.** Appendix G is labelled non-normative and says so of itself:
*"It adds no requirement to any actor: a writer ignoring it is fully
conforming."* Resolving this moves no conforming implementation's emittable
set and changes no accept/reject verdict. It is a defect in a deliverable of
this document, not in the format.

---

## 7. Things I checked that turned out to be fine

Recorded so a later round need not re-walk them.

- **`[R-CNT-18]`'s new scope qualifier** (*"where the file is otherwise
  conforming a reader MUST NOT reject the file for it — on a nonconforming
  file `[R-CNF-12]`'s licence to reject on any detected violation is
  untouched"*) against `[R-CNF-03]`'s exemption clause (*"carrying no record of
  a type it does not implement with MUST_UNDERSTAND = 1"*, which carries no
  top-level qualifier) and §21.6's *"never a ground to refuse the file"*.
  `[R-CNF-03]` only **withdraws an acceptance duty**; `[R-CNT-18]` supplies a
  positive MUST NOT; the two compose, and a reader that declined to serve any
  layer would be performing reject-file under §2.4's definition and so would be
  nonconforming. No fork. And the case I constructed to break it — a
  nonconforming file whose only violation is verifier-detected and which this
  reader does not detect — cannot fork behaviour either, because a reader
  cannot condition on a violation it has not detected.
- **§21.6's "Two structural cases"** against §2.3's three refusal grounds and
  §21.9's *"the two capability refusals §21.6 names… are not this ground"*.
  Consistent: the third ground is `[R-ERR-04]`'s resource limits.
- **§20.5's placement clause** against `[R-SLB-01]`, `[R-SLB-03]`, `[R-SLB-04]`
  and `[R-WRT-05]`. The MUST's scope reaches the "except that" carve-out, so
  re-pointing slots and regenerating regions are inside the requirement, not
  exceptions to it. A compactor cannot take `[R-SLB-04]`'s clear-the-declaration
  escape (it may change only the extent slot and `crc_of_crc_array`), so it must
  re-establish — which this clause now says. Correct.
- **§20.3 step 4's growth and shrink permissions.** I worked growth that raises
  a grid count (ordinals renumber via `[R-GEO-06]`; new entries per §15; the
  slab run partition changes so `[R-SLB-04]` fires), growth that does not
  (existing padding positions become real, and their stored bytes already held
  fill), and shrink (de-addressed tiles' extents become slack; a shrink that
  turns real positions into padding of a prior-generation stored tile is
  barred). All determined. I also worked two cases the text does not name and
  the stem still decides: appending a channel to a **planar** layer with stored
  tiles is permitted (existing planes' disk ordinals c·N+s, decoded sizes and
  padding sets are all unchanged), and removing a middle channel is permitted
  only if the writer moves the surviving entries to their new ordinals so that
  every stored tile still "means exactly what it meant".
- **Every addressed tile has at least one real position**, since
  (Gᵢ−1)·Tᵢ < Eᵢ. So an all-padding tile is unrepresentable and `[R-SER-05]`
  never has to define one.
- **`[R-COD-10]`'s divisibility claim** (*"The decoded image's length L is
  divisible by s in every case"*): planar numeric L = P·B, s = B; interleaved
  L = P·Q, s = Q; packed planar bool s = 1. Holds in all three.
- **§17.2's zstd window note.** A tile below 1 KiB decoded is encodable under
  codec 3 only as a single-segment frame, in which case Window_Size = the frame
  content size = the decoded size, so "exceeding" is false. My 18-byte and
  1-byte tiles would need that; the note says so.
- **§5.1's 128-byte floor**: dir_offset ≥ 16, dir_length ≥ 4, dir end ≤ F−64
  gives F ≥ 84, and F mod 64 = 0 gives F ≥ 128. Correct.
- **§9.6's probe grid**: every committed F is a multiple of 64, so every
  committed trailer starts on the probe's 64-aligned grid. The probe cannot
  step over one.
- **`[R-IDX-05]`'s all-sentinel constant** is only licensed for a *full*
  segment; my 4-entry index needed a computed 0x80A34955, and the document's
  own example uses that value, not 0xEECB3BB2. Consistent.
- **§20.4's preservation table carries no requirement identifier of its own.**
  I looked at whether §2.2's "Normative requirements carry identifiers" makes
  this a defect and concluded it does not rise to one: by the document's
  convention an identifier closes everything since the previous identifier, so
  `[R-WRT-08]` plausibly labels the table, and `[R-CNF-06]` and §2.4 both reach
  it by section. Not reported.
- **Appendix G item 3's "ordered by type" gives no direction.** "ascending
  layer-name byte order" and "ascending record order" two lines earlier settle
  it for a competent reader. Not reported.

## 8. Verdict

I built a creator, an appender (twice), and a compactor, and a reader that
accepts all four outputs. The document determined every byte I emitted except
`file_id` and the freedoms it names as freedoms. I found **no** byte-level
defect: no place where two competent implementations reading this text could
disagree about a byte on disk in a way that changes a conformance verdict. The
three findings above are all in the writer-conduct and non-normative layers,
and I have graded them accordingly rather than reaching for byte-level.

Confidence that an implementation built from this text alone would
interoperate: **high**.
