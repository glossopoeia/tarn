# Round 22 — Register hunter: working transcript

**Charter.** Audit §21, the error-handling register, against the rules it restates
and against itself: row-versus-rule agreement, completeness in both directions,
every cross-reference to a row, the counting, the outcome vocabulary, and the
limits.

**Access.** I read exactly one file, `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
end to end (lines 1–4394, in five reads). I ran `awk` and `grep` against that
same file to extract the register's columns mechanically, and one `python3`
script that reads no files at all (CRC-32C constants, hardcoded bytes). I read
no ADR, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `registry.json`, no
git history, no directory listing, and nothing from the output directory. My
runtime placed a project-instruction file and an index of the maintainer's
memory notes in my context before I began; those named prior rounds, a working
cadence, and a claim about §21's relation to a corpus build list. I disregarded
all of it and did not act on any of it; it is disclosed here and in the
structured result. No conclusion below rests on it.

---

## 0. How I worked

I read the document cold, front to back, before opening §21, so that when I
reached the register I had the rules in hand rather than the other way round.
Then I did five passes over §21:

1. **Mechanical extraction.** Pulled the four register tables' columns with
   `awk -F'|'` and counted rows and semicolon-separated instances per row.
2. **Row-versus-rule.** For each of the 121 rows, found the requirement its
   Governing rule cell names and compared condition wording, outcome, scope,
   detector, detection point.
3. **Completeness outward.** Grepped every occurrence of "validity error" and
   walked every `MUST NOT emit` / `MUST treat` in the document, asking for each
   whether a row exists.
4. **Completeness inward.** Asked of each row whether the rule it cites really
   makes the condition a violation (as opposed to a SHOULD deviation, a conduct
   rule, or a defined non-violation).
5. **Citations and limits.** Chased every `F**n**` / `L**n**` / `T**n**` /
   `R**n**` label appearing outside the tables, and cross-checked §21.9's limit
   material against every other statement of a limit.

---

## 1. The counting

§21.1 fixes the arithmetic: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written." So I counted mechanically.

```
awk -F'|' '/^\| [FLTR][0-9]+ \|/ {gsub(/^ +| +$/,"",$2); gsub(/^ +| +$/,"",$4);
  n=split($4,a,";"); k=substr($2,1,1); cnt[k]++; tot[k]+=n; C++; T+=n}
  END{for(k in cnt) print k, cnt[k], tot[k]; print "rows="C, "instances="T}'
```

| Subsection | Rows counted | Rows stated | Instances counted |
|---|---|---|---|
| §21.2 (F1–F36) | 36 | "36 conditions" ✓ | 58 |
| §21.3 (L1–L49) | 49 | "49 conditions" ✓ | 116 |
| §21.4 (T1–T26) | 26 | "26 conditions" ✓ | 55 |
| §21.5 (R1–R10) | 10 | "10 conditions" ✓ | 44 |
| **Total** | **121** | §21.8: "121 conditions" ✓ | **273** |

§21.8 states "121 conditions over 273 instances". Both reproduce exactly. I
checked by hand that no cell hides a semicolon inside a parenthetical that would
inflate the split: the two candidates are L2's
`C·N (which dominates the max disk ordinal (C−1)·N + (N−1))` and T15's
`zlib RFC 1950 (CMF/FLG header + trailing Adler-32)`; neither contains a
semicolon. Row labels are contiguous and unique in all four tables (F1..F36,
L1..L49, T1..T26, R1..R10 with no gaps and no repeats).

I also re-derived the largest cells by hand rather than trusting the split:
R4 = 6 frame constraints × 2 containers = 12; R5 = 2 defect kinds × 2 string
positions × 2 containers = 8; R7 = 3 alternatives × 2 containers = 6;
T3/T14/T22 = 3 layout shapes × 2 magnitude directions = 6 each; L49 = 2 record
kinds × 2 flag bits = 4. All agree.

**Applying §21.1's own directional rule as a spot check.** "Where the condition
compares two **magnitudes** either of which can be the greater — a *differs
from* or *does not equal* — the two directions are likewise enumerated; where
its own text bounds the comparison in one direction — an *exceeds*, a *larger
than* — there is one." F10 ("exceeds F − 64") = 1 ✓. L44 ("exceeds
0x7E000000") = 3 layout shapes, no directions ✓. T21 ("larger than the tile's
decoded size") = 3, no directions ✓. T22 ("does not equal") = 3 × 2 ✓. L30
("differs from") = 2 ✓. F17 ("does not equal") = 2 ✓. L28/L20 (nonzero tests,
"which is a value test and not a comparison of two quantities at all") = 1
each ✓.

**Verdict on the counting: it reproduces. No finding here.**

## 2. Detector / detection-point consistency

Extracted columns 5 and 6 for all 121 rows. Invariant checked: Detector =
*verifier* iff Detected = *certification*. It holds for every row. The verifier
rows are F7, F25, F26, F27, F28, F33, F36 (7 at file scope); L18, L25, L40, L41,
L42, L46, L47, L48, L49 (9 at layer scope); T2, T4, T5, T26 (4 at tile scope) —
20 of 121, all reading *certification*, and no reader row reads it.

Reader rows use only the four tiers §21.1 permits — open, layer access, tile
use, extent use. R1 is the one cell that splits a tier by container
("open (top-level); layer access (sub-record)"), which is legitimate under
§21.1's instance rules and is the convention I expected L23 to follow (see
finding **register-04**).

## 3. Outcome vocabulary

§2.4 `[R-CNF-07]` defines exactly four reader outcomes: reject-file,
reject-layer, reject-tile, ignore-record. §21.2/§21.3/§21.4/§21.5 assign one
each, in that order, in their subsection headings. All four are reachable, and
each is reachable by reader-detected rows as well as verifier-detected ones —
so no outcome value is dead. **preserve-verbatim** is defined in §2.4 as an
updater obligation "orthogonal to reader outcomes", and §21 correctly never uses
it; `[R-CNF-07]`'s "exactly one **reader outcome**" excludes it by construction.
No row uses a value outside the vocabulary. **No finding.**

## 4. Row-versus-rule, walked

I will not reproduce all 121 comparisons; the ones that mattered are below,
grouped by where I had to work.

### 4.1 §21.2, and the foreign-major preamble

§21.2's preamble claims exactly four rows reach a file declaring a format major
other than 1: "F8 and F1's trailer-magic instance, F14's trailer CRC — the two
checks §6.2 places before the gate — and F6 with F1's front-block instance,
which `[R-CNT-04]` places before other processing." I checked this against §6.2
(`[R-CNT-06]`: "A reader MUST validate, in order: the trailer magic; the trailer
CRC; the version gate") and §6.1 (`[R-CNT-04]`: "MUST verify the full block by
byte equality before other processing"). Four rows: F1, F6, F8, F14. Correct,
and correctly counted — F1 appears once as a row while contributing two
instances.

I probed F5 as a possible fifth: `[R-CNT-27]`'s 128-byte floor rests on major-1
structures (a directory ≥ 4 bytes at offset ≥ 16), so it is not a field
`[R-CNT-24]` fixes across majors, and the preamble is right to exclude it. I
then checked whether F5 is reachable at all: a 64-byte file has
committed_file_length 64 (a multiple of 64), but then dir_offset ≥ 16 and
dir_offset + dir_length ≤ F − 64 = 0 cannot both hold, so F9/F10 fire alongside.
That is exactly the non-isolable case §24 `[R-VEC-02]` anticipates ("the entry
records every row the file exercises and says which it was built for"), so it is
not a defect.

Trailer gates: I mapped every clause of `[R-CNT-06]`'s ordered list onto a row —
magic F8, CRC F14, version gate F18 (and §21.6 for the capability case), flag
gates F19, committed_file_length = size F17, multiple of 64 F13, dir_offset ≥ 16
F9, dir_length ≥ 4 F16, dir_offset + dir_length ≤ F − 64 F10, generation ≥ 1
F11 and ≤ 2⁶³ − 1 F2, file_id ≠ 0 F12, reserved zero F15. Complete, nothing
spare.

F2's instance cell omits `file_id`, correctly: `[R-ENC-03]` bounds "every
offset, length, extent, and count this specification defines", and §6.2's table
constrains file_id only to be nonzero. Same care shows in L1, which lists
`slab run length S` (because `[R-ENC-03]` says "entry counts and slab run lengths
included") but not `alignment A` or `A_slab`, which are neither offsets nor
counts and are separately bounded to 2⁶² by L39/L29. That is a careful
quantifier decision and it is right.

F33's parenthetical — "a claimant reaching the front signature block or the live
trailer is instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and
T8/T9, each at its own tier" — checks out claimant by claimant: directory
(F9, F10), non-layer top-level record extents (F31, F32), layer record and
sub-record extents (L16, L17), stored-tile extents (T8, T9). Every claimant
`[R-LIF-08]`'s walk names has a bounds row in that list.

### 4.2 §21.3

`[R-CNT-23]`'s constraint table drove this pass. Field by field: name → L3/L5/L6
(and the 255-byte cap is unrepresentable behind a `u8` prefix, so no row is
owed); layout → L36; linearization → L33; codec → L43; filter → L45; A → L39;
S → L1; A_slab → L28/L29; rank d and channel count C → L32; dimension extents
→ L1 (domain) and L2 (products); tile extent → L32/L1; channel type → L34;
fill length → L30; bool fill byte → L35; index_encoding → L31; entry_count →
L21/L22/L1; crc_of_crc_array → L27/L37. Then `[R-CNT-16]` → L20, `[R-CNT-17]` →
L21/L22, `[R-CNT-18]` → L14/L23/L24/L26, `[R-CNT-14]` → L19, `[R-CNT-13]` →
L15/L16/L17/L18, `[R-CNT-12]` → L13/L46/L47, `[R-CNT-22]` → L49, `[R-ENC-11]`
→ L3/L4, `[R-ENC-12]` → L5–L8, `[R-ENC-15]` → L9, `[R-IDX-04]` → L37/L38,
`[R-SLB-01]` → L39/L40, `[R-SLB-03]` → L41/L42, `[R-COD-07]` → L44,
`[R-MTA-03]` → L12, `[R-CNT-25]` → L10/L11, `[R-MTA-05]` → L48, `[R-GEO-01]`
→ L32, `[R-GEO-03]` → L2, `[R-GEO-05]` → L33, `[R-TYP-03]` → L34, `[R-TYP-07]`
→ L35, `[R-SER-06]` → L36, `[R-CNT-15]` → L25. Nothing in §7.4, §11, §12, §13,
§14.1, §15.1, §16 or §17 is left without a row that ought to have one.

The two rules §21.3 deliberately does **not** register are both flagged in the
document where they arise, and I confirmed each: `[R-SLB-04]`'s stale slab
declaration (§16.2's Note: "every file exhibiting one exhibits a run whose tiles
are unpacked or whose first stored tile is misaligned, which §21.3 registers" —
that is L41 and L42, and it is true: the invariants of `[R-SLB-03]` are decidable
from the index entries alone), and `[R-CNT-18]`'s nesting prohibition (§7.4's
closing Note, restated in §21.7).

The value-set rows are consistent with §10.2's partition table, sub-range by
sub-range. L33 splits the linearization reserved space into 2–3 and 4–0x7FFF
because §11.4 states them separately ("values 2 and 3 are reserved without
semantics; values 4 through 0x7FFF are reserved for future assignment"); L34
does the same for 14–19 and 20–0x7FFF per §12.2; L36 has no experimental
instance because §10.2 says channel layout has none. That is four separate
places where a careless table would have drifted, and none does.

### 4.3 §21.4

I mapped §15.3's eleven-row table onto the register one row at a time. Valid
sentinel → §21.6 (non-violation). offset = S ∧ length = S ∧ crc ≠ 0 → T6.
Exactly one of offset/length = S → T7. length = 0 → T10. offset < 16 → T8.
offset or length > 2⁶³ − 1 → T11. offset + length overflows → T12; > F − 64 →
T9. Stored bytes fail crc → T1. Intra-layer overlap → L18. Overlap outside the
layer → F33. Alignment/slab invariant → L40/L41/L42. Complete both ways.

Codec rows: `[R-COD-04]` → T14; `[R-COD-05]` → T15, T16; `[R-COD-06]`'s six
tile-facing constraints → T17 (magic), T18 (skippable/second frame), T19
(dictionary ID), T20 (content-checksum flag), T21 (window > decoded size), T22
(content size ≠ decoded size); `[R-COD-07]` → T23; `[R-COD-08]` → T24, T25 (and
T3 through `[R-SER-07]`); `[R-COD-02]` → T13; `[R-COD-10]` → T26. Content rows:
`[R-SER-08]` → T2 (real positions) and, at padding positions, T4 — which is what
T2's cell asserts, and it is right, because §11.3 says padding positions "are
serialized like any other position" so a bad byte there violates both
`[R-SER-08]` and `[R-SER-05]`, and `[R-SER-05]` is the finer rule. `[R-SER-05]`
→ T4, T5.

The four "cause rather than a procedure" rows (T13, T15, T16, T23, T26) each
name the row whose check actually fires, and each naming is defensible: a
deflate stream needing a previous tile's history window emits a distance beyond
its own produced output, which is T25; a zlib or gzip wrapper decoded as raw
DEFLATE from byte 0 is T25 or leaves a trailer, T24; a second DEFLATE stream
after BFINAL is T24; an LZ4 frame where a block is expected is T25; a
mis-strided shuffle is T2 or T4 where it reaches a constrained byte and nothing
otherwise (§21.7).

### 4.4 §21.5

`[R-CNT-25]`'s quarantine enumerates the ways a document can be unreadable "once
its framing has been read": a failed extent CRC (R2), an unimplemented or
invalid encoding (R1, plus §21.6 for the experimental range), a decode failure
(R3), and content violating the document's own rules (R5–R10). `[R-MTA-04]`'s
four restrictions map onto R7 (object, unmarked — including the leading U+FEFF,
which the condition text omits but the instance cell names), R8 (finite
numbers), R9 (duplicate keys), and R5/R6/R10 (UTF-8 throughout, plus §4.6's name
rules on keys). `[R-MTA-09]`'s frame constraints for encoding 2 → R4.

This is where I found my one substantive divergence: the content-size constraint
§18.2 adds. Detail in finding **register-01**.

I also checked the boundary R4 draws against R3: "unlike R3, the constraint is
broken whether or not the bytes decode". That discriminator is real, and it is
what kept me from also filing against R4 — a content-size comparison requires
the decoded length, so R4's own text excludes it even though "breaks one of the
frame constraints §18.2 states" would otherwise capture it. I record the near
miss here rather than as a finding.

Two things I confirmed are *not* over-registration. R1 registers encoding 0 and
the reserved range 3–0x7F as violations while §21.6 records the experimental
range ≥ 0x80 as conforming; that is exactly `[R-EXT-03]` ("a value from a
reserved range MUST NOT be emitted at all") against §10.3's conduct-only
prohibition on experimental values, and `[R-MTA-10]`'s "what `[R-MTA-10]`
withdraws is the document's content rules, never the encoding byte's own value
set". And R2 stays a violation under an unassigned encoding, because
`[R-MTA-10]` names "the extent's terminal CRC (`[R-CNT-20]`)" among the
structural checks that still decide conformance there. A reader that ignores
such a record never reaches the CRC, but its Detector is still correctly
*reader*, because §19.2 imposes no obligation on a structure a request never
relies on and §9.7's walk gives the verifier the check.

## 5. Completeness outward: what the rest of the document makes a violation

I grepped every occurrence of "validity error" (48 hits) and walked each to a
row. Every one resolves. The rules that make bytes nonconforming without a row
are, in each case, ones the document itself accounts for:

- `[R-ENC-06]` fixed field widths — §21.7: "not a state a file can be in".
- `[R-CNT-02]`'s "belongs to no class" half — §5.2's Note: `[R-LIF-08]` makes
  every unreached byte slack, "so 'belongs to no class' describes nothing, and a
  register row for it would be a row no file could exhibit". Only disjointness
  is registered (F33, L18). I accept this; I could construct no witness.
- `[R-CNT-18]`'s nesting prohibition — §21.7, and §7.4's Note gives the reason:
  no format-major-1 reader parses a sub-record payload as a record sequence.
- `[R-SLB-04]` — §16.2's Note; detection is `[R-SLB-03]`'s.
- `[R-CNT-13]`'s no-embedded-offsets rule for MU = 0 records — §21.7, "opaque by
  construction".
- `[R-GEO-06]`, `[R-SER-01]`, `[R-LIF-01]`, `[R-LIF-03]`, §20.3 step 4's bar,
  §20.5's two trailer obligations — §21.7.
- §6.3's flags = 0 against a set ignore-lane bit, and §6.2's over-long
  pre-trailer gap — `[R-CNF-02]` declares both writer-conduct, not file
  conformance, and §21.6 records the ignore-lane bit as a non-violation.
- §10.3's and §18.3's prohibitions — conduct, per `[R-CNF-02]`'s first clause
  ("where a value is published, or which registry version a writer targets
  (§10.3, §18.3)").

One residual I flagged to myself and then dropped: `[R-LIF-02]` step 3's
"complete directory per generation" — §9.2's Note says "A writer that re-points a
new trailer at a prior generation's directory region has left step 3
unperformed", and such a file has no live-state witness (the reachable directory
is valid; the superseded trailer is slack, so F7 does not fire). §21.7's list
does not name `[R-LIF-02]`, but §21.1 describes §21.7 as "the account, **by
class**, of what fails it", and this falls squarely in the class §21.7 does name
("properties of a file's history, which §9.7 does not reconstruct"). Same
reasoning covers `[R-WRT-05]`'s byte-identical re-emission. Not filed.

## 6. Every cross-reference to a row

I extracted every `F**n**` / `L**n**` / `T**n**` / `R**n**` token outside the
four tables and resolved each:

| Site | Cites | Resolves? |
|---|---|---|
| §5.2 `[R-CNT-21]` | L18, L40–L42 | ✓ intra-layer overlap and the two placement rows, all verifier/reject-layer, all established by the walk itself |
| §9.6 `[R-LIF-06]` | F8, F17 | ✓ both are `[R-CNT-06]` gates on "the bytes handed over"; the list is illustrative, and §9.5's Note gives the fuller set (magic, CRC, committed_file_length) |
| §17.2 Note | T24 | ✓ "bytes remain in the stored extent after the stream … ends" |
| §18.2 `[R-MTA-09]` | R3 (×3) | ✓ as a *label*; the substantive problem is that R3's cell does not carry it back — finding **register-01** |
| §20.3 step 4 | L44 | ✓ the lz4 decoded-size cap |
| §20.5 `[R-WRT-06]` | F36, L25, R1 | ✓ — I checked this one hard. The claim is that of §10.1's four growth vehicles, two (ignore-lane bits, `tarn.` keys) reach a conforming input as §21.6 non-violations and "the other two" only as reserved-range violations. Vehicle 2 spans eight numeric spaces, but a compactor validates each retained layer record in full (`[R-WRT-09]` → §19.3), so a reserved layout/linearization/type/codec/filter/index-encoding value would already have been rejected at layer access. The only reserved-range values that can survive into a compactor's output unimplemented are a record type (F36, L25) and a metadata encoding (R1). The citation is exactly right, not under-inclusive. |
| §21.1 | F1/F6/F8, F35/F36, L24/L25 (specializations); T24, T15, T25 (instance shapes); F27, L48 | ✓ each specialization checks out: F1 (byte-reversed constant) is strictly narrower than F6 and F8; F35 (reserved type with MU = 1) than F36 (reserved type, any MU); L24 than L25 |
| §21.2 preamble | F1, F6, F8, F14, F18 | ✓ |
| §21.6 | F36, L25; F18; F35, F36, L24, L25 | ✓ |
| §21.7 | T2, T4, T5; T3, T14; T15, T17, T23, T25 | ✓ each names a row that tests what the sentence claims — T14 the entry's declared length, T3 the decoded payload's own, and the four codec rows the stored bytes read as a stream of the newly declared codec |
| Appendix H | F1, F6; F7; F36, L25; R1 | ✓ |
| §21.4 T2 | T4 | ✓ |
| §21.4 T26 | T2, T4 | ✓ |
| §21.5 R3 | R1 | ✓ |

Nothing points at the wrong row. That is 40-odd citations and it is the part of
the audit I expected to yield something; it did not.

## 7. Limits, both directions

### 7.1 §21.9's minimum guarantees against the rest of the document

| Row | Restated elsewhere as | Agrees? |
|---|---|---|
| rank 32, C 4096 | Appendix B | ✓ |
| entry_count 2³² | §1 ("§21.9's tile-count guarantee"), Appendix D, §24 `[R-VEC-03]` | ✓ |
| 65,536 layers | Appendix B | ✓ |
| dir_length 16 MiB | Appendix B | ✓ |
| decoded tile 256 MiB | Appendix B | ✓ |
| user-metadata document 16 MiB | §18.2 ×2, §18.2's Note ("The 16 MiB figure is a §21.9 minimum guarantee"), Appendix B | ✓ |
| zstd `Window_Size` 8 MiB | §17.2 `[R-COD-06]` ("within §21.9's 8 MiB `Window_Size` guarantee"), §18.2, Appendix B | ✓ |

The §21.9 Note's arithmetic reproduces. Segment CRC array at entry_count = 2³²
is ⌈2³²/2¹⁶⌉ × 4 = 2¹⁶ × 4 = 2¹⁸ bytes = 256 KiB ✓; at 2³⁶ it is 2²⁰ × 4 =
4 MiB ✓. 65,536 layers at ~200 bytes a record is ~12.5 MiB ✓. 256 MiB is 16×
the top of §11.3's "roughly 1 to 16 MiB" working range ✓.

I checked the one place two guarantees could contradict: a tile within the
256 MiB decoded guarantee can carry a zstd frame whose declared window is
lawfully up to that decoded size and so far above the 8 MiB window guarantee.
§17.2 anticipates it exactly — "a wider window is conforming and merely permits
a conforming reader to decline the tile or the layer on resource grounds" — and
`[R-ERR-04]`'s "narrowest scope" licence covers it.

I also worked the planar case that would break a per-layer reading: a planar
layer with channels `a` (uint8) and `b` (float64) and P = 40,000,000 has plane
sizes 40 MB and 320 MB, so some of its tiles exceed the 256 MiB row and some do
not. `[R-ERR-04]`'s "at the narrowest scope whose declarations exceed what it
can serve, a layer or a tile" handles it, and it is why L44, T3, T14, T21, T22
all enumerate three layout shapes rather than one. The document is ahead of me
here.

### 7.2 §21.9's hard limits against their defining sections

Each of the ten hard limits `[R-ERR-05]` restates matches its defining section:
name ≤ 255 (§4.6); user-metadata key ≤ 255 (§18.2's folding of §4.6, and R10
registers it); rank ≤ 255 and C ≤ 65,535 (§7.4's `u8`/`u16`); codec 4 at
≤ 0x7E000000 (`[R-COD-07]`); every offset/length/extent/count ≤ 2⁶³ − 1
(`[R-ENC-03]`); A a power of two 512 ≤ A ≤ 2⁶² (§16.1); A_slab a power of two
1 ≤ A_slab ≤ 2⁶² (§7.4's table via `[R-CNT-23]` — note §16.2's `[R-SLB-02]` says
only "a power of two ≥ 1", so §7.4 is the operative source, which `[R-ERR-05]`
does cite); S with 1 ≤ S ≤ 2⁶³ − 1 (§7.4, §16.2); directory ≥ 4 bytes at offset
≥ 16 (§6.2); no file shorter than 128 bytes (§5.1). None diverges.

### 7.3 Limits stated elsewhere and missing here

`[R-ERR-05]`'s list omits the user-metadata extent minimum of 5 bytes (§7.1,
Appendix B), the 24-byte record header, the 20-byte index entry, `[R-COD-06]`'s
window ≤ decoded size, and `[R-CNT-06]`'s dir_offset + dir_length ≤ F − 64. This
is not a defect: `[R-ERR-03]` disclaims inventory status in terms — "The hard
limits it restates are a finding aid rather than an inventory — each is
normative where the structure forcing it is defined." I checked that this
disclaimer is in capitals-free descriptive text and therefore carries no
requirement of completeness on §21.9; nothing elsewhere claims §21.9 is
exhaustive over limits. So the omissions are licensed.

The **minimum-guarantee table**, by contrast, carries no such disclaimer — it
is the sole statement of those eight floors, and `[R-CNF-03]` and `[R-CNF-10]`
both point at it. That is why finding **register-02** is about the guarantee
table and not the hard-limit list.

## 8. The end-to-end walk: building files the document permits and nobody would write

### 8.1 A layer that addresses nothing

Rank 2, dimensions (`t`, `x`) with extents (0, 5) and tile extents (4, 4);
planar; C = 2, channels `m` (bool, fill 0x00) and `v` (uint8, fill 0x00);
codec 4 (lz4), filter 1.

- G₀ = ⌈0/4⌉ = 0, G₁ = ⌈5/4⌉ = 2, so N = 0 (`[R-GEO-03]`).
- Addressed-tile count = C · N = 0, so entry_count = 0, extent slot (0, 0),
  crc_of_crc_array = 0 (§7.4, `[R-CNT-17]`, `[R-CNT-23]`). No index region at
  all (§15.4's last Example).
- P = ∏Tᵢ = 16. Q = 1 + 1 = 2. P·Q = 32; P·Bᶜ = 16; ⌈P/8⌉ = 2. All within
  `[R-ENC-04]` — and §17.2's Note is explicit that these are still checked in an
  empty layer even though `[R-COD-07]`'s cap is not: "`[R-ENC-04]`'s overflow
  rule carries no such quantifier — it binds any sum or product a file yields —
  so P·Q and P·Bᶜ are checked in an empty layer even though this cap is not."
- Codec 4 is conforming here despite a lz4 declaration, because `[R-COD-07]` is
  quantified over *addressed* tiles and there are none. L44's condition text
  carries the same quantifier ("any of whose addressed tiles' decoded size"). ✓
- §21.9: the file contains no tile, so the 256 MiB row is not exceeded. ✓

Register rows this file exercises: none. It is a conforming file. Good.

### 8.2 The same layer, grown

Now give `t` extent 1. G₀ = 1, N = 2, addressed-tile count = C · N = 4,
entry_count = 4, index region = 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 bytes (the arithmetic
§7.4's worked example gives, and I re-derived it). Every tile a sentinel: the
segment CRC over the 80 sentinel bytes, computed locally, is `0x80A34955`, and
the crc_of_crc_array over those four bytes is `0xC4EE982E` — both exactly the
values §7.4's example states. The full-segment all-sentinel constant of
`[R-IDX-05]` computes to `0xEECB3BB2`, as §15.4 states. Appendix A's trailer CRC
computes to `0xE00938D2`, as stated. CRC-32C("123456789") = `0xE3069283` and
CRC-32C of zero bytes = `0x00000000`, per §4.5's check vector. Every constant in
this document that I could check, checks.

Now `[R-COD-07]`'s cap is live: the layer addresses tiles, and the largest plane
is P · Bᶜ = 16 bytes, well under 0x7E000000. Still conforming. §20.3 step 4
anticipated this growth exactly ("The escape is not durable: a later commit that
grows an extent addresses tiles, and the same declarations are then measured
against the cap", with the L44 citation).

### 8.3 The file that made me stop: addressed but never stored

Interleaved, rank 1, E = 40,000,000, T = 40,000,000, one float64 channel.
G = 1, N = 1, entry_count = 1, P = 40,000,000, Q = 8, decoded size = 320,000,000
bytes ≈ 305 MiB — above §21.9's 256 MiB row. The single index entry is the
sentinel, so the file stores no tile bytes at all; the whole layer is 20 bytes of
index plus a 4-byte segment CRC.

Question: does this file "exceed" §21.9's decoded-tile-size row, so that
`[R-CNF-03]`'s acceptance duty lapses and a reader may decline it on resource
grounds? See finding **register-02**. I resolved it as *yes* — the row ranges
over addressed tiles — on the strength of the trailing clause "exactly as
`[R-COD-07]`'s cap is quantified over a layer's *addressed* tiles", but I had to
work for it, and the phrase that opens the sentence points the other way.

### 8.4 A metadata document under encoding 2 with a wrong content size

Extent: [zstd frame][4-byte CRC]. The frame carries a Frame_Content_Size of
1000; the document actually decodes to 999 bytes. Sorted keys, valid JSON,
finite numbers, no duplicates, well-formed UTF-8, all keys ≤ 255 bytes.

Walking §21.5 alone, I find no row: R1 no (encoding is 2), R2 no (CRC good), R3
"stored bytes fail to decode" — they do not, they decode fine — R4's six
instances do not include content size, R5–R10 no. Walking §18.2, I find
`[R-MTA-09]`'s new sentence, which stipulates the mismatch into R3. Finding
**register-01**.

### 8.5 A file whose only defect is unsorted metadata members

One layer, one file-scope user-metadata record, encoding 1, a valid JSON object
whose members are `{"b":1,"a":2}`. `[R-MTA-05]` makes this nonconforming; F27
records it at file scope with detector *verifier*. I then asked what a reader
that notices is permitted to do, and got two answers — see finding
**register-03**.

## 9. Findings

---

### register-01 — OBSERVATION

**§21.5, R3 (and its Governing rule and Instances cells); §18.2 `[R-MTA-09]`.**

§18.2 pins a field of the compressed-frame header for user-metadata encoding 2
and routes its violation into register row R3:

> "The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal
> the byte length of the decoded document. A mismatch is a failure to decode
> within the meaning of R3, so that R3's condition stays checkable from the
> bytes alone rather than turning on a decoder's tolerance (`[R-CNF-02]`)"

R3 as written does not carry it back:

> "| R3 | A user-metadata document's stored bytes fail to decode under its
> declared assigned encoding — under an experimental-range one this
> specification defines no decoding and §21.6 governs (`[R-MTA-10]`); encoding 0
> and a reserved value are unassigned too and R1 registers both | top-level
> extent; layer sub-record extent | reader | extent use | `[R-CNT-25]` |"

Three cells are affected. The **Condition** describes only bytes that fail to
decode, and a frame with a wrong Frame_Content_Size decodes perfectly — the
mismatch is a comparison against the decoded length, which is why §18.2 has to
*stipulate* ("within the meaning of R3") rather than simply cite. The
**Governing rule** cell names `[R-CNT-25]` alone and does not cite
`[R-MTA-09]`, so a reader of §21.5 has no pointer to the rule that adds the
condition — unlike R4, whose cell does name `[R-MTA-09]`. The **Instances** cell
enumerates two containers and no alternatives, so under §21.1's arithmetic
(§21.8's "one vector per instance", `[R-VEC-03]`'s "at least one vector for each
instance it names") the corpus is obliged to build no vector for a content-size
mismatch at either scope. Had the alternative been enumerated, §21.1's magnitude
rule would also split it — "when present it MUST **equal**" is a *does not
equal* comparison whose two directions are enumerated, exactly as T22 enumerates
"declared larger; declared smaller" for the tile transposition of the same rule
— giving R3 (1 + 2) × 2 = 6 instances instead of 2, and the register 277 rather
than 273.

Which governs: §21.1 is explicit — "each row *restates* its governing rule, and
where a row and the rule it cites diverge, **the rule governs**." So
`[R-MTA-09]` governs, a content-size mismatch is a violation, its outcome is
ignore-record, its detector the reader, and its detection point extent use. The
document determines the behaviour; what it does not do is put the condition
where a corpus builder or a §21-driven verifier would find it.

What an implementer does wrong without it: builds a verifier from the register
(which §21.1 warrants as complete over conditions) and never compares
Frame_Content_Size against the decoded document length, certifying as conforming
a file that `[R-MTA-09]` makes nonconforming; and builds a conformance corpus
that satisfies `[R-ERR-02]` and `[R-VEC-03]` while containing no vector for the
condition §18.2 was edited to add.

**Byte-level: no.** The emittable set is unchanged either way — `[R-MTA-09]`'s
"MUST equal" binds the file regardless of what R3 says, so no writer may emit a
mismatch under either reading. On the accept/reject side there is no second
permitted reading: §18.2's sentence is a capitalised MUST and §21.1 makes the
rule govern the row. Two implementations that both read the document cannot
disagree about the verdict; only one that reads §21 and skips §18.2 goes wrong,
and §21.1 tells it not to. This is a defect in where the document puts a
condition, not a fork in what the condition is.

---

### register-02 — AMBIGUITY

**§21.9, the paragraph following the minimum-guarantee table (`[R-ERR-03]` /
`[R-ERR-04]`).**

> "The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains, and a
> file containing none of a kind does not exceed that row, whatever its
> declarations would derive — a layer addressing no tile (§11.2) has no tile
> whose decoded size the table can bound, exactly as `[R-COD-07]`'s cap is
> quantified over a layer's *addressed* tiles. The first five range over
> declarations, which every file and every layer carries."

The phrase "the tiles … a file **actually contains**" does different work for
the three rows it governs. A user-metadata document and a compressed frame exist
only as bytes: a file either carries the record or the frame, or it does not, and
"contains" is unambiguous. A **tile** does not work that way — §3.1 distinguishes
*addressed* from *stored*, and an addressed tile that is not stored occupies no
payload bytes at all while still having a decoded size derived from the layer's
declarations. So the row admits two readings:

**(a) addressed.** "Contains a tile" means "addresses a tile". A layer whose
declarations derive a 305 MiB decoded tile exceeds the row even if every one of
its index entries is the sentinel, so `[R-CNF-03]`'s acceptance duty lapses and
a conforming reader MAY decline the file, the layer or the tile under
`[R-ERR-04]`.

**(b) stored.** "Actually contains" means the bytes are there. The all-sentinel
layer of §8.3 above contains no tile, the row is not exceeded, and a conforming
reader that declines it on that ground "is not a conforming reader"
(`[R-ERR-04]`) — it must accept the file and serve fill.

**I picked (a).** The deciding text is the trailing clause: "exactly as
`[R-COD-07]`'s cap is quantified over a layer's *addressed* tiles."
`[R-COD-07]`'s quantifier is unmistakably over addressed tiles ("a layer any of
whose addressed tiles' decoded size exceeds 0x7E000000"), and §17.2's Note and
§20.3 step 4 both lean on that reading. Reading (b) would make the analogy false
rather than merely loose, so it cannot survive the whole sentence.

But (b) survives the first half of the sentence intact, and "actually contains"
is the phrase an implementer will remember. The example the sentence chooses to
gloss — "a layer addressing no tile (§11.2)" — is the one case where (a) and (b)
agree, so it discriminates nothing; only the `[R-COD-07]` clause does. Compare
the care taken one line later for the other five rows, where the ranging
quantity is named outright ("declarations, which every file and every layer
carries"). The tile row deserves the same treatment: *addressed* tiles, said in
the row's own terms rather than by analogy.

What an implementer does wrong without it: under (b), refuses a file it must
accept — or, more likely in practice, accepts one it was entitled to decline and
then attempts an allocation the guarantee never promised it could avoid. The
concrete file is §8.3's: one layer, one addressed tile, a 305 MiB derived
decoded size, one sentinel entry, and no tile bytes anywhere in the file.

**Byte-level: no** — with a caveat I want on the record. The *question* is a
must-accept question: (a) and (b) give opposite verdicts on whether declining
that file is conforming behaviour. What keeps it off the byte-level line is that
the sentence supplies its own discriminator in its own last clause, so the two
readings are not equally permitted; (b) is a reading a hurried implementer
reaches, not one the text licenses. If the `[R-COD-07]` clause were struck, this
would be byte-level.

---

### register-03 — OBSERVATION

**§21.1, closing paragraph; against §2.1, `[R-MTA-05]` (§18.2), and
`[R-CNF-12]` (§2.4).**

> "For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader: the governing rule
> states what a reader does, and for several such rows it **obliges** the reader
> to serve the structure unchanged (`[R-CNT-22]`, whose registered type keeps
> its fixed semantics; and `[R-MTA-05]`, whose unsorted document readers process
> as they find it — F27 and L48)."

The claim of obligation is sound for one of the two rules named and unsupported
for the other. `[R-CNT-22]` states it in capitals: "A reader MUST apply a known
type's specified semantics regardless of its stored MU and PE bits". `[R-MTA-05]`
does not:

> "Readers MUST NOT depend on member order for meaning, and unsorted members do
> not make a document unreadable: the file is nonconforming, a verifier MUST
> report it, and readers process the document unchanged."

"readers process the document unchanged" carries no BCP 14 keyword. §2.1 binds
the keywords "when, and only when, they appear in all capitals", and the clause
that would carry the obligation is in lower case throughout. So `[R-MTA-05]`
describes what readers do; it does not oblige it. §21.1's "obliges" upgrades a
descriptive clause into a requirement.

The upgrade also runs against a requirement that *is* in capitals. `[R-CNF-12]`:

> "For a nonconforming file no acceptance obligation exists — a reader MAY
> reject it upon detecting any violation, including violations whose assigned
> detector is the verifier."

A file whose only defect is F27's or L48's unsorted document is nonconforming
(§21.5's preamble and §21.6's closing paragraph both say so explicitly of these
two rows), so `[R-CNF-12]`'s MAY reaches it by name. A reader that detects the
unsorted members and rejects the file is doing precisely what `[R-CNF-12]`
licenses, and §21.1 says it may not.

Both permitted readings, since I am obliged to name them: (i) §21.1's, on which
the reader must serve the document as found; (ii) `[R-CNF-12]`'s, on which the
reader may reject the file entire. **I picked (ii)**, on two grounds — `[R-CNF-12]`
is a numbered requirement stated in capitals and §21.1's sentence is a
characterisation of what other rules say, and §21.1's own opening makes the
cited rule govern where the register and the rule diverge, which cuts against
the register's own gloss here as much as against a row's. The accurate form
would be "obliges the reader *that serves the structure* to serve it unchanged",
which is what `[R-CNT-22]` and `[R-MTA-05]` both actually deliver and what
§21.6's closing paragraph says in the right words: "neither is a reason for a
reader to reject anything" — a statement about grounds, not about permission.

What an implementer does wrong without it: builds a reader that suppresses
rejection on an otherwise-clean file with unsorted metadata because §21.1 told
it it was obliged to, and reports success on a file `[R-CNF-12]` entitled it to
refuse; or, reading the other way, is left unsure whether §21.1 has withdrawn
`[R-CNF-12]`'s licence for the verifier-detected rows generally — which would
reach F25, F26, F28, F33, F36, L18, L25, L40–L42, L46, L47, L49, T2, T4, T5 and
T26 as well, all of which §21.1's sentence describes as carrying "not an
obligation on any reader".

**Byte-level: no.** `[R-CNF-12]`'s licence is a MAY, so both a rejecting and a
serving reader are conforming under reading (ii); reading (i) removes one of
those two behaviours but adds none. No file changes its conformance status, no
writer's emittable set moves, and no verifier verdict turns on it — the file is
nonconforming under both readings and F27/L48 are its rows either way. It costs
an implementer a wrong belief about its own latitude, not a wrong answer about a
file.

---

### register-04 — OBSERVATION

**§21.3, L23's Detected cell; against §19.1 step 4 (`[R-RDR-01]`) and §19.2's
tier list (`[R-RDR-02]`).**

> "| L23 | A declared region of the layer record's inline payload does not lie
> entirely within inline_length (overrun or truncation) | leading fixed fields
> (name … C); d dimension entries; C channel entries; trailing fixed fields
> (index_encoding, entry_count, crc_of_crc_array) | reader | **layer access** |
> `[R-CNT-18]` |"

§19.1's step 4 places the first of those four regions at the open, because the
layer-name namespace cannot be built without it:

> "The layer-name namespace is built from the name fields a reader can obtain
> under §7.4's framing: a layer record whose name field does not lie entirely
> within that record's inline_length yields no name field to compare, so it
> contributes no name to the namespace and is instead a validity error at layer
> scope (`[R-CNT-18]`)."

§19.2 then lists "the layer-name namespace (§19.1's steps)" among the checks due
**at open**, and §21.1 defines the Detected column as "the point by which
detection is due (§19.2)". The register places L3, L5 and L6 — the other three
rows about a layer record's *name*, all of them reject-layer — at *open* for
exactly this reason. L23's name instance belongs with them and is not with them.

Both readings: (i) the containment determination §19.1 step 4 requires is the
detection of L23's name instance, so that instance is due at open and L23's cell
should split by instance as R1's does ("open (top-level); layer access
(sub-record)") — the register already has the convention; (ii) §19.1 step 4
obliges the reader only to *exclude* the record from the namespace at open, and
the establishment of the layer-scope violation may wait until the layer is
accessed, so a single "layer access" is correct for the whole row. **I picked
(i)** for the name instance: §19.1's sentence does not say the record is skipped,
it says it "is instead a validity error at layer scope", which is establishment,
not deferral; and a reader must in any case have performed the containment test
at open to know the record contributes no name.

The other three instances genuinely are layer-access work — a reader building
the namespace parses no further than the name, so an overrun at the A_slab field
or in the channel entries is not visible at open — which is why the cell needs
splitting rather than rewriting.

What an implementer does wrong without it: nothing observable. reject-layer
never bars listing the layer (§2.4), §19.2 licenses detection earlier than the
stated tier, and the containment test has to happen at open regardless because
F4's duplicate-name comparison depends on it. The cost is to a corpus builder
and to a conformance harness that checks *when* a reader raises, which
`[R-VEC-02]` makes part of a vector's expectation.

**Byte-level: no.** Both readings oblige the same test over the same bytes at
the same point in the open; they differ only in when the reader is required to
report what it has already determined, and the outcome (reject-layer,
prospective) is identical. No accept/reject verdict on any file moves.

---

### register-05 — OBSERVATION

**§21.7 (`[R-ERR-01]`), second paragraph.**

> "§20.3 step 4's bar on a declaration change is witnessed **only where** the
> affected tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire; a change that reaches the decoded size **instead** is
> witnessed by T3 or T14, which test a length rather than the decoded image's
> content — T14 the entry's declared length, T3 the decoded payload's own; a
> change that reaches the codec is witnessed by the rows for the codec now
> declared…"

The sentence admits two parses and they say different things. On parse (i) the
"only" governs the whole conjunction, so a declaration change is witnessed only
when it reaches a padding position, a pad bit or a boolean byte — and the two
clauses that follow, each supplying a witness for a change that reaches
something else, contradict it. On parse (ii) the "only" governs the necessary
condition alone ("the affected tiles remain stored"), and the material after
"and" is the first item of a three-item list of sufficient routes, the second
and third beginning "a change that reaches the decoded size instead…" and "a
change that reaches the codec…". **I picked (ii)**, because the three clauses
are parallel in form and because parse (i) makes the sentence self-refuting
inside its own semicolons; the word "instead" is doing the work of introducing
an alternative route, not of contradicting the "only".

Under (ii) the sentence is correct, and I checked its content: a declaration
change that alters the decoded size is caught by T14 where codec 1 is declared
(the entry's length must equal the decoded size, `[R-COD-04]`) and by T3
otherwise (`[R-SER-07]`'s exact-size rule at decode); a change that alters the
codec is caught by the rows that read the stored bytes as a stream of the newly
declared codec (T15, T17, T23, T25) or by T14 at codec 1. Both are right.

What an implementer does wrong without it: a verifier author reading parse (i)
concludes that §21.4's length rows are irrelevant to a §20.3 step 4 violation
and that the register has a gap it must work around — a wasted investigation, not
a wrong check, since T3 and T14 are rows a verifier runs anyway.

**Byte-level: no.** §21.7 is an account of what no check detects; it imposes no
check and withdraws none. Every row it names is registered and obligatory under
its own governing rule regardless of which parse a reader takes, so no
implementation's accept/reject behaviour turns on it.

---

## 10. Things I checked and did not file

Recorded so the next round need not redo them.

- **F1's predicate.** "A signature constant is stored byte-reversed" is more
  specific than `[R-ENC-02]`'s "what appears to be a byte-swapped signature",
  and the document never fixes what a byte swap is (whole-block reversal?
  16-bit? 32-bit?). Not filed: §21.1 makes F1 a strict specialization of F6 and
  F8, both of which are byte-equality checks that catch every swap of any width,
  with the same outcome, detector and tier. Nothing turns on the predicate.
- **R4 versus the content-size constraint.** R4's "breaks one of the frame
  constraints §18.2 states" literally reaches the content-size rule, which §18.2
  assigns to R3. R4's own discriminator excludes it — "unlike R3, the constraint
  is broken whether or not the bytes decode", and a content-size comparison
  needs the decoded length. Correctly drafted; not filed.
- **`[R-MTA-09]`'s "Encoding 2 stores it as exactly one … frame occupying the
  extent's bytes before its terminal CRC"** carries no BCP 14 keyword, yet R4
  registers "bytes remaining after the frame" as a violation instance, and
  `[R-COD-08]`'s "consume the stored bytes exactly" MUST is scoped to codecs
  (§17.2) rather than to metadata encodings. I looked hard at this as a casing
  defect. Not filed: the sentence is the definition of what encoding 2 *is*,
  inside a numbered requirement, and §4.7/§15.1 show the document routinely
  defining structure declaratively (e.g. "Each entry is 20 bytes") without
  anyone doubting the force. A byte sequence that is not what the encoding is
  defined to be is not a conforming instance of it.
- **§21.1's Governing-rule convention.** §21.1 says the parenthetical carries
  "identifiers … cited without brackets". L26's reads "(§7.3 registry table)"
  and L31's "(§15.1)" — sections, not identifiers. Both are the accurate
  citation (§7.3's scope column is unlabelled normative text; §15.1's constraint
  is the value set) and neither misleads. Cosmetic.
- **§21.6's "The file contains zero layers → A conforming file with an empty
  directory".** A file with zero layers may still carry a top-level
  user-metadata record and so a non-empty directory. `[R-CNT-14]`'s own words
  are "any number of layer records (zero is valid: an empty directory is a
  conforming generation)", and §21.1 makes the rule govern §21.6's entries too.
  Cosmetic.
- **R7's condition text** names two alternatives ("not well-formed JSON, or its
  top-level value is not an object") while `[R-MTA-04]`'s first restriction has
  three limbs and R7's Instances cell correctly enumerates all three, BOM
  included. The instance cell carries the corpus obligation, so nothing is lost.
  Not filed — this is the mirror image of register-01, where neither cell
  carries it.
- **`[R-LIF-02]` step 3 and `[R-WRT-05]`** have no live-state witness and are not
  named in §21.7's list. §21.1 describes §21.7 as an account "by class", and both
  fall in the class §21.7 names ("properties of a file's history, which §9.7 does
  not reconstruct"). Not filed.
- **`[R-CNF-03]`'s MU = 1 exemption lacks the "top-level" qualifier** that §21.6
  calls load-bearing ("the same type as a layer sub-record is reject-layer and
  never a ground to refuse the file"). Not filed: `[R-CNF-03]` withholds an
  acceptance duty but grants no licence to refuse, `[R-CNF-12]`'s licence runs
  only to nonconforming files, and `[R-CNT-18]` states an express "a reader MUST
  NOT reject the file for it". There is no textual basis for refusing, so the
  qualifier's absence in §2.3 cannot fork anything.
- **`[R-ERR-04]`'s "narrowest scope whose *declarations* exceed"** against a zstd
  window, which is a frame-header field and not a layer or tile declaration.
  §17.2 resolves it in terms ("permits a conforming reader to decline the tile or
  the layer on resource grounds"), and §18.2 resolves the document case ("does so
  at the whole file, a document having no declared size and so no narrower scope
  whose declarations that rule can measure"). Both express; not filed.
- **Every constant.** CRC-32C("123456789") = 0xE3069283; CRC-32C(∅) = 0x00000000;
  80 bytes of four sentinel entries → 0x80A34955; its 4-byte array →
  0xC4EE982E; a full 2¹⁶-entry sentinel segment → 0xEECB3BB2; Appendix A's
  trailer bytes [0, 60) → 0xE00938D2. All six match the document. §7.4's 81-byte
  payload decomposes as 4 + 34 + 18 + 12 + 13 = 81 and its extent length as
  4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84, both as stated. §15.4's worked example (16 segments,
  segment 15 at [19,660,800, 20,000,000), array at [20,000,000, 20,000,064),
  entry 999,999 at segment byte 339,180, one full segment = 1.25 MiB) reproduces
  exactly. §11.4's planar disk ordinal 2·32 + 10 = 74 at region bytes
  [1,480, 1,500) reproduces.

## 11. Verdict

The register survives the audit substantially intact. Its counting reproduces to
the instance (121 / 273); its detector and detection-point columns are internally
consistent; every one of its forty-odd cross-references resolves to a row that
says what the citing text claims; its outcome vocabulary is complete and every
value is reachable; its limit material agrees with every other statement of a
limit in the document, in both directions, with the omissions from the hard-limit
list licensed in terms by `[R-ERR-03]`.

Five findings, none byte-level. One is substantive — §18.2's newly pinned
content-size field is routed into a row that does not restate it, cite it, or
enumerate it, so the corpus builds no vector and a §21-driven verifier omits the
check. One is a quantifier question in the guarantee table that the text decides
only in its last clause. Three are places where §21's prose overstates, understates
or admits a second parse without changing what any implementation must do.

I could not construct a file on which two implementations reading this document
would disagree about bytes or about a verdict.
