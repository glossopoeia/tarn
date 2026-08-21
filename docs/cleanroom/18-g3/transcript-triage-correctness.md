# Round 18 triage — correctness lens — working transcript

## Disclosure of what I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — §2 (all), §5.1, §5.2,
  §6.1–§6.4, §7.1–§7.4, §9.4, §9.7, §17 (all), §18.1–§18.2, §20 (all), §21.1–§21.9,
  §23.1–§23.3, §24, Appendix G.
- **I ran `ls` on the round18 scratchpad directory once, in my first orientation
  command, before internalising the instruction not to.** The listing returned
  `__pycache__, build.py, calc.py, crc.py, reader.py, sst.tarn` and the six walk
  transcripts plus three quiz transcripts. No `transcript-triage-*.md` file was
  present in the listing and I opened none. I opened no transcript at all — every
  quotation below is from `spec/tarn.md`, checked myself.
- No `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `registry.json`,
  no git history, no web.

## Method

For each finding: locate the cited text, read the surrounding requirement whole,
test whether the reporter's "second reading" is available *in the words* rather
than only in a careless reading, then apply the byte-level test with a quotation.

---

## G1 — §21.7's "witnessed only where … *and* …" (reader-01, verifier-01, diagrams-01, register-03)

Four reporters, one sentence, one defect. Verified verbatim at §21.7:

> §20.3 step 4's bar on a declaration change is witnessed only where the affected
> tiles remain stored *and* the change reaches a byte §14 structurally constrains —
> a padding position, a pad bit, or a boolean byte — where §21.4's content rows fire;
> a change that reaches the decoded size instead is witnessed by T3 or T14 …

Confirmed: T3, T14, T15, T17, T23, T25 all exist in §21.4 with detector *reader*
and their own governing rules ([R-SER-07], [R-COD-04], [R-COD-05], [R-COD-06],
[R-COD-07], [R-COD-08]). Under the conjunctive reading the sentence's own next two
clauses refute it. All four reporters converge on the distributive reading; it is
the only coherent one, and it is consistent — the first conjunct (tiles remain
stored) really is necessary for all three branches, since T3/T14/T15/T17/T23/T25
only fire on stored tiles.

Also verified reader-01's parallel: three clauses earlier the same list uses the
correct construction — "except where §14 constrains a byte's content".

Byte-level: no. Decided by §21.1:

> The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations, §21.7's account of what no check detects, or
> §21.9's limits.

and by [R-CNF-04]: "A reader MUST detect every violation the error register (§21)
assigns to the reader as its detector" — the rows are in §21.4 and are untouched by
either reading of §21.7. §21.7 assigns no detector, tier or outcome.

Premise of my downgrade, stated so it can be attacked: *that §21.7 imposes no
independent obligation, so a reader/verifier's behaviour is fixed by §21.4's rows
regardless.* If someone showed that §21.7 governs which conformance vectors §24
obliges, that would still be corpus arithmetic (§21.8 counts only §21.2–§21.5), not
bytes. I checked §21.8: "Every row of §21.2 through §21.5 — 121 conditions over 273
instances". §21.7 contributes none.

Severity: editorial. Repair: repunctuate as a case analysis.

---

## G2 — §21.7's "exactly as a mis-strided filter is" vs T26 (register-01)

Verified both texts. §21.7: "a mis-ordered image is then witnessed by T2, T4 or T5,
exactly as a mis-strided filter is". T26: "the check that detects it is T2's or
T4's".

Checked the reporter's mechanics myself against §17.3 and T5's condition:

- §17.3: "for a packed boolean plane s = 1 and the filter is the identity"; forward
  shuffle places byte i of group j at offset i·n + j, n = L/s.
- Solve i·n + j = L − 1 with 0 ≤ i < s, 0 ≤ j < n: i = s − 1, j = n − 1, since
  (s−1)n + (n−1) = ns − 1 = L − 1. Source offset j·s + i = (n−1)s + s − 1 = L − 1.
  The final byte is a fixed point of the shuffle at every stride dividing L.
- T5's subject lives only in the final byte: "In a packed planar bool plane with
  P mod 8 ≠ 0, a final-byte pad bit (bit positions P mod 8 through 7)…" (§14.3 puts
  the pad bits there). The reader's inverse at the mandated s = 1 is the identity,
  so the writer's final byte reaches the decoded image intact.

So T5 cannot witness a mis-strided filter; T26 is right and §21.7's analogy
over-reaches. T4 can still fire (padding positions in non-final bytes), so T26's
packed-bool instance remains constructible — the reporter says so too.

Byte-level: no. Whether a given file exhibits T4/T5 is fixed by [R-SER-05] and
[R-SER-08], not by §21.7's account; and §21.1 makes the rule govern over any
restatement. Severity: register-bookkeeping. Repair: drop "or T5" from the
mis-strided half of the analogy, or split the two subjects.

---

## G3 — [R-WRT-09]: "every structure it copies" vs "each relocated extent" (reader-02)

Full text checked:

> A compactor's verification depth follows reliance over everything it carries
> (`[R-WRT-03]`): it relies structurally on every structure it copies, so it MUST
> verify each link of the chain — the open (§19.1), each retained layer's record
> (§19.3) and full index chain (`[R-IDX-04]`), and **each relocated extent's
> checksum, including every stored tile's entry crc** — before emitting that
> structure's bytes.

The reporter's reading (b) — only extents whose offset changes get verified — is
not sustainable against the same sentence. Two things in it decide:

1. The premise is stated *as* the rule: "it relies structurally on every structure
   it copies, **so** it MUST verify each link".
2. The enumeration's own specialisation is unrestricted: "**including every stored
   tile's entry crc**" — not *every relocated stored tile's*. Under reading (b) that
   clause would be inconsistent with the phrase it specialises.

So the defect is a loose word ("relocated") in an enumeration whose premise and
whose own including-clause both quantify universally. PARTIAL: the reporter is
right that the wording is wrong and right about which reading wins, but wrong that
the text leaves it open. Byte-level: no — reading (b) is not a reading the words
permit, so nothing forks; the repair is to write "each extent's checksum".

---

## G4 — [R-LIF-04]'s trailing clause (writer-01)

Text verified at §9.4. Two things the reporter did not test:

(i) **"Committed state" is a defined term and it excludes slack.** §5.2: "Coverage
is a property of the **live committed state** — the front signature block, and every
structure reachable from the live trailer …" and "Every byte the live state does not
claim is **slack**". Residue at [750,900) in his example is slack, hence *not* in the
committed state. On the defined term, the clause "bytes beyond a committed length
never survive into any committed state" is true and near-vacuous; on the loose
reading (physical presence at a commit) it is false in the overwrite path. So the
defect is the loose use of a defined term, not the meaning of "overwrite from F".

(ii) **The byte question is settled by [R-CNT-21] independently of which reading
wins:** "Slack has no internal structure this specification defines, its content is
unconstrained, and no conformance requirement applies to it." Even under his reading
(a), a writer obliged to *overwrite* [F, old physical length) may write any bytes
there — including the same bytes back — so the set of emittable byte sequences is
identical under both readings. That is a stronger downgrade argument than the
reporter's own.

PARTIAL, editorial. Repair: state the guarantee as the physical-length one it can
actually make ("after any commit completes the physical file length equals
committed_file_length"), and say plainly that residue not overwritten becomes slack.

---

## G5 — Appendix G item 8 (writer-02)

Verified: item 2 carries an explicit compactor carve-out ("This is a creator's rule:
a compactor adopting the profile takes `[R-WRT-06]`'s fresh draw instead"); item 8
carries none; item 4 ("One generation") is satisfied by a compacted file, which
carries generation 1 by definition (§20.5). §6.3 says the opposite of item 8's
`flags` = 0 in as many words: "A compactor, though its output is a new file, carries
the input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0 (§20.5, `[R-WRT-06]`)." So the finding is accurate.

Byte-level: no, and the deciding sentence is the appendix's own preamble:

> It adds no requirement to any actor: a writer ignoring it is fully conforming …

A non-normative profile cannot change what a conforming implementation may emit
(§2.1: "appendices identified as non-normative" are excluded from normative text).
Severity: editorial. Repair: scope item 8 to creation as item 2 does, and say what a
profile-adopting compactor writes. Note the interaction with G17: if §20.5's minor
clause is repaired to a MUST, item 8 as written instructs a violation of it.

---

## G6 — one failed checksum forecloses compaction forever (writer-03)

Chain verified end to end: [R-WRT-09] obliges "every stored tile's entry crc";
[R-WRT-06] "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
fails"; §20.5 "Where the table does not license a drop the compactor MUST refuse";
§20.4 "both registered types carry PE = 1, so neither can be dropped". A tile is not
a record at all, so no drop is even in question there. The conclusion holds.

Byte-level: no. Every step is an unambiguous MUST, so there is no second reading;
what the text decides is that the tool emits nothing. The input keeps its verdict.
Severity: design-decision — the maintainer may want this consequence said out loud
(§20.5, §21.7 or Appendix H), or may want a licensed disposal.

---

## G7 — [R-WRT-07] conditions regeneration on relocation (writer-04)

Verified: "except that relocation re-points extent slots, regenerates each
**relocated** tile-index region". The example says the operative fact is different:
"the one kind this operation regenerates rather than copies, since its entries carry
the offsets that moved." Placement freedom is explicit in the same paragraph ("it is
free to place structures anywhere §5.2 admits"), so the coincidence case (region
lands at its input offset, its tiles move) is real and the literal condition
under-covers it.

Byte-level: no, decided by the same requirement's closing sentence:

> The output's reference arrays MUST equal the live generation's bit for bit
> (`[R-MDL-02]`): compaction changes where bytes live, never what a layer denotes.

An output whose entries address slack fails that MUST (and fails T1/T9/F33 on its
own bytes), so [R-CNF-05] bars a conforming writer from emitting it under either
reading. Severity: editorial. Repair: condition regeneration on the entries' targets
moving, not on the region's own placement.

---

## G8 — §23.1's "the only removal of sample data a commit performs" (writer-05)

Verified §23.1 verbatim, and §20.3 step 4's two distinct words in one passage:
"Where a shrink is permitted the **de-addressed** tiles' extents become slack
(`[R-CNT-21]`)" and, lines later, "Extents this commit **supersedes** become slack".
So §20.3 does not treat de-addressing as superseding.

Stronger than the reporter noticed: §23.2 names a *third* removal and routes it back
to §23.1 — "a tile unstored by a later commit leaves its earlier payload in the file
as slack (§23.1)". Unstoring is neither superseding nor a record drop. So §23.1's
"only" is falsified twice over from inside §23 itself, and the intent of the broad
reading is evident.

Also verified the second half: §20.4 lets an updater drop a PE = 0 record of a type
it *does* implement — "For a type the updater implements that this specification
does not register, the definition it implements the type from supplies the flags" —
so §23.1's "an unknown ancillary record's drop" understates it.

Byte-level: no. [R-PRV-01] binds how a tool *describes* an operation
("MUST NOT represent a commit that supersedes data as erasure of it"); no structure
is emitted or withheld either way. Severity: design-decision, because the repair is
to widen a MUST's scope (any commit that makes sample data unreachable), which is a
maintainer's call, not a typo fix.

---

## G9 — §20.4's table scope vs the MU = 1 row (writer-06, adversary-01, diagrams-06)

Three reporters, three entry points, one scope mismatch:

- §20.4 introduces the table narrowly — "For a type the updater does not implement,
  the stored flags are authoritative (§7.3, `[R-CNT-15]`; …), and carry these
  obligations:" — and heads its first column "Stored flags".
- §20.4's own preamble generalises — "Persistence governs every record type; only
  the authoritative source of the flags differs" — and immediately reads the PE
  column for the registered types ("both registered types carry PE = 1, so neither
  can be dropped").
- [R-CNF-06] generalises with a MUST: "MUST honor the preservation obligations of
  §20.4 — which govern every record type, not only those it does not understand."
- §2.4 points at the table for preserve-verbatim: "§20.4's table states the cases:
  its MU = 1 and MU = 0 / PE = 1 rows" — for two registered types the table's own
  lead-in excludes (diagrams-06's angle).

Under the wide reading the MU = 1 row's second sentence ("The updater MUST NOT
modify the scope the record governs") reaches every layer record, since §7.3 fixes
MU = 1 for type 0x0001 and §20.4 says the registry's flags govern for registered
types. That bars the whole of §20.3.

Byte-level: no, and the table refutes itself in its own MU = 0 / PE = 0 cell:

> Superseding a stored tile's bytes re-places that layer's index region (§20.3,
> `[R-WRT-04]`), moving its extent slot (§7.4) and **so modifying that layer's
> record**, which is such a change

An appender modifying a layer record is the premise of that sentence, so the wide
reading cannot be the table's own. [R-WRT-04]'s step 4 is an explicit MUST-ordered
permission to modify layers. adversary-01's residue also checks out: [R-WRT-06]'s
text is "any record whose type it does not implement with MU = 1", so the cell's
"Compaction is barred on the same ground" is self-limiting and does not reach an
implemented-but-unregistered MU = 1 type, which §20.5 expressly admits.

Severity: design-decision. Repair: say which sentences of each cell are the
"preservation obligations" that generalise, and route §2.4's pointer for the
registered types at §20.4's prose rather than at the table.

---

## G10 — foreign-major file that also violates a permanently fixed field (verifier-02)

Both texts verified. §2.3 states the dichotomy exclusion with no exception; §21.2's
preamble restates it and then carves out four rows: "Four rows are outside that
reasoning and do reach it, because their subject is a field fixed across every major
(`[R-CNT-24]`)". §21.1 defines a row as one detectable *file-conformance violation*,
so "reaches it" pulls toward *nonconforming*, while §2.3's blanket sentence pulls
toward *cannot establish*. The tension is inside §21.2's own preamble. Real.

Byte-level: no. §6.2's ordered validation is the same under both readings — "A
reader MUST validate, in order: the trailer magic; the trailer CRC; the version gate
(§6.3) … Any failure is reject-file" — and §2.3's own gloss, "a reader refuses such
a file on capability grounds (§6.3, `[R-CNT-07]`)", holds either way. Only the
verdict label and §24's manifest boolean move; §24 does require "whether the file is
**conforming**", so the corpus feels it. Severity: design-decision.

---

## G11 — partial slack total when a file-scope failure stops the walk (verifier-03)

The reporter says "the text picks neither". It picks one. §9.7 states the principle
for exactly this question:

> … the stored extent of each non-sentinel tile-index entry (an entry `[R-IDX-03]`
> classifies reject-tile on a *structural* ground contributes no stored extent to
> the walk; **one whose stored bytes alone fail its crc keeps its extent**).

A claimant whose covering checksum fails is still a claimant. And §9.7 separates
reaching from verifying — "It checks that these occupy disjoint byte ranges, that
each lies within [16, F − 64), and that each verifies against the checksum covering
it" — with the directory named among the claimants the walk reaches, its bounds
coming from the already-validated trailer. So in his W1 example the answer is 387,
his reading (i).

PARTIAL: a real wording gap (the principle is stated for tile entries only, in a
parenthetical, and not generically), not the open fork claimed. Byte-level: no —
[R-CNT-21] itself: "It is not the file's slack total but a bound on it", and a
partial total only arises on files already established nonconforming or already
uncertifiable. Repair: lift §9.7's parenthetical into a general clause in §5.2.

---

## G12 — §21.6 cites [R-WRT-08] for a rule it does not state (diagrams-02)

Verified. [R-WRT-08]'s sentence is "An updater MUST NOT re-encode a record whose
type it does not implement, and MUST NOT modify one except by relocating its extent
and re-pointing its slot under §20.5" — nothing about dropping or the PE bit.
§21.6's row claims "Ignored, and preserved or dropped per its PE bit" on the
authority of `[R-CNT-15]`, `[R-WRT-08]`. The rule that states preserve/drop-per-PE
is §20.4's table block, which begins "Persistence governs every record type" and
ends before "An updater MUST NOT re-encode…" — and carries no identifier of its own.
[R-WRT-05] labels the paragraph above it. So reading (a) is right and the citation
is loose; §2.2's "Normative requirements carry identifiers" is the standard it
misses.

Byte-level: no. §21.1: "§21.6's entries restate their governing rules on the same
terms a row does, and where such an entry and the rule it cites diverge, the rule
governs there too." The obligations are §20.4's words either way. Severity:
register-bookkeeping. Repair: give §20.4's persistence block an identifier and cite
it (an ADR-level change, since identifiers are permanent).

---

## G13 — §21.5 governing-rule attribution split (diagrams-03)

Checked [R-MTA-04]'s fourth bullet: "every key satisfying §4.6's name rules —
non-empty, at most 255 bytes, free of U+0000 through U+001F". R6 (empty key /
U+0000–U+001F) and R10 (key over 255 bytes) are the same bullet, and cite different
rules first — R6 `[R-CNT-25]`, R10 `[R-MTA-04]`. §21.1: "A Governing rule cell names
that requirement first" (the requirement that *defines* it). So R6 vs R10 is a
genuine inconsistency and R6 is the wrong one.

**The reporter over-extends to R5.** [R-CNT-25]'s own text names R5's subject
explicitly: "content violating the document's own rules (ill-formed UTF-8 included,
`[R-ENC-11]`)". So R5 leading with [R-CNT-25] is defensible; R6 has no such support.
I record this as the qualification on an otherwise correct finding.

Byte-level: no — both cited rules agree on ignore-record and §21.1 makes the rule
govern. Severity: register-bookkeeping.

---

## G14 — R7's Condition omits the BOM its Instances enumerate (diagrams-04, register-02)

Same defect from two reporters; they differ only on which half is wrong.
§18.2's first restriction: "**A JSON object, unmarked.** The top-level value is an
object, and the encoding carries no byte-order mark: a leading U+FEFF makes the
document unreadable." R7's Condition stops at the top-level-object clause; its
Instances enumerate six, including two BOM instances. §21.1 licenses an instance
naming "one of several alternatives the condition text states" — the BOM is not one
the Condition states.

register-02's own rescue (a BOM is already not well-formed JSON under RFC 8259) is
correct as grammar but is not the reading the row takes, since it enumerates the BOM
as a distinct shape — and §21.1 does license enumerating members that "give the
condition materially different shapes". So the Instances cell is the right half and
the Condition is the incomplete one: diagrams-04 gets the direction right.

Byte-level: no. [R-MTA-04] states the BOM rule; §21.1 makes the rule govern over a
row. An implementer who omits the BOM test is violating [R-MTA-04], not exercising a
second reading. Severity: register-bookkeeping. Repair: add the third alternative to
R7's Condition, keeping the six instances and §21.8's 273 total intact.

---

## G15 — §20.3's cost Note drops "or index content" (diagrams-05)

Verified all three: step 4 — "Every layer whose stored-tile set **or index content**
this commit changes has its tile-index region re-emitted in full"; the Note — "any
change to a layer's stored-tile set re-emits that layer's whole tile-index region";
§5.1's caption — "A commit that changes a layer's stored-tile set or index content
re-emits that layer's whole tile-index region as well". Editing one sample supersedes
a tile: the tile is still stored, so the *set* is unchanged while the entry's offset,
length and crc change. The Note's conclusion is right under the rule and does not
follow from the Note's own premise.

Byte-level: no, decided by [R-CNF-01]: "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale* …".
The trigger that binds is step 4's, stated in full. Severity: editorial.

---

## G16 — §21.1 carries no requirement identifier (register-04)

Verified by reading §21.1 to its end: both paragraphs terminate without an
identifier, while §21.7 carries [R-ERR-01], §21.8 [R-ERR-02], §21.9
[R-ERR-03]–[R-ERR-05]. §21.1 does state normative rules in terms — "Its
**completeness is normative**" and "where a row and the rule it cites diverge, **the
rule governs**" — against §2.2's "Normative requirements carry identifiers".

Byte-level: no — the rules are in force as normative text under [R-CNF-01] whether
or not they are labelled, and every citation of them resolves by section number
today (§19's preamble, §21.6's close, [R-VEC-04]). Severity: register-bookkeeping;
the repair mints a permanent identifier, so it is ADR-shaped.

---

## G17 — §20.5's compactor version_minor clause has no modal (quiz-01) — **BYTE-LEVEL, upheld**

The clause, verified verbatim:

> The output trailer copies the input's unknown ignore-lane flag bits forward
> (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the input's
> version_minor — a compactor cannot know which minor version defined an ignore-lane
> bit it does not implement, so it does not lower the floor beneath one.

I tried hard to downgrade this and could not produce the sentence that decides it.
What I checked:

1. **Is the flags half backed by a MUST?** Yes — §6.3: "An updater MUST copy forward
   unknown ignore-lane bits of the file it modifies and MUST NOT clear them", and
   §6.3 names the compactor case expressly. So the first conjunct is anchored.
   **The second conjunct's only cited anchor is a SHOULD.** [R-CNT-26]: "A writer
   SHOULD emit the lowest version_minor … and an appender the maximum of that floor
   and the prior trailer's minor".
2. **Is the appender's identical construction mandatory?** No. §20.3 step 6, inside
   [R-WRT-04]'s "An appender MUST, in order", defers: "version_minor per
   `[R-CNT-26]`" — i.e. MUST comply with a SHOULD, which is a SHOULD. So the
   document deliberately leaves the appender's max-rule advisory. An unexplained
   MUST/SHOULD asymmetry between appender and compactor for the same rule is exactly
   what makes reading (2) available.
3. **Does [R-CNF-01] decide it?** It decides the clause is *normative*; it does not
   decide its *force*. §2.1 says the BCP 14 keywords apply "when, and only when, they
   appear in all capitals", and this clause has none. The drafting discipline stated
   in §2.1's Note cuts both ways: the clause names no actor (it names "the output
   trailer"), which a requirement should, and states no deviation consequence, which
   a SHOULD should. It is well-formed as neither.
4. **Appendix G treats the field as SHOULD-level freedom** — item 8 and the closing
   paragraph: "`version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD" —
   which is a third voice for reading (2).

The fork, concretely: minor-7 input, every feature expressible under this text.
Compactor A writes `07 00` at trailer offset 10; compactor B, reading the clause as
restating [R-CNT-26]'s SHOULD and creating a new file whose floor is 0, writes
`00 00`; the four CRC bytes at trailer offset 60 differ in consequence. Under
reading (1) B may not emit that byte sequence; under reading (2) it may, since
[R-CNF-12] says "Deviation from a SHOULD is not a violation for this purpose".
**That is a change in which byte sequences a conforming implementation may emit,
which is the test as written.** Both outputs are conforming *files* (§6.2 admits any
version_minor; [R-CNT-07] forbids rejecting on it) — the fork is in the writer's
permitted output set, not in any reader's verdict, and I say so plainly rather than
inflating it.

Premise my *upholding* rests on, stated for attack: *that a normative declarative
with no BCP-14 keyword, whose only cited anchor is a SHOULD and whose appender twin
is expressly SHOULD-level, does not by itself carry MUST force in this document.*
If the maintainer holds that every unqualified normative declarative is a MUST, this
collapses to REFUTED — but then §20.3 step 6's "per [R-CNT-26]" and Appendix G's
closing paragraph need reconciling, and the appender/compactor asymmetry needs
stating.

Repair (maintainer's call, one of): give the clause an explicit MUST and say the
appender's rule stays SHOULD, and fix Appendix G item 8 accordingly (G5); or restate
it as an extension of [R-CNT-26] in the SHOULD register, with the deviation
consequence.

---

## G18 — §2.3's "cannot execute a codec or filter" ground (quiz-02)

The reporter says the ground "has no instance: no conforming verifier can be in the
position it describes". That over-claims in two ways.

First, §17.4 already draws the conclusion he says it does not draw:

> For a conforming reader that position arises only at a reserved or experimental
> value, every assigned codec and filter being core: it rejects the layer
> (`[R-COD-03]`, `[R-COD-09]`); software unable to execute an assigned codec or
> filter is not a conforming reader (`[R-CNF-03]`).

Second, the position *does* arise — at a reserved or experimental value a conforming
verifier genuinely cannot execute the codec — and the ground stays live for
[R-CNF-11]'s separate reporting duty: "A verifier MUST report each requirement it was
unable to check on a capability or resource ground, naming the requirement and the
ground, **whichever of the three verdicts it reports**". What is unreachable is the
*cannot establish verdict* on this ground alone, because L43/L45 are established in
the same breath. §2.3's list is a list of grounds for inability, feeding both the
report and the verdict — so it is not a dead branch.

PARTIAL. Byte-level: no — [R-COD-03] and [R-COD-09] fix the outcome ("a reader MUST
treat any other value … as a validity error at layer scope"), so nothing forks.
Severity: editorial at most; a clause noting that this ground reaches the report but
not the verdict would close it.

---

## G19 — the malformed-entry refusal duty is contingent on a free placement choice (adversary-02, quiz-03)

Two reporters, same mechanism, and both resolved it as licensed rather than
ambiguous. I agree with their reading and checked the chain:

- Regeneration is conditioned on relocation ([R-WRT-07]) and placement is free:
  "it is free to place structures anywhere §5.2 admits and every declared layout
  invariant permits".
- [R-WRT-09]'s enumerated checks pass over a structurally malformed entry: §19.3
  "performs no fetch"; the index chain's segment CRCs verify over a malformed entry's
  bytes; and per [R-IDX-03] such an entry has no stored extent, hence no entry crc to
  check (§9.7 confirms: "an entry `[R-IDX-03]` classifies reject-tile on a
  *structural* ground contributes no stored extent to the walk").
- §20.5 says the contingency out loud: "That `[R-WRT-09]`'s checks reach the index
  chain and each stored tile's entry crc rather than an entry's own value domain
  bounds how far a compactor goes looking, **not what it owes on what regenerating
  the region has already put in front of it**."
- The divergent output is sanctioned: [R-WRT-01] "a violation latent in a structure
  they neither modify nor rely on travels with it", §20.5 "a violation latent in a
  structure it carries forward verbatim travels into its output", [R-CNF-12] "For a
  nonconforming file no acceptance obligation exists".

So both compactor behaviours are licensed, on a *nonconforming* input only. Not a
fork in what the text requires; a designed contingency that the regeneration
paragraph does not flag. Byte-level: no (quotes above). Severity: design-decision —
worth one sentence saying compactability of a damaged file is placement-dependent,
if the maintainer wants that visible.

Kept separate from G7: G7's repair (condition regeneration on entry targets moving)
does not close G19, and G19's does not close G7.

---

## Coverage count

Groups and member counts: G1 4; G2 1; G3 1; G4 1; G5 1; G6 1; G7 1; G8 1; G9 3;
G10 1; G11 1; G12 1; G13 1; G14 2; G15 1; G16 1; G17 1; G18 1; G19 2.
4+1+1+1+1+1+1+1+3+1+1+1+1+2+1+1+1+1+2 = **26**. Every input id appears once; I
counted the union against the input list twice by hand.

Byte-level survivors: **1** (G17, quiz-01).
