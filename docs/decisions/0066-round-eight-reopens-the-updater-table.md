# 0066. Round eight reopens the updater table

- Status: Accepted
- Date: 2026-08-14
- Covers: §20.4's MU = 1 grant at file scope; the MU = 0 / PE = 0 drop
  licence; the scope of *cannot establish*; the register's completeness
  claim
- Confirm: none

## Context

Cleanroom round 8 read the 371 lines inserted and 169 deleted across 43
sections since round 7 read the document. Its quiz held at 15 agree / 0
diverge / 0 underdetermined, and its 33 findings reduced to 22 distinct
defects — but **two are byte-level and unanimous across three independent
triage passes**, which reopens G3 after round 7 met the criterion for the
first time.

Both sit in §20.4's `[R-WRT-08]` table. That is the table round 7 repaired,
and the first of the two is a propagation failure of that repair: restoring
the table's scope to *"a type the updater does not implement"* was right for
the layer-scope half and walks the file-scope half straight into
`[R-CNT-15]`.

## Decision

**An unimplemented top-level MU = 1 record leaves an updater no commit at
all.** The MU = 1 row's file-scope grant — *"while a commit that only
changes a layer's own tiles, index, or record remains permitted"* — is
deleted. Five normative passages already compelled the opposite: §2.3's
*"updaters are readers of the files they process and inherit every reader
obligation"*, §20.3 step 2's *"the appender is a reader here"*, §19.1 step
4's MUST_UNDERSTAND gate, `[R-CNT-15]`'s *"MU = 1 → reject-file"*, and
§2.4's *"A reader MUST NOT rely on any structure in it."* §6.3 already
decides the analogous case in terms, for an unknown incompat-lane bit: the
updater *"is a reader first, and therefore rejects the file before
modifying anything."*

The candidate carve-out was not one. `[R-CNT-15]`'s *"Updater obligations
for unknown records are §20's subject"* says where the obligations live,
not that the updater is relieved of the outcome.

The mechanism settles what the citation chain only suggested.
`[R-WRT-06]` bars a compactor from a file carrying such a record because
*"such a type can define references this specification does not (§7.2), so
its bytes cannot be safely relocated"* — and §20.4 itself calls extent
re-pointing *"the operation the no-embedded-offsets rule (§7.2) makes safe
for MU = 0 records"*, pointedly not MU = 1. But `[R-WRT-04]` requires that
superseding a stored tile re-emit that layer's tile-index region at a new
placement. So the commit the row permitted is precisely the one that can
silently invalidate an unreadable critical record's references. The grant
authorized the harm `[R-WRT-06]` names.

**The MU = 0 / PE = 0 drop licence is narrowed to a non-layer record.**
*"another top-level record"* becomes *"another **non-layer** top-level
record"*, with the tile-supersede case named explicitly. `[R-CNT-13]`'s
*"the file for **other** top-level records"* settles that a layer record is
a top-level record, so the unqualified phrase was the literal reading — and
under it every tile commit changes a layer record's extent slot
(`[R-WRT-04]`), licensing the drop of any PE = 0 ancillary, making the
first disjunct redundant and the row's own purpose sentence (*"Dropping the
record is not itself such a change"*) nearly vacuous. The register writes
*"non-layer top-level record"* at F3, F4, F28, F29, F31 and F33–F35 — all 8
places it means to exclude them — so the repair follows the document's own
convention rather than inventing one.

**"Unable to check" is scoped to a capability or resource ground.**
`[R-CNF-11]`'s *cannot establish* clause was unscoped at both the verdict
and the report, and an adversary built a file arguing that since no
verifier can check `[R-COD-10]`'s shuffle stride, *conforming* is
unreachable for every file using filter 2 or codec 2/3/4. The claim does
not survive `[R-COD-10]`'s own closing words — a wrong stride with no
padding or bool witness means *"the consequence is wrong sample content —
undetectable by construction (§21.7)"* — so there is no violation to check,
not a violation the verifier cannot reach. All five of §2.3's illustrative
grounds were already capability or resource grounds; the governing clause
now says so, and §21.7 states that a requirement with no file-level witness
is not one a verifier is *unable to check*.

**The register's completeness claim is about file-conformance
violations.** `[R-CNF-07]` and §21.1 twice claimed to cover every
*detectable violation*. An over-long pre-trailer pad is a detectable
violation of a named MUST that the register omits by design, so the claim
as written had a counterexample. All three sites now read *detectable
file-conformance violation*.

## Consequences

G3 is **not met**: two byte-level ambiguities is not zero. Round 7's zero
did not survive a second cold reading of its own text, and the honest
reading is that a cleanroom round measures the text it reads, not the text
that follows it. This is the strongest argument the project has produced
for running a pass after every substantive edit rather than every several.

The §21 register is unchanged at **125 conditions over 252 instances**, and
the corpus at **305 vectors** with 100% per-instance coverage. Neither
decision adds or removes a condition: the first deletes a grant whose case
`[R-CNT-15]` already registers at F38, and the second narrows a phrase.

Priced knowingly. Deleting the grant means one experimental-range MU = 1
top-level record freezes a file against every tool that does not implement
the type — no append, and no compaction either (`[R-WRT-06]`). That is a
real loss of editability, accepted because it is what MU = 1 is for, and
because the alternative licensed an updater to relocate an index region an
unreadable record may point into. Narrowing the drop licence means a PE = 0
ancillary now survives commits that a literal reading would have let drop,
so slack grows more slowly and application state is harder to lose — at the
cost that dropping one requires a commit that genuinely touches the
non-layer record inventory.

Five findings remain escalated or deferred rather than decided here: F21's
registration against §21.6's account of the same condition, L2's collapsed
instance arithmetic, whether `[R-ENC-06]` gains a tile-scope cause row,
§21.9's short hard-limit list (which `[R-VEC-03]` binds corpus construction
to), and Appendix G's profile gaps. The first three move §21.8's totals and
the corpus, so none was applied unilaterally.

## Precedent

- §6.3's incompat-lane rule, which already resolves the updater-as-reader
  question the same way for the analogous unknown-flag case.
- ADR-0061, whose decision — persistence governs every record type — is
  unchanged; round 7's propagation of it was incomplete, exactly as round
  7's own propagation of ADR-0048 was.
- `[R-CNF-02]`'s conduct-versus-predicate split, which supplies the general
  form for scoping *cannot establish*: conduct rules bind the actor, the
  predicate binds the bytes.
- ADR-0046, under which the specification governs and a disagreeing vector
  is corrected — the authority for leaving the corpus untouched where these
  decisions change only prose.
