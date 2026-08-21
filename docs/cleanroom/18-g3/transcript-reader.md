# Round 18 — Reader implementer, working transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five sequential `Read` calls covering lines 1–4339, plus three `sed`/`grep`
re-reads of §20.4, §20.5, §21.7 and `[R-WRT-09]`. I opened no other file in the
repository. I ran no `git` command, no web search, no web fetch, and did not
list any directory. I ran local Python that reads no repository file except
`spec/tarn.md` (a mechanical instance-count over §21's tables) — plus a CRC-32C
implementation, a TARN file *builder*, and a TARN *reader* I wrote from the
document alone, all in my scratchpad. I did not read the round-18 output
directory.

---

## 0. What I set out to do

Build a conforming reader on paper and in code: cold open, validation tiers,
layer access, tile read to decoded samples, degradation, and a worked byte
example. Stop every time the text failed to tell me what to do.

I did the changed sections first (§20.4, §20.5, §21.7, §23.1, Appendix G), then
spent the bulk of the walk on the reader path and on the arithmetic anyone can
check independently.

---

## 1. Constants and checksums I could verify independently

Before trusting anything, I implemented CRC-32C from §4.5's parameters
(Castagnoli 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR
0xFFFFFFFF, stored little-endian) and checked it against §4.5's own check
vector:

```
CRC-32C("123456789") = 0xE3069283   ✓  (§4.5, Appendix B)
CRC-32C(zero bytes)  = 0x00000000   ✓
```

Then every checksum and constant the document states that I could reconstruct:

| Claim | Where | Computed | Verdict |
|---|---|---|---|
| Appendix A trailer CRC `D2 38 09 E0` = 0xE00938D2 over trailer [0,60) | Appendix A | 0xE00938D2 | ✓ |
| CRC over 4 sentinel entries (80 bytes) = 0x80A34955, stored `55 49 A3 80` | §7.4 example | 0x80A34955 | ✓ |
| `crc_of_crc_array` over that 4-byte array = 0xC4EE982E, stored `2E 98 EE C4` | §7.4 example | 0xC4EE982E | ✓ |
| CRC of a full 2¹⁶-entry all-sentinel segment = 0xEECB3BB2 | §15.4 `[R-IDX-05]`, Appendix B | 0xEECB3BB2 | ✓ |

I then reconstructed §7.4's 81-byte layer-record payload field by field from the
§7.4 table and compared it byte-for-byte against the annotated hex dump. It
matches exactly, including the field offsets in the left column (name at 0,
layout 4, linearization 5, codec 7, filter 9, A 11, S 19, A_slab 27, rank 35,
C 36, dimension entry 38, channel entry 56, index_encoding 68, entry_count 69,
crc_of_crc_array 77, end 81). The prose accounting also holds: `4 + 34` for the
name and the nine scalars, `18` for the dimension entry, `12` for the channel
entry, `13` for the trailing fixed fields, 81 exactly. `[R-CNT-17]`'s
extent_length for that layer is `4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84` ✓.

Every other worked example I checked by hand and found correct: §11.2's grid
(4, 8) and P = 65,536; §11.4's ordinals (tile (1,2) → s = 10; coordinate
(300,700) → in-tile ordinal 44·256 + 188 = 11,452; planar disk ordinal
2·32 + 10 = 74); §14.2's interleaved layout (Q = 3, decoded 18, ordinal 5 at
[15,18); planar `b` 12 bytes with ordinal 5 at bytes 10–11; `t`/`m` Q = 5,
decoded 30, ordinal 5 at [25,30)); §14.3's packed plane (`55 01` with fill
false, `55 FD` with fill true); §14.5's edge tile (grid 2×2, tile (1,1) with one
real position and 15 padding, 32 bytes, values 1–15 each `CD AB`); §15.4's
1,000,000-entry layer (16 segments, last covering 16,960; region 20,000,064
bytes; segment 15 at [19,660,800, 20,000,000); CRC array at [20,000,000,
20,000,064); segment-relative byte 339,180; a full segment 1.25 MiB); §15.4's
planar example (disk ordinal 74 at region bytes [1,480, 1,500); channel-3
entries 96–127); §16.2's slab example (four runs, viewport rows 1–2 = ordinals
8–23 = runs 1 and 2); §17.3's shuffle example (`00 00 00 00 00 00 80 00 40 3F
40 40` — I recomputed the permutation i·n + j from scratch); §12.1's bfloat16
1.0 = 0x3F80 stored `80 3F`; §4.6's `température` at 12 bytes NFC / 13 NFD;
§20.3's 644-byte index region and 20 MB index note; §21.9's note arithmetic
(2³² entries → 2¹⁶ segments → 256 KiB CRC array; 2³⁶ → 4 MiB).

**No stated constant, offset, or checksum in the document is wrong.** That is a
negative result, but it is the one the charter asked me to check first, and I
checked all of them I could reconstruct.

I also ran the §21 register's own arithmetic mechanically, applying §21.1's
counting rule ("Instances within a cell are separated by semicolons, and a cell
reading — is one instance"):

```
rows: 121   instances: 273
F 36 / 58    L 49 / 116    T 26 / 55    R 10 / 44
```

which matches §21.8's "121 conditions over 273 instances" and each subsection's
own count (36 / 49 / 26 / 10). I then hand-audited about thirty cells against
§21.1's stated axes (layout formulas enumerated; *does not equal* gives two
directions, *exceeds* one; no direction for a checksum or a constant comparison;
a single predicate over several fields gives one instance). Every cell I checked
obeys the rule, including the ones where it bites hardest: T21 (3 = one
direction × three layouts) against T22 and T14 (6 = two directions × three
layouts); L33 and L34 at 4 because §11.4 and §12.2 each describe *two* reserved
sub-ranges, while L31/L43/L45 sit at 3 because §7.4/§17.2/§17.3 describe one;
L16/L17 enumerating containers but not the fields of a single predicate;
T12/T9/F32 at 1 for the same reason; R4's 6 frame constraints × 2 containers =
12; R5's 2 × 2 × 2 = 8. The register is arithmetically self-consistent.

---

## 2. The open path — every byte, in order

I wrote the open as code and ran it. Here is what it fetches from a cold start
against a ranged server, and what bounds each range *before* the range is read.

### Request 1 — suffix `bytes=-64`, 64 bytes

Nothing in the file bounds it: 64 is a constant of the format (§6.2, Appendix
B), and the trailer's position is fixed at [F − 64, F) in every format major
(`[R-CNT-24]`). The response also carries F, and `[R-CNT-10]` licenses "the
complete length of a range response" as transport-authoritative, which is what
lets §19.1's steps 1 and 2 cost one request between them (§6.4).

Validation, in §6.2's mandated order — and the order matters, because only the
first three touch fields whose positions are fixed across majors:

1. trailer magic `8A 4E 52 41 54 0D 0A 1A` at trailer offset 0 — F8, and F1's
   byte-reversed specialization.
2. trailer CRC at [60,64) over [0,60) — F14. Nothing below this line may be
   acted on before it passes (`[R-ENC-05]`, `[R-ENC-10]`).
3. version gate: `version_major == 0` → F18, reject-file; `version_major != 1`
   → capability refusal, *not* a finding about the bytes (§2.3, §21.6). I made
   my reader emit a distinct diagnostic here per `[R-CNT-07]`'s SHOULD.
4. then, together: incompat lane bits 0–15 (F19); `committed_file_length ==
   transport size` (F17) and `% 64 == 0` (F13); `dir_offset ≥ 16` (F9);
   `dir_length ≥ 4` (F16); `dir_offset + dir_length ≤ F − 64` (F10);
   `1 ≤ generation ≤ 2⁶³−1` (F11 / F2); `file_id != 0` (F12); reserved [56,60)
   zero (F15). Plus `[R-ENC-03]`'s domain on each u64 (F2) and `[R-ENC-04]`'s
   sum rule on `dir_offset + dir_length` (F3), both before the sum is compared.

Note the ignore lane (bits 16–31) is *not* a gate: `[R-CNT-08]` requires
ignoring it, and §21.6 records a set ignore-lane bit as a non-violation.

**Front block.** My remote reader's 64-byte window does not reach offset 0, so
[0,16) is non-resident and `[R-CNT-04]` lets me defer or omit the equality
check. I omit it. A local reader, a memory mapping, or a speculative window that
reached 0 must check it *before other processing* (§19.1 step 1). This is a
deliberate, documented divergence between two conforming readers over the same
bytes — I looked hard at whether it is a defect and concluded it is not: §6.1
states the residency test explicitly and explains why it is residency and not
transport.

### Request 2 — `[dir_offset, dir_offset + dir_length)`

Bounded, before reading, by three gates already checked against a CRC-verified
trailer: `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64`.
That last one is what satisfies `[R-SEC-02]`'s "MUST NOT size a fetch in
proportion to a declared magnitude it has not corroborated against the file's
actual length". §21.9's 16 MiB directory guarantee is the floor a reader must
accept.

Then: verify the terminal 4 bytes against CRC-32C over the preceding
`dir_length − 4` bytes (F20, `[R-CNT-11]`) before any other use of the region.
The record sequence is exactly `[dir_offset, dir_offset + dir_length − 4)`,
which F29 restates.

### Record walk (§19.1 step 4)

24-byte header + `inline_length` inline payload, repeated, no residue. Per
record: type 0 → F24; header or payload past the sequence end, or trailing
residue → F29; unknown top-level type with MU = 1 → reject-file (F35 if
reserved-range; capability refusal if experimental, §21.6); unknown with MU = 0
→ ignore-record; two top-level type-0x0002 records → F34; the extent-slot rules
for **non-layer** top-level records (F30/F31/F32) — note the layer record's own
slot is *not* checked here, it is deferred to layer access, which is exactly
where L15/L17 place it; and for a top-level user-metadata record, no (0,0) slot
(F21), `extent_length ≥ 5` (F22), `inline_length == 1` (F23). An encoding byte
of 0 or 3–0x7F is R1 — **ignore-record, at open**, and the open continues.

I noticed that a reader must validate the extent slot of a record it will then
*ignore*. That is right — §19.1 step 4 says so in terms, and it is what makes
`[R-CNT-02]`'s partition checkable — but it is worth stating, because "skipped
as though absent" (§2.4) reads the other way at first.

Then the layer-name namespace. §19.1 nails the two things I would otherwise have
guessed: uniqueness is decided **first**, and over **raw bytes** regardless of
well-formedness; and a layer record whose name field does not lie within its
`inline_length` contributes no name and is instead reject-layer. So F4 fires on
two byte-identical name fields even when neither is a valid name, and L3/L5/L6
(ill-formed UTF-8, empty, C0 control) fire at **open** with **layer** scope —
the one place in the document where an open-tier check yields a layer-scope
outcome, and the register agrees.

### Cost, measured

Against the file I built (§4 below): **2 requests, 173 bytes** — `(384,448)` and
`(228,337)`. Against Appendix A's 128-byte file: **2 requests, 68 bytes**
(64 + 4). Appendix A's own paragraph about the 112-byte window covering [16,128)
checks out: that window contains the directory at [16,20) and the trailer at
[64,128), so §6.4's containment test spares request 2 while leaving [0,16)
non-resident.

The working set is the trailer and the directory and nothing else, at any file
size and layer count (`[R-RDR-01]`). Confirmed by construction: my open touches
no extent slot's contents, no index, no payload.

---

## 3. Validation timing by tier — what I check when, and what I never check

**At open** (§19.2 first bullet): front block if resident; trailer; directory
region and its record walk; layer-name namespace. Concretely F1–F24, F29–F32,
F34, F35, and L3/L5/L6, plus R1 for a top-level metadata record.

**At first access to a layer** (§19.3): the full layer record — slot validity
(`[R-CNT-13]`), the whole §7.4 constraint set (`[R-CNT-23]`), mutual exclusion
of A and S (`[R-CNT-16]`), exact parse and sub-record walk (`[R-CNT-18]`),
sub-record multiplicity (`[R-CNT-14]`), dimension/channel names, field widths and
the u64 domain, the value sets of §11.4/§12.2/§14.1/§15.1/§17.2/§17.3, the bool
fill constraint, the lz4 declaration cap, the geometry floor and its arithmetic,
`[R-ENC-04]`'s ceiling on every derived product including the decoded sizes, and
the index cross-checks `[R-CNT-17]` makes computable without I/O. **All of it
from resident bytes: layer access performs no fetch.** That is a strong claim
and I verified it holds — `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` against
`extent_length`, and `entry_count` against the geometry-derived addressed-tile
count, are both pure arithmetic over the directory.

**At use of a tile** (§19.4 steps 3–6): index chain, entry classification,
payload CRC, decode. Index-chain failures (L37, L38) are detected here but take
**layer** scope — §19.2 says so explicitly, and I would have got this wrong
otherwise.

**At use of a record's extent**: that extent's CRC, and the document content
rules §18.2 attaches *at its encoding* (R2–R10).

**Never, permissibly:** the front block when non-resident (`[R-CNT-04]`);
coverage and overlap (F7, F33, L18); alignment and slab invariants (L40–L42);
decoded content — padding positions, pad bits, interleaved bool bytes (T2, T4,
T5, T26); record flag bits — reserved bits, MU = 1 with PE = 0, and a registered
type's stored bits against §7.3 (F25, F26, F28, L46, L47, L49); a reserved-range
type value as such (F36, L25); user-metadata member ordering (F27, L48); and
anything in a layer the caller never touches (§19.2's closing sentence).

A verifier gives up every one of those exemptions (§2.3, Appendix H), including
the front block — F6's condition says so in terms.

---

## 4. A file I built, and the tile read through it

I built a complete file from the document alone: the §7.4 `sst` layer (rank 1,
dim `x` extent 100 / tile extent 32, one interleaved float32 channel `temp`,
fill 0x7FC00000, codec 1, filter 1), with tile 0 **stored** carrying the float32
values 0.0 … 31.0 and tiles 1–3 sentinel.

```
[0,16)     front signature block
[16,144)   tile 0 payload, 128 bytes           (P·Q = 32 · 4)
[144,224)  index entry array, 4 × 20 bytes
[224,228)  segment CRC array, ⌈4/2¹⁶⌉ × 4 = 4 bytes
[228,337)  directory: one 24-byte header + 81-byte payload + 4-byte CRC = 109
[337,384)  pre-trailer pad, 47 bytes of slack
[384,448)  trailer.  F = 448, 448 mod 64 = 0
```

Entry 0 = `(offset 16, length 128, crc 0xF8118D31)`; entries 1–3 =
`FF ×16 00 ×4`. Segment CRC over the 80 entry bytes = 0xB76F7866;
`crc_of_crc_array` = 0x9F491382. `dir_offset + dir_length = 337 ≤ F − 64 = 384`
✓. Coverage walk (§9.7): claimants are [0,16), [16,144), [144,228), [228,337),
[384,448); disjoint; each non-boundary claimant inside [16, F−64) = [16,384);
slack = 448 − 401 = **47 bytes**, exactly the pre-trailer pad. My builder and my
independent §9.7 walk agree.

My reader, run against it:

```
OPEN: 2 requests [(384,448),(228,337)], 173 bytes, generation 1, 1 layer
layer sst: G [4]  N 4  P 32  Q 4  decoded size 128  entry_count 4

x=0    tile 0 decoded, in-tile ordinal 0,  bytes 00 00 00 00 = 0.0
x=31   tile 0 decoded, in-tile ordinal 31, bytes 00 00 f8 41 = 31.0
       tile-read requests: (224,228) CRC array, (144,224) segment, (16,144) payload
       cumulative 5 requests, 385 bytes for a cold remote first-sample read
x=32   tile 1 -> fill 00 00 c0 7f
x=97   tile 3 -> fill 00 00 c0 7f      (tile 3 covers x 96..127; 96..99 real, 100..127 padding)
x=99   tile 3 -> fill 00 00 c0 7f
x=100  request fails as a request, no verdict on the file   (§19.4 step 1, R-MDL-01)
```

The three tile-read fetches are the ones §1 promises: the layer's segment-CRC
array, the index segment covering the tile, the tile's own bytes. Every range is
computable from the layer record alone — CRC array at
`[extent_offset + entry_count·20, extent_offset + extent_length)`, segment s at
`[extent_offset + s·2¹⁶·20, extent_offset + min((s+1)·2¹⁶, entry_count)·20)` —
which is what §15.4 claims and what makes the parallel fetch legal.

### The decoded byte layout I end up with

For this layer: 128 bytes, value k at byte `(k div C)·Q + F_{k mod C}` = `k·4`
with C = 1. Channel c's value at in-tile ordinal u is at `u·Q + Fᶜ`. For the
general cases I traced §14.2/§14.3 by hand:

- **planar numeric channel c**: `P · Bᶜ` bytes, value k at `k · Bᶜ`.
- **interleaved**: `P · Q` bytes, `Q = Σ Bᵢ`, value k at `(k div C)·Q + F_{k mod C}`,
  `Fᶜ = Σ_{j<c} Bⱼ`; bool contributes `Bᶜ = 1` and one byte 0x00/0x01.
- **planar bool**: `⌈P/8⌉` bytes, value k at bit `k mod 8` of byte `k div 8`,
  LSB-first, pad bits `P mod 8 … 7` of the final byte carrying the fill bit.

I checked `[R-COD-10]`'s divisibility claim ("The decoded image's length L is
divisible by s in every case") holds in all three: `P·Bᶜ / Bᶜ`, `P·Q / Q`,
`⌈P/8⌉ / 1`. And I re-derived the shuffle inverse from the forward rule: forward
sends byte i of group j to `i·n + j`; inverse sends filtered offset q to
`(q mod n)·s + (q div n)`, which is exactly the document's "restores byte
i · n + j to offset j · s + i". Correct.

Pipeline order on the read side, from §17.1 and §19.4 step 6: verify the entry
crc, **codec decode**, then **filter inverse**, then `[R-SER-07]`'s exact-size
check. (Write side is filter then codec.) I had to read §17.1 twice to be sure
which stage the stored bytes are "of"; the sentence "the filtered image is the
codec's input" settles it.

---

## 5. Degradation walks

**(1) Unknown record type, top level, MU = 0** (experimental ≥ 0x8000).
`[R-CNT-15]` → ignore-record; §21.6 → the file is conforming. My reader still
validates the record's extent slot (F30–F32) and still counts its extent as a
coverage claimant if it is a verifier. It serves every layer normally. The
extent is covered by *no* checksum (§8.1's last row), so corruption inside it is
invisible — §22.3 says so, and `[R-WRT-08]` bars an updater from re-encoding it.
If the same type came from the reserved range, my reader behaves identically and
a verifier additionally records F36.

**(2) Unknown record type, top level, MU = 1.** `[R-CNT-15]` → reject-file. The
reader serves nothing at all, not even the layer list. §21.6 is explicit that in
a conforming file this type is necessarily experimental, that the file stays
conforming, and that the diagnostic should distinguish a capability refusal from
corruption. A verifier reports *cannot establish*, not *nonconforming* (§2.3) —
and, because a live trailer *was* established, still owes a **partial** slack
total naming what stopped the walk (`[R-CNT-21]`). The same type as a layer
sub-record is reject-**layer**, never reject-file (`[R-CNT-18]`) — that
asymmetry is the one I most expected to be underspecified and it is not.

**(3) Unknown codec.** There is no such thing for a conforming reader: codecs
1–4 are core (`[R-COD-03]`, `[R-CNF-03]`), so software that cannot run one is
not a conforming reader. What a reader *can* meet is a reserved (5–0x7FFF) or
experimental (≥ 0x8000) value → L43, **reject-layer at layer access**, before
any fetch. It may still list the layer and its name (§2.4); every other layer is
untouched; no tile of this layer is served, and no fill is served in place of
one (`[R-TYP-09]`, `[R-CNF-09]`). Same shape for filter (L45), layout (L36),
linearization (L33), sample type (L34), index_encoding (L31).

**(4) Truncated tail.** The physical file is shorter than the last commit
intended. The final 64 bytes are payload or index bytes, so the magic fails →
F8, reject-file, reported as "torn or invalid", and `[R-LIF-05]` forbids me to
scan backward. If the last 64 bytes *do* happen to parse as an older valid
trailer, `committed_file_length` will not equal the transport size → F17. Either
way the reader stops; §9.6's probe is a recovery tool's operation and "not a
reader behavior", and its output must be re-verified as a whole file before
being trusted. §9.5's note reminded me to retry once on a shared filesystem
before concluding torn.

**(5) Checksum mismatch — five distinct blast radii.** trailer → reject-file
(F14); directory → reject-file (F20); `crc_of_crc_array` or a segment CRC →
reject-**layer** (L37, L38) even though I detect them at tile use; a stored
tile's crc → reject-**tile** (T1) with neighbours in the same layer unaffected;
a user-metadata extent's terminal CRC → **ignore-record** with a SHOULD-report
(R2), and the structural data it annotates is untouched. I traced the last one
carefully because the quarantine (`[R-CNT-25]`) overrides `[R-CNF-08]`'s
owning-scope mapping — a top-level metadata record's containing scope is the
file, and the outcome is still ignore-record.

**(6) Limit exceeded.** `[R-ERR-04]`: I may decline at the whole file, or at the
narrowest scope whose declarations exceed what I can serve — a layer or a tile —
and I MUST report it as a resource limit, never as a validity error. I may not
decline on that ground any file whose every quantity lies inside §21.9's table.
A concrete case I traced: a zstd frame declaring a 64 MiB window on a 256 MiB
tile is conforming (`[R-COD-06]` only bars a window *exceeding the decoded
size*), and a reader whose ceiling is §21.9's 8 MiB may decline the tile or the
layer. Critically, a declined tile may **not** read as fill: `[R-MDL-02]`
requires bit-exact reference-array content from any portion read, and fill is
produced by exactly one condition, a sentinel entry from a verified chain
(`[R-TYP-09]`).

**(7) Format major it does not implement.** `version_major = 2`: reject-file on
capability grounds at gate 3 of §6.2, before any other field is examined —
which is why §21.2's preamble can say the geometry rows do not reach such a
file, and why exactly four rows (F8, F14, F6, F1) do. A verifier reports
*cannot establish*. The diagnostic must be distinct from "not a TARN file" and
from "corrupt".

**(8, extra) Malformed index entry.** Six of §15.3's rows are *structural*:
sentinel-with-nonzero-crc, half-sentinel, zero length, offset < 16, either field
above 2⁶³−1, and sum overflow or past F − 64. All reject-tile; none yields a
stored extent, so they are transparent to slab run continuity and contribute
nothing to the coverage walk, and the bytes they nominally addressed fall to
slack. The seventh reject-tile row — stored bytes failing the entry's crc — is
*not* transparent: the entry is well-formed and its extent stands. I checked
this consistently across §15.3, §16.2, §9.7 and L41's condition text; all four
say the same thing.

---

## 6. Places I had to make a judgement

Enumerated honestly, whether or not I think they are defects.

1. **§19.2's "no earlier" clause.** "before anything the extent holds is
   returned — no earlier, since the open fetches no extent (§19.1)". Read as a
   prohibition it would contradict "A reader MAY detect any violation earlier
   (`[R-CNF-12]`)" three paragraphs down. Read as a statement about where the
   *obligation* sits — which the causal clause forces — it is fine. I took the
   second reading. Not reported: the causal clause is decisive and the
   Rationale ("The rule fixes the *latest* detection point") confirms it.

2. **Order of checks inside layer access.** Nothing fixes the order among
   `[R-CNT-16]`, `[R-CNT-23]`, `[R-GEO-01]` and the rest. All yield
   reject-layer, so no two readers can disagree about anything observable. Not
   reported.

3. **§21.7's "witnessed only where …".** Reported below as reader-01.

4. **`[R-WRT-09]`'s "each relocated extent's checksum" against its own premise
   "every structure it copies".** Reported below as reader-02.

5. **§20.4's obligations table carries no requirement identifier.** The
   paragraph introducing it ("Persistence governs every record type … and carry
   these obligations:") and the three-row table are normative under §2.1 and
   contain MUSTs, but sit between `[R-WRT-05]` and `[R-WRT-08]` unlabelled,
   against §2.2's "Normative requirements carry identifiers". I decided this is
   *not* a defect: `[R-CNF-06]` binds "the preservation obligations of §20.4" by
   reference, §2.4 points at "§20.4's table" by name, no §21 row cites the table
   (these are updater-conduct obligations with no single-file witness, §21.7's
   class), and so `[R-VEC-02]`'s "cite the governing requirement identifier"
   never has to reach it. Two implementers cannot disagree about the
   obligation. Not reported.

6. **§21.1's "which is why §14.2 calls it the sole resolved byte in this
   format".** §14.2 states `[R-SER-08]` but does not use that characterization;
   §12.3 does ("the one case where a reader resolves a byte to a value rather
   than passing it through"). Loose attribution, no behavioural consequence. Not
   reported.

7. **§23.1's "an unknown ancillary record's drop (§20.4) the one other removal
   available to it".** §20.4's preamble ("Persistence governs every record type;
   only the authoritative source of the flags differs") also lets an updater
   drop a record of a type it *does* implement that this specification does not
   register, where the external definition assigns PE = 0. That record is not
   "unknown". A privacy-consideration sentence understating one case by a hair;
   no actor behaves differently. Not reported.

8. **A compactor and a corrupt user-metadata extent.** Following the text: a
   one-bit flip in a user-metadata extent is R2 (ignore-record) to a reader, so
   the file reads fine forever — but `[R-WRT-09]` obliges a compactor to verify
   that extent's checksum, `[R-WRT-06]` obliges refusal when any `[R-WRT-09]`
   check fails, and §20.4 licenses no drop for a PE = 1 record, so the file can
   never be compacted, only rewritten wholesale by a producer. Surprising, but
   decidable and consistent, and §20.4's closing paragraph anticipates the
   "write a new file instead" answer. Not reported as a defect; noted here
   because it took me a while to be sure it was not one.

9. **A compactor silently repairing L18.** If the input has two overlapping
   stored extents within one layer, a compactor's `[R-WRT-09]` checks (index
   chain, entry crcs) do not detect it, and relocating both to disjoint places
   yields a conforming output with an unchanged reference array. Deliberate, per
   §20.1/`[R-WRT-01]` and §20.5's "placement is not among the things it carries
   forward". Not reported.

10. **A compactor that does not relocate a structurally-broken entry's region.**
    §20.5's regeneration passage says the compactor "cannot proceed without
    meeting it". But regeneration is scoped to "each *relocated* tile-index
    region"; a region that keeps its placement is never regenerated and the
    entry is never met. §20.1 and `[R-WRT-01]` explicitly license a latent
    violation travelling into the output, and §20.5's prohibition bites only on
    "a violation it has detected", so the outcome is determinate under both
    branches. Not reported; it is the same shape as finding reader-02 and I
    report that one once rather than twice.

---

## 7. Findings

### reader-01 — CONTRADICTION — §21.7, `[R-ERR-01]`

**Location.** §21.7, second paragraph, the clause on §20.3 step 4.

**Quotation** (verbatim, one sentence, semicolon-separated):

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — where §21.4's content rows fire; a change that reaches the
> decoded size instead is witnessed by T3 or T14, which
> test a length rather than the decoded image's content

**The defect.** The first clause asserts a *necessary* condition — the bar is
witnessed **only where** the change reaches "a byte §14 structurally
constrains", glossed exhaustively by the em-dashes as "a padding position, a pad
bit, or a boolean byte". The second clause then names a witness for a change
that reaches none of those: a decoded-size change, witnessed by T3 or T14, which
the sentence itself says "test a length rather than the decoded image's
content". The third clause does it again for a codec change (T15, T17, T23,
T25). A decoded size is not a byte; a codec declaration is not a byte; neither is
a padding position, a pad bit, or a boolean byte. The "only" is falsified inside
its own sentence, twice.

**Permitted readings.**
(a) The "only" governs the whole conjunction, and the two later clauses are then
wrong — untenable, because T3, T14, T17 and T25 demonstrably do fire on those
changes and are independently normative in §14/§17.
(b) The "only" governs "the affected tiles remain stored" alone, and the "and …"
clause is the first of three semicolon-separated *sufficient* conditions rather
than part of a necessary one. This is the only coherent reading, and it is
reinforced by the parallel item earlier in the same list, which uses the
opposite construction correctly: "the ordinal mappings of `[R-GEO-06]` and
`[R-SER-01]` are satisfied by a structurally valid tile whatever values it
carries, **except where** §14 constrains a byte's content".

**Which I picked, and what an implementer does wrong without it.** I took (b).
An implementer building a verifier's *reporting* from §21.7 who takes (a) would
conclude that a commit that changes a layer's decoded size or codec across
already-stored tiles is an unwitnessed obligation — one of the §21.7 class that
"no file-level witness exists to check" — and would classify a file failing T3
or T14 for that reason as an unwitnessed writer-conduct matter rather than the
established violation it is. He would not skip T3 or T14 themselves, because
they are normative in §14.2/§17.2 and registered in §21.4 with detector *reader*;
so the damage is confined to how the finding is characterised, not to whether it
is found.

**Byte-level: no.** §21.1 states that §21.7 "is not part of the register and
carries no rows", and that where a restatement and its rule diverge the rule
governs. T3, T14, T15, T17, T23 and T25 are unaffected by either reading, and
every reader and verifier reaches the same accept/reject verdict on every byte
sequence. I flag it because it is a self-contradiction in freshly revised text
and because reading (b) required me to override the plain sense of "only".

---

### reader-02 — AMBIGUITY — §20.5, `[R-WRT-09]`

**Location.** §20.5, the `[R-WRT-09]` paragraph.

**Quotation** (verbatim):

> A compactor's verification depth follows reliance over
> everything it carries (`[R-WRT-03]`): it relies structurally on every
> structure it copies, so it MUST verify each link of the chain —
> the open (§19.1), each retained layer's record (§19.3) and full
> index chain (`[R-IDX-04]`), and each relocated extent's checksum,
> including every stored tile's entry crc — before emitting that
> structure's bytes. `[R-WRT-09]`

**The ambiguity.** The premise quantifies over "every structure it **copies**";
the enumeration quantifies over "each **relocated** extent's checksum". §20.5's
own text distinguishes the two — "A compactor preserves content but not
placement" and "every stored tile's bytes verbatim … **except that relocation**
re-points extent slots, regenerates each relocated tile-index region" — so
"relocated" is a term the section uses to mean *placement changed*, not *carried
forward*. A compaction that reclaims slack moves nearly everything, but not
necessarily everything: a structure already at the first admissible offset, or
any structure whose new placement coincides with its old one, is copied without
being relocated.

**Permitted readings.**
(a) The compactor verifies the checksum of every extent it carries into its
output, relocated or not. The premise sentence and the closing "before emitting
that structure's bytes" both point here — emission, not relocation, is what
triggers the duty.
(b) The compactor verifies only the checksums of extents whose placement
changes. An extent that keeps its offset is copied unverified, and a violation
in it is "latent in a structure it carries forward verbatim", which §20.5's
first paragraph and `[R-WRT-01]` expressly let travel into the output.

**Which I picked, and why.** (a). The requirement's premise is stated as the
rule — "it relies structurally on every structure it copies, **so** it MUST
verify each link" — and the clause "before emitting that structure's bytes" ties
the duty to emission rather than to movement. The word "relocated" in the
enumeration reads as loose shorthand carried over from the neighbouring
sentence about regenerating relocated index regions.

**What an implementer does wrong without it.** Under (b) a compactor may emit an
output carrying an extent whose terminal CRC fails — an R2 or, for a stored tile,
a T1 — without ever having "detected" it, so `[R-WRT-06]`'s "MUST NOT emit a
file carrying a violation it has detected" is not triggered and the compactor's
conduct is conforming. Under (a) it must refuse. The concrete case is narrow but
real: a top-level user-metadata extent placed at offset 16 in an input whose
compaction leaves it at offset 16.

**Byte-level: no, and I want to be exact about why.** The two readings differ in
what a conforming *compactor* may emit, not in what any reader must accept or
reject: the output file's conformance is decided by its own bytes either way (it
carries an R2/T1 violation under (b), and a reader treats it exactly as it
treats any such file), and no reader's verdict on any byte sequence changes.
`[R-WRT-01]` already licenses latent violations to travel into a compactor's
output, so reading (b) produces nothing the document does not already admit for
structures a compactor's depth does not reach. The fork is in one writer-tier
tool's conduct on one input, not in the accept/reject predicate. I report it
because §20.5 is the section this round revised most, because the premise and
the enumeration genuinely disagree in scope, and because a compactor author
reading only the enumeration builds a shallower tool than the premise asks for.

---

## 8. Overall verdict

I built a conforming reader from this document and nothing else — cold open,
tiered validation, layer access, index chain, sentinel and fill, decode, extract
— and ran it against a file I also built from this document alone. Every
constant, offset and checksum the document states and that I could reconstruct
is correct, including the four checksums, the 81-byte layer-record layout, the
Appendix A dump, and the whole of §21's 121/273 instance arithmetic. The two
findings above are prose defects in text the round revised; neither forks bytes.

The document determined everything I needed.
