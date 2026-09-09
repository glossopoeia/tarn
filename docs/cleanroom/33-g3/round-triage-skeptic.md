# Round 33 — triage pass, Skeptic lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — the whole
  document, in chunks: lines 1–450, 450–900, 900–1350, 1350–1750, 2168–2428,
  2605–2885, 2883–3143, 3143–3403, 3403–3613, 3612–3902, 3901–4201, 4290–4376
  (§24), 4537–4577 (Appendix F), 4620–4720 (Appendix G), 4719–4806 (Appendix H).
  Plus targeted greps (below). Sections 12–14 and 17.1–17.4 I read only through
  greps and the register rows, because no finding turned on them.
- No walk transcript. No other triage pass's notes. No `docs/`, `PLAN.md`,
  `AGENTS.md`, `conformance/`, `registry.json`, git history, or web.
- I did **not** list any directory. I opened only the spec file by name.

## Greps run (all against spec/tarn.md)

```
grep -n "^#\{2,4\} "                                  # section index
grep -c "RFC 8878|1951|8259|8174|3720|3339|2119|1952|1950"
grep -n "declared, re-established or cleared|re-established or cleared|re-establish"
grep -n "alignment"
grep -c "counted and named"          -> 1
grep -c "report each record"         -> 1
awk NR 3700..3871 | grep governing-rule cells containing "§"   -> exactly 2 (L26, L31)
awk NR 3603..3700 | list [R-...] cited                          -> all citations, none defined
```

---

## Grouping

25 ids into 22 groups.

Merges made, with reasons:

- **verifier-01 + quiz-02** — identical defect, identical three passages, identical
  qualifier. Trivial merge.
- **writer-02 + adversary-03** — both centrally about §20.3 step 4's writer
  prohibition having no reader-side clause and no stated category. The decisive
  signal that they are one defect: they reach *opposite* answers to the same
  question. writer-02 concludes the resulting file is conforming; adversary-03
  concludes it is "nonconforming-but-invisible". Two careful readers of the same
  sentences disagreeing is what "the document does not settle it" looks like.
  adversary-03 carries a second limb (the SHOULD claim against [R-MTA-09]) which I
  fold into the same group's repair rather than splitting an id.
- **diagrams-04 + register-04** — both are "a register Governing-rule cell departs
  from the convention §21.1 states for that column". diagrams-04 raises L26/L31 and
  *also* raises the R6/R10 asymmetry by name; register-04 is that R10 asymmetry
  alone. One defect class, one repair pass over the column.

Merges I considered and rejected:

- **writer-01 / quiz-01 / adversary-04** — all three are §20.3 step 4 closed-list
  scope questions, but each disputes a different clause and a different operation
  (a declaration's value change; how many trailing planar channels may go in one
  commit; whether a rename of the last channel is a "replacement"). Different
  repairs. Kept apart.
- **reader-01 / register-06** — both cite F5. reader-01 is about §19.1's step
  ordering; register-06 is about F5's second Instance. Different defects.

---

## Judgements, with the text I checked

### G1 open-path-128-byte-floor (reader-01) — CONFIRMED, editorial, not byte-level

§19.1 step 1 reads "Obtain the transport-authoritative file size F"; step 2 "Fetch
bytes [F − 64, F)". No floor check. The arithmetic underflows for F < 64. True.

Deciding sentence (§19 preamble, lines 2886–2888):

> "A row this section does not restate is due at its own tier all the same, with
> its governing rule's own outcome."

So the obligation is settled: F5 is due at open whether or not §19.1 restates it.
Both readings reject the file ([R-CNT-27] is unambiguous, and every §6.2 gate fails
anyway). Not byte-level. Editorial: adding "and reject a file shorter than 128
bytes ([R-CNT-27])" to step 1 costs one clause and removes an underflowed
expression from the reader's normative path.

### G2 conduct-rule-classification-of-barriers (reader-02) — CONFIRMED, editorial

§2.3's second-category sentence is a closed list ("are the cases this text states")
whose class is "A writer obligation whose violation this specification expressly
declares not to be a file-conformance violation". §9.2 makes exactly that express
declaration about steps 4 and 6, and the barriers are not on the list. Literally,
the sentence is one member short.

Deciding sentence (§9.2, lines 1280–1287) — this is why nothing turns on it:

> "Steps 4 and 6 bind a writer's **conduct** rather than its output, and are
> declared so here on the model `[R-CNF-02]` states … as `[R-CNF-02]` says of every
> conduct rule."

§9.2 routes itself to §2.3's *first* category, whose examples are open-ended ("A
few obligations this specification places on writers govern their *conduct* rather
than their output — where a value is published, or which registry version a writer
targets (§10.3, §18.3) —"), not to the closed list. So the classification is
decided by the section that states the rule. Not byte-level: a barrier leaves no
trace in the bytes, by §9.2's own words. Editorial repair: name §9.2 alongside
§6.3 and §6.2 in the closed list, or narrow the class to exclude conduct rules.

### G3 metadata-encoding-valid-values-cell (reader-03) — PARTIAL, editorial

I set out to confirm this and found the reporter's comparison set is wrong. The
claim is that "every comparable cell elsewhere spells that out — §6.2's flags row …
§7.4's index_encoding row … §15.1". §15.1's own layout table (line 2186–2187):

> `| 0 | 8 | u64 | offset | structural | see §15.3 |`
> `| 8 | 8 | u64 | length | structural | see §15.3 |`

That is a pure pointer, no value set at all — the same device §18.2 uses. So
deferral-by-pointer *is* the document's practice in one of the three cells the
reporter cites as contrary practice. And §18.2's cell carries "see below", with the
next sentence partitioning the space correctly:

> "Field values: 0 is invalid; 1 = none and 2 = zstd are assigned; 3 through 0x7F
> are reserved; values ≥ 0x80 are the experimental range (§10)."

Not byte-level: [R-EXT-03], [R-MTA-10] and §21.6's row all decide the outcome, and
a verifier reading the cell as a value set would be wrong under the document rather
than licensed by it. The residual asymmetry against §7.4's index_encoding row is
real but small. PARTIAL.

### G4 declaration-value-change-under-the-closed-list (writer-01) — CONFIRMED, **BYTE-LEVEL**

**This is the group I tried hardest to kill and could not.**

The closed list (§20.3 step 4, lines 3197–3203) permits "a slab or alignment
declaration MAY be declared, re-established or cleared as this step provides
below", and closes with "with these exceptions and no other". Whether "declared"
covers writing a *different* nonzero value onto an existing declaration decides
whether a commit may lower A from 4096 to 512 in place.

Sentences I hunted for and did not find:

1. **A definition of the three verbs.** Whitespace-normalised sweep for the phrase:
   lines 1656 (§11.1 Rationale), 2361 ([R-SLB-04], two-verb remedy), 3203 (the
   list), 3299 (the below-clause's two-verb form), 4766 (Appendix H). Five sites,
   the same three or two words, no definition anywhere.
2. **A "fixed" clause reaching A/S/A_slab.** The fixed side (line 3209) enumerates
   "the layout, the linearization and the index encoding, the codec and the filter,
   the rank and the dimension order, every tile extent, every channel's type and
   fill, an interleaved layer's channel list (its names aside), and the position of
   every planar channel but the last." A, S and A_slab are absent, and the step
   then says "Between them the two lists reach every declaration field of §7.4" —
   so A/S/A_slab are reached by the *permitted* side alone, and the "A commit MUST
   NOT change one of these" attaches to the fixed enumeration, which does not
   include them.
3. **A mention in the "gives up" list.** Line 3260–3269 enumerates what is a
   rewrite, offered as stated rather than carved around: "a shrink, a fill change,
   a re-type, a re-tiling, a change to the dimension order, a change of rank,
   layout, linearization, index encoding, codec or filter, any change to an
   interleaved layer's channel list but a channel's name, a planar channel inserted
   or removed anywhere but the end of the list, and a planar channel list both
   extended and shortened in one commit". Neither a change of alignment nor of slab
   is there.
4. **Anything in §16.** [R-SLB-04] lists "or the slab declaration itself" among its
   five triggers. Read strictly, that phrase is satisfiable by a declare or a clear
   (the qualifier "of a layer slab-declared in either the superseded or the new
   generation" admits both), so it does not *prove* value changes are contemplated
   — but it is the only text in the document that even points at the question, and
   it points toward permitting them.
5. **Appendix G item 5** ("No declared alignment and no slab, or fixed declared
   values") — non-normative, and about reproducibility, not permission.

Against the reporter: (R-b) has one textual foothold — the below-clause at line
3299 offers only two dispositions ("a slab declaration is re-established or
cleared"), dropping "declared", which suggests the verbs are meant to partition
transitions. That is real but it is an inference from an omission, and the same
below-clause's *alignment* half ("an aligned layer's stored tiles — every one the
new state keeps, not only those this commit adds — satisfy its invariant or the
declaration is cleared") is written precisely for the case where the new
generation's invariant must be tested against tiles the commit did not place —
which is the changed-value case.

Against the document deciding it elsewhere: §7.4's own field semantics are
state-predicates, not transitions — "0 = none declared; else a power of two,
512 ≤ A ≤ 2⁶²" — and §16.1 "When declared: every stored tile's offset satisfies
offset mod A = 0". Under the document's own usage of *declared*, a generation
carrying A = 512 has declared an alignment of 512, whatever the prior generation
carried. That supports (R-a). It does not *foreclose* (R-b), because (R-b) attacks
the transition, not the resulting state.

**Byte-level, and the premise my uphold rests on.** The disputed file — commit n+1
carrying L's record with alignment 512, same file_id, F raised — is a *conforming
file* under both readings: [R-SLB-01]'s invariant holds over every stored tile the
new state keeps (every multiple of 4096 is a multiple of 512), [R-CNT-16] is
satisfied (S = 0), [R-CNT-23]'s range is satisfied, and nothing in the live state
witnesses what the superseded generation declared (§9.6: "no verdict turns on the
probe"; §5.2: slack "has no internal structure this specification defines"). So
this is **not** byte-level on the file-conformance predicate.

It is byte-level on the test as the brief states it — "which byte sequences a
conforming implementation *may emit*". Under (R-a) a conforming updater may emit
that file; under (R-b) it may not, and no other conforming writer can produce those
exact bytes (a creator emits one generation; the two-commit route produces three
generations and different bytes). **My premise, stated so it can be attacked: that
"a conforming implementation" in the byte-level test includes a conforming updater
bound by §20.3, not only the file-conformance predicate.** If the maintainer reads
the test as ranging over the conformance predicate alone, this group drops to
design-decision. I do not think that reading is available — §2.3 defines a
conforming updater as a conformance class, and [R-CNF-06] binds it — but it is the
one hinge, and it is the hinge round 16's passes would have wanted named.

Novelty caveat: the reporter says this is "the same shape as the composition defect
established here last round, one level down". I cannot check the ledger (docs/ is
out of bounds), so I cannot say whether this is new. It is real on this text.

### G5 step-4-prohibition-uncategorised (writer-02 + adversary-03) — CONFIRMED, editorial

Verified facts:
- §2.1's Note (lines 109–115) claims "every writer-side prohibition is paired with
  an explicit reader-side clause" and "every SHOULD states the consequence of
  deviation".
- §20.3 step 4's "A commit MUST NOT change one of these" carries no reader-side
  clause, no §21 row, and no statement of the file's status.
- [R-MTA-09]'s "the verifier SHOULD report the bound it applied and the stored
  length of the extent it declined" (line 2709–2710) states no consequence.

Both limbs are factually right. The Note is labelled *Note* and so non-normative
under [R-CNF-01], which caps the severity.

On the substantive disagreement between the two reporters (conforming vs
nonconforming-but-invisible), the text does lean one way, and the sentence is
§5.2's:

> "Slack has no internal structure this specification defines, its content is
> unconstrained, and no conformance requirement applies to it."

The superseded directory is slack. A fact recoverable only from slack cannot be a
file-conformance violation, so writer-02's reading (the file is conforming) is the
better one. But §2.3 [R-CNF-02] says such an obligation must be "declared where it
arises", and §20.3 step 4 does not declare it — which is exactly the gap. Not
byte-level: the actor is barred under every reading and no reader or verifier can
reach the question. Repair: one declaring sentence at step 4 on [R-CNF-02]'s model;
soften §2.1's Note's two absolute claims or supply [R-MTA-09]'s missing consequence.

### G6 slack-qualifier-dropped-twice (verifier-01 + quiz-02) — CONFIRMED, editorial

The three passages are as quoted. §15.3 carries "that no other claimant claims";
§5.2 and §9.7 do not. Both restatements are in normative bodies, so [R-CNF-01]
does not excuse them, and §21.1's "the rule governs" does not reach them (none is a
register row).

Deciding sentences — the definitions in the very passages that drop the qualifier:

> §5.2: "Every byte the live state does not claim is **slack**"
> §9.7: "Bytes the walk does not reach are slack"

Both are set-complements. Under them a byte claimed by the front block or by
another stored tile is not slack, however some malformed entry nominally addresses
it. [R-CNT-02]'s "No two of them overlap" makes the unqualified reading internally
impossible: it would make the front block simultaneously claimed and slack. So the
document decides it, and the defect is that the consequence clause is stated twice
without the qualifier while the definition that governs it is stated once each
time in the same paragraph. Not byte-level — the slack total is a report line, no
verdict turns on it, and every file where the divergence arises exhibits T6/T7/T8
and is nonconforming either way. Repair: insert "that no other claimant claims" at
§5.2 and §9.7.

### G7 unassigned-type-extent-not-named (verifier-02) — CONFIRMED, design-decision

Verified: "counted and named" occurs once, "report each record" once, both inside
[R-MTA-10]. §8.1's map row for an unassigned type's extent reads "none — the bytes
are opaque (§7.2)". §22.3 states that case first and calls it "equally invisible",
then supplies the operator remedy for the *other* case only. §21.6's
experimental-MU=0 row states "Ignored, and preserved or dropped per its PE bit" and
no report duty. Appendix H's verifier list names the [R-MTA-10] report and no
counterpart. §2.3's report duties run to requirements the verifier was unable to
check and scopes it did not examine; neither reaches an unassigned type's extent.

I looked for a naming duty and found none. That absence is the finding. Not
byte-level: a report obligation, verdicts identical either way. I grade this
design-decision rather than editorial because extending [R-MTA-10]'s duty to a
second class is a new obligation on a verifier, not a wording fix — the maintainer
has to decide whether to impose it.

### G8 residency-exemption-example (verifier-03) — PARTIAL, editorial

The clause does address verifiers (§2.3: "Verifiers and updaters are readers of the
files they process and inherit every reader obligation"). But it grants nothing —
its words are "an exemption the condition's governing requirement grants on a
ground other than the declared major **applies unchanged**", which preserves
whatever exemption the actor has and creates none. Three passages then settle it:

> §2.3: "**Conforming verifier.** A reader that additionally checks every
> file-level requirement — including those ordinary readers are exempted from"
> §21.2 F6: "a verifier holds no such exemption (§2.3)"
> Appendix H: "which `[R-CNT-04]` lets a reader not holding it resident defer or
> omit and §2.3 does not (F1, F6)"

So the document decides it three times and the clause's own verb does not grant.
The reporter's observation — that the one illustrative exemption chosen is one the
adjacent actor lacks — is fair as a pedagogical note, which is why PARTIAL rather
than REFUTED. Not byte-level.

### G9 note-misdescribes-7.4-columns (diagrams-01) — CONFIRMED, editorial

Verified column sets: §6.2, §15.1, §18.2 carry all six (Offset|Size|Type|Field|
Class|Valid values); §6.1 four (Offset|Size|Value|Class); §7.2 five
(Offset|Size|Type|Field|Class); §7.4 three (Field|Type|Constraint). The Note
accounts for §6.1 and §7.2 exactly and says §7.4 "omits the offset and class
columns" — three are absent, not two. Size is unaccounted for, and "size column"
returns 0 across the document.

The one candidate escape is the Note's own opening — "each table giving the columns
its structure needs" — but that clause is inside the sentence about *fixed-layout*
structures, and the Note then treats §7.4 separately and specifically. So it does
not cover the gap. Non-normative ([R-CNF-01]); §7.4's Type column gives every fixed
field's width, so nothing turns on it. Not byte-level. Repair: "omits the offset,
size and class columns", and reconcile the sixth column's three names.

### G10 compaction-example-slack-inventory (diagrams-02) — CONFIRMED, editorial

The closing sentence of §20.5's Example names a per-commit fixed term and a
per-layer index term and stops. §20.3's own Example says "The prior index region and
the superseded payload become slack", and §20.3 step 4 says normatively "Extents
this commit supersedes become slack (`[R-CNT-21]`)". On §20.3's own worked figure
the omitted term is 100,000 of ~100,800 bytes. Non-normative, and [R-CNT-21] plus
§9.7 govern the actual total. Not byte-level. Repair: add "the extents it
supersedes" to the inventory, or an "at least".

### G11 appendix-f-missing-rfcs (diagrams-03) — CONFIRMED, editorial

Verified: Appendix F alone among A–H carries no "(non-normative)" marker. RFC counts
across the document: 8878×7, 1951×5, 8259×3, 8174×2, 3720×2, 3339×2, 2119×2,
1952×2, 1950×2. Every one is in Appendix F except 1950 and 1952.

I looked for a scoping sentence in Appendix F that would exclude them and found the
opposite — the appendix's own practice defeats the "only what you need to produce
output" defence:

> "Informative: the OCP OFP8 specification, cited only to pin what sample-type
> identifiers 14 and 15 would mean if ever assigned (§12.2)."

That is exactly the status of RFC 1950 and 1952 in [R-COD-05] — cited only to pin
what codec 2 excludes — and it *is* listed. Not byte-level: [R-COD-05]/[R-COD-08]
reject a wrapper on the RFC 1951 test alone. Repair: add both, informative on the
OFP8 model.

### G12 governing-rule-cell-convention (diagrams-04 + register-04) — CONFIRMED, register-bookkeeping

Verified mechanically: scanning every Governing-rule cell in §21.2–§21.5 for a "§",
exactly two hit — L26 `[R-CNT-18]` (§7.3 registry table) and L31 `[R-CNT-23]`
(§15.1). §21.1 says the parenthetical holds "identifiers … cited without brackets
to keep them distinct from the governing one"; a § citation is not an identifier and
was never at risk of being read as the governing rule. And the R-row asymmetry is
as register-04 states: R6/R7/R8/R9 all carry (R-CNT-25); R10 alone does not, though
R6 is the other half of the same folding of §4.6's name rules onto keys.

§21.1's tiebreak ("where a row and the rule it cites diverge, the rule governs")
handles content divergence, not the column's grammar, so it does not foreclose
this. Not byte-level: no outcome, detector or detection point moves. Repair: put
the two § citations in the Condition cell or spell them as identifiers, and add
(R-CNT-25) to R10.

### G13 declines-to-judge-reason (register-01) — CONFIRMED, editorial

Verified: the paragraph says of case 2 "`[R-CNF-02]` makes the file conforming all
the same", then closes "Neither is a register row: the register enumerates
file-conformance violations (§21.1), and a file this document declines to judge is
not one." The relative clause is offered of both and is false of the second.

Mitigation the reporter does not credit: two sentences earlier the paragraph gives
the general ground that does cover both — "In both the outcome records a reader's
capability, not a defect in the bytes" — so the correct reason is present, and the
closing clause is a case-1 gloss over-reaching. Not byte-level. Repair: "and
neither a file this document declines to judge nor a conforming file is one."

### G14 quarantine-reach-over-R4 (register-02) — PARTIAL, editorial

I went looking to kill this and found the deciding text in §18.2 itself. [R-CNT-25]'s
fourth limb is "content violating **the document's own rules**". §18.2 defines that
phrase:

> "The document rules of this section — the frame constraints of encoding 2, the
> decoded-document restrictions above, and `[R-MTA-05]`'s member ordering — attach
> to a document only under an encoding this specification assigns."

So the frame constraints R4 registers *are* "the document's own rules" in this
document's own usage, and [R-CNT-25] reaches them. §21.5's preamble asserts the same
in terms ("every way its document can be unreadable takes this outcome … as a
violation in the rows below"), and the document uses "unreadable" broadly enough to
cover a document that parses (R9's duplicate keys decode fine and are called
unreadable). [R-MTA-09] expressly assigns ignore-record for R4 in any case ("Any
violation here is ignore-record").

Residual looseness the reporter is right about: §18.2 does say of the content-size
case "the bytes decode, and what is wrong is what the header said about them", which
sits awkwardly against a predicate keyed to unreadability. PARTIAL. Not byte-level.

### G15 overlap-row-instance-individuation (register-03) — CONFIRMED, register-bookkeeping

F33 names 5 claimant kinds, L18 names 3, and both conditions are symmetric
two-claimant relations. §21.1's individuation rules — "An instance names a field the
condition ranges over, a container it can occur in, one of several alternatives the
condition text states, or any combination of the three" and "One instance is one
*distinguishable* file" — do not say which side of the relation an instance names.
Two files exercising (tile ∩ index) and (tile ∩ sub-record) *are* distinguishable,
so the "distinguishable file" rule, applied to pairs, would demand more instances
than either cell holds. [R-VEC-03] then obliges "at least one vector for each
instance it names", which leaves the pairing to the builder.

I found no sentence fixing the pairing. [R-VEC-01]'s derivative-corpus clause and
[R-VEC-02]'s "the entry records every row the file exercises and says which it was
built for" bound the damage but do not decide it. Not byte-level: [R-CNT-13] fixes
reject-file for cross-scope overlap and reject-layer for intra-layer overlap
whichever pair a vector uses. Repair: state in §21.1 how an instance of a symmetric
relation is individuated, or restate F33/L18's cells as pairs.

### G16 §21.1-rules-unidentified (register-05) — CONFIRMED, register-bookkeeping

Verified: every `[R-...]` appearing in §21.1 and §21.2's header is a citation; none
is defined there. §21.1's rule-governs tiebreak, its normative completeness clause,
its specialization rule and its whole Instances arithmetic carry no identifier,
against §2.2's "Normative requirements carry identifiers of the form
`[R-<PREFIX>-<NN>]`". [R-ERR-02] does not supply one: it is defined in §21.8 and its
text is entirely about vector coverage.

Against the finding, and the reporter says it themselves: §2.2's own sentence
carries no identifier either, so the convention is not applied to every normative
sentence. But §21.1's rules are decision procedures other sections defer to, and
§24's [R-VEC-02] requires a vector to record "that row's governing requirement
identifier" while the rule deciding *which* row a vector is built for has none. Not
byte-level: [R-CNF-04] and [R-CNF-07] bind the register regardless. Repair is a
maintainer decision — assign ERR identifiers to §21.1's rules, or state that §21
headers are deliberately unnumbered.

### G17 F5-second-instance (register-06) — PARTIAL, register-bookkeeping

[R-CNT-27] is stated over physical length alone ("No conforming file is shorter than
128 bytes … A reader MUST treat a shorter file as a validity error at file scope"),
and a 192-byte file declaring committed_file_length = 64 is not a shorter file. So
the literal point stands.

But §21.1 licenses exactly this cell shape: "any identifiers following it in
parentheses are the further rules the condition reads", and F5's cell reads
(R-CNT-01, R-CNT-06). [R-CNT-01] supplies the bridge in terms:

> "The file size of a conforming file equals the live trailer's committed file
> length F"

The condition ("File size is below the 128-byte minimum") reads that to make the
declared length the file size. So the cell is constructed the way §21.1 says cells
are constructed. What remains is the reporter's own concession: a corpus vector for
the second instance necessarily also exercises F17 or F13, which [R-VEC-02] already
provides for. PARTIAL. Not byte-level — every such file is reject-file at open
under one row or another.

### G18 structure-in-the-pre-trailer-gap (adversary-01) — PARTIAL, editorial

The reporter's reading (B) — that §5.1's "structures the file's commits appended …
and each prior generation's trailer" is the operative sense of "structure" for
[R-CNT-05]/F7 — dies on a sentence directly above it in §5.2:

> "Every byte the live state does not claim is **slack**: alignment and slab gaps,
> the pre-trailer pad, and **everything an earlier commit superseded**."

A superseded tile-index region in the pre-trailer gap is expressly slack, by name.
[R-CNT-02]'s express definition of "structure" as a live-state partition class,
F7's Instances cell (live-state claimant kinds only, no superseded trailer or
directory among them), and [R-CNT-05]'s own "Those bytes — the **pre-trailer pad** —
are slack (§5.2)" all point the same way. §9.6 closes the implementability gap: "no
verdict turns on the probe".

So the constructed 448-byte file is conforming and the verdict does not fork. What
survives is a real editorial looseness: §5.1 uses "structure" for superseded
regions that §5.2 defines the word to exclude. PARTIAL, editorial. Not byte-level.

### G19 experimental-encoding-exception-vs-R2 (adversary-02) — REFUTED, editorial

This was the nearest miss in the input and it is dead. The §21.5 preamble's
exception is limited by its own relative clause — "except at an experimental-range
encoding, **where no document rule attaches**" — and R2 is not a document rule; it is
the extent's terminal CRC, a structural check. [R-MTA-10] then states the surviving
checks as a closed three-item list with the CRC inside it:

> "file conformance … is decided by the structural checks that precede the document
> alone: the record's framing and extent slot (`[R-CNT-13]`), the encoding byte's own
> value set (`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)."

Corroborated by §22.3 ("covered by its terminal CRC but constrained by no content
rule"), by §8.1's map (the User-metadata extent row carries no encoding qualifier),
and by R2's own row (no encoding qualifier). §21.1 seals it for the row and for the
§21.6 entry alike: "where a row and the rule it cites diverge, the rule governs …
where such an entry and the rule it cites diverge, the rule governs there too."

Not byte-level. Optional editorial: name R2 as surviving beside R1 in the preamble,
so the near-miss does not have to be resolved by three cross-references.

### G20 replacing-the-last-channel-gloss (adversary-04) — REFUTED, editorial

The gloss's antecedent is "an extension and a shortening of one channel list", and
the "so" ties it to that composition. A rename is neither, and the closed list's
first member permits it without qualification — "its name, and its dimension and
channel names, MAY change" — with the justification paragraph adding "a name enters
no map this specification defines, and a commit MAY change several names at once,
two swapped included". Appendix H repeats the unqualified rename permission. The
document decides it. Not byte-level. Optional editorial: phrase the gloss over the
operation rather than the result.

### G21 planar-suffix-removal-in-one-commit (quiz-01) — REFUTED, editorial

Deciding sentence, in the same step:

> "Between them the two lists reach every declaration field of §7.4, and where a
> field is on both sides — a dimension extent, a planar layer's channel list, an
> interleaved layer's channel list — the permitted side states the whole of what a
> commit MAY do to it"

The planar channel list is named expressly, and the permitted side says "extended at
its end or shortened from its end" with no count. The "gives up" list corroborates
with "anywhere but **the end** of the list", not "the last position". Reading 2 is
foreclosed. Not byte-level — the reporter's §9.3 argument is right, and in any case
both routes yield conforming files. Editorial only: the deciding sentence sits
several sentences below the clause it decides, and a cross-reference at "but the
last" would remove the trap.

### G22 compactor-refusal-turns-on-placement (quiz-03) — CONFIRMED, design-decision

The observation is accurate and every limb of it is stated text: [R-WRT-07] makes
regeneration conditional ("regenerates each tile-index region any of whose stored
extents the output relocates"), §20.5's Example calls placement "the compactor's to
choose", the regeneration paragraph obliges refusal on meeting a structurally
rejected entry, and [R-WRT-01] sanctions carrying a latent violation forward
verbatim. So two conforming compactors given the same nonconforming input diverge
on whether a compaction happens.

No ambiguity — the document licenses both behaviours expressly, so there is nothing
to resolve and no repair is owed. Not byte-level: the input is nonconforming, and
the copied-forward output exhibits exactly the row (T10) the input exhibited, which
every conforming reader rejects at tile scope either way. Filed design-decision
because the maintainer may want refusal to be placement-independent, which would be
a change to [R-WRT-07], not a wording fix.

---

## Coverage count

Groups: 22. Member ids across all groups, counted:
1+1+1+1+2+2+1+1+1+1+1+2+1+1+1+1+1+1+1+1+1+1 = 25. Input ids: 25. No duplicates.

Byte-level upheld: 1 (G4, writer-01). Reporters flagged 1.

## Groups I tried hardest to kill and failed

- **G4 (writer-01)** — five separate searches, listed above. No deciding sentence.
- **G7 (verifier-02)** — searched the whole document for a naming duty over an
  unassigned type's extent; "counted and named" and "report each record" each occur
  once and both inside [R-MTA-10].
- **G15 (register-03)** — §21.1's individuation rules, §21.8, and §24's three VEC
  rules all read, none fixes the pairing.
- **G12 (diagrams-04 + register-04)** — mechanically confirmed 2/120 and the R6/R10
  asymmetry; §21.1's tiebreak does not reach a grammar departure.

## Groups I killed, each with the quotation

G3 (§15.1's "see §15.3" cells), G8 (§2.3's verifier definition + F6 + Appendix H),
G14 (§18.2's "The document rules of this section — the frame constraints of
encoding 2 …"), G17 ([R-CNT-01]'s bridge + §21.1's parenthetical convention),
G18 (§5.2's "everything an earlier commit superseded"), G19 ([R-MTA-10]'s closed
three-item list), G20 (the closed list's first member), G21 ("the permitted side
states the whole of what a commit MAY do to it").
