# Cleanroom round 10 — Adversary transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
all 3,899 lines, in five `Read` calls. I opened nothing else — no `docs/`, no
`PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web.

I ran four local computations, all of which read only `spec/tarn.md` or nothing:

1. A regex sweep over `spec/tarn.md` collecting every `[R-XXX-NN]` identifier and
   every bare `R-XXX-NN` parenthetical citation, to check for dangling or
   orphaned identifiers.
2. A CRC-32C implementation (Castagnoli, reflected, init/final `0xFFFFFFFF`),
   reading no files, used to check the document's four published constants.
3. A parser over §21.2–§21.5 that counts rows and semicolon-separated Instances
   cells, to check §21.8's "121 conditions over 248 instances".
4. Hand arithmetic (below) on every worked example in §11.2, §11.4, §14.2,
   §14.3, §14.5, §15.4, §16.2, §17.3, §20.3, §21.9.

One incidental exposure I should name rather than hide: the task harness printed
a `gitStatus` block into my prompt containing the subject lines of the five most
recent commits (e.g. "ADR-0068: no commit removes a layer"). I did not read any
of those commits, and I did not use the subject lines as evidence for any
finding — but a subject line naming an ADR topic is more than zero information
about what changed, and a reader of this transcript should know it was in front
of me. I also received the brief's statement that §21's rows were renumbered;
that steered where I looked, and I have been careful to verify every row
cross-reference from the document itself rather than from that claim.

---

## 1. What I did, in order

I read the document front to back once, then implemented from it. "Implemented"
here means: I built the minimal file by hand and checked its every byte against
the rules; I computed every constant; I traced the reader algorithm (§19) and
the commit protocol (§9.2, §20.3) against concrete byte layouts; and then I
attacked. The attacks are §3 below. The findings are §4.

My first pass produced a long list of suspicions. Most died on a second reading,
because the sentence that killed them was three paragraphs away from the one
that raised them. I have kept the dead ones in §3 with the sentence that killed
each, because the brief asks for that and because a foreclosed attack is the
useful half of an acceptance round.

---

## 2. Verification of the document's own arithmetic

I checked everything the document asserts numerically. All of it holds.

### 2.1 Checksum constants (§4.5, §15.4, Appendix A, Appendix B)

CRC-32C implemented from §4.5's parameters alone — polynomial 0x1EDC6F41
(reflected form 0x82F63B78), reflected input and output, init 0xFFFFFFFF, final
XOR 0xFFFFFFFF:

| Claim | Where | Computed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) = 0xE3069283 | §4.5 | `0xe3069283` | ✔ |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | `0x0` | ✔ |
| Appendix A trailer CRC = 0xE00938D2, stored `D2 38 09 E0` | Appendix A | `0xe00938d2` → `D2 38 09 E0` | ✔ |
| CRC-32C of 2¹⁶ sentinel entries = 0xEECB3BB2 | §15.4, Appendix B | `0xeecb3bb2` | ✔ |

The trailer bytes I reconstructed from §6.2's layout table *without* copying
Appendix A's hex dump, to make the check independent:

```
8A 4E 52 41 54 0D 0A 1A   magic
01 00                     version_major = 1
00 00                     version_minor = 0
00 00 00 00               flags = 0
01 00 00 00 00 00 00 00   generation = 1
10 00 00 00 00 00 00 00   dir_offset = 16
04 00 00 00 00 00 00 00   dir_length = 4
80 00 00 00 00 00 00 00   committed_file_length = 128
EF CD AB 89 67 45 23 01   file_id = 0x0123456789ABCDEF
00 00 00 00               reserved
```
60 bytes; CRC over them = 0xE00938D2. Byte-for-byte identical to Appendix A's
rows `0040`–`0070`. The minimal file is correct.

The all-sentinel segment constant is worth naming: it is the CRC of
`(FF×16 00×4) × 65536` = 1,310,720 bytes. It matched. §15.4's carve-out — "a
partial segment's CRC MUST be computed" — is therefore load-bearing and correct:
the constant is only valid for a segment covering *exactly* 2¹⁶ entries.

### 2.2 §12.3's channel entry

Claim: name `temp`, type float32, fill quiet NaN 0x7FC00000 is the twelve bytes
`04 74 65 6D 70 0C 00 04 00 00 C0 7F`. Built from §7.4's channel-entry grammar
(name u8 len + bytes · type u16 · fill u8 len + bytes): `04` + `74 65 6D 70` +
`0C 00` + `04` + `00 00 C0 7F` = twelve bytes, identical. ✔

### 2.3 Geometry and serialization examples

- §11.2: extents (1024, 2048), tiles (256, 256) → G = (4, 8), N = 32, P = 65,536. ✔
  With extents (1000, 2048), G_y = ⌈1000/256⌉ = 4. ✔
- §11.4: tile (1,0) → s = 1·8 + 0 = 8. ✔ Coordinate (300, 700) → tile (1, 2),
  s = 10; in-tile (44, 188) → 44·256 + 188 = 11,452. ✔ Planar C = 4, channel 2 →
  2·32 + 10 = 74. ✔
- §14.2: interleaved `a` uint8 + `b` uint16 → Q = 3, decoded size 18, ordinal 5
  at bytes [15, 18). ✔ Planar `b` = 12 bytes, ordinal 5 at bytes 10–11. ✔
  `t` float32 + `m` bool → Q = 5, size 30, ordinal 5 at [25, 30), `m` at byte 29. ✔
- §14.3: P = 10, alternating from true → byte 0 = 0x55 (bits 0,2,4,6 set),
  byte 1 = 0x01 (value 8 true → bit 0; value 9 false → bit 1 clear), six pad
  bits. With fill true, pad bits 2–7 set → 0x01 | 0xFC = 0xFD. ✔ (`55 01` /
  `55 FD`.)
- §14.5: extents (5,5), tiles (4,4) → grid 2×2; edge tile (1,1) covers 4–7 on
  both axes, one real position (4,4) and 15 padding; one uint16 channel, P = 16
  → 32 bytes, values 1–15 each `CD AB`. ✔
- §15.4: entry_count = 1,000,000 → 16 segments (15 full = 983,040 entries, last
  = 16,960), CRC array 64 bytes, region 20,000,064 bytes. Tile 999,999 is
  999,999 − 983,040 = 16,959 into segment 15 → 20 × 16,959 = 339,180. ✔ CRC
  array at [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000),
  which is 339,200 bytes ("~339 KB"). ✔ One full segment = 65,536 × 20 =
  1,310,720 = 1.25 MiB. ✔ Second example: disk ordinal 74 → region bytes
  [1,480, 1,500) ✔; channel 3's block = [96, 128), 32 entries ✔.
- §16.2: N = 32, S = 8 → runs [0,8), [8,16), [16,24), [24,32); tile rows 1–2
  under row-major with G_x = 8 are ordinals 8–23 = runs 1 and 2 exactly. ✔
- §17.3: I reproduced the byte-shuffle by hand. Input `00 00 80 3F | 00 00 00 40
  | 00 00 40 40` (s = 4, n = 3). Placing byte *i* of group *j* at offset i·n + j
  gives, offset by offset: g0[0] g1[0] g2[0] g0[1] g1[1] g2[1] g0[2] g1[2] g2[2]
  g0[3] g1[3] g2[3] = `00 00 00 00 00 00 80 00 40 3F 40 40`. Identical to the
  document. I also checked the stated inverse ("restores byte i·n + j to offset
  j·s + i"): filtered offset 8 (i=2, j=2) → original offset 2·4 + 2 = 10, which
  holds 0x40 = g2[2]. ✔
- §20.3: 32-tile interleaved index region = 32·20 + ⌈32/65536⌉·4 = 644. ✔
- §21.9's note: 2³² entries / 2¹⁶ per segment × 4 bytes = 2¹⁸ = 256 KiB ✔;
  at 2³⁶ it is 2²² = 4 MiB ✔.

### 2.4 The register's own bookkeeping

I parsed §21.2–§21.5 mechanically. Rows: 36 / 49 / 26 / 10, matching each
subsection's stated count. Instances, counting a `—` cell as one and otherwise
splitting on semicolons per §21.1's rule ("Instances within a cell are separated
by semicolons, and a cell reading — is one instance"): 53 / 106 / 45 / 44 =
**248**, matching §21.8's "121 conditions over 248 instances" exactly.

Given the brief's warning about a wholesale re-labelling, this is the first
thing I would have expected to be stale. It is not.

### 2.5 Every register-row cross-reference in the document

The brief says row labels are newly suspect. I resolved every one against the
row it lands on:

| Citation | Where | Row it lands on | Does the sentence hold? |
|---|---|---|---|
| "F1 of F6 and of F8" | §21.1 | F1 byte-reversed signature constant; F6 front block not byte-identical; F8 trailer magic wrong | ✔ F1 is a strict specialization of both |
| "F35 of F36" | §21.1 | F35 reserved-range type with MU=1; F36 reserved-range type whatever MU | ✔ |
| "L24 of L25" | §21.1 | L24 reserved-range sub-record with MU=1; L25 whatever MU | ✔ |
| "T24's *any codec*" | §21.1 | T24 Instances cell reads `any codec` | ✔ |
| "(T15, T25)" | §21.1 | T15 has 2 instances (zlib, gzip); T25 has 3 | ✔ enumerated, as claimed |
| "§21.2 rows F8 and F17" | §9.6 | F8 trailer magic; F17 committed_file_length ≠ transport size | ✔ these are exactly the two gates a residue tail trips |
| "(§21.4, T24)" | §17.2 deflate note | T24 = bytes remain after the stream ends, `[R-COD-08]` | ✔ |
| "F9/F10, F31/F32, L16/L17 and T8/T9" | F33 | dir bounds; top-level record extent bounds; layer/sub-record extent bounds; tile-entry extent bounds | ✔ all four tiers, low bound then high bound, in order |
| "the same byte at a padding position is T4's" | T2 | T4 = padding position does not encode fill | ✔ |
| "the check that detects it is T25's" | T13 | T25 = malformed stream fails to decode | ✔ |
| "the check that detects it is T2's or T4's" | T26 | T2 bool byte, T4 padding fill | ✔ |
| "(F36, L25)" and "(F35, F36, L24, L25)" | §21.6 | reserved-range type rows | ✔ |
| "F18" | §21.6 | version_major = 0 | ✔ |
| "which §21.3 registers" | §16.2 note | L41 (unpacked run), L42 (misaligned first stored tile) | ✔ both exist |
| "whose appearance as a sub-record §21.3 registers" | §7.4 note | L26 layer record nested as sub-record | ✔ |
| "(`[R-CNT-05]`, F7)" | Appendix H | F7 structure between directory end and trailer | ✔ |
| "(`[R-CNT-15]`, F36, L25)" | Appendix H | reserved-range type, verifier rows | ✔ |

Every row cross-reference resolves to the row its sentence claims. I found no
stale label.

### 2.6 Identifier space

160 distinct `R-XXX-NN` identifiers. Every prefix is contiguous — CNF 1–12,
CNT 1–27, COD 1–11, ENC 1–16, ERR 1–5, EXT 1–5, GEO 1–6, IDX 1–5, LIF 1–8,
MDL 1–2, MTA 1–9, PRV 1–5, RDR 1–4, SEC 1–7, SER 1–9, SLB 1–5, TYP 1–10,
VEC 1–4, WRT 1–9 — with `R-SER-04` appearing exactly once, in §14.4's
withdrawal note, as §2.2 requires ("a withdrawn requirement leaves its
identifier permanently retired"). `R-ENC-100` appears once, as §2.2's own
example. No bare parenthetical citation names an identifier that is not defined
somewhere in brackets.

---

## 3. Attacks

Each attack below is a concrete file. For each I give the construction, the two
verdicts I hoped for, and the sentence that decided it.

### 3.1 Degenerate and boundary files

**A-1. The 128-byte minimum, and one byte under.**
§5.1's arithmetic: front block ends at 16; a directory of ≥ 4 bytes at an offset
of ≥ 16 ends at ≥ 20; `dir_offset + dir_length ≤ F − 64` forces F ≥ 84; F must
be a multiple of 64; therefore F ≥ 128. I built the 64-byte file (trailer only)
and the 192-byte file with one layer record. The 64-byte file trips F5
(`[R-CNT-27]`) *and* F10 (`dir_offset + dir_length ≤ F − 64 = 0` is unsatisfiable
for any legal slot). Both reject-file. **Foreclosed.**

I also computed the smallest file that can carry a layer: the minimum layer
record inline payload is 73 bytes (name 2 · layout 1 · lin 2 · codec 2 · filter
2 · A 8 · S 8 · A_slab 8 · d 1 · C 2 = 36, plus one dimension entry 18, plus one
channel entry 6, plus index_encoding 1 · entry_count 8 · crc_of_crc_array 4 =
13), so the record is 97 bytes, the directory 101, and F ≥ 64 + 16 + 101 rounded
up to a multiple of 64 = 192. No rule anywhere contradicts this. Good.

**A-2. Slack in front of the directory in a first-generation file.**
F = 128, `dir_offset = 60`, `dir_length = 4`, directory at [60, 64), trailer at
[64, 128), bytes [16, 60) slack. Every §6.2 gate passes; the coverage partition
holds; `[R-CNT-05]`'s pre-trailer pad is zero bytes long. Two verifiers certify.
Note this is a *conforming file with 44 bytes of slack produced by a single
commit*, which is worth knowing exists — §5.2's rationale frames slack as the
byproduct of superseding, and this file has superseded nothing. Not a defect;
`[R-SLB-05]` and §5.2 both make unclaimed bytes slack "whatever produced it".
**Foreclosed.**

**A-3. An over-long pre-trailer pad.**
Directory ends at 100; pad to 192 instead of 128; trailer at [192, 256).
§6.2 anticipates me exactly: *"this specification does not constrain their
content, and bounds their number only through step 5 of the commit protocol,
which pads to the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is
conforming, and no conforming commit produces one."* So the file is conforming
and no conforming writer emits it. Both verifiers certify. I checked whether a
second verifier could read `[R-LIF-02]` step 5 as a file-level requirement and
report nonconforming; §21.1's completeness clause blocks that — there is no
register row for an over-long pad, and the register's completeness is normative,
so an over-long pad is not a file-conformance violation. **Foreclosed, and
deliberately.**

**A-4. Zero-length structures everywhere.**
Zero-record directory (`dir_length = 4`, CRC of zero bytes = 0x00000000) —
conforming, and Appendix A is exactly this. Zero-length stored tile — T10.
Extent slot with one half zero — F30/L15. Extent slot (0,0) on a
user-metadata record — F21/L10 (reject-file / reject-layer), *not* the
quarantine, because §18.1 says so in terms: *"a malformed extent slot on such a
record, (0, 0) included, is a validity error at the record's containing scope
(`[R-CNT-13]`, `[R-CNT-25]`), because that failure precedes the document."*
Layer with `entry_count = 0` → slot (0,0), `crc_of_crc_array = 0` — conforming.
**All foreclosed.**

**A-5. `extent_length` = 4 and = 5 on a user-metadata record.**
4 → F22/L11 (below the 5-byte floor). 5 → legal framing, one document byte plus
the terminal CRC; under encoding 1 a one-byte JSON text cannot be an object
(minimum `{}` is two bytes), so the document is always unreadable → R7,
ignore-record; under encoding 2 a one-byte zstd frame is impossible (the magic
alone is four) → R4. So `extent_length = 5` is a legal-framing / always-ignored
record. That is coherent, not contradictory: the quarantine boundary sits
exactly where §18.1 puts it. **Foreclosed.**

**A-6. Empty layers under every other feature.**
Dimension extent 0 → G = 0, N = 0, addressed tiles 0, index absent. I then piled
on: codec 4 (lz4) with a declared tile shape whose decoded size exceeds
0x7E000000; a slab declaration; a per-tile alignment; C = 4096.
§17.2's note anticipates the codec-4 case verbatim: *"The cap is quantified over
the layer's *addressed* tiles, so a layer that addresses none — any dimension
extent 0 (`[R-GEO-02]`, §21.6) — satisfies it whatever its tile shape declares,
and codec 4 is conforming there."* And it closes the obvious follow-up: *"`[R-ENC-04]`'s
overflow rule carries no such quantifier — it binds any sum or product a file
yields — so P·Q and P·Bᶜ are checked in an empty layer even though this cap is
not."* The slab case: `[R-SLB-02]`'s blocks are [0, 0), so there are no runs, and
*"A run with no stored tiles imposes nothing."* The alignment case is vacuous.
**All foreclosed, and one of them by a sentence written to foreclose exactly
this.**

**A-7. Alignment A = 2⁶².**
Stored-tile offsets must be ≥ 16 and multiples of 2⁶², and ≤ 2⁶³ − 1. The only
legal offset is 2⁶². So such a layer can hold *at most one* stored tile, and a
file carrying two is nonconforming under L40. Degenerate but fully decided, and
`[R-ERR-05]` states the bound. Compaction of such a file cannot shrink it below
2⁶² bytes, which the document nowhere claims it can (`[R-WRT-07]`: "A compactor
preserves content but not placement"; it never promises a size reduction).
**Foreclosed.**

### 3.2 Two structures claiming the same bytes

**A-8. A file-scope user-metadata record's extent set exactly equal to the
directory region.**
This is the prettiest overlap available, because the two structures have
*identical checksum framing*: §7.1 puts the directory's CRC in its final 4 bytes
over the preceding `dir_length − 4`, and §8.1 puts a user-metadata extent's CRC
in its final 4 bytes over the preceding bytes. So the extent's terminal CRC
verifies. A reader then decodes the record sequence as a JSON document, fails,
and takes ignore-record. It serves the file.

Verdict fork attempted: reader accepts, verifier rejects. But that is the
licensed reader/verifier split, not a defect — F33's detector is *verifier*, and
`[R-RDR-02]` says a violation whose assigned detector is the verifier imposes no
reader obligation. Two *verifiers* both reject.

I then tried the narrower version: is the outcome for a **file-scope structure
overlapping another file-scope structure** actually assigned? `[R-CNT-13]`'s
outcome sentence reads *"a verifier MUST treat an intra-layer overlap ... as
reject-layer, and any overlap across layers or touching another scope's
structures as reject-file"* — neither clause obviously names two file-scope
claimants. But F33's lead clause does (*"two structures that do not belong to
the same layer"*), its Instances cell names `record extents` and
`directory region`, and `[R-CNF-08]` maps the directory's owning scope (the
file, §7.1) to reject-file independently. Three routes, one answer.
**Foreclosed.**

**A-9. Two index entries of one layer addressing one stored extent (dedup).**
§15.3 row: *"two stored extents of the same layer overlap ... *verifier*:
reject-layer"*. Both verifiers reject. Worth flagging to implementers that the
obvious dedup optimization is banned, but it is banned in terms.
**Foreclosed.**

**A-10. An index entry addressing another layer's index region.**
§15.3: *"a stored extent overlaps any structure outside its own layer —
*verifier*: reject-file"*. **Foreclosed.**

**A-11. An overlap kind §15.3's table does not enumerate: a layer's index region
against its own sub-record's extent, or two sub-record extents of one layer.**
§15.3's row enumerates three alternatives (stored∩stored, stored∩index,
stored∩sub-record). Neither of mine is among them. But `[R-CNT-13]`'s general
sentence is not the enumeration — *"no two extent slots and no two structures
overlap"*, with the enumeration introduced by "including". And L18's condition
text is fully general: *"Two structures of one and the same layer claim
overlapping bytes in the live committed state"*. Its three Instances are the
three *kinds of claimant* a layer owns (stored-tile extents, tile-index region,
sub-record extents), which is the same convention F33 uses for its five. So the
enumeration is of claimant kinds, not pairs, and my two overlaps are covered.
**Foreclosed** — I had this pencilled as a finding until I noticed F33 uses the
identical convention.

**A-12. A structure claiming the front block or the trailer.**
Every route is bounded: dir (F9/F10), top-level record extent (F31/F32),
layer/sub-record extent (L16/L17), tile entry (T8/T9). I checked the boundary
arithmetic on all four: the low bound is `< 16` and the high bound is
`> F − 64`, so an extent ending *exactly* at F − 64 is legal everywhere, and
§9.7's walk bound `[16, F − 64)` is half-open and agrees. I constructed a
1-byte extent at [F − 65, F − 64) and confirmed it is legal on every route.
**Foreclosed, and the four tiers agree on the boundary to the byte.**

### 3.3 Reserved, unknown and experimental values in every position

I enumerated the full cross product: record type ∈ {0x0000, 0x0001, 0x0002,
reserved 0x0003–0x7FFF, experimental ≥ 0x8000} × position ∈ {top-level, layer
sub-record} × MU ∈ {0,1} × PE ∈ {0,1} × reserved flag bits ∈ {clear, set}.
Every cell lands somewhere:

- type 0x0000 → F24 (top-level) / L13 (sub-record)
- type 0x0001 nested as a sub-record → L26
- registered type with a stored flag bit differing from §7.3 → F28 (the
  top-level user-metadata record) / L49 (the layer record, or a registered
  sub-record). The split follows `[R-CNT-13]`'s governing-scope rule — *"the
  layer for a layer record and for sub-records, the file for other top-level
  records"* — so a layer record's flag defect is layer-scope, and every F-row
  that could catch a layer record says "non-layer" in its condition text. I
  checked all of F25/F26/F28/F30/F31/F32 for this and all six carry the
  qualifier.
- MU = 1 with PE = 0 → F25 / L46
- reserved flag bits 2–15 set → F26 / L47
- reserved-range type, MU = 1 → F35 (reader, reject-file) + F36 (verifier);
  L24 + L25 for sub-records
- reserved-range type, MU = 0 → F36 / L25 only
- experimental-range type, MU = 0 → §21.6, conforming, ignored
- experimental-range type, MU = 1 → §21.6's closing paragraph, conforming file a
  reader refuses; verifier verdict *cannot establish* per §2.3

And the enum spaces: layout L36, linearization L33, sample type L34, codec L43,
filter L45, index encoding L31, metadata encoding R1 (0 and reserved) with the
experimental range declared conforming by §21.6, trailer flags F19 (incompat)
with the ignore lane declared conforming by §21.6. **No unassigned cell.** The
splits inside each reserved range (linearization 2–3 vs 4–0x7FFF; sample type
14–19 vs 20–0x7FFF) match §11.4 and §12.2 exactly.

**A-13. The metadata-encoding table cell against §21.6.**
§18.2's layout table says `Valid values | 1 or 2; see below`, while §21.6 says an
experimental-range (≥ 0x80) encoding leaves the file **conforming**. Elsewhere
in this document a layout table's valid-values column *is* the constraint — §6.2's
column is enforced verbatim by `[R-CNT-06]`, and §7.4's Constraint column by
`[R-CNT-23]` — so a table-driven validator built from §18.2's table would reject.
I nearly reported this. What killed it: the cell says **"see below"**, an explicit
deferral, and the three sentences immediately below partition the space into
assigned / reserved / experimental. `[R-EXT-03]` then closes it in terms —
*"for the metadata-encoding space of §18.2, ignore-record under the quarantine
(`[R-CNT-25]`), never a scope-level rejection"* — and `[R-CNF-02]` makes the
experimental prohibition bind conduct, not bytes. **Foreclosed.** Reporting it
would be padding.

### 3.4 The reader / verifier seam

**A-14. A corrupt front block, served remotely.**
Reader A (local, block resident) → reject-file per `[R-CNT-04]`. Reader B
(remote, two exact ranges) → *"MAY defer or omit the check"* → serves the file.
Two conforming readers, opposite behavior on the same bytes. This is the
seam the brief asks about, and it is licensed to the word, with the test
carefully chosen to be decidable locally: *"The test is residency, not
transport, so an implementation decides it at its own open path without having
to classify the network underneath it."* Two *verifiers* do not diverge: §2.3
obliges a verifier to check *"every file-level requirement — including those
ordinary readers are exempted from"*, so a verifier fetches [0, 16).
**Foreclosed.** (F6's Detector cell reads `reader`, which is imprecise for a
remote reader, but the condition cell states the exemption, and §21.1's tie-break
gives the rule the last word.)

**A-15. An interleaved bool byte of 0x02 at a real sample position.**
Verifier: T2, nonconforming. Reader: `[R-SER-08]` obliges it to report 0x00 as
false and every other byte as true if it returns the value at all. Two verifiers
agree; a reader and a verifier differ, which is the design. The document's own
rationale says why the earlier undefined-return text was a defect: *"two readers
handed the same malformed tile could disagree about a sample and both be
conforming, which is the divergence this document exists to prevent."*
**Foreclosed, and visibly repaired at some point.**

**A-16. A user-metadata document decoding to 16 MiB + 1.**
Reader A applies a 16 MiB bound → ignore-record. Reader B declines the whole
file on resource grounds. Verifier A declines to decode → *cannot establish*.
Verifier B with a 32 MiB bound → *conforming*. Four behaviors, all licensed:
§18.2's note is written about this exact file, and §2.3 makes *cannot establish*
a statement about the verifier, not a finding about the bytes. **Foreclosed.**

**A-17. A verifier that implements experimental type 0x8001 vs one that does
not, on a conforming file carrying such a record with MU = 1.**
Verdicts: *conforming* and *cannot establish*. Different, and both defensible —
but §2.3 pre-empts this by making *cannot establish* explicitly not a finding
about the file, and §10.3 warns that experimental values carry no collision
protection at all. **Foreclosed.**

**A-18. Whether a reader must detect a layer record's name overrun at open.**
Two layer records with byte-identical name fields, where record A's name field
runs past its own `inline_length`. If A contributes a name, the file is
reject-file (duplicate); if not, A is reject-layer and B is fine. §19.1 step 4
decides it explicitly: *"a layer record whose name field does not lie entirely
within that record's inline_length yields no name field to compare, so it
contributes no name to the namespace"*, and F4's condition cell repeats the
qualifier ("both obtainable within their records' inline_length"). It then
closes the follow-up — uniqueness is decided *first*, over raw bytes, *"whether
or not each name is itself well-formed"*. **Foreclosed, and this is the single
most carefully-written paragraph in the document.**

### 3.5 Feature interactions

**A-19. Sparse tile under a filter chain.** A sentinel occupies no bytes and
never enters the pipeline; `[R-TYP-08]` reads it as fill. **Foreclosed.**

**A-20. Byte-shuffle over a mixed bool/numeric planar layer.**
`[R-COD-10]` gives the stride per *tile*, not per layer: element size for a
planar numeric plane, Q for interleaved, and 1 (identity) for a packed bool
plane. So one layer's filter is the identity for some of its planes and not for
others. Divisibility holds in all three cases (P·Bᶜ by Bᶜ; P·Q by Q; anything by
1), as the rule asserts. **Foreclosed.**

**A-21. Codec 3 on a tile whose decoded size is below 1 KiB.**
RFC 8878's Window_Descriptor cannot express a window below 1 KiB, and
`[R-COD-06]` forbids a declared window exceeding the decoded size — so a small
tile is encodable only as a single-segment frame. §17.2's note works this
through and concludes *"no conforming file turns on which derivation a reader
implements."* I checked the boundary: at decoded size exactly 1024 the
Window_Descriptor's minimum equals the decoded size, so both forms are
available; below 1024 only single-segment is. **Foreclosed, and the boundary is
the one the note names.**

**A-22. Compaction over a record the compactor cannot read.**
`[R-WRT-06]` bars compacting a file with an unimplemented MU = 1 record. For an
unimplemented MU = 0 record, §8.1 gives its extent no checksum, so there is
nothing for `[R-WRT-09]` to verify and nothing to fail. §22.3 states the residue
honestly rather than pretending otherwise. **Foreclosed.**

**A-23. A verifying compactor that detects a droppable violation.**
This one took me a while. `[R-WRT-06]` says a compactor *"MUST refuse to compact
when any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a
violation it has detected: it can neither drop the structure (§20.4,
`[R-WRT-07]`), nor re-emit it corrected"* — but §20.4 says *"A compactor may drop
it whenever it rewrites the file"* for MU = 0 / PE = 0 records. So: input with a
reserved-range top-level record, MU = 0, PE = 0, detected as F36 by a compactor
that is also a verifier. Compactor A drops it and emits a conforming file;
compactor B refuses. Different bytes.

What killed it: the MUST-refuse triggers only on *a check `[R-WRT-09]` obliges*,
and `[R-WRT-09]`'s list is the open, each retained layer's record, the index
chain, and each relocated extent's checksum. I enumerated what can fail in that
list — an open failure, a layer-record defect, an index-chain failure, a stored
tile's crc, a user-metadata extent's crc — and **none of those structures is
droppable**: the layer record and the user-metadata record both carry PE = 1,
and a stored tile cannot be dropped without changing the reference array, which
`[R-WRT-07]` forbids. So the flat claim "it can neither drop the structure" is
true for every structure that can trigger the refusal. F36 is not a
`[R-WRT-09]` check, so it triggers only the second clause ("MUST NOT emit a file
carrying a violation it has detected"), which dropping satisfies.
**Foreclosed** — but only just, and only by an enumeration the document does not
perform.

**A-24. `[R-ERR-04]`'s per-quantity guarantees, conjoined.**
A file with 65,536 layers, each `entry_count = 2³²`, each tile 256 MiB decoded,
is within every listed quantity and is on the order of 2⁷⁶ bytes; §21.9 says
*"Software that declines a file whose every quantity lies within the table is
not a conforming reader."* Is conforming-reader status therefore unachievable?
No — every guarantee is individually implementable in bounded memory by a
streaming reader: 256 KiB of CRC array, 1.25 MiB of one segment, 16 MiB of
directory, 256 MiB of one tile. §21.9's note reasons this way explicitly (*"the
segment-CRC array a reader fetches whole before using any entry (§15.4) is still
256 KiB"*). The guarantees are sized against *working set*, not file size, which
is the same invariant §6.4's note names for the open. **Foreclosed, and
elegantly.**

### 3.6 Arithmetic boundaries

**A-25. `entry_count` at the top of its domain.**
`entry_count = 2⁶³ − 1` forces `extent_length = entry_count × 20 + 2⁴⁷ × 4`,
which exceeds 2⁶³ − 1 → L2 via `[R-ENC-04]`. The largest legal `entry_count` is
about 4.61 × 10¹⁷, and the extent must additionally fit inside `[16, F − 64)`.
§22.2's note is written about exactly this amplifier and names both checks.
**Foreclosed.**

**A-26. The overflow-checked quantity list.**
I tried to find a product a reader must compute that L2 does not name. L2 names
the two extent sums, N, P, N·P, C·N, P·Q, P·Bᶜ, and the index-region formula.
The candidates it omits are all dominated by ones it names: V = P·C ≤ P·Q since
each Bᵢ ≥ 1 (and L2 says so, parenthetically); the maximum disk ordinal
(C−1)·N + (N−1) = C·N − 1 (and L2 says so); the in-tile ordinal ≤ P; the spatial
ordinal ≤ N; ⌈P/8⌉ ≤ P; Q ≤ 65,535 × 8; the region byte offset 20·k <
entry_count × 20. **No gap.**

**A-27. Sentinel versus the value domain, at the exact boundary.**
An entry with offset = length = 2⁶⁴ − 1 and crc ≠ 0 is *not* a sentinel (§15.2
requires crc 0), so `[R-IDX-02]`'s carve-out does not protect it — and then
`[R-ENC-03]` would call it out-of-domain, which T11 would register. But T11's
condition text excludes it in terms: *"the value being distinct from the
all-ones sentinel"*, and §15.3's second row assigns it directly. Same outcome
(reject-tile) on both routes. I also counted §15.3's *structural*-marked rows —
`[R-IDX-03]` says "Six rows are marked *structural*" and there are exactly six.
**Foreclosed.**

**A-28. A structurally-rejected entry inside a slab run, and in the coverage
walk.**
Three separate passages have to agree on this and do, word for word:
`[R-IDX-03]` (*"contributes no stored extent to the *verifier* rows ... and none
to `[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed that no
other claimant claims fall to slack"*), `[R-LIF-08]` (*"the walk passes over it,
and the bytes it nominally addresses fall to slack (§15.3)"*), and `[R-SLB-03]`
(*"they address no usable extent, and the run's stored tiles close over them"*).
And all three draw the same line at the same place: an entry whose *only* defect
is that its stored bytes fail its crc is **not** transparent. L41's condition
cell restates that boundary too. This is the kind of four-way agreement that is
usually where a round finds its defect; it holds. **Foreclosed.**

---

## 4. Findings

Seven. None of them is a clean two-verifier fork; I did not find one. One is
byte-level under the stated test, and I say so with my reasoning exposed so a
triager can downgrade it cheaply.

---

### F-1 (adversary-01) — AMBIGUITY — "the regions the verifier did walk" is undefined, and one reading makes the partial slack total vacuously zero

**Location.** §5.2, `[R-CNT-21]`; §9.7, `[R-LIF-08]`.

**Quotation** (§5.2, `[R-CNT-21]`):

> Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection stops it, or because the verifier elected under
> `[R-CNF-11]` to stop at the first violation — the verifier MUST report the
> total as partial. A partial total counts only the bytes no claimant claims
> within the regions the verifier did walk, and a verifier reporting one MUST
> also name the regions it did not walk and report their byte extent.

**The problem.** "Region" is used here as if it were defined. It is not. §9.7
describes the walk as an enumeration of *claimants* — records, extents,
non-sentinel index entries — not as a traversal of byte ranges. Three readings
are available and they give different numbers:

1. **"Regions walked" = the set of claimant extents enumerated.** Then "the
   bytes no claimant claims within the regions the verifier did walk" is
   identically **zero**, because that set contains only claimed bytes. Every
   partial total is 0. Absurd, but it is the reading the sentence's own
   vocabulary supports.
2. **"Regions walked" = a coarser byte range the verifier judges fully
   accounted.** Then the total is that range minus its claimants — the intended
   meaning, I think. But the document never says how a verifier establishes that
   a byte range is fully accounted, and the walk is not sequential: claimants
   are scattered across `[16, F − 64)` in any order `[R-SLB-05]` permits, so
   there is no prefix the verifier can honestly declare complete.
3. **"Regions" = the file's whole unwalked remainder,** i.e. `[16, F − 64)` minus
   what was walked. Then the number is computable but is the same number as the
   full total, and "partial" means nothing.

The companion MUST fails under reading 2 in a common case. Take a layer whose
`crc_of_crc_array` mismatches (L37, reject-layer). The verifier cannot use that
layer's entries — `[R-ENC-05]` bars it from acting on any integer whose covering
checksum has not verified — so it does not know how many stored tiles that layer
has, where they are, or how many bytes they occupy. It is nonetheless obliged to
"name the regions it did not walk **and report their byte extent**". It can name
and size the index region (the extent slot is in the layer record and the
directory CRC verified) but it cannot report the byte extent of the stored
tiles, which is the part that matters. The obligation is undischargeable for
that file.

**Which I picked.** Reading 2, because 1 is vacuous and 3 makes "partial"
contentless — and then I treated the second MUST as satisfiable only in the weak
form "name the structures I could not enumerate, and give the byte extent of
those whose extent I know". That is not what it says.

**What an implementer does wrong without it.** Reports 0 slack bytes on every
partial walk (reading 1), or reports a number that is not comparable with
another verifier's on the same file. §5.2 says this number "is what tells an
operator to compact" and §22.3 calls it "the number that distinguishes a working
file from a padded one", so the number is a deliverable, not a diagnostic aside.

**Byte-level?** **No.** A partial total only arises after a violation is
established or the verifier elected to stop, and in either case the verdict is
already fixed — §2.4 and §21.1 both say the per-requirement and unexamined
reports "constrain the report, not the verdict". Two verifiers agree
*nonconforming* and disagree only about a reported integer.

---

### F-2 (adversary-02) — AMBIGUITY — §20.4 states the flag authority for two cases and there is a reachable third

**Location.** §20.4 (the paragraph introducing the preservation table),
`[R-WRT-08]`; §7.3, `[R-CNT-22]`; §2.3, `[R-CNF-06]`.

**Quotation** (§20.4):

> Persistence governs every record type; only the authoritative source of the
> flags differs. For a type §7.3 registers, the registry's fixed flags govern
> rather than the stored ones (`[R-CNT-22]`) — both registered types carry
> PE = 1, so neither can be dropped, and implementing a record's type confers
> understanding of it, not permission to drop it. For a type the updater does not
> implement, the stored flags are authoritative (§7.3, `[R-CNT-15]`; MU = 1 with
> PE = 0 is read as PE = 1, `[R-CNT-12]`), and carry these obligations:

and (§7.3, `[R-CNT-22]`):

> Stored flag bits are authoritative **only** for record types the consuming tool
> does not implement (`[R-CNT-15]`).

**The problem.** The two cases named are (a) a type §7.3 registers, (b) a type
the updater does not implement. The third case — **a type §7.3 does not register
that the updater does implement** — is reachable in a *conforming* file, and no
flag authority is stated for it. `[R-CNT-22]`'s "only" is exclusionary and shuts
the stored-flags door explicitly; §7.3's table has no row; §10.4's registration
machinery, which is where MU/PE assignments come from, by definition never ran.

Concretely: a top-level record of experimental type 0x8001, stored MU = 0,
PE = 0, with an extent at (E, L). §10.3's prohibition on emitting experimental
values binds the writer's *conduct*, and §2.3's `[R-CNF-02]` plus §21.6's row
make the file **conforming**. An updater U implements 0x8001 (§10.3 warns U
cannot actually know it is the same 0x8001, which is part of the point). U
performs a commit that adds a layer — an independent change to the file's layer
set, so §20.4's MU = 0 / PE = 0 row's drop condition is met if that row applies.

- Updater U₁ reads the table as governing every record type (which §20.4's own
  first sentence and `[R-CNF-06]`'s "which govern every record type" both say),
  takes the stored flags as the only flags there are, and **drops** the record.
  Bytes E…E+L become slack; the output directory has one record fewer.
- Updater U₂ reads `[R-CNT-22]`'s "only" as binding, finds no authoritative flag
  source, and **retains** the record byte-identically, since retention is always
  safe.

Both outputs are conforming files. Both implementers can defend their reading
from the text.

**Which I picked.** U₁'s. The stored bits are the only bits in existence, and
retaining a record forever because its type happens to be understood is the
opposite of what §20.4's rationale wants. But I picked it against
`[R-CNT-22]`'s "only", which is the sharper sentence.

**What an implementer does wrong without it.** Emits a different file for the
same input and the same intent — or, worse, an updater that *stops* implementing
0x8001 in the next release changes its own drop behavior on the same file.

**Byte-level?** **Yes**, under the stated test — resolving it changes which byte
sequences a conforming updater may emit for a given input. I want to be
scrupulous about how far that goes: **no verifier's verdict on any file
changes.** Both outputs are conforming; both inputs are conforming; no reader
accepts or rejects anything differently. What forks is one actor's permitted
output. If the triage bar is "two implementations disagree about an accept/reject
verdict", this fails it; if it is the brief's literal "which byte sequences a
conforming implementation may emit", it meets it. I flag it byte-level and hand
the triager the argument for downgrading.

---

### F-3 (adversary-03) — AMBIGUITY — §4.7's three classes have no home for a pure-identity field, and §6.2 labels two of them "semantic"

**Location.** §4.7, `[R-ENC-16]`; §6.2's trailer layout table; the front
matter's "How to read this document".

**Quotation** (§4.7):

> Every field this specification defines is classified by what its *value*
> determines, each class being what the one before it is not. A field is
> **structural** if its value determines how any byte is located or decoded;
> **semantic** if not, but its value determines what decoded values mean; and
> **descriptive** if neither — its value determines nothing a conforming reader
> does, and a reader MUST NOT alter decoding based on it. Each descriptive
> field's definition states what a reader does when the field contradicts the
> data it describes. `[R-ENC-16]`

and (§6.2):

> | 16 | 8 | u64 | generation | semantic | 1 ≤ generation ≤ 2⁶³ − 1 (`[R-ENC-03]`) |
> ...
> | 48 | 8 | u64 | file_id | semantic | ≠ 0 |

**The problem.** Neither `file_id` nor `generation` determines "what decoded
values mean". Change `file_id` from X to Y and recompute the trailer CRC: every
byte of every reference array is identical, and no reader's returned value
changes. Change `generation` from 7 to 8 likewise. What they determine is cache
identity and revalidation (`[R-LIF-03]`) — which is neither of the first two
classes. So under §4.7's own definitions they are **descriptive**.

But descriptive is defined as "its value determines nothing a conforming reader
does", and both fields determine something a conforming reader does: `[R-CNT-06]`
makes `generation = 0` and `file_id = 0` reject-file, and `[R-LIF-03]` makes a
changed `file_id` "treat as a different file". So they are not descriptive
either. The partition claimed to be exhaustive ("each class being what the one
before it is not") has a hole exactly where a pure-identity field sits.

The same hole swallows every **name** field, which §4.7's note pushes into this
same taxonomy: *"its table omits the offset and class columns, and each field's
class follows from the definitions above."* A layer name's value locates no byte
and gives no decoded value a meaning, so it is not structural or semantic; but
its value determines whether the file is reject-file under `[R-ENC-15]`, so it is
not descriptive. And `[R-ENC-16]`'s second sentence — "Each descriptive field's
definition states what a reader does when the field contradicts the data it
describes" — is vacuous for a name and for `file_id`, which describe nothing.

`version_minor` is the only field in the document actually labelled
*descriptive* (I grepped: four hits for "descriptive", one of them a table cell),
and it is the only field for which the second sentence has content.

**Which I picked.** I treated the class labels as commentary and drove every
behavior from the requirements — which is what `[R-CNF-04]` and §21.1's
"the rule governs" both push you toward.

**What an implementer does wrong without it.** Nothing to the bytes; the risk is
to a future editor, who has a normative rule (`[R-ENC-16]`) asserting a total
classification that the document cannot actually carry out, and a second
sentence that cannot be satisfied for the fields the first sentence forces into
its class.

**Byte-level?** **No.** Reclassifying `file_id` or `generation` as descriptive
would add "a reader MUST NOT alter decoding based on it", which no reader does
anyway, and would not touch `[R-CNT-06]`'s gates. No byte and no verdict moves.

---

### F-4 (adversary-04) — OBSERVATION — the conformance corpus is normatively keyed to register row labels, which carry no stability guarantee

**Location.** §2.2; §21.8, `[R-ERR-02]`; §24, `[R-VEC-02]`, `[R-VEC-03]`; the
front matter's "How to read this document".

**Quotation** (§2.2):

> Identifiers are stable: they are never renumbered or reused, a withdrawn
> requirement leaves its identifier permanently retired, and numbers above 99
> extend naturally (`[R-ENC-100]`) without renumbering.

and (§24, `[R-VEC-02]`):

> Each vector is one file plus a manifest entry recording, at minimum: its
> identifier; whether the file is **conforming**; ... and, for each structure the
> file damages, the outcome class (§2.4), the scope, and the §21 register row it
> exercises.

and (front matter):

> Normative requirements carry stable identifiers like `[R-IDX-03]`; test vectors
> and conformance checklists cite identifiers, never prose positions.

**The problem.** §2.2 guarantees stability for `[R-XXX-NN]` identifiers and for
nothing else. Register row labels — `F17`, `L41`, `T24`, `R4` — are a second
identifier space with no stability clause anywhere in the document. Yet
`[R-VEC-02]` normatively requires every manifest entry to record "the §21
register row it exercises", `[R-ERR-02]` states corpus coverage in terms of rows
and instances, `[R-VEC-03]` says "every register row has at least one vector for
each instance it names", and Appendix H cites F7, F36 and L25 by label. The
corpus's primary key is therefore the one key the document does not promise to
keep.

The consequence is silent, not loud. If a row is removed and the rest renumbered,
every manifest entry naming a row past the deletion point now names a *different*
condition, with the same outcome class and scope more often than not, and
nothing mechanical catches it — a vector built for "the trailer magic is wrong"
that now claims to exercise "committed_file_length is not a multiple of 64" still
passes, still has the right verdict, and quietly leaves the real row uncovered.
The front matter's rationale for citing identifiers rather than prose positions
is precisely that identifiers are stable; row labels sit on the wrong side of
that line while carrying the normative weight of the corpus.

Nine rounds have read this document; the row labels have been renumbered at
least once during that; I checked all seventeen in-document row citations (§2.5
above) and they are all correct today. The exposure is not that they are wrong —
it is that nothing but hand-checking makes them right, and the corpus manifest
is outside the document where hand-checking will not reach.

**Byte-level?** **No.** No file's conformance turns on it.

---

### F-5 (adversary-05) — OBSERVATION — §21.1 carries no requirement identifier though it states three rules the register's architecture rests on

**Location.** §21.1; §2.2.

**Quotation** (§2.2):

> Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`.

and (§21.1, three separate normative statements, none of them carrying one):

> Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document ...

> ... but each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**.

> Some rows are strict specializations of others — F1 of F6 and of F8, F35 of
> F36, L24 of L25 — and a file exhibiting a specialization is recorded against
> the narrower row, whose detector and detection point are the ones that apply.

**The problem.** §21.1 opens by citing `[R-ERR-02]` — "The register — §21.2
through §21.5 (`[R-ERR-02]`) — enumerates ..." — but `[R-ERR-02]` is §21.8's
identifier and its subject is *conformance-vector coverage*, not the register's
constitution. §21.7 carries `[R-ERR-01]`, §21.8 `[R-ERR-02]`, §21.9
`[R-ERR-03]`–`[R-ERR-05]`. §21.1 carries none, and it is not a Note, Example or
Rationale, so §2.1 makes it normative.

The tie-break rule in particular is the one an implementer needs most and can
cite least. It is the sentence that decides, whenever a register row and its
governing rule disagree, which of the two an implementation follows — and it is
also the sentence §21.1 relies on again for §21.6 ("where such an entry and the
rule it cites diverge, the rule governs there too"). A conformance vector cannot
cite it, a checklist cannot cite it, and a future revision cannot retire it,
because it has no name.

**Byte-level?** **No.** The rules are stated; only their citability is missing.
No implementation reading §21.1 is left in doubt about what to do.

---

### F-6 (adversary-06) — OBSERVATION — §21.7's account of undetectable obligations omits `[R-ENC-06]`

**Location.** §21.7, `[R-ERR-01]`; §21.1; §4.2, `[R-ENC-06]`.

**Quotation** (§4.2):

> No field's width is ever a writer choice: every field's width is fixed by this
> specification, and a structure whose fields appear at any other width is
> invalid at its owning scope. `[R-ENC-06]`

and (§21.1):

> Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document,
> detectability being the gate `[R-CNF-07]` already applies and §21.7 the
> account, by class, of what fails it ...

and (§21.7, the second class):

> A second set of obligations is omitted from the register because a single file
> exhibits no witness of their violation. Committed-prefix immutability and the
> generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's
> history, which §9.7 does not reconstruct; the ordinal mappings of `[R-GEO-06]`
> and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it
> carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record encoding file
> offsets in its own payload is opaque by construction.

**The problem.** `[R-ENC-06]` is a MUST-level statement that a structure is
"invalid at its owning scope" — the document's standard phrasing for a
file-conformance violation, which `[R-CNF-08]` maps straight onto a reader
outcome. It has no register row and it is not among the obligations §21.7
accounts for. Under §21.1's completeness clause that is a defect unless it is
undetectable.

I convinced myself it *is* undetectable, and I want to record the argument
because the document should be making it. Take the trailer: if a writer emitted
`version_major` as a `u32` at offset 8, the bytes are `01 00 00 00` and a reader
parses `version_major = 1` from [8, 10) and `version_minor = 0` from [10, 12) —
a perfectly valid trailer. The wrong width leaves no witness. Where a wrong
width *does* leave one, the witness is already registered under a different
rule: 24-byte index entries emitted as 28 bytes trip `[R-CNT-17]`'s
`extent_length` cross-check (L22); a 28-byte record header trips §7.2's framing
(F29/L14). So `[R-ENC-06]` contributes no independent detectable condition, its
absence from the register is correct, and what is missing is the sentence saying
so.

`[R-WRT-05]`'s byte-identical re-emission is in the same position — it needs two
generations to witness — but §21.7 does name "properties of a file's history" as
a class, and re-emission plausibly falls in it. `[R-ENC-06]` falls in no named
class at all.

**Byte-level?** **No.** Nothing about the file changes; the omission is in the
document's account of itself.

---

### F-7 (adversary-07) — OBSERVATION — Appendix G's closing count of what the profile adds is wrong

**Location.** Appendix G (non-normative), closing paragraph, against items 4, 5
and 6 of the same appendix.

**Quotation** (Appendix G, closing):

> Everything else the profile needs is already mandatory — fill-encoded edge
> padding (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among them.
> Four things are not, and the items above are where the profile adds them: gap
> *content*, which `[R-CNT-03]` only advises; gap *extent*, which placement
> freedom (`[R-SLB-05]`) leaves open; sub-record order within a layer record's
> inline payload, which `[R-CNT-14]` leaves free; and the fill a writer records
> when its caller chooses none, which `[R-TYP-10]` states as a SHOULD.

**The problem.** At least three of the profile's own items close format freedoms
that are neither "already mandatory" nor among the four named:

- **Item 6** — *"The sentinel for every all-fill tile, so that a tile whose
  samples all equal fill is never stored"*. Nothing in the format requires this:
  §13 makes storing an all-fill tile perfectly conforming, and item 6 says why
  it matters ("otherwise two writers agreeing on content still disagree on
  bytes"). This is the largest freedom the profile closes — it changes *which
  tiles exist*, not merely their placement — and item 7 explicitly says so.
- **Item 5** — *"No declared alignment and no slab, or fixed declared values"*.
  Declaring alignment is a writer's free choice (§16.1's "A layer MAY declare").
  Item 5 even names the reason: "both change placement and neither is implied by
  content."
- **Item 4** — *"One generation"*. The number of commits behind a file is free.

Item 3 also closes **top-level record order**, and the closing paragraph names
only *sub-record* order as free — though `[R-CNT-14]` makes both free
("Record semantics MUST NOT depend on record order").

Items 1, 2, 8 and 9 pin the *producer* (a named encoder, a hash rule, the minor
floor, a named JSON writer) rather than a format freedom, and I can see the
reading under which those are excluded from the count. Items 4, 5 and 6 are not
producer-pinning; they are format freedoms, and they are not among the four.

**Which I picked.** I read the closing paragraph as a summary that lost track of
its own list, and treated items 1–9 as the operative content.

**What an implementer does wrong without it.** An implementer auditing itself
against the closing paragraph rather than the numbered list will believe four
things stand between it and reproducibility, and ship a writer that stores
all-fill tiles — the one item that makes two profile-conforming writers disagree
about the file's *structure*, not just its bytes.

**Byte-level?** **No.** Appendix G is identified non-normative and adds no
requirement to any actor by its own first paragraph.

---

## 5. Ranking the survivors

None of the seven forks a verifier's verdict on a concrete file. Ranked by how
plausible it is that a real implementation lands on the wrong side:

1. **F-1** (partial slack total) — highest. An implementer writing the verifier's
   report has to pick a reading *today*, and reading 1 is the one the sentence's
   own vocabulary supports while being obviously useless. The number is a
   deliverable the document twice calls operationally decisive.
2. **F-2** (updater flag authority) — the only byte-level candidate. Low
   frequency, since it needs a conforming file carrying an experimental type and
   an updater that implements it, and §10.3 says such a file should not be in
   circulation. But both readings are natural and `[R-CNT-22]`'s "only" is
   unambiguous about shutting the door the table needs open.
3. **F-4** (row-label stability) — no implementation lands wrong, but the corpus
   silently rots and nothing catches it. Cheapest to fix, highest leverage.
4. **F-7** (Appendix G's count) — an implementer that reads the summary instead
   of the list gets a materially wrong answer, but the list is right above it.
5. **F-3** (taxonomy) — no behavioral consequence; a future-editing hazard.
6. **F-5** (§21.1 unidentified) — no behavioral consequence.
7. **F-6** (`[R-ENC-06]` unaccounted) — no behavioral consequence.

## 6. What I could not determine

- Whether the four-way agreement on structurally-rejected index entries (A-28)
  holds under a fifth reading I did not think of. Four passages say the same
  thing in four vocabularies; I checked them against each other and against two
  constructed files, and they agreed, but this is the densest coupling in the
  document.
- Whether `[R-WRT-06]`'s "it can neither drop the structure" is *intended* as the
  narrow claim I verified it to be (A-23), or is a genuine oversight that happens
  to be unreachable. It is unreachable either way, so nothing turns on it, but
  the document does not perform the enumeration that makes it safe.
- Whether any conforming file can distinguish the three readings of "region" in
  F-1 by more than the integer reported. I do not think so, but a verifier that
  reports a *partial* total on a file another verifier certifies outright would
  be worth constructing, and I could not build one: a partial total requires an
  established violation or a deliberate early stop, and the first fixes the
  verdict.
