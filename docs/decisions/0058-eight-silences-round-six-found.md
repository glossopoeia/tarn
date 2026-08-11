# 0058. Eight places the rules were silent

- Status: Accepted
- Date: 2026-08-11
- Covers: name namespaces; the front-block obligation's addressee; layer-name
  uniqueness ordering; `generation`'s ceiling; metadata member sort depth; the
  lz4 cap under a planar layout; experimental metadata encodings; the zstd
  window derivation
- Confirm: none

## Context

Cleanroom round 6 produced 85 findings, which triage reduced to 67 distinct
defects and 5 byte-level ones under a strict test: *does resolving it change
which byte sequences a conforming implementation may emit, or must accept or
reject?* Three more carried two-of-three support.

What the survivors have in common is worth stating, because it is not what the
earlier rounds found. Rounds 4 and 5 found **propagation failures** — a rule
changed in one place and left standing in another. These are **silences**: a
rule that says something true and stops short of a case a reader will meet. No
table contradicts them; there is simply nothing to read.

The over-report is instructive in the same way. Reporters flagged 33 findings
byte-level; 5 survived. The dominant cause was a reporter finding a register
row that contradicts a rule and concluding the verdict is open — when §21.1's
*"where a row and the rule it cites diverge, the rule governs"* has already
decided it, and only the table is wrong.

## Decision

**Names.** Dimension names and channel names are **separate namespaces**
within a layer. A layer may carry a dimension and a channel of the same name —
the ordinary way to name a channel after the axis it samples, and a convention
users arrive with from the array ecosystems this format targets. Forbidding it
would have rejected the idiom for no gain.

**The front signature block's addressee.** The obligation now turns on
**residency**, not on transport class: a reader whose open leaves bytes
[0, 16) resident MUST verify them; one that would have to issue a further range
request MAY defer or omit. The local/remote distinction stays — §6.4's request
accounting needs it — but it no longer decides this, because a memory mapping
over a network filesystem satisfies both definitions while residency is
decidable at any reader's own open path.

**Layer-name uniqueness runs first, over raw bytes**, whether or not each name
is well-formed. `[R-ENC-12]` already makes name comparison a byte comparison,
which needs no valid name, so two byte-identical name fields are a duplicate
even when neither name is valid. The alternative made a file-scope check depend
on which layers survived a prior layer-scope one.

**`generation` carries its ceiling into the gate list.** §6.2's table asserted
`1 ≤ generation ≤ 2⁶³ − 1` while `[R-CNT-06]`'s ordered validation stopped at
`≥ 1`. The bound is now checked, matching every other u64 the trailer carries.

**User-metadata members sort at every nesting depth.** The rule's own purpose —
*"This makes one writer's output reproducible for identical content"* — holds
only recursively, and §18.4 registers nested objects. Two conforming writers
given identical content were free to emit different bytes.

**The lz4 cap binds any addressed tile.** A planar layer has one decoded size
per channel plane, so *"the tiles' decoded size"* in the singular did not say
which. The largest governs, because the cap exists to keep every tile inside
what the block format can address.

**An experimental-range metadata encoding leaves the file conforming.** §21.6
had already decided the identical question for record types — `[R-CNF-02]`
makes §10.3's prohibition bind a writer's conduct and not the bytes — so the
register's row is narrowed to the reserved range and §21.6 gains the
experimental case. The register is **125 conditions over 242 named instances**.

**The zstd window derivation needed no decision.** RFC 8878's two derivations
agree on every tile: with Single_Segment_Flag set, `Window_Size` *is* the frame
content size, which this rule already obliges to equal the decoded size;
without it, the Window_Descriptor cannot express less than 1 KiB and so exceeds
any sub-1-KiB tile under either reading. A Note now records that a small tile
is encodable only as a single-segment frame. Two of three triage passes called
this byte-level; it is not.

## Consequences

Five byte-level ambiguities close, and each closes with a clause rather than a
redesign — which is the honest measure of how much of G3's remaining distance
was drafting rather than design.

The corpus follows: two vectors that claimed a register row for an
experimental-range encoding now name no row and ship as positive vectors for
§21.6's defined behavior, keeping their identifiers and their bytes.

Priced knowingly. The residency test replaces a classification the document
could not observe with one it can, but it does not make every reader check the
front block — a remote reader fetching only the trailer and directory still
never sees those bytes, and that was always the intent. And two namespaces mean
a tool addressing "the thing called x" in a layer must say whether it means the
dimension or the channel; the format never addressed either by name, so the
cost falls on tooling conventions rather than on files.

Nothing here touches the ~59 remaining defects, which are editorial: stale
sentences, dangling cross-references, mislabelled figures, register
bookkeeping. They are recorded in `docs/cleanroom/06-g3/findings.md` and remain
undispositioned.

## Precedent

- ADR-0049, 0056 and 0057, which repaired propagation failures and rows without
  witnesses. This one repairs a third kind — a rule that stops short — and the
  distinction is why a sixth cleanroom round found what a mechanical checker
  and a corpus could not.
- §21.1's row-versus-rule tiebreak, which did most of the triage's work by
  disposing of findings where only a table was wrong.
- netCDF's coordinate-variable convention, where a variable is deliberately
  named after its dimension — the precedent behind two namespaces.
