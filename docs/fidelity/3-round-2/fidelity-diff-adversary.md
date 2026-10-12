# diff-adversary transcript — TARN fidelity round

## Disclosure

A message labelled as the user's request ("Go") was relayed above this
brief by the harness. It is the launcher's message to the orchestrator,
carried out before this session was spawned; it named no task for this
agent, needed no reconciliation with this brief, and was not treated as
widening the access rule below. This disclosure is the only use made of
it.

No other content was placed in this agent's context before work began
beyond the brief itself and this environment's standard tool-result
framing (file reads this agent issued itself). Nothing else is treated
as evidence.

## Access taken

Read, by name, exactly:
- A: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4981 lines)
- B: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4755 lines)

No directory was listed. No other file was opened. All commands below
ran only against the two files above, in this agent's own scratch
directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/diff-adversary/`.

## Method

1. Line-numbered both files (`A.numbered.txt`, `B.numbered.txt`) and
   extracted every `#`/`##`/`###`/`####` heading line from each to get a
   structural map. A has 131 heading lines, B has 130; B reorders §2 and
   §3 (terms-and-model before conformance) but is otherwise the same
   outline. Diffing the sorted `N.N` subsection numbers found exactly one
   missing subsection: **3.3** present in A, absent from B. No other
   subsection is missing, added, or renumbered.

2. Because both files are hard-wrapped (including inside blockquotes,
   where lines begin `> `), wrote a small reflow script
   (`reflow.py`) that joins each paragraph (blockquote, table row, or
   plain text) into one line, tagging its type. Ran it over both files
   (`A.reflow.txt`, 848 paragraphs; `B.reflow.txt`, 861 paragraphs).

3. Wrote `match.py`: for every "normal"/"blockquote" paragraph over 40
   characters in A, searched for its closest match in B's paragraph list
   (`difflib.get_close_matches`, cutoff 0.6), and symmetrically for B
   paragraphs against A. This is reorder-tolerant (B moves whole clauses
   between sections), so it surfaces real candidates rather than noise
   from the §2/§3 swap. Got 29 unmatched-in-B paragraphs from A and 39
   unmatched-in-A paragraphs from B (`match.out.txt`). Each one was read
   in context in both files (grep + sed on the numbered files) and
   classified by hand; most were false positives of two kinds: (a) a
   paragraph that in A is one block but in B is split by a blank line
   (or the reverse), tripping the paragraph-boundary heuristic, and
   (b) content relocated to another section verbatim or near-verbatim
   (confirmed by grep for a distinctive phrase).

4. Grepped keyword counts of carve-out/quantifier vocabulary ("save
   where", "unless", "except", "only", "whatever", "notwithstanding",
   "in any commit", "any rewrite") across both files to find raw count
   mismatches worth opening. Only "notwithstanding" differed (A: 2,
   B: 0); both instances were run down (one is a synonym swap to
   "override", the other is inside the one paragraph `R-CNT-25`'s
   quarantine clause, which migrated from §7.1 to §7.3 and was
   reworded, not dropped — confirmed by grepping "quarantined" in both
   editions and reading the destination paragraph).

5. For every one of this project's charter-named hot zones, pulled the
   full section from both editions with `sed`/`cut` and read them
   side by side: §2.3 conformance classes, §2.4 outcome classes/owning
   scope, §5.2 byte coverage, §6.2/§6.3 trailer and flag gates, §7.1/§7.3
   directory and record framing, §8 integrity, §9.2/§9.3/§9.7 commit
   protocol/generations/coverage verification, §15 tile index, §19
   reading algorithm, §20.3/§20.4/§20.5 append/preservation/rewrite,
   §21.1/§21.5/§21.6/§21.9 register reading rule, ignored records,
   non-violations, implementation limits, §22/§23 security/privacy,
   §24 conformance vectors, Appendix A (worked minimal file, byte
   table), Appendix B (constants table), Appendix G (reproducible-writer
   profile), Appendix H (checklists), §3.1/§3.2/§3.3 terms and reference
   array, §12 channels/sample types.

6. Six concrete file/byte constructions were carried through against
   both editions' actual rule text (never a paraphrase) wherever a
   charter-named hot zone showed a wording gap worth testing; all six
   are reported in `rejected_candidates` with the sentence, quoted from
   each edition, that forced the same verdict both ways.

7. Wrote this transcript and the three surviving findings to
   `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/out/transcript-diff-adversary.md`.

## What survived: findings

### adv-01 — §2.4's outcome-vocabulary/preserve-verbatim orthogonality sentence has no B counterpart

**A** (§2.4, immediately after the reader-outcome enumeration):
> "Every detectable file-conformance violation named by this specification is assigned exactly one **reader outcome**: reject-file, reject-layer, reject-tile, or ignore-record. `[R-CNF-07]` The same vocabulary is used for defined conditions that are not violations (an unknown ancillary record is *ignored*, not rejected). **preserve-verbatim** names an updater obligation, orthogonal to reader outcomes: a record a reader ignores can still be one an updater preserves."

**B** (§2.4, same position):
> "Every detectable file-conformance violation named by this specification is assigned exactly one **reader outcome**: reject-file, reject-layer, reject-tile, or ignore-record. `[R-CNF-07]`"

B stops at `[R-CNF-07]`. The next two sentences of A — (a) that "ignore-record" vocabulary also names *defined non-violations*, not only violations, and (b) that **preserve-verbatim** is an orthogonal axis, so a record a reader is allowed to ignore can still bind an updater to carry it forward unmodified — have no match anywhere in B. Grepped `orthogonal` and `ignored, not rejected` across all of B: zero hits (control: grepping the same strings in A returns the lines quoted above, proving the search works). Grepped `preserve-verbatim` across B: present only in the table row itself (identical to A's), never with this explanatory sentence.

Checked whether the *content* survives elsewhere under a different sentence: §20.4 (Re-emission and preservation) is byte-identical in substance between editions and already states the updater's preservation duty purely in terms of the MU/PE flags, independent of what a reader does with the record — so an implementer who read only B's §20.4 would still build the correct updater. §21.6's table already uses "Ignored" for defined non-violations without needing §2.4's permission to reuse the word. So this is real LOSS — A states it, B does not, nowhere — but not byte-level: no construction forces a different byte or a different verdict, because the operative rules it was glossing (§20.4's flag-driven table, §21.6's own "Ignored" language) are unchanged and self-sufficient in both editions.

- kind: LOSS
- location_a: §2.4
- location_b: §2.4 (absent)
- byte_level: false — §20.4 and §21.6 already carry the operative rule this sentence only glosses; confirmed by reading both in full (see method step 5) and finding them substantively identical.

### adv-02 — §2.4's closing Note ("Reject" is about scope, not UI) is dropped

**A** (§2.4, closing line, inside a `> **Note.**` block):
> "**Note.** "Reject" prescribes the scope of unusability, not user interface: how failure is reported is implementation technique."

**B**: absent. §2.4 in B ends at `[R-CNF-12]`'s paragraph and goes straight to `#### 2.5`.

Grepped `not user interface` and `prescribes the scope` across B: zero hits. This Note is explicitly non-normative under `[R-CNF-01]` (any text labelled *Note*, *Example*, or *Rationale* is excluded from the normative text) even inside A, so its removal cannot change what either edition requires an implementation to do.

- kind: LOSS
- location_a: §2.4 (closing Note)
- location_b: §2.4 (absent)
- byte_level: false — the dropped text was itself a Note, non-normative in A by `[R-CNF-01]`'s own rule.

### adv-03 — §3.3 "Container and array model" (the whole subsection) is missing from B

A's table of contents has a `#### 3.3 Container and array model` subsection consisting of one Note:

> "**Note.** Part I (container) is independent of Part II (array model) by construction: no Part I structure requires decoding sample payloads, so appenders, and rewriters that carry a layer forward, operate on files whose layers they cannot decode — that independence is load-bearing for the updater rules of §7 and §20."

Subsection-number diff (method step 1) found this is the *only* `N.N` heading in A with no counterpart in B — every other subsection in both documents, 92 of them, lines up one-to-one. Grepped `Container and array model`, `independent of Part II`, `carry a layer forward` and `cannot decode` (the distinctive phrase) across all of B: zero hits for all four; the same four searches against A return exactly the quoted Note, proving the searches work (control). B goes straight from §3.2 (The reference array) to §2 (Conformance, which in B's reordering comes after §3).

This is, again, a dropped Note — non-normative under `[R-CNF-01]` even in A — so it cannot be byte-level: the architectural fact it states (Part I is decodable without Part II) is a property of the rules themselves, not a rule of its own, and every rule it was glossing (the updater's ability to carry forward a layer record and tile-index region it never decodes, §20.4; the fact that an appender's and rewriter's writer obligations run only to bytes, never to decoded content, `[R-WRT-01]` etc.) is unchanged, identically worded, in both editions' §20.

- kind: LOSS
- location_a: §3.3
- location_b: absent (no §3.3 in B at all)
- byte_level: false — Note content, non-normative under `[R-CNF-01]`; the Part I/II independence it states is still true of, and still exercised by, both editions' (unchanged) §7/§20 rules.

## Rejected candidates: six constructions carried to bytes

Each of these targeted a charter-named hot zone (a carve-out, a
preservation rule, an outcome-class boundary, or the register's
governing-rule clause) where A and B's wording diverged enough on its
face to look promising. Each resolved to the same bytes/verdict under
both editions once the actual operative sentence — never a paraphrase —
was pulled from each. Quoted below.

1. **Unregistered ancillary record, MU=0/PE=1, that no reader
   implements (tests adv-01's potential byte impact).** Does an
   updater's byte-identical-retention duty depend on whether the
   record's *reader* outcome is ignore-record? Closed by §20.4's table
   row, word-for-word identical in both editions: "MU = 0, PE = 1 |
   Retain byte-identical, extent content unmodified." The obligation is
   keyed to the stored flags alone, never to the reader-outcome
   vocabulary §2.4 glosses. Same bytes under A and B.

2. **Dimension extent grown from E=10 (1 tile) to E=25 (3 tiles)
   across a commit — "addressed tile" count (tests §3.1's reworded
   definition, "every tile of a layer is addressed" in A vs. "a tile
   is addressed *in a generation*... under the geometry that
   generation declares" in B).** Closed by `[R-CNT-17]`, identical in
   both editions: "an entry_count that does not equal the
   geometry-derived addressed-tile count[...] is a validity error at
   layer scope." Both editions require entry_count = 3 at the second
   generation regardless of how §3.1's prose phrases "addressed"; A's
   own §20.3 step 4 already says growth "adds to the addressed set,"
   so B's §3.1 rewording states nothing A's own operative text didn't
   already decide. Same bytes, same verdict.

3. **User-metadata extent of exactly 4 bytes (tests Appendix B's
   constants-table citation moving from §7.1 (A) to §7.3 (B)).**
   Closed by identical operative text at the (correctly, differently
   cited) locations in each edition: "An extent of (0, 0) on a
   user-metadata record, or one whose extent_length is less than 5 ...
   is a validity error at its containing scope" (A §7.1) and "an
   extent_length less than 5 is a validity error at its containing
   scope: fewer than 5 bytes cannot hold both a document and the
   terminal CRC-32C" (B §7.3). Both reject the file at the same scope
   on the same bytes; the Appendix B pointer change tracks real content
   movement (confirmed by locating "Metadata compression exists only at
   record granularity" in both: A §7.1 line 979, B §7.3 line 944) and
   is not itself a rule.

4. **Pre-trailer pad of 92 bytes where the commit protocol's own pad
   step would have produced 28 (tests §2.3's dropped enumeration of
   which writer obligations are "conduct, not conformance").** Closed
   by §6.2, identical in both: "a longer gap is conforming, though no
   conforming commit produces one." Both editions certify the file
   (reporting the extra bytes as slack), neither treats the oversized
   gap as a file-conformance violation, regardless of whether §2.3
   spells this case out in its own cross-reference list or leaves it
   to be found at §6.2 directly.

5. **Top-level user-metadata record at document encoding 0x80
   (experimental range) inside an otherwise-minimal file (tests
   whether a verifier's verdict is "cannot establish" or "conforming,
   certified" under each edition's differently organized account of
   that exception).** Closed by §21.6's table row, identical in both:
   "Ignored (ignore-record); the file is conforming — §10.3's
   prohibition binds a writer's conduct, not the bytes. No document
   rule attaches at such an encoding, so a verifier certifies,
   reporting the record it ignored." Both editions certify this file;
   neither reports cannot-establish for it. A's §2.3 repeats this
   exception inline after its cannot-establish list; B's §2.3 just
   says "(§21.6 names the grounds)" — but §21.6 itself, unchanged,
   already carries the exception either way.

6. **Top-level record of an experimental-range type (0x9000) carrying
   MUST_UNDERSTAND = 1, which the reader does not implement (tests
   whether this is registered as a file-conformance violation or as a
   reader's capability refusal of an otherwise-conforming file, under
   each edition's placement of that paragraph — A's §21.6 closing
   paragraph vs. B's non-closing, relocated one).** Closed by
   identical text in both: "`[R-CNT-15]` obliges the reader to reject,
   and `[R-CNF-02]` makes the file conforming all the same... since the
   prohibition on publishing experimental values binds a writer's
   conduct and not the bytes." Both editions: file conforming, reader
   refuses on capability grounds, no register row. B's version of this
   paragraph is no longer literally "closing" (the cannot-establish
   grounds list was moved to follow it), so B's own cross-reference
   wording was correctly updated elsewhere (§21.9) from "§21.6's
   closing paragraph" to "§21.6 names..." — a correct adaptation to
   the reflow, not a content change.
