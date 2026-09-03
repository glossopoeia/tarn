# Round 29 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,697 lines, read in full in sequential `sed -n` chunks). No other file in the
repository was opened, listed, or searched. No git history, no web access.

Working files, all in my private scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/quiz-author/`:

- `qa_crc.py` — CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF) plus the
  Q1/Q6 arithmetic.
- `qa_trailer.py` — trailer byte assembly and its CRC.
- `qa_geom.py` — grid/ordinal/offset arithmetic and the packed-bool tile image.

Plus one inline heredoc `python3` invocation (no file written) that counted the
register's rows and Instances cells.

## Instrument calibration before use

Before trusting any computed number I made every instrument reproduce a value the
document itself states:

- CRC-32C of `"123456789"` -> 0xE3069283 (§4.5 check vector) — reproduced.
- CRC-32C of zero bytes -> 0x00000000 (§4.5) — reproduced.
- CRC-32C of a full 2^16-entry all-sentinel segment -> 0xEECB3BB2
  (`[R-IDX-05]`, Appendix B) — reproduced.
- CRC-32C of §7.4's 4-entry all-sentinel array -> 0x80A34955, and
  crc_of_crc_array over that stored array -> 0xC4EE982E (§7.4 worked example) —
  both reproduced, which also confirms that the segment CRC enters
  crc_of_crc_array as a **little-endian u32**, not as a big-endian one.
- Trailer byte assembly: Appendix A's trailer CRC 0x402F157E — reproduced from
  my own field packing, which confirms the offsets and endianness I used.

Every arithmetic answer in the slate was then produced by the same, calibrated,
code path.

## Register counting

I extracted every row of §21.2–§21.5 and applied §21.1's counting rule
("Instances within a cell are separated by semicolons, and a cell reading — is
one instance; the count is therefore mechanical once the cell is written").

Result: 35 + 49 + 26 + 10 = 120 rows; the Instances cells total 275. That
reconciles exactly with §21.8's "120 conditions over 275 instances", so the
counting rule is well-formed and Q07 is determinate. Had it failed to reconcile,
that would itself have been the round's finding; it did not.

## How the slate was chosen

The brief names §11.1, §18.2, §20.3, §21.1 and §21.7 as the changed surface. I
weighted eight of fifteen questions onto them (Q07 §21.1; Q08, Q11, Q12 §20.3;
Q09, Q10 §18.2; Q13 §21.7; Q14 §11.1/§17.2), and left seven on unchanged
byte-layout surface, because the brief also records that recent rounds found
their survivors in text no hunk had touched — a slate weighted entirely onto the
new sections would have blind spots exactly where the last several rounds found
their defects.

I put the §21.7 test to a dozen requirements before writing Q13, as the brief
asks. The ones the test decides cleanly, and that I therefore trust as question
material: an undisclosed zstd dictionary (unwitnessed — §21.7 and §18.2 both
name it), a mis-strided filter 2 in a layer with neither padding positions nor a
bool channel (unwitnessed — T26's own parenthetical says so), an interleaved
bool byte 0x02 at a real position (detectable, T2), a padding position not
holding fill (detectable, T4), and `[R-ENC-06]`'s field widths (no condition a
file can exhibit — §21.7's own worked case). Those five became Q13. The test
also decides L40, L41, F27 and R4 correctly when I put them to it.

Two requirements the test does **not** decide cleanly are reported as findings
rather than asked about: `[R-LIF-02]`'s durability barriers, and `[R-WRT-06]`'s
version_minor floor for a compactor.

## Questions rejected, and why

- **"Which §21.2 rows reach a file declaring format major 7?"** — §21.2's own
  prose derives the answer (F1, F6, F8, F14) in the paragraph above the table.
  A lookup, not a combination.
- **"Which register row records a top-level user-metadata record with extent
  slot (0,0)?"** — F21 versus F22 under §21.1's strict-specialization rule. Real,
  but a single-sentence lookup once you find the specialization list. Replaced by
  Q08, which uses the same section's arithmetic on a planar shrink instead.
- **"What is the CRC of Appendix A's trailer?"** — printed in Appendix A.
- **Anything turning on a SHOULD** — `[R-CNF-12]` places SHOULD deviation outside
  the register, so a divergence there could not be scored as a byte fork and
  would only muddy the key. `[R-CNT-03]`'s gap zeroing, `[R-CNT-26]`'s
  version_minor floor and `[R-ENC-14]`'s NFC advice were all considered and
  dropped for this reason.
- **A question on the exact zstd `Window_Size` derivation for a small tile** —
  §17.2's Note states that no conforming file turns on which derivation a reader
  implements, so there is nothing to fork.
- **A question asking for the total slack of a specific multi-generation file** —
  the answer is determinate but only relative to a placement I would have to
  stipulate at length, and `[R-SLB-05]` leaves placement free, so the question
  would be testing my stipulation rather than the document.
- **A verdict question on `[R-MTA-09]`'s verifier decline on the window ground** —
  dropped because I judge the phrase "the bound above" genuinely underdetermined
  between the size bound and the window bound; §21.5's intro resolves it, but a
  key writer who reads only §18.2 could land the other way. Reported as
  finding quiz-01 instead of asked.

## Design constraints I held to

- Every question is self-contained: the answerer sees the question text and the
  document, nothing else. Every geometry question therefore restates the
  declared dimension order, extents, tile extents, layout, channel order and
  types, codec, filter and linearization explicitly, because §11.4's ordinals and
  §14.2's offsets all turn on declared order.
- Every hex answer names its case (lowercase) and says whether it wants stored
  byte order or a u32 value, so a formatting difference cannot masquerade as a
  divergence.
- No two questions fail together. In particular Q02 restates its trailer fields
  explicitly rather than inheriting Q01's dir_length, so a slip in Q01's inline
  payload arithmetic cannot propagate.
- Required spread satisfied: concrete bytes at concrete offsets — Q02, Q03, Q06
  (Q04 and Q08 additionally give byte offsets); reader/verifier verdicts on a
  specific malformed file — Q09, Q10, Q14, Q15; arithmetic — Q01, Q04, Q05, Q06,
  Q07, Q08; rules spread across more than one section — Q11, Q12, Q13, Q14, Q15.
- No answers are recorded here or in the question text.

## The slate

Q01 — smallest inline_length, dir_length and committed_file_length for a file
whose directory holds exactly one layer record for a rank-1, zero-extent layer.
(§5.1, §6.2, §7.2, §7.4, §11.2, §12.1)

Q02 — the 4 trailer CRC bytes at trailer offsets [60,64), in file order, for a
fully specified trailer. (§4.5, §6.2, §4.1)

Q03 — the decoded tile image of the corner edge tile of a planar bool layer,
with fill true, plus the non-sentinel index entry's length field under codec 1.
(§11.3, §11.4, §14.3, §14.5, §17.2)

Q04 — disk ordinal, index-region byte offset of that entry, and in-tile byte
offset of the value, for a rank-3 planar float32 layer. (§11.2, §11.4, §14.2,
§15.1)

Q05 — decoded size, disk ordinal and in-sample byte offset for an interleaved
layer mixing int16, bool and float64. (§11.2, §11.4, §14.2, §12.1)

Q06 — extent_length and crc_of_crc_array for an all-sentinel layer with
entry_count exactly 2^16. (§7.4, §11.2, §15.1, §15.4, §4.5)

Q07 — instance counts of §21.2, §21.3, §21.4 and §21.5 under §21.1's counting
rule. (§21.1, §21.8)

Q08 — entry_count, extent_length and the entry's array position after a planar
layer's extent is shrunk so that N falls. (§11.2, §11.4, §15.1, §7.4, §20.3)

Q09 — register row and outcome class for a user-metadata frame whose
Frame_Content_Size disagrees with the decoded document length. (§18.2, §21.5)

Q10 — verifier verdicts for an experimental-range versus a reserved-range
user-metadata encoding byte. (§18.2, §21.5, §21.6, §2.3)

Q11 — permitted/barred for four channel-declaration edits to a planar layer that
stores tiles for exactly one channel. (§20.3, §11.4, §11.2)

Q12 — permitted/barred for three shrinks and one re-type of an interleaved
layer with one stored tile. (§20.3, §14.5, §11.3, §11.2)

Q13 — classification of five conditions under §21.7's unwitnessed / detectable /
no-condition-a-file-can-exhibit test. (§21.7, §17.2, §14.2, §14.5, §4.2, §21.4)

Q14 — validity of codec 4 declared on a zero-extent layer whose declared tile
shape exceeds the lz4 cap, and the row the layer exhibits after a growth.
(§17.2, §11.1, §11.2, §20.3, §21.3, §21.9)

Q15 — reader outcome and verifier verdict for an experimental-range layer
sub-record type carrying MU = 1. (§2.3, §7.4, §21.6, §10.3)

## Findings

Three, all reported in the structured result as quiz-01 .. quiz-03. None is
graded byte-level, and each says in its own rationale what already decides it.
