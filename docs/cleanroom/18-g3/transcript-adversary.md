# Round 18 — Adversary transcript

**Role:** Adversary. **Charter:** construct a file two conforming verifiers could
judge differently; failing that, show for each attack which sentence forecloses it.

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–4340 (the whole document). I ran `grep`
against that same file only, and Python that reads no project file. I wrote
scratch files under my own scratchpad (`work/tarn.py`, `work/build.py`,
`work/planar.py`, `good.tarn`, `minlayer.tarn`) and this transcript. I did not
open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`CONTRIBUTING.md`, `conformance/`, `spec/registry.json`, or any git history; I
ran no `git` command, no web search, no web fetch, and did not list the output
directory. Prior knowledge of other array formats was used only to generate
suspicions, never to settle one.

---

## 1. Ground truth first: does the document's own arithmetic hold?

Before attacking I implemented enough of the format to know I was reading it
right. §4.5 fixes CRC-32C (Castagnoli 0x1EDC6F41, reflected in/out, init
0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian). I built the reflected
table from 0x82F63B78 and checked the document's own check vector:

| Claim | Section | Computed | Match |
|---|---|---|---|
| CRC-32C(`"123456789"`) = 0xE3069283 | §4.5 | `0xe3069283` | yes |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | `0x0` | yes |
| Appendix A trailer CRC = 0xE00938D2 | App. A | `0xe00938d2` | yes |
| §7.4 example: seg CRC over 80 sentinel bytes = 0x80A34955 | §7.4 | `0x80a34955` | yes |
| §7.4 example: crc_of_crc_array = 0xC4EE982E | §7.4 | `0xc4ee982e` | yes |
| CRC of a full 2¹⁶-sentinel segment = 0xEECB3BB2 | §15.4, App. B | `0xeecb3bb2` | yes |

I then reproduced Appendix A's 128 bytes from the field table alone and got the
listed hex line for line. That matters more than it looks: it means §6.2's
layout table, §7.1's empty-directory rule, and [R-CNT-27]'s 128-byte floor are
mutually consistent at the smallest point in the format's domain. I re-derived
the floor independently: dir_offset ≥ 16, dir_length ≥ 4, dir_offset +
dir_length ≤ F − 64 gives F ≥ 84; F ≡ 0 mod 64 gives F ≥ 128. Tight.

I checked every other worked number in the document by hand or by script:

- §11.2: G=(4,8), N=32, P=65536 for extents (1024,2048), tiles (256,256); and
  G_y = ⌈1000/256⌉ = 4. Both right.
- §11.4: (300,700) → tile (1,2) → s = 10; in-tile (44,188) → 44·256+188 = 11,452;
  planar channel 2 → 2·32+10 = 74. All right.
- §14.2: (2,3) P=6, uint8+uint16 → Q=3, size 18, ordinal 5 at [15,18); planar `b`
  12 bytes, ordinal 5 at 10–11; float32+bool → Q=5, size 30, sample at [25,30).
  All right.
- §14.3: P=10 alternating → `55 01` with fill false, `55 FD` with fill true. I
  reproduced both from my packer.
- §14.5: extents (5,5) tiles (4,4) → edge tile (1,1) has 1 real and 15 padding
  positions, 32-byte tile. Right.
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC
  array, region 20,000,064; entry 999,999 at segment-relative 339,180; segment 15
  at [19,660,800, 20,000,000); full segment 1.25 MiB. Every figure right.
- §17.3: shuffle of `00 00 80 3F 00 00 00 40 00 00 40 40` at s=4. My
  implementation emits `00 00 00 00 00 00 80 00 40 3f 40 40` — the document's
  example byte for byte.
- §21.9's Note: 2³² entries → 2¹⁶ segments × 4 B = 256 KiB; 2³⁶ → 4 MiB. Right.

**Nothing in the document's arithmetic is wrong.** I looked for the classic
off-by-one in ⌈entry_count / 2¹⁶⌉ × 4 at entry_count = 0, 1, 65,536 and 65,537
and the formula, §15.4's segment bounds and §15.4's own example agree at all
four.

## 2. Building the thing

**File 1 — a real layer.** Rank 1, dim `x` extent 100, tile extent 32 → G=4,
N=4, interleaved, one float32 channel `temp`, fill `0x7FC00000`, codec 1, filter
1. Decoded size P·Q = 32·4 = 128. Tile 3 covers coordinates 96–127, of which
100–127 are padding positions and must carry the fill bytes ([R-SER-05]). Layout
came out:

```
[   16,   144)  128  tile0        [  528,   612)   84  index (4·20 + 4)
[  144,   272)  128  tile1        [  612,   667)   55  user-metadata extent
[  272,   400)  128  tile2        [  667,   801)  134  directory
[  400,   528)  128  tile3        [  801,   832)   31  pre-trailer pad
                                  [  832,   896)   64  trailer      F = 896
```

F ≡ 0 mod 64, the pad runs to the next 64-boundary (§6.2: a directory ending on
a boundary leaves none — that disambiguates [R-LIF-02] step 5's "the next
64-byte boundary", which alone would not tell you whether to emit 0 or 64 bytes).
Coverage partitions: front 16, four tiles, index region (the layer record's
extent), the metadata extent, directory, trailer; slack = 31, the pad only.

**File 2 — the awkward one.** Planar, rank 2, E=(5,5), T=(3,3) → G=(2,2), N=4,
P=9. C=2: `m` bool (packed plane, ⌈9/8⌉ = 2 bytes, one value bit and seven pad
bits in byte 1) and `v` uint16 (18 bytes). Addressed tiles = C·N = 8; disk
ordinals 0–3 are `m`, 4–7 are `v` (§11.4's c·N + s). Filter 2 (byte-shuffle)
with stride 1 on the bool planes — identity, per [R-COD-10] — and stride 2 on
the uint16 planes. Slab S=2, A_slab=1: runs are [0,2),[2,4) in block 0 and
[4,6),[6,8) in block 1, never spanning the channel-block boundary ([R-SLB-02]).
Every plane round-tripped through shuffle/unshuffle. Pad bits carry the fill bit;
padding positions carry the fill bit in the packed plane and the fill bytes in
the uint16 plane.

I hit **no guess point** building either file. Every field width, every
derivation and every content obligation was stated. The two places I expected to
guess and did not:

- *Which stride the filter uses in a planar layer with mixed types.* §17.3 says
  the channel's element size for a planar tile — so different tiles of one layer
  filter at different strides, and packed bool planes at s = 1 (identity). Stated.
- *Whether pad bits are padding positions.* §14.3's Note separates them
  explicitly and §14.5 gives both their content.

**File 3 — degenerate but legal.** The smallest file carrying a layer: rank 1,
extent 0, tile extent 1. G = ⌈0/1⌉ = 0, N = 0, entry_count = 0, extent slot
(0,0), crc_of_crc_array = 0. inline_length 73, record 97, dir_length 101, pad 11,
F = 192. Verifier slack total = 192 − (16 + 101 + 64) = 11. It reads back clean.

## 3. The attacks

I ran the charter's surfaces and my own. Below, each attack, the two candidate
verdicts, and the sentence that forecloses it.

### 3.1 Boundary values

- **entry_count = 0 with a nonzero extent slot / entry_count > 0 with (0,0).**
  Both are L22 instances, verbatim ("including slot (0,0) with entry_count > 0,
  or a nonzero slot with entry_count = 0"). Foreclosed. The `(X, 0)` form is
  additionally L15. The only legal shape at entry_count = 0 is (0,0), and
  crc_of_crc_array must be 0 (L27) — which is also what CRC-32C of a zero-length
  segment array computes to, so the forced value and the computed value agree.
- **A zero-extent layer declaring codec 4 with a tile shape whose decoded size
  exceeds 0x7E000000.** Verifier A: L44 fires. Verifier B: the layer addresses no
  tile, so nothing is measured. Foreclosed by §17.2's Note, which is explicit and
  goes further than it needs to: "a layer that addresses none … satisfies it
  whatever its tile shape declares, and codec 4 is conforming there. … `[R-ENC-04]`'s
  overflow rule carries no such quantifier … so P·Q and P·Bᶜ are checked in an
  empty layer even though this cap is not." L44's own text says *addressed*.
  Both verifiers certify.
- **Products that overflow.** N, P, N·P, C·N, P·Q, P·Bᶜ, entry_count·20 + …
  L2 lists nine instances and [R-ENC-04] binds "any quantity this specification
  defines as a sum or product". I checked that L2's parentheticals are true:
  C·N ≥ (C−1)·N + (N−1) and P·Q ≥ P·C (since Q = ΣBᵢ ≥ C). They are.
- **Extent ending exactly at F − 64.** Legal everywhere: [R-CNT-13] says
  "extending past F − 64", L17/T9/F32 say "> F − 64", §6.2 says "≤ F − 64".
  Four statements of one boundary, all on the same side. Foreclosed.
- **A pre-trailer gap longer than one pad.** §6.2: "a longer gap is conforming,
  and no conforming commit produces one" — and §2.3 names this as one of exactly
  two declared conduct-not-predicate cases. Both verifiers certify. Foreclosed.

### 3.2 Two structures claiming the same bytes

I enumerated every pair of claimant kinds against [R-CNT-13]'s three-way scope
split and F33/L18:

| Overlap | Rule says | Row |
|---|---|---|
| two stored tiles of one layer | reject-layer | L18 |
| stored tile × its own layer's index region or sub-record extent | reject-layer | L18 |
| across two layers | reject-file | F33 |
| layer structure × directory / top-level record extent | reject-file | F33 |
| two non-layer structures | reject-file | F33 |
| claimant reaching [0,16) or [F−64,F) | bounds rows, at their own tier | F9/F10, F31/F32, L16/L17, T8/T9 |

F33's own text names that last escape and lists all four tiers. I checked the
list is complete against §5.2's claimant classes — directory, top-level record
extent, layer record extent (the index region), sub-record extent, stored-tile
extent — and it is. No gap.

The sharpest construction here: **an index entry pointing inside the live
directory region, with a crc correctly computed over those directory bytes and a
length equal to the decoded size under codec 1.** A conforming reader passes the
index chain, classifies the entry as well-formed (offset ≥ 16, length ≠ 0,
offset+length ≤ F−64), verifies the crc, decodes, and returns directory bytes as
samples. It is not obliged to detect the overlap — [R-CNT-13] says so in
parentheses: "readers are not obligated to detect overlap, which requires
whole-directory knowledge". A verifier detects F33. That is the reader/verifier
seam working exactly as advertised, and **both verifiers report nonconforming**.
Not a fork.

### 3.3 Every record flag and type combination, in every position

I walked the cross product of {top-level, layer sub-record} × {0x0000, 0x0001,
0x0002, reserved 0x0003–0x7FFF, experimental ≥ 0x8000} × {MU, PE} × reserved
bits. Results:

- type 0 → F24 / L13. Type 0 is expressly "not an unknown type".
- registered type with a stored flag differing from §7.3 → F28 (non-layer,
  file scope) / L49 (layer record or registered sub-record, layer scope). The
  scope split matches §7.2's "the layer for a layer record and for sub-records,
  the file for other top-level records". Readers apply fixed semantics regardless
  ([R-CNT-22]); verifiers report. Consistent.
- reserved-range type, MU = 1 → F35 (reader, open) / L24; MU = 0 → F36 / L25
  (verifier, certification). §21.1 names F35 of F36 and L24 of L25 as strict
  specializations and says the narrower row's detector and detection point apply.
- experimental-range type, MU = 0 → §21.6: conforming, ignored. MU = 1 → §21.6's
  second structural case: conforming file, reader rejects on capability, verifier
  reports *cannot establish*. All three statements agree.
- MU = 1 with PE = 0 → F25 / L46, verifier; readers treat as PE = 1.
- reserved flag bits 2–15 → F26 / L47, verifier.

The one place I expected trouble — an *experimental* MU = 1 record where one
verifier implements the private type and another does not — is a real divergence
(*cannot establish* vs. a verdict), but §10.3 declares it in terms: "two
unrelated experiments MAY select the same value, and nothing in this format
distinguishes them", and §2.3 lists exactly this as a *cannot establish* ground.
Designed-in, not a defect.

### 3.4 The certify / reject fork, hunted directly

This is the charter's target, and the document has systematically closed it. The
three candidates I built:

1. **A tile whose decoded size exceeds §21.9's 256 MiB guarantee.** Verifier A
   decodes and certifies; Verifier B declines on resource grounds. §2.3 names
   this precisely — "when it declines a layer's or a tile's decode on resource
   grounds and so cannot check §14's decoded-content obligations" — and B's
   verdict is *cannot establish*, which "is not a finding that the file is
   nonconforming". One certifies, one does not reject. Foreclosed.
2. **A user-metadata document decoding to more than 16 MiB.** [R-MTA-09]: "a
   reader instead decodes with a bound of its own choosing, no smaller than
   §21.9's user-metadata guarantee" and "the bound is that verifier's capability
   and not a limit on validity (`[R-CNF-10]`), so the decline is not a finding
   that the file is nonconforming and a verifier MUST NOT report it as one."
   Foreclosed, and explicitly.
3. **A zstd frame declaring Window_Size above 8 MiB on a tile whose decoded size
   is larger.** [R-COD-06]: "a wider window is conforming and merely permits a
   conforming reader to decline the tile or the layer on resource grounds
   (`[R-ERR-04]`)". Foreclosed.

Every one of these resolves to *certify vs. cannot-establish*, never *certify vs.
nonconforming*, and each time the document says so where the case arises. The
priority rule closes the remaining corner: "An established violation takes
priority: a verifier that has established any violation reports *nonconforming*,
however many requirements it was unable to check, and *cannot establish* is
available only to a traversal that established no violation."

### 3.5 Partial slack totals — my best hope for two verifiers reporting differently

[R-CNT-21] makes reporting the slack total a MUST. Two verifiers that stop at
different points report different partial totals. I thought this was a fork until
I read the closing clause: "It is not the file's slack total but a bound on it,
tightening to the exact total when the walk completes." The partial is *defined*
as "F less the bytes claimed by the claimants the walk did enumerate", and
[R-CNF-11] leaves the stopping point free, so two different partials are two
correct answers to two different questions. The order-dependence that would have
been a genuine bug is closed too: "where the rejection is one the walk itself
established … the claimants it had already enumerated are discarded with the
layer", which makes enumerate-then-discard identical to never-enumerate. And the
no-live-trailer case is carved out: "there is no F and no live state to walk, so
the total is not owed at all … which is not a partial total but the absence of
one." Foreclosed on all three axes.

### 3.6 The reader/verifier seam, and a file sitting exactly on it

A file with a reserved-range top-level record type carrying MU = 0, everything
else clean. A conforming reader ignores the record and serves the file. A
verifier reports nonconforming (F36). This is the seam, and it is stated, not
latent: §21.1 says "For a row whose Detector is *verifier*, the outcome names the
scope at which the damage is recorded, not an obligation on any reader", and
[R-CNF-12] licenses a reader to reject anyway. Both verifiers agree. Not a fork.

### 3.7 Feature interactions

- **Sparse tile under a filter chain.** A sentinel tile has no stored bytes; the
  pipeline never runs. §13.3 and §15.2 agree.
- **Empty layer under a limit.** §3.1 above.
- **Compaction over a record the compactor cannot read.** [R-WRT-06] bars MU = 1
  unimplemented; MU = 0 relocates safely by [R-CNT-13]'s no-embedded-offsets rule.
- **Shrink that turns real positions into padding of a prior-generation stored
  tile.** §20.3 bars it "in the bar's own tense" and forecloses the escape:
  "Unstoring that tile in the same commit does not rescue it either … so a shrink
  that turns real positions into padding of a tile stored there is barred whether
  or not the new state still stores it." §21.7 then records that the bar has no
  witness in exactly that case, which is honest rather than evasive. Both
  verifiers certify the resulting file; both are right; §21.7 says why.
- **Layout flip on a single-channel numeric layer** — decoded size, value order
  and byte offsets are all identical, so §20.3's "a change that leaves every one
  of those tiles' stored bytes meaning exactly what they meant … is not what this
  bars" permits it, and §14.4's Note confirms the byte-identity. Consistent.
- **Filter flip 1 → 2 on a single-byte-element layer** — s = 1 makes the shuffle
  the identity (i·n + j with s=1 gives j), and §20.3 names exactly that: "a
  filter whose mandated stride makes it the identity (`[R-COD-10]`)".

### 3.8 Mechanical sweeps

**The casing discriminator.** I grepped for lowercase `must|should|may|shall` in
the document. Nine hits, every one inside a `>` blockquote labelled Note,
Rationale or Example — non-normative by [R-CNF-01]. Then the converse: ALL-CAPS
BCP-14 keywords inside non-normative blocks. Five hits. Four are restatements of
rules stated normatively elsewhere (line 1212 restates [R-LIF-05]; 2840 and 3032
are advice with no normative counterpart to relax). The one that mattered was
line 2075: "a reader MAY verify each range once and cache the result" — a
*permission* living only in a Note, relaxing [R-IDX-04]'s "To use entry k, a
reader MUST verify". That is the exact shape of last round's surviving defect.
It is closed: §19.4 step 3 grants the same permission in normative text — "their
verifications MAY be cached per §15.4's note (`[R-IDX-04]`)". No asymmetry.

**Register completeness.** §21.1 makes completeness normative. I walked every
`[R-…]` in the document and asked, for each, whether it names a detectable
file-conformance violation and whether a row carries it. Every one is either
registered, a reader/writer-behavior rule, a SHOULD, or expressly accounted for in
§21.7's two paragraphs ([R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01],
[R-CNT-13]'s no-offsets clause, [R-CNT-18]'s nesting bar, §20.3 step 4's bar,
[R-ENC-06]) or in a Note that says why there is no row ([R-SLB-04]'s stale slab
declaration; [R-CNT-18]'s nesting). §6.2's field gates map one-to-one onto
F8–F19 with nothing left over. §15.3's eleven classification rows map onto
T1/T6–T12/L18/F33/L40–L42 with nothing left over. I found no unregistered
detectable condition.

**Instance arithmetic.** §21.8 claims "121 conditions over 273 instances". I
parsed the four register tables and counted semicolon-separated items, treating a
cell reading `—` as one instance, exactly as §21.1 prescribes: **121 rows, 273
instances** (F 36/58, L 49/116, T 26/55, R 10/44). The subsection headers claim
36, 49, 26 and 10; all four match. §21.8's number is right.

**Identifier hygiene.** 161 distinct identifiers referenced; every one has a
defining occurrence outside a register table; every prefix is one §2.2 lists; no
numbering gaps in any prefix ([R-ENC-100] is §2.2's own illustrative example, and
[R-SER-04] is present precisely as §14.4's withdrawal note). Every row
cross-reference in prose resolves to a row that exists and says what the citing
text claims: §21.2's four cross-major rows, §21.1's three specialization pairs,
§5.2's "L18's overlap or L40 through L42's placement", §9.6's "F8 and F17",
§17.2's "T24", §20.3's "(L44)", §21.7's "T2, T4 or T5" / "T3 or T14" /
"(T15, T17, T23, T25)", §21.6's "(F35, F36, L24, L25)", and Appendix H's four.
No wrong citation of the kind that survived nine rounds.

---

## 4. Findings

Two. Neither is a fork in bytes or verdicts; I say so plainly for each.

### adversary-01 — AMBIGUITY

**§20.4, the `MU = 1` row of the preservation table; §20.5, `[R-WRT-06]`,
`[R-WRT-07]`; §20.3 step 4, `[R-WRT-04]`**

The paragraph introducing §20.4's table opens by generalizing it to every record
type:

> Persistence governs every record type; only the authoritative source of the
> flags differs.

and immediately reads the table's PE column for *registered* types ("both
registered types carry PE = 1, so neither can be dropped"), which establishes
that the table is not confined to the not-implemented case that the sentence
introducing it names ("For a type the updater does not implement, the stored
flags are authoritative … and carry these obligations:"). The `MU = 1` row then
states four things in one cell, only the first of which is a persistence
obligation:

> Retain byte-identical. The updater MUST NOT modify the scope the record
> governs. At layer scope an unknown critical record blocks modification of that
> layer, leaving other layers editable (`[R-CNT-18]`). At file scope no commit is
> available at all … Compaction is barred on the same ground (`[R-WRT-06]`).

Nothing in the cell marks which of its four sentences generalize with the flags
and which stay with the not-implemented case. Two readings are available.

*Reading A (the whole cell generalizes).* Every layer record carries registry-fixed
MU = 1 (§7.3), and a layer record's governing scope is the layer (§7.2: "the
layer for a layer record and for sub-records"). So "The updater MUST NOT modify
the scope the record governs" bars an appender from modifying any layer of any
file — which annihilates the format's central operation. §20.3 step 4 flatly
contradicts it: "Every layer whose stored-tile set or index content this commit
changes has its tile-index region re-emitted in full". So Reading A is dead on
arrival for registered types, and no implementer would survive it.

*Reading B (only the retain/drop column generalizes).* The word "Persistence" in
the opening sentence is doing the narrowing, and the modification bar stays with
the unknown-critical case its own explanatory sentences describe. §2.4 supports
this: it describes the same two rows purely as preservation ("§20.4's table
states the cases: its MU = 1 and MU = 0 / PE = 1 rows").

I picked Reading B. The residue that Reading A's collapse does not clear up is
the case the paragraph expressly contemplates one sentence earlier — **a type the
updater implements that this specification does not register** — carrying MU = 1.
There §20.3 says nothing, and the cell and §20.5 point opposite ways. The cell
says "Compaction is barred on the same ground (`[R-WRT-06]`)". §20.5 says:

> An MU = 1 type it *does* implement is the remaining case, and §7.2 admits it …
> so a compactor implementing one relocates whatever that registration defines,
> on the same terms as the tile index.

An implementer must notice that the cell's compaction sentence cites
[R-WRT-06], and that [R-WRT-06]'s own text bars only "any record whose type it
does not implement with MU = 1" — so the cited ground does not reach an
implemented type and the cell's sentence is self-limiting. That is what decides
it, and it takes three sections to see.

*What an implementer does wrong without this.* An updater author who reads the
cell as written and applies it with the definition-supplied flags refuses to
compact, or refuses to commit at all, on files §20.5 expressly says it may
process — and, at the extreme of Reading A, ships an appender that declines every
layer edit.

**Byte-level: no.** §20.3's [R-WRT-04] forecloses Reading A for registered types,
and [R-WRT-06]'s own scoping clause forecloses the cell's compaction sentence for
implemented types. Both alternative readings are already decided by text
elsewhere in the document, so no conforming implementation may act on them and no
file's accept/reject verdict turns on it. It is a cost-of-reading defect, not a
fork.

### adversary-02 — OBSERVATION

**§20.5, `[R-WRT-06]` / `[R-WRT-07]` / `[R-WRT-09]`; §8.1's map; §15.3,
`[R-IDX-03]`**

§20.5's regeneration paragraph argues that a compactor cannot avoid meeting a
structurally-malformed index entry:

> An entry §15.3 classifies reject-tile on a structural ground is neither —
> `[R-IDX-03]` gives it no stored extent for a re-pointing to target — so
> regenerating the region cannot proceed without meeting it, and the violation is
> thereafter one the compactor has detected.

The argument is sound but conditional on the region being regenerated, and
regeneration is conditional on relocation: "except that relocation re-points
extent slots, regenerates each relocated tile-index region". Whether relocation is
obligatory is left in two minds by the sentence before it:

> A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits and every declared layout invariant permits

The first clause reads as "placement always changes"; the second grants freedom
that plainly includes leaving a structure where it was. Under the second reading
a compactor may place a layer's index region at its input offset, never
regenerate it, and never meet the malformed entry. Nothing else catches it:
[R-WRT-09]'s enumerated checks are the open, each retained layer's record
(§19.3, which performs no fetch and so never classifies an entry), the full index
chain ([R-IDX-04] — crc_of_crc_array and segment CRCs, which verify fine over a
malformed entry), and "each relocated extent's checksum, including every stored
tile's entry crc" — and a structurally-malformed entry addresses no stored tile,
so it has no crc to check. So Compactor A, which relocates, detects and MUST
refuse; Compactor B, which does not, emits an output carrying the violation.

I resolved this as *not a defect*: [R-WRT-01] anticipates the outcome — "a
violation latent in a structure it carries forward verbatim travels into its
output" — and §20.5's promise is conditioned on a clean input ("Given a
conforming input the output is a conforming file"), which this input is not.
[R-CNF-12] adds that "For a nonconforming file no acceptance obligation exists".
So both behaviours are licensed and neither compactor is wrong.

*What an implementer does wrong without this.* A compactor author who reads
"placement is not among the things it carries forward" as an obligation will
regenerate every index region unconditionally — correct but not required — while
one who reads the freedom clause will not, and the two will disagree about
whether a given damaged file is compactable. Both are conforming; the document
does not say which behaviour it prefers, and the regeneration paragraph reads as
though the question does not arise.

**Byte-level: no.** Both dispositions are licensed on a nonconforming input, and
on a conforming input no entry is structurally malformed, so no region's
regeneration is forced by anything and no output differs. Nothing a verifier says
about any file changes.

---

## 5. Honest summary of what did not survive

My charter's construction — a file two conforming verifiers judge differently —
did not survive. I tried it eleven ways (§3.1–§3.7 above) and each time the
document names the case where it arises. Three patterns account for the closure:
the *cannot establish* verdict absorbs every capability and resource divergence
and is explicitly not a rejection; §21.1's "where a row and the rule it cites
diverge, the rule governs" absorbs every register/rule disagreement I could
manufacture; and §21.7 pre-declares the conditions that have no file-level
witness, so a verifier is never asked to look for one.

The two things I would still change are above, and neither moves a byte.
