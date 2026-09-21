# 0129. Writers are bound by their operations: three tiers, two classes, and compaction one rewrite among several

- Status: Accepted (resolves Q-A8 on the maintainer's direction of
  2026-09-09; decision 2 withdrawn by ADR-0130 the same day, the layer
  record carrying PE = 0; §20.1's mapping restated as two positions on the
  maintainer's direction of 2026-09-21, the erratum of that date)
- Date: 2026-09-09
- Covers: §20.1's tiers and `[R-WRT-01]`; §2.3 `[R-CNF-06]` and
  `[R-CNF-02]`'s flags gloss; §20.5 whole, retitled, with `[R-WRT-06]`,
  `[R-WRT-07]` and `[R-WRT-09]`; §20.4's table and its layer-removal
  paragraph; `[R-LIF-01]`; §6.2's flags row; §6.3 `[R-CNT-08]`; the Notes
  of §3.3, §5.1, §7.2, §9.7 and §20.3; §5.2 `[R-CNT-21]`; §20.3 step 4's two
  citations of the rewrite; §21.6's slack entry; §23.1 `[R-PRV-03]` and
  `[R-PRV-04]`; Appendix G items 2 and 8 and its closing paragraph;
  Appendix H's writer and updater entries
- Confirm: none. The maintainer directed option (a) of Q-A8 on 2026-09-09
  and named the rewrites. One consequence is a permission the document did
  not carry and is stated below so a superseding ADR can withdraw it: a
  rewrite MAY omit a layer from its output, which no commit may (decision
  2). The erratum of 2026-09-19 put one byte-level repair to the
  maintainer, §20.1's two class tests made exclusive on a decode test; the
  maintainer declined it on 2026-09-21 and directed the two positions of
  the erratum of that date (E3). Nothing is outstanding.

## Context

Q-A8 recorded the maintainer's question: §2.3 defines five conformance
classes and §20.1 three writer tiers on two axes the document never
related. The classes bundle obligations, a writer answering for the bytes
it produces and an updater additionally for what it carries forward; the
tiers are shapes of operation, indexed by whether the operation has an
input file and whether its output keeps that file's identity. An appender
and a compactor were both updaters and a creator only a writer, and no
sentence said so. §20.5 specified the compactor closely, and its history
was a fork in every sentence that restated a general rule for that one
tier: Q-A6, decided twice; ADR-0083; ADR-0120; ADR-0128. Meanwhile the
document routed two other operations to *"a whole-file rewrite under a
fresh file_id"* and specified neither: §20.3 step 4 sent a changed fixed
declaration there, citing §20.5, and §20.4 sent dropping a layer there,
adding *"That is not compaction, which carries every layer of its input
forward"*. A tool that re-declared one layer, or dropped one, and still had
to preserve the records it did not understand had no rules.

**Why the tiers bind claims and not files.** File conformance is a
predicate on bytes (`[R-CNF-02]`). A tool that reads a file with a library
and writes what it understood through the creation path emits a conforming
file and is a conforming reader and creator; what it is not is an updater,
and the difference shows only in what the input carried that the tool did
not understand: a PE = 1 record dropped, an ignore-lane bit cleared, an
unknown MU = 1 layer skipped where a compactor had to refuse. So the tier
names carried no obligation of their own, and every obligation in §20.5
attached to an operation the compactor happened to perform: creating a
file, carrying forward a structure undecoded, relocating a structure, and,
in the two unspecified rewrites, re-creating a layer or dropping one.

**Why the layer drop is a decision.** §20.4's table gives a layer record
PE = 1, so no updater may drop one by commit, and the reason it gives is
the commit's: an in-place removal strands the layer's tiles and index as
slack and *"would cost what it appears to save"*. A rewrite carries no
slack, so the reason does not reach it, and the document had already
conceded the operation to a creator's new file, at the cost of every
record such a creator does not understand. Naming the rewrite gives the
operation to an actor that preserves what it does not understand, and
that is a permission the updater class did not have.

## Decision

**1. Writers are bound by their operations.** §20.1 states the mapping
once: the tiers are shapes of operation and §2.3's classes are the
obligations they carry. *"A creator is a writer and nothing more"*; *"An
appender and a rewriter are updaters"*, the appender's commit extending its
input under the input's file_id and the rewriter's output a new file under
a fresh one. *"Every obligation of §20.3 through §20.5 attaches to an
operation and binds whichever writer performs it: a writer that carries
forward any structure of an input file it did not decode is an updater and
owes §20.4's preservation for every record of that file, whatever else it
changes, and one that decodes everything it writes is a creator, whatever
it read."* §2.3's updater definition points at the two tiers. The third
tier is the **rewriter**, which *"writes a new file from an existing one
under a new identity (§20.5), carrying structures forward, re-creating
some, or dropping some"*; compaction is *"the rewrite that reclaims slack"*.
§20.5, retitled *Rewriting*, states its obligations by operation: what a
rewriter carries forward it preserves and verifies (`[R-WRT-07]`,
`[R-WRT-09]`); what it relocates it regenerates and re-points; a type it
does not implement with MU = 1 it refuses to relocate (`[R-WRT-06]`); what
it re-creates *"it decodes as a reader (`[R-CNF-11]`) and writes as a
creator (§20.2)"*. It names three rewrites, compaction, dropping a layer,
and re-declaring a layer that stores a tile, says *"A rewrite MAY be
several of these at once"*, and defines none other; physical reordering is
a placement choice inside any of them, a rewriter preserving no placement.
`[R-WRT-07]`'s bit-for-bit claim is scoped to what the output carries:
*"a rewrite changes where bytes live, never what a carried layer denotes,
and what a re-created layer denotes is the rewriter's to declare"*.

**2. A rewrite MAY omit a layer.** §20.5's dropping case reads *"dropping a
layer, which no commit removes (§20.4) and a rewrite does by omitting the
layer's record, index region and stored tiles"*, and §20.4 names it as its
table's one exception: *"it omits the dropped layer's record, index region
and stored tiles from its output, and carries every other record under the
table"*. A top-level user-metadata record keeps its PE = 1 and is edited by
superseding, as before. Appendix H's updater entry scopes *never removes a
layer record* to a commit.

**The renamings.** Every obligation stated on a compactor is stated on a
rewriter: `[R-CNT-08]`'s carry-forward and §6.2's flags row, §7.2's Note,
§20.4's two table rows, `[R-WRT-06]`'s fresh file_id, creation path, flags,
version_minor floor and MU = 1 refusal, `[R-WRT-07]`'s preservation and
regeneration, `[R-WRT-09]`'s verification, Appendix G items 2 and 8 and its
closing paragraph, Appendix H's writer entry. `[R-LIF-01]` names the second
kind of mutation *"a rewrite, §20.5"*; §5.1's Note, §20.3 step 4 and its
Example, §5.2, §9.7's Note, §21.6's slack entry, §20.4 and §23.1 say a
rewrite where they said compaction of the operation at large. The word
survives where it names the case: reclaiming slack (§1, §5.2, §20.3's
Note, §23.1's publication advice, Appendix D), §3.3's Note on actors that
cannot decode, §20.5's figure, and Appendix G item 8's reproducibility
claim, which is compaction's.

**Deferred.** Q-A7 and Q-C10 carry a note that their actor is now a
rewriter; each question is where it was.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331
vectors. Every obligation here is a conduct rule with no file witness, and
no reader behaviour changes. What changes for writers: a tool that carries
forward any undecoded structure owes preservation for the whole file,
whatever else it changes, which the updater class already said of tools
that modify a file; a rewrite may now omit a layer; and the two rewrites
the document had routed to §20.5 without rules have them.

**What decision 2 costs a caller**: nothing a commit could do. A caller
that wants a layer gone still cannot remove it by commit; it now has a
rewrite that removes it and keeps every record the tool does not
understand, where before it had only a creator's new file that kept none.

**The audit that precedes the next round reads this ADR's edits**: forty
or so sentences over fifteen sections, most of them a renamed actor and a
handful new, the two new paragraphs of §20.5 and §20.4's exception the
ones to read hardest.

**The repair list was ticked against the diff** before the commit, on
ADR-0119's rule: every site named above is in the diff, and none is
deferred.

## Alternatives rejected

- **A sixth conformance class, conforming compactor** (Q-A8's option (b)).
  Rejected: it gives a claim a name at the cost of a class whose
  obligations are conduct rules with no register row, and leaves the two
  other rewrites unspecified.
- **Leave the tiers and add the mapping sentence** (option (c)). Rejected:
  it leaves §20.5's restatements where the forks have lived and the two
  rewrites without rules.
- **Name physical reordering as a fourth rewrite.** Rejected: a rewriter
  preserves no placement, so reordering is a choice inside any rewrite and
  not an operation with obligations of its own.
- **Withhold the layer drop from a rewrite**, keeping §20.4's table
  absolute. Rejected: the table's reason is the commit's stranding cost,
  which a rewrite does not pay, and the only alternative the document
  offered lost every record the tool did not understand. Stated here so
  the maintainer can withdraw decision 2 alone.

## Precedent

- **ADR-0041**: compaction's identity and verification depth, which this
  ADR restates over the rewriter.
- **ADR-0094**: the creation path binds a rewriter, on the ground §20.5
  keeps.
- **ADR-0061** and **ADR-0120**: the preservation table governs every
  record type; decision 2 is its one stated exception.
- **ADR-0128**: the checksum duty follows what the actor carries.
- **ADR-0091**: a rule's reach is settled by an ADR; this is the ADR.
- **ADR-0119**: the repair list against the diff.

## Erratum, 2026-09-19 — the pre-round-36 audit

The audit ADR-0130's erratum describes, nine lanes and every one
fallback-grade, both Opus cross-hunk passes having been refused twice, found
sixteen distinct defects in this decision's wording. Thirteen are repaired in
the commit carrying this erratum and three declined.

**One is byte-level by the hand-check: §20.1's two class tests.** Three
lanes converged on it and both cross-hunk passes graded it byte-level; the
tiers lane graded it down, having missed the trailer. Decision 1's mapping
said an appender and a rewriter are updaters, and then that a writer that
decodes everything it writes is a creator, whatever it read. A tool that
reads a file whole and writes a new one from decoded content is a rewriter
by §20.1's bullet and §20.5's opening, and a creator by the test; on an
input carrying an unknown ignore-lane bit the first MUST copy the bit
forward (`[R-WRT-06]`) and the second MUST write flags = 0 (`[R-CNT-08]`),
and both outputs are conforming files. The same test, read of an appender
that implements every record it meets, made it a creator and freed it from
§20.4. **Repaired on this decision's own ground**, the Context's *Why the
tiers bind claims and not files*, which says such a tool is a conforming
reader and creator and not an updater, the difference showing in an
ignore-lane bit cleared: the test governs a new file, and the tiers are
exclusive. §20.1 reads *"a writer that extends an input file, or carries
forward into a new one any structure of an input file it did not decode, is
an updater"* and *"one whose output is a new file in which it decodes
everything it writes is a creator, whatever it read, and not a rewriter:
§20.2 binds it and §20.5 does not, it writes flags = 0"*. **Confirm**: the
repair follows what this ADR argued, but it decides a trailer's bytes, and
the alternative, that any new file written from an existing one is a rewrite
whatever its writer decodes, is stated so the maintainer can choose it.
*(Declined and replaced on 2026-09-21; see the erratum of that date.)*

**The renaming's leftovers.** §3.3's Note kept *compactors*, deliberately,
for the actors that cannot decode; six of the nine lanes reported it as the
rename's one survivor, and the word names no tier now: *"rewriters carrying
a layer forward"*. `[R-PRV-02]` said compaction is the only operation that
removes slack, and §9.3's Note that compaction is the continuation past F's
ceiling; both are true of every rewrite and say *"A rewrite (§20.5)"*.
Appendix G item 8, which the decision kept as compaction's claim, attributed
to a compaction's output the records §20.4 lets it drop, and compaction as
§20.5 defines it drops nothing (four lanes): *"A rewriter's output"*. §20.5's
"A rewrite MAY be several of these at once" could not be true of compaction
as defined, which changes nothing but placement: *"A rewrite MAY do several
of these at once, dropping one layer, re-declaring another and carrying the
rest forward, and is compaction only where it does nothing but carry"*. The
Example's "moves live bytes" was compaction's and reads *"changes what a
range holds"*.

**Restatements of an updater's duties.** §2.3 defines an updater as a tool
that modifies an existing file and then names the rewriter, whose output is
a new file, as one of its tiers: *"A tool that modifies an existing file, or
writes a new one from it"*. `[R-CNF-02]`'s flags gloss cited §20.5 alone for
an updater's copy-forward: *"§20.3 step 6 and §20.5"*. `[R-CNT-08]`'s MUST
ranged over "the file it modifies": *"its input file"*. Appendix H's updater
entry, headed for both tiers, stated step 4's list of what a commit may
change as though it bound a rewriter: *"as an appender, changes a layer that
stores a tile"*. Its rewriter sentence keyed regeneration to each index
region the rewriter relocates, where `[R-WRT-07]`'s trigger is a region any
of whose stored extents the output relocates, and called the regenerated
result verbatim; it restates `[R-WRT-07]` in that rule's words.
`[R-WRT-06]`'s version_minor sentence carried three dashes, the second
opening an aside inside the first pair: a colon.

**Declined.** The rewrite lane's C-01, which it graded byte-level: decision
1 says in terms that what a re-created layer denotes is the rewriter's to
declare, the lane itself found one reading, and a constraint there would be
vacuous while a rewrite MAY drop a layer and add what a creator could. The
tiers lane's D-08: Appendix H cites `[R-WRT-06]` for the fresh file_id, and
the identifier closes the two paragraphs it labels; §6.3, §23.2 and
Appendix G cite it the same way. The tiers lane's D-07: §20.4's last row
says an updater MAY drop the record in any commit; an updater that commits
is an appender, and the row's next clause names the rewriter.

## Erratum, 2026-09-21 — the maintainer's ruling on §20.1's class tests

The erratum of 2026-09-19 repaired §20.1's two class tests by making them
exclusive on a decode test, and put the repair to the maintainer. **The
maintainer declined it on 2026-09-21 and directed another.** The ruling:
both tools the fork names are legitimate, a converter that preserves what it
does not understand and a copier that carries data alone; both outputs are
conforming files, and neither is to be barred. §20.1 was drawing the line
without the mechanics that matter, and a rewriter is better defined by what
it undertakes to preserve.

**What was wrong with the first repair.** A line drawn at whether the writer
decoded every byte it wrote makes a tool's class turn on its input. A
converter that re-creates every layer and carries unknown records verbatim
is a rewriter on a file that holds an unknown PE = 1 record, and copies an
unknown ignore-lane bit forward; on a file that holds none, everything it
writes is decoded, the repair made it a creator, and the same tool was
obliged to clear the bit. In that second case the repair also barred the
preserving converter outright. The repair was the driver's, and the error
with it.

**Decision E3. A writer of a new file from an existing one takes one of two
positions, and the choice is its own.** The mechanic is the one §2.3 already
carries. A creator answers for every byte it emits (`[R-CNF-05]`) and owes
its input nothing. An updater answers for the bytes it produces
(`[R-CNF-06]`), a violation latent in what it carries forward unmodified
travelling with it (`[R-WRT-01]`), and owes preservation in exchange. §20.1
reads *"A writer of a new file from an existing one takes one of two
positions, and the choice is its own"*; of the rewriter, that it undertakes
to preserve its input and *"in return it answers for what it carries forward
unmodified only to `[R-WRT-09]`'s depth"*; and of the creator, that *"it
answers for every byte of its output (`[R-CNF-05]`), bytes it copied from
another file included"*. The appender's half stays forced, because it is
observable: *"A writer that extends an input file is an appender and an
updater, whatever it decodes: the file it leaves holds every byte of its
input"*, which closes the hole the decode test had opened for an appender
that implements every record it meets. No prohibition on mixing the two
positions is needed: a writer that does not undertake preservation is a
creator, and a creator has no carve-out to take. A rewriter that re-creates
every structure of its input still copies the ignore-lane bits forward,
having undertaken preservation; exempting full re-creation would bring back
the flip.

**With it.** §20.1's rewriter bullet described a shape of operation the
data-only copier fits too, and says *"preserving what it does not understand
as §20.4 provides"*. §2.3's updater clause, which the erratum of 2026-09-19
had widened to any tool that writes a new file from an existing one, says
*"writes a new one that preserves it (§20.1)"*.

**What this costs** is what this decision's Context already accepted: a tool
sold as a compactor may be a creator that loses what it did not understand,
and no byte shows it. Such a tool cannot claim updater conformance, and a
claim is the only place the line can sit, a new file under a fresh file_id
recording nothing of where its content came from.

**The fork is closed by barring neither reading.** An implementer asking
which class their tool is reads that the choice is its own, and each choice
determines the trailer's flags. Decided by the maintainer; no confirmation
is outstanding on this ADR. Register unchanged: 120 conditions, 277
instances, 331 vectors. Three edits, ticked against the diff.

## Erratum, 2026-09-21 — the scoped second audit

The audit ADR-0130's erratum of this date describes, four lanes and every
one fallback-grade, read E3 the day it landed. **It found nothing against
the two positions**: the by-operation pass carried a compaction, a rewrite
re-creating every layer, a tool writing a new file from decoded content and a
tool copying tiles undecoded to the trailer's bytes, on an input carrying an
unknown ignore-lane bit, an unimplemented PE = 1 record and a higher minor,
and found each decided; and an appender implementing every record it meets
is an updater still. Four defects are this decision's, three repaired and
one declined.

**Two are in the text E3 added beside the paragraph.** The rewriter bullet
said *preserving what it does not understand as §20.4 provides*, where
`[R-CNF-06]` has §20.4 govern every record type, *"not only those it does
not understand"*, and the paragraph below it says every record (two lanes):
*"undertaking to preserve it as §20.4 provides"*. §2.3's updater clause said
a tool that writes a new file *that preserves it*, which a rewrite that
drops a layer or re-declares one does not do on the words' face: *"as a
rewriter writes a new one from it (§20.1)"*. And Appendix H's updater entry,
whose step-4 clause the erratum of 2026-09-19 scoped to an appender, left
the validation clause beside it unscoped, citing §20.3 for a duty that is
`[R-WRT-09]`'s in a rewriter: *"validates, as an appender, the trailer and
full directory"*, with *"a rewriter's depth being `[R-WRT-09]`'s"*.

**Declined.** The positions lane's B-01, that *§20.4's table for every
record* overclaims against the table's own licence to drop. What a rewriter
undertakes is the table, and the table is what licenses the drop; the bullet
above names dropping, and the by-operation pass read the same words as the
correct quantifier. The maintainer's sentence stands as approved.
