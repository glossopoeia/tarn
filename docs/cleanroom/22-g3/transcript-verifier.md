# Cleanroom round 22 — Verifier implementer, working transcript

## 0. Access and disclosure

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,394 lines), read end to end in five passes. I opened no other file in the
repository — no `docs/`, no ADRs, no `PLAN.md`, no `AGENTS.md`, no
`conformance/`, no `spec/registry.json`, no git history. I ran no web search or
fetch. I ran `wc`, `sed -n` and `grep` against that one file only, and Python
scripts I wrote myself in a scratch directory (`crc.py`, `appA.py`, `build.py`,
`verify.py`, `adversarial.py`, `trace.py`, `count.py`), which read no repository
file other than `tarn.md` (only `count.py` reads it, to tokenize the register
tables). I did not read or list the output directory.

Context I did not ask for **did** appear before I began: a project instruction
file pointing at `AGENTS.md`, and an index of the maintainer's memory notes with
titles referring to working cadence, a naming constraint, prior workflow
failures, and the relationship of §21 to a vector corpus. I did not open any of
the files it named and I have not used its contents as evidence about the
specification. I name its appearance here because the brief requires it; I do
not repeat what it said.

---

## 1. Constants I could reproduce locally

The charter asks which checksum constants I reproduced and which I could not. I
implemented CRC-32C from §4.5's parameters alone (Castagnoli polynomial
`0x1EDC6F41`, reflected in and out, init `0xFFFFFFFF`, final XOR `0xFFFFFFFF`),
i.e. a table built from the reflected polynomial `0x82F63B78`, and checked it
against §4.5's own check vector before trusting it.

| Constant | Where stated | Computed | Match |
|---|---|---|---|
| CRC-32C(`"123456789"`) | §4.5, App. B | `0xE3069283` | yes |
| CRC-32C(zero bytes) | §4.5, App. B | `0x00000000` | yes |
| CRC-32C of a full all-sentinel segment (2¹⁶ × `FF×16 00×4`) | §15.4 `[R-IDX-05]`, App. B | `0xEECB3BB2` | yes |
| §7.4's example: segment CRC over 4 sentinel entries (80 bytes) | §7.4 | `0x80A34955`, stored `55 49 A3 80` | yes |
| §7.4's example: `crc_of_crc_array` over `55 49 A3 80` | §7.4 | `0xC4EE982E`, stored `2E 98 EE C4` | yes |
| Appendix A's trailer CRC over trailer bytes [0,60) | App. A | `0xE00938D2`, stored `D2 38 09 E0` | yes |
| Appendix A's directory CRC at [16,20) | App. A | `0x00000000` | yes |

**Every checksum constant the document states is one I could compute locally, and
every one reproduced.** There is no checksum constant in this document I was
unable to reproduce.

I also re-derived every worked numeric example that a verifier depends on, since
a verifier's arithmetic *is* the document's arithmetic:

- §7.4's layer-record payload: 81 bytes. Name 4 + nine scalars 34 (=1+2+2+2+8+8+8+1+2)
  + one dimension entry 18 + one channel entry 12 + trailing fixed 13 = 81. Offsets
  in the annotated dump all land where the packed field order puts them. Extent
  length `4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84`. Correct.
- §14.2: interleaved T=(2,3), P=6, a(uint8)+b(uint16) ⇒ Q=3, decoded size 18,
  ordinal 5 at [15,18). Planar b: 12 bytes, ordinal 5 at [10,12). t(float32)+m(bool)
  ⇒ Q=5, size 30, ordinal 5 at [25,30). All correct.
- §14.3: planar bool T=(2,5), P=10 ⇒ 2 bytes; alternating from true gives byte 0
  = `0x55`; values 8–9 = (true,false) give bit0=1, bit1=0 ⇒ `0x01`; with fill true
  the six pad bits set ⇒ `0xFD`. Correct.
- §14.5: extents (5,5), tiles (4,4) ⇒ grid 2×2; edge tile (1,1) covers 4–7 on both
  axes: 16 positions, 1 real, 15 padding; uint16 ⇒ 32 bytes. Correct.
- §15.4: entry_count 1,000,000 ⇒ 16 segments (15 full + 16,960), 64-byte CRC array,
  region 20,000,064 bytes; tile 999,999 at segment-relative 20×16,959 = 339,180;
  segment 15 = [19,660,800, 20,000,000) (339,200 bytes ≈ 339 KB); one full segment
  = 65,536×20 = 1,310,720 = 1.25 MiB. All correct.
- §11.4: grid (4,8); (300,700) ⇒ tile (1,2), s = 10; in-tile (44,188) ⇒ 44·256+188
  = 11,452; planar c=2 ⇒ 2·32+10 = 74; its entry at region [1480,1500); channel 3's
  entries are ordinals 96–127. All correct.
- §21.9's note: 2³² tiles ⇒ 65,536 segments × 4 = 256 KiB CRC array; 2³⁶ ⇒ 4 MiB.
  Correct. §17.2's lz4 cap `0x7E000000` = 2,113,929,216.
- §17.2's note on zstd window derivations: RFC 8878's `Window_Descriptor` bottoms
  out at `1 << 10` = 1 KiB, so a sub-1-KiB tile is encodable only as a
  single-segment frame. Consistent with the note.

I also tokenized §21.2–§21.5 mechanically and counted rows and semicolon-separated
instances, treating a cell reading `—` as one instance per §21.1:

```
F: 36 conditions,  58 instances
L: 49 conditions, 116 instances
T: 26 conditions,  55 instances
R: 10 conditions,  44 instances
   121 conditions, 273 instances
```

§21.8 states "121 conditions over 273 instances". **The register's own arithmetic
is exact.** That matters for finding 3 below: the count is right *given the cells
as written*, so the question there is about one cell's content, not about the sum.

---

## 2. The certification procedure, as an ordered algorithm

I implemented this and ran it (`verify.py`). Stated as the algorithm a verifier
actually executes, with the verdict vocabulary attached at each point.

**Verdict vocabulary** (§2.3, `[R-CNF-11]`): *conforming*, *nonconforming*,
*cannot establish*. Three report-only channels that are **not** verdicts:
*unexamined* (scopes skipped after an early stop), the per-requirement
"unable to check" report, and the slack total (`[R-CNT-21]`).

**Verdict availability.** These are the rules I had to assemble from §2.3,
`[R-CNF-12]`, `[R-COD-11]`, `[R-MTA-09]`, `[R-MTA-10]`, `[R-ERR-04]` and §21.7:

- *nonconforming* — available and **mandatory** the moment any violation is
  established, "however many requirements it was unable to check". It dominates
  everything.
- *cannot establish* — available **only** to a traversal that established no
  violation, and only on a **capability or resource** ground. The grounds §2.3
  names, with "as when" marking the list as open: an unimplemented format major;
  a record with MU = 1 of a type it does not implement; inability to execute a
  codec or filter (`[R-COD-11]`); declining a layer's or tile's decode on
  resource grounds (`[R-ERR-04]`, and thereby being unable to check `[R-SER-05]`
  / `[R-SER-08]`); declining to decode a user-metadata document
  (`[R-MTA-09]`, on either the size bound or the frame's declared window).
- *conforming* — available only when the traversal established no violation and
  had no unchecked requirement. **Explicitly not** a cannot-establish ground, and
  therefore no bar: a user-metadata record at an **unassigned** encoding
  (`[R-MTA-10]`, §21.6). Note the asymmetry I had to read carefully — encoding 0
  and reserved 3–0x7F are *violations* (R1), only the experimental range ≥ 0x80 is
  the non-violation.
- **What bars certification**: any established violation; any unchecked
  requirement on a capability/resource ground. What does *not* bar it: a SHOULD
  deviation (`[R-CNF-12]` — reported as an advisory, and not hunted for); an
  unassigned metadata encoding; an ignore-lane flag bit; an unrecognized `tarn.`
  key; a standardized key out of scope or off-shape (`[R-MTA-07]`); an
  experimental-range MU = 0 record.

**The ordered algorithm.**

```
C0. Residency check (§6.1 [R-CNT-04], §19.1 step 1).
    A verifier holds no deferral exemption (§2.3, F6's condition text): it MUST
    compare bytes [0,16) to the 16-byte constant. Mismatch -> F6 (or F1 if
    byte-reversed), reject-file, VIOLATION. Claim [0,16).
C1. Size floor (§5.1 [R-CNT-27]). F < 128 -> F5.
C2. Trailer, in §6.2's fixed order — this order is normative and I obeyed it:
    (a) magic at [F-64, F-56)          -> F8, reject-file, HALT the traversal
    (b) trailer CRC over [0,60)        -> F14, reject-file, HALT
    (c) version gate                   -> version_major 0 -> F18 (violation);
                                          any other unimplemented major ->
                                          CANNOT ESTABLISH, halt, and note that
                                          F8/F14/F1/F6 still reach such a file
                                          because their fields are fixed across
                                          majors ([R-CNT-24], §21.2 preamble)
    (d) only now, the remaining gates, all of which must pass before acting on
        the fields: flags incompat lane (F19); committed_file_length == transport
        size (F17) and 64-multiple (F13); dir_offset >= 16 (F9); dir_length >= 4
        (F16); dir_offset+dir_length <= F-64 (F10); generation in [1, 2^63-1]
        (F11, F2); file_id != 0 (F12); reserved [56,60) zero (F15); and the
        domain/overflow rows F2/F3.
    Claim [F-64, F).
    NOTE: if (a)-(c) fail there is no F and no live state, so per §5.2 the slack
    total is NOT OWED AT ALL — "not a partial total but the absence of one".
    I made my implementation emit no slack line in that case.
C3. Directory region (§7.1 [R-CNT-11]). Verify the terminal CRC over the
    preceding dir_length-4 bytes BEFORE any other use -> F20, reject-file, halt.
    Claim [dir_offset, dir_offset+dir_length).
C4. Top-level record walk (§7.2, §19.1 step 4). Parse to zero residue -> F29.
    Per record: type 0 -> F24; reserved range 0x0003-0x7FFF -> F36 (and F35 if
    MU=1); experimental >= 0x8000 with MU=1 and a type it does not implement ->
    CANNOT-ESTABLISH ground; MU=1/PE=0 -> F25 (non-layer) or L46 (layer);
    reserved flag bits 2-15 -> F26/L47; registered type's stored MU/PE against
    §7.3 -> F28/L49; extent slot -> F30/F31/F32 (non-layer) or L15/L16/L17;
    user-metadata framing -> F21 (0,0), F22 (<5), F23 (inline_length != 1);
    multiplicity -> F34. Then the layer-name namespace over raw name bytes,
    uniqueness decided first and independently of well-formedness -> F4.
C5. Per layer, §19.3's full validation ([R-RDR-03]) — all of it decidable from
    the resident directory and F, with no fetch: slot validity, the §7.4
    constraint set, exact parse + sub-record walk + sub-record multiplicity,
    dimension/channel name rules, field widths and u64 domain, the value sets of
    §11.4/§12.2/§14.1/§15.1/§17.2/§17.3, bool fill (L35), the lz4 declaration cap
    (L44), the geometry floor and its arithmetic, the 2^63-1 ceiling on every
    derived product (L2), and the index cross-checks (L21, L22).
C6. Per layer, the index chain (§8.2, §15.4): crc_of_crc_array over the stored
    segment CRC array (L37), then every segment CRC (L38). Both reject-layer.
    A verifier must verify EVERY segment, not just those covering tiles it wants;
    §2.3's "every file-level requirement" leaves it no per-tile laziness.
C7. Per entry, §15.3's classification (T6-T12), then per stored tile the entry
    crc (T1), then DECODE (§9.7: "A verifier decodes every stored tile"), then
    the codec rows T14/T17-T25 and the decoded-size row T3.
C8. Decoded-content obligations: T4 (every padding position carries fill),
    T5 (every pad bit carries the fill bit), T2 (every interleaved bool byte at
    a real position is 0x00 or 0x01). T26 has no procedure of its own; it is
    whatever T2/T4 catch.
C9. Verifier-only structural rows: F7 (a structure in the pre-trailer gap),
    F33/L18 (overlap), L40 (alignment), L41/L42 (slab), F27/L48 (metadata
    member ordering).
C10. Coverage walk (§9.7 [R-LIF-08]) — disjointness, the [16, F-64) bound,
    checksums where §8.1 states one, and the slack total.
C11. Verdict: nonconforming if anything in C0-C10 established a violation;
    else cannot establish if any requirement went unchecked on a capability or
    resource ground; else conforming. Plus: every unchecked requirement named
    with its ground, whatever the verdict; every unexamined scope named if the
    verifier stopped early.
```

Running this on Appendix A's 128-byte file returns *conforming* with slack 44
(the pre-trailer pad), which is the answer §5.1's example gives.

---

## 3. The concrete file, built byte by byte

I needed a file rich enough to exercise the whole charter, so I built one rather
than describing one. Generation 1:

**Layer `a`** — rank 1, dim `x`, E=5, T=2 ⇒ G = ⌈5/2⌉ = 3, N = 3, P = 2.
Interleaved, C = 1 channel `v` uint16 (element size 2), fill `0xABCD`. Codec 1,
filter 1, no alignment, no slab. entry_count 3, Q = 2, decoded size = P·Q = 4.
`G·T = 6 > E = 5`, so ordinal 2 (covering x ∈ [4,6)) carries one real position and
one **padding position** at x = 5. Tiles 0 and 2 stored, tile 1 sentinel.
Tile 0 = `01 00 02 00`; tile 2 = `34 12 CD AB` — the second value is the fill
bytes, as `[R-SER-05]` requires.
Index region: 3×20 + ⌈3/2¹⁶⌉×4 = 64 bytes, matching `[R-CNT-17]`.

**Layer `b`** — rank 1, dim `y`, E=4, T=2 ⇒ G = 2, N = 2, P = 2. **Planar**,
C = 2: `m` bool (fill `0x00`), `n` uint8 (fill `0x00`). Addressed tiles = C·N = 4.
Slab S = 2, A_slab = 64, no per-tile alignment (`[R-CNT-16]` makes them exclusive).
Bool plane decoded size = ⌈P/8⌉ = 1; uint8 plane = P·B = 2. `G·T = 4 = E`, so no
padding positions — but P mod 8 = 2, so **six pad bits** in each bool plane's only
byte, which `[R-SER-05]` fixes to the fill bit (false = 0).
Disk ordinals: `m` at 0,1 (block [0,2)); `n` at 2,3 (block [2,4)). All four stored.
Index region 4×20 + 4 = 84.

Plus a file-scope user-metadata record (encoding 1, document
`{"tarn.title":"demo"}`, extent = 21 doc bytes + 4 CRC = 25) and a **top-level
record of experimental type 0x8000, MU = 0, PE = 0**, with an 8-byte opaque
extent — conforming per §21.6, and the case I need in §5 below.

Placement, and the resulting claimant map (computed, not asserted):

```
  front block            [    0,   16)      16
  layer a tile 0         [   16,   20)       4
  layer a tile 2         [   20,   24)       4
  layer a index          [   24,   88)      64
  <<slack 40 — A_slab forces the next stored tile to 128>>
  layer b tile ord 0     [  128,  129)       1
  layer b tile ord 1     [  129,  130)       1
  <<slack 62 — block 1's run must start 64-aligned>>
  layer b tile ord 2     [  192,  194)       2
  layer b tile ord 3     [  194,  196)       2
  layer b index          [  196,  280)      84
  user-metadata extent   [  280,  305)      25
  ancillary extent       [  305,  313)       8
  directory              [  313,  567)     254
  <<slack 9 — pre-trailer pad>>
  trailer                [  576,  640)      64

  claimed 529 + slack 111 = 640 = F.   F mod 64 = 0.
```

My verifier returns *conforming* on it.

Two placement facts I had to derive rather than read off:

1. `[R-CNT-05]` ("no structure lies between its end and the trailer")
   effectively forces **the directory to be the last structure in the file**.
   Appendix A's minimal file puts the directory at offset 16 and is fine only
   because it has no other structures. I placed mine accordingly.
2. The layer's tile-index region enters the walk **once**, as the layer record's
   extent — §9.7 says so explicitly. A verifier that claimed both "the layer
   record's extent" and "the tile-index region" separately would report a
   spurious self-overlap. This is a trap the document closes; I hit it in my
   first draft and §9.7 corrected me.

---

## 4. The coverage walk, complete

**Partition of the live state.** Every byte of the live committed state belongs
to exactly one of: the front signature block, or a structure — stored-tile
extent, record extent (whatever the record's type), the directory, the trailer
(`[R-CNT-02]`). My 13 claimants above are pairwise disjoint and each lies in
[16, F−64) except the front block and the trailer, which §9.7 claims separately.

**Slack total: 111 bytes**, in three runs (40 + 62 + 9). Two of them exist
*because layer b declares a slab*: A_slab = 64 forces each run's first stored tile
to a 64-boundary, and the bytes before it are slack that no rule constrains. This
is the case §16's `[R-SLB-05]` describes — "A writer that scatters structures
wastes space rather than violating a rule, and the verifier's slack total, where
its walk completes, is what surfaces the waste."

**Can any byte be neither certified nor counted?** No — and the document says why
rather than leaving me to work it out. §5.2's Note: the live committed state is
*defined* as the front block plus what a complete walk reaches, and `[R-LIF-08]`
makes every byte the walk misses slack, "so 'belongs to no class' describes
nothing, and a register row for it would be a row no file could exhibit." So the
partition is total by construction and **only disjointness is testable**. That is
the honest answer to the charter's question, and it is the document's own.

**But "claimed" is not the same as "certified", and the three-way split matters.**
Working my own file:

| Class | Bytes in my file | What holds it |
|---|---|---|
| Claimed **and** checksum-covered **and** content-constrained | front 16 (byte equality), trailer 64, directory 254, both index regions 148, four stored tiles 12 (entry crc + §14 content rules) | §8.1's map + §14 |
| Claimed **and** checksum-covered, **no** content rule | user-metadata extent 25 under an *assigned* encoding is content-constrained; under an **unassigned** one it would be CRC-covered and content-free (`[R-MTA-10]`, §22.3) | §8.1 row 6 |
| Claimed, **no** checksum, **no** content rule | the 8-byte experimental-type extent | §8.1's last row; §22.3 |
| Counted, unconstrained | 111 bytes of slack | §5.2 `[R-CNT-21]` |

So on this 640-byte file, **8 bytes sit inside the certificate without ever being
inspected**, and 111 are counted without being inspected. The document is
deliberate about this: §22.3 says a certificate "covers those bytes uninspected —
which is why `[R-MTA-10]` makes the verifier's report name each such record".
Note the asymmetry I checked and confirmed: `[R-MTA-10]` obliges the verifier to
**name** each unassigned-*encoding* user-metadata record (owning scope, encoding
value, stored extent length), but there is **no** parallel obligation to name an
unassigned-*type* record whose extent is covered by nothing at all — the strictly
weaker case. §22.3 notes the exposure; no rule turns it into a report line. I did
not raise this as a finding because nothing is left undetermined by it: the
verifier's verdict and every byte are fixed either way, and a report line is
implementation technique under §2.4's Note. I record it as an observed
asymmetry, not a defect.

---

## 5. The coverage walk, incomplete

Two runs, on generation 4 of the trace in §9 (F = 1728, claimed 477, true slack
1251).

**(a) A walk stopped by a scope-level rejection the walk itself established.**
I moved layer b's block-1 run so its first stored tile sits at 200 rather than
192. 200 mod 64 = 8 ⇒ **L42**, verifier, certification, reject-layer. Per §5.2,
layer b's claimants "are not enumerated", and because this rejection is one the
walk itself established, "the claimants it had already enumerated are discarded
with the layer". Layer b's claimants total 1+1+2+2+84 = 90.

```
enumerated = 477 − 90 = 387
partial total = F − 387 = 1728 − 387 = 1341
true slack    = 1251
```

1341 > 1251 — an upper bound, over by exactly layer b's 90 live bytes, which is
what `[R-CNT-21]` promises ("an upper bound on the file's true slack, never an
under-count"). Verdict *nonconforming*; report names L42 and layer b as what
stopped the walk.

**(b) A walk stopped by the verifier's own election.** A verifier that stops at
the first violation under `[R-CNF-11]` and meets F26 (a reserved flag bit on a
top-level record) while parsing the directory has enumerated the front block, the
directory and the trailer: 16 + 230 + 64 = 310.

```
partial total = 1728 − 310 = 1418   (upper bound; true slack 1251)
```

Plus every scope it did not examine, reported as *unexamined* — which §2.3 is
careful to say "is not a finding that the scope is clean", and is neither a
verdict nor *cannot establish*.

**Where I had to guess.** Reading (b) forced the question I could not settle from
the text, and it is finding 2 below: a **file**-scope rejection that does not
impede the walk at all. If the verifier does *not* elect to stop — F27 (unsorted
user-metadata members), F28, F36, F25/F26, F33 — the walk demonstrably runs to
completion and the exact total is in hand. §5.2 says a partial total is owed
"because a scope-level rejection ends that scope's enumeration"; the rejected
scope here is the file. §9.7 says "a scope-level rejection **blocks**
enumeration", which is causal and would not fire. The two readings give different
report lines for the same file, and §5.2's own follow-on obligation — "a verifier
reporting one MUST say which scope or violation stopped the walk" — is
undischargeable under the reading that forces partiality, because nothing stopped
it. I picked the causal reading (exact total, F27 reported as a violation) and
flag the ambiguity.

**Two cases that do *not* make the walk incomplete**, which I checked because I
expected them to and they do not:

- An entry §15.3 classifies reject-tile on a **structural** ground (T6–T12).
  §9.7: "the walk passes over it, and the bytes it nominally addresses fall to
  slack". The walk stays complete and the total stays exact even though a
  violation was established. I confirmed the corollary in `[R-SLB-03]`: such an
  entry is likewise transparent to run continuity.
- An entry whose **only** defect is that its stored bytes fail its crc (T1).
  §15.3: "the defect lies in the bytes it addresses, not in the entry, so its
  extent stands and it keeps its place in the *verifier* rows, in run continuity,
  and in the coverage walk." Extent claimed, total exact, verdict nonconforming.

That pair is the sharpest bit of drafting in the section and I could implement it
without guessing.

---

## 6. Extent overlap, alignment, and slab, on concrete adversarial layouts

**Overlap.** Classified by `[R-CNT-13]` on real byte ranges from my file:

| Adversarial pair | Overlap | Outcome |
|---|---|---|
| layer a tile 0 [16,20) vs layer a index [18,82) | 2 B | intra-layer ⇒ **L18 reject-layer** |
| layer a tile 0 [16,20) vs layer b tile 2 [18,20) | 2 B | across layers ⇒ **F33 reject-file** |
| layer a tile 0 [16,20) vs file-scope UM extent [19,44) | 1 B | layer vs other scope ⇒ **F33 reject-file** |
| UM extent [280,305) vs ancillary extent [300,308) | 5 B | neither belongs to a layer ⇒ **F33 reject-file** |
| layer a index [24,88) vs directory [80,334) | 8 B | layer vs other scope ⇒ **F33 reject-file** |
| layer a sub-record extent vs layer a tile | 3 B | intra-layer ⇒ **L18 reject-layer** |

All six resolve without guessing. The one that took a second reading is the
fourth: `[R-CNT-13]`'s third clause ("any overlap between two structures neither
of which belongs to a layer as reject-file") exists precisely for it, and F33's
condition text restates all three. A claimant reaching [0,16) or [F−64,F) is
*not* an overlap row — F33 says so, routing it to the bounds rows F9/F10,
F31/F32, L16/L17, T8/T9, each at its own tier. I checked that this exhausts the
cases: my walk's [16, F−64) containment test and the overlap test between them
leave no byte of the live state unadjudicated.

**A structure in the pre-trailer gap (F7).** My generation-1 directory ends at
567 and the trailer begins at 576, so the gap is [567,576). I relocated the
8-byte ancillary extent to [567,575). Then:

- extent_offset 567 ≥ 16 ⇒ F31 does not fire;
- 567 + 8 = 575 ≤ F − 64 = 576 ⇒ F32 does not fire;
- it overlaps nothing ⇒ F33 does not fire;
- it is not a tile entry ⇒ T8/T9 do not fire.

**Only F7 fires** — verifier, certification, reject-file. A conforming *reader*
opens this file, walks it and reads every tile without a complaint, because
`[R-CNT-05]` explicitly says "readers check neither, their check being the
dir-bounds rule of `[R-CNT-06]`". This is the cleanest demonstration in the
document of why the verifier class exists at all, and I could implement it from
the text alone.

I also checked the neighbouring case: a **superseded** trailer or directory
sitting in a long pre-trailer gap is *slack*, not an F7 structure, because F7
ranges over live claimants only; and a gap longer than `[R-LIF-02]` step 5's pad
is declared not to be a file-conformance violation at all (`[R-CNF-02]`).
Decided, no guess needed.

**Alignment (`[R-SLB-01]`, L40).** Quantified over "every stored tile's offset" —
stored in the live generation, per §3.1's unqualified reading, and `[R-WRT-04]`
step 4 confirms it covers "every one the new state keeps, not only those this
commit adds". With A = 512, offsets 512 and 1024 pass; 16 and 768 are L40. The
tile-**index** region's offset is *not* constrained by A: `[R-SLB-01]` names
stored tiles and nothing else. I checked this deliberately because it is the kind
of thing a naive implementation over-enforces.

**Slab (`[R-SLB-03]`, L41/L42).** My layer b, S = 2, A_slab = 64:

```
block 0 (channel m), run 0 = ordinals 0,1: first offset 128, 128 mod 64 = 0  OK
                                            129 == 128 + 1                  OK
block 1 (channel n), run 0 = ordinals 2,3: first offset 192, 192 mod 64 = 0  OK
                                            194 == 192 + 2                  OK
```

Adversarial variants: moving ordinal 1 to 130 gives 130 ≠ 128+1 ⇒ **L41**
instance "gap"; moving the run's first stored tile to 136 gives 136 mod 64 = 8 ⇒
**L42**. Runs never span channel blocks (`[R-SLB-02]`), so ordinals 1 and 2 are
under no packing relation to each other and the 62-byte gap between them is
lawful slack — the point of `[R-SLB-05]`.

Transparency, which I checked against three entry states because the rule turns
on the distinction:

- a **sentinel** at ordinal 0 ⇒ run 0's first *stored* tile is ordinal 1, and its
  offset alone must be 64-aligned; packing closes over the sentinel;
- an entry §15.3 classifies reject-tile on a **structural** ground ⇒ same
  treatment, explicitly ("the run's stored tiles close over them");
- an entry whose **only** defect is a failed tile crc ⇒ **not** transparent; "its
  offset and length stand, and the packing relation reads them as it does any
  other stored tile's".

That last clause is what keeps L41 decidable from the index entries alone, and I
could implement all three without guessing. `[R-SLB-04]`'s stale-declaration rule
has no row of its own precisely because every file exhibiting one exhibits L41 or
L42 — I confirmed that by trying to construct a counterexample and failing.

---

## 7. Checksum obligations

**Which structures are covered by which checksum** (§8.1, and the chain order of
§8.2):

```
trailer[60,64)          covers trailer[0,60)                   -> F14
directory final 4 bytes covers the raw record sequence         -> F20
crc_of_crc_array (in    covers the segment CRC array           -> L37
  the layer record)
segment CRC array       covers that segment's entry bytes      -> L38
index entry .crc        covers that stored tile's bytes        -> T1
UM extent final 4 bytes covers the encoded document as stored  -> R2
front block             none — byte equality                   -> F1/F6
unassigned-type extent  none at all
```

Chain of trust, strictly ordered: trailer → directory → crc_of_crc_array →
segment CRC array → index segment → index entry → stored tile.

**Is every live structure covered by one? No — and the exceptions are stated
rather than latent.** The two gaps are (i) the front signature block, checked by
equality instead, and (ii) the extent of a record of a type this specification
has not assigned, "in which this specification defines no fields (§4.7) and whose
bytes it leaves opaque (§7.2)". §4.5 adds the third class I had to account for:
the three *terminal* checksum fields — the trailer's, the directory region's, and
a user-metadata extent's — are verified by comparison and covered by no further
checksum, while the three *interior* ones — each segment CRC array, each entry's
crc field, each layer record's crc_of_crc_array — are both compared and covered
by exactly one further checksum. I traced all six and they close: the segment CRC
array is covered by crc_of_crc_array, which lies in the layer record's inline
payload, which lies in the directory region, which is covered by the directory
CRC, which is terminal. No cycles, no orphans.

Two ordering rules constrain the verifier and I obeyed both in `verify.py`:
`[R-ENC-05]` (no allocation, seek or I/O from a file-derived integer before the
covering checksum verifies) and `[R-ENC-10]` (no *acting on* a field before its
checksum verifies, where comparing against a constant is not acting on it — which
is what lets §6.2's magic-then-CRC order be legal at all).

One point where the text left me to reason: §9.7 says "A verifier decodes every
stored tile", full stop, while `[R-CNT-20]`/`[R-ENC-10]` forbid acting on bytes
whose covering checksum failed. I read "every stored tile" as "every stored tile
whose entry crc verifies" and decode nothing else. This costs nothing: a tile
whose crc failed has already established T1, so the verdict is *nonconforming*
either way and no verdict turns on the reading. I record it as a reading I made,
not as a defect.

---

## 8. Decoded-content obligations

**What a verifier must decode.** Every stored tile of every layer it has not
already rejected — §9.7 is explicit that this holds "whatever content obligations
§14 places on the layer", which forecloses the optimization I would otherwise
have written (skip decode where the layer has no padding positions, no pad bits
and no bool channel). The reason is given: T3, T14, T24 and T25 are
file-conformance violations and "a verifier MUST NOT certify past a violation it
has not looked for". It must also decode every user-metadata document under an
**assigned** encoding, because `[R-MTA-09]` makes declining one a
cannot-establish ground.

**What it must compare against.**

| Check | Compared against | Row |
|---|---|---|
| decoded payload length | the declaration-derived decoded size (P·Q, P·Bᶜ, or ⌈P/8⌉) | T3 |
| every padding position's bytes | that channel's **recorded fill**, bit for bit | T4 |
| every pad bit of a packed plane | the plane's channel's **fill bit** | T5 |
| every interleaved bool byte at a real position | 0x00 or 0x01 | T2 |
| stored length under codec 1 | the decoded size | T14 |
| decode consumption | the entry's length, exactly | T24 |
| zstd frame header | magic; one frame, no skippable; dict ID 0; no content checksum; window ≤ decoded size; content size == decoded size if present | T17–T22 |

On my file this is concrete: layer a ordinal 2 must carry `CD AB` at value 1
(T4), and each of layer b's two bool planes must carry zero in bits 2–7 (T5).
Flipping either is caught; flipping a *real* sample value in layer a is not, and
cannot be.

**What it is permitted to skip.** Sample values at real positions, entirely.
§21.7 states it plainly: "this format detects *corruption of structure*, not
*incorrectness of content*", and — the part that matters for the verdict —
"None of these is a requirement a verifier is *unable to check* within the
meaning of `[R-CNF-11]`: no file-level witness exists to check, so nothing about
the file is left undetermined and the verdict is unaffected." That is the
sentence that stops a scrupulous implementer from downgrading every file to
*cannot establish*, and it is doing real work.

It may also skip a document under an **unassigned** encoding — not as a decline,
but because no rule attaches (`[R-MTA-10]`); certification is unaffected and the
record is instead **reported**. And it may decline a decode on resource grounds
only where the quantity exceeds a §21.9 row — which is where finding 1 bites.

Where the verifier is left with nothing to check even though it decoded: a
mis-strided byte-shuffle (T26) in a layer with no padding position, no pad bit
and no bool channel. §21.7 and `[R-COD-10]` both say so; T26's own condition text
says "the check that detects it is T2's or T4's". I confirmed by construction
that my layer b would catch a wrong stride (its pad bits would move) and a
hypothetical padding-free, bool-free single-channel numeric layer would not.

---

## 9. The multi-generation trace

All figures computed (`trace.py`), not asserted. Layer/record sizes from §3.

```
gen 1  create        F=  640  claimed 529  slack  111   verdict: conforming
gen 2  append        F= 1024  claimed 501  slack  523   verdict: conforming
gen 3  update        F= 1344  claimed 501  slack  843   verdict: conforming
gen 4  shrink        F= 1728  claimed 477  slack 1251   verdict: conforming
gen 1' compact       F=  640  claimed 477  slack  163   verdict: conforming
```

**gen 2 — append.** Stores layer a's ordinal 1 (`05 00 CD AB`; x=2 carries 0x0005,
x=3 deliberately carries the fill bytes, for the reason gen 4 needs). `[R-WRT-04]`
step 4: any change to a layer's stored-tile set re-emits that layer's **whole**
index region at a new placement, so a 4-byte payload costs 64 bytes of index.
The commit also **drops** the experimental MU=0/PE=0 ancillary record — licensed
because §20.4's last row permits a drop only "in a commit that *independently*
changes the scope the record attaches to", and this commit changes a layer
record's content (its extent slot moved). Newly slack: old index 64 + dropped
extent 8 + old directory 254 + old trailer 64 = 390, plus 22 of new pad, less the
9 of old pad already counted. Layer b's record is re-emitted **byte-identically**,
extent slot and all (`[R-WRT-05]`), and its index never moves.

**gen 3 — update.** Amends the file-scope user-metadata document. §20.3's example
(c) is explicit that this is *not* the directory-only shape: "its document lives
in an extent, so a new extent is appended and the old one becomes slack". Both
layer records re-emitted byte-identically.

**gen 4 — shrink.** Layer a's extent 5 → 3. G = ⌈3/2⌉ = 2, so entry_count falls to
2, the index region shrinks to 2×20+4 = 44 and is re-emitted, and **ordinal 2
leaves the addressed set** — its 4-byte extent becomes slack, which §20.3 says in
so many words. This is the interesting one, and I worked it carefully because the
bar in step 4 is quantified over *the generation this commit supersedes*:

> "a shrink is permitted exactly where it alters nothing §14 fixes for any tile
> the layer stores in the generation this commit supersedes."

Ordinal 1 **is** stored in generation 3, and the shrink turns its position x = 3
from a real position into a **padding position** — which alters "the set of
padding positions (§11.3) and the content `[R-SER-05]` fixes there". That would
bar the commit, except that step 4 carves out exactly this case: "a new padding
position whose stored byte already holds the fill `[R-SER-05]` fixes — is not
what this bars." I wrote x = 3's stored value as `CD AB` in generation 2 for this
reason, so the shrink is permitted. Had it been any other value, the commit would
be barred — and, crucially, a verifier of the *resulting* file detects it
**without any knowledge of history**, as **T4**: a padding position not carrying
fill, reject-tile. §21.7 confirms the boundary: the bar is witnessed "only where
the affected tiles remain stored *and* the change reaches a byte §14 structurally
constrains", and is unwitnessed where the commit unstores the tile in the same
breath. I could implement the verifier side of this from the text alone; the
updater side required reading the tense of "stores" three times.

Ordinal 2's own de-addressing alters nothing: "a tile the new state does not
address carries no §14 obligation and its extent becomes slack".

**gen 1' — compaction.** Fresh file_id (a new draw, not merely a different
value), generation 1, every stored tile's bytes and every entry crc verbatim,
extent slots re-pointed, both index regions regenerated with new offsets and
recomputed segment CRCs, crc_of_crc_array updated. Verification depth is
`[R-WRT-09]`'s: the open, each retained layer's record and full index chain, and
each relocated extent's checksum including every stored tile's entry crc — and
notably **not** decoded content, which §20.5 says outright.

The compacted file still carries **163 bytes of slack**, not zero, and I want to
be precise about why, because "compaction reclaims slack" reads like it should be
zero. Layer b's slab declaration survives compaction (a compactor preserves
content and "every declared layout invariant" must still hold), so A_slab = 64
still forces each run's first stored tile to a 64-boundary; plus the pre-trailer
pad. §20.5's own figure shows a `pad` in the output. So the correct statement is
that compaction carries none of the *input's* slack, not that its output has
none. That is consistent, and I record it as something an implementer will get
wrong on a first reading of the sentence "so slack is never carried."

Verification after each step returns *conforming*; the slack total is the number
that tells the operator when to run gen 1' (§20.5, §22.3), and 1251/1728 = 72%
waste at generation 4 is exactly the signal §9.7 is built to produce.

---

## 10. Findings

### verifier-01 — AMBIGUITY — §21.9 `[R-ERR-03]`/`[R-ERR-04]`, `[R-CNF-03]`

**§21.9's per-instance clause does not decide whether an addressed-but-unstored
tile is a tile "a file actually contains", and the two readings differ on whether
a conforming reader may refuse the file.**

> "The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains, and a
> file containing none of a kind does not exceed that row, whatever its
> declarations would derive — a layer addressing no tile (§11.2) has no tile
> whose decoded size the table can bound, exactly as `[R-COD-07]`'s cap is
> quantified over a layer's *addressed* tiles."

The gloss decides the **empty** case — a layer addressing no tile — and nothing
else. It leaves undecided the case one step in: a layer that **addresses** tiles
and **stores** none.

*Reading A (addressed tiles).* "exactly as `[R-COD-07]`'s cap is quantified over
a layer's *addressed* tiles" equates the two quantifiers, and `[R-COD-07]` is
unambiguously over addressed tiles. Every addressed tile has a decoded size,
whether or not it is stored, because §14.2/§14.3 make decoded size "a function of
the layer's declarations alone".

*Reading B (tiles present in the bytes).* The operative phrase is "a file
actually contains", and a sentinel tile occupies no bytes — §3.1: "An addressed
tile that is not stored reads as fill", §15.2: it "contributes fill to the
reference array". Two of the three rows this sentence governs **require** reading
B: a "user-metadata document" and a "compressed frame" exist only if the file
stores one. An implementer who reads one phrase uniformly across the three rows
it governs lands on B. Reading B is further supported by the very distinction the
sentence draws: an unstored tile's decoded size is *purely declaration-derived*,
and the sentence's own architecture puts declaration-derived quantities in the
other group ("The first five range over declarations").

**The fork.** Construct a conforming file with layer `big`: rank 2, extents (1,1),
tile extents (16384,16384), interleaved, one float32 channel, codec 1, filter 1.
Then G = (1,1), N = 1, P = 268,435,456, Q = 4, decoded size P·Q = 1 GiB. entry_count
= 1 and that entry is the sentinel. `[R-COD-07]`'s cap does not apply (codec 1);
`[R-ENC-04]` is satisfied (1 GiB < 2⁶³−1); every other declaration is in range.

- Under A, the file exceeds §21.9's "decoded size of one tile" row (256 MiB), so
  `[R-ERR-04]` licenses a reader to "decline it — at the whole file, or at the
  narrowest scope whose declarations exceed what it can serve".
- Under B, the file contains no tile, exceeds no row, and `[R-ERR-04]`'s next
  sentence bites: "Software that declines **on that ground** a file whose every
  quantity lies within the table is not a conforming reader (`[R-CNF-03]`)."

So implementation **Tarnix** (256 MiB tile ceiling) refuses these bytes and
reports a resource limit; implementation **Tarnyx** accepts them and serves the
single real coordinate (0,0) as fill. Under A both are conforming readers; under B
Tarnix is not. The set of byte sequences a conforming reader **must accept**
differs between the readings, which is `[R-CNF-03]`'s MUST. Derivatively, a
verifier exercising `[R-ERR-04]`'s whole-file decline reports *cannot establish*
under A and must report *conforming* under B — a different verdict on the same
bytes.

**I picked A**, because "exactly as … is quantified over a layer's *addressed*
tiles" is the only explicit quantifier in the sentence and I will not override an
explicit one with an inference from "contains". But an implementer who picks B is
not misreading English, and the cost of getting it wrong is a reader that refuses
files it is obliged to serve — precisely the failure `[R-ERR-04]`'s last sentence
exists to prevent, since it directs such a refusal to be reported as a resource
limit and "a reader that reports 'too large' as 'corrupt' invites the deletion of
intact data."

The repair is one clause: say "the tiles a layer **addresses**" (or "stores") in
place of "the tiles … a file actually contains", and give the other two rows
their own phrase.

**Byte-level: yes.**

### verifier-02 — AMBIGUITY — §5.2 `[R-CNT-21]` against §9.7 `[R-LIF-08]`

**Whether a file-scope rejection that does not impede the walk forces the slack
total to be reported as partial is undecided, and the two readings produce
different reports for the same file.**

§5.2:

> "Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection ends that scope's enumeration (a rejected
> layer's claimants are not enumerated, whether or not the rejection impeded
> reading them …), or because the verifier elected under `[R-CNF-11]` to stop at
> the first violation — the verifier MUST report the total as partial."

§9.7:

> "Where the walk does not complete — a scope-level rejection blocks enumeration,
> or the verifier stops at the first violation (`[R-CNF-11]`) — the sum is
> reported as partial"

The parenthetical stipulates the layer case: a layer rejection ends that layer's
enumeration *whether or not it impeded reading*. Tile scope is carved out
explicitly at the end of §9.7 ("does not make the walk incomplete"). **File scope
is stipulated neither way**, and several file-scope rows impede nothing at all:
F25, F26, F27, F28, F33 and F36 are all verifier-detected at certification, and a
verifier that does not elect to stop walks every byte after finding any of them.

*Reading 1 (stipulative, tracking §5.2's phrasing "ends that scope's
enumeration"):* the rejected scope is the file, so the enumeration ends and the
total is partial. On my generation-4 file with an unsorted user-metadata document
(F27) this yields "nonconforming; slack ≤ 1341" naming F27 as what stopped the
walk — which is false, since the walk completed and the exact total 1251 is in
hand.

*Reading 2 (causal, tracking §9.7's phrasing "blocks enumeration"):* only a
rejection that actually blocks enumeration — F10 or F20, say, where there is no
record sequence to walk — makes the total partial. F27 yields "nonconforming;
slack 1251".

**I picked reading 2**, on two textual grounds: §9.7's "blocks" is causal where
§5.2's "ends" is not, and §5.2's own follow-on — "a verifier reporting one MUST
say which scope or violation stopped the walk" — is undischargeable under
reading 1, since nothing stopped it. But the stipulative reading is available,
and it is the one a careful implementer arrives at by analogy with the layer
parenthetical, whose whole point is that a rejection ends enumeration *even when
it impedes nothing*.

The cost of getting it wrong is not a verdict — both readings report
*nonconforming* — it is the number §22.3 makes operationally load-bearing: "a
verifier that stopped early reports it only as partial (`[R-CNT-21]`), so the
distinguishing figure comes from a walk that completes." Under reading 1 an
exact figure is thrown away and replaced with a bound, for a class of violations
that costs the walk nothing. An operator reading two verifiers' reports for the
same file gets 1251 from one and "≤ 1341" from the other.

**Byte-level: no.** No byte changes, and no accept/reject verdict changes — both
readings give *nonconforming*. The divergence is confined to a report line, and
§5.2 itself classes a partial total as "a fact about that run and not about the
file's live state". I grade it as a report-fidelity defect and decline to reach
for byte-level.

### verifier-03 — OBSERVATION — §18.2 `[R-MTA-09]`, §21.5 R3, §21.1, §21.8 `[R-ERR-02]`

**The newly pinned metadata content-size condition is folded into R3 without an
instance, so §21.8's normative one-vector-per-instance obligation builds no vector
for it — against §21.1's own enumeration rules and against the treatment of the
identical condition on a tile.**

§18.2:

> "The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal the
> byte length of the decoded document. A mismatch is a failure to decode within
> the meaning of R3"

R3's Instances cell reads, in full: "top-level extent; layer sub-record extent" —
two instances, both **containers**, no shape.

I checked first whether the routing to R3 rather than R4 is itself confused, and
it is not: R4's condition says "unlike R3, the constraint is broken whether or not
the bytes decode", and a content-size mismatch cannot be established without
decoding, so R4's own text self-selects it out. The routing is sound.

What does not follow is the instance count. §21.1:

> "a row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them (T15,
> T25). … Where the condition compares two **magnitudes** either of which can be
> the greater — a *differs from* or *does not equal* — the two directions are
> likewise enumerated"

R3's family now has two materially different shapes: a stream that fails to
decode, and a header field that disagrees with the produced length — the latter
being exactly a "does not equal" between two magnitudes either of which can be the
greater. The comparison rows elsewhere in the register do enumerate this: the tile
analogue **T22** is a row of its own with six instances (three layouts × two
directions), and **T25**, itself a decode-failure family, enumerates three shapes
by codec. R3 enumerates none.

The consequence is bounded but real, and it lands on the corpus rather than on any
implementation: §21.8 makes the coverage obligation normative — "one vector per
instance" — and `[R-VEC-03]` repeats it. With R3's cell as written, a corpus built
to §21.8 contains **no vector** for a user-metadata frame whose
`Frame_Content_Size` disagrees with the decoded document's length, which is the
one condition §18.2's sentence was added to pin. The register's totals stay
self-consistent either way — I counted them mechanically and they come to exactly
121/273 — so this is not an arithmetic error; it is a cell that under-enumerates
by §21.1's own stated axes.

I record it as an OBSERVATION rather than an AMBIGUITY because nothing here is
undecided for an *implementer*: the reader obligation is pinned (R3, detector
reader, extent use, ignore-record), the verifier obligation follows, and the file
is nonconforming. It is decidable from the text; what it costs is disproportionate
to spot, since it requires cross-reading §18.2 against §21.1's enumeration rules
against T22's parallel cell.

**Byte-level: no.** Reader behavior and file conformance are both fixed by §18.2's
own sentence; only the corpus's instance list is short.

---

## 11. What I could not determine

Nothing beyond the three findings above. Every constant reproduced, every worked
example reproduced, the register's own arithmetic reproduced, and the certification
procedure, coverage walk, overlap/alignment/slab invariants, checksum map,
decoded-content obligations and five-generation lifecycle were all implementable
from this document alone. The two places I had to reason rather than read — the
"every stored tile" / failed-crc interaction in §9.7, and the discard discipline
when layer validation and the coverage walk run in the opposite order — resolve to
the same verdict and the same bytes under either reading, so I did not raise them.
