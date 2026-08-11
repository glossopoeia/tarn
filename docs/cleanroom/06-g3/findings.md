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

### The five — all resolved by ADR-0058

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

All five are now fixed (ADR-0058), each by a clause rather than a
redesign. Three more carried 2-of-3 support and were taken at the same
time:
the ordering of the layer-name uniqueness check against ill-formed names
(uniqueness first, over raw bytes) and `generation`'s 2⁶³−1 ceiling (now
in `[R-CNT-06]`'s gate list). The third — `[R-COD-06]`'s *"declared
window size"* — turned out to need no decision: RFC 8878's two
derivations agree on every tile, so it took a Note rather than a rule.
Two of three passes over-called it byte-level.

### Everything else — 49 of 56 cleared

The editorial tail deduplicated to **56 defects**, 37 of them agreed by
all three triage passes. Fifty-four edits landed: stale sentences,
dangling cross-references, figure labels that contradicted their own
section, register rows that restated their rule too broadly, and four
places where a verdict or a diagnostic had no name.

Three of the four §21 edits move instance counts — one row gains the
`generation` upper bound, one gains the trailing-residue instance its
layer-scope twin already carried, and one loses two instances that no
file can exhibit at certification because the bounds rows catch them at
open. They net to zero, so the register stands at **125 conditions over
242 named instances** and the corpus's 125/125 row coverage is
unchanged.

**Seven remain open, none of them editorial after all:**

- Three were declined on the merits — a drafter read the text and found
  no defect. The clearest is the claim that the endianness row's
  `generation` instance is unconstructible: a `generation` of 128 stored
  big-endian reads back as 2⁶³, which `[R-CNT-06]`'s gate now rejects,
  so the instance is exactly what that row describes.
- Four were design decisions wearing editorial clothes: whether metadata
  encoding 2 is core; whether a reject-layer outcome is prospective or
  retroactive; whether an appender may drop a record of a type it *does*
  implement; and whether a verifier may stop at the first violation.
  Each changes what an implementation must do, so each took an ADR
  rather than a redraft — **ADRs 0059, 0060, 0061 and 0062**, now all
  Accepted and propagated into §2.3, §18.2 and §20.4.

That the drafting agents refused four edits on exactly this ground is
the useful result. The instruction was *if this would change what a file
may contain or what a reader must reject, stop* — and the boundary held
where it mattered.

Three of the four turned out to be settled by rules already in force,
and only needed saying: PE governs a record's survival whether or not
an updater implements the type (`[R-CNT-22]` had already made the
registry authoritative), a layer rejection is prospective because
`[R-RDR-03]` validates the whole layer record before the first access,
and metadata encoding 2 costs a reader nothing because `[R-COD-11]`
already obliges it to carry a zstd decoder for codec 3. Only the
verifier's reporting obligation was genuinely open.

One of them was also already in the text. §2.4's prospective clause
landed in the editorial pass of `d29d9d7`, drafted by that section's
owner while a second agent escalated the identical finding. Both were
right, and the sequence is the defect: normative text reached `main` one
commit ahead of the ADR authorizing it. ADR-0060 ratifies rather than
introduces, and records the inversion.

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
