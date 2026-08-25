# 0101. §17.2's lz4 escape is stated by the addressed-tile count, and §11.1's growth Rationale goes to the ledger whole

- Status: Accepted (resolves the ADR-0099 audit)
- Date: 2026-08-25
- Covers: §17.2's `[R-COD-07]` Note; the disposition of the ADR-0099 audit
- Revises: nothing in normative text beyond §17.2's Note; ADR-0099's two
  re-keyed blocks are sent to the ledger rather than repaired a fourth time
- Confirm: Q-B8 records what this does not decide

## Context

Three auditors read ADR-0099's three hunks — the corrections against their
sources, downstream accounts, and cross-hunk — and returned **eleven findings**,
one self-flagged byte-level. Nine were verified under the per-auditor cap of 4;
three were left ungraded and all three were recovered rather than assumed.

**One verifier died mid-response.** Its transcript on disk shows it completed its
investigation — it wrote "I have what I need" and ran one last check — and then
never stated a verdict. Unlike round 25's verifier walk, whose findings were
recoverable verbatim, there was nothing here to recover but the reasoning, so the
finding was re-verified from scratch. **A dead agent is not lost work, and it is
also not a verdict.** The two the cap starved were verified in the same pass. All
three came back REFUTED, so neither the cap nor the death cost the audit
anything — which is knowable only because they were run.

**Every transcript matched its structured return exactly**, checked by
independent id-scrape: three, two and six findings against three, two and six.

## Decision

**§17.2's Note states the escape by the quantity that decides it.** Three
auditors independently found the same defect, in a passage no hunk touched: the
Note said "a later commit that grows an extent addresses tiles", which is false
whenever another dimension's extent stays 0. `[R-GEO-01]` gives Tᵢ ≥ 1 and
`[R-GEO-02]` makes Eᵢ = 0 valid, so Gᵢ = 0 exactly when Eᵢ = 0 and N = ∏ Gᵢ stays
0 while any extent does. A rank-3 layer at E = (0, 100, 0) whose E₀ grows to
100,000 still addresses no tile, and `[R-COD-07]`'s cap — quantified over
*addressed* tiles — is still vacuously satisfied.

The Note now reads: the escape ends exactly when the layer's addressed-tile count
rises above 0, which takes every dimension's extent nonzero, and a growth leaving
any extent at 0 holds the count at 0 and the escape with it. That is ADR-0095's
rule applied — the partition is stated by a property, needs no exception, and
carries no count. **The word "last" is deliberately not used**, for the reason
the same audit established below.

A sweep found the false claim in exactly **one** place. §20.3's growth permission
already states the correct test normatively — "a growth is permitted exactly
where the geometry it produces satisfies every rule that geometry is subject to
… which an empty layer escapes only because that cap is quantified over addressed
tiles" — and `[R-COD-07]` and row L44 both carry the right quantifier. Only the
Note overreached.

**§11.1's Rationale and §13.3's Note go to the ledger as Q-B8, not to a fourth
repair.** Seven of the eleven findings landed in those two blocks. Two are real:

- `entry_count` is ∏ Gᵢ, a **product**, while `[R-GEO-06]` computes each disk
  ordinal from the **individual** grid counts. A product does not determine its
  factors, and §20.3 permits one commit to grow and shrink together. At
  T = (1, 1), E = (2, 3) with a tile stored at (1, 0), growing E₀ 2→3 and
  shrinking E₁ 3→2 holds `entry_count` at 6 while that tile's ordinal moves
  3 → 2: index content changes, `entry_count` does not, and §20.3 step 4 requires
  re-emission — which §11.1 now denies in terms. The wording ADR-0099 replaced in
  §13.3 **did** reach that case, so that half is a regression. The verifier's
  words: "I tried hard to kill this and could not."
- The trailing clause's "**last** zero grid count" needs the depletion sense. A
  census of the document's sixteen bare uses of *last* finds thirteen meaning
  *final member of an ordered sequence*, two meaning *most recent committed
  state*, and none in the depletion sense — while the clause attaches to an
  i-indexed sequence named in the same sentence.

This is the third consecutive cycle rewriting those blocks, and ADR-0099's own
Consequences named the right model — §5.1's "stored-tile set or index content",
the formulation §20.3 states normatively — and then did not use it. §21.7 took
four repairs before Q-I5; §21.2 drew findings in three rounds before Q-H6. **A
fourth patch is what has already failed three times**, so Q-B8 asks whether
either block needs to state the rule at all, with three options priced.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. The
propagation checker reports no unswept restatement, and no acknowledgement was
needed.

**Zero byte-level, and the zero was tested rather than accepted.** The one
self-flagged byte-level finding was downgraded by a verifier instructed to
default to REFUTED — the shape ADR-0081 records as never standing on its own — so
two refuters attacked the downgrade from different lenses, one asking whether
`[R-CNF-01]` really settles it and one asking whether any rule *designates* the
Note authoritative as §2.3 once did for §21.6's paragraph. **Both upheld the
downgrade**, the second after a sweep finding the document's designation idiom
invariably elevates defining text and demotes restatements. Both nonetheless
found the defect real as text, which is why it is repaired here.

**The refute phase earned its keep on a different finding.** The "last" ambiguity
was reported by all three auditors and refuted three times on a shared premise —
that bare *last* is not this document's positional word. A refuter tested that
premise by census and falsified it thirteen to zero. Three internally sound
readings, one shared framing, overturned by attacking the framing: the round-16
shape, and the reason the phase is standing.

**On the audit's own inputs.** ADR-0099 recorded a hunk builder that mislabelled
two of four headers because its location map was keyed by index against hunks git
had ordered by line number. This cycle's headers were derived from each hunk's
own target line by scanning the current file backward for the nearest heading, so
the class is closed by construction rather than by an auditor catching it. No
auditor reported a mismatch, and each was asked to.

**A fourth contamination channel, disclosed.** The cross-hunk auditor reported a
git-status block carrying recent commit subject lines, one of which named this
commit's own intent — the section, the key quantity and the repaired rule. It
said so unprompted, said it could have seeded its grouping, and stated that it
had reconstructed the grouping from the diffs first. Nothing a charter writes can
suppress that channel; only the disclosure field surfaces it.

## Precedent

- ADR-0095's rule that a partition stated by a property beats a list, applied to
  §17.2's Note here and offered to §11.1 as Q-B8's option (b).
- ADR-0096's disposal of §21.7 to Q-I5 and ADR-0098's of §21.2 to Q-H6, whose bar
  §11.1's Rationale has now met.
- ADR-0081's finding that a verifier pool told how to default shares a premise,
  which is why a zero is the trigger for the refute phase rather than a result.
