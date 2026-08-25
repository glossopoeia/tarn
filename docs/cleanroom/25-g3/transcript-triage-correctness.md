# Round 25 — triage pass, CORRECTNESS lens

## Disclosure of what I read

Read `spec/tarn.md` only, in these ranges: §2 (94–280), §3.1 (282–345),
§4.7 (519–553), §5 (553–700), §6 (700–870), §7.2–§7.4 (899–1115),
§9.5–§9.7 (1260–1325), §11.1–§11.4 (1465–1545), §12.3 (1667–1700),
§14 (1792–1990), §16.1–§16.2 (2126–2215), §17.3 (2360–2400),
§18.2 (2440–2615), §19 (2679–2820), §20.3–§20.5 (2937–3335),
§21.1–§21.9 (3337–3820), §23.1–§23.2 (3924–3995), §24 (4005–4090),
Appendix G (4266–4410).

Ran one mechanical count over §21.2–§21.5 rows (python, counting
semicolon-separated Instances entries, `—` = 1): **121 rows, 277
instances**, matching §21.8's normative figures exactly. Per-prefix:
F 36 rows / 58 instances, L 49 / 116, T 26 / 55, R 10 / 48.

Read NO `transcript-*.md` — neither the six walk transcripts nor any
triage transcript. I did run `ls` on the round25 directory once before
reading the instruction's "do not list that directory" clause closely;
the listing showed only the nine permitted walk/quiz filenames and no
`transcript-triage-*` file existed at that moment. I opened none of them.

Did not read docs/, PLAN.md, AGENTS.md, conformance/, registry.json,
git history, or the web. (Git status in my pre-loaded context named
ADR-0093's subject line — "a compactor is outside the commit protocol,
and the shrink bar has one test". I flag it because it touches
diagrams-05's and quiz-03's subject matter; I derived both judgements
from the spec text alone and record the contamination so it can be
discounted.)

## The premise every one of my byte-level downgrades rests on

State it once, so it can be attacked once.

> **Premise P.** The byte-level test ranges over *byte sequences* —
> which files conform, which a reader must accept or reject — and not
> over *(input, output) pairs* an updater may produce. A fork that
> leaves both candidate outputs conforming files, and leaves every
> reader's and verifier's verdict on those files unchanged, is not
> byte-level however sharply it forks an updater's conduct.

Textual warrant: §2.3 `[R-CNF-02]` — "File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or
environment." And §21.7 `[R-ERR-01]` puts the whole class outside the
register: "A second set of obligations is omitted from the register
because a single file exhibits no witness of their violation …
§20.3 step 4's bar on a declaration change is witnessed only where the
affected tiles remain stored, and then only for part of what it bars."

**The attack on P, stated for the record.** "Which byte sequences a
conforming implementation may emit" can be read to include emission
*from a given input*: under one reading of §20.4 an updater may emit
output X from input I, under the other it may not, so the reading
decides whether a conforming implementation may emit X. If the
maintainer takes that reading, then writer-03, reader-03, writer-01,
adversary-01, diagrams-01 and diagrams-05 all become byte-level at
once — and the gate could never close, since every round produces
several. I take P because the document itself draws the line there
(§2.3's pure-predicate sentence, §21.7's account of what has no
witness), not because the prior says to.

Five findings rest on P: reader-03, writer-01, adversary-01,
writer-03, diagrams-05, diagrams-01. The rest are downgraded on
narrower quotations, given per group below.

## Groups, with the checking

### 1. f5-not-ordered-against-version-gate — reader-01, diagrams-02, register-01

Checked. §6.2 `[R-CNT-06]`: "A reader MUST validate, in order: the
trailer magic; the trailer CRC; the version gate (§6.3) … and then,
those gates passed, MUST validate all of the following … the flag
gates; committed_file_length equals the file size … dir_offset ≥ 16;
dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; 1 ≤ generation ≤
2⁶³ − 1; file_id ≠ 0; reserved bytes zero." The 128-byte floor is not
in that list. `[R-CNT-27]` (§5.1) states no position. §19.1 step 1
obtains F before step 2 fetches the trailer. §19.2 `[R-RDR-02]`: "A
reader MAY detect any violation earlier". So the preamble's warrant —
"§6.2 puts the version gate ahead of every check but the trailer magic
and the trailer CRC" — is true of the checks §6.2 lists and not of
`[R-CNT-27]`. The three reporters are right and their quotations are
accurate and in context. CONFIRMED.

Witness constructibility checked independently: `[R-CNT-24]` fixes
across majors only the magic at F−64, version fields at F−56, the CRC
at F−4 over [F−64, F−4), and the front block. F mod 64 = 0 is §6.2's
major-1 statement and `[R-CNT-06]`'s post-gate list. So F = 80 with a
correct front block at [0,16), trailer at [16,80), version_major = 7,
verifying CRC is constructible and passes every check §21.2 says
reaches it. Confirmed.

One refinement none of the three made: F5's Instances cell is "F
(physical file size); committed_file_length". The *second* instance is
a trailer field and is reached only through `[R-CNT-06]`'s post-gate
list, so the ordering warrant does hold for it. Only the physical-size
instance is unordered. A repair naming F5 wholesale would be slightly
over-broad.

Also noted, and it is the sharpest form of the defect: `[R-CNT-27]`'s
first sentence is scoped — "No conforming file is shorter than 128
bytes" — and §2.3 makes "conforming file" mean conforming to major 1.
Its second sentence, the reader clause, is unqualified. That is
exactly the seam.

Byte-level: NO. Both readings reject the file. §6.3 `[R-CNT-07]`: "A
reader MUST reject-file when version_major is 0 (invalid) **or is a
major it does not implement**". So reader B rejects at the gate and
reader A rejects at the floor; no file moves between accept and
reject, and a conforming major-1 file cannot be under 128 bytes, so F5
is unambiguous for every file this text judges. What forks is which of
§2.3's three verifier verdicts is reported (*nonconforming* under A,
*cannot establish* under B) and a §6.3 SHOULD-level diagnostic class.
Neither certifies. Severity design-decision: the document owes an
ordering, and reading A additionally collides with `[R-CNF-02]`'s
"neither conforming nor nonconforming under it".

### 2. geometry-term-underdescribes-carveout — quiz-01

Distinct defect from group 1, and I keep it separate because the
repairs do not overlap: group 1 needs an ordering rule (or F5 named
among the reaching rows); quiz-01 needs a word changed. Checked
against the rows: F12 (file_id = 0), F15 (reserved bytes), F19
(incompat lane), F20 (directory CRC), F24 (type 0), F27 (unsorted
document), F34 (second metadata record) are not geometry by any
ordinary sense of the word, and none is among the named four. quiz-01
is right that the excused property and the exception property are not
complements. Its own reading A (the reasoning after the colon does the
work) is correct and is why this is editorial: the clause after the
colon covers those rows even though the word before it does not.
CONFIRMED, editorial. Byte-level NO, on quiz-01's own ground plus
`[R-CNT-07]`'s MUST above.

### 3. metadata-edit-cited-as-shape-c — reader-02

Verified both passages verbatim. §23.1: "editing a user-metadata
document appends a new extent and strands the old one (§20.3's shape
(c))". §20.3 shape (c): "Editing user metadata is not this shape: its
document lives in an extent (`[R-CNT-25]`), so a new extent is
appended and the old one becomes slack, **as in (b)**." Flat
contradiction of label; agreement on mechanics. The cross-reference
should read shape (b). CONFIRMED, editorial. Byte-level NO: both
passages describe the same bytes, and §20.3 decides the classification
outright in the words just quoted.

### 4. appender-drop-bar-vs-preservation-table — reader-03

Quotation accurate. §20.3 step 2: "Against any other structure the
appender carries forward, it MUST NOT repair the defect — `[R-LIF-01]`
freezes the committed prefix — and MUST NOT drop the record (§20.4)."
§20.4's MU = 0 / PE = 0 row does license a drop in a qualifying
commit. reader-03's Reading A is strongly favoured by the sentence's
own premise — a record dropped is not one "the appender carries
forward" — and by the bare "(§20.4)" citation form. Reading B is
available but weak. The §20.5 asymmetry the reporter cites is real:
"Dropping is the one disposal that answers, and only where §20.4's
table licenses it … Where the table does not license a drop the
compactor MUST refuse." CONFIRMED as a looseness worth one clause;
severity editorial. Byte-level NO, per premise P — the fork is whether
one updater run was conforming; both outputs are conforming files.

### 5. bar-list-omits-pad-bits-and-bool-bytes — writer-01

Every element checked. §14.3 Note: "Pad bits are not padding positions
(§11.3)." §14.5 fixes them separately: "Every pad bit (§14.3) MUST
carry the plane's channel's fill bit." §14.2 `[R-SER-08]` fixes
interleaved bool bytes. §20.3 step 4's list names "the set of padding
positions (§11.3) and the content `[R-SER-05]` fixes **there**" —
which does not reach pad bits or bool bytes. §21.7 does: "A change
reaching a byte §14 structurally constrains — a padding position, a
**pad bit**, or a **boolean byte** — fires §21.4's content rows." And
Example (c) says "a layer with no padding position and **no pad bit**".
So the list is short and the document elsewhere shows it.

**PARTIAL**, and this is the correctness call. The reporter frames it
as a live ambiguity with reading (a) — list-as-exhaustive — permitted.
It is not permitted: the same sentence says "The test is the effect on
such a tile, and the list names where that effect arises rather than
standing on its own", and §21.7 and Example (c) both presuppose loci
the list omits. What is real is that the enumeration under-states its
own test — a consistency defect, not a fork. Severity editorial.
Byte-level NO twice over: under P, and independently because §14.5
makes the affected file nonconforming under *either* reading, so no
conforming implementation may emit it either way.

### 6. bar-list-omits-declared-sample-type — adversary-01

Separate group from 5, decisively: repairing 5 (adding pad bits and
bool bytes to the list) leaves 6 untouched. Checked the construction.
§14.2 fixes "a numeric value as its type's element size,
little-endian"; §14.1 fixes value k as "channel (k mod C)'s value". So
the lead test — "what §14 fixes for its stored bytes **or how they
decode**" — does reach a channel's declared type. The list does not,
and neither does §21.7, whose enumeration of the bar's witnesses stops
at §14-constrained bytes, decoded size, codec, filter and sample byte
offset. `[R-TYP-05]`: "Every bit pattern of a numeric type's element
size is a valid sample value" — so float32 → int32 at unchanged
element size fires no row and every verifier certifies. §12.1's
element-size groups make the silent moves real.

Unlike group 5, nothing in the document decides this one: no Example,
no §21.7 clause, no row. That is the live gap. CONFIRMED, severity
design-decision. Byte-level NO under P — and note that P is doing all
the work here, since the emitted file is conforming under both
readings and §21.7 already classes the unwitnessed part of this bar
with `[R-LIF-01]` as a property of history "which §9.7 does not
reconstruct".

### 7. zero-extent-growth-rationale-false — writer-02

Arithmetic checked. §11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉, N = ∏Gᵢ, addressed-tile count
N or C·N. `[R-GEO-02]`: "A dimension with extent 0 is valid" — no
limit on how many. E = (0,0), T = (4,4): G = (0,0), N = 0,
entry_count = 0. Grow E₀ to 4: G = (1,0), a grid count rose, N = 1·0 =
0, entry_count still 0. The Rationale's "growth that raises one
changes entry_count … — the first growth of a zero-extent layer
included" is false there. True for exactly one zero extent, false for
two or more. CONFIRMED. Byte-level NO, quoting §2.1: "All text in this
document is normative except: §1 (Introduction); any text labeled
*Note*, *Example*, or *Rationale*" — this is a Rationale, and
`[R-CNT-17]`, `[R-CNT-23]` and L21/L22 fix every byte independently.
Editorial.

### 8. adding-a-record-as-drop-licence — writer-03

The live ambiguity of this round, in normative text. Row text checked
verbatim: "for a top-level record, the file's layer set, any layer
record's content, or another *non-layer* top-level record. A commit
changes the layer set by adding a layer". For (b): the first item says
"set" explicitly and the third does not — it names *a record*, and
adding one changes no existing record; the gloss that includes
addition attaches to the layer-set item alone. For (a): the row's
closing purpose sentence — "a commit whose only effect would be the
drop MUST retain it" — is satisfied by a commit that also adds; and
the row expressly excludes one same-commit record operation
("Dropping the record, or dropping another record in the same commit,
is not itself such a change") without excluding addition. The
sub-record branch names a container ("that layer's record"), which
addition plainly changes; the top-level branch does not. The reporter
read it accurately and the asymmetry it names is in the text.
CONFIRMED, severity design-decision — this needs a maintainer's
decision, not an editor's.

Byte-level NO, and this is the group where P bites hardest: the two
outputs differ by one record's presence. But an unassigned-type MU = 0
record is conforming present or absent (§21.6, `[R-CNT-15]`), a
creator may emit either file, and the same row lets a compactor drop
it freely ("A compactor MAY drop it whenever it rewrites the file").
No reader's or verifier's verdict on either file moves.

### 9. profile-leaves-tiling-and-layout-open — writer-04

Checked. §11.3 Note: "Tile extents are a writer's choice, and this
specification imposes none." §14.4 Note: "A single-channel bool layer
does not — ⌈P/8⌉ packed bytes planar versus P bytes interleaved — and
both forms are valid". Item 2's own rationale: "two files carrying the
same arrays can legitimately differ in tiling, layout, and codec" —
and the profile pins the codec (item 1) and the filter (item 5) and
neither of the other two named in that clause. Item 5's argument
("changes the stored bytes of every tile it touches, and no content
implies it") transfers verbatim. Two profile adopters can emit
different files. CONFIRMED, editorial.

Byte-level NO: "Appendix G — Reproducible-writer profile
(non-normative)", and "It adds no requirement to any actor: a writer
ignoring it is fully conforming."

Counter-argument I considered and rejected as insufficient: tiling and
layout might be caller input rather than writer freedom. But the same
is true of codec and filter, which the profile pins anyway, so the
distinction does not save the omission.

### 10. shape-c-quantifies-over-layer-not-channel — diagrams-01

Checked. §3.1: a tile is "in a planar layer, one cell of the grid for
one channel". §14.5 fixes padding content "for each channel the
position carries". §20.3 step 4's bar is over "any tile that layer
stores in the generation this commit supersedes" and what §14 fixes
*for it*. So in a planar layer a fill change on channel b alters
nothing §14 fixes for channel f's stored planes, and step 4 permits
it. Example (c) conditions on the layer instead: "A fill change on a
layer that **stores** a tile carrying either is not an appender's
operation at all (step 4)". Over-broad for planar layers; correct for
interleaved. CONFIRMED. Byte-level NO, quoting §2.1's exemption of
text "labeled *Note*, *Example*, or *Rationale*" — step 4 governs, and
both the over-cautious and the correct output are conforming files.
Severity figure.

### 11. r8-instances-underenumerated — diagrams-03, adversary-02

Same defect, two reporters, same proposed repair (four instances,
§21.8 277 → 279). Merged. Both reporters' supporting counts verified
by me mechanically: R1 = 4, R5 = 8, R6 = 4, R7 = 6, R8 = 2, whole
register = 121 rows / 277 instances, matching §21.8 exactly. §18.2's
bullet does state two structurally distinct predicates ("a number
whose binary64 interpretation is not finite … **or** any of the bare
tokens `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not
admit and some parsers accept regardless"). §21.1 leaves "materially
different shapes" to judgement and R8 is the row where the judgement
went the other way, signalled by the word "alike".

CONFIRMED as a bookkeeping question requiring a maintainer's decision,
not an obvious error. Counter-weight I record for the reconciler: a
bare-`NaN` document also exhibits R7's "not well-formed JSON" instance,
and §21.1's specialization list ("F1 of F6 and of F8, F35 of F36, L24
of L25") has no R8-of-R7 pair — so enumerating the bare-token instance
creates a vector exercising two rows, which `[R-VEC-02]` handles but
§21.1 does not pair. Both rows carry the same outcome, detector and
detection point, so nothing observable turns on it.

Byte-level NO: §24 `[R-VEC-01]` — "The corpus is **derivative** …
where a vector's recorded expectation and this specification disagree,
this specification governs" — and §21.8 — "A row without a vector is a
gap in the corpus, not a licence to skip the check."
Register-bookkeeping.

### 12. layout-note-overclaims-7.2-ranges — diagrams-04

Counted §7.2's table: five fields, columns Offset | Size | Type |
Field | Class, no valid-range column. Field cells carrying a range:
`type (0 invalid)` and the flags bit layout. Carrying none:
`inline_length`, `extent_offset`, `extent_length`. §4.7's Note says
"§7.2 folds each field's range into its Field cell". Three of five do
not. CONFIRMED. Byte-level NO: §2.1 exempts *Note* text, and the
ranges are normative at `[R-ENC-03]`, `[R-CNT-12]` and `[R-CNT-13]`,
with §7.2's own next paragraph two lines below the table. Editorial.

### 13. shrink-consequences-overgeneralized — diagrams-05

Arithmetic checked: rank 1, T = 4, E 12 → 10 leaves G = 3 unchanged,
no tile de-addressed, entry_count unchanged, `[R-CNT-17]` obliging no
re-emission. The sentence — "Where a shrink is permitted the
de-addressed tiles' extents become slack (`[R-CNT-21]`), `[R-CNT-17]`
obliges the smaller entry_count and so a re-emitted index region, and
every surviving stored tile is untouched" — has "every permitted
shrink" as subject and states a consequence that holds only where a
grid count falls. §11.1's Rationale carries the distinction on the
growth side; this sentence does not. CONFIRMED, editorial.

Byte-level NO. The permission is fixed elsewhere and cannot be
narrowed by this sentence: "a shrink is permitted exactly where it
alters nothing §14 fixes for any tile the layer stores in the
generation this commit supersedes", and "What counts as such an
alteration is the bar above and nothing else." Re-emitting an
unchanged index region and not re-emitting it are both conforming.

### 14. recovery-citation-omits-f14 — register-02

Both passages checked. §9.5's Note: "A reader meets it as a trailer
that fails its gates — the magic, the CRC, or committed_file_length
against the transport size, each of which §21.2 already registers" =
F8, F14, F17. §9.6: "(§21.2 rows F8 and F17)". F14 omitted, and §9.6's
own probe requires "the trailer CRC to verify", so the case is live in
that very sentence. CONFIRMED. Byte-level NO: the outcome is fixed by
the rule, not the citation — `[R-CNT-06]` "Any failure is
reject-file" — and F8, F14, F17 share detector, detection point and
outcome. Register-bookkeeping.

### 15. hard-limit-provenance-count-short — register-03

Checked the four categories against the list. §7.4 makes A, S and
A_slab u64, so the power-of-two *form* follows from no field width;
from no external format; from no value domain (`[R-ENC-03]` bounds
magnitude only); and from no arithmetic over unomittable structures.
It is chosen here, as the 512 floor is, and chosen twice (§16.1,
§16.2). So "Two do not" is short by at least one. The reporter's
reproduction of the rest of the taxonomy checks out. CONFIRMED.
Byte-level NO: "The hard limits it restates are a finding aid rather
than an inventory — each is normative where the structure forcing it
is defined", and §7.4's table, §16.1 and §16.2 each independently
require the power-of-two form. Editorial.

### 16. cnf-03-missing-top-level-qualifier — adversary-03

Quotation accurate; §7.4 does make sub-records records ("Sub-records
are layer-scope records"). But the question is decided, as the
reporter itself concludes. `[R-CNT-18]`: "an unknown sub-record type
with MU = 1 is reject-layer, and where the file is otherwise
conforming a reader **MUST NOT reject the file for it**". §21.6: "The
qualifier is load-bearing — the same type as a layer sub-record is
reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so
only the top-level case is a file a reader refuses." And §2.3's own
clause delegates: "§21.6's closing paragraph names the other two". So
the missing qualifier sits in a sentence that points at the paragraph
supplying it, and lifting a duty to accept is not a licence to reject.
CONFIRMED as worth a clarifying qualifier; editorial. Byte-level NO on
the `[R-CNT-18]` MUST NOT quoted above.

### 17. l41-antecedent-loose — quiz-02

Checked. L41: "a stored tile's offset ≠ the previous stored tile's
offset plus **that tile's** length". `[R-SLB-03]`: "each stored tile's
offset equals the previous stored tile's offset plus **its** length".
Reading B (the current tile's length) would register almost every
conforming slab layer, so it is unsatisfiable in practice. One
correction to the reporter: `[R-SLB-03]`'s own "its" is not strictly
unambiguous either, though the possessive inside the same noun phrase
reads naturally as the previous tile's. CONFIRMED as loose wording;
byte-level NO, quoting §21.1: "where a row and the rule it cites
diverge, **the rule governs**". Register-bookkeeping.

### 18. compaction-cites-general-not-specialized-rows — quiz-03

Checked. §20.5 names "F36 and L25 for a record type"; §21.1 makes
"F35 of F36, L24 of L25" specializations recorded against the narrower
row. So the citation names the general row where a MU = 1 file would
attribute to the narrower one. CONFIRMED as a citation-completeness
observation, and I add the mitigation neither the reporter nor the row
states: the MU = 1 half cannot reach a compacted output at all, since
`[R-WRT-06]` says "A compactor MUST refuse to compact a file carrying
any record whose type it does not implement with MU = 1", and F35 is
reader/open reject-file so the compactor's own open refuses first. The
citation is therefore complete for the case §20.5's sentence can
reach. Byte-level NO. Register-bookkeeping.

## Tally

21 input ids, 18 groups, each id in exactly one group. Byte-level
count: 0. Recount of member_ids: 3+1+1+1+1+1+1+1+1+1+2+1+1+1+1+1+1+1
= 21.
