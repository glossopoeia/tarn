# 0114. The sample-type bar is withdrawn: the §14 bar already tests it, and tests it better

- Status: Accepted (supersedes ADR-0113 in part; resolves Q-B6's sample-type limb) — Superseded by ADR-0124, which withdraws the §14 bar and its gloss for a closed list of permitted changes
- Date: 2026-09-02
- Covers: §20.3 step 4's §14 bar and the withdrawn sample-type bar; §11.1's
  Rationale; §21.7's witness account
- Supersedes: ADR-0113's sample-type bar and its layer-scope decision. ADR-0113's
  disk-ordinal bar stands unchanged.
- Confirm: none

## Context

ADR-0113 added two bars to §20.3 step 4. The second, on a planar layer's disk
ordinals, closed a byte-level fork and stands. The first barred a change to a
channel's declared sample type on any layer storing a tile, and this decision
withdraws it.

**It was built on a misreading of the rule it sat beside.** ADR-0113's premise
was that the §14 bar reaches a type change only where the change moves something
structural — a decoded size, a sample offset, a padding position — so that
`int8` → `uint8` slipped through. The §14 bar says otherwise in its own gloss:

> The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: **a change that leaves every one of
> those tiles' stored bytes meaning exactly what they meant** … is not what this
> bars.

The test is the effect on the tile, and the enumeration is illustrative. A byte
that meant −128 as `int8` means 128 as `uint8`, so the change does not leave the
stored bytes meaning what they meant and **the §14 bar already barred it.** The
enumeration was read as the test, by the drafter of ADR-0113 and then four times
over in successive repairs, which is the whole reason that decision's motivating
paragraph produced a defect in every draft it went through.

**And the quantifier was already right.** The §14 bar ranges over "any tile that
layer stores **in the generation this commit supersedes**", so it reaches a
channel whose tiles are stored and does not reach one whose tiles are not. That
is the maintainer's position, already normative before ADR-0113 touched the
passage.

## Decision

**The sample-type bar is withdrawn.** §20.3 step 4 states two bars, not three:
the §14 bar and the disk-ordinal bar.

**The §14 bar's gloss gains the type case concretely**, because the misreading
that produced ADR-0113 is available to any reader. A channel's declared sample
type is such a declaration; changing it is such a change **wherever the layer
stores a tile that carries that channel**; and where the superseded generation stored
no such tile there is nothing to reinterpret and the bar reaches nothing.

**That phrasing settles the layout question without splitting the rule**, which
is why it is preferred to ADR-0113's layer scope. An interleaved tile carries
every channel, so a layer storing any tile has every channel's type pinned — the
result ADR-0113 reached by fixing the scope to the layer. A planar tile carries
one channel, so only a channel with stored tiles is pinned. One clause, the
document's own word for the relation (§3.2, `[R-SER-01]`, `[R-SER-05]` all say a
tile *carries* a channel), and no layout branch.

**The test is on the declared types, not on the values a tile holds**, and the
document now says so. This is the maintainer's substantive point and it is what
makes the rule usable: a per-value test would permit `int8` → `uint8` on a tile
whose bytes happen to lie in [0, 127] and bar it on the tile beside it, so the
same declaration change would be legal in one file and not another and an updater
could decide only by inspecting every stored byte. `0x80` denotes −128 as `int8`
and 128 as `uint8` whether or not any tile stores that byte.

## Consequences

**ADR-0113's layer-scope decision is reversed, and the reasoning that supported
it does not survive contact with the withdrawal.** That decision preferred one
answer for a caller — a type change means writing the tiles — over a rule that
behaved two ways. But the split it was avoiding is not a split in the rule: it is
the difference between a tile that carries the channel and one that does not,
which is the same predicate the §14 bar applies to every other declaration
change. A caller still has one concept, and it is the concept the format already
used.

**What is lost.** Nothing normative: every file the withdrawn bar excluded that
the §14 bar does not is a file in which no stored tile carries the re-typed
channel, and reading such a file returns the same values before and after. What
goes with it is a rewrite the format did not need to require.

**The register does not move**: 120 conditions, 275 instances, 329 vectors,
Appendix A byte-identical. Neither bar was ever witnessed and §21.7's account is
adjusted rather than re-derived.

**Four passages that counted the bars are swept**: §11.1's Rationale twice, the
re-declaration permission's tense anaphor, the shrink paragraph's exclusion, and
§21.7's witness sentence. A count in prose is a closed claim, and withdrawing one
member of three falsifies every statement of the number.

**Q-B10 is unaffected and stays open.** Whether a commit may remove a channel
whose tiles the superseded generation stored turns on the de-addressing
carve-out's scope, not on the type rule, and the maintainer's direction is to
guard it separately rather than fold it into this sentence.

## Alternatives rejected

- **Narrow the sample-type bar to stored channels** rather than withdraw it.
  Reaches the same outcome and keeps a rule that is redundant with the §14 bar
  wherever it bites, together with the motivating paragraph that produced a
  defect in each of its four drafts.
- **Keep ADR-0113's uniform layer scope.** Bars two operations that change no
  value a reader can extract, and leaves the redundancy with the §14 bar's own
  test unaddressed and unstated.
- **State the test as the range of possible values.** The maintainer's
  formulation, and the substance is adopted. "Denotes" is used instead because
  the mapping from bit pattern to value is what decides it; the two coincide for
  every pair in §12.1's list, and the mapping degrades gracefully if a future
  major ever assigns two types sharing a range.

## Precedent

- ADR-0106's rule that a sentence false more than once is deleted rather than
  repaired again, applied here to a whole rule rather than a sentence.
- ADR-0081's reading of §20.3 step 4: a declaration change that would reinterpret
  stored bytes is not an appender's operation. The §14 bar was always that rule;
  ADR-0113 duplicated it without recognising it.
