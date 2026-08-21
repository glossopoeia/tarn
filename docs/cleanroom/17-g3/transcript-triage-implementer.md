# Round 17 triage — implementer-consequence lens

## Disclosure

Read: `spec/tarn.md` only, in these ranges — §2.1/§2.2 (96–133), §2.3 (134–230),
§3.2 (341–362), §6.1/§6.2/§6.3 head (693–790), §11.1 (1463–1500), §13.3
(1739–1790), §15.3 (2027–2060), §18.2 (2434–2565), §19.1 (2647–2700), §19.2
(2700–2745), §20.1/§20.2 (2856–2890), §20.3 (2890–3097), §20.4/§20.5
(3097–3254), §21.1 (3256–3340), §21.4–§21.9 (3445–3690), §22.3 (3750–3768),
Appendix G (4119–4232), Appendix H (4230–4317). Plus `grep` for section
headings, `R-MTA-09|R-MTA-10`, `R-CNT-10`.

Read no walk transcript — every claim below was checked against the spec text
directly rather than against a reporter's account.

**Disclosure of a procedural slip:** I ran `ls` on the round17 scratchpad
directory to confirm the path before writing this file. The instructions told
me not to list that directory. No `transcript-triage-*.md` file existed in the
listing and I opened none; the listing showed only the six walk transcripts,
three quiz transcripts, and helper scripts. Reporting it because the round's
design depends on it.

## Method

The line I used to separate a byte-level fork from a decided one:

> A fork is byte-level when **both readings survive as readings of normative
> text after every decider in the document has been applied**. A reading that
> lives only in text `[R-CNF-01]` makes non-normative, or that a sentence in
> the same paragraph forecloses, is not a permitted reading and cannot fork
> what a conforming implementation may emit.

I applied the first limb of the test ("may emit") as literally as it is
written: an updater is an implementation, `[R-CNF-06]` binds it, and a
disagreement about which commits it may perform is a disagreement about which
byte sequences it may emit — even where both candidate outputs are themselves
conforming files. That is why groups B and C survive and group A does not: A's
second reading is not a reading of a requirement at all.

---

## Grouping

| Group | Defect | ids |
|---|---|---|
| A | §11.1 Rationale states §20.3's shrink bar over the wrong generation | reader-01, writer-03, verifier-01, diagrams-01, register-01, adversary-03, quiz-01 |
| B | compactor: [R-WRT-06] refuse vs [R-WRT-07] reproduce-and-emit | reader-02, writer-02, verifier-02, register-03, adversary-01 |
| C | §20.4 "modifying any layer's record" — mechanical vs logical | writer-01, verifier-03, adversary-02, quiz-02 |
| D | §20.4 "removing a layer" names an operation no commit performs | reader-04, diagrams-03, register-05 |
| E1 | §21.5 preamble: scope of the experimental-encoding exception | reader-03 |
| E2 | §21.5 preamble: oversize/resource decline is a third disposition | writer-05, adversary-04 |
| F | §21.7 says T3 reads the index entry | register-02, quiz-04 |
| G | §21.7 has no class for [R-LIF-02]'s durability barriers | writer-04 |
| H | Appendix G item 2's unnamed fallback file_id | writer-06 |
| I | Appendix G item 3's "any record extents" re-covers index regions | quiz-05 |
| J | reproduced F-dependent structural entry is not stable under new F | verifier-04 |
| K | Appendix H verifier block omits pad bits (T5) | diagrams-02 |
| L | §20.3's shrink sentence restated without the fill carve-out | diagrams-04 |
| M | §20.3 shape (c): "whatever its geometry", stores-none vs empty | diagrams-05 |
| N | §21.1's own rules carry no requirement identifier | register-04 |
| O | [R-ERR-04]'s decline sentence is unqualified | register-06 |
| P | §6.1's "and nothing else" vs §6.2's remote-reader parenthetical | quiz-03 |

7+5+4+3+1+2+2+1+1+1+1+1+1+1+1+1+1 = **34**. Counted twice by hand.

---

## Group A — §11.1 Rationale (7 ids). CONFIRMED, not byte-level.

Verified both texts. §11.1 (line ~1484): "a shrink is barred wherever it
alters what §14 fixes for a tile **the new state still stores**, and permitted
where it drops tiles out of the addressed set". §20.3 step 4: "the quantifier
is the superseded generation's, so a shrink that turns real positions into
padding of a tile stored there is barred whether or not the new state still
stores it." The contradiction is real, and it is on exactly the case §20.3
spends two sentences closing.

**Downgrade premise, stated so it can be attacked.** The §11.1 passage sits
inside a `> **Rationale.**` block. §2.1 `[R-CNF-01]`:

> "All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative."

and the passage's own first clause names its governor: "§20.3 states
normatively, and governs, what a commit may do to a layer that already stores
tiles". So §11.1's quantifier is not a permitted reading of any requirement.
There is exactly one normative reading, and the set of commits a conforming
appender may perform is the same under it whichever way the paraphrase is
repaired. Nothing about emission or acceptance moves.

**Tested against the two constructions the reporters offered, plus the shape
the calibration warning names.**

- *Unstored-in-the-same-commit* (reader-01, register-01, adversary-03,
  quiz-01, verifier-01, diagrams-01(a)): the damaged tile is de-addressed or
  written to the sentinel, so the live state is clean and `[R-ERR-01]` records
  it as unwitnessed. This is precisely the "damaged structure outside the new
  live state" shape the warning tells me to test. It does not rescue the
  finding, because the reason A fails is not "the file carries a violation
  anyway" — I am not making that claim. It fails because §11.1 is not a
  requirement. If §11.1's sentence sat in normative prose this would be
  byte-level; register-01 says exactly that and is right.
- *diagrams-01 construction (b)* (E 8→3, tile 0's position 3 turns to
  padding): here the reading actually does change the emitted file — but the
  emitted file carries T4, and `[R-CNF-05]` ("A writer MUST emit only
  conforming files") bars a conforming writer from emitting it under either
  reading. So the conforming-emission set is unchanged here too.

Repair: restate §11.1's clause in the superseded generation's tense, or drop
the paraphrase and cite §20.3. **Implementer consequence:** an appender author
who takes the guard from §11.1 ships a permissive guard nothing downstream
corrects. That is a real cost and worth the edit — but it is a cost to the
author, not a fork in the format.

---

## Group B — compactor refuse vs emit (5 ids). CONFIRMED, **byte-level**.

Both texts verified verbatim at §20.5.

`[R-WRT-06]` carries two limbs:

> "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
> fails, **and MUST NOT emit a file carrying a violation it has detected** …
> Dropping is the one disposal that answers, and only where §20.4's table
> licenses it … Where the table does not license a drop the compactor MUST
> refuse."

`[R-WRT-07]` disposes of it for one class:

> "`[R-WRT-09]`'s checks reach the index chain and each stored tile's entry
> crc, not an entry's own value domain, so such an entry is not one
> `[R-WRT-06]` obliges a compactor to refuse"

I checked the premise that clause rests on and it is false in the document's
own terms:

- §15.3 `[R-IDX-03]`: "For each entry … **a reader MUST classify as
  follows**".
- §2.3 `[R-CNF-11]`: "Verifiers and updaters are readers of the files they
  process and inherit every reader obligation."
- §2.3 `[R-CNF-04]`: "A reader MUST detect every violation the error register
  (§21) assigns to the reader as its detector" — T6–T12 all carry detector
  *reader*.
- §19.2 fixes the deadline at "first reliance on the structure that carries
  it", and `[R-WRT-09]` says the compactor "relies structurally on every
  structure it copies".

So the compactor has detected T6–T12 **in fact**, and limb 2's trigger is
detection in fact, not `[R-WRT-09]`'s check list.

**Why I did not downgrade.** The tempting downgrade — taken by reader-02 and
verifier-02 — is that the clause names `[R-WRT-06]` unqualifiedly and states a
conclusion, so a conclusion outranks its broken justification. I tested that
against the text and it does not hold, for a reason neither reporter states:
the object of the clause is the word **refuse**. `[R-WRT-07]` says the entry is
not one `[R-WRT-06]` *obliges a compactor to refuse*. Not being obliged to
refuse does not lift "MUST NOT emit a file carrying a violation it has
detected", which is a prohibition on emission, not an obligation to refuse.
Under that reading the compactor is free not to refuse and forbidden to emit,
and refusing is the only act left — which makes `[R-WRT-07]`'s whole
reproduction prescription dead text, exactly as register-03 says. Under the
other reading the clause is a blanket stipulation and the compactor emits, and
"the violation travels with it into the output (`[R-WRT-01]`)" confirms that is
what §20.5 intends. Both are readings of normative text; nothing in the
document picks one.

**The two implementations, concretely.** Input: a conforming file, one index
entry rewritten to `offset = 0xFFFF_FFFF_FFFF_FFFF, length = 5` (§15.3's
"exactly one of offset and length is the sentinel" row → T7, structural,
reject-tile), with the segment CRC and `crc_of_crc_array` recomputed so the
index chain verifies. Every `[R-WRT-09]` check passes.

- Compactor A classifies (as §15.3 obliges), has detected T7, finds no drop
  licensed — §20.4's table reaches records, and an index entry is not a record
  — and refuses. **No bytes on disk.**
- Compactor B reproduces the entry verbatim at its disk ordinal beside
  relocated siblings, recomputes segment CRCs and `crc_of_crc_array`, mints a
  fresh `file_id` at generation 1, and emits a complete file. **A specific byte
  sequence on disk.**

That is the first limb of the test directly: B's output either may or may not
be emitted by a conforming compactor, and §20.5 does not say which.

adversary-01's second construction (a reserved-range top-level record type,
F36) does *not* add a fork: Appendix H places F36 among the verifier-only
checks ("a reserved-range record or sub-record type value, whatever its MU
bit (`[R-CNT-15]`, F36, L25)"), so a compactor that does not recognise the
range has not detected it and limb 2 does not bite; one that does recognise it
must refuse. Detection-relative behaviour is designed, not defective. I note
it and do not count it.

**Repair (maintainer's call).** Turn the exception on the ground register-03
names: *no disposal exists and `[R-WRT-05]` bars correction*, and state
expressly that limb 2 does not reach a violation the compactor is obliged to
reproduce verbatim. The alternative — make the compactor refuse — kills
`[R-WRT-07]`'s reproduction rule and should be chosen deliberately if at all.

---

## Group C — §20.4's drop licence (4 ids). CONFIRMED, **byte-level**.

Text verified at §20.4's MU = 0 / PE = 0 row:

> "An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's record,
> the entry set of its index, or which of its tiles are stored; for a
> top-level record, the file's layer set — which a commit changes by adding or
> removing a layer **and equally by modifying any layer's record** — or
> another *non-layer* top-level record. Superseding a stored tile's bytes is
> not such a change for either kind … so a commit whose only change is a
> supersede MUST retain the record."

**The supersede sub-case is closed.** writer-01 and quiz-02 both build on it,
and the row's final clause settles it in terms: "a commit whose only change is
a supersede MUST retain the record." An implementer who reads the whole cell
does not fork there. That half of the group is refuted on its own construction.

**The store sub-case is open,** and verifier-03 and adversary-02 found it. A
commit whose only change is to store a previously-unstored tile in layer X, in
a file also carrying an unrelated top-level MU = 0 / PE = 0 record:

- Reading (a). §20.3 step 4 re-emits X's index region "necessarily at a new
  placement", so X's record's extent slot and `crc_of_crc_array` change and it
  cannot be re-emitted byte-identically. `[R-WRT-05]` requires byte-identical
  re-emission of "every record it retains and does not logically modify" — so
  either the store logically modified X's record, or every index-moving commit
  violates `[R-WRT-05]`. It modified it. Modifying any layer's record changes
  the file's layer set. Drop licensed.
- Reading (b). The carve-out's stated reason — a supersede "re-places that
  layer's index region … without altering the scope any record attaches to" —
  is true word for word of a store. So index-region re-placement never alters
  a record's scope, the store reaches the top-level list through no other
  item, and the record MUST be retained. Support: for a *layer sub-record* the
  list separately names "which of its tiles are stored", which would be
  redundant if "that layer's record" already covered any byte change; and the
  top-level list conspicuously does not carry that item.

Both are readings of normative text. Nothing in §20.4, §20.3 or §20.5 picks
one — the word "logically" is undefined, and the carve-out's conclusion is
restricted by name to one operation while its reason generalises.

**The two implementations, concretely.** Same input, same instruction "store
layer X's tile at disk ordinal 1":

- Updater A (a) omits the 24-byte MU=0/PE=0 record from the new directory.
  `dir_length` is 24 (or 24 + inline) smaller, the directory's terminal CRC
  differs, everything placed after it sits at a different offset,
  `committed_file_length` and the trailer CRC differ, and the old record's
  extent falls to slack — so the two files also disagree about a verifier's
  reported slack total.
- Updater B (b) carries the record forward.

Both outputs are conforming files, so no reader or verifier diverges. The fork
is entirely in which byte sequences a conforming **updater** may emit, which is
the first limb of the test, and it decides whether a third-party tool's
application state survives a routine append — the loss §20.4's own SHOULD-report
clause exists to make visible.

I considered downgrading on "both outputs are conforming, so this is conduct".
I did not, because the test's first limb is about emission, `[R-CNF-06]` makes
updater conduct a conformance class, and §21.7 already tells us no file-level
witness will ever adjudicate it — which makes the text the only arbiter and
therefore makes its silence expensive rather than harmless.

**Repair (maintainer's call).** Say "**logically** modifying any layer's
record" in the top-level list, and state whether storing or unstoring a tile
counts for a top-level record as it plainly does for a layer sub-record.
§20.3 step 4's vocabulary already exists: "a layer whose record alone changes"
vs. a layer whose index region moves.

---

## Group D — "removing a layer" (3 ids). CONFIRMED, editorial.

Decider, three lines below the table cell:

> "**No commit therefore removes a layer record**, or a user-metadata record
> at either scope."

and, for the compaction escape:

> "That is not compaction, which carries every layer of its input forward
> (§20.5)."

Layer records are type 0x0001 with registry-fixed PE = 1 (`[R-CNT-22]`), and
§20.5 carries forward "the live committed state … less any record §20.4 lets
it drop" — which is MU=0/PE=0 only. Tested the unchosen route: a commit that
zeroes every extent of a layer does not remove its record, so the layer set is
unchanged. The trigger is unreachable and the reachable trigger set is
identical under both readings; no file's bytes turn on it.

Repair: strike "or removing" from the em-dash clause, or add "(which no commit
performs — see below)".

---

## Group E1 — reader-03, §21.5's exception clause. CONFIRMED, register-bookkeeping.

The over-reach is real: the exception attaches to the encoding, and R2 (extent
CRC) carries no encoding qualifier.

**Downgrade quotation.** `[R-MTA-10]` names the surviving checks exhaustively
and the extent CRC is one of them:

> "file conformance — a pure predicate on bytes (`[R-CNF-02]`) — is decided by
> the structural checks that precede the document alone: the record's framing
> and extent slot (`[R-CNT-13]`), the encoding byte's own value set
> (`[R-MTA-03]`), **and the extent's terminal CRC (`[R-CNT-20]`)**."

Said again from the other side at §22.3 `[R-SEC-04]`: "the extent of a
user-metadata record under an unassigned encoding **is covered by its terminal
CRC** but constrained by no content rule". And the preamble's own next
sentence delimits itself: "what `[R-MTA-10]` withdraws is the document's
content rules". A failed extent CRC is not a content rule. §21.1's tie-break
("where a row and the rule it cites diverge, the rule governs") points the same
way for R2, whose governing rule is `[R-CNT-20]`.

Verifier verdict on reader-03's constructed file (encoding 0x80, bad extent
CRC): nonconforming, under every decider above. No fork.

Repair: qualify the preamble's exception — "except at an experimental-range
encoding, where the document's **content** rules do not attach".

---

## Group E2 — writer-05 + adversary-04, the oversize document. CONFIRMED, register-bookkeeping.

Same sentence, different defect: the preamble's disjunction has no room for a
document that is unreadable because it exceeds a reader's chosen decode bound
under an *assigned* encoding.

**Downgrade quotation**, §18.2 `[R-MTA-09]`:

> "a reader instead decodes with a bound of its own choosing, no smaller than
> §21.9's user-metadata guarantee, and a document exceeding that bound is
> ignore-record like any other it cannot read … the bound is that verifier's
> capability and not a limit on validity (`[R-CNF-10]`), so the decline is not
> a finding that the file is nonconforming and **a verifier MUST NOT report it
> as one**."

and its Note: "A file whose document decodes to more than the guarantee stays
conforming … A reader that proceeds takes ignore-record for that record."
§21.9 `[R-ERR-03]` independently: "A file exceeding any of these remains
conforming."

adversary-04's Verifier P (reports nonconforming) is barred by an explicit
MUST NOT. Verifier Q reports *cannot establish* or, with a larger bound,
certifies. No verdict fork survives.

Grouped separately from E1 because the repairs are different edits: E1 narrows
the exception to content rules; E2 adds the third disposition (or restricts
"unreadable" to file-relative unreadability, the rescuing reading adversary-04
names).

---

## Group F — §21.7 on T3 (2 ids). CONFIRMED, editorial.

§21.7: "witnessed by T3 or T14, **which read the index entry rather than the
decoded image**". §21.4's T3 condition: "The **decoded payload's** byte length
is not exactly the tile's decoded size derived from the layer's declarations"
— detectable only after §19.4 steps 6–7. True of T14 (`[R-COD-04]`, checkable
before any payload fetch), false of T3.

**Downgrade quotation**, §21.1: "The subsections after §21.5 are not part of
the register and carry no rows". §21.7 is an account; the operative rows are
§21.4's, and both fire on the same files under either description. Corpus
authorship is the only thing touched, and §21.8 builds from the rows.

Repair: "witnessed by T14, which reads the index entry, or T3, which reads the
decoded image's length".

---

## Group G — writer-04, the durability barriers. CONFIRMED, register-bookkeeping.

Checked §21.7's second paragraph against writer-04's claim. Its criterion is
"a single file exhibits no witness of their violation", and its classes are:
history properties (`[R-LIF-01]`, `[R-LIF-03]`); the ordinal mappings
(`[R-GEO-06]`, `[R-SER-01]`); `[R-CNT-13]`'s opacity; `[R-CNT-18]`'s nesting;
§20.3 step 4's declaration bar; `[R-ENC-06]`'s field widths. `[R-LIF-02]`
steps 4 and 6 — "both barriers, not one" (`[R-WRT-02]`) — meet the criterion
and fall in no class: the two files a barrier distinguishes are byte-identical,
so it is not a property of the file's *history* either. §21.1 makes §21.7 "the
account, by class, of what fails" the detectability gate, so the gap is a real
one in a passage that claims to be an inventory.

Not byte-level: barrier compliance leaves no byte trace by construction, so no
sequence and no verdict turns on it, and §9.2's Note already prices the
consequence. Repair: name `[R-LIF-02]`'s barriers as a class — obligations on
the write *process* rather than on any state a file can be in.

---

## Group H — writer-06, Appendix G item 2. CONFIRMED, design-decision.

"Any other fixed nonzero value is substituted in the measure-zero case that
they are all zero (§6.2 forbids `file_id` = 0)." Every other item in the
appendix names its value or names its producer; this one says pick one, which
is the shape of the freedom the appendix exists to remove.

**Downgrade quotation**, Appendix G's own head: "It adds no requirement to any
actor: a writer ignoring it is fully conforming", and `[R-CNF-05]` already
licenses two conforming writers to differ on bytes. Both writers emit
conforming files; only conformance to a voluntary profile diverges, at
probability 2⁻⁶⁴. Repair costs six words: name a constant.

---

## Group I — quiz-05, Appendix G item 3. CONFIRMED, editorial.

Verified the overlap: §5.2 and §20.5's Example both count a tile-index region
as a record extent ("every record extent but a relocated tile-index region —
itself a record extent (§5.2)"), and item 3's per-layer phase places it, then
its second phase claims "any record extents in ascending record order — all of
them after every layer's tiles and index region". The domain overlaps.

**Downgrade quotation**: same non-normativity clause as H, plus quiz-05's own
observation that reading (2) is internally unsatisfiable for any two-layer
file, so only reading (1) is available. Repair: "any *remaining* record
extents".

---

## Group J — verifier-04, F-dependence of a reproduced structural entry. CONFIRMED, design-decision.

The mechanism failure is real and I could not find a rule that closes it. Four
of §15.3's six structural rows classify against F ("offset + length overflows,
or offset + length > F − 64"). §20.5 makes a compactor "free to place
structures anywhere §5.2 admits" and bounds F_out nowhere, while
`[R-WRT-07]` requires the entry be "reproduced with its offset and length
exactly as they stand". So §20.5's claim that "the violation travels with it
into the output" is false for those rows at a large enough F_out.

I checked verifier-04's claim that `[R-WRT-07]`'s reference-array clause cannot
police outcome (iii), and it holds: §3.2 `[R-MDL-01]` gives a reference array
to "Each layer of **a conforming file**", and §13.3 `[R-TYP-09]` bars reading a
malformed entry's tile as fill — so the input layer denotes no array at that
tile and "MUST equal the live generation's bit for bit" has no referent.

**Why not byte-level.** This is not an ambiguity — verifier-04 says so itself
("The permitted readings are only about the remedy, not the fact"). The
reproduction rule has one reading; §20.5's placement freedom already licenses
two conforming compactors to emit different outputs from one input; and the
open question — whether `[R-WRT-06]`'s second bar makes the compactor refuse
such an input in the first place — *is* group B, which I have already flagged
byte-level. Closing B closes most of J. What remains after B is a design
decision: whether §20.5 must additionally bound F_out or re-emit F-dependent
structural entries as the sentinel, and whether the "travels with it" claim
should be narrowed to the F-independent rows.

Stating the premise so it can be attacked: **my downgrade rests on there being
only one reading of "exactly as they stand", not on any claim about the
disputed file's conformance.** The disputed file is nonconforming in the input
and may be conforming in the output — I am not treating either as decisive.

---

## Group K — diagrams-02, Appendix H's verifier block. CONFIRMED, figure.

Verified the asymmetry inside one appendix. Verifier block: "decoded-content
obligations — padding samples and interleaved boolean bytes (§14.5, §14.2)".
Writer block, four paragraphs earlier: "fill-encodes edge padding **and pad
bits** (`[R-SER-05]`, §14.5)". §14.3's Note makes pad bits distinct from
padding positions, and T5 is a verifier-detected row.

**Downgrade quotation**, Appendix H's own opening: "each entry's authority is
the requirement or section cited, **never this summary**." `[R-SER-05]` states
the pad-bit obligation normatively and T5 registers it; the parenthetical
"(§14.5, §14.2)" does carry the scope. Repair: add "and pad bits" to the
verifier line, matching the writer line.

---

## Group L — diagrams-04, §20.3's shrink sentence. PARTIAL, editorial.

The looseness is real; the contradiction is not. **Decider, the opening of the
very paragraph diagrams-04 quotes from:**

> "An extent MAY also **shrink**, and **the bar above is the whole of the
> test**, in the bar's own tense: a shrink is permitted exactly where it alters
> nothing §14 fixes for any tile the layer stores in the generation this
> commit supersedes."

"The bar above is the whole of the test" imports the bar's carve-out — "a new
padding position whose stored byte already holds the fill `[R-SER-05]` fixes —
is not what this bars" — wholesale. Reading (ii), an independent second bar
without a carve-out, is foreclosed by that clause: an independent second bar
would not be "the whole of the test". The later sentence's stated purpose is
the quantifier ("and for the same reason: the quantifier is the superseded
generation's"), not a new content test. So no implementer is entitled to (ii),
and the appender that refuses every shrink into a fill-valued position is
simply wrong rather than following a permitted reading.

Repair (optional): "a shrink that turns real positions into padding *of a tile
stored there, and thereby alters what §14 fixes for it,* is barred whether or
not …".

---

## Group M — diagrams-05, shape (c). CONFIRMED, figure.

Both moves check out. The Example says "A layer storing no tile is re-declared
freely **whatever its geometry**". Step 4's permission carries a proviso the
Example drops — "provided the grown geometry stays within every bound the
layer's own declarations impose, `[R-COD-07]`'s lz4 decoded-size cap among
them (L44)" — and the same sentence distinguishes the class the Example
conflates: "which **an empty layer** escapes only because that cap is
quantified over **addressed** tiles". A layer with E = 1000 and every entry the
sentinel stores no tile and addresses one; it is not empty.

**Downgrade quotation**: `[R-CNF-01]` makes Examples non-normative, and
`[R-CNF-05]` ("A writer MUST emit only conforming files") independently bars
the result — the produced layer is L44, a reader-detected layer-scope row, so
every verifier rejects it. The conforming-emission set is unchanged.

Repair: "A layer **addressing** no tile is re-declared freely, subject to
every bound its declarations impose".

---

## Group N — register-04, §21.1 has no identifier. CONFIRMED, register-bookkeeping.

Verified: §21.1 ends at "…the rule governs there too." with no `[R-…]`. The
ERR identifiers begin at `[R-ERR-01]` in §21.7. §2.2: "Normative requirements
carry identifiers of the form `[R-<PREFIX>-<NN>]`." §21.1 says of itself that
its completeness "is normative", so it claims requirement status.

**Downgrade quotation**: §2.1 `[R-CNF-01]` makes the text normative whether or
not it carries an identifier — "All text in this document is normative except
…" — so nothing an implementation does changes. The cost is citability: §24
`[R-VEC-02]` asks each vector to name "that row's governing requirement
identifier", and a vector exercising §21.1's own row-versus-rule precedence has
only a renumberable section number to cite.

---

## Group O — register-06, `[R-ERR-04]`. CONFIRMED, editorial.

The sentence is unqualified as written: "Software that declines a file whose
every quantity lies within the table is not a conforming reader
(`[R-CNF-03]`)".

**Downgrade quotation**, §2.3, which scopes it by name:

> "and none of whose values exceeds the minimum guarantees of §21's limits
> table (**§21.9's `[R-ERR-04]` governs a refusal on that last ground**;
> §21.6's closing paragraph names the other two)"

and the sentence's own citation `[R-CNF-03]` carries the two carve-outs, and
its own next sentence is "Either way, a refusal **on resource grounds** MUST be
reported as a resource limit". Reading (b) is additionally a reductio, since
`[R-CNT-15]` compels the very rejection it would condemn. Under either reading
the reader rejects the same file and returns the same bytes; only the label it
applies to itself changes. Repair: insert "on resource grounds".

---

## Group P — quiz-03, §6.1's "and nothing else". PARTIAL, editorial.

The term *remote reader* does appear outside §6.4, in `[R-CNT-06]`. But §6.1's
claim is about what the distinction **governs**, and in §6.2 it governs
nothing.

**Decider**, §19.1 step 1:

> "**End of file.** Obtain the transport-authoritative file size F
> (`[R-CNT-10]`)."

That obligation runs to every reader without classification, and F17's
condition is stated against that size ("Trailer committed_file_length does not
equal the transport-authoritative file size"). So a reader that classifies
itself either way performs the same comparison and reaches the same verdict.
§6.2's parenthetical explains what "the file size" means where there is no
local file; it adds no obligation. Repair (optional): "for a reader with no
local file, the size its transport reports", dropping the classification word.

---

## Byte-level tally

**2** — group B and group C. Both are forks between two readings of normative
text that survive every decider I could find, and in both the two
implementations are describable byte for byte. Everything else is decided by
text I have quoted above.

Reporters self-flagged 6 (writer-01, writer-02, verifier-03, register-03,
adversary-01, adversary-02); all six land in B and C, and all six survive as
groups even where an individual construction (writer-01's supersede-only) is
refuted by its own cell.
