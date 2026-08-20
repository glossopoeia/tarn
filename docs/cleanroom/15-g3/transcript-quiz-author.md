# Cleanroom round 15 — quiz author transcript

**No answers appear in this file.** Constructions are described only to the
depth needed to show that each question has a single determinate answer.

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only, in
four `Read` calls covering lines 1–4227 (the whole file), plus one `grep`
against that same file for `T19` (the §21.4 table looked as though a row
were missing between T18 and T20 across a read boundary; it was not — T19 is
present at line 3397).

Ran: local Python only, in this scratchpad, reading no project files —
a CRC-32C implementation (Castagnoli, reflected, init/final 0xFFFFFFFF),
a trailer serializer, a layer-record inline-payload serializer, a
packed-bool-plane serializer, and a small script that re-counted the §21.2–§21.5
register rows and their Instances cells from the spec text.

Did not read: `docs/`, ADRs, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `CONTRIBUTING.md`, `conformance/`, `spec/registry.json`, git
history, the round-15 output directory, or any other agent's transcript.
No web access. `CLAUDE.md`/`AGENTS.md` content reached me only as the
harness's own system context, not by my reading a file.

## What I did before writing questions

I tried to build the thing rather than narrate the changed sections.

1. **Re-derived every constant the document states.** CRC-32C of
   `"123456789"`, of zero bytes, of an 80-byte four-sentinel entry array
   (§7.4's worked example), of the 4-byte array that example then covers,
   of a full 2¹⁶-sentinel segment (§15.4), and of Appendix A's trailer bytes
   [0, 60). All six reproduce the document's stated values exactly. That
   gave me a checked CRC oracle and confirmed §7.4's new worked example and
   Appendix A are internally sound.
2. **Re-counted the register.** A script parsed every `| F… | L… | T… | R… |`
   row of §21.2–§21.5 and applied §21.1's mechanical instance rule (a cell
   reading `—` is one instance; otherwise semicolon-separated). Result:
   121 rows; 36 F / 49 L / 26 T / 10 R; 57 + 115 + 57 + 44 = 273 instances.
   §21.2/§21.3/§21.4/§21.5's preambles and §21.8's "121 conditions over 273
   instances" all agree. I also hand-checked §21.1's two stated axes —
   layout-varies and magnitude-direction — against T3, T14, T21, T22, L21,
   L22, L30, L44, F17 and against the value-test carve-out (L20, L27, L28).
   Every cell I checked matches the criterion. I found no arithmetic defect
   in §21.
3. **Serialized layer records byte by byte** for two layers (a planar
   rank-2 two-channel layer; a rank-1 zero-extent layer) using §7.4's field
   order and widths, §4.6's length prefixes and §12.1's element sizes,
   cross-checking my serializer against §7.4's own 81-byte worked example
   (it reproduces 4 + 34 + 18 + 12 + 13 = 81).
4. **Serialized a packed boolean plane** with padding positions and pad bits
   under §14.3 + §14.5 + §4.4, and an interleaved sample stride under §14.2.
5. **Walked coverage** for a fully specified live state under §9.7 and §5.2,
   both for a complete walk and for the partial-total case §5.2's new text
   introduces.
6. **Traced the transparency rule** (structural reject-tile entries vs. an
   entry that fails only its stored bytes' crc) through all five places it
   appears — §15.3's preamble, §16.2, §9.7, §16.1/L40, and L41's condition
   cell. They agree in every direction I could test. If this is the rule
   that has been rewritten three rounds running, it now reads consistent.

## The slate — why each question earns its place

Each question is stated to stand alone; the answerer sees only its text and
the document.

| # | Turns on | Kind | Sections it forces together |
|---|---|---|---|
| Q01 | smallest file carrying one zero-extent layer | arithmetic / bytes | §5.1, §6.2, §7.2, §7.4, §11.1, §12.1, R-CNT-17, R-CNT-23 |
| Q02 | index-region bytes and the two checksums over them | bytes | §4.5, §15.1, §15.2, §15.4, §7.4, §8.1 |
| Q03 | a stored packed bool tile with padding positions and pad bits | bytes | §4.4, §11.3, §14.3, §14.5, §11.4, §17.1 |
| Q04 | interleaved sample stride and in-sample offset | bytes / arithmetic | §11.4, §12.1, §14.2 |
| Q05 | planar disk ordinal → index-region byte offset | arithmetic | §3.1, §11.2, §11.4, §15.1 |
| Q06 | index extent_length and segment split at an exact 2¹⁶ boundary | arithmetic | §7.4 R-CNT-17, §15.1, §15.4 |
| Q07 | slack total from a complete coverage walk | arithmetic | §5.2, §9.7, §7.4 R-CNT-17 |
| Q08 | partial slack total after a walk-established L18 | arithmetic / verdict | §5.2 (new text), §9.7, §21.3 |
| Q09 | slab packing across a transparent structural entry | bytes / verdict | §15.3, §16.2 (new text), §21.3 L41 |
| Q10 | compactor meeting a stored tile whose crc fails | verdict | §20.5 (new text), R-WRT-09 |
| Q11 | compactor relocating a slab-declared layer | verdict / spread | §16.2, §20.4, §20.5 |
| Q12 | reproducible-writer emission order → directory offset | bytes | Appendix G item 3, §15.1, §5.2 |
| Q13 | experimental-range MU = 1 sub-record | verdict / spread | §7.4 R-CNT-18, §2.3, §21.6 |
| Q14 | unassigned metadata encodings: experimental vs. reserved | verdict / spread | §18.2, §21.5 R1, §21.6, R-MTA-10 |
| Q15 | filter declaration change over already-stored tiles | verdict / spread | §17.3, §20.3 step 4 (new text) |

Balance against the charter's floors: concrete bytes at concrete offsets —
Q02, Q03, Q04, Q05, Q12 (five, floor three). Reader/verifier verdicts on a
specific malformed file — Q09's second half, Q10, Q14's file B (three, floor
two). Arithmetic — Q01, Q06, Q07, Q08 (four, floor two). Rules whose
statement is spread over more than one section — Q01, Q08, Q11, Q13, Q14,
Q15 (six, floor two).

Weighting to the newest text: §5.2 (Q08), §11.1/§20.3 (Q15), §16.2 (Q09,
Q11), §20.5 (Q10, Q11), §21.3 (Q09), Appendix G (Q12). §21.1's rewritten
instance criterion I exercised by re-counting rather than by asking about it
— see "rejected" below. Nine of the fifteen sit outside the changed set, on
the charter's instruction that the last five rounds all found defects in
untouched text.

## Independence — no two questions fail together

I checked the slate for shared failure modes and moved two questions because
of it:

- Q02 is now the **only** question requiring a working CRC-32C. An earlier
  draft asked for a trailer's CRC bytes as well; a wrong CRC table would
  have failed both, so the trailer question was replaced by Q01, which
  exercises trailer/directory *placement* arithmetic and needs no checksum.
- Q01 and an earlier "give the layer record's inline_length" question both
  turned on §7.4's field-width arithmetic. The inline_length question was
  dropped and Q11 (compaction of a slab-declared layer) took its slot.
- Q07 and Q08 both concern slack, but Q07 tests §9.7's identification of
  claimants while Q08 hands the claimant list over explicitly and tests only
  §5.2's discard rule. They fail for different reasons.
- Q13 and Q14 both end in a verifier verdict, but Q13's ground is a
  capability decline (§2.3) and Q14's is the presence or absence of an
  attached content rule (R-MTA-10). An implementation could get either right
  and the other wrong.

## Questions I built and rejected

- **"How many instances does row T22 name?"** and variants on §21.1's
  rewritten criterion. Rejected: every phrasing I could find reduces to
  reading one cell of one table, which is the lazy-question shape the
  charter names. I exercised the criterion by re-deriving all 273 instances
  mechanically instead, and report the result above as a null finding.
- **"How many conformance vectors does the corpus owe for §21.4 alone?"**
  (sum of the T rows' instances). Determinate and moderately hard, but a
  wrong answer changes a corpus manifest, not a byte on disk or an
  accept/reject verdict. Dropped for a question that forks bytes.
- **A foreign-major trailer with a bad `dir_offset`.** Determinate — §6.2's
  ordered validation puts the version gate ahead of the field gates, and
  §21.2's preamble says so explicitly — but its answer coincides with Q13's
  verifier verdict, so the two would have failed together for the same
  reading of §2.3. Cut in favour of Q13, which additionally exercises
  §7.4's sub-record outcome.
- **"May a commit change a channel's declared sample type to another type of
  the same element size?"** I could not convince myself an answerer and a key
  would reliably converge, and I concluded the document *does* decide it
  (see finding quiz-04) but only through a chain long enough that a
  divergence would indict my question rather than either reader. Reported as
  a finding instead of asked.
- **"Which §21.4 row does a commit that reorders two equal-width channels
  exhibit?"** Rejected because I believe the honest answer is *none*, which
  contradicts §21.7's claim — that is a finding (quiz-01), not a question.
- **A question about §5.2's partial total after a walk-established
  *file*-scope rejection (F33).** Rejected because I do not think the text
  determines it; reported as quiz-02.
- **"What must a verifier report about slack when §6.2's gates reject the
  file?"** Determinate (§5.2 says the total is not owed at all) but a single
  sentence answers it — one-cell lookup.

## Findings hit while authoring

Four, none of which I rate byte-level. Detail, quotations and the byte-level
reasoning are in the structured result under ids `quiz-01` … `quiz-04`.
Summarised:

- `quiz-01` — §21.7's claim that where a barred declaration change's affected
  tiles remain stored "the §21.4 rows then fire" has a counter-example:
  reordering two equal-element-size channels of an interleaved layer with no
  padding positions and no bool channel. Barred by §20.3, tiles remain
  stored, and no §21.4 row can fire.
- `quiz-02` — §5.2's rule for discarding already-enumerated claimants is
  written for a rejected *layer* only; a walk-established file-scope
  rejection (F33) leaves the partial total's value open between two
  defensible readings.
- `quiz-03` — §21.1's list of strict specializations omits T14 ⊂ T3 (under
  codec 1 a length that differs from the decoded size necessarily yields a
  decoded payload of the wrong length).
- `quiz-04` — §20.3 step 4's phrase "or how they decode" does not visibly
  reach §12's sample type, so a same-element-size channel-type change is
  permitted; the chain that establishes this runs §20.3 → §14 → §3.2 →
  §12.3 and is expensive to walk.

Null results worth recording, since a round that finds nothing and a round
whose reader expected nothing look alike: §21's row counts and instance
total are exactly right; §7.4's new worked example is byte-correct including
both CRCs; Appendix A is byte-correct; the structural-entry transparency rule
is consistent across all five places it is stated; §21.2's F33 exclusion list
(F9/F10, F31/F32, L16/L17, T8/T9) is complete over the claimant kinds §9.7
enumerates; Appendix G's closing paragraph does pin record and sub-record
order, so item 3 is not the reproducibility gap it first looked like.
