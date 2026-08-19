# Cleanroom round 12 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**One byte-level ambiguity: a commit that shrinks a dimension extent silently
breaks its own file.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings | 34 — reader 3, writer 8, verifier 3, diagrams 10, register 2, adversary 5, quiz 3 |
| Distinct defects | **24** |
| **Byte-level, after triage and hand-check** | **1** |

## Two harness failures, before any finding

**The register walk died and the harness said it had not.** The walk thunks
return `{role, result}`, and `filter(Boolean)` keeps that wrapper when `result`
is `null`, so `deadWalks` came back empty while the highest-value role had
produced nothing. Only the workflow's own failure line disclosed it. Nothing
was recoverable — 11 journal result rows for 12 agents, no `register-NN`
finding id anywhere, no transcript on disk — so the walk was re-run by resume
rather than the round reported as six walks when it had five.

That is the third distinct shape of this failure: a degenerate return (round
9), a dead agent (round 11), and now a **wrong detector**. The
`transcript_finding_count` guard cannot see this one, because nothing is
returned to compare. What sees it is reading the workflow's error report
before reading any result.

After the re-run all six walks agreed: claimed = returned = transcript.

## The survivor

Extents (8, 8) with tile extents (4, 4) give grid counts (2, 2). Shrink `E_x`
to 7 and `⌈7/4⌉` is still 2, so `entry_count`, the stored-tile set and the
index content are all unchanged and §20.3 step 4 forces no re-emission. But
column x = 7 is now a **padding** column, and `[R-SER-05]` fixes every padding
position's content to the channel's fill. Two untouched edge tiles become T4
violations, in a file a conforming appender just produced.

Fill was one of ten such changes — the same hole reaches a changed tile extent,
channel type, channel set, layout, linearization, codec and filter — and the
document answered only fill, and only from earlier the same day.

Two passes downgraded it by pointing at the shape-(c) treatment of the
analogous fill change. That text sits inside `> **Example — the three shapes a
commit takes.**`, and `[R-CNF-01]` makes non-normative *"any text labeled
Note, Example, or Rationale"*. **The nearest governing sentence carried no
force**, which is what left the case undetermined — and which also meant round
9's repair of this very example had been inert for three rounds.

Decided in [ADR-0074](../../decisions/0074-a-stored-tile-freezes-its-declarations.md):
a stored tile freezes the declarations it depends on. The alternative — permit
the change and oblige re-emission — was rejected because `[R-LIF-01]` freezes
committed bytes where they lie, so re-emitting a layer's tiles strands the
originals as slack, the whole layer's worth. An operation that reads like a
directory edit and leaves the file larger is a cost discovered rather than
chosen, which is the ground ADR-0068 already settled for layer deletion.

## The one four reporters flagged, downgraded

Four independently read §20.3 step 2 as forking between committing and
refusing when an appender meets a malformed index entry. Downgraded on text
none of them quoted — §20.1: *"**A creator** emits only conforming files
(`[R-CNF-05]`). An appender and a compactor satisfy every writer requirement
**for the bytes they produce**… certifying the whole file is a verifier's
office."* Every refuse-reading rests on `[R-CNF-05]` binding the appender.

The skeptic pass caught the real residue: the justification cited `[R-WRT-05]`,
which governs *"a record's header, inline payload, and extent slot"*, to
license carrying forward an **index entry**, which is not a record. Right
conclusion, wrong citation, and four readers tripped on it. Fixed: it now
grounds on §20.1 `[R-WRT-01]`, where the production test lives.

## Disposition

All 24 dispositioned: **21 fixed, 2 deferred, 1 escalated.**

Beyond the two above, nineteen repairs landed. The ones that mattered:

- **§20.4's summary still named only file-scope user metadata as undroppable**,
  where the rule and Appendix H say either scope — a propagation miss from
  round 11, which fixed Appendix H and not the summary beside the rule.
- **`[R-SLB-04]`'s trigger was narrower than its own scope clause**, so
  first-storing a sentinel tile and unstoring a run's first stored tile both
  changed a run without triggering the rule that governs runs.
- **`[R-CNT-13]`'s overlap enumeration had no branch** for two file-scope
  structures overlapping each other — decidable through F33, but not by the
  rule that enumerates the cases.
- **Nothing said a verifier decodes every stored tile**, though §21.4's codec
  rows are file-conformance violations detectable only by decoding.
- **§23.2 said a sentinel marks a tile "never stored"**, where §3.1 makes
  storedness per generation — an under-count in a privacy disclosure inventory.
- **Appendix G item 2's derived `file_id` named no hash**, no input
  serialization and no digest-to-u64 rule, and collided with `[R-WRT-06]`'s
  fresh-draw requirement; item 3 ordered no two records sharing an unassigned
  type. Both closed by the appendix's own method — pin the producer.
- **`[R-VEC-02]` now records a row's governing requirement identifier beside
  the row label**, since §2.2 promises stability only for the identifier and
  row labels renumber. The mechanical half of this shipped as COV-06 in
  ADR-0073; this is the document catching up with the tool.

**Deferred, with owners.** §7.4 has no worked byte example for a layer record
— the most intricate encoding in the format, against §4.7's promise that every
non-obvious encoding gets one; adding it is authoring, not editing. And
§21.1's instance criterion is applied in opposite directions to conditions of
the same shape (T3 against T14, F33 against F7), which moves the register
totals and the corpus.

**Escalated.** No verdict is fixed for a verifier meeting a conforming file
whose user-metadata encoding it does not implement. `[R-MTA-09]`'s
cannot-establish clause is expressly about the size bound; §17.4's is about
executing a codec, a position it says "arises only at a reserved or
experimental value", which for metadata encodings is not a violation.
`[R-CNF-11]`'s general criterion points at *cannot establish*; nothing states
it.

Register and corpus unchanged: **121 conditions over 248 instances, 300
vectors**.
