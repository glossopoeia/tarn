# Cleanroom round 12 — Register hunter transcript

Charter: audit §21, the error-handling register, against the rules it restates
and against itself.

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.
I opened no other file in this repository — no `docs/`, no `PLAN.md`, no
`AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git history, no
network. I ran three Python scripts that I wrote myself in the scratchpad and
which read no repository file:

- `crc.py` — a CRC-32C implementation, used to check the document's three
  published CRC constants.
- `ids.py` / `reg.py` / `reg2.py` — parsers over the spec text (read through
  the Bash `grep`/`sed` and Read tools, which the access rule permits against
  that one file) that enumerate requirement identifiers and parse the four
  register tables.
- `build.py` — builds a complete conforming TARN file from the document alone.

I wrote `mini.tarn`, the built file, into the scratchpad. I did not read the
output directory.

---

## 0. Method

I read the document front to back once (3,982 lines), then did four passes
confined to my charter:

1. **Row-versus-rule.** For all 121 rows: locate the cited requirement, compare
   the row's condition wording, outcome class, scope, detector, and detection
   tier against what that requirement actually says.
2. **Completeness, both directions.** Enumerate every requirement identifier in
   the document (160 distinct strings, of which `R-ENC-100` is §2.2's
   illustrative example, not a requirement); for each, ask whether it names a
   single-file-detectable file-conformance violation, and if so find its row.
   Then the reverse: for each row, ask whether the cited rule really makes the
   condition a violation.
3. **Counting.** Recount conditions and instances by hand per subsection under
   §21.1's arithmetic, then re-derive them mechanically from the table source.
4. **Build.** Construct a conforming file end-to-end from the document alone
   and run the register against it, noting every point where I had to guess.

---

## 1. The counting

§21.1 fixes the arithmetic:

> Instances within a cell are separated by semicolons, and a cell reading — is
> one instance; the count is therefore mechanical once the cell is written.

and

> One instance is one *distinguishable* file: where a condition is a single
> predicate over several fields — a sum against a bound, a combination of two
> flag bits — the fields it reads are not instances, because no two files could
> differ.

### 1.1 Conditions

Hand count of row labels:

- §21.2 F1…F36 = **36**. Header states "36 conditions." ✔
- §21.3 L1…L49 = **49**. Header states "49 conditions." ✔
- §21.4 T1…T26 = **26**. Header states "26 conditions." ✔
- §21.5 R1…R10 = **10**. Header states "10 conditions." ✔

Total **121**. §21.8 states "121 conditions over 248 instances." ✔

### 1.2 Instances, by hand

§21.2 (semicolon counts, `—` = 1):

```
F1 2  F2 6  F3 2  F4 1  F5 2  F6 2  F7 1  F8 1  F9 1  F10 1
F11 1 F12 1 F13 1 F14 1 F15 1 F16 1 F17 1 F18 1 F19 1 F20 1
F21 1 F22 1 F23 1 F24 1 F25 1 F26 1 F27 1 F28 2 F29 3 F30 2
F31 1 F32 1 F33 5 F34 1 F35 1 F36 1
```

Running: 2,8,10,11,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,
33,34,35,36,38,41,43,44,45,50,51,52,**53**.

§21.3:

```
L1 8  L2 9  L3 1  L4 2  L5 1  L6 1  L7 2  L8 2  L9 2  L10 1
L11 1 L12 1 L13 1 L14 3 L15 4 L16 2 L17 2 L18 3 L19 1 L20 1
L21 1 L22 3 L23 4 L24 1 L25 1 L26 1 L27 1 L28 1 L29 3 L30 1
L31 3 L32 3 L33 4 L34 4 L35 1 L36 2 L37 1 L38 1 L39 3 L40 1
L41 1 L42 1 L43 3 L44 1 L45 3 L46 2 L47 2 L48 1 L49 4
```

Sum = **106**.

Spot checks on the two largest: L1's cell is `layer record extent_offset;
layer record extent_length; sub-record extent_offset; sub-record extent_length;
dimension extent Eᵢ; tile extent Tᵢ; entry_count; slab run length S` = 8. L2's
is `layer record extent_offset + extent_length; sub-record extent_offset +
extent_length; N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ; N·P; C·N (…); P·Q (…); P·Bᶜ; entry_count
× 20 + ⌈entry_count/2¹⁶⌉ × 4` = 9. Note both parenthetical asides inside L2's
cell (`(which dominates the max disk ordinal (C−1)·N + (N−1))` and `(which
dominates V = P·C)`) contain no semicolons, so they do not perturb the count —
that is deliberate drafting and it works.

§21.4:

```
T1 1  T2 1  T3 6  T4 4  T5 1  T6 1  T7 2  T8 1  T9 1  T10 1
T11 2 T12 1 T13 2 T14 1 T15 2 T16 1 T17 1 T18 4 T19 1 T20 1
T21 1 T22 1 T23 1 T24 1 T25 3 T26 3
```

Sum = **45**.

§21.5:

```
R1 4  R2 2  R3 2  R4 12  R5 8  R6 4  R7 6  R8 2  R9 2  R10 2
```

Sum = **44**. R4's twelve are six frame-constraint alternatives × two
containers (top-level extent, layer sub-record extent); R5's eight are four
alternatives × two containers; R7's six are three × two.

**53 + 106 + 45 + 44 = 248.** §21.8's "248 instances" reproduces exactly.

### 1.3 Mechanical re-derivation

I then parsed the four tables from source and re-counted, to guard against a
hand-counting error in my favour:

```
rows: 121 {'21.2': 36, '21.3': 49, '21.4': 26, '21.5': 10}
instances: {'21.2': 53, '21.3': 106, '21.4': 45, '21.5': 44} TOTAL 248
```

Both totals reproduce. **No counting finding.**

### 1.4 Vocabulary of the Detector and Detected columns

```
Detector: {reader: 101, verifier: 20}
Detected: {open: 32, layer access: 35, tile use: 24, extent use: 9,
           certification: 20, "open (top-level); layer access (sub-record)": 1}
```

§21.1 fixes exactly this vocabulary:

> Detection points name §19.2's reader tiers — open, layer access, tile use,
> extent use — or *certification* for the rows a verifier detects, which §19.2
> places outside the reader tiers entirely.

Every cell is inside it. R1's compound cell is the one row whose containing
scope decides the tier, and it names two tiers from the permitted set. ✔

### 1.5 Outcome vocabulary, both directions

`[R-CNF-07]` defines exactly four reader outcomes: reject-file, reject-layer,
reject-tile, ignore-record; `preserve-verbatim` is separately declared "an
updater obligation, orthogonal to reader outcomes."

- Every row's outcome comes from its subsection header, and the four headers
  are precisely those four values. **No row carries an undefined outcome.**
- All four defined values are reachable: §21.2 (36 rows), §21.3 (49), §21.4
  (26), §21.5 (10). **No defined value is unreachable.**
- `preserve-verbatim` correctly has no register subsection: it is not a reader
  outcome, and §2.4 routes it to §20.4's table instead. ✔

---

## 2. Row-versus-rule agreement

I checked all 121. Mechanically, every Governing-rule cell begins with a
bracketed identifier, and every identifier cited in those cells (primary and
parenthetical secondary) is defined somewhere in the document — zero dangling
citations.

The substantive check was outcome/scope. Working through the four subsections:

**§21.2 → reject-file.** F1 `[R-ENC-02]` ("MUST treat the file as invalid
(reject-file)") ✔. F2/F3 `[R-ENC-03]`/`[R-ENC-04]` — "validity error at the
owning scope", and `[R-CNT-06]` fixes "The owning scope of the front signature
block and the trailer is the file", while `[R-CNT-13]` fixes "the file for
other top-level records" ✔. F4 `[R-ENC-15]` — "a duplicate layer name is a
file-scope error (reject-file)" ✔. F5 `[R-CNT-27]` — "validity error at file
scope" ✔. F6 `[R-CNT-04]` — "MUST treat any mismatch as reject-file" ✔. F7
`[R-CNT-05]` — "A verifier MUST treat a structure in that gap as a validity
error at file scope" ✔. F8–F17 `[R-CNT-06]` — "Any failure is reject-file",
and I checked the gate list one-for-one: magic (F8), CRC (F14), version_major
(F18), flags (F19), committed_file_length vs size (F17) and multiple of 64
(F13), dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16), dir_offset + dir_length ≤
F − 64 (F10), generation range (F11 for 0, F2 for the ceiling), file_id ≠ 0
(F12), reserved bytes zero (F15). Every gate `[R-CNT-06]` names has a row and
no row invents a gate ✔. F21/F22 `[R-CNT-25]` — "validity error at its
containing scope", file for a top-level record ✔. F23 `[R-MTA-03]` ✔. F24/F29
`[R-CNT-12]` — "reject-file for the directory's top-level sequence" ✔.
F25/F26 `[R-CNT-12]` — "a verifier MUST treat a nonzero reserved flag bit or
the MU = 1 with PE = 0 combination as a validity error at the record's
governing scope" ✔. F27 `[R-MTA-05]` ✔ (below). F28 `[R-CNT-22]` ✔.
F30–F33 `[R-CNT-13]` ✔ — including F33's split from L18 exactly along
`[R-CNT-13]`'s own line ("an intra-layer overlap … as reject-layer, and any
overlap across layers or touching another scope's structures as reject-file").
F34 `[R-CNT-14]` ✔. F35/F36 `[R-CNT-15]` ✔.

**§21.3 → reject-layer.** The scope question that could have gone wrong is the
layer record's. §7.3's table gives type 0x0001 scope "file (container for layer
scope)", which read alone would put L46/L47/L49 at file scope. `[R-CNT-13]`
settles it explicitly — "the scope the record governs (§7.3): the layer for a
layer record and for sub-records, the file for other top-level records — a
malformed slot on a layer record is therefore reject-layer" — and L46/L47 cite
`(R-CNT-13)` precisely for that. The register is right and its secondary
citation is doing real work. ✔

L3/L5/L6 are the interesting pair: an ill-formed *layer record name* is
reject-layer, while a *duplicate* layer name is reject-file. That is exactly
`[R-ENC-11]`/`[R-ENC-12]` ("validity error at the owning scope", and §7.4:
"The owning scope of a layer record's inline payload is the layer") against
`[R-ENC-15]`'s express file-scope carve-out. ✔ And L3/L5/L6 carry Detected =
open while L4/L7/L8 (dimension/channel names) carry layer access, matching
§19.1 step 4 versus §19.3. ✔

L37/L38 carry Detected = tile use with outcome reject-layer. That looked wrong
until §19.2's own sentence: "index-chain failures take layer scope
(`[R-IDX-04]`) although their detection point is tile use." ✔

L40/L41/L42 verifier/certification, `[R-SLB-01]`/`[R-SLB-03]` both say
"(violation: reject-layer, §15.3)" ✔. L44 `[R-COD-07]` "validity error at layer
scope, checkable from declarations alone" — and the register puts it at layer
access, matching ✔.

**§21.4 → reject-tile.** T1 `[R-CNT-20]` ("a stored tile's CRC → reject-tile")
✔. T2 `[R-SER-08]` ("its assigned detector is the verifier, for which it is a
validity error at tile scope") ✔. T3 `[R-SER-07]` ✔. T4/T5 `[R-SER-05]` ("a
verifier MUST check it, and a violation is a validity error at tile scope") ✔.
T6–T12 against §15.3's ten-row table — I mapped every §15.3 row:

| §15.3 row | register |
|---|---|
| offset = S ∧ length = S ∧ crc ≠ 0 | T6 |
| exactly one of offset/length = S | T7 |
| length = 0 (non-sentinel) | T10 |
| offset < 16 (non-sentinel) | T8 |
| offset or length > 2⁶³ − 1 | T11 |
| offset + length overflows / > F − 64 | T12 / T9 |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 |
| overlap outside the layer | F33 |
| alignment or slab invariant | L40, L41, L42 |

Nothing in §15.3 is unregistered and no T-row invents a §15.3 state. I also
checked `[R-IDX-03]`'s own count — "Six rows are marked *structural*" — against
the table: rows 2,3,4,5,6,7 are the six. ✔

T14 `[R-COD-04]` ✔, T17–T22 `[R-COD-06]` ✔ (I checked each of the six against
the requirement's clauses: magic, exactly-one-frame/no-skippable, dictionary
ID, content-checksum flag, window size, frame content size — and against
`[R-COD-06]`'s own count "Three frame features are excluded", which is
dictionary / content-checksum / oversized window, the frame-count rule sitting
before that sentence). T24/T25 `[R-COD-08]` ✔. T26 `[R-COD-10]` ("a verifier
detects it as a validity error at tile scope") ✔.

**§21.5 → ignore-record.** `[R-CNT-25]` enumerates the ways a document can be
unreadable: "a failed extent CRC, an unimplemented or invalid encoding, a
decode failure, or content violating the document's own rules (ill-formed
UTF-8 included, `[R-ENC-11]`)". Mapping: extent CRC → R2; invalid encoding →
R1; decode failure → R3; content rules → R5–R10; and `[R-MTA-09]`'s frame
constraints → R4. `[R-MTA-04]`'s four restrictions map: object-unmarked → R7,
finite numbers → R8, no duplicate keys → R9, well-formed UTF-8 + §4.6 key rules
→ R5 (UTF-8) / R6 (empty, C0) / R10 (>255 bytes). Complete in both directions.
✔

The split of "unimplemented encoding" between R1 and §21.6 is the sharpest
piece of drafting in the subsection and it is right: R1 covers only `encoding 0`
and the reserved range 3–0x7F, because `[R-EXT-03]` makes emitting a reserved
value a violation, while the *experimental* range ≥ 0x80 is a conforming file
under `[R-CNF-02]` and therefore lives in §21.6, not §21.5. I tried to break
this and could not. ✔

### 2.1 Verifier rows and what §21.1 makes of them

Twenty rows carry Detector = verifier: F7, F25, F26, F27, F28, F33, F36, L18,
L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26. §21.1 governs their
outcome cells:

> For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader

I checked the two whose reader-side behaviour is *positively* specified —
`[R-SER-08]` (T2) and `[R-CNT-22]` (F28, L49) — and §21.1 names exactly those
two requirements as the examples. ✔ Appendix H's verifier checklist accounts
for nineteen of the twenty by name; T26 is covered under its "decoded-content
obligations" line, which is right, since §21.4 T26 says its check *is* T2's or
T4's.

I also confirmed F27/L48's placement. `[R-MTA-05]` says unsorted members "do
not make a document unreadable", so `[R-MTA-02]`'s quarantine ("the outcome of
every failure to **read** its document is ignore-record") does not reach them,
and the outcome falls back to the record's owning scope — file for a top-level
record, layer for a sub-record. That is exactly where the register puts them,
and §21.6's closing two paragraphs narrate the move. ✔

---

## 3. Completeness in both directions

### 3.1 Rule → row

I enumerated all requirement identifiers and asked, for the 91 that are cited
nowhere in §21.2–§21.5, whether each names a single-file-detectable
file-conformance violation. Every one falls into a class the document accounts
for:

- **SHOULDs** (`[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-ENC-14]`,
  `[R-LIF-07]`, `[R-TYP-10]`, `[R-MTA-07]`'s guidance) — §21.1: "§21's register
  enumerates MUST-level conditions only".
- **Reader/updater obligations** (`[R-ENC-05]`, `[R-ENC-10]`, `[R-ENC-13]`,
  `[R-MDL-01]`, `[R-MDL-02]`, `[R-GEO-04]`, `[R-TYP-08]`, `[R-TYP-09]`,
  `[R-RDR-01..04]`, `[R-MTA-02]`, `[R-MTA-08]`, `[R-SEC-*]`) — no file witness.
- **Conduct rules** (`[R-EXT-03]`'s publication ban, `[R-MTA-06]`'s registry
  version) — `[R-CNF-02]` expressly: "conduct rules bind the actor, the
  predicate binds the bytes".
- **History properties** (`[R-LIF-01]`, `[R-LIF-02]`, `[R-LIF-03]`,
  `[R-WRT-*]`) — §21.7's stated class, "properties of a file's history, which
  §9.7 does not reconstruct". `[R-LIF-02]`'s step 3 (a trailer re-pointed at a
  prior generation's directory) is the one I had to reason about myself: the
  resulting live state is internally consistent and the superseded bytes fall
  to slack, so there is no witness. §21.7 names `[R-LIF-01]`/`[R-LIF-03]` as
  representatives rather than an exhaustive list, and §21.1 describes §21.7 as
  "the account, **by class**", so the class covers it. Not a finding.
- **Content correctness** (`[R-ENC-01]`, `[R-TYP-04]`, `[R-TYP-05]`,
  `[R-SER-01]`, `[R-SER-02]`, `[R-IDX-01]`, `[R-GEO-06]`) — §21.7's first
  paragraph.
- **Definitional / non-violations** (`[R-GEO-02]`, `[R-SER-09]`, `[R-IDX-02]`,
  `[R-LIF-06]`, `[R-CNT-14]`'s zero-layer clause) — §21.6.
- **Explicit no-row notes.** Two obligations are called out in the text as
  carrying no row, and both are correct: `[R-SLB-04]`'s stale slab declaration
  ("every file exhibiting one exhibits a run whose tiles are unpacked or whose
  first stored tile is misaligned, which §21.3 registers" — L41, L42), and
  `[R-CNT-18]`'s nesting prohibition ("in format major 1 it has no
  reader-detectable witness, and so no register row"), whose one detectable
  case *is* registered, as L26.
- **Withdrawn.** `[R-SER-04]` is retired per §2.2 and correctly absent.

I then went the other way and grepped every writer-binding prohibition
(`Writers MUST NOT`, `MUST NOT emit`, `is a validity error`, `makes the file
nonconforming`, `is a violation`). Each maps: front block → F6; directory
placement → F7; big-endian → F1 (signature) else content; names → L3–L9/F4/
R5/R6/R10; §7.4 field constraints → L27–L36 and L39/L43/L45; geometry floor →
L32; linearization → L33; sample type → L34; bool fill → L35; interleaved bool
byte → T2; codec/filter → L43/L45; zstd frame → T17–T22; lz4 frame → T23; lz4
cap → L44; sorted members → F27/L48; record flags → F25/F26/F28/L46/L47/L49;
reserved-range values → F35/F36/L24/L25 and the per-space L-rows.

I also checked the eight numeric identifier spaces of §10.2 against the
register. Every one has a row that covers 0, its reserved range, and its
experimental range where one exists:

| space | row |
|---|---|
| record type | F35/F36, L24/L25 |
| channel layout (no experimental range) | L36 — and L36's instances are `layout 0; reserved 3-255`, correctly with no experimental instance |
| linearization | L33 |
| sample type | L34 |
| codec | L43 |
| filter | L45 |
| index encoding | L31 |
| metadata encoding | R1 (0 and reserved) + §21.6 (experimental) |

L33 and L34 split their reserved ranges into two instances each because §11.4
and §12.2 themselves distinguish "reserved without semantics" from "reserved
for future assignment"; L31, L36, L43, L45 do not, because their sections state
one reserved range. That is faithful. ✔

### 3.2 Row → rule

I looked for rows registering non-violations. The candidates and their
resolutions:

- **F19** (any incompat-lane flag bit set). §6.3 says a writer "MUST write
  flags = 0" and carves out *only* the ignore lane ("a set ignore-lane bit is
  not a file-conformance violation"), and `[R-CNF-02]` names that carve-out
  explicitly. Growth vehicle 3 (§10.1) is "new **ignore-lane** flag bits", so
  no minor can define an incompat bit. Under major 1 a set incompat bit is a
  violation. F19 stands. ✔
- **F27/L48** — `[R-MTA-05]`: "the file is nonconforming, a verifier MUST
  report it". Violation. ✔
- **F26/L47** — `[R-CNT-12]`: "writers MUST emit zero" plus the verifier
  clause. Violation. ✔
- **T13/T15/T16/T23/T26** — all are conditions whose detection is another
  row's check. Four of the five say so in the cell. T23 does not; see finding
  register-01.

**No row registers a non-violation.**

---

## 4. Every cross-reference to a row

The document cites register rows by label from nine places. I resolved each
against the row it names:

| citing text | cites | resolves? |
|---|---|---|
| §9.6 `[R-LIF-06]`: "fails `[R-CNT-06]`'s gates on the bytes handed over (§21.2 rows F8 and F17)" | F8, F17 | ✔ F8 = trailer magic; F17 = committed_file_length vs transport size — the two gates residue past a completed commit actually trips |
| §17.2 note: "A whole byte after the one holding the final bit does trail the stream, and `[R-COD-08]` rejects it (§21.4, T24)" | T24 | ✔ T24 is exactly "bytes remain in the stored extent after the stream … ends" |
| §21.1: "F1 of F6 and of F8, F35 of F36, L24 of L25" | 5 rows | ✔ each specialization holds, and the two where detector differs (F35/F36 reader vs verifier; L24/L25 likewise) are the ones where "whose detector and detection point are the ones that apply" has bite |
| §21.1: "T24's *any codec*" | T24 | ✔ its cell literally reads `any codec` |
| §21.1: "enumerates them (T15, T25)" | T15, T25 | ✔ T15 = 2 (zlib, gzip), T25 = 3 (deflate, zstd, lz4) — materially different shapes |
| §21.2 F33: "caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier" | 8 rows | ✔ directory bounds, top-level record extent bounds, layer/sub-record extent bounds, stored-tile bounds — the four claimant families, each with its low and high bound, at open/open/layer access/tile use |
| §21.4 T2: "the same byte at a padding position is T4's" | T4 | ✔ and T4's instance list carries `interleaved bool fill byte`, so the pair is exhaustive over `[R-SER-08]` as T2 claims |
| §21.4 T26: "the check that detects it is T2's or T4's" | T2, T4 | ✔ — and see §5 below, where I convinced myself T5 is *correctly* excluded |
| §21.6 and its closing: "(F36, L25)" and "(F18 …)", "(F35, F36, L24, L25)" | 6 rows | ✔ |
| Appendix H: "(`[R-CNT-05]`, F7)" and "(`[R-CNT-15]`, F36, L25)" | 3 rows | ✔ |

**All row citations resolve to rows that say what the citing text claims.**

The near-miss I chased hardest was T26's omission of T5. T26 names T2 and T4 as
the checks that detect a mis-strided filter, but §14.5 `[R-SER-05]` constrains
pad bits as well as padding positions, and pad bits are T5's row — so the
omission looked like a broken cross-reference. It is not. The byte-shuffle at
stride s over an image of length L = s·n places byte i of group j at offset
i·n + j; the last byte, i = s−1, j = n−1, lands at (s−1)·n + (n−1) = L − 1,
i.e. **the final byte is a fixed point of the shuffle at every stride**. Since
pad bits live only in the final byte of a packed plane, no stride error can
ever disturb them, and T5 can never fire from `[R-COD-10]`. T26's list of two
is exactly right. This is subtle and correct.

---

## 5. Limits

### 5.1 §21.9's minimum-guarantee table against every other statement

| §21.9 | restated at | agrees? |
|---|---|---|
| rank d 32 | Appendix B | ✔ |
| C 4096 | Appendix B | ✔ |
| entry_count 2³² | Appendix B; §1 "§21.9's tile-count guarantee"; §24 `[R-VEC-03]`; Appendix D | ✔ |
| layers 65,536 | Appendix B | ✔ |
| dir_length 16 MiB | Appendix B | ✔ |
| decoded tile 256 MiB | Appendix B | ✔ |
| metadata document 16 MiB | Appendix B; §18.2 note "The 16 MiB figure is a §21.9 minimum guarantee" | ✔ |
| zstd Window_Size 8 MiB | Appendix B; §17.2 "§21.9's 8 MiB `Window_Size` guarantee" | ✔ |

The §21.9 note's supporting arithmetic checks out: at entry_count = 2³² the
segment-CRC array is 2³²/2¹⁶ × 4 = 2¹⁶ × 4 = 262,144 bytes = 256 KiB, and at
2³⁶ it is 2²⁰ × 4 = 4 MiB — both as stated. §24's claim that a bound vector is
not constructible also checks: 2³² × 20 + 2¹⁶ × 4 ≈ 85.9 GB, "tens of
gigabytes".

Guarantee-versus-hard-limit consistency: rank 32 ≤ 255; C 4096 ≤ 65,535;
entry_count 2³² ≤ 2⁶³ − 1; decoded tile 256 MiB ≤ 0x7E000000 (= 2,113,929,216
≈ 1.97 GiB) so codec 4 never collides with the tile guarantee. ✔

`[R-CNF-10]` ("the table is §21.9"), `[R-CNF-03]`, and `[R-ERR-03]` state the
same acceptance duty three times without divergence. `[R-ERR-04]`'s scope for a
decline — "at the whole file, or at the narrowest scope whose declarations
exceed what it can serve, a layer or a tile" — has no record-level option, and
§18.2 resolves the metadata case explicitly ("does so at the whole file, a
document having no declared size and so no narrower scope whose declarations
that rule can measure"). No gap. ✔

### 5.2 §21.9's hard limits (`[R-ERR-05]`) against the defining sections

Name ≤ 255 bytes (§4.6) ✔ · metadata key ≤ 255 bytes (§18.2's fold of §4.6)
✔ · rank ≤ 255, C ≤ 65,535 (§7.4's u8/u16) ✔ · codec 4 decoded tile ≤
0x7E000000 (`[R-COD-07]`) ✔ · offsets/lengths/extents/counts ≤ 2⁶³ − 1
(`[R-ENC-03]`) ✔ · A power of two 512 ≤ A ≤ 2⁶² (§7.4, §16.1) ✔ · A_slab
power of two 1 ≤ A_slab ≤ 2⁶² (§7.4 — §16.2 states only "a power of two ≥ 1",
with the ceiling in §7.4's table, which is the defining layout table) ✔ · S
with 1 ≤ S ≤ 2⁶³ − 1 (§7.4, §16.2) ✔ · dir_length ≥ 4 at dir_offset ≥ 16
(§6.2) ✔ · file ≥ 128 bytes (§5.1) ✔.

I looked for limits stated elsewhere and missing here — the trailer's 64-byte
size and 64-alignment, the 24-byte record header, the 20-byte index entry, the
2¹⁶-entry segment, the "at most one user-metadata record per scope"
multiplicity, the ≥ 5 user-metadata extent_length. None is a *magnitude* limit
of the kind `[R-ERR-05]` collects, all are in Appendix B or their own sections,
and §21.9's opening declares the section "a finding aid rather than an
inventory", which withdraws any completeness claim. **No limits finding.**

The one number §21.9 flags as chosen rather than derived — "the 512 floor on A
is a number chosen here, fixed at the legacy sector size (§16.1)" — matches
§16.1's "512 is the legacy sector floor". ✔

---

## 6. Building the thing

I built a conforming file from the document alone, to find out where the
register would leave me guessing.

**Constants first.** All three published CRC values reproduce under my
independent CRC-32C (reflected Castagnoli 0x82F63B78, init 0xFFFFFFFF, final
XOR 0xFFFFFFFF):

```
crc32c("123456789") = 0xE3069283      §4.5 check vector      ✔
crc32c(<empty>)     = 0x00000000      §4.5 check vector      ✔
CRC-32C of 2¹⁶ sentinel entries = 0xEECB3BB2   §15.4         ✔
```

**Appendix A's minimal file.** I rebuilt its trailer bytes [0, 60) from the
annotation table and computed the CRC: **0xE00938D2**, stored little-endian as
`D2 38 09 E0` — byte-identical to the hex dump at offset 0x7C. The directory
region [16, 20) is the CRC of zero bytes, `00 00 00 00`. Appendix A is
arithmetically sound.

**A one-layer file.** Rank 1, E = 4, T = 2, interleaved, one uint8 channel
`v` with fill 0x00, codec 1, filter 1, no alignment, no slab.

```
G = ⌈4/2⌉ = 2   N = 2   P = 2   Q = 1   decoded size = P·Q = 2
addressed tiles = N = 2 (interleaved)
index region = 2×20 + ⌈2/2¹⁶⌉×4 = 44 bytes
layer-record inline payload = 73 bytes
  name(2) layout(1) linearization(2) codec(2) filter(2)
  A(8) S(8) A_slab(8) d(1) C(2)
  dim x: name(2) E(8) T(8) = 18
  chan v: name(2) type(2) fill(1+1) = 6
  index_encoding(1) entry_count(8) crc_of_crc_array(4)
record = 24 + 73 = 97      directory = 97 + 4 = 101
dir_offset = 64, dir_end = 165, trailer at 192, F = 256 (F mod 64 = 0)
live claimants: [0,16) [16,18) [18,20) [20,64) [64,165) [192,256)
slack = 27 bytes  (the pre-trailer pad [165,192))
```

Every claimant other than the front block and trailer lies in [16, F − 64) =
[16, 192) as `[R-LIF-08]` requires; none overlaps; the file partitions.

**Points where I had to decide something.** Only two, and both are settled by
the text:

1. The order of fields inside a channel entry — name, type, fill. §7.4's table
   gives the order, and §12.3's worked example
   (`04 74 65 6D 70 0C 00 04 00 00 C0 7F`) confirms it byte for byte: length
   prefix, name bytes, type little-endian, fill length, fill bytes. My builder
   emits the same shape.
2. Whether the layer record's stored flags must be MU = 1 / PE = 1. §7.3 fixes
   them and `[R-CNT-22]` makes a mismatch a verifier-detected violation (L49);
   I wrote 0b11.

I then wrote a verifier whose control flow is driven only by §21's rows and the
validation order §6.2 fixes, and ran it against the file: no row fires. I then
mutated the file thirteen ways, re-sealing the integrity chain each time
(segment CRC → crc_of_crc_array → directory CRC → trailer CRC) so that each
mutation reaches the row it is aimed at rather than being masked by an earlier
link:

```
clean file                 -> (no row)
front-block byte 3         -> F6      trailer magic byte 0      -> F8
trailer CRC                -> F14     generation := 0           -> F11
file_id := 0               -> F12     dir_length := 3           -> F16
tile0 payload byte         -> T1      entry0 offset := 8        -> T8
entry0 length := 0         -> T10     entry0 length bit 63 set  -> T11
entry0 half-sentinel       -> T7      entry1 sentinel + crc≠0   -> T6
entry1 := full sentinel    -> (no row)  ← R-IDX-02, §21.6 row 1
```

Each mutation attributed to exactly one row, with the outcome its governing
rule assigns, and the valid sentinel correctly produced no row at all — the
first entry of §21.6's non-violation table. **No condition I could construct
landed outside the register.**

One boundary is worth recording because I initially mis-set it. An entry with
offset 190 and length 2 in this F = 256 file has offset + length = 192 =
F − 64 exactly, and it does *not* fire T9: §15.3's condition is
`offset + length > F − 64`, so an extent ending exactly where the live trailer
begins is legal, which agrees with §9.7's half-open `[16, F − 64)` bound. My
verifier fell through to T1 on that file, which is the right answer. The
register and §9.7 use the same convention on both sides of the interval.

I checked the document's other worked arithmetic while I was in the code, since
a register that cites §14/§15 arithmetic is only as good as that arithmetic:

- §14.2's interleaved example: Q = 3, decoded 18, ordinal 5 at [15, 18); the
  float32+bool variant Q = 5, decoded 30, ordinal 5 at [25, 30). ✔
- §14.3's packed plane: P = 10 alternating from true → byte 0 = 0x55, byte 1 =
  0x01, and with fill true the pad bits 2–7 set give 0xFD. ✔
- §14.5's edge tile: extents (5,5), tiles (4,4) → the (1,1) tile holds one real
  position and 15 padding, 32 bytes, values 1–15 each `CD AB`. ✔
- §17.3's shuffle: `00 00 80 3F 00 00 00 40 00 00 40 40` at s = 4, n = 3 →
  `00 00 00 00 00 00 80 00 40 3F 40 40`. ✔ (matches the document exactly)
- §15.4's index example: 16 segments, 64-byte CRC array, region 20,000,064
  bytes, tile 999,999 at segment-relative byte 339,180, segment 15 at
  [19,660,800, 20,000,000), one full segment = 1.25 MiB. ✔
- §15.4's planar example: C = 4, N = 32, channel 2 at s = 10 → disk ordinal 74,
  entry at [1,480, 1,500); channel 3 unstored → entries 96–127. ✔
- §20.3's example: 32 · 20 + 4 = 644-byte index region. ✔
- §11.4's example: (300, 700) → tile (1,2), s = 10, in-tile (44, 188). ✔

---

## 7. Findings

### register-01 — OBSERVATION

**§21.4, row T24/T23; §17.2 `[R-COD-07]`.**

T23 registers the LZ4-frame-instead-of-block condition with Detector = reader,
Detected = tile use, outcome reject-tile, Governing rule `[R-COD-07]`:

> | T23 | Codec 4 (lz4) and the stored bytes are an LZ4 frame (magic 04 22 4D 18) instead of exactly one raw LZ4 block | — | reader | tile use | `[R-COD-07]` |

`[R-COD-07]` states no reader procedure for this condition. Its whole text on
the point is a definition —

> The stored bytes are exactly one LZ4 block per the LZ4 Block Format
> Description (lz4_Block_format.md, version 1.0; Appendix F pins the exact
> revision), decoded with the stored length as the input size and the decoded
> size as the output capacity. The LZ4 frame format is not used.

— and the only reader obligation `[R-COD-07]` imposes is on the decoded-size
cap ("a reader MUST treat such a declaration as a validity error at layer
scope"), which the register carries separately as L44. Compare `[R-COD-06]`,
which for zstd *does* give the parallel magic check a reader procedure ("a
reader MUST treat a payload whose first four bytes are not that magic … as a
validity error at tile scope"), and which the register carries as T17.

Four other rows register a condition whose detection belongs to a different
row, and all four say so in the cell: T13 ("the check that detects it is
T25's, and this row records the cause rather than a procedure of its own"),
T15 ("the check that detects it is T24's or T25's, and this row records the
cause…"), T16 ("the check that detects it is T24's…"), T26 ("the check that
detects it is T2's or T4's…"). T23 is the fifth such row and carries no
annotation.

Permitted readings: (a) T23 obliges a conforming reader to compare a codec-4
tile's first four bytes against `04 22 4D 18` and reject-tile on a match; (b)
T23 records a cause, and the detection is `[R-COD-08]`'s (T24/T25). I picked
(b), because §21.1 is explicit that "each row *restates* its governing rule,
and where a row and the rule it cites diverge, **the rule governs**", and
`[R-COD-07]` imposes no such reader check.

Nothing turns on the choice at the byte level, and I verified rather than
assumed this. An LZ4 frame always begins `04 22 4D 18`; decoded as an LZ4
block, the token 0x04 means zero literals and a match length of 8, after which
the decoder reads a two-byte little-endian offset from `22 4D` = 19,746 into an
output buffer holding zero bytes — invalid at every stride, for every tile, in
every file. So a reader taking reading (b) always reaches reject-tile via T25,
at the same tier and with the same outcome as a reader taking reading (a). The
defect is that a reader implementing the register literally adds a magic check
no requirement asks for, and that the register's own convention for marking
cause-rows is applied to four rows and not the fifth.

*Byte-level: no.* Both readings reject the same tile at the same tier with the
same outcome; the condition is unconditionally detected either way.

### register-02 — OBSERVATION

**§21.1's instance criterion, against §21.4 T14/T3 and §21.2 F7/F33.**

§21.1 states the criterion for what an Instances cell enumerates:

> What a cell enumerates is the condition's own alternatives and containers: a
> row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them (T15,
> T25).

Two pairs of rows apply this criterion in opposite directions to conditions of
the same shape.

**T3 versus T14.** T3 compares a length against the tile's decoded size and
enumerates six:

> | T3 | The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations | interleaved P·Q, payload longer; interleaved P·Q, payload shorter; planar numeric P·Bᶜ, payload longer; planar numeric P·Bᶜ, payload shorter; packed planar bool ⌈P/8⌉, payload longer; packed planar bool ⌈P/8⌉, payload shorter | reader | tile use | `[R-SER-07]` (R-COD-08) |

T14 compares a length against the tile's decoded size and enumerates one:

> | T14 | Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size | — | reader | tile use | `[R-COD-04]` |

T14 ranges over the same three decoded-size formulas — a codec-1 layer may be
interleaved, planar numeric, or a packed planar bool plane — and admits the
same longer/shorter alternatives. Whatever grounds T3's six, grounds T14's six;
whatever grounds T14's one, grounds T3's one.

**F7 versus F33.** F33 enumerates the claimant families a byte-range collision
can involve:

> | F33 | A byte of the live committed state is claimed by two structures that do not belong to the same layer … | stored-tile extents; tile-index regions; record extents; sub-record extents; directory region | verifier | certification | `[R-CNT-13]` (R-CNT-02, R-IDX-03) |

F7 is the same kind of range test against the pre-trailer gap and enumerates
none:

> | F7 | A structure occupies bytes between the live directory's end and the live trailer | — | verifier | certification | `[R-CNT-05]` (R-CNT-02) |

The structures that can sit in that gap are the same families F33 lists.

Permitted readings of §21.1's criterion: (a) "materially different shapes"
means the *check* changes shape, in which case T3 over-enumerates and F33
over-enumerates, both being single range or length comparisons; (b) it means
the *vector construction* changes shape, in which case T14 and F7 under-
enumerate. I picked (b), because T15 and T25 — the two rows §21.1 names as
correctly enumerating — are rows whose check is a single "does it decode"
call and whose *construction* is what differs by codec. Under that reading
T14 should read six and F7 five, and §21.8's stated totals would be 121
conditions over 258 instances rather than 248.

The counting itself is not the defect: §21.1 says "the count is therefore
mechanical once the cell is written", and I confirmed both stated totals
reproduce exactly from the cells as written (§1 above). The defect is that the
cells are not written to one criterion, so §21.8's per-instance corpus
obligation — "one vector per instance", restated by `[R-VEC-03]` as "at least
one vector for each instance it names" — yields six vectors for T3 and one for
T14 for conditions an implementer would write one comparison for.

*Byte-level: no.* Nothing here changes a row's outcome, detector, tier, or
governing rule; it changes only how many files a conforming corpus must
contain, and §24 `[R-VEC-01]` already makes the corpus derivative of the
specification rather than constitutive of it.

---

## 8. What I could not determine

Nothing in my charter was left undetermined by the document. The two places I
had to reason past the text rather than read it off — whether `[R-LIF-02]`'s
step-3 obligation belongs in §21.7's omitted set, and whether T26's exclusion
of T5 was a broken cross-reference — both resolved in the document's favour,
the first because §21.1 characterises §21.7 as an account "by class" rather
than by requirement, the second by the arithmetic in §5 above.

I did not attempt to audit sections outside §21 except where a rule the
register cites lives there. One thing I noticed in passing and am recording
without claiming it as a finding, since it lies outside my charter and inside a
non-normative appendix: Appendix G item 3 fixes a total emission order —
"Records are ordered by type, and within type 0x0001 by layer name; a layer
record's sub-records are ordered by type, and within a type by their encoded
bytes compared lexicographically" — and the lexicographic tiebreak is attached
grammatically to sub-records only, so two *top-level* records sharing a
non-0x0001 type have no order fixed by the profile. In practice the case is
unreachable for released software, since §10.3 bars experimental types from
published data and `[R-CNT-14]` permits at most one top-level type-0x0002
record.

## 9. Confidence

High that an implementation built from §21 plus the rules it cites would
interoperate. The register's 121 rows all agree with their governing rules on
outcome, scope, detector, and tier; both stated totals reproduce; every row
citation and every citation *to* a row resolves; the outcome vocabulary is
closed and fully reachable; the limits agree in both directions; and a file
built from the document alone passes every row while nine deliberate mutations
each attribute to exactly one.
