# Round 8 — Verifier implementer, working transcript

**Access disclosure.** I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read cover to cover in four `Read` calls (lines 1–934, 935–1634, 1635–2334,
2335–3034, 3035–3434, 3435–3843). I ran `grep`/`sed`/`awk` against that same
file twice: once to enumerate every occurrence of the string "verifier", once
to count register rows and semicolon-separated Instances cells. I ran five
Python programs; four of them contain only inline literal data (CRC tables,
hex constants transcribed by hand from the document, byte layouts I
constructed), and one (`trace.py`) reads a helper file `gen.py` that I wrote
myself in the scratchpad in the same session. I wrote four binary files
(`gen1.bin`…`gen4.bin`) into the scratchpad and read none of them back through
any tool — the Python that wrote them held the bytes in memory. I opened no
ADR, no plan file, no conformance vector, no registry, no git history, and did
no web access. I listed no directory other than `mkdir -p` of my own output
path.

---

## 0. What I set out to build

A conforming verifier, on paper but concretely: the ordered certification
procedure, the coverage walk with real arithmetic, extent/alignment/slab checks
on adversarial layouts, the checksum inventory with every stated constant
recomputed, the decode obligations, and a four-generation trace.

I built a real file to do it on rather than reasoning abstractly, because the
coverage-walk questions are arithmetic questions and I did not trust prose
answers to them.

---

## 1. The certification procedure, as an ordered algorithm

The document does not state a verifier algorithm in one place. It states a
*reader* algorithm (§19.1 open, §19.3 layer access, §19.4 tile read), a coverage
walk (§9.7), a verdict vocabulary (§2.3), and a register (§21) whose *Detector*
column names twenty rows a reader is exempt from. The verifier algorithm is the
composition. I assembled it as follows, and every step below cites the text that
put it there.

### Phase A — verdict state

Three verdicts (§2.3 `[R-CNF-11]`): *conforming*, *nonconforming*, *cannot
establish*. Plus two report-only vocabularies that are explicitly **not**
verdicts:

- *unexamined* — for scopes a verifier that stopped at the first violation did
  not look at. "*Unexamined* is neither a verdict nor *cannot establish* — it
  constrains the report, not the verdict."
- the per-requirement *unable to check* report — "that per-requirement report
  constrains the report and not the verdict, as *unexamined* does below."

Precedence is fixed and unambiguous: "An established violation takes priority: a
verifier that has established any violation reports *nonconforming*, however
many requirements it was unable to check, and *cannot establish* is available
only to a traversal that established no violation." So the state machine is a
monotone latch: `established_violation` sticks; `unable_to_check` is a set that
only downgrades *conforming* → *cannot establish*.

I implemented it as:

```
violations = []            # each: (row, scope, evidence)
unchecked  = []            # each: (requirement id, ground)
unexamined = []            # each: scope
advisories = []            # SHOULD deviations; §2.4 [R-CNF-12]

verdict = nonconforming        if violations
        = cannot_establish     elif unchecked
        = conforming           else
certify  = (verdict == conforming)
```

`[R-CNF-12]` is what licenses the `advisories` bucket to be inert: "Deviation
from a SHOULD is not a violation for this purpose: §21's register enumerates
MUST-level conditions only, and a verifier reports a SHOULD deviation as an
advisory that does not bar certification."

Grounds for *cannot establish* that §2.3 enumerates: unimplemented format
major; a record with MU = 1 whose type the verifier does not implement (§21.6);
inability to execute a codec or filter (`[R-COD-11]`); a decode declined on
resource grounds (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`); a user-metadata
document the verifier declines to decode (`[R-MTA-09]`). The list is introduced
with "as when", so it is illustrative, not closed. I return to what else it
might reach in §8 below — that turned out to be the sharpest question in §2.3.

### Phase B — file open (the reader path, §19.1, with the verifier's additions)

1. **Size.** Obtain the transport-authoritative F (`[R-CNT-10]`). Physical size
   below 128 → F7, reject-file (`[R-CNT-27]`).
2. **Front block.** Fetch [0, 16) *unconditionally*. §19.1 and `[R-CNT-04]`
   permit a reader that would need an extra range request to defer or omit the
   equality check, but §2.3 defines a verifier as a reader "that additionally
   checks every file-level requirement — including those ordinary readers are
   exempted from", and F8 is a file-level requirement readers are conditionally
   exempted from. I recorded this as a decision point: a remote verifier that
   inherits the residency escape would certify a file with a corrupt signature.
   I did not raise it as a finding because §2.3's clause decides it, and
   Appendix H's "every reader obligation, plus the checks readers are exempt
   from" says the same thing a second time.
3. **Trailer.** [F − 64, F), validated in §6.2's stated order: magic (F10/F2) →
   trailer CRC (F16) → version gate (F20/F21) → then the field gates together
   (F11–F19, F22). The ordering matters to the verifier's *report*, not its
   verdict: §24 `[R-VEC-02]` acknowledges "§6.2's field gates are validated
   together, so a file failing two of them attributes to neither alone."
4. **Directory.** [dir_offset, dir_offset + dir_length); CRC over
   dir_length − 4 bytes before any other use (F23, `[R-CNT-11]`).
5. **Record walk.** §7.2 framing (F27, F32), MU gate for unknown top-level
   types (F38), multiplicity (F37), extent slots for non-layer top-level
   records (F33–F35), user-metadata framing (F24, F25, F26), layer-name
   namespace (F6, L4, L6, L7).
   Verifier-only additions at this tier: F28 (MU = 1 with PE = 0), F29
   (reserved flag bits 2–15), F31 (registered type's stored flags against
   §7.3), F39 (any reserved-range type value, whatever its MU bit).

Note that §19.1's step-4 list deliberately excludes the *layer* record's extent
slot; that is layer-tier (L16–L18), and the register's Detected column agrees.
The layer-record **name**, by contrast, is open-tier (L4/L6/L7 all read
`open`), because step 4 builds the namespace. That is internally consistent and
I verified it row by row.

### Phase C — per layer (§19.3 `[R-RDR-03]`)

Full layer-record validation before anything else touches the layer:
slot validity, the §7.4 constraint set (`[R-CNT-23]`, `[R-CNT-16]`), exact
parse and sub-record walk (`[R-CNT-18]`), name rules, fixed widths and u64
domain, the six value sets (§11.4, §12.2, §14.1, §15.1, §17.2, §17.3), bool fill
(`[R-TYP-07]`), the lz4 declaration cap (`[R-COD-07]`), the geometry floor and
its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`), and the index cross-checks
computable without I/O (`[R-CNT-17]`). "All are decidable from the resident
directory and F: layer access performs no fetch."

Verifier-only at this tier: L47, L48, L50 (flag bits), L26 (reserved-range
sub-record type).

A verifier necessarily performs layer access on **every** layer, because §9.7
requires the walk to reach "the non-sentinel entries of each layer's tile-index
region." There is no verifier analogue of a reader's lazy layer access.

### Phase D — per layer, index chain (§15.4, §19.4 steps 3–4)

Fetch the segment-CRC array and each segment; verify `crc_of_crc_array` (L38)
then each segment CRC (L39). Then classify every entry against §15.3's eleven
rows (T6–T12 structural/reader, plus the three *verifier* rows).

I want to record the shape of §15.3 explicitly because it drives three later
computations. Six rows are marked *structural*; I counted them in the table and
got exactly six, matching the prose:

| # | condition | register row |
|---|---|---|
| 1 | offset = S ∧ length = S ∧ crc ≠ 0 | T6 |
| 2 | exactly one of offset, length = S | T7 |
| 3 | length = 0, non-sentinel | T10 |
| 4 | offset < 16, non-sentinel | T8 |
| 5 | offset or length > 2⁶³ − 1, non-sentinel | T11 |
| 6 | offset + length overflows or > F − 64 | T9, T12 |

A *structural* entry contributes no extent anywhere: not to the overlap rows,
not to slab run continuity, not to the coverage walk. An entry whose only defect
is that its stored bytes fail its crc is **not** structural: "its extent stands
and it keeps its place in the *verifier* rows, in run continuity, and in the
coverage walk." That asymmetry is stated three times (§15.3, §16.2, §9.7) and I
found no place where the three statements diverge.

### Phase E — per stored tile (§19.4 steps 5–8, plus verifier content rows)

Fetch, verify the entry crc (T1), decode under the codec (T14–T25), invert the
filter, check the decoded length against the declaration-derived decoded size
(T3), then the verifier-only content rows T2 (interleaved bool byte at a real
position), T4 (padding position content), T5 (packed-plane pad bits), T26
(mis-strided shuffle, detected *through* T2/T4).

### Phase F — coverage walk (§9.7 `[R-LIF-08]`) and the pre-trailer gap

Described in full in §2 below. Note that F9 (`[R-CNT-05]`) is **not** part of
the walk — see §3.

### Phase G — extent-carried documents (§19.2's fourth tier)

Each user-metadata extent: terminal CRC (R2), decode (R3, R4), content rules
(R5–R10), and the verifier-only sortedness check (F30, L49).

### What the verifier reports when a check cannot be run

Three distinct report channels, and the document keeps them apart cleanly:

| situation | channel | effect on verdict |
|---|---|---|
| capability/resource ground (no zstd, decode declined, unimplemented major, MU = 1 unknown type, metadata bound exceeded) | *unable to check*, naming requirement + ground | *conforming* → *cannot establish*; never overrides an established violation |
| verifier elected to stop at the first violation | *unexamined*, per scope | none — verdict is already *nonconforming* |
| SHOULD deviation | advisory | none |
| walk did not enumerate everything | slack total marked **partial**, plus the unwalked regions named with their byte extent (`[R-CNT-21]`) | none |

`[R-MTA-09]` additionally asks for a SHOULD-level detail on the metadata
decline: "the verifier SHOULD report the bound it applied and the stored length
of the extent it declined."

---

## 2. The coverage walk, on a file I built

I refused to do this in the abstract. Here is the file.

### 2.1 The layer

One layer, name `L`, interleaved, linearization 1, codec 1 (none), filter 1
(none), A = 0, S = 0, A_slab = 0, rank 2, C = 1.

- dimensions `y` (E = 3, T = 2) and `x` (E = 3, T = 2)
- channel `v`, type 6 (uint8), fill `0x00`

Grid arithmetic (§11.2): G = (⌈3/2⌉, ⌈3/2⌉) = (2, 2); N = 4; P = 4.
Interleaved ⇒ addressed-tile count = N = 4, Q = ΣBᵢ = 1, decoded size = P·Q = 4
bytes per tile. Under codec 1 that forces every non-sentinel entry's length to
be exactly 4 (`[R-COD-04]`, T14).

Padding positions, computed rather than assumed — a position is padding iff
tᵢ·Tᵢ + uᵢ ≥ Eᵢ for some i:

```
ordinal 0  tile (0,0)  padding at in-tile ordinals []
ordinal 1  tile (0,1)  padding at in-tile ordinals [1, 3]
ordinal 2  tile (1,0)  padding at in-tile ordinals [2, 3]
ordinal 3  tile (1,1)  padding at in-tile ordinals [1, 2, 3]
```

Every padding byte therefore has to be `0x00` (§14.5 `[R-SER-05]`). The four
tile images and their CRC-32Cs:

```
ordinal 0   0A 0B 0C 0D   crc 0xBF8D1BA1
ordinal 1   14 00 15 00   crc 0xB8CCC323
ordinal 2   1E 1F 00 00   crc 0xAF01AC48
ordinal 3   32 00 00 00   crc 0xC941CDF0
```

Layer-record inline payload length, field by field (§7.4's table order, "packed
in table order with no alignment or padding between them"):

```
name           1 + 1  =  2
layout                =  1
linearization         =  2
codec                 =  2
filter                =  2
A                     =  8
S                     =  8
A_slab                =  8
rank d                =  1
channel count C       =  2
2 dim entries  2×(1+1+8+8) = 36
1 chan entry   1+1 + 2 + 1+1 =  6
index_encoding        =  1
entry_count           =  8
crc_of_crc_array      =  4
                       ----
inline_length          = 91
```

Record = 24 + 91 = 115 bytes. Directory = 115 + 4 = 119 bytes. The program
agreed with the hand count.

### 2.2 Generation 1 — creator

```
[0,16)      front signature block
[16,20)     tile ordinal 0
[20,24)     tile ordinal 1
[24,28)     tile ordinal 2
[28,112)    tile-index region   (4×20 = 80 entries + ⌈4/2¹⁶⌉×4 = 4 CRC array = 84)
[112,231)   directory           (dir_offset 112, dir_length 119)
[231,256)   pre-trailer pad     (25 bytes)
[256,320)   trailer             generation 1, file_id 0x0123456789ABCDEF
```

`extent_length` cross-check (`[R-CNT-17]`): 4 × 20 + ⌈4/65536⌉ × 4 = 84 ✓.
F = 320, a multiple of 64 ✓. dir_offset + dir_length = 231 ≤ F − 64 = 256 ✓.
Entry 3 is the sentinel `FF ×16 00 ×4`. Segment CRC array = `9E AC CF DF`
(one partial segment over the 80 entry bytes); crc_of_crc_array = 0x6323BF56;
directory CRC = 0x0A314D1F; trailer CRC = 0x3EE1AA52.

**The walk.** From the live trailer: the directory region; the one layer
record's extent (= the tile-index region, entering the walk once, §9.7 says so
explicitly and I did not double-count it); the three non-sentinel entries'
extents. Plus front block and live trailer, "claimed by the walk as well".

```
claimants: front 16 + t0 4 + t1 4 + t2 4 + index 84 + dir 119 + trailer 64 = 295
disjoint:  yes
in bounds: every non-front, non-trailer claimant inside [16, 256) ✓
slack:     320 − 295 = 25, exactly the run [231,256)
```

### 2.3 Generation 2 — append (supersede a tile, store the sentinel one)

Supersede ordinal 2 (sample (2,0) 0x1E → 0x28) and store ordinal 3. The
stored-tile set changes, so `[R-WRT-04]` re-emits the whole index region at a
new placement.

```
[320,324)   tile 2'   28 1F 00 00
[324,328)   tile 3    32 00 00 00
[328,412)   index region (84)
[412,531)   directory (119)
[531,576)   pad (45)
[576,640)   trailer, generation 2, same file_id
```

Walk: 16 + 4 + 4 + 4 + 4 + 84 + 119 + 64 = 299 claimed; slack = 640 − 299 = 341.
Slack runs, printed by the program: `[(24, 320, 296), (531, 576, 45)]`, summing
to 341. Decomposed by hand: old tile 2 (4) + old index (84) + old dir (119) +
old pad (25) + old trailer (64) = 296, plus the new pad (45).

I got this wrong once by hand — I added the *old pad* twice, because the old
pad was already slack at generation 1 and is not "newly slack". Worth recording
because it is the obvious implementation bug in an incremental slack tracker:
the only sound formulation is §9.7's, `slack = F − |union of claimants|`,
recomputed from scratch each generation.

### 2.4 Generation 3 — a directory-only update

Rename the layer `L` → `M`. Same length, so `inline_length` is unchanged, the
extent slot still points at the generation-2 index region, and nothing but the
directory is re-emitted (§20.3 shape (c)).

```
[640,759)   directory (119)
[759,768)   pad (9)
[768,832)   trailer, generation 3
```

Walk: 299 claimed again; slack = 832 − 299 = 533. Runs:
`[(24, 320, 296), (412, 640, 228), (759, 768, 9)]`.

I initially chose "change the channel's fill value" for this generation,
because §20.3's example names it as a directory-only change. That is where
finding **verifier-02** came from — see §7.

### 2.5 Generation 4 — compaction

New file, fresh file_id 0x00DEADBEEFC0FFEE, generation 1. Only live structures
survive.

```
[0,16)      front
[16,20)     tile 0    0A 0B 0C 0D
[20,24)     tile 1    14 00 15 00
[24,28)     tile 2'   28 1F 00 00
[28,32)     tile 3    32 00 00 00
[32,116)    index′ (84)   entry offsets renumbered 16/20/24/28
[116,235)   directory (119)
[235,256)   pad (21)
[256,320)   trailer
```

Checks specific to `[R-WRT-07]`: every stored tile's bytes verbatim ✓; each
index entry's crc unchanged (I compared the four crc fields between generation 3
and generation 4 — identical) ✓; sentinel entries unchanged (there are none
left) ✓; segment CRCs recomputed over the entries as re-emitted, and
`crc_of_crc_array` updated from 0x8638B5EE to 0x49673712 ✓; reference arrays
identical ✓.

### 2.6 The trace

| generation | operation | F | claimed | slack | verdict |
|---|---|---|---|---|---|
| 1 | create | 320 | 295 | **25** | conforming |
| 2 | append: supersede + store | 640 | 299 | **341** | conforming |
| 3 | update: directory only | 832 | 299 | **533** | conforming |
| 4 | compact (new file_id, gen 1) | 320 | 299 | **21** | conforming |

Slack goes 25 → 341 → 533 → 21. Generation 3 is the honest illustration of
§20.3's note: a commit that changes nothing but a name added 192 bytes of file
and 192 bytes of slack. Compaction is the only thing that walks it back
(`[R-WRT-06]`, §20.5's figure).

### 2.7 Which bytes are certified, which are counted, and whether any is neither

This is the question the charter puts most sharply, so I want to answer it in
the document's own terms.

**Three classes, not two.**

1. **Checksum-certified.** Trailer (its own [60,64) over [0,60)); directory
   region (final 4 bytes over dir_length − 4); tile-index region (entry bytes
   covered per segment by the segment-CRC array, the array itself covered by
   `crc_of_crc_array`, which sits in the directory and is therefore covered by
   the directory CRC); stored tiles (the entry's crc field); user-metadata
   extents (final 4 bytes over the preceding bytes as stored, before decoding).
   §8.1's map, and §8.2's chain "trailer → directory → crc_of_crc_array →
   segment CRC array → index segment → index entry → stored tile".

2. **Claimed by the walk but not checksum-covered.** Exactly two things, and
   §4.5 names both as exceptions:
   - the front signature block — "a constant whose check is equality";
   - "the extent of a record of a type this specification has not assigned,
     which §8.1's map covers by no checksum at all."
   Also in this class, but differently: the terminal checksum *fields*
   themselves (trailer [60,64), the directory's last 4 bytes, a user-metadata
   extent's last 4 bytes), which are "verified by comparison and covered by no
   further checksum."

   The unknown-type extent is the interesting member. It is a claimant — §5.2
   defines a structure as including "a record extent (the bytes any record's
   extent slot references, **whatever the record's type**)" — so its bytes are
   in the partition, are disjointness-checked, and are bounds-checked; but their
   content is unconstrained and unchecksummed. §22.3 `[R-SEC-04]` says so out
   loud: "corruption inside it is equally invisible". A verifier certifies its
   *placement* and nothing about its content.

3. **Slack.** Everything the walk does not reach. Content unconstrained, no
   conformance requirement, counted and reported.

**Can a byte be in none of the three?** No, and the document proves it rather
than asserting it. §5.2's note: "The live committed state is *defined* as the
front block plus what a complete coverage walk reaches, and `[R-LIF-08]` makes
every byte that walk misses slack — so 'belongs to no class' describes nothing,
and a register row for it would be a row no file could exhibit." Combined with
`[R-CNT-01]`/F19 (physical size = F), the partition is total over [0, F). I
consider this settled, and I checked it against my four files: claimed + slack
= F in every generation.

**Can a byte be in two?** That is the only testable half, and it is F36/L19.
Which brings me to the adversarial layouts.

---

## 3. Extent overlap, alignment, and slab, on adversarial layouts

### 3.1 Overlap

I ran four variants of the generation-1 layout through the walk. Scope
attribution follows `[R-CNT-13]`: intra-layer → reject-layer (L19); "any
overlap across layers or touching another scope's structures" → reject-file
(F36).

**A1 — entry 1's offset moved 16 → 18.** tile0 [16,20) × tile1 [18,22) overlap
at [18,20). Both belong to layer A → **L19, reject-layer**. Sum of lengths 295,
union 293.

**A2 — entry 1 moved to offset 110, length 4.** [110,114) straddles two things:

```
index(layer A) x tile1 at [110,112) -> L19 reject-layer
tile1          x dir   at [112,114) -> F36 reject-file
```

One malformed entry, two register rows, two different scopes. The verifier
records both; the verdict is *nonconforming* either way. This is the case
`[R-CNT-13]` calls out by name — "including a stored extent overlapping its own
layer's index region."

**A3 — a second layer B whose tile [100,120) and index [118,142) collide with
layer A's index and the directory.** Four overlaps, three of them file-scope:

```
index(A) x tileB0        at [100,112) -> F36
tileB0   x dir           at [112,120) -> F36
tileB0   x index(B)      at [118,120) -> L19 (both layer B)
dir      x index(B)      at [118,142) -> F36
```

This one produced the useful arithmetic accident: sum-of-lengths = 339 against
F = 320, so a slack computed as `F − Σ lengths` came out **−19**. §9.7's
definition — "Bytes the walk does not reach are slack" — is a set-complement
definition and stays well defined under overlap; it gave 25. An implementer who
reads §5.2's partition as licence to sum lengths gets a negative number on
exactly the files where the partition has failed. The text is right; I record
the trap.

**A4 — a stored tile at [240,244), inside the pre-trailer gap [231,256).** It
is disjoint from every claimant and lies inside [16, F − 64). The §9.7 walk
therefore reports **clean**. Only `[R-CNT-05]` catches it: "A verifier MUST
treat a structure in that gap as a validity error at file scope" (F9). This is
a check *outside* the walk, and it is one of the three Appendix H omits — see
finding verifier-05.

### 3.2 Alignment (`[R-SLB-01]`, L41)

Declare A = 512 on the generation-1 layer. Stored tiles sit at 16, 20, 24:

```
ordinal 0 offset 16  16 mod 512 = 16  -> L41
ordinal 1 offset 20  20 mod 512 = 20  -> L41
ordinal 2 offset 24  24 mod 512 = 24  -> L41
```

Three instances of one row, reject-layer. The index region at offset 28 is
**not** checked: `[R-SLB-01]` says "every stored tile's offset satisfies
offset mod A = 0", and an index region is not a stored tile. I looked for a rule
aligning index regions and found none — correctly, I think, since alignment is
declared for I/O on tile payloads.

`[R-CNT-16]` (A ≠ 0 and S ≠ 0 both declared → L21) is a layer-access reader
check, not a verifier one; I kept them separate in the implementation.

### 3.3 Slab (`[R-SLB-02]`, `[R-SLB-03]`, L42/L43)

Interleaved, N = 4, S = 2 ⇒ one block [0,4), runs [0,2) and [2,4).

*Conforming case*, A_slab = 4, offsets 16/20/24 with ordinal 3 sentinel:

```
run [0,2): stored [0,1]; first offset 16 mod 4 = 0 OK; pack 0->1 expect 20 got 20 OK
run [2,4): stored [2];   first offset 24 mod 4 = 0 OK
```

*A_slab = 16*: run 1's first stored tile is at 24, 24 mod 16 = 8 → **L43**.

*tile 1 relocated to 100*: run 0's packing chain breaks, expect 20 got 100 →
**L42**.

*Planar C = 2, N = 4, S = 3*, offsets 16/20/24/28 and 40/44/48/52: blocks
[0,4) and [4,8), runs [0,3), [3,4), [4,7), [7,8). All four runs pass — and the
12-byte hole between ordinal 3 (at 28) and ordinal 4 (at 40) is *not* a
violation, because "Runs partition each contiguous block of disk ordinals
independently … runs never span channel blocks" and "The runs themselves are
not mutually ordered or joined". This is the case I most expected to be
underspecified and it is not: `[R-SLB-02]` fixes block boundaries, run starts,
and the short final run in one sentence each.

Transparency rules I implemented and cross-checked against §15.3 and §9.7:
sentinels are transparent; entries §15.3 calls *structural* are transparent; an
entry failing only its stored bytes' crc is **not** transparent. All three
statements appear in §16.2 and §15.3 and agree.

`[R-SLB-04]` (a stale slab declaration carried across a commit) has no register
row of its own, by design: "every file exhibiting one exhibits a run whose tiles
are unpacked or whose first stored tile is misaligned, which §21.3 registers."
My generation-2 append changed the stored-tile set; if the layer had declared a
slab I would have had to re-establish the invariants or clear S. I confirmed
this is decidable from the new generation's index bytes alone — which is the
point of the "not transparent" carve-out.

---

## 4. Checksum obligations, and every constant I could reproduce

### 4.1 Is every live structure covered?

Walking §8.1's map against §5.2's structure classes:

| live-state member | checksum | covered? |
|---|---|---|
| front signature block | none | equality-checked instead (§6.1) |
| trailer | own [60,64) over [0,60) | yes, by comparison; the field itself uncovered |
| directory region | final 4 bytes | yes; the field itself uncovered |
| tile-index region: entry bytes | segment CRC array | yes |
| tile-index region: segment CRC array | layer record's `crc_of_crc_array` | yes |
| `crc_of_crc_array` (in the directory) | directory CRC | yes |
| stored tile | entry's crc field | yes |
| user-metadata extent | final 4 bytes | yes; the field itself uncovered |
| extent of an unassigned-type record | **none** | no — content opaque |

So the map is complete: every byte of the live state is either
checksum-covered, equality-checked, a terminal comparison field, or inside an
unassigned-type extent. The last is the only content-unconstrained claimed
region, and §4.5 and §8.1 both name it.

One consequence worth stating because it is easy to get wrong: an
**ignore-record**'d user-metadata record's extent is still a claimant *and*
still checksum-covered. §2.4 says ignore-record means "the record is skipped as
though absent", but §5.2's claimant rule is "whatever the record's type" and
§8.1's row is per-structure, not per-encoding. So a file whose ignored
user-metadata extent fails its terminal CRC is **nonconforming** (R2) even
though every reader behaves identically on it. I implemented it that way.

### 4.2 Constants reproduced

I wrote a CRC-32C from the parameters in §4.5 (Castagnoli 0x1EDC6F41,
reflected in/out — table built from the reflected polynomial 0x82F63B78 —
init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and used it for everything below.

| constant | stated | computed | ✓ |
|---|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283, stored `83 92 06 E3` | 0xE3069283, `83 92 06 E3` | ✓ |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 | ✓ |
| CRC-32C of a full all-sentinel segment (2¹⁶ × `FF ×16 00 ×4`) | 0xEECB3BB2 | 0xEECB3BB2 | ✓ |
| Appendix A trailer CRC over [0,60) | 0xE00938D2 | 0xE00938D2 | ✓ |
| Appendix A directory region [16,20) | `00 00 00 00` = CRC of zero bytes | ✓ | ✓ |

The all-sentinel constant is the one that matters operationally, since
`[R-IDX-05]` lets writers of sparse layers emit it without computing it: a wrong
constant there would put wrong bytes on disk in every sparse file. It is right.

I additionally decoded the whole Appendix A dump and re-derived every field:
version_major 1, version_minor 0, flags 0, generation 1, dir_offset 16,
dir_length 4, committed_file_length 128 (= the dump's length), file_id
0x0123456789ABCDEF, reserved zero. Coverage: 16 + 4 + 64 = 84 claimed, slack 44,
matching the annotation's "pre-trailer pad, 44 bytes".

**Constants I could not reproduce:** none of the CRC values. What I could not
check locally are the *external* format constants — the zstd frame magic
`28 B5 2F FD` (I recognise it but cannot verify RFC 8878 without reading it),
the LZ4 frame magic `04 22 4D 18` in T23, the lz4 block-format cap
`0x7E000000`, and RFC 1951's bit-boundary behaviour that the §17.2 note relies
on. I treated all four as pinned external references (Appendix F) and did not
form an opinion on them.

### 4.3 Other stated arithmetic I re-derived

Everything below reproduced exactly, which is why I have no findings against
the worked examples other than verifier-02:

- §11.2: (1024, 2048) / (256, 256) → G = (4,8), N = 32, P = 65,536; and
  ⌈1000/256⌉ = 4.
- §11.4: (300,700) → tile (1,2), s = 10, in-tile (44,188), ordinal 11,452;
  planar channel 2 → disk ordinal 74.
- §14.2: interleaved uint8+uint16, Q = 3, decoded 18, ordinal 5 at [15,18);
  planar `b` plane 12 bytes, ordinal 5 at [10,12); float32+bool interleaved,
  Q = 5, decoded 30, ordinal 5 at [25,30).
- §14.3: P = 10 alternating → `55 01` with fill false, `55 FD` with fill true.
  I implemented the pad-bit fill separately and it produced exactly those.
- §14.5: extents (5,5) / tiles (4,4), edge tile (1,1) has 1 real and 15 padding
  positions, uint16 fill 0xABCD → 32 bytes with values 1–15 all `CD AB`.
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC
  array, region 20,000,064 bytes, tile 999,999 at segment-relative 339,180,
  segment 15 at [19,660,800, 20,000,000), full segment 1.25 MiB.
- §15.4 second example: disk ordinal 74 → region bytes [1,480, 1,500);
  channel 3's entries are 96–127.
- §16.2: N = 32, S = 8 → runs [0,8), [8,16), [16,24), [24,32); tile rows 1–2 =
  ordinals 8–23 = runs 1 and 2.
- §17.3: shuffle of float32 1.0/2.0/3.0 → `00 00 00 00 00 00 80 00 40 3F 40 40`,
  byte for byte, and the inverse round-trips.
- §20.3: 32-tile interleaved index re-emission = 32·20 + 4 = 644 bytes.
- §21.9 rationale: 2³² entries → 2¹⁶ segments × 4 = 256 KiB CRC array; 2³⁶ →
  4 MiB. 2³² × 20 = 85.9 GB of entries, consistent with §24's "tens of
  gigabytes".
- §21.8: I counted the register mechanically per §21.1's rule (semicolons
  separate instances; a cell reading "—" is one instance) and got **125 rows /
  252 instances**: F 39 rows/61 instances, L 50/102, T 26/45, R 10/44. Exactly
  the stated "125 conditions over 252 instances". §21.2's "39", §21.3's "50",
  §21.4's "26" and §21.5's "10" all check out.

---

## 5. Decoded-content obligations

**What a verifier must decode: every stored tile of every layer.** The document
does not say this in one sentence, so I want to show the derivation.

- §2.3: a verifier is "a reader that additionally checks every file-level
  requirement — including those ordinary readers are exempted from".
- §2.4: "A file is conforming only if it satisfies every requirement at every
  scope", and "a verifier certifies only violation-free files."
- §21.4 contains reader-detected tile rows that are only decidable by decoding:
  T3 (`[R-SER-07]`, decoded length ≠ decoded size), T24 (`[R-COD-08]`, bytes
  remaining after the stream/frame/block), T25 (malformed stream). A reader
  reaches these only "at use of a tile" (§19.2); a verifier has no
  use-triggered laziness available to it because it must certify the whole
  predicate.
- §17.4 `[R-COD-11]` then handles the case where it *can't*: "A verifier that
  cannot execute a layer's codec or filter cannot establish that layer's
  conformance and MUST NOT certify the file."

**What it compares against.**

| obligation | comparand | row |
|---|---|---|
| stored bytes | entry's crc field | T1 |
| codec 1 length | tile's decoded size, from declarations | T14 |
| decoded length | decoded size = P·Q, P·Bᶜ, or ⌈P/8⌉, from declarations alone | T3 |
| decode consumption | the entry's length, exactly | T24 |
| padding positions | the channel's **recorded fill bytes** | T4 |
| pad bits of a packed plane | the channel's **fill bit** | T5 |
| interleaved bool byte at a real position | ∈ {0x00, 0x01} | T2 |

The T2/T4 split is clean and stated: "the same byte at a padding position is
T4's, the two rows together covering `[R-SER-08]`." I implemented the padding
mask from geometry (`tᵢ·Tᵢ + uᵢ ≥ Eᵢ`) and ran T4 over my four tiles with
fill 0x00: clean, as designed.

**What it is permitted to skip.** Content-wise, nothing. The only exits are:

- **cannot execute** the codec or filter → *cannot establish* (`[R-COD-11]`);
- **decline** a layer's or a tile's decode on resource grounds
  (`[R-ERR-04]`) → *cannot establish*, and the refusal "MUST be reported as a
  resource limit and not as a validity error";
- **decline** a user-metadata document above its own bound
  (`[R-MTA-09]`) → *cannot establish*;
- **stop at the first violation** (`[R-CNF-11]`) → verdict already
  *nonconforming*, remaining scopes reported *unexamined*.

Note that every exit forfeits certification. There is no path on which a
verifier skips a decode and still says *conforming*. That is the cleanest
answer in the whole charter and the document earns it.

**Codec-header checks that need no full decode**, which I separated out because
they gate cheaply: T17 (zstd magic), T19 (dictionary ID), T20 (content-checksum
flag), T21 (window size vs decoded size), T22 (frame content size), T23 (lz4
frame magic), T15 (deflate wrapper), T14 (codec-1 length), L45 (lz4 declaration
cap). §17.2's note on Window_Size composition is correct as far as I can check
it without RFC 8878: with Single_Segment_Flag set there is no Window_Descriptor
and Window_Size is the frame content size, which the same rule already pins to
the decoded size; without it the descriptor floor is 1 KiB, so a tile with
decoded size below 1 KiB is encodable under codec 3 only as a single-segment
frame. My §14 worked examples give decoded sizes 18, 30 and 2 — exactly the
three the note cites — so the note's example set is consistent with §14's.

**Metadata.** The verifier decodes every user-metadata document it can, checks
R5–R10's content rules and the verifier-only sortedness rows F30/L49, and does
**not** check §18.4's standardized keys: `[R-MTA-07]` says "Neither placement
nor value shape bears on validity … enforcing them would put a verifier to work
on the content of metadata, which §21.7 excludes by design." I noted in passing
that §21.7 is actually about *sample* content and the verifier does check
metadata content elsewhere (sortedness, key length, duplicate keys), so the
cross-reference is loose; but the operative sentence ("Neither placement nor
value shape bears on validity") decides it, and §21.6 repeats it. Not a finding.

An edge I had to resolve: a user-metadata record declaring an
**experimental-range encoding (≥ 0x80)**. §21.6 says the file is conforming and
the record is ignored. Can the verifier certify, given that it cannot decode the
document and so cannot check `[R-MTA-05]`? Yes — §2.4 defines ignore-record as
"the record is skipped as though absent", and an absent record has no document,
so there is no `[R-MTA-04]`/`[R-MTA-05]` obligation left unchecked. `[R-MTA-09]`'s
*cannot establish* is scoped to a **decline** on the size bound, not to an
unassigned encoding. Its extent's terminal CRC still has to verify (§8.1),
because that is a structural check that precedes the document.

---

## 6. Where §9.7's walk stops, and what that does to the report

`[R-CNT-21]` requires a **partial** total "whether because a scope-level
rejection stops it, or because the verifier elected under `[R-CNF-11]` to stop
at the first violation", plus naming the unwalked regions and their byte extent.

I checked whether this can bite a *conforming* file. It cannot: both triggers
presuppose an established violation, so the file is already nonconforming.
Neither *cannot establish* ground stops the walk — the walk needs no decoding,
and an unimplemented MU = 1 record's extent slot is still readable. So on any
file a verifier certifies, the slack total is exact and unique. I therefore did
**not** file the residual latitude (whether e.g. a reject-layer for a bad bool
fill byte, which physically blocks nothing, "stops" the walk) as a finding: two
verifiers may legitimately differ on the mandatory partial/complete marking for
an already-nonconforming file, and the document nowhere requires the walk to
continue past a rejection. That is licensed variance, not underdetermination.

What I *did* file is the arithmetic in §15.3's parenthetical about structural
entries — see verifier-03. That one is not latitude; it is a formula that
produces impossible numbers.

---

## 7. Findings

### verifier-01 — AMBIGUITY. A pre-trailer gap of 64 bytes or more: conforming file, nonconforming commit

§6.2 `[R-CNT-05]`, §9.2 `[R-LIF-02]` step 5, §2.3 `[R-CNF-02]`.

`[R-CNT-05]`:

> "this specification does not constrain their content, and bounds their number
> only through step 5 of the commit protocol, which pads to the next 64-byte
> boundary (`[R-LIF-02]`) — a longer gap is conforming, and no conforming commit
> produces one."

`[R-LIF-02]`:

> "A writer performing a commit MUST, in order: … (5) append the pad to the next
> 64-byte boundary — zeroed by advice, `[R-CNT-03]` — and the new trailer, with
> generation one greater than the prior trailer's and committed_file_length
> equal to the new end"

The gap is byte-visible: `F − 64 − (dir_offset + dir_length)`. A commit
following step 5 leaves 0–63 bytes; anything ≥ 64 proves step 5 was not
followed. Two readings for the verifier handed such a file:

(a) **Certify.** `[R-CNT-05]` expressly declares a longer gap conforming, and
`[R-CNF-02]`'s general clause — "A writer obligation whose violation this
specification expressly declares not to be a file-conformance violation …
binds the actor in the same way" — turns step 5 into a conduct rule for this
case. §21's completeness is normative and there is no register row for an
over-long gap, which under §21.1 means there is no detectable violation.
§6.4's SHOULD ("dir_length plus the pre-trailer pad plus 64 within 65,536
bytes") also treats the pad as a term that can grow.

(b) **Refuse.** §2.4: "A file is conforming only if it satisfies every
requirement at every scope"; `[R-LIF-02]` is a MUST whose violation is visible
in the bytes; and `[R-CNF-02]`'s enumeration of conduct rules names §10.3,
§18.3 and §6.3 but not §9.2.

I picked (a). The cost of getting it wrong is that a verifier rejects
conforming files produced by a sloppy-but-legal writer, or accepts files it
should flag. What an implementer does wrong without this: treats every MUST in
§9.2 as a file predicate, because nothing local to §9.2 says otherwise — the
carve-out lives two sections earlier and is phrased as an aside inside a
sentence about pad *content*.

### verifier-02 — CONTRADICTION. §20.3's "changing a channel's fill value" is not a directory-only commit whenever the layer has stored edge tiles

§20.3 (Example, shape (c)) against §14.5 `[R-SER-05]`.

§20.3:

> "**(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, changing a channel's fill value. Only the directory is
> re-emitted."

§14.5 `[R-SER-05]`:

> "Padding positions (§11.3) are serialized like any other position, and their
> content is fixed: at every padding position, a writer MUST encode, for each
> channel the position carries, that channel's fill value — the recorded fill
> bytes for a numeric channel, the recorded fill byte for an interleaved bool
> channel, the fill bit in a packed plane. Every pad bit (§14.3) MUST carry the
> plane's channel's fill bit. A conforming reader never returns this content
> (`[R-GEO-04]`) and is not obligated to check it; a verifier MUST check it, and
> a violation is a validity error at tile scope."

Concretely, on my generation-3 file. The layer's fill is 0x00 and its stored
tiles carry padding at these in-tile ordinals: tile 1 at {1,3}, tile 2 at {2,3},
tile 3 at {1,2,3}. Re-emitting the directory alone with fill changed to 0x07
leaves seven padding bytes holding 0x00 against a recorded fill of 0x07:

```
T4 with fill=0x00: clean
T4 with fill=0x07: [(1,1,0x0), (1,3,0x0), (2,2,0x0), (2,3,0x0),
                    (3,1,0x0), (3,2,0x0), (3,3,0x0)]
```

Seven T4 instances across three tiles; the file is nonconforming and a verifier
must report reject-tile on each. The same holds for a bool channel's fill flip,
which invalidates every packed plane's pad bits as well (T5). The example is
sound only when the layer has no padding positions (Gᵢ·Tᵢ = Eᵢ for every i) or
no stored edge tile — neither of which it states.

The two other operations the same sentence lists are genuinely safe: clearing a
slab declaration is expressly permitted by `[R-SLB-04]`, and renaming a layer
touches nothing outside the record (I used exactly that for generation 3, which
is why generation 3 verified clean).

I picked `[R-SER-05]`: §2.1 makes the §20.3 block non-normative ("any text
labeled *Note*, *Example*, or *Rationale*"), and `[R-CNF-05]` obliges the
updater to emit a conforming file. What an implementer does wrong without this:
builds an updater whose `set_fill()` re-emits only the directory, silently
producing files that every conforming verifier rejects at tile scope — and
producing them on exactly the layers where fill matters most, the ones with
ragged edges.

### verifier-03 — CONTRADICTION. §15.3's slack gloss and §9.7's slack definition give different, sometimes impossible, totals

§15.3 `[R-IDX-03]` against §9.7 `[R-LIF-08]`.

§15.3:

> "Such an entry contributes no stored extent to the *verifier* rows, which bind
> over well-formed entries' extents only — `[R-SLB-03]`'s run continuity closes
> over it as it does over a sentinel — and none to `[R-LIF-08]`'s coverage walk,
> whose slack total therefore includes whatever bytes such an entry nominally
> addresses."

§9.7:

> "Bytes the walk does not reach are slack: the verifier sums them and reports
> the total, and their content is not its concern."

(§9.7 says the same thing a second time: "the walk passes over it, and the bytes
it nominally addresses fall to slack (§15.3)".)

The two agree only when the entry's nominal extent lies inside [16, F − 64) and
is unclaimed. Four of the six *structural* rows guarantee it does not. On my
generation-1 file (F = 320, claimants 291 once entry 1 is spoiled):

| spoiled entry 1 | row | slack per §9.7 | slack per §15.3's gloss |
|---|---|---|---|
| offset 8, length 4 | T8 (offset < 16) | 29 | 33 |
| offset 316, length 8 | T9 (past F − 64) | 29 | 37 |
| offset 20, length 0 | T10 | 29 | 29 |

For T8 the nominal bytes [8,12) sit **inside the front signature block**, which
§9.7 expressly claims for the walk — they cannot also be slack. For T9 the
nominal bytes [316,324) run four bytes **past the physical end of the file** —
they are not bytes at all. Both gloss totals exceed `F − claimed`, which is the
maximum possible slack. The same failure arises for T11 (offset or length above
2⁶³ − 1) and T12 (an overflowing sum), where the "nominal" extent is not even
representable.

Permitted readings: (i) the gloss is operative and the total is
`|complement of walk| + Σ nominal extents of structural entries`; (ii) §9.7's
set-complement definition is operative and the gloss is a loose paraphrase, true
only in the T10-shaped case. I picked (ii): reading (i) yields totals above
`F − claimed` and, for T9/T11/T12, totals over byte ranges that do not exist,
which no report can mean. The verifier must compute
`slack = F − |union of claimant ranges|`.

What an implementer does wrong without this: adds `entry.length` to a running
slack counter whenever it classifies an entry structural, and emits slack totals
that are wrong by construction — including, on the T9 layout above, a total
larger than the file.

### verifier-04 — OBSERVATION. The scope of "each requirement it was unable to check" is decidable, but only by a reductio

§2.3 `[R-CNF-11]` against §21.7 `[R-ERR-01]`.

§2.3:

> "A verifier MUST report each requirement it was unable to check, naming the
> requirement and the ground, whichever of the three verdicts it reports"

and, earlier in the same bullet:

> "A verifier reports one of three verdicts: *conforming*, *nonconforming*, or
> *cannot establish* — the last where some requirement is one it is unable to
> check"

§21.7:

> "A second set of obligations is omitted from the register because a single
> file exhibits no witness of their violation. Committed-prefix immutability and
> the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a
> file's history, which §9.7 does not reconstruct; the ordinal mappings of
> `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile
> whatever values it carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record
> encoding file offsets in its own payload is opaque by construction."

Read broadly, "each requirement it was unable to check" reaches §21.7's set,
plus `[R-CNT-26]`'s version_minor floor (uncheckable on any file carrying an
unknown ignore-lane bit, since the minor that defined that bit is unknown) and
`[R-WRT-04]`/`[R-WRT-05]`'s history obligations. Since those are unable-to-check
on *every* file, and §2.3 makes *cannot establish* available "where some
requirement is one it is unable to check", the broad reading makes every verdict
*cannot establish* and, with "a verifier MUST NOT certify a file it reports that
way", makes certification unreachable — the conforming-verifier class would be
empty.

The narrow reading is right, but nothing local says so. It has to be assembled
from: `[R-CNF-02]` ("File conformance is a pure predicate on bytes … conduct
rules bind the actor, the predicate binds the bytes"); §2.3's own framing of the
verifier as checking every **file-level** requirement; §21.7's own account that
these obligations have no witness in a file, so there is nothing to check rather
than something unchecked; and the reductio above. I picked: *unable to check*
covers only requirements the verifier could have checked on this file but did
not, for a capability or resource ground — the five §2.3 enumerates and their
kin. Requirements with no single-file witness are simply outside the predicate.

What an implementer does wrong without this: ships a verifier that never
certifies anything, or one that appends a boilerplate five-item "unchecked" list
to every report and thereby buries the real declines (the unimplemented codec,
the metadata bound) that are supposed to be actionable.

### verifier-05 — OBSERVATION. Appendix H's verifier checklist omits three of the twenty verifier-detected rows and understates the decode obligation

Appendix H, against §21.2–§21.4's *Detector* column.

Appendix H:

> "**Conforming verifier** — every reader obligation, plus the checks readers
> are exempt from: the live-state coverage partition and the slack total (§9.7)
> — reported as partial, with the unwalked regions named and their byte extent
> given, where its walk did not complete (`[R-CNT-21]`); extent overlap (§7.2);
> record flag bits — reserved bits, MU = 1 with PE = 0, and a registered type's
> stored bits against §7.3's registry (`[R-CNT-12]`, `[R-CNT-22]`); alignment
> and slab invariants (§16); decoded-content obligations — padding samples and
> interleaved boolean bytes (§14.5, §14.2); user-metadata member ordering
> (`[R-MTA-05]`, §18.2); …"

I enumerated the rows whose Detector cell reads *verifier* by grepping the
register: F9, F28, F29, F30, F31, F36, F39, L19, L26, L41, L42, L43, L47, L48,
L49, L50, T2, T4, T5, T26 — twenty rows. The checklist covers seventeen of them.
Missing:

1. **F9** — "A structure occupies bytes between the live directory's end and the
   live trailer", governed by `[R-CNT-05]`. This is *not* part of the coverage
   partition: my adversarial layout A4 places a stored tile at [240,244) inside
   the pre-trailer gap [231,256), where it is disjoint from every claimant and
   inside [16, F − 64), so §9.7's walk reports clean. A verifier built from the
   checklist's "live-state coverage partition and the slack total" alone runs no
   check that catches it.
2. **F39 and L26** — a record type from the reserved range 0x0003–0x7FFF, whose
   emission `[R-CNT-15]` makes a violation whatever its MU bit. The checklist's
   "record flag bits" line covers the flag rows but not the type-value rows, and
   the MU = 1 specialisations (F38, L25) are reader rows, so a
   checklist-derived verifier accepts a reserved-range MU = 0 record silently.
3. The decode obligation is described as "padding samples and interleaved
   boolean bytes", i.e. `[R-SER-05]` and `[R-SER-08]`. A verifier reading only
   that would skip decoding a tile in a layer with no padding positions and no
   bool channel — and thereby skip T3 (`[R-SER-07]`), T24 and T25
   (`[R-COD-08]`), which are reader-assigned but are still file-level
   requirements the verifier must check under §2.3.

Appendix H is non-normative and says so ("each entry's authority is the
requirement or section cited, never this summary"), and §21's register governs,
so this is not a defect in the normative text. I report it because Appendix H is
the only place in the document that collects the verifier's obligations, it is
what an implementer will build from, and the three gaps are all in the
verifier-only lane where there is no reader behaviour to fall back on.

---

## 8. Things I checked and did not report

For the record, so the absence is legible:

- **Two file-scope record extents overlapping each other.** `[R-CNT-13]`'s
  outcome clause ("intra-layer … reject-layer, and any overlap across layers or
  touching another scope's structures … reject-file") does not literally name
  file-vs-file. F36's leading clause does — "two structures that do not belong
  to the same layer" — and `[R-CNF-08]`'s owning-scope mapping gives reject-file
  independently. Decided.
- **Whether a verifier must fetch [0,16).** `[R-CNT-04]` and F8 grant a
  residency escape to readers; §2.3's "including those ordinary readers are
  exempted from" withdraws it for verifiers, and Appendix H's "plus the checks
  readers are exempt from" says it again. Decided.
- **Whether a reject-layer "stops" the walk.** Licensed variance, and it can
  only arise on files that are already nonconforming. Not underdetermined.
- **Whether the recovery probe of §9.6 bears on a verdict.** "no verdict turns
  on the probe … For a verifier the probe is diagnosis". Decided, explicitly.
- **`[R-CNT-26]`'s version_minor floor.** A SHOULD; advisory only under
  `[R-CNF-12]`. Not a certification gate.
- **Experimental-range metadata encoding.** §21.6 says the file is conforming;
  §2.4's "skipped as though absent" removes the document and with it
  `[R-MTA-04]`/`[R-MTA-05]`. The extent's terminal CRC still applies. Decided.
- **Bytes an unknown MU = 1 record might reference outside its extent slot.**
  §5.2 defines the live state as what is reachable "through the live directory's
  records, extent slots, and tile-index entries", so such bytes are slack by
  definition; and the file's verdict is *cannot establish* anyway (§2.3, §21.6).
  Decided.
- **Sum-of-lengths vs union for the slack total.** §9.7's "bytes the walk does
  not reach" is a complement, well defined under overlap. The −19 my A3 layout
  produced is an implementation trap, not a specification gap.

## 9. Confidence

I could implement the certification procedure, the coverage walk, the overlap /
alignment / slab checks, the checksum inventory, and the decode obligations from
this document alone, and I did — the arithmetic above is all mine and all of it
closes. Every constant the document states and I could compute locally
reproduced. The document's own worked examples reproduced without exception. My
five findings are all report-level or example-level; none of them forks the
bytes.
