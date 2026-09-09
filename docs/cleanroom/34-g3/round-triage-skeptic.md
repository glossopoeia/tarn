# Round 34 — triage pass: Skeptic

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only,
in these slices — §1 (14-95), §2.1-2.4 (97-300), §4.7 (594-630), §5.1 (633-700),
§5.2 (696-780), §6.1 (781-830), §6.2 (823-875), §6.4/Appendix F region, §7.2
(998-1015), §7.4 (1102-1175), §9.6 (1441-1490), §9.7 (1488-1545), §11.1
(1638-1682), §15.2-15.4 (2201-2300), §16 (2300-2406), §18.2 (2634-2690), §20.1-20.2
(3104-3146), §20.3 (3146-3420), §20.4-20.5 (3411-3520), §21.1 (3629-3730), §21.2
head (3730-3745), §21.4-21.6 (3830-3965), §21.7-21.9 (3963-4130), §22.3
(4161-4210), §24 (4320-4410), Appendix F and G (4568-4760), Appendix H (4790-4812).
Plus targeted greps for `re-establish`, `no condition a file can exhibit`,
`R-SLB-05`, `F27|F28|L48|L49`.

Did **not** read: any walk transcript, any other triage pass's notes, `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, the web.
I did not list any directory. No orienting listing was run.

Every finding was evaluated. No gaps.

---

## Method

For each finding I looked for the sentence that forecloses it. Where I found one I
quote it. Where I looked and did not find one, I say what I searched for.

Byte-level test applied throughout: *does resolving this change which byte
sequences a conforming implementation may emit, or must accept or reject?*

Byte-level upheld: **0**. That zero is stated with the reasoning below for each,
not as a default.

---

## G1 — `re-established` in the closed list (reader-01, adversary-01, quiz-01)

Three reporters, one defect: §20.3 step 4's closed list gives four verbs for a
slab/alignment declaration — "declared, changed, re-established or cleared as this
step provides below" (line 3217) — and the clause it delegates to gives
"declared, changed or kept ... has its invariants re-established over every run
the new state keeps, or is cleared" (line 3321).

**Search for the deciding sentence.** `grep -n "re-establish"` returns exactly five
sites: 1664 (§11.1 Rationale restatement, declaration object), 2368 ([R-SLB-04],
invariants object), 3217 (the list, declaration object), 3321 (the delegated
clause, invariants object), 4799 (Appendix H restatement, declaration object). No
sentence anywhere defines "re-established" applied to a *declaration*, and the
delegated clause's own third verb is "kept". I looked in §16.2, in [R-SLB-03] and
[R-SLB-04], in §11.1's Rationale and in Appendix H, and found no pairing. **That
absence is the evidence.** CONFIRMED.

**Byte-level: no.** I enumerated the transitions a slab or alignment declaration
can make on a layer that stored a tile: none→some ("declared"); some→different
("changed"); some→none ("cleared"); some→same (the baseline "keeps its
declarations", which the list is carved out of); and the exclusive alignment/slab
switch, reachable as cleared + declared under "A commit MAY make several of these
changes at once". Every transition is licensed under all three candidate readings,
and the new state's legal declaration values are fixed by [R-CNT-16],
[R-SLB-01]/[R-SLB-03] and [R-SLB-04] regardless. The bytes carry only the new
state's values; no field records how the commit arrived at them. Emittable set
identical.

Premise my downgrade rests on, stated for attack: *the exception list's only
normative effect is on the set of declaration values a new generation may carry,
and no reading of "re-established" adds or removes a value from that set.*

Repair: replace "re-established" with "kept" in all three restatements (3217, 1664,
4799), so the list's vocabulary is the delegated clause's; or drop it, since
some→same is the baseline the list is carved out of.

---

## G2 — §20.3's bar and §21.7's classes (reader-02, writer-02) — REFUTED

Both reporters say §20.3 step 4's bar is misfiled under §21.7's "no condition a
file can exhibit" class and belongs in the "unwitnessed" class, because the
superseded generation survives in the file as slack where §9.6's backward probe
would find it.

**This is the group I tried hardest to kill, and I killed it.** writer-02's witness
requires that a file *exhibit* the condition "layer L declares X live and declared
Y≠X, with a tile stored, in the superseded generation". Three sentences defeat it:

1. §16 [R-SLB-05]: "its stored tiles MAY occupy any non-overlapping byte positions,
   in any order ... a byte the live state does not claim is slack whatever produced
   it (§5.2)."
2. §5.2 [R-CNT-21]: "Slack has no internal structure this specification defines,
   its content is unconstrained, and no conformance requirement applies to it."
3. §18.2, on the third member of the same §21.7 class: "the bar on sizing a buffer
   binds a reader rather than the document, **and so states no condition a file can
   exhibit at all**."

Taken together: a *creator*, in a single commit, may emit a byte sequence identical
to the one a bar-violating commit leaves — placement is free, gap content is
unconstrained, so the "superseded trailer and directory" can be written as gap
bytes by a writer that made no prior commit. So the predicate is not a property of
the bytes at all; it is a property of history. That is exactly "no condition a file
can exhibit", and §18.2's own ground (a rule that binds an actor rather than
describing the document states no such condition) is the ground §20.3 states in the
same sentence: "This bar binds the commit as an actor".

§9.6 reinforces: "no verdict turns on the probe ... the earlier state the probe
finds is a different artifact"; "For a verifier the probe is diagnosis ... not a
finding about the file it was given."

Byte-level: no, and both reporters agree — [R-CNF-02] names this bar expressly
("§20.3 step 4's bar on the fixed declarations of a layer that stores a tile are
the cases this text states") and "a file is never nonconforming by virtue of one".

No repair needed.

---

## G3 — Appendix G item 8 vs §20.4's PE = 0 drop (writer-01) — CONFIRMED

Item 8: "A compactor's output is therefore reproducible only modulo its trailer:
[R-WRT-06]'s fresh file_id is no function of content, and this item's floor turns
on which features the compactor implements."

Both named causes are trailer fields. §20.4's MU = 0 / PE = 0 row: "a compactor MAY
drop the record whenever it rewrites the file." §20.5: the output is the live
committed state "less any record §20.4 lets it drop". Two profile-adopting
compactors on one input therefore may differ in the *directory* — and so in
dir_length, downstream offsets, the directory CRC, committed_file_length and F.

**Search for the closing item.** I re-read all ten numbered items and the closing
paragraph. Item 3 pins record *order*, not record *membership*. Item 4 pins one
generation. The closing paragraph's enumeration of what the items add (gap content,
gap extent, record and sub-record order, defaulted fill, the all-fill sentinel, a
single generation, alignment and slab, version_minor, a derived file_id, NFC names,
producer pinning) does not mention retention or the PE bit. I did not find the
sentence. CONFIRMED.

Byte-level: **no.** Appendix G is headed "(non-normative)" and states of itself "It
adds no requirement to any actor: a writer ignoring it is fully conforming."
[R-CNF-01] exempts "appendices identified as non-normative". Both outputs are
conforming and both compactors are conforming.

Repair (maintainer's call): add a profile item requiring retention of every record
the input carries, or narrow item 8's claim to "modulo its trailer and any PE = 0
record §20.4 lets it drop".

---

## G4 — "where a field is on both sides" (writer-04, adversary-02) — CONFIRMED

The fixed list is "Every **other** declaration is fixed ...: the layout, the
linearization and the index encoding, the codec and the filter, the rank and the
dimension order, every tile extent, every channel's type and fill, an interleaved
layer's channel list (its names aside), and the position of every planar channel
the new state keeps." A dimension extent is not in it, and cannot be, since the
list is by construction the complement of the permitted list, where "an extent MAY
grow, and MUST NOT shrink" already sits. So of the three "both sides" examples,
only two are on both *lists*. CONFIRMED as written.

I checked reading (b) — "sides" = permission and prohibition — and it does rescue
the third example, since "MAY grow, and MUST NOT shrink" is both, and "a shrink"
heads the give-up list later in the step. But the sentence's own words are "the two
lists ... on both sides ... the permitted side", which points at the lists.

adversary-02's second half (entry_count, crc_of_crc_array, the extent slot and
sub-records reached by neither list) is **refuted by the same sentence**, which
disposes of all four in its next clause: "entry_count and crc_of_crc_array follow
the commit, the record's extent slot with them (§7.2), and a layer's sub-records
are §20.4's subject whether or not the layer stores a tile." Those are derived
quantities and a containment, not declarations; §7.4 constrains entry_count as
"equals the addressed-tile count", which is not a thing a commit declares.

Byte-level: **no.** The operative claim — "the permitted side states the whole of
what a commit MAY do to it" — is true of a dimension extent under either reading,
and the lists' membership is unchanged either way. Verified field-by-field against
§7.4's table (name, layout, linearization, codec, filter, A, S, A_slab, rank d, C,
each dimension entry's name/extent/tile extent, each channel entry's
name/type/fill, index_encoding, entry_count, crc_of_crc_array, sub-records): every
declaration field is reached by one list or the other.

Repair: drop "a dimension extent" from the parenthesis, or say "on both a
permitting and a barring side".

---

## G5 — the slab half's "kept" carries no trigger (writer-03) — PARTIAL

Claim: §20.3's "a slab declaration declared, changed **or kept** has its invariants
re-established ... or is cleared ([R-SLB-04])" is broader than [R-SLB-04], which
fires only on five named changes.

**Deciding sentence found.** §20's own preamble, line 3108: "This section defines
the writer tiers and their procedures; like §19, **it consolidates — each step
cites the rule whose outcome governs it**." The clause cites [R-SLB-04]; its
trigger list governs. The broad reading is foreclosed by the section's stated
relation to the rules it restates.

So the defect is not that the two readings are both live — it is the asymmetry the
reporter also names: the alignment half is grounded in an unconditional invariant
([R-SLB-01], [R-CNF-05]) and stated at the right breadth, while the slab half is
stated at the same breadth over a triggered writer rule. [R-SLB-03] is equally
unconditional ("When declared, for every run: ...") and would ground the slab half
at that breadth. PARTIAL.

Byte-level: **no.** I walked [R-SLB-04]'s five triggers against every change §20.3
step 4 permits — name change, extent growth (grid count raised or not), planar
channel appended, planar channel shortened, and each slab/alignment verb including
the exclusive switch. Every change that can disturb a slab invariant changes the
run partition, the byte placement of a run, a stored tile's disk ordinal, the
stored-tile set, or the declaration — all triggers. On conforming input the broad
reading is satisfied vacuously. The two readings diverge only on an input already
carrying L41 or L42, where the file is nonconforming under both readings and every
verifier rejects the layer under both; §20.1 [R-WRT-01] separately allows an
appender to carry such a violation forward "seen or unseen".

Premise for attack: *[R-SLB-04]'s five triggers exhaustively cover the inputs to
[R-SLB-03]'s invariant (run partition, A_slab, stored tiles' offsets and lengths,
which tiles are stored), so on a conforming input no untriggered commit can break
it.*

Repair: ground the slab half in [R-SLB-03] and [R-CNF-05] as the alignment half is
grounded in [R-SLB-01] and [R-CNF-05], or attach [R-SLB-04]'s triggers to "kept".

---

## G6 — "the new state keeps" (adversary-03) — PARTIAL

Claim: "keeps" carries two incompatible senses four lines apart.

**Refutation of the incompatibility.** One sense — *present in the new state* —
reads all three uses without contradiction:

- "the position of every planar channel the new state keeps" — under that sense an
  appended channel is included, but it has no prior position for the fixity to bite
  on, so the clause is vacuous for it and false of nothing. The contrast the
  reporter relies on (channels a shortening removes) survives: removed channels are
  not in the new state under either sense.
- "every one the new state keeps, not only those this commit adds" — the appositive
  spells the same sense out, precisely because a reader might assume *retained*.
- "every run the new state keeps" — the same sense, and the one [R-SLB-03] demands.

So the senses are not mutually exclusive; the appositive is a clarification, not a
second sense. What remains is the asymmetry the reporter names in its last
sentence: one half of the sentence carries the disambiguating appositive and the
other does not. PARTIAL.

Byte-level: **no.** [R-SLB-03] is unconditional — "When declared, for every run:
the run's stored tiles are contiguous and packed in ordinal order ... and the first
stored tile's offset satisfies offset mod A_slab = 0" — so a new run that breaks it
makes the layer L41/L42 whoever wrote it, and an appender producing those tiles is
producing the offending bytes and so bound by [R-CNF-05] through [R-CNF-06].

Repair: give the slab half the same appositive, or say "every run of the new
state".

---

## G7 — structural/descriptive actor sets (verifier-01, adversary-04) — PARTIAL

**Deciding sentences found, two of them.**

1. §4.7's opening: "Every field this specification defines is classified by what
   its *value* determines, **each class being what the one before it is not**." A
   partition is asserted by construction.
2. The descriptive definition's operative clause is the *if*: "It is **descriptive**
   if **it determines none of those**". "Those" is the four-alternative gloss on
   "anything a conforming reader **or verifier** does", one alternative of which is
   "whether the file, layer or tile is accepted at all". The colon-introduced text
   ("its value determines nothing a conforming reader does, and a reader MUST NOT
   alter decoding based on it") is an elaboration of the consequence, not a second
   test.
3. Corroboration in §1's Note: "**descriptive** (none of those — §4.7)" — the same
   negation of the whole structural gloss, with no reader/verifier split.
4. And the assignment is closed by name: "In format major 1 `version_minor` is the
   only descriptive field, and every other field this specification defines is
   structural."

So the partition holds and no field is reclassified. What is real is that the
elaborating clause drops "or verifier" where the test carries it, which is loose in
a definition whose whole point is the negation. PARTIAL, editorial.

Byte-level: **no.** The reserved record flag bits are the reporters' witness, and
[R-CNT-12] independently states the only normative consequence the label carries:
"writers MUST emit zero; readers MUST ignore them". Both readings yield identical
reader behaviour, writer output and verifier verdict.

Repair: "its value determines nothing a conforming reader **or verifier** does".

---

## G8 — the coverage walk's incompleteness test (verifier-02) — REFUTED

**Deciding words found, in the passage itself.** §5.2: "The walk is incomplete
where a scope-level rejection **ends that scope's enumeration**" — the participle
is a condition, not a stipulation; the rejection must actually end the enumeration.
§9.7 says it the same way: "a scope-level rejection **blocks** enumeration". And
the operative criterion is stated first and factually: "Where the walk of §9.7 does
not enumerate every region's claimants, the verifier MUST report the total as
partial", with "A partial total is F less the bytes claimed by **the claimants the
walk did enumerate**".

The layer clause is the exception that proves it: "A rejected layer's claimants are
not enumerated, **whether or not the rejection impeded reading them**". A
stipulation had to be stated at layer scope; it is not stated at tile scope, so
tile scope falls to the factual criterion. And §15.3 settles the shape of the
answer for the whole class: an entry whose only defect is a crc failure "keeps its
place in the *verifier* rows, in run continuity, and in the coverage walk", because
"the defect lies in the bytes it addresses, not in the entry, so its extent
stands". The same reason transfers to T3, T4, T14 and the codec rows: the claimant
comes from the index entry, which was enumerated before any decode.

So a T4 tile leaves the walk complete and the total exact. Reading (b) is
foreclosed. REFUTED — with the honest residue that the passage names two tile
carve-outs and could name the criterion once instead.

Byte-level: **no.** The disputed quantity is a line in a verifier's report. The
verdict is *nonconforming* under both readings (§2.3: "An established violation
takes priority"), no reader owes a coverage walk at all (§5.2 Note: "Coverage is
checked by verifiers, never by readers"), and no byte moves.

---

## G9 — Example shape (c) and free re-declaration (diagrams-01) — PARTIAL

**Deciding text found, inside the sentence itself.** "A layer that stored no tile
in the generation the commit supersedes is re-declared freely, subject to every
rule its new declarations are subject to, **which is the same step's permission**"
— the clause labels itself a cross-reference to step 4's permission, not a member
of shape (c)'s taxonomy, exactly as its two neighbours are marked. And the
obligation it would otherwise contradict is unconditional above the figure:
"**Every** layer whose stored-tile set or index content this commit changes has its
tile-index region re-emitted in full ... necessarily at a new placement", with
[R-CNT-17] tying extent_length to entry_count. The block is a labelled *Example*
and so non-normative under [R-CNF-01].

Reading B is foreclosed. What survives is placement: the sentence sits between two
explicitly-negated ones, and a reader scanning the block for its taxonomy can take
it as a fourth member. PARTIAL, figure-level.

Byte-level: **no.** An implementer who reads step 4 cannot emit the L22 file the
reporter describes, and one who reads only the figure emits a nonconforming file
that every reader rejects at layer scope under [R-CNT-17].

Repair: move the sentence out of (c), or mark it as the neighbours are ("is not
this shape").

---

## G10 — §4.7's presentation Note vs §6.1 and §7.2 (diagrams-02) — CONFIRMED

Checked both tables against the Note.

(a) §6.1's table is `| Offset | Size | Value | Class |`. The Note's carve-out is "a
Value column replaces **type and range**" — which leaves *name* standing, and there
is no name column. The document does name those fields elsewhere (F6's Instances
cell: "magic bytes [0,8); reserved bytes [8,16)"). CONFIRMED.

(b) §7.2's table is `| Offset | Size | Type | Field | Class |`. The Note says §7.2
"folds each field's range into its Field cell". Two of five do — "type (0
invalid)" and the flags bit list. inline_length, extent_offset and extent_length
carry no range; their constraints are in [R-CNT-12] and [R-CNT-13]. CONFIRMED.

**Search for the escape hatch.** "each table giving the columns its structure
needs" would license any omission — but the Note's own practice is to state each
omission (§7.4's "omits the offset, size and class columns"; §6.1's "replaces type
and range"), which is why the two unstated ones read as oversights rather than as
exercises of the general licence.

Byte-level: **no.** The Note is labelled *Note* and so non-normative under
[R-CNF-01]; which columns a table prints changes no byte. Every omitted name and
range is stated normatively elsewhere.

Repair: "§6.1's block is a 16-byte constant, where a Value column replaces the
type, name and range columns, and §7.2 folds a field's range into its Field cell
where it has one."

---

## G11 — §18.2's "1 or 2" Valid-values cell (diagrams-03) — PARTIAL

The cell reads "1 or 2; **see below**", and the paragraph directly below gives the
whole set: "0 is invalid; 1 = none and 2 = zstd are assigned; 3 through 0x7F are
reserved; values ≥ 0x80 are the experimental range (§10)." §21.6 records the
experimental case as conforming; R1 registers only 0 and 3–0x7F.

The explicit deferral in the cell is the deciding text — the cell does not claim to
state the value set, it points at the paragraph that does. What is real is the
convention clash the reporter names: §7.4's index_encoding cell spells the whole
set out inline ("any other value — including 0, reserved 2–0x7F, and the
experimental range ≥ 0x80 (§10) — is a validity error at layer scope"), and the two
u8 spaces with experimental ranges are handled by opposite conventions. PARTIAL.

Byte-level: **no.** [R-EXT-03], [R-MTA-10] and §21.6's row decide with one voice,
and R1 registers the violating values.

Repair: make §18.2's cell read like §7.4's, or add "; ≥ 0x80 is conforming and
ignore-record".

---

## G12 — F5's reason clause names the pad (diagrams-04) — CONFIRMED

[R-CNT-27] derives the floor from three components: "the front signature block, a
directory of at least 4 bytes at an offset of at least 16, and the 64-byte trailer
at a 64-aligned offset cannot be satisfied in fewer." F5's Condition cell names
four: "the front block, directory, **pre-trailer pad** and trailer cannot all fit."

The pad is not a component of the floor, and [R-CNT-05] says so: "**a writer that
ends its directory on a 64-byte boundary leaves none**". I checked the reporter's
witness against [R-CNT-06]'s gates: F = 128, dir_offset = 16 (≥ 16), dir_length =
48 (≥ 4), dir_offset + dir_length = 64 = F − 64 (≤ F − 64). Legal, and the pad is
zero bytes. CONFIRMED.

The counter-reading (a zero-length pad "fits" in zero bytes) is real but does not
rescue a derivation, which is read as a list of minimum sizes.

Byte-level: **no.** The condition F5 tests, its outcome, detector and tier are
identical to [R-CNT-27]'s; only the reason clause differs, and §21.1 governs:
"where a row and the rule it cites diverge, **the rule governs**."

Repair: strike "pre-trailer pad" from F5's Condition cell.

---

## G13 — "— F27 and L48" (register-01) — REFUTED

**The punctuation decides.** The parenthetical is a semicolon-separated list of two
rules: "(`[R-CNT-22]`, whose registered type keeps its fixed semantics; **and**
`[R-MTA-05]`, whose unsorted document readers process as they find it — F27 and
L48)". The em-dash citation sits inside the second item, after the semicolon and
the "and". Reading B requires the citation to escape its own list item.

And the document's practice confirms it at §7.1, line 989: "where a rule outside
this quarantine records a document's defect at the file or the layer
(`[R-MTA-05]`, F27, L48), the verifier records it there". F27's and L48's Governing
rule cells read `[R-MTA-05]` (R-CNF-05); F28's and L49's read `[R-CNT-22]`
(R-CNF-05). The pairing is unambiguous.

REFUTED. The residue — that [R-CNT-22]'s rows go unnamed while [R-MTA-05]'s are
named — is cosmetic and costs nothing, since §21.6's closing paragraph names both
rules and both are findable by their Governing rule cells.

Byte-level: no, and the reporter agrees.

---

## G14 — the trailer-mimic entry's reason clause (register-02) — CONFIRMED

§21.6's entry: Condition "**A payload** contains a byte string that mimics a
trailer"; Defined behavior "Inert: **nothing enumerates slack** ...".

A live stored-tile payload *is* enumerated: §9.7 has the walk reach "the stored
extent of each non-sentinel tile-index entry", and §5.2 [R-CNT-02] makes a
stored-tile extent a structure of the live state. So the reason does not fit a live
payload, which is precisely the case the governing rule warns about — [R-LIF-06]:
"**a tile payload** can deliberately contain a byte string that mimics a valid
trailer". §22.3, which the entry condenses, keeps the two apart: "under live-state
coverage **a mimic in slack** is inert — nothing enumerates it". The entry dropped
"in slack" from the reason while widening the condition to "A payload". CONFIRMED.

The entry's second clause ("a recovery tool re-verifies its output whole") does
cover the live case, so the entry's *conclusion* holds; it is the first clause that
is mis-transplanted.

Byte-level: **no.** §21.1: "§21.6's entries restate their governing rules on the
same terms a row does, and where such an entry and the rule it cites diverge, the
rule governs there too." [R-LIF-06]'s obligations on recovery tools are unchanged.

Repair: "Inert: no reader scans backward ([R-LIF-05], §9.5), a mimic in slack is
enumerated by nothing, and a recovery tool re-verifies its output whole (§9.6)".

---

## G15 — §21.9's "which every file and every layer carries" (register-03) — REFUTED

**Deciding sentence found, immediately before the quoted one.** "**Either way a
file containing no instance of a kind does not exceed that row, whatever its
declarations would derive.**" That sentence is stated over *a kind*, not over the
last three rows, so a zero-layer file with no rank, no C and no entry_count is
already covered by it, and no reader may decline such a file on §21.9's ground.

And the quoted clause is not falsified on its face: "declarations, which every file
and every layer carries" distributes — file-level declarations over files,
layer-level over layers — and a zero-layer file vacuously satisfies "every layer
carries". Reading (2), the universal one, is not the grammar.

REFUTED. The residue the reporter identifies is rhetorical: under the distributive
reading the clause supports the contrast less crisply than the paragraph wants. It
costs nothing, since the preceding sentence already generalises.

Byte-level: no, and the reporter agrees.

---

## G16 — "the row is the rule" (register-04) — CONFIRMED

"The **Instances** column enumerates what a conformance corpus builds for that row
(§21.8): **the row is the rule**, and each instance is one file."

Twenty lines earlier the same subsection settles the opposite twice over: "each row
*restates* its governing rule, and where a row and the rule it cites diverge,
**the rule governs**"; and again for §21.6: "where such an entry and the rule it
cites diverge, the rule governs there too." §24 [R-VEC-02] keeps them distinct as
two things a manifest must both record, "recording both ties the vector to the rule
as well as to the row", and [R-VEC-01] makes the corpus derivative.

So the phrase, read as authority, contradicts its own subsection. Read as
corpus-building granularity ("the row is the unit"), it is consistent — and the
sentence's subject supports that reading. But a document that states its tie-break
twice should not then write "the row is the rule". CONFIRMED as an editorial
collision.

Byte-level: **no.** [R-VEC-01] makes a mis-built vector wrong rather than the
document wrong: "where a vector's recorded expectation and this specification
disagree, this specification governs and the vector is corrected."

Repair: "the row is the unit, and each instance is one file."

---

## G17 — "one vector per instance" (register-05) — PARTIAL

§21.8: "has **at least** one conformance vector ... and one vector per instance."
§24 [R-VEC-03], declaring itself the inheritor: "Coverage is the corpus's own
obligation, **inherited from `[R-ERR-02]`**: every register row has **at least** one
vector for each instance it names".

The inheriting statement carries the quantifier and the source drops it. §21.8's
own next sentence frames a floor — "A row without a vector is a gap in the corpus,
not a licence to skip the check" — as does §24's — "A missing vector is a gap in the
corpus and never a licence to skip the check it would have exercised." Nothing
anywhere gives a reason to cap a corpus. The cardinality-cap reading is available
grammatically but is refuted by [R-VEC-03]'s explicit restatement of the same
obligation. PARTIAL: the content is settled, the wording diverges.

Byte-level: **no.** Both rules bind the corpus, and [R-VEC-01] makes it derivative.

Repair: "and at least one vector per instance."

---

## G18 — L44 and the decoded-size parenthetical (adversary-05) — PARTIAL

The sentence: "...but for a decoded size, a padding position or pad bit, or a
boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode
that fails outright under a changed codec or filter (T24, T25), **no check any
actor owes able to see it** (§21.7)."

**Deciding material found, two pieces.**

1. The antecedent of "it" is the preceding clause's subject: "Under new ones **the
   same bytes would denote values, coordinates or padding the writer did not
   store**". The four cited rows all compare *stored bytes* against the newly
   derived decoded size. L44 compares a *derived* decoded size against a constant
   cap and reads no stored byte; it is exhibited identically by a file a creator
   wrote in one commit with those declarations, so it witnesses nothing about the
   change. It does not see "it".
2. §20.3 already cites L44, in the paragraph two below, for exactly the question
   the reporter raises: "A permitted change holds provided the declarations and
   geometry it produces stay within every bound they are subject to:
   `[R-COD-07]`'s lz4 decoded-size cap (**L44**, the largest channel plane
   governing in a planar layer) ... `[R-ENC-04]`'s 2⁶³ − 1 ceiling on every quantity
   it designates". The step handles declaration-bound rows in their own paragraph.

What survives: the parenthetical's phrase "a decoded size ... the register
witnesses" is loose enough to invite the reporter's reading, since L44 is a
decoded-size row and the register does carry it. PARTIAL.

Byte-level: **no.** L44 requires of every reader exactly what it requires under
either reading, and the file's verdict is identical.

Repair: "a decoded size a stored tile's own bytes contradict" or similar, to pin
the category to the tile-scope rows cited.

---

## G19 — T7 vs T11 for a half-sentinel entry (quiz-02) — PARTIAL

The factual claim checks out: §15.2 makes [R-ENC-03] apply "to the fields of
non-sentinel entries only", and a half-sentinel entry is non-sentinel, so §15.3's
"offset > 2⁶³ − 1 or length > 2⁶³ − 1 (non-sentinel)" row does reach an entry whose
one all-ones field exceeds 2⁶³ − 1. Two §15.3 rows reach the same 20 bytes.

**But the register is decided twice over, and the reporter looked at only one of
the two.** T11's own exclusion clause is one. The other is §21.1's specialization
rule, which the reporter mentions and then sets aside on the ground that its
enumerated pairs do not name T7/T11: "Some rows are strict specializations of
others: where every file exhibiting one row's condition ... necessarily exhibits
another's, the file is recorded against the narrower row ... **the property decides
any pair and this list is not offered as closed.**" Every half-sentinel entry
necessarily has a field above 2⁶³ − 1, so T7 is a strict specialization of T11 read
without its clause, and the property records the file against T7. Both routes give
T7.

So the answer is over-determined, not under-determined. What remains is the
reporter's sharpest point, which I confirm: T11's Condition cell carries a
qualification ("the value being distinct from the all-ones sentinel") that neither
[R-IDX-03] nor [R-ENC-03] states, which inverts §21.1's usual row/rule relation —
here the row narrows the rule. PARTIAL, register-bookkeeping.

Byte-level: **no.** Same outcome (reject-tile), same detector (reader), same
detection point (tile use), same structural classification. Only the manifest label
moves, and [R-VEC-02] provides for a file that cannot isolate one row.

---

## G20 — §21.1's rules carry no identifier (quiz-03) — PARTIAL

Factually right: §21.1 is normative under [R-CNF-01] (no *Note*/*Example*/
*Rationale* label, not an appendix), states a completeness rule, a rule-over-row
tie-break and a specialization test, and carries no `[R-<PREFIX>-<NN>]` of its own;
every identifier in it is a citation. Its neighbours each declare one ([R-ERR-01]
through [R-ERR-05]).

**The nearest thing to a deciding sentence.** §2.2 states the convention over
"**Normative requirements**", and §2.1's Note characterises what a requirement is
in this document: "every requirement **names the actor it binds** (writer, reader,
updater, verifier, or file)". §21.1's three clauses name no actor — the
completeness clause is a claim about *this document* ("is a defect in this
document"), and the tie-break and the specialization test are interpretive rules
about how the register's own rows relate to rules stated elsewhere. On the
document's own account of what a requirement is, they are not requirements, and
§2.2's convention does not reach them. That is a real answer, but it is assembled
from a Note, so I grade PARTIAL rather than REFUTED.

Byte-level: **no.** [R-CNF-01] makes the text normative whether or not it is
numbered; only the form of a manifest entry could change, and [R-VEC-02] already
covers a file that exercises more than one row.

Repair (maintainer's decision, not an edit): either give §21.1 an `[R-ERR-NN]`, or
state that the register's reading rules are interpretive and deliberately
unnumbered.

---

## Summary

- Groups: 20. Input ids: 26, each in exactly one group.
- CONFIRMED 7 · PARTIAL 9 · REFUTED 4.
- Byte-level upheld: **0**.
- Tried hardest to kill and failed: **G1** (searched all five occurrences of the
  stem and every restatement; no sentence pairs "re-established" with a
  declaration) and **G3** (re-read all ten profile items and the closing paragraph;
  nothing pins record retention).
- Tried hardest to kill and succeeded: **G2** (§16 [R-SLB-05] plus §5.2's
  unconstrained slack means a creator can emit the identical byte sequence, so the
  condition is not exhibitable) and **G8** ("ends that scope's enumeration" is a
  condition, and the layer counter-factual is stated because it is the exception).
