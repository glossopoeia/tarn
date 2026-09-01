# Round 28 triage — implementer-consequence lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, all 4648 lines,
  in twelve sequential reads (1–120, 120–680, 680–1080, 1080–1500, 1500–1920,
  1920–2340, 2340–2760, 2760–3180, 3180–3600, 3600–3900, 3900–4200, 4200–4648).
- Two `grep` runs against the same file: a count of lines containing `SHOULD`
  (44, matching adversary-05's census figure) and three line locations
  (`witnessed by T2, T4 or T5` at 3831; `SHOULD report the bound it applied`
  at 2648; `SHOULD compact before publication` at 4139).
- Nothing else. No walk transcripts opened. No directory listing run — not
  `round28/`, not my own output directory (I created it with `mkdir -p` without
  listing). No `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
  `spec/registry.json`, git history, or web.

Every quotation below I re-read in place rather than taking from a reporter.

## Grouping

18 groups over 22 ids. Three merges:

- **verifier-03 + diagrams-02 + adversary-06** — all three attack the same
  sentence, Appendix G item 5's closing clause "elsewhere it changes the stored
  bytes of every tile it touches", and all three build a fixed-point tile.
  One defect, three witnesses.
- **diagrams-03 + quiz-02** — both attack §21.6's zero-layers row, and both
  give the same counterexample (a layerless file carrying a file-scope
  user-metadata record). Identical.
- **diagrams-05 + adversary-02** — both attack §21.7's second-paragraph
  inventory of unwitnessed obligations for omitting §20.4's preservation
  duties. adversary-02 adds one further omitted item ([R-CNT-08]'s updater
  copy-forward) and notes the asymmetry against §20.5's compactor duty, which
  §21.7 *does* name. Same defect, adversary-02's version wider.

Everything else stands alone. No id dropped.

## Group-by-group

### 1. opening-blockquote-nonnormative-claim (reader-01)

[R-CNF-01], line ~102: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative."

The block at line 12 is none of the three: it precedes "### 1. Introduction",
carries no Note/Example/Rationale label, and is not an appendix. Its own
parenthetical "*(non-normative)*" invokes a mechanism [R-CNF-01] extends only
to appendices. Real inconsistency. CONFIRMED.

Byte level: no. Under either reading the block's content — "Sections follow a
fixed rubric where applicable: purpose, byte-layout table, writer rules, reader
rules, error handling, worked examples" — constrains no field, no offset, no
enum, no outcome. Its two substantive claims are already stated normatively
elsewhere: the structural/descriptive split by [R-ENC-16] ("In format major 1
`version_minor` is the only descriptive field") and the vector-citation rule by
[R-VEC-02] ("the §21 register row it exercises together with that row's
governing requirement identifier"). Nothing an implementation emits or accepts
turns on it.

Repair: one word. Either add the block to [R-CNF-01]'s exception list, or
relabel it as a *Note*.

### 2. profile-leaves-layout-tiling-order-unpinned (writer-01)

Appendix G preamble: the profile "closes the degrees of freedom this format
deliberately leaves open."

Item 5 pins the filter on three grounds, each of which holds word for word of
three things no item pins:

- channel layout — §7.4's `layout` field; §14.4's Note gives the two layouts
  different tile images for any bool channel;
- tile extents — §11.3's Note: "Tile extents are a writer's choice, and this
  specification imposes none";
- declaration order — §3.1: "the declared order is load-bearing".

Item 2's own sentence concedes the point: "two files carrying the same arrays
can legitimately differ in tiling, layout, and codec." Item 1 pins the codec;
nothing pins the tiling or the layout. The closing paragraph's enumeration of
what the items add names alignment/slab, gap content, gap extent, record order,
fill default, all-fill sentinel, one generation, version_minor, file_id, NFC
names, producer pinning — not layout, not tiling, not declaration order.

The reporter's reading (A), where "the same input" includes the whole layer
schema, would make item 1's codec pinning and item 5's filter pinning both
redundant, since codec and filter are layer-record fields supplied by the same
caller as layout and tiling. So (B) is right and the profile is incomplete.
CONFIRMED.

Byte level: no. Appendix G is identified non-normative at its heading and says
so of itself: "It adds no requirement to any actor: a writer ignoring it is
fully conforming." [R-CNF-05] expressly licenses exactly the divergence at
issue: "this specification does not promise canonical bytes, and two conforming
writers given identical input MAY produce different conforming files." Every
file either writer emits is conforming under both readings.

Implementer consequence, concretely: vendor A and vendor B both certify
profile-conformant writers; given the same arrays A emits an interleaved layer
at 256×256 tiles and B a planar layer at 512×512; both files are conforming,
both writers satisfy all ten numbered items, and the content-addressed store
sees two hashes. Appendix G's own refutation model ("refuted cheaply but
confirmed only by reproducing the file") diagnoses nothing, since no numbered
item is violated.

Repair needs a maintainer decision, not an edit: either scope "the same input"
in the preamble to include the layer schema (layout, tiling, declaration order,
names, fill, codec, filter), which makes items 1 and 5 redundant restatements
of the caller's contract, or add an item pinning layout, tile extents and
declaration order. I'd take the first: say in the preamble that the profile
takes the layer schema as given and closes only what the writer chooses within
it.

### 3. appender-tier-list-omits-shrink-unstore-drop (writer-02)

§20.1: "**appender** — extends an existing file by commits (§9.2): adding
layers or records, superseding tiles, growing extents, amending metadata."

Three operations §20.3/§20.4 spend paragraphs permitting are absent, and the
list takes one half of each of two pairs the governing sections treat
symmetrically:

- shrink — §20.3 step 4: "An extent MAY also **shrink**, and the bar above is
  the whole of the test"; "Where a shrink is permitted the de-addressed tiles'
  extents become slack ([R-CNT-21]), [R-CNT-17] obliges the smaller entry_count
  and so a re-emitted index region";
- unstore — §20.3 step 4: "entries for tiles that become unstored written as
  the sentinel";
- drop an MU = 0 / PE = 0 record — §20.4's table: "Retain byte-identical, or
  drop it — its extent becoming slack."

CONFIRMED as under-inclusive.

Byte level: no. The tier vocabulary gates nothing: [R-WRT-01] places the same
obligations on an appender and a compactor ("satisfy every writer requirement
for the bytes they produce and the preservation obligations of §20.4"), and no
requirement anywhere is conditioned on an actor *being* an appender. §20.3's
permissions are the operative text and admit one reading. The decisive sentence
is §20.1's own defining clause — "extends an existing file by commits (§9.2)" —
which makes the colon list a gloss on what a commit does, and §20.3 says what a
commit does.

Implementer consequence: a team that reads the list as constitutive ships an
appender that routes shrink/unstore/drop callers to a whole-file rewrite,
paying a full copy for operations §20.3 permits in place — and §20.3 itself
says the rewrite is the wrong shape except "wherever a commit would strand a
large share of a layer's stored bytes". Cost is I/O, not bytes.

Repair: add "shrinking extents, unstoring tiles, and dropping a droppable
record" to the list, or make it expressly open ("among them").

### 4. ordinal-renumber-gloss-misses-planar-channel-set (writer-03)

§20.3 step 4: "and every other entry byte-identical at its disk-ordinal
position (a geometry change renumbers ordinals wherever `[R-GEO-06]` moves
them)".

[R-GEO-06] makes the planar disk ordinal "**c · N + s** ... where c is the
channel's index (§3.1)", and §3.1 makes c positional. So reordering a planar
layer's channel declarations — no dimension, extent or tile extent touched, C
unchanged — moves every ordinal. I checked that such a commit is reachable on a
layer that already stores tiles: §20.3's bar prohibits only a declaration
change that alters, for a prior-generation stored tile, the padding-position
set and its [R-SER-05] content, the decoded size, the byte offset of any sample
within the decoded tile image, or the codec and filter. For a planar layer each
tile still carries one channel, its decoded size is still P·Bᶜ for *its own*
channel, its padding content is still its own channel's fill, and the layer's
codec and filter are unchanged — so the bar permits the reorder, and
[R-GEO-06] then obliges the entries to move. (For interleaved the same change
moves Fᶜ = Σ Bⱼ for j < c, so the bar catches it. The gap is planar-only.)

CONFIRMED as an under-inclusive gloss. The rule itself is right.

Byte level: no, and here is the premise I am resting on, stated for attack: a
file whose planar index leaves channel x's stored tile at the ordinal that now
belongs to channel y is a **conforming** file that denotes a different
reference array, not a nonconforming one. The text that decides it is §21.7:
"the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
structurally valid tile whatever values it carries, except where §14 constrains
a byte's content". So where the reordered channels' fills coincide (or the
layer has no padding position), nothing fires and both files — the correct one
and the mis-placed one — are conforming and emittable. What separates them is
the caller's intended array, which [R-MDL-01] derives *from* the file and does
not adjudicate against an external intent. Where the fills differ and padding
exists, T4 fires and [R-CNF-05] bars the mis-placed file under both readings.
Either way the emittable set does not move.

Independently, the *rule* is already unambiguous without the parenthetical:
[R-IDX-01] fixes it — "The entry for the tile with disk ordinal k (§11.4) is
the k-th entry, at region byte 20·k" — read with [R-GEO-06]'s formula over the
new declarations.

Implementer consequence, concretely: a writer that takes the parenthetical as
its trigger set leaves the entry array untouched across a planar channel
reorder. Every channel's data is then attributed to the wrong channel,
silently, in a file that verifies. That is the most expensive consequence in
this batch even though it is not a byte-level ambiguity, because the file
passes every check.

Repair: name the trigger set — "a change to the grid counts or, in a planar
layer, to the channel set or its declared order renumbers ordinals wherever
[R-GEO-06] moves them". §11.1's Rationale repeats the same geometry-only
pairing and wants the same widening.

### 5. slack-disposal-missing-no-other-claimant-qualifier (verifier-01)

§15.3 [R-IDX-03]: "so any bytes it nominally addressed **that no other claimant
claims** fall to slack."

§9.7 [R-LIF-08], the restatement: "the walk passes over it, and the bytes it
nominally addresses fall to slack (§15.3)." Qualifier dropped.

Cases where it bites: T8 (offset < 16) nominally reaches the front block, which
§9.7 itself says is claimed — "The front signature block at [0, 16) and the
live trailer at [F − 64, F) are claimed by the walk as well, being members of
the live committed state"; T9 nominally reaches the live trailer, likewise
claimed; T6/T7 carry offset 2⁶⁴ − 1 and nominally address bytes outside the
file, which is vacuous rather than contradictory. Read literally §9.7 puts
[8, 16) into two classes at once, which [R-CNT-02]'s "belongs to exactly one
of" forbids. CONFIRMED.

§9.7 also contains the correct general formulation two sentences earlier —
"Bytes the walk does not reach are slack: the verifier sums them and reports
the total" — so the section resolves itself internally, and §15.3 is the
defining rule.

Byte level: no. Every file that can exhibit the divergence carries a T6–T12
row and is nonconforming under both readings, so no accept/reject verdict
moves. What differs is one figure on a report line, and only for a verifier
that implements the disposal additively; slack computed as F minus the union of
enumerated claimants gives the same number under both readings.

Repair: add "that no other claimant claims" to §9.7's sentence.

### 6. slack-total-duty-gap-after-directory-failure (verifier-02)

[R-CNT-21]'s duty: "a verifier that reaches a live state MUST report the total
number of slack bytes". Its exemption: "Where §6.2's ordered validation rejects
the file **before a live trailer is established** there is no F and no live
state to walk, so the total is not owed at all".

The two conditions are not complements, and F20 (directory-region CRC mismatch,
governed by [R-CNT-11], not §6.2) and F29 (record-sequence framing failure)
fall between them. A live trailer *is* established there — §6.2's ordered
validation passed in full — so the exemption's own words do not reach the case,
and its stated ground does not transfer ("there is no F": here there is an F,
gated and CRC-covered). Whether the general duty reaches it turns on whether
"reaches a live state" is met when nothing is reachable *through* the
directory, which §5.2's definition makes the operative question: the live
committed state is "the front signature block, and every structure reachable
from the live trailer through the live directory's records, extent slots, and
tile-index entries, together with the live directory and the live trailer."
The document does not say. Real gap. CONFIRMED.

Byte level: no. F20 or F29 is established either way, and [R-CNF-11] fixes the
verdict against both readings: "An established violation takes priority: a
verifier that has established any violation reports *nonconforming*, however
many requirements it was unable to check." And §5.2's Note expressly separates
the total from any fact about the file: "A partial total (`[R-CNT-21]`) reports
what one verifier's incomplete walk left unclaimed, which is a fact about that
run and not about the file's live state." So a partial total is, by the
document's own words, a property of the verifier run, not a verdict or a
predicate on bytes.

Implementer consequence: two conforming verifiers hand an operator different
reports for the same corrupt file — one a line reading "partial slack total
N bytes; walk stopped at the directory CRC", the other no slack line at all.
For a file already reported nonconforming that difference is small; §22.3's
claim that the slack total "is the number that distinguishes a working file
from a padded one" is about files that certify.

Repair needs a maintainer decision: either widen the exemption's condition from
"before a live trailer is established" to "before a live state can be walked",
which disposes of F20/F29 with no total, or add the case to the partial-total
clause alongside the scope-level-rejection and stop-at-first-violation
triggers. I'd take the second — [R-CNT-21] already carries machinery built for
rejections that end an enumeration, and a partial total naming the directory
CRC is more useful to an operator than silence.

### 7. shuffle-fixed-point-tile-falsifies-item-5 (verifier-03, diagrams-02, adversary-06)

Appendix G item 5: "The filter is the identity exactly where its permutation is
— where the stride is 1 ... and equally where the decoded image is a single
group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the stored bytes of
every tile it touches."

First half verified against [R-COD-10]: "the filtered image places byte i of
group j at offset i · n + j", against an original offset of j · s + i. Identity
for all i, j iff s = 1 or n = 1 (take i = 0, j = 1 to force s = 1; i = 1, j = 0
to force n = 1). Correct.

Closing clause false. A non-identity permutation still fixes any image
invariant under it, and such tiles are legal and unremarkable. Three
independent witnesses, all of which I checked:

- verifier-03: any all-equal-bytes image, e.g. a uint16 channel every byte
  0xAB on a layer whose fill is 0x0000 — stored (item 6 removes only all-*fill*
  tiles) and fixed at s = 2.
- diagrams-02: interleaved, two uint8 channels, P = 2, so Q = s = 2, L = 4,
  n = 2; the permutation sends b0 b1 b2 b3 → b0 b2 b1 b3, identity on every
  image with b1 = b2, e.g. `07 07 07 09`. I recomputed this from [R-COD-10]
  directly and it is right.
- adversary-06: constant image, C = 2 uint8, P = 8, L = 16, s = 2, n = 8, all
  bytes 0x00 with nonzero fills so item 6 does not apply.

Nothing in §12.3, §14.2, §14.4 or §14.5 excludes such a tile. CONFIRMED.

adversary-06's stronger lemma is correct and I verified it: filtered[0] =
image[0] and filtered[L−1] = image[L−1] at every legal stride, since
L − 1 = (n−1)s + (s−1) maps to (s−1)n + (n−1) = sn − 1 = L − 1. It matters
again in group 12.

Byte level: no. Appendix G is non-normative by its heading and by [R-CNF-01],
and states of itself: "It adds no requirement to any actor: a writer ignoring
it is fully conforming." The item's operative instruction — pin the filter
value — is untouched, and is carried independently by the fact that the filter
is a `u16` field of the layer record (§7.4), so two writers disagreeing about
it emit different layer records whatever any payload does.

Repair: replace the universal with what the item needs — "elsewhere it permutes
the image, changing the stored bytes of every tile the permutation does not
fix".

### 8. compaction-figure-pad-not-hatched (diagrams-01)

§20.5's Example, line 3438: legend "Regions, not offsets; ▓ marks slack." Both
rows draw `pad` as its own unhatched cell, and the output row carries no ▓ at
all.

The pre-trailer pad is slack twice over in the document's own words —
§5.2: "Every byte the live state does not claim is **slack**: alignment and
slab gaps, the pre-trailer pad, and everything an earlier commit superseded";
§6.2: "Those bytes — the **pre-trailer pad** — are slack (§5.2)". So the figure
mis-classifies a region under its own unqualified legend, and the output row
invites the stronger false reading that a compacted file carries no slack.
That reading is false in general: §20.5 obliges the creation path, whose step 5
"append[s] the pad to the next 64-byte boundary", so unless the directory ends
64-aligned the output carries 1–63 pad bytes; and [R-WRT-07] has the compactor
honour "every declared layout invariant ... ([R-SLB-01], [R-SLB-03])", whose
gaps §16.1 and §16.2 both call slack.

The three parallel figures each avoid this and §20.5's does not: §5.1's is
corrected in prose ("the pad and the ▓ runs are slack"); §9.2's scopes its
legend ("▓ marks bytes outside the live committed state: in row 2 ... in row
3 ..."); §20.3's scopes its legend ("▓ marks what the commit turned to slack",
under which a fresh pad correctly carries no hatch). CONFIRMED.

Byte level: no. The figure sits inside a labelled *Example*, non-normative
under [R-CNF-01], and the normative text fixes the output's pad and gaps
([R-LIF-02] step 5, [R-SLB-01], [R-SLB-03], [R-WRT-07]). A compactor that took
the figure literally and emitted no pad would produce a file whose F is not a
multiple of 64 — nonconforming under [R-CNT-06] — rather than a different
conforming one, so the emittable set does not move.

Implementer consequence: a tool built from this figure expects a freshly
compacted file to report a slack total of zero and flags a conforming file as
suspect when it does not.

Repair: hatch the pads, or scope the legend as §20.3 does, or add §5.1's
corrective sentence.

### 9. zero-layers-row-glossed-as-empty-directory (diagrams-03, quiz-02)

§21.6: "| The file contains zero layers | A conforming file with an empty
directory | `[R-CNT-14]` (R-CNT-02) |"

The Defined-behavior cell adds a fact the Condition does not carry.
[R-CNT-14] permits, independently of the layer count, "any number of layer
records (zero is valid: an empty directory is a conforming generation); at most
one file-scope user-metadata record", and [R-CNT-15] permits unknown ancillary
records at file scope. Smallest counterexample, which I checked against §7.2's
framing: a directory holding exactly one type-0x0002 record with a valid extent
— zero layers, 24 header bytes plus a 1-byte inline payload plus the terminal
4-byte CRC — conforming throughout. CONFIRMED, and both reporters give the same
counterexample.

[R-CNT-14]'s own parenthetical makes the same slide but is not itself false: it
states a sufficient case, not a necessary one. The row lifts it into the answer
column, where it reads as the whole answer.

Byte level: no. §21.1 decides it expressly for §21.6's entries: "§21.6's
entries restate their governing rules on the same terms a row does, and where
such an entry and the rule it cites diverge, **the rule governs** there too."
[R-CNT-14]'s two clauses compose unambiguously and no reader reading both has
a ground to refuse the file. The cost is to someone building a
defined-behaviour inventory from §21.6 alone.

Repair: reword the cell — "A conforming file; its directory may be empty, or
may carry a file-scope user-metadata record or an ignorable ancillary record."
Consider loosening [R-CNT-14]'s parenthetical at the same time so the two do
not reinforce each other.

### 10. serve-unchanged-row-citation-names-only-two (diagrams-04)

§21.1: "the governing rule states what a reader does, and for several such rows
it obliges the reader to serve the structure unchanged (`[R-CNT-22]`, whose
registered type keeps its fixed semantics; and `[R-MTA-05]`, whose unsorted
document readers process as they find it — F27 and L48)."

I grouped the register rows by governing rule and confirmed: [R-MTA-05]'s rows
are F27 and L48; [R-CNT-22]'s are F28 and L49. Four rows carry the
serve-unchanged property, and [R-CNT-22]'s text confirms it — "conforming
readers nevertheless process the record under the fixed semantics". The
appositive names two.

Under reading A (the dash binds to the second conjunct only) the sentence is
true but leaves [R-CNT-22]'s rows unnamed. Under reading B (the appositive
names the whole set) it is false. "Several" reading oddly over two rows is
what invites B. CONFIRMED either way — one reading is short, the other wrong.

Byte level: no. Under either reading the register's own cells are unchanged,
and each rule states the reader's behaviour in its own text: [R-CNT-22]
"conforming readers nevertheless process the record under the fixed semantics";
[R-MTA-05] "readers process the document unchanged". No accept/reject verdict
moves; the cost is to a reader of §21.1's front matter building a table of
which rows carry the property.

Repair: name all four — "(`[R-CNT-22]` — F28 and L49 — whose registered type
keeps its fixed semantics; and `[R-MTA-05]` — F27 and L48 — whose unsorted
document readers process as they find it)".

### 11. unwitnessed-inventory-omits-updater-preservation (diagrams-05, adversary-02)

§21.7 second paragraph opens "A second set of obligations is omitted from the
register because a single file exhibits no witness of their violation" and
itemises by identifier: [R-LIF-01], [R-LIF-02]; [R-GEO-06] and [R-SER-01];
[R-CNT-13]'s embedded-offset bar; [R-CNT-18]'s nesting bar; §20.3 step 4's
declaration bar; §20.5's three trailer obligations ([R-WRT-06]); [R-ENC-06].

Absent, all MUST-level, none a conduct rule under [R-CNF-02] (whose stated
conduct cases are §10.3, §18.3, §6.3's flags = 0, §6.2's over-long pad), and
none witnessed by a single file:

- [R-WRT-05] — "an updater MUST re-emit byte-identically — header, inline
  payload, and extent slot — every record it retains and does not logically
  modify";
- [R-WRT-08] — "An updater MUST NOT re-encode a record whose type it does not
  implement";
- §20.4's table drop restriction — "An appender MUST NOT drop it except in a
  commit that *independently* changes the scope the record attaches to";
- [R-CNT-08]'s updater half — "An updater MUST copy forward unknown ignore-lane
  bits of the file it modifies and MUST NOT clear them" (adversary-02's
  addition, and the sharpest one: §21.7 names the *compactor's* identical duty
  under [R-WRT-06] and steps over the appender's, and the reason is the same
  for both — the input's flags survive only in the superseded trailer, which is
  slack, whose content [R-CNT-21] leaves unconstrained and which §9.7's walk
  does not enumerate).

§20.4's own Rationale supplies the account in almost §21.7's words — "nothing
in either says how many commits separate them. Adjacency is a fact about a
file's history, which §9.7 does not reconstruct" — but that Rationale is
non-normative under [R-CNF-01], and §21.7 is where the account belongs.
CONFIRMED.

The hedge both reporters raise and I checked: §21.1's normative completeness
clause does not reach here — "The subsections after §21.5 are not part of the
register and carry no rows: neither this completeness clause nor the instance
arithmetic below reaches §21.6's defined non-violations, §21.7's account of
what no check detects, or §21.9's limits." So §21.7 being short is not a
breach of a stated requirement. Both reporters said so themselves. What
remains is that §21.7 reads as an inventory (every other member is named by
identifier) and is missing four members.

Byte level: no, and decisively — these obligations have no file-level witness
under any reading, so no two implementations could disagree about bytes or
about accept/reject on account of the omission. §21.7's own first paragraph
says of the analogous class: "no file-level witness exists to check, so nothing
about the file is left undetermined and the verdict is unaffected."

Implementer consequence: a team reads §21.7 as the inventory it presents itself
as, concludes §20.4's preservation duties must be witnessed somewhere, and
either hunts for a register row that does not exist or builds a verifier that
tries to enforce byte-identical re-emission from a single file — undecidable
from one file.

Repair: add the four to §21.7's second paragraph, or add the "not offered as
closed" clause the document already uses at §20.3 step 4 and §23.1. Either is
cheap; adding the items is better, since the paragraph's value is its
specificity.

### 12. t5-as-mis-strided-filter-witness (register-01)

This is the one I graded against the reporter.

The two sentences are real. §21.7 line 3831: "a mis-ordered image is then
witnessed by T2, T4 or T5, exactly as a mis-strided filter is". §21.7 twenty
lines later: "where the resulting image breaks §14.5's padding content or
`[R-SER-08]`'s bool bytes, the check that detects it is T2's or T4's, exactly
as T26 has it". T26's cell agrees with the second: "the check that detects it
is T2's or T4's".

The reporter concludes T5 is a genuine witness of a mis-strided filter and the
second sentence and T26 are short. **That is wrong, and the byte-shuffle's own
arithmetic refutes it.**

T5's condition is a packed planar bool plane's final-byte pad bits. §17.3
mandates s = 1 for a packed boolean plane, so the mandated filter is the
identity and the reader's inverse is the identity; the image a reader
reconstructs from a wrongly-strided writer's bytes is the forward shuffle at
the wrong stride. But **the shuffle fixes the final byte at every stride**:
the byte at original offset L − 1 is byte i = s − 1 of group j = n − 1, since
(n−1)s + (s−1) = sn − 1 = L − 1, and its filtered offset is
i·n + j = (s−1)n + (n−1) = sn − 1 = L − 1. (It fixes offset 0 the same way.)
The pad bits live in that final byte. So a mis-strided filter can never disturb
a pad bit, T5 can never fire from one, and T26's naming of T2 and T4 is
correct. adversary-06 proved the same lemma in this very batch and
register-01 did not test it.

What *is* wrong there: §21.7's first sentence appends "exactly as a mis-strided
filter is" to a row list — T2, T4 or T5 — that is correct for a *mis-ordered
image* (a writer packing MSB-first, or offsetting the packing, can put a value
into a pad-bit position and fire T5) but not for a mis-strided filter. Read as
"on the same terms" — witnessed only where §14 constrains a byte's content —
the comparison is fine and matches the later sentence's "witnessed on the same
terms T26 states for a wrong stride". Read as "by the same rows" it is false.
So: something is wrong, but not what the reporter said, and the repair is the
opposite of the one proposed. PARTIAL.

Byte level: no. T2, T4, T5 and T26 all carry detector *verifier*, detection
point *certification*, and outcome reject-tile; [R-SER-05] obliges a verifier
to check every pad bit whatever it concludes about T26, and §9.7 makes the
decoded-content obligations a verifier's regardless. The file is nonconforming
and refused at tile scope under every reading. Only attribution moves — and
under my analysis it does not even move, since T26 is right.

Repair: do **not** add T5 to T26 or to the second sentence. Either leave the
first sentence and let "exactly as" carry its "on the same terms" sense, or —
better, since the sentence is checkable and a corpus builder will check it —
narrow it: "...witnessed by T2, T4 or T5; a mis-strided filter is witnessed on
the same terms, though never by T5, the shuffle fixing the final byte of every
image at every stride." A corpus builder taking the reporter's advice would try
to construct a T26 vector exercising the pad-bit path and find it
unconstructible, which is the concrete cost of getting this backwards.

### 13. experimental-encoding-exception-appears-to-withdraw-r2 (register-02)

§21.5's preamble writes its exception over "every way its document can be
unreadable ... except at an experimental-range encoding, where no document rule
attaches", and [R-CNT-25] — the rule cited for that phrase — enumerates those
ways with the extent CRC first: "each way a user-metadata record's document can
be unreadable once its framing has been read — a failed extent CRC, an
unimplemented or invalid encoding, a decode failure, or content violating the
document's own rules ... — is ignore-record". R2's row is unqualified by
encoding. So the sentence, read on its own terms, reaches R2 at an
experimental-range encoding. CONFIRMED as a defect in the sentence.

Byte level: no — the narrow reading is the only permitted one, and three
independent passages say so:

- [R-MTA-10], the rule the sentence itself cites, in an express closed list:
  "file conformance ... is decided by the structural checks that precede the
  document alone: the record's framing and extent slot (`[R-CNT-13]`), the
  encoding byte's own value set (`[R-MTA-03]`), and the extent's terminal CRC
  (`[R-CNT-20]`)";
- §22.3 [R-SEC-04]: "the extent of a user-metadata record under an unassigned
  encoding is covered by its terminal CRC but constrained by no content rule";
- §8.1's map, unconditional on encoding — "User-metadata extent | final 4 bytes
  of the extent | the preceding bytes" — which [R-LIF-08]'s walk obliges a
  verifier to check ("each verifies against the checksum covering it, where
  §8.1's map states one").

R2's own Governing rule cell is [R-CNT-20], not [R-CNT-25], and §21.1 makes the
governing rule control over any restatement. And a second-order check: even
under the broad reading the *file* is still nonconforming, because [R-MTA-10]
says conformance is decided by the terminal CRC — only whether a particular
verifier looks would move, and a verifier that skips a check §9.7 obliges is
not conforming. So the emittable set and the file's conformance status do not
fork under any reading.

Implementer consequence if the sentence is left: a team building a verifier
from §21 — where a verifier goes to learn what the ignore-record rows are and
when they apply — certifies a file whose user-metadata extent is corrupt
because the record's encoding happens to be ≥ 0x80, and only a cross-read three
sections away catches it. Worth repairing even though it is not byte-level.

Repair, and it is one clause: the preamble already carries the right sentence
for half the problem — "what `[R-MTA-10]` withdraws is the document's content
rules, never the encoding byte's own value set (`[R-MTA-03]`)". Extend it:
"...never the encoding byte's own value set (`[R-MTA-03]`) nor the extent's
terminal CRC (`[R-CNT-20]`, R2)."

### 14. partial-grid-product-overflow-undesignated (adversary-01)

Construction checked field by field: interleaved, C = 1 uint8 channel, rank 3,
dims (E = 2⁶², T = 1), (E = 3, T = 1), (E = 0, T = 1); G = (2⁶², 3, 0);
N = ∏Gᵢ = 0; P = ∏Tᵢ = 1; N·P = 0; C·N = 0; P·Q = 1; entry_count = 0, so
[R-CNT-17]'s extent_length formula gives 0, extent slot (0, 0),
crc_of_crc_array = 0 per [R-CNT-23]. Every declared field is within
[R-ENC-03]'s domain (2⁶² ≤ 2⁶³ − 1). Conforming. But G₀·G₁ = 3·2⁶² exceeds
2⁶³ − 1.

The document decides it, in [R-ENC-04] and in two clauses:

- "any quantity this specification **designates** ... whose **mathematical
  value** would exceed 2⁶³ − 1" — the designated quantity is N = ∏Gᵢ, whose
  mathematical value is 0;
- "A designation is express, made by the section that defines the quantity; an
  expression this specification writes only inside a comparison, and names
  nowhere, is not a designated quantity and no reader is obliged to form it" —
  a partial product is named nowhere. §11.2 designates Gᵢ, N, P, the
  addressed-tile count and N·P, and nothing smaller. L2's instance list is the
  same set.

I checked the reporter's claim that [R-SEC-02] pushes the other way, and it
does not: "Every declaration-derived sum and product `[R-ENC-04]` **designates**
is overflow-checked before use." That tracks the narrow reading exactly. And
[R-GEO-02] closes it from the other side: "A dimension with extent 0 is valid:
its grid count is 0, the layer has zero addressed tiles ... **Readers MUST
accept such a layer**." CONFIRMED as the reporter graded it — decidable, and
expensive to decide.

Byte level: no. One permitted reading; an implementation that rejects is not
exercising a second reading but breaching [R-CNF-03]'s duty to accept every
conforming file.

Implementer consequence, concretely: a checked-arithmetic implementation that
folds ∏Gᵢ left to right traps at 3·2⁶² and reject-layers a conforming file,
while a wrapping implementation gets the right answer (anything × 0 = 0) — so
the more careful implementation is the one that fails, which is the reason to
repair. §20.3 step 4 lets a schema-first workflow reach this state one legal
commit at a time, and §11.1 says zero-extent layers are the workflow that
section exists to serve.

Repair: a Note in §11.2, parallel to the one already there for the additive
ceiling-division idiom: N is the mathematical product, a zero grid count holds
it at 0 however large the others, and no partial product is a designated
quantity a reader is obliged to form.

### 15. compaction-regeneration-trigger-names-region-not-entries (adversary-03)

[R-WRT-07]: "...except that relocation re-points extent slots, regenerates each
**relocated** tile-index region (entry offsets new; entry lengths, entry crcs,
and sentinel entries unchanged; segment CRCs recomputed over the entries as
re-emitted), and updates the layer-record fields covering a regenerated region
(crc_of_crc_array)."

The construction is legal: the same sentence grants the compactor freedom to
"place structures anywhere §5.2 admits", so it may pack every tile and put the
index region back at its original offset. The region is not relocated; every
one of its entries' targets is. Read literally, the exception does not reach
the region and the compactor re-emits entries pointing where the tiles used to
be. CONFIRMED — the trigger clause names the wrong condition.

The surrounding text names the right one twice: the paragraph below —
"Regenerating a region means ... every other entry is re-pointed to where its
stored extent **now lies**" — and §20.5's own Example — "the one kind this
operation regenerates rather than copies, since its **entries carry the offsets
that moved**".

Byte level: no. The literal reading's output is itself nonconforming — stale
entry offsets break [R-WRT-07]'s own closing MUST ("The output's reference
arrays MUST equal the live generation's bit for bit") and §20.5's "Given a
conforming input the output is a conforming file", and in practice fire F33/L18
overlap or T1 — so [R-CNF-05] bars every conforming writer from emitting it
under both readings. The emittable set does not move.

Repair: change the trigger — "regenerates each tile-index region any of whose
entries' stored extents moved". The companion clause "updates the layer-record
fields covering a regenerated region (crc_of_crc_array)" then inherits the
right trigger automatically.

### 16. l23-detection-tier-for-the-name-field (adversary-04)

L23's condition is "A declared region of the layer record's inline payload does
not lie entirely within inline_length", first instance "leading fixed fields
(name … C)", Detected cell "layer access".

§19.1 step 4 places that determination at the open: "a layer record whose name
field does not lie entirely within that record's inline_length yields no name
field to compare, so it contributes no name to the namespace and is instead a
validity error at layer scope (`[R-CNT-18]`)". §19.2 confirms the tier: "at
open: ... the layer-name namespace (§19.1's steps)". The register already
places the other name checks at open — L3, L5 and L6 all read "open". So L23's
cell diverges for its name instance. CONFIRMED, and §21.1 already resolves it:
"where a row and the rule it cites diverge, the rule governs."

Byte level: no. Under either tier the same layer is reject-layer and the same
other layers are served; F4's namespace is built from the same set of names,
since F4's own condition requires both names "obtainable within their records'
inline_length" and excludes the defective record either way. And §19.2 fixes
only the *latest* detection point — "A reader MAY detect any violation earlier
(`[R-CNF-12]`)" — so open-tier detection is licensed under both readings. No
returned byte and no verdict differs.

Implementer consequence: coherence only. A reader that defers to layer access
cannot build the namespace §19.1 specifies, because it needs the answer to
build it — so the row's cell describes a tier no reader can actually take.

Repair: split the cell the way the Instances column cannot — "open for the name
field; layer access otherwise" — matching L3/L5/L6.

### 17. should-consequence-universal-falsified (adversary-05)

§2.1's Note: "every SHOULD states the consequence of deviation".

I confirmed the census figure independently: 44 lines contain `SHOULD`. I read
the four cited counterexamples in place:

- [R-MTA-09], line 2648: "the verifier SHOULD report the bound it applied and
  the stored length of the extent it declined." No consequence stated, there or
  anywhere. This is the clean one.
- [R-PRV-03], line 4139: "SHOULD treat names and metadata as published content,
  and SHOULD compact before publication when the history itself is sensitive."
  No local consequence.
- [R-SLB-03] and [R-SLB-01]: "which writers SHOULD zero" / "which writers
  SHOULD zero and no conformance requirement constrains". These are weaker
  witnesses — they restate [R-CNT-03], whose own consequence clause is stated
  where the rule lives ("A writer that does not leaves bytes indistinguishable
  from stale data and forfeits byte reproducibility (Appendix G)") — so they
  fall to the reporter's own second reading, which tolerates cross-referenced
  consequences.

The universal is false as literally read; CONFIRMED on [R-MTA-09] and
[R-PRV-03] alone.

Byte level: no. The passage is labelled *Note* and is non-normative under
[R-CNF-01], and it is a claim about this document's drafting rather than about
bytes. [R-CNF-12] independently puts SHOULD deviation outside the register:
"Deviation from a SHOULD is not a violation for this purpose: §21's register
enumerates MUST-level conditions only."

The Note's second universal, which the reporter flags in passing — "every
writer-side prohibition is paired with an explicit reader-side clause stating
what a reader does with a violating file" — is strained against [R-LIF-01],
[R-LIF-02] and §20.4's drop rules, but the defence the reporter names is
available and §21.7 states it: no file witnesses those violations, so "a
violating file" names nothing.

Repair, lowest priority in this batch: qualify the Note ("every SHOULD whose
deviation a file can carry states the consequence"), or give [R-MTA-09]'s and
[R-PRV-03]'s SHOULDs consequence clauses.

### 18. preservation-table-carries-no-identifier (quiz-01)

§2.2: "Normative requirements carry identifiers of the form
`[R-<PREFIX>-<NN>]`."

§20.4's structure, which I read line by line: [R-WRT-05] closes the paragraph
above the table ("...is new output under its writer obligations
(`[R-CNF-05]`). `[R-WRT-05]`"); the paragraph introducing the table ("For a
type the updater does not implement, the stored flags are authoritative ...
and carry these obligations:"), the table itself, and the paragraph below it
("No commit therefore removes a layer record...") carry no identifier; the next
identifier, [R-WRT-08], closes a later paragraph whose own sentence is about
re-encoding and relocation, not retention or dropping.

So the single most consequential updater rule in the document — retain
byte-identical, retain with extent content unmodified, and the conditional
permission to drop an MU = 0 / PE = 0 record — is unidentified normative text.
[R-CNF-01] makes it normative regardless (no Note/Example/Rationale label), and
§2.3's [R-CNF-06] and §2.4's preserve-verbatim row both reach it by section
reference ("§20.4's table states the cases"), which is how it is meant to be
reached.

The second half stands too: §21.6's row cites [R-WRT-08] for "preserved or
dropped per its PE bit", and [R-WRT-08]'s text says nothing about preserving or
dropping — it is the no-re-encode rule. CONFIRMED.

Byte level: no. The obligations are stated in full and are normative under
[R-CNF-01]; both readings oblige exactly the same retention and permit exactly
the same drops, so no updater emits a different directory under one reading
than under the other.

One correction to the reporter's cost estimate: the claim that "a vector
exercising a dropped-record case cannot name [an identifier]" overstates it.
[R-VEC-02]'s requirement runs to "the §21 register row it exercises together
with that row's governing requirement identifier", and §20.4's preservation
duties carry no register row at all — they are precisely the unwitnessed class
of group 11 — so no vector is put in that position. The real cost is to an
audit or a checklist working from identifiers.

Repair, and the maintainer must choose: either mint an identifier for the
table's obligations (§2.2 permits extension — "numbers above 99 extend
naturally ... without renumbering") and point §21.6's row at it, or leave the
table reachable by section reference and fix §21.6's row to cite the section
rather than [R-WRT-08]. Either way §21.6's citation is wrong as it stands.

## Coverage arithmetic

18 groups. Member counts: 1+1+1+1+1+1+3+1+2+1+2+1+1+1+1+1+1+1 = 22.
Input ids: 22. Each id appears once. Counted by hand against the brief's list,
not asserted.

Byte-level count: 0.

## Honest note on the calibration warning

Zero byte-level survivors is the answer the round-16 warning tells me to
distrust, so I have stated the load-bearing premise of each downgrade above
rather than only the conclusion, and I pressed hardest on the three findings
where two implementations could genuinely produce different observable output:
verifier-02 (two verifiers, different report lines — settled by [R-CNF-11]'s
priority rule and §5.2's Note making a partial total "a fact about that run and
not about the file's live state"), register-02 (two verifiers, different
verdicts — settled by [R-MTA-10]'s express closed list naming the terminal CRC,
which also means the *file* is nonconforming under both readings), and
adversary-01 (a checked-arithmetic reader rejecting a conforming file — settled
by [R-ENC-04]'s "mathematical value" plus its non-designation clause, with
[R-SEC-02] tracking the narrow reading rather than opposing it, and [R-GEO-02]'s
"Readers MUST accept such a layer"). If one of these is wrong, it is one of
those three, and the premise to attack is named in each.

The one finding I graded against its reporter is register-01, where the
byte-shuffle's own arithmetic — the same fixed-point lemma adversary-06 proved
elsewhere in this batch — shows the permutation fixes the final byte of every
image at every stride, so a mis-strided filter can never disturb a pad bit and
T26's naming of T2 and T4 is correct.
