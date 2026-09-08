# Cleanroom round 32 — Writer implementer, working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,754 lines), in four `Read` calls covering lines 1–4754 with no gaps. I opened no
other file, listed no directory, ran no `git` command, and issued no web request. The
brief's path was correct: `spec/tarn.md` was where it said it would be, and its line
count matched the brief's figure exactly.

Context I did not ask for **did** appear before I began: a project instruction file
pointer (`CLAUDE.md` → `AGENTS.md`), and an index of the maintainer's auto-memory with
about a dozen entry titles, several of which name TARN harness and repair topics. I did
not open any of it and I have not used any of it. I name its appearance here as the
brief requires and do not repeat its contents. Nothing below rests on it.

Everything I wrote lives in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/writer/`,
which I created. The files are:

- `wr_crc.py` — a CRC-32C (Castagnoli) implementation, table-driven, reflected in/out,
  init `0xFFFFFFFF`, final XOR `0xFFFFFFFF`. Self-checks against §4.5's check vector.
- `wr_consts.py` — recomputes every CRC constant the document states.
- `wr_reg.py` — parses §21.2–§21.5's tables out of the document and counts rows and
  instances.
- `wr_build.py` — builds a two-layer TARN file byte by byte; writes `demo.tarn`.
- `wr_read.py` — reads `demo.tarn` back as a reader/verifier would and walks coverage.
- `wr_grep.py` — a whitespace-normalising phrase search that strips `> ` blockquote
  markers before matching, so a phrase spanning a hard wrap or a blockquote prefix is
  still found. I used it for every sweep below; I confirmed on known-present phrases
  that it returns nonzero before resting anything on a zero.
- `demo.tarn` — the 640-byte file the walk produced.

I did not read the output directory.

---

## 1. Warm-up: does the document's own arithmetic hold?

Before trusting any of my own numbers I reproduced the document's.

| Quantity | Document | Mine |
|---|---|---|
| CRC-32C(`"123456789"`) (§4.5) | `0xE3069283` | `0xE3069283` |
| CRC-32C(zero bytes) (§4.5) | `0x00000000` | `0x00000000` |
| CRC of §7.4's 80-byte all-sentinel entry array | `0x80A34955`, stored `55 49 A3 80` | identical |
| §7.4's `crc_of_crc_array` over `55 49 A3 80` | `0xC4EE982E` | identical |
| CRC of a full 2¹⁶-entry all-sentinel segment (§15.4, App. B) | `0xEECB3BB2` | identical |
| Appendix A's trailer CRC over trailer `[0,60)` | `0x402F157E`, stored `7E 15 2F 40` | identical |

Hand-checked arithmetic, all confirming:

- §7.4's worked layer record: name 4 + nine scalars 34 + one dimension entry 18 + one
  channel entry 12 + trailing fixed 13 = **81**, as stated; extent length
  `4·20 + ⌈4/2¹⁶⌉·4 = 84`, as stated.
- §15.4's million-entry example: 16 segments (15 full + 16,960), CRC array 64 bytes,
  region 20,000,064 bytes, entry 999,999 at segment-relative byte 339,180, segment 15
  at `[19,660,800, 20,000,000)`, CRC array at `[20,000,000, 20,000,064)`, a full
  segment 1.25 MiB. All correct.
- §15.4's planar example: `2·32 + 10 = 74`; entry at `[1,480, 1,500)`; channel 3's
  entries 96–127. Correct.
- §11.4's ordinals: `(300,700)` → tile `(1,2)` → `s = 10`; in-tile `(44,188)` →
  `44·256 + 188 = 11,452`; planar disk ordinal `2·32 + 10 = 74`. Correct.
- §14.2's examples: `Q = 3`, decoded 18, ordinal 5 at `[15,18)`; planar `b` 12 bytes,
  ordinal 5 at 10–11; `t`+`m` → `Q = 5`, decoded 30, ordinal 5 at `[25,30)`. Correct.
- §14.3's packed plane: `0x55`, `0x01`; with fill true `0x55 0xFD`. Correct.
- §17.3's shuffle example: I recomputed the permutation from
  `filtered[i·n + j] = image[j·s + i]` with `s = 4, n = 3` and got
  `00 00 00 00 00 00 80 00 40 3F 40 40`, exactly as printed.
- §20.3's example: `32·20 + 4 = 644`. Correct.
- §21.9's note: `2³²/2¹⁶ · 4 = 256 KiB`; `2³⁶/2¹⁶ · 4 = 4 MiB`. Correct.

**Register counts.** I parsed the four register tables mechanically (`wr_reg.py`),
counting a cell of `—` as one instance and otherwise splitting on semicolons, per
§21.1's own rule ("Instances within a cell are separated by semicolons, and a cell
reading — is one instance; the count is therefore mechanical once the cell is
written"):

```
F rows: 35  instances:  56      (§21.2 says 35 conditions)
L rows: 49  instances: 116      (§21.3 says 49 conditions)
T rows: 26  instances:  55      (§21.4 says 26 conditions)
R rows: 10  instances:  50      (§21.5 says 10 conditions)
TOTAL:  120 rows, 277 instances (§21.8 says "120 conditions over 277 instances")
```

Both figures match to the unit. I also checked §21.1's specialization pairs
(F1/F6, F1/F8, F35/F36, L24/L25, F21/F22, L10/L11) and each holds: every file
exhibiting the narrower condition necessarily exhibits the wider one.

This is a document whose numbers are in order. The defects I found are in wording, not
arithmetic — which matches what the brief said the last several rounds cost.

---

## 2. Creation: a file built end to end

I built a deliberately non-trivial file: two layers of different layout, one sparse,
one with edge padding, one with a packed boolean plane, plus a file-scope
user-metadata record. Every offset below is a decision I had to make, and for each I
say whether the document fixed it or left it to me.

### 2.1 What I declared

**Layer `elev`** — rank 2, dimensions `y` (E=5, T=4) and `x` (E=5, T=4), layout 1
(interleaved), one channel `h` of type 7 (uint16) with fill `0xABCD`, linearization 1,
codec 1 (none), filter 1 (none), `A = 0`, `S = 0`, `A_slab = 0`.

- Grid `G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2)`, `N = 4`, `P = 16`, `Q = 2` (§11.2, §14.2).
- Addressed-tile count for an interleaved layer is `N = 4`, so `entry_count = 4`
  (`[R-CNT-17]`). *Fixed by the document.*
- Decoded size `P·Q = 32` bytes (`[R-SER-02]`). Under codec 1 every non-sentinel
  entry's length MUST be 32 (`[R-COD-04]`). *Fixed.*
- I stored ordinals 0 and 3 and left 1 and 2 sentinel. *My choice* — nothing obliges a
  writer to store a tile, and §13's fill machinery defines the rest. Appendix G item 6
  would forbid storing a tile whose samples all equal fill; neither of mine does.
- Tile ordinal 3 is tile coordinates `(1,1)`, covering coordinates 4–7 on both axes:
  one real position `(4,4)` and 15 padding positions. `[R-SER-05]` *fixes* their
  content: each must encode the channel's recorded fill, so values 1–15 of the value
  sequence are the bytes `CD AB`. This is §14.5's worked example, and I emitted
  exactly that.

**Layer `mask`** — rank 1, dimension `x` (E=10, T=5), layout 2 (planar), one channel
`m` of type 1 (bool) with fill `0x00`.

- `G = 2`, `N = 2`, `P = 5`. Addressed-tile count for a planar layer is `C·N = 2`
  (§11.2). *Fixed.*
- A planar bool plane packs (§14.3): decoded size `⌈5/8⌉ = 1` byte, value `k` at bit
  `k mod 8` of byte `k div 8`. Pad bits 5–7 exist because `P mod 8 ≠ 0`, and
  `[R-SER-05]` *fixes* them to the channel's fill bit — false — so they are 0.
- `E mod T = 0`, so there are no padding positions here. This matters later: a layer
  with no padding positions carries no `[R-SER-05]` witness at all.
- Tile 0 = values T,F,T,F,T → `0b00010101` = `0x15`; tile 1 = F,T,F,T,F →
  `0b00001010` = `0x0A`. Both length 1, matching `[R-COD-04]`'s equality under codec 1.

**File-scope user metadata** — one record of type `0x0002`, encoding 1 (none), a JSON
object with three `tarn.` keys. `[R-MTA-05]` *fixes* member order: ascending by the
keys' UTF-8 bytes with proper-prefix ordering first. `"tarn.created"` < `"tarn.creator"`
(they diverge at `e` vs `o`) < `"tarn.title"`. The extent is the document followed by
its 4-byte terminal CRC-32C (§8.1), so `extent_length = 94 ≥ 5` (`[R-CNT-25]`), and
`inline_length` must be exactly 1 (`[R-MTA-03]`).

### 2.2 Placement

The document leaves placement free (`[R-SLB-05]`: "its stored tiles MAY occupy any
non-overlapping byte positions, in any order"). It fixes only:

- byte 0 begins the 16-byte front signature block (§6.1), which §5.2 counts as *no
  structure*;
- every structure lies in `[16, F − 64)` (§9.7, `[R-CNT-13]`);
- structures do not overlap (`[R-CNT-02]`, `[R-CNT-13]`);
- the directory is last before the pad, with no structure between its end and the
  trailer (`[R-CNT-05]`, `[R-LIF-02]` step 3);
- the pad runs to the next 64-byte boundary (`[R-LIF-02]` step 5), and §6.2 settles the
  degenerate case explicitly — "a writer that ends its directory on a 64-byte boundary
  leaves none" — so "next boundary" means *at or after*, not *strictly after*. I would
  otherwise have had to guess; the document does not leave me to.

I chose Appendix G item 3's total order (layers in ascending name-byte order — `elev`
before `mask` — tiles in disk-ordinal order, then the layer's index region; then
remaining record extents; then the directory; each structure starting where the
previous ended) because it is the only order the document names, even though nothing
requires it. The result:

```
[0,   16)  front signature block   89 54 41 52 4E 0D 0A 1A + 8 zero
[16,  48)  elev tile ordinal 0     32 B, uint16 values 100..115
[48,  80)  elev tile ordinal 3     32 B, value 999 then 15 × CD AB (fill padding)
[80,  164) elev tile-index region  84 B = 4×20 entries + 1×4 segment CRC
[164, 165) mask tile ordinal 0     1 B  = 0x15
[165, 166) mask tile ordinal 1     1 B  = 0x0A
[166, 210) mask tile-index region  44 B = 2×20 + 4
[210, 304) user-metadata extent    94 B = 90 B JSON + 4 B CRC
[304, 552) directory               248 B = 244 B record sequence + 4 B CRC
[552, 576) pre-trailer pad         24 B  slack, zeroed by [R-CNT-03]'s advice
[576, 640) trailer                 64 B
F = 640, F mod 64 = 0
```

Directory record sequence, in Appendix G's order (type ascending; type `0x0001` tied by
layer name):

| Record | header | inline | extent slot |
|---|---|---|---|
| layer `elev` | type `0x0001`, flags `MU=1 PE=1` (§7.3 fixes them) | 95 B | (80, 84) |
| layer `mask` | type `0x0001`, flags `MU=1 PE=1` | 76 B | (166, 44) |
| user metadata | type `0x0002`, flags `MU=0 PE=1` | 1 B (`01`) | (210, 94) |

`24·3 + 95 + 76 + 1 = 244`; `dir_length = 248`.

Layer record inline payloads: I predicted 95 and 76 from §7.4's field list before
building, and the builder produced exactly those. The nine scalars from `layout`
through `channel count` are 34 bytes in both, per §7.4's own worked example.

Trailer fields, every one fixed by §6.2 except `file_id`:

```
magic 8A 4E 52 41 54 0D 0A 1A | version_major 1 | version_minor 0 ([R-CNT-26]'s floor)
flags 0 (a creator MUST write 0, [R-CNT-08]) | dir_offset 304 | dir_length 248
committed_file_length 640 | file_id 0x9E3779B97F4A7C15 (nonzero; my draw)
reserved 12 × 00 | CRC-32C over trailer [0,60)
```

`crc_of_crc_array`: `0xDB4A9A74` for `elev`, `0x0B575563` for `mask`. Both derived, not
chosen.

### 2.3 Read-back

`wr_read.py` reproduces §19.1's four-step open and §19.4's tile-read on the file:
front-block equality, trailer magic, trailer CRC, version gate, then every §6.2 field
gate; directory CRC; record walk with framing, multiplicity and extent-slot checks;
per-layer §19.3 validation including the `[R-CNT-17]` cross-checks; then per-tile
`crc_of_crc_array` → segment CRC → entry classification → stored-tile CRC. It also runs
§9.7's coverage walk. Result: ten claimants, disjoint, all inside `[16, F−64)` bar the
front block and the trailer, and a slack total of **24 bytes — exactly the pre-trailer
pad**. Nothing else in a single-generation file is slack, which is the right answer.

### 2.4 What creation left to me

Free, and I had to choose: `file_id`; placement and order of every structure; how much
slack to leave between structures (none, here); the content of slack (`[R-CNT-03]` only
advises zero); which tiles to store; tile extents and layout; codec and filter values;
record order in the directory; whether the metadata record is top-level or a
sub-record. Fixed, and I had no choice: every offset *within* a structure, every derived
count, every checksum, the padding content, the pad-bit content, the boolean byte
encoding, the flags of both registered record types, `flags = 0` in the trailer, the
64-byte trailer alignment, the pre-trailer pad's length, and `version_minor = 0`.

---

## 3. The append procedure

### 3.1 Adding a layer to the existing file

Following §20.3 (`[R-WRT-04]`) on `demo.tarn`:

1. **Establish F** — validate the trailer at the physical end (`[R-LIF-04]`). F = 640.
   On failure the file is torn and there is no append; §9.6's scan is a separate,
   deliberate operation.
2. **Open** — §19.1's four steps (`[R-RDR-01]`). Note what this does *not* establish:
   "The open establishes no tile-scope violation — it consumes the trailer and
   directory only". So an appender can be standing on a layer with a malformed index
   entry it has not looked at.
3. **Validate what the commit touches** — `[R-WRT-03]`: trailer and full directory
   always, plus §19.3 layer validation for every layer the commit modifies, plus the
   §19.4 index chain (`crc_of_crc_array` and each segment CRC) for every segment whose
   entries the commit reuses. For a pure layer-addition, that is the two existing layer
   records (they are re-emitted, so every directory byte is relied on) and no index
   chain at all — neither existing layer's index is reused, because neither is
   re-emitted.
4. **Write payloads and indexes** — writing begins at exactly 640. New layer `flux`'s
   tiles and index region go there. Neither existing layer's stored-tile set or index
   content changes, so both keep their extent slots pointing at 80 and 166
   (`[R-WRT-05]`); relocating a live index region is compaction's operation, not an
   appender's (`[R-WRT-07]`).
5. **Re-emit the directory** — complete, never a delta (§9.2's first Note). `elev`'s and
   `mask`'s records are re-emitted **byte-identically, header, inline payload and
   extent slot** (`[R-WRT-05]`); the user-metadata record likewise; `flux`'s record is
   new.
6. **Commit** — barrier; pad to the next 64-byte boundary; trailer with the *same*
   `file_id`, the new `committed_file_length`, unknown ignore-lane bits copied forward
   and no other set (`[R-CNT-08]`), `version_minor` the maximum of the floor and the
   prior trailer's minor (`[R-CNT-26]`); barrier.

The new F is at least 640 + 128: §9.2's second Note derives the floor rather than
asserting it, and I checked the derivation (directory ≥ 4 bytes at ≥ prior F, plus a
64-byte trailer, rounded up to a multiple of 64 ⇒ +128).

**Durability order.** Steps 1–3 of `[R-LIF-02]` durable *before* the pad and trailer are
written (step 4); the trailer durable last (step 6). Both barriers, not one — §20.2 and
§20.5 both say so explicitly. The commit point is step 6. §9.2 declares both barriers
*conduct* rules on `[R-CNF-02]`'s model: a file committed without a barrier can be
byte-identical to one committed with it, so the file is never nonconforming by virtue
of the omission. That is stated, and I took it as stated.

### 3.2 Appending to a file whose records I do not all understand

The document defines two record flag bits: `MUST_UNDERSTAND` (bit 0) and
`PRESERVE_ON_EDIT` (bit 1), with bits 2–15 reserved. §20.4 first fixes *which* flags
govern — "only the authoritative source of the flags differs" — and then gives the
obligation. The full walk:

**Which flags govern.**

- A type §7.3 registers (`0x0001` layer, `0x0002` user metadata): the registry's fixed
  values govern, never the stored bits (`[R-CNT-22]`). Both are PE = 1.
- A type the updater implements that this specification does not register: the
  definition it implements the type from supplies the flags; the stored bits never do.
- A type the updater does not implement: the stored flags are authoritative, with
  MU = 1 / PE = 0 read as PE = 1 (`[R-CNT-12]`).

**The obligation, by governing combination.**

| Governing | What my updater may do |
|---|---|
| MU = 0, PE = 0 | Retain byte-identical **or drop**, its extent becoming slack. §20.4 makes the licence unconditional as to occasion: "an updater MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included". SHOULD report the loss. A compactor may drop it whenever it rewrites. |
| MU = 0, PE = 1 | Retain byte-identical, **extent content unmodified**. A compactor may relocate the extent and re-point the slot, and only that (`[R-WRT-08]`, §20.5). |
| MU = 1, PE = 1 | Retain byte-identical, and **MUST NOT modify the scope the record governs**. At layer scope: that layer is frozen, other layers stay editable. At file scope: no commit at all — `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file, and the updater is a reader first. A compactor MUST refuse the whole file (`[R-WRT-06]`), because such a type can define references this specification does not. |
| MU = 1, PE = 0 | Never emitted by a conforming writer (`[R-CNT-12]`); if present, read as PE = 1, so identical to the row above. Its presence is a verifier-detected violation (F25 / L46). |
| Reserved bits 2–15 set | Readers MUST ignore; a verifier records it (F26 / L47). I carry them forward byte-identically — reproducing bytes is not authoring them, and `[R-LIF-01]` bars repair of a structure I carry forward. |
| Stored bits disagreeing with §7.3 for a registered type | I apply the fixed semantics; the mismatch is a verifier's finding (F28 / L49). If I *modify* that record it becomes new output under my writer obligations and I must emit the registry's values — so modifying silently repairs it, while carrying it forward silently propagates it. Both are stated; the document is consistent here. |

Two consequences worth stating because they surprised me and the document does answer
them:

- §20.4's MU = 1 row "reaches only a type the updater does not implement". A *layer*
  record is MU = 1 and I implement it — so for it only the PE bit bites, and §20.3
  governs how I may modify it. This is stated explicitly and I would have got it wrong
  without the sentence.
- A malformed index entry I meet while re-emitting a region is "carried forward
  byte-identically at its disk-ordinal position under step 4, not repaired to a
  sentinel" (§20.3 step 2). Note that `[R-WRT-03]`'s verification depth does *not*
  reach per-entry classification (that is §19.4 step 4, tile use), so I can reach step 4
  with such an entry unexamined; and if the commit grows an extent, the entry is
  carried to its *new* disk-ordinal position. A compactor is in the opposite position:
  regenerating a region forces it to classify every entry, so it meets the defect and
  `[R-WRT-06]` then obliges refusal.

---

## 4. Slack, by shape of commit

| Shape | What becomes slack | Who counts it | What it may contain |
|---|---|---|---|
| Append a new layer (§20.3 shape (a)) | the superseded directory, its pad, its trailer — sized by the file's *layer count*, never by any layer's data | a verifier's §9.7 walk; the total is `[R-CNT-21]`'s reporting duty | anything: "Slack has no internal structure this specification defines, its content is unconstrained, and no conformance requirement applies to it". Writers SHOULD zero (`[R-CNT-03]`) |
| Tiles added or superseded (shape (b)) | the layer's whole prior index region, every superseded payload, plus the prior directory/pad/trailer | same | same |
| Directory-only change (shape (c)) — a rename, a cleared slab declaration, a dropped PE = 0 record | the prior directory/pad/trailer, plus a dropped record's extent | same | same |
| Editing user metadata | the prior extent (a new one is appended); §20.3 places this with shape (b), and §23.1 flags it as the case most likely to strand content a caller believes deleted | same | same |
| Whole-file rewrite under a fresh `file_id` | nothing in the new file; the old file persists untouched | — | — |
| Compaction (§20.5) | nothing carried; the output's only slack is alignment gaps and its own pre-trailer pad | same | same |
| Abandoned partial write | **not slack at all.** A conforming file's size equals F (`[R-CNT-01]`), so residue past F makes the file nonconforming, caught as F8/F14/F17. §9.5's Note says exactly this: "What the residue violates is `[R-LIF-04]`'s writer obligation to truncate or overwrite" | a reader, at open | — |

Slack in my own file: 24 bytes, the pad, confirmed by the coverage walk. §5.2's rule
that only compaction reclaims it, and §22.3/§23.1's treatment of it as a security and
privacy residue rather than a defect, are consistent throughout; I found nothing wrong
in the slack machinery.

One thing worth recording as a *correctness* of the document rather than a defect:
§5.2's Note observes that of `[R-CNT-02]`'s two halves only disjointness is testable,
because the live state is *defined* as what the walk reaches. I tried to build a file
whose live state fails to partition without an overlap, and could not — the Note is
right, and there is correspondingly no register row for it. That is a place a
completeness clause could have been broken and is not.

---

## 5. Torn-write recovery: four crash points

**(a) Crash after the front block, before any structure.** Physical file 16 bytes. The
next reader: there are no final 64 bytes to fetch; §5.1's 128-byte floor makes it
reject-file (F5, `[R-CNT-27]`). The next updater: `[R-LIF-04]` requires establishing F
by validating the trailer at the physical end; that fails, so the file is torn and no
append is permitted. §9.6's probe "begins at the largest 64-aligned offset o with
o + 64 ≤ the physical file length" — there is none, so the tool reports that no
candidate survived and how many it rejected (zero). Not conforming in the meantime.

**(b) Crash mid-payload, before the directory.** Physical tail is payload bytes. Reader:
the final 64 bytes are not a trailer — F8 (magic) or, if the payload happens to carry
the magic, F14 (trailer CRC) or F17 (length cross-check). `[R-LIF-05]` forbids scanning
backward, so the reader reports the file torn and stops. Updater: torn, no append.
Recovery: probe back to the prior generation's trailer, re-verify the whole file, then
truncate. §9.2's crash figure draws exactly this state and makes the point I would have
had to reason to: the window is one in which the old state is *recoverable*, not
*readable*. Not conforming in the meantime; the prior generation is intact.

**(c) Crash after the directory, before the trailer.** Identical externally to (b) — the
tail is directory bytes. The interesting property is that step 4's barrier has already
made steps 1–3 durable, so recovery to the prior trailer is exact and the partial
commit is pure slack after re-append. Not conforming in the meantime.

**(d) Crash mid-trailer.** The final 64 bytes are partly the new trailer. If the magic
landed, the CRC over `[0,60)` almost certainly fails (F14); if the write reordered so
that the CRC landed and a field did not, the field gates catch it (F13/F17/F12/F15).
The document does not promise more than this and says so: §9.2's Note — "safety
degrades from 'torn commits are invisible' to 'torn commits are detected'". Not
conforming in the meantime.

**(e) A fifth, from `[R-LIF-04]`'s second option.** A writer may "overwrite from F and
truncate the physical file to the new committed_file_length no later than step 6". If it
crashes after the trailer is durable but before truncating, the file carries a *valid,
complete* commit plus residue. A reader sees a torn file (the tail is not the trailer)
and `[R-LIF-05]` forbids it to scan backward — but §9.6's probe finds the new trailer
immediately, since its `committed_file_length` equals its own offset + 64. So the
commit is not lost. I checked whether this needed a register row of its own: §9.5's
Note says explicitly that it does not, because the observable state is already named by
F8/F14/F17. That is right, and it closed a suspicion I opened.

**Rollback.** §9.6 is unusually careful here and I could not break it: truncating to an
earlier commit and re-appending can reproduce any committed file length at or above an
expected one, so "A signed committed file length is not among" the defences. Correct —
placement is free and slack is unconstrained, so the re-append controls the length.

---

## 6. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options (layer,
dimension and channel names; extents; tile extents; channel types and fills; layout;
codec; filter; alignment/slab). Every way their bytes may legitimately differ, and
whether Appendix G closes it:

| # | Degree of freedom | Rule that leaves it open | Closed by |
|---|---|---|---|
| 1 | `file_id` | §6.2 (any nonzero); §9.3 advises randomness only | **item 2** — derived from a hash of `[0, F−64)` plus the trailer's first 60 bytes with `file_id` zeroed. I checked for circularity: those 60 bytes contain `dir_offset`, `dir_length`, `committed_file_length` — all known before `file_id` is chosen — and exclude the trailer CRC. Well-founded. |
| 2 | Placement and order of structures | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **item 3** |
| 3 | Extent of gaps between structures | `[R-SLB-05]` | **item 3** ("each later structure begins where the previous one ended") |
| 4 | Content of gaps, including the pre-trailer pad | `[R-CNT-03]` (a SHOULD), `[R-CNT-21]` | **item 3** (zero, taken as a requirement) |
| 5 | Record and sub-record order in the directory | `[R-CNT-14]` | **item 3** |
| 6 | Compressed stream bytes under codecs 2–4 | `[R-CNF-05]`; RFC 1951/8878 constrain decoders, not encoders | **item 1** |
| 7 | DEFLATE's final-byte unused high bits | §17.2's Note says the spec constrains them nowhere | **item 1** (it names this explicitly) |
| 8 | Whether an all-fill tile is stored or left sentinel | no rule requires either | **item 6** |
| 9 | The fill recorded when the caller chooses none | `[R-TYP-10]`, a SHOULD | **item 7** (and item 7 correctly notes it compounds with item 6) |
| 10 | `version_minor` | `[R-CNT-26]`, a SHOULD | **item 8** |
| 11 | Trailer `flags` ignore lane | `[R-CNT-08]` (a creator MUST write 0; a compactor carries forward) | **item 8** |
| 12 | Number of generations / checkpoint commits | `[R-LIF-07]`, a SHOULD; §9 nowhere constrains | **item 4** |
| 13 | JSON serialisation of user metadata | `[R-MTA-05]` sorts members but not formatting | **item 9** |
| 14 | Name normalisation (NFC vs NFD) | `[R-ENC-14]`, a SHOULD | **item 10** |
| 15 | Declared alignment / slab | §16 leaves it to the writer | **item 5** |
| 16 | Filter value | §17.3 leaves it to the writer | **item 5** |
| 17 | Tile extents and layout | §11.3, §14.1 | **item 5** |
| 18 | Segment CRC constant substitution for a full all-sentinel segment | `[R-IDX-05]` | **not a divergence** — the emitted bytes are identical either way; only the writer's arithmetic differs |
| 19 | Linearization, index encoding | only value 1 is emittable | **no freedom** |
| 20 | Codec value itself (1 vs 2 vs 3 vs 4) | §17.2 leaves it to the writer | **item 1**, read as "the adopter names the encoder"; naming a zstd implementation names codec 3. Item 2's closing sentence names tiling, layout *and codec* as legitimate variation, and item 5 pins the first two while item 1 pins the third. Closed, though item 1 carries it obliquely rather than saying "a fixed codec value". |

I could not construct a divergence Appendix G leaves open. I also tried to falsify its
claims:

- **Item 5's identity claim** — "The filter is the identity exactly where its permutation
  is — where the stride is 1 … and equally where the decoded image is a single group,
  n = L/s being 1". I derived it: `filtered[i·n + j] = image[j·s + i]` is the identity
  iff `i·n + j = j·s + i` for all `i < s, j < n`. Taking `i = 0, j = 1` gives `1 = s`;
  taking `j = 0, i = 1` gives `n = 1`. So identity ⟺ `s = 1` or `n = 1`. The claim is
  exactly right, in both directions. **Not a finding.**
- **Item 2's compactor exclusion** — "re-deriving it on an already-compact input would
  reproduce the input's own `file_id`". True: a profile-compliant compaction of a
  profile-compliant compact file reproduces `[0, F−64)` and the trailer's other fields
  byte for byte, so the derived value is the input's, and `[R-WRT-06]` demands a fresh
  draw. **Not a finding.**
- **Item 3's tie-break key** — "every other type by the record's header with
  `extent_offset` masked to zero, then its inline payload, then the contents of its
  extent". I checked the self-reference argument: masking `extent_offset` is necessary
  because the order being defined is what fixes it. And two records the key does not
  separate really are byte-identical in everything but `extent_offset`, whose extents
  are emitted adjacently with identical content — so either assignment yields the same
  file, exactly as the item says. **Not a finding.**

The one soft spot I will name without filing: item 3's "The first structure begins at
16 … or, where a declared alignment admits no structure at 16, at the least position
above it the declaration admits" leaves the *content* of `[16, first structure)`
implicit — it is a gap before the first structure rather than one "between" two — and
the same item's zeroing rule is phrased over gaps alignment forces between structures.
The profile is non-normative and the intent is unmistakable; I record it as observed
and not filed.

---

## 7. The closed list of §20.3 step 4 — where the walk stopped

This is where I spent most of the second half of the walk, and it is where my findings
are.

### 7.1 Deriving the members myself

I enumerated §7.4's inline-payload fields and put each on a side, before reading the
list's own closure claim:

| §7.4 field | Side | By which words |
|---|---|---|
| name | permitted | "its name … MAY change" |
| layout | fixed | "the layout" |
| linearization | fixed | "the linearization" |
| codec | fixed | "the codec" |
| filter | fixed | "the filter" |
| alignment A | permitted | "a slab or alignment declaration MAY be declared, re-established or cleared" |
| slab S | permitted | same |
| slab alignment A_slab | permitted, **only inferentially** — the list never names it; it is reached only if "a slab declaration" means the pair (S, A_slab). §16.2 ("a slab run length S ≥ 1 with slab alignment A_slab") and `[R-CNT-23]` ("0 when S = 0") support that reading, so I took it as reached |
| rank d | fixed | "the rank" |
| channel count C | via the channel list | |
| dimension name | permitted | "its dimension and channel names, MAY change" |
| dimension extent | permitted (grow only) | "an extent MAY grow, and MUST NOT shrink" |
| dimension tile extent | fixed | "every tile extent" |
| dimension order | fixed | "the dimension order" |
| channel name | permitted | "its dimension and channel names, MAY change" |
| channel type | fixed | "every channel's type and fill" |
| channel fill | fixed | same |
| channel order | fixed for interleaved wholesale; for planar, "the position of every planar channel but the last" | |
| index_encoding | fixed | "the index encoding" |
| entry_count | neither — "entry_count and crc_of_crc_array follow the commit" | |
| crc_of_crc_array | neither — same | |
| sub-records | neither — "§20.4's subject whether or not the layer stores a tile" | |

**The closure claim holds.** "Between them the two lists reach every declaration field
of §7.4" is true on this derivation, with `A_slab` reached only by reading "a slab
declaration" as the pair. I opened that as a suspicion and closed it on §16.2's own
wording. It is the weakest joint in the closure claim but I do not think it is a defect.

The partition claim — "where a field is on both sides — a dimension extent, a planar
layer's channel list — the permitted side states the whole of what a commit MAY do to
it" — also holds on inspection: those are the only two fields the permitted side reaches
partially.

### 7.2 Taking each permitted member to its smallest legal instance

**Names.** A rename enters no decoding path. `tarn.stats` is keyed by channel name but
is advisory and cannot affect decoding (`[R-MTA-02]`). Uniqueness is re-checked
(`[R-ENC-15]`). Clean.

**A grown extent.** Smallest instance: E = 4, T = 4 (G = 1, no padding) grown to E = 5
(G = 2). The new positions live in a newly addressed, unstored tile and read as fill —
so the principle's "a grown extent adds positions that held their channel's fill" holds
even in the case where the positions were not previously *padding* at all. Second
instance: E = 5, T = 4 grown to E = 8, where positions 5–7 were padding holding fill and
become real. Also fill. The principle reaches both.

Ordinal renumbering: I worked a rank-2 case, `G = (2,3)` grown to `G = (2,4)`. Old
ordinals `(1,0),(1,1),(1,2) = 3,4,5` become `4,5,6`, and the new column takes 3 and 7.
So the re-emission clause's "byte-identical at its disk-ordinal position (a growth
renumbers ordinals wherever `[R-GEO-06]` moves them …)" is doing real work — a naive
writer that copies entries by array index rather than by tile identity silently
transposes the layer. The document says the right thing; it is easy to get wrong.

I also verified that a growth cannot renumber ordinals *without* changing `entry_count`
in an interleaved layer: extents only grow, tile extents are fixed, so every `Gᵢ` is
non-decreasing, and `N = ∏Gᵢ` unchanged with all `Gᵢ` non-decreasing forces all `Gᵢ`
unchanged — unless some `Gⱼ = 0`, in which case `N = 0` and the layer stores no tile and
is freely re-declarable anyway. §11.1's Rationale names exactly that carve-out. Clean.

**A slab or alignment declaration.** Declaring `A` on a layer that already stores tiles
cannot move committed bytes, so the writer must either be lucky or supersede every
misaligned tile. §20.3 step 4 states this — "an aligned layer's stored tiles — every one
the new state keeps, not only those this commit adds — satisfy its invariant or the
declaration is cleared" — and `[R-SLB-04]` states the slab analogue. I could not break
it. I opened one word-sense question — whether changing `A` from 512 to 4096 counts as
"declared, re-established or cleared" — and closed it: the net declaration is what the
rules bite on, and clearing-then-declaring reaches the same state, so nothing is
actually barred either way.

**A planar channel list extended or shortened at its end.** This is where the list
breaks. See §7.3 and §7.4 below.

### 7.3 Finding: the closing criterion reopens the closed list

§20.3 step 4's bounds paragraph ends:

> The list is not offered as exhaustive: a change is permitted exactly where the
> declarations it produces satisfy every rule they are subject to.

Two paragraphs earlier the same step says:

> A layer that stores a tile **in the generation this commit supersedes** keeps its
> declarations, with these exceptions and no other

and

> A commit MUST NOT change one of these; the change is a new layer, or a whole-file
> rewrite under a fresh file_id

The closing sentence states a **biconditional over "a change"**: permitted *exactly
where* the produced declarations satisfy every rule they are subject to. A fill change
produces a fill of the right element size. A re-type produces an assigned type. A
re-tiling produces tile extents ≥ 1. A transposition of the dimensions produces a valid
dimension list. Every one of them satisfies every rule it is subject to, and every one
of them is on the fixed side. Read as written, the sentence licenses precisely the
changes "and no other" forbids.

There is a rescuing reading, and I want to be honest that it exists: the paragraph opens
"A permitted change holds provided the declarations and geometry it produces stay within
every bound they are subject to", so its subject is a change already on the permitted
list, and "The list is not offered as exhaustive" refers to the *bounds* list that
precedes it, not to the permission list. Under that reading the closing sentence means
"the bounds I have named are not all of them; the real test is every rule", which is
coherent and non-vacuous.

Both readings are defensible from the words. I picked the scoped one, because the
alternative makes the closed list dead text and this is the one step of the document
that was rewritten to replace a bar with a list. But the sentence's own grammar does not
say so, and §11.1's Rationale — the same rule restated — gets the scoping right where
§20.3 does not:

> several of these in one commit, **each subject to every rule the declarations it
> produces are under**

That is a necessary condition attached to a listed change. §20.3's version turns it into
a sufficient condition over any change. A non-normative gloss stating the rule correctly
while the normative text states it loosely is the wrong way round.

**Why this forks bytes.** Take a planar layer L with C = 1, channel `a` of type float32
and fill `0x00000000`, one dimension E = 8, T = 4 — so G = 2, N = 2, `entry_count` = 2,
both tiles stored, and `E mod T = 0` so the layer has **no padding positions**. A caller
asks for the channel to be re-typed to int32 (same element size).

- Updater P follows the closing sentence: int32 is an assigned type, the fill length
  still equals the element size, `entry_count` still equals `C·N`, `extent_length` still
  equals the formula — every rule the produced declarations are subject to is satisfied
  — so it emits a directory-only commit (§20.3's shape (c)), re-emitting the layer
  record with the channel's type field changed from `0C 00` to `04 00`, keeping the
  extent slot pointing at the same, unmoved index region, and appending a directory, a
  pad and a trailer.
- Updater Q follows "and no other": a channel's type is on the fixed side, so this is a
  whole-file rewrite under a fresh `file_id` (§20.5), and it emits a different file
  end to end.

P's output is a **conforming file**: I walked it — front block, disjoint claimants, every
checksum, `[R-CNT-17]`'s cross-checks, `[R-COD-04]`'s equality (`P·B = 4·4 = 16` for both
types), and no register row applies. Because the layer has no padding positions there is
no `[R-SER-05]`/T4 witness of the old fill, and because both types have element size 4
there is no `[R-SER-07]`/T3 or `[R-COD-04]`/T14 witness of the old element size. So the
permissive reading admits a conforming file that the restrictive reading forbids the
updater to emit, and the two updaters' outputs differ in the layer record's type field
and in `file_id`. The emittable set moves.

Note that §20.3's own shape-(c) example says the opposite of P in as many words:

> A change to any fixed declaration of a layer that **stored** a tile in the generation
> the commit supersedes — a fill value, a type, a tile extent — is not an appender's
> operation at all (step 4)

so the step contains both the prohibition and, one paragraph later, a criterion that
lifts it.

### 7.4 Finding: a planar layer's tail channel can be replaced, and the principle does not reach that instance

The permitted side reads:

> a planar layer's channel list MAY be extended at its end, or shortened from its end

immediately followed by:

> A commit MAY make several of these changes at once.

and the fixed side freezes only

> the position of every planar channel but the last.

Take a planar layer with C = 2, channels `a` and `b`, `b` of type float32. A commit that
shortens from the end (removing `b`) **and** extends at the end (appending `d` of type
int32) leaves C = 2, N unchanged, `entry_count = C·N` unchanged, `extent_length`
unchanged — and `d` occupies disk ordinals `N … 2N−1`, exactly the ordinals `b`
occupied. Every element of that commit is on the permitted side, taken singly; the
question is whether "several of these changes at once" reaches two alternatives inside
one item, and whether "the whole of what a commit MAY do to it" means a *net* effect
that is one of the two or a *composition* of them. The document does not say.

Two things go wrong if it does reach.

**First, the principle does not reach the instance it licenses.** The paragraph that
justifies each permitted member says:

> an appended planar channel adds tiles at ordinals after every existing one, a disk
> ordinal being c · N + s with N the spatial-tile count

For the combined commit that is simply false: `d` is appended at index 1 because the
shortening freed index 1, so its ordinals are not after every existing one — they are
the ones the removed channel had. The justification for permitting an append is that it
cannot collide with existing stored tiles; in this instance it collides exactly.

**Second, the re-emission clause has two categories claiming the same entries.** Step 4
says a layer whose stored-tile set or index content changes re-emits its region

> with entries for tiles this commit stores or supersedes written to their new state,
> entries for tiles that become unstored written as the sentinel, entries new to this
> generation (added tiles, grown extents, an appended channel) emitted per §15, and
> every other entry byte-identical at its disk-ordinal position

For ordinals `N … 2N−1` in the combined commit, category 3 applies if the writer reads
them as belonging to an appended channel, and category 4 applies if it reads them as
disk-ordinal positions that existed in the superseded generation and whose tiles it
neither stores, supersedes, nor unstores. Category 3 has the writer emit fresh entries
(sentinels, or entries for tiles it stores now). Category 4 *obliges* it to carry the
removed channel's entries forward byte-identically — which points int32 declarations at
float32 stored bytes, with every checksum in §8 certifying the result and, as the same
step admits, "no check any actor owes able to see it".

Two conforming updaters, the same input and the same caller request, emit different
index regions and different reference arrays, both in conforming files. That is a byte
fork, and it sits inside the sentence that exists to prevent exactly this outcome:

> The line is drawn where a stored tile's meaning is fixed.

I checked whether the tense sentence closes it — "The tense is the prior generation's …
so a commit does not earn an empty layer's freedom by emptying the layer as it
re-declares it: unstoring or superseding every tile of a layer and re-declaring it is
one operation, and it is a rewrite". It closes the *empty-then-redeclare* route and says
nothing about the tail-replacement route. I checked whether the bounds paragraph closes
it: `[R-GEO-01]`'s floor of one channel bites only when the net C would be 0, and the
net here is 2.

I also checked the two-commit version (shorten in commit *n*, append in commit *n+1*,
pointing the new channel's entries at the removed channel's now-slack extents) and
decided it is **not** a defect: there the writer authors new index entries deliberately,
and nothing bars an entry from pointing at any conforming extent in `[16, F−64)`. The
defect is confined to the one-commit case, where the re-emission clause may *mandate*
the carry-forward.

**What I picked.** I would implement the restrictive reading: a commit's net effect on a
planar channel list must be an extension at the end or a shortening from the end, not a
composition, and any commit that leaves a disk ordinal addressing a different channel
than it addressed in the superseded generation is a rewrite. But the words permit the
other reading, and Appendix H's restatement — "a planar channel added or removed at the
end" — reads, if anything, more permissively than §20.3 does.

### 7.5 Finding: §13.3's sparse-writing Note is false for two permitted commits

§13.3's labelled **Note** says:

> each commit that changes a layer's stored-tile set or its index content — which, among
> the declaration changes §20.3 permits a layer that stores a tile, only a change to
> entry_count does — re-emits that layer's whole tile-index region

The parenthetical claims that among §20.3's permitted declaration changes, a change to
`entry_count` is the only one that changes a layer's stored-tile set or its index
content. Two counterexamples from changes §20.3 expressly permits:

1. **Declaring an alignment or a slab on a layer that already stores tiles.** §20.3 step
   4 requires that "an aligned layer's stored tiles — every one the new state keeps —
   satisfy its invariant or the declaration is cleared", and `[R-SLB-04]` requires the
   slab invariants be re-established or the declaration cleared. Committed bytes cannot
   move, so a writer that wants the declaration must supersede the offending tiles at
   conforming offsets. That changes the index region's entry offsets with `entry_count`
   untouched.
2. **A planar shortening combined with a growth,** which "A commit MAY make several of
   these changes at once" permits: `C` falls while `N` rises so that `entry_count = C·N`
   is unchanged, while every disk ordinal renumbers under `[R-GEO-06]`.

There is also a category error in the parenthetical: `entry_count` is not among the
declaration changes §20.3 permits at all. §20.3 puts it on neither side — "entry_count
and crc_of_crc_array follow the commit" — so it is a consequence, not a permitted
change.

The Note carries the *Note* label, so `[R-CNF-01]` makes it non-normative and
`[R-WRT-04]` step 4's own rule governs: "Every layer whose stored-tile set or index
content this commit changes has its tile-index region re-emitted in full". A writer that
took the Note as its test would skip a required re-emission and leave a layer whose
entries address the wrong tiles — a conforming file denoting the wrong array. I grade it
below byte-level for exactly the reason the brief gives: the normative rule already
decides it.

### 7.6 Finding: "`[R-CNT-17]` obliges the smaller entry_count"

§20.3 step 4, normative:

> A channel removed from the end leaves its stored tiles' extents as slack (§5.2), and
> `[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index region

`[R-CNT-17]` obliges an `entry_count` equal to the geometry-derived addressed-tile count
of the *new* declarations, which for a planar layer is `C·N`. If the same commit also
grows an extent — permitted, and expressly permitted *together* — the new `entry_count`
may be equal to or larger than the old. The consequence the sentence draws ("and so a
re-emitted index region") survives; the premise it draws it from does not. It is the
same combination that falsifies §13.3's Note, seen from the other side. `[R-CNT-17]`
itself is unambiguous, so an implementer who follows the requirement rather than the
step's gloss is safe.

---

## 8. Suspicions I opened and closed

- **"Every other declaration is fixed for as long as the layer stores a tile"** (§20.3)
  drops the "in the generation this commit supersedes" qualifier that the governing
  sentence carries. Closed by the paragraph's own tense clause four sentences later:
  "The tense is the prior generation's (§3.1 defines *stored* against a generation)".
  This is precisely the shape the brief warned dies on a clause above the sentence.
- **`[R-CNF-02]`'s closed list of expressly-declared non-violations** — "§6.3's flags
  rules … and §6.2's pre-trailer gap … are the cases this text states". I swept for
  every other candidate: §9.2's barriers (a *conduct* rule under the same requirement's
  first half, not this list), §10.3's experimental-value prohibition (also conduct,
  cited in the first half), `[R-LIF-04]`'s truncation duty (its residue *is* a
  file-conformance violation, F17). No fourth case. Closed clean.
- **Is a §20.3-violating commit's output a nonconforming file?** It has no register row,
  and the evidence of the violation lives in slack. Closed by §9.6 ("For a verifier the
  probe is diagnosis … not a finding about the file it was given") and §9.7's Note
  ("Nothing here enumerates prior commits"): no obliged check separates such a file, so
  §21.7's unwitnessed test excuses the missing row and no verifier's verdict turns on it.
- **`[R-WRT-09]`'s "each relocated extent's checksum, including every stored tile's entry
  crc"** — I suspected a compactor that relocates nothing for a layer might skip that
  layer's tile CRCs and so carry a bad tile forward where another compactor would
  refuse. Closed by the governing clause immediately before it: "it relies structurally
  on **every structure it copies**", and §20.5 has it copying every stored tile's bytes
  verbatim. The scope is every stored tile.
- **§20.3 shape (c) says an empty layer is re-declared "subject to every rule its new
  *geometry* is subject to"** where the normative sentence says "its new
  *declarations*". A narrowing — but every declaration rule (`[R-COD-03]`,
  `[R-COD-09]`, `[R-SER-06]`, `[R-TYP-03]`, `[R-GEO-05]`) binds unconditionally, so the
  narrower phrasing costs an implementer nothing. Observed, not filed.
- **`A_slab` never named on either side of the closed list.** Closed by reading "a slab
  declaration" as the pair (S, A_slab), which §16.2 and `[R-CNT-23]` support.
- **Whether changing `A` from 512 to 4096 is "declared, re-established or cleared".**
  Closed: the rules bite on the net declaration, and clear-then-declare reaches the same
  state, so no operation is actually barred by the verb list.
- **§23.1's "no commit turns a real position of a stored tile into padding"** — I tested
  it against every permitted change. A real position becomes padding only if an extent
  shrinks, and shrinking is a rewrite. True.
- **§23.1's "the bytes a commit makes unreachable always leave the live state whole"** —
  structures are claimed whole by an extent slot or an index entry, so no partial
  departure is expressible. True.
- **The `[R-LIF-04]` "overwrite then truncate" transient**, where a completed commit's
  file is briefly longer than `committed_file_length`. Closed by §9.5's Note: the
  observable state is already named by F8/F14/F17 and needs no row.
- **Appendix G item 1 and the codec value.** I suspected the profile pins the encoder
  without pinning which of codecs 1–4 is used. Closed: naming a codec implementation
  names the codec, and item 5's parallel pinning of layout and tile extents cites item
  2's closing sentence, which names codec alongside them.
- **`[R-CNT-05]`'s "a longer gap is conforming, and no conforming commit produces one"**
  — I checked this against `[R-CNF-02]`, which names it as one of the two expressly
  declared non-violations. Consistent.
- **Whether "pad to the next 64-byte boundary" means +64 when already aligned.** Closed
  by §6.2: "a writer that ends its directory on a 64-byte boundary leaves none".

---

## 9. Confidence

Creation, the append procedure, the record-flag walk, slack accounting and torn-write
recovery I found fully determined by the document; I built a file, read it back, and
walked coverage without once having to guess. The byte-divergence catalogue is closed by
Appendix G item for item, and its two non-obvious claims (the filter-identity
characterisation and the compactor's exclusion from the derived `file_id`) are both
correct on derivation.

The four findings all live in §20.3 step 4 and its restatements — the step the brief
said had been rewritten most and read hardest, and the one whose closed list is this
round's surface. Two of them (writer-01, writer-02) fork emittable bytes; two
(writer-03, writer-04) are false glosses that the requirements they gloss already
decide.
