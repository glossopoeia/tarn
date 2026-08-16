# Round 9 triage — correctness lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in full, lines 1–3893
  (six reads: 1–400, 400–849, 849–1248, 1248–1648, 1648–2098, 2098–2548,
  2548–2997, 2997–3446, 3446–3893).
- `ls` of `/private/tmp/.../round9/`. I did **not** open any reporter
  transcript: every claim below is checked against `spec/tarn.md` itself, which
  is what the lens asks for. Where a reporter's quotation is verbatim I say so;
  where it is selective or wrong I say that instead.

I did not read `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`spec/registry.json`, git history, or the web.

**Could not evaluate:** `diagrams-01`. Its Location is `x`, title `y`, body `z`,
quote `q`, rationale `r`. There is no claim in it. Grouped alone, REFUTED,
severity none.

---

## Grouping decisions

30 groups over 41 ids. Rationale for the non-obvious merges and splits:

- **Merged** reader-01 + writer-02 + quiz-01 (Appendix G's closing paragraph
  claims gap *content* is added by an item; no item adds it). Same sentence,
  same missing item, same repair.
- **Split** that from verifier-06 + register-09, which attack the *opposite*
  direction: the closing paragraph's count of four is short of the freedoms the
  items actually close (item 6, item 8, item 3's top-level record order).
  Different repair (extend the list vs add an item), so different defect.
- **Merged** reader-02 + writer-04 + verifier-05 (item 2's file_id hash is
  unpinned). Identical.
- **Merged** reader-03 + register-01 + adversary-01. All three attack F1's
  Instances cell. reader-03 additionally attacks the `generation` instance;
  adversary-01 refutes that half. One cell, one defect; the generation
  sub-question is recorded in the action.
- **Split** register-04 out of that group: it is about *missing* L- and T-scope
  endianness rows, not about the version_major instance being present.
- **Merged** register-03 + adversary-02 (L47/L48/L50 collapse the
  layer-record/sub-record container dimension; 253 vs 257).
- **Split** quiz-03 from those: quiz-03 argues the cells *over*-enumerate
  against §21.1's single-predicate exclusion. Opposite claim, different rows
  (F32/L16/L23), different resolution.
- **Merged** writer-06 + register-05 (§21.7's account of witnessless
  obligations is not exhaustive). Different omissions, one incompleteness.
- **Split** verifier-01 from adversary-04. Both concern a compactor and a
  nonconforming input, but verifier-01 is about violations the compactor
  *cannot* detect ([R-WRT-06]'s flat "emits a new conforming file"), and
  adversary-04 about violations it *must* detect ([R-WRT-09]'s extent-checksum
  duty) with no stated response. Two sentences, two edits.
- **Merged** reader-05 + writer-08 + quiz-02 (field taxonomy: empty informative
  class; name fields undetermined).

Every other finding stands alone.

---

## Per-group checking

### 1. appg-gap-content — reader-01, writer-02, quiz-01 — CONFIRMED, editorial

Checked all nine items (lines 3770–3820) against the closing paragraph
(3822–3829). The closing paragraph is verbatim as quoted. No item mentions gap
content. Item 3's own words concede the point: *"Each structure begins where the
previous one ended, save where a declared alignment forces a gap: order alone
does not fix bytes while the space between structures is free."* Item 5 removes
declared alignments; item 7 promotes [R-TYP-10]'s SHOULD, and says so
explicitly (*"[R-TYP-10]'s SHOULD, taken as a requirement here"*) — which is the
phrasing the profile uses when it means to promote a SHOULD, and which item 3
does not use for [R-CNT-03].

The pad is unavoidable: [R-LIF-02] step 5 is *"append the pad to the next
64-byte boundary"*; §7.2 forbids residue in the record sequence, so no filler
record; §6.2 *"this specification does not constrain their content"*. Appendix
A's minimal file carries 44 pad bytes at [20,64). Confirmed.

writer-02's second point is separately correct and belongs here: the
user-metadata `encoding` field (§18.2: 1 = none, 2 = zstd) and the zstd encoder
under encoding 2 are unclosed freedoms no item addresses, so *"Everything else
the profile needs is already mandatory"* is false of them too.

**Byte-level: no.** Appendix G is headed *(non-normative)* and states *"It adds
no requirement to any actor: a writer ignoring it is fully conforming"*; §2.1
[R-CNF-01]: *"All text in this document is normative except: §1 (Introduction);
any text labeled Note, Example, or Rationale; and appendices identified as
non-normative."* And §5.2 [R-CNT-21] already decides the bytes: *"Slack has no
internal structure this specification defines, its content is unconstrained,
and no conformance requirement applies to it."*

### 2. appg-four-things-undercount — verifier-06, register-09 — CONFIRMED, editorial

Item 6 (sentinel every all-fill tile): nothing in the core obliges it —
[R-IDX-02]/[R-TYP-08] govern what an unstored tile *reads as*, not which tiles
must be unstored. Genuine freedom, not among the four. Confirmed.
Item 8 (version_minor at the floor): [R-CNT-26] is *"A writer SHOULD emit the
lowest version_minor that defines every feature present in the file"* — a fifth
advisory. Its `flags = 0` half is genuinely mandatory (§6.3: *"a writer creating
a file under this text MUST write flags = 0"*), so only the minor half counts.
Confirmed.
Item 3's top-level record order: [R-CNT-14] leaves both top-level and sub-record
order free (*"Record semantics MUST NOT depend on record order"*); the four name
only sub-record order. Confirmed.

Byte-level: no — same quotations as group 1.

### 3. appg-file-id-hash — reader-02, writer-04, verifier-05 — CONFIRMED, editorial

Item 2 verbatim at 3779–3787. It names no hash, no digest→u64 reduction, no
preimage serialization for "the trailer's other fields", and no fallback for a
zero digest against [R-CNT-06]'s `file_id ≠ 0`. Items 1 and 9 both close their
freedom by pinning a producer (*"a named codec implementation at a named
version"*, *"a named JSON writer at a named version"*); item 2 asserts
"Deterministic" flatly. reader-02 is additionally right that this falsifies item
1's boundary claim, *"codec 1 is reproducible by anyone"*.

verifier-05's two "residues" check out: the trailer CRC at [60,64) covers
[0,60), which contains file_id, so it cannot be a hash input; and F is fixed
before file_id is chosen, so the definition is not circular in F.

Byte-level: no — same quotations as group 1; [R-CNT-06] accepts any nonzero
file_id.

### 4. appg-emission-order — writer-03 — CONFIRMED, editorial

Item 3 verbatim. "ascending record order" is defined only as *"by type, and
within type 0x0001 by layer name"* and *"a layer record's sub-records are ordered
by type, and within a type by their order of creation"* — the latter scoped
*within one layer record*, so two layers' type-0x0002 sub-record extents have no
relative order. Confirmed. The "then any record extents" clause is grammatically
ambiguous between inside and outside the per-layer loop, and the outside reading
is the only one that places the top-level user-metadata extent. Confirmed.
"order of creation" is producer history, not a function of the input, so it
closes nothing; and in major 1 it is very nearly vacuous — §7.3 registers only
0x0001 and 0x0002, [R-CNT-14] permits at most one user-metadata sub-record per
layer, and §10.3 bars experimental values in released software.

Byte-level: no — same quotations as group 1.

### 5. f1-version-major-instance — reader-03, register-01, adversary-01 — CONFIRMED, register-bookkeeping

F1 verbatim (3042). §21.6's closing paragraph verbatim (3232–3248), including
*"Neither is a register row: the register enumerates file-conformance violations
(§21.1), and a file this document declines to judge is not one. What is
registered in each case is the neighbouring condition that is a violation —
version_major = 0 … (F20 …)."* §2.3 [R-CNF-02] verbatim.

Enumeration, checked independently: version_major is a `u16` whose only invalid
value is 0. BE(0) = LE(0) = `00 00`, so a byte-swapped 0 is F20 and nothing
else. BE(1) = `00 01` reads 256; BE(256) = `01 00` reads 1 and is
indistinguishable from a valid file. So the *only* distinguishable file the
version_major instance can produce is a trailer naming a major other than 1 —
exactly the case §21.6 excludes and §2.3 declines to judge. The instance is
either redundant with F20 or excluded by §21.6. **Defect confirmed.**

The `generation` half of reader-03 does **not** survive. adversary-01's
construction is right: a big-endian generation of 0x80 reads
0x8000000000000000 and trips F3's 2⁶³−1 gate, so the instance is constructible
— the vector builder simply picks a value that trips. reader-03's cited support
(§21.7 recording that the generation sequence has no single-file witness) is
about [R-LIF-03]'s *increment* property, not about the field's value, and does
not reach this. Recorded in the action.

**Byte-level: no.** The fork is a verifier's verdict *label*, not a byte.
Deciding text: §6.3 [R-CNT-07] — *"A reader MUST reject-file when version_major
is 0 (invalid) or is a major it does not implement"* — so every reader rejects
the file under both readings; and §2.3 [R-CNF-11] — *"a verifier MUST NOT
certify a file it reports that way"* — so neither *nonconforming* nor *cannot
establish* permits certification. No conforming writer of major 1 emits the
bytes under either reading. What does change is one register instance and one
corpus vector, which is register bookkeeping. register-01 concedes the reader
half itself: "the reader half of the test does not fork — both readers
reject-file". This was one of my three closest calls.

### 6. f1-missing-layer-tile-endianness-rows — register-04 — CONFIRMED, register-bookkeeping

Checked: [R-ENC-01]/[R-ENC-02] are cited by F1 and F2 only, both file-scope. The
parallel *width* family is registered at all three scopes with scope-qualified
condition text — F5 *"A fixed file-scope structure"*, L3 *"A field of a
layer-scope structure"*, T27 *"A tile-index entry"*. The endianness family is
not. A big-endian dimension extent is detectable: E=1024 BE reads
1,125,899,906,842,624, inside L1's domain, but the derived grid count makes
entry_count fail L22's cross-check (or L2's product gate). So the asymmetry is
real.

But reading (1) — that F1's scope-neutral condition text imposes reject-file on
a layer-scope occurrence — is **not** permitted. F1's own condition says
*"detectable only through that field's own value or range gate"*; the gate that
fires is L22's or L2's, and those rows carry the outcome. The document's
practice for cause-rows is explicit at F5 and T27: *"this row records the cause
rather than a procedure of its own"*. §21.1 closes it: *"where a row and the
rule it cites diverge, the rule governs"*, and [R-CNF-08] maps the layer
record's inline payload (§7.4: *"The owning scope of a layer record's inline
payload is the layer"*) to reject-layer.

**Byte-level: no** — no reader outcome forks, because F1 imposes no independent
procedure; the gates that actually fire (L2/L22) already assign reject-layer.

### 7. instance-count-containers — register-03, adversary-02 — CONFIRMED, register-bookkeeping

§21.1 verbatim: *"An instance names a field the condition ranges over, a
container it can occur in, one of several alternatives the condition text
states, or any combination of the three — a condition applying to two
alternatives in two containers has four."*

Cells checked against the tables: L16 = 4 (two fields × two containers), L17 = 2,
L18 = 2, L47 = 1 (`—`), L48 = 1 (`flags bits 2-15`), L50 = 2, F30 = 2
(`flags bit 0; flags bit 1`).

L47's predicate *is* a combination of two flag bits, so §21.1's exclusion
(*"where a condition is a single predicate over several fields — a sum against a
bound, a combination of two flag bits — the fields it reads are not
instances"*) correctly collapses the bits — but not the two containers, which
L17/L18 with identical grammar do split. L48's collapse of bits 2–15 matches
F28; its collapse of containers does not match L17/L18. L50 states a disjunction
("a stored MU **or** PE bit differing"), which F30 with one container correctly
counts as two alternatives; L50 with two containers should therefore be four.

253 + 1 (L47) + 1 (L48) + 2 (L50) = 257. Arithmetic confirmed.

**Byte-level: no.** §21.1 itself: *"The Instances column enumerates what a
conformance corpus builds for that row (§21.8): the row is the rule, and each
instance is one file."* And §24 [R-VEC-03]: *"A missing vector is a gap in the
corpus and never a licence to skip the check it would have exercised."* Every
missing file is nonconforming under the same row and the same governing rule.

Note the interaction with group 5: 253 − 1 + 4 = 256, not 252 and not 257.

### 8. instance-cells-field-labels — quiz-03 — PARTIAL, editorial

The reporter's premise misreads §21.1. The exclusion is expressly conditioned:
*"One instance is one distinguishable file: where a condition is a single
predicate over several fields … the fields it reads are not instances, **because
no two files could differ**."* For L16, two files *do* differ — one has
extent_offset 0, the other extent_length 0 — so the field names are labelling
alternatives the condition states, which §21.1 counts. Same for L23 (its
condition spells out the alternatives: *"including slot (0,0) with entry_count >
0, or a nonzero slot with entry_count = 0"*) and F32 (*"offset 0 with length !=
0, or offset != 0 with length 0"*).

So there is no violation of the rule. What survives is the reporter's own
closing suggestion, which is a fair editorial point: the cells label
alternatives with bare field names, which invites exactly this misreading.
PARTIAL: something small is wrong there, but not what the reporter said.

Byte-level: no — corpus construction only, same quotations as group 7.

### 9. outcome-header-gloss — register-02 — PARTIAL, editorial

The header claim is already resolved *in the same subsection*. §21.1: *"For a
row whose Detector is verifier, the outcome names the scope at which the damage
is recorded, not an obligation on any reader: the governing rule states what a
reader does, and for several such rows it obliges the reader to serve the
structure unchanged ([R-SER-08], [R-CNT-22])."* So reading (1) — that a reader
meeting a T2 tile must report failure — is not permitted. The reporter's
"contradiction" is refuted.

Two real residues, both confirmed:
- §21.1's parenthetical omits [R-MTA-05], which does the same work for F29/L49:
  *"unsorted members do not make a document unreadable … readers process the
  document unchanged."*
- §24 [R-VEC-04] genuinely mis-frames verifier-detected rows: *"a vector's
  expectation is therefore a pair: the scope no reader is permitted to serve,
  and the content a reader that serves anything at all owes."* For a T2 vector
  there is no scope no reader is permitted to serve — [R-SER-08] instructs a
  reader that serves it what to return.

**Byte-level: no.** [R-SER-08]: *"A reader that neither detects the violation
nor rejects the tile, and returns the value, MUST report 0x00 as false and every
other byte as true."* And [R-CNF-12]: *"a reader MAY reject it upon detecting
any violation, including violations whose assigned detector is the verifier."*
Both dispositions are already licensed for the same bytes.

### 10. sec217-incomplete — writer-06, register-05 — PARTIAL, editorial

Both omissions are real as stated: §21.7's second paragraph names only
[R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01] and [R-CNT-13]'s embedded-offsets
clause; the durability barriers, [R-WRT-05]–[R-WRT-09], and [R-CNT-18]'s nesting
prohibition are absent.

But §21.7 states its *class*, not its members: *"A second set of obligations is
omitted from the register because a single file exhibits no witness of their
violation."* Every omission both reporters name falls inside that class,
including [R-CNT-18]'s nesting prohibition (§7.4's Note: *"in format major 1 it
has no reader-detectable witness, and so no register row"*). And §21.1 assigns
§21.7 the role *"by class"* and explicitly withholds the completeness clause
from it: *"The subsections after §21.5 are not part of the register and carry no
rows: neither this completeness clause nor the instance arithmetic below reaches
§21.6's defined non-violations, §21.7's account of what no check detects, or
§21.9's limits."*

So the claimed incompleteness against a normative standard is refuted; the
illustrative list being inexhaustive is a fair editorial point. PARTIAL.

**Byte-level: no.** §21.7's own closing: *"no file-level witness exists to check,
so nothing about the file is left undetermined and the verdict is unaffected."*

### 11. sec219-hard-limits — verifier-04 — CONFIRMED, editorial

Checked §21.9's hard-limit list (3329–3346) against the sections. The 5-byte
user-metadata extent floor ([R-CNT-25]: *"one whose extent_length is less than 5
… is a validity error at its containing scope"*; rows F24, L12) has exactly the
shape of the listed *"a directory of at least 4 bytes at an offset of at least
16"* and is absent. [R-COD-06]'s window cap (*"MUST NOT declare a window size
exceeding the tile's decoded size; a reader MUST treat either as a validity
error at tile scope"*; row T21) is a validity bound paired inside §21.9's own
table with a minimum guarantee, exactly as the lz4 cap is, and is absent. The
closing accounting is written as exhaustive (*"Most follow from … One does
not"*). The reporter is also right that §21.1 holds §21.9 outside the register's
completeness clause, so [R-ERR-03] carries the claim alone. Confirmed.

**Byte-level: no.** §21.9 itself: *"They are stated where the structures forcing
them are defined"* — the operative statements are [R-COD-06] and [R-CNT-25],
both unambiguous in their own sections and both registered (T21, F24, L12). Two
implementations reading the whole document reject identically.

### 12. sec219-name-cap-rationale — register-07 — CONFIRMED, editorial

§4.6: *"Names — the strings that identify layers, dimensions, channels, and
user-metadata keys — satisfy three further constraints"*, one of which is *"at
most 255 bytes of UTF-8 (so every name's length prefix is a single byte)"*. A
JSON object key has no length prefix of any width; [R-MTA-04] imports the cap
(*"every key satisfying §4.6's name rules — non-empty, at most 255 bytes"*) and
R10 registers the violation. So §21.9's parenthetical *"([R-ENC-12], a u8 length
prefix)"* is false for keys, and *"One does not: the 512 floor on A"* undercounts
by one. §4.6's own parenthetical is likewise inaccurate for keys. Confirmed.

**Byte-level: no.** The cap is stated identically in §4.6, §18.2 and R10; only
the rationale sentence is wrong, and no implementation reads a rationale for a
bound.

### 13. sec211-no-identifier — register-08 — CONFIRMED, editorial

Verified: §21.1's only bracketed identifier is `[R-ERR-02]`, and [R-ERR-02] is
defined in §21.8 as the vector-coverage requirement. §21.1's own rules —
normative completeness, row-versus-rule precedence, finest-structure
attachment, specialization, and the instance arithmetic — carry none. §2.2:
*"Normative requirements carry identifiers of the form [R-<PREFIX>-<NN>]."* §1's
note: *"test vectors and conformance checklists cite identifiers, never prose
positions."* Confirmed.

Worth recording for the maintainer: this is not unique to §21.1. §6.1's
*"Writers MUST emit exactly these 16 bytes"* also carries no identifier of its
own. So the repair is a sweep, not one insertion.

**Byte-level: no.** §2.1 [R-CNF-01]: *"All text in this document is normative
except: §1 (Introduction); any text labeled Note, Example, or Rationale; and
appendices identified as non-normative."* §21.1 binds either way.

### 14. r1-citation — register-06 — CONFIRMED, register-bookkeeping

R1 registers *"a document encoding of 0, or a reserved-range value (3-0x7F)"*
citing only [R-CNT-25], which fixes the outcome and says nothing about validity:
*"An encoding value of 0, or one the reader does not implement, makes that
record unreadable, with the same outcome as a failed CRC — ignore-record, SHOULD
be reported."* The clause that makes reserved-range emission a violation is
[R-EXT-03]: *"a value from a reserved range MUST NOT be emitted at all before
this specification assigns it"*. The zero case is [R-MTA-03]'s *"0 is invalid"*.
Neither is cited. F38 and L26 do cite the rule that states the violation. So the
citation cell is doubly incomplete. Confirmed.

The reporter's further point about §2.3 citing "§10.3" undifferentiated is also
accurate: §10.3 carries a conduct clause (experimental values in released
software) and a bytes clause (reserved values at all), and §2.3's parenthetical
sweeps both under conduct.

**Byte-level: no.** Reader behaviour is ignore-record under every reading, and
§21.5's preamble already decides the validity question the other way: *"Every
row here is a violation all the same: the outcome bounds a reader's blast radius
and never makes the file conforming."*

### 15. field-taxonomy — reader-05, writer-08, quiz-02 — CONFIRMED, editorial

Checked every layout table with a Class column — §6.1, §6.2, §7.2, §15.1, §18.2.
Classes used: structural, structural (reserved), and semantic (generation,
file_id in §6.2; fill declared semantic in §13.1). **No cell reads informative.**
So [R-ENC-16]'s second clause (*"each informative field's definition states what
a reader does when it contradicts the data it describes"*) has no subject in
format major 1, and §1's rubric advertises a class the document never uses.
Confirmed.

quiz-02's disjointness point is also correct as stated: §1's rubric gives
semantic as *"affects what decoded values mean"* and informative as *"never
affects decoding"*, and §13.1 says of fill — a semantic field — *"it affects what
unstored samples read as, never how any byte is located or decoded"*. So every
semantic field satisfies the informative definition; the two are not disjoint as
written.

The name-field question is real but its source is a **Note**: *"its table omits
the offset and class columns, and each field's class follows from the
definitions above"* — non-normative under [R-CNF-01].

**Byte-level: no.** [R-ENC-16] is the only rule keyed to the taxonomy, and it
binds only the informative class: *"A field classified informative MUST NOT
affect how any byte is located or decoded, and a reader MUST NOT alter decoding
based on it."* No register row keys off a field's class. Whichever label a name
carries, identical bytes are located, decoded and emitted.

### 16. layer-record-drop — writer-01 — PARTIAL, design-decision (byte-level flag downgraded)

The reporter flagged this byte-level. I checked §2.3's wording character by
character:

> "An updater MUST satisfy every writer requirement for the bytes it produces,
> and additionally MUST honor the preservation obligations of Part I for records
> it does not understand. `[R-CNF-06]`"

This is **additive**, not exhaustive. It adds an obligation for records the
updater does not understand; it nowhere says preservation is *confined* to them,
and it grants no permission to drop anything. The permission the reporter needs
does not exist in this sentence.

§20.4 supplies the rule and is unambiguous:

> "Persistence governs every record type; only the authoritative source of the
> flags differs. For a type §7.3 registers, the registry's fixed flags govern
> rather than the stored ones (`[R-CNT-22]`) — both registered types carry
> PE = 1, so neither can be dropped, and implementing a record's type confers
> understanding of it, not permission to drop it."

"Persistence governs every record type" and "neither can be dropped" close it.
There is no escape via [R-WRT-05] either — a dropped record is neither retained
nor logically modified. §20.5 closes the compactor route: *"less any record §20.4
lets it drop"*, and §20.4 lets a compactor drop only its MU = 0 / PE = 0 row.

So the **contradiction is refuted**. Two real defects survive:
1. §2.3 mis-locates the rule: it cites *"the preservation obligations of Part
   I"* while §20.4, which states them, is Part III. §20.1 [R-WRT-01] gets it
   right (*"the preservation obligations of §20.4"*), and §2.4's preserve-verbatim
   row points at §20.4 too.
2. The consequence — that **no defined operation removes a layer from a TARN
   file** — is nowhere stated, though it is a striking property of the format
   and the natural question an updater implementer asks. §20.4's MU = 0 / PE = 0
   row even speaks of a commit that changes *"the file's layer set"*, which
   reads as though removal were on the table.

**Byte-level: no**, on the §20.4 quotation above: the document decides which
directories a conforming updater may emit, so no two conforming updaters
diverge.

### 17. tile-vs-window-guarantee — writer-05 — CONFIRMED, editorial

Arithmetic checked. §21.9 guarantees a 256 MiB decoded tile and an 8 MiB zstd
`Window_Size`. §17.2's Note: *"with Single_Segment_Flag set there is no
Window_Descriptor and Window_Size is the frame content size, which this
requirement already obliges to equal the decoded size."* So a 64 MiB tile in a
single-segment frame has a 64 MiB window, and [R-ERR-03]'s duty — *"any
conforming file whose quantities lie within these bounds"*, conjunctive — is not
engaged. The trap is real.

**Byte-level: no.** §17.2 states the resolution in terms: *"Writers SHOULD keep
the declared window within §21.9's 8 MiB Window_Size guarantee even for a larger
tile; a wider window is conforming and merely permits a conforming reader to
decline the tile or the layer on resource grounds ([R-ERR-04])."* Conformance
status and reader licence are both fixed; what is wrong is that this sits two
sections away from the table row it conditions.

### 18. compactor-index-regen-trigger — writer-07 — PARTIAL, editorial

[R-WRT-07]'s trigger phrase is *"regenerates each relocated tile-index region"*,
and its parenthetical is about the *entries'* offsets (*"entry offsets new"*).
The reporter's scenario — region stays put, tiles move — is constructible.

Reading (ii) is nevertheless not a permitted reading of the requirement, because
the same requirement and its neighbour forbid its output: [R-WRT-06] *"A
compactor emits a new conforming file"*, and [R-WRT-07]'s own closing *"The
output's reference arrays MUST equal the live generation's bit for bit
([R-MDL-02]): compaction changes where bytes live, never what a layer
denotes."* A region whose entries address bytes the output no longer holds fails
T1 and [R-MDL-02].

So the ambiguity is refuted; the mis-keyed trigger phrase is a real editorial
defect, and the reporter's one-word fix is right.

**Byte-level: no**, on the two quotations above: no two *conforming* outputs
differ.

### 19. slab-trigger-omits-sentinel-fill — writer-09 — CONFIRMED, editorial

[R-SLB-04]'s trigger is *"supersedes a stored tile in, or grows the extents of"*.
A commit turning a sentinel entry into a stored tile does neither, yet changes
the run's stored-tile set and can break [R-SLB-03]'s packing relation or its
A_slab alignment. §13's Note recommends exactly that workflow (*"Declare-then-fill
workflows append tiles as data arrives, generation by generation"*), and §11.1's
Rationale describes schema-first layers grown from empty. Under-inclusive
trigger confirmed.

**Byte-level: no.** [R-SLB-03] is a standing invariant on the live state that a
verifier checks every generation — *"A verifier MUST check these invariants
(violation: reject-layer, §15.3)"* — so file validity is decided regardless of
which commit produced the state. §20.3 step 4 states the writer's duty without
the restrictive trigger anyway: *"a slab declaration is re-established or cleared
([R-SLB-04])"*.

### 20. appender-index-relocation-keyword — writer-10 — PARTIAL, editorial

Both sentences are declarative, as reported: §20.3 *"relocating a live index
region is compaction's operation (§20.5, [R-WRT-07]), not an appender's"*; §5.1
*"A commit never relocates a live index region otherwise."*

Reading (ii) — that the document merely declines to describe the operation — is
refuted by §2.1 [R-CNF-01]: *"All text in this document is normative except: §1
(Introduction); any text labeled Note, Example, or Rationale; and appendices
identified as non-normative."* §20.3's sentence is normative body text, and §5.1
states it as a flat negative ("never"). The document uses declarative normative
statements elsewhere for exactly this purpose — [R-CNT-05]'s *"no conforming
commit produces one"*.

Real residue: the prohibition carries no BCP 14 keyword, in a requirement whose
surrounding text is written in MUSTs, and §2.1's Note claims a phrasing
discipline the sentence does not meet. Editorial.

**Byte-level: no**, on the quotation above plus the fact that both readings
yield a conforming output file.

### 21. compactor-conforming-output-claim — verifier-01 — CONFIRMED, design-decision

The collision is real. [R-WRT-09]'s enumerated depth — *"the open (§19.1), each
retained layer's record (§19.3) and full index chain ([R-IDX-04]), and each
relocated extent's checksum, including every stored tile's entry crc"* — does not
include decoding, so a T2 or T4 content violation is not detected. [R-WRT-07]
requires *"every stored tile's bytes verbatim"*. [R-WRT-06] then states flatly
*"A compactor emits a new conforming file"*, which the output is not.

§20.1 supplies the resolution in principle, and it is the distinction the
reporter overlooked: *"An appender and a compactor satisfy every writer
requirement for **the bytes they produce** and the preservation obligations of
§20.4 for **what they carry forward** … a violation latent in a structure they
neither modify nor rely on travels with it, and certifying the whole file is a
verifier's office (§9.7)."* A copied tile is carried forward, not produced, so
[R-WRT-09]'s structural reliance does not make the escape empty. What remains
defective is [R-WRT-06]'s unqualified "conforming file", which §20.1 contradicts
on its face.

**Byte-level: no.** [R-WRT-07] fixes the tile bytes verbatim, so both readings
emit identical bytes when they emit at all, and the output is nonconforming
under both. §20.1's sentence above decides the actor question.

### 22. compactor-detected-violation-unstated — adversary-04 — CONFIRMED, design-decision

Traced the chain independently. [R-WRT-09] obliges verification of *"each
relocated extent's checksum"* before emitting. §8.1 gives a user-metadata extent
a checksum. On failure, [R-CNT-20] gives ignore-record and §21.5 R2 makes the
input nonconforming. The compactor then cannot drop (§20.4: *"both registered
types carry PE = 1, so neither can be dropped"* — user metadata is 0x0002,
PE = 1), cannot re-emit corrected ([R-WRT-05]: byte-identical for records it
retains and does not logically modify), and cannot emit ([R-CNF-05]: *"A writer
MUST emit only conforming files"*). Refusal is the only surviving move and is
licensed only indirectly, through [R-CNF-12] plus §20.1's *"are readers of every
structure they process"*. Nothing states it. Confirmed.

The same silence covers a stored tile whose entry crc fails.

**Byte-level: no.** The reporter is right that it converges: any compactor that
emits rather than refusing produces a file exhibiting R2 and is not a conforming
writer under [R-CNF-05]. The cost is the five-requirement derivation, not the
answer.

### 23. partial-slack-total-regions — verifier-02 — PARTIAL, editorial

"Region" is genuinely undefined as a unit of the walk: elsewhere the document
uses it for the *directory region* (§7.1) and the *tile-index region* (§15.1),
both claimants. And the second obligation — *"MUST also name the regions it did
not walk and report their byte extent"* — is hardest to satisfy in exactly the
case that produces it, since a broken checksum chain is what denies the verifier
the extents. Both points stand.

The comparability worry does not. §22.3 decides it: *"a verifier that stopped
early reports it only as partial ([R-CNT-21]), so the distinguishing figure
comes from a walk that completes."* And §5.2's Note: *"A partial total
([R-CNT-21]) reports what one verifier's incomplete walk left unclaimed, which
is a fact about that run and not about the file's live state."* Divergent partial
totals are by design.

**Byte-level: no**, on those two quotations; every reading yields nonconforming
on the same file and bars certification identically.

### 24. verifier-traversal-past-capability-refusal — verifier-03 — PARTIAL, design-decision

Real gap: §2.3's only stopping licence is *"A verifier MAY stop at the first
violation it finds"*, and a capability-ground refusal is not a violation, so
neither the licence nor its accompanying *unexamined* reporting duty reaches the
case. Nothing states how far a verifier traverses past one. Confirmed as a gap.

But the *file's* status is decided, which is what the reporter's framing
obscures. §2.3: *"File conformance is a pure predicate on bytes: it does not
depend on any reader, writer, or environment."* The file in the reporter's
construction carries L34 and is nonconforming, full stop — so [R-VEC-02]'s
manifest question ("whether the file is conforming") has a unique answer, and
the reporter's claim that it cannot be stated is wrong.

**Byte-level: no.** Both verdicts bar certification — [R-CNF-11]: *"a verifier
MUST NOT certify a file it reports that way"* — and *"cannot establish is not a
finding that the file is nonconforming"*, so neither verdict asserts anything
about the bytes that the other denies. Second of my three closest calls.

### 25. ignored-record-extent-in-walk — adversary-05 — PARTIAL, editorial

Reading (b) is foreclosed, in four places the reporter itself names and I
verified: §5.2 [R-CNT-02] *"a record extent (the bytes any record's extent slot
references, **whatever the record's type**, §7.2)"*; §9.7's walk *"its records and
their sub-records, each record's extent"* with no exception; §8.1's map giving
*"Extent of a record of a type this specification has not assigned"* its own row;
§22.3's *"carries such an extent forward unread"*. And §2.4 disclaims the
governing role the reporter says its table invites: *"the outcome classes
describe the blast radius of a violation for readers, never degrees of file
conformance"*.

So no ambiguity survives. What survives is the reporter's own framing — the
table *invites* the error — which is a fair editorial nudge on one table cell.
PARTIAL.

**Byte-level: no**, on [R-CNT-02]'s "whatever the record's type".

### 26. t14-sentinel-qualifier — adversary-03 — CONFIRMED, register-bookkeeping

Cell text checked against neighbours: T8, T9, T10, T11 and T12 each say
*"non-sentinel"* explicitly; T14 does not. A sentinel's length field is 2⁶⁴−1 and
differs from every decoded size, so T14 read literally condemns every sparse
codec-1 layer. The cell is genuinely under-qualified. Confirmed; the practical
hazard is high, since that is the most ordinary sparse layer in the format.

**Byte-level: no.** Four independent texts foreclose the strict reading:
[R-IDX-02] *"Sentinel entries are a reserved pattern, not offsets or lengths"*;
§3.1 *"A tile is stored in a generation if and only if that generation's
tile-index entry for it is not the sentinel"*, so [R-COD-04]'s premise (*"The
stored bytes are the filtered image verbatim"*) does not obtain; §19.4 step 4
*"A valid sentinel short-circuits steps 5 and 6 for that entry"*; and §21.6's
non-violation row *"An index entry is the sentinel | The tile is addressed but
not stored"*. §21.1's *"where a row and the rule it cites diverge, the rule
governs"* directs the reader to [R-COD-04], which the first two quotations then
close.

### 27. binary64-finiteness-pinning — adversary-06 — PARTIAL, editorial

The indeterminacy claim is refuted by the bullet's own words. [R-MTA-04]: *"A
document is unreadable if it contains a number whose **binary64 interpretation**
is not finite"* — the test names binary64 explicitly, so a reader using a wider
representation still applies the binary64 test. §2.3 confirms: *"File
conformance is a pure predicate on bytes: it does not depend on any reader,
writer, or environment."* And Appendix F carries [IEEE 754] IEEE 754-2019
normatively.

What survives is the reporter's own second point, and it is real: *"A reader
interprets every JSON number as an IEEE 754 binary64 value and MAY use a wider
representation"* sits immediately before the test and reads as licensing a wider
finiteness test. Nothing says the pinning outlives the permission. One clause
fixes it.

**Byte-level: no**, on the two quotations above.

### 28. front-block-residency — reader-04 — CONFIRMED, editorial

The defect is in the dash-list, not where the reporter puts it. [R-CNT-04]'s
operative subject is *"A reader whose open leaves bytes [0, 16) resident"*, and
its dash-list then names *"a local file"* — which is a **transport**
classification, not a property of an open path. The very next sentence disclaims
that: *"The test is residency, not transport, so an implementation decides it at
its own open path without having to classify the network underneath it."* §6.1
independently defines *"a local file or a memory mapping"* as the ordinary cases
of a *transport*, which is what makes the list item a category error.

So the document decides for reading (a): a pread-only local open does not leave
[0,16) resident and the obligation does not bind. F8's Instances cell glosses it
the same way and in wider vocabulary than the escape clause's: *"the obligation
binds a reader holding those bytes resident, and a reader that **would have to
fetch them** MAY defer or omit the check ([R-CNT-04])"* — "fetch", not "range
request", which covers a local pread.

**Byte-level: no**, on those two quotations. But I record for the maintainer
that this is the third of my three closest calls: under the misreading the list
item invites, a local pread reader would be *obliged* to reject a byte sequence
it is otherwise free to serve, so the repair is worth prioritising even though
the text as written decides it.

### 29. overlong-pretrailer-pad — quiz-04 — REFUTED, none

[R-CNF-02]'s generalising clause is the whole subject of the sentence, not an
appendix to the examples: *"**A writer obligation whose violation this
specification expressly declares not to be a file-conformance violation** —
§6.3's flags = 0 against a set ignore-lane bit — binds the actor in the same
way."* [R-CNT-05]'s *"a longer gap is conforming, and no conforming commit
produces one"* is exactly such an express declaration, so the general clause
catches it. The competing "exhaustive list" reading requires ignoring the
subject clause against its own em-dash example, and §21.2's having F9 (a
*structure* in the gap) and no row for an over-long empty pad corroborates.
The reporter reached this conclusion itself. No edit required.

**Byte-level: no**, on the quotation above.

### 30. null-finding — diagrams-01 — REFUTED, none

Placeholder text throughout (`x`, `y`, `z`, `q`, `r`). Nothing to evaluate.
Recorded as an input the reporter did not fill in, not as a judgement about the
document.

---

## Closing arithmetic

- 41 input ids, 30 groups, each id in exactly one group. Counted twice by hand:
  3+2+3+1+3+1+2+1+1+2+1+1+1+1+3+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1 = 41.
- Byte-level upheld: **0**. Every reporter byte-level flag (writer-01,
  register-01, adversary-01) downgraded, each with the deciding sentence quoted
  above.
- Closest calls, in order: group 5 (F1's version_major instance), group 28
  (residency), group 24 (verifier traversal). All three fork a verifier's
  verdict label or an implementation's self-classification, none forks what may
  be emitted or must be accepted or rejected.
- Cross-group arithmetic the maintainer needs: group 5 removes one instance and
  group 7 adds four, so the corrected §21.8 total is **256**, not 252 and not
  257.
