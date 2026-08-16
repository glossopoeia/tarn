# Round 9 triage — implementer-consequence lens

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, lines 1–3892, complete,
  in five `Read` calls (1–400, 400–850, 850–1250, 1250–1650, 1650–2070,
  2070–2500, 2500–2920, 2920–3320, 3320–3892).
- `wc -l` on the spec and `ls` on the round-9 scratchpad directory. I read
  **none** of the round-9 reporter transcripts — every claim below is checked
  against the document text, not against a reporter's account of it.
- I did not read `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
  `spec/registry.json`, git history, or the web.

## Method

For each finding: locate the cited text, read it and its neighbours, then ask
the implementer question — *name the byte an implementation emits differently,
the file it accepts that another rejects, or the branch it never writes*. Where
I downgrade a reporter's byte-level flag I quote the sentence that decides it.

---

## Groups

### A. `appendix-g-gap-content-unclosed` — reader-01, writer-02, quiz-01

Appendix G's closing paragraph names gap *content* first among "Four things"
the items add. I read all nine items. Item 3 gives extent
("Each structure begins where the previous one ended, save where a declared
alignment forces a gap: order alone does not fix bytes while the space between
structures is free" — that clause *declines* content). Item 5 removes
alignment gaps. Items 1, 2, 4, 6, 7, 8, 9 are codec, file_id, generation count,
all-fill sentinel, default fill, version_minor/flags, JSON writer. **No item
constrains gap bytes.**

The gap is unavoidable. `[R-LIF-02]` step 5: "append the pad to the next
64-byte boundary — zeroed by advice, `[R-CNT-03]`". §6.2: "this specification
does not constrain their content". §5.2 `[R-CNT-03]` is a SHOULD. Appendix A's
own 128-byte file carries a 44-byte pad at [20, 64).

So two writers implementing items 1–9 to the letter emit files differing in up
to 63 bytes, and — because item 2 hashes over [0, F−64) — in file_id and the
trailer CRC as well. The profile fails at its stated purpose on every file whose
directory does not land 64-aligned.

Item 7's phrasing is the tell that the drafter knows how to promote a SHOULD:
"`[R-TYP-10]`'s SHOULD, taken as a requirement here." Item 3 performs no such
promotion for `[R-CNT-03]`.

**Byte-level: no.** Deciding text, Appendix G's own preamble: "It adds no
requirement to any actor: a writer ignoring it is fully conforming." And §5.2
`[R-CNT-21]`: slack "content is unconstrained, and no conformance requirement
applies to it." Both pad contents yield conforming files every reader must
accept identically. What is falsified is the appendix's claim about itself.

**Severity: design-decision.** The maintainer must choose: add a tenth item (or
extend item 3) promoting `[R-CNT-03]` to a requirement inside the profile, or
strike gap content from the closing four and state that the profile does not
deliver byte-identity for files whose directory does not end 64-aligned.

writer-02 carries a second claim in the same sentence — that "Everything else
the profile needs is already mandatory" is untrue of §18.2's user-metadata
`encoding` field (1 = none, 2 = zstd), which item 9 does not pin. Checked and
correct: item 9 pins the JSON serializer, not the encoding choice, and encoding
2's zstd encoder is unpinned. Folded into this group's repair; it is the same
sentence and the same fix.

---

### B. `appendix-g-four-things-undercount` — verifier-06, register-09

Same sentence, different defect: the closing paragraph is written as an
exhaustive audit and undercounts the freedoms the items close.

- **Item 6** ("The sentinel for every all-fill tile"). Nothing in the core
  requires it. `[R-IDX-02]` and `[R-TYP-08]` govern what an unstored tile
  *reads as*, never which tiles must be unstored. Storing an all-fill tile is
  fully conforming. Independent freedom, not among the four.
- **Item 8** ("`version_minor` at the floor `[R-CNT-26]` states"). `[R-CNT-26]`
  is "A writer SHOULD emit the lowest version_minor that defines every feature
  present in the file" — the same SHOULD category as `[R-TYP-10]`, which *is*
  among the four. The `flags` = 0 half is genuinely mandatory under §6.3.
- **Item 3's top-level record order.** The four name only "sub-record order
  within a layer record's inline payload". `[R-CNT-14]` leaves the directory's
  record order free too ("Record semantics MUST NOT depend on record order"),
  and item 3 pins it: "Records are ordered by type, and within type 0x0001 by
  layer name."

So an auditor looking for four additions finds at least seven.

**Byte-level: no** — same quote as group A ("It adds no requirement to any
actor"). **Severity: editorial.** Rewrite the closing paragraph to enumerate
what the items actually close, or drop the count.

Kept separate from group A because the repairs are different and independent:
A adds a missing constraint, B corrects an inaccurate tally.

---

### C. `appendix-g-file-id-hash-unpinned` — reader-02, writer-04, verifier-05

Item 2: "`file_id` from a cryptographic hash of the file's own emitted bytes,
computed over [0, F − 64) together with the trailer's other fields with the
`file_id` field taken as zero, then written in. Deterministic…"

Four things an adopter must invent, and all three reporters found the same four:

1. **Which hash.** "a cryptographic hash" names none. Items 1 and 9 close their
   freedom by pinning a named implementation at a named version; item 2 does not.
2. **Digest → u64.** file_id is a `u64` (§6.2). First eight bytes, last eight,
   which byte order — unstated.
3. **The exact byte string.** "the trailer's other fields" does not say which,
   in what order, in what encoding. The trailer CRC at [60, 64) covers [0, 60),
   which contains file_id, so including it is circular and it must be excluded —
   which the text does not say.
4. **A zero digest.** §6.2 requires file_id ≠ 0. The procedure has an output the
   format forbids and offers no fallback.

Item 1's own boundary claim is falsified by this: "Byte-identity across
*implementations* is therefore unattainable for codecs 2–4; codec 1 is
reproducible by anyone." With item 2's hash unpinned (and group A's pad
unpinned), nobody reproduces a codec-1 file.

**Byte-level: no.** Deciding text: Appendix G — "It adds no requirement to any
actor: a writer ignoring it is fully conforming"; §6.2's trailer table —
`file_id | semantic | ≠ 0`. Every hash choice yields an equally conforming
trailer that every reader accepts identically.

**Severity: design-decision.** Name a hash and a truncation (e.g. SHA-256,
first eight bytes little-endian), state the serialization explicitly
(bytes [0, F−64) ‖ trailer[0, 48) ‖ eight zero bytes ‖ trailer[56, 60)), and
give a fallback for a zero result — or concede, as items 1 and 9 do, that item
2 pins the producer rather than the output.

---

### D. `appendix-g-emission-order-underdetermined` — writer-03

Item 3: "For each layer in ascending layer-name byte order: its stored tiles in
disk-ordinal order, then its tile-index region; then any record extents in
ascending record order; then the directory. Records are ordered by type, and
within type 0x0001 by layer name; a layer record's sub-records are ordered by
type, and within a type by their order of creation".

Two readings, both defensible:

(a) The per-layer loop ends at "its tile-index region", so "then any record
extents in ascending record order" is one pass after all layers. But "ascending
record order" is defined only as "by type, and within type 0x0001 by layer
name", which does **not** order two different layers' type-0x0002 *sub*-record
extents against each other — sub-record order is defined only within one layer
record. Two layers `a` and `b`, each with a metadata sub-record: their two
extents may be emitted in either order.

(b) "then any record extents" sits inside the per-layer loop — which fixes (a)
but leaves the top-level user-metadata extent with no position at all, and puts
"then the directory" inside the loop, which is impossible.

Second soft spot in the same sentence: sub-records ordered "within a type by
their order of creation" is a function of the producing application's history,
not of the input, so it cannot close the freedom the closing paragraph credits
it with closing. And in format major 1 it is vacuous — `[R-CNT-14]` permits at
most one user-metadata sub-record per layer, and no other sub-record type
exists.

**Byte-level: no** — Appendix G is non-normative, and §5.2's coverage classes
plus `[R-CNT-13]`'s disjointness admit either placement as conforming.
**Severity: design-decision** — a tie-break must be chosen (order sub-record
extents by their owning layer's name, the criterion item 3 uses everywhere
else) and item 3 must place the top-level extent explicitly.

---

### E. `f1-version-major-instance` — reader-03, register-01, adversary-01 — **BYTE-LEVEL**

F1 as written (§21.2):

> | F1 | A multi-byte field is stored big-endian rather than little-endian,
> detectable only through that field's own value or range gate | trailer
> version_major; dir_offset; dir_length; committed_file_length; generation |
> reader | open | `[R-ENC-01]` (R-CNT-07) |

I enumerated the constructible cases for the version_major instance myself.
`version_major` is a `u16` whose only invalid value is 0 (§6.2's table, F20).
Byte-swapping 0 gives 0 — a fixed point — so the one value with a validity gate
is unobservable under byte reversal. Little-endian 1 is `01 00`; written
big-endian it is `00 01`, which the fixed parse reads as 256. There is no
big-endian version_major that trips a validity gate. The only distinguishable
file this instance can produce is a trailer declaring a major other than 1.

Against that, two normative texts:

§2.3 `[R-CNF-02]`: "This document defines format major 1, and a file declaring
another major is neither conforming nor nonconforming under it: a reader refuses
such a file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not
a finding about its bytes."

§21.6's closing paragraph: "Neither is a register row: the register enumerates
file-conformance violations (§21.1), and a file this document declines to judge
is not one. What is registered in each case is the neighbouring condition that
*is* a violation — version_major = 0 … (F20, `[R-CNT-07]`)".

§21.6 asserts F20 is the only registered version_major condition. §21.2
registers version_major a second time under F1.

**Why §21.1's tiebreak does not reach it.** §21.1: "where a row and the rule it
cites diverge, the rule governs." F1 cites `[R-ENC-01]` and (R-CNT-07). F1 does
*not* diverge from `[R-ENC-01]` — a writer that emits big-endian really does
violate it. The conflicting text is §21.6 and §2.3, which F1 does not cite.
§21.1 also says "§21.6's entries restate their governing rules on the same terms
a row does, and where such an entry and the rule it cites diverge, the rule
governs there too" — which arbitrates an entry against *its* rule, not a §21.2
row against a §21.6 entry. There is no stated precedence between them.

**The two implementations, concretely.** Take Appendix A's 128-byte file with
[72, 74) changed from `01 00` to `00 01` and the trailer CRC recomputed over
[0, 60) of the trailer.

- Verifier A implements the register mechanically. It sees version_major = 256,
  notes that byte-swapping yields 1, records F1, and — per §2.3's "An
  established violation takes priority" — reports **nonconforming**, reject-file,
  `[R-ENC-01]`, detected at open.
- Verifier B implements §2.3 and §21.6. The file names a major it does not
  implement, which `[R-CNF-11]` lists verbatim as a *cannot establish* ground.
  It reports **cannot establish** and makes no finding about the bytes.

Both cite the document. §6.3 says exactly what the first costs users: "a reader
that reports an unimplemented major as corruption misleads users into
discarding files that current software reads."

**Byte-level: yes.** I want to be exact about where the fork lands, because it
is narrower than "reader acceptance":

- *Emit*: no fork. No conforming writer emits big-endian.
- *Reader accept/reject*: no fork. Both readers reject-file under `[R-CNT-07]`.
- *Certification*: no fork. Neither verifier certifies.
- *Verifier verdict on a specific byte sequence*: **forks**, and the two verdicts
  are normatively contradictory — §2.3 says "*Cannot establish* is not a finding
  that the file is nonconforming."
- *Corpus*: `[R-ERR-02]` demands one vector per instance whose expected verdict
  is the row's outcome; `[R-VEC-02]` demands the manifest record "whether the
  file is **conforming**". For this file §2.3 says neither, so the entry cannot
  be written, and `[R-VEC-02]` names that outcome "a finding against this
  document rather than a vector".

I considered downgrading on the strength of §2.3 alone — it is a
conformance-class definition and §1 tells the reader "§2 fixes the conformance
vocabulary every later section uses, and is worth reading first". But §19's
preamble points implementers the other way: "Those enumerations are not the
complete inventory of what a reader detects at that tier: §21's register is,
and `[R-CNF-04]` binds a reader to every register row whose detector is the
reader." A verifier author is told to build from the register, and the register
contains the wrong instance. Two competent teams reading the whole document do
ship different behaviour here. I uphold it.

**reader-03's second half is refuted.** reader-03 argues the `generation`
instance is equally witnessless, since a big-endian g ≤ 127 reads as g·2⁵⁶ <
2⁶³ − 1 and passes every trailer gate. True for small g, but the instance is
constructible for larger g: generation 0x80 written big-endian reads
0x8000000000000000, which exceeds 2⁶³ − 1 and fails F3 / `[R-CNT-06]`'s
`1 ≤ generation ≤ 2⁶³ − 1` gate. F1's own condition text — "detectable only
through that field's own value or range gate" — concedes that the vector builder
picks a value that trips, and for `generation` such a value exists. It does not
for `version_major`. The other three instances (dir_offset, dir_length,
committed_file_length) are likewise constructible: 16 byte-swapped is
0x1000000000000000, failing F12; committed_file_length byte-swapped fails
F15/F19.

**Repair.** Delete `trailer version_major` from F1's Instances cell, leaving
four instances; the register's instance total drops 253 → 252. Optionally add
a parenthetical to F1 noting that version_major carries no distinguishable
big-endian witness and that F20 is the registered version_major condition
(§21.6). Interacts with group F: if F's +4 is also accepted the total is 256.

---

### F. `instance-arithmetic-container-dimension` — register-03, adversary-02

§21.1: "An instance names a field the condition ranges over, a container it can
occur in, one of several alternatives the condition text states, or any
combination of the three — **a condition applying to two alternatives in two
containers has four**." And: "the count is therefore mechanical once the cell is
written."

I checked the disputed cells against the neighbours that share their grammar.

| Row | Condition shape | Cell | §21.1 arithmetic |
|---|---|---|---|
| L16 | "A layer record's or sub-record's extent slot has exactly one of offset and length zero" | 4 items | 2 alternatives × 2 containers = **4** ✓ |
| L17 | "A layer record's or sub-record's nonzero extent slot has extent_offset < 16" | "layer record extent slot; sub-record extent slot" | 1 × 2 = **2** ✓ |
| L18 | same grammar | 2 items | **2** ✓ |
| L47 | "A layer record's **or sub-record's** flags carry MU = 1 with PE = 0" | "—" = 1 | flag pair is one predicate (§21.1's own carve-out), but 2 containers = **2** ✗ |
| L48 | "Any of a layer record's **or sub-record's** reserved flag bits 2-15 is set" | "flags bits 2-15" = 1 | bits are one family (cf. F28), 2 containers = **2** ✗ |
| L50 | "A layer record, **or a sub-record** of a type §7.3 registers, carries a stored MU or PE bit differing…" | "layer record flags; sub-record flags" = 2 | F30's twin enumerates the two bits as 2 alternatives; × 2 containers = **4** ✗ |

L50 against its file-scope twin F30 is the sharpest: identical condition text,
F30 has one container and enumerates the two *bits* ("flags bit 0; flags bit 1");
L50 has two containers and enumerates the *containers*, dropping the bit split.
The document therefore treats "a stored MU or PE bit differing" as two
alternatives at file scope and as none at layer scope.

L47's collapse of the two flag bits is correct — §21.1 names "a combination of
two flag bits" as a single predicate. L48's treatment of bits 2–15 as one family
is correct (F28 does the same). Neither container collapse is.

Net: +1 (L47) +1 (L48) +2 (L50) = **+4**, so 253 → 257 under §21.1 as written.

**Byte-level: no.** Deciding text, §21.1: "The **Instances** column enumerates
what a conformance corpus builds for that row (§21.8): the row is the rule, and
each instance is one file." The row is the rule. Every one of the four missing
files is already a violation under the same row, the same governing rule, the
same detector and the same outcome — no implementation's verdict on any byte
sequence moves. And §24 `[R-VEC-01]`: "where a vector's recorded expectation and
this specification disagree, this specification governs and the vector is
corrected."

**Severity: register-bookkeeping.** Repair: rewrite the three cells to enumerate
containers (L47 → "layer record flags; sub-record flags"; L48 →
"layer record flags bits 2-15; sub-record flags bits 2-15"; L50 → the four
bit × container combinations), and update §21.8's totals. Note the interaction
with group E (−1) and the unresolved conflict with group G's counting claim.

---

### G. `instance-cells-label-alternatives-as-fields` — quiz-03

§21.1's exclusion: "One instance is one *distinguishable* file: where a
condition is a single predicate over several fields — a sum against a bound, a
combination of two flag bits — the fields it reads are not instances, because no
two files could differ."

Several cells nevertheless list field names for single-predicate conditions:
L16 ("layer record extent_offset; layer record extent_length; sub-record
extent_offset; sub-record extent_length"), L23 ("extent_offset; extent_length;
entry_count"), F32 ("extent_offset; extent_length").

**The labelling defect is real.** But the reporter's reading (i) — that these
counts should shrink — does not survive checking. L16's condition *does* state
two alternatives: an extent slot with offset 0 and length ≠ 0 is a different
file from one with offset ≠ 0 and length 0. F32's parenthetical spells them out
verbatim: "(offset 0 with length != 0, or offset != 0 with length 0)", and
L23's does too: "including slot (0,0) with entry_count > 0, or a nonzero slot
with entry_count = 0". So the counts are right and the *labels* are wrong: the
cells name fields where they mean alternatives.

**Consensus: PARTIAL.** The labelling defect stands; the arithmetic claim does
not. And the reporter's supporting claim — that counting every cell under the
shorthand reading "matches §21.8's stated instance figure exactly" — is in
direct conflict with group F's +4. I did not recount all 125 cells and so cannot
adjudicate; I flag the conflict rather than assert a total.

**Byte-level: no** — same §21.1 quote as group F ("the row is the rule, and each
instance is one file"). **Severity: register-bookkeeping.** Repair: rephrase
L16, L23 and F32's cells as alternatives ("offset zero, length nonzero; offset
nonzero, length zero; …") rather than as bare field names.

---

### H. `endianness-rows-missing-at-layer-and-tile-scope` — register-04

`[R-ENC-01]`/`[R-ENC-02]` are cited by exactly two rows, F1 and F2, both in
§21.2, and F1's instances name only trailer and directory fields. The parallel
encoding rule `[R-ENC-06]` (fixed field widths) is registered at all three
scopes with scope-qualified condition text:

- F5 "A fixed **file-scope** structure places its fields at widths other than…"
- L3 "A field of a **layer-scope** structure is written at a width other than…"
- T27 "A **tile-index entry** places its fields at widths other than…"

F1's condition text carries no scope qualifier. A layer-scope occurrence is real
and detectable: a dimension extent Eᵢ of 1024 written big-endian reads
0x0004000000000000 ≈ 1.13 × 10¹⁵, which passes L1's 2⁶³ − 1 domain gate but makes
⌈Eᵢ/Tᵢ⌉ absurd and fails L22's entry_count cross-check — detectable exactly as
F1's own "detectable only through that field's own value or range gate"
describes. Same at tile scope through T9/T11.

**Byte-level: no.** Two deciding sentences. On outcome, §21.1: "Conditions
attach to the finest structure they damage, and the outcome follows from that
scope, never from the severity of the corruption" — which, with F1's placement
in §21.2 and its file-scope instance list, fixes F1 as file-scoped. On reader
divergence, §2.4 `[R-CNF-12]`: "For a nonconforming file no acceptance
obligation exists — a reader MAY reject it upon detecting any violation." So a
reader that takes reject-layer and one that takes reject-file are both
conforming, and the file is nonconforming either way.

What remains is a completeness gap against §21.1's normative clause: "a
*detectable* file-conformance violation this specification names and the
register omits is a defect in this document." **Severity:
register-bookkeeping.** Repair: either scope-qualify F1's condition text ("A
multi-byte **file-scope** field…") and add L- and T-rows in the shape of
F5/L3/T27, or scope-qualify F1 and state that layer- and tile-scope endianness
is recorded under L1/L2/L22 and T9/T11/T12 as a cause with no row of its own.

---

### I. `register-outcome-headers-overreach-verifier-rows` — register-02

§21.3's header: "Outcome: reject-layer — the named layer is unusable, every
other layer unaffected."
§21.4's header: "Outcome: reject-tile — that tile's read reports failure, and
never returns fill in place of data (`[R-CNF-09]`)."

Both gloss the outcome as a reader consequence for every row beneath them. That
is false for the verifier-detected rows: L19, L41, L42, L43, L47, L48, L49, L50
in §21.3, and T2, T4, T5, T26 in §21.4. The governing rules say more than "no
obligation" — they oblige the reader to *serve*:

- `[R-SER-08]` (T2): "A reader that neither detects the violation nor rejects
  the tile, and returns the value, MUST report 0x00 as false and every other
  byte as true."
- `[R-CNT-22]` (L50): "conforming readers nevertheless process the record under
  the fixed semantics".
- `[R-MTA-05]` (L49, F29): "unsorted members do not make a document unreadable …
  readers process the document unchanged".

§24 `[R-VEC-04]` repeats the assumption: "a vector's expectation is therefore a
pair: the scope no reader is permitted to serve, and the content a reader that
serves anything at all owes." For T2, T4, T5, T26, L47–L50 that names a scope
readers *are* permitted — and in T2's case instructed — to serve.

**Byte-level: no.** Deciding sentence, §21.1: "For a row whose Detector is
*verifier*, the outcome names the scope at which the damage is recorded, not an
obligation on any reader: the governing rule states what a reader does, and for
several such rows it obliges the reader to serve the structure unchanged
(`[R-SER-08]`, `[R-CNT-22]`)." That is the section's own reading rule and it
decides the case explicitly. Both behaviours are already licensed for the same
bytes — `[R-SER-08]` permits returning the value, `[R-CNF-12]` permits
rejecting — so correcting the headers removes no freedom and moves no verdict.

**Severity: register-bookkeeping.** Repair: qualify both headers ("for the rows
whose Detector is *reader*"), add `[R-MTA-05]` to §21.1's parenthetical beside
`[R-SER-08]` and `[R-CNT-22]`, and qualify `[R-VEC-04]`'s "the scope no reader
is permitted to serve" for verifier-detected rows.

---

### J. `r1-cites-outcome-rule-not-prohibition` — register-06

R1 registers "a document encoding of 0, or a reserved-range value (3-0x7F)" as
an ignore-record violation, citing only `[R-CNT-25]`. `[R-CNT-25]` fixes the
outcome and says nothing about validity: "An encoding value of 0, or one the
reader does not implement, makes that record unreadable, with the same outcome
as a failed CRC — ignore-record, SHOULD be reported."

What makes emission of a reserved-range value a violation is `[R-EXT-03]`: "a
value from a reserved range MUST NOT be emitted at all before this
specification assigns it." F38 and L26 both cite the rule that states their
prohibition (`[R-CNT-15]`, which spells out "emitting it is a violation"). R1
does not.

The trap: §21.6's neighbouring row explains why the *experimental*-range
encoding is not a violation ("§10.3's prohibition binds a writer's conduct, not
the bytes"), and §2.3's conduct carve-out cites "§10.3" undifferentiated,
without separating its publication clause from its reserved-range clause. A
verifier author applying §21.1's "where a row and the rule it cites diverge, the
rule governs" to R1 lands on `[R-CNT-25]` and could conclude that encoding 5 is
conforming.

**Byte-level: no.** Deciding sentence, §21.5's preamble: "Every row here is a
violation all the same: the outcome bounds a reader's blast radius and never
makes the file conforming (`[R-CNF-12]`); §21.6 lists the ignore-record
conditions that are not violations." §21.6's table lists only the
experimental-range encoding. Reader behaviour is identical under every reading
(ignore-record, SHOULD report). **Severity: editorial.** Repair: add
(R-EXT-03) to R1's Governing rule cell.

---

### K. `21.9-hard-limit-list-incomplete` — verifier-04

§21.9 opens with a completeness claim — "Every limit affecting which files are
valid, or which files a conforming reader accepts, lives here (`[R-CNF-10]`)" —
and `[R-ERR-05]` enumerates the hard ones, closing with an accounting written
as exhaustive: "Most follow from a field's width, an external format, or the
value domain, and the rest from arithmetic over structures a generation cannot
omit. One does not: the 512 floor on A."

At least two limits of exactly that character are absent:

1. **The zstd declared-window cap.** `[R-COD-06]`: writers "MUST NOT declare a
   window size exceeding the tile's decoded size; a reader MUST treat either as
   a validity error at tile scope" — register row T21. Precisely parallel to the
   lz4 0x7E000000 cap, which *is* listed, and paired inside §21.9's own table
   with a minimum guarantee ("zstd frame `Window_Size` | 8 MiB") exactly as the
   tile-size guarantee is paired with the lz4 cap.
2. **The user-metadata extent floor of 5 bytes.** §7.1 `[R-CNT-25]`: an extent
   "whose extent_length is less than 5 … is a validity error at its containing
   scope" — rows F24 and L12. The same shape as the listed "a directory of at
   least 4 bytes".

**Byte-level: no.** Deciding sentences: §21.1 — "The register — §21.2 through
§21.5 (`[R-ERR-02]`) — enumerates every detectable file-conformance violation
this specification names" — and §2.3 `[R-CNF-04]`: "A reader MUST detect every
violation the error register (§21) assigns to the reader as its detector."
T21, F24 and L12 are register rows with detector *reader*, so both checks are
mandated regardless of §21.9's list. Two implementations that read the whole
document reject exactly the same bytes.

**Severity: editorial.** Repair: add both to `[R-ERR-05]`'s enumeration, or
soften §21.9's opening claim to "every *magnitude* limit", since the hard-limit
paragraph is explicitly a finding aid ("They are stated where the structures
forcing them are defined").

---

### L. `21.9-name-cap-rationale-false-for-metadata-keys` — register-07

§21.9: "a name at most 255 bytes (`[R-ENC-12]`, a `u8` length prefix)", then
"Most follow from a field's width … One does not: the 512 floor on A."

§4.6: "**Names** — the strings that identify layers, dimensions, channels, **and
user-metadata keys** — satisfy three further constraints." A user-metadata key
is a JSON string inside a document. It has no length prefix of any width, and
nothing about its representation forces 255. The cap reaches it only because
`[R-MTA-04]` imports §4.6's rules — "every key satisfying §4.6's name rules —
non-empty, at most 255 bytes, free of U+0000 through U+001F" — and R10 registers
the violation as ignore-record.

So for keys, 255 is a second number chosen here, and §21.9's parenthetical
justification is false for that case.

**Byte-level: no.** The bound is stated identically in §4.6, §18.2 and R10, and
§21.9 restates the same number; a 256-byte key is ignore-record under every
reading. Deciding sentence, `[R-MTA-04]`: "every key satisfying §4.6's name
rules — non-empty, **at most 255 bytes**, free of U+0000 through U+001F."
**Severity: editorial.** Repair: qualify the parenthetical ("a `u8` length
prefix where a name is a structural field; imported by `[R-MTA-04]` for
user-metadata keys") and adjust "One does not" to "Two do not".

---

### M. `21.7-account-incomplete` — writer-06, register-05

§21.1 bills §21.7 as "the account, **by class**, of what fails" the
detectability gate. §21.7's second paragraph gives a closed list of three
classes: `[R-LIF-01]`/`[R-LIF-03]` as history properties; `[R-GEO-06]`/
`[R-SER-01]` as satisfied by any structurally valid tile; `[R-CNT-13]`'s
no-embedded-offsets rule as opaque by construction.

Missing, from two directions:

- **Writer/updater obligations with no file witness** (writer-06):
  `[R-LIF-02]` steps 4 and 6, the two durability barriers — no byte records
  whether fdatasync was called, yet Appendix H lists "follows the commit
  protocol including both barriers" under conforming writer, i.e. as something
  to audit; `[R-WRT-05]`'s byte-identical re-emission and `[R-WRT-08]`'s
  no-re-encode rule, both comparisons between adjacent generations that §9.7
  does not reconstruct; `[R-WRT-06]`'s fresh file_id and `[R-WRT-07]`'s
  "reference arrays MUST equal the live generation's bit for bit", both needing
  the compactor's input; `[R-WRT-09]`'s verification-before-emission ordering;
  and §20.3's bar on an appender relocating a live index region (group U).
- **A stated validity error whose witness this major cannot produce**
  (register-05): `[R-CNT-18]`'s "a sub-record MUST NOT itself contain records
  (nesting depth beyond two is a validity error at layer scope)". It belongs to
  neither stated class — it is not content incorrectness, and it is not a
  property of history; a single file could in principle exhibit it. What makes
  it unwitnessed is that no sub-record payload in major 1 is defined as a record
  sequence.

Two witnessless writer rules are already handled by local notes instead of by
§21.7 — §16.2's note for `[R-SLB-04]` and §7.4's note for `[R-CNT-18]` — which
shows the class is known and treated case by case.

**Byte-level: no.** None of the omitted obligations is detectable in a single
file, so §21.1's completeness clause — scoped to "a *detectable*
file-conformance violation" — is unaffected and no register row is missing.
§7.4's own Note already gives the operative answer for nesting: "in format major
1 it has no reader-detectable witness, and so no register row." And §21.1's
billing is hedged: "the account, **by class**".

**Severity: editorial.** Repair: extend §21.7's second paragraph with the
writer/updater class and a third class ("a stated validity error whose witness
this format major version cannot produce"), or state that the paragraph
enumerates classes by example rather than exhaustively.

---

### N. `21.1-normative-rules-uncited` — register-08

§21.1 states the register's governing rules — completeness is normative;
row-versus-rule precedence; conditions attach to the finest structure they
damage; specializations record against the narrower row; the instance
arithmetic. None carries an `[R-<PREFIX>-<NN>]` identifier. The only identifier
in the subsection is `[R-ERR-02]` in its opening line, which §21.8 defines as
the vector-coverage requirement and which reads in §21.1 as a cross-reference
for the range "§21.2 through §21.5". `[R-ERR-01]` closes §21.7;
`[R-ERR-03]`–`[R-ERR-05]` are §21.9's. I checked §21.1 for other identifiers:
`[R-CNF-07]`, `[R-CNF-04]`, `[R-CNF-11]`, `[R-SER-08]`, `[R-CNT-22]` — all
cross-references, no assignment.

§2.2: "Normative requirements carry identifiers of the form
`[R-<PREFIX>-<NN>]`." §1's reading note: "test vectors and conformance
checklists cite identifiers, never prose positions." A manifest or checklist
needing to cite the row-versus-rule precedence rule — the sentence that decides
every triage question the register can raise — has nothing to cite but a prose
position.

**Byte-level: no.** Deciding sentence, §2.1 `[R-CNF-01]`: "All text in this
document is normative except: §1 (Introduction); any text labeled *Note*,
*Example*, or *Rationale*; and appendices identified as non-normative." §21.1 is
none of those, so every rule it states binds regardless of citability.
**Severity: editorial.** Repair: assign `[R-ERR-06]`… to §21.1's rules.

---

### O. `field-taxonomy-informative-class-empty` — reader-05, writer-08, quiz-02

`[R-ENC-16]`: "Every field this specification defines is classified
**structural**, **semantic**, or **informative**. A field classified informative
MUST NOT affect how any byte is located or decoded, and a reader MUST NOT alter
decoding based on it; **each informative field's definition states what a reader
does when it contradicts the data it describes**."

Two defects, both verified against the document:

1. **The informative class has no members.** I checked every layout table with a
   Class column — §6.1, §6.2, §7.2, §7.4's fixed fields, §15.1, §18.2 — and every
   cell reads structural, structural (reserved), or semantic. The word
   "informative" appears only in §1's rubric note and §4.7 itself. So
   `[R-ENC-16]`'s second clause has no subject, and §1's promise that every
   field is classified into one of three classes advertises a class the document
   never uses.
2. **The name fields are underdetermined.** §4.7's Note exempts the layer
   record's inline payload from carrying a class column and delegates: "its
   table omits the offset and class columns, and each field's class follows from
   the definitions above." For most fields it does follow (extents, tile
   extents, layout, codec, filter, index_encoding, entry_count,
   crc_of_crc_array are structural; §13.1 states outright that fill is
   semantic). For the layer, dimension and channel names it does not. A name
   locates no byte and decodes none, so it is not structural under §4.7's
   definition; it does not affect "what decoded values mean", so not obviously
   semantic; that leaves informative — but then `[R-ENC-16]`'s further
   obligation applies and §4.6 supplies no such statement, because a name cannot
   contradict data. The two definitions are also not disjoint as written: a
   semantic field never affects decoding either.

reader-05 adds that §6.2 classifies `generation` and `file_id` as semantic where
neither affects what a decoded value means. Same defect: the taxonomy's
definitions do not partition the fields the tables assign.

**Byte-level: no.** Two deciding points. `[R-ENC-16]` has exactly one operative
constraint and it binds only the informative class — a class no field in format
major 1 occupies — so whichever label a name carries, no byte is located,
decoded or emitted differently and no register row keys off the taxonomy. And
§4.7's delegating sentence is inside a block labelled **Note**, which
`[R-CNF-01]` makes non-normative: "All text in this document is normative
except … any text labeled *Note*, *Example*, or *Rationale*."

**Severity: editorial.** Repair: either give the inline-payload table a class
column and assign names explicitly, or state in §4.7 that format major 1 defines
no informative field and that `[R-ENC-16]`'s second clause binds only a class a
later version may populate.

---

### P. `front-block-residency-gloss` — reader-04

The question: a local reader that `pread`s the trailer, then the directory, and
never touches [0, 16) — must it check the front signature block?

Reading (a), literal residency: the obligation binds a reader that actually
holds the bytes; a pread-only open holds none, so it may omit.
Reading (b), the gloss: the dash-list names "a local file" alongside "a memory
mapping", so any local open makes [0, 16) resident per se and a pread-only
reader is nonconforming for failing to detect F8.

The consequence is observable: given a file whose byte 0 is `0x88`, an
mmap-based local reader rejects it and a pread-based one serves every layer.

**Byte-level: no** — and this is the group I most wanted to be wrong about, so I
worked the text carefully. §6.1's own preamble decides it:

> "A **local reader** is one whose transport serves any byte range at no
> per-range round trip — a local file or a memory mapping being the ordinary
> cases — and a **remote reader** one whose transport charges a round trip per
> range (§6.4). **That distinction governs the request accounting of §6.4 and
> nothing else; the obligation over the front block turns on residency
> instead**, because a transport can be classified either way at the margin
> while residency is decidable at any reader's own open path."

Reading (b) makes the front-block obligation turn on the local/remote
distinction, which that sentence forbids in terms. The rule's own subject —
"A reader whose **open leaves** bytes [0, 16) resident" — is a property of the
open path, and a pread-only open leaves nothing resident; the closing clause
repeats it: "The test is residency, not transport, so an implementation decides
it at its own open path without having to classify the network underneath it."
Three further restatements agree: §19.1 step 1 drops "a local file" from the
list entirely and keeps only "a speculative suffix window that reached offset 0
included"; F8's cell says "the obligation binds a reader holding those bytes
resident"; Appendix A says `[R-CNT-04]` "requires of any reader **holding
them**".

So the pread-only reader is conforming and may omit the check, and the mmap
reader is conforming and rejects — divergence on a nonconforming file, which
§2.4 `[R-CNF-12]` designs in: "For a nonconforming file no acceptance obligation
exists — a reader MAY reject it upon detecting any violation." No byte
sequence's status changes and no reader is obliged to accept.

**Consensus: PARTIAL.** Something is wrong there, but not the open fork the
reporter reports: the defect is the gloss "a local file" in the residency list,
which re-imports the very distinction the preceding paragraph disclaims.

**Severity: editorial**, with a caveat I want on the record for the maintainer:
the *repair direction* is byte-affecting. If the intent is (a), strike "a local
file" from the dash-list (leaving "a memory mapping, a speculative suffix window
that reached offset 0, or any transport already holding them") and add "a
reader whose open obtains only targeted ranges is one that would have to obtain
them, and MAY defer or omit the check". If the intent is (b) — which Appendix
A's "A local reader additionally verifies bytes [0, 16) by equality first"
suggests — then say so explicitly, and note that this *obliges* local readers to
reject F8 files that reading (a) lets them serve. Leaving the gloss as it stands
is what keeps the question alive.

---

### Q. `updater-may-not-drop-a-layer-record` — writer-01

The concrete question: can a conforming updater emit a generation whose
directory omits a layer record the prior generation carried — i.e. can a layer
ever be deleted?

§2.3 `[R-CNF-06]`: "An updater MUST satisfy every writer requirement for the
bytes it produces, and additionally MUST honor the preservation obligations of
Part I for records it does not understand."

§20.4: "Persistence governs every record type; only the authoritative source of
the flags differs. For a type §7.3 registers, the registry's fixed flags govern
rather than the stored ones (`[R-CNT-22]`) — both registered types carry PE = 1,
so neither can be dropped, and **implementing a record's type confers
understanding of it, not permission to drop it**."

§20.5 closes the compactor escape: the output contains the live committed state
"less any record §20.4 lets it drop", and §20.4 lets a compactor drop only its
MU = 0 / PE = 0 row. So under §20.4 no defined operation ever removes a layer
or a file-scope user-metadata record from a TARN file.

**Byte-level: no.** The document decides, and the deciding clause is written
precisely to defeat the §2.3-derived inference: "implementing a record's type
confers understanding of it, not permission to drop it." §2.3 is *silent* on
dropping understood records, not contrary — it states an obligation an updater
carries *in addition to* its writer requirements, and adding an obligation
elsewhere is not a contradiction. Independently, preservation across generations
has no single-file witness: §9.7 walks the live state only, and §21.7 names
exactly this class ("properties of a file's history, which §9.7 does not
reconstruct"), so no verifier and no reader can distinguish the two outputs.

**Consensus: PARTIAL.** The contradiction as framed (two normative rules "both
on point" with no tiebreak) does not hold; §20.4 governs. But three real defects
survive, and the third is the one that matters:

1. §2.3 mislocates the rule — "the preservation obligations of **Part I**" —
   while §20.4, which states them, is in Part III. Part I (§5–§10) contains no
   preservation obligation; §7.2 `[R-CNT-15]` explicitly defers: "Updater
   obligations for unknown records are §20's subject."
2. Appendix H's updater checklist says "respects unknown records' MU and PE bits
   (§20.4)", which scopes preservation to unknown records — siding with the
   reading §20.4 forecloses. Non-normative, but it is the summary an implementer
   auditing their own work reads.
3. **Substantively: the format has no defined delete-layer operation.** The
   nearest expressible move is to declare a zero extent on one dimension
   (`[R-GEO-02]`), dropping entry_count to 0 and the extent slot to (0, 0) — an
   idiom no text sanctions, and one that leaves the layer listed by name.

**Severity: design-decision.** The maintainer must answer whether layer deletion
is meant to be impossible. If it is not, §20.4's persistence paragraph needs a
carve-out for a caller-directed removal of a type the updater implements — and
that change *would* license outputs currently barred. If it is, say so
explicitly in §20.4 and fix §2.3's Part citation and Appendix H's line.

---

### R. `256mib-tile-guarantee-vs-8mib-window` — writer-05

§21.9 states minimum guarantees a writer "MAY rely on": decoded size of one
tile, 256 MiB; zstd frame `Window_Size`, 8 MiB. §17.2's note: "with
Single_Segment_Flag set there is no Window_Descriptor and Window_Size is the
frame content size, which this requirement already obliges to equal the decoded
size."

So a 64 MiB tile encoded as a single-segment zstd frame has Window_Size 64 MiB:
its tile quantity is inside the 256 MiB guarantee, its window quantity is
outside the 8 MiB one. `[R-ERR-03]`'s acceptance duty runs to a file "whose
quantities lie within these bounds" — conjunctive — so it is not engaged, and
`[R-ERR-04]` lets every conforming reader decline that tile, that layer, or the
whole file. A writer that took the 256 MiB row at face value has produced a file
no reader is obliged to read.

**Byte-level: no.** Two deciding sentences. §21.9 `[R-ERR-03]`: "a conforming
reader MUST accept any conforming file **whose quantities lie within these
bounds**" — the conjunction settles the verdict question. §17.2 `[R-COD-06]`:
"Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size`
guarantee even for a larger tile; **a wider window is conforming and merely
permits a conforming reader to decline the tile or the layer on resource
grounds** (`[R-ERR-04]`)." Declining is a MAY, so no two conforming readers are
obliged to differ, and no writer emits different bytes because of it.

**Severity: editorial.** The escape exists but lives in §17.2, three sections
from the guarantee it conditions, and satisfying it forces a writer to avoid
single-segment frames for every tile above 8 MiB. Repair: footnote §21.9's
`Window_Size` row pointing at `[R-COD-06]`'s SHOULD and naming the
single-segment interaction.

---

### S. `compactor-index-regeneration-keyed-on-wrong-thing` — writer-07

`[R-WRT-07]` triggers regeneration on "each **relocated** tile-index region".
But an index region's entries carry the *tiles'* offsets, not its own. A
compactor "free to place structures anywhere §5.2 admits" may legitimately leave
layer A's index region at its input offset while moving A's stored tiles to
close a slack run before them. Under the literal rule that region is not
relocated, so it is not regenerated, and its entries then address the tiles' old
positions.

Reading (i): "relocated" means "whose entries' targets relocated". Reading (ii):
literal, keyed on the region's own offset.

**Byte-level: no.** The same requirement's closing sentence decides it: "The
output's reference arrays MUST equal the live generation's bit for bit
(`[R-MDL-02]`): compaction changes where bytes live, never what a layer
denotes." Plus §2.3 `[R-CNF-05]`: "A writer MUST emit only conforming files." An
output whose entries point at the wrong bytes is nonconforming on its face (T1,
and T9 or F35 besides), so the file-conformance predicate already decides which
output is correct and no two *conforming* outputs differ.

**Severity: editorial** — but the practical stakes are high: an implementer who
reads (ii) and writes the obvious loop (`if region_offset changed then
regenerate`) ships a compactor that corrupts any layer whose region happens to
land back at its input offset. Repair is one clause: key the trigger on the
entries, e.g. "regenerates each tile-index region any of whose entries' offsets
the relocation changes".

---

### T. `slb-04-trigger-omits-sentinel-to-stored` — writer-09

`[R-SLB-04]`'s trigger: "A writer or updater whose commit **supersedes a stored
tile in, or grows the extents of**, a slab-declared layer MUST either
re-establish the invariants … or clear the declaration".

The declare-then-fill workflow the document promotes elsewhere does neither.
§13's Note — sparse writing: "Declare-then-fill workflows append tiles as data
arrives, generation by generation (§9)". §11.1's Rationale: "Empty layers serve
schema-first workflows: declare layers at creation, grow extents as data
arrives." A commit that turns a sentinel entry into a stored tile supersedes no
stored tile and grows no extent, yet it plainly changes the run's stored-tile
set and, unless the writer repacks, breaks `[R-SLB-03]`'s packing relation and
possibly its A_slab alignment when the new tile is the run's first stored one.

**Byte-level: no.** `[R-SLB-03]` is a standing invariant on the live state, not
on the commit: "When declared, for every run: the run's stored tiles are
contiguous and packed in ordinal order … A verifier MUST check these invariants
(violation: reject-layer, §15.3)." §16.2's own Note confirms the coupling:
"Because this rule's detection *is* `[R-SLB-03]`'s, a stale declaration carries
no register row of its own: every file exhibiting one exhibits a run whose tiles
are unpacked or whose first stored tile is misaligned, which §21.3 registers."
So the file's validity is decided either way and no implementation guesses what
to emit — it either repacks or the verifier catches it at L42/L43.

**Severity: editorial.** The rule is the one a writer reads to learn *when* it
must act, and its enumeration misses the exact commit shape §13 spends a note
recommending. Repair: broaden the trigger to "whose commit changes the
stored-tile set of, or grows the extents of".

---

### U. `appender-index-relocation-bar-has-no-keyword` — writer-10

§20.3, inside `[R-WRT-04]` step 4: "A layer whose record alone changes keeps its
extent slot, pointing at the existing region, as does a layer the commit leaves
untouched (`[R-WRT-05]`); relocating a live index region is compaction's
operation (§20.5, `[R-WRT-07]`), not an appender's."

Both this and §5.1's parallel sentence are declarative; neither carries a BCP 14
keyword, while the surrounding text of `[R-WRT-04]` is otherwise written in
MUSTs. The question: is an appender that re-emits a layer's index region at a
new offset — for defragmentation, to satisfy `[R-SLB-03]` after a repack, or
simply because it re-emits everything — violating a requirement?

**Consensus: PARTIAL**, on a point the reporter got wrong. §5.1's sentence ("A
commit never relocates a live index region otherwise; that is compaction's
operation") sits **inside** the block quoted as "> **Example — a file after
three commits.**", so `[R-CNF-01]` makes it non-normative: "All text in this
document is normative except … any text labeled *Note*, *Example*, or
*Rationale*." Only §20.3's clause is normative, and it sits inside "An appender
MUST, in order: … 4. **Write payloads and indexes**", so it is within a MUST-
scoped step and binds. The prohibition is real; what it lacks is an explicit
keyword.

**Byte-level: no.** Under both readings the emitted file is conforming — I
checked: §5.2's coverage classes are satisfied, `[R-CNT-13]`'s disjointness
holds, the old region becomes slack like any other superseded structure, and
`[R-CNT-17]`'s cross-check still holds. No verifier verdict and no reader
obligation differs; and like group Q, the property has no single-file witness.
§2.3 `[R-CNF-02]` already names this shape: "conduct rules bind the actor, the
predicate binds the bytes."

**Severity: editorial.** Repair: "an appender MUST NOT relocate a live index
region except as this step requires", with the reason stated — §20.5's fresh
file_id exists so that relocation is visible to (file_id, range) caches
(`[R-LIF-03]`), and relocating under the same file_id would move live bytes with
no invalidation signal. The document never states that reason.

---

### V. `compactor-latent-content-violation` — verifier-01

§20.1 `[R-WRT-01]`: "An appender and a compactor satisfy every writer
requirement for the bytes they produce and the preservation obligations of §20.4
for what they carry forward (`[R-CNF-06]`), and are readers of every structure
they process (`[R-CNF-11]`) — a violation latent in a structure they neither
modify nor rely on travels with it, and certifying the whole file is a verifier's
office (§9.7)."

§20.5 `[R-WRT-09]`: "it relies on **every** structure it copies, so it MUST
verify each link of the chain — the open (§19.1), each retained layer's record
(§19.3) and full index chain (`[R-IDX-04]`), and each relocated extent's
checksum, including every stored tile's entry crc — before emitting that
structure's bytes."

Take an input whose only defect is a verifier-detected *content* violation — a
padding position not carrying fill (T4, `[R-SER-05]`) or an interleaved bool
byte of 0x02 (T2, `[R-SER-08]`). `[R-WRT-09]`'s enumerated depth stops at the
entry crc and never reaches decoding, so the compactor does not detect it. Three
obligations then collide: copy verbatim (`[R-WRT-07]`: "every stored tile's
bytes verbatim"), emit a conforming file (`[R-WRT-06]`), and satisfy every
writer requirement for the bytes it produces (`[R-CNF-06]`, `[R-CNF-05]`). A
compactor produces every byte of its output, unlike an appender whose violating
bytes were written by an earlier generation and frozen by `[R-LIF-01]` — that
asymmetry is why §20.1's joint sentence works for appenders and strains for
compactors.

**Byte-level: no.** Both readings emit identical bytes when they emit at all —
`[R-WRT-07]` fixes the tile bytes verbatim — and the output file is nonconforming
under both, so no conforming file's byte sequence and no reader's accept/reject
verdict turns on it. Readers have no obligation to detect T2 or T4 at all
(detector: verifier), and §2.4 `[R-CNF-12]` covers a reader that does.

**Consensus: CONFIRMED**, severity **design-decision.** The tension is real and
the document should resolve it explicitly, because the wrong resolution is
expensive in both directions: an implementer builds either a compactor that
refuses a large class of compactable files, or one that silently launders a
nonconforming input into a fresh file_id at generation 1 — the more damaging
error, because the output looks new. Repair: state in §20.5 either that
`[R-WRT-09]`'s enumeration is the compactor's whole depth and `[R-WRT-06]`'s
"conforming" is conditional on a conforming input, or that a compactor must
verify to a verifier's depth. My reading of the text favours the first:
`[R-WRT-09]`'s list traces §8.2's chain of trust exactly ("trailer → directory →
… → index entry → stored tile"), which terminates at the tile's CRC.

---

### W. `partial-slack-total-regions-undefined` — verifier-02

§5.2 `[R-CNT-21]`: "A partial total counts only the bytes no claimant claims
**within the regions the verifier did walk**, and a verifier reporting one MUST
also name the regions it did not walk and report their byte extent."

"Region" is not a defined term for a unit of the walk. Elsewhere (§7.1, §15.1)
it names the directory region and the tile-index region, which are *claimants*,
not walk units. Three readings are defensible on a damaged file — say one whose
layer B's crc_of_crc_array is corrupt, so `[R-ENC-05]` forbids following B's
entry offsets:

(a) the region is the file and the claimants are the confirmed ones — a partial
total that overstates true slack by exactly B's unlocatable payload;
(b) a region is a span the verifier can certify it accounted for exhaustively —
B's tiles may lie anywhere in [16, F − 64), so no such span exists and the
partial total is 0;
(c) most literally, the regions walked are the byte ranges actually examined,
i.e. the claimants themselves, inside which nothing is unclaimed — 0 always,
which cannot be intended since the clause presupposes such bytes exist.

Two verifiers hand an operator different mandatory numbers for the same file,
and the second obligation is unsatisfiable in the case that produces it: the
byte extent of the regions not walked is precisely what the broken checksum
chain denied the verifier.

**Byte-level: no.** Deciding text, §5.2's Note: "A partial total (`[R-CNT-21]`)
reports what one verifier's incomplete walk left unclaimed, **which is a fact
about that run and not about the file's live state**." And §2.3: the
per-requirement report "constrains the report and not the verdict". Every
reading yields *nonconforming* on the same file and bars certification
identically.

**Severity: design-decision.** The maintainer must define the walk unit. Repair:
define "region" for `[R-CNT-21]`'s purposes (e.g. the byte ranges the walk
enumerated claimants for, expressed as a maximal partition of [16, F − 64)), or
replace the second obligation with one that is satisfiable — name the
*structures* whose enumeration failed and the scope each governs, and report
that the extent of what they addressed is unknown. §22.3 calls the slack total
"the number that distinguishes a working file from a padded one"; it stops being
comparable across tools until this is fixed.

---

### X. `verifier-traversal-past-capability-reject` — verifier-03

A file carrying (i) a top-level record of experimental type 0x8001 with MU = 1,
which the verifier does not implement, and (ii) a layer declaring
linearization = 2 (L34, a genuine violation). By §21.6 (i) is not a violation —
the file can be conforming in that respect — but `[R-CNT-15]` obliges the reader,
and hence the verifier, to reject-file.

(A) It stops there. §2.4: "A reader MUST NOT rely on any structure in it." The
traversal establishes no violation → *cannot establish*.
(B) A verifier "additionally checks **every** file-level requirement", so it
continues, establishes L34, and the priority sentence gives *nonconforming*.

Nothing licenses the stop cleanly: §2.3's only stopping licence is "A verifier
MAY stop at the first violation it finds", and this is not a violation — so a
verifier stopping here is also not caught by the accompanying obligation to
"report each scope it did not examine as *unexamined*", and the report loses
that signal too. §4.5 cuts the other way for (B): "*acting on* means using its
value to allocate, seek, fetch, or select behavior; **comparing a field against a
constant for validation is not acting on it**" — so checking linearization == 1
is not reliance and §2.4's bar does not forbid it.

The parallel case is clean by contrast: for an unimplemented version_major §2.3
says the file "is neither conforming nor nonconforming under it", so nothing is
establishable anywhere and *cannot establish* is forced.

**Byte-level: no.** Deciding sentence, `[R-CNF-11]`: "*Cannot establish* is not a
finding that the file is nonconforming, and **a verifier MUST NOT certify a file
it reports that way**." Both readings bar certification, both readers reject the
file, and no emitted byte turns on it. What differs is the label attached to the
refusal.

**Severity: design-decision.** The maintainer must say whether a capability-ground
reject-file halts the traversal, and if it does, extend the *unexamined*
reporting obligation to cover it. Without that, `[R-VEC-02]`'s manifest cannot
state a unique expectation for such a vector. (Note the file itself *is*
nonconforming — L34 is real — so the manifest's "whether the file is conforming"
field is answerable; it is the verifier verdict that is not unique.)

---

### Y. `t14-reads-on-sentinel-entries` — adversary-03

T14: "| T14 | Codec 1 (none) declared and the index entry's length differs from
the tile's decoded size | — | reader | tile use | `[R-COD-04]` |"

A sentinel entry's length field is 0xFFFF_FFFF_FFFF_FFFF, which differs from
every possible decoded size. T14's condition carries no non-sentinel qualifier —
unlike T8, T9, T10, T11 and T12, every one of which says "non-sentinel"
explicitly (I checked each). Read literally, T14 makes every sparse layer
declaring codec 1 nonconforming: the most ordinary sparse layer there is.

**Byte-level: no.** The document decides in three places that reach the sentinel
before `[R-COD-04]` is ever consulted:

- §3.1: "A tile is *stored in a generation* if and only if that generation's
  tile-index entry for it is not the sentinel." `[R-COD-04]` opens "**The stored
  bytes** are the filtered image verbatim. The index entry's length **therefore**
  MUST equal the tile's decoded size" — a derivation whose premise a sentinel
  lacks.
- §15.2 `[R-IDX-02]`: "**Sentinel entries are a reserved pattern, not offsets or
  lengths**" — so there is no "index entry's length" for `[R-COD-04]` to compare.
- §19.4 step 4: "A valid sentinel short-circuits steps 5 and 6 for that entry",
  and `[R-COD-04]`'s check is placed "before any payload fetch", i.e. between
  steps 4 and 5, after the short-circuit has fired.

§13.3 `[R-TYP-09]` independently confirms the sentinel path, listing the
conditions under which fill must NOT be returned — a malformed entry per §15.3,
a failed CRC array or segment, failed stored bytes — and not including a codec-1
length mismatch. And §21.1's tiebreak points at `[R-COD-04]`, which is where the
answer lives.

**Severity: register-bookkeeping**, but with the loudest practical consequence
of any editorial item here: an implementer who takes T14's cell literally rejects
every tile of every sparse codec-1 layer, and a verifier that does reports the
most common sparse file shape in the format as nonconforming. Repair: one word —
"Codec 1 (none) declared and a **non-sentinel** index entry's length differs
from the tile's decoded size".

---

### Z. `compactor-facing-a-failed-extent-crc` — adversary-04

`[R-WRT-09]` obliges a compactor to verify "each relocated extent's checksum …
before emitting that structure's bytes". §8.1's map gives a user-metadata extent
a checksum (its final four bytes). If it fails, `[R-CNT-20]` makes the outcome
ignore-record and §21.5 row R2 makes it a violation, so the input is
nonconforming.

The compactor is then boxed in:

- It may not drop the record — §20.4: "both registered types carry PE = 1, so
  neither can be dropped".
- It may not re-emit it corrected — `[R-WRT-05]` requires byte-identical
  re-emission of every record "it retains and does not logically modify", and
  recomputing a CRC over corrupt bytes is a modification.
- It may not carry the extent forward and emit — `[R-CNF-05]` requires a writer
  to emit only conforming files, and any output carrying that extent exhibits R2.

Refusing is the only surviving option, and nothing states it. Reaching it means
chaining five requirements across §20.4, §20.5, §8.2, §2.3 and §2.4, and the
natural first reading ("PE = 1, so carry it forward") produces a nonconforming
output. The same reasoning applies to a stored tile whose crc fails.

**Byte-level: no.** It converges on one answer. Deciding sentences: §2.3
`[R-CNF-05]` — "A writer MUST emit only conforming files" — bars emission; §2.4
`[R-CNF-12]` — "a reader MAY reject it upon detecting any violation" — licenses
refusal, and §20.1 `[R-WRT-01]` makes a compactor "a reader of every structure it
processes". No conforming implementation's emitted bytes or verdicts differ.

**Severity: editorial.** Repair: state the move in §20.5 — "a compactor whose
verification (`[R-WRT-09]`) fails for any structure it carries MUST refuse to
compact, since it can neither drop the record (§20.4) nor re-emit it modified
(`[R-WRT-05]`) nor emit a nonconforming file (`[R-CNF-05]`)." The cost of not
saying it is a compactor that launders corruption into a fresh file_id at
generation 1, with the input's history discarded — and §22.3 already notes that
byte-identical re-emission "carries such an extent forward unread" so "nothing an
updater does would surface the damage".

---

### AA. `ignored-record-extent-in-the-coverage-walk` — adversary-05

§2.4's outcome-class table, ignore-record row: "The record is skipped **as though
absent**. Decoding of all stored data is unaffected."

A verifier implementing the coverage walk reads that table to learn what an
ignored record contributes, and "as though absent" says: nothing. Two
consequences. First the slack total — §5.2 makes it a MUST-report, and a
verifier that drops an ignored record's extent reports a total larger by that
extent's length than one that keeps it. Second, and sharper, overlap: a
top-level record of experimental type 0x8001, MU = 0, PE = 0, inline_length 0,
extent slot (1000, 1000), with a layer's stored tile at [1500, 1600). Verifier A
walks the extent, finds the cross-scope overlap, reports F35 — reject-file.
Verifier B treats the ignored record as absent, finds no second claimant, and
certifies.

**Byte-level: no.** Deciding sentence, §5.2 `[R-CNT-02]`: "Every byte of the live
committed state belongs to exactly one of: the front signature block; or a
**structure** — a stored-tile extent, a record extent (the bytes any record's
extent slot references, **whatever the record's type**, §7.2), the directory, or
the trailer." Three further texts agree independently: §9.7's walk enumerates
"its records and their sub-records, each record's extent" with no exception;
§8.1's map gives "Extent of a record of a type this specification has not
assigned" its own row rather than omitting it; §22.3 says such an extent is
carried forward unread by re-emission, which only makes sense if it is live
state. And §2.4 disclaims the reach the misreading needs, two paragraphs below
the table: "the outcome classes describe the blast radius of a violation for
readers, never degrees of file conformance".

**Severity: editorial**, with real stakes: a verifier that gets it wrong
certifies files whose unknown-record extents alias live payload bytes —
precisely the aliasing class §22.3 claims `[R-CNT-13]` removes. Repair: extend
§2.4's ignore-record row — "The record is skipped as though absent for decoding;
its extent remains live committed state and is claimed by the coverage walk
(§5.2, §9.7)."

---

### AB. `json-number-finiteness-boundary` — adversary-06

`[R-MTA-04]`, second bullet: "A reader interprets every JSON number as an IEEE
754 binary64 value **and MAY use a wider representation**. A document is
unreadable if it contains a number whose binary64 interpretation is not finite —
which covers a magnitude that overflows on conversion, `1e400` being the ordinary
case…"

R8 registers a non-finite number as a violation, so this is a file-predicate
question. The threshold under roundTiesToEven is the midpoint between DBL_MAX
and 2¹⁰²⁴ — 2¹⁰²⁴ − 2⁹⁷⁰, a 309-digit decimal integer — so deciding whether a
literal makes the file nonconforming requires a correctly-rounded
decimal-to-binary64 conversion at full precision. A verifier that delegates to
its host JSON parser inherits that parser's overflow behaviour (saturate to
DBL_MAX on ERANGE, raise, or produce infinity), and the three disagree at the
boundary.

**Byte-level: no.** Two deciding texts. Appendix F incorporates "[IEEE 754] IEEE
754-2019 — binary16, binary32, and binary64" as a normative reference, which
fixes conversion from a decimal character sequence as correctly rounded under the
default rounding-direction attribute and carries overflow to infinity — so the
threshold is determinate and no two implementations reading this document plus
its normative references may legitimately differ. And the permission clause is
settled by the predicate's own wording: "**A document is unreadable if** it
contains a number whose binary64 interpretation is not finite" — the test is
stated over binary64 unconditionally, and §2.3 seals it: "File conformance is a
pure predicate on bytes: it does not depend on any reader."

**Severity: editorial.** What survives is cost, not indeterminacy: a verifier must
implement or borrow a correctly-rounded converter rather than trusting its host
parser, and the document never says that the pinning to binary64 outlives the
permission to go wider — "MAY use a wider representation" reads like it says the
opposite. Repair: add a clause — "the finiteness test is always the binary64 one,
whatever representation the reader uses internally" — and a pointer to Appendix
F for the rounding attribute.

---

### AC. `over-long-pre-trailer-pad` — quiz-04

`[R-LIF-02]` step 5 binds a writer to "append the pad to the next 64-byte
boundary" — a MUST-level step about emitted bytes. `[R-CNT-05]` then declares
that a longer gap is nevertheless conforming. With `[R-CNF-05]` ("A writer MUST
emit only conforming files") the two produce an odd creature: a writer that
violates a MUST while emitting a conforming file.

**Byte-level: no.** The reconciliation is in the document, in `[R-CNF-02]`'s
generalising clause: "A writer obligation whose violation this specification
expressly declares not to be a file-conformance violation — §6.3's flags = 0
against a set ignore-lane bit — binds the actor in the same way." `[R-CNT-05]`'s
"**a longer gap is conforming**, and no conforming commit produces one" is
exactly such an express declaration, so the generalisation catches it. The
competing reading — that `[R-CNF-02]`'s list is exhaustive — requires treating an
em-dash example as a closed enumeration against that same requirement's own
generalising sentence, and against §21.2's silence (F9 registers a *structure* in
that gap; no row registers an over-long empty pad).

**Severity: editorial.** Repair: name `[R-CNT-05]` alongside §6.3's flags case in
`[R-CNF-02]`'s example, so a verifier author working from the enumeration does
not report a conforming file as nonconforming. Settling it currently costs a trip
through three sections.

---

### AD. `diagrams-null-submission` — diagrams-01

The submission is a placeholder: Location "x", title "**y**", body "z", quote
"> q", rationale "r". There is no claim to evaluate and nothing in the document
it points at. Consistent with a reporter agent that produced no output; recorded
as REFUTED with severity none so that it is not counted as an unevaluated
finding. **No repair to the specification.** If the diagrams lens was meant to
run, it should be re-run — its absence means §5.1's, §9.2's, §20.3's and §20.5's
figures went ungraded this round.

---

## Coverage check

41 input ids, 30 groups, each id in exactly one group. Counted by hand against
the input list:

reader-01→A, reader-02→C, reader-03→E, reader-04→P, reader-05→O,
writer-01→Q, writer-02→A, writer-03→D, writer-04→C, writer-05→R, writer-06→M,
writer-07→S, writer-08→O, writer-09→T, writer-10→U,
verifier-01→V, verifier-02→W, verifier-03→X, verifier-04→K, verifier-05→C,
verifier-06→B,
diagrams-01→AD,
register-01→E, register-02→I, register-03→F, register-04→H, register-05→M,
register-06→J, register-07→L, register-08→N, register-09→B,
adversary-01→E, adversary-02→F, adversary-03→Y, adversary-04→Z, adversary-05→AA,
adversary-06→AB,
quiz-01→A, quiz-02→O, quiz-03→G, quiz-04→AC.

Group sizes: A 3, B 2, C 3, D 1, E 3, F 2, G 1, H 1, I 1, J 1, K 1, L 1, M 2,
N 1, O 3, P 1, Q 1, R 1, S 1, T 1, U 1, V 1, W 1, X 1, Y 1, Z 1, AA 1, AB 1,
AC 1, AD 1 = 41.

**Byte-level count: 1** (group E).

## Gaps I am not hiding

- I did **not** recount all 125 Instances cells of §21.2–§21.5. Group F's +4 and
  group G's claim that the shorthand reading reproduces 253 exactly cannot both
  be right, and I checked only the six cells the reporters named (L16, L17, L18,
  L47, L48, L50, F30, plus L23 and F32). The register's true total under a
  consistent reading is unestablished by me. Someone should count it
  mechanically, after resolving groups E, F and G together — E subtracts one, F
  adds four.
- I did not verify the byte-level arithmetic in adversary-01's or verifier-02's
  constructed vector files (X1, X2, the generation-2 worked file); I checked
  their reasoning against the spec but did not rebuild the files or recompute
  their CRCs.
- Group P is the one I would most want a second reader on. I downgraded it on
  §6.1's "That distinction governs the request accounting of §6.4 and nothing
  else" and on §19.1's and F8's restatements, all of which point at literal
  residency — but the dash-list's "a local file" is a normative phrase pointing
  the other way, and if the maintainer resolves it toward (b) that resolution
  *adds* a reader obligation to reject a byte sequence readers may currently
  serve.
