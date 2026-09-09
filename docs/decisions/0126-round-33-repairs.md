# 0126. Round 33's repairs: a declared alignment or slab may change, and the bar names its own category

- Status: Accepted (resolves round 33's repairable findings; decision 1
  confirmed by the maintainer on 2026-09-09)
- Date: 2026-09-08
- Covers: §20.3 step 4's permitted list, its closing paragraph and its
  fixed list; §11.1's Rationale; Appendix H's updater and reader entries;
  §2.3 `[R-CNF-02]`; §4.7's Note; §5.1 `[R-CNT-01]`; §5.2 `[R-CNT-21]`; §9.7
  `[R-LIF-08]`; §18.2 `[R-MTA-09]`; §19.1 `[R-RDR-01]`; §20.5's slack Note;
  §21.1; §21.5 R10; §21.6's closing paragraph; Appendix F
- Confirm: none. One decision was put to the maintainer and confirmed on
  2026-09-09, with its alternative stated below so a superseding ADR can
  choose it: that a layer which stores a tile
  MAY have an already-declared alignment or slab changed to another value in
  one commit, the new invariant holding over every stored tile the new state
  keeps or the declaration cleared, as `[R-SLB-04]` already provides for a
  slab.

## Context

Round 33 read ADR-0125's repairs, the audit of them and its erratum, fifteen
passages over three commits, with every lane on Opus. It returned 25 findings
from 7 reporters, 22 distinct defects, a 15/15 quiz, and one self-flagged
byte-level finding, upheld by all three passes, attacked by the
uphold-refuter, which returned UPHOLD_STANDS on Sonnet after Opus refused it twice at zero tokens, and confirmed by hand.

**The flag.** ADR-0124's list permits *"a slab or alignment declaration MAY
be declared, re-established or cleared as this step provides below"*, with
*"and no other"* closing the list. A commit that sets a layer's alignment
from 4096 to 512, every stored tile lying at a multiple of both, is on one
reading a declaration (the new generation declares 512) and on the other
none of the three verbs, a first-time declaration being *declared*, the same
value re-satisfied being *re-established*, and none being *cleared*. The
disputed file is conforming under both readings: `[R-SLB-01]`'s invariant
holds over every tile the new state keeps, `[R-CNT-16]` and `[R-CNT-23]` are
satisfied, and no register row witnesses the prior value. One updater
appends a directory-only commit under the same file_id; another refuses and
rewrites the file. The fixed list names neither A, S nor A_slab, the give-up
list names no change of alignment or slab, and the tie-break sentence does
not reach the field, so nothing in the step chooses. The hand-check found
what the passes found and two sentences that presuppose the answer without
stating it: `[R-SLB-04]` lists *"the slab declaration itself"* changing among
the events that oblige a commit to re-establish the runs or clear the
declaration, and step 4's closing sentence makes *"every one the new state
keeps, not only those this commit adds"* satisfy the new state's alignment
invariant, a clause with no work to do unless the declaration can be new or
different. The document provides for the change twice and never says it may
be made. It is new, and it is in the permitted list of §20.3 step 4, the
passage this round was chartered to read first.

**Why this is a repair here and not a ledger entry.** ADR-0124's principle
is that the fixed declarations are the ones a stored tile's meaning turns
on, and its own account of this member says *"a slab or alignment
declaration governs placement (§16), not a value, its coordinate or its
padding"*. A changed value governs placement exactly as a first declaration
does, and `[R-SLB-04]` has treated the change as a commit's event since it
was written. So the principle decides which way the list should read; what
the list lacked was the verb. ADR-0091's rule is satisfied by this ADR, and
the maintainer's veto is kept in the Confirm line.

## Decision

**1. A declared alignment or slab may change.** The permitted list reads
*"a slab or alignment declaration MAY be declared, changed, re-established
or cleared as this step provides below"*, and the closing paragraph *"a
slab declaration is declared, changed, re-established or cleared
(`[R-SLB-04]`)"*, the alignment sentence beside it already reaching every
kept tile. §11.1's Rationale and Appendix H's updater entry carry the verb.

**2. The bar names its own category.** `[R-CNF-02]` asks that a writer
obligation whose violation is not a file-conformance violation be declared
where it arises, and step 4's MUST NOT was the one writer prohibition with no
such declaration, no reader clause and no register row. It now says: *"This
bar binds the commit as an actor: the file a violating commit would produce
is conforming, the violation is not a file-conformance violation
(`[R-CNF-02]`), and no register row records it (§21.7)"*. Two reporters.

**The editorial repairs**, each confirmed by at least two passes:

3. The fixed list's *"the position of every planar channel but the last"*
   read as barring a run removal the permitted side allows; it says *"the
   position of every planar channel the new state keeps"*.
4. §5.2 and §9.7 disposed of a structurally rejected entry's bytes without
   §15.3's qualifier; both say they fall to slack *"where no other claimant
   claims them"*. Two reporters.
5. §20.5's slack Note counted the per-commit overhead and the index regions
   and omitted the superseded payloads and record extents, the largest term;
   it names them.
6. §21.6's closing paragraph gave one reason for excluding two capability
   refusals from the register, true of the foreign major alone; it now gives
   each case its own.
7. §21.1 attributed every §21.5 row's outcome to `[R-CNT-25]`'s quarantine;
   it names `[R-MTA-09]` beside it, which assigns the outcome for a frame
   constraint the document survives.
8. §4.7's Note said §7.4's table omits the offset and class columns; it omits
   the size column too, a field's size following from its type.
9. Appendix F, which is normative, lacked RFC 1950 and RFC 1952, cited by
   `[R-COD-05]` and required by T15's instances; both are listed.
10. §21.1's convention for the Governing-rule parenthetical did not admit
    the section references L26 and L31 carry; it does now. R10 cites
    `[R-CNT-25]` as its four siblings do. Two reporters.
11. §19.1's open path computed F − 64 before the 128-byte floor; step 1
    states the floor.
12. `[R-CNF-02]`'s enumeration of writer obligations declared not to be
    file-conformance violations omitted `[R-LIF-02]`'s barriers, which §9.2
    so declares; they are listed.
13. §5.1 called the superseded directories and trailers between the front
    block and the live trailer *"structures"*, a word §5.2 reserves for the
    live state; it says *"regions"* and names the superseded ones slack.
14. `[R-MTA-09]`'s SHOULD stated no consequence of deviation, the one such
    SHOULD in the document; it states one.

**Deferred.** Three findings ask a decision this ADR does not take. Whether
the extent of a record of an unassigned type, which no checksum covers, owes
the naming duty `[R-MTA-10]` places on a checksummed uninspected extent: Q-C8
carries it. Whether a compactor's duty to refuse a structurally malformed
entry should turn on the placement it chooses: a new ledger entry, Q-C10.
Whether §21.1's own rules should carry requirement identifiers, and how F33
and L18 individuate a two-claimant overlap: recorded with the register debts
beside T-01.

**Declined.** Three findings the passes refuted on sentences they quoted:
§21.5's experimental-encoding exception leaves R2 in force by `[R-MTA-10]`'s
closed list; the *"replacing the last channel"* gloss cannot reach a rename
the same step permits twice; §18.2's *"1 or 2; see below"* is the document's
established deferral. Two more the text decides and this ADR leaves: F5's
second instance reaches committed_file_length through `[R-CNT-01]`, which
its cell reads; `[R-CNF-13]`'s *"applies unchanged"* preserves an exemption
and creates none.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors.
Decision 1 binds a commit's conduct with no single-file witness, as the
list has none; decision 2 says so of the whole list. No reader behaviour
changes.

**What decision 1 costs a caller**: nothing. A writer that wanted a
different alignment could clear it in one commit and declare it in the next;
now it does both at once, under the same obligation to every kept tile.

**G3's second half is not met by this round**: round 33 read round 32's
repairs and their audit, and returned one byte-level flag, new, in the
permitted list ADR-0124 wrote and two audits and a round had read. Round 34
reads this ADR's repairs, and the criterion turns on it.

**The repair list was ticked against the diff** before the commit, on
ADR-0119's rule: every numbered item above is in the diff, and none is
deferred.

## Alternatives rejected

- **Bar a value change**, adding *"a change to a declared alignment or slab
  value"* to the give-up list. Rejected: it forbids in one commit what two
  commits achieve, which is the shape ADR-0124 removed; it contradicts
  `[R-SLB-04]`'s standing treatment of a changed slab declaration; and the
  principle beside the list gives no reason for it. Stated here so the
  maintainer can choose it.
- **Leave the verb to inference** from *"several of these changes at once"*,
  a clearing and a declaration composing into a change. Rejected: round 32
  and its audit each found a composition the list's words did not decide,
  and a rule a reader must compose is the shape that has produced the next
  finding every time.

## Precedent

- **ADR-0124**: the closed list and the principle beside it; the member's
  own account, that a slab or alignment declaration governs placement.
- **ADR-0125**: a reach question on the list decided on the trail's ground
  with the maintainer's confirmation asked.
- **ADR-0091**: a rule's reach is settled by an ADR; this is the ADR.
- **ADR-0119**: the repair list against the diff.
- **ADR-0104**: editorial repairs ride with the decision.
