# Round 11 triage — correctness lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in full for the
  sections at issue: front matter, §2.1–§2.5, §4.7, §5.1–§5.2, §6.1–§6.4,
  §7.1–§7.4, §8.1–§8.2, §9.2, §9.3, §9.7, §10.2–§10.4, §11.1–§11.3, §13.1–§13.3,
  §14.2–§14.5, §15.1–§15.3, §16, §18.2–§18.3, §19.1–§19.4, §20.1–§20.5,
  §21.1–§21.9, §22.3–§22.4, §24, Appendices A, B, G, H.
- I did **not** read the round-9/11 reporter transcripts in the scratchpad. Every
  claim below is checked against the specification text directly; where a
  reporter quoted selectively I re-read the surrounding paragraph.
- I ran one mechanical check: a script that parses the Instances cells of
  §21.2–§21.5 and counts rows and semicolon-separated instances.
  Result: F 36 rows / 53 instances; L 49 / 106; T 26 / 45; R 10 / 44;
  totals 121 rows / 248 instances, which matches §21.8's
  "121 conditions over 248 instances" exactly. This is the check that decides
  diagrams-07.

## Method

For each finding: (1) verify the quotation exists and is in context;
(2) ask whether the reporter's second reading is licensed by the words or only
by a reader who stopped early; (3) apply the byte-level test — does resolving
change which byte sequences may be emitted, or must be accepted or rejected —
and where I downgrade a reporter's byte-level flag, quote the deciding sentence.

## Grouping

| group | member ids |
|---|---|
| fill-is-structural-under-4-7s-own-test | reader-01, adversary-01, quiz-04 |
| compactor-placement-drops-declared-layout-invariants | reader-02, adversary-04 |
| compactor-refuses-on-quarantined-metadata-crc | reader-03 |
| no-commit-removes-user-metadata-at-either-scope | reader-04, verifier-04, diagrams-05 |
| section-21-7-witnessless-inventory-incomplete | reader-05, diagrams-09, register-06 |
| shrink-creates-padding-positions-unmentioned | reader-06 |
| listing-a-rejected-layers-unusable-name | reader-07 |
| verifier-front-block-obligation-unsurfaced | verifier-01, adversary-06 |
| verdict-for-experimental-metadata-encoding | verifier-02 |
| partial-slack-total-on-scope-rejection | verifier-03 |
| appendix-h-verifier-list-omits-pad-bits | verifier-05 |
| appendix-g-profile-is-not-total | verifier-06, adversary-05, diagrams-03 |
| layout-table-column-promises | diagrams-01 |
| appendix-g-four-things-undercount | diagrams-02 |
| vec-04-reads-a-detector-field-vec-02-does-not-promise | diagrams-04 |
| appendix-a-local-reader-front-block | diagrams-06 |
| r7-condition-omits-the-bom-alternative | diagrams-07 |
| index-encoding-value-set-attributed-to-15-1 | diagrams-08 |
| front-matter-vector-citation-claim | diagrams-10 |
| 21-1-gloss-misreads-r-ser-08 | register-01 |
| vec-02-cites-21-5-for-a-conforming-ignored-record | register-02 |
| f33-omits-file-scope-against-file-scope-overlap | register-03 |
| 21-6-omits-the-over-bound-metadata-document | register-04 |
| f5-instance-cell-and-its-gloss-of-F | register-05 |
| front-matter-block-normative-status | adversary-02, quiz-01 |
| 21-7s-opaque-by-construction-reason-for-r-cnt-13 | adversary-03 |
| trailer-mimic-row-argues-over-slack-not-payload | adversary-07 |
| compaction-barred-by-any-unimplemented-mu1-record | adversary-08 |
| compactor-version-minor-clause-strength | quiz-02 |
| verdict-unimplemented-major-with-failed-trailer-crc | quiz-03 |

41 ids, 30 groups, each id in exactly one group (counted: 3+2+1+3+3+1+1+2+1+1+1+3
+1+1+1+1+1+1+1+1+1+1+1+1+2+1+1+1+1+1 = 41).

Two merges deserve a note. verifier-01 (may a verifier omit the front-block
check?) and adversary-06 (Appendix H never mentions the front block) are one
defect with one repair: the verifier's front-block obligation is stated only in
§2.3's general clause and appears nowhere a verifier-builder looks (F6's
Detector cell reads *reader*; Appendix H's verifier list omits it).
verifier-06 / adversary-05 / diagrams-03 all say Appendix G's profile does not
determine its own output; adversary-05 spans both the item-2 hash gap and the
item-3 ordering gap, so the three cannot be split without splitting an id.

## Findings verified against the text

### fill (reader-01, adversary-01, quiz-04) — CONFIRMED, not byte-level

§4.7 as written: "A field is **structural** if its value determines anything a
conforming reader or verifier does with the file's bytes — where a byte lies,
how it decodes, or whether the file, layer or tile is accepted at all …
It is **semantic** if not". §14.5: "at every padding position, a writer MUST
encode … that channel's fill value … a verifier MUST check it, and a violation
is a validity error at tile scope." Register T4/T5 carry it. So the fill field's
value does determine whether a tile is accepted, and the classes are declared
mutually exclusive ("each class being what the one before it is not"), so the
closing sentence "in format major 1 `fill` is the only semantic field" is false
under §4.7's own test and the semantic class is empty. §13.2 [R-TYP-07] adds a
second ground at layer scope; §4.7's Note ("a variable-length field's value
includes its length prefix, so a name is structural") adds a third, which §13.1
answers only for fill ("the field's length prefix is §7.4's framing").
All three reporters describe the same defect; adversary-01 states it most
completely, reader-01 adds the §13.1 propagation.

Downgrade of nothing — all three flagged non-byte-level, and they are right.
Deciding text: the only MUST that keys off the taxonomy is the descriptive
class's ("a reader MUST NOT alter decoding based on it", §4.7), and fill is not
descriptive under either reading. [R-MTA-02] and [R-SEC-06] use "structural"
only as the opposite of "user metadata" — [R-SEC-06]: "User metadata is
application data and is never structural (§7.1)". L35, T4 and T5 state their
conditions directly over bytes, so no verifier's verdict on any file moves.

### compactor placement (reader-02 byte-level YES, adversary-04) — CONFIRMED defect, byte-level DOWNGRADED

The defect is real: §20.2 grants the creator placement "in any order satisfying
§5.2's coverage classes ([R-CNT-02], [R-CNT-03]) and every declared layout
invariant ([R-SLB-01], [R-SLB-03])"; §20.5 grants the compactor "free to place
structures anywhere §5.2 admits" with the second qualifier dropped, and §5.2
says nothing about alignment or slabs.

Byte-level downgrade, deciding sentences, both inside [R-WRT-06] two sentences
before the grant: "Given a conforming input the output is a conforming file. A
compactor satisfies every writer requirement for the bytes it produces
(`[R-CNF-06]`)". And [R-SLB-03] is a predicate over the output's own bytes,
verifier-checked: "When declared, for every run: the run's stored tiles are
contiguous and packed in ordinal order … and the first stored tile's offset
satisfies offset mod A_slab = 0." So compactor B's output is nonconforming
under *both* readings — L41/L42 read the output file, not its provenance — and
every verifier rejects it identically. Reader-02's claimed fork ("a verifier
must reject layer L in B's output and accept A's") is true but is not a fork:
it is the same verdict under both readings. What forks is only whether the tool
that produced B is a conforming compactor, and [R-CNF-05]/[R-CNF-06] plus the
quoted sentence close that. adversary-04 reached the same conclusion.

### compactor refusal on a corrupt metadata extent (reader-03 byte-level YES) — PARTIAL, byte-level DOWNGRADED

Facts check out: §8.1's map does state a checksum for a user-metadata extent
("final 4 bytes of the extent | the preceding bytes"), [R-WRT-09] does oblige
"each relocated extent's checksum", §21.5's header does make R2 a violation
("Every row here is a violation all the same"), and [R-WRT-05] bars a corrected
re-emission.

But the text decides it, and reader-03 half-concedes this. Deciding sentence:
"A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
and MUST NOT emit a file carrying a violation it has detected: it can neither
drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected
(`[R-WRT-05]`)." Two MUSTs. The quarantine cannot be read against them: its
"notwithstanding" is expressly scoped — "notwithstanding the owning-scope
mapping of `[R-CNF-08]`" — and [R-CNF-08] is the reader-outcome mapping, not an
updater rule. So reading (b) is not licensed and no byte sequence forks.
Graded PARTIAL rather than REFUTED because the *consequence* is real and is a
maintainer's decision, not a misreading: one failed metadata CRC permanently
bars the only operation that reclaims slack (§20.5, §23.1), on a record §7.1
says "never invalidates the structural data it annotates".

### the §20.4 summary sentence (reader-04, verifier-04, diagrams-05) — CONFIRMED, not byte-level

§20.4's summary reads "No commit therefore removes a layer record or a
file-scope user-metadata record"; Appendix H reads "never removes a layer
record, or a user-metadata record at either scope (§20.4)". The governing
paragraph is one line above the summary and is scope-unqualified: "For a type
§7.3 registers, the registry's fixed flags govern rather than the stored ones
(`[R-CNT-22]`) — both registered types carry PE = 1, so neither can be dropped".
§7.3 registers 0x0002 once, with Scope "file when top-level; layer as
sub-record", flags MU = 0, PE = 1. So Appendix H is right and the summary is
under-inclusive. Not byte-level: both resulting files are conforming, and the
quoted paragraph plus §20.4's "MU = 0, PE = 1 | Retain byte-identical, extent
content unmodified" row already decide which one a conforming updater emits.

### §21.7's second paragraph (reader-05, diagrams-09, register-06) — CONFIRMED, register-bookkeeping

§21.1 nominates §21.7 as "the account, by class, of what fails it". §21.7 ¶2
names five obligations in four classes. Candidates the three reporters add:
[R-LIF-02] step 3 (its own Note in §9.2 supplies the violation: "A writer that
re-points a new trailer at a prior generation's directory region has left step 3
unperformed"), [R-IDX-01]'s entry-order mapping, [R-WRT-05]'s byte-identical
re-emission, [R-WRT-06]/[R-WRT-07]'s compaction relations, [R-CNF-06].
I checked each: all are MUST-level, none has a single-file witness, none carries
a register row. [R-IDX-01] is the weakest — "The entry for the tile with disk
ordinal k is the k-th entry" is definitional, so there is arguably nothing to
violate — but that only strengthens the case that §21.7 should say which class
it falls in. The ambiguity is whether ¶2 is an inventory (its grammar: a
semicolon list closing with "and", each item naming identifiers) or a taxonomy
by class (§21.1's words). Not byte-level under either reading.

### shrink (reader-06) — CONFIRMED, not byte-level

Nothing in §11.1 forbids narrowing an extent; §11.1's rationale discusses growth
only and says grid-count-preserving growth "touches the directory alone".
A narrowing that turns real positions into padding positions makes every
affected edge tile violate [R-SER-05] unless re-emitted, and §20.3 step 4 never
says so while shape (c) states the symmetric fill-change rule. Real procedural
gap. Not byte-level: "at every padding position, a writer MUST encode … that
channel's fill value … a verifier MUST check it, and a violation is a validity
error at tile scope" is a predicate over the file, so both implementations reach
the same verdict on the emitted file, and [R-CNF-05] already bars emitting it.

### listing a rejected layer's name (reader-07) — CONFIRMED, not byte-level

L3, L5, L6 are all Detected = open and reject the layer because the name is
unusable; §2.4 permits "A reader MAY still list the file's layers, including the
rejected one's name" without saying what is handed over, and §22.4's rationale
for C0 screening is exactly the screening that failed. Real under-specification
of reader output. Not byte-level: it is a MAY about what a reader surfaces; the
file's verdict is fixed at reject-layer either way.

### verifier and the front block (verifier-01, adversary-06) — CONFIRMED, register-bookkeeping

The normative question is decided: §2.3 defines a verifier as "A reader that
additionally checks every file-level requirement — including those ordinary
readers are exempted from", and §6.1's "Writers MUST emit exactly these 16
bytes" is a file-level requirement from which [R-CNT-04] exempts exactly an
ordinary reader. So verifier-01's reading (a) is not licensed and the finding is
not an ambiguity. What *is* wrong is that this obligation is surfaced nowhere
else: F6's Condition cell states only the reader half ("the obligation binds a
reader holding those bytes resident, and a reader that would have to fetch them
MAY defer or omit the check") with Detector *reader*, and Appendix H's verifier
entry — whose stated job is "the checks readers are exempt from" — never
mentions the front block. adversary-06 describes this accurately.
Not byte-level: §2.3 decides, and F6's file predicate is unchanged.

### experimental metadata encoding verdict (verifier-02) — CONFIRMED, editorial

Checked §18.2: [R-MTA-09]'s cannot-establish clause is narrowly scoped — "A
**verifier** that declines to decode a document on the bound above cannot
establish that document's conformance and MUST NOT certify the file" — where
"the bound above" is the reader's self-chosen resource bound. §2.3's restatement
drops the qualifier: "or when it declines to decode a user-metadata document
(`[R-MTA-09]`)". §21.6 declares the experimental-encoding file conforming and
§21.6's closing paragraph enumerates exactly two "conforming files a reader
nevertheless refuses" with no verifier case. The repair is the dropped
qualifier. Not byte-level: no reader's accept/reject and no writer's bytes move;
both verifiers decline to call the file nonconforming.

### partial slack total (verifier-03) — CONFIRMED, editorial

§9.7: "Where the walk does not complete — a scope-level rejection blocks
enumeration, or the verifier stops at the first violation (`[R-CNF-11]`) — the
sum is reported as partial". Grammatically "blocks enumeration" is a predicate,
not an assertion that every rejection blocks, which favours the restrictive
reading; [R-CNT-21] phrases it "because a scope-level rejection stops it", same
shape. The residual question — may a verifier that rejected a layer for L35 and
nonetheless completed its walk label the total *exact*? — is genuinely
unanswered. Note that the numeric divergence the reporter measured is largely
licensed already: [R-CNF-11] lets any verifier stop at the first violation and
[R-CNT-21] governs the partial. What forks is the label. Not byte-level.

### Appendix H omits pad bits (verifier-05) — CONFIRMED, editorial

Appendix H's verifier entry: "decoded-content obligations — padding samples and
interleaved boolean bytes (§14.5, §14.2)". T5 (pad bits) is a fourth
verifier-only decoded-content row and is not named, though §14.3's note insists
the two mechanisms are distinct. Non-normative, cites §14.5, and [R-SER-05]
states the obligation ("Every pad bit (§14.3) MUST carry the plane's channel's
fill bit"), so nothing is underdetermined.

### Appendix G (verifier-06, adversary-05, diagrams-03) — CONFIRMED, editorial

Three concrete holes in a profile whose stated purpose is to close the format's
degrees of freedom:
(i) item 2 names no hash function and no reduction to 64 bits, and its input set
is circular on a literal reading — §6.2's table puts the trailer CRC at offset
60 covering "trailer bytes [0, 60)", which includes file_id at offset 48, so
"the trailer's other fields" includes a field that depends on file_id;
(ii) item 3 gives no tiebreak for two top-level records of one unassigned type
(§7.2 [R-CNT-14] states multiplicity rules only for 0x0001 and 0x0002);
(iii) item 3 orders sub-records within a layer record and top-level records
among themselves but never places a sub-record *extent* in the global "ascending
record order" that governs extent emission, though §9.7 counts sub-record
extents as claimants.
Not byte-level: "It adds no requirement to any actor: a writer ignoring it is
fully conforming", and §6.2 admits any nonzero file_id, so every choice yields a
conforming file.

### layout tables (diagrams-01) — CONFIRMED, editorial

Front matter: "On-disk structures are presented as offset/size/type/name/
valid-range tables" (five, no class). §4.7's Note: six columns, with one
carve-out for §7.4. Checked: §6.2, §15.1 and §18.2 deliver all six. §6.1's table
is `| Offset | Size | Value | Class |`; §7.2's is `| Offset | Size | Type |
Field | Class |` with the constraints folded into the Field cells. Both are
fixed-layout structures. The carve-out for §7.4 makes the "menu" reading
implausible. Not byte-level: §6.1's constants and §7.2's constraints are all
present, just not in the promised columns.

### Appendix G's "Four things" (diagrams-02) — CONFIRMED, editorial

Checked each item against the core text. Item 6 ("The sentinel for every
all-fill tile") is nowhere mandatory — [R-TYP-08] makes an unstored tile read as
fill but nothing forbids storing a tile whose samples equal fill — and item 7's
own text treats item 6 as a separate freedom, yet only item 7's is among the
four. Item 8 promotes [R-CNT-26]'s SHOULD exactly as item 7 promotes
[R-TYP-10]'s, and is not counted. Item 2's hash-derived file_id is not
mandatory (§9.3 requires only nonzero, advises randomness); item 5's "no
declared alignment and no slab" is free under §16 [R-SLB-05]; item 4's one
generation is free under §9.3. The count is wrong however it is defended.

### [R-VEC-04]'s detector field (diagrams-04) — CONFIRMED, editorial

[R-VEC-02]'s minimum: "its identifier; whether the file is **conforming**; the
decoded content …; and, for each structure the file damages, the outcome class
(§2.4), the scope, and the §21 register row it exercises." No detector.
[R-VEC-04] then says "carried by the entry's own scope and detector fields
(`[R-VEC-02]`)". "At minimum" rescues the schema but not the citation. Manifest
schema only; §24 makes the corpus derivative.

### Appendix A's local reader (diagrams-06) — CONFIRMED, editorial

§6.1 is explicit that the local/remote distinction "governs the request
accounting of §6.4 and nothing else; the obligation over the front block turns
on residency instead", and Appendix A's main clause makes it a property of being
a local reader before its own subordinate clause restates residency. A local
reader that preads only the tail and the directory range does not hold [0, 16).
Non-normative, self-correcting in the next clause. Not byte-level: "A reader
that would have to issue a further range request to obtain those bytes MAY
defer or omit the check" makes both behaviours conforming by construction.

### R7 and the BOM (diagrams-07) — CONFIRMED, register-bookkeeping

R7's Condition names two alternatives; its Instances cell names three
(adding "leading U+FEFF") over two containers = six. [R-MTA-04]'s first
restriction states the BOM rule separately: "The top-level value is an object,
and the encoding carries no byte-order mark: a leading U+FEFF makes the document
unreadable." My instance count confirms the six are load-bearing: the
mechanical total is exactly 248, matching §21.8, so removing them would break
the arithmetic. The Condition prose is the lagging half; §21.1's "where a row
and the rule it cites diverge, the rule governs" keeps it out of byte territory.

### index_encoding's defining section (diagrams-08) — CONFIRMED, editorial

§15.1's only mention is "Under index_encoding 1 (the only encoding this format
major version defines, §7.4)" — it states no value set. §7.4's row states the
set and points to "(§15)". §10.2's row reads "index encoding (§7.4, §15.1)";
L31's Governing rule reads "(§15.1)"; [R-EXT-03] and [R-RDR-03] list §15.1
among the six value-set sections, and for the other five the cited section does
state the set. [R-EXT-05] makes "the section that defines the space" the
tiebreaker, so the cross-references name a section that defines nothing.
Every statement of the set agrees, so nothing is underdetermined.

### front matter and vector citations (diagrams-10) — CONFIRMED, editorial

"Normative requirements carry stable identifiers like `[R-IDX-03]`, and test
vectors cite those identifiers rather than prose positions" against [R-VEC-02],
which requires the register row and never the identifier, and [R-ERR-02], which
ties vectors to rows. Manifest schema; §24 governs over any vector.

### §21.1's gloss on [R-SER-08] (register-01) — CONFIRMED, editorial

§21.1: "for several such rows it obliges the reader to serve the structure
unchanged (`[R-SER-08]`, `[R-CNT-22]`)". [R-CNT-22] fits. [R-SER-08] does not,
on either half. §14.2: "A reader is not obligated to screen decoded content …
`[R-CNF-12]` governs a reader that does detect it. A reader that neither detects
the violation nor rejects the tile, and returns the value, MUST report 0x00 as
false and every other byte as true." §12.3 and Appendix H both call this the
sole resolved byte. Not byte-level: the byte cannot occur in a conforming file
("it never arises in a conforming file, where the only bytes present are 0x00
and 0x01"), and §14.2 states both answers imperatively.

### [R-VEC-02]'s citation of §21.5 (register-02) — CONFIRMED, editorial

§21.5's header: "Every row here is a violation all the same: the outcome bounds
a reader's blast radius and never makes the file conforming (`[R-CNF-12]`);
§21.6 lists the ignore-record conditions that are not violations." So the
records a *conforming* file may carry and a reader ignores are §21.6's, not
§21.5's. Appendix H states it correctly. Not byte-level: [R-CNF-12] and §21.5's
header each decide it, and [R-VEC-01] makes the specification govern a vector.

### F33 and file-scope overlap (register-03) — PARTIAL

Shape (d) is constructible and the reporter is right that neither F33's
em-dash gloss nor [R-CNT-13]'s outcome sentence names it: "a verifier MUST
treat an intra-layer overlap … as reject-layer, and any overlap across layers or
touching another scope's structures as reject-file" leaves file-scope-against-
file-scope unnamed. But the claim that shape (d) has no row is refuted by the
row's own leading clause — "claimed by two structures that do not belong to the
same layer" is true of two file-scope structures — and by its Instances cell,
which already names "record extents" and "directory region". So the register is
complete and the gloss and [R-CNT-13]'s outcome clause are the defective parts.
Not byte-level: "No two of them overlap, and a file whose live state does not
partition this way is not a conforming file" (`[R-CNT-02]`) is unconditional,
and [R-CNF-08] maps file scope to reject-file.

### §21.5's signpost to §21.6 (register-04) — CONFIRMED, register-bookkeeping

[R-MTA-09] plus its Note do define a third ignore-record non-violation: "a
document exceeding that bound is ignore-record like any other it cannot read",
and "A file whose document decodes to more than the guarantee stays conforming".
§21.6's table has no entry for it. §21.6's own header claims only "These are
defined behaviors, not errors", and §21.1 says the completeness clause does not
reach §21.6 — so the sentence in §21.5 is a signpost, and the honest repair is
to add the entry. Not byte-level.

### F5 (register-05) — PARTIAL

The reporter's premise is right: §5.1 defines F as the committed file length
("the live trailer's committed file length F"; §6.2's table "committed_file_
length … = F"), so F5's parenthetical "F (physical file size)" is a local
redefinition. The conclusion is weaker than claimed: a file declaring
committed_file_length below 128 is a distinguishable file exhibiting the
condition, so the instance is not spurious under §21.1's rule ("One instance is
one *distinguishable* file"), it is merely over-determined — which [R-VEC-02]
already anticipates ("the entry records every row the file exercises and says
which it was built for"). Repair is the gloss, not the instance count (which the
248 arithmetic locks). Not byte-level: reject-file under either reading.

### front matter's normative status (adversary-02, quiz-01) — CONFIRMED, editorial

[R-CNF-01]'s list is exhaustive — "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*;
and appendices identified as non-normative" — and the "How to read this
document" block is above §1, is not labelled Note/Example/Rationale, and is not
an appendix, while labelling itself *(non-normative)*. The status paragraph and
licence line above §1 are in the same position. Not byte-level: nothing in the
block constrains any file's bytes, and its two falsifiable claims (table columns,
vector citations) are graded separately.

### "opaque by construction" (adversary-03) — CONFIRMED, editorial

§7.3 registers exactly one MU = 0 type, 0x0002, whose extent contents §18.2
specifies down to duplicate-key identity and number finiteness, and which
verifiers check (F27, L48, R5–R10). So §21.7's stated reason for omitting
[R-CNT-13]'s no-embedded-offsets prohibition — "opaque by construction" — is
untrue of the only MU = 0 instance a format-major-1 file can carry. The
conclusion survives (the prohibition is undecidable over a JSON document, and
[R-MTA-02]/[R-SEC-06] make user metadata inert reader-side); only the reason is
wrong. Not byte-level: a rule no implementation can evaluate separates no two
verifiers' verdicts on any concrete file.

### the trailer-mimic row (adversary-07) — PARTIAL

The §21.6 half is right: the row's Condition is "A payload contains a byte
string that mimics a trailer" while its justification opens "Inert: nothing
enumerates slack", and §5.2 makes a stored-tile extent a *structure*, not slack
("Every byte the live state does not claim is **slack**"). The operative reasons
are [R-LIF-05]'s no-backward-scan and §6.2's note on an end-of-file mimic.
The §22.3 half is not: [R-SEC-04] handles the payload case on its own ground
("which is why recovery output is re-verified as a whole file before being
trusted") and only then says "a mimic **in slack** is inert" — correctly scoped.
Not byte-level: §21.6 carries no rows and [R-LIF-05]/[R-LIF-06] decide every
file identically.
(Noticed in passing, reported by no one: §22.3's sentence reads "…before being
trusted (`[R-LIF-06]`) before any use" — a duplicated clause.)

### compaction and MU = 1 sub-records (adversary-08) — PARTIAL

The placement complaint is fair — §20.4's "Compaction is barred on the same
ground (`[R-WRT-06]`)" sits after the file-scope sentence. But the second
reading is not licensed once [R-WRT-06] is read: "A compactor MUST refuse to
compact a file carrying any record whose type it does not implement with
MU = 1", and §7.4 makes sub-records records ("sub-records | zero or more records
(§7.2 framing)"). A compactor author works from §20.5. So: real editorial
placement issue, no fork. Not byte-level, as the reporter's own caveat concedes.

### version_minor on compaction (quiz-02, byte-level YES) — CONFIRMED ambiguity, byte-level DOWNGRADED

This is the closest call in the set and I want the reasoning on the record.

The clause: "The output trailer copies the input's unknown ignore-lane flag bits
forward (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the
input's version_minor". One sentence, two declarative restatements, each citing
its own rule — and the two cited rules differ in strength: [R-CNT-08] is a MUST
for updaters, [R-CNT-26] is a SHOULD. The natural rule is that a declarative
restatement carries the strength of the rule it cites, and §20.3 step 6 does
exactly this for an appender ("version_minor per `[R-CNT-26]`") where nobody
reads a promotion to MUST.

Deciding sentence for the downgrade, §2.1: "The key words 'MUST', 'MUST NOT' …
are to be interpreted as described in BCP 14 … when, and only when, they appear
in all capitals, as shown here." §20.5's clause contains no capitalised keyword,
so it imposes no MUST of its own; its strength is [R-CNT-26]'s. Reading (2) is
therefore not licensed.

Second, even granting reading (2), the file predicate does not move. §6.2's
table gives version_minor Class *descriptive*, Valid values "any (see §6.3)";
§6.3 says "A reader MUST NOT reject a file for its version_minor"; §21.6 records
"version_minor is higher than this text defines | Accepted; minors never gate";
no register row exists. Both trailers are conforming files that every conforming
reader accepts identically, and [R-CNF-05] already licenses two writers to
"produce different conforming files" from identical input. What forks is a tier
conduct label, not the set of conforming byte sequences.

I still grade the group CONFIRMED: the clause's strength is unmarked and the
repair (mark it, presumably SHOULD, matching [R-CNT-26]) is a maintainer
decision.

### unimplemented major with a failed trailer CRC (quiz-03) — CONFIRMED, editorial

Both quoted passages are real and in tension: §2.3's "a file declaring another
major is neither conforming nor nonconforming under it" against §2.3's "An
established violation takes priority", with §6.2's fixed order and [R-CNT-24]'s
permanence making the CRC check major-agnostic. Worth a clarifying sentence.
Not byte-level: §6.2 fixes the reader's behaviour identically under both —
"A reader MUST validate, in order: the trailer magic; the trailer CRC; the
version gate (§6.3) … Any failure is reject-file" — so the file is rejected at
the CRC step either way, and neither verdict certifies.

## Byte-level tally

Zero groups fork the bytes. Three reporters self-flagged byte-level
(reader-02, reader-03, quiz-02); each is downgraded above with the sentence that
decides it quoted in place. The closest of the three is quiz-02, and if a
re-check overturns any of my downgrades I expect it to be that one.
