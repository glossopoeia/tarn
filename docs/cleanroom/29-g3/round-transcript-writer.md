# Cleanroom round 29 — Writer implementer transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,697 lines, 46,880 words by `wc`). I read it in full, in five sequential
`Read` calls, before doing any analysis. I opened no other file: no `docs/`, no
`PLAN.md`, no `OPEN-QUESTIONS.md`, no `conformance/`, no `spec/registry.json`,
no git history, no web.

The brief said the spec lives at `spec/tarn.md`. It does, under the repository
root `tarn-first-draft`. **However**, my runtime placed material in my context
before I began, unasked, and I disregarded it: a project instruction file
(`CLAUDE.md` pointing at `AGENTS.md`) whose repository root is named `tarn`
rather than `tarn-first-draft`, and an index of the maintainer's persistent
memory notes with six titled entries. I did not open any file either one named,
and I did not act on anything either one said; I am naming their appearance
because the brief requires it and because the path discrepancy (`tarn` vs
`tarn-first-draft`) is itself context the brief did not give me. Nothing in my
findings below derives from either.

Files I wrote, all in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/writer/`:

- `wr_crc.py` — a CRC-32C implementation (reflected 0x82F63B78, init/final 0xFFFFFFFF)
- `wr_checks.py` — reproduces the document's stated CRC constants
- `wr_count.py` — mechanical row/instance count over §21.2–§21.5
- `wr_build.py` — builds a complete two-layer file end to end and walks its coverage
- `wr_misc.py` — §21.9 note arithmetic, byte-shuffle fixed points, commit-2 layout
- `gen1.tarn` — the 576-byte file `wr_build.py` emits

Plus this transcript, at the single output path the brief named. I did not read
that output directory.

---

## 1. Checksum bootstrap

Before trusting anything I computed, I checked my CRC against the document's own
check vector (§4.5):

```
CRC-32C("123456789") = 0xE3069283   document: 0xE3069283   ✓
CRC-32C(zero bytes)  = 0x00000000   document: 0x00000000   ✓
```

Then every other stated CRC constant:

| Quantity | Computed | Document |
|---|---|---|
| Appendix A minimal-file trailer CRC over [0,60) | `0x402F157E` | `0x402F157E` (§Appendix A) ✓ |
| CRC of a full 2¹⁶-entry all-sentinel segment | `0xEECB3BB2` | `0xEECB3BB2` ([R-IDX-05], App. B) ✓ |
| §7.4 example: CRC over 4 sentinel entries (80 bytes) | `0x80A34955` | `0x80A34955` ✓ |
| §7.4 example: `crc_of_crc_array` over that 4-byte array | `0xC4EE982E` | `0xC4EE982E` ✓ |

All four reproduce byte for byte, stored little-endian as `[R-ENC-09]` requires.
I built the minimal-file trailer field by field from §6.2's layout table to get
the third figure, which incidentally confirms the layout table and Appendix A
agree on every offset.

---

## 2. Creation byte layout — a worked file

I built a file with two layers chosen to exercise edge padding, packed boolean
planes, sentinels, and both layouts. Everything below is what the document
determined; I flag each free choice.

**Layer 1 — `sst`**, interleaved, rank 2, dims `y` (E=3, T=2) and `x` (E=5, T=3);
channels `t` float32 fill `00 00 00 00`, `m` bool fill `00`; codec 1, filter 1,
linearization 1, A=0, S=0, A_slab=0, index_encoding 1.

Derived per §11.2 and §14.2 — all fixed, none free:

```
G = (⌈3/2⌉, ⌈5/3⌉) = (2, 2)      N = ∏G = 4        P = ∏T = 6
C = 2   B = (4, 1)   Q = ΣB = 5   decoded size = P·Q = 30
addressed-tile count = N = 4 (interleaved)  →  entry_count = 4
index extent_length = 4×20 + ⌈4/2¹⁶⌉×4 = 84        ([R-CNT-17])
```

Both axes overhang (3 mod 2 ≠ 0, 5 mod 3 ≠ 0), so tiles 1, 2 and 3 carry padding
positions. Tile 3 = tile coords (1,1) by `s = t_y·G_x + t_x` ([R-GEO-06]); it
covers y ∈ {2,3}, x ∈ {3,4,5}, of which only (2,3) and (2,4) are real. In-tile
ordinals 2, 3, 4, 5 are padding and I encoded each channel's fill there
([R-SER-05]). I stored tiles 0, 1, 3 and left tile 2 as the sentinel
`FF ×16 00 ×4` ([R-IDX-02]).

**Layer 2 — `mask`**, planar, rank 1, dim `i` (E=10, T=4); one bool channel `b`
fill `01`; codec 1, filter 1.

```
G = (⌈10/4⌉,) = (3,)   N = 3   P = 4   C = 1
addressed-tile count = C·N = 3   →   entry_count = 3
packed plane decoded size = ⌈P/8⌉ = 1 byte        (§14.3)
index extent_length = 3×20 + 1×4 = 64
```

Tile 2 covers i ∈ {8,9,10,11}; i=10 and i=11 are padding positions and take the
fill *bit* (1). P mod 8 = 4 ≠ 0, so bits 4–7 of every tile's single byte are pad
bits and also take the fill bit ([R-SER-05], §14.3). Concretely, with real values
i=8 true, i=9 false: byte = `0xFD`. Tile 1 (i ∈ {4..7}, all false) encodes `0xF0`
— note that with fill = true this tile is **not** all-fill, so it must be stored;
a writer that reflexively sentinels "all-false" boolean tiles would silently
change the reference array.

**Placement.** [R-LIF-02]'s creation path fixes: front block at 0, then step 2's
structures beginning at offset 16, then step 3's directory, then step 5's pad and
trailer. *Within* step 2 the order and the gaps are free ([R-SLB-05], §20.2). I
packed with no gaps:

```
[0,16)      front signature block                      §6.1, fixed
[16,46)     L1 tile 0 payload, 30 bytes                free placement
[46,76)     L1 tile 1 payload, 30 bytes
[76,106)    L1 tile 3 payload, 30 bytes
[106,190)   L1 tile-index region, 84 bytes             = 4×20 entries + one 4-byte segment CRC
[190,191)   L2 tile 0, 1 byte
[191,192)   L2 tile 1, 1 byte
[192,193)   L2 tile 2, 1 byte
[193,257)   L2 tile-index region, 64 bytes             = 3×20 + 4
[257,487)   directory region, 230 bytes                = 24+102 + 24+76 record bytes + 4 CRC
[487,512)   pre-trailer pad, 25 bytes                  forced by step 5: pad to the next 64 boundary
[512,576)   trailer                                    F = 576, 576 mod 64 = 0
```

The two layer-record inline payloads came out at 102 and 76 bytes. I checked the
102 by hand against §7.4's field list, the same way §7.4's own worked example
checks its 81: name 4 + the nine scalars from layout through channel count 34 +
2 dimension entries at 18 each + channel `t` (1+1 name, 2 type, 1+4 fill) 9 +
channel `m` 6 + trailing fixed fields 13 = 102, no residue, so the sub-record
sequence is empty ([R-CNT-18]).

The coverage walk of §9.7 gives eleven claimants — front block, six stored-tile
extents, two index regions, the directory, the trailer — pairwise disjoint, every
one inside [16, F−64) except the two the walk claims by membership. Slack total =
25 bytes, exactly the pre-trailer pad. That is the number [R-CNT-21] obliges a
verifier to report.

**What the document fixed, and what it left to me.** Fixed: every field width and
value; every derived count; the index region's internal layout (entry array then
segment CRC array, no padding, [R-IDX-01]); entry order = disk-ordinal order;
padding and pad-bit content; the emission *phases* (payloads before directory
before pad before trailer); the 64-byte trailer alignment and hence F; that the
directory's end be followed by nothing but pad. Left to me: the placement and
order of structures inside step 2; whether to leave gaps; `file_id` (any nonzero,
SHOULD be random); the record order inside the directory ([R-CNT-14]); tile
extents; layout; codec and filter; which all-fill tiles to sentinel; slack
content (SHOULD zero). Nothing in the creation walk left me unable to emit a byte.

---

## 3. The append procedure

### 3.1 Concrete second commit

Commit 2 supersedes L1's tile 0. Following §20.3's numbered steps:

1. **Establish F** by validating the trailer in the final 64 bytes ([R-LIF-04]).
   F = 576. Physical length equals it, so no truncation is owed.
2. **Open** per §19.1 — the appender is a reader here.
3. **Validate what the commit touches** per [R-WRT-03]: the trailer and the full
   directory always, plus §19.3's layer validation for L1, plus the §19.4 index
   chain for every segment whose entries I reuse. Because step 4 re-emits the
   region *in full*, I reuse every entry, so I verify L1's whole chain
   (`crc_of_crc_array`, then segment 0). L2 is untouched: nothing owed.
4. **Write payloads and indexes** beginning at exactly 576.

```
[576,606)   new L1 tile 0 payload
[606,690)   L1's whole index region re-emitted, 84 bytes
            entry 0 re-pointed and re-crc'd; entries 1,2,3 byte-identical at
            their disk-ordinal positions; segment CRC recomputed
[690,920)   directory: L2's record byte-identical ([R-WRT-05]); L1's record
            modified in two places — its header's extent_offset, and its inline
            payload's crc_of_crc_array
[920,960)   pad
[960,1024)  trailer, F = 1024
```

ΔF = 448 ≥ 128, as §9.2's Note derives. I re-derived that floor: dir_offset ≥
prior F, dir_length ≥ 4, dir_offset + dir_length ≤ new F − 64 gives new F ≥
prior F + 68; both are multiples of 64, so ≥ prior F + 128. Correct.

Worth recording because §20.4 leans on it: a commit that supersedes a stored
tile *necessarily* modifies that layer's record twice over — the extent slot
moves and `crc_of_crc_array` changes — which is what makes the MU=0/PE=0 drop
permission reachable.

5. **Re-emit the directory** per §20.4, then its CRC.
6. **Commit**: barrier; pad; trailer with the same `file_id`, ignore-lane bits
   copied forward, `version_minor` per [R-CNT-26]; barrier.

**Durability order.** Steps 1–3 durable before step 5 writes a byte (step 4's
barrier); the trailer durable at step 6. Both barriers, not one — §20.2 and §20.5
both say so explicitly for creators and compactors, and [R-LIF-02] states it for
every commit. The commit becomes *visible* the instant the trailer bytes land at
the physical end (that is what [R-LIF-05] makes a reader's snapshot) and
*durable* at step 6. The document does not name a "commit point" in those words;
the pair of facts above is what it gives, and it is enough.

### 3.2 Appending to a file whose records I do not all understand

§20.4 governs. Persistence attaches to every record type; only the source of the
flags differs. Three sources: the §7.3 registry for a registered type; the
definition the updater implements the type from, for an unregistered type it
does implement; the stored bits, only for a type it does not implement
([R-CNT-22], [R-CNT-15]).

Walking every flag combination, for a type my updater does **not** implement:

| MU | PE | Top-level record | Layer sub-record |
|---|---|---|---|
| 1 | 1 | **No commit at all.** [R-CNT-15] makes an unimplemented top-level MU=1 record reject-file, and an updater is a reader first (§2.3). A compactor MUST refuse ([R-WRT-06]). | Retain byte-identical; MUST NOT modify **that layer**; other layers stay editable ([R-CNT-18]). A compactor MUST refuse the whole file. |
| 1 | 0 | Not emittable ([R-CNT-12]); read as PE = 1, so treated exactly as the row above. A verifier records it (F25 / L46). | Same. |
| 0 | 1 | Retain byte-identical, extent content unmodified. May not be relocated: [R-WRT-08] permits relocation only under §20.5, and [R-WRT-05] requires the *extent slot* to be re-emitted byte-identically. | Same. |
| 0 | 0 | Retain byte-identical, or drop it (extent → slack), but an appender may drop it **only** in a commit that *independently* changes the file's layer set, any layer record's content, or another non-layer top-level record. A compactor may drop it whenever it rewrites. SHOULD report the loss. | Same, with the scope list being that layer's record, the entry set of its index, or which of its tiles are stored. |

Two things I had to reason out rather than read off. First, the "independently"
guard is not circular: dropping the record, or dropping another record in the
same commit, is not itself a qualifying change, so a commit whose only effect
would be the drop MUST retain it. A no-op commit — legal, §5.1 says a commit that
touches no layer re-emits directory, pad and trailer alone — therefore cannot
drop anything. Second, a commit that edits the *file-scope* user-metadata
document licenses dropping a top-level MU=0/PE=0 record ("another non-layer
top-level record") but does **not** license dropping any layer sub-record, whose
list names only that layer's own structures. Both fall out of the table read
carefully; neither is stated in those words.

**What an updater must never do.** Repair a defect in a structure it carries
forward ([R-LIF-01] freezes the prefix, §20.3 step 2 says so in terms);
re-encode a record whose type it does not implement ([R-WRT-08]); clear unknown
ignore-lane bits ([R-CNT-08]); remove a layer record or a user-metadata record at
either scope (§20.4); relocate a live index region (§20.3 step 4 — that is
compaction's operation).

The one genuinely surprising position, stated consistently in four places
([R-CNF-06], [R-WRT-01], §20.3 step 2, §20.4), is that a **conforming appender
may emit a file that is not a conforming file**: an appender that meets a
malformed index entry while re-emitting a region carries it forward
byte-identically at its disk-ordinal position, and "reproducing a structure's
bytes unchanged is not authoring them". I looked hard for a contradiction with
[R-CNF-05] and there is none: [R-CNF-05] binds *writers*, and §2.3 scopes an
updater's writer obligation to "the bytes it produces". The asymmetry with a
compactor — which MUST NOT emit a file carrying a violation *it has detected* —
is deliberate and stated.

---

## 4. Slack, by commit shape

| Shape | Which bytes become slack | Counted by | Permitted content |
|---|---|---|---|
| **Append (new layer)** | The prior generation's directory region, its pad and its trailer; plus any alignment gaps this commit leaves. Sized by the file's layer count, never by any layer's data. | A verifier, as F less the bytes its §9.7 walk claims ([R-CNT-21]). | Unconstrained. Writers SHOULD zero the gaps *they create* — [R-CNT-03] names the run before an aligned tile or slab run and the pre-trailer pad, and that narrowness is right: superseded bytes lie below the new F and [R-LIF-01] forbids touching them. |
| **In-place update (supersede a tile)** | The superseded payload extent, that layer's entire prior index region, and the prior directory/pad/trailer. | Same. | Same. |
| **Rewrite / compaction** | Nothing is *carried*: the output holds only structures reachable from the input's live trailer. But the output still has its own pre-trailer pad and any alignment gaps, which §5.2 classifies as slack — a compacted file's slack total is not zero. | Same. | Same. |
| **Shrink** | The de-addressed tiles' extents ([R-CNT-21]), plus the usual per-commit directory/pad/trailer and the re-emitted index region. §20.3 adds a SHOULD to write a new file instead where a commit would strand a large share of a layer's stored bytes. | Same. | Same. |
| **Abandoned partial write** | *None, and no total is owed.* This is the case I had to reason out. The physical file exceeds any valid F, so §6.2's ordered gates reject the file (F8 on the magic, or F17 on the length cross-check). §5.2 is explicit: where that ordered validation rejects before a live trailer is established "there is no F and no live state to walk, so the total is not owed at all". The residue is not slack; it is bytes of a file that has no live state. |

Two refinements the text supplies and I would otherwise have got wrong. A
verifier's total is **partial** — an upper bound, naming what stopped the walk —
whenever a scope-level rejection ends an enumeration or the verifier stops at the
first violation ([R-CNT-21], [R-LIF-08]). And an index entry §15.3 classifies
reject-tile on a *structural* ground contributes no stored extent, so the bytes
it nominally addressed fall to slack without making the walk incomplete; an entry
whose only defect is that its stored bytes fail its crc keeps its extent and its
place in the walk.

---

## 5. Torn-write recovery — five crash points

Throughout: a reader takes the trailer at the physical end or fails
([R-LIF-05]); it MUST NOT scan backward. A file with no valid trailer in its
final 64 bytes is not a conforming file, because [R-CNT-01] makes the file size
of a conforming file equal to the live trailer's F.

**A. Crash after the front block, before any payload (creation).** Physical
length 16. Next reader: [R-CNT-27]/F5 — below the 128-byte floor, reject-file at
open. Next updater: [R-LIF-04] — trailer validation fails, the file is torn, no
append, recovery is a separate deliberate operation. Not conforming. §9.6's probe
"begins at the largest 64-aligned offset o with o + 64 ≤ the physical file
length", and at length 16 there is none, so the probe enumerates nothing — see
finding **writer-06** for what the tool is then obliged to report.

**B. Crash after payloads, before the directory.** The final 64 bytes are payload.
Almost certainly F8 (trailer magic) at open. If the payload happens to mimic a
trailer at the exact physical end, §6.2's Note routes it to the directory CRC
(F20); §21.6's row is the careful version — the mimic is inert because nothing
enumerates slack, and a recovery tool re-verifies its output whole, "which
catches any mimic that is not itself a consistent generation". Not conforming.
Recovery: for a creation there is no earlier state to find; for an append the
probe finds trailₙ and truncating to it restores the file exactly.

**C. Crash after the directory and its CRC, before the trailer (between steps 4
and 5).** Indistinguishable from B to a reader: no trailer at the end, F8,
reject-file. This is the case §9.2's figure draws — trailₙ intact but no longer
at the file's end. Recoverable, not readable. Not conforming.

**D. Crash mid-trailer.** The physical length is F − k for some 0 < k < 64, so the
"final 64 bytes" straddle the pad and the partial trailer: the magic check fails
at offset (length − 64), which lands inside zeroed pad. F8. Not conforming.
Recovery as in C.

**E. Crash after step 5 wrote the trailer but before step 6's barrier, with
steps 1–3 not actually durable.** The trailer is valid and at the end; the file
*opens*. The directory bytes may be garbage → F20 at open, reject-file. §9.2's
Note names exactly this degradation: "safety degrades from 'torn commits are
invisible' to 'torn commits are detected'". The prior generation is still
recoverable by probing backward. Not conforming.

**F. The `[R-LIF-04]` overwrite-then-truncate window.** A writer that chose
"overwrite from F and truncate no later than step 6" has, between step 5 and step
6, a physical file longer than the new F with the new trailer buried mid-file. A
crash there leaves stale bytes at the physical end. The probe begins at the
largest 64-aligned o with o + 64 ≤ the physical length and works backward; the
new trailer at F_new − 64 satisfies both of §9.6's conditions (CRC verifies,
committed_file_length = o + 64), so the tool settles on it and truncates
correctly — provided nothing nearer the end also satisfies them. If the stale
residue contains an older *complete* commit state, the probe finds that one first
and whole-file re-verification is what has to reject it; §9.6 requires exactly
that re-verification and names the residual rollback hazard as needing
out-of-band state. I could not construct a case the document leaves undecided
here.

---

## 6. Byte-divergence catalogue, and Appendix G item by item

Given identical input arrays and identical stated options, here is every way I
can make two conforming writers disagree on bytes, with the Appendix G item that
closes it.

| # | Degree of freedom | Rule that leaves it open | Closed by |
|---|---|---|---|
| 1 | Encoder output for codecs 2–4, including a raw DEFLATE stream's unused final-byte high bits (§17.2's Note: "This specification constrains them nowhere") | [R-CNF-05] | item 1, by pinning the implementation and settings |
| 2 | `file_id` — any nonzero value | §6.2, §9.3 (advice only) | item 2 |
| 3 | Structure placement and emission order inside [R-LIF-02] step 2 | [R-SLB-05] | item 3 |
| 4 | Gap *extent* — how much space a writer leaves between structures | [R-SLB-05] | item 3 |
| 5 | Gap *content*, including the pre-trailer pad | [R-CNT-03] is a SHOULD; [R-CNT-21] constrains nothing | item 3, which takes the advice as a requirement |
| 6 | Record order and sub-record order in the directory | [R-CNT-14] | item 3 |
| 7 | Number of generations | §9 constrains nothing | item 4 |
| 8 | Declared alignment A and slab S/A_slab | §16 leaves both to the writer | item 5 |
| 9 | Filter value (1 or 2) | [R-COD-09] | item 5 |
| 10 | Whether an all-fill tile is stored or sentinelled | no rule requires either | item 6 |
| 11 | The fill a writer records when its caller chooses none | [R-TYP-10] is a SHOULD | item 7 |
| 12 | `version_minor` and `flags` | [R-CNT-26] is a SHOULD; [R-CNT-08]'s flags=0 is a MUST for a creator but a compactor carries bits forward | item 8 |
| 13 | JSON serialization of a user-metadata document; the storage encoding (1 or 2); the zstd settings under encoding 2 | [R-MTA-05] sorts members but §18.2 disclaims cross-writer byte-identity outright | item 9 |
| 14 | Unicode normalization of names | [R-ENC-14] is a SHOULD | item 10 |
| 15 | **Tile extents and channel layout** | §11.3's Note ("Tile extents are a writer's choice, and this specification imposes none"); §14.1 leaves layout free | **nothing** — see finding **writer-04** |

Things I checked and found *not* to be degrees of freedom, so that the list above
is not padded: storedness beyond the all-fill case is forced by [R-MDL-02] (a
tile carrying a non-fill sample must be stored, or the reference array is wrong);
the segment-CRC array and `crc_of_crc_array` are forced; `entry_count` and the
index `extent_length` are forced by [R-CNT-17]; `dir_offset`, `dir_length` and
`committed_file_length` follow from the order once item 3 fixes it; the trailer's
reserved 12 bytes are forced to zero; a registered type's flag bits are fixed by
§7.3; [R-IDX-05]'s licence to emit `0xEECB3BB2` without computing it produces the
same bytes as computing it, so it is not a divergence at all; `linearization` and
`index_encoding` each have exactly one legal value.

I also verified item 3's tie-breaking claim rather than taking it. Two records
that its key does not separate are byte-identical in type, flags, lengths,
payload and extent content, differing only in `extent_offset`; since the two
extents are equal-length and equal-content, swapping them in the emission order
puts identical bytes at both offsets and puts identical bytes in the directory,
so "emitting them in either order yields the same file" is true. And item 5's
identity condition — the byte-shuffle is the identity exactly where s = 1 or
n = L/s = 1 — I checked algebraically: the permutation sends byte i of group j
to i·n + j, and for s ≥ 2 and n ≥ 2 the byte at source offset s lands at offset
1 ≠ s. Correct. The *second half* of that same sentence is not: see finding
**writer-03**.

---

## 7. §21.7's test, put to work

The brief asked me to apply the section's test to a dozen requirements and to
report where it works as well as where it fails. §21.7 defines:

> A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it
> by any check this specification obliges a reader or a verifier to perform. It
> is **detectable** in the contrary case: where some file exhibiting it is
> separated by such a check from every file that does not.

Writing the quantifiers out, with X = files exhibiting the condition, Y = files
not exhibiting it, sep(f,g) = "some obliged check distinguishes f from g":

```
unwitnessed:  ∀f ∈ X.  ∃g ∈ Y.  ¬sep(f, g)
detectable:   ∃f ∈ X.  ∀g ∈ Y.   sep(f, g)
```

These are exact negations, including in the degenerate case X = ∅ (unwitnessed
holds vacuously, detectable fails) — so the duality claim holds under this
reading. It does not hold under the *other* available reading of "separated by
such a check from every file that does not", which is finding **writer-05**.

I also satisfied myself that "separated" must mean "some individual check's
result differs", not "the two get different verdicts" — because Y includes files
that are nonconforming for unrelated reasons and would share a reject-file
verdict with f. Under the verdict reading almost nothing would be detectable and
the register would be nearly empty. The document does not say which is meant; the
finer reading is the only one that makes the register's 120 rows correct, so I
adopted it.

Twenty-odd requirements put to the test, and what it says:

| Requirement | Verdict | Register |
|---|---|---|
| [R-LIF-02] steps 4 and 6, the storage barriers | Not a condition a file can exhibit — durability is not a property of a byte sequence | absent ✓ |
| [R-LIF-01] committed-prefix immutability | Same — needs two states to state | absent ✓ |
| [R-WRT-05] byte-identical re-emission | **Unwitnessed.** The witness (the superseded directory) is physically in slack, and no obliged check reads slack | absent ✓ |
| [R-CNT-08] an updater clearing an ignore-lane bit | Unwitnessed, same reason | absent ✓ |
| [R-WRT-08] re-encoding an unimplemented record | Unwitnessed, same reason | absent ✓ |
| [R-COD-10] mis-strided filter, no structural constraint broken | **Unwitnessed** — §21.7 names it | absent ✓ |
| [R-COD-10] mis-strided filter breaking padding or bool bytes | **Detectable** by a verifier | T26 ✓ |
| [R-COD-06] undisclosed compression dictionary | **Unwitnessed** — §21.7 names it, [R-COD-06] agrees | absent ✓ |
| [R-COD-06] nonzero dictionary ID | Detectable from the frame header | T19 ✓ |
| [R-SER-05] padding content / pad bits | Detectable — a verifier MUST check | T4, T5 ✓ |
| [R-SER-08] interleaved bool byte | Detectable — verifier | T2 ✓ |
| [R-MTA-05] unsorted members | Detectable — verifier | F27, L48 ✓ |
| [R-CNT-22] stored flags vs registry | Detectable — verifier | F28, L49 ✓ |
| [R-CNT-04] front block, reader exempt when non-resident | Detectable, because a verifier holds no exemption (§2.3) | F6, F1 ✓ |
| [R-CNT-05] a structure in the pre-trailer gap | Detectable — verifier | F7 ✓ |
| [R-CNT-05] a pre-trailer gap *longer* than step 5's pad | Detectable, but expressly **not a violation** (§2.3, §6.2) | absent ✓ |
| [R-CNT-18] sub-record nesting | No condition a file can exhibit in major 1: the only sub-record payloads are one byte, opaque, or already L26 | absent ✓ |
| [R-ENC-06] fixed field widths | No condition a file can exhibit — §21.7 says so | absent ✓ |
| [R-EXT-03] emitting an experimental value in released software | Conduct, expressly not a file property ([R-CNF-02], §21.6) | absent ✓ |
| [R-EXT-03] emitting a reserved-range value | Detectable | F35/F36, L24/L25, and L31/L33/L34/L36/L43/L45/R1 ✓ |
| [R-MTA-06] an unregistered `tarn.` key | Conforming by §21.6; conduct rule | absent ✓ |
| [R-CNT-03], [R-TYP-10], [R-ENC-14], [R-CNT-26], [R-LIF-07] | SHOULDs — not violations at all ([R-CNF-12]) | absent ✓ |
| §20.3 step 4's §14 bar, where the commit also unstores the damaged tile | **Unwitnessed** — §20.3 says so in terms ("the live state being clean") | absent ✓ |
| [R-WRT-06]'s "MUST mint a fresh `file_id`" | Relational across two files; neither §21.7 category names it, though the outcome (absent) is right | absent |

The test decided every one of these, and in each case its answer agrees with the
register. I could not construct a requirement it decides *wrongly*. The nearest
thing to a miss is the last row: a compactor reusing its input's `file_id`
produces a conforming file whose defect is a relation between two files. §2.3's
conduct class names only "where a value is published, or which registry version a
writer targets" plus two expressly-declared cases, and §21.7's two categories are
"unwitnessed condition" and "requirement stating no condition a file can
exhibit". A cross-file relation is arguably the second, but nothing says so. I
judged this too thin to report as a finding and record it here instead.

I also checked the register in the reverse direction — is every row a *detectable
file-conformance violation*? — going row family by row family. Every verifier-detected
row is backed by a rule that says a verifier MUST check it ([R-SER-05],
[R-SER-08], [R-SLB-01], [R-SLB-03], [R-CNT-12], [R-CNT-22], [R-CNT-13],
[R-CNT-05], [R-MTA-05]). T13, T15, T16, T23 and T26 are causes whose detecting
check is another row's; each row says so. No row struck me as unexhibitable.

---

## 8. Counts and cross-checks I derived myself

Everything in this table I computed from the document's own text and compared
against a figure the document states.

| Derived | My value | Document |
|---|---|---|
| Register rows across §21.2–§21.5 | 120 | "120 conditions" (§21.8) ✓ |
| Rows per subsection | 35 / 49 / 26 / 10 | 35 / 49 / 26 / 10 ✓ |
| Instances, counting semicolons and treating `—` as one | 275 | "275 instances" (§21.8) ✓ |
| Instances per subsection | 56 / 116 / 55 / 48 | not stated |
| Conditions [R-CNT-06] states (rows citing it as governing) | 9 — F8, F9, F10, F12, F13, F14, F15, F16, F17 | "[R-CNT-06] states nine" (§2.3) ✓ |
| Of those, reaching a foreign major | 2 — F8 (magic), F14 (CRC) | "the other seven do not" (§2.3) ✓ |
| Rows reaching a foreign major overall | F6, F8, F14, and F1's two instances | "and no other row" (§21.2) ✓ |
| L1 inline payload, my worked layer | 102 bytes, no residue | method matches §7.4's own 81-byte worked example ✓ |
| §7.4 worked example field arithmetic | 4 + 34 + 18 + 12 + 13 = 81 | 81 ✓ |
| §7.4 index extent_length | 4×20 + ⌈4/2¹⁶⌉×4 = 84 | 84 ✓ |
| §15.4 example: segments at entry_count 1,000,000 | 16 (15 full, last covers 16,960) | ✓ |
| §15.4 example: index region size | 20,000,064 bytes | 20,000,064 ✓ |
| §15.4 example: tile 999,999 segment-relative byte | 339,180 | 339,180 ✓ |
| §15.4 example: CRC array range / segment 15 range | [20,000,000, 20,000,064) / [19,660,800, 20,000,000) | ✓ |
| §15.4 example: full segment size | 1,310,720 = 1.25 MiB | 1.25 MiB ✓ |
| §21.9 Note: CRC array at entry_count 2³² | 65,536 segments × 4 = 262,144 = 256 KiB | 256 KiB ✓ |
| §21.9 Note: at 2³⁶ | 4,194,304 = 4 MiB | 4 MiB ✓ |
| §17.3 worked shuffle of 1.0, 2.0, 3.0 | `00 00 00 00 00 00 80 00 40 3F 40 40` | same ✓ |
| §11.4 example: planar disk ordinal | 2·32 + 10 = 74 | 74 ✓ |
| §15.4 example: channel 3's ordinals | 96–127 | 96–127 ✓ |
| §14.5 example: edge tile at (1,1) with E=(5,5), T=(4,4) | 1 real + 15 padding positions, 32-byte tile | ✓ |
| §14.2 example: interleaved (2,3), uint8+uint16 | Q=3, decoded size 18, ordinal 5 at bytes [15,18) | ✓ |
| §14.4 Note at P = 1: planar and interleaved bool images coincide | only when fill is false (fill true gives 0xFE/0xFF vs 0x00/0x01) | "exactly when that fill is false" ✓ |
| §17.2 Note: minimum zstd Window_Descriptor value | 1 << (10 + 0) = 1024 = 1 KiB | "cannot express less than 1 KiB" ✓ |
| §9.2 Note: minimum ΔF per commit | prior F + 68 rounded up to a multiple of 64 = prior F + 128 | 128 ✓ |
| My commit 2 | ΔF = 448 | ≥ 128 ✓ |
| My built file | F = 576, 11 claimants, 25 slack bytes | consistent with §5.2, §9.7 |
| Every decoded size is at least 1 byte | P ≥ 1, Q ≥ 1, ⌈P/8⌉ ≥ 1 | "§14's decoded sizes are at least 1 byte" (§17.2 Note) ✓ |

I also checked §21.1's instance-derivation rules against individual cells rather
than only the total: L21 (2 layout formulas × 2 magnitude directions = 4), L22
(2 directions + 2 stated alternatives = 4), T3/T14/T22 (3 layout formulas × 2
directions = 6 each), T21/L44 (3 formulas × one direction, because the text says
*exceeds*/*larger than* = 3 each), L30 (2 directions), F26 and F19 (a bit family
stated as one instance, per the T24 precedent), L47 (the same family in two
containers = 2), L23 (4 regions, with "overrun or truncation" correctly *not*
doubling because they name one predicate over a given region), F29 and L14
(three genuinely distinguishable states). Every cell I checked follows the stated
rules. I also verified all six named strict-specialization pairs (F1⊂F6, F1⊂F8,
F35⊂F36, L24⊂L25, F21⊂F22, L10⊂L11) and found the instance-level qualifier
doing real work: L46 is strictly narrower than L49 at its *layer record* instance
but not at its *sub-record* instance, which is exactly what "at a given instance
of it, where the row enumerates several" is for.

---

## 9. Findings

### writer-01 — [R-WRT-07] keys index-region regeneration to the region moving, when what forces it is the *tiles* moving

**Kind:** AMBIGUITY. **Location:** §20.5, [R-WRT-07].

> "A compactor MUST preserve content, and preserves no placement — placement is
> not among the things it carries forward, and it is free to place structures
> anywhere §5.2 admits and every declared layout invariant permits
> (`[R-SLB-01]`, `[R-SLB-03]`): every stored tile's bytes verbatim — each index
> entry's crc is unchanged — and every retained record per §20.4, except that
> relocation re-points extent slots, regenerates each relocated tile-index region
> (entry offsets new; entry lengths, entry crcs, and sentinel entries unchanged;
> segment CRCs recomputed over the entries as re-emitted), and updates the
> layer-record fields covering a regenerated region (crc_of_crc_array)."

The obligation to regenerate is triggered by the *region* being relocated. But
what makes regeneration necessary is that the region's **entries** now name the
wrong offsets — that is, that the layer's *stored tiles* moved. The same sentence
grants a compactor free placement of every structure independently, so the two
can come apart: a compactor may leave layer A's index region at the byte offset
it occupied in the input while placing A's stored tiles elsewhere. Under the rule
as written it then owes no regeneration and re-emits entries pointing at the
input's offsets.

Permitted readings: (a) regenerate exactly the regions that moved — the literal
text; (b) regenerate every region whose layer's stored tiles moved — the
substance. I picked (b): the parenthetical "entry offsets new" is only
meaningful under (b), and [R-WRT-07]'s closing sentence ("The output's reference
arrays MUST equal the live generation's bit for bit") is unsatisfiable under (a)
in the divergent case. An implementer who takes (a) and happens to hit the
coincidence emits stale entries.

**Byte-level: no.** Under (a) the output's entries point at bytes that are no
longer that tile's, so its entry crc fails (T1) and the coverage partition
breaks — the file is nonconforming, and [R-CNF-05]/[R-CNF-06] bar every
conforming actor from emitting it under both readings. The emittable set does
not move; what moves is how much a careless compactor has to be told.

### writer-02 — [R-ERR-04] scopes a resource decline by "declarations", and two other rules apply that clause to quantities that are not declarations

**Kind:** AMBIGUITY. **Location:** §21.9 [R-ERR-04]; §17.2 [R-COD-06]; §18.2.

[R-ERR-04]:

> "A file exceeding any of these remains conforming, and a reader MAY decline
> it — at the whole file, or at the narrowest scope whose declarations exceed
> what it can serve, a layer or a tile."

[R-COD-06], on a zstd frame's `Window_Size`:

> "a wider window is conforming and merely permits a conforming reader to decline
> the tile or the layer on resource grounds (`[R-ERR-04]`)."

§18.2, on a user-metadata document's decoded size:

> "a reader that instead declines on resource grounds under `[R-ERR-04]` does so
> at the whole file, a document having no declared size and so no narrower scope
> whose declarations that rule can measure."

Three treatments of one clause. §18.2 reads "declarations" strictly — a quantity
with no *declared* size forces the decline to the whole file. [R-COD-06] applies
the same clause to a frame's `Window_Size`, which is not declared anywhere in a
layer record either; it lives inside the tile's stored bytes, and under §18.2's
own reasoning would force a whole-file decline, yet [R-COD-06] offers "the tile
or the layer". And "the layer" is in any case not "the narrowest scope" when the
tile is the scope whose bytes carry the offending value.

Readings: (a) "declarations" means anything the file states, including a frame
header, so a tile is a scope whose declarations can exceed — but then §18.2's
argument for the whole-file decline loses its premise, since a document's
*extent* is likewise a stated length; (b) "declarations" means the layer record's
fields, which is how §19.3 uses the word ("before any use of the layer's
declarations") — but then [R-COD-06]'s tile-scope decline is unlicensed. I
picked (a) for the window and treated §18.2's whole-file rule as the special case
it declares itself to be, because a tile's decoded size is derived from layer
declarations and only the window is tile-local.

**Byte-level: no.** Every reading leaves the reader free to decline at the whole
file, so no file moves between "must accept" and "may reject"; only the
granularity of a permitted refusal is in dispute, and [R-ERR-04]'s reporting
requirement is the same either way.

### writer-03 — Appendix G item 5 claims the byte-shuffle changes every tile it touches; it does not

**Kind:** OBSERVATION. **Location:** Appendix G, item 5.

> "The filter is the identity exactly where its permutation is — where the
> stride is 1, as for a packed boolean plane, and equally where the decoded image
> is a single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the
> stored bytes of every tile it touches."

The first half is exactly right and I verified it algebraically. The last clause
is false. A permutation of bytes fixes any string invariant under it, and those
are common in this format rather than exotic:

- an all-zero decoded image — a float32 plane of `+0.0`, or any tile whose
  channels all carry the all-zero fill at every position — is fixed by the
  shuffle at any stride (I checked: 12 zero bytes at s = 4 are unchanged);
- at s = 2, n = 2 the permutation is the transposition of the middle two bytes,
  so `01 02 02 03` is fixed while `01 02 03 04` becomes `01 03 02 04`.

Because §14.5 forces every padding position to carry fill, padding-heavy edge
tiles are systematically more likely to be fixed points than arbitrary data would
be. The claim as written would tell an implementer that a stored tile's bytes are
a witness to which filter produced them, which they are not.

The item's *conclusion* — pin the filter value, because "no content implies it"
— is correct and unaffected; only the supporting universal is wrong. Appendix G
is non-normative, but this is a claim in the reproducible-writer material that a
reader can act on, which is why it is reported.

**Byte-level: no.** The profile adds no requirement to any actor ("a writer
ignoring it is fully conforming"), and the emittable set is fixed by [R-CNF-05]
independently of it.

### writer-04 — Appendix G claims to close the degrees of freedom this format leaves open, and closes neither of the two its own item 2 names beside the codec

**Kind:** OBSERVATION. **Location:** Appendix G, preamble and item 2.

Preamble:

> "Applications that need byte-identical output — content-addressed storage,
> reproducible builds — can adopt this profile, which closes the degrees of
> freedom this format deliberately leaves open."

Item 2, on why the `file_id` hash must be over emitted bytes:

> "this format fixes no canonical serialization of logical content, and two files
> carrying the same arrays can legitimately differ in tiling, layout, and codec."

Three freedoms named there. Item 1 closes the codec by pinning the implementation
and settings. Item 5 closes the filter, which item 2 did not name. **Nothing
closes tiling or layout.** §11.3's Note is explicit that "Tile extents are a
writer's choice, and this specification imposes none", and §14.1 leaves layout to
the writer; two writers given the same arrays and the same *stated options*, if
tile shape and layout are not among the stated options, produce entirely
different files while satisfying every one of the ten items. The closing
paragraph's inventory of what the items add — gap content, gap extent, record
order, the default fill, the all-fill sentinel, a single generation, alignment
and slab, `version_minor`, a derived `file_id`, NFC names, producer pinning —
omits tiling and layout as well, and also omits the filter that item 5 does pin.

The natural repair is the one item 5 already models for alignment and slab
("**No declared alignment and no slab**, or fixed declared values"): fixed
declared tile extents and a fixed layout. The alternative repair is to say
explicitly that tiling and layout are inputs to the profile rather than freedoms
it closes — but item 2's own sentence frames them as freedoms.

**Byte-level: no,** for the same reason as writer-03: the profile binds no actor
and [R-CNF-05] already licenses the divergence.

### writer-05 — §21.7's duality claim holds under only one of two available scopings of its own existential

**Kind:** AMBIGUITY. **Location:** §21.7, [R-ERR-01]; restated in §21.1.

> "A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it
> by any check this specification obliges a reader or a verifier to perform. It
> is **detectable** in the contrary case: where some file exhibiting it is
> separated by such a check from every file that does not. The two are stated
> over the same subject, and each quantifier is the other's dual, so each is
> exactly the negation of the other"

The unwitnessed clause is unambiguous: the check quantifier is innermost and
universal ("cannot be told apart ... by **any** check"), giving
∀f ∃g ∀check ¬sep. Its negation is ∃f ∀g ∃check sep — the separating check may
differ from one g to the next.

The detectable clause is not. "separated by such a check from every file that
does not" admits both ∃f ∀g ∃check sep (the dual) and ∃f ∃check ∀g sep (one
check separates f from all of Y). The second is strictly stronger, so under it
the two definitions are *not* exact negations and §21.7's stated duality fails.

I picked the dual reading, because §21.7 asserts the duality and §21.1's
restatement — "some file exhibiting it is separated, by a check this
specification obliges a reader or a verifier to perform, from every file that
does not" — carries the identical ambiguity and so cannot settle it. The two
readings coincide on every condition I could construct, since a condition's own
check separates its witness from all of Y at once; but the document leans on the
duality as a stated result ("so an unwitnessed condition is absent from it by
that clause's own terms rather than in breach of them"), and a result that turns
on which of two parses a reader takes is not a result. One word — "some" before
"such a check", or "any" — settles it.

**Byte-level: no.** Nothing about which files exist or how they are judged turns
on it; what turns on it is whether §21.1's completeness clause and §21.7's test
are provably the same gate, which is a claim about the document.

### writer-06 — [R-LIF-06] obliges a recovery tool to report the candidate it settled on, in cases where it settles on none

**Kind:** OBSERVATION. **Location:** §9.6, [R-LIF-06].

> "The probe begins at the largest 64-aligned offset o with o + 64 ≤ the physical
> file length; a candidate whose whole-file re-verification fails was not a
> commit state, so the tool continues the probe past it, and MUST report the
> candidate it settled on and how many it rejected."

Two reachable states leave no candidate to settle on, both of them ordinary
outcomes of the crash walk in §5 above:

- a physical file shorter than 64 bytes — my crash point A leaves exactly 16 —
  for which there is no 64-aligned o with o + 64 ≤ the length, so the probe
  enumerates nothing at all;
- a file every one of whose candidates fails whole-file re-verification, which
  the same sentence contemplates ("the tool continues the probe past it") and
  which terminates at offset 0 with nothing settled.

In both, "the candidate it settled on" has no referent, and the document does not
say what the tool reports instead. This matters to the operator-facing half of
the recovery story: "no recoverable commit state, N candidates rejected" and
"here is the state I recovered" are opposite messages, and only the second is
specified. The rejected count remains well defined in both cases.

**Byte-level: no.** [R-LIF-06] binds recovery tools, which §2.3 does not make a
conformance class, and §9.6 is explicit that "no verdict turns on the probe".
Nothing about which bytes are emitted or accepted changes.

### writer-07 — [R-SLB-04]'s trigger is quantified over changes to the tiles, never over changes to the declaration, so introducing or altering a slab declaration falls outside it

**Kind:** AMBIGUITY. **Location:** §16.2, [R-SLB-04]; §20.3 step 4.

> "A writer or updater whose commit changes the stored-tile set, the run
> partition, or the byte placement of any run of a slab-declared layer MUST
> either re-establish the invariants for every such run — or clear the
> declaration in the new generation; carrying a stale declaration forward is a
> validity error at layer scope"

[R-SLB-03]'s invariants turn on two things: the placement of the stored tiles,
and the declaration (S, which fixes the run partition, and A_slab, which fixes
what the first stored tile of each run must be aligned to). [R-SLB-04]'s trigger
names only the first. Two commits it does not reach:

- a commit that **introduces** S ≠ 0 and A_slab on a layer that declared none.
  In the superseded generation there is no slab-declared layer and no run
  partition, so nothing "of a slab-declared layer" changed; the stored tiles keep
  their scattered offsets.
- a commit that **changes A_slab** on an already-slab-declared layer, touching
  nothing else. The stored-tile set, the run partition and the byte placement are
  all unchanged; only the alignment the runs must satisfy has moved.

The parallel sentence in §20.3 step 4 treats the alignment case with the
quantifier and the authority this one lacks:

> "Extents this commit supersedes become slack (`[R-CNT-21]`); a slab declaration
> is re-established or cleared (`[R-SLB-04]`), and an aligned layer's stored
> tiles — every one the new state keeps, not only those this commit adds —
> satisfy its invariant or the declaration is cleared (`[R-SLB-01]`,
> `[R-CNF-05]`)."

For alignment: an explicit quantifier over every tile the new state keeps, and an
explicit [R-CNF-05] cite making the whole layer the writer's responsibility. For
the slab: a bare deferral to [R-SLB-04], whose trigger does not reach either
commit above.

Readings: (a) evaluate "slab-declared layer" in the new generation, so
introducing a declaration changes the run partition from none to some and the
rule binds; (b) evaluate it in the superseded generation, so neither commit is
reached and an updater may author a declaration its layer's frozen tiles do not
satisfy. I picked (a), on the strength of §20.3 step 2's doctrine that
"reproducing a structure's bytes unchanged is not authoring them" — by
contraposition an authored declaration is the updater's own output, and §20.3's
alignment clause cites [R-CNF-05] for exactly that proposition. But (b) is what
[R-SLB-04] says, and an implementer reading §16 alone gets it.

**Byte-level: no.** Under (b) the resulting file exhibits L41 or L42 and is
nonconforming, so [R-CNF-05] and [R-CNF-06] bar every conforming actor from
emitting it under both readings; the emittable set does not move. What moves is
whether §16 tells a writer that "declare a slab on an existing layer" is an
operation it must either back with a rewrite of every stored tile or refuse.

---

## 10. Suspicions I opened and closed

These are recorded so that the seven findings above can be read against what was
looked at and rejected.

**The §14 bar omits pad bits.** §20.3 step 4 lists "the set of padding positions
(§11.3) and the content `[R-SER-05]` fixes there" among the things a declaration
change must not alter. Pad bits are emphatically *not* padding positions —
§14.3's Note says so — and §14.5 states them in a separate sentence. Yet §20.3's
shape-(c) Example bars a fill change on a channel carrying "no padding position
and **no pad bit**". I thought this was a gap between the normative list and the
Example. **Closed by:** "The test is the effect on such a tile, and the list
names where that effect arises rather than standing on its own" — the list is
expressly non-exhaustive, and §14.5, which fixes pad-bit content, is inside §14.
The Example agrees with the bar.

**The §14 bar's list bars altering the set of padding positions, and the same
step permits a growth that does exactly that.** An extent growth turns padding
positions of a stored edge tile into real ones; it cannot alter any other item on
the bar's list, since P, Q, the element sizes, the codec and the filter are all
independent of E. So if the list were operative, no growth over a stored edge
tile would be legal. **Closed by:** the same non-exhaustiveness sentence, plus
§20.3's own exact formulation of the permission — "a growth is permitted exactly
where the geometry it produces satisfies every rule that geometry is subject to"
— which leaves the §14 bar imposing nothing additional on a growth. I checked
the justification for degenerate cases too: the fill is a legal in-tile value for
every type, bool included ([R-TYP-05], [R-TYP-07]), and a position that becomes
real in a newly-addressed tile carries no prior-generation obligation.

**May an appender relocate a retained record's extent verbatim?** [R-WRT-05]
requires byte-identical re-emission of "every record it retains and does not
logically modify", and "logically modify" is defined nowhere, so I wondered
whether an appender could declare a verbatim relocation a modification and escape
the rule. **Closed by:** [R-WRT-05] names the extent slot among the bytes that
must be identical, [R-WRT-08] permits relocation of an unimplemented type's
extent "only ... under §20.5", and §2.4's preserve-verbatim row says the bytes
are "relocated only as Part I permits". Relocation outside compaction is barred;
the reading that makes [R-WRT-05] vacuous is not available.

**Does §20.3 oblige an appender to emit a nonconforming file, against
[R-CNF-05]?** Step 2 requires a malformed index entry met while re-emitting a
region to be carried forward byte-identically, "not repaired to a sentinel".
**Closed by:** [R-CNF-05] binds writers; §2.3 and [R-CNF-06] scope an updater to
"the bytes it produces", §20.1 restates it, and §20.3 step 2 states the doctrine
explicitly. The position is deliberate and consistent across four passages.

**§16.2's claim that a stale slab declaration carries no register row of its
own.** The Note asserts "every file exhibiting one exhibits a run whose tiles are
unpacked or whose first stored tile is misaligned". I tried to build a
counterexample where a commit changes the stored-tile set but the invariants
survive by luck. **Closed by:** where the invariants hold, the declaration is not
stale — [R-SLB-04]'s first branch is satisfied trivially — so no file exhibits
the condition without exhibiting L41 or L42. The Note holds. (This is separate
from writer-07, which is about commits [R-SLB-04]'s trigger never reaches at all.)

**§7.4's claim that sub-record nesting has no reader-detectable witness.** The
Note says so, but §21.7's test is stated over checks obliged of "a reader **or a
verifier**", and §2.3 makes a verifier check "every file-level requirement —
including those ordinary readers are exempted from". **Closed by:** the Note's
substantive argument reaches verifiers too — in format major 1 a sub-record's
payload is one byte ([R-MTA-03]), opaque ([R-CNT-15]), or already L26, so no
actor has a payload it is obliged to parse as records. The Note's phrasing is
narrower than the test it invokes; its conclusion is right.

**§20.5's "one row for each of the other seven spaces §10.2 tabulates (L31, L33,
L34, L36, L43, L45, R1)".** I derived the list independently: §10.2 tabulates
eight spaces; excluding record type leaves channel layout (L36), linearization
(L33), sample type (L34), codec (L43), filter (L45), index encoding (L31),
metadata encoding (R1) — seven, exactly as named, and note that channel layout
has no experimental range yet still contributes a reserved-value row. **No
finding.**

**§20.5's "on a conforming input a carried ignore-lane bit ... or an
unrecognized `tarn.` key ... the two of §10.1's four vehicles §21.6 makes
conforming".** I tried to find a third way a conforming input carries a
later-minor feature. Experimental-range record types and metadata encodings are
conforming per §21.6, but they are private use, not later-minor features; a
merely elevated `version_minor` with no feature is conforming and is handled by
"Otherwise version_minor follows `[R-CNT-26]`'s floor". **Closed:** the pair is
right.

**§6.2's Note claiming a trailer-mimic at exact end of file "is caught at the
directory CRC ... detection is never silent".** Against the §22.1 adversary a
mimic can carry a directory whose CRC verifies. **Closed by:** §21.6's row states
the careful version — the mimic is inert, and recovery re-verification "catches
any mimic that is not itself a consistent generation; §9.6's second caution
covers the rest" — and §22.1 stipulates that files which validate are within the
threat model. The Note overstates in a non-normative sentence that the register
row corrects; not worth a row of its own.

**Whether §20.4's flag table lacks a requirement identifier.** It states four
MUSTs and carries none. **Closed by:** [R-CNF-06] identifies it — "MUST honor the
preservation obligations of §20.4" — and §2.4's preserve-verbatim row cites it by
name. §2.2's claim that normative requirements carry identifiers is satisfied in
substance.

**Whether [R-SER-08] is really "the one rule that goes the other way".**
[R-CNT-12] ("a reader or updater encountering it MUST treat the record as
PE = 1") and [R-CNT-22] ("a reader MUST apply a known type's specified semantics
regardless of its stored MU and PE bits") also resolve nonconforming bytes to a
fixed interpretation. **Closed by:** §12.3 fixes the sense — "the one case where
a reader **resolves a byte to a value** rather than passing it through" — and
neither flag rule concerns a value the reader returns. The claim is about
returned sample content and is correct.

**Whether a compactor reusing its input's `file_id` is a condition §21.7's two
categories miss.** Discussed in §7 above; I judged it too thin to report,
recording it there instead.

**Every zero I relied on was pre-tested.** Before treating the absence of a
phrase as evidence I searched for a phrase I knew was in the same passage. For
example, before concluding that nothing outside §20.3 step 4 and [R-WRT-08] bars
an appender from relocating an extent, I ran `relocat` and got eleven hits
including the three that decided the question (lines 300, 3134, 3382) — a search
returning zero would have been worthless because the document hard-wraps and
`relocating a live index region` spans a line break at line 3134.

---

## 11. Confidence

I could implement a conforming creator, appender and compactor from this document
alone, and I did implement a creator on paper down to the byte. The creation
walk left nothing undetermined. The append walk left nothing undetermined except
writer-07's question about authoring a slab declaration, which the resulting
file's own conformance settles even where §16 does not. Recovery left one
reporting gap (writer-06). The byte-divergence catalogue is complete against the
normative text; where it exceeds Appendix G, the appendix is non-normative and
adopting it is optional, so the two findings there (writer-03, writer-04) are
defects in a finding aid rather than in the format.

I found no finding I am willing to grade byte-level. That is a claim about my
lane, not about the round: my charter is the writer and updater path, where
[R-CNF-05] and [R-CNF-06] collapse most disputes — a permissive reading that
would let an updater author a nonconforming file is barred under every reading,
so the emittable set does not move. The places where it *could* move in my lane
are conduct rules that leave a conforming file, and of those I found one candidate
(the §14 bar in its unstore-the-damaged-tile case) which the document states
plainly enough that two competent implementations would not disagree, and one
(a compactor's fresh `file_id`) whose absence from the register I could not turn
into a fork.
