# Cleanroom round 29 — Verifier implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,697 lines). I read it whole, in four contiguous chunks, before doing any
analysis. I opened no ADR, no `docs/`, no `conformance/`, no `registry.json`, no
`PLAN.md`, no git history, and ran no web access. I listed no directory except
the implicit `mkdir -p` of my own scratch and output paths.

Working files I wrote, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/verifier/`:

- `vfy_crc.py`   — CRC-32C implementation + the document's four stated CRC constants
- `vfy_appa.py`  — Appendix A's 128-byte hexdump, re-CRC'd
- `vfy_build.py` — byte-exact construction of my generation-1 file
- `gen1.tarn`    — the 576-byte file that script emits
- `vfy_gens.py`  — the four-generation coverage/slack arithmetic

Plus this transcript at the single output path named in the brief. I did not
read that output directory.

**Context I did not ask for.** Material was placed in my context before I began:
a project instruction file pointing at a `CLAUDE.md`/`AGENTS.md` pair, and an
index of the maintainer's memory notes with titles referring to this project's
working cadence, a naming constraint, prior workflow failures, and the relation
of §21 to a vector corpus. I did not open any of it and I have not used any of
it. I disclose that it appeared.

**Path note.** The brief names the spec at
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` and it is
there. My shell's working directory is
`.../tarn-first-draft/scratch/cleanroom`, and the injected project-instruction
block referred to a sibling path `.../GitHub/tarn/CLAUDE.md` — a different
directory name from the one the brief uses. I did not go looking at either.

---

## 1. What I built

A conforming verifier, on paper but concretely: the certification procedure as
an ordered algorithm, the coverage walk with worked arithmetic on a file I
constructed byte-for-byte, the overlap/alignment/slab checks on an adversarial
layout, the checksum inventory with every constant I could compute reproduced
locally, the decode obligations, and a four-generation trace (create → append →
update → compact) with the certification result at each step.

---

## 2. The certification procedure, as an ordered algorithm

### 2.1 Verdict vocabulary

§2.3 `[R-CNF-11]` fixes three verdicts and their availability:

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or
> *cannot establish* — the last where some requirement is one it is unable to
> check on a capability or resource ground

with a strict priority rule:

> An established violation takes priority: a verifier that has established any
> violation reports *nonconforming*, however many requirements it was unable to
> check, and *cannot establish* is available only to a traversal that
> established no violation.

So the verdict function is total and order-independent:

```
if established_violations  : NONCONFORMING          (certification barred)
elif unable_to_check != {}  : CANNOT_ESTABLISH       (certification barred)
else                        : CONFORMING             (certify)
```

Two report-only channels ride alongside and constrain neither verdict:

- *unexamined* — available **only** to a verifier that exercised
  `[R-CNF-11]`'s licence to stop at the first violation. Since that licence is
  keyed to a violation, a verifier reporting *unexamined* is always reporting
  *nonconforming* as well. `[R-CNF-11]` says so directly: "*Unexamined* is
  neither a verdict nor *cannot establish* — it constrains the report, not the
  verdict."
- the per-requirement unable-to-check report, owed "whichever of the three
  verdicts it reports". The *conforming* branch of that is vacuous (a
  non-empty unable-to-check set forces one of the other two), but harmlessly so.

The five *cannot establish* grounds §2.3 lists, and what I concluded about each:

| # | Ground | Note |
|---|---|---|
| 1 | file declares a format major the verifier does not implement | `[R-CNF-13]` still obliges every *reaching* condition; a failure of one is *nonconforming*, not *cannot establish*. |
| 2 | a record carries MU = 1 with a type the verifier does not implement (§21.6) | Applies to sub-records too by its terms. The justification is not stated where the ground is, but is recoverable: `[R-CNT-13]` permits an MU = 1 type to "carry further references", so the coverage partition cannot be completed. That is exactly why `[R-WRT-06]` makes a compactor refuse. |
| 3 | cannot execute a codec or filter (`[R-COD-11]`) | For a *conforming* verifier this arises only at a reserved/experimental value, since every assigned codec and filter is core (`[R-CNF-03]`); §17.4 says so. |
| 4 | declines a layer's or a tile's decode on resource grounds | Stated over "§14's decoded-content obligations", but §9.7 obliges decoding also for §21.4's codec rows. The list is introduced by "as when", so it is illustrative and the general clause covers the wider case. Recorded as a rejected candidate, not a finding. |
| 5 | declines to decode a user-metadata document (`[R-MTA-09]`) | §21.5's preamble confirms "the bound above" in §18.2 covers both the size bound and the frame's declared window. |

Expressly **not** a ground: a user-metadata document under an encoding this
specification does not assign (`[R-MTA-10]`) — "no content rule attaches there,
so nothing is left unchecked". Note the asymmetry with ground 2: an unknown
*record type*'s extent likewise has no content rule and no checksum (§8.1), yet
it *is* a ground. The distinguishing fact is the MU = 1 reference licence above.
I satisfied myself the asymmetry is principled, not accidental.

### 2.2 The ordered checks

I write `→ F##/L##/T##/R##` for the register row a failure records against.

**Tier 0 — the file's ends.**

1. Physical size ≥ 128 → F5 (`[R-CNT-27]`).
2. If bytes [0,16) are resident, byte-equality against the 16-byte front block
   → F6, and its byte-reversed specialization → F1. §2.3 gives a verifier **no**
   residency exemption; `[R-CNT-04]`'s exemption is a reader's. Appendix H
   restates this. A verifier therefore always fetches [0,16).
3. Trailer, in `[R-CNT-06]`'s **fixed order**: magic → F8/F1; CRC over
   [F−64, F−4) → F14; version gate → F18/`[R-CNT-07]`. Only these three touch
   fields `[R-CNT-24]` fixes across majors.
4. Then, gates passed, the remaining trailer fields, which `[R-CNT-06]` does
   *not* order among themselves: flags incompat lane → F19; committed_file_length
   = transport-authoritative size → F17 and multiple of 64 → F13; dir_offset ≥ 16
   → F9; dir_length ≥ 4 → F16; dir_offset + dir_length ≤ F − 64 → F10; file_id ≠ 0
   → F12; reserved [48,60) zero → F15; and the value-domain rows F2/F3.

  §24 `[R-VEC-02]` notes the consequence for vectors: "§6.2's field gates are
  validated together, so a file failing two of them attributes to neither alone".

**Tier 1 — directory.**

5. CRC over the region's first dir_length − 4 bytes → F20 (`[R-CNT-11]`), before
   any other use.
6. Record walk: framing with no residue → F29; type 0 → F24; multiplicity → F34;
   unknown-type MU gate → F35; reserved-range type whatever its MU → F36
   (verifier-only); extent slots → F30/F31/F32; reserved flag bits → F26;
   MU = 1 with PE = 0 → F25; registered type's stored flags against §7.3 → F28;
   layer-name namespace over raw bytes → F4, plus L3/L5/L6 for the name itself,
   all placed **at open** by §19.1 step 4.

**Tier 2 — per layer** (§19.3 `[R-RDR-03]`; no I/O, all from the resident
directory and F): L1, L2, L4, L7–L17, L19–L36, L39, L43–L47, L49.

**Tier 3 — index chain, per layer:** crc_of_crc_array → L37; each segment CRC
→ L38 (`[R-IDX-04]`). §15.4's constant `0xEECB3BB2` "licenses nothing for
readers: verification is byte comparison of computed CRCs, never constant
matching".

**Tier 4 — per entry:** `[R-IDX-03]`'s table → T6–T12; codec-1 length equality
→ T14.

**Tier 5 — per stored tile:** entry crc over the stored bytes → T1; then decode.
§9.7 is emphatic that decoding is unconditional: "A verifier decodes **every**
stored tile, whatever content obligations §14 places on the layer: §21.4's codec
rows are file-conformance violations, and a verifier MUST NOT certify past a
violation it has not looked for." → T3, T13, T15–T25. Then the decoded-content
obligations: T4 (padding), T5 (pad bits), T2 (interleaved bool byte at a real
position), T26 (mis-strided filter, where it shows).

**Tier 6 — extents of user-metadata records:** terminal CRC → R2 (owed even at
an unassigned encoding: `[R-MTA-10]` names it among the structural checks that
decide conformance); encoding value set → R1; frame constraints → R4; decode →
R3; document rules → R5–R10; member ordering → F27/L48 (verifier-only).

**Tier 7 — whole-file:** the coverage walk (§9.7) — disjointness → L18/F33,
bounds, checksums; no structure in the pre-trailer gap → F7; alignment → L40;
slab → L41/L42; slack total.

I checked mechanically that every Detector cell in §21.2–§21.5 reads *reader* or
*verifier* and every Detected cell reads one of §19.2's four tiers or
*certification*. Result: 100 reader rows, 20 verifier rows, no other value.
The 20 verifier rows are F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41,
L42, L46, L47, L48, L49, T2, T4, T5, T26 — and Appendix H's verifier checklist
covers every one of them (T26 via "decoded-content obligations", since T26's own
row says "the check that detects it is T2's or T4's").

### 2.3 What bars certification

Exactly two things: an established violation, and a non-empty unable-to-check
set. Not barred: a SHOULD deviation (`[R-CNF-12]`: "a verifier reports a SHOULD
deviation as an advisory that does not bar certification", and "owes no search
for one"); a §21.9 quantity above a minimum guarantee (`[R-ERR-04]`: "A file
exceeding any of these remains conforming"); a user-metadata record at an
experimental-range encoding (`[R-MTA-10]`, §21.6) — reported, not counted
against; an unrecognized `tarn.` key or a standardized key out of scope
(`[R-MTA-06]`, `[R-MTA-07]`).

---

## 3. Checksums

### 3.1 Constants I reproduced

I implemented CRC-32C from §4.5's parameters alone (reflected polynomial
0x82F63B78, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, little-endian storage) and
computed every constant the document states that is locally computable:

| Constant | Document | Mine | Where |
|---|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | **0xE3069283** | §4.5 check vector |
| CRC-32C(zero bytes) | 0x00000000 | **0x00000000** | §4.5, §7.1, Appendix A |
| CRC-32C of 4 sentinel entries (80 bytes) | 0x80A34955, stored `55 49 A3 80` | **0x80A34955** | §7.4 example |
| crc_of_crc_array over that 4-byte array | 0xC4EE982E | **0xC4EE982E** | §7.4 example |
| CRC-32C of 2¹⁶ sentinel entries | 0xEECB3BB2 | **0xEECB3BB2** | §15.4 `[R-IDX-05]`, Appendix B |
| Appendix A trailer CRC over [0,60) | 0x402F157E, stored `7E 15 2F 40` | **0x402F157E** | Appendix A |

All six reproduce. There is no CRC constant in the document I was unable to
compute: the only checksums stated as values are these, and each is over bytes
the document also gives in full. Nothing here needed an external library or a
test vector.

### 3.2 Coverage: is every live structure covered?

§8.1's map, checked against §5.2's partition classes:

| Live-state member | Covered by | Covers it in turn |
|---|---|---|
| front signature block [0,16) | *nothing* — byte equality | — |
| stored-tile extent | its entry's crc field | segment CRC → crc_of_crc_array → directory CRC → trailer CRC |
| tile-index region: entry array | per-segment CRCs | crc_of_crc_array → directory CRC |
| tile-index region: segment CRC array | crc_of_crc_array | directory CRC |
| user-metadata extent | its own final 4 bytes | — (terminal) |
| extent of an unassigned record type | *nothing* | — |
| directory region | its own final 4 bytes | — (terminal) |
| trailer | its own [60,64) | — (terminal) |
| slack | *nothing*, by construction (§5.2) | — |

So the answer to my charter's question is **no**: two live-state members are
covered by no checksum — the front signature block (equality-checked instead)
and the extent of a record of a type this specification has not assigned. §4.5
and §8.1 state both exceptions, and §22.3 `[R-SEC-04]` names the second as a
residue "stated rather than defended". A third class, slack, is outside the live
state entirely.

I checked the three "interior" checksums §4.5 names — each segment CRC array,
each entry's crc field, each layer record's crc_of_crc_array — and each is both
comparison-verified and covered by exactly one further checksum, as §4.5 claims.
The chain terminates at three self-referential fields, exactly the three §4.5
excepts.

I also checked the degenerate case: at entry_count = 0 there is no region, the
extent slot is (0,0), and crc_of_crc_array is 0 (`[R-CNT-17]`, `[R-CNT-23]`,
§15.4's example). Nothing is left uncovered because nothing exists.

---

## 4. The coverage walk, on a file I built

### 4.1 The file

`vfy_build.py` emits a 576-byte generation-1 file. Layer `sst`: interleaved,
rank 1, dimension `x` with E = 100 and T = 32, one float32 channel `temp` with
fill 0x7FC00000, codec 1 (none), filter 1 (none), no alignment or slab. Derived:

```
G = ceil(100/32) = 4     N = 4     P = 32     C = 1     Q = 4
decoded size = P·Q = 128
entry_count = N = 4                          (interleaved, [R-GEO-03])
extent_length = 4·20 + ceil(4/2^16)·4 = 84   ([R-CNT-17])
inline payload = 81 bytes                    (§7.4's worked example, same shape)
```

Tiles 0 and 3 stored; entries 1 and 2 are the sentinel `FF ×16 00 ×4`. Tile 3
covers x = 96..127, so x = 100..127 are **28 padding positions** (`[R-GEO-04]`),
and I encoded the channel's fill at every one of them, as `[R-SER-05]` requires.
Layout:

```
[0,16)      front signature block
[16,144)    stored tile, disk ordinal 0        128 B
[144,272)   stored tile, disk ordinal 3        128 B
[272,356)   layer record's extent = index      84 B
[356,465)   directory (1 record + CRC)         109 B  = 24 + 81 + 4
[465,512)   pre-trailer pad                    47 B   slack
[512,576)   trailer                            64 B
F = 576, F mod 64 = 0
```

### 4.2 The walk

§9.7 `[R-LIF-08]` names the claimants: the directory itself; each record's
extent; the stored extent of each non-sentinel entry; plus the front block and
the live trailer, which "are claimed by the walk as well, being members of the
live committed state". A record is not a claimant of its own — its header and
inline payload lie inside the directory region. A layer record's extent slot
addresses the index region, so the region "enters the walk once, as that
record's extent, and is not a second claimant beside it."

```
front      [0,16)       16
tile ord0  [16,144)    128
tile ord3  [144,272)   128
index      [272,356)    84
directory  [356,465)   109
trailer    [512,576)    64
                      ----
claimed                529
F                      576
slack                   47   = exactly the pre-trailer pad
```

Disjoint ✓. Every non-front, non-trailer claimant inside [16, F−64) = [16,512) ✓.
Every claimant verifies against the checksum §8.1 states for it ✓.

**Which bytes are certified, which are counted-but-unconstrained, and can a byte
be neither?** 529 bytes are certified (claimed, bounded, checksummed where the
map states one — less the 16 front-block bytes, which are certified by equality
rather than by checksum). 47 bytes are counted and unconstrained: "Slack has no
internal structure this specification defines, its content is unconstrained, and
no conformance requirement applies to it." No byte can be neither. §5.2's Note
argues this and I agree with the argument: the live committed state is *defined*
as the front block plus what a complete walk reaches, and `[R-LIF-08]` makes
every byte the walk misses slack, so "'belongs to no class' describes nothing,
and a register row for it would be a row no file could exhibit." Only
disjointness is testable, which is why F33 and L18 exist and no "unclassified
byte" row does.

Sanity check against the document's own smallest file: Appendix A's 128-byte
file claims 16 + 4 + 64 = 84 and leaves 44 slack, and §5.1's Example says
"44 bytes of slack". Reproduces.

### 4.3 A walk that does not complete

I injected an L18 into generation 3 of the trace below: entry 3 re-pointed to
(700, 128), so its extent [700,828) overlaps that same layer's index region
[704,788). Intra-layer overlap → reject-layer, verifier-detected, certification
tier.

`[R-CNT-21]` then governs:

> a rejected layer's claimants are not enumerated, whether or not the rejection
> impeded reading them — and where the rejection is one the walk itself
> established, L18's overlap or L40 through L42's placement among them, the
> claimants it had already enumerated are discarded with the layer

So layer `sst`'s three claimants (two tiles, one index region) are discarded.
What remains enumerated at F = 1280: front 16, user-metadata extent 25,
directory 134, trailer 64 = 239.

```
partial slack total = F − 239 = 1041
true slack (had the layer been clean) = 701
```

1041 ≥ 701 ✓ — "an upper bound on the file's true slack, never an under-count".
The verifier "MUST say which scope or violation stopped the walk": layer `sst`,
L18. Verdict *nonconforming* (a violation was established), certification
barred, and the total reported **as partial** — not as a slack total.

One reading I had to settle: "F less the bytes claimed by the claimants the walk
did enumerate". If that means the *sum of lengths*, overlapping claimants
double-count and the partial total can drop below the true slack, defeating the
"never an under-count" guarantee. If it means the *union of byte positions* — the
plain reading of "the bytes claimed" — the bound holds unconditionally. I took
the union reading and record the alternative as closed rather than as a finding.

A second case I worked: an entry `[R-IDX-03]` classifies reject-tile on a
**structural** ground. §9.7 is explicit that this does **not** make the walk
incomplete — "the walk passes over it, and the bytes it nominally addresses fall
to slack" — so the total stays exact even though the verdict is *nonconforming*.
By contrast an entry whose only defect is a failed stored-bytes crc "keeps its
extent", stays a claimant, and is checksum-checked in place (T1). I confirmed
that the six *structural* rows §15.3 marks are all decidable from an entry's own
20 bytes plus F, which is what makes §16.2's claim work (below).

---

## 5. Overlap, alignment, and slab invariants on an adversarial layout

### 5.1 Overlap — which row, at which scope

I enumerated the pairs and matched each against `[R-CNT-13]`, §15.3's table, F33
and L18:

| Overlapping pair | Row | Outcome |
|---|---|---|
| two stored extents of layer A | L18 | reject-layer |
| stored extent of A × A's own index region | L18 | reject-layer |
| stored extent of A × A's sub-record extent | L18 | reject-layer |
| stored extent of A × stored extent of B | F33 | reject-file |
| stored extent of A × the directory | F33 | reject-file |
| top-level record extent × the directory | F33 | reject-file |
| any claimant reaching [0,16) | *not* F33 — F31/L16/T8, or F30/L15 where the slot is (0, N) | reject-file/layer/tile |
| any claimant reaching [F−64, F) | *not* F33 — F10/F32/L17/T9 | reject-file/layer/tile |

I checked F33's exclusion list is complete for the claimant kinds that exist:
directory (F9/F10), non-layer top-level record extent (F30/F31/F32), layer record
and sub-record extent (L15/L16/L17), stored-tile extent (T8/T9). Nothing else
claims bytes. F33's instance cell adds "directory region" to F7's four kinds,
correctly — the directory can be an overlap party but cannot lie between its own
end and the trailer.

### 5.2 Alignment

`[R-SLB-01]`: A a power of two, 512 ≤ A ≤ 2⁶²; "every stored tile's offset
satisfies offset mod A = 0"; a verifier MUST check it, readers need not.
Adversarial: A = 4096 with stored tiles at 4096 (✓), 8192 (✓), 12,290 (✗ → L40,
reject-layer). Note what alignment does **not** constrain: index regions, record
extents, and the directory are unconstrained by A. Appendix G item 3 quietly
treats A as constraining "structures" generally ("where a declared alignment
admits no structure at 16") — a looseness, but Appendix G is non-normative and
adopting the profile only narrows what a writer emits.

Boundary: with A = 512 the first legal stored-tile offset is 512, not 16, because
T8 forbids offset < 16 and alignment forbids anything not a multiple of 512.

### 5.3 Slabs

Adversarial planar layer, C = 2, N = 4 (ordinals 0..7), S = 3, A_slab = 16.
`[R-SLB-02]` partitions each channel block independently and runs never span
blocks:

```
block 0 = [0,4)  -> run 0 = {0,1,2}, run 1 = {3}
block 1 = [4,8)  -> run 0 = {4,5,6}, run 1 = {7}
```

Stored/sentinel assignment: 0 stored (len 10), 1 sentinel, 2 stored (len 20),
3 stored (len 5), 4 stored (len 8), 5 stored (len 8), 6 sentinel, 7 stored (len 4).

Conforming placement:

```
off(0)=256  (256 mod 16 = 0, first stored of run 0 block 0)   [256,266)
off(2)=266  (= off(0)+len(0); ordinal 1 is a sentinel, transparent)  [266,286)
off(3)=288  (288 mod 16 = 0, first stored of run 1 block 0)   [288,293)
off(4)=320  (320 mod 16 = 0)                                  [320,328)
off(5)=328  (= off(4)+len(4))                                 [328,336)
off(7)=352  (352 mod 16 = 0)                                  [352,356)
```

Injections and the rows they hit:

- off(2) = 267 → gap → **L41** (reject-layer), and *only* L41: the extents stay
  disjoint, so no L18.
- off(2) = 265 → overlap → **L41** *and* **L18**. Every file exhibiting L41's
  "overlap" instance necessarily exhibits L18, so §21.1's specialization rule
  records it against the narrower row, L41. Both are reject-layer and both
  verifier/certification, so nothing turns on the choice. §21.1's pair list does
  not name (L41, L18), but says the list "is not offered as closed".
- off(3) = 290 → first stored tile of a run misaligned → **L42**.
- ordinal 1 replaced by a *structurally* invalid entry (offset = S, length = 5)
  → transparent to run continuity, exactly as a sentinel is, so off(2) still
  must equal 266. The file exhibits T7 and not L41.
- ordinal 1 kept as a well-formed stored entry whose bytes fail their crc →
  **not** transparent; off(2) must now equal off(1)+len(1). File exhibits T1 and,
  if the writer treated it as transparent, L41 too.

§16.2 claims this last distinction keeps the invariant "decidable from the index
entries alone, given the committed file length §15.3 already requires to classify
any entry." I checked that claim: transparency turns only on *structural*
classification, and all six structural rows are decidable from an entry's own
20 bytes plus F. The claim holds — a verifier never needs a payload fetch to
decide L41/L42. That is a non-obvious property and it survives the check.

Also confirmed: a run with no stored tiles imposes nothing; and `[R-SLB-04]`'s
stale-declaration obligation genuinely carries no row of its own, because a
declaration is "stale" only where the invariants fail, which is L41 or L42.

---

## 6. Decoded-content obligations

**What a verifier must decode:** every stored tile of every layer (§9.7), and
every user-metadata document under an *assigned* encoding (`[R-MTA-09]`,
`[R-MTA-04]`, `[R-MTA-05]`).

**What it compares against:**

- decoded length exactly the declaration-derived decoded size — `P·Q`
  interleaved, `P·Bᶜ` planar numeric, `⌈P/8⌉` packed planar bool
  (`[R-SER-07]`, T3);
- every padding position carrying that channel's recorded fill — "the recorded
  fill bytes for a numeric channel, the recorded fill byte for an interleaved
  bool channel, the fill bit in a packed plane" (`[R-SER-05]`, T4);
- every pad bit carrying the plane's channel's fill bit (`[R-SER-05]`, T5);
- every interleaved bool value byte 0x00 or 0x01 at a real position
  (`[R-SER-08]`, T2) — the padding-position case is T4's, "the two rows together
  covering `[R-SER-08]`", which I verified: any byte outside {0x00, 0x01} at a
  padding position necessarily differs from a legal bool fill byte, so T4 fires;
- codec conformance: exactly one stream/frame/block, no trailing bytes, decode
  consumes the extent exactly (T15–T25).

**What it is permitted to skip:** nothing, except by declining on a capability or
resource ground and taking *cannot establish* instead. In particular it may not
skip a decode because §14 places no content obligation on the layer — §9.7 is
explicit — and it may not hunt for SHOULD deviations. It attaches **no** content
rule to a user-metadata document under an unassigned encoding (`[R-MTA-10]`),
but must still check that record's framing, extent slot, encoding-byte value set,
and terminal CRC, and must **report** the record: "owning scope, the encoding
value, and the stored extent length".

I re-derived §14's worked examples to be sure my decode model matched the
document's: §14.2's (2,3)/uint8+uint16 tile (Q = 3, size 18, ordinal 5 at bytes
[15,18)); its float32+bool variant (Q = 5, size 30, bytes [25,30)); §14.3's
(2,5) packed bool plane (`55 01` at fill false, `55 FD` at fill true); §14.5's
(5,5)/(4,4) edge tile (1 real position, 15 padding, 32 bytes, `CD AB` fifteen
times); §17.3's byte-shuffle of three float32 values. All five reproduce exactly.

---

## 7. Multi-generation trace

Same layer, verified after each step. `vfy_gens.py` computes it; the numbers
below are that script's output and match my hand arithmetic.

**Gen 1 — creation.** `[R-LIF-02]`'s creation path: front block, then steps 2–6
from offset 16, both barriers.

```
F1 = 576   dir = [356,465)   trailer @ 512
claimed 529   slack 47 (the pad)
verdict: CONFORMING
```

**Gen 2 — append, superseding stored tile 0.** Writing begins at exactly F1.
The layer's stored-tile set changed, so `[R-WRT-04]` step 4 re-emits its whole
index region "necessarily at a new placement", with 3 of 4 entries byte-identical
at their disk-ordinal positions and one re-pointed.

```
new payload [576,704)   new index [704,788)   dir = [788,897)   trailer @ 960
F2 = 1024   (F2 − F1 = 448 ≥ 128, as [R-LIF-02] forces)
claimed 529   slack 495
   = old tile0 128 + old index 84 + dir1 109 + pad1 47 + trailer1 64 + pad2 63
verdict: CONFORMING
```

Cross-check against §20.3's own example ("32 · 20 + 4 = 644 bytes — one entry
re-pointed, 31 byte-identical"): same shape, 4·20 + 4 = 84 here.

**Gen 3 — update, adding a file-scope user-metadata record.** Document
`{"tarn.title":"demo"}` (21 bytes) plus its terminal CRC = a 25-byte extent;
extent_length 25 ≥ 5 ✓, inline_length exactly 1 ✓, members trivially sorted ✓.
The layer record is re-emitted byte-identically (`[R-WRT-05]`) — extent slot and
all — so it still addresses the gen-2 index region.

```
umd extent [1024,1049)   dir = [1049,1183)   trailer @ 1216
F3 = 1280   claimed 579   slack 701
verdict: CONFORMING
```

This is §20.3's shape (b), not (c): "Editing user metadata is not this shape:
its document lives in an extent, so a new extent is appended and the old one
becomes slack."

**Gen 3′ — the injected fault.** Entry 3 re-pointed to (700,128), overlapping the
layer's own index region.

```
verdict: NONCONFORMING (L18 established, reject-layer)
slack reported as PARTIAL: 1041, stopped by layer `sst` / L18
```

**Gen 4 — compaction.** Fresh file_id (`[R-WRT-06]`: "a new draw under §9.3's
randomness advice, not merely a value compared against the input's"), creation
path, both barriers, pad. Every stored tile's bytes verbatim and every entry crc
unchanged; the index region is regenerated because its entry offsets moved, and
crc_of_crc_array is updated with it.

```
tiles [16,144) and [144,272); index [272,356); umd [356,381)
dir = [381,515)   trailer @ 576
F4 = 640   claimed 579   slack 61 (the pad only)
reclaimed 1280 − 640 = 640 bytes
verdict: CONFORMING
```

The compactor's verification depth is `[R-WRT-09]`'s: the open, each retained
layer's record and full index chain, and each relocated extent's checksum
including every stored tile's entry crc — and it "reaches no decoded content".
So a compactor is *not* a verifier: it can emit a conforming-looking output from
an input carrying, say, a T4 padding violation, because it never decodes. §20.5
says exactly this — "a violation latent in a structure it carries forward verbatim
travels into its output". This is a real and correctly-stated asymmetry, and it
is why §20.5 says "certifying the whole file is a verifier's office."

---

## 8. Findings

### verifier-01 — AMBIGUITY. §21.7's *detectable*/*unwitnessed* pair is not the dual it claims to be; the two readings decide register row F35 differently

**Location:** §21.7, `[R-ERR-01]`; restated in §21.1's completeness clause.

**Quotation** (§21.7):

> A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it
> by any check this specification obliges a reader or a verifier to perform. It
> is **detectable** in the contrary case: where some file exhibiting it is
> separated by such a check from every file that does not. The two are stated
> over the same subject, and each quantifier is the other's dual, so each is
> exactly the negation of the other

**The problem.** Written out, with `E` the files exhibiting the condition and `N`
its complement:

```
unwitnessed  :  ∀f∈E . ∃g∈N . ∀check . ¬separates(check, f, g)
its negation :  ∃f∈E . ∀g∈N . ∃check .  separates(check, f, g)
detectable   :  ∃f∈E . ∃check . ∀g∈N .  separates(check, f, g)     [reading 1]
            or  ∃f∈E . ∀g∈N . ∃check .  separates(check, f, g)     [reading 2]
```

*Unwitnessed* has three quantifiers and fixes their order unambiguously.
*Detectable* has three as well, but the sentence places "by such a check"
adjacent to the verb and "from every file that does not" after it, which is the
word order of reading 1 — one check that separates the witness from the whole
complement. §21.1's restatement is if anything more strongly reading 1, because
it sets the check off in commas as a single adjunct: "some file exhibiting it is
separated, **by a check** this specification obliges a reader or a verifier to
perform, from every file that does not." Only reading 2 is the negation of
*unwitnessed*. The document asserts the duality rather than deriving it, so the
assertion is evidence for reading 2 and the syntax is evidence for reading 1.

**This is not academic — it flips a row of the register.** Take F35, "A top-level
record has a reserved-range type value (0x0003-0x7FFF) with MUST_UNDERSTAND set
to 1." Two obliged checks bear on it, both from `[R-CNT-15]`:

- the reader's: unknown type with MU = 1 → reject-file. Its failure set is
  `reserved∧MU1 ∪ experimental∧MU1`.
- the verifier's: a reserved-range type is a validity error. Its failure set is
  `reserved∧MU1 ∪ reserved∧MU0`.

Neither failure set is contained in F35's condition `reserved∧MU1`, so **no
single obliged check separates an F35 file from every non-F35 file**. Under
reading 1, F35 is unwitnessed and §21.7 says the register should carry no row
for it. Under reading 2 it is (for most complements) detectable, because the two
checks between them separate f from each g. The register does carry F35, and
§21.1 lists it as a strict specialization of F36.

**Which I picked and why.** Reading 2, because the duality sentence is the only
thing in the passage that is stated as a *claim* rather than left to syntax, and
because reading 1 would strip rows the register carries. But reading 1 is the
plainer English of both statements of the test, and §21.1's comma placement
pushes harder toward it than §21.7's does.

**What an implementer does wrong without it.** §21.7 says the test "decides any
condition put to it without appeal to a list". An implementer auditing the
register for §21.1's normative completeness — the intended use — will reach
opposite verdicts on the specialization rows depending on which reading it
picked, and will report the document either as carrying rows it should not or as
correct.

### verifier-02 — CONTRADICTION. §21.7 says the register carries a row *exactly where* a condition is detectable; F1 has a row and is not detectable under §21.7's own test

**Location:** §21.7 `[R-ERR-01]`; §21.2 row F1; §21.1's specialization paragraph.

**Quotations.** §21.7:

> The register carries a row for a condition exactly where it is a detectable
> file-conformance violation, so an unwitnessed condition is absent from it by
> that clause's own terms rather than in breach of them.

§21.2, row F1:

> A signature constant is stored byte-reversed — never to be adapted as a
> foreign-endian TARN file; the front-block instance binds only a reader holding
> bytes [0, 16) resident (`[R-CNT-04]`), the trailer-magic instance every reader
> (`[R-CNT-06]`)

§21.1:

> F1's front-block instance of F6 and its trailer-magic instance of F8 ... stand
> in that relation

**The problem.** Apply §21.7's test to F1's condition. Let `f` be a file whose
trailer magic holds the byte-reversed constant `1A 0A 0D 54 41 52 4E 8A`, with
its trailer CRC correctly recomputed over those bytes. Let `g` be the same file
with the magic replaced by eight zero bytes and its CRC recomputed. `g` does not
exhibit F1. Every obliged check gives the same verdict on both: `[R-CNT-06]`'s
ordered validation fails at the magic on each, identically, and no later check
runs. No check this specification obliges separates `f` from `g`. By §21.7's
definition F1's condition is therefore **unwitnessed**, under either quantifier
reading, since the counter-file `g` defeats even the ∀g∃check form. Yet the
register carries F1, so the biconditional "exactly where" is false as stated.

§21.1 states only the forward half — "a *detectable* file-conformance violation
this specification names and the register omits is a defect in this document" —
and §21.1's specialization rule positively *requires* the narrow rows to exist,
since a file is "recorded against the narrower row, whose detector and detection
point are the ones that apply." Recording a file against a narrower row is a
corpus-construction rule; it does not entail that an obliged check separates the
narrow condition from the broad one. §21.7's converse contradicts it.

**A second, independent cause of the same failure: "check" is never
individuated.** §21.7 is careful that "The subject is the condition and not the
requirement", and cites `[R-CNF-13]` and `[R-CNT-06]`'s nine conditions for how
conditions are individuated. Its *instrument*, though, is "any check this
specification obliges a reader or a verifier to perform", and nothing in the
document individuates checks. If `[R-ENC-02]`'s sentence — "a reader encountering
what appears to be a byte-swapped signature MUST treat the file as invalid,
never as a foreign-endian file to be adapted" — counts as obliging a distinct
check whose failure set is exactly "byte-swapped", then F1 *is* detectable and
the biconditional survives. If it is instead a constraint on the *response* to
`[R-CNT-06]`'s magic check, F1 is not. The document supplies nothing that
settles it, and §21.7 explicitly forbids the one instrument that would — "the
instrument is the checks this specification obliges an actor to perform, and
deliberately not the register's own rows".

**Permitted readings and the one I picked.** (a) The biconditional is exact, and
`[R-ENC-02]`, `[R-CNT-25]`'s "(0,0)" clause and similar sentences each oblige a
distinct check at exactly the granularity of the narrow rows — in which case the
narrow rows are detectable and §21.1's specialization list is a list of
check-granularity facts. (b) The biconditional over-reaches, §21.1's forward-only
clause is the operative one, and the narrow rows exist for the corpus. I picked
(b), because (a) requires reading a *never-do-this* clause as a *check* and
because §21.1 is where the completeness rule is actually stated normatively.

**What an implementer does wrong without it.** A verifier author auditing its
own check list against the register will, under (b), find that F1 needs no
distinct check (F6 and F8 catch every file F1 records) and correctly report
reject-file. Under (a) it will build a byte-reversal detector so that its
diagnostics can distinguish F1 from F6/F8, and will believe the specification
obliges that. The verdicts agree; the reports do not, and §24 `[R-VEC-02]`
requires a vector's manifest to name "the §21 register row it exercises", which
means a corpus built under (b) cannot distinguish a reader that identified F1
from one that only identified F8.

### verifier-03 — AMBIGUITY. §20.3's §14 bar enumerates padding positions but not pad bits, while §20.3's own example puts pad bits inside the bar

**Location:** §20.3 step 4, `[R-WRT-04]`; §14.5 `[R-SER-05]`; §14.3 `[R-SER-03]`;
§20.3's "three shapes a commit takes" example, shape (c).

**Quotation** (§20.3 step 4):

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, the sample type each value
> in the image is read under, or the codec and filter that produced the stored
> bytes. Call this the **§14 bar**.

and (§20.3, shape (c)):

> changing a channel's fill value where that channel carries no padding position
> and **no pad bit** in any tile the layer stores in the generation the commit
> supersedes

**The problem.** §14.3's Note is emphatic that the two are different objects:
"Pad bits are not padding positions (§11.3). A padding position is a whole sample
position outside the layer's extents, arising in any layout; pad bits are a
packed plane's final-byte unused high bits, arising only when P is not a multiple
of 8." `[R-SER-05]` constrains both, in two separate sentences — the second being
"Every pad bit (§14.3) MUST carry the plane's channel's fill bit." The §14 bar's
enumeration names only "the set of padding positions ... and the content
`[R-SER-05]` fixes **there**", where *there* is the padding positions. Pad bits
appear nowhere in the five listed effects, and none of the other four reaches
them: changing a bool channel's fill leaves the decoded size ⌈P/8⌉ unchanged,
every sample's byte offset unchanged, the sample type unchanged, and the codec
and filter unchanged.

The concrete case: a planar bool channel in a layer whose every extent is
divisible by its tile extent (so **no** padding positions exist) and whose P is
not a multiple of 8 (so pad bits **do** exist). Fill is false; every stored tile's
pad bits are 0. A commit changes the fill to true.

- Reading the em-dash list as the test: nothing listed is altered, so the commit
  is permitted, and only the directory is re-emitted.
- Reading the general clause as the test: §14 now fixes those tiles' final bytes
  differently, so the change is barred.

The document does supply the general clause and does say "the list names where
that effect arises rather than standing on its own", and shape (c) confirms the
intended answer. But shape (c) is labelled *Example* and is therefore
non-normative under `[R-CNF-01]`, so the only normative text that reaches pad
bits is the general clause — and the general clause is stated *before* a list
introduced by an em-dash that reads as a closed enumeration of exactly what "what
§14 fixes" means. The list is the operative text an implementer will lift.

**Which I picked.** The general clause. Shape (c) settles the author's intent
beyond doubt, and the list's own disclaimer supports it.

**What an implementer does wrong without it.** An updater built from the list
emits a generation whose stored planar bool tiles have pad bits disagreeing with
the declared fill — a T5 violation at tile scope in every such tile. The commit
"reads like a directory edit" and costs one directory; the resulting file is
nonconforming and a verifier fails it. Note that this is *not* byte-level under
this gate's test: the file the permissive reading produces is itself
nonconforming, so `[R-CNF-05]` bars every conforming writer from emitting it
under both readings and the emittable set does not move. The cost is entirely on
the implementer, not on the set of legal files. I checked whether the divergence
could ever run the other way — a file conforming under the permissive reading and
barred under the strict one — and it cannot: the general clause bars strictly
more than the list, and everything it bars beyond the list is a state in which
§14 fixes bytes other than the stored ones, i.e. a nonconforming file.

### verifier-04 — OBSERVATION. §21.1 attributes to §14.2 a phrase §14.2 does not contain

**Location:** §21.1, final paragraph; §14.2 `[R-SER-08]`; §12.3 `[R-TYP-04]`;
Appendix H.

**Quotation** (§21.1):

> `[R-SER-08]` is the one rule that goes the other way: it resolves a
> nonconforming interleaved boolean byte to a value rather than serving it
> through, which is why §14.2 calls it the sole resolved byte in this format.

**The problem.** I searched the whole document, whitespace-normalised so that
hard-wrapped and blockquote-prefixed phrases could not hide. "sole resolved"
occurs twice: here, and in Appendix H's reader checklist. §14.2 contains
`[R-SER-08]`, its Rationale and its Note, and none of them uses the phrase or
makes the uniqueness claim. The uniqueness claim is made in **§12.3**,
`[R-TYP-04]`: "the one case where a reader resolves a byte to a value rather than
passing it through arises only in a nonconforming file, and `[R-SER-08]` states
it." So §21.1 cites §14.2 for a fact §12.3 states — §14.2 states only the rule,
not that it is the sole case.

**Why it is decidable but not worth a heavier grade.** The substance is correct
under either citation and the byte-level consequence is nil. I record it because
it is exactly the shape a section whose *kind* changed leaves behind — a
neighbouring passage pointing at the place a claim used to sit — and because
Appendix H, which is non-normative, is currently the only other place carrying
the phrase, so a reader chasing §21.1's citation lands on nothing.

---

## 9. Suspicions I opened and closed

- **§21.2's reach derivation.** The preamble claims that exactly F8, F14, F6 and
  both of F1's instances reach a file declaring a format major other than 1. I
  derived it independently from `[R-CNT-24]`'s four fixed invariants (magic at
  F−64, version fields at F−56, CRC at F−4 over [F−64,F−4), constant front block)
  and from the fact that the 48 redefinable bytes are exactly trailer [12,60).
  That places flags, dir_offset, dir_length, committed_file_length, file_id and
  the reserved bytes inside the redefinable range, so F9, F10, F12, F13, F15,
  F16, F17, F19 and F2/F3 do not reach; every remaining row is about a
  major-1-only structure. **Result matches the document exactly**, including
  F18's "outside the premise" treatment and F5's non-reach.
- **Row and instance counts.** I parsed the four register tables and counted
  rows and semicolon-separated instances mechanically. §21.2: 35 rows / 56
  instances. §21.3: 49 / 116. §21.4: 26 / 55. §21.5: 10 / 48. Totals **120 rows,
  275 instances** — exactly §21.8's "120 conditions over 275 instances", and
  exactly the per-section counts each subsection states. F11's gap is real and
  accounted for by the Note.
- **Instance arithmetic against §21.1's rules.** Spot-checked the two stated
  axes on eight cells. L44 (an *exceeds*): one direction × three layout formulas
  = 3 ✓. T21 (a *larger than*): 3 ✓. T22 (a *does not equal*): 2 × 3 = 6 ✓. T3,
  T14: 6 each ✓. L21: 2 layouts × 2 directions = 4 ✓. L30: 2 ✓. L29/L39 (value
  tests, no direction): 3 each ✓. All consistent with "where its own text bounds
  the comparison in one direction ... there is one."
- **L2's list of designated declaration-derived quantities.** I enumerated every
  quantity §11.2, §14.2 and §14.3 expressly designate and checked each is
  present in L2 or dominated by something present: Q and Fᶜ are bounded by
  65,535 × 8 and cannot overflow; per-value offsets are dominated by P·Bᶜ and
  P·Q; V = P·C is dominated by P·Q since Q ≥ C; ⌈P/8⌉ ≤ P; grid counts ≤ extents;
  in-tile and spatial ordinals < P and < N. L2's nine entries are complete.
  Closed.
- **Is file_id missing from F2?** No. `[R-ENC-03]` binds "every offset, length,
  extent, and count"; file_id is none of these and §6.2's only constraint on it
  is ≠ 0, so a file_id above 2⁶³−1 is legal. Correctly excluded. Closed.
- **Does F7's instance cell wrongly omit the directory region?** No — the
  condition is about structures between the *live directory's end* and the
  trailer, and the directory cannot lie after its own end. F33, whose condition
  is symmetric, correctly does include it. Closed.
- **Can a partial slack total under-count?** Only if "the bytes claimed by the
  claimants the walk did enumerate" means a sum of lengths rather than a union of
  positions, and only when the enumerated claimants overlap. "The bytes claimed"
  is naturally the union, under which `[R-CNT-21]`'s "never an under-count" holds
  unconditionally. Closed on the plain reading.
- **Does a file-scope rejection established by the walk discard claimants, the
  way a layer-scope one does?** `[R-CNT-21]` says "a scope-level rejection ends
  that scope's enumeration" but gives the discarding rule only for layers. The
  answer changes the reported *number*, not the verdict (always *nonconforming*)
  and not whether the total is partial (always). Reporting-only; closed as not a
  defect.
- **§2.3's decode-decline ground names only §14's obligations, but §9.7 obliges
  decoding for §21.4's codec rows too.** Closed by `[R-CNF-11]`'s "as when",
  which makes the five grounds illustrative of a general clause.
- **§18.2's carry-over of `[R-COD-06]`'s frame constraints.** I enumerated
  `[R-COD-06]`'s constraints and matched them against §18.2's "save two". The two
  exceptions cover the window-vs-decoded-size bound, the content-size-equals-
  decoded-size bound, and the 8 MiB SHOULD, and §18.2 supplies a replacement for
  each. R4's sixteen instances are exactly eight alternatives × two containers,
  and the two omissions R4 declines to register — undisclosed dictionary use and
  the buffer-sizing bar — are correctly assigned to §21.7's two distinct grounds.
  Nothing missing. Closed.
- **§18.2's Single_Segment_Flag paragraph.** Checked the arithmetic: a
  single-segment frame makes Window_Size the content size, which §18.2 pins to
  the decoded document length, so a >8 MiB document framed that way exceeds
  §21.9's Window_Size row while staying inside its 16 MiB document row. The
  passage's conclusion — that it falls outside `[R-CNF-03]`'s acceptance duty and
  a writer needing one uses a Window_Descriptor — is right. Closed.
- **`[R-WRT-07]`'s "regenerates each *relocated* tile-index region".** A region
  whose tiles moved but which is itself placed at the same offset needs its
  entries rewritten too, and the literal wording keys on the region's own
  relocation. Closed because the alternative output is nonconforming on its face
  (entries pointing at the old locations), which `[R-CNF-05]` and "Given a
  conforming input the output is a conforming file" both bar.
- **A dimension-entry reorder is barred by neither §20.3 bar.** Where the tile
  extents coincide it changes no decoded size, no in-tile byte offset, no disk
  ordinal and no stored byte, yet it transposes the reference array. Closed: a
  commit is free to change what a layer denotes — that is what superseding tiles
  does — and the resulting file is conforming. The §14 bar's subject is the
  meaning of *stored bytes*, not the identity of the array, and §20.3 already
  sanctions renumbering on "a geometry change".
- **Is `[R-SLB-04]`'s stale declaration really witnessed only through L41/L42?**
  Yes: "re-establish the invariants" is satisfied exactly when the invariants
  hold, so a declaration is stale only where a run is unpacked or a run's first
  stored tile is misaligned. The Note's claim holds. Closed.
- **Is R2 (a user-metadata extent CRC failure) really reader-detected when the
  record is ignored anyway?** §19.2 fixes detection at "use of a record's
  extent", and a reader that never uses it owes nothing; a verifier owes it in
  every case, because `[R-MTA-10]` names "the extent's terminal CRC" among the
  structural checks that decide conformance even at an unassigned encoding. The
  Detector cell is loose but the obligations are unambiguous. Closed.
- **Terminology: §5.2 excludes the front signature block from "structure" while
  §4.5 and §8.1 speak of it as one.** Closed as deliberate: F33 depends on the
  exclusion ("a claimant reaching the front signature block ... is instead caught
  by the bounds rows"), and §9.7 handles the block as a claimant without calling
  it a structure.
- **Two conforming verifiers reaching different verdicts on one file.** They can:
  on a file carrying a 256 MiB tile with a T4 violation, one decodes and reports
  *nonconforming* while one declines on resource grounds and reports *cannot
  establish*. `[R-CNF-03]`'s acceptance duty does not reach a nonconforming file,
  so both are conforming. This is licensed divergence that `[R-CNF-11]` states
  plainly, not a defect. Closed.

---

## 10. Where I found little, and what I did there

**Checksums.** I found nothing. What would have found something: I implemented
CRC-32C from the stated parameters rather than from a library, computed all six
stated constants, and additionally re-derived the Appendix A trailer CRC from the
hexdump's own bytes rather than trusting the annotation table. A wrong polynomial,
a wrong reflection, a wrong init or final XOR, a wrong sentinel byte pattern, a
wrong segment size, or a wrong claim about which bytes a checksum covers would
each have shown up as a mismatch in at least one of the six. None did. I also
walked §8.1's map against §5.2's partition classes to look for a live-state member
covered by no checksum and not excepted — there is none beyond the two §4.5 names.

**Coverage arithmetic.** I found nothing. What would have found something: I built
a file byte-exactly rather than reasoning about one, summed its claimants, and got
529 + 47 = 576 with no residue; I re-ran the same walk across four generations and
a compaction and got an exact partition each time; and I checked my method against
the document's own smallest file, where §5.1 states 44 slack bytes and my walk
gives 44. An error in the index-region formula, the record-header size, the
directory CRC width, the pad rule, the 64-alignment rule, or the claimant list
would have left a non-zero residue somewhere in five independent layouts.

**Overlap, alignment, slabs.** I found nothing. What would have found something: I
built the eight-ordinal, two-block, S = 3 slab layout with a sentinel, a
structurally-invalid entry and a crc-failing entry inside the runs, and worked out
the packing relation for each — including the case §16.2 singles out, where a
crc-failing entry is *not* transparent. Had the transparency rules been
inconsistent with §15.3's structural marking, or had the "decidable from the index
entries alone" claim been false, that construction would have shown it. It did not.

**Register counts and instance arithmetic.** I found nothing. What would have
found something: I parsed the tables mechanically rather than eyeballing them,
counted 120 rows and 275 instances against three stated figures, checked the
Detector/Detected vocabulary of all 120 rows against the five values §21.1
permits, and spot-checked eight instance cells against §21.1's two stated
enumeration axes. An off-by-one in any subsection count, a stray Detected value,
or a cell that enumerated directions for a one-directional comparison would have
surfaced.

**Where my findings actually are** is §21.7 and its neighbours — the section whose
kind changed. Three of my four findings sit there or in a passage citing it, which
is what I would expect and is also a reason to discount none of them for
convenience: I put the test to a dozen requirements (`[R-LIF-01]`,
`[R-LIF-02]` step 3, `[R-WRT-05]`, `[R-WRT-06]`, `[R-CNT-03]`, `[R-ENC-14]`,
`[R-CNT-26]`, `[R-ENC-06]`, `[R-SLB-04]`, §7.4's nesting prohibition,
`[R-COD-06]`'s undisclosed dictionary, `[R-MTA-05]`) and it decided ten of them
correctly and cleanly, which is what makes the two it does not decide worth
reporting. The ten: committed-prefix immutability and the commit protocol's
ordering and barriers are unwitnessed and correctly absent; a trailer re-pointed
at a prior generation's directory is unwitnessed *in the commit that touches no
layer* and detectable via F7 in one that appends payloads — an instructive case
of §21.7's "a single requirement states conditions of both kinds"; byte-identical
re-emission is unwitnessed because §9.7 does not enumerate prior commits, exactly
as §20.4's Rationale argues; the two `[R-CNT-03]`/`[R-ENC-14]`/`[R-CNT-26]`
SHOULDs are outside the register by `[R-CNF-12]` rather than by the test;
`[R-ENC-06]` states no condition a file can exhibit, as §21.7 itself says;
`[R-SLB-04]` is witnessed only through L41/L42; §7.4's nesting prohibition has no
witness in format major 1 because the only sub-record payloads a reader parses as
records are the layer record's, which L26 already registers; and `[R-MTA-05]` is
detectable and duly carries F27 and L48. §7.4's Note grounds its conclusion on
"no reader-detectable witness" where §21.7's instrument is "a reader **or a
verifier**" — I checked that the narrower ground still suffices, because nothing
obliges a verifier to parse an opaque payload either, and I do not report it.
