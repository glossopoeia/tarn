# Cleanroom round 19 — findings

Protocol: ADR-0034, four phases, preceded by **three** repair-audit passes over
the surface it reads. Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level ambiguity. G3 is not met.** For the second round running the
survivor is in text no recent round touched — and it is not the finding the
round's own reporters flagged.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — thirteenth round running, and no normalization needed |
| Findings | 44 — the most since round 6 |
| Self-flagged byte-level | **1** (and it is *not* the survivor) |
| Distinct defects | **28** — 2 graded byte-level by some pass, 8 design-decision, 5 register-bookkeeping, 13 editorial |
| **Byte-level after triage and the refute phase** | **1** |
| Harness | **not clean — see below** |

Byte-level history: 5 → 4 → 4 → 3 → 3 → 5 → 0 → 2 → 0 → 1 → 1 → 1 → 0 → 1 →
1 → 1 → 1 → 1 → **1**.

## Harness: one triage pass died twice, and was recovered from disk

`[triage:correctness]` failed on its first run with a server error mid-response,
and again on resume with a safeguards refusal. **Its transcript was on disk and
complete both times** — 32 KB, 26 groups, with an explicit "THE CLOSE CALL"
section — so its work was recovered by hand rather than lost. This is the
failure shape the harness notes warn about: *diff every transcript against its
structured return.* Two passes returned structurally; the third was read.

**An access-rule breach was disclosed by the refute agent**, and it is a
harness defect rather than an agent's: the runtime injected the project
CLAUDE.md pointer and a summary index of the maintainer's auto-memory into its
context, whose lines mention the round's own position and the
"lowercase-vs-ALLCAPS discriminator". The agent disclosed it unprompted, said
it opened none of the named files, and its argument rests on quoted spec text
about scope rather than casing — but a disclosed breach is usable only because
it was disclosed, and **this leak is not specific to this round.** It should be
assumed to have been present in earlier ones.

## The survivor: §21.6 states a file-wide refusal where `[R-CNT-18]` confines it to a layer

§21.6's closing paragraph names, without any placement qualifier, "an
**experimental-range record type carrying MU = 1**" as a conforming file a
reader nevertheless refuses, attributing the obligation to `[R-CNT-15]` — which
governs **top-level records only**: "An unknown record type at file scope:
MU = 1 → reject-file."

For a layer sub-record the governing rule is `[R-CNT-18]`: "an unknown
sub-record type with MU = 1 is **reject-layer — never reject-file**." §10.3
keeps the two apart in as many words, and §20.4's table does too.

This matters because **§2.3 designates §21.6's paragraph as the authority**:
`[R-CNF-03]` relieves the MUST-accept and adds "§21.6's closing paragraph names
the other two". So a conforming file with layers X and Y, where Y carries a
sub-record of experimental type 0x8001 with MU = 1, is **refused whole** by a
reader following §21.6 and **rejected at layer scope only** by a reader
following `[R-CNT-18]`, §10.3 and §20.4. Two conforming readers, one conforming
file, opposite verdicts.

**Its own reporter graded it not byte-level**, on the ground that
`[R-CNT-18]`'s "never reject-file" carries no BCP 14 keyword and so "has no
force of its own". One triage pass upheld it as byte-level, one did not; the
refute phase attacked the split and returned **DOWNGRADE_REFUTED**.

## The two findings turn on one question, and it is not the one the charter asked

The round's *self-flagged* byte-level finding — that `[R-WRT-07]`'s
tile-preservation clause carries no capitalized keyword — was downgraded by
two passes and the refute phase let the downgrade stand. But the recovered
correctness pass answered the underlying question directly, and against this
charter's own discriminator:

> §2.1 governs how the listed **key words** are read, not whether a
> keyword-free normative declarative binds. `[R-CNT-13]` states a rule with no
> keyword, and §21.7 calls that very sentence "`[R-CNT-13]`'s **prohibition**".
> `[R-CNT-02]`, `[R-SER-01]` and `[R-SER-02]` are the same construction.

So **this document's own practice is that keyword-free normative declaratives
bind.** The charter told reporters that "a clause with no keyword at all has no
force of its own" — that instruction was wrong, and it is the premise the
survivor's reporter used to *under*-grade the survivor. The discriminator
introduced after round 18 needs narrowing to what it actually established: a
lowercase *keyword* does not carry BCP 14 force, which is not the same claim.

## Disposition

The survivor needs a maintainer decision — whether §21.6's paragraph gains the
placement qualifier `[R-CNT-18]` requires, or `[R-CNT-18]`'s "never
reject-file" is raised to a keyword — and the `[R-WRT-07]` preservation clause
needs a MUST on the same occasion. Recorded and pending; **no repair was made
this session**, so round 20 would read an unchanged surface.

Register and corpus unchanged: 121 conditions over 273 instances, 327 vectors.
The quiz author reproduced §21.8's totals mechanically (36/58, 49/116, 26/55,
10/44) and every published checksum constant before authoring.
