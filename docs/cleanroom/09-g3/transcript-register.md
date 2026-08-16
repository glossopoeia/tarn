# Round 9 — Register hunter — verbatim working transcript

Charter: §21, the error-handling register, audited against the rules it restates
and against itself.

Access discipline: I read exactly one file, `spec/tarn.md`. I ran `grep`/`sed`
and Python against that file and against nothing else. I did not open `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or
the web. The only other artifact I touched is this transcript, which I wrote and
never read back. Everything below was derived from the document's own text plus
arithmetic I ran locally.

---

## 1. First pass: the shape of §21, and the counting

I read §21 end to end before anything else, because §21.1 claims to govern the
rest of the section. Then I mechanically extracted the four register tables
(§21.2 F1–F38, §21.3 L1–L50, §21.4 T1–T27, §21.5 R1–R10) with a Python script
that splits each row on `|` and counts the Instances cell by semicolons, with a
cell reading `—` counted as one — which is exactly the rule §21.1 states:

> Instances within a cell are separated by semicolons, and a cell reading — is
> one instance; the count is therefore mechanical once the cell is written.

Result:

| subsection | rows | header claims | instances |
|---|---|---|---|
| §21.2 | 38 | "38 conditions" | 60 |
| §21.3 | 50 | "50 conditions" | 103 |
| §21.4 | 27 | "27 conditions" | 46 |
| §21.5 | 10 | "10 conditions" | 44 |
| total | **125** | — | **253** |

§21.8 says "125 conditions over 253 instances". Both totals reproduce exactly
from the cells as written. Row numbering is dense and gap-free in all four
tables (F1…F38, L1…L50, T1…T27, R1…R10 — no skips, no duplicates).

So the arithmetic *from the cells* is clean. The question the charter really
asks is whether the cells themselves were written under §21.1's definition of an
instance. That turned out to be where the counting problem is (finding
register-03 below), not in the addition.

Per-subsection instance sums, for anyone re-deriving: F 5+2+6+2+2+1+2+2+1+1+1+1+
1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+2+3+2+1+1+5+1+1+1 = 60. L 8+9+1+1+2+1+1+2+2+2+
1+1+1+1+3+4+2+2+3+1+1+1+3+4+1+1+1+1+1+3+1+3+3+4+4+1+2+1+1+3+1+1+1+3+1+3+1+1+1+2
= 103. T 1+1+6+4+1+1+2+1+1+1+2+1+2+1+2+1+1+4+1+1+1+1+1+1+3+3+1 = 46. R 4+2+2+12+
8+4+6+2+2+2 = 44.

## 2. Detector / detection-point vocabulary

§21.1 fixes the vocabulary:

> Detection points name §19.2's reader tiers — open, layer access, tile use,
> extent use — or *certification* for the rows a verifier detects

Mechanical grouping of (Detector, Detected) pairs over all 125 rows:

- reader / open — 34 rows
- reader / layer access — 36
- reader / tile use — 25
- reader / extent use — 9
- reader / "open (top-level); layer access (sub-record)" — 1 (R1, a compound
  matching its two containers)
- verifier / certification — 20

No row uses a value outside the vocabulary, no reader row is due at
certification, and no verifier row is due at a reader tier. All four reader
tiers are reached, and all four outcome classes of §2.4 (reject-file,
reject-layer, reject-tile, ignore-record) are reached by a subsection. The fifth
value of §2.4's table, **preserve-verbatim**, is not a reader outcome — §2.4
says so itself ("names an updater obligation, orthogonal to reader outcomes") —
and it is reachable through §20.4's table. So the outcome vocabulary checks out
in both directions: nothing undefined is used, nothing defined is unreachable.

The 20 verifier rows are F9, F27, F28, F29, F30, F35, F38; L19, L26, L41, L42,
L43, L47, L48, L49, L50; T2, T4, T5, T26. That list matters for finding
register-02.

## 3. Row-versus-rule sweep

I walked every row against the requirement in its Governing rule cell, reading
the cited rule in place. I will not narrate all 125; I record here the ones that
took work and the ones that failed.

**Clean and worth recording as checked:** the eleven-row §15.3 entry-state table
maps one-for-one onto T6/T7/T8/T9/T10/T11/T12 (structural rows), T1 (crc), and
L19/F35 + L41/L42/L43 (the verifier rows) — no §15.3 row is unregistered and no
T-row invents a state §15.3 does not classify. R-CNT-06's eleven trailer gates
map onto F10, F16, F20, F21, F19, F15, F11, F18, F12, F13, F14, F17 with F3
picking up generation > 2⁶³ − 1; no gate is missing. R-COD-06's six zstd
constraints map onto T17–T22 and, for metadata, onto R4's six alternatives.
R-MTA-04's four restrictions map onto R5–R10. §7.4's constraint table maps onto
L28–L37, L40, L44, L46. The width family R-ENC-06 is carefully split across
three scopes: F5 ("A fixed **file-scope** structure"), L3 ("A field of a
**layer-scope** structure"), T27 ("A **tile-index entry**").

**L23's arithmetic** I checked against §15.4's worked example: entry_count =
1,000,000 gives 1,000,000×20 + ⌈1,000,000/65,536⌉×4 = 20,000,000 + 16×4 =
20,000,064, which is the region size §15.4 states. Consistent.

**L2's dominance claims** I checked by hand: C·N dominates the maximum disk
ordinal (C−1)·N + (N−1) = C·N − 1, true; P·Q dominates V = P·C because
Q = ΣBᵢ ≥ C when every Bᵢ ≥ 1, true.

**Constants.** I implemented CRC-32C (reflected, poly 0x82F63B78, init/final
0xFFFFFFFF) locally and reproduced: CRC-32C("123456789") = 0xE3069283 (§4.5);
CRC-32C of zero bytes = 0x00000000 (§4.5, and Appendix A's directory);
Appendix A's trailer CRC over bytes [0,60) = 0xE00938D2, matching the stored
`D2 38 09 E0`; and the CRC of 65,536 concatenated sentinel entries
(`FF ×16 00 ×4`) = 0xEECB3BB2, the constant §15.4 and L39 name. All four
reproduce. That mattered for L39, whose text says the constant "never
substitutes for comparison" — the constant is right, and the row's caution about
partial segments matches R-IDX-05's "a partial segment's CRC MUST be computed".

**Where I had to guess, and did not have to in the end:** L4/L6/L7 carry
detection point *open* while sitting in the reject-layer table. I went to §19.1
step 4 ("build the layer table: each layer record's name, parsed and checked per
§4.6") and §19.3 (which assigns dimension- and channel-name rules to layer
access, not the layer record's own name). The split is deliberate and the rows
match it: layer-record name at open (L4, L6, L7, and F6 for duplicates),
dimension/channel names at layer access (L5, L8, L9, L10). No finding.

Likewise L38/L39 carry detection point *tile use* while sitting in the
reject-layer table; §19.2 states exactly this ("index-chain failures take layer
scope (`[R-IDX-04]`) although their detection point is tile use"). No finding.

## 4. Completeness sweep, register → rules

I extracted every `[R-XXX-NN]` identifier in the document (160, including the
`[R-ENC-100]` that §2.2 uses only as an example of a three-digit number) and
diffed against the 68 cited in the register's Governing rule column. I then read
each uncited requirement and asked whether it names a detectable
file-conformance violation.

The uncited set is dominated by: reader/writer/updater/verifier *behaviour*
rules (R-RDR-*, R-WRT-*, R-CNF-*, R-COD-01, R-COD-11, R-ENC-05, R-TYP-08/09,
R-MDL-*), SHOULD-level advice (R-CNT-03, R-CNT-09, R-CNT-26, R-ENC-14,
R-TYP-10), meta rules (R-EXT-01/04/05, R-VEC-*, R-ERR-*), security/privacy
narrative (R-SEC-*, R-PRV-*), defined non-violations already in §21.6 (R-GEO-02,
R-IDX-02, R-SER-09, R-MTA-06/07, R-CNT-08's ignore lane), history properties
§21.7 accounts for (R-LIF-01, R-LIF-03), and the withdrawn R-SER-04. None of
those needs a row, and §2.4 confirms the register carries MUST-level conditions
only ("Deviation from a SHOULD is not a violation for this purpose").

Two uncited rules needed real thought.

**R-SLB-04** (stale slab declaration carried forward). §16.2's note says it
"carries no register row of its own" because every file exhibiting it exhibits
an L42 or L43 condition. That is detection-by-another-row, not undetectability,
so it belongs in neither §21.7 nor the register. Correct as it stands.

**R-CNT-18's nesting-depth prohibition** ("a sub-record MUST NOT itself contain
records (nesting depth beyond two is a validity error at layer scope)"). §7.4's
note explains it has no reader-detectable witness in format major 1 and so no
register row. But §21.1 nominates §21.7 as "the account, by class, of what
fails" the detectability gate, and §21.7 accounts only for content-incorrectness
and for R-LIF-01, R-LIF-03, R-GEO-06, R-SER-01 and R-CNT-13's embedded-offsets
clause. The nesting prohibition — which unlike those is expressly stated as "a
validity error at layer scope", i.e. a file-conformance violation — appears in
neither list. That is finding register-05.

## 5. Completeness sweep, rules → register (the reverse direction)

I grepped rule *terms* rather than identifiers, as instructed, for conditions
that make a file nonconforming or that a verifier must detect. Everything I
found has a row, with one exception.

**Endianness.** R-ENC-01/R-ENC-02 are cited by exactly two rows, F1 and F2, both
in the reject-file table. The width analogue (R-ENC-06) is split across three
scopes; the endianness analogue is not. A dimension extent Eᵢ written
big-endian in a layer record is an R-ENC-01 violation and is detectable
(1024 stored big-endian reads as 0x0004000000000000 ≈ 1.13×10¹⁵, which passes
L1's domain gate but blows up ⌈Eᵢ/Tᵢ⌉ and so fails L22's entry_count
cross-check). There is no L- or T-scope endianness row, while F1's condition
text is scope-neutral ("A multi-byte field is stored big-endian rather than
little-endian") and sits under a reject-file header. Finding register-04.

I checked whether this forks readers: it does not, because §2.4's `[R-CNF-12]`
lets a reader reject any nonconforming file at file scope regardless of the
row's scope. That escape valve is general and is why scope disputes in this
register are not byte-level for readers. It is also why finding register-01 is
different in kind: there the dispute is whether the file is nonconforming *at
all*.

## 6. F1's version_major instance — the one that forks a verdict

F1's Instances cell reads:

> trailer version_major; dir_offset; dir_length; committed_file_length; generation

Four of those five are sound. Writing dir_offset = 16 big-endian yields
0x1000000000000000 ≈ 1.15×10¹⁸, which fails F12's dir_offset + dir_length ≤
F − 64 gate; dir_length, committed_file_length and generation behave the same
way against F18/F15/F19/F13. In each case the file is genuinely nonconforming
*under major 1* and the gate that fires is a major-1 gate.

version_major is not like that. I enumerated the cases:

- Intended value 1, written big-endian → the field reads 0x0100 = 256.
- Intended value 0, written big-endian → 0x0000, byte-identical to
  little-endian; nothing is detectable, and F20 covers version_major = 0 anyway.
- Intended value 256, written big-endian → reads 1, and the file is judged as a
  major-1 file with nothing detectable.

So the only constructible case is a trailer whose version_major field reads a
value that is not 1. And §2.3 says of exactly that:

> It is always conformance to a stated format major version. This document
> defines format major 1, and a file declaring another major is neither
> conforming nor nonconforming under it: a reader refuses such a file on
> capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding
> about its bytes.

and §21.6's closing paragraph says of exactly that:

> The first is **version_major naming a major this reader does not implement**:
> the reader rejects the file (`[R-CNT-07]`), but the file can be perfectly
> conforming under that major. […] Neither is a register row: the register
> enumerates file-conformance violations (§21.1), and a file this document
> declines to judge is not one. What is registered in each case is the
> neighbouring condition that *is* a violation — version_major = 0, permanently
> invalid in every format major version (F20, `[R-CNT-07]`)

§21.6 names F20 as the *only* registered condition on version_major. F1's
instance cell is a second one, and it registers precisely the case §21.6 says is
not a register row.

I checked whether §21.1's precedence clause disposes of this. It does not: that
clause resolves a row against *the rule it cites*, and F1 cites R-ENC-01, which
a big-endian writer genuinely does violate. The conflict is between the row and
§21.6/§2.3, which are not the cited rule. Nothing in §21 subordinates a row to
§21.6.

Worked verdict divergence, on a concrete file. Take Appendix A's 128-byte file
and change bytes [72, 74) from `01 00` to `00 01`, recomputing the trailer CRC
over [64, 124):

- Verifier A implements the register literally. F1 is a reader-detected,
  open-tier, reject-file row; the file exhibits its version_major instance; a
  violation of R-ENC-01 is established. §2.3: "An established violation takes
  priority: a verifier that has established any violation reports
  *nonconforming*." Verdict: **nonconforming**.
- Verifier B follows §2.3's enumeration and §21.6's closing paragraph. The file
  names a major it does not implement; that is listed verbatim in `[R-CNF-11]`
  as a *cannot establish* ground, and §21.6 says the refusal "records a reader's
  capability, not a defect in the bytes". Verdict: **cannot establish**.

Both refuse to certify; both readers reject-file. The divergence is the verdict
label, which this document makes a normative three-valued output and spends a
paragraph distinguishing, and it propagates into the corpus: §21.8 obliges one
vector per instance, so a conforming corpus must contain this file with a
recorded expectation of reject-file, while §6.3 tells readers the diagnostic for
an unimplemented major SHOULD be distinct from "corrupt". Finding register-01. I
flag it byte-level on the verdict half of the test and say plainly in the
rationale that the reader accept/reject half is common to both.

Removing the instance would also drop the register's instance total from 253 to
252.

## 7. The subsection headers versus §21.1's verifier paragraph

§21.3 and §21.4 gloss their outcome classes behaviourally:

> Outcome: reject-layer — the named layer is unusable, every other layer
> unaffected. 50 conditions.

> Outcome: reject-tile — that tile's read reports failure, and never returns
> fill in place of data (`[R-CNF-09]`). 27 conditions.

§21.1 says the opposite for the verifier rows those headers cover:

> For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader: the governing rule
> states what a reader does, and for several such rows it obliges the reader to
> serve the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`).

Thirteen rows are caught by this: L19, L41, L42, L43, L47, L48, L49, L50 (a
"layer" a reader is not merely permitted but in some cases obliged to serve —
`[R-CNT-22]`: "conforming readers nevertheless process the record under the
fixed semantics"; `[R-MTA-05]`: "readers process the document unchanged"), and
T2, T4, T5, T26 (a "tile" whose read need not report failure —
`[R-SER-08]`: "A reader that neither detects the violation nor rejects the tile,
and returns the value, MUST report 0x00 as false and every other byte as true").

The same assumption is baked into §24:

> a vector's expectation is therefore a pair: the scope no reader is permitted
> to serve, and the content a reader that serves anything at all owes.

For a T2 vector there is no "scope no reader is permitted to serve" — R-SER-08
says what a reader that serves it returns. Finding register-02.

I checked whether this forks bytes and concluded it does not: R-SER-08 licenses
returning the value, and `[R-CNF-12]` licenses rejecting the file, so both
implementations are conforming today and resolving the wording removes no
freedom. §21.1's verifier paragraph already decides which reading governs. I
also noticed in passing that that paragraph's parenthetical names `[R-SER-08]`
and `[R-CNT-22]` but not `[R-MTA-05]`, which is the third rule with rows
(F29, L49) that oblige the reader to serve the structure unchanged; too small to
report on its own, folded into register-02's detail.

§21.2's header ("Outcome: reject-file. 38 conditions.") carries no behavioural
gloss and is fine. §21.5's header does gloss, but every R-row is reader-detected
so the gloss is true there.

## 8. Recounting the instances against §21.1's definition

§21.1:

> An instance names a field the condition ranges over, a container it can occur
> in, one of several alternatives the condition text states, or any combination
> of the three — a condition applying to two alternatives in two containers has
> four.

and

> One instance is one *distinguishable* file: where a condition is a single
> predicate over several fields — a sum against a bound, a combination of two
> flag bits — the fields it reads are not instances, because no two files could
> differ.

I applied this to every row that names two containers. §21.3 has a family of
rows with identical grammar, "A layer record's or sub-record's X":

| row | condition shape | cell | count | expected |
|---|---|---|---|---|
| L16 | 2 containers × 2 alternatives (offset zero / length zero) | layer record extent_offset; layer record extent_length; sub-record extent_offset; sub-record extent_length | 4 | 4 ✓ |
| L17 | 2 containers × 1 | layer record extent slot; sub-record extent slot | 2 | 2 ✓ |
| L18 | 2 containers × 1 | layer record extent slot; sub-record extent slot | 2 | 2 ✓ |
| L47 | 2 containers × 1 (MU/PE is one predicate, §21.1's own example) | — | 1 | **2** |
| L48 | 2 containers × 1 (bits 2–15 is a family of one shape) | flags bits 2-15 | 1 | **2** |
| L50 | 2 containers × 2 alternatives (stored MU bit / stored PE bit) | layer record flags; sub-record flags | 2 | **4** |

L50 is the sharpest, because F30 restates the *same rule* (`[R-CNT-22]`) with
the *same condition shape* in one container and does enumerate the two bits:

> | F30 | A non-layer top-level record of a type §7.3 registers carries a stored
> MU or PE bit differing from the value the registry fixes […] | flags bit 0;
> flags bit 1 | verifier | certification | `[R-CNT-22]` (R-CNF-05) |

So the document itself treats "a stored MU or PE bit differing" as two
alternatives at file scope and as none at layer scope.

L47's collapse of the two bits is right — §21.1 names "a combination of two flag
bits" as a single predicate — but its collapse of the two containers is not,
because L17 and L18 do not collapse theirs.

Applying the rule consistently gives 60 + 107 + 46 + 44 = 257 instances, not the
253 §21.8 states. That is finding register-03. I note explicitly that the total
*does* reproduce from the cells as written; what does not reproduce is the cells
from the definition.

Two weaker granularity mismatches I found and decided not to raise separately,
because each is individually defensible under §21.1's "without the condition
changing shape" escape: T18 splits the zstd extra-frame family four ways (second
frame; skippable before / after / between) while R4 splits the same constraint
set two ways (a skippable frame; a second frame); and F9 states one instance for
"A structure occupies bytes between the live directory's end and the live
trailer" while F35 enumerates five claimant kinds for a structurally similar
whole-file question. I mention them in register-03's detail as corroboration
that the instance rule is applied unevenly, not as findings of their own.

## 9. Every cross-reference to a row

I grepped for row labels outside the tables and resolved each:

- §9.6 line 1213: "(§21.2 rows F10 and F19)" for a file whose final 64 bytes are
  not a valid trailer. F10 is the magic, F19 is committed_file_length against
  the transport size. Both are `[R-CNT-06]` gates and both are apt; the list is
  illustrative rather than exhaustive (F16, the trailer CRC, is the third likely
  one), which the sentence's grammar allows. Resolves correctly.
- §17.2 note line 2156: "`[R-COD-08]` rejects it (§21.4, T24)" for a whole
  trailing byte after a DEFLATE stream's final bit. T24 is "The decode does not
  consume the entry's length exactly — bytes remain in the stored extent after
  the stream, frame, or block ends", governing rule `[R-COD-08]`. Exact match.
- §21.1: "F2 of F8 and of F10, F37 of F38, L25 of L26". Checked each: F2's
  front-block instance specializes F8 (the 16-byte block not byte-identical) and
  its trailer instance specializes F10 (the 8 bytes at F−64 not the magic); F37
  (reserved-range type with MU = 1) specializes F38 (reserved-range type
  whatever the MU bit); L25 specializes L26 the same way. All three hold.
- §21.1: "T24's *any codec*" and "(T15, T25)" — the cells read exactly that.
- F35's own text: "caught by the bounds rows F11/F12, F33/F34, L17/L18 and
  T8/T9, each at its own tier". Checked all eight: F11 dir_offset < 16, F12
  dir_offset + dir_length past F−64, F33 extent_offset in 1–15, F34 extent past
  F−64, L17 layer/sub-record extent_offset < 16, L18 layer/sub-record extent
  past F−64, T8 entry offset < 16, T9 entry extent past F−64. Every one is the
  front-block-or-trailer bound at its scope. Correct, and the tiers differ as
  claimed (open / open / layer access / tile use).
- §21.6 line 3210: "emitting one is a violation (F38, L26)" — correct.
- §21.6 lines 3246–3248: "(F20, `[R-CNT-07]`)" and "(F37, F38, L25, L26)" —
  correct.
- Appendix H line 3883: "no structure between the live directory's end and the
  live trailer (`[R-CNT-05]`, F9)" — F9 says exactly that, detector verifier.
  Correct.
- Appendix H line 3884: "a reserved-range record or sub-record type value,
  whatever its MU bit (`[R-CNT-15]`, F38, L26)" — correct, and "whatever its MU
  bit" is F38's and L26's own wording.

Every row citation in the document resolves to a row that says what the citing
text claims. No misdirected citation found. That is a clean result and I record
it as such rather than padding it into a finding.

## 10. Limits, in both directions

§21.9's minimum-guarantee table (rank 32, C 4096, entry_count 2³², 65,536
layers, 16 MiB dir_length, 256 MiB decoded tile, 16 MiB metadata document, 8 MiB
zstd Window_Size) matches Appendix B's restatement item for item:

> | Reader minimum guarantees | rank 32 · C 4096 · entry_count 2³² · 65,536
> layers · 16 MiB directory region · 256 MiB decoded tile · 16 MiB metadata
> document · 8 MiB zstd window | §21.9 |

I checked the note's arithmetic: 2³² entries is ⌈2³²/2¹⁶⌉ = 2¹⁶ segments, times
4 bytes = 262,144 = 256 KiB — as stated; at 2³⁶ it is 2²⁰ × 4 = 4 MiB — as
stated. The two forward references out of §21.9 also hold: §17.2 says "Writers
SHOULD keep the declared window within §21.9's 8 MiB `Window_Size` guarantee",
and §18.2 says a reader decodes "with a bound of its own choosing, no smaller
than §21.9's user-metadata guarantee". Both land on rows that exist.

Hard limits stated in §21.9 versus their defining sections:

| §21.9 says | defining section says | agree? |
|---|---|---|
| name at most 255 bytes (`[R-ENC-12]`) | §4.6 "at most 255 bytes of UTF-8" | yes |
| rank at most 255, C at most 65,535 (§7.4's u8 and u16) | §7.4 field widths | yes |
| codec 4 at decoded tile size at most 0x7E000000 | `[R-COD-07]` | yes |
| every offset, length, extent, count at most 2⁶³ − 1 | `[R-ENC-03]` | yes |
| A a power of two, 512 ≤ A ≤ 2⁶² | §7.4, `[R-SLB-01]`, §16.1 | yes |
| A_slab a power of two, 1 ≤ A_slab ≤ 2⁶² | §7.4, §16.2 | yes |
| S with 1 ≤ S ≤ 2⁶³ − 1 | §7.4, §16.2 | yes |
| directory at least 4 bytes at offset at least 16 | §6.2 table, `[R-CNT-06]` | yes |
| no conforming file shorter than 128 bytes | §5.1, `[R-CNT-27]` | yes |

I then swept the document for limits stated elsewhere and absent here. The
multiplicity caps (at most one file-scope user-metadata record, at most one
user-metadata sub-record per layer) and the two-deep nesting cap are limits in a
loose sense but not magnitude limits of the kind §21.9's paragraph describes
("a file violating one is invalid, not merely large"), and the first two are
registered as F36/L20. §6.4's 65,536-byte discovery window is a writer SHOULD
and affects neither validity nor acceptance. §11.3's 1–16 MiB tile range is
explicitly guidance. I found no missing magnitude limit.

One thing in the hard-limit paragraph is wrong, though. It says:

> Most follow from a field's width, an external format, or the value domain, and
> the rest from arithmetic over structures a generation cannot omit. One does
> not: the 512 floor on A is a number chosen here

The 255-byte name cap is justified in the same sentence as "(`[R-ENC-12]`, a
`u8` length prefix)". But §4.6 defines names to include user-metadata keys —
"**Names** — the strings that identify layers, dimensions, channels, and
user-metadata keys" — and a user-metadata key is a JSON string with no length
prefix at all. R10 registers "A user-metadata document key is longer than 255
bytes" as an ignore-record violation, governing rule `[R-MTA-04]` (R-ENC-12).
So for keys the 255 is a chosen number too, and §21.9's "One does not" is two.
Finding register-07.

## 11. Reverse direction: rows registering non-violations

I asked, of every row, whether the cited rules actually make the condition a
violation. All of the verifier-detected rows survive: `[R-CNT-12]` states
outright that the reserved-flag and MU = 1 / PE = 0 cases "make the file
nonconforming (`[R-CNF-05]`)"; `[R-CNT-22]` states "A stored-flag mismatch on a
registered type makes the file nonconforming"; `[R-MTA-05]` states "the file is
nonconforming, a verifier MUST report it"; `[R-CNT-15]` states "emitting it is a
violation". F21's incompat-lane row survives because §6.3 carves out only the
*ignore* lane from file conformance.

One row does not carry its own weight: **R1**. Its Governing rule cell is
`[R-CNT-25]`, and R-CNT-25 says only

> An encoding value of 0, or one the reader does not implement, makes that
> record unreadable, with the same outcome as a failed CRC — ignore-record,
> SHOULD be reported.

which fixes an outcome and says nothing about validity. What makes a
reserved-range encoding a *violation* is `[R-EXT-03]`'s "a value from a reserved
range MUST NOT be emitted at all before this specification assigns it" — the
same clause that carries F38 and L26 — and R1 does not cite it. Meanwhile
§21.6's neighbouring row explains the experimental-range encoding as conforming
because "§10.3's prohibition binds a writer's conduct, not the bytes", and §2.3
cites "§10.3" undifferentiated when listing the conduct rules. A reader who
applies §21.1's "where a row and the rule it cites diverge, the rule governs" to
R1 gets R-CNT-25, which does not make the file nonconforming — the wrong answer.
§21.5's preamble ("Every row here is a violation all the same") and R-EXT-03
between them settle it, so I do not call this byte-level, but the citation is
incomplete in a place where the parallel rows F38 and L26 get it right. Finding
register-06.

## 12. §21.1's own normative status

§21.1 carries the register's load-bearing rules — completeness is normative; the
row-versus-rule precedence; the finest-structure scope rule; the specialization
attribution rule; the instance arithmetic — and carries no requirement
identifier of its own. Its opening cites `[R-ERR-02]`, but R-ERR-02 is defined
in §21.8 and is the vector-coverage requirement ("Every row of §21.2 through
§21.5 — 125 conditions over 253 instances — has at least one conformance vector
… `[R-ERR-02]`"); in §21.1 it reads as a cross-reference for the range "§21.2
through §21.5", not as an assignment. §21.7 ends with `[R-ERR-01]`, §21.9
carries R-ERR-03/04/05, so the identifiers around §21.1 are all spoken for.

§2.2 says "Normative requirements carry identifiers of the form
`[R-<PREFIX>-<NN>]`", and §1's reading note says "test vectors and conformance
checklists cite identifiers, never prose positions". A vector or checklist that
wants to cite the precedence rule has nothing to cite. Finding register-08.

## 13. Outside my charter, but found while reading: Appendix G's closing claim

Appendix G ends:

> Everything else the profile needs is already mandatory — fill-encoded edge
> padding (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among them.
> Four things are not, and the items above are where the profile adds them: gap
> *content*, which `[R-CNT-03]` only advises; gap *extent*, which placement
> freedom (`[R-SLB-05]`) leaves open; sub-record order within a layer record's
> inline payload, which `[R-CNT-14]` leaves free; and the fill a writer records
> when its caller chooses none, which `[R-TYP-10]` states as a SHOULD.

At least three of the numbered items close a freedom that is neither already
mandatory nor one of the four:

- item 6, "**The sentinel for every all-fill tile**, so that a tile whose
  samples all equal fill is never stored" — nothing in the core obliges a writer
  to leave an all-fill tile unstored; `[R-TYP-08]` and `[R-IDX-02]` govern
  unstored tiles, not which tiles must be unstored. Item 6 has exactly the same
  grammatical form as item 7, which *is* in the list of four.
- item 8, "`version_minor` at the floor `[R-CNT-26]` states" — `[R-CNT-26]` is a
  SHOULD, so this hardens a fifth advisory. (The `flags` = 0 half of item 8 is
  genuinely mandatory under §6.3, so only the minor half counts.)
- item 3's top-level record ordering ("Records are ordered by type, and within
  type 0x0001 by layer name") — `[R-CNT-14]` leaves top-level record order as
  free as sub-record order, but only sub-record order is named in the four.

Appendix G is non-normative and adds no requirement to any actor, so nothing
turns on this for bytes. Recorded as register-09 and flagged as out of charter.

## 14. Things I checked and found sound (recorded so the negative result counts)

- Every register row's Governing rule identifier exists in the document; no
  dangling citation.
- The four subsection condition counts (38/50/27/10) and §21.8's 125 reproduce.
- 253 reproduces from the cells as written.
- All four outcome classes reachable; no undefined outcome used.
- All five detection-point values used and no misuse.
- §15.3's eleven entry states, R-CNT-06's eleven trailer gates, R-COD-06's six
  zstd constraints, R-MTA-04's four document restrictions, and §7.4's constraint
  table are each fully registered.
- Every row-label citation elsewhere in the document resolves correctly.
- §21.9's table matches Appendix B's restatement exactly, and its note's
  arithmetic (256 KiB at 2³², 4 MiB at 2³⁶) is right.
- CRC-32C check vector, Appendix A's trailer CRC, and the all-sentinel segment
  constant all reproduce under a locally implemented CRC-32C.
- §21.6's fourteen entries each match the rule they cite (the only slip is that
  the slack row omits "and report their byte extent" that `[R-CNT-21]` and
  Appendix H both include — too small to raise).
- §21.1 explicitly disclaims completeness for §21.6, §21.7 and §21.9, which
  forecloses a whole family of would-be findings about §21.6 being non-exhaustive.
  That disclaimer is doing real work and is correctly placed.

## 15. Findings, in the order I would fix them

1. register-01 — F1's version_major instance registers what §21.6 and §2.3 say
   is not a violation. Byte-level (verifier verdict).
2. register-02 — §21.3/§21.4 headers and §24's `[R-VEC-04]` state reader
   obligations that §21.1's verifier paragraph and `[R-SER-08]`/`[R-CNT-22]`/
   `[R-MTA-05]` deny, for 13 rows.
3. register-03 — instance arithmetic applied inconsistently at L47, L48, L50;
   consistent application gives 257, not §21.8's 253.
4. register-04 — no layer- or tile-scope endianness row, against a
   scope-neutral F1 and against the width family's three-scope precedent.
5. register-05 — §21.7 does not account for `[R-CNT-18]`'s nesting-depth
   prohibition, though §21.1 nominates it as the account of what fails the
   detectability gate.
6. register-06 — R1 cites only `[R-CNT-25]`, which does not make a
   reserved-range encoding a violation; `[R-EXT-03]` is the operative rule and
   is uncited.
7. register-07 — §21.9's "a `u8` length prefix" justification does not hold for
   user-metadata keys, so "One does not" undercounts the chosen numbers.
8. register-08 — §21.1's normative rules carry no requirement identifier.
9. register-09 — Appendix G's "Four things are not" is at least three short.
   Out of charter, reported anyway.
