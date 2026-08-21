# 0082. A compactor answers for the region it regenerates, on detection

- Status: Accepted (confirms ADR-0081's open item)
- Date: 2026-08-21
- Covers: §20.5's disposal of a structurally invalid index entry
- Supersedes: ADR-0080's compactor clause, as to that entry's disposal
- Confirm: none

## Context

ADR-0081 left one question open, and it is the second place where this
repository's decision trail and its specification had come apart.

**ADR-0080 decided one way.** A structurally invalid index entry "is now
reproduced with its offset and length exactly as they stand, there being no
live extent for a re-pointing to target (`[R-IDX-03]`), and the violation
travels with it (`[R-WRT-01]`)."

**Round 17 decided the other**, deleting that text verbatim and replacing it
with an obligation to refuse — and, like the rest of round 17, recording no
ADR. So an Accepted ADR and the normative text disagreed, again.

The repair audit attacked the reversal and found its **argument** faulty in
three independent ways, while leaving its **conclusion** standing:

- It glossed `[R-WRT-01]` at *region* granularity — the licence "reaches only
  a structure the commit neither modifies nor relies on, which a regenerated
  region is not" — where §20.3 step 2 glosses the same single rule at *entry*
  granularity, holding it "as true of an index entry copied to its
  disk-ordinal position as of a record re-emitted byte-identically". One rule,
  two incompatible reaches, and nothing in the document fixing which.
- It read §20.1 as making a compactor "answer for those in full", when
  §20.1's sentence carries in its own second clause the very carve-out the
  gloss omits.
- It stated the obligation unconditionally and then, three clauses later,
  conceded that "a compactor need not have looked" — an unconditional MUST
  beside a permission not to know, inside one parenthetical, and both at odds
  with §20.5's untouched "MUST NOT emit a file carrying a violation **it has
  detected**" thirty lines above.

It also broke the sentence it landed in: the refusal was spliced into a
semicolon list of what a regenerated region *contains*, orphaning the
segment-CRC item that followed it.

## Decision

**The conclusion stands; the argument is replaced.**

A compactor MUST refuse — but on the ground §20.5 already states, not on a
claim about `[R-WRT-01]`'s reach. Regenerating a region means classifying
every entry in it: a sentinel is re-emitted unchanged, every other entry is
re-pointed to where its stored extent now lies. An entry §15.3 classifies
reject-tile on a structural ground is neither, because `[R-IDX-03]` gives it
no stored extent for a re-pointing to target — so regenerating the region
cannot proceed without meeting it, and from that moment the violation is one
the compactor **has detected**. `[R-WRT-06]` then bites: the compactor can
neither reproduce the entry nor invent a replacement, and no drop is
available, a tile-index entry being no record §20.4's table licenses
dropping.

`[R-IDX-03]`'s no-stored-extent fact is ADR-0080's own insight, and it is
kept — but it now does the opposite work. ADR-0080 read it as *what to
reproduce*; it is better read as *how the compactor cannot avoid noticing*.

Two claims are deleted outright: that `[R-WRT-01]`'s licence "reaches only" a
structure neither modified nor relied on, and that §20.1 makes a compactor
answer for produced bytes "in full". Neither is in the cited text, and the
first contradicted §20.3 step 2. `[R-WRT-09]`'s depth is restated as what it
is — a bound on how far a compactor goes looking, not a discharge of what
regenerating the region has already put in front of it.

The disposal is lifted out of the parenthetical into its own paragraph, and
the list of what a regenerated region contains is restored to its four clean
items.

## Consequences

**The appender and the compactor now differ for a stated reason.** §20.3 step
2 has an appender carry a malformed entry forward byte-identically; §20.5 has
a compactor refuse. The asymmetry is real and the document already grounded
it: relocating a live index region "is compaction's operation (§20.5,
`[R-WRT-07]`), **not an appender's**" (§20.3 step 4), so the antecedent never
obtains for an appender. Resting the compactor's duty on detection rather
than on `[R-WRT-01]`'s scope keeps the two passages one rule with two actors
instead of two rules about one licence.

**The pattern this closes is worth naming.** Round 16 wrote §20.5's compactor
clauses; round 17 reversed them within a day; both changed normative text and
neither recorded an ADR against the other. Two ADRs in this session exist only
to reconcile decisions the spec had already made and the trail had not
recorded. The rule that would have prevented both is the one AGENTS.md already
states — an ADR before or with the text it authorises — and the cleanroom
protocol cannot enforce it, because every cleanroom agent reads the spec and
nothing else. The repair audit can, and now does.

## Precedent

- ADR-0080's `[R-IDX-03]` reasoning, retained and re-pointed.
- ADR-0081, whose open item this confirms, and whose finding that a
  default-to-REFUTED verifier pool returns a false zero is what kept this
  passage under examination at all.
- §20.3 step 4's actor split, which supplies the asymmetry's real ground.
