# Round 11 — Verifier implementer, working transcript

**Charter.** Implement, on paper but concretely, a conforming TARN verifier: the
certification procedure, the coverage walk, extent/alignment/slab invariants,
checksum obligations, decoded-content obligations, and a multi-generation trace.

**Access.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,953 lines, read whole in five `Read` calls). I ran `grep` against that file
only. All other computation was local Python over byte buffers I constructed
myself in a scratch directory. I did not open `docs/`, `conformance/`,
`spec/registry.json`, `PLAN.md`, `AGENTS.md`, `OPEN-QUESTIONS.md`, `README.md`,
git history, or any network resource.

**One disclosure that is not a breach but is worth stating.** My first scratch
directory was the shared `scratchpad/round11/`. Between two of my Bash calls a
*concurrent process* overwrote my `crc.py` and `build.py` with files of the same
names belonging to some other run, and its stdout (lines like
`layer A inline_length 98`, a trailer hex string, `slack runs: [...]`) appeared
in my terminal as a side effect of my own `python3` invocation. I did not read
any file to obtain that; I did not use any of it; and I immediately moved my work
to a private subdirectory `scratchpad/round11/vfy-work/` and rebuilt every scratch
file from scratch. Everything below was re-derived after the move. I flag it
because an undisclosed contamination poisons a round and a disclosed one does not.

---

## 0. Reading order and what I built

I read §2 first (as §1 advises), then Part I end to end, then Part II, then
Part III, then the appendices, then re-read §2.3, §5.2, §9.7, §21.1, §21.7 and
Appendix H several times because the verifier's whole contract lives in those
six places and nowhere else in one piece.

What I built:

* `crc.py` — CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF).
* `build.py` — structure emitters for the trailer, records, layer-record inline
  payload, and tile-index regions.
* `verify.py` — the verifier: ~230 lines implementing the ordered certification
  procedure, the coverage walk with a claimant list, extent overlap, alignment
  and slab invariants, the index chain, and the three-verdict report model.
* `mk.py` / `adv.py` / `trace.py` — one conforming file, eight adversarial
  variants, and a four-generation trace.

---

## 1. The certification procedure, as an ordered algorithm

The document never states the verifier's algorithm in one place. It has to be
assembled from §2.3 (`[R-CNF-11]`), §19.1–§19.4 (which the verifier inherits as a
reader), §9.7 (`[R-LIF-08]`), §8.2 (`[R-CNT-20]`), and §21's Detected column.
This is the order I implemented, and I believe it is forced:

| # | Check | Input | Failure | Notes |
|---|---|---|---|---|
| 0 | file size F′ (transport-authoritative) | transport | — | `[R-CNT-10]`; §19.1 step 1 |
| 1 | front block equality, if [0,16) resident | bytes [0,16) | F6/F1, reject-file | `[R-CNT-04]`; see finding **verifier-01** |
| 2 | physical size ≥ 128 | F′ | F5, reject-file | `[R-CNT-27]` |
| 3 | trailer magic at F′−64 | 8 bytes | F8, reject-file | `[R-CNT-06]`, fixed across majors (`[R-CNT-24]`) |
| 4 | trailer CRC over [0,60) | 60 bytes | F14 | ordered *before* the version gate |
| 5 | version gate | version_major | F18, or *cannot establish* | 0 → violation; other major → verdict fixed, §2.3 |
| 6 | flag gates | flags | F19 (incompat lane) | ignore lane never a violation (§21.6) |
| 7 | remaining trailer gates | trailer | F9–F13, F15–F17, F2, F3 | `[R-CNT-06]`'s enumerated list |
| 8 | directory region CRC | dir_length bytes | F20 | `[R-CNT-11]`, before any other use |
| 9 | record walk, framing | record sequence | F29, F24 | `[R-CNT-12]` |
| 10 | per-type multiplicity | records | F34 | `[R-CNT-14]` |
| 11 | flag bits (verifier-only) | each record | F25/F26/F28, L46/L47/L49 | `[R-CNT-12]`, `[R-CNT-22]` |
| 12 | reserved-range types (verifier-only) | each record | F36/F35, L25/L24 | `[R-CNT-15]` |
| 13 | extent slots of non-layer top-level records | slots | F30/F31/F32 | `[R-CNT-13]` |
| 14 | layer-name namespace, over raw bytes, *first* | layer records | F4 | §19.1 step 4 |
| 15 | per layer: full `[R-RDR-03]` validation | inline payload | L1–L36, L39, L43–L45 | §19.3, all I/O-free |
| 16 | per layer: index chain | crc_of_crc_array, segment CRCs | L37/L38 | `[R-IDX-04]` |
| 17 | per entry: §15.3 classification | 20 bytes | T6–T12 | six *structural* rows |
| 18 | per stored tile: entry crc, then codec/filter decode | payload | T1, T3, T14–T25 | `[R-CNT-20]`, `[R-COD-08]` |
| 19 | per stored tile: decoded-content | decoded image | T2, T4, T5, T26 | `[R-SER-05]`, `[R-SER-08]` |
| 20 | alignment / slab invariants | index bytes only | L40, L41, L42 | `[R-SLB-01]`, `[R-SLB-03]` |
| 21 | per user-metadata extent: CRC, decode, content, sort | extent | R2–R10, F27/L48 | `[R-CNT-20]`, `[R-MTA-04]`, `[R-MTA-05]` |
| 22 | coverage walk: disjointness, [16,F−64) bounds | claimant list | F33, L18 | `[R-LIF-08]`, `[R-CNT-13]` |
| 23 | `[R-CNT-05]`: nothing live between dir end and trailer | claimant list | F7 | verifier-only |
| 24 | slack total (exact or partial) | claimant list | — | `[R-CNT-21]`, MUST report |

Two orderings are pinned by text rather than by dependency and I had to obey them
rather than optimise: (a) §6.2's "in order: the trailer magic; the trailer CRC;
the version gate … and then, those gates passed, MUST validate all of the
following"; (b) §19.1 step 4's "Uniqueness is decided first, and over the raw name
bytes whether or not each name is itself well-formed" — which is why F4 sits at
step 14 and L3/L5/L6 (also at *open*, per §21.3) sit after it.

### 1.1 Verdict vocabulary

Three verdicts (`[R-CNF-11]`): **conforming**, **nonconforming**, **cannot
establish**. The availability rules are stated crisply and I found them
implementable without guessing:

* Any *established* violation ⇒ **nonconforming**, "however many requirements it
  was unable to check". Established violation dominates absolutely.
* **cannot establish** is available *only* to a traversal that established no
  violation, and only when some requirement is one it "is unable to check on a
  capability or resource ground".
* Otherwise **conforming**.
* A verifier MUST NOT certify a file it reports as *cannot establish*.

The report carries three things beside the verdict, and they are three different
things, which the document is careful about and which I implemented as three
separate lists:

1. **findings** — established violations, each with row, scope, governing rule.
2. **unchecked** — "each requirement it was unable to check on a capability or
   resource ground, naming the requirement and the ground", emitted "whichever of
   the three verdicts it reports". This constrains the report, not the verdict.
3. **unexamined** — scopes skipped by a verifier exercising `[R-CNF-11]`'s licence
   to stop at the first violation. "*Unexamined* is neither a verdict nor *cannot
   establish*."

Plus **advisories** for SHOULD deviations, which "[do] not bar certification"
(`[R-CNF-12]`).

The enumerated capability/resource grounds (§2.3) are: an unimplemented format
major; a record with MU = 1 of a type it does not implement; inability to execute
a codec or filter (`[R-COD-11]`); a decline of a layer's or tile's decode on
resource grounds (`[R-ERR-04]`); a decline to decode a user-metadata document
(`[R-MTA-09]`). The list is introduced with "as when", so it is illustrative — I
relied on that when handling a verifier that declines a 200 MiB directory, which
is on no list but is plainly a resource ground.

Note that `[R-COD-11]`'s ground is *unreachable for a conforming verifier* if
"cannot execute" means "does not implement": §17.4 itself says so — every assigned
codec and filter is core, and a reserved or experimental value is a layer-scope
violation (L43/L45), i.e. **nonconforming**, not *cannot establish*. I read
"cannot execute" as covering a runtime failure of an implemented codec, which
keeps the clause live. I did not raise this as a finding: §17.4 states the
reasoning itself, so nothing is left open.

---

## 2. The concrete file, and the coverage walk arithmetic

### 2.1 Construction

One layer `L`, interleaved, linearization 1, codec 1 (none), filter 1 (none),
A = 0, S = 0, A_slab = 0, rank 2, C = 1.

* dims `y` (E = 4, T = 2), `x` (E = 4, T = 2) → G = (2, 2), N = ∏Gᵢ = 4, P = ∏Tᵢ = 4
* channel `v`, type 6 (uint8, element size 1), fill `00`
* addressed-tile count = N = 4 (interleaved, `[R-GEO-03]`)
* decoded size = P · Q where Q = ΣBᵢ = 1 → **4 bytes** (`[R-SER-02]`)
* codec 1 ⇒ each stored length MUST equal 4 (`[R-COD-04]`)
* tiles 0, 1, 3 stored; **tile 2 is the sentinel** `FF ×16 00 ×4` (`[R-IDX-02]`)
* index region = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 = 4·20 + 1·4 = **84** (`[R-CNT-17]`)
* one file-scope user-metadata record, encoding 1, document `{"tarn.title":"demo"}`
  (21 bytes) + terminal CRC-32C = 25-byte extent (`[R-CNT-25]`, §8.1)

I hand-computed the layer record's inline payload before coding it, as a check on
my reading of §7.4's packing ("fields are packed in table order with no alignment
or padding between them"):

```
name        1 + 1 =  2      d dim entries  2 × (1+1+8+8) = 36
layout             1        C chan entries 1 × (1+1+2+1+1) = 6
linearization      2        index_encoding             1
codec              2        entry_count                8
filter             2        crc_of_crc_array           4
A, S, A_slab      24        sub-records                0
rank d             1        ─────────────────────────────
channel count C    2        TOTAL inline_length = 91
```

The builder produced `inline_length = 91`. Layer record = 24 + 91 = 115 bytes;
user-metadata record = 24 + 1 = 25; record sequence = 140; directory region =
140 + 4 = **144**.

### 2.2 Live layout of generation 1

```
[0,16)      front signature block          16
[16,20)     stored tile 0                   4
[20,24)     stored tile 1                   4
[24,28)     stored tile 3                   4      (tile 2 = sentinel, no bytes)
[28,53)     user-metadata extent           25
[53,137)    tile-index region              84      = the layer record's extent
[137,281)   directory region              144
[281,320)   pre-trailer pad                39      SLACK
[320,384)   live trailer                   64
F = 384, F mod 64 = 0
```

Hexdump of the whole 384-byte file (my own construction, verified by the
verifier below):

```
00000000: 8954 4152 4e0d 0a1a 0000 0000 0000 0000  .TARN...........
00000010: 0a0b 0c0d 1415 1617 1e1f 2021 7b22 7461  .......... !{"ta
00000020: 726e 2e74 6974 6c65 223a 2264 656d 6f22  rn.title":"demo"
00000030: 7d74 f873 1210 0000 0000 0000 0004 0000  }t.s............
00000040: 0000 0000 00a1 1b8d bf14 0000 0000 0000  ................
00000050: 0004 0000 0000 0000 00d0 8382 03ff ffff  ................
00000060: ffff ffff ffff ffff ffff ffff ff00 0000  ................
00000070: 0018 0000 0000 0000 0004 0000 0000 0000  ................
00000080: 0097 425c 02f0 684e ef01 0003 005b 0000  ..B\..hN.....[..
00000090: 0035 0000 0000 0000 0054 0000 0000 0000  .5.......T......
000000a0: 0001 4c01 0100 0100 0100 0000 0000 0000  ..L.............
000000b0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000000c0: 0000 0201 0001 7904 0000 0000 0000 0002  ......y.........
000000d0: 0000 0000 0000 0001 7804 0000 0000 0000  ........x.......
000000e0: 0002 0000 0000 0000 0001 7606 0001 0001  ..........v.....
000000f0: 0400 0000 0000 0000 11fd bf27 0200 0200  ...........'....
00000100: 0100 0000 1c00 0000 0000 0000 1900 0000  ................
00000110: 0000 0000 01c9 566c c100 0000 0000 0000  ......Vl........
00000120: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000130: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000140: 8a4e 5241 540d 0a1a 0100 0000 0000 0000  .NRAT...........
00000150: 0100 0000 0000 0000 8900 0000 0000 0000  ................
00000160: 9000 0000 0000 0000 8001 0000 0000 0000  ................
00000170: efcd ab89 6745 2301 0000 0000 6a55 eff8  ....gE#.....jU..
```

Index entries, disk-ordinal order (`[R-IDX-01]`: entry k at region byte 20·k):

```
ordinal 0  10000000 00000000 04000000 00000000 a11b8dbf   off 16 len 4
ordinal 1  14000000 00000000 04000000 00000000 d0838203   off 20 len 4
ordinal 2  ffffffff ffffffff ffffffff ffffffff 00000000   SENTINEL
ordinal 3  18000000 00000000 04000000 00000000 97425c02   off 24 len 4
segment CRC array  f0684eef
```

### 2.3 The partition, and the arithmetic

§5.2 gives four classes and the front block: "the front signature block; or a
**structure** — a stored-tile extent, a record extent … the directory, or the
trailer". §9.7 tells the verifier exactly what to enumerate, and it is careful
about one thing that would otherwise be a double count:

> "A layer record's extent slot addresses that layer's tile-index region (§7.4),
> so the region enters the walk once, as that record's extent, and is not a
> second claimant beside it."

My claimant list for generation 1:

```
front block          16
stored tiles      3 × 4 = 12
umd extent           25
index region         84   (= the layer record's extent)
directory region    144
trailer              64
                    ───
claimed             345
F                   384
SLACK                39   = the pre-trailer pad [281,320)
```

The verifier reported exactly 345 / 39, matching the hand arithmetic. A second
build with a deliberate 6-byte hole between tiles 1 and 3 gave claimed 345,
F 384, slack 39 = 6 (hole) + 33 (pad), again matching by hand.

### 2.4 Which bytes are certified, and the third category

My charter asks which bytes are certified, which are counted-but-unconstrained,
and whether any byte can be neither. The document supports a sharper answer than
a two-way split, and I want to record it because the two-way framing hides a real
class:

1. **Certified** — claimed by the walk *and* covered by a checksum §8.1's map
   states, which the verifier verified: the trailer, the directory region, each
   tile-index region (entries via segment CRCs, the array via crc_of_crc_array),
   each stored tile (entry crc), each user-metadata extent (terminal 4 bytes).
   Plus the front block, certified by equality rather than checksum (§8.1 row 1).
   In my file: 16 + 64 + 144 + 84 + 12 + 25 = **345 bytes, all 384 minus slack**.
2. **Live but unconstrained** — the extent of a record of a type this
   specification has not assigned. §8.1's last row: "none — the bytes are
   opaque (§7.2)". Such an extent *is* claimed by the walk (§5.2's "record extent
   … whatever the record's type"), so it does **not** count toward the slack
   total, yet no checksum covers it and no content rule constrains it.
   §22.3 `[R-SEC-04]` says so outright: "corruption inside it is equally
   invisible". My file carries no such record, so this class is empty here, but a
   verifier must not report those bytes as certified.
3. **Slack** — counted, content unconstrained, MUST be reported as a total.

Can a byte be neither claimed nor slack? No, and §5.2's Note explains why the
answer is structural rather than empirical: "The live committed state is *defined*
as the front block plus what a complete coverage walk reaches, and `[R-LIF-08]`
makes every byte that walk misses slack — so 'belongs to no class' describes
nothing, and a register row for it would be a row no file could exhibit." I
checked this against the six *structural* rows of §15.3, which are the only way an
entry could nominally address bytes that the walk does not claim: each such entry
"contributes no stored extent to the walk … so any bytes it nominally addressed
that no other claimant claims fall to slack" (§9.7). The escape hatch "that no
other claimant claims" is load-bearing and correct: an entry with offset 8,
length 4 nominally addresses bytes inside the front block, which *is* claimed.

### 2.5 A walk that does not complete

I built two.

**(a) Stop at the directory CRC.** Corrupting the directory's terminal CRC gives
F20 at step 8. The walk has claimed only the front block and the trailer:

```
claimed = 16 + 64 = 80        F = 384
partial slack total = 304     true slack = 39
report: "PARTIAL — upper bound; walk stopped by F20 at file scope"
```

304 ≥ 39 ✓. This is what `[R-CNT-21]` demands: "A partial total is F less the
bytes claimed by the claimants the walk did enumerate — an upper bound on the
file's true slack, never an under-count — and a verifier reporting one MUST say
which scope or violation stopped the walk."

**(b) A layer-scope rejection that blocks enumeration.** I flipped a byte of
crc_of_crc_array and repaired the directory CRC, giving L37 (`[R-IDX-04]`,
reject-layer). `[R-ENC-05]` then forbids the verifier to act on any entry's
offset — "MUST NOT allocate, seek, or issue I/O based on any integer obtained
from a file before the checksum covering it has been verified" — so the three
stored extents cannot enter the walk. The index region itself still can: its
bounds come from the layer record's extent slot, which the directory CRC covered.

```
claimed = 16 (front) + 25 (umd) + 84 (index region) + 144 (dir) + 64 (trailer) = 333
F = 384    partial slack total = 51    true slack = 39
report: "PARTIAL — upper bound; walk stopped by L37 at layer 'L'"
```

51 ≥ 39 ✓, and it is tighter than 304, which is what §5.2 means by "tightening to
the exact total when the walk completes".

**Where I had to guess.** §9.7's clause is *"a scope-level rejection blocks
enumeration, or the verifier stops at the first violation"*. I read the first
disjunct restrictively — a scope-level rejection that *in fact* blocks
enumeration — rather than as an assertion that every scope-level rejection blocks
it. Under the other reading, a file whose only defect is, say, L35 (a bool fill
byte of `0x02`, reject-layer, but whose index chain verifies perfectly) forces a
*partial* total even though nothing prevented the walk from finishing. Both
verdicts are NONCONFORMING either way, but the two verifiers print different
slack totals for the same bytes, and §5.2 and §22.3 both say that number is the
operational output. Reported as **verifier-03**.

---

## 3. Extent overlap, alignment, and slab invariants, on adversarial layouts

All eight variants below were built and run; the outcomes are the verifier's
actual output.

### 3.1 Overlap

`[R-CNT-13]` splits overlap by scope, and §15.3's last three rows restate it:

> "a verifier MUST treat an intra-layer overlap — including a stored extent
> overlapping its own layer's index region or sub-record extents — as
> reject-layer, and any overlap across layers or touching another scope's
> structures as reject-file"

* **(A) intra-layer.** Tile 0 at [16,20), tile 1 at [18,22). Verifier: **L18,
  reject-layer**, plus T1 on tile 0 (whose bytes are now the overlap, so its crc
  fails). Correct: F33's row explicitly says it fires only for "two structures
  that do not belong to the same layer".
* **(B) cross-scope.** Tile 3 at [30,34), inside the file-scope user-metadata
  extent [28,53). Verifier: **F33, reject-file**. Correct — the umd record's
  extent is a *file*-scope structure, so this is "touching another scope's
  structures" even though the tile is a layer structure.

Two cases I resolved from the text rather than by testing, because they matter to
a real implementation:

* A layer's user-metadata *sub-record* extent overlapping that same layer's index
  region → **L18**, reject-layer (both are structures of one layer).
* A layer's sub-record extent overlapping the *top-level* user-metadata extent →
  **F33**, reject-file (layer structure vs file structure).

And one that is *not* F33's business: a claimant that runs into [0,16) or
[F−64,F). F33's row is explicit — "a claimant reaching the front signature block
or the live trailer is instead caught by the bounds rows F9/F10, F31/F32, L16/L17
and T8/T9, each at its own tier". I implemented the bounds check as a separate
pass and confirmed the row list is complete: directory (F9/F10), non-layer
top-level record extents (F31/F32), layer and sub-record extents (L16/L17),
stored-tile extents (T8/T9). Nothing else can be a claimant.

### 3.2 Alignment

* **(C)** A = 512 declared with tiles at 16, 20, 24 → three **L40**,
  reject-layer. Worth noting for an implementer: with A ≥ 512 and the
  offset ≥ 16 floor of §15.3, the smallest legal stored-tile offset in an aligned
  layer is 512, not 0 — offset 0 satisfies `offset mod A = 0` but is a T8
  structural reject.

`[R-SLB-01]` puts this squarely on the verifier: "A verifier MUST check the
invariant (violation: reject-layer, §15.3); readers are not obligated to —
offsets are always explicit, so alignment is reader-invisible."

### 3.3 Slabs

`[R-SLB-02]`/`[R-SLB-03]`. Runs partition each contiguous block of disk ordinals
independently; interleaved gives the single block [0,N).

* **(D)** S = 2, A_slab = 16, tiles at 16/20/24, ordinal 2 sentinel. Run 0 =
  ordinals {0,1}: first stored offset 16, 16 mod 16 = 0 ✓; packing 16 + 4 = 20 ✓.
  Run 1 = ordinals {2 (sentinel), 3}: the sentinel is transparent, so the run's
  first *stored* tile is ordinal 3 at offset 24, and 24 mod 16 = 8 → **L42**,
  reject-layer. This is the case worth building: without the transparency rule you
  would test ordinal 2's (nonexistent) offset and get the wrong answer.
* **(E)** Same with a 2-byte gap: tiles at 16/22/26. Run 0: 22 ≠ 16 + 4 → **L41**.
  Run 1: 26 mod 16 = 10 → **L42**. Both fire.

I want to record that §16.2's decidability claim holds up under implementation.
The rule has to be checkable from index bytes alone, and it is, because the two
transparency classes are exactly the two classes decidable from an entry's own 20
bytes plus F:

> "Sentinel tiles are transparent to run continuity … So are the entries §15.3
> classifies reject-tile on a *structural* ground … An entry whose only defect is
> that its stored bytes fail its crc is not transparent — its offset and length
> stand, and the packing relation reads them as it does any other stored tile's —
> so this invariant stays decidable from index bytes alone."

The crc case is the subtle one and the document gets it right: whether the crc
passes or fails, the entry participates identically, so the verifier never needs
the payload to decide continuity. A third class exists that the text does not
name — an entry that is well-formed and whose crc passes but which is reject-tile
under `[R-COD-04]` (codec 1, length ≠ decoded size, T14) or under §17.2's frame
rules. I resolved it by default: those entries are neither sentinel nor
`[R-IDX-03]`-structural, so they are not transparent, and their extents both
participate in run continuity and enter the coverage walk. The general rules
(§9.7's "the non-sentinel entries", §16.2's two named exceptions) decide it
without a special clause; I did not raise a finding.

### 3.4 The pre-trailer gap

* **(F)** Tile 0 relocated to [281,285), i.e. between the directory's end (281)
  and the trailer (320) → **F7**, reject-file, per `[R-CNT-05]`: "A verifier MUST
  treat a structure in that gap as a validity error at file scope, and counts the
  rest as slack". Note that the walk still completes (the tile is claimed), so the
  slack total stays *exact* at 39 — 35 pad bytes plus the 4 bytes the tile
  vacated. That combination — a file-scope violation with an exact slack total —
  is correct and is worth a vector.

I checked that a *superseded* structure can never land in this gap: the gap
belongs to the current commit (`[R-LIF-02]` step 5 appends pad and trailer last,
after the directory), and every earlier commit's bytes lie below this commit's
start at F_prev. So `[R-CNT-05]`'s check is over live claimants only, which is how
I implemented it.

---

## 4. Checksum obligations

### 4.1 Constants I reproduced locally

| Constant | Where | Stated | Computed | ✓ |
|---|---|---|---|---|
| CRC-32C(`"123456789"`) | §4.5, App. B | `0xE3069283` | `0xE3069283` | ✓ |
| CRC-32C(zero bytes) | §4.5, App. B | `0x00000000` | `0x00000000` | ✓ |
| CRC-32C of 2¹⁶ sentinel entries | §15.4 `[R-IDX-05]`, App. B | `0xEECB3BB2` | `0xEECB3BB2` | ✓ |
| Appendix A trailer CRC over [0,60) | App. A | `0xE00938D2` | `0xE00938D2` | ✓ |
| Appendix A directory region | App. A | `00 00 00 00` | CRC of 0 bytes = 0 | ✓ |

I also re-derived, by hand and then by code, every worked numeric example that a
verifier depends on:

* §11.4: (300,700) with T = (256,256) → tile (1,2), s = 1·8+2 = 10, in-tile
  ordinal 44·256+188 = 11,452; planar C = 4 → disk ordinal 2·32+10 = 74 ✓
* §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), CRC array 64
  bytes, region 20,000,064; entry 999,999 at segment-relative byte 339,180;
  segment 15 at [19,660,800, 20,000,000) ✓; full segment = 1.25 MiB ✓
* §15.4: planar C = 4, N = 32, channel 2 at s = 10 → ordinal 74, region bytes
  [1,480, 1,500) ✓; channel 3 entries 96–127 ✓
* §14.2: interleaved (2,3), uint8+uint16 → Q = 3, decoded 18, ordinal 5 at [15,18);
  planar `b` plane 12 bytes, ordinal 5 at 10–11; float32+bool → Q = 5, decoded 30,
  ordinal 5 at [25,30) ✓
* §14.3: planar bool P = 10 alternating → `55 01` (fill false) / `55 FD`
  (fill true, pad bits 2–7 set) ✓
* §14.5: extents (5,5) tiles (4,4), edge tile (1,1) = 1 real + 15 padding, uint16
  fill `0xABCD` → 32 bytes, values 1–15 each `CD AB` ✓
* §17.3 shuffle: three float32 → `00 00 00 00 00 00 80 00 40 3F 40 40` ✓
* §12.1 bfloat16 1.0 = `0x3F80` from binary32 `0x3F800000` ✓
* §12.3 channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` = 12 bytes ✓
* §20.3 example: 32-tile index region = 32·20 + 4 = 644 ✓; 10⁶ tiles ≈ 20 MB ✓
* §21.9 note: 2³² entries → 2¹⁶ segments × 4 = 256 KiB ✓; 2³⁶ → 4 MiB ✓

**Could not reproduce locally, and did not need to:** the zstd frame magic
`28 B5 2F FD` and the LZ4 frame magic `04 22 4D 18` (T23) are external constants
with no computation to check; RFC 1951/8878/LZ4-block conformance of a stream is
external-format behaviour. Nothing in §4.5's own check vector, §15.4's constant,
or Appendix A resisted local computation.

### 4.2 Is every live structure covered by a checksum?

**No, and the document says so twice.** §4.5's exception list and §8.1's map agree,
and I verified the list is exhaustive over the structures a major-1 file can hold:

| Live structure | Checksum | Class |
|---|---|---|
| front signature block | none — byte equality | excepted (§4.5, §8.1) |
| trailer bytes [0,60) | trailer CRC at [60,64) | covered |
| trailer CRC field itself | none | terminal |
| directory record sequence | directory region's final 4 bytes | covered |
| directory region CRC itself | none | terminal |
| layer record inline payload (incl. crc_of_crc_array) | directory CRC | covered; crc_of_crc_array is *interior* |
| sub-record header + inline payload | directory CRC | covered |
| tile-index entries | segment CRCs | covered; each entry's crc field is *interior* |
| segment CRC array | crc_of_crc_array | covered; *interior* |
| stored tile bytes | its entry's crc field | covered |
| user-metadata extent, less final 4 | those final 4 bytes | covered |
| user-metadata extent's terminal CRC | none | terminal |
| **extent of a record of an unassigned type** | **none** | **excepted — opaque** |
| slack | none | outside the live state |

§4.5's classification of the three *terminal* fields (trailer, directory-region,
user-metadata) and the three *interior* ones (segment CRC array, entry crc,
crc_of_crc_array) matches §8.1 exactly. The one hole — an unassigned type's
extent — is stated in §4.5, in §8.1's last row, in §7.2 ("opaque"), and in §22.3
`[R-SEC-04]`. It is a designed hole, not a defect, but it is the reason a verifier
cannot honestly say "every live byte is certified".

### 4.3 The chain, and what "before acting on" costs a verifier

§8.2's chain — trailer → directory → crc_of_crc_array → segment CRC array →
index segment → index entry → stored tile — is strict, and `[R-ENC-05]`'s
prohibition ("MUST NOT allocate, seek, or issue I/O based on any integer obtained
from a file before the checksum covering it has been verified") is what makes a
blocked walk blocked. I implemented it literally, which is what produced the
correct partial total in §2.5(b).

Unlike a reader, a verifier must verify *every* link, not only the links under
structures it reads: §9.7 requires "that each verifies against the checksum
covering it, where §8.1's map states one". So every stored tile's crc is checked
even for tiles no reader would ever fetch. That is the single biggest cost
difference between a reader and a verifier, and the document is unambiguous
about it.

---

## 5. Decoded-content obligations

### 5.1 What a verifier must decode

Three obligations force decode, and the register assigns all of them detector
*verifier*:

* **`[R-SER-05]` padding content** (T4): "at every padding position, a writer
  MUST encode, for each channel the position carries, that channel's fill value …
  a verifier MUST check it, and a violation is a validity error at tile scope."
  Forces decoding every stored tile that carries a padding position, i.e. every
  edge tile where Gᵢ·Tᵢ > Eᵢ for some i.
* **`[R-SER-05]` pad bits** (T5): "Every pad bit (§14.3) MUST carry the plane's
  channel's fill bit." Forces decoding every stored planar bool plane where
  P mod 8 ≠ 0. §14.3's note is emphatic that these are *not* padding positions:
  "A plane can have many padding positions and no pad bits."
* **`[R-SER-08]` interleaved bool bytes** (T2): forces decoding every stored tile
  of an interleaved layer carrying a bool channel.

T26 (mis-strided filter 2) needs no separate procedure: "the check that detects it
is T2's or T4's".

Beyond those, a verifier decodes every stored tile anyway, because T3
(`[R-SER-07]` exact decoded size), T24 (`[R-COD-08]` exact consumption) and T25
(malformed stream) are file-level requirements over tile bytes, and §2.3 obliges
the verifier to check every file-level requirement.

**What it compares against.** Never against stored data. §14.2/§14.3's decoded
size is "a function of the layer's declarations alone — geometry, layout, and
channel types — never of payload content, and readers allocate from those
declarations, not from stored data" (`[R-SER-07]`). Under codec 3 the frame's
content-size field, if present, must *equal* that number but "a reader MUST NOT
allocate or size any buffer from it" (`[R-COD-06]`). My verifier derives dsize
from declarations and treats any embedded size as a value to compare, never to
size with. In my test file, dsize = P·Q = 4, and the codec-1 equality of
`[R-COD-04]` made T14 checkable from the entry alone, before any payload fetch.

**What it is permitted to skip.** Exactly three things, all of which convert the
verdict to *cannot establish* rather than licensing certification:

1. A codec or filter it cannot execute (`[R-COD-11]`, §17.4).
2. A layer's or tile's decode declined on resource grounds
   (`[R-ERR-04]`, §21.9) — the refusal "MUST be reported as a resource limit and
   not as a validity error".
3. A user-metadata document it declines to decode on its own size bound
   (`[R-MTA-09]`).

And it is permitted to skip *nothing* on the ground that no witness exists: §21.7
closes this cleanly — "None of these is a requirement a verifier is *unable to
check* within the meaning of `[R-CNF-11]`: no file-level witness exists to check,
so nothing about the file is left undetermined and the verdict is unaffected."
A file whose writer used a mis-strided filter with no padding position, or an
undisclosed zstd dictionary, is **certified**. That is stated, deliberate, and I
implemented it that way.

### 5.2 The one byte a conforming file cannot carry

`[R-SER-08]`'s reader-side rule ("MUST report 0x00 as false and every other byte
as true") is a reader rule and imposes nothing on the verifier, which must
*reject* the tile rather than interpret it. I checked that T2 and T4 jointly
cover `[R-SER-08]`, as T2's row claims: a bad bool byte at a padding position is
always caught by T4, because the fill byte itself is constrained to `0x00`/`0x01`
by `[R-TYP-07]`, so any padding byte outside {0,1} necessarily differs from the
fill. The claim holds.

---

## 6. The multi-generation trace

Four states, verified after each. All appends satisfy `[R-LIF-01]` — I asserted
byte-identity of the committed prefix in code at each step, and every assertion
passed.

### Generation 1 — creation (`[R-WRT-02]`)

Layout as in §2.2. Commit path: front block; payloads and index; directory + CRC;
barrier; pad; trailer (generation 1, fresh nonzero file_id `0x0123456789ABCDEF`);
barrier.

```
VERDICT: CONFORMING     F = 384    slack 39 (10.2%), exact
```

### Generation 2 — append: supersede stored tile 1 (`[R-WRT-04]`)

New payload at 384; the layer's **whole** index region re-emitted at 388 (one
entry re-pointed, three byte-identical — including the sentinel); the
user-metadata record re-emitted byte-identically, extent slot still (28, 25),
which is `[R-WRT-05]`'s preservation and §20.3's shape (b).

```
new tile 1 [384,388)   index' [388,472)   dir [472,616)   pad [616,640)   trailer [640,704)
VERDICT: CONFORMING     F = 704    slack 359 (51.0%), exact
```

Slack check by hand: old tile 1 (4) + old index (84) + old dir (144) + old pad
(39) + old trailer (64) + new pad (24) = **359** ✓. This is the §20.3 note's point
made concrete: superseding four bytes of payload cost 84 bytes of re-emitted index
plus 144 bytes of re-emitted directory.

### Generation 3 — update: edit the user-metadata document

New extent appended (two keys, sorted ascending by UTF-8 bytes per `[R-MTA-05]`:
`tarn.creator` < `tarn.title`); the old extent becomes slack. The **layer record
is byte-identical**, extent slot still (388, 84) — the commit touches no tile and
no index content, so §20.3's "A layer whose record alone changes keeps its extent
slot" applies a fortiori. §20.3's shape (c) note is explicit that a metadata edit
is not the directory-only shape: "its document lives in an extent (`[R-CNT-25]`),
so a new extent is appended and the old one becomes slack, as in (b)."

```
umd' [704,760)   dir [760,904)   pad [904,960)   trailer [960,1024)
VERDICT: CONFORMING     F = 1024   slack 648 (63.3%), exact
```

Slack check: 359 + old umd (25) + old dir (144) + old trailer (64) + new pad (56)
= **648** ✓ (generation 2's pad was already counted in the 359).

### Compaction (`[R-WRT-06]`, `[R-WRT-07]`, `[R-WRT-09]`)

Output carries only the live state of generation 3, repacked; **fresh file_id**
`0x7766554433221100` and **generation 1**; every stored tile's bytes and every
entry crc byte-identical; extent slots re-pointed; the index region regenerated
(offsets new, lengths/crcs/sentinels unchanged, segment CRCs recomputed) and
crc_of_crc_array updated. The user-metadata extent is carried verbatim.

```
tiles [16,28)   index' [28,112)   umd [112,168)   dir [168,312)   pad [312,320)   trailer [320,384)
VERDICT: CONFORMING     F = 384    slack 8 (2.1%), exact
```

`[R-WRT-07]`'s equality obligation — "The output's reference arrays MUST equal the
live generation's bit for bit" — holds by construction: the same three stored
payloads, the same sentinel at ordinal 2, the same fill `0x00`.

**Verification depth I had to implement for the compactor.** `[R-WRT-09]` is
stronger than an appender's: "it relies structurally on every structure it copies,
so it MUST verify each link of the chain — the open (§19.1), each retained layer's
record (§19.3) and full index chain (`[R-IDX-04]`), and each relocated extent's
checksum, including every stored tile's entry crc — before emitting that
structure's bytes." That is a verifier-grade walk minus decoded content
(`[R-WRT-06]`: "its verification depth is `[R-WRT-09]`'s and reaches no decoded
content"). So a compactor is a verifier that stops before §14 — a useful thing to
have written down and it *is* written down.

### Certification results across the trace

| Generation | F | verdict | slack | note |
|---|---|---|---|---|
| 1 (create) | 384 | CONFORMING | 39 exact | pad only |
| 2 (append, supersede) | 704 | CONFORMING | 359 exact | 51% waste after one 4-byte edit |
| 3 (metadata update) | 1024 | CONFORMING | 648 exact | 63% |
| compacted | 384 | CONFORMING | 8 exact | 2% |

---

## 7. Places where the document decided things I expected to have to guess

Recorded because a "found nothing" walk is worth less than a walk that says where
it was carried:

* **The register-vs-rule trap.** F36 and L25 carry outcome *reject-file* /
  *reject-layer* while `[R-CNT-15]` has a reader *ignore* an MU = 0
  reserved-range record. §21.1 pre-empts this exactly: "For a row whose Detector
  is *verifier*, the outcome names the scope at which the damage is recorded, not
  an obligation on any reader". No ambiguity survives.
* **`[R-CNT-05]`'s longer pre-trailer gap.** "a longer gap is conforming, and no
  conforming commit produces one" reads paradoxical until §2.3's conduct/predicate
  split is applied. It is consistent.
* **§21.8's arithmetic.** I counted the register by hand under §21.1's instance
  rule ("a cell reading — is one instance; the count is therefore mechanical once
  the cell is written"): F = 53, L = 106, T = 45, R = 44 → **248** instances over
  36 + 49 + 26 + 10 = **121** conditions. Both match §21.8 exactly. §21.2–§21.5's
  stated per-table counts also match their row counts.
* **§4.7's closure claim.** "In format major 1 `fill` is the only semantic field
  and `version_minor` the only descriptive one." I grepped every layout table:
  the only non-`structural` class cells in the document are line 716
  (version_minor, descriptive) and line 1616's prose (fill, semantic). The claim
  is true of what the document contains.
* **§21.1's completeness claim.** I walked every MUST in the document looking for
  a *detectable* file-conformance violation the register omits, including
  `[R-CNT-05]`, `[R-CNT-02]`, `[R-CNT-18]`'s nesting bar, `[R-SLB-04]`'s stale
  slab declaration, `[R-EXT-03]`'s reserved values in all eight spaces,
  `[R-IDX-05]`'s partial-segment rule, `[R-MTA-04]`'s four restrictions, and
  `[R-COD-06]`'s six frame constraints. Every one is either registered, explained
  as witness-free (§21.7, or the §7.4 and §16.2 notes), or a conduct rule
  `[R-CNF-02]` carves out. I found no gap.
* **§21.9's two guarantees are jointly satisfiable.** 65,536 layers at the minimum
  layer record (24 + 73 = 97 bytes) is 6.06 MiB, inside the 16 MiB directory
  guarantee. Worth checking because a pair of guarantees that cannot both hold
  would make `[R-CNF-03]` unsatisfiable.
* **A verifier and `[R-CNT-03]`.** A verifier *can* observe that the pre-trailer
  pad is nonzero, and §5.2's "A reader MUST NOT interpret it" does not obviously
  bar emitting an advisory. `[R-CNF-12]` says a SHOULD deviation is "an advisory
  that does not bar certification", so nothing turns on the choice and I did not
  raise it as a finding. My implementation does not check.

---

## 8. Findings

Six. Each carries its quotation and section. None of them, on my reading, changes
which byte sequences a conforming writer may emit or which files a conforming
*reader* must accept or reject; two of them (01, 02) change what a *verifier*
prints, which is the closest any of them comes to the byte-level bar, and I say so
explicitly rather than upgrading them.

---

### verifier-01 — AMBIGUITY — §6.1 `[R-CNT-04]`, §2.3 `[R-CNF-11]`, §9.7 `[R-LIF-08]`, §21.2 F6, Appendix H

**May a verifier whose open leaves bytes [0,16) non-resident omit the front-block
equality check and still certify?**

§6.1 grants the omission to readers, and a verifier is a reader:

> "A reader that would have to issue a further range request to obtain those bytes
> MAY defer or omit the check: its open path is anchored at the trailer (§6.2),
> and the two-request accounting of §6.4 does not include the front block."
> `[R-CNT-04]`

F6's row repeats it — "the obligation binds a reader holding those bytes resident,
and a reader that would have to fetch them MAY defer or omit the check
(`[R-CNT-04]`)" — with detector *reader*, not verifier. §9.7 claims the block for
the walk but routes explicitly around checking it:

> "It checks that these occupy disjoint byte ranges, that each lies within
> [16, F − 64), and that each verifies against the checksum covering it, **where
> §8.1's map states one** (§8.1)."

and §8.1's map states, for the front signature block, "none — checked by byte
equality (§6.1)". Appendix H's verifier checklist enumerates nine "checks readers
are exempt from" and the front block is not among them.

**Permitted readings.** (a) The verifier inherits the reader's deferral and may
certify a remote file whose bytes [0,16) it never fetched. (b) §2.3's verifier
definition overrides: "A reader that additionally checks every file-level
requirement — **including those ordinary readers are exempted from** — and
certifies conformance." §6.1's "Writers MUST emit exactly these 16 bytes" is a
file-level requirement, and this is precisely a case where an ordinary reader is
exempted.

**I picked (b)** and made the front-block equality check unconditional in the
verifier, before any other processing. The phrase "including those ordinary
readers are exempted from" has no other obvious referent, and reading (a) lets a
verifier issue a certificate over 16 bytes it never looked at, which contradicts
"certifies only violation-free files" (`[R-CNF-12]`).

**What an implementer does wrong without it.** A remote verifier written from F6
and Appendix H alone certifies a file whose front block is corrupt or
byte-reversed — the exact condition F1 and F6 exist to catch, and the one §6.1's
rationale says the signature is engineered against.

---

### verifier-02 — AMBIGUITY — §18.2 `[R-MTA-03]`/`[R-MTA-09]`, §2.3 `[R-CNF-11]`, §21.6

**A user-metadata record declaring an experimental-range (≥ 0x80) document
encoding: does the verifier report *conforming* or *cannot establish*?**

§21.6 settles the file's status:

> "| A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming — §10.3's
> prohibition binds a writer's conduct, not the bytes | `[R-MTA-03]`,
> `[R-EXT-03]`, `[R-CNF-02]` |"

But no verifier can decode such a document, so it can check neither
`[R-MTA-04]`'s content rules nor `[R-MTA-05]`'s member ordering (F27/L48, both
detector *verifier*). §2.3 lists among the *cannot establish* grounds, without
qualification:

> "or when it declines to decode a user-metadata document (`[R-MTA-09]`)."

whereas §18.2's `[R-MTA-09]` itself scopes its clause to the resource bound: "A
**verifier** that declines to decode a document **on the bound above** cannot
establish that document's conformance and MUST NOT certify the file".

**Permitted readings.** (a) *cannot establish*: the verifier declines to decode a
document; §2.3's bare clause fits; the analogy `[R-MTA-09]` draws to
`[R-COD-11]`'s "codec it cannot execute" fits too. Consequence: a class of files
§21.6 calls conforming can never be certified by any verifier, ever — unlike every
other *cannot establish* ground, which is one verifier's capability limit.
(b) *conforming*: no requirement is left unchecked, because `[R-MTA-04]` and
`[R-MTA-05]` are predicated on a decoded document ("**The decoded document** is a
JSON text as defined by RFC 8259"), and under an unassigned encoding no decoded
document exists.

**I picked (b)**, on the parallel the document itself draws for record types: an
unassigned record type's extent is "opaque (§7.2)", covered by no checksum and
constrained by no rule, and a file carrying one with MU = 0 is certifiable
(§21.6, §8.1). An undecodable document is the same shape — no rule has a subject
— and §21.6's closing paragraph enumerates the *two* structural cases of
"conforming files a reader nevertheless refuses" without adding a third for
verifiers.

**What an implementer does wrong without it.** Two verifiers print different
verdicts — *conforming* vs *cannot establish* — over identical bytes that §21.6
declares conforming. No reader's accept/reject changes and no writer's bytes
change, which is why I do not call it byte-level; but "what bars certification" is
the verifier's whole output, and this is the one place I could not settle it from
a single sentence.

---

### verifier-03 — AMBIGUITY — §9.7 `[R-LIF-08]`, §5.2 `[R-CNT-21]`, §22.3 `[R-SEC-03]`

**Does every layer-scope rejection make the coverage walk partial, or only one
that actually blocks enumeration?**

> "Where the walk does not complete — **a scope-level rejection blocks
> enumeration**, or the verifier stops at the first violation (`[R-CNF-11]`) —
> the sum is reported as partial, and `[R-CNT-21]` governs what such a total
> counts and what the verifier reports beside it." §9.7

**Permitted readings.** (a) Restrictive: the clause names "a scope-level rejection
[that] blocks enumeration", so a rejection which leaves the index chain verifiable
does not make the walk partial. (b) Assertive: "a scope-level rejection blocks
enumeration" states a fact, so *any* reject-layer or reject-file makes the total
partial.

The two diverge on a concrete file. Take my generation-1 file with the bool fill
byte changed to `0x02` (L35, reject-layer, `[R-TYP-07]`) and nothing else wrong:
the layer record parses, crc_of_crc_array and the segment CRC verify, and all
three stored extents are enumerable. Reading (a) gives an **exact** total of 39;
reading (b) gives a **partial** total of at least 51 (claiming the index region
but not the tiles), or 304 if the verifier abandons the layer record entirely.
Both verifiers report NONCONFORMING; both are honest; the numbers differ by
almost an order of magnitude.

**I picked (a).** "Blocks" is doing work that "a scope-level rejection makes the
walk partial" would not need, and `[R-ENC-05]` supplies exactly the mechanism by
which some rejections block and others do not: a verifier "MUST NOT allocate,
seek, or issue I/O based on any integer obtained from a file before the checksum
covering it has been verified", which bites for L37/L38/L23 and not for L35.

**What an implementer does wrong without it.** The slack total is a MUST-report
field and, per §5.2 and §22.3, the operational output of the whole exercise —
"the number that distinguishes a working file from a padded one", "what tells an
operator to compact". Two conforming verifiers giving 39 and 304 for the same
file, with no way for the operator to tell which is the file's property, defeats
that. Note also that §22.3's restatement names only one of §9.7's two causes ("a
verifier that stopped early reports it only as partial"), which nudges a reader
toward reading (a) without settling it.

---

### verifier-04 — AMBIGUITY — §20.4, Appendix H (updater checklist)

**Can a commit remove a layer's user-metadata *sub-record*?**

§20.4, immediately after its obligations table:

> "No commit therefore removes a layer record or a **file-scope** user-metadata
> record. Both registered types carry PE = 1, and an in-place removal would
> strand that layer's stored tiles and index region as slack (§5.2) …"

Appendix H, stating the same obligation:

> "never removes a layer record, or a user-metadata record **at either scope**
> (§20.4)"

**Permitted readings.** (a) §20.4's sentence is an exhaustive list of what no
commit removes, so a *layer-scope* user-metadata sub-record may be dropped.
(b) §20.4's sentence under-states its own premise, and Appendix H states the rule
at its true scope.

**I picked (b).** The premise in the same sentence — and the paragraph above it —
decides it: "For a type §7.3 registers, the registry's fixed flags govern rather
than the stored ones (`[R-CNT-22]`) — **both registered types carry PE = 1, so
neither can be dropped**, and implementing a record's type confers understanding
of it, not permission to drop it." §7.3's registry fixes type 0x0002 at
MU = 0, PE = 1 for both of its scopes ("file when top-level; layer as
sub-record"), so the drop bar reaches a sub-record. Reading (a) would also require
§20.4's MU = 0 / PE = 0 table row — which carefully spells out when a *layer
sub-record* may be dropped — to be governing a case that cannot arise for the only
registered sub-record type, which it plainly is not.

**What an implementer does wrong without it.** An updater carrying forward a layer
that has a `tarn.axes` document drops it on any commit that touches the layer, and
the application state disappears — the exact failure §20.4's last table row calls
out ("unreported, application state disappears with no diagnostic"). The bytes an
updater emits differ; the resulting file is conforming either way, and §20.4's own
premise sentence already decides which one a conforming updater may emit, so I do
not claim this forks bytes.

---

### verifier-05 — OBSERVATION — Appendix H (verifier checklist) vs §14.5 `[R-SER-05]`, §14.3, §21.4 T5

**Appendix H's verifier checklist omits pad bits from the decoded-content
obligations, naming the two things §14.3 insists are different mechanisms.**

Appendix H:

> "alignment and slab invariants (§16); decoded-content obligations — **padding
> samples and interleaved boolean bytes** (§14.5, §14.2); user-metadata member
> ordering (`[R-MTA-05]`, §18.2)"

§14.3's note, defining the distinction the checklist elides:

> "**Note.** Pad bits are not padding positions (§11.3). A padding position is a
> whole sample position outside the layer's extents, arising in any layout; pad
> bits are a packed plane's final-byte unused high bits, arising only when P is
> not a multiple of 8. A plane can have many padding positions and no pad bits —
> §14.5 gives both their content."

The obligation exists (`[R-SER-05]`: "Every pad bit (§14.3) MUST carry the plane's
channel's fill bit") and the register carries it as its own row, T5, detector
*verifier*, detection *certification*. So the checklist's three-item list of
verifier-only decoded-content checks — padding samples (T4), interleaved bool
bytes (T2), and nothing else — is missing one of four (T4, T5, T2, T26; T26 is
detected *by* T2/T4 and needs no separate entry, T5 does).

Decidable, but only by cross-reading Appendix H against §21.4's table row by row,
which is the disproportionate part. Appendix H is non-normative and disclaims
itself — "each entry's authority is the requirement or section cited, never this
summary" — and it does cite §14.5, which covers pad bits. So nothing is
underdetermined; the audit aid just fails to enumerate a check for an implementer
auditing against it, which is the one thing it is for. A planar bool layer with
P mod 8 ≠ 0 is the common case (any tile whose ∏Tᵢ is not a multiple of 8), so
this is not an exotic corner.

---

### verifier-06 — AMBIGUITY — Appendix G item 3

**Appendix G's "total emission order" is not total.**

> "3. **A total emission order, contiguously.** For each layer in ascending
> layer-name byte order: its stored tiles in disk-ordinal order, then its
> tile-index region; then any record extents in ascending record order; then the
> directory. Records are ordered by type, and within type 0x0001 by layer name; a
> layer record's sub-records are ordered by type, and within a type by their
> encoded bytes compared lexicographically — an order a reader can derive, which
> a creation order is not"

Two gaps, both reachable:

1. **Two top-level records of the same unassigned type.** The order given is "by
   type, and within type 0x0001 by layer name". Type 0x0002 admits at most one
   top-level record (`[R-CNT-14]`), so it needs no tiebreak — but an unassigned
   type does not, and a file may carry any number of them (multiplicity rules are
   per type, and §7.2 states none for unassigned types). Two records of type
   0x8001 with distinct extents have no defined relative order, so their extents'
   offsets are not fixed by the profile.
2. **Sub-record extents against top-level record extents.** "then any record
   extents in ascending record order" must cover a layer's user-metadata
   sub-record extent, since a sub-record is a record and its extent is a
   claimant. But the ordering rule ranks sub-records only *within a layer
   record*, never against top-level records. Under a second reading, "any record
   extents" means top-level extents only and sub-record extents have no stated
   position at all.

**I picked** the reading that sub-record extents follow their own layer record in
the global record order and that unassigned-type ties are unresolved, and noted
that a writer adopting the profile must add its own tiebreak (encoded-bytes
lexicographic, as the sub-record rule already uses) to get byte-identity.

**What an implementer does wrong without it.** Two writers both adopting the
profile, given the same input file carrying a file-scope document and a
layer-scope document, emit those two extents in different orders and produce
different bytes — which is the one thing the profile exists to prevent, and which
its own preamble says can be "refuted cheaply but confirmed only by reproducing
the file". Not byte-level for TARN conformance: Appendix G is non-normative and
"adds no requirement to any actor", so both outputs are equally conforming files
and no reader's verdict changes.

---

## 9. Confidence

**Medium-high.** I implemented the certification procedure, the coverage walk with
exact and partial totals, extent overlap at both scopes, alignment, slab runs with
sentinel and structural-reject transparency, the index chain, and a four-generation
lifecycle, from this document alone, and every constant and worked example I could
compute locally reproduced. Two conforming implementations built from this text
would agree on every byte and every reader verdict I tested. Where they would
diverge is confined to a verifier's own output: whether a certificate issues for a
file with an experimental metadata encoding (verifier-02), whether a slack total
prints as exact or partial after a non-blocking layer rejection (verifier-03), and
whether a remote verifier checks 16 bytes (verifier-01). I mark none of the six
byte-level, and I would rather be told I under-claimed than have padded the
count — but I would defend verifier-02 and verifier-03 as real forks in the
verifier's contract, which is this round's charter.
