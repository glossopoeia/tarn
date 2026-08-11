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

Every AMBIGUITY and CONTRADICTION is a spec bug under ADR-0034, to be
fixed or explicitly deferred with a named owning section. None is
dispositioned yet — the raw findings are recorded here first so the
triage can be reviewed against them rather than replacing them.

Before fixing, the set needs deduplication: several findings are the same
defect seen from different roles (§9.6 vs §9.7 appears three times,
§17.4's dangling citation three times), and the `byte_level` flag is the
reporter's own judgement and is over-claimed in places — a finding about
which register row a verifier names does not change a byte any
implementation emits or accepts.

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
