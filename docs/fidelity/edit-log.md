# The readable edition — edit log

ADR-0133, decision 3: a restatement of a rule may be removed where the rule's
statement remains and the removal is logged with the ADR that added it; a
normative sentence is reworded only one at a time and its ID listed in
`conformance/tools/reworded-ids.txt`. This log is where the edits to edition B
(the `readable` branch's `spec/tarn.md`) are recorded, one entry per commit,
newest first. Edition A is `spec/tarn.md` at tag `edition-a` (`81e2ad2`).

Each entry carries: the date and commit; the sections touched; what was cut,
merged, moved or reworded, in a sentence each; every restatement removed, with
the location where the rule still stands and the ADR that added the
restatement where `git log -S` finds it; every reworded requirement ID; the
soft items `tarn_inventory.py` reported and what each was; and any question
that had to go to the maintainer.

## Ready for calibration 2

Stretches the maintainer has declared reworded, in which the next seed set is
planted (`fidelity-seed.py`, every seed with `statement_count` 1): none yet.

## Entries

### 2026-09-23 — §3.1: *directory* and *generation* entries shortened

- **Commit:** `Readable: §3.1 — directory and generation entries shortened`
  (the commit carrying this entry).
- **Sections:** §3.1 only.
- **Edits.**
  1. *directory*: "Each commit appends a *complete* directory — never a
     delta (§9.2) — so a conforming commit adds one directory per
     generation; unqualified, …" becomes "Each commit appends a *complete*
     directory; unqualified, …".
  2. *generation*: "No field numbers generations; successive generations of
     one file are ordered by the strictly increasing committed file length
     their trailers carry (§9.3)." becomes "No field numbers generations."
     The negative is kept on purpose: ADR-0111 removed the generation
     counter field, and this sentence is where the document says so.
- **Removed restatements:**
  - "never a delta (§9.2) — so a conforming commit adds one directory per
    generation" → *complete* in the same sentence; §5.1 ("the directory
    each commit appended"); §9.2 `[R-LIF-02]` step 3 ("append the new
    complete directory"); Appendix D ("a complete directory per
    generation"). Added by `140d491`, ADR-0065.
  - "successive generations of one file are ordered by the strictly
    increasing committed file length their trailers carry (§9.3)" → §9.3
    ("F strictly increases per commit — by at least 128 (`[R-LIF-02]`) —
    so it orders that file's generations and identifies each of them");
    §9.2's step 5 gloss. Added by `115c890`, ADR-0111.
- **Reworded IDs:** none. Neither sentence carries a keyword or closes with
  an ID.
- **Soft items:** `TERM_TEXT_CHANGED` for *directory* and *generation*
  (edits 1 and 2), added to the three from the earlier rewording;
  `HEADINGS`.
- **Questions raised:** none.

### 2026-09-23 — §3.1: the list reordered, container terms first

- **Commit:** `Readable: §3.1 — terms reordered, container structures before
  the array model's` (the commit carrying this entry).
- **Sections:** §3.1 only.
- **Edits.** The eighteen entries stay one list, every entry byte-identical,
  in a new order: the container's structures first (file, front signature
  block, generation, trailer, directory), then the array model's in their
  existing order (layer, dimension, rank, channel, channel layout, sample,
  coordinate, tile, addressed tile / stored tile, fill value, slab, tile
  index, user metadata). The lead-in sentence is unchanged. A version with
  the two groups as separate lists under a lead-in each was tried and
  dropped at the maintainer's preference for one list; it had also shown
  that the inventory tool's term parser reads a paragraph between two
  entries as the tail of the preceding term (a spurious
  `TERM_TEXT_CHANGED`), which is worth a parser fix if a lead-in is ever
  wanted inside the list.
- **Removed restatements:** none.
- **Reworded IDs:** none.
- **Soft items:** unchanged (`TERM_TEXT_CHANGED` ×3 from the earlier
  rewording, `HEADINGS`).
- **Questions raised:** none.

### 2026-09-23 — §3.1: *generation* moved ahead of its first use

- **Commit:** `Readable: §3.1 — generation defined before its first use` (the
  commit carrying this entry).
- **Sections:** §3.1 only.
- **Edits.** The *generation* entry (four lines, verbatim) moves from the
  seventeenth position to the second, directly after *file*, so that
  *addressed tile / stored tile*, *directory* and *trailer* no longer use
  the term before it is defined. The list now runs: file, generation,
  layer, dimension, rank, channel, channel layout, sample, coordinate,
  tile, addressed tile / stored tile, fill value, slab, tile index,
  directory, trailer, front signature block, user metadata. Forward
  references remaining inside the list: *generation* names trailers,
  *channel* names samples, *sample* names coordinates, *tile* names the
  tile index; every one is a mutual dependency the list cannot order away.
- **Removed restatements:** none.
- **Reworded IDs:** none.
- **Soft items:** unchanged from the previous entry (`TERM_TEXT_CHANGED` ×3,
  `HEADINGS`); the term's text is byte-identical, so the move adds none.
- **Questions raised:** none.

### 2026-09-23 — §3.1 and §12: "load-bearing" replaced by what the declared order fixes

- **Commit:** `Readable: §3.1, §12 — dimension, channel and channel-layout
  entries reworded; load-bearing replaced` (the commit carrying this entry).
- **Sections:** §3.1 (three term entries), §12 (opening paragraph).
- **Edits.**
  1. §3.1 *dimension*: "the declared order is load-bearing (§11.4)" becomes
     "the declared order fixes the sample order on disk: within a tile the
     last-declared dimension varies fastest, and tile ordinals follow the
     same order (§11.4)". Derived from §11.4's row-major rule (last-declared
     dimension fastest, `[R-GEO-05]`) and its ordinal formulas
     (`[R-GEO-06]`).
  2. §3.1 *channel*: "the order is load-bearing (§11.4, §14)" becomes
     "which fixes where the channel's value sits within each interleaved
     sample (§14) and where its tiles fall in a planar layer's index
     (§11.4)". Derived from `[R-SER-01]` (channel values adjacent in
     declared channel order) and `[R-GEO-06]` (planar disk ordinal
     c · N + s).
  3. §3.1 *channel layout*: the clause "encoded in the layer record (§7.4),
     byte-layout semantics in §14" cut; the definition ends at *planar*.
  4. §12, opening paragraph: "the declared order is load-bearing (§3.1,
     §11.4)" becomes "the declared order fixes each channel's index (§3.1,
     §11.4)". The paragraph cites `[R-CNT-23]` but does not define it
     (the ID closes §7.4's paragraph), so no ID paragraph changed.
- **Removed restatements:** §3.1 *channel layout*'s two pointers → §7.4
  (the `channel_layout` field) and §14; `86162e0`, Batch 3 (ADR-0029 to
  ADR-0032). §12's "load-bearing" clause was a restatement of §3.1's, added
  by `75af4ac`, Batch 5 (ADR-0036); it now points at §3.1's precise form.
- **Reworded IDs:** none. None of the four sentences carries a keyword or
  closes with an ID.
- **Soft items:** `TERM_TEXT_CHANGED` for *dimension*, *channel* and
  *channel layout* (edits 1–3, read side by side above); `HEADINGS`,
  carried from the previous entry. Keyword counts identical.
- **Questions raised:** none. "Load-bearing" still appears in §3.3's Note
  (Part I's independence from Part II) and in §21 (line "load-bearing — the
  same type as a layer sub-record"), both outside this edit.

### 2026-09-23 — §1–§3: introduction rewritten, front-matter Note folded in, §3 moved ahead of §2

- **Commit:** `c486508`, `Readable: §1–§3 — introduction rewritten,
  front-matter note folded in; terminology moved ahead of conformance`.
- **Sections:** the front matter (the Note before Part 0), §1, §2, §3.
  Nothing from §4 on changed.
- **Edits.**
  1. §3 (Terminology and Data Model) moved ahead of §2 (Conformance), both
     verbatim, so that §2 no longer uses *layer*, *tile*, *record*,
     *directory*, *trailer*, *updater* and *verifier* before §3.1 defines
     them. Section numbers stay as they are (ADR-0133 decision 3), so the
     file reads §1, §3, §2, §4 until the renumbering step (mapping 3→2,
     2→3), which the maintainer wants done soon rather than last.
     Consequence accepted: §3.2's MUST and MUST NOT now precede §2.1's
     keyword statement, which binds the keywords wherever they appear.
  2. §1 rewritten from 587 words to 360 and from 19 section citations to
     one (§4.7). The five design goals keep their names and lose their
     mechanisms, figures and citations; the "four questions" paragraph and
     the "Reading this document" roadmap are cut; "what TARN is not" is
     kept without its citation. §1 stays non-normative under `[R-CNF-01]`.
  3. The front-matter Note "How to read this document" is removed and its
     two surviving sentences (the section rubric; layout tables whose
     columns suit the structure, with §4.7 for what they carry and for the
     structural/descriptive classes) become §1's closing paragraph. Notes
     61 → 60.
- **Removed restatements** (surviving location; commit or ADR that added the
  restatement, by `git log -S`):
  - the "four questions" paragraph: the 64-byte trailer committing each
    state, the directory reachable in one further request, the per-layer
    index with one entry per tile, an outcome class on every named
    violation → §3.1 (*trailer*, *directory*, *tile index*), §6.4, §2.4
    `[R-CNF-07]`; `c75a127`, Batch 13 (ADR-0046, ADR-0047).
  - "Opening a file costs two range requests whatever its size" → §6.4
    ("the baseline remote open is two requests"); `c75a127`. Generalised in
    goal 1.
  - "reading one tile costs that layer's segment-CRC array, the index
    segment covering the tile, and the tile's own bytes … which is what
    §21.9's tile-count guarantee is sized against" → §19.4 step 3 (the two
    fetches and their CRCs); the sizing remark has no counterpart and was
    design commentary, not a rule; `c75a127`.
  - "A commit appends payloads, a complete directory, and a trailer, in
    that order; committed bytes are never modified" → §9.1 ("an append-only
    transaction that extends the file and never modifies a committed
    byte"), §9.2 `[R-LIF-02]` (the ordered steps), §5.1 ("directory,
    pre-trailer pad, and trailer last, in that order"); `c75a127`.
    Generalised in goal 3.
  - "a torn write cannot damage the previous state — a recovery tool
    truncates back to it (§9.6), while a conforming reader declines the
    torn file rather than scanning backward (§9.5)" → §9.5, §9.6;
    `c75a127`. Generalised in goal 3.
  - "Superseded bytes remain as slack until compaction reclaims them: this
    is a write-mostly artifact, not a version store, and bulk work followed
    by compaction is the shape it is built for" → §5.1 (slack), §7's Note
    ("this format is not a version store"); `f738b29`, ADR-0048.
  - "A long series of small edits is supported and wasteful — each costs a
    full tile and its layer's whole index (§20.3)" → §20.3, §21's Note on
    index regions; `f738b29`, ADR-0048.
  - "no subset profiles, no subset readers, and no feature a conforming
    reader can decline" → §2.3 `[R-CNF-03]`; `c75a127`. Kept in general
    form in goal 5.
  - "Sparse tiles, zero-extent dimensions, padding content, malformed index
    entries, and every other boundary have stated answers (§21)" → §21;
    `c75a127`. Generalised in goal 4.
  - "growth happens through four enumerated vehicles and a registry (§10)"
    → §10.1 `[R-ENC-07]`; `c75a127`. Generalised in goal 5.
  - the roadmap: "§2 fixes the conformance vocabulary", the Parts and their
    section ranges, "§21's register lists every violation with its
    outcome", "Part I alone yields a container reader … §19.3's layer
    validation resolves into Part II's value sets and geometry rules" →
    the Part headings; §21.1; §3.3's Note (Part I independent of Part II);
    §19.3; `c75a127`.
  - front-matter Note, "a packed variable-length payload has no offsets to
    give" → §4.7's Note (the layer record's inline payload); `ff07009`,
    cleanroom round 12.
  - front-matter Note, the definitions of *structural* and *descriptive*
    → §4.7 `[R-ENC-16]`; `0ce8fc4`, Batch 1 (ADR-0027). The class names
    stay in §1.
  - front-matter Note, "Normative requirements carry stable identifiers
    like `[R-IDX-03]`, and test vectors cite those identifiers rather than
    prose positions" → §2.2; §24 ("a row label is never renumbered");
    `4751657`, cleanroom round 10.
- **Reworded IDs:** none.
- **Soft items:** `HEADINGS`, 130 in A and 130 in B, order differing by the
  §3/§2 move. The info line's labelled-paragraph count: Note 61 → 60, the
  front-matter Note. Keyword counts identical.
- **Questions raised:** none needing an ADR. Held for the maintainer: when
  to run the renumbering step (3→2, 2→3) with its mapping table.
