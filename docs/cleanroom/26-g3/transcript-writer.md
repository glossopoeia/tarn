# Cleanroom round 26 — Writer implementer transcript

## 0. Disclosure

**Files read: exactly one — `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.** I read
it whole, in six `sed`/`cat -n` chunks. I ran no `git` command, listed no directory, fetched
nothing, and opened no ADR, plan, register, vector, or conformance artifact. Every other command I
ran was local computation over data I typed myself: a CRC-32C implementation, an instance-counting
script over the register tables extracted from that one file by regex, and a file-builder that
emits a candidate TARN file into my own scratch directory. The spec file was found exactly where
the brief said it would be.

**Context I did not ask for, and did not act on.** Material appeared in my context before I began:

- a `CLAUDE.md` pointer to `AGENTS.md` (contents not read);
- a memory index listing six memory-file titles, several TARN-specific (e.g. one about a naming
  constraint on published rationale, one about a working cadence, one about §21 and a corpus build
  list). I opened none of them;
- a git status block carrying the subjects of the five most recent commits. Two of those subjects
  name sections and identifiers this round's brief deliberately withheld reasons for — one names
  §11.1 and `[R-SLB-03]` and characterises what each edit did; one names §21.2; one states last
  round's byte-level count.

That is a disclosed breach of the round's independence, not one I chose but one I have to report.
Concretely: I already had §11.1 and §16.2 on my list because the brief names them among the seven,
and shapes 6 and 7 in the brief point straight at them. The one place the leaked material could
have steered me is §11.1's `entry_count` keying. I record here that I chased that lead hard and
concluded **against** what the leaked subject line suggests — §11.1's growth claim survives under
its natural reading (§3.6 below proves it) — and that my §11.1 finding is about a different word
in the same paragraph, reached by the word-census method the brief describes. I also checked
`[R-SLB-03]` for a dangling pronoun and found none. I have not repeated any leaked content beyond
what is necessary to name the breach.

I did not read the output directory.

---

## 1. What I built

A byte-layout walk of a conforming **creator**, then an **appender**, then a **compactor**, in the
order the bytes actually leave the writer. Everything below is either (a) a value the document
fixed, cited; (b) a value I chose, with the freedom named; or (c) a place I had to stop and decide
something the document does not decide, which becomes a finding.

I built one file end to end in Python and verified every checksum in it. I also verified every
checksum constant the document states, because a writer that cannot reproduce them cannot write a
file at all.

### 1.1 The document's constants, checked

| Constant | §  | Document | Computed |
|---|---|---|---|
| CRC-32C(`"123456789"`) | §4.5 | `0xE3069283` | `0xe3069283` ✓ |
| CRC-32C(zero bytes) | §4.5 | `0x00000000` | `0x0` ✓ |
| CRC of a full 2¹⁶-entry all-sentinel segment | §15.4 | `0xEECB3BB2` | `0xeecb3bb2` ✓ |
| §7.4 example: segment CRC over 4 sentinel entries | §7.4 | `0x80A34955` | `0x80a34955` ✓ |
| §7.4 example: `crc_of_crc_array` | §7.4 | `0xC4EE982E` | `0xc4ee982e` ✓ |
| Appendix A trailer CRC | App. A | `0xE00938D2` | `0xe00938d2` ✓ |

CRC-32C parameters taken only from `[R-ENC-09]`: Castagnoli, reflected in and out, init
`0xFFFFFFFF`, final XOR `0xFFFFFFFF`, stored little-endian. The reflected table constant
`0x82F63B78` is the reflection of `0x1EDC6F41`; the document gives the unreflected polynomial and
says "reflected input and output", which is enough. Every constant reproduces. **The document's
arithmetic is sound and an implementer can bootstrap from it alone.**

I also re-derived §7.4's worked layer-record payload by hand: name 4 + nine scalars 34 + one
dimension entry 18 + one channel entry 12 + trailing fixed 13 = 81, and its extent length
4·20 + ⌈4/2¹⁶⌉·4 = 84. Both match. §11.2's, §11.4's, §14.2's, §14.3's, §14.5's, §15.4's and
§21.9's worked numbers all check (ordinals 8, 10, 11 452, 74; offsets 15, 10, 25; `0x55`/`0x01`
and `0x55`/`0xFD`; 16 segments with the last covering 16 960 entries; region 20 000 064 bytes;
segment 15 at [19 660 800, 20 000 000); 2¹⁶ segments × 4 = 256 KiB at 2³² entries, 4 MiB at 2³⁶).

---

## 2. Creation: a byte-layout walk

### 2.1 The file I chose to write

Not minimal — Appendix A already gives the minimal one, and it teaches nothing about padding,
sentinels, mixed channel types, or record extents. Mine:

- one layer `grid`, rank 2, **interleaved**, linearization 1 (row-major — the only value a writer
  may emit, `[R-GEO-05]`), codec 1 (none), filter 1 (none), `A` = 0, `S` = 0, `A_slab` = 0;
- dimensions `y` (E=5, T=4) and `x` (E=5, T=4). `[R-GEO-03]`: G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2),
  N = 4, P = 16;
- channels `t` (float32, fill `00 00 00 00`) and `m` (bool, fill `01`). `[R-SER-02]`: Q = 4 + 1 = 5,
  decoded size = P·Q = **80** bytes; F_t = 0, F_m = 4;
- `entry_count` = N = 4 (interleaved, `[R-GEO-03]`); index region length =
  4·20 + ⌈4/2¹⁶⌉·4 = **84** (`[R-CNT-17]`);
- tiles 0 and 3 stored; tiles 1 and 2 sentinel;
- one **file-scope** user-metadata record, encoding 1, document `{"tarn.title":"demo"}` (21 bytes).

Tile 3 is the interesting one: tile coordinates (1,1) covers y∈[4,8), x∈[4,8), of which exactly
one position — (4,4) — is inside the extents. The other **15 are padding positions** (§11.3), and
`[R-SER-05]` fixes their content: for every one, channel `t`'s recorded fill bytes and channel
`m`'s recorded fill byte. So tile 3's 80-byte decoded image is 5 bytes of real sample followed by
15 × `00 00 00 00 01`. That is a writer obligation with a verifier detector (T4), not a reader
one, so it is the single easiest thing for a creator to get silently wrong.

### 2.2 Emission order and the offsets

`[R-LIF-02]`'s creation path (§9.2, second paragraph): front block first, then steps 2–6 with
writing beginning at **offset 16**, generation 1.

| Bytes | What | Fixed by | Or my choice |
|---|---|---|---|
| [0, 16) | front signature block `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes | `[R-CNT-04]`, §6.1 — "Writers MUST emit exactly these 16 bytes" | fixed |
| [16, 96) | tile 0 payload, 80 bytes | length fixed by `[R-COD-04]` (codec 1 ⇒ length = decoded size) | **offset mine** (`[R-SLB-05]`) |
| [96, 176) | tile 3 payload, 80 bytes | same | **offset mine** |
| [176, 260) | tile-index region: 4 × 20-byte entries then one 4-byte segment CRC, no padding | §15.1, length by `[R-CNT-17]` | **offset mine** |
| [260, 285) | user-metadata extent: 21 document bytes + 4-byte terminal CRC | §7.1 (extent_length ≥ 5), §8.1 | **offset mine** |
| [285, 441) | directory: layer record (127) + user-metadata record (25) + 4-byte CRC = 156 | §7.1, §7.2 | **offset and record order mine** (`[R-CNT-14]`) |
| [441, 448) | pre-trailer pad, 7 bytes | `[R-LIF-02]` step 5: pad to the next 64-byte boundary; content unconstrained, zeroed by `[R-CNT-03]`'s advice | length fixed, content advisory |
| [448, 512) | trailer | §6.2 | fixed |

F = **512**. Checks I performed as the writer, in the order the reader will: F mod 64 = 0 ✓;
F ≥ 128 (`[R-CNT-27]`) ✓; dir_offset = 285 ≥ 16 ✓; dir_length = 156 ≥ 4 ✓;
dir_offset + dir_length = 441 ≤ F − 64 = 448 ✓; no structure between 441 and 448 (`[R-CNT-05]`) ✓.

Computed values, all from my own CRC-32C:

```
tile 0 crc            0x479F35AC
tile 3 crc            0x3ECAB22A
segment CRC (80 B)    0x5B63F2F1
crc_of_crc_array      0xBC790D6F
metadata document crc 0x1273F874
directory CRC         (over the 152 record bytes)
trailer CRC           0x7D6EC749
```

Layer record inline payload = **103** bytes, packed in §7.4's table order with no alignment or
padding between fields (`[R-CNT-18]`):

```
  0  04 67 72 69 64             name: length 4, "grid"
  5  01                         layout 1 = interleaved
  6  01 00                      linearization 1
  8  01 00                      codec 1 = none
 10  01 00                      filter 1 = none
 12  00 x8                      A = 0
 20  00 x8                      S = 0
 28  00 x8                      A_slab = 0 (forced by S = 0, [R-CNT-23])
 36  02                         rank d = 2
 37  02 00                      channel count C = 2
 39  01 79 | 05 x8 | 04 x8      dim "y": extent 5, tile extent 4
 57  01 78 | 05 x8 | 04 x8      dim "x": extent 5, tile extent 4
 75  01 74 0C 00 04 00 00 00 00 channel "t": float32, fill length 4, +0.0
 84  01 6D 01 00 01 01          channel "m": bool, fill length 1, 0x01
 90  01                         index_encoding 1
 91  04 00 00 00 00 00 00 00    entry_count = 4
 99  6F 0D 79 BC                crc_of_crc_array
```

Record framing: type `0x0001`, flags MU=1/PE=1 (**fixed by the registry**, `[R-CNT-22]`, §7.3 —
not a writer choice, and the stored bits are authoritative only for types the consumer does not
implement), inline_length 103, extent slot (176, 84). Total record 127 bytes.

The user-metadata record: type `0x0002`, flags MU=0/PE=1 (registry-fixed), inline_length **exactly
1** (`[R-MTA-03]` — "A record whose inline_length is not 1 is a validity error"), inline payload
the single byte `01` = encoding 1, extent slot (260, 25). The document must be a JSON object,
UTF-8, no BOM, members sorted ascending by their keys' UTF-8 bytes (`[R-MTA-05]`); one member, so
sorting is trivial.

### 2.3 What the document fixed, and what it left to me

**Fixed, no writer latitude:** the 16 front bytes; the trailer magic and layout; version_major = 1;
reserved trailer bytes zero; flags = 0 for a creator (`[R-CNT-08]`); F a multiple of 64;
dir_length ≥ 4 and dir_offset ≥ 16; the directory's terminal CRC and every other checksum; the
20-byte entry layout and disk-ordinal order (`[R-IDX-01]`, `[R-GEO-06]`); the sentinel's exact 20
bytes; the segment size 2¹⁶ and the CRC array's placement immediately after the entry array with
no padding; `entry_count` = the geometry-derived addressed-tile count; `extent_length` = the
`[R-CNT-17]` formula; codec-1 stored length = decoded size; the decoded tile image's value order
and byte offsets; padding content; the pre-trailer pad's *length*; the registered types' flag bits;
linearization 1; index_encoding 1.

**Left to me:** file_id (any nonzero — I used `0x9E3779B97F4A7C15`; `[R-LIF-03]` only *SHOULD*s a
cryptographically random draw); version_minor (SHOULD be 0 here, `[R-CNT-26]`); the placement of
every tile, index region and record extent (`[R-SLB-05]`); the size and content of every gap
(`[R-CNT-03]` advises zero, "no conformance requirement rides on slack content either way");
dir_offset; record order in the directory (`[R-CNT-14]`); which of tiles 1 and 2 to store versus
sentinel where their samples are all fill; the tile extents; the layout; the codec and filter; the
alignment/slab declarations; whether to emit user metadata at all; the JSON serialization inside
the document (`[R-MTA-05]` fixes member order and nothing else).

Nothing in creation forced me to guess. §20.2 (`[R-WRT-02]`) is a faithful consolidation of
`[R-LIF-02]`'s creation path — including the point that step 4's and step 6's barriers are **both**
owed, which a naive implementer would collapse into one.

One micro-observation I did not raise to a finding: §20.2 cites "§5.2's coverage classes
(`[R-CNT-02]`, `[R-CNT-03]`)", but `[R-CNT-03]` is the zero-the-gaps advice, not a coverage class.
It misleads nobody.

---

## 3. The append procedure

### 3.1 Establishing F, and the reliance depth

`[R-LIF-04]`: validate the trailer in the final 64 bytes of the **physical** file per §6.2. Note
what that buys: §6.2's field gates already include "committed_file_length equals the file size",
so if validation succeeds the physical file cannot be longer than F. The "physical file longer
than F" branch of `[R-LIF-04]` is therefore reachable **only** by way of §9.6 recovery whose
output has been re-verified but not truncated. §20.3 step 1 says exactly that. Good — that is a
non-obvious consequence and the document states it rather than leaving it derived.

`[R-WRT-03]` fixes verification depth by reliance: trailer and **full directory always** (because
re-emission relies on every directory byte), plus §19.3 layer validation for every layer the
commit modifies, plus the §19.4 index chain for every segment whose entries the commit reuses.
Structures the commit neither modifies nor relies on impose nothing. So an appender adding a new
layer to my file must CRC and parse the whole directory, but need not touch `grid`'s index chain
at all.

### 3.2 Commit 2 — add a layer `mask`

Layer `mask`: rank 1, dim `x` (E=3, T=4) ⇒ G = 1, N = 1, P = 4; interleaved, one bool channel `b`,
fill `00`; Q = 1; decoded size 4; entry_count 1; index region 20 + 4 = 24. Tile 0 stored.

Write order, `[R-LIF-02]`:

1. begin at exactly F = 512;
2. new tile payload at [512, 516); new index region at [516, 540). Order within step 2 is free —
   "in any order satisfying §5.2's coverage classes";
3. the **new complete directory** at 540: `grid`'s record re-emitted **byte-identically** including
   its extent slot (176, 84) and its `crc_of_crc_array` (`[R-WRT-05]`), the user-metadata record
   re-emitted byte-identically including its extent slot (260, 25), plus `mask`'s new record;
   then the directory CRC;
4. **barrier**;
5. pad to the next 64-byte boundary, then the trailer: generation **2**, the **same** file_id,
   committed_file_length = the new end, ignore-lane bits copied forward (`[R-CNT-08]` — none here),
   version_minor per `[R-CNT-26]` (max of the floor and the prior minor = 0);
6. **barrier**. This is the commit point.

Slack created: the old directory [285, 441) = 156, the old pad [441, 448) = 7, the old trailer
[448, 512) = 64. **227 bytes, sized by the file's layer count and nothing else.** `grid`'s tiles
and index region did not move: `[R-WRT-05]`, and §5.1's example says so in words — "a layer the
commit does not touch keeps its extent slot pointing where it always pointed".

### 3.3 Commit 3 — supersede tile 0 of `grid`

New payload appended; `grid`'s **whole** index region re-emitted (all 84 bytes, necessarily at a
new placement because `[R-LIF-01]` freezes the old one): entry 0 re-pointed with a new crc,
entries 1 and 2 the sentinel byte-identically, entry 3 byte-identical **at its disk-ordinal
position**, segment CRC recomputed, `crc_of_crc_array` recomputed. That makes `grid`'s layer
record *modified* — its extent_offset and its `crc_of_crc_array` both change — so it is new output
under the writer's obligations, not a byte-identical re-emission.

Slack created: the superseded 80-byte payload, the old 84-byte index region, plus the previous
directory/pad/trailer. This is §20.3's "a commit's cost is dominated by its index, not its data".

### 3.4 The record-flag walk — every combination the document defines

Record flags are a `u16`: bit 0 MU, bit 1 PE, bits 2–15 reserved (§7.2). The authoritative source
of MU and PE differs by whether the updater implements the type (§20.4, first paragraph), so the
matrix is (implements? × MU × PE × top-level/sub-record).

**A. Type the specification registers (`0x0001` layer, `0x0002` user metadata).** The registry's
fixed flags govern, *not* the stored ones (`[R-CNT-22]`). Layer = MU 1 / PE 1, user metadata =
MU 0 / PE 1. Both PE = 1, so **neither can ever be dropped**; §20.4's closing paragraph draws the
conclusion: "No commit therefore removes a layer record, or a user-metadata record at either
scope." A stored bit that disagrees with the registry makes the file nonconforming (F28, L49,
detector *verifier*) but changes no conforming behaviour: my updater applies the fixed semantics
and re-emits the record byte-identically, disagreeing bit and all, unless it modifies the record —
in which case, as new output, it must write the registry's values.

What PE = 1 means for a type the updater *implements* is "cannot be dropped", not "extent content
unmodified": §20.4's table row with that wording is scoped to types the updater does **not**
implement, and §20.3's shape (c) explicitly permits editing user metadata by appending a new
extent and stranding the old. I had to read the paragraph before the table twice to be sure of
that scoping; it holds — "Persistence governs every record type; only the authoritative source of
the flags differs", and for registered types the extracted obligation is "neither can be dropped".

**B. Type the updater implements that this specification does not register** (experimental range,
or a type registered by a later minor). "the definition it implements the type from supplies the
flags, and the stored bits never do." I note without raising it to a finding that §10.3 gives the
experimental range no collision protection, so an updater implementing *some* experiment's
`0x8001` may drop a record whose stored PE bit said otherwise. The document has already priced
this ("two unrelated experiments MAY select the same value, and nothing in this format
distinguishes them") and forbids publishing such files.

**C. Type the updater does not implement — the stored flags are authoritative.**

| Stored | Top-level | Layer sub-record |
|---|---|---|
| MU=1, PE=1 | Retain byte-identical. **No commit is available at all** — `[R-CNT-15]` makes an unimplemented top-level MU=1 record reject-file, and the updater is a reader first. Compaction barred on the same ground (`[R-WRT-06]`). | Retain byte-identical; **that layer** may not be modified; every other layer stays editable (`[R-CNT-18]`). The layer record as a whole is still re-emitted byte-identically into the new directory. |
| MU=1, PE=0 | Read as PE=1 (`[R-CNT-12]`, "never silently deletable"); collapses into the row above. | Same. |
| MU=0, PE=1 | Retain byte-identical, **extent content unmodified**. The extent may not be relocated by an appender: `[R-WRT-08]` allows relocation "only … under §20.5", and `[R-LIF-01]` makes moving committed bytes impossible anyway. | Same. |
| MU=0, PE=0 | Retain byte-identical, **or drop it** (extent → slack) — but only in a commit that *independently* changes the file's layer set, any layer record's content, or another non-layer top-level record. Dropping is not itself such a change, so a commit whose only effect would be the drop MUST retain it. A compactor may drop it whenever it rewrites. | Same, with the qualifying changes being *that layer's* record, the entry set of its index, or which of its tiles are stored. |
| any reserved bit 2–15 set | Readers MUST ignore; verifier flags F26/L47. My updater re-emits the record byte-identically, reserved bits and all. If it *modifies* the record, the new output must carry zeros there. | Same (L47). |

Two things I checked rather than assumed. First, §20.4's licence "an appender superseding a tile
MAY drop a top-level such record, or such a sub-record of the layer whose tile it superseded" is
consistent with the table's own conditions: superseding re-places the index region, which moves
the layer record's extent slot, which *is* a change to "any layer record's content" (top-level
case) and to "that layer's record" (sub-record case). The three sub-clauses of the sub-record
condition are in fact redundant — every change to the entry set or the stored set forces the index
region to move and hence the layer record to change — but redundancy is not a defect.

Second: for an unknown MU=1 **sub-record**, the appender's block is not established at the open.
§19.1's open consumes trailer and directory only; sub-records are parsed at layer access (§19.3),
which `[R-WRT-03]` demands only for layers the commit modifies. So an appender that never touches
that layer never meets the block, and its byte-identical re-emission of the layer record is
untroubled — even though re-emission "relies on every directory byte". That distinction (relying
on directory *bytes* ≠ layer *access*) is load-bearing and the document draws it cleanly.

### 3.5 Carrying a defect forward

§20.3 step 2 is unusually explicit and I record it because it is the rule most likely to be got
wrong: "a malformed index entry an appender meets while re-emitting a region is carried forward
byte-identically at its disk-ordinal position under step 4, **not repaired to a sentinel**", and
"Reproducing a structure's bytes unchanged is not authoring them". So my appender re-emits a
`length = 0` entry verbatim into the new region, emits a nonconforming file, and is still a
conforming appender — with a SHOULD to report. A compactor in the same position must **refuse**
(`[R-WRT-06]`, and §20.5's regeneration paragraph, because a structurally-rejected entry gives it
"no stored extent for a re-pointing to target" and no drop is available for a tile-index entry).
The asymmetry is deliberate and stated.

### 3.6 Where I pushed on §11.1 and §20.3 step 4, and what survived

§11.1's Rationale asserts: "Growth that leaves **entry_count** unchanged touches the directory
alone" and "Growth that changes entry_count changes extent_length with it". The brief's shape 6
("a rule keyed to a quantity that does not decide it — ask what a single commit may do at once")
points here, so I tried to break it.

*Pure extent growth.* Every Eᵢ non-decreasing ⇒ every Gᵢ = ⌈Eᵢ/Tᵢ⌉ non-decreasing. If
entry_count = C·∏Gᵢ is unchanged and nonzero, then no Gᵢ changed (a non-decreasing family with an
unchanged nonzero product is constant), so no disk ordinal moves and the index needs nothing. If
entry_count is unchanged and zero, some Gⱼ was and remains 0, so no index region exists at all —
which is the em-dash example the passage gives. **The claim is a theorem for pure extent growth.**
It survives.

*Compound commits.* It does not survive a commit that grows an extent **and** drops a channel from
a planar layer: C = 4 with N = 2 (entry_count 8) → C = 2 with N = 4 (entry_count 8), where the
surviving channels' tiles move from disk ordinals c·2+s to c·4+s. entry_count holds still while
its factors move, and the index region *must* be re-emitted with entries at new positions. Whether
that commit is permitted turns on a question §20.3 does not answer (finding **writer-06**).
Because §11.1's sentence says "Growth", and a channel drop is not growth, I do **not** raise the
sentence itself as a defect. I raise the gap that makes the compound commit possible.

*Grow-one, shrink-another.* I also tried extents (4,2)→(2,4) with T = (2,2): entry_count and the
ordinal *numbering* both hold (ordinal 1 is still ordinal 1), but ordinal 1 now denotes a different
spatial tile. Under §20.3's bar nothing §14 fixes for a stored tile changes — same padding set
(none), same decoded size, same in-tile offsets, same codec and filter — so the commit is
permitted, the writer may keep the index byte-for-byte, and "touches the directory alone" is
literally true. The tile's *content* is silently reassigned to different coordinates, which is
data the caller chose to reinterpret; §20.3 says "Discarding data is the caller's operation and
this specification does not bar it." No finding.

*The word `last`.* §11.1's closing clause bolds one word. That is finding **writer-01**.

---

## 4. Slack, by commit shape

`[R-CNT-21]`: every byte the live state does not claim is slack, its content is unconstrained, no
conformance requirement applies to it, a reader MUST NOT interpret it, and a **verifier that
reaches a live state MUST report the total**. Only compaction reclaims it.

| Commit shape | Bytes that become slack | Counted by | May contain |
|---|---|---|---|
| **Creation** | the pre-trailer pad, plus any gap the writer leaves between structures. In my file: exactly the 7-byte pad — claimed 505 of 512. | verifier | anything; writers SHOULD zero (`[R-CNT-03]`) |
| **Append — new layer/record** | the previous directory, its pad and its trailer. **Sized by the file's layer count, never by any layer's data** (§20.3's shape (a)). | verifier | anything |
| **Append — in-place update (supersede a tile)** | the above, plus every superseded payload, plus that layer's **entire** previous index region — 20·entry_count + 4·⌈entry_count/2¹⁶⌉ bytes for a one-entry change. | verifier | anything |
| **Append — directory-only change** (rename, clear a slab, change a fill on a layer with no padding position and no pad bit) | the previous directory, pad and trailer only. Editing user metadata is **not** this shape: its document lives in an extent, so a new extent is appended and the old one is stranded (§20.3 shape (c)). | verifier | anything |
| **Shrink** | the de-addressed tiles' extents, plus the old index region (`[R-CNT-17]` obliges a new entry_count). Where the shrink turns real positions into padding of a tile the new state *still stores*, **no bytes leave the live state at all** — they stay inside the tile as padding content, which §20.3 permits only where they already hold the recorded fill. §23.1 states both cases and calls them exhaustive; I could not construct a third. | verifier | anything (case 1); fill, mandated (case 2) |
| **Rewrite / compaction** | nothing is *carried*: the output holds only what is reachable from the input's live trailer, less any record §20.4 licenses dropping. The output still has its own slack — the pre-trailer pad and any alignment gaps — so a compacted file's slack total is generally nonzero, and "slack is never carried" is about the input, not the output. The **input persists unmodified** until something outside this specification deletes it (`[R-PRV-02]`). | verifier, on the output | pad/gap content, advisory zero |
| **Abandoned partial write** | **none.** The bytes past F are not slack, because there is no live state: the physical tail is not a valid trailer, so §6.2's ordered validation rejects before any F is established, and `[R-CNT-21]` says the slack total "is not owed at all … which is not a partial total but the absence of one". `[R-LIF-04]` obliges the next writer to truncate to F or overwrite from it. §9.5's Note confirms residue carries no register row of its own — a reader meets it as F8, F14 or F17. | nobody | n/a — the file is nonconforming until repaired |

The verifier's total is **partial** — an upper bound, never an under-count — wherever a scope-level
rejection ends an enumeration or the verifier stopped at the first violation, and it must then say
which scope or violation stopped the walk. I checked the monotonicity claim: discarding a rejected
layer's already-enumerated claimants makes "claimed" smaller and the reported total larger, so the
upper-bound property holds. ✓

---

## 5. Torn-write recovery — four crash points

Throughout: the commit point is **step 6**, the barrier that makes the trailer durable. Before it,
the previous generation is intact and the file is recoverable but not readable.

**Crash A — after step 1, during step 2 (payloads written, no directory).** Physical length
L > F_n. The final 64 bytes are payload residue.
*Next reader:* the tail is not a trailer. `[R-CNT-06]` fails — on the magic (F8) in the ordinary
case, on the trailer CRC (F14) if the residue happens to carry the magic, on the length
cross-check (F17) if it carries both. reject-file. `[R-LIF-05]` forbids scanning backward.
*Next updater:* `[R-LIF-04]` — the file is torn, MUST NOT append; recovery is a separate,
deliberate operation.
*Conforming?* **No.** `[R-CNT-01]` requires the file size to equal the live trailer's F, and there
is no live trailer at the tail.
*Recovery:* §9.6 probes backward from the largest 64-aligned o with o + 64 ≤ L, requiring magic,
CRC, and committed_file_length = o + 64. It finds trail_n at F_n − 64, since F_n mod 64 = 0.
Truncating to F_n restores the file **exactly** — that is the return on never modifying a
committed byte.

**Crash B — after step 3, before step 4's barrier.** Payloads, index and directory are written but
not durable. Same reader/updater outcome. If the barrier is weaker than assumed and the trailer
lands while the directory does not, §9.2's Note is right that §8's chain still catches it loudly:
the directory CRC over garbage fails ⇒ F20 ⇒ reject-file. I checked the one pathological case —
stale all-zero bytes with dir_length = 4 would "verify", since CRC-32C of zero bytes is
`0x00000000` — and it is harmless, because dir_length = 4 means the commit's directory *was*
empty, so the zeros reproduce the intended content exactly.

**Crash C — mid-trailer, in step 5.** The tail is a partial trailer. Magic may be present, CRC
almost certainly not ⇒ F14. Same outcomes as A.

**Crash D — trailer fully written, step 6's barrier not completed.** Two sub-cases, and the
document distinguishes them: if the trailer is durable, the commit *happened* — a reader sees the
new generation, and the physical size equals the new committed_file_length only if `[R-LIF-04]`'s
truncation is also done. That is why `[R-LIF-04]` puts the truncation "no later than step 6" and
not after it: on the overwrite-from-F path the truncation is what makes the commit visible, so a
crash between the trailer write and the truncation leaves a torn file that recovery finds at the
*new* F. If the trailer is not durable, the file reverts to crash A/B.

**Crash E, extra — a payload that mimics a trailer.** §9.6 makes this normative for tools: "a tile
payload can deliberately contain a byte string that mimics a valid trailer, so recovery output
MUST be re-verified as a whole file (§8) before being trusted", the tool continues past a
candidate whose re-verification fails, and MUST report the candidate it settled on and how many it
rejected. Under live-state coverage a mimic sitting in slack is inert — nothing enumerates it
(§21.6, §22.3). I confirmed a torn file's tail can never *be* a verbatim earlier trailer: trail_n
sits at F_n − 64, and the tail at [L−64, L) coincides with it only when L = F_n, i.e. when the
file is not torn.

**Is a torn file conforming in the meantime?** No, in every case: the final 64 bytes are not a
valid trailer, so `[R-CNT-01]`/`[R-CNT-06]` fail. And `[R-LIF-06]`'s second caution is the honest
one — truncation to an earlier commit boundary is *indistinguishable in-format* from that earlier
version, so rollback detection needs out-of-band state.

---

## 6. Byte-divergence catalogue, and Appendix G item by item

Two conforming writers, identical input arrays, identical stated options (tiling, layout, channel
set and types, codec choice, metadata content). Every legitimate way their bytes can differ, and
whether the reproducible-writer profile closes it:

| # | Degree of freedom | Rule that leaves it open | Closed by |
|---|---|---|---|
| 1 | Encoder choices inside a codec — DEFLATE block/table choices and the up-to-seven unconstrained high bits of its final byte; zstd frame options (Frame_Content_Size present or not, Single_Segment vs Window_Descriptor); LZ4 match choices | `[R-CNF-05]`; §17.2's DEFLATE Note; `[R-COD-06]` "MAY be present" | **G1** (codec 1, or a named implementation at a named version with fixed settings — level, strategy, thread count) |
| 2 | `file_id`: any nonzero value | §6.2, `[R-LIF-03]` (randomness is a SHOULD) | **G2** for a creator; explicitly **left open for a compactor** (item 8 concedes "reproducible only modulo its trailer") |
| 3 | `version_minor` | `[R-CNT-26]` is a SHOULD | **G8** |
| 4 | Ignore-lane `flags` bits | `[R-CNT-08]` MUSTs 0 for a creator but declares a set bit *not* a file-conformance violation (§2.3) | **G8** for a creator; a compactor carries the input's forward |
| 5 | Placement of every tile, index region and record extent; their relative order | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **G3** |
| 6 | Gap **extent** (how much space between structures) | `[R-SLB-05]` | **G3** ("each later structure begins where the previous one ended, save where alignment forces a gap") |
| 7 | Gap **content** | `[R-CNT-03]` is advisory | **G3** ("every byte of every such gap is zero — `[R-CNT-03]`'s advice, taken as a requirement here") |
| 8 | `dir_offset` | `[R-CNT-06]` bounds only | **G3** (directory last) |
| 9 | Record order in the directory, and sub-record order in a layer record's payload | `[R-CNT-14]` — "Record semantics MUST NOT depend on record order" | **G3**, with a total key (type; layer records tie by name; others by header with `extent_offset` masked to zero, then inline payload, then extent contents) |
| 10 | Whether an all-fill tile is stored or sentinel | nothing requires either | **G6** |
| 11 | The fill recorded when the caller chooses none | `[R-TYP-10]` is a SHOULD | **G7** — and G7 correctly notes this reaches further than eight bytes, because item 6 makes the *set of stored tiles* depend on it |
| 12 | Declared alignment / slab / `A_slab` | §16 leaves them to the writer | **G5** |
| 13 | Filter value (1 or 2) | `[R-COD-09]` | **G5** |
| 14 | Name normalization (NFC vs NFD — a different name *and* a different length, so a different `inline_length` and `dir_length`) | `[R-ENC-14]` is a SHOULD | **G10** |
| 15 | User-metadata JSON serialization (number formatting, escaping, whitespace); storage encoding 1 vs 2; zstd settings for encoding 2 | `[R-MTA-05]` fixes member order only and says so | **G9** |
| 16 | Number of generations used to reach the same content | §9 nowhere constrains it | **G4** |
| 17 | Pre-trailer pad *length* | — | **not** a divergence: `[R-LIF-02]` step 5 fixes it, and `[R-CNT-05]` states that a longer gap is conforming but "no conforming commit produces one" |
| 18 | Segment CRC of a full all-sentinel segment | `[R-IDX-05]` lets a writer emit the constant "without computing it" | **not** a divergence: the constant equals the computed value (verified: `0xEECB3BB2`) |

**Falsification attempts against G, and their results.**

- *Is G3's record ordering key total?* I tried to break it. Two records the key does not separate
  share type, flags, `inline_length`, `extent_length`, inline payload and extent contents; they
  differ only in `extent_offset`, which the key masks. Swapping them swaps both the header order
  and the extent order, and because the extents are equal-length and equal-content the resulting
  byte sequence is identical. **G's claim holds.** The masking rationale ("a key containing it
  would depend on its own result") is correct.
- *Is G3's "first structure begins at 16" right under a declared alignment?* With A = 512 the
  first *stored tile* must sit at 512, so [16, 512) is an alignment-forced gap and G3 zeroes it. A
  layer that declares A but stores no tile has an index region as its first structure, which A
  does not constrain, so 16 is admitted. The phrase "where a declared alignment admits no structure
  at 16" reads correctly once you know A binds stored tiles only; I flag it as a soft edge, not a
  finding.
- *Does G4 conflict with `[R-LIF-07]`?* `[R-LIF-07]` SHOULDs checkpoint commits for very large
  single commits; G4 pins one generation. A profile adopter deviates from a SHOULD, which
  `[R-CNF-12]` puts outside the register entirely. No conflict with conformance.
- *Does G close item 12 and 13 in its own closing summary?* **No — item 13 is missing.** Finding
  **writer-04**.
- *Is item 5's justification true?* **No.** Finding **writer-05**.
- *Does G leave anything else open?* One thing, which I do not raise: §18.4's `tarn.created` and
  `tarn.creator` are writer-synthesised values a caller may not supply, and nothing in G pins them.
  A writer adopting the profile simply omits them; the keys are OPTIONAL. Not a defect.

**Every divergence I found is either closed by G or expressly conceded by it (item 2 for a
compactor).** That is a real result and it should be recorded as one.

---

## 7. Findings

### writer-01 — AMBIGUITY. §11.1's bolded "last" has two live readings that disagree

*Location:* §11.1, the Rationale block under `[R-GEO-02]`.

> Growth that changes entry_count changes extent_length with it (`[R-CNT-17]`), so the layer's
> whole tile-index region is re-emitted and disk ordinals renumber wherever `[R-GEO-06]` moves
> them (§20.3, `[R-WRT-04]`) — the growth that raises a zero-extent layer's **last** zero grid
> count included.

Reading A — "the last zero grid count *remaining*", i.e. the one whose raising finally makes
∏Gᵢ nonzero. Under A the clause is true: entry_count goes 0 → C·N, extent_length changes with it,
the index region comes into existence.

Reading B — "the *last-declared* dimension's zero grid count". This is the document's own house
sense of "last": `[R-GEO-05]` defines row-major as "the **last-declared** dimension varies
fastest", §16.2's Note says "under row-major, a run is a band along the **last-declared**
dimension", and the bare word elsewhere is consistently positional-in-a-sequence — "the last row
of tiles" (§11.2), "the last value" (§14.3), "the last complete record" (F29), "the last three
rows" (§21.9). I censused every occurrence; not one uses "last" to mean "final remaining".

The readings disagree for any layer with **two or more** zero grid counts. Take G = (0, 5, 0) and
grow E₂ so G₂ = 3. Under reading B this is "the last zero grid count", so the clause says
entry_count changes — but N = 0·5·3 = 0 still, entry_count is unchanged, and the sentence has
placed the commit under the wrong one of its two halves. Under reading A it is not "the last" at
all and the preceding sentence governs, correctly.

I picked reading A: the immediately preceding clause ("a growth raising one grid count while
another stays 0 among them") sets up the contrast, and only A makes the sentence true. But the
bolding is what makes this reportable — the word is emphasised precisely because it is
load-bearing, and it is emphasised in the one sense the document never elsewhere uses.

*What an implementer does wrong without it:* believes a growth raising the last-declared
zero-extent dimension forces a tile-index re-emission, looks for a region to re-emit on a layer
whose entry_count is still 0, and finds `[R-CNT-17]` and §7.4 forcing extent (0, 0) and
`crc_of_crc_array` = 0 instead. Self-correcting, which is why I grade it as I do.

*Byte-level:* **No.** The block is a *Rationale* and so non-normative under `[R-CNF-01]`, and
`[R-CNT-17]`, `[R-CNT-23]` and `[R-WRT-04]` independently fix what a writer emits under either
reading. No conforming implementation's emitted bytes or accept/reject verdict moves.

### writer-02 — OBSERVATION. §13.3's Note restates §20.3's re-emission rule short by one disjunct, and "stored-tile set" carries two senses

*Location:* §13.3, "Note — sparse writing"; against §20.3 step 4 (`[R-WRT-04]`).

The Note:

> each commit that changes a layer's stored-tile set, or that grows its extents so that
> entry_count changes, re-emits that layer's whole tile-index region (§11.1, §20.3,
> `[R-WRT-04]`).

The rule it cites:

> Every layer whose stored-tile set **or index content** this commit changes has its tile-index
> region re-emitted in full

The Note drops "or index content" and narrows the extent clause to *growth*. Two commit shapes
fall through: (a) **superseding a stored tile's bytes**, which leaves the stored-tile set exactly
as it was — the same tiles are stored — while changing the entry's offset and crc; and (b) a
**shrink** that changes entry_count, which `[R-CNT-17]` obliges just as growth does.

The phrase itself is the problem. I censused all six uses. Two pair it with the second disjunct
and are precise — §5.1's example ("A commit that changes a layer's stored-tile set **or index
content** re-emits that layer's whole tile-index region") and §20.3 step 4 itself. §20.4 uses the
precise sense a third time, listing "which of its tiles are stored" as one trigger among three and
routing a supersede through a *different* trigger ("Superseding a stored tile's bytes re-places
that layer's index region … and so modifying that layer's record"). `[R-SLB-04]` uses the precise
sense and covers supersedes with a separate clause ("or the byte placement of any run"). But
§20.3's own Note uses it loosely — "any change to a layer's stored-tile set re-emits that layer's
whole tile-index region, so editing one sample of a 10⁶-tile layer appends about 20 MB of index" —
where editing one sample *is* a supersede. So the house sense is the precise one, four uses to
one, and §13.3's Note is short under it.

*What an implementer does wrong without it:* an updater built from §13.3's Note treats a supersede
as index-neutral, or treats a shrink as index-neutral, and does not re-emit. Both are caught
downstream — a superseded payload at a new offset with a stale entry simply is not a supersede,
and a shrink that changes entry_count trips `[R-CNT-17]`'s extent_length equality — so the error
is self-correcting rather than latent.

*Byte-level:* **No.** The Note is non-normative (`[R-CNF-01]`), §20.3 step 4 governs, and neither
mistaken writer can emit a nonconforming file — it emits a *pointless* one whose new payload is
unreferenced slack. No verdict moves.

### writer-03 — OBSERVATION. §21.7's account of unwitnessed obligations omits `[R-LIF-02]` step 3

*Location:* §21.7 (`[R-ERR-01]`), second paragraph; against §9.2 (`[R-LIF-02]`) step 3 and its Note.

§21.1 designates §21.7 as the account of what fails the register's detectability gate — "§21.7 the
account, by class, of what fails it". §21.7's second paragraph opens:

> A second set of obligations is omitted from the register because a single file exhibits no
> witness of their violation. Committed-prefix immutability and the generation sequence
> (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not
> reconstruct;

and goes on to cite `[R-GEO-06]`/`[R-SER-01]`, `[R-CNT-13]`'s no-embedded-offsets prohibition,
`[R-CNT-18]`'s nesting prohibition, §20.3 step 4's bar, §20.5's four trailer obligations, and
`[R-ENC-06]`'s field widths. `[R-LIF-02]` appears nowhere in it — although §9.2 states its step 3
obligation and then singles out the exact way a writer violates it:

> **Note.** Step 3 is not discharged by a directory an earlier generation appended: each commit
> appends its own complete directory, and the trailer of step 5 addresses that one. A writer that
> re-points a new trailer at a prior generation's directory region has left step 3 unperformed.

I constructed that file to check it is genuinely unwitnessed. Commit n+1 appends payloads at F_n,
skips step 3, and writes a trailer with generation n+1 and `dir_offset` = D_n. The result: the
live directory is dir_n; the newly appended payloads are reachable from nothing, so under §5.2
they are **slack, not structures**, and `[R-CNT-05]`/F7 (which bars a *structure* between the
directory's end and the trailer) does not bite; `[R-CNT-06]`'s bounds hold, since D_n ≥ 16 and
D_n + dir_length ≤ F − 64; `[R-CNT-02]`'s partition holds; every checksum verifies; the generation
counter is correct. **A verifier certifies it.** The only observable is a large slack total, which
§5.2 makes an operational signal and not a verdict. This obligation is a property of the file's
history in exactly the sense the paragraph's own first sentence names, sits in the same section as
the two rules it does cite, and is the one a writer is most tempted to skip — a no-op "touch"
commit that bumps the generation can save its whole directory by re-pointing.

*Permitted readings and my choice:* either (i) the citation list is illustrative and the class
"properties of a file's history" already covers step 3, or (ii) the list is the account and is
short. §21.1's "the account, by class" supports (i) more than I would like, which is why I grade
this an OBSERVATION rather than pressing it harder. But a reader auditing §21.7 against §9 will
find `[R-LIF-01]` and `[R-LIF-03]` cited by identifier and their sibling in the same requirement
family absent, and will not know whether that absence means "covered by the class" or "witnessed
somewhere I have not found".

*Byte-level:* **No.** Nothing about the verdict on any byte sequence changes: the offending file is
conforming under either reading, and the obligation binds the writer either way.

### writer-04 — OBSERVATION. Appendix G's closing enumeration omits the one freedom item 5's second half closes

*Location:* Appendix G, closing paragraph.

> The items above add what is not, and the list is not short: gap *content*, which `[R-CNT-03]`
> only advises; gap *extent*, which placement freedom (`[R-SLB-05]`) leaves open; record and
> sub-record order, which `[R-CNT-14]` leaves free; the fill a writer records when its caller
> chooses none (`[R-TYP-10]`, a SHOULD); the sentinel for every all-fill tile, which no rule
> requires; a single generation, which §9 nowhere constrains; the absence or fixing of a declared
> alignment and slab, which §16 leaves to the writer; `version_minor` at its floor, which
> `[R-CNT-26]` states as a SHOULD — item 8's creator's rule, not a compactor's (§20.5); a derived
> `file_id`, where §9.3 states only advice; NFC-normalized names, which `[R-ENC-14]` states as a
> SHOULD; and the producer pinning of items 1 and 9.

I walked the ten numbered items against that sentence. Every half of every item is named except
one: **item 5's fixed filter value**. Item 5 reads "**No declared alignment and no slab**, or fixed
declared values … **A fixed filter value** likewise", and the closing sentence names only "the
absence or fixing of a declared alignment and slab". The filter is a real, independent degree of
freedom — `[R-COD-09]` lets a writer emit 1 or 2, the choice is implied by no content, and it
changes both the layer record's `filter` field and (for most layer shapes) every stored tile's
bytes.

The paragraph's own disclaimer is "Read the numbered items as the list; this paragraph names what
they are for, not how many there are." That disclaims the *count*, not the *membership*: the
paragraph undertakes to name what the items are for, and for one half of one item it does not.
Deriving the members from the items rather than from the sentence is the only way to notice.

*What an implementer does wrong without it:* an adopter auditing their profile implementation
against the summary paragraph rather than the numbered items ships a writer that leaves the filter
unpinned and produces different bytes from another adopter's.

*Byte-level:* **No.** Appendix G is explicitly non-normative and "adds no requirement to any
actor"; both files remain conforming, and `[R-CNF-05]` already promises no canonical bytes.

### writer-05 — CONTRADICTION. Appendix G item 5 says byte-shuffle changes every tile it touches; §17.3 says it is the identity at stride 1

*Location:* Appendix G item 5, against §17.3 (`[R-COD-10]`) and §20.3 step 4.

Appendix G item 5:

> **A fixed filter value** likewise: §17.3 leaves the choice to the writer, it changes the stored
> bytes of every tile it touches, and no content implies it, so two writers agreeing on everything
> else still disagree on bytes without it pinned.

§17.3 (`[R-COD-10]`):

> The shuffle stride s is the channel's element size for a planar tile and the sample stride Q for
> an interleaved tile (§14.2); for a packed boolean plane s = 1 and the filter is the identity.

At s = 1 the transform "byte i of group j at offset i·n + j" has i ≡ 0, so it maps offset j to
offset j: the filtered image equals the decoded image, byte for byte. That is not a corner case. It
holds for every packed planar bool plane (stated outright), for every planar plane of a
1-byte-element channel (int8, uint8, bool), and for every interleaved layer whose sample stride
Q = 1 — a single uint8, int8 or bool channel. For all of those, filter 1 and filter 2 produce
**identical stored tile bytes**, so the filter changes the stored bytes of *no* tile it touches.

§20.3 step 4 relies on precisely this, in normative text, when it lists what the declaration-change
bar does not reach:

> a change that leaves every one of those tiles' stored bytes meaning exactly what they meant — a
> filter whose mandated stride makes it the identity (`[R-COD-10]`) …

So the document knows the identity case in its normative text and denies it in its appendix.

*Permitted readings and my choice:* one could read "every tile it touches" as "every tile whose
bytes it in fact alters", making the sentence a tautology. I reject that: the sentence is offered
as the *reason* the filter must be pinned, and a tautology supports nothing. The intended claim is
the false one. The item's conclusion survives anyway — the layer record's `filter` field differs
(`01` versus `02`), so two writers still disagree on bytes — but by a mechanism the item does not
state.

*What an implementer does wrong without it:* concludes that a filter change on a stride-1 layer is
byte-visible in the tiles and, under §20.3 step 4, treats such a change as barred for a layer with
stored tiles — when §20.3 expressly permits it.

*Byte-level:* **No.** Appendix G is non-normative, §17.3 and §20.3 govern, and the disagreement
does not alter which files are conforming or which a reader accepts.

### writer-06 — AMBIGUITY. §20.3 step 4 never says whether a commit may change a layer's channel set or rank

*Location:* §20.3 step 4 (`[R-WRT-04]`).

The bar is stated over declarations generally:

> A commit MUST NOT change a layer's declarations in a way that alters, for any tile that layer
> stores **in the generation this commit supersedes**, what §14 fixes for its stored bytes or how
> they decode — the set of padding positions (§11.3) and the content `[R-SER-05]` fixes there, the
> decoded size, the byte offset of any sample within the decoded tile image, or the codec and
> filter that produced the stored bytes.

Every worked permission and carve-out that follows is about **extents**: "an extent MAY **grow**",
"An extent MAY also **shrink**", and the de-addressing carve-out is tied to a grid-count fall —

> Dropping a tile out of the addressed set (§11.2's grid count falls) is not itself such an
> alteration — a tile the new state does not address carries no §14 obligation and its extent
> becomes slack

Nothing anywhere says whether a commit may change **C** (channel count) or **d** (rank), and in a
**planar** layer a channel drop de-addresses tiles the superseded generation stored without any
grid count falling. Concretely: a planar layer with C = 4 numeric channels and N = 2 addresses
8 tiles at disk ordinals c·N + s (`[R-GEO-06]`). Drop channel 3. For every surviving tile the
decoded size P·Bᶜ is unchanged, the padding set is unchanged, the in-plane byte offset k·Bᶜ is
unchanged, and the codec and filter are unchanged — so the bar's enumerated list is untouched. But
channel 3's two tiles *were* stored in the superseded generation, and §14 now fixes nothing for
them at all.

Two defensible readings:

- **(A) Permitted.** The general principle the shrink paragraph states — "a tile the new state does
  not address carries no §14 obligation" — is not restricted to grid-count falls, so the
  de-addressed channel's tiles carry no obligation and their extents become slack, exactly as for
  a shrink. The bar is a prohibition; what it does not prohibit is allowed.
- **(B) Barred.** The bar quantifies over "any tile that layer stores in the generation this commit
  supersedes" — which includes channel 3's tiles — and ceasing to fix a decoded size for a tile
  *is* altering what §14 fixes for it. The document says so explicitly for extent shrinks precisely
  because the reading is otherwise available; the absence of an equivalent sentence for a channel
  drop is then meaningful.

I picked **(A)**, because the carve-out's stated *reason* is general and because §20.3's shape (c)
already contemplates channel declarations changing ("changing a channel's fill value"). But I had
to supply the extension of the parenthetical myself, which is the test the brief sets: this is a
rule whose correctness rests on a step the document does not take.

The stake is not academic for an updater. Under (A) a single commit may **grow an extent and drop a
planar channel at once** — C = 4 with N = 2 → C = 2 with N = 4 — leaving `entry_count` = C·N
unchanged at 8 while every surviving channel's tiles move from disk ordinal c·2 + s to c·4 + s.
The tile-index region must then be re-emitted with entries at new positions even though
`entry_count`, `extent_length` and `crc_of_crc_array`'s *size* all hold still. That is the one
operation which separates `entry_count` from its factors, and it is reachable only by doing two
things the document permits in the same commit. §20.3 step 4's own normative trigger — "stored-tile
set **or index content**" — catches it correctly; §11.1's Rationale, keyed to `entry_count`, does
not describe it (see §3.6 above, where I show §11.1's sentence survives because it says
"Growth").

*What an implementer does wrong without it:* an updater built on reading (B) refuses a legitimate
caller request (drop a channel from a planar layer that stores tiles) and forces a whole-file
rewrite; one built on reading (A) performs it and must know to re-emit the index region under the
"index content" trigger rather than the `entry_count` one.

*Byte-level:* **No**, and I want to be precise about why rather than reach. Under (B) the commit is
barred, but §21.7 already establishes that the bar has no file-level witness where the affected
tiles leave the live state — "a commit that supersedes every tile it would have damaged leaves the
live state clean, so the bar is unwitnessed there". De-addressed tiles leave the live state, so the
output is a conforming file under both readings, no verifier verdict moves, and no reader accepts
or rejects differently. What the ambiguity costs is an updater's behaviour toward its caller, not
bytes on disk.

---

## 8. What I could not determine, and what I deliberately did not raise

- Whether a commit may change a layer's **rank** is the same gap as writer-06 and I folded it in;
  I checked that a rank change adding or removing a dimension with T = 1 in a position that leaves
  P, the in-tile ordinal and the spatial ordinal all fixed is permitted under either reading, so
  the ambiguity bites only where the change de-addresses stored tiles.
- I could not construct a third case in §23.1's "two cases are exhaustive" claim about where
  unreachable sample bytes end up. I tried supersedes, unstores, extent shrinks that de-address,
  extent shrinks that turn real positions into padding, channel drops, fill changes, metadata
  edits and record drops; every one lands in case 1 (the structure leaves the live state) or case 2
  (a still-stored tile's padding). The claim holds.
- §20.5 keys index-region regeneration to "each **relocated** tile-index region" while the actual
  driver is whether that layer's *tiles* moved. In a whole-file rewrite "relocated" plausibly means
  "placed by the compactor", i.e. all of them, and `[R-MDL-02]`'s reference-array equality forces
  the right behaviour under either reading. I decided this was not a defect and left it out rather
  than pad the list.
- Appendix G does not pin the *content* of writer-synthesised standardized keys (`tarn.created`,
  `tarn.creator`). Those keys are OPTIONAL and a profile adopter simply omits them. Not a defect.
- The status of writer obligations with no file-level witness — `[R-LIF-01]`, `[R-LIF-02]`,
  `[R-LIF-03]`, §20.5's four, `[R-WRT-05]`'s byte-identical re-emission — sits uneasily against
  `[R-CNF-02]`'s "file conformance is a pure predicate on bytes": a byte sequence cannot be both
  conforming and not depending on who produced it. §2.3 draws the conduct/predicate line and names
  two express cases; §21.7 handles the rest as violations with no witness whose "verdict is
  unaffected". The two accounts land in the same place operationally (the verifier certifies), so
  I raise only the concrete omission (writer-03) and not the framing.
- **Register arithmetic.** I extracted all 121 rows mechanically and counted instances by §21.1's
  stated rules (a `—` cell is one instance; otherwise semicolon-separated). Result: F 36 rows / 58
  instances, L 49 / 116, T 26 / 55, R 10 / 48 — **121 rows over 277 instances**, matching §21.8
  exactly. I spot-audited the direction rule (L21, L22, L30, T3, T14, T22 all enumerate both
  directions of a "does not equal"; L37, L38, T1 enumerate none, correctly, a checksum comparison
  having no magnitude ordering; L44, T21 enumerate one, correctly, for an "exceeds"/"larger than"),
  the layout rule (L44, T3, T14, T21, T22, T26 all enumerate the three layout formulas), and L2's
  derived-quantity list against §11.2/§14.2/§14.3/§15.1 — I could find no derived quantity it
  misses (⌈P/8⌉, Gᵢ, Q, the in-tile ordinal and the spatial ordinal are each dominated by a listed
  term). **The counts are right.**
- §21.2's "36 conditions", §21.3's "49", §21.4's "26", §21.5's "10", §15.3's "Six rows are marked
  *structural*", §22.3's "Four residues", §17.2's "Three frame features are excluded", §12.1's
  "exactly thirteen sample types" and "twelve … numeric types", §2.3's "five classes",
  §10.1/§4.3's "four vehicles", §20.5's "the other seven spaces … (L31, L33, L34, L36, L43, L45,
  R1)", §21.7's "§20.5's four obligations", §6.3's "the remaining 48 trailer bytes" and §21.9's
  "The last three rows are per-instance" all check out against the text they account for.
