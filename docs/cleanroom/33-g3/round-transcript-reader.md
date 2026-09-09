# Round 33 — Reader implementer, working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full, in five sequential reads (lines 1–400, 400–800, 800–1198, 1199–1598,
1598–1997, 1998–2417, 2418–2837, 2838–3257, 3258–3657, 3658–4057, 4058–4457,
4458–4805). I opened no other file, ran no `git` command, listed no directory,
and made no network access.

I wrote and ran three files, all in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-round/scratch/reader/`:

- `crc_check_rdr.py` — my own CRC-32C (table built from the reflected
  Castagnoli polynomial 0x82F63B78) and every stated constant re-derived.
- `count_register_rdr.py` — mechanical count of the §21.2–§21.5 register rows
  and of the semicolon-separated instances in each Instances cell.
- `build_file_rdr.py` — a complete conforming one-layer, one-stored-tile TARN
  file built from the document alone and then walked through my reader.
  It also wrote `built.tarn` in that same directory.

I named those files with a lane-specific suffix precisely because a prior round
lost an agent's script to a filename collision. Nothing of mine lives outside
that directory except this transcript.

**Context I did not ask for.** My runtime placed a project instruction file
(`CLAUDE.md`, which only forwards to `AGENTS.md`) and an index of the
maintainer's auto-memory notes in my context before I began. The memory index
carried titles that reference this project's harness, its gates, and prior
rounds' lessons. I did not open any of the files it names, and I have not used
any of it as evidence about the specification; I disregarded it. I report its
appearance here as the brief requires.

**Paths.** The specification was exactly where the brief said it was. My
scratch directory did not exist; I created it. The output directory
`.../r33-round/out/` did not exist either and I created it in order to write
this file; I did not list or read it.

---

## 1. What I built

I implemented, on paper, a conforming reader, in the order I would write the
code: constants and CRC first, then the open path, then validation timing,
then layer access, then the tile-read algorithm, then the degradation walks.
At every step I stopped and asked whether the document told me what to do.

### 1.1 Constants — every one I could check, checked

My CRC-32C is built from scratch: reflected Castagnoli 0x82F63B78, init
0xFFFFFFFF, final XOR 0xFFFFFFFF, little-endian storage, per `[R-ENC-09]`.
Results, mine on the left, the document's figure on the right:

| Quantity | I derived | Document states | § |
|---|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283`, stored `83 92 06 E3` | `0xE3069283`, `83 92 06 E3` | §4.5 |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` | §4.5 |
| CRC-32C(4 sentinel entries, 80 bytes) | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955`, `55 49 A3 80` | §7.4 example |
| crc_of_crc_array over `55 49 A3 80` | `0xC4EE982E`, stored `2E 98 EE C4` | `0xC4EE982E`, `2E 98 EE C4` | §7.4 example |
| CRC-32C(2¹⁶ sentinel entries) | `0xEECB3BB2` | `0xEECB3BB2` | §15.4, App. B |
| Appendix A trailer CRC over [0,60) | `0x402F157E`, stored `7E 15 2F 40` | `0x402F157E`, `7E 15 2F 40` | App. A |

I reconstructed Appendix A's 128-byte hex dump byte for byte from the field
table (magic, `01 00`, `00 00`, `00 00 00 00`, dir_offset 16, dir_length 4,
committed_file_length 128, file_id 0x0123456789ABCDEF, twelve zero bytes) and
compared: bytes [64,124) of the dump equal my constructed trailer exactly, the
stored CRC field equals my computed one, the directory region [16,20) is four
zero bytes as the CRC of a zero-byte record sequence requires, and F mod 64 = 0.

I also re-derived the worked arithmetic:

- §7.4's layer-record example: name 4 bytes, nine scalars layout→C
  1+2+2+2+8+8+8+1+2 = **34**, dimension entry 2+8+8 = **18**, channel entry
  5+2+5 = **12**, trailing fixed 1+8+4 = **13**; 4+34+18+12+13 = **81**, the
  stated inline_length, and every hex-dump offset in that block lands where
  those widths put it. `[R-CNT-17]`'s extent length 4·20 + ⌈4/2¹⁶⌉·4 = **84**.
- §11.2/§11.4: G = (4,8), N = 32, P = 65,536; (300,700) → tile (1,2), s = 10,
  in-tile (44,188), ordinal 44·256+188 = **11,452**; planar C = 4 channel 2 →
  disk ordinal **74**; its entry at region bytes [**1,480**, **1,500**);
  channel 3's entries **96–127**.
- §15.4: entry_count 1,000,000 → **16** segments, last covering **16,960**
  entries, CRC array **64** bytes, region **20,000,064** bytes; k = 999,999 in
  segment 15 at segment-relative byte **339,180**; CRC array at
  [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000); a full
  segment is 1,310,720 bytes = **1.25 MiB**.
- §14.3: planar bool P = 10 alternating → byte 0 = `0x55`, byte 1 = `0x01`
  with fill false and `0xFD` with fill true.
- §17.3: the shuffle of `00 00 80 3F 00 00 00 40 00 00 40 40` at s = 4, n = 3
  is `00 00 00 00 00 00 80 00 40 3F 40 40`, matching.
- §14.2's three worked layouts (Q = 3 decoded 18; planar `b` 12 bytes with
  ordinal 5 at bytes 10–11; Q = 5 decoded 30 with ordinal 5 at [25,30)) all
  reproduce from the table's formulas.
- §14.5: extents (5,5), tiles (4,4) → 32-byte edge tile, value 0 real,
  values 1–15 = `CD AB`.
- §20.3's example: 32·20 + 4 = **644**.
- §21.9's note: 2³² entries → 2¹⁶ segments × 4 = **256 KiB**; 2³⁶ → **4 MiB**.

**Not one stated constant, offset or checksum in this document is wrong.** I
consider that a meaningful negative result: it is the first thing a reader
implementer would trip over, and there is nothing to trip on.

### 1.2 Register arithmetic

I extracted every row of §21.2–§21.5 mechanically (a line beginning `| F`/`L`/
`T`/`R` followed by digits and `|`), took the third cell as Instances, and
counted semicolon-separated items, treating a cell reading `—` as one instance
exactly as §21.1 directs ("a cell reading — is one instance; the count is
therefore mechanical once the cell is written").

- §21.2: **35** rows (F1–F36 less the struck F11), **56** instances. Heading
  says 35. ✔
- §21.3: **49** rows, **116** instances. Heading says 49. ✔
- §21.4: **26** rows, **55** instances. Heading says 26. ✔
- §21.5: **10** rows, **50** instances. Heading says 10. ✔
- Totals: **120** rows, **277** instances. §21.8 says "120 conditions over 277
  instances". ✔

I also checked identifier hygiene: 162 distinct `[R-…]` identifiers; every
bare `R-XXX-NN` citation inside a Governing-rule cell matches a bracketed
identifier; every prefix numbers contiguously from 1 with no gaps
(`ENC` runs 1–16 plus the illustrative `[R-ENC-100]` of §2.2, and `SER-4` is
the withdrawn one §14.4 names); every `§N.M` reference in the document
resolves to an actual heading (no dangling section reference anywhere); and
the only register-row label referenced without a defining row is **F11**,
which §21.2's Note strikes deliberately.

---

## 2. The open path, byte-exact

### 2.1 Cold remote open against a ranged server

**Request 1** — suffix range, last 64 bytes. Bounded before reading by a
constant: the trailer is 64 bytes at `F − 64` in *every* format major
(`[R-CNT-24]`), so 64 is not derived from anything in the file. The response
also carries the transport-authoritative F (`[R-CNT-10]`), which is why §19.1
says steps 1 and 2 "cost one request between them". If the transport gives a
200 instead of a 206 the reader must abort or deliberately accept the whole
body and must never treat a body prefix as the requested range
(`[R-CNT-10]`); if the transport has no suffix ranges it SHOULD probe the size
and issue an absolute range.

Then §6.2's ordered gate, and the order is normative: magic; trailer CRC;
version gate; and only then, "those gates passed", the field gates — flags,
`committed_file_length` against the transport size and mod 64, dir_offset ≥ 16,
dir_length ≥ 4, dir_offset + dir_length ≤ F − 64 (a designated
declaration-derived sum under `[R-ENC-04]`), file_id ≠ 0, reserved zero.
`[R-ENC-10]` is what makes the first three legal before the CRC: comparing a
field against a constant "is not acting on it", and §6.2's explicit order
governs anyway.

**Request 2** — `[dir_offset, dir_offset + dir_length)`. Both halves come from
a trailer whose CRC has verified, which is what `[R-ENC-05]` requires before
issuing I/O on a file-derived integer. Verify the region's final four bytes
against the CRC of the preceding `dir_length − 4` (`[R-CNT-11]`), then parse.

**Total: two requests, `64 + dir_length` bytes.** For Appendix A's file that is
64 + 4 = **68 bytes**. For the file I built in §4 below it is 64 + 109 =
**173 bytes**. Nothing else is fetched: `[R-RDR-01]` says the open "consumes
the trailer and directory only — no extent slot's content, no tile index, no
payload", at any layer count and file size.

The front signature block is **not** in that accounting. `[R-CNT-04]` keys the
obligation to *residency*, not transport: a reader whose open leaves [0,16)
resident MUST check it by byte equality before other processing; one that would
need another range request MAY defer or omit. A remote reader speculating a
suffix window that reaches offset 0 is therefore bound. Appendix A works this
through correctly for its own 128-byte file: a 112-byte window over [16,128)
captures the directory (so request 2 is spared by §6.4's containment test)
while leaving [0,16) non-resident, so the block check stays optional.

### 2.2 What bounds each range before I have read it

- Request 1: the constant 64 (`[R-CNT-24]`).
- Request 2: dir_offset and dir_length, each range-checked by §6.2 against F
  before use, and their sum overflow-checked under `[R-ENC-04]`.
- Index CRC array and index segment (first tile read): computable "from the
  layer record alone" (`[R-IDX-04]`) — the extent slot plus entry_count, and
  `[R-CNT-17]` has already tied entry_count to extent_length and `[R-CNT-13]`
  has tied extent_length to F. §22.2's Note states exactly this chain.
- Tile payload: the entry's offset and length, covered by a segment CRC that
  step 3 has already verified.

I could not find a single fetch a conforming reader issues on an unverified
integer. That is a real property of this document and it took work to build in.

---

## 3. Validation timing by tier

§19.2 fixes the **latest** detection point, four tiers plus *certification*:

- **open** — front block (if resident), trailer, directory region, record walk,
  layer-name namespace.
- **layer access** — the full §19.3 validation of that layer's record, before
  any use of its declarations other than the name.
- **tile use** — index chain, payload CRC, decode checks.
- **extent use** — the extent's CRC and the document content rules §18.2
  attaches at that encoding.

A reader may **never** check: anything whose Detector cell reads *verifier*.
By my extraction those are F7, F25, F26, F27, F28, F33, F36; L18, L25, L40,
L41, L42, L46, L47, L48, L49; T2, T4, T5, T26. Plus the live-state coverage
partition and slack total (§9.7), extent overlap (§7.2), and the front block
where the reader does not hold it resident.

I cross-checked §19.3's enumeration against every L-row in §21.3 and found no
layer-scope reader-detected row it fails to reach: L27 and L28 are named
directly, L29/L30/L39 fall under "the §7.4 constraint set (`[R-CNT-23]`)",
L31/L33/L34/L36/L43/L45 under "the value sets of §11.4, §12.2, §14.1, §15.1,
§17.2, and §17.3", L44 under "the codec declaration bounds (`[R-COD-07]`)",
L21/L22 under "the index cross-checks computable without I/O", L1 under
`[R-ENC-03]` and L2 under `[R-ENC-04]`/`[R-SER-02]`/`[R-SER-07]`. L3/L5/L6 are
at *open* because §19.1 step 4 parses the layer name there, and §19.3 says so
in as many words ("other than its name, whose parse §19.1 step 4 places at the
open").

Where a check is not restated, §19's preamble carries it: "A row this section
does not restate is due at its own tier all the same, with its governing rule's
own outcome." I relied on that for R1's encoding-byte value set (tier: open for
a top-level record, layer access for a sub-record), for F2/F3's u64 domain and
sum checks on non-layer top-level records, and for T14's codec-1 length
equality.

---

## 4. A file I built, and walked

To test whether the document really suffices I built a complete conforming
file from it alone — not Appendix A's empty one, but the §7.4 example layer
with a tile actually stored, so that the whole index chain, the codec-1 length
rule and the fill path all get exercised.

Declarations: layer `sst`, interleaved, linearization 1, codec 1, filter 1,
A = 0, S = 0, A_slab = 0, rank 1, C = 1, dimension `x` with E = 100, T = 32,
channel `temp` type 12 (float32), fill `00 00 C0 7F`.

Derived: G = (4), **N = 4**, **P = 32**, **Q = 4**, entry_count = **4**,
decoded size P·Q = **128** bytes. Index region 4·20 + ⌈4/2¹⁶⌉·4 = **84** bytes,
matching `[R-CNT-17]`. inline_length **81**, matching §7.4's worked example
byte for byte in its field widths.

Placement I chose (placement is free — `[R-SLB-05]`):

```
[0, 16)      front signature block
[16, 144)    stored tile, disk ordinal 0, 128 bytes   (entry: off 16, len 128,
                                                       crc 0x2CD1D07E)
[144, 228)   tile-index region: 4×20 entry array + one 4-byte segment CRC
             segment CRC array = D4C6BB3C  ->  crc_of_crc_array = 0x4AACA874
[228, 337)   directory: one layer record (24-byte header + 81 inline) + 4-byte CRC
[337, 384)   pre-trailer pad, 47 bytes of slack
[384, 448)   trailer.   F = 448,  448 mod 64 = 0
```

Entries 1, 2 and 3 are the sentinel `FF ×16 00 ×4`.

**The walk.** Step 1: transport size 448. Step 2: fetch [384,448); magic
matches; trailer CRC verifies; version 1.0; flags 0; dir(228,109); cfl = 448 =
size and 448 mod 64 = 0; 228 ≥ 16; 109 ≥ 4; 228 + 109 = 337 ≤ 448 − 64 = 384;
file_id ≠ 0; twelve reserved bytes zero. Step 3: fetch [228,337); directory CRC
verifies. Step 4: one record, type 0x0001, flags 3 (MU = 1, PE = 1 — the values
§7.3 fixes), inline_length 81, extent (144, 84). One layer name, `sst`, unique,
well-formed, non-empty, no C0 code points.

Layer access: §19.3's whole list passes, including `[R-CNT-17]`'s two
cross-checks — entry_count 4 equals the geometry-derived addressed-tile count
N = 4 (interleaved), and extent_length 84 equals the formula.

Point request x = 5. Step 2: tile coordinate 5 div 32 = 0, in-tile position
5 mod 32 = 5, spatial ordinal s = 0, disk ordinal 0 (interleaved). Step 3:
fetch the 4-byte CRC array at [228−84+80 …] — concretely region bytes
[80, 84), i.e. file [224, 228) — and verify against crc_of_crc_array; fetch
segment 0, region bytes [0, 80), file [144, 224), and verify against the array's
u32. Both pass. Step 4: entry is (16, 128, 0x2CD1D07E) — non-sentinel, offset
≥ 16, length ≠ 0, neither field the sentinel, sum 144 ≤ 384. Codec 1 so
`[R-COD-04]` applies before any payload fetch: length 128 must equal the decoded
size 128 — it does. Step 5: fetch [16,144), CRC verifies. Step 6: codec 1 is
verbatim, filter 1 is identity, decoded length 128 = decoded size
(`[R-SER-07]`). Step 7: `[R-SER-02]`'s interleaved offset with C = 1 gives
`(k div 1)·4 + F⁰ = 5·4 = 20`, so the float32 sits at decoded bytes [20,24).
Step 8: return those four bytes unaltered.

Point request x = 99. Tile coordinate 3, in-tile 3; entry 3 is the sentinel, so
step 4 short-circuits 5 and 6 and returns the recorded fill `00 00 C0 7F`
bit-exactly, with **no payload I/O**. Tile 3 addresses coordinates 96–127, of
which 100–127 are padding positions; a reader never returns them
(`[R-GEO-04]`), and because tile 3 is unstored there is no stored padding
content for `[R-SER-05]` to constrain.

**Cold cost for that one tile:** 4 bytes of CRC array + 80 bytes of segment
+ 128 bytes of payload, on top of the 173-byte open. §15.4's guarantee — never
more than one full segment (1.25 MiB) plus the CRC array — holds trivially here
and is the term §21.9's 2³² entry_count guarantee is sized against.

The document determined every one of those steps. I had to guess nothing.

---

## 5. Degradation walks

**(1) Unknown top-level record type 0x8000, MU = 0.** Open step 4 parses it;
`[R-CNT-15]` gives ignore-record; §21.6's table records the file as conforming
(§10.3's prohibition on publishing experimental values binds the writer's
conduct, not the bytes, `[R-CNF-02]`). Its extent slot is still checked, and a
malformed slot on a non-layer top-level record is reject-**file**
(`[R-CNT-13]`: "the file for other top-level records"). Its extent is covered
by no checksum at all (§8.1's last row), which §22.3 names as one of the four
stated residues. An updater re-emits it byte-identically or, at PE = 0, may drop
it (§20.4). A compactor may relocate it, which is exactly what §7.2's
no-embedded-offsets rule for MU = 0 records exists to make safe. Everything
else in the file is served normally.

**(2) Unknown codec value 0x8000 on layer B of a two-layer file.** The open
completes — codec lives in the layer record's inline payload and §19.3 places
value-set checks at layer access, not open. First access to B: `[R-COD-03]` →
validity error at layer scope → **reject-layer** (L43, reader, layer access).
Layer A is unaffected and fully readable; §2.4 lets me still list B's name. A
verifier reports *nonconforming*, not *cannot establish*: §17.4 is explicit
that the cannot-execute position arises for a conforming reader "only at a
reserved or experimental value", where it rejects the layer instead.

**(3) Truncated / extended tail.** Physical file 458 bytes for my F = 448 file:
step 1 gets 458, step 2 fetches [394,458), the eight bytes at 394 are tile or
index bytes, not `8A 4E 52 41 54 0D 0A 1A` → F8 → **reject-file**, and
`[R-LIF-05]` forbids scanning backward. §9.5's Note is explicit that residue
past a completed commit carries no register row of its own: a reader "cannot
tell residue from corruption and is not asked to". Truncated to 400: [336,400)
likewise fails the magic, or if it did not, F17's cross-check of
committed_file_length against the transport size catches it. Recovery is §9.6's
deliberate operation and is not a reader behavior.

**(4) Tile CRC mismatch.** Open and layer access pass. At step 5 the computed
CRC over [offset, offset+length) differs from the entry's crc → T1 →
**reject-tile**. The read of that tile reports failure and `[R-CNF-09]`
forbids returning fill in its place; `[R-TYP-09]` says the same from the other
side ("Fill is produced by exactly one condition: a sentinel entry read from a
verified index chain"). Neighbouring tiles are unaffected. For a region request
step 8 lets me either return the validating entries' values with a per-entry
report or fail the request whole — but never substitute fill. §15.3 also tells
me this entry stays *well-formed*: its extent still stands, so it still counts
in the verifier rows, in slab run continuity, and in the coverage walk.

**(5) Limit exceeded — entry_count = 2³³.** §21.9's guarantee is 2³². The file
"remains conforming, and a reader MAY decline it" at the narrowest scope whose
quantities exceed what it can serve — here the layer — or any scope containing
it, up to the file. The refusal **MUST** be reported as a resource limit and
not as a validity error (`[R-ERR-04]`). A verifier that declines the layer on
that ground never enumerates its claimants, so its slack total is reported as
**partial**, an upper bound, naming what stopped the walk (`[R-CNT-21]`), and
it cannot certify.

**(6) Format major 2.** Magic and trailer CRC still bind: §2.3 derives, and
§21.2 restates, that exactly F8, F14, F6 and both of F1's instances reach a
foreign major, each asserting an invariant `[R-CNT-24]` fixes permanently.
F6's residency exemption survives, because it is granted "on a ground other
than the declared major". If all reaching conditions pass, the reader rejects on
**capability** grounds with a diagnostic distinct from both "not a TARN file"
and "corrupt" (`[R-CNT-07]`). A verifier that does not implement major 2 and
established no violation reports *cannot establish*. F18 (version_major = 0) is
outside the premise entirely: it declares no major at all.

**(7) User metadata under an unimplemented experimental encoding 0x80.** Open
checks the record's framing — no (0,0) slot, extent_length ≥ 5, inline_length
exactly 1. The encoding value is experimental, so the record is
**ignore-record**, SHOULD be reported, and the file stays conforming: §21.6's
row and `[R-MTA-10]` agree that no document rule attaches. But the structural
checks that *precede* the document still bind, and a verifier must still verify
the extent's terminal CRC (§8.1's map, §9.7's walk) — a failure there is R2, a
real violation at ignore-record. §22.3 names the resulting hole honestly: the
certificate covers those bytes uninspected, which is why `[R-MTA-10]` obliges
the verifier to name each such record with its scope, encoding value and stored
extent length.

**(8) Layer sub-record of an unknown type with MU = 1.** `[R-CNT-18]`:
reject-**layer**, and "where the file is otherwise conforming a reader MUST NOT
reject the file for it". §21.6's closing paragraph is where the asymmetry is
stated — the same type at top level is the one case where a conforming file is
refused whole. So this is a conforming file from which a conforming reader
serves nothing of one layer. I checked and that is consistent: §2.3's acceptance
duty is qualified only on *top-level* MU = 1 records.

---

## 6. Where I pushed hardest, and what closed each suspicion

I read the fifteen named passages first and then went back over §14–§17, which
the surface does not touch and which my charter runs straight through.

### 6.1 §20.3's qualified closed list

This is the passage the brief points at hardest, so I did the exercise the
brief prescribes: derive the members from §7.4's structure myself, put each on
exactly one side, then take them in pairs.

§7.4's declaration fields are: name; layout; linearization; codec; filter;
alignment A; slab S; slab alignment A_slab; rank d; channel count C; per
dimension a name, extent and tile extent; per channel a name, type and fill;
index_encoding; entry_count; crc_of_crc_array; sub-records.

Permitted side: name; dimension and channel names; an extent (grow only);
a planar layer's channel list (extend at end / shorten from end); slab and
alignment declarations. Fixed side: layout; linearization; index_encoding;
codec; filter; rank; dimension order; every tile extent; every channel's type
and fill; an interleaved layer's channel list bar names; the position of every
planar channel but the last. Accounted for separately: entry_count,
crc_of_crc_array and the extent slot "follow the commit"; sub-records are
§20.4's subject. **Every field lands on exactly one side, and the closing
sentence handles the three that appear on both — a dimension extent, a planar
channel list, an interleaved channel list — by saying the permitted side states
the whole of what a commit may do to that field.** I could not find a member on
neither side or a member on both that the closing sentence fails to route.

Pairs, and whether the text decides their composition:

- *name + anything*: a name "enters no map this specification defines", and
  the dimension and channel orders are positional, so two swapped names are
  explicitly permitted. Nothing composes badly.
- *growth + channel extension* (planar): growth changes N, extension adds
  ordinals `C·N′ + s` after every existing one. The claim "an appended planar
  channel adds tiles at ordinals after every existing one" stays true of the new
  state under the new N. Retained ordinals renumber, which is exactly what "a
  growth renumbers ordinals wherever `[R-GEO-06]` moves them" licenses.
- *growth + channel shortening*: removal takes only the removed channels'
  ordinals out; growth adds spatial tiles. Both justifications survive.
- *growth + slab or alignment*: `[R-SLB-04]` is triggered by "the disk ordinal
  of any tile the new state stores" changing, and step 4 says the invariant runs
  over "every one the new state keeps, not only those this commit adds". That
  is the sentence that makes the composition decidable, and it is there.
- *extension + shortening of one channel list*: the excepted pair.
- *alignment declared + slab declared*: `[R-CNT-16]` forbids both nonzero, and
  the paragraph "A permitted change holds provided the declarations and geometry
  it produces stay within every bound they are subject to … These bounds are not
  offered as exhaustive" reaches it.

I then tested each justification sentence against the composed cases, per the
brief's "a justification true of the pair the exception names and false of one
it does not":

- "a grown extent adds positions that held their channel's fill (§14.5)" — true
  whether the old edge tile was stored (its padding positions were fill by
  `[R-SER-05]`) or unstored (fill by `[R-TYP-08]`), and true when growth raises a
  grid count and adds whole new tiles.
- "an appended planar channel adds tiles at ordinals after every existing one"
  — `C·N + s ≥ C·N > (C−1)·N + (N−1)`. Holds under any N, so it survives being
  composed with a growth.
- "a channel removed from the end takes only its own tiles out of the addressed
  set" — retained `c·N + s` for `c < C′` are untouched; composed with a growth
  they renumber under `[R-GEO-06]`, which the same paragraph already licenses.
- "nothing else this step permits moves one [ordinal]" — I checked all four
  permitted changes: only a growth changes N or a grid count, so only a growth
  moves an ordinal. **True.** I also checked the sharper case: in a rank-2 layer
  a growth of the *first* dimension raises G₀ but leaves
  `s = t₀·G₁ + t₁` … no: it leaves `∏_{j>0} Gⱼ = G₁` unchanged, so s is
  unchanged and entries are only appended. Growing the *last* dimension moves
  them. "wherever `[R-GEO-06]` moves them" is exactly the right quantifier for
  that, and a weaker phrasing would have been wrong.

I then checked every restatement of this rule elsewhere in the document, by
searching the whitespace-normalised text for "channel list" (11 hits), "shorten"
(10), "extended at" (2), "in one commit" (5), "at once" (3), "stores a tile"
(6), "stores no tile" (2) and "re-declared" (3). The restatements are §11.1's
Rationale ("one or the other in a commit"), §20.3's own "what the line gives up"
list ("a planar channel list both extended and shortened in one commit are
rewrites"), §20.3's shape-(c) example, §23.1, and Appendix H's updater checklist
("not both in one commit"). **Every one carries the exception.** None carries
the unqualified form. That is the failure mode the brief warned about and it is
not present.

### 6.2 The finiteness test and its named reference

§18.2 now says a reader interprets every JSON number as "the IEEE 754 binary64
value its decimal text converts to under IEEE 754's default rounding-direction
attribute, roundTiesToEven", and Appendix F's IEEE 754 entry now names that
conversion. I opened what is named and asked whether it supplies exactly that,
for exactly the case at hand. It does: under roundTiesToEven, decimal-to-binary64
conversion of a magnitude at or above `2¹⁰²⁴ − 2⁹⁷⁰` yields infinity and below
it yields DBL_MAX, so the boundary case — `1.7976931348623158e308` and its
neighbours — is decided rather than left to a runtime's strtod. Before that
attribute was named, two readers could genuinely have disagreed about whether
such a document is R8, hence whether the file is conforming. `1e400` is called
out as the ordinary case and is unambiguous under any rounding attribute.
Underflow is untouched — a value rounding to zero or a subnormal is finite and
readable — and the "MAY hold the value so obtained in a wider representation"
clause does not reopen the conversion, because the conversion is specified *to*
binary64 first. I judge this repair sound.

### 6.3 §18.2's frame-constraint carry-over

The reference here is `[R-COD-06]`, and §18.2 carries it over "named here or
not, save two". I enumerated `[R-COD-06]`'s constraints and checked the
partition: frame magic, no skippable frame, no second frame, no dictionary
(disclosed or not), no nonzero dictionary ID, no content-checksum flag → carried
(and §18.2's "named for convenience, not as a closed list" is what makes the
"or not" safe); the window bound and the content-size-against-decoded-size rule
→ excluded and replaced. The replacement re-points the content-size rule from
"the tile's declared decoded size" to "the byte length of the decoded document".

I asked the brief's question 10 — which property of the old subject made the
rule true, and does the new subject have it? The old subject was
*declaration-derived*, so a reader could check it **before decoding**; the new
one is only known **after** decoding. R4's own text is where I expected that to
break, and it does not: it says a constraint of that row is "checkable from the
extent's bytes without relying on a decoder's tolerance", which is still true —
the decoded length is a deterministic function of the extent's bytes, and
nothing external is needed.

I then built the case I thought would fork: a document whose declared
content-size is wrong and whose decoded length exceeds the reader's own bound.
Reader A (16 MiB bound) declines on resource grounds; reader B (32 MiB bound)
establishes R4. Do their verdicts contradict? No — §18.2 says a *verifier*
declining on either bound "cannot establish that document's conformance and MUST
NOT certify the file", so verifier A reports *cannot establish* and verifier B
reports *nonconforming*, and §2.3 is explicit that *cannot establish* "is not a
finding that the file is nonconforming". The two are compatible. Closed.

I also checked the Window_Size interaction arithmetically: a 16 MiB document
framed with a Window_Descriptor needs only an ≤8 MiB window, so §21.9's two
rows compose; framed single-segment, RFC 8878 makes Window_Size the content
size, which §18.2 pins to the document's decoded length, so a >8 MiB document
framed that way exceeds §21.9's window row — and §18.2 says exactly that, and
tells the writer to use a Window_Descriptor instead. The parallel tile note in
§17.2 ("a tile whose decoded size is below 1 KiB … is encodable under codec 3
only as a single-segment frame") is the mirror case and is also right: the
Window_Descriptor cannot express less than 1 KiB.

### 6.4 §15.3's entry classification, exhaustively

I enumerated the classification myself over an arbitrary 20-byte entry and
confirmed it is total: all three sentinel values → valid sentinel; offset =
length = S with crc ≠ 0 → structural; exactly one of offset/length = S →
structural; otherwise non-sentinel, and then length 0, offset < 16, either
field above 2⁶³ − 1, and sum-overflow-or-past-F−64 → structural, else a
well-formed stored entry proceeding to the crc. Exactly **six** rows are marked
structural, as the paragraph says.

I checked the overlaps for a verdict fork and found none: an entry with
offset = length = S and crc ≠ 0 satisfies both the second row and the
"above 2⁶³ − 1" row, and both give reject-tile; T11's register row carries the
disambiguating qualifier "the value being distinct from the all-ones sentinel"
that the §15.3 table cell does not, and §21.1 says the rule governs where they
diverge — but since the outcome is the same either way, nothing moves.

I checked the T10/T14 pair against §21.1's specialization test and confirmed
they merely overlap rather than specialize: a zero-length non-sentinel entry
under codec 2 exhibits T10 without T14, and a length-5-against-128 entry under
codec 1 exhibits T14 without T10. So the register is right not to list them.

### 6.5 §8.1's coverage map

I checked "every field of every structure is covered by exactly one checksum"
against the exceptions §4.5 states, field by field: the front block (equality),
the three terminal checksum fields (trailer [60,64), the directory's final
four, a user-metadata extent's final four), and an unassigned type's extent.
The three interior checksum fields are each both comparison-verified and
covered once — a segment CRC array by crc_of_crc_array, an entry's crc field by
its segment CRC (it is part of the entry bytes), crc_of_crc_array by the
directory CRC (it lives in the layer record's inline payload). The layer
record's extent slot, entry_count and index_encoding all sit inside the
directory region and are covered by the directory CRC. The pre-trailer pad is
slack and by construction not a structure. I found no field with two checksums
and none with zero that the exception list does not name.

---

## 7. Findings

Three, all honestly graded. None is byte-level, and I say why for each.

### reader-01 — OBSERVATION — §19.1's consolidated open path omits the 128-byte floor before it directs the reader to compute `F − 64`

**Location:** §19.1 steps 1–2 (`[R-RDR-01]`); §5.1 (`[R-CNT-27]`); §21.2 row F5.

**Quotation** (§19.1):

> 1. **End of file.** Obtain the transport-authoritative file size F
>    (`[R-CNT-10]`). …
> 2. **Trailer.** Fetch bytes [F − 64, F) and validate them in §6.2's fixed
>    order …

and (§5.1):

> No conforming file is shorter than 128 bytes … A reader MUST treat a shorter
> file as a validity error at file scope. `[R-CNT-27]`

**Detail.** §19 announces itself as "the reader's normative path" and its steps
are "in order". Step 2's range expression is not well-defined for F < 64: the
lower bound is negative. F5 is a reader-detected row whose Detected cell is
*open*, and §19's preamble routes any unrestated row to its own tier — so the
check is owed at the open — but §19.1 restates a great many checks that §21
also carries (the MU gate, multiplicity, extent-slot validity, the user-metadata
framing trio, duplicate names) and does not restate this one, which is the only
one step 2's own arithmetic depends on. An implementer following §19.1 literally
computes `F − 64` on a 30-byte file before anything has told it to stop. The
permitted readings are (a) the floor is due somewhere in the open and an
implementer must find it in §5.1/§21.2, or (b) step 1 implicitly includes it. I
picked (a), because §19's preamble says so in terms. What an implementer does
wrong without it is an underflowed range computation on a hostile short file —
in a document whose §22.2 is otherwise scrupulous about never sizing I/O from an
unvalidated quantity.

**Byte-level: no.** Both readings reject the file; only the point at which the
rejection is reached differs, and no file's accept/reject verdict moves.

### reader-02 — AMBIGUITY — §2.3's closed list of writer obligations "expressly declared not to be a file-conformance violation" omits §9.2's durability barriers, which §9.2 expressly so declares

**Location:** §2.3, `[R-CNF-02]`; §9.2, second paragraph after `[R-LIF-02]`.

**Quotation** (§2.3):

> A writer obligation whose violation this specification expressly declares not
> to be a file-conformance violation binds the actor in the same way; §6.3's
> flags rules against a set ignore-lane bit — a creator's flags = 0, and an
> updater's or compactor's copy-forward and set-no-other (§20.5) — and §6.2's
> pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this text
> states, and each is declared where it arises rather than enumerated here.

against (§9.2):

> A writer that omits a barrier violates this requirement as an actor, and the
> file it produces is never nonconforming by virtue of it, as `[R-CNF-02]` says
> of every conduct rule.

**Detail.** The class the §2.3 sentence names is "a writer obligation whose
violation this specification expressly declares not to be a file-conformance
violation". §9.2 makes exactly that express declaration about `[R-LIF-02]`
steps 4 and 6, and the list of "the cases this text states" does not include
them. Two readings. **Reading A:** the list is complete because the sentence's
class is implicitly restricted to obligations that *do* govern output — a set
ignore-lane bit and an over-long pre-trailer gap are both visible in the bytes,
whereas a barrier "leaves no trace in the bytes" and so is already covered by
the preceding sentence's conduct-rule category, which §9.2's own closing words
("as `[R-CNF-02]` says of every conduct rule") route it to. **Reading B:** the
class is as written, and the closed list is one member short. I picked A,
because §9.2 explicitly self-identifies as a conduct rule and the preceding
sentence of §2.3 is where conduct rules live — but the sentence gives the reader
no cue that its class excludes conduct rules, and it is the only closed list in
§2.3. An implementer building a conformance checklist from §2.3 alone would
either duplicate the barriers into the wrong bucket or, worse, conclude that a
barrier omission *is* a file-conformance violation because it is not on the list
of things that are not.

**Byte-level: no.** Under both readings a barrier omission binds the writer as an
actor and leaves the file conforming; §9.2 says so directly, and a barrier
leaves no trace in the bytes by construction, so no file's conformance changes.

### reader-03 — AMBIGUITY — §18.2's encoding layout table gives "Valid values: 1 or 2" for the one enumeration space in this document where an unassigned value is conforming

**Location:** §18.2, the `[R-MTA-03]` layout table; §21.6's experimental-encoding
row; §10.2.

**Quotation** (§18.2):

> | Offset | Size | Type | Field | Class | Valid values |
> |---|---|---|---|---|---|
> | 0 | 1 | u8 | encoding | structural | 1 or 2; see below |

against §21.6:

> | A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming — §10.3's
> prohibition binds a writer's conduct, not the bytes. …

**Detail.** Metadata encoding is the single numeric space in §10.2's table where
an experimental value in a file is *not* a validity error: `[R-EXT-03]` routes it
to "ignore-record under the quarantine (`[R-CNT-25]`), never a scope-level
rejection", and §21.6 records the file as conforming. Every comparable cell
elsewhere in the document spells that kind of thing out — §7.4's index_encoding
row enumerates "0, reserved 2–0x7F, and the experimental range ≥ 0x80" and says
each is a layer-scope error, and §6.2's flags row says in the cell itself that a
set ignore-lane bit is ignored. Here the cell says only "1 or 2". The readings
are (a) the Valid-values cell states the field's file-conformance-valid set, in
which case it is wrong, since ≥ 0x80 is conforming; (b) it states the *assigned*
set and defers everything else to "see below". I picked (b) — the pointer is
right there and the very next sentence partitions the space correctly. But (b)
makes this cell mean something different from the same column in §6.2, §7.4 and
§15.1, and the actor it would mislead is a verifier: a verifier implemented from
the table would report *nonconforming* for a conforming file, whereas a reader
so implemented lands on ignore-record either way, because `[R-CNT-25]` gives an
encoding "one the reader does not implement" the same outcome.

**Byte-level: no.** The prose immediately below the table, §10.2, `[R-EXT-03]`,
§21.6 and `[R-MTA-10]` all decide it the same way, and the cell's own "see
below" points at them. A verifier that got it wrong would be wrong under the
document, not licensed by it, so the accept/reject set does not move.

---

## 8. Suspicions I opened and closed

Recorded because a clean lane has to show it looked.

- **"declared, re-established or cleared" for a slab or alignment declaration
  (§20.3 step 4)** — does that permit *changing* A from 4096 to 512, or only
  declaring/clearing? Closed by `[R-SLB-04]`, which triggers on a commit that
  changes "the slab declaration itself", and by step 4's own closing clause "an
  aligned layer's stored tiles — every one the new state keeps, not only those
  this commit adds — satisfy its invariant or the declaration is cleared", which
  is written for a *new* invariant. Both presuppose a value change is available.
- **Replacing the last planar channel across two commits** — commit 1 shortens,
  commit 2 extends with a different type. Does that reinterpret stored bytes?
  No: commit 1 takes the removed channel's tiles out of the addressed set and
  strands their extents as slack, so commit 2's new entries are "new to this
  generation". §20.3 names this as the sanctioned route ("is two commits or a
  rewrite"), and it is genuinely sound.
- **Codec 4's cap under a permitted change** — appending a float64 plane to a
  planar uint8 layer can raise the largest plane's decoded size past
  `0x7E000000` while no existing plane exceeds it. Closed by §20.3's "A
  permitted change holds provided the declarations and geometry it produces stay
  within every bound they are subject to: `[R-COD-07]`'s lz4 decoded-size cap
  (L44, the largest channel plane governing in a planar layer)".
- **§19.2's "no earlier, since the open fetches no extent"** against "A reader
  MAY detect any violation earlier (`[R-CNF-12]`)" two sentences later. Closed
  by reading the paragraph: the Rationale says the rule "fixes the *latest*
  detection point", so "no earlier" is a statement about what the open's tier
  can reach, not a bar. I would have filed this had I stopped at the sentence.
- **§21.1's "`[R-SER-08]` is the one rule that goes the other way"** — is
  `[R-CNT-12]`'s "MUST treat the record as PE = 1" not also a resolution of a
  stored bit? Closed: §21.1's claim is about *the reader that serves the
  structure*, and PE binds an updater's disposal, not what a reader serves;
  `[R-TYP-04]` scopes "the one case" to sample values, where it is true.
- **§23.1's "no commit turns a real position of a stored tile into padding"** —
  I checked all four permitted changes. Growth turns padding into real, never
  the reverse; a channel shortening removes whole tiles; names and
  slab/alignment touch no coordinate. A shrink would, and it is a rewrite. True.
- **§13.3's and §11.1's "a growth that raises a grid count while another stays
  0"** — verified: `Gᵢ = ⌈Eᵢ/Tᵢ⌉` is 0 exactly when `Eᵢ = 0`, so the product
  holds at 0 and entry_count stays 0 under either layout. Also verified that
  such a layer stores no tile, so it is freely re-declarable anyway.
- **§14.4's "At P = 1 … the images coincide exactly when that fill is false"**
  — computed both: planar `⌈1/8⌉ = 1` byte with seven pad bits at the fill bit
  versus one interleaved byte. They coincide iff fill is false. True.
- **§17.3's "The decoded image's length L is divisible by s in every case"** —
  checked all three layouts: `P·Bᶜ / Bᶜ`, `P·Q / Q`, `⌈P/8⌉ / 1`. True.
- **Whether a reader must be told what representation to hand back for a packed
  planar bool sample** — decided out of scope: §2.1's Note and §2.4's Note both
  put representation and reporting on the implementation-technique side, and
  §13.2 fixes the one encoding of a bool value that this format stores.
- **§15.3's structural rows overlapping T11's register row** — same outcome
  under either, so no verdict moves.
- **R5 against R7 (ill-formed UTF-8 in a document is also not well-formed
  JSON)** — §21.1's specialization rule routes the file to the narrower row,
  and the unpaired-surrogate instances make R5 reachable without R7. Both are
  ignore-record, so nothing moves either way.
- **F5's non-reach into a foreign major** — checked §2.3's Note's reasoning
  independently: `[R-CNT-24]` fixes the trailer's position, size and CRC but not
  64-alignment of F, and fixes no directory at all, so the 128-byte floor is
  format major 1's. The Note is right.
- **§21.1's specialization list** — verified each named pair really does have
  the containment property (F21 ⊂ F22 because a (0,0) slot has extent_length 0;
  L10 ⊂ L11 likewise; F35 ⊂ F36; L24 ⊂ L25; F1's two instances into F6 and F8).
- **§21.6's table not carrying a row for an experimental MU = 1 *sub-record***
  — §21.1 excludes §21.6 from the completeness clause, and the closing paragraph
  names the case explicitly. Not an omission.

## 9. Verdict

The document sufficed for everything my charter names. I built a conforming
file from it alone and read the file back with no guesses; every stated
constant, offset, size and checksum I could compute reproduced exactly; the
register's own counts reproduced exactly; every cross-reference resolves. The
§20.3 surface — the qualified closed list — survived the pairwise composition
test I was asked to run against it, and its five restatements elsewhere all
carry the qualification. The §18.2 and Appendix F work on the rounding attribute
closes a reading that would genuinely have forked verdicts on boundary-magnitude
JSON numbers.

I found no byte-level fork. I file three non-byte-level findings and record
above the fifteen suspicions I opened and closed, including one — §19.2's "no
earlier" — that I would have filed had I not read the sentences around it.
