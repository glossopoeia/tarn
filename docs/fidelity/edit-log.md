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

**Calibration 2 ran on 2026-09-24** over B at `f1feb3f` with six seeds in
§2.3 and §21.6 (`wf_c16a4649-e70`; [1-calibration-2/findings.md](1-calibration-2/findings.md)).
The reading instruments found every content change; the two seeds that were
restatement removals were correctly overturned on refute. Correction to the
entry for `2c00338` below: the resource-decline ground is not "tied to the
verdict nowhere else"; §9.7 states it ("reports that check unmade and cannot
certify (`[R-CNF-11]`, `[R-ERR-04]`)"). The stretches as declared:

- **§1** (declared 2026-09-24 with §3): rewritten 2026-09-23 (`c486508`);
  non-normative under `[R-CNF-01]`, so it carries no rule to seed.
- **§3** (declared done 2026-09-24): §3.1 reworded in eight entries
  (dimension, channel, channel layout, directory, generation, fill value,
  addressed tile / stored tile, tile) and reordered; §3.2 untouched; §3.3
  removed. Candidate seeds, each a sentence A states once: "No field
  numbers generations"; "unqualified *stored* means stored in the live
  generation"; "Superseded payload bytes from earlier generations do not
  make a tile stored"; the *directory* entry's "located from the trailer".
- **§2** (declared done for this pass, 2026-09-24): §2.3 reworded in
  every item but the writer's, seven of its IDs listed (`R-CNF-02`, `-03`,
  `-04`, `-06`, `-11`, `-13`, and `R-COD-11` by the tool's citation
  mapping), its Note removed and the cannot-establish grounds moved to
  §21.6; §2.4 cut after `[R-CNF-07]` and its Note removed; §2.1, §2.2
  and §2.5 untouched. This is the stretch that carries reworded rules, so
  the seeds for calibration 2 belong here. Candidate seeds, each a
  sentence inside reworded text that A and B state exactly once (counts
  checked with whitespace normalised):
  "binds the writer and never makes a file nonconforming" (`[R-CNF-02]`);
  "both record types §7.3 registers" (`[R-CNF-03]`);
  "available only to a traversal that established no violation" (`[R-CNF-11]`);
  "MAY stop at the first violation it finds" (`[R-CNF-11]`);
  "reject-file under the requirement that states the condition, not as a capability refusal" (`[R-CNF-13]`);
  "an exemption that the condition's own requirement grants for a reason other than the declared major still holds" (`[R-CNF-13]`);
  "reports *nonconforming*, whatever major the file declares" (`[R-CNF-13]`);
  "assigned exactly one **reader outcome**" (`[R-CNF-07]`).
  The moved paragraph in §21.6 closes with no ID and is a further
  candidate, being invisible to the inventory tool by construction.
- **§4** (declared done 2026-09-28): §4.2, §4.5, §4.6 and §4.7 reworded or
  cut (`8f16983` through `eacb6cc`); `R-ENC-03`, `-04`, `-05`, `-10`,
  `-12`, `-16` listed; §4.1 and §4.3 untouched. Candidate seeds, each
  inside reworded text: the three width exceptions (`[R-ENC-03]`); "MUST
  NOT act on a wrapped or truncated value" (`[R-ENC-04]`); "comparing it
  against a constant for validation is not acting on it" (`[R-ENC-10]`);
  "with the same exception for a key inside a user-metadata document"
  (`[R-ENC-12]`). Not yet listed for a real round: none of these has run.

## Entries

### 2026-09-27 — §4.7's Note in plain sentences

- **Commit:** `Readable: §4.7 — layout-table Note in plain sentences` (the
  commit carrying this entry). Previous: `c1621b7`.
- **Sections:** §4.7, the Note.
- **Edits.** The one-paragraph Note (a general rule and three exceptions in
  participial chains) becomes six sentences: what a layout table is; the
  columns of a fixed-layout structure's table; "Some tables depart from
  this."; the inline payload's table (§7.4) without offset, size or class
  columns and why; §6.1's Value column; §7.2's folded range and the bounds
  below its table. Same facts, same three exceptions; nothing added.
- **Removed restatements:** none.
- **Reworded IDs:** none (a Note).
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×13, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-27 — the contract tool watches every defining paragraph; `R-COD-11` off the list

- **Commit:** `Readable: reworded-ids — R-COD-11 removed, its paragraph
  untouched under the repaired mapping` (the commit carrying this entry).
  Previous: `5541a0f`; the tool change is `main`'s commit merged just
  before it.
- **Sections:** none of the spec. `conformance/tools/tarn_inventory.py`
  (on `main`, merged) and `conformance/tools/reworded-ids.txt`.
- **Edits.** `tarn_inventory.py` now takes an ID's governing text to be the
  paragraph in which the ID stands as a marker of its own (after a sentence
  end, before the block's end or a new sentence), falling back to the block
  it closes and then to its first citation. Under the old rule seventeen
  IDs written with text after the ID mapped to a register row or a
  citation, and their defining paragraphs were unwatched; `[R-ENC-12]`'s
  listing came back stale for that reason in the entry below. Under the new
  rule A against B reports every listed ID as `ID_REWORDED_LISTED` except
  `R-COD-11`, whose §17 paragraph is untouched: it had been listed on
  2026-09-24 only because the tool mapped it to §2.3's verifier item by
  citation. It is removed from the list. Selftest PASS with a new case;
  gate.sh PASS on `main`.
- **Removed restatements:** none.
- **Reworded IDs:** thirteen remain listed: `R-CNF-02`, `-03`, `-04`, `-06`,
  `-07`, `-11`, `-13`, `R-ENC-03`, `-04`, `-05`, `-10`, `-12`, `-16`.
- **Soft items:** `ID_REWORDED_LISTED` ×13; `TERM_TEXT_CHANGED` ×8;
  `HEADINGS`. No stale listing. Keyword counts unchanged.
- **Questions raised:** none; the tool change was the maintainer's go.

### 2026-09-27 — §4.6: `[R-ENC-12]`'s exception stated by reference

- **Commit:** `Readable: §4.6 — name rule's quarantine exception by
  reference to [R-ENC-11]'s` (the commit carrying this entry). Previous:
  `afb2ba6`.
- **Sections:** §4.6, the names paragraph.
- **Edits.** "— except for a key inside a user-metadata document, where
  `[R-CNT-25]`'s quarantine governs and the outcome is ignore-record."
  becomes ", with the same exception for a key inside a user-metadata
  document (`[R-CNT-25]`)." The exception itself is kept: the maintainer
  read it as redundant, and it is not (a name includes a user-metadata
  key, and without it a bad key would be a validity error at the record's
  owning scope, reject-file or reject-layer, against `[R-CNT-25]`'s
  ignore-record); what was repeated were the words of `[R-ENC-11]`'s
  identical exception one paragraph above, which the shorter form now
  points at.
- **Removed restatements:** the exception's wording, restated by reference
  → `[R-ENC-11]` (the paragraph above) and `[R-CNT-25]`; the clause's
  origin is `0ce8fc4`, Batch 1 (ADR-0027), the quarantine's ADR-0066.
- **Reworded IDs:** `R-ENC-12`, listed (fourteen IDs in all).
- **Soft items:** `REWORDED_LIST_STALE R-ENC-12` (corrected 2026-09-27: the
  entry first said `ID_REWORDED_LISTED`). The tool reported the listing
  stale because it takes as `[R-ENC-12]`'s governing text the first block
  the ID *closes*, which is register row L5, not the names paragraph, where
  the ID is followed by "A name is:" and closes nothing; the paragraph did
  change and the listing is right. `ID_REWORDED_LISTED` ×13,
  `TERM_TEXT_CHANGED` ×8 and `HEADINGS` carried. Keyword counts unchanged.
- **Questions raised:** the tool's mapping leaves the defining paragraph of
  every ID that is followed by more text unwatched; a fix is proposed to
  the maintainer (below, next entry). Cutting the exception outright was
  declined as a content change.

### 2026-09-25 — §4.5: `[R-ENC-10]`'s sentence in three

- **Commit:** `Readable: §4.5 — verify-before-acting rule in three sentences`
  (the commit carrying this entry). Previous: `708bf7e`.
- **Sections:** §4.5, `[R-ENC-10]`'s paragraph.
- **Edits.** "A reader MUST verify the checksum covering a field before
  acting on that field — where *acting on* means using its value to
  allocate, seek, fetch, or select behavior; comparing a field against a
  constant for validation is not acting on it, and an explicit validation
  order (§6.2) governs where one is stated." becomes "A reader MUST verify
  the checksum covering a field before acting on that field. *Acting on* a
  field means using its value to allocate, seek, fetch, or select
  behavior; comparing it against a constant for validation is not acting
  on it. Where this specification states an explicit validation order
  (§6.2), that order governs." The pointer sentence after the ID is
  verbatim.
- **Removed restatements:** none.
- **Reworded IDs:** `R-ENC-10`, reason line extended.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×13, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-25 — §1: the four growth vehicles named in the fifth goal

- **Commit:** `Readable: §1 — the four ways the format grows, named in the
  closed-core goal` (the commit carrying this entry). Previous: `209f403`.
- **Sections:** §1, the fifth design goal.
- **Edits.** "; the format grows through a fixed set of extension vehicles
  and a registry" becomes ". The format grows in exactly four ways: new
  record types, new enum values in reserved ranges, new ignore-lane flag
  bits, and new standardized user-metadata keys (§10)." The maintainer
  wanted the closed set highlighted outside §4.3; §1 is non-normative
  (`[R-CNF-01]`), so naming the four there adds no content, and the rule
  stays where it is stated: §4.3 (with `[R-ENC-07]`, as the reason an
  unexpected size is never evidence of a newer format version) and §10.1
  ("This format grows through exactly four vehicles (`[R-ENC-07]`)").
- **Removed restatements:** none (one restatement added, in the
  non-normative introduction; §1 now cites §10 as well as §4.7).
- **Reworded IDs:** none.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×13, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none. Considered and not done: moving §4.3's
  sentence itself, which would leave `[R-ENC-07]`'s paragraph without the
  rule §10.1 cites it for.

### 2026-09-25 — §4.2: `[R-ENC-04]` in plain order

- **Commit:** `Readable: §4.2 — designated quantities stated in plain order`
  (the commit carrying this entry). Previous: `0a6e4c9`.
- **Sections:** §4.2, the paragraph carrying `[R-ENC-04]` and `[R-ENC-05]`.
- **Edits.** The one long sentence "A reader MUST treat any quantity this
  specification **designates** a declaration-derived sum or product of
  integers obtained from a file (offsets plus lengths, grid counts, tile
  counts, sample-position counts, ordinals) whose mathematical value would
  exceed 2⁶³ − 1 as a validity error at the owning scope, and MUST NOT act
  on a wrapped or truncated value." becomes two: the class first ("Some
  quantities are not stored but computed from stored integers: an offset
  plus a length, a grid count, a tile count, a sample-position count, an
  ordinal."), then the rule ("Where the section that defines such a
  quantity **designates** it a declaration-derived sum or product, a reader
  MUST treat a mathematical value above 2⁶³ − 1 as a validity error at the
  owning scope, and MUST NOT act on a wrapped or truncated value."). "A
  designation is express, made by the section that defines the quantity"
  becomes "A quantity counts as designated only where its defining section
  says so in words"; the comparison-only carve-out follows in the same
  words. `[R-ENC-05]`'s sentence is verbatim. Both MUSTs and the MUST NOT
  keep their subjects and objects.
- **Removed restatements:** none.
- **Reworded IDs:** `R-ENC-04` (reason line rewritten); `R-ENC-05` already
  listed for sharing the paragraph.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×13, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-25 — §4.2: the range rule's parenthetical cut

- **Commit:** `Readable: §4.2 — range rule without its entry-count and
  slab-run-length aside` (the commit carrying this entry). Previous:
  `7d2e987`.
- **Sections:** §4.2, `[R-ENC-03]`'s paragraph.
- **Edits.** "— entry counts and slab run lengths included —" cut from the
  range sentence; the quantifier "every offset, length, extent, and count
  this specification defines" and the MUST are verbatim.
- **Removed restatements:** the aside → the sentence's own word *count*
  (entry_count) and §7.4's layout table for the slab run length ("run
  length in tiles, 1 ≤ S ≤ 2⁶³ − 1 (§16.2)"), restated in Appendix B and
  covered by register row L1; `72ae3fa`, Batch 10 (ADR-0042).
- **Reworded IDs:** `R-ENC-03`, reason line extended.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×13, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-25 — §4.2: the width rule states its three exceptions

- **Commit:** `Readable: §4.2 — u64 widths rule with its three exceptions
  named` (the commit carrying this entry). Previous: `8f16983`.
- **Sections:** §4.2, `[R-ENC-03]`'s paragraph.
- **Edits.** "All file offsets, dimension extents, and tile extents are
  `u64`, as is every byte length this specification does not give another
  width where it defines the field." becomes "All file offsets, dimension
  extents, tile extents and byte lengths are `u64`, with three exceptions:
  a record's inline_length is a `u32` (§7.2), and the length prefix of a
  name (§4.6) or of a fill value (§7.4) is a `u8`." The maintainer asked
  whether the exceptions are enumerated elsewhere; they are not, and the
  clause cut in `8f16983` as examples was in fact the whole list, so it
  returns as a list. "Three" asserts a closure A implied and did not state;
  the derivation is every layout table in A (inline_length is the only
  byte-length row narrower than `u64`; the two prefixes are stated in §4.6
  and §7.4's prose). A future width change touches this sentence.
- **Removed restatements:** none (one restored, as the enumeration).
- **Reworded IDs:** `R-ENC-03`, its reason line rewritten.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×13, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-25 — §4.2–§4.7: six glosses and restatements cut

- **Commit:** `Readable: §4 — width examples, actor gloss, bit-numbering
  Note, coverage-map restatement, three-ID gloss and the taxonomy Note's
  tail cut; R-ENC-03, -04, -05, -10, -16 listed` (the commit carrying this
  entry). Previous entry's commit: `da95a34`; the calibration commits
  between are `572b5c5`, `60b6d30` and the merge `d8cc58a`.
- **Sections:** §4.2, §4.4, §4.5, §4.7. §4 falls from 188 lines to 164.
  §4.1, §4.3 and §4.6 untouched; the maintainer kept §4.3's four-vehicles
  sentence because `[R-ENC-07]` lives in its paragraph and §10.1 cites it.
- **Edits.** Every keyword sentence is verbatim.
  1. §4.2, `[R-ENC-03]`: "— a record's inline_length is a `u32` (§7.2),
     and a name's or fill's length prefix a `u8` (§4.6, §7.4)" cut; the
     sentence ends at "where it defines the field."
  2. §4.2, `[R-ENC-04]`: "A reader — including any updater or verifier,
     which are readers of the files they process — MUST treat" becomes
     "A reader MUST treat".
  3. §4.4: the Note pointing at §14 for the bit mapping of boolean samples
     removed. Notes 57 → 56.
  4. §4.5, `[R-ENC-10]`: the twelve lines after the ID restating §8.1's
     coverage map (the exactly-one-checksum rule, its three exceptions,
     the interior checksum fields) cut; the paragraph keeps "Which bytes
     each checksum covers, and each conformance class's verification
     obligations, are defined with the structures that carry them (§8)."
  5. §4.7, `[R-ENC-16]`: ", which is the sense `[R-CNT-07]`, `[R-MTA-02]`
     and `[R-SEC-06]` already use" cut.
  6. §4.7's Note: its last three sentences cut (a name is structural and its
     prefix is framing; worked examples and paired vectors; constants in
     Appendix B); the layout-table conventions stay.
- **Removed restatements** (surviving location; origin):
  - the width examples → §7.2's table (inline_length), §7.4's table and
    §4.6's list (length prefixes); `73ad568`, cleanroom round 15.
  - updaters and verifiers are readers → §2.3 (the verifier item) and §20.1
    ("is a reader of every structure it processes"); `0ce8fc4`, Batch 1
    (ADR-0027). The restatement calibration 2's C3 refuter found.
  - §4.4's Note → §14.3 ("bit-packed LSB-first: value k occupies bit k mod
    8"); `0ce8fc4`.
  - the coverage-map restatement → §8.1 `[R-CNT-19]` ("Every field of every
    structure is covered by exactly one checksum — excepting the
    equality-checked front signature block and this map's terminal
    checksum fields, per §4.5, and the extent of a record of a type this
    specification has not assigned") and its table (the segment CRC array
    "itself covered by the layer record's crc_of_crc_array"); `ffc6f0d`,
    cleanroom gate 1, and `1297d0a`, round 2.
  - the three-ID gloss → the three IDs at their own sites; `033ef41`,
    ADR-0071.
  - "A name is structural: a duplicate is a validity error at file or layer
    scope (`[R-ENC-15]`, F4, L9), and its length prefix is §7.4's framing,
    not its value." → §4.6 `[R-ENC-15]`, rows F4 and L9; `29e8b62`,
    ADR-0128.
  - "Every non-obvious encoding is followed by a worked numeric example,
    and every sentinel or overloaded encoding additionally has a paired
    conformance vector. All named constants appear once in Appendix B." →
    §24 ("every sentinel, every boundary value, and every …") and Appendix
    B's lead ("Every named constant this specification fixes, collected.");
    `0ce8fc4`.
- **Reworded IDs:** `R-ENC-03`, `R-ENC-04`, `R-ENC-10`, `R-ENC-16`; and
  `R-ENC-05`, which shares `[R-ENC-04]`'s paragraph with its own sentence
  untouched. Thirteen IDs listed in all.
- **Soft items:** `ID_REWORDED_LISTED` ×13 (five new); `TERM_TEXT_CHANGED`
  ×8 and `HEADINGS` carried. Keyword counts unchanged.
- **Questions raised:** none. Held: §4.3's four-vehicles sentence, kept for
  the reason above.

### 2026-09-24 — §2.3: the rest of the reach paragraph in plain words

- **Commit:** `Readable: §2.3 — reach paragraph's rules restated plainly`
  (the commit carrying this entry).
- **Sections:** §2.3, the closing paragraph (`[R-CNF-13]`), sentences three
  to seven.
- **Edits.** Each sentence keeps its decision and loses its dashes:
  - "The test is the property asserted, not the bytes read: a check that
    consumes bytes a future major is free to redefine can still assert
    only a fixed property." → "What matters is the property a check
    asserts, not the bytes it reads: a check can read bytes a future major
    is free to redefine and still assert only a property fixed for every
    major."
  - "A reader MUST apply every reaching condition to a file whatever major
    it declares — an exemption … applies unchanged, `[R-CNT-04]`'s
    residency exemption among them — and MUST treat its failure as
    reject-file on the ground of the requirement stating it rather than
    on capability grounds" → "A reader MUST check every reaching
    condition whatever major the file declares, and MUST treat a failure
    as reject-file under the requirement that states the condition, not
    as a capability refusal; an exemption that the condition's own
    requirement grants for a reason other than the declared major still
    holds, `[R-CNT-04]`'s residency exemption among them." Both MUSTs,
    same subject, same objects; the exemption clause follows instead of
    interrupting.
  - "the distinct diagnostic `[R-CNT-07]` asks for is owed where …" →
    "`[R-CNT-07]`'s distinct diagnostic is given where …".
  - "A verifier that establishes such a failure … the property broken is
    one that major shares (`[R-CNT-24]`), so the finding is not relative
    to format major 1." → "A verifier that finds such a failure … the
    property broken is one shared among all majors (`[R-CNT-24]`)." The
    dropped clause is the consequence of the kept one. "Finds" is the
    plain synonym here; the verifier item's verdict rules still use
    "established" as their term.
  - "Every other condition this specification names is one of a structure
    this text defines for format major 1 alone; it is not assessed …, no
    violation of it is established there, and no §21 row restating it
    records such a file." → "Every other condition concerns a structure
    this document defines for format major 1 alone: it is not checked …,
    no violation of it is found there, and no §21 row records such a
    file."
  The maintainer read the result as much clearer overall, with two
  sentences still hard to parse; they are left for a later pass.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNF-13`, its reason line rewritten to cover the
  whole paragraph.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×8, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-24 — §2.4: two explanatory passages cut

- **Commit:** `Readable: §2.4 — preserve-verbatim gloss and the reject Note
  cut; R-CNF-07 listed` (the commit carrying this entry).
- **Sections:** §2.4, the first paragraph and the closing Note.
- **Edits.**
  1. After `[R-CNF-07]`, the sentences "The same vocabulary is used for
     defined conditions that are not violations (an unknown ancillary
     record is *ignored*, not rejected). **preserve-verbatim** names an
     updater obligation, orthogonal to reader outcomes: a record a reader
     ignores can still be one an updater preserves." are cut; the
     paragraph ends at the ID. The rule sentence is verbatim.
  2. The closing Note, "'Reject' prescribes the scope of unusability, not
     user interface: how failure is reported is implementation
     technique.", is removed. Notes 58 → 57.
- **Removed restatements:**
  - the vocabulary's use for conditions that are not violations → §21.6
    (its table's Defined-behavior column) and §21.5; `0ce8fc4`, Batch 1
    (ADR-0027).
  - preserve-verbatim as an updater obligation orthogonal to reader
    outcomes → the outcome table's own *preserve-verbatim* row ("Binds
    updaters …") and §20.4's MU = 0 / PE = 1 row; same origin.
  - the Note → §2.1's Note ("requirements constrain bytes and observable
    behavior, never implementation technique"); same origin.
- **Reworded IDs:** `R-CNF-07`, listed: only sentences after the ID
  changed, the tool comparing the whole paragraph.
- **Soft items:** `ID_REWORDED_LISTED R-CNF-07` (new) and the seven
  earlier; `TERM_TEXT_CHANGED` ×8 and `HEADINGS` carried. Keyword counts
  unchanged.
- **Questions raised:** none.

### 2026-09-24 — §2.3: the reach paragraph's definitions in plain words

- **Commit:** `Readable: §2.3 — condition and reach defined in plain words;
  invariant is property` (the commit carrying this entry).
- **Sections:** §2.3, the closing paragraph (`[R-CNF-13]`).
- **Edits.** The first sentence, "A **condition** this specification names —
  one malformed state, as §21.1 individuates them, and not the requirement
  that defines it — **reaches** a file …", becomes two: "A **condition** is
  one specific way a file's bytes can fail a requirement of this
  specification; §21.1 says where one condition ends and the next begins,
  one requirement can state several, and reach is decided for each. A
  condition **reaches** a file declaring a format major other than 1 when,
  and only when, the property it violates is one `[R-CNT-24]` fixes for
  every format major version." "Invariant" becomes "property" in the
  paragraph's four uses; §15's and §16's slab and alignment invariants are
  untouched. The test sentence, both MUSTs, the verifier's verdict and the
  closing sentence are otherwise verbatim. "Reaches" stays: the maintainer
  asked about *covers* and *applies to*, and both collide with words in
  use (byte coverage, §5.2; "applies unchanged" in this paragraph).
  "Rule" was asked for in place of "invariant" and declined: F14 reaches
  although its rule, `[R-CNT-06]`, does not as a whole, because the
  property it asserts is `[R-CNT-24]`'s; "rule" would restate the test
  wrongly.
- **Removed restatements:** none beyond the previous entry's.
- **Reworded IDs:** `R-CNF-13`, its reason line in `reworded-ids.txt`
  extended.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×7, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-24 — §2.3: the reach paragraph `[R-CNF-13]` cut to its rules; its Note removed

- **Commit:** `Readable: §2.3 — reach paragraph cut to its rules, its Note
  removed; R-CNF-13 listed` (the commit carrying this entry).
- **Sections:** §2.3, the closing paragraph and its Note. §2.3 is now about
  95 lines, from 144.
- **Edits.** The paragraph falls from 29 lines to 24: two sentences cut
  (below) and one pointer added at the end, "§21.2 lists the rows that
  reach." The definitions of *condition* and *reaches*, the test
  sentence, both MUSTs with the `[R-CNT-04]` exemption clause, the
  verifier's verdict and the closing "every other condition" sentence are
  verbatim. The Note (F14, F5 and F15 worked through the test) is
  removed: the results stand in §21.2's lead-in and the test they follow
  from stays in the paragraph.
- **Removed restatements:**
  - "A file whose version_major is 0 declares no major at all (§6.3): it
    is not a file declaring a format major other than 1, no reach question
    arises for it, and `[R-CNT-07]` rejects it (§21.2, F18)." → §21.2's
    lead-in ("F18 is not an exception but a case outside the premise:
    version_major = 0 declares no major at all, so `[R-CNF-13]`'s premise
    is unmet and `[R-CNT-07]` governs"), §6.3, row F18; `b7ccaed`, the
    pre-round-30 audit (ADR-0118's repairs).
  - "Reach is per condition because a single requirement can state
    several: `[R-CNT-06]` states nine, of which the trailer magic and the
    trailer CRC assert invariants `[R-CNT-24]` fixes and the other seven
    do not." → the definition's own first clause (per condition, not per
    requirement) and §21.2's lead-in (F8, F14, F6 and F1's instances, and
    no other row); `e19e03a`, ADR-0106.
  - the Note → §21.2's lead-in for the results; the reasoning for F14, F5
    and F15 now stands nowhere, being explanatory; `e999df7`, ADR-0105.
    Notes 59 → 58.
- **Reworded IDs:** `R-CNF-13`, listed.
- **Soft items:** `ID_REWORDED_LISTED R-CNF-13` (new) and the six earlier;
  `TERM_TEXT_CHANGED` ×8 and `HEADINGS` carried. Keyword counts
  unchanged.
- **Questions raised:** none. The maintainer's question whether
  *condition* and *reaches* want §3.1 entries stays open; both
  definitions now lead the paragraph.

### 2026-09-24 — §2.3 verifier and updater items; the cannot-establish grounds moved to §21.6

- **Commit:** `Readable: §2.3 — verifier and updater items cut; the
  cannot-establish grounds moved to §21.6; R-CNF-06, R-CNF-11, R-COD-11
  listed` (the commit carrying this entry).
- **Sections:** §2.3 (the updater and verifier list items); §21.6 (a new
  closing paragraph).
- **Edits.**
  1. Verifier item, 37 lines to 21. The "as when" list of five grounds for
     *cannot establish* moves, verbatim, to a new paragraph at the end of
     §21.6, which already holds every condition the list names, with
     `[R-CNF-11]` cited as its authority and "as when" kept so the list
     stays illustrative; §2.3 keeps "(§21.6 names the grounds)". Two dash
     pairs become commas. "That per-requirement report constrains the
     report and not the verdict, as *unexamined* does below" and the
     closing sentence merge into "*Unexamined* is neither a verdict nor
     *cannot establish*; it and the per-requirement report constrain the
     report, not the verdict." Every MUST, MUST NOT and MAY is verbatim.
     The list was not cut because three of its grounds (an unimplemented
     major, an MU = 1 record of an unimplemented type, a decode declined
     on resource grounds) are tied to the verdict nowhere else; only the
     codec ground (§17.4) and the user-metadata bound (§18) are.
  2. Updater item, 7 lines to 6: the tiers sentence joins the definition;
     one gloss cut (below).
  3. §21.6 gains the moved paragraph after "(F35, F36, L24, L25)". It
     closes with no ID of its own, so the inventory tool cannot see it.
- **Removed restatements:**
  - verifier item: "A user-metadata document under an experimental-range
    encoding — one this specification does not assign and a conforming
    file can carry (§21.6) — is not such a ground: no content rule
    attaches there, so nothing is left unchecked, and certification is
    unaffected (`[R-MTA-10]`); encoding 0 and a reserved value are
    violations (§21.5, R1)." → `[R-MTA-10]` ("the record is not among
    `[R-CNF-11]`'s cannot-establish grounds, and at an experimental-range
    encoding certification is unaffected, encoding 0 and a reserved value
    being R1's violations"); `45f9367`, ADR-0066.
  - updater item: "which govern every record type, not only those it does
    not understand" → §20.4 ("Persistence governs every record type");
    `6bcc735`, ADR-0068.
- **Reworded IDs:** `R-CNF-06`, `R-CNF-11`; and `R-COD-11`, whose §17 text
  is untouched: the tool maps a cited-only ID to the first block citing
  it, and that block is now §21.6's paragraph instead of the verifier
  item.
- **Soft items:** `ID_REWORDED_LISTED` for the three above (new) and
  `R-CNF-02`, `R-CNF-03`, `R-CNF-04` carried; `TERM_TEXT_CHANGED` ×8 and
  `HEADINGS` carried. Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-24 — §2.3: the conforming-reader class, `[R-CNF-03]` and `[R-CNF-04]` listed

- **Commit:** `Readable: §2.3 — conforming reader item, three glosses cut;
  R-CNF-03 and R-CNF-04 listed` (the commit carrying this entry).
- **Sections:** §2.3, the second list item only.
- **Edits.** The item falls from 24 lines to 17. Every keyword sentence
  (three MUSTs, one MAY, one MUST NOT) is verbatim; the limits clause
  reads "the minimum guarantees of §21's limits table (§21.9)"; the
  no-subset-profiles sentence reads "software that declines any of
  those", in place of a repeat of the preceding six-item list.
- **Removed restatements:**
  - "in a conforming file such a type is necessarily from the
    experimental range, since a reserved-range type carrying MU = 1 is
    itself a violation" → `[R-CNT-15]` (register rows F35, F36, L24, L25),
    and §21.6's closing paragraph, which draws the inference; `53d6006`,
    the round 7 editorial tail.
  - "(§21.9's `[R-ERR-04]` governs a refusal on that last ground; §21.6's
    closing paragraph names the other two)" → §21.9 `[R-ERR-04]`; §21.6's
    closing paragraph; same origin.
  - the second listing of "a core codec, a core filter, either channel
    layout, a core sample type, an assigned user-metadata encoding, or a
    registered record type" → the item's own preceding sentence;
    `0ce8fc4`, Batch 1 (ADR-0027).
- **Reworded IDs:** `R-CNF-03` and `R-CNF-04`, both listed; `R-CNF-04` only
  because the inventory maps both IDs to the one list item, its own
  sentences being untouched.
- **Soft items:** `ID_REWORDED_LISTED` for `R-CNF-03` and `R-CNF-04` (new),
  `R-CNF-02` carried; `TERM_TEXT_CHANGED` ×8 and `HEADINGS` carried.
  Keyword counts unchanged.
- **Questions raised:** none.

### 2026-09-24 — §2.3: the conforming-file class, `[R-CNF-02]` reworded

- **Commit:** `Readable: §2.3 — conforming file item cut to its rules;
  R-CNF-02 listed` (the commit carrying this entry).
- **Sections:** §2.3, the first list item only.
- **Edits.** The item falls from 24 lines to 13. "It is always conformance
  to a stated format major version" folds into the first sentence
  ("always at a stated format major version"); the other-major sentence
  keeps every clause in one sentence; the two conduct sentences become
  one: "A writer obligation that governs conduct rather than output, or
  whose violation this specification expressly declares not to be a
  file-conformance violation, binds the writer and never makes a file
  nonconforming." "Conduct rules bind the actor, the predicate binds the
  bytes" is dropped, the second half being the item's own second
  sentence.
- **Removed restatements:**
  - the three examples of conduct rules (where a value is published, which
    registry version a writer targets, §10.3 and §18.3, the barriers a
    commit performs, §9.2) → each at its site; `ed3395e`, cleanroom
    round 3.
  - the enumeration of the expressly-declared cases (§6.3's flags rules
    with §20.3 step 6 and §20.5, §6.2's pre-trailer gap against
    `[R-LIF-02]` step 5, §20.3 step 4's bar) → each declared at its site,
    as the cut sentence itself said; `df71fb8`, the pre-round-31 audit.
    What is lost is the enumeration's closure ("these are the cases this
    text states"), a fact about the text, not a rule.
- **Reworded IDs:** `R-CNF-02`, listed in `conformance/tools/reworded-ids.txt`
  with the reason above. The reworded paragraph decides the same things:
  file conformance is a predicate on bytes at a stated major; another
  major is judged only by reaching conditions; a capability refusal is
  not a finding; conduct obligations and expressly-carved-out obligations
  bind the writer and never the file's conformance.
- **Soft items:** `ID_REWORDED_LISTED R-CNF-02` (new); `TERM_TEXT_CHANGED`
  ×8 and `HEADINGS` carried. Keyword counts unchanged (the item carried no
  keyword).
- **Questions raised:** none.

### 2026-09-24 — §3.3 removed

- **Commit:** `Readable: §3.3 — removed; its point stands in §2.3 and §20.1`
  (the commit carrying this entry).
- **Sections:** §3.3 (heading and its one Note), gone; §3 now ends at §3.2.
- **Edits.** The subsection was a heading over a single Note ("Part I
  (container) is independent of Part II (array model) by construction: no
  Part I structure requires decoding sample payloads, so appenders, and
  rewriters that carry a layer forward, operate on files whose layers they
  cannot decode — that independence is load-bearing for the updater rules
  of §7 and §20."). Nothing in the specification, the tools or the vectors
  cites §3.3; ADR-0129 and ADR-0131 mention the Note and quote edition A,
  which is unchanged. The maintainer waived the standing rule that headings
  stay, for an uncited leaf, with the renumbering step to follow; that step
  maps 3.3 to nothing.
- **Removed restatements:** the Note's operative point, that an updater
  operates on layers it cannot decode → §2.3, the updater class ("without
  necessarily understanding all of its content"), and §20.1 ("a writer that
  extends an input file is an appender and an updater, whatever it
  decodes"). Added by `d855308`, Batch 2 (ADR-0028); its actor list
  repaired by ADR-0131. The "independent by construction" framing was
  design commentary and now stands nowhere; the same is true of the
  container-reader sentence cut from §1 on 2026-09-23, for which the §1
  entry named this Note as the surviving location. Neither bound anything.
- **Reworded IDs:** none.
- **Soft items:** `HEADINGS` now also carries the removed `#### 3.3` (129
  headings in B against 130 in A); the info line's Note count falls to 59.
  `TERM_TEXT_CHANGED` ×8 unchanged.
- **Questions raised:** none; the heading waiver was the maintainer's own
  call, made in session.

### 2026-09-24 — §3.1: *tile* says what it means for a tile to carry a channel

- **Commit:** `Readable: §3.1 — tile entry defines "carries"` (the commit
  carrying this entry).
- **Sections:** §3.1 only.
- **Edits.** In the *tile* entry, "one cell of the grid for one channel"
  becomes "one cell of the grid carrying one channel", and the sentence "A
  tile *carries* a channel when its payload holds that channel's samples
  at the cell's positions." is added. The maintainer asked for a
  definition of *carry*, which the document uses 167 times: mostly as
  ordinary English (a record carries a flag), a dozen times in this
  technical sense (the tile carrying that channel, §3.1 *fill value*, §3.2,
  §13, §14.5), and as "carried forward" in §20.4's updater sense. A §3.1
  term would govern all three, so the technical sense is stated where the
  document first uses it instead. The added sentence restates the entry's
  own two clauses and §3.2's "the tile carrying that channel at that
  coordinate"; no new term, no new content.
- **Removed restatements:** none.
- **Reworded IDs:** none. No keyword, no ID.
- **Soft items:** `TERM_TEXT_CHANGED` for *tile*, added to the seven from
  earlier entries; `HEADINGS`.
- **Questions raised:** none; a *carry* term of its own was considered and
  not asked for.

### 2026-09-24 — §3.1: *tile index* moved to follow *tile*

- **Commit:** `Readable: §3.1 — tile index defined directly after tile` (the
  commit carrying this entry).
- **Sections:** §3.1 only.
- **Edits.** The *tile index* entry (three lines, verbatim) moves from
  after *slab* to directly after *tile*, so that the tile-index entry
  *tile* names, and the sentinel *addressed tile / stored tile* names, are
  defined before use. The list now runs: file, front signature block,
  generation, trailer, directory, layer, dimension, rank, channel, channel
  layout, sample, coordinate, tile, tile index, fill value, addressed tile
  / stored tile, slab, user metadata.
- **Removed restatements:** none.
- **Reworded IDs:** none.
- **Soft items:** unchanged (`TERM_TEXT_CHANGED` ×7, `HEADINGS`); the moved
  text is byte-identical.
- **Questions raised:** none.

### 2026-09-24 — §3.1: *fill value* moved ahead of *addressed tile / stored tile*

- **Commit:** `Readable: §3.1 — fill value defined before the stored-tile
  entry uses it` (the commit carrying this entry).
- **Sections:** §3.1 only.
- **Edits.** The *fill value* entry (two lines, verbatim) moves from after
  *addressed tile / stored tile* to before it, so that "an addressed tile
  that is not stored reads as fill" follows the definition of fill. The
  list now runs: file, front signature block, generation, trailer,
  directory, layer, dimension, rank, channel, channel layout, sample,
  coordinate, tile, fill value, addressed tile / stored tile, slab, tile
  index, user metadata.
- **Removed restatements:** none.
- **Reworded IDs:** none.
- **Soft items:** unchanged (`TERM_TEXT_CHANGED` ×7, `HEADINGS`); the moved
  text is byte-identical.
- **Questions raised:** none.

### 2026-09-24 — §3.1: *addressed tile / stored tile* says what "addressed" means

- **Commit:** `Readable: §3.1 — addressed tile defined by the index entry,
  not by "every tile"` (the commit carrying this entry).
- **Sections:** §3.1 only.
- **Edits.** The entry's first sentence, "every tile of a layer is
  *addressed*. A tile is *stored in a generation* if and only if that
  generation's tile-index entry for it is not the sentinel (§15)", becomes
  "a tile is *addressed* in a generation if that generation's tile index
  has an entry for it: the tiles of the layer's grid under the geometry
  that generation declares (§11.2, §15). It is *stored in a generation* if
  and only if that entry is not the sentinel (§15)". The rest of the entry
  is unchanged. Derived from §11.2 `[R-GEO-03]` (the addressed-tile count
  is the number of tile-index entries, N or C · N from the declared
  geometry) and §15.2. The maintainer asked why the term exists if every
  tile is addressed; the answer (a tile a later commit no longer
  addresses, §20.3 step 4, is neither stored nor a sentinel, and the
  counts and caps are quantified over addressed tiles) is why the
  definition now names the index entry rather than "every tile". The
  third state is left to §20.3 at the maintainer's choice. The term's name
  stays: it is a hard item of the contract and appears in six register
  rows.
- **Removed restatements:** none.
- **Reworded IDs:** none. No keyword, no ID.
- **Soft items:** `TERM_TEXT_CHANGED` for *addressed tile / stored tile*,
  added to the six from earlier entries; `HEADINGS`.
- **Questions raised:** none; dropping the term would be an ADR against A,
  and was not asked.

### 2026-09-23 — §3.1: *fill value* entry, "per-channel" dropped

- **Commit:** `Readable: §3.1 — fill value entry, redundant per-channel
  dropped` (the commit carrying this entry).
- **Sections:** §3.1 only.
- **Edits.** *fill value*: "the per-channel value that a channel's samples
  take …" becomes "the value that a channel's samples take …"; the sentence
  already says whose value it is.
- **Removed restatements:** none.
- **Reworded IDs:** none. No keyword, no ID.
- **Soft items:** `TERM_TEXT_CHANGED` for *fill value*, added to the five
  from earlier entries; `HEADINGS`.
- **Questions raised:** none.

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
