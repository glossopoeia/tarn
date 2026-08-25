# Round 25 triage — skeptic lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in these spans:
  §2 (94–290), §4.6–4.7 (470–553), §5 (555–700), §6 (700–870), §7 (866–1110),
  §9 (1154–1370), §11 (1463–1600), §14 (1792–1990), §16 (2113–2215),
  §18.2 (2470–2560), §19 (2679–2900), §20 (2900–3335), §21.1–21.2 (3335–3480),
  §21.3/21.4/21.5 selected rows (grep), §21.6–21.9 (3590–3816), §23 (3924–4005),
  §24 (4005–4090), Appendix G (4266–4410).
- One mechanical count over §21.2–§21.5 table cells (script below).
- **No** transcript in `round25/` — not the walk transcripts, not the triage ones.
  I never listed the directory; I only `mkdir -p`'d it to write this file.
- No `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `registry.json`,
  no git history (the git-status block in my system context named commit subjects;
  I did not act on it and no finding below turns on it), no web.

## Instance count (checks the arithmetic two reporters rest on)

```python
import re
lines=open('spec/tarn.md').read().split('\n')
tot=0; rows=0
for l in lines[3335:3640]:
    if re.match(r'^\|\s*[FLTR]\d+\s*\|', l):
        cells=[c.strip() for c in l.strip().strip('|').split('|')]
        if len(cells)>=6:
            inst=cells[2]
            n=len([x for x in inst.split(';') if x.strip()])
            if inst.strip()=='—': n=1
            rows+=1; tot+=n
print(rows, tot)   # -> 121 277
```
So §21.8's "121 conditions over 277 instances" is exact **for the cells as
written**. The R8 dispute is about what the cell ought to say, not about
whether the total matches it.

## The framing premise behind every downgrade (attack this first)

The byte-level test I applied: *does the fork change the set of conforming
files, or what a reader/verifier must accept, reject, or certify?* I did **not**
count a divergence in **updater conduct** as byte-level where both candidate
outputs are conforming files that some conforming actor may emit. Four groups
(G4 reader-03, G5 writer-01, G6 adversary-01, G8 writer-03) turn entirely on
this premise, and all four would flip if the maintainer reads "which byte
sequences a conforming implementation may emit" as ranging over *an updater's
output for a given input* rather than over *the set of conforming files*.

The document supports my narrower reading explicitly, and this is the quotation
the premise rests on — §2.3 `[R-CNF-02]`:

> "File conformance is a pure predicate on bytes: it does not depend on any
> reader, writer, or environment. … conduct rules bind the actor, the predicate
> binds the bytes."

and §21.7 `[R-ERR-01]`, which classifies the §20.3 step-4 bar's unwitnessed part
with `[R-LIF-01]`:

> "§20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored, and then only for part of what it bars."

If that premise is wrong, G6 is the most expensive miss (a silent whole-layer
reinterpretation), then G8, G4, G5.

## Groups

### G1 — [R-CNT-27] is unordered against the version gate (reader-01, diagrams-02, register-01)

Same defect from three angles: the §21.2 preamble's warrant, and the closed
count of four rows. All three reporters self-flagged non-byte-level, so nothing
here is a downgrade of a reporter's flag; I still had to decide it myself.

Verified against the text:
- §6.2 `[R-CNT-06]` lists: "the trailer magic; the trailer CRC; the version gate
  (§6.3) … and then, those gates passed, MUST validate all of the following …".
  `[R-CNT-27]` appears nowhere in that list. §5.1 states it with no ordering.
- §19.1 step 1 obtains F before step 2 fetches the trailer; §19.2 `[R-RDR-02]`
  adds "A reader MAY detect any violation earlier". F5's *Detected* cell is
  "open", and §19.2 orders nothing **within** a tier.
- So the reporters' factual claim holds: **nothing orders the 128-byte floor
  relative to the version gate.** I searched §5.1, §6.2, §6.3, §19.1, §19.2,
  §21.1, §21.2 and §2.3 for a sequencing sentence and there is none. That
  absence is the finding.

Why it is not byte-level, with the quotations:
- Reader outcome is identical under both readings. `[R-CNT-27]`: "A reader MUST
  treat a shorter file as a validity error at file scope" → reject-file.
  `[R-CNT-07]`: "A reader MUST reject-file when version_major … is a major it
  does not implement" → reject-file. Same file, same refusal.
- No file this text judges is affected: a conforming major-1 file cannot be
  under 128 bytes, so F5 is unambiguous over the whole conforming set.
- The substance of the verifier verdict is already decided by §2.3: "a file
  declaring another major is neither conforming nor nonconforming under it: a
  reader refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and
  that refusal is not a finding about its bytes." A verifier reporting
  *nonconforming* would be asserting exactly what that sentence denies.
- The diagnostic half is SHOULD-level: §6.3 "the diagnostic … SHOULD be distinct
  from both 'not a TARN file' and 'corrupt'".

What survives: the preamble's stated **warrant** ("§6.2 puts the version gate
ahead of every check but the trailer magic and the trailer CRC") does not reach
F5, whose check is not one of §6.2's, and the count "Four rows" is asserted as
closed on that warrant. That is a real defect in a normative paragraph
(§2.1 exempts only §1, Note/Example/Rationale and non-normative appendices).
CONFIRMED, design-decision — a maintainer must decide whether F5 is inside the
excused set (then §5.1 or §6.2 owes an explicit ordering clause) or outside it
(then the count is five, not four).

### G2 — "geometry" under-describes the excused set (quiz-01)

Not the same defect as G1: fixing the word "geometry" leaves the missing
ordering for `[R-CNT-27]` exactly where it is, and supplying the ordering leaves
"geometry" exactly as loose. Separate group.

The paragraph's own clause after the colon does the work the word does not:
"§6.2 puts the version gate ahead of every check but the trailer magic and the
trailer CRC, so such a file is refused on capability grounds first" — which
reaches F9–F20, F24, F27, F34 and the rest of quiz-01's list, all of them
§6.2-ordered or later. So the reporter's harmful reading (a verifier believing
itself entitled to record F12 against a foreign-major file) is foreclosed by the
sentence the reporter itself quotes, plus §2.3. Editorial: the excusing property
and the excepting property are not complements, and "geometry" is the wrong
word for "not fixed across majors by `[R-CNT-24]`". Not byte-level.

### G3 — §23.1 cites shape (c) for a user-metadata edit (reader-02)

§20.3, inside shape (c): "Editing user metadata is not this shape: its document
lives in an extent (`[R-CNT-25]`), so a new extent is appended and the old one
becomes slack, as in (b)." §23.1 says "(§20.3's shape (c))". Verified verbatim
in both places. The mechanics §23.1 states ("appends a new extent and strands
the old one") are (b)'s, so no reader can reach a wrong byte from it; the
pointer alone is wrong. CONFIRMED, editorial. Repair: "§20.3's shape (b)", or
"the paragraph of §20.3's shape (c)".

### G4 — §20.3 step 2's "MUST NOT drop the record" (reader-03)

I tried to kill this and got halfway. Killers considered:
- The premise clause "Against any other structure the appender carries forward"
  — cuts both ways: a dropped record is not carried forward, which makes the
  drop prohibition vacuous under one reading and additive under the other.
- §20.5's compactor parallel: "Dropping is the one disposal that answers, and
  only where §20.4's table licenses it … Where the table does not license a drop
  the compactor MUST refuse." Analogical support for Reading A, not a decision
  about the appender; and the reporter is right that the explicit compactor
  treatment beside a bare appender "MUST NOT drop" reads as deliberate asymmetry.
- The bare "(§20.4)" citation form is this document's way of naming the governing
  rule, which is Reading A. That is the strongest indicator and it is a
  convention, not a stated rule.
No foreclosing sentence found. CONFIRMED, design-decision. Not byte-level under
the premise above: both outputs exist as byte sequences whose reader treatment is
fixed independently of the reading. Repair: one clause — "and MUST NOT drop the
record except as §20.4's table licenses".

### G5 — step-4 list omits pad bits and interleaved bool bytes (writer-01)

Checked the three §14 content obligations: §14.5 `[R-SER-05]` fixes padding-position
content **and** pad-bit content ("Every pad bit (§14.3) MUST carry the plane's
channel's fill bit"); §14.2 `[R-SER-08]` fixes interleaved bool bytes. §20.3's
list says "the set of padding positions (§11.3) and the content `[R-SER-05]`
fixes **there**" — "there" is the padding positions. So the list is short by
two, exactly as reported.

The *ambiguity* half is foreclosed, and this is the downgrade quotation:
"The test is the effect on such a tile, and **the list names where that effect
arises rather than standing on its own**." Reading (a), list-as-exhaustive, is
dead on that sentence. Corroborated by §21.7: "A change reaching a byte §14
structurally constrains — a padding position, a pad bit, or a boolean byte —
fires §21.4's content rows", and by Example (c)'s "a padding position or a pad
bit". So: the headline is CONFIRMED (the list is incomplete), the fork is not.
Editorial. Not byte-level — where the tiles stay stored T2/T4/T5 fire under
either reading; where they do not, §21.7 already records that there is no witness.

### G6 — step-4 list and §21.7 omit sample type and channel order (adversary-01)

Not merged with G5: fixing G5 (adding "pad bits and boolean bytes" to the list)
leaves this untouched, and vice versa — different items, different witness
status. G5's items are named by §21.7 and by Example (c); G6's are named nowhere.

Verified the construction's ingredients: §14.2 "a numeric value as its type's
element size, little-endian"; §12.1's element-size groups do put float32 and
int32 at 4 bytes; §14.1 "value k of the sequence is channel (k mod C)'s value";
§7.4's channel entry carries the type, and §12 "channels are declared in order,
and the declared order is load-bearing". So a directory-only re-declaration of a
channel's type inside an element-size group moves no offset, no decoded size, no
codec, no filter, no padding-position set — and changes what every stored sample
denotes. The operative test ("what §14 fixes for its stored bytes **or how they
decode**") reaches it; the enumerated list does not, and §21.7's per-category
account does not name it either.

I hunted for another rule that bars it — §9.1 `[R-LIF-01]` (bytes, not
declarations), `[R-MDL-02]` (compaction's output), §20.4 (records, not
declarations) — and found none. CONFIRMED, design-decision. Not byte-level:
`[R-TYP-05]`'s "every bit pattern is a valid sample value" plus the absence of a
register row means every verifier certifies the output under either reading.
This is the group I would most want a second opinion on.

### G7 — §11.1's growth Rationale (writer-02)

Checked the arithmetic: §11.2 N = ∏Gᵢ; §7.4 "entry_count | u64 | equals the
addressed-tile count"; §11.1 `[R-GEO-02]` "A dimension with extent 0 is valid",
with no cap on how many. E = (0,0), T = (4,4), grow E₀ to 4: G = (1,0), N = 0,
entry_count still 0. The sentence "growth that raises one changes entry_count"
is false there, and the trailing "the first growth of a zero-extent layer
included" is false for that layer. CONFIRMED, editorial. Downgrade quotation,
§2.1: "All text in this document is normative except: §1 (Introduction); any
text labeled *Note*, *Example*, or *Rationale*" — this is a Rationale, and every
byte it touches is fixed by `[R-CNT-17]`, `[R-CNT-23]` and L22 in agreement.

### G8 — may adding a top-level record license the drop? (writer-03)

Searched §20.4, §7.2, §7.3, §10, §20.3 and §20.5 for a sentence disposing of
addition on the top-level branch. The only gloss is "A commit changes the layer
set by adding a layer", which glosses the first item, a **set**. The third item
names "another *non-layer* top-level record", a record. The nearest thing to a
foreclosing sentence is "Dropping the record, or dropping another record in the
same commit, is not itself such a change, so a commit whose only effect would be
the drop MUST retain it" — which excludes a same-commit *drop* and is silent on a
same-commit *add*. Not a decision. CONFIRMED, design-decision. Not byte-level:
both directories are conforming files (§21.6 with `[R-CNT-15]` for the absent
case; a creator emits either), so the conforming set does not move.

### G9 — Appendix G leaves tiling and layout open (writer-04)

Verified the transfer argument: §11.3's Note "Tile extents are a writer's choice,
and this specification imposes none"; §14.4's Note "A single-channel bool layer
does not — ⌈P/8⌉ packed bytes planar versus P bytes interleaved — and both forms
are valid"; item 2's own "two files carrying the same arrays can legitimately
differ in tiling, layout, and codec". Item 5 pins alignment, slab and filter on
an argument that transfers verbatim. Item 7 shows the profile does pin
caller-facing choices where the writer has latitude. Closing paragraph "Read the
numbered items as the list; this paragraph names what they are for, not how many
there are" disclaims the *summary paragraph*, not the items' completeness — so
it is not a foreclosing sentence. CONFIRMED, design-decision (a maintainer must
decide whether the profile takes the layer schema as given input). Not
byte-level: the appendix is identified non-normative and "adds no requirement to
any actor: a writer ignoring it is fully conforming".

### G10 — shape (c) quantifies over the layer, not the channel (diagrams-01)

Verified: §14.1 "the tile with disk ordinal c · N + s … carries exactly the
values of channel c"; §14.5 fixes padding content "for each channel the position
carries". So in a planar layer a stored plane of channel f carries nothing of
channel b, and step 4's quantifier ("any tile that layer stores") is not
satisfied by a change to b's fill. The Example conditions on the layer instead.
Decided by §2.1 — the block is labelled *Example* and is non-normative, so step 4
governs — which is why this is a figure-level defect and not a fork. CONFIRMED,
figure. Repair: condition the Example on a stored tile the change *reaches*.

### G11 — R8 enumerates containers and no forms (diagrams-03, adversary-02)

One defect, two reporters, same row, same repair. Both arrive at four instances
and at §21.8 being short by two.

I tried hard to kill this one. The candidate killers:
- R8's own "in any form … and the bare tokens … **alike**" — the author's
  explicit judgement that the forms are one family, which §21.1 licenses: "a row
  whose check ranges over a family without the condition changing shape states
  that range as a single instance (T24's *any codec*)".
- Against it: §21.1's other half, "one whose members give the condition
  materially different shapes enumerates them (T15, T25)", and the governing
  rule's own text, which joins the two by "or" and gives them different
  mechanisms — "which RFC 8259 does not admit and some parsers accept
  regardless". The predicate "contains a number whose binary64 interpretation is
  not finite" does not even apply to a bare `NaN`, which is not a JSON number.
  T15 (zlib vs gzip) is enumerated on a narrower difference than this.
So §21.1 does not decide it either way; it hands the call to judgement, and the
row is the one place the judgement went against the pattern of R1, R5, R6, R7.
CONFIRMED, register-bookkeeping. Not byte-level: §24 `[R-VEC-01]` "the corpus is
**derivative** … where a vector's recorded expectation and this specification
disagree, this specification governs", and §21.8 "A row without a vector is a gap
in the corpus, not a licence to skip the check". Repair: either enumerate four
and restate §21.8 as 279, or say in the row why the forms are one family.
(Both reporters disclosed contamination — an auto-memory title and a git-status
commit subject naming this row. Their counting arguments stand without it, and I
re-derived the 277 mechanically.)

### G12 — §4.7's Note about §7.2 (diagrams-04)

Verified §7.2's header table: columns Offset | Size | Type | Field | Class; five
fields; ranges appear only in "type (0 invalid)" and the flags cell.
inline_length, extent_offset and extent_length carry none. The Note's claim
"§7.2 folds each field's range into its Field cell" is inaccurate for three of
five. Decided by §2.1 (a *Note*), and the ranges are stated normatively two
lines below the table ("The **extent slot** … Any other combination with either
half zero, an extent_offset < 16, an extent extending past F − 64, or an
overflowing sum is a validity error …") and in `[R-ENC-03]`, `[R-CNT-12]`,
`[R-CNT-13]`. CONFIRMED, editorial. Not byte-level.

### G13 — the shrink sentence's three consequences (diagrams-05)

The reporter is right on the arithmetic (rank 1, T = 4, E 12→10 leaves G = 3),
and right that §11.1's Rationale carries the distinction the shrink sentence
does not. But I found the foreclosing sentence the reporter did not quote, in
§20.3 step 4 itself, three paragraphs above:

> "A layer whose record alone changes keeps its extent slot, pointing at the
> existing region, as does a layer the commit leaves untouched (`[R-WRT-05]`);
> relocating a live index region is compaction's operation (§20.5,
> `[R-WRT-07]`), not an appender's."

and the re-emission trigger, also step 4's: "Every layer whose **stored-tile set
or index content** this commit changes has its tile-index region re-emitted in
full". A shrink that de-addresses nothing changes neither, so re-emission is not
merely unnecessary — relocating the region is *not an appender's operation*.
Reading (ii) is therefore dead, and the reporter's worse case (20 MB re-emitted
for nothing) is barred rather than merely wasteful. What remains is a normative
sentence whose subject is "a shrink [that] is permitted" and whose two middle
clauses hold only where a grid count falls. CONFIRMED, editorial. Not byte-level.
Repair: "Where such a shrink drops tiles out of the addressed set, …".

### G14 — §9.6 cites F8 and F17, omitting F14 (register-02)

Verified both passages. §9.5's Note: "the magic, the CRC, or
committed_file_length against the transport size, each of which §21.2 already
registers" — three grounds. §9.6: "(§21.2 rows F8 and F17)" — two. F14 is the
CRC row and is reachable in exactly the residue case §9.6 discusses. CONFIRMED,
register-bookkeeping. Not byte-level: F8, F14 and F17 share detector, detection
point and outcome (reader / open / reject-file), and all three are independently
reachable rows.

### G15 — "Two do not" (register-03)

Tested the taxonomy against the paragraph's own list. Power-of-two form of A and
of A_slab: not a field width (§7.4 has both as u64), not an external format, not
the value domain (`[R-ENC-03]` bounds magnitude only), not arithmetic over an
unomittable structure. It is chosen here, twice, and for A_slab it is the only
substantive constraint (1 = 2⁰; 2⁶² is the largest power of two in domain). So
"Two" is short. I checked the reporter's reproduction of the rest and it holds.
CONFIRMED, editorial. Not byte-level: §7.4's constraint table, §16.1 and §16.2
state the requirement normatively and L39/L29 remain reachable either way.

### G16 — L41's "that tile's length" (quiz-02)

The pronoun is genuinely loose. Three things decide it:
- §21.1: "where a row and the rule it cites diverge, **the rule governs**".
- §16.2 `[R-SLB-03]`: "the run's stored tiles are **contiguous and packed in
  ordinal order** — each stored tile's offset equals the previous stored tile's
  offset plus its length". "Contiguous and packed" admits only offset(k) =
  offset(k−1) + length(k−1).
- The row's own parenthetical and its three instances — "gap; overlap;
  out-of-ordinal placement" — are the failure modes of that relation and of no
  other.
CONFIRMED as a wording defect, register-bookkeeping, not byte-level: no verifier
that follows §21.1 can reach the unsatisfiable reading. Repair: "plus **that
previous tile's** length".

### G17 — §20.5 names F36 and L25 (quiz-03) — REFUTED

This is the one I killed. The citation sits inside §20.5's clause about a
**compacted output** carrying a feature the compactor does not implement. Two
sentences later in the same requirement:

> "A compactor MUST refuse to compact a file carrying any record whose type it
> does not implement with MU = 1: such a type can define references this
> specification does not (§7.2), so its bytes cannot be safely relocated."

F35 and L24 are the MU = 1 specializations. In this context the MU = 1 case never
reaches an output at all — the compactor is obliged to refuse — so F36 and L25
are exactly and completely the rows a reserved-range record type in a compacted
output is recorded against. §21.6's closing sentence names all four because its
context is general, not compaction. The reporter applied §21.1's specialization
clause without the context restriction that keeps MU = 1 out of the picture.
Severity none; no repair owed. (The reporter's own seven-space check, L31, L33,
L34, L36, L43, L45, R1, I did not re-verify exhaustively — see notes.)

### G18 — `[R-CNF-03]`'s missing *top-level* qualifier (adversary-03)

The closest thing in the input to an accept/reject fork, so I pushed on it.
§7.4 `[R-CNT-18]` is explicit: "an unknown sub-record type with MU = 1 is
reject-layer, and **where the file is otherwise conforming a reader MUST NOT
reject the file for it**". §21.6's closing paragraph flags the qualifier at
exactly the point §2.3 drops it: "The qualifier is load-bearing — the same type
as a layer sub-record is reject-layer and never a ground to refuse the file
(`[R-CNT-18]`), so only the top-level case is a file a reader refuses."

The logical point that settles it: `[R-CNF-03]`'s clause is a **carve-out from a
duty**, not a licence. Lifting an obligation to accept does not create a
permission to reject, and `[R-CNT-18]`'s MUST NOT expressly forbids the
rejection. So no conforming reader may actually diverge, and this is not
byte-level. CONFIRMED, editorial. Repair: insert "top-level" into `[R-CNF-03]`.

## Which ones I tried hardest to kill and failed

G1 (found the sentence that decides the substance — §2.3 — but none that
supplies the ordering the preamble's warrant needs), G6 (searched §9, §14, §20.4,
§21.7 for any other rule barring a type re-declaration; nothing), G8 (searched
§20.4's whole row and its neighbours for a gloss on addition; nothing),
G11 (§21.1 hands "materially different shapes" to judgement and does not decide),
G18 (killed as a fork, survives as an omission). Killed outright: G17.
