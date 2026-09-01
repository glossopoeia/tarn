# Round 28 triage — correctness lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, the whole
  file (4648 lines), in five reads plus a tail read: lines 1–200, 200–1099,
  1100–1999, 2000–2899, 2900–3519, 3520–3918, 3919–4318, 4318–4648.
- Two `grep`/`sed` checks against the same file: a count of lines containing
  `SHOULD` (44, matching adversary-05's census claim), the location of
  `SHOULD report the bound` and of each `SHOULD zero`, and the literal text of
  §20.1's writer-tier list.

I opened **no** walk transcript, no other triage pass's notes, no `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or
the web. I ran no directory listing of the round28 scratch directory or of my
own output directory beyond `mkdir -p` on the output path I was given.

## Grouping

22 input ids → 18 groups. Three merges:

- `verifier-03` + `diagrams-02` + `adversary-06` — all three attack the same
  clause, Appendix G item 5's "elsewhere it changes the stored bytes of every
  tile it touches", with the same counterexample class (an image the
  permutation fixes). Different witnesses, one defect.
- `diagrams-03` + `quiz-02` — both attack §21.6's zero-layers row's "with an
  empty directory", both citing [R-CNT-14]'s file-scope user-metadata
  permission and both noting [R-CNT-14]'s own parenthetical makes the same
  slide.
- `diagrams-05` + `adversary-02` — both attack §21.7's second-paragraph
  inventory of unwitnessed obligations for omitting §20.4's preservation
  duties. adversary-02 names one further omitted member ([R-CNT-08]'s updater
  ignore-lane carry-forward, whose compactor twin §21.7 *does* name); that is
  another instance of the same omission at the same location, not a second
  defect.

Everything else is a singleton. Every input id lands in exactly one group.

## Findings checked, one by one

### 1. reader-01 — the opening blockquote

[R-CNF-01] (line 104): "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative."

The block at line 12 is "**How to read this document** *(non-normative).*". It
is not §1 (§1 begins at line 28), not labeled Note/Example/Rationale, not an
appendix. So under [R-CNF-01] it is normative while calling itself
non-normative. Quotation accurate, context accurate. The reporter's control
case checks too: §15.1's unlabelled blockquote (line 2124) carries the
tile-index region layout and is normative, which [R-CNT-17]'s extent-length
formula needs.

Byte-level: no. The block's content is about the document's own rubric,
layout-table columns, field taxonomy and vector citation practice. Nothing in
it constrains a field, an offset, an enum or an outcome. CONFIRMED, editorial.

### 2. writer-01 — Appendix G's preamble against its items

Preamble (4433): the profile "closes the degrees of freedom this format
deliberately leaves open". Items 1–10 pin codec/encoder, file_id, emission and
record order, one generation, alignment/slab and filter, all-fill sentinel,
fill default, version_minor/flags, metadata producer, NFC names. Nothing pins
channel layout, tile extents, or dimension/channel declaration order. The
closing paragraph's enumeration of what the items add (4560–4575) names none of
the three either. Verified by reading all ten items.

The asymmetry the reporter names is real and checkable: **filter** is a u16
field of the layer record and the profile pins it with a three-part argument
(§17.3 leaves it to the writer, no content implies it, unpinned writers
diverge); **layout** is a u8 field of the same record and the same three
clauses hold of it verbatim (§14.4's Note: the two layouts give different tile
images for any bool channel), and it is not pinned. Same for tile extents
(§11.3's Note: "Tile extents are a writer's choice, and this specification
imposes none") and for declaration order (§3.1: "the declared order is
load-bearing").

One correction to the reporter's reasoning, which does not change the verdict:
item 1 is not redundant under reading (A). Its operative content is the
*encoder implementation and settings*, not the codec ID — "RFC 1951 and RFC
8878 constrain what a decoder accepts, not how an encoder chooses blocks" —
and that is a degree of freedom no layer schema supplies. Item 5's filter
clause is the one that is a bare layer-record field. So the defect is narrower
than "the profile is incomplete under reading (B)": it is that item 5 pins one
layer-record field on an argument the profile does not apply to the others.
That is still a defect in the same sentence, so CONFIRMED rather than PARTIAL.

Byte-level: no. "It adds no requirement to any actor: a writer ignoring it is
fully conforming" (4436), and [R-CNF-05] licenses exactly the divergence at
issue.

### 3. writer-02 — §20.1's appender definition

Text confirmed verbatim by `sed`: "**appender** — extends an existing file by
commits (§9.2): adding layers or records, superseding tiles, growing extents,
amending metadata."

§20.3 permits, in a commit: shrinking an extent ("An extent MAY also
**shrink**", 3165); unstoring ("entries for tiles that become unstored written
as the sentinel", 3117); §20.4's table permits dropping an MU = 0 / PE = 0
record. All three are absent from §20.1's list, and the list takes one half of
each of two pairs (growing/not shrinking, superseding/not unstoring).

The defining clause is "extends an existing file by commits (§9.2)"; the colon
list is illustrative, and reading it as constitutive would put §20.1 in direct
conflict with §20.3's own permissions. No byte fork: the appender's permitted
outputs are fixed by §20.3 and §20.4, neither of which is ambiguous here.
CONFIRMED, editorial.

### 4. writer-03 — the disk-ordinal renumbering gloss

Text (3119): "and every other entry byte-identical at its disk-ordinal position
(a geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)".

[R-GEO-06]: the planar disk ordinal is "**c · N + s** ... where c is the
channel's index (§3.1)". §3.1: "a channel's **index** is its 0-based position
in that order, and the order is load-bearing". So inserting, removing or
reordering a planar layer's channel declarations moves ordinals with no change
to any extent or tile extent. Verified against §20.3's bar (3126–3143): for a
planar layer the bar's four items are the padding-position set and its
[R-SER-05] content, the decoded size, a sample's byte offset within the decoded
image, and the codec and filter. A channel-set change moves none of them for a
planar tile — each tile still carries one channel, its decoded size is still
P·Bᶜ for that channel, its padding content is still that channel's fill — so
the commit is permitted, and the gloss's "geometry change" does not name it.
For an interleaved layer the same change moves Fᶜ = Σ_{j<c} Bⱼ, so the bar
catches it; the gap is planar-specific, as the reporter says.

Byte-level: no. The governing clause says the entry is byte-identical *at its
disk-ordinal position*, and the parenthetical is not phrased as a restriction —
it says a geometry change renumbers, not that only a geometry change does. A
writer that follows the parenthetical instead of the rule has made an
implementation error; where the resulting file is detectable it fires T4, and
where it is not, what distinguishes the two files is the caller's intended
reference array, which this format does not adjudicate. CONFIRMED, editorial.

### 5. verifier-01 — §9.7's disposal sentence

§15.3 (2168): "and none to `[R-LIF-08]`'s coverage walk, so any bytes it
nominally addressed **that no other claimant claims** fall to slack."
§9.7 (1477): "the walk passes over it, and the bytes it nominally addresses
fall to slack (§15.3)." The qualifier is dropped. Quotation accurate.

The gap bites on three of §15.3's six structural rows: offset < 16 (T8) reaches
the front block, which §9.7 itself calls claimed ("The front signature block at
[0, 16) and the live trailer at [F − 64, F) are claimed by the walk as well");
offset + length > F − 64 (T9) reaches the live trailer; T6/T7 carry offset
2⁶⁴ − 1 and address nothing in the file. Read literally §9.7 would put
[0, 16) or [F − 64, F) in two classes, which [R-CNT-02]'s "belongs to exactly
one of" forbids.

Three passages already decide it against the literal reading: §15.3's
qualifier, [R-CNT-02]'s partition, and §5.2's own definition — "Every byte the
live state does not claim is **slack**" — under which a claimed byte cannot be
slack at all. §9.7's sentence cites §15.3 for its authority, so it is a
restatement.

Byte-level: no. Every file that can exhibit the divergence already carries a
T6–T12 violation and is nonconforming under both readings; what moves is a
figure on a verifier's report line, which [R-CNT-21] makes a report and not a
verdict. CONFIRMED, editorial.

### 6. verifier-02 — the slack-total trigger and its exemption

[R-CNT-21] (699–706): "a verifier that reaches a live state MUST report the
total ... Where §6.2's ordered validation rejects the file before a live
trailer is established there is no F and no live state to walk, so the total is
not owed at all".

The reporter is right that the duty's trigger ("reaches a live state") and the
exemption's trigger ("before a live trailer is established") are not
complementary, and that F20 (directory-region CRC) and F29 (record-sequence
framing) fall between them.

But the case is **not ungoverned**, and this is where the finding overstates.
§9.7 [R-LIF-08] (1473): "Where the walk does not complete — a scope-level
rejection blocks enumeration, or the verifier stops at the first violation
(`[R-CNF-11]`) — the sum is reported as partial, and `[R-CNT-21]` governs what
such a total counts and what the verifier reports beside it." A directory-CRC
failure is a file-scope rejection that blocks enumeration, and the walk does
begin: §9.7 starts it "From the live trailer", which here is valid. So the
document answers the case, and answers it with the reporter's own reading (2).
[R-CNT-21]'s third clause says the same on its own terms ("a scope-level
rejection ends that scope's enumeration").

So: PARTIAL. Real defect = §5.2's duty/exemption pair is phrased so that only
§9.7 joins it up; the sentence is not self-contained. Not the defect the
reporter described (two defensible readings, verifiers diverging), because
§9.7's rule governs.

Byte-level: no under either account — F20/F29 is established either way and the
verdict is *nonconforming*.

### 7. verifier-03 + diagrams-02 + adversary-06 — Appendix G item 5's universal

Clause (4517): "The filter is the identity exactly where its permutation is —
where the stride is 1 ... and equally where the decoded image is a single
group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the stored bytes of
every tile it touches."

First half checked: [R-COD-10] sends byte i of group j from j·s + i to i·n + j.
Identity for all i, j iff s = 1 or n = 1 (i = 1, j = 0 forces n = 1; i = 0,
j = 1 forces s = 1). Correct as all three reporters state.

Final clause: false. Any image invariant under the permutation is a fixed
point, and such images are legal. Checked all three witnesses:
- adversary-06: interleaved, C = 2 uint8, P = 8, L = 16, s = Q = 2, n = 8, all
  16 bytes 0x00 with nonzero fills so item 6 does not remove it. Any constant
  image is fixed by any byte permutation.
- diagrams-02: interleaved, C = 2 uint8, P = 2, L = 4, s = 2, n = 2. Mapping
  computed: b0 b1 b2 b3 → b0 b2 b1 b3, identity on any image with b1 = b2, e.g.
  `07 07 07 09`. Verified by hand.
- verifier-03: uint16 channel, every byte 0xAB, fill 0x0000, s = 2. Fixed.
Nothing in §12.3, §13.2, §14.2, §14.5 or §15.3 excludes such tiles; only item 6
excludes all-*fill* tiles.

adversary-06's stronger lemma checks too and I use it again in §12 below:
filtered[0] = image[0] always, and taking i = s − 1, j = n − 1 gives
(s − 1)n + n − 1 = L − 1 and (n − 1)s + s − 1 = L − 1, so the byte at offset
L − 1 is fixed by **every** legal stride.

Byte-level: no. Appendix G is identified as non-normative; the item's operative
instruction (pin the filter value) is untouched — the filter is a layer-record
field, so two writers disagreeing about it emit different layer records
whatever the payload does. CONFIRMED, editorial.

### 8. diagrams-01 — §20.5's compaction figure

Legend (3438): "Regions, not offsets; ▓ marks slack." Both rows draw `pad` as
its own unhatched cell and the output row carries no ▓.

The pre-trailer pad is slack twice over in the document's own words: §5.2
("alignment and slab gaps, the pre-trailer pad, and everything an earlier
commit superseded") and §6.2 ("Those bytes — the **pre-trailer pad** — are
slack (§5.2)"). So the figure mis-classifies a region under its own legend.

The three parallel figures check out as the reporter says: §5.1's has the same
unqualified legend but a correcting sentence ("the pad and the ▓ runs are
slack"); §9.2's scopes its legend to the two rows; §20.3's scopes it to "what
the commit turned to slack", under which an unhatched fresh pad is correct.
§20.5's is the one with an unscoped legend and no corrective.

The output row's stronger implication is checkable and wrong: §20.5 requires
"A compactor MUST follow `[R-LIF-02]`'s **creation path**", whose step 5 pads
to the next 64-byte boundary, and [R-WRT-07] has the compactor honour
[R-SLB-01]/[R-SLB-03], whose gaps §16.1 and §16.2 both call slack.

Byte-level: no. Labelled *Example*, non-normative under [R-CNF-01], and the
normative text fixes the output's pad and gaps. CONFIRMED, figure.

### 9. diagrams-03 + quiz-02 — §21.6's zero-layers row

Row (3759): "| The file contains zero layers | A conforming file with an empty
directory | `[R-CNT-14]` (R-CNT-02) |".

[R-CNT-14] permits, with no dependence on the layer count, "at most one
file-scope user-metadata record", and [R-CNT-15] plus §21.6's own
experimental-MU=0 row make an unknown ancillary record conforming. So a
zero-layer file may carry a non-empty directory; diagrams-03's witness (a
single type-0x0002 record: 24-byte header + 1-byte inline payload + the
directory's 4-byte terminal CRC) is conforming. The Defined-behavior cell
answers with a conjunction the Condition cell does not carry.

Both reporters independently note that [R-CNT-14]'s own parenthetical repeats
the slide — "zero is valid: an empty directory is a conforming generation" —
which states a sufficient case in a place a reader reads as the answer. Checked
§5.1's Example, which does *not* make the move: "It contains no layers (a
valid, empty file)" is about one 128-byte file.

Byte-level: no. §21.6 lists non-violations; a case its list does not cover is
not thereby a violation, since the register's normative completeness runs to
§21.2–§21.5 and no row there covers it. §21.1's "the rule governs" applies
expressly to §21.6 entries. CONFIRMED, register-bookkeeping.

### 10. diagrams-04 — §21.1's "several such rows"

Text (3556): "... for several such rows it obliges the reader to serve the
structure unchanged (`[R-CNT-22]`, whose registered type keeps its fixed
semantics; and `[R-MTA-05]`, whose unsorted document readers process as they
find it — F27 and L48)."

Verified the row-to-rule mapping from §21.2/§21.3: F27 and L48 are governed by
[R-MTA-05]; F28 and L49 by [R-CNT-22]. So the trailing citation names only one
of the two rules' rows. Under the appositive-on-the-second-conjunct reading the
sentence is true but short; under the whole-parenthetical reading it is false.
"Several" over two rows is what invites the second reading, exactly as the
reporter says.

I note in passing that the set may be larger still: [R-CNT-12]'s reserved-flag
and MU = 1 / PE = 0 rows (F25, F26, L46, L47) also oblige a reader to process
the record unchanged ("readers MUST ignore them"; "MUST treat the record as
PE = 1"), and §7.2 says of both that they leave "conforming behavior
unchanged". That makes the citation short under any reading, which strengthens
rather than changes the finding.

Byte-level: no. [R-CNT-22] and [R-MTA-05] each state the reader's behaviour in
their own text. CONFIRMED, register-bookkeeping.

### 11. diagrams-05 + adversary-02 — §21.7's inventory

§21.7's second paragraph (3821–3874) itemises by identifier: [R-LIF-01],
[R-LIF-02]; [R-GEO-06] and [R-SER-01]; [R-CNT-13]'s embedded-offset bar;
[R-CNT-18]'s nesting bar; §20.3 step 4's declaration bar; §20.5's three trailer
obligations ([R-WRT-06]); [R-ENC-06]. Verified.

Omitted, and of exactly the named kind:
- [R-WRT-05]'s byte-identical re-emission and §20.4's table's drop restriction.
  §20.4's own Rationale supplies the account in almost §21.7's words: "Put that
  way the claim is a commit's own and holds whether or not an observer can pair
  the two directories. It cannot, from the format ... Adjacency is a fact about
  a file's history, which §9.7 does not reconstruct." That is a Rationale, so
  non-normative; §21.7 is where the account belongs and is silent.
- [R-WRT-08]'s bar on re-encoding an unimplemented type.
- [R-CNT-08]'s "An updater MUST copy forward unknown ignore-lane bits ... and
  MUST NOT clear them" (adversary-02). The superseded trailer survives only as
  slack, whose content is unconstrained and which a reader "MUST NOT
  interpret", so no single file witnesses the clearing — which is the very
  reason §21.7 gives for naming the compactor's identical duty under
  [R-WRT-06]. The asymmetry is real.

Against the finding: §21.1 expressly exempts §21.7 from the register's
normative completeness clause — "neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations, §21.7's
account of what no check detects, or §21.9's limits". So an incomplete §21.7 is
not a defect by [R-ERR-02]'s own terms; both reporters saw this and picked the
by-class/exemplar reading. The claims are accurate all the same, and §21.7's
opening ("A second set of obligations is omitted from the register because a
single file exhibits no witness of their violation") followed by a
by-identifier itemisation reads as an inventory.

Byte-level: no — these obligations are unwitnessed under every reading, which
is the point. CONFIRMED, editorial, with the repair marked discretionary.

### 12. register-01 — T5 in §21.7's first sentence

Both quotations verified verbatim:
- 3827: "the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by
  a structurally valid tile whatever values it carries, except where §14
  constrains a byte's content — a padding position, a pad bit, or an
  interleaved boolean — and a mis-ordered image is then witnessed by T2, T4 or
  T5, exactly as a mis-strided filter is;"
- 3849: "where the resulting image breaks §14.5's padding content or
  `[R-SER-08]`'s bool bytes, the check that detects it is T2's or T4's, exactly
  as T26 has it, and where it breaks neither there is no witness."
- T26's cell: "the check that detects it is T2's or T4's".

The inconsistency is real: one sentence includes T5 for a mis-strided filter,
the other two exclude it. **But the reporter resolves it the wrong way.**

T5's condition is exclusively about the *final byte's* pad bits: "In a packed
planar bool plane with P mod 8 ≠ 0, a final-byte pad bit (bit positions
P mod 8 through 7) is not the channel's fill bit." And the byte-shuffle fixes
offset L − 1 at every legal stride: with i = s − 1, j = n − 1, the source
offset is (n − 1)s + s − 1 = L − 1 and the destination is (s − 1)n + n − 1 =
L − 1. (Same lemma adversary-06 proved independently in this round.) So for a
packed bool plane — where the mandated stride is 1, the mandated filter the
identity, and the reader therefore takes the writer's shuffled bytes as the
decoded image — the final byte, and with it every pad bit, survives a wrong
stride untouched. T5 cannot fire on a mis-strided filter. T4 can (padding
positions in non-final bytes move), and T2 can (a bool channel's byte position
comes to hold a numeric byte).

T5 *is* a genuine witness for the other half of that sentence, the ordinal
mappings: a planar tile stored at a disk ordinal belonging to a different
channel carries that other channel's fill in its pad bits, and where the two
channels' bool fills differ the verifier's check against the declared channel's
fill bit fires T5. That is why the sentence lists three rows against the three
structurally constrained content kinds. What is wrong is the trailing "exactly
as a mis-strided filter is", which imports T5 into the filter case.

Caveat stated honestly: this analysis assumes the wrong stride divides L, which
is the only case [R-COD-10]'s shuffle is defined for ("Viewing the image as
n = L/s consecutive groups of s bytes"). A writer using a stride that does not
divide L is doing something this document does not define, and nothing follows
about which byte lands last. T26's condition does not require the wrong stride
to divide L, so a pedant can reach T5 through undefined writer behaviour; the
drafter plainly reasoned inside the defined model, and so do I.

Consequence for the repair: taking the reporter's advice would add to T26 a row
that cannot fire within the defined shuffle and would ask a corpus builder for
a T26 pad-bit vector that is not constructible. The repair belongs in §21.7's
first sentence instead.

Byte-level: no. [R-SER-05] obliges a verifier to check every padding position
and every pad bit whatever it concludes about T26, and §9.7 and §17.4 make the
decoded-content obligations a verifier's regardless; the file is nonconforming
and refused at tile scope under either account. Only attribution moves.
PARTIAL, register-bookkeeping.

### 13. register-02 — §21.5's experimental-encoding exception

§21.5 preamble (3719): "User metadata is quarantined (`[R-CNT-25]`): every way
its document can be unreadable takes this outcome, whatever the containing
scope — as a violation in the rows below, except at an experimental-range
encoding, where no document rule attaches and §21.6 records the defined
non-violation (`[R-MTA-10]`) ..."

[R-CNT-25] enumerates the ways with the CRC first: "each way a user-metadata
record's document can be unreadable once its framing has been read — a failed
extent CRC, an unimplemented or invalid encoding, a decode failure, or content
violating the document's own rules ... — is ignore-record". R2's row is
unqualified by encoding. So on the preamble's own terms the broad reading is
available: a failed extent CRC at an experimental encoding would fall into the
exception and out of R2. The reporter's reading of the sentence is accurate.

What decides it, and decides it against the broad reading, is [R-MTA-10] — the
rule the preamble itself cites for the exception: "file conformance ... is
decided by the structural checks that precede the document alone: the record's
framing and extent slot (`[R-CNT-13]`), the encoding byte's own value set
(`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)." An express,
closed list naming the CRC. §22.3 [R-SEC-04] says it again: "the extent of a
user-metadata record under an unassigned encoding is covered by its terminal
CRC but constrained by no content rule (`[R-MTA-10]`)". §8.1's map states a
checksum for every user-metadata extent with no encoding qualifier, and §9.7
obliges the walk to check "each ... against the checksum covering it, where
§8.1's map states one".

The preamble carries no requirement identifier of its own and cites [R-CNT-25]
and [R-MTA-10] as its authorities, so it is restatement and the rules govern —
§21.1's principle, stated there for rows and for §21.6 entries alike. The
preamble's very next sentence already carves the encoding byte's value set back
out, which shows the intended scope of the exception is content rules.

Byte-level: no, on that quotation. This was my closest call: if the broad
reading were permitted, one verifier certifies a file with a corrupt
user-metadata extent and another reports nonconforming, which is an accept/
reject fork. It is not permitted, because [R-MTA-10] expressly names the CRC
among the checks that decide conformance there. CONFIRMED, register-bookkeeping
— worth repairing precisely because the sentence invites an error three
sections away from its correction.

### 14. adversary-01 — the partial product with a zero factor

Construction checked: rank 3, (E, T) = (2⁶², 1), (3, 1), (0, 1) gives
G = (2⁶², 3, 0), N = 0, P = 1, N·P = 0, C·N = 0, P·Q = 1, entry_count = 0 with
extent slot (0, 0) and crc_of_crc_array = 0, satisfying [R-CNT-17] and
[R-CNT-23]. Every field within 2⁶³ − 1. [R-GEO-02] makes the zero extent valid.
The file is conforming. G₀·G₁ = 3·2⁶² exceeds the domain.

[R-ENC-04] decides it twice over: it binds a quantity "whose **mathematical
value** would exceed 2⁶³ − 1" — the mathematical value of ∏Gᵢ is 0 — and "an
expression this specification writes only inside a comparison, and names
nowhere, is not a designated quantity and no reader is obliged to form it",
which a partial product is. §11.2 designates N, P, the addressed-tile count and
N·P and nothing smaller.

One correction: the reporter says [R-SEC-02] "pushes the other way". It does
not. Its text is "Every declaration-derived sum and product `[R-ENC-04]`
**designates** is overflow-checked before use" — scoped to designated
quantities, so it is aligned with the narrow reading, not against it. That
removes the only normative counter-pressure the finding cites and leaves the
case cleanly decided.

What survives is small and real: §11.2's Note warns against the additive
overflow idiom ("(Eᵢ + Tᵢ − 1)/Tᵢ, whose intermediate sum can exceed 2⁶³ − 1")
and says nothing about the multiplicative evaluation-order hazard, which is the
same shape and reachable by a checked-arithmetic reader, while the only place
the zero-factor case is discussed is §11.1's Rationale, non-normative under
[R-CNF-01]. CONFIRMED, editorial, repair optional and Note-level.

Byte-level: no — quoted above.

### 15. adversary-03 — compaction's regeneration trigger

Text (3403): "except that relocation re-points extent slots, regenerates each
**relocated** tile-index region (entry offsets new; ...)". The same sentence
grants the compactor freedom "to place structures anywhere §5.2 admits", so a
region can land back at its original offset while every tile it addresses has
moved. The trigger clause then does not reach it, and the literal reading
leaves stale entry offsets.

That reading is barred by the surrounding text, which I checked: [R-WRT-07]'s
own closing "The output's reference arrays MUST equal the live generation's bit
for bit (`[R-MDL-02]`)"; §20.5's "Given a conforming input the output is a
conforming file"; and the resulting output would fire F33 or T9. §20.5's
Example states the purposive trigger outright — the index region is "the one
kind this operation regenerates rather than copies, since its entries carry the
offsets that moved."

So the defect is that the trigger names the wrong condition, not that the bytes
are open. Byte-level: no — [R-CNF-05] bars the literal reading's output under
both accounts. CONFIRMED, editorial.

### 16. adversary-04 — L23's Detected cell

L23's Detected cell reads "layer access"; its first instance is "leading fixed
fields (name … C)". §19.1 step 4 places the name-field-fits determination at the
open: "a layer record whose name field does not lie entirely within that
record's inline_length yields no name field to compare, so it contributes no
name to the namespace and is instead a validity error at layer scope
(`[R-CNT-18]`)", and §19.2's first bullet confirms the tier: "at open: ... the
layer-name namespace (§19.1's steps)". Divergence confirmed, and it is
[R-CNT-18] on both sides, so it is L23's row.

Corroboration the reporter did not use: L3, L5 and L6 — the other layer-record
*name* rows — already carry Detected "open", while every other layer-record row
carries "layer access". L23's name instance is the outlier.

Byte-level: no. §21.1's "where a row and the rule it cites diverge, the rule
governs" settles which text controls, the same layer is rejected under either
tier, and F4 cannot fork because its own condition is guarded — "both
obtainable within their records' inline_length". CONFIRMED,
register-bookkeeping.

### 17. adversary-05 — §2.1's Note on SHOULD

`grep -c SHOULD` gives 44 lines, matching the census claim. Counterexamples
checked in place:
- [R-MTA-09], line 2648: "the verifier SHOULD report the bound it applied and
  the stored length of the extent it declined." No consequence there or
  nearby; the MUST-level reporting duty beside it is [R-CNF-11]'s, not this
  SHOULD's.
- [R-SLB-01] (2258) "which writers SHOULD zero and no conformance requirement
  constrains" and [R-SLB-03] (2286) "which writers SHOULD zero" — restatements
  of [R-CNT-03], whose own consequence clause ("leaves bytes indistinguishable
  from stale data and forfeits byte reproducibility") is not carried with them.
- [R-PRV-03] (4138): two SHOULDs with no local consequence, though §23.2's
  preceding paragraphs arguably supply it.
Many SHOULDs do state consequences ([R-CNT-26], [R-LIF-07], [R-ENC-14],
[R-TYP-10], [R-CNT-09], [R-CNT-10], [R-COD-06], [R-SEC-03], [R-PRV-05], §20.3's
new-file advice), which is why the discipline is visible and the exceptions
stand out.

Byte-level: no. The passage is labelled *Note*, non-normative under
[R-CNF-01], and [R-CNF-12] places SHOULD deviation outside the register.
CONFIRMED, editorial, and the weakest CONFIRMED in this set.

### 18. quiz-01 — §20.4's table carries no identifier

Verified the identifier placement: [R-WRT-05] closes at line 3288, before the
paragraph introducing the table; the next identifier is [R-WRT-08] at 3322,
closing a paragraph whose sentence is about re-encoding and relocation, not
retention or dropping. So the table's three obligations — retain
byte-identical; retain with extent content unmodified; the conditional drop —
carry no identifier, against §2.2's "Normative requirements carry identifiers
of the form `[R-<PREFIX>-<NN>]`".

Second half checked: §21.6's row cites "`[R-CNT-15]`, `[R-WRT-08]`" for
"Ignored, and preserved or dropped per its PE bit". [R-WRT-08]'s text says
nothing about preservation or dropping per PE; that disposition is the table's.
So the citation reaches a rule that does not state what it is cited for.

The obligations themselves are normative regardless ([R-CNF-01]: no Note,
Example or Rationale label) and are reached by section reference from
[R-CNF-06] ("MUST honor the preservation obligations of §20.4") and §2.4's
preserve-verbatim row ("§20.4's table states the cases"). Byte-level: no — both
readings oblige the same retention and permit the same drops. CONFIRMED,
editorial; minting an identifier is a maintainer's act since §2.2 makes
identifiers permanent.

## Byte-level tally

Zero groups byte-level. The two closest calls were register-02 (decided by
[R-MTA-10]'s express closed list naming "the extent's terminal CRC
(`[R-CNT-20]`)") and verifier-02 (verdict *nonconforming* under both readings,
since F20 or F29 is established either way). Every downgrade above rests on a
quoted sentence, named in the group's byte_level_rationale.
