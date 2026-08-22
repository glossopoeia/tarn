# Round 19 triage — correctness lens — working transcript

## What I read

Only `spec/tarn.md`, in these ranges (via sed/grep, absolute path
/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md):

- §2.1–§2.5 (94–280), §3.1–§3.2 (282–362), §4.6 (473–520)
- §5.1–§5.2 (557–695), §6.1–§6.3 (693–830)
- §7.1–§7.4 (868–1110), §8.1 (1111–1135)
- §9.1–§9.2 (1154–1170), §9.7 (1319–1370)
- §10.1–§10.4 (1368–1460), §11.2–§11.4 (1497–1590)
- §12.1–§12.3 (1593–1700), §14.2 (1819–1890)
- §18.2 (2435–2566)
- §19.1 (2648–2705)
- §20.1–§20.5 (2849–3272)
- §21.1–§21.9 (3274–3642, incl. the F-row and L-row tables and §21.5's R rows)
- §22.3 (3752–3800), §23.1–§23.3 (3825–3892)
- Appendix G and Appendix H (4153–4364)
- section index via grep of headings

I read NO transcript at all — not the six walk transcripts, not the quiz
transcripts, and (per instruction) none of transcript-triage-*.md. I listed
the round19 directory once with `ls` before reading the instruction's warning
in full; the listing showed nine files and I opened none of them. Everything
below is checked against the spec text directly.

## Method

For each finding: locate the quoted sentence in the spec, check the quotation
is verbatim and in context, check the cited neighbouring rules actually say
what the reporter says, then ask the byte-level question. For every downgrade
of a byte-level flag I record the sentence that decides it.

## The byte-level test as I applied it

I applied: does resolving this change (a) whether some byte sequence is a
conforming file, or (b) what some actor must accept or reject?

I state the premise so it can be attacked: **I treat a two-file conduct
obligation — one whose satisfaction is not decidable from any single file —
as not byte-level, even when two implementers would emit different bytes from
the same input under the two readings.** The document's own framework
supports this: [R-CNF-02] "File conformance is a pure predicate on bytes: it
does not depend on any reader, writer, or environment", and §21.7 exists
precisely to inventory the MUST-level obligations no file witnesses
([R-LIF-01], [R-LIF-03], §20.3 step 4's bar, [R-WRT-06]'s carry-forward).
An ambiguity inside that class forks tool conduct, not the conforming set.

If the maintainer's test instead reaches "which bytes a conforming tool may
emit from a given input", then THREE groups flip to byte-level together:
quiz-01 (compactor tile preservation), writer-05 (§20.4 drop licence on an
add-only commit), adversary-05 (type re-declaration at equal element size).
I flag that in notes rather than hide it.

## Group-by-group

### 1. §23.1's "two ways" omits unstoring (reader-01, writer-01, verifier-07,
    diagrams-01, register-01, adversary-02)

Text checked, §23.1: "A commit removes sample data two ways — superseding it,
and a shrink that de-addresses tiles (§20.3 step 4) — and a dropped ancillary
record's extent (§20.4) goes the same way; no commit removes a layer at all."

§20.3 step 4 verified: "with entries for tiles this commit stores or
supersedes written to their new state, entries for tiles that become unstored
written as the sentinel" — the narrow usage is real and is in the very passage
§23.1 cites.

§23.2 verified: "a tile unstored by a later commit leaves its earlier payload
in the file as slack (§23.1)" — a back-reference to an enumeration that does
not name the case under the narrow reading.

Broad-reading support verified: §3.1 "Superseded payload bytes from earlier
generations do not make a tile stored"; §5.2 "everything an earlier commit
superseded"; §20.3 step 4's own close "Extents this commit supersedes become
slack". So the broad reading is genuinely available and the enumeration is
then complete — but only by a reading the cited section contradicts one clause
earlier. Six independent reporters landing here is itself evidence the closed
count does not read as complete.

adversary-02's planar channel drop merged here rather than split: I checked
[R-GEO-06] (disk ordinal c·N+s), §14.2 (planar decoded size P·Bᶜ), §11.2
(addressed-tile count C·N) and §20.3 step 4's "Dropping a tile out of the
addressed set ... is not itself such an alteration". A trailing-channel drop
on a planar layer does pass step 4's bar and does turn a plane's payloads to
slack, and it is not an *extent* shrink, which is what step 4's "An extent MAY
also shrink" is stated of. So it is a second instance of the same defect and
the same one-clause repair fixes both.

Byte-level: no. [R-PRV-01]'s own quantifier decides it — "Writers and the
tools built on them MUST NOT represent **any commit that makes sample data
unreachable** as erasure of it". The obligation reaches every route however
the preceding sentence is read, and it binds a representation made to a
caller, not a byte. CONFIRMED, editorial.

### 2. §23.1's MUST NOT is scoped to sample data (reader-05, quiz-02)

Verified: the paragraph brings the dropped ancillary record's extent inside
its scope ("goes the same way", "In each case the bytes remain in the file as
slack"), and the MUST NOT then quantifies only over "sample data", with a
gloss naming only shrink and supersede. §20.4 independently says "An updater
that drops such a record SHOULD report the loss; unreported, application state
disappears with no diagnostic" — so the document cares about this loss and
leaves its honest description unbound. Both reporters read it the same way,
by the letter, and the letter is what a tool author applies.

Byte-level: no, same quotation as group 1. CONFIRMED. I grade severity
design-decision, not editorial: whether the honesty rule should reach
non-sample content is a maintainer's call, not a wording slip.

### 3. §20.5's version_minor antecedent (reader-02, writer-02)

Verified [R-WRT-09]: "the open (§19.1), each retained layer's record (§19.3)
and full index chain ([R-IDX-04]), and each relocated extent's checksum" and
§20.5's own "its verification depth is [R-WRT-09]'s and **reaches no decoded
content**". So the compactor is told, in the same requirement, that it does
not decode the document in which the rule's own example of the antecedent
lives. Both branches are then reachable and they pull opposite ways whenever
the input's minor exceeds [R-CNT-26]'s floor. The stated reason ("a compactor
cannot know which minor version defined a feature it does not implement")
addresses a different gap than the one the example opens.

Byte-level: no. [R-CNF-12]: "Deviation from a SHOULD is not a violation for
this purpose: §21's register enumerates MUST-level conditions only, and a
verifier reports a SHOULD deviation as an advisory that does not bar
certification." Plus [R-CNT-07]: "A reader MUST NOT reject a file for its
version_minor." Two trailers differing in this u16 (and hence in the trailer
CRC) are both conforming and both accepted. CONFIRMED, design-decision — the
repair is a maintainer's choice between "assume the antecedent when carrying
undecoded content forward" and "take the floor absent positive evidence".

### 4. The (F36, L25, R1) citation (register-06, adversary-01, quiz-04)

Checked §10.2's table: eight spaces, each with a reserved range. Checked the
register: L31 (index_encoding 2–0x7F), L33 (linearization), L34 (sample type),
L36 (layout 3–255), L43 (codec), L45 (filter) all register reserved-range
values, beside F36/L25 (record type) and R1 (metadata encoding). Nine rows at
least; the parenthesis names three. The claim the parenthesis supports still
holds. CONFIRMED, editorial.

adversary-01's refinement — that R1 should be struck because its Detector is
*reader* and a compactor therefore detects it and must refuse — I do NOT
uphold. The sentence claims only that a later minor's new values reach such a
file "only as values this text still registers as reserved-range violations".
That is true of R1. Nothing in the sentence asserts a compactor could carry
one forward. Reading A adds a claim the words do not make.

### 5. "the two of §10.1's four vehicles §21.6 makes conforming" (verifier-08)

REFUTED. The reporter reads §21.6's experimental-range rows as instances of
§10.1's vehicles. They are not. §10.1's vehicles are how the format *grows*:
"1. New record types (§7.3) ... 2. New values in the ranges this
specification reserves (§10.2)". §10.3 puts experimental values outside that
entirely — "Experimental values are private use and carry no collision
protection: two unrelated experiments MAY select the same value" — and §20.5's
antecedent is "a feature a later minor defines". An experimental value is
never one. So no restriction is being "silently applied"; the antecedent does
the work on the page. The count of two is correct as written, and the reporter
concedes the conclusion holds. Its secondary observation (six omitted rows) is
real and is group 4's subject.

### 6. Appendix G item 8 vs §20.4's compactor drop licence (reader-03,
    adversary-03)

Verified §20.4's MU = 0 / PE = 0 row: "A compactor MAY drop it whenever it
rewrites the file" — unconditional, unlike the appender's clause beside it.
Verified reachability in a conforming input: §7.3 registers two types, both
PE = 1, so an MU = 0 / PE = 0 record is of an unassigned type, and §21.6's row
"A record type this specification has not assigned, from the experimental
range ... carries MU = 0 | Ignored, and preserved or dropped per its PE bit"
makes such a file conforming. Verified Appendix G's closing inventory does not
mention a drop policy. So item 8's "reproducible only modulo its trailer" is
false for two profile-adopting compactors on such an input: they differ in the
record sequence, dir_length, the directory CRC and every offset after it.
CONFIRMED, editorial.

Byte-level: no. Appendix G is non-normative by §2.1 and by its own text: "It
adds no requirement to any actor: a writer ignoring it is fully conforming."
Both outputs are conforming files.

### 7. [R-WRT-07]'s regeneration trigger (reader-04)

Verified the clause: "regenerates each **relocated** tile-index region (entry
offsets new; ...)" against the Example's statement of the real trigger, "the
one kind this operation regenerates rather than copies, since its entries
carry the offsets that moved", and against §20.5's other paragraph
"Regenerating a region means classifying every entry in it: ... every other
entry is re-pointed to where its stored extent now lies". The condition is
written on the region's own placement; what forces regeneration is its
entries' targets moving. The corner case (region lands at its old offset while
its tiles move) is reachable.

Byte-level: no, and the sentence that decides it is in the same requirement:
"The output's reference arrays MUST equal the live generation's bit for bit
(`[R-MDL-02]`)." A compactor following the letter and skipping regeneration
emits stale offsets and violates that MUST, so [R-CNF-05]'s "A writer MUST
emit only conforming files" excludes those bytes under both readings.
CONFIRMED, editorial.

### 8. quiz-01 — no keyword obliges tile-byte preservation. THE CLOSE CALL.

The reporter is right about the surface facts, and I checked all of them:
- [R-WRT-07]'s preservation clause carries no capitalized keyword.
- [R-WRT-05] reaches "header, inline payload, and extent slot" of *records*;
  §5.2 makes a stored-tile extent a different claimant class.
- [R-WRT-08] is limited to "a record whose type it does not implement".
- [R-CNF-06] and [R-WRT-01] name only "the preservation obligations of §20.4".
- [R-MDL-02]'s MUST is satisfied by a re-encoding compactor.
So no all-caps MUST states it.

I downgrade, and here is the premise and the sentences that decide it.

Premise being attacked: reading B needs "a normative sentence with no
capitalized keyword imposes no obligation". §2.1 does not say that. What it
says is: 'The key words "MUST", "MUST NOT", ... are to be interpreted as
described in BCP 14 ... when, and only when, they appear in all capitals.'
That governs how the listed *key words* are read; [R-WRT-07]'s clause contains
none of them. And §2.1's next paragraph is: "All text in this document is
normative except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*; and appendices identified as non-normative. `[R-CNF-01]`"

Internal proof that this document treats keyword-free normative declaratives
as binding: [R-CNT-13] states "neither its inline payload nor its extent
contents encode offsets or lengths of other file bytes" — no keyword — and
§21.7 calls exactly that sentence "`[R-CNT-13]`'s **prohibition** on an MU = 0
record encoding file offsets in its own payload". Same construction, and the
document's own account of it is that it prohibits.

Second decider: §23.2's [R-PRV-04], normative text, states what [R-WRT-07]
requires — "`[R-WRT-07]` preserves every stored tile's bytes and every index
entry's crc bit for bit, so a compacted file remains trivially correlatable
with its input by content." Third: §20.4 uses the same declarative mood
definitionally — "That is not compaction, which carries every layer of its
input forward (§20.5)."

I tested the reporter's premise that both outputs are conforming files: they
are (a re-encoded tile with updated entry length/crc, segment CRCs and
crc_of_crc_array is self-consistent; all thirteen types are fixed-width
little-endian so the reference arrays are bit-identical). That premise
survives. What does not survive is the inference from §2.1.

Verdict: CONFIRMED as a real drafting defect, byte_level false,
severity design-decision. Repair: give the clause a MUST. This is the group I
would re-read first if any is re-opened.

### 9. §21.7's "witnessed only where A and B" (verifier-09, register-03,
    adversary-04)

Verified verbatim. The first clause makes "the change reaches a byte §14
structurally constrains — a padding position, a pad bit, or a boolean byte" a
necessary condition; the next clause, opened by "instead", supplies a witness
(T3 or T14) for a change reaching none of the three, and the clause after that
does it again for the codec (T15, T17, T23, T25). Taken literally the sentence
refutes itself within twenty words. The scoped parse ("only where ... where
§21.4's content rows fire") is the only true one and nothing marks the scope.
CONFIRMED, editorial. Not byte-level: §21.1 "The subsections after §21.5 are
not part of the register and carry no rows" — T3/T14/T15/T17/T23/T25 are
checked from §21.4 regardless.

### 10. §21.7 counts two [R-WRT-06] trailer obligations (writer-03)

Verified [R-WRT-06]: "It MUST mint a fresh file_id for the output — a new draw
under §9.3's randomness advice, not merely a value compared against the
input's — and generation 1". Four obligations touch the output trailer; §21.7
names two. Both omitted ones are unwitnessed on §21.7's own ground. The
defensible repair reading (that "[R-LIF-01], [R-LIF-03] ... properties of a
file's history" swallows them) is available but §21.7 cites identifiers
precisely everywhere else and [R-WRT-06] is neither. CONFIRMED, editorial.
Not byte-level: [R-WRT-06] states all four unambiguously.

### 11. §21.7 omits the appender's twin (register-05, adversary-06)

Verified [R-CNT-08]: "An updater MUST copy forward unknown ignore-lane bits of
the file it modifies and MUST NOT clear them", restated at §20.3 step 6. It is
unwitnessed for exactly the reason §21.7 gives for the compactor's, and §21.7
lists only the compactor's. §21.1 makes §21.7 "the account, by class, of what
fails" detectability, so a visible asymmetry inside one sentence is a real
gap. adversary-06 adds [R-CNT-26]'s appender floor, the SHOULD-side twin —
same shape. CONFIRMED, editorial.

### 12. A SHOULD listed among witnessless "violations" (writer-04, quiz-03)

Verified §21.7 ¶2's opening — "A second set of obligations is omitted from the
register because a single file exhibits no witness of their violation" — and
[R-CNF-12] — "Deviation from a SHOULD is not a violation for this purpose:
§21's register enumerates MUST-level conditions only". The version_minor floor
would be out of the register with or without a witness, and calling its
deviation a "violation" is precisely what [R-CNF-12] denies. CONFIRMED,
editorial. Not byte-level: [R-CNF-12] fixes both the register's contents and
the verifier's duty.

### 13. Head 3 of §20.3 step 4 unwalked (register-04)

Verified step 4's four heads and §21.7's walk: heads 1, 2, 4 walked; head 3
("the byte offset of any sample within the decoded tile image") not walked,
and a filter-only change not walked either. I checked the reporter's example
against §14.2's table: interleaved a(uint32)+b(uint16) re-declared
a(uint16)+b(uint32) leaves Q = Σ Bᵢ = 6 and P·Q unchanged, so T3 and T14 are
silent, while F_b moves 4 → 2 and every retained stored sample decodes
differently. [R-CNT-23]'s fill-length rule changes the layer record but leaves
the live state self-consistent. So the bar has a second unwitnessed case and
§21.7 names one. CONFIRMED, editorial.

### 14. §21.7's disclaimer placement (verifier-02)

PARTIAL. The placement observation is accurate: "None of these" sits in ¶1 and
¶2 carries no disclaimer of its own. But the catastrophic narrow reading the
reporter fears is foreclosed by text the reporter did not quote — [R-CNF-11]
makes *cannot establish* available only "where some requirement is one it is
**unable to check on a capability or resource ground**", and §2.4 repeats it:
"§2.3's duty to check every file-level requirement runs to the MUST-level
conditions §21 inventories". A witnessless obligation is not a capability or
resource ground, so ¶2's members were never cannot-establish grounds. The real
defect is the missing repetition, not an open reading. Editorial.

### 15. [R-CNF-02]'s conduct enumeration (verifier-04, quiz-05)

Verified the witness pair: bytes B (well-formed, generation 1, flags = 0)
emitted by a creator is conforming; the same bytes emitted by a compactor
whose input carried ignore-lane bit 20 violate [R-WRT-06]'s "The output
trailer MUST copy the input's unknown ignore-lane flag bits forward". Since
"File conformance is a pure predicate on bytes", the carry-forward MUST is a
conduct rule. [R-CNF-02] enumerates two such cases and says "are the cases
this text states"; §20.5 declares only that the obligation is witnessless,
which is a different claim, and §21.7 files it with genuine file properties
([R-LIF-01]). A defensible reading exists — that [R-CNF-02]'s "§6.3's flags =
0 against a set ignore-lane bit" denotes the whole §6.3 flags complex,
including its compactor sentence and [R-CNT-08]'s updater clause. On that
reading the case is declared where it arises. CONFIRMED as a taxonomy defect;
editorial. Not byte-level: the compactor is bound under either taxonomy and no
verifier can distinguish B's provenances.

### 16. File-scope rejection and the coverage walk (verifier-01)

Verified [R-CNT-21]. Its file-scope carve-out covers only pre-trailer failure
("Where §6.2's ordered validation rejects the file before a live trailer is
established there is no F and no live state to walk"), and its discard clause
is expressly a layer clause: "a rejected layer's claimants are not enumerated
... the claimants it had already enumerated are discarded **with the layer**".
Reading 2 (complete walk) is foreclosed by "a scope-level rejection ends that
scope's enumeration". Between readings 1 and 3, the definitional sentence
decides for 3 — "A partial total is F less the bytes claimed by the claimants
the walk did enumerate" — but the layer discard's stated reason ("the total is
a claim about a live state one of whose layers is not usable") generalizes
uncomfortably to file scope, which is why the fork is worth naming. So: two
readings, not three, and the text leans hard to reading 3. CONFIRMED (the gap
is real), design-decision.

Not byte-level: §2.3 "An established violation takes priority: a verifier that
has established any violation reports *nonconforming*" — the verdict is fixed
under every reading; only a mandatory report field's value moves.

### 17. No general duty to name an established violation (verifier-05)

Checked mechanically: `grep -n "MUST report"` yields seven hits — §2.3's
unchecked-requirement and unexamined-scope duties, §5.2's slack total (twice),
§9.6's recovery-tool duty, §14.2's [R-SER-08] return rule, and §18.2's
[R-MTA-10] ignored-record report. The only place a violation must be *named*
is [R-MTA-05]: "the file is nonconforming, a verifier MUST report it". So the
reporter's inventory is right, and a verifier emitting the single token
"nonconforming" satisfies the document. The counter (§2.4's Note, "how failure
is reported is implementation technique") is about reader outcome classes and
sits against six mandated report contents in the same section. §24's
[R-VEC-02] requires a manifest to record the row and its governing identifier
— the pair a verifier owes nobody. CONFIRMED, design-decision.

### 18. Unassigned-type record extents unnamed (verifier-06)

Verified §8.1's last row: "Extent of a record of a type this specification has
not assigned | none — the bytes are opaque (§7.2) | —" and §22.3's [R-SEC-04]:
"The extent of a record of a type this specification has not assigned is
covered by no checksum either (§8.1), so corruption inside it is equally
invisible". Verified [R-MTA-10]'s naming duty is stated only of user-metadata
records ("bytes a certificate covers without inspecting are counted and named,
never silent") and Appendix H's verifier list names only the metadata report.
The reporter's conclusion — that no duty exists and this is decidable, not
ambiguous — is correct. CONFIRMED, design-decision.

### 19. Appendix G item 6 unmarked (verifier-03)

Verified items 2 and 8 both mark their creator-only halves and item 6 does
not, and that [R-WRT-07] requires "every stored tile's bytes verbatim — each
index entry's crc is unchanged", which sentinelling an all-fill tile would
break, while §20.5 licenses dropping only records §20.4's table names.
CONFIRMED, editorial. Not byte-level: Appendix G "adds no requirement to any
actor".

### 20. Appendix G's closing gloss vs item 8 (register-07)

Verified both. Item 8: "The version_minor floor binds a compactor too, save
where its output carries a feature it does not implement". Closing paragraph:
"`version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD — item
8's creator's rule, not a compactor's (§20.5)". Flat contradiction on the same
half, and it reads as if the two halves were swapped relative to item 8's own
split. The closing paragraph disclaims itself ("Read the numbered items as the
list"), so item 8 governs. CONFIRMED, editorial.

### 21. §20.4's drop licence and an added record (writer-05)

Verified the row. The layer-set limb is glossed for additions ("A commit
changes the layer set by adding a layer"); the top-level-record limb is not,
and the only carve-out stated is for drops ("Dropping the record, or dropping
another record in the same commit, is not itself such a change"). Reading (b)
— that a record which did not exist is not "another" one — is available on the
words. Reading (a) is better supported: the parallel limb's gloss, and the
fact that the drafters carved out drops specifically rather than restricting
the limb to modifications. CONFIRMED as a narrow under-specification,
editorial. Not byte-level under my stated premise: both outputs are conforming
files and the obligation binds a commit across two files with no witness in
either — the same class §21.7 inventories.

### 22. §20.4's table and §6.1 carry no identifier (diagrams-02)

Verified: between [R-WRT-05] and [R-WRT-08] the table and its two framing
paragraphs carry no closing identifier, and the table states three MUSTs.
Verified §6.1's "Writers MUST emit exactly these 16 bytes." stands alone, with
[R-CNT-04] (a reader rule, residency-scoped) the nearest identifier — and F6
does cite [R-CNT-04]. Verified the citation-by-section pattern the reporter
predicts: [R-CNF-06] "the preservation obligations of §20.4", §2.4's
preserve-verbatim row "§20.4's table states the cases", §20.5 "only where
§20.4's table licenses it", Appendix H "(§20.4, [R-CNT-22])". Verified
§21.6's unassigned-type row cites [R-CNT-15], [R-WRT-08] for a PE-bit
disposition [R-WRT-08] does not state. Against §2.2 "Normative requirements
carry identifiers of the form `[R-<PREFIX>-<NN>]`". CONFIRMED,
register-bookkeeping. Not byte-level: the obligations are stated in full.

### 23. §21.2's preamble and F5 (diagrams-03)

PARTIAL. The headline is accurate: the preamble's reason is an ordering
argument about §6.2's ordered validation, and [R-CNT-27]'s 128-byte floor is
not one of §6.2's checks — §19.1 step 1 obtains F before the trailer is
fetched. So the stated reason does not reach F5's physical-size instance.

But the reporter's reading (b) is not open. §2.3 decides it: "a file declaring
another major is neither conforming nor nonconforming under it: a reader
refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that
refusal is not a finding about its bytes." A verifier that reported
*nonconforming* for the 80-byte major-7 file would be making a finding about
its bytes, which that sentence forbids; and the preamble's own conclusion
names four reaching rows, F5 not among them. So the conclusion is fixed and
only the justification is defective. Editorial; the repair is to rest F5's
exclusion on [R-CNT-27]'s floor being a major-1 derivation (it is built from
§6.2's dir_offset ≥ 16, dir_length ≥ 4 and 64-alignment, none of which
[R-CNT-24] fixes across majors) rather than on gate ordering.

### 24. Appendix H's reader entry (diagrams-04)

Verified §2.3's three qualifiers and Appendix H's one. Verified §21.6's
closing paragraph names both dropped cases as "conforming files a reader
nevertheless refuses", and [R-ERR-04] carries the carve-out. Appendix H's own
preamble — "each entry's authority is the requirement or section cited, never
this summary" — is what keeps this from being open. CONFIRMED, editorial.

### 25. §18.2's "Valid values" cell (diagrams-05)

PARTIAL. The cell is "1 or 2; **see below**" — it defers explicitly, which the
reporter's headline drops and its block quote keeps. The prose immediately
below gives the full partition, §10.3 states "never a scope-level rejection",
§21.6 has a dedicated row, and [R-MTA-10] requires certification with a
report. So the cell is weaker than §6.2's version_major cell but is not a trap
a reader falls into without ignoring the pointer it carries. The improvement
is worth making and is cosmetic. Editorial, not byte-level.

### 26. §21.6's closing paragraph on an experimental MU = 1 sub-record
    (register-02)

Verified [R-CNT-15] ("An unknown record type **at file scope**: MU = 1 →
reject-file"), [R-CNT-18] ("an unknown sub-record type with MU = 1 is
reject-layer — never reject-file"), §10.3's split, and §20.4's table ("At
layer scope an unknown critical record blocks modification of that layer,
leaving other layers editable"). §21.6's closing prose states the case without
a placement qualifier, under a heading — "conforming files a reader
nevertheless refuses" — that presupposes a whole-file refusal, and cites only
the file-scope rule. §2.3 designates that paragraph as the authority for two
of the three relief grounds. So the defect is real: the paragraph either
over-states the sub-record case or silently omits it, and §21.1's tie-break is
written for §21.6's *entries* (table rows), not for prose after the table.

Secondary claim also verified: "Neither is a register row: the register
enumerates file-conformance violations (§21.1), and a file this document
declines to judge is not one" — that reason covers case 1 only. Case 2's file
is judged, and judged conforming; it is not a row because it is not a
violation.

Byte-level: no, and this is the group where I looked hardest, because a
reject-file/reject-layer fork is literally an accept/reject fork. The sentence
that decides it is [R-CNF-03]: a reader MUST accept every conforming file "of
a format major version it implements, **carrying no record of a type it does
not implement with MUST_UNDERSTAND = 1**". §7.4 makes a sub-record a record
("Sub-records are layer-scope records"), so a file carrying an experimental
MU = 1 sub-record falls outside the acceptance duty under BOTH readings. No
reader is obliged to serve the other layers under either reading, so no
verdict is forced apart; what is lost is the narrowest scope a reader *should*
refuse. CONFIRMED, design-decision.

### 27. R6 and R10's governing cells (register-08)

Verified §21.1's rule: each row carries "the requirement that defines it. A
Governing rule cell names that requirement first; any identifiers following it
in parentheses are the further rules the condition reads." Verified R5 and R6
name [R-CNT-25] first with R-ENC-12/R-MTA-04 parenthetical, while R7–R10 name
[R-MTA-04] first with R-CNT-25 parenthetical — a four-to-two split over one
rule's restrictions. Verified [R-CNT-25] states no key constraint at all
(it names ill-formed UTF-8 explicitly, which is why R5 is defensible and R6 is
not) and that [R-MTA-04] does restate §4.6's three name rules ("and every key
satisfying §4.6's name rules — non-empty, at most 255 bytes, free ..."), which
is why R10's cell is right in kind. CONFIRMED, register-bookkeeping.

### 28. §21.1 carries no identifier (register-09)

Verified: §21.7 [R-ERR-01], §21.8 [R-ERR-02], §21.9 [R-ERR-03]/[R-ERR-04]/
[R-ERR-05]; §21.1 ends "...which is why §14.2 calls it the sole resolved byte
in this format." with no identifier, while stating the register's extent, its
normative completeness, the row/rule tie-break, the Detector/Detected
semantics and the Instances arithmetic. Verified [R-ERR-02] as stated in §21.8
is a corpus-coverage rule and states none of those. Against §2.2 and against
[R-VEC-02]'s requirement that a vector cite a governing identifier. CONFIRMED,
register-bookkeeping.

### 29. Type re-declaration at equal element size (adversary-05)

REFUTED as framed — the criterion and the gloss do not disagree, because the
document defines a sample value as its bytes.

[R-TYP-04]: "A sample value is its bit pattern (§3.2, `[R-MDL-02]`). ...
Wherever this specification treats two sample or fill values as the same
value, it means their encoded bytes are identical; this format defines no
numeric equality, no ordering, and no NaN-aware comparison over sample
values." [R-MDL-02]: "sample values are bit patterns, and decoding MUST NOT
alter them". And §12.1's table makes every one of the thirteen types a
fixed-width little-endian bit pattern, so int32 → float32 at element size 4
changes no byte a reader returns and no element of the reference array.

So the gloss's "stored bytes meaning exactly what they meant" is satisfied on
the document's own definition of meaning, and the criterion permits the
commit — reading (a), which the reporter also picked. Reading (b) requires
importing a notion of numeric meaning the format expressly disclaims. The
neighbouring uint8 → bool case the reporter contrasts is decided the other way
by the criterion itself, since [R-SER-08] is a §14 constraint on the stored
bytes, and that is consistency rather than evidence of a gap. The only residue
is that §20.3 step 4 offers no worked example for a type change; that is not a
defect in the rule.

## Coverage check

44 input ids. Groups: 29. Members counted:
6+2+2+3+1+2+1+1+3+1+2+2+1+1+2+1+1+1+1+1+1+1+1+1+1+1+1+1+1 = 44. Each id
appears once; I listed the ids per group and re-summed before writing the
result. Byte-level groups: 0.
