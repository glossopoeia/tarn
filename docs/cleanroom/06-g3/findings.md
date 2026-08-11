# Cleanroom round 6 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Seven fresh-context roles plus an independently-keyed quiz, all against
`spec/tarn.md` alone. Every agent disclosed its access; none reported a
breach.

## Verdict

**G3 is not met.** The round found byte-level ambiguities and
contradictions, which is what G3 forbids outright.

| | |
|---|---|
| Quiz | **14 agree / 1 diverge / 0 underdetermined** |
| Findings | 85 — 19 CONTRADICTION, 35 AMBIGUITY, 31 OBSERVATION |
| Flagged byte-level by their reporter | 33 |

The quiz result and the findings count point in opposite directions, and
both are informative. Fifteen pointed byte-level questions, answered cold
by two agents working independently from the same text, produced one
divergence — and that divergence was adjudicated in the answer's favour,
against a key that had followed a non-normative Example over the
requirement it illustrates. On the questions asked, the document is
determinate.

The findings are concentrated somewhere else: in the seams between
sections, and overwhelmingly in text this project has added since
round 5. That text has never been read cold before, which is the whole
reason this round was weighted toward it.

## Why this round found so much more than rounds 4 and 5

Rounds 4 and 5 each found three byte-level defects and reported their two
constructive instruments empty. This round has seven roles rather than
four, two of them aimed at material that did not exist in round 5: the
figures, and the error register — which has since been rewritten three
times, twice by decisions that deleted rows.

Two findings deserve naming because they are the project's own recent
work, caught by the instruments built to catch exactly them:

**§9.6's generation-enumeration sentence.** *"Generation enumeration for
coverage verification (§5.2) is the same probe continued to offset 0."*
§9.7's Note says the opposite in as many words: *"Nothing here enumerates
prior commits."* The sentence is stale from before live-state coverage,
and three independent agents reported it. Verified.

**The §5.1 figure's `live state` brace.** It spans `dir₃ pad trail₃`.
§5.2 defines the live committed state as the front block plus every
structure the walk reaches plus the directory and trailer — so the brace
omits the front block and both layers, and wrongly includes the pad,
which is slack. Verified. The figure was added this session as a clarity
measure, with a stated design rule that symbolic regions cannot drift.
The regions did not drift; the *label* did, and the role invented to
audit figures is what found it.

**A dangling cross-reference.** §17.4 cites *"the rule of §9.7(d)"*.
§9.7 has no lettered clauses. Reported by three agents. Verified.

## Disposition

Three independent triage passes deduplicated the 85 findings and
re-judged each against a strict test: *does resolving it change which
byte sequences a conforming implementation may emit, or must accept or
reject?* Each pass covered every finding id; 84 of 85 were covered by all
three.

| | |
|---|---|
| Distinct defects | **67** (passes reached 68 / 67 / 66) |
| Consensus status | 55 CONFIRMED · 22 PARTIAL · 8 REFUTED |
| **Byte-level, unanimous** | **5 defects** |
| Byte-level with 2-of-3 support | 8 defects |

**The 33 self-flagged byte-level findings reduce to 5 unanimous.** The
over-claim has one dominant cause, and it is worth recording because it
will recur: a reporter finds a register row contradicting a rule and
concludes a verifier's verdict is open — when §21.1's *"where a row and
the rule it cites diverge, the rule governs"* has already decided it, and
only the table is wrong. Every surviving byte-level defect is a place
where **the rule itself is silent**: a namespace, a nesting depth, a
quantifier over channels, an ordering of two checks, a reader class with
an undetermined middle.

### The five

1. **§18.2 `[R-MTA-05]` does not say at what nesting depth the
   ascending-key sort binds.** The cleanest defect of the round: two
   conforming writers given identical content emit different bytes, and
   the rule's own stated purpose — *"This makes one writer's output
   reproducible for identical content"* — is achieved only under the
   recursive reading. Nesting is not hypothetical; §18.4 registers
   `tarn.stats` as *"object keyed by channel name, each value an
   object"*. Fix: three words.
2. **§4.6 `[R-ENC-15]` does not say whether dimension names and channel
   names share one namespace.** *"dimension names and channel names
   within their layer"* — a layer with a dimension `x` and a channel `x`
   is conforming under one reading and reject-layer under the other.
3. **§17.2 `[R-COD-07]`'s lz4 cap says "the tiles' decoded size" in the
   singular**, but §14.2/§14.3 give a planar layer one decoded size per
   channel, and `[R-SER-09]` guarantees a planar layer may mix types.
4. **§6.1 `[R-CNT-04]`'s local/remote reader test is economic, not
   structural**, so a memory mapping over a network filesystem satisfies
   both definitions and the MUST over bytes [0,16) has no determinate
   addressee.
5. **§21.5 row R1 registers experimental-range metadata encodings as
   violations**, where §21.6 states the opposite principle for the
   identical case — `[R-CNF-02]` makes conduct bind the actor and not the
   bytes.

Three more carried 2-of-3 support and want a decision either way:
`[R-COD-06]`'s *"declared window size"* against RFC 8878's two
derivations; the ordering of the layer-name uniqueness check against
ill-formed names; and `generation`'s 2⁶³−1 ceiling, asserted by §6.2's
table and enforced by no rule.

### Everything else

The remaining ~59 defects are real but not byte-level: stale sentences,
dangling cross-references, mislabelled figures, register bookkeeping, and
places where a diagnostic or a verdict label is undefined. Roughly 25 need
no decision about what the format means at all — a quarter of those are
figures and captions added in the same session as this round.

One correction to the round's own reporting, recorded because the error
was mine: I judged the §9.6/§9.7 generation-enumeration contradiction
byte-level before the triage ran. It is not. Prior generations' bytes are
slack, and `[R-CNT-21]` says no conformance requirement applies to them —
so a verifier that enumerated generations would find nothing it could
reject, and neither reading changes which files are accepted. The
contradiction is real and still wants fixing; it does not bear on G3.

The per-role transcripts carry the full text of every finding, including
the permitted readings each agent enumerated and which it picked.

## Artifacts

- [prompt.md](prompt.md) — charters, access rule, taxonomy, pass criteria
- `transcript-reader.md`, `transcript-writer.md`, `transcript-verifier.md`
  — the three implementer walks
- `transcript-diagrams.md` — the figure audit
- `transcript-register.md` — §21 against the rules it restates
- `transcript-adversary.md` — attacks tried, and which the text refutes
- `transcript-quiz.md`, `transcript-quiz-key.md`, `transcript-grade.md`
  — answers, the independently derived key, and the adjudication
