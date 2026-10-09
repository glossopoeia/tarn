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

Stretches done through §8 on 2026-10-08.

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

## Entries

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
