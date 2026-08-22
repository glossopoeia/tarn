# Round 20 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in full,
in seven `sed -n` slices. No other file was read; no directory listing; no git; no web.
Local computation only: Python for CRC-32C, ceiling arithmetic, and a mechanical count of
the register's Instances cells (that count reads the one permitted file via a Python
`open()` — the same file, no other).

Context contamination: my runtime placed a project-instruction pointer and an index of the
maintainer's memory notes in context before I began, naming round position and prior
findings. I did not open any of it and did not use it. Disclosed in the structured result.

## Reading order

1. Whole document cold, front to back (§1 → Appendix H).
2. Re-read §7.4, §20.5, §21.6 with the changed-surface hint in hand.
3. Numeric self-checks (below) to make sure I only build questions on ground the document
   actually determines.

## Self-checks run (all against the document's own stated values)

- CRC-32C implementation validated against §4.5's check vector: `"123456789"` → 0xE3069283,
  zero bytes → 0x00000000. Both reproduce.
- §7.4's worked layer-record example: 4 sentinel entries (80 bytes) → segment CRC
  0x80A34955; crc_of_crc_array over those 4 bytes → 0xC4EE982E. Both reproduce.
- §15.4's full all-sentinel segment constant 0xEECB3BB2 reproduces (2^16 entries).
- Appendix A's trailer CRC 0xE00938D2 over trailer bytes [0,60) reproduces, which also
  validates my field packing of §6.2's layout.
- §15.4's two examples (entry_count 1,000,000; planar C=4 N=32) check out arithmetically.
- §21.8's "121 conditions over 273 instances": counted mechanically under §21.1's rule
  (semicolon-separated, a `—` cell is one instance) — 36+49+26+10 = 121 rows, 273 instances.
  Both reproduce.

The document is arithmetically self-consistent everywhere I probed. That mattered for
question design: it means I can ask for computed bytes without the answer forking on a
typo in the source.

## How I chose the slate

I built the slate around one principle: a question earns its place if a reader who guesses
wrong at it emits different bytes or reaches a different verdict. So I preferred questions
whose answer is a byte string I computed myself, or an outcome name the register and the
governing rule together fix.

Weighting: the brief says the newest text is §7.4, §20.5, §21.6. Q01, Q02 and Q09 sit on
§7.4; Q11 and Q12 sit on §20.5; Q09, Q10, Q14 and Q15 turn on §21.6's non-violation
inventory and its two closing paragraphs. That is nine of fifteen on the changed surface.
The other six are the end-to-end build the charter asks for — open, geometry, tiling,
serialization, filter, codec, index, commit — which is where rounds 18 and 19 found their
survivors.

Coverage against the charter's required spread:

- Concrete bytes at concrete offsets: Q02 (two chained CRCs), Q03 (a whole stored tile plus
  its entry crc), Q04 (a packed bool plane with padding and pad bits), Q07 (a trailer's CRC
  field after a commit).
- Reader/verifier verdicts on a specific malformed file: Q08, Q09, Q10, Q12, Q13, Q14, Q15.
- Arithmetic: Q01 (inline_length and extent_length), Q05 (ordinals and in-tile offsets),
  Q06 (index-region byte offsets), Q07's slack total, Q14's decoded-size cap.
- Rules spread across more than one section: nearly all. Q03 spans §11.2/§11.3/§14.2/§14.5/
  §17.1/§17.3/§15.1/§4.5. Q14 spans §17.2/§11.2/§20.3/§21.3/§21.6.

Independence: I checked that no two questions fail for one reason.
- The [R-CNT-17] extent_length formula appears only in Q01. I deliberately removed it from
  Q02 and Q06, which would otherwise have shared its failure mode.
- Q02 and Q03 both compute a CRC-32C, but over different stages of different pipelines;
  Q02's trap is the partial-segment rule ([R-IDX-05] forbids substituting 0xEECB3BB2), Q03's
  is which stage the entry crc covers (filtered/stored, not the decoded image).
- Q05 and Q06 both use §11.4 ordinals, but Q05 is in-tile + spatial + in-sample offset and
  Q06 is spatial + planar disk ordinal + region layout. A row-major misreading breaks both,
  which is the one overlap I accepted; the two answers are different shapes (a byte offset
  inside a tile vs a byte offset inside an index region), so a divergence is diagnosable.
- Q09 and Q10 both concern unassigned record types, but they land on opposite sides of the
  experimental/reserved line and opposite scopes, which is exactly the discrimination
  §21.6's closing paragraph exists to make.

## Questions I built and then rejected

- **"What is the smallest conforming file, byte for byte?"** Rejected: Appendix A prints it.
  A lookup, not a derivation.
- **"How many slack bytes does a verifier report for the Appendix A file?"** Rejected for
  the same reason — §5.1's example states 44. I kept the idea but moved it onto a file the
  document does not print (Q07's generation-2 file, where the answer is 172).
- **"Which sample types are core?"** Rejected: quoting a table back.
- **A question on `[R-CNT-26]`'s version_minor floor.** Rejected on the SHOULD discriminator:
  `[R-CNF-12]` puts SHOULD deviation outside the register, so no answer to it can move the
  emittable set. Same reason I dropped a question on `[R-TYP-10]`'s zero fill default and on
  §6.4's 65,536-byte discovery window.
- **A question on which of T7 and T11 a vector attributes an entry with `offset = S`,
  `length = 5` to.** Both rows fire, both give reject-tile, and §21.1's specialization list
  (F1/F6/F8, F35/F36, L24/L25) does not name this pair. Same outcome either way, so it
  cannot fork bytes; I dropped it rather than ask a question whose answer is a corpus
  bookkeeping convention.
- **A duplicate-layer-name question** (two byte-identical, ill-formed name fields → §19.1
  step 4 decides uniqueness first, over raw bytes → reject-file at open). Good question, cut
  purely for slate space in favour of the §20.5 and §21.6 material the brief weights.
- **"Must a compactor's output file_id differ from its input's?"** Rejected as
  indeterminate-by-design and therefore unfair as a quiz item: `[R-WRT-06]` binds the *draw*
  ("a new draw ... not merely a value compared against the input's"), not the resulting
  inequality, so a collision produces a conforming output. I kept the safe half of it
  (may the output *reuse* the input's identifier — no) inside Q11.
- **A question asking whether an experimental-range MU = 1 *sub-record* leaves the file
  conforming.** I kept this, as Q09 part (c), but only after satisfying myself it is
  determinate: `[R-CNF-02]`'s conduct/bytes split, §21.1's normative register completeness
  (no row exists for it), and §21.6's closing paragraph together fix it. The tension I found
  along the way is reported as a finding rather than hidden in a question.

## Findings hit while authoring

Two, both reported in the structured result: `quiz-01` (AMBIGUITY, not byte-level) on §2.3's
unscoped acceptance carve-out against §7.4 `[R-CNT-18]`'s MUST NOT, and `quiz-02`
(OBSERVATION) on §21.7's count of §20.5's unwitnessed trailer obligations.

No question on the slate turned out to lack a determinate answer, so no question was
replaced on that ground.

## Note on form

Every question that asks for hex states the case. Every question that asks for a number
states the unit. Every question restates the whole scenario, since the answerer sees the
question text and the document and nothing else. No answers appear in this transcript or in
any question text.
