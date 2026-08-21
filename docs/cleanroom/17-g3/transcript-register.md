# Round 17 — Register hunter — working transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,317 lines, in five `Read` calls plus targeted `grep`s against that same
file). I opened no ADR, no `docs/`, no `PLAN.md`, `AGENTS.md`, `README.md`,
`OPEN-QUESTIONS.md`, no `conformance/` material, no `spec/registry.json`, no git
history, no web resource. I did not list the output directory and did not read
any other agent's transcript.

Local computation I ran, reading no files: a Python CRC-32C implementation used
to reproduce every checksum constant the document states; Python scripts that
parse the register tables out of the one file I am permitted to read and count
rows, semicolon-separated instances, detectors and detection points; hand
arithmetic on the geometry and byte-layout worked examples. The scripts were
typed inline into `bash` heredocs; no scratch file was created other than this
transcript.

---

## 0. How I worked

I read §21 first, end to end, then read the whole document front to back so that
every row's governing rule was in hand. Then four passes:

1. **Counting** — mechanical reconstruction of §21.2–§21.5's row and instance
   totals from the table text, and re-derivation of §21.8's `121 conditions over
   273 instances`.
2. **Row-versus-rule** — for all 121 rows, locate the governing requirement,
   compare condition wording, outcome class, scope, detector, detection point.
3. **Completeness both ways** — sweep every `validity error`, `reject-*`,
   `ignore-record`, `nonconforming`, `Writers MUST` / `MUST NOT emit` occurrence
   in the document and check each maps to a row, to §21.6, or to §21.7's account;
   then check no row registers a condition the rules do not make a violation.
4. **Build it** — walk the reader/verifier/updater algorithms against concrete
   constructed files, and note every point where I had to guess.

Findings are numbered `register-01`…`register-06` and appear in full at §6 below.

---

## 1. The counting

§21.1 fixes the arithmetic: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written."

I parsed every table line in §21.2–§21.5 whose first cell matches `[FLTR]\d+`
and counted `cell.count(';') + 1`.

```
F rows 36  instances 58
  F1=2 F2=6 F3=2 F4=1 F5=2 F6=2 F7=4 F8=1 F9=1 F10=1 F11=1 F12=1 F13=1 F14=1
  F15=1 F16=1 F17=2 F18=1 F19=1 F20=1 F21=1 F22=1 F23=2 F24=1 F25=1 F26=1
  F27=1 F28=2 F29=3 F30=2 F31=1 F32=1 F33=5 F34=1 F35=1 F36=1
L rows 49  instances 116
  L1=8 L2=9 L3=1 L4=2 L5=1 L6=1 L7=2 L8=2 L9=2 L10=1 L11=1 L12=2 L13=1 L14=3
  L15=4 L16=2 L17=2 L18=3 L19=1 L20=1 L21=4 L22=4 L23=4 L24=1 L25=1 L26=1
  L27=1 L28=1 L29=3 L30=2 L31=3 L32=3 L33=4 L34=4 L35=1 L36=2 L37=1 L38=1
  L39=3 L40=1 L41=3 L42=1 L43=3 L44=3 L45=3 L46=2 L47=2 L48=1 L49=4
T rows 26  instances 55
  T1=1 T2=1 T3=6 T4=4 T5=1 T6=1 T7=2 T8=1 T9=1 T10=1 T11=2 T12=1 T13=2 T14=6
  T15=2 T16=1 T17=1 T18=2 T19=1 T20=1 T21=3 T22=6 T23=1 T24=1 T25=3 T26=3
R rows 10  instances 44
  R1=4 R2=2 R3=2 R4=12 R5=8 R6=4 R7=6 R8=2 R9=2 R10=2
TOTAL rows 121  instances 273
```

Against the document's own totals:

| Claim | Stated | Recomputed |
|---|---|---|
| §21.2 "36 conditions" | 36 | 36 ✓ |
| §21.3 "49 conditions" | 49 | 49 ✓ |
| §21.4 "26 conditions" | 26 | 26 ✓ |
| §21.5 "10 conditions" | 10 | 10 ✓ |
| §21.8 "121 conditions over 273 instances" | 121 / 273 | 121 / 273 ✓ |

Row labels are contiguous in each subsection (F1–F36, L1–L49, T1–T26, R1–R10),
no gaps, no duplicates, and no two rows carry byte-identical Condition text.
**Every total in §21 reproduces exactly.** I record this as a clean result
because a total that does not reproduce would be a finding even at a discrepancy
of one.

### 1.1 Was each cell written to §21.1's criteria?

The count is mechanical *given the cell*; §21.1's criteria govern how the cell is
authored. I checked every cell against the two stated axes.

**Layout axis** — "Where the quantity a condition derives varies by layout, the
layout formulas are materially different shapes and the cell enumerates them."
Applied consistently at the three shapes §14 gives (interleaved `P·Q`, planar
numeric `P·Bᶜ`, packed planar bool `⌈P/8⌉`): T3 (×2 directions = 6), T14 (6),
T21 (3, one direction), T22 (6), L44 (3, one direction), T4 (4 — numeric split
by layout), T26 (3). L21 splits by layout too (`N` interleaved, `C·N` planar,
× 2 directions = 4). No layout-varying quantity is collapsed anywhere.

**Magnitude axis** — "*differs from* or *does not equal*" → two directions;
"*exceeds*, *larger than*" → one; a checksum-or-constant comparison → none; a
nonzero test → none. Verified row by row. Spot checks that could have gone
wrong and did not: F23 / L12 (`inline_length is not 1`) correctly enumerate
`inline_length 0` and `inline_length ≥ 2` — the two directions; L30
(`differs from the element size`) gives longer/shorter; F17 (`does not equal
the transport-authoritative file size`) gives shorter/longer; L37, L38, T1,
F14, F20 (checksum comparisons) each give one; L20 (`both A ≠ 0 and S ≠ 0`),
L27, L28 each give one, per "a field tested only for being nonzero … is a value
test and not a comparison of two quantities at all" and "a single predicate over
several fields … the fields it reads are not instances".

**The one judgment call I could not derive.** L41's condition is a `≠` over two
magnitudes, which the magnitude axis would settle at two directions; the cell
gives three (`gap; overlap; out-of-ordinal placement`). This is defensible under
the *other* criterion — "one of several alternatives the condition text states",
and the condition text does state three — and the two magnitude directions are
covered (gap = greater; overlap and out-of-ordinal = two refinements of lesser).
Three distinguishable files exist. I did not file this: the axes are stated as
axes that "recur often enough to be stated rather than judged each time", not as
an exhaustive decision procedure, and the alternatives criterion is a first-class
criterion in the same paragraph. But I record that a second author working from
§21.1 alone could have written `2` here and produced a corpus of 272, and that
§21.8's 273 is therefore not fully derivable from §21.1 — it is derivable from
the cells as written, which is what §21.1 actually claims.

### 1.2 Detector / detection-point vocabulary

§21.1: "Detection points name §19.2's reader tiers — open, layer access, tile
use, extent use — or *certification* for the rows a verifier detects, which
§19.2 places outside the reader tiers entirely."

Mechanical check over all 121 rows:

- Detectors: `reader` 101, `verifier` 20. No third value.
- Detection points: `layer access` 35, `open` 32, `tile use` 24,
  `certification` 20, `extent use` 9, and R1's compound
  `open (top-level); layer access (sub-record)` 1.
- **Zero anomalies**: every `verifier` row is `certification`, every `reader`
  row names a §19.2 tier. R1's compound names two tiers, one per container,
  which is the only sensible reading and is consistent with §19.2's structure.

### 1.3 The outcome vocabulary

§2.4 `[R-CNF-07]` defines exactly four reader outcomes — reject-file,
reject-layer, reject-tile, ignore-record — plus **preserve-verbatim** as an
updater obligation "orthogonal to reader outcomes".

- Every row's outcome comes from its subsection heading, and all four
  subsections exist: §21.2 reject-file, §21.3 reject-layer, §21.4 reject-tile,
  §21.5 ignore-record. **All four defined reader outcomes are reachable, and no
  row carries an outcome outside the vocabulary.**
- preserve-verbatim is correctly kept out of the register (it binds updaters, not
  readers) and §2.4 points at §20.4's table for its cases: "its MU = 1 and
  MU = 0 / PE = 1 rows". §20.4's table does carry exactly those two rows plus the
  MU = 0 / PE = 0 droppable row. Reachable ✓.

The one place where a subsection heading over-reaches is §21.4's: "Outcome:
reject-tile — that tile's read reports failure, and never returns fill in place
of data (`[R-CNF-09]`)." Four §21.4 rows carry detector *verifier* (T2, T4, T5,
T26), and for those no reader is obliged to fail the read — `[R-SER-08]`
expressly tells a reader that returns the value what to return. I did **not**
file this: §21.1 already adjudicates it in terms ("For a row whose Detector is
*verifier*, the outcome names the scope at which the damage is recorded, not an
obligation on any reader … `[R-SER-08]` is the one rule that goes the other
way"), and `[R-CNF-09]` itself carries the qualifier "and whose rejection this
reader is obliged to detect". This is exactly the over-claim shape the brief
names, and the document has already decided it.

---

## 2. Row-versus-rule, all 121 rows

I walked every row to its governing requirement. Recorded here are the checks
that could have failed; the rest agreed on wording, outcome, scope, detector and
tier.

**Trailer rows F8–F17 against `[R-CNT-06]`.** §6.2's ordered gate list is:
magic (F8); trailer CRC (F14); version gate (F18/F19 via §6.3); then
committed_file_length = file size (F17) and multiple of 64 (F13); dir_offset ≥ 16
(F9); dir_length ≥ 4 (F16); dir_offset + dir_length ≤ F − 64 (F10);
1 ≤ generation ≤ 2⁶³ − 1 (F11 for the floor, F2 for the ceiling); file_id ≠ 0
(F12); reserved bytes zero (F15). Every gate has a row and every row a gate.

**F5 / `[R-CNT-27]`.** I re-derived the 128-byte floor rather than taking it:
dir_offset ≥ 16 and dir_length ≥ 4 put the directory's end at ≥ 20;
dir_offset + dir_length ≤ F − 64 gives F ≥ 84; F ≡ 0 (mod 64) gives F ≥ 128. ✓

**F19 / `[R-CNT-08]`.** I checked that "this text defines no flag bits, so every
such bit is unimplemented" survives the extension surface: §4.3 and §10.1 both
list *ignore-lane* bits only as a growth vehicle, so no minor version can define
an incompat-lane bit, and a file declaring a later major is refused at the
version gate before the flag gate. F19 is sound, and the ignore-lane counterpart
is correctly a non-violation (§21.6, `[R-CNF-02]`).

**F33 / L18 against `[R-CNT-13]`'s three overlap classes.** intra-layer →
reject-layer → L18; across layers or touching another scope → reject-file → F33;
two non-layer structures → reject-file → F33. Both rows' condition text matches
the rule's partition exactly, and F33's escape clause ("a claimant reaching the
front signature block or the live trailer is instead caught by the bounds rows
F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier") resolves: F9/F10 the
directory, F31/F32 non-layer record extents, L16/L17 layer record and sub-record
slots, T8/T9 tile-index entries. Four claimant kinds, four row pairs, no gap.

**§15.3's classification table against T1, T6–T12, L18, L40–L42, F33.** Eleven
rows in §15.3; I mapped each: valid sentinel → §21.6; sentinel with crc ≠ 0 →
T6; exactly one half sentinel → T7; length = 0 → T10; offset < 16 → T8;
offset or length > 2⁶³ − 1 → T11; sum overflows → T12; sum > F − 64 → T9;
stored bytes fail crc → T1; intra-layer overlap → L18; extra-layer overlap →
F33; alignment/slab invariant → L40/L41/L42. **Complete, both directions.**

**`[R-CNT-23]`'s constraint set against L1, L27–L36, L39, L43, L45.** Field by
field from §7.4's table: name (L3/L5/L6, F4), layout (L36), linearization (L33),
codec (L43), filter (L45), A (L39), S (L1 ceiling), A_slab (L28, L29), rank d and
C (L32), dimension extents (L1), tile extents (L32, L1), channel type (L34), fill
length (L30), bool fill (L35), index_encoding (L31), entry_count (L21, L1),
crc_of_crc_array (L27), sub-records (L13, L14, L19, L24, L25, L26). Every table
constraint has a row.

**Value-set rows against §10.2's partition table.** L31 (index encoding: 0,
2–0x7F, ≥0x80 = 3), L33 (linearization: 0, 2–3, 4–0x7FFF, ≥0x8000 = 4 — the
split at 3 tracks §11.4's own two-part text), L34 (type: 0, 14–19, 20–0x7FFF,
≥0x8000 = 4, tracking §12.2), L36 (layout: 0, 3–255 = 2 — correctly no
experimental instance, since `[R-EXT-02]` gives channel layout no experimental
range), L43 (codec: 3), L45 (filter: 3), R1 (metadata encoding 0 and 3–0x7F = 2
alternatives × 2 containers). All agree with §10.2 and with the defining
sections.

**Codec rows T14–T25 against §17.2.** `[R-COD-04]` → T14; `[R-COD-05]` →
T15, T16; `[R-COD-06]` → T17 (magic), T18 (second/skippable frame), T19
(dictionary ID), T20 (content checksum), T21 (window > decoded size), T22
(FCS ≠ decoded size); `[R-COD-07]` → T23 and L44; `[R-COD-08]` → T24, T25;
`[R-COD-02]` → T13. The undisclosed-dictionary case §17.2 calls out as
undetectable is correctly *not* registered and is named in §21.7.

**`[R-MTA-09]`'s frame constraints against R4.** §18.2 lists the `[R-COD-06]`
constraints "that do not reference a tile": frame magic; no skippable frame and
no second frame; no nonzero dictionary ID; no content-checksum flag — plus "the
single frame occupying the extent's bytes before its terminal CRC". That is six
alternatives; R4's cell enumerates exactly six (`missing frame magic; a
skippable frame; a second frame; a nonzero dictionary ID; the content-checksum
flag set; bytes remaining after the frame`) × 2 containers = 12. ✓ The two
tile-referencing constraints (window size, Frame_Content_Size) are correctly
absent.

**`[R-MTA-04]`'s four restrictions against R5–R10.** object + no BOM → R7 (3
alternatives × 2 containers); finite numbers → R8; no duplicate keys → R9;
well-formed UTF-8 throughout → R5, and §4.6's key rules folded on → R6 (empty,
C0) and R10 (>255 bytes). ✓ Nothing in §18.2's bulleted restrictions lacks a
row, and no R row registers something §18.2 does not require.

### 2.1 Divergences I looked for and did not find

- **L46/L49 and F25/F28 overlap.** A layer record stored with MU = 1 / PE = 0
  exhibits both L46 and (because §7.3 fixes PE = 1 for type 0x0001) L49. I
  checked whether §21.1's specialization list ("F1 of F6 and of F8, F35 of F36,
  L24 of L25") is therefore incomplete. It is not: L46 and F25 also range over
  *unregistered* types, for which no registry value exists, so neither row is a
  strict specialization at row granularity. The list holds.
- **T2 / T4 and `[R-SER-08]`.** T2 says "the same byte at a padding position is
  T4's, the two rows together covering `[R-SER-08]`". I verified this closes:
  at a padding position `[R-SER-05]` requires the *recorded fill byte*, and
  `[R-TYP-07]` constrains a bool fill to 0x00 or 0x01, so any byte that violates
  `[R-SER-08]` there also violates `[R-SER-05]` and fires T4. Nothing falls
  through.
- **T26's "the check that detects it is T2's or T4's" — why T5 is correctly
  absent.** For a packed planar bool plane the mandated stride is s = 1 and the
  filter is the identity, so a mis-strided writer's output reaches the reader
  unshuffled. I worked the permutation: byte at offset `j·s + i` moves to
  `i·n + j`, so offset 0 → 0 and offset `L − 1 = (n−1)s + (s−1)` →
  `(s−1)n + (n−1) = L − 1`. **The final byte is a fixed point of every stride.**
  The pad bits live in the final byte, so a wrong stride can never disturb them
  and T5 can never be the witness. T26's enumeration of T2 and T4 is exactly
  right, and I would have filed a false positive here had I not done the
  arithmetic.
- **L44 quantifier.** `[R-COD-07]` quantifies over "addressed tiles"; L44 says
  "any of whose addressed tiles' decoded size exceeds 0x7E000000 — in a planar
  layer the largest channel plane governs", matching §17.2 word for word,
  including the empty-layer escape §17.2's Note and §20.3's growth permission
  both rely on. Agrees.

---

## 3. Completeness in both directions

### 3.1 Rules → rows

I swept every occurrence of `validity error`, `reject-file`, `reject-layer`,
`reject-tile`, `ignore-record` and `nonconforming`, and separately every
`Writers MUST` / `MUST NOT emit` / `a writer MUST` in the document, and assigned
each to a row, to §21.6, to §21.7, or to a conduct carve-out.

Requirement IDs with no row, and where each is accounted for:

| Rule | Account |
|---|---|
| `[R-ENC-05]`, `[R-ENC-10]`, `[R-ENC-13]`, `[R-GEO-04]`, `[R-TYP-04]`, `[R-TYP-09]`, `[R-MDL-02]` | reader behavior, not a file state |
| `[R-ENC-06]` | §21.7 — "not a state a file can be in" |
| `[R-ENC-14]`, `[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-TYP-10]`, `[R-LIF-07]` | SHOULD-level; `[R-CNF-12]` excludes them from the register by design |
| `[R-LIF-01]`, `[R-LIF-03]` | §21.7 — history properties |
| `[R-GEO-06]`, `[R-SER-01]` | §21.7 — ordinal mappings |
| `[R-CNT-13]`'s MU = 0 embedded-offsets bar | §21.7 — opaque by construction |
| `[R-CNT-18]`'s nesting bar | §21.7 — no format-major-1 parse witnesses it |
| §20.3 step 4's declaration bar | §21.7 — witnessed only where §21.4's content rows or T3/T14 fire |
| `[R-SLB-04]` | §16.2's Note — detection *is* `[R-SLB-03]`'s, so L41/L42 are the rows |
| `[R-CNT-05]`'s over-long pre-trailer gap | `[R-CNF-02]` — expressly not a file-conformance violation |
| §6.3's flags = 0 against a set ignore-lane bit | `[R-CNF-02]` — same |
| §10.3 experimental publication, §18.3 registry targeting | `[R-CNF-02]` — writer conduct |
| `[R-CNT-02]`'s "belongs to no class" half | §5.2's Note — "a row no file could exhibit" |

Two IDs are named nowhere in §21.7 and have no row: **`[R-IDX-01]`** (entry k
lies at region byte 20·k, entry order is disk-ordinal order) and
**`[R-ENC-01]`/`[R-ENC-02]`**'s general little-endian obligation beyond the
signature (F1). I did not file either. `[R-IDX-01]` is the same mapping
`[R-GEO-06]` states and §21.7's named class ("the ordinal mappings … satisfied
by a structurally valid tile whatever values it carries") covers it;
`[R-ENC-01]` falls in the class §21.7 names via `[R-ENC-06]` — the parse is
always at the fixed endianness, so a big-endian field simply holds a different
value, caught by the rows for the field that holds it. §21.1 licenses this:
§21.7 is "the account, **by class**, of what fails it", not an inventory of IDs.

**Result: I found no detectable file-conformance violation the register omits.**

### 3.2 Rows → rules

Every row registers a condition some MUST-level rule actually prohibits. The
three I probed hardest:

- **F18** (version_major = 0). Not merely a capability refusal: §6.2's table
  makes 0 invalid and §21.6's closing paragraph explicitly separates it from the
  two conforming-file-refused cases. Correctly registered.
- **F19** (incompat-lane bit). A violation because `[R-CNT-08]`'s flags = 0
  obligation is carved out only for the *ignore* lane. Correctly registered.
- **R1** (metadata encoding 0 or reserved). `[R-MTA-10]` withdraws content
  rules, never `[R-MTA-03]`'s value set, and `[R-EXT-03]` makes a reserved value
  "MUST NOT be emitted at all". Correctly registered, and the experimental
  counterpart is correctly a §21.6 non-violation.

**No row registers a non-violation.** §21.6's fourteen entries were checked
against their cited rules individually; all fourteen hold, and the two conditions
the closing paragraph says were promoted out of §21.6 (`[R-MTA-05]` unsorted
documents; `[R-CNT-22]` stored-flag mismatch) do appear above as F27/L48 and
F28/L49 with detector *verifier*.

---

## 4. Every cross-reference to a row

I grepped the whole file for row labels used outside the register tables and
resolved each against the row it names.

| Citation | Site | Resolves? |
|---|---|---|
| "L18's overlap or L40 through L42's placement" | §5.2 | ✓ all four verifier-detected, layer-scope, established by the coverage walk |
| "§21.2 rows F8 and F17" | §9.6 | ✓ trailer magic; committed_file_length vs transport size |
| "(§21.4, T24)" | §17.2's DEFLATE note | ✓ T24 is exactly "bytes remain in the stored extent after the stream … ends" |
| "(L44)" | §20.3 step 4 | ✓ the lz4 decoded-size cap |
| "F1 of F6 and of F8, F35 of F36, L24 of L25" | §21.1 | ✓ each verified a strict specialization |
| "T24's *any codec*"; "(T15, T25)" | §21.1 | ✓ T24 = 1 instance; T15 = 2, T25 = 3 |
| "F27 and L48" | §21.1 | ✓ both are the `[R-MTA-05]` rows (see note below) |
| "F8 and F1's trailer-magic instance, F14's trailer CRC … F6 with F1's front-block instance" | §21.2 preamble | ✓ and the count "Four rows" is right: F8, F1, F14, F6 |
| "F9/F10, F31/F32, L16/L17 and T8/T9" | F33 | ✓ four claimant kinds, four tiers |
| "(F36, L25)" | §21.6 row 5 | ✓ the MU-agnostic reserved-range rows, correct for an MU = 0 subject |
| "(F18, `[R-CNT-07]`) … (F35, F36, L24, L25)" | §21.6 closing | ✓ |
| "T2, T4 or T5" | §21.7 | ✓ interleaved bool byte; padding content; pad bits |
| "T3 or T14, which read the index entry rather than the decoded image" | §21.7 | ✗ — see **register-02** |
| "(F1, F6)"; "(`[R-CNT-05]`, F7)"; "(`[R-CNT-15]`, F36, L25)"; "(R1)" | Appendix H | ✓ all four |
| "which §21.3 registers" | §16.2 Note (stale slab declaration) | ✓ L41/L42 |
| "§21.3 registers in its own right" | §7.4 Note (layer record as sub-record) | ✓ L26 |

One weak spot I inspected and let stand: §21.1's parenthetical
"(`[R-CNT-22]`, whose registered type keeps its fixed semantics; and
`[R-MTA-05]`, whose unsorted document readers process as they find it — F27 and
L48)" names row labels for `[R-MTA-05]` only, leaving `[R-CNT-22]`'s F28 and L49
unnamed. The sentence opens "for several such rows", so it is offering examples
rather than an inventory, and both row pairs are correctly present in the tables.
Not filed.

---

## 5. Building it end to end, and where I had to guess

### 5.1 Constants reproduced

I implemented CRC-32C (poly 0x1EDC6F41 reflected → 0x82F63B78, init/final
0xFFFFFFFF, reflected in and out) from §4.5 alone and reproduced **every**
checksum constant the document states:

```
CRC-32C("123456789")            = 0xE3069283   ✓ §4.5 check vector
CRC-32C("")                     = 0x00000000   ✓ §4.5, and Appendix A's [16,20)
Appendix A trailer [0,60)       = 0xE00938D2   ✓ Appendix A byte table
§7.4's 4-sentinel entry array   = 0x80A34955   ✓ stored `55 49 A3 80`
CRC of that 4-byte array        = 0xC4EE982E   ✓ crc_of_crc_array, stored `2E 98 EE C4`
2¹⁶ sentinel entries            = 0xEECB3BB2   ✓ §15.4, Appendix B
```

The Appendix A trailer reproduces byte for byte from §6.2's layout with no
guessing: I assembled magic ‖ u16 1 ‖ u16 0 ‖ u32 0 ‖ u64 1 ‖ u64 16 ‖ u64 4 ‖
u64 128 ‖ u64 0x0123456789ABCDEF ‖ 4 zero bytes and got the stated CRC. This is
a strong end-to-end check on §4.1, §4.2, §4.5 and §6.2 together.

### 5.2 The §7.4 layer record

Re-derived independently from §7.4's table: name 4 + nine scalars 34 (1+2+2+2+
8+8+8+1+2) + one dimension entry 18 (1+1+8+8) + one channel entry 12 (1+4+2+1+4)
+ trailing 13 (1+8+4) = **81**, matching the stated `inline_length = 81` and
every annotated offset. Grid ⌈100/32⌉ = 4 ✓. Extent length
4×20 + ⌈4/2¹⁶⌉×4 = **84** ✓. The `temp` channel entry is byte-identical to
§12.3's twelve-byte example. Nothing to guess.

### 5.3 A planar layer with a bool channel, worked

To exercise §14.3, §15.1 and §21's tile rows together: rank 1, T = 4, E = 10,
layout planar, C = 2 (`m` bool, `v` uint16). G = ⌈10/4⌉ = 3, N = 3, P = 4,
addressed-tile count = C·N = 6, entry_count = 6, index region
6×20 + 1×4 = 124 bytes. Channel 0's plane decodes to ⌈4/8⌉ = 1 byte; channel 1's
to 4×2 = 8 bytes. Disk ordinals 0–2 are channel 0, 3–5 channel 1
(`c·N + s`). Tile at ordinal 2 covers x = 8..11: real x = 8, 9; padding x = 10,
11 (bits 2–3 must be the fill bit, `[R-SER-05]`); pad bits 4–7 must be the fill
bit too (P mod 8 = 4). Under filter 2 the stride is s = 1 and the filter is the
identity. Every step was determined by the text; **no guess required.**

### 5.4 Growth and shrink under §20.3 step 4

This is where the document made me stop and re-read four times, and where I
found **register-01**. §20.3's bar and both of its permissions are quantified
over "the generation this commit supersedes", and §20.3 says so three times,
including "the quantifier is the superseded generation's, so a shrink that turns
real positions into padding of a tile stored there is barred whether or not the
new state still stores it." §11.1's Rationale, which purports to restate the same
rule, quantifies it over "a tile the new state still stores" — the opposite
domain. Construction and analysis in §6 below.

I also checked the growth permission against the bar's own list and satisfied
myself it is consistent: growing Eᵢ leaves P, the decoded size, every in-image
byte offset, and the codec and filter untouched, and *shrinks* the padding set —
which the bar's escape clause ("the list names where that effect arises rather
than standing on its own") plus the explicit growth permission together license.
The renumbering of disk ordinals when a grid count rises is handled at §20.3
step 4 and §11.1's Rationale alike.

### 5.5 Compaction over a structurally-broken index entry

Second place I had to guess, and the source of **register-03**. Constructed
input: a layer with entry_count = 2, entry 0 a valid stored tile, entry 1 with
offset = 0xFFFF_FFFF_FFFF_FFFF and length = 5 — §15.3's third row, *structural*
reject-tile, register row T7. I then ran `[R-WRT-09]`'s obligations over it: the
open passes; §19.3's layer-record validation does not classify entries; the index
chain (`[R-IDX-04]`) passes, because the segment CRC is over the entry bytes as
stored, broken or not; and "every stored tile's entry crc" has nothing to check
for entry 1, which addresses no stored tile. So no `[R-WRT-09]` check fails, and
the compactor must decide between `[R-WRT-06]`'s "Where the table does not
license a drop the compactor MUST refuse" and `[R-WRT-07]`'s instruction to
reproduce the entry and let "the violation travel with it into the output". I
could not settle this from the text.

### 5.6 Limits, both directions

I checked every limit in §21.9 against its defining section and every limit
statement elsewhere against §21.9.

*Hard limits.* Name ≤ 255 bytes (§4.6 `[R-ENC-12]`) ✓; user-metadata key ≤ 255
bytes (§18.2's fold of §4.6) ✓; rank ≤ 255 and C ≤ 65,535 (§7.4's u8 and u16) ✓;
lz4 decoded tile ≤ 0x7E000000 — §17.2 says "exceeds", so equality is legal and
"at most" is right ✓; every offset/length/extent/count ≤ 2⁶³ − 1 (§4.2) ✓;
A a power of two in [512, 2⁶²] and A_slab a power of two in [1, 2⁶²] (§7.4,
§16.1, §16.2) ✓; S in [1, 2⁶³ − 1] (§7.4, §16.2) ✓; dir_length ≥ 4 at
dir_offset ≥ 16 (§6.2) ✓; file ≥ 128 bytes (§5.1) ✓. Appendix B restates all of
these and agrees.

Limits stated elsewhere and *not* in §21.9: user-metadata extent_length ≥ 5
(§7.1); user-metadata inline_length exactly 1 (§18.2); trailer 64 bytes; record
header 24 bytes; index entry 20 bytes; segment 2¹⁶ entries. §21.9 licenses the
omissions in terms — "a finding aid rather than an inventory". Not findings.

*Minimum guarantees.* The table's eight rows agree with every citation:
§2.3 and §2.5 (`[R-CNF-10]`), §17.2's 8 MiB Window_Size, §18.2's 16 MiB
document bound, §24 `[R-VEC-03]`'s note that the tile-count bound is not
constructible, Appendix B's one-line restatement, Appendix H, and §1's
"§21.9's tile-count guarantee". I checked the Note's arithmetic: 2³² entries →
2¹⁶ segments → 2¹⁶ × 4 = **256 KiB** CRC array ✓, and 2³⁶ → 2²⁰ × 4 = **4 MiB**
✓; 65,536 layers × 200 bytes = 13,107,200 = **12.5 MiB** ✓; 256 MiB is 16× the
16 MiB top of §11.3's "ordinary" range, which the Note calls "an order of
magnitude" — loose but not wrong. I also checked the two guarantees are jointly
satisfiable: a minimal layer record is 24 + 73 = 97 bytes, so 65,536 of them is
≈ 6.1 MiB, inside the 16 MiB directory guarantee.
§24's "tens of gigabytes" for the 2³² index region: 2³² × 20 = 85.9 GB ✓.

One statement in `[R-ERR-04]` reads wider than the rule it cites — see
**register-06**.

---

## 6. Findings

### register-01 — CONTRADICTION — §11.1's Rationale states §20.3's shrink bar over the wrong generation

**Location.** §11.1 (Rationale following `[R-GEO-02]`); §20.3 step 4
(`[R-WRT-04]`); §21.7 (`[R-ERR-01]`).

**Quotation (§11.1).**

> §20.3 states normatively, and governs, what a commit may do to a layer that
> already stores tiles: a shrink is barred wherever it alters what §14 fixes for
> a tile the new state still stores, and permitted where it drops tiles out of
> the addressed set, whose extents then become slack.

**Quotation (§20.3, the rule it claims to restate).**

> An extent MAY also **shrink**, and the bar above is the whole of the test,
> **in the bar's own tense**: a shrink is permitted exactly where it alters
> nothing §14 fixes for any tile the layer stores in the generation this commit
> supersedes. … Unstoring that tile in the same commit does not rescue it
> either, and for the same reason: the quantifier is the superseded
> generation's, so a shrink that turns real positions into padding of a tile
> stored there is barred whether or not the new state still stores it.

**Detail.** The two sentences quantify over disjoint domains. §20.3's bar ranges
over tiles stored *in the generation the commit supersedes* and says in terms
that the new state's storedness is irrelevant. §11.1's Rationale ranges over
tiles *the new state still stores*, which is precisely the set §20.3 says does
not decide the question, and it adds "permitted where it drops tiles out of the
addressed set" as if de-addressing were a licence — where §20.3 says dropping a
tile out of the addressed set "is not itself such an alteration … but neither
does it rescue a commit that damages a prior-generation stored tile."

**Construction.** Layer L: rank 1, T₀ = 4, E₀ = 8, one uint8 channel with fill
0x00, interleaved, codec 1. G = 2, N = 2, entry_count = 2; no padding position
exists (G·T = E). Generation 1 stores both tiles: ordinal 0 = `01 02 03 04`,
ordinal 1 = `05 06 07 08`. Generation 2 shrinks E₀ to 6 **and** writes ordinal
1's entry as the sentinel in the same commit. Under the new geometry
G = ⌈6/4⌉ = 2, so entry_count is unchanged, and ordinal 1's positions x = 6, 7
become padding positions of a tile that generation 1 stored with the bytes
`07 08` — not the fill 0x00 that `[R-SER-05]` fixes there.

- An updater built from §20.3 refuses the commit: the tile is stored in the
  superseded generation, the shrink alters what §14 fixes for it, and unstoring
  it in the same breath does not rescue it. It writes a new file under a fresh
  file_id instead (§20.5, `[R-LIF-01]`).
- An updater built from §11.1's Rationale emits the commit: the new state does
  not store that tile, so on that reading the bar does not reach it.

The two emit different byte sequences for the same caller request, and — this is
what makes the divergence durable — §21.7 records that the live state left behind
is clean, so no register row and no verifier will ever tell the second updater it
was wrong: "a commit that supersedes every tile it would have damaged leaves the
live state clean, so the bar is unwitnessed there."

**Why I nevertheless rate it not byte-level.** §2.1 `[R-CNF-01]` makes any text
"labeled *Note*, *Example*, or *Rationale*" non-normative, and this block is
labeled Rationale; the same sentence also says "§20.3 states normatively, and
governs". Two independent signals point a competent implementer at §20.3, so the
document does adjudicate. I tested that premise rather than assuming it — the
block is a `> **Rationale.**` block, so §2.1 applies squarely. What remains is a
real defect: the one place in Part II where a reader of §11's geometry rules is
told what §20.3 says, states its quantifier backwards.

**What an implementer does wrong without it.** Ships an appender that silently
strands a prior generation's stored tile in a state §14 no longer describes,
producing files whose *prior* generations are unrecoverable-as-written by
§9.6's recovery path even though the live state certifies.

---

### register-02 — CONTRADICTION — §21.7 says T3 reads the index entry; T3 reads the decoded payload

**Location.** §21.7 (`[R-ERR-01]`); §21.4 row T3.

**Quotation (§21.7).**

> a change that reaches the decoded size or the codec instead is witnessed by T3
> or T14, which read the index entry rather than the decoded image

**Quotation (§21.4, T3).**

> The decoded payload's byte length is not exactly the tile's decoded size
> derived from the layer's declarations

**Detail.** T14 does read the index entry — `[R-COD-04]` says the check is
"checkable from the entry and the layer record alone, before any payload fetch."
T3 does not: its governing rule `[R-SER-07]` (§14.3) is "a reader MUST treat a
decoded payload whose byte length is not exactly that decoded size as a validity
error at tile scope", which requires the codec stage to have run. §21.7's
parenthetical is therefore false of one of the two rows it names, and it is
false in the direction that matters to the sentence's argument: the point being
made is that these witnesses fire without inspecting decoded *content*, and the
accurate contrast is "read a length rather than the image's content", not "read
the index entry".

Permitted readings: (a) the parenthetical is a loose gloss meaning "test a length
rather than the image's content", true of both rows; (b) it is a claim about
where the compared quantity is read from, true of T14 and false of T3. I take
(a) as intended and (b) as what is written. Under either, §21.1's precedence rule
("where a row and the rule it cites diverge, the rule governs") does not help,
because the divergence here is between two pieces of §21 itself.

**Why not byte-level.** Both rows are reader-detected at tile use with outcome
reject-tile, so whichever row a verifier attributes the file to, the accept/reject
verdict and the bytes are identical. The cost is to a corpus author, who is told
that a vector for this witness needs no decodable payload.

---

### register-03 — CONTRADICTION — a compactor must both refuse and emit when an index entry is structurally invalid

**Location.** §20.5, `[R-WRT-06]` and `[R-WRT-07]`; §15.3 `[R-IDX-03]`;
§21.4 rows T6–T12.

**Quotation (`[R-WRT-06]`).**

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
> and MUST NOT emit a file carrying a violation it has detected: it can neither
> re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the
> output clean. Dropping is the one disposal that answers, and only where
> §20.4's table licenses it … Where the table does not license a drop the
> compactor MUST refuse.

**Quotation (`[R-WRT-07]`).**

> an entry §15.3 classifies reject-tile on a structural ground is reproduced
> with its offset and length exactly as they stand, there being no live extent
> for a re-pointing to target — `[R-IDX-03]` gives such an entry no stored
> extent and no claimant in the coverage walk — and the violation travels with
> it into the output (`[R-WRT-01]`); `[R-WRT-09]`'s checks reach the index chain
> and each stored tile's entry crc, not an entry's own value domain, so such an
> entry is not one `[R-WRT-06]` obliges a compactor to refuse

**Detail.** `[R-WRT-06]` carries two obligations. The first — refuse when a
`[R-WRT-09]` check fails — is not triggered here, and that is the only one
`[R-WRT-07]`'s reasoning addresses. The second is a flat prohibition on
*emitting* a file carrying a violation the compactor has detected, and its
closing sentence resolves the no-disposal case explicitly against emission:
"Where the table does not license a drop the compactor MUST refuse." §20.4's
table licenses dropping *records*; a tile-index entry is not a record and cannot
be dropped. So `[R-WRT-06]` says refuse, and `[R-WRT-07]` says reproduce and emit.

Detection is not optional for the compactor. `[R-WRT-07]` itself requires
differential handling — a well-formed entry gets a new offset, a structurally
broken one is "reproduced with its offset and length exactly as they stand" — so
the compactor must classify each entry under §15.3 to know which branch to take,
and §15.3's classification *is* the detection of T6–T12. `[R-WRT-01]`'s
latent-violation clause does not cover it either: that clause reads "a violation
latent in a structure they neither modify nor rely on travels with it", and the
compactor both relies on the entry and modifies the region that holds it. (The
parallel move at §20.3 step 2 for an *appender* is clean, because no
`[R-WRT-06]`-style prohibition binds an appender and §20.3 adds only a SHOULD to
report.)

**Construction.** Input file, generation 7, one layer, entry_count = 2. Entry 0
is a valid stored tile. Entry 1 has offset = 0xFFFF_FFFF_FFFF_FFFF and
length = 5 — §15.3's "offset = S ∧ length ≠ S" row, *structural* reject-tile,
register row T7. Every `[R-WRT-09]` check passes: the open succeeds; §19.3's
layer-record validation does not classify entries; crc_of_crc_array and the
single segment CRC verify over the entry bytes as stored; and entry 1 addresses
no stored tile, so "every stored tile's entry crc" is discharged by entry 0
alone.

- **Implementation A** (auditing against `[R-WRT-06]`): it has classified entry 1
  under §15.3, hence detected a violation; §20.4's table licenses no drop for an
  index entry; therefore refuse. **No output file is written.**
- **Implementation B** (following `[R-WRT-07]`'s carve-out): compact, writing a
  new file with a fresh file_id at generation 1, whose regenerated index region
  holds entry 0 at a new offset and entry 1 as
  `FF FF FF FF FF FF FF FF 05 00 00 00 00 00 00 00 <crc>`, with the segment CRC
  recomputed over both.

They disagree about whether that output byte sequence may be emitted by a
conforming compactor. That is the byte-level test met directly.

**The counter-argument, stated honestly.** `[R-WRT-07]`'s sentence does end with
an explicit conclusion about `[R-WRT-06]` — "such an entry is not one
`[R-WRT-06]` obliges a compactor to refuse" — and a reader who takes the later,
more specific text as governing lands on B. I file the finding anyway because
the *ground* that sentence offers ("`[R-WRT-09]`'s checks … not an entry's own
value domain") answers only `[R-WRT-06]`'s first clause, which was never the
obstacle; the obstacle is the second clause plus its "Where the table does not
license a drop the compactor MUST refuse" closer, which the carve-out never
mentions. An implementer who checks the reasoning rather than the conclusion —
which is what a careful implementer does with a conclusion whose stated reason
does not reach — is pushed to A.

**Resolution I would pick.** B, with `[R-WRT-06]` amended to except a violation
in a structure the compactor is obliged to reproduce verbatim and cannot drop —
i.e., make the exception turn on "no disposal exists and `[R-WRT-05]` bars
correction", not on `[R-WRT-09]`'s reach. Under A, §20.5's entire prescription
for reproducing structurally broken entries is dead text, which is strong
evidence B is what was meant.

---

### register-04 — OBSERVATION — §21.1's governing rules for the register carry no requirement identifier

**Location.** §21.1 (whole subsection); §2.2; §24 `[R-VEC-02]`; §10.4
`[R-EXT-05]`.

**Quotation (§21.1).**

> Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document
> … but each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**.

**Detail.** §21.1 states the register's own governing rules: that its
completeness is normative; that the rule governs over a divergent row; that
conditions attach to the finest structure they damage; that a specialization is
recorded against the narrower row; and the whole Instances arithmetic. §2.1
makes all of this normative text (it is not labelled Note, Example or
Rationale). But §21.1 assigns no `[R-<PREFIX>-<NN>]` of its own — the ERR
identifiers begin at `[R-ERR-01]` in §21.7 — so the most load-bearing rule in
Part III's error material cannot be cited by identifier.

This has a concrete consequence in the document's own machinery. §24
`[R-VEC-02]` requires each vector to record "the §21 register row it exercises
together with that row's governing requirement identifier — row labels are
positional and renumber when a row is struck, while §2.2 makes the identifier
permanent, so the pair is what survives a renumbering." A vector built to
exercise the *precedence* rule itself — a file whose row and governing rule
diverge — has no permanent identifier to name, only the section number.
§10.4 `[R-EXT-05]` already cross-refers to it by section alone ("§21.1 applies
the same principle to the error register").

Permitted readings: (a) §2.2's "Normative requirements carry identifiers"
describes MUST/SHOULD-form requirements only, and §21.1's declarative statements
are not requirements in that sense; (b) §21.1's statements are normative
requirements and should carry an identifier. I pick (b): §21.1 says of itself
that its completeness "is normative", which is a claim to requirement status.
Cheap to resolve — assign `[R-ERR-06]` (or renumber within ERR) to §21.1 — and
disproportionately expensive to leave, because every future triage of a
row-versus-rule divergence has to cite a section rather than a stable ID.

Not byte-level: the precedence rule's *content* is unambiguous, so no
implementation reads a byte or a verdict differently.

---

### register-05 — OBSERVATION — §20.4 lists "removing a layer" as a way a commit changes the file's layer set, three sentences before saying no commit can

**Location.** §20.4, `[R-WRT-08]`'s table (MU = 0 / PE = 0 row) and the
paragraph immediately following it.

**Quotation (the table row).**

> for a top-level record, the file's layer set — which a commit changes by
> adding or removing a layer and equally by modifying any layer's record — or
> another *non-layer* top-level record.

**Quotation (the next paragraph).**

> No commit therefore removes a layer record, or a user-metadata record at
> either scope.

**Detail.** Removing a layer means removing its layer record; type 0x0001
carries PE = 1 in §7.3's registry, and §20.4 says in terms that no commit
performs the operation. So the enumeration that licenses an appender to drop an
MU = 0 / PE = 0 top-level record includes a trigger no commit can exhibit. The
licence is not widened by it — "adding a layer" and "modifying any layer's
record" remain reachable — but an implementer reading the table row alone may
build a drop path gated on an event that never fires, or, worse, conclude that
layer removal is an appender operation after all and go looking for how to
express it.

Not byte-level: the reachable triggers are unaffected, so the set of commits an
appender may emit is the same under either reading of the dead clause.

---

### register-06 — AMBIGUITY — `[R-ERR-04]`'s unconditional non-conformance sentence reads over the two refusal grounds §2.3 preserves

**Location.** §21.9 `[R-ERR-04]`; §2.3 `[R-CNF-03]`; §7.2 `[R-CNT-15]`;
§21.6's closing paragraphs.

**Quotation (§21.9).**

> Software that declines a file whose every quantity lies within the table is
> not a conforming reader (`[R-CNF-03]`) — the guarantees are the floor, not a
> suggestion.

**Detail.** §2.3 states the acceptance duty with three conditions: a conforming
reader "MUST accept every conforming file *of a format major version it
implements*, *carrying no record of a type it does not implement with
MUST_UNDERSTAND = 1* … and none of whose values exceeds the minimum guarantees".
§21.6's closing paragraphs then describe two **conforming files a reader
nevertheless refuses**, and for the second `[R-CNT-15]` *obliges* the refusal.

§21.9's sentence is unqualified: it says any software that declines a
within-guarantees file is not a conforming reader. Read literally it condemns
exactly the reader `[R-CNT-15]` compels — a reader meeting a conforming file
whose every quantity lies within the table but which carries an experimental-range
record type with MU = 1 must reject it, and is then "not a conforming reader".

Permitted readings: (a) "declines" means declines *on resource grounds*, the
subject of the surrounding paragraph, whose next sentence begins "Either way, a
refusal on resource grounds MUST be reported as a resource limit"; (b) the
sentence is a general statement about acceptance. I pick (a) — it is the only
reading that is not self-contradictory, the sentence cites `[R-CNF-03]` (which
carries the qualifiers), and §2.3 scopes it explicitly: "§21.9's `[R-ERR-04]`
governs a refusal on that last ground; §21.6's closing paragraph names the other
two." The document therefore does adjudicate, and I file this at OBSERVATION
strength rather than as a fork: an implementer who follows the citation gets the
right answer. What an implementer does wrong without it is narrower than a byte
divergence — it is a conformance self-assessment that reports itself
nonconforming for behavior `[R-CNT-15]` required.

Not byte-level: under either reading the reader rejects the same file; only the
label attached to the reader changes.

---

## 7. What I checked and cleared, for the record

So that a later round can see where the effort went rather than re-spending it:

- All four register totals and the 273-instance grand total, recomputed from the
  table text (§1).
- All 121 rows against their governing requirements (§2), including the full
  §15.3 mapping, the full `[R-CNT-23]` field sweep, and the codec/metadata
  frame-constraint enumerations.
- Detector and detection-point vocabulary over all 121 rows, mechanically (§1.2).
- Outcome vocabulary: all four defined values reachable, none out of vocabulary,
  preserve-verbatim correctly excluded (§1.3).
- Completeness rules→rows and rows→rules, with an account for every requirement
  ID that has no row (§3).
- Every register-row citation in the document — sixteen sites — resolved (§4).
- Every CRC constant reproduced from an independent implementation (§5.1).
- The §7.4 layer-record byte example re-derived offset by offset (§5.2).
- §21.9's limits against every defining section and every other citation, in
  both directions, including the Note's four arithmetic claims (§5.6).
- Three false leads killed by working the arithmetic rather than the prose:
  T26's omission of T5 (correct — the byte-shuffle fixes the final byte under
  every stride); L46 as a specialization of L49 (correct as written — L46 ranges
  over unregistered types too); §21.4's heading versus `[R-SER-08]` (already
  adjudicated by §21.1).
