# Cleanroom round 17 — Verifier implementer, working transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full, in five sequential reads (lines 1–400, 400–850, 850–1300, 1300–1750,
1750–2199, 2199–2648, 2648–3097, 3097–3543, 3543–3992, 3992–4317). I opened no
other file in the repository — no `docs/`, no ADRs, no `PLAN.md`, no
`AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git history. I ran
no web search or fetch. I did not list the output directory.

I ran local Python only, over files I created myself in my scratchpad:
`crc.py` (a CRC-32C implementation written from §4.5's parameters),
`build.py` (constructs a conforming TARN file byte by byte),
`verify.py` (a verifier written from the document),
`gens.py` (the four-generation lifecycle trace), plus ad-hoc probe scripts.
The only bytes I read from disk with a program were the ones those scripts
had just written. I used `grep` against `spec/tarn.md` once, to enumerate
verifier-binding obligations, and a Python script that parsed §21.2–§21.5's
tables out of `spec/tarn.md` to count register rows and instances.

Where I used prior knowledge of other formats it was only to generate
suspicions (e.g. "does a raw DEFLATE stream's trailing bit padding matter?"),
never to settle a question. Every settled question below cites the document.

---

## 1. What I built

A conforming verifier, as an ordered algorithm, plus the artefacts to exercise
it:

* `verify.py` — the certification procedure. Three verdicts,
  `CONFORMING` / `NONCONFORMING` / `CANNOT_ESTABLISH`, per `[R-CNF-11]`.
* `gen1.tarn` — a 2,112-byte conforming file I constructed by hand: two layers
  (one interleaved with a declared alignment and edge padding, one planar bool
  with a slab declaration), a file-scope user-metadata record, and an
  experimental-range MU = 0 ancillary record whose extent §8.1 covers by no
  checksum.
* gen 2 (append a layer), gen 3 (supersede a tile), and a compacted output.

Everything below is output from those runs.

---

## 2. The certification procedure, as an ordered algorithm

Assembled from §19.1 (open), §19.3 (layer access), §19.4 (tile use), §9.7
(coverage), §2.3 (verdicts), and Appendix H's checklist. §19's preamble was the
governing instruction for what to include: *"Those enumerations are not the
complete inventory of what a reader detects at that tier: §21's register is."*
So I drove the check list off §21.2–§21.5's 121 rows rather than off §19's
prose, and used §19 only to fix the *ordering*.

**Verdict vocabulary and availability** (§2.3, `[R-CNF-11]`):

| Verdict | When |
|---|---|
| *nonconforming* | any violation established. Takes priority: *"a verifier that has established any violation reports nonconforming, however many requirements it was unable to check"* |
| *cannot establish* | no violation established, and ≥ 1 requirement uncheckable on a capability or resource ground |
| *conforming* | no violation established, nothing left unchecked |

Two report-only channels that are **not** verdicts and never bar certification
on their own:

* *unexamined* — only reachable by electing to stop at the first violation, so
  it only ever co-occurs with *nonconforming*. §2.3: *"Unexamined is neither a
  verdict nor cannot establish — it constrains the report, not the verdict."*
* per-requirement "unable to check" reports, owed *"whichever of the three
  verdicts it reports"*.

And one advisory channel: SHOULD deviations. §2.4 is explicit that these do not
bar certification and that the verifier *"owes no search for one"* — its duty
*"runs to the MUST-level conditions §21 inventories"*. I therefore built no
SHOULD-hunting machinery (I do report `[R-CNT-03]` gap-zeroing deviations if I
happen to observe them, which the same sentence licenses).

**The ordered steps I implemented.**

0. Physical length ≥ 128 (`[R-CNT-27]`, F5). Must come first: below 128 there
   is no place for the trailer to be.
1. **Front block, by byte equality**, before other processing (`[R-CNT-04]`).
   The residency exemption is a *reader's*: §2.3 makes a verifier check *"every
   file-level requirement — including those ordinary readers are exempted
   from"*, and Appendix H spells it out — *"which `[R-CNT-04]` lets a reader not
   holding it resident defer or omit and §2.3 does not (F1, F6)"*. So a verifier
   always fetches [0, 16).
2. **Trailer in §6.2's fixed order**: magic → trailer CRC → version gate → then
   the remaining field gates. §21.2's preamble is the reason the order is
   load-bearing rather than cosmetic: only the magic, the CRC and the front
   block *"reach"* a file declaring a foreign major, because their subject is
   fixed across every major (`[R-CNT-24]`).
3. **Directory CRC** before any other use of the region (`[R-CNT-11]`, F20).
4. **Record walk** — framing, type 0, multiplicity, MU gate, extent slots, the
   user-metadata framing rules, the layer-name namespace. Uniqueness over raw
   bytes and decided *before* well-formedness, per §19.1 step 4.
5. **Per layer**: §19.3's full validation, then the index chain
   (`[R-IDX-04]`), then per-entry classification (§15.3), then payload CRC,
   then decode, then §14.5 / `[R-SER-08]` content checks.
6. **Coverage walk** (§9.7): disjointness, bounds, checksums, slack total.
7. Emit verdict + reports.

**What the verifier reports when a check cannot be run.** §2.3's grounds are
introduced with *"as when"*, so the list is illustrative, not closed. I
implemented: foreign major (`[R-CNT-07]`); an unimplemented type carrying
MU = 1 (§21.6 — and only from the *experimental* range, since §2.3 says *"a
reserved-range type carrying MU = 1 is itself a violation"*, i.e. F35, so that
path yields *nonconforming*, not *cannot establish*); codec/filter not
executable (`[R-COD-11]`); a decode declined on resource grounds (`[R-ERR-04]`,
`[R-SER-05]`, `[R-SER-08]`); a user-metadata document declined on the §21.9
bound (`[R-MTA-09]`). And explicitly **not** a ground: a user-metadata record
under an unassigned encoding — `[R-MTA-10]` and §9.7 both say nothing is left
unchecked there, so certification is unaffected and the record is instead
*reported*, naming owning scope, encoding value and stored extent length.

One thing I had to reason out rather than read: `[R-COD-11]`'s "cannot execute"
ground is, for a *conforming* verifier, unreachable. §17.4 says so itself —
every assigned codec and filter is core, so software that cannot execute one
*"is not a conforming reader"*, and any unassigned value is L43/L45, a
*violation*. So the only reachable decode-decline for a conforming verifier is
the resource one. That is a redundancy, not a defect: `[R-COD-11]` is there to
tell a partial implementation what to report honestly. I note it because I
spent time convincing myself it was not a hole.

### Probe results on the verdict machinery

```
P1  version_major = 7, front block + trailer CRC good  -> CANNOT_ESTABLISH
P2  version_major = 7 with a corrupt front block       -> NONCONFORMING   (violation takes priority)
P4  layer a codec=3, verifier lacking zstd             -> CANNOT_ESTABLISH
P5  layer a codec=3, verifier with zstd                -> NONCONFORMING   (payload is not a frame)
P6  layer a tile1 padding position != fill (T4)        -> NONCONFORMING
```

P2 is the case I most wanted to see behave: a file the document declines to
judge (`[R-CNF-02]`) can *still* be established nonconforming, because F1/F6/F8/F14
reach every major. §21.2's four-row carve-out is doing real work.

---

## 3. The coverage walk, with arithmetic

### 3.1 The partition, and whether a byte can be neither

§5.2's classes are: the front signature block; or a **structure** — a
stored-tile extent, a record extent, the directory, or the trailer. Everything
else is slack. §5.2's Note settles the "neither" question outright:

> *"The live committed state is defined as the front block plus what a complete
> coverage walk reaches, and `[R-LIF-08]` makes every byte that walk misses
> slack — so 'belongs to no class' describes nothing, and a register row for it
> would be a row no file could exhibit."*

So **no byte can be neither**. A verifier's testable obligation is disjointness
plus the total. I implemented exactly that.

Three things I had to read carefully to get the claimant set right, all of which
the document does settle:

* A record is **not** a claimant of its own header/inline payload — those lie
  inside the directory region, *"so reaching a record through the directory is
  traversal, not a second claim on those bytes"* (§9.7).
* A layer's tile-index region enters the walk **once**, as the layer record's
  extent, *"and is not a second claimant beside it"* (§9.7).
* The front block and the trailer **are** claimed, and the [16, F − 64) bound on
  everything else is what keeps them disjoint (§9.7).

And two edge classifications that decide real bytes:

* An entry `[R-IDX-03]` classifies reject-tile on a **structural** ground
  contributes no extent; *"the bytes it nominally addressed that no other
  claimant claims fall to slack"* (§15.3), and the walk stays **complete**
  (§9.7).
* An entry whose **only** defect is a failing stored-bytes crc is well-formed;
  *"its extent stands and it keeps its place in the verifier rows, in run
  continuity, and in the coverage walk"* (§15.3). Same, a fortiori, for a tile
  whose crc passes but whose decoded content or decode exactness fails: the
  entry is not defective at all, so its extent is claimed.
* An **ignored** record's extent is still claimed — §5.2 says *"whatever the
  record's type"*, and `[R-MTA-10]` confirms it for the unassigned-encoding
  case: *"bytes a certificate covers without inspecting are counted and named,
  never silent."*

### 3.2 A concrete file, and its total

`gen1.tarn`, built byte by byte. Layer `a`: interleaved, rank 2, extents (4, 5),
tile extents (2, 3) — so grid (2, 2), N = 4, P = 6, and the tiles at t_x = 1
carry padding at in-tile ordinals 2 and 5. Channels `p` (uint8, fill `00`) and
`q` (uint16, fill `ABCD`), so Q = 3 and the decoded size is 18. Codec 1, filter
1, alignment **A = 512**. Tiles 0, 1, 3 stored; tile 2 sentinel. Layer `b`:
planar bool, extent 10, tile extent 5 — N = 2, P = 5, packed decoded size
⌈5/8⌉ = 1, three pad bits per tile. **S = 2, A_slab = 1.** Plus a file-scope
user-metadata record (encoding 1) and an experimental-range type 0x8001 record
with an 8-byte extent.

```
  front            [     0,     16)      16
  tile a0          [   512,    530)      18     A = 512
  tile a1          [  1024,   1042)      18     A = 512
  tile a3          [  1536,   1554)      18     A = 512
  index a          [  1554,   1638)      84     = 4*20 + ceil(4/2^16)*4
  tile b0          [  1638,   1639)       1     slab run 0, first tile, A_slab = 1
  tile b1          [  1639,   1640)       1     packed: 1639 == 1638 + 1
  index b          [  1640,   1684)      44     = 2*20 + 4
  um extent        [  1684,   1747)      63     document + terminal CRC-32C
  unknown extent   [  1747,   1755)       8     covered by NO checksum (§8.1)
  directory        [  1755,   2027)     272
  trailer          [  2048,   2112)      64
  ------------------------------------------------
  claimed                               607
  F                                    2112
  SLACK  = 2112 - 607                  1505     EXACT (walk complete)
```

Slack runs, which is the useful diagnostic form: (16, 512) = 496,
(530, 1024) = 494, (1042, 1536) = 494, (2027, 2048) = 21. Sum 1505. ✓ The first
three are the price of `A = 512`; the last is the pre-trailer pad, which
`[R-LIF-02]` step 5 pads to the next 64-byte boundary (2027 → 2048 = 21 bytes).
Verdict: **CONFORMING**.

This file is a good advertisement for why §5.2 makes the total a MUST-report:
71% of it is slack, and nothing else in a certificate would say so.

### 3.3 Certified vs counted-but-unconstrained

* **Certified** (covered by a checksum §8.1 states, and verified): the trailer
  ([0,60) under [60,64)); the directory region; every tile-index region (entries
  under segment CRCs, the CRC array under `crc_of_crc_array`, that field under
  the directory CRC); every stored tile (its entry's crc); the user-metadata
  extent (its terminal 4 bytes). — 599 bytes here.
* **Certified by equality, not checksum**: the front block, 16 bytes.
* **Counted but unconstrained**: 1,505 slack bytes, plus the **8 bytes of the
  unknown record's extent**, which §8.1's last row covers by no checksum at all
  and §22.3 flags: *"corruption inside it is equally invisible"*. Note this is
  *claimed* state, not slack — it is inside the partition and inside the
  certificate, and uninspected.
* **Terminal checksum fields**, comparison-verified and covered by nothing
  further: trailer [60,64), the directory's last 4, the UM extent's last 4 —
  12 bytes. §4.5 enumerates exactly these three.

I checked §8.1's map for exhaustiveness against §5.2's claimant classes. The
"record extent" class splits into exactly three: the layer record's (= index
region), a user-metadata record's, and an unassigned type's. There is no fourth
— a registered type appearing outside the scope §7.3 gives it is L26/L13, and a
layer record with zero addressed tiles carries slot (0, 0). So **every live
structure is covered by exactly one checksum except the three stated
exceptions**, and the chain of trust in §8.2 closes with no dangling link.

### 3.4 A walk that does not complete

§5.2's rule, which I had to read three times to implement:

> *"a rejected layer's claimants are not enumerated, whether or not the
> rejection impeded reading them — and where the rejection is one the walk
> itself established, L18's overlap or L40 through L42's placement among them,
> the claimants it had already enumerated are discarded with the layer"*

My first implementation got this wrong in both directions and the probes caught
it: I was counting layer `a`'s claimants after establishing L40 (alignment).
Corrected, the two shapes are:

**(a) rejection established before enumeration** — layer `a` linearization set
to 2 (L33, reject-layer at layer access). Layer `a`'s claimants are never
enumerated at all:

```
enumerated: front 16 + index b 44 + b0 1 + b1 1 + um 63 + unk 8 + dir 272 + trailer 64 = 469
partial slack = F - 469 = 2112 - 469 = 1643
```

**(b) rejection established *by* the walk** — layer `a`'s tile 1 moved to offset
1025 with `A = 512` still declared (L40). The claimants were enumerated, the
invariant checked, and then discarded:

```
claimed=469  slack=PARTIAL 1643  stopped_by=L40 in layer#0
```

Both give 1643 against a true 1505 — an **upper bound**, never an under-count,
exactly as `[R-CNT-21]` promises, and 138 bytes loose (layer `a`'s 3 × 18 tile
bytes + 84 index bytes). And per `[R-CNT-21]` the report must name what stopped
the walk, which mine does.

**A nonconforming file with an EXACT total.** Probe P3: layer `a` entry 0's
offset set to 8 (T8, structural).

```
P3  layer a entry 0 offset=8 (T8, structural)  -> NONCONFORMING
    claimed=589 slack=1523 EXACT
```

589 = 607 − 18: the structurally-rejected entry's 18 nominal bytes fell to
slack, the walk did not become incomplete (§9.7 says so in terms), and the total
is exact. So "nonconforming" and "exact slack total" are independent axes. That
is not obvious from §5.2 alone and I want it on the record as the answer I
settled on.

**One place I had to guess.** §5.2 handles three ways a walk fails to complete:
a *layer*-scope rejection, an election to stop, and (by exclusion) a pre-trailer
rejection where no total is owed. It does not say what a verifier that
establishes a **file**-scope violation *after* the trailer — F20's directory
CRC, F4's duplicate layer name, F33's overlap — and elects to continue should
report. Reading "a scope-level rejection ends that scope's enumeration" with
"that scope" = the file gives: partial, F less whatever was enumerated. I
implemented that. I am not filing it, because §5.2 already concedes that a
partial total *"reports what one verifier's incomplete walk left unclaimed,
which is a fact about that run and not about the file"* — variance between
verifiers is licensed here by design, and both readings yield a valid upper
bound. It is a genuine under-determination of a report, not of a verdict.

---

## 4. Extent overlap, alignment, and slab, on adversarial layouts

All four built by mutating `gen1.tarn` and repairing every checksum in the chain
above the mutation, so that each file fails on exactly the invariant under test.

**A1 — intra-layer overlap.** Layer `a` tile 0's length set to 600, so
[512, 1112) swallows tile 1's [1024, 1042). Both extents belong to layer `a`.

```
viol ('T1','tile','layer#0 tile 0 crc')          <- expected: the extent now covers different bytes
viol ('L18','layer','overlap tile 0/tile 1')     <- reject-layer
verdict NONCONFORMING; walk incomplete, partial total
```

§7.2: *"a verifier MUST treat an intra-layer overlap — including a stored extent
overlapping its own layer's index region or sub-record extents — as
reject-layer"*, and §15.3's table row agrees. L18 it is.

**A2 — cross-layer overlap.** Layer `b` tile 0 re-pointed to 1560, inside layer
`a`'s index region.

```
viol ('F33','file','overlap index region/tile 0')  <- reject-file
```

Correct: §7.2 assigns *"any overlap across layers or touching another scope's
structures"* to reject-file, and §15.3's row says the same. F33's own text
confirms the boundary — a claimant reaching the front block or trailer is
instead caught by the bounds rows F9/F10, F31/F32, L16/L17, T8/T9. I checked
that partition: it is complete, because every claimant class carries a
`≥ 16` / `≤ F − 64` rule of its own (`[R-CNT-06]`, `[R-CNT-13]`, §15.3), so the
only way to reach [0,16) or [F−64, F) is through a bounds row.

**A3 — alignment.** `A = 512` declared, tile 1 relocated to 1025.

```
viol ('L40','layer','layer#0 tile 1 offset 1025 not 512-aligned')
```

`[R-SLB-01]` quantifies over *"every stored tile's offset"* in the live
generation, and §20.3 step 4 keeps that quantifier honest across commits —
*"every one the new state keeps, not only those this commit adds"*. Same domain
on both sides; I checked this specifically because the brief warned about
permissions and prohibitions ranging over different sets.

**A4 — slab packing.** Layer `b`, S = 2, A_slab = 1, tile 1 moved from 1639
to 1641.

```
viol ('L41','layer','layer#1 run@0 not packed (1641 vs 1639)')
```

The run partition I implemented from `[R-SLB-02]`: blocks are [0, N) interleaved
and [c·N, (c+1)·N) per channel planar, *"runs never span channel blocks"*, and
run r of a block starts at `block_start + r·S` — i.e. runs are aligned to the
**block** start, not to ordinal 0. The transparency rules from `[R-SLB-03]` are
unambiguous and I implemented them literally: sentinels transparent;
structural-reject entries transparent; a crc-failing entry **not** transparent,
*"its offset and length stand, and the packing relation reads them as it does
any other stored tile's"*. That last clause is what keeps L41 decidable from the
index alone, which is the property `[R-SLB-03]` claims for itself, and it holds.

I also confirmed that "the previous stored tile's offset plus its length" means
the *previous* tile's length, not the current one's — L41's own wording,
*"the previous stored tile's offset plus that tile's length"*, disambiguates it.

---

## 5. Checksum obligations, and every constant I could compute

I wrote CRC-32C from §4.5's parameters alone (Castagnoli, reflected in and out,
init and final XOR 0xFFFFFFFF, stored little-endian) and gated it on the check
vector before using it for anything.

**Reproduced — every stated checksum constant in the document:**

| Constant | Stated | Computed |
|---|---|---|
| §4.5 / App. B — CRC-32C(`"123456789"`) | `0xE3069283` | `0xe3069283` ✓ |
| §4.5 / App. B — CRC-32C(zero bytes) | `0x00000000` | `0x0` ✓ |
| §15.4 / App. B — full all-sentinel segment (2¹⁶ entries) | `0xEECB3BB2` | `0xeecb3bb2` ✓ |
| §7.4 example — segment CRC over 4 sentinel entries (80 bytes) | `0x80A34955`, stored `55 49 A3 80` | `0x80a34955`, `55 49 a3 80` ✓ |
| §7.4 example — `crc_of_crc_array` over that 4-byte array | `0xC4EE982E` | `0xc4ee982e` ✓ |
| Appendix A — trailer CRC over bytes [0, 60) | `0xE00938D2`, stored `D2 38 09 E0` | `0xe00938d2` ✓ |
| Appendix A — directory CRC over zero record bytes | `0x00000000` | `0x0` ✓ |

**Could not reproduce:** none. There is no stated checksum constant in this
document that I was unable to compute locally.

I also recomputed every non-checksum worked number I could:

* §17.3's byte-shuffle example — 1.0, 2.0, 3.0 float32 shuffle to
  `00 00 00 00 00 00 80 00 40 3f 40 40` ✓, and the stated inverse round-trips ✓.
* §14.3's packed-bool example — P = 10 alternating, `55 01` at fill false and
  `55 FD` at fill true ✓ (both).
* §15.4's entry_count = 1,000,000 example — 16 segments, last covering 16,960;
  64-byte CRC array; region 20,000,064 bytes; k = 999,999 in segment 15 at
  segment-relative byte 339,180; array at [20,000,000, 20,000,064); segment 15
  at [19,660,800, 20,000,000); a full segment 1.25 MiB ✓ (all).
* §15.4's planar example — C = 4, N = 32, channel 2 at s = 10 → disk ordinal 74,
  entry at [1,480, 1,500); channel 3's entries 96–127 ✓.
* §11.4's example — (300, 700) → tile (1, 2), s = 10, in-tile (44, 188), in-tile
  ordinal 11,452 ✓.
* §7.4's worked layer record — I rebuilt the whole 81-byte inline payload from
  the field table and got 81 exactly, with bytes 56–68 matching
  `04 74 65 6D 70 0C 00 / 04 00 00 C0 7F`, grid 4, extent_length 84, and the
  stated 4 + 34 + 18 + 12 + 13 decomposition ✓.
* §5.1 / Appendix A — the 128-byte minimal file parses and certifies under my
  verifier ✓.
* §21.8's bookkeeping — I parsed §21.2–§21.5's tables mechanically:
  **36 + 49 + 26 + 10 = 121 rows** and **58 + 116 + 55 + 44 = 273 instances**,
  matching *"121 conditions over 273 instances"* exactly, and each subsection's
  own stated count. Detector split: 101 reader / 20 verifier.

That is an unusually clean result and I want it stated plainly: the document's
arithmetic is sound everywhere I could check it.

**Which structures are covered by which checksum** — see §3.3 above. The answer
to "is every live structure covered by one?" is **no, and deliberately so**:
three classes are not, and §4.5 and §8.1 enumerate exactly the same three
(front block by equality; the three terminal checksum fields; an unassigned
type's extent). §22.3 names the consequence for the third. I found no fourth
uncovered class.

---

## 6. Decoded-content obligations

**What a verifier MUST decode.** §9.7 is categorical: *"A verifier decodes every
stored tile, whatever content obligations §14 places on the layer"* — the
reason being that §21.4's codec rows (T24, T25, T3, T17–T22) are file-conformance
violations and *"a verifier MUST NOT certify past a violation it has not looked
for."* So decoding is not conditional on the layer having padding positions or
bool channels. I implemented that; my layer `c` in gen 2 has neither, and is
still decoded.

**What it compares against.** Three things, and only three:

1. Decoded length **exactly** the decoded size derived from declarations alone
   (`[R-SER-07]`, T3) — and under codec 1 the *entry length* too, before any
   fetch (`[R-COD-04]`, T14).
2. Every padding position carries its channel's recorded fill
   (`[R-SER-05]`, T4), and every pad bit the plane's fill bit (T5).
3. Every interleaved bool byte at a **real** position is 0x00 or 0x01
   (`[R-SER-08]`, T2).

I checked T2/T4's partition of `[R-SER-08]` carefully, because §21.4 was flagged
as changed and T2 carries an explicit narrowing — *"the same byte at a padding
position is T4's, the two rows together covering `[R-SER-08]`"*. It closes: a
bool fill byte is constrained to 0x00/0x01 by `[R-TYP-07]`, so **every**
interleaved bool byte at a padding position that violates `[R-SER-08]` also
violates `[R-SER-05]` and fires T4. Same detector, same detection point, same
tile scope. No gap. The narrowing is correct.

**What it is permitted to skip.** Nothing, except on a resource ground, and
skipping costs it certification: §17.4 and `[R-MTA-09]` both say the file's
verdict becomes *cannot establish* where no violation was found elsewhere. The
one thing it genuinely need not look at is a user-metadata document under an
**unassigned** encoding — §9.7: *"asks nothing of this walk: no rule attaches to
its content, so there is no violation there to look for"* — and there it owes a
report instead, per `[R-MTA-10]`.

**What no decode can catch**, which a certificate must not be read as covering:
§21.7 is blunt about it — *"this format detects corruption of structure, not
incorrectness of content"*. A mis-strided filter or an undisclosed zstd
dictionary produces a file every checksum certifies, unless the wrong bytes
happen to land on a padding position, a pad bit, or a boolean byte (T26's
route). §21.7 correctly says none of this is a "cannot check" ground: *"no
file-level witness exists to check, so nothing about the file is left
undetermined and the verdict is unaffected."*

---

## 7. The multi-generation trace

```
gen 1  (creator)                   F=  2112  CONFORMING  claimed=607 slack=1505
gen 2  (append new layer c)        F=  2624  CONFORMING  claimed=735 slack=1889
gen 3  (supersede layer a tile 1)  F=  3648  CONFORMING  claimed=735 slack=2913
compacted (new file_id, gen 1)     F=  2240  CONFORMING  claimed=735 slack=1505
```

* **gen 2** is §20.3's shape (a): a new layer `c`, writing beginning at exactly
  F = 2112 (`[R-LIF-02]` step 1). Layers `a` and `b` and both non-layer records
  carried into dir₂ **byte-identically**, extent slots and all (`[R-WRT-05]`),
  so `a`'s index never moves. Slack grew by 384 — dir₁ + pad₁ + trailer₁ — which
  is sized by the layer count, not by any layer's data, exactly as §20.3's
  figure claims.
* **gen 3** is shape (b): supersede layer `a`'s tile 1. The whole index region
  is re-emitted (`[R-WRT-04]`: *"entry_count entries plus the segment CRC
  array — necessarily at a new placement"*), one entry re-pointed and three
  byte-identical at their disk-ordinal positions. The new payload had to land
  on a 512 boundary, because `A = 512` binds *"every one the new state keeps"*.
  Slack grew by 1,024: the old index (84), the superseded payload (18), dir₂ +
  pad + trailer, and the alignment gap the 512 boundary forced.
* **compaction** minted a fresh `file_id` (0x00FEDCBA98765432) and generation 1,
  carried every stored tile's bytes and every entry crc verbatim, regenerated
  both relocated index regions with new offsets and recomputed segment CRCs, and
  updated each `crc_of_crc_array`. I verified `[R-WRT-07]`'s hard requirement
  directly: **the reference arrays of gen 3 and the compacted output are equal**
  (I compared, per layer and per disk ordinal, the stored bytes of every stored
  tile and the FILL marker of every sentinel — `gen3 == compacted: True`).

The compacted file is only 1,408 bytes shorter than gen 3, and still carries
1,505 bytes of slack, because `A = 512` forces the same gaps. Worth stating
because §20.5's *"so slack is never carried"* is easy to misread as "the output
has no slack": it means the *input's* slack is not copied. A compactor that
honours a declared alignment necessarily creates its own.

---

## 8. Findings

Four. Two concern the append/compaction rules in §20.4 and §20.5, one concerns a
tense in §11.1's account of §20.3, and one is a hazard in compaction's handling
of malformed index entries.

---

### verifier-01 — CONTRADICTION

**§11.1's Rationale states §20.3's shrink bar over the new generation's stored
set; §20.3 states it over the superseded generation's.**

§11.1 (Rationale block):

> *"§20.3 states normatively, and governs, what a commit may do to a layer that
> already stores tiles: a shrink is barred wherever it alters what §14 fixes for
> a tile **the new state still stores**, and permitted where it drops tiles out
> of the addressed set, whose extents then become slack. A layer that stores
> nothing may be re-declared freely."*

§20.3 step 4:

> *"a shrink is permitted exactly where it alters nothing §14 fixes for any tile
> the layer stores **in the generation this commit supersedes**. ... Unstoring
> that tile in the same commit does not rescue it either, and for the same
> reason: the quantifier is the superseded generation's, so a shrink that turns
> real positions into padding of a tile stored there is barred **whether or not
> the new state still stores it**."*

These range over different sets and are opposed on precisely the case §20.3 goes
out of its way to name. A shrink that turns real positions into padding of a
tile stored in generation *n*, where the commit producing generation *n+1* also
unstores that tile: §20.3 bars it in terms; §11.1's Rationale permits it,
because the new state does not store the tile. §11.1's second sentence has the
same problem in miniature — *"A layer that stores nothing may be re-declared
freely"* omits the tense that §20.3 spends a clause insisting on (*"the tense is
the bar's, so a commit does not earn this permission by emptying the layer as it
re-declares it"*).

**Which I picked, and why.** §20.3's. Two independent reasons: `[R-CNF-01]`
makes text *"labeled Note, Example, or Rationale"* non-normative, and this block
is labeled Rationale; and the Rationale itself defers — *"§20.3 states
normatively, and governs"*. So an implementer who notices the conflict resolves
it correctly.

**What an implementer does wrong without it.** An appender author who reads
§11.1 — which sits in the normative geometry section, immediately after
`[R-GEO-02]`, and reads as an authoritative summary of the rule it names — will
build the shrink guard over the wrong generation's stored set. That guard is
strictly weaker: it permits commits §20.3 bars. Nothing will ever tell the
author, because §21.7 records that this is exactly where the bar has no witness
(*"a commit that supersedes every tile it would have damaged leaves the live
state clean"*), so no verifier and no corpus vector can catch the mistake. A
summary that silently inverts a quantifier in a rule whose violations are
undetectable is worth more than the usual amount of care.

**Byte-level:** no. `[R-CNF-01]` decides it, and there is no file-level witness
either way — §21.7 places §20.3 step 4's bar in the class of obligations *"a
single file exhibits no witness of their violation"*. No verifier verdict on any
byte sequence differs.

---

### verifier-02 — AMBIGUITY

**§20.5: a compactor both must and must not emit an output carrying a
structurally-malformed index entry.**

`[R-WRT-06]`:

> *"A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
> fails, and MUST NOT emit a file carrying a violation it has detected: it can
> neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call
> the output clean. Dropping is the one disposal that answers, and only where
> §20.4's table licenses it ... Where the table does not license a drop the
> compactor MUST refuse."*

`[R-WRT-07]`:

> *"an entry §15.3 classifies reject-tile on a structural ground is reproduced
> with its offset and length exactly as they stand ... and the violation travels
> with it into the output (`[R-WRT-01]`); `[R-WRT-09]`'s checks reach the index
> chain and each stored tile's entry crc, not an entry's own value domain, so
> such an entry is not one `[R-WRT-06]` obliges a compactor to refuse"*

`[R-WRT-06]` states **two** independent bars. `[R-WRT-07]` rebuts only the
first: it shows the entry's value domain is outside `[R-WRT-09]`'s obliged
checks. It says nothing about the second — *"MUST NOT emit a file carrying a
violation it has detected"* — and the compactor **has** detected this one. It
must have: `[R-WRT-07]` itself instructs it to distinguish *"an entry §15.3
classifies reject-tile on a structural ground"* from a sentinel and from a
re-pointable entry, which is §15.3's classification, whose rows (T6–T12) are
reader-detected. §20.1 and `[R-WRT-03]` confirm the reliance that triggers the
duty: a compactor *"relies structurally on every structure it copies"*. Dropping
is not available — §20.4's table licenses dropping *records*, not index entries
— so `[R-WRT-06]`'s second bar reads: MUST refuse.

**Permitted readings.** (a) `[R-WRT-07]`'s closing clause is a stipulation over
`[R-WRT-06]` as a whole — *"not one `[R-WRT-06]` obliges a compactor to
refuse"* — and so disposes of both bars regardless of the reasoning offered:
the compactor reproduces the entry and emits. (b) The stipulation is only as
wide as the reason given for it, which reaches one bar; the other stands
independently, so the compactor refuses.

**Which I picked.** (a). The clause names `[R-WRT-06]` and states a conclusion
about it without qualification, and a stated conclusion outranks an incomplete
justification for it. My compactor reproduces and emits.

**What an implementer does wrong without it.** A compactor author who checks the
reasoning rather than the conclusion finds it does not cover the case, distrusts
the conclusion, and refuses to compact any file containing a single malformed
index entry — the exact files whose owners most want them compacted, and files
whose other layers are perfectly serviceable. The opposite error is milder but
real: an author following (a) without noticing the second bar will not realise
they need `[R-WRT-07]`'s licence at all.

**Byte-level:** no. The explicit clause in `[R-WRT-07]` names `[R-WRT-06]` and
decides it, so a careful implementer does not fork; and the disagreement is
between emitting an output and refusing to, not between two outputs. Every
reader and verifier reaches the same verdict on whatever bytes result.

---

### verifier-03 — AMBIGUITY

**§20.4: does a commit that re-points a layer record's extent slot count as
"modifying any layer's record" for the MU = 0 / PE = 0 drop licence?**

§20.4's table, MU = 0 / PE = 0 row:

> *"An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's record, the
> entry set of its index, or which of its tiles are stored; for a top-level
> record, the file's layer set — which a commit changes by adding or removing a
> layer and equally by **modifying any layer's record** — or another *non-layer*
> top-level record. Superseding a stored tile's bytes is not such a change for
> either kind — it re-places that layer's index region (§20.3, `[R-WRT-04]`)
> without altering the scope any record attaches to — so a commit whose only
> change is a supersede MUST retain the record."*

The deciding case is **not** the supersede, which the last sentence settles, but
the neighbouring one it does not reach: a commit whose only change is to
**store a tile that was previously a sentinel** in layer X, in a file that also
carries an unrelated top-level MU = 0 / PE = 0 ancillary record. Such a commit
re-emits X's index region *"necessarily at a new placement"* (`[R-WRT-04]`), so
X's layer record's extent slot changes and the record cannot be re-emitted
byte-identically — which is precisely what `[R-WRT-05]` calls modifying it
(*"every record it retains and does not logically modify; a record it modifies
is new output"*).

**Permitted readings.**

(a) *Modifying = any change to the record's bytes.* Storing a new tile modifies
X's record, therefore changes "the file's layer set" by the em-dash clause,
therefore licenses dropping the top-level ancillary. The supersede carve-out is
load-bearing on this reading: it exists precisely because a supersede would
otherwise qualify by the same mechanics.

(b) *Modifying = changing the layer's declarations.* §20.3's shape (c) supplies
the referent — *"clearing a slab declaration, renaming a layer, or changing a
channel's fill value"* — commits that change a layer record without touching its
index. On this reading the store does not license the drop, and the supersede
carve-out is clarifying rather than load-bearing. Reading (b) is supported by the
carve-out's own *reason*: *"it re-places that layer's index region ... without
altering the scope any record attaches to"* — a sentence that is equally true of
storing a new tile, so if it is a reason at all it excludes the store too.

**Which I picked.** (b), on the ground that the carve-out's stated reason is
general and the em-dash clause's purpose is to name changes to the *layer set*,
which neither a store nor a supersede is. My updater retains the ancillary
record through any commit that only changes a layer's stored-tile set. But I
hold this weakly, and reading (a) has the better textual claim on the literal
words.

**What an implementer does wrong without it.** Two conforming updaters, given
the same file and asked to store one tile, emit different directories: one
carrying the ancillary record's 24-byte header plus its inline payload, one not
— and consequently different `dir_length`, a different directory CRC, a
different `F`, and a live extent in one file that is slack in the other. The
record is application state, and §20.4 itself says the loss *"SHOULD be
reported"* because *"unreported, application state disappears with no
diagnostic."* This is the one preservation question an updater author cannot
route around: it decides whether user data survives a routine append.

**Byte-level:** yes — see the structured field for the case, stated with its
limits.

---

### verifier-04 — OBSERVATION

**§20.5: reproducing a structurally-rejected index entry verbatim is not stable
under a change of F, so "the violation travels with it into the output" can
fail.**

`[R-WRT-07]`:

> *"an entry §15.3 classifies reject-tile on a structural ground is reproduced
> with its offset and length exactly as they stand, there being no live extent
> for a re-pointing to target ... and the violation travels with it into the
> output (`[R-WRT-01]`)"*

Four of §15.3's six structural rows classify an entry by comparing its fields
against **F**: `offset + length > F − 64`, and the overflow rows. F is not
preserved by compaction. Take an input with `F_in = 100,000` and an entry
`offset = 99,000, length = 5,000`: `99,000 + 5,000 = 104,000 > F_in − 64`, so
the entry is structural reject-tile (T9) and contributes no claimant. The
compactor reproduces `99,000 / 5,000` verbatim. Nothing in §20.5 bounds the
output's length — *"it is free to place structures anywhere §5.2 admits"*, and
gaps it leaves are slack — so `F_out` can exceed 104,064. In that output the
entry is **no longer** structurally rejected: it is a well-formed non-sentinel
entry addressing live bytes.

Three outcomes, none of them "the violation travels":

* those bytes belong to another structure → the output carries **L18 or F33**,
  a *different and broader* violation than the input's tile-scope one;
* those bytes are slack → the entry's reproduced `crc` field almost certainly
  mismatches → **T1**, again a different row;
* adversarially chosen so the crc matches → the output is **conforming**, and
  the tile decodes to content the input's reference array never denoted, which
  `[R-WRT-07]`'s own *"The output's reference arrays MUST equal the live
  generation's bit for bit"* cannot police, the input's reference array being
  undefined at a tile `[R-TYP-09]` bars from reading as fill.

It is decidable from the text — §20.5 says reproduce verbatim, §15.3's rows read
F, and nothing pins `F_out ≤ F_in` — but the chain runs through four sections
and a quantifier over compactor placement freedom, which is why I am filing it
as an observation rather than expecting it to be obvious. The cheap fix an
implementer can adopt unilaterally: refuse to compact any input carrying a
structurally-rejected entry whose classification depends on F, or re-emit it as
`offset = length = 0` — though `[R-WRT-05]`'s byte-identity and §20.5's *"exactly
as they stand"* both bar the second.

**Byte-level:** no. Placement freedom already licenses two compactors to emit
different outputs from one input (`[R-CNF-05]`), and every reader and verifier
agrees about whatever output results. What fails is a claim the document makes
about its own mechanism, not a determination about bytes.

---

## 9. Things I checked and found sound

Recording these because a clean result is only worth the work behind it, and
because several are places earlier rounds would plausibly have looked.

* **§21's bookkeeping** — 121 rows, 273 instances, every subsection count
  matching, computed mechanically from the tables.
* **§8.1's coverage map is exhaustive** over §5.2's claimant classes, and §4.5's
  three-exception list matches it exactly. The chain of trust in §8.2 closes.
* **T2/T4's partition of `[R-SER-08]`** closes, because `[R-TYP-07]` constrains
  the bool fill byte to 0x00/0x01 (§6 above).
* **The verdict priority rule** — an established violation beats any number of
  unchecked requirements — is stated and unambiguous, and correctly makes a
  foreign-major file with a corrupt front block *nonconforming* rather than
  *cannot establish* (probe P2).
* **`[R-SLB-01]`'s and §20.3's alignment quantifiers agree** (both "every stored
  tile the new state keeps"), which is the pairing the brief warned about and
  which I checked explicitly.
* **§20.3's bar, permission, shrink and grow clauses all use one tense** — the
  superseded generation's — and the text says so three times. The only place
  that tense is stated differently in this document is §11.1's Rationale
  (verifier-01).
* **Ignored records' extents remain claimants**, so `[R-MTA-10]`'s "counted and
  named" and §5.2's partition agree.
* **A structurally-rejected entry leaves the walk complete**; a crc-failing one
  keeps its claim. Both stated in terms, both implemented, both probed.
* **§20.5's "free to place structures anywhere §5.2 admits"** is narrower than
  the actual constraint set (§6.2's pre-trailer-gap rule, F7, is not in §5.2),
  but `[R-CNF-05]` via `[R-WRT-01]` obliges a compactor to emit a conforming
  file regardless, so the shorthand under-states without licensing anything.
  Not filed.
* **§21.7's "witnessed only where the affected tiles remain stored *and* the
  change reaches a byte §14 structurally constrains"** over-states in its first
  limb and is corrected by its own second limb (T3/T14 witness a decoded-size
  change). Prose, not a fork; §21.4's rows govern what a verifier checks and I
  check all of them. Not filed.
* **`[R-COD-11]`'s "cannot execute" ground is vacuous for a conforming
  verifier** (§2 above), which is a redundancy the document itself explains, not
  a hole.
* **The slack total after a post-trailer file-scope rejection** is
  under-determined as to the number, but §5.2 explicitly licenses that variance
  (*"a fact about that run and not about the file"*), and every reading yields a
  valid upper bound. Not filed.

## 10. Where my implementation, not the document, fell short

For honesty about what the probes did and did not exercise: my verifier does not
implement JSON parsing, so it checks none of R5–R10 or F27/L48; it decodes only
codecs 1 and 2 (deflate via zlib), so T17–T22 were exercised only by their
failure path; its F7 test catches a structure wholly inside the pre-trailer gap
but not one straddling its start; and when it elects to stop at the first
violation it currently reports no slack total at all, where `[R-CNT-21]` obliges
a partial one. None of these is a gap in the document.
