# Cleanroom round 31 — Register hunter transcript

Charter: §21, the error-handling register, against the rules it restates and
against itself. Row-versus-rule agreement; completeness in both directions;
every cross-reference to a row; the counting; the outcome vocabulary; the
limits.

## 0. Access disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
I read it in five chunks (lines 95–450, 440–1000, 999–1519, 1518–2078,
2078–2609, 2609–3079, 3078–3613, 3610–4100, 4093–4493, 4492–4791) plus the
register itself first (3610–4100). I did not read `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, or any web resource. I did not list any
directory. I did not read the output directory this transcript goes to.

Context I did not ask for: my runtime placed a project instruction file
(`CLAUDE.md` pointing at `AGENTS.md`) and an index of the maintainer's memory
notes into my context before I began. I did not open any of the files those
name, and I have not used their contents as evidence about the specification.
I note their appearance here as the brief requires and do not repeat their
contents. The spec file was exactly where the brief said it would be.

Scratch files I wrote, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/register/`:
`count_inst.py`, `xref.py`, `cols.py`, `crc32c_check.py`. Several one-off
scripts were run as heredocs to `python3 -` from the spec directory and left no
file. No file was written anywhere else except this transcript.

## 1. First pass: the counting

§21.1's instance arithmetic is mechanical once a cell is written: "Instances
within a cell are separated by semicolons, and a cell reading — is one
instance; the count is therefore mechanical once the cell is written." So I
parsed the four register tables directly (`count_inst.py`), splitting the
Instances column on `;` and treating an em-dash cell as one.

Rows per subsection:

| subsection | rows counted | rows stated |
|---|---|---|
| §21.2 file scope | 35 (F1–F10, F12–F36; F11 struck) | 35 |
| §21.3 layer scope | 49 (L1–L49) | 49 |
| §21.4 tile scope | 26 (T1–T26) | 26 |
| §21.5 ignored records | 10 (R1–R10) | 10 |
| **total** | **120** | — |

Instances per subsection: F 56, L 116, T 55, R 50. **Total 277.**

§21.8 states "120 conditions over 277 instances". Both figures reproduce
exactly, and each subsection heading's condition count reproduces. I checked
for semicolons inside parentheses that could inflate the split — L2's
`planar C·N (which dominates the max disk ordinal (C−1)·N + (N−1))`, L23's
`trailing fixed fields (index_encoding, entry_count, crc_of_crc_array)`,
F1/F6's `bytes [0,8)` — none contains a semicolon, so the naive split is
right. The largest cells are R4 (16 = 8 frame constraints × 2 containers),
L2 (9), L1 (8), R5 (8).

I then re-derived a sample of cells from §21.1's own two stated axes rather
than trusting the split:

- **Magnitude direction.** "Where the condition compares two magnitudes either
  of which can be the greater — a *differs from* or *does not equal* — the two
  directions are likewise enumerated; where its own text bounds the comparison
  in one direction — an *exceeds*, a *larger than* — there is one." Checked
  against F17 (2), L21 (4), L22 (4), L30 (2), T3 (6), T14 (6), T22 (6), R4's
  content-size pair (4 of its 16) — all enumerate both directions. Checked
  against F10, F32, L17, T9, L44, T21, F2, F3, L1, L2, T11, T12, F5, F9, F16,
  F22, T24 — all one direction, all one-directional in their own text.
- **No magnitude ordering.** F14, F20, L37, L38, T1, R2 are checksum
  comparisons and enumerate no direction; F1, F6, F8, T17, T23 are
  pattern-against-constant. F13, L40, L42 are "not a multiple of" and likewise
  enumerate none. All consistent with "a stored checksum against a computed
  one, or a byte pattern against a constant, is equal or it is not".
- **Nonzero value tests.** L20 ("A ≠ 0 and S ≠ 0") is one instance, matching
  "a field tested only for being nonzero — an *A ≠ 0*, an *S ≠ 0* — which is a
  value test and not a comparison of two quantities at all" and "a combination
  of two flag bits — the fields it reads are not instances".
- **Layout-varying quantities.** "Where the quantity a condition derives varies
  by layout, the layout formulas are materially different shapes and the cell
  enumerates them." L2, L21, L44, T3, T4, T14, T21, T22, T26 all enumerate
  layout formulas. T5 does not, correctly — it exists only in a packed planar
  bool plane.
- **Families stated as one instance.** T24's "any codec" and F19's "flags bits
  0-15" and F26's "flags bits 2-15" are single instances; T15 and T25 enumerate
  because their members give the condition different shapes. Exactly §21.1's
  worked examples.

One asymmetry I opened and closed: F26 gives reserved flag bits 2–15 as one
instance while F28 gives bits 0 and 1 as two. That is right: bits 2–15 all
carry the same condition (be zero), whereas bit 0 and bit 1 carry different
registry-fixed values (MU = 0, PE = 1 for type 0x0002) and so are materially
different shapes.

A second I opened and closed: L22 lists four instances two of which are subsets
of the other two — "a nonzero slot with entry_count = 0" is an
`extent_length larger` case, and "slot (0,0) with entry_count > 0" is an
`extent_length smaller` case. §21.1's arithmetic does not forbid overlap, only
indistinguishability ("One instance is one *distinguishable* file"), and these
are distinguishable files. The cost is two extra corpus vectors at a boundary
worth pinning. Not a defect.

## 2. Row-versus-rule agreement

I walked all 120 rows against their governing requirements, comparing four
attributes: wording, outcome class, scope, detector. `cols.py` tabulated the
Detector, Detected and Governing-rule cells so I could check them as sets.

**Detector.** Exactly two values appear: `reader` (100 rows) and `verifier`
(20 rows: F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46, L47,
L48, L49, T2, T4, T5, T26). Every verifier row is backed by an explicit
verifier obligation in its rule — [R-CNT-05] "A verifier MUST treat a structure
in that gap"; [R-CNT-12] "a verifier MUST treat a nonzero reserved flag bit or
the MU = 1 with PE = 0 combination"; [R-MTA-05] "a verifier MUST report it";
[R-CNT-22] "a verifier MUST treat the mismatch"; [R-CNT-13] "a verifier MUST
treat an intra-layer overlap ... (readers are not obligated to detect overlap)";
[R-CNT-15] "a verifier MUST treat a reserved-range record type"; [R-SLB-01] "A
verifier MUST check the invariant ...; readers are not obligated to";
[R-SLB-03] "A verifier MUST check these invariants"; [R-SER-08] "its assigned
detector is the verifier"; [R-SER-05] "a verifier MUST check it"; [R-COD-10] "a
verifier detects it as a validity error at tile scope". No verifier row is
assigned to a reader-obliged check and no reader row is assigned to a
verifier-only check. F33/L18 and L40/L41/L42 correctly carry `verifier` where
their rules say readers are not obligated.

**Detected.** Values are exactly §19.2's four reader tiers plus `certification`.
Every one of the 20 verifier rows carries `certification`; no reader row does.
Two cells are split rather than single: L23 ("open (the name field, §19.1 step
4); layer access (every other field and entry)") and R1 ("open (top-level);
layer access (sub-record)"). Both splits are licensed by their rules — §19.1
step 4 places the layer-record name parse at the open and says a name field
that does not lie within inline_length "is instead a validity error at layer
scope ([R-CNT-18])", which is L23; and a top-level user-metadata record's
encoding byte is resident in the directory at the open while a sub-record's is
not reached until layer access.

**Outcome class and scope.** I checked each row's subsection outcome against
the scope its rule assigns:

- Every §21.2 row resolves to file scope. F4 by [R-ENC-15]'s express "a
  duplicate layer name is a file-scope error (reject-file)"; F21/F22/F23 by
  "the record's containing scope", which for a top-level record is the file;
  F25/F26/F28/F36 by "the record's governing scope", which §7.2 fixes as "the
  file for other top-level records"; F27 by [R-MTA-02]'s "The owning scope of a
  user-metadata record is the file when the record is top-level"; F33 by
  [R-CNT-13]'s "any overlap across layers or touching another scope's
  structures as reject-file".
- Every §21.3 row resolves to layer scope. L3/L5/L6 through §7.4's "The owning
  scope of a layer record's inline payload is the layer"; L15–L17 through
  [R-CNT-13]'s "the layer for a layer record and for sub-records"; L37/L38
  through [R-IDX-04]'s "reject-layer", which §19.2 confirms takes layer scope
  though detected at tile use.
- Every §21.4 row resolves to tile scope. T13, T15, T16 and T23 have governing
  rules that state no outcome of their own; each resolves through §17's "the
  owning scope of one stored tile's payload under them is the tile", and each
  row says which registered check detects it (T25's, T24's).
- Every §21.5 row is ignore-record by [R-CNT-25]'s express assignment, which
  §21.1 names as the exception to scope-determined outcome: "except where a
  rule assigns one expressly, as [R-CNT-25]'s quarantine does for every §21.5
  row, whatever the containing scope". R2 additionally has [R-CNT-20]'s own "a
  user-metadata extent's CRC → ignore-record", and R4 has [R-MTA-09]'s "Any
  violation here is ignore-record, never the tile-scope outcome §17.2 assigns".

**Two rules that state several conditions.** I checked §2.3's arithmetic claim
that "[R-CNT-06] states nine". Counting the register rows whose Governing rule
is `[R-CNT-06]`: F8, F9, F10, F12, F13, F14, F15, F16, F17 — nine exactly. The
version gate and flag gates that [R-CNT-06] also names are delegated to
[R-CNT-07] and [R-CNT-08], which is why F18 and F19 cite those instead. §2.3
then says "the trailer magic and the trailer CRC assert invariants [R-CNT-24]
fixes and the other seven do not" — F8 and F14, leaving F9, F10, F12, F13, F15,
F16, F17: seven. That reproduces. §21.2's preamble says deriving reach yields
"F8, F14, F6 and both of F1's instances ... and no other row"; I checked
[R-CNT-24]'s three fixed invariants (magic at F−64, version fields at F−56,
CRC at F−4) plus §6.1's constant block against every row and found no other
candidate. The flags field sits at trailer offset 12 = F−52, inside the 48
bytes [R-CNT-24] lets a future major redefine, so F19 correctly does not reach.

**§15.3's classification table against §21.4.** I enumerated §15.3's eleven
rows and paired each with a register row: sentinel-with-crc≠0 → T6; exactly one
of offset/length sentinel → T7; length = 0 → T10; offset < 16 → T8; offset or
length > 2⁶³−1 → T11; overflowing sum → T12; extent past F−64 → T9; stored
bytes fail crc → T1; intra-layer overlap → L18; overlap outside the layer →
F33; alignment/slab invariant → L40/L41/L42. Complete in both directions.

**§18.2's four decoded-document restrictions against §21.5.** Object/unmarked →
R7; finite numbers → R8; no duplicate keys → R9; well-formed UTF-8 throughout
plus §4.6's name rules on keys → R5 (ill-formed source bytes and unpaired-
surrogate escapes), R6 (empty key, C0 code point), R10 (key over 255 bytes).
Complete. R10's existence beside L5–L8 is exactly right: a layer, dimension or
channel name cannot exceed 255 bytes because its length prefix is a `u8`, so no
file can exhibit that condition and no row exists for it; a user-metadata key
"carr[ies] no such prefix", so it can, and R10 registers it. This is the
sharpest single piece of internal consistency I checked.

**§18.2's carried-over frame constraints against R4.** §18.2 carries over from
[R-COD-06] the frame magic, no skippable frame, no second frame, no dictionary
use disclosed or not, no nonzero dictionary ID, no content-checksum flag, and
the bar on sizing a buffer from a declared length; it replaces the decoded-size
and Window_Size constraints and pins the content-size field to the decoded
document's byte length; and it adds the single frame occupying the extent's
bytes before the terminal CRC. That is eight conditions a file can exhibit
(magic, skippable, second frame, dictionary ID, checksum flag, trailing bytes,
content-size larger, content-size smaller) and two that fall out — undisclosed
dictionary use as unwitnessed, buffer sizing as no condition a file can exhibit.
R4 enumerates exactly those eight over two containers: 16. The two omissions are
named in §18.2 itself as "Two of those fall outside the register, on the two
distinct grounds §21.7 separates, and R4 registers neither". Exact.

## 3. Completeness, both directions

**Direction one: is anything detectable and unregistered?** I ran a
whitespace-normalised sweep for `validity error` (52 hits) and read every one
in context, pairing it with a row or with the document's own stated reason for
having none. The ones with no row all carry that reason:

- [R-ENC-06]'s field widths — §21.7's closing paragraph: "not a state a file
  can be in ... Nothing is omitted from the register on its account".
- [R-CNT-18]'s nesting prohibition — §7.4's Note: "in format major 1 it has no
  reader-detectable witness, and so no register row", with the one detectable
  case (a layer record as a sub-record) registered as L26.
- [R-SLB-04]'s stale slab declaration — §16.2's Note: "a stale declaration
  carries no register row of its own: every file exhibiting one exhibits a run
  whose tiles are unpacked or whose first stored tile is misaligned, which
  §21.3 registers" (L41, L42).
- [R-CNT-02]'s "belongs to no class" half — §5.2's Note: "a register row for it
  would be a row no file could exhibit".
- Residue past a completed commit — §9.5's Note: "carries no register row of
  its own ... each of which §21.2 already registers" (F8, F14, F17).
- Undisclosed dictionary use, wrong sample content, a mis-strided filter with no
  structural consequence — §21.7's unwitnessed class.

I also walked every requirement identifier's writer-side prohibition looking for
one with no row and no stated reason. [R-ENC-11]/[R-ENC-12]/[R-ENC-15] over the
four string kinds → L3/L4, L5/L7, L6/L8, F4/L9, R5, R6, R9, R10 (complete, per
above). [R-IDX-05]'s "a partial segment's CRC MUST be computed" → L38, whose
condition text names the case explicitly ("a partial segment covers only its
actual bytes, and the all-sentinel constant 0xEECB3BB2 never substitutes for
comparison"). [R-CNT-08]'s "flags = 0" → F19 for the incompat lane; the ignore
lane is expressly not a file-conformance violation ([R-CNT-08] itself, and
[R-CNF-02] naming it) and §21.6 records it. [R-CNT-05] → F7. [R-CNT-22] → F28,
L49. [R-CNT-12]'s two writer bars → F25/F26, L46/L47. [R-MTA-05] → F27, L48.
[R-COD-*] → T13–T26 and L43/L44/L45. [R-SER-05] → T4 (four padding-position
shapes) and T5 (pad bits), which between them cover [R-SER-05]'s five stated
alternatives. [R-SER-08] → T2 for real positions and T4 for padding positions,
which T2's own text asserts ("the two rows together covering [R-SER-08]") and
which I verified: a padding-position bool byte other than 0x00/0x01 necessarily
also fails to be the recorded fill, since [R-TYP-07] confines a bool fill byte
to 0x00 or 0x01.

I found no detectable file-conformance violation the register omits.

**Direction two: does a row register something the rules do not make a
violation?** I checked each row's rule for an output-level (not conduct-level)
prohibition. The interesting cases:

- L31/L33/L34/L36/L43/L45 register *experimental*-range values as violations,
  whereas F36/L25 and R1 register only *reserved*-range values (experimental
  record types and metadata encodings being conforming). That asymmetry is real
  and correct: [R-COD-03], [R-GEO-05], [R-TYP-03], [R-SER-06], [R-COD-09] and
  §7.4's index_encoding row each carry an *output* prohibition ("Writers MUST
  NOT emit a codec value other than 1 through 4"), while [R-CNT-15] and
  [R-MTA-03] do not, and §10.3's experimental prohibition is expressly conduct
  ([R-CNF-02]: "where a value is published ... (§10.3, §18.3)"). [R-EXT-03]
  states the three-way split explicitly.
- F19 registers a set incompat-lane bit. [R-CNT-08]'s carve-out ("but a set
  ignore-lane bit is not a file-conformance violation") reaches only the ignore
  lane, and [R-EXT-01]'s vehicle 3 is "New ignore-lane flag bits" only, so no
  minor version can make an incompat bit conforming. Correctly a violation.
- T13, T15, T16 and T23 rest on keyword-free declaratives ("The LZ4 frame
  format is not used", "raw, not a zlib (RFC 1950) or gzip (RFC 1952)
  wrapper"). I checked the document's own practice before treating these as
  inert: §21.7 calls [R-CNT-13]'s keyword-free clause a prohibition, and
  [R-CNT-02] and [R-SER-01]/[R-SER-02] are the same construction. They have
  force; the rows are right.

No row registers a non-violation.

## 4. Every cross-reference to a row

`xref.py` scanned the whole document for `[FLTR]\d{1,2}` tokens outside the row
definition lines and resolved each against the 120 defined labels. Every
citation resolves. The one unresolved token is `F11` at line 3746, which is the
struck-label Note itself ("Row label F11 is struck, and the gap it leaves in
this table is deliberate"), so it is the absence being described rather than a
dangling reference.

I then checked that each citation says what the row says:

- §2.3's Note, lines 280–288: F14 reaches, F5 does not, F15 does not. Each row's
  condition matches the reason given (F14 checksums bytes a future major may
  redefine but asserts only [R-CNT-24]'s CRC; F5's 128-byte floor is derived
  from major-1 facts; F15's reserved bytes lie inside the 48 redefinable ones).
- §2.3 line 255 and §21.6's closing, line 3933: F18 as version_major = 0. ✓
- §9.6 line 1430: "§21.2 rows F8, F14 and F17 — the magic, the trailer CRC and
  the length cross-check". F8 is trailer magic, F14 is trailer CRC, F17 is
  committed_file_length against the transport-authoritative size. ✓
- §5.2 line 718: "L18's overlap or L40 through L42's placement". L18 is
  intra-layer overlap; L40 is per-tile alignment, L41 slab run continuity, L42
  slab first-tile alignment. ✓
- §7.4's Note line 1185: a layer record "whose appearance as a sub-record §21.3
  registers in its own right" — L26. ✓
- §16.2's Note line 2351: the two rows a stale slab declaration surfaces as —
  L41, L42, both in §21.3. ✓
- §17.2's Note line 2435: "[R-COD-08] rejects it (§21.4, T24)" — T24 is the
  trailing-bytes row and its governing rule is [R-COD-08]. ✓
- §17.2's Note line 2498: an addressed-tile-less layer, "(`[R-GEO-02]`, §21.6)"
  — §21.6's "A dimension has extent 0" entry. ✓
- §20.3 line 3213: "T3 and T14 for a changed decoded size, T2 for a boolean
  byte". T3 is the decoded-payload-length row (any codec), T14 the codec-1
  entry-length row, T2 the interleaved bool byte. ✓
- §20.3 line 3269: "[R-COD-07]'s lz4 decoded-size cap among them (L44)". ✓
- §20.5 lines 3516–3518: "F36 and L25 for a record type, and one row for each of
  the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)". I
  derived the mapping myself from §10.2's eight-row table: channel layout →
  L36, linearization → L33, sample type → L34, codec → L43, filter → L45, index
  encoding → L31, metadata encoding → R1. Seven, exactly the seven listed, and
  each row does register that space's reserved range. Channel layout has no
  experimental range ([R-EXT-02]) and L36's second instance is "reserved 3-255",
  so it is genuinely a reserved-range row. ✓
- §21.1 lines 3642–3644: the specialization list. I checked the property for
  each pair rather than taking it: F1's front-block instance ⊂ F6 (a reversed
  16-byte block is not byte-identical to the constant); F1's trailer-magic
  instance ⊂ F8; F35 ⊂ F36; L24 ⊂ L25; F21 ⊂ F22 (a (0,0) slot has
  extent_length 0 < 5); L10 ⊂ L11. All hold strictly, and each broader row
  remains separately reachable, so each has a constructible vector under §21.8.
  The detector and detection point of the narrower row are what apply in each
  case, as §21.1 says.
- §21.1 line 3692: "F27 and L48" for [R-MTA-05]. ✓
- Appendix H lines 4774–4786: "(F1, F6)" for the front block, "(§9.7 ... F7)"
  for the pre-trailer gap, "(F36, L25)" for reserved-range types, "(R1)" for
  encoding 0 and the reserved range. All resolve to rows saying what the
  checklist claims. ✓

## 5. Outcome vocabulary

§2.4 defines four reader outcomes — reject-file, reject-layer, reject-tile,
ignore-record — plus preserve-verbatim, which it expressly places outside the
reader outcomes ("names an updater obligation, orthogonal to reader outcomes").
Each of the four is the outcome of exactly one register subsection, so all four
are reachable and no row carries a value §2.4 does not define. §21.2's,
§21.3's, §21.4's and §21.5's headings restate §2.4's definitions and I compared
them word for word; the restatements add scope detail ("the named layer is
unusable, every other layer unaffected"; "never returns fill in place of data")
that §2.4 and [R-CNF-09] already carry.

preserve-verbatim is reachable through §20.4's table (its MU = 1 and
MU = 0 / PE = 1 rows), which §2.4 names. It correctly has no register row: it
is not a condition.

## 6. Limits

The minimum-guarantee table has eight rows. Appendix B's summary row restates
all eight identically ("rank 32 · C 4096 · entry_count 2³² · 65,536 layers ·
16 MiB directory region · 256 MiB decoded tile · 16 MiB metadata document ·
8 MiB zstd window"). §2.3 and §2.5 both point at the table without restating
figures. §17.2 and §18.2 both cite "§21.9's 8 MiB `Window_Size` guarantee";
§18.2 additionally cites the user-metadata row and says correctly that it "is
stated over a document's decoded size, which a verbatim document has as surely
as a compressed one". No figure diverges anywhere.

I verified the Note's arithmetic (it is labelled *Note* and so non-normative,
but a wrong figure there would still mislead): 2³² entries give
⌈2³²/2¹⁶⌉ × 4 = 262,144 bytes = 256 KiB exactly; 2³⁶ gives 4 MiB exactly;
12.5 MiB over 65,536 layers is 200 bytes per record exactly; 256 MiB is 16×
the top of §11.3's "roughly 1 to 16 MiB" band. §24's "tens of gigabytes"
for a 2³² -entry index region is 80 GiB. All reproduce.

The hard-limit paragraph ([R-ERR-05]) I checked item by item against the
defining sections. Nine of ten restate their source exactly. The tenth — the
lz4 cap — drops [R-COD-07]'s "any of whose **addressed** tiles" quantifier and
its planar largest-plane rule; that is finding register-02 below.

I also checked the *reverse* direction, a limit stated elsewhere and missing
here. Appendix B's "User-metadata extent minimum | extent_length ≥ 5" has no
counterpart in §21.9's hard-limit list, and neither do the record header's 24
bytes or the index entry's 20. None is a defect: §21.9 says in its own opening
that "The hard limits it restates are a finding aid rather than an inventory",
which licenses omission but not misstatement.

The one place where a limit statement outside §21 asks for something §21.9's
text does not obviously grant is the *scope* at which a reader may decline a
file that exceeds a guarantee. That is finding register-01.

## 7. Checksums and worked arithmetic I recomputed

I implemented CRC-32C to §4.5's parameters (Castagnoli 0x1EDC6F41, reflected in
and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and reproduced its own check
vector before using it (`crc32c_check.py`):

| quantity | computed | document |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 (§4.5) |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 (§4.5) |
| CRC of a full 2¹⁶-entry all-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, L38, App. B) |
| CRC of §7.4's 80-byte four-sentinel entry array | 0x80A34955 | 0x80A34955 (§7.4) |
| crc_of_crc_array over `55 49 A3 80` | 0xC4EE982E | 0xC4EE982E (§7.4) |
| Appendix A's trailer CRC over trailer[0,60) | 0x402F157E | 0x402F157E (App. A) |

The all-sentinel constant matters directly to my charter: L38's condition text
turns on it ("the all-sentinel constant 0xEECB3BB2 never substitutes for
comparison"), and Appendix B restates it.

Other arithmetic I recomputed rather than trusted:

- §7.4's layer-record payload: 4 + 34 + 18 + 12 + 13 = 81 bytes, matching the
  stated 81 and the stated inline_length; its index extent
  4×20 + ⌈4/2¹⁶⌉×4 = 84, matching [R-CNT-17]'s formula that L22 restates.
- §15.4's example: entry_count 1,000,000 gives 16 segments (15 full plus 16,960),
  a 64-byte CRC array and a 20,000,064-byte region; tile 999,999 falls in
  segment 15 at segment-relative byte 339,180, with segment 15 at
  [19,660,800, 20,000,000). Every figure reproduces, and the full-segment size
  is 1,310,720 bytes = 1.25 MiB as stated.
- L2's domination claims, which are what let it enumerate nine instances rather
  than more: planar C·N dominates the max disk ordinal (C−1)·N + (N−1) = C·N − 1;
  interleaved P·Q dominates V = P·C because every Bᵢ ≥ 1 so Q ≥ C; P dominates
  the packed planar bool decoded size ⌈P/8⌉; N dominates the spatial ordinal
  s ≤ N−1; P dominates the in-tile ordinal. I also checked that §14.2's Q and Fᶜ
  need no instance: with C ≤ 65,535 (a `u16` field) and every element size ≤ 8,
  Q ≤ 524,280, which cannot approach 2⁶³−1, so no file can exhibit an
  overflowing Q. L2's omission of them is right.
- 0x7E000000 = 2,113,929,216 bytes ≈ 2016 MiB, comfortably above the 256 MiB
  decoded-tile guarantee, so the two limits do not collide.

## 8. Degenerate legal cases built against §21's universals

- **A layer with entry_count = 0.** Extent slot (0,0), crc_of_crc_array = 0.
  L22's formula gives 0, satisfied. L27 requires crc_of_crc_array = 0, satisfied.
  L37 compares crc_of_crc_array against the CRC of a zero-byte array, which is
  0x00000000 — satisfied, and in any case L37's detection point is tile use,
  which never arrives. No row fires.
- **A layer with one dimension of extent 0.** N = 0, addressed-tile count 0,
  entry_count 0. §21.6 records this as a valid empty layer. L44 does not fire
  whatever the tile shape, because its condition is quantified over addressed
  tiles; §17.2's Note confirms and adds that [R-ENC-04]'s ceiling "carries no
  such quantifier", so L2 still fires on P·Q or P·Bᶜ in such a layer. The two
  rows' quantifiers differ deliberately and both cells reflect it.
- **A file with zero layers** — the 128-byte minimal file of Appendix A. I
  reproduced its trailer CRC. §21.6 records it. §21.9's first five rows range
  over declarations "which every file and every layer carries"; a file with no
  layer simply has no instance of the layer rows.
- **A single-position planar bool plane (P = 1).** ⌈P/8⌉ = 1 byte with seven pad
  bits, which T5 governs and which §14.4's Note discusses. T5 fires only in a
  packed planar bool plane with P mod 8 ≠ 0, and its single instance is right —
  there is no other layout in which pad bits exist.
- **A user-metadata record with extent slot (0, 3).** Exhibits F30 (exactly one
  half zero) and F22 (extent_length < 5) but not F21. Neither is a
  specialization of the other, so §21.1's "Rows that merely overlap, each
  reachable without the other, do not stand in it" applies, correctly.

## 9. Suspicions I opened and closed

- **§21.1's parenthetical `[R-ERR-02]` after "§21.2 through §21.5".**
  [R-ERR-02] is the identifier at the end of §21.8, whose subject is
  conformance-vector coverage, not the register's completeness. I nearly filed
  this as a misattributed identifier. Closed: §21.8's own text is "Every row of
  §21.2 through §21.5 ...", so the parenthetical reads as a forward pointer
  identifying the register as what [R-ERR-02] quantifies over, not as an
  attribution of §21.1's rules. §21.1's normative content is covered by
  [R-ERR-01] at the end of §21.7 under the document's own convention of placing
  an identifier at the end of the block it governs (visible throughout §2.3,
  §7.2, §7.4).
- **"the row is the rule" (§21.1 ¶2)** against ¶1's "where a row and the rule
  it cites diverge, **the rule governs**". Closed by the parallel construction:
  "the row is the rule, and each instance is one file" is a statement about
  corpus granularity — a row corresponds to a condition, an instance to a file —
  not about authority. No implementer following the sentence to its end reads it
  as an authority claim.
- **"[R-SER-08] is the one rule that goes the other way" (§21.1 ¶2).** A
  uniqueness claim, so I derived the members: I listed all twenty verifier rows
  and what each governing rule obliges a reader to do. The only competitor is
  [R-CNT-12]'s "a reader or updater encountering it MUST treat the record as
  PE = 1", which resolves a nonconforming flag combination to a defined value.
  Closed: the claim in context is about a *byte a reader returns* ([R-TYP-04],
  §12.3, "the one byte a reader resolves rather than serves through"), and
  [R-CNT-12]'s resolution is a disposition rule about preservation, shared with
  updaters, that leaves a reader serving the record unchanged.
- **L46 against L49 as an unlisted specialization.** Every file whose *layer
  record* carries MU = 1 with PE = 0 also has a PE bit differing from the
  registry's fixed PE = 1, so L46's layer-record instance is strictly inside
  L49's. Closed: §21.1 says "the property decides any pair and this list is not
  offered as closed", and L46's sub-record instance is reachable without L49
  (an unregistered sub-record type). Both rows are verifier/certification with
  the same outcome, so nothing turns on it.
- **F27's reject-file outcome under the quarantine.** [R-CNT-25] makes "every
  way its document can be unreadable" ignore-record. Closed: [R-MTA-05] says
  "unsorted members do not make a document unreadable", so the quarantine does
  not reach it, and the record's owning scope ([R-MTA-02]) gives file for a
  top-level record and layer for a sub-record — F27 and L48 respectively.
- **"neither is a reason for a reader to reject anything" (§21.6's closing)**
  against [R-CNF-12]'s "a reader MAY reject it upon detecting any violation,
  including violations whose assigned detector is the verifier". Closed: the
  sentence's subject is the reader's *obligation* and the paragraph's claim is
  that "the reader's side of them ... is unchanged"; §7.4 shows the document's
  careful phrasing for the same point when it needs to be exact ("where the file
  is otherwise conforming a reader MUST NOT reject the file for it — on a
  nonconforming file [R-CNF-12]'s licence ... is untouched"). Not a divergence
  a competent reader could act on wrongly, since [R-CNF-12] states the licence
  unconditionally.
- **§21.9's "rank at most 255" as a hard limit a file could violate.** No file
  can carry rank 256: the field is a `u8`. This is §21.7's "no condition a file
  can exhibit" class, so calling it a limit "a file violating one is invalid"
  is loose. Closed: §21.9 immediately says "Most follow from a field's width",
  which is the same observation, and there is correctly no register row for it.
- **§21.9's per-instance individuation against [R-COD-07].** "*Decoded size of
  one tile* ranges over a layer's **addressed** tiles, stored or not, exactly as
  [R-COD-07]'s cap is". I put the two governing verbs side by side as the
  analogy shape demands: [R-COD-07] is "for a layer any of whose addressed
  tiles' decoded size exceeds", §21.9 is "ranges over a layer's addressed
  tiles". The analogy holds exactly. (It is the *hard-limit restatement* later
  in the same subsection that drops the quantifier — register-02.)
- **§21.8's "one vector per instance" against the specialization rule.** A
  vector for F6 must be a front-block mismatch that is not a byte-reversal, or
  it would be recorded against F1. I checked each of the six specialization
  pairs for a constructible broader-row vector; all six have one.
- **T13 as a duplicate of T25.** T13's two instances (a deflate history window,
  an lz4 back-reference past produced output) both fail T25's decode. Closed:
  T13's own text says so — "the check that detects it is T25's, and this row
  records the cause rather than a procedure of its own" — and T15, T16, T23 and
  T26 use the same construction, which the register applies consistently.
- **A missing row for a zstd tile carrying an undeclared dictionary.** Closed:
  [R-COD-06] states it is "not detectable by inspection", §21.7 places it in the
  unwitnessed class, and §18.2 names the document-side analogue as the same
  class. Consistent across three places.

## 10. Findings

### register-01 — AMBIGUITY. [R-ERR-04]'s decline scopes are enumerated in a way two other requirements read past.

§21.9, [R-ERR-04]:

> A file exceeding any of these remains conforming, and a reader MAY decline it
> — at the whole file, or at the narrowest scope whose stated or derived
> quantities exceed what it can serve: a layer, a tile, or the record carrying a
> user-metadata document, as §18.2 assigns.

§17.2, [R-COD-06]:

> a wider window is conforming and merely permits a conforming reader to decline
> the tile or the layer on resource grounds (`[R-ERR-04]`).

§2.3, [R-CNF-11]:

> when it declines a layer's or a tile's decode on resource grounds and so
> cannot check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`,
> `[R-SER-08]`)

A frame's declared `Window_Size` is not a layer declaration. §21.9's own
per-instance paragraph individuates that row over "the ... compressed frames a
file actually contains, neither of which exists except as stored bytes", and a
compressed frame in a tile payload lies in the tile's stored extent, whose
owning scope §17 fixes as the tile. So the "narrowest scope whose stated or
derived quantities exceed what it can serve" is the tile, and the layer's own
stated or derived quantities do not exceed anything. Yet both requirements above
cite [R-ERR-04] for a layer-scope decline driven by exactly that quantity.

Permitted readings. **(a)** The enumeration is exhaustive: a reader declining
the layer over one tile's frame window is doing something [R-ERR-04] does not
license, and [R-COD-06] and [R-CNF-11] overstate what it grants. **(b)** The
enumeration is illustrative of the narrowest available granularity, and any
scope from the narrowest up to the whole file is licensed. I pick (b): §18.2,
which is the one other place that works the same mechanism through in detail,
offers exactly two options for a document ("which is also the narrowest scope at
which [R-ERR-04] lets it decline the document on resource grounds; it MAY
instead decline the whole file"), and the whole-file option is broader than the
narrowest — so [R-ERR-04] already licenses a scope wider than the narrowest in
the one case it spells out. And once any quantity exceeds a guarantee,
[R-CNF-03]'s acceptance duty has lapsed for that file altogether, so no reader
is barred from refusing at any granularity.

An implementer who reads (a) and builds a verifier that reports a layer-scope
resource decline as an overreach — or a reader that refuses to offer one — is
following the text of the requirement that defines the licence, and is
diverging from what [R-COD-06] and [R-CNF-11] tell it to expect.

Not byte-level. Both readings concern a reader's *resource* decline on a file
the document calls conforming under either reading. The emittable set is
untouched, and [R-CNF-03]'s acceptance duty does not run to the file in
question under either reading, so no accept/reject verdict a rule obliges
changes.

### register-02 — OBSERVATION. §21.9's hard-limit restatement of the lz4 cap drops [R-COD-07]'s addressed-tile quantifier.

§21.9, [R-ERR-05]:

> Some limits are instead **hard**: a file violating one is invalid, not merely
> large. They are stated where the structures forcing them are defined — ... a
> layer declaring codec 4 at decoded tile size at most `0x7E000000`
> (`[R-COD-07]`); ...

[R-COD-07] itself:

> Writers MUST NOT declare this codec for a layer any of whose addressed tiles'
> decoded size exceeds 0x7E000000 bytes — the block format's practical
> interoperability bound; in a planar layer each channel's plane carries its own
> decoded size (§14.2, §14.3), and the largest governs

L44 restates it faithfully: "Codec 4 (lz4) declared on a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes — in a planar layer the
largest channel plane governs". §21.9's restatement drops both qualifiers. Read
on its own, it makes a layer that addresses no tile (every dimension extent 0,
§11.2) but declares codec 4 with tile extents whose product exceeds the cap into
an invalid file — precisely the case [R-COD-07]'s Note takes pains to exempt:

> The cap is quantified over the layer's *addressed* tiles, so a layer that
> addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
> whatever its tile shape declares, and codec 4 is conforming there.

The dropped planar qualifier is less consequential — "decoded tile size" over a
planar layer's several plane sizes reduces to the largest under any reading that
requires every tile to satisfy the cap.

What decides it, and why this is not byte-level. §21.9's own two governing
sentences, immediately above the list and inside it: "The hard limits it
restates are a finding aid rather than an inventory — each is normative where
the structure forcing it is defined", and "They are stated where the structures
forcing them are defined". That subordination is explicit and unconditional, so
[R-COD-07] governs and the empty layer stays conforming. §21.9's own
per-instance paragraph, forty lines earlier, states the addressed-tile
quantifier correctly ("exactly as [R-COD-07]'s cap is"), and L44 states it
correctly, so three passages in §21 agree with [R-COD-07] against one compressed
restatement that disclaims its own authority. An implementer would have to read
[R-ERR-05]'s clause in isolation, past both disclaimers, to reject the file.

I report it because my charter asks for "a limit claimed here that the defining
section states differently" in both directions, and this is the only one of the
ten hard limits that does not restate its source exactly.

### register-03 — OBSERVATION. A §21.6 entry reaches layer sub-records but its Rule cell names only the top-level rule.

§21.6:

> | A record type this specification has not assigned, from the experimental
> range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
> per its PE bit; a *reserved*-range type is read the same way, but emitting one
> is a violation (F36, L25) | `[R-CNT-15]`, `[R-WRT-08]` |

The Condition cell is not restricted to top-level records, and the Defined
behavior cell names L25, which is a *sub-record* row. But the Rule cell cites
[R-CNT-15], whose scope is the top-level sequence ("An unknown record type at
file scope: MU = 1 → reject-file; MU = 0 → ignore-record"), and [R-WRT-08]. The
rule that gives an unassigned sub-record type with MU = 0 its ignore-record
outcome is [R-CNT-18] — "an unknown sub-record type with MU = 1 is
reject-layer ... with MU = 0 it is ignore-record" — which the entry does not
cite. §10.3 keeps the two apart where it needs to: "for record types, the MU-bit
outcome of `[R-CNT-15]` at file scope and `[R-CNT-18]` for layer sub-records".

§21.1 makes the rule govern here as it does for a register row: "§21.6's entries
restate their governing rules on the same terms a row does, and where such an
entry and the rule it cites diverge, the rule governs there too." So [R-CNT-18]
governs the sub-record half and the outcome is the same ignore-record the entry
states. Nothing an implementer does changes; the entry is under-cited rather
than wrong, and the outcome it states is the outcome both rules assign.

Not byte-level: both rules give the same outcome for the case, so no file's
verdict and no writer's output set turns on which is cited.

## 11. Where I found little, and what I did that would have found something

The four charter areas that produced no finding, and the instrument I used on
each:

- **Row-versus-rule agreement (0 findings across 120 rows).** I did not sample.
  I tabulated all 120 Detector, Detected and Governing-rule cells
  programmatically and checked the value sets closed; then read every governing
  requirement in the document and compared each row's four attributes against
  it. Two constructions that would have shown up: a verifier row whose rule
  obliges a reader (none — every verifier row's rule either says "a verifier
  MUST" or says readers are not obligated), and a row whose subsection outcome
  differs from the scope its rule assigns (none — I traced each of the four
  outcome classes back through §2.4's owning-scope mapping, [R-CNF-08], and each
  rule's own express assignment). The instrument caught the T13/T15/T16/T23
  family, whose rules state no outcome, and resolved each through §17's owning
  scope rather than letting it pass.
- **Completeness (0 findings).** I read all 52 occurrences of "validity error"
  in context with whitespace normalised across the hard wrap, and paired each
  with a row or with the document's own stated reason for having none. I
  separately walked every `R-*` identifier's writer-side prohibitions. The
  instrument would have found an unregistered detectable violation: it did find
  the six passages where the document declares a deliberate absence, which is
  the same shape a genuine omission would take without the declaration.
- **Cross-references (0 findings).** Every `[FLTR]\d` token in the document was
  resolved mechanically; every citation was then read against the row it names.
  The only unresolved token was the struck F11, which is the Note describing the
  gap. I checked the seven-space mapping in §20.5 by deriving it from §10.2's
  table rather than reading it off, which is where a wrong row would have shown.
- **The counting (0 findings).** All four subsection totals and §21.8's
  120/277 reproduce exactly from a mechanical parse, and I re-derived a sample
  of cells from §21.1's own magnitude, layout, family and nonzero-value rules
  rather than only counting semicolons. A cell written against those rules
  would have shown as a count mismatch or as a rule-violating cell; neither
  appeared.
- **Outcome vocabulary (0 findings).** All four §2.4 reader outcomes are
  reachable, one per subsection, and no row carries a value outside them. I
  checked preserve-verbatim's placement outside the register against §2.4's own
  "orthogonal to reader outcomes".

My confidence that §21 is clean is high on the counting and the cross-references
— both are mechanical and both reproduced — and good on row-versus-rule
agreement, where the work was exhaustive but by hand. It is lowest on the
completeness sweep in the "detectable but unregistered" direction, because that
one requires imagining a condition the document does not name; the best I can
say is that I derived the condition sets of [R-CNT-06] (nine), §15.3 (eleven),
§18.2's document restrictions (four, expanding to six rows), and §18.2's
carried-over frame constraints (eight, expanding to sixteen instances) from the
rules rather than from the register, and each derivation landed exactly on the
rows the register carries.
