# Round 17 — triage pass: CORRECTNESS lens

Working transcript. Verbatim notes, in the order I worked.

## What I read

Only `spec/tarn.md`, by section, plus `ls` of the round17 scratchpad directory
(to confirm the walk transcripts exist by name — the listing showed
`transcript-adversary.md`, `transcript-diagrams.md`, `transcript-quiz-*.md`,
`transcript-reader.md`, `transcript-register.md`, `transcript-verifier.md`,
`transcript-writer.md` and some build scripts; **no `transcript-triage-*.md`
appeared in that listing and I opened none**). I opened no walk transcript
either — every claim below is checked against the specification text directly.
No `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`registry.json`, no git history, no web.

Sections read in full or in relevant part: §2.1–§2.4, §3.x (terms via grep),
§5.2, §6.1–§6.4, §7.4 (grep), §9.1–§9.5, §10.4, §11.1–§11.3, §13.3, §14.3,
§14.4, §14.5, §15.3, §15.4, §17.2 (codec cap + Note), §18.2, §19.1–§19.4,
§20.1–§20.5, §21.1, §21.2 (head), §21.4, §21.5, §21.6, §21.7, §21.8, §21.9,
§24, Appendix G, Appendix H.

## Grouping (34 ids → 17 groups)

| group | ids |
|---|---|
| shrink-bar-quantifier | reader-01, writer-03, verifier-01, diagrams-01, register-01, adversary-03, quiz-01 |
| compactor-refuse-vs-reproduce | reader-02, writer-02, verifier-02, register-03, adversary-01 |
| drop-licence-modifying-layer-record | writer-01, verifier-03, adversary-02, quiz-02 |
| removing-a-layer-dead-branch | reader-04, diagrams-03, register-05 |
| metadata-preamble-resource-decline | writer-05, adversary-04 |
| metadata-preamble-exception-scope | reader-03 |
| t3-reads-decoded-image | register-02, quiz-04 |
| barriers-absent-from-21-7 | writer-04 |
| appendix-h-pad-bits | diagrams-02 |
| shrink-sentence-fill-carveout | diagrams-04 |
| shape-c-widens-redeclaration | diagrams-05 |
| §21.1-has-no-identifier | register-04 |
| err-04-unqualified-sentence | register-06 |
| reproduced-entry-not-stable-under-F | verifier-04 |
| profile-file-id-fallback | writer-06 |
| profile-emission-order-domain | quiz-05 |
| local-remote-nothing-else | quiz-03 |

7+5+4+3+2+1+2+1+1+1+1+1+1+1+1+1+1 = 34. Counted twice, by hand.

---

## Group 1 — §11.1's Rationale quantifies the shrink bar over the new state

Seven reporters. Every quotation checks out.

§11.1, lines 1481-1488, is a `> **Rationale.**` block:

> "§20.3 states normatively, and governs, what a commit may do to a layer that
> already stores tiles: a shrink is barred wherever it alters what §14 fixes
> for a tile the new state still stores, and permitted where it drops tiles out
> of the addressed set, whose extents then become slack. A layer that stores
> nothing may be re-declared freely."

§20.3 step 4, lines 2989-3001:

> "the bar above is the whole of the test, **in the bar's own tense**: a shrink
> is permitted exactly where it alters nothing §14 fixes for any tile the layer
> stores in the generation this commit supersedes. Dropping a tile out of the
> addressed set … is not itself such an alteration … but neither does it rescue
> a commit that damages a prior-generation stored tile. Unstoring that tile in
> the same commit does not rescue it either … the quantifier is the superseded
> generation's, so a shrink that turns real positions into padding of a tile
> stored there is barred whether or not the new state still stores it."

Both halves of §11.1's sentence are wrong in the same direction, and the
reporters between them catch both: the bar's quantifier (new state vs superseded
generation) and the de-addressing clause stated as a flat permission where
§20.3 states it as "not itself such an alteration — but neither does it rescue".
Same sentence, same repair. One group.

**Downgrade, and the sentence that decides it.** [R-CNF-01], §2.1:

> "All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative."

Line 1481 opens `> **Rationale.**`. So the passage is non-normative, and it
additionally defers by name ("§20.3 states normatively, and governs").

Testing the downgrade against a construction the reporters did not pick, per the
round-16 lesson: my premise is *not* a claim about the disputed file (I am not
relying on §21.7's unwitnessedness), so the "unstored in the new generation"
escape does not touch it. I checked the other direction anyway —
diagrams-01's construction (b), where the shrink damages a tile the new state
*does* still store (E=8,T=4 → E=3; tile 0's position 3 turns to padding holding
non-fill). There §11.1's second clause ("permitted where it drops tiles out of
the addressed set") would license a commit whose output carries a live T4. But
the output is decided nonconforming by [R-SER-05]/T4 under both readings, and
[R-CNF-05] ("A writer MUST emit only conforming files") bars it independently
of §20.3. So no verifier verdict and no emission permission forks in that
construction either. Downgrade holds.

CONFIRMED, not byte-level, editorial.

---

## Group 2 — §20.5: [R-WRT-06] refuse vs [R-WRT-07] reproduce

Five reporters; three flagged byte-level, two downgraded. This is the one I
spent the most time on. I checked every load-bearing premise.

[R-WRT-06], lines 3157-3164:

> "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
> fails, and MUST NOT emit a file carrying a violation it has detected … Where
> the table does not license a drop the compactor MUST refuse."

[R-WRT-07], lines 3186-3194:

> "an entry §15.3 classifies reject-tile on a *structural* ground is reproduced
> with its offset and length exactly as they stand … and the violation travels
> with it into the output (`[R-WRT-01]`); `[R-WRT-09]`'s checks reach the index
> chain and each stored tile's entry crc, not an entry's own value domain, so
> such an entry is not one `[R-WRT-06]` obliges a compactor to refuse"

Premises I checked:

1. *Is the [R-WRT-09] ground true as stated?* Yes. [R-WRT-09] (3242-3248)
   enumerates "the open (§19.1), each retained layer's record (§19.3) and full
   index chain (`[R-IDX-04]`), and each relocated extent's checksum, including
   every stored tile's entry crc". §19.4 separates step 3 ("Index chain … 
   `[R-IDX-04]`") from step 4 ("Entry. Classify per §15.3 (`[R-IDX-03]`)"), so
   "index chain" really is the CRC chain and not §15.3 classification. The
   reporters who said this ground is *false* are wrong; it is true.
2. *Does the compactor nevertheless detect?* Yes, and the document says so
   itself: [R-WRT-07] directs it to identify "an entry §15.3 classifies
   reject-tile on a structural ground", which is the classification §15.3
   ("a reader MUST classify as follows") assigns, and §2.3 makes updaters
   "readers of the files they process" who "inherit every reader obligation".
   T6–T12 are detector *reader*.
3. *Does the output carry the violation?* The document asserts it: "the
   violation travels with it into the output".

So limb 2's two antecedents — a violation detected, carried by the output — are
both asserted by the disputed passage itself. The carve-out's ground answers
limb 1's trigger ([R-WRT-09]'s check list) and not limb 2's (actual detection).

**Why I did not downgrade.** The best downgrade available is that the clause
"such an entry is not one `[R-WRT-06]` obliges a compactor to refuse" names
[R-WRT-06] whole and is the exact complement of limb 2, so it must dispose of
both limbs or be vacuous. I weighed that seriously and rejected it, for a
reason the document supplies: grammatically the clause is presented as an
*inference* from the [R-WRT-09] premise ("so X"), i.e. as a restatement of
[R-WRT-06]'s reach rather than a stipulation over it — and §21.1 states this
document's own principle for a restatement that misdescribes its rule:

> "each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**."

Applied by analogy (as diagrams-03 applies it, and as §10.4's [R-EXT-05]
applies it to the registry), the misdescription yields and [R-WRT-06] governs —
in which case [R-WRT-07]'s whole reproduction prescription is unexercisable.
There is no rule-versus-rule tie-break in the document to settle which way this
goes. Empirically it does fork: of five independent implementers reading the
same subsection, writer-02 and adversary-01 built refusing compactors,
reader-02, verifier-02 and register-03 built emitting ones.

Byte consequence: compactor A emits nothing; compactor B emits a complete
compacted file whose regenerated index region carries the malformed entry
verbatim. Resolving decides whether B's byte sequence may be emitted by a
conforming compactor at all ([R-CNF-06]). That is the byte-level test on its
face. Flagged byte-level.

adversary-01's second sharpening (a reserved-range MU=0/PE=1 top-level record,
F36) is a different mechanism and I did **not** treat it as a second defect:
limb 2 is conditioned on *actual* detection, F36's detector is the verifier, and
[R-CNF-04] imposes no reader obligation for a verifier row — so a compactor that
checks the range must refuse and one that does not may carry it forward, which
is licensed variation rather than ambiguity. Noted in the group's action.

---

## Group 3 — §20.4's MU=0/PE=0 drop licence and "modifying any layer's record"

Four reporters. Two frame it from the supersede side (writer-01, quiz-02) and
two from the store side (verifier-03, adversary-02). Same phrase, same repair,
one group.

Text (line 3121): "…for a top-level record, the file's layer set — which a
commit changes by adding or removing a layer and equally by modifying any
layer's record … Superseding a stored tile's bytes is not such a change for
either kind — it re-places that layer's index region (§20.3, `[R-WRT-04]`)
without altering the scope any record attaches to — so a commit whose only
change is a supersede MUST retain the record."

§20.4 opening (3099-3103): "every record it retains and does not **logically**
modify; a record it modifies is new output". The adverb appears there and not in
the licence clause.

*Supersede side (writer-01, quiz-02): partly answered by the text.* The carve-out
is an express exception that stipulates a supersede is "not such a change"; an
exception is not a contradiction, and it terminates in a MUST. So the supersede
case is decided.

*Store side (verifier-03, adversary-02): not answered anywhere.* A commit whose
only change is to store a previously-sentinel tile re-emits that layer's index
region "necessarily at a new placement" (§20.3 step 4), so the layer record's
extent slot and crc_of_crc_array change and the record is not re-emitted
byte-identically. Does that satisfy "modifying any layer's record"?

- For (a): §20.4's own retention test is byte-identity; and if "modifying" meant
  *logically* modifying, the supersede carve-out would be unnecessary, since a
  supersede is not a logical change either. Non-vacuity favours (a).
- For (b): the carve-out's stated reason — "without altering the scope any
  record attaches to" — is equally true of a store; and §20.3 step 4 treats "a
  layer whose record alone changes" as a distinct category.

I looked for a decider and found none. Note the fork is confined to a *top-level*
MU=0/PE=0 record: for a layer sub-record the list already names "which of its
tiles are stored", so a store licenses the drop under both readings.

Byte consequence: on the same input and the same instruction, updater X's new
directory omits the ancillary record's 24-byte header and inline payload and
updater Y's carries it; dir_length, the directory CRC, every later offset,
committed_file_length and the trailer CRC all differ, and both outputs are
conforming files, so no verifier corrects either. Which byte sequences a
conforming updater may emit forks. Byte-level.

---

## Group 4 — "removing a layer" is a dead branch

Line 3121 lists "adding or removing a layer"; line 3123 says "No commit
therefore removes a layer record, or a user-metadata record at either scope."
I checked every route: §7.3's registry fixes PE=1 for type 0x0001 (§20.4 says
so at 3107-3108, "both registered types carry PE = 1, so neither can be
dropped"); §20.5 "carries every layer of its input forward"; a whole-file
rewrite is not a commit ([R-LIF-01]). Unreachable branch. No file's bytes and no
verdict turn on it. CONFIRMED, editorial.

---

## Group 5 — §21.5's preamble omits §18.2's resource decline

Preamble (3484-3488): "every way its document can be unreadable takes this
outcome, whatever the containing scope — as a violation in the rows below,
except at an experimental-range encoding…".

§18.2 [R-MTA-09] (2460-2463): "a reader instead decodes with a bound of its own
choosing, no smaller than §21.9's user-metadata guarantee, and a document
exceeding that bound is ignore-record like any other it cannot read." Its Note:
"A file whose document decodes to more than the guarantee stays conforming."
Third disposition, confirmed: ignore-record, not a violation, assigned encoding.

Downgrade quote — [R-MTA-09]: "the decline is not a finding that the file is
nonconforming and a verifier MUST NOT report it as one"; and [R-ERR-03]: "A file
exceeding any of these remains conforming". Every verdict is fixed. CONFIRMED,
editorial.

---

## Group 6 — reader-03: does the experimental exception withdraw R2?

The reporter claims the exception, read on its face, withdraws violation status
from every §21.5 row (R2, a failed extent CRC, included) at encoding ≥ 0x80.
Checked against the text: the exception carries its own restrictive relative —
"except at an experimental-range encoding, **where no document rule attaches**"
— and the very next sentence says

> "what `[R-MTA-10]` withdraws is the document's content rules, never the
> encoding byte's own value set (`[R-MTA-03]`)."

and [R-MTA-10] names the surviving checks, the extent's terminal CRC among them.
An extent CRC is not a document content rule, so the exception does not reach R2
even on its face. The reporter's second reading requires dropping the relative
clause and the following sentence. PARTIAL: residual looseness worth tightening,
claimed defect refuted. Editorial.

---

## Group 7 — §21.7 says T3 reads the index entry

§21.7 (3594-3596): "a change that reaches the decoded size or the codec instead
is witnessed by T3 or T14, which read the index entry rather than the decoded
image". §21.4's T3: "The decoded payload's byte length is not exactly the tile's
decoded size…", governing [R-SER-07], reachable only after §19.4 steps 5-6.
T14 is entry-only. The parenthetical is false of T3. Both reporters correct.
Both rows fire on the same files and §9.7 decodes every stored tile, so no
verdict moves. CONFIRMED, register-bookkeeping.

---

## Group 8 — writer-04: [R-LIF-02]'s barriers absent from §21.7

Verified the enumeration at 3577-3605: history properties ([R-LIF-01],
[R-LIF-03]), the ordinal mappings ([R-GEO-06], [R-SER-01]), [R-CNT-13],
[R-CNT-18], §20.3 step 4's bar, [R-ENC-06]. The barriers of [R-LIF-02] steps 4
and 6 appear nowhere. Factually accurate.

But whether §21.7 owes them a class is a judgement, and the document's own
scoping cuts against it. §2.3: "File conformance is a pure predicate on bytes:
it does not depend on any reader, writer, or environment." Two files written
with and without a barrier are byte-identical, so a barrier violation is not a
candidate file-conformance violation at all — it is not something the register
could have omitted, and §21.1 ties §21.7 to "a *detectable* file-conformance
violation this specification names and the register omits". The classes §21.7
does name are all obligations that constrain bytes in some generation.
PARTIAL, editorial: the repair is a maintainer's choice between naming the
barriers and stating the paragraph's scope.

---

## Group 9 — Appendix H's verifier block omits pad bits

Verifier block (4306-4307): "decoded-content obligations — padding samples and
interleaved boolean bytes (§14.5, §14.2)". Writer block (4275): "fill-encodes
edge padding **and pad bits** (`[R-SER-05]`, §14.5)". §14.3's Note: "Pad bits
are not padding positions (§11.3)." T5 is verifier-detected, governing
[R-SER-05]. The asymmetry is real. Downgrade quote — Appendix H's opening:
"each entry's authority is the requirement or section cited, never this
summary"; and [R-SER-05]: "Every pad bit (§14.3) MUST carry the plane's
channel's fill bit … a verifier MUST check it". CONFIRMED, editorial.

---

## Group 10 — diagrams-04: the shrink sentence and the "already holds fill" carve-out

The reporter reads "a shrink that turns real positions into padding of a tile
stored there is barred" as a flat second bar that drops the carve-out at
2961-2967. Checked in context: the same paragraph opens

> "the bar above is the whole of the test, **in the bar's own tense**: a shrink
> is permitted exactly where it alters nothing §14 fixes for any tile the layer
> stores in the generation this commit supersedes"

which imports the carve-out expressly and states the permission with "exactly".
The trailing clause is subordinate to "and for the same reason: the quantifier
is the superseded generation's", so it is about tense, not about content. The
second reading is foreclosed by the paragraph's own opening. PARTIAL: the
ellipsis is worth one clause of tightening, the claimed contradiction is not
there. Editorial.

---

## Group 11 — diagrams-05: shape (c) widens re-declaration

Example, line 3082: "A layer storing no tile is re-declared freely whatever its
geometry, which is the same step's permission." The normative permission
(2974-2987) is quantified over "A layer that stores no tile **in the generation
this commit supersedes**" and the geometry proviso reads "provided the grown
geometry stays within every bound the layer's own declarations impose,
`[R-COD-07]`'s lz4 decoded-size cap among them (L44), **which an empty layer
escapes only because that cap is quantified over addressed tiles**". §17.2's
Note confirms the escape belongs to a layer that *addresses* none — "any
dimension extent 0". So the Example conflates storing none with addressing none
and drops the proviso. Reporter correct on both counts.

Downgrade quotes: [R-CNF-01] makes an Example non-normative, and [R-CNF-05] "A
writer MUST emit only conforming files" decides the resulting file
independently; L44 is reader-detected at layer access with a fixed outcome, so
two verifiers agree. CONFIRMED, editorial.

---

## Group 12 — register-04: §21.1 carries no identifier

True: §21.1 assigns none; it cites [R-ERR-02], which is assigned at §21.8
(3612). But the claimed bite does not exist. [R-VEC-02] requires each vector to
name "the §21 register row it exercises together with that row's governing
requirement identifier" — a vector is a *file*, and a row-versus-rule divergence
is a defect in this document, not a condition a file can exhibit; §24 says so
itself ("A vector whose expectation cannot be stated in those terms is testing
something this specification has not defined, which makes it a finding against
this document rather than a vector"). And §2.1's Note fixes the phrasing
discipline for a requirement — "every requirement names the actor it binds
(writer, reader, updater, verifier, or file)" — which §21.1's interpretive
statements do not do, supporting the reading that they are not identifier-bearing
requirements. PARTIAL, editorial.

---

## Group 13 — register-06: [R-ERR-04]'s unqualified decline sentence

"Software that declines a file whose every quantity lies within the table is not
a conforming reader (`[R-CNF-03]`)". Read alone it condemns the [R-CNT-15]-
compelled rejection of an experimental MU=1 record. Downgrade quote — §2.3,
which scopes it in terms:

> "(§21.9's `[R-ERR-04]` governs a refusal on that last ground; §21.6's closing
> paragraph names the other two)"

plus the sentence's own citation to the qualified [R-CNF-03] and the next
sentence's "Either way, a refusal **on resource grounds**". CONFIRMED,
editorial; repair is three words.

---

## Group 14 — verifier-04: the reproduced entry is not stable under a change of F

Mechanism checked and real for **one** row. §15.3's structural rows are six:
sentinel-with-crc≠0; exactly one field sentinel; length=0; offset<16; either
field > 2⁶³−1; and "offset + length overflows, or offset + length > F − 64".
Only the last references F, and only its second disjunct. The reporter's
"Four of §15.3's six structural rows classify an entry by comparing its fields
against F" is **false** — it is one of six. That is a material overstatement,
since it is what makes the class sound broad.

The residual mechanism holds: a T9 entry reproduced "exactly as they stand" into
an output with F_out > offset+length+64 is no longer structurally rejected, and
[R-TYP-09] confirms the input's reference array is undefined there ("A reader
MUST NOT return fill for a tile whose entry is malformed"), so [R-WRT-07]'s
"reference arrays MUST equal the live generation's bit for bit" cannot police
the substitution. But the scenario needs F_out > F_in, which compaction does not
normally produce, and the compactor is already barred from authoring the
resulting overlap or crc mismatch by [R-CNF-06] ("An updater MUST satisfy every
writer requirement for the bytes it produces") — the regenerated index region is
bytes it produces. So a conforming compactor must already choose a placement
that keeps the reproduced entry structurally invalid; what is missing is that
this is nowhere said. PARTIAL, design-decision, not byte-level.

---

## Group 15 — writer-06: Appendix G item 2's fallback

"Any other fixed nonzero value is substituted in the measure-zero case that they
are all zero" (4148-4151). Confirmed: every other item names its value or its
producer. Downgrade quotes: Appendix G is "(non-normative)" in its heading and
says "It adds no requirement to any actor: a writer ignoring it is fully
conforming"; [R-CNF-05] already licenses two conforming writers to differ.
CONFIRMED, editorial; repair is naming a constant.

---

## Group 16 — quiz-05: Appendix G item 3's "any record extents"

§7.4 line 1002: "A layer record's extent slot addresses the layer's tile-index
region"; §5.2 counts "a record extent (the bytes any record's extent slot
references, whatever the record's type)"; §20.5's Example: "a relocated
tile-index region — itself a record extent (§5.2)". So the second phase's domain
literally re-covers the first phase's index regions. Reading (2) is
self-referentially unsatisfiable for a two-layer file, as the reporter says, so
only reading (1) survives; and the appendix is non-normative. CONFIRMED,
editorial; repair is the word "remaining".

---

## Group 17 — quiz-03: "governs §6.4's accounting and nothing else"

§6.1: "That distinction governs the request accounting of §6.4 and nothing
else". §6.2 [R-CNT-06]: "committed_file_length equals the file size (for a
remote reader, the size reported by its transport)".

Checked where the substantive rule lives: [R-CNT-10] is stated in **§6.4**
("The size a remote reader compares against committed_file_length MUST be
transport-authoritative"), so the distinction governing it is inside the reach
§6.1 grants. And §19.1 step 1 binds *every* conforming reader: "Obtain the
transport-authoritative file size F (`[R-CNT-10]`)". §6.2's parenthetical
therefore adds no obligation and creates no second decision point; a local and a
remote reader perform the same comparison and reach the same F17 verdict.
PARTIAL: the mention is real, the claim that the gate "turns on" the distinction
is not. Editorial.

---

## Coverage check

Union of member_ids, sorted and de-duplicated by hand against the input list:
reader-01..04 (4), writer-01..06 (6), verifier-01..04 (4), diagrams-01..05 (5),
register-01..06 (6), adversary-01..04 (4), quiz-01..05 (5) = 34. Each appears in
exactly one group. Byte-level groups: 2 (compactor-refuse-vs-reproduce,
drop-licence-modifying-layer-record).
