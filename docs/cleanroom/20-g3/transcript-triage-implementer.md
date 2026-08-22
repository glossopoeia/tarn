# Round 20 triage — implementer-consequence lens

## Access disclosure

Read: `spec/tarn.md` in full (in chunks: 1–400, 400–900, 900–1200, 1200–1372
selectively, 1524–1545, 1691–1990, 2235–2420, 2417–2570, 2635–2860,
2893–3280, 3276–3730, 3757–3800, 3897–4040, 4158–4369). Ran one script over
the register tables to recount §21.8's instance arithmetic. Read **no**
`transcript-*.md` file at all — not the walk transcripts, not the quiz
transcripts, and above all not `transcript-triage-*.md`. Every reporter claim
below was checked against the specification text directly. `ls` of the round20
directory happened once, before I had read the prohibition carefully; it
listed filenames only and no `transcript-triage-*` file existed in it at that
moment. No triage transcript was opened.

## Mechanical check run

Counted every register row's Instances cell (`;`-separated, `—` = 1):

    121 conditions, 273 instances
    F 36 rows / 58 inst; L 49 / 116; T 26 / 55; R 10 / 44
    F29 = 3, L14 = 3, R7 = 6

§21.8's published "121 conditions over 273 instances" is reproduced exactly
by the **Instances** cells. That decides the direction of the repair in G9.

---

## G1 — §2.3's acceptance carve-out is scope-blind (reader-01, quiz-01)

Same defect, two reporters, same resolution. Both read §2.3 `[R-CNF-03]`'s
"carrying no record of a type it does not implement with MUST_UNDERSTAND = 1"
as unqualified by scope, and both resolve it by §7.4.

Checked:
- §7.4 `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer,
  and where the file is otherwise conforming a reader MUST NOT reject the file
  for it". Capitalised, actor named, outcome named, and the antecedent holds —
  an experimental-range type is conforming bytes (`[R-CNT-15]`: "a record type
  from the experimental range is conforming"), MU=1/PE=1 satisfies
  `[R-CNT-12]`.
- §21.6 closing: "the same type as a layer sub-record is reject-layer and
  never a ground to refuse the file (`[R-CNT-18]`), so only the top-level case
  is a file a reader refuses."
- §2.4 `[R-CNF-12]`: the licence to reject is stated only "For a nonconforming
  file". There is no general permission to reject a conforming file.

So reading (i)/(1) — refusal permitted — requires deriving a permission from
the absence of a duty, against a capitalised MUST NOT that names the case.
Not available. **Byte-level: no.** Implementer consequence is real but is a
misreading cost: a reader built from §2.3 or Appendix H alone discards every
layer of a conforming file over one sub-record. Repair is a scope qualifier
("no *top-level* record"), nothing more. Editorial.

## G2 — channel selection is not in §19.4's request vocabulary (reader-02)

Checked §19.4's opening: "A **point request** names a single coordinate
(§3.1); a **region request** names a rectangular range of coordinates, one
interval per dimension" — coordinates only, no channel. Then step 2 "per
requested channel c planar", step 7 "Locate each requested value", step 8 "a
planar layer's several channels", closing note "Channel-subset reads verify
only the segments they touch". All four confirmed present. `[R-TYP-08]`'s
"for each channel the tile carries" confirmed.

The reporter's (b) — one-channel request against an interleaved *sentinel*
tile returns all C fill values while the same request against a *stored* tile
returns one — is a genuine incoherence the literal words permit. (c) is right
on `[R-MDL-02]` ("MUST return exactly the corresponding portion of the
reference array").

**Byte-level: no.** No file's bytes, no accept/reject verdict. And the corpus
cannot witness it: `[R-VEC-02]` records "the decoded content a reader is to
return from every scope it can read" — a scope's full content, not a
per-request projection. What forks is an API's arity. But it is a decision
the maintainer owes: either channel selection is part of a request (then
§19.4 must say so and `[R-TYP-08]` must be read as fixing which channels
*read as* fill), or it is not (then step 2's "requested channel" and the
closing note's "channel-subset reads" are describing an operation the document
does not define). Design-decision.

## G3 — `[R-SER-08]` fixes a truth value, not a returned byte (reader-03)

Checked §19.4 step 8: "Return the requested values' bit patterns unaltered …
for every byte a conforming file can carry, the whole of this step
(`[R-SER-08]` fixes what a reader returns for the one byte a conforming file
cannot)." So step 8 expressly carves the case out of "bit patterns unaltered".
`[R-SER-08]`: "MUST report 0x00 as false and every other byte as true."

Decisive text I found that the reporter did not quote — §21.1, normative:

> "`[R-SER-08]` is the one rule that goes the other way: it **resolves** a
> nonconforming interleaved boolean byte **to a value rather than serving it
> through**, which is why §14.2 calls it the sole resolved byte in this
> format."

Handing 0x37 back *is* serving it through. Appendix H says the same
("the sole *resolved* byte"). With §14.2 fixing true's encoding as 0x01, the
returned byte is 0x01. Decided, at the cost of three hops.

**Byte-level: no**, and the premise of that downgrade, stated for attack: the
thing that forks is a value handed to a caller from a *nonconforming* file,
which is neither a byte a writer may emit ("Writers MUST NOT emit any byte
other than 0x00 or 0x01 as an interleaved bool value") nor an accept/reject
verdict (the reader is expressly relieved: "A reader is not obligated to
screen decoded content, and a reader that does not detect the violation is not
thereby nonconforming"). Residual cost worth naming in the repair: a T2
conformance vector's `[R-VEC-02]` "decoded content a reader is to return"
field has to state 0x01, and today the manifest author has to derive that
from §21.1 rather than read it in `[R-SER-08]`. One clause fixes it.

## G4 — appender relocating a live index region (writer-01)

The reporter's central claim is that Reading A "leaves open the case of a
layer whose record the commit does logically modify — a rename, a fill change
…, a slab clear". The sentence they quoted answers exactly that case in its
own first clause:

> "**A layer whose record alone changes keeps its extent slot, pointing at
> the existing region**, as does a layer the commit leaves untouched
> (`[R-WRT-05]`); relocating a live index region is compaction's operation
> (§20.5, `[R-WRT-07]`), not an appender's."

Rename, fill change on a layer storing no tile, and clearing a slab
declaration are precisely §20.3 shape (c) — "a change confined to the
directory" — i.e. a layer whose record alone changes. The clause covers them.

Also: this sentence is inside §20.3's numbered list, which closes at step 6
with `[R-WRT-04]`. It is not identifier-less. And §2.1 `[R-CNF-01]` — "All
text in this document is normative except: §1; any text labeled *Note*,
*Example*, or *Rationale*; and appendices identified as non-normative" —
makes keyword-free declarative text normative. §2.1's "when, and only when,
they appear in all capitals" governs how the *key words* are interpreted, not
whether unkeyworded normative sentences bind. The document relies on this
everywhere (§5.1: "The file size of a conforming file equals the live
trailer's committed file length F").

So PARTIAL: "logically modify" being used exactly once and never defined is a
real editorial weakness; the relocation question is not open.
**Byte-level: no.** Premise: the byte-level test quantifies over files — which
byte sequences are conforming, and which a reader must accept or reject — not
over one tool's conduct. Under the other quantification every appender-conduct
rule in §20 would be byte-level. Both candidate outputs here are conforming
files and no reader or verifier can tell which tool produced which.
(Note: the reporter's aside that §21.7 "does not list this obligation" is
right, and their sibling claim in adversary-03 that §21.7 lists `[R-WRT-05]`
is wrong — grep shows `[R-WRT-05]` nowhere in §21.7.)

## G5 — step 2's "MUST NOT drop the record" vs §20.4's drop licence (writer-02)

> "Against any other structure the appender carries forward, it MUST NOT
> repair the defect — `[R-LIF-01]` freezes the committed prefix — and MUST NOT
> drop the record (§20.4)."

Both readings have content. Reading A is not dead letter: it says an appender
that has *established* a defect may not launder it by dropping, which is the
same policy as the neighbouring "MUST NOT repair the defect" and the paragraph
"An appender that carries a violation forward SHOULD report it". Reading B
rests on the sentence's subject ("any other structure the appender carries
forward" — a dropped record is not carried forward) and on the bare "(§20.4)"
reading as a pointer to the governing rule, which §20.4 states in full with
its own MUST-NOT-except:

> "An appender MUST NOT drop it except in a commit that *independently*
> changes the scope the record attaches to … a commit whose only effect would
> be the drop MUST retain it."

Nothing in the text picks between them. **Byte-level: no** — the two outputs
are different files; each is graded identically by every verifier under both
readings (the retained one nonconforming for its F26 bit, the dropped one
conforming). What forks is whether the appender's *conduct* was licensed,
which no file witnesses. Same premise as G4, stated the same way. But the
operational cost the reporter names is real and worth the clause: an operator
verifying after every append gets red or green depending on which reading its
updater's author took. This one needs a decision, not just wording: does the
drop licence survive a defect the appender has detected?

## G6 — Appendix G's item 5 test catches tile extents and layout (writer-03)

Item 5's test verbatim: "§17.3 leaves the choice to the writer, it changes the
stored bytes of every tile it touches, and no content implies it".
- Tile extents: §11.3's Note — "Tile extents are a writer's choice, and this
  specification imposes none". Changes the stored bytes of every tile. Not
  implied by content. Satisfies all three. Not pinned by any item.
- Layout: `[R-SER-06]` leaves 1 or 2 to the writer; §14.4's Note — a bool
  channel is "⌈P/8⌉ packed bytes planar versus P bytes interleaved". Satisfies
  all three. Not pinned by any item.

The reporter's counter to Reading A is sound: item 2's rationale groups
"tiling, layout, and codec" as things two files with the same arrays may
differ in, and item 1 pins the codec anyway — so membership in that list does
not exempt a degree of freedom from being pinned.

**Byte-level: no**, decisively: "Core writer conformance is semantic … It adds
no requirement to any actor: a writer ignoring it is fully conforming."
Non-normative appendix, no rule moves. But the appendix does not deliver what
its own opening claims ("closes the degrees of freedom this format
deliberately leaves open"), and the failure mode is silent — two vendors both
certifying "Appendix G profile" get different digests for the same arrays and
see a cache-miss rate, not an error. Needs a scoping decision: either the
profile takes the layer's declarations as given input, or items 5 grows.

## G7 — `[R-CNT-21]`'s relief cites §6.2 only (verifier-01)

Checked all four legs:
- `[R-CNT-04]` places the front-block equality check "before other
  processing"; §19.1 step 1 confirms it precedes the step-2 trailer fetch.
  F6's row: "a verifier holds no such exemption (§2.3)".
- `[R-CNT-27]` is in §5.1, and `[R-CNT-06]`'s ordered list does not contain
  it; §19.1 never mentions it. F5's Detected cell is "open".
- `[R-CNT-21]`'s relief: "Where **§6.2's ordered validation** rejects the file
  before a live trailer is established there is no F and no live state to
  walk, so the total is not owed at all".
- `[R-CNT-21]`'s partial MUST: "or because the verifier elected under
  `[R-CNF-11]` to stop at the first violation — the verifier MUST report the
  total as partial."

The relief's *reason* ("there is no F and no live state to walk") holds at F6
and F5; its *citation* does not reach them. Reading (b) is incoherent for F5 —
a 40-byte file cannot present a trailer to derive F from — which is itself
evidence that the relief was meant to be about the state.

**Byte-level: no.** Verdict is *nonconforming* under every reading; nothing is
emitted, accepted or rejected differently. `[R-CNF-11]`'s own framing — the
per-requirement and unexamined channels "constrain the report, not the
verdict" — puts the slack figure in the same class. Repair is one clause:
extend the relief to any rejection established before a live trailer, naming
`[R-CNT-04]` and `[R-CNT-27]`.

## G8 — no naming duty for unassigned-type record extents (verifier-02)

`[R-SEC-04]` sets the two uninspected residues side by side and states the
remedy for one only. `[R-MTA-10]` has the MUST for the metadata case ("it MUST
report each record it ignored on this ground, naming the owning scope, the
encoding value, and the stored extent length … bytes a certificate covers
without inspecting are counted and named, never silent"). For the
unassigned-*type* extent, §22.3 says only that corruption there is "equally
invisible" and that nothing an updater does would surface it. I searched for a
counterpart duty and found none: §8.1's map gives those bytes no checksum,
§7.2 makes them opaque, and §9.7 makes them a claimant, so they are not in the
slack total either.

Reporter's reading (a) is correct on the keywords and the reporter says so.
**Byte-level: no** — no rule attaches to those bytes under either reading.
The consequence is the one that matters to an implementer building the §22.3
policy: "an operator who wants no such bytes rejects on that report line" is
unavailable for the class carrying no checksum, which is the worse class. Two
verifiers' certificates differ in whether the bytes are mentioned. A decision
is owed (extend the naming duty, or say expressly that none is owed and why).

## G9 — Condition cells omit an alternative their Instances cells price (diagrams-01, register-01)

One defect, two rows, two reporters (register-01 saw R7 only). Verified both:

- L14 Condition: "its 24-byte header is truncated at the payload end, or its
  inline_length runs past that end" — two alternatives; Instances:
  "sub-record header; sub-record inline_length; **trailing residue**" — three.
  The file-scope twin F29 states it: "…or bytes remain after the last complete
  record". `[R-CNT-18]` states it normatively: "the remaining bytes MUST parse
  as zero or more complete sub-records … with no residue; any overrun,
  truncation, or residue is a validity error at layer scope."
- R7 Condition: "not well-formed JSON, or its top-level value is not an
  object" — two; Instances include "**leading U+FEFF**" × 2 containers — six
  total. `[R-MTA-04]` states the BOM as its own restriction: "The top-level
  value is an object, and the encoding carries no byte-order mark: a leading
  U+FEFF makes the document unreadable." A permissive parser accepts a BOM'd
  document as well-formed JSON, so the first alternative does not subsume it.

**Byte-level: no** — §21.1: "each row *restates* its governing rule, and where
a row and the rule it cites diverge, **the rule governs**", and the governing
rules state both conditions, so reader disposition (reject-layer; ignore-
record) is identical for both implementations.

Direction of repair is decided mechanically: my recount gives 121/273 from the
Instances cells, exactly §21.8's published figure. So the Instances cells are
right and the **Condition cells** must gain the missing alternatives; touching
the Instances cells instead would move the published totals and shift the
corpus build list by four files.

## G10 — Appendix A and "local reader" (diagrams-02)

The reporter quotes half a sentence. Full text:

> "A local reader additionally verifies bytes [0, 16) by equality first, which
> `[R-CNT-04]` **requires of any reader holding them** — as a **remote reader
> does too** whenever its speculative suffix window reaches offset 0 … A
> shorter window can still spare the second request: 112 bytes covering
> [16, 128) contains the directory … while **bytes [0, 16) stay non-resident,
> so §6.1 leaves the front-block check to the reader**."

The residency test is stated twice in the same paragraph and applied to a
remote reader in the very next clause. Appendix A does not attach the
obligation to transport class; it names the ordinary case and immediately
gives the rule. The claimed hazard — "a verifier author may grant a remote
verifier an exemption" — is not reachable from this text, and F6 forecloses it
("a verifier holds no such exemption (§2.3)"). PARTIAL: the lead-in words are
loose, everything after them is right, and the appendix is non-normative.
**Byte-level: no.** No repair required; an optional reword.

## G11 — §4.7's Note mis-describes two layout tables (diagrams-03)

Both claims check out.
- §7.4's table columns are Field | Type | Constraint. Against the Note's own
  six-item list it omits offset, **size**, and class; the Note says "omits the
  offset and class columns".
- §7.2's five Field cells: "type (0 invalid)"; "flags: bit 0 …, bits 2–15
  reserved"; "inline_length"; "extent_offset"; "extent_length". Two of five
  carry a range; the extent slot's range is in `[R-CNT-13]`'s prose. The Note
  says "§7.2 folds **each** field's range into its Field cell".

**Byte-level: no** — labelled *Note*, excepted by `[R-CNF-01]`; every width
comes from §7.4's Type cells and every omitted range from `[R-CNT-12]`/
`[R-CNT-13]`. The cost is to a reader auditing the document's own map of how
to read its tables. Two-word fix in each clause.

## G12 — §21.6's fifth entry (register-02)

Three sub-claims, graded separately.
1. *Which identifier owns §20.4's table.* The document's convention is that an
   identifier closes the whole run of normative text since the previous one —
   `[R-WRT-04]` closes a six-step numbered list, `[R-CNF-11]` a multi-paragraph
   bullet, `[R-WRT-06]` a run whose final sentence (refusing an MU = 1 record)
   is a different topic from its opening one (file_id). On that convention the
   table is inside `[R-WRT-08]`'s block and §21.6's citation is defensible.
   The convention is nowhere stated — see G17.
2. *The dropped qualifier.* Confirmed and real. §20.4: "For a type the updater
   **implements** that this specification does not register, the definition it
   implements the type from supplies the flags, **and the stored bits never
   do**". §21.6's cell says "preserved or dropped per its PE bit", flat. An
   updater that implements an experimental type and reads the entry alone
   takes the disposition from a bit §20.4 says never governs there.
   §21.1 makes the rule govern, so the divergence is decided — but the entry
   is the defect.
3. *`[R-CNT-15]` cited for a sub-record claim.* `[R-CNT-15]` opens "An unknown
   record type **at file scope**"; the entry names L25, a sub-record row, whose
   own Governing cell is "`[R-CNT-15]` (R-CNT-18)". The entry should carry
   R-CNT-18 the same way.

**Byte-level: no** — both dispositions (retain byte-identically; drop, extent
becoming slack) produce conforming files, and no reader's verdict on either
differs. Register bookkeeping.

## G13 — §21.7 counts two unwitnessed trailer obligations (register-03, quiz-02)

Same defect. `[R-WRT-06]` places on the output trailer: fresh file_id ("a new
draw under §9.3's randomness advice, not merely a value compared against the
input's"), generation 1, the ignore-lane copy-forward, and the version_minor
floor. §21.7 names two. The fresh *draw* is unwitnessed by construction — the
output discloses a value, never whether it was drawn — and is exactly what
§21.7's second paragraph inventories. Generation 1 is visible in the output
but not as a compaction obligation; `[R-LIF-03]`, which §21.7 does name,
absorbs it.

Propagation point for whoever repairs this: §20.5's own answering sentence,
"**Neither** obligation has a witness in the output alone (§21.7)", sits
immediately after the version_minor sentence and refers to the same two. Add
the fresh draw to §21.7 and that sentence needs adjusting too, or the two
sites disagree again in the other direction.

**Byte-level: no** — §21.1 removes §21.7 from the completeness clause
("neither this completeness clause nor the instance arithmetic below reaches …
§21.7's account of what no check detects"), and F12 already registers the only
file_id condition a single file can exhibit. Register bookkeeping.

## G14 — §21.2's preamble and F5 (register-04)

Verified: `[R-CNT-27]` lives in §5.1, is absent from `[R-CNT-06]`'s ordered
list, and is unmentioned in §19.1 — yet §19.1 step 1 hands the reader F before
the trailer is fetched, and F5's Detected cell is "open". The preamble's
justification is purely about §6.2's ordering ("§6.2 puts the version gate
ahead of every check but the trailer magic and the trailer CRC"), which does
not reach a check §6.2 does not order. F6 got named as an exception on exactly
that ground; F5 did not get named at all.

The conclusion the preamble reaches is nevertheless right, and §2.3 is what
makes it right, not the ordering argument: "a file declaring another major is
neither conforming nor nonconforming under it … that refusal is not a finding
about its bytes." A verifier may not report *nonconforming* for such a file
whatever else it observed.

**Byte-level: no** — neither reading certifies the file and neither serves it;
what forks is the printed verdict label (*nonconforming* vs *cannot
establish*) and the diagnostic class. Note the discriminator against G15: here
no verifier certifies, so nothing accepts. Register bookkeeping — the preamble
needs F5 named with the reason `[R-CNT-27]`'s check yields to the gate.

## G15 — metadata zstd window above the 8 MiB guarantee (adversary-01) — the one flagged byte-level

Worked this hardest. The construction is right as far as it goes:
- §18.2 imposes only "the frame constraints of `[R-COD-06]` **that do not
  reference a tile**" and says "The constraints §17.2 states against a tile's
  declared decoded size do not apply". §17.2's window rule is stated against
  the tile's decoded size, so it is withdrawn. R4's instance list confirms it:
  frame magic, skippable frame, second frame, dictionary ID, content-checksum
  flag, trailing bytes — **no window row**. A 1 GiB metadata window is
  conforming.
- §21.9 guarantees a conforming reader only 8 MiB of `Window_Size`.
- `[R-MTA-09]`'s decline provision is written around "the bound above", which
  is the *document-size* bound (16 MiB), not a window. A verifier declining on
  a window is not literally inside it. That gap is real.

But the byte-level claim needs Verifier A to be permitted to report
*nonconforming* on R3, and three sentences forbid it:

1. §2.3 `[R-CNF-02]`: "File conformance is a pure predicate on bytes: **it
   does not depend on any reader, writer, or environment**." R3's condition —
   "a document's stored bytes fail to decode under its declared assigned
   encoding" — is therefore a fact about the bytes, and these bytes decode
   under RFC 8878. "My decoder refused" is not R3.
2. §21.9 `[R-ERR-04]`: "**A file exceeding any of these remains conforming**,
   and a reader MAY decline it — at the whole file, or at the narrowest scope
   whose declarations exceed what it can serve". The `Window_Size` row is one
   of "these", and it is not tile-scoped in its wording — §17.2 itself calls
   it "§21.9's 8 MiB `Window_Size` guarantee" and `[R-MTA-09]` reaches into
   §21.9 for metadata. So the document states in terms that this file is
   conforming.
3. `[R-ERR-04]` again: "a refusal on resource grounds **MUST be reported as a
   resource limit and not as a validity error**: the two send a user to
   opposite remedies". Reporting R3 for a window the decoder cannot afford is
   the forbidden move, named.

And the §18.2 Note already answers the "not a layer or a tile" objection for
documents: "a reader that instead declines on resource grounds under
`[R-ERR-04]` does so at the whole file, a document having no declared size and
so no narrower scope whose declarations that rule can measure."

So the two implementations are: Verifier A (8 MiB window) declines the decode,
reports the resource ground, verdict *cannot establish*, certifies nothing;
Verifier B (larger window) decodes `{}`, finds nothing, certifies. §2.3
sanctions that spread expressly — "*Cannot establish* is not a finding that
the file is nonconforming" — exactly as it does for a foreign major or an
unexecutable codec. A plain reader with an 8 MiB window takes ignore-record
for the record under `[R-CNT-25]`'s quarantine ("a decode failure … is
ignore-record") and serves every sample. No accept/reject fork.

**Byte-level: no.** Premises, stated so they can be attacked:
(P1) §21.9's `Window_Size` row is not tile-scoped and reaches a metadata
frame. If the maintainer intends that row to govern tile frames only, P1 falls
and `[R-ERR-04]`'s "remains conforming" no longer reaches this file — and then
the reporter's fork is live. I checked P1 against three sites (§17.2's
back-reference, §21.9's own unqualified wording, `[R-MTA-09]`'s reach into
§21.9) and it held at all three.
(P2) R3's condition is a byte predicate, not an actor predicate. `[R-CNF-02]`
is explicit; if R3 were actor-relative, file conformance would depend on the
reader, which `[R-CNF-02]` forbids in the same sentence.

PARTIAL, not REFUTED: what the reporter found and the document really lacks is
(i) any sentence for metadata matching §17.2's "a wider window is conforming
and merely permits a conforming reader to decline … on resource grounds", and
(ii) any writer-side steer matching §17.2's "Writers SHOULD keep the declared
window within §21.9's 8 MiB `Window_Size` guarantee". Without (ii) a writer at
a high zstd level emits a 1 GiB window as a matter of course and its metadata
is unreadable by every floor-conformant reader, which is a live interop
hazard even though every party is conforming. Two sentences close both.

## G16 — the 16 MiB metadata floor carries no keyword (adversary-02)

"a reader instead decodes with a bound of its own choosing, no smaller than
§21.9's user-metadata guarantee" — keyword-free, confirmed. Reading (b) (only
capitals bind, so the floor is descriptive) fails on the same ground as G4:
§2.1 `[R-CNF-01]` makes all text normative except Notes/Examples/Rationales/
§1/non-normative appendices, and the "when, and only when" clause governs the
interpretation of the eleven key words, not whether unkeyworded normative
sentences bind. Two further supports for (a): under (b) the §21.9 row
guarantees nothing whatever, and `[R-VEC-03]` treats the guarantees as
exercisable ("§21.9's minimum guarantees are exercised where a vector at the
bound is constructible"), which presupposes a testable obligation.

**Byte-level: no** — under both readings the reader accepts the file and
ignore-records the document, and *cannot establish* "is not a finding that the
file is nonconforming". What moves is which implementations count as
conforming readers. Editorial: give the floor a MUST.

## G17 — §20.4's preservation table and its citation handle (adversary-03)

The table's cells carry "The updater MUST NOT modify the scope the record
governs", "An appender MUST NOT drop it except…", "a commit whose only effect
would be the drop MUST retain it", "A compactor MAY drop it whenever it
rewrites the file", "SHOULD report the loss". They bind: §2.1 gives the
capitals BCP 14 force, `[R-CNF-06]` says an updater "MUST honor the
preservation obligations of §20.4", and §2.4's preserve-verbatim row points at
"§20.4's table". Nobody disputes the behaviour.

The reporter's claim that the block carries **no** identifier is contestable —
the document's trailing-identifier convention (`[R-WRT-04]` over a six-step
list, `[R-CNF-11]` over a multi-paragraph bullet, `[R-WRT-06]` over a run
ending on an unrelated sentence) puts it inside `[R-WRT-08]`'s block, which is
what §21.6 assumes. What is actually missing is the *statement* of that
convention: §2.2 says only "Normative requirements carry identifiers of the
form `[R-<PREFIX>-<NN>]`" and never says where an identifier sits or how far
back it reaches. Two competent readers (this reporter and the register
reporter) reached opposite conclusions from the same two paragraphs, which is
the evidence.

One factual correction: the reporter writes "§21.7 further places
`[R-WRT-05]`'s preservation among the obligations with no single-file
witness". `[R-WRT-05]` does not appear in §21.7 at all (grep: 604, 2931, 2951,
3107, 3164, 3784 — none in §21.7's range).

**Byte-level: no.** PARTIAL. Repair is a decision: state the scoping
convention in §2.2, or mint an identifier for the table — and §2.2 makes
minting a one-way door ("Identifiers are stable: they are never renumbered or
reused").

---

## Coverage

20 input ids, 17 groups, union checked by hand against the input list:
reader-01, reader-02, reader-03, writer-01, writer-02, writer-03,
verifier-01, verifier-02, diagrams-01, diagrams-02, diagrams-03,
register-01, register-02, register-03, register-04, adversary-01,
adversary-02, adversary-03, quiz-01, quiz-02 — each in exactly one group,
no duplicates.

Byte-level survivors: **0**.
