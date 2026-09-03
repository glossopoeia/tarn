# Round-30 repair audit — lane "the-tools" (hunks 02, 10, 11)

## 0. Disclosure

Read:
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-02.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-10.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-11.diff
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md — via `sed -n` ranges and `grep`:
  headings list (`grep -n '^#'`); lines 55-64, 95-117, 117-152, 195-215, 285-331, 670-684, 684-757, 801-851,
  851-932, 965-1043, 1068-1180, 1182-1223, 1235-1313, 1313-1362, 1362-1378, 1378-1400, 1400-1500, 1502-1545,
  2131-2260, 2269-2335, 3054-3110, 3140-3150, 3364-3569, 3571-3600, 3676/3681/3684 (F8, F14, F17),
  3839-3960, 4110-4125, 4222-4234, 4247-4334, 4615-4635, 4655-4739.
Wrote: this file only. No scratch files (all computation was inline shell: `grep`, `sed`, `tr`, `wc`).
Not read: docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, git history,
full.diff, any other hunk file, the case directory listing, the web.

Unrequested context that appeared before I began: a project CLAUDE.md (one line pointing to AGENTS.md — I did
not open AGENTS.md); an index of the user's auto-memory files (four titles, which I did not open); an
environment block naming the branch and five recent commit subjects (which name ADR numbers and round
numbers); the user's email. None of it was used as evidence; nothing below rests on it. The hunk files' own
header comments state a landing line and nearest heading, which I verified against the body (see §1).

## 1. Hunk headers vs bodies

- hunk-02: header says lines 1441-1443, heading 1406 "9.6 Recovery scan". `sed -n 1441,1443p` gives
  "candidate it settled on and how many it rejected, or, where no / candidate survived re-verification, that
  none did and how many it / rejected. `[R-LIF-06]`" — matches the "+" lines. Heading at 1406 confirmed. OK.
- hunk-10: header says 3479-3482, heading 3423 "20.5 Compaction". Lines 3479-3482: "floor. Neither obligation
  has a witness in the output alone, save / that where the output carries no later-minor feature the compactor
  / does not implement, its stored version_minor is checkable against / the floor `[R-CNT-26]` states." OK.
- hunk-11: header says 3491-3492. Lines 3491-3492: "extent slots, regenerates each tile-index region any of
  whose stored / extents the output relocates (entry". OK.
No header/body discrepancy in any of the three.

## 2. Sweeps (verbatim) and controls

Line-oriented greps (`grep -n`), hit counts:
- `settled` → 1 (1441). `how many` → 6 (1354, 1441, 1442, 3417, 4589, 4610, 4665); only 1441-1442 are the
  report clause. `candidate` → 4 (1412, 1439, 1441, 1442), all in §9.6.
- `regenerat` → 6 (3491, 3496, 3502, 3510, 3537, 3540). `relocated` → 7 (301, 3386, 3486, 3536, 3540, 3561).
- `R-WRT-07` → 5 (677, 3147, 3522, 3541, 4229). `R-LIF-08` → 4. `R-LIF-06` → 4 (1443, 3551, 3858, 4118).
- `R-CNT-26` → 6 (890, 3288, 3478, 3482, 4622, 4661). None between 3569 and 4051 (§21) — so no register row
  cites it. Control: the same grep found the row-free citations, and `grep -n 'R-LIF-06'` found the §21.6 row
  at 3858, proving register rows are reachable by this pattern.
- `version_minor` → 14 hits; none inside §21.7 (3893-3953); one §21.6 row at 3852 citing `[R-CNT-07]`.
- `witness` → 11 hits; the §20.5 hit is only 3479.
- `recovery\|Recovery` outside 1400-1449 → 60, 682, 831, 1362, 1368, 1369, 3104, 3105, 3550, 3858, 4116, 4117,
  4119. All read; none restates the report obligation.
- CONTROL that failed as expected: `grep -n 'the candidate it'` → 0, although the phrase is present at
  1441-1442 across the wrap ("the\ncandidate"). This proves line-oriented grep cannot be trusted for phrases.

Whitespace-normalised sweep (`tr '\n' ' ' | sed 's/> / /g; s/  */ /g' | grep -o -F`), counts:
- "the candidate it settled on" 1 (control — present, found)
- "the candidate it" 1 (the failed line-grep control, now found)
- "how many it rejected" 2 (both in the repaired sentence)
- "none did" 1; "no candidate survived" 1
- "regenerates each" 1; "any of whose stored extents" 1; "entry offsets new" 1
- "relocated tile-index region" 1 (3536, Example); "relocated index region" 1 (3540, Example); "each relocated" 2
  (3540 Example; 3561 `[R-WRT-09]` "each relocated extent's checksum"); "the one kind this operation
  regenerates" 1 (3537, Example)
- "has a witness" 1; "no witness" 1 (3262, §20.3 step, unrelated); "checkable against" 1;
  "feature the compactor does not implement" 1; "version_minor is checkable" 1.

## 3. Hunk 02 — §9.6 recovery report

### Rule adopted
A tool running §9.6's probe with whole-file re-verification (a recovery tool, or a verifier using the probe
as diagnosis) that continues past a candidate failing re-verification MUST report either the surviving
candidate plus the number rejected, or — when no candidate survives — that none survived plus the number
rejected.

### The two kinds of tool and where each stops
The paragraph opens "Recovery tools and verifiers — never conforming readers on the default path". Stopping
places it states: "The nearest-to-end valid candidate is the last committed state; truncating to it recovers
the file" (the default probe stops at the first survivor); "A recovery tool enumerating a file's commit states
continues the same probe to offset 0; coverage verification does not (§9.7, `[R-LIF-08]`)"; "For a verifier
the probe is diagnosis — which commit state is recoverable — not a finding about the file it was given."
§9.7 confirms coverage verification "walks the live state only" and its Note says "Nothing here enumerates
prior commits."
- Recovering tool / diagnosing verifier: "the candidate it settled on" = the nearest-to-end gate-passing
  candidate whose whole-file re-verification passes. The new branch arises when every candidate down to
  offset 0 fails re-verification, or there is no gate-passing candidate at all. Since "the tool continues the
  probe past it" has no bound but the probe's start ("probe backward"), such a tool does reach offset 0 with
  no survivor, so the branch is reachable.
- Enumerating recovery tool: continues to offset 0 regardless and produces the set of survivors; "the
  candidate it settled on" is singular and fits it awkwardly (pre-existing — see rejected candidates). The new
  branch arises for it as the empty enumeration.

### Check 1 (tense/quantifier/actor)
Tense: the probe reads the physical file as handed over; the repaired clause is in that same present. Set:
"no candidate survived" ranges over every candidate probed to offset 0; "how many it rejected" is a count
(see check 6). Actor: "the tool" — the sentence's subject since "so the tool continues the probe past it",
ranging over both kinds the paragraph opened with. The repair IS the normative rule (`[R-LIF-06]`).

### Check 2 (citations)
The changed text carries only the label `[R-LIF-06]`, which is this paragraph's own. In the surrounding
untouched paragraph I opened: `[R-LIF-08]` (§9.7, walks live state only — pass); `[R-CNT-06]` and rows F8,
F14, F17 at 3676/3681/3684 (magic, trailer CRC, length cross-check — pass); §8 (whole-file verification —
pass); `[R-SLB-05]`/`[R-CNT-21]` (placement freedom / slack — pass).

### Check 3 (label)
The sentence sits in unmarked prose, not in any ">" block; label test: no Note/Example/Rationale. Normative.
Restatements: §21.6 row at 3858 restates only the re-verification caution; §22.3 at 4116-4121 likewise; §1 at
60 and §20.3 step 1 at 3104 mention recovery without the report. Nothing restates the report obligation, so
nothing was left unswept.

### Check 4 (contradiction in passage)
Read 1406-1449 whole. Candidate tension: line 1411-1413 "The nearest-to-end valid candidate is the last
committed state; truncating to it recovers the file" asserts a survivor whenever a valid candidate exists,
whereas the repaired branch admits none surviving. Judged pre-existing and reconcilable: the paragraph
explicitly supersedes the naive rule with "Two cautions are normative for tools" and the mimic caution, and
"valid candidate" is the pre-caution term. No MUST/MAY collision. Rejected as a finding (see §6).

### Check 5 (exhaustive claims)
"no candidate survived" / "none did": a closed dichotomy (some survivor / no survivor) — exhaustive by
construction. "how many it rejected": a count, undefined — check 6.

### Check 6 (structure: the report)
Quantities the probe produces: (a) matches — 64-aligned offsets carrying the trailer magic; (b) gate failures
— matches whose trailer CRC fails or whose committed_file_length ≠ o + 64; (c) valid candidates — matches
passing both gates; (d) rejections — candidates whose whole-file re-verification (§8) fails; (e) the survivor
— the nearest-to-end candidate passing re-verification (or, for an enumerator, all survivors). The report
names (e) and a count called "how many it rejected". "rejected" is not defined. The word "candidate" is used
two ways in the paragraph: "valid candidate" at 1412 implies a candidate can be invalid (i.e. candidate = any
match), while "a candidate whose whole-file re-verification fails" at 1439 reads candidate = gate-passing
match. So "how many it rejected" admits: count of (d) only; or count of (b) + (d). The repair restated the
count a second time without fixing it. → FINDING C-01. Not byte-level: a report number, not bytes on disk
or an accept/reject verdict; the file is unchanged either way.

### Check 7 (analogy)
No "exactly as / the same way / on the model" in the repaired text. Nothing to compare.

### Check 8 (anaphors)
Inserted text's own back-references: "it" (rejected) → the tool; "none did" → survived re-verification;
"re-verification" → "the whole-file re-verification below" at 1420 / caution at 1424-1426 — same referent
before and after. Forward to end of §9.6: the next paragraph (`[R-LIF-07]`, 1445-1449) contains "the
consequence of not doing so" (→ not emitting checkpoints, own sentence) and "recoverable only by scanning back
across its entire length" (→ the torn append) — neither touches the insertion. Unaffected.

## 4. Hunk 10 — §20.5 version_minor witness

### Rule adopted
The compactor's two version_minor obligations cannot be checked from the output alone, except that when the
output carries no later-minor feature the compactor does not implement, the stored version_minor can be
checked against `[R-CNT-26]`'s floor.

### The two obligations
The paragraph states three things about the trailer: (0) "The output trailer MUST copy the input's unknown
ignore-lane flag bits forward" (`[R-CNT-08]`); (1) where the output carries a later-minor feature the
compactor does not implement, "the output's version_minor SHOULD be at least the input's"; (2) "Otherwise
version_minor follows `[R-CNT-26]`'s floor." "Neither obligation" is the pair (1)/(2) by proximity and by
subject (version_minor). (0) is also unwitnessed from the output alone, so "neither" is not wrong, merely
scoped by the sentence before it. Not a finding.

### `[R-CNT-26]` quoted (line 886-890)
"A writer SHOULD emit the lowest version_minor that defines every feature present in the file — for a file
expressible under this text, 0 — and an appender the maximum of that floor and the prior trailer's minor; a
higher minor than needed costs readers nothing (minors never gate) but misstates the file's feature floor to
tooling."
The floor: the lowest minor that defines every feature present; 0 for a file with no later-minor feature.

### Check 1 — the actor (the whole question)
Who checks, from what? A witness is what a checker (verifier/tooling) finds in the output. The qualifier's
condition — "carries no later-minor feature the compactor does not implement" — is a fact about the
compactor's implementation set, which the output records nowhere (§21.7's own point: no field counts commits
or names the producer). Cases:
(a) output carries no later-minor feature at all (no ignore-lane bit, no unrecognized `tarn.` key — the two
    conforming vehicles the paragraph names): any checker under this text sees this, floor = 0, stored minor
    checkable. Condition holds. Sentence true.
(b) output carries a minor-N feature the compactor implements (an ignore-lane bit minor N defined): condition
    holds → sentence says checkable. A checker under this text sees a bit it cannot date (§6.3: "such bits are
    defined by later minor versions") and cannot compute the floor. Only a checker implementing minor ≥ N can.
(c) output carries a minor-N feature the compactor does not implement: condition fails → sentence says no
    witness. But a checker implementing minor N sees the feature, knows the floor is ≥ N, and a stored minor
    < N is the understatement the paragraph itself names — a witness for that checker.
So checkability turns on the checker's knowledge relative to the output's features; the compactor's
implementation set is neither visible in the output nor the right variable. Under reading "checkable by this
text's verifier", the stated set is too wide (case b); under "checkable by some tool", too narrow (case c).
→ FINDING C-02. Not byte-level: the sentence describes witnessability of SHOULD-level obligations; the
compactor's obligations (1)/(2) are unchanged by either reading, and `[R-CNF-12]` makes a SHOULD deviation
no violation, so no accept/reject verdict and no emittable byte moves.

### Check 2 (citations)
`[R-CNT-26]` "the floor `[R-CNT-26]` states" — it states one (quoted above). PASS. The dropped "(§21.7)":
§21.7 (3893-3953) mentions neither version_minor nor `[R-CNT-26]`; it defines "unwitnessed" over "any check
this specification obliges a reader or a verifier to perform". Since `[R-CNT-26]` is a SHOULD and `[R-CNF-12]`
says "A verifier owes no search for one", no obliged check exists in any case, so under §21.7's definition
the obligations are unwitnessed even in the qualifier's case — the repair's "checkable" is the informal
sense, and dropping the citation is consistent with that. Untouched neighbours: "the mirror of the
overstatement `[R-CNT-26]` names" — `[R-CNT-26]` names "misstates the file's feature floor" for a higher
minor — PASS.

### Check 3 (label)
Unmarked prose; normative. Restatements found: Appendix G item 8 (4622-4629, non-normative): "The
version_minor floor binds a compactor too, save where its output carries a feature it does not implement,
when §20.5's floor governs instead" — consistent with (1)/(2); it says nothing about witnesses. §21.6 row
3852 ("version_minor is higher than this text defines | Accepted; minors never gate | `[R-CNT-07]`") — a
not-a-violation row citing `[R-CNT-07]`, consistent with the claim that a wrong minor is no violation.

### Register search for `[R-CNT-26]`
Zero rows in §21.2-§21.7 cite it (grep above). What bears on the claim is the §21.6 `[R-CNT-07]` row: a high
minor is accepted, so no reader/verifier verdict turns on version_minor — consistent with "no witness".

### Check 4 (contradiction)
Read 3423-3569 whole. "Otherwise version_minor follows `[R-CNT-26]`'s floor": `[R-CNT-26]` gives a writer's
floor and an appender's max; §20.5 puts a compactor on the creation path, so the writer's floor applies —
consistent. No MUST/MAY collision around the sentence. Appendix G's closing paragraph (4661: "item 8's
creator's rule, not a compactor's (§20.5)") sits against item 8's "binds a compactor too" — an internal
Appendix G tension, non-normative, outside this hunk, pre-existing; noted, not filed.

### Check 5 (exhaustive claims)
"Neither" — two, correct for the pair. "no later-minor feature" — the class is defined by the untouched
sentence before it ("a carried ignore-lane bit (§6.3) or an unrecognized `tarn.` key in a record it never
decoded (§18.3)"). "checkable against the floor" — a claim of possibility; falsified for case (b) above.

### Check 6 (structure: the output trailer's version/flags)
version_major — fixed at 1 by §6.2's table and `[R-CNT-24]`; version_minor — this paragraph; flags —
incompat lane 0 / ignore lane copied (`[R-CNT-08]`). All three governed. No unconstrained sibling.

### Check 7 (analogy)
No analogy in the repaired text; "the floor `[R-CNT-26]` states" is a citation. Verbs side by side anyway:
`[R-CNT-26]` "SHOULD emit the lowest version_minor that defines every feature present in the file"; repair
"its stored version_minor is checkable against the floor" — same quantity. PASS.

### Check 8 (anaphors)
Inserted: "the output" (the compactor's output, §20.5 first sentence); "the compactor"; "its stored
version_minor" → the output's; "Neither obligation" → (1)/(2), unchanged. Forward: "A compactor MUST refuse
… such a type can define references … so its bytes" — "such a type"/"its" resolve within their sentence.
Unaffected.

## 5. Hunk 11 — §20.5 regeneration keying

### Rule adopted
A compactor regenerates a layer's tile-index region exactly when the output relocates at least one stored
extent that region's entries address. A region none of whose stored extents relocates is not regenerated:
it is carried forward under §20.4 byte-identically, its extent slot re-pointed if the region itself moved.

### The separated case
Region R of layer L is placed at a new offset in the output, but every stored tile of L keeps its offset.
Old keying: R "relocated" → regenerated; but every entry's stored extent "now lies" where it did, so every
entry is re-emitted unchanged, segment CRCs over unchanged entries are unchanged, crc_of_crc_array unchanged.
New keying: R not regenerated; copied verbatim; slot re-pointed. Bytes of R identical under both.
The converse case (R stays at its offset, some stored extents move): new keying regenerates; old keying's
wording did not, which would leave stale offsets in a live region — a nonconforming output that `[R-CNF-05]`
and `[R-WRT-07]`'s "reference arrays MUST equal the live generation's bit for bit" already barred. So the
re-keying changes no emittable byte set; it makes the prose name the right trigger.

### The other sentences about the region
- Unchanged-list (3488-3496): "every stored tile's bytes verbatim — each index entry's crc is unchanged — and
  every retained record per §20.4, except that relocation re-points extent slots, regenerates each tile-index
  region any of whose stored extents the output relocates (entry offsets new; entry lengths, entry crcs, and
  sentinel entries unchanged; segment CRCs recomputed over the entries as re-emitted), and updates the
  layer-record fields covering a regenerated region (crc_of_crc_array)." Consistent with the new key. The
  gloss "entry offsets new" overstates for a regenerated region only some of whose extents moved, but the
  defining paragraph governs the gloss (below).
- Defining paragraph (3498-3510): "Regenerating a region means classifying every entry in it: a sentinel is
  re-emitted unchanged, and every other entry is re-pointed to where its stored extent now lies." Neutral to
  the keying; consistent.
- Example block (3525-3554, labelled **Example** → non-normative by `[R-CNF-01]`): "as does every record
  extent but a relocated tile-index region — itself a record extent (§5.2), and the one kind this operation
  regenerates rather than copies, since its entries carry the offsets that moved" and "extent slots are
  re-pointed and each relocated index region is regenerated — the ′ marks (`[R-WRT-07]`)". Both key
  regeneration on the region's own relocation — the wording the repair removed from the rule. Under the new
  rule a relocated region none of whose extents moved is copied, not regenerated (so it does survive
  byte-for-byte, against "every record extent but a relocated tile-index region"), and a non-relocated region
  whose extents moved is regenerated (which the Example does not say). The Example's own reason — "since its
  entries carry the offsets that moved" — states the new criterion, so its key and its reason now disagree.
  → FINDING C-03. Not byte-level: the block is labelled Example (non-normative, rule governs), and the case
  the keyings separate produces identical bytes.

### Check 1
Tense: "the output relocates" — the compactor's output against the input's live state, the only state a
compactor carries (§20.5 first sentence). Set: "each tile-index region" universal over regions; "any of whose
stored extents" existential over the region's stored extents — per §15.3 those of well-formed non-sentinel
entries (a structural reject-tile entry has none; a crc-failing entry keeps its extent). Actor: the compactor.
The repair IS the normative rule (`[R-WRT-07]`'s paragraph).

### Check 2
The changed text carries no identifier or section number. Its sentence cites §5.2 (record extent / placement
classes — pass), `[R-SLB-01]`/`[R-SLB-03]` (alignment / slab invariants — pass), §20.4 (retained records —
pass). Example cites §5.2 ("a record extent (the bytes any record's extent slot references…)" — pass) and
`[R-WRT-07]` — pass.

### Check 3
Unmarked prose; normative. Restatements: the Example (C-03); §23.2 `[R-PRV-04]` at 4229 "`[R-WRT-07]`
preserves every stored tile's bytes and every index entry's crc bit for bit" — consistent; §5.1 Note 677 and
§20.3 step 3147 "relocating a live index region is compaction's operation" — about relocation, which
compaction still does; consistent. Appendix H updater checklist — no regeneration statement.

### Check 4
Read 3423-3569 whole. `[R-WRT-09]` (3556-3562) "each relocated extent's checksum, including every stored
tile's entry crc" — verification depth keyed on relocated extents, consistent with the new key. Structural
reject-tile paragraph: a region not regenerated is not classified, so a structural reject-tile entry in it is
not "met" and travels forward under `[R-WRT-01]`; the paragraph acknowledges this ("bounds how far a
compactor goes looking"). The set of not-met regions changed (old: non-relocated regions; new: regions with
no relocated extent) but both are placement-dependent and both outputs are nonconforming-from-nonconforming,
which `[R-CNF-05]` bars conforming writers from producing from a conforming input. No contradiction.

### Check 5
"each" (universal), "any of whose" (existential) — both carry. A region with only sentinels has no stored
extents and is never regenerated — its bytes are placement-independent anyway. Correct.

### Check 6 (structure: what relocation touches)
Extent slots (re-pointed); tile-index region entries (offset re-pointed; length, crc, sentinel unchanged);
segment CRC array (recomputed); layer record crc_of_crc_array (updated); entry_count and extent_length
(unchanged — same entries, `[R-CNT-17]`); the directory (re-emitted whole on the creation path); implemented
MU = 1 non-layer types ("relocates whatever that registration defines, on the same terms as the tile index").
No quantity left ungoverned.

### Check 7
"on the same terms as the tile index" (3520, untouched) now points at the re-keyed rule. Verbs: tile index —
"regenerates each tile-index region any of whose stored extents the output relocates"; MU = 1 type —
"relocates whatever that registration defines". Both range over references to relocated extents; the new key
is the more general principle, so the analogy is sounder after the repair than before. PASS.

### Check 8
Inserted text's back-refs: "the output" → the compactor's output; "whose" → the region. Forward: "a
regenerated region" (3496) → regenerated under the new key — intended; "Regenerating a region means" (3498)
— term definition; "regenerating the region cannot proceed without meeting it" (3502) — same; Example
"a relocated tile-index region … the one kind this operation regenerates" and "each relocated index region
is regenerated" → still the old key (C-03). `[R-WRT-09]` "each relocated extent's checksum" → extents, not
regions; unaffected.

## 6. Rejected candidates
1. §9.6 line 1411-1413 "The nearest-to-end valid candidate is the last committed state" vs the new no-survivor
   branch. Dropped: the paragraph's "Two cautions are normative for tools" and the mimic caution explicitly
   supersede the naive statement, and the tension predates the repair; no implementer following the MUST would
   fork.
2. §9.6 "the candidate it settled on" for an enumerating recovery tool (singular vs a set). Dropped: pre-existing
   and the enumerator's output is the enumeration itself; not created or worsened by the repair.
3. Hunk 10 "Neither obligation" with three obligations in the paragraph. Dropped: the sentence immediately
   before names version_minor, so the pair is unambiguous by subject.
4. Hunk 10: dropping "(§21.7)" leaves "witness" undefined locally. Dropped: §21.7's definition would make the
   qualifier's own "checkable" case unwitnessed too (no obliged check), so keeping the citation would have
   contradicted the qualifier; the informal sense is the only consistent one.
5. Appendix G 4661 "not a compactor's" vs item 8 "binds a compactor too". Dropped: non-normative, outside all
   three hunks, pre-existing.
6. Hunk 11 gloss "entry offsets new" overstating for partially-relocated regions. Dropped: the defining
   paragraph ("re-pointed to where its stored extent now lies") governs the gloss; same overstatement existed
   under the old key.
7. Hunk 11: structural reject-tile detection now hinges on whether any stored extent relocated (a placement
   choice). Dropped: the same placement-dependence existed under the old key; §20.5 says so ("bounds how far a
   compactor goes looking"); the input is nonconforming, so the emittable set of conforming files is unmoved.

## 7. Derived numbers
- Hunk landing lines: 1441-1443, 3479-3482, 3491-3492 — each confirmed by `sed -n` against the "+" lines.
- Register rows citing `[R-CNT-26]`: 0 (of 6 citations file-wide, none in 3569-4051). Rows citing
  `[R-LIF-06]`: 1 (§21.6, 3858). Rows citing `[R-WRT-07]`: 0 (5 citations, none in §21).
- Obligations about the trailer in hunk 10's paragraph: 3 (flags copy; SHOULD ≥ input's; floor) vs the
  sentence's "Neither" = 2.
- Probe quantities enumerated for hunk 02: 5 classes (matches, gate failures, valid candidates, rejections,
  survivor); the report names 2 (survivor-or-none, rejected count).
- Occurrences of the old region-relocation key after the repair: 2 (3536-3537, 3540), both in the Example.
- No CRC or offset recomputation was called for by these hunks.

## 8. Findings
C-01 (hunk 02, UNCONSTRAINED_SIBLING, not byte-level) — "how many it rejected" counts an undefined set.
C-02 (hunk 10, TENSE_QUANTIFIER/actor, not byte-level) — checkability keyed to the compactor's implementation
     set, which no checker of the output holds.
C-03 (hunk 11, UNSWEPT_RESTATEMENT, not byte-level) — the Example still keys regeneration on region relocation.
