# Round 22 triage — SKEPTIC pass — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full-by-section
  (targeted greps + sed ranges): §2.1, §2.2, §2.3, §2.4, §2.5, §3.1, §4.7's Note,
  §5.1's three-commit Example, §5.2 [R-CNT-21], §7.4's table, §9.7 [R-LIF-08],
  §17.2 codec-4 rule + Note, §18.2 [R-MTA-09] entire, §19.1 step 4, §19.2
  [R-RDR-02] + Rationale, §20.3 shapes (a)/(b)/(c), §20.4 entire incl. the
  updater-obligation table, §20.5 head, §21.1 entire, §21.2 head + F-rows
  cited, §21.3 rows L1/L2/L3/L5/L6/L21/L23/L44/L48/L49, §21.4 rows T22/T23/T24/T25,
  §21.5 preamble + rows R1-R4/R9/R10, §21.6 entire, §21.7 entire, §21.8, §21.9
  entire incl. table, per-instance paragraph, [R-ERR-04] and the Note,
  §24 [R-VEC-01]..[R-VEC-04].
- **No** transcript files were opened. Not the walk transcripts, not the quiz
  transcripts, and above all not any `transcript-triage-*.md`. I listed the
  round22 directory once (`ls`) before reading the instruction closely enough;
  the listing showed filenames only and no `transcript-triage-*` file existed in
  it at that moment. I opened nothing from it.
- No `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
  `spec/registry.json`, no git history, no web.

## Grouping

Two big clusters and eight singletons. 20 ids, 10 groups, no id in two groups.

- **G1 tile-quantifier** (6): reader-01, writer-01, verifier-01, register-02,
  adversary-01, quiz-01. All six quote the same sentence in §21.9 and pose the
  same question: does "the tiles ... a file actually contains" mean addressed or
  stored? All six *picked reading A*. Five flagged byte-level; register-02 alone
  flagged no, on my own grounds.
- **G2 R3-and-the-content-size-condition** (6): reader-02, verifier-03,
  diagrams-02, register-01, adversary-02, quiz-03. One defect with three faces —
  R3's Condition cell, its Governing-rule cell, its Instances cell — all created
  by the same edit ([R-MTA-09]'s new MUST routed into R3 without revising R3).
  diagrams-02 adds an R3-vs-R4 fork; I merge it because the same edit to R3's
  condition cell resolves it and because R4's own "unlike R3" clause plus
  §18.2's express "within the meaning of R3" already decide it.
- Singletons: verifier-02, diagrams-01, diagrams-03, diagrams-04, register-03,
  register-04, register-05, quiz-02.

## G1 — the one I tried hardest to uphold

The text, verbatim (spec line 3686-3693):

> The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains, and a
> file containing none of a kind does not exceed that row, whatever its
> declarations would derive — a layer addressing no tile (§11.2) has no tile
> whose decoded size the table can bound, exactly as `[R-COD-07]`'s cap is
> quantified over a layer's *addressed* tiles. The first five range over
> declarations, which every file and every layer carries.

I verified the reporters' factual scaffolding rather than taking it:

- [R-COD-07] (line 2321): "Writers MUST NOT declare this codec for a layer any
  of whose addressed tiles' decoded size exceeds 0x7E000000 bytes". Quantifier
  confirmed: addressed.
- §17.2's Note (line 2328): "The cap is quantified over the layer's *addressed*
  tiles, so a layer that addresses none — any dimension extent 0 — satisfies it
  **whatever its tile shape declares**".
- §20.3 step 4 (line 3001): "`[R-COD-07]`'s lz4 decoded-size cap ... which an
  empty layer escapes only because that cap is quantified over addressed tiles".
- L44 (line 3473): "any of whose addressed tiles' decoded size exceeds".
- §3.1 (line 312): "every tile of a layer is *addressed*. A tile is *stored in a
  generation* if and only if that generation's tile-index entry for it is not the
  sentinel". "Contains" is not a defined predicate for either.
- [R-CNF-03] (line 163): acceptance duty runs to a file "none of whose values
  exceeds the minimum guarantees of §21's limits table".
- [R-ERR-04] (line 3697): "Software that declines **on that ground** a file whose
  every quantity lies within the table is not a conforming reader".

So the fork the reporters describe is real *if* reading B is permitted. It is
not, and the deciding text is the clause the reporters themselves quote:

> **"exactly as `[R-COD-07]`'s cap is quantified over a layer's *addressed*
> tiles."**

**The premise my downgrade rests on, stated for attack:** the term after
"exactly as" is a *quantifier proposition* — "[R-COD-07]'s cap **is quantified
over** a layer's addressed tiles" — not a vacuity proposition. A comparison whose
second term states a quantifier asserts that the first term's quantifier is that
one. Under reading B the §21.9 tile row would be quantified over a strict subset
of [R-COD-07]'s set, so "exactly as" would be false. A reading that falsifies an
explicit clause of the very sentence being construed is not a permitted reading
of it, and the imprecise "actually contains" (not a §3.1 term of art, compatible
with either) is construed by the precise clause rather than the reverse.

The best attack on that premise is the adversary's: that "exactly as" compares
only the *mechanism* — per-instance quantification, vacuous when the instance set
is empty — which stored tiles also exhibit. I tested it and rejected it on three
further signals, none of which any reporter raised:

1. *addressed* is **italicised** in §21.9's gloss, exactly as it is italicised in
   §17.2's Note. The italics mark which set, and the only thing in the sentence
   that needs telling is which set the tile row ranges over — for documents and
   frames it is obvious. Emphasis on the set is pointless if only the mechanism
   is being compared.
2. The gloss's trailing contrast "does not exceed that row, **whatever its
   declarations would derive**" is a verbatim structural copy of §17.2's Note
   "satisfies it **whatever its tile shape declares**". §21.9's sentence is
   patterned on the [R-COD-07] Note, whose whole subject is the addressed
   quantifier.
3. Drafting economy. Under B the natural and far more useful gloss would be "a
   layer *storing* no tile has no tile whose decoded size the table can bound" —
   the broad, surprising consequence. The drafter instead glossed the strictly
   narrower case (addressing no tile), which is informative only under A. Under B
   the gloss would be weaker than the rule it glosses, which glosses do not do.

I also tested writer-01's strongest independent argument — that under A the tile
row is itself declaration-derived, collapsing the paragraph's own contrast with
"The first five range over declarations". It does not collapse: under A the row
still differs from a declaration row exactly in the extent-0 case, which is
precisely the difference §17.2's Note draws for [R-COD-07] ("a layer that
addresses none ... satisfies it whatever its tile shape declares" versus
"[R-ENC-04]'s overflow rule carries no such quantifier ... so P·Q and P·Bᶜ are
checked in an empty layer even though this cap is not"). The per-instance/
declaration contrast does real work under A.

And writer-01's collision claim — that under A [R-ERR-04]'s licence to decline
collides with [R-TYP-08]'s MUST to return fill — fails: [R-ERR-04] licenses
declining "at the narrowest scope whose declarations exceed what it can serve, a
layer or a tile", and a reader that declines serves nothing, so [R-TYP-08] (which
binds what a reader that serves returns) never bites. No collision, so no reason
to prefer B.

**Verdict:** PARTIAL / not byte-level / editorial. The wording defect is real —
the operative clause borrows its quantifier from a trailing analogy instead of
stating it, and uses a phrase §3.1 does not define where §3.1 supplies a precise
pair — and six independent readers stopping on it is evidence the sentence should
be repaired. But the sentence decides it, so the emittable and must-accept sets
do not fork. Repair: one word. This is the group where a wrong downgrade would be
most expensive, and I have stated the premise so it can be attacked.

## G2 — R3 and [R-MTA-09]'s content-size condition

Checked:
- §18.2 (line 2473f): "it MAY be present, and when present it MUST equal the byte
  length of the decoded document. A mismatch is a failure to decode within the
  meaning of R3".
- R3 as written (line 3539): condition "A user-metadata document's stored bytes
  fail to decode under its declared assigned encoding — ..."; Instances "top-level
  extent; layer sub-record extent"; Governing rule `[R-CNT-25]` **with no
  parenthetical**. R1 by contrast reads "`[R-CNT-25]` (R-MTA-03, R-EXT-03)" and
  R4 reads "`[R-MTA-09]` (R-COD-06, R-CNT-25)". So R3 alone omits [R-MTA-09] from
  a row whose condition [R-MTA-09] now partly supplies. Real, and against the
  document's own citation convention.
- R4's own text self-excludes: "unlike R3, the constraint is broken whether or
  not the bytes decode". A content-size mismatch is established only after
  decoding. So diagrams-02's R3/R4 fork is decided by R4's own clause plus
  §18.2's express routing — REFUTED as a fork, though it is a symptom of the same
  omission.
- §21.1 instance axes (line 3335f): "Where the condition compares two
  **magnitudes** either of which can be the greater — a *differs from* or *does
  not equal* — the two directions are likewise enumerated". T22 (line 3508) is the
  tile transposition and enumerates six (three layouts x two directions).

Skeptical counter I looked for and partly found: §18.2 *stipulates* the mismatch
"is a failure to decode within the meaning of R3", which is an argument that R3's
Condition cell already reaches it as a term of art and that the family therefore
does not change shape (T24's "any codec" pattern). That defends the Condition
cell but not the Instances cell: a corpus builder satisfying R3's two instances
can do so with two corrupt-zstd files and owe nothing for the content-size
comparison, so the newest MUST in the document has no vector behind it. That is
the durable part of the finding and it survives.

Byte-level? No, and the deciding sentences are:
- [R-MTA-09]: "when present it **MUST** equal the byte length of the decoded
  document" — a capitalised MUST binding the file, so the emittable set does not
  move under any reading of R3.
- §21.8 [R-ERR-02]: "A row without a vector is a gap in the corpus, **not a
  licence to skip the check**."
- §2.3: a verifier "checks every file-level requirement".
There is no permitted reading on which the check is not owed. CONFIRMED,
register-bookkeeping.

Arithmetic note: two reporters independently hand-counted 121 conditions / 273
instances against §21.8's stated figure and agree the cells as written are
arithmetically right. I did not re-count. Adding the directions moves the total,
so §21.8's figure must move with any repair.

## Singletons

**verifier-02 (file-scope partial slack).** §5.2's trigger is extensional:
"Where the walk of §9.7 **does not enumerate every region's claimants**", and its
consequent is "a verifier reporting one MUST say which scope or violation
**stopped the walk**". §9.7 is causal too: "Where the walk does not complete — a
scope-level rejection **blocks** enumeration, or the verifier stops at the first
violation". Reading 1 (stipulative at file scope) also has a reductio the
reporter did not run: §5.2 says a rejected scope's already-enumerated claimants
"are discarded with the layer", so applying it at file scope discards every
claimant and yields a partial total of F. Reading 2 is what the text supports.
CONFIRMED as a gap nonetheless — file scope is stipulated neither way where §9.7
stipulates tile scope expressly ("An entry [R-IDX-03] classifies reject-tile on a
*structural* ground does not make the walk incomplete"). Not byte-level: both
readings report *nonconforming*; only one report line moves. Editorial.

**diagrams-01 (§21.6 cites [R-WRT-08] for preserve-or-drop).** The reporter's
load-bearing premise is that [R-WRT-08] is only its final sentence and that
§20.4's obligation table carries no identifier. The document never states where a
requirement's identifier sits relative to its text, and it does use end-of-block
markers spanning several paragraphs (§5.2's [R-CNT-21] block runs from "Every
byte the live state does not claim is slack" to "Only compaction reclaims it.")
and does attach tables across markers by forward reference (§21.9: "The table
below states **minimum guarantees** ... `[R-ERR-03]`", with the table after the
marker). Under the end-marker convention the table falls inside [R-WRT-08] and
§21.6's citation is correct. Against that: every *other* reference to the table's
content in this document cites it by section, never by identifier — §2.3 line
187 "the preservation obligations of §20.4", §2.4 line 241 "§20.4's table states
the cases", §20.5 line 3180 "only where §20.4's table licenses", §25 lines
4363-4367. So there is a real traceability wrinkle even if the citation is
defensible. PARTIAL, editorial, not byte-level: updater-side, §21.7 records the
obligations as unwitnessed in a single file, and no reader byte turns on it.

**diagrams-03 (§5.1's "alone").** Verified both halves. §20.3 shape (c): "Editing
user metadata is not this shape: its document lives in an extent (`[R-CNT-25]`),
so a new extent is appended and the old one becomes slack, as in (b)." §5.1's
Example: "so a commit that touches no layer re-emits the directory, the pad and
the trailer alone." A file-scope metadata edit touches no layer and appends an
extent, so "alone" overreaches. Example text, non-normative under [R-CNF-01]
("All text in this document is normative except: §1; any text labeled *Note*,
*Example*, or *Rationale*"). CONFIRMED, figure, not byte-level.

**diagrams-04 (§4.7's Note).** The Note lists six columns — "byte offset within
the structure, size, type, name, taxonomy class, and valid range" — then says of
§7.4's table "its table omits the offset and class columns". §7.4's table has
three columns: Field | Type | Constraint. Omitted: offset, size, class — three,
not two. Verified the six-column baseline at §18.2's encoding-byte table
(Offset|Size|Type|Field|Class|Valid values). Skeptical counter I weighed and
rejected: the Note accounts for other merges explicitly ("a Value column replaces
type and range", "§7.2 folds each field's range into its Field cell"), so its
silence about size here is an omission and not an implied merge. Non-normative
Note; widths are fixed by the Type column and [R-ENC-06]. CONFIRMED, editorial,
not byte-level.

**register-03 (§21.1's "obliges").** [R-MTA-05] (line 2552): "...the file is
nonconforming, a verifier MUST report it, and readers process the document
unchanged" — the operative clause carries no BCP 14 keyword, and §2.1 binds the
keywords "when, and only when, they appear in all capitals". [R-CNF-12]: "For a
nonconforming file no acceptance obligation exists — a reader **MAY** reject it
upon detecting any violation, **including violations whose assigned detector is
the verifier**." That is the sentence that decides it, and it names exactly these
rows. §21.1's own tie-breaker ("where a row and the rule it cites diverge, the
rule governs") cuts the same way, and §21.6's closing paragraph puts it in the
right words: "neither is a reason for a reader to reject anything" — grounds, not
permission. So §21.1's "obliges" is a loose gloss, not a withdrawal of the MAY.
CONFIRMED as a wording defect; not byte-level, because under both readings the
file is nonconforming with F27/L48 as its rows and only a MAY's availability
moves. Editorial. Repair is the reporter's own: "obliges the reader **that serves
the structure** to serve it unchanged".

**register-04 (L23's Detected cell).** The refutation I found and the reporter did
not: §19.1 step 4 uses an explicit timing phrase for the duplicate-name case —
"A duplicate layer name is a validity error at file scope, **here, at open**
(`[R-ENC-15]`, §19.2)" — and pointedly omits it two sentences later for the
overrun case, which reads only "is instead a validity error at layer scope
(`[R-CNT-18]`)": scope, not tier. The drafter distinguished the two. Add §19.2's
"A reader MAY detect any violation earlier" and the Detected column's definition
as "the point by which detection is due" (the *latest*, per [R-RDR-02]'s
Rationale: "The rule fixes the *latest* detection point"), and L23's cell is
defensible as written. One reporter claim is simply wrong: [R-VEC-02]'s manifest
records "the outcome class (§2.4), the scope, and the §21 register row ...
together with that row's governing requirement identifier" — no detection point,
so no harness expectation turns on it. PARTIAL; the tension with §19.2's at-open
namespace item is real enough to be worth a maintainer decision, but the row is
not shown wrong. Register-bookkeeping, not byte-level: the outcome is reject-layer
under both readings and no file's served bytes move.

**register-05 (§21.7's "only where ... *and* ...").** Parse (ii) is decided inside
the same sentence: the necessary condition "the affected tiles remain stored" is
independently restated at the end of the same list — "a commit that supersedes
every tile it would have damaged leaves the live state clean, so the bar is
unwitnessed there" — which only makes sense if "remain stored" is necessary for
*every* route, not just the first. So the "instead" clauses are alternative
routes, not contradictions. PARTIAL; the scoping is genuinely awkward on first
read and the fix is to make the list a list. Not byte-level: §21.7 "imposes no
check and withdraws none" — every row it names is obligatory under its own
governing rule either way. Editorial.

**quiz-02 ("the bound above").** Decided in three places. §18.2 itself: the window
bound "takes the same treatment" as the size bound, and the following sentence
generalises in the singular ("the bound is that verifier's capability and not a
limit on validity"). §21.5's preamble: "except where a reader **or verifier**
declines the decode **on the size bound or on the frame's declared window**, which
`[R-MTA-09]` makes that actor's capability and not a fact about the file". §2.3
lists the [R-MTA-09] decline unqualified. PARTIAL — the singular noun is loose
but nothing is left undetermined. Editorial, not byte-level; the verdict is
*cannot establish* under either reading.

## Coverage

20 input ids. 10 groups. Membership counted twice by hand:
G1 6 + G2 6 + 8 singletons = 20. No id appears twice; none dropped.
byte-level survivors: 0.

## Where I would put the maintainer's attention

1. G1 — one word, and six of six readers stopped on it. Make the edit even though
   I grade it editorial; my grade is a claim about what the sentence decides, not
   a claim that the sentence reads well.
2. G2 — R3's three cells, plus §21.8's totals.
3. verifier-02 — one sentence for file scope, mirroring §9.7's tile-scope carve-out.
