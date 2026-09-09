# 0129. Writers are bound by their operations: three tiers, two classes, and compaction one rewrite among several

- Status: Accepted (resolves Q-A8 on the maintainer's direction of
  2026-09-09)
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
  2).

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
