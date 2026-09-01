# Round 28 — Reader implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,648 lines — the brief said 4,649; I counted 4,648 with `wc -l`, which counts
newline-terminated lines, so this is almost certainly the same file with no
trailing newline on the last line, not a different document). It was where the
brief said it would be.

I ran `ls` on `spec/` once, before I had internalised the access rule, and saw two
entries: `registry.json` and `tarn.md`. I did not open `registry.json` and I did
not list any other directory. I disclose it because the rule says to.

Context I did not ask for: my runtime placed a project-instruction preamble
(`CLAUDE.md` pointing at `AGENTS.md`), a git status snapshot with five recent
commit subject lines, and a user-email/date block into my context before I began.
The commit subjects name round numbers, ADR numbers and, in three cases, the
substance of recent changes. I did not act on any of it, and I have not repeated
its contents here beyond saying that it appeared. I note specifically that I did
**not** use it to locate the format change; the brief itself told me a structural
field had been removed from a fixed-size structure, and §6.2's layout table plus
§3.1's "No field numbers generations" told me which one.

Computation: I wrote two throwaway Python scripts in my scratchpad
(`crc.py`, `crc2.py`) implementing CRC-32C from the polynomial in §4.5 and fed
them byte strings I transcribed by hand from the document. They read no files
except each other. I also ran `grep`/`awk` over `spec/tarn.md` only.

No web access, no git history, no ADRs, no conformance corpus, no registry.

---

## 1. How I worked

I read the document straight through in eight chunks, then went back over it as an
implementer: open path, validation tiers, layer access, tile read, degradation,
worked example. Along the way I ran mechanical sweeps (§2) and recomputed every
number I could (§3). Findings are in §7.

The brief told me a structural field had been removed from a fixed-size structure
and that the fields after it had moved without the structure shrinking. §6.2's
trailer is 64 bytes with `file_id` at 40 and a **12-byte** reserved run at
[48, 60). §3.1 says "No field numbers generations; successive generations of one
file are ordered by the strictly increasing committed file length their trailers
carry". Appendix D says the format has "no counter in the trailer numbering the
commits". So the removed field was a generation counter, `file_id` moved down to
40, and the freed 8 bytes went into `reserved`, which grew from 4 to 12. §21.2's
struck row label F11 is where its register row used to sit. The new property the
document now asserts of `committed_file_length` is **strict increase per commit**
(§9.2 `[R-LIF-02]`, §9.3 `[R-LIF-03]`). That framing drove most of my shape-10
checking.

---

## 2. Mechanical sweeps

Each of these was run against `spec/tarn.md` alone.

**S1 — requirement-identifier census.**
`grep -o "R-[A-Z]\{3\}-[0-9]\{1,3\}" | sort | uniq -c` → 165 distinct identifiers.
Prefix ranges, with no gaps except one:
CNF 01–13, CNT 01–27, COD 01–11, ENC 01–16 (+ ENC-100, which is §2.2's worked
illustration of "numbers above 99 extend naturally", not a requirement),
ERR 01–05, EXT 01–05, GEO 01–06, IDX 01–05, LIF 01–08, MDL 01–02, MTA 01–10,
PRV 01–05, RDR 01–04, SEC 01–07, SER 01–09, SLB 01–05, TYP 01–10, VEC 01–04,
WRT 01–09. The one anomaly is `R-SER-04`, which occurs exactly once, in §14.4's
Note declaring it withdrawn — which is what §2.2 prescribes. **No dangling
citation to an undefined identifier, and no identifier defined but never cited
that isn't simply a leaf requirement.**

**S2 — prefix table vs. prefixes actually used.** §2.2 tabulates 19 prefixes;
the 19 in use are exactly those. No unlisted prefix, no listed-but-unused prefix.

**S3 — register row count.**
`awk -F'|' '/^\| (F|L|T|R)[0-9]+ \|/'` over the four register tables:
F1–F10 + F12–F36 = **35** (§21.2 says 35 ✓; F11 struck, and §21.2's closing Note
says so deliberately), L1–L49 = **49** (§21.3 says 49 ✓), T1–T26 = **26** (§21.4
says 26 ✓), R1–R10 = **10** (§21.5 says 10 ✓). Sum **120**, matching §21.8's
"120 conditions".

**S4 — register instance count.** Same awk, splitting each row's Instances cell on
`;` and counting `—` as 1, per §21.1's stated mechanical rule. Per-row counts
came out as: F 2,5,2,1,2,2,4,1,1,1 / 1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,3,2,1,1,5,1,1,1;
L 8,9,1,2,1,1,2,2,2,1,1,2,1,3,4,2,2,3,1,1,4,4,4,1,1,1,1,1,3,2,3,3,4,4,1,2,1,1,3,1,3,1,3,3,3,2,2,1,4;
T 1,1,6,4,1,1,2,1,1,1,2,1,2,6,2,1,1,2,1,1,3,6,1,1,3,3;
R 4,2,2,16,8,4,6,2,2,2. **Total 275**, matching §21.8's "275 instances" exactly.
This is the sweep most likely to have caught a stale count after a struck row, and
it is clean.

**S5 — instance-individuation rules vs. cells.** I spot-checked §21.1's two stated
axes against the cells they govern. "Does not equal / differs from" rows enumerate
two directions: T22 (6 = 3 layouts × 2), T14 (6), T3 (6), L21 (4 = 2 layouts × 2),
L30 (2), F17 (2). "Exceeds / larger than" rows enumerate one: T21 (3 layouts),
L44 (3 layouts). Value tests enumerate no direction: L28 (nonzero A_slab with
S = 0) is 1. All consistent.

**S6 — detector/detection-point grid.** Grouping every row by (Detector, Detected)
yields only the five legal tiers: reader/open (32 rows incl. L3, L5, L6 and R1's
top-level half), reader/layer access (35), reader/tile use (24), reader/extent use
(9), verifier/certification (20). No row names a tier §19.2 does not define.

**S7 — blockquote label sweep.** `awk` over first lines of blockquotes: 96 blocks.
95 open with `**Note`, `**Example`, or `**Rationale`. Two anomalies:
line 2124 (§15.1's tile-index region layout) carries no label at all and is
therefore normative under `[R-CNF-01]` — correctly so, since `[R-CNT-17]`'s
extent-length formula depends on it; and line 12 (the "How to read this document"
block) labels itself `*(non-normative)*`, which is **not** one of the three labels
`[R-CNF-01]` exempts. That is finding reader-01.

**S8 — trailer offset/width sweep.** `grep` for `F − 56`, `F − 64`, `F − 4`,
`offset 48`, `offset 60`, `[0, 60)`, `[60, 64)`, `48 trailer`, `12 reserved`.
Twenty-two hits, in §2.3's Note, §6.2's table and prose, §6.3 `[R-CNT-24]`,
§7.2, §8.1's map, §9.2's Note, §9.7, §15.3, §19.1, §21.2 (F10, F14, F15, F32),
§21.3 (L17), §21.4 (T9), Appendix A (two rows), Appendix G item 2. Every one is
consistent with the current 64-byte layout. **No stale offset or width survives
anywhere**: nothing says `file_id` is at 48, nothing says `reserved` is 4 bytes,
nothing describes a field between `committed_file_length` and `file_id`.

**S9 — "generation" sweep.** 53 hits. `grep -io "generation counter|generation
number|generation field|generation_|numbers generations"` → 1 hit, §3.1's
"No field numbers generations", which is the negative statement. No text anywhere
reads a generation value out of a trailer.

**S10 — identity/ordering claims sweep** (`identifies`, `orders`, `distinguish`,
`indistinguishable`, `names the same`, `tells a cache`). 30 hits. I read all of
them; the ones re-pointed at `committed_file_length` are §3.1, §9.2, §9.3 (three
sentences plus three Notes), §20.4's Rationale, §20.5, §21.7, §22.5, §23.2.
Analysis in §5 below — all survive.

**S11 — value-space sweep.** §10.2's eight-row table against the six defining
sections plus §7.3 and §18.2, and against Appendix C's snapshot. All eight
partitions agree in all three places.

**S12 — conformance carve-out sweep** (`not a file-conformance violation`,
`the file is conforming`, `binds a writer's conduct`, `conduct rule`). Nine hits.
The carve-outs are exactly the ones `[R-CNF-02]` enumerates: §10.3/§18.3 conduct
rules (where a value is published, which registry version a writer targets), and
the two express declarations — §6.3's flags = 0 against a set ignore-lane bit, and
§6.2's over-long pre-trailer gap. I found no third express declaration that
`[R-CNF-02]`'s "are the cases this text states" would have to swallow.

---

## 3. Every number I derived myself

CRC-32C implemented from §4.5's parameters (Castagnoli 0x1EDC6F41, reflected in
and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF), i.e. reflected constant
0x82F63B78.

| Quantity | I computed | Document states | Where |
|---|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283, bytes `83 92 06 E3` | §4.5 |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 | §4.5, §7.1, App A |
| CRC-32C of trailer bytes [0,60) of App A's file | 0x402F157E → `7E 15 2F 40` | `7E 15 2F 40` at [124,128) | App A |
| CRC-32C of 4 sentinel entries (80 bytes `FF×16 00×4` ×4) | 0x80A34955 → `55 49 A3 80` | 0x80A34955, stored `55 49 A3 80` | §7.4 example |
| CRC-32C of that 4-byte segment-CRC array | 0xC4EE982E → `2E 98 EE C4` | 0xC4EE982E, payload bytes `2E 98 EE C4` at offset 77 | §7.4 example |
| CRC-32C of 2¹⁶ sentinel entries (1,310,720 bytes) | 0xEECB3BB2 | 0xEECB3BB2 | §15.4, App B |

Non-checksum arithmetic I re-derived:

- **App A trailer field positions.** From the hex dump: magic [64,72); `01 00` at
  [72,74) = trailer offset 8 = version_major; `00 00` at [74,76) = offset 10 =
  version_minor; `00 00 00 00` at [76,80) = offset 12 = flags; `10 00…` at
  [80,88) = offset 16 = dir_offset 16; `04 00…` at [88,96) = offset 24 =
  dir_length 4; `80 00…` at [96,104) = offset 32 = committed_file_length 128;
  `EF CD AB 89 67 45 23 01` at [104,112) = offset 40 = file_id 0x0123456789ABCDEF
  little-endian; twelve zero bytes at [112,124) = offset 48 = reserved; CRC at
  [124,128) = offset 60. **Every row of the annotation table matches the hex dump
  and §6.2's layout table, byte for byte.** File length 8 rows × 16 = 128 ✓.
- **App A open cost.** 64 + dir_length = 64 + 4 = 68 bytes in two requests. The
  prose's "112 bytes covering [16, 128)" = 128 − 16 ✓.
- **§7.4 layer-record payload.** Field-by-field: name 4, layout 1, linearization 2,
  codec 2, filter 2, A 8, S 8, A_slab 8, d 1, C 2 (nine scalars = 34, and the
  prose says "4 + 34" ✓); dimension entry 2+8+8 = 18 ✓; channel entry 5+2+5 = 12 ✓;
  trailing 1+8+4 = 13 ✓. 4+34+18+12+13 = **81** ✓ = stated inline_length, with the
  stated per-field offsets 0/4/5/7/9/11/19/27/35/36/38/40/48/56/63/68/69/77 all
  landing correctly. Extent length 4×20 + ⌈4/2¹⁶⌉×4 = **84** ✓. Grid ⌈100/32⌉ = 4 ✓.
  float32 quiet NaN 0x7FC00000 little-endian = `00 00 C0 7F` ✓; type 12 = `0C 00` ✓.
- **§12.3 channel entry.** 12 bytes `04 74 65 6D 70 0C 00 04 00 00 C0 7F` ✓,
  byte-identical to §7.4's example, as §7.4 claims ("§12.3's `temp` entry, byte for
  byte").
- **§11.2/§11.4.** G = (4,8), N = 32, P = 65,536 ✓; ⌈1000/256⌉ = 4 ✓;
  (300,700) → tile (1,2), s = 1·8+2 = 10 ✓, in-tile (44,188), ordinal
  44·256+188 = 11,452 ✓; planar C = 4, channel 2 → 2·32+10 = 74 ✓.
- **§14.2.** Q = 1+2 = 3, decoded 6·3 = 18 ✓; ordinal 5 → bytes [15,18) ✓; planar
  `b` 12 bytes, ordinal 5 at [10,12) ✓; float32+bool Q = 5, decoded 30, ordinal 5
  at [25,30), t at 25–28, m at 29 ✓. Cross-checked against the general form
  u·Q + Fᶜ and against §14.1's k = u·C + c ✓.
- **§14.3.** P = 10, alternating from true: byte 0 = 0b01010101 = 0x55 ✓; byte 1
  bits 0–1 = `10` → 0x01 ✓; with fill true, pad bits 2–7 set → 0x01|0xFC = 0xFD ✓.
- **§14.4's P = 1 claim.** Planar bool at P = 1: one byte, bit 0 the value, bits
  1–7 the fill bit. Fill false → 0x00/0x01, identical to the interleaved byte;
  fill true → 0xFE/0xFF, different. "The images coincide exactly when that fill is
  false" ✓.
- **§14.5.** Extents (5,5), tiles (4,4) → grid 2×2; edge tile (1,1) covers 4–7 on
  both axes → exactly one real position (4,4) and 15 padding ✓; P = 16, uint16 →
  32 bytes ✓; fill 0xABCD → `CD AB` ✓.
- **§15.4 first example.** ⌈10⁶/65536⌉ = 16 segments, last covering
  10⁶ − 15·65536 = **16,960** ✓; array 64 bytes ✓; region 20,000,064 ✓;
  k = 999,999 → segment 15, segment-relative byte 20·16,959 = **339,180** ✓;
  array at [20,000,000, 20,000,064) ✓; segment 15 at
  [983,040·20, 20,000,000) = [19,660,800, 20,000,000) ✓ ≈ 339 KB ✓;
  full segment 65,536·20 = 1,310,720 = **1.25 MiB** ✓; ⌈1/65536⌉ = ⌈65536/65536⌉ = 1 ✓.
- **§15.4 second example.** disk ordinal 74 → region bytes [1,480, 1,500) ✓;
  channel 3's block = ordinals [96, 128) ✓.
- **§16.2 example.** N = 32, S = 8 → runs [0,8),[8,16),[16,24),[24,32) ✓;
  tile rows 1–2 = ordinals 8–23 = runs 1 and 2 ✓.
- **§17.3 example.** s = 4, n = 3 over `00 00 80 3F 00 00 00 40 00 00 40 40`;
  applying "byte i of group j at offset i·n + j" gives
  `00 00 00 00 00 00 80 00 40 3F 40 40` ✓, matching both the hex and the prose
  gloss.
- **§20.3 examples.** 32·20 + 4 = **644** ✓; 10⁶ tiles × 20 B ≈ **20 MB** ✓.
- **§9.2's floor argument.** new F ≥ dir_offset + dir_length + 64 ≥ priorF + 68,
  and both are multiples of 64, so new F ≥ priorF + **128** ✓. Same argument from
  offset 0 gives §5.1's 128-byte floor: 16 + 4 = 20, next multiple of 64 above
  20 + 64 = 84 is **128** ✓, matching App A's 16 + 4 + 44 + 64.
- **§9.3's ceiling Note.** 2⁶³ is a multiple of 64, so the largest multiple of 64
  at or below 2⁶³ − 1 is **2⁶³ − 64** ✓, and 2⁶³ − 64 + 128 > 2⁶³ − 1 ✓.
- **§21.9's Note.** ⌈2³²/2¹⁶⌉ × 4 = 2¹⁸ = **256 KiB** ✓; at 2³⁶ it is 2²⁰ × 4 =
  **4 MiB** ✓. §24's "tens of gigabytes" for 2³² × 20 B = 85.9 GB ✓.
- **`[R-CNT-24]`'s 48 redefinable bytes.** 64 − 8 (magic) − 4 (major+minor) −
  4 (CRC) = **48** ✓, and reserved [48,60) lies inside the redefinable span, which
  is exactly why §2.3's Note says F15 does not reach ✓. §6.3's "zero slack: every
  byte is assigned" holds: 8+2+2+4+8+8+8+8+12+4 = **64** ✓.
- **§2.3's "`[R-CNT-06]` states nine".** Rows whose *Governing rule* cell is
  `[R-CNT-06]`: F8, F9, F10, F12, F13, F14, F15, F16, F17 = **nine** ✓, of which
  magic and CRC assert `[R-CNT-24]` invariants and **seven** do not ✓.
- **§20.5's "one row for each of the other seven spaces".** §10.2 tabulates eight;
  record type → F36/L25; the other seven → L36 (layout), L33 (linearization),
  L34 (sample type), L43 (codec), L45 (filter), L31 (index encoding), R1 (metadata
  encoding) = **seven** ✓.
- **§4.6's `température`.** NFC 12 bytes (10 ASCII + `C3 A9`) ✓, matching the given
  byte string; NFD 13 (`65 CC 81`) ✓. App G item 10 repeats both ✓.
- **§12.1's bfloat16.** binary32 1.0 = 0x3F800000, high 16 = 0x3F80, stored
  `80 3F` ✓; sign at bit 15, exponent 14–7, significand 6–0 is exactly binary32's
  31/30–23/22–16 shifted right 16 ✓.
- **§21.9 limits table row count.** Eight rows; "the first five rows range over
  declarations" (rank, C, entry_count, layers, dir_length) + "the last three are
  per-instance" (tile, document, window) = 8 ✓. App B's one-line restatement lists
  the same eight ✓.
- **Closed-list counts elsewhere.** §12.1 thirteen sample types ✓ (twelve numeric
  ✓); §10.1 four vehicles ✓; §17.2 four codecs ✓; §17.3 two filters ✓; §18.2
  "Four restrictions" ✓; §17.2 "Three frame features are excluded" ✓ (dictionary,
  content-checksum flag, oversized window); §22.2 "Three properties" ✓;
  §22.3 "Four residues" ✓; App D "Six choices" ✓; §21.1's six specialization pairs
  ✓ (F1-front⊂F6, F1-magic⊂F8, F35⊂F36, L24⊂L25, F21⊂F22, L10⊂L11 — each verified
  by implication); §15.3 "Six rows are marked *structural*" ✓ (I counted six in the
  eleven-row table); R4's 16 = 8 conditions × 2 containers ✓.

**Nothing I recomputed disagreed with the document.** That is the strongest single
statement I can make about this round: every stated constant, offset, size,
checksum, count and derived product in the specification is correct as it now
stands, including all six CRC constants and both worked byte-level examples.

---

## 4. The implementation walk

### 4.1 Cold open, byte-exact

**Local reader.** `stat` the file → F. If F < 128, reject-file (§5.1
`[R-CNT-27]`, F5) — this must precede computing F − 64, and the document does not
order it explicitly, but it is forced arithmetically and F5's tier is *open*, so
there is nothing to guess. Map or read; bytes [0,16) are now resident, so
`[R-CNT-04]` obliges byte-equality against
`89 54 41 52 4E 0D 0A 1A` + eight zeros **before other processing** (§19.1 step 1);
mismatch is reject-file (F6; byte-reversed is F1, the narrower row).

**Remote reader, two requests, 64 + dir_length bytes.**

*Request 1* — suffix range, final 64 bytes. Bounded before reading by the constant
64; no file knowledge needed. Its response also carries the transport-authoritative
size F (`[R-CNT-10]`), which is why §19.1's steps 1 and 2 cost one request between
them. `[R-CNT-10]` additionally obliges me to handle a 200 response deliberately
(never treating the body prefix as the range) and to fall back to size-probe +
absolute range where suffix ranges are unsupported, and forbids substituting the
trailer's own `committed_file_length` for the transport size — which matters,
because F17 is precisely the cross-check between them.

Validate in §6.2's **fixed order**: (i) magic `8A 4E 52 41 54 0D 0A 1A` at trailer
offset 0 (F8); (ii) CRC-32C at offset 60 over [0,60) (F14); (iii) the version gate
(F18 for 0; capability refusal with a distinct diagnostic for an unimplemented
major, `[R-CNT-07]`). Only these three touch fields `[R-CNT-24]` pins across
majors, which is why exactly F8, F14, F6 and F1's two instances "reach" a foreign
major (§2.3 `[R-CNF-13]`, §21.2's preamble) — and the order matters: the reaching
conditions are all checked *before* the capability refusal is owed, which
`[R-CNF-13]` states outright. Then, unordered but all before acting: flag gates
(F19 for any incompat bit; ignore-lane bits ignored, `[R-CNT-08]`);
`committed_file_length` = F and ≡ 0 mod 64 (F17, F13); `dir_offset` ≥ 16 (F9);
`dir_length` ≥ 4 (F16); `dir_offset + dir_length` ≤ F − 64 (F10), a
declaration-derived sum under `[R-ENC-04]` so overflow is F3; `file_id` ≠ 0 (F12);
reserved [48,60) all zero (F15). Domain violations above 2⁶³ − 1 are F2.

Note what §4.5 `[R-ENC-10]` buys here: comparing the magic against a constant is
*not* "acting on" it, so checking the magic before the CRC that covers it is
licensed, and §6.2's explicit order governs. Without that sentence the ordering
would be a genuine fork; with it, it is settled.

*Request 2* — `[dir_offset, dir_offset + dir_length)`. Bounded before reading by
values the trailer CRC has already covered — which is the whole point of
`[R-ENC-05]`: no seek or fetch on an unverified integer. Verify the region's final
4 bytes as CRC-32C over the preceding `dir_length − 4` (F20) **before any other
use** (`[R-CNT-11]`), then parse.

The speculative variant collapses requests: one suffix window that contains
`[dir_offset, F)` makes request 2 unnecessary (§6.4's containment test), and a
window that reaches offset 0 makes [0,16) resident and so re-arms the front-block
obligation. §6.4's Note is explicit that no request count is a conformance
property. Writers are advised (SHOULD) to keep `dir_length + pad + 64` ≤ 65,536 so
a 64 KiB suffix suffices — I verified that F − dir_offset is exactly that sum.

*Record walk* (§19.1 step 4): parse 24-byte headers + `inline_length` payloads to
exactly `dir_offset + dir_length − 4` with no residue (F29); type 0 is F24; unknown
top-level type with MU = 1 is reject-file (F35 if reserved-range; an
experimental-range one is a **conforming file the reader refuses**, §21.6);
multiplicity (F34); extent slots of non-layer top-level records (F30/F31/F32);
user-metadata framing — no (0,0) slot, `extent_length` ≥ 5, `inline_length` = 1,
encoding byte in 1..2 (F21, F22, F23, R1). Build the layer-name namespace from name
fields obtainable within each record's `inline_length`; uniqueness is decided first
and over raw bytes, so two byte-identical invalid names are still a duplicate (F4);
a name field that overruns yields no name and is a layer-scope error instead.
Layer-name well-formedness and the name rules are L3/L5/L6, and their tier is
*open*, consistent with §19.2's first bullet.

**Working set of the open: the trailer and the directory, nothing else** — no
extent slot's content, no index, no payload (`[R-RDR-01]`). For App A's 128-byte
file: 64 + 4 = 68 bytes, two requests, and step 4 finds an empty layer table.

### 4.2 Validation timing by tier

`[R-RDR-02]` fixes the **latest** point, never the earliest, and earlier detection
is always licensed (`[R-CNF-12]`), so divergence is only ever toward earlier
rejection.

- **Open**: front block (if resident), trailer, directory region + record walk,
  layer-name namespace. 32 register rows.
- **First layer access** — defined as the first use of any declaration *other than
  the name* — full validation of the layer record: extent slot (`[R-CNT-13]`), the
  §7.4 constraint set (`[R-CNT-23]`), A/S exclusivity (`[R-CNT-16]`), exact parse
  and sub-record walk with no residue (`[R-CNT-18]`), sub-record multiplicity,
  dimension/channel name rules, user-metadata sub-record framing, field widths and
  u64 domain, the six value sets (linearization §11.4, sample type §12.2, layout
  §14.1, index encoding §15.1, codec §17.2, filter §17.3), bool fill
  (`[R-TYP-07]`), the lz4 declaration cap (`[R-COD-07]`), the geometry floor and
  its products (`[R-GEO-01]`–`[R-GEO-03]`), the 2⁶³ − 1 ceiling on everything
  `[R-ENC-04]` designates including §14's decoded sizes, and the two I/O-free index
  cross-checks (`[R-CNT-17]`). **I checked §19.3's enumeration against every
  layer-access row of §21.3 and each of the 35 is reachable from something §19.3
  names.** No fetch happens here.
- **Tile use**: the index chain (`[R-IDX-04]`, L37/L38 — layer scope though
  detected at tile use), entry classification (T6–T12), payload CRC (T1), codec
  header/stream rows (T14, T17–T25), decoded size (T3).
- **Extent use**: a record extent's terminal CRC (R2) and the document content
  rules §18.2 attaches at its encoding (R3–R10). No earlier, because the open
  fetches no extent.
- **Never**: everything whose Detector cell is *verifier* — 20 rows. A reader that
  detects one MAY reject the file (`[R-CNF-12]`) but is not obliged to, and for
  several of them the governing rule positively obliges it to serve the structure
  unchanged (`[R-CNT-12]`, `[R-CNT-22]`, `[R-MTA-05]`). `[R-SER-08]` is the one
  that goes the other way, resolving one nonconforming byte to a value.
- **Verdicts**: a reader's outcome is per §21's scope; a verifier's verdict is
  *conforming* / *nonconforming* / *cannot establish*, with an established
  violation always winning, *cannot establish* available only to a traversal that
  established none, and *unexamined* constraining the report rather than the
  verdict.

### 4.3 Layer access and the tile read

From a layer name: match raw bytes against the namespace built at open, then run
§19.3's validation once. Geometry: Gᵢ = ⌈Eᵢ/Tᵢ⌉ stated as Eᵢ/Tᵢ + (Eᵢ mod Tᵢ ≠ 0)
to avoid the overflowing idiom; N = ∏Gᵢ; P = ∏Tᵢ; addressed-tile count N
(interleaved) or C·N (planar), cross-checked against `entry_count` (L21) and
against the region length formula `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` (L22).

From a coordinate: tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; s = Σ tᵢ·∏_{j>i}Gⱼ; in-tile
ordinal = Σ uᵢ·∏_{j>i}Tⱼ (row-major for *every* linearization, permanently); disk
ordinal s, or c·N + s planar.

Index chain: entry k lies at region byte 20k. The segment-CRC array is at region
bytes [entry_count·20, entry_count·20 + ⌈entry_count/2¹⁶⌉·4); segment
⌊k/2¹⁶⌋ covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)) at region bytes
20× those. Both ranges are computable from the layer record alone and may be
fetched in parallel; verify `crc_of_crc_array` over the whole fetched array, then
the segment CRC over the fetched segment (L37, L38), in dependency order. Both may
be cached under committed-prefix immutability. At `entry_count = 0` there is no
region, the slot is (0,0), `crc_of_crc_array` is 0, and nothing is fetched or
verified.

Entry classification (§15.3, eleven rows, six *structural*): sentinel
`FF×16 00×4` reads as fill and short-circuits; six structural malformations are
reject-tile and contribute no extent to the coverage walk, to slab run continuity,
or to the verifier overlap rows; a stored-bytes CRC failure is reject-tile but the
entry stays well-formed and keeps its place everywhere. Fill is produced by
**exactly one** condition — a sentinel read from a verified chain — and never as a
failure fallback (`[R-TYP-09]`, `[R-CNF-09]`).

Payload: fetch [offset, offset+length), verify the entry crc, then decode —
**codec first, then the filter's inverse** (§17.1). Codec 1 requires
length = decoded size, checkable before the fetch (T14). Codec 3's header checks
(magic, one frame, no skippable frame, zero dictionary ID, no content-checksum
flag, window ≤ decoded size, content-size = decoded size if present, and never
sizing a buffer from it) are all pre-decode. Every codec must consume the extent
exactly and produce exactly the decoded size (T24, T25, T3).

Decoded byte layout — the thing a caller actually gets:

- planar numeric channel c: P·Bᶜ bytes, value k at k·Bᶜ;
- planar bool: ⌈P/8⌉ bytes, value k at bit k mod 8 of byte k div 8, LSB-first, pad
  bits carrying the channel's fill bit;
- interleaved: P·Q bytes with Q = ΣBᵢ, channel c at in-tile ordinal u at byte
  u·Q + Fᶜ where Fᶜ = Σ_{j<c} Bⱼ; bool as one byte.

Byte-shuffle's stride is Bᶜ planar, Q interleaved, 1 (identity) for a packed bool
plane — and L is divisible by s in every one of those cases, which I checked.

Extraction never returns padding positions, and step 8 returns bit patterns
unaltered, the single exception being the charitable resolution `[R-SER-08]`
defines for a nonconforming interleaved bool byte. Where a request spans several
entries, a tile-scope failure is bounded to that entry's positions (return the rest
with a per-entry report, or fail the whole request — but never fill); a
layer-scope failure inside the same request bars everything further, prospectively.

### 4.4 Degradation walks (five, end to end)

1. **Unknown top-level record type, MU = 0, PE = 0, experimental range.** Open,
   record walk: type unassigned, MU gate passes, `[R-CNT-15]` → ignore-record. The
   file is conforming (§21.6). I serve every layer normally. An updater must retain
   it byte-identically unless the same commit independently changes the scope it
   attaches to; a compactor may drop it whenever it rewrites, and SHOULD report the
   loss. Contrast the same type with MU = 1 at top level: `[R-CNT-15]` → reject-file,
   and §21.6 records that as a **conforming file a reader refuses** — a capability
   diagnostic, not corruption. The same type as a *layer sub-record* with MU = 1 is
   reject-layer and `[R-CNT-18]` positively forbids rejecting the file for it; I
   serve every other layer. That asymmetry is the load-bearing qualifier in §21.6's
   closing paragraph and I checked it against `[R-CNF-03]`'s carve-out, which is
   silent rather than permissive there — `[R-CNT-18]` supplies the prohibition.
2. **Unknown codec value 7 on layer B.** §19.3, at first access to B: codec is
   outside 1..4 → L43, reject-layer. Layers A and C unaffected; I may still list
   B's name. I am *not* a non-conforming reader for this, because all four assigned
   codecs are core and I implement them (`[R-COD-03]`, `[R-COD-11]`); a verifier
   here reports *nonconforming*, not *cannot establish*, because the value set is a
   violation rather than a capability gap.
3. **Truncated tail / torn commit.** Physical length F′ > the last committed F, with
   a partial write beyond. Final 64 bytes are not a trailer: magic fails (F8), or
   CRC (F14), or the length cross-check (F17). Reject-file; §9.5 forbids scanning
   backward, so I cannot tell residue from corruption and am not asked to. Nothing
   is served. Recovery is a separate, deliberate operation: probe backward at
   64-aligned o requiring magic + CRC + `committed_file_length = o + 64`, take the
   nearest-to-end candidate, re-verify the truncated result as a whole file, report
   how many candidates were rejected.
4. **Segment CRC mismatch on layer D while reading tile 900,000.** Tier: tile use.
   Outcome: layer scope (`[R-IDX-04]`, L38). The bar is prospective — samples I
   already returned from D under §19.2's timing stand, but D serves nothing further.
   Other layers, and other tiles of other layers, are untouched. I must not return
   fill for D's tiles (`[R-TYP-09]`).
5. **A limit exceeded.** Layer E declares `entry_count = 2³⁶` and my index budget
   stops at 2³². The file remains **conforming** — §21.9's table states minimum
   guarantees, not caps — and I MAY decline, at the narrowest scope whose
   declarations exceed what I can serve, here the layer. I MUST report it as a
   resource limit and not as corruption (`[R-ERR-04]`), because the two remedies are
   opposite. A verifier declining on the same ground reports *cannot establish* for
   that requirement, not *nonconforming*.
   (Sixth, since the charter names it: **format major 3.** Apply every reaching
   condition first — front block if resident, trailer magic, trailer CRC — and
   report a failure of one on the requirement's own ground, reject-file. Only if all
   of them pass is the distinct "TARN format major 3; this reader supports major 1"
   diagnostic owed. Nothing is served either way; a verifier reports *cannot
   establish*, unless a reaching condition failed, in which case *nonconforming*
   regardless of the declared major.)

### 4.5 Worked example — App A through my reader

F = 128 (≥ 128 ✓, ≡ 0 mod 64 ✓). Front block equals the constant. Trailer at
[64,128): magic ✓; CRC 0x402F157E, which I recomputed over the 60 bytes and matched
byte for byte; version_major 1, version_minor 0; flags 0 (no incompat bit);
committed_file_length 128 = F ✓; dir_offset 16 ≥ 16 ✓; dir_length 4 ≥ 4 ✓;
16 + 4 = 20 ≤ 64 ✓; file_id 0x0123456789ABCDEF ≠ 0 ✓; twelve reserved bytes zero ✓.
Directory [16,20): a zero-length record sequence plus its CRC, which for zero bytes
is 0x00000000 — matches. Record walk: zero records, no residue. Layer table empty.
Cold remote cost: two requests, 68 bytes.

---

## 5. Shape-10 audit of the re-pointed sentences

The removed field used to supply a generation ordinal. Everything that ordinal
supported now rests on `committed_file_length`, on a property the document now
asserts: strict increase per commit, by at least 128. For each re-pointed sentence
I asked which property of its subject makes it true and whether F has it.

- **§3.1, "ordered by the strictly increasing committed file length".** Needs
  monotonicity. `[R-LIF-02]` supplies it and §9.2's second Note *derives* it from
  step 1 + `[R-LIF-01]` + `[R-CNT-06]` rather than asserting it, so it is not a new
  free-standing obligation on the writer. Holds.
- **§9.3, "orders that file's generations and identifies each of them".** Ordering
  needs monotonicity ✓; *identification* needs injectivity, which strict increase
  gives ✓ — no two commits of one file_id share an F. Holds. The cases where it
  fails are named: a file_id collision (Note 1) and truncate-then-re-append
  (Note 3).
- **§9.3's revalidation triple.** "Same F → everything cached stays valid" needs
  same-F ⇒ same generation ⇒ same prefix: injectivity again ✓. "Higher F → refetch
  the directory" needs immutability below the old F ✓. "Lower F → a different file"
  needs `[R-LIF-01]` to forbid losing committed bytes ✓, and the Note says exactly
  that. A generation counter would have supported all three identically; F does too.
- **§9.3's ceiling Note.** Bounded above by two rules: F ≤ 2⁶³ − 1 (`[R-ENC-03]`)
  and F ≡ 0 mod 64 (`[R-CNT-06]`), reachable ceiling 2⁶³ − 64. This is the shape the
  brief warns about — a ceiling claim inherited from a different subject — and it is
  arithmetically correct as re-derived. A generation counter would have had a
  different ceiling (2⁶³ − 1, no alignment term); the Note has been rewritten
  correctly, including "by two rules rather than one".
- **§9.3's third Note, "F counts bytes, not commits".** This is the property F
  *lacks*, correctly disclosed, and it is echoed in §20.4's Rationale, §20.5,
  §21.7, §23.2 and App G item 4 — five places, all consistent.
- **§20.5, "`[R-LIF-03]` reaches that verdict on file_id alone, before any
  comparison of committed_file_length".** I tested the degenerate case: a
  zero-slack input compacts to an output of the *same* F, so a reused file_id would
  not even be caught by the "lower F" clause. That is precisely why the fresh
  file_id must be a draw and not a comparison, and §20.5 says so. Holds.
- **§21.7, "no witness".** I checked whether a backward probe witnesses a violation
  of strict growth. It cannot: §9.6 requires a candidate's
  `committed_file_length = o + 64`, so among probe candidates the value is a strictly
  increasing function of position by construction. A generation counter *could* have
  been witnessed this way (out-of-order counters in the slack); F cannot. The claim
  is more true now, not less.
- **§22.5's detached signature.** "over the committed prefix [0, F) ... pinned to
  the file_id its trailer names and to that F" — needs only immutability of
  [0, F) ✓, and it is the "detached hash over the committed prefix" §9.6 names as
  one of the two things that still work, distinct from the "signed committed file
  length" §9.6 explicitly rules out. The two passages do not collide.
- **§23.2.** Commit count is recoverable only by probe, unavailable from the live
  trailer, absent from a compacted file ✓.
- **App G item 2.** The derived `file_id` hashes [0, F − 64) followed by the
  trailer's first 60 bytes with `file_id` zeroed — all of which is now
  well-defined against the current 60-byte pre-CRC span ✓; and the carve-out
  ("re-deriving it on an already-compact input would reproduce the input's own
  file_id") is exactly right, since a profile-pinned compaction of an already
  compact file reproduces every hashed byte.

I found no sentence in this family that inherited a property F does not have.

---

## 6. Suspicions I opened and closed

Recorded so a reader can see what was looked at and why it is clean.

1. **A row in §21.2 stranded by the struck F11 / a stale count.** Closed by S3 and
   S4: 35/49/26/10 = 120, and 275 instances, both exactly as stated. The struck
   label is deliberate and §24's `[R-VEC-02]` supplies the normative permanence rule
   (§21.2's Note is only a Note, but `[R-VEC-02]` is not).
2. **A stale trailer offset somewhere outside §6.2.** Closed by S8: 22 hits, all
   consistent, including §8.1's map, §2.3's Note, App A twice, and App G item 2.
3. **App A's dump disagreeing with its annotation table.** Closed byte by byte; and
   the CRC recomputes to the stated `7E 15 2F 40`.
4. **A worked example whose arithmetic no longer follows.** Closed: §5.1, §7.4,
   §11.2, §11.4, §12.1, §12.3, §14.2, §14.3, §14.4, §14.5, §15.4 ×2, §16.2, §17.3,
   §20.3 ×2 all recomputed clean, and the three interior CRC constants
   (0x80A34955, 0xC4EE982E, 0xEECB3BB2) all reproduce.
5. **`[R-CNF-03]`'s acceptance carve-out vs. `[R-CNT-18]`'s "MUST NOT reject the
   file" for an experimental MU = 1 sub-record.** Closed: §2.3 makes the acceptance
   duty *silent*, not permissive; `[R-CNT-18]` supplies a positive prohibition and
   `[R-CNF-12]`'s licence reaches only nonconforming files. §21.6's closing
   paragraph states the same asymmetry and calls the qualifier load-bearing.
6. **§20.3 step 4's list omitting `[R-SER-08]`'s bool-byte constraint** — a change
   from uint8 to bool on an interleaved channel preserves Q, decoded size, offsets,
   padding set and codec, yet can strand a stored 0x7F. Closed: step 4 states the
   test as "what §14 fixes for its stored bytes or how they decode" and says "the
   list names where that effect arises rather than standing on its own", and §21.7
   independently names "a boolean byte" among the witnesses of a step-4 violation.
   So the list is illustrative and the general test reaches the case.
7. **§20.3's example (c) claiming a fill change is directory-only "on a layer with
   no padding position and no pad bit"**, which is narrower than the rule (the rule
   quantifies over *stored* tiles). Closed: the following sentence gives the barred
   case in the rule's own terms, and (c) is an Example, hence non-normative and
   stating a sufficient condition rather than a boundary.
8. **§6.2's Note claiming a trailer-mimicking payload at EOF "is caught at the
   directory CRC".** Closed: §21.6's row concedes the residue in terms — "which
   catches any mimic that is not itself a consistent generation; §9.6's second
   caution covers the rest" — and §9.6 makes whole-file re-verification of recovery
   output normative. The Note is non-normative and does not disagree with the rule
   it glosses once §21.6 is read with it.
9. **§21.1 attributing to §14.2 the phrase "the sole resolved byte", which §12.3
   `[R-TYP-04]` actually coins.** Closed: §14.2's own Note says the equivalent
   ("Only the in-tile byte ... could be met by a reader with no obligation to act on
   it"), and App H cites both. A citation shade, not a divergence.
10. **§11.1's "a zero-extent layer's **last** zero grid count" — *last* in the
    sense of last-declared, or last-remaining?** Closed as last-remaining: the
    sentence sits under "Growth that changes entry_count", and only exhausting the
    final zero raises N above 0. It is also inside a Rationale, so non-normative.
11. **`[R-CNF-02]`'s closed list of express non-violations swallowing something
    else** (e.g. `[R-COD-06]`'s undisclosed dictionary). Closed by S12: the
    dictionary case is not *expressly declared* a non-violation; §21.7 places it in
    the undetectable class, and §21.1 limits register completeness to *detectable*
    violations, so the two do not collide.
12. **§21.9's per-instance rows vs. the eight-row table** (5 + 3 = 8). Closed by
    count.
13. **F2's `committed_file_length` instance being unreachable without also firing
    F17.** Closed: §21.1's specialization rule plus `[R-VEC-02]`'s explicit
    provision for conditions that cannot be isolated ("the entry records every row
    the file exercises and says which it was built for").
14. **A point request vs. a single-position region request on a zero-extent
    layer** — the first fails as a request, the second succeeds returning nothing.
    Closed: §19.4 step 1 and §21.6 both state it, and `[R-GEO-02]`'s "a read of any
    region of it returns no samples" is about regions only. Deliberate, not
    contradictory.
15. **Whether §8.1's coverage map is complete for major 1.** Closed by walking it:
    trailer→directory→crc_of_crc_array→segment CRC array→segment→entry→stored tile,
    plus the user-metadata extent's terminal CRC, plus the three declared
    exceptions (front block by equality, the three terminal checksum fields,
    unassigned-type extents). Every field of every structure is reached exactly
    once.
16. **§19.3's enumeration vs. §21.3's layer-access rows.** Closed: all 35 rows are
    reachable from something §19.3 names, including the six value sets which map
    one-to-one onto L33/L34/L36/L31/L43/L45.
17. **Whether any register row is missing for a reader-detectable condition I
    derived from the walk.** I enumerated the conditions my open/layer/tile/extent
    paths can raise and matched each to a row; I found no unregistered one.
18. **The unlabelled blockquote the brief warned about.** Found (§15.1's index
    region layout, line 2124) and confirmed normative and consistent with
    `[R-CNT-17]`. But S7 turned up a *second* anomaly in the other direction, which
    is finding reader-01.

---

## 7. Findings

### reader-01 — CONTRADICTION

**Location.** §2.1, `[R-CNF-01]`; and the unnumbered blockquote at the head of the
document (line 12), before §1.

**Quotation.** `[R-CNF-01]`:

> All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative. `[R-CNF-01]`

and the block it governs:

> **How to read this document** *(non-normative).* Sections follow a fixed
> rubric where applicable: purpose, byte-layout table, writer rules, reader
> rules, error handling, worked examples.

**The two readings.**

(a) `[R-CNF-01]` governs literally. The block is not §1 — §1 begins later, at
"### 1. Introduction" — it is not labeled *Note*, *Example* or *Rationale*, and it
is not an appendix. It is therefore **normative**, and its self-label is simply
wrong about it. On this reading the block's sentences are requirements: sections
"follow a fixed rubric where applicable"; layout tables give the stated columns;
"test vectors cite those identifiers rather than prose positions".

(b) The block's own parenthetical governs and it is non-normative.

**Which I picked, and why.** (a). `[R-CNF-01]` is the rule that *defines*
normativity for this document, and this document's own settled practice is that
the defining rule beats a restatement or a local label: §21.1 — "where a row and
the rule it cites diverge, **the rule governs**" — and `[R-EXT-05]` — "the section
that defines the space governs". Note also that "identified as non-normative" is a
mechanism `[R-CNF-01]` recognises, but recognises **only for appendices**; the
block uses that mechanism outside the scope the rule grants it. Every appendix that
is meant to be non-normative (A, B, C, D, E, G, H) uses it correctly and is covered,
and Appendix F, which carries no such identification, is correctly normative. This
one block is the only text in the document that claims an exemption `[R-CNF-01]`
does not extend to it. Symmetrically, the only other blockquote anomaly runs the
other way and is fine: §15.1's tile-index region layout carries no label and is
therefore normative, which is exactly what `[R-CNT-17]`'s extent-length formula
needs.

**What an implementer does wrong without it.** Concretely, not much, because the
block's substance duplicates §4.7 (`[R-ENC-16]`'s structural/descriptive split),
§2.2 (stable identifiers) and §24 (`[R-VEC-02]` already obliges vectors to cite
requirement identifiers). Nothing in the block contradicts the normative text it
paraphrases, so no reader or writer behaviour changes. What does go wrong is
downstream tooling and process: anyone building a requirement inventory, a
normative-statement extractor, or a review checklist from `[R-CNF-01]` — exactly
the sort of tool this project has built before — must decide whether the block is
in or out, and the document answers "in" while the block answers "out". A
specification whose §2.1 is the conformance vocabulary should not have a
disagreement about its own normativity anywhere in it, and the fix is one word: add
the block's label to `[R-CNF-01]`'s exception list, or relabel the block as a
*Note*.

**Byte-level: no.** Under either reading the emittable set is unchanged and no
accept/reject verdict moves. The block constrains no field, no offset and no
outcome; its only imperative content is about how this document and its test
vectors are organised, and `[R-VEC-02]` already states the vector half normatively.
Two implementations disagreeing about this block would still emit and accept exactly
the same bytes.

---

## 8. Confidence, and what I did where I found little

I found one defect, and it is not byte-level. That is a thin result for an
acceptance round, so here is what I did that *would* have found something.

**On the byte-level worked example and its annotation table** — the passage the
brief singled out as the highest-value target — I verified all sixteen lines of
Appendix A's hex dump against all fourteen rows of its annotation table against
§6.2's ten-row layout table, and independently recomputed the trailer CRC from
§4.5's parameters, getting `7E 15 2F 40`. Every field lands at the offset the new
layout puts it at: `file_id` at trailer 40, reserved twelve bytes at 48, CRC at 60.
If the removal of the generation field had left a stale offset, a stale width, a
stale reserved-length, or a CRC computed over the old byte string, this is where it
would have shown, and it did not.

**On the register** I recomputed the row count (120) and the instance count (275)
mechanically from the tables themselves and matched both against §21.8's stated
figures, checked the struck-label gap, checked §21.2's nine-condition and
seven-condition sub-counts against the rows whose Governing rule cell is
`[R-CNT-06]`, checked §20.5's "seven spaces / seven rows" against §10.2's table,
checked the six specialization pairs by implication, and checked every Detected
cell against §19.2's tier vocabulary. A single stranded, duplicated or miscounted
row would have fallen out of any of those.

**On the reader path** I walked §19.1 → §19.2 → §19.3 → §19.4 as code, listed the
conditions each step can raise, and matched them to register rows in both
directions — rows to steps and steps to rows. §19.3's enumeration is complete
against §21.3's 35 layer-access rows; §19.1's is complete against §21.2's open rows
once §19's preamble ("§21's register is [the inventory]") is taken at its word.

**On the format change specifically** I audited ten sentences that now name
`committed_file_length` where a generation counter used to serve, asking of each
what property makes it true (monotonicity, injectivity, immutability, a ceiling)
and whether F has it. All ten hold, and two of them — §21.7's "no witness" and
§20.5's "on file_id alone" — I tested against the degenerate cases that would break
them (an out-of-order probe candidate; a zero-slack compaction that preserves F).
The document's derivations were already there.

**Where I am least sure.** Two areas.

First, §18.2's `[R-MTA-09]` is the densest single requirement in the document —
three interacting size/window bounds, two of which are the reader's own capability
and one of which (the frame content-size field) is the file's, routed to R4 rather
than R3. I checked R4's sixteen instances against the carried-over constraint list
and they reconcile (six witnessed constraints + two directions of content-size,
times two containers), and I checked that the two unwitnessed carry-overs are named
as such. But I did not construct a zstd frame and test the Single_Segment_Flag
interaction empirically; I reasoned it from RFC 8878's two Window_Size derivations
as §17.2's Note describes them, and my confidence there rests on that Note being an
accurate account of the RFC, which I could not check from this document alone.

Second, the *undetectable* class in §21.7. A file whose tile was compressed with an
undisclosed dictionary, or whose filter used a wrong stride with no structural
constraint to break, violates a MUST while every checksum certifies it. Whether
such a file is "nonconforming but undetectably so" or "conforming, the rule being
conduct" is a question §21.7 answers by saying "no file-level witness exists to
check, so nothing about the file is left undetermined" — which is a claim about
verdicts rather than about the predicate. I could not find a place where the two
readings diverge in bytes or verdicts (a verifier certifies either way, and no
reader behaviour turns on it), so I did not raise it; but it is the one place where
I think the document's account of its own conformance predicate is doing more work
than it shows.

**Confidence that an implementation built from this text alone would
interoperate: high.** The open path, the validation tiers, the index chain, the
decoded byte layouts, the codec/filter order, the sentinel and fill semantics, the
degradation outcomes and the worked examples are all determinate and mutually
consistent, and every constant I could compute is right.
