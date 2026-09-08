# Triage pass — implementer consequence — cleanroom round 32

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only, by
line range, via `sed -n`. Ranges opened: 1–200 heading index (grep of `^#{1,4} `),
§2.1 (97–116), §2.3–§2.4 (152–300), §3.1–§3.2 (348–410), §5.1 (629–690),
§5.2 (690–767), §7.1 (948–979), §7.3 (1058–1083), §7.4 (1083–1195),
§9.2 (1250–1300), §9.7 (1469–1523), §11.1–§11.3 (1618–1700), §11.4 (1701–1748),
§13.3 (1903–1951), §14.5 (2119–2152), §15 (2154–2277), §18.2 (2611–2790),
§20.3 (3114–3352), §20.4 (3352–3417), §20.5 (3417–3560), §21.1 (3562–3648),
§21.5 (3796–3830), §21.6 (3830–3886), §21.7–§21.8 (3887–3950),
Appendix F (4492–4507), Appendix H (4672–4754); plus a targeted `grep -n` for
register rows F2, F3, F27, F28, L2, L14, L48, L49, T2, T3, T4, T5, T8, T12, T14.

Ran: `wc -l`, `grep -n`, `sed -n`, one `mkdir -p`, and the heredoc that wrote this file.

NOT read: any other triage pass's notes; any walk transcript in
`r32-round/out/` (I opened none, by name or otherwise); `docs/`, `PLAN.md`,
`AGENTS.md`, `conformance/`, `spec/registry.json`, git history, the web.
I ran **no** directory listing anywhere under `r32-round/` — the only `ls`-shaped
call I made was none; `mkdir -p` on my own output directory was the sole
filesystem-touching command outside the spec. Nothing I read was outside the spec
file itself.

Every input finding was evaluated. No finding was skipped for room or judgement.

---

## Grouping

29 input ids → 19 groups.

| group | members |
|---|---|
| note-entrycount-closure | reader-01, writer-03, verifier-02, adversary-02, quiz-01 |
| permitted-change-biconditional | reader-02, writer-01 |
| cnt17-smaller-entrycount | reader-03, writer-04 |
| planar-tail-replacement | writer-02, verifier-03, adversary-01, quiz-03 |
| interleaved-channel-names | quiz-02 |
| fixed-decl-witness-rows | verifier-01, register-01 |
| anatomy-figure-metadata-commit | diagrams-01 |
| appendix-h-reader-acceptance | diagrams-02 |
| appendix-h-updater-reemission | diagrams-03 |
| shape-c-geometry-vs-declarations | diagrams-04 |
| compaction-prime-mark | diagrams-05 |
| l14-condition-third-alternative | diagrams-06 |
| f3-in-domain-qualifier | diagrams-07 |
| s216-reader-rejection-licence | register-02 |
| cnt25-never-invalidates | register-03 |
| registered-type-implementation-premise | adversary-03 |
| json-number-rounding-direction | adversary-04 |
| compactor-regeneration-trigger | adversary-05 |
| slack-walk-incompleteness-grounds | quiz-04 |

Coverage arithmetic: 5+2+2+4+1+2+1×13 … recounted as 5+2+2+4+2+14 = **29**,
each id in exactly one group, no duplicates. The 14 singletons are quiz-02,
diagrams-01…diagrams-07, register-02, register-03, adversary-03, adversary-04,
adversary-05, quiz-04.

Merge notes:
- quiz-03 is grouped with writer-02/verifier-03/adversary-01 even though it
  reaches the opposite conclusion about entry disposition. Same construction
  (shorten the planar channel list and append in one commit), same passage, one
  repair. Its disagreement is recorded inside the group's judgement, not as a
  second group.
- reader-01 and writer-03/adversary-02/quiz-01 are one group: all five attack the
  same parenthetical in §13.3's *Note — sparse writing*. verifier-02 reaches it by
  the alignment/slab route rather than the growth+shortening route; that is the
  same false closure claim, not a second defect.
- reader-03 and writer-04 quote the same sentence ("`[R-CNT-17]` obliges the
  smaller entry_count"); kept apart from the Note group because it is normative
  text and a different sentence.

---

## Judgements

### 1. note-entrycount-closure — CONFIRMED, not byte-level, editorial

The text, §13.3:

> each commit that changes a layer's stored-tile set or its index content —
> which, among the declaration changes §20.3 permits a layer that stores a tile,
> only a change to entry_count does — re-emits that layer's whole tile-index
> region

The closure claim is false at least twice, and I verified both against §20.3
step 4 rather than the reporters' accounts:

(i) Alignment/slab. §20.3 step 4's permitted side carries "a slab or alignment
declaration MAY be declared, re-established or cleared as this step provides
below", and its own closing clause prices it: "an aligned layer's stored tiles —
every one the new state keeps, not only those this commit adds — satisfy its
invariant or the declaration is cleared". With [R-LIF-01] freezing committed
bytes, satisfying the invariant for an already-stored tile at a non-conforming
offset means superseding it at a new offset. Entry offsets change; entry_count
does not.

(ii) Growth + planar shortening in one commit, which "A commit MAY make several
of these changes at once" permits. I re-did reader-01's arithmetic
independently: rank 1, T=1, E 8→16 so N 8→16; C 4→2; entry_count = C·N = 32
before and after; extent_length = 32·20 + ⌈32/2¹⁶⌉·4 = 644 before and after.
[R-GEO-06]'s c·N + s reassigns every ordinal from 8 up. Index content changes
utterly, entry_count does not. quiz-01's variant (E 21→60, T=10, C 4→2,
entry_count 12 both sides) checks out too.

(iii) The category error is real: §20.3 puts entry_count on neither list —
"entry_count and crc_of_crc_array follow the commit, the record's extent slot
with them (§7.2)".

**Downgrade, and the sentences that decide it.** [R-CNF-01], §2.1: "All text in
this document is normative except: §1 (Introduction); any text labeled *Note*,
*Example*, or *Rationale*". The block opens "> **Note — sparse writing.**". The
governing test sits unconditionally at the head of the very step the Note cites:
"Every layer whose stored-tile set or index content this commit changes has its
tile-index region re-emitted in full — entry_count entries plus the segment CRC
array — necessarily at a new placement". That test is keyed to index content, not
to entry_count, and reaches every case above.

**Premise of the downgrade, stated so it can be attacked.** I am assuming that a
*Note* labelled non-normative cannot supply a writer with an operative
re-emission test, even when it makes a factual closure claim in the voice of a
rule and cites `[R-WRT-04]` as its authority. If a triager holds that a Note
which cites a requirement narrows it, this becomes byte-level, because the file a
writer emits under the Note's test is fully conforming and denotes the wrong
array — I checked: entry_count = C·N satisfies [R-CNT-17], extent_length
satisfies the formula, crc_of_crc_array and every segment CRC verify over
unmodified bytes, and no §21 row fires.

**Implementer consequence.** Real, and this is the group's whole cost: a
declare-then-fill writer reads §13.3, not §20.3. Keying re-emission to
`entry_count == old_entry_count` produces a file every checksum certifies whose
channel-1 samples are served at channel-0 ordinals. But two implementations that
read the requirement do not diverge, because the requirement is unambiguous.

### 2. permitted-change-biconditional — CONFIRMED, not byte-level, editorial

> The list is not offered as exhaustive: a change is permitted exactly where the
> declarations it produces satisfy every rule they are subject to.

Read literally and unscoped, this is a sufficient condition over "a change" at
large, and every fixed-side change satisfies it (a new type is assigned, a new
fill's length equals the element size, a new tile extent is ≥ 1). writer-01
flagged it byte-level with a walked example (float32 → int32 re-type, P·B = 16
both ways so no T14/T3, E mod T = 0 so no T4/T5, no bool so no T2).

**Downgrade, and the sentences that decide it.** Two paragraphs above, in the
same numbered step: "A layer that stores a tile **in the generation this commit
supersedes** keeps its declarations, with these exceptions and no other" and "A
commit MUST NOT change one of these; the change is a new layer, or a whole-file
rewrite under a fresh file_id (`[R-LIF-01]`, §20.5)." Also: "Between them the two
lists reach every declaration field of §7.4" — which leaves no residue for a
criterion to reach. And the same step's own figure: "A change to any fixed
declaration of a layer that **stored** a tile in the generation the commit
supersedes — a fill value, a type, a tile extent — is not an appender's operation
at all (step 4)".

**Premise, stated for attack.** (a) "The list" takes the four bounds enumerated
in the sentence immediately before it as its antecedent — [R-COD-07]'s lz4 cap,
[R-ENC-04]'s ceiling, [R-GEO-01]'s channel floor, §4.6/[R-ENC-15]'s names — not
the permitted list three paragraphs up. (b) Even if (a) fails, §2.1's casing rule
makes an all-capitals "MUST NOT" govern over a lowercase "is permitted". Both
premises must fail together for this to fork. If a triager holds that a
biconditional in normative text supplies its own operative rule irrespective of
casing, this becomes byte-level and writer-01's construction is the witness.

**Implementer consequence.** None that survives reading the paragraph the
sentence sits in. The repair is one word.

### 3. cnt17-smaller-entrycount — CONFIRMED, not byte-level, editorial

> A channel removed from the end leaves its stored tiles' extents as slack
> (§5.2), and `[R-CNT-17]` obliges the smaller entry_count and so a re-emitted
> index region;

False in a case the same step expressly permits. Under the group-1 construction
(shorten while growing) entry_count is unchanged, so [R-CNT-17] obliges nothing
"smaller"; and under group 4's construction the removed channel's extents are
re-addressed rather than falling to slack, so the companion clause is false too.

**Downgrade, and the sentence that decides it.** [R-CNT-17] itself, §7.4: "a
mismatch, or an entry_count that does not equal the geometry-derived
addressed-tile count, is a validity error at layer scope". A writer that
decrements instead of re-deriving C·N emits L21 and, through the extent_length
formula, L22 — a nonconforming file [R-CNF-05] bars every conforming writer from
emitting under either reading. And the re-emission obligation the sentence draws
survives on the head-of-step test regardless. So the disputed file is
nonconforming on both readings; the emittable set does not move.

**Implementer consequence.** An implementer misled into a bug the register
catches at layer access. Not a fork.

### 4. planar-tail-replacement — CONFIRMED, **BYTE-LEVEL**

This is the one I uphold.

**The question.** May one commit both shorten a planar layer's channel list from
its end and extend it at its end, so that the last position carries a different
channel — and if so, what may the entries at the vacated disk ordinals address?

**What the text gives each side.** Permissive: "a planar layer's channel list MAY
be extended at its end, **or** shortened from its end … A commit MAY make several
of these changes at once." The antecedent of "these changes" is the enumerated
changes, not the bullets — and it must reach within a bullet at least once, since
switching a layer from a slab to an alignment requires clearing one and declaring
the other in one commit ([R-CNT-16] makes A ≠ 0 and S ≠ 0 mutually exclusive) and
both live inside the fourth item. The tie-break hands the field over wholesale:
"where a field is on both sides — a dimension extent, a planar layer's channel
list — the permitted side states the whole of what a commit MAY do to it". And
the fixed side affirmatively frees the tail: "the position of every planar
channel but the last".

Restrictive: "every channel's type and fill" is fixed; "a re-type … [is a]
rewrite even where a particular file would survive [it] in place"; "the permitted
side states the whole of what a commit MAY do to it" can be read as a test on the
net effect.

**The sentences I looked for and did not find.** (a) that the two channel-list
alternatives do not compose within one commit; (b) that the net effect on a
planar channel list must be an extension at its end or a shortening from its end;
(c) that an entry new to a generation must not address bytes an earlier
generation's entry addressed; (d) that a disk ordinal must address the same
channel it addressed in the superseded generation. None is in the document. The
nearest thing is the tense sentence — "a commit does not earn an empty layer's
freedom by emptying the layer as it re-declares it" — which closes exactly one
composition (unstore-then-redeclare) and is justified on a ground specific to the
tense of "stores a tile", so it does not generalise; if anything, its presence
argues *expressio unius* for the composition it does not close. The re-emission
clause's parenthetical "(a growth renumbers ordinals wherever `[R-GEO-06]` moves
them, and nothing else this step permits moves one)" is not it either: the
composition moves no ordinal, it changes which channel occupies one, and the
parenthetical does not speak to that.

**The drafters' own justification fails on this case, which is the evidence that
the text does not decide it.** "an appended planar channel adds tiles at ordinals
after every existing one, a disk ordinal being c · N + s with N the spatial-tile
count" — false when a shortening freed index C−1 in the same commit. "a channel
removed from the end takes only its own tiles out of the addressed set, and a
tile the new state does not address carries no obligation" — false, because the
new state does address those ordinals.

**Where I part company with the reporters.** writer-02's updater P — carrying the
removed channel's entries forward byte-identically under the catch-all — is
decided against by the text, and quiz-03 is right about this. The re-emission
clause categorises *entries*, and lists "an appended channel" among "entries new
to this generation … emitted per §15"; an entry addressing a tile of a channel
appended in this generation is such an entry, so it is not "every other entry".
That sub-question is closed. It does not close the group.

**What is not closed, and is the byte-level core.** Under the permissive reading
a writer emits entries for the appended channel "per §15" — and §15 lets an entry
address any extent in [16, F − 64) that does not overlap another claimant.
Nothing bars pointing it at the extents the removed channel just vacated, and
§3.1 makes the tile *stored* by that act: "A tile is *stored in a generation* if
and only if that generation's tile-index entry for it is not the sentinel". So
adversary-01's construction is admissible on the text: gen 2's entry 1 =
(20, 4, 0xDD54C4AB), byte-for-byte addressing gen 1's channel-`b` float32 tile,
now declared int32.

I verified there is no witness. [R-COD-04]/T14 and [R-SER-07]/T3: P·B = 1·4 = 4
for float32 and int32 alike. [R-SER-05]/T4 and T5: E = T so there is no padding
position, and no bool plane. T2: no bool channel. [R-CNT-17]/L21: entry_count =
C·N = 2 both generations. L22: extent_length = 2×20 + ⌈2/2¹⁶⌉×4 = 44 both.
[R-CNT-02] partitions. Every checksum in §8 verifies over bytes nobody changed.
This is, in the section's own words, "the same bytes … denot[ing] values …
the writer did not store, with every checksum in §8 certifying the result … no
check any actor owes able to see it".

**The two implementations, concretely.** Both are handed the same file and the
same caller request: drop trailing channel `b` (float32), add trailing channel
`q` (int32).

- Team A composes the two permitted operations in one commit. It appends a 44-byte
  index region, a directory, a pad and a 64-byte trailer — a few hundred bytes —
  and keeps the file's `file_id`, so every `(file_id, range)` cache of it stays
  warm ([R-LIF-03]). If its index writer re-points the appended channel's entries
  at the vacated extents (the cheapest thing to write, and nothing forbids it),
  `q` serves `b`'s float32 bit patterns as int32 1,065,353,216 where `b` read 1.0.
- Team B computes the net delta on the channel list, sees the tail replaced,
  refuses the commit and performs a whole-file rewrite under a fresh `file_id` —
  megabytes on a real layer, every cached range of that file invalidated by
  §9.3's contract, and prior generations discarded.

Same input, same API call, different files on disk, and under Team A's second
variant a different reference array. That is the emittable set moving.

**Repair (a maintainer decision, two shapes).** Either (i) close the composition:
state on the permitted side that a commit's net effect on a planar layer's
channel list is an extension at its end or a shortening from its end, and that
the two do not compose in one commit; or (ii) open it and fence it: permit the
composition and add that an entry new to this generation MUST NOT address an
extent a superseded generation's entry addressed — and then repair the two
justification clauses ("adds tiles at ordinals after every existing one"; "a tile
the new state does not address carries no obligation"), which are false under
(ii) and would otherwise stand as false normative prose. Under either shape the
sentence in §20.3's bounds paragraph about a removed channel leaving its extents
"as slack" needs the same qualification (group 3).

**Why I did not treat verifier-03's counterweight as decisive.** verifier-03 and
adversary-01 both note that a *creator* could emit the disputed file byte-for-byte,
so the set of conforming files does not move. True, and I checked it. But the
test the brief states is which byte sequences a conforming implementation may
emit — and an updater is a conforming implementation. From this input, one reading
permits the emission and the other forbids it. Holding otherwise would make every
updater-conduct rule in §20.3 unfalsifiable at the byte level, which would in turn
make the whole closed list that ADR-0124 introduced non-byte-level by construction.
I do not accept that.

### 5. interleaved-channel-names — CONFIRMED, not byte-level, editorial

May a commit rename an interleaved layer's channel while the layer stores a tile?
The question is real: the permitted side's "its name, and its dimension and
channel names, MAY change" is unqualified by layout, the fixed side names "an
interleaved layer's channel list", and the tie-break's on-both-sides list
("a dimension extent, a planar layer's channel list") does not mention it.

**Downgrade, and the sentences that decide it.** Three, all in the same
paragraph. (a) "its name, and its dimension and channel names, MAY change" —
stated without a layout qualifier, in a paragraph that qualifies by layout
wherever it means to ("a **planar** layer's channel list", "an **interleaved**
layer's channel list", "every **planar** channel but the last"). (b) The fixed
side enumerates "every channel's type and fill" *separately from* "an interleaved
layer's channel list"; that separation is redundant unless "channel list" means
membership and order rather than the per-channel entries. (c) The principle
paragraph's ground for the permission is generic: "a name enters no map". Add
that "Between them the two lists reach every declaration field of §7.4" — a
channel name is such a field, and the permitted side is where it is reached.

**Premise, for attack.** That "an interleaved layer's channel list" names
membership and order, not the C channel entries of §7.4 with their names. If a
triager reads "channel list" as the entries, this has the same shape as group 4
and would be byte-level for the same reason. I judge (a)–(c) to settle it; group
4 has nothing of that strength on the closing side, which is why the two are
graded differently.

**Implementer consequence under the wrong reading.** Over-strictness: a whole-file
rewrite under a fresh file_id, breaking every `(file_id, range)` cache
([R-LIF-03]), to change a few bytes of one directory record. Costly, but both
outputs are conforming files.

### 6. fixed-decl-witness-rows — CONFIRMED, not byte-level, editorial

> … but for a decoded size or a boolean byte the register witnesses (T3, T14,
> T2), no check any actor owes able to see it (§21.7).

The enumeration is exhaustive in form ("but for X … no check … able to see it")
and omits T4 and T5, which the same §21.7 it cites names: "The obligations of
§14.5 and `[R-SER-08]` narrow this only where content is structurally
constrained: padding positions, pad bits, and boolean bytes" — three classes, not
two. I confirmed the rows by grep: T4 "A padding position does not encode, for
each channel it carries, that channel's recorded fill value | interleaved numeric
fill bytes; interleaved bool fill byte; planar numeric plane fill bytes; packed
planar bool plane fill bit | verifier | certification | `[R-SER-05]`"; T5 the pad
bits of a packed planar bool plane. register-01's worked witness (uint8 fill 0x00
→ 0xFF, extent 5, tile extent 4) is right; so is verifier-01's float32 case.

**Downgrade, and the sentence that decides it.** §14.5, [R-SER-05]: "at every
padding position, a writer MUST encode, for each channel the position carries,
that channel's fill value … a verifier MUST check it, and a violation is a
validity error at tile scope." Unconditional, and §21.1: "where a row and the
rule it cites diverge, **the rule governs**." The complained-of sentence grants
no permission, states no condition a file can exhibit, and sits inside a
justification for a closed list that bars the change on both readings.

**Implementer consequence.** A verifier author who takes the parenthetical as a
census of the register's witness set may conclude padding content need not be
re-checked when a layer's declarations move. T4 and T5 stand on their own, so a
verifier built to §14.5 is correct anyway. The defect is that the document's
account of its own detection surface is wrong in the passage whose entire purpose
is to explain why the line falls where it does — and that it disagrees with the
section it cites for the proposition.

### 7. anatomy-figure-metadata-commit — CONFIRMED, figure

> so a commit that touches no layer re-emits the directory, the pad and the
> trailer alone.

Confirmed false against [R-LIF-02] step 2, §9.2: a commit appends "new stored-tile
payloads and tile-index regions for the layers it changes, **and any new record
extents (file-scope or layer-scope)**". [R-CNT-25], §7.1: "Each user-metadata
record carries its document in its extent — never inline". §20.3's own shape-(c)
figure says so in terms: "Editing user metadata is not this shape: its document
lives in an extent (`[R-CNT-25]`), so a new extent is appended and the old one
becomes slack, as in (b)."

**Downgrade:** both passages are inside blocks labelled *Example* ([R-CNF-01]),
and [R-LIF-02] step 2 governs unambiguously. A writer misled by §5.1 could only
fail to append an extent it needed, producing a record whose slot points at
nothing — [R-CNT-13]/[R-CNT-02], barred by [R-CNF-05] on both readings.

**Implementer consequence.** An implementer treating §5.1's figure as the
enumeration of commit shapes has no shape for the commonest metadata edit the
document names, and §20.3's figure would then read as a fourth shape rather than
a correction. Repair: scope it — "a commit that touches no layer and adds no
record extent".

### 8. appendix-h-reader-acceptance — CONFIRMED, editorial

Checklist: "accepts every conforming file within §21.9's minimum guarantees".
[R-CNF-03] states three qualifiers; the checklist keeps one. §21.6 names the file
that bites: "an **experimental-range top-level record type carrying MU = 1**
(§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes
the file conforming all the same."

**Downgrade:** Appendix H is headed "(non-normative)" and disclaims itself in its
first sentence — "each entry's authority is the requirement or section cited,
never this summary" — and [R-CNF-03], [R-CNT-15], §21.6 and [R-ERR-04] all decide
the case identically. The same appendix's *updater* entry even states the rule
correctly ("rejects outright a file carrying an unimplemented top-level MU = 1
record"), so the appendix contradicts itself rather than the spec.

**Implementer consequence.** An implementer auditing a correctly-rejecting reader
against the checklist marks it nonconforming, or builds one that accepts. That
is the appendix's stated purpose ("for implementers auditing their own work"),
which is why it is worth repairing.

### 9. appendix-h-updater-reemission — CONFIRMED, editorial

Checklist: "re-emits every retained record byte-identically (§20.4)". [R-WRT-05]:
"every record it retains **and does not logically modify** … a record it modifies
is new output under its writer obligations (`[R-CNF-05]`)". §20.4 keeps the two
conditions apart deliberately — "The table states what an updater owes a record it
does not logically modify". The checklist entry contradicts its own preceding
clause, which permits an updater to change a layer's names, grow an extent, and
declare or clear a slab, none of which can be re-emitted byte-identically.

**Downgrade:** non-normative appendix, self-subordinating, and [R-WRT-05] states
both conditions in the section the checklist cites.

**Implementer consequence.** Over-strictness on the audit (an auditor thinks
renaming a layer is barred), plus loss of the second half — that a modified record
is new output under writer obligations and must be validated as such rather than
copied forward. Repair: restore the five words.

### 10. shape-c-geometry-vs-declarations — CONFIRMED, figure

Step 4: "subject to every rule its new **declarations** are subject to". Shape (c):
"subject to every rule its new **geometry** is subject to, which is the same
step's permission". §11.1's Rationale: "may be re-declared freely" — no qualifier.
Three statements, three qualifiers. Confirmed that this document uses *geometry*
narrowly (§11.1 is headed "Geometry and its validity floor"; §10.4 lists
"geometry, channel sets and layout, codecs, filters, linearization, fill" as
distinct things), so "new geometry" drops [R-COD-07]'s lz4 cap, [R-TYP-07]'s bool
fill constraint, [R-CNT-16]'s A/S exclusivity, and the §7.4 value sets.

**Downgrade:** both restatements sit in labelled blocks (*Example*, *Rationale*),
and [R-CNT-23], [R-CNT-16], [R-COD-07] and the rest bind a layer record in any
generation independently of §20.3 — so a file written on the narrow reading
carries a register row and [R-CNF-05] bars it either way.

**Implementer consequence.** A reader of the figure alone concludes an emptied
layer's non-geometry declarations are not rechecked. Repair: one word, and align
§11.1's Rationale with it.

### 11. compaction-prime-mark — CONFIRMED, figure

The caption compounds two operations under one mark: "extent slots are re-pointed
**and** each index region any of whose stored extents moved is regenerated — the ′
marks". In the drawing A's tiles sit immediately after `front` in both rows, so on
the drawing's own left-to-right reading A's extents did not move and `A: index′`
asserts a regeneration [R-WRT-07] does not license there.

**Downgrade:** [R-WRT-07]'s normative text is unambiguous — it "regenerates each
tile-index region any of whose stored extents the output relocates" — and where
nothing moved a regenerated region is byte-identical to a copied one (offsets,
lengths and crcs unchanged, segment CRCs recomputed over identical entries).

**Implementer consequence.** Non-zero and worth naming: §20.5 makes regeneration
the step at which a compactor necessarily meets a structurally malformed entry
("regenerating the region cannot proceed without meeting it … `[R-WRT-06]` then
obliges refusal"), so whether an unmoved region is regenerated or copied decides
whether the compactor is put in front of a defect it is not otherwise obliged to
look for. The divergence is refuse-versus-emit on an input already nonconforming,
whose compacted output carries the violation either way. Repair: draw A's tiles
as relocated, or mark only B's region.

### 12. l14-condition-third-alternative — CONFIRMED, register-bookkeeping

Verified by grep. L14 Condition: "A sub-record does not fit in the layer record's
inline payload: its 24-byte header is truncated at the payload end, or its
inline_length runs past that end". L14 Instances: "sub-record header; sub-record
inline_length; trailing residue" — three. [R-CNT-18], §7.4: "the remaining bytes
MUST parse as zero or more complete sub-records under §7.2's framing with no
residue; any overrun, truncation, or residue is a validity error at layer scope".
The parallel file-scope row F29 states all three. The Condition cell is missing
the residue alternative.

**Downgrade:** §21.1, "where a row and the rule it cites diverge, **the rule
governs**", and §21.1 makes the instance count mechanical from the cell, so the
totals are unaffected.

**Implementer consequence.** A corpus builder constructing L14's third vector
must go to [R-CNT-18] to learn what condition it exhibits, because the row does
not name it; [R-VEC-03] obliges "at least one vector for each instance it names".
Repair: add ", or bytes remain after the last complete sub-record" to the cell.

### 13. f3-in-domain-qualifier — CONFIRMED, register-bookkeeping

Verified by grep. F3: "A sum of a u64 offset and length taken from the file
exceeds 2^63 - 1, so the sum wraps". L2 and T12 both carry the qualifier F3 lacks
— L2: "although every contributing field is in domain"; T12: "although each field
alone is in domain". Without it, F3 is entailed by F2 for the same field, and
§21.1's specialization rule would record the file against F2 without the row
saying so. "so the sum wraps" also reads two ways; [R-ENC-04] states the
condition as exceeding 2⁶³ − 1 with no wrap requirement.

**Downgrade:** §21.1, "where a row and the rule it cites diverge, the rule
governs"; [R-ENC-04] is operative and no verifier verdict is open.

**Implementer consequence.** A corpus builder working from F3's cell alone may
construct a vector that in fact exercises F2. Repair: add the in-domain qualifier
its two siblings carry, and demote "so the sum wraps" to a consequence.

### 14. s216-reader-rejection-licence — CONFIRMED, editorial

> What belongs here is the reader's side of them, and it is unchanged: neither is
> a reason for a reader to reject anything.

§2.4/[R-CNF-12], as quoted in §2.3: "a violation whose assigned detector is the
verifier imposes no reader obligation … though a reader detecting one MAY reject
the file (`[R-CNF-12]`)". Now that F27/L48 and F28/L49 are registered violations
the files are nonconforming and that licence attaches. The document makes exactly
this qualification for the structurally identical case in [R-CNT-18]: "where the
file is otherwise conforming a reader MUST NOT reject the file for it — on a
nonconforming file `[R-CNF-12]`'s licence to reject on any detected violation is
untouched". §21.6's sentence omits it.

**Downgrade, and the sentences that decide it.** §21.6's opening rule is scoped
to "**These**" — the table's entries — and these two conditions are expressly not
among them ("Two conditions that once sat in this table are violations and are
registered above"). And §2.1 binds BCP 14 keywords "when, and only when, they
appear in all capitals", so a lowercase "is a reason" cannot bound an
all-capitals "MAY reject".

**Implementer consequence.** An implementer taking the strong reading builds a
reader that must serve a file the register calls nonconforming, and would count a
[R-CNF-12]-exercising reader as the nonconforming party. Repair: adopt
[R-CNT-18]'s wording verbatim.

### 15. cnt25-never-invalidates — CONFIRMED, editorial

> Application metadata never invalidates the structural data it annotates.

Unscoped, in a paragraph whose subject is outcome assignment ("is ignore-record
with a SHOULD-report, notwithstanding the owning-scope mapping of `[R-CNF-08]`").
F27 and L48 record an unsorted document as a violation at file and layer scope.

**Downgrade, and the sentence that decides it.** [R-MTA-05], §18.2: "unsorted
members do not make a document unreadable: the file is nonconforming, a verifier
MUST report it, and readers process the document unchanged." That is the later,
more specific rule and the one F27 and L48 cite, so §21.1's "where a row and the
rule it cites diverge, the rule governs" resolves toward it. [R-CNT-25]'s
quarantine is scoped to unreadability ("each way a user-metadata record's document
can be unreadable once its framing has been read"), and unsortedness is expressly
outside it.

**Implementer consequence.** A verifier author who reads §7.1 and stops there
certifies a file §21 records as nonconforming — a verdict fork on paper, closed by
[R-MTA-05] for anyone who reaches it. Repair: a scope word — "never causes a
reader to reject the structural data it annotates" — or a pointer to [R-MTA-05].

### 16. registered-type-implementation-premise — CONFIRMED, editorial

[R-CNF-03] relieves the acceptance duty for a file "carrying no top-level record
of a type it does not implement with MUST_UNDERSTAND = 1", and glosses "in a
conforming file such a type is necessarily from the experimental range". §7.3
fixes type 0x0001 (layer) at MU = 1, so the gloss is false on its face for a
reader that does not implement 0x0001. §20.4 leans on the same unstated premise
and says so out loud: "an updater implements both registered types".

**Downgrade, and the sentences that decide it.** [R-CNF-04], §2.3: "A reader MUST
detect every violation the error register (§21) assigns to the reader as its
detector, and apply the outcome class this specification assigns to each" — §21.3
assigns a large number of layer-scope rows to the reader at detection point
*layer access*, none of which is detectable without parsing type 0x0001. And
[R-CNF-03]: "There are no subset profiles". A reader that declines the layer
record fails [R-CNF-04] outright, so the relief clause never reaches 0x0001.

**Implementer consequence.** None in practice: no team ships a reader that
rejects every file containing a layer and calls it conforming, and adversary-03's
one reachable divergence (an updater dropping a layer record) additionally needs
a nonconforming input storing MU = 0 / PE = 0 on a layer record, which [R-CNF-05]
already bars any conforming writer from producing. Repair: state the premise once
— implementing a format major entails implementing the record types §7.3 registers
for it — so the gloss and §20.4's aside rest on text.

### 17. json-number-rounding-direction — PARTIAL, not byte-level, design-decision

**The reporter's own construction is refuted.** adversary-04 picks the exact
midpoint 2¹⁰²⁴ − 2⁹⁷⁰ and argues roundTiesToEven makes it infinite while
roundTowardZero makes it DBL_MAX. But [R-MTA-04] states, in normative text,
"which covers a magnitude that overflows on conversion, `1e400` being the ordinary
case", and §21.5's R8 repeats it: "a magnitude whose binary64 interpretation
overflows (`1e400`)". Under roundTowardZero 1e400 converts to DBL_MAX — finite.
So the document's own example rules out every clamping rounding direction
(roundTowardZero, and roundTowardNegative for a positive value). Every remaining
direction — roundTiesToEven, roundTiesToAway, roundTowardPositive — maps his exact
midpoint to +∞, because the midpoint exceeds DBL_MAX = 2¹⁰²⁴ − 2⁹⁷¹. Both
verifiers establish R8. His fork does not open.

**What survives.** The rule genuinely names no rounding-direction attribute, and a
narrower literal reaches it: a value strictly between DBL_MAX and the midpoint
(say 2¹⁰²⁴ − 1.5·2⁹⁷⁰) rounds to DBL_MAX under roundTiesToEven and to +∞ under
roundTowardPositive, and both are consistent with the 1e400 clause.

**Downgrade of that residue, and the sentence that decides it.** [R-MTA-04]: "A
reader interprets every JSON number as an **IEEE 754** binary64 value" — and
IEEE 754-2019 is a normative reference of this document (Appendix F: "**[IEEE 754]**
IEEE 754-2019 — binary16, binary32, and binary64"), whose default
rounding-direction attribute for binary formats is roundTiesToEven. Naming the
format imports its default.

**Premise, stated for attack.** That invoking "an IEEE 754 binary64 value"
imports IEEE 754's default rounding-direction attribute rather than leaving the
attribute to the reader's ambient environment. If a triager holds that Appendix F
cites IEEE 754 only "for binary16, binary32, and binary64" — the formats, not the
conversion operations or the default attribute — then the residue is a real fork
and this is byte-level, with the narrow literal above as the witness.

**Implementer consequence.** Nil in practice: every decimal-to-binary64 converter
a JSON parser reaches (strtod and its equivalents) runs under the default
attribute, and a directed-rounding parser is not a thing anyone ships. But
[R-VEC-03] asks the corpus for a vector at every stated bound, and R8's boundary
vector cannot have a stable expected outcome until the attribute is named.
Repair (a maintainer decision, not an edit I would make unilaterally): add
"under roundTiesToEven" to [R-MTA-04]'s second restriction, and say whether the
"MAY use a wider representation" licence changes the test (it does not — the test
is stated over the binary64 interpretation).

### 18. compactor-regeneration-trigger — CONFIRMED, not byte-level, editorial

The construction is right: [R-WRT-07] keys regeneration to relocation
("regenerates each tile-index region any of whose stored extents the output
relocates") while "A compactor MUST preserve content, and preserves no placement …
it is free to place structures anywhere §5.2 admits", so a packing that leaves a
layer's tiles in place never regenerates its region, never classifies its entries,
and carries an offset = 5 entry (T8) into the output; a different packing meets it
and MUST refuse.

**Downgrade, and the sentence that decides it.** [R-WRT-09]: "it relies
structurally on every structure it copies, so it MUST verify each link of the
chain — the open (§19.1), each retained layer's record (§19.3) and full index
chain (`[R-IDX-04]`), and each relocated extent's checksum, **including every
stored tile's entry crc**". The restrictive reading of "including" is
self-defeating: a relocated stored tile's extent checksum *is* its entry crc, so
under that reading the clause says nothing at all. "every stored tile's entry crc"
is therefore owed whatever the compactor relocates — and verifying one obliges the
compactor to use the entry, which under §19.4's tile-read algorithm means
classifying it under §15.3. The malformed entry is met under every placement.

**Implementer consequence.** A team that takes the restrictive reading of one
compound list ships a compactor that silently launders a nonconforming index into
its output whenever its packing happens to leave a layer's tiles where they were —
and, since compaction mints a fresh file_id, the laundered output looks like a
first committed state. Both files are nonconforming either way, so the emittable
set does not move, but the divergence in tool behaviour is real. Repair: split the
list — "each relocated extent's checksum, and every stored tile's entry crc
whether or not the output relocates it".

### 19. slack-walk-incompleteness-grounds — CONFIRMED, editorial

§5.2: "The walk is incomplete where a **scope-level rejection** ends that scope's
enumeration …". §2.4 makes tile one of three scopes and §15.3 classifies six entry
states reject-tile on a *structural* ground, so §5.2's first ground reads onto them
unless something excludes it. §5.2's own qualifier does not: it exempts "a tile's
or a document's decode declined", a resource decline, and says "that claimant
being enumerated from its index entry or extent slot", which a structural entry
does not supply.

**Downgrade, and the sentences that decide it.** Two, both outside §5.2. §9.7:
"An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground does not
make the walk incomplete: the walk passes over it, and the bytes it nominally
addresses fall to slack (§15.3)" — and §9.7's first paragraph says it a second
time parenthetically. §15.3 says it a third time: such an entry "contributes …
none to `[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed that no
other claimant claims fall to slack." Three statements against §5.2's silence.

**Implementer consequence.** A verifier author looking for the incompleteness
grounds reads §5.2, where they are enumerated, and reports every slack total as
partial for a file carrying one malformed index entry — telling an operator that
the figure is an upper bound when it is exact, and depriving §22.3's compaction
signal of the completeness it asks for. Nothing a writer emits changes, and no
file is accepted or rejected differently: §5.2 itself says of a partial total "It
is not the file's slack total but a bound on it". Repair: carry §9.7's carve-out
into §5.2's list, or replace §5.2's enumeration with a pointer to §9.7's.

---

## Tally

Byte-level upheld: **1** of 29 findings, in 1 of 19 groups —
`planar-tail-replacement` (writer-02, verifier-03, adversary-01, quiz-03).

Reporters self-flagged byte-level: 4 (writer-01, writer-02, adversary-01,
adversary-04). Two of those (writer-02, adversary-01) are in the group I upheld;
writer-01 downgraded on §2.1's casing rule and the antecedent of "The list";
adversary-04 downgraded, and its specific construction refuted, on the
document's own `1e400` clause.
