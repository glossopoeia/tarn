# Round 21 triage — correctness lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (lines 1–4377), in
  chunks: 1–200, 200–420, 420–700, 700–1000, 1000–1330, 1330–1650, 1650–2000,
  2000–2360, 2360–2700, 2700–3050, 3050–3300, 3300–3400, 3400–3480, 3480–3620,
  3620–3800, and 3905–3990 + 4166–4377 (§24, Appendix G, Appendix H).
- Nothing else. No walk transcripts opened (I checked every claim against the
  document instead). No `transcript-triage-*.md` opened; I listed the round21
  scratch directory once with `ls | head -20`, which returned only `.py`/`.tarn`
  build artefacts before the cut — no triage filenames were displayed, and I did
  not open any.
- No `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
  `spec/registry.json`, no git history, no web. Notably **I could not consult
  RFC 8878**, which matters for adversary-01 and is disclosed there.

## Grouping

Every one of the 21 findings turned out to be a distinct defect. No reporter
split one defect across two findings, and no two reporters described the same
one. The near-misses I checked and rejected as merges:

- **diagrams-01 vs quiz-02.** Both concern §2.3's acceptance-duty qualifier and
  §21.6's two capability refusals — but from opposite ends. diagrams-01: Appendix
  H's summary *drops* the MU = 1 carve-out. quiz-02: §2.3's carve-out is *too
  broad* (reaches sub-records). Different locations, opposite repairs. Separate.
- **quiz-01 / quiz-03 / verifier-02 / writer-03.** All four touch §18.2
  [R-MTA-09]. quiz-01 = the referent of "the bound above". quiz-03 = keywordless
  "is ignore-record" against [R-ERR-04]'s MAY. verifier-02 = the verifier SHOULD
  states no consequence. writer-03 = §21.5's preamble points at §21.6 for the
  decline. Four distinct sentences, four distinct repairs. Separate.
- **verifier-01 vs adversary-02.** Both are about a verifier's scope
  bookkeeping, but §5.2's partial total and §16.1's alignment invariant are
  unrelated rules. Separate.

---

## writer-01 — §21.9's per-tile guarantee over a layer that addresses no tile

**Quotations checked (all accurate and in context):**

§21.9 table row: `| decoded size of one tile | 256 MiB |` — no "addressed"
qualifier anywhere in the row or the table.

[R-ERR-04]: "A file exceeding any of these remains conforming, and a reader MAY
decline it — at the whole file, or at the narrowest scope whose declarations
exceed what it can serve, a layer or a tile. Software that declines **on that
ground** a file whose every quantity lies within the table is not a conforming
reader (`[R-CNF-03]`)…" — quoted correctly by the reporter.

§17.2's Note: "The cap is quantified over the layer's *addressed* tiles, so a
layer that addresses none … satisfies it whatever its tile shape declares…
`[R-ENC-04]`'s overflow rule carries no such quantifier — it binds any sum or
product a file yields — so P·Q and P·Bᶜ are checked in an empty layer even
though this cap is not." — accurate.

§3.1: "**tile** — the unit a tile-index entry addresses". §11.2 gives N = 0 at
Eᵢ = 0. §19.3 obliges at layer access "the decoded sizes §14 derives from it
(`[R-SER-02]`, `[R-SER-07]`)".

**Is the constructed file conforming?** Checked field by field. Eᵢ = 0 is valid
([R-GEO-01], [R-GEO-02]); Tᵢ = 2³¹ ≥ 1 and MAY exceed the extent; P·Q = 2³¹ is
under 2⁶³−1 so [R-ENC-04] is satisfied; entry_count = 0 forces extent slot (0,0)
and crc_of_crc_array = 0 per [R-CNT-17]/[R-CNT-23]. Yes, conforming.

**Where I land.** The balance of the text actually favours *Reading B* (the
reader MAY decline), and by two routes the reporter under-weights:

- §14.2 calls P·Q and P·Bᶜ "declaration-derived quantities", and [R-SER-07]
  says "decoded size is a function of the layer's declarations alone —
  geometry, layout, and channel types — never of payload content". So the layer
  has a decoded size whether or not any tile instantiates it, and §19.3 obliges
  a reader to derive it at layer access for *every* layer.
- §17.2's Note's own logic: [R-COD-07] carries the "addressed tiles" quantifier
  **in the rule's own text** ("for a layer any of whose *addressed* tiles'
  decoded size exceeds 0x7E000000"); [R-ENC-04] carries none and therefore binds
  "any sum or product a file yields". §21.9's row carries none either.

But Reading A is *not* a careless reading. §3.1 defines a tile as the unit an
index entry addresses, and the row's subject is "decoded size of **one tile**",
which presupposes a tile. The writer built an actual 1088-byte file on it.

So the row's silence leaves both readings reachable, and the two differ in what
a conforming reader may do with one specific conforming byte sequence: under A a
reader declining that layer on the 256 MiB budget **is not a conforming
reader**; under B it is. That is precisely [R-ERR-04]'s last sentence going both
ways on one file. **Byte-level: yes.** CONFIRMED.

Repair: one clause in §21.9 or in the row, saying whether the quantity is
measured over addressed tiles (as [R-COD-07]'s cap expressly is) or over the
layer's declarations (as [R-ENC-04]'s ceiling expressly is). On the text as it
stands the honest default is the latter, which also matches [R-ERR-04]'s
"whose *declarations* exceed what it can serve" — but the maintainer has to say
so, because §3.1 makes the other side arguable.

---

## writer-02 — Appendix G leaves tiling and layout unpinned

Checked: Appendix G is headed "(non-normative)" and its preamble says "It adds
no requirement to any actor: a writer ignoring it is fully conforming."
[R-CNF-01] makes non-normative appendices non-normative. So **not byte-level**:
both tilings and both layouts are already conforming and already licensed by
[R-CNF-05] ("two conforming writers given identical input MAY produce different
conforming files").

Item 5's text is quoted accurately. §11.3's Note ("Tile extents are a writer's
choice, and this specification imposes none") and §14.4's Note ("A single-channel
bool layer does not — ⌈P/8⌉ packed bytes planar versus P bytes interleaved — and
both forms are valid") are both accurate.

**The strongest evidence the reporter did not use** is inside Appendix G itself,
item 2's rationale: "this format fixes no canonical serialization of logical
content, and two files carrying the same arrays can legitimately differ in
**tiling, layout, and codec**." The profile names the three axes on which same-
array files differ, pins codec (item 1), and pins neither of the other two. That
kills the "tiling and layout are input, not writer freedom" defence, which was
my main candidate refutation.

CONFIRMED. Severity design-decision: the maintainer must decide whether the
profile treats tiling and layout as caller input (say so in the preamble) or as
writer freedom to pin (add them to item 5's list).

---

## writer-03 — §21.5's pointer at §21.6

§21.5's preamble, verbatim, carries both exceptions and the pointer sentence:
"…and except where a reader or verifier declines the decode on the size bound or
on the frame's declared window, which `[R-MTA-09]` makes that actor's capability
and **not a fact about the file**. … §21.6 lists the ignore-record conditions
that are not violations."

§21.6 does not list the bound-decline. That much is factual.

**But the same paragraph decides why.** §21.6 is titled "Conditions that are not
violations" and every one of its rows names a *fact about a file* ("An index
entry is the sentinel", "A dimension has extent 0", "version_minor is higher
than this text defines"…). The preamble itself says the decline is "that actor's
capability and **not a fact about the file**" — so it is not a condition of the
kind §21.6 tabulates, and its absence is not an omission. §21.1 separately
exempts §21.6 from the completeness clause.

The claimed harm — an implementer classing a bound-decline as corruption — is
foreclosed by [R-ERR-04]: "a refusal on resource grounds MUST be reported as a
resource limit and not as a validity error".

PARTIAL: the asymmetry between the two exceptions (one has a §21.6 row, one does
not) is real, but the claimed false cross-reference is not established. Editorial
at most; the cheapest repair is one word ("§21.6 lists the ignore-record *file
conditions* that are not violations").

---

## verifier-01 — [R-CNT-21]'s partial total at file scope

Full text of the clause re-read. The **lead clause is the operative test**:
"Where the walk of §9.7 does not enumerate every region's claimants — whether
because … — the verifier MUST report the total as partial."

For F33 (cross-layer overlap) and F7 (a structure in the pre-trailer gap), the
walk *completes*; the violation is established **by** the completed enumeration,
since overlap "requires whole-directory knowledge" ([R-CNT-13]). So the test in
the lead clause is not met and the total is exact.

Three further passages decide it, which the reporter cites only in part:

1. §5.2's Note: "A partial total (`[R-CNT-21]`) reports what one verifier's
   **incomplete** walk left unclaimed."
2. [R-LIF-08]: "Where the walk does not complete — a scope-level rejection
   **blocks enumeration**, or the verifier stops at the first violation — the sum
   is reported as partial." An F33 established *after* enumeration blocks nothing.
3. [R-CNT-05], which the reporter does not cite at all, and which is decisive for
   F7 specifically: "A verifier MUST treat a structure in that gap as a validity
   error at file scope, **and counts the rest as slack**." The rule that creates
   F7 expressly keeps the counting obligation alive.

Readings (B) and (C) require reading the em-dashed gloss as *replacing* the lead
test and extending "discarded with the layer" to the file — neither is permitted
by the words. REFUTED. No repair owed; if the maintainer wants belt-and-braces,
one clause saying a file-scope rejection the walk itself established leaves the
walk complete would cost nothing.

---

## verifier-02 — [R-MTA-09]'s verifier SHOULD

Verbatim: "…the verifier SHOULD report the bound it applied and the stored length
of the extent it declined. The decline presupposes an encoding this
specification assigns…" — the sentence ends at "declined" and the next changes
subject. No consequence stated. Claim accurate.

§2.1's Note: "every SHOULD states the consequence of deviation." Accurate quote;
it is a *Note* and so non-normative ([R-CNF-01]), which is why this grades low.

I spot-checked the reporter's mechanical claim on a sample rather than all 25:
[R-CNT-03], [R-CNT-09], [R-CNT-10], [R-CNT-26], [R-COD-06], [R-LIF-03],
[R-LIF-07], [R-MTA-04], [R-TYP-10], [R-ENC-14], [R-WRT-04] step 2, [R-WRT-06]'s
version_minor floor, [R-SEC-03], §20.4's table, [R-CNT-20], §21.5's preamble —
every one states its consequence in the same sentence or the next. The claim
holds on the sample.

Not byte-level: [R-CNF-12] — "§21's register enumerates MUST-level conditions
only, and a verifier reports a SHOULD deviation as an advisory that does not bar
certification." CONFIRMED, editorial. Repair: append the consequence, on the
model of [R-MTA-10]'s "bytes a certificate covers without inspecting are counted
and named, never silent" — e.g. "unreported, an operator meeting *cannot
establish* cannot tell how much headroom would resolve it, or which document was
declined."

---

## diagrams-01 — Appendix H's reader checklist

§2.3 verbatim: "A reader MUST accept every conforming file of a format major
version it implements, **carrying no record of a type it does not implement with
MUST_UNDERSTAND = 1** … and none of whose values exceeds the minimum guarantees
of §21's limits table".

Appendix H: "accepts every conforming file within §21.9's minimum guarantees and
reports any resource refusal as a limit rather than as corruption
(`[R-ERR-04]`)". Both omissions are as described.

That the omission bites is settled by §21.6's closing paragraph: of an
experimental-range top-level type with MU = 1, "`[R-CNT-15]` obliges the reader
to reject, and `[R-CNF-02]` makes the file conforming all the same." So there is
a conforming file inside every guarantee that a conforming reader MUST reject.

Not byte-level: Appendix H is "(non-normative)" and states "each entry's
authority is the requirement or section cited, never this summary"; [R-CNT-15]'s
reject-file is an unqualified MUST. Also worth noting the *updater* checklist in
the same appendix already carries the carve-out ("rejects outright a file
carrying an unimplemented top-level MU = 1 record"), which makes the reader
line's silence an inconsistency inside one appendix. CONFIRMED, editorial.

---

## diagrams-02 — [R-CNT-27]'s 128-byte floor and the version gate

§6.2's ordered list verbatim: "A reader MUST validate, in order: the trailer
magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose
positions are fixed across all majors (`[R-CNT-24]`) — and then, those gates
passed, MUST validate all of the following…". The 128-byte floor is not in that
list, and [R-CNT-27]'s own MUST carries no ordering. Claim accurate.

§21.2's preamble is the only place that orders it, and it *is* normative text:
"the rows below whose subject is that file's *geometry* do not reach it… Four
rows are outside that reasoning and do reach it… F8 and F1's trailer-magic
instance, F14's trailer CRC… and F6 with F1's front-block instance." F5 is not
among the four, so §21.2 does place it behind the gate.

I checked the premise that an 80-byte future-major file is constructible:
[R-CNT-24] fixes only the magic at F−64, version fields at F−56, the CRC at F−4,
the front block, and the no-growth rule — it does not fix 64-alignment or
dir_offset/dir_length across majors. Premise stands.

Not byte-level: both readings refuse the file, and [R-CNF-02] already forbids a
finding about a foreign major's bytes — "a file declaring another major is
neither conforming nor nonconforming under it: a reader refuses such a file on
capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding about
its bytes." Only the diagnostic class and the report label move, and [R-CNT-07]
states the diagnostic obligation as a SHOULD, which [R-CNF-12] puts outside the
register. CONFIRMED, editorial: the ordering belongs where an implementer working
through §5.1/§6.2 will meet it.

---

## diagrams-03 — §4.7's folding promise vs §7.2's table

§7.2's five rows, verbatim Field cells: "type (0 invalid)"; "flags: bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved"; "inline_length";
"extent_offset"; "extent_length". Three of five carry no range. Claim accurate.

§4.7's Note, verbatim: "§6.1's block is a 16-byte constant, where a Value column
replaces type and range, and §7.2 folds **each** field's range into its Field
cell." The other two halves of that sentence are delivered exactly (§6.1 does
have a Value column; §7.4's packed table does omit offset and class), which is
what makes this an unmet promise rather than paraphrase.

Not byte-level: the promise is in a *Note* ([R-CNF-01]), and the three ranges are
normative elsewhere — [R-ENC-03]'s 0…2⁶³−1 domain, [R-CNT-12]/[R-CNT-18]'s
containment rules for inline_length, [R-CNT-13]'s (0,0)/one-half-zero/offset < 16
/past F−64 rules — and are cited as reader checks from §19.1 step 4 and §19.3.
CONFIRMED, editorial. Either fill the three cells or soften "each" to what §7.2
actually gives.

---

## diagrams-04 — §18.2's "Valid values | 1 or 2"

Cell verbatim: "1 or 2; see below". §21.6's row verbatim: "A user-metadata record
declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); the file is conforming — §10.3's prohibition binds a writer's
conduct, not the bytes." Both accurate.

The contrast with §7.4 is real and is the finding's strength: §7.4's
index_encoding cell spells the whole partition out ("any other value — including
0, reserved 2–0x7F, and the experimental range ≥ 0x80 (§10) — is a validity error
at layer scope"), and the metadata-encoding space is the one space where the
experimental range is *not* a validity error.

Not byte-level: "see below" is an explicit deferral and the prose directly under
the table gives the partition, corroborated by [R-MTA-03], [R-EXT-03], §17.4's
closing sentence, §21.6's row and [R-MTA-10]. CONFIRMED, editorial: extend the
cell on §7.4's model.

---

## diagrams-05 — §21.6's sentinel row

Row verbatim: "The tile is addressed but not stored; every sample position it
carries reads as the channel's fill".

[R-TYP-08] verbatim: "a reader that returns any of the tile's sample positions
**inside the layer's extents** MUST return, **for each channel the tile
carries**, that channel's fill value at every such position." Both divergences
are as described, and both widen.

[R-GEO-04]: "a reader MUST NOT return padding positions as samples." §19.4 step 4
restates it fully qualified. §13.3's Note draws the line expressly.

Not byte-level, and the document's own precedence device says so: §21.1 — "§21.6's
entries restate their governing rules on the same terms a row does, and where such
an entry and the rule it cites diverge, **the rule governs** there too."
CONFIRMED, register-bookkeeping. Repair: restore both qualifiers in the row.

---

## register-01 — §21.1's unidentified rules

Verified: §21.1 through §21.6 carry no terminating requirement identifier; the
only bracketed ids in that stretch are [R-ERR-02] cited *inside* §21.1 to fix the
register's extent, and [R-ERR-01] terminating §21.7.

**But the reporter's Reading (b) is foreclosed by the document**, which makes the
claimed harm impossible: [R-CNF-01] — "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*;
and appendices identified as non-normative." §21.1 is none of those. So no
reviewer can lose the completeness guarantee, the precedence rule or the instance
arithmetic by treating identifier-bearing text as the normative surface: §21.1
binds either way.

And §2.2's scope is narrower than the reporter reads it: it says "**Normative
requirements** carry identifiers", and §2.1's Note characterises a requirement as
naming "the actor it binds (writer, reader, updater, verifier, or file)". §21.1's
clauses bind no such actor — they govern the register's relation to the rules and
how a corpus is built. The same pattern occurs elsewhere without complaint: §8.2's
"Verification is not optional: no in-file flag disables it, and a reader that
skips it is not a conforming reader" ends no identifier either.

PARTIAL. The residual is real and worth a maintainer's decision — [R-VEC-02]
obliges a vector to cite "that row's governing requirement identifier", and a
vector exercising a §21.1 clause has only a prose position — but the claimed
contradiction with §2.2 is not established. Severity design-decision: mint an
[R-ERR-nn] for §21.1's completeness/precedence/specialization clauses, or state
that §21.1 is meta-text that binds no actor.

---

## register-02 — §21.6 citing [R-WRT-08]

§21.6 row's Rule cell: "`[R-CNT-15]`, `[R-WRT-08]`". [R-WRT-08] verbatim: "An
updater MUST NOT re-encode a record whose type it does not implement, and MUST
NOT modify one except by relocating its extent and re-pointing its slot under
§20.5 — the operation the no-embedded-offsets rule (§7.2) makes safe for MU = 0
records." Nothing about preserving or dropping per PE. Claim accurate.

Verified the drop rule lives in §20.4's table (MU = 0 / PE = 1: "Retain
byte-identical, extent content unmodified"; MU = 0 / PE = 0: "Retain
byte-identical, or drop it… An appender MUST NOT drop it except in a commit that
*independently* changes the scope the record attaches to"), and that neither the
table nor its introducing paragraph carries an identifier — [R-WRT-05] closes the
paragraph before it and [R-WRT-08] opens a new sentence after it. §2.4 likewise
cites it by section: "§20.4's table states the cases: its MU = 1 and MU = 0 /
PE = 1 rows."

Not byte-level: §20.4's table is reached normatively through [R-CNF-06] ("MUST
honor the preservation obligations of §20.4"), so two updaters emit the same
files. CONFIRMED, register-bookkeeping. Repair: cite §20.4 (or [R-WRT-05] with
it) in the row, or give §20.4's table an identifier.

---

## register-03 — §20.5's "(F36, L25, R1)"

Verified all six omitted rows exist and register reserved-range values: L31
(index_encoding), L33 (linearization), L34 (sample type), L36 (layout), L43
(codec), L45 (filter). The underlying claim in [R-WRT-06] is true for every
space, as the reporter says, via §19.3 + [R-WRT-09] + §20.5's refusal rule.

I looked for a narrower reading that would make the three named rows exactly
right, and there is a near-miss one: F36 and L25 are *verifier*-detected, so an
MU = 0 reserved-range record type can pass a compactor's reader-level open and
reach its output, while L31/L33/L34/L36/L43/L45 are reader-detected at layer
access and force refusal. But R1 is reader-detected too (open / layer access), so
that reading does not pick out the three either, and the sentence's own subject —
"values this text still registers as reserved-range violations" — is an inventory
of rows, not of what survives into an output.

CONFIRMED, register-bookkeeping, low. Repair: "(F36, L25, R1 among them)", or the
full list. Not byte-level: the omitted rows say what is needed on their own.

---

## register-04 — "— F27 and L48"

Verified the row-to-rule mapping from the Governing rule cells themselves: F27 →
[R-MTA-05]; L48 → [R-MTA-05]; F28 → [R-CNT-22]; L49 → [R-CNT-22]. The reporter's
Reading (A) is the correct one and the row texts confirm it.

Reading (B) — one row per rule — requires reading across a semicolon that closes
the [R-CNT-22] conjunct ("`[R-CNT-22]`, whose registered type keeps its fixed
semantics; **and** `[R-MTA-05]`, whose unsorted document readers process as they
find it — F27 and L48"). That is not permitted by the punctuation; it is available
only to a reader who does not read the sentence. So the claimed mis-mapping does
not stand.

PARTIAL: what is actually there is an asymmetry — one conjunct gets its rows
named and the other does not, in a sentence whose whole point is to spare a
lookup. Cheap repair: name F28 and L49 alongside. Register-bookkeeping. Not
byte-level: [R-CNT-22] and [R-MTA-05] each independently fix reader behaviour.

---

## register-05 — R7 / R8 overlap on the bare tokens

[R-MTA-04]'s bullet verbatim: "…or any of the bare tokens `NaN`, `Infinity`, or
`-Infinity`, **which RFC 8259 does not admit** and some parsers accept
regardless." R7's condition: "not well-formed JSON, or its top-level value is not
an object". R8's: "contains a non-finite number, **in any form**". A document
carrying a bare `NaN` satisfies both — the bullet's own clause is what makes it
not well-formed JSON. Overlap confirmed.

Checked §21.1's disposal device and it does not reach this pair: "Some rows are
strict specializations of others — F1 of F6 and of F8, F35 of F36, L24 of L25".
R8 is not a strict specialization of R7 (R8 also covers `1e400`, which *is*
well-formed JSON), so the specialization rule cannot resolve it even by analogy.

Instance count: I agree with the reporter's Reading (a) — §21.1 makes the count
"mechanical once the cell is written", and R8's cell says "in any form", so 2
stands and the 273 total is unaffected. No arithmetic consequence.

Not byte-level: both rows are ignore-record / reader / extent use, the file is
nonconforming either way, and [R-VEC-02]'s fallback ("the entry records every row
the file exercises and says which it was built for") already resolves the
attribution. CONFIRMED, register-bookkeeping. Cleanest repair: narrow R8's cell to
the binary64-non-finite case and let the bare tokens sit with R7, or name the
overlap where §21.1 names the specializations.

---

## register-06 — the 2⁶² ceilings

[R-ENC-03] verbatim: "The valid range of every offset, length, extent, and count
this specification defines — **entry counts and slab run lengths included** — is
0 to 2⁶³ − 1 inclusive". Alignments are not among the four categories, and the
express extension names exactly the two borderline cases the drafters wanted
included — which cuts toward Reading (B), since an alignment is at least as
borderline as a slab run length and is not named.

[R-ERR-05] verbatim: "Most follow from a field's width, an external format, or
the value domain… **Two do not**: the 512 floor on A… and the 255-byte cap on a
user-metadata key…". A field's width would give 2⁶³, not 2⁶², so the accounting
needs the value domain to reach A — which is exactly what [R-ENC-03] does not
say it does.

Not byte-level, and I checked the reporter's corpus claim rather than taking it:
under **either** reading an out-of-domain A is recorded against L39 ("A above
2^62") and A_slab against L29, because L1's Instances cell enumerates its fields
and names neither A nor A_slab, and §21.1 makes the count mechanical from the
cell. So the total stays 273 under both readings — the reporter's "275" is wrong,
which does not affect the finding. What decides the bytes is §7.4's table row plus
[R-CNT-23] and [R-SLB-01]'s "a reader MUST treat one as a validity error at layer
scope", independent of provenance.

CONFIRMED, editorial. Repair is a maintainer's pick of two: add alignments to
[R-ENC-03]'s enumeration, or amend §21.9's "Two do not" to four.

---

## adversary-01 — Frame_Content_Size on a metadata document

Checked every link.

§18.2 verbatim: "Encoding 2 stores it as exactly one RFC 8878 compressed frame
occupying the extent's bytes before its terminal CRC, under the frame constraints
of `[R-COD-06]` that do not reference a tile: the frame magic; no skippable frame
and no second frame; no nonzero dictionary ID; no content-checksum flag. The
constraints §17.2 states against a tile's declared decoded size do not apply,
because a document has no declared size…"

[R-COD-06] verbatim: "The frame content-size field MAY be present; when present it
MUST equal the tile's decoded size, a reader MUST treat a mismatch as a validity
error at tile scope" — T22. So for tiles TARN pins the constraint itself rather
than relying on the zstd binding.

R4's Instances cell enumerates exactly six carried-over constraints plus "bytes
remaining after the frame" (× two containers = 12 instances). FCS is in neither
R4's condition nor its cell. R3's condition is "A user-metadata document's stored
bytes **fail to decode** under its declared assigned encoding".

[R-SEC-02] verbatim: "A reader MUST NOT size an allocation, fetch, or index walk
in proportion to a declared magnitude it has not corroborated against the file's
actual length" — so a reader may not decline on FCS's strength; it must decode.

I also checked the reporter's claim about the window rule and found the gap is
*wider* than they say. §17.2's Note: "with Single_Segment_Flag set there is no
Window_Descriptor and Window_Size is the frame content size". That only converts
an FCS **above the reader's window bound** into a decline; an FCS of 999 against
100 bytes of content is below every bound and is caught nowhere, single-segment or
not.

**What decides it, and what I cannot check.** §18.2 withdraws only the constraint
"§17.2 states against a tile's declared decoded size" — i.e. FCS-equals-*the
tile's* decoded size. It does not address whether a frame whose FCS contradicts
its own content is a well-formed RFC 8878 frame; §18.2 requires "exactly one RFC
8878 compressed frame", which imports whatever RFC 8878 says. **I could not
consult RFC 8878 under this round's access rule.** So on this document alone, R3's
predicate on that byte sequence is not determined, and the two verdicts the
reporter describes — nonconforming (strict binding reports R3) versus certified
(lenient binding decodes a valid object) — are both reachable. Same bytes,
opposite conformance verdicts, and a reader difference too: one returns the
document, the other ignores the record.

**Byte-level: yes**, with the contingency stated. My premise, so it can be
attacked: *this document nowhere states whether an FCS inconsistent with its own
frame's content makes the stored bytes fail to decode, and its enumerated
carry-over list plus the express withdrawal of the tile-size comparison give a
reader positive grounds to think no FCS rule attaches.* The attack is to produce
RFC 8878 text making such a frame malformed, which would reduce this to an
asymmetry worth one sentence — but the asymmetry would still be worth that
sentence, because for tiles this document deliberately did not rely on the
external answer, and it already makes the express-non-constraint move one sentence
later for the window ("not a failure to decode within the meaning of R3").
CONFIRMED.

---

## adversary-02 — §16.1's "every stored tile"

§3.1 verbatim: "A tile is *stored in a generation* if and only if that
generation's tile-index entry for it is not the sentinel (§15)." §16.1: "When
declared: every stored tile's offset satisfies offset mod A = 0." Read alone, an
offset-5 entry is "stored" and trips L40.

**The document decides it**, at [R-IDX-03]: "Such an entry contributes no stored
extent to the ***verifier* rows**, which bind over well-formed entries' extents
only — `[R-SLB-03]`'s run continuity closes over it as it does over a sentinel."
§15.3's verifier-marked rows include "alignment or slab invariant violated (§16)",
so L40 is one of the rows that bind over well-formed entries only. [R-LIF-08]
says the same for the coverage walk.

The asymmetry the reporter identifies is real and I verified all three halves of
it: §16.2 answers the identical question in the open ("So are the entries §15.3
classifies reject-tile on a *structural* ground: they address no usable extent,
and the run's stored tiles close over them"); L41's Condition cell restates it a
third time; L40's Condition cell says none of it and reaches transparency only
through the "(R-IDX-03)" citation in its Governing rule cell.

Not byte-level: L40's detector is the verifier, [R-RDR-02] gives a verifier row
"no reader obligation", §16.1 itself says "readers are not obligated to — offsets
are always explicit, so alignment is reader-invisible", and T8 makes the file
nonconforming under both verifiers. CONFIRMED, editorial. Repair: mirror §16.2's
clause into §16.1, or into L40's Condition cell where L41 already carries it.

---

## quiz-01 — "the bound above"

Verified two bounds precede the verifier sentence and that the phrase is singular.
Reading 3 is right, and it is settled by normative text in two other places, not
only §21.5's preamble as the reporter says:

- §21.5's preamble: "except where a reader or verifier declines the decode on the
  **size bound or on the frame's declared window**".
- §2.3's cannot-establish list: "or when it declines to decode a user-metadata
  document (`[R-MTA-09]`)" — unqualified, so both.
- [R-CNF-11] independently makes any capability-ground inability to check a
  *cannot establish* ground, so no verdict moves under any of the three readings.

CONFIRMED as an editorial imprecision, not byte-level. Repair: "on either bound
above", four characters.

---

## quiz-02 — §2.3's acceptance-duty qualifier

§7.4 verbatim: "Sub-records are layer-scope records", so *record* in §2.3 does
literally reach them, and §2.3's clause literally withdraws the acceptance duty
for a file whose only unimplemented MU = 1 record is a sub-record.

[R-CNT-18] verbatim: "an unknown sub-record type with MU = 1 is reject-layer, and
where the file is otherwise conforming a reader **MUST NOT reject the file for
it**". §21.6's closing paragraph: "The qualifier is load-bearing — the same type
as a layer sub-record is reject-layer and never a ground to refuse the file
(`[R-CNT-18]`), so **only the top-level case** is a file a reader refuses."

Not byte-level, and I tested the gap the reporter did not: if the duty is
withdrawn *and* rejection of the file is forbidden, what is left? Exactly
reject-layer plus service of every other layer — which is what [R-CNT-18]
requires. So no behaviour is open. A withdrawn obligation cannot license the act a
MUST NOT forbids.

CONFIRMED, editorial. Repair: insert "top-level" into §2.3's qualifier, which is
what its own parenthetical ("§21.6's closing paragraph names the other two")
already asserts.

---

## quiz-03 — ignore-record versus whole-file decline

[R-MTA-09]: "a document exceeding that bound **is ignore-record** like any other
it cannot read" — no BCP 14 keyword. [R-ERR-04]: "a reader **MAY** decline it — at
the whole file, or at the narrowest scope whose declarations exceed what it can
serve, a layer or a tile" — and neither enumerated narrower scope is a record.
The Note is the only place the two are composed for the *size* bound.

**The sharpening the reporter missed**: [R-MTA-09] composes them in normative
text for the *window* bound, one sentence later — "is ignore-record on that ground
… and no violation: the file exceeds a §21.9 guarantee and so remains conforming
while the reader MAY decline it (`[R-ERR-04]`)". So the asymmetry is inside one
paragraph: the window sentence carries the composition, the size sentence does
not, and only a Note repairs it.

Not byte-level, on two normative sentences rather than the casing rule alone.
[R-CNF-03]'s duty runs only to "a conforming file … none of whose values exceeds
the minimum guarantees of §21's limits table", and this file's document exceeds
one; [R-ERR-04] then says "A file exceeding any of these remains conforming, and a
reader MAY decline it". Both behaviours are licensed by normative text, so no
writer's output and no file's status moves. CONFIRMED, editorial. Repair: mirror
the window sentence's clause into the size-bound sentence.

---

## Coverage

21 input ids; 21 groups; each id in exactly one group; union equals the input
list. Counted twice against the id list in the prompt.

Byte-level survivors: 2 — writer-01 and adversary-01. Both are stated with the
premise the judgement rests on, and adversary-01 carries an explicit external
contingency I could not discharge under this round's access rule.
