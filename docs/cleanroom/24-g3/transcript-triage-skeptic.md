# Round 24 triage — skeptic pass — working transcript

## Disclosure of what I read and ran

- Read `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (4,445 lines), in
  sequential chunks via `sed -n`. Nothing else in the repo was opened.
- Ran two checks:
  1. `grep -i -E "barrier|durable|R-LIF-02|commit protocol"` over lines 3192–3316 (§20.5,
     Compaction). Result: zero normative hits. The only matches for "pad" are the two ASCII
     figures and one prose sentence about what slack accumulates *per commit*. This
     corroborates writer-01's grep claim.
  2. A python count of every `| Fn | / | Ln | / | Tn | / | Rn |` register row, counting
     instances as `semicolons + 1` and a bare `—` as 1. Result: **121 rows, 277 instances**;
     per table F 36/58, L 49/116, T 26/55, R 10/48. This matches §21.8's "121 conditions over
     277 instances" and each subsection's own stated condition count (36 / 49 / 26 / 10).
     Spot values: R7 = 6, R8 = 2, F30 = 2, F31 = 1, L15 = 4, L16 = 2.
- I did **not** open any `transcript-triage-*.md`, and did not list the round24 directory to
  see what triage files exist — I listed it once at the start of the session before reading
  the instruction's warning in full; the listing showed nine files, none of them
  triage-prefixed (calc.py, count.py, transcript-adversary/diagrams/quiz-answers/quiz-author/
  quiz-key/reader/register/verifier/writer). No triage file existed at that moment and I
  opened none.
- I did not read any walk transcript. Every claim below was re-derived from the spec text.
- I did not read docs/, PLAN.md, AGENTS.md, conformance/, registry.json, git history, or the
  web.

## Method

Default: the finding is wrong and the document decides it somewhere the reporter did not
look. For each finding I hunted for the foreclosing sentence and recorded it, or recorded
that I searched and did not find one. Every downgrade below carries a quotation.

Groups I tried hardest to kill and could not: **adversary-01** and **writer-01**. Both are
recorded below with the counter-premise a downgrader would have to establish, stated
explicitly so it can be attacked.

---

## Group-by-group

### 1. `geo06-witness-account-omits-disk-ordinal` — reader-01, quiz-04

Text under review (§21.7 ¶2):

> the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid
> tile whatever values it carries, except where §14 constrains a byte's content — a padding
> position, a pad bit, or an interleaved boolean — and a mis-ordered image is then witnessed
> by T2, T4 or T5, exactly as a mis-strided filter is

Both reporters attack the same clause from opposite ends. reader-01: a planar layer with
unequal channel element sizes has a *decoded-size* witness (T3 / T14) the clause omits.
quiz-04: the clause addresses the in-tile sample ordinal ("a mis-ordered image") and never
the disk tile ordinal, which [R-GEO-06] also fixes ("orders tile-index entries (§15)").
Same defect, two halves: the sentence's account of [R-GEO-06] does not cover the
disk-ordinal mapping or its witnesses. Grouped.

I re-derived reader-01's instance. Planar, d = 1, E = T = 4 → G = 1, N = 1, P = 4; channels
a (uint8, B = 1) and b (uint32, B = 4); addressed tiles C·N = 2, disk ordinals 0 and 1.
§14.2's planar numeric decoded size is P·Bᶜ = 4 and 16. Swapping the two planes gives entry 0
a 16-byte payload against a derived decoded size of 4. Under codec 1, [R-COD-04]/T14 fires on
the entry's declared length before any fetch; under codecs 2–4, [R-SER-07]/T3 fires on the
decoded length. E == T so there is no padding position, and no bool channel so no pad bit.
So a violation of the ordinal mapping is witnessed with **no** byte's content constrained by
§14 — which is the case the quoted "except" clause says is the only one.

The document knows this class and applies it one paragraph later, for the step-4 bar:

> A change reaching the decoded size is witnessed by T3 or T14, which test a length rather
> than the decoded image's content

Search for a foreclosing sentence: none found in §11.4, §14.1, §15.1 or §21.4. T3 and T14 are
register rows with detector *reader*, and T4 / T5 / L41 with detector *verifier*; the
enumeration in §21.7 is prose about coverage, not a rule.

**Byte-level: no.** The deciding text is §21.1:

> neither this completeness clause nor the instance arithmetic below reaches §21.6's defined
> non-violations, §21.7's account of what no check detects, or §21.9's limits.

§21.7 is expressly outside the register's normative completeness clause. T3, T14, T4, T5 and
L41 are rows in their own right with their own detectors and outcomes, and [R-CNF-04] binds a
reader to every reader-detected row "at the tier that row's *Detected* cell names" regardless
of what §21.7 says about coverage. No emitted byte and no accept/reject verdict moves.

Consensus CONFIRMED. Severity editorial.

### 2. `mis-strided-filter-clause-attaches-T5` — register-02

Same paragraph, different clause: "exactly as a mis-strided filter is", sitting immediately
after "T2, T4 or T5", reads as asserting the same three-row witness set for a wrong stride.

I re-derived register-02's fixed-point argument from §17.3. With stride s and n = L/s, the
filter places byte i of group j at offset i·n + j. Solve i·n + j = L − 1 with 0 ≤ i < s,
0 ≤ j < n: i = s − 1, j = n − 1, and (s−1)·n + (n−1) = sn − 1 = L − 1. The source offset of
that byte is j·s + i = (n−1)s + (s−1) = L − 1. So **the last byte is a fixed point for every
stride dividing L**. §17.3's own worked example agrees (decoded ends `40 40`, shuffled ends
`40 40`). Pad bits live only in a packed planar bool plane's final byte (§14.3), so T5 can
never witness a wrong stride. T26 says exactly that:

> the check that detects it is T2's or T4's, and this row records the cause rather than a
> procedure of its own

and §21.7's own later sentence says the same: "the check that detects it is T2's or T4's,
exactly as T26 has it". So the paragraph contradicts itself internally.

**Byte-level: no**, on T26's text above plus §21.1's tie-break: "where a row and the rule it
cites diverge, the rule governs". [R-SER-05] is a verifier MUST with outcome reject-tile
under either reading; no reader's verdict and no writer's bytes move.

Consensus CONFIRMED. Severity editorial. Kept separate from group 1: different clause,
different repair.

### 3. `21-7-omits-lif02` — diagrams-01, register-03, quiz-02, writer-03

Four reporters, one defect: §21.7 ¶2's list of obligations omitted from the register does not
name [R-LIF-02]. diagrams-01 and register-03 press step 3 (the re-pointed prior directory,
which §9.2's Note expressly says leaves step 3 unperformed); quiz-02 and writer-03 press
steps 4 and 6 (the durability barriers) and the step ordering. writer-03 additionally presses
§20.4's preservation regime ([R-WRT-05], [R-WRT-08]) — I fold that into this group rather
than splitting writer-03's id, and the repair below covers it.

I verified the list is closed and identifier-granular: it names [R-LIF-01], [R-LIF-03],
[R-GEO-06], [R-SER-01], [R-CNT-13]'s embedded-offsets prohibition, [R-CNT-18]'s nesting
prohibition, §20.3 step 4's bar, §20.5's four trailer obligations, and [R-ENC-06]. Two members
are *clauses* of larger rules, so "the class covers it unnamed" is a weak defence.

I checked the two escape routes the reporters name:
- [R-CNF-02]'s conduct carve-out: "§6.3's flags = 0 against a set ignore-lane bit and §6.2's
  pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this text states". The
  barriers are not among them, and §2.3 mentions [R-LIF-02] only to define step 5's pad.
- §21.7's own two classes are "wrong content" and "properties of a file's history". A storage
  barrier is neither — it is a property of how bytes reached the medium. Step 3 arguably fits
  the history class; the barriers do not.

I verified register-03's construction is conforming: a generation-(n+1) commit that appends
only a pad and a trailer pointing at generation n's directory passes every §6.2 gate; the
superseded directory/pad/trailer between the live directory's end and the live trailer are
slack, not structures (§5.2: "everything an earlier commit superseded"), so F7 does not fire;
and [R-CNT-05] says of that gap "a longer gap is conforming".

**Byte-level: no.** Deciding text, §21.1:

> neither this completeness clause nor the instance arithmetic below reaches ... §21.7's
> account of what no check detects

plus [R-LIF-02]'s own "A writer performing a commit MUST, in order", which binds whether or
not §21.7 lists it. No register row is added or removed; by construction no file exhibits a
witness, so no reader or verifier behaves differently.

Consensus CONFIRMED. Severity editorial.

### 4. `21-7-omits-updater-ignore-lane` — reader-04

Distinct from group 3: reader-04's target is the *stated reason*, not just the omission.
§21.7 gives §20.5's four compactor trailer obligations a shared reason —

> the output carries no record that it is a compaction output at all, so no check can know
> that any of the four was owed

— and [R-CNT-08] places the identical ignore-lane obligation on an ordinary updater ("An
updater MUST copy forward unknown ignore-lane bits of the file it modifies and MUST NOT clear
them"), repeated at §20.3 step 6. That one is accounted for nowhere, and the compactor's
reason positively fails for it: an append output *does* record that it is an append output,
via generation > 1.

I checked reader-04's substitute reason and it holds: §5.2 makes the prior generation's
trailer slack ("everything an earlier commit superseded"), and §9.7's walk "walks the live
state only. From the live trailer it reads the live directory" — so the value the new
trailer's flags were to be copied from is not reachable from the file handed over.

I also checked the in-place-note idiom reader-04 invokes and it is real: §7.4's closing Note
("no reader-detectable witness, and so no register row"), §9.5's Note ("carries no register
row of its own"), §16.2's Note (same phrase). [R-CNT-08] gets neither a note nor a §21.7 line.

**Byte-level: no**, on [R-CNT-08]'s own text quoted above — the obligation binds an updater
identically under both readings — and on §21.1's disclaimer of §21.7's completeness.

Consensus CONFIRMED. Severity editorial.

### 5. `cnf03-missing-top-level-qualifier` — reader-03, adversary-02

Straight duplicate. §2.3 [R-CNF-03] scopes the reader's acceptance duty by excluding a file
"carrying no record of a type it does not implement with MUST_UNDERSTAND = 1", with no scope
qualifier; §21.6 says the qualifier is load-bearing.

I tried to kill this by finding the qualifier implied. It is not implied — §2.3's clause is
flat. But the alarming reading (reader may refuse the whole file) is foreclosed, by
[R-CNT-18]:

> an unknown sub-record type with MU = 1 is reject-layer, and where the file is otherwise
> conforming a reader MUST NOT reject the file for it — on a nonconforming file
> `[R-CNF-12]`'s licence to reject on any detected violation is untouched

and by §21.6:

> The qualifier is load-bearing — the same type as a layer sub-record is reject-layer and
> never a ground to refuse the file (`[R-CNT-18]`), so only the top-level case is a file a
> reader refuses

A capitalised MUST NOT directly on point; removing a duty to accept is not a licence to
reject in its face. **Byte-level: no** — no conforming reader's verdict forks. The defect is
that §2.3, which §1 tells the implementer to read first, states the boundary at the wrong
scope.

Consensus CONFIRMED. Severity editorial. Repair is adversary-02's: insert "top-level".

### 6. `verifier-verdict-mu1-sub-record` — verifier-02

Reporter's headline: "No stated verdict for a conforming file carrying an experimental MU = 1
layer sub-record." I set out to refute this and did.

§2.3's *verifier* bullet lists the cannot-establish grounds and states this one **without any
scope qualifier**:

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or *cannot
> establish* — the last where some requirement is one it is unable to check on a capability
> or resource ground, ... when a record carries MUST_UNDERSTAND = 1 with a type it does not
> implement (§21.6)

and

> *Cannot establish* is not a finding that the file is nonconforming, and a verifier MUST NOT
> certify a file it reports that way.

§21.6's carve-out is about a **reader refusing the file**, not about a verifier's verdict, so
it does not withdraw the verifier's ground. The verifier genuinely cannot check the
requirements an unimplemented type's definition imposes, at either scope. So the verdict is
*cannot establish* — the reporter's own Reading 2 — and it is stated, in §2.3's own bullet.
The reporter reached the right answer by a chain the document does not assemble, but the
document does decide it by a shorter route the reporter did not quote.

What survives: the parenthetical "(§21.6)" points at the one passage that carves the
sub-record case out for a *different* purpose, which is a genuine confusability.

**Byte-level: no** — quoted above: a verifier MUST NOT certify on *cannot establish*, and the
priority rule ("An established violation takes priority") means no file moves between
certified and not-certified under either reading. Consensus **PARTIAL**. Severity editorial.

### 7. `index-regeneration-trigger` — writer-02, quiz-01

Straight duplicate. §20.5's clause keys regeneration on the region being relocated; the
operative trigger is that its entries' targets moved. Both reporters build the same
counter-layout (a compactor that emits index regions before payloads leaves a region at
offset 16 while its tiles move).

I confirmed §20.5 imposes no emission order — Appendix G item 3 is the only total order and
is labelled non-normative and a creator's profile. So the literal reading is constructible.

But the divergent output is foreclosed three ways, and I quote the strongest, from the same
requirement's closing sentence:

> The output's reference arrays MUST equal the live generation's bit for bit
> (`[R-MDL-02]`): compaction changes where bytes live, never what a layer denotes.

plus [R-WRT-06]'s "Given a conforming input the output is a conforming file", plus §5.2's
[R-CNT-02] disjointness — a stale entry either overlaps another claimant (F33/L18) or fails
T1/T9. **Byte-level: no**: no conforming compactor can reach the divergent byte sequence.

Consensus CONFIRMED. Severity editorial.

### 8. `compactor-not-bound-to-commit-protocol` — writer-01  **[byte-level upheld]**

This is one of the two I worked hardest to kill.

Confirmed by grep: §20.5 (spec lines 3192–3316) contains **no** occurrence of "[R-LIF-02]",
"barrier", or "durable". §20.2 invokes the creation path by name for a creator ("both
barriers, not one"); §20.3 step 6 invokes steps 4–6 by name for an appender. §20.5 does not,
although it otherwise states the compactor's trailer obligations field by field.

Reading B's textual support, which is what makes it hard to dismiss:
- [R-LIF-01]: "every conforming mutation of a file is either a commit (§9.2) or a whole-file
  rewrite under a new file_id (compaction, §20)" — compaction is set against commit.
- [R-CNT-05], on the pre-trailer pad: "bounds their number only through step 5 of the commit
  protocol, which pads to the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is
  conforming, and **no conforming commit produces one**." The qualifier is *commit*, not
  *writer*, in a sentence that had every opportunity to say *writer*.
- [R-LIF-02]'s own antecedent is "A writer performing a commit MUST, in order".

Candidate foreclosing sentences I found and why each fails:
- [R-WRT-01]: "An appender and a compactor satisfy every writer requirement for the bytes
  they produce". This is the best candidate for killing the byte half. It fails because it
  does not rewrite the antecedent of a conditional requirement: a rule conditioned on
  "performing a commit" imposes nothing on an actor not performing one. And the drafters
  plainly did not think it sufficed — a creator is covered by the same principle
  ([R-CNF-05]) and §20.2 still spells [R-LIF-02] out.
- [R-CNT-01]: "A TARN file is written generation by generation (§9)". Descriptive anatomy,
  not an obligation on a compactor.
- Appendix H, "Conforming writer — ... follows the commit protocol including both barriers
  (§9.2)". This is the strongest evidence of *intent* — and it is expressly non-normative:
  "each entry's authority is the requirement or section cited, never this summary", and the
  cited §9.2 is the rule whose antecedent is at issue.

So the document does not decide it. Reading A is the better design reading (§20.5's output is
a new file at generation 1, exactly [R-LIF-02]'s creation path) but is nowhere stated.

**Byte-level: YES.** Under reading A no conforming writer of any tier emits a file whose
pre-trailer gap exceeds step 5's pad — creator and appender are both bound by name. Under
reading B a conforming compactor may pad its trailer out to a device block boundary and emit
a file thousands of bytes longer, with a gap [R-CNT-05] itself calls conforming. Both files
are conforming *files*, so no reader's verdict separates them and [R-CNF-05] cannot settle
it; what differs is exactly the set of byte sequences a conforming implementation may emit,
which is the test as stated. §16.1's own Note ("4096 — the page size and modern physical
sector size — is the recommended value") shows wanting that pad is ordinary, not contrived.

**The premise my grade rests on, stated for attack:** that step 5's pad is the *only* bound
on the pre-trailer gap ([R-CNT-05] says so in terms), and that step 5's antecedent does not
reach a compactor. A downgrader must establish either that [R-WRT-01]'s "every writer
requirement for the bytes they produce" strips the antecedent, or that producing a
generation-1 output *is* performing a commit — neither of which this text states about a
compactor.

The durability half (a compactor may write its trailer before its relocated payloads are
durable) is not byte-level and is the more consequential half.

Consensus CONFIRMED. Severity byte-level.

### 9. `compactor-version-minor-antecedent` — reader-02

§20.5's SHOULD conditions the minor floor on a fact about the input, and names as one of its
two cases "an unrecognized `tarn.` key in a record it never decoded (§18.3)". A compactor's
verification depth is [R-WRT-09]'s — "each relocated extent's checksum" — and §20.5 itself
relies on that bound ("No other record payload carries a file offset"); [R-MTA-02] quarantines
the document. So for half its stated scope the antecedent is not evaluable.

I searched §20.5, §18.3, [R-CNT-26] and Appendix G item 8 for a resolution. Appendix G item 8
restates the same conditional and is non-normative. None found.

**Byte-level: no.** Deciding text, [R-CNF-12]:

> Deviation from a SHOULD is not a violation for this purpose: §21's register enumerates
> MUST-level conditions only, and a verifier reports a SHOULD deviation as an advisory that
> does not bar certification.

Both minor values are therefore emitted by conforming compactors under either reading; the
emittable set does not move even though the two bytes at trailer [10,12) differ. The cost is
to an implementer who must guess, and to tooling reading the minor as a feature floor.

Consensus CONFIRMED. Severity design-decision — this needs a maintainer ruling, not a
wording fix.

### 10. `23-1-omits-unstore` — writer-04

§23.1: "A commit removes sample data two ways — superseding it, and a shrink that de-addresses
tiles (§20.3 step 4)". §20.3 step 4 lists three dispositions, not two: "entries for tiles this
commit stores or supersedes written to their new state, entries for tiles that become
unstored written as the sentinel, entries new to this generation".

I tried to refute by folding unstore into "superseding". §20.3's own text separates them, and
§23.2 cross-references §23.1 for exactly this case — "a tile unstored by a later commit leaves
its earlier payload in the file as slack (§23.1)" — pointing at a passage where it is not
among the two. So the enumeration is incomplete as written, and §23.2 assumes it is not.

**Byte-level: no.** The rule's own quantifier already reaches the omitted case:

> Writers and the tools built on them MUST NOT represent **any commit that makes sample data
> unreachable** as erasure of it

No actor's obligation is in doubt; the bytes a commit writes are identical either way (the
entry is the sentinel, the payload is slack).

Consensus CONFIRMED. Severity editorial.

### 11. `r8-collapses-non-finite-forms` — writer-05

Verified mechanically: R8 = 2 instances, R7 = 6 instances, register total 121/277 matching
§21.8. So R8's cell yields two vectors and both may legitimately use `1e400`; an
implementation whose JSON parser accepts a bare `NaN` — the commonest way to be wrong here —
passes the corpus.

Checked §21.1's licence. It states only two axes as pre-decided ("Where the quantity a
condition derives varies by layout ... Where the condition compares two **magnitudes**"),
leaving the rest to judgement, so R8's collapse is *permitted by the letter*. But its sibling
R7 — drawn from the same bullet list in §18.2 — enumerates three alternatives, and
[R-MTA-04]'s own text separates the two forms with "or" and adds an operational warning
("which RFC 8259 does not admit and some parsers accept regardless"). A conversion overflow
inside a valid JSON number and a token RFC 8259's grammar does not define are on opposite
sides of the parser.

**Byte-level: no.** Deciding text, [R-MTA-04]:

> A document is unreadable if it contains a number whose binary64 interpretation is not
> finite — which covers a magnitude that overflows on conversion, `1e400` being the ordinary
> case — or any of the bare tokens `NaN`, `Infinity`, or `-Infinity`

All four forms are unreadable, R8 says so, every reader takes ignore-record. What is at stake
is [R-ERR-02]/[R-VEC-03] corpus coverage.

Consensus CONFIRMED. Severity register-bookkeeping.

### 12. `r7-condition-cell-drops-bom` — register-04

Verified: R7's Condition cell states two alternatives; its Instances cell enumerates six,
including two BOM instances. Verified the arithmetic claim mechanically — with R7 at 6 the
register totals 277, matching §21.8; at 4 it would total 275.

I tried to refute by arguing a leading U+FEFF *is* "not well-formed JSON" under RFC 8259
(whose `ws` production admits only space, tab, CR, LF), so the first alternative already
covers it. That defence works for the rule but not for the cell: §18.2 states the BOM
separately precisely because real parsers skip it, and register-04's implementer failure mode
is exactly that — a BOM-skipping parser reports the document as well-formed JSON with an
object at top level, so R7's condition **as written** is not met and the parser ships.

**Byte-level: no.** Deciding text, [R-MTA-04]:

> the encoding carries no byte-order mark: a leading U+FEFF makes the document unreadable

plus §21.1's "where a row and the rule it cites diverge, the rule governs". Consensus
CONFIRMED. Severity register-bookkeeping.

### 13. `f31-l16-boundary-inconsistent` — register-05

Verified from the tables: F31 says "extent_offset in 1-15"; L16 says "extent_offset < 16";
[R-CNT-13] says "an extent_offset < 16". F30/F31 are therefore disjoint at file scope while
L15/L16 overlap at layer scope on the slot (0, nonzero), for one and the same rule clause.
§21.1's specialization list names F1/F6, F1/F8, F35/F36, L24/L25 — not this pair — so the
specialization machinery gives no answer, and [R-VEC-02]'s "where a condition cannot be
isolated" is where it falls.

**Byte-level: no.** Deciding text, §21.1: "where a row and the rule it cites diverge, the rule
governs" — so [R-CNT-13]'s "< 16" is the operative bound at both scopes. Identical outcome,
detector and detection point on either rendering; the union covers the clause either way.
Only corpus attribution for the single slot (0, nonzero) is affected.

Consensus CONFIRMED. Severity register-bookkeeping.

### 14. `foreign-major-verdict-label` — register-01

§21.2's preamble asserts four rows "do reach" a file §2.3 declares neither conforming nor
nonconforming, and §21.1 defines a register row as "one detectable file-conformance violation
this specification names". The case is constructible: valid trailer magic, verifying trailer
CRC, version_major = 7, and a front block that is not byte-identical to the constant —
[R-CNT-24] fixes that block "in every format major version", so F6 fires on bytes this
document says are wrong under major 7 too.

The tension is real and I could not resolve it from the text. §2.3 says "a file declaring
another major is neither conforming nor nonconforming under it ... and that refusal is not a
finding about its bytes", which pulls toward *cannot establish*; §2.3 also says "An
established violation takes priority: a verifier that has established any violation reports
*nonconforming*", which pulls the other way once F6 is granted to be an established
violation. §21.2's preamble grants exactly that and never says what verdict follows.

**Byte-level: no.** Deciding text, §2.3:

> *Cannot establish* is not a finding that the file is nonconforming, and a verifier MUST NOT
> certify a file it reports that way.

Under both readings every reader is at reject-file (version gate or F6) and no verifier
certifies, so the certified set is identical; no writer can emit a major-7 file under this
text. Only the printed label differs.

Consensus CONFIRMED. Severity design-decision — a maintainer must rule on whether F6 on a
foreign-major file is an *established violation*.

### 15. `21-2-geometry-terminology` — quiz-03

Checked "geometry" everywhere it appears: §11.1's heading "Geometry and its validity floor",
§19.3's "the geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`)", §20.3's "the
grown geometry", §21.3's L21 "geometry-derived addressed-tile count". Every one is *layer*
geometry. §21.2's file-scope table contains no layer-geometry row, so under that sense the
carve-out excludes nothing and the contrast with "Four rows are outside that reasoning" has no
first term. The intended sense must be the file's own byte geometry — the offsets, lengths
and sizes F5, F9, F10, F13, F16, F17 test. The italicised *geometry* signals a special sense
without defining it.

**Byte-level: no.** Deciding text, §6.2 [R-CNT-06]: "A reader MUST validate, in order: the
trailer magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose
positions are fixed across all majors (`[R-CNT-24]`)". That order, not this paragraph, fixes
which checks a foreign-major file is subjected to, and it is identical under both senses of
the word.

Consensus CONFIRMED. Severity editorial.

### 16. `partial-total-before-live-trailer` — verifier-01

I set out to refute this and largely did.

The reporter is right on one point: F6's governing rule is [R-CNT-04], and §21.2's preamble
itself places it outside §6.2's ordered validation ("F6 with F1's front-block instance, which
`[R-CNT-04]` places before other processing"), so §5.2's exemption — cited to "§6.2's ordered
validation" — does not name it. F5 is weaker: its Governing-rule cell is "`[R-CNT-27]`
(R-CNT-01, **R-CNT-06**)", so F5 is reachable through §6.2's gates on any concrete file (a
100-byte file's committed_file_length is not a multiple of 64).

But the reported consequence does not follow. Reading (2) requires the partial-total limb to
fire with no F, and two sentences foreclose it. §9.7 [R-LIF-08]:

> A verifier checking `[R-CNT-02]`'s partition walks the live state only. **From the live
> trailer** it reads the live directory

— there is no walk to be incomplete before a live trailer exists. And [R-CNT-21]'s own reason
clause is general, not restricted to its citation:

> there is no F and no live state to walk, so the total is not owed at all: the verifier
> reports the trailer failure and nothing about slack, which is not a partial total but the
> absence of one

An uncomputable MUST is not a reading a competent implementer adopts, and the structural
definition of the walk decides it. What survives is a wording imprecision: the exemption is
scoped by citation more narrowly than by reason.

**Byte-level: no**, on the two quotations above; under both readings the file is reject-file
and the verifier's verdict is nonconforming. Consensus **PARTIAL**. Severity editorial.

### 17. `appendix-h-partial-total-condition` — diagrams-02

Distinct from group 16, and in the opposite direction: §5.2's exemption is too narrowly
*cited*; Appendix H's condition is too *broad*. Appendix H's verifier entry makes the
condition "where its walk did not complete", which on its face covers a walk that never began
because the trailer failed its magic, CRC or field gates — exactly the case [R-CNT-21] spends
four lines carving out. The number it would then direct a verifier to report is not
computable, F being undefined. Disjoint row sets (F8/F14/F9–F17 here; F5/F6 in group 16), so
not merged.

**Byte-level: no.** Deciding text is Appendix H's own disclaimer — "each entry's authority is
the requirement or section cited, never this summary" — and the cited [R-CNT-21], quoted in
group 16. §21.6's slack row has the same two-way shape but is a condition row predicated on
slack existing, which presupposes a live state, so it is defensible; Appendix H's entry is
predicated on nothing. No file's conformance and no verdict changes.

Consensus CONFIRMED. Severity editorial (non-normative appendix).

### 18. `21-6-mimic-row-justification` — diagrams-03

§21.6's row states a **payload** condition and justifies it with "nothing enumerates slack".
A payload is enumerated by §9.7's walk, as that entry's stored extent. §22.3 keeps the two
cases apart in terms: "Under live-state coverage a mimic in slack is inert — nothing
enumerates it — but a recovery tool that truncates to one produces a different file".
[R-LIF-06] states the payload case directly: "a tile payload can deliberately contain a byte
string that mimics a valid trailer, so recovery output MUST be re-verified as a whole file".
So the row's cited rule and verdict are right and only its first justification clause is
misplaced.

**Byte-level: no.** Deciding text, §21.1: "§21.6's entries restate their governing rules on
the same terms a row does, and where such an entry and the rule it cites diverge, the rule
governs there too."

Consensus CONFIRMED. Severity editorial.

### 19. `4-7-note-omits-size-column` — diagrams-04

Verified all six layout tables against §4.7's Note:
- §6.2 — Offset | Size | Type | Field | Class | Valid values: all six.
- §15.1 — same six.
- §18.2 — same six.
- §6.1 — Offset | Size | Value | Class: covered explicitly by the Note.
- §7.2 — Offset | Size | Type | Field | Class: covered explicitly ("folds each field's range
  into its Field cell").
- §7.4 — **Field | Type | Constraint**: omits Offset, Class **and Size**. The Note names two.

§7.4 is the only table whose omissions the contract states incompletely, and the Note supplies
the analogous reasoning explicitly for §6.1 and §7.2 while leaving it to the reader here.

**Byte-level: no.** Deciding text, [R-ENC-06]: "No field's width is ever a writer choice:
every field's width is fixed by this specification" — and §7.4's Type column gives every width
(`u8`, `u16`, `u64`, `u8 len + bytes`). No implementation can read a different width out of
this.

Consensus CONFIRMED. Severity editorial.

### 20. `shrink-into-fill-valued-padding` — adversary-01  **[byte-level upheld]**

The second one I worked hardest to kill.

(A), §20.3 step 4:

> The test is the effect on such a tile, and the list names where that effect arises rather
> than standing on its own: a change that leaves every one of those tiles' stored bytes
> meaning exactly what they meant — a filter whose mandated stride makes it the identity
> (`[R-COD-10]`), **or a new padding position whose stored byte already holds the fill
> `[R-SER-05]` fixes** — is not what this bars.

(B), two paragraphs later:

> Unstoring that tile in the same commit does not rescue it either, and for the same reason:
> the quantifier is the superseded generation's, so **a shrink that turns real positions into
> padding of a tile stored there is barred whether or not the new state still stores it**.

I verified adversary-01's referent argument independently. A padding position of a tile at
grid index tᵢ is a position with coordinate ≥ Eᵢ inside [tᵢ·Tᵢ, (tᵢ+1)·Tᵢ). **Raising** Eᵢ
strictly shrinks that set, so a grow never adds a padding position to a tile the prior
generation stored; new tiles a grow addresses were not stored in the superseded generation and
carry no §14 obligation under the bar. Changing any Tᵢ changes P and the decoded size, or the
sample byte offsets — barred outright. Changing rank, channel count or channel order changes
Q or the offsets — likewise. Changing fill alters the content at existing padding positions,
not the set of them (§20.3's shape (c) treats it separately). **So (A)'s second carve-out has
exactly one referent, and it is the case (B) forbids.**

I verified the construction arithmetically. E = 6, T = 4, d = 1, C = 1, uint8, interleaved,
fill 0x00: G = ⌈6/4⌉ = 2, entry_count = 2, P = ∏Tᵢ = 4, Q = 1, decoded size P·Q = 4. Tile 1
covers x = 4…7; with E = 6, x = 4 and 5 are real and x = 6, 7 are padding holding 0x00.
Shrink E to 5: G = ⌈5/4⌉ = 2 unchanged, so entry_count, every disk ordinal and the stored-tile
set are unchanged; x = 5 becomes a padding position whose stored byte is already 0x00, which
is the fill [R-SER-05] fixes. T4 passes, the live state is clean, every verifier certifies.

Candidate foreclosing sentences and why each fails:
- (B)'s own opening, "the bar above is the whole of the test, **in the bar's own tense**".
  This is the strongest candidate and it favours (A) — the bar above *includes* (A)'s gloss,
  so (B) cannot add to it. It fails as a foreclosure because (B)'s closing clause is stated
  as a universal ("is barred"), and if (A) governs, that clause is false as written for
  exactly the case (A) names. One of the two sentences has to be edited either way.
- §11.1's Rationale: "a shrink is barred wherever it alters what §14 fixes for such a tile —
  whether or not the new state still stores it". §2.1 makes Rationale text non-normative, and
  it is ambiguous on its face: turning an unconstrained position into a fill-constrained one
  changes *which* constraints §14 imposes while changing no stored byte and breaking none.
- §21.7's account. It leans toward (A) — "A change reaching a byte §14 structurally
  constrains — a padding position, a pad bit, or a boolean byte — fires §21.4's content rows"
  would be false under (B), since T4 passes when the byte already holds fill — but it is an
  account of coverage, not a rule, and §21.1 puts it outside the completeness clause.

So the document contains two normative sentences that, read literally, give opposite answers
for one commit, with the surrounding text leaning toward (A) and never saying so decisively.

**Byte-level: YES.** Appender P (reading A) emits a 448-byte generation-2 file; appender Q
(reading B) must refuse and tell its caller to rewrite whole under a fresh file_id. That byte
sequence — same file_id, generation 2, generation 1's bytes as an intact committed prefix,
dimension extent 5 — is producible by no other conforming writer: [R-LIF-02]'s creation path
fixes a creator at generation 1, and [R-WRT-06] fixes a compactor at generation 1 under a
fresh file_id. So the set of byte sequences a conforming writer may emit differs between the
readings. It is *not* byte-level on the accept/reject half — the live state stays clean and
every verifier certifies the 448-byte file under either reading.

**The premise my grade rests on, stated for attack:** that (A)'s "or a new padding position
whose stored byte already holds the fill" is a genuine carve-out with the shrink as its only
possible referent, and that (B)'s closing universal is therefore in conflict with it rather
than a loose restatement of it. A downgrader must establish either that (A)'s carve-out has
some *other* referent reachable by a permitted change (I enumerated the declaration changes
above and found none), or that (B)'s "is barred" is read by every competent implementer as
implicitly qualified by (A) despite naming (A)'s exact case.

Consensus CONFIRMED. Severity byte-level.

### 21. `unassigned-type-extent-unreported` — verifier-03

§8.1's map, final row: "| Extent of a record of a type this specification has not assigned |
none — the bytes are opaque (§7.2) | — |". §21.6 makes an experimental-range MU = 0 record a
conforming file, and §9.7's walk checks each claimant "against the checksum covering it,
**where §8.1's map states one**" — so these bytes are claimed, unchecksummed, uninspected and
uncounted-as-slack.

[R-MTA-10] imposes the parallel duty on the sibling residue:

> it MUST report each record it ignored on this ground, naming the owning scope, the encoding
> value, and the stored extent length, as it reports the slack total (`[R-CNT-21]`): bytes a
> certificate covers without inspecting are counted and named, never silent.

§22.3 sets the two residues side by side, calls the unassigned-type extent "equally
invisible" — strictly worse, since the metadata extent at least carries a terminal CRC — and
gives the reporting duty to only one. Appendix H's verifier checklist carries the [R-MTA-10]
line and not this one.

I searched [R-CNF-11], [R-CNT-21] and §9.7 for a residual duty that would cover it. [R-CNF-11]
obliges a report only for "each requirement it was unable to check on a capability or resource
ground", and no requirement attaches to these bytes, so nothing is unchecked. §5.2's slack
total does not reach them: they are a claimed structure, not slack. So none exists — the
reporter is right that this is decidable rather than ambiguous.

**Byte-level: no.** Deciding text, [R-CNT-15] plus §21.6's row: an experimental-range MU = 0
record is "Ignored, and preserved or dropped per its PE bit", the file is conforming, and the
verifier's verdict is conforming either way. Only the certificate's content differs.

Consensus CONFIRMED. Severity design-decision — whether to extend [R-MTA-10]-style reporting
is a maintainer call, and §22.3's own framing argues for it.

---

## Coverage

27 input ids. Union of group member_ids = 27, no duplicates, no omissions. Counted twice by
hand against the input list and once by construction of the output object.

Byte-level count: **2** (writer-01, adversary-01). No finding was dropped for weakness; the
two PARTIAL grades (verifier-02, verifier-01) are recorded with the sentences that decide
them.
