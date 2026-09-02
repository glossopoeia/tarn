# 0115. §21.7 states a test instead of an inventory, and its walk-through stops being normative

- Status: Accepted (resolves Q-I5)
- Date: 2026-09-02
- Covers: §21.7 and `[R-ERR-01]`; §21.1's two characterisations of §21.7
- Confirm: none
- Erratum: 2026-09-02 — the Decision states the superseded formulation of the test; see the Erratum section.

## Context

Q-I5 has been open since ADR-0096. §21.7 accounts for obligations no single file
witnesses; four ADRs repaired it in four days (0089–0092), it drew a finding
cluster in five consecutive cleanroom rounds — eight findings in round 24 alone —
and each of the four repair audits over ADR-0113 and ADR-0114 drew findings there
again. Every patch produced the next round's findings in the same section.

**The section's measured shape explains the cluster.** Before this decision §21.7
was 926 words, carried no `>` marker and no *Note*, *Example* or *Rationale*
label — so `[R-CNF-01]` made all 926 words normative — and **imposed no
obligation on any actor**: its only MUST and SHOULD were quotations of §20.5's,
belonging to `[R-WRT-06]`. §21.1 expressly places it outside the register's
completeness clause and its instance arithmetic, so no mechanical check reached
it. Full normative force, nothing to discharge it against, and every sentence a
closed universal over 161 requirements and 120 rows.

**The cluster escalated in this cycle from staleness to contradiction.** The
fourth ADR-0113 audit found §21.7 asserting that a commit "escapes … the §14 bar"
where §20.3 step 4 says of the same actor, tense and operation that it "bars it".
An adversarial verifier upheld that byte-level and could not kill it. An account
of what checks miss had become a rule about what a writer may do, with force
enough to contradict the rule it was accounting for.

**And the term the register's completeness turns on was undefined.** §21.1 makes
the register's completeness normative but scopes it to *detectable* violations;
`[R-CNF-07]` applies that gate in assigning outcome classes. Neither defines
"detectable". §21.7 was its only account, by enumeration.

## Decision

**§21.7 states a test.** A requirement is **unwitnessed** where a file that
violates it and a file that satisfies it can present identical live states, so no
check §21.2 through §21.5 states can separate them and there is no condition for
a row to carry. The test decides any requirement put to it without appeal to a
list: ask whether the breach can be made to leave the live state — all §9.7
walks — exactly as a conforming commit would leave it.

**Detectability is its negation, and is now defined**: a violation this
specification names is detectable exactly where some file exhibiting it differs,
in its live state, from every file that does not. §21.1's two characterisations
of §21.7 are swept to match, from "the account, by class, of what fails it" to
"states the test for", with the test quoted where the completeness clause needs
it.

**Being unwitnessed bears on detection and not on permission.** The requirement
binds its actor as any other does; §2.4's outcome classes are assigned to
violations a reader or verifier can establish rather than to every violation the
document names. This is stated because the section's own drift was toward reading
an absence of witness as an absence of obligation, which is the error that made
the ADR-0113 defect byte-level.

**An unwitnessed requirement is distinguished from one no file can violate.**
`[R-ENC-06]`'s fixed field widths are not a state a file can be in; nothing is
omitted from the register on their account because there is no condition to omit.
The old inventory listed them beside genuinely unwitnessed obligations, conflating
two classes. The distinction is now normative and the duplicate entry in the
walk-through is removed.

**The walk-through is demoted to a block labelled *Rationale*.** Under
`[R-CNF-01]` it carries no force. It says of itself that it illustrates the test
and does not extend it, that where an item and the test disagree the test governs,
and that a stale item is a defect in that block and not in the register.

**The split**: 434 normative words and 858 illustrative, where there were 926
normative and no illustration.

## Consequences

**A stale item in the walk-through is now editorial rather than normative**, which
is the property the cycle's evidence argued for: this cycle's §21.7 defect was
byte-level precisely because the account had force. Future failures in that block
change class.

**The test was derived and checked before being written**, which is the step every
previous repair skipped. It was put to all nine members of the old inventory, to
each of the three exceptions the old text stated, and to three witnessed
requirements as controls against over-inclusion — `[R-CNT-06]`'s trailer magic,
`[R-SER-05]`'s padding content, `[R-CNT-11]`'s directory CRC, all of which the
test correctly declines to call unwitnessed. Every member resolved, every stated
exception resolved the right way, and one member — `[R-ENC-06]` — resolved only
vacuously, which is what exposed the conflated class.

**Eleven propagation acknowledgements were recorded and two sites swept.** The
demotion re-registers the whole section as one changed hunk, so every row and rule
the walk-through names lights up; all are sources the walk-through cites rather
than restatements left behind. The two §21.1 sentences were swept rather than
acknowledged.

**The register does not move**: 120 conditions, 275 instances, 329 vectors,
Appendix A byte-identical. §21.7 carries no rows and is outside the arithmetic.

## Alternatives rejected, and retained

The maintainer selected the test option and asked that the others be kept
available, since this section has resisted four previous repairs.

- **(b) Derive the inventory mechanically** — enumerate every requirement, ask of
  each whether a row witnesses it, and make the result a checked artifact beside
  `tarn_check`. **Retained as the fallback if the test proves undecidable for some
  requirement**, which is the one way this decision can fail: the test's whole
  claim is that it decides membership without naming cases. It is also the only
  option that survives if a property cannot be stated at all. Cost: a second
  checked artifact to build and maintain.
- **(d) Label the walk-through** — adopted in substance as part of this decision
  rather than rejected. Option (a) as Q-I5 stated it already called for the cases
  to become non-normative illustration; the two compose, and both are here.
  **Retained as a further step if the walk-through keeps drawing findings even
  without force**: it could be cut rather than demoted.
- **(c) Split the normative claim from the walk-through, both staying normative.**
  Rejected: closest to what four repair cycles already attempted, and it leaves
  the walk-through with the force that let this cycle's defect reach byte-level.

## Precedent

- ADR-0095's property-over-list rule, which Q-I5 identified as the general form of
  this failure, applied to the section that most needed it.
- ADR-0106's limit on that move — a property beats a list only where it is true
  and determinate — which is why the test was derived against every member and
  three controls before it was written.

## Erratum, 2026-09-02

**The Decision above states the test as it was first written, not as it now
stands.** The audit of this decision's own commit (`a4d912e`) found its central
claim logically false and repaired §21.7; the ADR text was not swept with it, and
the pre-round-29 audit found the gap. The Decision paragraphs are left as written
— what they said is part of the trail — and this erratum states what governs.

**The test's subject, instrument and quantifiers.** The Decision defines
*unwitnessed* over "a requirement" and *detectable* over "a violation", and makes
the instrument "identical live states", glossed as "all §9.7 walks" and as "no
check §21.2 through §21.5 states". Every one of those is superseded:

- **The subject is the condition**, for both limbs, as `[R-CNF-13]` individuates
  them. A requirement stating several conditions is classified as a whole by
  neither. §21.7 says so in terms.
- **The instrument is the checks this specification obliges a reader or a
  verifier to perform**, and expressly *not* the register's rows. The Decision's
  "no check §21.2 through §21.5 states" is the keying §21.7 now rejects by name:
  a test keyed to the rows would make §21.1's completeness clause vacuous, every
  omitted condition being undetectable by construction.
- **The quantifiers are duals, not matches.** *Unwitnessed* is *for every file
  exhibiting it, some file that does not*; *detectable* is *some file exhibiting
  it, every file that does not*. They are exact negations **because** each
  quantifier is the other's dual. `a4d912e` repaired the ∃∃/∃∀ mismatch the
  Decision carried but wrote "with matching quantifiers" as the reason — a false
  warrant for a true conclusion, since matching quantifiers would defeat the
  negation. Round 29's audit found it (A-06, confirmed) and §21.7 now reads "each
  quantifier is the other's dual".

**The evidence claim in Consequences is scoped to the superseded test.** "The
test was derived and checked before being written" records a derivation against
the live-state formulation, put to nine inventory members, three stated
exceptions and three controls. That derivation has **not** been re-run against
the obliged-check formulation, and the Consequences paragraph should be read as
history rather than as a standing warrant.

**Five further corrections the pre-round-29 audit confirmed**, all repaired in
the commit carrying this erratum:

- **The register-row criterion needed its qualifier.** "The register carries a
  row for a condition exactly where it is detectable" reaches §21.6, whose
  conditions are detectable and carry no rows because they are not violations.
  It now reads "exactly where it is a detectable file-conformance violation",
  matching §21.1's completeness clause and §21.6's own closing sentence.
- **§21.1's gloss stated the superseded test.** This decision's own sweep of
  §21.1 wrote "a violation is detectable exactly where some file exhibiting it
  differs, in its live state, from every file that does not" — the abandoned
  subject and the abandoned instrument, written into the clause the test exists
  to serve. Three audit lanes found it independently. §21.1 now states the
  obliged-check test with "such a check" spelled out.
- **The walk-through's lead-in claimed a closed set.** "The obligations this test
  places outside the register" reads as complete and is not: §20.4's preservation
  obligations and `[R-CNT-03]`'s zeroing SHOULD both belong and are absent. Per
  ADR-0106's rule against an enumeration that has been wrong twice, the lead-in
  is now indefinite and says the list is not offered as closed, rather than
  gaining two more members.
- **One walk-through item was unconditionally false.** "Where the fills differ,
  §14.5's padding positions and §14.3's pad bits carry the wrong channel's fill
  and T4 or T5 sees it" holds only where the layer has a padding position or a
  pad bit; `[R-GEO-04]` creates the first only where Eᵢ mod Tᵢ ≠ 0 and
  `[R-SER-03]` the second only where P mod 8 ≠ 0. The item now carries that
  condition and states the residue.
- **§18.2 conflated the two classes this decision separated.** "Two of those
  carry no witness a file exhibits" covered both undisclosed dictionary use (an
  unwitnessed condition) and the bar on sizing a buffer from a declared length
  (which binds a reader and states no condition a file can exhibit). The sentence
  now names the two grounds separately.

**What this decision got right, and the audit confirms.** The demotion worked as
designed. Three of the six defects round 29's audit confirmed sit inside the
`> **Rationale.**` block and are therefore editorial rather than normative — the
property this decision was taken to obtain, stated in Consequences as "future
failures in that block change class", and now observed.
