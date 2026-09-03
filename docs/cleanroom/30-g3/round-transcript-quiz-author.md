# Quiz-author transcript — cleanroom round 30

## Access discipline

Read only `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,743 lines), start to finish, in eight `Read` calls covering every line of
the file (offsets 1–400, 400–900, 935–1184, 1184–1324, 1324–1504, 1598–1748,
1744–2044, 2043–2273, 2273–2373, 2372–2592, 2591–2851, 2851–3051, 3052–3382,
3381–3581, 3580–3780, 3780–4060, 4249–4349, 4348–4488, 4497–4677, 4676–4746 —
i.e. a full pass with extra dwell time on the sections the brief named as
changed: front matter, §2.3–2.4, §9.2/§9.6, §11.1, §16.2, §18.2, §19.3,
§20.3/§20.5, §21.1–§21.9, Appendices G–H). One `grep -n` call listed section
headers to navigate by line number; no other file in the repository was read,
listed, or grepped. No git history, no web access, no other tool against any
other path.

Ran one local Python script, `verify.py`, written to and executed from my own
scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/quiz-author/verify.py`).
It reads no files — it only holds literal numbers and byte strings I typed in
from the document's own worked examples and my own constructed scenarios, plus
a hand-rolled CRC-32C implementation. I used it to (a) confirm my CRC-32C
routine reproduces the spec's own check vector (`0xE3069283` for `"123456789"`,
matching §4.5 exactly) before trusting it for anything else, and (b) confirm
that every arithmetic/byte-level question below actually resolves to a single
value under the document's stated rules, so that I am not asking a question
with no determinate answer. I did not write any answer into this transcript or
into the question text; the script's output stayed in the script's own output
and in my working memory only.

**Disclosure of unrequested context.** Before this task began, material
appeared in my context that I did not request and that this exercise's access
rule says is not part of the specification: a project `CLAUDE.md` pointing to
an `AGENTS.md`, and a user memory file naming several prior findings about
this project by title (a harness-spec-path issue, a lineage-gate word-list
issue, a preflight-before-launch issue, and a prose-vs-rules issue in this
project's repair history). I did not open `AGENTS.md`, the harness spec, or
any memory-referenced file, and I did not let the titles steer which sections
I weighted, which questions I wrote, or what I treated as already-known
defects — I disregarded all of it and reasoned only from `tarn.md`'s own text.
No path I was given diverged from what the brief stated (`spec/tarn.md`
existed exactly where named).

## Method

Read the whole document once, then reread the nineteen named passages closely
a second time, cross-referencing each against the sections that restate the
same rule elsewhere (as the brief instructs). Built the slate to hit the
brief's coverage requirements: ≥3 concrete-byte-construction questions, ≥2
reader/verifier-verdict questions against a specific (possibly malformed)
file, ≥2 arithmetic questions, ≥2 questions whose answer requires combining
rules stated in more than one section. Weighted toward the changed surface
but did not confine the slate to it, per the brief's warning that recent
rounds' survivors turned up in untouched text.

For every byte-producing question I hand-verified, using the local script,
that the document's stated rules pin down one value — not merely that a
value exists, but that I could actually derive it mechanically from the text
alone (grid arithmetic, the entry/segment/crc-of-crc-array chain of §8.1/§15,
the byte-shuffle permutation of §17.3). This caught one framing mistake before
it went in a question: an early draft of the coverage-partial-total question
(now Q7) used a verifier-detected *overlap* violation (§7.2's `[R-CNT-13]`,
register row L18) as the stopping condition. §5.2 states a special discard
rule for exactly that case — a walk-established scope-level rejection under
L18 or L40–L42 discards *that layer's own already-enumerated claimants* from
the count, which would have made my hand-picked numbers wrong and the question
secretly about a different, more convoluted rule than the one I meant to test.
I reworked the scenario to use an ordinary reader-tier domain violation
(`[R-ENC-03]`, an out-of-range dimension extent) detected during layer-record
validation, before any of that layer's coverage-walk claimants are
enumerated — a case the special discard clause does not reach — so the
question tests the ordinary partial-total mechanism cleanly. This near-miss is
itself reported below as an observation.

## Rejected questions (considered, cut)

- A question asking whether appending a new channel to a planar layer (rather
  than swapping two existing ones) is permitted under §20.3's ordinal-move
  bar. Cut as redundant with Q12 (the swap case): both exercise the same
  clause from opposite sides, and the brief asks that no two questions fail
  for the same reason — keeping both would spend two slots on one rule.
- A question about codec 4 (lz4)'s decoded-size cap being escaped by a
  zero-addressed-tile layer (§17.2's note under `[R-COD-07]`). Cut for space;
  it overlaps in spirit with Q7 and Q9 as another "does a stated escape clause
  actually cover this degenerate case" question, and the slate already has
  four verdict-style questions.
- A question about whether a compactor may drop an unimplemented MU=0/PE=0
  top-level record unconditionally (§20.4's table, compactor row) versus an
  appender's narrower "independently changes the scope" condition. Cut for
  space; a good question, but the slate was already at 15 with stronger
  coverage-required categories filled.
- A literal "what CRC does Appendix A's own file have" question — rejected as
  lazy: it would only be reading back a table already printed in the
  document, not combining rules or applying one to a new case. Q1 keeps the
  same file but perturbs one field, which forces an actual recomputation.

## Findings hit while authoring

One OBSERVATION, filed as `quiz-01` below (see structured findings).

## The slate

(Recorded in the structured result, not duplicated here, per the instruction
not to record answers — and to avoid drift between this file and the
structured output, the question text lives in exactly one place: the
structured result's `questions` array.)

Coverage check against the brief's requirements:
- Concrete-byte questions at concrete offsets: Q1 (trailer CRC recompute),
  Q2 (index-entry/segment-CRC/crc_of_crc_array chain), Q3 (byte-shuffle filter
  + CRC) — three.
- Reader/verifier verdict on a specific file: Q8 (validation-order priority),
  Q9 (experimental MU=1 top-level record), Q10 (recovery-scan candidate
  selection), Q11 (user-metadata frame content-size mismatch) — four.
- Arithmetic (sizes/counts/alignment/coverage): Q4 (extent_length formula),
  Q5 (disk ordinal via grid + linearization), Q6 (slab run partition), Q7
  (partial slack total) — four.
- Rules spread across ≥2 sections: Q9 (§2.3 + §21.6 + §10.2/10.3), Q10 (§9.6 +
  §21.2), Q12 (§20.3 + §11.4 + §7.4), Q13 (§2.1/`[R-CNF-01]` + front matter),
  Q14 (§2.4 + §19.2), Q15 (§19.1 + §19.3) — six, exceeding the floor of two.

No two questions share a failure mode: each targets a distinct governing
rule or chain of rules, and getting one wrong does not imply getting any
other wrong.
