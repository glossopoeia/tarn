# Round 22 triage — implementer-consequence lens

## Access disclosure

Read only `spec/tarn.md` (targeted `sed`/`grep` over §2.1–2.5, §3.1, §4.7,
§5.1, §5.2, §7.2–7.4, §9.7, §11.2–11.4, §17.2 ([R-COD-06], [R-COD-07] and
their Notes), §18.1–18.2, §19.1–19.4, §20.3 step 4 and its three-shapes
Example, §20.4, §21.1–21.9, §22.2–22.3, §24, Appendix B row for the
guarantees). Ran one mechanical count over the register tables
(§21.2–§21.5) to check the 121/273 claim two reporters made.

Read **no** walk transcript, **no** `transcript-triage-*.md`, no `docs/`,
no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`,
no git history, no web. I listed the round22 directory once with
`| grep -v triage` so no triage filename was displayed; the walk-file
names came back and nothing else. Every finding was evaluated.

## Register count check (my own, mechanical)

Parsed every `| F<n> | / | L<n> | / | T<n> | / | R<n> |` row in
§21.2–§21.5, splitting the Instances cell on `;` (a lone `—` = 1):

    conditions 121  instances 273
    F 36 / 58 · L 49 / 116 · T 26 / 55 · R 10 / 44

Matches §21.8 exactly. So the reporters who said "the cells as written
total 273" are right, and any under-enumeration is a real shortfall
rather than an arithmetic slip. Adding the content-size condition's
2 directions × 2 containers takes it to 277.

## Grouping

Twenty ids, ten groups.

- **G1 tile-row-quantifier** — reader-01, writer-01, verifier-01,
  register-02, adversary-01, quiz-01. All six quote the same §21.9
  sentence and pose the same addressed-vs-stored question.
- **G2 r3-cells-vs-[R-MTA-09]** — reader-02, verifier-03, diagrams-02,
  register-01, adversary-02, quiz-03. All six are facets of one edit that
  did not propagate: §18.2 routed a new condition into R3 and R3's
  condition / governing-rule / instances cells were not revised.
  Splitting "traceability" from "instance count" is impossible without
  breaking the one-id-one-group rule, since register-01 and adversary-02
  each raise both; so one group, with the full repair stated.
  diagrams-02's extra claim (that R4 also claims the condition) is
  answered inside the group: §18.2 names R3 expressly and R4's own
  "unlike R3, the constraint is broken whether or not the bytes decode"
  self-excludes a comparison against a decoded length.
- G3..G10 are singletons: verifier-02, diagrams-01, diagrams-03,
  diagrams-04, register-03, register-04, register-05, quiz-02.

## G1 — the one I uphold as byte-level

Text (§21.9, [R-ERR-03]):

> The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually
> contains, and a file containing none of a kind does not exceed that
> row, whatever its declarations would derive — a layer addressing no
> tile (§11.2) has no tile whose decoded size the table can bound,
> exactly as `[R-COD-07]`'s cap is quantified over a layer's *addressed*
> tiles. The first five range over declarations, which every file and
> every layer carries.

Verified independently of the reporters:

- §3.1 does define the pair of terms of art the operative clause avoids:
  "every tile of a layer is *addressed*. A tile is *stored in a
  generation* if and only if that generation's tile-index entry for it
  is not the sentinel". Neither word appears in the operative clause.
- §21.9's own table row 3 says "addressed tiles per layer (entry_count)",
  so the section knows and uses the word where it means it.
- [R-COD-07] at §17.2 is indeed over addressed tiles, and its Note says
  the escape "is not durable".
- §20.3 step 4 leans on that quantifier explicitly.
- The witness files the reporters built are conforming: §11.3's Note says
  "Tile extents are a writer's choice, and this specification imposes
  none ... Tiles far outside that range remain conforming"; [R-CNT-17]'s
  entry_count/extent_length cross-check is satisfied at N = 1; [R-ENC-04]
  is satisfied. I checked each of these rather than taking them.
- [R-CNF-03] conditions its acceptance duty on "none of whose values
  exceeds the minimum guarantees of §21's limits table", and [R-ERR-04]
  closes with "Software that declines **on that ground** a file whose
  every quantity lies within the table is not a conforming reader".

**The premise my upholding rests on**, stated so it can be attacked: that
the trailing "exactly as [R-COD-07]'s cap is quantified over a layer's
*addressed* tiles" is an analogy hung on the vacuous example, not a
definition of the operative verb. Test: the gloss it modifies is "a layer
addressing no tile has no tile whose decoded size the table can bound" —
a case that is **true under both readings**, since a layer addressing no
tile stores none. An analogy attached to a case that does not discriminate
does not discriminate. Against my premise: "exactly as ... is quantified"
is, read strictly, a statement about quantification and not about the
example. I concede that is available; I do not think it is compelled, and
the operative clause says the opposite in the words an implementer will
remember. Pulling the same way as the operative clause: the very next
sentence ("The first five range over declarations") draws a per-instance /
per-declaration contrast that collapses for this row under the addressed
reading, because both the addressed set and the decoded size are functions
of declarations alone.

Implementer consequence — two designs, both defensible from this text,
diverging on identified bytes:

- **X, declaration-bounded.** §19.3 already obliges layer access to check
  "the 2⁶³ − 1 ceiling on every quantity that arithmetic derives
  ([R-ENC-04]) and on the decoded sizes §14 derives from it ([R-SER-02],
  [R-SER-07])", so X has the decoded tile size in hand at layer access
  with no I/O. It compares against its own ceiling and declines the layer
  with a resource-limit diagnostic.
- **Y, storage-bounded.** Y applies its ceiling at §19.4 step 6. §19.4
  step 4 short-circuits a sentinel entry "with no payload I/O", so Y
  serves fill at every coordinate of that layer.

Handed a conforming file whose sole layer declares a decoded tile size
above 256 MiB and whose every index entry is the sentinel (adversary-01's
256-byte file; verifier-01's 1 GiB float32 variant; quiz-01's 1,000-entry
variant — all conforming, checked above), X refuses and Y serves. Under
the addressed reading both are conforming readers. Under the stored
reading X "declines on that ground a file whose every quantity lies within
the table" and is by [R-ERR-04]'s own sentence not a conforming reader.
The set of files a conforming reader MUST accept differs between the
readings. That is the second half of the byte-level test, met on named
bytes. **Byte-level: yes.**

Which way should the repair go — an implementer argument the reporters
did not make. Under the stored reading, whether a file is within the
guarantees is not decidable at layer access at all: §19.3 says "layer
access performs no fetch", and deciding "does this layer store any tile?"
requires walking up to 2³² index entries. The acceptance boundary would
become I/O-dependent and would move from open/layer access to tile use.
[R-COD-07], §17.2's Note and §20.3 step 4 have all already committed the
document to declaration-time bounding. So I recommend pinning the row to
*addressed*, in the row's own words, and giving the other two rows their
own phrase — they can only mean physical presence. This is a maintainer
decision, not a free edit: the alternative (stored) is the reading that
never refuses a file containing no data, and [R-SEC-02] ("A reader MUST
NOT size an allocation, fetch, or index walk in proportion to a declared
magnitude it has not corroborated") is the reason someone will argue for
it. Either way the fix is one clause; leaving the analogy to carry it is
what must stop.

## G2 — real, and not byte-level

What decides the reader's behaviour, quoted (§18.2, [R-MTA-09]):

> it MAY be present, and when present it MUST equal the byte length of
> the decoded document. A mismatch is a failure to decode within the
> meaning of R3

A capitalised MUST binding the file, plus a stated outcome (R3 →
ignore-record, detector reader, extent use). No two implementations that
read §18.2 can differ on the verdict or on any emitted byte. The register
tie-break §21.1 offers — "where a row and the rule it cites diverge, the
rule governs" — does **not** literally reach here, because R3 does not
cite [R-MTA-09] at all; but nothing turns on that, since §18.2's own
sentence is unconditional and §2.3 obliges a verifier to check "every
file-level requirement" rather than only the register.

So the defect is bookkeeping — and it is the expensive kind, because the
corpus is the artifact implementers actually run. [R-ERR-02]: "one vector
per instance"; R3's cell is "top-level extent; layer sub-record extent".
As written the corpus owes no vector in which a content-size mismatch is
the condition under test. adversary-02's trap is real and I would repeat
it: a reader that decodes with a whole-buffer zstd API which does not
itself validate Frame_Content_Size returns the document where [R-MTA-09]
requires ignore-record, and passes the whole corpus. The tile-side twin of
that trap gets six vectors through T22.

Repair: (a) R3's condition cell names the content-size mismatch expressly
rather than leaving §18.2 to legislate it in from outside; (b) R3's
governing-rule cell cites [R-MTA-09] (R4's already does); (c) R3's
instances cell gains 2 directions × 2 containers = 4 instances, by §21.1's
own magnitude axis and on T22's precedent; (d) §21.8's total moves 273 →
277 and [R-ERR-02]'s figure with it. A separate row (an "R11") instead of
loading R3 is equally serviceable and would keep R3's condition text
clean; that is a maintainer's call.

## G3 — verifier-02, file-scope rejection and the partial total

Both governing sentences gate on the walk not completing:

- §5.2: "Where the walk of §9.7 **does not enumerate every region's
  claimants** — whether because a scope-level rejection ends that scope's
  enumeration ... or because the verifier elected under [R-CNF-11] to stop
  at the first violation — the verifier MUST report the total as partial."
- §9.7: "Where the walk **does not complete** — a scope-level rejection
  blocks enumeration, or the verifier stops at the first violation".

F27 (unsorted metadata, verifier, certification) enumerates every
claimant. The trigger is not met, so the total is exact. §5.2's follow-on
— "a verifier reporting one MUST say which scope or violation stopped the
walk" — has nothing to name under the other reading, which is the tell.
The reporter's reading 1 exists only by analogy from the *layer*
parenthetical, which is stipulative for layers. So: PARTIAL — the
underdetermination is milder than reported, but the layer parenthetical
does invite the analogy and file scope is stipulated neither way.
Consequence is one report line (exact total vs upper bound), no byte, no
verdict; §22.3 makes the line operationally load-bearing, which is why a
one-sentence carve-out for file scope, matching §9.7's tile-scope one, is
worth writing. Editorial.

## G4 — diagrams-01

Checked both cited rules. [R-CNT-15] ends "Updater obligations for unknown
records are §20's subject" — it supplies "ignored" and expressly defers
the rest. [R-WRT-08] in full is a re-encoding prohibition plus a
relocation permission; no PE, no preservation, no dropping. The rule that
states preserve-or-drop is §20.4's three-row table, and the table carries
no `[R-...]` identifier despite holding four MUST/MAY/SHOULD-level
obligations, against §2.2's "Normative requirements carry identifiers".
Real, and worth an identifier.

Why nothing happens to an implementer: [R-CNF-06] anchors the table by
section — an updater "MUST honor the preservation obligations of §20.4 —
which govern every record type, not only those it does not implement" —
and the §21.6 pointer lands two lines above the table anyway. Editorial;
the cost is to review and to §21.1's own divergence rule, which cannot be
applied to an entry whose cited rule does not contain the claim.

## G5 — diagrams-03

§5.1: "so a commit that touches no layer re-emits the directory, the pad
and the trailer alone." §20.3 shape (c): "Editing user metadata is not
this shape: its document lives in an extent ([R-CNT-25]), so a new extent
is appended and the old one becomes slack, as in (b)." §7.2 admits exactly
two top-level record types, so "touches no layer" does not entail
"appends nothing but dir/pad/trailer". The clause overreaches; the figure
itself is right. Both texts are Example, non-normative under [R-CNF-01],
and a writer that believed it cannot emit the file it imagines, since
[R-LIF-01] freezes the prior extent. Figure-level.

## G6 — diagrams-04

§7.4's table is `Field | Type | Constraint` — three columns. §4.7's Note
baseline is six (offset, size, type, name, class, valid range), so §7.4
omits offset, **size**, and class; the Note names two. Verified the
baseline against §6.1, §6.2, §7.2, §15.1, §18.2 — the Note accounts for
each of those explicitly, which is what makes the one incomplete
enumeration stand out. Nothing follows for an implementer: widths come
from the Type column, [R-ENC-06], and §7.4's worked example, and a Note is
non-normative under [R-CNF-01]. Editorial.

## G7 — register-03

The deciding text is capitalised and directly on point, [R-CNF-12]: "For
a nonconforming file no acceptance obligation exists — a reader MAY reject
it upon detecting any violation, **including violations whose assigned
detector is the verifier**." [R-VEC-04] repeats the point in the corpus's
own terms: "[R-CNF-12] permits the latter for any nonconforming file and
every vector built from §21's register is nonconforming." §21.1's sentence
is a gloss reporting what two other rules say, in a section that disclaims
governing ("where a row and the rule it cites diverge, the rule governs"),
and neither cited rule states a serve-obligation: [R-MTA-05]'s "readers
process the document unchanged" carries no capital, and §2.1 binds the
keywords "when, and only when, they appear in all capitals". So "obliges"
overstates and the repair is the reporter's own: "obliges the reader that
serves the structure to serve it unchanged". §21.6's closing already says
it correctly — "neither is a reason for a reader to reject anything".
Nothing an implementer builds changes: rejecting stays licensed, serving
stays licensed. Editorial.

## G8 — register-04

Refuted by the column's own definition. §21.1: the Detected column is "the
point by which detection is **due** (§19.2)" — a deadline. §19.2: "A
reader MAY detect any violation earlier ([R-CNF-12])", and its rationale
says the rule "fixes the *latest* detection point". §19.1 step 4 does
oblige the containment test at open — that part of the report is accurate
— but performing a test at open and having the violation *due* by layer
access are consistent, and a vector's recorded expectation must tolerate
earlier detection regardless. L23's single "layer access" is correct as
written; no split is owed and no corpus expectation moves. Severity none.

## G9 — register-05

The sentence is genuinely awkward: read with "only" governing the whole
conjunction, the two clauses that follow it contradict it inside the same
semicolon run. Parse (ii) — necessary condition, then three parallel
sufficient routes — is the one the parallel form supports and the only one
that is not self-refuting. Nothing turns on it: §21.7 is an account of
what no check detects and creates no check; T3, T14, T15, T17, T23 and T25
are all registered §21.4 rows with reader detectors and their own
governing rules, obligatory under either parse. A verifier author who took
parse (i) loses an afternoon, not a check. Editorial; make the list a
list.

## G10 — quiz-02

Decided outside §18.2, twice. §21.5's preamble: "except where a reader or
**verifier** declines the decode on **the size bound or on the frame's
declared window**, which [R-MTA-09] makes that actor's capability and not
a fact about the file." §2.3 lists the [R-MTA-09] decline among
cannot-establish grounds without qualifying the bound. Within §18.2 the
window sentence itself says the window "takes the same treatment". So the
singular "the bound above" is imprecise, not ambiguous: a verifier that
declines on either bound owes *cannot establish* and MUST NOT certify.
Reading cost only. Editorial; pluralise, or write "either bound above".

## Byte-level tally

1 of 20 — G1. Five reporters flagged it; the sixth picked the same reading
and wrote that striking the [R-COD-07] clause would make it byte-level.
I did not count flags: I upheld it because the operative clause and the
gloss point opposite ways, the gloss's example is true under both
readings, and the two reader designs the text licenses give opposite
answers on identified bytes.
