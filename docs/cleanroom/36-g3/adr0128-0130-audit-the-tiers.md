# Audit transcript — "the-tiers" lane (hunks 01, 02, 08, 09, 13, 19, 48)

## 0. Disclosure of contaminating context

Before any tool call, my context already contained (via CLAUDE.md, MEMORY.md,
and a git-status system reminder) references to: AGENTS.md, prior-round memory
notes with titles like "TARN harness vs charter", "TARN repair prose vs
rules", "TARN lineage gate word list", recent commit subjects (ADR-0130,
ADR-0129, ADR-0128, Q-A8, ADR-0125), and other project material I am not
permitted to read. This is disclosed per the access rule. I did not open
AGENTS.md, any ADR, docs/, PLAN.md, OPEN-QUESTIONS.md, conformance/,
spec/registry.json, git log/diff, or the web, and I did not let the
memory-file titles steer which defects I looked for — every finding below is
argued from spec/tarn.md and my seven hunk files alone. I also did not read
full.diff or any other lane's hunk file, and did not list the `case/`
directory.

Files read: `spec/tarn.md` (via Read, in five passes: lines 140–380,
1255–1394, 2365–2395, 3095–3693, 4847–4942) and the seven named hunk files
under `.../r36-audit/case/`. Commands run: `wc -l`, and a series of `grep`
calls (below) against `spec/tarn.md` only. No other file was opened.

Working file written: none needed beyond this transcript (no CRC
recomputation was required for this lane's checks). If I had needed a
scratch file it would have gone under
`.../r36-audit/scratch/the-tiers/`, which I created but left empty.

## 1. Hunk files, read first

All seven hunk files matched their stated headers (section context, line
numbers) and the bodies were internally consistent with their own `@@`
headers — no hunk/header mismatch to report for any of my seven.

- hunk-01: §2.3, line 175, actor-binding parenthetical in the §6.3-flags
  example inside `[R-CNF-02]`'s paragraph.
- hunk-02: §2.3, lines 212–213, end of the "Conforming updater" bullet.
- hunk-08: §6.2, line 837, the trailer's `flags` table cell.
- hunk-09: §6.3, lines 904–912, the ignore-lane-bits paragraph under
  `[R-CNT-08]`.
- hunk-13: §9.1, line 1273, `[R-LIF-01]`'s own sentence.
- hunk-19: §20.1, lines 3129–3151, the tier bullets and the classification
  paragraph under `[R-WRT-01]`.
- hunk-48: Appendix H, lines 4883–4889 (writer entry) and updater entry's
  opening.

## 2. §2.3's five classes and §20.1 in full — read first as instructed

Read lines 152–250 (all five §2.3 classes) and lines 3114–3693 (all of
§20 through §20.5) before touching any specific check. Key excerpts I rely
on below:

- Tier bullets (§20.1, post-repair): creator / appender / **rewriter** —
  "writes a new file from an existing one under a new identity (§20.5),
  carrying structures forward, re-creating some, or dropping some;
  compaction ... is the rewrite that reclaims slack."
- "An appender and a rewriter are updaters" (§20.1).
- "Conforming updater. **A tool that modifies an existing file** without
  necessarily understanding all of its content. ... Its tiers, the
  appender and the rewriter, are §20.1's." (§2.3, post hunk-02)
- "A rewriter's output is a new file under a fresh file_id" (§20.5, opening
  sentence) — output, explicitly, is *a new file*, not a modification of
  the input.
- "That a rewrite is not a commit (`[R-LIF-01]`) fixes what the output
  *is*, not which rules govern the writing of it." (§20.5)

## 3. Classification test (hunk-19) — run against the charter's four cases

The new §20.1 paragraph gives two tests for "updater vs. creator":

- **Test 1 (shape/identity)**: creator = first-generation, one commit;
  appender = extends by commit, same file_id; rewriter = new file, new
  identity, per §20.5.
- **Test 2 (decode test, new sentence)**: "a writer that carries forward
  any structure of an input file it did not decode is an updater ... and
  one that decodes everything it writes is a creator, **whatever it
  read**."

Classified all four charter scenarios:

**(a) An appender that adds one layer, decodes nothing else.**
Test 1: appender (extends by commit, §9.2). Test 2: it re-emits (§20.4,
`[R-WRT-05]`) every other record byte-identically without decoding it →
"carries forward ... did not decode" → updater. **Agree.** Owes: same
file_id (not fresh — "The appender's commit extends its input under the
input's file_id," §20.1); §20.4 preservation, yes; `[R-CNT-08]`
carry-forward, yes (§20.3 step 6).

**(b) A rewriter that re-creates every layer, implementing every record
type present (so nothing it meets is unimplemented).**
As long as it carries forward *something* undecoded (e.g. a retained
non-layer record it does not re-derive, or even just the unread portions
of what §20.5's checksum-only verification touches without full content
decode), Test 2 still calls it "updater." Test 1: rewriter → updater.
**Agree**, on the reading that "re-creates every layer" does not entail
"decodes literally everything in the file." Owes: fresh file_id (§20.5,
always); §20.4 preservation for what it carries; `[R-CNT-08]` (§20.5).

**(c) "A tool that reads a file whole and writes a new one from the
decoded content."**
Test 2, read literally: "one that decodes everything it writes is a
creator, whatever it read" → this tool is a **creator**. Test 1: this is
exactly what §20.1's rewriter bullet describes — "writes a new file from
an existing one under a new identity ..., re-creating some [up to
all]" — and §20.5 explicitly allows full re-creation with nothing carried
verbatim ("Each structure of the input is carried forward verbatim,
re-created as new output, or dropped"; "A layer the rewrite re-creates is
new output ... nothing of the input's copy of that layer is carried
forward"). Test 1 → **rewriter**, hence (by "An appender and a rewriter
are updaters") **updater**.
**The two tests disagree** for this scenario: one classifies it creator,
the other rewriter/updater. This is a genuine contradiction inside the
one paragraph hunk-19 wrote — reported as **D-01**.

**(d) A compaction.**
§20.5's own definition: "carries every structure forward and changes
nothing but placement" — and explicitly does not decode tile payloads
("every carried stored tile's bytes verbatim — each index entry's crc is
unchanged"; the §20.5 verification-depth paragraph distinguishes
"verify[ing] each link of the chain ... and the checksum" from decoding).
So compaction carries forward structures it did not decode → Test 2:
updater. Test 1: rewriter → updater. **Agree.** Owes: fresh file_id (yes,
by the general rewriter rule, even though bytes are otherwise unchanged);
§20.4 preservation (yes, for everything, since it drops nothing);
`[R-CNT-08]` (yes, §20.5).

### Byte-level assessment of D-01

Checked whether the creator/rewriter fork for case (c) changes the
emittable byte set or accept/reject verdicts. Obligations that differ
between the two labels (fresh-file_id mechanics comparison against the
input under `[R-LIF-03]`; §20.4 preservation for anything carried
undecoded; `[R-WRT-06]`'s MU=1 refusal; `[R-WRT-09]`'s verify-before-copy
duty; §20.5's version_minor floor exception for carried-but-undecoded
features) are all **conditioned on something being carried forward
without full decode**. In the pure case-(c) scenario (decodes literally
everything, carries nothing undecoded), every one of those duties is
vacuous under either label, and both labels converge on the same
`[R-LIF-02]` creation-path mechanics for the output bytes. **Not
byte-level** — this is a definitional contradiction, not a fork in what a
conforming implementation may emit.

## 4. hunk-02 — "Conforming updater" class vs. the rewriter it now names

Quoted above: "A tool that modifies an existing file ... Its tiers, the
appender and the rewriter, are §20.1's." Held side by side with §20.5's
opening sentence: "A rewriter's output is a new file under a fresh
file_id." A rewriter, by the document's own repeated framing (§9.1's
immutable committed prefix; §20.5's "not a commit"), **never modifies the
existing file** — the input is left completely untouched; the rewriter's
product is a wholly separate file. So the class-defining sentence ("a
tool that modifies an existing file") is false of one of the two tiers
the very same bullet, in this hunk's own insertion, names as belonging to
that class. **D-02.**

Grep control: searched for "modifies an existing file" (single line,
short, no wrap risk) — one hit, line 208, confirming this is the class's
sole defining clause, not a paraphrase I mis-picked.

Checked `[R-CNF-06]` against `[R-WRT-01]` word for word, per the charter's
instruction: `[R-CNF-06]` (§2.3) — "An updater MUST satisfy every writer
requirement for the bytes it produces, and additionally MUST honor the
preservation obligations of §20.4." `[R-WRT-01]` (§20.1, hunk-19) — "each
satisfies every writer requirement for the bytes it produces and the
preservation obligations of §20.4 for what it carries forward." Same
governing verbs ("satisfy"/"satisfies," "honor"/[implicit]), same two
duties, same section citation. **Confirmed consistent.**

Byte-level: no — the substantive MUST-duties (`[R-CNF-06]`'s own two
duties) are independently and correctly restated for the rewriter in
§20.5 itself, so no implementation would be misled about what bytes it
must produce; this is a definitional-sentence contradiction, not an
obligation gap.

## 5. hunk-01 — the §2.3 citation

Old: "a creator's flags = 0, and an updater's or compactor's copy-forward
and set-no-other, §20.5". New: "a creator's flags = 0, and an updater's
copy-forward and set-no-other, §20.5".

Checked where "an updater's" (= appender ∪ rewriter, per hunk-02) duty to
copy forward ignore-lane bits and set no other is actually stated:

- Appender's version: §20.3 step 6 — "unknown ignore-lane flag bits
  copied forward and no other set (`[R-CNT-08]`)" (line 3363–3364).
- Rewriter's version: §20.5 — "The output trailer MUST copy the input's
  unknown ignore-lane flag bits forward and set no other ... (`[R-CNT-08]`)"
  (line 3574–3577), and the earlier §6.3 sentence citing "(§20.5,
  `[R-WRT-06]`)" (line 906).

"§20.5" therefore only locates the rewriter half of "an updater's ...
duty." The repair *removed* the "or compactor's" disjunction that
previously scoped "§20.5" to the compactor-only clause and left the
single citation attached to the whole, now-unified "an updater's" phrase
— which is broader than what §20.5 states. The appender's copy-forward
duty (§20.3 step 6) is uncited here. **D-03**, category CITATION.
Byte-level: no — this is a pointer, not itself an obligation; the actual
duties are correctly stated at their real locations.

## 6. hunk-09 / hunk-08 — §6.3 and §6.2's flags text, held to `[R-CNT-08]`

Read the whole §6.3 paragraph (877–915). The paragraph:

1. Creator: "MUST write flags = 0."
2. Rewriter (hunk-09 edited this sentence): "though its output is a new
   file, carries the input's unknown ignore-lane bits into its output
   trailer rather than writing flags = 0, and sets no other (§20.5,
   `[R-WRT-06]`)."
3. **Unedited by this hunk**: "An updater MUST copy forward unknown
   ignore-lane bits of **the file it modifies**, MUST NOT clear them, and
   MUST NOT set any other: ..."
4. Hunk-09's edited tail: "... so a bit is set only by a writer under the
   later minor version that defines it and carried forward by every
   updater under this text, **appender and rewriter alike**."

Sentence 3's operative phrase, "the file it modifies," is precisely the
verb the document elsewhere reserves for the appender ("A tool that
modifies an existing file," §2.3; a rewriter's output is "a new file,"
§20.5, never a modification of the input). Sentence 3 is unedited by
hunk-09, but it sits inside the same paragraph, under the same
`[R-CNT-08]` tag, as hunk-09's new clause that explicitly extends the
duty to "appender and rewriter alike." Read narrowly, sentence 3's own
MUST-clause textually excludes the rewriter (which does not "modify" any
file); read as part of the whole paragraph (sentence 2 already covers the
rewriter, sentence 4 summarizes both), it is defensible. I could not
resolve this to a single unambiguous reading from the text alone.
**D-04**, category TENSE_QUANTIFIER, verdict PLAUSIBLE rather than
CONFIRMED given the competing charitable reading.

Byte-level: no. The rewriter's ignore-lane duty is independently and
unambiguously pinned at §20.5 (line 3574–3577), under the same
`[R-CNT-08]` tag, so — per the charter's own framing — the MUST "reaches
a rewriter twice," once cleanly (§20.5, unconditional "the output
trailer MUST") and once through the ambiguous §6.3 wording. No
implementation could conclude from this that a rewriter is *exempt* from
copying ignore-lane bits forward, because §20.5 alone already settles it.

hunk-08 (§6.2 table cell): "carried forward unchanged by an updater,
appender or rewriter alike" — checked this is not under- or over-broad:
"updater" = appender ∪ rewriter (§2.3 post-repair), so naming all three is
redundant-but-not-wrong, matching the same "supertype, then both
subtypes" construction hunk-09 uses. Confirmed the table itself is
**not** inside a blockquote (raw-byte check below) — it is a normative
`|...|` table, correctly binding. No defect.

## 7. hunk-13 — `[R-LIF-01]`'s parenthetical

Old: "under a new file_id (compaction, §20)." New: "under a new file_id
(a rewrite, §20.5)."

`[R-LIF-01]`'s governing sentence is "every conforming mutation of a file
is either a commit (§9.2) or a whole-file rewrite under a new file_id."
The old parenthetical example ("compaction") named only one of the three
named rewrites (§20.5: compaction, dropping, re-declaring) as if it were
the whole category; the new one ("a rewrite") matches the governing
sentence's own noun and points at the section (§20.5) that actually
defines the mechanism (fresh file_id draw, `[R-LIF-03]` cache-contract
reasoning). This widens the illustrative label correctly rather than
narrowing or over-generalizing it — no defect.

Checked every other `[R-LIF-01]` citation in the document (grep, 10
hits total): lines 1273 (this one), 1316, 1381, 3117, 3145, 3198, 3219,
3255, 3554, 3570 — read each in context (§9.1, §9.3's two Notes, §20.1,
§20.3 steps 2 and 4, §20.5 twice). All are consistent with "a rewrite,
not a commit, mints a new file_id" and none depend on the old
"compaction"-only wording. **No defect; hunk-13 passes cleanly.**

One adjacent, pre-existing wrinkle noted but **not** flagged as a hunk-13
defect (it doesn't cite `[R-LIF-01]` and isn't part of any of my seven
hunks): a §9.3 Note (line 1389–1391) calls a rewrite's output "a fresh
file_id whose **first commit** starts F over," which sits oddly next to
§20.5's explicit "a rewrite is not a commit." This is pre-existing,
untouched text outside my charter; noted for completeness, not counted as
a finding.

## 8. hunk-48 — Appendix H, "Conforming updater" as a checklist for a rewriter

Confirmed Appendix H is non-normative by its own heading ("Appendix H —
Conformance checklists (non-normative)") and by its own preamble: "each
entry's authority is the requirement or section cited, **never this
summary**" (line 4850–4851) — this satisfies `[R-CNF-01]`'s "appendices
identified as non-normative" clause. So findings here are inherently
non-byte-level, but the charter specifically asked for this checklist to
be read as binding on a rewriter, and I did so.

Read the whole entry (lines 4888–4915). The header, edited by this hunk,
now reads: "**Conforming updater**, an appender or a rewriter (§20.1) —
everything a writer does ... plus:" — i.e. everything that follows, up to
"A rewriter, in addition," is presented as shared between both tiers.

Quoted clause that cannot be true of a rewriter: "changes a layer that
stores a tile in the generation **its commit** supersedes only as §20.3
step 4 permits — its names, a grown dimension extent, a planar channel
list extended at its end or shortened from it (not both in one commit),
a slab or alignment declaration declared, changed or cleared — and makes
any other change to it as a new layer **or a whole-file rewrite** (§20.3)."

This is §20.3 step 4's rule verbatim in substance — a rule that binds a
*commit*. §20.3 step 4 itself states the escape valve: "the change is a
new layer, or **a rewrite that re-declares it** under a fresh file_id
(`[R-LIF-01]`, §20.5)" (line 3254–3255) — i.e. a rewrite (specifically
the "re-declaring" case named in §20.5) is exactly the operation that is
*not* bound by step 4's limited list; it is free to change layout, codec,
filter, rank, tile extent, etc., which step 4 forbids a commit from
touching. Placed under the now-shared "Conforming updater ... an
appender or a rewriter" header, this clause reads as though a rewriter
too is limited to §20.3 step 4's list, which is false of the very
re-declaring case §20.5 names. **D-05**, category UNSWEPT_RESTATEMENT /
OVERCLAIM. Not byte-level (non-normative appendix, explicitly
disclaimed).

Secondary citation check on the same entry: "A rewriter, in addition,
mints a fresh file_id and follows the creation path (`[R-WRT-06]`)."
Traced `[R-WRT-06]`'s actual definition: it closes §20.5's *second*
paragraph (ignore-lane-bits-forward + MU=1 refuse-to-rewrite, ending
"... so its bytes cannot be safely relocated. `[R-WRT-06]`", line 3592).
The "mint a fresh file_id ... follow `[R-LIF-02]`'s creation path"
material is in the *first* paragraph of §20.5 (lines 3521–3572), which
closes with no single dedicated R-ID of its own (inline cites to
`[R-LIF-01]`, `[R-LIF-03]`, `[R-LIF-02]` instead). So `[R-WRT-06]` is the
wrong tag for this clause. **D-08**, category CITATION, low severity
(non-normative appendix), not byte-level.

Checked the rest of the entry's clauses against their cited sources —
all others (re-emission/`[R-WRT-05]`, ignore-lane copy-forward/
`[R-CNT-08]`, MU/PE governance/`[R-CNT-22]`, PE=0 drop licence, MU=1
top-level reject/`[R-CNT-15]`, carries-forward-verbatim/regenerates-
index/`[R-WRT-07]`, verifies-checksum/`[R-WRT-09]`) matched their
targets on inspection. Reported as passing.

## 9. Sweep: "updater" across the whole document (34 hits)

`grep -n "updater" spec/tarn.md` → 34 lines (list below, used as my own
working index; matches `grep -c` = 34, a self-consistency control).

```
85 111 175 208 209 216 301 303 311 440 472 837 906 911 912 1026
2372 2390 2889 3138 3148 3170 3171 3454 3466 3469 3472 3474 3481
3483 3492 3496 4272 4888
```

Read every one in its surrounding sentence. Findings beyond what's
already reported above:

- **Line 3483** (§20.4's persistence table, MU=0/PE=0 row, unedited by
  any of my hunks): "so **an updater** MAY drop the record in **any
  commit** it is otherwise free to make ... and **a rewriter** MAY drop
  it in any rewrite." "Updater" here is glossed by "in any commit" — only
  an appender commits — so this instance uses "updater" where the
  post-repair vocabulary established by hunks 01/02/19 would say
  "appender." The sentence is not *wrong* (a rewriter's own clause
  follows immediately and correctly), just imprecise against the new
  naming convention. **D-07**, category UNSWEPT_RESTATEMENT, low
  confidence, not byte-level (both tiers' drop permission is in fact
  stated, just inexactly labeled for one of them).
- **Line 2372, §16 (`[R-SLB-04]`)**: "A writer or updater whose **commit**
  changes the stored-tile set ..." — correctly commit-scoped (this rule
  is about the append path only); §20.5 separately covers rewriter
  placement freedom under `[R-SLB-01]`/`[R-SLB-03]`. Checked, no
  contradiction, and outside my hunks' subject (§16, not tier/class
  mapping) — not pursued further, noted as considered.
- All other 31 hits are either generic ("a reader — including any updater
  or verifier, which are readers of the files they process," line 472),
  already covered under §20.3/§20.4 above, or in the "Terminology"/
  "Reading this document" front matter (lines 85, 111) where "updater" is
  just named as one of the four algorithm classes — no obligation stated
  there to check.

## 10. Sweep: "compactor" / "rewriter" / "appender" (renaming completeness)

```
$ grep -c "compactor" spec/tarn.md
1
$ grep -n "compactor" spec/tarn.md
438:> payloads, so verifiers, appenders, and compactors operate on files
$ grep -c "rewriter" spec/tarn.md
41
$ grep -c "appender" spec/tarn.md
18
$ grep -c "compaction" spec/tarn.md
8
```

Control for the "compactor" zero-risk: the word is a single token that
cannot wrap across the hard-wrap boundary the way a multi-word phrase can,
so a line-oriented grep is reliable here (unlike the phrase search
below). The single surviving hit is inside a **Note** block (line
435–442: "> **Note.** Part I (container) is independent of Part II (array
model) by construction: no Part I structure requires decoding sample
payloads, so verifiers, appenders, and compactors operate on files whose
layers they cannot decode ..."). Confirmed the block's label by reading
the raw line: it begins `> **Note.**`, so per `[R-CNF-01]` it is
non-normative — this stale reference to the retired tier name has no
normative force, but it is a restatement the renaming sweep (my hunks
01/02/08/09/19/48 all replace "compactor" with "rewriter" or "an
appender and a rewriter") should have caught and did not. **D-06**,
category UNSWEPT_RESTATEMENT, not byte-level (Note, non-normative).

## 11. Hard-wrap control (methodology check, run before trusting any zero)

```
$ grep -n "carries forward any structure of an input file it did not decode" spec/tarn.md
(no output, exit 1)
$ tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -o "carries forward any structure of an input file it did not decode"
carries forward any structure of an input file it did not decode
```

This confirms the phrase is present (it is — I quoted it above straight
from the Read tool's output, which does not hard-wrap) and that a naive
line-oriented grep for a hard-wrapped multi-word phrase silently returns
zero. All phrase-level claims above were either verified by reading the
Read tool's un-wrapped output directly, or (where I used grep) restricted
to single tokens/short citations (`compactor`, `updater`, `R-LIF-01`,
"copy-forward and set-no-other" — this last one is short enough that it
happened to sit on one physical line, confirmed by the direct hit at line
175 shown in §5 above) that cannot wrap.

## 12. BCP-14 casing and NESTED_DASH, all seven hunks' `+` text

Checked every inserted/changed line in all seven hunk files for stray
lowercase `must`/`should`/`may`/`shall` meant as keywords, and for
non-keyword text wrongly capitalized as if a keyword. None of the seven
hunks introduce a BCP-14 keyword at all (the MUST/SHOULD/MAY instances
near them are all pre-existing, unedited context). No casing defects.

Checked every inserted line for an em-dash pair nested inside a clause
already set off by em-dashes. Found one em-dash-delimited clause in
hunk-19's insertion ("... is a reader of every structure it processes
(`[R-CNF-11]`) — a violation latent in a structure it carries forward
unmodified travels with it, seen or unseen, and certifying the whole
file is a verifier's office (§9.7)."), but it is a single dash running to
the sentence's end, not a pair, and not nested. Hunk-48's "— everything a
writer does for the bytes it produces, plus:" is likewise a single,
non-nested dash. No NESTED_DASH defects in the seven hunks' own edited
text.

## 13. Rejected candidates

- Considered flagging "Its tiers, the appender and the rewriter, are
  §20.1's" (hunk-02) as an ANAPHOR defect ("Its" reads across two
  intervening sentences). Rejected: "tiers" as a noun only attaches
  meaningfully to "an updater" in this passage (no other candidate
  antecedent — "§20.4," "every record type" — has "tiers"), so the
  reference resolves unambiguously despite the distance.
- Considered flagging the "carries forward" predicate in hunk-19's
  Test 2 as conflating two physically different operations (an appender
  literally copies no committed byte — the old bytes stay put in [0,F)
  and only a fresh directory entry is written past F; a rewriter
  literally copies bytes into new output). Rejected as a defect: the
  test's behavioral point (did the writer include a structure without
  decoding/understanding it) holds regardless of which physical
  mechanism achieves it; the charter's own question ("say what 'carries
  forward' means of an appender, which copies no committed byte") is
  answered by this observation, not falsified by it.
- Considered whether hunk-19's "Every obligation of §20.3 through §20.5
  attaches to an operation" is an EXHAUSTIVE_CLAIM defect (does some
  §20.3–§20.5 obligation NOT attach to an operation?). Checked §20.4's
  table and §20.5's paragraphs; all stated duties are operation-keyed
  (what the actor does to a given structure), expressed via actor nouns
  as shorthand. Rejected — this reads as an architectural/framing claim,
  not a falsifiable enumeration.
- Considered the §9.3 Note calling a rewrite's output start "its first
  commit" (line 1389–1391) as a LOCAL_CONTRADICTION against §20.5's "a
  rewrite is not a commit." Not reported as a hunk finding: it neither
  cites `[R-LIF-01]` nor sits inside any of my seven hunks or their
  landing subsections; noted in §7 above for the record but excluded
  from the findings array as out of charter.
- Considered §16's `[R-SLB-04]` ("A writer or updater whose commit
  changes...", line 2372) for the same appender/rewriter scoping issue as
  D-07. Left out of the findings array: it is correctly commit-scoped on
  inspection (the rewriter's parallel duty is stated separately, under
  R-SLB-01/R-SLB-03, in §20.5), and it is outside my charter's
  tier/class-mapping hunks.

## 14. Checks 1–8 status summary

1. TENSE/QUANTIFIER: run on all seven hunks; failures at D-01 (which
   generation/definition — creator vs rewriter — a "decodes everything"
   writer belongs to) and D-04 ("the file it modifies").
2. CITATIONS RESOLVE: every `[R-ID]` and §-number in the seven hunks'
   changed text checked against its target (list in `citations_checked`).
   Failures: D-03 (§20.5 under-cites), D-08 (`[R-WRT-06]` mistargeted in
   Appendix H).
3. LABEL, NOT MARKER: checked the §6.2 and §20.4 tables (not
   blockquoted, confirmed by raw-line inspection — normative, correctly
   binding) and the line-438 Note (labeled `**Note.**`, confirmed
   non-normative — D-06 has no force, which is itself part of the
   finding). No case found where a `>`-marked block without a Note/
   Example/Rationale label was wrongly treated as inert.
4. NO CONTRADICTION IN THE PASSAGE: D-01, D-02, D-04, D-05 are all this
   check.
5. NO EXHAUSTIVE CLAIM: checked "every obligation... attaches to an
   operation," "Its tiers, the appender and the rewriter" (closed pair,
   confirmed exhaustive against §20.1's own three-bullet list), "carried
   forward unchanged by an updater, appender or rewriter alike" (exhaustive
   given creator's separate flags=0 clause). No overclaim found beyond
   what's in D-01/D-02/D-05 (which are contradictions, not overclaims per
   se).
6. UNCONSTRAINED SIBLING: the structure hunk-19 governs is the
   three-way tier taxonomy itself; every writer operation must resolve to
   exactly one tier. Case (c) shows it does not always resolve to exactly
   one (D-01). No other sibling quantity found unconstrained within my
   seven hunks' scope.
7. ANALOGY: only one "hold X to Y" instance in my hunks — the rewriter
   bullet's compaction clause vs. §20.5's own compaction definition.
   Compared word for word: "carries every structure forward and changes
   nothing but placement, is the rewrite that reclaims slack" (§20.1) vs.
   "which carries every structure forward and changes nothing but
   placement, and is the rewrite that reclaims slack" (§20.5) — identical
   governing verbs and quantifiers. Passes.
8. ANAPHOR: ran on hunk-19 (largest insertion) and hunk-02. No case
   where a back-reference's antecedent changed as a result of the
   insertion — see §13 for the "Its tiers" case considered and rejected.

## 15. Confidence where findings are thin

D-04 and D-07 are reported at lower confidence (PLAUSIBLE, not CONFIRMED)
because each has a genuine competing charitable reading, which I have
stated alongside the finding rather than suppressing. I did not stop
after finding D-01/D-02; I completed the full 34-line "updater" sweep, the
"compactor" sweep, the citation check on every `[R-ID]` in all seven
hunks' changed text, and the blockquote-label check on both tables named
in the charter's own hints, specifically to avoid the failure mode the
brief warns about (a lane returning few findings without having actually
run the checks).
