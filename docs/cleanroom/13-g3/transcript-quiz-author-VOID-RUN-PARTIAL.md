# Cleanroom round 13 — quiz author transcript

**No answers appear anywhere in this file.**

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,128 lines, in five sequential Read calls, plus two greps against that
same file for `renumber|positional`, `shrink|MAY always|grow`, and
`0xEECB3BB2|0x7E000000|65,536|2¹⁶`). Ran `wc -l` on that path.

Ran local Python that reads no files, in
`/private/tmp/.../scratchpad/round13/{calc,build,file1,q,verify}.py`:
a CRC-32C implementation (reflected poly 0x82F63B78, init/final 0xFFFFFFFF)
validated against §4.5's own check vector and against every CRC constant the
document publishes, plus grid/ordinal/offset/slack arithmetic and a
byte-shuffle round-trip.

No ADRs, no `docs/`, no `PLAN.md`, `AGENTS.md`, `README.md`, no
`conformance/`, no `spec/registry.json`, no git history, no directory
listings, no web. I did not read the round-13 output directory.

## Method

1. Read the document cold, front to back.
2. Re-implemented the document's own published constants from scratch to
   establish that the CRC parameters, the §7.4 worked layer-record example
   (`0x80A34955`, `0xC4EE982E`, the 81-byte payload arithmetic), §15.4's
   `0xEECB3BB2`, and Appendix A's trailer CRC `0xE00938D2` all reproduce.
   All did. That gave me a trusted arithmetic base to build questions on.
3. Built structures the document does not contain — a minimal one-layer
   file, a planar packed-bool edge tile, a filtered interleaved tile, a
   65,537-entry all-sentinel index, a slack accounting — and recorded every
   place I had to make a judgement call.
4. Chose questions where an implementer's wrong turn produces wrong bytes
   or a wrong verdict, not where a table can be quoted back.

## The slate, and why each earns its place

| id | crux | sections it forces together |
|---|---|---|
| Q01 | smallest conforming file with one layer record | §7.4 field list · §4.6 name floor · §12.1 element sizes · §11.1/§11.2 zero-extent layer · §7.2 header · §7.1 CRC · §6.2 64-alignment · §5.1 |
| Q02 | trailer CRC bytes from stated field values | §6.2 layout · §4.2 LE · §4.5 CRC params · §6.3 flag lanes |
| Q03 | one channel entry, bfloat16, fill −2.0 | §7.4 channel entry · §12.1 element size + bfloat16 identification · §4.2 |
| Q04 | 65,537 all-sentinel entries: region length, CRC array, crc_of_crc_array | §15.1 · §15.4 full-vs-partial segment · §7.4 · §4.5 LE storage |
| Q05 | planar packed-bool edge tile: disk ordinal, decoded byte, entry offset | §11.2 · §11.4 planar c·N+s · §11.3 padding · §14.3 packing · §14.5 padding+pad-bit content · §15.1 |
| Q06 | interleaved in-sample byte offset for a coordinate | §11.2 · §11.4 · §14.2 stride/offset table · §12.1 |
| Q07 | byte-shuffle at stride Q, stored bytes under codec 1 | §14.2 · §17.1 stage order · §17.3 shuffle · §17.2 codec-1 length equality |
| Q08 | verifier's slack total for a described file | §5.2 claimants · §9.7 walk (records are not their own claimants; sentinels claim nothing) · §15.1 |
| Q09 | verdict when the version gate fails and a later field looks bad | §2.3 three verdicts · §6.2 fixed validation order · §6.3 · §21.6 closing paragraph |
| Q10 | duplicate layer names that are themselves invalid, plus a truncated name field | §19.1 step 4 · §4.6 [R-ENC-13]/[R-ENC-15] · §21.2 vs §21.3 |
| Q11 | reserved-range top-level record type with MU = 0 | §7.2 [R-CNT-15] · §21.2 · §21.6 · §2.3 |
| Q12 | user-metadata record at an experimental encoding with non-JSON bytes | §18.2 [R-MTA-10] · §17.4 · §21.5 vs §21.6 · §2.3 |
| Q13 | slab run packing across a structurally-invalid entry vs a crc-failing one | §15.3 structural rows · §16.2 [R-SLB-03] · §21.3 L41 |
| Q14 | when an appender may drop an MU = 0 / PE = 0 record | §20.4 table · §20.3 step 4 |
| Q15 | instance count of §21.4 | §21.1 instance criterion · §21.4 cells |

Spread against the charter: concrete bytes at concrete offsets — Q02, Q03,
Q04, Q05, Q06, Q07. Verdicts on a specific malformed file — Q09, Q10, Q11,
Q12. Arithmetic — Q01, Q06, Q08, Q13, Q15. Rules stated across more than one
section — Q01, Q10, Q12, Q13, Q14.

Independence: no two questions fail for one shared reason. Q05 and Q06 both
touch §11.4 but on disjoint halves (planar disk ordinal + packing versus
spatial ordinal + interleaved stride). Q04 and Q08 both touch §15.1's region
formula, but Q08's crux is the claimant set, not the formula.

## What I rejected, and why

- **Reciting §15.4's `0xEECB3BB2`.** One table cell. Replaced by Q04, whose
  second segment is *partial* and so must be computed — the rule that
  actually forks bytes.
- **A hex dump of a whole 128-byte file to validate.** Transcription risk
  between answerer and key; a described-fields form is equally sharp and
  cannot diverge on a typo.
- **A question about the smallest one-layer file's trailer CRC.** It would
  have failed together with Q01 on any slip in the payload arithmetic.
  Q02 uses a fully-stated, independent trailer instead.
- **A question about which tier §21.5 R1's encoding-byte check falls in.**
  §19.1 step 4 enumerates a top-level user-metadata record's framing checks
  but not its encoding value set, while R1's *Detected* cell says "open".
  §21.1 makes the governing rule win and neither rule states a tier, so the
  answer is arguable — and the outcome (ignore-record) is the same either
  way, so nothing byte-level turns on it. Recorded as a finding rather than
  a question.
- **A question about extent shrinkage.** No determinate answer (see
  quiz-02). Reported as a finding instead, per the charter.
- **A zstd single-segment-flag question.** §17.2's note states the
  conclusion outright; the question would be a quotation.
- **Instance counts for §21.2, §21.3, §21.5 as separate questions.** Same
  failure mode as Q15; one is enough.

## Guesses I had to make while building

Recorded here because the charter asks for them, whether or not they became
findings:

1. Growing a dimension extent shrinks the set of padding positions of a
   stored edge tile. §20.3 step 4 forbids a commit that alters that set and
   then permits growth outright. I took growth as permitted (finding
   quiz-01).
2. Nothing normative forbids *shrinking* an extent where no stored tile
   gains a padding position; the only statement to the contrary sits in a
   §11.1 Rationale, which [R-CNF-01] makes non-normative (finding quiz-02).
3. For Q08 I had to decide that a layer record's tile-index region enters
   the coverage walk exactly once, as that record's extent, and that the
   record itself is not a claimant. §9.7 states both explicitly; no guess in
   the end.
4. For Q04 I had to decide that each segment CRC is stored as a
   little-endian `u32` — §15.1's array is "×4 bytes" and only §4.5's
   [R-ENC-09] says little-endian. Decided by [R-ENC-09]; no guess.
5. For Q01 I had to decide that a layer with every extent 0 has extent slot
   (0, 0) and `crc_of_crc_array` = 0, and that the minimum channel element
   size is 1. §7.4, [R-CNT-17], [R-CNT-23] and §12.1 all decide it.
