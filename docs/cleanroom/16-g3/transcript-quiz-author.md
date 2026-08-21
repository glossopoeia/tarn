# Cleanroom round 16 — quiz author transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,282 lines, in five `Read` calls plus a handful of `grep` passes against
that same file). No `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md` / `AGENTS.md` / `README.md`, no git history, no web. I did not read or
list the round-16 output directory.

Local computation only: `python3` with a hand-written CRC-32C table (no file
input) plus integer arithmetic, in
`scratchpad/round16/crc.py`, `q.py`, `q2.py` — scratch files I created myself.
The CRC implementation was validated against the document's own check vectors
before use: CRC-32C("123456789") = 0xE3069283 (§4.5), CRC-32C of zero bytes =
0x00000000 (§4.5), the 80-byte four-sentinel entry array = 0x80A34955 and its
crc_of_crc_array = 0xC4EE982E (§7.4's worked example), and Appendix A's trailer
CRC 0xE00938D2 over trailer bytes [0, 60). All four reproduced exactly, so the
CRCs behind the slate are computed with a checker the document itself certifies.

No answers are recorded in this file.

## How I worked

I did not walk the nine changed sections in order. I built things:

1. **A minimal one-empty-layer file, end to end.** Sized a layer record's inline
   payload field by field against §7.4's table (name … C = 34 bytes plus the
   name's prefix+bytes; dimension entries 1+len+16; channel entries
   1+len+2+1+elemsize; trailing fixed fields 13), framed it under §7.2's 24-byte
   header, added §7.1's terminal directory CRC, placed the directory at 16, and
   derived the pre-trailer pad and F from §6.2 and `[R-LIF-02]` step 5. The
   §7.4 worked example's own accounting ("4 + 34", "the dimension entry 18, the
   channel entry 12, and the trailing fixed fields 13 — 81 exactly") is what let
   me confirm the sizing rather than guess it.
2. **A planar layer with mixed bool/numeric channels**, sized its index region
   under `[R-CNT-17]`, located a specific entry and its covering segment CRC
   under §15.1/§15.4, and packed a bool plane's decoded image under §14.3 with
   §14.5's padding-position and pad-bit content.
3. **A slab-declared layer** with a deliberately mixed set of index entries —
   sentinel, crc-failing, two different §15.3 *structural* rows — and ran
   `[R-SLB-03]`'s packing relation over it, which is where the transparency
   asymmetry (structural entries transparent, crc-failing entries not) actually
   bites.
4. **A shrink/grow commit sequence** against §20.3 step 4, which is where I hit
   the one finding I believe forks the bytes.
5. **A verifier coverage walk** with one layer rejected, against §5.2's partial
   total.

I also mechanically re-derived §21.8's "121 conditions over 275 instances" from
the four register tables under §21.1's instance criterion: 36 + 49 + 26 + 10 =
121 rows, and 58 + 116 + 57 + 44 = 275 instances. Both check out; the instance
criterion as now written is self-consistent with every cell I sampled (T21 one
direction / T22 two directions × three layouts, L21/L22/L30 two directions, L37
and F14 checksum comparisons at one, F5's two fields, T24's *any codec* at one
against T25's three). That is a null result and I report it as such rather than
manufacturing a row-versus-rule complaint out of it — §21.1 already decides that
the rule governs, so a divergent cell would not be byte-level anyway.

## The slate — what each question is for, and what it must not fail with

| # | Buys | Sections it forces together |
|---|---|---|
| Q01 | trailer bytes at a fixed offset, incl. deriving flags/minor from §6.3 rather than being handed them | §4.5, §4.1, §6.2, §6.3 |
| Q02 | two concrete little-endian fields of a record header, both derived from a payload the answerer must size | §4.2 (u32/u64 widths), §7.2, §7.4, §12.1, §11.2, §15.1 |
| Q03 | packed bool image bytes — padding positions *and* pad bits, two different mechanisms §14.3's Note deliberately separates | §14.3, §14.5, §11.4, §4.4, §17.2 |
| Q04 | segment CRC of a **partial** segment, which §15.4 forbids substituting the all-sentinel constant for | §15.1, §15.2, §15.4, §7.4, §4.5 |
| Q05 | in-tile ordinal, spatial ordinal, and interleaved stride arithmetic in one | §11.2, §11.4, §14.2, §12.1 |
| Q06 | disk ordinal in a planar layer + the segment that covers it | §11.2, §11.4, §15.1, §15.4 |
| Q07 | §20.3 step 4's bar, in four shapes: grow, drop-a-tile shrink, retain-a-tile shrink, codec change | §20.3, §14.5, §11.2, §17.2 |
| Q08 | `[R-SLB-03]`'s transparency asymmetry + §15.3's six structural rows + `[R-CNF-09]` | §15.3, §16.2, §21.3, §21.4, §13.3 |
| Q09 | §21.1's specialization rule applied to a real record | §21.1, §21.2, §10.2, §7.2 |
| Q10 | *cannot establish* vs *nonconforming*, with an unassigned-encoding record as a decoy | §2.3, §18.2, §21.5, §21.6 |
| Q11 | partial slack total with a walk-established layer rejection discarding its own claimants | §5.2, §9.7, §21.3 |
| Q12 | compaction's trailer: generation, minor floor, ignore-lane carry-forward, fresh file_id | §20.5, §6.3, §9.3 |
| Q13 | Appendix G item 3's total emission order | App. G, §5.1, §6.2 |
| Q14 | the lz4 cap's quantifier over *addressed* tiles vs `[R-ENC-04]`'s unquantified overflow rule | §11.1, §11.2, §17.2, §4.2, §20.3 |
| Q15 | §21.7's account of what carries no register row, mixed with two conditions that do | §21.7, §21.3, §21.4 |

Failure-independence: no two questions fail for one reason. Q02 is the only
question needing layer-record payload sizing (I dropped a second one that did —
see below). Q04 and Q06 both touch §15.4 but on opposite halves (CRC value vs
array position). Q07, Q08, Q10, Q14 are four different verdict machines.

## Questions I built and rejected

- **"Smallest committed_file_length for the one-empty-layer file"** (answer
  derivable from §7.2 + §7.4 + §6.2). Rejected: it fails together with Q02 —
  both die on the same layer-record payload sizing. Q02 keeps the byte-level
  half; the pad/F arithmetic is already implicit in Q01's given trailer.
- **"Sum the Instances column of §21.3."** Determinate (I computed it), but it
  diverges for clerical reasons rather than for reading reasons, which indicts
  neither party usefully.
- **"Verify the all-sentinel constant 0xEECB3BB2."** 1.3 MB of input; a correct
  answerer without a code tool cannot produce it, and a wrong one cannot be
  distinguished from a lazy one.
- **"Which register row fires for a filter changed from 1 to 2 on a retained
  planar numeric layer?"** Folded into Q15 rather than asked alone; alone the
  answer is a bare "none", which a guesser reaches for free.
- **"A shrink that both drops a tile and re-pads a retained tile: permitted?"**
  Rejected *because it has no determinate answer* — this is finding quiz-01
  below, and Q07's scenarios are chosen to stay clear of it (its shrink cases
  are each unambiguously on one side of the split).

## Findings

Three. One I believe forks emitted bytes; two are accuracy defects in normative
prose that no implementation would actually act on.

- **quiz-01 (CONTRADICTION, byte-level).** §20.3 step 4's shrink permission
  ("where it drops a tile out of the addressed set entirely (§11.2's grid count
  falls), nothing is altered for a tile the new state stores, and the commit is
  permitted") is false whenever one shrink both drops a tile and re-pads a
  retained one. Worked counterexample: rank 1, E = 25, T = 10 → G = 3; shrink to
  E = 15 → G = 2. Tile 2 drops out of the addressed set *and* tile 1, stored in
  both generations, gains padding positions at x = 15…19 that previously held
  real samples. `[R-SER-05]` now fixes those bytes to fill; they do not hold it.
  §11.1's Rationale repeats the same either/or ("permitted where it drops tiles
  out of the addressed set"), which is non-normative but shows the reading is
  the intended one.
- **quiz-02 (CONTRADICTION, not byte-level).** §21.7's "witnessed only where
  … the change reaches a byte §14 structurally constrains … the §21.4 rows
  firing there and nowhere else" is contradicted by T14 and T25, which witness a
  codec or decoded-size change with no §14-constrained byte anywhere in the tile.
- **quiz-03 (OBSERVATION).** §20.5 lists the same alternative twice inside one
  "neither … nor … nor" construction.

Reserved values, reserved ranges and unresolvable forward references into them
are not reported.
