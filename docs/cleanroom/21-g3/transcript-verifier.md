# Round 21 — Verifier implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in four
sequential chunks covering all 4,377 lines, plus targeted `grep` passes over the same file.
I opened no other file. I did not run `git log`, `git diff`, or any directory listing of the
repository. I did not read `docs/`, `conformance/`, `spec/registry.json`, `PLAN.md`,
`AGENTS.md`, or the round-21 output directory.

I ran local Python that reads no repository file except `spec/tarn.md` itself (two scripts
parse the register tables out of it to count rows and instances). Everything else — CRC
tables, file construction, the verifier — is code I wrote in the scratchpad from the
document's text alone. Scratch files I created and re-read:
`crc.py`, `appA.py`, `lib.py`, `build.py`, `verify.py`, `adv.py`, `trace.py`, and the
`.tarn` files they emit.

**Context I did not ask for.** My runtime placed a project-instruction file (`CLAUDE.md`,
which forwards to `AGENTS.md`) and an index of the maintainer's memory notes into my context
before I began. I did not open any file they name and I did not act on their contents; I am
naming their appearance here, not repeating them. I also received a listing of pre-existing
task items in a tool reminder. None of it entered my reasoning about the specification.

I used prior knowledge of other container formats only to generate suspicions (e.g. "is the
DEFLATE final-byte padding constrained?"), never to settle one — every settlement below cites
this document.

---

## 1. What I built

A conforming verifier, on paper and in code: the ordered certification procedure, the coverage
walk, the overlap/alignment/slab checks, the checksum chain, the decode obligations, and a
four-generation trace. The code is `verify.py`; the files it certifies or condemns are
constructed byte-by-byte by `build.py`, `adv.py`, and `trace.py`, from the document's layout
tables and nothing else.

I want to record the order I worked in, because it is what exposed the two things I am
reporting. I read §2.3, §5.2 and §9.7 first (the verifier's charter, the coverage rule, the
walk), then §18.2 and §21.5 as instructed, then built the conforming file, then broke it six
ways, then traced four generations. The two findings surfaced at step 2 (the changed §18.2
sentence) and step 5 (breaking the file — the partial-total rule).

---

## 2. The certification procedure, as an ordered algorithm

`[R-CNF-12]` fixes the scope of the whole exercise: "§2.3's duty to check every file-level
requirement runs to the MUST-level conditions §21 inventories". So the verifier's checklist
*is* the register — §21.2 through §21.5 — plus the reporting duties of `[R-CNF-11]`,
`[R-CNT-21]`, and `[R-MTA-10]`. I confirmed the register's own arithmetic mechanically before
trusting it as a checklist:

```
row counts: {'F': 36, 'L': 49, 'T': 26, 'R': 10}  sum 121
instance total: 273
per-section instances: {'F': 58, 'L': 116, 'T': 55, 'R': 44}
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10; §21.8 says "121 conditions over
273 instances". All four subsection counts and both totals reproduce exactly under §21.1's
stated counting rule (a cell reading `—` is one instance; otherwise semicolon-separated).
That is a strong signal the register is maintained rather than asserted, and it let me treat
it as the authoritative checklist.

### 2.1 The ordered algorithm

**Tier 0 — front block.** Verify bytes [0,16) against the 16-byte constant by equality
(`[R-CNT-04]`, §6.1). §6.1's residency exemption does not reach a verifier: F6's row says
"a verifier holds no such exemption (§2.3)", and Appendix H repeats it. §21.2's preamble
puts this check "before other processing", alongside F8 and F14, as one of the four rows that
reach a file declaring a foreign major. Verdict on mismatch: **nonconforming** (F6; F1's
front-block instance for the byte-reversed specialisation).

Note what this does to the slack total. §5.2 owes a total only to "a verifier that reaches a
live state"; a verifier that stops at F6 has not established a trailer, so it owes none. One
that continues past F6 does reach a live state and owes one. Both are conforming verifiers.

**Tier 1 — minimum length.** F < 128 → nonconforming (`[R-CNT-27]`, F5). I checked the
128 floor arithmetically: front 16 + directory ≥ 4 at offset ≥ 16 + a 64-byte trailer at a
64-aligned offset forces F ≥ 84, and F mod 64 = 0 forces F ≥ 128. F = 64 would place the
trailer at 0, over the front block.

**Tier 2 — trailer, in §6.2's fixed order.** Magic (F8) → trailer CRC (F14) → version gate
(F18 at 0; a foreign major is *cannot establish*, not a verdict about the bytes, per §2.3 and
`[R-CNF-02]`) → then, and only then, the remaining gates as a group: flags (F19),
committed_file_length against the transport-authoritative size (F17), F mod 64 (F13),
dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16), dir_offset + dir_length ≤ F − 64 (F10),
generation (F11), file_id (F12), reserved zero (F15), value domain (F2/F3).

The ordering matters and is not cosmetic: §21.2's preamble explains that only the magic and
the CRC precede the version gate, which is why a foreign-major file is refused on capability
grounds before any geometry row can reach it. My implementation returns at this tier without a
slack total, per `[R-CNT-21]`: "Where §6.2's ordered validation rejects the file before a live
trailer is established there is no F and no live state to walk, so the total is not owed at
all ... which is not a partial total but the absence of one."

**Tier 3 — directory region.** Verify the terminal CRC before any other use of the region
(`[R-CNT-11]`, F20). This is the first place a live state exists but is not walkable: F is
established, so a total *is* owed, but only front + trailer + directory can be claimed. Partial
total = F − 16 − 64 − dir_length, naming F20 as what stopped the walk.

**Tier 4 — record walk.** §7.2 framing (F29, F24), MU/PE and reserved flag bits (F25, F26,
F28 at file scope; L46, L47, L49 at layer scope — §7.2 puts a layer record's *governing* scope
at the layer, which is why the layer record's own flag rows live in §21.3), multiplicity
(F34), reserved-range types (F35, F36), extent slots for non-layer top-level records (F30,
F31, F32), the user-metadata framing rules (F21, F22, F23), and the layer-name namespace (F4,
L3, L5, L6).

§19.1 step 4 settles the namespace question I would otherwise have had to guess: a layer
record whose name field does not fit its inline_length "contributes no name to the namespace
and is instead a validity error at layer scope", and uniqueness is decided "over the raw name
bytes whether or not each name is itself well-formed". So F4 fires between two byte-identical
ill-formed names. My implementation follows that.

**Tier 5 — per layer.** §19.3's list, exactly: extent slot, the §7.4 constraint set, the exact
parse and sub-record walk, name rules, value sets, fill constraints, geometry floor and
arithmetic, the 2⁶³−1 ceiling on derived products, and the index cross-checks. All decidable
from the resident directory and F — §19.3 says so explicitly ("layer access performs no
fetch"), which is what makes the verifier's per-layer pass cheap.

Then the index chain: crc_of_crc_array over the stored CRC array (L37), then each segment CRC
over its entries as stored (L38), the final partial segment covering only its actual bytes
(§15.4). Then per-entry classification (§15.3), then the placement invariants, then decode.

**Tier 6 — coverage, overlap, placement.** §9.7's walk. Detailed in §3.

**Tier 7 — verdict.**

### 2.2 Verdict vocabulary — when each is available, and what bars certification

Certification requires **both**: zero established violations, and zero requirements left
unchecked on a capability or resource ground.

- **nonconforming** — any established violation. Takes priority absolutely: "a verifier that
  has established any violation reports *nonconforming*, however many requirements it was
  unable to check" (§2.3).
- **cannot establish** — no violation established, and at least one requirement unable to be
  checked on a capability or resource ground. The document gives five instances of the general
  criterion: a foreign format major; a record carrying MU = 1 with a type the verifier does not
  implement; a codec or filter it cannot execute (`[R-COD-11]`); a layer's or tile's decode
  declined on resource grounds (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`); and a user-metadata
  document it declines to decode (`[R-MTA-09]`). The list is introduced by "as when", so the
  general criterion governs and the five are examples — which is how I resolved the
  experimental-MU=1-*sub-record* case below.
- **conforming** — the residue.

Two report categories that are **not** verdicts and do not move one:

- ***unexamined*** — owed only by a verifier that elected to stop at the first violation.
  "*Unexamined* is neither a verdict nor *cannot establish* — it constrains the report, not the
  verdict."
- **the per-requirement unchecked report** — owed under every verdict, "naming the requirement
  and the ground". §2.3 says this too "constrains the report and not the verdict". I read that
  as: the *duty to name* does not itself change the verdict; the *fact of inability* already
  fixed it as cannot-establish, unless a violation was established. The alternative reading —
  that an unchecked requirement never fixes cannot-establish — is closed by `[R-COD-11]` and
  `[R-MTA-09]`, both of which say MUST NOT certify.

And two things that are reported but bar nothing: SHOULD deviations (`[R-CNF-12]` — "reported
where the verifier observes it and not hunted for"), and each user-metadata record ignored
under an unassigned encoding (`[R-MTA-10]`, a MUST, naming owning scope, encoding value, and
stored extent length).

### 2.3 The case I had to reason out rather than look up

**An experimental-range record type carrying MU = 1 as a layer sub-record.** §21.6 is careful
that the *file-refusal* case is top-level only: "the same type as a layer sub-record is
reject-layer and never a ground to refuse the file". §2.3's cannot-establish list, though,
says "when a record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)",
without the qualifier. If §2.3's citation imported §21.6's top-level restriction, a verifier
meeting such a sub-record would have no stated ground and would have to certify a layer whose
sub-record could, under §7.2, "carry further references where this specification or registry
review defines them" — making the overlap check unsound.

I resolved this from §2.3's own construction: the five grounds are introduced by "as when",
so the operative test is the general one — "some requirement is one it is unable to check on a
capability or resource ground" — and an unimplementable MU = 1 sub-record is squarely that.
Verdict: cannot establish. The file is conforming (`[R-CNF-02]`, §21.6); cannot-establish is
exactly the verdict for "conforming file, verifier's limit", so nothing is lost. Not a finding.

---

## 3. The coverage walk

### 3.1 The partition

§5.2 puts every byte of the live committed state in exactly one of: the front signature block,
or a structure (stored-tile extent, record extent, directory, trailer). §9.7 names the
claimants the walk reaches: the directory itself, each record's extent (including each
sub-record's), and the stored extent of each non-sentinel tile-index entry — plus the front
block and the live trailer, "claimed by the walk as well".

Three traps in that enumeration, all closed by the text:

1. **A record is not a claimant of its own.** Its header and inline payload lie inside the
   directory region, "which is the claimant covering them — so reaching a record through the
   directory is traversal, not a second claim on those bytes." Without that sentence a
   verifier would double-count every record and report negative slack.
2. **The tile-index region enters once**, as the layer record's extent, "and is not a second
   claimant beside it."
3. **Structurally-bad entries contribute nothing.** §15.3's six *structural* rows classify an
   entry "whose own 20 bytes yield no usable extent"; §9.7 says such an entry "does not make
   the walk incomplete: the walk passes over it, and the bytes it nominally addresses fall to
   slack". An entry whose *only* defect is a failed stored-tile crc is well-formed and **keeps
   its extent** — "the defect lies in the bytes it addresses, not in the entry". I checked
   that §15.3's table really has six structural rows: sentinel-with-crc≠0, half-sentinel,
   length 0, offset < 16, field > 2⁶³−1, and sum-overflow-or-past-F−64. Six.

### 3.2 Can any byte be neither certified nor counted?

No. §5.2's own Note gives the argument and I could not break it: "The live committed state is
*defined* as the front block plus what a complete coverage walk reaches, and `[R-LIF-08]` makes
every byte that walk misses slack — so 'belongs to no class' describes nothing, and a register
row for it would be a row no file could exhibit."

I attacked it three ways and each time the byte landed in one of the two classes:

- A structurally-invalid entry with offset 0, length 100. It contributes no extent. Bytes
  [0,16) are the front block (claimed); [16,100) fall to slack unless another claimant takes
  them. §15.3 says exactly this.
- An entry with offset 2⁶³. Nominally addresses nothing inside F.
- A structure in the pre-trailer gap. Its bytes are *claimed* (it is a real claimant reachable
  from the directory) and it is simultaneously an F7 violation. Claimed, not slack, and
  condemned.

But the two-class picture understates what a certificate actually asserts. There is a third,
**claimed-and-disjoint but uninspected**, and a verifier implementer must know it exists:

- **The extent of a record of a type this specification has not assigned.** §8.1's map covers
  it "by no checksum at all"; §7.2 leaves its bytes opaque. §22.3: "corruption inside it is
  equally invisible".
- **The extent of a user-metadata record under an unassigned encoding.** CRC-covered (so
  corruption is caught) but content-unconstrained: `[R-MTA-10]` withdraws every document rule
  there. §22.3 is explicit that "a certificate covers those bytes uninspected — which is why
  `[R-MTA-10]` makes the verifier's report name each such record".

So the honest statement is: *certified* bytes are those the walk claims, finds disjoint, and
verifies against §8.1's map where the map states a checksum; *counted-but-unconstrained* bytes
are slack; and a third set is claimed and disjoint but its content is inspected by nobody. No
byte is in none of the three.

### 3.3 The arithmetic, on a file of my own construction

I built a real file from §6.1, §6.2, §7.2, §7.4, §15.1 and §15.4. Layer `sst`: rank 1,
dimension `x` with E = 100, T = 32; interleaved; one float32 channel `temp` with fill
`0x7FC00000`; codec 1, filter 1; no alignment, no slab. G = ⌈100/32⌉ = 4, N = 4, P = 32,
Q = 4, decoded size P·Q = 128. Tiles 0 and 3 stored, tiles 1 and 2 sentinel. Tile 3 is the
edge tile: it covers x ∈ [96,128), so positions x = 100…127 are padding and carry the fill
bytes `00 00 C0 7F`, per `[R-SER-05]`. Plus a top-level user-metadata record, encoding 1.

Independent cross-check that I had parsed §7.4 correctly: my constructed inline payload came
out at **81 bytes**, which is exactly the length §7.4's worked example states for the same
layer. The field-by-field breakdown also reproduces (4 for the name, 34 for the nine scalars
from layout through channel count, 18 for the dimension entry, 12 for the channel entry, 13
for the trailing fixed fields — 81, no residue, empty sub-record sequence). The extent length
4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 reproduces `[R-CNT-17]`.

Layout, with a deliberate 48-byte gap after the front block so the arithmetic is not trivial:

```
[0,16)      front signature block          claimed      16
[16,64)     gap                            SLACK        48
[64,192)    tile 0 payload                 claimed     128
[192,320)   tile 3 payload                 claimed     128
[320,404)   tile-index region              claimed      84   (layer record's extent)
[404,428)   user-metadata extent           claimed      24   (20-byte doc + 4-byte CRC)
[428,562)   directory region               claimed     134
[562,576)   pre-trailer pad                SLACK        14
[576,640)   live trailer                   claimed      64
F = 640
```

Claimed = 16 + 128 + 128 + 84 + 24 + 134 + 64 = **578**. Slack = 640 − 578 = **62** = 48 + 14. ✓

The verifier's own output on that file:

```
verdict: conforming
violations: []       unable to check: []
   [0,16) 16 bytes  front
   [64,192) 128 bytes  layer sst tile 0
   [192,320) 128 bytes  layer sst tile 3
   [320,404) 84 bytes  layer sst index region
   [404,428) 24 bytes  record extent type 0x0002
   [428,562) 134 bytes  directory
   [576,640) 64 bytes  trailer
F=640 claimed=578  slack total (exact) = 62
```

### 3.4 The same arithmetic for a walk that does not complete

Two layers, `A` and `B`, identical geometry. `A` is laid out so its tile 3 extent [192,320)
overlaps its own index region at [300,384) — an **intra-layer** overlap, which `[R-CNT-13]`
and §15.3 both make **reject-layer**, register row L18. `B` is clean.

§5.2 is the operative rule: "a rejected layer's claimants are not enumerated, whether or not
the rejection impeded reading them — and where the rejection is one the walk itself
established, L18's overlap or L40 through L42's placement among them, the claimants it had
already enumerated are discarded with the layer".

So A's three claimants (two tiles at 128 each, index region at 84 = 340 bytes) are discarded,
and the total is reported as **partial**, naming L18 as what stopped the walk.

```
F = 1216, dir = [896,1106), dir_length = 210

EXACT total, had A been clean : claimed = 16+64+210 + (128+128+84) + (128+128+84) = 970
                                slack = 1216 - 970 = 246
PARTIAL total, A discarded    : claimed = 16+64+210 + (128+128+84)               = 630
                                partial total = 1216 - 630 = 586
```

586 ≥ 246 — the upper-bound property of `[R-CNT-21]` ("an upper bound on the file's true
slack, never an under-count") holds, and holds structurally: discarding claimants only ever
reduces the claimed sum. My implementation reproduces 586 and labels it PARTIAL, naming layer
A. The same rule applied to the alignment case below gives 1856 − 16 − 64 − 109 = 1667 against
a true slack of 1327.

I got this wrong on my first pass — my verifier reported the exact total for a file with an
L18 — and had to go back to §5.2 to find the discard clause. That re-read is what produced
finding **verifier-01**.

### 3.5 Which rejections make the walk incomplete

I worked the full table, because it is not stated in one place:

| Rejection | Walk complete? | Total |
|---|---|---|
| §6.2 gate failure (F8–F19) | no live trailer | **no total owed at all** |
| directory CRC (F20) | no — enumeration never starts | partial: F − 16 − 64 − dir_length |
| any reject-layer row | no — that layer's claimants discarded | partial, naming the layer |
| structural reject-tile (T6–T12) | **yes** — §9.7 says so expressly | exact |
| crc-failing entry (T1) | **yes** — the entry keeps its extent | exact |
| content reject-tile (T2, T3, T4, T5, T14, T17–T26) | **yes** — entry well-formed, extent stands | exact |
| verifier elects to stop at first violation | no | partial + *unexamined* scopes |
| reject-file established **by the walk** (F33, F7) | see **verifier-01** | ambiguous |

The last row is the finding.

---

## 4. Extent overlap, alignment and slab invariants, on adversarial layouts

Not in the abstract — six files, each built to trip exactly one invariant.

**(A) Intra-layer overlap → L18, reject-layer.** Layer `sst`, tile 3 at [200,328), index
region at [320,404). `[R-CNT-13]`: "a verifier MUST treat an intra-layer overlap — including
a stored extent overlapping its own layer's index region or sub-record extents — as
reject-layer". Verifier output: `L18` plus, incidentally, `T1` (the assembler wrote the index
over the tile's tail, so the stored bytes no longer match the entry's crc — a fair
demonstration that overlap and checksum failure are independent findings). Partial total 451
against a true slack of 111.

**(B) Cross-scope overlap → F33, reject-file.** A stored tile of `sst` placed at [424,552),
straddling the directory at [420,529). `[R-CNT-13]`: "any overlap across layers or touching
another scope's structures as reject-file". Verifier output: `F33`. Note the layer itself is
*not* rejected here — F33 is a file-scope row and no L-row fires — so under my reading the
layer's claimants stay enumerated and the total stays exact. This is the case verifier-01 is
about.

I also checked F33's completeness claim by enumerating claimant kinds against the bounds rows
it defers to: directory → F9/F10; non-layer top-level record extent → F31/F32; layer record
extent and sub-record extent → L16/L17; stored-tile extent → T8/T9. Those are all the
claimant kinds there are, so F33's parenthetical ("a claimant reaching the front signature
block or the live trailer is instead caught by the bounds rows ... each at its own tier") is
exhaustive.

**(C) Per-tile alignment → L40.** A = 512 declared, tiles at 64 and 1024. `[R-SLB-01]`: "every
stored tile's offset satisfies offset mod A = 0 ... A verifier MUST check the invariant
(violation: reject-layer, §15.3)". Verifier output: `L40 tile 0 offset 64 not 512-aligned`,
partial total 1667.

**(D) Slab, three files.** S = 2, A_slab = 512, interleaved so the run partition is the single
block [0,4) split into runs [0,2) and [2,4) (`[R-SLB-02]`: "Run r of a block starts at ordinal
block_start + r·S").

- *ok*: tile 0 at 512, tile 1 at 640 = 512 + 128. Packed, and the run's first stored tile is
  512-aligned. **Certified.**
- *gap*: tile 1 at 704. `L41 run at 0: tile 1 at 704, expected 640`.
- *mis*: run 0's first stored tile at 640. `L42 first stored tile offset 640 not 512-aligned`.

The subtle part of `[R-SLB-03]` is what is *transparent* to run continuity. Sentinels are
("they occupy no bytes and do not break packing"), and so are entries §15.3 classifies
reject-tile on a structural ground ("the run's stored tiles close over them"). But an entry
whose only defect is a failed stored-byte crc is **not** transparent — "its offset and length
stand, and the packing relation reads them as it does any other stored tile's". That last
clause is what makes the invariant "decidable from the index entries alone, given the
committed file length", and I want to record why it matters: without it, a verifier would have
to fetch and checksum every tile *before* it could compute the run partition, because it would
not know which entries to skip. As written, the slab check runs off the 20-byte entries and F,
and the crc results are irrelevant to it. My implementation does exactly that and the three
files above confirm the three outcomes.

One thing I noticed and decided is not a defect: L41's *overlap* instance can never be
isolated from L18. If tile k+1's offset is less than tile k's offset plus tile k's length,
those two stored extents of the same layer overlap, so L18 fires too. §24's `[R-VEC-02]`
already provides for exactly this — "where a condition cannot be isolated ... the entry
records every row the file exercises and says which it was built for" — so the corpus rule
absorbs it. Not reportable.

**(E) Padding content → T4.** Tile 3's padding position at x = 100 written as `00 00 00 00`
(float 0.0) instead of the recorded fill `00 00 C0 7F`. `[R-SER-05]`: "at every padding
position, a writer MUST encode, for each channel the position carries, that channel's fill
value ... a verifier MUST check it, and a violation is a validity error at tile scope."
Verifier output: `T4 tile 3 pos 4 channel temp padding != fill`. The layer is not rejected, so
the total stays exact (111).

To compute which positions are padding I had to implement `[R-GEO-06]` in reverse: from the
disk ordinal, recover the spatial ordinal (k for interleaved, k mod N for planar), then invert
s = Σ tᵢ·∏_{j>i} Gⱼ to get tile coordinates, then invert the in-tile ordinal Σ uᵢ·∏_{j>i} Tⱼ,
then test tᵢ·Tᵢ + uᵢ ≥ Eᵢ. I checked the inversion against §11.4's worked example: coordinate
(300, 700) with T = (256,256) and G = (4,8) gives tile (1,2), s = 1·8 + 2 = 10, in-tile
(44,188), in-tile ordinal 44·256 + 188 = 11,452, and planar channel 2 disk ordinal
2·32 + 10 = 74. All four reproduce.

---

## 5. Checksum obligations

### 5.1 Which structures are covered by which checksum

§8.1's map, walked against §4.5's classification:

| Structure | Covered by | Class |
|---|---|---|
| front signature block | nothing — byte equality | equality-checked |
| trailer [0,60) | trailer [60,64) | terminal |
| directory record sequence | final 4 bytes of the region | terminal |
| index entries, per segment | the segment CRC array | interior |
| the segment CRC array | crc_of_crc_array | interior |
| crc_of_crc_array | the directory CRC (it lies in the layer record's inline payload) | — |
| stored tile bytes | its index entry's crc field | — |
| each entry's crc field | its segment CRC | interior |
| user-metadata extent | final 4 bytes of the extent | terminal |
| extent of an unassigned record type | nothing | uncovered |

**Is every live structure covered by one?** Yes, with exactly the three exception classes §4.5
names and no others: the front block (equality), the three terminal fields (comparison-verified,
covered by no further checksum), and the unassigned-type extent (covered by nothing at all). I
went looking for a fourth and could not find one. The chain §8.2 states — trailer → directory →
crc_of_crc_array → segment CRC array → index segment → index entry → stored tile — closes over
everything the walk claims.

The one that took a second look: the segment CRC array sits at the *tail of the index region*,
i.e. inside the layer record's extent, and is therefore not covered by the directory CRC. It is
covered by crc_of_crc_array, which is itself inside the directory. So the region is fully
covered by two different checksums applied to disjoint halves of it — entries by segment CRCs,
CRC array by crc_of_crc_array. My implementation verifies in that dependency order
(`[R-IDX-04]`: crc_of_crc_array first, then the segment).

### 5.2 Constants I reproduced

Every checksum constant the document states, computed locally with a CRC-32C implementation
built from §4.5's parameters alone (Castagnoli 0x1EDC6F41, reflected in and out, init
0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian):

| Constant | §  | Stated | Computed | ✓ |
|---|---|---|---|---|
| CRC-32C("123456789") | §4.5 | 0xE3069283 | 0xE3069283 | ✓ |
| CRC-32C(zero bytes) | §4.5 | 0x00000000 | 0x00000000 | ✓ |
| CRC over 80 bytes of 4 sentinel entries | §7.4 example | 0x80A34955, stored `55 49 A3 80` | 0x80A34955, `55 49 a3 80` | ✓ |
| crc_of_crc_array over that 4-byte array | §7.4 example | 0xC4EE982E | 0xC4EE982E | ✓ |
| CRC of a full 2¹⁶-entry all-sentinel segment | §15.4, App. B | 0xEECB3BB2 | 0xEECB3BB2 | ✓ |
| Appendix A trailer CRC over [0,60) | App. A | 0xE00938D2 | 0xE00938D2 | ✓ |
| Appendix A directory CRC (zero-byte sequence) | App. A | 0x00000000 | 0x00000000 | ✓ |

**Reproduced: all seven.** There is no CRC constant in this document I could not compute
locally. I also re-derived every field of Appendix A's 128-byte file from its hex dump and
each decoded to the value the annotation table gives (version_major 1, minor 0, flags 0,
generation 1, dir_offset 16, dir_length 4, committed_file_length 128, file_id
0x0123456789ABCDEF, reserved zero).

Non-CRC constants and arithmetic I also checked and reproduced:

- §17.3's byte-shuffle example. Three float32 values 1.0, 2.0, 3.0, s = 4, n = 3. Placing byte
  i of group j at offset i·n + j gives `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40` — exactly
  the document's `00 00 00 00 00 00 80 00 40 3F 40 40`.
- §14.3's packed-bool example: P = 10, alternating true/false → byte 0 = 0b01010101 = 0x55,
  byte 1 = 0x01 with six pad bits; with fill true the pad bits set gives 0x01 | 0xFC = 0xFD.
- §15.4's large example: entry_count 1,000,000 → 16 segments (15 full plus 16,960), a 64-byte
  CRC array, region 20,000,064 bytes; tile 999,999 in segment 15 at segment-relative byte
  20 × 16,959 = 339,180; array at [20,000,000, 20,000,064); segment 15 at [19,660,800,
  20,000,000) = 339,200 bytes. All reproduce. A full segment is 65,536 × 20 = 1,310,720 =
  1.25 MiB, as stated.
- §21.9's Note: 2³² entries → 2¹⁶ segments × 4 bytes = 256 KiB; 2³⁶ → 4 MiB. Both reproduce.
- §20.3's example: a 32-tile interleaved layer's index region is 32 × 20 + ⌈32/2¹⁶⌉ × 4 = 644.
- `[R-CNT-17]` at the §21.9 tile-count guarantee: 2³² × 20 + 2¹⁶ × 4 ≈ 80 GiB, which is why
  §24 says that guarantee's vector "is not [constructible] ... running to tens of gigabytes of
  incompressible entries".

**Could not reproduce: none.** Every stated constant is locally computable and every one
matched.

---

## 6. Decoded-content obligations

**What the verifier must decode.**

Every stored tile. §9.7 is flat about it — "A verifier decodes every stored tile, whatever
content obligations §14 places on the layer" — and the obligation is anchored in caps by the
clause that follows: "§21.4's codec rows are file-conformance violations, and a verifier MUST
NOT certify past a violation it has not looked for." That MUST NOT is general and it is what
makes the whole of §21.4 a verifier duty, including T2/T4/T5, which have no MUST of their own
in `[R-SER-08]`. I checked that anchoring deliberately, because a declarative "decodes every
stored tile" with no keyword would have force only through `[R-CNF-01]`'s
everything-is-normative clause; the paired MUST NOT removes the question.

Also: every user-metadata document under an encoding this specification assigns.

**What it compares against.**

- decoded length vs the decoded size derived from declarations alone — `[R-SER-07]`, T3. Never
  from payload content: "readers allocate from those declarations, not from stored data."
- exact consumption of the stored extent — `[R-COD-08]`, T24/T25.
- codec-1 length equality — `[R-COD-04]`, T14 — checkable before any payload fetch.
- zstd frame header: magic (T17), exactly one non-skippable frame (T18), zero dictionary ID
  (T19), no content-checksum flag (T20), window ≤ decoded size (T21), FCS = decoded size when
  present (T22).
- every padding position against the channel's recorded fill — `[R-SER-05]`, T4.
- every pad bit of a packed bool plane against the fill bit — T5.
- every interleaved bool byte at a *real* position against {0x00, 0x01} — T2. (The same byte
  at a padding position is T4's; §21.4 says the two rows together cover `[R-SER-08]`.)
- the document: JSON well-formedness and object-ness (R7), finite numbers (R8), no duplicate
  decoded keys (R9), UTF-8 including after escape resolution (R5), key rules (R6, R10), the
  encoding-2 frame constraints (R4), and member sort order (F27/L48).

**What it is permitted to skip.**

- the *content* of a user-metadata document under an unassigned encoding — `[R-MTA-10]` and
  §17.4's closing sentence. Not a cannot-establish ground: "no content rule attaches there, so
  nothing is left unchecked". But it MUST be reported: owning scope, encoding value, stored
  extent length.
- the content of an unassigned record type's extent (§7.2, §8.1).
- slack content (§5.2 — "their content is not its concern").
- sample values at real, non-boolean positions. §21.7 is explicit that this leaves nothing
  undetermined: "no file-level witness exists to check, so nothing about the file is left
  undetermined and the verdict is unaffected." That sentence is what stops a conscientious
  verifier from reporting cannot-establish on every file that has any sample data.
- searching for SHOULD deviations (`[R-CNF-12]`).

**What it may decline, at the cost of cannot-establish.** A codec or filter it cannot execute
(`[R-COD-11]`); a tile's or layer's decode on resource grounds (`[R-ERR-04]`); a document on
its size bound or the frame's declared window (`[R-MTA-09]`).

An ordering point I had to derive: a verifier must **not** decode a tile whose entry crc
failed. `[R-ENC-05]` and `[R-ENC-10]` forbid acting on unverified bytes, and §19.4 step 5 puts
crc verification "before decoding". So T1 pre-empts the decode, and the skipped §14 checks are
*not* reported as unchecked-on-a-capability-ground — they were skipped on a violation ground,
and the verdict is already nonconforming.

### 6.1 The changed §18.2 passage, read closely

`[R-MTA-09]`'s verifier sentence: "A **verifier** that declines to decode a document on the
bound above cannot establish that document's conformance and MUST NOT certify the file ... the
bound is that verifier's capability and not a limit on validity (`[R-CNF-10]`), so the decline
is not a finding that the file is nonconforming and a verifier MUST NOT report it as one."

"the bound above" is singular, and two bounds precede it — the decoded-size bound and the
frame's declared-window bound. I read the singular as potentially ambiguous, went looking, and
found §21.5's clause resolves it in the same breath: "except where a reader or verifier
declines the decode on the size bound **or** on the frame's declared window, which
`[R-MTA-09]` makes that actor's capability and not a fact about the file." §2.3 also names the
decline generically. Three passages agree that both grounds are covered, so I did not have to
guess and I am not reporting it.

Two consequences for the walk that I checked and that are clean:

- **A decline does not make the walk incomplete.** The user-metadata extent is enumerated as a
  record extent whether or not its document decodes. `[R-CNT-21]`'s two partial grounds are a
  scope-level rejection ending enumeration, and an elected stop; a decline is neither. So the
  slack total stays exact and the verdict is cannot-establish. Same for a codec the verifier
  cannot execute: the stored extents come from the entries, which need no decode.
- **A decline never becomes R3.** `[R-MTA-09]` says the window decline is "not a failure to
  decode within the meaning of R3", and §21.5's clause exempts both grounds from being
  violations at all. So two verifiers with different bounds can report *conforming* and
  *cannot establish* for the same conforming file — licensed by design, and not a fork, since
  cannot-establish "is not a finding that the file is nonconforming".

I did find one thing wrong with that sentence, reported as **verifier-02**.

I also checked the neighbouring risk that §2.3's "A user-metadata document under an encoding
this specification does not assign is not such a ground: ... and certification is unaffected"
could be over-read to cover encoding 0 and the reserved range, where R1 makes the encoding
byte itself a violation. §21.5 closes it explicitly — "Encoding 0 and a reserved-range value
are unassigned too, and R1 registers both as violations: what `[R-MTA-10]` withdraws is the
document's content rules, never the encoding byte's own value set" — and Appendix H repeats
it. The document anticipated the reading and refuted it; not reportable.

---

## 7. Multi-generation trace

Four states, each built as bytes and each run through the verifier.

**Generation 1 — creation.** `[R-LIF-02]`'s creation path: front block; tiles 0 and 3;
index region; the user-metadata extent; the complete directory and its CRC; barrier; pad;
generation-1 trailer with a fresh nonzero file_id; barrier.

```
F = 704   dir = [456,590) len 134   idx = [320,404)   um = [404,453)
claimed = 603   slack = 101
verdict: CONFORMING
```

**Generation 2 — append.** Store tile 1. `[R-WRT-04]` step 4: "Every layer whose stored-tile
set or index content this commit changes has its tile-index region re-emitted in full ...
necessarily at a new placement (`[R-LIF-01]`)". Writing begins at exactly F = 704: tile 1 at
[704,832), the whole new 84-byte index region at [832,916), the re-emitted directory at
[916,1050). Entries for tiles 0 and 3 are byte-identical at their disk-ordinal positions; the
entry for tile 1 is new; tile 2 stays the sentinel. The user-metadata record is re-emitted
byte-identically, extent slot and all (`[R-WRT-05]`), so it still addresses its original
extent at [404,453) — which is why that extent is still a live claimant even though nothing
this commit wrote touched it.

```
F = 1152  idx = [832,916)  um = [404,453) unchanged  dir = [916,1050)
claimed = 731   slack = 421       (gen 1's index region, directory, pad and trailer are now slack)
verdict: CONFORMING
```

**Generation 3 — metadata amendment.** §20.3's shape (c) explicitly says this is not a
directory-only change: "Editing user metadata is not this shape: its document lives in an
extent (`[R-CNT-25]`), so a new extent is appended and the old one becomes slack, as in (b)."
So a new 79-byte extent at [1152,1231), a re-emitted directory at [1231,1365), and the layer
record carried forward byte-identically — its extent slot still pointing at the generation-2
index region, which never moved because the stored-tile set did not change.

```
F = 1408  idx = [832,916) unchanged  um = [1152,1231)  dir = [1231,1365)
claimed = 761   slack = 711
verdict: CONFORMING
```

**Generation 4 — compaction.** `[R-WRT-06]`/`[R-WRT-07]`: a fresh file_id (a new draw, not a
value compared against the input's), generation 1, only live structures, every stored tile's
bytes verbatim and every index entry's crc unchanged, entry offsets new, segment CRCs
recomputed over the entries as re-emitted, and the layer record's crc_of_crc_array updated.
Placement contiguous from offset 16 upward.

```
F = 768   tiles at [16,144) [144,272) [272,400)   idx = [400,484)
          um = [484,563)   dir = [563,697)   trailer = [704,768)
claimed = 761   slack = 7          (the pre-trailer pad, and nothing else)
verdict: CONFORMING, file_id = 0x00DEADBEEFCAFE01, generation = 1
```

The slack curve 101 → 421 → 711 → 7 is the whole argument of §5.2's rationale, and 7 is the
floor for this content: 761 claimed bytes cannot be padded to a multiple of 64 with fewer.

Certification result at each generation: **conforming, conforming, conforming, conforming**.

Two compaction points I checked rather than assumed:

- **Can a compactor clear a stale slab declaration?** `[R-SLB-04]` offers "either re-establish
  the invariants for every such run — or clear the declaration". But §20.5's re-emission rule
  is a closed exception list: "every retained record per §20.4, **except that** relocation
  re-points extent slots, regenerates each relocated tile-index region ..., and updates the
  layer-record fields covering a regenerated region (crc_of_crc_array)." Clearing the slab
  declaration is not on that list. So a compactor always takes `[R-SLB-04]`'s first branch.
  That is achievable — it controls placement — so no contradiction, just a narrowing.
- **Does a compactor's directory change length?** No: extent_offset, extent_length and
  crc_of_crc_array are all fixed-width, so dir_length is unchanged unless a record is dropped.
  My generation-4 directory is 134 bytes, same as generations 1–3. That is a useful invariant
  for a compactor's placement planner and I confirmed it holds in the built bytes.

---

## 8. Findings

### verifier-01 — AMBIGUITY

**Location:** §5.2, `[R-CNT-21]`; read against §9.7 `[R-LIF-08]` and §21.2 rows F7, F33.

**Quotation** (§5.2, `[R-CNT-21]`):

> Where the walk of §9.7 does not enumerate every region's claimants — whether because a
> scope-level rejection ends that scope's enumeration (a rejected layer's claimants are not
> enumerated, whether or not the rejection impeded reading them — and where the rejection is
> one the walk itself established, L18's overlap or L40 through L42's placement among them,
> the claimants it had already enumerated are discarded with the layer, since the total is a
> claim about a live state one of whose layers is not usable), or because the verifier elected
> under `[R-CNF-11]` to stop at the first violation — the verifier MUST report the total as
> partial.

**The problem.** "A scope-level rejection ends that scope's enumeration" is stated over
*scopes*, and §2.4 makes the scopes file, layer and tile. But everything that follows is
written for layer scope: the parenthetical says "a rejected **layer's** claimants", the discard
rule says "discarded **with the layer**", and its justification is "the total is a claim about
a live state one of whose **layers** is not usable". The enumeration of walk-established
rejections names L18, L40, L41 and L42 — all layer rows — and omits **F33** and **F7**, which
are the file-scope rejections the walk itself establishes, F33 being the exact file-scope
analogue of L18 (`[R-CNT-13]` splits one overlap rule into the two by whether the claimants
belong to the same layer).

Three readings are available for a file-scope rejection the walk establishes:

- **(A)** The lead clause is the operative test. With F33 or F7, the walk *did* enumerate every
  claimant, so the total is **exact** and carries no partial label.
- **(B)** "Scope-level" means any scope; a reject-file ends the file's enumeration, and by the
  parenthetical's discard rule everything enumerated is discarded, giving a partial total of
  **F** — formally still an upper bound, and useless.
- **(C)** "Scope-level" means any scope, but the discard clause is expressly "with the layer"
  and so does not apply; the already-enumerated claimants survive, the number equals (A)'s, but
  it MUST be **labelled partial** and the verifier MUST "say which scope or violation stopped
  the walk" — naming F33.

**Which I picked and why.** (A). The lead clause — "Where the walk of §9.7 does not enumerate
every region's claimants" — is the operative test, and the em-dashed clause lists causes rather
than replacing it. §5.2's Note reinforces this: "A partial total (`[R-CNT-21]`) reports what
one verifier's **incomplete** walk left unclaimed". A walk that enumerated every claimant and
then found two of them overlapping is not incomplete. And the parenthetical's careful
enumeration of *exactly* the layer-scope walk-established rows is evidence that the drafters
considered the walk-established set and scoped the discard rule to layers deliberately.

I note the reading is not forced: (C) is the one a cautious implementer might choose, since it
loses nothing and gains a report line naming F33.

**What an implementer does wrong without it.** Reports a wrong slack total for a file whose
only defect is a cross-layer or cross-scope overlap. On my file (B) above, reading (A) reports
a slack total of 111 on F = 640; reading (B) reports 640; reading (C) reports 111 labelled
partial and names F33. §22.3 makes the number consequential — the slack total is "the number
that distinguishes a working file from a padded one" — and §20.3's note makes it the operator's
signal to compact, so three verifiers giving an operator three different numbers for one file
is a real cost. Worse under (B): the verifier tells an operator that a 640-byte file is 640
bytes of slack.

**Byte-level: no.** All three readings produce the same verdict — *nonconforming* — on the same
files, since F33 and F7 are established violations either way. The disagreement is confined to
a diagnostic number and a report label. No byte sequence changes emittability, and no file's
accept/reject verdict moves.

**Suggested minimal repair (not required of me, offered because it is cheap):** either add F33
and F7 to the enumeration alongside L18 and L40–L42 with the discard rule stated for them, or
add a clause stating that a file-scope rejection the walk itself establishes leaves the walk
complete.

---

### verifier-02 — OBSERVATION

**Location:** §18.2, `[R-MTA-09]` — the newly inserted verifier passage.

**Quotation** (§18.2, `[R-MTA-09]`):

> The decline is one of the unchecked requirements `[R-CNF-11]` obliges the verifier to report,
> and it fixes the file's verdict as *cannot establish* only where the verifier established no
> violation elsewhere; the verifier SHOULD report the bound it applied and the stored length of
> the extent it declined.

**The problem.** §2.1's Note states the document's own phrasing discipline: "every SHOULD
states the consequence of deviation". I checked this mechanically against every normative
SHOULD outside blockquotes and appendices — 25 distinct SHOULD-level requirements. Every one
states its consequence in the same sentence or the next, e.g. `[R-CNT-03]` ("A writer that does
not leaves bytes indistinguishable from stale data and forfeits byte reproducibility"),
`[R-CNT-26]` ("misstates the file's feature floor to tooling"), `[R-LIF-07]` ("the consequence
of not doing so is that a torn multi-hour append is recoverable only by scanning back across
its entire length"), `[R-COD-06]` ("a wider window is conforming and merely permits a conforming
reader to decline the tile or the layer on resource grounds"), §20.4's table ("unreported,
application state disappears with no diagnostic"). Three lean on an adjacent restatement
(`[R-SLB-01]` and `[R-SLB-03]` restate `[R-CNT-03]`'s advice; `[R-PRV-03]` follows its
disclosure list). This one states nothing: the sentence ends at "declined", and the next
sentence changes subject to unassigned encodings.

The consequence is not hard to state, and the document states the analogous one next door.
`[R-MTA-10]` handles the parallel case — bytes a certificate covers without inspecting — with a
**MUST** and a rationale: "it MUST report each record it ignored on this ground, naming the
owning scope, the encoding value, and the stored extent length, as it reports the slack total
(`[R-CNT-21]`): bytes a certificate covers without inspecting are counted and named, never
silent." §22.3 completes that thought: "an operator who wants no such bytes rejects on that
report line, a policy above conformance."

The decline case has an equally concrete operator action and it is different: the operator's
remedy for *cannot establish* on a size or window bound is to raise the bound and re-run. To do
that they need the bound applied and the extent's stored length — precisely the two items the
SHOULD names. A verifier that omits them satisfies `[R-CNF-11]`'s MUST (it names the requirement
and the ground) while leaving the operator with a *cannot establish* they cannot act on: no
indication of how much headroom would suffice, and in a file with a top-level document and many
per-layer documents, no indication of which document was declined.

**Why this taxonomy.** Not an AMBIGUITY: the SHOULD is unambiguous, and `[R-CNF-12]` already
tells a verifier that SHOULD deviations do not bar certification, so the *normative* effect is
determined. Not a CONTRADICTION: nothing in the document says otherwise. I am filing it as an
OBSERVATION with the caveat that it does not match the "disproportionately expensive to decide"
gloss either — it is a departure from a self-declared drafting discipline in newly inserted
text, cheap to check and cheap to fix, which is the residual category. §2.1's discipline
statement is itself in a *Note* and therefore non-normative under `[R-CNF-01]`, which is why I
am grading it here and not higher.

**Byte-level: no**, and not close. `[R-CNF-12]` places SHOULD deviation outside the register
entirely: "§21's register enumerates MUST-level conditions only, and a verifier reports a SHOULD
deviation as an advisory that does not bar certification." A dispute about what this SHOULD
requires cannot move the emittable set, cannot change any file's conformance, and cannot change
any verdict. What it costs an implementer is a decision made without knowing what it buys, and
an operator a report line they may not get.

---

## 9. Things I checked and did not report

Recorded so a reader can see the search, not only its output.

- **`[R-MTA-09]`'s "the bound above" (singular) with two bounds preceding.** Resolved by
  §21.5's clause naming both grounds and §2.3's generic phrasing. Three passages agree.
- **§2.3's "certification is unaffected" for an unassigned encoding, read against R1.** §21.5
  refutes the over-broad reading in terms ("Encoding 0 and a reserved-range value are unassigned
  too, and R1 registers both as violations"), and Appendix H repeats it.
- **Whether "A verifier reports one of three verdicts" and "an established violation takes
  priority" bind without a BCP 14 keyword.** They are declarative and normative under
  `[R-CNF-01]`, and — the point that decided it — there is no *capitalized permission* they
  purport to narrow, which is the shape of the rounds 17/18 defects. The prohibitions that
  matter are all in caps (`MUST NOT certify` in §2.3, `[R-COD-11]`, `[R-MTA-09]`).
- **Whether §9.7's declaratives ("It checks that these occupy disjoint byte ranges", "A verifier
  decodes every stored tile") bind.** Each is anchored by a capitalized rule: `[R-CNT-13]`'s
  "a verifier MUST treat an intra-layer overlap ... as reject-layer", `[R-ENC-10]`'s
  verify-before-acting MUST, and §9.7's own "a verifier MUST NOT certify past a violation it has
  not looked for".
- **Register completeness against a verifier's actual checklist.** I walked every verifier
  MUST looking for one with no row: `[R-CNT-05]`→F7, `[R-CNT-12]`→F25/F26/L46/L47,
  `[R-CNT-13]`→F33/L18, `[R-CNT-15]`→F35/F36/L24/L25, `[R-CNT-22]`→F28/L49, `[R-MTA-05]`→F27/L48,
  `[R-SLB-01]`→L40, `[R-SLB-03]`→L41/L42, `[R-SER-05]`→T4/T5, `[R-SER-08]`→T2, `[R-COD-10]`→T26.
  The three verifier-relevant rules with no row (`[R-CNT-02]`'s "belongs to no class",
  `[R-SLB-04]`'s stale declaration, `[R-CNT-18]`'s nesting prohibition) each carry an explicit
  Note explaining why no file exhibits a witness. All eight numeric-identifier spaces of §10.2
  have a reserved-range row.
- **F33's deferral list.** Exhaustive over claimant kinds (checked above).
- **L41's overlap instance never isolable from L18.** §24's `[R-VEC-02]` provides for
  non-isolable conditions.
- **`[R-IDX-05]`'s all-sentinel constant as a shortcut.** "Equality with the constant licenses
  nothing for readers: verification is byte comparison of computed CRCs, never constant
  matching." My implementation computes; I never compare against 0xEECB3BB2.
- **DEFLATE's unconstrained final-byte high bits.** §17.2's Note settles it: two such files are
  both conforming, and they are not one bit apart as whole files because the entry crc, segment
  CRC, crc_of_crc_array and directory CRC all move with them.
- **Whether a verifier that skips a rejected layer's interior owes *unexamined*.** No —
  `[R-CNF-11]` conditions *unexamined* on stopping at the first violation. §5.2's partial total
  naming the layer carries the same information, and §2.3 does not oblige exhaustive enumeration
  once one violation is established.
- **Whether a decline or a codec it cannot execute makes the walk incomplete.** No — stored
  extents are enumerated from the entries, which need no decode.
- **Whether a 5-byte user-metadata extent (the `[R-ERR-05]` hard-limit bound) can be
  conforming.** No: a 1-byte document is never a JSON object, so such a file always exhibits R7.
  That is a corpus-construction fact, not a document defect; §24 already handles multi-row files.

---

## 10. Confidence

**Medium-high.** I implemented the verifier end to end from this document alone, and everything
I needed was there: the ordered algorithm, the verdict lattice, the claimant set, the discard
rule, the six structural entry rows, the slab transparency rule, the checksum map, and the
decode obligations. Every constant reproduced. The register's own row and instance counts
reproduce. The four-generation trace certifies at each step and my hand arithmetic matches the
implementation's at every generation.

The one place two competent implementations would produce different *reports* from this text is
verifier-01, and it is confined to a diagnostic number. I found nothing that forks the bytes or
the verdicts.
