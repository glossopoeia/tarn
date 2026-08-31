# Cross-hunk consistency audit — case-adr0109

## Disclosure

Read: spec/tarn.md (sections 2.1-2.5, 3.x intro, 4.6, 4.7 opening, 6.3, 7.1-7.4,
11.3 refs, 13.x, 14.1-14.5, 15.1-15.4, 17.3, 17.4, 18.1-18.2, 19.4 step 4 (via
normalised grep), 20.1-20.5, 21.1-21.9, Appendix G, Appendix H opening), and the
eight files hunk-01.diff .. hunk-08.diff. Did NOT read full.diff, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, registry.json, git history.
Did not list the case directory beyond `ls hunk-*.diff`.

Ran: `wc -l`, `grep -n '^#'`, `sed -n` range reads, three python3 snippets over
tarn.md only (whitespace-normalised phrase search; unlabelled-blockquote finder;
register row/instance counter).

Unrequested context appeared before I began: a project instruction file pointer
(CLAUDE.md -> AGENTS.md) and an index of the maintainer's memory notes listing
topic titles. I did not open any of it and did not use it. Its presence is
disclosed here; contents not repeated.

## Grouping (worked out from the hunk bodies, not from section numbers)

- **Group A — which register row a file is recorded against.**
  hunk 3 (§21.1 specialization property), hunk 4 (§21.2 F21 condition text),
  hunk 6 (§21.5 R3/R4 disambiguation). Three sections, one question.
  hunk 4 is a deletion whose whole effect is elsewhere: it is what makes
  §21.1's new "F21 of F22" clean, and it removes a gloss that contradicted
  R-CNT-25's "never inline".
- **Group B — what a reader is obliged to do, and over what.**
  hunk 5 (§21.4 preamble, reject-tile vs verifier rows), hunk 7 (§21.6 sentinel
  row, re-quantified over positions and channels), hunk 1 (§14.4 Note, the
  planar/interleaved bool coincidence, which turns on R-SER-05's pad-bit fill).
- **Group C — compaction and unimplemented MU = 1 types.**
  hunk 2 (§20.4 table cell) against R-WRT-06 (§20.5), §21.6's closing paragraph
  and §21.9's R-ERR-04 sentence.
- **Group D — names and byte reproducibility.** hunk 8 (Appendix G item 10),
  non-normative, against §4.6 / R-ENC-13 / R-ENC-14 / §18.2's key rule.
  Second deletion whose effect is elsewhere (it removes the inline_length and
  dir_length consequences).

## Rule each repair adopts, in my words

1. For a single-channel bool layer the planar and interleaved tile images differ
   whenever ceil(P/8) != P; at P = 1 they are the same length and are equal iff
   the channel's fill is false (because R-SER-05 forces the seven pad bits to the
   fill bit and an interleaved bool byte is 0x00/0x01).
2. An updater that does not implement a record's type and finds MU = 1 stored:
   at layer scope only that layer is frozen for an appender, at file scope
   nothing can be committed, and at BOTH scopes a compactor must refuse.
3. Row X is recorded in preference to row Y exactly when every file exhibiting
   X's condition necessarily exhibits Y's; the named pairs are examples, not a
   closed list; merely-overlapping rows are outside the relation.
4. F21's condition is exactly "a top-level user-metadata record carries extent
   slot (0, 0)" — nothing about where its document sits.
5. reject-tile's "never fill instead of data" binds a reader only for rejections
   it is obliged to detect; for a verifier-detector row the governing rule says
   what a reader does.
6. A user-metadata failure under encoding 2 that is one of R4's frame constraints
   is R4's row, not R3's, even when the bytes also fail to decode; and R4's
   constraints are checkable from the extent's bytes rather than from a decoder's
   tolerance.
7. A sentinel entry means: for each channel THAT TILE carries, every sample
   position of the tile INSIDE THE LAYER'S EXTENTS reads as that channel's fill.
8. A non-NFC name is a different name because its bytes differ, length change or
   not; the writer therefore emits a different layer record.

## Searches run (whitespace-normalised across line breaks)

python3 flattening of tarn.md, then substring search for:
"reads as fill", "read as fill", "fill at every", "every sample position",
"sample position it carries", "contributes fill", "inside the layer",
"outside the layer", "never inline", "document inline", "extent slot (0, 0)",
"slot (0,0)", "(0, 0)".

Material hits:
- §13 opening paragraph (line ~1768): "an addressed tile that is not stored
  (§3.1) occupies no payload bytes, and reading it is defined behavior — each
  channel it carries reads as fill AT EVERY SAMPLE POSITION (§13.3) — rather
  than an error."  <- the exact quantifier hunk 7 removed from §21.6, unswept.
- §13.3 R-TYP-08: "a reader that returns any of the tile's sample positions
  inside the layer's extents MUST return, for each channel the tile carries,
  that channel's fill value at every such position."  <- hunk 7 matches this
  word for word.
- §19.4 step 4: "every REQUESTED sample position of its tile reads as fill" —
  clean, because R-MDL-01/R-RDR-04 make a requested position one inside the
  extents. PASSES.
- §3.1 term "stored": "An addressed tile that is not stored reads as fill (§13)."
  Coarse but not quantified over positions. PASSES.
- §7.1 R-CNT-25: "Each user-metadata record carries its document in its extent —
  NEVER INLINE". No other text claims (0,0) places a document inline, so hunk 4
  is fully swept.

Unlabelled blockquote scan: only two blockquotes carry no Note/Example/Rationale
label — the "How to read this document" block (self-labelled non-normative) and
§15.1's index-region layout block. No hunk lands in either. hunk 1 lands inside a
labelled **Note**, so it carries no normative force; it makes no claim that needs
any.

Register arithmetic (python3 count over the four tables): 121 rows, 277
instances; F 36/58, L 49/116, T 26/55, R 10/48. §21.8 says "121 conditions over
277 instances". Hunks 4 and 6 changed only Condition cells, so the arithmetic is
intact. §21.4's "26 conditions" that hunk 5 preserved is right.

## Check-by-check

### hunk 1 — PASSES
- Quantifier: "wherever ceil(P/8) != P" is exactly the length-difference
  condition; ceil(P/8) = P only at P = 1 for P >= 1.
- Citation R-SER-05: §14.5 "Every pad bit (§14.3) MUST carry the plane's
  channel's fill bit." Resolves. §14.3 confirms pad bits exist at P = 1
  (bits 1-7, since 1 mod 8 != 0). §14.2 confirms an interleaved bool value is
  "a single byte, 0x00 = false, 0x01 = true". So planar {0x00,0x01} vs
  interleaved {0x00,0x01} under fill false, and {0xFE,0xFF} vs {0x00,0x01}
  under fill true. "coincide exactly when that fill is false" is an iff and it
  holds.
- Check 6: P = 1 forces every T_i = 1, so ceil(E_i/T_i)*T_i = E_i and the tile
  has NO padding positions. Nothing else in the structure is left open by the
  claim.
- Non-normative (labelled Note); nothing normative depends on it.

### hunk 2 — one finding (X-06)
- R-WRT-06 quoted: "A compactor MUST refuse to compact a file carrying any
  record whose type it does not implement with MU = 1: such a type can define
  references this specification does not (§7.2), so its bytes cannot be safely
  relocated." Repair copies the ground verbatim; §7.2 confirms "Records with
  MU = 1 carry further references only where this specification or registry
  review (§10) defines them". Citations R-CNT-15, R-CNT-18, §2.3, §6.3 all
  resolve (R-CNT-08: "an updater encountering an unknown incompat-lane bit is a
  reader first, and therefore rejects the file before modifying anything").
- Check 7 (warrant verbs side by side): repair "a compactor MUST refuse THE FILE";
  R-WRT-06 "A compactor MUST refuse TO COMPACT a file". Same set of files, but
  "refuse the file" is the phrase §21.6 uses for a reader declining to serve a
  file, and R-WRT-01 makes a compactor "a reader of every structure they
  process". See X-06.

### hunk 3 — two findings (X-01, X-02)
- The property is stated over FILES ("where every file exhibiting one row's
  condition necessarily exhibits another's"). Tested against each listed pair:
  F35/F36 holds; L24/L25 holds; F21/F22 holds (slot (0,0) => extent_length 0 < 5);
  L10/L11 holds; F1/F6 FAILS and F1/F8 FAILS (F1's condition is "a signature
  constant is stored byte-reversed", with two instances; a file with only the
  trailer magic reversed exhibits F1 and F8 but NOT F6). See X-01.
- "the property decides any pair" is an exhaustive claim. Falsified by R3/R4 as
  hunk 6 leaves them: they merely overlap, the property therefore yields nothing,
  and hunk 6 had to write a bespoke precedence. See X-02.
- Instance arithmetic unaffected (277 confirmed).

### hunk 4 — PASSES
- The deleted gloss contradicted R-CNT-25's "never inline" and §7.2's
  "(0, 0) means no extent". Deletion is correct and there is no surviving
  restatement of it anywhere (grep above). §18.1's R-MTA-02 independently states
  "a malformed extent slot on such a record, (0, 0) included, is a validity
  error at the record's containing scope" — agrees with the trimmed row.
- Consequence for §21.8: F22's and L11's single vectors must now be built with a
  nonzero extent_offset and extent_length in 1..4 (offset 0 with nonzero length
  would be F30/L15). Reachable, so no corpus contradiction.

### hunk 5 — two findings (X-07, X-08)
- R-CNF-09 quoted: "A reader MUST NOT return data as valid from a scope this
  specification rejects AND WHOSE REJECTION THIS READER IS OBLIGED TO DETECT
  ([R-RDR-02]); in particular, a read of a rejected tile MUST NOT silently return
  fill." The repair's qualifier matches word for word. CITATION PASSES.
- §21.4's verifier rows are T2, T4, T5, T26. R-SER-08 (§14.2) states reader
  behaviour explicitly; R-SER-05 (§14.5) states "A conforming reader never
  returns this content ([R-GEO-04]) and is not obligated to check it"; R-COD-10
  (§17.3) states only what a WRITER violates and what a VERIFIER detects — it
  says nothing about a reader. See X-07.
- §21.2's and §21.3's preambles carry the same unqualified outcome sentence and
  were not swept. See X-08.

### hunk 6 — one finding (X-03)
- Check 7: repair "checkable from the extent's bytes without relying on a
  decoder's tolerance" vs R-MTA-09 (§18.2) "keeps the condition checkable from
  the bytes alone rather than turning on a decoder's tolerance". Same verb, same
  range. PASSES.
- Instance cell unchanged: 8 constraint kinds x 2 containers = 16, matching
  §18.2's list minus the two it says "carry no witness a file exhibits, and R4
  registers neither". PASSES.
- But §18.2 states the R3->R4 routing for ONE constraint only ("A mismatch [of
  the content-size field] is one of the frame constraints R4 registers, not a
  failure to decode under R3: THE BYTES DECODE"). The row generalises to all of
  R4's constraints and to the case where the bytes do NOT decode, and it does so
  in R3's cell, whose Governing rule is R-CNT-25, which is silent. See X-03.

### hunk 7 — two findings (X-04, X-05)
- Check 1: the repair's quantifiers now match R-TYP-08's exactly ("inside the
  layer's extents", "for each channel the tile carries"). Citations R-IDX-02 and
  R-TYP-08 both resolve. PASSES on its own terms.
- §13's opening paragraph still carries the pre-repair quantifier. See X-04.
- Check 6: the structure is the sentinel index entry and the read of its tile.
  Quantities in play: (a) which positions — now pinned; (b) which channels — now
  pinned; (c) the precondition that the index chain verified and the entry is a
  VALID sentinel (crc = 0). (c) is governed by R-TYP-09 and R-IDX-04 and is
  neither stated in the cell nor cited in its Rule column. See X-05.

### hunk 8 — one finding (X-09), otherwise PASSES
- R-ENC-13 quoted: "two names are the same name if and only if their encoded
  byte sequences are identical." Supports "a different name ... because its
  bytes differ". R-ENC-14 is indeed a SHOULD. §4.6's example is indeed 12 vs 13
  bytes. Canonical reordering permutes code points without changing their number,
  so "the same length in both forms" holds. The deletion of the inline_length and
  dir_length consequences is therefore correct.
- Check 6: §4.6 defines "names" as "the strings that identify layers, dimensions,
  channels, AND USER-METADATA KEYS". The item's title governs all four; its
  consequence sentence now names only the layer record. See X-09.
  (Appendix G is labelled non-normative and says "It adds no requirement to any
  actor", so nothing here is byte-level.)

## Byte-level dispositions

Only X-06 forks bytes. Its disputed input file — a conforming file (R-CNF-02,
§21.6) carrying an experimental-range MU = 1 layer sub-record the compactor does
not implement — is compacted by an implementation reading §21.6's "never a ground
to refuse the file" and is refused by one reading R-WRT-06 / hunk 2. One reading
permits an actor to produce the compacted output file; the other bars it.

Every other finding concerns a file that already carries a register-row violation
(X-05: L38; X-07: T26; X-08: F27/L48), or concerns only which row a nonconforming
file is recorded against (X-01, X-02, X-03), or sits in text that constrains no
actor (X-04 is redundant with R-GEO-04; X-09 is non-normative). R-CNF-05 bars a
conforming writer from emitting any of those files under both readings, so the
emittable set does not move.
