# Cleanroom round 17 — Diagram auditor — verbatim working transcript

## Access disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,317 lines), in five `Read` calls covering lines 1–4317 with no gaps. I ran
`wc -l` and two `grep` invocations against that same file, and I wrote and ran
four Python scripts in my own scratchpad that read no project file except that
one (`inst.py` and one inline script open `spec/tarn.md`; `crc.py` and `appA.py`
read nothing — they carry their inputs literally, transcribed by hand from the
document). I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `conformance/`, `spec/registry.json`, or any ADR. I ran no `git`
command, no web search, no web fetch. I did not read or list the round-17 output
directory. Prior knowledge of other array/image formats was used only to
generate suspicions; every conclusion below is settled against the document's
own text.

---

## 1. Inventory — every figure, diagram, layout box, table, worked example and checklist

Found first, judged second, so coverage is checkable. Line numbers are from the
file as read.

### 1a. ASCII diagrams / box drawings

| # | Line | What |
|---|---|---|
| D1 | 587–592 | §5.1 "a file after three commits" region box, with an under-brace row |
| D2 | 1200–1209 | §9.2 "what a crash sees" — three rows (committed / mid-commit / committed) |
| D3 | 1069–1088 | §7.4 annotated 81-byte layer-record inline payload (offset/bytes/gloss) |
| D4 | 1993–1994 | §15.1 tile-index region layout block (`[ entry array ] [ segment CRC array ]`) |
| D5 | 3049–3053 | §20.3 example shape (a) — a new layer |
| D6 | 3065–3069 | §20.3 example shape (b) — tiles added to an existing layer |
| D7 | 3088–3091 | §20.3 example shape (c) — a change confined to the directory |
| D8 | 3212–3218 | §20.5 "what compaction reclaims" — input/output rows with file_id + generation |
| D9 | 3951–3960 | Appendix A hexdump of the 128-byte minimal file |

### 1b. Layout / normative tables

| # | Line | What |
|---|---|---|
| T-a | 235–241 | §2.4 outcome-class table (5 rows) |
| T-b | 697–700 | §6.1 front signature block (Offset/Size/Value/Class) |
| T-c | 740–752 | §6.2 trailer layout (11 rows) |
| T-d | 904–910 | §7.2 record header (5 rows) |
| T-e | 977–980 | §7.3 record types of format major 1 |
| T-f | 1006–1023 | §7.4 layer-record inline payload (17 rows) |
| T-g | 1121–1129 | §8.1 checksum coverage map (7 rows) |
| T-h | 1395–1404 | §10.2 numeric identifier spaces (8 rows) |
| T-i | 1598–1612 | §12.1 core sample types (13 rows) |
| T-j | 1830–1833 | §14.2 decoded size / offset of value k (2 rows) |
| T-k | 1998–2002 | §15.1 tile-index entry (3 rows) |
| T-l | 2046–2058 | §15.3 entry validity (11 rows) |
| T-m | 2438–2440 | §18.2 user-metadata inline payload (1 row) |
| T-n | 2587–2594 | §18.4 standardized keys (6 rows) |
| T-o | 3117–3121 | §20.4 updater obligations by stored flags (3 rows) |
| T-p | 3349–3386 | §21.2 file-scope register, F1–F36 |
| T-q | 3393–3443 | §21.3 layer-scope register, L1–L49 |
| T-r | 3450–3477 | §21.4 tile-scope register, T1–T26 |
| T-s | 3497–3508 | §21.5 ignored-records register, R1–R10 |
| T-t | 3515–3530 | §21.6 conditions that are not violations (14 rows) |
| T-u | 3626–3635 | §21.9 minimum-guarantee limits (8 rows) |
| T-v | 3962–3978 | Appendix A byte-range annotation table (13 rows) |
| T-w | 3998–4026 | Appendix B constants (28 rows) |
| T-x | 4095–4097 | Appendix E changelog |

### 1c. Worked examples (the 21 `**Example**` blockquotes)

513 (`température`), 577 (smallest file), 584 (D1), 1058 (D3), 1196 (D2),
1515 (grid arithmetic), 1569 (ordinals), 1632 (bfloat16), 1681 (channel entry),
1751 (fill tuples), 1872 (interleaved byte layout), 1906 (packed bool plane),
1962 (edge-tile padding), 2086 (segment arithmetic at 10^6 entries),
2101 (planar entry placement), 2200 (slab runs), 2381 (byte-shuffle),
3035 (supersede cost), 3044 (D5–D7), 3209 (D8).

### 1d. Checklists / enumerated lists that function as figures

- Appendix C registry snapshot (4028–4053) — restates T-e, T-h, T-i, T-n.
- Appendix D six design choices (4055–4091).
- Appendix F normative references (4104–4117).
- Appendix G reproducible-writer profile, items 1–10 (4119–4245) plus its
  closing "what they are for" paragraph.
- Appendix H conformance checklists, five class blocks (4247–4317).
- §10.1's four extension vehicles (1375–1379).
- §19.1's four open steps; §19.4's eight tile-read steps; §9.2's six commit
  steps; §20.3's six append steps.
- §18.2's four decoded-document restrictions.

---

## 2. Arithmetic actually performed

I did not eyeball any of these. Scripts: `crc.py`, `appA.py`, `inst.py`.

### 2.1 CRC-32C implementation, checked against §4.5's own check vector

Reflected Castagnoli table, poly 0x82F63B78, init/final 0xFFFFFFFF.

- `CRC32C("123456789")` = **0xE3069283** — matches §4.5 (`83 92 06 E3` LE). ✓
- `CRC32C(<zero bytes>)` = **0x00000000** — matches §4.5. ✓

### 2.2 §7.4's layer-record example (D3), byte by byte

Field walk against T-f's declared order:

```
off  len  field                    bytes                       check
  0    4  name (u8 len + 3)        03 73 73 74                 's'=73 's'=73 't'=74  OK
  4    1  layout                   01                          interleaved          OK
  5    2  linearization            01 00                       row-major            OK
  7    2  codec                    01 00                       none                 OK
  9    2  filter                   01 00                       none                 OK
 11    8  alignment A              00 x8                                            OK
 19    8  slab S                   00 x8                                            OK
 27    8  slab alignment A_slab    00 x8       (forced 0 by S=0, [R-CNT-23])         OK
 35    1  rank d                   01                                               OK
 36    2  channel count C          01 00                                            OK
 38   18  dim entry 'x'            01 78 | 64 00.. | 20 00..   E=100 T=32           OK
 56   12  channel entry 'temp'     04 74 65 6D 70 0C 00 04 00 00 C0 7F              OK
 68    1  index_encoding           01                                               OK
 69    8  entry_count              04 00 ..                    =4                   OK
 77    4  crc_of_crc_array         2E 98 EE C4                 =0xC4EE982E          OK
```

Total 77+4 = **81 bytes**, matching the stated `inline_length = 81` and the
stated decomposition 4 + 34 + 18 + 12 + 13 = 81. I re-derived the "nine scalars"
sum independently: 1+2+2+2+8+8+8+1+2 = 34 over layout, linearization, codec,
filter, A, S, A_slab, rank, C — nine fields, 34 bytes. ✓

Geometry: G = ceil(100/32) = 4, so entry_count = 4 (interleaved, N = 4). ✓
Index region under `[R-CNT-17]`: 4x20 + ceil(4/2^16)x4 = 80 + 4 = **84**. ✓

CRCs, computed:

```
sentinel entry            = FF x16 00 x4                      (20 bytes)
entry array               = sentinel x4                       (80 bytes)
CRC32C(entry array)       = 0x80A34955   -> stored 55 49 A3 80   MATCHES doc
CRC32C(55 49 A3 80)       = 0xC4EE982E                            MATCHES doc
CRC32C(sentinel x 65536)  = 0xEECB3BB2                            MATCHES §15.4/App B
```

All three constants in the document reproduce exactly. The channel-entry bytes
at offsets 56–67 are byte-identical to §12.3's twelve-byte example, as the text
claims ("§12.3's `temp` entry, byte for byte"). ✓

### 2.3 Appendix A's 128-byte file (D9 + T-v), byte by byte

Transcribed the hexdump literally and decoded it:

```
file length                = 128                              OK (= §5.1 minimum)
[0,8)   89 54 41 52 4E 0D 0A 1A                               = §6.1 constant OK
[8,16)  zero                                                  OK
[16,20) 00 00 00 00   directory: 0 record bytes + CRC(0 bytes)=0  OK
[20,64) zero, 44 bytes pre-trailer pad                        64-20 = 44 OK
trailer at [64,128), offsets relative to 64:
  0  magic          8A 4E 52 41 54 0D 0A 1A                   OK
  8  version_major  1                                         OK
 10  version_minor  0                                         OK
 12  flags          0                                         OK
 16  generation     1                                         OK
 24  dir_offset     16                                        >= 16 OK
 32  dir_length     4                                         >= 4  OK
 40  cfl            128   (= file size, 128 mod 64 = 0)        OK
 48  file_id        0x0123456789ABCDEF from EF CD AB 89 67 45 23 01 LE  OK
 56  reserved       00000000                                  OK
 60  CRC            computed CRC32C(trailer[0,60)) = 0xE00938D2
                    stored D2 38 09 E0 = 0xE00938D2           MATCHES
```

Every field offset in T-v matches T-c's trailer layout exactly
(0/8/10/12/16/24/32/40/48/56/60). Appendix A is byte-perfect. Its closing
paragraph's "112 bytes covering [16, 128)" is also right: a 112-byte suffix of a
128-byte file is [16,128), which contains [16,20) and excludes [0,16). ✓

### 2.4 Every other numeric example

- §4.6 `température`: NFC t-e-m-p-é-r-a-t-u-r-e = 10 one-byte + 1 two-byte = **12**;
  NFD `65 CC 81` in place of `C3 A9` = **13**. ✓
- §11.2: extents (1024,2048) tiles (256,256) -> G=(4,8), N=32, P=65,536. ✓
  extents (1000,2048) -> G_y = ceil(1000/256) = 4. ✓
- §11.4: s = t0*G1 + t1; (0,0)->0, (0,1)->1, (1,0)->8. ✓
  (300,700) -> t=(1,2), s=1*8+2=10; u=(44,188), in-tile ordinal 44*256+188 = **11,452**. ✓
  planar C=4: 2*32+10 = **74**. ✓
- §12.1: bfloat16 1.0 = high 16 bits of 0x3F800000 = 0x3F80, LE bytes `80 3F`. ✓
- §14.2: (2,3) P=6; a=uint8,b=uint16 -> Q=3, decoded 18; ordinal (1,2)=1*3+2=5;
  sample at 5*3=15, bytes [15,18). ✓ planar b: 6*2=12 bytes, ordinal 5 at 10. ✓
  t=float32,m=bool -> Q=5, decoded 30, ordinal 5 at [25,30), t 25–28, m 29. ✓
  Cross-check of the closing generalisation: k = u*C + c gives k div C = u and
  k mod C = c, so (k div C)*Q + F_{k mod C} = u*Q + F_c. ✓
- §14.3: (2,5) P=10, alternating from true -> byte0 bits0..7 = 1,0,1,0,1,0,1,0
  = 0b01010101 = **0x55**; byte1 bits0,1 = 1,0 = **0x01**; pad bits 2–7. Fill
  false -> `55 01`; fill true -> 0x01 | 0xFC = **0xFD**. ✓ decoded size ceil(10/8)=2. ✓
- §14.5: extents (5,5) tiles (4,4) -> G=(2,2); edge tile (1,1) covers 4..7 both
  axes; real positions are those with both coords < 5, i.e. exactly (4,4); so
  1 real + **15 padding** of P=16; uint16 fill 0xABCD -> 32 bytes, values 1–15
  each `CD AB`. ✓
- §15.4 (a): entry_count 1,000,000 -> ceil/65536 = **16** segments, 15 full
  (983,040 entries) + last of **16,960**. CRC array 64 bytes. Region
  20,000,000 + 64 = **20,000,064**. k=999,999 in segment 15 at relative index
  16,959 -> byte 339,180. CRC array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000) — 983,040*20 = 19,660,800 and length 339,200 ~ 339 KB.
  Full segment 65,536*20 = 1,310,720 = **1.25 MiB**. All ✓.
- §15.4 (b): planar C=4 N=32, disk ordinal 74 -> region bytes [1,480, 1,500). ✓
  channel 3 block = [96,128) -> "entries 96–127", 32 sentinels. ✓
- §16.2: N=32, S=8 -> runs [0,8),[8,16),[16,24),[24,32). Tile rows 1–2 under
  row-major with G=(4,8) are s in [8,24) = runs 1 and 2 exactly. ✓
- §17.3: s=4, n=3 over `00 00 80 3F | 00 00 00 40 | 00 00 40 40`; output byte
  i*n+j -> `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`. Matches the document's
  `00 00 00 00 00 00 80 00 40 3F 40 40` exactly. ✓
- §19.4 note: entries c*N+s spaced N apart; N >= 2^16 forces different segments
  because floor(k/2^16) strictly increases across a gap of >= 2^16. ✓
- §20.3 note: 10^6 tiles * 20 = 20,000,000 + 64 ~ "about 20 MB". ✓
  §20.3 example: 32*20 + ceil(32/2^16)*4 = 640 + 4 = **644**. ✓
- §21.9 note: 2^32 entries -> 2^16 segments * 4 = 2^18 = **256 KiB**; 2^36 ->
  2^20 * 4 = **4 MiB**. 65,536 layers at 200 B/record = 13,107,200 = **12.5 MiB**. ✓

Nothing in any worked example is arithmetically wrong. I found no numeric defect.

### 2.5 Mechanical checks over the register

Script `inst.py` parses every 6-column row whose first cell matches `^[FLTR]\d+$`,
counts instances as semicolon-separated fields with a bare em-dash counting as
one (that is §21.1's own stated rule: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance").

```
rows 121   instances 273
```

§21.2 claims 36 (F1–F36 present), §21.3 claims 49 (L1–L49 present), §21.4 claims
26 (T1–T26), §21.5 claims 10 (R1–R10). 36+49+26+10 = **121**, and §21.8 claims
"121 conditions over 273 instances". Both numbers reproduce exactly. ✓

Detector/detection-point consistency, scripted: 101 reader rows, 20 verifier
rows; every verifier row is detected at `certification` and no reader row is;
the only non-atomic Detected cell is R1's `open (top-level); layer access
(sub-record)`, which §21.1 licenses by naming §19.2's tiers. ✓

Identifier hygiene, scripted: every `[R-XXX-NN]` prefix is dense from 1 with no
gaps (ENC additionally has the illustrative 100 from §2.2; SER-04 appears only
as the withdrawn-identifier note in §14.4, which §2.2's retirement rule
sanctions). Every bare `(R-XXX-NN)` continuation cite in a Governing-rule cell
resolves to a defined identifier — zero dangling cites. ✓

§15.3's "Six rows are marked *structural*" — I counted the marked rows: crc≠0
sentinel; exactly-one-sentinel; length 0; offset < 16; field > 2^63−1;
sum overflow-or-past-F−64. **Six.** ✓ And they map onto exactly seven §21.4 rows
(T6, T7, T10, T8, T11, and T12+T9 splitting the last), which with T1 gives the
eight index-entry rows the tile register carries. ✓

§21.2's "Four rows are outside that reasoning": F8, F1 (trailer-magic instance),
F14, F6 (+F1's front-block instance). Four named. ✓

§12.1 "exactly thirteen sample types" — 13 rows; "the twelve types other than
bool" — 13−1 = 12, matching §13.2's "For the twelve numeric types". ✓

Appendix B and Appendix C were checked row by row against their defining
sections (§4.5, §4.6, §5.1, §6.1, §6.2, §6.4, §7.1, §7.2, §7.4, §11.3, §12.1,
§15.1, §15.2, §15.4, §16.1, §16.2, §17.2, §18.3, §18.4, §21.9). Every constant,
range and value set agrees. The 8 rows of §10.2's identifier-space table agree
with §7.3, §11.4, §12.2, §14.1, §15.1, §17.2, §17.3 and §18.2 in all four
columns. §21.9's eight-row table agrees with Appendix B's "Reader minimum
guarantees" row item for item. ✓

---

## 3. The implementer's walk — what I built and where I had to guess

I worked the container end to end against the document alone.

**Writer.** I laid out, on paper, a two-channel planar layer: name `grid`,
layout 2, linearization 1, codec 1, filter 1, A=S=A_slab=0, rank 2, C=2,
dimensions `y`/`x` with E=5, T=4 each, channels `v` (uint16, fill 0x0000) and
`m` (bool, fill 0x00). Grid (2,2), N=4, P=16, addressed tiles = C·N = **8**,
index extent_length = 8*20 + ceil(8/2^16)*4 = **164**. Channel 0's plane decoded
size = P·B = 32; channel 1's packed bool plane = ceil(16/8) = **2**, no pad bits.
Disk ordinals 0–3 for channel 0, 4–7 for channel 1 (channel-major, `[R-GEO-06]`).
Inline payload length: 5 (name) + 34 (nine scalars) + 36 (two dim entries) +
7+5 (two channel entries) + 13 (trailing) = **100**. Every one of those numbers
came out of the document without a guess.

Edge padding on tile s=1 (t=(0,1)): a position (u_y,u_x) is real iff
4+u_x < 5, i.e. u_x = 0, so in-tile ordinals 0,4,8,12 are real and the other
twelve are padding. In the packed bool plane that means byte 0 carries real
values at bits 0 and 4 and fill bits elsewhere — `[R-SER-05]`'s "the fill bit in
a packed plane" answers this without ambiguity, and §14.3's Note is explicit
that pad bits (none here, P mod 8 = 0) are a different mechanism from padding
positions.

**Reader.** §19.1's four steps, §6.2's ordered gates, §7.1's directory CRC,
§7.2's framing, §19.3's layer validation, §15.4's two-CRC index chain, §19.4's
eight steps. I could execute all of it. Places I checked twice but that the
document did settle:

- Whether a truncated layer-record name contributes to the duplicate-name
  namespace. §19.1 step 4 settles it: it "yields no name field to compare", so
  it contributes nothing and is layer-scope instead; uniqueness runs over raw
  bytes even for names that are themselves invalid. (Note the register puts
  L23's deadline at *layer access* while §19.1 forces the fit determination at
  *open*; §19.2 licenses earlier detection and §21.1 calls the Detected cell the
  point "by which" detection is due, so the two are consistent. I flag this only
  as something I had to reason about, not as a defect.)
- Whether F for `[R-IDX-03]`'s bound is the committed file length or the
  physical size. §15.3 says "with F the committed file length". Settled.
- Whether the tile-index region is a second coverage claimant beside the layer
  record's extent. §9.7 says it enters the walk once, as that record's extent.
  Settled.
- Whether a sub-1 KiB tile can use codec 3. §17.2's Note works it out
  (single-segment frame only). Settled.
- Whether the byte-shuffle stride divides every decoded image length. Checked
  each of the three layouts: planar numeric L = P·B divisible by B; interleaved
  L = P·Q divisible by Q; packed bool s = 1. Settled.

**Verifier.** Coverage walk per §9.7, overlap per §7.2, slack total per
`[R-CNT-21]`, decoded-content per §14.5/§14.2, alignment/slab per §16, flag bits
per §7.2/§7.3, member ordering per §18.2. The only place my verifier's
obligation list disagreed with the document's own summary is Appendix H — see
finding diagrams-02.

**Updater/compactor.** §20.3's six steps and §20.4's re-emission table. This is
where I had to guess, twice, and both guesses are findings below
(diagrams-01/04/05 on the shrink and re-declaration quantifiers, diagrams-03 on
the layer-set enumeration).

---

## 4. Findings

### diagrams-01 — CONTRADICTION — §11.1 Rationale restates §20.3's shrink bar over the wrong generation, and converts a "not itself an alteration" into a standalone permission

**Location.** §11.1 (Rationale following `[R-GEO-02]`, lines 1481–1494) against
§20.3 step 4 (lines 2989–3003), `[R-WRT-04]`.

**Quotation (§11.1).**

> §20.3 states normatively, and governs, what a commit may do to a layer that
> already stores tiles: a shrink is barred wherever it alters what §14 fixes for
> a tile the new state still stores, and permitted where it drops tiles out of
> the addressed set, whose extents then become slack.

**Quotation (§20.3 step 4).**

> An extent MAY also **shrink**, and the bar above is the whole of the test,
> **in the bar's own tense**: a shrink is permitted exactly where it alters
> nothing §14 fixes for any tile the layer stores in the generation this commit
> supersedes. Dropping a tile out of the addressed set (§11.2's grid count
> falls) is not itself such an alteration — a tile the new state does not
> address carries no §14 obligation and its extent becomes slack — but neither
> does it rescue a commit that damages a prior-generation stored tile. Unstoring
> that tile in the same commit does not rescue it either, and for the same
> reason: the quantifier is the superseded generation's, so a shrink that turns
> real positions into padding of a tile stored there is barred whether or not
> the new state still stores it.

**The two defects in one sentence.**

*(a) The quantifier.* §11.1 quantifies the bar over "a tile the new state still
stores". §20.3 quantifies it over "any tile the layer stores in the generation
this commit supersedes", and then names §11.1's reading as the one it is
rejecting — "barred whether or not the new state still stores it". These are
different domains. Their difference is exactly the set of tiles stored in the
superseded generation and not in the new one, which is a non-empty set: a commit
can unstore a tile (write its entry as the sentinel) or de-address it (shrink the
grid count) in the same breath.

Construction. Layer L, interleaved, rank 1, one uint16 channel, fill 0x0000,
E = 6, T = 4, so G = ceil(6/4) = 2 and tiles 0 and 1 are both stored at
generation g. Tile 1 covers coordinates 4..7: real positions 4 and 5, padding
positions 6 and 7 (which hold `00 00` by `[R-SER-05]`). Position 5 holds a real
non-zero sample. Commit: shrink E to 5 and write tile 1's index entry as the
sentinel. New grid is still ceil(5/4) = 2, so tile 1 stays addressed but
unstored. Under §20.3 this commit is barred — position 5 of a tile stored in the
superseded generation becomes padding, and unstoring it "does not rescue it".
Under §11.1's clause the commit is permitted, because the new state stores no
tile whose §14 obligations changed.

*(b) The permission.* §11.1's second clause reads "and permitted where it drops
tiles out of the addressed set" — a sufficient condition for permission. §20.3
says the same fact is "not itself such an alteration ... **but neither does it
rescue** a commit that damages a prior-generation stored tile" — explicitly not
sufficient. Construction: E = 8, T = 4, G = 2, both tiles stored, no padding
anywhere. Shrink to E = 3: G falls to 1, so tile 1 drops out of the addressed
set (§11.1's permission fires) while tile 0's position 3 turns from real into
padding and must now hold fill. If tile 0's byte pair at position 3 is not the
recorded fill, the resulting live state carries a T4 violation
(`[R-SER-05]`, reject-tile). §11.1's own first clause bars this case too, so
§11.1 is internally under-determined on which clause wins; §20.3 is not.

**Which reading I picked and why.** §20.3's. §11.1 is a Rationale, hence
non-normative under `[R-CNF-01]`, and it says of itself that "§20.3 states
normatively, and governs". An implementer who reads both defers. That deference
clause is what keeps this out of byte-level territory — it is structurally the
same decider as §21.1's "where a row and the rule it cites diverge, the rule
governs".

**What an implementer does wrong without it.** An appender written from §11.1
alone accepts two classes of commit §20.3 forbids: the unstore-and-shrink of
construction (a), whose output is byte-clean and therefore uncatchable (§21.7
says so in terms: "a commit that supersedes every tile it would have damaged
leaves the live state clean, so the bar is unwitnessed there"), and the
drop-out-of-the-addressed-set of construction (b), whose output a verifier does
reject at T4. The second means a writer following §11.1 can emit a nonconforming
file; the first means it can silently violate a MUST no tool will ever surface.

**Byte-level.** No. Both `[R-CNF-01]`'s Rationale exemption and §11.1's own
"§20.3 ... governs" decide the conflict in one direction, so two competent
implementations reading the whole document reach §20.3's answer. What the defect
buys an implementer who stops at §11.1 is a wrong writer, not a disagreement
about a verdict on any given byte sequence.

---

### diagrams-02 — OBSERVATION — Appendix H's verifier checklist omits pad bits from the decoded-content obligations, and pad bits are the one such obligation the document elsewhere insists is a *different* mechanism

**Location.** Appendix H, "Conforming verifier" block (lines 4293–4317), against
`[R-SER-05]` (§14.5), §14.3's distinguishing Note, and §21.4 row T5.

**Quotation (Appendix H, verifier).**

> **Conforming verifier** — every reader obligation, plus the checks readers are
> exempt from: ... alignment and slab invariants (§16); decoded-content
> obligations — padding samples and interleaved boolean bytes (§14.5, §14.2);
> user-metadata member ordering (`[R-MTA-05]`, §18.2); ...

**Quotation (Appendix H, writer — the same appendix, four paragraphs earlier).**

> **Conforming writer** — ... fill-encodes edge padding **and pad bits**
> (`[R-SER-05]`, §14.5); ...

**Quotation (§14.3's Note).**

> Pad bits are not padding positions (§11.3). A padding position is a whole
> sample position outside the layer's extents, arising in any layout; pad bits
> are a packed plane's final-byte unused high bits, arising only when P is not a
> multiple of 8.

**The defect.** The verifier block's list is introduced as "every reader
obligation, **plus the checks readers are exempt from:**" followed by a colon and
an enumeration. I enumerated the twenty verifier-detected register rows
mechanically (F7, F25, F26, F27, F28, F33, F36; L18, L25, L40, L41, L42, L46,
L47, L48, L49; T2, T4, T5, T26) and matched each against a clause of that list.
Nineteen match. **T5 — "In a packed planar bool plane with P mod 8 ≠ 0, a
final-byte pad bit (bit positions P mod 8 through 7) is not the channel's fill
bit"** matches none of them: it is not a "padding sample" (§14.3's Note says so
in as many words) and it is not an "interleaved boolean byte" (it arises only in
a *planar* plane). The same appendix names pad bits explicitly in the writer
block, so the omission is an asymmetry inside one figure, not a house style.

The knock-on is that T26's packed-planar-bool instance — "packed planar bool:
identity s = 1", a byte-shuffle applied at a stride other than 1 to a packed
plane — is witnessed only by T5 for a plane whose padding positions all happen
to hold fill, so a verifier built from this checklist loses that instance too.

**Permitted readings.** (i) The dash-list is an exhaustive enumeration of the
decoded-content obligations, in which case pad bits are omitted from a checklist
that promises the "checks readers are exempt from". (ii) "decoded-content
obligations" is the head and the dash-list is illustrative, the parenthetical
"(§14.5, §14.2)" carrying the real scope — and §14.5 does cover pad bits. I
picked (ii), because Appendix H is labelled non-normative and opens with "each
entry's authority is the requirement or section cited, never this summary". But
(i) is the natural reading of a colon-introduced list of exempt checks, and it is
the reading the writer block's parallel clause invites, since that one bothered
to say "and pad bits".

**What an implementer does wrong without it.** A verifier audited against
Appendix H skips `[R-SER-05]`'s pad-bit half and certifies files carrying T5
(and the packed-bool instance of T26). Since no reader is obliged to detect
either, such a file circulates as certified.

**Byte-level.** No. `[R-SER-05]` and §21.4's T5 both state the obligation
normatively, and Appendix H disclaims its own authority in its opening sentence,
so the verdict on any given file is already fixed by text that outranks the
checklist.

---

### diagrams-03 — CONTRADICTION — §20.4's table names "removing a layer" as a change a commit makes; the paragraph immediately below the table says no commit removes a layer record

**Location.** §20.4, the MU = 0 / PE = 0 row of the updater-obligations table
(line 3121), against §20.4's own next paragraph (lines 3123–3131).

**Quotation (table cell).**

> An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: ... for a top-level record, the file's layer set
> — which a commit changes by adding or removing a layer and equally by
> modifying any layer's record — or another *non-layer* top-level record.

**Quotation (next paragraph).**

> No commit therefore removes a layer record, or a user-metadata record at
> either scope. Both registered types carry PE = 1, and an in-place removal
> would strand that layer's stored tiles and index region as slack (§5.2) which
> only compaction reclaims ...

**The defect.** The table cell enumerates three ways a commit changes the file's
layer set — adding a layer, removing a layer, modifying any layer's record — and
one of the three is an operation the document forbids outright. I checked every
route: a layer record is type 0x0001, whose registry-fixed flags are MU = 1,
PE = 1 (§7.3, Appendix C); §20.4's table gives PE = 1 records "Retain
byte-identical"; §20.5 says a compactor's output carries the live committed state
"less any record §20.4 lets it drop", and §20.4 lets it drop only MU = 0 / PE = 0
records, so compaction does not remove a layer either — §20.4 says as much
("That is not compaction, which carries every layer of its input forward
(§20.5)"). The only way to a file without a layer is a whole-file rewrite under a
fresh file_id, which is not a commit (`[R-LIF-01]`, §20.4). So "removing a layer"
names an operation with no realisation.

**Permitted readings.** (i) The clause is a definition of what changing a layer
set *means*, listing removal for symmetry even though removal is unavailable —
harmless, because the drop licence is then never triggered by it. (ii) The clause
licenses a commit that removes a layer, in which case it contradicts the
paragraph beneath it and Appendix H's "never removes a layer record, or a
user-metadata record at either scope (§20.4)". I picked (i): the paragraph and
the Appendix H checklist agree against the table cell, two to one, and §21.1's
principle that a restatement yields to the rule it restates applies by analogy.

**What an implementer does wrong without it.** An updater author reading the
table row before the paragraph beneath it builds a layer-removal path. Its
output would either strand the layer's tiles and index as slack (the paragraph's
own objection) or, worse, be taken as licence to omit a PE = 1 record from a
re-emitted directory, which `[R-WRT-05]` forbids.

**Byte-level.** No. The condition is unsatisfiable: no file can exhibit a commit
that removed a layer, because removal is barred by a rule stated three ways
(§20.4's paragraph, the table's own PE = 1 rows, `[R-WRT-05]`). Nothing about
which bytes are accepted, rejected or emitted turns on the dead branch — the harm
is to the reader of the table, not to any file.

---

### diagrams-04 — AMBIGUITY — §20.3 step 4's shrink paragraph states a flat bar that drops the "already holds the fill" carve-out the same step states for the same rule

**Location.** §20.3 step 4, `[R-WRT-04]` (lines 2961–2967 against 2999–3003).

**Quotation (the carve-out, in the growth half of step 4).**

> The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: a change that leaves every one of
> those tiles' stored bytes meaning exactly what they meant — a filter whose
> mandated stride makes it the identity (`[R-COD-10]`), or a new padding
> position whose stored byte already holds the fill `[R-SER-05]` fixes — is not
> what this bars.

**Quotation (the shrink half, ten lines later).**

> ... so a shrink that turns real positions into padding of a tile stored there
> is barred whether or not the new state still stores it.

**The defect.** The shrink sentence opens by importing the whole of the bar —
"the bar above is the whole of the test, **in the bar's own tense**" — and then
states as flatly barred a class the bar itself expressly carves out. "A new
padding position whose stored byte already holds the fill `[R-SER-05]` fixes"
*is* a real position turned into padding; the carve-out exists precisely for it.

Construction. Layer L, rank 1, one uint16 channel, fill 0x0000, E = 6, T = 4,
tile 1 stored, its four bytes for positions 4..7 being `xx xx 00 00 | 00 00 00 00`
— i.e. position 5's sample happens to be the fill value 0x0000, as does the
padding at 6 and 7. Shrink E to 5. Position 5 becomes padding and `[R-SER-05]`
now fixes its content to fill — which it already is. Nothing §14 fixes has been
altered: the stored bytes mean exactly what they meant. Under the carve-out the
commit is permitted; under the flat sentence it is barred.

**Permitted readings.** (i) "turns real positions into padding" is shorthand for
"turns real positions into padding *and thereby breaks §14.5*", so the carve-out
survives and the sentence is about tense only. (ii) The sentence is a second,
independent bar with no carve-out, in which case §20.3 contradicts itself within
one step. I picked (i): the sentence's own preamble says the bar above "is the
whole of the test", and its stated purpose ("the quantifier is the superseded
generation's") is the tense, not the content. But the sentence as written admits
(ii), and (ii) is what a reader who reaches the shrink paragraph without holding
the growth paragraph in mind will take.

**What an implementer does wrong without it.** An appender that adopts (ii)
refuses a class of commits the document permits — every shrink into a fill-valued
position, which for the very common all-zero-fill default is a large class.
Refusing is safe but it drives callers to the whole-file rewrite §20.3 itself
warns costs more.

**Byte-level.** No. The disagreement is over whether a commit is *available*, and
in the disputed class the file either implementation would emit is conforming
either way — the byte at the disputed position holds fill, which is what
`[R-SER-05]` requires of it as padding and what `[R-TYP-05]` permits of it as a
sample. No verifier verdict and no reader outcome differs; only one writer
refuses where the other proceeds.

---

### diagrams-05 — CONTRADICTION — §20.3's shape-(c) example widens the free-re-declaration licence to "whatever its geometry", which the same step's own proviso denies, and conflates "stores no tile" with "addresses no tile"

**Location.** §20.3, the Example "the three shapes a commit takes", shape (c)
(lines 3076–3086), against §20.3 step 4's permission and its proviso
(lines 2974–2987), `[R-COD-07]` and §21.3 row L44.

**Quotation (shape (c)).**

> A layer storing no tile is re-declared freely whatever its geometry, which is
> the same step's permission.

**Quotation (the step's permission and proviso).**

> A layer that stores no tile **in the generation this commit supersedes** MAY
> be re-declared freely, which is what schema-first creation needs (§11.1) — the
> tense is the bar's, so a commit does not earn this permission by emptying the
> layer as it re-declares it; and an extent MAY **grow**, since a position that
> becomes real held that channel's fill and fill is a legal sample value —
> provided the grown geometry stays within every bound the layer's own
> declarations impose, `[R-COD-07]`'s lz4 decoded-size cap among them (L44),
> which an empty layer escapes only because that cap is quantified over
> addressed tiles.

**Quotation (§17.2's Note, which fixes what "empty layer" means there).**

> The cap is quantified over the layer's *addressed* tiles, so a layer that
> addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
> whatever its tile shape declares, and codec 4 is conforming there.

**The defect, in two moves.** First, the example adds "whatever its geometry" to
a permission whose normative statement carries no such phrase and whose sibling
clause, in the same sentence, spends a full line saying that geometry is exactly
what must stay "within every bound the layer's own declarations impose". Second,
it applies that widened permission to "a layer storing no tile", whereas the
escape §20.3 names belongs to an *empty* layer — one that **addresses** no tile.
Those are different classes: a layer with E = (1000,) and every index entry the
sentinel stores no tile and addresses a thousand.

Construction. Layer L declares codec 4 (lz4), interleaved, rank 1, one uint8
channel, E = 1000, T = 1000. Addressed tiles = 1, decoded size P·Q = 1000 bytes,
well inside `[R-COD-07]`'s 0x7E000000 cap; every entry is the sentinel, so the
layer stores no tile. A commit re-declares T = 0x7E000001 (leaving E alone, so
G = ceil(1000/0x7E000001) = 1 and the layer still addresses exactly one tile).
Decoded size is now 0x7E000001 > 0x7E000000. Shape (c) says this is free
"whatever its geometry". `[R-COD-07]` and L44 make the resulting layer a
layer-scope validity error, and `[R-CNF-05]` makes the writer nonconforming for
emitting it. Note that no tile is stored, so §20.3's *bar* genuinely does not
reach the commit — the only thing stopping it is the geometry proviso the
example dropped.

**Permitted readings.** (i) "freely" means free of *this step's bar*, and every
other rule still applies by `[R-CNF-05]`, so "whatever its geometry" is loose but
harmless. (ii) "whatever its geometry" means what it says, and geometry is not
among the things a re-declaration must keep within bounds. I picked (i) — the
step's own proviso and `[R-CNF-05]` outrank a non-normative Example — but (ii) is
the plain reading of "whatever", and the example volunteers the word in the one
place where the normative text takes pains to bound geometry.

**What an implementer does wrong without it.** An appender re-declares an
all-sentinel codec-4 layer past the lz4 cap, or past `[R-ENC-04]`'s 2^63−1
ceiling on N, P, N·P, C·N, P·Q or P·B, and emits a file whose layer every
conforming reader must reject at layer access (L44, L2). The example's "which is
the same step's permission" invites the reader not to go back and check the step.

**Byte-level.** No. The output is decided against the file by rules the example
does not touch: L44 and L2 are reader-detected layer-scope rows with a fixed
outcome, so two verifiers reading this text agree the resulting layer is
rejected. The fork is in what a writer believes it may produce, and
`[R-CNF-05]`'s "A writer MUST emit only conforming files" closes it independently
of the example.

---

## 5. Things I checked and did not report

Recorded so the coverage claim is auditable, and so a later pass can see what I
declined and why.

- **§6.1's table omits a Name/Field column** (Offset | Size | Value | Class),
  where §4.7's Note says layout tables give "byte offset ..., size, type, name,
  taxonomy class, and valid range" and then says only that "§6.1's block is a
  16-byte constant, where a Value column replaces type and range". The two fields
  do have names elsewhere (Appendix A: "front signature magic", "front signature
  reserved"; F6's instances). Not reported: the same Note ends "each table giving
  the columns its structure needs", which licenses the omission.
- **§21.1's specialization list is not exhaustive.** "F1 of F6 and of F8, F35 of
  F36, L24 of L25" omits at least T11 ⊂ T9, T12 ⊂ T9, F2's dir_offset instance
  ⊂ F10, and L46 ⊂ L49 (a layer record with MU = 1 / PE = 0 also mismatches the
  registry's fixed PE = 1). Not reported: the sentence says "Some rows are", not
  "the rows that are", and in every unlisted pair the detector, detection point
  and outcome coincide, so nothing turns on which row a file is recorded against.
- **§21.7's "witnessed only where ... *and* ..." immediately followed by "a
  change that reaches the decoded size or the codec instead is witnessed by T3 or
  T14"** reads as an "only if" contradicted by its own next clause. Not reported:
  the intended parse (the "only" governs the storedness condition, the two
  branches are alternative witnesses) is coherent and is the only one that makes
  the sentence do work.
- **§20.5's "regenerates each *relocated* tile-index region"** is conditioned on
  relocation, whereas what forces regeneration is a change in entry offsets. A
  compactor that happened to place a region at its input offset while moving that
  layer's tiles would, read literally, owe no regeneration. Not reported: the
  output must be a conforming file (`[R-CNF-06]`) whose reference arrays equal
  the input's bit for bit (`[R-WRT-07]`, `[R-MDL-02]`), which forecloses it, and
  the coincidence is not constructible in any realistic generation-1 layout.
- **`[R-WRT-06]`'s "MUST NOT emit a file carrying a violation it has detected"
  against `[R-WRT-07]`'s carve-out** for an entry §15.3 classifies reject-tile on
  a structural ground. A compactor must classify such an entry to know it has no
  extent to re-point, which is detection. Not reported: `[R-WRT-07]` names
  `[R-WRT-06]` and settles it explicitly ("such an entry is not one `[R-WRT-06]`
  obliges a compactor to refuse").
- **L23's Detected cell says "layer access" while §19.1 step 4 forces the
  name-field fit determination at open.** Not reported: §21.1 calls the Detected
  cell the point "by which" detection is due and §19.2 licenses earlier
  detection, so an earlier mandatory point for one instance is consistent.
- **§21.6's "The file contains zero layers | A conforming file with an empty
  directory"** conflates zero layer records with an empty directory (a file with
  zero layers may still carry a file-scope user-metadata record). Not reported:
  `[R-CNT-14]`, the rule the row cites, makes the same elision, so the row is a
  faithful restatement and the defect, if any, is not the figure's.
- **§20.3's "A layer whose record alone changes keeps its extent slot ...
  (`[R-WRT-05]`)"** cites the byte-identical-re-emission rule for a record that
  is by hypothesis logically modified, so `[R-WRT-05]` does not reach it. Not
  reported: the citation is right for the clause's second half ("as does a layer
  the commit leaves untouched") and nothing normative rides on it.
- Every count claim in the document reproduces: 36 / 49 / 26 / 10 rows, 121
  conditions, 273 instances, six *structural* rows in §15.3, four rows outside
  §21.2's version-gate reasoning, thirteen sample types, twelve numeric types,
  four codecs, two filters, two layouts, two metadata encodings, six
  standardized keys, four extension vehicles. None is wrong.
- Every worked example's arithmetic reproduces; every CRC constant in the
  document reproduces from an implementation validated against §4.5's own check
  vector; Appendix A is byte-perfect against §6.2's layout and §7.1's CRC rule.

**Finding count in this transcript: 5.**
