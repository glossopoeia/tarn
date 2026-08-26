# Round 27 triage — skeptic lens — working transcript

## What I read

Only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, via `grep`
and `sed -n` ranges. No walk transcripts. No directory listings — I opened
nothing by enumeration; every read was a line range of the spec chosen from
the heading index (`grep -n '^#\{1,4\} '`). No `docs/`, `PLAN.md`,
`AGENTS.md`, `conformance/`, `spec/registry.json`, git history, web.

Ranges read: §2 (94–340), §3.2/3.3 (400–430), §5.2 (681–754), §6.3/6.4
(849–930), §7.1/7.2/7.3 (932–1045), §8.1/8.2 (1180–1222), §9.7 (1389–1438),
§10 (1438–1530), §11.1–11.4 (1533–1620), §13.3 (1817–1866), §14 (1864–2060),
§16 (2185–2290), §17.2–17.4 (2311–2500), §18.2 (2516–2690), §19.4
(2892–2975), §20.1–20.3 (2979–3230), §20.4–20.5 (3226–3412), §21.1
(3413–3500), §21.2–21.3 rows (3500–3600), §21.4–21.6 (3596–3720), §21.7
(3718–3796), §21.9 (3796–3884), §22 (3884–3990), Appendices G and H
(4335–4549). Plus targeted greps for `corroborat|declared magnitude`,
`adding a|attaches to`.

## Grouping

23 ids → 16 groups.

- `sec02-allocation-mustnot-vs-decode-buffer`: reader-01, writer-01,
  verifier-01, quiz-01 — one defect, four descriptions.
- `appendix-g5-filter-changes-every-tile`: writer-04, diagrams-02,
  adversary-01 — same sentence, three different fixed-point witnesses.
- `appendix-g10-nfc-different-length`: reader-03, diagrams-03 — same
  sentence, two equal-length NFD/NFC witnesses.
- `specialization-list-omits-f21-f22`: register-01, quiz-03 — same row pair.
- Twelve singletons.

Every id lands in exactly one group; union = the 23 input ids.

## Group-by-group

### 1. [R-SEC-02]'s closing MUST NOT vs the decode buffer (reader-01,
writer-01, verifier-01, quiz-01)

Verified in the file. §22.2 opens [R-SEC-02] with "Decoded tile size is a
function of the layer's declarations alone (§14.2, §14.3), so a reader
allocates from geometry and never from a length embedded in a payload" and
closes it with "A reader MUST NOT size an allocation, fetch, or index walk
in proportion to a declared magnitude it has not corroborated against the
file's actual length".

Skeptic search for a scoping sentence: `grep` shows "corroborated" occurs
**once** in the whole document and "declared magnitude" **once** — both in
that sentence. Nothing defines either term, nothing restricts "an
allocation", and nothing exempts the decoded size by name. §17.2's closing
Note is the opposite of a corroboration: "no bound relates a stored length
to its decoded size in either direction". [R-COD-06] and [R-SER-07] both
positively direct the reader to size from declarations. So the finding is
real: the sentence is unscoped and, read as written, bars what four other
passages require. **CONFIRMED.**

Byte-level? Two reporters claim a verdict fork on a conforming file. I tried
to build that fork and it does not close, because the literal reading leaves
*no* conforming reader for such a file rather than two conforming readers
that disagree:

- §2.5 [R-CNF-10]: "Readers MAY enforce resource limits, but MUST accept any
  conforming file within the minimum guarantees stated in §21's limits
  table."
- §21.9 [R-ERR-04]: "Software that declines **on that ground** a file whose
  every quantity lies within the table is not a conforming reader
  (`[R-CNF-03]`) — the two capability refusals §21.6 names, a foreign format
  major and an unimplemented MU = 1 type, are not this ground".
  That clause enumerates the *only* non-resource refusals the document
  admits; a refusal grounded in [R-SEC-02] is neither of them.
- §3.2 [R-MDL-02]: "a conforming reader that reads any portion of a layer
  MUST return exactly the corresponding portion of the reference array".
- §2.3 [R-CNF-11]: *cannot establish* is available only "where some
  requirement is one it is unable to check on a capability or resource
  ground" — so verifier-01's "conforming vs cannot establish" fork also
  fails: a verifier refusing on [R-SEC-02] grounds has neither ground
  available and cannot report cannot-establish either.

Both witness files (writer-01's 190.7 MiB tile in a ~512-byte file;
verifier-01's exactly-256 MiB tile in a 1,280-byte file) are inside every
§21.9 row — I checked rank, C, entry_count, layer count, dir_length, decoded
tile size, and Window_Size against the table, and [R-COD-07]'s lz4 cap does
not apply at codec 3. So [R-CNF-03] MUST-accepts and [R-MDL-02] MUST-serves
both. The accept/serve verdict is therefore fixed under **both** readings;
what the literal reading produces is an unsatisfiable requirement set, not a
second permitted behaviour.

**Premise of the downgrade, stated so it can be attacked:** that a reading
under which the reader requirements are jointly unsatisfiable is not a
"permitted reading" for the byte-level test, and that the test's "a
conforming implementation" excludes a reader that refuses. If the gate
instead counts "an implementer who applies the last sentence as written
builds a rejecting reader" as a fork regardless of that reader's
conformance, this is byte-level. Two of the four reporters took that view.
I record that this is the group I fought hardest and the one a reconciler
should weigh first.

Repair: bound the MUST NOT to magnitudes that determine how many of the
file's own bytes a reader fetches, walks, or buffers (offsets, lengths,
extents, entry counts), and say expressly that a decoded size is governed
by [R-SER-07] and bounded by §21.9's per-tile guarantee instead.

### 2. Appendix G item 5's closing universal (writer-04, diagrams-02,
adversary-01)

Text verified: "…elsewhere it changes the stored bytes of every tile it
touches." [R-COD-10] defines a *permutation of byte positions*; a
permutation fixes any image invariant under it. All three witnesses check
out under `i·n + j` with s = n = 2 (the permutation transposes offsets 1 and
2 and fixes 0 and 3):

- adversary-01: all-zero image `00 00 00 00`, fill 0x0001 so item 6 does not
  sentinel it — fixed.
- writer-04: `00 01 01 00` — fixed.
- diagrams-02: `AA BB BB CC` — fixed.

Non-normative: Appendix G's heading says so, its opening says "It adds no
requirement to any actor: a writer ignoring it is fully conforming", and
[R-CNF-01] exempts "appendices identified as non-normative". [R-COD-10],
which is normative, makes no such claim. **CONFIRMED, editorial, not
byte-level.**

### 3. Appendix G item 10's "a different length" (reader-03, diagrams-03)

Text verified. The `température` clause sits between em-dashes as
illustration and the "so …" conclusion is drawn from the general claim, so
the general reading is the grammar. Both witnesses hold: U+1E00 (NFD
`41 CC A5`, NFC `E1 B8 80`, three bytes each) and the pure
canonical-reordering case `61 CC 81 CC A7` → `61 CC A7 CC 81` (five bytes
each, no composition available). Item 10's actual advice survives, since
[R-ENC-13] decides name identity on raw bytes and those differ. Same
non-normative quotations as group 2. **CONFIRMED, editorial, not
byte-level.**

### 4. §14.4's Note on single-channel bool layers (reader-02)

[R-GEO-01] requires only Tᵢ ≥ 1, so a rank-1 layer with T = (1) gives P = 1
and ⌈1/8⌉ = 1 = P. [R-SER-05]: "Every pad bit (§14.3) MUST carry the plane's
channel's fill bit." With fill false the planar byte is 0x00/0x01 and the
interleaved byte is 0x00/0x01 — byte-identical, which the Note says cannot
happen. With fill true they differ, so the Note is silently fill-dependent.
Note text is exempt under [R-CNF-01] and §14.2/§14.3 fix both images
regardless. **CONFIRMED, editorial, not byte-level.**

### 5. May an appender originate an ignore-lane flag bit? (writer-02)

Searched for a sentence binding an appender. [R-CNT-08]'s MUST is scoped to
"a writer creating a file under this text"; §20.1 defines creator as the one
that "emits a complete file in one commit" and appender as extending "an
existing file by commits". The compactor sentence — "A compactor, though its
output is a new file, carries the input's unknown ignore-lane bits into its
output trailer rather than writing flags = 0" — shows the drafters read
"creating a file" as producing a new file, which an appender does not do.
§10.2 expressly keeps the flag lanes out of the assigned/reserved/
experimental partition ("the trailer's flag lanes, which §6.3 partitions
instead"), so §10.3's "a value from a reserved range MUST NOT be emitted at
all" does not reach a flag bit. §20.3 step 6's enumeration ("unknown
ignore-lane flag bits copied forward") governs those bits, not the field.
Nothing decides it. **CONFIRMED.**

Byte-level downgrade quote — §2.3 [R-CNF-02]: "File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or
environment… A writer obligation whose violation this specification
expressly declares not to be a file-conformance violation binds the actor in
the same way; §6.3's flags = 0 against a set ignore-lane bit … are the cases
this text states." §21.6 agrees: "An ignore-lane flag bit (16–31) is set |
Ignored; the file is conforming". The disputed trailer is a conforming file
under both readings, every reader ignores the bit, every verifier certifies.
**Premise:** I read the test's "which byte sequences a conforming
implementation may emit" as *the set of conforming files*, not *which actor
may produce which file from which input*; the document itself removes this
obligation from the byte predicate. Attack it by insisting on the
actor-relative reading.

### 6. §20.4's PE = 0 drop licence and an *added* top-level record
(writer-03)

Grepped for any further sentence about adding a non-layer top-level record:
there is none — the only "adding a" in the document is the layer-set gloss
in this same cell. The asymmetry is real: the first qualifying item names a
set ("the file's layer set") and gets an express gloss for additions, while
the third names an individual record ("another *non-layer* top-level
record") and gets none, and the express carve-out covers only *drops*.
Nothing resolves it. **CONFIRMED.**

Byte-level: no. Both candidate outputs are conforming files ([R-CNF-02]:
pure predicate on bytes), and §21.7 [R-ERR-01] puts this class of obligation
outside any file-level witness — "properties of a file's history, which §9.7
does not reconstruct". No reader or verifier verdict moves. Same premise as
group 5, stated there.

### 7. [R-MTA-10]'s reporting MUST — every unassigned encoding, or only the
experimental range? (adversary-03)

The conflict is between normative texts, which is why it survives. §22.3
[R-SEC-04] says "the extent of a user-metadata record under an **unassigned**
encoding … which is why `[R-MTA-10]` makes the verifier's report name each
such record". §21.6's row and Appendix H state the duty for the experimental
case only, Appendix H adding "encoding 0 and the reserved range stay
violations (R1)". §21.5's preamble cuts toward the wide reading — "what
`[R-MTA-10]` withdraws is the document's content rules, never the encoding
byte's own value set" — while the MUST's own sentence is conditioned on "in
an otherwise conforming file", which an R1 file never is. I could not find a
sentence that settles it. **CONFIRMED.**

Byte-level: no. §2.3 [R-CNF-11]: "that per-requirement report constrains the
report and not the verdict". R1 fixes the verdict as nonconforming either
way and [R-MTA-03]/[R-CNT-25] fix the reader outcome as ignore-record.

### 8. [R-MTA-10]'s "counted and named, never silent" (verifier-02)

Two premises of the finding fail on checking.

(a) "counted by nothing". §9.7 [R-LIF-08] enumerates *every* record extent
as a claimant of the coverage walk — "the directory itself, each record's
extent, and the stored extent of each non-sentinel tile-index entry" — and
"checks that these occupy disjoint byte ranges, that each lies within
[16, F − 64), and that each verifies against the checksum covering it,
**where §8.1's map states one**". So an unassigned-type extent is walked,
bounded, and excluded from slack; what it is not is *named in the
certificate*.

(b) the general-duty reading. §22.3 [R-SEC-04] takes up exactly this class
in its own list of "Four residues … stated rather than defended": "The
extent of a record of a type this specification has not assigned is covered
by no checksum either (§8.1), so corruption inside it is equally invisible…
nothing an updater does would surface the damage." In the *same requirement*
it says of the unassigned-*encoding* class "which is why `[R-MTA-10]` makes
the verifier's report name each such record". The document therefore
considered both classes side by side and imposed the naming duty on one
only. Reading (1) is foreclosed.

What survives is that the closing gloss overstates as a free-standing
principle. **PARTIAL, editorial, not byte-level.**

### 9. §20.4's MU = 1 row, "Compaction is barred on the same ground"
(diagrams-01)

[R-WRT-06] settles the operation: "A compactor MUST refuse to compact a file
carrying **any** record whose type it does not implement with MU = 1: such a
type can define references this specification does not (§7.2), so its bytes
cannot be safely relocated." §7.2 treats sub-records as records (its
truncation rule assigns "reject-layer for a layer record's sub-record
sequence"), and §20.5 restates the bar as "an MU = 1 type the compactor does
not implement never reaches this step (`[R-WRT-06]`)". The cell cites the
rule. So the compaction question is decided and reading (i) has no
implementation consequence. What is genuinely wrong is the reporter's
closing observation: "the same ground" misdescribes [R-WRT-06], whose ground
is unsafe relocation of undeclared references, not reject-file.
**CONFIRMED as an editorial misdescription, not byte-level.**

### 10. §21.6's sentinel row (diagrams-04)

The cell reads "every sample position it carries reads as the channel's
fill" against [R-TYP-08]'s "a reader that returns any of the tile's sample
positions **inside the layer's extents** MUST return, **for each channel the
tile carries**, that channel's fill value". Both qualifications are dropped;
the singular is positively wrong for an interleaved tile of three channels.
Decided in advance by §21.1: "§21.6's entries restate their governing rules
on the same terms a row does, and where such an entry and the rule it cites
diverge, the rule governs there too." The extents half is further blunted by
[R-GEO-04]'s unconditional "a reader MUST NOT return padding positions as
samples" and §13.3's own Note ("a reader never returns padding positions in
any case"), so "reads as fill" never becomes "is returned".
**CONFIRMED, register-bookkeeping, not byte-level.**

### 11. §21.1's specialization list (register-01, quiz-03)

F21 ("carries extent slot (0, 0)") and F22 ("extent_length is less than 5")
both take reader/open/reject-file; L10 and L11 both take
reader/layer access/reject-layer — verified in the row tables. 0 < 5, so
F21 ⊆ F22 as written and §21.1 names neither pair.

Skeptic's best counter, which the reporter offered as reading (b) and
rejected: §7.2 defines "The extent slot (extent_offset, extent_length):
(0, 0) means **no extent**", so [R-CNT-25]'s second disjunct — "or **one**
whose extent_length is less than 5" — can be read as ranging over extents
that exist, i.e. nonzero slots. That reading is undercut by the same
sentence calling the first case "An extent of (0, 0)". Either branch leaves
a defect: on (a) §21.1's list is incomplete, on (b) F22's and L11's row
wording is. **CONFIRMED**, with the note that the cleaner repair is
probably (b) — qualify F22/L11 (and [R-CNT-25]'s second disjunct) to a
nonzero slot — rather than extending §21.1's list.

quiz-03's extra pair is inexact: F30 ("exactly one half zero") also covers
offset 0 with length ≠ 0, whose length may be ≥ 5, so F30 and F22 partially
overlap and neither contains the other. register-01 records that correctly
as an overlap rather than a containment.

Byte-level: no. Identical outcome, detector and detection point on each
pair; the file is nonconforming under every attribution and [R-CNF-05] bars
emitting it.

### 12. R3 / R4 (register-02)

R4's instance list opens with "missing frame magic, top-level extent", and
its stated ground is "a constraint of this row is broken by what the frame
declares rather than by whether the bytes decode, so a reader that only
tries decoding establishes none of them". A magic-less extent under encoding
2 fails in every zstd decoder, so a reader that only tries decoding does
establish a failure — and R3's condition ("stored bytes fail to decode under
its declared assigned encoding") is satisfied verbatim, with a carve-out
only for unassigned encodings. §18.2's separating sentence — "A mismatch is
one of the frame constraints R4 registers, not a failure to decode under R3:
the bytes decode" — is expressly about the *content-size* mismatch and does
not reach missing magic or a nonzero dictionary ID. Nothing routes those.
**CONFIRMED, register-bookkeeping, not byte-level** (both rows are
violations taking ignore-record at extent use; §21.5's preamble: "Every row
here is a violation all the same").

### 13. F21's gloss (register-03)

§7.1: "Each user-metadata record carries its document in its extent —
**never inline** — and declares the document's encoding in its own inline
payload (u8…)", and [R-MTA-03] makes any inline_length ≠ 1 a validity error
(F23). So "placing its document inline" names a state the framing makes
unrepresentable. L10, the layer-scope twin, carries no such clause and is
the model wording. **CONFIRMED, register-bookkeeping, not byte-level**
(§21.1 makes [R-CNT-25] govern; slot (0,0) is reject-file either way).

### 14. §21.4's outcome header (register-04)

Header: "Outcome: reject-tile — that tile's read reports failure, and never
returns fill in place of data (`[R-CNF-09]`)". [R-CNF-09] is qualified:
"…from a scope this specification rejects **and whose rejection this reader
is obliged to detect** (`[R-RDR-02]`)". T2, T4, T5 and T26 carry Detector
*verifier* — verified in the table. §21.1 forecloses the harmful reading in
advance and even names the case: "For a row whose Detector is *verifier*,
the outcome names the scope at which the damage is recorded, not an
obligation on any reader: the governing rule states what a reader does…
`[R-SER-08]` is the one rule that goes the other way: it resolves a
nonconforming interleaved boolean byte to a value rather than serving it
through." The header's unqualified restatement is nonetheless a real
imprecision. **CONFIRMED, register-bookkeeping, not byte-level.**

### 15. Appendix G item 3's leading gap — REFUTED (adversary-02)

This is the second group I tried hardest to kill, and here I succeeded. The
item's own clause names its source: "…and every byte of every such gap is
zero — `[R-CNT-03]`'s advice, **taken as a requirement here**". [R-CNT-03]'s
advice is scoped in §5.2: "Writers SHOULD zero the gaps they create — **the
run before an aligned tile or slab run**, and the pre-trailer pad."

The leading run is nonempty only "where a declared alignment admits no
structure at 16". §16.1 [R-SLB-01] constrains only stored tiles' offsets and
§16.2 [R-SLB-03] only a run's first stored tile — no declaration constrains
the offset of a tile-index region or a record extent. So the structure that
displaces the first offset above 16 is always an aligned tile or a slab
run's first tile, i.e. exactly "the run before an aligned tile or slab run".
The profile adopts that advice by name, so the leading run is required to be
zero under either antecedent for "such gap". No hole. Severity none.

### 16. §20.3 step 4's list vs a channel reordering — REFUTED (quiz-02)

The paragraph subordinates its own enumeration in terms: "The test is the
effect on such a tile, and **the list names where that effect arises rather
than standing on its own**". §14.1 [R-SER-01] fixes that "value k of the
sequence is channel (k mod C)'s value", so reordering the channel
declarations alters "how they decode" for every prior-generation stored
tile, and the general test bars the commit. The reporter reaches the same
conclusion. Adding "the byte offset of any channel's value" to the list
would be a nicety, not a repair. Severity none.

## Coverage

23 input ids, 16 groups, each id in exactly one group, no duplicates.
byte-level count: 0.
