# Round 22 triage — correctness lens — working transcript

## Access log

Read only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, by section:
§2.1, §2.2, §2.3, §2.4, §2.5, §3.1, §4.7, §5.1, §5.2, §6.1, §7.2, §7.3, §7.4,
§9.7, §11.1, §11.2, §11.3, §17.2 (codec 4 + Note), §18.2, §19.1, §19.2, §19.3,
§20.3 (three-shapes Example), §20.4, §21.1, §21.3 (L3/L5/L6/L18/L23/L44/L48),
§21.4, §21.5, §21.6, §21.7, §21.8, §21.9, §22.2, §24.
Ran `grep` for: R-COD-07, "actually contains", "user metadata", section headers.
Did **not** open any walk transcript, and did **not** open or list any
`transcript-triage-*.md`. Did not read docs/, PLAN.md, AGENTS.md, conformance/,
registry.json, git history, or the web.

## Grouping

20 ids → 10 groups.

- G1 per-instance tile quantifier (§21.9): reader-01, writer-01, verifier-01,
  register-02, adversary-01, quiz-01.  All six quote the same sentence and
  describe the same fork (addressed vs stored). register-02 alone downgrades.
- G2 R3 does not carry [R-MTA-09]'s content-size condition: reader-02,
  verifier-03, diagrams-02, register-01, adversary-02, quiz-03.  One root
  cause — R3's row was not revised when §18.2 gained the content-size MUST —
  presented as (a) instances/vector coverage (reader-02, verifier-03, quiz-03),
  (b) condition text + governing-rule cite + instances (register-01,
  adversary-02), (c) R3-vs-R4 routing (diagrams-02).  Same edit repairs all.
- G3 verifier-02, G4 diagrams-01, G5 diagrams-03, G6 diagrams-04,
  G7 register-03, G8 register-04, G9 register-05, G10 quiz-02 — singletons.

6+6+1×8 = 20. Each id in exactly one group.

## G1 — §21.9 per-instance rows: addressed or stored?  UPHELD, byte-level

Operative text (verified verbatim at spec lines 3686-3693):

> The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains, and a
> file containing none of a kind does not exceed that row, whatever its
> declarations would derive — a layer addressing no tile (§11.2) has no tile
> whose decoded size the table can bound, exactly as `[R-COD-07]`'s cap is
> quantified over a layer's *addressed* tiles. The first five range over
> declarations, which every file and every layer carries.

Checks performed:

1. `grep "actually contains"` → one hit, this sentence. §3.1 defines
   *addressed tile / stored tile*; it defines no "contains". So the operative
   phrase is not a defined term, as adversary-01 says. TRUE.
2. [R-COD-07] quantifier verified: §17.2 "Writers MUST NOT declare this codec
   for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000";
   its Note "The cap is quantified over the layer's *addressed* tiles"; L44
   "any of whose addressed tiles'". §20.3 step 4 "which an empty layer escapes
   only because that cap is quantified over addressed tiles". So the analogy's
   factual content is accurate. TRUE.
3. [R-CNF-03] verified: "MUST accept every conforming file ... and none of
   whose values exceeds the minimum guarantees of §21's limits table".
   [R-ERR-04] verified: "a reader MAY decline it — at the whole file, or at the
   narrowest scope whose declarations exceed what it can serve ... Software that
   declines **on that ground** a file whose every quantity lies within the table
   is not a conforming reader (`[R-CNF-03]`)". So the fork really does decide
   which of two readers is conforming on one identified byte sequence. TRUE.
4. Witness files check out. §11.1: "A tile extent MAY exceed its dimension's
   extent (where 0 < Eᵢ < Tᵢ the grid is then a single padded tile along that
   axis)". So adversary-01's tile extent 2^30 over extent 1 (G=1, N=1,
   P=2^30, Q=1, decoded size 1024 MiB, single sentinel entry) is a conforming
   file, and so are quiz-01's 512 MiB and verifier-01's 1 GiB variants. The
   fork does not depend on the extreme 2^63−1 examples reader-01 and writer-01
   chose.
5. [R-VEC-03] checked as a possible tie-breaker: "§21.9's minimum guarantees
   are exercised where a vector at the bound is constructible — the tile-count
   guarantee is not". Neutral: a 256 MiB tile of constant data compresses to
   nothing, so a stored-tile vector is constructible too. writer-01's reading
   of it is right.

Arguments I tested and rejected:

- writer-01's "under Reading A the tile row is itself declaration-derived, so
  the paragraph's contrast collapses". Wrong: the contrast the next sentence
  draws is presence, not derivation — "The first five range over declarations,
  **which every file and every layer carries**". Under A the row is still
  per-instance because a file may address no tile at all. Noted as a weak leg,
  not as a reason to downgrade the group.
- register-02's downgrade, which is the only downgrade in the group. Its
  premise: the trailing clause "exactly as `[R-COD-07]`'s cap is quantified
  over a layer's *addressed* tiles" is a discriminator that makes the stored
  reading "a reading a hurried implementer reaches rather than one the text
  licenses". I state the premise so it can be attacked, and then attack it:
  (a) the clause's grammatical subject is [R-COD-07]'s cap, not this row —
      it asserts a fact about a different rule and compares;
  (b) the proposition it glosses is the *vacuous* case, "a layer addressing no
      tile", which is true under both readings, so the gloss discriminates
      nothing on its own;
  (c) the document has a house style for pinning this quantifier and does not
      use it here: L44 and §17.2's Note and §20.3 step 4 all put the word
      **addressed** in the operative position. §21.9 puts a phrase it nowhere
      defines, "a file actually contains", in the operative position and puts
      "addressed" only inside an analogy about another rule;
  (d) one phrase governs three rows and can only mean physical presence for two
      of them (a document and a frame exist only as stored bytes), so reading A
      requires the same four words to be read non-uniformly across the three
      rows with nothing saying so;
  (e) "whatever its declarations would derive" is set in opposition to
      "actually contains"; under A both sides of that opposition are
      declaration-derived facts (addressedness is ⌈Eᵢ/Tᵢ⌉ > 0), which blunts it.
  I therefore do not accept the downgrade. I still think A is the better-
  supported reading and the one to legislate; that is a repair, not a finding
  that the text already says it.

Byte-level: yes, on [R-ERR-04]'s own closing sentence. Under A the eager reader
declining a ~256-byte all-sentinel file with a 1 GiB declared decoded tile size
is exercising a MAY; under B that same reader "declines on that ground a file
whose every quantity lies within the table" and is not a conforming reader,
while the file is one [R-CNF-03] obliges it to accept and serve as fill
([R-TYP-08], §21.6's sentinel row). Same bytes, opposite verdicts, and the two
implementations disagree about each other's conformance.

Repair: give the tile row its own quantifier in the operative clause — "the
tiles a layer **addresses**" — and give the other two rows their own phrase
("the user-metadata documents and compressed frames the file **stores**"). A is
the coherent choice: [R-ERR-04] measures a decline against *declarations*, §22.2
makes decoded tile size "a function of the layer's declarations alone", and
[R-COD-07] is already quantified that way. If B is intended instead, the
[R-COD-07] analogy must go, because it would then be false.

## G2 — R3 and [R-MTA-09]'s content-size condition.  UPHELD, register-bookkeeping

Verified verbatim:
- §18.2: "it MAY be present, and when present it MUST equal the byte length of
  the decoded document. A mismatch is a failure to decode within the meaning of
  R3".
- R3 row: Condition "A user-metadata document's stored bytes fail to decode
  under its declared assigned encoding — ..."; Instances "top-level extent;
  layer sub-record extent"; Governing rule "`[R-CNT-25]`" alone.
- R4 row: "...unlike R3, the constraint is broken whether or not the bytes
  decode"; 12 instances, six constraint kinds × two containers, none of them
  content size; Governing rule "`[R-MTA-09]` (R-COD-06, R-CNT-25)".
- T22: six instances, "declared larger; declared smaller" × three layouts.
- §21.1: "Where the condition compares two **magnitudes** either of which can be
  the greater — a *differs from* or *does not equal* — the two directions are
  likewise enumerated"; and "where a row and the rule it cites diverge, **the
  rule governs**".
- §21.8: "121 conditions over 273 instances ... one vector per instance".

So every factual leg the six reporters stand on is accurate. R3 carries the
condition by stipulation and restates none of it: not in its condition text, not
in its governing-rule cell, not in its instances.

diagrams-02's extra claim — that R4 also claims the condition — is half right
and I record it as such: R4's first clause ("breaks one of the frame constraints
§18.2 states") does reach a content-size mismatch on its face, but R4's own
discriminator ("unlike R3, the constraint is broken whether or not the bytes
decode") excludes it, since the comparison needs the decoded length, and §18.2
names R3 expressly. verifier-03's check of this is the correct one. So the
group is not an R3/R4 fork; it is R3 under-restating its rule.

Byte-level: no, and no reporter claimed otherwise. The deciding text is §21.1's
"where a row and the rule it cites diverge, **the rule governs**" together with
§18.2's capitalised MUST. Both are already in the document, so no writer may
emit the mismatch and every reader takes ignore-record whichever way the cell
reads. What moves is only the corpus's instance list — and §21.8 already says
"A row without a vector is a gap in the corpus, not a licence to skip the
check", i.e. the missing vector changes no implementation's obligations.

Repair: extend R3's condition cell to name the content-size case; add
`[R-MTA-09]` to its governing-rule cell (R4 already cites it); enumerate the
instances on §21.1's magnitude axis — declared larger / declared smaller × two
containers, so 2 → 6 for the row and 273 → 277 in §21.8. Whether the drafter
prefers a separate row (the T22 shape) instead is a maintainer's choice; the
arithmetic in §21.8 must move either way.

## G3 — verifier-02, file-scope rejection and the partial slack total.  UPHELD, design-decision

§5.2 verbatim: "Where the walk of §9.7 does not enumerate every region's
claimants — whether because a scope-level rejection ends that scope's
enumeration (a rejected layer's claimants are not enumerated, whether or not the
rejection impeded reading them — and where the rejection is one the walk itself
established ... the claimants it had already enumerated are discarded with the
layer ...), or because the verifier elected under `[R-CNF-11]` to stop at the
first violation — the verifier MUST report the total as partial."

§9.7 verbatim: "Where the walk does not complete — a scope-level rejection
blocks enumeration, or the verifier stops at the first violation — the sum is
reported as partial"; and, for tiles, "An entry `[R-IDX-03]` classifies
reject-tile on a *structural* ground does not make the walk incomplete".

The reporter is right that the layer case is stipulated ("whether or not the
rejection impeded reading them"), the tile case is carved out expressly, and the
file case is stipulated neither way. "a scope-level rejection ends **that
scope's** enumeration" applied to file scope reads as ending the whole
enumeration; §5.2's gate sentence, read causally, does not, because the walk did
enumerate every claimant. Both parses are on the words. Rows F25/F26/F27/F28/
F33/F36 are verifier-detected at certification and impede nothing.

One correction to the reporter: it says §5.2's follow-on obligation is
undischargeable under reading 1. Not quite — "a verifier reporting one MUST say
which scope or violation stopped the walk" can be discharged by naming the
violation. Also, taken strictly, reading 1 plus §5.2's "discarded with the
layer" logic would discard *every* claimant for a file-scope rejection, making
the partial total F, which is worse than the reporter's "≤ 1341". That
strengthens rather than weakens the case for stipulating the file case.

Byte-level: no. Deciding text: §5.2's own Note — "A partial total (`[R-CNT-21]`)
reports what one verifier's incomplete walk left unclaimed, which is a fact
about that run and not about the file's live state" — and the verdict is
*nonconforming* under both parses since the file-scope violation is established
either way. It is a MUST-level report divergence, which is why I grade it
design-decision rather than editorial: the maintainer has to choose.

Repair: say for file scope what §9.7 says for tile scope. Recommended wording:
a file-scope violation the walk did not need to stop for does not make the walk
incomplete; only a rejection that blocks enumeration, or an elected stop, does.

## G4 — diagrams-01, §21.6's `[R-WRT-08]` citation.  UPHELD, register-bookkeeping

[R-WRT-08] verbatim, in full: "An updater MUST NOT re-encode a record whose type
it does not implement, and MUST NOT modify one except by relocating its extent
and re-pointing its slot under §20.5 — the operation the no-embedded-offsets
rule (§7.2) makes safe for MU = 0 records." Nothing about PE, preservation, or
dropping. Confirmed.

[R-CNT-15] verbatim ends: "Updater obligations for unknown records are §20's
subject." So it supplies "Ignored" and expressly defers the rest. Confirmed.

§20.4's flag table carries the actual rule — "MU = 0, PE = 1 | Retain
byte-identical, extent content unmodified" and "MU = 0, PE = 0 | Retain
byte-identical, or drop it — its extent becoming slack" — and I confirmed by
reading §20.4 top to bottom that no `[R-...]` identifier attaches to it: the
identifiers in §20.4 are [R-WRT-05] before it and [R-WRT-08] after it, and
neither sentence states the table's content. §2.2: "Normative requirements carry
identifiers of the form `[R-<PREFIX>-<NN>]`." §2.4 points *at* the table as the
source ("§20.4's table states the cases"), so it is not a restatement inheriting
another identifier. The reporter's two rejected innocent readings are the right
two, and both are correctly rejected.

Byte-level: no. §21.7 records the updater obligations as having no single-file
witness, and following the wrong pointer still lands the reader in §20.4 two
lines from the table. Deciding text for the downgrade-equivalent: §20.4's table
cells are themselves unambiguous ("Retain byte-identical, or drop it — its
extent becoming slack"), so no implementation's output turns on which identifier
§21.6 names.

Repair: give §20.4's flag table its own identifier (a new [R-WRT-nn]) and cite
that from §21.6's row and from §2.4's preserve-verbatim entry.

## G5 — diagrams-03, §5.1's "alone".  UPHELD, figure

§5.1 caption verbatim: "a commit that touches no layer re-emits the directory,
the pad and the trailer alone." §20.3's three-shapes Example verbatim: "Editing
user metadata is not this shape: its document lives in an extent
(`[R-CNT-25]`), so a new extent is appended and the old one becomes slack, as in
(b)." §7.3 admits exactly two top-level types, layer and user metadata, so a
metadata-only commit touches no layer and appends an extent. The caption's "so"
clause is therefore false as a general claim. Confirmed.

Both passages are labeled **Example**, hence non-normative under [R-CNF-01]
("All text ... is normative except: §1; any text labeled *Note*, *Example*, or
*Rationale*"). Byte-level: no — that quotation is the deciding one, and
[R-LIF-01] freezes the prior extent so a writer misled by the caption cannot
emit the file it imagines.

Repair: "...re-emits the directory, the pad and the trailer alone — a commit
that edits user metadata appends that document's new extent besides (§20.3)."

## G6 — diagrams-04, §4.7's Note.  UPHELD, editorial

§4.7's Note baseline: "byte offset within the structure, size, type, name,
taxonomy class, and valid range". §7.4's table columns, counted in the file:
Field | Type | Constraint. Three of the six are absent: offset, size, class.
The Note names two, "its table omits the offset and class columns". Off by one,
confirmed. The reporter's accounting of the other tables is accurate: §6.1 is
Offset|Size|Value|Class (the Note's "a Value column replaces type and range"),
§7.2 is Offset|Size|Type|Field|Class with the range folded into Field (the
Note's own account), §6.2/§15.1/§18.2 carry the full six.

Byte-level: no. [R-CNF-01] makes a Note non-normative, and the widths are in
§7.4's own Type column ("u8", "u16", "u64", "u8 len + bytes") and §4.2.

Repair: "its table omits the offset, size and class columns" — or say that a
packed payload's widths come from the Type column.

## G7 — register-03, §21.1's "obliges".  UPHELD, editorial

[R-MTA-05] verbatim: "Readers MUST NOT depend on member order for meaning, and
unsorted members do not make a document unreadable: the file is nonconforming, a
verifier MUST report it, and readers process the document unchanged." The clause
§21.1 leans on carries no BCP 14 keyword, and §2.1 binds the keywords "when, and
only when, they appear in all capitals". [R-CNT-22] by contrast is a MUST. So
the reporter's first half is exactly true of the text.

The second half — that §21.1 collides with [R-CNF-12] — is true on a literal
reading and softer than the reporter frames it. [R-CNF-12]: "For a nonconforming
file no acceptance obligation exists — a reader MAY reject it upon detecting any
violation, including violations whose assigned detector is the verifier."
[R-CNF-04] already states both halves together: "a violation whose assigned
detector is the verifier imposes no reader obligation ..., though a reader
detecting one MAY reject the file (`[R-CNF-12]`)." So the harmonized reading is
available and stated, and no implementer is left without an answer.

Byte-level: no, and the reporter did not claim it. This one has the *shape* of
G1 — it forks which readers are conforming — so I checked it against the same
test rather than assuming. It fails the test because the document decides it
twice in capitals: [R-CNF-12]'s "a reader MAY reject it upon detecting any
violation" and [R-CNF-04]'s "though a reader detecting one MAY reject the file",
against §21.1's keyword-free "obliges", which §2.1 denies the force of a MUST.
G1 has no such capitalised decider anywhere.

Repair: "obliges the reader **that serves the structure** to serve it
unchanged", which is what both cited rules deliver and what §21.6's closing
paragraph already says in the right register ("neither is a reason for a reader
to reject anything" — a statement about grounds).

## G8 — register-04, L23's Detected cell.  REFUTED

The reporter's load-bearing claim is that "§19.1 step 4 places its name-field
instance at the open". It does not. §19.1 step 4 reads:

> A duplicate layer name is a validity error at file scope, **here, at open**
> (`[R-ENC-15]`, §19.2). The layer-name namespace is built from the name fields
> a reader can obtain under §7.4's framing: a layer record whose name field does
> not lie entirely within that record's inline_length yields no name field to
> compare, so it contributes no name to the namespace and is **instead a
> validity error at layer scope** (`[R-CNT-18]`).

The sentence that pins timing is the duplicate-name one, and it pins it
explicitly — "here, at open". The overrun sentence's "instead" contrasts with
that sentence's *scope* (file → layer) and pins no timing at all. The reporter
read a scope contrast as a timing placement.

§21.1 defines Detected as "the point by which detection is **due**" — a latest
bound — and §19.2 adds "A reader MAY detect any violation earlier". A reader
does perform the containment test at open (it must, to check L3/L5/L6 over the
name bytes and to decide uniqueness), but performing a test earlier than the
tier that requires it is exactly what §19.2 licenses, and the register cell
states a bound, not an event. Nothing at open is served on the strength of the
overrunning record: §19.1 excludes it from the namespace. So "layer access" is
correct as written and R1's split-cell convention is not owed here.

Byte-level: no, and the reporter conceded as much. Nothing to repair.

## G9 — register-05, §21.7's "witnessed only where ... and ...".  UPHELD, editorial

Verbatim: "§20.3 step 4's bar on a declaration change is witnessed only where
the affected tiles remain stored *and* the change reaches a byte §14
structurally constrains — a padding position, a pad bit, or a boolean byte —
where §21.4's content rows fire; a change that reaches the decoded size instead
is witnessed by T3 or T14 ...; a change that reaches the codec is witnessed by
the rows for the codec now declared ...". So the "only" is followed by two
further witnessing routes and is literally false as scoped. The reporter's parse
(ii) is clearly the intended one — "instead" marks an alternative route — and
its content check is right (T3/T14 for decoded size, T15/T17/T23/T25 or T14 for
codec). The defect is the scope of "only", not the substance.

Byte-level: no. [R-ERR-01] is an account of what no check detects; it imposes
and withdraws no check, and T3, T14, T15, T17, T23 and T25 are registered rows a
verifier runs under their own governing rules regardless of the parse.

Repair: state the necessary condition once, then enumerate the three routes as a
list.

## G10 — quiz-02, "the bound above".  UPHELD, editorial

§18.2 introduces two reader bounds in one paragraph — the decoded-size bound
("no smaller than §21.9's user-metadata guarantee") and the window bound ("a
reader's window bound is its own, no smaller than §21.9's guarantee for that
quantity") — and then writes "A **verifier** that declines to decode a document
on the bound above cannot establish that document's conformance and MUST NOT
certify the file". The singular is imprecise; both readings are open on that
sentence alone. Confirmed.

Byte-level: no. Two passages decide it, and I verified both verbatim.
§21.5's preamble: "except where a reader **or verifier** declines the decode
**on the size bound or on the frame's declared window**, which `[R-MTA-09]`
makes that actor's capability and not a fact about the file". §2.3: "or when it
declines to decode a user-metadata document (`[R-MTA-09]`)", unqualified. A
verifier that declined on the window bound therefore cannot certify under either
reading of §18.2's singular noun, so no verdict on any file moves.

Repair: "on either bound above", or name the two.

## Count

10 groups, 20 member ids, no id in two groups, none dropped.
Byte-level groups: 1 (G1). Reporter byte-level flags: 5 (reader-01, writer-01,
verifier-01, adversary-01, quiz-01), all in G1, all upheld. Downgrades: none.
One reporter-side non-flag (register-02, in G1) I decline to follow.
