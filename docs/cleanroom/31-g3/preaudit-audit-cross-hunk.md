# Cross-hunk consistency audit — round 31 — working transcript

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (all sections
§2–§24 and Appendices A, G, H, read in `sed -n` ranges; §1, Appendices B–F not read) and
`hunk-01.diff` … `hunk-23.diff` under `r31-audit/case/`, each by name (no directory listing;
`full.diff` not read; no other hunk file exists in my knowledge). Ran `grep -n` on the spec and
`python3` scripts of my own that read only the spec. Wrote, under my private scratch directory
only: `flat.txt` (a whitespace-normalised, `> `-stripped copy of the spec for phrase search),
`ph.py` (phrase-search helper), `count.py` (register instance counter), `transcript-head.md`,
`transcript-findings.md`, and the assembled transcript at `r31-audit/out/audit-cross-hunk.md`.

Context I did not ask for and did not use: the runtime placed a project-instruction pointer
(CLAUDE.md → AGENTS.md, not opened), an index of four user-memory notes (titles only, not
opened), a git-status block naming the branch and five recent commit subjects, and MCP server
instructions. None of it was read as evidence; the commit subjects name prior rounds and ADR
numbers, and I disregarded them. Nothing was read from docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, registry.json, git history, or the web.

Path check: every hunk file was at the path the brief gave; the spec was at the path given.
Hunk headers ("lands at lines N–M", "nearest preceding heading") were verified against the
current file by grep/sed for a distinctive phrase of each hunk — all 23 anchors matched
(224, 887, 1265, 1633, 1998, 2009, 2502, 2577, 2698, 2741, 3135, 3202, 3227, 3271, 3316,
3417, 3495, 3745, 3766, 3884, 4578, 4652, 4690). No header mismatch.

## Grouping by rule (not by section)

**A. Trailer flags: the ignore-lane copy-forward / set-no-other rule.** Hunks 02 (§6.3
[R-CNT-08], compactor sentence and updater MUSTs), 15 (§20.3 step 6 [R-WRT-04]), 17 (§20.5
[R-WRT-06]), 22 (App G item 8), 23 (App G closing paragraph). Untouched restatements:
§2.3 [R-CNF-02] ("§6.3's flags = 0 against a set ignore-lane bit"), §21.6 row "An ignore-lane
flag bit (16–31) is set", §18.3, §10.1, F19, Appendix A's annotated trailer.

**B. The §14 bar's de-addressing carve-out, extended from grid-count shrink to planar channel
removal.** Hunks 04 (§11.1 *Rationale* block — labelled, so non-normative), 13 (§20.3 step 4,
ordinal-bar paragraph — normative), 14 (§20.3 step 4, shrink paragraph — normative), and 12
(§20.3 step 4, sample-type paragraph). Untouched sibling in the same step: "Where a shrink is
permitted the de-addressed tiles' extents become slack ([R-CNT-21]), [R-CNT-17] obliges the
smaller entry_count and so a re-emitted index region, and every surviving stored tile is
untouched." Also §23.1 [R-PRV-01] ("a shrink that either drops tiles out of the addressed set
or turns real positions into padding").

**C. Where a reader declines a user-metadata document on resource grounds.** Hunks 09 (§18.2
*Note* — non-normative) and 20 (new §21.6 row — restates its governing rule; §21.1 says the
rule governs on divergence). Rule edited before this range that names the scope: §21.9
[R-ERR-04] ("a layer, a tile, or the record carrying a user-metadata document, as §18.2
assigns"), and [R-MTA-09] in §18.2.

**D. Layout-specific designation of P·Q / P·Bᶜ / C·N under [R-ENC-04].** Hunks 05 (§14.2
[R-SER-02] — normative), 18 (§21.3 L2 register cell), 07 (§17.2 *Note* — non-normative).
Untouched: [R-GEO-03] (C·N planar), [R-SER-07], L21, L44, T3/T14/T21/T22, [R-RDR-03].

**E. The PE = 0 drop licence.** Hunks 16 (§20.4 table cell, MU = 0 / PE = 0 — the table sits
in a ">"-free block and is normative) and 11 (§20.3 step 2). Untouched: §20.4's three
flag-source sentences above the table, §20.5 ("less any record §20.4 lets it drop"; "only
where §20.4's table licenses it"), §2.4 preserve-verbatim, §21.6 experimental-type row, §23.1.

**F. Unassigned vs experimental-range user-metadata encoding.** Hunks 01 (§2.3 [R-CNF-11])
and 08 (§17.4). Untouched: [R-MTA-10], [R-MTA-09]'s last sentences, §21.5 preamble, §21.6 row,
§9.7 [R-LIF-08], §22.3 [R-SEC-04], Appendix H.

**G. Singletons.** 03 (§9.2 barrier conduct), 06 (§14.2 [R-SER-08]), 10 + 21 ([R-MTA-05] key
comparison and App G item 3's layer-name order), 19 (L23 detection point).

## Per-hunk rule statements (what each repair makes true of an implementation)

01. A verifier meeting a user-metadata record whose encoding is ≥ 0x80 has nothing unchecked
    and certifies; encoding 0 or 3–0x7F is an R1 violation (nonconforming).
02. A compactor's output trailer and an appender's new trailer carry exactly the input's
    ignore-lane bits: none cleared, none added. (Bytes: the ignore lane of the emitted trailer
    equals the input's.)
03. Omitting a barrier is an actor violation; the file is conforming regardless.
04. (Rationale) a planar channel removal de-addresses its tiles the way a grid shrink does.
05. [R-ENC-04] binds P·Q only in an interleaved layer and P·Bᶜ only in a planar one.
06. A reader that returns a non-0/1 interleaved bool byte, detected or not, returns true.
07. (Note) an empty layer's decoded size is still overflow-checked, per its layout.
08. Same rule as 01, stated in §17.4.
09. (Note) a resource decline of a document is ignore-record or whole-file, reported as a limit.
10. Key order is unsigned-byte lexicographic with proper prefixes first.
11. An appender may drop a defective carried-forward record only if it is an unregistered
    record with MU = 0, PE = 0.
12. A re-type reaching stored tiles yields wrong content (motivating the bar).
13. A planar channel removal de-addresses that channel's N tiles; their extents become slack;
    the new-file SHOULD reaches such a commit.
14. In the shrink test, de-addressing by grid fall or by channel removal is not itself a §14
    alteration, and rescues nothing.
15. Step 6's trailer: copied-forward ignore-lane bits and no other set.
16. An updater MAY drop an unimplemented MU = 0 / PE = 0 record in any commit; a compactor
    whenever it rewrites.
17. Compactor output trailer: input's ignore-lane bits and no other.
18. L2's instances are layout-keyed: planar C·N, interleaved P·Q, planar numeric P·Bᶜ.
19. L23's name-region overrun is detected at open; the others at layer access.
20. New §21.6 row: document/window over the reader's bound → ignore-record (or whole-file),
    reported as a resource limit, file conforming.
21. (Profile) layer-name order uses [R-MTA-05]'s comparison.
22. (Profile) a compactor under the profile carries ignore-lane bits and sets no other.
23. (Profile) item 8's floor binds creator and compactor save §20.5's case; its flags half is
    the creator's only.

## Within-group agreement (word for word, quantifier for quantifier)

**A.** §6.3 compactor: "carries the input's unknown ignore-lane bits into its output trailer
rather than writing flags = 0, and sets no other". §6.3 updater: "MUST copy forward unknown
ignore-lane bits of the file it modifies, MUST NOT clear them, and MUST NOT set any other".
Step 6: "unknown ignore-lane flag bits copied forward and no other set". §20.5: "MUST copy
the input's unknown ignore-lane flag bits forward and set no other". G item 8: "carries its
input's unknown ignore-lane bits forward instead, setting no other". G closing: "its `flags`
half a creator's rule alone". Set ranged over: "the input's / the file it modifies' unknown
ignore-lane bits" in every member; "no other" in every member. AGREE. Force: §6.3 and §20.5
and step 6 are normative; G is non-normative and cites [R-CNT-08]. The §21.6 row ("Ignored;
the file is conforming") and [R-CNF-02] ("not a file-conformance violation") agree that a set
bit never makes the file nonconforming, so the new MUST NOTs are conduct rules — consistent
with [R-CNF-02]'s model. "no other": whether it ranges over ignore-lane bits only or all flag
bits does not fork, since an incompat-lane bit is F19 (reject-file) and [R-CNF-05] already bars
it.

**B.** Rationale (04): "a tile dropped out of the addressed set carries no §14 obligation and
its extent becomes slack — by a grid count falling or, in a planar layer, by its channel being
removed (§20.3)". Ordinal paragraph (13): "Removing a channel de-addresses its N tiles: those
the superseded generation stored carry no §14 obligation afterwards and their extents become
slack (§5.2), as a shrink's de-addressed tiles do below". Shrink paragraph (14): "Dropping a
tile out of the addressed set — §11.2's grid count falling, or a channel removed from a planar
layer taking its N tiles with it — is not itself such an alteration, a tile the new state does
not address carrying no §14 obligation and its extent becoming slack however it was
de-addressed; but neither does it rescue a commit that damages a prior-generation stored
tile." The three agree on the carve-out and on "planar". They do NOT agree on the caveat: 14
and the pre-existing shrink text carry "neither does it rescue"; 13 does not (finding X-05).
04 and 14 both place channel removal inside shrink-framed sentences that are followed by "The
other bar reaches neither a shrink nor a growth" / "a shrink is not one" (finding X-06). The
untouched consequence sentence names entry_count and index re-emission for "a shrink" only;
for a channel removal the same consequences follow from step 4's general re-emission rule and
[R-CNT-17], so no obligation is missing, only the restatement.

**C.** Note (09): "ignore-record for that record, which is also the narrowest scope at which
[R-ERR-04] lets it decline the document on resource grounds; it MAY instead decline the whole
file. Either refusal is reported as a resource limit, not as corruption." Row (20):
"Ignore-record on capability grounds — the narrowest-scope decline [R-ERR-04] names for a
document — reported as a resource limit and not as corruption; the file is conforming, and
the reader MAY instead decline the whole file". [R-ERR-04]: "a reader MAY decline it — at the
whole file, or at the narrowest scope … the record carrying a user-metadata document, as
§18.2 assigns"; "a refusal on resource grounds MUST be reported as a resource limit". Scope
and reporting AGREE. Ground label DISAGREES: Note says "resource grounds", row says
"capability grounds", and [R-ERR-04] counts "the two capability refusals §21.6 names … are not
this ground" (finding X-01). Condition DISAGREES in quantifier: Note "decodes to more than the
guarantee", row "exceeds the reader's own bound" (finding X-07).

**D.** [R-SER-02] (05): "each for the layout its row states — a planar layer has no P · Q to
form". L2 (18): "planar C·N …; interleaved P·Q …; planar numeric P·Bᶜ". Note (07): "the decoded
size the layout gives, P·Q or P·Bᶜ". [R-GEO-03] (untouched): addressed-tile count "N for an
interleaved layer and C · N for a planar layer … These products are declaration-derived
quantities". L44/T3/T14/T21/T22 already keyed "interleaved P·Q; planar numeric P·Bᶜ; packed
planar bool ⌈P/8⌉". AGREE. L2 omits ⌈P/8⌉ correctly (⌈P/8⌉ ≤ P; no distinguishable file). L2
instance count 9 before and after (relabelling only); register total 277 unchanged (computed).

**E.** Cell (16): "an updater MAY drop the record in any commit, including one whose only
effect is the drop, and a compactor MAY drop it whenever it rewrites the file". Step 2 (11):
"MUST NOT drop the record save where §20.4's table licenses the drop, which it does for an
unregistered record stored MU = 0, PE = 0 and for no other". §20.5: "less any record §20.4
lets it drop"; "only where §20.4's table licenses it". The licence AGREES across 16, 11 and
§20.5. The key of the licence DISAGREES between 11 and §20.4's flag-source sentences:
11 keys it to *stored* bits for every unregistered type; §20.4 keys it to stored bits only
for a type the updater does not implement, and to the implementing definition ("the stored
bits never do") otherwise (finding X-02). Sweep for the removed condition: "independently"
3 hits, none about records; "only effect" 1 hit (the new cell). The old condition has no
surviving restatement.

**F.** §2.3 (01): "under an experimental-range encoding — one this specification does not
assign and a conforming file can carry (§21.6) — is not such a ground … encoding 0 and a
reserved value are violations (§21.5, R1)". §17.4 (08): "an experimental-range document
encoding in a conforming file is not a violation (§21.6), no document rule attaches to its
extent, and certification is unaffected". AGREE with each other, with the §21.5 preamble,
the §21.6 row, Appendix H, and [R-MTA-10]'s structural-checks sentence. Unswept: §9.7 and
§22.3 still say "under an unassigned encoding" (finding X-04).

**G.** 03: "as [R-CNF-02] says of every conduct rule" — [R-CNF-02]: "a file is never
nonconforming by virtue of one: conduct rules bind the actor". Verbs match ("never
nonconforming by virtue of"). 06: consistent with §21.1 ("resolves a nonconforming
interleaved boolean byte to a value"), [R-TYP-04], Appendix H ("it chooses to return rather
than reject"), T2, [R-CNF-12]. 10/21: [R-MTA-05]'s comparison is over "keys' UTF-8 bytes";
layer names are raw bytes ([R-ENC-13]); item 3 borrows it for layer-name order — verbs
"compared lexicographically as unsigned bytes with a proper prefix ordering first" vs
"compared as [R-MTA-05] compares keys": match. Item 3's other comparison ("compared
lexicographically" over header/payload/extent, and "ties by layer name") remains unpinned
(finding X-08). 19: §19.1 step 4 and §19.2 place the name parse at open; L3/L5/L6 are
"open"; consistent.

## Force check ([R-CNF-01]: by label, not marker)

- 04: inside "> **Rationale.**" — non-normative. Its normative counterpart is 13/14 in §20.3
  (numbered step, no label) — the repair landed in force.
- 07: inside "> **Note.**" — non-normative; the rule it restates is [R-ENC-04]/[R-SER-02]
  (05, normative). Landed.
- 09: inside "> **Note.**" — non-normative; the governing rule is [R-MTA-09] + [R-ERR-04],
  both normative and untouched, and both already say record-scope decline is available.
  Landed (nothing normative depends on the Note).
- 16: the §20.4 table sits in a block with no ">" and no label — normative.
- 20: §21.6 table — no ">" and no label; §21.1 makes its entries restatements that yield to
  the rule they cite. Normative as restatement.
- 21/22/23: Appendix G is "(non-normative)" by title. Nothing normative depends on them.
- All others: body prose in normative sections.
- Nothing that carries force now depends on a labelled block. [R-ERR-04] (normative) is now
  contradicted by a normative §21.6 row's self-label (X-01).


## Anaphor check (check 8) — every back-reference read forward from each insertion

- 01 (§2.3): "*Cannot establish* is not a finding…", "An established violation takes
  priority" — no anaphor into the edited sentence; "such a ground" inside the repair resolves
  to "a capability or resource ground" two sentences up, unchanged. UNAFFECTED.
- 02 (§6.3): "it" in "for it to mean anything by" = the writer; "it" in "that defines it" =
  the bit; following sentence "An updater encountering an unknown incompat-lane bit…" carries
  no anaphor. UNAFFECTED.
- 04 (§11.1 Rationale): "One shrink can do several of these at once" — "these" = the listed
  non-alterations, now including the two de-addressing means; still true. UNAFFECTED.
- 09 (§18.2 Note): "Either refusal" = ignore-record and whole-file decline, both in the new
  sentence. UNAFFECTED.
- 11 (§20.3 step 2): "Reproducing a structure's bytes unchanged…" no anaphor. UNAFFECTED.
- 12 (§20.3 step 4): "Such a change is a new layer…" = a re-type reaching stored tiles, same
  as before. UNAFFECTED.
- 13 (§20.3 step 4): the sentence after the insertion — "**The test is the effect on a stored
  tile, not the shape of the edit**: a commit that moves only the ordinals of channels the
  superseded generation stored no tile for alters nothing this bars" — "this" resolved before
  to the ordinal bar (nearest rule: "Appending a channel, or removing the last, re-indexes
  nothing"); the nearest preceding sentence is now the inserted §14-obligation sentence.
  "this bars" still reads as the paragraph's bar because "moves only the ordinals" names it;
  UNAFFECTED, but the insertion sits between the ordinal statement and its test sentence
  (noted under X-06). Backwards: "as a shrink's de-addressed tiles do below" and "the
  recommendation below" resolve forward to the shrink paragraph and the SHOULD — both present.
- 14 (§20.3 step 4): "but neither does it rescue" — "it" = dropping a tile out of the addressed
  set (either means); "Unstoring that tile … does not rescue it either" — "that tile" = "a
  prior-generation stored tile" in the repaired sentence, unchanged. UNAFFECTED.
- 16 (§20.4): "No commit therefore removes a layer record…" — "therefore" = the PE = 1 rows,
  unchanged. UNAFFECTED.
- 20 (§21.6): the closing paragraph's "Two structural cases are conforming files a reader
  nevertheless refuses" — "structural" keeps the new (resource) row out of the two.
  UNAFFECTED as anaphor; see X-01 for the count in [R-ERR-04].
- 21/22/23 (App G): item 8's "The `flags` half is a creator's rule" and the closing
  paragraph's "item 8" resolve to each other consistently. UNAFFECTED.

## Analogy check (check 7) — governing verbs side by side

- 03: repair "the file it produces is never nonconforming by virtue of it" / [R-CNF-02] "a
  file is never nonconforming by virtue of one". Same verb, same set. PASS.
- 13: "as a shrink's de-addressed tiles do below" / shrink text "a tile the new state does not
  address carrying no §14 obligation and its extent becoming slack … but neither does it
  rescue". Repair drops the qualifier (X-05).
- 14: "as … §11.2's grid count falling" — §11.2 defines Gᵢ = ⌈Eᵢ/Tᵢ⌉. PASS.
- 20 and 09: "the narrowest-scope decline [R-ERR-04] names for a document" / [R-ERR-04] "the
  record carrying a user-metadata document, as §18.2 assigns". PASS on scope.
- 21: "compared as [R-MTA-05] compares keys" / [R-MTA-05] "compared lexicographically as
  unsigned bytes with a proper prefix ordering first". Both range over byte strings; layer
  names are raw bytes by [R-ENC-13]. PASS.
- 12: "of the kind §21.7 leaves unwitnessed" / §21.7 "A writer that emits well-formed
  structures carrying wrong sample values … produces a file that every checksum in §8
  certifies" — but a size-changing re-type is not "well-formed": T3/T14 witness it (X-03).
- 05: "each for the layout its row states" / table rows. PASS.
- 22/23: "§20.5's carried-feature case" / §20.5 "Where the output carries a feature a later
  minor defines and this compactor does not … SHOULD be at least the input's". PASS.

## Unconstrained siblings (check 6)

- Trailer (02/15/17/22): fields magic, major, minor, flags (incompat: F19; ignore: this rule),
  dir_offset, dir_length, committed_file_length, file_id (fresh for compactor, same for
  appender), reserved (zero), CRC — all fixed. NONE OPEN.
- §20.4 cell (16): MU = 1 / MU = 0,PE = 1 / MU = 0,PE = 0 — all three rows carry an
  obligation; MU = 1,PE = 0 folded by [R-CNT-12]. NONE OPEN.
- [R-SER-08] (06): detect+reject, detect+return, not-detect+return, detect+reject-file
  ([R-CNF-12]) — all four fixed. NONE OPEN.
- App G item 3 (21): layer-name order pinned; record-key comparison and "ties by layer name"
  not (X-08).
- L2 (18) / [R-SER-02] (05): planar bool ⌈P/8⌉ not listed in L2 — correctly, since
  ⌈P/8⌉ ≤ P and P is its own instance; the Note (07) omits it too (rejected R3).
- Channel removal (13/14): §14 obligation and slack stated; entry_count/index re-emission
  and [R-SLB-04]/[R-SLB-01] follow from step 4's general rules ("bind a shrink as they bind
  any commit"; "Every layer whose stored-tile set or index content this commit changes has
  its tile-index region re-emitted"). NONE OPEN in force; the restatement is shrink-only.

## Findings

### X-01 — [R-ERR-04]'s "the two capability refusals §21.6 names" is now a miscount, and the two repairs label the same decline differently
Hunks 20 (and 09). OVERCLAIM (with LOCAL_CONTRADICTION). §21.6 new row (line 3884), Defined
behavior cell: "Ignore-record on capability grounds — the narrowest-scope decline
`[R-ERR-04]` names for a document —". §18.2 Note (hunk 09, line 2698–2700): "lets it decline
the document on resource grounds". §21.9 [R-ERR-04] (untouched): "Software that declines **on
that ground** a file whose every quantity lies within the table is not a conforming reader
(`[R-CNF-03]`) — the two capability refusals §21.6 names, a foreign format major and an
unimplemented MU = 1 type, are not this ground —". After hunk 20, §21.6 names three refusals
of which one calls itself "on capability grounds" and *is* this ground. Within the pair, the
Note says "resource grounds" and the row says "capability grounds" for the identical decline.
Not byte-level: the decline is permitted, and its reporting fixed, under every reading; only
the classification sentence in [R-ERR-04] becomes false. Direction: the row should change —
"Ignore-record on resource grounds" — matching [R-ERR-04]'s own vocabulary and the Note; if
the maintainer prefers [R-MTA-09]'s "capability" word, [R-ERR-04] must instead read "the two
capability refusals §21.6's closing paragraph names", as §2.3 [R-CNF-03] already does.

### X-02 — step 2 keys the drop licence to *stored* flags for every unregistered type; §20.4 keys it to the implementing definition for a type the updater implements
Hunk 11. OVERCLAIM. §20.3 step 2 (lines 3135–3137): "MUST NOT drop the record save where
§20.4's table licenses the drop, which it does for an unregistered record stored MU = 0,
PE = 0 and for no other." §20.4 (lines ~3400–3410, untouched): "For a type the updater
implements that this specification does not register, the definition it implements the type
from supplies the flags, and the stored bits never do (`[R-CNT-22]`, §10.3). For a type the
updater does not implement, the stored flags are authoritative". So the table licenses a
drop for an implemented experimental type whose *definition* says PE = 0 whatever the stored
bit says, and withholds it where the definition says PE = 1 though the stored bit is 0. The
gloss "stored … and for no other" is wrong in both directions for that class. Byte-level
question: the file with the record dropped is conforming, and an appender trusting the gloss
would drop a stored-PE=0 record its own definition marks PE = 1 (or refuse to drop a
stored-PE=1 one its definition marks PE = 0) — a fork in emitted directories — but the
operative clause of the same sentence defers to "§20.4's table", and the table's own preamble
states the source rule, so I grade it not byte-level: the fork exists only for an implementer
who trusts the gloss over the clause that cites the table. Repair: "which it does for a
record with MU = 0, PE = 0 under the flags §20.4 makes authoritative for its type — the stored
bits for a type the appender does not implement, its own definition for an unregistered type
it does — and for no other." Direction: step 2 changes; §20.4 stands.

### X-03 — "wrong content, of the kind §21.7 leaves unwitnessed" overclaims: a size-changing re-type is witnessed
Hunk 12. OVERCLAIM. §20.3 step 4 (lines 3202–3204): "it makes the stored bytes of each tile
it reaches denote values the writer did not store — wrong content, of the kind §21.7 leaves
unwitnessed —". A re-type between types of equal element size (int8 → uint8) is unwitnessed.
A re-type that changes element size (uint8 → uint16) changes the decoded size (§14.2), which
T3 (`[R-SER-07]`) and T14 (`[R-COD-04]`) witness at tile use, and the fill-length cross-check
L30 witnesses at layer access unless the fill is re-emitted; a re-type uint8 → bool in an
interleaved layer is T2's witness. The previous wording ("makes each stored tile it reaches
nonconforming") overclaimed the other way; the repair swapped one exhaustive claim for its
opposite. Not byte-level: the bar binds either way and the sentence is motivation. Repair:
"— wrong content, unwitnessed (§21.7) where the element size is unchanged and a
decoded-size violation (T3, T14) where it is not —".

### X-04 — §9.7 and §22.3 still say "under an unassigned encoding" where the repairs changed §2.3 and §17.4 to "experimental-range"
Hunks 01, 08. UNSWEPT_RESTATEMENT. §9.7 [R-LIF-08] (lines 1491–1494): "A user-metadata
document under an unassigned encoding asks nothing of this walk: no rule attaches to its
content (`[R-MTA-10]`), so there is no violation there to look for, and what the verifier
reports instead is that rule's subject." §22.3 [R-SEC-04] (lines 4146–4151): "the extent of a
user-metadata record under an unassigned encoding is covered by its terminal CRC but
constrained by no content rule (`[R-MTA-10]`): … so a certificate covers those bytes
uninspected". "Unassigned" covers encoding 0 and 3–0x7F, which R1 registers as violations —
exactly the conflation hunks 01 and 08 removed ("encoding 0 and a reserved value are
violations (§21.5, R1)"). For those values there is a violation to look for and no
certificate covers anything. Not byte-level: R1 is reader-detected at open/layer access
regardless of the walk. Repair: "under an experimental-range encoding" in both, as §2.3,
§17.4, §21.5's preamble and Appendix H now read.

### X-05 — hunk 13 restates the de-addressing carve-out without the "neither does it rescue" caveat its two siblings carry
Hunk 13. UNDERSHOT. §20.3 step 4 (lines 3227–3229): "Removing a channel de-addresses its N
tiles: those the superseded generation stored carry no §14 obligation afterwards and their
extents become slack (§5.2), as a shrink's de-addressed tiles do below". Sibling (hunk 14,
line 3273–3276): "a tile the new state does not address carrying no §14 obligation and its
extent becoming slack however it was de-addressed; but neither does it rescue a commit that
damages a prior-generation stored tile." "Carry no §14 obligation afterwards" invites the
reading that a commit which removes channel c and also changes tile extents is clear of the
bar for c's superseded-stored tiles, since they carry no obligation "afterwards". The bar's
own statement above — "for any tile that layer stores **in the generation this commit
supersedes** … The tense is the prior generation's" — and the shrink paragraph's "the §14 bar
is the whole of the test" govern, so not byte-level. Repair: append "— and, as there,
de-addressing rescues nothing: a commit that also alters what §14 fixes for such a tile is
barred".

### X-06 — channel removal is now stated inside shrink-framed sentences that go on to say the ordinal bar "reaches neither a shrink" / "a shrink is not one"
Hunks 04, 14 (13). NEW_AMBIGUITY. §11.1 Rationale (lines 1628–1644): "a shrink is barred
wherever it alters what §14 fixes … and permitted wherever it does not: a tile dropped out of
the addressed set carries no §14 obligation … — by a grid count falling or, in a planar layer,
by its channel being removed (§20.3) — … The other bar reaches neither a shrink nor a growth:
it bars a change to a planar layer's channel declarations that moves a stored tile's disk
ordinal." §20.3 shrink paragraph (lines 3270–3289): "Dropping a tile out of the addressed
set — §11.2's grid count falling, or a channel removed from a planar layer taking its N tiles
with it — is not itself such an alteration … The bar beside the §14 bar does not reach a
shrink either: it bars a change to a planar layer's channel declarations that moves a stored
tile's disk ordinal, and a shrink is not one." A reader who takes channel removal as a
species of "shrink" (it is introduced as one of the ways a shrink de-addresses) concludes the
ordinal bar does not reach it; the ordinal paragraph (lines 3218–3222) says "inserting or
removing one moves every channel after the affected position. Either is such a change
wherever the layer stores a tile for a channel that moved." Under shrink = extent shrink, no
contradiction; but the two repairs together created the reading. Not byte-level: the ordinal
paragraph states the rule unconditionally and "a shrink is not one" is literally true.
Repair: in both places, say "by a grid count falling — a shrink — or, in a planar layer, by
its channel being removed, which is not a shrink and which the ordinal bar reaches wherever a
later channel stores a tile".

### X-07 — the Note's condition ranges over the §21.9 guarantee; the row's ranges over the reader's own bound
Hunks 09, 20. TENSE_QUANTIFIER. §18.2 Note (lines 2695–2701): "A file whose document decodes
to more than the guarantee stays conforming … A reader that proceeds takes ignore-record for
that record, which is also the narrowest scope at which `[R-ERR-04]` lets it decline the
document on resource grounds; it MAY instead decline the whole file." §21.6 row (line 3884):
"exceeds the reader's own bound, which is no smaller than §21.9's guarantee". [R-MTA-09]:
"a reader decodes with a bound of its own choosing, no smaller than §21.9's user-metadata
guarantee, and a document exceeding that bound is ignore-record". The Note names two
outcomes for a document above the guarantee — ignore-record or whole-file decline — and
omits the third, which [R-MTA-09] obliges: a reader whose own bound admits it decodes it.
Non-normative Note; not byte-level. Repair: "A reader whose bound it exceeds takes
ignore-record for that record …".

### X-08 — item 3 pins the comparison for layer-name order but not for the record key in the same item
Hunk 21. UNCONSTRAINED_SIBLING. App G item 3 (line 4578): "ascending layer-name byte order,
compared as `[R-MTA-05]` compares keys"; same item (lines 4589–4592, untouched): "type 0x0001
ties by layer name, and every other type by the record's header with **extent_offset masked
to zero**, then its inline payload, then the contents of its extent, compared
lexicographically." Payload and extent are byte strings of differing lengths; without the
proper-prefix rule two writers can order two records differently and both meet the item.
Non-normative profile; not byte-level. Repair: "compared lexicographically, as
`[R-MTA-05]` compares keys" at the record-key sentence, and "ties by layer name, compared the
same way".

## Rejected candidates

- R1 (hunk 02): [R-CNF-02] names "§6.3's flags = 0 against a set ignore-lane bit" as one of
  "the cases this text states" of expressly non-file-violations, and hunk 02's updater "MUST
  NOT set any other" / compactor "sets no other" are not named. Dropped because the phrase
  names the family by its declared non-violation ("a set ignore-lane bit"), which §6.3's
  general clause ("a set ignore-lane bit is not a file-conformance violation") already
  extends to the new clauses, and [R-CNF-02]'s general sentence binds them without
  enumeration.
- R2 (hunk 02): "carried by every tool after" — a producer's whole-file rewrite that is not a
  compaction (§20.4) is a creator and writes flags = 0. Dropped because the clause is a
  rationale for "no writer under this text originates a bit", ranges over the file's own
  custody chain, and forks nothing.
- R3 (hunk 07): "the decoded size the layout gives, P·Q or P·Bᶜ" omits planar bool ⌈P/8⌉.
  Dropped because ⌈P/8⌉ ≤ P is bounded by P's own check, so no file distinguishes, and the
  block is a Note.
- R4 (hunk 20): §21.6's preamble "A reader that treats any of them as a failure is the
  nonconforming party" against a row whose defined behaviour is a decline. Dropped because
  "failure" there means a validity finding, and the row fixes the report as a resource limit.
- R5 (hunk 19): L23's Detected cell now splits by region while the Instances cell keeps
  "leading fixed fields (name … C)" as one instance spanning both points. Dropped because
  §21.1 individuates instances by alternative and container, not detection point, and
  [R-VEC-02] records no detection point, so the corpus is unaffected.
- R6 (hunk 16): "MAY drop the record in any commit" against the MU = 1 row's "MUST NOT modify
  the scope the record governs" for a PE = 0 sub-record of a layer blocked by an MU = 1
  sub-record. Dropped because a blocked commit is not an available commit; the licence
  presupposes one.
- R7 (hunk 13): "Removing a channel de-addresses its N tiles" lacks "planar". Dropped because
  the paragraph opens "For a **planar** layer" and closes "An interleaved layer is
  unaffected".
- R8 (hunk 14): "however it was de-addressed" admits a third means (a planar → interleaved
  layout switch). Dropped because that switch alters every stored tile's decoded size and is
  barred wherever a tile is stored, so the only permitted means are the two named.

## Sweeps (verbatim, flat-copy phrase search; hit counts)

```
### [ignore-lane] hits=14
### [no other] hits=11
### [set any other] hits=1
### [flags = 0] hits=4
### [originates an ignore-lane] hits=1
### [carried by every tool] hits=1
### [independently] hits=3
### [only effect] hits=1
### [drop it] hits=3
### [drop the record] hits=2
### [MAY drop] hits=2
### [licenses the drop] hits=1
### [lets it drop] hits=1
### [declined preservation] hits=1
### [silently deletable] hits=1
### [for no other] hits=1
### [unassigned encoding] hits=3
### [encoding this specification does not assign] hits=0
### [encoding it does not assign] hits=1
### [experimental-range encoding] hits=3
### [experimental-range document encoding] hits=1
### [experimental-range (≥ 0x80) document] hits=1
### [not such a ground] hits=1
### [no content rule attaches] hits=2
### [no rule attaches to its content] hits=1
### [no document rule attaches] hits=2
### [de-address] hits=4
### [dropped out of the addressed set] hits=1
### [Dropping a tile out of the addressed set] hits=1
### [channel being removed] hits=1
### [channel removed] hits=1
### [Removing a channel] hits=1
### [removing one moves] hits=1
### [removing the last] hits=1
### [however it was] hits=1
### [neither does it rescue] hits=1
### [carry no §14 obligation] hits=1
### [carries no §14 obligation] hits=1
### [carrying no §14 obligation] hits=1
### [a shrink is not one] hits=1
### [reaches neither a shrink] hits=1
### [narrowest] hits=4
### [decline the whole file] hits=2
### [does so at the whole file] hits=0
### [on resource grounds] hits=4
### [capability grounds] hits=3
### [capability refusal] hits=1
### [the two capability] hits=1
### [the other two] hits=2
### [reader's own bound] hits=1
### [bound of its own] hits=1
### [resource limit] hits=4
### [narrower scope] hits=0
### [no narrower] hits=0
### [capability or resource] hits=3
### [resource ground] hits=7
### [refuses] hits=5
### [P·Q] hits=10
### [P · Q] hits=2
### [P·Bᶜ] hits=10
### [P · Bᶜ] hits=1
### [C·N] hits=4
### [C · N] hits=2
### [each for the layout] hits=1
### [has no P] hits=1
### [⌈P/8⌉] hits=11
### [the layout gives] hits=1
### [varies by layout] hits=1
### [neither detects] hits=0
### [does not reject the tile] hits=1
### [0x00 as false] hits=1
### [resolves a nonconforming] hits=1
### [as an actor] hits=1
### [never nonconforming by virtue] hits=2
### [conduct rule] hits=2
### [proper prefix] hits=1
### [compared lexicographically] hits=2
### [compares keys] hits=1
### [layer-name byte order] hits=1
### [ties by layer name] hits=1
### [the name, §19.1 step 4] hits=1
### [yields no name field] hits=1
### [leaves unwitnessed] hits=1
### [did not store] hits=2
### [wrong content] hits=2
### [declines to decode] hits=2
### [unregistered] hits=2
### [stored flags are authoritative] hits=1
### [definition it implements] hits=1
### [stored bits never] hits=1
### [the whole file] hits=7
### [cannot establish* grounds] hits=0
### [cannot-establish grounds] hits=1
```

Line-oriented grep controls (hard wrap): `grep -n` for "each for the layout its row states", "which is also the narrowest scope", "which it does for an unregistered record", "of the kind §21.7 leaves unwitnessed", "or a channel removed from a planar layer" each returned 0 lines while the flat-copy search returned 1 hit each — the wrap, not absence. Zeros relied on and their controls: "does so at the whole file" 0 vs "decline the whole file" 2; "neither detects" 0 vs "does not reject the tile" 1; "narrower scope"/"no narrower" 0 vs "narrowest" 4; "encoding this specification does not assign" 0 vs "encoding it does not assign" 1 and "unassigned encoding" 3; "cannot establish* grounds" 0 vs "cannot-establish grounds" 1.

## Derived numbers

register rows 120 instances 277
L2 9
L23 4
L21 4
L44 3
T3 6

§21.8 states "120 conditions over 277 instances" — matches. L2 = 9 instances before and after hunk 18 (labels changed, semicolons not). L23 = 4 (hunk 19 changed Detected only). §21.3 "49 conditions" = L1..L49. §21.6 refusals named after hunk 20: closing paragraph 2 + rows self-labelled "capability grounds" 1 = 3, against [R-ERR-04]'s "the two capability refusals §21.6 names" (X-01). R1 instances = 4 (encoding 0 / reserved × top-level / sub-record). Hunk anchor lines: 23 of 23 verified.
