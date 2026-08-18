# 0070. A supersede-only commit drops nothing

- Status: Accepted
- Date: 2026-08-17
- Covers: the scope of §20.4's tiles-only caveat; round 10's editorial tail
- Confirm: none

## Context

Cleanroom round 10 read the 157 lines inserted and 130 deleted since round 9,
which is every fix round 9 landed plus ADR-0068 and ADR-0069. Its quiz came
back 15 agree / 0 diverge / 0 underdetermined for the fourth round running,
and its 44 findings reduced to 27 defects with **one** byte-level — in a
clause ADR-0066 wrote.

§20.4's MU = 0 / PE = 0 row let an appender drop an unknown record only in a
commit that *independently* changes the scope the record attaches to, listing
two branches — a sub-record's layer, and a top-level record's file — and then
closing with an em-dash caveat: *"a commit that only supersedes a layer's
tiles is not such a change, though it re-places that layer's index region."*

The caveat can attach to the top-level branch alone or to the whole
enumeration, and the two give different bytes. Attached narrowly, superseding
a tile changes *"that layer's … stored tiles"* and so licenses dropping that
layer's unknown sub-record. Attached globally, it never does. Two reporters
took the narrow reading independently; two of three triage passes upheld the
finding as byte-level; the skeptic downgraded it on the ground that the next
sentence reuses *"such a change"* with a global antecedent — which shows the
global reading is available, not that the embedded clause is unambiguous.

The drafting intent covered neither branch: the caveat was added to stop a
routine tile commit licensing the drop of a *top-level* ancillary, and the
sub-record branch was never considered.

## Decision

**The caveat is global, and the text now says so.** Superseding a stored
tile's bytes is not a change to the scope any record attaches to, for either
kind of record, so a commit whose only change is a supersede MUST retain the
record.

The sub-record branch's triggers are restated so they carry that meaning
without straining: *"that layer's record, the entry set of its index, or
which of its tiles are stored."* Adding a tile, unstoring one, growing an
extent across a grid boundary or editing the layer record all remain
triggers. Only re-writing an existing tile's bytes is excluded — which is
what the caveat was always about.

The reason to prefer this reading over the drafter's original narrow one is
the row's own purpose. Its closing sentence already refuses to let a commit
manufacture its own licence (*"Dropping the record is not itself such a
change"*), and the narrow reading would have let the format's single most
routine commit silently destroy application state, protected only by a
SHOULD-level report. That is the protection ADR-0066 gave top-level records;
sub-records get it too.

## Consequences

An unknown MU = 0 / PE = 0 sub-record now survives every tile supersede, and
an appender that wants to drop one must make a commit that genuinely changes
its layer. Slack grows more slowly and application state is harder to lose;
the cost is that shedding an unwanted ancillary takes a commit that touches
the layer for another reason, or a compaction.

Nothing moves in the register or the corpus: **121 conditions over 248
instances, 300 vectors**.

### The editorial tail

Twelve further repairs landed with it. Three are consequences of the two
previous ADRs, which is the pattern this gate keeps producing:

- **`[R-ENC-06]` had no register row and no exemption.** ADR-0069 retired its
  rows on the ground that fixed widths are not a state a file can be in, and
  left §21.7 — the account, by class, of what escapes the register — not
  saying so. It says so now.
- **ADR-0068's summary omitted the layer-scope user-metadata sub-record**, in
  §20.4 and again in Appendix H's updater checklist.
- **§18.4 cited §21.7 for a ground §21.7 does not state.** The reason
  standardized-key placement carries no verifier obligation is §21.6's
  declaration that it is not a violation; §21.7 is about sample content.

The rest: `[R-CNT-04]`'s residency gloss led with *"a local file"*, a
transport classification in a test the same paragraph twice says is not about
transport — round 9 deferred this as editorial and round 10 argued it to
byte-level; it is decided by the rule's own closing sentence and by Appendix A
applying literal residency, but the gloss is repaired. §21.8 called a row's
outcome a *verdict*, a closed three-value term that contains no outcome.
T15 and T16 lacked the cause-row annotation T13 and T26 carry. L22's
Instances cell named three fields its equality never reads; relabelled as the
three alternatives its condition already states, which keeps the count at
three and the three existing vectors, re-annotated. `[R-MTA-09]`'s decline
was unscoped and read onto an experimental-range encoding §21.6 calls
conforming. Appendix G's zeroing reached only gaps a *declared* alignment
forces, leaving the pre-trailer pad free. The front matter claimed
conformance checklists cite identifiers and never prose positions, which
Appendix H contradicts throughout.

Six defects are deferred as maintainer decisions rather than edits: the field
taxonomy's residual class against `generation`, `file_id` and the name fields;
*"region"* being undefined in `[R-CNT-21]`'s partial slack total; the
appender's missing counterpart to §20.5's refusal rule; §21.9's omitted
validity floors; the corpus being normatively keyed to row labels no clause
promises to keep stable; and `[R-VEC-04]`'s intact-sibling pair, which for a
verifier-detected row names a scope no reader is obliged to refuse.

## Precedent

- ADR-0066, whose narrowing of the same row this completes; the decision
  there was right and its clause reached one branch of two.
- `[R-CNT-14]`'s rule that record order carries no meaning, which is why
  retention costs nothing but bytes.
