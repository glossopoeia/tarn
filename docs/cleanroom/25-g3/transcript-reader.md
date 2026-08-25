# Cleanroom round 25 — Reader implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,477 lines, read in full in five sequential chunks). I ran `wc -l` and one
`grep -o` over that same file, and four local Python scripts that read no
project file (a CRC-32C implementation, an Appendix A decoder over a hex dump I
typed from the document, a register-instance counter that reads the spec file,
and a file builder/reader pair operating on bytes I generated myself in
`scratchpad/`). I opened no ADR, no `docs/`, no `conformance/`, no
`registry.json`, no `PLAN.md`, no `AGENTS.md`, no git history. I ran no
`git log`, `git diff`, `ls`, or directory listing. No web access.

**Unrequested context that appeared before I began.** My runtime placed three
things in context without my asking:

1. A project-instruction file (`CLAUDE.md` → `AGENTS.md` pointer) — content not
   loaded beyond the pointer line.
2. An index of the maintainer's private memory notes, with six titled entries
   and one-line descriptions naming project process, a naming constraint, and
   past workflow-failure shapes.
3. A `gitStatus` block listing the **five most recent commit subject lines**.
   Those subjects name round 24's outcome, ADR numbers, and — in one case — a
   phrase about a specific register row and a specific rule identifier.

Item 3 is the material one: it named a register row and a requirement
identifier that I would otherwise have had no pointer to. I disregarded it. I
did examine the row it names, but only as part of a systematic mechanical
re-derivation of *every* register cell's instance count (§1 of my walk below,
run over all 121 rows), and I reached no finding about it — I explicitly
declined to report it after deriving its instance count from §21.1's stated
rules and finding it defensible. None of my three findings touches any section
or identifier those commit subjects name. I report the exposure because the
brief requires it and because a disclosed breach is usable where a silent one
is not.

I did not read the output directory, and did not list it.

---

## 1. Constants and arithmetic I could check

Before implementing anything I checked every stated constant and every worked
number I could reproduce locally. All of the following verified:

| Claim | Section | Result |
|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5 | ✔ |
| CRC-32C(zero bytes) = `0x00000000` | §4.5 | ✔ |
| CRC of the 80-byte 4-sentinel entry array = `0x80A34955`, stored `55 49 A3 80` | §7.4 example | ✔ |
| crc_of_crc_array over `55 49 A3 80` = `0xC4EE982E` | §7.4 example | ✔ |
| CRC of a full 2¹⁶-sentinel segment = `0xEECB3BB2` | §15.4, App. B | ✔ |
| Appendix A's 128-byte file: trailer CRC `0xE00938D2` over `[0,60)` | App. A | ✔ |
| Appendix A field decode (gen 1, dir_offset 16, dir_length 4, cfl 128, file_id `0x0123456789ABCDEF`, reserved zero) | App. A | ✔ all |
| §7.4's layer-record payload = 81 bytes, every listed offset | §7.4 | ✔ each of 18 field offsets |
| ⌈100/32⌉ = 4; 4×20 + ⌈4/2¹⁶⌉×4 = 84 | §7.4 | ✔ |
| §11.2 grid: (1024,2048)/(256,256) → G=(4,8), N=32, P=65,536; ⌈1000/256⌉ = 4 | §11.2 | ✔ |
| §11.4: (300,700) → tile (1,2), s = 10, in-tile (44,188), ordinal 11,452; planar c=2 → 74 | §11.4 | ✔ |
| §14.2: interleaved (2,3) uint8+uint16 → Q=3, size 18, ordinal 5 at [15,18); planar `b` 12 bytes, ordinal 5 at 10–11; float32+bool → Q=5, size 30, [25,30) | §14.2 | ✔ |
| §14.3: P=10 alternating → `55 01`; fill true → `55 FD` (0x01 \| 0xFC) | §14.3 | ✔ |
| §14.5: (5,5)/(4,4) edge tile (1,1) → 1 real + 15 padding, 32 bytes, values 1–15 = `CD AB` | §14.5 | ✔ |
| §15.4: 1,000,000 entries → 16 segments (15 full + 16,960), array 64 B, region 20,000,064; k=999,999 at segment-relative 339,180; array [20,000,000, 20,000,064); segment 15 [19,660,800, 20,000,000); full segment 1.25 MiB | §15.4 | ✔ |
| §15.4: planar C=4 N=32, ordinal 74 at region bytes [1,480, 1,500); channel 3 = ordinals 96–127 | §15.4 | ✔ |
| §16.2: N=32, S=8 → runs [0,8) [8,16) [16,24) [24,32); rows 1–2 = ordinals 8–23 | §16.2 | ✔ |
| §17.3: shuffle of `00 00 80 3F 00 00 00 40 00 00 40 40` (s=4,n=3) → `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | ✔ |
| §20.3: 32·20 + 4 = 644 | §20.3 | ✔ |
| §21.9 note: 2³² entries → 256 KiB CRC array; 2³⁶ → 4 MiB | §21.9 | ✔ |
| `température` NFC 12 bytes / NFD 13 bytes, byte sequence as given | §4.6 | ✔ |
| Signature/magic byte strings; zstd magic `28 B5 2F FD`; lz4 frame magic `04 22 4D 18`; `0x7E000000` | §6.1, §6.2, §17.2, §21.4 | ✔ |
| CRC-32C polynomial 0x1EDC6F41 → reflected 0x82F63B78 | §4.5 | ✔ |

**Register counts.** I parsed all four register tables mechanically and applied
§21.1's own counting rule ("Instances within a cell are separated by
semicolons, and a cell reading — is one instance"):

```
rows: 121   instances: 277
F: 36 rows / 58 instances     L: 49 rows / 116 instances
T: 26 rows / 55 instances     R: 10 rows /  48 instances
```

§21.2 claims 36, §21.3 claims 49, §21.4 claims 26, §21.5 claims 10, §21.8
claims "121 conditions over 277 instances". **All five figures are exact.**

I also derived, independently of the cells, the instance sets the *rules*
imply, for the cells most exposed to hint #5:

- **L1** (u64 fields of a layer record) — the layer record's `u64` "offset,
  length, extent, or count" fields are exactly: layer extent_offset, layer
  extent_length, sub-record extent_offset, sub-record extent_length, Eᵢ, Tᵢ,
  entry_count, S = **8**. `A` and `A_slab` are correctly *excluded*: they are
  neither offset, length, extent nor count, and their out-of-domain values are
  caught by L39/L29's power-of-two range rows instead. Cell says 8. ✔
- **L2** (derived sums/products) — I enumerated every quantity §11.2, §14.2,
  §14.3, §15.1 and §7.4 derive: Gᵢ (≤ Eᵢ, cannot overflow), N, P, N·P, C·N,
  Q (≤ 65,535·8, cannot overflow), Fᶜ (≤ Q), P·Q, V=P·C (dominated by P·Q),
  P·Bᶜ, ⌈P/8⌉ (≤ P), 20·k (dominated), the index-length formula, and the two
  extent sums = **9 that can overflow**. Cell says 9, and its two "dominates"
  parentheticals are both correct: P·Q ≥ P·C because every Bᵢ ≥ 1, and
  C·N = (C−1)·N + (N−1) + 1. ✔
- **T4** vs `[R-SER-05]` — the rule names three forms (numeric fill bytes,
  interleaved bool fill byte, packed-plane fill bit); the cell splits the first
  by layout, which §21.1's stated layout axis licenses. 4. ✔
- **F7 / F33** — §5.2's structure classes are stored-tile extent, record
  extent, directory, trailer. F7 (gap between directory and trailer) correctly
  omits directory and trailer; F33 adds directory. ✔
- **L18** vs §15.3/`[R-CNT-13]` — the structures a layer owns are stored-tile
  extents, its index region, its sub-record extents. 3. ✔
- **§20.5's row list** — "one row for each of the other seven spaces §10.2
  tabulates (L31, L33, L34, L36, L43, L45, R1)": index encoding, linearization,
  sample type, channel layout, codec, filter, metadata encoding = 7, and each
  space does carry exactly one row. ✔
- **§15.3's "Six rows are marked *structural*"** — I counted 6. ✔
- **§18.2's "Four restrictions"** — 4 bullets. ✔ **§17.2's "Three frame
  features are excluded"** — dictionary, content-checksum, window. ✔
  **§22.3's "Four residues"** — 4. ✔ **§10.1's four vehicles** — 4. ✔
  **§21.7's "four obligations" on a compacted trailer** — fresh file_id draw,
  generation, ignore-lane bits, version_minor floor; all four are in
  `[R-WRT-06]`. ✔ **§21.9's "last three rows … first five rows"** — 3+5 = 8
  table rows. ✔

**Requirement identifiers.** I extracted every `[R-…]` token: 19 prefixes, all
in §2.2's list; numbering is contiguous within every prefix with exactly one
gap — `[R-SER-04]`, which §14.4 declares withdrawn and permanently retired.
`[R-ENC-100]` appears once, in §2.2's own example of a three-digit number, not
as a requirement. No duplicates, no orphans.

I found no numeric error anywhere in the document.

---

## 2. The open path, byte by byte

I implemented §19.1 literally. The four steps and what each costs:

**Step 1 — end of file.** Obtain transport-authoritative F (`[R-CNT-10]`). A
local reader gets this for free; a remote reader gets it from the
`Content-Range` of the step-2 suffix response, so steps 1 and 2 cost one
request between them (§6.4). Three things are *not* substitutable here: the
trailer's own `committed_file_length` (`[R-CNT-10]` forbids it), a 200 response
treated as a range (`[R-CNT-10]` forbids it), and a transport with no
suffix-range support (SHOULD fall back to size probe + absolute range; without
it the open fails).

Front block: the obligation turns on **residency**, not transport
(`[R-CNT-04]`). My local reader holds `[0,16)` and MUST compare it by equality
before other processing. A remote reader that would have to issue another
request MAY defer or omit — and §6.4's two-request accounting excludes the
front block. A verifier holds no such exemption (§2.3, Appendix H), so a remote
verifier owes a third request.

**Step 2 — trailer.** Fetch `[F−64, F)` = **64 bytes, one request**. What
bounds this range before I have read anything: nothing derived from the file —
the trailer's 64-byte size is a constant fixed permanently by `[R-CNT-24]` and
Appendix B. Validate in §6.2's fixed order: magic → CRC → version gate → then,
as an unordered set, flags / cfl-vs-transport-size / cfl mod 64 / dir_offset ≥
16 / dir_length ≥ 4 / dir_offset+dir_length ≤ F−64 / 1 ≤ generation ≤ 2⁶³−1 /
file_id ≠ 0 / reserved zero.

**Step 3 — directory.** Fetch `[dir_offset, dir_offset + dir_length)` =
**dir_length bytes, one request**. What bounds it *before* I read it: the
step-2 gates — dir_length ≥ 4, dir_offset ≥ 16, dir_offset + dir_length ≤
F − 64 — all of which are covered by the trailer CRC I have already verified,
which is what makes `[R-ENC-05]` satisfiable. The ceiling is therefore F − 80;
§21.9's 16 MiB minimum guarantee is the point below which a reader may not
decline on resource grounds.

**Step 4 — record walk.** No I/O. Parse 24-byte headers + inline payloads with
no residue; MU gate for unknown top-level types; multiplicity; extent-slot
validity for *non-layer* top-level records only (layer slots wait for §19.3);
the user-metadata framing triple (no (0,0), extent_length ≥ 5, inline_length
exactly 1); and the layer-name namespace.

**Cold remote open, byte-exact.**

> **2 requests, 64 + dir_length bytes.**
> Request 1: suffix `bytes=-64` → 64 bytes, also yielding F.
> Request 2: `bytes=dir_offset-(dir_offset+dir_length-1)` → dir_length bytes.

For Appendix A's minimal file that is **2 requests, 68 bytes**. For the sample
file I built (below) it is **2 requests, 187 bytes** (64 + 123). Neither figure
scales with layer count or file size — that is `[R-RDR-01]`'s working-set
invariant, and I confirmed it: my open touches no extent slot's contents, no
index, no payload.

The speculative alternative (§6.4) is one request for a suffix window plus a
containment test. Appendix A's note that a 112-byte window covering [16,128)
contains the directory while leaving [0,16) non-resident is correct, and my
reader reproduces that split.

---

## 3. Validation timing by tier

I implemented §19.2's four tiers plus certification. Restating them as the
decision table my reader actually uses:

| Tier | Checked | Register rows |
|---|---|---|
| open | front block (if resident), trailer, directory CRC, record walk, top-level extent slots, top-level user-metadata framing, layer-name namespace, layer-record names | F1–F6, F8–F24, F29–F32, F34, F35; L3, L5, L6; R1 (top-level) |
| layer access | everything in §19.3's list, all from resident bytes and F — **no fetch** | L1, L2, L4, L7–L17, L19–L36, L39, L43–L45; R1 (sub-record) |
| tile use | index chain, entry classification, payload CRC, decode, exact size | L37, L38; T1, T3, T6–T14, T17–T25 |
| extent use | extent CRC and the document rules §18.2 attaches at its encoding | R2–R10 |
| certification | everything a reader is exempt from | F7, F25–F28, F33, F36; L18, L25, L40–L42, L46–L49; T2, T4, T5, T26 |

Three timing facts I had to pin down and which the document does give me:

- **Never checked by a conforming reader**: live-state coverage/overlap
  (F33, L18), the pre-trailer-gap rule (F7), record flag bits (F25/F26/F28,
  L46/L47/L49), reserved-range *types* with MU = 0 (F36, L25), slab/alignment
  invariants (L40–L42), decoded content (T2, T4, T5, T26), and metadata member
  ordering (F27, L48). §21.1 is explicit that for those rows "the outcome names
  the scope at which the damage is recorded, not an obligation on any reader",
  and `[R-CNF-12]` still licenses a reader that *does* detect one to reject.
- **Detected earlier than its outcome's scope suggests**: index-chain failure
  is detected at tile use and takes *layer* scope (`[R-IDX-04]`, §19.2). My
  reader had to carry a per-layer "barred" flag distinct from its per-tile
  failures.
- **Prospective, not retroactive**: reject-layer "bars further service from the
  layer, and does not retroactively invalidate content already returned under
  §19.2's validation timing" (§2.4, §19.4 step 8). So a region read that
  returns tiles 0–4 and then hits a bad segment CRC keeps its first five tiles.

---

## 4. Layer access and the tile-read algorithm — a worked file

I built a complete non-trivial file byte-exactly from the document alone, then
wrote a second, independent reader that consumes it through §19.1/§19.3/§19.4
and issues explicit ranges so I could count them.

**The layer.** interleaved, rank 2, dimensions `y`,`x`, E = (5,5), T = (4,4),
one channel `v` of type 7 (uint16) with fill `0xABCD`, codec 1, filter 1, no
alignment, no slab, linearization 1, index_encoding 1.

Derived: G = (2,2); N = 4; P = 16; Q = 2; addressed = N = 4 (interleaved);
decoded size = P·Q = 32; index extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = **84**;
inline_length = **95** bytes.

**Placement.**

```
[0,16)      front signature block
[16,48)     tile s=0   32 B      [48,80)    tile s=1
[80,112)    tile s=2             [112,144)  tile s=3
[144,224)   index entry array (4 × 20)
[224,228)   segment-CRC array (1 × 4)
[228,351)   directory: one layer record (24 + 95) + 4-byte CRC   dir_length = 123
[351,384)   pre-trailer pad, 33 bytes (to the next 64 boundary)
[384,448)   trailer                                              F = 448, F mod 64 = 0
```

Cross-checks: dir_offset + dir_length = 351 ≤ F − 64 = 384 ✔; F is a multiple of
64 ✔; discovery window dir_length + pad + 64 = 220 ≤ 65,536, satisfying §6.4's
writer SHOULD ✔; no structure lies between the directory's end and the trailer
(`[R-CNT-05]`) ✔; the four stored extents, the index region and the directory
partition [16, 384) with no overlap (`[R-CNT-02]`) ✔.

**Padding content.** Under `[R-SER-05]` every padding position of every edge
tile carries `CD AB`. Tile s=3 (tile coords (1,1)) covers y,x ∈ [4,8): only
(4,4) is real, so its decoded image is `94 01` followed by fifteen `CD AB`
pairs — the exact shape of §14.5's worked example, at a different fill.

**The read.** Point request (y,x) = (4,4):

1. Domain: 0 ≤ 4 < 5 for both axes ✔.
2. Ordinals: t = (4 div 4, 4 div 4) = (1,1); u = (0,0);
   s = t₀·G₁ + t₁ = 1·2 + 1 = **3**; in-tile ordinal = u₀·T₁ + u₁ = **0**;
   interleaved so disk ordinal = s = 3.
3. Index chain: segment index 3 div 2¹⁶ = 0. CRC array at
   [eo + entry_count·20, …) = [144 + 80, 228) = **[224,228)**; verify against
   crc_of_crc_array. Segment 0 at [144, 144 + min(2¹⁶,4)·20) = **[144,224)**;
   verify against array word 0. Both ranges are computable from the layer
   record alone and MAY be fetched in parallel (`[R-IDX-04]`) — here they are
   adjacent, so the "naive reader" of §15.4 coalesces them into one 84-byte
   fetch.
4. Entry: bytes [144 + 60, 144 + 80) = offset 112, length 32, crc. Not the
   sentinel; length ≠ 0; offset ≥ 16; both ≤ 2⁶³−1; 112 + 32 = 144 ≤ F − 64.
   Codec 1, so `[R-COD-04]`: length must equal the decoded size 32 — checkable
   here, before any payload fetch. ✔
5. Payload: fetch **[112,144)**, 32 bytes; CRC-32C matches the entry's crc.
6. Decode: codec 1 is verbatim; filter 1 is the identity; length is exactly 32
   (`[R-SER-07]`).
7. Extract: interleaved, so value k = u·C + c with C = 1, c = 0 → byte offset
   u·Q + F⁰ = 0·2 + 0 = 0.
8. Return: `0x0194` = 404 = my synthetic sample y·100 + x. ✔

**Cold cost of that one tile read**, on top of the open: 3 requests
(4 + 80 + 32 = 116 bytes), or 2 if the CRC array and segment are coalesced.
Whole-session total against my file: **5 requests, 303 bytes** for a 448-byte
file — i.e. the reader never fetched the three tiles it did not need.

**The decoded byte layout I ended up with**, stated exactly because my charter
asks for it: for an interleaved tile the decoded image is P·Q bytes, sample-
major, channel c's value at in-tile ordinal u at byte `u·Q + Fᶜ` where
Fᶜ = Σ_{j<c} Bʲ; for a planar numeric tile it is P·Bᶜ bytes with value k at
`k·Bᶜ`; for a planar bool plane it is ⌈P/8⌉ bytes with value k at bit `k mod 8`
of byte `k div 8`, LSB-first, and the final byte's high bits are pad bits
carrying the fill bit. There is no padding *between* values in any layout. The
byte-shuffle filter, where declared, is applied over the whole image at stride
s = Bᶜ (planar numeric) or Q (interleaved) or 1 (packed bool, hence identity),
placing byte i of group j at `i·n + j` with n = L/s; the inverse restores
`filtered[i·n + j]` to `image[j·s + i]`. I verified that inverse against
§17.3's worked example.

**Sparse and fill.** A valid sentinel short-circuits steps 5–6: no payload I/O,
and the read yields the recorded fill bit-exactly — every carried channel's
fill in declared order for an interleaved tile, the entry's own channel's fill
for a planar tile. Fill is produced by exactly one condition, a sentinel read
from a verified chain (`[R-TYP-09]`); a malformed entry, a failed segment or
array CRC, and a failed payload CRC all reject their scopes and MUST NOT return
fill (`[R-CNF-09]`). I implemented that as a hard distinction between "entry is
sentinel" and every other non-success, and the document supports it without
gaps.

---

## 5. Degradation walks

Ten traced end to end; every one is determined by the text.

1. **Unknown top-level record type, experimental (≥ 0x8000), MU = 0.** Open
   step 4 → ignore-record (`[R-CNT-15]`); the file is *conforming* (§21.6,
   `[R-CNF-02]`); the reader serves everything else, and never fetches the
   record's extent. If MU = 1 instead: reject-file, and §21.6 records that this
   is a conforming file a reader nevertheless refuses — the diagnostic ought to
   say capability, not corruption. The same type as a *sub-record* with MU = 1
   is reject-layer and never a ground to refuse the file (`[R-CNT-18]`).
2. **Unknown codec (reserved value 5) on layer B.** Layer access → L43,
   reject-layer. Layer A unaffected; the reader MAY still list B's name (§2.4).
   A verifier has *established* a violation, so its verdict is *nonconforming*,
   not *cannot establish* — `[R-COD-11]`'s cannot-establish is reserved for a
   codec it cannot **execute**, which for a conforming reader can only be an
   assigned one, and all four assigned codecs are core.
3. **Unrecognized layout value 3.** Layer access → L36, reject-layer. §10.2
   notes the layout space has no experimental range at all — 3–255 stay
   reserved — so there is no "private layout" case to consider.
4. **Truncated tail / torn commit.** The last 64 bytes are not a trailer →
   F8 at open, reject-file, and the reader MUST NOT scan backward
   (`[R-LIF-05]`). Nothing may be served. If the tail *does* parse but the file
   is longer than committed_file_length (residue past a completed commit), F17
   fires instead; §9.5's note is explicit that residue carries no row of its
   own because the reader cannot tell it from corruption.
5. **Tile checksum mismatch.** Index chain verifies, entry is well-formed,
   payload CRC fails → T1, reject-tile. That tile's read reports failure; fill
   is never a fallback; neighbours in the same layer are unaffected; and
   §15.3 is explicit that such an entry stays well-formed — its extent still
   counts in the coverage walk, in run continuity, and in the overlap rows.
6. **Segment CRC mismatch.** L38, reject-layer, detected at tile use. My reader
   sets the layer's bar, returns the values already returned, and refuses the
   request's remaining entries (§19.4 step 8).
7. **Limit exceeded.** A layer declaring entry_count = 2³³ exceeds §21.9's 2³²
   guarantee; the file stays conforming and the reader MAY decline at the
   narrowest scope whose declarations exceed what it can serve — here the
   layer — and MUST report it as a resource limit, not as corruption
   (`[R-ERR-04]`). A reader that declines a file *within* every table row on
   that ground is not conforming.
8. **Foreign format major.** Magic ✔, CRC ✔, version gate → reject-file on
   capability grounds with a diagnostic distinct from "not a TARN file" and
   "corrupt" (`[R-CNT-07]`); a verifier reports *cannot establish*. See
   finding **reader-01** — this walk is where the document stops determining
   the answer for one particular file size.
9. **User-metadata document with a duplicate key.** Extent CRC ✔, decode ✔,
   R9 → ignore-record with a SHOULD-report; every structural read is
   unaffected; the file is nonconforming, but the quarantine means no scope is
   rejected (`[R-CNT-25]`, `[R-MTA-02]`).
10. **User-metadata record at an experimental-range encoding (≥ 0x80).**
    Ignore-record; the file is *conforming*; no document rule attaches, so a
    verifier certifies and MUST report the record it ignored, naming owning
    scope, encoding value and stored extent length (`[R-MTA-10]`). Encoding 0
    and the reserved range 3–0x7F are unassigned too but *are* violations
    (R1) — §21.5's preamble is explicit that what `[R-MTA-10]` withdraws is the
    document's content rules, never the encoding byte's own value set.

---

## 6. Places I pressed and found the document sufficient

Recording these so a checker can see where I looked and came away empty.

- **`[R-ENC-05]`'s chain is closed.** Every integer I act on is covered before
  use: entry offsets/lengths by the segment CRC, the segment CRC by
  crc_of_crc_array, that by the directory CRC, that by nothing further but
  compared against a stored constant; the directory's location by the trailer
  CRC. I found no field I must act on ahead of its cover.
- **§8.1's coverage map is complete.** I enumerated every field of every
  structure and every one is covered exactly once, or is a named exception
  (front block, the three terminal checksum fields, an unassigned type's
  extent). The record extents of both *assigned* types are covered — a layer
  record's extent is the index region, a user-metadata record's carries its own
  terminal CRC.
- **The value spaces are exhaustively partitioned.** §10.3 routes all eight of
  §10.2's spaces: six value sets to a scope-level validity error, record types
  to `[R-CNT-15]`/`[R-CNT-18]`'s MU rule, metadata encoding to the quarantine.
  I checked each against its own section and the register rows match.
- **The reserved/experimental split is stated where it bites.** For the six
  value-set spaces, *both* ranges are file-conformance violations, so the split
  is invisible. It matters only for record types (§21.6's row and closing
  paragraph) and for metadata encodings (§21.5's preamble, §21.6's row) — and
  both are stated.
- **Quantifiers on the recently-worked §20.3 bar are consistent.** The bar, the
  re-declaration permission, the growth permission and the shrink permission
  are all quantified over "the generation this commit supersedes", and the text
  says so four separate times, including the two rescue questions ("a commit
  does not escape this by unstoring in the same breath"; "the tense is the
  bar's"). I constructed the awkward case — a commit that shrinks one extent
  and grows another so that entry_count is unchanged but every disk ordinal
  renumbers — and §20.3's step 4 handles it ("a geometry change renumbers
  ordinals wherever `[R-GEO-06]` moves them").
- **The "byte offset of any sample" clause.** §3.1 defines *sample* as a tuple,
  so a literal reading would leave a swap of two equal-size interleaved
  channels — with equal fills or no padding position — outside the bar's list.
  I did not report this, because §20.3 says outright that "the list names where
  that effect arises rather than standing on its own" and the operative test is
  "what §14 fixes for its stored bytes **or how they decode**", which §14.1
  does fix (value k is channel (k mod C)'s); and because §21.7 uses the same
  phrase "moving a sample's byte offset within the decoded image", showing the
  two passages mean the same thing by it. Two passages agreeing settles it.
- **§21.9's per-instance individuation.** The three per-instance rows are
  individuated explicitly ("addressed tiles, stored or not"; "documents and
  frames a file actually contains"), and the analogy it draws — "exactly as
  `[R-COD-07]`'s cap is" — is sound: `[R-COD-07]` is likewise quantified over
  addressed tiles, and both note that a layer addressing none escapes.
- **Every "exactly as / for the same reason / likewise" I could find.** I
  grepped them all out (23 sites) and put the two governing verbs side by side
  at each. `[R-MTA-09]` vs `[R-COD-11]` (verifier cannot establish), §18.2 vs
  `[R-COD-06]` (window SHOULD, undisclosed dictionary), `[R-CNT-22]` vs
  `[R-CNT-12]` (verifier-detected, reader serves unchanged), §21.9 vs
  `[R-COD-07]` (addressed tiles) all check out word for word.
- **Ordering claims.** §6.2's three-step order is a MUST; `[R-CNT-04]`'s
  "before other processing" is a MUST for a resident reader and §21.2
  acknowledges it sits ahead of §6.2's first step; §8.2's chain and §15.4's
  "dependency order" are MUSTs; §17.1's stage order is inside `[R-COD-01]` and
  restated in §19.4 step 6. The one ordering that is asserted as a consequence
  rather than stated as a rule is `[R-CNT-27]`'s — finding **reader-01**.

---

## 7. Findings

### reader-01 — AMBIGUITY — §21.2 preamble vs §5.1 `[R-CNT-27]`: nothing orders the 128-byte floor against the version gate

**Location.** §21.2, opening paragraph; §5.1, `[R-CNT-27]`; §21.2 row F5;
§6.2, `[R-CNT-06]`; §2.3, `[R-CNF-02]`.

**Quotation.** §21.2:

> A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below whose
> subject is that file's *geometry* do not reach it: §6.2 puts the version gate
> ahead of every check but the trailer magic and the trailer CRC, so such a
> file is refused on capability grounds first. Four rows are outside that
> reasoning and do reach it, because their subject is a field fixed across
> every major (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer
> CRC — the two checks §6.2 places before the gate — and F6 with F1's
> front-block instance …

and §5.1:

> No conforming file is shorter than 128 bytes: the front signature block, a
> directory of at least 4 bytes at an offset of at least 16, and the 64-byte
> trailer at a 64-aligned offset cannot be satisfied in fewer. A reader MUST
> treat a shorter file as a validity error at file scope. `[R-CNT-27]`

**The two readings.** §6.2's ordered list is: trailer magic; trailer CRC;
version gate; then, as an unordered set, nine field gates. `[R-CNT-27]`'s
128-byte check is in **none** of those positions — §6.2 never mentions it, and
`[R-CNT-27]` itself states no ordering. It is naturally performed at §19.1
step 1, the moment F is obtained, before the trailer is even fetched. So for a
file shorter than 128 bytes that declares a format major other than 1:

*Reading A* — `[R-CNT-27]`'s reader clause is unqualified, so F5 fires. The
reader reports a **validity error at file scope**; a verifier has *established*
a violation and, by §2.3's "An established violation takes priority", MUST
report **nonconforming**.

*Reading B* — §21.2's preamble excludes F5 (its subject being read as "that
file's geometry"), the version gate runs first, and the refusal is on
**capability** grounds. §6.3's SHOULD then requires a diagnostic distinct from
"corrupt", and a verifier reports **cannot establish**, since §2.3 names an
unimplemented major as exactly such a ground.

**Why the file is constructible.** `[R-CNT-24]` fixes, permanently and in every
major, only: the trailer magic at F−64, version_major/version_minor at F−56, a
CRC-32C at F−4 over [F−64, F−4), and the 16-byte front block. It does **not**
fix F mod 64 = 0 across majors — that is `[R-CNT-06]`'s major-1 gate, which
§6.2 places *after* the version gate. So an 80-byte file (front block at
[0,16), trailer at [16,80)) is a perfectly plausible future-major file, and I
built one: magic at F−64 correct, version_major = 2, CRC over [F−64, F−4)
verifying, front block byte-identical to the constant. Every gate §21.2 says
reaches such a file passes. Only `[R-CNT-27]` is left, and it says the reader
MUST treat it as a validity error.

**Which I picked, and why.** Reading B. `[R-CNT-24]`'s silence on 64-alignment
across majors is exactly the evidence that a future major could conform at
F = 80, so `[R-CNT-27]`'s floor cannot be a fact about that file's bytes; and
§21.2's preamble is normative text (§2.1 exempts only §1, *Note*/*Example*/
*Rationale*, and non-normative appendices). But I reached it by supplying the
`[R-CNT-24]` argument myself: the document nowhere says that the 128-byte floor
is major-1-specific, and F5's row cites `[R-CNT-27]` without qualification.
§21.1's own tie-break — "where a row and the rule it cites diverge, **the rule
governs**" — points the *other* way here, and the preamble is not a row, so
that clause does not reach it.

**What an implementer does wrong without it.** Places the cheap `F < 128` test
at the top of the open, which is the obvious implementation, and thereby
reports a well-formed future-major file as corrupt — precisely the failure
`[R-CNT-07]` says "misleads users into discarding files that current software
reads". A verifier built the same way returns *nonconforming* where the
document intends *cannot establish*, and pronounces a verdict on a file
`[R-CNF-02]` says this text does not judge. The repair is one clause: either
name F5 among the rows that do not reach a foreign-major file, or give
`[R-CNT-27]` an explicit position relative to §6.2's version gate.

**Byte-level: no.** Both readings reject the file, so the accept/reject verdict
is identical and no emittable byte sequence changes. What forks is (a) the
verifier's three-way verdict label, which §2.3 constrains at MUST level, and
(b) the reader's diagnostic class, which §6.3 constrains only at SHOULD level.
I am flagging it as a real defect at that grade rather than reaching for
byte-level: a disagreement between *nonconforming* and *cannot establish* is
not a disagreement about which files are accepted.

---

### reader-02 — CONTRADICTION — §23.1 assigns user-metadata editing to §20.3's shape (c), which §20.3 explicitly denies

**Location.** §23.1, `[R-PRV-01]`; §20.3, the "three shapes a commit takes"
example, shape (c).

**Quotation.** §23.1:

> and a record's extent goes the same way whether a commit drops the record
> (§20.4) or supersedes it — editing a user-metadata document appends a new
> extent and strands the old one (§20.3's shape (c)), which is the case most
> likely to strand content a caller believes it deleted

§20.3, inside shape (c):

> **(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or changing a channel's fill value on a layer with no
> padding position and no pad bit. Only the directory is re-emitted. … Editing
> user metadata is not this shape: its document lives in an extent
> (`[R-CNT-25]`), so a new extent is appended and the old one becomes slack,
> as in (b).

**The conflict.** §20.3 states in terms that editing user metadata is **not**
shape (c) and is instead shape (b). §23.1 cites it *as* shape (c). The two
sentences even agree on the mechanics — new extent appended, old one stranded —
which is what makes the citation, not the substance, the defect: §23.1 is
pointing a privacy-sensitive reader at the wrong one of three labelled figures.

**Permitted readings.** Either (i) §23.1's parenthetical names the shape the
operation takes — which §20.3 contradicts outright — or (ii) it is a pointer to
the *paragraph* in which §20.3 happens to discuss the operation, which is
indeed shape (c)'s paragraph. I picked (ii), because §20.3 is unambiguous and
§21.1's principle that a restatement yields to the rule it restates carries
over. But (ii) requires reading a shape label as a location rather than as a
classification, in a document that uses the three labels as classifications
everywhere else, including twice in §23.1's own neighbourhood.

**What an implementer does wrong without it.** Nothing on disk. But §23.1 is
the section a deployment reads to learn which operations strand data, and its
two cases are load-bearing — "Where the structure carrying the bytes leaves the
live state" versus "Where it does not". A reader who follows the pointer to
shape (c), the shape in which "Only the directory is re-emitted", lands on the
one figure that leaves nothing stranded and is told it is "the case most likely
to strand content a caller believes it deleted". That is a documentation
defect in a section whose whole purpose is to stop a tool from reporting a
commit as erasure.

**Byte-level: no.** Both passages describe the same bytes — a new extent
appended, the old one becoming slack — and neither changes what a writer may
emit or a reader must accept. §20.3 already decides the classification; only
the cross-reference in §23.1 is wrong.

---

### reader-03 — AMBIGUITY — §20.3 step 2's "MUST NOT drop the record" reads as absolute against §20.4's MU = 0 / PE = 0 licence

**Location.** §20.3, step 2 of the append procedure (`[R-WRT-04]`); §20.4's
preservation table, MU = 0 / PE = 0 row (`[R-WRT-05]`); §20.5 (`[R-WRT-06]`).

**Quotation.** §20.3, step 2:

> Against any other structure the appender carries forward, it MUST NOT repair
> the defect — `[R-LIF-01]` freezes the committed prefix — and MUST NOT drop
> the record (§20.4).

§20.4's table, MU = 0 / PE = 0 row:

> Retain byte-identical, or drop it — its extent becoming slack. An appender
> MUST NOT drop it except in a commit that *independently* changes the scope
> the record attaches to …

**The two readings.** The context of §20.3 step 2 is an appender that has met a
violation in a structure it is carrying forward.

*Reading A* — "MUST NOT drop the record (§20.4)" restates §20.4's general
preservation duty, with the citation pointing at the full rule *including* its
MU = 0 / PE = 0 exception. Dropping a defective ancillary in a qualifying
commit stays permitted.

*Reading B* — §20.3 step 2 adds an obligation that §20.4 does not carry: a
record in which the appender has *detected a defect* must not be dropped, even
in a commit §20.4 would license the drop in. On this reading an appender's only
disposal is to carry the defect forward.

**Which I picked, and why.** Reading A. Three things point to it: the clause's
own premise is "structures the appender **carries forward**", which excludes a
dropped record by construction; §20.3 step 5 hands re-emission wholesale to
§20.4 ("Re-emit the directory per §20.4"); and the bare "(§20.4)" is the
citation form this document uses for "the governing rule is over there".

**What made me hesitate, and what an implementer does wrong without it.** §20.5
states the compactor's version of this question *explicitly and in the opposite
direction*: "Dropping is the one disposal that answers, and only where §20.4's
table licenses it … Where the table does not license a drop the compactor MUST
refuse." So the document does contemplate dropping as the sanctioned response
to an undroppable-but-defective record — for a compactor. Given that the
compactor case is spelled out and the appender case is a bare "MUST NOT drop",
an implementer can reasonably read the asymmetry as deliberate and take Reading
B, and will then build an appender that can never shed a defective
experimental-range ancillary record its caller wants gone — the only records
this can arise for, since both registered types carry PE = 1.

**Byte-level: no.** The forked question is whether one *updater* may emit an
output lacking a record it could otherwise drop. It does not move the set of
conforming files: an output produced either way is a conforming file on its own
bytes, and `[R-CNF-05]` gates emission on file conformance, so neither writer
emits a nonconforming file. The cost is to updater conformance and to a
caller's ability to shed a record, not to what any reader must accept or
reject.

---

## 8. What I could not determine

Nothing beyond the three findings above. Every step of the open, every tier of
validation, every branch of the tile-read algorithm, and all ten degradation
walks resolved from the document alone, and every constant, offset and checksum
I could check reproduced exactly. The document supported an end-to-end reader
written from it and nothing else.
