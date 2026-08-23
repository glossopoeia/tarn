# Cleanroom round 22 — Adversary transcript

**Access.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,394 lines), in six `Read` calls covering lines 1–4394. I ran `grep`/`python3`
against that file only, plus local Python that reads no file (a CRC-32C
implementation and a file builder). I wrote and read four scratch files of my own
under my scratchpad: `tarnlib.py`, `good.tarn`, `two_layer.tarn`,
`giant_sentinel.tarn`. I opened no ADR, no `docs/`, no `conformance/`, no
`registry.json`, no `PLAN.md`, no git history, no network resource. I did not list
or read the round-22 output directory.

**Context I did not ask for.** Before I began, my runtime placed a project
instruction file and an index of the maintainer's private memory notes in my
context. Both name things about this project's cadence and about prior rounds.
I did not read any file they point at, and nothing below is drawn from them. I
disclose their appearance because the access rule requires it; I have not
repeated their contents.

---

## 0. Method

I did three things, in order.

1. **Calibrated my tools against the document's own worked examples.** Before
   attacking anything I implemented CRC-32C to §4.5's parameters and reproduced,
   byte for byte, Appendix A's 128-byte minimal file, §7.4's 81-byte layer-record
   payload, §7.4's `0x80A34955` / `0xC4EE982E`, §15.4's `0xEECB3BB2`, and §4.5's
   two check vectors. All matched. This matters: it means that where I later say
   "the document determined this byte", I am not guessing at my own arithmetic.

2. **Built two conforming files end to end from the document alone** — a
   single-layer file with stored tiles, and a two-layer file exercising planar
   mixed types, edge padding, a packed boolean plane, a slab declaration with two
   runs, and a file-scope user-metadata record. I recorded every point where I had
   to make a decision the text did not make for me. There was exactly one class of
   such point, and it is finding 01.

3. **Ran the attack surfaces of my charter**, then wrote up both the survivors and
   the attacks the text forecloses, with the sentence that forecloses each.

I read §18.2 and §21.9 first, as directed, then walked the whole document.

---

## 1. Tool calibration

CRC-32C per `[R-ENC-09]`: Castagnoli, reflected in/out, init `0xFFFFFFFF`, final
XOR `0xFFFFFFFF`, stored little-endian.

```
crc32c("123456789") = 0xE3069283      (§4.5 check vector: 0xE3069283)  ✓
crc32c("")          = 0x00000000      (§4.5 check vector: 0x00000000)  ✓
```

Appendix A's minimal file, rebuilt from §6.1, §7.1 and §6.2 and not copied:

```
89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
00 00 00 00 ... (44 bytes of pad) ...
8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
04 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00
EF CD AB 89 67 45 23 01 00 00 00 00 D2 38 09 E0
```

My computed trailer CRC over bytes [0,60) is `0xE00938D2`; Appendix A stores
`D2 38 09 E0`. Identical.

§7.4's index constants: CRC-32C over 80 sentinel bytes = `0x80A34955`, stored
`55 49 A3 80`; CRC of that 4-byte array = `0xC4EE982E`. Both reproduce. §15.4's
full all-sentinel segment (2¹⁶ entries) = `0xEECB3BB2`. Reproduces.

I also re-derived §7.4's 81-byte inline payload field by field from the table and
got byte-identical output, including the 4+34/18/12/13 accounting the example
states.

**Conclusion.** The document's arithmetic is checkable and correct. I found no
numeric error anywhere I looked, including §11.2's, §11.4's, §14.2's, §14.3's,
§14.5's, §15.4's and §17.3's worked examples, and §21.9's note's 256 KiB / 4 MiB /
1.25 MiB / 12.5 MiB figures. I verified §17.3's byte-shuffle example by
recomputing `i·n + j` for all twelve bytes.

---

## 2. Register self-consistency (mechanical)

§21.8 says: "Every row of §21.2 through §21.5 — 121 conditions over 273
instances — has at least one conformance vector". I extracted all register rows
and counted instances by §21.1's own rule ("Instances within a cell are separated
by semicolons, and a cell reading — is one instance"):

| section | conditions | instances |
|---|---|---|
| §21.2 (F) | 36 | 58 |
| §21.3 (L) | 49 | 116 |
| §21.4 (T) | 26 | 55 |
| §21.5 (R) | 10 | 44 |
| **total** | **121** | **273** |

Matches §21.8 exactly, and each subsection header's own count (36 / 49 / 26 / 10).

I then extracted every `[R-XXX-NN]` identifier (161, minus the `[R-ENC-100]`
example in §2.2) and every identifier named in a Governing-rule cell, and worked
the 94-identifier difference by hand looking for a **detectable** file-conformance
violation the register omits — §21.1 makes that completeness normative. Every one
I checked is either a reader/writer/updater/verifier *behaviour* rule with no file
witness, a SHOULD, a process rule, a rule §21.6 records as a non-violation, or a
rule §21.7 expressly accounts for (`[R-ENC-06]`, `[R-LIF-01]`, `[R-LIF-03]`,
`[R-SLB-04]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s embedded-offset
prohibition, `[R-CNT-18]`'s nesting prohibition, §20.3 step 4's bar, §20.5's two
trailer obligations). I found no missing row.

I also checked that every row label cross-referenced in prose resolves: §21.1's
`F1 of F6 and of F8, F35 of F36, L24 of L25`; §21.2's preamble (`F8`, `F14`, `F6`,
`F18`); F33's `F9/F10, F31/F32, L16/L17 and T8/T9`; §9.6's `F8 and F17`; §20.3's
`L44`; §20.5's `F36, L25, R1`; §21.7's `T2, T4 or T5`, `T3 or T14`,
`T15, T17, T23, T25`; Appendix H's `F1, F6`, `F7`, `F36, L25`, `R1`. All resolve.

---

## 3. Building a conforming file end to end

### 3.1 Single layer, stored tiles

Layer `sst` of §7.4's example, but with all four tiles *stored* rather than
sentinel, so that I had to exercise `[R-SER-05]`'s padding rule and `[R-COD-04]`'s
codec-1 length equality.

- rank 1, `x` extent 100, tile extent 32 → G = ⌈100/32⌉ = 4 (§11.2), N = 4,
  P = 32.
- interleaved, one float32 channel, Q = 4 → decoded size P·Q = 128 (`[R-SER-02]`).
- codec 1 → each entry's `length` MUST equal 128 (`[R-COD-04]`).
- Tile 3 covers x = 96..127; x = 100..127 are padding positions (§11.3), and
  `[R-SER-05]` fixes each to the channel's recorded fill — here the quiet NaN
  `00 00 C0 7F`. Nothing else is admissible; §14.5 is unambiguous.
- Placement: tiles at 16, 144, 272, 400; index region [528, 612) = 4×20 + 4 = 84
  (`[R-CNT-17]`); directory [612, 721); pad [721, 768) = 47 bytes
  (`[R-LIF-02]` step 5 pads to the next 64-boundary from 721 → 768); trailer
  [768, 832). F = 832, F mod 64 = 0.

Every byte was determined by the document. No guesses.

### 3.2 Two layers, planar mixed types, slab, user metadata

Second file, harder:

**Layer `a`** — planar, rank 2, E = (5,5), T = (4,4), C = 2: channel 0 `v` uint16
fill `0xABCD`, channel 1 `m` bool fill true.
G = (2,2), N = 4, P = 16, addressed-tile count = C·N = 8 (§11.2).
Disk ordinals 0–3 are channel 0's tiles, 4–7 channel 1's (`[R-GEO-06]`).
Channel 0's plane is P·Bᶜ = 32 bytes (§14.2); channel 1's is ⌈P/8⌉ = 2 bytes
(§14.3). P mod 8 = 0, so there are **no pad bits** — but there are plenty of
padding *positions*, which §14.3's note is careful to distinguish. The four
u16 planes and four bool planes came out as:

```
s=0 (tile 0,0) 0000 0100 0200 0300 6400 6500 6600 6700 c800 c900 ca00 cb00 2c01 2d01 2e01 2f01   bool 5a 5a
s=1 (tile 0,1) 0400 cdab cdab cdab 6800 cdab cdab cdab cc00 cdab cdab cdab 3001 cdab cdab cdab   bool fe fe
s=2 (tile 1,0) 9001 9101 9201 9301 cdab ... (all fill) ...                                        bool fa ff
s=3 (tile 1,1) 9401 cdab ... (15 fill values) ...                                                 bool fe ff
```

Worked by hand for `s=1`: in-tile ordinal k = u₀·4 + u₁ (§11.4). k=0 → u=(0,0) →
coordinate (0,4), inside the extents, sample value 4 → `04 00`. k=1 → (0,5),
outside → `[R-SER-05]` fill `CD AB`. k=4 → (1,4) → 104 = 0x68 → `68 00`. Matches.
For the bool plane at `s=2`: real positions k=0..3 are coordinates (4,0)..(4,3),
bits 0,1,0,1; k=4..15 are padding, so each carries the fill bit 1 — byte 0 =
`0b11111010` = `0xFA`, byte 1 = `0xFF`. The document fixes every bit.

**Layer `b`** — interleaved, rank 1, E = 10, T = 4 → G = 3, N = 3, P = 4, one
uint8 channel, decoded size 4. Slab S = 2, A_slab = 16 (`[R-SLB-02]`,
`[R-SLB-03]`). Block [0,3) partitions into run 0 = ordinals [0,2) and run 1 =
ordinal [2,3) — "the final run of a block can cover fewer than S ordinals". I
placed run 0's first stored tile at 320 (320 mod 16 = 0), tile 1 immediately after
at 324 ("each stored tile's offset equals the previous stored tile's offset plus
its length"), and run 1's single tile at 336 (336 mod 16 = 0). The bytes
[316,320) and [328,336) are slack — `[R-SLB-03]`: "between runs, placement freedom
(`[R-SLB-05]`) governs, and the bytes left between them are slack".

**File-scope user metadata**, encoding 1, document
`{"tarn.creator":"adversary 22","tarn.title":"round22"}` — members in ascending
UTF-8 byte order of their decoded keys (`[R-MTA-05]`; `tarn.c` < `tarn.t`), extent
= document ‖ CRC-32C of the document (§8.1), extent_length 58 ≥ 5 (§7.1),
inline_length exactly 1 (`[R-MTA-03]`).

F = 832, F mod 64 = 0, coverage partitions, `[R-CNT-17]`'s formula holds for both
layers (164 and 64), `[R-CNT-05]`'s gap holds no structure.

**Where I had to guess: nowhere, in either build.** Both files fell out of the
text. That is a strong result for the document and I want it on the record before
the findings.

---

## 4. Attacks

I state each attack as a construction, the two verdicts, and whether the text
forecloses it. Foreclosed attacks come first, so that the two survivors are not
read out of context.

### 4.1 Foreclosed — overlap taxonomy

I tried every overlap pairing I could enumerate and every one is classified:

| construction | classification | citation |
|---|---|---|
| two stored extents of one layer overlap (including byte-identical extents) | reject-layer, verifier | §15.3 row; `[R-CNT-13]`; L18 |
| stored extent overlaps its own layer's index region | reject-layer | `[R-CNT-13]` names it explicitly |
| stored extent overlaps its own layer's sub-record extent | reject-layer | same |
| two sub-record extents of one layer overlap | reject-layer | L18's "layer sub-record extents" |
| stored extent overlaps another layer's anything | reject-file | `[R-CNT-13]`, F33 |
| top-level record extent overlaps a layer's stored tile | reject-file | `[R-CNT-13]` "touching another scope's structures" |
| a record extent whose slot equals (dir_offset, dir_length) | reject-file | F33 "two structures neither of which belongs to a layer" |
| two layer records sharing one index region | reject-file (cross-layer) | F33 |
| any claimant reaching [0,16) or [F−64,F) | caught at the bounds rows | F33's own text: "instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9" |

Nothing overlaps unclassified. I could not build a two-claimant file whose
disposition the text leaves open.

### 4.2 Foreclosed — a structure in the pre-trailer gap

A stored tile placed at [730, 760) in my 832-byte file, where the directory ends
at 721 and F−64 = 768: it clears T8 (offset ≥ 16) and T9 (offset+length ≤ F−64),
so a reader serves it. `[R-CNT-05]` — "A verifier MUST treat a structure in that
gap as a validity error at file scope ... (readers check neither, their check
being the dir-bounds rule of `[R-CNT-06]`)" — makes it F7, reject-file, verifier.
Reader serves, verifier rejects. That is the licensed reader/verifier seam,
stated in the same sentence. Not a defect.

Corollary I checked: this makes the live directory necessarily the **last**
structure in a conforming file, so a writer that emits the directory before its
payloads produces a nonconforming file even though every payload is in bounds.
`[R-LIF-02]` step 3 already orders it that way. Consistent.

### 4.3 Foreclosed — a longer-than-a-pad gap

A commit leaving a 1000-byte pre-trailer pad. `[R-CNT-05]`: "a longer gap is
conforming, and no conforming commit produces one", and §2.3 names exactly this
as one of the two output-governing writer obligations expressly declared not to be
a file-conformance violation. I initially read §2.3's "§6.3's flags = 0 ... and
§6.2's pre-trailer gap ... are the cases this text states" as an incomplete
enumeration, since §10.3's experimental-value prohibition and §18.3's `tarn.` key
rule are also writer-conduct-not-bytes rules. Re-reading, §2.3 puts those two in a
*different, preceding* category ("govern their *conduct* rather than their
output ... (§10.3, §18.3)"), and the two-item list enumerates only the second
category, obligations that do govern output. The sentence is right. Attack dead.

### 4.4 Foreclosed — the duplicate-layer-name trap

Two layer records whose name fields are byte-identical but neither of which is a
valid name (empty, or ill-formed UTF-8), and a layer record whose *name field*
fits inside `inline_length` while the rest of the payload does not. §19.1 step 4
decides all three: "a layer record whose name field does not lie entirely within
that record's inline_length yields no name field to compare, so it contributes no
name to the namespace"; "Uniqueness is decided first, and over the raw name bytes
whether or not each name is itself well-formed ... so two layers whose name fields
are byte-identical are a duplicate even when neither name is valid". Closed.

### 4.5 Foreclosed — reserved / experimental values in every position

I enumerated record type × position × MU/PE and found every cell disposed:

- type 0: F24 (top-level), L13 (sub-record).
- type 0x0001 as sub-record: L26 (`[R-CNT-18]`: "A *known* type appearing where
  §7.3's table does not scope it ... is a validity error at layer scope").
- second type 0x0002 at either scope: F34 / L19.
- reserved-range: F36 / L25 (verifier), with MU=1 specialising to F35 / L24
  (reader).
- experimental MU=0: conforming and ignored (§21.6).
- experimental MU=1 top-level: conforming file the reader must refuse (§21.6's
  second "structural case"); as a sub-record, reject-layer and explicitly *not* a
  ground to refuse the file (§7.4: "where the file is otherwise conforming a
  reader MUST NOT reject the file for it").
- stored-flag mismatch on a registered type: F28 (non-layer top-level) / L49
  (layer record or registered sub-record). MU=1 with PE=0: F25 / L46. Reserved
  flag bits: F26 / L47. The file/layer partition follows `[R-CNT-12]`'s "the
  record's governing scope" and §7.2's scope table. Consistent.

The only thing I could not settle was a compactor's duty toward an
**experimental-range MU=1 type it does implement**: §20.5 says it "relocates
whatever that registration defines", and an experimental value has no
registration. But §7.2 forecloses the harm — "Records with MU = 1 carry further
references only where this specification or registry review (§10) defines them" —
so such a record may not carry offsets, and verbatim relocation is the whole duty.
A compactor that rewrote private offsets inside such an extent would be acting on
a nonconforming input. Not a fork on a conforming input.

### 4.6 Foreclosed — boundary sweep

I walked every stated bound to its edge and one past. All held:

F = 128 exactly (§5.1's arithmetic — dir at 16 length 4 ends at 20, trailer at a
64-aligned offset with dir_offset + dir_length ≤ F − 64 forces F ≥ 128); F = 64
fails F10 before F5; dir_offset = 16 and dir_offset + dir_length = F − 64 exactly
(legal — "exceeds F − 64" is `>`, and the extent ending *at* F−64 does not include
the trailer's first byte; F32, T9 and §15.3's row all use the same `>`);
generation 1 and 2⁶³−1 (§9.3's note closes the file at the ceiling); rank 1 and
255; C 1 and 65535; Eᵢ = 0 (grid count 0, zero addressed tiles, `[R-GEO-02]`);
Tᵢ = 1; Tᵢ > Eᵢ (§11.1: "the grid is then a single padded tile along that axis");
A = 512 and 2⁶²; A_slab = 1 and 2⁶²; S = 1 and 2⁶³−1; name length 1 and 255;
entry index offset = 16; entry length = 1; user-metadata extent_length = 5;
`inline_length` = 0 on an unknown record (legal); codec 4 at decoded size
`0x7E000000` and one past (L44); a zstd tile window equal to the decoded size and
one past (T21); P mod 8 = 0 (no pad bits) and P mod 8 ≠ 0.

Two edges are legal-but-unreachable and the text survives both: **A = 2⁶²** (and
**A_slab = 2⁶²**) forces every stored tile's offset to a multiple of 2⁶², which
with `offset ≥ 16` means no constructible file can store a tile in such a layer —
so L40 and L42 are vacuous there, which is exactly what `[R-SLB-01]` and
`[R-SLB-03]` say ("A run with no stored tiles imposes nothing").

I also checked that `[R-ENC-04]`'s ceiling is reachable ahead of every other bound
it could race: `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` overflows at
entry_count ≈ 4.6 × 10¹⁷, well below `[R-ENC-03]`'s 2⁶³−1 on `entry_count` itself,
so L2 fires before L1 on that path. Both are reader/layer-access/reject-layer, so
nothing turns on the order.

### 4.7 Foreclosed — L2's instance cell and layout-conditioned quantities

L2 enumerates, among others, `P·Q (which dominates V = P·C)` and `P·Bᶜ` and
`C·N`. `P·Q` and `V = P·C` are defined by §14.2 and §14.1 **for interleaved
layers only**; `P·Bᶜ` for planar numeric planes only; `C·N` is §11.2's
addressed-tile count **for planar layers only**. A literal reading of the cell as
a conjunction would make a *planar* layer with P = 2⁶⁰, C = 4096, Bᶜ = 1 reject
(P·Q = 2⁷²) though nothing the specification defines for that layer overflows.

Foreclosed twice over: §21.1 says an instance names "one of several alternatives
the condition text states" and that "Where the quantity a condition derives varies
by layout, the layout formulas are materially different shapes and the cell
enumerates them" — the cell is a disjunction across layouts, not a conjunction —
and "where a row and the rule it cites diverge, **the rule governs**", the rule
being `[R-ENC-04]`'s "any quantity this specification **defines**". I also checked
that the interleaved analogue (C·N overflowing on an interleaved layer) needs
entry_count > 2⁴⁷, hence an index region above a petabyte, so it is unreachable in
any file that also satisfies L17.

### 4.8 Foreclosed — T14 as an unrecorded specialization of T3

Under codec 1 with either filter (filter 2 leaves length unchanged,
`[R-COD-10]`), the decoded payload's length *is* the entry's length, so every file
exhibiting T14 exhibits T3. §21.1 names three specialization pairs ("F1 of F6 and
of F8, F35 of F36, L24 of L25") and not this one. I nearly reported the list as
incomplete, then re-read: the *rule* is stated generally — "a file exhibiting a
specialization is recorded against the narrower row, whose detector and detection
point are the ones that apply" — and the dash-list exemplifies rather than
exhausts. The rule self-applies to T14/T3, and since both rows are
reader/tile-use/reject-tile nothing turns on it anyway. Dead.

(Same disposal for a smaller asymmetry I noticed and am not reporting: L2 and T12
both carry an "although every contributing field is in domain" qualifier and F3
does not, so a file with `dir_offset` above 2⁶³−1 exhibits F2 *and* F3 where the
sibling phrasing would give F2 alone. §24 covers files that exercise several rows,
and all three rows are reader/open/reject-file.)

### 4.9 Foreclosed — `[R-COD-11]`'s cannot-establish branch at a reserved codec

A verifier meeting `codec = 7`. `[R-COD-11]` sentence 1 reads: "A verifier that
cannot execute a layer's codec or filter cannot establish that layer's conformance
and MUST NOT certify the file." Nobody can execute codec 7, so a verifier could
read itself into reporting *cannot establish* rather than *nonconforming* — two
different verdicts on the same bytes. Foreclosed by two later clauses:
`[R-COD-03]` makes the value itself "a validity error at layer scope" (L43,
detector *reader*), and §2.3 says "An established violation takes priority: a
verifier that has established any violation reports *nonconforming* ... and
*cannot establish* is available only to a traversal that established no
violation." Verdict is *nonconforming*. `[R-COD-11]`'s own third sentence says
the same. The branch is dead text for a conforming verifier — every assigned codec
and filter is core — but it is not a contradiction.

### 4.10 Foreclosed — the §18.2 window text

I read §18.2's new material hunting for a scope slip and did not find one.

- "the bound above" is singular where two bounds (decode size, window) precede it.
  §21.5's preamble disambiguates: "except where a reader or verifier declines the
  decode on the size bound **or on the frame's declared window**, which
  `[R-MTA-09]` makes that actor's capability and not a fact about the file", and
  §2.3 lists "when it declines to decode a user-metadata document (`[R-MTA-09]`)"
  unqualified. Both bounds.
- "the file exceeds a §21.9 guarantee and so remains conforming" is asserted
  unconditionally. I checked it is sound: the reader's window bound is "no smaller
  than §21.9's guarantee", so a frame "declaring more than the reader admits"
  necessarily declares more than 8 MiB. The assertion cannot be false.
- The two clauses that constrain a reader's own bounds carry no BCP 14 keyword
  ("a reader's window bound is its own, no smaller than §21.9's guarantee"), which
  by §2.1 gives them no force of their own. They are nonetheless backed by
  capitalised text elsewhere: `[R-CNF-03]`'s MUST-accept and `[R-ERR-04]`'s
  "Software that declines **on that ground** a file whose every quantity lies
  within the table is not a conforming reader". So the floor binds. I looked
  specifically for a case where the lowercase clause is the *only* thing standing
  between two readings and did not find one.
- `[R-ERR-04]` offers exactly three decline scopes ("at the whole file, or at the
  narrowest scope whose declarations exceed what it can serve, a layer or a
  tile") and does not offer *record* scope, while `[R-MTA-09]` says an
  over-window document "is ignore-record". §18.2's own Note reconciles them: "A
  reader that proceeds takes ignore-record for that record; a reader that instead
  declines on resource grounds under `[R-ERR-04]` does so at the whole file". Two
  licensed paths, stated.
- The excluded frame constraints are enumerated ("the frame magic; no skippable
  frame and no second frame; no nonzero dictionary ID; no content-checksum flag"),
  which drops `[R-COD-06]`'s *undisclosed*-dictionary writer prohibition, since
  that clause references a tile. I do not report this: §21.7 already places
  undisclosed dictionary use in the class that "every checksum in §8 certifies",
  so carrying it over or not cannot change the set of emittable conforming files.

### 4.11 Foreclosed — capability forks that are not defects

I confirmed and set aside a large family of file-specific divergences that the
document *licenses* explicitly, so that they are not reported as findings: a
conforming file whose zstd metadata window exceeds a verifier's bound gets
*conforming* from one verifier and *cannot establish* from another (§2.3,
`[R-MTA-09]`); a verifier that implements a private experimental type certifies
where one that does not reports *cannot establish* (§21.6); a reader that stops at
the first violation reports fewer rows (`[R-CNF-11]`); a reader whose speculative
suffix window reaches offset 0 must check the front block where one whose window
starts at offset 4 need not (`[R-CNT-04]`, and F6's Condition cell restates it).
None of these is a certify-versus-reject fork: *cannot establish* is not
certification, and §2.3's priority rule keeps an established violation on top.

### 4.12 Foreclosed — the degenerate files

Smallest conforming file: 128 bytes (Appendix A), verified.

Smallest conforming file **carrying a record**: 128 bytes as well — front block,
a 28-byte directory at [16,44) holding one 24-byte record of an experimental type
(MU = 0, PE = 0, `inline_length` = 0, extent slot (0,0)) plus its CRC, 20 bytes of
slack, trailer at [64,128). Conforming by §21.6's "A record type this
specification has not assigned, from the experimental range ... carries MU = 0 |
Ignored". Nothing in the document objects.

A layer with a zero extent, a slab declared, codec 4 declared, and a tile shape
whose decoded size is enormous: conforming, and §17.2's Note says so in terms —
"a layer that addresses none ... satisfies it whatever its tile shape declares,
and codec 4 is conforming there ... `[R-ENC-04]`'s overflow rule carries no such
quantifier". I confirmed the escape is not durable, per the same Note.

A file whose directory occupies [16, F−64) entirely, leaving room for no other
structure: conforming.

**The one degenerate file whose disposition I could not settle is finding 01.**

---

## 5. Findings

### Finding 01 — §21.9: "the tiles ... a file actually contains" does not say whether an addressed-but-unstored tile is one

**Kind:** AMBIGUITY
**Location:** §21.9, `[R-ERR-03]`'s paragraph following the limits table; reads
onto §2.3 `[R-CNF-03]` and §21.9 `[R-ERR-04]`.

**Quotation.**

> The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains, and a
> file containing none of a kind does not exceed that row, whatever its
> declarations would derive — a layer addressing no tile (§11.2) has no tile whose
> decoded size the table can bound, exactly as `[R-COD-07]`'s cap is quantified
> over a layer's *addressed* tiles. The first five range over declarations, which
> every file and every layer carries.

**The file.** 256 bytes, built and checked against every rule I could find:

```
front block                       [0, 16)
tile-index region                 [16, 40)   one entry: FF×16 00×4  ‖ segment CRC
directory                         [40, 141)  one layer record, inline_length 73
pad                               [141, 192)
trailer                           [192, 256)  F = 256
```

The layer declares rank 1, dimension `x` with extent 1 and **tile extent 2³⁰**,
one interleaved `uint8` channel with fill `0x00`, codec 1, filter 1,
`index_encoding` 1, `entry_count` 1, and its one index entry is the sentinel.
Grid count ⌈1/2³⁰⌉ = 1, so N = 1 and `entry_count` = 1 satisfies `[R-CNT-17]`;
P = ∏Tᵢ = 2³⁰ and Q = 1, so the tile's decoded size is **2³⁰ = 1024 MiB**.
Nothing is stored, so §14.5's padding obligation and `[R-COD-04]`'s length
equality are both vacuous. N·P = 2³⁰ and P·Q = 2³⁰ are far inside
`[R-ENC-04]`'s ceiling. The file is conforming.

**The two readings.**

*Reading A — "contains" means addressed.* The file contains one tile, whose
decoded size (1024 MiB) exceeds the table's 256 MiB row. The file therefore does
not satisfy `[R-CNF-03]`'s "none of whose values exceeds the minimum guarantees",
the MUST-accept duty does not run, and a reader with a 512 MiB ceiling MAY decline
the layer under `[R-ERR-04]`, reporting a resource limit.

*Reading B — "contains" means physically present.* A sentinel tile "occupies no
payload bytes" (§13) and is precisely the thing §3.1 calls addressed-and-not-
stored. The file therefore contains no tile, "a file containing none of a kind
does not exceed that row, whatever its declarations would derive" applies, every
quantity of the file lies within the table, and a reader that declines is caught
by `[R-ERR-04]`'s "Software that declines **on that ground** a file whose every
quantity lies within the table is not a conforming reader".

**Which I picked, and why.** Reading A. The em-dash clause pins the quantifier by
analogy — "exactly as `[R-COD-07]`'s cap is quantified over a layer's *addressed*
tiles" — and `[R-COD-07]`'s quantifier is beyond argument: L44 reads "Codec 4
(lz4) declared on a layer any of whose **addressed** tiles' decoded size exceeds
`0x7E000000`", and §17.2's Note spells out that an all-sentinel layer whose
declared decoded size is over the cap still violates it. Making §21.9 range over
stored tiles would break the "exactly as" and leave the two rules with different
quantifiers over the same derived quantity.

**Why it is nonetheless open.** Three things pull the other way, and they are in
the operative sentence rather than in its gloss.

1. The governing phrase is "a file **actually contains**", and *actually
   contains* is not one of §3.1's defined terms. §3.1 gives the document a
   precise pair — "**addressed tile / stored tile** — every tile of a layer is
   *addressed*. A tile is *stored in a generation* if and only if that
   generation's tile-index entry for it is not the sentinel" — and the sentence
   uses neither. Where the document means addressed it says *addressed*: L44 does,
   §17.2's Note does, and §21.9's own gloss does. The operative clause does not.
2. The phrase governs all three rows at once, and for the other two it can only
   mean physical presence. A user-metadata document exists because a record's
   extent holds one; a compressed frame exists because a tile's or an extent's
   stored bytes are one. Under reading A the same four words mean "addressed" for
   row 1 and "physically present" for rows 2 and 3 — and the split has a visible
   consequence: the very layer above, if it declared codec 3, would *contain a
   tile* (row 1 engaged) and *contain no frame* (row 3 vacuous) simultaneously.
   The sentence never says the phrase is read non-uniformly.
3. The analogy is doing weaker work than it appears. It explains the **vacuous**
   case — a layer that addresses nothing — and that case is vacuous under both
   readings, since a layer addressing no tile stores none either. The analogy is
   therefore *consistent with* reading B rather than excluding it; what would
   exclude B is a sentence saying a tile counts as contained iff addressed, and
   there is none.

**What an implementer does wrong without it.** Two reader designs that both look
correct from this text:

- *Eager*: at layer access, §19.3 already obliges the reader to compute "the
  decoded sizes §14 derives" (`[R-SER-02]`, `[R-SER-07]`) as part of the overflow
  check. Having the number in hand, it compares it against its own configured
  ceiling and declines the layer with a resource-limit diagnostic. Under reading B
  this design is not a conforming reader, and its diagnostic on a 256-byte file
  that contains no data at all reads as a bug to the operator.
- *Lazy*: it applies its ceiling at step 6 of §19.4, when a payload is actually
  decoded, so a sentinel-only layer never trips it and the layer serves fill. Under
  reading A this design is merely one that chose not to exercise a MAY, so it is
  conforming either way — but its author cannot tell from this text whether the
  eager design is also conforming, which is what a limits section exists to settle.

The same question decides a corpus obligation: `[R-VEC-03]` requires that
"§21.9's minimum guarantees are exercised where a vector at the bound is
constructible". Under reading A the 256 MiB tile-size bound is exercisable by a
~256-byte all-sentinel file like the one above; under reading B it requires a
vector with a genuinely stored 256 MiB tile. §24 calls out only the *tile-count*
guarantee as unconstructible, so it does not settle this either.

**Byte-level: yes.** It decides whether a conforming reader must accept a specific
byte sequence — the 256-byte file above. Under reading A, *Eager* refusing it is
an exercise of `[R-ERR-04]`'s MAY; under reading B, *Eager* refusing it makes
*Eager* not a conforming reader while *Lazy* serves the layer as fill. The two
implementations differ on accept-versus-refuse for those exact 256 bytes.

**Repair shape (not a proposal, just to show the fix is one word).** Replacing
"a file actually contains" with "a file addresses" — or adding, after the em-dash,
that a tile counts as contained when addressed whether or not it is stored —
closes it. Either way the sentence should say which of §3.1's two defined terms it
means, since it has both available.

---

### Finding 02 — `[R-MTA-09]` creates a content-size condition and assigns it to R3, which never mentions it

**Kind:** OBSERVATION
**Location:** §18.2 `[R-MTA-09]`; §21.5 row R3; §21.1's instance discipline;
compare §21.4 row T22 and §21.8 `[R-ERR-02]`.

**Quotation.** §18.2:

> The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal the
> byte length of the decoded document. A mismatch is a failure to decode within
> the meaning of R3, so that R3's condition stays checkable from the bytes alone
> rather than turning on a decoder's tolerance (`[R-CNF-02]`) — the tile rule of
> `[R-COD-06]` transposed to the quantity a document does have, its decoded
> length, in place of the declared size it does not.

And the row it assigns the condition to, in full:

> | R3 | A user-metadata document's stored bytes fail to decode under its declared
> assigned encoding — under an experimental-range one this specification defines
> no decoding and §21.6 governs (`[R-MTA-10]`); encoding 0 and a reserved value
> are unassigned too and R1 registers both | top-level extent; layer sub-record
> extent | reader | extent use | `[R-CNT-25]` |

**The gap.** Three of the row's five cells fail to carry the condition
`[R-MTA-09]` puts in it.

1. *Condition cell.* "stored bytes fail to decode" does not describe a
   content-size mismatch. Such a frame decodes perfectly well as RFC 8878; what
   fails is an equality between a header field and the decoded length. R4's cell,
   by contrast, is explicit that it covers constraints broken "whether or not the
   bytes decode". R3's is not, and §21.1 says a row "*restates* its governing
   rule".
2. *Governing rule cell.* R3 cites `[R-CNT-25]` alone. `[R-MTA-09]` — the rule
   that creates this condition, states its MUST and assigns it here — is not named,
   in the row or in its parentheses. R4's cell does name `[R-MTA-09]`. A reader
   who chases R3 to its governing rule lands on the quarantine paragraph in §7.1
   and never learns that a content-size field must be compared at all.
3. *Instances cell.* "top-level extent; layer sub-record extent" — two containers,
   no alternatives. Compare the tile-side rule this one is explicitly "transposed"
   from. `[R-COD-06]`'s content-size equality gets its own row, T22, whose
   instances are "interleaved P·Q, declared larger; interleaved P·Q, declared
   smaller; planar numeric P·Bᶜ, declared larger; ... packed planar bool ⌈P/8⌉,
   declared smaller" — six, because §21.1 says "Where the condition compares two
   **magnitudes** either of which can be the greater — a *differs from* or *does
   not equal* — the two directions are likewise enumerated". A document has no
   layout axis, so the transposed condition has 2 directions × 2 containers = 4
   instances. R3's cell enumerates none of them, and R3's instance count of 2 is
   what feeds §21.8's "121 conditions over 273 instances" (I counted; the total is
   arithmetically correct *as the cells are written*).

**What an implementer does wrong without it.** `[R-ERR-02]` promises "one vector
per instance", so as the register stands the corpus owes **no vector** for a
user-metadata frame whose `Frame_Content_Size` disagrees with the decoded document
— in either direction, at either scope. That is a real interoperability trap and
not a hypothetical one: several zstd bindings validate the frame content size for
the caller and several do not, so an implementation that decodes with a
whole-buffer API and never inspects the header will silently accept the file and
return the document, where `[R-MTA-09]` requires ignore-record. The tile side of
exactly this trap gets six vectors via T22; the document side gets zero. §21.8's
own answer — "A row without a vector is a gap in the corpus, not a licence to skip
the check" — keeps the check owed, which is why I grade this an observation rather
than a fork.

I also note the asymmetry this leaves inside §21.5 itself: R4's cell enumerates
six frame constraints × two containers = twelve instances, so the register is
plainly willing to enumerate frame-level alternatives for metadata; the one frame
constraint that lives in R3 instead of R4 is the one that gets none.

**Byte-level: no.** `[R-MTA-09]`'s MUST is unambiguous and capitalised, the outcome
(ignore-record, R3) is stated, and §21.1 puts the rule above the row where they
diverge. No two implementations reading `[R-MTA-09]` can disagree about the
verdict on a mismatching frame. What is lost is the register's traceability and
the corpus obligation that would have caught an implementation that skipped the
check — a cost to conformance testing, not to the emittable set.

---

## 6. Ranking, and what I could not determine

Only finding 01 survives as something two implementations could land on opposite
sides of, and I rank its plausibility **moderate**. The eager design in §5 is the
one a reader written straight from §19.3 falls into, since §19.3 already makes it
compute the decoded size at layer access for the overflow check; the lazy design
is the one a reader written straight from §19.4 falls into. Both are natural. What
makes me hold the plausibility at moderate rather than high is that the sentence's
own gloss points hard at reading A, so an implementer who reads §21.9's paragraph
at all will probably get there — the divergence needs one implementer who read the
table and `[R-ERR-04]` without the paragraph, which is exactly the population the
paragraph was added for.

Finding 02 is a register and corpus defect, not a fork, and I say so.

**What I could not determine.** Whether the two changed passages were meant to
settle the addressed-versus-stored question and merely under-shot the wording, or
whether the maintainer intends "actually contains" to mean stored and the
`[R-COD-07]` analogy to be read narrowly. I have no access to the reasoning and
did not look for it; the finding is written to be judged on the text alone.

**What I want on the record as a negative result.** I built two non-trivial
conforming files, one of them exercising planar mixed types, packed boolean
planes, edge padding under two fill values, a two-run slab with an alignment, and
a user-metadata extent, and the document determined every single byte. I ran the
overlap taxonomy, the reserved/experimental matrix in every position and flag
combination, the full boundary sweep, the reader/verifier seam, and the
degenerate-file family, and found the text closed in all of them — usually by a
clause written specifically for the case I was attacking. The two findings above
are the whole of what I have.
