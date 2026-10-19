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
- **§5** (declared done 2026-09-28): §5.1's anatomy sentence and its second
  Example reworded (`711a94f`, `5296c8b`); §5.2's `[R-CNT-02]` and
  `[R-CNT-21]` paragraphs reworded, the latter split in four with three
  ID-less rule paragraphs, and its Rationale cut (`d9f34ab`, `2bef8ff`);
  `R-CNT-01`, `R-CNT-02`, `R-CNT-21` listed. Candidate seeds: "A reader MUST
  NOT interpret it" and "no total is owed" (ID-less paragraphs); "its
  extent is still enumerated" (the decode sentence); "never an
  under-count" (`[R-CNT-21]`).
- **§6** (declared done 2026-09-29): every subsection reworded (`2124a23`,
  `f3a14cf`, `f60d1a9`, `083cc8d`), two of the commits being the
  maintainer's own edits reviewed; residency defined in §6.1; `R-CNT-04`
  through `-10`, `-24` and `-26` listed; the tables, the Rationale and
  §6.2's first Note untouched. SHOULD is 46 in A and 47 in B
  (`[R-CNT-26]`'s ellipsis written out). Candidate seeds: the residency
  definition's "takes no further range request"; "though no conforming
  commit produces one" (`[R-CNT-05]`); "MUST NOT set any other"
  (`[R-CNT-08]`, stated also by `[R-WRT-06]`: a cut there tests restraint,
  a flip tests reach); "never treats the body's prefix as the requested
  range" (`[R-CNT-10]`).
- **§7** (declared done 2026-10-05): every rule paragraph but `[R-CNT-12]`
  and `[R-CNT-16]`/`[R-CNT-17]` reworded (`9a67884` through `4b0d01f`);
  `[R-CNT-25]` moved from §7.1 to the end of §7.3 in two paragraphs, the
  first without an ID; four citations re-pointed; `R-CNT-11`, `-13`,
  `-14`, `-15`, `-18`, `-22`, `-23`, `-25`, `R-MTA-01`, `R-SEC-05`,
  `R-SEC-06`, `R-PRV-03` listed; the tables, the Example and both Notes
  untouched. Candidate seeds: "an extent slot of (0, 0) or an
  extent_length less than 5" (the ID-less paragraph; rows F21, F22, L10,
  L11 restate it, so a flip there tests reach against the register); "The
  quarantine overrides the owning-scope mapping" (`[R-CNT-25]`);
  "including none (§21.6)" (`[R-CNT-14]`, a pointer whose target states
  the rule); "MU = 1 is reject-file, and MU = 0 is ignore-record"
  (`[R-CNT-15]`); "With MU = 0 an unknown sub-record type is
  ignore-record" (`[R-CNT-18]`).
- **§8** (declared done 2026-10-08): `[R-CNT-19]` and `[R-CNT-20]` reworded
  (`fe9c082`), the former restoring the terminal- and interior-checksum
  statements the §4.5 cut had lost; the table, "Verification is not
  optional" and the Note untouched. Candidate seeds: "covered by no further
  checksum" and "covered by exactly one further checksum" (`[R-CNT-19]`,
  each stated once now that §4.5's copy is gone); "a user-metadata extent's
  CRC, ignore-record" (`[R-CNT-20]`, restated by R2).

- **§9** (read through 2026-10-13 to 2026-10-14, after the first pass of
  2026-10-08): every subsection; `R-LIF-01` through `-06` and `-08` listed,
  `R-LIF-09` added by ADR-0134 in both editions; §9.2's second Note, §9.3's
  first Note, §9.5's first Note and §9.7's first paragraph re-cut on the
  maintainer's questions. Candidate seeds: "by at least 128" (`[R-LIF-02]`,
  restated at §9.3 and §20.3 step 6: a flip tests reach); "MUST NOT scan
  backward" (`[R-LIF-05]`, restated at §9.6 and §9.2's Example); "only one
  writer at a time" (`[R-LIF-05]`, restated at §1 and §20); "truncate to F
  before step 1 of `[R-LIF-02]`, or overwrite from F" (`[R-LIF-04]`, stated
  once); "MUST report the candidate it settled on and how many candidates
  it rejected" (`[R-LIF-06]`, stated once); "MUST leave the physical file
  length equal to the candidate's committed file length" (`[R-LIF-09]`,
  stated once, identical in both editions).
- **§10** (read through 2026-10-14, one edit): `R-EXT-01`, `-03`, `-04`,
  `-05` listed by the spruce-up. Candidate seeds: "never a minor revision
  and never an implementation's private convention" (`[R-EXT-01]`);
  "sufficient for independent implementation without consulting any
  implementation" (`[R-EXT-04]`); "the registry is machine-readable
  convenience, never a second authority" (`[R-EXT-05]`).

- **§11** (read through 2026-10-14 to 2026-10-15): `R-GEO-01`, `-03`,
  `-04`, `-05`, `-06` listed by the spruce-up; §11.1's Rationale in plain
  language, §11.2's Note and Example and §11.4's Note and Example re-cut
  at the maintainer's ask. Candidate seeds: "channel count 0" among
  `[R-GEO-01]`'s three barred values (row L32 restates it: a flip tests
  reach); "a reader MUST treat one exceeding 2⁶³ − 1 as a validity error
  at layer scope" (`[R-GEO-03]`); "stated in a form that forms no product
  (§4.2)" (`[R-GEO-04]`, stated once); "the last-declared dimension varies
  fastest" (`[R-GEO-05]`); "c · N + s for a planar layer" (`[R-GEO-06]`,
  restated in §14 and §15's worked figures: a flip tests reach).

- **§12** (read through 2026-10-15): `R-TYP-03`, `-04`, `-05` listed by
  the spruce-up, `R-TYP-03`'s lead-in and §12.3's Example edited by the
  maintainer. Candidate seeds: "a reader MUST NOT infer an element size or
  any semantics for a type value this specification does not assign"
  (`[R-TYP-03]`, stated once); "never quieted, canonicalized or collapsed"
  (`[R-TYP-04]`); "bits 14–7 the biased exponent, and bits 6–0 the
  trailing significand" (`[R-TYP-02]`, stated once); "every bit pattern of
  the element size is a valid fill" (`[R-TYP-05]`, restated at §13.2: a
  flip tests reach).

- **§13** (read through 2026-10-15 to 2026-10-19, no edit but §13.2's
  Rationale gaining the reader's exemption): `R-TYP-06`, `-08`, `-10`
  listed. Candidate seeds: "MUST NOT substitute a type-derived default or
  any other value" (`[R-TYP-06]`, stated once); "`0x00` (false) or `0x01`
  (true)" (`[R-TYP-07]`, restated at §14.2 and row L35: a flip tests
  reach); "MUST return … that channel's fill" for the sentinel
  (`[R-TYP-08]`); "SHOULD record all-zero bytes" (`[R-TYP-10]`, stated
  once); "MUST NOT return" a value from an unverified chain
  (`[R-TYP-09]`).

Stretches done through §8 on 2026-10-08; §9 and §10 on 2026-10-14; §11 and
§12 on 2026-10-15; §13 on 2026-10-19.

**Fidelity round 1 ran on 2026-10-08** over B at `5220d1a`, the head of
`readable` with §1 through §8 done (`wf_e2a8d709-b50`;
[2-round-1/findings.md](2-round-1/findings.md)): no seeds, the repository's
`spec/tarn.md` as edition B, 29 agents on `claude-sonnet-5`, 74 minutes.
**No byte-level divergence and no addition.** Every blind walk and quiz
taker read the same rules from both editions; the sweeps and the adversary
found nothing B decides that A does not. Six findings were graded LOSS,
unanimously, and upheld on refute: every one a cut this log records and the
maintainer approved, every one explanatory prose, and for every one the
hand-check finds the rule standing in B in text identical to A. They are
`[R-CNF-03]`'s experimental-range aside (the entry for 2026-09-24 below),
`[R-CNF-02]`'s closed enumeration (the standing question), the Part I /
Part II Note of §3.3 with §1's roadmap sentence, §2.4's preserve-verbatim
bridge and its reject Note, and §2.3's three-row reach Note. All six go to
the maintainer with both texts quoted, as ADR-0133 decision 4 says; none is
changed in B by this round. The round found the §4.5 cut of 2026-09-25 and
its §8.1 restoration lossless, the §7.1 → §7.3 move lossless, and every
other restatement removal in this log standing where the log says it does.

**The maintainer's rulings, 2026-10-08: all six kept cut** ("Keep all six
cut; record the rulings in the edit log"). `[R-CNF-03]`'s experimental-range
aside stays cut: the rule stands at §7.2 `[R-CNT-15]`, rows F35 and F36 and
§21.6's closing paragraph. `[R-CNF-02]`'s closed enumeration stays cut, and
the standing question from calibration 2 closes with it: each case is
declared at its site, §6.3, §6.2 and §20.3 step 4. §3.3's Note and §1's
roadmap sentence stay cut: the permission stands at §20.1 and §20.4, the
point at §2.3's updater definition. §2.4's preserve-verbatim bridge stays
cut: the rules stand at §20.4 `[R-WRT-05]`, the outcome table's own row and
§21.5. §2.4's reject Note stays cut: §2.1's Note states the principle for
every requirement. §2.3's three-row reach Note stays cut: the results stand
in §21.2's lead-in. No edit to B follows from the round.

**Fidelity round 2 ran on 2026-10-12** over B at `7b5b9a7`, the head of
`readable` with §1 through §8 rewritten, §9 re-cut and §10 through the
appendices spruced up (`wf_ed2decfe-4e2`;
[3-round-2/findings.md](3-round-2/findings.md)): no seeds, the repository's
`spec/tarn.md` as edition B, 30 agents on `claude-sonnet-5`, 66 minutes, the
launch turn the single word "Go". Before the launch the word-diff preflight
the spruce-up owed read every word lost or gained over its twenty-one
commits ([3-round-2/word-diff.md](3-round-2/word-diff.md)) and found one
transcription loss, "above" in §9.7's bound sentence, restored as `7b5b9a7`
(the entry below). **No byte-level divergence and no addition, and nothing
graded LOSS or ADDITION by any lane from §5 to the end of the document**:
the spruce-up series drew no finding from any instrument. Eight groups were
graded LOSS by at least one triage pass, every one a cut of explanatory
prose in the front matter and §1–§4 that this log records: round 1's items
3 through 6 (the §3.3 Note and §1's roadmap sentence, §2.4's
preserve-verbatim bridge, §2.4's reject Note, §2.3's reach Note), all ruled
kept cut on 2026-10-08, and three new grades on cuts of 2026-09-23 and
2026-09-25 (§4.4's bit-numbering Note, standing at §14.3; the tail of §4.7's
layout-table Note, standing at §4.6 `[R-ENC-15]`, rows F4 and L9 and
`[R-ENC-16]`; the front-matter clause on vectors citing identifiers,
standing at §2.2 and §24 `[R-VEC-02]`). Six split refuters stood on
EQUIVALENT, the bridge's loss-refuter stood on LOSS and the reach Note's
overturned it; every one is EQUIVALENT by hand and all eight go to the
maintainer with both texts, as decision 4 says. Round 1's items 1 and 2
were graded EQUIVALENT this time. None is changed in B by this round. The
ten blind-walk findings are shared text of A, for the ledger.

**The maintainer's rulings, 2026-10-13: all three kept cut** ("Keep the
three cuts"). §4.4's bit-numbering Note stays cut: the mapping of boolean
samples to bits stands at §14.3, with its own pointer to §4.4, and
`[R-ENC-08]` is cited nowhere else. The tail of §4.7's layout-table Note
stays cut: the duplicate-name rule stands at §4.6 `[R-ENC-15]` and rows F4
and L9, "every other field this specification defines is structural" at
`[R-ENC-16]`, and the remaining sentences describe the document's own
conventions. The front-matter clause on vectors stays cut: §2.2 makes the
identifier permanent and §24 `[R-VEC-02]` ties every vector to its row's
governing requirement identifier. Round 1's items 3 through 6, graded again
by this round, stand ruled from 2026-10-08. No edit to B follows from the
round.

## Entries

### 2026-10-19 — §14.4, §2.2: the retired-identifier Note moved to where the rule is

- **Commit:** `Readable: §14.4, §2.2 — the R-SER-04 withdrawal Note moved from
  §14.4 to §2.2; R-SER-04 listed` (the commit carrying this entry).
  Previous: `52dbc95` (§14.2's Rationale).
- **Sections:** §14.4 (the first Note, removed); §2.2 (a Note added after
  the prefixes paragraph). Both non-normative. At the maintainer's ask
  ("Can we remove the first note of section 14.4"); proposed as a move
  after a trial showed a plain removal fails both gates; approved ("Go,
  both").
- **Why a move and not a cut.** `tarn_inventory.py`'s hard item requires
  the identifier set of B to equal A's, and `[R-SER-04]` is in A's only
  through this Note; `tarn_check`'s SPEC-02 fails a hole in a prefix's
  numbering unless the identifier is recorded somewhere in the text, and
  SPEC-01 requires a withdrawn one to have no definition site. The fact
  therefore stays in B; §2.2, which states the retirement rule, is where a
  reader would look for it.
- **Edits.**
  1. §14.4: "> **Note.** Identifier `[R-SER-04]`, which earlier governed
     this subsection, is withdrawn; per §2.2 it is permanently retired and
     never reassigned." removed. Added by ADR-0038 (`f38b6ec`), which
     withdrew `[R-SER-04]` when interleaved bool values became single
     bytes.
  2. §2.2, after "existing prefixes are never reassigned.": "> **Note.**
     One identifier is retired: `[R-SER-04]`, which once governed §14.4,
     is withdrawn and never reassigned." The same fact in the same words
     but for "per §2.2", which the placement makes redundant.
- **Removed restatements:** none; a relocation. Notes unchanged in count.
- **Reworded IDs:** `R-SER-04`, listed: the inventory takes the Note as the
  withdrawn identifier's governing paragraph and sees it moved, which is
  the case the list exists for; the identifier is defined nowhere in
  either edition.
- **Soft items:** `ID_REWORDED_LISTED` ×127 (the one new); the carried
  items as before. Keyword counts unchanged. B is 4,787 lines and
  48,735 words.
- **Questions raised:** none. `tarn_check`'s WITHDRAWN_IDS message for
  `R-SER-04` ("§14.4 records the withdrawal") is a string, not a check;
  updated to §2.2 on `main` behind `gate.sh` and merged, the same day.

### 2026-10-19 — §14.2: the boolean-byte Rationale without its history

- **Commit:** `Readable: §14.2 — the boolean-byte Rationale argues the rule,
  not the draft it replaced` (the commit carrying this entry). Previous:
  `ff7bac9` (§14.1's layout paragraph).
- **Sections:** §14.2, the Rationale after `[R-SER-08]`. Non-normative. At
  the maintainer's ask ("should not mention 'earlier text'"); proposed
  with before and after; approved ("Go").
- **Edit.** The Rationale came in with ADR-0051 (`d8b8418`), which added
  the reader's return rule to a §14.2 that carried only the writer's
  constraint, and it argued against that draft: "and the earlier text
  answered only the first", "so the constraint stays", "But leaving the
  return value undefined bought nothing". Now: "and both need an answer",
  "so the constraint stands", "Leaving the return value undefined would
  buy nothing". The four reasons kept: the two questions differ; one
  encoding per value serves §14.5's padding check, `[R-COD-10]`'s stride
  detection and Appendix G's reproducibility; an undefined return lets
  two conforming readers disagree on a sample; the charitable path costs
  nothing. "Earlier text" occurs nowhere else in B.
- **Removed restatements:** none. Word-level diff: "the earlier text
  answered only the first", "stays", "But", "bought" lost; "both need an
  answer", "stands", "would buy" gained.
- **Reworded IDs:** none; a Rationale.
- **Soft items:** `ID_REWORDED_LISTED` ×126; the carried items as before.
  Keyword counts unchanged. B is 4,788 lines and 48,740 words.
- **Questions raised:** none.

### 2026-10-19 — §14.1: the maintainer's edit to the layout field's paragraph, reviewed; R-SER-06 listed

- **Commit:** `Readable: §14.1 — maintainer's edit, reviewed: the layout
  field's value set reordered; R-SER-06 listed` (the commit carrying this
  entry). Previous: `b96560c` (§14.1's bullets).
- **Sections:** §14.1, `[R-SER-06]`'s paragraph.
- **The maintainer's edit.** "Field values: 0 is invalid; 1 = interleaved
  and 2 = planar are the only values this specification defines and the
  only values a writer MAY emit; values 3 through 255 are reserved
  without semantics." → "1 = interleaved and 2 = planar are the only
  values this specification defines for the field, and the only values a
  writer MAY emit; 0 is invalid, and values 3 through 255 are reserved
  without semantics." The defined values first, "for the field" added,
  the invalid and reserved values after; the MAY and the reader's MUST
  verbatim. Re-wrapped by the driver.
- **Flagged and resolved.** The edit first read "0 is permanently
  invalid". A says "0 is invalid" and makes no promise about future
  versions for this field, as it makes none for the type and
  linearization fields' zeros; "permanently" would have decided what A
  leaves open (new content, a decision against A by ADR). The maintainer
  dropped the word ("Drop permanently, Go").
- **Removed restatements:** none.
- **Reworded IDs:** `R-SER-06`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×126 (the one new); the carried
  items as before. Keyword counts unchanged. B is 4,788 lines and
  48,743 words.
- **Questions raised:** none.

### 2026-10-19 — §14.1: the two layout bullets in short sentences; §13 read through

- **Commit:** `Readable: §14.1 — the value sequence's two bullets in short
  sentences; R-SER-01's line extended` (the commit carrying this entry).
  Previous: `58dd3bb` (§13.2's Rationale).
- **Sections:** §14.1, the two bullets `[R-SER-01]` governs. At the
  maintainer's ask ("the two bullets are pretty complexly stated, hard to
  parse"); proposed with before and after and the inventory; approved
  ("Go"). §13 declared done ("Section 13 is done"), no edits saved;
  added under "Ready for calibration 2".
- **Edits.** Each bullet now says in turn what the tile holds, how its
  sequence runs, and its length.
  1. Planar: "carries exactly the values of channel c at the tile's P
     positions: value k of the sequence is channel c's value at in-tile
     ordinal k, and the sequence has V = P values" → "carries one channel,
     c, at the tile's P positions and nothing else. Its sequence runs
     through the positions in in-tile order: value k is channel c's value
     at in-tile ordinal k. The sequence has V = P values."
  2. Interleaved: "carries all C channels at the tile's P positions,
     sample-major: value k of the sequence is channel (k mod C)'s value at
     in-tile ordinal k div C, with each sample's channel values adjacent in
     declared channel order, and the sequence has V = P · C values" →
     "carries every channel at the tile's P positions. Its sequence is
     sample-major: it runs through the positions in in-tile order and,
     within each position, through the channels in declared order, so that
     value k is channel (k mod C)'s value at in-tile ordinal k div C and
     each sample's channel values sit together. The sequence has V = P · C
     values." Sample-major, used nowhere else, is spelled out before its
     formula; "adjacent in declared channel order" becomes the order
     clause and "sit together".
  Every ordinal, formula, count and the §11.4 pointer kept; no keyword
  in either bullet.
- **Removed restatements:** none. Word-level diff: "exactly", "all",
  "adjacent" and connectives lost; "one", "nothing else", "runs through",
  "within each position", "sit together" gained.
- **Reworded IDs:** `R-SER-01`, already listed; line extended.
- **Soft items:** `ID_REWORDED_LISTED` ×125; the carried items as before.
  Keyword counts unchanged. B is 4,788 lines and 48,741 words.
- **Questions raised:** none.

### 2026-10-15 — §13.2: the fill Rationale says readers need not screen value bytes

- **Commit:** `Readable: §13.2 — the fill Rationale points at the reader's
  exemption from screening value bytes` (the commit carrying this entry).
  Previous: `fd87472` (§12.3 and §13.1).
- **Sections:** §13.2, the Rationale after `[R-TYP-07]`. Non-normative.
- **The maintainer's question.** Why 0x01 alone for true, given the reader
  cost of checking every bool byte. Answered from ADR-0036 (one value, one
  encoding; value identity throughout is byte equality, which the padding
  check and channel-entry comparison rely on) and ADR-0038 (the value-byte
  rule binds writers with the verifier as detector; `[R-SER-08]` says a
  reader is not obligated to screen and returns every nonzero byte as
  true). The Rationale argued the fill rule without naming the exemption,
  which is where the question came from.
- **Edit.** One sentence appended, in the maintainer's words ("need not"
  rather than "never", a combined reader-verifier being free to screen):
  "Readers need not screen value bytes for it (§14.2, `[R-SER-08]`)."
  Derived from A's own `[R-SER-08]` ("A reader is not obligated to screen
  decoded content"); B saying what A implies, for the round to grade.
- **Removed restatements:** none.
- **Reworded IDs:** none; a Rationale.
- **Soft items:** `ID_REWORDED_LISTED` ×125; the carried items as before.
  Keyword counts unchanged. B is 4,787 lines and 48,721 words.
- **Questions raised:** none.

### 2026-10-15 — §12.3, §13.1: the maintainer's edits, reviewed; §12 read through

- **Commit:** `Readable: §12.3, §13.1 — maintainer's edits, reviewed; R-TYP-10
  listed` (the commit carrying this entry). Previous: `1309ac7` (the merge
  of main's Q-D7); the spec's previous commit `3ed24c3`.
- **Sections:** §12.3, the channel-entry Example; §13.1, `[R-TYP-10]`.
- **The maintainer's edits.**
  1. §12.3's Example: "type float32, fill the quiet NaN `0x7FC00000` is the
     twelve bytes" → "type float32, with fill of the quiet NaN
     `0x7FC00000` is the twelve bytes". Every byte and figure kept.
  2. §13.1, `[R-TYP-10]`: "read back as a value consumers of the
     conventional zero default will not expect" → "… a value that
     consumers …". The SHOULD verbatim; same statement.
- **Read through.** §12 declared done by the maintainer ("section 12 is
  done"); added under "Ready for calibration 2".
- **Removed restatements:** none.
- **Reworded IDs:** `R-TYP-10`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×125 (the one new); the carried
  items as before; the Example's numbers unchanged. Keyword counts
  unchanged. B is 4,786 lines and 48,710 words.
- **Questions raised:** the maintainer asked why a bool byte is 0x01 alone
  for true, fearing a reader-side cost of checking every byte; answered
  from ADR-0036 and ADR-0038 (one value, one encoding, byte equality being
  value identity throughout; readers are not obligated to screen and
  `[R-SER-08]` has a reader take every nonzero byte as true; the verifier
  is the detector). No edit.

### 2026-10-15 — §12.2: the maintainer's edit, reviewed; the value set's lead-in counts its ranges

- **Commit:** `Readable: §12.2 — maintainer's edit, reviewed: the type
  field's values fall into five ranges` (the commit carrying this entry).
  Previous: `c21a48d` (§11.4's Example).
- **Sections:** §12.2, `[R-TYP-03]`'s paragraph.
- **The maintainer's edit.** "The field's values: 0 is invalid; 1 through
  13 are assigned per §12.1; …" → "The type field's values fall into
  five ranges: 0 is invalid; 1 through 13 are assigned per §12.1; …".
  The field named; the count the list's own (0; 1–13; 14–19; 20–0x7FFF;
  ≥ 0x8000). The five value cases, both MUSTs and the MUST NOT verbatim.
  Re-wrapped by the driver.
- **Removed restatements:** none.
- **Reworded IDs:** `R-TYP-03`, already listed; line extended.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before.
  Keyword counts unchanged. B is 4,786 lines and 48,707 words.
- **Questions raised:** the maintainer floated a ledger question on 2-bit
  and 4-bit unsigned integer types for packable small-range counts;
  drafted for his word (Q-D7 if opened).

### 2026-10-15 — §11.4: the ordinals Example in sentences, its three arrows gone; §11 read through

- **Commit:** `Readable: §11.4 — the ordinals Example in sentences, its three
  arrows gone` (the commit carrying this entry). Previous: `0db63fe`
  (§11.4's Note).
- **Sections:** §11.4, the Example after `[R-GEO-06]`. Non-normative. The
  block the maintainer meant by "written a bit tersely"; proposed with
  before and after and the number sequence checked; approved ("Go").
- **Edit.** "The layer of §11.2's example, grid (G_y, G_x) = (4, 8).
  Spatial ordinals: tile (0, 0) → 0; tile (0, 1) → 1; tile (1, 0) → 1·8
  + 0 = 8. The coordinate (y, x) = (300, 700) lies in tile (1, 2) → s =
  1·8 + 2 = 10, at in-tile position (44, 188) → in-tile ordinal 44·256 +
  188 = 11,452. …" → "Take the layer of §11.2's example, with grid (G_y,
  G_x) = (4, 8). Under linearization 1, tile (0, 0) has spatial ordinal 0,
  tile (0, 1) has ordinal 1, and tile (1, 0) has ordinal 1·8 + 0 = 8. The
  coordinate (y, x) = (300, 700) lies in tile (1, 2), whose spatial
  ordinal is s = 1·8 + 2 = 10, at in-tile position (44, 188), whose
  in-tile ordinal is 44·256 + 188 = 11,452. …"; the planar sentence
  "the tile carrying channel 2" reads "the tile that carries channel 2".
  Every figure kept in order (the number sequence identical before and
  after; the arithmetic re-done by hand: 300 div 256 = 1, 700 div 256 =
  2, 300 mod 256 = 44, 700 mod 256 = 188, 44·256 + 188 = 11,452, 2·32 +
  10 = 74); each arrow replaced by the sentence it stood for; "Under
  linearization 1" is the list's own qualifier a line above.
- **Read through.** §11 is done (§11.1 to §11.4, 2026-10-14 to
  2026-10-15); added under "Ready for calibration 2".
- **Removed restatements:** none. Word-level diff: "Spatial ordinals",
  "carrying" lost; "Take", "Under linearization 1", "has", "whose",
  "is", "carries" gained.
- **Reworded IDs:** none.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before;
  the Example's numbers unchanged. Keyword counts unchanged. B is 4,785 lines and 48,702 words.
- **Questions raised:** none.

### 2026-10-15 — §11.4: the linearization Note in ordinary sentences

- **Commit:** `Readable: §11.4 — the linearization Note in ordinary
  sentences` (the commit carrying this entry). Previous: `0b9ed09`
  (§11.2's Note and Example).
- **Sections:** §11.4, the Note after the Example. Non-normative. The
  maintainer found a block of §11.4 terse and "LLM obvious"; the Note was
  proposed and approved ("Go"), the Example being the block he meant
  (the next entry).
- **Edit.** "Linearization fixes the mapping from *declared dimension
  order* to bytes; it says nothing about axis direction or orientation
  (whether y points up or down is semantics, carried in user metadata,
  §18). Column-major ecosystems (Fortran, Julia, MATLAB) write zero-copy
  by declaring dimensions in reversed order — the same convention their
  HDF5 and netCDF bindings already apply." → "Linearization decides only
  how the declared dimension order maps to bytes. It carries no notion of
  axis direction or orientation: whether y points up or down is
  semantics, and that travels in user metadata (§18). A column-major
  ecosystem such as Fortran, Julia or MATLAB gets zero-copy writes by
  declaring its dimensions in reversed order, which is the convention its
  HDF5 and netCDF bindings already apply." Five facts kept; the semicolon,
  the parenthesis and the dash gone; the italics on "declared dimension
  order" dropped; "semantics" and "zero-copy" kept as the document's
  words.
- **Removed restatements:** none. Word-level diff: "fixes", "mapping",
  "says nothing about", "carried", "same", "their" lost; "decides only
  how", "carries no notion", "travels", "such as", "gets", "which" gained.
- **Reworded IDs:** none.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before.
  Keyword counts unchanged. B is 4,784 lines and 48,688 words.
- **Questions raised:** none.

### 2026-10-15 — §11.2: the ceiling-division Note and the Example without dashes

- **Commit:** `Readable: §11.2 — the ceiling-division Note and the Example
  without dashes` (the commit carrying this entry). Previous: `dc66fc9`
  (§11.1's Rationale).
- **Sections:** §11.2, the Note and the Example after `[R-GEO-03]`. Both
  non-normative. At the maintainer's ask ("First note of 11.2 needs some
  dashes fixed"); proposed with before and after, both taken ("Go, both").
- **Edits.**
  1. The Note: "whose intermediate sum can exceed 2⁶³ − 1 — the declared
     valid domain (§4.2) and the range of signed 64-bit integers — for
     large extents, even though it fits an unsigned 64-bit integer" →
     "avoids the idiom (Eᵢ + Tᵢ − 1)/Tᵢ: for large extents its
     intermediate sum can exceed 2⁶³ − 1, the declared valid domain (§4.2)
     and the range of signed 64-bit integers, even though it fits an
     unsigned 64-bit integer". The aside an appositive; "for large
     extents" moved to the front of the clause it qualifies; the four
     facts and the pointer kept.
  2. The Example: "G_y = ⌈1000/256⌉ = 4 still — the last row of tiles is
     padded (§11.3)." → "… = 4 still, and the last row of tiles is padded
     (§11.3)."; every figure kept.
- **Removed restatements:** none. Word-level diff: "whose" lost, "its"
  and "and" gained, nothing else.
- **Reworded IDs:** none.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before;
  the Example's numbers unchanged. Keyword counts unchanged. B is
  4,783 lines and 48,677 words.
- **Questions raised:** none.

### 2026-10-14 — §11.1: the Rationale in plain language, A's six lowercase keywords rewritten around

- **Commit:** `Readable: §11.1 — the growth Rationale in plain language; the
  §20.3 summary kept, the two stated-once sentences kept` (the commit
  carrying this entry). Previous: `f96eb0b` (§10's lead-in).
- **Sections:** §11.1, the Rationale after `[R-GEO-02]`. Non-normative; the
  item held for the read-through since the §11 pass of 2026-10-09.
- **The maintainer's ask:** "The rationale may need more plain language in
  11.1, but the rest of 11.1 is fine." Proposed with before and after and
  the inventory; approved ("Go").
- **Edits.** The Rationale rewritten in plain sentences, every fact kept
  in order: the schema-first purpose; §20.3 step 4 named as the rule
  ("is §20.3 step 4's to say" for "states normatively, and governs") and
  its summary kept item by item (extents grow and never shrink; a planar
  channel list extended or shortened at its end, not both in one commit;
  names; a slab or alignment declaration declared, changed or cleared;
  several in one commit, each subject to every rule the resulting
  declarations are under; every other declaration fixed while the layer
  stores a tile, a change being a new layer or a rewrite; a layer that
  stored no tile re-declared freely, not one the commit itself empties);
  the two sentences stated nowhere else kept ("Growth is cheap where it
  changes no grid count": the no-change growth and the one-rises-one-
  stays-0 growth touch the directory alone; any other growth changes
  entry_count and extent_length (`[R-CNT-17]`), renumbers ordinals where
  `[R-GEO-06]` moves them, and re-emits the whole tile-index region
  (§20.3, `[R-WRT-04]`), the last-zero-grid-count growth included). A's
  six lowercase "may"s rewritten around ("is allowed to", "is extended",
  "can be re-declared"); the two dash asides made a colon clause and a
  "since" clause; "**only remaining**" reads "the last", unbolded.
- **Removed restatements:** none; the §20.3 summary stays as a Rationale's
  summary with the rule named.
- **Reworded IDs:** none; a Rationale.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before;
  Rationales 13 against 13. Keyword counts unchanged. B is 4,784
  lines and 48,680 words.
- **Questions raised:** none. The maintainer asked why a channel count of
  0 is barred; answered from ADR-0028 (a zero-channel layer has no sample
  content; every channel-indexed formula degenerates; extent 0 and the
  channel-list extension of §20.3 serve the schema-first case). No edit.

### 2026-10-14 — §10: the maintainer's edit, reviewed; §9 and §10 read through

- **Commit:** `Readable: §10 — maintainer's edit, reviewed: the identifier
  spaces' lead-in a sentence` (the commit carrying this entry). Previous:
  `66b0f01` (§9.7's claimants paragraph).
- **Sections:** §10, the opening paragraph before the identifier-space
  table. No ID; no keyword.
- **The maintainer's edit.** "The spaces, defined in the sections that own
  them and collected here:" → "The spaces are defined in the sections
  that own them but collected here:". A fragment made a sentence before
  the table; the same two facts.
- **Read through.** The maintainer's read-through has covered §9 whole
  (§9.1–§9.7, 2026-10-13 to 2026-10-14, the entries above) and §10 ("otherwise
  I think it looks good"); both added under "Ready for calibration 2".
- **Removed restatements:** none.
- **Reworded IDs:** none.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before.
  Keyword counts unchanged. B is 4,784 lines and 48,670 words.
- **Questions raised:** none.

### 2026-10-14 — §9.7: the claimants paragraph says what a claimant is and what a record adds

- **Commit:** `Readable: §9.7 — the claimants paragraph: a claimant glossed
  from R-CNT-02 and §5.2; a record claims nothing in its own right` (the
  commit carrying this entry). Previous: `2d3e790` (ADR-0134's erratum
  ported). §9.6 declared done by the maintainer.
- **Sections:** §9.7, the first paragraph (ID-less since the first pass;
  `[R-LIF-08]` governs the fourth).
- **The maintainer's questions.** The two sentences on what is not a
  claimant were hard to get the gist of; then whether "claims nothing
  new" meant suppressing errors during directory traversal (it does not:
  the sentences say which byte ranges enter the claimed set the next
  paragraph checks for disjointness, bounds, checksums and the slack
  total); then that "claim" had slipped his mind, and a callback to its
  definition was wanted. The document introduces the verb once, in
  §5.2 ("Every byte the live state does not claim is **slack**"), right
  after `[R-CNT-02]`'s partition, and uses "claimant" from there on
  without a sentence of its own; §9.7's "the claimants `[R-CNT-02]`
  names" pointed at a paragraph that says "structures".
- **Edits**, in the maintainer's direction and partly his words.
  1. "reaches the claimants `[R-CNT-02]` names: the directory itself, …"
     → "reaches the claimants: the structures `[R-CNT-02]` partitions the
     live committed state into, each claiming the bytes that belong to
     it, the rest being slack (§5.2). They are the directory itself, …".
     The gloss is derived from A's own text, `[R-CNT-02]`'s "Every byte
     of the live committed state belongs to exactly one of these … a
     structure" and §5.2's slack sentence; B saying what A implies, for
     the round to grade. "Claimants" left unbolded, §5.2 using the word
     first.
  2. "A record is not a claimant of its own: its header and inline
     payload lie inside the directory region, which is the claimant
     covering them, so reaching a record through the directory is
     traversal, not a second claim on those bytes." → "A record does not
     claim bytes in its own right. Its header and inline payload lie
     inside the directory region, and the directory region is the
     claimant that covers them, so a record reached through the directory
     adds no claimed range of its own." The first sentence the
     maintainer's; "claimed range" is the next paragraph's own term.
  3. "A layer record's extent slot addresses that layer's tile-index
     region (§7.4), so the region enters the walk once, as that record's
     extent, and is not a second claimant beside it." → "A layer's
     tile-index region is the extent that its layer record's extent slot
     addresses (§7.4), so it is claimed once, as that record's extent, and
     not again as a region." The counted thing made the subject.
  The `[R-IDX-03]` sentence, the list of claimants and every pointer
  unchanged; "its crc" kept lowercase, the entry's field name as §15.1
  names it, on the maintainer's question. Re-wrapped.
- **Removed restatements:** none. Word-level diff: "names", "which",
  "covering", "reaching", "traversal", "second", "those", "enters",
  "beside" and connectives lost; the gloss's words, "right", "covers",
  "adds", "claimed", "range", "again" gained; every pointer and figure
  kept.
- **Reworded IDs:** none; no ID paragraph.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before.
  Keyword counts unchanged. B is 4,784 lines and 48,669 words.
- **Questions raised:** none.

### 2026-10-14 — §9.6: ADR-0134's erratum ported, `[R-LIF-09]`'s referent repeated

- **Commit:** `Readable: §9.6 — ADR-0134's erratum ported: "the candidate's
  committed file length" for "that committed file length"` (the commit
  carrying this entry). Previous: the merge of `main` (`7cf0e0c`, the
  erratum) with B's spec kept; the spec's previous commit `a4ac2d2`.
- **Sections:** §9.6, the `[R-LIF-09]` paragraph.
- **Edit.** The maintainer, reading the port, took "equal to that
  committed file length" for a length other than the candidate's. On
  `main`, by erratum to ADR-0134: "it MUST leave the physical file length
  equal to the candidate's committed file length". Ported here in the
  same words and the same wrapping; the paragraph stays byte-identical to
  A's and unlisted. The A export refreshed from `main` before the gates.
- **Removed restatements:** none.
- **Reworded IDs:** none.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before.
  Keyword counts unchanged. B is 4,783 lines and 48,644 words.
- **Questions raised:** none.

### 2026-10-14 — §2.3, §9.6, §20.1, Appendix H: ADR-0134 ported, `[R-LIF-09]` added to both editions

- **Commit:** `Readable: §2.3, §9.6, §20.1, Appendix H — ADR-0134 ported:
  truncation to the last committed state is an updater's operation;
  R-LIF-09 added` (the commit carrying this entry). Previous: the merge
  of `main` (ADR-0134 `80d2dc6`, ADR-0133's erratum `02e19bb`) with B's
  spec kept; the spec's previous commit `64b6e5e`.
- **Sections:** §2.3 (`[R-CNF-06]`); §9.6 (new `[R-LIF-09]`, after
  `[R-LIF-06]`'s paragraph); §20.1 (`[R-WRT-01]`); Appendix H's updater
  entry.
- **The decision.** ADR-0134 (Q-A10, option (b), the maintainer's
  direction of 2026-10-14): a tool that truncates a file to its last
  committed state is an updater and the truncation its operation; the
  first decision against A since B opened, taken on `main` under the old
  gates and ported here under ADR-0133 decision 1 and its erratum of
  2026-10-14.
- **Edits**, each in the words the ADR put into A.
  1. §9.6: the `[R-LIF-09]` paragraph, byte-identical to A's (the MUST
     NOT and the MUST; `[R-LIF-01]` reaching the tool; the probe off the
     default path; the latent violation travelling with the state).
  2. §20.1, `[R-WRT-01]`: "A tool that truncates a file to its last
     committed state is an updater too: the operation is `[R-LIF-09]`'s,
     it produces no bytes, and it carries forward every byte of the state
     it leaves." after the rewriter's-output sentence; re-wrapped.
  3. §2.3, `[R-CNF-06]`: "A tool that truncates a file to its last
     committed state is an updater as well, bound as §9.6 provides
     (`[R-LIF-09]`)." after "are §20.1's."; re-wrapped.
  4. Appendix H, the updater entry: the one sentence before the Advisory
     sentence; re-wrapped.
- **The reference.** The export `scratch/cleanroom/editions/a/tarn.md` is
  refreshed from `main` (`80d2dc6`'s spec), as the erratum directs; the
  inventory below compares against it. The merge kept B's spec.
- **Removed restatements:** none.
- **Reworded IDs:** none new; `R-WRT-01` and `R-CNF-06` lines extended;
  `R-LIF-09` identical in both editions and not listed.
- **Soft items:** `ID_REWORDED_LISTED` ×124; the carried items as before;
  the ID inventory now 163 in each edition. Keyword counts: MUST NOT and
  MUST one higher in both editions. B is 4,782 lines and
  48,643 words.
- **Questions raised:** none; Q-A10 resolved on `main`.

### 2026-10-13 — §7.2, §7.4: "residue" stated as rows F29 and L14 state it

- **Commit:** `Readable: §7.2, §7.4 — residue stated as the register states
  it; R-CNT-12 listed` (the commit carrying this entry). Previous: `8b1eefe`
  (§9.4–§9.5).
- **Sections:** §7.2 (`[R-CNT-12]`); §7.4 (`[R-CNT-18]`, the layer-record
  Example). At the maintainer's ask, on finding "residue" defined nowhere
  (the entry above).
- **Edits.** Each use of "residue" in §7 replaced by the words the
  register's condition cells use for the same condition.
  1. §7.2, `[R-CNT-12]`: "The sequence MUST parse as zero or more
     complete records with no residue." → "… with no bytes remaining
     after the last complete record." (row F29: "or bytes remain after
     the last complete record"). The paragraph's other sentences and its
     six keyword clauses verbatim; re-wrapped.
  2. §7.4, `[R-CNT-18]`: "… MUST parse as zero or more complete
     sub-records under §7.2's framing with no residue. Any overrun,
     truncation, or residue is a validity error at layer scope." → "…
     with no bytes remaining after the last complete sub-record. Any
     overrun, truncation, or bytes remaining after the last complete
     sub-record is a validity error at layer scope." (row L14). The
     qualifier is spelled out both times because "the remaining bytes"
     earlier in the sentence means the payload after the fixed fields.
     Every other clause verbatim; re-wrapped.
  3. The Example: "81 exactly, with no residue, so the sub-record
     sequence is empty" → "with no bytes remaining, so …"; the figures
     kept.
  The register rows keep "trailing residue" in their instances cells,
  rows being fixed while B is open; §22's "Four residues are stated
  rather than defended" is the other sense, residual risks, and stands.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-12`, listed; `R-CNT-18`'s line extended.
- **Soft items:** `ID_REWORDED_LISTED` ×124 (the one new); the carried
  items as before. Keyword counts unchanged. B is 4,762 lines and
  48,404 words.
- **Questions raised:** none.

### 2026-10-13 — §9.4, §9.5: the maintainer's edits, reviewed; §9.5's Note says which bytes

- **Commit:** `Readable: §9.4–§9.5 — maintainer's edits, reviewed; §9.5's
  Note says which bytes it means` (the commit carrying this entry).
  Previous: `44f113d` (§9.2–§9.3's Notes).
- **Sections:** §9.4 (`[R-LIF-04]`); §9.5 (`[R-LIF-05]`, the first Note).
  §9.3 declared done by the maintainer the same day; §9 joins the
  stretch list when its last subsection is done.
- **The maintainer's edits.**
  1. §9.4, `[R-LIF-04]`: "after any commit completes" → "after any commit
     is completed". Same statement; the three MUST clauses verbatim.
  2. §9.5, `[R-LIF-05]`: "One writer at a time, any number of concurrent
     readers: this specification defines no multi-writer coordination,
     …" → "TARN supports any number of concurrent readers, but only one
     writer at a time. This specification defines no multi-writer
     coordination, …". The model in a sentence of its own; both MUSTs
     verbatim. A first version cut the model sentence; the driver
     flagged that §20's opening cites `[R-LIF-05]` for "by one writer at
     a time", and the sentence came back in the maintainer's words.
- **The driver's edit, on the maintainer's question whether "residue" is
  defined.** It is defined nowhere and used in three senses (the bytes
  after the last complete record, §7.2, §7.4, rows F29 and L14; the
  bytes past the committed file length, this Note; residual risks,
  §22). The Note's three uses replaced, the first in the maintainer's
  words: "Residue past a completed commit carries no register row of its
  own" → "The case in which extra bytes are present in the file beyond
  the committed file length carries no register row of its own";
  "cannot tell residue from corruption" → "cannot tell such bytes from
  corruption"; "What the residue violates" → "What those bytes violate".
  Every citation and the dash pair kept; re-wrapped.
- **Removed restatements:** none.
- **Reworded IDs:** `R-LIF-05`, listed; `R-LIF-04`'s line extended.
- **Soft items:** `ID_REWORDED_LISTED` ×123 (the one new); the carried
  items as before. Keyword counts unchanged. B is 4,760 lines and
  48,385 words.
- **Questions raised:** none.

### 2026-10-13 — §9.2, §9.3: two of the maintainer's Note edits, reviewed; §9.3's first Note cites the rules

- **Commit:** `Readable: §9.2–§9.3 — maintainer's edits, reviewed; §9.3's
  first Note cites the rules its derivation rests on` (the commit
  carrying this entry). Previous: `48e65f4` (the crash Example's lead-in).
- **Sections:** §9.2 (the barriers Note); §9.3 (the first and the last
  Note). All non-normative.
- **The maintainer's edits.**
  1. §9.2, the barriers Note: "the outcome is rejection at the affected
     scope, never silent corruption" → "… not silent corruption". Same
     statement.
  2. §9.3, the last Note: "tells a cache which one it holds" → "which
     generation it holds". Same statement; re-wrapped by the driver.
- **The driver's edit, on the maintainer's question whether §9.3's first
  Note should cite normative text.** It said "The strict increase is what
  makes that revalidation sound, and §9.2's second Note is what makes it
  checkable". A Note is non-normative under `[R-CNF-01]`, and §9.2's
  second Note only writes out a derivation whose premises are rules. It
  now reads "The strict increase (`[R-LIF-02]`) is what makes that
  revalidation sound, and it is forced by the steps a conforming writer
  performs rather than promised beside them: `[R-LIF-01]`, `[R-LIF-02]`'s
  steps 1, 3 and 5 and `[R-CNT-06]` yield it, as §9.2's second Note
  derives." The colon sentence that followed ("no two commits of one file
  share a committed file length, so …") is now a sentence of its own,
  unchanged in words; the rest of the Note from "Where one has" is
  untouched, its dash pair included. "Checkable" reads "forced by the
  steps … rather than promised beside them", which is what the second
  Note now says of itself (the entry below).
- **Removed restatements:** none. The word-level diff of §9.2–§9.3
  against `48e65f4`: "never", "one", "checkable" lost; "not",
  "generation", the citations' words ("1", "3", "5", "LIF", "CNT",
  "forced", "performs", "promised", "yield", "derives") and connectives
  gained; every figure kept.
- **Reworded IDs:** none; Notes.
- **Soft items:** `ID_REWORDED_LISTED` ×122; the carried items as before.
  Keyword counts unchanged. B is 4,759 lines and 48,367 words.
- **Questions raised:** none.

### 2026-10-13 — §9.2: the crash Example's lead-in, the maintainer's edit, reviewed

- **Commit:** `Readable: §9.2 — maintainer's edit, reviewed: the crash
  Example's lead-in in sentences` (the commit carrying this entry).
  Previous: `005045f` (the merge of main's Q-A10); the spec's previous
  commit `1df7b0d`.
- **Sections:** §9.2, the Example "what a crash sees", its lead-in
  paragraph. Non-normative.
- **The maintainer's edit.** "▓ marks bytes outside the live committed
  state: in row 2 the partial write of an interrupted commit, in row 3
  the structures commit n + 1 superseded." → "In the following, ▓ marks
  bytes outside the live committed state. In row 2, it is the partial
  write of an interrupted commit. In row 3, it is the structures commit
  n + 1 superseded." The colon list made three sentences; the same three
  facts; the figure and the paragraph after it untouched. Re-wrapped by
  the driver to 70 columns inside the blockquote. The run-in label's
  dash kept, as every label's is.
- **Removed restatements:** none.
- **Reworded IDs:** none; an Example.
- **Soft items:** `ID_REWORDED_LISTED` ×122; the carried items as before.
  Keyword counts unchanged. B is 4,757 lines and 48,341 words.
- **Questions raised:** none.

### 2026-10-13 — §9.2: the strict-increase Note's premise is step 3's requirement, not the Note's

- **Commit:** `Readable: §9.2 — the strict-increase Note's premise stated as
  step 3's requirement, not the first Note's` (the commit carrying this
  entry). Previous: `58d3201` (§9.1–§9.2, the maintainer's edits).
- **Sections:** §9.2, the second Note (ADR-0111's derivation of the
  128-byte floor from the steps).
- **The maintainer's questions, 2026-10-13.** Three on §9.2: whether the
  first Note describes a writer that violates step 3 and still produces
  a conforming file; whether a Note can forbid, as the second Note's "the
  Note above forbids" has it; and whether recovery is a class of tool.
  Answers given with the text: yes, a trailer re-pointed at an earlier
  generation's directory leaves a file every register row accepts (the
  old directory inside the immutable prefix, the appended payloads
  slack under `[R-CNT-21]`, no row comparing dir_offset with the prior F,
  which `[R-LIF-05]` keeps a reader from seeing), unwitnessed by §21.7's
  own test since one conforming commit can write the same bytes, so a
  conforming file from a nonconforming writer; no, a Note is
  non-normative under `[R-CNF-01]` and the forbidding is step 3's "append
  the new complete directory"; and recovery is a role, not a class (the
  ledger question Q-A10, opened on main the same day). The maintainer
  added that the second Note's "so there is such a directory" is not a
  fact about every file, only about a writer that performs the steps,
  and that a reader relies on the strict increase alone, never on its
  size (§9.3's first Note), which the text confirms: no reader check and
  no register row cites the floor.
- **Edits.** The second Note, every figure and citation kept: "is forced
  by the steps before it, not an extra obligation on the writer" reads
  "is forced on a writer that performs the steps before it; it is not an
  extra obligation", so the derivation is framed as what the steps force
  on a writer performing them; "so this commit's directory lies at
  dir_offset ≥ the prior F; the Note above forbids reusing an earlier
  generation's, so there is such a directory" reads "so the directory
  step 3 appends, this commit's own as the Note above reads it, lies at
  dir_offset ≥ the prior F", which puts the force where it is, in step
  3, and asserts nothing about files a nonconforming writer leaves. The
  reader's side is not added, at the maintainer's word. Re-wrapped.
- **Removed restatements:** none. The word-level diff of the Note: "by",
  "an", "so", "directory", "forbids", "reusing", "earlier",
  "generation's", "there", "such" lost; "that", "performs", "it", "step",
  "3", "appends", "own", "as", "reads" gained; every number and ID kept.
- **Reworded IDs:** none; a Note.
- **Soft items:** `ID_REWORDED_LISTED` ×122; the carried items as before.
  Keyword counts unchanged. B is 4,756 lines and 48,340 words.
- **Questions raised:** Q-A10 (recovery as a class) opened on main at the
  maintainer's word. For the ledger when the maintainer asks: a trailer
  re-pointed at an earlier generation's directory violates step 3 and
  leaves a conforming file, unwitnessed by §21.7's test, which the text
  says of steps 4 and 6 only.

### 2026-10-13 — §9.1, §9.2: the maintainer's edits, reviewed; the creation paragraph in order

- **Commit:** `Readable: §9.1–§9.2 — maintainer's edits, reviewed` (the
  commit carrying this entry). Previous: `0bca6d5` (the log: round 2's
  rulings); the spec's previous commit `7b5b9a7`. The maintainer's
  read-through from §9 begins with this batch.
- **Sections:** §9.1 (`[R-LIF-01]`); §9.2 (the six steps, the creation
  paragraph).
- **The maintainer's edits.**
  1. §9.1, `[R-LIF-01]`: "Bytes in [0, F) — F being the live trailer's
     committed file length — are immutable: a writer MUST NOT modify
     them, and every conforming mutation … (a rewrite, §20.5)" → "All
     bytes in [0, F), with F being the live trailer's committed file
     length, are immutable: a writer MUST NOT modify them. Every
     conforming mutation … (§20.5)". The interval and the MUST NOT
     verbatim; the dash aside a comma clause; one sentence made two; "a
     rewrite," dropped as a duplicate of "whole-file rewrite". Same
     statement. A first version read "All bytes up to the live trailer's
     committed file length"; the interval came back on the driver's note
     that "up to" is looser than [0, F), and "in" on his note that A
     says "Bytes in".
  2. §9.2, the six steps: each set at a line start. No word changed. At
     `7b5b9a7` steps 2 to 6 stood mid-line after the first pass of
     2026-10-08, so Markdown rendered the six as one list item; the edit
     makes them six. Re-wrapped by the driver to 72 columns with
     three-space continuations.
  3. §9.2, the creation paragraph: the dash aside on the front block's
     durability a comma clause ("whose durability is covered by steps 4
     and 6").
- **The driver's edit, on the maintainer's observation that the paragraph
  names steps 4 and 6 before steps 2–6.** "On creation there is no prior
  trailer: the writer first emits the front signature block (§6.1), whose
  durability is covered by steps 4 and 6, then performs steps 2–6, writing
  beginning at offset 16. There being no prior committed file length, the
  strict increase above binds from the second commit onward." → "On
  creation there is no prior trailer. The writer first emits the front
  signature block (§6.1), then performs steps 2–6 beginning at offset 16;
  the barriers of steps 4 and 6 cover the block's durability. Because
  there is no prior committed file length, the strict increase above binds
  from the second commit onward." The sequence first and the durability
  remark after it, in A's words ("the barriers of steps 4 and 6 cover");
  "Because there is" for "There being" at the maintainer's word. Every
  fact kept: no prior trailer; the block first; steps 2–6 from offset 16;
  durability by the barriers of 4 and 6; the strict increase from the
  second commit. No ID, no keyword.
- **Removed restatements:** none. The word-level diff of §9.1–§9.2 against
  `7b5b9a7` shows the splits' connectives and capitals, "a rewrite" and
  "writing" lost, "with", "block's" and "Because" gained, nothing else.
- **Reworded IDs:** `R-LIF-01`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×122 (the one new); the carried
  items as before. Keyword counts unchanged. B is 4,756 lines and 48,333
  words.
- **Questions raised:** none.

### 2026-10-12 — §9.7: the word-diff preflight's one repair, "above" restored

- **Commit:** `Readable: §9.7 — word-diff preflight: "above" restored to the
  bound sentence` (the commit carrying this entry). Previous: `7a2046e`
  (Appendix H's pass).
- **Sections:** §9.7, the verifier's second paragraph (ID-less;
  `[R-LIF-08]` governs the fourth). Found by the word-diff preflight that
  round 2 was owed: for every commit from `95b5a30` to `7a2046e`, the
  diff's removed and added lines tokenised as `propose.py` does and the
  Counter difference read word by word
  (`scratch/cleanroom/pass/word-diff-preflight.py`; the per-commit result
  goes into `docs/fidelity/3-round-2/word-diff.md` with the round's
  artifacts).
- **Edits.** A's "the [16, F − 64) bound above already keeps every other
  claimant disjoint from them" had lost "above" in the §9 first pass
  (`95b5a30`): the word was absent from the proposal's after-text and
  named nowhere in its inventory or in the entry below, so it is a
  transcription loss and not an approved cut. Restored; the line is 70
  characters and no re-wrap was needed. The bound it points at stands two
  sentences earlier in the same paragraph ("that each lies within [16,
  F − 64)"), as in A.
- **The preflight's other findings, none a defect.** Over the twenty-one
  commits every other word lost or gained is a connective, an inflection,
  a capital at a sentence split, a recorded swap ("has to" for the
  lowercase *must*, "can" for *may*, "advised" for *recommended*,
  "override" for "govern notwithstanding", "decides" for "is
  load-bearing", "tells apart" for "individuates", "nevertheless" for "—
  but"), the `[R-ERR-04]` pointer's words, or the dropped duplicate
  "(§8.1)". Three wordings the entries did not name are in the approved
  proposals' after-texts: "Field values:" → "The field's values:" (§11.4's
  and §12.2's lead-ins), "all reserved values" → "every reserved value"
  (§11.4, quoted in the §11 entry), and "the table's forms with k" → "the
  table's form with k" (§14.2's offsets Example). The range pooled commit
  by commit and the range as one diff agree word for word.
- **Removed restatements:** none.
- **Reworded IDs:** none new; the sentence stands in an ID-less paragraph,
  and `R-LIF-08` is listed already.
- **Soft items:** `ID_REWORDED_LISTED` ×121; the carried items as before
  (the eight §3.1 term rewordings, Appendix B's row, HEADINGS 130 against
  129, SHOULD 46 against 47). Keyword counts unchanged. B is 4,755 lines
  and 48,337 words.
- **Questions raised:** none; reported for the maintainer's eye before
  round 2's launch.

### 2026-10-12 — Appendix H: spruce-up pass, sixteen dash asides out; the series closed

- **Commit:** `Readable: Appendix H — spruce-up pass: the five checklists
  without asides` (the commit carrying this entry). Previous: `586b36f`
  (Appendix G's pass).
- **Sections:** Appendix H's five checklists. Non-normative; no ID
  paragraph. The last pass of the spruce-up series the maintainer asked
  for on 2026-10-09 ("a spruce-up pass that will hopefully make my requests
  later on fewer", not his read-through); proposed with before and after
  (`scratch/cleanroom/proposals/sH-pass.md`), approved ("Go").
- **Edits.** The five label dashes colons, as §20.1's tier list's; the
  file checklist's example aside a comma clause; the updater's permitted
  changes a parenthesis with "not both in one commit" a comma clause
  inside it; the verifier's seven asides comma clauses and a "while"
  clause ("a user-metadata record at an experimental-range encoding being
  no violation and no bar, and instead reported with its owning scope,
  encoding value and stored extent length, while encoding 0 and the
  reserved range stay violations (R1)"); re-wrapped.
- **Removed restatements:** none. Nothing dropped: the word-level diff is
  empty for four checklists and shows connectives only for the verifier's.
- **Reworded IDs:** none; no ID paragraph changed.
- **Soft items:** `ID_REWORDED_LISTED` ×121; the carried items as before.
  Keyword counts unchanged. B is 4,755 lines and 48,336 words.
- **The series, closed.** Twenty commits from `95b5a30` (§9's first pass,
  2026-10-08) to this one, over §9 through §24 and Appendices A, D, G and
  H: em-dashes in B 589 → 189, of which outside tables and headings 491 →
  91; those 91 are §1–§8's (46, the maintainer's read-through stretch),
  §9's Notes (14), Appendix F's reference labels (13), the §21.1 cell
  character, and label dashes. Lines 4,847 → 4,755; words 48,606 →
  48,336; Notes, Examples and Rationales unchanged at 56, 20 and 13;
  `reworded-ids.txt` 39 → 121 IDs. Every pass: every keyword clause
  verbatim, nothing cut but duplicate pointers, every rule paragraph
  listed, a word-level diff per item from §20.3 on. Two defects of the
  rewrite found and repaired on the way: `[R-ERR-04]`'s stale pointer at
  §21.6 (2026-10-12) and the duplicate `R-PRV-03` line (merged). Four
  words the maintainer dislikes replaced in explanatory prose
  ("notwithstanding" in §15.3, "load-bearing" and "individuates" in §21,
  "recommended" and other lowercase keywords of A's in re-wrapped Notes).
  Held for the read-through: §11.1's Rationale (restates §20.3 step 4; two
  sentences stated nowhere else), §9's Notes, and the table cells of
  §15.3, §20.4 and §21 that carry asides (table values stay).
- **Questions raised:** none.

### 2026-10-12 — Appendix G: spruce-up pass, twenty-one dash asides out

- **Commit:** `Readable: Appendix G — spruce-up pass: the reproducible-writer
  profile's intro, ten items and closing paragraph without asides` (the
  commit carrying this entry). Previous: `92f5789` (§24's pass).
- **Sections:** Appendix G whole but its heading. Non-normative; no ID
  paragraph. A spruce-up pass, not the maintainer's read-through;
  proposed with before and after (`scratch/cleanroom/proposals/sG-pass.md`),
  approved ("Go").
- **Edits.**
  1. The intro: the byte-identical applications a parenthesis.
  2. Items 1 to 9: sixteen asides made commas, colons, parentheses, "which
     is" and "since" clauses. Item 2's hash definition a sentence of its
     own ("The hash is a named function at a named version … and the
     identifier is the digest's last eight bytes in output order, the
     eight a named hash emits last"); "already-compact" rejoined across
     its line break. Item 3's alignment gap a parenthesis and "which is
     `[R-CNT-03]`'s advice taken as a requirement here". Item 5's
     placement and filter cases after colons. Item 7: "which is
     `[R-TYP-10]`'s SHOULD taken as a requirement here". Item 9: "since
     number formatting varies by runtime". The list tight; re-wrapped.
  3. Item 10: the dash a comma; set apart as in A. The closing paragraph:
     the mandatory examples a comma clause, the item-8 aside a
     parenthesis.
- **Removed restatements:** none. Nothing dropped: the word-level diff
  over the 1,360-word list shows only connectives gained ("is" ×4,
  "which" ×2, "and", "since", a capital) and one "the" lost to the split.
- **Reworded IDs:** none; no ID paragraph changed.
- **Soft items:** `ID_REWORDED_LISTED` ×121; the carried items as before.
  Keyword counts unchanged. B is 4,758 lines and 48,346 words.
- **Questions raised:** none.

### 2026-10-12 — §24, Appendix A and Appendix D: spruce-up pass, twelve dash asides out

- **Commit:** `Readable: §24, Appendices A and D — spruce-up pass: the four
  R-VEC paragraphs, the Note and two appendix paragraphs without asides;
  R-VEC-01 through -04 listed` (the commit carrying this entry). Previous:
  `2ae99f9` (§22–§23's pass).
- **Sections:** §24 (`[R-VEC-01]` through `[R-VEC-04]`, the Note), Appendix
  A (the open applied), Appendix D (append-only). A spruce-up pass, not
  the maintainer's read-through; proposed with before and after
  (`scratch/cleanroom/proposals/s24-pass.md`), approved ("Go").
- **Edits.**
  1. `[R-VEC-01]`: the evidence-not-definition aside a colon.
  2. `[R-VEC-02]`: the row-label permanence a sentence of its own; the
     §6.2 field-gates aside a parenthesis; the ID joined to the last
     line; "The two axes are independent", a surviving statement of
     §2.4's cut bridge (round 1, item 4, kept cut), unchanged.
  3. `[R-VEC-04]`: the sibling's definition and the verifier-case fields
     comma clauses. `[R-VEC-03]`: the tile-count aside after a semicolon;
     the ID joined to the last line.
  4. The Note: the dash a comma; its first line, which carries A's
     lowercase "may", untouched. Appendix A's open paragraph and
     Appendix D's append-only paragraph: a comma each.
- **Removed restatements:** none. Nothing dropped: the word-level diff
  shows one sentence-initial capital and nothing else.
- **Reworded IDs:** `R-VEC-01`, `R-VEC-02`, `R-VEC-03`, `R-VEC-04`, listed.
- **Correction to the entry for `2ae99f9`.** The 118th line of
  `reworded-ids.txt` was not a retired `R-COD-11` line but a second
  `R-PRV-03` line, added by that pass beside the one from the §7
  re-pointing (the tool keys by ID, hence 117 listed). The two are merged
  here into one line carrying both reasons; the file has 121 lines and
  121 distinct IDs, all listed.
- **Soft items:** `ID_REWORDED_LISTED` ×121 (the four new); the carried
  items as before. Keyword counts unchanged. B is 4,764 lines and 48,360
  words.
- **Questions raised:** none.

### 2026-10-12 — §22 and §23: spruce-up pass, twenty-three asides out

- **Commit:** `Readable: §22–§23 — spruce-up pass: every R-SEC and R-PRV
  paragraph and the index Note without asides; R-SEC-01 through -07 and
  R-PRV-01 through -05 listed` (the commit carrying this entry). Previous:
  `cfb70aa` (§21's second pass).
- **Sections:** §22.1 through §22.5 (`[R-SEC-01]` through `[R-SEC-07]`, the
  §22.2 Note), §23.1 through §23.3 (`[R-PRV-01]` through `[R-PRV-05]`). A
  spruce-up pass, not the maintainer's read-through; proposed with before
  and after (`scratch/cleanroom/proposals/s22-pass.md`), approved ("Go").
- **Edits.**
  1. `[R-SEC-01]`: "including files that validate" a parenthesis.
     `[R-SEC-02]`: the decompression-bomb aside after a semicolon; the
     MUST NOT verbatim. The Note: a semicolon.
  2. `[R-SEC-03]`: the aliasing examples a parenthesis after "as a class";
     "slack being unconstrained and able to hold anything" for the aside;
     the partial-total caveat after a semicolon; the SHOULD verbatim.
     `[R-SEC-04]`: four asides "which is why" and "since" clauses; the four
     residues in A's order.
  3. `[R-SEC-05]` and `[R-SEC-06]` (one paragraph): the filesystem-path
     aside a colon clause; all three MUST NOTs verbatim; their existing
     lines in `reworded-ids.txt` (from the §7 re-pointing) updated in
     place rather than duplicated. `[R-SEC-07]`: the attests-that-generation
     aside a comma.
  4. `[R-PRV-01]`: two dashes a semicolon and a colon; the MUST NOT and
     every operation in A's order, "not offered as closed" kept.
     `[R-PRV-02]`: a colon; the MUST verbatim. `[R-PRV-03]`: a parenthesis
     and a comma clause; both SHOULDs verbatim. `[R-PRV-04]`: two spaced
     hyphens used as dashes made commas. `[R-PRV-05]`: the observers a
     parenthesis; the MAY and the SHOULD verbatim.
- **Removed restatements:** none. Nothing dropped: the word-level diff
  shows "since" gained in `[R-SEC-04]` and "being … able to" for "is … can"
  in `[R-SEC-03]`, nothing else.
- **Reworded IDs:** `R-SEC-01`, `-02`, `-03`, `-04`, `-07`, `R-PRV-01`
  through `-05` listed anew; `R-SEC-05` and `R-SEC-06` updated.
- **Soft items:** `ID_REWORDED_LISTED` ×117 (the ten new; 118 lines in the
  file, `R-COD-11`'s line having been retired from the list on
  2026-09-27 and kept as a comment); the carried items as before. Keyword
  counts unchanged. B is 4,769 lines and 48,372 words.
- **Questions raised:** none.

### 2026-10-12 — §21.5 to §21.9: spruce-up pass, twenty dash asides out; a stale pointer repaired

- **Commit:** `Readable: §21.5–§21.9 — spruce-up pass: the ignored-records
  lead-in, the non-violations, what no check detects, coverage and limits
  without asides; R-ERR-04's pointer at §21.6 repaired; R-ERR-01 through
  -05 listed` (the commit carrying this entry). Previous: `8f70e4f` (§21's
  first pass).
- **Sections:** §21.5 (the lead-in), §21.6 (both prose paragraphs), §21.7
  (five paragraphs, `[R-ERR-01]`), §21.8 (`[R-ERR-02]`), §21.9
  (`[R-ERR-03]`, `[R-ERR-04]`, the Note, `[R-ERR-05]`). The tables untouched.
  The second of two passes over §21, not the maintainer's read-through;
  proposed with before and after (`scratch/cleanroom/proposals/s21b-pass.md`),
  approved ("Go").
- **A defect of the rewrite, found and repaired.** `[R-ERR-04]` names the
  two capability refusals as the ones "§21.6's closing paragraph names".
  In A that paragraph was the two conforming-but-refused cases; the entry
  for 2026-09-24 moved `[R-CNF-11]`'s cannot-establish grounds into §21.6
  as a new closing paragraph, so B's pointer named the wrong paragraph
  (A's other such pointer, in §2.3, was cut in the same entry). It now
  reads "the two capability refusals §21.6 names as conforming files a
  reader nevertheless refuses", the paragraph's own words. The same class
  as the §8.1 pointer repaired on 2026-10-08; a search for "§21.6's
  closing paragraph" finds no other in B.
- **Edits.**
  1. The §21.5 lead-in: the outcome's gloss after a semicolon; the
     quarantine's exceptions after a comma; the SHOULD verbatim.
  2. §21.6: the reader-behavior aside a parenthesis; "The qualifier is
     load-bearing —" reads "The qualifier decides:" (a word the maintainer
     dislikes, in explanatory prose); the neighbouring-condition aside a
     colon. Every clause of the two-cases paragraph kept, round 1's first
     item resting on it.
  3. §21.7: the three kinds of wrong content moved after the main clause
     as a colon list; the rows aside a colon; "as `[R-CNF-13]`
     individuates them" reads "tells them apart" (likewise); `[R-ERR-01]`'s
     widths aside a colon clause and a comma.
  4. `[R-ERR-02]`: the counts a parenthesis. `[R-ERR-03]`: the finding-aid
     aside a colon. `[R-ERR-04]`: the two capability refusals a sentence of
     their own with the pointer above; the three keyword clauses verbatim.
     The Note: a parenthesis. `[R-ERR-05]`: the structures aside a colon
     before its list; re-wrapped.
- **Removed restatements:** none. Nothing dropped: the word-level diff
  shows exactly the three intended word changes and the pointer's words.
- **Reworded IDs:** `R-ERR-01`, `R-ERR-02`, `R-ERR-03`, `R-ERR-04`,
  `R-ERR-05`, listed; thirteen keyword clauses and figures checked.
- **Soft items:** `ID_REWORDED_LISTED` ×108 (the five new); the carried
  items as before. Keyword counts unchanged. B is 4,778 lines and 48,395
  words. §21 is done for this pass: 46 dashes in its prose to 1, the
  quoted cell character; the tables keep their 68.
- **Questions raised:** none; the pointer repair is reported for the
  maintainer's eye.

### 2026-10-09 — §21.1 to §21.4: spruce-up pass, twenty-seven dash asides out of the register's prose

- **Commit:** `Readable: §21.1–§21.4 — spruce-up pass: how to read the
  register, three lead-ins and the F11 Note without asides` (the commit
  carrying this entry). Previous: `1e2734f` (§20.5's pass).
- **Sections:** §21.1 (both paragraphs), §21.2 (the lead-in, the F11
  Note), §21.3 and §21.4 (the lead-ins). The register rows untouched. The
  first of two passes over §21, not the maintainer's read-through;
  proposed with before and after (`scratch/cleanroom/proposals/s21a-pass.md`),
  approved ("Go").
- **Edits.**
  1. §21.1's register paragraph: a row's four parts a semicolon list after
     "together with", the express-assignment exception inside the first;
     "completeness is normative" with a colon and the detectability test
     as an "under which" clause; "But each row restates its governing
     rule" a sentence of its own; the scope exception and the
     specialization qualifier a comma clause and a parenthesis;
     re-wrapped.
  2. §21.1's Instances paragraph: eleven asides parentheses and a
     semicolon; "a cell reading —", which names the dash character a cell
     can contain, reads a cell reading "—" in quotation marks, the one
     dash kept; re-wrapped.
  3. The §21.2 lead-in: the reaching rows' aside a comma clause (this
     lead-in remains the surviving statement of the reach Note's results,
     round 1's sixth item, kept cut). The F11 Note: a parenthesis. The
     §21.3 and §21.4 lead-ins: semicolons.
- **Removed restatements:** none. Nothing dropped: the word-level diff
  shows "together with", "under which" and a capitalised "But" gained in
  the first paragraph and nothing else.
- **Reworded IDs:** none; no ID paragraph changed (§21.1's prose and the
  lead-ins carry no marker; `[R-ERR-02]` in §21.1 is a citation).
- **Soft items:** `ID_REWORDED_LISTED` ×103; the carried items as before.
  Keyword counts unchanged. B is 4,783 lines and 48,410 words.
- **Questions raised:** none.

### 2026-10-09 — §20.5: spruce-up pass, twenty-four dash asides out; the opening in four paragraphs

- **Commit:** `Readable: §20.5 — spruce-up pass: the opening in four
  paragraphs, R-WRT-06, -07, -09, the Example's prose and the Note without
  asides; R-WRT-06, -07, -09 listed` (the commit carrying this entry).
  Previous: `582b87e` (§20.4's pass).
- **Sections:** §20.5 whole but the compaction figure. The last of four
  passes over §20, not the maintainer's read-through; proposed with
  before and after (`scratch/cleanroom/proposals/s20d-pass.md`), approved
  ("Go").
- **Edits.**
  1. The ID-less opening paragraph (591 words, ten asides) made four by
     topic: the three rewrites; refusal and dropping; the fresh file_id;
     the creation path. Ten asides made parentheses, semicolons, commas
     and clauses ("both and not one"); all seven keyword clauses and
     every sentence in A's order verbatim.
  2. `[R-WRT-06]`: the vehicles aside, which stood between the SHOULD's
     subject and the SHOULD, moved after the SHOULD's reason as a
     sentence of its own, "On a conforming input such a feature is a
     carried ignore-lane bit (§6.3) or an unrecognized `tarn.` key …",
     its inner colon list after a comma, the nine row numbers kept; the
     three keyword clauses verbatim.
  3. `[R-WRT-07]`'s lead paragraphs: the placement freedom a "since"
     clause, the preserved content opening "The content preserved is",
     the crc aside participial; the `[R-IDX-03]` aside in the
     regeneration paragraph a "since" clause (the passage quiz item
     quizb-14 turned on, its SHOULD verbatim); `[R-WRT-07]`: the §7.2
     aside participial.
  4. The compaction Example's prose: two dashes a comma and a semicolon;
     the figure untouched. `[R-WRT-09]`: the links of the chain after
     "before emitting that structure's bytes" as a colon list; the ID
     joined to the last line. The Note: the dash a comma.
- **Removed restatements:** none. Nothing dropped: the word-level diff
  shows only connectives gained ("and", "since", "The content preserved
  is", "such a feature is") and two inflections ("carrying", "reach").
- **Reworded IDs:** `R-WRT-06`, `R-WRT-07`, `R-WRT-09`, listed; fourteen
  keyword clauses and row lists checked.
- **Soft items:** `ID_REWORDED_LISTED` ×103 (the three new); the carried
  items as before. Keyword counts unchanged. B is 4,788 lines and 48,433
  words. §20 is done for this pass: 70 dashes to 5, those five the
  preservation table's.
- **Questions raised:** none.

### 2026-10-09 — §20.4: spruce-up pass, seven dash asides out

- **Commit:** `Readable: §20.4 — spruce-up pass: four paragraphs and the
  Rationale without asides; R-WRT-05, -08 listed` (the commit carrying
  this entry). Previous: `26d651e` (§20.3's pass).
- **Sections:** §20.4 (`[R-WRT-05]`, the persistence paragraph, the drop
  paragraph, `[R-WRT-08]`, the Rationale). The preservation table
  untouched: its cells carry five asides, but table values stay as they
  are. The third of four passes over §20, not the maintainer's
  read-through; proposed with before and after
  (`scratch/cleanroom/proposals/s20c-pass.md`), approved ("Go").
- **Edits.**
  1. `[R-WRT-05]`: "header, inline payload, and extent slot" a parenthesis
     after the MUST.
  2. The persistence paragraph: the registered types' flags after a
     colon; the MU = 1 row's reach given its reason as a "since" clause,
     "so for an implemented type only the PE bit bites" after a
     semicolon; re-wrapped. Every clause in A's order.
  3. The drop paragraph: re-wrapped only; no word changed.
  4. `[R-WRT-08]`: the no-embedded-offsets aside a comma; the ID joined to
     the last line.
  5. The Rationale: "the directory a commit emits differing from the one
     it supersedes" for the aside.
- **Removed restatements:** none. Nothing dropped: the word-level diff
  shows "since" gained in the persistence paragraph and "differs" become
  "differing" in the Rationale, nothing else.
- **Reworded IDs:** `R-WRT-05`, `R-WRT-08`, listed; seven keyword clauses
  checked.
- **Soft items:** `ID_REWORDED_LISTED` ×100 (the two new); the carried
  items as before. Keyword counts unchanged. B is 4,791 lines and 48,446
  words.
- **Questions raised:** none.

### 2026-10-09 — §20.3: spruce-up pass, twenty-five dash asides out of the append procedure

- **Commit:** `Readable: §20.3 — spruce-up pass: the append procedure's
  steps, continuation paragraphs, Note and Examples without asides;
  R-WRT-03, -04 listed` (the commit carrying this entry). Previous:
  `890ae06` (§20's first pass).
- **Sections:** §20.3 (`[R-WRT-03]`, the six steps and step 4's three
  continuation paragraphs under `[R-WRT-04]`, the cost Note, the 644-byte
  Example, the three-shapes Example's prose). The second of four passes
  over §20, not the maintainer's read-through; proposed with before and
  after (`scratch/cleanroom/proposals/s20b-pass.md`), approved ("Go").
- **Edits.**
  1. `[R-WRT-03]`: the re-emission aside a "since" clause.
  2. Steps 1 to 3: the recovery-output aside a comma clause; "the
     appender is a reader here" after a colon; the open's two reasons
     "since" clauses; the entry-as-record parallel after a semicolon; the
     three keyword clauses verbatim.
  3. Step 4: the region's contents a comma clause; in the
     fixed-declarations paragraph the both-sides fields a parenthesis
     (all ten keyword clauses verbatim; it remains the surviving
     statement of the rules §11.1's Rationale restates); in the
     line-is-drawn paragraph the §14 reading a parenthesis; in the bounds
     paragraph nothing but wrapping; step 6's at-least-128 aside a
     parenthesis. The three continuation paragraphs re-wrapped, and the
     ID's governing block keeps A's shape, the bounds paragraph running
     tight into steps 5 and 6.
  4. The Note: the verifier clause after a semicolon. The 644-byte
     Example: the entry aside a colon. The three-shapes Example: shape
     (a)'s and (b)'s asides commas; shape (c)'s label dash a colon, its
     fill-type-extent aside a parenthesis and its empties clause after a
     semicolon; the figures untouched.
- **Removed restatements:** none. Nothing dropped: a word-level diff per
  item shows no word lost or gained in nine of the eleven, "since" gained
  in `[R-WRT-03]`, and "which" for "that" with two "since" in steps 1 to 3.
- **Reworded IDs:** `R-WRT-03`, `R-WRT-04`, listed; eighteen keyword
  clauses and figures checked.
- **Soft items:** `ID_REWORDED_LISTED` ×98 (the two new); the carried items
  as before; the Example numbers unchanged. Keyword counts unchanged. B
  is 4,793 lines and 48,454 words.
- **Questions raised:** none.

### 2026-10-09 — §20, first pass (opening, §20.1, §20.2): six dash asides out

- **Commit:** `Readable: §20.1–§20.2 — spruce-up pass: the opening, the tier
  list, R-WRT-01 and R-WRT-02 without asides; R-WRT-01, -02 listed` (the
  commit carrying this entry). Previous: `d8b1af8` (§19's pass).
- **Sections:** §20 (opening), §20.1 (the tier list, `[R-WRT-01]`), §20.2
  (`[R-WRT-02]`). The first of four spruce-up passes over §20, not the
  maintainer's read-through; proposed with before and after
  (`scratch/cleanroom/proposals/s20a-pass.md`), approved ("Go").
- **Edits.**
  1. The opening: "it consolidates: each step cites the rule".
  2. The tier list: the three label dashes colons; the list tight.
  3. `[R-WRT-01]`: the latent-violation aside after a semicolon; every
     clause in A's order.
  4. `[R-WRT-02]`: "placement being otherwise free" a participial clause;
     "both barriers, not one" a comma clause inside its parenthesis; the
     MUST verbatim.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-WRT-01`, `R-WRT-02`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×96 (the two new); the carried items
  as before. Keyword counts unchanged. B is 4,810 lines and 48,479 words.
- **Questions raised:** none.

### 2026-10-09 — §19: spruce-up pass, thirty-six dash asides out

- **Commit:** `Readable: §19 — spruce-up pass: both step lists, four
  paragraphs, the timing bullets, the Rationale and two Notes without
  asides; R-RDR-01 through -04 listed` (the commit carrying this entry).
  Previous: `bdf68a5` (§18's pass).
- **Sections:** §19.1 (the open's steps, `[R-RDR-01]`), §19.2 (the
  lead-in, the four tiers, `[R-RDR-02]`, the Rationale), §19.3
  (`[R-RDR-03]`), §19.4 (the tile-read steps, `[R-RDR-04]`, two Notes). A
  spruce-up pass, not the maintainer's read-through; proposed with before
  and after (`scratch/cleanroom/proposals/s19-pass.md`), approved ("Go").
- **Edits.**
  1. The open's four steps: eight asides made comma clauses, a colon, a
     parenthesis (step 4's user-metadata framing rules) and a "because"
     clause ("whether or not each name is itself well-formed, because
     `[R-ENC-13]` makes name comparison a byte comparison, which needs no
     valid name; so two layers …"); re-wrapped; the list tight. The list
     carries no ID (`[R-RDR-01]` closes the paragraph after it, whose
     aside is now a comma clause).
  2. §19.2: the verifier-detector exclusion a parenthesis inside the
     MUST; the extent tier's three asides comma clauses; `[R-RDR-02]`'s
     index-chain aside a colon clause; the Rationale's three dashes a
     semicolon and comma clauses.
  3. `[R-RDR-03]`: the definition of first access a "which is" clause with
     a parenthesis; "extent slot and inline payload both" a comma clause;
     the sub-record framing rules a parenthesis; re-wrapped; the twelve
     rule sets in A's order.
  4. `[R-RDR-04]`'s eight steps: ten asides made colons, commas,
     parentheses, a semicolon and a "which" clause; the sentinel's
     fill-per-layout aside placed after "bit-exactly and with no payload
     I/O"; the ID joined to the last line; the whole list the ID's text,
     as before.
  5. Two Notes: a "while" clause and an "and" clause; the labels' dashes
     kept.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-RDR-01`, `R-RDR-02`, `R-RDR-03`, `R-RDR-04`, listed;
  eleven keyword clauses and figures checked.
- **Soft items:** `ID_REWORDED_LISTED` ×94 (the four new); the carried items
  as before. Keyword counts unchanged. B is 4,812 lines and 48,486 words.
- **Questions raised:** none.

### 2026-10-09 — §18: spruce-up pass, twenty-nine dash asides out; `[R-MTA-09]` in five paragraphs

- **Commit:** `Readable: §18 — spruce-up pass: seven paragraphs, the
  restriction list, three lead-ins and two Notes without asides; R-MTA-09
  in five paragraphs; R-MTA-02, -03, -05, -06, -07, -09, -10 listed` (the
  commit carrying this entry). Previous: `fdd0d93` (§17's pass).
- **Sections:** §18.1 (`[R-MTA-02]`), §18.2 (`[R-MTA-03]`, `[R-MTA-09]`,
  the JSON lead-in and `[R-MTA-04]`'s list, `[R-MTA-05]`, `[R-MTA-10]`, the
  JSON Note), §18.3 (`[R-MTA-06]`), §18.4 (the lead-in, `[R-MTA-07]`,
  `tarn.axes`, the Note). A spruce-up pass, not the maintainer's
  read-through; proposed with before and after
  (`scratch/cleanroom/proposals/s18-pass.md`), approved ("Go").
- **Edits.**
  1. `[R-MTA-02]`: the "— but" aside a sentence with "nevertheless".
     `[R-MTA-03]`: the fixed-structure aside a colon clause.
  2. `[R-MTA-09]`, 743 words in 73 ragged lines, made five paragraphs by
     topic: the reader's own bound (encoding 1); encoding 2's frame and
     its carried-over constraints; the decoded-size and `Window_Size`
     treatment; the content-size field; the verifier's decline. Six
     asides made clauses and a semicolon; one sentence split at "and no
     violation"; every sentence in A's order; all seven keyword clauses
     verbatim. The ID governs the fifth paragraph; the MAY decline, the
     SHOULD on the window and the content-size field's MAY and MUST stand
     in ID-less paragraphs, as `[R-LIF-06]`'s and `[R-LIF-08]`'s splits
     left theirs.
  3. The JSON lead-in: the dash a comma. `[R-MTA-04]`'s four restrictions:
     the overflow case a parenthesis, the escape-resolution aside a comma
     clause, and the key rules a sentence of their own ("Every key
     satisfies §4.6's name rules: non-empty, at most 255 bytes, free of
     U+0000 through U+001F"); the list's shape kept. The ID stands alone
     on the line after the list, which is what the inventory tool
     watches, so `[R-MTA-04]` is not listed.
  4. `[R-MTA-05]`: the content-addressing aside after a semicolon.
     `[R-MTA-10]`: six asides made a "which are" clause, a parenthesis, a
     colon and two sentence splits; the verifier's MUST now opens its own
     sentence ("It MUST report each record it ignored on this ground").
  5. `[R-MTA-06]`: the minor-versions aside a colon clause. The §18.4
     lead-in: "since being metadata none can affect decoding".
     `[R-MTA-07]`: the dash before "and enforcing them" a full stop.
     `tarn.axes`: the dash a colon. Two Notes: a parenthesis and a comma.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-MTA-02`, `R-MTA-03`, `R-MTA-05`, `R-MTA-06`,
  `R-MTA-07`, `R-MTA-09`, `R-MTA-10`, listed; twenty-three keyword
  clauses and figures checked.
- **Soft items:** `ID_REWORDED_LISTED` ×90 (the seven new); the carried
  items as before. Keyword counts unchanged. B is 4,829 lines and 48,510
  words.
- **Questions raised:** none.

### 2026-10-09 — §17: spruce-up pass, twenty-eight dash asides out

- **Commit:** `Readable: §17 — spruce-up pass: ten paragraphs and eight
  blocks without asides; R-COD-01 through -10 listed` (the commit carrying
  this entry). Previous: `eea3fa8` (§16's pass).
- **Sections:** §17.1 (`[R-COD-01]`, `[R-COD-02]`), §17.2 (`[R-COD-03]`
  through `[R-COD-08]`, six Notes), §17.3 (`[R-COD-09]`, `[R-COD-10]`, the
  Example, the Rationale). §17.4 (`[R-COD-11]`) untouched. A spruce-up
  pass, not the maintainer's read-through; proposed with before and after
  (`scratch/cleanroom/proposals/s17-pass.md`), approved ("Go").
- **Edits.**
  1. `[R-COD-01]`, `[R-COD-02]`: the codec's-input and dictionaries asides
     a participial clause and a comma.
  2. `[R-COD-03]`, `[R-COD-09]`: "all four are core" and "both are core"
     take colons before their MUSTs; the codec reader's three included
     cases follow the citation, as §12.2's do; "the filtered image is the
     decoded image" an "under which" clause.
  3. Codecs 1 and 2 (`[R-COD-04]`, `[R-COD-05]`): the checkability aside a
     comma, the raw-stream aside a colon; the run-in labels keep their
     dashes ("Codec 1 — none").
  4. Codec 3 (`[R-COD-06]`): three asides a comma clause (the dictionary),
     a "since" clause (the content-checksum reason) and a colon clause
     (the decoded size); re-wrapped; all thirteen keyword clauses, the
     magic and the figures verbatim.
  5. Codec 4 (`[R-COD-07]`): the cap's reason a comma clause after the
     MUST NOT; the planar rule ("each channel's plane carries its own
     decoded size, and the largest governs") a sentence of its own after
     the reader's MUST; re-wrapped.
  6. `[R-COD-08]`: "no more and no fewer" a comma clause. `[R-COD-10]`: the
     mapping gloss after a colon, the inverse a sentence of its own, the
     final dash a comma.
  7. Six Notes, the Example and the Rationale: sixteen asides made
     clauses, parentheses, semicolons or colons; every figure kept. A's
     lowercase "must support" and "may expand" in two re-wrapped Notes
     read "has to support" and "can expand".
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-COD-01` through `R-COD-10`, listed; eighteen keyword
  clauses, magics and figures checked verbatim.
- **Soft items:** `ID_REWORDED_LISTED` ×83 (the ten new); the carried items
  as before; the Example numbers unchanged. Keyword counts unchanged. B
  is 4,834 lines and 48,534 words.
- **Questions raised:** none.

### 2026-10-09 — §16: spruce-up pass, fifteen dash asides out

- **Commit:** `Readable: §16 — spruce-up pass: five paragraphs, two Notes
  and the Example without asides; R-SLB-01 through -05 listed` (the commit
  carrying this entry). Previous: `9793c06` (§15's pass).
- **Sections:** §16 (`[R-SLB-05]`), §16.1 (`[R-SLB-01]`, its Note), §16.2
  (`[R-SLB-02]`, `[R-SLB-03]`, `[R-SLB-04]`, the slabs Note, the Example). A
  spruce-up pass, not the maintainer's read-through; proposed with before
  and after (`scratch/cleanroom/proposals/s16-pass.md`), approved ("Go").
- **Edits.**
  1. `[R-SLB-05]`: the streaming-writer aside a "so" clause; the ID joined
     to the paragraph's last line.
  2. `[R-SLB-01]`: "readers are not obligated to, since offsets are always
     explicit and alignment is reader-invisible"; re-wrapped; all five
     keyword clauses verbatim.
  3. §16.1's Note: the page-size aside a comma clause; A's lowercase
     "recommended" reads "advised", the line being re-wrapped.
  4. `[R-SLB-02]`: the dash a semicolon, "and" joining the two block cases.
  5. `[R-SLB-03]`: the packing relation an appositive clause; the
     crc-failing entry's aside a colon clause ending in its "so"
     consequence; re-wrapped; the SHOULD, MUST and MAY verbatim.
  6. `[R-SLB-04]`: the dash before "or clear" a comma; "detected by a
     verifier as the invariant failures of `[R-SLB-03]` are" a sentence of
     its own; re-wrapped; the MUST and both options verbatim.
  7. The slabs Note: two dashes a colon and a comma, the label's dash
     kept; the Example: the run list after a comma; every figure kept.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-SLB-01`, `R-SLB-02`, `R-SLB-03`, `R-SLB-04`,
  `R-SLB-05`, listed; twelve keyword clauses and figures checked.
- **Soft items:** `ID_REWORDED_LISTED` ×73 (the five new); the carried items
  as before; the Example numbers unchanged. Keyword counts unchanged. B
  is 4,842 lines and 48,563 words.
- **Questions raised:** none. Process note: the session scratchpad was
  swept mid-session; the pass scripts now live in
  `scratch/cleanroom/pass/` (git-ignored) with the proposals beside them.

### 2026-10-09 — §15: spruce-up pass, thirteen dash asides out and one "notwithstanding"

- **Commit:** `Readable: §15 — spruce-up pass: four paragraphs, a Rationale
  and an Example without asides; R-IDX-02, -03, -04, -05 listed` (the
  commit carrying this entry). Previous: `17c527a` (§14's pass).
- **Sections:** §15.2 (`[R-IDX-02]`, the Rationale), §15.3 (`[R-IDX-03]`),
  §15.4 (`[R-IDX-04]`, `[R-IDX-05]`, the first Example). A spruce-up pass,
  not the maintainer's read-through; proposed with before and after
  (`scratch/cleanroom/proposals/s15-pass.md`), approved ("Go").
- **Edits.**
  1. §15.2 `[R-IDX-02]`: the dash before the 20 bytes a comma. The
     Rationale: "loudly invalid (§15.3)" a comma clause.
  2. §15.3 `[R-IDX-03]`: "The per-entry outcomes below govern
     notwithstanding the general owning-scope mapping of
     `[R-ENC-03]`/`[R-ENC-04]`" reads "The per-entry outcomes below
     override the general owning-scope mapping of `[R-ENC-03]` and
     `[R-ENC-04]`", the same precedence in a word the maintainer does not
     dislike; the run-continuity aside a sentence after a semicolon; the
     MUST verbatim. The outcome table untouched (table values stay).
  3. §15.4 `[R-IDX-04]`: the partial-segment aside a "so" clause, the
     consequence of "exactly those entries' bytes as stored"; the MUST
     and the MAY verbatim.
  4. §15.4 `[R-IDX-05]`: the definition of a full segment a comma clause;
     "a partial segment's CRC MUST be computed" a sentence of its own,
     capitalised; the constant, the MAY and the MUST verbatim.
  5. The first Example: four asides made comma and "with" clauses;
     "~339 KB" reads "about 339 KB"; every figure kept.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-IDX-02`, `R-IDX-03`, `R-IDX-04`, `R-IDX-05`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×68 (the four new); the carried items
  as before; the Example numbers unchanged. Keyword counts unchanged. B
  is 4,847 lines and 48,574 words.
- **Questions raised:** none.

### 2026-10-09 — §14: spruce-up pass, twenty-seven dash asides out

- **Commit:** `Readable: §14 — spruce-up pass: six paragraphs and seven
  blocks without asides; R-SER-01, -02, -03, -05, -07, -08 listed` (the
  commit carrying this entry). Previous: `db2b575` (§13's pass).
- **Sections:** §14.1 (`[R-SER-01]`), §14.2 (`[R-SER-02]`, `[R-SER-08]`, a
  Note, an Example), §14.3 (`[R-SER-03]`, `[R-SER-07]`, a Note), §14.4 (a
  Note, the Rationale), §14.5 (`[R-SER-05]`, the Example, the Rationale).
  A spruce-up pass, not the maintainer's read-through; proposed with
  before and after (`scratch/cleanroom/proposals/s14-pass.md`), approved
  ("Go").
- **Edits.**
  1. §14.1: the lead-in's dash a colon; the mode labels take colons; the
     adjacency aside "with each sample's channel values adjacent in
     declared channel order"; the list tight.
  2. §14.2 lead paragraph and `[R-SER-02]`: "in interleaved layers only
     since §14.3 governs planar bool planes" and "the decoded size" comma
     clauses; "a planar layer has no P · Q to form" after a colon.
  3. §14.2 `[R-SER-08]`: "whether or not it detected the violation" a comma
     clause; the returned value ("the value, encoded 0x00 or 0x01 as
     above, and not the stored byte") after a colon; both keyword clauses
     verbatim.
  4. §14.3 `[R-SER-03]`: two asides made colons; `[R-SER-07]`: the
     declarations aside a parenthesis.
  5. §14.5 `[R-SER-05]`: the three fill forms after "which is"; all three
     keyword clauses verbatim.
  6. Seven blocks (the bool-fill Note, the offsets Example, the pad-bits
     Note, the single-channel Note, §14.4's Rationale, §14.5's Example and
     Rationale): asides made commas, colons, parentheses or clauses; every
     figure kept. In the bool-fill Note A's lowercase "must" ("a fill byte
     it must interpret") is rewritten around as "a fill byte that it has
     to interpret", the line being re-wrapped.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-SER-01`, `R-SER-02`, `R-SER-03`, `R-SER-05`,
  `R-SER-07`, `R-SER-08`, listed; nine keyword clauses and figures
  checked verbatim.
- **Soft items:** `ID_REWORDED_LISTED` ×64 (the six new); the carried items
  as before; the Example numbers unchanged. Keyword counts unchanged. B
  is 4,847 lines and 48,583 words.
- **Questions raised:** none.

### 2026-10-09 — §13: spruce-up pass, thirteen dash asides out

- **Commit:** `Readable: §13 — spruce-up pass: four paragraphs and three
  blocks without asides; R-TYP-06, -08 listed` (the commit carrying this
  entry). Previous: `6903d04` (§12's pass).
- **Sections:** §13 (opening), §13.1 (`[R-TYP-06]`, the structural
  paragraph, the Note), §13.2 (the Rationale), §13.3 (`[R-TYP-08]`, the
  padding Note). A spruce-up pass, not the maintainer's read-through;
  proposed with before and after (`scratch/cleanroom/proposals/s13-pass.md`),
  approved ("Go").
- **Edits.**
  1. The opening: the reads-as-fill aside a "since" clause after "rather
     than an error".
  2. §13.1 `[R-TYP-06]`: "always present" given its reason as a "since"
     clause; the reader's three keyword clauses verbatim.
  3. §13.1's structural paragraph: "though it never affects how any byte
     is located or decoded" a sentence; the length-prefix clause a
     sentence.
  4. §13.1's Note: "deliberately so" after a comma.
  5. §13.2's Rationale: the §4.6 parallel after a colon.
  6. §13.3 `[R-TYP-08]`: the sentinel definition a "which is" clause, the
     declared-order aside a comma clause; the interleaved and planar
     cases two sentences; the MUST verbatim.
  7. §13.3's padding Note: the §14 aside a participial clause.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-TYP-06`, `R-TYP-08`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×58 (the two new); the carried items
  as before. Keyword counts unchanged. B is 4,852 lines and 48,601 words.
- **Questions raised:** none.

### 2026-10-09 — §12: spruce-up pass, eleven dash asides out

- **Commit:** `Readable: §12 — spruce-up pass: three paragraphs and three
  blocks without asides; R-TYP-03, -04, -05 listed` (the commit carrying
  this entry). Previous: `2dde2b2` (§11's pass).
- **Sections:** §12.1 (the bfloat16 Example), §12.2 (`[R-TYP-03]`, its
  Note), §12.3 (`[R-TYP-04]`, `[R-TYP-05]`, the channel-entry Example). A
  spruce-up pass, not the maintainer's read-through; proposed with before
  and after (`scratch/cleanroom/proposals/s12-pass.md`), approved ("Go").
- **Edits.**
  1. The bfloat16 Example: the nested aside a colon clause, the storage
     bytes `80 3F` placed beside the value they store; every figure kept.
  2. §12.2 `[R-TYP-03]`: the reader's three included cases moved from a
     dash aside inside the MUST to a colon clause after the citation ("0,
     every reserved value and the experimental range included"); the five
     value cases in A's order; the three keyword clauses verbatim.
  3. §12.2's Note: the 8-bit float reservation a clause and a sentence
     ("no other 8-bit float definition will be considered"); every number
     and name kept.
  4. §12.3 `[R-TYP-04]`: "never quieted, canonicalized or collapsed" a comma
     clause; the no-exception sentence split at its semicolon; the MUST
     NOT verbatim.
  5. §12.3 `[R-TYP-05]`: the inclusions a colon clause.
  6. The channel-entry Example: "a NaN carrying a payload" a comma clause;
     the twelve bytes kept on one line.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-TYP-03`, `R-TYP-04`, `R-TYP-05`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×56 (the three new); the carried
  items as before; the Example numbers unchanged (the tool reports none).
  Keyword counts unchanged. B is 4,852 lines and 48,609 words.
- **Questions raised:** none.

### 2026-10-09 — §11: spruce-up pass, ten dash asides out

- **Commit:** `Readable: §11 — spruce-up pass: five paragraphs without
  asides; R-GEO-01, -03, -04, -05, -06 listed` (the commit carrying this
  entry). Previous: `b1366ee` (§10's pass).
- **Sections:** §11.1 (`[R-GEO-01]`), §11.2 (`[R-GEO-03]`), §11.3
  (`[R-GEO-04]`), §11.4 (`[R-GEO-05]`, `[R-GEO-06]`). A spruce-up pass, not
  the maintainer's read-through; proposed with before and after
  (`scratch/cleanroom/proposals/s11-pass.md`), approved ("Go").
- **Edits.**
  1. §11.1 `[R-GEO-01]`: the parenthesis on the two tile-extent cases a
     colon clause after the MAY.
  2. §11.2 `[R-GEO-03]`: the dash aside on tile-index entries a comma
     clause; the sentence split before the total sample-position count.
  3. §11.3 `[R-GEO-04]`: three asides made a colon clause and a sentence
     (the padding condition; the definition of a padding position; the
     no-product form, "stated in a form that forms no product (§4.2)",
     verbatim); the §14 parenthesis a clause.
  4. §11.4 `[R-GEO-05]`: the value cases kept in A's order after a colon,
     "the last-declared dimension varies fastest" an "in which" clause;
     the reader's included cases ("0, every reserved value and the
     experimental range, which no conforming writer of format major
     version 1 emits") a sentence of their own.
  5. §11.4 `[R-GEO-06]`: the ordinals list's two asides a comma clause
     ("for every linearization value and permanently") and a colon clause
     ("channel-major grouping"); the list tight as in A.
- **Removed restatements:** none. Nothing dropped. §11.1's Rationale (272
  words restating §20.3 step 4) is left whole: §20.3 states every rule it
  restates except the two sentences on a growth that changes no grid
  count, which the rule check finds in no other words, so it is not a
  restatement this pass can cut; named for the read-through.
- **Reworded IDs:** `R-GEO-01`, `R-GEO-03`, `R-GEO-04`, `R-GEO-05`,
  `R-GEO-06`, listed; every keyword clause verbatim (eight checked).
- **Soft items:** `ID_REWORDED_LISTED` ×53 (the five new); the carried
  items as before. Keyword counts unchanged. B is 4,853 lines and 48,616
  words.
- **Questions raised:** none.

### 2026-10-09 — §10: spruce-up pass, four dash asides out

- **Commit:** `Readable: §10 — spruce-up pass: four paragraphs without
  asides; R-EXT-01, -03, -04, -05 listed` (the commit carrying this entry).
  Previous: `95b5a30` (§9's first pass).
- **Sections:** §10.1 (`[R-EXT-01]`), §10.3 (`[R-EXT-03]`), §10.4
  (`[R-EXT-04]`, `[R-EXT-05]`). A spruce-up pass on the maintainer's
  instruction of 2026-10-09, not his read-through; proposed with before and
  after (`scratch/cleanroom/proposals/s10-pass.md`), approved ("Go").
- **Edits.**
  1. §10.1's closing paragraph: the dash aside a clause ("never a minor
     revision and never an implementation's private convention").
  2. §10.3: the escape rationale its own sentence; the reader's three
     outcomes set space first and outcome second, in A's order, after the
     same colon; the MAY and both MUST NOTs verbatim.
  3. §10.4, registration: the three requirements a colon list counted as
     three (A lists exactly three); "sufficient for independent
     implementation without consulting any implementation" a clause; the
     MU = 0 sentence split at its semicolon.
  4. §10.4, the registry: the precedence reason a colon clause ("the
     registry is machine-readable convenience, never a second authority");
     the §21.1 parenthesis a sentence.
- **Removed restatements:** none. Nothing dropped.
- **Reworded IDs:** `R-EXT-01`, `R-EXT-03`, `R-EXT-04`, `R-EXT-05`, listed.
- **Soft items:** `ID_REWORDED_LISTED` ×48 (the four new); the eight term
  rewordings, Appendix B's row, `HEADINGS` 130 against 129, SHOULD 46
  against 47, all carried. Keyword counts unchanged. B is 4,852 lines and
  48,620 words.
- **Questions raised:** none.

### 2026-10-08 — §9, first pass: five dense paragraphs re-cut

- **Commit:** `Readable: §9 — first pass: five dense paragraphs re-cut;
  R-LIF-02, -03, -04, -06, -08 listed` (the commit carrying this entry).
  Previous: `5220d1a` (spec), `8fa607d` (log: round 1's rulings).
- **Sections:** §9.2 (`[R-LIF-02]`), §9.3 (`[R-LIF-03]`), §9.4
  (`[R-LIF-04]`), §9.6 (`[R-LIF-06]`), §9.7 (`[R-LIF-08]`). §9 was
  byte-identical to A before this commit. Proposed with before, after and
  inventory per paragraph (`scratch/cleanroom/proposals/s9-first-pass.md`),
  approved whole by the maintainer, list form and splits included.
- **Edits.**
  1. §9.2's commit protocol: the six steps set as a numbered list, each
     step's words and number kept; the three dash asides made clauses or a
     parenthesis ("zeroed by advice (`[R-CNT-03]`)"); "(file-scope or
     layer-scope)" reads "at file scope or layer scope". "MUST, in order"
     and the strict-increase sentence verbatim. The ID now governs the
     closing sentence; the steps are list items the inventory tool does
     not watch, the shape of `[R-CNT-21]`'s split.
  2. §9.3's first paragraph: one sentence made five. The two trailer
     values first; the file_id's SHOULD and its collision reason a
     sentence of their own; the strict increase; the immutability
     consequence; the three revalidation outcomes as a colon list ("the
     same F, and everything cached remains valid; a higher F, and the
     directory is refetched; a different file_id or a lower F, and the
     file is treated as a different file"). The SHOULD verbatim.
  3. §9.4: the torn sentence split at its colon; "(directly, or by
     recovery whose output has been re-verified)" a clause; "— so that …"
     reads "Either way, …". The three MUST clauses verbatim.
  4. §9.6's first paragraph, 411 words and eight dashes, made four
     paragraphs: the probe and the candidate (the reader aside its own
     sentence with a pointer to §9.5); enumeration against coverage
     verification and "no verdict turns on the probe"; the two cautions,
     numbered First and Second, with the expected-length argument; the
     start offset and the report. Both MUSTs, "Two cautions are normative
     for tools" and the candidate definition verbatim; the sentence order
     is A's. The ID governs the fourth paragraph; the two MUST clauses
     stand in the third, an ID-less normative paragraph.
  5. §9.7's walk paragraph, 435 words, made four paragraphs: the
     claimants; the checks and slack; decoding and certification; the
     incomplete walk. The parenthesis on the structural entry became two
     sentences; "It checks" reads "The verifier checks … these claimants";
     the "Where the walk does not complete — … —" aside became two
     sentences, the cases first ("The walk does not complete where …, where
     …, or where …") and the partial total second. The MUST NOT, "reports
     that check unmade and cannot certify (`[R-CNF-11]`, `[R-ERR-04]`)" and
     both `[R-IDX-03]` sentences verbatim. The ID governs the fourth
     paragraph; the MUST NOT stands in the third.
- **Removed restatements:** none. One duplicate pointer dropped: §9.7's
  "(§8.1)" closing the sentence that already says "where §8.1's map states
  one"; `0d7ab60`-era text, no ADR needed for a repeated pointer. §9.7 is
  the surviving statement of three §5.2 cuts (the entry for 2026-09-28):
  "contributes no stored extent to the walk", "does not make the walk
  incomplete …" and the incomplete-walk cases; the first two stand
  verbatim, the third in two sentences with the same three cases and the
  same consequence. Every cross-reference into §9 (§9.3 ×11, §9.7 ×10, §9.6
  ×9, §9.1, §9.2, §9.5) points at a subsection, and every subsection and
  heading stands.
- **Reworded IDs:** `R-LIF-02`, `R-LIF-03`, `R-LIF-04`, `R-LIF-06`,
  `R-LIF-08`, listed with the reasons above. Each paragraph decides what
  it decided: the ordered protocol and its strict increase; the file_id's
  source, the ordering and the cache contract; establishing F and the
  truncate-or-overwrite duty; the probe, the candidate, the two cautions
  and the report; the walk's claimants, checks, slack, certification bar
  and partial total.
- **Soft items:** `ID_REWORDED_LISTED` ×44 (the five new); `TERM_TEXT_CHANGED`
  ×8, `TABLE_ROW_ONLY_IN_A`/`_B` 1 each (Appendix B's user-metadata row's
  section cell), `HEADINGS` 130 in A against 129 in B (§3.3), SHOULD 46
  against 47 (`[R-CNT-26]`), all carried. Keyword counts otherwise
  unchanged. B is 4,854 lines and 48,624 words against A's 4,981 and
  49,821; the first pass adds 7 lines and 18 words to §9 and removes its
  22 em-dashes in these paragraphs.
- **Questions raised:** none. Held for the maintainer's specifics: §9.2's
  second Note and §9.3's first Note both argue the strict increase; §9.3's
  three Notes; the Example; §9.1 and §9.5 untouched.

### 2026-10-08 — §8: the coverage map stands on its own; the chain's outcomes without arrows

- **Commit:** `Readable: §8 — coverage map's exceptions stated in full,
  restoring what the §4.5 cut lost; chain-of-trust outcomes without arrows;
  R-CNT-19 and R-CNT-20 listed` (the commit carrying this entry).
  Previous: `4b0d01f` (spec), `7693731` (log).
- **Sections:** §8.1 (`[R-CNT-19]`), §8.2 (`[R-CNT-20]`).
- **A defect of the rewrite, found and repaired.** The entry for `8f16983`
  (2026-09-25) cut twelve lines from §4.5 as a restatement of §8.1's map.
  §8.1's own sentence named its second exception only by pointing at
  §4.5 ("this map's terminal checksum fields, per §4.5"); the cut text was
  where those fields were named ("the trailer, directory-region, and
  user-metadata checksum fields — which are verified by comparison and
  covered by no further checksum") and the only statement that interior
  checksum fields "are both comparison-verified and covered by exactly one
  further checksum". B had neither statement and a dangling pointer. The
  check that would have caught it is the one the memory note
  tarn-stated-once-is-a-rule-check describes: read what each clause of
  the surviving statement rests on, not its first sentence.
- **Edits.**
  1. `[R-CNT-19]`: "Every field of every structure is covered by exactly one
     checksum — excepting [three exceptions in a dash aside] — as this map
     states." becomes five sentences: the rule "with three exceptions";
     the front block by equality; the terminal checksum fields, now named
     here and said to be verified by comparison and covered by no further
     checksum; the unassigned record extent, with its reasons; the
     interior checksum fields, restored here. The CRC-32C sentence is
     verbatim. Every clause is A's, from §8.1 or from the §4.5 text cut
     on 2026-09-25, which now stands here.
  2. `[R-CNT-20]`: the outcomes read "the trailer or the directory,
     reject-file; any of a layer's index cross-checks (`[R-CNT-17]`), its
     CRC array or its segments, reject-layer; a stored tile's CRC,
     reject-tile; a user-metadata extent's CRC, ignore-record, and readers
     SHOULD report the loss …"; the chain of trust keeps its arrows, at
     the maintainer's word; the MUST and the SHOULD are verbatim.
- **Removed restatements:** none. Two statements moved into §8.1 from where
  §4.5 had them; the `8f16983` entry is corrected below.
- **Reworded IDs:** `R-CNT-19`, `R-CNT-20`, listed (thirty-nine in all);
  `R-ENC-10`'s reason line corrected.
- **Soft items:** `ID_REWORDED_LISTED` ×39 (two new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **Questions raised:** none. Untouched: §8.1's table, "Verification is not
  optional …" and §8.2's Note.

### 2026-10-05 — §7.4: `[R-CNT-18]`, parsing and sub-records, in nine sentences

- **Commit:** `Readable: §7.4 — inline-payload parsing and sub-record rules
  in nine sentences; R-CNT-18 listed` (the commit carrying this entry).
  Previous: `566330d`.
- **Sections:** §7.4, `[R-CNT-18]`'s paragraph.
- **Edits.** The first sentence (a colon and two semicolons) becomes four:
  "The inline payload MUST parse exactly."; the packing sentence; the two
  MUST clauses on what lies within the payload and how the rest parses;
  "Any overrun, truncation, or residue is a validity error at layer
  scope." The second (a semicolon, a parenthesis, two "and"s, a dash and
  another semicolon) becomes four: "Sub-records are layer-scope records.";
  the nesting MUST NOT with its parenthesis; the MU = 1 case with "a
  reader MUST NOT reject the file for it" and the `[R-CNF-12]` reservation
  after a semicolon in place of the dash; "With MU = 0 an unknown
  sub-record type is ignore-record." for "with MU = 0 it is
  ignore-record". The known-type sentence's dash pair becomes
  parentheses. Three MUSTs and two MUST NOTs verbatim. "Unknown sub-record
  type" is kept at the maintainer's word, `[R-CNT-15]`'s spelling-out not
  being repeated here.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-18`, listed (thirty-seven in all).
- **Soft items:** `ID_REWORDED_LISTED` ×37 (one new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **The §7 first pass is complete**: `[R-CNT-25]`, `-13`, `-14`, `-22`,
  `-18`, with `[R-CNT-11]`, `-15` and `-23` added along the way.
  `[R-CNT-12]` with its Note and the `[R-CNT-16]`/`[R-CNT-17]` paragraph
  were read by the maintainer and left as they are.
- **Questions raised:** none.

### 2026-10-04 — §7.4: `[R-CNT-23]`, the table's constraints, in sentences

- **Commit:** `Readable: §7.4 — table-constraint rule in three sentences;
  R-CNT-23 listed` (the commit carrying this entry). Previous: `d75a28b`.
- **Sections:** §7.4, `[R-CNT-23]`'s paragraph.
- **Edits.** "Writers MUST NOT emit a field violating a constraint in the
  table above; a reader MUST treat any such violation — including [four
  cases] — as a validity error at layer scope, except where another rule
  assigns a different scope (a duplicate layer name is file scope,
  `[R-ENC-15]`)." becomes three sentences: the MUST NOT; the MUST with
  its exception; "Such violations include a reserved or unassigned
  layout, codec, filter, index_encoding, or channel-type value (…), a
  nonzero A_slab with S = 0, a fill whose byte length differs from its
  type's element size, and a nonzero crc_of_crc_array with entry_count =
  0." The four cases, their order and their status as inclusions are
  unchanged ("or" before the last becomes "and" under "include"). The
  maintainer named the paragraph as R-CNT-32; no such ID exists, and the
  one-sentence paragraph under the layer record's table is this one.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-23`, listed (thirty-six in all).
- **Soft items:** `ID_REWORDED_LISTED` ×36 (one new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **Outstanding from the §7 first pass:** `[R-CNT-18]`.
- **Questions raised:** none.

### 2026-09-29 — §7.3: `[R-CNT-22]`, registry-fixed flags

- **Commit:** `Readable: §7.3 — fixed-flags rule without its analogy or its
  dash aside; R-CNT-22 listed` (the commit carrying this entry). Previous:
  `7f89555`.
- **Sections:** §7.3, `[R-CNT-22]`'s paragraph. 14 lines to 11.
- **Edits.** "A reader MUST apply a known type's specified semantics
  regardless of its stored MU and PE bits — a flipped stored bit never
  changes conforming behavior — and a verifier MUST treat the mismatch …"
  becomes two sentences: the reader's MUST with the aside after a colon,
  and "A verifier MUST treat the mismatch as a validity error at the
  record's governing scope; unreported, …". The three MUSTs are verbatim.
- **Removed restatements** (checked by rule): the closing clause ",
  exactly as they do for `[R-CNT-12]`'s reserved-flag and MU = 1 / PE = 0
  violations, whose detection this specification likewise assigns to the
  verifier" → `[R-CNT-12]` ("Both writer violations make the file
  nonconforming (`[R-CNF-05]`) while leaving conforming behavior
  unchanged, so their detection is a verifier's: a verifier MUST treat a
  nonzero reserved flag bit or the MU = 1 with PE = 0 combination as a
  validity error at the record's governing scope").
- **Reworded IDs:** `R-CNT-22`, listed (thirty-five in all).
- **Soft items:** `ID_REWORDED_LISTED` ×35 (one new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **Outstanding from the §7 first pass:** `[R-CNT-18]`.
- **Questions raised:** none. `[R-CNT-12]` and its Note were read by the
  maintainer and left as they are.

### 2026-09-29 — §7.2: `[R-CNT-15]`, the unknown record type, in sentences

- **Commit:** `Readable: §7.2 — unknown record type rule in sentences;
  R-CNT-15 listed` (the commit carrying this entry). Previous: `40997f1`.
- **Sections:** §7.2, `[R-CNT-15]`'s paragraph.
- **The maintainer's edit.** "… has not assigned — emitting it is a
  violation" → "… has not assigned. Emitting one from the reserved range
  is a violation"; reviewed as the same statement, and trimmed at the
  maintainer's word to "Emitting one is a violation", the sentence before
  naming the range.
- **The driver's edits, at the maintainer's request.** The opening
  shorthand "An unknown record type at file scope: MU = 1 → reject-file;
  MU = 0 → ignore-record." becomes "A record at file scope whose type the
  reader does not implement is governed by its stored MU bit: MU = 1 is
  reject-file, and MU = 0 is ignore-record." ("unknown" is A's word for a
  type the reader does not implement, §2.3 and §7.3). "This governs a
  reader's treatment, not the file's validity:" becomes "That rule is
  about what a reader does, not about whether the file is valid."; the
  experimental and reserved ranges each get a sentence; "Readers of both
  apply the MU rule above unchanged" becomes "A reader applies the MU rule
  to both, unchanged." The verifier's MUST is verbatim.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-15`, listed (thirty-four in all).
- **Soft items:** `ID_REWORDED_LISTED` ×34 (one new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **Outstanding from the §7 first pass:** `[R-CNT-22]`, `[R-CNT-18]`.
- **Questions raised:** none.

### 2026-09-29 — §7.2: `[R-CNT-14]`, order and multiplicity, in five sentences

- **Commit:** `Readable: §7.2 — order and multiplicity in five sentences;
  R-CNT-14 listed` (the commit carrying this entry). Previous: `e3b6ded`.
- **Sections:** §7.2, `[R-CNT-14]`'s paragraph.
- **The maintainer's edit.** ", an empty directory included" removed from
  the parenthesis on zero layer records. Reviewed: an empty directory is a
  directory carrying no layer record, so the phrase named a special case
  of its own clause.
- **The driver's edit.** The one sentence (a dash, a parenthesis, two
  semicolons) becomes five: the two MUST NOTs; "Multiplicity rules are per
  type."; "In format major 1 a directory carries any number of layer
  records, including none (§21.6)."; the file-scope user-metadata rule;
  the sub-record rule. "Zero is valid: a directory carrying no layer
  record is a conforming generation" said one thing twice; the pointer
  version, chosen by the maintainer, leaves the consequence to §21.6.
- **Removed restatements** (checked by rule):
  - "a directory carrying no layer record is a conforming generation" →
    §21.6's row "The file contains zero layers" ("A conforming file: a
    directory carrying no layer record is a conforming generation whether
    or not it carries other records"), and §24's minimal file ("It
    contains no layers, which §21.6 records as valid").
  - "an empty directory included" → the same row; §7.2's "zero or more
    records"; §5.1's smallest-file Example.
  Origins: "zero is valid …" `86162e0`, Batch 3 (ADR-0029 to ADR-0032);
  "an empty directory included" `09cd44c`, ADR-0123.
- **Reworded IDs:** `R-CNT-14`, listed (thirty-three in all).
- **Correction.** The `[R-CNT-13]` entry below said "31 lines to 28"; the
  result was 27. Corrected there.
- **Soft items:** `ID_REWORDED_LISTED` ×33 (one new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **Outstanding from the §7 first pass:** `[R-CNT-22]`, `[R-CNT-18]`.
- **Questions raised:** none.

### 2026-09-29 — §7.2: `[R-CNT-13]`, the extent slot, re-cut

- **Commit:** `Readable: §7.2 — extent slot paragraph re-cut; its
  restatement of §5.2 made a pointer; R-CNT-13 listed` (the commit carrying
  this entry). Previous: `0af72b6`.
- **Sections:** §7.2, `[R-CNT-13]`'s paragraph. 31 lines to 27.
- **Edits.** The five dash asides become sentences or clauses: the sum's
  designation under `[R-ENC-04]`; "A malformed slot on a layer record is
  therefore reject-layer"; "which is what lets a rewriter relocate an
  unknown ancillary's extent without parsing it". The verifier's MUST keeps
  its three outcomes and their order, with "including a stored extent
  overlapping its own layer's index region or sub-record extents" placed
  after "as reject-layer" and ending "included". "(readers are not
  obligated to detect overlap, …)" becomes a sentence.
- **Removed restatements** (checked by rule; the maintainer asked whether
  the paragraph's end was the defining statement or a copy):
  - "within the live committed state — all structures reachable from the
    live trailer, whichever generation's commit appended them — no two
    extent slots and no two structures overlap" → §5.2 `[R-CNT-02]`, which
    defines the live committed state and states "No two of them overlap";
    `[R-CNT-13]` now reads "no two extent slots and no two structures of
    the live committed state overlap (§5.2, `[R-CNT-02]`)". `86162e0`,
    Batch 3 (ADR-0029 to ADR-0032). What `[R-CNT-13]` alone defines is the
    outcome an overlap draws, and register rows F33 and L18 name it as
    their governing rule; that sentence is verbatim.
- **Reworded IDs:** `R-CNT-13`, listed (thirty-two in all).
- **Soft items:** `ID_REWORDED_LISTED` ×32 (one new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **Outstanding from the §7 first pass:** `[R-CNT-14]`, `[R-CNT-22]`,
  `[R-CNT-18]`.
- **Questions raised:** none.

### 2026-09-29 — §7.1: the directory region says what it holds

- **Commit:** `Readable: §7.1 — directory region's contents stated first;
  R-CNT-11 listed` (the commit carrying this entry). Previous: `9a67884`.
- **Sections:** §7.1, `[R-CNT-11]`'s paragraph.
- **Edits.** "Its final 4 bytes are a CRC-32C over the preceding dir_length
  − 4 bytes; those covered bytes are the record sequence itself — the
  directory is always raw, with no codec involvement on the open path."
  becomes "It holds the record sequence (§7.2) in its first dir_length − 4
  bytes and, in its final 4, a CRC-32C over them. The directory is always
  raw, with no codec involvement on the open path." The maintainer asked
  whether the region's content is the record sequence; it is, and A said
  so after the CRC. Same figures; the MUST sentence and the owning-scope
  sentence are verbatim. Agrees with §3.1's *directory*.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-11`, listed (thirty-one in all).
- **Soft items:** `ID_REWORDED_LISTED` ×31 (one new); the Appendix B row,
  `KEYWORD_COUNT SHOULD` 46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS`
  carried.
- **Questions raised:** none.

### 2026-09-29 — §7.1 → §7.3: user metadata's rules moved after the things they use, and re-cut

- **Commit:** `Readable: §7 — user-metadata rules moved to the end of §7.3
  and re-cut; four citations re-pointed; R-CNT-25, R-MTA-01, R-SEC-05,
  R-SEC-06, R-PRV-03 listed` (the commit carrying this entry). Previous:
  `083cc8d` (spec), `ffe5700` (log).
- **Sections:** §7.1 (now `[R-CNT-11]` alone, ten lines), §7.3 (two
  paragraphs added at its end), and one citation each in §18, §22 (two),
  §23 and Appendix B.
- **Edits.**
  1. `[R-CNT-25]`'s paragraph leaves §7.1, where it used the extent slot
     and the user-metadata record type before §7.2 and §7.3 introduce
     them (the maintainer could not tell which of "(0, 0)" was which), and
     goes to the end of §7.3, after `[R-CNT-22]`.
  2. It is re-cut, in two paragraphs. First: what is compressed and what is
     raw (the old last sentence joined to the old first); where the
     document lives; "On a user-metadata record, an extent slot of (0, 0)
     or an extent_length less than 5 is a validity error at its
     containing scope: fewer than 5 bytes cannot hold both a document and
     the terminal CRC-32C §8.1 places in the final 4"; the encoding rule,
     "ignore-record, and SHOULD be reported" (the maintainer's "and").
     Second: the quarantine, with "notwithstanding the owning-scope
     mapping of `[R-CNF-08]`" restated as "The quarantine overrides the
     owning-scope mapping of `[R-CNF-08]`: the outcome is ignore-record
     whichever scope owns the record"; and the resource-decline sentence
     restated as the quarantine's limit: "The quarantine does not reach a
     resource decline: a reader that declines a document on resource
     grounds MAY decline a scope containing it, which `[R-MTA-09]` and
     `[R-ERR-04]` govern."
  3. Four citations that said §7.1 and meant these rules now say §7.3:
     `[R-MTA-01]` (§18), `[R-SEC-06]` (§22), `[R-PRV-03]` (§23) and
     Appendix B's row "User-metadata extent minimum". The three citations
     of §7.1 that mean the directory CRC are unchanged.
- **Removed restatements:** none; the resource-decline sentence, which
  restates `[R-ERR-04]` ("It MAY also decline at any scope that contains
  the narrowest one"), is kept as the quarantine's stated limit.
- **Reworded IDs:** newly listed `R-CNT-25`, `R-MTA-01`, `R-SEC-05` (shares
  `[R-SEC-06]`'s paragraph), `R-SEC-06`, `R-PRV-03` (thirty in all).
- **Unwatched paragraph.** `[R-CNT-25]` stands in the quarantine paragraph;
  the paragraph before it carries two rules (the extent rule, the encoding
  rule with its SHOULD) and no ID.
- **ADR candidate, parked by the maintainer: split `[R-CNT-25]`.** The
  first paragraph's rules want an ID of their own (`[R-CNT-28]` is the
  next free number). The register already divides that way: F21, F22,
  L10, L11 and R1 cite `[R-CNT-25]` for the first paragraph's conditions,
  R2 through R10 for the quarantine. IDs are fixed while B is open
  (ADR-0133 decision 3), so this is an ADR against A on `main`, ported to
  B; the driver's suggestion is one ADR for every ID-less rule paragraph
  the rewrite leaves (§5.2's three under `[R-CNT-21]`, §21.6's closing
  paragraph, this one), re-pointing register rows and vectors once.
- **Soft items:** `ID_REWORDED_LISTED` ×30 (five new); `TABLE_ROW_ONLY_IN_A`
  and `_IN_B`, one each, Appendix B's row with its section cell changed;
  `KEYWORD_COUNT SHOULD` 46/47 carried; `TERM_TEXT_CHANGED` ×8 and
  `HEADINGS` carried.
- **Outstanding from the §7 first pass**, proposed 2026-09-29 and parked by
  the maintainer until this item was done: `[R-CNT-13]` (the extent
  slot), `[R-CNT-14]` (order and multiplicity), `[R-CNT-22]` (the closing
  analogy), `[R-CNT-18]` (parsing and sub-records).
- **Questions raised:** none open.

### 2026-09-29 — §6.4: the Note's last sentence; `[R-CNT-10]` in five sentences

- **Commit:** `Readable: §6.4 — accounting Note's close; transport rules in
  five sentences; R-CNT-10 listed` (the commit carrying this entry).
  Previous: `f60d1a9`.
- **Sections:** §6.4, the Note and the closing paragraph.
- **Edits.**
  1. The Note's last sentence, "That is the invariant this section exists
     to make legible, and the request counts are what it costs a reader
     that fetches exactly what it needs.", becomes "That working set is
     what this section describes; the request counts are only what
     fetching exactly that costs."
  2. `[R-CNT-10]`: "MUST handle a 200 response to a range request (HTTP's
     terms, RFC 9110, where the transport is HTTP; abort or accept the
     full body deliberately — never treat the body prefix as the requested
     range) and SHOULD fall back …" becomes three sentences: the MUST with
     what handling is after a colon ("it aborts, or accepts the full body
     deliberately, and never treats the body's prefix as the requested
     range"); "The terms are HTTP's (RFC 9110), where the transport is
     HTTP."; the SHOULD with its consequence after a semicolon. The
     transport-authoritative sentence's parenthesis becomes a colon list,
     and its second half a sentence of its own. Five keyword clauses
     verbatim.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-10`, listed (twenty-five in all).
- **Soft items:** `ID_REWORDED_LISTED` ×25 (one new); `KEYWORD_COUNT SHOULD`
  46/47, `TERM_TEXT_CHANGED` ×8 and `HEADINGS` carried.
- **Questions raised:** none.

### 2026-09-29 — §6.2, §6.3: the maintainer's second batch, reviewed; the flags paragraph re-cut

- **Commit:** `Readable: §6.2, §6.3 — maintainer's edits, reviewed; flags
  paragraph re-cut; R-CNT-07, -24, -26 listed` (the commit carrying this
  entry). Previous: `f3a14cf`.
- **Sections:** §6.2 (`[R-CNT-06]`, the second Note); §6.3 (`[R-CNT-07]`,
  `[R-CNT-24]`, `[R-CNT-08]`, `[R-CNT-26]`).
- **The maintainer's edits, as committed.**
  1. `[R-CNT-06]`: "Those gates passed," → "If those gates pass,";
     "reserved bytes zero" → "reserved bytes all zero". Same rule.
  2. §6.2's second Note: "at exact physical end of file" → "at the exact
     physical end of the file"; "(§7.1) — detection is never silent" →
     "(§7.1). Detection is never silent". Explanatory.
  3. `[R-CNT-07]`: the dash before the consequence becomes a full stop;
     "files that current software reads" → "files that other software can
     read". The consequence of the SHOULD, in plainer words.
  4. `[R-CNT-24]`: "permanently:" → "the following are permanently
     required:", **changed on review** to "… permanently fixed:". "Required"
     is one of the seven words kept out of added lines (`tarn_check` warned
     on it), and A states facts that hold in every major, not an
     obligation; "fixed" is the reach paragraph's own word for them.
  5. `[R-CNT-08]`: "such bits are defined by later minor versions" → "such
     bits might be defined …", **superseded on review** by the re-cut below:
     A's sentence says what the ignore lane is for, and "might" put a
     particular bit in doubt against the paragraph's own later sentence.
  6. `[R-CNT-26]`: "— for a file expressible under this text, 0 — and an
     appender the maximum …" → "(for a file expressible under this text,
     version_minor is 0). An appender SHOULD emit the maximum …"; and, on
     review, the consequence ("A higher minor than needed costs readers
     nothing …") made a sentence of its own so that it covers both SHOULDs.
     The second SHOULD is A's first, written out where A elided it.
- **The driver's edit, at the maintainer's request.** `[R-CNT-08]` re-cut
  into six sentences. "In this specification's text no flag bits are
  defined: a writer … MUST write flags = 0, but a set ignore-lane bit is
  not a file-conformance violation — such bits are defined by later minor
  versions, and files carrying them are conforming files this text's
  readers ignore." becomes "This specification's text defines no flag
  bits, so a writer creating a file under this text MUST write flags = 0.
  A set ignore-lane bit is nevertheless not a file-conformance violation:
  the ignore lane is where later minor versions define bits, and a file
  carrying one is a conforming file whose bit this text's readers ignore."
  (A's clause could be read as readers ignoring the files.) The updater's
  three duties stand alone; ADR-0121's sentence follows with its reason as
  "since this text defines none"; "An updater encountering … is a reader
  first, and therefore rejects" becomes "An updater that meets … is a
  reader first, and rejects". All six keyword clauses verbatim.
- **Removed restatements:** none.
- **Reworded IDs:** newly listed `R-CNT-07`, `R-CNT-24`, `R-CNT-26`
  (twenty-four in all); `R-CNT-06` and `R-CNT-08` extended.
- **Soft items:** `ID_REWORDED_LISTED` ×24; **`KEYWORD_COUNT SHOULD`, 46 in
  A and 47 in B**: the appender's SHOULD in `[R-CNT-26]`, which A carried
  by ellipsis ("A writer SHOULD emit … and an appender the maximum …");
  no rule added. `TERM_TEXT_CHANGED` ×8 and `HEADINGS` carried.
  `tarn_check`: 10 warnings.
- **Questions raised:** none open.

### 2026-09-29 — §6.1, §6.2: the maintainer's four edits, reviewed; residency defined

- **Commit:** `Readable: §6.1, §6.2 — maintainer's edits, reviewed;
  residency defined` (the commit carrying this entry). Previous: `2124a23`.
  The first batch under the review workflow agreed the same day: the
  maintainer edits `spec/tarn.md`, the driver reads the word diff, checks
  each edit against A, and commits.
- **Sections:** §6.1 (the line above the table, the definitions paragraph,
  `[R-CNT-04]`, the media-type Note); §6.2 (`[R-CNT-05]`).
- **The maintainer's edits.**
  1. §6.1, above the table: "Bytes [0, 16) of every file, constant in
     every format major version:" → "… of every file are constant in …". A
     fragment made a sentence; the rule is `[R-CNT-24]`'s. Same statement.
  2. §6.1, `[R-CNT-04]`: the dash pair around the list of resident cases →
     "(e.g. a local file read whole, a memory mapping, a speculative suffix
     window that reached offset 0, or any transport already holding
     them)". The list becomes examples; see the driver's edit below.
  3. §6.1, the Note: "no other prefix of a conforming file is constant" →
     "no further prefix …". Explanatory; and more accurate, every shorter
     prefix of the block being constant too.
  4. §6.2, `[R-CNT-05]`: "leaves none" → "leaves no pad". Same meaning.
- **The driver's edit, on the maintainer's observation that *residency* is
  used and never defined.** The definitions paragraph's last sentence
  becomes "The obligation over the front block turns on **residency**
  instead: bytes are resident when the reader already holds them after its
  open, so that reading them takes no further range request." The bold
  moves there from `[R-CNT-04]`'s "resident". The definition is derived
  from A's own text: `[R-CNT-04]` partitions readers into those whose open
  "leaves bytes [0, 16) resident" and those that "would have to issue a
  further range request to obtain those bytes", and register row F6 binds
  "a reader holding those bytes resident". In A the dash list, ending in
  the catch-all "any transport already holding them", did the work of a
  definition; with "e.g." it no longer does, so the definition is stated.
  This is B saying what A implies; the fidelity round grades it.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-04` and `R-CNT-05`, already listed; reason lines
  extended.
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×21, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged.
- **Questions raised:** none open. Offered and not taken: "no longer
  prefix" for the Note.

### 2026-09-29 — §6, first pass: five dense paragraphs re-cut

- **Commit:** `Readable: §6 — definitions, pre-trailer pad, validation
  order, flags and baseline open re-cut; R-CNT-04, -05, -06, -08, -09
  listed` (the commit carrying this entry). Previous: `2bef8ff` (spec),
  `256e5f1` (log).
- **Sections:** §6.1, §6.2, §6.3, §6.4. §6 falls from 185 lines to 178. The
  maintainer took all five as a first pass and will return with specifics.
- **Edits.** Every keyword sentence is verbatim.
  1. §6.1, the local/remote definitions (no ID): two definitions and the
     three things the distinction governs, as four sentences; its reason
     for residency ("a transport can be classified either way at the
     margin while residency is decidable at any reader's own open path")
     moves into `[R-CNT-04]`'s closing sentence, which stated the same
     reason in other words: "The test is residency, not transport: a
     transport can be classified either way at the margin, while an
     implementation decides residency at its own open path without having
     to classify the network underneath it."
  2. §6.2, `[R-CNT-05]`: the pre-trailer pad paragraph in six sentences,
     no dashes; "their number" is "its length"; "a longer gap is
     conforming, and no conforming commit produces one" reads "…, though
     no conforming commit produces one".
  3. §6.2, `[R-CNT-06]`: "— only these touch fields whose positions are
     fixed across all majors (`[R-CNT-24]`) — and then, those gates
     passed, MUST validate" becomes "Only these three touch fields whose
     positions are fixed across all majors (`[R-CNT-24]`). Those gates
     passed, the reader MUST validate"; the list is unchanged.
  4. §6.3, `[R-CNT-08]`: one sentence cut (below).
  5. §6.4, `[R-CNT-09]`: step 1's dash clause with its parenthesis becomes
     three sentences; "(1) fetch" and "(2) fetch" are capitalised as
     sentences.
- **Removed restatements** (checked by rule):
  - "A rewriter, though its output is a new file, carries the input's
    unknown ignore-lane bits into its output trailer rather than writing
    flags = 0, and sets no other (§20.5, `[R-WRT-06]`)." → §20.5
    `[R-WRT-06]` ("The output trailer MUST copy the input's unknown
    ignore-lane flag bits forward and set no other, in place of the flags
    = 0 §6.3 requires of a file created under this text") and the next
    sentence of `[R-CNT-08]` itself ("carried forward by every updater
    under this text, appender and rewriter alike"). Origin not found by
    `git log -S` on its opening words (the sentence was rewrapped); it
    follows ADR-0121's text.
  - the residency reason stated twice in §6.1 → once, in `[R-CNT-04]`;
    both from `b027e12`, ADR-0058.
- **Reworded IDs:** `R-CNT-04`, `R-CNT-05`, `R-CNT-06`, `R-CNT-08`,
  `R-CNT-09`, listed (twenty-one in all).
- **Soft items:** `ID_REWORDED_LISTED` ×21 (five new); `TERM_TEXT_CHANGED`
  ×8 and `HEADINGS` carried. Keyword counts unchanged.
- **Questions raised:** none. Untouched in §6: both tables, `[R-CNT-07]`,
  `[R-CNT-24]`, `[R-CNT-26]`, `[R-CNT-10]`, the Rationale and the Notes.

### 2026-09-28 — §5.2's Rationale cut to its argument

- **Commit:** `Readable: §5.2 — Rationale cut to its argument` (the commit
  carrying this entry). Previous: `fe73fa6`.
- **Sections:** §5.2, the Rationale.
- **Edits.** The Rationale keeps its argument (slack is a byproduct;
  certifying it would mean deciding which slack bytes this commit wrote,
  which the live state cannot tell; so the live state is certified and the
  rest counted) and loses "— not a record anyone keeps: this format is not
  a version store, and an operator paying for storage compacts rather than
  retains". "Which is not decidable from the live state — the only thing a
  reader ever walks" becomes "and the live state, the only thing a reader
  ever walks, cannot tell".
- **Removed restatements:** the version-store commentary → §9.7's Note ("a
  history the format does not promise to keep and a rewrite is expected to
  discard") and §1's third goal; `f738b29`, ADR-0048.
- **Correction.** The §1 entry of 2026-09-23 gave "§7's Note" as the
  surviving location of "this format is not a version store". It was this
  Rationale, in §5.2. Corrected there, with the present cut noted.
- **Reworded IDs:** none (a Rationale).
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×16, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged. `tarn_check`: 10 warnings.
- **Questions raised:** none. The first Note of §5.2 was read by the
  maintainer and left as it is.

### 2026-09-28 — §5.2: the coverage definition without dashes; the slack paragraph in four

- **Commit:** `Readable: §5.2 — coverage definition plain; slack paragraph
  split in four, §9.7's restatements cut; R-CNT-02 and R-CNT-21 listed` (the
  commit carrying this entry). Previous: `5296c8b`.
- **Sections:** §5.2, the paragraphs of `[R-CNT-02]` and `[R-CNT-21]`. The
  `[R-CNT-03]` paragraph, the Rationale and the two Notes are untouched.
- **Edits.**
  1. `[R-CNT-02]`: the two dash-set definitions become colon and
     which-clauses; the live committed state's members and a structure's
     four kinds are the same lists; the partition rule is verbatim.
  2. `[R-CNT-21]`: one paragraph of 40 lines becomes four of 31 in all:
     what slack is, that a reader MUST NOT interpret it and that only a
     rewrite reclaims it; the verifier's total and the case in which none
     is owed; when the total is partial and what leaves the walk complete;
     what a partial total is and what the verifier says beside it. "Which
     is not a partial total but the absence of one" becomes "which is the
     absence of a total and not a partial one"; "a tile's or a document's
     decode declined leaves the walk complete, that claimant being
     enumerated from its index entry or extent slot" becomes "Declining to
     decode a tile or a document leaves the walk complete: its extent is
     still enumerated, from its index entry or its extent slot" (the
     maintainer's complaint); "It is not the file's slack total but a
     bound on it, tightening …" folds into the partial-total sentence. The
     three MUSTs and the MUST NOT are verbatim.
- **Removed restatements** (checked by rule against §9.7's full text, not
  by phrase):
  - the three cases in which the walk is incomplete (a scope-level
    rejection, a layer declined on resource grounds under `[R-ERR-04]`,
    stopping at the first violation under `[R-CNF-11]`) → §9.7
    `[R-LIF-08]`: "Where the walk does not complete — a scope-level
    rejection blocks enumeration, the verifier declines a layer on
    resource grounds and so never enumerates its claimants
    (`[R-ERR-04]`), or it stops at the first violation (`[R-CNF-11]`) —
    the sum is reported as partial, and `[R-CNT-21]` governs what such a
    total counts"; §5.2 keeps "§9.7 says when that is". Added by `af08428`,
    the pre-round-32 audit, over `140d491` (ADR-0065).
  - "An entry `[R-IDX-03]` classifies reject-tile on a structural ground
    leaves it complete too …" → §9.7, stated at its opening ("contributes
    no stored extent to the walk") and its close ("does not make the walk
    incomplete: the walk passes over it, and the bytes of the file it
    nominally addresses fall to slack where no other claimant claims
    them (§15.3)"); `42e60b8`, the pre-round-33 audit of ADR-0125, over
    `d29d9d7`.
- **Reworded IDs:** `R-CNT-02` and `R-CNT-21`, listed (sixteen in all).
- **Unwatched paragraphs.** `[R-CNT-21]` now stands in the fourth paragraph
  only. The first three carry rules (one MUST NOT, two MUSTs) and no ID, so
  `tarn_inventory.py` cannot see a change to them; any later edit to them
  is a rule edit and goes through the maintainer, and the fidelity round
  is their guard (calibration 2's C6 was such a paragraph).
- **Soft items:** `ID_REWORDED_LISTED` ×16 (two new); `TERM_TEXT_CHANGED`
  ×8 and `HEADINGS` carried. Keyword counts unchanged.
- **`tarn_check` warnings: 11 → 10.** REG-08, the register-completeness
  heuristic, no longer says "R-CNT-21 names a violation and no register row
  cites it at all": it reads the paragraph the ID stands in, and the
  rejection language that tripped it (§6.2's rejecting validation, the
  rejected layer) is now in the second and third paragraphs. The warning
  was the heuristic's, not a finding; `[R-CNT-21]` states a verifier's
  reporting duty and names no violation. Recorded because a warning that
  disappears is a change in what a gate says.
- **Questions raised:** none.

### 2026-09-28 — §5.1: the three-commits Example's last two paragraphs

- **Commit:** `Readable: §5.1 — three-commits Example, its last two
  paragraphs in plain sentences` (the commit carrying this entry).
  Previous: `711a94f`.
- **Sections:** §5.1, the second Example.
- **Edits.** The paragraph beginning "The ▓ runs are" is re-cut into five
  sentences: the dash-set aside "a user-metadata document lives in one,
  `[R-CNT-25]`", which the maintainer could not parse, becomes "such as the
  extent that holds a user-metadata document (`[R-CNT-25]`)"; "re-emits the
  directory, the pad and the trailer alone" becomes "re-emits only …"; the
  two sentences about layer B join the index-region sentence after a
  colon; "A commit never relocates a live index region otherwise; that is
  a rewrite's operation" becomes "… for any other reason; relocation is a
  rewrite's operation". The closing paragraph drops "Because … must change"
  for "The structures that change on every commit are the last ones in the
  file, so …", which also removes a lowercase keyword from the Example.
  Every citation is kept.
- **Removed restatements:** none.
- **Reworded IDs:** none (an Example).
- **Soft items:** unchanged (`ID_REWORDED_LISTED` ×14, `TERM_TEXT_CHANGED`
  ×8, `HEADINGS`). Keyword counts unchanged; no number in the Example
  changed.
- **Questions raised:** none.

### 2026-09-28 — §5.1: the anatomy sentence in three

- **Commit:** `Readable: §5.1 — what lies between the front block and the
  trailer, in three sentences` (the commit carrying this entry). Previous
  spec commit: `eacb6cc`.
- **Sections:** §5.1, `[R-CNT-01]`'s paragraph.
- **Edits.** "Between them lie the regions the file's commits appended —
  stored-tile payloads, tile-index regions, record extents (§5.2), the
  directory each commit appended, and each prior generation's trailer —
  with the superseded among them slack and no structure (§5.2), and slack
  wherever a commit left a gap; a commit appends its own directory,
  pre-trailer pad, and trailer last, in that order (§6.2, `[R-LIF-02]`
  steps 3 and 5)." becomes "Between them lie the regions each commit
  appended: stored-tile payloads, tile-index regions, record extents
  (§5.2), each commit's directory, and each prior generation's trailer. A
  region a later commit superseded is slack with no structure (§5.2), as
  is any gap a commit left. Each commit appends its directory, its
  pre-trailer pad and its trailer last, in that order (§6.2, `[R-LIF-02]`
  steps 3 and 5)." The maintainer's wording for "each commit appended" and
  "slack with no structure". The file-size sentence and its ID are
  verbatim.
- **Removed restatements:** none.
- **Reworded IDs:** `R-CNT-01`, listed (fourteen in all).
- **Soft items:** `ID_REWORDED_LISTED` ×14 (one new); `TERM_TEXT_CHANGED` ×8
  and `HEADINGS` carried. Keyword counts unchanged.
- **Questions raised:** none.

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
    **Corrected 2026-10-08:** wrong in part. §8.1 named its second
    exception only as "this map's terminal checksum fields, per §4.5", and
    the words naming those fields, and the interior-checksum sentence,
    were in the text cut here and nowhere else. Both are restored into
    §8.1 by the entry of 2026-10-08 ("§8: the coverage map stands on its
    own").
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
    by compaction is the shape it is built for" → §5.1 (slack), §5.2's
    Rationale ("this format is not a version store"; this entry first
    said §7's Note, wrongly; and since 2026-09-28 the Rationale no longer
    carries the phrase, the thought standing in §9.7's Note); `f738b29`,
    ADR-0048.
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
