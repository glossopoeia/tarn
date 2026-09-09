# Round 34 — Reader implementer, working transcript

## 0. Disclosure, up front

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in five `Read` calls covering lines 1–4838 (the file is 4,838 lines, 48,163 words by
`wc -w`). The brief said the document is about 48,200 words; `wc -w` says 48,163, close
enough that I did not treat the difference as signal.

I opened no other file. I ran no `git` command, no directory listing, no web access. I ran
`grep`/`rg`-equivalent searches only as Python `re` over that one file's text, and three
Python scripts that read no file except that one:

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-round/scratch/reader/rdr_crc_check.py`
  — CRC-32C implementation and constant checks; reads nothing.
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-round/scratch/reader/rdr_count_instances.py`
  — parses the §21 register tables out of `spec/tarn.md` and counts rows and instances.
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-round/scratch/reader/rdr_register_audit.py`
  — detector/detection-point consistency over the same tables.
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-round/scratch/reader/rdr_build_file.py`
  — builds a conforming 256-byte TARN file from the document's rules alone and reads it
  back through §19.1/§19.3/§19.4; writes `worked_file.tarn` into my own scratch directory.

Two more inline `python3 - <<PY` heredocs ran phrase searches with blockquote markers
stripped and whitespace normalised (the brief's hard-wrap warning); they read only
`spec/tarn.md`.

I created my scratch directory myself and wrote only into it, plus this one output file.
I did not read or list the output directory.

**Context I did not ask for.** My runtime placed material in my context before I began: a
project instruction file (`CLAUDE.md`, which forwards to `AGENTS.md`), a user auto-memory
index listing a dozen or so TARN-related memory titles, a git status snapshot with recent
commit subject lines, an attribution notice, and an MCP server instruction block. I did not
open any of the files those things named, and I have not used any of their contents as
evidence about the specification. The git subject lines in particular name a round number
and describe prior repairs; I read them only as far as they scrolled past and did not act
on them. Naming that they appeared, per the brief.

**Paths.** The spec was exactly where the brief said it would be. My scratch directory did
not exist; I created it. The output directory did not exist; I created it with `mkdir -p`
before writing this file. Nothing about the path layout carried information the brief
withheld, so far as I could tell.

---

## 1. What I built

A conforming reader, on paper and then partly in code. I walked it in the order I would
actually write it: open, validation timing, layer access, tile read, degradation, and a
worked file. I stopped at every point where I had to guess and recorded it.

---

## 2. The open path, byte-exact

### 2.1 Step 1 — end of file

`[R-RDR-01]` step 1: obtain the transport-authoritative file size F (`[R-CNT-10]`). An F
below 128 is reject-file from F alone (`[R-CNT-27]`, F5).

`[R-CNT-10]` fixes "transport-authoritative" as "a full-response content length, the
complete length of a range response, or a size probe", and bars substituting the trailer's
own `committed_file_length`. That is exactly what I needed: the naive implementation
(trust the trailer) is explicitly forbidden, so F17 is reachable.

I derived the 128 floor myself rather than taking it: `dir_offset ≥ 16`, `dir_length ≥ 4`
give a directory end ≥ 20; `dir_offset + dir_length ≤ F − 64` gives F ≥ 84; F a multiple of
64 gives F ≥ 128. The document's own derivation in `[R-CNT-27]` matches. F = 64 would need
the directory to end at or before offset 0.

### 2.2 Step 2 — trailer

Fetch [F − 64, F). Validate in `[R-CNT-06]`'s fixed order, which is a *partial* order and
the document says so: magic, then trailer CRC, then the version gate — "only these touch
fields whose positions are fixed across all majors (`[R-CNT-24]`)" — and then, those three
passed, all of: flag gates; `committed_file_length` = file size and a multiple of 64;
`dir_offset ≥ 16`; `dir_length ≥ 4`; `dir_offset + dir_length ≤ F − 64`; `file_id ≠ 0`;
reserved bytes zero.

I counted the conditions `[R-CNT-06]` states, because §2.3 asserts it states nine. Register
rows whose Governing rule cell names `[R-CNT-06]` first: F8, F9, F10, F12, F13, F14, F15,
F16, F17 — **nine**. §2.3 says two of them (trailer magic, trailer CRC) assert invariants
`[R-CNT-24]` fixes and "the other seven do not": 2 + 7 = 9. Consistent.

The version gate is `[R-CNT-07]`'s (F18) and the flag gates `[R-CNT-08]`'s (F19), which is
why they are not among `[R-CNT-06]`'s nine even though §6.2 lists them in the same
sentence. I had to read that twice.

### 2.3 Step 3 — directory

Fetch [dir_offset, dir_offset + dir_length); verify the final 4 bytes against CRC-32C over
the preceding dir_length − 4 (`[R-CNT-11]`, F20) before any other use.

### 2.4 Step 4 — record walk

Parse under §7.2's framing. Per §19.1 step 4 the open applies: the MU gate for unknown
top-level types (`[R-CNT-15]`), the per-type multiplicity rules (`[R-CNT-14]`), the
extent-slot validity rules **for non-layer top-level records** (`[R-CNT-13]`), the extra
framing rules a top-level user-metadata record carries (no (0,0) slot, extent_length ≥ 5,
inline_length exactly 1), and the layer-name namespace.

The "non-layer" qualifier is load-bearing and correct: a layer record's extent slot is
checked at layer access, not at open, and the register agrees — F30/F31/F32 say "A
non-layer top-level record's extent slot…" and are reader/open; L15/L16/L17 cover a layer
record's or sub-record's slot and are reader/layer access. This is the kind of split that
is usually wrong somewhere; here it is not.

### 2.5 Byte-exact cold remote open

Against a server supporting ranged requests, for the Appendix A file (F = 128):

| # | Range | Bytes | What bounds it before I have read it |
|---|---|---|---|
| 1 | suffix, final 64 bytes → [64, 128) | 64 | the constant 64 from §6.2; a suffix range needs no prior knowledge, and its response carries F (`[R-CNT-10]`) |
| 2 | [dir_offset, dir_offset + dir_length) = [16, 20) | 4 | `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64`, all validated in §6.2's order and all covered by the trailer CRC already verified (`[R-ENC-05]`, `[R-ENC-10]`) |

**Two requests, 68 bytes.** No third request: [0, 16) is not resident, and `[R-CNT-04]`
lets a reader that would have to fetch it defer or omit the check. Appendix A states the
same and adds the 112-byte-window variant; I checked that a 112-byte suffix of a 128-byte
file is [16, 128), which contains [16, 20) and excludes [0, 16). Both true.

In general the open is 2 requests: 64 bytes plus `dir_length`. The speculative variant is 1
request of whatever window the reader picks, and if the window reaches offset 0 the front
block becomes resident and `[R-CNT-04]`'s equality check becomes mandatory. `[R-RDR-01]`
says the open's I/O is independent of layer count and file size; I could not construct a
counterexample — step 4 needs no fetch, and the layer-name namespace is built from bytes
already in the directory.

A **remote verifier** costs one more: §2.3 gives it no residency exemption, so it must
fetch [0, 16). Appendix H says this explicitly and F6's condition text says it too.

---

## 3. Validation timing by tier

`[R-RDR-02]` fixes the *latest* detection point, in four tiers, and §19's preamble supplies
the governing clause I needed twice: "Those enumerations are not the complete inventory of
what a reader detects at that tier: §21's register is, and `[R-CNF-04]` binds a reader to
every register row whose detector is the reader, at the tier that row's *Detected* cell
names." Without that sentence I would have filed two findings; with it, both die. I record
them below as rejected candidates rather than pretend I did not chase them.

I audited the register's Detector/Detected columns mechanically. 120 rows: 100
reader-detected, 20 verifier-detected. **Every** verifier row is at *certification* and
**no** reader row is. The 20 verifier rows are F7, F25, F26, F27, F28, F33, F36; L18, L25,
L40, L41, L42, L46, L47, L48, L49; T2, T4, T5, T26.

**What a reader is permitted never to check** — I assembled this from the rule text and
then checked it against exactly that list of 20:

- live-state coverage and the slack total (§5.2's Note: "Coverage is checked by verifiers,
  never by readers"; §9.7) — F33, L18
- a structure in the pre-trailer gap (`[R-CNT-05]`: "readers check neither, their check
  being the dir-bounds rule of `[R-CNT-06]`") — F7
- record flag bits: reserved 2–15, MU = 1 with PE = 0, and a registered type's stored bits
  (`[R-CNT-12]`, `[R-CNT-22]`) — F25, F26, F28, L46, L47, L49
- a reserved-range record or sub-record type value whatever its MU bit (`[R-CNT-15]`) —
  F36, L25
- alignment and slab invariants (`[R-SLB-01]`, `[R-SLB-03]`: "readers are not obligated
  to") — L40, L41, L42
- padding content and pad bits (`[R-SER-05]`: "is not obligated to check it") — T4, T5
- interleaved bool byte values (`[R-SER-08]`: "A reader is not obligated to screen decoded
  content") — T2
- a mis-strided filter (`[R-COD-10]`, detected through T2's or T4's check) — T26
- user-metadata member ordering (`[R-MTA-05]`: "readers process the document unchanged") —
  F27, L48
- the front signature block when the open does not leave it resident (`[R-CNT-04]`) — this
  is the one exemption that is *not* a verifier-detector row: F1 and F6 stay reader-detected
  and the exemption is inside the condition text. Appendix H says the same. I checked
  this specifically because it is the shape that usually goes wrong, and it does not.

The list closes exactly. 20 verifier rows, 20 accounted for.

**What becomes a verdict when.** `[R-CNF-11]`: an established violation always outranks an
unchecked requirement — "a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check, and *cannot establish*
is available only to a traversal that established no violation". *Unexamined* constrains
the report and not the verdict, and so does the per-requirement capability report. Three
verdicts; I checked the word "three" against the enumeration and it is three.

---

## 4. Layer access

`[R-RDR-03]` enumerates the full validation of a layer record. I checked its enumeration
against every L-row whose Detected cell is "layer access" and found a citation for each:

L1 → §4.2 value domain; L2 → `[R-ENC-04]` plus `[R-SER-02]`/`[R-SER-07]`; L4/L7/L8/L9 →
the dimension- and channel-name rules; L10/L11/L12 → the user-metadata sub-record framing
rules, spelled out inline; L13/L14/L23 → the exact parse and sub-record walk
(`[R-CNT-18]`, `[R-CNT-12]`); L15/L16/L17 → the slot's validity rules; L19 →
`[R-CNT-14]`; L20 → `[R-CNT-16]`; L21/L22 → the index cross-checks computable without I/O;
L24/L26 → `[R-CNT-18]`; L27/L28/L29/L30 → the §7.4 constraint set; L31/L33/L34/L36/L43/L45
→ "the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3"; L32 → the geometry
floor; L35 → the per-type fill constraints; L39 → §7.4's table via `[R-CNT-23]`; L44 →
"the codec declaration bounds (`[R-COD-07]`)".

Only L3/L5/L6 (the layer record's own name) fall outside, and they are at *open*, which
§19.1 step 4 places there. Complete.

"All are decidable from the resident directory and F: layer access performs no fetch." I
checked the awkward ones: L22's formula is arithmetic on `entry_count`; L44's cap is
arithmetic on declarations; L2's nine derived quantities are all products or sums of
declared fields. None needs a byte outside the directory. True.

---

## 5. Layer access to decoded samples — the tile-read algorithm

From a layer name and a coordinate:

1. **Domain** (`[R-RDR-04]` step 1). Point request: `0 ≤ xᵢ < Eᵢ`; a coordinate outside
   "fails as a request, with no verdict on the file". Region request: the intersection with
   the extents; wholly outside, or any region of a zero-extent layer, succeeds and returns
   no samples. Note the deliberate asymmetry — "a range whose every interval holds a single
   position **is a region request**" — so the same single position gets opposite treatment
   by request *form*. I looked hard at this and it is stated on purpose, not by accident.
2. **Ordinals** (`[R-GEO-06]`). `tᵢ = xᵢ div Tᵢ`, `uᵢ = xᵢ mod Tᵢ`; in-tile ordinal
   `Σ uᵢ ∏_{j>i} Tⱼ` (row-major "for every linearization value, permanently"); spatial
   ordinal `s = Σ tᵢ ∏_{j>i} Gⱼ`; disk ordinal `s` interleaved, `c·N + s` planar.
3. **Index chain.** Fetch the CRC array at region bytes
   `[entry_count·20, entry_count·20 + ⌈entry_count/2¹⁶⌉·4)` and the segment containing k at
   `[s·2¹⁶·20, min((s+1)·2¹⁶, entry_count)·20)`; verify `crc_of_crc_array` then the segment
   CRC (`[R-IDX-04]`, L37/L38, reject-**layer** though detected at tile use — `[R-RDR-02]`
   says so explicitly). Both ranges come from the layer record alone, so `[R-ENC-05]`'s
   "no I/O on an unverified integer" holds: the layer record is inside the directory, whose
   CRC is already verified.
4. **Entry.** Classify per §15.3. Seven structural rows (T6–T12), a valid sentinel, T1, and
   three verifier rows.
5. **Payload.** Fetch [offset, offset + length); verify the entry's crc (T1) before decoding.
6. **Decode.** Codec first, then the filter's inverse (`[R-COD-01]` — writer order is
   filter then codec, reader order is codec then inverse filter; I checked the direction
   twice). Then the exact-size rule `[R-SER-07]` (T3).
7. **Extract.** §14's offset arithmetic. Padding positions never returned (`[R-GEO-04]`).
8. **Return.** Bit patterns unaltered, with `[R-SER-08]` the single resolved case.

**Cold remote cost of one tile:** 3 requests — CRC array, segment, payload — the first two
parallelisable (`[R-IDX-04]`). §1's pillar says the same. For §15.4's worked layer
(entry_count = 1,000,000) I re-derived the figures: 16 segments (15 full at 65,536, the
last 16,960); CRC array 64 bytes at region [20,000,000, 20,000,064); index region
1,000,000·20 + 64 = 20,000,064 bytes; tile 999,999 sits in segment 15 at segment-relative
byte 20·(999,999 − 983,040) = 20·16,959 = 339,180; segment 15 spans
[983,040·20, 20,000,000) = [19,660,800, 20,000,000), i.e. 339,200 bytes. The document says
"~339 KB" and "never more than one full segment (1.25 MiB) plus the CRC array"; one full
segment is 65,536·20 = 1,310,720 = 1.25 MiB. Every figure reproduces.

### 5.1 The exact decoded byte layout

- planar numeric channel c: `P · Bᶜ` bytes; value k at `k · Bᶜ`.
- interleaved: `P · Q` bytes with `Q = Σ Bᵢ`; value k at `(k div C)·Q + F_{k mod C}` where
  `Fᶜ = Σ_{j<c} Bⱼ`. Equivalently channel c at in-tile ordinal u sits at `u·Q + Fᶜ`; I
  verified the substitution `k = u·C + c` gives `k div C = u`, `k mod C = c`.
- planar bool: `⌈P/8⌉` bytes, LSB-first, value k at bit `k mod 8` of byte `k div 8`.

I checked §14.2's worked example arithmetic: tile extents (2,3), P = 6, channels a(uint8)
b(uint16) → Q = 3, decoded size 18, ordinal 5 at bytes [15,18); planar b's plane 12 bytes,
ordinal 5 at 10–11; t(float32)+m(bool) interleaved → Q = 5, size 30, ordinal 5 at [25,30)
with m the single byte at 29. All correct. §14.3's example: P = 10 alternating from true →
byte 0 = 0x55, byte 1 = 0x01 with six pad bits, and 0xFD with fill true. Correct.
`[R-COD-10]`'s shuffle example on 1.0/2.0/3.0 float32 (s = 4, n = 3) reproduces
`00 00 00 00 00 00 80 00 40 3F 40 40` byte for byte.

I also checked that `L` is divisible by `s` in every case as `[R-COD-10]` claims: planar
numeric L = P·Bᶜ with s = Bᶜ; interleaved L = P·Q with s = Q; packed bool L = ⌈P/8⌉ with
s = 1. It is.

---

## 6. A worked file, built from the document and read back

Appendix A's file I checked constant by constant (§7 below). Then I built my own, because
Appendix A has no layer and therefore exercises none of Part II.

**Design.** Layer `sst`, rank 1, dimension `x` with E = 4, T = 2; interleaved; one uint8
channel `t` with fill 0x00; codec 1, filter 1; no alignment, no slab; linearization 1;
index_encoding 1. Tile 0 stored as `11 22`; tile 1 the sentinel.

**Derived, by me, from the rules:**

- `G₀ = ⌈4/2⌉ = 2`, `N = 2`, `P = ∏Tᵢ = 2`, `Q = 1`, decoded size `P·Q = 2`.
- addressed-tile count = N = 2 (interleaved) → `entry_count = 2`.
- segments `⌈2/2¹⁶⌉ = 1`; index `extent_length = 2·20 + 1·4 = 44` (`[R-CNT-17]`).
- layer-record inline payload: 4 (name) + 1 + 2 + 2 + 2 (layout, lin, codec, filter)
  + 24 (A, S, A_slab) + 1 + 2 (rank, C) + 18 (one dimension entry) + 6 (one channel entry)
  + 1 + 8 + 4 (trailing fixed) = **75** bytes. The record is 24 + 75 = 99; the directory is
  99 + 4 = **103**.

**Placement:** front [0,16); tile 0 [16,18); index region [18,62); directory [62,165); pad
[165,192); trailer [192,256). F = 256, the least multiple of 64 with
`dir_offset + dir_length ≤ F − 64` (165 + 64 = 229 → 256). Pre-trailer pad 27 bytes.

**Read-back.** I then ran §19.1's four steps, §19.3's layer validation and §19.4's eight
steps against those bytes as a separate pass, asserting each register row by label. Every
assertion passed; the sample at x = 1 came back 0x22, and x = 2, 3 resolved to the
sentinel and read as fill 0x00. Nothing in the round trip required me to invent a rule.
That is the single strongest thing I can say for this document: a reader is buildable from
it, and I built one.

The one place I had to think rather than read: §7.4's layout table gives the payload in
order but no offsets (by design — §4.7's Note says a packed variable-length payload has
none), so I derived the packing from "fields are packed in table order with no alignment or
padding between them" in `[R-CNT-18]`. That is sufficient. I cross-checked my 75-byte
result against §7.4's own 81-byte worked example by re-deriving its arithmetic: name 4, the
nine scalars from layout through channel count 34, dimension entry 18, channel entry 12,
trailing fixed 13 → 81. The document's summation is right, and its per-field offsets in the
hex block are right.

---

## 7. Constants and checksums I recomputed

I implemented CRC-32C from §4.5's parameters alone (polynomial 0x1EDC6F41 reflected to
0x82F63B78, init 0xFFFFFFFF, reflected in/out, final XOR 0xFFFFFFFF) and checked:

| Quantity | I computed | Document states |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 ✓ |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 ✓ |
| Appendix A trailer CRC over [0,60) | 0x402F157E → `7E 15 2F 40` | 0x402F157E / `7E 15 2F 40` ✓ |
| §7.4 example: CRC over 80 bytes of 4 sentinel entries | 0x80A34955 → `55 49 A3 80` | 0x80A34955 / `55 49 A3 80` ✓ |
| §7.4 example: crc_of_crc_array over that 4-byte array | 0xC4EE982E → `2E 98 EE C4` | 0xC4EE982E / `2E 98 EE C4` ✓ |
| §15.4: CRC of a full 2¹⁶-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 ✓ |
| Appendix A file_id 0x0123456789ABCDEF little-endian | `EF CD AB 89 67 45 23 01` | same ✓ |

Every stated checksum in this document is correct. That is not something I assumed.

Other numbers I derived and compared:

- §5.1 / Appendix A: 128-byte floor, directory [16,20), pad [20,64) = 44 bytes, trailer
  [64,128). Consistent, and 20 + 44 = 64.
- §9.2's Note: prior F + 68 rounded up to a multiple of 64 is prior F + 128. Correct.
- §11.2 example: extents (1024, 2048), tiles (256,256) → G = (4,8), N = 32, P = 65,536. ✓
- §11.4 example: (300,700) → tile (1,2), s = 1·8+2 = 10; in-tile (44,188), ordinal
  44·256+188 = 11,452; planar channel 2 → 2·32+10 = 74. ✓
- §15.4 second example: ordinal 74 at region bytes [1,480, 1,500) = [74·20, 75·20). Channel
  3's entries 96–127 = [3·32, 4·32). ✓
- §14.5 example: extents (5,5), tiles (4,4) → grid 2×2; edge tile (1,1) covers 4–7 on both
  axes, one real position (4,4) and 15 padding; 32 bytes with values 1–15 each `CD AB`. ✓
- §20.3 example: 32-tile interleaved index region = 32·20 + 4 = 644. ✓
- §21.9's Note: at 2³² entries the CRC array is ⌈2³²/2¹⁶⌉·4 = 2¹⁶·4 = 256 KiB, and at 2³⁶ it
  is 2²⁰·4 = 4 MiB. ✓
- §21.8: **120 conditions over 277 instances.** I parsed all four register tables and
  counted by the document's own mechanical rule ("Instances within a cell are separated by
  semicolons, and a cell reading — is one instance"). Rows: F 35, L 49, T 26, R 10 = 120,
  matching each subsection's stated count. Instances: F 56, L 116, T 55, R 50 = **277**.
  Exact.
- Cross-references: every `§n` and `§n.m` reference in the document resolves to a heading;
  every `[R-XXX-NN]` identifier cited in the register is defined somewhere in the document;
  the only row-like label referenced but not defined in a table is **F11**, which §21.2's
  Note declares deliberately struck.
- §10.2's eight identifier spaces: exactly one table row (channel layout) carries no
  experimental range, and `[R-EXT-02]` says two spaces do — the second being the trailer's
  flag lanes, which are not in the table and which the rule names. Consistent.
- §20.5's arithmetic on the extension vehicles: "F36 and L25 for a record type, and one row
  for each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)".
  I mapped each: layout→L36, linearization→L33, sample type→L34, codec→L43, filter→L45,
  index encoding→L31, metadata encoding→R1. Seven, all present, none duplicated. This is
  the tightest cross-count in the document and it holds.

---

## 8. Degradation walks — seven, traced end to end

**D1. Unknown top-level record type, MU = 1, experimental range (≥ 0x8000).**
`[R-CNT-15]`: reject-file. §21.6's closing paragraph classifies this as a *conforming file
a reader nevertheless refuses*: `[R-CNF-02]` makes the file conforming (§10.3's prohibition
binds a writer's conduct, not the bytes) and the reader still rejects. The reader may serve
nothing. The diagnostic ought to distinguish this from corruption. `[R-CNF-03]`'s
acceptance duty carves it out explicitly, and adds the observation that in a conforming
file such a type is *necessarily* experimental, because a reserved-range type with MU = 1 is
itself F35. A verifier reports *cannot establish* (§2.3). The same type as a **layer
sub-record** is reject-layer and never a ground to refuse the file (`[R-CNT-18]`, §21.6) —
I checked that qualifier because it is exactly the kind of thing that goes stale, and it
does not.

**D2. Unknown codec.** A conforming reader implements all four assigned codecs
(`[R-COD-03]`, `[R-CNF-03]`), so the only reachable case is a reserved (5–0x7FFF) or
experimental (≥ 0x8000) value: reject-**layer** (L43), detected at layer access, from
declarations alone with no I/O. Other layers unaffected; §2.4 lets the reader still list the
rejected layer's name. A verifier that cannot execute a codec cannot certify and reports
*cannot establish* (`[R-COD-11]`), but that position "arises only at a reserved or
experimental value" for a conforming reader. Traced and consistent.

**D3. Unrecognized flag or enum value.** Trailer incompat lane (bits 0–15): any set bit is
reject-file (F19), because this text defines none. Ignore lane (16–31): ignored, file
conforming (§21.6), and an updater must copy them forward, clear none and set no other
(`[R-CNT-08]`). Record flags bits 2–15: readers MUST **ignore** them; a verifier records
F26/L47. Layout value 3–255: reject-layer (L36) — and note this space has no experimental
range at all. Each of these has a different answer and each is stated.

**D4. Truncated or extended tail.** Physical length ≠ committed_file_length is F17 at open.
Mid-commit, the physical tail is not a trailer: F8 (magic) fires and `[R-LIF-05]` bars
scanning backward — "MUST report the file torn or invalid and MUST NOT scan backward". §9.5's
Note is careful that residue past a *completed* commit carries no row of its own because
the reader meets it as one of F8/F14/F17 and cannot tell residue from corruption. §9.6's
recovery scan is explicitly not a reader behavior and "no verdict turns on the probe". The
reader serves nothing.

**D5. Checksum mismatch, by scope.** `[R-CNT-20]` gives the whole ladder: trailer or
directory → reject-file (F14, F20); a layer's index cross-checks, CRC array or segments →
reject-layer (L21, L22, L37, L38); a stored tile's crc → reject-tile (T1); a user-metadata
extent's crc → ignore-record with a SHOULD-report (R2). After a reject-tile the reader may
still serve every other tile of the same layer, and §19.4 step 8 says how: return the
validating entries' values with a per-entry report, or fail the whole request — **but never
stand fill in for the rejected tile** (`[R-CNF-09]`, `[R-TYP-09]`). After a reject-layer
the bar is prospective: values already returned under §19.2's timing stand.

**D6. Limit exceeded.** §21.9's table is minimum guarantees, not caps. A file exceeding one
stays conforming and the reader MAY decline — at the narrowest scope whose quantities
exceed what it can serve, or any containing scope. The refusal MUST be reported as a
resource limit and not as a validity error. Declining **on that ground** a file within the
table makes the reader nonconforming. I checked the individuation paragraph: the last three
rows (tile decoded size, document decoded size, zstd Window_Size) are per-instance, the tile
row ranging over *addressed* tiles stored or not, the other two over instances a file
actually contains; the first five range over declarations. A layer addressing no tile has no
tile whose decoded size the table bounds — which I checked against `[R-COD-07]`'s parallel
escape in §17.2's Note, and they agree.

**D7. Format major version not implemented.** `[R-CNT-07]` rejects, and the diagnostic
SHOULD be distinct from both "not a TARN file" and "corrupt". But `[R-CNF-13]` gets there
first: the reader MUST apply every **reaching** condition whatever major is declared, and
§21.2's preamble derives which those are — F8, F14, F6, and both of F1's instances, and no
other row. Those are exactly §6.2's pre-version-gate checks plus the front-block equality.
Failure of a reaching condition is reject-file *on the requirement's ground*, not on
capability grounds, and a verifier that establishes one reports **nonconforming** whatever
major the file declares. version_major = 0 is outside the premise entirely — it declares no
major (F18). I traced §2.3's Note on why F14 reaches (it consumes redefinable bytes but
asserts only `[R-CNT-24]`'s CRC placement) and why F5 and F15 do not (F5's 128 floor is
derived from format-major-1 minimums; F15's reserved bytes lie inside the 48 a future major
may redefine). Both arguments hold.

---

## 9. Suspicions I opened and closed

These are the places I stopped, and the sentence that closed each. Recording them because a
clean lane has to show it looked.

**(a) §19.1 step 4 does not order the user-metadata *encoding value* check, but R1 is
reader/open.** Step 4 lists three framing rules a top-level user-metadata record carries
(no (0,0) slot, extent_length ≥ 5, inline_length exactly 1) and stops; it never says the
encoding byte's value set (0 invalid, 3–0x7F reserved) is checked at open. R1 places
exactly that at open. **Closed by** §19's preamble: "Those enumerations are not the complete
inventory of what a reader detects at that tier: §21's register is… A row this section does
not restate is due at its own tier all the same, with its governing rule's own outcome."
This is the governing clause above the sentence. I would have filed this without it.

**(b) T14 seems to be a strict specialization of T3, and §21.1's list of specializations
does not name the pair.** Under codec 1 the decoded payload *is* the stored bytes, so every
file exhibiting T14 also exhibits T3. **Closed by** §21.1: "the property decides any pair
and this list is not offered as closed." Both rows are reader / tile use / reject-tile, so
nothing turns on which is recorded.

**(c) An unknown MU = 0 record is "skipped as though absent" — does a reader still check its
extent slot?** If it did not, F30/F31/F32 would be unreachable for unknown types. **Closed
by** §19.1 step 4 ordering the slot check over *non-layer top-level records* without
exempting unknown types, plus F30–F32's Detector/Detected cells (reader / open) and
`[R-CNT-13]`'s "For a record with MU = 0, the extent slot is its only sanctioned reference
to bytes outside the record sequence". §8.1 leaves the extent's *contents* opaque, not its
slot. Determined.

**(d) §19.2's fourth bullet says "at use of a record's extent: that extent's CRC", but a
layer record's extent (the tile-index region) has no terminal CRC and an unassigned type's
extent has none at all.** **Closed by** §8.1's map, which gives the index region's coverage
as the segment CRC array under `crc_of_crc_array`, and by bullet 3, which places the
index-chain checks at tile use — where L37/L38 sit. The bullet is loose but has no referent
that conflicts. Nine register rows carry Detected = "extent use" and they are exactly
R2–R10.

**(e) §4.7 says "each descriptive field's definition states what a reader does when the
field contradicts the data it describes", and version_minor is the only descriptive
field.** Does `[R-CNT-07]` state that? **Closed by** "A reader MUST NOT reject a file for its
version_minor: minor releases are additive-only, and all feature gating is structural
(records, enums, flags)" — which answers both directions of contradiction (an overstated and
an understated feature floor) by directing the reader to gate on structures. §21.6 records
the higher-than-defined case as accepted.

**(f) Is version_minor really descriptive when `[R-CNT-26]` and `[R-WRT-06]` make an
appender's and a compactor's output depend on it?** **Closed by** §4.7's own wording: the
test is what a "conforming reader or verifier does with the bytes it reads", not what a
writer emits; and both dependencies are SHOULDs, which `[R-CNF-12]` places outside the
register entirely.

**(g) `[R-CNF-02]`'s closed list of expressly-carved-out writer obligations — is it
complete?** Three cases: §6.3's flags rules, §6.2's over-long pre-trailer gap, §20.3 step
4's bar. I checked each is declared where it arises (`[R-CNT-08]`: "a set ignore-lane bit is
not a file-conformance violation"; `[R-CNT-05]`: "a longer gap is conforming, and no
conforming commit produces one"; §20.3 step 4: "no file is nonconforming by virtue of its
violation"). Then I hunted for a fourth. `[R-CNT-12]`, `[R-CNT-22]` and `[R-MTA-05]` say the
opposite ("makes the file nonconforming"); `[R-EXT-03]` and `[R-MTA-06]` are conduct rules
`[R-CNF-02]` already names in its first clause; `[R-LIF-04]`'s residue is F17;
`[R-SLB-04]`'s stale declaration is L41/L42; the undisclosed zstd dictionary is
**unwitnessed**, not carved out, and §21.7 is explicit that unwitnessed ≠ permitted; and
`[R-WRT-05]`'s byte-identical re-emission is unwitnessed too, since §9.6's probe is the
only thing that could pair two directories and "no verdict turns on the probe". No fourth
case. The list holds.

**(h) Do §20.3 step 4's two lists really reach every declaration field of §7.4?** I walked
the table field by field: name → permitted; layout, linearization, codec, filter, rank,
index_encoding → fixed; A, S, A_slab → the slab/alignment member; d, C → follow the
dimension and channel lists; dimension entries (name permitted, extent permitted-to-grow,
tile extent fixed); channel entries (name permitted, type and fill fixed); entry_count and
crc_of_crc_array → "follow the commit, the record's extent slot with them"; sub-records →
§20.4's subject. Every field reached. **Closed.**

**(i) Compositions — what may a single commit do at once?** I enumerated the pairs. Grow an
extent + append a planar channel (N and C both move; ordinals renumber under `[R-GEO-06]`;
the whole index region is re-emitted). Grow + shorten from the end. Append + slab-declared
(the new channel's block [C·N, (C+1)·N) adds runs without disturbing existing blocks, since
N is unchanged — a genuinely cheap case). Grow + slab kept (the run partition changes, so
`[R-SLB-04]` forces re-establishment or clearing, and committed bytes cannot move, so the
writer must re-store or clear). Switch alignment→slab or slab→alignment in one commit
(clear one, declare the other; `[R-CNT-16]` is satisfied because only the new generation's
state is tested, and there is no intermediate file). The only barred composition is an
extension **and** a shortening of one channel list, and the document says why: "replacing
the last channel, or any run of channels at the end, is two commits or a rewrite." Every
composition I could build is either permitted and safe, or barred and explained.

**(j) The transitions a slab or alignment declaration can make.** none→some (declared);
some→another (changed); some→same (the default "keeps its declarations", or
"re-established"); some→none (cleared); and the exclusive switch (two members composed).
**No transition lacks a verb.** This closed the strongest form of the suspicion I carried
into §20.3 — but it left a weaker one standing, which I file as reader-01 below.

**(k) §21.5's claim that its ten rows cover every way a document can be unreadable.**
`[R-CNT-25]` names four ways; I mapped them: failed extent CRC → R2; unimplemented or
invalid encoding → R1 (experimental → §21.6); decode failure → R3, with the frame
constraints routed to R4; content violating the document's own rules → R5–R10 against
`[R-MTA-04]`'s four restrictions (object-unmarked → R7; finite numbers → R8; no duplicate
keys → R9; well-formed UTF-8 and §4.6 name rules on keys → R5, R6, R10). Member ordering is
explicitly *not* unreadable and lands at F27/L48. Complete.

**(l) R4's sixteen instances against §18.2's carried-over constraints.** Eight conditions ×
two containers: frame magic; skippable frame; second frame; nonzero dictionary ID;
content-checksum flag; bytes remaining after the frame; content-size declared larger; content-size
declared smaller. §18.2 names exactly those plus two it removes from the register on stated
grounds — undisclosed dictionary use (unwitnessed) and the buffer-sizing bar (binds a reader,
states no condition a file can exhibit). 8 × 2 = 16, matching my mechanical count. And
§17.2's "Three frame features are excluded" counts correctly too: dictionary, content-checksum
flag, oversized window — the content-size field is *not* excluded, it MAY be present.

**(m) §18.2's Window_Size treatment and the Single_Segment_Flag corner.** With SSF there is
no Window_Descriptor and RFC 8878 makes Window_Size the content-size field, which §18.2 pins
to the decoded document's length — so a document above the 8 MiB Window_Size guarantee,
framed that way, exceeds a §21.9 row and falls outside `[R-CNF-03]`'s acceptance duty, and
the writer is told to use a Window_Descriptor instead. §17.2's parallel Note for tiles
(below 1 KiB a tile is encodable under codec 3 only as a single-segment frame) is the same
argument run the other way, and both are right about the RFC's two derivations agreeing.
Closed.

**(n) The §21.9 guarantees bound decoded and declared quantities but never a *stored*
length, so a reader is obliged to accept a file with an arbitrarily large stored tile.**
`[R-CNF-10]`: "Readers MAY enforce resource limits, but MUST accept any conforming file
within the minimum guarantees." A file with a 2⁶³−1-byte stored tile whose decoded size is
within 256 MiB is within every guarantee, so declining it makes the reader nonconforming.
That is a harsh obligation but it is **decided**, not open, so no two conforming
implementations can disagree. Not a fork.

**(o) Every stated constant, offset and checksum I could check.** All correct — §7 above.
This was the highest-expected-value place to look for a hard finding and it produced none.

---

## 10. Findings

### reader-01 — AMBIGUITY

**Location:** §20.3 step 4, `[R-WRT-04]`; restated at §11.1 (Rationale, non-normative) and
Appendix H (non-normative).

**Quotation (normative, §20.3 step 4):**

> A layer that stores a tile **in the generation this commit supersedes** keeps its
> declarations, with these exceptions and no other: […] and a slab or alignment declaration
> MAY be declared, changed, re-established or cleared as this step provides below.

and, later in the same step, the clause it delegates to:

> a slab declaration declared, changed or kept has its invariants re-established over every
> run the new state keeps, or is cleared (`[R-SLB-04]`)

**The problem.** The permitted-list member names four verbs; the clause "this step provides
below" names four dispositions, but its third is **kept**, not **re-established**, and its
own use of "re-established" is of the *invariants*, not of the declaration. So the member's
third verb has no counterpart in the clause it delegates to, and the clause's third
disposition has no counterpart in the member's list. An updater implementer has to decide
what "a declaration re-established" means, from a list the document declares closed ("with
these exceptions and no other").

**Permitted readings.**

1. *"re-established" = "kept at the same value", with the invariants re-established over the
   new placement.* This makes the member's four verbs and the clause's four dispositions
   correspond one-for-one. But then the member includes, among "these exceptions and no
   other", a case that is not an exception at all: "keeps its declarations" is the rule the
   exception list is carved out of, so a declaration kept unchanged needs no permission.
2. *"re-established" means the declaration's invariants are re-established* — a loose
   phrasing in which the verb attaches to the wrong noun. Then the member names only three
   *transitions* (declared, changed, cleared) and the some→same case is left to the default,
   which handles it.
3. *"re-established" names re-declaring after an earlier commit cleared the declaration.*
   Within one commit this is indistinguishable from "declared" (none→some) and adds nothing.

**Which I picked and why.** Reading 1, because it is the only one under which the delegated
clause's "kept" has a counterpart, and because §20.3's own safety argument for the member
("a slab or alignment declaration governs placement (§16), not a value, its coordinate or
its padding") covers all four verbs indifferently.

**What an implementer does wrong without it.** Nothing byte-visible, which is why I grade it
as I do. I enumerated the transitions a slab or alignment declaration can make on a layer
that stores a tile — none→some, some→another, some→same, some→none, and the exclusive
switch between an alignment and a slab in one commit — and found a verb (or the default
"keeps its declarations") for every one under **every** reading above. So the set of files a
conforming updater may emit is the same under all three. What is wrong is the closed list's
own bookkeeping: a list that says "these exceptions and no other" should not contain a
member that is not an exception, and a member that delegates with "as this step provides
below" should use the vocabulary of the clause it delegates to. Given the document's own
practice of repairing this list repeatedly, I state the readings and leave the wording to
human disposition rather than repairing it in my head.

**Byte-level:** no. Two implementations, one reading "re-established" as reading 1 and one
as reading 2, permit and forbid exactly the same commits, because the some→same case is
permitted by the default clause under both. No file's conformance and no reader's verdict
moves.

---

### reader-02 — OBSERVATION

**Location:** §20.3 step 4, `[R-WRT-04]`; against §21.7, `[R-ERR-01]`.

**Quotation (§20.3 step 4):**

> This bar binds the commit as an actor: no file is nonconforming by virtue of its
> violation, and no register row records the violation itself, the register enumerating
> file-conformance violations (§21.1) and the bar stating no condition a file can exhibit
> (§21.7, `[R-ERR-01]`, `[R-CNF-02]`);

**And §21.7, `[R-ERR-01]`, defining that category:**

> Distinguish an unwitnessed condition from a requirement that states **no condition a file
> can exhibit**. `[R-ENC-06]`'s fixed field widths are not a state a file can be in — the
> parse is always at the widths this specification fixes, and a structure written at any
> other yields different values at them — a different file, conforming or not on its own
> terms.

**The problem.** §20.3's bar names its own category and the section defining that category
supports it only by analogy to a case of a different shape. §21.7's worked case rests on the
parse being definitional: there is no byte sequence that *is* a structure at the wrong
width. §20.3's bar rests on something else — a file left by a commit that changed a fixed
declaration is byte-identical to a file a creator could have written in one commit, and the
superseded generation's own directory is still physically in the file as slack, where §9.6's
backward probe would find it. That is §21.7's **unwitnessed** shape ("for every file
exhibiting it, some file that does not exhibit it cannot be told apart from it by any check
this specification obliges a reader or a verifier to perform"), applied to a condition the
file *can* physically carry and no obliged check reaches — §9.6 says "no verdict turns on
the probe".

The two categories are not interchangeable on one point §21.7 makes explicitly: an
unwitnessed condition remains a violation ("the requirement binds its actor as any other
does"), whereas a requirement stating no condition a file can exhibit has nothing to
violate. §20.3's sentence cites both categories in the same breath and relies on
`[R-CNF-02]`, which independently and correctly settles the question ("no file is
nonconforming by virtue of its violation"). The §21.7 citation is therefore doing no work,
and if it is doing work it is doing it on the wrong ground.

**Why I grade it OBSERVATION and not a contradiction.** It is decidable from the text — the
test in `[R-ERR-01]` is stated and is complete — but deciding it costs a reader a careful
comparison of two paragraphs three sections apart, and either answer produces the same
outcome: no register row, and no file nonconforming by virtue of the bar. §21.7's paragraph
also does not claim to enumerate its category; `[R-ENC-06]` is offered as an example, not as
the only member, and §18.2 adds a second member ("the bar on sizing a buffer binds a reader
rather than the document, and so states no condition a file can exhibit at all") without
contradiction. So there is no closed list to violate. A reader that wants to know whether a
commit-level bar can be in `[R-ERR-01]`'s second category has to reason it out unassisted;
the document supplies the test but not the application.

**Byte-level:** no. Both classifications yield no register row and no reader or verifier
obligation. The bar is a per-commit rule that `[R-CNF-02]` has already placed outside file
conformance, so the emittable set is fixed either way.

---

## 11. What I could not determine

Nothing in my charter. Every branch of the open path, the timing rule, layer access, the
tile-read algorithm, and the seven degradation walks resolved from the document. The one
place I had to supply reasoning the document does not was reader-02's classification
question, and it is inconsequential.

The specification supported a complete reader implementation, and I checked that claim by
building one and round-tripping a file I constructed from the rules alone.
