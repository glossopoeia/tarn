# Cleanroom round 22 — findings

Protocol: ADR-0034, four phases, preceded by the audit in
[repair-audit.md](repair-audit.md). Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level ambiguity, and it is in ADR-0086 — the fix written this cycle
for round 21's unanimous finding.** G3 is not met.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — sixteenth round running (all 12 raw "divergences" were the answerer's `; ` against the keyer's double space; every value identical) |
| Findings | 20 |
| **Self-flagged byte-level** | **5** — the most since round 17 |
| Distinct defects | **10** — 1 byte-level, 1 design-decision, 3 register-bookkeeping, 4 editorial, 1 figure |
| **Byte-level after triage and the refute phase** | **1** |
| Harness | clean: 13/13, 0 errors, every `transcript_finding_count` matching, all three passes echoing all 20 ids with no gap, duplicate or extra |

Byte-level history: … → 1 → 1 → 1 → 1 → 2 → **1**.

## Six reporters, independently

**Every implementer walk found it, plus the register hunter and the quiz
author** — reader, writer, verifier, register, adversary, quiz. That is the
widest independent convergence on a single defect in this project's history;
the previous best was four. Two of three triage passes upheld it byte-level,
the skeptic did not, and the refute phase attacked the split and returned
DOWNGRADE_REFUTED.

## The survivor: ADR-0086's own sentence carries two quantifiers

The sentence added last commit reads that the last three rows "range over the
tiles, user-metadata documents and compressed frames a file **actually
contains**", glossed "exactly as `[R-COD-07]`'s cap is quantified over a
layer's ***addressed*** tiles".

Those are not the same quantifier, and for the tile row the two halves point
opposite ways:

- **Reading A — addressed tiles.** The gloss says so outright. A layer that
  addresses tiles has tiles whose decoded size the row bounds, stored or not.
  Corroborated by `[R-ERR-04]`'s "narrowest scope whose **declarations** exceed
  what it can serve" and by `[R-SER-07]`, "decoded size is a function of the
  layer's declarations alone … never of payload content".
- **Reading B — stored tiles.** The governing verb is "a file actually
  contains", and for the *other two* rows the same sentence covers — documents
  and frames — "contains" can only mean physically present, since neither
  exists except as stored bytes.

**One sentence supplies the quantifier for three rows whose instances are
individuated differently.** A tile can be addressed without being stored (its
index entry is the sentinel); a document or a frame cannot.

## The honest reading

ADR-0086 fixed a quantifier defect and introduced a quantifier defect, in the
sentence written to settle quantifiers. The maintainer's own explainer used
"contains" while the precedent it cited used "addressed", and neither the
maintainer's pass nor the pre-round audit — which ran **check 6 specifically to
catch what a repair leaves open** — noticed that the word had changed between
the claim and its warrant.

Check 6 asks what quantities a structure carries that no rule fixes. It does
not ask whether the repair's own governing verb matches the verb of the rule it
cites as precedent. That is a seventh check, and it is cheap: **when a repair
justifies itself by analogy, quote both rules and compare their quantifiers
word for word.**

## Disposition

The survivor needs a maintainer decision — whether the tile row is quantified
over *addressed* or over *stored* tiles — and the sentence then needs the other
two rows separated from it, since "contains" is right for them and is the wrong
word for whichever the tile answer is.

Register and corpus unchanged at 121 conditions over 273 instances. **The
instance debt recorded in the pre-round audit is still open** and is unrelated
to this finding.
