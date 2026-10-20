# Reader-comparator working transcript

## Disclosure

**Relayed user request.** A line above the computed task relayed the literal
text "Go" as the message that launched this round. That is the launcher's
message to the orchestrator, carried out before I was spawned; it is not a
task for me, needs no reconciliation with this brief, and does not widen the
access rule below. I disclose that it appeared and do nothing else with it.

**Context I did not ask for.** Before this task began my context already
contained a CLAUDE.md pointer to AGENTS.md (not opened), a user MEMORY.md
index of many prior-round entries about this project's harness and findings,
a git-status block naming the current branch ("readable") and five recent
commit subjects about a "Readable" rewrite of §§14-17, and a model/
environment identity block. None of this is the specification and none of
it is evidence about its content. I did not let it shape which passages I
read or how I resolved any difference below; I used the commit subjects only
as a hint of *where* a human-reviewed prose change might be concentrated
(§14, §15.1, §15.4, §16.2, §17.4), and then verified every one of those
locations against the actual file bytes rather than trusting the subject
lines.

**Access.** I read exactly:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
  (edition A, 5,004 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
  (edition B, 4,810 lines)
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/out/transcript-reader-a.md`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/out/transcript-reader-b.md`

I did not list any directory other than my own scratch directory (to create
it). I did not open AGENTS.md, PLAN.md, OPEN-QUESTIONS.md, README.md,
docs/, conformance/, spec/registry.json, git history, or the web. Every
`grep`/`rg` I ran was against only the two spec files above, to pin line
numbers or to search a short, non-wrapping fragment; every such search is
listed in the evidence block with its hit count, and every zero I report is
backed by a control search for a phrase I had already read and knew was
present nearby (so the zero reflects a real absence, not a wrap miss). I
read every passage I cite below directly with `Read` in addition to any
grep, specifically to avoid trusting either walker's citations on faith, per
the charter's instruction.

**Wrapping.** Both editions are hard-wrapped prose with `> `-continued
blockquotes. I located candidate passages with short single-line grep
fragments (never a multi-line phrase) and then always opened the
surrounding 50-150 lines with `Read` and compared the unwrapped sense,
never relying on a line-anchored multi-line grep.

---

## Method

I worked the charter in order: (1) for every probe, opened both editions at
the cited passages; (2) did the same even where R1/R2/R4/R5/R6/R7/R8's
answers already agreed, to rule out agreement-by-luck; (3) took each walk's
own findings (readera-01, readera-02; readerb reported none) and checked
whether the condition exists identically in the other edition; (4) read
both transcripts for forced guesses/re-derivations and checked whether the
other walker needed the same one; (5) read the sections both walks lean on
most (§2.3-2.4, §5.1, §6.2-6.4, §7.1-7.2, §11.2/11.4, §14.1-14.2,
§15.1-15.4, §16.2, §17.2-17.4, §19.1-19.4, §21.2) side by side in full,
beyond what any single probe cites.

## Probe-by-probe comparison

**R1** (open request accounting). Opened A §6.4 (925-967), §19.1
(2938-2994), §7.1 (971-1003) against B §6.4 (792-841), §19.1 (2810-2905),
§7.1 (834-841, with the user-metadata paragraph relocated to B's
§7.1-area text at 949-975 rather than deleted — confirmed present via
`grep -n "Metadata compression exists only at record granularity"` in both
files, one hit each). Sentence-for-sentence identical content, reflowed to
different line widths and occasionally re-ordered within a sentence (e.g. A:
"...so that §19.1's first two steps cost one request between them; validate
per §6.2-§6.3" vs B: "...and validate per §6.2-§6.3.... so §19.1's first two
steps cost one request between them" - same two facts, clauses swapped).
Both walkers' identical two-request, `64 + dir_length` answers are genuine
agreement on genuinely identical text. **EQUIVALENT.**

**R2** (incompat-lane bit 2). Opened A §6.2 (830-924) and §6.3, register
row F19 (3882) against B §6.2 (698-791), F19 (3707). Table row text,
`[R-CNT-08]` prose, and F19's register line are byte-identical between
editions (confirmed by direct quotation, not just citation). Both walkers'
reject-file / nonconforming answers rest on identical text. **EQUIVALENT.**

**R3** (zstd/codec-3 reader that cannot execute a core codec) — see Finding
cmp-reader-01 below. This is the one probe where the two walks' answers
diverge in *content* (A: "underdetermined," AMBIGUITY; B: "scenario's
premise cannot occur," resolved) despite the governing sentence being
**byte-for-byte identical** in both editions.

**R4** (sentinel half-match entry). Opened A §15.1-15.3 (2211-2289) against
B §15.1-15.3 (2080-2157). One wording difference with no effect: A "The
per-entry outcomes below govern notwithstanding the general owning-scope
mapping of [R-ENC-03]/[R-ENC-04]" vs B "...override the general
owning-scope mapping..." - "govern notwithstanding" vs "override," same
effect. Register row T7 identical. **EQUIVALENT.**

**R5** (directory CRC mismatch). Opened A §7.1 (971-979), §2.4 (298-317)
against B §7.1 (834-841), §2.4 (299-322). The reject-file table row ("A
reader MUST NOT rely on any structure in it") is identical in both; F20 is
identical. **EQUIVALENT.**

**R6** (F=96). Opened A §5.1 (637-661) against B §5.1 (515-539): identical
sentence-for-sentence, including the "No conforming file is shorter than
128 bytes: ... cannot be satisfied in fewer" sentence both walkers quote
verbatim. F5 register row identical. **EQUIVALENT.**

**R7** (interleaved tile-offset arithmetic). Opened A §11.2/§11.4
(1716-1805) and §14.2 against B §11.2/§11.4 (1589-1678). Identical formulas,
identical worked example (grid (4,8), ordinal 74), differences are only
clause order/punctuation. Both walkers reach ordinal 4, offset 17 by the
same arithmetic over the same text. **EQUIVALENT.**

**R8** (top-level vs sub-record MU=1). Opened A §2.3 (152-283), §2.4
(298-317), register rows F35/F36/L24/L25 against the same sections/rows in
B. All four register rows are byte-identical (verified by direct grep and
quotation, not citation alone); §21.6's closing-paragraph asymmetry claim
("...the same type as a layer sub-record is reject-layer and never a
ground to refuse the file...") — present in A at 4080-4082 and
functionally mirrored in B (confirmed via B's own R8 answer's verbatim
quotation, cross-checked against B's text). **EQUIVALENT.**

## Each walk's own findings, checked against the other edition

**readera-01** (edition A's AMBIGUITY finding on R3/codec capability) — see
Finding cmp-reader-01. On inspection this is not an ambiguity *of the
document*; both editions already resolve it in the same sentence, which
walker A's own transcript quotes a truncated version of and then claims
"no equivalent text binds an ordinary reader" for — directly contradicted
by text inside the very line range (2634-2646) walker A cites.

**readera-02** (edition A's OBSERVATION that the trailer's 16-bit
"incompat lane" is permanently unpopulatable under the closed §10.1
extension-vehicle list and `[R-EXT-01]`) — checked every citation walker A
gives (§10.1's vehicle list at A:1580-1594 / B:1454-1465 via grep hits on
"New ignore-lane flag bits"; `[R-EXT-01]`'s closing text; the five mentions
of the incompat lane in each file) against edition B: **identical in every
respect** (§10.1's vehicle 3 reads "New ignore-lane flag bits in the
trailer (§6.3)" in both, never "incompat"; `[R-CNT-24]`'s "may redefine...
the remaining 48 trailer bytes" is identical in both). Walker B's own
transcript reports zero findings and does not raise this point even though
the condition it describes is equally present in B's text. This is not a
fidelity divergence (**EQUIVALENT** - see cmp-reader-03): it is a
difference in how thoroughly each walk searched, not in what the two
editions say.

**readerb** reported zero findings. I checked its explicit statement that it
"found no place where two passages bearing on the same act disagreed" by
re-deriving every one of the specific comparisons it names (§19.1 vs §6.4
for R1; §6.3 vs §21.6 for R2; §17.2/§17.4/§2.3 for R3; §15.2/§15.3/§16.2/
§9.7 for R4; §7.1/§2.4 for R5; §5.1/§19.1 for R6; §11.2/§11.4/§14.1/§14.2
for R7; §2.3/§20.4/§21.6 for R8) and found walker B's internal
cross-checks accurate wherever I independently re-opened the cited
passage.

## Forced guesses / re-derivations (charter item 4)

Walker B, under R6, explicitly reports needing to independently verify
something the text does not say directly: "I checked this because I
expected F5 might be a fifth 'reaches-every-major' row and wanted to see
whether the document says so; it does not name F5 among the four... I
[worked out] this is because `[R-CNT-27]`'s check needs no byte of the
file's content." I traced this to a real textual absence: edition A's §2.3
carries a Note (A:285-296) working exactly this reasoning by hand over
three named rows (F14 reaches; F5 does not reach; F15 does not reach
despite citing `[R-CNT-24]`) immediately after `[R-CNF-13]`'s definition.
That Note is **entirely absent from edition B** (confirmed: zero hits for
"F14 reaches" or "does not reach" in B's §2.3 region; the only "does not
reach" hits in B are at lines 1386/1420, an unrelated §9.7 coverage-walk
passage). Walker A, reading edition A, had this reasoning handed to it and
did not need to re-derive it; walker B, reading edition B, had to do the
work itself (and, by its own account, "checked this because I expected..."
- a guess edition A does not force). See Finding cmp-reader-02. The
byte-level test comes back negative because B's §21.2 opening paragraph
*states the conclusion* ("Deriving it there yields F8, F14, F6 and both of
F1's instances... and no other row") identically to A's, so no
implementation built from either edition differs in which register rows it
treats as reaching another major — but a careful implementer of B must take
that sentence on faith or re-derive it themselves (as walker B did),
where A's reader is shown the derivation.

## Beyond the probes (charter item 5): sections read side by side in full

- §2.3 Conformance classes, both editions, in full (A:152-296, B:206-297).
  Found: (a) the F14/F5/F15 Note gap above; (b) A's "Conforming TARN file"
  bullet (A:166-179) names four specific writer-conduct-only cases
  ("where a value is published...", the ignore-lane flags case, the
  pre-trailer-gap case, the §20.3-step-4 case) that B's corresponding
  bullet (B:218-222) compresses to the general rule without naming them;
  A's own text frames these as "declared where it arises rather than
  enumerated here," i.e. a convenience index rather than new content. I
  spot-checked one (the ignore-lane-bit conduct rule) at §6.3 in both
  editions and found it unchanged and present in both outside §2.3,
  supporting EQUIVALENT rather than LOSS, but I did not individually
  re-verify all four named cases at their own sections in both editions, so
  I report this with lower confidence than cmp-reader-01/02 and flag it as
  AMBIGUITY-leaning-EQUIVALENT rather than a clean verdict. (c) B drops
  A's parenthetical explaining why an unimplemented top-level MU=1 type in
  a conforming file is "necessarily... experimental range" (A:182-184); the
  underlying fact (F35/F36 making reserved-range + MU=1 a violation
  regardless) is stated identically elsewhere in both editions' register
  (verified: F35/F36 text is byte-identical, see above), so this is a
  dropped restatement, not a dropped rule. **EQUIVALENT**, not reported as
  a separate numbered finding beyond the note above.
- §2.4 Outcome classes, both editions, in full: byte-identical reject-file/
  reject-layer/reject-tile/ignore-record table text (A:307-311, B's
  equivalent), confirmed by direct quotation both directions.
- §15.1-15.4, §16.2 in full, both editions (the sections the commit log
  names as hand-edited for "Readable"): §15.1-15.3 identical in substance
  (one synonym swap, noted under R4); §16.2's slab-scope block is
  restructured from a "Note" to a "Rationale" (A:2421 "> **Note - what
  slabs are, and are not.**" vs B:2301 "> **Rationale.**"), with the
  content preserved and one sentence of added connective rationale ("A_slab
  adds alignment for direct I/O at each run's start") that restates, rather
  than adds to, what `[R-SLB-02]`/`[R-SLB-03]` already state earlier in the
  same section in both editions. Since both Note and Rationale are
  non-normative blocks under `[R-CNF-01]`, and no normative content moved
  into or out of either block, this re-labeling has no fidelity
  consequence. **EQUIVALENT.**
- §17.2-17.4 in full, both editions: identical in substance; this matches
  the commit log's own description of the §17.4 pass as "re-wrapped, no
  word changed." This is also where Finding cmp-reader-01 lives (identical
  text, one walker misread it).
- §6.2-6.4, §7.1-7.2, §19.1-19.4, §5.1, §11.2/§11.4, §14.1-14.2, §21.2
  register tables (F1-F36): read in full in both editions per probe; no
  further divergence found beyond what is logged under each probe above.

## Findings

See structured findings cmp-reader-01 through cmp-reader-03 in the
returned result. Summary:

- **cmp-reader-01 (REPORTER_ERROR, high confidence).** R3 / readera-01.
  §17.4's `[R-COD-11]` sentence resolving the core-codec-capability
  question for an ordinary reader is present, word for word (modulo
  rewrapping), in *both* editions, at the exact line range walker A itself
  cites. Walker A's transcript quotes only the verifier half of the
  passage and asserts the reader half does not exist; walker B, reading
  the same sentence in edition B, found and used it correctly. This is not
  an edition difference at all — both texts decide R3 identically — so it
  is REPORTER_ERROR rather than LOSS or AMBIGUITY, and I classify it as
  such even though the brief's probe answers present it as if it reflected
  a textual divergence between A and B.
- **cmp-reader-02 (OBSERVATION, byte_level: false).** Edition A's §2.3
  carries a worked Note deriving, example by example (F14/F5/F15), why
  `[R-CNF-13]`'s "reach" test yields the specific rows §21.2 then names;
  edition B states the same conclusion but omits the worked derivation
  entirely. No register row's outcome differs between editions (both
  state "F8, F14, F6 and both of F1's instances... and no other row"
  identically), so no implementation built from either edition diverges in
  behavior — but walker B's transcript shows it having to re-derive, for
  itself, exactly the reasoning A's Note spells out, which is the kind of
  forced-guess divergence charter item 4 asks me to report.
- **cmp-reader-03 (EQUIVALENT, not a fidelity defect).** readera-02's
  incompat-lane OBSERVATION is supported identically by both editions'
  text; walker B simply did not report it. Recorded for completeness, not
  as a loss or addition.
