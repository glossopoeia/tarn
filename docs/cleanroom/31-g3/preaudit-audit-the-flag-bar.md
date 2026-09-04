# Audit transcript — lane "the-flag-bar" — hunks 02, 15, 17, 22

## Disclosure

Read: the four hunk files under r31-audit/case/ (hunk-02.diff, hunk-15.diff,
hunk-17.diff, hunk-22.diff) and spec/tarn.md via `sed -n` ranges and `grep -n`
(ranges listed below). Wrote: this file only. Nothing written to the scratch
directory. Did not open docs/, conformance/, registry.json, git history,
full.diff, or any other hunk file; did not list the case directory.

Unasked-for context present at start: a project-instruction pointer
(CLAUDE.md -> AGENTS.md, not followed), an auto-memory index naming four
note titles, and an environment block whose recent-commit subjects name a
round number and an ADR number. None was used as evidence; the round/ADR
names told me nothing about these hunks and I did not open the notes.

## Hunk headers vs bodies

- hunk-02: header says lines 885-892, heading §6.3 (line 856). Current file
  line 885 = "flags = 0, and sets no other (§20.5, `[R-WRT-06]`). An updater MUST";
  lines 886-892 match the "+" body. Header agrees with body.
- hunk-15: header says 3316-3317, heading §20.3 (line 3104). Line 3316 =
  "   forward and no other set (`[R-CNT-08]`), and version_minor per". Agrees.
- hunk-17: header says 3494-3496, heading §20.5 (line 3452). Lines 3494-3496
  = "trailer MUST copy the input's unknown ignore-lane flag bits forward /
  and set no other, in place of the flags = 0 §6.3 requires of a file /
  created under this text (`[R-CNT-08]`). ...". Agrees.
- hunk-22: header says 4652-4653, heading Appendix G (line 4535). Line 4652 =
  "   unknown ignore-lane bits forward instead, setting no other". Agrees.

## Passages read in full

- §2.1-2.4 (lines 95-336): [R-CNF-01], [R-CNF-02] conduct-rule clause,
  [R-CNF-05], [R-CNF-06], outcome table.
- §4.2 tail (460-500): [R-ENC-07] four growth vehicles.
- §6.2 trailer table row line 816: flags u32 at trailer offset 12, lanes.
- §6.3 whole (856-899): [R-CNT-07], [R-CNT-24], [R-CNT-08], [R-CNT-26].
  No line in 856-900 begins with ">" (verified by grep, 0 hits; control:
  `grep -c "^> \*\*Note"` over the file = 60), so every paragraph there is
  normative under [R-CNF-01].
- §9.1-9.3 (1233-1371), §9.6 opening (1415-1425).
- §10.1 (1511-1530), §18.3 (2780-2795), §19.1 steps 1-4 (2862-2900).
- §20 intro, §20.1, §20.2, §20.3 steps 1-6 and the Notes after (3062-3150,
  3255-3340), §20.4 opening and table (3393-3417), §20.5 whole (3452-3545).
- §21.1 (3597-3683), F13-F21 rows (3706-3714), §21.6 whole (3865-3920).
- Appendix G whole (4535-4700), Appendix H intro through updater and
  verifier entries (4700-4770). Vector trailer bytes (4380-4390).

## The rule each hunk adopts (my words)

All four state one rule: a writer under this text that has an input file
(an appender/updater, or a compactor) emits in its output trailer exactly
the ignore-lane bits its input's live trailer carried — none dropped, none
added. A creator still writes flags = 0.

- hunk-02 (§6.3, [R-CNT-08]): normative MUST/MUST NOT for the updater, plus
  a descriptive "and sets no other" for the compactor pointing at §20.5,
  plus a reason clause ("no writer under this text originates ... carried
  by every tool after").
- hunk-15 (§20.3 step 6, under "An appender MUST, in order:", [R-WRT-04]):
  restatement in the commit step, citing [R-CNT-08].
- hunk-17 (§20.5, [R-WRT-06]): the compactor's normative MUST.
- hunk-22 (Appendix G item 8, non-normative): restatement in the profile,
  citing [R-CNT-08].

## Charter exercise: the two inputs, four passages, two actors

Input A: live trailer flags = 0x0010_0000 (bit 20, ignore lane). Under this
text every ignore-lane bit is unknown (§6.3: "In this specification's text
no flag bits are defined"), so "unknown ignore-lane bits" = all set
ignore-lane bits.

| passage | appender output flags | compactor output flags |
|---|---|---|
| §6.3 [R-CNT-08] | copy bit 20, clear none, set no other -> 0x00100000 | "carries ... and sets no other" -> 0x00100000 (MUST is §20.5's) |
| §20.3 step 6 | "copied forward and no other set" -> 0x00100000 | n/a (compactor follows creation path, §20.5) |
| §20.5 [R-WRT-06] | n/a | "copy ... forward and set no other" -> 0x00100000 |
| App G item 8 | profile is one-generation (item 4); appender not addressed | "carries ... forward instead, setting no other" -> 0x00100000 |

Input B: live trailer flags = 0. Every passage -> output flags = 0 for both
actors (nothing to copy, nothing else may be set). No pair of obligations
conflicts; no passage admits a bit another forbids.

Incompat lane: an input with any incompat bit never reaches an appender's
step 6 or a compactor's output — §6.3 "an updater encountering an unknown
incompat-lane bit is a reader first, and therefore rejects"; F19 makes any
set incompat bit reject-file under this text. So "no other" read as
ignore-lane-only or as any-bit gives the same bytes for a writer under
this text.

## Charter exercise: the reason clause against every writer tier

Clause (line 887-890): "no writer under this text originates an
ignore-lane bit, this text defining none for it to mean anything by, so a
bit is set only by a writer under the later minor version that defines it
and carried by every tool after."

- creator (§20.1): has no input; "originates" none — true. But a creator
  that is fed an old file's *content* (a transcoder, an exporter, any tool
  emitting a new file under a fresh identity that is not a compactor —
  §20.5's compactor MUST preserve every stored tile's bytes verbatim, so a
  re-encoding tool cannot be one) MUST write flags = 0 (§6.3 line 879). The
  bit is NOT carried by that tool. "carried by every tool after" is false
  of it.
- appender: copies forward, sets no other — holds.
- compactor: copies forward, sets no other — holds.
- a tool under the later minor that defines the bit: this text cannot bind
  it; it may legitimately clear the bit (e.g. the feature it flags was
  removed). "carried by every tool after" is also not something this text
  can assert of it.
- recovery tool (§9.6): truncates to an earlier generation whose trailer
  may predate the bit; the bit is not "carried". Marginal, noted only.

Verdict: OVERCLAIM (finding B-01).

## Charter exercise: "unknown" is actor-relative

Writer under this text: all 16 ignore-lane bits unknown. "copy forward
unknown ignore-lane bits" = copy all; "MUST NOT set any other" = set none
not in input. Consistent.

Writer recognising a bit (later minor): the known bit is not among
"unknown ignore-lane bits", so this sentence neither obliges it to copy
nor bars it from clearing that bit; "MUST NOT set any other" read literally
would bar it from setting the known bit, but the same sentence says "a bit
is set only by a writer under the later minor version that defines it",
and that writer's own text governs it. Within this text the two clauses are
consistent for the actor this text binds. No finding.

## Charter exercise: placement vs §2.3 and the §21.6 row

Is a file an appender marks in violation of the new MUST NOT conforming?
Yes. Deciding sentence: §6.3 line 880-882 "a set ignore-lane bit is not a
file-conformance violation — such bits are defined by later minor
versions, and files carrying them are conforming files this text's readers
ignore", restated by the §21.6 row "An ignore-lane flag bit (16–31) is set
| Ignored; the file is conforming". So the MUST NOT is a conduct rule.

§2.3 [R-CNF-02]: "A writer obligation whose violation this specification
expressly declares not to be a file-conformance violation binds the actor
in the same way; §6.3's flags = 0 against a set ignore-lane bit and §6.2's
pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this
text states, and each is declared where it arises rather than enumerated
here." The general clause covers the new MUST NOT exactly (its violation
produces a file carrying a set ignore-lane bit, which §6.3 expressly
declares not a violation). The enumeration "are the cases this text
states" names only the creator's flags = 0. The repair added a case in
§6.3 and did not sweep §2.3. Finding B-02 (non-byte-level).

## The eight checks, per hunk

### Hunk 02 (§6.3)

1. Tense/quantifier. "unknown ignore-lane bits of the file it modifies" —
   the file's live trailer (the one step 1/2 of §20.3 validated; superseded
   trailers are slack per §21.6). Actor: updater. "any other" ranges over
   bits not set in that trailer. The MUST here IS the normative rule for an
   updater. Pass.
2. Citations. §20.5: read; contains the compactor MUST — pass. [R-WRT-06]:
   the §20.5 paragraph ending line 3511 carries it and contains the MUST —
   pass. [R-CNT-08] labels this paragraph — pass.
3. Label. Paragraph at 876-892 has no ">" and no Note/Example/Rationale
   label; normative. Pass.
4. Same-passage contradiction. Line 879 "a writer creating a file under
   this text MUST write flags = 0" vs. the compactor carrying bits: the
   paragraph itself carves the compactor out ("though its output is a new
   file, carries ... rather than writing flags = 0") and §20.5 says "in
   place of". Pre-existing and self-resolving. But the new reason clause
   "carried by every tool after" collides with line 879 for a creator fed
   old content — see B-01.
5. Exhaustive claims: "no writer under this text originates" (true by rule),
   "none" (true), "only by a writer under the later minor version that
   defines it" (true modulo a still-later minor also defining it),
   "every tool after" (FALSE — B-01), "any other" (fine).
6. Unconstrained siblings. Structure: trailer flags u32. Ignore lane
   (16-31): fixed for creator (0), appender (copy, no other), compactor
   (copy, no other). Incompat lane (0-15): creator 0; appender/compactor —
   input can carry none (reader-first rejection) and output carrying any
   is F19 reject-file, hence barred by [R-CNF-05]/[R-CNF-06]. Sibling
   field version_minor: [R-CNT-26] (creator floor, appender max of floor and
   prior), §20.5 SHOULD for compactor. Nothing left open.
7. Analogy. "rather than writing flags = 0" against line 879 "a writer
   creating a file ... MUST write flags = 0": both are the creator's
   flags = 0; same verb "write/writing", same object. Pass.
8. Anaphors after the insertion: "An updater encountering an unknown
   incompat-lane bit is a reader first" — no back-reference. [R-CNT-26]
   paragraph: "that floor" resolves inside its own sentence, "the prior
   trailer's minor" is self-contained. Inside the insertion: "them" =
   unknown ignore-lane bits; "it" (for it to mean anything by) = writer;
   "it" (defines it) = bit; "after" = after that later-minor writer. All
   resolve locally. Pass.

### Hunk 15 (§20.3 step 6)

1. Under "An appender MUST, in order:" so "no other set" is MUST-level via
   the list head; restates [R-CNT-08]'s updater rule with the same
   quantifier (unknown ignore-lane bits; no other). Pass.
2. [R-CNT-08]: read; says copy forward, don't clear, set no other — pass.
   [R-CNT-26]: read; appender = max(floor, prior minor) — pass.
   [R-LIF-02]: steps 4-6 barrier/pad/trailer/barrier, "+128" — pass.
   [R-WRT-04]: labels this procedure — pass.
3. Numbered step, no label; normative. Pass.
4. Step 6 also says "the same file_id" — consistent with [R-LIF-01] commit.
   No carve-out collides. Pass.
5. "no other" — fine (see hunk 02 check 6). Pass.
6. Same structure analysis as hunk 02. Pass.
7. No analogy. n/a.
8. Following text is a Note and Examples; no back-reference re-resolves.
   Pass.

### Hunk 17 (§20.5)

1. "the input's unknown ignore-lane flag bits" — the input's live trailer
   (§20.5 first sentence: output contains only what is reachable from the
   input's live trailer). This MUST IS the compactor's normative rule.
   Pass.
2. §6.3: read; "a writer creating a file under this text MUST write
   flags = 0" — the sentence's "flags = 0 §6.3 requires of a file created
   under this text" matches — pass. [R-CNT-08]: pass.
3. Prose paragraph, no label; normative, tagged [R-WRT-06]. Pass.
4. The paragraph above obliges a compactor to follow [R-LIF-02]'s creation
   path "as §20.2 obliges a creator" — §20.2 does not mention flags, and
   the "in place of" clause names the departure. The next sentence
   ("Where the output carries a feature ... a carried ignore-lane bit") is
   consistent with copying. Pass.
5. "set no other" — fine. Pass.
6. As hunk 02. Pass.
7. Analogy "in place of the flags = 0 §6.3 requires of a file created under
   this text" vs §6.3 "a writer creating a file under this text MUST write
   flags = 0": "created" / "creating", same set (creators' files). Pass.
8. "a carried ignore-lane bit (§6.3)" resolves to the copy-forward — same
   before and after the insertion. Pass. Subject "The output trailer MUST
   ... set" is a structure named as actor — pre-existing wording, the actor
   is the compactor from context; not filed.

### Hunk 22 (Appendix G item 8)

1. Non-normative restatement; quantifier matches [R-CNT-08]. Pass.
2. [R-CNT-08]: pass. [R-CNT-26]: pass. [R-WRT-06]: §20.5's SHOULD on
   version_minor for a carried feature and the fresh file_id — pass.
3. Appendix headed "(non-normative)"; the rule's normative statements are
   §6.3 and §20.5. Pass (restatement, not sole statement).
4. Closing paragraph line 4689-4691 "item 8, binding creator and compactor
   alike save §20.5's carried-feature case, its `flags` half a creator's
   rule alone" — still true: the compactor's flags are fixed by [R-CNT-08],
   not by the profile. Item 8's "reproducible only modulo its trailer:
   file_id ... and this item's floor" — flags no longer a source of
   variance, consistent. Pass.
5. No new exhaustive word. Pass.
6. As above. Pass.
7. "as item 2's identifier is" — item 2 line 4567-4568: "This is a
   creator's rule: a compactor adopting the profile takes [R-WRT-06]'s
   fresh draw instead". Parallel: creator's rule / compactor does X
   instead. Same shape. Pass.
8. "The version_minor floor binds a compactor too" — no anaphor re-resolves.
   Pass.

## Sweeps (verbatim, with counts)

- `grep -n "sets no other\|set no other\|no other set\|setting no other"` -> 4
  hits: 885, 3316, 3495, 4652 (= the four hunks; no fifth restatement).
- `grep -n "set any other"` -> 1: 887.
- `grep -n "every tool after"` -> 1: 890.
- `grep -n "originates"` -> 1: 888.
- `grep -n "flags. = 0\|flags = 0"` -> 5: 173, 880, 885, 3495, 4650.
- `grep -n -i "copy forward\|copied forward\|copies forward\|carries forward\|carried forward\|carry forward\|forward instead\|bits forward"` -> 9:
  306, 886, 3083, 3131, 3134, 3494, 3513, 4652 (flag-related: 886, 3494,
  4652; 3315 is caught by the "no other" sweep).
- `grep -n -i "ignore-lane\|ignore lane\|incompat-lane\|incompat lane"` -> 22
  hits (173, 495, 816, 877-891 cluster, 1521, 2788, 3315, 3415, 3494, 3498,
  3712, 3877, 4387, 4464-4465, 4652). Each opened; only 886/3315/3494/4652
  state the copy-forward rule; 173 restates the conduct classification
  (B-02); 3415 is the incompat reject; 3712 is F19; 3877 is the §21.6 row.
- `grep -n "creating a file\|created under this text\|file created"` -> 2:
  879, 3496.
- `sed -n '856,900p' | grep -n "^>"` -> 0 hits. Control:
  `grep -c "^> \*\*Note"` over the file -> 60 (the marker pattern finds
  blockquotes elsewhere, so the zero is real).
- `grep -n -i "updater\b"` -> 30+ hits; opened the ones in §2.3, §6.3, §20.3,
  §20.4, Appendix H. Appendix H's updater entry (4735-4744) does not mention
  the flag copy at all — pre-existing omission (the MUST copy forward
  predates the repair), non-normative summary whose "authority is the
  requirement or section cited, never this summary" (4701-4702). Not filed.

## Derived numbers

- Hunk line ranges vs current file: 885-892, 3316-3317, 3494-3496,
  4652-4653 — all four match the text at those lines.
- Restatements of the "no other" clause: 4 found = 4 hunks. 0 unswept.
- Normative statements of the no-set rule: 2 (§6.3 updater MUST NOT;
  §20.5 compactor MUST), + 1 MUST-level step restatement (§20.3 step 6),
  + 1 non-normative (App G).
- Lanes: bits 0-15 = 16 incompat, 16-31 = 16 ignore, total 32 = u32 width
  at trailer offset 12 (line 816). Vector: trailer at 64, flags at [76,80)
  = offset 12 — matches; value 00 00 00 00 matches creator's flags = 0.
- §2.3 [R-CNF-02] enumeration: 2 cases named; §6.3 now carries (creator
  flags = 0), (updater MUST NOT clear), (updater MUST NOT set), and §20.5
  the compactor MUST — 3 of these are obligations whose violation yields a
  file §6.3 expressly declares conforming (flags = 0; MUST NOT set; §20.5's
  set-no-other), against the 1 named for §6.3.

## Findings

B-01 (hunk 02, OVERCLAIM, §6.3 line 887-890): "carried by every tool after"
is false of a creator under this text that emits a new file from an old
file's content — §6.3 line 879 obliges it to write flags = 0, dropping the
bit — and is a claim this text cannot make about tools under a later
minor. Non-byte-level: the MUST at 879 governs a creator unambiguously,
and any file either reading produces is conforming (§21.6 row), so the
emittable set of a competent implementation does not move; the defect is
a false explanatory sentence in normative text that a reader could take as
a rule. Repair: cut "and carried by every tool after", or replace with
"and carried by every updater and compactor of that file under this text".

B-02 (hunk 02, UNSWEPT_RESTATEMENT, §2.3 [R-CNF-02] line 172-175): §2.3
enumerates the writer obligations whose violation is expressly declared
not a file-conformance violation as "§6.3's flags = 0 against a set
ignore-lane bit and §6.2's pre-trailer gap ... are the cases this text
states". The repair added "MUST NOT set any other" to §6.3 (and "set no
other" to §20.5), whose violation is exactly such a case, and did not sweep
§2.3. Non-byte-level: file conformance is unchanged under either reading;
what is at stake is whether §2.3's list is read as closed. Repair: in §2.3
replace "§6.3's flags = 0 against a set ignore-lane bit" with "§6.3's and
§20.5's flags rules — flags = 0, and the copy-forward-and-set-no-other
obligations — against a set ignore-lane bit".

## Rejected candidates

- §6.3's creator MUST flags = 0 vs §20.5's compactor MUST copy (compactor
  follows the creation path): dropped because the same §6.3 paragraph
  carves the compactor out ("though its output is a new file, carries ...
  rather than writing flags = 0") and §20.5 says "in place of the
  flags = 0 §6.3 requires"; pre-existing, not touched by the repair.
- "MUST NOT set any other" lane ambiguity (ignore lane only vs any bit):
  dropped because F19 makes any set incompat bit reject-file, so both
  readings give the same emittable set for a writer under this text.
- "The output trailer MUST ... set no other" — structure as actor: dropped
  as pre-existing subject, meaning unmistakable from the paragraph.
- Appendix H updater checklist silent on the flag copy: dropped — the
  omission predates the repair and the appendix disclaims authority.
- App G closing paragraph "its `flags` half a creator's rule alone" vs
  item 8's compactor clause: dropped — the compactor's flags are fixed by
  [R-CNT-08] not the profile, so the sentence remains true.
- Later-minor writer barred by "MUST NOT set any other" from setting a bit
  it knows: dropped — that writer is governed by its own text, and the
  sentence itself says such a writer is the one that sets it.
