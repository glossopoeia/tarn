# Fidelity round 3 — findings

Protocol: ADR-0133, decision 4, the third real round after the two
calibrations ([0-calibration](../0-calibration/findings.md),
[1-calibration-2](../1-calibration-2/findings.md)), round 1
([2-round-1](../2-round-1/findings.md)) and round 2
([3-round-2](../3-round-2/findings.md)). Edition A is `main`'s
`spec/tarn.md` at `fe30c96` (ADR-0133's erratum of 2026-10-14: the
reference moves with `main`; the tag `edition-a` marks where B branched),
exported at `scratch/cleanroom/editions/a/tarn.md` and checked
byte-identical to `main`'s spec before launch (`7ca2f6f9…`); it carries
`[R-LIF-09]` (ADR-0134) and is 5,004 lines and 50,061 words. Edition B is
the `readable` branch's `spec/tarn.md` at `0c3ab26`, 115 commits into the
rewrite and 26 spec commits past round 2's `7b5b9a7`: the maintainer's
read-through of §9 through §17 (2026-10-13 to 2026-10-19) with the
driver's re-cuts, the ADR-0134 port and its erratum, "residue" stated as
the register states it, and the `[R-SER-04]` Note moved from §14.4 to
§2.2; 128 IDs in `reworded-ids.txt`, 163 IDs in each edition, 4,810
lines and 49,058 words. Unlike the spruce-up round 2 graded, this stretch
ADDED explanatory prose that says what A implies without A's words, the
class the round exists to grade. No seeds. Run `wf_401e3f0b-8d4`,
2026-10-20, every agent on `claude-sonnet-5` by the harness constant; the
launch turn was the single word "Go".

## Verdict

**No byte-level divergence. No ADDITION found by any lane survives the
hand-check as a decision B makes that A does not; one clause of
explanatory prose the read-through added says what A's text does not
support, found by the hand-check and by no lane, and goes to the
maintainer. The stretch this round was run to grade, §9 through §17 as
the read-through left it with its new Rationales, glosses and re-cut
Notes, drew nothing graded LOSS or byte-level from any instrument: the
two sweeps and the adversary closed every new block on A's own text, the
three comparators found every rule either walk cited deciding what A
decides, and every blind walk and quiz taker read the same rules from
both editions. Six groups were graded LOSS, unanimously by the three
passes, every one a cut of explanatory prose the edit log records in the
front matter and §1 through §4: five are grades rounds 1 and 2 gave and
the maintainer ruled kept cut (`[R-CNF-03]`'s experimental-range gloss,
§2.3's reach Note, §2.4's reject Note, §3.3's Note, §4.4's bit-numbering
Note), and one is new, the carve-out A's §2.3 states beside the
verifier's cannot-establish grounds, that an experimental-range metadata
encoding is not such a ground, which B's relocation of the grounds to
§21.6 did not carry and whose rule stands in B at §18.2 `[R-MTA-10]` in
the cut clause's own words and in three other places. Four of the six
were overturned by their refuters on the surviving statement; the
hand-check grades all six EQUIVALENT. Two groups were graded ADDITION,
both Rationales the read-through added on 2026-10-19: §15.4's,
unanimous, states A's own rule, Example and arithmetic and is EQUIVALENT
by hand; §16.2's, split 2–1 with its refuter standing on EQUIVALENT,
carries one clause A does not support, that a planner can size a buffer
and issue one direct read per run before it has fetched an index byte,
where A gives a run's offset and length only from its index entries.
Under decision 4 all eight go to the maintainer with both texts. Two of
the twelve two-edition lanes lost their returns at the validator on the
missing evidence object, one to a placeholder the degeneracy check set
aside and one to the retry cap; both were recovered from their
transcripts, neither carried a LOSS or ADDITION, and the hand-check stood
in for the triage they missed. The absence of a byte-level divergence is
measured by calibration 2, subject to its floor: a one-word inversion
inside a long reworded sentence reached triage there through two of six
lanes, and a change of that size that both lanes miss is not excluded
here; this round ran with one of those six lanes recovered rather than
triaged.**

| | |
|---|---|
| Edition B | `readable` at `0c3ab26`: §1–§8 rewritten, §9–§17 read through with new explanatory prose, §18 onward spruced up; 128 listed IDs; 4,810 lines against A's 5,004 on `main` |
| Byte-level LOSS surviving the hand-check | **0** |
| ADDITION | **1 clause, by hand**: §16.2's new Rationale says a planner can issue a run's read before fetching an index byte, which A's §16 does not give; non-normative, byte-neutral, the maintainer's. The two ADDITION grades are otherwise EQUIVALENT by hand |
| LOSS graded by triage | **6 groups**, unanimous, every one a logged cut of explanatory prose in the front matter and §1–§4; five ruled kept cut on 2026-10-08 and 2026-10-13, one new; EQUIVALENT by hand; four of six overturned on refute; to the maintainer with both texts |
| Findings in §5 through Appendix H | **0** graded LOSS by any lane; the two ADDITION grades, on §15.4's and §16.2's Rationales |
| Quiz | 30 questions; 14 loose divergences, 8 on slate A and 6 on slate B; both quiz comparators ran and graded all 14 EQUIVALENT, as does the hand-check; 0 reached triage |
| Blind walks | 10 own-edition findings, every one shared text of A (ledger); no fidelity difference |
| Triage | 29 findings into 19, 17 and 20 groups; coverage CLEAN, 29 of 29 ids on each pass; byte-level 0, 0 and 0; LOSS 6, 6 and 6; ADDITION 2, 2 and 1 |
| Refute | 7 refuters on the unanimous groups: `LOSS_STANDS` on the reach Note, the reject Note and §15.4's ADDITION, `LOSS_REFUTED` on §3.3, §4.4, the metadata carve-out and `[R-CNF-03]`'s gloss; 1 equivalence-refuter on §16.2's split, `EQUIVALENCE_STANDS`; no refuter failed; no zero-attacker |
| Harness | 31 slots, 30 returned, 1 failed at the validator's retry cap, 1 returned a placeholder the degeneracy check set aside, both recovered; no refusal, no stall; every agent `claude-sonnet-5`; "Go" disclosed by all and acted on by none; 60.4 minutes, 826 tool calls, 5.23 M tokens |
| Word-diff preflight | 26 commits accounted word by word against their log entries; no transcription defect; three notes, one an unlogged punctuation hunk; [word-diff.md](word-diff.md) |
| Coverage | sonnet-grade |

## The LOSS grades, hand-checked

Six groups were graded LOSS, unanimously by the three triage passes.
Every one sits on a cut the edit log records, with the surviving location
named there; five are grades rounds 1 and 2 gave and the maintainer ruled
on, and one is new. None is byte-level by any pass's account. ADR-0133
decision 4 and the maintainer's standing instruction send every LOSS on an
approved cut to the maintainer with both texts quoted, so all six are
listed, the five ruled ones with their ruling and a pointer to the round
that quoted them in full.

1. **`[R-CNF-03]`'s experimental-range gloss** (`cmp-verifier-01` LOSS,
   `cmp-verifier-05` OBSERVATION; unanimous LOSS at triage, severity
   content; `LOSS_REFUTED` on refute, the refuter finding the derivation in §21.6's closing paragraph, which A's own clause cites and which is identical in both editions). A's conforming-reader item: *"carrying no top-level
   record of a type it does not implement with MUST_UNDERSTAND = 1 — in a
   conforming file such a type is necessarily from the experimental range,
   since a reserved-range type carrying MU = 1 is itself a violation — and
   none of whose values exceeds the minimum guarantees of §21's limits
   table (§21.9's `[R-ERR-04]` governs a refusal on that last ground;
   §21.6's closing paragraph names the other two)"*. B: *"carrying no
   top-level record of a type it does not implement with MUST_UNDERSTAND
   = 1 and none of whose values exceeds the minimum guarantees of §21's
   limits table (§21.9)"*. Round 1's item 1, ruled kept cut 2026-10-08;
   graded EQUIVALENT by every lane in round 2. Hand-check as round 1's:
   rows F35 and F36 and §21.6's two-structural-cases paragraph are
   byte-identical in both editions, and the comparator's own rationale
   says so, both verifier walks having reached the same two verdicts.
   **EQUIVALENT by hand; ruled.**

2. **§2.3's three-row reach Note** (`cmp-reader-02` LOSS, `swab-01` LOSS;
   unanimous LOSS, content; `LOSS_STANDS` on refute, no sentence of B carrying the three rows' reasoning). A's Note works F14, F5 and F15
   through `[R-CNF-13]`'s test; B ends §2.3 at the ID with *"§21.2 lists
   the rows that reach"*. Round 1's item 6 and round 2's item 2, ruled
   kept cut 2026-10-08. Hand-check: §21.2's lead-in, byte-identical in
   both editions, says *"Deriving it there yields F8, F14, F6 and both of
   F1's instances … and no other row"*. **EQUIVALENT by hand; ruled.**

3. **§2.4's reject Note** (`swab-02` LOSS; unanimous LOSS, clarity;
   `LOSS_STANDS` on refute). A: *"**Note.** "Reject" prescribes the scope of unusability,
   not user interface: how failure is reported is implementation
   technique."* Absent from B. Round 1's item 5 and round 2's item 3,
   ruled kept cut. Hand-check: §2.1's Note, byte-identical in both
   editions, constrains *"bytes and observable behavior, never
   implementation technique"*. **EQUIVALENT by hand; ruled.**

4. **§3.3's Note** (`swab-03` LOSS, `adv-01` LOSS; unanimous LOSS, content;
   `LOSS_REFUTED` on refute, on §20.1's identical text; the refuter's `new_findings` names §1's roadmap sentence, round 1's item 3, ruled with it). A's one-Note subsection on Part I's independence from Part
   II, *"load-bearing for the updater rules of §7 and §20"*; B has no
   §3.3. Round 1's item 3 and round 2's item 4, ruled kept cut. Hand-check:
   the permission the claim explains stands at §2.3's updater definition
   (*"without necessarily understanding all of its content"*) and at §20.1
   and §20.4, byte-identical in both editions; the adversary carried it to
   a construction and found none whose verdict or bytes differ.
   **EQUIVALENT by hand; ruled.**

5. **§4.4's bit-numbering Note** (`swab-04` LOSS; unanimous LOSS, clarity;
   `LOSS_REFUTED` on refute, on §14.3). A: *"**Note.** This rule fixes bit numbering in flags and
   packed fields generally; the mapping of boolean *samples* to bits is
   defined in §14."* B's §4.4 ends at `[R-ENC-08]`. Round 2's item 6,
   ruled kept cut 2026-10-13. Hand-check: §14.3, identical in both
   editions, states the mapping with its own pointer back to §4.4.
   **EQUIVALENT by hand; ruled.**

6. **The experimental-encoding carve-out in `[R-CNF-11]`'s grounds**
   (`swab-05` LOSS; unanimous LOSS, content; `LOSS_REFUTED` on refute, the refuter searching B for the rule's substance rather than A's phrase and finding it). **New to the
   maintainer.** A's verifier item, after the five cannot-establish
   grounds: *"A user-metadata document under an experimental-range
   encoding — one this specification does not assign and a conforming
   file can carry (§21.6) — is not such a ground: no content rule
   attaches there, so nothing is left unchecked, and certification is
   unaffected (`[R-MTA-10]`); encoding 0 and a reserved value are
   violations (§21.5, R1)."* B moved the grounds to §21.6's closing
   paragraph (the entry of 2026-09-24, "§2.3 verifier and updater items;
   the cannot-establish grounds moved to §21.6") and that paragraph does
   not carry the carve-out. The entry records the cut as a restatement
   removal with `[R-MTA-10]` as the surviving statement and ADR-0066
   (`45f9367`) as the restatement's origin. Hand-check: B's §18.2
   `[R-MTA-10]` paragraph says *"A verifier meeting such a record in an
   otherwise conforming file has no requirement it is unable to check: the
   record is not among `[R-CNF-11]`'s cannot-establish grounds, and at an
   experimental-range encoding certification is unaffected, encoding 0 and
   a reserved value being R1's violations"*, A's words but for a dash made
   a colon; B's §17.4 closes `[R-COD-11]`'s paragraph, byte-identical in
   both editions, with *"an experimental-range document encoding in a
   conforming file is not a violation (§21.6), no document rule attaches
   to its extent, and certification is unaffected (`[R-MTA-10]`, §18.2)"*;
   §21.5's lead-in (*"except at an experimental-range encoding, where no
   document rule attaches"*), §9.7 (*"asks nothing of this walk: no rule
   attaches to its content (`[R-MTA-10]`)"*) and Appendix H's verifier
   checklist state it again, each in both editions. A restatement removal
   whose rule stands in four places, the governing one with the cut
   clause's own words. **EQUIVALENT by hand; to the maintainer with both
   texts, expecting "keep cut".**

## The ADDITION grades, hand-checked

Two groups were graded ADDITION, both on Rationales the read-through added
on 2026-10-19 at the maintainer's ask, and both hand-checked here sentence
by sentence against A's text and the log entry that records the
derivation. Decision 3 lets B say what A implies only where the
derivation is A's own text; the round grades anything else as an addition
for the maintainer.

1. **§15.4's Rationale for segments** (`swab-06` ADDITION; `swba-01`
   EQUIVALENT; the adversary's rejected candidate 3, EQUIVALENT; unanimous
   ADDITION at triage, severity content for the correctness pass and none
   for the other two; the refuter `LOSS_STANDS`, its enum being the gate-failing one: the 19 and 190 MiB figures found nowhere in A, their inputs (the 20-byte entry, the 1.25 MiB segment) found in both editions). A has no such block. B, after the "To use"
   Note:

   > **Rationale.** Segments bound what a reader verifies to use one
   > entry. Under a single CRC over the whole entry array,
   > verify-before-use (§8.2) would oblige a remote reader to fetch the
   > entire index to use any entry: about 19 MiB at a million tiles and
   > 190 MiB at ten million. With one CRC per 2¹⁶ entries and a CRC over
   > the CRC array, a reader fetches the array and the one segment holding
   > its entry, never more than 1.25 MiB plus the array at any layer scale,
   > and both ranges follow from the layer record alone. Segments are not
   > an option a writer takes or declines: every tile index under
   > index_encoding 1 is laid out this way, and a writer's whole duty is
   > one CRC per segment, full or partial, and the CRC over the array. A
   > layer of at most 65,536 entries has a single segment and a single
   > CRC, so its writer and the naive whole-index reader see nothing they
   > would not see under one CRC; the segmentation shows only when an
   > index outgrows that.

   Hand-check, each sentence against A (identical in B): *"To use entry
   k, a reader MUST verify … crc_of_crc_array over the fetched CRC array
   and the segment CRC over the fetched segment containing k (both ranges
   are computable from the layer record alone …)"* (`[R-IDX-04]`), which
   is the first sentence and the "both ranges" clause; §8.2's
   verify-before-use, the hypothetical's premise; the two MiB figures are
   entry_count × 20 bytes, the entry size §15.1 fixes and A's own Example
   uses (*"index region 20,000,064 bytes"* at a million entries); *"never
   more than one full segment (1.25 MiB) plus the CRC array, at any layer
   scale"* and *"A layer with 1 ≤ entry_count ≤ 65,536 has one segment
   and a 4-byte array: fetching the whole region and verifying one CRC is
   the naive reader, unchanged"* (A's Example, verbatim in B); the
   writer's duty, `[R-IDX-04]` and `[R-IDX-05]` (a partial segment's CRC
   MUST be computed). The two sweeps that read both editions and the
   adversary each closed it on those facts. **EQUIVALENT by hand: every
   figure and every claim is A's own text or its arithmetic; to the
   maintainer as the round's first ADDITION grade on his read-through,
   with the text above.**

2. **§16.2's slab Rationale** (`swab-07` OBSERVATION; `swba-02`
   EQUIVALENT; the adversary's rejected candidate 3, EQUIVALENT; split at
   triage, ADDITION for the correctness and implementer passes and
   EQUIVALENT for the skeptic; `EQUIVALENCE_STANDS` on refute, on `[R-CNF-01]`'s identical definition of what is non-normative; the refuter tested the relabelling and not the clause below against §16's rules). A's third labelled block of §16.2:

   > **Note — what slabs are, and are not.** A slab guarantees
   > *contiguity*: consecutive disk ordinals occupy consecutive bytes.
   > Which tiles are ordinal-consecutive is the linearization field's job
   > (§11.4); under row-major, a run is a band along the last-declared
   > dimension. Rectangular-window locality is therefore not a slab
   > property — it belongs to the reserved space-filling-curve
   > linearization values, under which the same slab machinery, unchanged,
   > would make compact windows contiguous. Slabs are the byte-layout half
   > of that future answer. With A_slab = 1 a slab is contiguity-only — the
   > right declaration for remote range coalescing with no direct-I/O
   > alignment need.

   B, the same block relabelled and rewritten (the entry of 2026-10-19,
   "§16.2: the slab-scope Note made a Rationale with its motivations"):

   > **Rationale.** A slab promises one thing, contiguity: within a run,
   > consecutive disk ordinals occupy consecutive bytes. A reader that
   > wants a run can therefore fetch it as one range, however many tiles
   > it holds and whatever their stored sizes, and a planner can size a
   > buffer and issue one direct read per run before it has fetched a
   > single index byte. A reader holding the index entries can always
   > detect contiguity by arithmetic; what the declaration adds is the
   > promise in advance, checkable by a verifier, with the index left as
   > it is, one entry per tile. Which tiles are consecutive in ordinal is
   > not the slab's business but the linearization field's (§11.4): under
   > row-major, a run is a band along the last-declared dimension. So a
   > slab does not by itself make a rectangular window contiguous; that
   > locality belongs to the reserved space-filling-curve linearization
   > values, under which the same slab machinery, unchanged, would make
   > compact windows contiguous. Slabs are the byte-layout half of that
   > future answer. A_slab adds alignment for direct I/O at each run's
   > start; with A_slab = 1 a slab is contiguity alone, the right
   > declaration for coalescing remote range requests when no direct-I/O
   > alignment is needed.

   Hand-check against A's §16 (identical in B): the five facts of A's
   Note stand in order; *"within a run"* is `[R-SLB-03]`'s own scope
   (*"for every run: the run's stored tiles are contiguous and packed in
   ordinal order"*, with placement freedom between runs); the one-range
   fetch *"whatever their stored sizes"* is the section's Example (*"two
   range requests regardless of stored-tile sizes"*); arithmetic detection
   and the verifier's check are `[R-SLB-03]`'s last sentence (*"A verifier
   MUST check these invariants …; readers are not obligated to, and MAY
   instead detect contiguity arithmetically from any index segment"*);
   one entry per tile is §15.1; alignment for direct I/O at a run's start
   is `[R-SLB-03]`'s *"the first stored tile's offset satisfies offset
   mod A_slab = 0"* read with §16.1's Note on what alignment serves and
   A's own closing clause. **One clause is not A's: *"and a planner can
   size a buffer and issue one direct read per run before it has fetched
   a single index byte"*.** A run's byte range is known only from its
   index entries: `[R-SLB-01]` says *"offsets are always explicit"*,
   `[R-SLB-03]` that the invariant *"stays decidable from the index
   entries alone"*, and nothing in §16 or §15 gives a run's start or
   length from the layer record. What the declaration tells a planner in
   advance is that each run is one range to read, not where it lies or how
   long it is; sizing a buffer and issuing the read wait on the run's
   entries. The log entry derives the clause from ADR-0022's context
   ("the promise known in advance"), which is not A's text. The A-into-B
   sweep named the clause as new material (*"buffer sizing before touching
   the index"*) and the correctness pass asked the maintainer to confirm
   the added sentences; no lane tested it against §16's rules. It is a
   Rationale, so no byte or verdict turns on it; an implementer who
   believed it would find the index necessary before the first read.
   **ADDITION by hand, in one clause: to the maintainer. The rest of the
   block is EQUIVALENT by hand. If the clause is to be kept it wants A's
   support stated, for instance that a planner knows from the layer record,
   before it fetches an index byte, that each run is one range; the fix is
   the maintainer's to word, after this round.**

## The read-through's new prose, hand-checked against the log

The handoff listed nine pieces of prose the read-through added or
reframed without A's words and asked that each be hand-checked against the
log entry that records its derivation, whatever the lanes said. The two
Rationales above are items 4 and 5 of that list. The rest:

- **§9.7's gloss of a claimant** (`66b0f01`): *"the claimants: the
  structures `[R-CNT-02]` partitions the live committed state into, each
  claiming the bytes that belong to it, the rest being slack (§5.2)"*.
  Derived from `[R-CNT-02]` (*"Every byte of the live committed state
  belongs to exactly one of: the front signature block; or a structure
  …"*) and §5.2's *"Every byte the live state does not claim is slack"*,
  both A's and identical in B. No lane reported it; the writer comparator's
  full paragraph diff read the replace block and found no keyword or
  numeral change. EQUIVALENT by hand.
- **§13.2's *"Readers need not screen value bytes for it (§14.2,
  `[R-SER-08]`)"*** (`58dd3bb`): from `[R-SER-08]`'s *"A reader is not
  obligated to screen decoded content"*, A's, identical in B. No lane
  reported it. EQUIVALENT by hand.
- **§14.4's epigram written out** (`586e412`): A's *"a format that makes
  the honest type inexpressible gets the dishonest one"* reads in B
  *"Barred from interleaved layers, a bool channel would be declared int8
  instead, the same bytes with the type label erased, and every consumer
  would inherit an untyped 0/1 conversion"*. The dishonest type is int8
  (§12.1's table), the same bytes are §14.2's one byte per bool value,
  both A's; the sentence names what A's epigram alludes to and decides
  nothing. No lane reported it. EQUIVALENT by hand.
- **§11.1's growth Rationale re-cut** (`dc66fc9`): the §20.3 step 4
  summary item by item, the two stated-once sentences kept, A's six
  lowercase keywords rewritten around; the word-diff preflight noted the
  new topic sentence *"Growth is cheap where it changes no grid count"*,
  which summarises the sentence after it (such a growth touches the
  directory alone), and *"stored a tile"* for A's *"stored tiles"*, the
  quantifier §20.3 step 4 uses. No lane reported the block. EQUIVALENT
  by hand.
- **§9.2's second Note** (`1df7b0d`): the 128-byte floor's derivation now
  framed as *"forced on a writer that performs the steps before it"*, with
  the premise placed in step 3's *"append the new complete directory"*
  rather than in the first Note. It asserts less than A's framing, not
  more, and every figure and citation is kept. No lane reported it.
  EQUIVALENT by hand.
- **§9.3's first Note** (`44f113d`): now cites `[R-LIF-02]`, `[R-LIF-01]`,
  `[R-LIF-02]`'s steps 1, 3 and 5 and `[R-CNT-06]` as what yields the
  strict increase, the premises A's §9.2 second Note derives from. No lane
  reported it. EQUIVALENT by hand.
- **§2.2's retired-identifier Note** (`770ffcb`): moved from §14.4;
  `swba-03` EQUIVALENT, the skeptic pass likewise; §2.2's rule two
  paragraphs above says *"permanently retired"* in both editions, which
  the moved Note no longer repeats. EQUIVALENT by hand.
- **"Residue" stated as the register states it** (`64b6e5e`, `8b1eefe`):
  §7.2's and §7.4's *"bytes remaining after the last complete record"*
  (rows F29 and L14's words) and §9.5's Note's *"extra bytes … beyond the
  committed file length"*. No lane reported them; the keyword clauses are
  verbatim. EQUIVALENT by hand.

## Shared indeterminacies of A, for the ledger

The six blind walks reported ten findings about their own editions and
quiz author B one. Every one quotes text that stands identically in both
editions, checked here by whitespace-normalised search and by the
comparators, and every pass graded each EQUIVALENT or REPORTER_ERROR with
the location in both editions named. They are observations about A, not
fidelity findings.

- **No outcome class for a reader lacking an assigned core codec**
  (`readera-01` AMBIGUITY; `verifierb-01` OBSERVATION; §2.3 `[R-CNF-03]`,
  §17.4 `[R-COD-11]`). The finding every calibration and round has
  returned. This time the reader comparator and two passes graded it
  REPORTER_ERROR: §17.4's second sentence, byte-identical in both
  editions, confines the cannot-establish position to a reserved or
  experimental value and says software unable to execute an assigned codec
  is not a conforming reader; what the walker asked, what such software
  does, is a question about non-conforming software.
- **A fixed-declaration change on a stored-tile layer is unwitnessed**
  (`verifiera-02`, `verifierb-02`, `writerb-01`; §20.3 step 4, §21.7, row
  T4). Rounds 1 and 2's T4 group again, identical text; `verifierb-02`
  takes a bare name change for a barred change where §20.3 step 4 lists
  names among the permitted ones (*"a commit MAY change several names at
  once, two swapped included"*), a walker's reading of shared text.
- **`[R-CNT-12]`'s MU = 1 / PE = 0 coercion against §20.4's governing
  flags** (`writerb-02` CONTRADICTION; §7.2's Note, §20.4). Round 1's
  ledger item; the writer comparator and the implementer pass grade it a
  reporter error, §20.4's *"so for an implemented type only the PE bit
  bites"* deciding the case in both editions.
- **A creator that decodes and re-emits writes flags = 0** (`writera-02`;
  §20.1). Round 2's item; identical text.
- **An append's exact offsets are writer-chosen** (`writera-01`;
  `[R-SLB-05]`, §20.3). New; identical text; the placement freedom A
  states on purpose.
- **§2.4's unqualified "reader outcome" against §21.1's verifier-row
  carve-out** (`verifiera-01` AMBIGUITY; `[R-CNF-07]`, §21.1). New; both
  sentences byte-identical in both editions; the verifier comparator calls
  it a real reading trap that does not distinguish the editions.
- **The trailer's incompat lane has no extension vehicle** (`readera-02`
  OBSERVATION; §10.1, `[R-EXT-01]`, F19). New; identical text; a design
  observation, F19 deciding every current case.
- **§6.2's post-gate trailer checks have no stated order among
  themselves** (`quizb-01` AMBIGUITY; `[R-CNT-06]`). New; A and B both
  order the three gates and then say *"MUST validate all of the
  following"*; every member yields reject-file.

## The instruments, one by one

- **The word-diff preflight** ([word-diff.md](word-diff.md)): for each of
  the twenty-six commits from `58d3201` to `0c3ab26`, the diff's removed
  and added lines tokenised as `propose.py` does and the Counter
  difference read against the commit's edit-log entry, since this stretch
  changed words on purpose. Every lost and gained word is accounted for by
  the entry's "Edits" paragraph, its word-level diff line or its quoted
  before and after texts; no transcription defect; nothing restored. Three
  notes: `fd87472` carries a third hunk its entry does not record,
  punctuation only, in §13.3's `[R-TYP-08]` paragraph (*"MUST return, for
  each channel the tile carries, that channel's fill"* → *"MUST return
  (for each channel the tile carries) that channel's fill"*; the ID listed
  since the §13 spruce-up with a reason line that still reads "the MUST
  verbatim"); the entry for `770ffcb` says "the same words but for 'per
  §2.2'" where its own quoted after-text also drops "permanently"; and
  `dc66fc9`'s two unnamed wordings, above. The pooled and one-diff lists
  agree word for word.
- **`tarn_inventory.py`** was not part of the run; it passed before the
  launch with the 128 listed IDs and the carried soft items (the eight
  §3.1 term rewordings, Appendix B's row, HEADINGS 130 against 129, SHOULD
  46 against 47); `tarn_check` PASS with 10 warnings.
- **The quiz, cross-answered**: 30 questions, author A with no findings,
  author B with the §6.2 observation above. The loose match found eight
  divergences on slate A and six on slate B, so both quiz comparators ran;
  all fourteen are EQUIVALENT by the comparators and by hand, every one a
  phrasing (*"00 00 F0"* against *"0x00, 0x00, 0xF0"*; *"Nonconforming"*
  against *"No"*; *"F1, F6, F8, F14; total instances = 5"* against the
  same with *"5"*), save one where the taker on A named the rewrite alone
  and the taker on B both the new layer and the rewrite for §20.3 step
  4's alternative, both quoting the same sentence, identical in both
  editions, and the question asking for one phrase. Nothing reached
  triage from the quiz.
- **The six blind walks**: 10 to 19 minutes each, every probe answered the
  same from both editions on substance; ten own-edition findings, all
  shared text (above). No walk found a fidelity difference, as in every
  earlier run. Walker B of the writer role read §1 through §21.7 and not
  §22 onward, which the writer comparator confirmed identical in both
  editions.
- **The three comparators**: reader 3 findings (1 LOSS, 1
  REPORTER_ERROR, 1 EQUIVALENT), verifier 6 (1 LOSS, 3 EQUIVALENT, 2
  OBSERVATION), writer 6 **recovered from its transcript** (1
  REPORTER_ERROR, 3 OBSERVATION, 2 EQUIVALENT; below): the writer
  comparator's full paragraph diff of Part I through Appendix H aligned
  228 blocks, found no insert or delete, read all 114 replace blocks and
  found one keyword change (the SHOULD the log records written out in
  §6.3) and no numeral change. The two LOSS grades are items 1 and 2
  above.
- **The two sweeps**: A into B, 8 findings (5 LOSS, 1 ADDITION, 1
  OBSERVATION, 1 EQUIVALENT), with a labelled-block census by fingerprint
  (94 in A against 90 in B: 89 paired, one new block in B, four A blocks
  gone and one reworded outside its blockquote, closing exactly) and a
  per-subsection diff of every matched pair; B into A **recovered from its
  transcript** (below), 9 findings (7 EQUIVALENT, 2 OBSERVATION, no
  ADDITION) over two order-preserving alignments of every labelled block
  and every paragraph under the ~90 shared headings: *"I found no case
  where A states a B-decided rule, carve-out, exception, quantifier, or
  worked figure more narrowly, more widely, only inside a non-normative
  block where B is normative, or not at all in any form"*.
- **The diff-adversary**: 1 finding (item 4 above); a requirement-ID sweep
  (163 against 163, fifteen IDs with differing citation counts each traced
  to a relocation), a heading-aligned diff of all 129 matched headings
  with the fifteen largest deltas read in full, and five candidates
  opened and closed, among them the §2.3 conduct-rule cases at their home
  sections, §21.6's relocated grounds, and the §15.4 and §16.2 Rationales
  as derivations of A's own unchanged text; no file, commit or verdict on
  which the editions disagree.
- **Triage**: 29 findings (three comparators 9, the A-into-B sweep 8,
  the adversary 1, six walks 10, one author 1; the writer comparator's and
  the B-into-A sweep's returns were lost at the validator and reached no
  pass) into 19, 17 and 20 groups; coverage CLEAN, 29 of 29 ids on each
  pass; byte-level 0, 0 and 0. Unanimous LOSS on the six groups above;
  unanimous ADDITION on §15.4's Rationale; §16.2's block split 2–1, the
  skeptic on EQUIVALENT; every walk group EQUIVALENT or REPORTER_ERROR on
  identical text. The correctness and skeptic passes read the two editions
  only; the implementer also read the walk and comparator transcripts.
- **Refute**: seven refuters on the unanimous gate-failing groups (six LOSS,
  one ADDITION), 1 to 3 minutes each, every one in its own vocabulary with
  `decisive_quotes` filled and a control search behind every zero: the
  reach Note's and the reject Note's `LOSS_STANDS` (no sentence of B
  carries the Note); §3.3's `LOSS_REFUTED` on §20.1's identical text, its
  `new_findings` naming §1's roadmap sentence, round 1's item 3; §4.4's
  `LOSS_REFUTED` on §14.3; the metadata carve-out's `LOSS_REFUTED`, the
  refuter searching for the rule's substance rather than A's phrase, as
  the hand-check did; `[R-CNF-03]`'s gloss `LOSS_REFUTED` on §21.6's
  closing paragraph, which A's own clause cites; §15.4's `LOSS_STANDS`,
  the figures found nowhere in A and their inputs found in both editions.
  One equivalence-refuter on §16.2's split, `EQUIVALENCE_STANDS` on
  `[R-CNF-01]`'s identical definition of non-normative text; it tested
  the relabelling and did not test the planner clause against §16's rules,
  which is the hand-check's finding above. No refuter failed; no
  zero-attacker, the round not being a zero in the harness's terms. Every
  refuter read the two editions only.

## Harness integrity

- 31 agent slots (two authors, four takers, six walks, three comparators,
  two sweeps, the adversary, two quiz comparators, three passes, eight
  refuters), 30 returned, 1 failed, no refusal, no stall, every agent at
  its first attempt; one return degenerate (below). Authors 6–7 minutes,
  takers 5–6, walks 10–19, comparators 7–11 (the adversary 12, the sweeps
  15 and 18), quiz comparators 3–4, passes 7–10, refuters 1–3; 60.4
  minutes end to end, 1,517 assistant messages, 826 tool calls, 5.23 M
  tokens.
- `rebuild.py` substituted 29 of 30 journal results, the one unused being
  the placeholder the harness set aside; the two ellipsis characters left
  in the output are quoted text. `collect-fidelity.py --full` printed the
  matrix, the findings by kind, the three passes' groups and the eight
  verdicts. `copy-fidelity.sh` copied 24 files, every triage transcript
  from its own directory.
- **Two returns lost at the validator, both on the missing `evidence`
  object.** `compare:writer` made four structured returns: the second and
  third carried its summary and six findings without the `evidence`
  object and were rejected; the fourth, a placeholder ("test" in every
  prose field, one letter in each evidence field, no findings), was
  accepted. The degeneracy check round 1 mandated caught it ("DEGENERATE
  RETURN: compare-writer … recover the lane from its transcript"), the
  run went on, and the harness's result sets the lane aside in
  `degenerateLanes`. `sweep:b-to-a` made five: the first two carried its
  summary and nine findings without `evidence`, the third was unparseable
  JSON of 13.7 KB, the fourth and fifth a disclosure field alone, and the
  runtime failed the agent at the retry cap, `rebuild.py` and the journal
  recording it as failed. Both lanes had done their work (41 and 56 tool
  calls, transcripts written) and both are recovered from the last full
  attempt in their transcripts, as ADR-0034 directs for a started agent
  whose return is unusable: [fidelity-compare-writer-recovered.json](fidelity-compare-writer-recovered.json)
  and [fidelity-sweep-b-to-a-recovered.json](fidelity-sweep-b-to-a-recovered.json).
  The brief's validator rule (keep the content, add the missing field;
  never send placeholders) held neither agent. Triage saw neither lane's
  findings; the hand-check carried them, and neither carried a LOSS or
  ADDITION.
- **The model.** Every agent's meta file says `claude-sonnet-5` and all
  1,517 assistant messages across the 31 transcripts carry
  `claude-sonnet-5`. The pin is the harness constant, `SUBAGENT_MODEL =
  'claude-sonnet-5'` (line 47), with preflight under `--models
  claude-sonnet-5`; the pre-launch probe `wf_229b11ed-c51` (one agent,
  `model: 'claude-sonnet-5'`, no tools) ran on it in 2.4 seconds.
- **The launch turn.** The Workflow runtime prepended the launching user
  turn to every agent's prompt as "the only user voice in this task";
  this round's was the single word "Go", and the first transcript's user
  turn reads exactly "Go" after the harness's label. All 31 returns, the
  two recovered included, disclosed it; 30 said in so many words that
  they set it aside; none acted on it, the boundary scan showing no git
  command and no read outside any agent's rule.
- **The mechanical boundary scan** (`pass/boundary-scan.py` over every
  transcript's tool calls): the six blind-A agents named
  `editions/a/tarn.md` and never the repository's `spec/tarn.md`, the six
  blind-B agents the reverse; no agent named `editions/b`, `editions/c`
  or the stale sibling repository; no agent ran a git command. Directory
  listings were of the agent's own scratch directory, a stat of its one
  permitted file (`walk:reader-a`, `quiz:b-on-b`), and `quiz:b-on-b`'s
  `ls -la out/ | head -5` (two filenames, the authors' transcripts, which
  it disclosed as a breach and did not open). The adversary and
  `walk:reader-a` read the runtime's tool-result spill files (its own
  mechanism for a long result). **One undisclosed write to `/tmp`**:
  `sweep:a-to-b` wrote `/tmp/x`, a sed extract of A's labelled-block
  headers, the class round 2 noted twice; the ACCESS rule's
  scratch-directory clause still does not name `/tmp`.
- **Other disclosures.** Every return disclosed the injected context (the
  project pointer file, the memory index, the git-status block, the
  environment); 17 named the git-status block's commit subjects, the
  channel the maintainer accepted for this round, used as disclosure
  only, save that the recovered B-into-A sweep cited the §16.2 commit
  subject as corroboration of the relabelling it had found by diff and
  said so. Walker B of the writer role disclosed reading §1 through §21.7
  and not §22 onward; the writer comparator confirmed the unread region
  identical in both editions.
- **Preflight** on `/usr/local/bin/node` v22.19.0: selftest PASS; PASS
  with the run's args under `--models claude-sonnet-5`, 22 calls
  rendered, 11 model sites on `claude-sonnet-5`; `render-prompts.js` 24
  briefs; the path audit PASS (six A-agents `editions/a/tarn.md` only,
  six B-agents `tarn-first-draft/spec/tarn.md` only, twelve two-edition
  briefs both, no `editions/b`, no `editions/c`, all 24 naming
  `fidelity-5`, all 24 carrying the validator rule and the relayed-request
  paragraph); the export checked byte-identical to `main`'s spec
  (`7ca2f6f9…`); `fidelity-5` empty; `git status` empty at `0c3ab26`.

## What this round mandates

1. **The `evidence` object is the harness's tripwire.** Round 1 lost one
   two-edition return to it and this round lost two of twelve, one to a
   placeholder and one to the retry cap, and the validator rule round 1
   added to every brief saved neither. The schema should stop asking for a
   nested object: the four fields `sweeps_run`, `derived_numbers`,
   `rejected_candidates` and `confidence_empty` at the top level, or
   `evidence` optional with the four accepted at either level, and the
   brief showing the return's skeleton once. A harness change, on the
   maintainer's word, before round 4; `rebuild.py` and `collect-fidelity.py`
   follow it.
2. **Round 2's two small debts are still unpaid**: probe R4's field names
   (*offset*, *length*), and the ACCESS rule naming `/tmp` as the shared
   directory it means, a third agent having written there this round.
3. **For B, not the harness, after this round and on the maintainer's
   word**: §16.2's planner clause, kept with A's support stated or cut;
   and the entry for `fd87472` and `R-TYP-08`'s reason line recording the
   punctuation change the word-diff preflight found.
4. **The grade a round gives a logged Note cut is now measured four
   times**: this round's six LOSS groups are the class again, five of them
   grades already ruled on, and the refuters overturned four of the six on
   the surviving statement. Expect it over the front matter and §1–§4
   until the read-through settles that stretch.

## What this round says about B

For ADR-0133 decision 5's test, no LOSS survives the hand-check. One
ADDITION does, by the hand-check and not by any lane: a clause of §16.2's
new Rationale that states a reader capability A's text does not give,
non-normative and byte-neutral, the maintainer's to reword or cut. The
read-through's stretch, twenty-six commits over §9 through §17 that added
explanatory prose on purpose, drew nothing graded LOSS or byte-level from
any instrument, the two sweeps and the adversary closing every new block
on A's own text and the writer comparator's full paragraph diff finding no
keyword or numeral changed anywhere from Part I to Appendix H. The six
graded losses are the front matter's and §1 through §4's, where the
rewrite has cut the most explanatory prose and where the read-through has
not yet passed; five were ruled before this round and one is new, with
its rule standing in four places. On every rule the instruments read, B
at `0c3ab26` says what A says.
