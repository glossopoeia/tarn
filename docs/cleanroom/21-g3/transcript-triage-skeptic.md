# Round 21 triage — SKEPTIC pass — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (4377 lines), in
  seven `sed` chunks: 1–400, 400–900, 900–1400, 1400–1900, 1900–2400, 2400–2900,
  2900–3120, 3120–3330, 3355–3450, 3450–3560, 3560–3720, 3720–3900, 3900–3992,
  4151–4377 (Appendices F, G, H), plus a targeted read of §24's `[R-VEC-02]` /
  `[R-VEC-04]`.
- No walk transcripts opened. No `transcript-triage-*.md` opened; I did `ls` the
  round21 directory once before I had read the charter's prohibition closely — the
  listing showed six named walk transcripts and three quiz transcripts and **no**
  `transcript-triage-*` files existed at that moment, so nothing of another pass was
  disclosed to me. I opened none of them.
- No `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git
  history, or web.

## Method

For each finding: (1) locate the quoted text in `tarn.md` and confirm the quotation
is not selective; (2) hunt for a *different* sentence that forecloses the reading the
reporter says is open; (3) if found, quote it and downgrade; if not found, say so and
grade up. I state the premise every downgrade rests on.

Dedup: I looked hard for merges and found none. The four §18.2/`[R-MTA-09]` findings
(verifier-02, adversary-01, quiz-01, quiz-03) and writer-03 all sit in the same
neighbourhood but name five different sentences with five different repairs. The two
§2.3/MU=1 findings (diagrams-01, quiz-02) are opposite defects — a summary too narrow
vs. a rule too broad — in different sections. So: 21 findings, 21 groups.

---

## writer-01 — §21.9's per-tile guarantee over a layer that addresses no tile

**BYTE-LEVEL, CONFIRMED. This is the one I tried hardest to kill and could not.**

Premise check first (the round-16 failure mode is inherited premises). The reporter's
file: one dimension, E = 0, T = 2^31, one uint8 channel, interleaved.
- `[R-GEO-01]`: T ≥ 1 — satisfied. `[R-ENC-03]`: T ≤ 2^63−1 — satisfied.
- §11.1: "at Eᵢ = 0 the grid count is 0 and the layer addresses no tile". N = 0.
- §11.2: "its **sample-position count per tile** is P = ∏ Tᵢ" — P = 2^31, defined for
  the *layer*, not per stored tile.
- §14.2 table: interleaved decoded size = P·Q, Q = 1 → 2^31 bytes = 2048 MiB.
- §19.3 `[R-RDR-03]` obliges the reader to derive it at layer access: "and on the
  decoded sizes §14 derives from it (`[R-SER-02]`, `[R-SER-07]`)".
- §17.2's Note confirms the derivation happens in an empty layer: "P·Q and P·Bᶜ are
  checked in an empty layer even though this cap is not."

Premise holds. 2048 MiB is a quantity a conforming reader computes on this file.

Now the kill attempts.

1. §3.1: "**tile** — the unit a tile-index entry addresses". With entry_count = 0
   nothing is addressed, so the layer has no tile, so "decoded size of one tile"
   names no quantity of this file. → Reading A.
2. `[R-GEO-02]`: "Readers MUST accept such a layer, and a read of any region of it
   returns no samples." → Reading A.
3. §21.6 row: "A dimension has extent 0 | A valid, empty layer …" under the header
   "A reader that treats any of them as a failure is the nonconforming party."
   → Reading A, but weakly: `[R-ERR-04]` expressly separates a resource refusal from a
   validity error ("MUST be reported as a resource limit and not as a validity
   error"), so a resource decline is not "treating it as a failure".

Against those, the text that keeps Reading B alive:

> "A file exceeding any of these remains conforming, and a reader MAY decline it — at
> the whole file, or at **the narrowest scope whose declarations exceed what it can
> serve**, a layer or a tile." — §21.9 `[R-ERR-04]`

*Declarations*, not tiles. This layer's declarations do derive 2048 MiB, and §17.2's
Note establishes in terms that the document treats P·Q as a live derived quantity in
an empty layer. `[R-CNF-03]`'s "none of whose values exceeds the minimum guarantees"
does not separate them either, since the table's rows are themselves derived
quantities.

So the document takes an explicit position on the quantifier for two members of this
family — `[R-COD-07]` ("quantified over the layer's *addressed* tiles, so a layer that
addresses none … satisfies it") and `[R-ENC-04]` ("carries no such quantifier — it
binds any sum or product a file yields") — in one Note, in one breath, and says
nothing about the third. That silence, in a document this deliberate about exactly
this quantifier, is evidence, and I could not find the sentence that closes it.

The fork is a must-accept fork on a specific byte sequence: under A a reader that
declines this layer on resource grounds "declines on that ground a file whose every
quantity lies within the table" and **is not a conforming reader**; under B it is.
Two readers, same bytes, opposite verdicts at layer scope, and `[R-ERR-04]`'s last
sentence makes exactly one of them conforming without saying which.

Scope note the reporter overstates: §20.3 does *not* trap the writer forever — "A
layer that stores no tile **in the generation this commit supersedes** MAY be
re-declared freely." The divergence lives only while the layer is empty. That narrows
the blast radius; it does not close the fork.

**Repair:** state the quantifier for the "decoded size of one tile" row as §17.2's
Note states `[R-COD-07]`'s — one clause in §21.9 saying whether the row ranges over
addressed tiles or over the layer's declaration-derived per-tile size.

---

## writer-02 — Appendix G leaves tile extents and channel layout unpinned

CONFIRMED, not byte-level.

Verified item by item: items 1–10 pin codec/encoder, file_id, emission order,
generation count, alignment+slab+filter, all-fill sentinel, fill default,
version_minor+flags, metadata producer, NFC names. Neither tile extents nor the
layout byte appears anywhere.

Kill attempt: the closing paragraph's "Read the numbered items as the list; this
paragraph names what they are for, not how many there are" — this defends the closing
*inventory*, not the items. And §11.3's Note is explicit that tile extents are exactly
the class of freedom item 5 exists for: "Tile extents are a writer's choice, and this
specification imposes none". §14.4's Note gives the layout case in bytes: "A single-
channel bool layer does not — ⌈P/8⌉ packed bytes planar versus P bytes interleaved —
and both forms are valid". No foreclosure found.

Not byte-level: Appendix G is "(non-normative)" and "adds no requirement to any actor:
a writer ignoring it is fully conforming." Both tilings and both layouts are already
conforming under `[R-CNF-05]`.

**Repair:** add tile extents and channel layout to item 5, or state expressly that the
profile takes tiling and layout as part of its input.

---

## writer-03 — §21.5's signpost to §21.6 for the bound-decline

CONFIRMED, not byte-level.

Checked §21.6's table: exactly two ignore-record non-violations (experimental-range
MU = 0 record type; experimental-range document encoding) and, in prose, exactly two
"conforming files a reader nevertheless refuses" (foreign major; experimental
top-level MU = 1). The bound-decline is in none of them. §21.5's own closing sentence
— "§21.6 lists the ignore-record conditions that are not violations." — reads as a
definite description and is therefore incomplete.

Kill attempt: §21.1 exempts §21.6 from completeness — "neither this completeness
clause nor the instance arithmetic below reaches §21.6's defined non-violations". That
kills any claim that the *omission* is a register defect; the reporter already
conceded this and located the defect in §21.5's sentence instead. I found nothing
that repairs that sentence.

Not byte-level: `[R-ERR-04]` licenses the decline whether or not §21.6 lists it, and
what moves is the diagnostic class, which alters no byte and no accept/reject verdict.

**Repair:** soften §21.5's closing sentence, or add the bound-decline to §21.6's
closing prose beside the two capability refusals it already names.

---

## verifier-01 — `[R-CNT-21]`'s partial-total rule and F33/F7

**REFUTED.** The lead clause is the operative test and it is quotable:

> "**Where the walk of §9.7 does not enumerate every region's claimants** — whether
> because a scope-level rejection ends that scope's enumeration (…) or because the
> verifier elected under `[R-CNF-11]` to stop at the first violation — the verifier
> MUST report the total as partial." — §5.2 `[R-CNT-21]`

A verifier cannot *establish* F33 (two claimants on one byte) or F7 (a structure in
the pre-trailer gap) without having enumerated the claimants; the antecedent is
therefore false and no partial label is owed. §9.7 says the same: "Where the walk does
not complete — a scope-level rejection **blocks** enumeration, or the verifier stops at
the first violation" — a rejection the walk itself established blocks nothing. And a
verifier that *does* stop on F33 is already covered by the second branch, which
requires the partial label and requires it to "say which scope or violation stopped
the walk" — reading (C)'s report line, obtained without any edit. §5.2's Note closes
it: "A partial total (`[R-CNT-21]`) reports what one verifier's **incomplete** walk
left unclaimed".

Readings (B) and (C) are not open. No change needed.

---

## verifier-02 — `[R-MTA-09]`'s verifier SHOULD states no consequence

CONFIRMED, not byte-level.

Read the sentence in place: "… and it fixes the file's verdict as *cannot establish*
only where the verifier established no violation elsewhere; the verifier SHOULD report
the bound it applied and the stored length of the extent it declined." The sentence
ends there; the next changes subject to unassigned encodings. No consequence stated,
and no adjacent restatement supplies one — unlike `[R-SLB-01]`/`[R-SLB-03]`, which
lean on `[R-CNT-03]`.

Kill attempt: `[R-CNF-12]`'s "a verifier reports a SHOULD deviation as an advisory
that does not bar certification" is a *general* consequence for every verifier SHOULD;
§2.1's discipline asks what deviation costs, and "does not bar certification" is not a
cost. `[R-MTA-10]` next door does state one, which is what makes the omission visible:
"bytes a certificate covers without inspecting are counted and named, never silent."

Not byte-level, and §2.1's discipline statement is itself a Note (non-normative under
`[R-CNF-01]`), so this is editorial by the document's own accounting.

**Repair:** one clause — without the bound and the extent length an operator with a
*cannot establish* cannot tell how much headroom would resolve it, or which document
was declined.

---

## diagrams-01 — Appendix H's reader checklist omits the MU = 1 carve-out

CONFIRMED, not byte-level.

Verified: §2.3 qualifies three ways; the checklist line keeps one. The case is real —
§21.6's closing paragraph: "`[R-CNT-15]` obliges the reader to reject, and
`[R-CNF-02]` makes the file conforming all the same."

Kill attempt on the behavioural claim succeeds: Appendix H is headed
"(non-normative)" and disclaims itself — "each entry's authority is the requirement or
section cited, never this summary" — and `[R-CNT-15]`'s reject-file is an unqualified
MUST. So no reader could defend serving the file. The checklist line is still wrong as
printed, and a checklist is exactly what gets audited against.

**Repair:** add "carrying no unimplemented MU = 1 top-level record" to the line, or
cite §21.6's closing paragraph beside `[R-ERR-04]`.

---

## diagrams-02 — `[R-CNT-27]`'s 128-byte floor and the version gate

PARTIAL, not byte-level. The reporter's ordering observation is right; the ambiguity
is not open, because two normative passages decide it.

> "§6.2 puts the version gate ahead of every check but the trailer magic and the
> trailer CRC, so such a file is refused on capability grounds first. **Four rows are
> outside that reasoning** and do reach it … F8 and F1's trailer-magic instance, F14's
> trailer CRC … and F6 with F1's front-block instance" — §21.2 preamble (normative)

F5 is not among the four. And `[R-CNF-02]` forecloses the verifier-verdict half
outright: "a file declaring another major is neither conforming nor nonconforming
under it … and that refusal is not a finding about its bytes." A verifier reporting
*nonconforming* on a major-2 file contradicts `[R-CNF-02]` directly, so reading (a) is
not available for the verdict; what remains is the reader's diagnostic class, which
`[R-CNT-07]` states as a SHOULD.

Residual defect: the ordering of `[R-CNT-27]` is stated only in §21.2's preamble, a
place an implementer working through §5.1, §6.2 and §19.1 has no reason to be.

**Repair:** name the floor in §6.2's ordered list (after the version gate) or add one
clause to §5.1 saying the floor is a major-1 premise.

---

## diagrams-03 — §4.7's Note promises §7.2 folds each field's range

CONFIRMED, not byte-level, low.

Verified §7.2's five Field cells: ranges appear for `type` and `flags` only;
`inline_length`, `extent_offset`, `extent_length` are bare names.

Kill attempt: "each table giving the columns its structure needs" licenses dropping a
column, not a partial fold; and one could argue the three bare fields' range *is*
`[R-ENC-03]`'s universal 0…2^63−1, which the document does not reprint anywhere. That
argument is available but the Note says "each field's range", and the two neighbouring
halves of the same sentence (§6.1's Value column, §7.4's dropped columns) are
delivered exactly. No foreclosure.

Non-normative Note; all three ranges are stated normatively in `[R-ENC-03]`,
`[R-CNT-12]`, `[R-CNT-13]`, `[R-CNT-18]`.

**Repair:** reword the Note, or fold the three ranges in.

---

## diagrams-04 — §18.2's "Valid values | 1 or 2; see below"

PARTIAL, not byte-level. The cell's own deferral is the foreclosure:

> "| 0 | 1 | u8 | encoding | structural | **1 or 2; see below** |"

"see below" is an explicit deferral, and the prose directly under the table gives the
full three-way partition, as do §10.2's table, §10.3, `[R-EXT-03]`, §17.4's closing
sentence, §21.6's row and `[R-MTA-10]`. So the cell is not narrower than the rule; it
is a pointer. The reporter picked this reading themselves.

Residual: this is genuinely the one field where "valid" and "conforming" come apart,
and §7.4's index_encoding cell shows the document knows how to say so in a cell.

**Repair (optional):** spell the partition in the cell, as §7.4's index_encoding cell
does.

---

## diagrams-05 — §21.6's sentinel row states the fill rule wider than `[R-TYP-08]`

CONFIRMED that the row diverges; harmless, not byte-level. The precedence device is
explicit and quotable:

> "§21.6's entries restate their governing rules on the same terms a row does, and
> where such an entry and the rule it cites diverge, **the rule governs there too**."
> — §21.1

Plus `[R-GEO-04]`'s "a reader MUST NOT return padding positions as samples", §13.3's
Note ("Fill governs unstored tiles. The padding positions of stored edge tiles … are a
different mechanism"), and §19.4 step 4's fully qualified restatement.

**Repair:** tighten the row to `[R-TYP-08]`'s terms — "every sample position inside
the layer's extents reads as fill, for each channel the tile carries".

---

## register-01 — §21.1 states normative rules with no identifier

CONFIRMED, not byte-level.

Verified: no line in §21.1–§21.6 terminates in a backticked identifier; §21.1 ends
"…which is why §14.2 calls it the sole resolved byte in this format." The rules it
states — normative completeness, rule-governs-on-divergence, specialization recording,
instance arithmetic, Detector/Detected semantics — restate nothing else and are
normative under `[R-CNF-01]` (§21.1 is neither §1, nor a Note/Example/Rationale, nor a
non-normative appendix).

Kill attempt: this document's convention is that an identifier *terminates* a run of
paragraphs, not one sentence — §6.1's "Writers MUST emit exactly these 16 bytes."
carries no identifier of its own and is covered by `[R-CNT-04]` several paragraphs
later. So unidentified MUST-bearing prose is not unprecedented here. But §21.1 ends
with *no* identifier at all, so nothing terminates it. `[R-ERR-02]`, cited inside
§21.1, lives in §21.8 and states only the vector-coverage obligation. No foreclosure.

Cost is real and confined to review and corpus: `[R-VEC-02]` requires a manifest to
record "the §21 register row it exercises together with that row's governing
requirement identifier … row labels are positional and renumber when a row is
struck" — a rule stated only in §21.1 has only a prose position to cite.

**Repair — a maintainer decision, not an edit I can pick:** mint `[R-ERR-NN]`
identifiers for §21.1's rules, or state in §2.2 that §21's reading rules are carried
by `[R-ERR-02]`.

---

## register-02 — §21.6 cites `[R-WRT-08]` for "preserved or dropped per its PE bit"

PARTIAL, not byte-level.

`[R-WRT-08]`'s whole text: "An updater MUST NOT re-encode a record whose type it does
not implement, and MUST NOT modify one except by relocating its extent and re-pointing
its slot under §20.5". It does not state preserve-or-drop. §20.4's table does.

Kill attempt — and it half-lands. Under this document's own identifier convention
(identifiers terminate a run of paragraphs; see §6.1/`[R-CNT-04]`), `[R-WRT-08]` is
the first identifier *after* §20.4's table and the "No commit therefore removes a
layer record" paragraph, so its scope arguably reaches back over both. On that reading
the citation is correct and the reporter is wrong. Against it: §2.4 and `[R-CNF-06]`
both reach the table **by section**, never by identifier — "§20.4's table states the
cases", "MUST honor the preservation obligations of §20.4" — which is what an
identifier-bearing table would not need.

So what is actually wrong is upstream of the citation: it is unclear which identifier,
if any, carries §20.4's table. That is register-01's disease in a second place, but a
different sentence and a different repair, so I did not merge them.

Not byte-level: §20.4's table is unambiguous where it stands and normatively reachable
through `[R-CNF-06]`.

**Repair:** add §20.4 to the §21.6 row's Rule cell; separately, settle which
identifier carries §20.4's table.

---

## register-03 — §20.5's "(F36, L25, R1)"

PARTIAL, not byte-level. I think the parenthetical is better than the reporter reads
it, on a sentence the reporter did not use:

> "A reader encountering either treats it as its space's rules require: **a validity
> error at the owning scope for the value sets of §11.4, §12.2, §14.1, §15.1, §17.2,
> and §17.3**; for record types, the MU-bit outcome of `[R-CNT-15]` …; and **for the
> metadata-encoding space of §18.2, ignore-record** under the quarantine" — §10.3
> `[R-EXT-03]`

`[R-EXT-03]` splits the eight spaces in two. In the six layer-declaration spaces
(L31, L33, L34, L36, L43, L45) *both* the reserved and the experimental range reject
the layer, so §10.1's vehicles produce nothing a compactor's output can carry and the
sentence's contrast — "the two … §21.6 makes conforming, the other two reaching such a
file only as … violations" — has no purchase there. The two spaces where an
experimental value *is* conforming, and where a reserved value is therefore the
near-miss neighbour, are record type (F36, L25) and metadata encoding (R1) — exactly
the three rows named.

The reporter's underlying verification (a compactor refuses in every case) is correct
and I re-checked it; their reading of the parenthetical as an inventory is not forced.

**Repair (optional):** "among them", or name the remaining six.

---

## register-04 — §21.1's "— F27 and L48"

**REFUTED.** The mapping is right and the punctuation says so:

> "(`[R-CNT-22]`, whose registered type keeps its fixed semantics**;** and
> `[R-MTA-05]`, whose unsorted document readers process as they find it — F27 and
> L48)."

The semicolon closes the `[R-CNT-22]` conjunct; the em-dash sits inside the
`[R-MTA-05]` conjunct. F27's and L48's Governing rule cells both read `[R-MTA-05]`, and
`[R-CNT-22]`'s rows F28 and L49 are simply not named. Reading (B) requires ignoring
the semicolon *and* not looking the rows up.

**Repair (optional, symmetry only):** name F28 and L49 beside `[R-CNT-22]`.

---

## register-05 — R7 and R8 both register the bare tokens

CONFIRMED, not byte-level. Register bookkeeping.

`[R-MTA-04]`'s bullet makes a document unreadable for a non-finite binary64 value *or*
"any of the bare tokens `NaN`, `Infinity`, or `-Infinity`, **which RFC 8259 does not
admit**". A document carrying a bare `NaN` therefore satisfies R8's "contains a
non-finite number, in any form" and R7's "is not well-formed JSON" simultaneously.

Kill attempt: §21.1's specialization device — "Some rows are strict specializations of
others — F1 of F6 and of F8, F35 of F36, L24 of L25 — and a file exhibiting a
specialization is recorded against the narrower row". This pair is not there, and it
would not fit if it were: R8 is not *strictly* narrower than R7 (1e400 is well-formed
JSON), so it is a partial overlap the device does not reach. No foreclosure.

Not byte-level: both rows carry ignore-record / reader / extent use, so no reader's
treatment of any byte differs, and the file is nonconforming under either.
`[R-VEC-02]`'s fallback ("the entry records every row the file exercises and says
which it was built for") absorbs the corpus cost, which is why this is bookkeeping
rather than a gap.

**Repair:** narrow R8's condition to "a number whose binary64 interpretation is not
finite" and move the bare tokens to R7 explicitly, or name the pair in §21.1's
specialization list. Either way the 273 total needs a re-check.

---

## register-06 — are the 2^62 ceilings derived or chosen?

**REFUTED.** §21.9 states the answer in the sentence the reporter quotes:

> "Most follow from a field's width, an external format, or **the value domain**, and
> the rest from arithmetic over structures a generation cannot omit. **Two do not:**
> the 512 floor on A … and the 255-byte cap on a user-metadata key …" — `[R-ERR-05]`

By naming exactly what is chosen, the sentence asserts that everything else — the
2^62 ceilings included — is derived. And it is derivable: A and A_slab are u64 byte
quantities within §4.2's opening sense, `[R-ENC-03]` caps them at 2^63−1, and the
largest power of two at or below 2^63−1 is 2^62. Reading (B) would make §21.9's own
sentence false, which is not a reading the document leaves open.

Downstream, the reporter's own consistency check holds: an out-of-domain A is an
L39/L29 instance, not L1, because §21.1 records a file against the narrower row, so
the 273 total stands.

**Repair (optional):** one clause in §4.2 or §16.1 naming an alignment as a byte
length within `[R-ENC-03]`'s reach.

---

## adversary-01 — Frame_Content_Size of a metadata document

PARTIAL, **not** byte-level. This is my second-hardest call and the premise below is
the one to attack.

Confirmed the reporter's reading of §18.2: the carried-over frame constraints are a
closed enumeration (magic; no skippable and no second frame; no nonzero dictionary ID;
no content-checksum flag), the tile-size constraints are expressly withdrawn ("The
constraints §17.2 states against a tile's declared decoded size do not apply, because
a document has no declared size"), and R4's Instances cell does not list FCS.
Confirmed too that §18.2 makes the disambiguating move one sentence later *for the
window* — "the reader's capability, **not a failure to decode within the meaning of
R3**" — and does not make it for FCS. That asymmetry is real.

The foreclosing sentence:

> "File conformance is a pure predicate on bytes: **it does not depend on any
> reader**, writer, or environment." — §2.3 `[R-CNF-02]`

R3's "fail to decode under its declared assigned encoding" therefore cannot mean "the
implementer's zstd binding returned an error". The declared encoding is "exactly one
RFC 8878 compressed frame" (§18.2), and RFC 8878 is pinned as a normative reference
for "codec 3 and metadata encoding 2" (Appendix F). So the question has one answer per
byte sequence, whichever way RFC 8878 falls:

- if RFC 8878 makes an FCS-inconsistent frame malformed → the bytes are not one RFC
  8878 frame → R3 (or R4, whose governing rule `[R-MTA-09]` says "exactly one RFC 8878
  compressed frame" and, per §21.1, governs over the Instances cell) → ignore-record,
  nonconforming;
- if RFC 8878 imposes no such constraint → the frame ends at its last block, the bytes
  decode to 100 bytes, no rule is broken → conforming.

Silence in RFC 8878 resolves *toward* conforming; it does not leave the predicate
undetermined. Adversary A's "verifier A" and "verifier B" are therefore not two
defensible readings — one of them is over-strict or under-strict against a pinned
reference, which is an implementation bug, not a spec fork.

**The premise my downgrade rests on, stated so it can be attacked:** that "fail to
decode under its declared assigned encoding" is a property of RFC 8878, not of a
binding, and that `[R-CNF-02]` forces that reading. Attack it by arguing that a
pinned format whose decode semantics are themselves underdetermined makes the
predicate ill-defined rather than reader-independent — in which case `[R-CNF-02]`
manufactures nothing and the fork is real.

I could not consult RFC 8878 under this round's access rule and I am not asserting
what it says. Note one piece of *internal* evidence the reporter surfaced and I
credit: `[R-COD-06]` pins the tile FCS constraint itself and §21.4 registers it as T22
separately from T25 ("malformed stream that fails to decode"), and §21.1's
specialization list does not name T22 as a specialization of T25 — which is evidence
the drafters did not believe RFC 8878 already rejects an inconsistent FCS. If that is
right the document should say so for documents too.

**Repair:** the maintainer should check RFC 8878. If it makes an inconsistent FCS
malformed, one clarifying clause suffices. If it does not, make the same move §18.2
already makes for the window — "a Frame_Content_Size inconsistent with the document's
actual decoded length is / is not a failure to decode within the meaning of R3" — and
adjust R4's Instances cell either way.

---

## adversary-02 — §16.1's "every stored tile" and structurally-bad entries

CONFIRMED as an asymmetry; foreclosed on behaviour, not byte-level. The deciding
sentence is in §15.3 and it is general, not an example:

> "Such an entry contributes no stored extent to the *verifier* rows, **which bind
> over well-formed entries' extents only** — `[R-SLB-03]`'s run continuity closes over
> it as it does over a sentinel — and none to `[R-LIF-08]`'s coverage walk"
> — §15.3 `[R-IDX-03]`

§15.3's verifier rows include "alignment or slab invariant violated (§16)". So an
entry with offset 5 contributes no extent to L40 and the damage stays at reject-tile;
verifier B is wrong, not differently-right.

The reporter's actual complaint survives that: §16.2 answers the identical question in
the open ("So are the entries §15.3 classifies reject-tile on a *structural* ground:
they address no usable extent, and the run's stored tiles close over them"), L41's
Condition cell restates it a third time, and §16.1 with L40 say nothing — an
asymmetry a careful reader reads as meaning the opposite.

**Repair:** the reporter's own suggested clause, in §16.1 or in L40's Condition cell,
mirroring what L41 already carries.

---

## quiz-01 — "the bound above"

PARTIAL, not byte-level. The phrase is loose in place; the document decides it twice
elsewhere.

> "except where a reader or verifier declines the decode **on the size bound or on the
> frame's declared window**, which `[R-MTA-09]` makes that actor's capability and not a
> fact about the file" — §21.5 preamble (normative)

> "… or when it declines to decode a user-metadata document (`[R-MTA-09]`)" — §2.3
> `[R-CNF-11]`, unqualified, covering both grounds

`[R-CNF-11]` independently fixes any capability-ground inability as *cannot establish*,
so all three of the reporter's readings converge.

**Repair:** "either bound above".

---

## quiz-02 — §2.3's acceptance duty and layer sub-records

PARTIAL, not byte-level. The literal over-breadth is real; the ambiguity is closed by
§2.3's own cross-reference and by `[R-CNT-18]`.

> "The qualifier is load-bearing — the same type as a layer sub-record is reject-layer
> and **never a ground to refuse the file** (`[R-CNT-18]`), so only the top-level case
> is a file a reader refuses." — §21.6 closing paragraph

§2.3 points there itself ("§21.6's closing paragraph names the other two"), and
`[R-CNT-18]`'s "where the file is otherwise conforming a reader MUST NOT reject the
file for it" is an independent prohibition a withdrawn duty cannot license around.

**Repair:** insert "top-level" into §2.3's qualifier.

---

## quiz-03 — ignore-record vs whole-file decline for an oversized document

PARTIAL, not byte-level. Both behaviours are normatively permitted without recourse to
the Note.

> "A file exceeding any of these remains conforming, and a reader **MAY** decline it —
> at the whole file, …" — §21.9 `[R-ERR-04]`

Any document exceeding a reader's own bound necessarily exceeds §21.9's 16 MiB
guarantee (the bound is "no smaller than" it), so `[R-ERR-04]` always applies here. And
`[R-CNF-04]`'s obligation to "apply the outcome class this specification assigns" runs
to *violations*; this file is conforming, so nothing converts the keywordless "is
ignore-record" into a bar on declining. §2.1's casing rule ("when, and only when, they
appear in all capitals") completes it. The Note is confirmatory, not load-bearing.

The reporter's vector worry is foreclosed too: §21.1 — "neither this completeness
clause nor the instance arithmetic below reaches §21.6's defined non-violations …
or §21.9's limits."

**Repair (optional):** promote the Note's reconciling sentence into the normative text
of §18.2.

---

## Coverage

21 input ids; 21 groups; each id in exactly one group; no duplicates. Counted twice
against the charter's id list.

Byte-level survivors: 1 (writer-01).
Tried hardest to kill and failed: **writer-01** (upheld) and **adversary-01**
(downgraded, but only on a premise about an external reference I could not check —
flagged as such).
