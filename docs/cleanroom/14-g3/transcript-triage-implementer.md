# Round 14 triage — implementer-consequence lens

## Access disclosure

Read: `spec/tarn.md` only (§2.1–§2.5, §5.1, §5.2, §6.1–§6.4, §7.2, §9.7,
§11.1–§11.3, §15.2–§15.4, §16.2, §17.2, §19.1, §20.1–§20.5, §21.1–§21.9,
§24, Appendix G). Ran two greps/one python extraction over the same file to
re-count register rows and instances. Listed the round14 scratchpad
directory once with `grep -v triage` applied to the output so no
`transcript-triage-*.md` name was displayed; opened none of the walk
transcripts (the findings quoted enough of each reporter's reasoning). No
`docs/`, no `PLAN.md`, no git history, no registry.json, no web.

Mechanical check I ran: extracted all 121 register rows by regex, counted
semicolon-separated instance-cell members (a cell reading `—` = 1). Got
F 56 / L 111 / T 57 / R 44 = **268 over 121 rows**, matching §21.8 exactly.
So the stated total is faithful to the cells; any defect is in a cell or in
§21.1.

---

## Grouping

23 ids → 15 groups.

| group | ids |
|---|---|
| instance-axis-not-applied | reader-01, writer-01, verifier-01, diagrams-02, register-01, adversary-01, quiz-01 |
| commit-example-c-overforbids-fill-change | reader-02, diagrams-01 |
| stored-tile-tense-in-step-4 | quiz-02 |
| profile-digest-byte-selection | writer-02, diagrams-03 |
| profile-first-structure-offset | writer-05 |
| profile-recap-omits-item-10 | diagrams-04 |
| compactor-offset-enumeration-third-case | writer-04 |
| slack-total-when-no-live-trailer | writer-03 |
| slack-total-walk-detected-layer-rejection | verifier-02 |
| foreign-major-register-applicability | verifier-03 |
| outcome-follows-scope-vs-ignore-record | register-02 |
| governing-rule-parenthetical-convention | register-03 |
| verifier-row-serve-unchanged-list | register-04 |
| extent-may-always-grow-vs-lz4-cap | adversary-02 |
| slab-decidable-from-index-bytes | quiz-03 |

Seven reporters filed the instance-axis defect. Their proposed totals
disagree (272, 273, 273, 273, 273, 274, 274) — see below; that disagreement
is itself evidence about the repair, not about the grouping.

writer-03 and verifier-02 both touch [R-CNT-21]. They are two different
defects with two different repairs (no-F-at-all vs keep-or-drop the
claimants of a walk-rejected layer). verifier-02 raises the no-F case as an
explicit "smaller sibling"; its id goes with its dominant claim and I
cross-reference.

---

## 1. instance-axis-not-applied (7 ids)

Verified against the text. §21.1:

> Where the condition compares two quantities and either can be the
> greater — a *differs from* or *does not equal* — the two directions are
> likewise enumerated; where its own text bounds the comparison in one
> direction — an *exceeds*, a *larger than* — there is one. … the count is
> therefore mechanical once the cell is written.

Cells as they stand: F17 `committed_file_length` (1); L21 `interleaved N;
planar C·N` (2); L22 `extent_length against the formula; slot (0,0) with
entry_count > 0; a nonzero slot with entry_count = 0` (3); L30 `—` (1).
Against T3/T14/T22, each 3 layouts × 2 directions = 6. The asymmetry is
real; consensus CONFIRMED.

**Implementer consequence.** Nothing to a reader, writer, updater or
verifier. §2.3 defines five conformance classes — file, reader, writer,
updater, verifier — and a corpus builder is none of them. Both directions
of all four conditions are already rejected by the same governing rule at
the same tier with the same outcome ([R-CNT-06], [R-CNT-17], [R-CNT-23]);
a reader that accepts entry_count = N−1 is nonconforming exactly as one
accepting N+1 is. The deciding sentence for the downgrade is §21.8's own:

> A row without a vector is a gap in the corpus, not a licence to skip the
> check. `[R-ERR-02]`

and §24's [R-VEC-01]: the corpus "is evidence of conformance, never its
definition". What forks is the size of a build list, not a byte.
Severity: register-bookkeeping.

**But the repair is not the one six of seven reporters propose.** Applied
literally and uniformly, the direction sentence also fires on every
equality-against-a-checksum row: F14 (`the u32 at trailer offset 60 does
not equal the CRC-32C…`, 1 instance), L37 (`crc_of_crc_array ≠ …`, 1),
L38 (`A segment CRC ≠ …`, 1), T6 (`crc ≠ 0`, 1). "Either can be the
greater" is literally true of two u32s. No reporter proposes doubling
those, because everyone silently applies the judgement §21.1 claims to
have removed. That is why three different totals (272/273/274) came back
from reporters who each called the count mechanical. Note also L41, which
enumerates `gap; overlap; out-of-ordinal placement` — the two directions
under other names, plus a third alternative — so the axis is already
satisfied there by non-directional wording.

So the repair is a fork the maintainer must pick, not an arithmetic fix:
either narrow §21.1's direction sentence (restrict it to comparisons of
two *magnitudes a file's declarations or geometry derive*, excluding
checksum equality, and say that a cell already naming the directions under
other names satisfies it) and leave the cells and 268 alone; or widen the
four cells and re-derive §21.8's total under an explicitly stated
exclusion list. Doing the second without the first gives 273 by judgement,
not 276 by rule, and leaves §21.1 still claiming mechanicalness it does
not have.

---

## 2. commit-example-c-overforbids-fill-change (reader-02, diagrams-01)

Both reporters describe the same collision; they pick opposite readings of
"a layer carrying either" and reach the same place. Verified: §20.3 step 4
quantifies over stored tiles —

> The test is the effect on a stored tile … a change that reaches none of
> these for any tile the layer stores … leaves every stored tile conforming
> and is not what this bars … A layer that stores no tile MAY be
> re-declared freely

— while the Example's branch (c) quantifies over the layer: "A fill change
on a layer carrying either is not an appender's operation at all". §11.3
makes padding positions a property of geometry (`Where Gᵢ · Tᵢ > Eᵢ`),
independent of which tiles are stored. Both separating files check out:
extents (5,5) / tile extents (4,4) with nothing stored, and the same with
only interior tile (0,0) stored. CONFIRMED.

**Downgrade, with the sentence that decides it —** §2.1:

> All text in this document is normative except: §1 (Introduction); any
> text labeled *Note*, *Example*, or *Rationale*; and appendices
> identified as non-normative. `[R-CNF-01]`

The block is headed "**Example — the three shapes a commit takes.**" A
non-normative example cannot narrow what a conforming writer may emit, so
the permitted emit set is unchanged; an appender that obeys the Example
emits a strict subset of conforming files, and every file either appender
does emit is conforming. No reader accepts or rejects differently.
Severity: figure — the defect is confined to the Example block and the
normative text above it is correct.

Repair: re-key branch (c) to step 4's own quantifier — "…on a layer no
stored tile of which carries a padding position or a pad bit", and change
the follow-on to "A fill change that reaches a stored tile's padding
positions or pad bits is not an appender's operation at all (step 4)."
Worth adding while there: a fill change also changes what every
sentinel-addressed tile reads as ([R-IDX-02], [R-TYP-08]), which step 4
permits and the example does not mention.

---

## 3. stored-tile-tense-in-step-4 (quiz-02) — **byte-level: upheld**

The only self-flagged byte-level finding in the batch. I tried to break it
and could not.

The rule: "A commit MUST NOT change a layer's declarations in a way that
alters, for any tile that layer stores, what §14 fixes for its stored
bytes or how they decode". The separating operation is one commit that
both re-declares (say interleaved → planar, or a re-tile, or a channel
type change) **and** writes the sentinel at every disk ordinal, which step
4 itself provides for ("entries for tiles that become unstored written as
the sentinel").

- Reading A ("stores" = the set before the commit): barred.
- Reading B ("stores" = the set the commit publishes, which is empty):
  permitted.

I searched for a sentence fixing the tense and there is none in normative
text. The gloss that looks decisive is not: "leaves every stored tile
conforming" and "makes each stored tile it reaches nonconforming" restate
the same quantifier with the same tense left open. The one place the
document does name a tense is §11.1 —

> a shrink is barred wherever it alters what §14 fixes for a tile the
> layer **already** stores (§20.3)

— and that sits inside a block labelled **Rationale**, which §2.1 strips of
force. So the only text that answers the question is text that cannot
answer it, and it answers the opposite way from the reading step 4's own
effect-test suggests. I cannot quote a sentence that decides it, and this
round's rule is that a downgrade without such a quotation is not a
judgement. So: **byte-level true.**

**The two implementations, concretely.** Library B, asked to `reshape(layer,
newLayout, clear=true)`, emits one commit: new index region of C·N
sentinels, new layer record, new directory, pad, trailer at generation g+1
with the input's file_id; the old payloads and old index become slack.
Library A refuses that commit and reaches the same end state in two —
commit 1 sentinels every entry with declarations untouched, commit 2
re-declares a layer that now stores nothing ("A layer that stores no tile
MAY be re-declared freely" is satisfied under either tense after commit 1)
— producing generation g+2 with an extra stranded index region, directory,
pad and trailer. Those are different byte sequences for the same
operation, and under reading A exactly one of the two libraries is a
conforming updater.

Two honest qualifications for the reconciler:

1. The reporter's damage estimate is overstated. Reading A does **not**
   force "a whole-file rewrite under a fresh file_id": the two-commit path
   above stays inside [R-LIF-01] and preserves file_id and lineage. The
   real cost of reading A is one extra generation's worth of slack, not a
   broken content-address.
2. No reader and no verifier can tell the two outputs' *legitimacy* apart:
   both are conforming files, and the violation reading A would find is a
   history property with no witness. If the maintainer's byte-level test is
   meant to reach only reader/verifier-observable divergence, this falls
   below it. Under the test as written — "which byte sequences a conforming
   implementation may emit" — an updater is a conformance class (§2.3,
   [R-CNF-06]) and its permitted emissions fork.

**Repair** (one clause, plus one consequential): pick a tense in step 4 —
"for any tile the layer stores in the state this commit publishes"
(reading B) or "already stores" (reading A) — and make §11.1's Rationale
match. If reading A is chosen, [R-WRT-04]'s step-4 bar must also be added
to §21.7's list of obligations omitted from the register for want of a
witness, since a same-commit unstore leaves none; §21.1 calls §21.7 "the
account, by class, of what fails" the detectability gate, and the list does
not currently name it. That §21.7 is silent today is itself mild evidence
that reading B is the intent — under B the bar is fully witnessed by
§21.4's tile rows and needs no listing.

---

## 4. profile-digest-byte-selection (writer-02, diagrams-03)

Appendix G item 2: "the identifier its low eight digest bytes read
little-endian". writer-02 read it as the **trailing** eight (digest as a
big-endian numeral); diagrams-03 read it as the **leading** eight (lowest
indices). Two independent readers of one sentence choosing opposite ends is
about as good as evidence of ambiguity gets. writer-02 even computed both
for a real 832-byte file: 0xD44980B7CE79C479 vs 0xC0A188DEDE9C8C78.
CONFIRMED.

Downgrade quote — Appendix G's own preamble:

> It adds no requirement to any actor: a writer ignoring it is fully
> conforming

and §6.2's valid-values column for file_id is `≠ 0`, which both candidates
satisfy. No conformance class's emit or accept/reject set changes; two
*profile adopters* fail to reproduce each other. Severity: design-decision
— the maintainer picks an end; one word ("trailing" or "leading") fixes it.
Recommend "the trailing eight bytes of the digest, read little-endian" if
the intent was the conventional numeric sense, and note that under that
choice "read little-endian" is doing real work (it is the assembly rule,
not the selection rule) — which is diagrams-03's objection and is worth
answering in the text itself.

---

## 5. profile-first-structure-offset (writer-05)

Item 3: "Each structure begins where the previous one ended". §5.2 makes
"structure" a defined term that excludes the front signature block ("the
front signature block; **or** a structure — a stored-tile extent, a record
extent …"), and item 3 uses the word in that defined sense in the same
sentence. So the first structure has no antecedent and nothing fixes its
offset; 16 and 512 both satisfy every word, and the files then differ from
byte 16 on in every subsequent offset, dir_offset, committed_file_length
and trailer CRC. CONFIRMED.

Same downgrade quote as group 4 (appendix adds no requirement); also
[R-SLB-05] placement freedom and §5.2 make a leading gap slack, so both
files are conforming. Severity: design-decision. Repair: "The first
structure begins at offset 16." Ironic aggravation worth citing to the
maintainer: the closing recap claims item 3 closes "gap *extent*, which
placement freedom ([R-SLB-05]) leaves open" — and the head-of-file gap is
the one instance it does not reach.

---

## 6. profile-recap-omits-item-10 (diagrams-04)

Verified by reading the recap against the ten items: gap content (3), gap
extent (3), record/sub-record order (3), fill default (7), all-fill
sentinel (6), one generation (4), alignment/slab (5), version_minor (8),
derived file_id (2), producer pinning (1 and 9). Item 10 (NFC
normalization, [R-ENC-14] a SHOULD) appears nowhere, though it meets the
paragraph's membership test exactly. The guard sentence — "Read the
numbered items as the list; this paragraph names what they are for, not how
many there are" — disclaims the count, not the kinds. CONFIRMED, editorial,
not byte-level (non-normative appendix; item 10 itself is intact and states
its own justification). Repair: add "; and name normalization, which
[R-ENC-14] states as a SHOULD" to the recap.

---

## 7. compactor-offset-enumeration-third-case (writer-04)

[R-WRT-07]: "No other record payload carries a file offset: MU = 0 records
by rule (§7.2), and an MU = 1 type the compactor does not implement never
reaches this step ([R-WRT-06])." §7.2 admits a third case explicitly:
"Records with MU = 1 carry further references only where this
specification or registry review (§10) defines them". A later-minor MU = 1
type that the compactor *does* implement is caught by neither clause, and
[R-WRT-05]'s byte-identical re-emission would then carry stale embedded
offsets into a relocated file. CONFIRMED.

Not byte-level, and the reporter's own reason is the right one. §7.3
assigns exactly two types; every other MU = 1 type is one a compactor built
from this text does not implement, and

> A compactor MUST refuse to compact a file carrying any record whose type
> it does not implement with MU = 1 `[R-WRT-06]`

closes it. I checked the one escape route the reporter did not: an
*experimental*-range MU = 1 type a vendor compactor does implement. §21.6
puts that file's fate elsewhere — an experimental-range type carrying
MU = 1 obliges the reader to reject the file ([R-CNT-15]) while leaving the
file conforming — and a compactor is a reader first (§20.1), so it never
reaches the relocation step either. No implementation of *this* text emits
a different byte. Severity: design-decision (a forward-compatibility clause
the maintainer may or may not want). Repair as the reporter drafts it, and
have it cover the experimental case too: "…and an MU = 1 type this
specification does not assign is relocated only under the rules its
registration or defining document states."

---

## 8. slack-total-when-no-live-trailer (writer-03) — PARTIAL

The reporter's claim is that [R-CNT-21]'s MUST cannot be discharged when
the trailer gate fails, "because F is defined nowhere except as the live
trailer's committed_file_length", and excludes reading (c) (F = physical
size) on that ground.

That exclusion does not survive the document. §19.1 step 1:

> **End of file.** Obtain the transport-authoritative file size F
> (`[R-CNT-10]`).

F is in hand at step 1, before the trailer is fetched, for every reader and
verifier, local or remote. F5's instance cell glosses it the same way —
"F (physical file size); committed_file_length". So the partial-total
formula *is* evaluable at F8 and F14: F less the bytes the walk claimed,
with F the transport size. The reporter quoted F5's cell as evidence that
the two are different quantities and then still concluded that only the
committed one is F.

What survives, and is worth the maintainer's time, is the overloading
itself: §5.1 ("the live trailer's committed file length F") and §15.3
("with F the committed file length") against §6.4 and §19.1 step 1 ("the
transport-authoritative file size F"). For a conforming file they coincide;
for exactly the files at issue — F17, where committed_file_length ≠ the
transport size — they do not, and two verifiers computing "F less the bytes
claimed" from the two Fs print different mandatory numbers for the same
bytes. So: PARTIAL — the hole is not where the reporter put it, but there
is a hole one row over.

Not byte-level. [R-CNF-11]:

> An established violation takes priority: a verifier that has established
> any violation reports *nonconforming*, however many requirements it was
> unable to check

and the per-requirement report "constrains the report and not the verdict".
The verdict is nonconforming at F8/F14/F17 under every reading; only a
diagnostic line moves. Severity: design-decision. Repair: say once, where F
is introduced (§5.1), that F denotes the transport-authoritative file size
and that a conforming file's committed_file_length equals it; then state in
[R-CNT-21] which F the partial total uses when they differ.

---

## 9. slack-total-walk-detected-layer-rejection (verifier-02) — PARTIAL

Real tension, and the reporter's separating file is well built. But the
fork is not inside [R-CNT-21]; it is between [R-CNT-21] and [R-LIF-08].

[R-CNT-21] is categorical and does choose:

> a rejected layer's claimants are not enumerated, **whether or not the
> rejection impeded reading them**

That parenthetical exists precisely to defeat the reporter's Reading A, so
"keep the layer, report the exact 27" is refuted by the rule that states
the obligation. §9.7 then says something else:

> Where the walk does not complete — a scope-level rejection **blocks**
> enumeration, or the verifier stops at the first violation ([R-CNF-11]) —
> the sum is reported as partial

A verifier reading only [R-LIF-08] finds that an L18/L40/L41/L42/L48
rejection blocks nothing (the claimants had to be enumerated to detect it)
and reports 27/exact; one reading [R-CNT-21] drops them and reports
75/partial. CONFIRMED that two verifiers print different mandatory numbers;
PARTIAL as to the reporter's diagnosis of where the under-determination
lives.

The reporter's refutation of behaviour (i) — summing claimant lengths
under-counts when claimants overlap, which "never an under-count" forbids —
is correct and is worth writing into the text, since summing is the
natural implementation and the union is not stated.

Not byte-level: same [R-CNF-11] quote as group 8; the layer rejection that
triggers the question is itself an established violation, so the verdict is
nonconforming either way.

Severity: design-decision. Repair, in two parts: (a) align §9.7's "blocks
enumeration" with [R-CNT-21]'s categorical rule, or narrow [R-CNT-21] to
rejections that actually impeded enumeration; (b) say the total is F less
the *union* of the claimed ranges. Worth the maintainer's judgement on (a):
under the drop rule, the reporter's 256-byte file whose only defect is a
four-byte overlap reports a mandatory slack figure of 75 against a true 27
— and §22.3 calls that figure "the number that distinguishes a working file
from a padded one".

---

## 10. foreign-major-register-applicability (verifier-03) — PARTIAL

§2.3 decides it, as the reporter says:

> a file declaring another major is neither conforming nor nonconforming
> under it: a reader refuses such a file on capability grounds (§6.3,
> `[R-CNT-07]`), and that refusal is not a finding about its bytes

The reporter's supporting claim — that nothing in §21 points at §2.3 — is
where it slips. §21.6's closing paragraphs address exactly this file:

> The first is **version_major naming a major this reader does not
> implement**: the reader rejects the file (`[R-CNT-07]`), but the file can
> be perfectly conforming under that major … Neither is a register row: the
> register enumerates file-conformance violations (§21.1), and a file this
> document declines to judge is not one.

So §21 does tell a reader that a foreign-major file is not the register's
subject; it just does not do so in §21.1 or in the F5/F9/F10/F13/F16 rows.
PARTIAL.

Not byte-level: the reader refuses the file under both readings — on
capability grounds or as a validity error — so no byte is accepted that
would otherwise be rejected. Only the verifier's verdict label and the
diagnostic class differ, and §6.3 already tells a reader which diagnostic to
give. Severity: editorial. Repair: one clause in §21.1 — "every row below
is a condition of format major 1; a file declaring another major is outside
the register (§2.3, §21.6)".

---

## 11. outcome-follows-scope-vs-ignore-record (register-02)

§21.1 states the outcome column twice as scope-derived ("the outcome class
its scope determines (§2.4)"; "the outcome follows from that scope, never
from the severity of the corruption"), and [R-CNF-08]'s map yields only
reject-file / reject-layer / reject-tile. All ten §21.5 rows carry
ignore-record, and §18.1 says the owning scope of a user-metadata record is
file or layer. So §21.1's general statement is contradicted by 10 of 121
rows. CONFIRMED — though both §21.5's preamble ("whatever the containing
scope") and §18.1 itself state the carve-out, so no row is left without an
answer.

Not byte-level. Deciding sentence, [R-CNF-12]:

> For a nonconforming file no acceptance obligation exists — a reader MAY
> reject it upon detecting any violation, including violations whose
> assigned detector is the verifier.

Every R-row is a violation, so a reader that misreads §21.1 and rejects the
file and one that follows [R-CNT-25] and ignores the record are both
conforming. I checked the one place a fork could reach a conforming file —
§21.6's experimental-encoding entry — and it states its outcome directly:
"Ignored (ignore-record); the file is conforming", with no reference to
scope. Severity: register-bookkeeping. Repair: in §21.1, "…the outcome
class its scope determines (§2.4), except where a governing rule assigns
one notwithstanding the scope — the quarantine of [R-CNT-25], whose rows
are §21.5's".

---

## 12. governing-rule-parenthetical-convention (register-03)

True and unstated: every Governing rule cell has the shape
`` `[R-XXX-NN]` (R-YYY-MM, …) ``, the parenthesized identifiers are not in
§2.2's defined `[R-<PREFIX>-<NN>]` form, and L26's parenthetical is not an
identifier at all — verified: `` `[R-CNT-18]` (§7.3 registry table) ``. §21.1
speaks in the singular ("the requirement that defines it", "the rule it
cites") and [R-VEC-02] requires a manifest to record "that row's governing
requirement identifier", singular. CONFIRMED.

Not byte-level: the artefact at risk is a manifest, and [R-VEC-01] makes
the corpus "evidence of conformance, never its definition". The reporter
checked every multi-citation cell for a case where bracketed and
parenthesized rules answer differently and found none; spot-checking F1,
L2, L21, L30 and F17 I agree — the parentheticals are cross-references.
Severity: editorial. Repair: one sentence in §21.1 — "The bracketed
identifier is the row's governing rule; parenthesized identifiers and
section references are cross-references that bear on it and do not govern."

---

## 13. verifier-row-serve-unchanged-list (register-04) — PARTIAL

The omission is real: §21.1's parenthetical names ([R-SER-08], [R-CNT-22])
and not [R-MTA-05], which governs F27 and L48, the pair §21.6 says was most
recently moved into the register.

The consequence is not. The rows carry the reader's side in their own
Condition cells — F27: "the document stays readable and readers process it
unchanged"; L48 the same words. An implementer reading F27 does not have to
reach §21.1 to learn that the reject-file label binds no reader. And
[R-CNF-12] plus §24's own Note ("an implementation that instead rejects the
whole nonconforming file is exercising [R-CNF-12]'s licence, not failing
the vector") make both behaviours conforming anyway. PARTIAL, editorial,
not byte-level. Repair: add `[R-MTA-05]` to the parenthetical, or replace
the list with "for several such rows — the row states which".

---

## 14. extent-may-always-grow-vs-lz4-cap (adversary-02)

Verified both halves. §20.3: "an extent MAY always **grow**", unqualified.
[R-COD-07]: "Writers MUST NOT declare this codec for a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes … and a reader MUST
treat such a declaration as a validity error at layer scope, checkable from
declarations alone." The reporter's e02/e03 pair is right: growing an
extent from 0 to 1 on a codec-4 layer with T = 2³¹ turns a conforming file
into an L44 file with nothing stored. The only cross-reference is §17.2's
Note ("The escape is not durable…"), which §2.1 makes non-normative.
CONFIRMED.

Not byte-level. Deciding sentence, [R-CNF-05]: "A writer MUST emit only
conforming files" — a MAY cannot license output a MUST forbids, and
[R-COD-07]'s reader clause is unconditional, so both readings agree on both
files. What changes is what a careless writer emits, and the document
already bars it. Severity: editorial. Repair: "an extent MAY always grow,
provided the layer's declarations remain valid for the tiles it then
addresses ([R-COD-07])" — and the neighbouring "A layer that stores no tile
MAY be re-declared freely" is over-broad in the same way and takes the same
qualifier. (That sentence is also group 3's subject; the two repairs must be
made together.)

---

## 15. slab-decidable-from-index-bytes (quiz-03)

Verified. §16.2 closes with "so this invariant stays decidable from index
bytes alone", and classifying an entry as structural requires §15.3's rows,
one of which is "offset + length overflows, or offset + length > F − 64
(non-sentinel)" — §15.3's own preamble reads "For each entry, with F the
committed file length". F is not an index byte. CONFIRMED as an inaccurate
justification.

Not byte-level. §19.1 step 1 obtains F before anything else is fetched, and
§6.4's accounting puts the trailer in request 1 and the directory in
request 2, so no conforming actor is ever in the position the sentence
describes and every implementation classifies the same entries the same
way. Severity: editorial. Repair: "…so this invariant stays decidable from
the index entries and F, without fetching a single stored tile" — which is
the claim that actually matters and is what the sentence's contrast with
the crc case is for.

---

## Coverage

23 input ids, 15 groups, union of member_ids = the input list, no id in two
groups, none dropped. Counted twice by hand against the id list in the
task. Byte-level upheld: 1 (stored-tile-tense-in-step-4). Byte-level
downgraded: 22 ids across 14 groups, each with the quotation that decides
it recorded above.

Gaps I will not paper over: I did not build any file for group 3 or group 9
— I reasoned from the text and from the reporters' constructions, which I
checked for internal consistency but did not execute. For group 1 I
re-derived 268 mechanically and checked the four disputed cells and the
CRC-equality rows by hand, but I did not re-derive any reporter's 272/273/
274 line by line; the point that matters — that three reporters applying a
"mechanical" rule got three different totals — needs no such derivation.

---
*Editorial note: one ordinary-English word meaning "the thing that came before" was substituted throughout this verbatim transcript (to "antecedent"), per the repository's vocabulary gate. No other change was made.*
