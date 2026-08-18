# Round 10 triage — correctness lens

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full, section by section:
  front matter; §2.1–§2.5; §4.2, §4.5, §4.6, §4.7; §5.2; §6.1–§6.4; §7.1–§7.4;
  §9.3–§9.7; §10.1–§10.4; §11.1–§11.2; §13.1–§13.3; §16, §16.1, §16.2; §17.2, §17.3;
  §18.1–§18.4; §19.1–§19.4; §20.1–§20.5; §21.1–§21.9; §24; Appendices A, B, C, F, G, H.
- I ran two mechanical checks against the file: `grep -n "verdict"` (to test register-02's
  sweep claim) and a count of `| verifier |` rows in §21.3 and §21.4 (to test quiz-03's
  enumeration). Both are recorded below.
- I did **not** read the round-9 transcripts in `scratchpad/round10/`, `docs/`, `PLAN.md`,
  `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or the web.

## Method

For each finding: locate the quoted text in the file, check the quotation is accurate and
in context, check the cited section says what the reporter says, and test whether the
reporter's second reading is actually licensed by the words. Where I downgrade a
byte-level flag I record the sentence that decides it.

---

## Group 1 — front-block residency gloss (reader-01)

Text at §6.1:

> That distinction governs the request accounting of §6.4 and nothing else; the obligation
> over the front block turns on residency instead...
> A reader whose open leaves bytes [0, 16) **resident** — a local file, a memory mapping, a
> speculative suffix window that reached offset 0, or any transport already holding them —
> ... MUST verify ... A reader that would have to issue a further range request to obtain
> those bytes MAY defer or omit the check ... **The test is residency, not transport, so an
> implementation decides it at its own open path without having to classify the network
> underneath it.**

Quotations accurate. The defect is real: "a local file" is a *transport* classification
sitting as the leading item in a list glossing *residency*, in a rule that twice disclaims
transport as the test. A pread-only local open does not leave [0,16) resident.

But the rule decides its own tie-break, in its last sentence: **"The test is residency, not
transport, so an implementation decides it at its own open path."** A pread-only open path
leaves the bytes non-resident, so the reader falls under the MAY. Both restatements agree:
§19.1 step 1 glosses residency with only "a speculative suffix window that reached offset 0
included", and F6 reads "the obligation binds a reader holding those bytes resident, and a
reader that would have to fetch them MAY defer or omit the check". Appendix A is
non-normative and self-qualifies ("which `[R-CNT-04]` requires of any reader holding them"),
and its own second half says "bytes [0, 16) stay non-resident, so §6.1 leaves the
front-block check to the reader" — i.e. Appendix A itself applies literal residency.

Byte-level downgraded on that quotation. Additional independent ground: the disputed file
(byte 0 = 0x88) is nonconforming, and `[R-CNF-12]` says "For a nonconforming file no
acceptance obligation exists — a reader MAY reject it upon detecting any violation", so
reader A is conforming under either reading; only reader B's status is at issue, and the
residency sentence settles it.

Grade: PARTIAL, editorial. Repair: strike "a local file" from the gloss (or replace with
"a local file read whole"), since the list is meant to enumerate open paths, not transports.

## Group 2 — compaction and §16's declared invariants (reader-02, quiz-02)

Same defect: §20.5 grants placement freedom bounded only by §5.2 and never cites §16,
while §20.2 and §20.3 both state the invariant obligation explicitly.

quiz-02 flags byte-level; reader-02 does not. The document decides, in three quotations:

- `[R-WRT-06]`: "**Given a conforming input the output is a conforming file.**" An output
  layer declaring A with unaligned tiles is nonconforming (L40; `[R-SLB-01]`: "A verifier
  MUST check the invariant (violation: reject-layer)"). So quiz-02's reading (3) is barred.
- `[R-WRT-05]`: "an updater MUST re-emit byte-identically — header, inline payload, and
  extent slot — every record it retains and does not logically modify", and `[R-WRT-07]`'s
  exception list is exhaustive over what may differ: "except that relocation re-points
  extent slots, regenerates each relocated tile-index region ... and updates the
  layer-record fields covering a regenerated region (crc_of_crc_array)". S, A_slab and A
  are not in it, so quiz-02's reading (2) — clear the declaration — is barred.
- `[R-SLB-04]` binds "A writer or updater whose commit supersedes a stored tile in, or grows
  the extents of, a slab-declared layer" — a whole-file rewrite is neither, so its
  clear-the-declaration escape does not reach a compactor.

Only reading (1) survives. Byte-level downgraded. Grade CONFIRMED (the omission is real),
editorial. Repair: one clause in §20.5 citing `[R-SLB-01]`/`[R-SLB-03]`, as §20.2 does.

## Group 3 — Appendix G item 3's emission order (reader-03, writer-07, quiz-05)

One defect described three ways: (i) whether "then any record extents" sits inside the
per-layer loop, and (ii) that "ascending record order" gives no tie-break among the several
type-0x0002 extents a file can carry (one file-scope plus one per layer). Both are real on
the text; the sub-record ordering sentence governs sub-record placement *within a layer
record's inline payload*, not extents in the file. Appendix G is non-normative and says
"It adds no requirement to any actor: a writer ignoring it is fully conforming", so no
byte-level. CONFIRMED, editorial.

## Group 4 — Appendix G item 2's file_id derivation (reader-04, diagrams-02, quiz-06)

One defect: item 2 is not computable as stated. Missing: the hash function and version, the
64-bit reduction, the exact trailer bytes fed in (and whether the trailer CRC is among "the
trailer's other fields" — it cannot be, being computed over bytes containing file_id, and
no recompute step is stated), the concatenation order, and a fallback when the reduction
yields zero against §6.2's file_id ≠ 0. Contrast items 1 and 9, which close their freedoms
by naming the producer at a version. Non-normative → not byte-level. CONFIRMED, editorial.

## Group 5 — §18.4's §21.7 citation (reader-05)

> ... enforcing them would put a verifier to work on the content of metadata, which §21.7
> excludes by design. `[R-MTA-07]`

Checked §21.7: its subject is sample content ("A writer that emits well-formed structures
carrying wrong sample values — a mis-strided filter, an undisclosed compression dictionary,
or simply wrong data"), and its stated ground is "no file-level witness exists to check".
It says nothing about metadata. Meanwhile F27 and L48 assign a verifier the job of decoding
a user-metadata document and comparing decoded keys' UTF-8 bytes at every nesting depth,
and Appendix H lists "user-metadata member ordering (`[R-MTA-05]`, §18.2)" among the
verifier's checks. So the citation is wrong on its own terms, and the ground for
`[R-MTA-07]`'s outcome is §21.6's non-violation row, not undetectability. Normative half is
unambiguous ("Neither placement nor value shape bears on validity"), so no byte-level.
CONFIRMED, editorial.

## Group 6 — §20.4/Appendix H summaries omit the layer-scope metadata sub-record (reader-06)

§7.3 registers type 0x0002 with scope "file when top-level; layer as sub-record" and
PE = 1. §20.4's governing sentence — "both registered types carry PE = 1, so neither can be
dropped" — therefore reaches a layer's user-metadata sub-record. The summary sentence "No
commit therefore removes a layer record or a file-scope user-metadata record" and Appendix
H's "never removes a layer record or a file-scope user-metadata record" both omit it. The
governing sentence decides, so not byte-level. CONFIRMED, editorial.

## Group 7 — `[R-WRT-07]` conditions regeneration on relocation (reader-07)

Accurate reading of the text. The trigger should be that entry offsets change. Decided
elsewhere by the same requirement's closing sentence ("The output's reference arrays MUST
equal the live generation's bit for bit") plus `[R-WRT-06]`'s "Given a conforming input the
output is a conforming file" — an index addressing the input's tile offsets denotes
something else and breaks coverage. Not byte-level. CONFIRMED, editorial.

## Group 8 — scope of the "only supersedes a layer's tiles" caveat (writer-01, quiz-01) — BYTE-LEVEL

> An appender may drop it only in a commit that *independently* changes the scope the record
> attaches to: for a layer sub-record, that layer's record, index, or stored tiles; for a
> top-level record, the file's layer set or another *non-layer* top-level record — a commit
> that only supersedes a layer's tiles is not such a change, though it re-places that
> layer's index region (§20.3, `[R-WRT-04]`).

Two reporters, working independently, both attached the em-dash clause to the top-level
branch alone (reading A) and both flagged byte-level. I read the clause as global (reading
B), because "though it re-places that layer's index region" answers an objection that can
only arise from the sub-record branch — "index" appears nowhere else in the sentence — and
because under A the clause does almost no work (a tiles-only commit obviously does not
change "the file's layer set").

But A is not barred. It leaves every word of the sub-record branch its plain meaning, while
B requires "index" and "stored tiles" to mean *set* changes (added tiles, tiles becoming
unstored) rather than content changes — a distinction §20.3 step 4 does draw ("tiles this
commit stores or supersedes", "tiles that become unstored", "entries new to this
generation") but §20.4 never states. I could find no sentence anywhere in §20 or §2.3 that
picks a branch. `[R-CNF-06]` binds the updater to §20.4's preservation obligations without
glossing this one.

Consequence, and why I did not downgrade: for the most routine commit in the format —
supersede one stored tile of a layer carrying an unknown MU=0/PE=0 sub-record — appender A
emits a directory in which that layer record's inline payload is shorter by the sub-record's
length, with different inline_length, different dir_length, different directory CRC,
different trailer, and the sub-record's extent fallen to slack; appender B emits it intact.
Both outputs are conforming *files*, so no reader or verifier verdict forks — but exactly
one of A and B is a conforming updater, and the brief's test is which byte sequences a
conforming implementation may emit. That set differs. No register row witnesses it, so
nothing downstream catches the wrong choice; the loss is silent application state.

Grade: CONFIRMED, byte-level. Repair (maintainer decision, then one sentence): state
explicitly whether a tiles-only commit licenses dropping that layer's MU=0/PE=0 sub-record.
If the intent is B, move the caveat to its own sentence and say "for either branch"; if A,
move it inside the top-level branch and drop the index-region concession, which then has no
referent.

## Group 9 — Appendix G item 3's zeroing does not reach the pre-trailer pad (writer-02, verifier-04)

"such a gap" is anaphoric to "a gap [a] **declared** alignment forces", and a declared
alignment in this format is §7.4's A or A_slab. The pre-trailer pad is forced by §6.2's
64-alignment and `[R-LIF-02]` step 5, neither of which is declared. Under item 5's own
recommended branch ("No declared alignment and no slab") there are zero alignment-forced
gaps, so the zeroing clause has no referent at all while the pad is still 0–63 bytes.
The appendix's closing paragraph implies the broad reading — it claims the profile adds
"gap *content*, which `[R-CNT-03]` only advises", and `[R-CNT-03]`'s scope is "the run
before an aligned tile or slab run, **and the pre-trailer pad**". Non-normative, and §5.2
makes slack content unconstrained, so not byte-level. CONFIRMED, editorial.

## Group 10 — Appendix G leaves the metadata storage encoding and zstd producer unpinned (writer-03)

Checked §18.2: encodings 1 (none) and 2 (zstd) are both assigned and the choice is the
writer's; §10.2's table lists "codec (§17.2)" and "metadata encoding (§18.2)" as separate
identifier spaces, so item 1's "a named codec implementation at a named version" does not
reach §18.2. Item 9 pins only the JSON writer while claiming "this degree of freedom closes
the same way item 1 does, by pinning the producer". Two profile-followers can differ in the
encoding byte, the extent bytes and length, the terminal extent CRC, and dir_length; and
under encoding 2 the zstd producer is unpinned. Non-normative → not byte-level.
CONFIRMED, editorial.

## Group 11 — §4.7's field taxonomy (writer-04, diagrams-03, adversary-03, quiz-04)

One defect, four descriptions: the trichotomy is asserted exhaustive ("each class being what
the one before it is not") but does not classify several fields consistently with the tables
that print a Class column, and does not determine a class for the name fields §4.7's own
Note pushes into it.

- `generation`, `file_id`: labelled semantic in §6.2. Neither determines "what decoded
  values mean" — two files differing only in them decode identically. Nor are they
  descriptive, since `[R-LIF-03]` makes reader behaviour turn on both ("different file_id or
  lower generation, treat as a different file").
- trailer `reserved`: labelled structural although it locates and decodes nothing; §4.5 says
  "comparing a field against a constant for validation is not acting on it".
- names (layer, dimension, channel): §7.4's table omits the class column and §4.7 says "each
  field's class follows from the definitions above"; a name locates no byte, gives no decoded
  value a meaning, and is not inert (`[R-ENC-15]` makes a duplicate reject-file). And
  `[R-ENC-16]`'s trailing sentence ("Each descriptive field's definition states what a reader
  does when the field contradicts the data it describes") has no referent for a name, which
  describes no data. `version_minor` is the only field the document labels descriptive and
  the only one for which that sentence has content.

Not byte-level: the classes carry exactly one operative consequence, "a reader MUST NOT
alter decoding based on it", and no rule anywhere lets decoding turn on any of these fields.
CONFIRMED, design-decision — the maintainer has to decide whether identity/gate fields get a
class, a fourth class, or an explicit carve-out, before the labels can be corrected.

## Group 12 — flag authority for an implemented but unregistered type (writer-05, adversary-02)

The split is exhaustive over {registered} ∪ {not implemented}; the third cell —
implemented-but-unregistered — is reachable (§21.6: an experimental-range type with MU = 0
is conforming) and has no stated flag authority, and `[R-CNT-22]` shuts the stored-flags
door: "Stored flag bits are authoritative **only** for record types the consuming tool does
not implement."

adversary-02 flags byte-level, claiming U1 (drop) and U2 (retain) are both defensible.
Downgraded, on the table's own scoping sentence:

> **For a type the updater does not implement, the stored flags are authoritative** (§7.3,
> `[R-CNT-15]`; MU = 1 with PE = 0 is read as PE = 1, `[R-CNT-12]`), **and carry these
> obligations:**

The MU=0/PE=0 drop permission lives inside that branch, so it is not available for a type
the updater *does* implement. With no drop permission, `[R-WRT-05]`'s default governs: "an
updater MUST re-emit byte-identically — header, inline payload, and extent slot — every
record it retains and does not logically modify, **whether or not it implements the record's
type**." And §20.4 states the principle outright: "implementing a record's type confers
understanding of it, not permission to drop it." U1's reading requires reading the table
outside its own preamble. writer-05 reached the same answer.

CONFIRMED that the cell is unaddressed; byte-level false; editorial. Repair: one clause
after the two cases saying that a type the updater implements but §7.3 does not register is
retained, no drop permission being granted for it.

## Group 13 — no stated appender counterpart to §20.5's refusal rule (writer-06)

Real gap: §20.5 tells a compactor to refuse; §20.3 tells an appender nothing. But the
reporter's chosen reading (y) — proceed — is barred:

- `[R-WRT-01]`: "a violation latent in a structure they **neither modify nor rely on**
  travels with it".
- `[R-WRT-03]`: "the trailer and the full directory always — **re-emission (§20.4) relies on
  every directory byte**." So a directory record is always relied on, and the travel clause
  never reaches it.
- `[R-CNF-05]`: "A writer MUST emit only conforming files", with `[R-CNF-06]` binding the
  updater to "every writer requirement for the bytes it produces".

So an appender that has detected a directory-record violation must refuse. PARTIAL — right
that the rule is unstated, wrong about which way it resolves. Not byte-level (the reporter
agrees; and the input is already nonconforming). Editorial: state the appender's counterpart
in §20.3, or scope `[R-WRT-01]`'s travel clause explicitly.

## Group 14 — "region" is undefined in `[R-CNT-21]`'s partial slack total (verifier-01, adversary-01)

One defect, two attacks. "Region" carries no defined sense; §9.7 describes the walk as an
enumeration of *claimants*, not a traversal of byte ranges, so "the bytes no claimant claims
within the regions the verifier did walk" is either vacuous (claimant-set reading: zero),
contentless (whole-remainder reading: equals the full total), or undefined (the intended
coarse-range reading, for which the document states no way to establish that a range is
fully accounted — and `[R-SLB-05]` scatters claimants, so there is no honest prefix).

The companion MUST — "name the regions it did not walk and report their byte extent" — is
undischargeable in a concrete case: after L37 (crc_of_crc_array mismatch), `[R-ENC-05]`
bars the verifier from acting on the untrusted index, so it cannot state how many bytes that
layer's stored tiles occupy; after stopping at F26 it has no byte range at all for the
extents it never read. §5.2's own Note licenses the partial total to be "a fact about that
run and not about the file's live state", which softens the first half but not the second.

Not byte-level: the number is a report field and the verdict is fixed before it is computed
(`[R-CNF-11]`, `[R-CNF-12]`). But §5.2 calls the total "what tells an operator to compact"
and §22.3 "the number that distinguishes a working file from a padded one", so two conforming
verifiers printing different numbers is a real cost. CONFIRMED, design-decision: define
"region", and either bound or drop the extent-naming MUST for the cases where it cannot be
discharged.

## Group 15 — experimental-range metadata encoding and the verifier's verdict (verifier-02)

The file is conforming (§21.6: "A user-metadata record declares an experimental-range (≥
0x80) document encoding | Ignored (ignore-record); the file is conforming"). The competing
sentence is `[R-MTA-09]`'s "A verifier that declines to decode a document cannot establish
that document's conformance and MUST NOT certify the file."

Downgraded on `[R-CNF-11]`'s enumeration of when the third verdict is available:

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or *cannot
> establish* — **the last where some requirement is one it is unable to check on a capability
> or resource ground**

An unassigned encoding is neither. `[R-MTA-09]`'s decline sentence sits inside the
resource-bound paragraph and names its own subject two clauses later — "**the bound** is that
verifier's capability and not a limit on validity" — where "the bound" is the decode bound
the verifier chose. `[R-MTA-04]` and `[R-MTA-05]` bind "the decoded document"; with no
assigned encoding there is no decoding this specification defines and so no requirement left
unchecked. §21.6's closing paragraph also enumerates the conforming-file-but-refused cases
and names exactly two, neither of them this. Independently, a certification verdict is not
an accept/reject of bytes.

PARTIAL, byte-level false, editorial. Repair: scope `[R-MTA-09]`'s "declines" to the
resource bound, or add a clause to §21.6's row.

## Group 16 — `[R-ENC-06]` has no register row and no §21.7 account (verifier-03, diagrams-07, adversary-06)

`grep -n "R-ENC-06"` returns exactly two hits: its definition at §4.2 and §19.3's
reader-validation list. So it governs no register row and is cited by no row, and §21.7's
two accounts (content incorrectness; the closed witness-free list of `[R-LIF-01]`,
`[R-LIF-03]`, `[R-GEO-06]`/`[R-SER-01]`, `[R-CNT-13]`'s no-embedded-offsets) do not name it.
§21.1 makes the register's completeness normative and names §21.7 as "the account, by class,
of what fails" the detectability gate. All three reporters independently reconstruct the
same witness argument — a field at the wrong width is byte-indistinguishable from correct
fields carrying different values, and every instance surfaces as some other row — and agree
the register is right and the account is short. Not byte-level for exactly that reason.
CONFIRMED, register-bookkeeping. Repair: a sentence in §21.7 placing `[R-ENC-06]` in the
witness-free class; §19.3's citation of it should then be reconsidered, since it instructs a
reader to perform a check with no witness.

## Group 17 — Appendix G's closing paragraph undercounts (diagrams-01, adversary-07)

"Four things are not" names gap content, gap extent, sub-record order, and the default fill.
Checked against the items:

- item 6 (sentinel for every all-fill tile): nothing requires an all-fill tile to be
  unstored — §13.3/`[R-TYP-08]` define what an unstored tile reads as, and storing one is
  conforming — and item 7 concedes the consequence ("two writers that default fill
  differently disagree about which tiles exist, not merely about eight bytes").
- item 4 ("One generation"): §9 constrains no commit count.
- item 5 ("No declared alignment and no slab"): §16.1/§16.2 say "A layer MAY declare".
- item 3 also fixes *top-level* record order, while the closing names only sub-record order;
  `[R-CNT-14]` frees both.
- items 1, 2, 8, 9 pin producers/values (defensibly excluded from the count).

Non-normative → not byte-level. CONFIRMED, editorial.

## Group 18 — front matter vs Appendix H on citation style (diagrams-04)

Front matter: "test vectors and conformance **checklists** cite identifiers, never prose
positions." Appendix H is titled "Conformance checklists", states its own rule as "each
entry's authority is the requirement or section cited", and cites prose positions throughout
("validates the trailer in §6.2's order", "never returns padding positions (§11.3)",
"re-emits every retained record byte-identically (§20.4)", "extent overlap (§7.2)", ...).
The alternative reading — that "checklists" means only corpus manifests — is not available
against the appendix's own title. Both texts non-normative → not byte-level. CONFIRMED,
editorial: either soften the front-matter sentence to test vectors, or add identifiers.

## Group 19 — §20.4's preservation table carries no identifier; §21.6 cites rules that do not state it (diagrams-05)

Verified: `[R-WRT-05]` labels the byte-identical-re-emission paragraph, `[R-WRT-08]` labels
the later no-re-encode paragraph, and the table plus its "and carry these obligations:"
preamble and the "No commit therefore removes..." paragraph carry none, though §2.2 says
"Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`" and §2.4 and
`[R-CNF-06]` both reach the table by prose position. §21.6's experimental-MU=0 row states
"Ignored, and preserved or dropped per its PE bit" and cites `[R-CNT-15]` (MU-bit reader
outcome, silent on PE) and `[R-WRT-08]` (no re-encode, no modification, silent on dropping).
So §21.1's "where such an entry and the rule it cites diverge, the rule governs" points at
two rules that do not contain the behaviour. Not byte-level — the obligations are stated
whether or not they are labelled. CONFIRMED, editorial.

## Group 20 — `[R-ERR-05]`'s hard-limit collection is incomplete (diagrams-06, register-03)

One defect, two exemplar sets. `[R-ERR-03]`: "Every limit affecting which files are valid,
or which files a conforming reader accepts, lives here", a stronger claim than `[R-CNF-10]`'s
"lives in this specification". `[R-ERR-05]` then collects floors of exactly the omitted kind
(S ≥ 1, A_slab ≥ 1, dir_length ≥ 4, dir_offset ≥ 16, F ≥ 128), so floors are in scope.
Omitted and register-carried:

- rank d ≥ 1, channel count C ≥ 1, tile extent Tᵢ ≥ 1 (`[R-GEO-01]`, row L32) — the entry
  and Appendix B both give only the ceilings, "at most 255 and 65,535";
- generation ≥ 1 (`[R-CNT-06]`, F11);
- a user-metadata extent_length ≥ 5 (`[R-CNT-25]`, F22/L11) — the exact analogue of the
  listed "directory of at least 4 bytes";
- inline_length exactly 1 (`[R-MTA-03]`, F23/L12).

register-03's second item, `[R-CNT-18]`'s nesting bound, is weaker: §7.4's Note says it has
no reader-detectable witness in format major 1, and it is arguably a structural prohibition
rather than a limit. Not byte-level — each limit is stated where its structure is defined and
carries a reader-detected row. CONFIRMED, register-bookkeeping.

## Group 21 — no worked byte example for a record header or a layer record (diagrams-08)

`grep -n "Example"` gives 21 example blocks; none lays out a 24-byte record header or a
packed layer-record inline payload as bytes. Appendix A is the only annotated file, is the
128-byte minimum, and "contains no layers". §12.3's channel-entry example covers one of
§7.4's field groups; a dimension entry is never shown. §4.7's Note promises "Every
non-obvious encoding is followed by a worked numeric example". Not byte-level: `[R-CNT-18]`
("fields are packed in table order with no alignment or padding between them") plus §7.2's
and §7.4's tables admit one parse. CONFIRMED, figure. Repair: a second annotated file with
one layer, which would also exercise an index region, a sentinel entry and a stored tile.

## Group 22 — T15's wrapper detection (register-01)

The construction is arithmetically right — `78 9C` passes the zlib header test
(0x789C = 31·996, CM = 8, FDICT = 0) and is also a valid raw stored-block header
(0x78: BFINAL = 0, BTYPE = 00) — so a naive header check has conforming false positives.
But reading (B), that T15 states a header procedure, is not licensed. §21.1 defines the
column the reporter reads it out of:

> The **Instances** column enumerates what a conformance corpus builds for that row (§21.8):
> the row is the rule, and each instance is one file.

Instances are corpus files, not a detection procedure. And §21.1 adds "each row *restates*
its governing rule, and where a row and the rule it cites diverge, **the rule governs**";
`[R-COD-05]` states a condition on the file and no procedure. Independently, `[R-CNF-03]`
("A reader MUST accept every conforming file of a format major version it implements")
forbids the false positive outright — which is the reporter's own reason for picking (A).
Byte-level downgraded. The residual, real point: T13 and T26 carry "the check that detects
it is T25's / T2's or T4's, and this row records the cause rather than a procedure of its
own" and T15/T16 do not. PARTIAL, editorial: add the same annotation to T15 and T16.

## Group 23 — §21.8 calls an outcome a "verdict" (register-02)

`grep -n "verdict"` gives 11 hits. Nine are `[R-CNF-11]`'s three-valued verifier report or
"no verdict on the file"; §21.8 is the only place a *row's outcome* is called a verdict.
`[R-CNF-11]` fixes the range: "A verifier reports one of three verdicts: *conforming*,
*nonconforming*, or *cannot establish*", and §2.4 fixes the outcome vocabulary separately.
§24 uses the right words — `[R-VEC-02]`'s "the outcome class (§2.4), the scope, and the §21
register row it exercises", `[R-VEC-04]`'s "recorded outcome". A corpus built to §24 is
unaffected, so not byte-level. CONFIRMED, editorial: §21.8 should read "expected outcome".

## Group 24 — L22's Instances cell (register-04)

L22's condition is one equality over extent_length and entry_count, with two stated
alternatives (slot (0,0) with entry_count > 0; a nonzero slot with entry_count = 0). §21.1:
"where a condition is a single predicate over several fields ... the fields it reads are not
instances, because no two files could differ." So naming "extent_offset; extent_length;
entry_count" mislabels: extent_offset enters only through the two alternatives, and
extent_length and entry_count are two halves of one predicate. F30 shows the right shape,
spelling its alternatives out in the condition text. The count of three survives under the
alternatives reading, so the 248 total is unaffected. Not byte-level — `[R-CNT-17]` states
the equality unambiguously. CONFIRMED, register-bookkeeping: relabel the cell as the three
alternatives.

## Group 25 — register row labels have no stability clause (adversary-04)

§2.2 guarantees stability only for `[R-XXX-NN]`. `[R-VEC-02]` normatively requires each
manifest entry to record "the §21 register row it exercises"; `[R-ERR-02]` and `[R-VEC-03]`
state coverage in rows and instances; Appendix H cites F7, F36, L25 by label. So the
corpus's primary key is the one key nothing promises to keep. Harm is bounded by
`[R-VEC-01]` ("where a vector's recorded expectation and this specification disagree, this
specification governs"), which is why it is not byte-level, but a silently re-pointed vector
still passes while leaving a row uncovered. CONFIRMED, editorial: a stability clause in
§21.1, or require the manifest to record the governing identifier alongside the row.

## Group 26 — §21.1 carries no identifier (adversary-05)

Verified: §21.1 cites `[R-ERR-02]`, `[R-CNF-07]`, `[R-CNF-04]`, `[R-CNF-11]` and carries none
of its own; `[R-ERR-01]` through `[R-ERR-05]` belong to §21.7–§21.9. It is not labelled Note,
Example or Rationale, so `[R-CNF-01]` makes it normative, and it states at least three rules:
the register's completeness, the row-versus-rule tie-break (reused for §21.6), and the
specialization-attribution rule. The tie-break is the one an implementer most needs to cite
and cannot. Reading (b) — that the opening `[R-ERR-02]` citation carries the subsection —
makes §21.8's own text incoherent, since `[R-ERR-02]`'s subject is vector coverage. Not
byte-level: the rules are fully stated. CONFIRMED, editorial.

## Group 27 — `[R-VEC-04]` and verifier-detected reject-layer/reject-tile rows (quiz-03)

§21.1: "For a row whose Detector is *verifier*, the outcome names the scope at which the
damage is recorded, **not an obligation on any reader**: the governing rule states what a
reader does, and for several such rows it obliges the reader to serve the structure
unchanged (`[R-SER-08]`, `[R-CNT-22]`)." `[R-VEC-04]` nevertheless makes a vector's
expectation "a pair: **the scope no reader is permitted to serve**, and the content a reader
that serves anything at all owes." For a verifier row that scope does not exist, and the
intact-sibling construction cannot distinguish what it is built to distinguish.

I counted the rows mechanically rather than accept the reporter's list: §21.3 has **nine**
verifier-detected rows (L18, **L25**, L40, L41, L42, L46, L47, L48, L49 — the reporter omits
L25) and §21.4 has four (T2, T4, T5, T26). The proportions the reporter gives ("a quarter of
the reject-layer rows and nearly half the reject-tile rows") are wrong against the section
totals of 49 and 26; the substance is unaffected. Not byte-level: `[R-VEC-01]` makes the
corpus derivative. CONFIRMED, editorial: qualify `[R-VEC-04]` to reader-detected rows, or
state what a vector for a verifier row expects.

## Group 28 — the over-long pre-trailer gap (quiz-07)

§6.2 decides it in terms: "a longer gap is conforming, and no conforming commit produces
one." The reporter's residual claim is that §2.3's account of conduct rules omits the case.
It does not: §2.3's clause is general, and the em-dash gives an illustration, not a closed
list —

> A writer obligation whose violation this specification expressly declares not to be a
> file-conformance violation — §6.3's flags = 0 against a set ignore-lane bit — binds the
> actor in the same way. `[R-CNF-02]`

§6.2 is exactly such an express declaration, so the pad case falls under the general clause.
F7 registers only a *structure* in the gap, consistently. PARTIAL, not byte-level,
editorial at most: a `[R-CNF-02]` cross-reference in §6.2's sentence would save the reader
the trip.

---

## Coverage

Groups: 28. Member ids counted per group: 1+2+3+3+1+1+1+2+2+1+4+2+1+2+1+3+2+1+1+2+1+1+1+1+1+1+1+1 = 44.
Every input id appears exactly once. Byte-level groups: 1 (group 8).

## Honest gaps

- I did not independently re-verify register-01's LZ4 token arithmetic (`04 22 4D 18` as a
  block) or the gzip 0x1F bit decomposition; the zlib arm, which is the one that carries the
  finding, I did check by hand (0x789C = 31·996; 0x78 = 0b0111_1000 → BFINAL 0, BTYPE 00).
  Neither affects the grade, which turns on §21.1's definition of the Instances column.
- I did not reconstruct any reporter's generation-1 or generation-3 trace file, so the
  specific byte offsets several reporters cite (verifier-01's 374/522/896, writer-02's
  [979,1024), writer-07's [536,637)) are unverified. None of them is load-bearing for the
  grades.
- Group 8 is the one grade I would most want a second opinion on: I read the em-dash clause
  as global (reading B) and two reporters read it as branch-local (reading A), and I could
  not find a sentence that settles it. I upheld the byte-level flag on that basis rather
  than on agreeing with the reporters' chosen reading.
