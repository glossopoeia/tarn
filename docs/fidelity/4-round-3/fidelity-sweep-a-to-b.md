# Completeness sweep, edition A -> edition B — working transcript

Disclosure: a relayed "user request" (the single word "Go") was prepended to my
brief by the harness. It is the message that launched this round and was
carried out before I was spawned; it is not a task for me and needed no
reconciliation with the brief. It never widened the access rule below.

## Access actually used

Read, by name only (never listed a directory):
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (edition A, 5004 lines)
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (edition B, 4810 lines)

No other file was opened. `rg`/`grep` and local Python were run only against
these two files (plus my own derived scratch files under
`/private/tmp/claude-501/.../fidelity-5/scratch/sweep-a-to-b/`, which is mine
alone and not listed here as a directory, only named).

## Method

1. **Structure check.** `grep -n '^#'` on both files to get the heading
   outline. Found: B reorders §3 (Terminology) to sit before §2
   (Conformance) — a pure reading-order change, both sections' own numbers
   unchanged. Found: A's §3.3 ("Container and array model") has **no
   counterpart heading at all** in B's outline (confirmed below as swab-03).
   Every other `####`/`###`/Appendix heading in A has a same-numbered
   counterpart in B, and vice versa.

2. **Labelled-block census.** Extracted every line starting `> **Note`,
   `> **Example`, `> **Rationale` in both files (pattern anchored at `^> `,
   since every such block in this document is a block-quote). A: 94 blocks.
   B: 90 blocks. Paired every block across editions by fingerprint (its
   first distinctive clause) in file order; where a fingerprint did not
   appear in the other edition, read both files' surrounding prose by line
   number to decide: moved-and-reworded, relabelled, added, or dropped.
   Full pairing is in `scratch/sweep-a-to-b/a-blocks-full.txt` and
   `b-blocks-full.txt`. Result: 89 blocks pair up one-to-one (content
   preserved, wording/location sometimes changed); 1 block in B (a new
   Rationale at §15.4) has no A counterpart (swab-06); 5 blocks in A have no
   B counterpart at all (one partially survives as reworked non-blockquote
   prose in §1; the other four are simply gone: swab-01, swab-02, swab-03,
   swab-04). 94 − 5 + 1(B's new one) = 90, which is exactly B's count: the
   census closes with no unaccounted block on either side.

3. **Paragraph-level diff per section.** Wrote a small de-wrapper
   (`scratch/sweep-a-to-b/dewrap.py`) that joins hard-wrapped lines of one
   logical paragraph (including block-quoted ones, tracking `> ` prefix
   separately) back into single lines, while leaving headings, table rows,
   list-item starts, horizontal rules and fenced-code blocks as their own
   lines. This turns "A and B say the same thing but wrap differently" into
   a no-diff, and makes every remaining `diff` hunk a real wording or
   content change. Split both de-wrapped files into per-subsection files
   keyed by heading number (`splitsec.py`), then ran `diff -u` on every
   matched pair (97 of the ~115 subsections differed at all). Read every
   hunk (not just the register tables and `[R-ID]` paragraphs the
   mechanical checker already compares) in file order, section by section,
   for §1 through Appendix H. This is the bulk of the work; the full diff
   is `scratch/sweep-a-to-b/diffs-all.txt` (1711 lines).

4. **Targeted re-reads at point of difference**, both editions side by
   side with `sed -n`, wherever a hunk looked like it might be changing a
   quantifier, a carve-out, or a cross-reference's target rather than just
   its phrasing. Each such case is logged below under "Candidates opened
   and closed."

5. **Keyword sanity check.** Counted raw occurrences of MUST, MUST NOT,
   SHOULD, SHOULD NOT, MAY, REQUIRED, SHALL across the two de-wrapped whole
   files, as a control that the rewrite did not silently flip a modal verb
   somewhere my paragraph reading missed. MUST=220/220, MUST NOT=78/78,
   MAY=57/57, REQUIRED=1/1, SHALL=2/2 — exact matches. SHOULD was 48 in A
   and 49 in B; traced the +1 to §6.3, where A's "a writer SHOULD emit the
   lowest version_minor ... and an appender the maximum of that floor ..."
   elides the second SHOULD grammatically (zeugma) and B spells it out as
   its own sentence with its own SHOULD. No new obligation; logged as
   closed below, not as a finding.

## Sections worked, in order

§1 (Introduction, itself non-normative under R-CNF-01) through Appendix H,
all 24 numbered sections and all 8 appendices, every matched subsection's
diff hunk read. Appendices C, E and F produced *no* diff at all after
de-wrapping (byte-identical content, just re-flowed or untouched) — checked
and clean. Every other section/appendix had at least one hunk; all were
read and judged. I reached every section; nothing was skipped for time.

## Findings carried to the structured result (see `findings`)

- **swab-01** (LOSS): §2.3's R-CNF-13 paragraph loses its trailing Note,
  which walked F14/F5/F15 as a worked illustration of "the test is the
  invariant, not the bytes read." B replaces it with one sentence, "§21.2
  lists the rows that reach." The *list itself* (F8, F14, F6, both of F1's
  instances) is unchanged, verbatim, in §21.2 in both editions — so no
  accept/reject verdict differs — but the worked reasoning that lets a
  reader generalize the test to a *new* row is gone from B with nothing
  replacing it.

- **swab-02** (LOSS): §2.4's trailing Note — '"Reject" prescribes the scope
  of unusability, not user interface: how failure is reported is
  implementation technique' — is simply absent from B. Grepped both files
  for "unusability" / "implementation technique": the only other hit in
  each edition is a *different* Note (§2.1's, about requirement phrasing
  discipline, which both editions keep). Nothing in B restates this
  specific clarification anywhere.

- **swab-03** (LOSS): A's whole §3.3, "Container and array model" — one
  Note stating that Part I is independent of Part II by construction and
  that this is "load-bearing for the updater rules of §7 and §20" — has no
  heading, no paragraph, and no restatement anywhere in B. Grepped B for
  "independent of Part II", "cannot decode", "load-bearing": zero hits
  carrying this claim (the string "load-bearing" survives in B only at two
  *other*, unrelated sentences, §3.1 and §12.1, about declared order).

- **swab-04** (LOSS, lower severity): §4.4's trailing Note, scoping
  R-ENC-08's bit-numbering rule to "flags and packed fields generally" and
  pointing out that boolean *sample* bit-mapping is §14's separate rule, is
  dropped with nothing in its place. Lower severity because §14.3 itself
  already cites "(§4.4)" directly when it states the packed-boolean bit
  order, in both editions identically, so the practical connection between
  the two rules survives even without this signpost.

- **swab-05** (LOSS): on relocation, B's §21.6 gains a new closing
  paragraph (moved from A's §2.3 "Conforming verifier" bullet) enumerating
  the grounds on which a verifier reports *cannot establish*. The move
  carries the five positive grounds over intact, but drops the one
  *negative* carve-out A stated in the same place: that a user-metadata
  document under an experimental-range encoding is explicitly *not* such a
  ground (R-MTA-10), with certification unaffected, and that encoding 0 /
  a reserved value *are* violations (R1). The conclusion is still
  recoverable from §21.6's own table row ("the file is conforming ... a
  verifier certifies"), unchanged in both editions, so no verdict differs
  — but the explicit disambiguating sentence is gone.

- **swab-06** (ADDITION, low severity): B's §15.4 gains a Rationale block
  with no A counterpart, including two new worked figures ("about 19 MiB at
  a million tiles and 190 MiB at ten million" for a hypothetical
  single-CRC-over-the-whole-index design). Both figures follow by plain
  arithmetic from facts A itself already states (20 bytes/entry, §15.1),
  so the derivation is A's own text; flagged for completeness since it is
  new prose A never wrote, not because it changes any rule.

- **swab-07** (OBSERVATION): §16.2's "what slabs are, and are not" block is
  relabelled from **Note** to **Rationale** between editions, with expanded
  content (new material on why a reader fetches a run as one range, and an
  explicit statement of A_slab's role). Both labels are non-normative under
  R-CNF-01, so the relabelling itself carries no fidelity consequence;
  logged because the charter asks for every label change to be reported.

- **swab-08** (EQUIVALENT / relocation, logged for completeness): A's
  preface block (lines 12–20, before "Part 0") is a **Note** titled "How to
  read this document," giving the section rubric, the structural/
  descriptive field split, and the sentence "Normative requirements carry
  stable identifiers like `[R-IDX-03]`, and test vectors cite those
  identifiers rather than prose positions." In B this Note is gone as a
  block-quote, but its rubric sentence and field-split sentence reappear as
  plain bold prose at the end of B's §1. The identifiers/test-vectors
  sentence is not repeated there, but §2.2 (identifier stability) and §24/
  R-VEC-02 (vectors cite the governing requirement identifier) state the
  same two facts separately, in both editions. Judged EQUIVALENT: nothing
  this sentence asserted is undecided in B, only its one-sentence summary
  form.

## Candidates opened and closed (did not become findings)

- §2.3's "Conforming TARN file" bullet in A spells out, with named
  examples, which writer obligations are "conduct, not output" (§10.3/
  §18.3's targeting advice, §9.2's barriers, §6.3's ignore-lane rule, §6.2's
  pre-trailer-gap length, §20.3 step 4's fixed-declaration bar) and so never
  make a file nonconforming by themselves. B's parallel bullet compresses
  this to one generic sentence. Checked every one of the five named cases
  at its own home section in B (§9.2, §6.3, §6.2, §20.3, §10.3/§18.3): each
  one's "this is conduct, not a file-conformance violation" statement is
  present, word-for-word or near enough, in B at that section. Closed as a
  relocation (EQUIVALENT), not a loss: the enumeration moved, the facts
  did not disappear.
- §2.3's "Conforming verifier" bullet's enumerated *cannot-establish*
  grounds (format major, MU=1-unimplemented type, codec/filter execution,
  decode-on-resource-grounds, metadata-decode decline): confirmed these
  five relocated to B's new §21.6 closing paragraph (see swab-05 above for
  the one piece that did *not* travel).
- §3.1's "addressed tile" term: A says baldly "every tile of a layer is
  addressed"; B qualifies it "a tile is addressed *in a generation* if that
  generation's tile index has an entry for it ... under the geometry that
  generation declares." Looked for whether this generation-qualification
  is a genuine addition (since §20.3 permits extents to grow between
  generations, which changes the addressed-tile count). Closed as
  EQUIVALENT: the generation-dependence of addressed-tile-count is already
  fully normative in A's own §11.2/§20.3 text; B's glossary entry only
  makes explicit what A's own body text already entails.
- §3.1's new sentence "A tile *carries* a channel when its payload holds
  that channel's samples at the cell's positions" has no word-for-word
  A counterpart, but A's own definition of *tile* in the same list already
  says a planar tile is "one cell of the grid for one channel" and an
  interleaved one "carrying all channels" — so B's added sentence only
  spells out what A's own adjacent definition already means. Closed as
  EQUIVALENT.
- §14.4's Rationale ending: A closes "a format that makes the honest type
  inexpressible gets the dishonest one"; B closes instead with "a bool
  channel would be declared int8 instead, the same bytes with the type
  label erased, and every consumer would inherit an untyped 0/1
  conversion." Different illustration of the same design point, inside a
  non-normative Rationale block; the decided rule it explains (`[R-SER-09]`,
  bool is expressible in both layouts) is identical and unchanged in the
  surrounding normative paragraph in both editions. Closed as EQUIVALENT,
  not logged as a separate finding (same category as swab-07, lower
  priority, omitted for space).
- §18.1 / §22.4 / §23.2 / Appendix B: a cross-reference to "the user-
  metadata record's extent" changes from "(§7.1)" to "(§7.3)" in four
  places, consistently. §7.1 is Directory region, §7.3 is Record types of
  format major 1 — the latter is where record-type scoping actually lives.
  Read as a citation correction, not a content change: nothing about what
  the extent is or how it's governed changed, only which section number is
  cited for it, same in all four places. Closed, not logged.
- Global keyword counts (MUST/MUST NOT/MAY/REQUIRED/SHALL exact; SHOULD +1
  traced and closed) — see Method §5 above.
- §21.2, §21.5, §21.6 register tables and intro paragraphs: read in full
  both editions; byte-for-byte identical content (only inter-word
  punctuation/dash-vs-comma differs). No finding.

## Sweeps run, as a flat list (for the evidence object)

- `grep -n '^#'` both files: 1 structural difference found (§3.3 missing),
  confirmed by control (searched headings list exhaustively, not a sample).
- `grep -n '^> \*\*\(Note\|Example\|Rationale\)'` both files: 94 vs 90,
  fully paired (see census above); every unpaired block resolved by direct
  read, none left unexplained.
- Paragraph-diff of every one of ~115 matched subsections (`diff -u` after
  de-wrapping): 97 produced a hunk; all 97 read in full; 18 produced
  byte-identical de-wrapped text (no hunk), also confirmed clean.
- `grep -n 'R-ENC-15'`, `'R-SER-04'`, `'conduct'`, `'ignore-lane'`,
  `'pre-trailer'`, `'R-MTA-10'`, `'not such a ground'`,
  `'load-bearing\|independent of Part II\|cannot decode'`,
  `'unusability\|implementation technique'`, `'F14'` — each a control
  search run against *both* files to prove a candidate loss was (or was
  not) restated anywhere else in the document, not just near where it used
  to sit.
- Keyword frequency counts (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY,
  REQUIRED, SHALL) over both whole de-wrapped files, then per-subsection,
  to localize the one discrepancy found.

## Sections not reached

None. Every numbered section (1–24) and every appendix (A–H) had its
matched subsections diffed and every hunk read in file order.
