# Cleanroom round 13 — Register hunter transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (all 4,128 lines, in four Read calls plus targeted greps). I ran `grep`/`rg`
and `python3` against that file only, plus two standalone Python computations that
read no files (a CRC-32C implementation and the register's row/instance arithmetic).
I opened no ADR, no `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`/`AGENTS.md`/`README.md`, no git history, and no network resource. I did
not list or read the round-13 output directory. I wrote this file and nothing else.

I did not consult prior-round findings. Where prior knowledge of other array or
image formats generated a suspicion, I settled it against this document's text
only, and I say so where it happened.

---

## 0. Method

My charter is §21. I read §21 first, then read the whole document, then held §21 to
the rules it cites. Concretely I did six passes:

1. Mechanically count rows and instances per §21.1's stated arithmetic and compare
   against every total the document states (§21.2/§21.3/§21.4/§21.5 headings, §21.8).
2. Row-versus-rule: for each of the 121 rows, locate the cited requirement, and
   compare wording, outcome class, scope, detector, and detection point.
3. Completeness forward: enumerate every requirement identifier in the document and
   classify each as (a) registered, (b) SHOULD/advisory, (c) actor conduct, (d)
   accounted for as undetectable, or (e) unaccounted.
4. Completeness backward: for each row, confirm the rule actually makes the
   condition a violation.
5. Every cross-reference *to* a register row or to §21, from anywhere in the
   document, resolved against the row it names.
6. Limits: §21.9 against every other statement of a limit, both directions;
   plus arithmetic and CRC verification of every constant §21 or its neighbours
   depend on.

---

## 1. The counting

§21.1 fixes the arithmetic:

> The **Instances** column enumerates what a conformance corpus builds
> for that row (§21.8) […] Instances within a
> cell are separated by semicolons, and a cell reading — is one
> instance; the count is therefore mechanical once the cell is
> written.

I extracted all 121 table rows from lines 3209–3363 and counted semicolon-separated
items per Instances cell, with `—` counting 1.

| Subsection | Rows | Stated | Instances |
|---|---|---|---|
| §21.2 file-scope | 36 | "36 conditions" ✓ | 56 |
| §21.3 layer-scope | 49 | "49 conditions" ✓ | 110 |
| §21.4 tile-scope | 26 | "26 conditions" ✓ | 54 |
| §21.5 ignored records | 10 | "10 conditions" ✓ | 44 |
| **Total** | **121** | — | **264** |

§21.8 states "121 conditions over 264 instances". **Both reproduce exactly.** Every
subsection heading count reproduces. No arithmetic discrepancy anywhere in the
register's own totals.

Per-row instance counts, for anyone who wants to check the sum:

```
F1 2  F2 6  F3 2  F4 1  F5 2  F6 2  F7 4  F8 1  F9 1  F10 1
F11 1 F12 1 F13 1 F14 1 F15 1 F16 1 F17 1 F18 1 F19 1 F20 1
F21 1 F22 1 F23 1 F24 1 F25 1 F26 1 F27 1 F28 2 F29 3 F30 2
F31 1 F32 1 F33 5 F34 1 F35 1 F36 1                    = 56

L1 8  L2 9  L3 1  L4 2  L5 1  L6 1  L7 2  L8 2  L9 2  L10 1
L11 1 L12 1 L13 1 L14 3 L15 4 L16 2 L17 2 L18 3 L19 1 L20 1
L21 1 L22 3 L23 4 L24 1 L25 1 L26 1 L27 1 L28 1 L29 3 L30 1
L31 3 L32 3 L33 4 L34 4 L35 1 L36 2 L37 1 L38 1 L39 3 L40 1
L41 3 L42 1 L43 3 L44 3 L45 3 L46 2 L47 2 L48 1 L49 4    = 110

T1 1  T2 1  T3 6  T4 4  T5 1  T6 1  T7 2  T8 1  T9 1  T10 1
T11 2 T12 1 T13 2 T14 6 T15 2 T16 1 T17 1 T18 4 T19 1 T20 1
T21 3 T22 3 T23 1 T24 1 T25 3 T26 3                      = 54

R1 4  R2 2  R3 2  R4 12 R5 8  R6 4  R7 6  R8 2  R9 2  R10 2 = 44
```

I also checked the L2 dominance claims by hand, since they are the only
instance cell that argues its own completeness:

- `C·N (which dominates the max disk ordinal (C−1)·N + (N−1))` —
  (C−1)·N + (N−1) = C·N − N + N − 1 = C·N − 1. Dominated. ✓
- `P·Q (which dominates V = P·C)` — Q = Σ Bᵢ over all channels and every Bᵢ ≥ 1
  (§12.1's table has no element size below 1), so Q ≥ C and P·Q ≥ P·C. ✓
- `P·Bᶜ` covers the planar numeric plane; `⌈P/8⌉` for a packed bool plane is
  dominated by P, which is listed. ✓
- Q itself and Fᶜ cannot overflow: C ≤ 65,535 (§7.4's u16) and Bᵢ ≤ 8, so
  Q ≤ 524,280. Correctly absent from the instance list. ✓

And I checked what L1 does *not* list. Alignment A and slab alignment A_slab are
u64 fields of the layer record, and they are not L1 instances. That is right:
`[R-ENC-03]` binds "every offset, length, extent, and count", and an alignment is
none of those; §16.1/§16.2 bound A and A_slab directly at 2⁶², which L39 and L29
register. So the omission is deliberate and correct, not a gap.

### Where the counting is uneven — see finding register-03

The totals reproduce, but §21.1's *criterion* for what goes in a cell is applied
inconsistently across rows of identical shape. Detailed in §5 below.

---

## 2. Row-versus-rule, row by row

I walked all 121. Only the rows where I had to stop and think are written up here;
the rest agreed with their rules on wording, outcome, scope, detector and detection
point without argument.

### The F/L parity is complete

Every record-level condition is registered once at file scope for a top-level
non-layer record and once at layer scope for a layer record or sub-record. I
checked the partition is exhaustive — records are exactly {top-level layer,
top-level non-layer, layer sub-record}:

| Condition | Top-level non-layer | Layer record / sub-record |
|---|---|---|
| type 0 | F24 | L13 |
| framing overrun / residue | F29 | L14 |
| extent slot half-zero | F30 | L15 |
| extent_offset < 16 | F31 | L16 |
| extent past F−64 | F32 | L17 |
| MU=1 with PE=0 | F25 (verifier) | L46 (verifier) |
| reserved flag bits 2–15 | F26 (verifier) | L47 (verifier) |
| registered type's stored MU/PE | F28 (verifier) | L49 (verifier) |
| reserved-range type, MU=1 | F35 (reader) | L24 (reader) |
| reserved-range type, any MU | F36 (verifier) | L25 (verifier) |
| >1 user-metadata record | F34 | L19 |
| UM slot (0,0) | F21 | L10 |
| UM extent_length < 5 | F22 | L11 |
| UM inline_length ≠ 1 | F23 | L12 |
| UM document unsorted | F27 (verifier) | L48 (verifier) |

The detector/scope split matches `[R-CNT-12]`, `[R-CNT-13]`, `[R-CNT-15]`,
`[R-CNT-18]`, `[R-CNT-22]`, `[R-CNT-25]`, `[R-MTA-03]`, `[R-MTA-05]` in every
row. `[R-CNT-13]`'s "the layer for a layer record and for sub-records, the file for
other top-level records" is what makes the "non-layer" qualifier on F25/F26/F28/
F30/F31/F32 correct, and it is present on exactly those rows and no others.

### F1 / F6 / F8 and the residency caveat

F1 carries a conditional detector inside its condition text:

> the front-block instance binds only a reader holding bytes [0, 16) resident
> (`[R-CNT-04]`), the trailer-magic instance every reader (`[R-CNT-06]`)

and its Detector cell reads "reader" flat. I checked this against §6.1:

> A reader that would have to issue a further range request to obtain those bytes
> MAY defer or omit the check

so two conforming readers *can* differ on whether they reject a file whose front
block is reversed: a local reader rejects, a suffix-only remote reader accepts. I
considered flagging this as a byte-level fork and rejected it: the file is
nonconforming (F1/F6 are violations), and `[R-CNF-12]` says "For a nonconforming
file no acceptance obligation exists". The divergence is deliberate, stated in three
places (§6.1, §19.1 step 1, §19.2's first bullet), and does not bear on which bytes
a conforming *writer* may emit.

§21.1's specialization list — "F1 of F6 and of F8, F35 of F36, L24 of L25" —
checks out. F1's front-block instance is strictly inside F6's condition; F1's
trailer-magic instance is strictly inside F8's; F35 is strictly inside F36; L24 is
strictly inside L25. The list says "Some rows are strict specializations", not
"these are all", so the tile rows that record a cause detected by another row's
check (T13→T25, T15→T24/T25, T16→T24, T23→T25, T26→T2/T4) are not a gap; and in
every one of those pairs the detector and detection point are identical, so
§21.1's attribution rule ("recorded against the narrower row, whose detector and
detection point are the ones that apply") has no consequence there anyway.

### F19 — is a set incompat-lane bit really a violation?

`[R-CNT-08]` carves out only the ignore lane:

> a writer creating a file under this text MUST write
> flags = 0, but a set ignore-lane bit is not a file-conformance
> violation

and `[R-CNF-02]` names that same carve-out as the model for conduct-only writer
rules. So a set bit in 0–15 violates the flags = 0 obligation with no carve-out →
file-conformance violation → F19 correct. I checked the growth vehicles to be sure
no minor version can define an incompat bit: §4.3 and §10.1 name "new ignore-lane
flag bits" only. F19 therefore holds unconditionally in major 1, and its single
instance ("flags bits 0-15") is consistent with F26's treatment of bits 2–15 of a
record's flags field as one instance.

### F5's use of the symbol F

F5's instance cell reads `F (physical file size); committed_file_length`. Everywhere
else in the document F is the *committed* file length — §5.1 ("The file size of a
conforming file equals the live trailer's committed file length F"), §15.3 ("with F
the committed file length"), §6.2's "F − 64", §9.7's "[16, F − 64)". F5 glosses F as
the physical size. The two instances are genuinely distinguishable files (a
64-byte physical file; a 128-byte physical file declaring committed_file_length =
64), and `[R-CNT-27]`'s "A reader MUST treat a shorter file as a validity error"
plainly means the physical file, which §19.1 step 1 obtains first. The parenthetical
disambiguates itself and the second instance is named explicitly, so the row is
readable. I did not raise this as a finding; recording it so the next reader does
not have to re-derive it.

### F33 versus `[R-CNT-13]`'s three overlap cases — finding register-04

`[R-CNT-13]` names three:

> a verifier MUST treat an intra-layer overlap — including a stored extent
> overlapping its own layer's index region or sub-record extents — as
> reject-layer, any overlap across layers or touching another scope's structures
> as reject-file, and any overlap between two structures neither of which belongs
> to a layer as reject-file

F33's condition text names two after its em-dash:

> A byte of the live committed state is claimed by two structures that do not
> belong to the same layer — across two layers, or a layer structure against
> another scope's structure

The third case (two structures *neither* of which belongs to a layer — a top-level
record extent overlapping the directory region, or two top-level record extents
overlapping each other) is covered by F33's headline ("two structures that do not
belong to the same layer" is true of two non-layer structures) and by its instance
list, which includes both `record extents` and `directory region`. But the gloss,
read restrictively, excludes it, and under that reading there is no register row for
it at all — which would be a violation of §21.1's normative completeness. I picked
the illustrative reading. Written up as a finding below.

### The verifier-detected rows and their outcome cells

Twenty-one rows carry Detector *verifier*: F7, F25, F26, F27, F28, F33, F36; L18,
L25, L40, L41, L42, L46, L47, L48, L49; T2, T4, T5, T26. For each I checked that
the outcome cell names the scope at which damage is recorded rather than an
obligation on a reader, per §21.1:

> For a row whose Detector is *verifier*, the outcome names the scope at which the
> damage is recorded, not an obligation on any reader

and that the governing rule says what a reader does. All twenty-one agree. The two
that most invite a mistake — F27/L48 (unsorted metadata members) and F28/L49
(stored MU/PE against the registry) — are exactly the pair §21.6's closing text
calls out:

> Both make the file nonconforming while leaving every reader behavior unchanged —
> readers process the document and apply the type's fixed semantics — so both carry
> detector *verifier*

and `[R-MTA-05]` ("readers process the document unchanged") and `[R-CNT-22]` ("A
reader MUST apply a known type's specified semantics regardless of its stored MU
and PE bits") both confirm it. This is the pattern the brief warns reporters
over-claim on; I found no divergence here to claim.

I noted one wording tension and decided against raising it. §21.1 says of
verifier-detected rows that "for several such rows it obliges the reader to serve
the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`)". For `[R-CNT-22]` that is
exact. For `[R-SER-08]` the reader serves the *tile* unchanged but does not return
the *byte* unchanged — §14.2 obliges it to "report 0x00 as false and every other
byte as true", which §12.3 calls "the one case where a reader resolves a byte to a
value rather than passing it through" and Appendix H calls "the sole resolved
byte". The word §21.1 uses is "structure", not "value" or "byte", and under that
reading the two examples are parallel (neither reader rejects). Not a finding.

### §21.5 and the quarantine

§21.5's preamble asserts two things I checked separately:

> every way its document can be unreadable takes this outcome, whatever the
> containing scope

against `[R-CNT-25]`'s enumeration — "a failed extent CRC, an unimplemented or
invalid encoding, a decode failure, or content violating the document's own rules
(ill-formed UTF-8 included)" — which maps to R2, R1, R3, and R5–R10, with R4
supplied by `[R-MTA-09]`'s frame constraints. Complete.

> Every row here is a violation all the same

against `[R-MTA-04]`, which states its four restrictions declaratively ("Four
restrictions apply, and a document violating any of them is unreadable") without a
MUST NOT on the writer. §2.1 makes all such text normative and `[R-CNF-12]` makes
failure of any requirement a conformance failure, so the assertion holds.

I checked R4's instance count against `[R-MTA-09]`'s constraint list: frame magic;
no skippable frame; no second frame; no nonzero dictionary ID; no content-checksum
flag; "the single frame occupying the extent's bytes before its terminal CRC
included" — six constraints × two containers = 12. The cell has exactly 12. ✓

I checked R3 is not over-counted: under encoding 1 the document is stored verbatim
(§18.2), so "stored bytes fail to decode" is unreachable there and the row's two
instances (the two containers) are right, not four.

I checked R2 is not under-scoped: it must still fire under an *unassigned*
encoding, because `[R-MTA-10]` lists "the extent's terminal CRC (`[R-CNT-20]`)"
among the structural checks that survive there. R2's condition text carries no
encoding restriction. ✓

### §15.3's entry table against §21.4

All eleven rows of §15.3 map:

| §15.3 row | Register |
|---|---|
| valid sentinel | §21.6 (non-violation) |
| sentinel offset/length, crc ≠ 0 | T6 |
| exactly one of offset/length = S | T7 |
| length = 0 (non-sentinel) | T10 |
| offset < 16 (non-sentinel) | T8 |
| offset or length > 2⁶³−1 | T11 |
| offset + length overflows | T12 |
| offset + length > F − 64 | T9 |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 |
| overlap outside the layer | F33 |
| alignment or slab invariant | L40, L41, L42 |

§15.3's "Six rows are marked *structural*" is right: rows 2–7 of its table. ✓

---

## 3. Completeness, forward and backward

### Forward: every requirement identifier accounted for

I enumerated all identifiers (`R-CNF-01…12`, `R-MDL-01…02`, `R-ENC-01…16`,
`R-CNT-01…27`, `R-LIF-01…08`, `R-EXT-01…05`, `R-GEO-01…06`, `R-IDX-01…05`,
`R-SLB-01…05`, `R-TYP-01…10`, `R-SER-01…09` with `R-SER-04` explicitly withdrawn
and noted as retired in §14.4, `R-COD-01…11`, `R-MTA-01…10`, `R-RDR-01…04`,
`R-WRT-01…09`, `R-ERR-01…05`, `R-SEC-01…07`, `R-PRV-01…05`, `R-VEC-01…04`) and
classified each. No numbering gaps except the deliberate `R-ENC-100` illustration
in §2.2, which is a worked example of §2.2's own numbering rule and not a
requirement.

Every MUST-level file condition I could find has a row. The ones that do not, and
why:

- `[R-LIF-01]`, `[R-LIF-03]` — history properties; §21.7 names them.
- `[R-GEO-06]`, `[R-SER-01]` — ordinal mappings; §21.7 names them.
- `[R-CNT-13]`'s no-embedded-offsets prohibition — §21.7 names it.
- `[R-ENC-06]` fixed field widths — §21.7 names it.
- `[R-SLB-04]` stale slab declaration — §16.2's own note: "Because this rule's
  detection *is* `[R-SLB-03]`'s, a stale declaration carries no register row of its
  own", and L41/L42 are the rows.
- `[R-LIF-04]` residue past a completed commit — §9.5's note: "Residue past a
  completed commit carries no register row of its own", met as F8/F14/F17, and F17
  cites `[R-LIF-04]` in its parenthetical. ✓
- `[R-CNT-02]`'s "belongs to no class" half — §5.2's note: "a register row for it
  would be a row no file could exhibit". The testable half (disjointness) is F33/L18.
- `[R-CNT-18]`'s nesting prohibition — §7.4's note: "in format major 1 it has no
  reader-detectable witness, and so no register row". **This one is accounted for
  nowhere in §21.7**, which §21.1 designates as the account. See finding
  register-02.
- `[R-ENC-01]` byte order — no witness beyond the signature, which is F1. Not named
  in §21.7 either, but it is inside §21.7's "wrong data" class in a way the nesting
  rule is not, so I did not raise it separately.
- `[R-MTA-06]`'s registry-version targeting, `[R-EXT-03]`'s publication ban — conduct
  rules under `[R-CNF-02]`; §21.6 records the file side as conforming.
- All SHOULDs (`[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-ENC-14]`,
  `[R-LIF-07]`, `[R-TYP-10]`, `[R-MTA-07]`'s writer half) — `[R-CNF-12]`: "§21's
  register enumerates MUST-level conditions only".

I checked `[R-CNT-23]`'s own "including" list item by item against §21.3: layout →
L36, codec → L43, filter → L45, index_encoding → L31, channel type → L34, nonzero
A_slab with S = 0 → L28, fill length ≠ element size → L30, nonzero
crc_of_crc_array with entry_count = 0 → L27. Eight for eight. Plus the §7.4 table
constraints not in that list: name → L3/L5/L6 and F4, linearization → L33, A → L39,
S → L1, rank → L32, C → L32, entry_count → L21/L22/L1, sub-records → L13/L14/
L24/L25/L26 and L10–L12/L19/L46/L47/L49.

I checked `[R-CNT-18]`'s five parse obligations: fixed fields, d dimension entries,
C channel entries, trailing fixed fields (all four → L23's four instances), and
"the remaining bytes MUST parse as zero or more complete sub-records […] with no
residue" → L14's three instances, including `trailing residue`. Five for five.

### Backward: no row registers a non-violation

I checked the rows whose governing rule is stated declaratively rather than with a
keyword — T13 (`[R-COD-02]` "Every stored tile is independently decodable"), T15/
T16 (`[R-COD-05]` "The stored bytes are exactly one DEFLATE compressed data stream
[…] raw, not a zlib […] or gzip […] wrapper"), T23 (`[R-COD-07]` "The LZ4 frame
format is not used"), R7–R10 (`[R-MTA-04]`'s four restrictions). §2.1 makes all of
them normative, so all are violations, and §21.5's preamble says so explicitly for
the R rows. No row registers something the rules leave conforming.

I checked the reverse trap too: everything §21.6 calls a non-violation is a
non-violation under its cited rules. All fourteen table entries check out against
`[R-IDX-02]`/`[R-TYP-08]`, `[R-MDL-01]`/`[R-GEO-02]`/`[R-RDR-04]`, `[R-GEO-02]`,
`[R-CNT-14]`, `[R-CNT-15]`/`[R-WRT-08]`, `[R-CNT-08]`, `[R-CNT-07]`, `[R-CNT-21]`,
`[R-SER-09]`, `[R-MTA-03]`/`[R-EXT-03]`/`[R-CNF-02]`/`[R-MTA-10]`, `[R-MTA-06]`,
`[R-MTA-07]`, `[R-LIF-06]`, `[R-COD-08]`. §21.1 explicitly removes §21.6 from the
completeness clause and the instance arithmetic, so §21.6's own completeness is not
a claim I need to test — which is just as well, since §18.2's "a document exceeding
that bound is ignore-record" is a defined non-violation §21.6 does not list.

---

## 4. Every cross-reference to a row

Exhaustive list of citations to register rows by label, anywhere in the document,
each resolved:

| Where | Cites | Resolves? |
|---|---|---|
| §9.6 `[R-LIF-06]`, line 1276 | "§21.2 rows F8 and F17" | ✓ F8 is the trailer-magic gate, F17 the committed_file_length-vs-transport-size gate; both are what a file "whose final 64 bytes are not a valid trailer" fails. |
| §17.2 note, line 2235 | "(§21.4, T24)" | ✓ T24 is "bytes remain in the stored extent after the stream […] ends", governed by `[R-COD-08]`, which is the rule the note invokes. |
| §21.1, line 3166–7 | "F1 of F6 and of F8, F35 of F36, L24 of L25" | ✓ all four specialization relations hold as strict containments. |
| §21.1, line 3185 | "T24's *any codec*" | ✓ T24's Instances cell is literally `any codec`. |
| §21.1, line 3187 | "(T15, T25)" as rows that enumerate | ✓ T15 has 2, T25 has 3. |
| §21.6, line 3376 | "(F36, L25)" for reserved-range emission | ✓ F36 top-level, L25 sub-record, both verifier. |
| §21.6, line 3411–4 | "(F18, `[R-CNT-07]`)" and "(F35, F36, L24, L25)" | ✓ F18 is version_major = 0; the four reserved-range rows are right. |
| Appendix H, line 4116 | "(`[R-CNT-05]`, F7)" | ✓ F7 is the structure-in-the-pre-trailer-gap row, verifier, `[R-CNT-05]`. |
| Appendix H, line 4117 | "(`[R-CNT-15]`, F36, L25)" | ✓ |

Every one resolves to a row that says what the citing text claims. This is the
class the brief flags as most dangerous ("A citation that points at the wrong row is
indistinguishable, to a reader, from a rule that means something else") and I found
no misdirected row citation.

I then checked every citation to §21 *sections* rather than rows (39 of them). All
resolve except one, §24's citation of §21.1 for a proposition about label
stability — finding register-01.

I also audited Appendix H's verifier checklist against the twenty-one
verifier-detected rows, since it is the only place that tries to summarise them:
F7 ✓ named; F25/L46 ✓ ("MU = 1 with PE = 0"); F26/L47 ✓ ("reserved bits");
F27/L48 ✓ ("user-metadata member ordering"); F28/L49 ✓ ("a registered type's
stored bits against §7.3's registry"); F33/L18 ✓ ("extent overlap (§7.2)");
F36/L25 ✓; L40/L41/L42 ✓ ("alignment and slab invariants (§16)"); T2/T4/T5/T26 ✓
("decoded-content obligations — padding samples and interleaved boolean bytes
(§14.5, §14.2)"). Complete.

---

## 5. Building it — a verifier from §21 alone

I wrote out, from §21 plus the rules it cites, the dispatch a verifier would need.
Where I had to guess, I say so.

**Open tier.** Physical size ≥ 128 (F5). Front block by equality if resident (F1,
F6). Trailer magic (F1, F8), trailer CRC (F14), version_major ≠ 0 and implemented
(F18, and §21.6's non-violation refusal), incompat lane clear (F19), then the field
gates in §6.2's order: committed_file_length = transport size (F17) and multiple of
64 (F13), dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16), dir_offset + dir_length ≤
F − 64 (F10), 1 ≤ generation ≤ 2⁶³−1 (F11 for the floor, F2 for the ceiling),
file_id ≠ 0 (F12), reserved bytes zero (F15). Directory CRC (F20). Record walk:
framing (F29), type ≠ 0 (F24), reserved-range types (F35 reader, F36 verifier),
multiplicity (F34), extent slots (F30, F31, F32, F2, F3), user-metadata framing
(F21, F22, F23) and encoding byte (R1). Layer-name namespace: uniqueness first
(F4), then §4.6 (L3, L5, L6).

That last ordering — uniqueness before validity — is not derivable from §21; I had
to go to §19.1 step 4, which states it outright ("Uniqueness is decided first, and
over the raw name bytes whether or not each name is itself well-formed"). §21's
Detected cells put F4, L3, L5 and L6 all at "open" without ordering them. That is
not a defect: §21.1 says the Detected cell names §19.2's tier, and ordering within a
tier is §19.1's job.

**Layer-access tier.** §21.3's 49 rows partition by Detected cell as:

- open (3): L3, L5, L6 — the layer record's own name, checked in §19.1 step 4.
- layer access (35): L1, L2, L4, L7-L17, L19-L24, L26-L36, L39, L43-L45.
- tile use (2): L37, L38 — the index chain, layer-scoped though detected here,
  which §19.2 states outright ("index-chain failures take layer scope
  (`[R-IDX-04]`) although their detection point is tile use").
- certification (9): L18, L25, L40, L41, L42, L46, L47, L48, L49.

3 + 35 + 2 + 9 = 49. (My first hand tally came to 50 by double-counting L19; the
extracted per-row values above are the authority, and I record the slip because it
is exactly the kind of error the register's own totals exist to catch.) The same
partition for the other subsections: §21.2 is 29 open + 7 certification = 36;
§21.4 is 22 tile use + 4 certification = 26; §21.5 is 9 extent use plus R1's
split cell = 10.

**Tile-use tier.** Index chain (L37, L38 — layer scope though detected here, which
§19.2 states explicitly), entry classification (T6–T12), payload CRC (T1), decode
(T3, T13–T25), and codec-1's pre-fetch length check (T14).

**Extent-use tier.** R2–R10.

**Certification.** F7, F25, F26, F27, F28, F33, F36; L18, L25, L40, L41, L42, L46,
L47, L48, L49; T2, T4, T5, T26.

**Where I had to guess.** Three places, all resolved against text elsewhere and
none left open:

1. Whether F33 covers two overlapping structures neither of which belongs to a
   layer. Resolved from `[R-CNT-13]`'s third clause and F33's instance list.
   Finding register-04.
2. Whether "F" in F5's instance cell means the physical size or committed_file_length.
   Resolved by the parenthetical and by the second instance being named separately.
3. Whether a verifier that declines a user-metadata document on its own decode
   bound reports nonconforming. Resolved by `[R-MTA-09]`: "the decline is not a
   finding that the file is nonconforming and a verifier MUST NOT report it as
   one", and by `[R-MTA-10]` for the unassigned-encoding case, which is *not* a
   decline. This was the most cross-cut chain in the document — §2.3, §9.7, §17.4,
   §18.2, §19.2, §21.5's preamble, §21.5 R3, §21.6's table row, §22.3 and
   Appendix H all restate it — and all ten agree, including on the three-way split
   between encoding 0 / reserved (violation, R1), experimental (non-violation,
   §21.6), and assigned-but-undecodable (violation, R3). This is the largest
   restatement surface in the document and I found no propagation defect in it.

---

## 6. Limits, both directions

### §21.9's minimum guarantees

| Quantity | §21.9 | Appendix B | Elsewhere |
|---|---|---|---|
| rank d | 32 | 32 ✓ | — |
| channels C | 4096 | 4096 ✓ | — |
| entry_count | 2³² | 2³² ✓ | §1, Appendix D cite it as "the tile-count guarantee"/"entry_count guarantee" ✓ |
| layers per file | 65,536 | 65,536 ✓ | — |
| dir_length | 16 MiB | 16 MiB ✓ | — |
| decoded tile | 256 MiB | 256 MiB ✓ | — |
| user-metadata document | 16 MiB | 16 MiB ✓ | §18.2 `[R-MTA-09]` and its note ✓ |
| zstd Window_Size | 8 MiB | 8 MiB ✓ | §17.2 `[R-COD-06]` ✓ |

Eight for eight, in both places, with three externally cross-referenced and
consistent.

§21.9's note argues the entry_count figure: "2³² addressed tiles is the point where
the segment-CRC array a reader fetches whole before using any entry (§15.4) is
still 256 KiB — it reaches 4 MiB at 2³⁶". Checked: ⌈2³²/2¹⁶⌉ × 4 = 2¹⁶ × 4 = 2¹⁸ =
256 KiB ✓; ⌈2³⁶/2¹⁶⌉ × 4 = 2²⁰ × 4 = 2²² = 4 MiB ✓. The layer figure — "65,536
layers is roughly a 12.5 MiB directory at the small layer records that figure
assumed" — implies ~200 bytes per record, which is the right order for §7.4's
81-byte worked example plus a couple of channels. ✓

The one place two guarantees interact is a 256 MiB tile under codec 3, where the
window may legitimately exceed the 8 MiB Window_Size guarantee. §17.2 prices it
explicitly — "a wider window is conforming and merely permits a conforming reader
to decline the tile or the layer on resource grounds (`[R-ERR-04]`)" — so the
composition is stated, not left to the implementer.

### §21.9's hard limits

All nine reproduce against their defining sections:

- names ≤ 255 bytes → §4.6 ✓ (and the u8 prefix makes it unwitnessable, correctly
  giving it no register row).
- user-metadata key ≤ 255 bytes → §18.2 bullet 4 ✓, and R10 is the row, correctly,
  since keys carry no prefix.
- rank ≤ 255, C ≤ 65,535 → §7.4's u8 and u16 ✓, Appendix B ✓.
- codec 4 at decoded size ≤ 0x7E000000 → §17.2 `[R-COD-07]` ✓, L44 ✓, Appendix B ✓.
- offsets/lengths/extents/counts ≤ 2⁶³−1 → §4.2 `[R-ENC-03]` ✓, Appendix B ✓.
- A power of two 512 ≤ A ≤ 2⁶² → §7.4, §16.1 ✓, L39 ✓, Appendix B ✓.
- A_slab power of two 1 ≤ A_slab ≤ 2⁶² → §7.4, §16.2 ✓, L29 ✓, Appendix B ✓.
- 1 ≤ S ≤ 2⁶³−1 → §7.4, §16.2 ✓, Appendix B ✓ (S = 0 means "no declaration", which
  §7.4's table states and §21.9's phrasing "a slab run length S" presupposes).
- no file shorter than 128 bytes → §5.1 `[R-CNT-27]` ✓, F5 ✓, Appendix A ✓,
  Appendix B ✓.

**No limit stated elsewhere contradicts §21.9, and no limit in §21.9 is stated
differently by its defining section.** The one limit stated elsewhere and absent
here — the user-metadata extent minimum of 5 bytes (§7.1, Appendix B, F22, L11) —
is not a defect, because §21.9 disclaims exhaustiveness in its opening sentence.
That disclaimer is itself the subject of finding register-05.

### Constants and arithmetic verified by computation

I implemented CRC-32C to §4.5's parameters (polynomial 0x1EDC6F41 reflected =
0x82F63B78, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it
against §4.5's own check vector before using it:

```
CRC-32C("123456789") = 0xE3069283   ✓ matches §4.5 and Appendix B
CRC-32C(zero bytes)  = 0x00000000   ✓
```

Then, on the register's neighbours:

```
CRC-32C(2^16 sentinel entries)      = 0xEECB3BB2  ✓ matches §15.4, Appendix B, and L38
CRC-32C(4 sentinel entries, 80 B)   = 0x80A34955  ✓ matches §7.4's new worked example
                                                    (stored 55 49 A3 80 ✓)
CRC-32C(that 4-byte CRC array)      = 0xC4EE982E  ✓ matches crc_of_crc_array ✓
CRC-32C(Appendix A trailer [0,60))  = 0xE00938D2  ✓ matches D2 38 09 E0 ✓
```

And §7.4's new worked layer-record example, field by field against its own table
order: name 4 bytes at 0; layout 1 at 4; linearization 2 at 5; codec 2 at 7; filter
2 at 9; A 8 at 11; S 8 at 19; A_slab 8 at 27; d 1 at 35; C 2 at 36; dimension entry
2 + 8 + 8 = 18 at 38; channel entry 7 + 5 = 12 at 56; index_encoding 1 at 68;
entry_count 8 at 69; crc_of_crc_array 4 at 77 — ends at 81. The prose totals
(4 + 34 name-and-nine-scalars, 18 dimension, 12 channel, 13 trailing) sum to 81 ✓,
and the nine scalars from layout through channel count are 1+2+2+2+8+8+8+1+2 = 34 ✓.
entry_count = ⌈100/32⌉ = 4 ✓. Extent length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 ✓. The
channel entry is byte-identical to §12.3's `temp` example as it claims ✓.

Nothing in the register's numeric neighbourhood is wrong.

---

## 7. Findings

### register-01 — OBSERVATION

**Location.** §24, `[R-VEC-02]` (line 3719); the cited target is §21.1.

**Quotation.**

> row labels are positional and renumber when a
> row is struck (§21.1), while §2.2 makes the identifier permanent, so
> the pair is what survives a renumbering.

**Detail.** §21.1 states nothing about row labels being positional, about
renumbering, or about what happens when a row is struck. I grepped the whole
document for `renumber`, `positional`, `struck` and `row label`: the only other
occurrences of `renumber` are §2.2's rule for *requirement identifiers* ("they are
never renumbered or reused") and two unrelated uses about disk ordinals (§11.1,
§20.3). So the half of the citation that names §2.2 resolves; the half that names
§21.1 does not, and the proposition it attributes to §21.1 is stated nowhere in the
document.

Permitted readings: (a) §21.1 is meant to be some other section and the citation is
a typo — but no section states it, so this reading has no target; (b) the
proposition is intended as a bare assertion of `[R-VEC-02]`'s own and the "(§21.1)"
is a stray cross-reference; (c) the reader is meant to infer positional labels from
the register's own F1…F36 numbering. I picked (b): the sentence reads perfectly
without the parenthetical, and `[R-VEC-02]`'s actual normative content (record the
row *and* the identifier) does not depend on where the label-instability claim
lives. An implementer building a corpus manifest is not misled about what to
record; a maintainer striking a row is left without a stated rule for what happens
to the labels below it, which is a documentation gap rather than an interoperability
one.

**Byte-level.** No. Nothing about a manifest's citation format changes which bytes
a writer may emit or a reader must accept. The requirement `[R-VEC-02]` imposes
(record both the row and the identifier) is unambiguous either way.

---

### register-02 — OBSERVATION

**Location.** §21.1 (line 3157–3161), against §21.7 and §7.4's closing note (line
1078–1086).

**Quotation.** §21.1:

> its **completeness is normative** — a
> *detectable* file-conformance violation this specification names and
> the register omits is a defect in this document, detectability being the gate
> `[R-CNF-07]` already applies and §21.7 the account, by class, of
> what fails
> it

§7.4:

> **Note.** The nesting prohibition binds writers and any type a later
> version registers; in format major 1 it has no reader-detectable
> witness, and so no register row.

**Detail.** §21.1 designates §21.7 as *the* account of what fails the detectability
gate, and that is the path an implementer auditing register completeness will take:
find a MUST with no row, look for it in §21.7, and conclude the register has a gap
if it is not there. §21.7's second paragraph names four groups — `[R-LIF-01]` and
`[R-LIF-03]` as history properties, `[R-GEO-06]` and `[R-SER-01]` as ordinal
mappings, `[R-CNT-13]`'s no-embedded-offsets clause as opaque by construction, and
`[R-ENC-06]`'s field widths as not a state a file can be in.

`[R-CNT-18]`'s nesting prohibition — "a sub-record MUST NOT itself contain records
(nesting depth beyond two is a validity error at layer scope)" — has no register
row and appears in none of those four groups. Its account lives only in §7.4's note,
which reasons on a fifth ground entirely (no reader parses a sub-record's payload as
a record sequence in format major 1). The same is true, less sharply, of `[R-SLB-04]`
(accounted for in §16.2's note), `[R-LIF-04]`'s residue (§9.5's note), and the
untestable half of `[R-CNT-02]` (§5.2's note) — though those three are detected
*through other rows* rather than being undetectable, so §21.7's "no witness" framing
would not fit them anyway.

Permitted readings: (a) "the account, by class" means §21.7 gives representative
classes rather than an exhaustive list, so scattered notes are legitimate
supplements; (b) §21.7 is the single place a completeness audit must satisfy, and
the nesting rule's absence is a gap in it. I picked (a), because "by class" is a
real hedge and §21.7's own opener says "A second set of obligations is omitted"
rather than "the following are all". But an implementer who takes §21.1 at its word
will look in §21.7, not find `[R-CNT-18]`'s nesting prohibition, and have to search
the document for the note that explains it. The fix that costs nothing is a clause
in §21.7 naming the class §7.4's note describes.

**Byte-level.** No. `[R-CNT-18]`'s nesting prohibition binds writers either way, and
no reader's accept/reject verdict turns on where its account is written.

---

### register-03 — OBSERVATION

**Location.** §21.1's instance criterion (lines 3177–3193) against §21.3 row L21
and §21.4 rows T14 and T22.

**Quotation.** §21.1:

> What a cell
> enumerates is the condition's own alternatives and containers: a row
> whose check ranges over a family without the condition changing
> shape states that range as a single instance (T24's *any codec*),
> and one whose members give the condition materially different shapes
> enumerates them (T15, T25).

L21:

> | L21 | entry_count does not equal the geometry-derived addressed-tile count (N interleaved, C·N planar) | — | reader | layer access | `[R-CNT-17]` (R-CNT-20) |

T22:

> | T22 | Codec 3 (zstd) and the frame's Frame_Content_Size field is present but does not equal the tile's decoded size | interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉ | reader | tile use | `[R-COD-06]` |

T14:

> | T14 | Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size | interleaved P·Q, length longer; interleaved P·Q, length shorter; planar numeric P·Bᶜ, length longer; planar numeric P·Bᶜ, length shorter; packed planar bool ⌈P/8⌉, length longer; packed planar bool ⌈P/8⌉, length shorter | reader | tile use | `[R-COD-04]` |

**Detail.** The 264 total reproduces exactly against the cells as written; this is
not an arithmetic error. It is that the register applies §21.1's own criterion two
different ways to conditions of identical shape, which matters because §21.8 and
`[R-VEC-03]` make the corpus build one vector per instance.

Two concrete asymmetries:

1. **Layout alternatives.** L21's condition text names two alternatives itself —
   "(N interleaved, C·N planar)" — and its cell records one instance. Every other
   row whose arithmetic varies by layout enumerates the layouts: L44 ("interleaved
   P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉"), T3, T14, T21, T22 all do.
   The corpus therefore builds three vectors for "declared window vs decoded size"
   and one for "declared entry_count vs derived tile count", though both are a
   single comparison whose right-hand side is a layout-dependent formula.

2. **Direction of a mismatch.** T14 and T3 split "differs from the decoded size"
   into longer and shorter, doubling their cells to six. T22 — the same shape, a
   declared quantity compared against the derived decoded size — does not, and
   neither does L22's first instance ("extent_length against the formula").

Permitted readings of §21.1: (a) "materially different shapes" is a judgment the
author exercises per row, so both treatments are licensed and the register is
merely uneven; (b) the criterion is meant to be mechanical, so one of each pair is
wrong. I picked (a) — §21.1 says "the count is therefore mechanical once the cell is
written", which locates the discretion in the cell rather than the count. But the
consequence is that a corpus builder reading §21.8 cannot predict from the criterion
alone whether a layout-dependent or direction-dependent condition needs one vector
or six, and must copy each cell verbatim. Making L21 and T22 match L44 and T14
would raise the total from 264 to 269 (L21 +1, T22 +3, L22 +1); making T3 and T14
match T22 would lower it to 258. Either is self-consistent; the register is
currently neither.

**Byte-level.** No. Vector counts are a corpus obligation. No implementation's
accept/reject verdict on any byte sequence changes.

---

### register-04 — AMBIGUITY

**Location.** §21.2 row F33, against `[R-CNT-13]` (§7.2).

**Quotation.** F33:

> | F33 | A byte of the live committed state is claimed by two structures that do not belong to the same layer — across two layers, or a layer structure against another scope's structure; a claimant reaching the front signature block or the live trailer is instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier | stored-tile extents; tile-index regions; record extents; sub-record extents; directory region | verifier | certification | `[R-CNT-13]` (R-CNT-02, R-IDX-03) |

`[R-CNT-13]`:

> a verifier MUST treat an intra-layer
> overlap — including a stored extent overlapping its own layer's index
> region or sub-record extents — as reject-layer, any overlap
> across layers or touching another scope's structures as reject-file,
> and any overlap between two structures neither of which belongs to a
> layer as reject-file

**Detail.** `[R-CNT-13]` names three overlap cases and assigns each an outcome. L18
registers the first. F33 registers the second and third — but its em-dash gloss
names only two, and both of the two require one party to be a layer structure
("across two layers, or a layer structure against another scope's structure"). The
third case, "any overlap between two structures neither of which belongs to a
layer", is not in the gloss. Concretely: a top-level user-metadata record's extent
overlapping the directory region, or two top-level record extents overlapping each
other.

Permitted readings:

(a) **Illustrative gloss.** F33's headline — "claimed by two structures that do not
belong to the same layer" — is the condition, and the em-dash clause is an example
list. Two non-layer structures do not belong to the same layer, so they are in.
This is confirmed by F33's own instance list, which pairs `record extents` with
`directory region`: those two claimants can only overlap in the third case, since
neither belongs to a layer.

(b) **Restrictive gloss.** The em-dash clause defines the condition. Then the third
case has no register row anywhere, and §21.1's normative completeness ("a
*detectable* file-conformance violation this specification names and the register
omits is a defect in this document") is violated by a case `[R-CNT-13]` names in so
many words.

I picked (a): the headline is general, the instance list only makes sense under it,
and §21.1's own tie-breaker — "where a row and the rule it cites diverge, **the rule
governs**" — puts `[R-CNT-13]` in charge regardless. A verifier that implemented
the gloss restrictively and missed two overlapping top-level extents would be
non-conformant to `[R-CNT-13]`, not to F33.

An implementer who reads F33 as its own specification and skips `[R-CNT-13]` builds
a verifier with a hole exactly where a hostile file would put smuggled bytes — a
top-level record extent aliased over the directory region. §22.3 names that class:
"which removes aliasing — two index entries pointing at one payload, or a payload
overlapping a structure that governs it — as a class". Extending F33's gloss with
"or two structures neither of which belongs to a layer" closes it.

**Byte-level.** No. §21.1 already decides which of the two governs, so a verifier
reaching for the rule gets the right answer, and a verifier reaching only for the
row is wrong under a rule it was bound by anyway. Two competent implementations
that both read `[R-CNT-13]` reach the same verdict on the same bytes.

---

### register-05 — AMBIGUITY

**Location.** §21.9's opening paragraph, `[R-ERR-03]` (lines 3455–3463), against
§2.5 `[R-CNF-10]` and against §21.9's own last paragraph `[R-ERR-05]`.

**Quotation.** §21.9:

> Every limit affecting which files are valid, or which files a
> conforming reader accepts, lives in this specification and never only
> in an implementation (`[R-CNF-10]`); this section collects the ones an
> implementer most often needs at hand, and is a finding aid rather than
> an inventory — each limit is normative where the structure forcing it
> is defined. The table
> below states **minimum guarantees**, not caps

§2.5:

> Readers MAY enforce resource limits, but MUST accept any
> conforming file within the minimum guarantees stated in §21's limits
> table; writers MAY rely on those minimums; the table is §21.9.

**Detail.** The framing sentence claims two things about "this section": that it is a
finding aid rather than an inventory, and that each limit it collects is normative
somewhere else, "where the structure forcing it is defined". Both are exactly right
about the *hard* limits in the last paragraph, which restates the same idea in its
own words ("They are stated where the structures forcing them are defined"). Neither
is right about the *minimum guarantees table*: rank 32, C 4096, entry_count 2³²,
65,536 layers, 16 MiB directory, 256 MiB tile, 16 MiB metadata document and 8 MiB
window appear nowhere else in the document (I grepped each figure), no structure
forces them, and §2.5 treats the table as the single authoritative source
("the table is §21.9"), with `[R-ERR-03]`'s own MUST attached to it.

Permitted readings:

(a) **The framing sentence scopes over the whole section**, in which case it is
false of the table: the table is an inventory, is normative in situ, and has no
elsewhere.

(b) **The framing sentence scopes over the hard limits it prefigures**, with the
table introduced separately by the next sentence and made normative by `[R-ERR-03]`.
Under this reading "each limit is normative where the structure forcing it is
defined" simply has no application to a guarantee no structure forces.

I picked (b), because `[R-ERR-03]`'s "a conforming reader MUST accept any conforming
file whose quantities lie within these bounds" sits in the same paragraph and is
unambiguous, and because §2.5 points at the table by name. The cost of (a) is that
an implementer building a limits table from §21.9 may go looking for the
authoritative rank guarantee in §11.1 and find nothing, then treat §21.9's figure as
advisory. That would make it decline a rank-32 file and fail `[R-CNF-03]`. The
resolution is immediate for anyone who reads to the end of the paragraph, which is
why I do not call this a fork.

**Byte-level.** No. Two competent implementations reading `[R-ERR-03]` and §2.5
agree that the guarantees bind. The misreading requires stopping mid-paragraph.

---

## 8. What I checked and found clean

Recorded so the next round does not re-spend the effort:

- **Row/instance totals.** 36/49/26/10 = 121 rows, 56/110/54/44 = 264 instances.
  Every stated total reproduces.
- **All 121 governing-rule citations** name requirements that exist and that state
  what the row says, on outcome class, scope, detector and detection point.
  (L26's `(§7.3 registry table)` and L31's `(§15.1)` are section references rather
  than identifiers in the parenthetical position; both are the correct authority,
  and both rows' primary citations are identifiers.)
- **All nine row-label cross-references** from outside the register resolve
  correctly.
- **F/L parity** across all fifteen record-level conditions.
- **§15.3's eleven entry states** all map to rows.
- **`[R-CNT-23]`'s eight named constraints** and §7.4's full table all map.
- **`[R-CNT-18]`'s five parse obligations** all map (L23 ×4, L14).
- **`[R-MTA-09]`'s six frame constraints** × two containers = R4's 12 instances.
- **Outcome vocabulary.** All four reader outcomes of `[R-CNF-07]` appear as
  subsection outcomes and all four are reachable both by reader-detected and (for
  the first three) verifier-detected rows; preserve-verbatim is correctly absent
  from the register and reachable in §20.4's table.
- **Detection-point vocabulary.** open, layer access, tile use, extent use,
  certification — §21.1's exact list, all five used, none invented.
- **Limits.** No mismatch in either direction; eight minimum guarantees and nine
  hard limits all agree with Appendix B and with every defining section.
- **Constants.** Every CRC the register or its worked examples depend on
  recomputed and matched: 0xEECB3BB2, 0x80A34955, 0xC4EE982E, 0xE00938D2, plus
  §4.5's own check vector.
- **§7.4's new worked layer record.** Offsets, field sizes, the 81-byte total, the
  four sub-totals, entry_count = 4, extent length 84, and byte-identity with
  §12.3's channel entry — all verified.
- **The `[R-MTA-10]` restatement surface** — ten passages across §2.3, §9.7, §17.4,
  §18.2, §19.2, §21.5 (preamble and R3), §21.6, §22.3 and Appendix H — mutually
  consistent, including the three-way split between encoding 0/reserved (violation),
  experimental (non-violation), and assigned-but-undecodable (violation). This was
  the most likely propagation target in the changed surface and it is clean.
- **Appendix H's verifier checklist** against all 21 verifier-detected rows:
  complete.

---

## 9. Confidence

Medium-high on the register itself. The register's arithmetic reproduces, its rows
agree with their rules, its cross-references resolve, and its limits are consistent
in both directions. I could not find a missing row for any detectable
file-conformance violation, and I could not find a row that registers a
non-violation.

My five findings are all documentation-level: a citation that does not resolve
(register-01), an audit path that is incomplete where §21.1 says it is complete
(register-02), an unevenly applied instance criterion that changes what a corpus
builds (register-03), a row gloss narrower than the rule it restates
(register-04), and a framing sentence that over-reaches its own table
(register-05). None of them forks bytes, and I say so for each rather than
hedging: in every case §21.1's "the rule governs" or a MUST in the same paragraph
already decides the question a divergent implementation would have to guess at.

The thing I am least certain about is register-03. §21.1 genuinely locates the
discretion in the cell ("mechanical once the cell is written"), so a triager may
reasonably rule that L21 and T22 are choices rather than errors. I report it
because the *same distinction* — layout-dependent arithmetic — is enumerated in
five rows and collapsed in one, and because §21.8 makes the cells load-bearing for
the corpus.
