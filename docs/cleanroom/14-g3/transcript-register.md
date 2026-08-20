# Cleanroom round 14 — Register hunter transcript

Charter: audit §21, the error-handling register, against the rules it restates
and against itself.

## 0. Disclosure

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read in four `Read` calls covering lines 1–4168 (the whole document), plus targeted
`grep`/`awk` passes over that same file. I opened no ADR, no `docs/`, no
`conformance/`, no `registry.json`, no `PLAN.md`, `AGENTS.md`, `README.md`,
`OPEN-QUESTIONS.md`. I ran no `git` command. No web search, no web fetch. I did not
list the output directory or read any other agent's transcript.

I wrote and ran four Python scripts of my own in the scratchpad
(`crc.py`, `layer.py`, `build.py`, and two inline heredocs). They read no files
except the one heredoc that re-parses `spec/tarn.md` to recount the register tables.

I did carry prior knowledge of CRC-32C, RFC 1951/8878, LZ4 block format and JSON
into the reading. I used it only to generate suspicions and to check the document's
own arithmetic; every conclusion below is sourced to the document's text.

## 1. Method

1. Read the whole document cold, front to back.
2. Verified every constant §21 and its neighbours depend on, by computation.
3. Built a conforming two-tile file end to end from the text alone, then ran the
   §9.7 coverage walk over it by hand.
4. Recounted §21.2–§21.5 conditions and instances by hand, then again
   mechanically by parsing the tables, and compared against every total stated.
5. Swept the document for every "validity error" / "reject-*" / "ignore-record"
   statement and checked each has a row, and each row has such a statement.
6. Resolved every cross-reference to a register row from anywhere in the document.
7. Checked §21.9's limits against every other statement of a limit, both ways.

## 2. Constants and arithmetic (all reproduce)

```
check vector CRC-32C("123456789")   = 0xE3069283   §4.5  ✓
CRC-32C(zero bytes)                 = 0x00000000   §4.5  ✓
CRC-32C(4 sentinel entries, 80 B)   = 0x80A34955   §7.4 example ✓
CRC-32C(55 49 A3 80)                = 0xC4EE982E   §7.4 example ✓  (crc_of_crc_array)
CRC-32C(2^16 sentinel entries)      = 0xEECB3BB2   §15.4, [R-IDX-05], Appendix B ✓
Appendix A trailer CRC over [0,60)  = 0xE00938D2   stored D2 38 09 E0 ✓
```

§7.4's worked layer-record payload reproduces byte for byte at 81 bytes, and its
arithmetic (`4 + 34 + 18 + 12 + 13 = 81`) and its extent length
(`4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84`) are right.

§21.9's Note: 2³² addressed tiles ⇒ 2¹⁶ segments × 4 B = 262,144 B = 256 KiB ✓;
2³⁶ ⇒ 2²⁰ × 4 = 4 MiB ✓. §24's "tens of gigabytes" for a 2³² index region:
2³² × 20 = 85.9 GB ✓. §21.9's "65,536 layers ≈ 12.5 MiB directory" implies ~200 B
per record ✓.

## 3. Building the thing, end to end

I built a conforming file from the text alone, to find out where I had to guess.

Layer `grid`, rank 2, dimensions `y` and `x`, extents (5,5), tile extents (4,4),
interleaved, channels `a` (uint8, fill `0x07`) and `b` (uint16, fill `0xABCD`),
linearization 1, codec 1, filter 1, no alignment, no slab, index_encoding 1.

```
G = (⌈5/4⌉, ⌈5/4⌉) = (2,2)   N = 4   P = 16              §11.2
Q = 1 + 2 = 3   decoded size = P·Q = 48                    §14.2
entry_count = N = 4 (interleaved)                          §11.2, [R-CNT-17]
index extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = 84                [R-CNT-17]
layer-record inline_length = 101, sub-record sequence empty §7.4, [R-CNT-18]
```

Stored tiles: disk ordinal 0 (all 16 positions real) and disk ordinal 3
(tile coords (1,1), covering y,x ∈ 4..7 — one real position at (4,4), fifteen
padding positions). §14.5 fixes the padding content to the recorded fill, so
tile 3's image is the real sample followed by fifteen copies of `07 CD AB`;
my build emits exactly that.

Resulting file: F = 448, F mod 64 = 0, dir_offset = 196, dir_length = 129,
pre-trailer pad = 59, trailer at [384,448). §6.4's discovery window
(dir_length + pad + 64 = 252) is comfortably inside 65,536.

I then ran §9.7's walk over it. Claimants: front block [0,16); tile 0; tile 3;
index region; directory; trailer. Disjoint ✓; every non-terminal claimant inside
[16, F−64) ✓; claimed 389 bytes, slack 59 (the pre-trailer pad) ✓;
dir_offset + dir_length ≤ F − 64 ✓.

**Guesses required: none.** Every field, every derived quantity, every placement
rule and the whole coverage walk were decidable from the text. That is a real
result for a container this size and I want it recorded as such.

I then perturbed the file mentally against the register and every perturbation
landed on exactly one row with the outcome the governing rule states: entry
length 47 under codec 1 → T14; entry (offset = S, length = 5) → T7; wrong
`crc_of_crc_array` → L37 (and note §19.3's layer access does *not* reach it,
because it needs I/O — so a reader that only lists layers never detects it, which
matches L37's `tile use` detection point); channel count 0 → L32; duplicate
dimension name → L9.

## 4. The counting

§21.1 fixes the arithmetic: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written."

Hand count, then a mechanical recount by parsing the four tables:

| Subsection | Conditions | Stated | Instances |
|---|---|---|---|
| §21.2 file scope | 36 | "36 conditions" ✓ | 56 |
| §21.3 layer scope | 49 | "49 conditions" ✓ | 111 |
| §21.4 tile scope | 26 | "26 conditions" ✓ | 57 |
| §21.5 ignored records | 10 | "10 conditions" ✓ | 44 |
| **total** | **121** | §21.8 "121 conditions over 268 instances" | **268** ✓ |

Every stated total reproduces exactly. Labels are dense and gapless: F1–F36,
L1–L49, T1–T26, R1–R10.

Detector/detection-point tabulation across all 121 rows:

```
35 reader | layer access      20 verifier | certification
32 reader | open               9 reader | extent use
24 reader | tile use           1 reader | open (top-level); layer access (sub-record)   [R1]
```

Only `reader` and `verifier` appear as detectors. Every detection point is one of
§19.2's four reader tiers or `certification`, exactly as §21.1 says. Every
verifier row carries `certification` and no reader row does.

Outcome vocabulary: §2.4 defines reject-file, reject-layer, reject-tile,
ignore-record (reader outcomes) and preserve-verbatim (an updater obligation).
All four reader outcomes have a register subsection and are therefore reachable;
preserve-verbatim correctly has none, being reachable through §20.4's table.
No row carries an outcome outside the vocabulary — outcome is fixed by table
placement.

**But the cells are not written to the criterion §21.1 states.** See finding
register-01. Applying §21.1's own two-direction axis, the true instance total is
273, not 268.

## 5. Completeness, both directions

### 5.1 Rule → row

I swept every "validity error" / "reject-file" / "reject-layer" / "reject-tile" /
"ignore-record" statement in the document (76 hits) and mapped each to a row.
Every reader-detectable and verifier-detectable file-conformance violation the
document names has a row. Spot list of the mapping I most doubted:

- `[R-ENC-07]` (a known structure at any other size) — no row of its own, and
  needs none: every instance is a concrete field, and F16, F22, F23, F29, L11,
  L12, L14, L22 each carry `(R-ENC-07)` in their governing cell.
- `[R-SLB-04]` (a stale slab declaration carried forward) — §16.2's Note declares
  it has no row of its own because its detection *is* `[R-SLB-03]`'s, i.e. L41/L42.
  Checked: sound.
- `[R-CNT-02]`'s "belongs to no class" half — §5.2's Note declares "a register row
  for it would be a row no file could exhibit". Checked against `[R-LIF-08]`:
  sound, every byte the walk misses is slack by definition.
- `[R-CNT-18]`'s nesting prohibition, `[R-ENC-06]`'s field widths, `[R-GEO-06]`
  and `[R-SER-01]`'s ordinal mappings, `[R-LIF-01]`/`[R-LIF-03]` — all accounted
  in §21.7 with a stated reason ✓.
- §15.3's eleven-row entry-validity table maps onto T6–T12, T1, L18, F33,
  L40–L42 with nothing left over and nothing invented ✓.
- `[R-MTA-04]`'s four document restrictions map onto R5–R10 with nothing left
  over ✓.
- `[R-COD-06]`'s six checkable zstd constraints map onto T17–T22 plus T24 ✓, and
  the same constraints carried onto metadata encoding 2 by `[R-MTA-09]` map onto
  R4's six alternatives ✓.

### 5.2 Row → rule

Every row states a condition some rule actually makes a violation. The two I
tested hardest:

- **F19** (any incompat-lane bit set). Is a set incompat bit a violation of *this*
  text, or a later minor's file? §10.1 lists exactly four growth vehicles and
  vehicle 3 is "**New ignore-lane flag bits** in the trailer (§6.3)" — the
  incompat lane is not an extension vehicle at all, so no minor version can ever
  define one and a set bit is always a violation. F19 is right. The asymmetric
  treatment of the two lanes (ignore lane in §21.6 as a non-violation, incompat
  lane in §21.2 as F19) is coherent, not a defect.
- **R1** (encoding 0 or reserved 3–0x7F). `[R-MTA-10]` withdraws only *content*
  rules under an unassigned encoding; the encoding byte's own value set survives
  (`[R-MTA-03]`, `[R-EXT-03]`), so encoding 0 and the reserved range stay
  violations while ≥ 0x80 is §21.6's non-violation. §21.5's preamble says exactly
  this. Checked against `[R-MTA-10]`'s own text: sound.

§21.6's fourteen non-violation entries all check out against their cited rules,
including the two structural cases (unimplemented major; experimental-range
MU = 1 record) that §2.3 calls "the other two" — that cross-reference resolves.

### 5.3 Specializations

§21.1 names three: "F1 of F6 and of F8, F35 of F36, L24 of L25". All three hold.
I looked for unlisted ones. The near misses are overlaps, not specializations
(F22 ∩ F30 at extent_length 0; L11 ∩ L15; T10 ∩ T14 under codec 1; F25 ∩ F28 on a
registered type), and §24's `[R-VEC-02]` already governs a file that cannot
isolate one row. The five "the check that detects it is X's" rows (T13, T15, T16,
T23, T26) use a different mechanism from specialization, and each explains itself
inline. No condition is assigned two different outcomes anywhere, so
`[R-CNF-07]`'s "exactly one reader outcome" holds across the register.

## 6. Cross-references to rows

Every citation of a row label anywhere in the document, checked:

| Site | Cites | Resolves? |
|---|---|---|
| §9.6 | "§21.2 rows F8 and F17" | ✓ trailer magic; committed_file_length vs transport size |
| §17.2 Note | "(§21.4, T24)" | ✓ trailing bytes after the stream |
| §21.1 | F1 of F6/F8, F35 of F36, L24 of L25 | ✓ |
| §21.1 | "(T24's *any codec*)", "(T15, T25)" | ✓ T24 is one instance; T15 has 2, T25 has 3 |
| §21.2 F33 | F9/F10, F31/F32, L16/L17, T8/T9 | ✓ all four pairs are the bounds rows at their tiers |
| §21.2 T2 | "the same byte at a padding position is T4's" | ✓ T4's instance list carries `interleaved bool fill byte` |
| §21.4 T13/T15/T16/T23/T26 | T24, T25, T2, T4 | ✓ (T26 verified by construction — see §7 below) |
| §21.6 | "(F36, L25)", "(F18 …)", "(F35, F36, L24, L25)" | ✓ |
| Appendix H | "(F1, F6)", "(…, F7)", "(…, F36, L25)", "(R1)" | ✓ |

Not one citation points at the wrong row. This is the cleanest part of §21.

## 7. A candidate finding I raised and then refuted

I suspected T26's "the check that detects it is T2's or T4's" was incomplete,
because for a **packed planar bool plane** the only structural constraints §14.5
imposes are the padding positions' fill bits *and the pad bits*, and pad bits are
T5's row, not T4's. A tile with pad bits and no padding positions (an interior
tile with P mod 8 ≠ 0) would then be detectable only by T5, which T26 does not
name.

I tested it. §17.3's shuffle is `filtered[i·n + j] = image[j·s + i]` with
`n = L/s`. Position `L − 1` is `i = s − 1, j = n − 1`, so
`filtered[L−1] = image[(n−1)·s + (s−1)] = image[L−1]` — **the final byte is a
fixed point of every stride**, for every `s | L` (position 0 likewise). Verified
numerically for L ∈ {2,4,6,8,12,16,24,32} over every divisor stride. Pad bits live
in the final byte's high positions (§14.3), so a mis-strided shuffle can never
disturb them, and T5 can never witness T26.

T26's cross-reference is therefore **correct as written**, and its
packed-planar-bool instance is reachable only through T4. I confirmed that
instance *is* reachable: a plane whose bytes are `A5 5A 00 00` with fill false and
padding positions filling bytes 2–3, shuffled at s = 2, decodes as `A5 00 5A 00`
— padding byte 2 now holds `0x5A` rather than fill, and T4 fires.

Recording the refutation because a report that only lists survivors hides how the
survivors were selected.

## 8. Limits (§21.9), both directions

**Minimum guarantees.** Eight rows. Cross-checked against §2.5 `[R-CNF-10]`
("the table is §21.9"), §2.3's acceptance clause, §17.2's `Window_Size` advisory,
§18.2's 16 MiB note, and Appendix B's restatement — Appendix B reproduces all
eight values exactly (rank 32 · C 4096 · entry_count 2³² · 65,536 layers · 16 MiB
directory · 256 MiB tile · 16 MiB document · 8 MiB zstd window). No divergence.

**Hard limits.** All ten restated hard limits agree with their defining sections:
255-byte names (§4.6 `u8` prefix); 255-byte metadata keys (§18.2); rank ≤ 255 and
C ≤ 65,535 (§7.4's `u8`/`u16`); codec-4 decoded size ≤ `0x7E000000`
(`[R-COD-07]`); every offset/length/extent/count ≤ 2⁶³ − 1 (`[R-ENC-03]`);
A a power of two in [512, 2⁶²] and A_slab a power of two in [1, 2⁶²] (§7.4, §16.1,
§16.2 — note §16.2's prose gives A_slab's floor only, deferring its ceiling to
§7.4, which is consistent); S in [1, 2⁶³ − 1] (§7.4, §16.2); directory ≥ 4 bytes
at offset ≥ 16 (§6.2); no file shorter than 128 bytes (§5.1). The claim "Two do
not [follow mechanically]: the 512 floor on A … and the 255-byte cap on a
user-metadata key" is correct — every other one falls out of a field width, an
external format, the value domain, or arithmetic over structures a generation
cannot omit.

**A limit stated elsewhere and missing here.** §7.1/Appendix B's
`extent_length ≥ 5` for a user-metadata extent is not in §21.9's hard list. This
is *not* a defect: §21.9 disclaims inventory status in terms — "The hard limits it
restates are a finding aid rather than an inventory — each is normative where the
structure forcing it is defined." I checked that this hedge is actually present
before deciding not to report it.

**A limit claimed here that its defining section states differently.** None.

**Considered and rejected.** §17.2's Note says "Resource limits are §21's
subject", and §21.9 states no guarantee on a stored tile's *compressed* length,
so under `[R-ERR-04]` a reader must accept a stored extent of any length whose
decoded size is within 256 MiB. I decided this is not a finding: the stored
extent is bounded by F through T9, a reader allocates from declarations
(`[R-SEC-02]`), and the text does decide the question — it just decides it
permissively. Recording the consideration rather than filing it.

## 9. Findings

### register-01 — §21.1's two-direction instance axis is not applied at F17, L21, L22, L30

**Kind:** CONTRADICTION. **Location:** §21.1; §21.2 F17; §21.3 L21, L22, L30;
§21.8 `[R-ERR-02]`.

§21.1 states the axis as a rule, not as guidance:

> "Two axes recur often enough to be stated rather than judged each time. Where
> the quantity a condition derives varies by layout, the layout formulas are
> materially different shapes and the cell enumerates them. Where the condition
> compares two quantities and either can be the greater — a *differs from* or
> *does not equal* — the two directions are likewise enumerated; where its own
> text bounds the comparison in one direction — an *exceeds*, a *larger than* —
> there is one."

Three rows obey it. T3 ("is not exactly the tile's decoded size") enumerates
`interleaved P·Q, payload longer; interleaved P·Q, payload shorter; …` — six
instances, two directions across three layouts. T14 ("length differs from") and
T22 ("does not equal") likewise carry six.

Four rows do not:

> "| F17 | Trailer committed_file_length **does not equal** the
> transport-authoritative file size (physical file **not truncated or extended**
> to it) | committed_file_length | reader | open | `[R-CNT-06]` (R-LIF-04,
> R-CNT-10) |"

F17's own condition text names both directions in its parenthetical, and its cell
gives one instance where the axis requires two. Both directions are ordinary,
distinguishable files: a physically truncated file, and a completed commit with
residue past F — the case §9.5's Note discusses in its own right
("Residue past a completed commit carries no register row of its own. A reader
meets it as a trailer that fails its gates").

> "| L21 | entry_count **does not equal** the geometry-derived addressed-tile
> count (N interleaved, C·N planar) | interleaved N; planar C·N | reader | layer
> access | `[R-CNT-17]` (R-CNT-20) |"

L21 applies the layout axis and not the direction axis: 2 instances where the two
axes together require 4.

> "| L22 | Under index_encoding 1, extent_length **≠** entry_count × 20 +
> ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero
> slot with entry_count = 0 | extent_length against the formula; slot (0,0) with
> entry_count > 0; a nonzero slot with entry_count = 0 | reader | layer access |"

L22's first instance, "extent_length against the formula", is a bare `≠` carrying
both directions: 3 instances where 4 are required.

> "| L30 | A channel entry's fill length prefix **differs from** the element size
> of the channel's declared type | — | reader | layer access | `[R-CNT-23]`
> (R-TYP-06) |"

L30 is a textbook "differs from": the prefix can be longer or shorter than the
element size, both trivially constructible. Cell reads `—`, i.e. one instance.

**Which governs.** §21.1 makes the *rule* govern a row's condition, but the
instance criterion is §21.1's own and there is no rule outside §21 for it to
defer to. So §21.1's criterion governs and four cells are wrong, and with them
§21.8's total: applying the criterion gives F17 → 2 (+1), L21 → 4 (+2), L22 → 4
(+1), L30 → 2 (+1), a corrected total of **273 instances**, not the 268 §21.8
states and I otherwise reproduce exactly.

**What an implementer does wrong.** Nothing to a file's bytes. `[R-ERR-02]` and
`[R-VEC-03]` make the instance count the corpus build list — "one vector per
instance", "every register row has at least one vector for each instance it
names". A corpus built from the cells ships five fewer vectors than the stated
criterion demands and never tests, for example, an over-long fill prefix *and* an
over-short one; a corpus built from the criterion overruns §21.8's declared total
by five and looks like it has a counting bug.

**Byte level: no.** The instance criterion governs how many files a corpus
contains. It changes no byte a writer may emit and no verdict a reader reaches:
both direction-cases of each of these four conditions are already violations
under the same governing rule, with the same outcome, detector and detection
point.

### register-02 — §21.1 says a row's outcome follows from its scope; §21.5's ten rows have an outcome no scope produces

**Kind:** CONTRADICTION. **Location:** §21.1; §2.4 `[R-CNF-08]`; §21.5 R1–R10;
§18.1 `[R-MTA-02]`.

§21.1 describes the outcome column twice, both times as scope-determined:

> "each row is one malformed condition, with **the outcome class its scope
> determines** (§2.4), the actor obliged to detect it …"

and

> "Conditions attach to the finest structure they damage, and **the outcome
> follows from that scope**, never from the severity of the corruption."

§2.4's scope mapping has exactly three outputs and ignore-record is not among
them:

> "The phrase 'a validity error at the owning scope' means the reader outcome for
> that scope: file → reject-file, layer → reject-layer, tile → reject-tile.
> `[R-CNF-08]`"

Yet §21.5's ten rows all carry ignore-record, and for a *top-level* user-metadata
record the owning scope is the file. §18.1 says so and says the outcome does not
follow from it:

> "The owning scope of a user-metadata record is the file when the record is
> top-level and the layer when it is a sub-record — but the outcome of every
> failure to read its **document** is ignore-record whatever the scope, because
> the document is **quarantined** (`[R-CNT-25]`)."

So the register's own governing section states a rule that a full twelfth of the
register (10 of 121 rows) contradicts by design, and states it without the
carve-out. §21.5's preamble carries the carve-out — "every way its document can
be unreadable takes this outcome, **whatever the containing scope**" — but §21.1
is where a reader is told how to read the table, and it is where the rule is
stated wrongly.

**Which governs.** §21.1's own escape clause, "where a row and the rule it cites
diverge, **the rule governs**", sends the reader to `[R-CNT-25]` and
`[R-MTA-02]`, which say ignore-record notwithstanding `[R-CNF-08]`. So the rows
are right and §21.1's two general statements are the defective text. But a reader
who applies §21.1 as written — the section that exists precisely to tell him how
to apply the table — derives reject-file for R1–R10 at file scope and
reject-layer at layer scope.

**What an implementer does wrong.** Refuses a whole file, or a whole layer, over
an unreadable user-metadata document — the exact outcome the quarantine exists to
prevent, and the one §18.1, §7.1 and §22.4 spend paragraphs on ("Application
metadata never invalidates the structural data it annotates").

**Byte level: no**, and this is the case I most wanted to be byte-level. It is
not, because every one of R1–R10 is a *violation*, so the file is nonconforming,
and `[R-CNF-12]` independently licenses any reader to reject a nonconforming file
at any scope: "For a nonconforming file no acceptance obligation exists — a
reader MAY reject it upon detecting any violation." Both the misreading reader
and the correct reader are conforming. The one place a fork could arise —
a *conforming* file carrying an unassigned-encoding document — is §21.6's row,
not a §21.5 row, and §21.6 states the outcome without reference to scope.

### register-03 — the "Governing rule" cell's parenthesized identifiers are never defined, and §24 requires a single one

**Kind:** AMBIGUITY. **Location:** §21.1; §21.2–§21.5 column 6; §24
`[R-VEC-02]`.

Every register cell in the last column has the shape "`[R-XXX-NN]` (R-YYY-MM,
R-ZZZ-KK)" — one identifier in the `[R-…]` form §2.2 defines, then zero or more
bare, unbracketed, un-backticked identifiers in parentheses. F1 reads
"`[R-ENC-02]` (R-CNT-04, R-CNT-06)"; L2 reads "`[R-ENC-04]` (R-GEO-03, R-CNT-13,
R-SER-02, R-SER-07)"; L26's parenthetical is not an identifier at all —
"`[R-CNT-18]` (§7.3 registry table)".

The convention is nowhere stated. §21.1 describes the column in the singular —
"and **the requirement that defines it**" — and its escape clause is likewise
singular: "each row *restates* its governing rule, and where a row and **the rule
it cites** diverge, the rule governs." §4.7's Note explains the columns of layout
tables and does not reach the register. §24 then makes the question operative:

> "the §21 register row it exercises together with **that row's governing
> requirement identifier** — row labels are positional and renumber when a row is
> struck, while §2.2 makes the identifier permanent, so the pair is what survives
> a renumbering."

**Permitted readings.** (a) The bracketed identifier is the governing rule and the
parenthesized ones are informative cross-references. (b) All identifiers in the
cell co-govern, the bracketing being typographic emphasis on the primary one.

**Which I picked and why.** (a). Three things point at it and none is stated:
§2.2 defines the identifier form as `[R-<PREFIX>-<NN>]`, so a bare `R-CNT-04` is
not an identifier of the defined form at all; the column header and §21.1's prose
are singular; and L26's parenthetical holds a section reference, which cannot
co-govern anything. Under reading (b), §24's singular "that row's governing
requirement identifier" has no referent for the 60-odd rows carrying more than one.

**What an implementer does wrong.** Builds a conformance manifest whose
row-to-requirement pairing is not the one the corpus maintainer used, so the pair
`[R-VEC-02]` designed to survive renumbering does not survive it; or, taking
reading (b), treats §21.1's "the rule governs" as ambiguous whenever a row's
several cited rules could be read against each other.

**Byte level: no.** This is a manifest-construction and document-navigation
question. I checked every multi-citation cell for a case where the bracketed and
parenthesized rules would give different answers about a file, and found none:
the parentheticals are uniformly consistent with the bracketed rule.

### register-04 — §21.1's list of verifier rows a reader must serve unchanged omits `[R-MTA-05]`, the rule behind F27 and L48

**Kind:** OBSERVATION. **Location:** §21.1; §21.2 F27; §21.3 L48; §18.2
`[R-MTA-05]`; §21.6 closing.

§21.1 defuses the outcome column for verifier rows and names the rules involved:

> "For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader: the governing rule
> states what a reader does, and for several such rows it obliges the reader to
> serve the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`)."

Two identifiers. There is a third rule in exactly that class, and it is the one
governing the two rows §21.6 says were most recently moved into the register:

> "Readers MUST NOT depend on member order for meaning, and unsorted members do
> not make a document unreadable: the file is nonconforming, a verifier MUST
> report it, and **readers process the document unchanged**. `[R-MTA-05]`"

and §21.6 confirms these two rows are the new arrivals:

> "Two conditions that once sat in this table are violations and are registered
> above: a user-metadata document whose object members are unsorted
> (`[R-MTA-05]`), and a registered record type whose stored MU or PE bit differs
> from §7.3's registry (`[R-CNT-22]`). Both make the file nonconforming while
> leaving every reader behavior unchanged."

`[R-CNT-22]`, the second of that pair, made it into §21.1's parenthetical.
`[R-MTA-05]`, the first, did not — so F27 (a verifier row in §21.2, outcome
reject-file) and L48 (a verifier row in §21.3, outcome reject-layer) sit in the
register with the harshest outcomes in the vocabulary, and the sentence that
exists to tell a reader those outcomes bind nobody omits the rule that would
confirm it for them.

**Which governs.** `[R-MTA-05]`, by §21.1's own "the rule governs" clause:
readers process the document unchanged, and a file whose only defect is unsorted
metadata members is served in full by a conforming reader.

**What an implementer does wrong.** Reads F27, sees `reject-file`, checks §21.1
for the escape, finds a closed-looking parenthetical that names two rules neither
of which is F27's, and concludes F27 is not one of "several such rows" — then
refuses a file over the ordering of JSON object members. §2.4's reject-file row
would seem to back him: "The file is not usable … A reader MUST NOT rely on any
structure in it."

I record this as an OBSERVATION rather than a contradiction because §21.1 says
"for **several** such rows", which can be read as illustrative rather than
exhaustive. The decision is cheap to make and expensive to leave to each reader.

**Byte level: no**, for the same reason as register-02: F27 and L48 make the file
nonconforming, so `[R-CNF-12]` licenses the refusal anyway, and §24's Note already
provides for it — "an implementation that instead rejects the whole nonconforming
file is exercising `[R-CNF-12]`'s licence, not failing the vector."

## 10. Things I checked and found clean

Recorded so the report is legible as coverage, not just as a list of complaints.

- All 121 row labels dense and gapless; all four stated per-subsection counts and
  §21.8's 121/268 reproduce mechanically.
- Every row cites a rule that exists and says what the row says, with the four
  exceptions above (none of which is a mis-citation).
- Every cross-reference to a row from outside the tables resolves to a row that
  says what the citing text claims. Not one exception.
- Every reader-detectable violation the document names has a row; no row invents
  a violation. Both directions swept.
- Every row's detection point is discharge-able without violating `[R-ENC-05]` /
  `[R-ENC-10]`: the checksum covering the field is verified at or before the
  named tier in every case (directory CRC before the record walk; segment CRC
  before entry use; extent CRC before document rules).
- §21.9's eight guarantees agree with §2.3, §2.5, §17.2, §18.2 and Appendix B;
  its ten hard limits agree with §4.2, §4.6, §5.1, §6.2, §7.4, §16.1, §16.2,
  §17.2, §18.2.
- §21.6's fourteen non-violations each agree with the rule cited, including the
  "conforming files a reader nevertheless refuses" pair that §2.3 calls "the
  other two".
- §21.7's two classes account for everything I could find that fails the
  detectability gate; `[R-CNT-08]`'s updater copy-forward and `[R-LIF-02]`'s
  protocol ordering are covered by the "properties of a file's history" class
  even though not named by identifier.
- T2/T4's split of `[R-SER-08]` across real and padding positions leaves no gap.
- T26's "the check that detects it is T2's or T4's" is correct — refuted my own
  suspicion by proving the shuffle's endpoint fixed points (§7 above).
- The §7.4 worked example, Appendix A's 128-byte file, and every named constant
  reproduce byte for byte.
