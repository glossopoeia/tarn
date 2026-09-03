# Triage pass — correctness lens — cleanroom round 30

## Disclosure

Read: `spec/tarn.md` §2, §4, §5, §6, §7, §9, §11, §12, §13, §14, §17, §18,
§19, §20, §21 (all subsections), §22, Appendix G (all via `sed -n` ranges;
one §20 read spilled to a persisted tool-result file which I re-read by
range from the spec instead). Grepped two walk transcripts by name —
`out/transcript-reader.md` and `out/transcript-adversary.md` — for the
reporters' reasoning on reader-01 and adversary-02 only. Did not list any
directory. Did not open any other triage pass's notes, `docs/`, `PLAN.md`,
`AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or the web.

Ids received (19): reader-01..04, writer-01..03, verifier-01..04,
diagrams-01, register-01..03, adversary-01..03, quiz-01. Each is placed in
exactly one group below; the union is counted at the end.

## Groups

### G1 planar-pq-designation — reader-01 — CONFIRMED, byte-level

Text checked, §14.2 [R-SER-02]:

> | planar, numeric channel c | P · Bᶜ | k · Bᶜ |
> | interleaved | P · Q | (k div C) · Q + F_{k mod C} |
> where Bᶜ is channel c's element size (§12.1; 1 for bool), Q = Σ Bᵢ over
> all channels (the **sample stride**), and Fᶜ = Σ Bⱼ over channels j < c
> (channel c's in-sample offset). These products and sums are
> declaration-derived quantities under `[R-ENC-04]`.

[R-ENC-04]: "A designation is express, made by the section that defines the
quantity; an expression this specification writes only inside a comparison,
and names nowhere, is not a designated quantity and no reader is obliged to
form it."

L2 Instances cell (untagged): "…; P·Q (which dominates V = P·C); P·Bᶜ; …"
against L44/T3/T14/T21/T22 which tag "interleaved P·Q; planar numeric
P·Bᶜ". §21.1: "Where the quantity a condition derives varies by layout, the
layout formulas are materially different shapes and the cell enumerates
them." §19.3: "the 2⁶³ − 1 ceiling on every quantity that arithmetic derives
(`[R-ENC-04]`) and on the decoded sizes §14 derives from it". [R-SER-07]:
"Every decoded size, and the value count V, is a declaration-derived
quantity". §17.2 Note: "so P·Q and P·Bᶜ are checked in an empty layer even
though this cap is not."

Judgement. The designation sentence "These products and sums are
declaration-derived quantities" is not layout-qualified, and Q is defined
"over all channels" for every layer. Reading (i) — every product written in
the table is designated for every layer — is what a literal reader of that
sentence takes, and it is exactly what L2's untagged cell restates (L2 lists
P·Q beside N, P, N·P and C·N, all of which *are* computed for every layer).
Reading (ii) — the designated quantity is the layer's own decoded size, so a
planar layer has no P·Q — is what §19.3's "the decoded sizes §14 derives",
[R-SER-07]'s "every decoded size", and §21.1's layout-shape convention
support. No sentence says which. I verified the reporter's construction:
rank 1, E = 0, T = 2⁵², C = 4096 uint8, planar: P = 2⁵², Bᶜ = 1, Q = 2¹²,
P·Bᶜ = 2⁵², V = P = 2⁵², N = 0, entry_count = 0, P·Q = 2⁶⁴. No §21.9 row is
exceeded (the tile row ranges over addressed tiles; there are none). Under
(ii) the file is conforming and within the guarantees, so [R-CNF-03]
obliges acceptance; under (i) L2 fires and the file is nonconforming. The
same fork reaches a non-empty layer through a sentinel entry (N = 1,
addressed but unstored): the emittable set moves. Byte-level: yes.

Repair: in §14.2 add "for the layout the layer declares" (or: "a layer's
designated products are those of its own layout's row"), and tag L2's cell
"interleaved P·Q (which dominates V = P·C); planar numeric P·Bᶜ" as L44
does. Either direction closes it; (ii) is the reading the rest of the text
already assumes.

### G2 cnf02-closed-list-vs-barriers — reader-02, writer-03, verifier-04 — REFUTED

All three say §9.2's barrier paragraph is a third member of [R-CNF-02]'s
closed list of two. Text checked, [R-CNF-02]:

> A few obligations this specification places on writers govern their
> *conduct* rather than their output — where a value is published, or which
> registry version a writer targets (§10.3, §18.3) — and a file is never
> nonconforming by virtue of one: conduct rules bind the actor, the
> predicate binds the bytes. A writer obligation whose violation this
> specification expressly declares not to be a file-conformance violation
> binds the actor in the same way; §6.3's flags = 0 … and §6.2's pre-trailer
> gap … are the cases this text states

Two categories: (1) conduct rules, open list by example; (2) *output*
obligations expressly declared not to make the file nonconforming, closed
at two. §9.2:

> Steps 4 and 6 bind a writer's **conduct** rather than its output, and are
> declared so here on the model `[R-CNF-02]` states

"bind a writer's conduct rather than its output" is category (1)'s defining
phrase verbatim ("govern their conduct rather than their output"). The
closing sentence "the file it produces is not nonconforming on that
account" restates category (1)'s consequence ("a file is never
nonconforming by virtue of one"); it does not move the barriers into
category (2), whose members are obligations *on the output bytes* (a flags
value, a gap length). writer-03's "the text does not say which" is not
right: the first clause says which. The closed count of two stands. No
bytes turn on it under any reading, as all three reporters concede.
Severity none.

### G3 retype-nonconforming-overstatement — reader-03 — CONFIRMED, editorial

§20.3 step 4: "Where a change does reach them it makes each stored tile it
reaches nonconforming, and re-emitting those tiles would strand the
originals as slack". §2.3: "File conformance is a pure predicate on bytes".
§21.7: a writer emitting well-formed structures with wrong content
"produces a file that every checksum in §8 certifies … the verdict is
unaffected". I checked the construction: int8 → uint8 by a directory-only
commit; element size and fill length unchanged; every byte a valid uint8
sample ([R-TYP-05]); with no padding positions no T4 witness; no row
applies. A creator can emit the identical bytes (uint8 layer, superseded
directory as slack, [R-CNT-21]). So the re-typed file is conforming, and
the sentence's "makes each stored tile it reaches nonconforming" is an
overstatement — true where §14 supplies a witness (uint8 → bool: T2 or T3;
a fill-length change: T4), unwitnessed otherwise. The bar itself
(MUST NOT) is clear. Not byte-level: no check separates the two files, the
emittable set is unchanged. Repair: "makes each stored tile it reaches
carry a violation wherever §14 gives one a witness, and wrong content §21.7
leaves unwitnessed otherwise".

### G4 l23-name-overrun-tier — reader-04, register-02 — CONFIRMED, register-bookkeeping

L23: "leading fixed fields (name … C); … | reader | layer access |
`[R-CNT-18]`". §19.1 step 4: "a layer record whose name field does not lie
entirely within that record's inline_length yields no name field to
compare, so it contributes no name to the namespace and is instead a
validity error at layer scope (`[R-CNT-18]`)". §19.2: "at open: … the
layer-name namespace (§19.1's steps)". The name-overrun instance is
therefore established at open by every conforming reader; L3/L5/L6 (the
other name rows) already say *open*. L23's cell states a later deadline
than the rule for one sub-instance. §21.1: the rule governs. Same outcome
(reject-layer), same bytes, and [R-RDR-02] licenses earlier detection, so
not byte-level. Repair: split the Detected cell as R1 does — "open (name);
layer access (the rest)".

### G5 key-order-prefix — writer-01 — PARTIAL, editorial, not byte-level

[R-MTA-05]: "in ascending order of their keys' UTF-8 bytes"; §18.2's
duplicate-key bullet: "sort order is likewise over decoded keys' UTF-8
bytes"; Appendix G item 3: "ascending layer-name byte order" and, for other
record types, "compared lexicographically". Premise of the downgrade,
stated for attack: an order "of their bytes" is the lexicographic order of
byte sequences (memcmp, a proper prefix first); a length-first (shortlex)
order is an order by *length* that consults bytes only secondarily, and no
sentence names length. The reporter agrees a competent implementer reads
lexicographic. F27/L48 fork only under the shortlex reading, which the
words do not offer. PARTIAL because the observation is real (the document
pins "low"/"last" at item 2 to a higher standard than this) but the fork
claimed is not one the text permits. Repair: "in ascending order of their
keys' UTF-8 bytes, compared lexicographically with a proper prefix first".

### G6 appendix-g-version-minor-gloss — writer-02, diagrams-01 — CONFIRMED, editorial

Item 8: "The version_minor floor binds a compactor too, save where its
output carries a feature it does not implement, when §20.5's floor governs
instead (`[R-WRT-06]`)." Closing paragraph: "`version_minor` at its floor,
which `[R-CNT-26]` states as a SHOULD — item 8's creator's rule, not a
compactor's (§20.5)". §20.5 [R-WRT-06]: "Otherwise version_minor follows
`[R-CNT-26]`'s floor." Item 8 and §20.5 agree; the closing gloss says the
opposite. Appendix G is non-normative ("adds no requirement to any actor"),
version_minor is descriptive ([R-ENC-16]), the floor is a SHOULD
([R-CNT-26]), readers never gate on it ([R-CNT-07]) — no emittable set or
verdict moves. Repair: rewrite the gloss: "item 8's rule for creator and
compactor alike, the flags half a creator's (§20.5)".

### G7 unassigned-encoding-two-senses — verifier-01 — PARTIAL, editorial

§21.5 fixes "unassigned" as {0, 3–0x7F, ≥ 0x80} and says "Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as
violations". §2.3: "A user-metadata document under an encoding this
specification does not assign is not such a ground: no content rule attaches
there, so nothing is left unchecked, and certification is unaffected".
§17.4: "an unassigned document encoding in a conforming file is not a
violation (§21.6)". Read with their qualifiers both are true in the broad
sense — §2.3's sentence is about the cannot-establish ground (encoding 0 is
not that ground either; it is R1's violation), and §17.4's "in a conforming
file" excludes encoding 0 and reserved values, since no conforming file
carries them. [R-MTA-10] itself is written in the broad sense and names
"the encoding byte's own value set (`[R-MTA-03]`)" among the checks that
still decide conformance. So the verdict does not fork — the reporter says
as much — but the word carries two senses and a reader of §2.3 or §17.4
alone can miss that R1 still bars certification. PARTIAL: the sentences
are not false, they are under-qualified. Repair: append "(encoding 0 and a
reserved value remain R1's violations, §21.5)" at §2.3 and §17.4.

### G8 err04-document-scope-note — verifier-02, register-01 — CONFIRMED, editorial

[R-ERR-04]: "a reader MAY decline it — at the whole file, or at the
narrowest scope whose stated or derived quantities exceed what it can
serve: a layer, a tile, or the record carrying a user-metadata document, as
§18.2 assigns." §18.2 body (window bound): "a frame declaring more than the
reader admits is ignore-record on that ground — … the file exceeds a §21.9
guarantee and so remains conforming while the reader MAY decline it
(`[R-ERR-04]`)." §18.2 Note: "a reader that instead declines on resource
grounds under `[R-ERR-04]` does so at the whole file, a document having no
declared size and so no narrower scope whose stated or derived quantities
that rule can measure, its decoded size being neither." The Note denies the
record scope that the rule expressly names ("as §18.2 assigns") and that the
same section's body uses; §21.9's table row is stated over "decoded size of
one user-metadata document", so the decoded size is a quantity the rule
does measure. Non-normative Note, [R-CNF-01]: the rule governs. Behaviour
does not fork (ignore the record, or refuse the file; file conforming);
what differs is whether the record-level response carries [R-ERR-04]'s
resource-limit label or [R-CNT-25]'s SHOULD-report. Repair: rewrite the
Note: "a reader that declines under [R-ERR-04] does so at the record —
ignore-record, reported as a resource limit — or at the whole file".

### G9 partial-total-file-scope-rejection — verifier-03 — CONFIRMED, design-decision

[R-CNT-21]: the total is owed once a live trailer is established; the
discard clause is stated for layers only ("a rejected layer's claimants are
not enumerated … the claimants it had already enumerated are discarded with
the layer"); the definition is "F less the bytes claimed by the claimants
the walk did enumerate". For a reject-file the walk itself establishes (F33
cross-layer overlap, F7 structure in the gap) or a post-trailer reject-file
(F20, F29, F34) the text states no composition: literal (b) keeps every
enumerated claimant; the stated rationale ("a claim about a live state …
not usable") extends to (a) discard all but front block and trailer. Both
are upper bounds and both satisfy "naming what stopped the walk", so two
conforming verifiers report different MUST-level figures for one file. Not
byte-level: the file is nonconforming under both, no emitted byte or
verdict moves; the figure is diagnostic. The maintainer decides whether the
discard extends to a walk-established file-scope rejection (the natural
extension of the stated rationale) or the literal definition holds; either
is one sentence.

### G10 partial-total-discard-clause-cost — quiz-01 — REFUTED, none

Same clause as G9, different claim: that the layer-scope discard sub-rule
is easy to misapply. The reporter resolved it correctly from the text and
files it as decidable. The text does decide it (quoted in G9). No defect;
if G9's repair restructures the clause into stated cases, this reading cost
falls with it.

### G11 ser08-antecedent-detecting-reader — adversary-01 — CONFIRMED, editorial

[R-SER-08]: "A reader is not obligated to screen decoded content, and a
reader that does not detect the violation is not thereby nonconforming;
`[R-CNF-12]` governs a reader that does detect it. A reader that neither
detects the violation nor rejects the tile, and returns the value, MUST
report 0x00 as false and every other byte as true." [R-CNF-12] gives a
detecting reader only a MAY to reject and fixes no return. A reader that
detects, elects not to reject (permitted: T2's detector is the verifier, so
[R-CNF-09] does not oblige refusal), and serves is outside the literal
antecedent "neither detects … nor rejects". §19.4 step 8 and [R-TYP-04]
read the rule universally ("`[R-SER-08]` fixes what a reader returns for
the one byte a conforming file cannot"), so the intent is plain and the
antecedent is the defect. Not byte-level: the file is nonconforming under
both readings, the emittable set and every verdict are unchanged; only the
value a detecting-and-serving reader returns is left to the rule's evident
purpose. Repair: "A reader that returns the value — whether or not it
detected the violation — MUST report 0x00 as false and every other byte as
true."

### G12 pe0-drop-on-record-add — adversary-02 — PARTIAL, editorial, not byte-level

§20.4 MU = 0 / PE = 0 cell: "An appender MUST NOT drop it except in a
commit that *independently* changes the scope the record attaches to: …
for a top-level record, the file's layer set, any layer record's content,
or another *non-layer* top-level record. A commit changes the layer set by
adding a layer; an appender never removes one … Dropping the record, or
dropping another record in the same commit, is not itself such a change".
Premise of the downgrade, stated for attack: the objects of "changes" are
"the file's layer set", "any layer record's content", "another non-layer
top-level record"; a record that did not exist before the commit is not one
the commit *changed*, and the drafters used set-language ("layer set",
"the entry set of its index", "which of its tiles are stored") exactly
where membership changes count, adding the express sentence "A commit
changes the layer set by adding a layer" for the one case where a set is
the object. Adding record M therefore changes no existing record and not
the layer set, and the drop is not licensed: reading (i), the reporter's
own pick. Reading (ii) requires "changes another record" to mean "changes
the set of other records", which the words do not say. Under the letter a
conforming appender may not emit the drop, so the emittable set does not
fork; the reporter's fork exists only if (ii) is admitted, and I do not
admit it. PARTIAL because the asymmetry the reporter points at is real —
adding a layer is addressed, dropping another record is addressed, adding a
record is not — and one clause closes it. Repair: append "Adding a
non-layer top-level record is not such a change." If the maintainer instead
wants adding to license the drop, that is a design change to the letter,
not a reading of it.

### G13 cod11-ground-unreachable — adversary-03 — REFUTED, none

[R-COD-11]: "A verifier that cannot execute a layer's codec or filter
cannot establish that layer's conformance and MUST NOT certify the file.
That inability is not a finding that the file is nonconforming, and it
fixes the file's verdict as *cannot establish* only where the verifier
established no violation elsewhere (`[R-CNF-11]`). For a conforming reader
that position arises only at a reserved or experimental value, every
assigned codec and filter being core: it rejects the layer". The rule's own
third sentence states what the reporter derives: a conforming verifier
meets the inability only at an L43/L45 value, which it establishes as a
violation, and [R-CNF-11]'s priority clause then fixes *nonconforming*. The
reporter concedes decidability. That §2.3 lists a ground reachable only by
software that is not a conforming reader is a redundancy, not a defect; no
verdict forks. Severity none.

### G14 sec216-cross-ref-underdelivers — register-03 — CONFIRMED, editorial

§21.5: "except where a reader or verifier declines the decode on the size
bound or on the frame's declared window, which `[R-MTA-09]` makes that
actor's capability and not a fact about the file. … §21.6 lists the
ignore-record conditions that are not violations." §18.2 makes both
declines "ignore-record … and no violation". I checked §21.6's table: its
ignore-record non-violations are the experimental record type with MU = 0
and the experimental document encoding; no row covers a §21.9
guarantee-excess decline at any scope. §21.1 exempts §21.6 from the
completeness clause, so this is a cross-reference that under-delivers, not a
register gap; behaviour is fully stated in §18.2 and [R-ERR-04]. Repair:
either "§21.6 lists the ignore-record conditions that are not violations,
and §21.9 the declines a guarantee excess licenses", or add a §21.6 row for
"a quantity exceeds a §21.9 minimum guarantee".

## Coverage count

G1: reader-01 (1). G2: reader-02, writer-03, verifier-04 (3). G3: reader-03
(1). G4: reader-04, register-02 (2). G5: writer-01 (1). G6: writer-02,
diagrams-01 (2). G7: verifier-01 (1). G8: verifier-02, register-01 (2). G9:
verifier-03 (1). G10: quiz-01 (1). G11: adversary-01 (1). G12: adversary-02
(1). G13: adversary-03 (1). G14: register-03 (1).
1+3+1+2+1+2+1+2+1+1+1+1+1+1 = 19. Byte-level groups: 1 (G1).
