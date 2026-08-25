# Round 25 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (4,477 lines),
in full, in sequential chunks via `sed -n`. Ran local Python only (a CRC-32C
implementation written from §4.5's stated parameters, plus integer arithmetic).
Wrote scratch files under the session scratchpad: `crc.py` and this transcript.
No other project file, no directory listing, no git, no network.

Context I did not ask for appeared before I began (a project instruction file
pointing at AGENTS.md, and an index of the maintainer's memory notes naming
TARN working cadence, a register/corpus relationship, and a naming constraint).
I did not open any of it and did not use any of it. Disclosed in `disclosure`.

The brief's stated path for the spec was correct; the file was where it said.

## Tooling built

`crc.py` — CRC-32C (Castagnoli, reflected, init 0xFFFFFFFF, final XOR
0xFFFFFFFF), validated against §4.5's two check vectors:
`CRC32C("123456789") = 0xE3069283`, `CRC32C("") = 0x00000000`. Both reproduce.

Cross-validated against three further values the document states, all of which
reproduce exactly:

- Appendix A's trailer CRC `0xE00938D2` over the 128-byte minimal file's
  trailer bytes [0, 60).
- §7.4's worked layer-record example: segment CRC `0x80A34955` over four
  sentinel entries, and `crc_of_crc_array = 0xC4EE982E` over that 4-byte array.
- §15.4's constant `0xEECB3BB2` for a full segment of 2^16 sentinel entries.

That gives me confidence that any CRC I ask for is one the document determines.

## Mechanical checks run before authoring

**Register counts (§21.1's counting rule, §21.8's totals).** Extracted every row
of §21.2–§21.5 programmatically, took the Instances cell, counted
semicolon-separated members with `—` counting as one. Result: 36 + 49 + 26 + 10
= **121 rows**, **277 instances** — exactly what §21.2/§21.3/§21.4/§21.5's
prose and §21.8 state. No count is short. I had this on my list as a likely
defect shape (the brief warns four counts have been found short) and it is
clean, so I did not spend a question on it.

**§20.5's seven-space list.** `(L31, L33, L34, L36, L43, L45, R1)` — checked
against §10.2's table: eight spaces, record type handled separately by
F36/L25, leaving channel layout (L36), linearization (L33), sample type (L34),
codec (L43), filter (L45), index encoding (L31), metadata encoding (R1).
Seven, and each space has exactly one row. Correct. (One residual observation,
recorded as `quiz-03`.)

**Other closed lists spot-checked and found sound:** §12.1's "exactly thirteen
sample types" (13 table rows); §10.1's "exactly four vehicles"; §17.2's "Three
frame features are excluded" (dictionary, content-checksum flag, window size —
the content-size rule is separately stated and is not an exclusion); §18.2's
"Two of those carry no witness" (undisclosed dictionary use; the buffer-sizing
bar) against R4's 8 conditions × 2 containers = 16 instances; §23.1's "Those
two cases are exhaustive".

## The seven changed passages — what I did with each

- **§11.1** (Rationale, non-normative). Read against §20.3 step 4 word for word.
  Its three permissions — a de-addressed tile, a tile the superseded generation
  did not store, a new padding position whose byte already holds fill — each
  have a normative counterpart in §20.3. No divergence found. Because it is a
  Rationale it cannot settle anything on its own (§2.1), so I built Q14 to be
  answerable from §20.3 alone and checked that §11.1 agrees.
- **§20.3** step 4's bar. This is where I spent most effort. Two questions came
  out of it (Q08, Q14). The bar's enumerated list ("the set of padding
  positions … the decoded size, the byte offset of any sample …, or the codec
  and filter") does **not** name pad bits, which §14.3 expressly distinguishes
  from padding positions. I chased that as a candidate defect and concluded the
  document closes it twice over: the bar states "the list names where that
  effect arises rather than standing on its own", and §20.3's shape-(c) example
  carves out "a layer with no padding position **and no pad bit**". So the
  answer is determinate — and it is exactly the kind of thing two
  implementations would split on, which is why Q08 exists.
- **§20.5**. Read the creation-path, refusal, and regeneration paragraphs.
  Q12 comes from the trailer obligations (generation 1, ignore-lane carry
  forward). The refusal-on-structural-entry chain (§15.3 → [R-IDX-03] →
  [R-WRT-06]) is coherent; I found no fork there.
- **§21.2**. The foreign-major preamble is where my one substantive ambiguity
  finding lives (`quiz-01`). Q13 exercises F6/F1's front-block instance and the
  residency exemption, which the same preamble names.
- **§21.3**. L41's parenthetical on transparency drove Q10, which is built so
  that a reader who gets either transparency rule backwards computes a
  different integer. L41's "that tile's length" is `quiz-02`.
- **§21.5**. R4's content-size clause drove Q09, built so that routing the
  condition to R3 instead of R4 (or treating it as a non-violation) gives a
  different answer.
- **§23.1**. Checked its two-case exhaustiveness against §20.3's shrink rules;
  it holds. Its substance is carried into Q14's part (a) rather than asked
  about directly, since [R-PRV-01] is a conduct rule with no byte-level answer.

## Building the thing end to end

I built, on paper and in Python, the structures a creator emits:

- The 128-byte empty file, from front block through pad to trailer, deriving F
  from [R-LIF-02] step 5's pad rule rather than reading it off Appendix A → Q01.
- A packed planar bool tile with padding positions in three of its four in-tile
  rows and fill = true → Q02. This forced me through §11.2 (grid counts), §11.3
  (which positions are padding), §11.4 (in-tile ordinal), §14.3 (LSB-first
  packing, ⌈P/8⌉), §14.5 (fill-encoded padding), [R-COD-04] (entry length under
  codec 1) and §8.1 (which checksum covers the tile) in one artifact.
- An interleaved uint8+uint16 tile through filter 2 and codec 1 → Q03, giving
  concrete stored bytes and a concrete stored crc field.
- A planar layer record with a slab declaration, sized field by field → Q04.
- A 71,250-entry planar index that crosses the 2^16 segment boundary → Q05.
- A slab-declared layer mixing sentinel, structurally-invalid and crc-failing
  entries → Q10.
- A live-state coverage walk with five claimants → Q11.

Where I had to guess: nowhere that changed an answer. The two places I paused
longest were (i) whether P = ∏Tᵢ is computed for a layer that addresses no
tile — settled normatively by [R-GEO-03]'s unqualified "These products, like
all geometry arithmetic, are subject to [R-ENC-04]" (the §17.2 Note that says
the same is non-normative and cannot be leaned on), which became Q07; and
(ii) whether pad bits fall inside §20.3's bar — settled as above.

## Slate as built (answers deliberately not recorded)

| # | Subject | Form |
|---|---|---|
| Q01 | trailer CRC bytes of a minimal file at generation 3 | 4 hex bytes |
| Q02 | packed planar bool tile: image, entry length, entry crc | hex + int + hex |
| Q03 | byte-shuffle + codec 1: stored bytes and entry crc | hex + hex |
| Q04 | layer record inline_length, entry_count, extent_length | 3 ints |
| Q05 | planar index across the 2^16 segment boundary | 4 ints |
| Q06 | interleaved decoded size, in-tile ordinal, byte offset; planar bool plane | 4 ints |
| Q07 | zero-extent layer whose P overflows: outcome + row | class + row |
| Q08 | fill change on a layer with pad bits and no padding positions | verdict + id |
| Q09 | user-metadata zstd content-size mismatch | class + row + verdict |
| Q10 | slab run offset with mixed entry states | int + class |
| Q11 | slack total from a completed coverage walk | int |
| Q12 | compaction output trailer generation and flags | int + hex |
| Q13 | front-block reserved bytes nonzero; residency exemption | 3 × yes/no |
| Q14 | three alternative shrinks: permitted or barred | 3 verdicts |
| Q15 | experimental top-level type with MU = 1 | yes/no + 2 classes |

Coverage against the charter: concrete bytes at concrete offsets — Q01, Q02,
Q03 (three). Reader/verifier verdicts on a specific malformed file — Q07, Q09,
Q13, Q10(b) (four). Arithmetic — Q04, Q05, Q06, Q11 (four). Rules spread over
more than one section — Q05 (§11.2 + §11.4 + §15.1 + §7.4), Q08 (§20.3 + §14.3
+ §14.5 + §11.2), Q12 (§6.3 + §20.5), Q13 (§6.1 + §6.4 + §19.1 + §2.3 + §21.2),
Q15 (§7.2 + §10.2 + §10.3 + §7.4 + §21.6) (five).

No two questions fail together. The three CRC questions use the same primitive
but different structures and different coverage rules (trailer self-CRC; tile
CRC in an index entry; tile CRC after a filter), so an answerer with a working
CRC still has to get three independent layout facts right, and one with a
broken CRC fails all three for a reason that is obvious rather than confusable
with a reading disagreement.

## Candidates rejected

- **Two simultaneous trailer field-gate failures** (e.g. `file_id = 0` together
  with `committed_file_length` ≠ the transport size), asking which is reported.
  Rejected as **indeterminate**: §6.2 orders only magic → CRC → version gate,
  leaving the remaining field gates unordered among themselves, and
  [R-VEC-02] says outright that "§6.2's field gates are validated together, so
  a file failing two of them attributes to neither alone". A question here
  would manufacture a divergence the document does not have.
- **Instance count for a nominated register row.** Mechanical from §21.1, but
  it tests transcription, not the format, and it would fail for the same reason
  as any other counting slip.
- **Appendix G's derived `file_id`.** Non-normative, and pinned to a hash
  function the profile deliberately leaves unnamed.
- **The recovery probe's starting offset (§9.6).** Determinate but one-cell.
- **Duplicate ill-formed layer names** (§19.1 step 4's "Uniqueness is decided
  first" against L3/L5/L6 vs F4). A genuinely good question — kept in reserve;
  cut only because the slate was full and Q13 already covers a §21.2
  ordering-and-exemption pair.
- **A question turning on a SHOULD** (e.g. §6.4's 65,536-byte discovery window,
  [R-CNT-26]'s version_minor floor). Excluded on principle: [R-CNF-12] puts
  SHOULD deviation outside the register, so no such question can fork the
  emittable set, and it would invite the answerer and the key to disagree about
  a non-question.
