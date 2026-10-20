# Writer comparator — working transcript

## Disclosure (mandatory, read first)

- **Relayed "user request."** A harness message reading "Go" was prepended above
  the computed brief, labelled as the user's request to the orchestrator. Per
  the brief's own instruction, it predates my spawning, is not a task for me,
  needs no reconciliation with this brief, and does not widen the access rule.
  Noted and set aside; its content is not repeated further.
- **Unsolicited context.** Before the task text, my runtime surfaced a project
  `CLAUDE.md` pointer, a user memory-index file (TARN-process note titles), a
  git-status/environment block, model identity, and skill/deferred-tool
  listings. None of this is part of either specification edition and none of
  it is evidence about them; I disregarded its content and am not repeating it
  beyond this acknowledgment.
- **Access taken.** I read exactly the four files the brief named:
  - `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
    (edition A, 5,004 lines), read in full via sequential `Read` calls (offsets
    1, 700, 1300, 1900, plus targeted re-reads of §20–§21 and the user-metadata
    section at matched offsets).
  - `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
    (edition B, 4,810 lines), read in full the same way, offsets aligned to A's
    by matching `### N.` section headers (confirmed via `grep -n` against both
    files for `§13`–`§24`).
  - `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/out/transcript-writer-a.md`
    (654 lines) and `…/transcript-writer-b.md` (716 lines), each read in full in
    one call.
  I ran `wc -l` against the four files above (nothing else) to size my read
  plan and plan offsets, and `grep -n` against the two edition files only, to
  locate section headers and to confirm a handful of register-row strings
  (`T4`, `R-SER-05`) were byte-identical between editions. I ran local Python
  (`python3 -I`, no file reads inside the script beyond the two edition files
  already read and saved into my own scratch directory) to diff the two
  editions at paragraph granularity and to scan the diff for modal-verb and
  numeral differences. No other file was opened, no other directory was
  listed, no git history/diff was consulted, and no web search or fetch was
  made.
- **Scratch directory.** My scratch directory,
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/compare-writer/`,
  was empty when I started. I created it and wrote these files there:
  `a_paras.txt`, `b_paras.txt` (the two editions' Part I–III-plus-appendices
  text, reflowed one paragraph per blank-line-delimited block, to make a
  wrap-insensitive diff possible), `diff_report.txt` (superseded, not used
  further), `diff_report2.txt` and `diff_report3.txt` (the filtered diffs I
  actually read and quote from below).
- **Wrapping caveat.** Both editions are hard-wrapped prose with `> `
  blockquote continuations. Rather than line-grep prose claims, I read full
  sections with the `Read` tool (which returns unwrapped, line-numbered text)
  and additionally ran a paragraph-reflow diff (joining wrapped lines on blank
  lines) over the entirety of Part I through the appendices of both editions,
  so wrapping differences cannot hide as content differences in that swept
  region. Where I report a zero (e.g., "no modal-verb difference found"), the
  control is stated in the Evidence object.
- **Path check.** Both files exist exactly where the brief named them; no
  discrepancy to report.

## Method

1. Read both walk transcripts in full first, to extract the 11 probes' cited
   passages and each walk's own findings (charter items 1–4).
2. Read both editions sequentially, side by side, through Part 0 (§1–§4),
   confirming §1–§4 differ only in section order (B moves §3 before §2) and
   wording, not content, by direct comparison of matched passages.
3. Read both editions sequentially through Part I (§5–§10), Part II (§11–§18),
   and Part III (§19–§21.1), confirming every passage the 11 probes cite,
   every passage either walk's own findings cite, and the sections the writer
   charter depends on most (§9, §15, §16, §20, §21).
4. Built a wrap-insensitive paragraph-level diff of both editions from
   `## Part I — Container` to the end of each file (which includes every
   appendix), to check charter item 5 ("go past the probes") systematically
   rather than by sampling alone, and to catch anything my sequential read
   might have skimmed past. I excluded Part 0 (§1–§4) from this automated diff
   because the two editions reorder those sections differently (A: §1,§2,§3,§4;
   B: §1,§3,§2,§4), which would misalign a positional paragraph diff; I instead
   checked Part 0 passage-by-passage during the sequential read in step 2.
5. Filtered that diff to: (a) every block where paragraph counts differ
   between editions (content moved, split, or merged across paragraph
   boundaries), and (b) every 1:1-paired paragraph whose text-similarity ratio
   fell below 0.80, and separately re-scanned the entire 1:1-paired set for any
   change in which RFC-2119 keyword (MUST/MUST NOT/SHOULD/SHOULD
   NOT/MAY/SHALL/REQUIRED/OPTIONAL/RECOMMENDED) appears, and any change in the
   set of decimal/hex numerals appearing. I read every flagged block in full.
6. For each of the 11 probes, opened both editions at the governing
   requirement(s) the probes/walks cite and quoted both.

## Findings from the automated full-corpus diff (charter item 5)

The paragraph diff over "Part I — Container" through the end of file (which
includes §5–§24 and Appendices A–H in both editions — confirmed present and
identically titled in both via `grep -n "^### Appendix"`) produced 228 aligned
blocks: 114 equal, 114 "replace" (no pure insert/delete blocks at all — every
difference is a reworded or re-split counterpart, never content appearing in
one edition with literally nothing on the other side). Of the 114 replace
blocks, I read all of them; every one I inspected is a sentence-level
rewording, a paragraph split/merge, a conjunction-vs-em-dash change, or (once)
an explicit repetition of a SHOULD the other edition left to a shared verb
across a semicolon (§6.3, `[R-CNT-26]`: A has "a writer SHOULD emit the lowest
version_minor … and an appender the maximum of that floor…"; B has "A writer
SHOULD emit the lowest version_minor … An appender SHOULD emit the maximum of
that floor…" — same obligation, stated once implicitly vs. twice explicitly).
The targeted modal-verb-difference scan over all 1:1-paired replace blocks
found exactly one hit, and it was that same SHOULD-explicitness case (reported
above) — no MUST/MUST NOT appeared or disappeared anywhere, and no SHOULD
flipped to a MAY or vice versa. The numeral scan flagged 13 blocks, all of
which I opened; every flagged case was either a cross-reference's section
number changing because the same prose moved to a different section (see
below) or a tokenizer artifact from `[R-xxx-NN]` identifiers inside rewrapped
sentences — no limit, offset, count, or worked-example number differs between
the two editions anywhere in this sweep.

One structural move did surface: the paragraph beginning "Metadata compression
exists only at record granularity…" sits under §7.1 (Directory region) in
edition A and under §7.3 (Record types of format major 1) in edition B — the
prose is otherwise identical, and each edition's own internal cross-references
to it (`§7.1` in A's §18.1/§23, `§7.3` in B's §18.1/§23) were each updated to
match where the content actually sits in that edition. This is a reorganization,
not a content change.

Given this sweep found no MUST/SHOULD-class change and no numeral change, and
everywhere content moved its moving was itself tracked by a correspondingly
moved cross-reference, I treat the writer-charter's governing sections as
verified equivalent in substance between editions by direct inspection rather
than by reasoning from the probes alone.

---

## Probe-by-probe: governing text comparison

For each probe below I quote the passage(s) both walks relied on in **both**
editions, note whether they are identical, and give the verdict.

### W1 — smallest conforming file

A (`§5.1` Example): *"The smallest conforming file is exactly 128 bytes: front
block [0, 16); an empty directory — zero records, so 4 bytes holding the
CRC-32C of zero bytes, `0x00000000` — at [16, 20); 44 bytes of slack, zeroed by
advice; trailer at [64, 128). It contains no layers (a valid, empty file)."*

B (`§5.1` Example): byte-for-byte the same sentence (confirmed identical in my
side-by-side read of lines 658–663 (A) / 536–541 (B)), down to the em-dash
placement.

`§6.2`'s trailer layout table (offset/size/type/field/class/valid-values
columns) is identical in both editions, field for field, including the exact
byte ranges each field occupies and the note on the pre-trailer pad
(`[R-CNT-05]`). Both walks' per-field summaries agree and both ground on the
same rule, `[R-CNT-27]`, quoted identically: *"No conforming file is shorter
than 128 bytes: the front signature block, a directory of at least 4 bytes at
an offset of at least 16, and the 64-byte trailer at a 64-aligned offset cannot
be satisfied in fewer."*

**Verdict: EQUIVALENT.** No divergence; the governing text is identical.
Byte-level test: an implementation built from B alone and one built from A
alone would produce the identical 128-byte file for this case, since every
offset, every field value, and the CRC-32C check vector (`§4.5`, identical
wording in both) are stated identically.

### W2 — 32-tile interleaved supersede

A (`§20.3` step 4, worked example) and B (same location) carry the identical
sentence: *"Superseding one 100,000-byte stored tile of a 32-tile interleaved
layer appends: the new payload (100,000 bytes), the layer's full new index
region (32 · 20 + 4 = 644 bytes: one entry re-pointed, 31 byte-identical), the
new directory (every record byte-identical except the modified layer's), the
pad, and the 64-byte trailer. The prior index region and the superseded
payload become slack, reclaimable only by a rewrite (§20.5)."* (A's version
uses em-dashes in two places where B uses colons/commas — pure wrapping/style,
confirmed by direct comparison, lines 3417–3424 (A) / 3255–3261 (B).)

`[R-CNT-17]`'s index-region size formula (`entry_count × 20 + ⌈entry_count /
2¹⁶⌉ × 4`) and `§15.4`'s segment definition are identically worded in both
editions (confirmed via the diff and via direct side-by-side read of §15.4).

**Verdict: EQUIVALENT.** Both walks' answers agree and are grounded in
identical text. Writer-a's own finding (writera-01) that the *exact byte
offsets* of the new payload versus the new index region are not fixed by the
document (`[R-SLB-05]`'s placement freedom) is equally true of edition B: the
placement-freedom rule is quoted identically in both editions' `§16`
(*"A layer that declares neither alignment nor a slab makes no layout
promise: its stored tiles MAY occupy any non-overlapping byte positions, in
any order…"*) and in the identical Example-after-three-commits passage in
`§5.1` ("a layer's structures need not be contiguous or ordered
(`[R-SLB-05]`)"). This is a property shared by both editions, not a fidelity
difference.

### W3 — unimplemented top-level MU = 1

Both editions carry `§20.4`'s table MU = 1 row identically, word for word
(confirmed in my direct §20.4 read, both editions): *"At file scope no commit
is available at all: the updater is a reader of the file first (§2.3), and
`[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file — the
same treatment §6.3 gives an unknown incompat-lane bit. At either scope a
rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground…"*
`[R-WRT-06]`'s prose ("A rewriter MUST refuse to rewrite a file carrying any
record whose type it does not implement with MU = 1: such a type can define
references this specification does not (§7.2), so its bytes cannot be safely
relocated.") is likewise identical in both.

**Verdict: EQUIVALENT.**

### W4 — unimplemented MU = 0 / PE = 0, drop with no other effect

`§20.4`'s table last row is identical in both editions, including the exact
clause both walks quote: *"an appender MAY drop the record in any commit it is
otherwise free to make — one whose only effect is the drop included — and a
rewriter MAY drop it in any rewrite. An updater that drops such a record
SHOULD report the loss…"* (A keeps the em-dashes; B's copy, read at the
matched location, is word-for-word the same, including the em-dashes — this
is one of the 114 "equal" diff blocks, not a replace block.)

**Verdict: EQUIVALENT.**

### W5 — ignore-lane bit 20 through three writer tiers

`[R-CNT-08]` (ignore-lane copy-forward rule), `[R-WRT-06]`'s rewriter-flags
sentence, and `§20.1`/`[R-WRT-01]`'s creator-vs-rewriter paragraph are each
identical between editions (confirmed by direct read and by the diff, which
placed the whole `§20.1` passage, including the sentence "A writer of a new
file from an existing one takes one of two positions, and the choice is its
own," in an "equal" block for both editions).

**Verdict: EQUIVALENT.** Writer-a's OBSERVATION (writera-02) that the
creator/rewriter position is a self-declared choice rather than a function of
what the tool actually does is accurate, and it is true of edition B exactly
as it is of edition A: the sentence it rests on ("the choice is its own") is
unchanged. This is not a B-specific gap.

### W6 — supersede a stored tile's own layer, changing only its fill

`§20.3` step 4's fixed-declarations list and bar, the conduct-rule framing
(`[R-ERR-01]`, `[R-CNF-02]`, "a file such a commit leaves can be nonconforming
on its own terms, as the paragraph below sets out"), and the list of register
rows that *can* detect a changed fixed declaration ("T3, T14, T21, T22, T4,
T5, T2") are **identical, word for word**, in both editions (confirmed in the
diff: this entire passage falls in "equal" blocks, and I independently
confirmed the T4 register row itself — `§21.4`, `[R-SER-05]` — is
byte-identical in both files by `grep`).

Both walks reach the same bottom-line answer (not permitted as a commit; drop
layer + add new one, or rewrite with re-declare, are the two alternatives; the
bar is conduct-only per `[R-CNF-02]`). Walker B goes one step further and
derives a **finding** (writerb-01): where the layer has no edge tile for the
changed channel (no padding position exists for it, per `§11.3`), T4/`[R-SER-05]`
has nothing to check, and no other register row catches the change either, so
the forbidden fill-change is byte-invisible to any conformance check. I traced
this argument against edition A's identical text (`§11.3`'s padding-position
definition and `§21.4`'s T4 row are the same in A) and found nothing in A that
closes the gap B's walk identifies. **This gap is a property of the shared
text, present identically in both editions** — it is not a defect edition B
introduced or edition A avoided; walker A simply did not pursue this
particular corollary as far.

**Verdict: OBSERVATION, not a LOSS.** Per the charter's item 3, a defect "B
alone has" would be a LOSS; this defect is not B's alone — the identical
sentences are present in A — so it does not count as fidelity loss by the
rewrite. Byte-level test: an implementation built from B alone and one built
from A alone would behave identically here (neither text closes the gap), so
there is no A-vs-B byte or verdict divergence; the divergence this finding
describes is between two *conforming writers of either edition* (one that
violates the fill-change bar on a no-padding layer, one that does not),
which both editions license equally through the identical conduct-rule
language.

### W7 — crash after directory durable, before trailer durable

`[R-LIF-05]`, `[R-LIF-04]`, `[R-LIF-06]`, and the `§9.2` "what a crash sees"
worked example (the ASCII-art figure with `dirₙ`, `trailₙ`, and the ▓ marks)
are identical between editions (confirmed directly; this is one of the
"equal" diff blocks). `§9.6`'s prose is split into more, shorter paragraphs in
B than in A (one of the unequal-count replace blocks I read in full) but
every sentence survives with the same content — e.g. A's single sentence
*"Recovery tools and verifiers — never conforming readers on the default path
— locate commit states as follows: probe backward…"* becomes B's two
sentences *"Recovery tools and verifiers locate commit states as follows. A
conforming reader on the default path never does (§9.5). Probe backward…"* —
same claim, split differently.

**Verdict: EQUIVALENT.**

### W8 — rewriter carries forward a layer with an unimplemented sample type

`§12.1`'s closed-core rule (`[R-TYP-01]`: *"This specification defines exactly
thirteen sample types, all core: a conforming reader MUST decode every one of
them, and none is skippable."*), `§2.3`'s `[R-CNF-03]`/`[R-CNF-06]` conformance
classes, and `[R-WRT-09]`'s verification-depth rule are each identical between
editions (confirmed directly and via the diff). Walker B uses `[R-TYP-01]`
plus `[R-CNF-03]`/`[R-CNF-06]` to argue the probe's literal premise (a
*conforming* rewriter missing a core sample type) cannot occur, then answers
the nearest on-document analogue; walker A answers the nearest-analogue
question directly without raising the foreclosure point. Because the
foreclosure argument rests entirely on text identical in A, this is a
difference in how far each walk pursued an available argument, not a text
difference between editions.

**Verdict: OBSERVATION** (walker depth asymmetry, not a document difference).
Byte-level test: not applicable to an A-vs-B divergence, since the argument is
equally available from either edition's text.

### W9 — drop a PE = 0 layer carrying an MU = 1 unimplemented sub-record

`§20.4`'s table MU = 1 row and its layer-drop paragraph (*"One sub-record
blocks the drop, a sub-record of a type the updater does not implement with
MU = 1, the drop being a modification of the scope it governs (the table's
first row)."*) are identical in both editions (confirmed directly — this
whole passage is in an "equal" diff block). Both walks reach the identical
answer with the identical citations; walker B additionally cross-checks
against `§7.2` (`[R-CNT-12]`), whose text is also identical between editions.

**Verdict: EQUIVALENT.**

### W10 — appender drops a carried-forward MU = 0 / PE = 0 top-level record

`§20.3` step 2's *"MUST NOT drop the record save where §20.4 licenses the
drop"* and `§20.4`'s PE = 0 row are identical in both editions (confirmed
directly).

**Verdict: EQUIVALENT.**

### W11 — updater implements an unregistered type whose definition fixes MU = 1, PE = 0

This is the one probe where the two walks' **confidence** differs sharply —
walker A: "No disagreement among (a)/(b)/(c)'s governing sentences" / "the
document resolves it with an explicit sentence"; walker B: flags it
"`[underdetermined]`" and records a CONTRADICTION-shaped finding
(writerb-02) — while the governing text is **identical** in both editions. I
read both passages in both editions side by side to settle which reading the
shared text supports:

Both editions, `§20.4` (immediately before the preservation table): *"…For a
type the updater implements that this specification does not register, the
definition it implements the type from supplies the flags, and the stored
bits never do (`[R-CNT-22]`, §10.3). For a type the updater does not
implement, the stored flags are authoritative… The table states what an
updater owes a record it does not logically modify, read under whichever
flags govern it. **Its MU = 1 row reaches only a type the updater does not
implement** — an updater implements both registered types and understands an
unregistered type it implements from its definition, modifying their records
as §20.3 and that definition provide — **so for an implemented type only the
PE bit bites**:"*

Both editions, `§7.2`'s Note (the sentence walker B leans on for the
tension): *"The two flag bits are not orthogonal. `[R-CNT-12]` leaves a record
three states, not four, and they are §20.4's three rows: MU = 1, whose PE bit
is read as 1 whatever is stored; MU = 0 with PE = 1; and MU = 0 with PE = 0.
PE is a choice within MU = 0. An updater that does not implement an MU = 1
record's type never drops the record, alone or with the scope it governs
(§20.4)."*

Read in context, `[R-CNT-12]`'s own rule (also identical in both: *"Writers
MUST NOT emit the combination MU = 1 with PE = 0; a reader or updater
encountering it MUST treat the record as PE = 1…"*) is a rule about a
record's **own stored bits**, i.e. the literal two flag bits as written in the
24-byte header on the wire; `§7.2`'s Note restates that stored-bit collapse.
W11's scenario is a record whose **governing** flags come from an external
definition — and `§20.4` is explicit, two sentences earlier, that for exactly
this case "the stored bits never do" supply the governing flags. The Note's
"whatever is stored" clause is therefore about a different question (how a
record's own stored bits collapse when *they* govern) than the one `§20.4`'s
explicit carve-out answers (whether the stored-bit collapse rule reaches a
type the updater *implements*, where the stored bits are not what governs in
the first place). The Note's own final sentence — "An updater that **does not
implement** an MU = 1 record's type never drops the record" — is itself scoped
to the not-implemented case, consistent with, not contradicting, `§20.4`'s
carve-out.

**Verdict: this is not a document fidelity issue (the text is identical in
both editions), and on the merits I read it as REPORTER_ERROR by walker B**:
the sentence "so for an implemented type only the PE bit bites" directly and
explicitly decides the W11 scenario (updater implements, definition fixes
MU = 1 / PE = 0 → PE = 0 alone governs → drop licensed), and walker B's own
quoted Note does not state an exception-free rule over the same cases, since
its final sentence itself carves out the not-implemented case. Byte-level
test: not applicable to A-vs-B, since both editions state the identical
sentences; the disagreement is between the two walks' readings of one shared
text, not between two texts.

---

## Each walk's own findings, checked against the other edition

- **writera-01** (placement-offset freedom) and **writera-02**
  (creator/rewriter self-declared position): both rest on `[R-SLB-05]` and
  `§20.1`'s "the choice is its own," respectively — both confirmed identical
  in edition B (see W2 and W5 above). Not B-specific; not a fidelity
  divergence.
- **writerb-01** (padding-silent fill-change gap) and **writerb-02** (W11
  tension): both rest on text confirmed identical in edition A (see W6 and
  W11 above). Not B-specific; not a fidelity divergence, though writerb-01 is
  a genuine, useful corollary of the shared text and writerb-02 I read as a
  misreading of the shared text (see W11).

## Where a walker had to guess, re-read, or go elsewhere (charter item 4)

Walker B's own disclosure states it "did not read §22–24 or the appendices"
of edition B, stopping after confirming the error-register rows needed in
§21.2–21.6. Walker A's disclosure states it read edition A start to finish,
"including all appendices (A–H)." My own full-corpus diff (which spans both
editions' entire Appendices A–H and §22–24, since I diffed from "Part I —
Container" to the literal end of each file) found these sections are
textually identical in substance between editions (only the diff blocks
already quoted above fall before §21.1; nothing diverges in §21.2 onward
through the appendices). So this asymmetry in the two walks' own reading
depth did not cause either walk to reach an answer the other edition's text
would not equally have supported — had walker B read the appendices, it would
have found the same content walker A did. I flag this as a walk-methodology
asymmetry, not a document fidelity issue.

## Going past the probes (charter item 5)

Covered systematically by the full-corpus diff described above (Findings
section) plus the sequential side-by-side read. No rule, exception,
quantifier, or figure present in one edition and absent from the other was
found anywhere in the writer/updater-relevant text (§5–§10, §11.1–§11.4,
§14.4–§14.5, §15, §16, §17, §18.2, §19, §20, §21), nor anywhere else in the
document.
