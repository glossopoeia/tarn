# Round 16 triage — correctness lens — working transcript

Read: `spec/tarn.md` only (§2.1–2.5, §4.2, §5.2, §6.1–6.2, §9.1–9.3, §9.7 excerpt,
§11.1–11.4, §14.2–14.5, §15.2–15.3, §17.2, §19.2–19.4, §20.3–20.5, §21.1–21.9,
§22.3, Appendix G). Read no transcripts at all — not the walk transcripts, and
(by construction) none of `transcript-triage-*.md`. Everything below is checked
against the document text, not against a reporter's account of it.

## Groups

### G1 — §21.7's "and nowhere else" account of §20.3 step 4
members: reader-01, writer-01, verifier-02, diagrams-01, register-01, adversary-01, quiz-02

Text checked (§21.7, verbatim, line ~3556):

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — the §21.4 rows firing there and nowhere else

§20.3 step 4's bar has four listed effects, verified verbatim:
"the set of padding positions (§11.3) and the content `[R-SER-05]` fixes there,
the decoded size, the byte offset of any sample within the decoded tile image,
or the codec and filter that produced the stored bytes."

Counterexample verified against the rows themselves:
- T17 (line 3439) `| T17 | Codec 3 (zstd) and the stored bytes do not begin with the
  compressed-frame magic 28 B5 2F FD | — | reader | tile use | [R-COD-06] |`
- T14 (line 3436) `| T14 | Codec 1 (none) declared and a non-sentinel index entry's
  length differs from the tile's decoded size | ... | reader | tile use | [R-COD-04] |`
- T3 (3425), T24 (3446), T25 (3447) likewise reader/tile use.

A codec 1→3 edit on a layer with G·T = E (no padding position), no bool channel,
tiles retained: the affected tile remains stored, the change reaches no
§14-constrained byte, and T17 fires. So the stated conjunctive necessary
condition is false and "nowhere else" is false. Consensus CONFIRMED. Only the
third limb (a sample byte offset moving inside an unchanged decoded size) is
genuinely unwitnessed — reader-01 and diagrams-01 both isolate that correctly.

Byte-level: NO. Deciding text, §21.1: "The subsections after §21.5 are not part
of the register and carry no rows: neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations, §21.7's account
of what no check detects, or §21.9's limits." And [R-CNF-04]: "A reader MUST
detect every violation the error register (§21) assigns to the reader as its
detector". T3/T14/T17/T24/T25 therefore bind regardless of §21.7's prose; every
verdict on every file is unchanged. Severity editorial (accuracy of a normative
account that carries no rows).

### G2 — the prior-generation tense vs the shrink paragraph's new-state tense
members: reader-02, register-04, adversary-02

Both sentences verified verbatim in §20.3 step 4. The bar quantifies over "any
tile that layer stores **in the generation this commit supersedes**" and glosses
"a commit does not escape this by unstoring in the same breath". The shrink
paragraph justifies its permission with "nothing is altered for a tile the new
state stores". A shrink to extent 0 de-addresses every tile (§11.1 [R-GEO-02]:
"A dimension with extent 0 is valid: its grid count is 0, the layer has zero
addressed tiles"), so the two quantifiers disagree about one and the same commit.
Genuine under-determination; CONFIRMED.

Byte-level: NO, and this is the closest of the conduct findings. Deciding text,
§21.7: "a commit that supersedes every tile it would have damaged leaves the live
state clean, so the bar is unwitnessed there for the same reason `[R-LIF-01]` is:
it is a property of the prior generation, which §9.7 does not reconstruct."
[R-CNF-02] fixes the predicate: "File conformance is a pure predicate on bytes:
it does not depend on any reader, writer, or environment." Both routes leave a
conforming live state (entry_count 0, extent slot (0,0), no stored tiles) that
every reader and verifier accepts identically. Emittable-by-another-actor: the
resulting live state is one a writer could equally have created outright — a
zero-extent layer with those declarations and no stored tiles is [R-GEO-02]'s
ordinary case — so no byte sequence leaves or enters the conforming set. Severity
design-decision: the maintainer must choose which tense governs a shrink.

### G3 — the shrink permission's premise is false when one shrink both drops and alters
members: writer-02, quiz-01

Arithmetic checked both ways. writer-02: E=(5,5), T=(4,4), shrink E_x 5→3 ⇒
G_x = ⌈3/4⌉ = 1, the t_x=1 column drops, and x=3 in the surviving t_x=0 tiles is
now a padding position. quiz-01: E=25, T=10, shrink to 15 ⇒ grid 3→2, tile 2
drops, tile 1's x=15..19 become padding. Both correct. In each case the
permission's stated premise — "nothing is altered for a tile the new state
stores" — is false while its trigger ("§11.2's grid count falls") holds, and the
clause ends in a flat "and the commit is permitted". CONFIRMED.

Byte-level: NO. Three sentences decide it. (i) The same step, one sentence
earlier: "Where the shrink leaves a stored tile addressed it is the case above —
barred wherever it alters what §14 fixes for that tile" — the clauses classify
tiles, not commits. (ii) The same step, on the general bar: "Where a change does
reach them it makes each stored tile it reaches nonconforming". (iii) [R-CNF-05]:
"A writer MUST emit only conforming files." [R-SER-05] closes it at file level:
"a verifier MUST check it, and a violation is a validity error at tile scope",
registered as T4 (detector verifier). So reading (a)'s output is a nonconforming
file under both readings, no verifier's verdict on it differs, and no conforming
writer may emit it. quiz-01's byte-level YES is downgraded on exactly those
quotations; its worked file is real and its repair is the right one. Severity
design-decision (normative wording of [R-WRT-04] must be conditioned).

### G4 — [R-WRT-06]'s neither/nor list repeats its first limb verbatim
members: reader-04, writer-04, verifier-04, diagrams-03, register-05, adversary-05, quiz-03

Verified verbatim at §20.5: "it can neither re-emit the structure corrected
(`[R-WRT-05]`), nor keep it and call the output clean — and a record §20.4 does
let it drop is no exception, dropping being available only where that table
licenses it — nor re-emit it corrected (`[R-WRT-05]`)." Same proposition, same
citation, first and third limbs. CONFIRMED, editorial.

adversary-05 additionally reports the same shape in §22.3 [R-SEC-04], and I
verified it: "which is why recovery output is re-verified as a whole file before
being trusted (`[R-LIF-06]`) before any use." That duplication is real and is a
second, distinct repair; I carry it in this group's recommended action because
adversary-05 can occupy only one group.

Byte-level: NO — the limbs are word-for-word identical, so every reading forbids
the same set of compactor outputs.

reader-04's reading (b) (the third limb's "it" being the droppable record) is
available grammatically but is a strict special case of the first limb, so it
changes nothing; reader-04 says so itself.

### G5 — [R-CNT-04] binds a "content sniffer", not one of §2.3's five classes
members: reader-03, diagrams-05

Verified: §2.3 opens "Conformance is defined for five classes" and names file,
reader, writer, updater, verifier. §2.1's Note states the discipline: "every
requirement names the actor it binds (writer, reader, updater, verifier, or
file)". "content sniffer" occurs exactly twice — in [R-CNT-04]'s MUST and in the
following Note ("Content sniffers match the 16-byte front block by equality"),
the latter excluded from normative text by [R-CNF-01]. CONFIRMED.

Byte-level: NO. The resident-reader half of the same sentence already binds any
party holding [0,16): "A reader whose open leaves bytes [0, 16) **resident** …
MUST verify the full block by byte equality before other processing, and MUST
treat any mismatch as reject-file. A reader that would have to issue a further
range request to obtain those bytes MAY defer or omit the check." A sniffer
necessarily holds those bytes resident, so the conjunct is inert either way.
Severity editorial; repair is to strike the conjunct.

### G6 — §11.1's Rationale says growth renumbers disk ordinals; first-dimension growth does not
members: writer-06, adversary-04

Checked [R-GEO-06] verbatim: "the **spatial tile ordinal** of (t₀, …, t_{d−1}) is
s = Σᵢ tᵢ · ∏_{j>i} Gⱼ". G₀ appears in no coefficient, so raising G₀ moves no
existing spatial ordinal. Both worked examples are arithmetically correct
(writer-06's G (2,2)→(3,2) and adversary-04's (1,2)→(2,2) both leave s = 2t_y+t_x).
The claim is true for planar layers (disk ordinal c·N + s moves with N) and for
growth along a non-first dimension with a nonzero earlier coordinate.
CONFIRMED as over-general.

Byte-level: NO. [R-CNF-01]: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*". The
normative sentence in §20.3 step 4 carries the correct qualifier: "(a geometry
change renumbers ordinals wherever `[R-GEO-06]` moves them)". Severity editorial.

### G7 — T18 enumerates skippable-frame placement, R4 does not
members: diagrams-04, register-03, adversary-03

Cells verified verbatim (T18 line 3440, R4 line 3462). T18 gives four instances
including three placements; R4 gives "a skippable frame, top-level extent; a
skippable frame, layer sub-record extent" — one per container — for the same
[R-COD-06]-derived constraint. §21.1's criterion: "a row whose check ranges over
a family without the condition changing shape states that range as a single
instance (T24's *any codec*), and one whose members give the condition materially
different shapes enumerates them (T15, T25)." The two cells apply it opposite
ways to one constraint. CONFIRMED.

Byte-level: NO. §21.1: "The subsections after §21.5 are not part of the register
and carry no rows" does not reach here (T18/R4 are rows), but the divergence
moves only §21.8's instance count and the corpus size; [R-COD-06] and [R-MTA-09]
decide reject-tile / ignore-record wherever the frame sits. Severity
register-bookkeeping. Note both reporters independently reproduced 275 from the
cells as written, so no arithmetic error exists today; the choice changes it to
273 or 279.

### G8 — whether [R-ENC-04] reaches P·Q in a zero-extent layer
member: verifier-01 (self-flagged byte-level YES — downgraded)

This is the one finding whose flag I had to work to settle. The reporter's claim
is that only the §17.2 Note decides it, and a Note is non-normative.

Three normative places decide it:

1. §21.3 row L2 (line 3367): "A declaration-derived sum or product of a layer
   exceeds 2^63 - 1 although every contributing field is in domain | … N·P; C·N …;
   **P·Q** (which dominates V = P·C); **P·Bᶜ**; … | reader | layer access |
   `[R-ENC-04]`". The cell carries no addressed-tile qualifier. The row directly
   above the reporter's own alternative — L44 (line 3409) — shows the drafters
   write the qualifier when they mean it: "Codec 4 (lz4) declared on a layer **any
   of whose addressed tiles'** decoded size exceeds 0x7E000000 bytes". §21.1
   makes register completeness normative and [R-CNF-04] binds a reader to every
   row whose detector is the reader.
2. [R-SER-07], normative: "decoded size is a function of the layer's declarations
   alone — geometry, layout, and channel types — never of payload content …
   Every decoded size, and the value count V, is a declaration-derived quantity
   under `[R-ENC-04]`." A function of declarations exists wherever the
   declarations do; Reading B needs decoded size to be a property of a tile, and
   this sentence says it is a property of the declarations.
3. §20.3 step 4, normative (not a Note): "`[R-COD-07]`'s lz4 decoded-size cap
   among them (L44), **which an empty layer escapes only because that cap is
   quantified over addressed tiles**. `[R-ENC-04]`'s 2⁶³ − 1 ceiling on every
   derived product is another". That states the whole contrast the reporter says
   lives only in §17.2's Note: the escape is available *because of* the
   quantifier, and [R-ENC-04]'s ceiling is named as a bound that binds anyway.

Reading B additionally requires ignoring L2's instance list, which [R-CNF-04]
makes a reader obligation; a "Verifier B" that certifies the 192-byte witness is
not a second permitted reading but a nonconforming verifier. Consensus PARTIAL:
the underlying observation — §19.3's enumeration of layer-access validation cites
"[R-GEO-01]–[R-GEO-03]" and "[R-ENC-06], [R-ENC-03]" but never [R-ENC-04] or
[R-SER-02]/[R-SER-07] — is accurate and worth repairing, but the claim that only
a Note decides the question is not. Severity editorial. Byte-level NO.

### G9 — [R-WRT-07] asserts a refusal its citation chain does not oblige
member: verifier-03

Chain verified. [R-WRT-09]: "the open (§19.1), each retained layer's record
(§19.3) and full index chain (`[R-IDX-04]`), and each relocated extent's
checksum, including every stored tile's entry crc". [R-RDR-03]'s §19.3 list ends
at "the index cross-checks computable without I/O (`[R-CNT-17]`)"; [R-IDX-04] is
crc_of_crc_array plus segment CRCs, both of which pass over an intact T6 entry;
and §15.3's structural rows "classify an entry whose own 20 bytes yield no usable
extent", so there is no relocated extent and no entry crc to verify. [R-IDX-03]
is nowhere in [R-WRT-09]'s list. So [R-WRT-07]'s "an entry §15.3 classifies
reject-tile on a structural ground never reaches this step, `[R-WRT-06]` having
obliged the compactor to refuse" is not reached by the citation given. CONFIRMED.

Byte-level: NO. §20.5 expressly permits the alternative outcome: "a violation
latent in a structure it carries forward verbatim travels into its output
(`[R-WRT-01]`)", and §20.3 step 2 permits the same for an appender — "a malformed
index entry an appender meets while re-emitting a region is carried forward
byte-identically at its disk-ordinal position under step 4, not repaired to a
sentinel." The carried-forward file is nonconforming under [R-IDX-03] on either
reading, and every reader rejects that tile. Emittable-by-another-actor: an
appender may lawfully produce a file carrying that same entry, so the byte
sequence is not one the reading adds to or removes from anyone's output set.
Severity design-decision: naming [R-IDX-03] in [R-WRT-09] closes it in one word.

### G10 — whether a verifier owes a check for every SHOULD
member: verifier-05

§2.3: "**Conforming verifier.** A reader that additionally checks every
file-level requirement — including those ordinary readers are exempted from — and
certifies conformance." [R-CNF-12]: "Deviation from a SHOULD is not a violation
for this purpose: §21's register enumerates MUST-level conditions only, and a
verifier reports a SHOULD deviation as an advisory that does not bar
certification." Neither sentence says whether a verifier must go looking. Under
BCP 14 as adopted by §2.1 a SHOULD is a requirement, so "every file-level
requirement" reaches them; the register, which §21.1 makes the operational
inventory, deliberately excludes them. Genuine under-determination. CONFIRMED.

Byte-level: NO — the rule states the answer itself: a SHOULD deviation "does not
bar certification", so both readings return the same verdict on every file and
differ only in advisory text. Severity design-decision. The reporter's own
[R-CNT-03] example is correctly self-resolved (§5.2: slack's "content is
unconstrained, and no conformance requirement applies to it").

### G11 — Appendix G never pins the filter
member: writer-03

Verified mechanically: `filter` does not occur anywhere in Appendix G
(lines 4088–4211). §17.3 assigns both values as core. Item 5 pins alignment and
slab because "both change placement and neither is implied by content"; the
filter changes every stored tile's bytes and is not implied by content, and item
1 already treats the codec choice as within scope. The closing paragraph does
claim completeness — "Everything else the profile needs is already mandatory" —
and that claim is false of the filter. CONFIRMED.

Byte-level: NO. Appendix G is "non-normative" in its own heading and says "It
adds no requirement to any actor: a writer ignoring it is fully conforming";
[R-CNF-01] excludes such appendices. Severity editorial.

### G12 — the compaction Example's caption contradicts [R-WRT-07]
member: diagrams-02

Verified that an index region is a record extent: §5.2 [R-CNT-02] — "a **structure**
— a stored-tile extent, a record extent (the bytes any record's extent slot
references, whatever the record's type, §7.2), the directory, or the trailer" —
and §9.7 — "A layer record's extent slot addresses that layer's tile-index region
(§7.4), so the region enters the walk once, as that record's extent". The figure's
only record extents are A: index and B: index, and both carry the ′ mark. So the
caption's leading clause ("every record extent survive byte-for-byte") is false of
every record extent in its own figure; the trailing clause states the correction.
CONFIRMED.

Byte-level: NO. [R-CNF-01] excludes text labeled *Example*, and [R-WRT-07]
normatively states the regeneration: "regenerates each relocated tile-index region
(entry offsets new; … segment CRCs recomputed over the entries as re-emitted)".
Severity figure.

### G13 — R3's "§21.6 governs" parenthetical
member: register-02

The reporter's reading (a) is refuted inside the same subsection, four lines above
the table: "Encoding 0 and a reserved-range value are unassigned too, and R1
registers both as violations: what `[R-MTA-10]` withdraws is the document's
content rules, never the encoding byte's own value set (`[R-MTA-03]`)." R1's own
cell registers "a document encoding of 0, or a reserved-range value (3-0x7F)".
R3's condition is expressly scoped to a "declared **assigned** encoding", so the
row never reaches encoding 0. The cell's shorthand is loose in isolation, but the
document decides it in three places and the reporter says so. PARTIAL — something
is worth tightening, but not the under-determination claimed. Byte-level NO;
severity editorial.

### G14 — §20.4's "the file's layer set"
member: writer-05

Neither reading is closed by the text. Against the reporter's parallel-construction
argument: §4.6 makes a layer's name its identity within the file — "Names are
unique within their scope: layer names among a file's" — so "the file's layer
set" can be read as the set of named layers, which a rename does change. Nothing
in §20.4, §20.3 or §7.4 settles it. CONFIRMED as a genuine under-determination.

Byte-level: NO. Both outputs are conforming files, and the drop-side output is
emittable by another actor on the same table's own terms: "A compactor may drop it
whenever it rewrites the file." No file-level witness distinguishes a record that
was dropped from one that was never written, as the reporter notes. Severity
design-decision.

## Coverage

33 input ids, 14 groups. Union of member_ids counted by hand against the input
list: reader-01..04 (4), writer-01..06 (6), verifier-01..05 (5), diagrams-01..05
(5), register-01..05 (5), adversary-01..05 (5), quiz-01..03 (3) = 33. No id in
two groups; no id omitted. Byte-level count: 0.

Downgrades made, each with the quotation that decides it: verifier-01 (L2's
unqualified instance list + [R-SER-07]'s "function of the layer's declarations
alone" + §20.3's "escapes only because that cap is quantified over addressed
tiles"), quiz-01 ([R-CNF-05] + §20.3's "makes each stored tile it reaches
nonconforming" + [R-SER-05]'s tile-scope validity error). Every other finding was
self-flagged not-byte-level and I concur, on the quotations recorded above.
