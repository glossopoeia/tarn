# 0117. The five decisions round 29 put to the maintainer

- Status: Accepted (resolves round 29's five maintainer decisions)
- Date: 2026-09-02
- Covers: §21.7's register-membership sentence and its operational gloss; §21.5
  row R8 and §21.8's instance total; the front-matter block against §2.1
  `[R-CNF-01]`; §9.2 `[R-LIF-02]` steps 4 and 6 against §2.3 `[R-CNF-02]`;
  Appendix G
- Confirm: none

## Context

Round 29 returned **zero byte-level ambiguities** and 26 distinct defects. Five
were not repairs but decisions: each admitted more than one defensible answer, and
under the maintainer's standing direction — prose is not expected to converge, and
a passage too hard to disambiguate is named rather than reworded again — they were
put to him rather than settled in a repair slot. This ADR records the five answers
and the grounds. The remaining twenty-one are repairs and land separately.

## Decision 1 — §21.7's membership sentence states one direction, not two

**Four reporters converged here**, the widest convergence of the round.

The sentence read *"The register carries a row for a condition **exactly where** it
is a detectable file-conformance violation."* "Exactly where" is a biconditional.
Its forward half — a detectable violation the register omits is a defect — is what
§21.1 states normatively and is uncontested. **Its converse is false, of two
classes the document creates on purpose.**

- **Specialization rows.** §21.1 provides that a file is *"recorded against the
  narrower row, whose detector and detection point are the ones that apply"*, and
  names the pairs: F1 of F6/F8, F35 of F36, L24 of L25, F21 of F22, L10 of L11.
  No obliged check separates the narrow condition from the broad one. Take F1: a
  trailer magic holding the byte-reversed constant and one holding eight zero
  bytes both fail `[R-CNT-04]`'s byte-equality identically, with the same outcome,
  and no later check runs.
- **Cause rows.** T13, T15, T16, T23 and T26 say so in their own Condition cells.
  T13: *"the check that detects it is T25's, and this row records the cause rather
  than a procedure of its own"*

Meanwhile four passages **decline** a row on that same ground — §16.2 for a stale
slab declaration, §7.4 for the nesting prohibition, §9.5 for residue past a
completed commit, §20.5 for the compactor's obligations. One test cannot yield
both practices.

**The sentence is weakened to the forward direction alone.** The register carries
a row for every condition that is a detectable file-conformance violation; the
claim that it carries one *only* there is withdrawn.

**The conclusion drawn from it had to be weakened with it, and the first draft of
this decision did not do that.** The sentence continued *"so an unwitnessed
condition is absent from it by that clause's own terms"* — which asserts
*not-detectable ⟹ no row*, the inverse of the new premise and equivalent to the
converse just withdrawn. Two audit lanes found it independently within the hour.
What the forward direction licenses is weaker and is what the sentence now says:
an unwitnessed condition is not a detectable violation, **so the clause requires
no row for it and its absence breaches nothing.** The distinction is between an
absence the clause *entails* and an absence it *permits*, and only the second
survives the weakening.

**The alternative was rejected on ADR-0091's ground.** Keeping "exactly" and
adding a carve-out for specialization and cause rows would resolve the practice
conflict rather than defer it — but it requires a principle distinguishing T13
(cause, granted a row) from §16.2's stale slab (cause, denied one), and the
document states none. Inventing one in a repair slot is what ADR-0091 forbids.
Harmonising the practice — granting rows to the four denied cases, or removing the
five cause rows — moves register totals and discards diagnostic precision the
specialization rule exists to provide.

**A claim the round made about the corpus is false, and is corrected here.** One
reporter held that no vector can be built to exercise T13 rather than T25, over
nine instances. Two exist — **TV-0707** and **TV-0708** — and
`tarn_vectors --verify` reports every vector carrying exactly the defect it
claims, at 275 of 275 instances. The corpus was never in jeopardy; only the
sentence was overstated.

**The operational gloss is aligned with the definition in the same edit.** §21.7
stated its test twice over different comparison classes: the formal definition
over *"some file that does not exhibit it"* — files not exhibiting the condition —
and the gloss three sentences later over *"a conforming one"*. A reporter put both to twenty-two conditions and found
seven where they disagree. The gloss now quantifies as the definition does.

## Decision 2 — R8 enumerates four instances, and §21.8 moves to 277

§21.1 fixes the count: *"An instance names a field the condition ranges over, a
container it can occur in, one of several alternatives the condition text states,
or any combination of the three — a condition applying to two alternatives in two
containers has four."* R8 enumerated its two containers only. Its neighbours
enumerate alternatives as well: **R5 = 8, R6 = 4, R7 = 6.**

R8's own cell invoked §21.1's single-family escape — a non-finite number *"in any
form … alike"*. Its governing rule does not: `[R-MTA-04]` states a disjunction with
two different mechanisms, *"a magnitude that overflows on conversion, `1e400` being
the ordinary case — **or** any of the bare tokens `NaN`, `Infinity`, or
`-Infinity`, which RFC 8259 does not admit"*. §21.1 provides that where a row and
the rule it cites diverge, the rule governs; and its precedents for enumerating
materially different failure shapes are T15's two wrappers and T25's three
malformed streams. These are two different parser paths: one a valid RFC 8259
number failing a binary64 finiteness test after conversion, the other a token RFC
8259 never admits.

**The counterargument, which is recorded in the corpus and was weighed.** The
vector definitions treat the two limbs as one instance on the ground that a
document carrying a bare token *"is not well-formed JSON either, so no two files
could differ on the predicate alone (§21.1's distinguishability test)"*. That test
does not reach this case: it is stated over **a single predicate across several
fields** — *"a sum against a bound, a combination of two flag bits — the fields it
reads are not instances, because no two files could differ"* — and not over
alternatives the condition text states, which §21.1 enumerates in the sentence
above. The overlap the comment identifies is real and is handled by the
specialization clause: a bare-token document exhibits R7 as well, and is recorded
against the narrower row. R7 and R8 carry the **same detector, the same detection
point and the same governing rule**, so which row records it changes no verdict —
only the diagnostic, which is what specialization is for.

**Consequences.** R8's Instances cell enumerates four; its Condition cell drops the
"in any form … alike" framing that asserted one shape. §21.8's total moves **275 →
277**. Two vectors are added for the bare-token limb and the two existing R8
vectors are re-annotated to name their instance. The register's condition count is
unchanged at 120.

## Decision 3 — the front-matter block is labelled *Note*

`[R-CNF-01]`'s exception list is closed: *"§1 (Introduction); any text labeled
*Note*, *Example*, or *Rationale*; and appendices identified as non-normative."*
The front-matter block sat above the rule divider and above §1, carried none of
the three labels, and is not an appendix — so it was **normative while announcing
itself non-normative**, by a device the list does not recognise. It also carries a
gloss of *structural* that drops `[R-ENC-16]`'s verifier clause, so on the literal
reading the document held two normative definitions of that term that disagree.

**The block is relabelled *Note*.** That is a device `[R-CNF-01]` already honours,
it changes no normative rule, and it needs no widening of the exception list. The
parenthetical is dropped as redundant.

**Extending `[R-CNF-01]` to "any text identified as non-normative" was rejected**:
it widens a normativity rule document-wide to solve one passage, and would let any
text exempt itself by self-labelling. A sweep confirmed the collision is unique —
appendices A–E, G and H all carry the parenthetical *and* are appendices, so the
rule reaches them; F carries no marking and is correctly normative.

The *structural* gloss remains wrong about `[R-ENC-16]`'s test and is repaired
separately; the label decision makes it a non-normative gloss disagreeing with a
normative rule rather than a second normative definition.

## Decision 4 — §9.2's durability barriers are declared conduct rules where they arise

`[R-LIF-02]` steps 4 and 6 are writer MUSTs with no byte witness: two files, one
written with barriers and one without, can be byte-identical. `[R-CNF-02]` opens
two doors and the barriers fit neither. Its conduct kinds are *"where a value is
published, or which registry version a writer targets"*; its express-exclusion
door names §6.3's flags = 0 and §6.2's pre-trailer gap as *"the cases this text
states"*. So the enumeration leaves a barrier-less commit producing a nonconforming
file, while the same paragraph's first principle — *"File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or environment"* —
says it cannot. §21.7 does not settle it either: the barriers answer to both of its
absence-classes.

**§9.2 declares steps 4 and 6 conduct rules.** This is the pattern `[R-CNF-02]`
itself prescribes for the door it opens — *"each is declared where it arises rather
than enumerated here"* — and it is the accurate description: a barrier is a fact
about the writing, not a state the bytes can be in. `[R-CNF-02]` is unchanged.

Adding durability to `[R-CNF-02]`'s central list was rejected as centralising what
that rule says should be declared locally. Using the express-exclusion door instead
was rejected as the less accurate classification: it would make the barriers an
exception to file conformance rather than conduct that never entered it.

## Decision 5 — Appendix G pins tile extents and layout

The preamble claims the profile *"closes the degrees of freedom this format
deliberately leaves open"*. Item 2 names three of them in the course of justifying
a byte-derived `file_id`: *"two files carrying the same arrays can legitimately
differ in **tiling, layout**, and codec."* Item 1 closes codec. **Nothing closed
tiling or layout**, and §11.3's Note is explicit that *"Tile extents are a writer's
choice, and this specification imposes none"*, while §14.1 leaves layout to the
writer. An adopter pinning items 1 through 10 and expecting byte-identity did not
get it.

**Item 5 pins fixed declared tile extents and a fixed layout**, on the model it
already sets for alignment, slab and filter: *"§17.3 leaves the choice to the
writer, and no content implies it, so two writers agreeing on everything else
still disagree on bytes without it pinned."* Tiling and layout satisfy that
sentence word for word. The profile becomes complete on its own terms, under one
principle rather than two.

**The clause extends item 5 rather than becoming an eleventh item, and the reason
is renumbering.** Item 5 is already the profile's "things a writer chooses that
content does not imply" item, so the clause belongs there on the merits. It also
avoids moving the numbers, and the numbers are referenced: the closing paragraph
names *"item 8's creator's rule"* and *"the producer pinning of items 1 and 9"*,
and the new clause itself cites item 2. Appendix G still carries ten items.

Naming them instead as inputs the adopter supplies was rejected as sitting
awkwardly against item 2's own framing of them as freedoms over the same arrays.

One sub-claim of the finding is **not** adopted: that the closing paragraph's
inventory wrongly omits tiling, layout and the filter. That paragraph says of
itself *"Read the numbered items as the list; this paragraph names what they are
for, not how many there are."* It makes no completeness claim to falsify.

**A second reader raised the same sub-claim in the audit of this decision**,
reading that very sentence as *presenting* the paragraph as the complete list. It
says the opposite. The claim is declined a second time, and deliberately not
answered by adding the missing items: a longer enumeration would make the
paragraph read more like the checklist it disclaims being, not less. That two
readers have now misread it is recorded here rather than repaired, on the
maintainer's standing direction — the impact is a reader consulting the wrong
paragraph in a non-normative appendix, and the sentence that prevents it is
already there.

## Consequences

**The register moves for the first time this cycle**: 120 conditions over **277**
instances, from 275, and the corpus gains two vectors. `tarn_check` fails while
§21.8 and the table disagree, which is how the change is proved rather than
asserted; the totals are recomputed from the table and never hand-adjusted.

**Appendix G is non-normative**, so decision 5 changes no obligation. Decisions 3
and 4 change what force existing text carries without changing what it requires.
Decision 1 withdraws a claim the document could not support and leaves every row
where it stands.

**Round 30 reads these repairs.** Round 29 met the first half of G3's criterion;
the second half is whether a round reading this work returns zero. Five previous
zeros were each followed by a round that found the next defect in the repairs the
zero produced, and three of this cycle's repairs were defective in ways their own
audits caught — so these five, and the twenty-one repairs beside them, are exactly
the text round 30 exists to test.

## Precedent

- **ADR-0091**, that a rule's reach is not settled in a repair slot — the ground on
  which decision 1 takes the narrow fix and leaves the practice question open.
- **ADR-0104**, requiring an ADR for a register change: decision 2 moves an
  instance total and is recorded here for that reason.
- **ADR-0106**'s limit on property-over-list, and ADR-0116's cut, which between
  them are why §21.7 now states a test with no illustration to fall stale.
