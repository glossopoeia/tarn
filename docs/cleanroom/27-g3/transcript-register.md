# Cleanroom round 27 — Register hunter — working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,549 lines; the brief said 4,550 — `wc -l` reports 4549, which is the same
document with or without a trailing newline, and I mention it only because
"paths are context too" and so are counts). I read it whole, in six passes
through `Read`, plus targeted `grep`/`rg` against that same file. I ran three
local Python computations that read no files: an instance-count tabulator over
the four register tables (fed by parsing the register's markdown rows out of the
one permitted file), a CRC-32C implementation to check the document's own
constants, and a detector/detection-point consistency check over the same rows.

I opened no ADR, no findings file, no charter, no `conformance/`, no
`spec/registry.json`, no `PLAN.md`, no `AGENTS.md`, no git history. I ran no
`git log`, no `git diff`, no web search, no web fetch. I did not list any
directory. I did not read the output directory.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file pointing at `AGENTS.md`, and an index of the
maintainer's persistent memory naming several notes (working cadence, a naming
constraint, a note about the register and a "corpus build list", among others).
I did not open any of it and I have not used it. Naming that it appeared is the
disclosure; I am not repeating its contents. One line of that index does
gesture at §21's relationship to a corpus, which is exactly the sort of hint
this round's access rule exists to neutralise — I note it so a reader can
discount my §21.8 reasoning if they think it was primed. For what it is worth,
the §21.8 work below is arithmetic I did from the tables, and it reproduces.

Everything below is derived from the specification text alone.

---

## 1. First orientation: what §21 claims about itself

§21.1 is the register's own governing rule, so I read it before anything else
and extracted the claims I would have to test:

1. §21.2–§21.5 enumerate **every detectable file-conformance violation** the
   specification names. Completeness is normative in that direction.
2. Each row **restates** its governing rule, and **where a row and the rule
   diverge, the rule governs.**
3. Conditions attach to the finest structure they damage; the outcome follows
   from that scope, except where a rule assigns one expressly (the [R-CNT-25]
   quarantine, for every §21.5 row).
4. "Some rows are strict specializations of others — F1 of F6 and of F8, F35 of
   F36, L24 of L25 — and a file exhibiting a specialization is recorded against
   the narrower row, whose detector and detection point are the ones that
   apply."
5. §21.6/§21.7/§21.9 are **not** part of the register and the completeness
   clause does not reach them.
6. The **Instances** arithmetic: semicolon-separated; a cell reading `—` is one
   instance; "the count is therefore mechanical once the cell is written."
   Plus two stated axes — layout formulas enumerate; a *differs from* / *does
   not equal* enumerates two directions, an *exceeds* / *larger than* one; a
   comparison with no magnitude ordering (checksum, byte pattern against a
   constant) enumerates none; a field tested only for being nonzero is a value
   test, not a comparison.
7. Detection points are §19.2's four reader tiers or *certification*.
8. For a **verifier**-detector row the outcome names the scope at which damage
   is recorded, **not an obligation on any reader**.

That list is what I audited against.

---

## 2. The counting

### 2.1 Conditions

Row labels are contiguous in every table:

| Subsection | Rows | Header claims |
|---|---|---|
| §21.2 | F1–F36 = 36 | "36 conditions" |
| §21.3 | L1–L49 = 49 | "49 conditions" |
| §21.4 | T1–T26 = 26 | "26 conditions" |
| §21.5 | R1–R10 = 10 | "10 conditions" |
| total | **121** | §21.8: "121 conditions" |

Reproduces exactly.

### 2.2 Instances

I applied §21.1's own mechanical rule — split the Instances cell on `;`, count
the pieces, count a bare `—` as 1 — to all 121 rows. Per-subsection subtotals:

- §21.2: **58**
- §21.3: **116**
- §21.4: **55**
- §21.5: **48**
- **Total: 277**

§21.8 claims "121 conditions over 277 instances". **Reproduces exactly.** I
checked that no Instances cell carries a semicolon inside a parenthetical that
is not a separator (L2's `C·N (which dominates the max disk ordinal (C−1)·N +
(N−1))` and L23's `leading fixed fields (name … C)` are the two nested-paren
cells; neither contains a semicolon). R1 is the only row whose *Detected* cell
carries a semicolon, and that column is not counted.

### 2.3 Instance cells against §21.1's two stated axes

I spot-checked every cell whose count could turn on the axes, and they hold
without exception:

- Two-direction rows (a *differs from* / *does not equal*): F17 (2), F23 (2),
  L12 (2), L21 (4 = 2 layouts × 2), L22 (4), L30 (2), T3 (6 = 3 layouts × 2),
  T14 (6), T22 (6). All enumerate both directions.
- One-direction rows (an *exceeds* / *below* / *larger than*): F2 (6 fields, no
  direction split), F3 (2 containers), F5 (2 fields), F9, F10, F16, T9, T12,
  T21 (3 layouts, no direction), L44 (3 layouts, no direction). All one
  direction.
- No-ordering comparisons: F6 (2 fields, byte pattern against a constant), F8,
  F14, F20, L37, L38, T1 — one instance each per field, no direction.
- Nonzero value tests: T6 (`crc ≠ 0`), L20 (`A ≠ 0` and `S ≠ 0`), L27, L28 —
  one instance each.
- Single predicate over several fields: F32 (a sum), F25 (two flag bits), T12 —
  one instance each. Correct per "the fields it reads are not instances,
  because no two files could differ."
- Family without a shape change stated as one instance: F19 (`flags bits
  0-15`), F26 (`flags bits 2-15`), T24 (`any codec`). Family with materially
  different shapes enumerated: T15, T25, L33/L34 (which split the reserved
  range because §11.4 and §12.2 themselves name two sub-ranges), L31/L43/L45
  (which do not, because §15.1/§17.2/§17.3 name one).

The file-scope/layer-scope mirror pairs also line up on containers, which is a
good independent check that nobody hand-tuned the numbers: F30(2)/L15(4),
F31(1)/L16(2), F32(1)/L17(2), F25(1)/L46(2), F26(1)/L47(2), F28(2)/L49(4),
F29(3)/L14(3), F23(2)/L12(2), F21(1)/L10(1), F22(1)/L11(1). Each layer row
carries exactly the file row's count times its extra container, or the same
count where there is only one container.

**Verdict on the counting: every total in §21 and §21.8 reproduces.** I found
no arithmetic finding.

### 2.4 The document's own constants (sanity, since I was computing anyway)

Ran CRC-32C (poly 0x1EDC6F41 reflected, init/final 0xFFFFFFFF):

- `CRC32C("123456789")` = `0xE3069283` — §4.5 ✓
- `CRC32C(<empty>)` = `0x00000000` — §4.5 ✓
- Appendix A's trailer bytes [0,60) → `0xE00938D2` — Appendix A ✓
- 4 sentinel entries (80 bytes `FF×16 00×4` ×4) → `0x80A34955` — §7.4 example ✓
- CRC of that 4-byte array → `0xC4EE982E` — §7.4 example ✓
- 2¹⁶ sentinel entries → `0xEECB3BB2` — §15.4 / Appendix B ✓

§15.4's worked example also reproduces by hand: entry_count 1,000,000 → 16
segments (15 full + 16,960), CRC array 64 bytes, region 20,000,064 bytes, entry
999,999 at segment-relative 339,180, CRC array at [20,000,000, 20,000,064),
segment 15 at [19,660,800, 20,000,000), one full segment 1,310,720 = 1.25 MiB.
§21.9's Note reproduces too: 2³² entries → 2¹⁶ segments × 4 bytes = 256 KiB;
2³⁶ → 4 MiB.

---

## 3. Row-versus-rule agreement, row by row

I walked all 121 rows against their cited requirement. What follows is the
audit trail, condensed to what I actually had to decide.

### 3.1 §21.2 (file scope)

F1 restates [R-ENC-02], and adds two exemption clauses drawn from the
parenthetical rules ([R-CNT-04] residency for the front-block instance,
[R-CNT-06] for the trailer instance). I worried this was a row asserting an
exemption its **governing** rule does not grant — [R-ENC-02] says flatly "a
reader encountering what appears to be a byte-swapped signature (§6) MUST treat
the file as invalid" — but [R-ENC-02] is self-limiting on *encountering*, so a
reader that never fetches [0,16) never encounters it. No divergence. Note that
F6 carries "a verifier holds no such exemption (§2.3)" and F1 does not; §2.3's
[R-CNF-11] supplies it independently and Appendix H names "(F1, F6)" together,
so nothing is lost.

F2's six instances are exactly the file-scope u64 fields [R-ENC-03] reaches.
`file_id` is correctly absent: it is a u64 but not an offset, length, extent or
count, and [R-ENC-03]'s domain names only those four kinds. F12 registers
`file_id = 0` under [R-CNT-06] separately, which is right.

F3's instances are both expressly designated sums (§6.2 for
`dir_offset + dir_length`, §7.2 for `extent_offset + extent_length`), satisfying
[R-ENC-04]'s "A designation is express" test. I checked this because [R-ENC-04]
disclaims non-designated expressions.

F9/F10/F11/F12/F13/F14/F15/F16/F17 are exactly [R-CNT-06]'s field gates.
Counting the register rows whose Governing rule cell is `[R-CNT-06]` gives F8,
F9, F10, F11, F12, F13, F14, F15, F16, F17 = **ten**, which independently
confirms §2.3's claim that "[R-CNT-06] states ten, of which the trailer magic
and the trailer CRC assert invariants [R-CNT-24] fixes and the other eight do
not." The version gate and flag gates are delegated to [R-CNT-07]/[R-CNT-08]
(F18, F19) and correctly not counted among the ten. `generation > 2⁶³−1` is
F2's, governed by [R-ENC-03], and also correctly not counted.

The §21.2 preamble's foreign-major derivation checks out against [R-CNT-24]'s
four fixed invariants (trailer magic at F−64; version_major/minor at F−56; a
CRC-32C at F−4 over [F−64, F−4); the front block constant): the reaching rows
are F8, F14, F6 and both F1 instances, and no other row asserts a fixed
invariant. F13 asserts 64-alignment of F, which [R-CNT-24] does not fix. F17
asserts a cross-check on a field inside the 48 redefinable bytes. F19's flags
lie there too. §2.3's Note's three worked cases (F14 reaches, F5 does not, F15
does not despite citing R-CNT-24 in its parenthetical) are all correct — F15's
Governing rule cell does read `[R-CNT-06]` (R-CNT-24), so the Note's
description of it is accurate.

I also checked that no row is *mixed* on reach (some instances reaching, some
not), since [R-CNF-13] makes reach per **condition** and not per instance. No
row is mixed. F1's two instances both reach; F6's two both reach; F2's six all
fail to reach; F17's two both fail. So the per-condition granularity is safe.

F21 gave me my first real pause, twice — see §5 findings.

F33's parenthetical claim that "a claimant reaching the front signature block or
the live trailer is instead caught by the bounds rows F9/F10, F30/F31/F32,
L15/L16/L17 and T8/T9" is complete against [R-CNT-02]'s claimant classes: the
directory (F9/F10), non-layer top-level record extents (F30–F32), layer record
and sub-record extents (L15–L17), stored-tile extents (T8/T9). And the
half-zero carve-out is right: a slot of (0, N) with N nonzero has offset 0,
which is not in 1–15, so F31/L16 genuinely do not reach it and F30/L15 do.

F35/F36 and their scope ([R-CNT-15]'s reader MU-gate versus the verifier's
reserved-range check) match. F27/F28 and L48/L49 match [R-MTA-05] and
[R-CNT-22], including that both rules leave reader behavior unchanged, which is
why the detector is the verifier.

### 3.2 §21.3 (layer scope)

L1's eight instances are the layer-scope u64 offset/length/extent/count fields.
A and A_slab are correctly **absent**: they are alignments, not offsets,
lengths, extents or counts, so [R-ENC-03]'s domain does not reach them, and they
carry their own bounds through L39 and L29 (which is also why L39's third
instance "A above 2^62" is reachable at all — A may legally be a u64 value
above 2⁶³−1 without tripping L1). S is present because [R-ENC-03] names slab
run lengths expressly. `inline_length` is a u32 length and can never exceed the
domain, so its absence is right. Tile-index entry offsets and lengths are
tile-scope and belong to T11, per §15.1's owning-scope statement and §15.3's
"notwithstanding the general owning-scope mapping" clause.

L2's nine instances: I checked every quantity [R-ENC-04] designates at layer
scope and each is either listed or strictly dominated by one that is.
[R-GEO-03] designates N, P, the addressed-tile count (N or C·N), and N·P — all
four present. [R-SER-02] designates P·Q, P·Bᶜ, k·Bᶜ, (k div C)·Q + F_{k mod C},
Q and Fᶜ; the last four are dominated (Q ≤ 65535·8 cannot overflow; the value
offsets are below the decoded size). [R-SER-07] designates every decoded size
and V — the row's parenthetical "P·Q (which dominates V = P·C)" is arithmetically
right since Q = ΣBᵢ ≥ C. [R-CNT-17] designates the index-length formula —
present. [R-GEO-06]'s ordinals are dominated by C·N, N and P, and the row says
so ("C·N (which dominates the max disk ordinal (C−1)·N + (N−1))" — correct,
that expression is C·N − 1). ⌈P/8⌉ ≤ P. Nothing missing.

I confirmed each of the five derived instances is separately reachable, i.e.
they are genuinely distinguishable files: C·N can overflow at N = 2⁴⁸,
C = 2¹⁶ while N·P = 2⁴⁸ stays in domain (P = 1); P·Q can overflow at P = 2⁵⁰,
Q = 2¹⁴ while P alone stays in domain. Good.

L3/L5/L6 are detected at **open** while L4/L7/L8 are at **layer access**. That
is not an inconsistency: §19.1 step 4 parses and checks each layer record's name
"per §4.6" at the open (which covers [R-ENC-11] as well as [R-ENC-12], since
§4.6 is cited rather than the identifier alone), and §19.3 defines first access
as "the first operation using any of the layer's declarations **other than its
name**". The Detected column tracks that split precisely.

L15/L16/L17 sit at layer access while F30/F31/F32 sit at open. Also correct:
§19.1 step 4 checks "the extent-slot validity rules for **non-layer** top-level
records", and §19.3 places [R-CNT-13] for the layer record and its sub-records.

L21/L22 restate [R-CNT-17] faithfully, including the entry_count = 0 case
(formula yields 0, §7.4 requires slot (0,0)).

L26's Governing rule cell is `[R-CNT-18]` (§7.3 registry table) and L31's is
`[R-CNT-23]` (§15.1) — parentheticals holding a **section** where §21.1 says
"any identifiers following it in parentheses are the further rules the condition
reads". A two-cell departure from a stated convention; I judged this editorial
and did not raise it as a finding.

L41's three instances (gap; overlap; out-of-ordinal placement) are alternatives
the row's own text states, which §21.1 licenses alongside the two-direction
axis; three distinguishable files exist.

L44's three layout-formula instances and its "in a planar layer the largest
channel plane governs" gloss match [R-COD-07] word for word.

### 3.3 §21.4 (tile scope)

The §15.3 table maps one-to-one onto T1 and T6–T12, with the last structural
row splitting into T12 (sum overflows) and T9 (sum > F−64). §15.3's claim "Six
rows are marked *structural*" is exactly right — I counted them.

T7 and T11 are disjoint only because T11 says "the value being distinct from the
all-ones sentinel". Without that clause every T7 file would also be a T11 file.
The document caught that; I mention it because it is the same hazard I do report
below for F21/F22, and its being handled here is what convinces me the F21/F22
case is an oversight rather than a convention.

T2's "the same byte at a padding position is T4's, the two rows together
covering [R-SER-08]" is sound: a padding position's bool byte must be the fill
byte, which [R-TYP-07] constrains to 0x00/0x01, so any other byte there fails
T4 under [R-SER-05].

T4's four instances and T5's one exactly partition [R-SER-05]'s obligations
(fill bytes for a numeric channel in each layout; the fill byte for an
interleaved bool; the fill bit in a packed plane; and separately every pad bit).

T26 says the check that detects a wrong stride is "T2's or T4's" and does not
mention T5. I spent some time trying to falsify this with a packed planar bool
plane whose *pad bits* alone are corrupted by a wrong stride, and it cannot
happen: for the shuffle at stride s over L = s·n bytes, the byte at filtered
offset i·n + j comes from j·s + i, and setting i = s−1, j = n−1 gives
sn − 1 = L − 1 on both sides — **the last byte is a fixed point of the shuffle
at every stride**. Pad bits live only in the last byte, so no stride can move
them. T26's claim survives, and so does §21.7's restatement of it.

T13's two instances are the *detectable* cases of [R-COD-02]; an undisclosed
zstd dictionary is correctly excluded (it is [R-COD-06]'s expressly
undetectable class), and a disclosed one is T19.

T14 correctly carries [R-COD-04]'s "**non-sentinel**" qualifier.

### 3.4 §21.5 (ignored records)

I derived the ignore-record violation set from [R-CNT-25]'s own enumeration
("a failed extent CRC, an unimplemented or invalid encoding, a decode failure,
or content violating the document's own rules") plus [R-MTA-04]'s four
restrictions, and mapped it:

- failed extent CRC → R2
- invalid/unassigned encoding: 0 and reserved → R1; experimental → §21.6, not a
  violation (correct, [R-CNF-02] plus §10.3's conduct/bytes split)
- decode failure → R3
- encoding-2 frame constraints → R4
- object-unmarked / not-JSON / BOM → R7
- non-finite numbers → R8
- duplicate keys → R9
- ill-formed UTF-8 and unpaired-surrogate escapes → R5
- empty key / C0 in a key → R6
- key over 255 bytes → R10

Ten, matching the header. Nothing in [R-MTA-04] or [R-CNT-25] is unregistered.
[R-MTA-05]'s member ordering is correctly *not* here — it does not make the
document unreadable, so it takes the record's containing scope and lands as F27
/ L48, which §21.6's closing paragraph explains at length.

R4's sixteen instances derive exactly: eight alternatives (magic, skippable
frame, second frame, dictionary ID, checksum flag, trailing bytes, content-size
larger, content-size smaller) × two containers. §18.2 expressly excludes the two
witness-less carry-overs (undisclosed dictionary use; the bar on sizing a
buffer) and R4 registers neither — checked.

R1 is disjoint from R3 by construction ("under its declared **assigned**
encoding"). R4 is not — see finding `register-02`.

---

## 4. Completeness sweeps

### 4.1 Outward (a violation the register omits)

I grepped every occurrence of "validity error", "MUST treat", "is a violation",
"makes the file nonconforming", "is invalid", "not a conforming file", "MUST NOT
emit", "Writers MUST", "MUST write", "MUST place", and walked each hit to a row
or to an express account of why there is none. Everything landed:

- [R-ENC-01]'s little-endianness carries no MUST of its own (the MUST NOT is
  [R-ENC-02]'s), so there is no unregistered condition there.
- [R-ENC-06] (fixed field widths) → §21.7, "not a state a file can be in".
- [R-ENC-07] → F16, F22/L11, F23/L12, L22, and the framing rows.
- [R-CNT-02]'s partition → the §5.2 Note explains that only disjointness is
  testable, and F33/F7/L18 register it.
- [R-CNT-18]'s nesting prohibition → §7.4's closing Note and §21.7; the one
  detectable case (a layer record as a sub-record) is L26.
- [R-SLB-04]'s stale slab declaration → §16.2's Note; detected as L41/L42.
- [R-LIF-04]'s truncate-or-overwrite → §9.5's Note; observable state is F8/F14/F17.
- [R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01], [R-CNT-13]'s embedded-offset
  bar, §20.3 step 4, §20.5's four trailer obligations → §21.7, by class.
- [R-MTA-06]/[R-MTA-07]/[R-EXT-03]'s experimental prohibition → conduct rules
  under [R-CNF-02]; §21.6 records the non-violations.
- [R-CNT-08]: a set **ignore**-lane bit is expressly not a violation (§21.6); a
  set **incompat**-lane bit is one, and F19 registers it. §10.1's four vehicles
  list only ignore-lane bits, so within major 1 no incompat bit is ever legitimate.
- All four checksums in §8.1's map that exist are registered: trailer F14,
  directory F20, index L37/L38, stored tile T1, user-metadata extent R2, front
  block F6 by equality, unassigned-type extent by nothing (expressly).
- Value 0 in each of §10.2's eight spaces: F24/L13, L36, L33, L34, L43, L45,
  L31, R1. All eight present.

I found no unregistered detectable file-conformance violation.

### 4.2 Inward (a row registering a non-violation)

I checked the rows whose violation status is least obvious — F7, F15, F19, F25,
F26, F27, F28, F33, F36, L46–L49, T2, T4, T5, T13, T26 — and every one traces to
a MUST or an express "is a violation" in its governing rule. §21.6's two
promoted entries (unsorted members; a registered type's stored flag bits) are
accounted for in §21.6's own closing paragraph.

### 4.3 Every cross-reference to a row

Grepped every `F<n>`, `L<n>`, `T<n>`, `R<n>` token in the document and resolved
each against the row it names:

| Where | Rows cited | Resolves? |
|---|---|---|
| §2.3 Note | F14, F5, F15 | yes — F15's cell does cite R-CNT-24 in parentheses |
| §5.2 [R-CNT-21] | L18, L40–L42 | yes — all four are verifier/reject-layer rows the walk itself establishes |
| §9.6 [R-LIF-06] | F8, F14, F17 | yes — magic, trailer CRC, length cross-check |
| §17.2 Note | T24 | yes |
| §18.2 [R-MTA-09] | R3, R4 | yes (but see `register-02`) |
| §20.3 step 4 | L44 | yes |
| §20.5 [R-WRT-06] | F36, L25, L31, L33, L34, L36, L43, L45, R1 | yes — "one row for each of the other seven spaces §10.2 tabulates" is exactly right: layout L36, linearization L33, sample type L34, codec L43, filter L45, index encoding L31, metadata encoding R1 |
| §21.1 | F1/F6/F8, F35/F36, L24/L25, T24, T15/T25, F27/L48 | resolve; the specialization list is incomplete — `register-01` |
| §21.2 preamble | F8, F14, F6, F1, F18 | yes |
| §21.6 | F36, L25, F18, F35, L24 | yes |
| §21.7 | T2, T4, T5, T3, T14, T15, T17, T23, T25, T26 | yes |
| Appendix H | F1, F6, F7, F36, L25, R1 | yes |

No citation points at the wrong row. §20.5's seven-space enumeration is the one
I expected to break and it does not.

### 4.4 Outcome vocabulary

§2.4 defines four reader outcomes and one updater obligation. All four reader
outcomes are reachable, one per register subsection. `preserve-verbatim` occurs
only in §2.4 and points at §20.4's table "its MU = 1 and MU = 0 / PE = 1 rows" —
both rows exist, and the MU = 0 / PE = 0 row is correctly excluded because
retention is optional there. No row carries an outcome outside the vocabulary.
The mechanical detector/detected check passed for all 121 rows: every
`verifier` row is `certification`, every `reader` row names one of §19.2's four
tiers (R1's compound cell being the only two-tier cell, correctly so — a
top-level record's encoding byte is resident at open, a sub-record's at layer
access).

Every Governing-rule identifier cited by any row (67 distinct) exists in the
document. Nothing dangles.

### 4.5 Limits, both directions

**Elsewhere → §21.9.** §21.9 expressly disclaims inventory status ("The hard
limits it restates are a finding aid rather than an inventory"), so the limits
it omits — the user-metadata `extent_length ≥ 5`, F ≡ 0 mod 64, the geometry
floors d ≥ 1 / C ≥ 1 / Tᵢ ≥ 1, `file_id ≠ 0`, the 20-byte entry and 2¹⁶-entry
segment — are not defects. Each is normative where its structure is defined,
which is what §21.9 promises.

**§21.9 → defining sections.** I checked all nine hard limits against their
defining sections: names ≤ 255 (§4.6); user-metadata key ≤ 255 (§18.2 folding
§4.6); rank ≤ 255 and C ≤ 65,535 (§7.4's u8/u16); codec-4 decoded tile size
≤ 0x7E000000 ([R-COD-07] — "exceeds" means the cap is inclusive, and §21.9 says
"at most", consistent); every offset/length/extent/count ≤ 2⁶³−1 ([R-ENC-03]);
A a power of two in 512…2⁶² and A_slab a power of two in 1…2⁶² (§7.4, §16.1,
§16.2); S in 1…2⁶³−1 (§7.4's table via [R-CNT-23] — §16.2 itself states only
S ≥ 1, and §21.9 cites [R-CNT-23] alongside §16.2, which supplies the ceiling);
dir_length ≥ 4 at dir_offset ≥ 16 (§6.2); 128-byte file floor (§5.1). All nine
agree.

The eight minimum guarantees agree with Appendix B's restatement row for row,
and with every downstream citation: §18.2's two "no smaller than §21.9's
guarantee" clauses, §17.2's "§21.9's 8 MiB `Window_Size` guarantee", §2.3's
[R-CNF-03], §2.5's [R-CNF-10], §24's [R-VEC-03]. The §21.9 Note's arithmetic
reproduces (256 KiB at 2³², 4 MiB at 2³⁶; ~12.5 MiB for 65,536 layers at ~200
bytes a record; 256 MiB an order above §11.3's 1–16 MiB working range).

The per-instance paragraph survives the degenerate cases I could build: a layer
addressing no tile (any Eᵢ = 0) has no tile whose decoded size the table bounds
— stated, and consistent with [R-COD-07]'s Note; a file with no user-metadata
document and no zstd frame exceeds neither of the other two per-instance rows —
stated; and the first five rows range over declarations every file and layer
carries, including entry_count = 0.

I considered raising §2.5's "Readers MAY enforce resource limits, but MUST
accept any conforming file within the minimum guarantees" against §21.9's
[R-ERR-04], which carves out "the two capability refusals §21.6 names, a foreign
format major and an unimplemented MU = 1 type", where §2.5 does not. Read
literally as a standalone MUST, §2.5 would oblige a reader to accept a
conforming file carrying an experimental-range top-level MU = 1 record that
[R-CNT-15] obliges it to reject. I decided this is an over-flag: the "but"
clause plainly bounds the preceding permission to enforce *resource* limits,
and [R-CNF-03], §21.6's closing paragraph and [R-ERR-04] all settle it the same
way. Recording the reasoning rather than the finding.

**No limits finding.**

---

## 5. Findings

### register-01 — AMBIGUITY — §21.1's specialization list omits F21 ⊂ F22 and L10 ⊂ L11

§21.1 quotes:

> Some rows are strict specializations of others — F1 of F6 and of F8, F35 of
> F36, L24 of L25 — and a file exhibiting a specialization is recorded against
> the narrower row, whose detector and detection point are the ones that apply.

The register carries at least two more strict containments that this list does
not name.

F21: "A top-level user-metadata record (type 0x0002) carries extent slot (0, 0)".
F22: "A top-level user-metadata record's extent_length is less than 5, too short
to hold both a document and the terminal CRC-32C of its final 4 bytes."

A slot of (0, 0) has extent_length = 0, and 0 is less than 5. **Every file
exhibiting F21 exhibits F22.** L10 and L11 are the same pair at layer scope,
verbatim.

The governing rule does not separate them either. §7.1 ([R-CNT-25]) reads:

> An extent of (0, 0) on a user-metadata record, or one whose extent_length is
> less than 5 — too short to hold both a document and the terminal CRC-32C §8.1
> places in its final 4 bytes — is a validity error at its containing scope.

Two readings are available. (a) "one whose extent_length is less than 5" ranges
over every extent slot, so the two disjuncts overlap and F21 ⊂ F22. (b) The "or"
is meant exclusively — the second disjunct silently means a *nonzero* slot whose
length is under 5 — so the rows are disjoint. Nothing in either the rule or the
rows chooses. I pick (a), because the text says "less than 5" without
qualification, because §21.2's neighbouring rows do carry that qualifier where
it is meant (F31: "A non-layer top-level record's **nonzero** extent slot…"),
and because the document demonstrably knows how to write the exclusion when it
wants it: T11 says "the value being distinct from the all-ones sentinel"
precisely to keep T7 and T11 apart, and L22 says "**including** slot (0,0) with
entry_count > 0" precisely to fold a special case *in*.

Under reading (a) the containment is real and §21.1's list is incomplete. That
matters because the specialization clause is the register's only mechanism for
resolving one condition contained in another, and §21.8/[R-VEC-03] require a
vector per row: a vector built for F21 unavoidably exercises F22, so the corpus
cannot satisfy [R-VEC-02]'s "a vector is constructed so that one row is the one
it exercises" without falling back on its "where a condition cannot be isolated"
escape — an escape whose only worked example is §6.2's jointly-validated field
gates. Under reading (b) the list is complete but F22's and L11's wording is
wrong and needs the missing qualifier.

Related but weaker, and recorded here rather than as a separate finding: F30 and
F31 are not disjoint either (a slot of (5, 0) has exactly one half zero *and* an
extent_offset in 1–15), nor are L15 and L16. Those are partial overlaps rather
than containments, so §21.1's specialization clause would not resolve them even
if it named them.

Not byte-level: F21/F22 and L10/L11 share outcome, detector and detection point,
so no reader or verifier verdict moves, and a file exhibiting either is
nonconforming under both readings, so [R-CNF-05] bars every conforming writer
from emitting it either way. The cost falls on the corpus and on a verifier's
diagnostic.

### register-02 — AMBIGUITY — R3 and R4 both register an encoding-2 document with no frame magic, and R4's stated ground for the split is false for that instance

R4's Condition cell says:

> unlike R3, a constraint of this row is broken by what the frame declares
> rather than by whether the bytes decode, so a reader that only tries decoding
> establishes none of them

R4's own first instance is "missing frame magic, top-level extent". A
user-metadata extent under encoding 2 whose bytes do not begin with
`28 B5 2F FD` is not a Zstandard frame at all: every conforming zstd decoder
fails on it. So for that instance nothing "the frame declares" is broken — there
is no frame — and a reader that only tries decoding does establish a failure.

That file also satisfies R3 verbatim: "A user-metadata document's stored bytes
fail to decode under its declared assigned encoding". R3 carves out only
unassigned encodings (which it does explicitly, and correctly, for experimental,
0 and reserved values); it does not carve out R4's frame constraints.

§18.2 supplies a separating criterion, but only for one of R4's eight
alternatives:

> A mismatch is one of the frame constraints R4 registers, not a failure to
> decode under R3: the bytes decode, and what is wrong is what the header said
> about them.

"The bytes decode" is true of the content-size mismatch, of the
content-checksum flag, and (for a tolerant decoder) of a second or skippable
frame. It is false of a missing frame magic and of a nonzero dictionary ID,
both of which R4 enumerates as instances and both of which make a decoder fail.

Two readings. (a) "a reader that only tries decoding establishes none of them"
means *detects none of these violations* — then it is falsified by R4's own
first instance, and a missing magic is R3, not R4. (b) It means *cannot
establish any of these constraints as satisfied* — true, and then the missing
magic is R4 and R3 must be read as excluding whatever R4 covers, which R3's text
does not say. I pick (b), because §18.2's stated purpose for routing the
condition to R4 is to keep it "checkable from the bytes alone rather than
turning on a decoder's tolerance", and reading (a) reintroduces exactly the
decoder-dependence the section is trying to eliminate. But R3's text has to be
read against its own words to get there.

An implementer who takes reading (a) writes a verifier that reports R3 for a
magic-less extent; one who takes (b) reports R4. Both find the file
nonconforming and both take ignore-record for the record, so no verdict and no
byte moves; the divergence is in which row a corpus vector and a verifier's
report name — and §24 makes that pair (row plus governing identifier) the thing
a manifest records.

Not byte-level.

### register-03 — OBSERVATION — F21's gloss "placing its document inline" describes a state the format makes unrepresentable

F21 reads:

> A top-level user-metadata record (type 0x0002) carries extent slot (0, 0),
> placing its document inline

The trailing clause diverges from every rule it depends on. §7.1 says "Each
user-metadata record carries its document in its extent — **never inline**".
[R-MTA-03] says "A user-metadata record's inline payload is exactly one byte"
and that "A record whose inline_length is not 1 is a validity error". So a
record with slot (0, 0) and a conforming inline payload has its document
nowhere at all — it cannot place it inline, and a record that tried to would
fail F23 (inline_length ≠ 1), not F21. §21.1 makes the rule govern, so nothing
turns on it for a verdict; but the register is where an implementer looks up
what a row means, and this row's causal gloss names a condition no file can
exhibit. Note that L10, the same condition at layer scope, carries no such
gloss — "A user-metadata sub-record of a layer record carries extent slot
(0, 0)" — which is the wording F21 should have.

Not byte-level: a purely descriptive clause in a row whose governing rule is
unambiguous.

### register-04 — OBSERVATION — §21.4's outcome header drops [R-CNF-09]'s own qualifier, and four of its own rows contradict the result

§21.4's header:

> Outcome: reject-tile — that tile's read reports failure, and never returns
> fill in place of data (`[R-CNF-09]`). 26 conditions.

[R-CNF-09], the rule it cites, is qualified:

> A reader MUST NOT return data as valid from a scope this specification rejects
> **and whose rejection this reader is obliged to detect** (`[R-RDR-02]`); in
> particular, a read of a rejected tile MUST NOT silently return fill.

Four of §21.4's twenty-six rows — T2, T4, T5 and T26 — carry Detector
*verifier*, so no reader is obliged to detect them, and [R-CNF-09] therefore
does not reach a reader that meets one. For T2 the governing rule goes further
and tells such a reader what to do instead:

> A reader that neither detects the violation nor rejects the tile, and returns
> the value, MUST report 0x00 as false and every other byte as true.
> (`[R-SER-08]`)

Read as a universal over its own table, §21.4's header would forbid exactly the
behavior [R-SER-08] mandates. §21.1 rescues it — "For a row whose Detector is
*verifier*, the outcome names the scope at which the damage is recorded, not an
obligation on any reader: the governing rule states what a reader does" — so the
resolution is available, but it lives a subsection away and requires the reader
to notice that [R-CNF-09]'s qualifier was dropped in the restatement. §21.2's
and §21.3's headers make the same compression (F7, F25–F28, F33, F36 and L18,
L25, L40–L42, L46–L49 are all verifier rows), but only §21.4's cites a rule
whose own text carries the missing qualifier.

Not byte-level: the disputed file is nonconforming under every reading, so
[R-CNF-05] bars every conforming writer from emitting it and the emittable set
does not move; and [R-CNF-12] independently licenses any reader to reject any
nonconforming file, so both behaviors were already available.

---

## 6. What I could not determine

- Whether §21.1's specialization list is meant as exhaustive. "Some rows are
  strict specializations of others — [three pairs] —" reads as an enumeration
  but does not say "these are the only ones". `register-01` is stated so that it
  is a finding either way (an incomplete list, or two rows that need a
  qualifier).
- Whether "a reader that only tries decoding establishes none of them" in R4 is
  about detection or about establishing satisfaction. `register-02` gives both.
- §21.7's parenthetical witness list for a codec change "(T15, T17, T23, T25)"
  omits T14 (named separately), T16, T18–T22 and T24, all of which can witness a
  codec change. I did not raise it because the claim it supports is explicitly
  "*sometimes* witnessed", which an incomplete list of witnesses cannot falsify.
- §21.7's closing clause on [R-ENC-06] — "a structure written at any other
  [width] yields different values at them, caught by the rows for the fields
  that hold them" — is an unproven universal. I tried to falsify it by
  constructing a layer record whose mis-width parse yields a wholly valid but
  different record (u16 rank, u16 name prefix, u16 fill prefix) and every attempt
  tripped L23, L31, L32, L36 or L7. I could not falsify it and could not prove
  it, so I did not report it; it is decidable but expensive.
- §21.1's "which is why §14.2 calls it the sole resolved byte in this format" —
  §14.2 makes no such statement in normative text; its Note says "Only the
  in-tile byte, whose detector is the verifier, could be met by a reader with no
  obligation to act on it", and the "one case where a reader resolves a byte to
  a value" formulation is §12.3's [R-TYP-04]. I judged the attribution close
  enough to §14.2's Note not to raise it.

## 7. Summary

Four findings, none byte-level. The register's completeness holds in both
directions as far as I could push it; every row's outcome, scope, detector and
detection point agrees with its governing rule; every cross-reference to a row
from outside §21 resolves to a row that says what the citing text claims; every
stated total reproduces exactly (121 conditions, 277 instances, 36/49/26/10,
and the ten conditions [R-CNT-06] states); the limit material agrees with every
defining section in both directions; and the document's own CRC constants all
check. What is left is a specialization list that misses two containments, one
row pair whose separating rationale does not cover its own first instance, one
row gloss that describes an unrepresentable state, and one subsection header
that drops a qualifier its cited rule carries.
