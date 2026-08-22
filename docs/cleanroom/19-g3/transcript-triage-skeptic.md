# Round 19 triage — skeptic pass

## What I read

- `spec/tarn.md` in full for the sections at issue: §2.1–§2.5, §3.1–§3.3, §4.6,
  §5.1, §5.2, §6.1–§6.4, §7.1–§7.4, §9.7, §10.1–§10.3, §11.4, §12.2–§12.3,
  §14.1–§14.2, §17.2, §17.4, §18.2–§18.4, §20.1–§20.5, §21.1, §21.2 preamble,
  §21.5, §21.6, §21.7, §21.8, §22.3, §23.1–§23.3, §24, Appendix G, Appendix H,
  plus targeted greps of the register rows (F1/F5/F6/F8/F14/F18/F35/F36, L24/L25,
  L31/L33/L34/L36/L43/L45, R1–R10).
- No walk transcripts. I judged every finding against the document text as
  quoted in the finding, and re-fetched the surrounding text myself in every
  case. Where a reporter's quotation was partial I say so below.
- No `transcript-triage-*.md`. I did not list the round19 directory for the
  purpose of seeing what was in it; I did run one `ls` at the very start
  (before reading the prohibition carefully enough) which printed the three
  triage filenames. I opened none of them. Disclosed.
- I deliberately did NOT consult the user's memory files, though nothing in the
  brief forbade it, because one index line names a "lowercase-vs-ALLCAPS
  discriminator" as an established project position and the brief says each
  finding is decided on this text.

## The one upgrade/keep: quiz-01

Claim: nothing MUST-level obliges a compactor to carry a stored tile's payload
bytes forward unchanged.

I tried hardest to kill this one and failed. Searched for a governing MUST in:

- `[R-CNF-05]` "A writer MUST emit only conforming files" — output conforming
  under either reading, so no bite.
- `[R-CNF-06]` / `[R-WRT-01]` — "An appender and a compactor satisfy every
  writer requirement for the bytes they produce and **the preservation
  obligations of §20.4** for what they carry forward". §20.4 governs *records*.
- §2.4's preserve-verbatim row — "§20.4's table states the cases: its MU = 1 and
  MU = 0 / PE = 1 rows." Closed at records.
- §5.2 `[R-CNT-02]` distinguishes "a stored-tile extent" from "a record extent",
  so a tile payload is not reached by any record rule.
- `[R-WRT-05]` reaches "header, inline payload, and extent slot" only.
- `[R-WRT-08]` bars re-encoding "a record whose type it does not implement".
- `[R-WRT-09]` obliges *verification* ("each relocated extent's checksum,
  including every stored tile's entry crc"), not preservation. It presupposes
  copying; it does not prohibit re-encoding.
- `[R-MDL-02]` "reference arrays MUST equal the live generation's bit for bit"
  — satisfied by a re-encode that preserves decoded values.
- §17.4 `[R-COD-11]`, §8.2 — nothing.
- Appendix H's updater entry — non-normative, and about records.

The only text that forecloses reading B is `[R-PRV-04]` in §23.2: "`[R-WRT-07]`
preserves every stored tile's bytes and every index entry's crc bit for bit, so
a compacted file remains trivially correlatable with its input by content."
That is normative under `[R-CNF-01]`, but it is a *characterisation of another
rule*, not an obligation on the compactor. Under reading B it is simply a false
sentence in normative text — which is a defect of a different kind, not a
decision.

Counter-argument I weighed and rejected as insufficient: that a re-encoding tool
is not a compactor at all but a whole-file rewrite under `[R-LIF-01]`, so both
outputs are emittable by *some* conforming writer and the conforming-file set is
unchanged. That is true, and it is the reason I did **not** flag writer-05 or
adversary-05 byte-level despite their identical shape. The distinction I am
drawing, stated so it can be attacked:

> In writer-05 and adversary-05 a MUST exists and the question is its scope; the
> document decides the scope elsewhere (quoted below). In quiz-01 the obligation
> the rest of the document relies on — `[R-PRV-04]` states it as fact, item 8 of
> Appendix G assumes it when it concedes irreproducibility "only modulo its
> trailer", verifier-03's item-6 problem only exists because of it — is not
> stated at MUST level anywhere. The absence is of the requirement, not of a
> qualifier.

If the maintainer's byte-level test ranges over the set of conforming files
rather than over what a named actor may emit from a named input, this downgrades
to editorial and the repair is unchanged. I say so rather than hide it.

Repair: capitalise. "A compactor MUST carry every stored tile's bytes forward
verbatim, and MUST leave each index entry's length and crc unchanged; …".

## Groups, with the sentence I used to decide each

### G1 §23.1's "two ways" omits unstoring — reader-01, writer-01, verifier-07, diagrams-01, register-01

Narrow reading refuted by the document's own vocabulary:

- §5.2 `[R-CNT-21]`: "Every byte the live state does not claim is **slack**:
  alignment and slab gaps, the pre-trailer pad, and **everything an earlier
  commit superseded**." That is an exhaustive account of slack. §23.2 says the
  unstored tile's earlier payload is slack. It is not a gap and not the pad,
  so in this document's own terms an earlier commit superseded it.
- §3.1: "**Superseded payload bytes from earlier generations do not make a tile
  stored**" — applied to precisely the tile whose live entry is the sentinel.

§20.3 step 4's "stores or supersedes … become unstored" contrasts what a commit
does to *entries*, not what becomes of *bytes*. Two of the five reporters
(diagrams, verifier) reached the broad reading themselves.

Byte-level: no. `[R-PRV-01]`'s own quantifier — "MUST NOT represent **any
commit that makes sample data unreachable** as erasure of it" — reaches the
unstore on either reading, and the rule binds a representation, not a byte.

PARTIAL. One clarifying word is still worth having: "superseding it (its payload
replaced, or the tile unstored)".

### G2 a planar channel drop is a further way — adversary-02

Checked the construction: `[R-GEO-06]`'s disk ordinal is c·N+s, so dropping the
*trailing* channel leaves every surviving ordinal fixed; §14.2 makes a planar
plane's decoded size P·Bᶜ, independent of C; §20.3 step 4 expressly says
"Dropping a tile out of the addressed set … is not itself such an alteration".
So the operation is permitted and the reporter is right about that.

But the dropped plane's payloads become slack, and by §5.2's exhaustive slack
account they are therefore superseded — so the count survives for the same
reason as G1. PARTIAL, editorial. Not byte-level: same `[R-PRV-01]` quantifier.

### G3 `[R-PRV-01]` is scoped to sample data; the paragraph covers a dropped record's extent — reader-05, quiz-02

I looked for a widening sentence and found none. §20.4 gives only "An updater
that drops such a record SHOULD report the loss"; §23.2 gives only a SHOULD
about treating metadata as published. The MUST NOT says "sample data" and the
gloss that follows names only shrink and supersede. The paragraph's own third
member is outside the requirement it introduces. CONFIRMED, editorial.

Byte-level: no — "`[R-PRV-01]` binds how a tool represents a commit"; both
readings leave every file byte-identical, and `[R-CNT-21]` fixes what happens to
the bytes either way ("its content is unconstrained, and no conformance
requirement applies to it").

### G4 quiz-01 — see above. CONFIRMED, byte-level.

### G5 the compactor cannot evaluate §20.5's antecedent — reader-02, writer-02

Both reporters build the fork on "[R-CNT-26]'s floor is 0". That is only half
right: `[R-CNT-26]` says "the lowest version_minor that defines **every feature
present in the file** — *for a file expressible under this text*, 0". For an
output carrying a later-minor `tarn.` key the floor is not 0, so in the
reporters' headline case the two branches converge and the constructed
divergence dissolves.

It does not dissolve everywhere: an input whose minor merely *overstates* (minor
3, no later-minor feature present) leaves branch 1 at floor 0 and the
conservative branch at 3, and the compactor cannot tell that case from the other
one. So the ambiguity is real, just narrower than reported. CONFIRMED.

Byte-level: no, and this one is airtight. Both branches are SHOULDs.
`[R-CNF-12]`: "Deviation from a SHOULD is not a violation for this purpose:
§21's register enumerates MUST-level conditions only, and a verifier reports a
SHOULD deviation as an advisory that does not bar certification." `[R-CNF-05]`:
"A writer MUST emit only conforming files. … two conforming writers given
identical input MAY produce different conforming files." `[R-CNT-07]`: "A reader
MUST NOT reject a file for its version_minor." So both trailers are emittable by
a conforming writer under *both* readings — unlike quiz-01, where one reading
removes an output from the compactor's repertoire. Severity: design-decision
(the repair adds a rule for the unevaluable case).

### G6 §20.5's "(F36, L25, R1)" and "the two of §10.1's four vehicles" — verifier-08, register-06, adversary-01, quiz-04

Checked §10.2's table: eight numeric spaces. Reserved-range violation rows are
F36 and L25 (record type), L36 (channel layout 3–255), L33 (linearization),
L34 (sample type), L43 (codec), L45 (filter), L31 (index encoding), R1
(metadata encoding) — nine rows, three cited. Confirmed by grep of §21.3/§21.5.

verifier-08's second half is also right on its face: §21.6 has a row making an
experimental-range instance of vehicles 1 and 2 conforming, so "the two of
§10.1's four vehicles §21.6 makes conforming" is only true once §10.3's
"Experimental values are private use" is silently applied to exclude them from
"a feature a later minor defines". The conclusion holds; the wording does not.

adversary-01's extra claim — that R1 does not belong under the output reading,
its Detector being *reader* at open, so `[R-WRT-06]`'s "MUST NOT emit a file
carrying a violation it has detected" forces refusal — checks out against R1's
row (`reader`, `open (top-level); layer access (sub-record)`).

CONFIRMED, register-bookkeeping. Byte-level: no — every omitted row states its
own condition and §21.1 makes the rule govern where a row and its rule diverge;
and the obligation served is a SHOULD (`[R-CNF-12]`, quoted above).

### G7 §21.7's "witnessed only where A *and* B" — verifier-09, register-03, adversary-04

The literal parse is contradicted by the next clause, which is marked "instead".
The charitable parse (the "only" governs the content-row witness, scoped by the
trailing "where §21.4's content rows fire") is the only one on which the
sentence is true; nothing marks that scope. All three reporters reached the
charitable parse independently, which is evidence it is recoverable, not that it
is written. CONFIRMED, editorial.

Byte-level: no. §21.1: "The subsections after §21.5 are not part of the register
and carry no rows". T3/T14/T15/T17/T23/T25 are §21.4 rows with their own
governing rules, and `[R-CNF-04]` binds a reader to the register, not to §21.7.

Repair: "is witnessed by §21.4's content rows only where the affected tiles
remain stored *and* the change reaches a byte §14 structurally constrains …".

### G8 a SHOULD listed among register-omitted "violations" — writer-04, quiz-03

§21.7 ¶2's stated reason (no witness) is true of the version_minor floor; it is
just not the operative reason, which `[R-CNF-12]` supplies. Stating one of two
sufficient reasons is imprecise, not contradictory, and §21.7 itself writes the
modal in capitals ("the floor its version_minor SHOULD take"), which is the flag
a reader needs. PARTIAL, editorial. Repair: "— and, being a SHOULD, outside the
register in any case (`[R-CNF-12]`)".

### G9 §21.7 omits the appender's identical `[R-CNT-08]` obligation — register-05, adversary-06

Accurate. `[R-CNT-08]`: "An updater MUST copy forward unknown ignore-lane bits
of the file it modifies and MUST NOT clear them", equally unwitnessed. But the
completeness expectation is foreclosed: §21.1 says "neither this completeness
clause nor the instance arithmetic below reaches … §21.7's account of what no
check detects", and calls §21.7 "the account, **by class**, of what fails it".
An account by class owes no per-instance enumeration. PARTIAL, editorial —
naming the twin is a cheap improvement, not a defect against a stated rule.

### G10 "§20.5's two obligations on a compacted file's trailer" omits two more — writer-03

The fresh file_id and generation 1 are trailer obligations and are equally
unwitnessed. But §20.5 grounds both in exactly the two identifiers §21.7's ¶2
opens by naming: "a compacted file is a whole-file rewrite under a new file_id
by definition (`[R-LIF-01]`) … would break the (file_id, range) cache contract
of `[R-LIF-03]`". §21.7 ¶2 opens: "Committed-prefix immutability and the
generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's
history". Covered by class, plus §21.1's "by class" as in G9. PARTIAL.

### G11 §21.7 walks three of the bar's four heads — register-04

The worked example holds: interleaved a:uint32 / b:uint16 → a:uint16 / b:uint32
leaves Q = 6 and the decoded size unchanged while `[R-SER-01]`/§14.2 move b's
in-sample offset, so head 3 is damaged with no row firing. But the reporter's
own mitigation is the deciding one: §21.7 ¶1 states the class ("A writer that
emits well-formed structures carrying wrong sample values … produces a file that
every checksum in §8 certifies"), and §21.1 makes §21.7 an account by class.
PARTIAL, editorial.

### G12 §21.7's "None of these" disclaimer placement — verifier-02

Refuted from inside §21.7. The disclaimer's *reason* is stated generally — "no
file-level witness exists to check, so nothing about the file is left
undetermined and the verdict is unaffected" — and ¶2's members are defined by
exactly that property ("omitted from the register because a single file exhibits
no witness of their violation"). The reason therefore transfers on its own
terms. Independently §2.4: "a verifier certifies only violation-free files", and
§24's corpus presupposes conforming is reachable. REFUTED; the placement is
still worth improving. Editorial.

### G13 `[R-CNF-02]`'s conduct enumeration vs §21.7's classification — verifier-04, quiz-05

The constructed witness pair is sound and the conclusion (the compactor's
carry-forward binds the actor, not the bytes) is right. But the enumeration is
not falsified, because `[R-CNF-02]` states **two** classes and closes only the
second: "A few obligations this specification places on writers govern their
*conduct* rather than their output — where a value is published, or which
registry version a writer targets (§10.3, §18.3) —" (open, "a few", illustrative
gloss) and then "A writer obligation **whose violation this specification
expressly declares not to be a file-conformance violation** binds the actor in
the same way; §6.3's flags = 0 … and §6.2's pre-trailer gap … are the cases this
text states". §20.5's carry-forward is nowhere *expressly declared* not to be a
file-conformance violation — §21.7 says only that it has no witness — so it does
not join the closed class. PARTIAL, editorial: §21.7's "no witness" vocabulary
is genuinely the wrong bin for a conduct rule, and one clause would fix it.

### G14 "reproducible only modulo its trailer" vs §20.4's drop licence — reader-03, adversary-03

Confirmed and I could not break it. §20.4's MU = 0 / PE = 0 row: "**A compactor
MAY drop it whenever it rewrites the file**" — unconditional, unlike the
appender's. §7.3 gives both registered types PE = 1, so the record must be
unassigned-type; the reserved range is F36/L25, and §21.6 records the
experimental-range MU = 0 record as conforming — so the input is reachable.
Appendix G item 3 pins record *order*, and the closing inventory does not mention
the drop. Two profile-adopting compactors therefore differ in the record set,
dir_length, the directory CRC and every downstream offset. CONFIRMED, editorial.

Byte-level: no. Appendix G is non-normative under `[R-CNF-01]` and disclaims
itself: "It adds no requirement to any actor: a writer ignoring it is fully
conforming." Both outputs are conforming files.

Repair: either add a fixed drop policy to the profile, or widen the concession —
"reproducible only modulo its trailer and §20.4's drop licence".

### G15 Appendix G item 6 is unmarked and a compactor cannot obey it — verifier-03

Items 2 and 8 mark their creator-only halves; item 6 does not, and under
`[R-WRT-07]` a compactor cannot convert a stored all-fill tile to a sentinel
(entry lengths and crcs would change, and §20.5 licenses dropping only records
§20.4's table names — "a tile-index entry being no record §20.4's table licenses
dropping"). CONFIRMED, editorial. Note the cross-link: item 6 is obeyable by a
compactor *only* under quiz-01's reading B, so the appendix's silence here is
weak evidence for reading B — I recorded it and did not let it decide quiz-01.

Byte-level: no, same non-normativity quote as G14.

### G16 Appendix G's closing paragraph vs item 8 — register-07

Item 8: "The `flags` half is a creator's rule … The version_minor floor **binds a
compactor too**". Closing paragraph: "`version_minor` at its floor … — item 8's
creator's rule, not a compactor's (§20.5)". Straight contradiction; the two
halves read as swapped. The closing paragraph disclaims itself — "Read the
numbered items as the list; this paragraph names what they are for, not how many
there are" — which settles which governs but not that the gloss is wrong.
CONFIRMED, editorial. Not byte-level (non-normative appendix).

### G17 "regenerates each relocated tile-index region" — reader-04

Tried to kill this and largely succeeded. "Relocation" in `[R-WRT-07]` names
compaction's operation, not a per-structure predicate of having changed offset:
the sentence opens "A compactor preserves content but not **placement**", the
output is a whole new file in which every structure is placed anew, and
`[R-WRT-09]` obliges verification of "each relocated extent's checksum,
including every stored tile's entry crc" — which on the reporter's literal
reading would exempt any extent that happened to land at the same offset, an
absurd result. And if the literal reading were available, `[R-WRT-07]`'s own
closing MUST plus `[R-CNF-05]` ("A writer MUST emit only conforming files")
forbids emitting the result. PARTIAL, editorial: dropping the word "relocated"
costs nothing.

### G18 §20.4: does adding a top-level record count as changing one? — writer-05

Deciding text, both halves of it in the same row: "A commit changes the layer set
by adding a layer" (an addition *is* a change to a set), and the closed
carve-out "Dropping the record, or dropping another record in the same commit,
is not itself such a change, so a commit whose only effect would be the drop
MUST retain it." The carve-out names drops and only drops; the row's evident test
is whether the commit has an independent effect, which a commit that adds a
user-metadata record has. PARTIAL — reading (b) is foreclosed, though the word
"another" is worth replacing with "any other non-layer top-level record, added
or modified".

Byte-level: no, and the reporter agrees. Both outputs are conforming files;
`[R-CNF-05]` gates emission on file conformance.

### G19 int32 → float32 at equal element size — adversary-05

Refuted by `[R-TYP-04]`: "**A sample value is its bit pattern** (§3.2,
`[R-MDL-02]`) … Wherever this specification treats two sample or fill values as
the same value, it means **their encoded bytes are identical**." The gloss's
"meaning exactly what they meant" is therefore fixed to byte identity, and the
bytes are identical, so criterion and gloss agree: the commit is permitted. The
reporter's own bool counter-example confirms the criterion is doing the work —
uint8 → bool retroactively engages `[R-SER-08]`, which *is* something §14 fixes.
PARTIAL (reading (a) is right; the "disagreement" is not one), editorial at most.

### G20 a file-scope rejection and the partial total — verifier-01

Refuted; I worked all three readings against the text. §9.7 `[R-LIF-08]`: "Where
the walk does not complete — a scope-level rejection blocks enumeration, or the
verifier stops at the first violation (`[R-CNF-11]`) — the sum is reported as
partial" kills reading 2. §5.2 `[R-CNT-21]`: "A partial total is **F less the
bytes claimed by the claimants the walk did enumerate**" kills reading 1, and
the discard clause the reporter generalises is expressly confined — "the
claimants it had already enumerated are discarded **with the layer**", inside a
parenthetical whose subject is "a rejected layer's claimants". Reading 3 is what
the text gives. REFUTED. Not byte-level (§2.3: "An established violation takes
priority").

### G21 no general duty to name an established violation — verifier-05

The fact is right; the implied defect is not. §2.4's Note decides it: "'Reject'
prescribes the scope of unusability, not user interface: **how failure is
reported is implementation technique**." The §24 argument fails too — §24's own
Note says "What the corpus tests is that no reader serves data from a scope this
specification rejects", i.e. behaviour, not report strings. PARTIAL; whether to
add a naming duty is a maintainer decision, not an edit forced by the text.

### G22 no naming duty for an unassigned-type record extent — verifier-06

The document notices the case and closes it deliberately: §22.3 opens "**Four
residues are stated rather than defended**" and names this one — "The extent of
a record of a type this specification has not assigned is covered by no checksum
either (§8.1), so corruption inside it is equally invisible". No duty is
withheld by oversight. The asymmetry with `[R-MTA-10]` is real and is a design
question. PARTIAL, design-decision.

### G23 §20.4's table and §6.1's writer MUST carry no identifier — diagrams-02

Accurate as a fact: `[R-WRT-05]` closes §20.4 ¶1, `[R-WRT-08]` closes its last
paragraph, and the table between them states three MUSTs. §6.1's "Writers MUST
emit exactly these 16 bytes" sits two paragraphs ahead of `[R-CNT-04]`.

Counter I found and weighed: there may be an unstated convention that an
identifier terminates its requirement and reaches back to the previous one — and
§21.6's row *does* cite `[R-WRT-08]` for the PE-bit disposition, which only
makes sense under that convention. But `[R-CNF-06]`, §2.4 and §20.5 all reach
the table by *section*, which suggests the author did not treat it as
`[R-WRT-08]`. Either mint identifiers or state the convention in §2.2.
CONFIRMED, register-bookkeeping. Not byte-level: the obligations are stated in
full and reachable by section.

### G24 §21.2's preamble reason does not reach F5's physical-size instance — diagrams-03

The reason really is inapplicable: §19.1 step 1 obtains F before the trailer is
fetched, so for F5's "F (physical file size)" instance the version gate is
behind, not ahead. But the preamble's *conclusion* is decided elsewhere, by §2.3
`[R-CNF-02]`: "a file declaring another major is **neither conforming nor
nonconforming** under it: a reader refuses such a file on capability grounds
(§6.3, `[R-CNT-07]`), and that refusal is not a finding about its bytes."
PARTIAL, editorial.

Byte-level: no. Both verifiers refuse and neither certifies (`[R-CNF-11]`: "a
verifier MUST NOT certify a file it reports that way"); what differs is the
label on a refusal, not accept/reject.

### G25 Appendix H's reader entry is wider than `[R-CNF-03]` — diagrams-04

Confirmed by comparison: §2.3 carries three qualifiers, the checklist keeps one,
and the two dropped are exactly the two §21.6's closing paragraph exists for.
`[R-ERR-04]` states the carve-out verbatim. Appendix H disclaims itself — "each
entry's authority is the requirement or section cited, never this summary" —
which is why this is editorial and not open. CONFIRMED, editorial.

### G26 §18.2's "Valid values | 1 or 2" — diagrams-05

Largely refuted by the cell itself, which the reporter quotes in full and then
argues past: the cell reads "**1 or 2; see below**". It does not purport to
delimit validity; it defers, and the prose immediately below gives the whole
value set, with §10.3, §21.6 and `[R-MTA-10]` agreeing. §6.2's version_major
hedges inline instead; both devices work. PARTIAL, editorial.

### G27 §21.5's governing-rule cells are inconsistent — register-08

Checked all ten cells: R1 `[R-CNT-25]`, R2 `[R-CNT-20]`, R3 `[R-CNT-25]`,
R4 `[R-MTA-09]`, R5 `[R-CNT-25]` (R-MTA-04, R-ENC-11), R6 `[R-CNT-25]`
(R-ENC-12), R7–R9 `[R-MTA-04]` (R-CNT-25), R10 `[R-MTA-04]` (R-ENC-12).
`[R-MTA-04]`'s own text carries all three name constraints — "every key
satisfying §4.6's name rules — non-empty, at most 255 bytes, free of U+0000
through U+001F" — so R6 and R10 restate one list under two different governing
rules. §21.1: "A Governing rule cell names **that requirement** first" — the
requirement that defines the condition — and `[R-CNT-25]` defines the outcome,
not the condition. CONFIRMED, register-bookkeeping.

### G28 §21.1 carries no requirement identifier — register-09

Verified: §21.7 `[R-ERR-01]`, §21.8 `[R-ERR-02]`, §21.9 `[R-ERR-03]`–
`[R-ERR-05]`; §21.1 has none, and its opening citation of `[R-ERR-02]` points at
a corpus-coverage rule that states neither the tie-break nor the instance
arithmetic. The tie-break binds readers, verifiers and corpus builders, so §2.2
reaches it. CONFIRMED, register-bookkeeping. Same repair family as G23.

### G29 §21.6's MU = 1 refusal lacks a placement qualifier — register-02

Real: `[R-CNT-18]` says "an unknown sub-record type with MU = 1 is reject-layer
— **never reject-file**", §10.3 keeps the two apart ("the MU-bit outcome of
`[R-CNT-15]` at file scope and `[R-CNT-18]` for layer sub-records"), and §20.4's
table keeps them apart again. But §21.1's tie-break does reach it — "§21.6's
entries restate their governing rules on the same terms a row does, and where
such an entry and the rule it cites diverge, **the rule governs there too**" —
and the closing paragraph's two cases are §21.6 entries in the ordinary sense.
The secondary defect the reporter names is also right: "a file this document
declines to judge is not one" explains only the first case. PARTIAL, editorial.

Byte-level: no. `[R-CNF-03]`'s acceptance duty is relieved for a file "carrying
no record of a type it does not implement with MUST_UNDERSTAND = 1" whatever the
placement, so both behaviours are licensed.

## Which groups I tried hardest to kill and failed

- **quiz-01 (G4)** — ten separate candidate MUSTs checked; only a
  characterisation in §23.2 stands against it.
- **G14** (Appendix G's drop-licence leak) — I checked reachability of the input
  (§7.3 flags, F36/L25, §21.6) and every item of the profile for a pin. None.
- **G6** (the row citation) — checked all eight spaces of §10.2 against §21.3
  and §21.5 by grep. The citation is short by six rows.
- **G27** (the §21.5 cells) — read `[R-MTA-04]`, `[R-CNT-25]` and `[R-ENC-12]`
  in full. The inconsistency survives.

## Counted coverage

44 input ids, 29 groups, each id in exactly one group. Counted twice by hand
against the id list in the brief.
