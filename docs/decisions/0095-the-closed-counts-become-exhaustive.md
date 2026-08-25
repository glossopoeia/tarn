# 0095. Two closed counts are replaced by statements exhaustive by construction

- Status: Accepted (resolves the round-25 re-audit's confirmed findings)
- Date: 2026-08-25
- Covers: §23.1's enumeration of how a commit removes sample data; §11.1's
  shrink Rationale
- Revises: the counts ADR-0094 wrote in both places
- Confirm: none

## Context

The audit of ADR-0094 returned **19 findings, four self-flagged byte-level**;
verification gave 1 CONFIRMED, 1 PARTIAL and 10 REFUTED, with 7 left unverified
by the per-auditor cap.

**The compactor reversal held.** Seven findings attacked it — on the
`[R-WRT-01]` warrant's "for the bytes it produces" quantifier, on §6.2's scoping
of the pad to commits, on the inference drawn from `[R-LIF-01]`, on whether
§20.2's content obligations come along — and **every one was refuted**, the
decisive citation being §2.3's own statement that conduct rules bind the actor
while the predicate binds the bytes. ADR-0094's central decision stands.

What did not hold were the two enumerations ADR-0094 wrote around it, and they
failed the same way for the third and fourth time in this passage's history.
§23.1 has now been **two** ways, then **three**, and each count was short. The
audit found a fourth (unstoring a tile, which §20.3 step 4 names in its own
vocabulary — "entries for tiles this commit **stores or supersedes** … entries
for tiles that **become unstored**" — and which §23.2 cites §23.1 for by name,
so the cross-reference pointed at a list without the case it cited for). Two
auditors found it independently, and a third found a *fifth*: a shrink whose new
padding positions all fall in tiles the superseded generation never stored,
which carries no §14 obligation and is permitted with no fill precondition at
all.

ADR-0094's §23.1 sentence also carried a tense defect of the class this project
has found most often. The **permission** is quantified over the superseded
generation; the **consequence** — bytes remaining inside a live stored tile — is
quantified over the live one. "Without de-addressing it" was offered as the
hinge between them and cannot bear it, because de-addressing is not the only way
a tile stops being live-stored: the same commit may unstore it, and then the
bytes are slack rather than live padding.

## Decision

**Neither passage states a count.** Adding one more member each time a count is
found short has now failed three times, so both are restated in a form that
cannot be short.

**§23.1 partitions by consequence, not by operation.** It says a commit removes
sample data by making it unreachable and never by erasing it, names the
operations that do so without offering the list as closed, and then splits on
the one distinction that is exhaustive: **where the structure carrying the bytes
leaves the live state** they are slack, and **where it does not** — a shrink
turning real positions into padding of a tile the new state still stores — they
remain inside that tile as its padding content. Those two cases are exhaustive
because the bytes either travel out of the live state or stay in the structure
that carried them, and the section now says so. That also fixes the tense: the
consequence is keyed to the live state explicitly rather than to a hinge that
could not carry it.

**§11.1's Rationale drops its closure.** A shrink is permitted wherever it
alters nothing §14 fixes, and three ways that happens are named — a tile dropped
out of the addressed set, a tile the superseded generation did not store, and a
new padding position whose stored byte already holds the fill — with the
observation that one shrink can do several at once. The previous wording offered
two as alternatives when they routinely co-occur.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. No
propagation acknowledgement was needed; the checker returned clean.

**The general lesson, and it is about drafting rather than about this passage.**
A closed count in normative prose is a claim about the whole document, and this
project has now had four of them found short in four cycles — §20.5's identifier
spaces, §21.7's trailer obligations, and §23.1 twice. Every one was written by
someone enumerating from memory of the passage rather than deriving from the
rule. **Where a partition can be stated by a property the members must satisfy,
state it that way**: the property is checkable against any candidate, while a
list is only checkable against the candidates someone thought of.

## Precedent

- §20.3 step 4's own vocabulary, which distinguishes storing, superseding and
  becoming unstored inside one sentence, and which §23.1 had been eliding.
- §23.2's cross-reference into §23.1 for the unstored case, which is what made
  the omission a dangling pointer rather than a matter of taste.
- ADR-0091's rule that a repair which must invent a warrant is a decision — here
  the parallel: a repair that must enumerate is a claim, and a claim needs a
  derivation, not a recollection.
