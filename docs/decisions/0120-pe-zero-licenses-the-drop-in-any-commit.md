# 0120. PE = 0 licenses the drop in any commit, and Q-B7 is moot

- Status: Accepted (resolves Q-B7, as moot)
- Date: 2026-09-03
- Covers: §20.4's MU = 0 / PE = 0 cell; §20.3 step 2's restatement of it
- Supersedes: the scope-edit gate on that cell — ADR-0041's "drop only when
  the commit modifies the record's scope", as narrowed by ADR-0066 and made
  operative by ADR-0081. Their other decisions stand; their status lines say so.
- Confirm: none

## Context

§7.2 names bit 1 of a record's flags PRESERVE_ON_EDIT, and ADR-0026 adopted
the pair from PNG: *"updaters preserve or drop per the preserve flag"*, §21.6
saying of an unknown ancillary that it is *"preserved or dropped per its PE
bit"*. ADR-0041's updater table then let a PE = 0 record be dropped *"only when
the commit modifies the record's scope"* — PNG's safe-to-copy model, under
which an editor that changes the critical data may shed a chunk that might now
be stale and one that changes nothing carries everything.

That gate has been the document's most defect-prone passage. ADR-0066 narrowed
its third limb so a tile commit could not license dropping a top-level
ancillary; ADR-0070 held that a supersede-only commit drops nothing; ADR-0080
reversed that without recording it; ADR-0081 recorded the supersession, made
the gate BCP 14 and bounded its conclusion. Rounds 10, 14, 16, 17, 27 and 30
each found a byte-level fork in the cell, and Q-B7 — whether *adding* a
non-layer top-level record is a change to *"another non-layer top-level
record"* — was found cold in three of them. A priced sweep on 2026-08-26 found
the abstract property cannot decide it either: at file scope every commit
changes the file, so *"independently changes the scope the record attaches
to"* is satisfied by the bare drop and the cell's own exclusion sentence
becomes dead letter. For a layer sub-record, *edits the layer* is crisp — the
record, the entry set, the stored-tile set. For a top-level record, *edits the
file* never was.

**The maintainer put the underlying question**: the bit is named
PRESERVE_ON_EDIT, a writer that clears it has declined preservation across
edits, and the document was nonetheless obliging updaters to preserve such a
record in most commits. That is the design question the six forks were
symptoms of, and it is the maintainer's to decide.

## Decision

**A PE = 0 record may be dropped in any commit.** §20.4's cell now reads:
*"Retain byte-identical, or drop it — its extent becoming slack. The licence
is the bit's own: the writer that stored PE = 0 declined preservation across
edits, so an updater MAY drop the record in any commit, including one whose
only effect is the drop, and a compactor MAY drop it whenever it rewrites the
file. An updater that drops such a record SHOULD report the loss; unreported,
application state disappears with no diagnostic."*

The scope-edit gate — *"An appender MUST NOT drop it except in a commit that
independently changes the scope the record attaches to"*, its two enumerated
limbs, the supersede conclusion, and *"a commit whose only effect would be the
drop MUST retain it"* — is withdrawn. §20.3 step 2's *"MUST NOT drop the
record (§20.4)"*, which restated the gate for a defective structure an appender
carries forward, now defers to the table: the drop is barred *"save where
§20.4's table licenses the drop, which it does for an unregistered record
stored MU = 0, PE = 0 and for no other"*.

Everything else in §20.4 stands: MU = 1 records are retained byte-identical and
block their scope; MU = 0 / PE = 1 records are retained byte-identical;
`[R-CNT-12]` still reads MU = 1 with PE = 0 as PE = 1, *"never silently
deletable"*; both registered types carry PE = 1, so no commit removes a layer
record or a user-metadata record; the compactor's disposal rule in §20.5 —
dropping *"only where §20.4's table licenses it"* — is unchanged in words and
now licenses the same class it always did, more simply.

## Consequences

**Q-B7 is resolved as moot.** Nothing turns on whether adding a record changes
the file's scope, because no commit needs a qualifying change. The cell that
produced six byte-level forks is four sentences with one MAY and one SHOULD.

**What is given up, stated plainly.** Under the old gate an updater that did
not understand a PE = 0 record could not discard it while touching nothing it
belonged to; under this decision it can, on any append, and the SHOULD-report
is the whole protection. Three things bound that cost. The record's own author
chose PE = 0, which this specification has always defined as declining
preservation. Retention remains the cell's first option and the default of any
updater that simply re-emits what it does not understand, which `[R-WRT-05]`
already obliges for everything it retains. And PE = 1 is available to any
writer that wants a record to survive edits by tools that do not implement it.

**Nothing moves in the register, the corpus, or any reader.** A dropped record
leaves a conforming file under the old rule and the new; the drop rule binds
updater conduct and has no file witness, so it has no row and no vector.
`tarn_editorial` reports the change as content, which it is.

**The PNG lineage is departed from, deliberately, for top-level records.**
Safe-to-copy semantics need a decidable notion of "the critical data was
edited". This format has one for a layer and not for the file, and the trail
spent five ADRs learning that. A format that wants stale-ancillary protection
at file scope needs a mechanism this one does not have — a record naming what
it depends on — and none is proposed here.

## Alternatives rejected

- **Keep the gate and close Q-B7 in the "no" direction** with one clause —
  *adding a non-layer top-level record changes no record and is not such a
  change*. This is what every round-30 pass recommended, and it would have
  closed the sixth fork exactly as the previous five were closed. Rejected on
  ADR-0106's rule: a passage wrong six times is not repaired a seventh, and the
  maintainer's question was about the gate itself.
- **Compactor-only drops** — an appender always retains, a compaction sheds.
  Decidable and safe, and rejected because it makes PE = 0 mean nothing to an
  appender, which is the tool the bit was designed for, and because shedding
  one ancillary would cost a whole-file rewrite.
- **State the test instead of the enumeration.** Rejected by the priced sweep
  before this decision: the property does not close the fork.

## Precedent

- **ADR-0026**, whose PNG-derived design this narrows: the bit keeps its name
  and its two registered values; only the updater's licence changes.
- **ADR-0106**, on a passage that has been false repeatedly: stop repairing the
  sentence and ask what it is for.
- **ADR-0081**'s observation that §20.4's cell is *the only statement of the
  updater's drop rule* in the document, which is why this decision is two
  edits and not a sweep.
