# Round 26 triage — correctness lens — working transcript

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — §§1–2 (all),
3.1, 3.2, 4.1–4.7, 5.1, 5.2, 6.1–6.4, 7.1–7.4, 8.1–8.2, 9.1–9.7, 10.1–10.4,
11.1–11.4, 12.1–12.2, 13.1–13.3, 14.1–14.3, 15.1–15.4, 16.1–16.2, 17.1–17.4,
19.1–19.4, 20.1–20.5, 21.1–21.9, Appendix A, Appendix G.

Ran: `grep -n '\blast\b'`, `grep -n 'geometr'`, `grep -n 'stored-tile set'`,
`grep -n '^####'` over the spec. No other file was read. I did NOT open any
`transcript-*.md`, walk or triage — I did `ls` the round26 directory once
before I had read the charter's prohibition on listing it; the listing showed
only file names (calc.py, check.py, and the six walk transcripts plus three
quiz transcripts). No `transcript-triage-*` file exists in that listing and
none was opened. Nothing from that listing informed any judgement.

No `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`,
git history, or web.

## Grouping

25 ids → 17 groups. Coverage check by hand, id by id:

| id | group |
|---|---|
| reader-01 | 2 |
| reader-02 | 1 |
| reader-03 | 4 |
| writer-01 | 1 |
| writer-02 | 2 |
| writer-03 | 5 |
| writer-04 | 6 |
| writer-05 | 7 |
| writer-06 | 16 |
| verifier-01 | 9 |
| verifier-02 | 10 |
| verifier-03 | 1 |
| diagrams-01 | 11 |
| diagrams-02 | 3 |
| diagrams-03 | 2 |
| diagrams-04 | 8 |
| register-01 | 12 |
| register-02 | 13 |
| register-03 | 14 |
| register-04 | 5 |
| adversary-01 | 15 |
| adversary-02 | 1 |
| quiz-01 | 17 |
| quiz-02 | 1 |
| quiz-03 | 2 |

Sizes: 5+4+1+1+2+1+1+1+1+1+1+1+1+1+1+1+1 = 25. Every id once.

Two near-merges I declined:

- diagrams-02 (§20.3's cost Note) vs group 2 (§13.3's sparse Note). Same
  *kind* of error — a Note keying re-emission on the stored-tile set alone —
  but two different passages needing two different edits. diagrams-03 itself
  says "the same case as diagrams-02, reached through a different phrasing";
  its *location* is §13.3, so it groups with §13.3.
- writer-04 vs diagrams-04 (both Appendix G, item 5 + closing paragraph).
  Different claims: writer-04 says the closing enumeration omits the filter;
  diagrams-04 says item 5's argument fits layout and tiling equally and
  "Everything else … is already mandatory" is false under one reading of
  "the same input". Different repairs. Kept apart.
- writer-06 (§20.3 says nothing about C or d changing) vs reader-01's third
  case (ordinal renumbering with entry_count unchanged). Related consequence,
  different passages and different repairs. Kept apart.

## Verifications, one by one

### Group 1 — §11.1 Rationale, "last" (reader-02, writer-01, verifier-03, adversary-02, quiz-02)

Text at line 1495–1502:

> Growth that leaves **entry_count** unchanged touches the directory alone —
> a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0
> among them, the product holding at 0. Growth that changes entry_count
> changes extent_length with it (`[R-CNT-17]`), … — the growth that raises a
> zero-extent layer's **last** zero grid count included.

Both readings check out. Positional ("last-declared"): with G = (0, 5, 0),
raising G₂ leaves ∏G = 0, entry_count unchanged — the *previous* sentence's
class, so the clause is false. Final-remaining: raising the last zero takes
the product off 0, entry_count changes, clause true.

Census verified by grep (`\blast\b`, 17 hits): 163 "that last ground"
(most-recently-mentioned), 194 "the last where some requirement" (positional
in a list of three), 504 "The last two are separate namespaces", 566 "trailer
last, in that order", 614 "the last ones in the file", 1249/1294 "the last
committed state", 1527 "the last row of tiles", 1553 "the last-declared
dimension varies fastest", 1900 "the last value", 2096 "the last covering
16,960 entries", 2202 "a band along the last-declared dimension", 3468 "the
last complete record", 3719 "the last two", 3757 "The last three rows",
4298/4299 "the digest's last eight bytes in output order". The reporters'
claim holds: 1502 is the only candidate for a "final remaining" sense, and
the two uses that index a *dimension* both say "last-declared".

adversary-02 adds a point the others miss and it is correct: in a rank-3
layer with two zero extents, neither zero is "the last remaining" until one
has been raised, so even the intended reading is loose.

Byte level: no. `[R-CNF-01]`: "All text in this document is normative except:
§1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*". This
is a Rationale. §20.3 step 4 and `[R-CNT-17]` are normative and unambiguous,
and §11.1 itself defers: "§20.3 states normatively, and governs".

Repair: "last **remaining**" / "final remaining".

### Group 2 — §13.3's "Note — sparse writing" (reader-01, writer-02, diagrams-03, quiz-03)

Note: "each commit that changes a layer's stored-tile set, or that grows its
extents so that entry_count changes, re-emits that layer's whole tile-index
region". Rule (§20.3 step 4): "Every layer whose stored-tile set **or index
content** this commit changes has its tile-index region re-emitted in full".

Three commits satisfy the rule and not the Note, all verified:

(a) Supersede. §3.1: "A tile is *stored in a generation* if and only if that
generation's tile-index entry for it is not the sentinel." A supersede leaves
every entry non-sentinel, so the set is unchanged; the offset/length/crc
change, so index content changes. §20.4 confirms the document knows this:
"Superseding a stored tile's bytes re-places that layer's index region (§20.3,
`[R-WRT-04]`), moving its extent slot (§7.4) and so modifying that layer's
record".

(b) Shrink changing entry_count. §20.3: "`[R-CNT-17]` obliges the smaller
entry_count and so a re-emitted index region". The Note says "grows".

(c) reader-01's renumbering case. Rank 2, tile extents (1,1), extents (2,3) →
(3,2). entry_count 6 → 6, extent_length unchanged, stored set can be unchanged
(store only tiles addressed under both), yet every ordinal moves under
`[R-GEO-06]`. §20.3 step 4 names it: "(a geometry change renumbers ordinals
wherever `[R-GEO-06]` moves them)". Neither of the Note's disjuncts fires. I
checked the shrink half is permitted: with T = (1,1) there are no padding
positions and no decoded-size change, so the bar alters nothing §14 fixes.

House form verified by grep on "stored-tile set" (6 hits): §5.1's Example
(606) and §20.3 step 4 (2989) both carry "or index content"; `[R-SLB-04]`
(2179) uses it for a different purpose; 610, 1791 and 3086 are the loose ones,
of which 1791 is this Note and 3086 is group 3.

Byte level: no. Non-normative Note; §20.3 step 4 governs. Case (a) yields a
conforming file with a lost edit; case (b) yields an L22 file the rule already
rejects; case (c) yields a conforming file with a wrong reference array, which
§21.7 already records as unwitnessed. The *emittable set* does not move,
because a writer following the normative rules emits the same bytes on either
reading.

### Group 3 — §20.3's cost Note (diagrams-02)

> **Note.** A commit's cost is dominated by its index, not its data: any
> change to a layer's stored-tile set re-emits that layer's whole tile-index
> region, so editing one sample of a 10⁶-tile layer appends about 20 MB of
> index and leaves as much slack.

The implication stated is true; the instance ("editing one sample") is a
supersede, which by §3.1 does not change the stored-tile set. So the "so"
runs through a trigger its own example does not fire. (If the edited tile was
previously unstored, the set does change — but that is not what "editing one
sample" ordinarily names, and it is not the 20 MB case the Note quantifies.)

Byte level: no — same grounds as group 2, plus diagrams-02's own point that
`[R-LIF-01]` makes the mis-keying physically unsurvivable into an emitted file.

### Group 4 — §16.1's alignment invariant (reader-03)

`[R-SLB-01]`: "When declared: every stored tile's offset satisfies offset mod
A = 0." §3.1 makes a structurally-rejected non-sentinel entry's tile *stored*,
so the invariant literally reaches it. §16.2 states the transparency in its own
text; §16.1 does not.

What settles it, and reader-03 has this right, is `[R-IDX-03]`: "Such an entry
contributes no stored extent to the *verifier* rows, which bind over
well-formed entries' extents only". §15.3's verifier rows are three, the third
being "alignment or slab invariant violated (§16)". So L40 does not fire.

Byte level: no. L40's detector is *verifier*, so no reader obligation moves;
and the situation only arises in a file that already exhibits T10 (or another
structural row), i.e. an already-nonconforming file, where `[R-CNF-12]`
licenses either verdict. No conforming file changes treatment. What moves is
the scope a verifier records and hence `[R-VEC-02]`'s manifest.

### Group 5 — §21.7's unwitnessed-obligation account (writer-03, register-04)

Paragraph verified: it cites `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`/
`[R-SER-01]`, `[R-CNT-13]`, `[R-CNT-18]`, §20.3 step 4's bar, `[R-WRT-06]`'s
four, `[R-ENC-06]`. `[R-LIF-02]` does not appear. §9.2's Note does single out
step 3: "A writer that re-points a new trailer at a prior generation's
directory region has left step 3 unperformed."

I checked writer-03's constructed file. Payloads appended, step 3 skipped,
trailer at generation n+1 with dir_offset = D_n. The new payloads are
unreachable from dir_n, so by §5.2 they are slack, not structures, and
`[R-CNT-05]`/F7 ("A structure occupies bytes between the live directory's end
and the live trailer") does not bite. Bounds, partition, checksums, generation
all hold. The file is conforming. So the omission is real, not merely
rhetorical.

register-04's larger family checks out too: `[R-CNT-08]`'s updater clause
(prior trailer is slack; §9.7 does not reconstruct it), `[R-WRT-05]`,
`[R-WRT-07]`, `[R-WRT-08]`, `[R-WRT-03]`.

Against it: §21.1 calls §21.7 "the account, **by class**, of what fails it",
and the paragraph opens with the class rather than a list. So the paragraph is
defensible as a class account with examples — which is exactly why both
reporters graded OBSERVATION. The defect is that it reads as an enumeration
while enumerating one requirement's four sub-obligations at item level.

Byte level: no. Every member of the class is defined by having no witness in
one file's bytes; `[R-CNF-02]` makes file conformance "a pure predicate on
bytes", identical either way.

### Group 6 — Appendix G's closing enumeration omits the filter (writer-04)

Walked the ten items against the closing paragraph:
1 → "the producer pinning of items 1 and 9"; 2 → "a derived `file_id`";
3 → "gap *content*", "gap *extent*", "record and sub-record order";
4 → "a single generation"; 5a → "the absence or fixing of a declared alignment
and slab"; **5b (fixed filter) → nothing**; 6 → "the sentinel for every
all-fill tile"; 7 → "the fill a writer records when its caller chooses none";
8a → "`version_minor` at its floor"; 8b (flags = 0) → not named, correctly, as
§6.3 already makes it mandatory ("a writer creating a file under this text
MUST write flags = 0"); 9 → producer pinning; 10 → "NFC-normalized names".

So the filter is the one genuine omission, and it is a real freedom:
`[R-COD-09]` lets a writer emit 1 or 2.

What limits the harm, and writer-04 under-weighs it: "Read the numbered items
as the list; this paragraph names what they are for, not how many there are."
"Read the numbered items as the list" disclaims the paragraph's membership as
well as its count. Still an incompleteness worth an edit.

Byte level: no. Appendix G "adds no requirement to any actor: a writer
ignoring it is fully conforming", and `[R-CNF-05]` already licenses divergent
bytes.

### Group 7 — Appendix G item 5 vs §17.3's identity stride (writer-05)

Item 5: the filter "changes the stored bytes of every tile it touches".
`[R-COD-10]`: "for a packed boolean plane s = 1 and the filter is the
identity", and the general transform at s = 1 has i ≡ 0, so offset j → j.
Verified against §14.2's table: this covers every planar plane of a one-byte
channel (B = 1) and every interleaved layer with Q = ΣBᵢ = 1 (one int8/uint8/
bool channel), besides the packed bool plane the rule names outright.

§20.3 step 4 relies on the identity case in *normative* text: "a change that
leaves every one of those tiles' stored bytes meaning exactly what they meant
— a filter whose mandated stride makes it the identity (`[R-COD-10]`)".

So item 5's factual premise is false for a real class of layers. Its
conclusion survives by a mechanism it does not state (the layer record's
filter field byte, 01 vs 02).

writer-05's rejection of the tautological reading is right: the sentence is
offered as the *reason* to pin the filter, and a tautology supports nothing.

Byte level: no. Non-normative appendix; §17.3 and §20.3 agree with each other;
both a commit that changes the filter on a stride-1 layer and one that does
not produce conforming files.

### Group 8 — Appendix G never fixes "the same input" (diagrams-04)

Item 5's test — "§17.3 leaves the choice to the writer, it changes the stored
bytes of every tile it touches, and no content implies it" — is satisfied by
layout: `[R-SER-06]` leaves interleaved/planar to the writer, the choice
changes every tile's image and the layer's entry_count (N vs C·N), and §3.2's
reference array is indifferent to it. §11.3's Note leaves tile extents open in
the same way: "Tile extents are a writer's choice, and this specification
imposes none". No item pins either, and neither is "already mandatory".

Item 2's parenthetical cuts the other way — "two files carrying the same
arrays can legitimately differ in tiling, layout, and codec" — which reads
"input" as including the declared schema. But items 1 and 5 then pin codec and
filter, and item 5's stated reasoning does not distinguish them from layout.
The appendix's opening says only that the profile "closes the degrees of
freedom this format deliberately leaves open"; it never says over what input.

This one needs a maintainer decision (define "input" in the opening, or extend
item 5 to layout and tiling), not just an edit.

Byte level: no. Same appendix disclaimer; `[R-CNF-05]`.

### Group 9 — Gᵢ·Tᵢ and `[R-ENC-04]` in a zero-extent layer (verifier-01) — BYTE-LEVEL

I rebuilt the arithmetic. rank 2; E₀ = 0, T₀ = 1 → G₀ = 0; E₁ = 2⁶³−1
(in domain, `[R-ENC-03]` is inclusive), T₁ = 2 → G₁ = ⌈(2⁶³−1)/2⌉ = 2⁶².
G₁·T₁ = 2⁶³, exceeding the ceiling by exactly 1. Every other quantity is in
domain: N = 0, P = 2, N·P = 0, C·N = 0, P·Q = 2, entry_count = 0, index-region
length 0, extent slot (0,0), crc_of_crc_array = 0. `[R-GEO-02]` obliges
acceptance of a zero-extent layer; L21, L22, L27 all hold; `[R-COD-07]`'s cap
is not engaged (codec 1); §21.9's decoded-tile row does not bind.

For the broad reading (reject):
- §11.2, normative: "These products, like **all geometry arithmetic**, are
  subject to `[R-ENC-04]`: a reader MUST treat a product exceeding 2⁶³ − 1 as
  a validity error at layer scope."
- §19.3, normative: a reader's first access validates "the 2⁶³ − 1 ceiling on
  **every quantity that arithmetic derives** (`[R-ENC-04]`)".
- §17.2's Note: "`[R-ENC-04]`'s overflow rule carries no such quantifier — it
  binds **any sum or product a file yields** — so P·Q and P·Bᶜ are checked in
  an empty layer even though this cap is not."

For the narrow reading (accept):
- `[R-ENC-04]` itself: "any quantity **this specification defines** as a sum or
  product of integers obtained from a file (offsets plus lengths, grid counts,
  tile counts, sample-position counts, ordinals)". §11.3 writes Gᵢ·Tᵢ inside a
  comparison ("Where Gᵢ · Tᵢ > Eᵢ") and never defines it as a quantity; it is
  in none of the five named classes unless "sample-position counts" is
  stretched to cover a padded axis length.
- L2's instance cell enumerates the derived products exhaustively —
  "N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ; N·P; C·N …; P·Q …; P·Bᶜ; entry_count × 20 + …" — and
  omits Gᵢ·Tᵢ.

§21.1 ("where a row and the rule it cites diverge, the rule governs") weakens
the L2 leg but does not touch the `[R-ENC-04]` leg, which is the one that
matters: the rule's own quantifier is "any quantity this specification
defines", and a careful reader can hold that Gᵢ·Tᵢ is not one.

The readings coincide on every layer with all extents nonzero, since
N·P = ∏(Gⱼ·Tⱼ) with every factor ≥ 1 dominates each Gᵢ·Tᵢ and L2's N·P
instance catches it. They separate only at N = 0. So this is not a general
divergence — it is a divergence on exactly the constructible file above.

I am upholding this as byte-level. Two carefully-reasoning implementations
reach opposite accept/reject verdicts on a file that can be built, and
correspondingly `[R-CNF-05]` permits a writer to emit it under one reading and
forbids it under the other. The reporter picked the *narrow* reading, which is
itself evidence the text does not decide it plainly; I lean the other way on
the merits and that is exactly why it must be written down rather than left to
the reader's lean.

Repair, either direction: (i) add Gᵢ·Tᵢ to L2's instance cell and say so in
§11.3 — costs one instance against §21.8's 277 and one vector; or (ii) say in
§11.3 that Gᵢ·Tᵢ is evaluated only for a layer that addresses a tile, leaving
the counts alone. The maintainer picks.

### Group 10 — §5.2's partial slack total (verifier-02)

> A partial total is F less the bytes claimed by the claimants the walk did
> enumerate — an upper bound on the file's true slack, never an under-count

Reading A (sum of lengths) gives a negative number on verifier-02's F33 file
(704 − 1119 = −415), which the same sentence forbids. Reading B (union) is
provably an upper bound. The appositive is what decides it, so the document
does settle the question — but it settles it by a property clause rather than
by the formula, and the formula is the half an implementer codes.

Verified that the discard clause does not reach the case: §5.2 discards
enumerated claimants only "where the rejection is one the walk itself
established, L18's overlap or L40 through L42's placement among them", all
layer-scope. F33 is reject-file and is not discarded.

Byte level: no. A partial total arises only where the walk stopped, which
requires a violation, so only ever on a nonconforming file; `[R-CNF-12]`
already fixes the verdict.

Repair: say "the union of the byte ranges claimed by the claimants the walk
did enumerate".

### Group 11 — Appendix A's "local reader" (diagrams-01)

The reporter's quotation stops mid-sentence. The full passage:

> A local reader additionally verifies bytes [0, 16) by equality first, which
> `[R-CNT-04]` requires of any reader holding them — as a remote reader does
> too whenever its speculative suffix window reaches offset 0 … A shorter
> window can still spare the second request: 112 bytes covering [16, 128)
> contains the directory, so §6.4's containment test applies, while bytes
> [0, 16) stay non-resident, so §6.1 leaves the front-block check to the
> reader.

The relative clause names the residency test in the same sentence, and the
next sentence works the non-resident case explicitly. So Appendix A does not
"key the check to locality" against §6.1's "The test is residency, not
transport" — it uses "a local reader" as a loose stand-in for a reader that
holds the bytes. That is worth tightening, but the contradiction the reporter
alleges does not stand. PARTIAL.

Byte level: no. Non-normative appendix; the over-stated duty is verification;
a file failing the comparison is F6 and nonconforming anyway.

### Group 12 — §21.2's italicised "geometry" (register-01)

grep 'geometr' = 18 hits, verified. Line 3425 is the only one whose subject is
a *file's* geometry; every other means a layer's dimensional declarations
(§11.1's title, §11.2's "all geometry arithmetic", `[R-CNT-17]`'s
"geometry-derived addressed-tile count", §19.3, §20.3, L32).

Under the house sense the clause excludes no row of a file-scope table, and
the following sentence — "Four rows are outside that reasoning and do reach it"
— becomes incoherent. So context decides for the loose sense. register-01's
arithmetic is slightly off (36 = 4 + F18 + 31, not 32 + 4), but the
disambiguating force of the next sentence is what it says it is.

Byte level: no. §2.3 fixes the outcome for a foreign-major file independently
("neither conforming nor nonconforming under it"), and §21.1 gives the rule
priority over the row.

### Group 13 — two senses of F inside §21.2 (register-02)

Both senses verified. Committed: §5.1 "The file size of a conforming file
equals the live trailer's committed file length F"; §6.2's table
"committed_file_length … = F"; §15.3 "with F the committed file length".
Transport: §6.4 and §19.1 step 1 "Obtain the transport-authoritative file size
F". F5's cell glosses "F (physical file size)"; F10 and F32 restate
`[R-CNT-06]`/`[R-CNT-13]` bounds, which are stated against the committed
length.

One correction to the reporter: F5's parenthetical is *local disambiguation*,
not a table-wide definition, which weakens the claim that a corpus author
would carry it into F10 and F32. The underlying observation — F carries two
senses and only one row glosses it — stands.

Byte level: no. Any file on which the senses diverge fails F17, which §6.2
validates in the same batch: "committed_file_length equals the file size …
Any failure is reject-file."

### Group 14 — L23's Detected cell (register-03)

§19.1 step 4 does place the name-field containment determination at the open:
"a layer record whose name field does not lie entirely within that record's
inline_length yields no name field to compare, so it contributes no name to
the namespace and is instead a validity error at layer scope (`[R-CNT-18]`)".
L23's Detected cell says layer access, and its first instance is "leading
fixed fields (name … C)". Note L3, L5, L6 — the other layer-record-name
rows — are Detected: *open*, so the register is not uniform here.

What decides it: §19.2's Rationale — "The rule fixes the *latest* detection
point" — and "A reader MAY detect any violation earlier (`[R-CNF-12]`)". So
the cell is a deadline and reading (a) is right; the observation is that for
this sub-case the deadline is later than the point §19.1 requires the
determination anyway, and later than its three siblings.

Byte level: no. reject-layer under both, F4 already excludes such a record
from the duplicate test ("both obtainable within their records' inline_length").

### Group 15 — `[R-COD-04]` and sentinel entries (adversary-01) — DOWNGRADED

The reporter is right that `[R-COD-04]` carries no "(non-sentinel)" qualifier
where §15.3's structural rows and T1, T8–T12, T14 all do. That is a real
editorial inconsistency.

The reporter is wrong that the reading is live. Three texts decide it:

1. `[R-IDX-02]`: "**Sentinel entries are a reserved pattern, not offsets or
   lengths**: `[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule
   apply to the fields of non-sentinel entries only." The reporter treats the
   clause after the colon as a closed exemption pair. But the clause *before*
   the colon is the general statement, and it is what removes `[R-COD-04]`'s
   subject: "the index entry's length" is not a length in a sentinel entry.
2. §15.3's first row: "offset = S ∧ length = S ∧ crc = 0 | **valid sentinel —
   reads as fill**". The classification a reader MUST make is a positive one
   with a prescribed outcome, not a pass-through to a further length test.
3. `[R-TYP-08]` (§13.3): "For every addressed tile that is not stored in the
   live generation — its index entry is the sentinel (§15.2) — a reader …
   MUST return, for each channel the tile carries, that channel's fill value
   at every such position." Under the reporter's reading (a) this MUST would
   be unreachable for every sparse codec-1 layer, and `[R-TYP-09]` would then
   forbid the fill `[R-TYP-08]` commands.

And the document instantiates the combination as ordinary: §7.4's worked layer
record is codec 1, entry_count = 4, "With no tile stored, every index entry is
the sentinel (§15.2)". Under reading (a) the specification's own worked example
is a layer all of whose tiles a reader must reject.

**The premise my downgrade rests on**, stated so it can be attacked: that
`[R-IDX-02]`'s "not offsets or lengths" is a general statement about what the
sentinel's twenty bytes *are*, and not merely a preamble to the two-rule
exemption after its colon. Attack it by arguing expressio unius — the sentence
names two rules and `[R-COD-04]` is not among them. My answer is that reading
(a) makes `[R-TYP-08]` unsatisfiable across the format's whole sparse case and
makes §7.4's example nonconforming, and a reading that does that is not one the
words permit.

Grade PARTIAL: real defect, wrong severity. Repair: write "(non-sentinel)"
into `[R-COD-04]`, matching T14 and §15.3.

### Group 16 — commits that change C or d (writer-06)

Verified: nothing in §20.3 (or §20.1's tier list, which names "adding layers or
records, superseding tiles, growing extents, amending metadata") says whether a
commit may change channel count or rank. The worked permissions are all about
extents.

The carve-out, though, is general in its main clause: "Dropping a tile out of
the addressed set (§11.2's grid count falls) is not itself such an alteration —
a tile the new state does not address carries no §14 obligation and its extent
becomes slack". A planar channel drop drops tiles out of the addressed set, and
the stated reason applies verbatim; the parenthetical reads to me as naming the
ordinary mechanism, not restricting the clause. And the shrink paragraph closes
it: "What counts as such an alteration is the bar above and nothing else, its
carve-out included."

So reading (A) is better supported than writer-06 allows — the extension of the
carve-out is in its own main clause, not something the reader must supply. What
survives is the gap: the section's permission set is stated over extents only,
and the one operation that separates entry_count from its factors (grow an
extent and drop a planar channel in one commit, C·N held constant while every
ordinal moves) is described nowhere.

Byte level: no, but the reasoning needs care. Under reading (B) an updater
must refuse an operation reading (A) permits — so the *operation* set forks.
The *file* does not: §21.7 records that "a commit that supersedes every tile it
would have damaged leaves the live state clean, so the bar is unwitnessed
there", and de-addressed tiles leave the live state, so the output is a
conforming file under both readings and the same bytes are emittable by a
creator in one commit regardless. No reader accepts or rejects differently.

Severity: design-decision — the repair is a maintainer's call about whether to
state a channel-set/rank permission or to leave it to the bar.

### Group 17 — §9.6's rejected-candidate count (quiz-01)

> probe backward at 64-aligned offsets o for the trailer magic; on a match,
> require the trailer CRC to verify and committed_file_length = o + 64. The
> nearest-to-end **valid** candidate is the last committed state
> … MUST report the candidate it settled on and how many it rejected.

"valid candidate" presupposes invalid ones, which supports counting CRC and
length failures as rejections; the closing sentence's grammatical subject is
"a candidate whose whole-file re-verification fails", which supports the
narrow count. Genuinely open, and it is a MUST-report, so two tools can
report different numbers for one file.

Byte level: no. §9.6: "no verdict turns on the probe", and recovery output
"MUST be re-verified as a whole file (§8) before being trusted". The candidate
settled on — the thing that decides recovered bytes — is fixed by requirements
this sentence leaves alone.

## Tally

Byte-level upheld: 1 of 25 (verifier-01). Reporters self-flagged 2
(verifier-01, adversary-01).
