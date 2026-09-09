# 0128. Round 35's repairs: a compactor's checksum duty reaches every extent it copies, and seventeen wording repairs

- Status: Accepted (resolves round 35's repairable findings; decision 1
  confirmed by the maintainer on 2026-09-09)
- Date: 2026-09-09
- Covers: §20.5 `[R-WRT-09]` and `[R-WRT-07]`'s restatement of it; §20.3
  step 4's principle parenthetical, its re-emission clause and its
  fixed-declarations characterisation; §4.7 `[R-ENC-16]` and its Note; §6.1;
  §6.4 `[R-CNT-09]`; §19.1 step 1; §10.2 `[R-EXT-02]` and its table; §10.3
  `[R-EXT-03]`; §19.3 `[R-RDR-03]`; §21.1's quarantine clause, its
  parenthetical convention, its §21.6 clause and its `[R-SER-08]` sentence;
  §21.6's zero-layers entry; §22.3
  `[R-SEC-03]`; Appendix G items 3 and 5 and its closing paragraph
- Confirm: none. Decision 1 was put to the maintainer and confirmed on
  2026-09-09, with its alternative stated below so a superseding ADR can
  choose it: that a compactor's verification duty reaches the checksum §8.1
  states over every extent it copies, whether or not its output relocates
  the extent, so that a compactor meeting a failed CRC on an extent it
  would carry forward unmoved MUST refuse as §20.5 already obliges it to
  on any failed check. ADR-0129 has since restated the actor as a rewriter.

## Context

Round 35 read ADR-0127's seventeen repairs, their confirmation, the audit
of them and its erratum, sixteen passages over two commits, with every lane
on the model the brief names. It returned 25 findings from 6 reporters, 22
distinct defects, a 15/15 quiz, and no self-flagged byte-level finding. All
three passes upheld one group byte-level against both of its reporters' own
grading; the uphold-refuter, on Sonnet after Opus refused it twice at zero
tokens, returned UPHOLD_STANDS with an account of its search, and the
hand-check agrees. The 24 hunks the round was chartered to read returned
zero byte-level ambiguities, so G3's second half held across this cycle; the
fork is in §20.5, which no recent cycle touched.

**The flag.** `[R-WRT-09]` states a principle and a list: *"it relies
structurally on every structure it copies, so it MUST verify each link of the
chain — the open (§19.1), each retained layer's record (§19.3) and full index
chain (`[R-IDX-04]`), and each relocated extent's checksum, including every
stored tile's entry crc — before emitting that structure's bytes"*. The
premise ranges over everything copied; the list's third item ranges over
relocated extents. §20.5 makes the difference live: a compactor *"preserves
no placement"*, is *"free to place structures anywhere §5.2 admits"*, and its
figure commentary says *"In this placement A's stored extents happen not to
move"*. Two reporters built the input: a top-level user-metadata extent
whose terminal CRC fails (R2), a PE = 1 record no table licenses dropping, one
stored tile and its index, no interior slack, and a compactor keeping every
structure at its input offset. Under the list it never reads the extent's
CRC, detects nothing, and emits the output under a fresh file_id; under the
premise it verifies, fails, and *"A compactor MUST refuse to compact when any
check `[R-WRT-09]` obliges fails"*. Both reporters graded it below byte-level
on `[R-CNF-05]`'s ground, that the output is nonconforming under both
readings; all three passes upgraded it on `[R-WRT-01]`, *"a violation latent
in a structure they carry forward unmodified travels with it, seen or
unseen"*, and on §20.5's *"Given a conforming input the output is a
conforming file"*, a conditional with no work to do unless a nonconforming
input may yield a nonconforming output. The output is a file a conforming
compactor may emit under one reading and none may under the other. The
hand-check found three formulations of one duty, in the premise, the list,
and `[R-WRT-07]`'s restatement, which drops the *relocated* qualifier for
tiles and is silent on every other extent, and no sentence choosing among
them. It is new: Q-C10 asks the neighbouring question, an index entry's
classification, and names `[R-WRT-09]` only as the depth bound.

**Why this is a repair here and not a ledger entry.** The rule states its
own principle, *"A compactor's verification depth follows reliance over
everything it carries"*, in contrast with `[R-WRT-03]`'s gated rule for an
appender; `[R-WRT-07]` already treats the tile half of the duty as
placement-free; and the cost of the wide reading is a CRC over bytes the
compactor reads in order to copy them. So the principle decides which way
the list should read, and what the list lacked was one word. ADR-0091's rule
is satisfied by this ADR, and the maintainer's veto is kept in the Confirm
line.

## Decision

**1. A compactor's checksum duty reaches every extent it copies.**
`[R-WRT-09]`'s list reads *"and the checksum §8.1 states over each extent it
copies, every stored tile's entry crc among them"*, and the rule adds *"The
duty follows what the compactor carries and not where it places it: an
extent the output leaves at its input offset owes the same check as one it
relocates."* `[R-WRT-07]`'s restatement says the checks *"reach the index
chain and the checksum over each extent it copies"*. §20.5's refusal on any
failed check then reaches a corrupt extent the output would carry unmoved.
Two reporters, three passes.

**The seventeen editorial repairs**, each confirmed by at least two passes
or, where two passes held the text already decided it, repaired for its
wording on ADR-0125's precedent:

2. The principle paragraph's second parenthetical named T24 and T25 alone,
   while T17 witnesses a codec re-declared to zstd before any decode is
   attempted; it names *"a decode that fails outright, or a codec's framing
   check that precedes it, under a changed codec or filter (T17, T24, T25)"*.
   Two reporters.
3. §6.1 said the local/remote distinction governs §6.4's request accounting
   *and nothing else*, while `[R-CNT-06]`'s gate and `[R-CNT-10]`'s size
   obligations turn on it; it names all three.
4. Appendix G item 3 said *a declared alignment* where its next clause says
   *a declared A or A_slab*, and constrained no structure that is not a
   stored tile; it says *"where that structure is a stored tile and a
   declared A or A_slab admits none at 16"*, and that a structure no
   declaration constrains begins at 16 like any other.
5. Appendix G item 5's reason for pinning the layout fails for a
   single-channel numeric layer, as §14.4's Note says; the item adds that
   the layer record's own layout byte still differs.
6. Step 4's *added tiles* named tiles that produce no new index entry; the
   parenthetical reads *"tiles a grown extent or an appended channel adds to
   the addressed set"*.
7. §22.3 said every reachable byte belongs to a named structure, where
   `[R-CNT-02]` puts the front block on the other side of its own *or*; it
   says *"is the front signature block or belongs to exactly one named
   structure"*.
8. *The fixed declarations are* characterised them by §14, §11.4 and §15 and
   omitted §17's codec and filter, which the operative list names; the
   fourth limb is added.
9. §21.1 said `[R-CNT-25]`'s quarantine assigns the outcome *for every §21.5
   row*, while its trigger is four ways a document can be unreadable and
   several of R4's instances leave it readable; it says *"for every way a
   §21.5 row makes the document unreadable"*.
10. §21.6's Rule column carried one cell in the register's parenthetical
    form among fourteen comma lists, and §21.1 extended governance to it in
    the singular; the cell is normalised and §21.1 says *"each rule its Rule
    cell lists governing the part of the entry it states and none first
    among them"*.
11. §21.1's *the further rules the condition reads* claimed a completeness
    four groups of rows do not have; it says *"further rules the condition
    reads, a finding aid and not the whole of them"*.
12. §21.1's `[R-SER-08]` sentence, ADR-0127's erratum's, explained its claim
    by restating it; it says *"which `[R-TYP-04]` (§12.3) records as the one
    such case"*.
13. `[R-EXT-03]` and `[R-RDR-03]` sent a reader to §15.1 for the
    index-encoding value set, which §7.4 states and L31 cites; both lists and
    §10.2's row say §7.4.
14. Appendix G's closing inventory omitted item 5's filter, tile-extent and
    layout pins; the three kinds are added in the paragraph's own form.
15. `[R-EXT-02]` opened with a universal over every numeric identifier space
    and closed by calling the trailer's flag lanes a space §6.3 partitions
    otherwise; the lanes *"are not a space of this kind and are not tabulated
    above"*.
16. `[R-CNT-09]` and §19.1 step 1 asserted that a suffix-range response
    carries F, which `[R-CNT-10]` provides against; both are hedged to *"where
    the transport discloses a range response's complete length"*.
17. §4.7's Note put a variable-length field's length prefix inside its value
    where §13.1 puts the fill's prefix in §7.4's framing; the Note rests a
    name's structurality on `[R-ENC-15]` and calls the prefix *"§7.4's framing,
    not its value"*.
18. `[R-ENC-16]`'s *each class being what the one before it is not* named an
    order two classes do not have; the clause is cut, the descriptive test's
    *none of those* carrying it.

**Deferred.** How a condition is individuated for the completeness clause,
which chains through `[R-CNF-13]` and §21.1 back to the rows: Q-I7 carries
it as a third question beside the identifiers and the pair individuation.
L23's name field, which its Detected cell places at open with a consequence
for F4 while its Instances cell folds it into the leading fixed fields: an
instance by §21.1's own test, and one the corpus has no vector for, so the
split waits for TV-0963, the gate failing on an instance with none; Q-I7
carries that too. Q-C10 carries a note that decision 1 takes the checksum
duty off placement, leaving its own question where it was.

**Declined.** Two findings the passes refuted on sentences they quoted: the
member's three verbs against the closing clause's four, decided by the head
of the same sentence, *"keeps its declarations, with these exceptions and no
other"*; and `[R-ERR-04]`'s narrowest scope for a tile's decoded size,
decided by §21.9's per-instance paragraph and made inconsequential by the
containing-scope licence.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors;
L23's split waits for its vector. Decision 1 changes what a conforming
compactor owes and nothing a reader does: a CRC over each checksummed extent
it copies, computed over bytes it reads in any case, and a refusal where one
fails, which §20.5 already obliged for every check the rule names.

**G3, in both halves.** The chartered text returned zero, so the criterion's
second half held across this repair cycle. The document carried one fork
outside that text, and this decision removes it; the reading of this ADR's
repairs, if the maintainer runs one, tests whether it stays removed.

**The repair list was ticked against the diff** before the commit, on
ADR-0119's rule: every numbered item above is in the diff, twenty-three
edits over eighteen items, and none is deferred.

## Alternatives rejected

- **Narrow the premise to the list**, saying a compactor relies on the
  structures whose bytes or offsets its output re-derives and owes no
  checksum check on an extent it copies unmoved. Rejected: it lets a
  compactor carry a corrupt extent into a fresh file_id under a clean
  trailer while the rule beside it claims reliance over everything carried;
  it contradicts `[R-WRT-07]`'s placement-free treatment of the tile half;
  and it saves a CRC over bytes already in hand. Stated here so the
  maintainer can choose it.
- **Send the fork to the ledger.** Rejected on ADR-0123's ground: the rule
  states its own principle and the alternative has no defender in the trail.
- **Split L23's name field out now.** Rejected for this commit alone:
  `tarn_check` fails on an instance the corpus has no vector for, and a
  vector ships with the section that needs it; the split and TV-0963 land
  together.

## Precedent

- **ADR-0094**: the compactor as a writer tier with a verification depth of
  its own; this ADR fixes that depth's quantifier.
- **ADR-0127**: the previous cycle's repairs, which this round read clean.
- **ADR-0125** and **ADR-0126**: a reach question decided on the rule's own
  principle with the maintainer's confirmation asked.
- **ADR-0091**: a rule's reach is settled by an ADR; this is the ADR.
- **ADR-0119**: the repair list against the diff.
- **ADR-0104**: editorial repairs ride with the decision.
