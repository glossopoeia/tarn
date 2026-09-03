# Round 29 — triage pass: CORRECTNESS lens

## Disclosure of what I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, read in
  targeted extracts by line range (never listed a directory):
  lines 1–120 (front matter, §1, §2.1–2.2), 120–420 (§2.3, §2.4, §2.5, §3.1, §3.2),
  433–500 (§4.1–4.4), 584–620 (§4.7), 756–935 (§6.1–6.4), 1234–1305 (§9.2),
  1369–1490 (§9.5–9.7), 1584–1680 (§11.1–11.4 head), 1797–1824 (§12.3),
  1922–2120 (§14), 2122–2200 (§15.1–15.3), 2245–2350 (§16), 2415–2445 (§17.2
  window text), 2496–2554 (§17.3, §17.4), 2576–2760 (§18.2), 2929–2960 (§19.3),
  3076–3350 (§20.3), 3404–3546 (§20.5), 3546–3700 (§21.1, §21.2, §21.3 head),
  3743–3870 (§21.4, §21.5, §21.6), 3868–3935 (§21.7, §21.8), 3932–4022 (§21.9),
  4479–4697 (Appendices G and H). Plus two greps: section headers, and a
  whole-document whitespace-normalised search for "sole resolved".
- I read NO walk transcript, no other triage pass's notes, no docs/, no
  PLAN.md, no AGENTS.md, no conformance/, no registry.json, no git history,
  no web. I did not run an orienting directory listing.
- Everything below is checked against the spec text, not against the
  reporters' accounts of it.

## Method

For each finding: (1) locate the quoted text and verify the quotation and its
context; (2) ask whether the reporter's second reading is permitted by the
words as they stand in context, or only by a reader applying a clause detached
from its own case-key/scope; (3) apply the byte-level test and, where I
downgrade a reporter's flag, quote the sentence that decides it.

---

## G1 — cnf12-verifier-duty-scope  (reader-01, register-02)

Text checked, §2.4 [R-CNF-12], verbatim:
"Deviation from a SHOULD is not a violation for this purpose: §21's register
enumerates MUST-level conditions only, and a verifier reports a SHOULD
deviation as an advisory that does not bar certification. A verifier owes no
search for one: §2.3's duty to check every file-level requirement runs to the
MUST-level conditions §21 inventories, and a SHOULD deviation is reported
where the verifier observes it and not hunted for."

§21.7, verbatim: "The instrument is the checks this specification obliges an
actor to perform, and deliberately not the register's own rows — a test keyed
to the rows would make §21.1's completeness clause vacuous, every omitted
condition being undetectable by construction."

§2.3 [R-CNF-11] states the duty unqualified: "A reader that additionally
checks every file-level requirement — including those ordinary readers are
exempted from — and certifies conformance."

Both reporters are accurate. The restrictive/appositive fork is real English
and the restrictive reading makes §21.7's disclaimer false of its own
instrument. Both reporters independently picked the appositive reading and
both swept for an omitted MUST-level detectable condition and found none.

Correction to reader-01's framing: reader-01 says "the reader half of that
instrument is already row-keyed: by §19.2 and §21.1 a reader's obliged checks
are exactly the rows whose Detector cell reads *reader*." That overstates.
[R-CNF-04] does make row-detection a reader duty, but readers also carry
duties stated directly by governing rules independent of any row — [R-CNT-06]
("A reader MUST validate, in order: the trailer magic; the trailer CRC; …"),
[R-CNT-04], [R-IDX-03]'s classification table, [R-SER-07]. So the reader half
of §21.7's instrument is not purely row-keyed, and §21.7's disclaimer is not
already false on that ground alone. The [R-CNF-12] fork is still real.

Byte-level: NO. Premise stated so it can be attacked: I rest the downgrade on
the register in fact being complete for detectable MUST-level file-conformance
conditions, so that reading (A) and reading (B) have the same extension and no
file can be constructed on which two verifiers diverge. Two independent
reporters swept for an omitted condition (reader-01 §4–§18 requirement by
requirement; register-02 over 51 "validity error" clauses, 18 "MUST NOT emit",
111 non-governing identifiers) and neither could name one. I did not repeat
that sweep. Deciding text: §21.1, "a *detectable* file-conformance violation
this specification names and the register omits is a defect in this document".
If someone names an omitted detectable MUST-level condition, this group
becomes a verifier-verdict fork on a nameable file and my downgrade fails.
This is the group I would attack first.

Severity: design-decision. Repair: make the clause appositive in terms —
"runs to MUST-level conditions, which §21 inventories" — or, better, state
that a verifier's duty runs to every MUST-level file-level requirement and
that §21 is the inventory of it rather than its bound.

---

## G2 — s14bar-growth-vs-padding-list  (reader-02)

§20.3 step 4 quoted accurately. The bar's list does include "the set of
padding positions (§11.3)", and a growth over a stored edge tile does alter
that set. The list is subordinated in terms: "The test is the effect on such a
tile, and the list names where that effect arises rather than standing on its
own". So reading (i) — the list as the test — is not permitted by the words;
the document says the list does not stand on its own.

But reader-02's residual point survives on a sharper footing than the one
reported: the *general* clause ("alters … what §14 fixes for its stored bytes
or how they decode") also reaches a growth, because §14 fixes a different
padding set for that tile afterwards, and the two carve-out examples are both
shrink-direction ("a filter whose mandated stride makes it the identity", "a
new padding position whose stored byte already holds the fill"). What actually
licenses growth is the express permission with its own stated ground: "an
extent MAY **grow**, since a position that becomes real held, for each channel
the position carries, that channel's fill (§14.5), and fill is a legal sample
value … a growth is permitted exactly where the geometry it produces satisfies
every rule that geometry is subject to." §11.1's Rationale agrees.

So: PARTIAL. The defect is not "the list bars growth" (the list is expressly
not the test) but "the general clause reaches growth and only the express MAY
takes it back out, with the carve-out illustrating only the shrink direction".

Byte-level: NO. Deciding text, §2.3 [R-CNF-02]: "File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or environment."
The §14 bar's subject is a commit; the file a growth produces is conforming on
its own bytes under both readings, and a creator can emit those bytes in one
commit. Premise: that the byte-level test asks about the set of byte sequences
that may be emitted as *files*, not about which of two routes an updater may
take to a file that is emittable either way.

Severity: editorial. Repair: add the growth direction to the carve-out, or say
the express growth permission is an exception to the bar.

---

## G3 — compactor-minor-floor-witness  (reader-03)

§20.5 verbatim: "Otherwise version_minor follows `[R-CNT-26]`'s floor. Neither
obligation has a witness in the output alone (§21.7)."

[R-CNT-26] verbatim: "A writer SHOULD emit the lowest version_minor that
defines every feature present in the file — for a file expressible under this
text, 0".

§20.5 itself enumerates exhaustively the ways a conforming output can carry a
later-minor feature: "a carried ignore-lane bit (§6.3) or an unrecognized
`tarn.` key in a record it never decoded (§18.3), the two of §10.1's four
vehicles §21.6 makes conforming, the other two reaching such a file only as
values this text still registers as reserved-range violations".

CONFIRMED. On an output with flags = 0 and no unrecognized `tarn.` key, the
floor is determinately 0 and version_minor sits at trailer offset 10, i.e.
F − 54 — a witness in the output alone. Appendix G item 8's defence ("this
item's floor turns on which features the compactor implements") does not reach
this branch, because the output carries no feature at all.

Byte-level: NO. Deciding text, [R-CNF-12]: "§21's register enumerates
MUST-level conditions only, and a verifier reports a SHOULD deviation as an
advisory that does not bar certification." Both obligations are SHOULDs.

Severity: editorial. Repair: restrict the sentence to the first obligation, or
say the [R-CNT-26] branch has a witness only where the output carries no
later-minor feature.

---

## G4 — shrink-witness-antecedent  (reader-04)

Quoted sentence verified verbatim. Antecedent of "This" is not spelled out.

Reading (a) — the shrink case generally — makes "the live state being clean"
false, as the reporter says: a shrink that turns real positions into padding
of a still-stored tile leaves that tile violating [R-SER-05], which §21.4
registers as T4. But that self-falsification is exactly why (a) is not
sustainable: the surrounding paragraph is built on the unstore/de-address
rescue ("Unstoring that tile in the same commit does not rescue it either …
whether or not the new state still stores it"), and (b) is the only reading on
which the sentence is true.

Reporter's "further wrinkle" is wrong and I record it as refuted: the reporter
says "on §21.7's own test the §14 bar has no witness anywhere". Where the bar
bars a change that damages a tile the new state still stores, the damage does
show in the live state as T4/T5, and that is precisely the contrast the
sentence draws — the rule is "stated here and not left to the rows" only for
the sub-case where the damaged tile is gone from the live state.

PARTIAL: loose antecedent is a real editorial defect; reading (a) and the
wrinkle are not.

Byte-level: NO. Deciding text, §14.5 [R-SER-05]: "a verifier MUST check it,
and a violation is a validity error at tile scope" — the still-stored damaged
tile is registered (T4) under both readings, so [R-CNF-05] bars a conforming
writer from emitting it either way.

Severity: editorial. Repair: name the antecedent ("A shrink whose damage falls
on a tile the new state no longer stores is precisely where …").

---

## G5 — witness-ground-misapplied  (reader-05)

§21.7 verbatim: "Distinguish an unwitnessed condition from a requirement that
states **no condition a file can exhibit**."

Accurate that both of §21.7's defined grounds quantify over files, and that
the §14 bar's and the planar-ordinal bar's subject is a relation between two
generations. But two corrections weaken the finding:

1. §20.3's sentence ("This is precisely where the §14 bar has no witness, the
   live state being clean") does not cite §21.7 and reads as plain English
   about the live state, not as an invocation of §21.7's defined class. Only
   §20.5's sentence cites §21.7.
2. Committed-prefix immutability (§9.1, §9.2) means a bar-violating commit's
   output does physically retain the superseded generation's structures as
   slack, so it is not obvious that "no file is in that state"; what is true
   is that slack content is unconstrained ([R-CNT-21]) and no obliged check
   reaches it, which is the *unwitnessed* ground rather than the
   no-condition ground.

PARTIAL. The criticism bites on §20.5's citation; on §20.3 it does not.

Byte-level: NO — the reporter's own ground is right: both §21.7 grounds keep a
condition out of the register, so nothing about the register's contents or any
actor's behaviour turns on the label.

Severity: editorial.

---

## G6 — compaction-regeneration-trigger  (writer-01)

§20.5 [R-WRT-07] verbatim: "…except that relocation re-points extent slots,
regenerates each relocated tile-index region (entry offsets new; …)". Quoted
accurately. The trigger is the *region* being relocated; what forces
regeneration is the region's entries pointing at moved tiles. The same
sentence grants free placement: "it is free to place structures anywhere §5.2
admits and every declared layout invariant permits".

CONFIRMED. The divergent case (tiles move, region lands where it was) is
constructible in principle and the literal trigger owes no regeneration there.

Byte-level: NO. Deciding text, the same rule's closing sentence: "The output's
reference arrays MUST equal the live generation's bit for bit
(`[R-MDL-02]`)" — plus T1 (entry crc) and the [R-CNT-02] partition. The output
of the literal reading is nonconforming, so [R-CNF-05]/[R-CNF-06] bar it under
both readings.

Severity: editorial. Repair: "regenerates each tile-index region any of whose
stored extents the output relocates".

---

## G7 — resource-decline-scope-declarations  (writer-02)

[R-ERR-04] verbatim: "A file exceeding any of these remains conforming, and a
reader MAY decline it — at the whole file, or at the narrowest scope whose
declarations exceed what it can serve, a layer or a tile."

[R-COD-06] verbatim: "a wider window is conforming and merely permits a
conforming reader to decline the tile or the layer on resource grounds
(`[R-ERR-04]`)."

§18.2's Note verbatim: "a reader that instead declines on resource grounds
under `[R-ERR-04]` does so at the whole file, a document having no declared
size and so no narrower scope whose declarations that rule can measure."

The word "declarations" is used loosely across the three, which is a real
editorial inconsistency. But the reporter's reading (b) — that [R-COD-06]'s
tile-scope decline is "unlicensed" — is refuted by two express texts:
[R-COD-06] itself names the tile, and §2.3's cannot-establish list names "when
it declines a layer's or a tile's decode on resource grounds". §18.2's
whole-file result is also independently forced by [R-ERR-04]'s own scope
enumeration, "a layer or a tile", of which a top-level user-metadata record is
neither.

PARTIAL. Byte-level: NO — deciding text is [R-ERR-04]'s "A file exceeding any
of these remains conforming, and a reader MAY decline it": a MAY at every
granularity, so no file moves between must-accept and may-reject.

Severity: editorial.

---

## G8 — shuffle-identity-universal  (writer-03, diagrams-04)

Both report the same sentence, Appendix G item 5: "elsewhere it changes the
stored bytes of every tile it touches." Same defect, two constructions.

I verified the permutation arithmetic against [R-COD-10] ("the filtered image
places byte i of group j at offset i · n + j"):
- s = 2, n = 2: output[0]=src[0], output[1]=src[2], output[2]=src[1],
  output[3]=src[3] — the transposition of the middle two bytes. `01 02 02 03`
  is fixed; `01 02 03 04` → `01 03 02 04`. writer-03's arithmetic is right.
- diagrams-04's construction: interleaved, one uint16 channel, P = 4, Q = s = 2,
  L = 8, n = 4, all bytes 0x01 — a permutation of eight equal bytes is those
  eight bytes. Right, and it is a legal sample value under [R-TYP-05] and not
  an all-fill tile (fill 0x0000), so item 6 does not exclude it.
- writer-03's "for s ≥ 2 and n ≥ 2 the byte at source offset s lands at offset
  1" checks out: source offset s is byte i = 0 of group j = 1 → 0·n + 1 = 1.

CONFIRMED. The universal is false; the item's operative conclusion (pin the
filter) is untouched.

Byte-level: NO. Deciding text, Appendix G's own preamble: "It adds no
requirement to any actor: a writer ignoring it is fully conforming", and
[R-CNF-01]: "All text in this document is normative except: … appendices
identified as non-normative."

Severity: editorial. Repair: "elsewhere it changes the stored bytes of any
tile whose decoded image the permutation does not fix".

---

## G9 — profile-completeness-tiling-layout  (writer-04)

Preamble verbatim: "can adopt this profile, which closes the degrees of
freedom this format deliberately leaves open."
Item 2 verbatim: "two files carrying the same arrays can legitimately differ
in tiling, layout, and codec."

Item 1 closes the codec. No item closes tiling or layout. §11.3's Note: "Tile
extents are a writer's choice, and this specification imposes none." The
closing inventory omits tiling and layout, and also omits the filter that item
5 does pin — though that inventory disclaims itself ("Read the numbered items
as the list; this paragraph names what they are for, not how many there are"),
so the omission there is defused and only the preamble's completeness claim
and the missing items stand.

CONFIRMED. Byte-level: NO, same deciding text as G8.

Severity: editorial. Repair: either add fixed declared tile extents and a
fixed layout as an item, or say tiling and layout are inputs to the profile
rather than freedoms it closes.

---

## G10 — detectable-quantifier-scope  (writer-05, verifier-01, adversary-03)

All three report the same defect: the scope of "by such a check" in §21.7's
detectable clause. Verified verbatim:

"A condition this specification names is **unwitnessed** where, for every file
exhibiting it, some file that does not exhibit it cannot be told apart from it
by any check this specification obliges a reader or a verifier to perform. It
is **detectable** in the contrary case: where some file exhibiting it is
separated by such a check from every file that does not. The two are stated
over the same subject, and each quantifier is the other's dual, so each is
exactly the negation of the other…"

The unwitnessed clause fixes ∀f ∃g ∀check ¬sep. Its negation is
∃f ∀g ∃check sep. The detectable clause's word order ("separated by such a
check from every file that does not") reads as ∃f ∃check ∀g sep, which is
strictly stronger and is not the negation. §21.1's restatement, with the check
set off in commas ("separated, by a check this specification obliges a reader
or a verifier to perform, from every file that does not"), reads the same way.
So the asserted duality is evidence for one parse and the syntax for the
other. CONFIRMED.

verifier-01's F35 test checks out and is worth keeping: [R-CNT-15] gives the
reader an unknown-type-with-MU=1 check (failure set reserved∧MU1 ∪
experimental∧MU1) and the verifier a reserved-range check (failure set
reserved∧MU1 ∪ reserved∧MU0). Neither failure set is contained in F35, so no
single obliged check separates an F35 file from every non-F35 file; under the
one-check parse F35 loses its row, which the register carries.

writer-05's second point is separate and also right, and I fold it into the
repair: "separated" is undefined between "some individual check's result
differs" and "the two files get different verdicts". Under the verdict reading
almost nothing is detectable, because the complement contains files
nonconforming for unrelated reasons that share a reject-file verdict.

Byte-level: NO. Deciding text, §21.1: "each row *restates* its governing rule,
and where a row and the rule it cites diverge, **the rule governs**", and "a
*detectable* file-conformance violation this specification names and the
register omits is a defect in this document" — a missing row is a document
defect, not a licence. Readers' duties under [R-CNF-04] run to the rows the
register actually carries, and those rows are fixed as printed under either
parse.

Severity: design-decision. Repair: one word — "separated by *some* such check"
(distributive, the parse the duality claim needs) — plus a clause defining
"separated" as a difference in an individual check's result.

---

## G11 — recovery-report-no-candidate  (writer-06)

[R-LIF-06] verbatim: "The probe begins at the largest 64-aligned offset o with
o + 64 ≤ the physical file length; a candidate whose whole-file
re-verification fails was not a commit state, so the tool continues the probe
past it, and MUST report the candidate it settled on and how many it
rejected."

Both no-candidate states are reachable and unaddressed: a file below 64 bytes
admits no o at all, and a file all of whose candidates fail re-verification —
a case this very sentence contemplates — terminates with nothing settled.
CONFIRMED.

Byte-level: NO. Deciding text, §9.6: "no verdict turns on the probe: a file
whose final 64 bytes are not a valid trailer fails `[R-CNT-06]`'s gates on the
bytes handed over". §2.3 makes recovery tools no conformance class.

Severity: editorial. Repair: add "or, where none survived, that none did".

---

## G12 — slb04-trigger-omits-declaration-change  (writer-07)

[R-SLB-04] verbatim: "A writer or updater whose commit changes the stored-tile
set, the run partition, or the byte placement of any run of a slab-declared
layer MUST either re-establish the invariants for every such run — or clear
the declaration in the new generation".

Case (2) — changing A_slab alone — escapes both of the reporter's readings,
not just reading (b): the stored-tile set, the run partition ([R-SLB-02] keys
it to S alone: "Run r of a block starts at ordinal block_start + r·S") and the
byte placement are all unchanged; only the alignment the runs must satisfy has
moved. So the gap is wider than the reporter's (a)/(b) framing allows.
Case (1) — introducing a declaration — turns on the untensed
"slab-declared layer", and §20.3's neighbouring alignment clause shows the
document knows how to say it: "an aligned layer's stored tiles — every one the
new state keeps, not only those this commit adds — satisfy its invariant or
the declaration is cleared (`[R-SLB-01]`, `[R-CNF-05]`)".

CONFIRMED. Byte-level: NO. Deciding text, §21.3 rows L41 and L42 — a run whose
stored tiles are unpacked, or whose first stored tile's offset is not a
multiple of A_slab, is a verifier-detected reject-layer violation whatever
[R-SLB-04]'s trigger says; [R-CNF-05] ("A writer MUST emit only conforming
files") therefore bars the output under both readings.

Severity: design-decision. Repair: add the declaration itself to the trigger
and give the trigger a tense — "changes the stored-tile set, the run
partition, the byte placement, or the slab declaration of a layer slab-declared
in either generation".

---

## G13 — register-biconditional-overreaches  (verifier-02, register-01, adversary-04)

§21.7 verbatim: "The register carries a row for a condition exactly where it
is a detectable file-conformance violation, so an unwitnessed condition is
absent from it by that clause's own terms rather than in breach of them."

All three report exhibits of one defect: rows the register carries whose
conditions are unwitnessed under §21.7's own test.

F1 (verifier-02, register-01). I checked the construction independently. Take
f with the trailer magic byte-reversed and its trailer CRC recomputed; take g
with those eight bytes zeroed and the CRC likewise recomputed. [R-CNT-06]
orders validation — "A reader MUST validate, in order: the trailer magic; the
trailer CRC; the version gate … Any failure is reject-file" — so the magic
check fails identically on both and nothing later runs. The same pairing works
for the front-block instance against [R-CNT-04]'s byte-equality check. The
only candidate for a separating check is [R-ENC-02], whose text is a
prohibition on a response — "a reader encountering what appears to be a
byte-swapped signature (§6) MUST treat the file as invalid (reject-file),
never as a foreign-endian file to be adapted" — satisfied vacuously by a
reader that never looks. So F1 is unwitnessed under *either* parse of G10's
ambiguity, and the biconditional is false of it. §21.1 names F1 as a strict
specialization of F6/F8 in terms, which is the same fact stated positively.

T13, T15, T16, T23, T26 (adversary-04, and adversary-02 in passing). Verified
against §21.4: each row's own Condition cell says its detection is another
row's — T13 "the check that detects it is T25's, and this row records the
cause rather than a procedure of its own"; T15 "T24's or T25's"; T16 "T24's";
T23 "T25's"; T26 "T2's or T4's". Pairing a file exhibiting the cause with a
file exhibiting a different cause that fails the identical check leaves no
obliged check separating them, so all five are unwitnessed and all five carry
rows. T26 says so of itself: "a wrong stride with no such structural
constraint is undetectable, §21.7".

adversary-04's asymmetry is the same defect seen from the other side and I
verified all three declines: §16.2's Note "Because this rule's detection *is*
`[R-SLB-03]`'s, a stale declaration carries no register row of its own";
§9.5's Note "Residue past a completed commit carries no register row of its
own"; §20.5 "Neither obligation has a witness in the output alone". The
register declines rows on exactly the ground on which T13/T15/T16/T23/T26 take
them.

CONFIRMED. Byte-level: NO. Deciding text, §21.1's specialization clause:
"where every file exhibiting one row's condition … necessarily exhibits
another's, the file is recorded against the narrower row" — every F1 file
necessarily exhibits F6 or F8, both reject-file at open by an obliged check,
so a reader rejects and a verifier reports nonconforming under both readings;
and for the five tile rows, T24/T25/T2/T4 are the checks and their outcomes
are identical. Plus §21.1: "where a row and the rule it cites diverge, **the
rule governs**". What moves is diagnostic attribution and [R-VEC-02] corpus
bookkeeping.

Severity: design-decision. Repair is a maintainer's choice between: (i) weaken
"exactly where" to the one direction §21.1 actually states normatively and say
the register may carry narrower rows for attribution; (ii) state that a rule
naming a distinguishing predicate obliges a check at that granularity (which
would rescue F1 via [R-ENC-02] and the five tile rows via their cause text);
or (iii) strike the rows. (i) is the least disruptive and matches §21.1.

---

## G14 — s14bar-list-omits-pad-bits  (verifier-03)

Verified: §14.3's Note separates the two objects — "Pad bits are not padding
positions (§11.3)" — and [R-SER-05] constrains them in two separate sentences,
the second being "Every pad bit (§14.3) MUST carry the plane's channel's fill
bit." The §14 bar's list names "the set of padding positions (§11.3) and the
content `[R-SER-05]` fixes there", where *there* is the padding positions; pad
bits appear in none of the five listed effects, and none of the other four
reaches a bool fill change (⌈P/8⌉ unchanged, offsets unchanged, type
unchanged, codec/filter unchanged).

The general clause does reach them, and §20.3's shape-(c) example confirms the
intent by naming "no padding position and **no pad bit**" — but that block is
labelled *Example* and [R-CNF-01] exempts it, so the reporter is right that
the only normative text reaching pad bits is the general clause plus its
"the list names where that effect arises rather than standing on its own".
CONFIRMED.

Byte-level: NO. Deciding text, §21.4 row T5: "In a packed planar bool plane
with P mod 8 ≠ 0, a final-byte pad bit … is not the channel's fill bit |
verifier | certification | `[R-SER-05]`". The permissive reading's output is
nonconforming on its own bytes, so [R-CNF-05] bars it either way; and the
general clause bars strictly more than the list, so the divergence cannot run
the other way.

Severity: editorial. Repair: add "and the pad bits `[R-SER-03]` gives it" to
the list's first item.

---

## G15 — sole-resolved-byte-misattribution  (verifier-04, register-06)

I re-ran the whole-document search with newlines collapsed. "sole resolved"
occurs exactly twice: §21.1's sentence and Appendix H's checklist. §14.2
carries [R-SER-08], its Rationale and two Notes, none of which makes the
uniqueness claim. §12.3 [R-TYP-04] does: "In a conforming file this rule
admits no exception; the one case where a reader resolves a byte to a value
rather than passing it through arises only in a nonconforming file, and
`[R-SER-08]` states it."

CONFIRMED, and the two findings are the same defect. Byte-level: NO —
[R-SER-08] itself fixes the behaviour ("MUST report 0x00 as false and every
other byte as true"), and the uniqueness claim is true and stated normatively
in §12.3.

Severity: editorial. Repair: cite §12.3 / [R-TYP-04] instead of §14.2.

---

## G16 — r8-instances-omit-alternatives  (diagrams-01)

Row R8 verified verbatim; its Instances cell is "top-level document; layer
sub-record document" = 2, while its Condition cell states two alternatives
("a magnitude whose binary64 interpretation overflows (`1e400`) and the bare
tokens `NaN`, `Infinity` and `-Infinity` alike"). Neighbours: R5 = 8, R6 = 4,
R7 = 6, each enumerating alternatives × containers. §21.1: "An instance names
a field the condition ranges over, a container it can occur in, one of several
alternatives the condition text states, or any combination of the three."

But §21.1 also supplies an escape the reporter acknowledges: "a row whose
check ranges over a family without the condition changing shape states that
range as a single instance (T24's *any codec*), and one whose members give the
condition materially different shapes enumerates them". R8's "in any form" is
the author asserting one family. Whether an overflowing magnitude and a bare
token give "materially different shapes" is exactly the judgement §21.1 leaves
open.

PARTIAL: the inconsistency with R5/R6/R7 practice is real and the corpus
consequence is real ([R-VEC-03] one vector per instance, so no vector exercises
the bare tokens), but the row is defensible under the family escape, so this
is a bookkeeping decision rather than a demonstrated error.

Byte-level: NO — both alternatives are [R-MTA-04] violations with the same
ignore-record outcome whichever way the cell is written.

Severity: register-bookkeeping. Repair: either enumerate 4 (and move §21.8 to
277) or add a clause to R8 saying the two forms are one family for corpus
purposes.

---

## G17 — frontmatter-structural-gloss  (diagrams-02)

Front-matter gloss verbatim: "**structural** (its value affects where a byte
lies, how it decodes, what a decoded value is, or whether the file is
accepted)".
§4.7 [R-ENC-16] verbatim: "A field is **structural** if its value determines
anything a conforming reader or verifier does with the bytes it reads — where
a byte lies, how it decodes, what a decoded value is, or whether the file,
layer or tile is accepted at all".

The gloss drops "or verifier" and drops "layer or tile". Both droppings bite:
§15.1's entry table marks crc structural and its only effect is reject-tile
(T1); crc_of_crc_array's only effect is reject-layer (L37); §7.2's reserved
record flag bits are verifier-detected (F26). CONFIRMED.

Byte-level: NO. Deciding text, [R-ENC-16]'s own closing sentence: "In format
major 1 `version_minor` is the only descriptive field, and every other field
this specification defines is structural" — which settles the class of every
field the gloss would reclassify — together with §15.1's table cell
"| 16 | 4 | u32 | crc | structural |" and T1's reader-detected reject-tile
outcome. The gloss states no MUST of its own and cannot displace those.

Severity: editorial. Repair: make the gloss quote [R-ENC-16]'s test.

---

## G18 — frontmatter-normative-status  (diagrams-03)

[R-CNF-01] verbatim: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative."

The block sits above the `---` and above `### 1. Introduction`; it is not
labeled Note/Example/Rationale; it is not an appendix. By the list's own terms
it is normative while announcing "*(non-normative)*". CONFIRMED. The
reporter's sweep is consistent with what I saw: §15.1's region-layout
blockquote is likewise unlabelled and correctly normative, so unlabelled
normative blockquotes exist by design.

Distinct from G17: G17 is about what the gloss says, G18 about what status the
block has; the repairs are different edits.

Byte-level: NO — G17's deciding text settles the one case where the block's
content could reach bytes, and every other claim in the block restates §2.2,
§4.7 and [R-VEC-02] faithfully or states nothing a file can violate.

Severity: editorial. Repair: extend [R-CNF-01]'s exception list to cover text
identified as non-normative wherever it appears, not only in appendices.

---

## G19 — err05-chosen-limit-count-vs-l1  (register-04)

[R-ERR-05] verbatim: "Most follow from a field's width, an external format, or
the value domain, and the rest from arithmetic over structures a generation
cannot omit. Two do not: the 512 floor on A … and the 255-byte cap on a
user-metadata key…"

[R-ENC-03] verbatim: "The valid range of every offset, length, extent, and
count this specification defines — entry counts and slab run lengths
included — is 0 to 2⁶³ − 1 inclusive". Alignments are named neither in the
enumeration nor in its parenthetical of marginal members.

L1's instance cell, verified: "layer record extent_offset; layer record
extent_length; sub-record extent_offset; sub-record extent_length; dimension
extent Eᵢ; tile extent Tᵢ; entry_count; slab run length S" — no A, no A_slab.
L39 carries "A above 2^62" as its own instance.

So the 2⁶² ceilings on A and A_slab follow from the value domain only if A and
A_slab are in it, and both [R-ENC-03]'s enumeration and L1's cell say they are
not — in which case a u64 field admits 2⁶³ and the 2⁶² ceiling is a chosen
number, and "Two do not" undercounts. CONFIRMED, and the reporter's preferred
resolution (a) is the one the register was written to.

Byte-level: NO. Deciding text, §21.3 row L39: "Layer record declares a nonzero
alignment A that is not a power of two in 512 … 2^62 | A not a power of two;
A below 512; A above 2^62 | reader | layer access" — same outcome, scope and
detector under both readings.

Severity: register-bookkeeping. Repair: name the 2⁶² ceilings (and the
power-of-two shape) among [R-ERR-05]'s chosen limits, or add A and A_slab to
[R-ENC-03]'s enumeration and to L1's cell (which moves §21.8 to 277).

---

## G20 — f18-cross-major-invalidity-gloss  (register-05)

F18's Condition cell verbatim: "Trailer version_major is 0, a permanently
invalid major in every format major version". §21.2 preamble: "version_major =
0 declares no major at all and is permanently invalid in every one (§21.6)".
[R-CNT-24] verbatim fixes only positions: "the final 64 bytes of a file
contain the trailer magic at F − 64, version_major and version_minor at
F − 56, and a CRC-32C at F − 4 … and the front signature block (§6.1) is
constant." No value constraint. [R-CNT-07], the governing rule, is this
document's: "A reader MUST reject-file when version_major is 0 (invalid) or is
a major it does not implement."

CONFIRMED that the cross-major invalidity claim has no instrument in this
document. The reporter's reading (a) is right that the operative argument —
version_major = 0 does not meet [R-CNF-13]'s premise "a file declaring a
format major other than 1", so the file falls to major 1's rules and
[R-CNT-07] rejects it — does not need the claim at all.

Byte-level: NO. Deciding text, [R-CNT-07] as quoted: every major-1 reader
rejects version_major = 0 at file scope under both readings.

Severity: editorial. Repair: drop "in every format major version" from F18 and
§21.2, or add the invariant to [R-CNT-24].

---

## G21 — enc06-width-check-vs-no-condition  (register-03)

§21.7 verbatim: "`[R-ENC-06]`'s fixed field widths are not a state a file can
be in — the parse is always at the widths this specification fixes, and a
structure written at any other yields different values at them, caught by the
rows for the fields that hold them. Nothing is omitted from the register on
its account, there being no condition to omit."

§19.3 verbatim: "MUST be preceded by full validation of the layer record …
the fixed field widths and u64 value domain of §4 (`[R-ENC-06]`,
`[R-ENC-03]`)".

Both quotations accurate; they cannot both describe an act. CONFIRMED as a
wording collision. Reading (a) — §19.3's item is a parsing convention, not a
check — is the right resolution, and the reporter's aside is also right that
§21.7 slightly overstates: a shifted parse can satisfy every value set and
merely return wrong samples, which is §21.7's own undetectable-content class,
so "caught by the rows for the fields that hold them" is not guaranteed.

Byte-level: NO. Deciding text, [R-CNF-04]: "A reader MUST NOT heuristically
repair a violating structure or infer values this specification does not
define" — which forecloses the only way an implementer could turn this into
divergent behaviour (inventing a width heuristic).

Severity: editorial. Repair: reword §19.3's item as "parses at the fixed field
widths of §4" rather than listing it among validations.

---

## G22 — detectability-gloss-vs-definition  (adversary-02)

§21.7's gloss verbatim: "That is the whole of the test, and it decides any
condition put to it without appeal to a list: ask whether a breach can be made
to leave behind a file no obliged check separates from **a conforming one**."

The formal definition quantifies over "some file that does not exhibit it" —
a class that includes files nonconforming for other reasons. The gloss
quantifies over conforming files, and its outer quantifier is existential
("can be made") where the definition's is universal ("for every file
exhibiting it"). Two divergences, and the gloss contradicts §21.7's own worked
example: an undisclosed zstd dictionary is separated from every *conforming*
file by T25's decode check, so the gloss makes it detectable and owed a row,
while §21.7 and §18.2 both class it unwitnessed — §18.2 verbatim: "dictionary
use the header does not disclose is a writer violation nothing in the extent
shows — an unwitnessed condition, exactly as `[R-COD-06]` has it for a tile
(§21.7)". CONFIRMED, and distinct from G13: G13 is about the biconditional's
exactness against existing rows, this is about the gloss not restating the
definition it claims to be "the whole of".

Byte-level: NO. Same deciding text as G10 and G13: §21.1's "the rule governs"
and "a … violation this specification names and the register omits is a defect
in this document". The rows are fixed as printed; [R-CNF-04] runs readers to
them.

Severity: design-decision. Repair: restate the gloss over "a file that does
not exhibit it" and with the definition's universal, or mark it explicitly as
a heuristic rather than "the whole of the test".

---

## G23 — s14bar-list-names-sample-not-value  (adversary-05)

§3.1 verbatim: "**sample** — the tuple of one value per channel at one
coordinate." §14.2's Example confirms the usage: "its sample occupies bytes
[15, 18)". The §14 bar's third item is "the byte offset of any sample within
the decoded tile image"; what a same-type channel permutation moves is Fᶜ,
"channel c's in-sample offset" — a *value* offset, which the list does not
name. The permutation case passes every one of the five listed effects, and
the neighbouring planar-ordinal bar exempts interleaved layers in terms: "An
interleaved layer is unaffected, its disk ordinal being s, which no channel
declaration enters."

CONFIRMED. The general clause does bar it, via §14.1's "value k of the
sequence is channel (k mod C)'s value", and §20.3 says the list does not stand
on its own — which is why the reporter files it as an observation rather than
an ambiguity, correctly.

Byte-level: NO. Deciding text, [R-CNF-02]: "File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or environment."
The permuted file is itself conforming (it merely denotes a different
reference array), so no accept/reject verdict and no emittable byte sequence
moves; only whether a particular commit route was permitted.

Severity: editorial. Repair: "the byte offset of any value within the decoded
tile image".

---

## G24 — planar-pq-designation  (adversary-01)  ** the one self-flagged byte-level finding **

§14.2 verbatim, with the table header:

| Layout | Decoded size | Offset of value k |
| planar, numeric channel c | P · Bᶜ | k · Bᶜ |
| interleaved | P · Q | (k div C) · Q + F_{k mod C} |

"where Bᶜ is channel c's element size (§12.1; 1 for bool), Q = Σ Bᵢ over all
channels (the **sample stride**), and Fᶜ = Σ Bⱼ over channels j < c (channel
c's in-sample offset). These products and sums are declaration-derived
quantities under `[R-ENC-04]`."

The reporter's quotation is accurate and the arithmetic of the 256-byte file
checks out: rank 1, E = 1, T = 2⁵⁹ → G = 1, N = 1, P = 2⁵⁹; two float64
channels planar → C·N = 2, P·Bᶜ = 2⁶², N·P = 2⁵⁹, V = P = 2⁵⁹, index
extent_length = 2·20 + 4 = 44 ([R-CNT-17] satisfied), both entries sentinel.
Q = 16 and P·Q = 2⁶³, one above [R-ENC-03]'s 2⁶³ − 1. Geometry is legal:
[R-GEO-01] requires only d ≥ 1, Tᵢ ≥ 1, C ≥ 1, and [R-GEO-01] expressly allows
"A tile extent MAY exceed its dimension's extent". So if the designation
reaches a planar layer, the file is L2 and reject-layer; if not, it is
conforming. The fork would be byte-level if reading (a) were permitted.

I judge it is not, and I state the premise so it can be attacked.

**Premise of my downgrade:** designating a *tabulated* formula does not detach
it from the case-key of the table row that states it. "These products and
sums" designates each quantity for the layout whose row gives it; a planar
layer therefore has no quantity P·Q for [R-ENC-04] to bound, and forming one
means applying the row keyed "interleaved" to a layer that is not.

**Deciding text.** §14.2's own introduction to the table: "The image's byte
length — the **decoded size** — and each value's byte offset follow:" —
followed by a table whose first column is `Layout` and whose rows are keyed
"planar, numeric channel c" and "interleaved". P·Q is *the decoded size of an
interleaved tile*; §14.2's opening sentence scopes the section to "a planar
tile of a numeric channel (§12.1), and … every interleaved tile", and for the
planar case it gives P·Bᶜ.

**Corroboration — six independent places key P·Q to interleaved.**
- §21.3 L2: "P·Q (which dominates V = P·C)". Planar V is P, not P·C
  ([R-SER-01]: planar "the sequence has V = P values"; interleaved "V = P · C
  values"), so this instance is expressly the interleaved one.
- §21.3 L44: "in a planar layer the largest channel plane governs |
  interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉".
- §21.4 T3, T14, T21, T22: every instance cell reads "interleaved P·Q, …;
  planar numeric P·Bᶜ, …; packed planar bool ⌈P/8⌉, …".
- §19.3 describes [R-SER-02]'s contribution as "the decoded sizes §14 derives
  from it", which for a planar layer are P·Bᶜ and ⌈P/8⌉.
- §17.3: "The shuffle stride s is the channel's element size for a planar tile
  and the sample stride Q for an interleaved tile" — Q is used only where the
  tile is interleaved.
- §11.2 [R-GEO-03] shows the document's habit of layout-keying designations:
  "the number of its tile-index entries … is N for an interleaved layer and
  C · N for a planar layer."

**Verdict: PARTIAL, byte_level false.** The claimed verdict fork is not
permitted by the words read against their own table; a verifier that forms P·Q
for a planar layer and rejects would be rejecting a conforming file and would
itself fail [R-CNF-03]. But something *is* wrong there, and it is worth the
one-clause repair: [R-SER-02]'s designation sentence carries no layout
qualifier where its five register restatements and its sibling designation in
[R-GEO-03] all do, and [R-ENC-04]'s own warning — "an expression this
specification writes only inside a comparison, and names nowhere, is not a
designated quantity" — addresses the opposite failure mode and gives no help
here.

**If my premise is wrong, this is byte-level on a named 256-byte file.** That
is the honest shape of it, and I flag it in `notes` as the group where I would
most want a second opinion.

Severity: design-decision. Repair: "These products and sums are
declaration-derived quantities under `[R-ENC-04]`, each for the layout whose
row states it; a planar layer derives no P·Q and an interleaved layer no
P·Bᶜ."

---

## G25 — mta09-bound-above-antecedent  (quiz-01)

Verified: §18.2 states two reader-chosen bounds above the verifier sentence —
"a reader decodes with a bound of its own choosing, no smaller than §21.9's
user-metadata guarantee" and "a reader's window bound is its own, no smaller
than §21.9's guarantee for that quantity" — and the verifier sentence says
only "the bound above". Locally ambiguous, and the window bound is the nearer
antecedent. CONFIRMED.

The document does decide it elsewhere, and the reporter found the right text.
§21.5's introduction verbatim: "except where a reader or verifier declines the
decode on the size bound or on the frame's declared window, which
`[R-MTA-09]` makes that actor's capability and not a fact about the file" —
naming the verifier and the window in one clause. §2.3's cannot-establish list
is also unqualified: "when it declines to decode a user-metadata document
(`[R-MTA-09]`)".

Byte-level: NO. Deciding text is §21.5's clause just quoted: it settles the
question for a reader of the whole document, so no two competent
implementations are left free to differ; and under both readings the file is
conforming and the record is ignore-record, so no byte sequence changes
acceptance.

Severity: editorial. Repair: "on either bound above".

---

## G26 — rationale-last-zero-grid-count  (quiz-02)

Verified verbatim inside the §11.1 *Rationale* blockquote: "— the growth that
raises a zero-extent layer's **last** zero grid count included." The
document's own uses of "last" are ordinal-by-declaration: §11.4 "the
last-declared dimension varies fastest"; §16.2 "a run is a band along the
last-declared dimension"; §20.3 "removing the last" channel. Under that
reading the sentence is false — raising the last-declared dimension's grid
count while another stays 0 keeps N = 0 and entry_count = 0, which is the
*preceding* sentence's directory-only case. Only "last remaining" makes it
true. CONFIRMED.

Byte-level: NO. Deciding text, [R-CNF-01]: "All text in this document is
normative except: … any text labeled *Note*, *Example*, or *Rationale*"; and
the passage defers in terms — "§20.3 states normatively, and governs, what a
commit may do to a layer". L22 ("a nonzero slot with entry_count = 0") catches
an implementer who follows the wrong reading.

Severity: editorial. Repair: "a zero-extent layer's *only remaining* zero grid
count".

---

## G27 — barriers-conduct-classification  (quiz-03)

Verified: [R-LIF-02] steps 4 and 6 are MUSTs on a writer — "(4) make steps 1–3
durable (a storage barrier such as fdatasync…)"; "(6) make the trailer
durable" — restated in §20.5 as "The pad of step 5 and the barriers of steps 4
and 6 — both, not one — are owed here as they are of a creator." [R-CNF-02]'s
conduct enumeration names only "where a value is published, or which registry
version a writer targets (§10.3, §18.3)" plus the two expressly-declared cases
(§6.3's flags, §6.2's pre-trailer gap). The barriers are in neither, and §9.2
does not declare them conduct. §21.7's taxonomy does not obviously place them
either: they are unwitnessed on its definition and equally "no condition a
file can exhibit", and its worked case for the second class ([R-ENC-06]) turns
on a quite different argument. CONFIRMED as a real gap in the enumeration.

Byte-level: NO. Deciding text, [R-CNF-02]: "File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or environment."
Two byte-identical files, one written with barriers and one without, are the
same file to that predicate, so no byte sequence moves.

Severity: design-decision (it needs the maintainer to say which category the
barriers fall in). Repair: one clause in §9.2 declaring steps 4 and 6 conduct
rules, on the model [R-CNF-02] itself describes — "each is declared where it
arises rather than enumerated here".

---

## Coverage check

34 input ids. Union of member_ids, counted by hand:
G1 2, G2 1, G3 1, G4 1, G5 1, G6 1, G7 1, G8 2, G9 1, G10 3, G11 1, G12 1,
G13 3, G14 1, G15 2, G16 1, G17 1, G18 1, G19 1, G20 1, G21 1, G22 1, G23 1,
G24 1, G25 1, G26 1, G27 1.
Running total: 2,3,4,5,6,7,8,10,11,14,15,16,19,20,22,23,24,25,26,27,28,29,30,
31,32,33,34. = 34, no duplicates.

Byte-level count upheld: 0.
Reporters' byte-level flags: 1 (adversary-01), downgraded with quotation and a
stated premise.
