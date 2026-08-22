# Round 19 triage — implementer-consequence pass

## Disclosure

Read: `spec/tarn.md` only — §2.1–§2.5, §3.1, §3.2, §5.1, §5.2, §6.1–§6.4,
§7.2, §7.3, §7.4 ([R-CNT-16]–[R-CNT-18]), §9.7, §10.1–§10.4, §12.3, §13.1
opener, §14.1–§14.3, §18.1, §18.2, §19.1, §20.3–§20.5, §21.1, §21.2 (preamble
+ full row table), §21.5, §21.6, §21.7, §21.8, §23.1–§23.3, §24, Appendix G,
Appendix H. Ran `grep`/`sed` over the file to locate rules by identifier.

Read no walk transcript. Read no `transcript-triage-*.md` (I listed the round19
directory once, before I had internalised the prohibition on listing it; the
listing showed three triage filenames and I opened none of them — the contents
of the other two passes' notes are unknown to me). Read no `docs/`, no
`PLAN.md`, no `AGENTS.md`, no `conformance/`, no `registry.json`, no git
history, no web.

Every one of the 44 input findings was evaluated. No finding was skipped.

## The line I am drawing on "byte-level"

The test as posed: *does resolving this change which byte sequences a
conforming implementation may emit, or must accept or reject?*

Several findings in this batch fork what a **producer** may emit for a given
logical operation while leaving both outputs conforming **files**
(quiz-01, writer-05, adversary-05, reader-02/writer-02, reader-04). Taken
literally, "which byte sequences a conforming implementation may emit" could be
read to catch all of them, because a conforming *updater*/*compactor* is a
conforming implementation and its emittable set is input-relative.

I am not reading it that way, and here is the premise, stated so it can be
attacked:

> **Premise D.** A fork with no single-file witness is, by this document's own
> architecture, not a byte-level fork. §2.3: "File conformance is a pure
> predicate on bytes: it does not depend on any reader, writer, or
> environment." §21.7's second paragraph and [R-CNF-02]'s conduct carve-out
> exist precisely to hold a class of MUSTs (committed-prefix immutability, the
> generation sequence, the compactor's fresh file_id, §20.3 step 4's bar)
> outside file conformance because no single file exhibits their violation.
> A finding that forks one of those forks nothing observable.
>
> **Premise R.** A fork in what a reader or verifier must *do with given bytes*
> — accept, reject, or which scope it refuses — is byte-level, because the same
> byte sequence gets two different treatments from two implementations each of
> which can cite text.

If Premise D is wrong, then quiz-01, writer-05 and adversary-05 all become
byte-level and this pass has three false negatives. I have said so explicitly
in each group's rationale so the reconciler can flip them as a set rather than
one at a time. What makes me confident in D is that the document does not
merely tolerate witnessless writer obligations, it inventories them (§21.7 ¶2)
and it declares the taxonomy ([R-CNF-02]) — which would be pointless drafting
if a witnessless conduct fork were a conformance fork.

Under Premise R exactly one finding survives: **register-02**, which the
reporter itself declined to flag. See group `mu1-subrecord-refusal-scope`.

---

## Groups

### A. `prv01-enumeration-omits-unstore` — reader-01, writer-01, verifier-07, diagrams-01, register-01, adversary-02

Six reporters on one sentence:

> A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all.

Checked. §20.3 step 4 does set the words apart in the passage §23.1 cites:
"entries for tiles this commit stores **or supersedes** written to their new
state, entries for tiles that **become unstored** written as the sentinel."
§23.2 names the missing case and back-references §23.1 for it: "a tile unstored
by a later commit leaves its earlier payload in the file as slack (§23.1)".

diagrams-01's counter is the strongest thing said in defence of the sentence:
§3.1 uses *superseded* of exactly this case — "Superseded payload bytes from
earlier generations do not make a tile stored." So the document uses the word
both broadly (§1, §3.1, §5.2) and narrowly (§20.3 step 4). That inconsistency
*is* the defect; it does not rescue a closed count.

adversary-02 supplies a further route that neither "supersede" (narrow) nor
"shrink" names: dropping a trailing channel from a planar layer. I checked its
arithmetic against §14.2 and §11.4 — each surviving plane's decoded size is
P·Bᶜ, independent of C; disk ordinals are c·N+s so surviving ordinals do not
move; [R-CNT-17] forces the smaller entry_count. Nothing in §7.4, §11, §20.3 or
§20.4 bars a channel-count change on a layer that stores tiles. writer-01
raises the same route independently. Grouped here: same sentence, same defect
(a closed count that is short), different missing member.

**Implementer consequence.** Nothing to the bytes. [R-PRV-01]'s operative
quantifier is "**any** commit that makes sample data unreachable", which
reaches every route however the preceding sentence is read. What breaks is the
enumeration's use as a checklist: a tool that builds its "this is not erasure"
warning path from the two named routes ships without the warning for
sentinel-overwrite — the operation a user calls "delete this tile" — and for a
channel drop.

**Downgrade quotation:** "Writers and the tools built on them MUST NOT
represent **any commit that makes sample data unreachable** as erasure of it".
The requirement is quantified over the general case; the enumeration is prose
preceding it.

Severity: editorial. Repair: "superseding it (its payload replaced, the tile
unstored, or its channel or extent de-addressed)" — or drop the count and write
"A commit removes sample data in several ways —".

### B. `prv01-scope-excludes-dropped-record` — reader-05, quiz-02

Distinct from A: not the completeness of the enumeration but the scope of the
MUST NOT. The paragraph deliberately pulls the dropped-record extent inside
("and a dropped ancillary record's extent (§20.4) goes the same way … In each
case the bytes remain in the file as slack"), then the requirement quantifies
only over "sample data". So a tool that drops an MU = 0 / PE = 0 record, or
appends a new user-metadata extent superseding the old (§20.3 shape (c)), may
call it erasure and violate nothing.

Checked §20.4: "An updater that drops such a record SHOULD report the loss;
unreported, application state disappears with no diagnostic." The document
plainly cares about this case; it just did not bind it.

**Implementer consequence.** A "forget this record" feature ships with an
honest label over a fully recoverable document — the material §23.2 tells
writers to "treat as published content". No byte, no verdict.

**Downgrade quotation:** [R-PRV-01] binds representation, not emission —
"MUST NOT **represent** any commit … as erasure of it"; and [R-CNT-21] already
fixes the byte outcome in both cases ("Slack has no internal structure this
specification defines, its content is unconstrained").

Severity: design-decision — the maintainer must decide whether the honesty
requirement is deliberately sample-data-only or was widened incompletely.

### C. `compactor-minor-antecedent-unevaluable` — reader-02, writer-02

The rule's antecedent is "the output carries a feature a later minor defines
and this compactor does not", and its own worked example is "an unrecognized
`tarn.` key in a record it never decoded (§18.3)". [R-WRT-09] fixes the
compactor's depth at "the open (§19.1), each retained layer's record (§19.3)
and full index chain ([R-IDX-04]), and each relocated extent's checksum" and
says outright it "reaches no decoded content". [R-MTA-02] bars metadata from
influencing anything structural. So in the example case the compactor cannot
evaluate its own antecedent, and the two branches — "SHOULD be at least the
input's" vs "Otherwise version_minor follows [R-CNT-26]'s floor" — pull
opposite ways whenever the input's minor exceeds the floor.

Both reporters land on the conservative branch (max(floor, input minor)) and
both give the same reason: §20.5's stated harms are asymmetric. That is a
sound choice; the document does not make it.

**Implementer consequence.** Two compactors, one conforming input, trailers
differing in one u16 and therefore in the trailer CRC. Appendix G item 8
concedes this divergence but attributes it to "which features the compactor
implements" — which in the `tarn.` case it is not a function of at all.

**Downgrade quotation:** [R-CNF-12]: "Deviation from a SHOULD is not a
violation for this purpose: §21's register enumerates MUST-level conditions
only, and a verifier reports a SHOULD deviation as an advisory that does not
bar certification." And [R-CNT-07]: "A reader MUST NOT reject a file for its
version_minor." Both outputs are conforming files; no verdict moves.

Severity: design-decision. Repair: say which branch applies when the compactor
cannot establish the antecedent — the honest answer being "take the input's
minor as the floor unless it can show no such feature is present", which for
an undecoded document it never can.

### D1. `minor-vehicle-count-vs-2136` — verifier-08

verifier-08 attacks the *count*, not the row citation: "the two of §10.1's four
vehicles §21.6 makes conforming". §21.6's table does make an instance of all
four conforming — an experimental record type with MU = 0; an experimental
metadata encoding; a set ignore-lane bit; an unrecognized `tarn.` key. I
verified all four rows.

But the sentence's own antecedent is "a feature **a later minor defines**", and
§10.3 makes experimental values private use — never a later minor's. So the
restriction is supplied by the sentence itself, one clause earlier. The count
is correct in context and loose out of it.

Note that adversary-01 audits the same count and *upholds* it, which is why
these two ids are in different groups: they make opposite claims.

**Implementer consequence.** None. An implementer who reads the antecedent
before the parenthetical never reaches the wrong count.

**Downgrade quotation:** §20.5, same sentence: "Where the output carries a
feature **a later minor defines** and this compactor does not". §10.3:
"Experimental values are private use".

Severity: editorial. Consensus PARTIAL — the imprecision is real, the
conclusion the reporter draws (that the closure argument needs a silent
restriction) is answered by the antecedent.

### D2. `reserved-range-row-citation` — register-06, adversary-01, quiz-04

The parenthetical "(F36, L25, R1)" against §10.2's eight numeric spaces.
Verified against §21.2/§21.3/§21.5: reserved-range values in the other spaces
are registered as L31 (index encoding), L33 (linearization), L34 (sample type),
L36 (channel layout 3–255), L43 (codec), L45 (filter). Six rows omitted.

adversary-01 adds a sharper reading: if "such a file" is the compactor's
**output**, then R1 does not belong at all — its Detector is *reader* and its
Detected cell "open (top-level); layer access (sub-record)", so a compactor
performing §19.1's open detects it, and [R-WRT-06]'s "MUST NOT emit a file
carrying a violation it has detected" plus §20.4's PE = 1 on type 0x0002 (no
drop available) force refusal. I checked R1's row: Detector *reader*, Detected
"open (top-level); layer access (sub-record)". adversary-01 is right on the
row's face.

So the citation is wrong under both readings: short by six under the
input reading, and wrong by one under the output reading.

**Implementer consequence.** adversary-01 names the real one: a reader who
takes the parenthetical as the inventory concludes a reserved-range codec or
sample type is unregistered (it is L43 / L34), or builds a compactor that
carries an encoding-0x40 metadata record into its output believing R1 to be a
survivable class. That second one is a live compactor bug, though [R-WRT-06]'s
own detection prohibition catches it for anyone who reads §20.5's opening
paragraph.

**Downgrade quotation:** §21.1: "each row *restates* its governing rule, and
where a row and the rule it cites diverge, **the rule governs**." Every omitted
row states its own condition in its own section; no rule is misstated.

Severity: register-bookkeeping. Repair: either name all eight spaces' rows or
replace the list with "§10.2's reserved ranges, each registered in §21" — and
decide whether "such a file" is the input or the output, which determines
whether R1 belongs.

### E. `s217-only-where-self-contradiction` — verifier-09, register-03, adversary-04

> §20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire; a change that reaches the decoded size **instead** is
> witnessed by T3 or T14 …

Three reporters, one sentence. The literal parse makes the second conjunct
necessary and the next clause supplies a witness with that conjunct false; the
word "instead" marks it as false. The scoped parse ("witnessed **by §21.4's
content rows** only where …") is the only one on which the sentence is true,
and nothing in the text marks that scope.

adversary-04's constructive check is good and I reproduced it: float32 →
float64 on a layer with a stored codec-1 tile leaves entry_length at 128 while
the derived decoded size becomes 256, so T14 fires from the index entry alone
with no structurally constrained byte in play.

**Implementer consequence.** A corpus builder or verifier author taking the
first clause at face value skips T3/T14 vectors for declaration changes. §21.7
corrects them three clauses later, which caps the damage.

**Downgrade quotation:** §21.1: "The subsections after §21.5 are not part of
the register and carry no rows". T3 and T14 are §21.4 rows with their own
governing rules; a verifier built from §21.4 checks them regardless.

Severity: editorial. Repair: re-scope the "only" explicitly, or restructure as
"The bar is witnessed where the affected tiles remain stored, as follows: …".

### F. `s217-misses-in-sample-offset-head` — register-04

§20.3 step 4's bar has four heads: padding positions and their content;
decoded size; **the byte offset of any sample within the decoded tile image**;
codec and filter. §21.7 walks heads 1, 2 and 4 and never head 3.

register-04's construction checks out against §14.2's table: interleaved,
`a` uint32 + `b` uint16 → `a` uint16 + `b` uint32. Q = Σ Bᵢ = 6 either way, so
P·Q is unchanged and T3/T14 are silent; codec/filter unchanged so the codec
rows are silent; no padding position and no bool channel so T2/T4/T5 are
silent. But Fᵦ = Σ Bⱼ for j < b moves 4 → 2, so every retained stored sample
decodes to a different value. A violated bar with no row firing, and §21.7
names only supersede-everything as the unwitnessed case.

**Implementer consequence.** Nothing changes in any implementation — an
unwitnessed obligation is unwitnessed whether or not the account names it.
The cost is to §21.7's standing as "the account, by class, of what fails"
detectability (§21.1), and to anyone auditing their vector set against it.

**Downgrade quotation:** §21.7's own framing — "What no check detects" — and
§21.1's "The subsections after §21.5 are not part of the register and carry no
rows". No check is imposed or removed.

Severity: editorial. Repair: add the head-3 class ("a change that alters a
sample's in-sample offset without altering any length or the codec is
unwitnessed").

### G. `s217-lists-a-should-as-witnessless` — writer-04, quiz-03

§21.7 ¶2 opens "A second set of obligations is omitted from the register
because a single file exhibits no witness of their violation", and lists among
them "the floor its version_minor SHOULD take". [R-CNF-12] already excludes it
on a prior ground: "Deviation from a SHOULD is not a violation **for this
purpose**: §21's register enumerates MUST-level conditions only." The purpose
named is register membership, which is the paragraph's subject. So the reason
given is true but inoperative, and calling a SHOULD deviation "their violation"
is the word [R-CNF-12] denies it.

**Implementer consequence.** writer-04 names it precisely: a verifier author
reads §21.7 as licence to hunt for the version_minor floor, which [R-CNF-12]
says it owes no search for ("A verifier owes no search for one"), or to report
it as a finding rather than an advisory, which [R-CNF-12] forbids.

**Downgrade quotation:** as above, [R-CNF-12] — and it is the same quotation
that neutralises the consequence, since a verifier reading §2.4 gets the right
answer.

Severity: editorial. Repair: split the sentence — the MUST belongs in the
witnessless set, the SHOULD is excluded by [R-CNF-12] and should say so.

### H. `s217-counts-two-of-four-trailer-obligations` — writer-03

§21.7 writes "§20.5's **two** obligations on a compacted file's trailer
([R-WRT-06])". [R-WRT-06] places four on the output trailer: a fresh file_id
("a new draw under §9.3's randomness advice, not merely a value compared
against the input's"), generation 1, the ignore-lane carry-forward, and the
version_minor floor. The first two are unwitnessed on exactly §21.7's own
ground — the output carries no record that it is a compaction output.

I checked writer-03's own counter-argument and agree with its rejection: the
paragraph's opening clause names [R-LIF-01] and [R-LIF-03] by identifier, and
[R-WRT-06] is neither; §21.7 cites identifiers precisely everywhere else.

**Implementer consequence.** writer-03's is right and small: a verifier author
reading §21.7 as complete concludes the fresh-file_id MUST is witnessed and
looks for a check that cannot exist. No emitted byte, no verdict.

**Downgrade quotation:** [R-WRT-06] itself states all four unambiguously —
"It MUST mint a fresh file_id for the output … and generation 1". Nothing turns
on §21.7's accounting.

Severity: editorial.

### I. `s217-omits-appender-ignore-lane` — register-05, adversary-06

§21.7 names §20.5's compactor carry-forward and not [R-CNT-08]'s identical
appender obligation: "An updater MUST copy forward unknown ignore-lane bits of
the file it modifies and MUST NOT clear them", restated at §20.3 step 6. It is
unwitnessed for the same reason — the live state carries one trailer, §9.7
walks the live state only, and a prior trailer is slack a reader "MUST NOT
interpret" (§5.2). Listing one half of a symmetric pair is visibly asymmetric.

register-05 records two further members ([R-LIF-02] step 3's re-pointed
directory region; [R-LIF-04]'s truncation obligation) so they need not be
re-derived. adversary-06 adds [R-CNT-26]'s appender floor, the SHOULD-side
twin.

**Implementer consequence.** adversary-06 names the concrete one: an
implementer auditing §21.7 for untestable writer obligations finds the
compactor case listed and the appender case absent, writes a vector for
"appender clears an ignore-lane bit", and cannot state its expected outcome,
because the output is conforming. [R-VEC-02] then classifies that as "a finding
against this document rather than a vector".

**Downgrade quotation:** [R-CNT-08] states the appender's obligation in §6.3
and binds it whether or not §21.7 lists it; §21.1: the subsections after §21.5
"carry no rows".

Severity: editorial.

### J. `conduct-rule-taxonomy-for-carryforward` — verifier-04, quiz-05

Both construct the same witness pair: bytes B, well-formed, generation 1,
flags = 0. A creator emitting B satisfies §6.3. A compactor that produced B
from an input carrying ignore-lane bit 20 has violated [R-WRT-06]'s "The output
trailer MUST copy the input's unknown ignore-lane flag bits forward". §2.3:
"File conformance is a pure predicate on bytes: it does not depend on any
reader, writer, or environment." B cannot be both; B is conforming; so the
carry-forward binds conduct.

Where I part company with both reporters: they say [R-CNF-02]'s enumeration
is incomplete. Read carefully, that clause enumerates something narrower —
"A writer obligation whose violation this specification **expressly declares**
not to be a file-conformance violation binds the actor in the same way; §6.3's
flags = 0 … and §6.2's pre-trailer gap … are the cases this text states." It
is a list of *express declarations*, and there are exactly two. The defect is
that no express declaration exists for the compactor's carry-forward while
§21.7 files it under "no witness", which is the vocabulary used for file
properties like [R-LIF-01]. A taxonomy mismatch, not a miscount.

There is a further defensible reading I could not close: "§6.3's flags = 0
against a set ignore-lane bit" might be meant to cover the whole of §6.3's
flags material, [R-CNT-08]'s compactor sentence included. Nothing marks it
either way.

**Implementer consequence.** None to any implementation: the compactor is
bound by the MUST under either taxonomy, and no verifier can distinguish B's
two provenances. quiz-05 states the real one — whether a tool may truthfully
report "this compacted output is a conforming file" after dropping the input's
flags. It may.

**Downgrade quotation:** §2.3, the pure-predicate sentence above, which
already settles B's status.

Severity: design-decision. Consensus PARTIAL (the reporters' framing of *which*
enumeration is short does not survive; the taxonomy gap does).

### K. `appendix-g-modulo-trailer-vs-drop-licence` — reader-03, adversary-03

Item 8: "A compactor's output is therefore reproducible only modulo its
trailer". §20.4's MU = 0 / PE = 0 row: "A compactor MAY drop it whenever it
rewrites the file" — unconditional, unlike the appender's independent-change
test. Reachability checked: §7.3 registers only two types and both carry PE = 1
(so an MU = 0 / PE = 0 record must be of an unassigned type), reserved-range
types are violations (F36, L25), and §21.6 records an experimental-range MU = 0
record as conforming. So the input is reachable.

Two profile-adopting compactors on that input differ in the record sequence,
dir_length, the directory CRC, every offset after the directory, and the
dropped extent's bytes. None of that is the trailer.

reader-03 additionally swept items 1, 3, 5, 6, 7, 9, 10 for the same leak and
found them inherited from the input rather than chosen, on the strength of
[R-WRT-07]'s closed exception list. I spot-checked items 3 (pins record order,
not the record set) and 9 (user-metadata serialization, carried verbatim by a
compactor) and agree the drop licence is the only leak. adversary-03 reaches
the same result independently and checks the closing paragraph's inventory,
which does not mention the drop licence either.

**Implementer consequence.** An adopter builds a content-addressed pipeline
believing the compactor need only be pinned for eight trailer bytes, and finds
two pinned compactors disagreeing structurally.

**Downgrade quotation:** Appendix G's own opening — "It adds no requirement to
any actor: a writer ignoring it is fully conforming" — and [R-CNF-01], which
makes appendices identified as non-normative non-normative. Both outputs are
conforming files and §20.4's MAY is unambiguous.

Severity: design-decision — the maintainer must choose between adding a fixed
drop policy to the profile and widening the concession.

### L. `appendix-g-item6-unmarked-creator-rule` — verifier-03

Items 2 and 8 mark their creator-only halves; item 6 ("The sentinel for every
all-fill tile") does not, and a compactor cannot obey it. Checked: [R-WRT-07]
requires "every stored tile's bytes verbatim — each index entry's crc is
unchanged" and "entry lengths, entry crcs, and sentinel entries unchanged", so
converting a stored all-fill tile to a sentinel changes both length and crc;
and dropping is unavailable, §20.5 licensing drops only for records §20.4's
table names, "a tile-index entry being no record §20.4's table licenses
dropping".

**Implementer consequence.** Real and named: an implementer writes a
profile-adopting compactor that sentinels all-fill tiles, violating a normative
MUST in pursuit of a non-normative appendix. Marking costs one clause.

**Downgrade quotation:** [R-CNF-01] plus Appendix G's self-disclaimer, as in K;
and [R-WRT-07]'s "The output's reference arrays MUST equal the live
generation's bit for bit", the paragraph's operative MUST, which outranks the
appendix.

Severity: editorial.

### M. `appendix-g-closing-vs-item8` — register-07

Item 8: "The version_minor floor binds a compactor too, save where its output
carries a feature it does not implement". Closing paragraph: "`version_minor`
at its floor, which `[R-CNT-26]` states as a SHOULD — item 8's creator's rule,
not a compactor's (§20.5)". Direct contradiction, and it reads as though the
two halves of item 8 were swapped: the flags half *is* the creator's rule.

**Implementer consequence.** An adopter deciding whether a profile-claiming
compactor must put version_minor at [R-CNT-26]'s floor gets opposite answers
from two paragraphs of one appendix.

**Downgrade quotation:** the closing paragraph disclaims itself — "Read the
numbered items as the list; this paragraph names what they are for, not how
many there are." Item 8 governs.

Severity: editorial.

### N. `wrt07-regeneration-trigger` — reader-04

"regenerates each **relocated** tile-index region (entry offsets new; …)".
The trigger that matters is the tiles moving, not the region moving. A
compactor's packing arithmetic can land a region at the offset it already held
while every tile it addresses has moved; under the letter that region is not
regenerated and its entries keep offsets into slack. The Example states the
real trigger — "since its entries carry the offsets that moved" — and is
labelled Example, hence non-normative under [R-CNF-01].

**Implementer consequence.** A latent correctness bug whose reachability is a
function of the compactor's own packing, and which its own pipeline cannot
catch: [R-WRT-09]'s verification runs over the **input's** chain before
emitting, not over the output. That is the class of bug that appears in
production and never in a test — the sharpest practical point in this batch,
even though no conforming implementation can diverge.

**Downgrade quotation:** [R-WRT-07]'s closing MUST — "The output's reference
arrays MUST equal the live generation's bit for bit (`[R-MDL-02]`)" — together
with [R-CNF-05], "A writer MUST emit only conforming files". A region with
stale entry offsets yields entries whose stored bytes fail their crc or address
the wrong bytes, so the output is nonconforming and reading (a) is not a
reading available to a conforming compactor. The emittable set is identical.

Severity: editorial. Repair: "regenerates each tile-index region any of whose
entries change — every region of a layer any of whose stored tiles moved".

### O. `wrt07-preservation-lacks-a-must` — quiz-01

The one self-flagged byte-level finding. Claim: §2.1 binds BCP 14 keywords
"when, and only when, they appear in all capitals", the preservation clause
carries none, therefore a compactor may re-encode every tile so long as the
reference arrays match.

I take this seriously and it does not survive, on three independent grounds.

1. **[R-CNF-01] settles normativity, not [R-CNF-01]'s all-caps neighbour.**
   "All text in this document is normative except: §1 (Introduction); any text
   labeled *Note*, *Example*, or *Rationale*; and appendices identified as
   non-normative." §20.5's second paragraph is none of those and carries a
   requirement identifier, which §2.2 says is what a normative requirement
   carries. The RFC 8174 sentence governs how the listed *key words* are
   interpreted where they appear; it does not make unkeyworded normative text
   advisory.

2. **The reading unravels the register.** [R-CNT-02] ("Every byte of the live
   committed state belongs to exactly one of … No two of them overlap"),
   [R-SER-01] ("Every tile serializes a value sequence"), [R-SER-02] (the
   decoded-size table) and [R-MTA-03] ("is a validity error at the record's
   containing scope") carry no all-caps keyword either, and F33, T3, T14 and
   F23 are register rows built on them. Reading B would leave those rows
   without governing rules.

3. **The document states the answer elsewhere, in a MUST-bearing normative
   requirement.** §23.2, [R-PRV-04]: "`[R-WRT-07]` **preserves every stored
   tile's bytes and every index entry's crc bit for bit**, so a compacted file
   remains trivially correlatable with its input by content." If reading B were
   available, [R-PRV-04] would be false. And [R-WRT-07]'s own parenthetical
   says "entry lengths, entry **crcs**, and sentinel entries **unchanged**",
   which a re-encoding compactor cannot satisfy; [R-WRT-09] obliges it to
   verify "every stored tile's entry crc … before emitting that structure's
   bytes".

The premise my downgrade rests on, stated for attack: **a normative declarative
sentence carrying a requirement identifier binds, and §2.1's all-caps clause
governs only the interpretation of the eleven listed key words, not whether a
sentence creates an obligation.** If that premise falls, this is byte-level and
so is a large part of Part I.

What is nonetheless real: the paragraph reaches for MUST one sentence later and
not here, and the obligation it states is load-bearing for [R-PRV-04] and for
Appendix G's reproducibility claims. Consensus PARTIAL — the title's literal
claim (no MUST-level keyword) is true; the inference (that reading B is live)
is not.

Severity: editorial. Repair: "every stored tile's bytes MUST be carried forward
verbatim, and each index entry's length and crc MUST be unchanged".

### P. `s204-drop-licence-does-adding-count` — writer-05

The row says explicitly that adding counts for the layer limb — "A commit
changes the layer set by adding a layer; an appender never removes one" — and
says nothing for the top-level limb, whose three triggers are "the file's layer
set, any layer record's content, or another *non-layer* top-level record". It
closes the neighbouring hole for drops ("Dropping the record, or dropping
another record in the same commit, is not itself such a change") and not for
adds.

Reachability checked as in K: an experimental-range MU = 0 / PE = 0 top-level
record in a conforming file, and a commit whose only effects are to add a
file-scope user-metadata record and drop the experimental one.

**Implementer consequence.** Two conforming-looking updaters, one commit
request: one emits a directory without the record and lets its extent fall to
slack, the other re-emits it byte-identically under [R-WRT-05]. The files differ
in dir_length, in every offset after the directory, in F, and in the verifier's
slack total. The user-visible difference is data loss.

**Downgrade quotation, and the premise it rests on:** both outputs are
conforming files — [R-CNF-05]'s gate is file conformance, and neither file
carries a violation — and the drop licence binds an updater's conduct across
two files with no witness in either, exactly as [R-LIF-01] and [R-WRT-06]'s
fresh file_id do (§21.7 ¶2, §2.3's conduct carve-out). This is the group where
Premise D is doing the most work: if a witnessless producer fork counts as
byte-level, this is byte-level.

Severity: design-decision. Repair: state the top-level limb's treatment of
additions as the layer limb's is stated — one clause, either direction.

### Q. `partial-slack-total-at-file-scope` — verifier-01

Checked §5.2's clause. It states the general rule at scope generality ("a
scope-level rejection ends that scope's enumeration") and works the layer case
in a parenthetical, including the discard rule. But it then states the
arithmetic flatly, and the arithmetic decides the file case:

> A partial total is **F less the bytes claimed by the claimants the walk did
> enumerate** — an upper bound on the file's true slack, never an under-count

That is the reporter's reading (3). The discard rule that would produce reading
(1) is expressly scoped: "the claimants it had already enumerated are discarded
**with the layer**". And reading (2) (the total is exact) is foreclosed by the
same sentence plus the MUST to "say which scope or violation stopped the walk".
So on the reporter's own two-layer file the answer is 47, not 704.

**Implementer consequence.** None, once the arithmetic sentence is read. The
reporter implemented reading (3) and is right. The residue is that the general
clause's "ends that scope's enumeration", applied at file scope, reads as
though it also discards — the discard rule sits inside a layer-scoped
parenthetical and could be mistaken for a general one.

**Downgrade quotation:** the arithmetic sentence above, plus "discarded with
the layer". Verdict is nonconforming either way (§2.3, "An established
violation takes priority").

Severity: editorial. Consensus PARTIAL — a wording risk, not three live
readings.

### R. `s217-disclaimer-placement` — verifier-02

The "None of these" disclaimer closes ¶1 (content-incorrectness); ¶2 introduces
the larger list with no disclaimer of its own. The reporter's narrow reading
would make *conforming* unreachable for any file with a stored tile.

The narrow reading is closed by §2.3's definition of the verdict itself:

> a verifier reports one of three verdicts … the last where some requirement is
> one it is **unable to check on a capability or resource ground**

[R-GEO-06]'s and [R-SER-01]'s ordinal mappings, [R-CNT-13]'s and [R-CNT-18]'s
prohibitions are not capability or resource grounds; the grounds §2.3 goes on
to enumerate are a foreign major, an unimplemented MU = 1 type, an unexecutable
codec, a declined decode, a declined metadata document. So *cannot establish*
is not available for §21.7 ¶2's members, disclaimer or no.

**Implementer consequence.** None. A verifier built from §2.3's own definition
of its verdicts never reaches the narrow reading.

Severity: editorial. Consensus REFUTED as to the ambiguity; the placement
observation is fair and cheap to fix (move or repeat the disclaimer).

### S. `verifier-owes-no-violation-report` — verifier-05

I re-assembled the reporting duties and agree with the inventory: unchecked
requirements by name and ground, unexamined scopes, the slack total with what
stopped the walk, [R-MTA-10]'s three fields, [R-ERR-04]'s limit-vs-corruption
distinction, [R-MTA-09]'s bound; and exactly one general duty to name a
violation, [R-MTA-05]'s. A verifier whose whole output is "nonconforming"
satisfies the document.

**Implementer consequence.** A conforming verifier can be useless for §22.3's
job. But the corpus is not blocked: [R-VEC-04] makes a vector's expectation a
pair of *served content* and *refused scope* — "the scope no reader is
permitted to serve and the content a reader that serves anything at all owes" —
which a harness checks against behaviour, not against report strings. So the
reporter's [R-VEC-02] argument overreaches.

**Downgrade quotation:** §2.4's Note — "'Reject' prescribes the scope of
unusability, not user interface: how failure is reported is implementation
technique" — and §2.1's Note, "requirements constrain bytes and observable
behavior, never implementation technique."

Severity: design-decision. Consensus PARTIAL — the asymmetry is real, the
corpus consequence is not.

### T. `unassigned-type-extent-unnamed` — verifier-06

Verified §8.1's last row via §7.2's opacity and §22.3's own sentence: "The
extent of a record of a type this specification has not assigned is covered by
no checksum either (§8.1), so corruption inside it is equally invisible."
[R-MTA-10] imposes a naming duty for the analogous metadata case ("bytes a
certificate covers without inspecting are counted and named, never silent") and
nothing imposes one here. Appendix H's verifier checklist likewise names the
metadata report only. The reporter is right that this is decidable, not
ambiguous: no duty exists.

**Implementer consequence.** A certificate covers an arbitrary, unchecksummed,
uninspected, unmentioned byte range of any size — the smuggling channel §22.3
tells an operator to police "on that report line", for the residue that has
one. Nothing an implementation does is *wrong*; what is missing is a duty.

**Downgrade quotation:** §21.6 — such a record is "Ignored, and preserved or
dropped per its PE bit"; the file is conforming and the verdict identical
whether or not the extent is named.

Severity: design-decision — extending [R-MTA-10] is a maintainer's call.

### U. `s204-table-has-no-identifier` — diagrams-02

Verified mechanically: between [R-WRT-05] closing §20.4 ¶1 and [R-WRT-08]
closing the re-encode paragraph, the table-introducing paragraph, the table,
and "No commit therefore removes a layer record…" carry no closing identifier.
The table states at least three MUSTs. §2.2: "Normative requirements carry
identifiers of the form `[R-<PREFIX>-<NN>]`."

The wrong-citation consequence checks out. §21.6's row for an experimental-range
MU = 0 record gives the behaviour "Ignored, and preserved or dropped per its PE
bit" and cites [R-CNT-15], [R-WRT-08]. [R-WRT-08] reads in full: "An updater
MUST NOT re-encode a record whose type it does not implement, and MUST NOT
modify one except by relocating its extent and re-pointing its slot under
§20.5." It says nothing about PE disposition. §20.4's unidentified table does.

**Implementer consequence.** None to the bytes; the obligations are reachable
by section, which is how [R-CNF-06], §2.4's preserve-verbatim row, §20.5 and
Appendix H already reach them. The cost lands on [R-VEC-02], which requires a
vector to cite "that row's governing requirement identifier … while §2.2 makes
the identifier permanent" — and there is none to cite.

Severity: register-bookkeeping. Repair: assign an identifier to §20.4's table
(and, as diagrams-02 notes, to §6.1's "Writers MUST emit exactly these 16
bytes").

### V. `f5-vs-foreign-major-preamble` — diagrams-03

The preamble's reason is an ordering argument about §6.2's gate sequence.
[R-CNT-27] is not one of §6.2's gates — it is a check on physical size, and
§19.1 step 1 obtains F before the trailer is fetched at step 2. F5's row lists
"F (physical file size)" as an instance and its Detected cell is *open*. So for
that instance the version gate is behind, not ahead, and the preamble's
conclusion does not follow from its stated reason. I confirmed the witness is
constructible: at F = 80 with a valid trailer at [16, 80) and version_major = 7,
every later gate (dir_offset ≥ 16, dir_offset + dir_length ≤ F − 64,
F mod 64 = 0) sits behind the version gate and is never reached.

**Implementer consequence.** Two verifiers, same 80 bytes: one reports
*nonconforming*, one *cannot establish*. Both refuse; neither certifies. §6.3
asks for the diagnostic to be distinct precisely because confusing the two
"misleads users into discarding files that current software reads", so the
divergence is not cosmetic — but it is not accept/reject.

**Downgrade quotation, and it also decides the outcome:** §2.3 — "a file
declaring another major is neither conforming nor nonconforming under it: a
reader refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and
**that refusal is not a finding about its bytes**." A verifier reporting
*nonconforming* contradicts that sentence directly. So reading (a) governs and
the ambiguity is closed; what is defective is the preamble's reason and F5's
unlisted status among the exceptions.

Severity: register-bookkeeping. Repair: add F5's physical-size instance to the
four exceptions with its own reason (it is not a geometry claim about a
major-1 file but a floor derived from major-1 fields), or say in §5.1 that the
128-byte floor is applied after the version gate.

### W. `appendix-h-reader-entry-too-wide` — diagrams-04

§2.3's acceptance duty carries three qualifiers; Appendix H's reader entry
keeps one. The two dropped are exactly the two §21.6's closing paragraph is
about, and [R-ERR-04] carries the carve-out verbatim: "the two capability
refusals §21.6 names, a foreign format major and an unimplemented MU = 1 type,
are not this ground".

**Implementer consequence.** An implementer auditing against the checklist —
which Appendix H says is its purpose — concludes that refusing a major-7 file
and rejecting an experimental MU = 1 record both make them nonconforming, when
the first is licensed and the second required.

**Downgrade quotation:** Appendix H's own opening — "each entry's authority is
the requirement or section cited, never this summary" — plus [R-CNF-01] making
it non-normative.

Severity: editorial. Repair: diagrams-04's own clause, "save the two capability
refusals §21.6 names".

### X. `s182-valid-values-cell` — diagrams-05

The cell reads "1 or 2; see below" in a column that elsewhere means "or the
file is invalid". §18.2's encoding byte is the one enumerator in the document
whose unassigned values leave the file conforming. §6.2's version_major cell
hedges inside the cell — "1 (0 invalid; others: §6.3)" — which is good evidence
the trap was seen elsewhere.

**Implementer consequence.** A verifier written from the box alone reports
*nonconforming* for encoding 0x85 and refuses to certify, where §21.6 and
[R-MTA-10] require it to certify and report the record. But the box does not
stand alone.

**Downgrade quotation:** the cell itself says "1 or 2; **see below**", and the
sentence four lines down: "Field values: 0 is invalid; 1 = none and 2 = zstd
are assigned; 3 through 0x7F are reserved; values ≥ 0x80 are the experimental
range (§10)." §10.3 adds "never a scope-level rejection"; §21.6 has a dedicated
row; [R-MTA-10] a paragraph.

Severity: editorial (a table cell — could be graded *figure*; I grade the
content, not the presentation). Repair: diagrams-05's parenthesis.

### Y. `mu1-subrecord-refusal-scope` — register-02  **[BYTE-LEVEL]**

This is the one I am upgrading against its reporter.

The texts:

- §21.6 closing: "The second is an **experimental-range record type carrying
  MU = 1** (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject" — no
  placement qualifier.
- [R-CNT-15]: "An unknown record type **at file scope**: MU = 1 → reject-file".
- [R-CNT-18]: "an unknown sub-record type with MU = 1 is **reject-layer —
  never reject-file** — and with MU = 0 is ignore-record."
- §10.3: "for record types, the MU-bit outcome of `[R-CNT-15]` **at file
  scope** and `[R-CNT-18]` **for layer sub-records**".
- §20.4's table: "At layer scope an unknown critical record blocks modification
  of that layer, leaving other layers editable ([R-CNT-18]). At file scope no
  commit is available at all."
- §2.3, [R-CNF-03]: "A reader MUST accept every conforming file of a format
  major version it implements, **carrying no record of a type it does not
  implement with MUST_UNDERSTAND = 1** … (§21.9's [R-ERR-04] governs a refusal
  on that last ground; **§21.6's closing paragraph names the other two**)."

Now the concrete pair of implementations. File: conforming, layers X and Y,
Y's layer record carries a sub-record of experimental type 0x8001 with MU = 1.

- **Reader A** builds from [R-CNT-18], §10.3 and §20.4: rejects layer Y,
  serves X's samples, lists both layers. §2.4's reject-layer row: "all other
  layers are unaffected."
- **Reader B** builds from §2.3 and the paragraph §2.3 designates: the
  acceptance duty is relieved — the relief clause says "record", and
  [R-CNT-18] says "Sub-records are layer-scope records", so it is scope-blind
  — and §21.6 calls this a conforming file "a reader nevertheless refuses".
  Reader B refuses the whole file and serves nothing.

One byte sequence; one implementation accepts it (serving layer X), one
rejects it. That is the second half of the byte-level test on its face.

Why the usual escapes do not apply here:

- **[R-CNF-12]'s whole-file licence is unavailable.** It reads "For a
  **nonconforming** file no acceptance obligation exists — a reader MAY reject
  it upon detecting any violation." This file is conforming. §24's Note leans
  on exactly that licence to excuse a whole-file refusal against a
  reject-layer vector, and says so: "an implementation that instead rejects the
  whole **nonconforming** file is exercising `[R-CNF-12]`'s licence". No such
  licence exists for a conforming file.
- **The relief in [R-CNF-03] is not the same as a permission to reject-file**,
  and [R-CNT-18] states a flat prohibition on the other side — "never
  reject-file". Under the same premise I used to uphold [R-WRT-07] in group O
  (an unkeyworded normative sentence with an identifier binds), [R-CNT-18]'s
  "never reject-file" binds, and Reader B is nonconforming. Under quiz-01's
  premise it does not bind and both are licensed. Either way the document does
  not decide the case the same way in two places.
- **The tie-break does not reach it cleanly.** §21.1: "§21.6's entries restate
  their governing rules on the same terms a row does, and where such an entry
  and the rule it cites diverge, the rule governs there too." The closing
  paragraph is prose after the table, and register-02 is right that the
  tie-break is written for entries. Even granting it, the rule cited is
  [R-CNT-15], which is silent on sub-records — so the paragraph is left
  asserting a file-wide refusal with no rule behind it, which is worse than
  divergence, not better.
- **[R-VEC-04] is built on this exact distinction** — "the pair is the scope no
  reader is permitted to serve and the content a reader that serves anything at
  all owes … Without the sibling a vector cannot distinguish a reader that
  scopes its refusal from one that rejects the file entire." The corpus exists
  to test the thing this paragraph makes ambiguous.

Where I think register-02's own byte-level analysis goes wrong: it argues both
behaviours are licensed and therefore nothing is forced apart. But "both
licensed" is itself the defect when the two behaviours are *accept this file*
and *reject this file*, and when [R-CNT-18] says one of them never happens.
A specification that licenses both has not decided whether a conforming reader
must accept these bytes.

register-02's secondary point is also correct and I fold it into the repair:
the paragraph's stated reason for neither case being a register row — "the
register enumerates file-conformance violations (§21.1), and a file this
document declines to judge is not one" — covers only the first case. The
second case's file is judged, and judged conforming; it is not a row because it
is not a violation.

**Repair (concrete).** (i) In §2.3, qualify the relief: "carrying no
**top-level** record of a type it does not implement with MUST_UNDERSTAND = 1",
and add that an unimplemented MU = 1 **sub-record** is reject-layer
([R-CNT-18]) and does not relieve the acceptance duty for the rest of the file.
(ii) In §21.6's closing paragraph, qualify the second case as a **top-level**
experimental-range MU = 1 type, cite [R-CNT-18] for the sub-record case, and
correct the "declines to judge" reason for that case. (iii) Optionally add the
sub-record case to §21.6 as its own entry, since it is a defined non-violation
with a defined outcome.

Severity: **byte-level**.

### Z. `r6-r10-governing-rule-cells` — register-08

§4.6's [R-ENC-12] states all three key constraints; §18.2's [R-MTA-04] restates
them. R6 (empty key, C0 code point) cites [R-CNT-25] first; R10 (key over 255
bytes) cites [R-MTA-04] first; neither names [R-ENC-12]. §21.1 fixes the cell's
meaning: "A Governing rule cell names that requirement first" — the requirement
that defines the condition — "any identifiers following it in parentheses are
the further rules the condition reads."

[R-CNT-25] defines no key constraint; it is the quarantine that assigns the
outcome, and §21.1 already accounts for that separately ("except where a rule
assigns one expressly, as `[R-CNT-25]`'s quarantine does for every §21.5 row").
So naming it *governing* on R6 conflates the two roles the same paragraph
distinguishes. Verified the R5/R7–R9 split the reporter describes: four rows
name [R-MTA-04] first, two name [R-CNT-25] first, over one four-restriction
rule.

**Implementer consequence.** None to any reader or verifier — same condition,
same outcome, same detector, same detection point. The cost is to a corpus
indexed by governing identifier under [R-VEC-02], where [R-ENC-12]'s three key
constraints appear under two other identifiers and never under [R-ENC-12].

Severity: register-bookkeeping.

### AA. `s211-has-no-identifier` — register-09

§21.1 states the register's extent, its normative completeness, the row-vs-rule
tie-break, the Detector/Detected semantics and the Instances arithmetic, and
carries no identifier, while §21.7–§21.9 each carry theirs. Verified that
[R-ERR-02], which §21.1 cites in its first line, is §21.8's corpus-coverage
requirement and states none of those things. Verified the prose-position
citations: §19's preamble ("at the tier that row's *Detected* cell names
(§21.1)") and [R-VEC-04] ("no reader is obliged to refuse anything (§21.1)").

The reporter's own counter (a rule binding the document rather than an actor is
arguably not a requirement) is fair for the completeness clause and does not
reach the tie-break, which binds every reader, verifier and corpus builder that
meets a divergence.

**Implementer consequence.** None to behaviour. [R-VEC-02] requires a vector to
name "that row's governing requirement identifier", and a vector exercising
§21.1's tie-break or its instance arithmetic has none to name.

Severity: register-bookkeeping. Distinct from group U (a different section, a
different repair), though the two share a cause.

### AB. `step4-criterion-vs-gloss-on-type-change` — adversary-05

Construction: one int32 channel, interleaved, codec 1, filter 1, no padding
positions, storing tiles; re-declare as float32. I checked every head of
§20.3 step 4 against §14: element size 4 → Q unchanged → decoded size P·Q
unchanged; every sample's byte offset unchanged; padding-position set empty
either way; codec and filter unchanged; [R-CNT-23]'s fill length 4 either way.

The document decides this, and more clearly than the reporter allows.
[R-MDL-02]: "sample values are bit patterns, and decoding MUST NOT alter them
(floating-point payloads included; **type semantics are §12's subject**)."
[R-TYP-04]: "A sample value is its bit pattern." So the reference array is
bit-identical across the change, and §14 — which fixes the value sequence, the
byte layout, the decoded size and each value's offset — fixes nothing that
moves. The bar quantifies over "what **§14** fixes for its stored bytes or how
they decode", and §14 does not fix type semantics; §12 does.

The gloss is what invites reading (b), and the reporter's analysis of it is
right: it is introduced as a narrowing device ("the list names where that
effect arises rather than standing on its own"), its two examples are both
cases where a listed item is touched to no effect, and its verb phrase is "is
not what this bars". A device that only subtracts cannot add a case.

The reporter's neighbouring uint8 → bool case is decided the other way and I
agree: [R-SER-08] makes the byte's content a thing §14 fixes, so the change
retroactively makes stored bytes like 0x7F nonconforming, and §21.7 names "a
boolean byte" as the witness.

**Implementer consequence.** Under (b) an appender refuses a legal in-place
reinterpretation and forces a whole-file rewrite of a large layer. Under (a) it
performs a commit that silently changes every sample value a consumer sees with
no diagnostic and no witness. That is a genuine fork in appender behaviour and
the most consequential of the witnessless-conduct group.

**Downgrade quotation, with Premise D:** [R-MDL-02] and [R-TYP-04] above decide
it in favour of (a); and even if they did not, §21.7 places §20.3 step 4's bar
among the obligations with no live-state witness, and both outputs are files a
creator could have written from scratch — so neither the conforming set nor any
verdict moves. If Premise D falls, this is byte-level alongside P and O.

Severity: design-decision. Consensus PARTIAL — the criterion is not silent, but
the gloss's "meaning exactly what they meant" is the wrong phrase for a
bit-pattern format and should say "leaves every one of §14's quantities and
every stored byte's §14 obligation unchanged".

---

## Coverage check

44 input ids, 29 groups. Counted by reporter: reader 5, writer 5, verifier 9,
diagrams 5, register 9, adversary 6, quiz 5 = 44. Counted by group:
6+2+2+1+3+3+1+2+1+2+2+2+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1 = 44. No id appears
in two groups; no id is dropped.

Byte-level count: 1 (register-02).
