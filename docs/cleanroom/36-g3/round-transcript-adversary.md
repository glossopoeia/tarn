# Adversary transcript — Cleanroom round 36

## Access and setup

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in five
sequential `Read` calls covering lines 1–4981 (the whole document; `wc -l` confirmed 4981 lines
before I began, matching the brief's stated size). I ran `grep` against that same file only, four
times, to check specific textual questions (listed below under "Sweeps run"). I ran `mkdir -p` to
create my scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-round/scratch/adversary/`);
it was empty when I created it, so there is no prior attempt's material beside which I am working.
I wrote no scratch files into it — every check I ran was either a `grep` against the one permitted
file or arithmetic I did by hand in this transcript, so there was nothing to persist there. I did
not list or read the shared output directory at any point; I only ever wrote to my own single
output file. I did not read `AGENTS.md`, any file under `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`,
`README.md`, `CONTRIBUTING.md`, anything under `conformance/`, or `spec/registry.json`. I ran no
`git` command and did no web search or fetch.

**Contamination disclosure.** Before this task's instructions arrived, my context already
contained a project `CLAUDE.md` (a one-line pointer to `AGENTS.md`, which I did not open), a
user memory file listing about twenty short titled notes whose titles reference "TARN" rounds,
gates, wordlists, harness paths, and similar round-infrastructure topics, and a git-status block
naming recent commit messages from this repository's history (mentioning "ADR-0129", "ADR-0130",
"cleanroom round 36", an "erratum E3", and other round/ADR labels). None of this is part of the
specification and I have treated none of it as evidence about the specification's text. I did not
open any of the memory's linked files, did not read the named ADRs, and did not let the commit
messages' hints about what changed (checksum duty, writer tiers, a registry constant) steer which
passages I trusted or distrusted — I verified everything I report below against the spec text
itself, independently, and would have reported the same things had that context been absent. I am
naming that it appeared, per the brief's instruction, without repeating its contents beyond what is
above.

The one path the brief named was exactly where the file was; no path discrepancy to report.

## First pass — full read

I read the document straight through, section by section, before attempting any construction. I
paid special attention to the thirty-one listed passages, but read everything else too, since the
brief and this project's own history are explicit that survivors have repeatedly turned up in
unlisted text. Below I record the reasoning that survived — the suspicions I opened and closed are
under "Rejected candidates," and the checks I actually ran are under "Sweeps run" and "Derived
numbers."

## The convention check (§2.1, [R-CNF-01])

The brief specifically warns that the blockquote marker `>` is not itself the exemption — only a
*label* (Note/Example/Rationale) or a non-normative appendix is. I went looking for an unlabeled
blockquote carrying normative content, since the brief says at least one exists and a prior
briefing in this project got this backwards.

I grepped `^> \*\*` (a blockquote whose first line starts with a bolded word) and got every
blockquote's opening line. Every one of them opens with **Note**, **Example**, or **Rationale**,
or is a lettered continuation — `(a)`, `(b)`, `(c)` — inside an already-labeled Example block. That
sweep alone would suggest no unlabeled blockquote exists, which would make my check pointless
before it started — exactly the "search that could not have succeeded" trap the brief warns about,
since a grep anchored on `\*\*` cannot find a blockquote that never carries a bold label in the
first place. So I went back to the full text I had already read looking for `>` lines with no
label anywhere nearby, rather than trusting the negative grep.

I found one: §15.1, in the middle of otherwise fully normative running text defining the tile-index
region's byte layout, the specification drops into an unlabeled blockquote to draw the layout:

> Under index_encoding 1 (the only encoding this format major version defines, §7.4), the
> tile-index region addressed by the layer record's extent slot is, contiguously:
>
> > [ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]
>
> with no padding anywhere inside the region.

Under [R-CNF-01]'s literal test (label, not markup), this is normative: it carries none of the
three labels, and §15's region is not among the appendices the exemption reaches. Its content adds
nothing beyond what [R-IDX-01] (20-byte entries, disk-ordinal order) and [R-CNT-17] (the
extent_length formula, which already fixes where the segment-CRC array starts and how long it is)
already establish in ordinary prose, so no implementation can read the diagram and reach a
different byte layout than one that reads only the surrounding sentences — this is a documentation
risk, not a byte-level fork, and I record it as Finding adversary-01 on that basis.

## Working the three decisions and the writer-tier restatement

I re-read §20.1–§20.5 several times, holding a concrete tool in mind each pass, per the brief's
instruction to "take a concrete tool and ask of every sentence that classifies it what the tool
then owes."

**Tool A — a naive `cp`-style duplicator.** It opens an existing conforming file, decodes nothing,
and writes a byte-identical copy elsewhere with a different name. Is it a creator or an updater? It
extends no existing file under that file's file_id (it starts a brand-new file at a new location),
so §20.1's "a writer that extends an input file is an appender and an updater, whatever it decodes"
does not capture it — it never *extends*, it *writes a new one*. So it falls under "a writer of a
new file from an existing one," and "the choice is its own": it may declare itself a creator (undertaking
nothing toward its input, writing flags = 0 per §6.3/§20.2) or a rewriter (carrying the input's
ignore-lane bits forward per [R-WRT-06], and answering to [R-WRT-09]'s verification depth for
every byte it copied). I worked through whether this creates two different sets of *conforming
bytes* for what looks like the same operation (see "Rejected candidates" below, item 1) — it does
not, because [R-CNF-02] expressly carves the flags-value conduct rule out of file-conformance:
an ignore-lane bit is conforming set or clear regardless of which duty the actor undertook, so the
two "positions" can produce different trailers but never a nonconforming one on that account alone.

**Tool B — an appender that drops a stored-tile layer and adds a same-named replacement in one
commit.** §20.3 step 4's fixed-declarations bar explicitly reaches only "a layer the commit keeps,"
and separately licenses "a commit MAY drop the layer (§20.4) and add a new one under its name and
other declarations, the new layer being new whatever bytes its entries address, the dropped layer's
former extents included." I checked this against [R-ENC-15]'s name-uniqueness rule and against
[R-CNT-13]'s extent-ownership rule: since drop and add resolve into one final directory carrying
only the new record, there is no duplicate name in the live state, and the new layer's tiles/index
are placed at fresh offsets while the old ones fall to slack — no overlap. This reads as
consistent and deliberately anticipated (§20.4's closing sentence: "A dropped layer's name is free
to the same commit and to any later one").

**Tool C — a rewriter regenerating a slab-declared, planar layer whose channel list it also
shortens.** I checked whether §16.2's run-partition rule ("runs never span channel blocks") and
§20.3 step 4's re-emission clause compose correctly when a channel is dropped from the end. §20.3
step 4 states the region is re-emitted under the clause "whether or not entry_count changes with it
... and whether or not a retained ordinal moves," and separately (same section) "a slab declaration
declared, changed or kept has its invariants satisfied over every run of the new state, the runs
this commit adds included, or is cleared." Both cover the shortening case: the removed channel's
block simply stops being addressed, and no retained run needs to reach across the old boundary.

**The PE = 0 preservation-licence sentence.** Working Tool A and Tool B forward through §20.4's
table, I noticed the licence sentence states the drop permission twice — once for "an updater," once
for "a rewriter" — inside one sentence, but "commit" is specifically the appender's unit of
operation (§9.2), and §20.5 is explicit that "a rewrite is not a commit." Read at face value, "an
updater MAY drop the record in any commit it is otherwise free to make" assigns a commit-shaped
permission to the whole updater class (appender and rewriter both), when only the appender tier
ever performs a commit — exactly the actor-name/operation conflation the brief's second shape warns
against. I traced whether this actually licenses or forecloses anything incorrectly: it does not,
because the same sentence's second clause independently and correctly licenses "a rewriter... in
any rewrite," so between the two clauses both real operations are covered, and neither tier is
denied a drop it should have or granted one it should not. I record this as Finding adversary-02:
an imprecision in the operation/actor phrasing that this round's own brief singles out as the shape
to look for, but one that does not move any byte or verdict, since the surrounding sentence and the
rest of §20.4/§20.5 already state both tiers' actual permissions correctly and independently.

## Registry constant and "bar restated as a scope" (decision 3)

I checked every appearance of the layer record's and the user-metadata record's fixed MU/PE values
for consistency, since the brief flags a changed registry constant as this round's third decision.

```
grep -n "MU = 0, PE = 0\|MU = 0, PE = 1" spec/tarn.md
```
returned four lines: §7.3's table (both rows), §20.4's table (both rows), and Appendix C's
restatement. All four agree: `0x0001 layer` is MU = 0, PE = 0; `0x0002 user metadata` is MU = 0,
PE = 1. No drift between the registry table, the preservation table, and the non-normative
Appendix C snapshot.

I then reread the "permission with a warning" and "bar... what it binds and what it does not"
language the brief describes for this decision and matched it to text already in place: §20.4's
"A commit MAY therefore drop a layer record... An updater that drops such a record SHOULD report
the loss" (the permission-with-a-warning), and §20.3 step 4's "The bar binds a layer the commit
keeps and nothing else... What the bar removes is a re-declaration carried as the same layer over
the tiles it stored" (the bar restated as a scope, separating "re-declare in place" from
"drop-then-add," which I exercised as Tool B above). Both read as settled, not as leaving a gap.

## Numeric checks

**§21.8's instance count.** The register claims "120 conditions over 277 instances." I counted the
rows (F1–F10, F12–F36 = 35; L1–L49 = 49; T1–T26 = 26; R1–R10 = 10; total 120, matching — note F11
is deliberately struck, as §21.2's own note explains) and then counted every semicolon-separated
instance in every row's Instances column by hand, section by section:

- §21.2 (F-rows): 56 instances (F1=2, F2=5, F3=2, F4=1, F5=2, F6=2, F7=4, F8=1, F9=1, F10=1, F12=1,
  F13=1, F14=1, F15=1, F16=1, F17=2, F18=1, F19=1, F20=1, F21=1, F22=1, F23=2, F24=1, F25=1, F26=1,
  F27=1, F28=2, F29=3, F30=2, F31=1, F32=1, F33=5, F34=1, F35=1, F36=1).
- §21.3 (L-rows): 116 instances (L1=8, L2=9, L3=1, L4=2, L5=1, L6=1, L7=2, L8=2, L9=2, L10=1, L11=1,
  L12=2, L13=1, L14=3, L15=4, L16=2, L17=2, L18=3, L19=1, L20=1, L21=4, L22=4, L23=4, L24=1, L25=1,
  L26=1, L27=1, L28=1, L29=3, L30=2, L31=3, L32=3, L33=4, L34=4, L35=1, L36=2, L37=1, L38=1, L39=3,
  L40=1, L41=3, L42=1, L43=3, L44=3, L45=3, L46=2, L47=2, L48=1, L49=4).
- §21.4 (T-rows): 55 instances (T1=1, T2=1, T3=6, T4=4, T5=1, T6=1, T7=2, T8=1, T9=1, T10=1, T11=2,
  T12=1, T13=2, T14=6, T15=2, T16=1, T17=1, T18=2, T19=1, T20=1, T21=3, T22=6, T23=1, T24=1, T25=3,
  T26=3).
- §21.5 (R-rows): 50 instances (R1=4, R2=2, R3=2, R4=16, R5=8, R6=4, R7=6, R8=4, R9=2, R10=2).

Total: 56 + 116 + 55 + 50 = **277**, exactly matching the document's own stated figure. This is not
a passage the brief lists as changed, so it is background verification rather than an attack on the
surface, but it gave me confidence that this register — which several of the listed passages lean
on by cross-reference — is internally arithmetic-consistent, and it is the kind of closed-count
check (shape 5) the brief asks for.

**§19.3's reader-detection checklist against §21.3's rows.** I went through every L-row whose
Detector is "reader" and Detected is "layer access," and confirmed each one's governing
requirement is cited (directly or via the requirement it is itself governed by) in §19.3's
enumeration of what full layer validation covers. All of them are — including the ones that reach
§19.3's citations only indirectly (L13/L14/L24/L26 via [R-CNT-18]'s "sub-record walk," L39/L45 via
the §7.4 value-set citation, which is the requirement [R-SLB-01]/[R-COD-09] themselves route their
outcome through). I found no L-row left uncited.

## Degenerate-but-legal constructions tried

- **Zero-extent, zero-addressed-tile layer with codec 4 (lz4) and extreme tile extents.** [R-COD-07]'s
  own note already states this is conforming ("an empty layer escapes only because that cap is
  quantified over addressed tiles"), and [R-ENC-04]'s overflow ceiling on P·Q/P·Bᶜ still applies
  "whether or not the layer addresses a tile" — so before the lz4 cap could even become interesting,
  extreme tile extents overflow the 2⁶³−1 ceiling and are rejected on that ground first. I could not
  build a file that reaches the lz4 cap question while also being degenerate in extent; the two
  checks are already ordered correctly against each other in the text.
- **entry_count exactly 65,536 (= 2¹⁶).** Segment count ⌈65536/65536⌉ = 1, and that one segment
  covers [0, 65536) exactly — a *full* segment, not a partial one, so [R-IDX-05]'s "final partial
  segment" language does not (and should not) apply here. No boundary confusion.
- **extent_length formula at entry_count = 0.** entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 already
  evaluates to 0 without the parenthetical "(and 0 when entry_count is 0)" — ⌈0/65536⌉ = 0. The
  parenthetical is mathematically redundant but not wrong; I treat this as a non-finding (see
  rejected candidates).
- **Smallest legal file (128 bytes, zero layers).** Cross-checked byte-for-byte against Appendix A's
  worked example and confirmed the trailer CRC and directory CRC values given there are internally
  consistent with the stated bytes (CRC-32C of zero bytes = 0x00000000 per [R-ENC-09]'s check
  vector, matching the directory region's stated 4 bytes).

## Rejected candidates

1. **"Creator vs. rewriter, choice is its own" as a byte-level fork on trailer flags.** I built the
   scenario in Tool A above: a tool that reads an existing file, discards all its structures, and
   emits a wholly unrelated new file, then asked whether declaring itself creator (flags = 0) vs.
   rewriter (carry forward the input's ignore-lane bits) produces two different *conforming*
   outcomes for the same bytes. It does not, because [R-CNF-02] explicitly lists "a creator's
   flags = 0, and an updater's copy-forward and set-no-other" among the writer *conduct* rules that
   never make a file nonconforming by their violation — and §21.6 independently confirms an
   ignore-lane bit, set or clear, is always a conforming file. The verdict on the bytes does not
   move; only a private conduct question about the tool does. Closed by [R-CNF-02]'s own carve-out
   list plus §21.6's ignore-lane row.
2. **A commit that both extends and shortens a planar channel list via a net-zero remove-then-re-add
   of the same channel.** §20.3 step 4's "an extension and a shortening of one channel list
   excepted" reads as a bright line regardless of whether the net effect is null. Closed by the
   sentence's own "whatever the counts" clause, which forecloses exactly this reading.
3. **Interaction of extent growth and channel-list extension in one commit, and whether the
   appended channel's new ordinals are computed against the pre- or post-growth N.** Closed by
   [R-GEO-06] and §20.3 step 4's ordinal-renumbering clause: ordinals are always a function of the
   *final* declared geometry of the generation being committed, never of an intermediate state, so
   there is only one N to compute against.
4. **F30/F31 vs. L15/L16 "half-zero" boundary at extent_offset = 0 exactly.** I checked whether an
   extent slot of (0, N) with N ≠ 0 could be double-counted under both the half-zero row and the
   into-the-front-block row. §21.1's own cross-reference paragraph resolves this by name ("a record
   extent slot of (0, N) with N nonzero reaches the block through its zero offset and is theirs
   [F30/L15's] rather than F31's or L16's"), and F31/L16 are textually restricted to
   extent_offset in 1–15, which 0 is not a member of. No overlap.
5. **Appendix C, G, and H (the three non-normative appendices on this round's changed-passage list)
   against the normative text they restate.** I cross-checked Appendix C's registry snapshot
   field-by-field against §7.3, §10.2, §11.4, §12.1/§12.2, §14.1, §17.2/§17.3, §18.2, and §18.4 —
   no divergence. I read Appendix G's ten reproducibility items against the SHOULDs and freedoms
   they each name as closing, and Appendix H's five per-class checklists against §2.3–§2.5, §19,
   §20, and §21 — in particular I checked Appendix H's "Conforming updater" paragraph, since it is
   the summary of the most heavily rewritten section, line by line against [R-WRT-03] through
   [R-WRT-09] and §20.4's table, and found it accurate including the [R-WRT-09] "every extent it
   copies" language (matching this round's first decision, the checksum-duty move from relocated
   structures to copied ones). No restatement I found disagrees with what it restates.
6. **Whether "the flags of the record type every file is built from" (this round's third decision)
   pointed at a divergence between §7.3's table and §20.4's table.** Already covered under
   "Registry constant" above; closed by the direct grep showing all four occurrences agree.

## Sweeps run

- `grep -n -i "duplicat\|clone\|copier\|compactor\|replicat" spec/tarn.md` — 8 hits, all ordinary
  uses of "duplicate" (names, keys); none is a stray old name for the rewriter tier surviving a
  rename.
- `grep -n "[Aa]n appender\|[Tt]he appender\|[Aa]n updater\|[Tt]he updater\|[Aa] rewriter\|[Tt]he rewriter\|[Aa] creator\|[Tt]he creator" spec/tarn.md` —
  71 hits; read every one in context to check for a sentence classifying one tier with an
  obligation only another tier can perform. Found the PE = 0 row's "updater... in any commit"
  imprecision (Finding adversary-02); found no other actor/operation mismatch.
- `grep -n "MU = 0, PE = 0\|MU = 0, PE = 1" spec/tarn.md` — 4 hits, fully consistent (see above).
- `grep -n "^> \*\*" spec/tarn.md` — 98 hits, confirming (by its *completeness*, not by finding a
  gap directly) that every labeled blockquote is properly labeled; used as a negative control
  against which I located the one unlabeled blockquote by re-reading rather than by grep, since a
  grep for a label cannot itself find an absence of one.
- Manual, full-document instance count against §21.8's stated "277 instances" (see Derived
  numbers) — one hit: exact match, 277 = 277.
- Manual cross-check of every §21.3 row with Detector = reader, Detected = layer access, against
  §19.3's citation list — one pass, no uncited row found.

## What I did not, and could not, fully verify

I did not attempt to enumerate every combination of §20.3 step 4's permitted per-commit changes
(name changes × extent growth × channel-list edit × slab/alignment edit, each MAY-or-not) against
every bound §20.3 step 4 lists (the lz4 cap, the 2⁶³−1 ceiling, the channel floor, the name rules) —
that is a large combinatorial space, and I instead worked concrete representative tools (A, B, C
above) through it rather than exhausting it. I did not build or hand-verify actual CRC-32C values
for any construction beyond confirming the two check-vector values already in the document
([R-ENC-09] and Appendix A) are self-consistent; I did not write an independent CRC implementation,
since none of my candidate attacks turned on a specific checksum's numeric value surviving or
failing. I did not exhaustively check that every one of the register's 277 instances has language
elsewhere in the document that is fully consistent with it — I sampled heavily (all of §21.1's
strict-specialization list, the L-rows reachable at layer access, the F-rows' declared-major reach
under [R-CNF-13]) but did not read all 120 rows against all of Part II a third time.

## Findings

Two findings survive, both grade OBSERVATION and both explicitly not byte-level, with the
reasoning that closes each given inline above and repeated in the structured result:

- **adversary-01** — §15.1's tile-index-region diagram is an unlabeled blockquote carrying
  normative content, which [R-CNF-01]'s label-based exemption does not reach; a reader who applies
  the "blockquote = non-normative" heuristic this project has been burned by before could mistake
  it for decoration. No byte-level fork: the diagram is a redundant restatement of [R-IDX-01] and
  [R-CNT-17].
- **adversary-02** — §20.4's PE = 0 preservation-licence sentence assigns a "commit"-shaped
  permission to "an updater" generally, though only the appender tier of that class ever performs a
  commit (a rewrite is expressly "not a commit," §20.5). No byte-level fork: the same sentence's
  second clause separately and correctly licenses the rewriter's actual operation (a rewrite), so
  both tiers' real permissions are stated correctly somewhere in the row; only the first clause's
  subject is imprecise.

I could not construct an attack that survives to a genuine byte-level fork — one where two
conforming verifiers, given the same bytes, could reach different certify/reject verdicts, or where
two conforming writers' outputs diverge on a question this specification actually leaves open in a
way that matters. Given this project's own calibration data (several recent rounds have also
returned zero, including the immediately following repair cycles of five-of-seven prior zero
rounds), an honest zero-byte-level result here is plausible on its own terms; I record it as such
rather than padding the finding list.
