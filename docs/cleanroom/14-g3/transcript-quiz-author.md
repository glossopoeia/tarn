# Cleanroom round 14 — quiz author transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,168 lines, in four `Read` calls plus one `wc -l`). No `docs/`, no ADRs,
no `PLAN.md`, `AGENTS.md`, `README.md`, `OPEN-QUESTIONS.md`, no
`conformance/`, no `spec/registry.json`, no git history, no web. No directory
listings. Did not read the round14 output directory.

Local computation only, in Python, over data I typed in from the spec:
- a CRC-32C implementation (Castagnoli reflected, init/final 0xFFFFFFFF)
  checked against §4.5's own check vector;
- CRC of the §7.4 layer-record example's index region and CRC array;
- CRC of Appendix A's trailer bytes [0,60);
- CRC of a full 2^16-sentinel segment;
- a mechanical instance count over §21.2–§21.5 (regex over the register
  tables in the one file I am allowed to read);
- the arithmetic behind every question I authored.

Scratch files written: `crc.py`, `appa.py`, `inst.py` under my own scratchpad.

## Verification pass (before authoring)

Everything below reproduced exactly what the document states, so none of it
is a finding:

| Check | Document's value | Computed |
|---|---|---|
| CRC-32C("123456789") (§4.5) | 0xE3069283 | 0xE3069283 |
| CRC-32C(zero bytes) (§4.5) | 0x00000000 | 0x00000000 |
| §7.4 example: CRC over 4 sentinel entries (80 B) | 0x80A34955 | 0x80A34955 |
| §7.4 example: crc_of_crc_array over `55 49 A3 80` | 0xC4EE982E | 0xC4EE982E |
| §15.4: CRC of a full all-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 |
| Appendix A trailer CRC over [0,60) | 0xE00938D2 | 0xE00938D2 |
| §7.4 example inline_length | 81 | 81 (4+34+18+12+13) |
| §7.4 example extent_length | 84 | 84 |
| §21.2–§21.5 row count | 36+49+26+10 = 121 | 121 |
| §21.8 instance total | 268 | 268 |
| §15.4 example (entry_count 1,000,000) | 16 segs, 20,000,064 B, seg-rel 339,180 | all match |
| §11.4 example (300,700) | s=10, in-tile 11,452, planar disk 74 | match |
| §14.2 example (t float32 + m bool) | Q=5, size 30, sample at [25,30) | match |
| §14.3 example (P=10, alternating) | `55 01` / `55 FD` | match |
| §17.3 shuffle example | `00 00 00 00 00 00 80 00 40 3F 40 40` | match |
| §20.3 example (32 tiles) | 32·20+4 = 644 | match |
| §5.1 / Appendix A 128-byte minimum | 16+4 → pad to 64 → +64 = 128 | match |

The §7.4 worked byte example is internally consistent to the byte, including
both CRCs and the 81-byte field accounting.

## How the slate was chosen

The brief points at the previous round's repairs (§2.3, §4.7, §5.2, §11.1,
§16.2, §20.3, §21.1–§21.7, §21.9, §24, Appendices G and H). I read those
seventeen sections as an implementer, then built the artefacts they govern:
a layer record's inline payload, an index region, a slab run, a decoded tile
image at a padded edge, a commit's trailer, and a verifier's coverage walk.
Nine of the fifteen questions land on repaired text; the other six cover
arithmetic and byte layout no one round owns.

Distribution against the charter:
- concrete bytes at concrete offsets: Q01, Q02, Q03, Q11 (4)
- reader/verifier verdicts on a specific malformed file: Q08, Q09, Q10, Q15 (4)
- arithmetic (sizes, counts, alignment, coverage): Q04, Q05, Q06, Q07, Q12 (5)
- rules stated across more than one section: Q02, Q06, Q11, Q12, Q13, Q14, Q15

No two questions fail for the same reason. Q02 and Q13 both touch padding but
one is a decoded-image byte question and the other is an updater-permission
question; Q06 and Q12 both touch index entries but one is ordinal arithmetic
and the other is slab-run transparency.

The traps each question sets, stated as the fork a wrong reading produces:

- **Q01** — reading bfloat16's element size off §12.1's table (2) and its bit
  identification (high half of the binary32 pattern), then §7.4's channel-entry
  field order. Wrong → a 9- or 11-byte channel entry, or `c0 20` big-endian.
- **Q02** — the difference §14.3's Note draws between *padding positions* and
  *pad bits*. P = 16 so there are no pad bits at all; there are fifteen padding
  positions, whose bits §14.5 fixes to the fill bit. A reader who conflates the
  two emits `fe 00` or `01 00`.
- **Q03** — `[R-LIF-02]` step 5 says "pad to the next 64-byte boundary"; §6.2
  says a writer whose directory ends on a boundary "leaves none". I placed the
  directory end exactly on a boundary so the two readings give F = 960 vs 1024.
- **Q04** — §9.7 makes the front block and the live trailer claimants of the
  coverage walk; §5.2 does not repeat that. A walker who omits them under-counts
  the claimed bytes by 80 and reports 2872.
- **Q05** — planar addressed-tile count is C·N (§11.2), not N; and the §15.1
  region formula adds the segment-CRC array even for one segment.
- **Q06** — §11.4's spatial ordinal uses ∏_{j>i} G_j, and planar disk ordinal is
  c·N + s (channel-major), not s·C + c.
- **Q07** — §17.3's shuffle stride for an interleaved tile is Q, not the channel's
  element size; and the in-sample offset F_c sums the *preceding* channels' sizes
  with bool counting as 1.
- **Q08** — §2.3's priority rule: an established violation outranks any number of
  requirements the verifier could not check. A reader who takes the decode
  decline as controlling answers "cannot establish".
- **Q09** — §6.2 splits F7 (verifier) from the reader's dir-bounds check
  explicitly: "readers check neither".
- **Q10** — §4.2's value domain binds "every offset, length, extent, and count".
  `file_id` is none of those and §6.2 constrains it only to ≠ 0; `generation` is
  capped. A reader that clamps both, or neither, forks accept/reject.
- **Q11** — §20.3 step 2's repair: a malformed index entry met while re-emitting
  a region is carried forward byte-identically, *not* repaired to the sentinel.
  Two appenders otherwise emit different 20-byte entries.
- **Q12** — §15.3's structural/crc split, restated in §16.2: a structural-ground
  reject-tile entry is transparent to run continuity; an entry whose only defect
  is that its bytes fail its crc is not.
- **Q13** — §20.3's test is the effect on a stored tile, and a fill change reaches
  a stored tile only through §14.5's padding content. G·T = E on one layer and
  not the other.
- **Q14** — Appendix G item 3's two-level order: layers by name (tiles then index
  region), then record extents, top-level records before layer sub-records.
- **Q15** — §24's `[R-VEC-04]` verifier branch: where the detector is the verifier
  no reader is obliged to refuse, so the sibling may live in the same layer and
  the manifest still records the damaged scope's decoded content.

## Rejected candidates, and why

- **"How many instances does §21.8 count?"** — a lookup; and the answer is a
  number the register itself prints.
- **A CRC value as the answer** — divergence would indict an arithmetic slip
  rather than a reading. I used CRCs only as *inputs* (Q11's entry) or verified
  them myself against the document's own worked examples.
- **"Is the front signature block resident when a suffix window covers [8,128)?"**
  — §6.1's test is stated over bytes [0,16) as a unit; partial residency has no
  stated answer, so the question has no determinate answer and I dropped it
  rather than filing it. (Not filed as a finding either: no conforming file
  turns on it, and §6.1 gives the non-resident reader a MAY in any case, so both
  readings converge on permitted behaviour.)
- **"May a writer skip `[R-LIF-02]`'s barriers and still be conforming?"** —
  durability leaves no witness in the bytes; the answer is derivable but the
  question tests nothing about a file.
- **An instance-count question applying §21.1's criterion to a hypothetical row**
  — this is exactly the axis I found inconsistent (see finding quiz-01), so it
  has no single determinate answer. Filed as a finding instead.
- **"Which reading of §20.3's 'any tile that layer stores' governs?"** — filed as
  finding quiz-02 rather than asked, since I could not settle it from the
  normative text.

## The slate

(Answers deliberately not recorded anywhere in this file.)

**Q01** — §7.4 + §12.1 + §4.1. The seven bytes of a bfloat16 channel entry
with fill −2.5.

**Q02** — §11.2/§11.3/§11.4/§14.3/§14.5. The two bytes of a planar bool edge
tile's decoded image.

**Q03** — §9.2 step 5 + §6.2 + §5.1. Trailer bytes at offsets 24 and 40 when
the directory ends exactly on a 64-byte boundary.

**Q04** — §5.2 + §9.7 + §15.1. The slack total of a fully enumerated file.

**Q05** — §7.4 + §11.2 + §12.1 + §15.1. inline_length and extent_length of a
planar rank-2 layer record.

**Q06** — §11.2 + §11.4 + §15.1. Disk ordinal and index-region byte offset for
a planar rank-3 coordinate.

**Q07** — §14.2 + §12.1 + §17.3. Decoded-image offset and post-shuffle offset
of one sample's channel value.

**Q08** — §2.3 + §18.2 + §21.2. Verifier verdict when a decode decline and an
established violation coexist.

**Q09** — §6.2 + §21.2 F7 + §2.3. Reader obligation vs verifier verdict for a
structure in the pre-trailer gap.

**Q10** — §4.2 + §6.2 + §21.2. Accept/reject for extreme `file_id` and
`generation` values.

**Q11** — §20.3 + §15.3 + §20.4. The 20 bytes an appender must write for a
malformed index entry it carries forward.

**Q12** — §15.3 + §16.2. The offset a slab run's third entry must carry.

**Q13** — §11.2 + §11.3 + §14.5 + §20.3. Which of two layers admits a fill
change in an append.

**Q14** — Appendix G item 3. The profile's emission order for seven structures.

**Q15** — §24 + §21.4 T4 + §14.5. What a vector for a verifier-detected
reject-tile row must carry.

## Findings

Three, reported in the structured result as `quiz-01` … `quiz-03`. One
contradiction (§21.1's instance criterion against four register cells), one
ambiguity (§20.3's tense for "any tile that layer stores", whose only
disambiguating text sits in a non-normative Rationale that resolves it the
other way), one observation (§16.2's decidability claim needs F, which is not
an index byte).
