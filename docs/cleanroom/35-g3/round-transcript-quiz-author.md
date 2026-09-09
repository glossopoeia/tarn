# Cleanroom round 35 — quiz author transcript

## Access and disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,864 lines, read in full in six sequential `Read` calls, offsets 1/400/800/1200/1600/2019/2439/2859/3279/3699/4099/4499).
No other file in the repository was opened, listed, or searched. No git history, no
web access, no conformance corpus, no ADRs, no registry.json.

Local computation only, in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-round/scratch/quiz-author/`,
which was **empty** when I created it. Files I wrote there:

- `qa_check_r35.py` — a CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF)
  implementation, validated against the document's own two check vectors
  (`CRC-32C("123456789") = 0xE3069283`, `CRC-32C(<zero bytes>) = 0x00000000`)
  and then against Appendix A's published trailer CRC, which it reproduces.
  Used to confirm that Q01 has a determinate answer.
- `qa_arith_r35.py` — grid/ordinal/offset/packing arithmetic for the numeric
  questions, cross-checked against §7.4's 81-byte `sst` worked example and
  §11.4's and §15.4's worked ordinals, all of which it reproduces.
- `count_r35.py` — a mechanical parse of §21.2–§21.5's tables applying §21.1's
  instance rule ("Instances within a cell are separated by semicolons, and a
  cell reading — is one instance"). Result: 35/49/26/10 rows and 56/116/55/50
  instances, total **120 rows over 277 instances** — exactly §21.8's claim.
  No finding there; recorded because a mismatch would have been one.

Context I did not ask for: my runtime placed a project instruction file and an
index of the maintainer's memory notes in my context before I began. I did not
open any of the files they name and drew no conclusion from them; none of the
questions or findings below rests on anything in that material. Disclosed here
as the brief requires. The specification was where the brief said it would be.

No answers are recorded in this transcript or in any question's text.

## How the slate was chosen

The charter asks for byte-level questions, weighted toward the sixteen changed
passages, with at least three producing/validating concrete bytes at concrete
offsets, at least two reader/verifier verdicts on a specific malformed file, at
least two arithmetic, and at least two spanning more than one section. The
governing constraint I applied throughout: **the question must be one where the
document determines a single answer**, since a divergence indicts the key as
readily as the answer. Every numeric answer below I re-derived myself before
admitting the question, and every verdict answer I traced to the sentence that
fixes it.

Coverage of the changed surface: §4.7 (Q02, Q06 — the packed variable-length
payload whose table omits offsets), §6.4/§19.1 (Q01, Q08 — the trailer the open
validates), §11.1 (Q12 — the zero-grid-count growth), §15.2/§15.3 (Q11 — the
sentinel and the structural rows), §18.2 (Q10 — the frame constraints R4
registers and the content-size rule transposed to the decoded length), §20.3
(Q09, Q12 — the closed list of permitted changes), §21.1/§21.2/§21.4/§21.6
(Q07, Q10, Q11, Q14, Q15 — row attribution, detector, detection point, and the
defined non-violations), Appendix G (Q13 — item 2's "last eight bytes in output
order"), Appendix H (Q09, cross-checked against the updater checklist).
Unchanged text is deliberately also represented: Q03, Q04, Q05 sit in §11.4,
§14.2, §14.3, §15.1 and §15.4, on the record that rounds 18–22 and 30–33 found
their survivors in text no recent round had touched.

Spread as required:
- concrete bytes at concrete offsets: Q01 (trailer CRC field), Q04 (a decoded
  tile image including its pad bits), Q06 (a channel entry), Q13 (a derived
  `file_id`).
- reader/verifier verdicts on a specific file: Q07, Q08, Q10, Q11, Q14, Q15.
- arithmetic: Q02, Q03, Q05, Q12, Q14.
- rules spread across more than one section: Q02 (§7.4 + §11.2 + §12.1 + §15.1),
  Q05 (§11.2 + §11.4 + §15.1 + §15.4), Q08 (§2.3 + §6.3 + §21.2's note),
  Q10 (§18.2 + §21.1 + §21.5), Q11 (§15.3 + §16.2 + §21.4), Q14 (§11.2 + §14.2
  + §14.3 + §17.2 + §21.3).

No two questions fail together for the same reason: the CRC question fails on
checksum parameters, the layout questions on packing arithmetic, the ordinal
questions on linearization, the verdict questions each on a different rule
(quarantine, reach, frame constraints, structural transparency, the lz4 cap,
the reserved range).

## The slate

**Q01 — trailer CRC field.** A 192-byte file with all trailer fields stated;
asks for the four bytes at [188, 192) in lowercase hex. Requires assembling
§6.2's 60-byte layout correctly (field order, widths, little-endianness) and
applying §4.5's exact CRC-32C parameters. Wrong answer = a file every reader
rejects at F14.

**Q02 — layer record arithmetic.** A planar rank-2 two-channel layer, fully
specified; asks for entry_count, the index region's extent_length, and the
inline payload's total byte length. Requires §11.2's ceiling division, §11.2's
planar C·N, §15.1/§7.4's `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`, §12.1's
element sizes, §4.6's length prefixes, and §4.7's rule that a packed payload's
field sizes follow from type or length prefix. Wrong answer = L21/L22.

**Q03 — interleaved decoded size and value offset.** Rank-3 tile extents, three
channels including a bool; asks for the decoded size and the byte offset of one
channel's value at a stated in-tile position. Requires §11.4's in-tile ordinal,
§14.2's table, and §12.1's bool-in-interleaved element size of 1.

**Q04 — packed boolean plane, including pad bits.** A planar bool tile with
P = 15 and a stated fill; asks for the complete decoded tile image in hex.
Requires §14.3's LSB-first packing, ⌈P/8⌉, and §14.5's rule that every pad bit
carries the plane's channel's fill bit — the half a writer most often gets
wrong, and a T5 violation when it does.

**Q05 — planar disk ordinal, entry offset, segment.** Asks for a tile's disk
ordinal, its entry's byte offset within the index region, and its segment index.
Requires §11.2's grid, §11.4's spatial ordinal and c·N + s, §15.1's 20·k, and
§15.4's segment partition.

**Q06 — a channel entry's bytes.** bfloat16 with fill 1.0; asks for the entry's
exact bytes. Requires §7.4's channel entry shape, §12.1's type identifier and
element size, and §12.1's bfloat16 identification with binary32's high half.

**Q07 — verifier verdict at an experimental-range metadata encoding.** Asks for
the verdict word and the reader outcome class. The point is §21.6's defined
non-violation and §18.2's rule that no document rule attaches at an unassigned
encoding, against §2.3's cannot-establish grounds.

**Q08 — reach, and the verdict on a foreign major.** A trailer declaring
major 3 whose reserved bytes are nonzero. Asks for the verdict and the
requirement identifier a reader refuses on. Tests §2.3's per-condition reach
test against §21.2's note that the reserved-bytes condition does not reach.

**Q09 — the closed list of permitted changes.** Nine candidate operations on a
planar layer that stored a tile; asks which a single commit may make. Targets
§20.3 step 4's newest text directly, including the switch between two mutually
exclusive placement declarations in one commit and the bar on extending and
shortening one channel list in one commit. The stem stipulates that every
resulting declaration satisfies every other rule, so the proviso paragraph
cannot make the answer turn on facts the question does not give.

**Q10 — R3 versus R4 routing for a frame's content-size field.** A document that
decodes cleanly but whose Frame_Content_Size disagrees with the decoded length.
Asks for the row, the outcome, and the detection point. This is §18.2's
transposition of `[R-COD-06]`'s tile rule onto the quantity a document has.

**Q11 — slab run continuity across a structurally invalid entry.** Asks for the
row the malformed entry exhibits, the outcome for its tile, and whether the run
violates §16.2's packing invariant. Tests §15.3's structural-transparency
paragraph against §16.2's run continuity.

**Q12 — a growth that raises one grid count while another stays 0.** Asks
whether the index region is re-emitted, and for the extent slot and entry_count
in the new generation. This is §11.1's newest clause read together with §20.3
step 4's re-emission trigger.

**Q13 — Appendix G's derived file_id.** A 32-byte digest is given; asks for the
resulting identifier. The appendix is explicit that it means the last eight
bytes in output order, read little-endian, and says why it does not say "low".

**Q14 — the lz4 cap on a planar layer.** Asks for the largest addressed tile's
decoded size, the row, and the outcome. Requires §14.2's planar numeric plane
and §14.3's packed bool plane, and `[R-COD-07]`'s largest-plane rule.

**Q15 — a reserved-range top-level record with MU = 0.** Asks for the reader
outcome, the row, and whether the file is conforming. Separates §21.6's
"read the same way" from `[R-CNT-15]`'s "emitting one is a violation", and
keeps F35 off the answer by setting MU = 0.

## Candidates considered and rejected

- **Counting §21.4's or §21.5's instances by §21.1's rule.** Determinate and I
  verified the totals mechanically, but the failure mode is arithmetic slips by
  the answerer and the key independently, which would produce a divergence that
  indicts neither the document nor a reading. Dropped as a lazy question in the
  charter's sense.
- **"How many descriptive fields does format major 1 define?"** One cell of §4.7.
- **Request counts for a remote open.** §6.4's Note says no request count is a
  conformance property and nothing bounds what a reader fetches; the question
  would have had no determinate answer, which is why the surface's own text
  exists.
- **The narrowest scope at which a reader may decline an oversized tile on
  resource grounds.** `[R-ERR-04]` lists candidate scopes but a tile's decoded
  size is a function of the layer's declarations, so "layer" and "tile" are both
  arguable and I could not settle it from the text. I replaced it with Q07 and
  Q08, which turn on verdicts the document fixes explicitly. Recorded as
  finding quiz-04 rather than asked.
- **Whether a commit may keep a slab declaration unchanged.** The permitted-change
  member names three verbs and the clause it delegates to names four
  dispositions; I judged the reading resolvable from the paragraph's opening
  "keeps its declarations, with these exceptions" but not cleanly enough to make
  a quiz answer. Filed as finding quiz-01.
- **A question on `[R-CNF-05]`'s second sentence.** The brief records that the
  argument has been made here before and did not survive; asking it would
  reproduce a settled dispute rather than test the document.
- **Anything turning on a SHOULD.** `[R-CNF-12]` puts SHOULD deviation outside
  the register, so no such question can fork the emittable set.

## Findings noted while authoring

Four, all reported in the structured result: quiz-01 (§20.3 step 4 / §11.1 —
the permitted-change member's verbs against the dispositions the delegated
clause names), quiz-02 (§11.1's Rationale restatement, which lacks the default
clause that makes §20.3's list complete), quiz-03 (§4.7's "each class being what
the one before it is not", and the "or verifier" widening against version_minor's
classification), quiz-04 (§21.9 / `[R-ERR-04]` — the narrowest declinable scope
for an oversized tile). None is byte-level; quiz-01's grading turns on §20.3
step 4's own express declaration that its bar binds the commit as an actor and
that no file is nonconforming by virtue of its violation, which is the
`[R-CNF-02]` discriminator the brief names.
