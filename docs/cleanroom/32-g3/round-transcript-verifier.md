# Cleanroom round 32 — Verifier implementer, working transcript

## 0. Disclosure and apparatus

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,754 lines, 47,314 words by `wc`). I opened no other file in the repository,
ran no `git` command, listed no directory, and did no web access. The file was
where the brief said it would be.

Context I did not ask for **did** appear before I began: a project instruction
file (`CLAUDE.md`, pointing at `AGENTS.md`) and an index of the maintainer's
auto-memory notes with a dozen entry titles, several naming this project's
harness and prior-round failure modes. I did not open any of the files it
indexed and I have not used any of its content as evidence. I name its
appearance here as the brief requires and do not repeat its contents.

Everything I wrote went to my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/verifier/`:

| file | what it does |
|---|---|
| `crc32c_check.py` | CRC-32C from the polynomial the document states; the check vector, the two §7.4 example constants, the all-sentinel segment constant |
| `appA.py` | parses Appendix A's 128-byte hex dump and re-derives every field and its trailer CRC |
| `count_instances.py` | parses §21.2–§21.5's tables and counts rows and Instances cells |
| `buildfile.py` | builds a complete conforming two-record file byte-exactly (`file1.tarn`) and runs the §9.7 coverage walk on it |
| `flat.txt` | whitespace-normalised, `> `-stripped single-line rendering of the whole document, for phrase search across hard wraps |
| `adversarial.py` | slab / alignment / overlap invariants on a hostile planar layout |
| `trace.py` | four-generation trace with the slack arithmetic at each generation |

**Search hygiene.** The document is hard-wrapped and blockquotes wrap with
`> ` inserted, so a line-oriented `grep` reports false zeros. I built `flat.txt`
first and searched that. My first control phrase returned **0** — because I had
mis-remembered the phrase, not because the text was absent — which is exactly
the failure the brief warns about. I re-ran with five phrases I had just read
verbatim; all five returned 1. Every zero I rest anything on below was taken
against that flattened text with a matching positive control.

---

## 1. What I built

A conforming verifier, on paper, as an ordered algorithm. I state it first,
then walk each part against a file I constructed byte-exactly.

### 1.1 The certification procedure

The verdict vocabulary is `[R-CNF-11]`'s three: *conforming*, *nonconforming*,
*cannot establish*, plus two report-only markers — *unexamined* (a scope the
verifier elected not to look at, `[R-CNF-11]`) and *advisory* (a SHOULD
deviation observed in passing, `[R-CNF-12]`). Neither marker is a verdict.

Availability, derived rather than quoted, because `[R-CNF-11]` states two of
the three and leaves *conforming* to fall out:

- **nonconforming** iff the verifier has *established* at least one violation.
  It dominates: "a verifier that has established any violation reports
  *nonconforming*, however many requirements it was unable to check".
- **cannot establish** iff no violation established **and** at least one
  requirement was unable to be checked on a capability or resource ground.
  The grounds list in `[R-CNF-11]` is introduced by "as when" and is therefore
  open — which matters, because a whole-layer resource decline (§9.7,
  `[R-ERR-04]`) is not on the list and needs the general clause to reach it.
- **conforming** iff no violation established **and** nothing left unchecked.
  §9.7 supplies the second conjunct directly: "a verifier MUST NOT certify past
  a violation it has not looked for."

Three things bar certification and they are distinct: an established violation;
an unchecked requirement; and an incomplete traversal. `[R-CNF-11]` licenses
stopping early **only** at the first violation, so an incomplete traversal that
is not a resource/capability wall always coincides with case 1.

The ordered algorithm:

```
V0. Front block.        Verify [0,16) by byte equality.  A verifier has no
                        residency exemption ([R-CNT-04] gives one; §2.3
                        withdraws it, F1/F6).           -> reject-file
V1. Trailer, in order.  magic; trailer CRC; version gate; then, gates passed,
                        the flag gates, F == transport size, F mod 64 == 0,
                        dir_offset >= 16, dir_length >= 4,
                        dir_offset+dir_length <= F-64, file_id != 0,
                        reserved zero.   ([R-CNT-06], [R-CNT-07], [R-CNT-08])
                        A failure here means NO live state: [R-CNT-21] then
                        owes no slack total at all -- "not a partial total but
                        the absence of one".
V2. Directory CRC.      ([R-CNT-11])  Then parse the record sequence.
V3. Record walk.        Framing, MU gate, multiplicity, extent slots, layer
                        name namespace.  ([R-CNT-12..15], [R-ENC-15])
                        Verifier-only here: F25/F26 flag bits, F28 stored-flag
                        mismatch, F36 reserved-range type.
V4. Per layer.          §19.3's full record validation, then the index chain
                        ([R-IDX-04]), then per entry §15.3's eleven rows.
                        Verifier-only: L18 intra-layer overlap, L40/L41/L42
                        alignment and slab, L46/L47/L49 flag bits, L25.
V5. Decode every        [R-SER-07] exact decoded size; [R-COD-08] exact
    stored tile.        consumption; codec header rows T17-T23; then the
                        decoded-content obligations T2 (interleaved bool),
                        T4 (padding positions), T5 (pad bits), T26 (stride).
V6. Every record        Terminal CRC (R2), then the document rules R3-R10 at
    extent.             an assigned encoding.  At an experimental encoding:
                        no content rule attaches; report the record and move
                        on ([R-MTA-10]).
V7. Coverage walk.      §9.7 / [R-LIF-08].  Claimants, disjointness, bounds,
                        checksums, slack total.  Plus F7 (a structure in the
                        pre-trailer gap), which is [R-CNT-05]'s check and not
                        part of [R-CNT-02]'s partition.
V8. Verdict + report.   Verdict per 1.1; plus the slack total (partial or
                        exact); each unchecked requirement with its ground;
                        each unexamined scope; each [R-MTA-10] record with
                        owning scope, encoding value, stored extent length.
```

Ordering note that I had to settle myself: V0 precedes V1 because §19.1 step 1
says the front-block check happens "before other processing", while §6.2's
ordered validation governs only the trailer's own fields. The two orders do not
conflict; they are about different structures.

**What the verifier reports when a check cannot be run** is fixed
per-mechanism, and the four mechanisms are not interchangeable:

| mechanism | verdict effect | report |
|---|---|---|
| capability: foreign format major | cannot establish | name the requirement + ground |
| capability: unimplemented MU=1 type | cannot establish | ditto |
| capability: cannot execute codec/filter (`[R-COD-11]`) | cannot establish | ditto — but see 1.6, this is vacuous for a *conforming* verifier |
| resource: layer declined (`[R-ERR-04]`) | cannot establish | ditto **and** slack total becomes partial |
| resource: tile decode declined | cannot establish | walk stays complete |
| resource: document decode declined (`[R-MTA-09]`) | cannot establish | SHOULD also report bound applied + stored extent length |
| experimental-range document encoding | **none** | MUST report scope, encoding, extent length (`[R-MTA-10]`) |
| SHOULD deviation observed | none | advisory |
| stopped at first violation | nonconforming | each unexamined scope; partial slack total |

The seventh row is the one an implementer gets wrong. `[R-MTA-10]` is emphatic
that an experimental encoding is *not* a cannot-establish ground — "no content
rule attaches there, so nothing is left unchecked" — so the verifier certifies
and merely names the bytes it did not inspect.

### 1.2 The concrete file

I built a complete file rather than describing one. Layer `sst`: rank 1,
dimension `x` with E = 100, T = 32; interleaved; one float32 channel `temp`
with fill `0x7FC00000`; codec 1, filter 1; **alignment A = 512 declared**
(the document's §7.4 example declares none — I wanted the alignment invariant
live). G = ⌈100/32⌉ = 4, N = 4, P = 32, entry_count = 4, decoded size
P·Q = 32·4 = 128. Index region 4·20 + ⌈4/2¹⁶⌉·4 = **84** bytes. Tiles 0 and 1
stored, tiles 2 and 3 sentinel. One top-level user-metadata record, encoding 1,
document `{"tarn.title":"a"}` (18 bytes) + terminal CRC = 22-byte extent.

Layer-record inline payload came out at **81 bytes** — identical to §7.4's
worked example, which is a useful cross-check since I changed the alignment
field's value but not its width. Directory: 24+81 + 24+1 + 4 = **134** bytes.

```
[    0,   16)   16   front signature block
[   16,  512)  496   SLACK (alignment gap: first stored tile must be 512-aligned)
[  512,  640)  128   stored tile, disk ordinal 0
[  640, 1024)  384   SLACK (alignment gap)
[ 1024, 1152)  128   stored tile, disk ordinal 1
[ 1152, 1236)   84   layer record extent  = tile-index region
[ 1236, 1258)   22   user-metadata record extent
[ 1258, 1264)    6   SLACK
[ 1264, 1398)  134   directory region
[ 1398, 1408)   10   SLACK (pre-trailer pad)
[ 1408, 1472)   64   live trailer                       F = 1472,  1472 mod 64 = 0
```

The walk found an overlap on my *first* attempt, because I had sized the
metadata extent at 20 bytes in the layout plan and 22 in the builder. That is
the F33 check firing on my own file, and it is worth recording that the check is
cheap and catches exactly the class of writer bug it is aimed at.

### 1.3 The coverage walk, partitioned

Claimants under §9.7, in the order the walk reaches them:

| claimant | bytes | reached via |
|---|---|---|
| front signature block | 16 | member of the live committed state, not "a structure" (Appendix G item 3 says §5.2 counts it as none) |
| live trailer | 64 | ditto |
| directory region | 134 | the trailer |
| layer record extent (index region) | 84 | the directory — **once**, §9.7: "not a second claimant beside it" |
| user-metadata record extent | 22 | the directory |
| stored tile, ordinal 0 | 128 | non-sentinel index entry |
| stored tile, ordinal 1 | 128 | non-sentinel index entry |
| **claimed** | **576** | |
| **slack** | **896** | F − 576 |

Independently: the gap runs are 496 + 384 + 6 + 10 = 896. They agree.

**Certified, counted-but-unconstrained, neither.** Of the 576 claimed bytes:

- **548** are covered by a further checksum: 256 tile bytes (entry `crc`
  fields), 80 index-entry bytes (the segment CRC), 4 segment-CRC-array bytes
  (`crc_of_crc_array`), 18 metadata-document bytes (the extent's terminal CRC),
  130 record-sequence bytes (the directory CRC), 60 trailer bytes (the trailer
  CRC).
- **12** are terminal checksum fields, comparison-verified and covered by
  nothing further (§4.5's list of exactly three: trailer, directory region,
  user-metadata extent). I checked that §4.5's *other* list — the interior
  checksum fields, "each segment CRC array, each tile-index entry's crc field,
  and each layer record's crc_of_crc_array" — has all three genuinely covered:
  the array by `crc_of_crc_array`, the entry crc by its segment CRC, and
  `crc_of_crc_array` by the directory CRC, since it is an inline-payload field.
  The two lists partition the checksum fields; nothing is on both or neither.
- **16** are the front block, checked by equality, which `[R-CNT-19]` excepts
  by name.

So on this file every claimed byte is verified by something. **The general
answer is different**, and I built the case: add a top-level record of an
experimental type (0x8000, MU = 0, PE = 0) with a 32-byte extent. Those 32
bytes are *claimed* — `[R-CNT-02]` says "a record extent (the bytes any
record's extent slot references, **whatever the record's type**)" — so they are
not slack and they are counted. But §8.1's last row gives them no checksum at
all, and §7.2 leaves them opaque. They are therefore **claimed, counted, and
uncertified**: the third category.

So the honest answer to "can a byte be neither certified nor
counted-but-unconstrained" is: no byte escapes counting — every byte is claimed
or slack, and both are counted — but *certified* and *counted-but-unconstrained*
are **not** a partition of the file. `[R-SEC-04]` says so directly: "The extent
of a record of a type this specification has not assigned is covered by no
checksum either (§8.1), so corruption inside it is equally invisible." Note the
asymmetry, which I opened as a suspicion and closed as deliberate: the
experimental-*encoding* metadata extent, which at least carries a CRC, gets a
mandatory report line under `[R-MTA-10]`; the unassigned-*type* extent, which
carries none, gets no report line. §22.3 acknowledges the invisibility and
offers no remedy, so it is stated, not omitted.

### 1.4 A walk that does not complete

Same file, three generations on (see 1.7), F = 2304, true slack 1708. Suppose
the verifier declines layer `sst` on resource grounds (`[R-ERR-04]` licenses a
decline at layer scope). It never reads the index, so it enumerates only:
front block 16 + metadata extent 22 + directory 134 + trailer 64 = **236**.

Partial total = F − 236 = **2068**. Against the true 1708 that is an over-count
by 360 — exactly the layer's three claimants — which is what `[R-CNT-21]`
promises: "an upper bound on the file's true slack, never an under-count". The
verifier MUST say what stopped it: layer `sst`, declined on resource grounds.
Verdict: no violation established, one requirement unchecked on a resource
ground → **cannot establish**.

I checked the upper-bound claim can't fail. Partial = F − |union of enumerated
claimants|; true = F − |union of all|; enumerated ⊆ all, so partial ≥ true. It
would fail if "the bytes claimed by the claimants" meant the *sum of lengths*
rather than the union, because overlapping claimants would double-count and
push the total below the truth. Reading it as the union is the only reading that
makes the sentence's own claim true, so that is the reading I took.

Second incomplete walk, on the same file: the walk itself establishes L40
(a stored tile's offset not a multiple of the declared A). `[R-CNT-21]` then
directs that "the claimants it had already enumerated are discarded with the
layer" — the same 360 bytes fall out — so the partial total is again 2068, but
the verdict is **nonconforming**, not cannot-establish. Two identical numbers,
two different verdicts, and the report must say which.

I noticed a small tension here and closed it: the formula sentence says "F less
the bytes claimed by the claimants the walk **did enumerate**", while the
discard sentence has already un-enumerated some of them. Read literally the two
give different totals (2068 vs 1708), both of which satisfy "upper bound, never
an under-count". The discard sentence is directive ("are discarded with the
layer"), so it governs and the formula means the post-discard set. Not filed —
and in any case the document already declares a partial total run-dependent:
"a fact about that run and not about the file's live state."

### 1.5 Extent overlap, alignment and slab on an adversarial layout

I built a hostile planar layer rather than reasoning about it abstractly.
Layer `P`: rank 1, E = 10, T = 4 → G = N = 3, P = 4; **planar**, C = 2, channels
`c0` uint16 and `c1` bool. entry_count = C·N = 6. Decoded sizes: `c0` plane
P·Bᶜ = 8 bytes; `c1` plane ⌈P/8⌉ = 1 byte, with P mod 8 = 4 so bits 4–7 are pad
bits. Slab S = 2, A_slab = 64.

Run partition (`[R-SLB-02]`, runs never span channel blocks):
channel block 0 = ordinals [0,3) → runs [0,2), [2,3);
channel block 1 = ordinals [3,6) → runs [3,5), [5,6).
The final run of each block covers fewer than S ordinals, as the rule provides.

Entries planted at offsets 64, 72, 128, 192, 194, 200 with lengths 8, 8, 8, 1,
1, 1. Checking `[R-SLB-03]` from the index entries alone plus F:

- run [0,2): first stored offset 64, 64 mod 64 = 0 ✓; 64 + 8 = 72 = next ✓.
- run [2,3): 128 mod 64 = 0 ✓, single tile ✓.
- run [3,5): 192 mod 64 = 0 ✓; 192 + 1 = 193 ≠ 194 → **L41, gap**, reject-layer,
  verifier, certification.
- run [5,6): 200 mod 64 = 8 ≠ 0 → **L42**, reject-layer, verifier.

Swapping the slab for A = 512 instead: every one of the six offsets fails
`offset mod 512 = 0` → **L40** six times over. Both invariants are decidable
from the entries and F, as `[R-SLB-03]` claims — I did not need any payload
byte, which is the point of the claim.

Overlap: place the index region at offset 70. Its length is 6·20 + 4 = 124, so
it spans [70, 194) and swallows the `c0` extents. §15.3's row "a stored extent
overlaps its own layer's index region" → **L18**, reject-layer. Move the same
collision to another layer's structure and it becomes **F33**, reject-file. I
checked §7.2's four-way split is a genuine partition of the overlap cases —
both in one layer / different layers / one in a layer and one not / neither in
a layer — and it is, with L18 taking the first and F33 the other three.

Content obligations on this layer, which is where the verifier's decode work
lands: tile s = 2 covers x ∈ [8,12) and E = 10, so x = 10, 11 are padding
positions. In `c0`'s plane for s = 2, in-tile ordinals 2 and 3 must hold the
recorded uint16 fill bytes (**T4**). In `c1`'s packed plane for s = 2, bits 2
and 3 are padding *positions* (T4) and bits 4–7 are *pad bits* (**T5**) — and
§14.3's Note is right that these are two different mechanisms living in one
byte. Both must equal the channel's fill bit.

### 1.6 Checksum obligations

I reproduced, locally, **every** checksum constant the document states:

| constant | document | computed |
|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283`, stored `83 92 06 E3` | ✔ identical |
| CRC-32C(zero bytes) | `0x00000000` | ✔ |
| §7.4 segment CRC over 4 sentinel entries (80 B) | `0x80A34955`, stored `55 49 A3 80` | ✔ |
| §7.4 `crc_of_crc_array` over that 4-byte array | `0xC4EE982E`, stored `2E 98 EE C4` | ✔ |
| §15.4 / App. B, CRC of a full 2¹⁶-sentinel segment | `0xEECB3BB2` | ✔ |
| Appendix A trailer CRC over trailer [0,60) | `0x402F157E` | ✔ |
| Appendix A directory CRC over zero bytes | `0x00000000` | ✔ |

All seven fall out of one implementation parameterised exactly as §4.5 states
(reflected polynomial 0x82F63B78 from the stated 0x1EDC6F41, init and final XOR
0xFFFFFFFF, stored little-endian), which is itself evidence that the stated
parameter set is self-consistent. **None** was unreproducible. I additionally
re-derived Appendix A's whole 128-byte file: front block, dir_offset = 16,
dir_length = 4, F = 128, file_id = 0x0123456789ABCDEF, reserved zero — every
annotation checks out.

Non-checksum constants I could check locally and did: the two magics
(`\x89`+"TARN"+CRLF+^Z and `\x8A`+"NRAT"+CRLF+^Z), the zstd frame magic
(0xFD2FB528 → `28 B5 2F FD`), the LZ4 *frame* magic in T23 (`04 22 4D 18` →
0x184D2204), §12.3's twelve-byte channel entry, §4.6's `température` at 12 bytes
NFC and 13 NFD with `é` NFD = `65 CC 81`, and bfloat16 1.0 = 0x3F80 from
binary32 0x3F800000. All correct. The LZ4 *block* format revision and RFC 8878's
window derivations I could not check without the external documents, and did not
try.

**Is every live structure covered by one checksum?** I derived §8.1's map rather
than trusting it: `[R-CNT-02]`'s classes are front block, stored-tile extent,
record extent, directory, trailer — five, expanding to seven map rows because
"record extent" splits by type into tile-index region (a layer record's extent,
always, per §7.4), user-metadata extent, and unassigned-type extent. In format
major 1 only two types are assigned, so no fourth split exists. The map is
complete, and the one uncovered class is the unassigned-type extent, excepted by
name in `[R-CNT-19]`.

**A vacuity worth recording.** `[R-CNF-11]` lists "when it cannot execute a
codec or filter (`[R-COD-11]`)" among the cannot-establish grounds. For a
*conforming* verifier this can never fire: all four codecs and both filters are
core (`[R-COD-03]`, `[R-COD-09]`, `[R-CNF-03]`), and any other value is a
layer-scope violation → nonconforming, not cannot-establish. §17.4 states this
in terms — "For a conforming reader that position arises only at a reserved or
experimental value" — so it is an acknowledged vacuity, not a defect. I opened
it and closed it on that sentence.

### 1.7 Decoded-content obligations

What a verifier that certifies **must** decode: every stored tile, "whatever
content obligations §14 places on the layer" (§9.7). The "whatever" is
load-bearing — a layer with no padding positions and no bool channels still
needs `[R-SER-07]`'s exact-size check and `[R-COD-08]`'s exact-consumption
check, which are only observable by decoding.

What it compares against: the decoded size derived from declarations alone
(T3), the entry length under codec 1 (T14), the recorded fill at every padding
position (T4), the fill bit at every pad bit (T5), 0x00/0x01 at every
interleaved bool value (T2), and the codec header rows T17–T23. T26 (wrong
filter stride) has no procedure of its own — the register says "the check that
detects it is T2's or T4's".

What it is permitted to skip: SHOULD deviations, which it "owes no search for"
(`[R-CNF-12]`); the content of slack, which "is not its concern" (§9.7); the
content of a document under an experimental encoding, which "asks nothing of
this walk"; and the content of an unassigned type's extent, opaque by §7.2. It
may also *decline* a tile's or a document's decode on resource grounds — but
declining is not skipping: it forfeits certification.

One boundary I had to settle: a verifier must decode every *stored* tile, and
§3.1 makes a tile stored iff its entry is not the sentinel — including an entry
that §15.3 classifies reject-tile on a structural ground, which yields no extent
to decode. The resolution is that such an entry is itself a violation (T6–T12),
so the "verifier that certifies" precondition has already failed. No gap.

### 1.8 Multi-generation trace

Same layer, four generations. Every F is a multiple of 64 and every increase is
at least 128, as `[R-LIF-02]` forces.

| gen | operation | F | claimed | slack | verdict |
|---|---|---|---|---|---|
| 1 | create | 1472 | 576 | **896** | conforming |
| 2 | supersede stored tile ordinal 0 | 1984 | 576 | **1408** | conforming |
| 3 | grow E 100 → 130 (entry_count 4 → 5) | 2304 | 596 | **1708** | conforming |
| 4 | compact, fresh file_id | 1536 | 596 | **940** | conforming |

Gen 2 writes the new tile at 1536 (the next multiple of 512 at or above F = 1472,
so `[R-SLB-01]` holds), a new 84-byte index region at 1664, a new 134-byte
directory at 1748 ending at 1882, pad to 1920, trailer [1920, 1984). The slack
delta checks two ways: 896 + 128 (old tile) + 84 (old index) + 134 (old
directory) + 64 (old trailer) + 64 (alignment gap) + 38 (new pad) = 1408, and
the walk's gap runs sum to 1408.

Gen 3 is the interesting one for §20.3. Growing E from 100 to 130 raises
G = ⌈130/32⌉ from 4 to 5, so entry_count changes, so `[R-CNT-17]`'s
extent_length changes from 84 to 104, so the whole index region is re-emitted at
a new placement. Disk ordinals do **not** renumber here: rank 1 means s = t₀ and
`[R-GEO-06]`'s ∏_{j>0} Gⱼ is the empty product 1, so entries 0–3 are copied
byte-identically at their positions and entry 4 is a fresh sentinel — exactly
what §20.3 step 4 prescribes. `[R-GEO-06]` *does* move ordinals when a
non-leading grid count grows, which is why the parenthetical exists.

The verifier's work changes at gen 3 in a way worth spelling out. At gen 1–2,
tile ordinal 3 covers x ∈ [96,128) with E = 100, so positions 100–127 are
padding — but the tile is a sentinel, so `[R-SER-05]` places no obligation on it
("a tile the new state does not address carries no obligation" is the sibling
principle). At gen 3 with E = 130, ordinal 3 covers [96,128) entirely inside the
extents, so it has *no* padding positions and T4 is vacuous for it; the new
ordinal 4 covers [128,160) with 130–159 padding, again a sentinel. Growth only
ever turns padding into real, never the reverse — which is the load-bearing fact
behind §20.3's permission and behind §23.1's "no commit turns a real position of
a stored tile into padding", and I checked it holds because tile extents are
fixed, so tᵢ = xᵢ div Tᵢ and uᵢ = xᵢ mod Tᵢ are untouched by a change in Eᵢ.

Gen 4, compaction: fresh file_id, every stored tile's bytes verbatim, index
regenerated because the extents relocated (entry offsets new, lengths and crcs
unchanged, segment CRCs recomputed), `crc_of_crc_array` updated. The result is
**940 bytes of slack in a freshly compacted file** — 496 + 384 of alignment gap
plus a 60-byte pad. That is not a defect: §5.2 lists "alignment and slab gaps"
as slack, and §20.5 says slack is never *carried*, not that none is created.
But §20.5's figure draws the output with no gaps at all, and an implementer who
reads the figure as the general case will size a compaction wrong. I checked the
normative text for an over-claim and found none, so this stays an observation
about the figure rather than a finding.

---

## 2. Findings

Three. Two are contradictions between passages, one is an ambiguity in the
closed list. None is byte-level, and I say why for each rather than reaching.

### verifier-01 — §20.3's closure claim about which register rows witness a fixed-declaration change omits the padding rows T4 and T5

**Kind:** CONTRADICTION. **Location:** §20.3 step 4, `[R-WRT-04]` (normative
prose — not a Note, Example or Rationale block, so `[R-CNF-01]` does not exempt
it); against §21.7 `[R-ERR-01]` and §14.5 `[R-SER-05]` / §21.4 rows T4, T5.

§20.3 justifies its fixed list by asserting that a fixed-declaration change is
invisible to every owed check but three:

> Under new ones the same bytes would denote values,
> coordinates or padding the writer did not store, with every
> checksum in §8 certifying the result and, but for a decoded size
> or a boolean byte the register witnesses (T3, T14, T2), no check
> any actor owes able to see it (§21.7).

§21.7, cited in that very sentence, gives the class as **three**, not two:

> The obligations of §14.5 and
> `[R-SER-08]` narrow this only where content is structurally
> constrained: padding positions, pad bits, and boolean bytes.

Padding positions and pad bits are the two §20.3 drops. They are owed checks —
`[R-SER-05]`: "A conforming reader never returns this content and is not
obligated to check it; **a verifier MUST check it**" — and they are registered
as T4 and T5, detector *verifier*, detected *certification*.

They witness fixed-declaration changes routinely. Take my own layer: E = 100,
T = 32, so tile ordinal 3 has 28 padding positions, each holding the recorded
float32 fill `0x7FC00000` by `[R-SER-05]`. Store that tile, then commit a fill
change to `0x00000000` — one of the changes §20.3 forbids ("every channel's type
and fill"). Every checksum still verifies, T3 and T14 see nothing (the decoded
size is unchanged at 128 bytes), T2 is inapplicable (no bool channel), and the
file is nevertheless caught cold by **T4**: 28 padding positions holding
`00 00 C0 7F` against a recorded fill of `00 00 00 00`. The same happens for a
re-tiling that preserves the decoded size — interleaved, extents (4,4), tile
extents (2,8) → (8,2) holds N = 2 and P = 16 and therefore the decoded size,
while moving the padding set from {x₁ ≥ 4} to {x₀ ≥ 4} — and for a planar bool
plane, where T5 catches a fill change in the pad bits alone.

What an implementer does wrong without this: builds a verifier that treats the
three named rows as the complete set of checks that can catch a bad commit, and
then reasons — from §20.3, in normative text — that a padding mismatch on a
layer whose declarations changed is somehow out of scope. The correct behaviour
is unaffected because T4 and T5 stand on their own governing rule; what is wrong
is the document's own account of its detection surface, in the passage whose
whole purpose is to explain why the line falls where it does.

**Byte-level: no.** T4 and T5 are stated unconditionally in §14.5 and registered
in §21.4; §21.1 makes the rule govern over any row, and this passage is neither
a rule that grants a permission nor a row. No writer's emittable set and no
verifier's verdict changes on either reading of the sentence — the sentence is
an assertion about detectability, and the checks it mis-describes are
independently mandatory.

### verifier-02 — §13.3 claims only an entry_count change forces index re-emission among §20.3's permitted changes; §20.3 step 4 says an alignment or slab declaration does too

**Kind:** CONTRADICTION. **Location:** §13.3, the "Note — sparse writing" block
(labelled *Note*, therefore non-normative under `[R-CNF-01]`); against §20.3
step 4, `[R-WRT-04]` (normative).

§13.3 says:

> each commit that changes a
> layer's stored-tile set or its index content — which, among the
> declaration changes §20.3 permits a layer that stores a tile, only
> a change to entry_count does — re-emits that layer's whole
> tile-index region (§11.1, §20.3, `[R-WRT-04]`).

The parenthetical is a closed claim: of the changes §20.3 permits a
tile-storing layer — names, extent growth, planar channel list at the end, and
a slab or alignment declaration — only one that moves entry_count changes index
content. §20.3 step 4 itself says otherwise, in the clause that governs exactly
this case:

> Extents this commit supersedes become slack (`[R-CNT-21]`);
> a slab declaration is re-established or cleared (`[R-SLB-04]`),
> and an aligned layer's stored tiles — every one the new state
> keeps, not only those this commit adds — satisfy its invariant or
> the declaration is cleared (`[R-SLB-01]`, `[R-CNF-05]`).

"every one the new state keeps, not only those this commit adds" is the whole
point: a commit that declares A = 4096 on a layer whose already-stored tiles sit
at unaligned offsets must move them, which it does by superseding each extent
(explicitly an appender operation — step 4 writes "entries for tiles this commit
stores or **supersedes** written to their new state") and re-pointing its entry.
Every such entry's `offset` field changes. entry_count does not move at all:
the addressed-tile set is untouched. The same holds for `[R-SLB-04]`'s
"re-establish the invariants for every such run", which by construction means
re-packing stored tiles at new offsets.

§11.1's Rationale, which §13.3 cites, states the true and narrower claim —
"**Growth** that leaves entry_count unchanged touches the directory alone" —
and that is correct, because growth never moves a tile's bytes. §13.3 has
generalised a growth-only statement across all four permitted changes, and two
of them (declaring alignment, declaring or re-establishing a slab) falsify it.

What an implementer does wrong without this: writes an appender that, on
declaring an alignment or a slab, re-emits the layer record but not the index
region, because it read §13.3 as telling it when re-emission is required. The
output then carries an index whose entries point at the old, unaligned
placements — L40, or L41/L42 — and a verifier rejects the layer.

**Byte-level: no.** The block is labelled *Note* and therefore non-normative
under `[R-CNF-01]`; §20.3's normative clause and `[R-SLB-04]` decide what a
commit owes, and both readings of §13.3 leave the set of conforming files
untouched. I file it because a non-normative block that contradicts the
normative text it glosses still tells an implementer what to build, and this one
tells it something that produces a rejectable file.

### verifier-03 — §20.3 does not say whether one commit may both extend and shorten a planar channel list, and the combination replaces the last channel's type and fill

**Kind:** AMBIGUITY. **Location:** §20.3 step 4, `[R-WRT-04]` (normative).

The permitted list and its combination clause:

> A layer that stores a tile **in the generation this commit
> supersedes** keeps its declarations, with these exceptions and no
> other: its name, and its dimension and channel names, MAY change;
> an extent MAY grow, and MUST NOT shrink; a planar layer's channel
> list MAY be extended at its end, or shortened from its end; and a
> slab or alignment declaration MAY be declared, re-established or
> cleared as this step provides below. A commit MAY make several of
> these changes at once.

Two readings, and the tie-break clause a few lines later — "the permitted side
states the whole of what a commit MAY do to it" — does not separate them.

**Reading A (operations compose).** "several of these changes at once" reaches
*within* a bullet, not only across bullets. It must, or a commit could not clear
a slab and declare an alignment in one go — both are inside the fourth bullet,
and switching between them is the ordinary way to change a layer's layout
promise. But then it equally reaches inside the third bullet, and a commit may
shorten by one and extend by one. Net effect on the declarations: the channel at
position C−1 now has a different **name, type and fill**. The fixed list's
"every channel's type and fill" is not contradicted on this reading, because no
channel's type changed — one channel left the list and another arrived; and the
fixed list already carves out "the position of every planar channel **but the
last**".

**Reading B (declarations compared).** Compare the two generations' layer
records: the channel at index C−1 has a different type and fill, and "every
channel's type and fill" is fixed, so the commit is a rewrite.

I picked **B** for the implementation, on two grounds. First, §20.3's own
principle for the appended-channel case does not reach A: "an appended planar
channel adds tiles at ordinals after every existing one, a disk ordinal being
c · N + s with N the spatial-tile count". Under A the appended channel's tiles
land at ordinals [(C−1)·N, C·N) — precisely the ordinals the removed channel's
tiles occupied — so they are *not* after every existing one, and the
justification the list rests on evaporates. Second, A makes the outcome
order-dependent while "at once" fixes no order: shorten-then-extend replaces the
last channel, extend-then-shorten is a no-op, and nothing in the text chooses.

Under A the hazard is concrete. Step 4's default for the index is "every other
entry byte-identical at its disk-ordinal position", and an updater that treats
ordinals [(C−1)·N, C·N) as "other" — they existed in the prior generation —
copies the departed channel's entries forward to serve the arrived channel. If
the two element sizes differ, T3 or T14 catches it. If they do not — int32
replaced by float32, both 4 bytes — and the layer has no padding positions and
no bool channel, nothing catches it: every checksum verifies, the decoded size
matches, and the stored bytes are reinterpreted under a declaration the fixed
list exists to freeze.

**Byte-level: no**, and I want to be explicit about why, because it is close.
Call the disputed output X: generation 2 of a planar layer whose last channel
has been replaced by one of the same element size and byte-identical fill.
X *is* a conforming file — I checked every register row that could bite: no T3,
no T14 (element sizes equal), no T4 or T5 (E = 8, T = 4 leaves no padding
position), no T2 (no bool). Under reading A an updater may emit X; under B it
must do a whole-file rewrite instead. But a **creator** may emit X under either
reading: X's superseded generation-1 bytes are slack, slack content is
unconstrained (`[R-CNT-03]` only advises zeroing), and `[R-SLB-05]` leaves
placement free, so a single-commit creator can produce X byte-for-byte. X is
therefore in the emittable set on both readings, and a verifier certifies it on
both. The fork is in which actor may reach X by which route — updater conduct —
not in the set of bytes a conforming implementation may emit or must reject.
That is the discriminator §2.3's `[R-CNF-05]` and the register jointly impose,
and it lands on the "not byte-level" side.

I also note, per the brief's instruction about twice-rewritten passages: this
list is the most-repaired step in the document and I am not proposing wording.
What it still admits is stated above; which reading is intended is a matter for
human disposition.

---

## 3. Suspicions I opened and closed

- **Is `[R-CNF-11]`'s cannot-establish list closed, and does it reach a
  whole-layer resource decline?** §9.7 and `[R-CNT-21]` contemplate a verifier
  that "declined a layer on resource grounds and so never enumerated its
  claimants", which is broader than the list's "declines a layer's or a tile's
  **decode**". Closed by the list's own introducer: "as when the file names a
  format major version it does not implement, when … or when …" — "as when"
  makes it exemplary, and the general clause ("some requirement is one it is
  unable to check on a capability or resource ground") covers it.
- **Can a verifier report *conforming* while also reporting an unchecked
  requirement?** `[R-CNF-11]` says it reports unchecked requirements "whichever
  of the three verdicts it reports". I could construct no case: an unchecked
  requirement on a capability or resource ground *is* the cannot-establish
  condition. Over-broad phrasing, harmless; not filed.
- **Does §9.7's walk omit `[R-CNT-05]`'s pre-trailer-gap check (F7)?** It does
  not mention it. Closed: §9.7 is expressly about "`[R-CNT-02]`'s partition",
  and F7 is `[R-CNT-05]`'s condition, stated there and listed in Appendix H's
  verifier checklist. Two checks, two homes.
- **Does F33's Instances cell double-count, listing "tile-index regions" beside
  "record extents" when §9.7 says the region enters the walk *as* a record
  extent?** Closed on §21.1: an instance may name "a container it can occur
  in", and building a vector that collides an index region is materially
  different work from colliding a metadata extent.
- **Does a §20.3-violating commit make its output nonconforming, and can a
  verifier ever say so?** No. §2.3 makes file conformance "a pure predicate on
  bytes"; §20.3's rule ranges over two generations; §9.7's Note is explicit that
  "Nothing here enumerates prior commits". The register correctly carries no
  row. A verifier can never adjudicate §20.3.
- **Is `[R-MTA-06]`'s `tarn.` key prohibition a missing member of
  `[R-CNF-02]`'s closed list of writer obligations whose violation leaves the
  file conforming?** Closed: `[R-CNF-02]`'s *first* sentence already catches it
  by name — "which registry version a writer targets (§10.3, §18.3)" — and it
  belongs there rather than in the second sentence's list, because "at the
  version they target" is not decidable from the bytes.
- **Is the `[R-SLB-04]` Note right that a stale slab declaration needs no
  register row of its own?** Yes, near-tautologically: "stale" means the
  invariants do not hold, and `[R-SLB-03]`'s invariants are exactly packing
  (L41) and first-stored-tile alignment (L42). I checked the trigger set for a
  case that produces no L41/L42 — S changed 8 → 4 with A_slab = 1 and placement
  untouched — and found the invariants simply already hold there, so the
  declaration is not stale.
- **Does `[R-CNT-21]`'s "upper bound, never an under-count" survive overlapping
  claimants?** Only if "the bytes claimed" means the union, not the sum of
  lengths. Taken as the union; noted in 1.4.
- **Is the unassigned-type extent's lack of a report line, beside
  `[R-MTA-10]`'s mandatory one, an omission?** No — §22.3 `[R-SEC-04]` names
  the invisibility as one of four "residues … stated rather than defended".
  Deliberate asymmetry, not a gap.
- **Are T6/T11 and T7/T11 double-registrations of the all-ones entry?** No —
  T11 carries the qualifier "the value being distinct from the all-ones
  sentinel", which makes it disjoint from both. Cleanly separated.
- **Is `[R-COD-11]` reachable by a conforming verifier?** No; §17.4 says so in
  terms. Acknowledged vacuity, not a defect.
- **Does §23.1's "no commit turns a real position of a stored tile into
  padding" hold?** Yes. Tile extents are fixed for a tile-storing layer, so
  tᵢ = xᵢ div Tᵢ and uᵢ = xᵢ mod Tᵢ never move, and growth only shrinks
  {x : x ≥ Eᵢ}. Every operation that would reverse it — shrink, re-tile,
  transpose, rank change — is on the fixed side.

## 4. Numbers I derived, against the document's own

| I computed | document states |
|---|---|
| register rows: F 35, L 49, T 26, R 10 = **120** | §21.2 "35 conditions", §21.3 "49", §21.4 "26", §21.5 "10"; §21.8 "120 conditions" ✔ |
| Instances cells, semicolon-counted, `—` = 1: F 56, L 116, T 55, R 50 = **277** | §21.8 "277 instances" ✔ |
| §7.4 inline payload = 4 + 34 + 18 + 12 + 13 = **81** | "The inline payload is 81 bytes" ✔ |
| §7.4 index extent = 4·20 + ⌈4/2¹⁶⌉·4 = **84** | "= 84" ✔ |
| §11.2: G = (4,8), N = 32, P = 65,536; ⌈1000/256⌉ = 4 | ✔ |
| §11.4: s = 10, in-tile ordinal 44·256+188 = **11,452**, planar disk ordinal 2·32+10 = **74** | ✔ |
| §15.4: 16 segments, last covers **16,960**; array 64 B; region **20,000,064**; seg 15 = [19,660,800, 20,000,000) = 339,200 B; entry 999,999 at seg byte **339,180**; full segment 1,310,720 B = 1.25 MiB | ✔ all |
| §15.4: planar entry for ordinal 74 at region bytes [1,480, 1,500); channel 3 = ordinals 96–127 | ✔ |
| §14.2: Q = 3, decoded 18, ordinal 5 at [15,18); planar `b` plane 12 B, ordinal 5 at 10–11; Q = 5, decoded 30, [25,30) | ✔ |
| §14.3: bits give `55 01` (fill false) and `55 FD` (fill true) | ✔ |
| §14.5: 2×2 grid, edge tile 1 real + 15 padding, 32 B, values 1–15 = `CD AB` | ✔ |
| §17.3: shuffle of 1.0/2.0/3.0 → `00 00 00 00 00 00 80 00 40 3F 40 40` | ✔ |
| §20.3: 32·20 + 4 = **644** | ✔ |
| §21.9 Note: segment CRC array at 2³² entries = **256 KiB**, at 2³⁶ = **4 MiB**; 12.5 MiB / 65,536 = 200 B per layer record | ✔ |
| lz4 cap 0x7E000000 = 2,113,929,216 (≈1.97 GiB) | ✔ consistent |
| my file: F = 1472, claimed 576, slack 896 (gap runs 496+384+6+10) | — my own construction |
| trace: slack 896 → 1408 → 1708 → 940 across four generations, each F a multiple of 64, each increase ≥ 128 | — my own construction |

## 5. Sweeps run

Against the flattened text, with matching positive controls first.

| pattern | hits |
|---|---|
| controls: "MUST report the total number of slack bytes" / "A partial total is F less the bytes claimed" / "only a change to entry_count does" / "no check any actor owes able to see it" / "every one the new state keeps, not only those this commit adds" | 1 each (all five) |
| `verif(ier\|iers)` — sentence extraction, all 103 read | 118 word hits, 103 sentences |
| "cannot establish" | 9 |
| "slack" | 64 |
| "certif" | 47 |
| "unexamined" | 4 |
| "coverage walk" | 3 |
| "partial total" | 4 |
| "claimant" | 15 |
| "live committed state" | 10 |
| "decoded size" | 44 |
| "slab" / "A_slab" / "alignment" | 68 / 20 / 41 |
| "a verifier MUST" | 9 |
| "verifier MUST NOT" | 3 |
| "verifiers MUST" | **0** (the document uses the singular throughout — checked against "a verifier MUST" = 9, so the zero is real, not a wrap artefact) |
| "MUST NOT certify" | 4 |
| "certifies" | 9 |
| "certification is unaffected" | 3 |
| register table rows parsed by regex `^\|\s*([FLTR]\d+)\s*\|` | 120 |

## 6. Where I found little, and what I did that would have found something

**The certification procedure and the verdict vocabulary (§2.3, §9.7, §17.4,
§18.2, §21.9).** I found nothing here and I am confident it is clean. What I did
that would have found something: I extracted and read all 103 sentences in the
document containing "verifier", not the ones I expected to matter; I derived the
availability condition for *conforming* rather than taking it, and checked it
against the three independent bars (established violation, unchecked
requirement, incomplete traversal); I tested the cannot-establish list for
closedness and found its introducer open; I chased `[R-COD-11]` to its vacuity
and found §17.4 had already declared it; and I built the table in 1.1 by
enumerating every mechanism in the document that can leave a check unmade, then
checking each against `[R-CNF-11]`, `[R-ERR-04]`, `[R-MTA-09]` and `[R-MTA-10]`
for its verdict effect and its report obligation. The one asymmetry I found —
`[R-MTA-10]` reports, the unassigned-type extent does not — is stated in §22.3
rather than omitted.

**Checksum obligations (§4.5, §8.1, §8.2).** Nothing found. I reproduced all
seven stated constants from the stated parameters, re-derived §8.1's seven map
rows from `[R-CNT-02]`'s five byte classes rather than reading them off, and
checked that §4.5's terminal list (three fields) and interior list (three
fields) partition the checksum fields with nothing on both sides or neither. A
missing row or a mis-assigned coverage would have shown up in that derivation.

**Extent overlap, alignment, slabs (§7.2, §15.3, §16).** Nothing found. I built
a planar layer with two channel blocks and four runs, planted a gap and a
misalignment, and confirmed L41 and L42 fire from the entries and F alone as
`[R-SLB-03]` claims; I checked §7.2's overlap split is a genuine four-way
partition of the cases; I counted §15.3's *structural* rows and got exactly the
six the text asserts; and I checked T6/T7/T11's boundaries around the all-ones
value and found them disjoint.

**The coverage walk (§5.2, §9.7).** One near-miss (the enumerate/discard tension
in 1.4), closed on the directive sense of "are discarded". I built a real file,
ran the walk, caught a real overlap in my own layout, ran the walk twice more on
an incomplete traversal, and verified the "upper bound, never an under-count"
claim both by construction and by argument — including finding the one reading
(sum of lengths rather than union) under which it would fail, and rejecting it.

