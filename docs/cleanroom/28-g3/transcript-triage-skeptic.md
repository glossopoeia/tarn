# Round 28 — triage pass, SKEPTIC lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, all 4648 lines,
  in four Read calls (1–1200, 1200–2400, 2400–3399, 3399–4098, 4098–4648).
- Nothing else. I did not open any walk transcript, did not list any directory,
  and did not read any other triage pass's notes.
- One `mkdir -p` of my own output directory (`Bash`), which creates nothing but
  the directory I was given.

## Method

Default position: the finding is wrong and the document decides it somewhere the
reporter did not look. For each finding I went hunting for the foreclosing
sentence and recorded whether I found it. Where I could not find one, I said so.

Byte-level test applied verbatim: *does resolving this change which byte
sequences a conforming implementation may emit, or must accept or reject?*
Every downgrade below carries the quotation that decides it, and states the
premise the downgrade rests on so it can be attacked.

---

## Grouping (22 ids → 18 groups)

Merges:

- **appendix-g-shuffle-universal** = verifier-03 + diagrams-02 + adversary-06.
  All three attack the same closing clause of Appendix G item 5, all three
  supply a fixed-point counterexample, all three concede the item's operative
  content survives. One defect.
- **zero-layers-empty-directory** = diagrams-03 + quiz-02. Same §21.6 row, same
  counterexample (a layerless file carrying a file-scope user-metadata record),
  same [R-CNT-14] argument, same §21.1 escape hatch. One defect.
- **s217-omits-preservation-duties** = diagrams-05 + adversary-02. Both say
  §21.7's second-paragraph inventory omits obligations of exactly the class it
  enumerates. diagrams-05 names [R-WRT-05], [R-WRT-08] and §20.4's drop
  restriction; adversary-02 names those plus [R-CNT-08]'s updater carry-forward.
  Overlapping item lists, one defect: the inventory is under-inclusive.

Everything else stands alone. 3 + 2 + 2 + 15 singletons = 22. Checked by hand
against the id list twice.

---

## Findings, group by group

### 1. appendix-g-shuffle-universal (verifier-03, diagrams-02, adversary-06)

Text: "elsewhere it changes the stored bytes of every tile it touches."
(Appendix G item 5, line 4520–4521.)

I checked the permutation arithmetic myself. [R-COD-10] sends byte *i* of group
*j* from offset j·s + i to i·n + j. Identity for all i,j iff s = 1 or n = 1
(i = 1, j = 0 forces n = 1; i = 0, j = 1 forces s = 1). The first half of the
sentence is right.

The closing universal is false: a permutation fixes any string it fixes, and a
constant decoded image is fixed by every byte permutation. adversary-06's
witness (C = 2 uint8 channels, P = 8, L = 16, s = 2, n = 8, all-zero image,
nonzero fills) is legal — item 6 excludes only all-*fill* tiles, and this tile's
samples are (0,0) against nonzero fills, so it must be stored.

**Kill attempt.** I looked for a scoping sentence — anything reading "touches"
as "tiles whose image it does not fix", or scoping the claim to the general
case. §17.3 makes no such claim; the appendix has no other sentence about it.
Not found. The universal stands falsified.

**Byte-level: no.** Deciding text — Appendix G's own heading and preamble:
"### Appendix G — Reproducible-writer profile (non-normative)" and "It adds no
requirement to any actor: a writer ignoring it is fully conforming", read with
[R-CNF-01]: "All text in this document is normative except: … appendices
identified as non-normative." Nothing a writer may emit or a reader must accept
turns on a rationale clause inside a non-normative profile item whose operative
instruction (pin the filter value) is unaffected.

*Premise of the downgrade, stated so it can be attacked:* that item 5's
operative content is the instruction "pin the filter", not the clause, and that
Appendix G binds no actor. If someone could show a normative rule that reads
this clause as its own (nothing cites it), the downgrade would fail.

CONFIRMED / editorial.

### 2. zero-layers-empty-directory (diagrams-03, quiz-02)

Row: "| The file contains zero layers | A conforming file with an empty
directory | `[R-CNT-14]` (R-CNT-02) |"

[R-CNT-14] permits, in one sentence and with no dependency between the clauses,
"any number of layer records (zero is valid…); at most one file-scope
user-metadata record". [R-CNT-15] additionally admits unknown ancillary records
at file scope. So zero layers does not entail an empty directory, and the
Defined-behavior cell answers with a strictly narrower fact than its Condition
cell names.

**Kill attempt.** §21.1 does decide the *outcome*: "§21.6's entries restate
their governing rules on the same terms a row does, and where such an entry and
the rule it cites diverge, the rule governs there too." So no reader gets a
ground to reject. That kills the consequence, not the misstatement. I also
checked whether [R-CNT-14]'s own parenthetical is the defect instead — "zero is
valid: an empty directory is a conforming generation" states a sufficient case
and is true as written; the row is what lifts it into an answer column. And
§5.1's Example says "It contains no layers (a valid, empty file)" about one
specific 128-byte file, not about the class, so it does not make the same move.

**Byte-level: no.** Quote deciding it: §21.1, "where such an entry and the rule
it cites diverge, the rule governs there too", together with [R-CNT-14]'s own
permission. Under both readings the file is conforming and [R-CNF-03] obliges a
reader to accept it.

CONFIRMED / register-bookkeeping.

### 3. s217-omits-preservation-duties (diagrams-05, adversary-02)

§21.7's second paragraph opens "A second set of obligations is omitted from the
register because a single file exhibits no witness of their violation" and then
itemises by identifier: [R-LIF-01], [R-LIF-02], [R-GEO-06]/[R-SER-01],
[R-CNT-13]'s embedded-offset bar, [R-CNT-18]'s nesting bar, §20.3 step 4's
declaration bar, [R-WRT-06]'s three trailer obligations, [R-ENC-06].

Not itemised: [R-WRT-05]'s byte-identical re-emission, [R-WRT-08]'s no-re-encode
bar, §20.4's MU = 0 / PE = 0 drop restriction, and [R-CNT-08]'s "An updater MUST
copy forward unknown ignore-lane bits of the file it modifies and MUST NOT clear
them." I checked each is genuinely unwitnessed: all four need a prior
generation, whose trailer and directory are slack — [R-CNT-21] "Slack has no
internal structure this specification defines, its content is unconstrained…
A reader MUST NOT interpret it" and §9.7's walk does not enumerate it. §20.4's
own Rationale makes the argument in §21.7's own words. The asymmetry is sharpest
at [R-CNT-08]: §21.7 names the *compactor's* ignore-lane carry-forward
([R-WRT-06]) and steps over the *appender's* ([R-CNT-08]), which is the same
duty for the same reason.

**Kill attempt — and this one lands, partly.** §21.1 expressly removes §21.7
from the completeness obligation: "The subsections after §21.5 are not part of
the register and carry no rows: neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations, §21.7's
account of what no check detects, or §21.9's limits." So no normative
completeness duty is breached; §21.7 is "the account, **by class**, of what
fails it". What survives is that §21.7 reads as an inventory (every other member
is named by identifier) and is short by four. That is a drafting complaint, not
a rule violation.

**Byte-level: no.** Deciding quote as above, plus §21.7's own premise: "a single
file exhibits no witness of their violation" — by hypothesis nothing about any
file's acceptance turns on whether the paragraph names them.

CONFIRMED (as an under-inclusive inventory) / editorial. Repair is optional
under §21.1.

### 4. front-matter-normativity (reader-01)

[R-CNF-01]: "All text in this document is normative except: §1 (Introduction);
any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as
non-normative." The line-12 blockquote is none of those and labels itself
"*(non-normative)*".

**Kill attempt.** I looked for a front-matter carve-out and found none. I did
find something the reporter missed that *widens* the defect rather than closing
it: lines 3–10 (Status, drafting process, "where an ADR and this document
diverge, this document governs", License) are also unlabeled non-§1 text and are
therefore normative under [R-CNF-01] too. So the repair should cover front
matter generally, not just the one block. The reporter's claim that this block
is the only text *claiming* an exemption remains true.

**Byte-level: no.** The block's imperative content concerns this document's own
organisation and its corpus, and the corpus half is already stated normatively:
[R-VEC-02] requires each vector to record "the §21 register row it exercises
together with that row's governing requirement identifier". No field, offset,
enum or outcome class is constrained by the block under either reading.

*Premise:* that documentary self-description cannot fork bytes. Attackable only
by showing a sentence in the block that constrains a file; I read all six and
none does.

CONFIRMED / editorial.

### 5. profile-input-undefined (writer-01)

Claim: item 5's three-part argument for pinning the filter is true word for word
of channel layout, tile extents and declaration order, none of which the profile
pins, so under the "same arrays" reading the profile is incomplete and its
preamble's claim is false.

**Kill attempt — this one lands.** Item 2 itself forecloses the "same arrays"
reading: "Hashing the bytes rather than an abstract notion of 'content' is what
makes the identifier well defined: this format fixes no canonical serialization
of logical content, and **two files carrying the same arrays can legitimately
differ in tiling, layout, and codec**." The appendix expressly denies that
logical-content reproducibility is even well defined. Item 7 confirms the
division: "**The all-zero fill default.** Where a caller chooses no fill, the
writer records all-zero bytes" — fill is the caller's, and the profile pins only
the default. So "the same input" is the caller's full layer schema (tiling,
layout, declaration order, names, fill) and the items pin the *encoding knobs*
the caller does not state.

What survives: item 2's sentence lists codec alongside tiling and layout, and
item 1 pins codec — so the boundary between "input" and "knob" is drawn but
never stated, and "the same input" is nowhere defined (nor in [R-CNF-05], whose
word it borrows). That is a real legibility gap; the incompleteness charge is
not established.

**Byte-level: no.** "It adds no requirement to any actor: a writer ignoring it
is fully conforming" and [R-CNF-05]: "two conforming writers given identical
input MAY produce different conforming files." Every file either writer emits is
conforming under both readings.

PARTIAL / editorial.

### 6. appender-tier-list-asymmetric (writer-02)

"- **appender** — extends an existing file by commits (§9.2): adding layers or
records, superseding tiles, growing extents, amending metadata."

The list takes one half of each of two pairs §20.3 treats symmetrically: growing
but not shrinking, superseding but not unstoring; and it omits the §20.4 drop.
§20.3 permits all three expressly: "An extent MAY also **shrink**, and the bar
above is the whole of the test"; "entries for tiles that become unstored written
as the sentinel"; §20.4's table "Retain byte-identical, or drop it — its extent
becoming slack."

**Kill attempt.** §20's preamble reads "This section defines the writer tiers
and their procedures; like §19, it consolidates", and §19's parallel preamble is
explicit that its enumerations "are not the complete inventory". §20 does not
restate that disclaimer, which is why the finding is not empty. But the
constitutive reading is barred anyway, twice over: it would put §20.1 in direct
conflict with §20.3's MAY, and tier membership cannot bear on a file, since
[R-CNF-02] fixes that "File conformance is a pure predicate on bytes: it does
not depend on any reader, writer, or environment."

**Byte-level: no.** Quote deciding it: [R-CNF-02] above, plus §20.3's express
"An extent MAY also **shrink**". The narrow reading costs a tool work it could
have done; a whole-file rewrite it produces instead is itself conforming.

CONFIRMED / editorial.

### 7. ordinal-renumber-trigger-gloss (writer-03)

"…and every other entry byte-identical at its disk-ordinal position (a geometry
change renumbers ordinals wherever `[R-GEO-06]` moves them)."

Verified: [R-GEO-06] makes the planar disk ordinal "c · N + s … where c is the
channel's index (§3.1)", and §3.1 makes c positional ("a channel's **index** is
its 0-based position in that order, and the order is load-bearing"). A commit
reordering a planar layer's channel declarations moves ordinals with no geometry
change, and §20.3's bar does not catch it for a planar layer: each tile still
carries one channel, keeps its decoded size P·Bᶜ, its padding content and its
codec/filter. So the parenthetical's named trigger is under-inclusive, and it is
the document's only statement of *when* to recompute (§11.1's Rationale repeats
the same pairing).

**Kill attempt — this one lands on the byte question.** The parenthetical states
a case, not a closed trigger set: it says a geometry change renumbers ordinals
"wherever [R-GEO-06] moves them", not "only where". The governing clause is
exhaustive and admits one reading: "every other entry byte-identical at its
**disk-ordinal position**", the ordinal being [R-GEO-06]'s function of the
declarations in force.

**Byte-level: no.** Two premises, either sufficient. (a) The rule has one
reading, so a writer that leaves entries in place has made an implementation
error, not exercised a permitted reading. (b) Even granting the gloss-follower's
file, §21.7 fixes that "the ordinal mappings of [R-GEO-06] and [R-SER-01] are
satisfied by a structurally valid tile whatever values it carries" — so the
file's conformance status is the same under both readings and the emittable set
does not move; what distinguishes the two files is the caller's intended
reference array, which the format does not adjudicate.

*Premise to attack:* that "its disk-ordinal position" cannot be read as "the
position it previously held". I think the parenthetical rules that out — it
exists precisely to say ordinals renumber.

CONFIRMED / editorial. The repair is worth taking: name the trigger set.

### 8. s97-slack-disposal-missing-qualifier (verifier-01)

§9.7: "the walk passes over it, and the bytes it nominally addresses fall to
slack (§15.3)." §15.3: "any bytes it nominally addressed **that no other
claimant claims** fall to slack." The qualifier is dropped, and T8 (offset < 16)
and T9 (extent past F − 64) reach bytes §9.7 itself says are claimed: "The front
signature block at [0, 16) and the live trailer at [F − 64, F) are claimed by
the walk as well".

**Kill attempt — this one lands.** §5.2 defines slack as the complement, not
additively: "Every byte the live state does not claim is **slack**". Bytes
[0, 16) are claimed by the live state, so they are not slack under any reading
of §9.7 that survives its own defining rule. §9.7's own earlier sentence says
the same: "Bytes the walk does not reach are slack". So the document decides it
in two places, and the sentence at issue is a restatement citing §15.3.

**Byte-level: no.** Quote deciding it: §5.2's "Every byte the live state does
not claim is **slack**", plus [R-CNT-21]'s framing of the total as a report — "a
verifier that reaches a live state MUST report the total number of slack bytes".
Every file that can exhibit the divergence already carries a T6–T12 violation
and is nonconforming under both readings.

CONFIRMED (the restatement is imprecise) / editorial. One-clause repair.

### 9. slack-total-trigger-vs-exemption (verifier-02)

Claim: F20/F29 fall between a duty keyed to "reaches a live state" and an
exemption keyed to "before a live trailer is established", so they are
ungoverned.

**Kill attempt — this one lands.** §5.2 defines the live committed state as "the
front signature block, and every structure reachable from the live trailer
through the live directory's records, extent slots, and tile-index entries,
**together with the live directory and the live trailer**." The last clause is
unconditional: once the trailer validates, the directory and trailer are in the
live state whether or not any record parses. So the duty triggers. And
[R-CNT-21]'s next clause covers the case: "Where the walk of §9.7 does not
enumerate every region's claimants — whether because a **scope-level rejection**
ends that scope's enumeration … the verifier MUST report the total as partial."
F20 is a file-scope rejection. The exemption's own stated ground fails here
("there is no F and no live state to walk" — here there is an F, validated).
§5.2's Note confirms partial totals do not presuppose a completed live state:
"A partial total ([R-CNT-21]) reports what one verifier's incomplete walk left
unclaimed, which is a fact about that run".

So the case is governed, and governed to reading (2), which the reporter picked.
The residue is that the duty's trigger and the exemption's are worded
differently — a wobble worth tightening, not a hole.

**Byte-level: no.** F20/F29 is established either way; the divergence is one
report line. [R-CNT-21] makes the total a report, and §22.3 keeps it out of the
verdict: "Both are verifier-detected".

PARTIAL / editorial.

### 10. compaction-figure-unhatched-pad (diagrams-01)

Legend "▓ marks slack"; both rows draw `pad` as its own unhatched cell; the
output row carries no ▓. The pre-trailer pad is slack in the document's own
words twice: §5.2 "alignment and slab gaps, **the pre-trailer pad**, and
everything an earlier commit superseded" and §6.2 "Those bytes — the
**pre-trailer pad** — are slack (§5.2)".

**Kill attempt — partial.** Two defences exist. (i) "▓ marks slack" is a legend
for a symbol, not a partition claim, so an unhatched cell asserts nothing. (ii)
The same Example's closing prose does name the pad as slack: "Slack accumulates
a directory, a pad and a trailer per commit, plus a whole index region for each
layer a commit touched (§20.3)". That is weaker than §5.1's corrective ("the pad
and the ▓ runs are slack") because it is about accumulation across commits
rather than about the output row, but it is not nothing. Against both: the
figure draws `pad` as a peer cell beside `dir` and `tr`, which are live-state
structures, and §20.3's parallel figure scopes its legend expressly ("▓ marks
what the commit turned to slack"), so §20.5's is the outlier. The claim that a
compacted output generally carries slack is right: [R-LIF-02] step 5 pads to the
next 64-byte boundary, and §20.5 has the compactor honour "every declared layout
invariant … ([R-SLB-01], [R-SLB-03])", whose gaps §16.1 and §16.2 both call
slack.

**Byte-level: no.** [R-CNF-01]: "any text labeled *Note*, *Example*, or
*Rationale*" is non-normative, and this is "**Example — what compaction
reclaims.**" The output's pad and gaps are fixed by normative text
([R-LIF-02] step 5, [R-WRT-07]); a compactor following the figure's implication
could not produce a conforming file at all rather than a different one.

CONFIRMED / figure.

### 11. serve-unchanged-rows-cited-short (diagrams-04)

"…for several such rows it obliges the reader to serve the structure unchanged
(`[R-CNT-22]`, whose registered type keeps its fixed semantics; and
`[R-MTA-05]`, whose unsorted document readers process as they find it — F27 and
L48)."

I grouped the register rows by governing rule: [R-MTA-05] → F27, L48;
[R-CNT-22] → F28, L49. Four rows, and only two are named.

**Kill attempt — this one lands on the ambiguity charge.** The parenthetical is
"(X, whose …; and Y, whose … — rows)". The semicolon separates the two glosses
and the em-dash sits inside Y's, so the appositive binds to [R-MTA-05]. Under
that reading the sentence is true: there are four such rows ("several" reads
correctly over four), and the citation names the two belonging to the second
rule. Reading B would make a checkable statement false, which is a reason to
reject it rather than to call the sentence ambiguous. So what is actually wrong
is an asymmetric citation, not an ambiguity.

**Byte-level: no.** Each rule states the reader's behavior in its own text —
[R-CNT-22]: "conforming readers nevertheless process the record under the fixed
semantics"; [R-MTA-05]: "readers process the document unchanged" — and §21.1
adds "where a row and the rule it cites diverge, **the rule governs**."

PARTIAL / register-bookkeeping.

### 12. t5-witness-omitted-from-t26 (register-01)

Two §21.7 sentences and T26's own cell give different answers.

- §21.7, first: "a mis-ordered image is then witnessed by T2, T4 or T5, exactly
  as a mis-strided filter is".
- §21.7, later: "where the resulting image breaks §14.5's padding content or
  `[R-SER-08]`'s bool bytes, the check that detects it is T2's or T4's, exactly
  as T26 has it".
- T26's cell: "…the check that detects it is T2's or T4's".

I built the witness rather than reasoning about it. Rank 1, E = T = 44, planar
bool: P = 44, no padding positions (E mod T = 0), decoded size ⌈44/8⌉ = 6 bytes,
P mod 8 = 4 so four pad bits exist. §17.3 mandates s = 1 (identity) for a packed
boolean plane. Filter at s = 2 gives n = 3, a non-identity permutation, which
moves some other byte into the final position; its high four bits are then
generally not the fill bit. T4 has no padding position to check, T2 is
interleaved-only, so **T5 is the sole witness** — and T26's own Instances cell
ranges over exactly this case ("packed planar bool: identity s = 1"). T26's
scoping clause is broader than the two checks it names, because §14.5 fixes both
kinds of content: "at every padding position, a writer MUST encode … that
channel's fill value" and "Every pad bit (§14.3) MUST carry the plane's
channel's fill bit", which the register splits into T4 and T5, with §14.3's Note
insisting "Pad bits are not padding positions (§11.3)."

**Kill attempt.** I looked for a sentence folding pad bits into T4 or excluding
them from T26's scope. §14.3's Note does the opposite. T26's governing rule
[R-COD-10] names no row at all ("a verifier detects it as a validity error at
tile scope"), so §21.1's "the rule governs" leaves the row's row-naming as an
under-inclusive restatement rather than something the rule corrects. **Not
found. This is the group I tried hardest to kill and failed.**

**Byte-level: no.** [R-SER-05] decides it independently of T26: "A conforming
reader never returns this content ([R-GEO-04]) and is not obligated to check it;
**a verifier MUST check it**, and a violation is a validity error at tile
scope." So the file is refused at tile scope, and barred to a conforming writer
by [R-CNF-05], under either reading. What moves is attribution and which path a
T26 corpus vector exercises — and §24 already handles multi-row attribution:
"where a condition cannot be isolated … the entry records every row the file
exercises and says which it was built for."

*Premise to attack:* that a pad-bit violation is established by T5 whatever the
verifier concludes about T26. If [R-SER-05]'s pad-bit clause were somehow
conditioned on the filter being correct, the downgrade would fail; it is not —
it is unconditional over every packed plane.

CONFIRMED / register-bookkeeping. Highest-value repair in the batch alongside
group 13.

### 13. experimental-encoding-exception-over-r2 (register-02)

§21.5 preamble: "every way its document can be unreadable takes this outcome,
whatever the containing scope — as a violation in the rows below, except at an
experimental-range encoding, where no document rule attaches and §21.6 records
the defined non-violation ([R-MTA-10])…". [R-CNT-25] enumerates those ways with
"a failed extent CRC" first, and R2's row is unqualified by encoding.

I took this one seriously as a byte-level candidate, because the broad reading
genuinely would fork a verdict: one verifier certifying a file whose
user-metadata extent CRC fails at encoding ≥ 0x80, another reporting
nonconforming. So I pushed on whether the broad reading is *permitted*.

Grammatically it is tempting — "where no document rule attaches" reads most
naturally as modifying "an experimental-range encoding", not the failure mode,
which would sweep every failure mode including the CRC. But four normative
passages defeat it, and the first is the sentence immediately following:

1. §21.5's own next sentence: "Encoding 0 and a reserved-range value are
   unassigned too, and R1 registers both as violations: **what [R-MTA-10]
   withdraws is the document's content rules**, never the encoding byte's own
   value set (`[R-MTA-03]`)." A failed extent CRC is not a document content
   rule.
2. [R-MTA-10], the rule the exception itself cites, in an express closed list:
   "file conformance … is decided by the structural checks that precede the
   document alone: the record's framing and extent slot (`[R-CNT-13]`), the
   encoding byte's own value set (`[R-MTA-03]`), and **the extent's terminal CRC
   (`[R-CNT-20]`)**."
3. §22.3 [R-SEC-04]: "the extent of a user-metadata record under an unassigned
   encoding **is covered by its terminal CRC** but constrained by no content
   rule (`[R-MTA-10]`)".
4. §8.1's map states a checksum for "User-metadata extent" with no encoding
   qualifier, and §9.7 obliges the walk to check "that each verifies against the
   checksum covering it, where §8.1's map states one".

Weakness in my own kill, stated honestly: §21.1's express "the rule governs"
clause is written about *rows* and about §21.6 *entries*, not about §21.5's
preamble prose, so I cannot invoke it directly; I rely instead on the settled
principle the document states for the registry — [R-EXT-05], "the section that
defines the space governs … (§21.1 applies the same principle to the error
register)" — plus the four passages above, of which (1) sits in the very same
paragraph. Also cutting slightly the other way: the preamble says expressly that
R1 survives at an unassigned encoding and says nothing about R2, which invites
an expressio-unius inference. That asymmetry is exactly what wants repairing.

**Byte-level: no.** Deciding quote: [R-MTA-10]'s closed list above, which names
"the extent's terminal CRC (`[R-CNT-20]`)" as one of the checks that decide
conformance there. A verifier reading the rule the preamble cites lands on the
narrow reading, so the verdict does not actually fork.

*Premise to attack, and the one I would attack if I were the next reader:* that
a preamble clause cannot defeat the rule it cites, when §21.1's express
precedence clause reaches rows and §21.6 entries but not §21.5 preamble prose.
If a reader rejects that, the broad reading becomes permitted and this group is
byte-level. I judge it defeated by the immediately following sentence, which is
in the same paragraph and states the reach of the withdrawal directly.

PARTIAL (the hazard is real; two *permitted* readings are not) /
register-bookkeeping. Repair it first.

### 14. partial-product-not-designated (adversary-01)

I checked the construction: rank 3, dims (E = 2⁶², T = 1), (3, 1), (0, 1),
interleaved, C = 1 uint8. G = (2⁶², 3, 0), N = 0, P = 1, N·P = 0, C·N = 0,
P·Q = 1, entry_count = 0, extent slot (0, 0), crc_of_crc_array = 0. [R-CNT-17]'s
formula gives 0. Conforming. G₀·G₁ = 3·2⁶² > 2⁶³ − 1.

**Kill attempt — this one lands outright, and the reporter's own counter-pressure
evaporates on inspection.** [R-ENC-04]: "A designation is express, made by the
section that defines the quantity; an expression this specification writes only
inside a comparison, and names nowhere, is not a designated quantity and no
reader is obliged to form it." §11.2 designates N, P, the addressed-tile count
and N·P, and nothing smaller. A partial product is written nowhere at all — a
fortiori not designated. And [R-SEC-02], cited as pushing the other way, is
expressly limited by the same word: "Every declaration-derived sum and product
**`[R-ENC-04]` designates** is overflow-checked before use." It does not push the
other way. The document also shows its method twice: §11.2's Note against the
additive idiom, and §11.3's "stated in a form that forms no product (§4.2)".

**Byte-level: no**, and no defect. Quote: [R-ENC-04]'s non-designation clause
above. The reporter reaches the same conclusion and files the cost of reaching
it; but the reasoning that closes it is normative and express in two rules, not
supplied by a Rationale.

REFUTED / none. Optional legibility addition only.

### 15. compaction-regeneration-trigger (adversary-03)

"…except that relocation re-points extent slots, regenerates each **relocated**
tile-index region…". The scenario is constructible: §20.5 grants "it is free to
place structures anywhere §5.2 admits", so a compactor may pack every tile
(moving all of them) and land a region back at its original offset.

**Kill attempt — the literal reading is barred, but by the surrounding text
rather than by the trigger clause.** "The output's reference arrays MUST equal
the live generation's bit for bit (`[R-MDL-02]`)"; "Given a conforming input the
output is a conforming file"; and the regeneration paragraph's own operative
sentence, "every other entry is re-pointed to where its stored extent now lies."
The §20.5 Example supplies the purposive ground: the index region is "the one
kind this operation regenerates rather than copies, **since its entries carry
the offsets that moved**." So the trigger clause names the wrong condition while
the section forbids the outcome that condition would produce.

**Byte-level: no.** Quote deciding it: "The output's reference arrays MUST equal
the live generation's bit for bit (`[R-MDL-02]`)". A literal-reading output with
stale entry offsets is nonconforming (its entries' crcs cannot match whatever
now occupies those bytes — T1 — and the extents collide with other claimants —
F33), so [R-CNF-05] bars a conforming writer from emitting it under both
readings.

CONFIRMED / editorial.

### 16. l23-detected-tier (adversary-04)

L23's Detected cell reads "layer access"; §19.1 step 4 forces the name-field
determination at the open ("a layer record whose name field does not lie
entirely within that record's inline_length yields no name field to compare, so
it contributes no name to the namespace and is instead a validity error at layer
scope"), and §19.2 lists "the layer-name namespace (§19.1's steps)" at open.

**Kill attempt — this one lands.** §21.1 defines the column as a deadline, not a
tier of performance: "the point **by which** detection is due (§19.2)". And
[R-RDR-02] fixes latest, not exact: "A reader MUST detect each violation … **no
later than** the reader's first reliance on the structure that carries it… A
reader MAY detect any violation earlier". Its Rationale says so outright: "The
rule fixes the *latest* detection point". A reader that determines the name
field's fit at open has met a layer-access deadline early. So the cell is not in
divergence with §19.1 at all; it is a loose deadline for one of the row's four
instances.

**Byte-level: no**, and the reporter agrees: the layer is reject-layer either
way and F4's namespace is built from the same names either way.

PARTIAL / register-bookkeeping.

### 17. should-consequence-universal (adversary-05)

§2.1's Note: "every SHOULD states the consequence of deviation."

I spot-checked roughly twenty SHOULDs rather than trusting the census.
Consequence stated: [R-CNT-26], [R-ENC-14], [R-LIF-07], [R-CNT-09], [R-COD-06],
[R-CNT-10], [R-TYP-10], [R-SEC-03], [R-PRV-05], [R-LIF-03], [R-CNT-07],
[R-CNT-20], [R-MTA-06], §20.3's new-file SHOULD, §20.4's drop-report SHOULD,
§20.3 step 2's carry-forward-report SHOULD, §20.5's version_minor floor.
Not stated: [R-MTA-09]'s "the verifier SHOULD report the bound it applied and
the stored length of the extent it declined" — I searched its paragraph and the
§21.9 material and found no consequence anywhere. Also [R-SLB-01] ("which
writers SHOULD zero and no conformance requirement constrains") and [R-SLB-03]
("which writers SHOULD zero"), both restating [R-CNT-03] without its consequence
clause; and [R-PRV-03]'s pair.

**Kill attempt.** The charitable scoping — the Note is about *requirements*, so a
restatement of an existing SHOULD need not repeat the consequence — rescues the
[R-SLB-01]/[R-SLB-03] cases but not [R-MTA-09]'s reporting duty, which is a
unique obligation stated once. So the universal is falsified by at least one
case. Not killed.

**Byte-level: no.** [R-CNF-01] makes a *Note* non-normative, and [R-CNF-12]
puts SHOULD deviation outside the register entirely: "Deviation from a SHOULD is
not a violation for this purpose: §21's register enumerates MUST-level
conditions only."

CONFIRMED (weakest surviving group in the batch) / editorial.

### 18. s204-table-unidentified (quiz-01)

Two checks, both confirmed against the text.

(i) §20.4's preservation paragraph and table sit between two identifiers and
carry none: "[R-WRT-05]" closes the paragraph before ("…is new output under its
writer obligations (`[R-CNF-05]`). `[R-WRT-05]`"), and "[R-WRT-08]" closes a
later paragraph whose own sentence is about re-encoding and relocation. §2.2:
"Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`."

(ii) §21.6's row cites "`[R-CNT-15]`, `[R-WRT-08]`" for "Ignored, and preserved
or dropped per its PE bit". [R-WRT-08]'s text is "An updater MUST NOT re-encode
a record whose type it does not implement, and MUST NOT modify one except by
relocating its extent and re-pointing its slot under §20.5" — it says nothing
about dropping per the PE bit. The citation points at the nearest identifier
because the governing text has none, which is evidence for (i) rather than a
separate accident.

**Kill attempt.** The obligations are reachable: [R-CNF-06] "MUST honor the
preservation obligations of §20.4" and §2.4's row "§20.4's table states the
cases: its MU = 1 and MU = 0 / PE = 1 rows." And the corpus cost the reporter
names is smaller than claimed: [R-VEC-02]'s identifier duty runs to register
rows, and §20.4's preservation duties carry none (that is group 3's subject), so
no vector needs to cite one.

**Byte-level: no.** [R-CNF-01] makes the unidentified text normative regardless
("All text in this document is normative except…" — the table carries no *Note*,
*Example* or *Rationale* label), and [R-CNF-06] binds updaters to it by section
reference. Both readings oblige exactly the same retention and permit exactly
the same drops.

CONFIRMED / editorial.

---

## Byte-level tally

0 of 18 groups. Every reporter self-flagged non-byte-level and I did not
overturn any of them, so no reporter flag was downgraded — but I did test group
13 (register-02) as a byte-level candidate on its own merits, because the broad
reading there would genuinely fork a verifier's verdict, and groups 12 and 7 as
runners-up. The premises of all three downgrades are stated above in a form
someone else can attack.

Groups I tried hardest to kill and failed: **12 (t5-witness-omitted-from-t26)** —
no sentence anywhere folds pad bits into T4 or scopes T26 away from them, and
§14.3's Note insists on the distinction; and **17** and **1**, where the
universals are simply falsified by constructible cases.

Groups where the kill landed: 5, 9, 11, 13 (partly), 14 (outright), 16.

## Coverage

22 input ids. Union of member_ids = the 22 input ids, no duplicates, no
omissions. Counted twice by hand against the list in the brief.
