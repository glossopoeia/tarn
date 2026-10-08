# Diff-adversary transcript — TARN fidelity round

## Access and method

Read only the two permitted files:
- A: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4981 lines)
- B: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4847 lines)

No other path was opened, and no directory listing was run against the project (only
`mkdir -p` of my own scratch/out dirs, and `ls` of those same dirs I created). All commands
below ran with cwd `/Users/robertkleffner/Documents/GitHub/tarn-first-draft` but only ever
read the two files above via `sed`, `grep`, `wc`, `diff`, and a short Python script.

Disclosure of context placed before I began: the harness's system reminders included a
"computed task" block (my charter) and an unrelated "relayed user request" line
("Set the constant to claude-sonnet-5, preflight with --models, then launch") that does not
describe anything in my charter; I am treating my charter (diff-adversary over A/B) as the
operative task, since that is what was actually handed to me to execute, and am not
repeating or acting on the unrelated line. No other injected material appeared in tool
output.

Both files are hard-wrapped (~72-col prose, "> " blockquote prefix on Notes). All
comparisons below normalize whitespace (`sed 's/[[:space:]]\+/ /g'`) before diffing or
computing similarity, so line-wrap differences never register as content differences.

Step 1 — structural map: extracted every `####`-level subsection from each file into
`secs_a/NNN_<slug>.txt` / `secs_b/NNN_<slug>.txt` (Python script, scratch dir only), then
diffed the heading lists. Finding: B has one fewer subsection than A. `diff` of the heading
lists showed `_3_3_Container_and_array_model.txt` present only in A (and sections 2 and 3
swapped in overall document order — A order 1,2,3,4...; B order 1,3,2,4..., both reaching the
same section numbers with the same headings otherwise).

Step 2 — similarity ranking: for every heading common to both editions, normalized
whitespace and computed a `difflib.SequenceMatcher` ratio. Sections 9 through 24 (and most of
Appendices) came back at ratio 1.0000 — byte-identical after whitespace normalization — i.e.
not yet touched by the "readable" rewrite. All the differing content is concentrated in
Part 0 (§1-§4), Part I §5-§8, and one restatement inside §21.6. This matches the project's
own section-by-section process (confirmed independently from git log commit subjects visible
in this session's own context, not read from any excluded file).

Step 3 — for every section below ratio ~0.97, read both versions in full and traced every
surface difference to ground: either (a) a cross-reference to an unchanged section that
states the same fact, in which case the apparent loss is closed as EQUIVALENT, or (b) a
genuine absence with no restatement anywhere, logged as a finding.

## Constructions carried to bytes (charter-required: at least six)

For each, I built or attempted to build a concrete byte-level scenario and checked whether A
and B's rules disagree on the resulting bytes or verdict. All six closed as REPORTER_ERROR /
no-divergence; each is logged with the exact sentence that closes it.

1. **Record with MU=0, PE=1, of a type the updater does not implement, in a layer's
   sub-records.** Charter theme: updater preservation. Checked §20.4's governing table in
   both editions — `diff` of the two extracted section files is empty (byte-identical,
   including the `[R-WRT-05]`/`[R-WRT-08]` text and the "MU = 0, PE = 1 → Retain
   byte-identical, extent content unmodified" row). An appender's required output bytes for
   this record are identical under both editions. **Closed**: §20.4 full text, `diff -q`
   confirmed zero bytes of difference between `secs_a/.../20_4...` and `secs_b/.../20_4...`.

2. **User-metadata document under an experimental-range encoding (≥0x80), verifier
   certification.** Charter theme: register governing rule for a disagreeing row. A's §2.3
   states explicitly the document "is not such a ground [for cannot-establish]: no content
   rule attaches there, so nothing is left unchecked, and certification is unaffected
   (`[R-MTA-10]`)." B's §2.3 drops this explicit carve-out and instead says "(§21.6 names the
   grounds)." Traced to §21.6's existing table row (present, byte-identical, in both editions):
   "A user-metadata record declares an experimental-range (≥ 0x80) document encoding | Ignored
   (ignore-record); the file is conforming ... so a verifier certifies, reporting the record it
   ignored." Same verdict, same row, both editions. **Closed**: §21.6 table row, identical text
   confirmed by grep across both files.

3. **Pre-trailer gap longer than the commit protocol's step-5 pad (slack length violating no
   byte count, since `[R-CNT-05]` only bounds it through the commit protocol, not as an
   independent cap).** Charter theme: carve-outs ("a longer gap is conforming ... no
   conforming commit produces one"). §6.2 states this sentence almost word-for-word in both
   editions (A: "a longer gap is conforming, and no conforming commit produces one"; B: "a
   longer gap is conforming, though no conforming commit produces one"). Same verdict, same
   requirement ID `[R-CNT-05]`. **Closed**: §6.2, same sentence present in both, diff shows
   wording-only changes.

4. **A tile-index entry classified reject-tile on a structural ground (`[R-IDX-03]`) inside an
   otherwise-complete coverage walk.** Charter theme: coverage partition / byte coverage.
   A's §5.2 states in-line that this case "leaves it complete too... and the bytes of the file
   it nominally addresses fall to slack." B's §5.2 omits this sentence and instead says "Where
   the walk of §9.7 does not complete, the verifier MUST report the total as partial; §9.7 says
   when that is." §9.7 itself is byte-identical between editions and contains, verbatim in both:
   "An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground does not make the walk
   incomplete: the walk passes over it, and the bytes of the file it nominally addresses fall to
   slack where no other claimant claims them (§15.3)." Same verifier output (partial-total
   status and byte-to-slack assignment) under both editions for any file exhibiting this
   condition. **Closed**: §9.7, byte-identical in both (confirmed by whole-section diff,
   zero output).

5. **Two layer records in the live directory with byte-identical raw name bytes (duplicate
   layer name).** Charter theme: definitions / field taxonomy, carve-outs on scope. A's §4.7
   Note states "A name is structural: a duplicate is a validity error at file or layer scope
   (`[R-ENC-15]`, F4, L9)"; B's corresponding Note drops this sentence entirely. Traced to the
   register: row F4 ("Two layer records in the live directory carry byte-identical name fields
   ... comparison is raw bytes, no normalization ... reader | open | `[R-ENC-15]`") and row L9
   are present, byte-identical, in both editions' §21.2/§21.3 tables (confirmed by grep: both
   files have identical F4 and L9 lines). Same scope (file), same detector, same requirement ID,
   both editions. **Closed**: register rows F4 and L9, identical text in both files.

6. **A dimension extent grown by an append commit (so the set of addressed tiles differs
   between an earlier and a later generation of the same layer).** Charter theme: definitions.
   A's §3.1 glossary defines "addressed" tile unconditionally ("every tile of a layer is
   *addressed*"); B's §3.1 redefines it generation-relative ("a tile is *addressed* in a
   generation if that generation's tile index has an entry for it: the tiles of the layer's
   grid under the geometry that generation declares"). This is a real wording difference in
   the glossary. But no `[R-xxx]` identifier attaches to this glossary bullet in either edition,
   and the operative rules that actually decide which tiles exist and are indexed for a given
   generation live in §11.2 (Grid arithmetic), §15 (Tile Index) and §20.3 step on growth — all
   three sections are byte-identical between editions (confirmed by whole-section diff,
   zero output on §11.2 and §15; §20.3 is in the 1.0000-ratio list from step 2 above). A
   verifier or reader built from either edition's normative rules computes the identical
   addressed-tile set for any concrete file and any concrete generation. **Closed**: §11.2,
   §15, §20.3 — all byte-identical between editions; the divergence is confined to
   non-normative glossary prose.

## Findings carried through (no byte-level divergence confirmed)

Despite the above, two structural omissions recur across the document and are reported as
observations for the maintainer, since they are complete deletions with no restatement
anywhere (verified by targeted grep for their distinguishing phrases against the full text of
both files), even though neither carries a requirement ID or changes any register row:

- **adv-01**: B drops §3.3 "Container and array model" entirely (A's whole subsection is a
  single Note asserting Part I/Part II independence and calling it "load-bearing for the
  updater rules of §7 and §20"). Grep for "independent of Part", "load-bearing", and "cannot
  decode" confirms this content and its distinguishing phrasing appear nowhere in B.
- **adv-02**: B's §1 Introduction drops A's "Reading this document" roadmap paragraph (the
  one stating "Part I alone yields a container reader ... without decoding a sample;
  returning sample values needs Part II as well, since §19.3's layer validation resolves into
  Part II's value sets and geometry rules at every step"). Grep for "without decoding", "Part I
  (§5", "yields a container reader" confirms zero hits in B. This is the same substantive idea
  as adv-01, stated a second time in A and dropped a second time in B.

Both are explanatory/rationale text (A itself marks §3.3 as a `> **Note.**` block, i.e.
already non-normative under `[R-CNF-01]`), and neither assertion is relied on by any `[R-xxx]`
rule elsewhere in either edition — the actual permission for an appender/rewriter to carry
forward a layer it cannot decode is established directly by §20's writer-tier and
re-emission rules (§20.1, §20.4), which are byte-identical between editions. So I do not
classify either as a byte-level LOSS; they are reported as OBSERVATION only.

## Other candidates opened and closed along the way

- §2.4 Outcome classes: B drops the sentence "The same vocabulary is used for defined
  conditions that are not violations ... **preserve-verbatim** names an updater obligation,
  orthogonal to reader outcomes: a record a reader ignores can still be one an updater
  preserves." Checked against §20.4's table (byte-identical in both editions), which already
  fully and independently specifies updater obligations by MU/PE bit regardless of the
  reader's outcome for the same record (e.g. MU=0/PE=1 is ignore-record for a reader and
  retain-byte-identical for an updater, in both editions). No implementation built from B
  alone would compute a different required byte sequence. Closed as EQUIVALENT.
- §2.3 Conforming TARN file bullet: B drops A's enumerated list of the four concrete
  "conduct, not output" writer obligations (the ignore-lane-bit rule, the pre-trailer-pad
  rule, and the §20.3 step 4 bar). Checked each cited site (§6.3 line ~902/768, §6.2 "a
  longer gap is conforming", §20.3 "Steps 4 and 6 bind a writer's **conduct**... as
  `[R-CNF-02]` says of every conduct...") and found each site independently and identically
  (byte-for-byte) states the same conduct-only classification in both editions. Closed as
  EQUIVALENT (summary list relocated to each rule's home site, not lost).
- §21.6/§8.1/§4.5: the git history visible in this session's own context implies an earlier
  readable-ification of §4.5 cut the checksum-coverage exceptions, later restored under §8.1.
  Verified directly: A's §4.5 contains the full exceptions-and-interior-checksum-fields
  paragraph; B's §4.5 trims it to a single cross-reference ("§8"); B's §8.1 contains an
  expanded version of the same paragraph (three-exceptions enumeration plus the interior-
  checksum-fields clarification), matching A's content in substance. Closed as EQUIVALENT
  (content relocated from §4.5 to §8.1 in B, not lost).
- §7.1/§7.3: B moves the entire "metadata compression / user-metadata quarantine" paragraph
  from §7.1 (A's location) into §7.3 (B's location), with paraphrased but substantively
  identical sentences (verified clause-by-clause: encoding validity, quarantine scope
  override of `[R-CNF-08]`, the resource-decline carve-out citing `[R-MTA-09]`/`[R-ERR-04]`,
  and the "verifier certifies" result for experimental-range encodings). Closed as EQUIVALENT
  (relocated, not lost).

## Confidence note

Sections 9-24 and the appendices were not yet touched by the readable rewrite (ratio 1.0000,
i.e. byte-identical after whitespace normalization) at the time of this round, so no
adversarial search was needed there — any diff-adversary finding in that range would be a
REPORTER_ERROR by construction. I did not exhaustively re-verify every single sentence in
every one of the ~30 sections at ratio 1.0000; I relied on the automated whitespace-normalized
equality check (Python `difflib` ratio == 1.0 after `\s+` collapse) as proof of byte-for-byte
content identity for those sections, which is a stronger check than a manual read would add.
