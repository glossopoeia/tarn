# Round 21 — Register hunter — working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,377 lines), in five `Read` calls covering lines 1–400, 400–850, 850–1299,
1299–1749, 1749–2199, 2199–2649, 2649–3048, 3048–3448, 3447–3897, 3893–4377 —
the whole document, cold.

I ran three `grep`/`awk`/`sed` pipelines **against that one file only**
(instance counting over the register tables, a scan for the string
`validity error`, a scan for register-row labels cited outside the tables, a
scan for requirement identifiers inside §20.4 and §21), and one `python3`
heredoc that reads no files at all (a CRC-32C implementation used to check
the document's stated constants).

I opened no other file. No `docs/`, no ADRs, no `PLAN.md`, no
`OPEN-QUESTIONS.md`, no `AGENTS.md`/`CLAUDE.md` beyond what the runtime
injected, no `conformance/`, no `spec/registry.json`, no git history, no web.
I did not list the output directory.

**Context I did not ask for.** Before I began, my runtime placed in context: a
project-instruction pointer (`CLAUDE.md` → `AGENTS.md`), a memory index naming
six memory files with one-line descriptions (one of which names §21 and the
"corpus build list"), a task list of five completed items whose titles name
prior rounds and ADR numbers, and a git status showing the last five commit
subject lines — which name round numbers, ADR numbers, and per-round
byte-level counts. None of it is the specification and I treated none of it as
evidence. I did not open any file it named. I note specifically that the
commit subjects and the memory index gesture at where prior rounds landed; I
deliberately did not let that steer the walk, and every finding below is
anchored to a quotation I read in `spec/tarn.md`.

## 1. What I was asked to audit

§21, the error-handling register, against the rules it restates and against
itself. §21.1 first, then the rest of §21 held to §21.1.

I read the two changed surfaces first as instructed (§18.2's `[R-MTA-09]`
verifier passage, §21.5's preamble clause about a declined decode), then did
the full charter sweep: row-vs-rule, completeness both ways, every
cross-reference to a row, the counting, the outcome vocabulary, and the
limits.

## 2. The counting — done by hand, then mechanically

§21.1 fixes the arithmetic:

> Instances within a cell are separated by semicolons, and a cell reading — is
> one instance; the count is therefore mechanical once the cell is written.

I extracted every table row matching `^\| [FLTR][0-9]+ \|` from lines
3376–3540 and split field 4 (the Instances cell) on `;`.

Row counts:

| Subsection | Rows found | Document states |
|---|---|---|
| §21.2 file-scope | 36 (F1…F36) | "36 conditions" ✔ |
| §21.3 layer-scope | 49 (L1…L49) | "49 conditions" ✔ |
| §21.4 tile-scope | 26 (T1…T26) | "26 conditions" ✔ |
| §21.5 ignored records | 10 (R1…R10) | "10 conditions" ✔ |
| total | **121** | §21.8: "121 conditions" ✔ |

Instance counts:

| Subsection | Instances |
|---|---|
| F | 58 |
| L | 116 |
| T | 55 |
| R | 44 |
| **total** | **273** |

§21.8 states "121 conditions over 273 instances". **Both totals reproduce
exactly.** I checked by hand that no semicolon inside a parenthetical is being
miscounted as a separator: the only Instances cells carrying parentheses are
L2 (`C·N (which dominates the max disk ordinal (C−1)·N + (N−1))`,
`P·Q (which dominates V = P·C)`) and neither parenthetical contains a
semicolon; T26 uses colons, not semicolons, inside its three items.

Spot-checks of the §21.1 axes:

- Layout axis: T3 (6 = 3 layout shapes × 2 magnitude directions), T14 (6),
  T22 (6), T21 (3 — "larger than" bounds the comparison in one direction),
  L44 (3), T4 (4 — interleaved numeric, interleaved bool, planar numeric,
  packed planar bool). All consistent with "Where the quantity a condition
  derives varies by layout, the layout formulas are materially different
  shapes and the cell enumerates them."
- Magnitude axis: F17 (2), F23 (2), L21 (4), L22 (4), L30 (2), T3/T14/T22
  (×2 each). Consistent with "Where the condition compares two **magnitudes**
  either of which can be the greater … the two directions are likewise
  enumerated".
- Single-predicate rule: F25 (MU=1 with PE=0, cell `—`, 1), L20 (A≠0 and S≠0,
  cell `—`, 1). §21.1 explicitly disposes of both: "the fields it reads are
  not instances" and "Nor does a field tested only for being nonzero — an
  *A ≠ 0*, an *S ≠ 0*".
- Family-vs-shape rule: T24 `any codec` = 1 ✔ (§21.1 names it), T15 = 2 ✔,
  T25 = 3 ✔ (§21.1 names both).

**Verdict on the counting: clean. Nothing to report.**

## 3. Outcome vocabulary and the Detector/Detected columns

§2.4 defines five values: reject-file, reject-layer, reject-tile,
ignore-record (reader outcomes), and preserve-verbatim (an updater
obligation).

- reject-file → §21.2's stated outcome. reject-layer → §21.3. reject-tile →
  §21.4. ignore-record → §21.5, and §21.6's non-violation entries. All four
  reader outcomes reachable.
- preserve-verbatim occurs exactly twice in the document, both in §2.4
  (definition and table row). §2.4 points at where it is reachable:
  "§20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows." It is
  correctly absent from the register, being orthogonal to reader outcomes.
  Not a defect — but see finding register-02, which is about how §21.6 cites
  the rule behind those rows.

Mechanical tabulation of (Detector, Detected) over all 121 rows:

```
35 reader   layer access
32 reader   open
24 reader   tile use
20 verifier certification
 9 reader   extent use
 1 reader   open (top-level); layer access (sub-record)   [R1]
```

Every Detector cell is `reader` or `verifier`; every verifier row is at
`certification` and no reader row is; every reader tier is one of §19.2's
four. §21.1 says exactly this: "Detection points name §19.2's reader tiers —
open, layer access, tile use, extent use — or *certification* for the rows a
verifier detects". Clean.

I then checked, for every one of the 20 verifier rows, that the governing rule
actually assigns detection to the verifier, and for the reader rows that the
rule does not exempt readers:

- `[R-CNT-05]` "A verifier MUST treat a structure in that gap" → F7 ✔
- `[R-CNT-12]` "their detection is a verifier's" → F25, F26, L46, L47 ✔
- `[R-CNT-13]` "(readers are not obligated to detect overlap …)" → F33, L18 ✔
- `[R-CNT-15]` "a verifier MUST treat a reserved-range record type" → F36, L25 ✔
- `[R-CNT-22]` "a verifier MUST treat the mismatch" → F28, L49 ✔
- `[R-MTA-05]` "a verifier MUST report it" → F27, L48 ✔
- `[R-SLB-01]` "A verifier MUST check the invariant … readers are not obligated to" → L40 ✔
- `[R-SLB-03]` same → L41, L42 ✔
- `[R-SER-05]` "is not obligated to check it; a verifier MUST check it" → T4, T5 ✔
- `[R-SER-08]` "its assigned detector is the verifier" → T2 ✔
- `[R-COD-10]` "a verifier detects it as a validity error at tile scope" → T26 ✔

No row's Detector cell contradicts its governing rule. I looked hard for one,
because a divergence there would be the sharpest thing in this charter: §21.1
says "where a row and the rule it cites diverge, **the rule governs**", while
§2.3's `[R-CNF-04]` says "A reader MUST detect every violation the error
register (§21) assigns to the reader as its detector" and §19's preamble says
"§21's register is [the complete inventory], and `[R-CNF-04]` binds a reader
to every register row whose detector is the reader, at the tier that row's
*Detected* cell names". Those two sources would answer differently if a row's
Detector cell ever disagreed with its rule. **No row does**, so the tension is
latent, not instantiated, and I am not reporting it — reporting a hypothetical
fork is exactly the over-claim this project has been warned about.

Four reader-detector rows sit on rules with no reader MUST of their own —
T13 (`[R-COD-02]`), T15/T16 (`[R-COD-05]`), T23 (`[R-COD-07]`'s first
sentence). Each row disposes of this itself: "the check that detects it is
T24's or T25's, and this row records the cause rather than a procedure of its
own", and T24/T25 rest on `[R-COD-08]`, which does carry a reader MUST ("a
reader MUST treat a malformed stream and either inexactness as a validity
error at tile scope"). Not a defect.

## 4. Row-versus-rule, row by row

I walked all 121 rows against their cited requirements. Rather than reproduce
121 paragraphs, here is the shape of the check and everything that did not
come out clean.

**§21.2.** F1–F36 against `[R-ENC-02]`, `[R-ENC-03]`, `[R-ENC-04]`,
`[R-ENC-15]`, `[R-CNT-04]`–`[R-CNT-15]`, `[R-CNT-22]`, `[R-CNT-25]`,
`[R-CNT-27]`, `[R-MTA-03]`, `[R-MTA-05]`. §6.2's field-gate list —

> committed_file_length equals the file size … and is a multiple of 64;
> dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64;
> 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved bytes zero

— maps one-to-one onto F17, F13, F9, F16, F10, F11 (+F2 for the upper half),
F12, F15, with F8 (magic), F14 (CRC) and F18 (version_major 0) ahead of them
and F19 (incompat lane) at the flag gate. Nothing in §6.2 lacks a row.

I checked that `file_id` correctly has *no* upper-bound row: §6.2's table
gives it "≠ 0" alone, and `[R-ENC-03]` reaches "every offset, length, extent,
and count", of which a file identifier is none. F12 registering only
`file_id = 0` is right.

I checked the §21.2 preamble's arithmetic:

> Four rows are outside that reasoning and do reach it, because their subject
> is a field fixed across every major (`[R-CNT-24]`): F8 and F1's
> trailer-magic instance, F14's trailer CRC — the two checks §6.2 places
> before the gate — and F6 with F1's front-block instance, which
> `[R-CNT-04]` places before other processing.

Four rows: F1, F6, F8, F14. `[R-CNT-24]` fixes the trailer magic at F−64,
version_major/minor at F−56, the CRC at F−4 over [F−64, F−4), and the front
block. §6.2's order is "the trailer magic; the trailer CRC; the version gate".
Both halves check out. F18's carve-out ("version_major = 0 declares no major
at all") is right too.

**§21.3.** L1–L49. The two big instance cells reproduce:

- L1's eight fields are exactly the layer-record quantities `[R-ENC-03]`
  reaches with no narrower row — layer/sub-record extent_offset and
  extent_length, Eᵢ, Tᵢ, entry_count, S. `A` and `A_slab` are absent, and
  correctly so: L39's "A above 2^62" and L29's "A_slab above 2^62" already
  register the out-of-range case, and §21.1's specialization principle
  records a file against the narrower row. (This is where finding
  register-06 lives — not in L1, but in §21.9's account of *why* 2⁶² is the
  ceiling.)
- L2's nine derived quantities: I checked that nothing §14 or §11 derives is
  missing. Q = Σ Bᵢ ≤ 65,535 × 8 cannot overflow; Fᶜ ≤ Q; the in-sample
  offset (k div C)·Q + F_{k mod C} is dominated by P·Q; ⌈P/8⌉ ≤ P; the
  spatial ordinal is bounded by N and the in-tile ordinal by P; V = P·C is
  dominated by P·Q since Q ≥ C (each Bᵢ ≥ 1) — which the cell says. The max
  disk ordinal (C−1)·N + (N−1) = C·N − 1 — which the cell also says. Complete.

L3/L5/L6 are detected at `open` while L4/L7/L8 are at `layer access`. That is
not an error: §19.1 step 4 places the layer-record *name* parse at the open
("build the layer table: each layer record's name, parsed and checked per
§4.6"), while §19.3 places dimension- and channel-name rules at layer access.
Their outcome is layer scope, which §7.4 fixes ("The owning scope of a layer
record's inline payload is the layer") and which §19.1 confirms is a state a
reader can reach at open ("is instead a validity error at layer scope").

**§21.4.** I checked §15.3's classification table against §21.4 in both
directions. §15.3 has eleven rows; the mapping is:

| §15.3 row | Register |
|---|---|
| valid sentinel | §21.6 (not a violation) |
| both S, crc ≠ 0 | T6 |
| exactly one S | T7 (2 instances) |
| length = 0 non-sentinel | T10 |
| offset < 16 non-sentinel | T8 |
| offset or length > 2⁶³−1 | T11 (2) |
| sum overflows, or > F−64 | T12, T9 |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 (verifier) |
| overlap outside the layer | F33 (verifier) |
| alignment/slab invariant | L40, L41, L42 (verifier) |

§15.3 says "Six rows are marked *structural*"; I counted six. Complete in both
directions, with no §15.3 row unregistered and no T row without a §15.3 or
§17 source.

T11's exclusion "the value being distinct from the all-ones sentinel" is what
keeps T7 and T11 from double-claiming a half-sentinel entry. I checked this
because it is the sort of place a partition leaks; it does not.

T2 and T4 partition `[R-SER-08]` by position — "the same byte at a padding
position is T4's, the two rows together covering `[R-SER-08]`". I verified the
partition holds: a padding position's interleaved bool byte is constrained to
the fill byte by `[R-SER-05]`, and the fill byte is itself constrained to
0x00/0x01 by `[R-TYP-07]`, so a bad byte at a padding position is T4 and a bad
byte at a real position is T2, with no third case.

**§21.5.** R1–R10 against §18.2. I checked R4's constraint list exhaustively,
because it is the row nearest the changed text. `[R-MTA-09]` states:

> under the frame constraints of `[R-COD-06]` that do not reference a tile:
> the frame magic; no skippable frame and no second frame; no nonzero
> dictionary ID; no content-checksum flag

— five, plus "exactly one RFC 8878 compressed frame **occupying the extent's
bytes before its terminal CRC**", which R4 renders as "bytes remaining after
the frame". Six constraints × two containers = 12 instances. R4 has 12.
Crucially, R4 correctly *omits* the two `[R-COD-06]` constraints that do
reference a tile — the window-size bound and Frame_Content_Size — because
`[R-MTA-09]` withdraws both ("The constraints §17.2 states against a tile's
declared decoded size do not apply, because a document has no declared size";
"The frame's declared `Window_Size` is unconstrained here for the same
reason"). This is exact.

`[R-MTA-04]`'s four bullets map onto R7 (object/BOM), R8 (finite numbers), R9
(duplicate keys), R5+R6+R10 (UTF-8 and the key name rules). I checked that a
*string value* carrying U+0000–U+001F is correctly not registered: §4.6's name
rules are folded onto keys only. Complete — with one seam, reported below as
register-05.

## 5. Completeness the other way — a sweep for unregistered conditions

I grepped every occurrence of `validity error` (33 hits) and walked each to its
row. Everything landed. The interesting cases are the ones the document
*deliberately* leaves unregistered, and each is declared where it arises:

- `[R-SLB-04]`'s stale slab declaration — §16.2's Note: "a stale declaration
  carries no register row of its own: every file exhibiting one exhibits a
  run whose tiles are unpacked or whose first stored tile is misaligned,
  which §21.3 registers." Correct: L41 and L42.
- `[R-CNT-18]`'s nesting prohibition — §7.4's Note: "in format major 1 it has
  no reader-detectable witness, and so no register row", and §21.7 repeats it.
  Correct: a sub-record payload is never parsed as a record sequence except
  for the layer record, which L26 registers in its own right.
- `[R-CNT-02]`'s "belongs to no class" half — §5.2's Note: "a register row for
  it would be a row no file could exhibit". Correct, since `[R-LIF-08]` makes
  every unreached byte slack by definition.
- `[R-LIF-04]`'s residue — §9.5's Note: "Residue past a completed commit
  carries no register row of its own … the state a reader can observe is
  already named", i.e. F8/F14/F17.
- The undisclosed zstd dictionary — `[R-COD-06]` and §21.7. Correctly excluded
  from T13, whose two instances are deflate and lz4 only, both of which *are*
  detectable as malformed streams.

I also checked that no row registers a non-violation. The four that need an
argument all have one:

- F36/L25/R1 (reserved-range values). §10.3: "a value from a reserved range
  MUST NOT be emitted at all before this specification assigns it" — an
  output rule, distinguished from the experimental prohibition's "in released
  software or published data", which `[R-CNF-02]` classifies as conduct. §21.6
  and §21.5's preamble both state the distinction explicitly.
- F27/L48 (unsorted members). `[R-MTA-05]`: "the file is nonconforming".
- F28/L49 (stored flag mismatch). `[R-CNT-22]`: "A stored-flag mismatch on a
  registered type makes the file nonconforming".
- F19 (incompat-lane bit). §6.3 carves out only the *ignore* lane — "a set
  ignore-lane bit is not a file-conformance violation" — and §4.3/§10.1's
  growth vehicles admit "new ignore-lane flag bits" and nothing in the
  incompat lane, so under major 1 a set incompat bit is a violation of
  "a writer creating a file under this text MUST write flags = 0". Correct.

## 6. Every cross-reference to a register row

I grepped all row labels outside the tables and resolved each.

| Citing site | Cites | Resolves? |
|---|---|---|
| §5.2 `[R-CNT-21]` l.646 | L18, L40–L42 | ✔ intra-layer overlap; alignment; slab packing; slab first-tile alignment — exactly the layer-scope rejections a coverage walk establishes |
| §9.6 `[R-LIF-06]` l.1299 | F8, F17 | ✔ trailer magic; committed_file_length vs transport size |
| §17.2 Note l.2267 | T24 | ✔ trailing byte after a DEFLATE stream |
| §18.2 `[R-MTA-09]` l.2471 | R3 | ✔ "fail to decode under its declared assigned encoding" |
| §20.3 step 4 l.2992 | L44 | ✔ lz4 decoded-size cap |
| §20.5 `[R-WRT-06]` l.3190 | F36, L25, R1 | resolve individually, but the enumeration is short — **register-03** |
| §21.1 l.3306 | F1 of F6 and F8; F35 of F36; L24 of L25 | ✔ all three specialization claims verified against the row texts |
| §21.1 l.3325 | T24; T15, T25 | ✔ 1 instance; 2 and 3 instances |
| §21.1 l.3355 | F27, L48 | ✔ as [R-MTA-05]'s rows, but the attachment is ambiguous — **register-04** |
| §21.2 preamble | F8, F1, F14, F6, F18 | ✔ |
| F33's cell | F9/F10, F31/F32, L16/L17, T8/T9 | ✔ all eight are the front-block and trailer bounds rows at their own tiers |
| §21.6 table | F36, L25 | ✔ |
| §21.6 closing | F18; F35, F36, L24, L25 | ✔ |
| §21.7 | T2, T4, T5; T3, T14; T15, T17, T23, T25 | ✔ (T15's fit is loose — a zstd frame re-declared as codec 2 is not a zlib/gzip wrapper, so T25 rather than T15 fires — but the sentence names the set collectively) |
| §24 `[R-VEC-03]`/notes | §21 rows generally | ✔ |
| Appendix H | F1, F6; F7; F36, L25; R1 | ✔ |

## 7. Limits — §21.9 against every other statement of a limit

Minimum-guarantee table vs Appendix B's "Reader minimum guarantees" row:
rank 32, C 4096, entry_count 2³², 65,536 layers, 16 MiB directory region,
256 MiB decoded tile, 16 MiB metadata document, 8 MiB zstd window — identical
in both places. ✔

I re-derived §21.9's own Note: ⌈2³²/2¹⁶⌉ × 4 = 65,536 × 4 = 262,144 = 256 KiB
✔; at 2³⁶, 2²⁰ × 4 = 4 MiB ✔; 65,536 layers × ~200 B = 13,107,200 B = 12.5 MiB
✔; §15.4's "one full segment (1.25 MiB)" = 2¹⁶ × 20 = 1,310,720 ✔.

Hard limits vs their defining sections:

| §21.9 claim | Defining section | Agrees? |
|---|---|---|
| name ≤ 255 B | §4.6 `[R-ENC-12]` | ✔ |
| user-metadata key ≤ 255 B | §18.2 `[R-MTA-04]` | ✔ |
| rank ≤ 255, C ≤ 65,535 | §7.4 u8/u16 | ✔ |
| codec 4 decoded size ≤ 0x7E000000 | `[R-COD-07]` | ✔ |
| offsets/lengths/extents/counts ≤ 2⁶³−1 | `[R-ENC-03]` | ✔ |
| A power of two, 512 ≤ A ≤ 2⁶² | §16.1 | ✔ |
| A_slab power of two, 1 ≤ A_slab ≤ 2⁶² | §16.2 / §7.4 | §16.2's own text says only "a power of two ≥ 1"; the 2⁶² ceiling is §7.4's table. §21.9 cites §16.2 for it. Minor; folded into register-06's discussion. |
| 1 ≤ S ≤ 2⁶³−1 | §16.2 / §7.4 | ✔ |
| dir_offset ≥ 16, dir_length ≥ 4 | §6.2 | ✔ |
| no file < 128 B | §5.1 `[R-CNT-27]` | ✔ |

A limit stated elsewhere but absent from §21.9 is not a defect: §21.9 says
"The hard limits it restates are a finding aid rather than an inventory."
(`inline_length` ≤ 2³²−1 from its u32 width is the obvious omission; licensed.)

`[R-ERR-04]`'s decline scopes — "at the whole file, or at the narrowest scope
whose declarations exceed what it can serve, a layer or a tile" — compose with
§18.2's note that a user-metadata document, having no declared size, admits no
narrower scope than the file. ✔ And with `[R-COD-06]`'s "permits a conforming
reader to decline the tile or the layer on resource grounds". ✔ And with
`[R-CNF-03]`'s and §21.6's "the two capability refusals §21.6 names, a foreign
format major and an unimplemented MU = 1 type, are not this ground". ✔

## 8. The two changed surfaces

**§18.2's `[R-MTA-09]` verifier passage.** I read it against §2.3's
cannot-establish list, §9.7, `[R-MTA-10]`, `[R-CNF-11]`, `[R-ERR-04]` and
§21.5's preamble. It composes:

- §2.3 already names "when it declines to decode a user-metadata document
  (`[R-MTA-09]`)" among the cannot-establish grounds. ✔
- The decline does not stop the coverage walk: the extent is still a claimant
  and its terminal CRC is still verified, so §9.7's slack total stays exact
  and does not become partial under `[R-CNT-21]`. Nothing in §9.7 needs a
  carve-out here, and none is missing. ✔
- "an established violation takes priority" is honoured: "it fixes the file's
  verdict as *cannot establish* only where the verifier established no
  violation elsewhere". ✔
- The `[R-MTA-10]` boundary is held on both sides: an *unassigned* encoding is
  not a decline ground ("The decline presupposes an encoding this
  specification assigns"), and §2.3 says the same ("A user-metadata document
  under an encoding this specification does not assign is not such a ground").
  ✔

The one softness I found: the verifier sentence says "declines to decode a
document **on the bound above**" — singular — where the two preceding
sentences give two bounds (decode size, and the frame's declared
`Window_Size`). §21.5's clause names both ("on the size bound or on the
frame's declared window"), and §2.3 names neither, saying only "declines to
decode a user-metadata document". I worked the case where they might diverge —
a verifier whose window bound is the 8 MiB guarantee meeting a metadata frame
declaring 16 MiB — and both readings converge on the same verdict: either the
verifier declines (cannot establish) or it ignore-records without checking
`[R-MTA-04]`'s content rules, which is a requirement it was unable to check,
which `[R-CNF-11]` also routes to cannot-establish. **No fork. Not reported.**

**§21.5's clause.** "as a violation in the rows below, except at an
experimental-range encoding, where no document rule attaches and §21.6 records
the defined non-violation (`[R-MTA-10]`), and except where a reader or
verifier declines the decode on the size bound or on the frame's declared
window, which `[R-MTA-09]` makes that actor's capability and not a fact about
the file. Encoding 0 and a reserved-range value are unassigned too, and R1
registers both as violations: what `[R-MTA-10]` withdraws is the document's
content rules, never the encoding byte's own value set (`[R-MTA-03]`)."

I checked all three carve-outs land somewhere: the experimental encoding is
§21.6's table row ("A user-metadata record declares an experimental-range
(≥ 0x80) document encoding | Ignored (ignore-record); the file is conforming");
the decline is nowhere in §21.6 but needs no home, since §21.1 exempts §21.6
from the completeness clause ("neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations"); and R1
carries encoding 0 and the reserved range with four instances. ✔

I also confirmed R4 does not silently pick up a window constraint from
`[R-COD-06]` (it does not — see §4 above), which is the seam these two edits
sit on. **I found no defect in either changed surface.**

## 9. Building it end to end

I implemented the document's checksum from §4.5 alone and reproduced every
constant the document states, as a test of whether §21's rows are actually
constructible from the text:

```
CRC-32C("123456789")                = 0xE3069283   (§4.5 check vector)      ✔
CRC-32C(zero bytes)                 = 0x00000000   (§4.5)                   ✔
CRC-32C(4 sentinel entries, 80 B)   = 0x80A34955   (§7.4 example)           ✔
CRC-32C(that 4-byte array)          = 0xC4EE982E   (§7.4 crc_of_crc_array)  ✔
CRC-32C(2¹⁶ sentinel entries)       = 0xEECB3BB2   (§15.4, Appendix B)      ✔
CRC-32C(Appendix A trailer [0,60))  = 0xE00938D2   (Appendix A)             ✔
```

The trailer bytes I fed the last one were built field-by-field from §6.2's
layout table, not copied from Appendix A's hex dump, so this is an
independent check of the layout table: magic (8) ‖ version_major=1 (2) ‖
version_minor=0 (2) ‖ flags=0 (4) ‖ generation=1 (8) ‖ dir_offset=16 (8) ‖
dir_length=4 (8) ‖ committed_file_length=128 (8) ‖ file_id=0x0123456789ABCDEF
(8) ‖ reserved (4) = 60 bytes. It reproduces.

I then hand-checked every worked numeric example the register depends on:
§7.4's 81-byte inline payload (4 + 34 + 18 + 12 + 13 = 81, matching the hex
offsets and the extent length 4×20 + ⌈4/2¹⁶⌉×4 = 84); §11.2's G/N/P; §11.4's
ordinals (1·8+2 = 10, 44·256+188 = 11,452, 2·32+10 = 74); §14.2's strides
(Q = 3, 18 bytes, ordinal 5 at [15,18); Q = 5, 30 bytes, [25,30)); §14.3's
packed plane (0x55, 0x01, and 0xFD with fill true); §14.5's edge tile (16
positions, 1 real, 15 padding, 32 bytes); §15.4's 1,000,000-entry example
(16 segments, 64-byte array, region 20,000,064, segment 15 at
[19,660,800, 20,000,000), tile 999,999 at segment byte 339,180); §16.2's four
runs; §17.3's byte-shuffle (`00 00 00 00 00 00 80 00 40 3F 40 40`); §20.3's
644-byte index region; §4.6's `température` at 12 bytes NFC / 13 NFD.

**All of them reproduce.** I did not have to guess at any of them. That is a
strong signal for the register: every row whose instances name a derived
quantity (L2, L44, T3, T14, T21, T22, T26) is anchored to arithmetic I could
carry out from the text alone.

Where I *did* have to guess is recorded as the findings below.

## 10. Findings

### register-01 — CONTRADICTION — §21.1 (and §21.2–§21.6) state original normative rules with no requirement identifier, which §2.2 says every normative requirement carries

§2.2 states, without qualification:

> Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`.
> Identifiers are stable: they are never renumbered or reused …

and the how-to-read box at the head of the document:

> Normative requirements carry stable identifiers like `[R-IDX-03]`, and test
> vectors cite those identifiers rather than prose positions.

§21.1 states rules that are not restatements of anything else in the document
and that carry no identifier:

> Its **completeness is normative** — a *detectable* file-conformance
> violation this specification names and the register omits is a defect in
> this document …

> … but each row *restates* its governing rule, and where a row and the rule
> it cites diverge, **the rule governs**.

> Some rows are strict specializations of others — F1 of F6 and of F8, F35 of
> F36, L24 of L25 — and a file exhibiting a specialization is recorded
> against the narrower row, whose detector and detection point are the ones
> that apply.

I confirmed mechanically that no requirement identifier terminates anywhere in
§21.1 through §21.6: scanning lines 3281–3660 for a line ending in a
backticked identifier yields only `[R-ERR-01]` (line 3646, §21.7) and
`[R-ERR-02]` (line 3653, §21.8). `[R-ERR-02]` is cited *inside* §21.1 to fix
the register's extent, but its own text lives in §21.8 and states only the
vector-coverage obligation.

The rules above are load-bearing and unciteable. `[R-VEC-02]` explains
precisely why that matters:

> the §21 register row it exercises together with that row's governing
> requirement identifier — row labels are positional and renumber when a row
> is struck, while §2.2 makes the identifier permanent, so the pair is what
> survives a renumbering.

A vector built to exercise §21.1's specialization-recording rule, or a
conformance report asserting the register's completeness, has only a prose
position to cite — the thing the how-to-read box says the document's citation
discipline avoids. The same gap covers §21.5's preamble (which assigns the
quarantine outcome to every row in the subsection) and §21.6's non-violation
table, whose entries §21.1 explicitly holds to the same standard as rows
("§21.6's entries restate their governing rules on the same terms a row does").

**What I picked / what an implementer does wrong without it.** I treated
§21.1's rules as normative and binding, because §2.1 makes all text normative
except §1, labelled Notes/Examples/Rationale, and non-normative appendices,
and §21.1 is none of those — and because §21.1 asserts its own normativity.
An implementer or reviewer who instead treats identifier-bearing text as the
normative surface (which §2.2 invites) would read §21.1 as editorial
front-matter and lose the completeness guarantee, the rule-governs precedence,
and the instance arithmetic — the three rules this document's own review
process turns on.

**Byte-level: no.** Nothing here changes which byte sequences may be emitted
or must be accepted. It changes which text a reviewer treats as binding and
what a vector manifest can cite. Two competent implementations reading §21.1
reach the same reader and writer behavior either way, because the rules §21.1
states are about the register's relationship to the requirements, not about
bytes.

### register-02 — OBSERVATION — §21.6's experimental-type entry cites `[R-WRT-08]` for a preserve-or-drop rule that `[R-WRT-08]` does not state; the rule lives in §20.4's table, which carries no identifier

§21.6's table row reads:

> | A record type this specification has not assigned, from the experimental
> range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
> per its PE bit; a *reserved*-range type is read the same way, but emitting
> one is a violation (F36, L25) | `[R-CNT-15]`, `[R-WRT-08]` |

`[R-CNT-15]` supplies "Ignored" ("An unknown record type at file scope:
MU = 1 → reject-file; MU = 0 → ignore-record"). `[R-WRT-08]` is cited for
"preserved or dropped per its PE bit". Its full text is:

> An updater MUST NOT re-encode a record whose type it does not implement,
> and MUST NOT modify one except by relocating its extent and re-pointing its
> slot under §20.5 — the operation the no-embedded-offsets rule (§7.2) makes
> safe for MU = 0 records. `[R-WRT-08]`

That says nothing about preserving or dropping per the PE bit. The rule the
entry is restating is §20.4's table —

> | MU = 0, PE = 1 | Retain byte-identical, extent content unmodified. |
> | MU = 0, PE = 0 | Retain byte-identical, or drop it — its extent becoming
> slack. An appender MUST NOT drop it except in a commit that *independently*
> changes the scope the record attaches to …

— and I confirmed that this paragraph and table carry **no** requirement
identifier: `[R-WRT-05]` terminates the paragraph before it (line 3114) and
`[R-WRT-08]` opens a new sentence after it (line 3144). §2.4 refers to the
same table by section, not by identifier: "§20.4's table states the cases: its
MU = 1 and MU = 0 / PE = 1 rows."

§21.1 says: "§21.6's entries restate their governing rules on the same terms a
row does, and where such an entry and the rule it cites diverge, the rule
governs there too." Applied literally, `[R-WRT-08]` governs and is silent on
the drop, leaving the entry's second clause without a governing rule.

**What an implementer does wrong.** An updater author who follows §21.6's
pointer lands on a rule about re-encoding and relocation and does not find the
drop permission or its "independently changes the scope" precondition — the
one clause that keeps a commit from being written solely to delete an
application's record. They would either drop too freely or not at all. The
correct text is reachable (it is §20.4's table, one section earlier and
already cited by `[R-CNF-06]`), so this is a mis-citation rather than a
lacuna.

**Byte-level: no.** §20.4's table is unambiguous where it stands and reaches
the reader through `[R-CNF-06]` ("MUST honor the preservation obligations of
§20.4"). Two updaters reading §20.4 emit the same files; only the pointer from
§21.6 is wrong.

### register-03 — OBSERVATION — §20.5 names three register rows as the reserved-range rows behind a claim that six further rows also carry

`[R-WRT-06]` says:

> Where the output carries a feature a later minor defines and this compactor
> does not — on a conforming input a carried ignore-lane bit (§6.3) or an
> unrecognized `tarn.` key in a record it never decoded (§18.3), the two of
> §10.1's four vehicles §21.6 makes conforming, the other two reaching such a
> file only as values this text still registers as reserved-range violations
> (F36, L25, R1) — the output's version_minor SHOULD be at least the input's

"The other two" of §10.1's four vehicles are (1) new record types and (2) "New
values in the ranges this specification reserves (§10.2)". §10.2's table
partitions eight spaces, and the register carries a reserved-range row for
each of them:

- record type → F36 (top-level), L25 (sub-record) — both cited ✔
- metadata encoding → R1 — cited ✔
- channel layout → **L36** ("layout 0; reserved 3-255")
- linearization → **L33** ("reserved 2-3; reserved 4-0x7FFF")
- sample type → **L34** ("reserved 14-19; reserved 20-0x7FFF")
- codec → **L43** ("reserved 5-0x7FFF")
- filter → **L45** ("reserved 3-0x7FFF")
- index encoding → **L31** ("reserved 2-0x7F")

Six rows are omitted from a parenthetical that reads as the full set. I
verified the underlying claim is *true* for each omitted space — a compactor
meeting a reserved-range codec or sample type fails §19.3's layer validation,
which `[R-WRT-09]` obliges it to run, so §20.5's "A compactor MUST refuse to
compact when any check `[R-WRT-09]` obliges fails" bites, and the value never
reaches the output. So the sentence is right and its citation is short.

I checked the R1 case specially because it is the one that does *not* produce
a scope rejection: R1 is ignore-record, so the compactor does not refuse on a
validation failure — but it has now *detected* a violation, and §20.5's "MUST
NOT emit a file carrying a violation it has detected … Where the table does
not license a drop the compactor MUST refuse" combined with §20.4's "both
registered types carry PE = 1, so neither can be dropped" forces refusal
anyway. The claim holds. That is presumably why R1 was singled out; but naming
R1 and not L31/L33/L34/L36/L43/L45 leaves a reader checking the claim with a
list that does not cover the ground the sentence quantifies over.

**What I picked.** I read the parenthetical as illustrative rather than
exhaustive, because the sentence's claim is verifiable independently for every
space. A reader who reads it as exhaustive concludes that a reserved-range
codec or sample type is *not* a registered violation, which is false.

**Byte-level: no.** The rows it omits exist and say what is needed; a
compactor built from L31/L33/L34/L36/L43/L45 and §19.3 behaves identically
whether or not §20.5 names them.

### register-04 — AMBIGUITY — §21.1's parenthetical leaves it unclear whether "F27 and L48" names the rows of both cited rules or only the second's; `[R-CNT-22]`'s rows are F28 and L49

§21.1 reads:

> For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader: the governing rule
> states what a reader does, and for several such rows it obliges the reader
> to serve the structure unchanged (`[R-CNT-22]`, whose registered type keeps
> its fixed semantics; and `[R-MTA-05]`, whose unsorted document readers
> process as they find it — F27 and L48).

Two readings are defensible.

**Reading A (the one I picked).** The em-dash list attaches to the second
conjunct only, so "F27 and L48" are `[R-MTA-05]`'s rows. This is correct on
the facts: F27 is "A file-scope user-metadata document has object members …
not in ascending order" governed by `[R-MTA-05]`, and L48 is the layer
sub-record twin. `[R-CNT-22]`'s rows — F28 and L49 — then go unnamed.

**Reading B.** The parenthesis closes the whole construction, so "F27 and
L48" enumerate the register rows for both cited rules — two rules, two labels,
one each. That reading maps F27 to `[R-CNT-22]` and L48 to `[R-MTA-05]`, and
is simply wrong: F27's Governing rule cell reads `` `[R-MTA-05]` (R-CNF-05) ``
and `[R-CNT-22]`'s rows are F28 (`` `[R-CNT-22]` (R-CNF-05) ``, "A non-layer
top-level record of a type §7.3 registers carries a stored MU or PE bit
differing from the value the registry fixes") and L49.

**Why I picked A.** The semicolon after the `[R-CNT-22]` gloss closes that
conjunct, and the row texts confirm the mapping. But the count coincidence —
two rules, two labels — makes B available to a reader who does not go look the
rows up, and the whole point of naming rows here is to spare that lookup.

**What an implementer does wrong.** Nothing to their bytes. A triager or
vector author reading B attributes a stored-flag-mismatch vector to F27
instead of F28 and an unsorted-document vector to L48 alone, losing F27. Under
`[R-VEC-02]`, "the §21 register row it exercises together with that row's
governing requirement identifier" is a manifest field, so the mis-attribution
propagates into the corpus.

**Byte-level: no.** Both readings leave the reader obligations identical:
under either, `[R-CNT-22]` obliges the reader to "apply a known type's
specified semantics regardless of its stored MU and PE bits" and `[R-MTA-05]`
obliges it to process an unsorted document unchanged. Only the row labels
move.

### register-05 — OBSERVATION — the bare tokens `NaN` / `Infinity` / `-Infinity` are registered by both R7 and R8, and §21.1's specialization list does not cover the pair

`[R-MTA-04]`'s second bullet:

> **Finite numbers only.** … A document is unreadable if it contains a number
> whose binary64 interpretation is not finite — which covers a magnitude that
> overflows on conversion, `1e400` being the ordinary case — or any of the
> bare tokens `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not admit
> and some parsers accept regardless.

R8 registers this as one row: "A user-metadata document contains a non-finite
number, in any form", 2 instances (top-level; layer sub-record).

R7 registers: "A decoded user-metadata document is not well-formed JSON, or
its top-level value is not an object", 6 instances, the first pair being "not
well-formed JSON".

A document containing the bare token `NaN` satisfies both conditions at once —
the bullet itself says RFC 8259 "does not admit" the token, which is precisely
what makes the document not well-formed JSON. So one file exhibits two rows.

§21.1 handles overlaps of this kind by naming them:

> Some rows are strict specializations of others — F1 of F6 and of F8, F35 of
> F36, L24 of L25 — and a file exhibiting a specialization is recorded against
> the narrower row, whose detector and detection point are the ones that apply.

The R8-bare-token / R7-not-well-formed-JSON pair is not in that list. There is
also an asymmetry inside §21.5 in how the two bullets were turned into cells:
R7 enumerates the three alternatives of its bullet ("A JSON object,
unmarked") as three shapes, giving 3 × 2 = 6 instances, while R8 collapses the
two alternatives of its bullet with "in any form", giving 1 × 2 = 2. §21.1's
own axis rule — "a row whose check ranges over a family without the condition
changing shape states that range as a single instance … and one whose members
give the condition materially different shapes enumerates them" — cuts toward
enumeration here, since detecting `1e400` is a conversion-overflow test and
detecting a bare `NaN` is a tokenizer rejection.

**What I picked.** I treated the count as correct-as-written, because §21.1
makes the count "mechanical once the cell is written" and R8's cell says "in
any form", so 273 stands. The defect I am reporting is the unregistered
overlap, not the total.

**What an implementer does wrong.** Nothing to their reader: both rows are
ignore-record, detector reader, detection at extent use, so the behavior is
identical and the outcome cannot fork. The cost is to the corpus and to
triage — a vector carrying `NaN` has no stated home, and `[R-VEC-02]`'s
fallback ("the entry records every row the file exercises and says which it
was built for") is the only thing that resolves it. R8's two instances remain
independently constructible via `1e400`, and R7's via any other JSON syntax
error, so no coverage is lost.

**Byte-level: no.**

### register-06 — AMBIGUITY — §21.9 asserts the 2⁶² ceilings on A and A_slab follow from the value domain, but §4.2's value domain does not name alignments; the two readings disagree about whether 2⁶² is derived or chosen, and §21.9 counts the chosen numbers

`[R-ERR-05]` closes with a claim about provenance:

> Most follow from a field's width, an external format, or the value domain,
> and the rest from arithmetic over structures a generation cannot omit. Two
> do not: the 512 floor on A is a number chosen here, fixed at the legacy
> sector size (§16.1) so that a declared alignment is worth declaring, and the
> 255-byte cap on a user-metadata key is this specification folding §4.6's
> name rules onto keys, which carry no length prefix to force it.

The limits in question are stated two paragraphs earlier in the same
requirement:

> a declared alignment A a power of two with 512 ≤ A ≤ 2⁶², and a declared
> slab alignment A_slab a power of two with 1 ≤ A_slab ≤ 2⁶² (§16.1, §16.2,
> `[R-SLB-01]`, `[R-CNT-23]`)

And the value domain is `[R-ENC-03]`:

> The valid range of every offset, length, extent, and count this
> specification defines — entry counts and slab run lengths included — is 0 to
> 2⁶³ − 1 inclusive

**Reading A (the one I picked).** An alignment is "a byte length" within the
sense §4.2 opens with ("as is every byte length this specification does not
give another width where it defines the field"), so `[R-ENC-03]` reaches A and
A_slab, and 2⁶² is the largest power of two inside 0 … 2⁶³ − 1 — genuinely
derived, and §21.9's "Two do not" is accurate. Under this reading L1's
instance cell is also right to omit A and A_slab, because L39's "A above 2^62"
and L29's "A_slab above 2^62" are the narrower rows and §21.1 records a file
against the narrower row.

**Reading B.** An alignment is not an offset, a length *of* anything, an
extent, or a count. `[R-ENC-03]`'s enumeration goes out of its way to name the
borderline inclusions — "entry counts and slab run lengths included" — and
does not name alignments. Under this reading the 2⁶² ceilings are chosen
numbers stated in §7.4's table and §16.1, not derived ones, and §21.9's "Two
do not" undercounts: there would be four numbers chosen here rather than two,
and the derivation §21.9 offers for the ceilings is wrong.

**Why I picked A.** Because §21.9's own sentence is the only place the
document accounts for where the 2⁶² ceilings come from, and A is the reading
that makes it true; and because §16.2 states A_slab as "a power of two ≥ 1"
with no ceiling of its own, pushing the ceiling's origin onto §7.4's table,
which cites `[R-CNT-23]` and would then have a bare unexplained constant.

**What an implementer does wrong.** Nothing to their bytes: under either
reading a reader must reject A = 2⁶³ at layer scope, because L39's third
instance is "A above 2^62" and `[R-SLB-01]` says "Writers MUST NOT emit any
other nonzero value; a reader MUST treat one as a validity error at layer
scope". The cost falls on a reviewer auditing §21.9's inventory of chosen
constants, and on anyone building the 273-instance corpus who has to decide
whether an out-of-domain alignment is an L1 instance (Reading B would suggest
adding two, taking the total to 275) or an L39/L29 instance (Reading A, total
stays 273).

**Byte-level: no.** L39 and L29 already fix the accept/reject verdict for
every out-of-range alignment value, in one direction, from declarations alone.
No file's verdict turns on which reading of §4.2 an implementation adopts.

## 11. What I checked and found clean (recorded so the next round need not redo it)

- All four subsection condition counts and both §21.8 totals (121 / 273).
- Every Detector/Detected cell against §19.2's tiers and against the governing
  rule's assignment of detection.
- §15.3's eleven-row classification table against §21.4 and §21.3 in both
  directions, including the "Six rows are marked *structural*" count.
- §6.2's field-gate list against F8–F19.
- `[R-MTA-04]`'s four bullets against R5–R10, and `[R-MTA-09]`'s six imported
  frame constraints against R4's twelve instances.
- All sixteen citation sites that name a register row by label.
- §21.9's minimum-guarantee table against Appendix B, and its ten hard limits
  against their defining sections.
- §21.9's Note arithmetic (256 KiB, 4 MiB, 12.5 MiB) and §15.4's 1.25 MiB.
- Every deliberately unregistered condition (`[R-SLB-04]`, `[R-CNT-18]`'s
  nesting, `[R-CNT-02]`'s untestable half, `[R-LIF-04]`'s residue, the
  undisclosed zstd dictionary) against the Note or §21.7 clause that declares
  it.
- The six CRC constants and every worked numeric example the register's
  derived-quantity rows depend on.
- Both changed surfaces (§18.2's `[R-MTA-09]` verifier passage, §21.5's
  preamble clause), against §2.3, §9.7, §21.6, `[R-MTA-10]`, `[R-CNF-11]`,
  `[R-ERR-04]` and R4's instance list.

**Byte-level findings: zero.** I looked specifically for a fork in the
register — a row whose Detector cell contradicts its rule, a scope assignment
that would make one implementation reject a file another serves, an outcome
value the register uses that §2.4 does not define, a limit §21.9 states
differently from its defining section. I found none of those. The six findings
above are citation, identifier, and enumeration defects; none of them changes
which byte sequences a conforming implementation may emit or must accept or
reject, and I have said so in each.

Transcript finding count: **6**.
