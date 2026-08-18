# Round 11 — Adversary transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,953 lines), in four `Read` passes covering lines 1–3953 with no gaps. I opened
no other file. I ran no `git` command, no directory listing, no web access, and
consulted no ADR, no `PLAN.md`, no `conformance/` artifact, and no
`spec/registry.json`.

I ran four things, all of which read only that file or nothing at all:

- `wc -l spec/tarn.md`
- `python3 crc.py` — a self-contained CRC-32C implementation (reflected poly
  0x82F63B78), reading no files, used to check §4.5's check vector and §15.4's
  all-sentinel segment constant.
- `python3 crc2.py` — the same CRC over the hex dump of Appendix A, which I
  pasted into the script by hand from what I had read. Reads no files.
- `python3 count.py` and two `grep`/`python3` passes over `spec/tarn.md` only —
  to count §21's register rows and instances mechanically, to check requirement
  identifier hygiene, and to locate the three phrases I quote in findings 02,
  03 and 04.

Scratch files written under my scratchpad: `crc.py`, `crc2.py`, `count.py`, and
this transcript. I did not read the scratchpad directory.

I used general knowledge of DEFLATE / zstd / LZ4 framing only to *generate*
suspicions (e.g. "can an LZ4 frame magic also parse as a valid block?"); every
suspicion was settled against this document's text, and the one place where I
reasoned about an external format's bytes (the LZ4 token) I show the arithmetic
below so it can be checked.

---

## 1. What I built

The charter asks for a file two conforming verifiers could judge differently. I
worked from the outside in: first I implemented, byte for byte, the degenerate
files the document says exist, to find out whether the document actually
determines them; then I attacked the seams.

### 1.1 The 128-byte file — implemented and checked

§5.1's example and Appendix A both claim the smallest conforming file is 128
bytes. I reconstructed it from §5.1/§6.1/§6.2/§7.1 *without* looking at
Appendix A's dump first, then diffed:

```
[0,16)    front block   89 54 41 52 4E 0D 0A 1A + 8 zero bytes   (§6.1)
[16,20)   directory     zero records, so 4 bytes = CRC-32C("") = 00000000
[20,64)   pre-trailer pad, 44 bytes, slack
[64,128)  trailer
```

Trailer field placement derived from §6.2's table with the trailer base at 64:
magic [64,72); version_major [72,74); version_minor [74,76); flags [76,80);
generation [80,88); dir_offset [88,96); dir_length [96,104);
committed_file_length [104,112); file_id [112,120); reserved [120,124);
CRC [124,128). Appendix A's annotation table agrees on every one.

Then I computed, with my own CRC-32C:

```
CRC-32C("123456789") = 0xE3069283      §4.5's check vector      ✓
CRC-32C(<zero bytes>) = 0x00000000     §4.5's check vector      ✓
CRC-32C(Appendix A trailer[0,60)) = 0xE00938D2                  ✓  (stored: D2 38 09 E0)
```

Appendix A is byte-correct. Decoded fields: version_major 1, version_minor 0,
flags 0, generation 1, dir_offset 16, dir_length 4, committed_file_length 128,
file_id 0x0123456789ABCDEF, reserved 0. All within §6.2's valid ranges.

I also re-derived §5.1's 128 floor independently: `dir_offset ≥ 16`,
`dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64` gives `20 ≤ F − 64`, so
`F ≥ 84`; `F mod 64 = 0` gives `F ≥ 128`. `[R-CNT-27]` is derivable, not
asserted. Slack total for this file: `128 − (16 + 4 + 64) = 44`, matching
Appendix A's "44 bytes".

**Verdict: fully determined. No guesses.**

### 1.2 The smallest file containing a layer — implemented

Nothing in the document shows this, so I built it. One layer, rank 1, one
uint8 channel, extent 0 (so `[R-GEO-02]`'s valid empty layer), no sub-records.
Inline payload packed per §7.4's table order, no padding between fields:

| field | bytes |
|---|---|
| name `a` | `01 61` → 2 |
| layout = 1 | 1 |
| linearization = 1 | 2 |
| codec = 1 | 2 |
| filter = 1 | 2 |
| A = 0 | 8 |
| S = 0 | 8 |
| A_slab = 0 | 8 |
| d = 1 | 1 |
| C = 1 | 2 |
| dim entry `x`, E=0, T=1 | 2 + 8 + 8 = 18 |
| chan entry `c`, type 6, fill `00` | 2 + 2 + 2 = 6 |
| index_encoding = 1 | 1 |
| entry_count = 0 | 8 |
| crc_of_crc_array = 0 | 4 |
| **total inline_length** | **73** |

Record = 24 + 73 = 97; directory = 97 + 4 = 101 at [16,117); pad [117,128);
trailer [128,192); F = 192.

Cross-checks the document forced me to run: G₀ = ⌈0/1⌉ = 0, so N = 0, so
addressed-tile count 0, so `entry_count = 0` (`[R-CNT-17]`), so extent slot
(0,0) (§7.4) and `crc_of_crc_array = 0` (`[R-CNT-23]`, L27), and
`[R-CNT-17]`'s length formula yields 0 = 0. Every one of those is stated.
`[R-CNT-16]` (A and S mutually exclusive) is satisfied vacuously.

**Verdict: fully determined. No guesses.**

### 1.3 The smallest file with a stored tile — implemented

Rank 1, E = 1, T = 1, C = 1 uint8, interleaved, codec 1, filter 1. N = 1,
P = 1, Q = 1, decoded size = P·Q = 1 byte. entry_count = 1. Index region
length by `[R-CNT-17]` = 1×20 + ⌈1/2¹⁶⌉×4 = 24.

```
[0,16)    front block
[16,17)   the one stored tile (1 byte)
[17,41)   index region: entry[0] = {offset 16, length 1, crc = CRC32C(tile byte)}
                        + segment CRC array = 1 u32 over those 20 bytes
[41,142)  directory (101 bytes; same layer record, extent slot now (17,24))
[142,192) pad, 50 bytes
[192,256) trailer, F = 256
```

`[R-COD-04]` forced `length = decoded size = 1`. `crc_of_crc_array` =
CRC-32C over the 4-byte segment CRC array. `[R-SER-05]` imposes nothing
(no padding position: G·T = 1 = E). Every value determined.

I note that this is the *only* file shape where I had to reason about
`[R-COD-04]`'s "checkable from the entry and the layer record alone, before any
payload fetch" — and it does check out: a codec-1 layer's index is fully
validatable at layer-access time except for the entry CRCs.

### 1.4 The all-sentinel segment constant — recomputed

§15.4 and Appendix B pin `0xEECB3BB2` as the CRC-32C of a full segment of
sentinels. I built 65,536 copies of `FF ×16 00 ×4` (1,310,720 bytes) and got:

```
0xEECB3BB2   ✓
```

This is the one constant in the document a writer may emit *without computing
it* (`[R-IDX-05]`), so an error there would have been a live byte-level defect
— a sparse writer would emit an index whose segment CRC mismatched, and every
reader would reject-layer. It is correct.

### 1.5 The register's own arithmetic — recounted

§21.8 claims "121 conditions over 248 instances", and §21.1 makes the count
mechanical: "Instances within a cell are separated by semicolons, and a cell
reading — is one instance". I parsed every `| F<n> |`, `| L<n> |`, `| T<n> |`,
`| R<n> |` row out of the document and applied exactly that rule:

```
rows:      F 36   L 49   T 26   R 10   = 121      (§21.2/3/4/5 say 36/49/26/10) ✓
instances: F 53   L 106  T 45   R 44   = 248                                     ✓
```

Both numbers are exactly right. I also checked the §21.1 specialization claims:
F1's two instances are a front-block mismatch (F6) and a trailer-magic
mismatch (F8) ✓; F35 ⊂ F36 ✓; L24 ⊂ L25 ✓.

I checked requirement-identifier hygiene across the whole document: prefixes
CNF 1–12, CNT 1–27, COD 1–11, ENC 1–16 (plus the illustrative `[R-ENC-100]` in
§2.2), ERR 1–5, EXT 1–5, GEO 1–6, IDX 1–5, LIF 1–8, MDL 1–2, MTA 1–9, PRV 1–5,
RDR 1–4, SEC 1–7, SER 1–9 (4 withdrawn, and it appears only in §14.4's
withdrawal note), SLB 1–5, TYP 1–10, VEC 1–4, WRT 1–9. No gaps, no duplicates,
no dangling reference. This is the cleanest identifier space I have audited in
this document.

### 1.6 Worked examples spot-checked

I recomputed every numeric example in Part II and Part III rather than trusting
them, because an example that disagrees with its rule is the cheapest way to
fork two implementations:

- §11.2: (1024, 2048)/(256,256) → G = (4,8), N = 32, P = 65,536 ✓; with
  E_y = 1000, G_y = ⌈1000/256⌉ = 4 ✓.
- §11.4: tile (1,2) → s = 1·8 + 2 = 10 ✓; in-tile (44,188) → 44·256 + 188 =
  11,452 ✓; planar c = 2 → 2·32 + 10 = 74 ✓.
- §14.2: (2,3), P = 6, uint8 + uint16 → Q = 3, size 18; ordinal 5 at [15,18) ✓;
  planar `b` 12 bytes, ordinal 5 at [10,12) ✓; float32 + bool → Q = 5, size 30,
  ordinal 5 at [25,30) ✓.
- §14.3: (2,5), P = 10, alternating → byte 0 = 0b01010101 = 0x55 ✓; byte 1
  bits 0–1 = 1,0 = 0x01 ✓; with fill true, 0x01 | 0xFC = 0xFD ✓.
- §14.5: (5,5)/(4,4) → grid 2×2, edge tile (1,1) covers 4–7 both axes → 1 real
  position and 15 padding ✓; uint16 → 32 bytes ✓; ordinal of (4,4) is 0 ✓.
- §17.3: three float32 shuffled at s = 4, n = 3 →
  `00 00 00 00 00 00 80 00 40 3F 40 40` ✓ (I re-derived it from
  "byte i of group j at offset i·n + j").
- §15.4: entry_count = 1,000,000 → 16 segments (15 full + 16,960) ✓, CRC array
  64 bytes ✓, region 20,000,064 ✓, k = 999,999 in segment 15 at
  segment-relative byte 20 × 16,959 = 339,180 ✓, segment 15 at
  [19,660,800, 20,000,000) ✓, one full segment = 65,536 × 20 = 1.25 MiB ✓.
- §15.4 second example: planar C = 4, N = 32 → disk ordinal 74, entry at
  [1,480, 1,500) ✓; channel 3's entries are 96–127 ✓.
- §20.3: 32-tile index re-emission = 32·20 + 4 = 644 ✓.
- §21.9's note: 2³²/2¹⁶ segments × 4 = 256 KiB ✓; 2³⁶ → 4 MiB ✓. §24's "tens of
  gigabytes" for the 2³² index region: 2³²·20 + 2¹⁶·4 = 85,899,608,064 ≈ 80 GiB ✓.
- L2's parenthetical dominance claims: C·N − ((C−1)N + N − 1) = 1 ≥ 0 ✓;
  P·Q ≥ P·C because Q = ΣBᵢ ≥ C (every Bᵢ ≥ 1) ✓.

Every example is arithmetically correct. I found no numeric error anywhere in
the document.

---

## 2. Attacks that failed, and the sentence that forecloses each

This is the honest half of the result. Each of these is a file I was prepared to
build; each died on a specific sentence.

**A2.1 — Two layer records sharing one tile-index region.** Two layers with
identical geometry whose layer records carry the same extent slot, so one index
region serves both. Foreclosed: `[R-CNT-13]` — "within the live committed
state … no two extent slots and no two structures overlap … any overlap across
layers or touching another scope's structures as reject-file". F33 registers it.
Both verifiers reject.

**A2.2 — Deduplicated tiles inside one layer.** Two index entries with the same
offset/length/crc. Foreclosed: §15.3's row "two stored extents of the same layer
overlap … *verifier*: reject-layer". A reader accepts (it is not obliged to
detect overlap); both verifiers reject. This is a designed reader/verifier seam,
not a fork.

**A2.3 — An index entry whose bytes are simultaneously claimed by a
structurally-invalid sibling entry.** Entry 0 = {1000, 100, X} valid;
entry 1 = {1000, 0, Y}. Foreclosed and *deliberately* so: §15.3 marks the
`length = 0` row *structural*, and §9.7 says such an entry "contributes no
stored extent to the walk", so there is no overlap to record — entry 1's tile
is rejected and entry 0 stands. I then flipped it: entry 1 = {1000, 100, Y}
with bytes matching X. §15.3 — "An entry whose only defect is that its stored
bytes fail its crc is well-formed … its extent stands and it keeps its place in
the *verifier* rows" — so this one *does* overlap, L18 fires, reject-layer.
The six *structural* rows are counted correctly in §15.3 ("Six rows are marked
*structural*"): I counted them, there are exactly six.

**A2.4 — A structure between the live directory and the live trailer.** I built
a layout `front | dir | tile | pad | trailer`. Foreclosed: `[R-CNT-05]` — "A
verifier MUST treat a structure in that gap as a validity error at file scope",
F7. A reader accepts; both verifiers reject. I checked that this makes
"the directory is the last structure" a hard invariant, and that §5.1's,
§20.3's and §20.5's figures and Appendix G item 3 all respect it.

**A2.5 — A longer-than-necessary pre-trailer pad.** Directory ends at 100,
trailer at 192. `[R-LIF-02]` step 5 says "append the pad to the next 64-byte
boundary", so no conforming commit produces this — but is the *file* conforming?
Foreclosed explicitly, in the same sentence: §6.2 — "a longer gap is
conforming, and no conforming commit produces one". And `[R-CNF-02]` provides
the general machinery: "A writer obligation whose violation this specification
expressly declares not to be a file-conformance violation … binds the actor".
Both verifiers certify.

**A2.6 — file_id with bit 63 set.** `[R-ENC-03]` caps "every offset, length,
extent, and count" at 2⁶³ − 1. Is file_id one? Foreclosed: §6.2's table gives
file_id's valid values as "≠ 0" and nothing else, `[R-ENC-03]`'s enumeration
does not reach it, and Appendix G item 2 has the profile derive file_id from a
cryptographic hash — which sets bit 63 half the time. A verifier that
over-applied `[R-ENC-03]` here would be wrong, and F12's condition is
"file_id is 0", full stop.

**A2.7 — An experimental-range record type carrying MU = 1 at top level.** The
reader must reject (`[R-CNT-15]`) and the file is conforming (`[R-CNF-02]`).
Two verifiers: one reports *nonconforming*, one *cannot establish*. Foreclosed
by §2.3, which names this case in the *cannot establish* list verbatim — "when
a record carries MUST_UNDERSTAND = 1 with a type it does not implement
(§21.6)" — and by §21.6's closing paragraph. A verifier that reports
*nonconforming* here is refuted by text naming the exact condition.

**A2.8 — A conforming file with a reserved-range record type, MU = 0.** Reader
ignores (`[R-CNT-15]`), verifier rejects (F36). Not a fork: F36 is explicit and
its detector is the verifier, and §21.6's table row distinguishes the
experimental case from the reserved one in as many words.

**A2.9 — An LZ4 frame smuggled in as a block (T23).** T15 and T16 (deflate
wrappers) carry the disclaimer "the check that detects it is T24's or T25's, and
this row records the cause rather than a procedure of its own"; T23 (the lz4
analogue) does not, which reads as though a reader has an independent magic
sniff. I tried to build bytes that are both an LZ4 frame *and* a valid block.
Frame magic is `04 22 4D 18`. As a block, the first byte is the token: 0x04 →
literal-count nibble 0, match-length nibble 4 (match length 4 + 4 = 8), so the
next two bytes are the little-endian match offset `22 4D` = 0x4D22 = 19,746,
against zero bytes of produced output. That is "lz4 match offset … reaching past
produced output" — T25. So *every* LZ4 stream beginning with the frame magic is
an invalid block, T23 is always detected as T25, and no file sits on the seam.
Foreclosed by arithmetic rather than by text; I record it here because the
missing disclaimer is a cosmetic asymmetry with no reachable consequence, and
`[R-VEC-02]`'s "where a condition cannot be isolated … the entry records every
row the file exercises" already handles the corpus side.

**A2.10 — A remote verifier that never fetches bytes [0,16).** `[R-CNT-04]`
exempts a non-resident reader; F6's Detector cell says "reader"; §9.7's walk
claims [0,16) but §8.1 states no checksum over it, so the walk's
"each verifies against the checksum covering it, where §8.1's map states one"
imposes nothing. So: does a remote verifier have to check the front block?
Foreclosed by §2.3 — a verifier is "A reader that additionally checks every
file-level requirement — **including those ordinary readers are exempted
from**". The front block is precisely such a requirement. A verifier that
skipped it would be certifying a file it had not checked, and `[R-CNF-11]`'s
*cannot establish* is available only "on a capability or resource ground",
which fetching 16 bytes is not. Foreclosed — but Appendix H's verifier
checklist, which purports to enumerate exactly "the checks readers are exempt
from", omits it. That is finding 06.

**A2.11 — A reserved enum value assigned by a later minor version.** A file at
version_minor = 7 carrying sample type 14. §6.3 says "A reader MUST NOT reject a
file for its version_minor", §4.3 lists "new enum values in ranges this
specification reserves" as a growth vehicle, and §12.2's note says such a value
"makes exactly that layer unreadable (reject-layer), never the file". Could a
verifier report *cannot establish* rather than *nonconforming*? Foreclosed:
`[R-TYP-03]` — "a reader MUST treat any other value — 0, every reserved value,
and the experimental range included — as a validity error at layer scope" —
plus §2.3's "An established violation takes priority". L34 registers it. Both
verifiers report nonconforming. The residual observation — that "conformance to
a stated format major version" is evaluated against a document that minor
versions amend — is a meta-level tension I could not turn into a file, so I do
not report it.

**A2.12 — Zero-extent layer under codec 4 with an oversized tile shape.**
`[R-COD-07]` caps decoded tile size at 0x7E000000 for codec 4; a layer with
E = 0 addresses no tiles. Foreclosed *and anticipated*: §17.2's note —
"the cap is quantified over the layer's *addressed* tiles, so a layer that
addresses none … satisfies it whatever its tile shape declares … `[R-ENC-04]`'s
overflow rule carries no such quantifier — so P·Q and P·Bᶜ are checked in an
empty layer even though this cap is not." This is the single best-defended
boundary in the document.

**A2.13 — A layer declaring A = 2⁶² (or A_slab = 2⁶²).** No offset ≥ 16 in any
realizable file is 2⁶²-aligned, so the layer can carry no stored tile. Legal:
`[R-SLB-01]`'s invariant is over stored tiles, and an all-sentinel layer
satisfies it vacuously. §24's "every hard limit of `[R-ERR-05]` has one [a
vector] at its stated bound" is therefore constructible here — as an
all-sentinel layer. Determined.

**A2.14 — Zero-length and one-past-the-end boundaries.** I walked every bound:
`extent_offset + extent_length ≤ F − 64` (equal is legal, §9.7's "[16, F − 64)"
agrees, T9/F32/L17 all say "exceeds"/"past"); `offset < 16` vs `offset` in
1–15 vs 0-with-nonzero-length (T8/F31/F30/L15/L16 partition it exactly);
`dir_length ≥ 4` and `dir_offset ≥ 16`; sentinel vs `offset > 2⁶³ − 1`
(`[R-IDX-02]` — "Sentinel entries are a reserved pattern, not offsets or
lengths"); `entry_count = 0` vs a nonzero slot (L22 enumerates both
directions). I found no boundary stated twice with different endpoints.

**A2.15 — A user-metadata extent of exactly 4 bytes, and of exactly 5.** 4 is
`[R-CNT-25]`'s scope-level error (F22/L11) because "that failure precedes the
document" (`[R-MTA-02]`); 5 leaves one document byte, which under encoding 1
cannot be valid JSON (R7, ignore-record) and under encoding 2 cannot carry a
frame magic (R4). The quarantine boundary — framing errors take the containing
scope, document errors take ignore-record — is drawn in one sentence and holds
at both values.

**A2.16 — The interleaved bool byte 0x02.** Two readers: one returns "true"
(`[R-SER-08]`), one rejects the tile (`[R-CNF-12]`). Divergent behavior, but the
file is nonconforming either way (T2), both verifiers agree, and §14.2's
rationale states the trade explicitly. Not a fork. The residual — whether a
byte-oriented API returns 0x01 or 0x02 for that sample — arises only in a
nonconforming file and §14.2 fixes bool's encoding as 0x00/0x01, so I do not
report it.

**A2.17 — Compaction of a file whose layer-2 sub-record has an unknown MU = 1
type.** This one nearly survived; it is finding 08.

---

## 3. Findings

Eight. None of them, in my judgement, forks the bytes. I say why in each case,
and I say where I think I could be wrong.

---

### adversary-01 — CONTRADICTION — §4.7, `[R-ENC-16]`

**§4.7 asserts `fill` is the only semantic field, but §4.7's own definition of
*structural* covers `fill` twice over.**

Quoted (§4.7):

> A field is **structural** if its value determines anything a
> conforming reader or verifier does with the file's bytes — where a
> byte lies, how it decodes, or whether the file, layer or tile is
> accepted at all, which is the sense `[R-CNT-07]`, `[R-MTA-02]` and
> `[R-SEC-06]` already use. It is **semantic** if not, but its value
> determines what decoded values are. […] In format major 1 `fill` is the
> only semantic field and `version_minor` the only descriptive one:
> every other field this specification defines is structural.

And, in the same subsection's Note:

> A variable-length field's value includes its length prefix, so a name
> is structural: it determines where the field after it begins.

Two independent grounds make `fill` structural under those definitions, and
§4.7 says "each class being what the one before it is not", so it cannot be
both.

*Ground 1 — fill's value decides whether a tile is accepted.* `[R-SER-05]`:
"at every padding position, a writer MUST encode, for each channel the position
carries, that channel's fill value … a verifier MUST check it, and a violation
is a validity error at tile scope." Register rows T4 and T5 record it. Take
§14.5's own worked example: extents (5,5), tiles (4,4), one uint16 channel,
fill 0xABCD, edge tile = `<sample> CD AB ×15`. Change *only* the fill field in
the layer record to 0x1234 and those same 32 tile bytes flip from conforming
to nonconforming. That is squarely "whether the … tile is accepted at all".

*Ground 2 — fill's value decides whether a layer is accepted.* `[R-TYP-07]`:
"For bool, the fill field is one byte and its value is constrained: `0x00`
(false) or `0x01` (true). Writers MUST NOT emit any other byte; a reader MUST
treat any other byte as a validity error at layer scope." Register row L35.

*Ground 3 — fill is a length-prefixed variable-length field.* §7.4's table
gives the channel entry as "name (u8 len + bytes) · type u16 · fill (u8 len +
bytes)". Under §4.7's own Note, a variable-length field's value includes its
length prefix and so determines where the next field begins — exactly the
argument the Note uses to classify *name* as structural. The fill field is the
same shape, and the next channel entry begins after it.

§13.1 restates the classification on a *narrower* principle than §4.7 defines,
which is how the inconsistency survives:

> The fill value is semantic (§4.7): it affects what unstored samples read
> as, never how any byte is located or decoded

— note the omission of §4.7's third clause, "or whether the file, layer or tile
is accepted at all". §13.1 also anticipates ground 3 ("the field's length
prefix is §7.4's framing, cross-checked against the element size") but §4.7's
Note offers no such carve-out and applies its rule to *any* variable-length
field.

**What an implementer does wrong without this:** nothing to a byte. That is why
I do not flag it byte-level — but it is a genuine self-contradiction in the one
subsection whose whole job is to define an exhaustive, mutually exclusive
taxonomy, and it is the kind of claim ("every other field this specification
defines is structural") that invites exactly this check.

**Which reading I pick:** `fill` is structural under §4.7's definitions, and
either §4.7's definition of structural must drop the acceptance clause (which
would break `[R-CNT-07]`'s and `[R-SEC-06]`'s use of the word), or the
exhaustive sentence must say that format major 1 has no semantic field at all
and delete the class, or the definition of *semantic* must be stated as an
override rather than a residue ("a field is semantic if its value determines
what decoded values are, whatever else it determines"). The last is what §13.1
appears to intend.

**Byte-level: no.** No normative rule keys off the structural/semantic
distinction. Only *descriptive* carries a MUST (`[R-ENC-16]`: "a reader MUST NOT
alter decoding based on it"), and `[R-MTA-02]`/`[R-SEC-06]` use "structural" as
a synonym for "not user metadata", which is unaffected. A verifier's verdict on
any file is identical under either classification, because L35, T4 and T5 state
their conditions directly.

---

### adversary-02 — CONTRADICTION — front matter (lines 12–20) vs §2.1, `[R-CNF-01]`

**A front-matter block labels itself non-normative; `[R-CNF-01]`'s exception
list is exhaustive and does not reach it.**

`[R-CNF-01]` (§2.1), quoted in full:

> All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative. `[R-CNF-01]`

The block at the top of the document reads:

> **How to read this document** *(non-normative).* Sections follow a fixed
> rubric where applicable: purpose, byte-layout table, writer rules, reader
> rules, error handling, worked examples. On-disk structures are presented
> as offset/size/type/name/valid-range tables. Every field is classified as
> **structural** … Normative requirements carry
> stable identifiers like `[R-IDX-03]`, and test vectors cite those
> identifiers rather than prose positions.

It is not §1 (it precedes §1); it is not labeled *Note*, *Example* or
*Rationale*; it is not an appendix. I grepped every occurrence of
"non-normative" in the document: line 12 is the only one outside an appendix
heading, and Appendix F (Normative references) is correctly *not* marked, so the
appendix half of the rule is clean. The stray is this one block.

**The permitted readings.** (a) `[R-CNF-01]`'s list is exhaustive as written,
and the block is normative despite its label — in which case the document
contains normative text that declares itself non-normative. (b) The
self-label governs and `[R-CNF-01]`'s list is incomplete. I pick (b) as the
evident intent, but only (a) is what the text says.

**Why it matters at all, and why not much.** Read as normative, the block makes
three claims that do not survive contact with the document. "On-disk structures
are presented as offset/size/type/name/valid-range tables" — §6.1's front-block
table has columns Offset | Size | Value | Class (no type, no name, no valid
range) and §7.2's record-header table has no valid-range column. "test vectors
cite those identifiers rather than prose positions" — `[R-VEC-02]` has the
manifest record "the §21 register row it exercises", which is a row label
(F7, L24), not an `[R-…]` identifier. Under reading (a) those are normative
statements the document falsifies; under (b) they are prose.

**Byte-level: no.** Nothing in the block constrains any byte of any file.

---

### adversary-03 — AMBIGUITY — §21.7 `[R-ERR-01]` and §7.2 `[R-CNT-13]`

**§21.7 justifies omitting `[R-CNT-13]`'s no-embedded-offsets prohibition from
the register on the ground that it is "opaque by construction" — which is false
for the one MU = 0 record type this specification defines and whose content it
fully specifies.**

Quoted (§21.7):

> `[R-CNT-13]`'s prohibition on an MU = 0
> record encoding file offsets in its own payload is opaque by
> construction

The prohibition (§7.2, `[R-CNT-13]`):

> For a record
> with MU = 0, the extent slot is its only sanctioned reference to bytes
> outside the record sequence: neither its inline payload nor its extent
> contents encode offsets or lengths of other file bytes — this is what
> lets a compactor relocate an unknown ancillary's extent without
> parsing it (§20).

§7.3 registers exactly one MU = 0 type: 0x0002, user metadata. Its extent
contents are not opaque — they are a JSON document this specification defines
down to duplicate-key identity and number finiteness (§18.2), which a reader
decodes and a verifier checks (F27/L48, R5–R10). So the stated ground for
omitting the prohibition from the register is untrue for the only instance of
the rule that a format-major-1 file can exhibit.

**Permitted readings.**

(a) The prohibition binds every MU = 0 record including user metadata. Then a
document containing, say, `{"acme.index_at": 16, "acme.index_len": 24}` — where
those are the true offsets of a layer's tile-index region — violates
`[R-CNT-13]`, the file is nonconforming, and §21.1's normative completeness
clause is breached, since "a *detectable* file-conformance violation this
specification names and the register omits is a defect in this document."

(b) The prohibition binds only records whose payload the format leaves opaque —
i.e. unknown ancillaries — the compactor-relocation clause being the operative
scope. Then user-metadata documents may carry any numbers they like, and §21.7's
"opaque by construction" is true of everything the rule reaches.

**Which I pick, and why.** (b), on two grounds: the rule's own trailing clause
names the purpose ("this is what lets a compactor relocate an unknown
ancillary's extent without parsing it"), and `[R-MTA-02]`/`[R-SEC-06]` already
make user metadata structurally inert by a *reader-side* prohibition rather than
a content-side one — "A reader MUST NOT let any part of a user-metadata document
affect how a byte is located, decoded, or returned". Under (b) the register is
complete and §21.7's conclusion stands; only its stated reason is wrong for the
0x0002 case, and the honest reason is "semantically undecidable" rather than
"opaque".

**What an implementer does wrong without this:** a verifier author reading (a)
has an unimplementable obligation on their list and no register row to hang it
on; a specification editor reading §21.7 at face value believes a claim about
the document's own contents that its §7.3 table refutes.

**Byte-level: no.** Under (a) the violation is undecidable — no verifier can
determine whether an application means a JSON number as a file offset — so no
verifier can *establish* it, and §2.3's "An established violation takes
priority" never fires. Both verifiers certify the same files under either
reading. I considered flagging it byte-level (reading (a) does change which
byte sequences a conforming writer may emit) and decided against it: a rule no
implementation can evaluate cannot separate two implementations' verdicts.

---

### adversary-04 — AMBIGUITY — §20.5, `[R-WRT-07]` vs §20.2, `[R-WRT-02]`

**§20.5 grants a compactor placement freedom "anywhere §5.2 admits", dropping
the declared-layout-invariant clause that §20.2 attaches to the identical grant
for a creator.**

§20.5, `[R-WRT-07]`:

> A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits: every stored tile's bytes verbatim …

§20.2, `[R-WRT-02]`, the same grant for a creator:

> each layer's stored tiles, tile-index region, and
> any record extents, in any order satisfying §5.2's coverage
> classes (`[R-CNT-02]`, `[R-CNT-03]`) and every declared layout
> invariant (`[R-SLB-01]`, `[R-SLB-03]`) — placement is otherwise
> free (`[R-SLB-05]`)

§5.2 says nothing about alignment or slabs; §16 does. The concrete file: input
declares layer L with slab S = 8, A_slab = 4096, eight stored tiles packed and
4096-aligned per run. Compactor A reads §20.5 literally and packs every
structure contiguously from offset 16; its output's run-0 first stored tile is
at offset 16, so `offset mod 4096 ≠ 0` — L42, reject-layer. Compactor B
re-establishes the alignment.

**Permitted readings.** (a) §20.5's grant is complete, and a compactor may
discard declared placement. (b) The grant inherits §20.2's qualification.

**Which I pick.** (b), decisively, on the strength of two sentences in the same
requirement — `[R-WRT-06]`: "Given a conforming input the output is a
conforming file", and "A compactor satisfies every writer requirement for the
bytes it produces (`[R-CNF-06]`)". I also checked whether a compactor could
escape by *clearing* the slab declaration: it cannot. `[R-SLB-04]`'s clearing
licence is conditioned on a commit that "supersedes a stored tile in, or grows
the extents of" the layer, which compaction does neither of, and `[R-WRT-07]`
enumerates the only layer-record fields a compactor may change ("re-points
extent slots, regenerates each relocated tile-index region … and updates the
layer-record fields covering a regenerated region (crc_of_crc_array)"). So a
compactor must honour A and A_slab.

**What an implementer does wrong without this:** compactor A ships, and every
slab- or alignment-declaring file it touches comes out nonconforming at layer
scope, detectable only by a verifier (L40/L41/L42 all carry Detector *verifier*)
— which is precisely the class of damage a pipeline that "verifies rather than
merely reads" (§22.3) is warned about, and which an ordinary reader will never
surface.

**Byte-level: no.** Compactor A's output is nonconforming under both readings —
L40/L41/L42 state their conditions over the output's bytes without reference to
how it was produced — so no verifier's verdict on any file changes. The fork is
in which tool is conforming, and it is closed by `[R-WRT-06]`'s next sentence.

---

### adversary-05 — OBSERVATION — Appendix G, items 2 and 3

**The reproducible-writer profile leaves open two degrees of freedom it exists
to close, and does so silently — unlike items 1 and 9, which name the residual
freedom and pin the producer.**

Appendix G's stated purpose:

> Applications that
> need byte-identical output — content-addressed storage, reproducible
> builds — can adopt this profile, which closes the degrees of freedom
> this format deliberately leaves open.

*Gap 1 — the order of record extents across the top-level / sub-record
boundary.* Item 3:

> **A total emission order, contiguously.** For each layer in
> ascending layer-name byte order: its stored tiles in disk-ordinal
> order, then its tile-index region; then any record extents in
> ascending record order; then the directory. Records are ordered by
> type, and within type 0x0001 by layer name; a layer record's
> sub-records are ordered by type, and within a type by their encoded
> bytes compared lexicographically

"Records are ordered by type" gives a total order on the *top-level* sequence,
and a separate total order *within* each layer record's sub-record sequence. It
gives no order across the two. Concrete file: one layer `a` carrying a
user-metadata sub-record (extent 100 bytes) and one top-level user-metadata
record (extent 200 bytes). Both are type 0x0002. Profile writer A emits the
top-level extent then the sub-record extent; profile writer B emits the
sub-record extent with its layer, or orders the two by encoded bytes. Different
files, both following item 3. Item 3's own parenthetical concedes that
"record order carries no meaning (`[R-CNT-14]`), so it is otherwise free to
vary" — which is the freedom the item is there to remove.

*Gap 2 — the hash in item 2.* 

> **`file_id` from a cryptographic hash of the file's own emitted
> bytes**, computed over [0, F − 64) together with the trailer's
> other fields with the `file_id` field taken as zero, then written
> in. Deterministic, and high-entropy

No hash function is named, no reduction from the digest to 64 bits is specified,
no serialization order for "the trailer's other fields" is given, and no rule
covers the (2⁻⁶⁴) case where the result is 0, which `[R-CNT-06]` forbids. Two
profile writers choosing SHA-256-truncated-low and BLAKE3-truncated-high emit
different `file_id`s and therefore different files, from identical input. Item 1
handles the same problem honestly for codecs — "a named codec implementation at
a named version with fixed encoder settings … Byte-identity across
*implementations* is therefore unattainable for codecs 2–4" — and item 9 does
the same for JSON writers. Item 2 asserts "Deterministic" without the
corresponding pin.

**Byte-level: no.** Appendix G is non-normative and, by its own text, "adds no
requirement to any actor: a writer ignoring it is fully conforming". Every
ordering and every hash choice yields a conforming file. What is lost is the
appendix's claim to close the freedoms, and the closing paragraph's inventory
("Four things are not [already mandatory], and the items above are where the
profile adds them: gap *content* … gap *extent* … sub-record order within a
layer record's inline payload … and the fill a writer records") does not list
either gap.

---

### adversary-06 — OBSERVATION — Appendix H

**Appendix H's checklists never mention the front signature block — including
the verifier list, which purports to enumerate exactly the class the front-block
check falls into.**

Appendix H, conforming verifier:

> **Conforming verifier** — every reader obligation, plus the checks
> readers are exempt from: the live-state coverage partition and the
> slack total (§9.7) … extent overlap (§7.2); record flag bits …
> no structure between the live directory's end and the live trailer
> (`[R-CNT-05]`, F7); a reserved-range record or sub-record type value,
> whatever its MU bit …; alignment and slab invariants (§16);
> decoded-content obligations …; user-metadata member ordering …

Appendix H, conforming reader:

> **Conforming reader** — validates the trailer in §6.2's order; verifies
> each checksum before acting on what it covers (§4.5, §8.2) …

The front block is the only structure in the format checked by *equality*
rather than by checksum (§8.1: "Front signature block | none — checked by byte
equality (§6.1) | —"), and it is the only check a conforming reader is
conditionally exempt from — `[R-CNT-04]`: "A reader that would have to issue a
further range request to obtain those bytes MAY defer or omit the check." That
makes it, for a remote verifier, precisely one of "the checks readers are exempt
from", and it is absent from the list that names that class. It is likewise
absent from the conforming-reader and conforming-file entries, and from the
"verifies each checksum" clause, which by construction cannot reach it.

I traced whether the omission is load-bearing: it is not, because §2.3's
"including those ordinary readers are exempted from" and F6 both stand on their
own, and Appendix H disclaims itself ("each entry's authority is the requirement
or section cited, never this summary"). But the appendix is offered as an audit
aid, and an implementer auditing a remote verifier against it will not be
prompted to fetch bytes [0,16) — the one fetch §6.4's two-request accounting
deliberately excludes ("the two-request accounting of §6.4 does not include the
front block").

I also note, without making it a separate finding, that the reader entry's
"applies the outcome and scope §21 assigns" drops §2.3's qualifier "assigns to
the reader as its detector"; read literally it would have a reader reject-file
on F27 (unsorted user-metadata members), which `[R-MTA-05]` forbids ("readers
process the document unchanged"). It is harmless only because `[R-CNF-12]`
licenses a reader to reject any nonconforming file anyway.

**Byte-level: no.** A non-normative summary's omission changes no verdict; the
governing text (§2.3, F6, `[R-CNT-04]`) decides the obligation completely.

---

### adversary-07 — OBSERVATION — §21.6 (trailer-mimic row) and §22.3, `[R-SEC-04]`

**A defined-behavior row states its condition over a *payload* and its
justification over *slack*; the two are disjoint byte classes under §5.2.**

§21.6's row, quoted:

> | A payload contains a byte string that mimics a trailer | Inert: nothing
> enumerates slack, and a recovery tool re-verifies its output whole (§9.6) —
> which catches any mimic that is not itself a consistent generation; §9.6's
> second caution covers the rest | `[R-LIF-06]` |

A payload is a stored-tile extent: under §5.2 it is a *structure* of the live
committed state, explicitly not slack ("Every byte the live state does not claim
is **slack**"). "Nothing enumerates slack" is therefore not the reason a
payload-resident mimic is inert. The actual reason is `[R-LIF-05]`: "a reader
that finds no valid trailer in the final 64 bytes MUST report the file torn or
invalid and MUST NOT scan backward", so no reader ever looks at a mid-file
64-aligned offset for a trailer at all; and §6.2's note handles the one
placement a reader does look at ("A payload byte-string that mimics a trailer
and happens to sit at exact physical end of file … is caught at the directory
CRC").

§22.3's `[R-SEC-04]` makes the same slide in one paragraph, opening with the
payload case and closing on the slack case:

> And a payload can contain a byte string that mimics
> a trailer; recovery tooling that scans backward can land on one … Under live-state coverage a
> mimic in slack is inert — nothing enumerates it

**What an implementer does wrong without this:** nothing to a byte; but a reader
implementer looking for *why* a mid-file trailer mimic is safe is pointed at a
coverage argument that does not apply to the case named, and may conclude that a
mimic inside a live payload needs some check that §5.2 provides. It needs none,
for a different stated reason.

**Byte-level: no.** §21.6 is expressly not part of the register and carries no
rows (§21.1: "The subsections after §21.5 are not part of the register"), and
§21.1 adds "where such an entry and the rule it cites diverge, the rule governs
there too". `[R-LIF-05]` and `[R-LIF-06]` decide every file.

---

### adversary-08 — AMBIGUITY — §20.4's MU = 1 row vs §20.5, `[R-WRT-06]`

**§20.4 places "Compaction is barred on the same ground" at the end of its
*file-scope* sentence run, after having said that a layer-scope unknown critical
record leaves the rest of the file editable; `[R-WRT-06]` bars compaction for
*any* such record.**

§20.4's table, MU = 1 row, quoted whole:

> | MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the
> record governs. At layer scope an unknown critical record blocks modification
> of that layer, leaving other layers editable (`[R-CNT-18]`). At file scope no
> commit is available at all: the updater is a reader of the file first (§2.3),
> and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file —
> the same treatment §6.3 gives an unknown incompat-lane bit. Compaction is
> barred on the same ground (`[R-WRT-06]`). |

§20.5, `[R-WRT-06]`:

> A compactor MUST refuse to compact a file carrying any record
> whose type it does not implement with MU = 1: such a type can
> define references this specification does not (§7.2), so its
> bytes cannot be safely relocated.

The concrete file: layers A and B; B's layer record carries a sub-record of an
unimplemented experimental type with MU = 1 and a 4 KiB extent. Compactor A
reads §20.4 — layer-scope critical records "block modification of that layer,
leaving other layers editable", and "Compaction is barred on the same ground"
attaches to the *file-scope* sentence it immediately follows — and compacts,
relocating B's tiles, B's index region, and the unknown sub-record's extent, and
re-pointing every slot. Compactor B refuses.

**Which reading I pick.** Compactor B. `[R-WRT-06]` says "any record", and its
stated reason — such a type "can define references this specification does not
(§7.2), so its bytes cannot be safely relocated" — applies with full force to a
layer sub-record's extent, which is exactly what compaction relocates. §7.2
confirms that MU = 1 records are the ones permitted further references
("Records with MU = 1 carry further references only where this specification or
registry review (§10) defines them"). §20.4's row is a cross-reference and reads
its narrower scope only by proximity.

**What an implementer does wrong without this:** compactor A produces an output
whose unknown critical record's embedded references now point at the input's
byte positions. The output is *structurally* conforming — nothing in the format
can see inside that extent (§8.1: "Extent of a record of a type this
specification has not assigned | none — the bytes are opaque"), so no verifier
detects the breakage and §21.7's first paragraph applies: "this format detects
*corruption of structure*, not *incorrectness of content*." This is the one
attack I ran where a real tool could ship silent data loss.

**Byte-level: no — with a caveat I want on the record.** No file's verdict
changes: compactor A's output is conforming bytes under either reading, and
compactor B emits nothing. The fork is in which *tool* is conforming, and
`[R-WRT-06]`'s "any record" is categorical enough that a compactor implementer
working from §20.5 — the section that defines compaction — lands on B. I flag it
non-byte-level for that reason. The caveat: if one insists that "which byte
sequences a conforming implementation may emit" includes a compactor's output,
then reading (a) licenses an emission reading (b) forbids, and this is the one
finding in my list that could be argued the other way. I do not argue it, because
the sentence that decides it sits in the requirement a compactor author must
read.

---

## 4. Ranking the survivors

Nothing survived as a byte-level fork. Ranked by how plausible it is that a real
implementation lands on the wrong side:

1. **adversary-08** — a compactor author who works from §20.4's preservation
   table (the section that *is* about preservation) rather than §20.5 lands on
   the wrong side, and the damage is silent. Highest real-world risk of the
   eight, and the only one whose consequence is corrupted data rather than a
   wrong document.
2. **adversary-04** — a compactor that packs a slab-declared layer flat. Caught
   by a verifier, so noisy, but the reading is genuinely available in §20.5's
   own sentence.
3. **adversary-06** — an implementer auditing a remote verifier against
   Appendix H omits the front-block fetch. Produces a verifier that certifies a
   file with a corrupt reserved half-block.
4. **adversary-05** — two "reproducible" writers that are not. Confined to a
   non-normative profile.
5. **adversary-01** — a document-internal contradiction with no reachable
   behavioural consequence.
6. **adversary-03**, **adversary-07**, **adversary-02** — wrong or misplaced
   justifications for correct conclusions.

## 5. What I could not determine

- Whether §21.7's second paragraph ("A second set of obligations is omitted from
  the register because a single file exhibits no witness of their violation")
  is meant as an exhaustive list or as an account by class. It names
  `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s
  offsets clause and `[R-ENC-06]`, but not `[R-WRT-04]`'s "relocating a live
  index region is compaction's operation, not an appender's", nor
  `[R-LIF-02]`'s step ordering, nor `[R-WRT-05]`'s byte-identical re-emission —
  all of which are equally history properties with no single-file witness.
  §21.1 calls §21.7 "the account, **by class**, of what fails it", which I read
  as making the list illustrative, so I did not report it. If it is meant as an
  inventory, it is incomplete.
- Whether `[R-CNF-02]`'s "It is always conformance to a stated format major
  version" is meant to survive minor revisions that assign reserved enum values
  (§4.3's growth vehicle 2). Under this text a reserved sample type is a
  layer-scope violation (`[R-TYP-03]`, L34), so a file conforming under major 1
  / minor 7 is nonconforming under major 1 / minor 0's register. I could not
  turn this into a fork between two implementations of *this* text — both reject
  — so I left it out of the findings.
