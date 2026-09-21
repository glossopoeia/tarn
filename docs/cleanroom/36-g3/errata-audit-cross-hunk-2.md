# Second cross-hunk auditor — working transcript

## 0. Disclosure

Before opening any file, my context already contained, from the harness/host
(not from the user): a `CLAUDE.md` pointer to `AGENTS.md`, a `MEMORY.md` file
with ~16 bullet titles about "TARN" rounds (e.g. "TARN harness spec path",
"TARN repair prose vs rules", "TARN closed-list exceptions compose", "TARN
walk stall and retry", etc.), a git status block naming five recent commit
subjects (including "Cleanroom round 36: charter, re-cut over the
maintainer's rulings", "ADR-0129's erratum E3...", "ADR-0130's erratum
decision E2/E1 confirmed"), and standard environment/tooling boilerplate.
None of this is part of the specification and none of it is evidence about
the specification. Per the access rule I am disclosing that it appeared and
am not treating any of it as informative about which hunks are defective,
what "erratum E1/E2/E3" said, or what prior rounds concluded. In particular
I did not read AGENTS.md, docs/, PLAN.md, OPEN-QUESTIONS.md,
conformance/, spec/registry.json, or git history/log/diff, and did not
consult the memory files' linked note bodies (only their index titles were
present in context; I did not open any of them).

Paths: both paths given in the brief resolved exactly as stated —
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4980 lines) and
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-audit2/case/`
containing `hunk-01.diff` through `hunk-26.diff` plus `full.diff` (not read).
No discrepancy to report there.

## 1. What I read and ran

- Read `spec/tarn.md` in full (offsets 1–4980, in ~5 chunks) — I paid
  particular attention to §2.3–2.5, §3.3, §5.2, §6.1–6.4, §7.1–7.4, §8,
  §9.1–9.3, §10.2–10.3, §15, §19.1–19.4, §20.1–20.5, §21.1–21.7, §23.1,
  Appendix C, Appendix G, Appendix H — i.e., every section any hunk lands in
  or cites, plus the register rows and appendix checklists that restate
  those sections.
- Read all 26 hunk files in `case/` in one batch (via a single large Bash
  cat, then re-read the saved tool-output file with the Read tool to get
  line numbers). Did not read `full.diff` and did not read any other
  auditor's hunk subset; did not `ls` the parent `r36-audit2/` directory
  beyond the one `case/` listing needed to enumerate my own hunk files.
- No local scripts were needed (no CRC or arithmetic recomputation was
  required by anything I found — all findings are textual/structural). I
  wrote only this transcript and the placeholder scratch note, both under
  my own scratch directory
  `r36-audit2/scratch/cross-hunk-2/`.
- Searches run (grep, `spec/tarn.md`), with hit counts and a control search
  for each zero result:
  - `grep -n "compactor" tarn.md` → 0 hits. Control: `grep -n "[Cc]ompaction" tarn.md`
    → 7 hits (lines 62, 64, 746, 3144, 3560, 3568, 3675, 4650 — 8 actually,
    recount below) confirming the search machinery works and "compaction"
    the noun survives (correctly) while "compactor" the actor-noun is fully
    swept. This is the control the brief requires before trusting a zero.
  - `grep -n "decodes everything\|decoded every byte\|whether it decode" tarn.md`
    → 0 hits. Control: `grep -n "creator\b" tarn.md` → 16 hits, all of which
    I read; none restates the old "decoded everything" test for
    creator-vs-rewriter, confirming the zero is a real sweep and not a
    failed match (the old test's own vocabulary is gone, not just
    unmatched by my phrasing).
  - `grep -n "layer's identity\|layer identity" tarn.md` → 0 hits. Control:
    `grep -n "The bar binds" tarn.md` → found the replacement sentence at
    line 3293 ("The bar binds a layer the commit keeps and nothing else"),
    confirming the old phrase is gone and its replacement is where hunk-13
    says it is.
  - `grep -n "MU = 1" tarn.md` → 21 hits, all read, to confirm no stray
    "MU = 1, PE = 1" survives tied to the layer record after hunk-08's fix.
    None found (the worked example at §7.4 is the only place that ever
    carried that value, and it is now MU=0/PE=0, matching §7.3's table).
  - `grep -n "reports the loss\|report the loss\|reporting the loss" tarn.md`
    → 3 hits (lines 1265, 3508, 3525), all "SHOULD report" — confirms
    hunks 15/19/26's sweep to advisory phrasing is complete; no leftover
    MUST-sounding "reports the loss."
  - `grep -n "dropped layer\|drops a layer\|drop the layer\|dropping a layer\|dropping the layer" tarn.md`
    → 10 hits; read each. This is what surfaced the §20.3 example-(c)
    finding below (line 3443-3446, untouched by any hunk, still omits
    sub-records from what becomes slack).
  - `grep -n "tile-index region\\b" tarn.md | grep -i "strand\|slack\|reclaim"`
    → 1 hit (line 3519, inside hunk-15's own new text). Control already
    performed by the broader "dropped layer" search above, which shows the
    example-(c) passage exists and uses different wording ("index region
    included") that this narrower grep's phrasing didn't need to catch
    separately — cross-checked by hand.

## 2. Operations, worked to bytes where charged

### Op A — commit drops a layer carrying a user-metadata sub-record with an extent

Concrete case: layer `sst` (the §7.4 worked-example layer, entry_count=4,
all sentinel) additionally carries one user-metadata sub-record (type
0x0002, registry-fixed MU=0/PE=1) whose extent holds a small JSON document.
An appender's commit drops `sst` under §20.4's PE=0 licence on the layer
record itself.

- Deciding sentence: §20.4, hunk-15's paragraph: "the drop takes the layer
  whole: a sub-record's flags govern it within a layer the updater keeps,
  so a dropped layer's sub-records and their extents go with it whatever
  their PE bits." The sub-record's own PE=1 (which would otherwise forbid
  dropping *it* while the layer is kept) is overridden once the containing
  layer itself is dropped.
- Directory after: the new directory simply omits the `sst` layer record
  (and therefore its sub-record, which lived inside the layer record's
  inline payload) entirely. No trace of either survives in the live
  directory.
- What is slack: `sst`'s 4-entry/1-segment tile-index region (84 bytes, per
  the worked example) *and* the user-metadata sub-record's extent (its
  document bytes + terminal CRC-32C) — both now unclaimed by any live
  structure, per hunk-15's explicit "strands its stored tiles, its
  tile-index region and its sub-records' extents as slack."
- What is reported: the drop is advisory-reported — "an updater that drops
  a layer SHOULD report the loss" (hunk-15) — not a MUST, and this
  specifically covers the compound loss (layer + its sub-record); no
  separate report is owed for the sub-record as such.
- Survives to the general worked example? **No** — see Finding 1 below:
  §20.3's own "Example — the three shapes a commit takes," case (c)
  (line 3443-3446, untouched by any of the 26 hunks), still enumerates only
  "a dropped layer's tiles and index region included" becoming slack, not
  its sub-records' extents. That Example is labeled Example (non-normative,
  R-CNF-01), so it cannot itself misstate a conformance predicate, but it
  is the passage most likely to be read by an implementer skimming for "what
  becomes slack when I drop a layer" and it is now visibly stale next to
  §20.4's more complete statement three pages later.
- By a rewriter instead: same layer dropped in a rewrite — §20.5's own
  disposal list (hunk-17) now says "a record dropped, a layer with its
  sub-records, its index region and stored tiles among them, is not in the
  output" — swept correctly, matching §20.4.

### Op B — commit drops a layer carrying an unimplemented type's sub-record, MU=0/PE=1 vs. MU=1

- **MU=0, PE=1** (ordinary case, e.g. an unregistered-but-implemented
  ancillary the updater doesn't specifically implement but that carries
  PE=1 by its own definition): the updater doesn't implement the type, so
  the *stored* flags are authoritative (§7.3/`[R-CNT-15]`) — if those
  stored flags read PE=1 (and MU=0, since if MU=1 were stored we'd be in
  the next case), the record is preserved unless the whole layer is
  dropped (§20.4's PE=1 row: "Retain byte-identical, extent content
  unmodified"). Dropping the *layer* is still licensed by the layer
  record's own PE=0 (a different record, a different flags pair), and per
  hunk-15 the sub-record's PE bit stops mattering once its containing
  scope is dropped. So: **droppable**, by dropping the layer.
- **MU=1** (unimplemented type, governing flags MU=1): per hunk-6's new
  Note and hunk-15's edited table row ("blocks modification of that layer,
  its drop included"), the updater cannot modify — including drop — the
  layer at all. So the layer becomes permanently un-droppable and
  effectively frozen (all its other declarations too) by *this* updater,
  though "leaving other layers editable." **Not droppable** by an updater
  that doesn't implement that sub-record's type. Confirmed again by hunk-6's
  Note: "An updater that does not implement an MU = 1 record's type never
  drops the record, alone or with the scope it governs."
- **Layer carrying both** a user-metadata sub-record (PE=1) and an
  unimplemented MU=1 sub-record: the MU=1 sub-record's block is
  controlling — the whole layer (and therefore, moot, the user-metadata
  sub-record inside it) cannot be touched or dropped by this updater. The
  PE=1 sub-record's own preservation duty never even comes into play,
  since nothing about that layer can be committed at all.
- By a rewriter meeting the same violation while regenerating the layer's
  region: if the layer's tile-index region also needs to be regenerated
  (some stored extent relocated) and the layer carries an unimplemented
  MU=1 sub-record, `[R-WRT-06]`'s own ground already forces total refusal
  of the *whole rewrite* (not just that layer) — "At either scope a
  rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground:
  such a type can define references this specification does not (§7.2),
  so its bytes cannot be safely relocated" (pre-existing text, unedited by
  my hunks, but load-bearing for reading hunk-6/hunk-15 correctly): a
  rewrite touches placement of everything it carries, so it cannot
  selectively spare one layer the way an appender's ordinary commit can.

### Op C — a creator that copies a stored tile's bytes and its entry crc from another file without decoding, tile is sound but carries a decode-only violation

Per hunk-11's R-WRT-01: "As a **creator** it undertakes nothing toward its
input, whatever it read: §20.2 binds it, it writes flags = 0, and it
answers for every byte of its output (`[R-CNF-05]`), bytes it copied from
another file included." §20.2/R-WRT-02 (the creation path) requires correct
framing (coverage classes, layout invariants, content obligations for
padding/booleans) but never requires a creator to decode a tile it merely
copies. So nothing in the writer procedure forces detection at write time.

- What it answers for: the whole output file's conformance, under R-CNF-05,
  unconditionally — including the copied tile, even though it never
  decoded it.
- Under which rule the violation is later found: whichever tile-scope row
  the specific decode-only defect is — e.g. T25 ("stored bytes are a
  malformed stream that fails to decode," detector reader, detected at
  tile use, `[R-COD-08]`), or T3/T13/T21/T22/T24 depending on the exact
  shape of the latent defect. The entry's crc matching (since it was
  copied verbatim) means the structural chain (§8.2) passes; only an
  actual decode attempt (§19.4 step 6, by the *next* reader) surfaces it.
- Register row that "records the file": the tile-scope row matching the
  specific violation (T25 is the generic "fails to decode" case). The file
  is nonconforming from the moment the creator wrote it, but the defect is
  *detected* only at first tile-use by some later reader (§19.2's
  detection-timing rule), not at write time by the creator itself, and not
  by the creator's own writer procedure. This is a genuine, deliberate
  asymmetry versus the rewriter, whose R-WRT-09 obliges crc-level (but not
  decode-level) verification before emitting a carried structure — a
  narrower duty than the creator's unconditional R-CNF-05 exposure, but a
  duty that is at least *stated as an explicit checklist* for the rewriter,
  where the creator has none. I did not find this asymmetry contradicted
  anywhere; it reads as intended (see hunk-11 discussion below), not a
  defect, but worth flagging as exactly what the charter's scenario is
  testing for.

### Op D — writer positions through §20.1's rewriter/creator split, to trailer bytes, input with an unknown ignore-lane bit set, an unimplemented-type top-level PE=1 record, and version_minor above this text

- **A compaction**: rewriter position. Output trailer: fresh file_id, flags
  = input's unknown ignore-lane bits copied forward "and set no other"
  (§20.5/`[R-WRT-06]`), version_minor "SHOULD be at least the input's" per
  the carried-feature branch since an ignore-lane bit is exactly the
  "conforming input... carried ignore-lane bit" case the text names. The
  top-level PE=1 record of an unimplemented type: retained byte-identical,
  its extent unmodified or relocated-and-repointed (never regenerated in
  content) per R-WRT-07; compaction being "carries every structure forward
  and changes nothing but placement" cannot drop it (PE=1 is never
  drop-licensed) and does not need to, since compaction doesn't decode it.
- **A rewrite that re-creates every layer** (but is still a rewrite, not a
  creation): still rewriter position by choice (§20.1's "the choice is its
  own" — nothing about re-creating every layer forces creator status).
  Trailer: same as compaction's case above — fresh file_id, ignore-lane
  bits carried forward, version_minor floor per `[R-CNT-26]`/`[R-WRT-06]`.
  The unimplemented top-level PE=1 record: still cannot be dropped (PE=1),
  must still be carried forward byte-identical even though every *layer*
  is being re-created — the record and the layers are independent
  top-level structures.
- **A tool that reads the file whole and writes a new one from decoded
  content, choosing the creator position**: writes flags = 0 (loses the
  ignore-lane bit entirely — legal, since a creator "undertakes nothing"),
  and per R-WRT-01 "answers for every byte of its output" — if it silently
  drops the unimplemented-type top-level record because it can't decode it
  and doesn't know it's PE=1-protected, that's simply a creator choosing
  not to carry it forward — legal, since creator obligations are §20.2's
  only, and §20.2 never mentions preserving unrecognized records. version_minor:
  ordinary `[R-CNT-26]` floor (lowest that defines every feature present —
  here 0, since the file it emits expresses nothing from the later minor).
  Note this is a real behavioral fork depending purely on which "position"
  the tool's author self-selects — same input bytes, same output shape
  possible either way, but the creator path has no obligation at all
  toward the ignore-lane bit or the unimplemented record, while the
  rewriter path is bound to carry both.
- **A tool that copies the tiles undecoded and leaves the unknown record
  out**: this is a hybrid that doesn't cleanly fit either position as
  stated. If it declares itself rewriter, `[R-WRT-06]` requires it to
  refuse entirely once it meets a top-level record whose type it doesn't
  implement with MU=1 — but this scenario's record is PE=1 with
  unspecified MU. If MU=0/PE=1 (ordinary unimplemented ancillary), the
  rewriter MUST retain it byte-identical (§20.4's PE=1 row) — "leaves the
  unknown record out" would then violate `[R-WRT-05]`/§20.4 for a
  rewriter. If it instead declares itself creator, dropping the record is
  legal (§20.2 imposes no such duty) — but then it also isn't entitled to
  the ignore-lane-bit carry-forward or to `[R-WRT-09]`'s bounded
  liability for the tiles it copied undecoded; per R-WRT-01 it "answers
  for every byte of its output," copied tiles included. This is not a
  document defect — §20.1's binary choice already resolves it (the tool's
  author must pick one position and take on that position's whole
  obligation set, not cherry-pick) — but it is worth stating plainly since
  the charter asks what each position "leaves undecided": choosing creator
  to avoid the MU=1 refusal leaves the implementer with *no* explicit
  verification checklist for the tiles it copies (unlike `[R-WRT-09]`),
  which is a real, if intentional, gap in guidance.

### Op E — remote reader whose transport doesn't disclose a range response's complete length

Requests counted under the current §6.4 text: 3 total — a first request
(suffix range for the last 64 bytes, needed regardless), a second, separate
request for a size probe (since the suffix response alone didn't carry a
usable F per `[R-CNT-10]`), and a third for the directory range. This
matches the newly-inserted parenthetical's own claim ("a separate size probe
then making the baseline three"). See Finding 3 below for why the *word*
"baseline" doing this double duty (2 in the opening sentence, 3 in the
parenthetical fifteen words later) is a defect in the prose even though the
arithmetic itself is right.

### Op F — a commit that adds a layer, and one that re-declares an empty layer: place every entry under one of step 4's four kinds

Step 4 (as amended by hunk-12) names four kinds: (1) entries for tiles this
commit stores or supersedes, written to new state; (2) entries for tiles
that become unstored, written sentinel; (3) entries new to this generation
— *now* explicitly including "every entry of a layer this commit adds or
re-declares" as well as tiles a grown extent/appended channel adds —
emitted per §15; (4) every other entry, byte-identical at its disk-ordinal
position.

For a **brand-new layer C** (entry_count = N_C, say all sentinel, no tile
stored): every one of its N_C entries falls under kind (3) — "every entry
of a layer this commit adds... emitted per §15" — since kind (3)'s
parenthetical now explicitly reaches this case (before hunk-12 it did not:
neither "tiles this commit stores or supersedes" (kind 1, which presumes an
existing addressed position transitioning state) nor the old kind-3
wording ("tiles a grown extent or an appended channel adds," which
presumes an *existing* layer being grown) named a wholly new layer's
entries, and kind (4)'s "byte-identical" carry-forward has no prior entry
to be identical to. This was a genuine, real gap that hunk-12 closes — I
worked this to bytes and confirm no entry of a newly-added or newly
re-declared-from-empty layer is left without a home in the post-hunk
enumeration.

For a **re-declared, previously-empty layer** whose new declarations
address M tiles: identical reasoning — all M entries are kind (3). If a
tile among them is *also* written with real data this same commit, does it
double-count under kind (1) as well as kind (3)? I read this as harmless
overlap in the prose (kind 3 says how the entry's *bytes* are computed —
"emitted per §15" — for any brand-new address, whether that computation
yields a real offset/length/crc or a sentinel; kind 1 is the complementary
description for an *existing* address transitioning state). The two kinds
are not stated as formally disjoint by an explicit "exactly one of," so this
is not a citation-checkable defect, but see the note under Finding 4 below
(a soft ambiguity, not filed as a top finding given low confidence and
zero byte-level consequence — an implementer would compute the same bytes
either way).

## 3. §20.4 read start-to-finish as an updater holding a two-layer file (Layer A: stores tiles, carries a PE=1 user-metadata sub-record; Layer B: stores tiles, carries a sub-record of a type this updater does not implement, MU=1)

- The updater MAY: commit any change to Layer A that §20.3 step 4 permits
  (rename, grow a dimension, extend/shorten a planar channel list at its
  end, declare/change/clear slab or alignment), MAY edit Layer A's
  user-metadata document's *content* (that makes it new output under
  R-CNF-05/R-WRT-05, independent of the PE bit, which only governs
  *unmodified* retention), MAY add wholly new layers, MAY edit or add a
  top-level user-metadata record, MAY drop Layer A outright under the
  layer record's own PE=0 (taking A's sub-record with it per hunk-15,
  regardless of the sub-record's PE=1).
- The updater MUST NOT: modify Layer B's record, its geometry, its names,
  its tile-index region, or drop Layer B, for as long as this updater
  doesn't implement the MU=1 sub-record's type — the whole layer is frozen
  by that sub-record ("blocks modification of that layer, its drop
  included," hunk-15). It MUST re-emit Layer B's record and sub-record
  byte-identically in every commit it makes (to Layer A or anywhere else),
  including B's index region unmoved (extent slot unchanged) — this is an
  ordinary appender operation (leave B's extent slot pointing at its
  existing region, per `[R-WRT-05]`), not a rewrite, so this alone does
  not require becoming a rewriter.
- The updater MAY still commit changes that touch *only* Layer A or add
  new structures, "leaving other layers editable" (§20.4's MU=1 row,
  unchanged text). It may never target B at all through a commit; only a
  rewrite could attempt to relocate B's structures, and per `[R-WRT-06]` a
  rewriter facing this same file MUST refuse to rewrite the file outright —
  the appender path is thus the *only* one under which this two-layer file
  remains editable at all, once you also want to touch A.
- If the updater wants to remove Layer B's PE=1... there is no PE=1
  sub-record on B in this scenario (B's sub-record is MU=1), so this
  doesn't arise for B; but restating for completeness: even without the
  MU=1 block, a PE=1 sub-record is never independently drop-licensed
  (§20.4's table has no "or drop it" language on the PE=1 row) — the only
  path to its removal is dropping the entire containing layer, which for B
  is itself blocked by the MU=1 sibling record. So Layer B, as specified
  here, is **permanently frozen** for this updater: it cannot be edited,
  dropped, or (via rewrite) relocated, only carried forward unchanged
  forever (or until a future updater implements the type).

## 4. §20.1 read as the author of a converter choosing rewriter vs. creator

- **Choosing rewriter**: gains cheap relocation without full decode
  (compaction-style efficiency), a bounded, explicit verification
  checklist (`[R-WRT-09]`: open, each retained layer's record, full index
  chain, checksums over copied extents — crc-level, not decode-level), and
  automatic carry-forward of ignore-lane bits and unrecognized `tarn.`
  keys it never decoded. Costs: total refusal on meeting *any* top-level or
  layer-scope record of an unimplemented type with MU=1 (no partial
  output), and it must preserve every retained record per §20.4's table
  (cannot silently drop a PE=1 record it doesn't want, cannot re-encode a
  record whose type it doesn't implement). It answers for carried
  structures only to `[R-WRT-09]`'s depth — a latent decode-only defect in
  a tile it copies travels into the output without making *the rewriter*
  non-compliant, though the *output file* itself remains nonconforming by
  the ordinary R-CNF-05 predicate (which binds bytes, not actors).
- **Choosing creator**: total freedom to drop, reinterpret, or ignore
  anything from its input (§20.4 doesn't bind it at all), no obligation to
  carry forward ignore-lane bits (writes flags=0) or unrecognized keys, no
  MU=1 refusal trap. Cost: it "answers for every byte of its output... bytes
  it copied from another file included" under the unconditional R-CNF-05 —
  and unlike the rewriter, §20.2/R-WRT-02 gives it **no explicit
  verification checklist at all**. A creator that takes any shortcut (e.g.
  copying tiles+crcs to save a decode pass, exactly Op C above) is fully
  exposed to producing a nonconforming file with no spec-stated minimum
  diligence duty to catch it first. This is the converter-author's real
  trade: rewriter buys a bounded, stated duty plus a hard refusal
  trapdoor; creator buys total flexibility at the price of open-ended,
  unstated diligence exposure. Both leave undecided *when in the pipeline*
  either tier must actually perform the checks it owes — that is `[R-WRT-03]`'s
  reliance principle for the rewriter (verify what you rely on, before
  emitting), and nothing at all, procedurally, for the creator beyond "the
  output must be conforming."

## 5. The eight checks, run against every hunk

I ran all eight checks against each of the 26 hunks; below are only the
hunks where a check surfaced something worth recording (pass or fail). For
brevity I do not re-print the full eight-check log for hunks that passed
cleanly on all eight with nothing distinctive to say (hunks 3, 4, 9, 16, 18,
20, 21, 22, 23, 24 — verified individually, no defect, notes above under
Operations or inline).

**Hunk 1** (§2.3, `[R-CNF-02]`): adds "§20.3 step 6 and" before "§20.5" in a
citation list of conduct-rule examples for "an updater's copy-forward and
set-no-other." CITATION check: both cited locations verified — §20.3 step 6
literally says "unknown ignore-lane flag bits copied forward and no other
set (`[R-CNT-08]`)"; §20.5 literally says "MUST copy the input's unknown
ignore-lane flag bits forward and set no other." Both pass. TENSE/QUANTIFIER:
the term being cited is "updater" (ranges over appender+rewriter); before
the fix only the rewriter instance was cited, an under-citation for a
claim quantified over "updater." No defect after the fix.

**Hunk 2** (§2.3, Conforming updater bullet): "A tool that modifies an
existing file, or writes a new one that preserves it (§20.1), without
necessarily understanding..." CITATION: §20.1 (as amended by hunk 11) does
state exactly this two-position split. Consistent with hunk 11. No defect.

**Hunk 5** (§6.4): see **Finding 3** below.

**Hunk 6** (§7.2, new Note): "The two flag bits are not orthogonal...
§20.4's three rows... An updater that does not implement an MU = 1
record's type never drops the record, alone or with the scope it governs
(§20.4)." LABEL check: this is inside a block headed "> **Note.**" — I
confirmed it is non-normative by R-CNF-01, and confirmed its claims are
*also* stated in normative text (§20.4's table, itself amended by hunk-15
to add "its drop included" to the MU=1 row) — so the Note restates rather
than uniquely carries the rule; no defect of the "rule stated only in a
Note" shape. CITATION: §20.4's three rows verified to match exactly
(MU=1/MU=0,PE=1/MU=0,PE=0). No defect.

**Hunk 7** (§7.2, layer record as the "one exception"): moved the layer
record's characterization from "such a case" of MU=1-carries-further-
references (WRONG, since the layer record is MU=0 per §7.3, both before
and after hunk-8) to "the one exception" to the MU=0 rule that "the extent
slot is its only sanctioned reference to bytes outside the record
sequence." This is a real, correct fix — the original placement described
the layer record's tile index as an instance of the *MU=1* carry-further-
references rule, which cannot be right since the layer record's registry-
fixed flags are MU=0 (§7.3, confirmed both pre- and post-hunk-8). CITATION:
`[R-CNF-03]` verified — states conforming readers must implement both
record types §7.3 registers; the "and updater" half of "every conforming
reader and updater implements the type" leans on R-CNF-11's "updater...
inherits every reader obligation," not cited here — a minor, non-byte-level
citation-completeness gap, not filed as a top finding (the claim is true,
just supported by a chain of two rules where one is named).

**Hunk 8** (§7.4 worked example): MU=1,PE=1 → MU=0,PE=0 for the layer
record's registry-fixed flags in the numeric worked example, now matching
§7.3's table. Verified via grep that no other place in the document still
states MU=1/PE=1 for the layer record. Correct, necessary fix; also the
load-bearing companion to hunk-7 (hunk-7's "the layer record is the one
exception [to the MU=0 rule]" only makes sense once §7.4's own example
stops contradicting §7.3's MU=0 table entry).

**Hunk 10** and **Hunk 11** (§20.1): see **Finding 2** below.

**Hunk 12** (§20.3 step 4): see Op F above — correct, necessary
completion of the four-kind partition.

**Hunk 13** (§20.3 step 4, "the bar binds a layer the commit keeps"): see
Op A/general discussion above — correct; the "no byte tells the two apart"
addition is accurate given hunk-12's parallel fix (a new layer's entries
are always freshly emitted, so physically reusing the dropped layer's old
extents is indistinguishable, byte-for-byte, from an illegal in-place
re-declaration). UNCONSTRAINED-SIBLING check: I checked whether the
sentence's new "the dropped layer's former extents included" clause omits
any sibling case — e.g. can the *new* layer's sub-records also legally
reuse the old layer's former sub-record extent bytes? Yes, by the same
logic (§5.2's partition is over the live state alone), and nothing in the
text contradicts this; no gap found.

**Hunk 14** (§20.4, PE=1 user-metadata dropped only with a layer that
carries it): see **Finding 4** below.

**Hunk 15** (§20.4, the drop-takes-the-layer-whole paragraph): see Op A/B
above; also see **Finding 1** (the untouched §20.3 Example that this hunk's
fix should have sent me to sweep and didn't get swept). Verified
exhaustiveness of "One sub-record blocks the drop" — confirmed against
§20.4's own "so for an implemented type only the PE bit bites" sentence
that MU=1-as-governing-flags is possible only for unimplemented types, so
"a sub-record... with MU=1" fully and correctly identifies the only
blocking case; tried to falsify with a registered-type or
updater-implements-it-from-its-own-definition counterexample and could
not.

**Hunk 17** (§20.5, "a layer with its sub-records" added to the drop-
disposal list): correct, swept consistently with hunk-15.

**Hunk 19** (§20.5, "whose loss the rewriter SHOULD report as that table
says"): correct, part of the same SHOULD-report sweep as hunks 15/26;
verified via grep that all three surviving "report the loss" instances now
read SHOULD.

**Hunk 25** (Appendix H, "as an appender, changes a layer..."): correct —
scopes the §20.3-step-4 fixed-declaration restriction to the appender
specifically, resolving what would otherwise be a real contradiction with
§20.5's own statement that re-declaring a layer's fixed declarations is
reserved as a *rewrite* operation precisely because a mere commit cannot do
it. Before this fix, Appendix H's "Conforming updater" bullet read as if
the restriction bound rewriters too.

**Hunk 26** (Appendix H, large block): multiple precise fixes, all
verified against their governing rules: (a) "its sub-records with it"
matches hunk-15; (b) "never removes a user-metadata record from a scope it
keeps" matches hunk-15's exact phrase; (c) "never modifies or drops a
scope" adds "or drops," matching hunk-6/hunk-15; (d) "regenerating each
tile-index region any of whose stored extents it relocates" is a
substantial, correct precision fix over the old "regenerating each index
region it relocates" — verified word-for-word against `[R-WRT-07]`'s own
text ("regenerates each tile-index region any of whose stored extents the
output relocates") and against the worked compaction example ("under a
placement that moved them it would be regenerated too" — confirming an
index region can be relocated *without* being regenerated, which the old
Appendix H wording did not distinguish); (e) new closing sentence demotes
"reports the loss" to an explicit SHOULD/advisory note, matching the
sweep. No residual defect found in this hunk.

## 6. Findings (see structured output for the canonical list; narrative here)

**Finding 1 — UNSWEPT_RESTATEMENT, §20.3 worked example (c), lines
3443-3446 (untouched by any hunk).** hunk-15 correctly expanded §20.4's
prose to "Dropping a layer by commit strands its stored tiles, its
tile-index region and its sub-records' extents as slack." The parallel
restatement in §20.3's own "Example — the three shapes a commit takes,"
case (c), still reads "...dropping a layer or another PE = 0 record where
§20.4 licenses the drop, any extent it owned, a dropped layer's tiles and
index region included, becoming slack..." — omitting any mention of
sub-records' extents. Non-byte-level: this passage is inside a block headed
"> **Example**," hence non-normative under R-CNF-01, so it cannot itself
create a conformance divergence; but it is the passage an implementer is
most likely to consult for "what becomes slack," and it now visibly
disagrees with §20.4 on enumeration completeness. Repair: append ", and its
sub-records' extents" (or equivalent) to the (c) example's list.

**Finding 2 — LOCAL_CONTRADICTION between hunk-10 and hunk-11, both in
§20.1.** Hunk-10 rewrites the rewriter *bullet* to read "writes a new file
from an existing one under a new identity (§20.5), **preserving what it
does not understand** as §20.4 provides, and carrying structures
forward...". A few sentences later, hunk-11's replacement `[R-WRT-01]` text
says "As a **rewriter** it undertakes to preserve its input: §20.4's table
**for every record**, the unknown ignore-lane bits..." These two
quantifiers disagree: §20.4's table in fact governs preservation of every
*retained* record, understood or not (its MU=0/PE=1 and MU=0/PE=0 rows
apply to implemented types too — "implementing a record's type confers
understanding of it," and the PE=0 row's drop-licence is explicitly
available for the layer record, a type every conforming updater
implements). "What it does not understand" mischaracterizes the bullet's
own scope down to only the MU=1 case, which is a narrower set than "every
record." Non-byte-level: the bullet list is informal orientation prose
preceding the numbered `[R-WRT-01]` requirement; an implementer following
the requirement text (the correct, broader statement) would not diverge in
output bytes. Repair: change hunk-10's clause to "preserving what §20.4
provides" (drop "it does not understand"), or otherwise align it with
`[R-WRT-01]`'s "for every record."

**Finding 3 — NEW_AMBIGUITY / soft LOCAL_CONTRADICTION, hunk-5, §6.4.**
"The baseline remote open is two requests..." opens the paragraph
unconditionally. Fifteen words into item (1)'s description, the hunk's new
parenthetical says "(`[R-CNT-10]`, which governs where it does not, a
separate size probe then making **the baseline three**)." The same noun
phrase "the baseline" is used first to mean an unconditional "2" and then,
in the very next clause, to mean "3" under a stated condition — without
ever saying "the baseline *becomes*" or "*rises to*" three, or otherwise
flagging that this is a variant, not a redefinition. A reader who reads
only the opening sentence and this parenthetical, without working through
the surrounding prose as carefully as this audit did, could reasonably
read the document as internally contradicting itself about what "the
baseline" is. Arithmetic itself checks out (2 fixed-target requests + 1
separate size probe = 3, consistent with `[R-CNT-10]`'s "probe separately
or fail the open"). Non-byte-level: §6.4's own governing Note states "no
request count is a conformance property," so this cannot fork accept/reject
bytes. Repair: replace "the baseline three" with "the open three requests"
or "this count to three," reserving "the baseline" for its one, fixed,
opening-sentence meaning.

**Finding 4 — NEW_AMBIGUITY, hunk-14, §20.4 (lower confidence).** "...the
user-metadata record PE = 1 and is dropped only with a layer that carries
it" uses "the user-metadata record" (singular, matching "the layer record"
in the same sentence) to describe *both* the top-level and the
sub-record instance of type 0x0002 (§7.3: "user metadata | file when
top-level; layer as sub-record"). Taken literally, "is dropped only with a
layer that carries it" is vacuously true for the top-level instance (no
layer ever "carries" a top-level record, so the stated condition never
obtains, and it is in fact never dropped) — but a reader who has not
worked through hunk-15's much more explicit restatement a few lines later
("A commit never removes a user-metadata record from a scope it keeps: a
top-level one from the file, or a sub-record from a layer the commit
retains") could misread the clause as implying every user-metadata record
has an associated layer. Non-byte-level, and I rate this lower-confidence
than Findings 1-3 since the very next paragraph in the same subsection
(hunk-15) does fully disambiguate it; flagged because the charter asks for
exactly this kind of same-passage tension. Repair: "and is dropped only
where it is a sub-record of a layer that is itself dropped, never
otherwise" (or simply defer entirely to hunk-15's fuller sentence and drop
the parenthetical claim here).

## 7. Rejected candidates

- Hunk-9/21/24's "Compaction" → "A rewrite"/"A rewriter's output"
  substitutions: I initially suspected an overclaim (does *any* rewrite
  really reclaim slack/reset F the same way compaction does?), but §20.5's
  own unedited text ("A rewrite is the only operation that reclaims
  slack") already states this unconditionally for any rewrite, not just
  compaction, so the generalization is correct in all three places, not a
  defect. Dropped.
- Hunk-22 (Appendix C, "Index encodings (§15.1)" → "(§7.4)"): I initially
  flagged this as breaking the pattern of every other line in that list
  (which cites the *semantic* section, e.g. "Codecs (§17.2)," not the
  §7.4 field-declaration table). Checked against §10.2's own canonical
  registry-space table, which explicitly lists "index encoding (§7.4)" —
  the *same* citation the hunk produces. So hunk-22 in fact *aligns*
  Appendix C with §10.2 rather than breaking a pattern; the apparent
  inconsistency with the other appendix lines (which don't all match
  §10.2 either — e.g. Appendix C says "Sample types (§12.1)" while §10.2
  says "sample type (§12.2)") is pre-existing and untouched by this hunk.
  Dropped as a finding against this hunk specifically.
- Hunk-18's colon-for-dash swap: initially flagged as a possible new prose
  issue, then recognized as itself a correct NESTED_DASH repair (removing
  an em-dash pair that had been nested inside the sentence's own outer
  em-dash-delimited aside). Verified by counting all em-dashes in the
  surrounding paragraph post-fix (exactly one matched pair remains).
  Dropped as a finding; noted as a correct fix instead.
- The §20.4 MU=1-row tension between "leaving other layers editable" and
  "a rewriter MUST refuse to rewrite the file" (both pre-existing,
  untouched text): initially looked like a contradiction (partial vs.
  total refusal for the "same" actor), resolved once I distinguished that
  the "leaving other layers editable" clause characterizes an *appender's*
  option (touch other layers via ordinary commits, leaving this layer's
  bytes physically undisturbed) while "a rewriter MUST refuse to rewrite
  the file" is the *rewriter's* stricter case (a rewrite must place every
  structure it carries, so it cannot selectively spare one layer). Not
  introduced or touched by any of my 26 hunks; dropped as a finding but
  used in the Op B narrative above.
- Op F's possible kind-(1)/kind-(3) overlap for a newly stored tile in a
  newly added layer: considered as a partition-completeness defect, but
  concluded it's harmless (both descriptions, where they overlap, compute
  the identical byte result — a stored entry with real offset/length/crc)
  and the charter's "four kinds" language doesn't itself claim strict
  mutual exclusivity. Dropped as a top finding, noted as a soft
  observation only.

## 8. Confidence / what an empty-findings list would have needed

Not applicable — four findings are reported above. Where I came up empty
(the eight-check sweep on hunks 1-4, 6-9, 16, 18, 20-25), I record here
what would have caught a defect had one been present: full re-reading of
the governing rule cited by each new/changed citation (I opened and quoted
every cited requirement in §2, §6, §7, §9, §20, §21 at least once), a
positive-control search proving each zero-hit grep could have matched
(§1 above), and, for every insertion, forward and backward reads for
stranded anaphora (documented per-hunk above, e.g. hunk-3, hunk-13,
hunk-23, hunk-26).
