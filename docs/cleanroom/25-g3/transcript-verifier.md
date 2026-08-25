# Cleanroom round 25 — Verifier implementer, working transcript

## 0. Disclosure, up front

**What I read.** `spec/tarn.md` and nothing else. I opened no ADR, no
`PLAN.md`, no `AGENTS.md`/`CLAUDE.md`, no `conformance/`, no
`spec/registry.json`, no git history. I ran no web search or fetch.

**Two breaches to disclose, both accidental, both mine.**

1. **Context I did not ask for appeared before I began.** My runtime placed
   a project-instruction pointer (`CLAUDE.md` → `AGENTS.md`) and an index of
   the maintainer's memory files in my context window. I am naming that it
   appeared, not repeating its contents, and I did not open any file it
   named or act on anything in it.

2. **I executed another agent's scratch file.** I wrote a CRC helper to
   `<scratchpad>/crc.py`, and by the time my second script imported it, the
   file at that path had been *replaced by another round-25 agent's* CRC
   helper — the scratchpad root is shared. Importing it executed their
   module-level prints, and I saw six lines of their output before the
   import error:

   ```
   check 123456789: 0xe3069283
   check empty: 0x0
   Q01 trailer CRC: 0xf33c1f65 65 1f 3c f3
   Q02 image: fd len 1 crc: 0x1e3b70f7 f7 70 3b 1e
   Q03 decoded: 11 33 22 44 66 55
   Q03 stored : 11 44 33 66 22 55 crc: 0x38eb4fc5 c5 4f eb 38
   ```

   That is another walk's CRC scratch (a trailer, a one-byte packed image,
   and a byte-shuffle before/after). It contains no finding, no section
   number and no verdict, and nothing in this transcript derives from it. I
   then listed the shared scratchpad root once, to find a directory name I
   could safely claim; that listing showed me *filenames* from other agents
   and from earlier rounds (`accumulated.diff`, `checks_block.txt`,
   `flat.txt`, `inst.txt`, `l1.json`, various `.tarn` and `.zst` files). **I
   opened none of them.** I then moved all my work into
   `<scratchpad>/vfy-private-rk/` and worked there. I did not read or list
   the `round25/` output directory.

   The exposure is small but it is real, and a disclosed breach is usable
   where a silent one is not.

**Paths.** `spec/tarn.md` was exactly where the brief said it would be:
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, 4,477 lines. No
surprise there.

**What I ran.** Python 3, locally, reading no files except `spec/tarn.md`:
a bit-serial CRC-32C implementation; an extractor over §21.2–§21.5 that
counts register rows and instances mechanically; and a builder that
assembles real TARN files byte for byte and runs the coverage walk over
them. All arithmetic below is machine-computed, not eyeballed.

---

## 1. What I set out to build

A conforming verifier, end to end, on paper but concretely: the ordered
certification procedure, the coverage walk with real arithmetic, the
overlap/alignment/slab checks on adversarial layouts I constructed, the
checksum inventory with every locally-computable constant reproduced, the
decoded-content obligations, and a four-step generation trace with a
certification result after each step.

I read the seven passages the brief named first (§11.1, §20.3, §20.5,
§21.2, §21.3, §21.5, §23.1), then read the document end to end, then built.

---

## 2. The certification procedure, as an ordered algorithm

### 2.1 Verdict vocabulary and what bars certification

`[R-CNF-11]` (§2.3) gives three verdicts and no others: **conforming**,
**nonconforming**, **cannot establish**. Two rules fix their availability
completely:

> "An established violation takes priority: a verifier that has
> established any violation reports *nonconforming*, however many
> requirements it was unable to check, and *cannot establish* is available
> only to a traversal that established no violation."

> "*Cannot establish* is not a finding that the file is nonconforming, and
> a verifier MUST NOT certify a file it reports that way."

So the decision procedure is a two-key lattice:

| established ≥1 violation | ≥1 requirement unchecked (capability/resource) | verdict |
|---|---|---|
| yes | either | **nonconforming** |
| no | yes | **cannot establish** |
| no | no | **conforming** (certify) |

Grounds for "unable to check". §2.3 enumerates with "as when", so the list
is illustrative, not closed:

- a format major the verifier does not implement;
- a record carrying MU = 1 with a type it does not implement (§21.6);
- inability to execute a codec or filter (`[R-COD-11]`) — see finding
  `verifier-04`, this branch is vacuous for a *conforming* verifier;
- declining a layer's or a tile's decode on resource grounds
  (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`);
- declining to decode a user-metadata document (`[R-MTA-09]`).

Expressly **not** a ground, and expressly not a bar: a user-metadata
record under an encoding this specification does not assign
(`[R-MTA-10]`, §21.6) — "no content rule attaches there, so nothing is
left unchecked, and certification is unaffected".

Expressly **not** a bar either: a SHOULD deviation. `[R-CNF-12]`:

> "Deviation from a SHOULD is not a violation for this purpose: §21's
> register enumerates MUST-level conditions only, and a verifier reports a
> SHOULD deviation as an advisory that does not bar certification. A
> verifier owes no search for one."

The observable SHOULD deviations a verifier can stumble into are:
unzeroed gaps (`[R-CNT-03]`), `dir_length + pad + 64 > 65,536`
(`[R-CNT-09]`), a `version_minor` above the floor (`[R-CNT-26]`), a
non-NFC name (`[R-ENC-14]`), a zstd window above 8 MiB
(`[R-COD-06]`, §18.2), and a standardized key outside its listed scope
(`[R-MTA-07]`). All advisory; none searched for.

### 2.2 The report, distinct from the verdict

Four report obligations that constrain the report and not the verdict:

1. **Unchecked requirements** — "A verifier MUST report each requirement
   it was unable to check on a capability or resource ground, naming the
   requirement and the ground, whichever of the three verdicts it
   reports."
2. **Unexamined scopes** — a verifier that stops at the first violation
   "MUST report each scope it did not examine as *unexamined*, which is
   not a finding that the scope is clean."
3. **The slack total** (§5.2, and §3 below), exact or partial; a partial
   total "MUST say which scope or violation stopped the walk."
4. **Unassigned-encoding user-metadata records** — `[R-MTA-10]`: "it MUST
   report each record it ignored on this ground, naming the owning scope,
   the encoding value, and the stored extent length … bytes a certificate
   covers without inspecting are counted and named, never silent."

Note the asymmetry that becomes finding `verifier-03`: obligation 4 exists
for one uncovered-extent class and not for its twin.

### 2.3 The ordered algorithm I would implement

Every step names its input, its checks, and the register rows it can
establish. Ordering constraints that are actually normative are marked
**[ord]**; everything else may be reordered (§19.2 licenses earlier
detection, `[R-CNF-12]`).

**Phase 0 — file size.**
Input: the transport-authoritative length (`[R-CNT-10]`; a local verifier
gets it free). Check `[R-CNT-27]`: ≥ 128 bytes → F5. See `verifier-02` for
the one case where this step's position in the order matters.

**Phase 1 — front signature block. [ord for a resident reader]**
Input: bytes [0, 16). Byte-equality against
`89 54 41 52 4E 0D 0A 1A` + 8 zero bytes. Rows F6, F1's front-block
instance. `[R-CNT-04]` lets a *reader* that would have to fetch these bytes
defer or omit; §2.3 gives a verifier no such exemption, and F6's own text
says so: "a verifier holds no such exemption (§2.3)". So a remote verifier
spends a third range request the two-request open (§6.4) does not budget.

**Phase 2 — trailer, in §6.2's fixed order. [ord]**
Input: bytes [F−64, F).
1. magic → F8, F1's trailer-magic instance;
2. trailer CRC-32C over [0, 60) → F14;
3. version gate (§6.3) → F18 for `version_major = 0`; a major this
   verifier does not implement is **not** a violation but a
   cannot-establish ground (`[R-CNF-02]`: "neither conforming nor
   nonconforming under it");
4. only then: flag gates (F19), `committed_file_length` = size and
   multiple of 64 (F17, F13), `dir_offset ≥ 16` (F9), `dir_length ≥ 4`
   (F16), `dir_offset + dir_length ≤ F − 64` (F10), `1 ≤ generation`
   (F11), `file_id ≠ 0` (F12), reserved [56,60) zero (F15), and the
   2⁶³−1 domain and sum rules (F2, F3).

If any of these fails, no live trailer is established, and §5.2 is
explicit that no slack total is owed: "the verifier reports the trailer
failure and nothing about slack, which is not a partial total but the
absence of one."

*Aside I checked:* `file_id` is deliberately absent from F2's instance
list. `[R-ENC-03]` binds "every offset, length, extent, and count";
`file_id` is none of those, so bit 63 may be set. Appendix G item 2's
derived `file_id` — "the digest's **last eight bytes in output order** …
read little-endian" — routinely exceeds 2⁶³−1, and only the all-zero case
is substituted. Consistent.

**Phase 3 — directory region.**
Input: [dir_offset, dir_offset + dir_length). Terminal CRC over the
preceding dir_length − 4 bytes, **before any other use** (`[R-CNT-11]`,
`[R-ENC-10]`) → F20. Then parse the record sequence (`[R-CNT-12]`) →
F24, F29; multiplicity (`[R-CNT-14]`) → F34; unknown-type MU gate
(`[R-CNT-15]`) → F35, F36; extent slots of non-layer top-level records
(`[R-CNT-13]`) → F30, F31, F32; user-metadata framing → F21, F22, F23;
layer-name namespace over raw bytes (`[R-ENC-13]`, `[R-ENC-15]`) → F4,
and each layer record's own name → L3, L5, L6.

Verifier-only rows at this phase: F25, F26 (record flag bits), F28
(registered type's stored flags), L46, L47, L49.

**Phase 4 — per layer, full record validation (§19.3's list, which §19
warns is not the complete inventory: "§21's register is").**
Everything decidable from the resident directory and F: L1, L2, L4, L7,
L8, L9, L10–L17, L19–L23, L24, L25, L26–L36, L39, L43, L44, L45.
No I/O. A verifier does this for **every** layer, where a reader does it
only for layers it accesses (`[R-RDR-02]`).

**Phase 5 — per layer, index chain.**
`crc_of_crc_array` over the fetched segment-CRC array → L37; each segment
CRC over its entries as stored → L38 (`[R-IDX-04]`). Both are reject-layer
even though a reader's detection point is tile use. Then classify every
entry per §15.3 → T6–T12.

**Phase 6 — per stored tile, payload and decode.**
Entry crc over the stored bytes → T1. Then decode: §9.7 is categorical —
"**A verifier decodes every stored tile**, whatever content obligations
§14 places on the layer: §21.4's codec rows are file-conformance
violations, and a verifier MUST NOT certify past a violation it has not
looked for." Rows T3, T13–T25. Then content: T2, T4, T5, T26.

**Phase 7 — per record extent.**
User-metadata terminal CRC → R2. Under an *assigned* encoding, decode and
check the document → R3–R10, plus F27/L48 for member order. Under an
unassigned encoding (0, reserved, or experimental) no content rule
attaches (`[R-MTA-10]`); encoding 0 and the reserved range are still R1.
The extent of a record of a type this specification has not assigned is
covered by no checksum (§8.1) and constrained by nothing — claimed by the
walk, inspected by nobody.

**Phase 8 — whole-file structural checks (the ones readers are exempt
from).** Coverage walk and slack total (§9.7); overlap F33/L18; the
pre-trailer gap F7; alignment L40; slab L41, L42.

**Phase 9 — verdict.** Apply the two-key lattice of §2.1.

### 2.4 What the verifier reports when a check cannot be run

Three shapes, and the document keeps them apart cleanly:

- **cannot be run on a capability or resource ground** → per-requirement
  report + verdict cannot-establish (absent a violation). §2.3.
- **not run because the verifier stopped at the first violation** →
  *unexamined* for each scope skipped. Not a verdict, not
  cannot-establish. §2.3.
- **nothing to run** — the `[R-MTA-10]` case, where the requirement was
  withdrawn rather than skipped. Reported, but certification unaffected.

The one shape the document does **not** cover: a verifier that does not
stop at the first violation but is nonetheless barred from examining a
rejected layer's tiles. §5.2 mandates that such a layer's claimants drop
out of the walk ("whether or not the rejection impeded reading them"), but
§2.3 ties *unexamined* only to the stop-at-first-violation verifier. I
implemented it as: report those tile scopes as unexamined anyway, because
the alternative — silence — is what §2.3 calls out as misleading. That is
a guess; it costs a report line, not a verdict.

---

## 3. The coverage walk

### 3.1 The claimant set, derived from the rules rather than from a list

`[R-CNT-02]` partitions the live committed state into: the front signature
block; or a structure — a stored-tile extent, a record extent ("the bytes
any record's extent slot references, whatever the record's type"), the
directory, or the trailer. `[R-LIF-08]` (§9.7) turns that into a walk:

> "From the live trailer it reads the live directory and, through its
> records and their sub-records, reaches the claimants `[R-CNT-02]` names:
> the directory itself, each record's extent, and the stored extent of
> each non-sentinel tile-index entry"

with three disambiguations I needed and found:

- a record is **not** a claimant of its own header and inline payload —
  the directory region covers those, "so reaching a record through the
  directory is traversal, not a second claim";
- a layer's tile-index region "enters the walk once, as that record's
  extent, and is not a second claimant beside it";
- the front block [0,16) and the live trailer [F−64,F) "are claimed by the
  walk as well".

Two entry classes behave differently, and §15.3 states both:

- an entry §15.3 classifies reject-tile **on a structural ground**
  contributes no stored extent; "the walk passes over it, and the bytes it
  nominally addresses fall to slack" — and this does *not* make the walk
  incomplete;
- an entry "whose only defect is that its stored bytes fail its crc is
  well-formed: the defect lies in the bytes it addresses, not in the
  entry, so its extent stands and it keeps its place … in the coverage
  walk."

I counted the *structural* rows in §15.3's table: sentinel-with-crc≠0,
half-sentinel, length 0, offset < 16, offset or length > 2⁶³−1,
sum overflow or sum > F−64. **Six.** §15.3 says "Six rows are marked
*structural*". That count is right.

### 3.2 Which bytes are certified, which are counted-but-unconstrained,
### and whether any byte can be neither

**Certified**: every byte the walk claims and a checksum covers. §8.1's
map, checked against every live structure I could enumerate:

| live structure | checksum | verified how |
|---|---|---|
| front signature block | none | byte equality |
| trailer | its own [60,64) | comparison |
| directory region | its own final 4 bytes | comparison |
| tile-index entry array | per-segment CRCs | comparison |
| tile-index segment-CRC array | layer record's `crc_of_crc_array` | comparison |
| stored tile | its index entry's `crc` | comparison |
| user-metadata extent | its own final 4 bytes | comparison |
| extent of a record of an unassigned type | **none** | — |

The map is complete: in format major 1 the only assigned record types are
0x0001 (whose extent is always the tile-index region, §7.4) and 0x0002
(whose extent is a document). Sub-record extents are the same two cases
plus unassigned types. §4.5's closing sentence covers the interior
checksums explicitly — "each segment CRC array, each tile-index entry's
crc field, and each layer record's crc_of_crc_array — are both
comparison-verified and covered by exactly one further checksum" — so no
checksum field is orphaned.

**Counted-but-unconstrained**, two distinct classes:

1. **Slack** — outside the live state. "its content is unconstrained, and
   no conformance requirement applies to it." Counted, never inspected.
2. **Live bytes no rule constrains** — the extent of a record of an
   unassigned type (no checksum, no content rule), and the extent of a
   user-metadata record under an unassigned encoding (a checksum, but no
   content rule, `[R-MTA-10]`). §22.3 names these among its "four residues
   … stated rather than defended". I counted the four: slack; the
   unassigned-type extent; a payload mimicking a trailer; the
   unassigned-encoding metadata extent. Four, correct.

**Can a byte be neither?** No, and the document says why rather than
leaving me to work it out:

> "The live committed state is *defined* as the front block plus what a
> complete coverage walk reaches, and `[R-LIF-08]` makes every byte that
> walk misses slack — so 'belongs to no class' describes nothing, and a
> register row for it would be a row no file could exhibit."

So the partition has one testable half — disjointness — and that is
exactly what F33 and L18 register. Bytes beyond F cannot exist in a
conforming file (F17 ties the physical length to F).

### 3.3 A concrete file, and the arithmetic

I built a real one. Layer `sst` is §7.4's worked example verbatim: rank 1,
dimension `x` with E = 100, T = 32, interleaved, one float32 channel
`temp` with fill `0x7FC00000`, codec 1, filter 1, no alignment, no slab,
linearization 1, index_encoding 1. Grid count ⌈100/32⌉ = 4, so
entry_count = 4 and the inline payload is **81 bytes** — my builder emits
81, matching the document's worked layout byte for byte.

Decoded tile size = P·Q = 32 · 4 = **128 bytes**. Codec 1, so
`[R-COD-04]` forces every stored entry's length to 128.

Generation 1 stores tiles 0 and 1 (both wholly inside the extents, so no
padding obligation yet) and sentinels tiles 2 and 3.

```
generation 1   F = 576
   [    0,   16) front signature block    16
   [   16,  144) tile 0 stored extent    128
   [  144,  272) tile 1 stored extent    128
   [  272,  356) tile-index region        84    = 4·20 + ⌈4/2¹⁶⌉·4
   [  356,  465) directory               109    = 24 + 81 + 4
   [  512,  576) live trailer             64
   ---------------------------------------------
   claimed 529        slack 576 − 529 =  47
```

The 47 is exactly the pre-trailer pad [465, 512) — `[R-LIF-02]` step 5
pads to the next 64-byte boundary, 465 → 512. Every claimant is disjoint;
every non-front, non-trailer claimant lies in [16, 512) = [16, F−64).
Walk complete, total exact.

Cross-check against the document's own smallest file (Appendix A, 128
bytes): claimants front 16 + directory 4 + trailer 64 = 84, slack 44. §5.1
says "44 bytes of slack". Matches.

### 3.4 A walk that does not complete

Same file, one byte changed in the index: tile 1's entry now reads
offset 140, length 128, so its extent [140, 268) overlaps tile 0's
[16, 144) by four bytes. Both are stored extents of the same layer →
**L18**, reject-layer, detector verifier, at certification.

§5.2 then governs:

> "a rejected layer's claimants are not enumerated, whether or not the
> rejection impeded reading them — and where the rejection is one the walk
> itself established, L18's overlap or L40 through L42's placement among
> them, the claimants it had already enumerated are discarded with the
> layer"

So the layer's four claimants (two tiles, the index region) go, leaving
front + directory + trailer:

```
partial total = 576 − (16 + 109 + 64) = 576 − 189 = 387
```

Sanity: the union of *all* claimants would be [0,268) ∪ [272,465) ∪
[512,576) = 268 + 193 + 64 = 525, true slack 51. And 387 ≥ 51 — an upper
bound, "never an under-count", as `[R-CNT-21]` promises. The verifier
reports: **nonconforming**; partial slack total 387; stopped by layer
`sst`, row L18.

This case is clean. The case that is not clean is a **file**-scope
rejection, and that is finding `verifier-01` below.

---

## 4. Extent overlap, alignment, and slab invariants on adversarial layouts

### 4.1 Overlap — where each variant lands

`[R-CNT-13]` routes overlaps by whose structures collide:

> "a verifier MUST treat an intra-layer overlap — including a stored
> extent overlapping its own layer's index region or sub-record extents —
> as reject-layer, any overlap across layers or touching another scope's
> structures as reject-file, and any overlap between two structures
> neither of which belongs to a layer as reject-file"

I built four adversarial variants of the §3.3 file and traced each:

| # | layout | row | outcome |
|---|---|---|---|
| A | tile 1 at [140, 268) vs tile 0 at [16, 144) | L18 | reject-layer |
| B | tile 1 at [360, 460), inside the directory [356, 465) | F33 | reject-file |
| C | tile 1 at [470, 500), inside the pre-trailer gap [465, 512) | F7 | reject-file |
| D | a second layer's index region sharing [272, 356) | F33 | reject-file |

Variant C is the one the coverage walk alone cannot catch: [470, 500) is
disjoint from every other claimant, so disjointness passes and only
`[R-CNT-05]`'s separate check fires. A verifier that implements only the
walk certifies a nonconforming file. F7's Detector cell says verifier and
its detection point is certification; Appendix H lists it as its own line
item. I implemented it as a separate phase-8 predicate.

I checked the boundary claim in F33's own text — that a claimant reaching
the front block or the trailer is caught by the bounds rows instead — and
it holds for every path I could construct. A tile entry cannot reach
[0,16) without tripping T8 (`offset < 16`), and cannot reach [F−64, F)
without tripping T9, because T10 bars length 0, so any extent with
offset ≥ F−64 has offset + length > F−64. A record extent slot of (0, N)
with N ≠ 0 reaches the front block through its zero offset and is F30's /
L15's (half-zero), not F31's — F33 says exactly that, and it is right.

### 4.2 Alignment

`[R-SLB-01]`: "When declared: every stored tile's offset satisfies
offset mod A = 0." Quantified over the *live* generation's stored tiles,
and §20.3 spells out the append-time quantifier that I would otherwise
have had to supply myself — "an aligned layer's stored tiles — **every one
the new state keeps, not only those this commit adds** — satisfy its
invariant or the declaration is cleared". That is a quantifier this
document has clearly already been bitten by, and it now reads correctly.

Adversarial: declare A = 512 on the §3.3 file. Tiles sit at 16 and 144;
16 mod 512 = 16 ≠ 0 and 144 mod 512 = 144 ≠ 0 → **L40** twice (one row,
two witnesses), reject-layer, verifier, certification. Partial slack total
387, as in §3.4.

Note what alignment does *not* reach: the tile-index region, sub-record
extents, and the directory. `[R-SLB-01]` names stored tiles only. I looked
hard for a sibling quantity governed by nothing here and did not find one
— placement of everything else is free by `[R-SLB-05]` and the bytes
between are slack, which is a stated answer rather than a gap.

A degenerate case the document permits and I would certify: A = 2⁶², on a
layer with every entry a sentinel. No stored tile, so no offset to
misalign, and `[R-CNT-23]`'s bounds (power of two, 512 ≤ A ≤ 2⁶²) are
satisfied. Conforming. Nobody would write it; nothing rejects it.

### 4.3 Slabs

`[R-SLB-02]` partitions disk ordinals into runs per contiguous block —
[0, N) interleaved, [c·N, (c+1)·N) per channel planar, run r starting at
`block_start + r·S`. `[R-SLB-03]` then requires, per run, packing in
ordinal order and A_slab-alignment of the *first stored* tile.

Transparency rules, both stated: sentinels are transparent; entries §15.3
classifies reject-tile on a structural ground are transparent; an entry
failing only its stored bytes' crc is **not** transparent. That last one
is what makes the invariant decidable without fetching payloads —
`[R-SLB-03]` says so, and it is right: from the entries plus F you can
classify every entry, and crc-pass versus crc-fail does not change an
entry's participation.

Adversarial layout, built concretely. Same layer, now S = 2,
A_slab = 512, all four tiles stored, 128 bytes each:

```
run 0 = ordinals [0,2)     tile 0 @  512   512 mod 512 = 0     ok
                           tile 1 @  640   = 512 + 128         packed
run 1 = ordinals [2,4)     tile 2 @  900   900 mod 512 = 388   L42
                           tile 3 @ 1030   ≠ 900 + 128 = 1028  L41 (gap 2)

index region [1158, 1242)   directory [1242, 1351)
pad [1351, 1408)            trailer [1408, 1472)      F = 1472
```

Complete-walk slack, had the layer been clean:
1472 − (16 + 4·128 + 84 + 109 + 64) = 1472 − 785 = **687**, which I
verified equals the sum of the four gaps 496 + 132 + 2 + 57 = 687.

But L41 and L42 are placement rejections the walk itself establishes, so
§5.2 discards the layer's claimants:
partial total = 1472 − (16 + 109 + 64) = **1283**. Upper bound on 687. ✓

Verdict: **nonconforming**; partial total 1283; stopped by layer `sst`,
rows L41 and L42.

Two more slab cases I checked because they are the shapes a naive
implementation gets wrong:

- A run whose only stored tile is its last ordinal: packing is vacuous,
  alignment binds that one tile. "A run with no stored tiles imposes
  nothing" covers the empty case explicitly.
- S > N: the block has one run covering fewer than S ordinals — "the final
  run of a block can cover fewer than S ordinals". Legal.
- `[R-SLB-04]`'s stale declaration carries no row of its own, and §16.2's
  Note explains why: a stale declaration that still satisfies the
  invariants *is* a re-established declaration, and one that does not
  exhibits L41 or L42. I tried to construct a counterexample and could
  not. The reasoning is sound.

---

## 5. Checksum obligations

### 5.1 Constants I reproduced

Bit-serial CRC-32C, reflected polynomial 0x82F63B78 (the reflection of
0x1EDC6F41), init 0xFFFFFFFF, final XOR 0xFFFFFFFF, exactly as §4.5
states. Every constant the document states that is computable from the
document alone:

| constant | document | computed | § |
|---|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283 | **0xE3069283** | §4.5 |
| CRC-32C(zero bytes) | 0x00000000 | **0x00000000** | §4.5 |
| CRC over 4 sentinel entries (80 B) | 0x80A34955 | **0x80A34955** | §7.4 |
| `crc_of_crc_array` over those 4 bytes | 0xC4EE982E | **0xC4EE982E** | §7.4 |
| CRC of a full all-sentinel segment (2¹⁶ entries, 1,310,720 B) | 0xEECB3BB2 | **0xEECB3BB2** | §15.4 |
| Appendix A trailer CRC over [0,60) | 0xE00938D2 | **0xE00938D2** | App. A |
| Appendix A directory CRC (zero bytes) | 0x00000000 | **0x00000000** | App. A |

All seven reproduce. That is every CRC constant in the document.

### 5.2 Non-CRC constants I could also check by arithmetic

- bfloat16 1.0 = 0x3F80 from binary32 0x3F800000's high half, stored
  `80 3F`; 0x7FC0 ↔ 0x7FC00000. ✓ (§12.1)
- §12.3's channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` — length 4,
  "temp", type 12 LE, fill length 4, `0x7FC00000` LE. ✓
- §4.6's `température` in NFC = 12 bytes
  `74 65 6D 70 C3 A9 72 61 74 75 72 65`. ✓
- §17.3's byte-shuffle example: 1.0f/2.0f/3.0f decode to
  `00 00 80 3F 00 00 00 40 00 00 40 40`; with s = 4, n = 3, byte i of
  group j lands at i·n + j, giving
  `00 00 00 00 00 00 80 00 40 3F 40 40`. ✓ exactly as printed.
- §14.3's packed-bool example: P = 10, alternating from true → byte 0 =
  0x55, byte 1 = 0x01 with fill false, 0xFD with fill true (pad bits 2–7
  set). ✓
- §15.4's 1,000,000-entry worked example: 16 segments (15 full + 16,960),
  64-byte CRC array, region 20,000,064 B, entry 999,999 at segment 15
  offset 339,180, segment 15 at [19,660,800, 20,000,000), full segment
  1.25 MiB. ✓ every figure.
- §21.9's note: ⌈2³²/2¹⁶⌉ · 4 = 256 KiB, ⌈2³⁶/2¹⁶⌉ · 4 = 4 MiB. ✓
- §20.3's example: 32·20 + ⌈32/2¹⁶⌉·4 = 644. ✓
- §11.4's example: (300,700) → tile (1,2), s = 10, in-tile (44,188),
  ordinal 11,452; planar channel 2 → 2·32 + 10 = 74. ✓
- §14.2's examples: Q = 3 → 18 bytes, ordinal 5 at [15,18); planar b →
  12 bytes, ordinal 5 at [10,12); float32+bool → Q = 5, 30 bytes,
  ordinal 5 at [25,30). ✓

### 5.3 What I could not reproduce, and why

- The zstd frame magic 0xFD2FB528 / `28 B5 2F FD` and the LZ4 frame magic
  `04 22 4D 18` are constants of external specifications (RFC 8878, the
  LZ4 Block Format Description). The document pins them by reference
  (Appendix F). I cannot confirm them from this document alone and did not
  try.
- The 8 MiB `Window_Size` figure is described as "the decoder window
  support RFC 8878 itself recommends" — an external claim.
- The lz4 cap 0x7E000000 is "the block format's practical
  interoperability bound" — external.

None of these is a defect; they are exactly the pinned external references
§1 says codecs are.

### 5.4 Is every live structure covered?

Yes, with one stated exception and one that surprised me only in its
reporting consequence.

- Covered: every structure in §5.1's table above except the last row.
- Not covered: the extent of a record of a type this specification has not
  assigned. §8.1's map states this, §4.5 restates it, §22.3 names it a
  residue. That is honest.
- The extent of a user-metadata record under an *unassigned encoding* is
  covered by its terminal CRC but by no content rule — a distinct residue,
  and `[R-MTA-10]` obliges the verifier to name each such record.

The asymmetry between the last two is finding `verifier-03`.

---

## 6. Decoded-content obligations

**What a verifier must decode.** Every stored tile, unconditionally
(§9.7). Every user-metadata document under an encoding this specification
assigns (`[R-MTA-09]`'s decline is a *cannot-establish* ground, which only
makes sense if decoding is otherwise owed; R3–R10 are register rows, and
§2.3 puts every file-level requirement on the verifier).

**What it must compare against.**

| obligation | rule | row |
|---|---|---|
| decoded payload length = decoded size | `[R-SER-07]` | T3 |
| codec 1: entry length = decoded size | `[R-COD-04]` | T14 |
| decode consumes the extent exactly | `[R-COD-08]` | T24 |
| stream/frame/block well-formed | `[R-COD-08]`, `[R-COD-05..07]` | T15–T25 |
| every padding position = channel fill | `[R-SER-05]` | T4 |
| every pad bit = channel fill bit | `[R-SER-05]`, `[R-SER-03]` | T5 |
| interleaved bool byte ∈ {0x00, 0x01} at a real position | `[R-SER-08]` | T2 |
| document content rules | `[R-MTA-04]`, `[R-CNT-25]` | R3, R5–R10 |
| document member order | `[R-MTA-05]` | F27, L48 |

I checked that T2 and T4 together really do cover `[R-SER-08]`, as T2
claims. A padding position's interleaved bool byte must be the recorded
fill byte, which `[R-TYP-07]` constrains to 0x00 or 0x01, so a padding
byte of 0x02 is T4's; a real position's is T2's. There is no third
placement. Correct.

T4's four instances — interleaved numeric, interleaved bool, planar
numeric plane, packed planar bool bit — exhaust the ways a padding
position can carry a value, given §14.2 and §14.3. Correct.

**What it is permitted to skip.** §21.7 is the account, and it is the
right one:

> "this format detects *corruption of structure*, not *incorrectness of
> content*. A writer that emits well-formed structures carrying wrong
> sample values … produces a file that every checksum in §8 certifies."

and crucially:

> "None of these is a requirement a verifier is *unable to check* within
> the meaning of `[R-CNF-11]`: no file-level witness exists to check, so
> nothing about the file is left undetermined and the verdict is
> unaffected."

That sentence is load-bearing for my implementation: it is what stops a
verifier from reporting cannot-establish on every file merely because
sample content is uncertifiable. It also has a boundary I flag as
`verifier-05`.

**What it may decline.** Only where `[R-ERR-04]` licenses it — a quantity
outside §21.9's minimum guarantees. "Software that declines **on that
ground** a file whose every quantity lies within the table is not a
conforming reader." So a 300 MiB decoded tile may be declined (256 MiB
guarantee); a 4 MiB one may not. A decline is reported as a resource
limit, never as corruption, and yields cannot-establish.

One imprecision I noted and worked around: §2.3 says a resource decline
means the verifier "cannot check §14's decoded-content obligations
(`[R-SER-05]`, `[R-SER-08]`)". It equally cannot check `[R-SER-07]` and
`[R-COD-08]` — T3, T24, T25 all need the decode. Since §2.3's list is
introduced with "as when" and the operative test is "some requirement is
one it is unable to check", I report all of them. Not a finding; a
partial citation inside an open list.

---

## 7. Multi-generation trace

One layer, `sst`, as in §3.3. Written, appended to, updated, compacted.
Every number below is machine-computed from real bytes.

### Generation 1 — creation (`[R-WRT-02]`, `[R-LIF-02]` creation path)

Front block, tiles 0 and 1, index region, directory, barrier, pad,
generation-1 trailer with a fresh nonzero `file_id`, barrier. Layout as in
§3.3.

```
F = 576   claimed 529   slack 47   (the pre-trailer pad)
```

**Verdict: conforming.** Exact slack total 47. Nothing unchecked.

### Generation 2 — append: supersede tile 1, store tile 3

Tile 3 covers x ∈ [96, 128); E = 100, so x ∈ [100, 128) — in-tile ordinals
4–31 — are padding positions and `[R-SER-05]` fixes each to the recorded
fill `00 00 C0 7F`. My tile 3 is four real float32 samples followed by
28 × `00 00 C0 7F` = 112 bytes. A verifier decodes it and checks all 28.

The layer's stored-tile set changed, so `[R-WRT-04]` re-emits the whole
tile-index region at a new placement; the layer record's extent slot moves
with it, so the layer record is modified rather than re-emitted
byte-identically.

```
generation 2   F = 1152
   [    0,   16) front                    16
   [   16,  144) tile 0 (unmoved)        128
   [  576,  704) tile 1 (new)            128
   [  704,  832) tile 3 (new)            128
   [  832,  916) index region (new)       84
   [  916, 1025) directory                109
   [ 1088, 1152) trailer                   64
   ---------------------------------------------
   claimed 657        slack 1152 − 657 = 495
```

The 495 decomposes exactly as §20.3's cost note predicts: superseded
tile 1 (128) + old index region (84) + old directory (109) + old pad (47)
+ old trailer (64) + new pad (63) = 495. Machine-checked.

**Verdict: conforming.** Exact slack total 495. Note the shape §20.3's
note warns about — one superseded tile of 128 bytes cost 495 bytes of
slack, because the index and directory go with it.

### Generation 3 — update: add a file-scope user-metadata record

Encoding 1 (none). Document, members sorted by their keys' UTF-8 bytes as
`[R-MTA-05]` requires:

```json
{"tarn.creator":"tarnw 0.1","tarn.title":"sea surface temp"}
```

60 bytes + 4-byte terminal CRC = extent_length 64, comfortably above
`[R-CNT-25]`'s floor of 5. The record carries type 0x0002 with the
registry-fixed flags MU = 0, PE = 1 (§7.3) and inline_length 1
(`[R-MTA-03]`). The layer record is re-emitted **byte-identically**,
extent slot and all, per `[R-WRT-05]` — its index still lives at 832.

```
generation 3   F = 1472
   [    0,   16) front                    16
   [   16,  144) tile 0                  128
   [  576,  704) tile 1                  128
   [  704,  832) tile 3                  128
   [  832,  916) index region             84
   [ 1152, 1216) user-metadata extent     64
   [ 1216, 1350) directory                134
   [ 1408, 1472) trailer                   64
   ---------------------------------------------
   claimed 746        slack 1472 − 746 = 726
```

**Verdict: conforming.** Exact slack total 726 — now half the file. This
is the number §5.2 says "tells an operator to compact", and it does.

### Compaction (`[R-WRT-06]`, `[R-WRT-07]`, `[R-WRT-09]`)

Fresh `file_id`, generation 1, `[R-LIF-02]`'s **creation** path (§20.5 is
explicit: "The pad of step 5 and the barriers of steps 4 and 6 — both, not
one — are owed here as they are of a creator"). Every stored tile's bytes
verbatim, every entry crc unchanged, the index region *regenerated* with
new offsets and recomputed segment CRCs, `crc_of_crc_array` updated, the
user-metadata extent relocated and its slot re-pointed. Unknown ignore-lane
flag bits carried forward (none here).

```
compacted output   F = 768, generation 1, new file_id
   [    0,   16) front                    16
   [   16,  144) tile 0                  128
   [  144,  272) tile 1                  128
   [  272,  400) tile 3                  128
   [  400,  484) index region             84
   [  484,  548) user-metadata extent     64
   [  548,  682) directory                134
   [  704,  768) trailer                   64
   ---------------------------------------------
   claimed 746        slack 768 − 746 = 22   (pre-trailer pad only)
```

**Verdict: conforming.** Exact slack total 22. File length 1472 → 768;
704 bytes reclaimed; claimed bytes identical (746) as `[R-WRT-07]` requires
("The output's reference arrays MUST equal the live generation's bit for
bit").

Two compactor rules I exercised on paper against this trace and found
determinate:

- Regenerating the index means classifying every entry (§20.5). A sentinel
  is re-emitted unchanged; every other entry is re-pointed. An entry §15.3
  classifies reject-tile on a structural ground is neither, so
  "regenerating the region cannot proceed without meeting it", and
  `[R-WRT-06]` obliges refusal — no drop is available, "a tile-index entry
  being no record §20.4's table licenses dropping". Clean.
- The compactor's verification depth is `[R-WRT-09]`'s and "reaches no
  decoded content". So a T4 padding violation in tile 3 would travel into
  the output undetected, which §20.1 sanctions expressly ("a violation
  latent in a structure they neither modify nor rely on travels with it").
  A verifier run on the output would then report nonconforming. That is
  coherent, not a gap.

---

## 8. Mechanical checks of the register's own counts

Because the brief warns that four counts have been found short in four
cycles, I extracted §21.2–§21.5 and counted by §21.1's stated rule — a
cell reading "—" is one instance, otherwise semicolon-separated items.

```
rows:      F 36   L 49   T 26   R 10      total 121
instances: F 58   L 116  T 55   R 48      total 277
```

§21.2 says "36 conditions", §21.3 "49 conditions", §21.4 "26 conditions",
§21.5 "10 conditions", §21.8 "121 conditions over 277 instances". **All
five match.** Detector/detection-point pairs are consistent too: 20 rows
carry Detector *verifier*, all 20 at *certification*, and no reader-detected
row is placed at certification.

Two derived counts I also checked by deriving the members rather than
trusting the prose:

- §15.3's "Six rows are marked *structural*" — I counted six. ✓
- §20.5's "F36 and L25 for a record type, and one row for each of the
  other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" —
  §10.2 tabulates eight spaces; the other seven are index encoding (L31),
  linearization (L33), sample type (L34), channel layout (L36), codec
  (L43), filter (L45), metadata encoding (R1). ✓
- §21.2's "Four rows are outside that reasoning" — F1, F6, F8, F14. The
  *criterion* is right; the *argument* offered for it is not, which is
  `verifier-02`.
- §22.3's "Four residues" — I derived four. ✓

The one instance cell I second-guessed was L18's three ("stored-tile
extents; tile-index region; layer sub-record extents"), because an
intra-layer overlap can also pair index-region against sub-record extent,
or sub-record against sub-record. But F33's cell uses the same convention
— it enumerates the *kinds* of claimant, not the pairs — so L18's three is
consistent with the document's own practice. Not a finding.

---

## 9. Findings

### verifier-01 — AMBIGUITY

**Where.** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`.

**Quoted.**

> "Where the walk of §9.7 does not enumerate every region's claimants —
> whether because a scope-level rejection ends that scope's enumeration (a
> rejected layer's claimants are not enumerated, whether or not the
> rejection impeded reading them — and where the rejection is one the walk
> itself established, L18's overlap or L40 through L42's placement among
> them, the claimants it had already enumerated are discarded with the
> layer, since the total is a claim about a live state one of whose layers
> is not usable), or because the verifier elected under `[R-CNF-11]` to
> stop at the first violation — the verifier MUST report the total as
> partial. A partial total is F less the bytes claimed by the claimants
> the walk did enumerate"

**The problem.** Every clause that says *which claimants survive into a
partial total* is written about a **layer**. Nothing says what survives
when the rejection is at **file** scope. But file-scope rejections that
occur after a live trailer is established are common — F20 (directory CRC),
F33 (cross-scope overlap), F7 (a structure in the pre-trailer gap) — and
§5.2's excusal from reporting a total at all is expressly narrow: it
covers only the case where "§6.2's ordered validation rejects the file
before a live trailer is established". So a total is owed, and the
document does not fix its value.

**Worked instance.** My §3.3 file, F = 576, with the directory's terminal
CRC corrupted (F20, reject-file, detected at open). `[R-ENC-10]` bars
acting on any record field, so nothing past the directory can be
enumerated. Three defensible partial totals:

- **A.** Front block (16), directory (109) and trailer (64) were
  enumerated before the failure — §9.7 enumerates claimants and *then*
  checks "that each verifies against the checksum covering it" — so
  partial = 576 − 189 = **387**.
- **B.** A file-scope rejection ends the file's enumeration exactly as a
  layer-scope one ends a layer's, and by the stated rationale ("the total
  is a claim about a live state one of whose layers is not usable" — here
  the whole live state is unusable) everything is discarded, so
  partial = **576**.
- **C.** Only the claimant whose checksum failed is discarded, front and
  trailer standing, so partial = 576 − 80 = **496**.

A second instance separates the readings differently: variant B of §4.1
(a stored tile at [360, 460) inside the directory, F33). Here the walk
*did* enumerate every claimant — overlap detection requires that — so
"tightening to the exact total when the walk completes" argues the total is
**exact**, 576 − |union| = 576 − 401 = **175**; while "a scope-level
rejection ends that scope's enumeration" argues it is partial, and B gives
576. So the readings differ not only in value but in the *label* the
verifier attaches, which is itself normative ("It is not the file's slack
total but a bound on it").

**Which I picked.** A, and *partial*. Rationale: §9.7's ordering makes
enumeration precede checksum verification, so the claimants reached were
enumerated; the discard clause is written for layers and I declined to
extend a rule the document scoped; and labelling it partial is the safe
side of "an upper bound on the file's true slack, never an under-count".
I also report which row stopped the walk, which `[R-CNT-21]` requires.

**Cost to an implementer without this.** Two conforming verifiers hand an
operator different slack figures for the same file — 387 versus 576 versus
496 — and one of them says "exact" where the other says "partial". §22.3
makes that number a security-relevant signal ("the number that
distinguishes a working file from a padded one"), and §20.3's note makes
it the compaction trigger. A number two tools disagree about by a factor of
1.5 is not a signal.

**Byte-level?** No. It changes a reported diagnostic quantity and its
label. Both verifiers report *nonconforming*, both readers reject the
file, and no writer's output changes.

---

### verifier-02 — OBSERVATION

**Where.** §21.2, opening paragraph; §5.1 `[R-CNT-27]`; §2.3 `[R-CNF-02]`.

**Quoted.**

> "A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below
> whose subject is that file's *geometry* do not reach it: §6.2 puts the
> version gate ahead of every check but the trailer magic and the trailer
> CRC, so such a file is refused on capability grounds first."

and, from §5.1:

> "A reader MUST treat a shorter file as a validity error at file scope.
> `[R-CNT-27]`"

**The problem.** The justification offered — that the version gate comes
ahead of everything but the magic and the CRC — is not true of
`[R-CNT-27]`. §6.2's ordered list is "the trailer magic; the trailer CRC;
the version gate … and then, those gates passed, … the flag gates;
committed_file_length equals the file size …". The 128-byte minimum is not
in that list; it lives in §5.1, it is decidable from F alone with no
trailer at all, and §19.2 expressly licenses earlier detection ("A reader
MAY detect any violation earlier"). §21.2 handles the parallel case
correctly for F6 by citing `[R-CNT-04]`'s "before other processing" — and
then does not apply the same test to F5.

**Constructible instance.** A 96-byte file: a correct 16-byte front block,
a trailer at [32, 96) with correct magic and correct CRC, and
`version_major = 7`. Verifier A checks `[R-CNT-27]` at open (it is F5's
Detected tier), establishes a registered violation, and by §2.3's "An
established violation takes priority" reports **nonconforming**. Verifier B
follows §6.2's order, fails the version gate, and reports **cannot
establish**.

**Which I picked.** Cannot establish. `[R-CNF-02]` settles it independently
of check order — "a file declaring another major is neither conforming nor
nonconforming under it" makes the *nonconforming* verdict unavailable
whatever the verifier noticed — and §21.2's actual criterion ("their
subject is a field fixed across every major") gives the same answer, since
the 128-byte floor derives from `dir_offset ≥ 16`, `dir_length ≥ 4` and
64-alignment, all of which live in the 48 trailer bytes `[R-CNT-24]` lets a
future major redefine.

**Cost to an implementer without this.** They must reconstruct a
three-passage argument to place one check in the order, and the passage
that looks like it is telling them the answer tells them a false thing.
Reading §21.2's stated reason literally and applying it to F5 yields the
wrong verdict. It is decidable — hence OBSERVATION rather than AMBIGUITY —
but expensive to decide.

**Byte-level?** No. The reader-level outcome is reject-file under either
reading, so no byte sequence changes hands differently; only the verifier's
verdict label and the diagnostic (§6.3's SHOULD asks it to be distinct from
"corrupt") are at stake, and `[R-CNF-02]` decides even that.

---

### verifier-03 — OBSERVATION

**Where.** §8.1 `[R-CNT-19]`; §22.3 `[R-SEC-04]`; §18.2 `[R-MTA-10]`.

**Quoted.** §8.1's map row:

> "| Extent of a record of a type this specification has not assigned |
> none — the bytes are opaque (§7.2) | — |"

and §22.3, treating it and the metadata case as one residue class:

> "The extent of a record of a type this specification has not assigned is
> covered by no checksum either (§8.1), so corruption inside it is equally
> invisible … And the extent of a user-metadata record under an unassigned
> encoding is covered by its terminal CRC but constrained by no content
> rule (`[R-MTA-10]`): the CRC detects corruption and authenticates
> nothing (§4.5), so a certificate covers those bytes uninspected — which
> is why `[R-MTA-10]` makes the verifier's report name each such record,
> and an operator who wants no such bytes rejects on that report line, a
> policy above conformance."

**The problem.** §22.3 puts both extents in the same residue class and
gives the same reason — a certificate covers bytes nobody inspected — but
only one of them carries a reporting obligation. `[R-MTA-10]` says the
verifier "MUST report each record it ignored on this ground, naming the
owning scope, the encoding value, and the stored extent length … bytes a
certificate covers without inspecting are counted and named, never
silent." No rule anywhere says the same of the extent of a record of an
unassigned type — and that one is *worse*, being covered by no checksum at
all, so its corruption is invisible to reader and verifier alike, exactly
as slack's is.

An experimental-range MU = 0 record is a **conforming** file's furniture
(§21.6's row), so this is not an edge case reachable only through
violations: a verifier certifies such a file, and the certificate silently
covers an arbitrary, unchecksummed, unconstrained extent.

**Which I picked.** I report it: owning scope, record type value, extent
offset and length, and the fact that no checksum covers it. §22.3's
"policy above conformance" sentence describes the operator control that
`[R-MTA-10]` creates, and an operator who wants that control needs the
same line for both classes. But I am supplying the obligation, not reading
it.

**Cost to an implementer without this.** Two verifiers' certificates
differ in what they disclose about the same conforming file. One names the
uninspected bytes and one does not, and the operator policy §22.3
describes — "rejects on that report line" — works against unassigned
*encodings* and silently fails against unassigned *types*.

**Byte-level?** No. Report content on a file both verifiers certify.

---

### verifier-04 — OBSERVATION

**Where.** §17.4 `[R-COD-11]`; §2.3 `[R-CNF-11]`; §21.3 L43, L45.

**Quoted.** §17.4, second and fourth sentences:

> "A verifier that cannot execute a layer's codec or filter cannot
> establish that layer's conformance and MUST NOT certify the file. That
> inability is not a finding that the file is nonconforming, and it fixes
> the file's verdict as *cannot establish* only where the verifier
> established no violation elsewhere (`[R-CNF-11]`). For a conforming
> reader that position arises only at a reserved or experimental value,
> every assigned codec and filter being core: it rejects the layer
> (`[R-COD-03]`, `[R-COD-09]`); software unable to execute an assigned
> codec or filter is not a conforming reader (`[R-CNF-03]`)."

and §2.3's ground list, which cites it:

> "when it cannot execute a codec or filter (`[R-COD-11]`)"

**The problem.** Put the two halves side by side, which is what the
brief's "argument by analogy" test asks. Codecs 1–4 and filters 1–2 are all
core, and `[R-CNF-03]` makes software that cannot execute one **not a
conforming reader**, hence not a conforming verifier (§2.3: "Verifiers and
updaters are readers of the files they process and inherit every reader
obligation"). So the only value at which a *conforming* verifier meets a
codec it cannot execute is a reserved or experimental one — and that value
is itself a violation (L43 for codec, L45 for filter, `[R-COD-03]` /
`[R-COD-09]`, reject-layer, detector reader). §2.3 then forces
**nonconforming**, because "An established violation takes priority".

The cannot-establish branch of `[R-COD-11]`'s second sentence is therefore
unreachable by any conforming verifier, and §2.3 lists it as a live ground
beside four that are reachable. §17.4's fourth sentence is what closes it,
and it reads as an aside rather than as the sentence that empties the
second.

**Which I picked.** A reserved or experimental codec/filter value yields
**nonconforming**, not cannot-establish; I implemented no
codec-capability cannot-establish path at all. The reachable
codec-adjacent cannot-establish ground is the *resource* one — §17.2's
"a wider window is conforming and merely permits a conforming reader to
decline the tile or the layer on resource grounds (`[R-ERR-04]`)" — which
is a different rule with a different citation.

**Cost to an implementer without this.** An implementer who reads §2.3's
ground list and §17.4's second sentence, and stops there, reports *cannot
establish* for a file carrying codec 7. That file is nonconforming and the
verifier must say so. It is a verdict error on a constructible file,
reachable by a plausible reading path, and it is fixed only by the fourth
sentence of the same paragraph.

**Byte-level?** No — the text does decide it, and the reader outcome
(reject-layer) is the same either way. But the verdict divergence is real
for a careless implementation, which is why I report it rather than
letting the dead branch pass.

---

### verifier-05 — OBSERVATION

**Where.** §21.7 `[R-ERR-01]`, second paragraph; §21.1's completeness
clause.

**Quoted.**

> "A second set of obligations is omitted from the register because a
> single file exhibits no witness of their violation. Committed-prefix
> immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`)
> are properties of a file's history, which §9.7 does not reconstruct; the
> ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` … ; `[R-CNT-13]`'s
> prohibition on an MU = 0 record encoding file offsets in its own payload
> is opaque by construction; `[R-CNT-18]`'s prohibition on a sub-record
> containing records … ; §20.3 step 4's bar on a declaration change … ;
> §20.5's four obligations on a compacted file's trailer … ; and
> `[R-ENC-06]`'s fixed field widths are not a state a file can be in"

**The problem.** This is an enumeration with a closing "and", and §21.1
leans on it: "Its **completeness is normative** — a *detectable*
file-conformance violation this specification names and the register omits
is a defect in this document, detectability being the gate `[R-CNF-07]`
already applies **and §21.7 the account, by class, of what fails it**."
So §21.7 is the document's own inventory of what falls outside the
register, and a reader auditing the register's completeness works the list
backwards: anything not here should be detectable and should have a row.

I derived the members from the rule the list is about — writer obligations
this specification states whose violation a single file cannot witness —
and found at least four that are not named:

- **`[R-LIF-02]` steps 4 and 6, the durability barriers.** No file
  exhibits whether `fdatasync` was called. §20.2 and §20.5 both stress
  them ("both barriers, not one"), and §9.2's own Note concedes only that
  weak barriers degrade detection, not that a missing barrier leaves a
  witness.
- **`[R-WRT-05]`'s byte-identical re-emission.** Detecting a re-encoded
  record requires the prior generation's directory, which §9.7 does not
  reconstruct. Its Rationale even says "byte-identity makes preservation
  testable — the records of adjacent generations differ exactly by those
  modified, added, or dropped" — *adjacent generations*, i.e. two files.
- **`[R-WRT-08]`'s bar on re-encoding an unimplemented record type**, for
  the same reason.
- **§20.4's drop rules** ("An appender MUST NOT drop it except in a commit
  that *independently* changes the scope the record attaches to"), which
  compare two generations' record multisets.

All four fall inside the *class* the paragraph names, so a reader who
treats "by class" as governing is fine. A reader who treats the
enumeration as closed — which the closing "and" invites, and which §21.1's
normative completeness makes worth doing — concludes these four must be
detectable, looks for their rows, finds none, and reports a register
defect that is not one.

**Which I picked.** The class governs; the enumeration is illustrative. I
implemented no checks for any of the four and reported nothing about them,
consistent with §21.7's "nothing about the file is left undetermined and
the verdict is unaffected".

**Cost to an implementer without this.** Wasted audit effort, and a
spurious defect report against §21.1's completeness claim. No verdict
changes.

**Byte-level?** No. Nothing here reaches bytes, verdicts, or the register's
rows; it reaches whether an implementer trusts the register's completeness
clause.

---

## 10. Places I had to guess that did not become findings

Recorded because the charter asks for them, and because the next round may
disagree with my calls.

1. **Is a resource decline a "scope-level rejection" for §5.2's partial
   rule?** §5.2's causes are given as "whether because a scope-level
   rejection ends that scope's enumeration … or because the verifier
   elected … to stop at the first violation", and a resource decline
   (`[R-ERR-04]`) is neither. I read the governing clause as "Where the
   walk … does not enumerate every region's claimants … MUST report the
   total as partial", with the two causes illustrative, and reported
   partial. The alternative reading gives an exact total for a walk that
   demonstrably skipped a layer, which contradicts "tightening to the exact
   total when the walk completes".

2. **Must a verifier that does not stop early report a rejected layer's
   tile scopes as unexamined?** §2.3 attaches *unexamined* only to the
   stop-at-first-violation case, but §5.2 mandates that a rejected layer's
   claimants leave the walk regardless. I report them. Costs a report line.

3. **Does a layer sub-record of an unimplemented MU = 1 type make the
   verdict cannot-establish?** §2.3's ground reads generally ("a record")
   with a pointer to §21.6, whose worked case is the *top-level* one, and
   §21.6 stresses that the top-level qualifier "is load-bearing". I read
   the ground as general — §7.2's reason (an MU = 1 type may carry
   references this specification does not define, so the coverage partition
   cannot be established) applies identically to a sub-record — and report
   cannot-establish plus a partial slack total, on a file that is
   conforming. That combination is unusual enough that I checked it twice.

4. **`[R-MTA-09]`'s "the bound above" for a verifier** — size bound only,
   or the frame's declared window too? §21.5's preamble names both
   ("declines the decode on the size bound or on the frame's declared
   window"), and either way §2.3's general test reaches the same verdict,
   so the readings converge. Not a finding.

5. **Slack accounting when claimants overlap.** I compute the slack total
   as |[0,F) minus the union of claimants|, not as F minus the sum of
   claimant lengths, which would double-subtract and can go negative.
   §5.2's "F less the bytes claimed by the claimants" reads as set
   measure, and §9.7's "Bytes the walk does not reach are slack: the
   verifier sums them" is unambiguous for a complete walk. I am confident,
   but a naive implementation summing lengths gets a different number on
   any overlapping file.

## 11. Things I expected to be wrong and were not

Recorded so a later round does not re-spend the effort.

- Every CRC constant reproduces (§5.1 above), including the two in §7.4's
  worked layer record and the all-sentinel segment constant.
- The register's five counts and 277 instances are mechanically correct.
- §15.3's "six structural rows", §20.5's "other seven spaces", §22.3's
  "four residues", and §21.2's "four rows" all check out as counts.
- §20.3 step 4's shrink/grow tense is now consistent everywhere I could
  test it: the bar quantifies over "any tile that layer stores **in the
  generation this commit supersedes**", the permission for re-declaration
  quantifies the same way, and §11.1's Rationale, §21.7's
  unwitnessed-there paragraph and §23.1's two-case dichotomy all agree with
  it. In particular the "superseding does not rescue" answer is stated
  twice and I could not construct a case the two statements answer
  differently. Growth can never add a padding position to a
  previously-stored tile (raising Eᵢ only converts padding to real, and
  any tile with new padding is a newly addressed tile), which is why the
  growth permission is safe; the document supplies that reasoning rather
  than leaving it to me.
- `[R-COD-07]`'s lz4 cap and §21.9's tile-size guarantee are both
  quantified over *addressed* tiles, and both say so, and §17.2's Note
  correctly contrasts them with `[R-ENC-04]`'s unquantified overflow rule.
- F33's boundary claim (that a claimant reaching the front block or the
  trailer is caught by the bounds rows instead) survived every path I
  tried to construct against it.
- `file_id`'s absence from F2's instance list is correct, not an omission.

## 12. Confidence

**Medium-high.** I could build the verifier end to end from this document:
the certification procedure, the walk, the checksum inventory, the
decoded-content obligations and the four-generation trace all closed
without a guess that changes a verdict. The one place the document left me
without an answer is what a partial slack total counts after a file-scope
rejection, and that costs a diagnostic number rather than a verdict or a
byte. I found nothing this round that forks the emittable set or a
reader's accept/reject.
