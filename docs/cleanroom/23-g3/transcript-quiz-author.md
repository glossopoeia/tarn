# Round 23 — quiz author working transcript

**No answers are recorded in this file.** I am the author only.

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,426 lines, read end to end in six `Read` calls). No `docs/`, no `PLAN.md`,
no `conformance/`, no `spec/registry.json`, no git history, no web.

Two `awk` invocations against that same file (counting semicolon-separated
Instances cells in the §21.2–§21.5 register tables). One Python snippet that
reads no files, used only to confirm my CRC-32C implementation reproduces the
spec's *own published* check values — `CRC-32C("123456789") = 0xE3069283`,
§7.4's `0x80A34955` over 80 sentinel bytes, and §15.4's `0xEECB3BB2` over a
full all-sentinel segment. All three matched, which is what told me the
CRC-shaped questions below are well posed. I did not compute any quiz answer
and none appears here.

Context I did not ask for appeared before I began — a project instruction file
pointer and an index of maintainer memory notes naming this project. I treated
none of it as evidence and none of it shaped a question. Disclosed in the
structured result.

## How I read the document

Straight through, once, cold, then a second pass over the five passages the
brief flagged (§18.2, §21.5, §21.7, §21.8, §21.9) plus §14/§15/§16/§9.7, which
is where I ended up building files.

Working notes I kept while reading:

- §18.2 is the passage where the newest text is doing the most work. Its
  spine is: encoding 2 inherits **every** `[R-COD-06]` frame constraint *save
  two* — the tile-decoded-size comparison and the declared `Window_Size` — and
  then replaces both. The replacement for the first is *the decoded document's
  byte length*; the replacement for the second is *the reader's own bound, no
  smaller than §21.9's 8 MiB row*, which is explicitly **not a violation**.
  Three questions come out of that split and they fail independently.
- §21.5's preamble draws a line I expect implementers to get wrong: encoding
  `0x00` and the reserved range `0x03–0x7F` are **violations** (R1); the
  experimental range `≥ 0x80` is a §21.6 **non-violation**. `[R-MTA-10]`
  withdraws the *document's content rules*, never the encoding byte's own
  value set.
- §21.9's individuation paragraph is a pure quantifier passage: three rows are
  per-instance, the tile row ranges over *addressed* tiles, and a layer that
  addresses none has no instance. That composes with `[R-COD-07]`'s note (the
  lz4 cap is quantified the same way) and with `[R-ERR-04]`'s "declines **on
  that ground**" clause to decide whether a specific degenerate file must be
  accepted. That is a legal-but-degenerate file worth building.
- §21.7 names, per class, which register row witnesses a §20.3-step-4
  declaration change. The codec-change clause ends "**or by T14 where the new
  declaration is codec 1**", which is a single determinate row label.
- §21.8's "121 conditions over 277 instances" is a stated total. I counted it.

## Arithmetic I checked before writing questions

Register shape (by `awk` over the four tables, then hand-verified for §21.2
and §21.5):

| table | rows | instances |
|---|---|---|
| §21.2 F | 36 | 58 |
| §21.3 L | 49 | 116 |
| §21.4 T | 26 | 55 |
| §21.5 R | 10 | 48 |
| total | **121** | **277** |

§21.8's stated pair is correct. §21.1's counting rules make this mechanical:
semicolons separate instances, a cell reading `—` is one instance, a range
stated without the condition changing shape is one instance (T24's *any
codec*). I used that as the basis for one question and report the cost of
checking it as an OBSERVATION.

Other arithmetic I worked before committing to a question, so that each has a
single value: `[R-CNT-17]`'s `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`;
§7.4's inline-payload field widths (cross-checked against the §7.4 worked
example's own 4 + 34 + 18 + 12 + 13 = 81); §11.2's grid counts and the planar
`C·N` addressed-tile count; §11.4's in-tile and disk ordinals; §14.2's
`(k div C)·Q + F_{k mod C}`; §14.3's `⌈P/8⌉` packing with `[R-SER-05]`'s pad
bits; §9.7's claimant list.

## The slate, and why each earns its place

Weighting: **7 of 15** land on the five flagged passages (Q01–Q07); the other
eight are the end-to-end build, spread so that no two fail together.

| # | Sections combined | Shape | Category |
|---|---|---|---|
| Q01 | §18.2 + §21.5 R4 + §21.1 | encoding-2 content-size mismatch → row, outcome, verdict | verdict |
| Q02 | §18.2 + §21.9 + `[R-CNF-03]` | single-segment frame, doc under the 16 MiB row but window over the 8 MiB row | verdict / limits |
| Q03 | §18.2 + §2.3 + §21.2 | verifier that declines *and* establishes one violation | verdict |
| Q04 | §21.5 + §21.6 + §10.2 | encoding `0x00` / `0x7F` / `0x80`, three files | verdict |
| Q05 | §21.8 + §21.1 | instance count of R4 and of §21.5 | arithmetic |
| Q06 | §21.9 + §11.2 + `[R-COD-07]` note + `[R-ERR-04]` | zero-extent layer, lz4, 2 GiB derived tile | verdict / limits |
| Q07 | §21.7 + §21.4 + §20.3 step 4 | codec 3 → codec 1 on a layer with prior-generation stored tiles | ordering / row |
| Q08 | §14.3 + §14.5 + §11.3 + §17.3 + `[R-COD-04]` | packed bool plane with padding positions *and* pad bits | concrete bytes |
| Q09 | §14.2 + §14.5 + §12.1 | interleaved mixed-type padding sample, offset + bytes | concrete bytes |
| Q10 | §15.1 + §15.4 + `[R-IDX-05]` + §4.5 + `[R-CNT-17]` | two full all-sentinel segments | concrete bytes + arithmetic |
| Q11 | §6.2 + §9.5 + §19.1 + §21.2 | residue past a completed commit | verdict |
| Q12 | §15.3 + §16.2 | run continuity across a structural reject-tile vs a crc-failing entry | arithmetic |
| Q13 | §9.7 + §5.2 + §15.3 | coverage walk: slack total, and whether partial | arithmetic |
| Q14 | §7.4 + §11.2 + `[R-CNT-17]` | inline_length and extent_length of one layer record | arithmetic |
| Q15 | §19.1 step 4 + §4.6 + §21.2 | two byte-identical *and* ill-formed layer names | verdict |

Charter coverage: concrete bytes at concrete offsets — Q08, Q09, Q10 (and Q09
asks for an offset explicitly). Reader/verifier verdicts on a malformed file —
Q01, Q03, Q04, Q11, Q15. Arithmetic — Q05, Q10, Q12, Q13, Q14. Rules spread
across more than one section — Q02, Q06, Q07, Q08, Q13, Q15 all require at
least two.

Independence check: no two questions turn on the same sentence. Q01 turns on
the content-size replacement, Q02 on the window replacement, Q03 on the
verifier-decline clause and §2.3's priority rule, Q04 on the value set — four
different mechanisms inside §18.2/§21.5. Q06 and Q02 both touch §21.9 but on
different rows and opposite directions (within-guarantee vs exceeds-guarantee).

## What I rejected, and why

- **"How many bytes is the smallest conforming file?"** — Appendix A answers
  it in one cell. Lazy.
- **Reproducing §7.4's worked layer-record payload.** The document already
  prints the byte listing; the answerer would transcribe, not derive. Q14
  instead uses a different rank/layout/channel set so the field widths must be
  applied rather than copied, and cross-checks against the planar
  addressed-tile count.
- **Asking for §7.4's `0x80A34955` / `0xC4EE982E`.** Printed in the document.
  Q10 uses two *full* segments instead, so the answerer must reach
  `[R-IDX-05]`'s constant, place two little-endian copies, and check one CRC
  over the resulting array.
- **A trailer-CRC question.** I drafted one (a fully specified 60-byte trailer,
  asking for the four stored CRC bytes) and cut it: Appendix A already prints
  a worked trailer, so the exercise reduces to "run CRC-32C over bytes you were
  handed", which tests a library and not this document. Q10 keeps one CRC in
  the slate but makes the *input bytes* the thing that has to be derived.
- **"Which §21.2 row does this file exercise?" for the 200-byte residue file**
  — as first drafted the file exercises both F8 and F17, and §24 explicitly
  contemplates a file exercising several rows. I rewrote Q11 to ask for the
  row of the **first** check §6.2's ordered validation fails, which §6.2 and
  §9.5's note together determine.
- **Same defect in Q15's first draft** (a file with two byte-identical
  ill-formed layer names exercises F4 *and* L3). Rewritten to ask which
  violation §19.1 requires be decided *first*, which §19.1 step 4 states in
  terms.
- **A question on whether §21.9 bounds a user-metadata record's *stored*
  extent length.** I convinced myself this is not indeterminate: no §21.9 row
  covers it, so it exceeds no guarantee, `[R-CNF-03]`'s acceptance duty runs,
  and the CRC over it is streamable at O(1) memory — so nothing forks. Not
  asked, not reported.
- **A question built on §21.7's "witnessed only where …" sentence.** I believe
  that sentence is defective (see findings), so I will not build a question on
  it. Q07 uses the *clause* of that sentence that is determinate — the codec-1
  witness — and does not depend on the "only" claim.
- **Instance count of §21.3 (116).** Determinate but 49 rows of semicolon
  counting invites an arithmetic slip rather than a reading difference, which
  would indict nobody usefully. Q05 uses §21.5's ten rows plus R4's sixteen,
  where a miscount is a genuine reading disagreement about R4's shape.

## Findings raised while authoring

1. `quiz-01` — §21.7's "witnessed **only where** the affected tiles remain
   stored *and* the change reaches a byte §14 structurally constrains" is
   falsified by the two clauses that follow it in the same sentence, which
   name T3/T14 for a decoded-size change and T15/T17/T23/T25/T14 for a codec
   change. Neither of those is "a byte §14 structurally constrains". Reported
   as CONTRADICTION, **not** byte-level: §21.7 is an account of coverage and
   imposes no obligation; the rows and their governing rules fix every verdict
   either way, and §21.1 already says the rule governs where a row diverges.
2. `quiz-02` — OBSERVATION on §21.8's "121 conditions over 277 instances":
   decidable, and I decided it (it is correct), but only by mechanically
   counting semicolons across 121 Instances cells under §21.1's counting
   rules. Disproportionately expensive for a reader, and silently wrong for
   any reader who does not notice that a `—` cell counts as one.
3. `quiz-03` — AMBIGUITY on §21.9's "The first five rows range over
   declarations, which every file and every layer carries", set against a
   conforming file with zero layers (`[R-CNT-14]`, §21.6). Low severity, and
   I picked the vacuous reading; recorded because the paragraph is one of the
   five and its whole subject is what each row ranges over.
