# Cleanroom round 12 — Adversary transcript

## Disclosure

I opened exactly one file with a read tool: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(four `Read` calls covering lines 1–3983, the whole document). I opened no ADR, no
`PLAN.md`, `AGENTS.md`, `README.md`, `OPEN-QUESTIONS.md`, no `conformance/` file, no
`spec/registry.json`, no charter, no findings from earlier rounds. I ran no `git`
command of any kind, no web search, no web fetch, and I did not list any directory to
see what else exists.

Everything else I ran was local computation over files **I** wrote, in
`…/scratchpad/round12/`: `crc.py`, `tarn.py` (an encoder I wrote from §4–§18 alone),
`build1.py`…`build5.py`, and one throwaway `python3 -` that parsed §21's register
tables out of `spec/tarn.md` to count rows and instances. The artifacts I produced are
`file1.tarn`, `file2_emptylayer.tarn`, `file3_alias.tarn`, `file4_expenc.tarn`,
`file5_badentry.tarn`. I used prior knowledge of DEFLATE/zstd/LZ4/CRC-32C only to
generate suspicions and to check the document's own worked numbers; every verdict below
is argued from quoted text in this document.

---

## 0. Method

The charter is constructive: build a file two conforming verifiers judge differently, or
say which sentence forecloses each attempt. So I built an encoder before I built any
attack, on the theory that the places where I had to guess while writing a *legal* file
are the places where an attack will land. I then went after (i) the document's own
arithmetic, (ii) boundary values, (iii) aliasing, (iv) the reader/verifier seam, (v) the
degenerate-but-legal file, and (vi) the two-features-that-interact cases.

I read the six sections the brief named first (front matter, §4.7, §9.7, §13.1, §20.3,
Appendix G) and then stopped treating them specially, because a small changed surface is
not a small defect surface. Three of my five findings are outside those six; two are
inside.

---

## 1. Checking the document's own numbers

Before trusting any construction of mine I reproduced every constant and every worked
example the document states. This is cheap and it calibrates how much of the rest to
trust.

CRC-32C (Castagnoli 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR
0xFFFFFFFF), implemented from §4.5's parameters alone:

```
CRC-32C("123456789") = 0xE3069283      §4.5 check vector          OK
CRC-32C(<zero bytes>) = 0x00000000     §4.5 check vector          OK
CRC-32C(2^16 sentinel entries) = 0xEECB3BB2   §15.4, App. B       OK
```

Appendix A's 128-byte file: I retyped the hex dump, sliced `[64,124)`, and got
`0xE00938D2` — the stored trailer CRC. The annotation table's field offsets all match
§6.2's layout. Appendix A is sound.

Worked examples re-derived by hand and by script:

| Where | Claim | Verdict |
|---|---|---|
| §11.2 | E=(1024,2048), T=(256,256) → G=(4,8), N=32, P=65536 | OK |
| §11.4 | (300,700) → tile (1,2), s=10, in-tile (44,188), ordinal 11452 | OK |
| §11.4 | planar C=4, channel 2 at s=10 → disk ordinal 74 | OK |
| §14.2 | T=(2,3), a:u8 b:u16 → Q=3, size 18, ordinal 5 at [15,18) | OK |
| §14.2 | t:f32 m:bool → Q=5, size 30, ordinal 5 at [25,30) | OK |
| §14.3 | T=(2,5), P=10, alternating → `55 01` (fill false), `55 FD` (fill true) | OK |
| §14.5 | E=(5,5) T=(4,4), edge tile (1,1): 1 real + 15 padding, 32 bytes | OK |
| §15.4 | entry_count=10^6 → 16 segments, array 64 B, region 20,000,064 B; k=999,999 in seg 15 at rel. byte 339,180; seg 15 = [19,660,800, 20,000,000) | OK |
| §15.4 | planar C=4 N=32: ordinal 74 at region [1480,1500); channel 3 = entries 96–127 | OK |
| §16.2 | N=32, S=8 → runs [0,8),[8,16),[16,24),[24,32) | OK |
| §17.3 | f32 1.0,2.0,3.0 shuffled at s=4,n=3 → `00 00 00 00 00 00 80 00 40 3F 40 40` | OK |
| §12.3 | channel entry `temp`/f32/NaN = `04 74 65 6D 70 0C 00 04 00 00 C0 7F` | OK |
| §4.6 | `température` NFC 12 bytes / NFD 13 bytes | OK |
| §20.3 | 32-tile index region = 32·20+4 = 644 | OK |
| §21.9 note | 2^32 tiles → 2^16 segments → 256 KiB array; 4 MiB at 2^36 | OK |
| §19.4 note | N ≥ 2^16 ⇒ per-channel entries in distinct segments | OK |
| §6.3 | major-1 trailer has zero slack: 8+2+2+4+8+8+8+8+8+4+4 = 64 | OK |
| §6.3 | a future major may redefine 48 bytes: 64−8−4−4 = 48 | OK |

§21's register arithmetic, counted mechanically by parsing the four tables and applying
§21.1's counting rule ("Instances within a cell are separated by semicolons, and a cell
reading — is one instance"):

```
rows: F=36, L=49, T=26, R=10  -> 121   (§21.2/3/4/5 headers say 36/49/26/10)
instances: F=53, L=106, T=45, R=44 -> 248
§21.8: "121 conditions over 248 instances"    MATCHES
```

Nothing wrong here. I record this because it means the cheap findings are already gone
and anything I find has to come from actually building.

---

## 2. Building a conforming file from the document alone

### 2.1 The minimal file

I rebuilt Appendix A's 128-byte file from §5.1, §6.1, §6.2, §7.1 without looking at the
appendix's hex, and got the same bytes. Front block `[0,16)`, directory `[16,20)` = the
CRC-32C of zero bytes, pad `[20,64)`, trailer `[64,128)`.

Sanity on the 128-byte floor of `[R-CNT-27]`: `dir_offset ≥ 16`, `dir_length ≥ 4`,
`dir_offset + dir_length ≤ F − 64`, `F mod 64 = 0`. The smallest F satisfying
`16 + 4 ≤ F − 64` with `F ≡ 0 (mod 64)` is 128. The floor is derivable, not asserted.

### 2.2 A real layer — `file1.tarn`, 448 bytes

§14.5's worked layer, fully built: rank 2, dims `(y,x)`, E=(5,5), T=(4,4), interleaved,
one `uint16` channel `v` with fill `0xABCD`, codec 1, filter 1, linearization 1, A=0,
S=0, A_slab=0.

```
G = (2,2)   N = 4   P = 16   Q = 2   decoded size = 32 bytes/tile
index region = 4·20 + ceil(4/2^16)·4 = 84 bytes
layer-record inline payload = 122 − 24 − 4 = ... (dir_length 122 total)

[0,16)     front signature block
[16,144)   four stored tiles, 32 B each, in disk-ordinal order
[144,228)  tile-index region (80 B of entries + 4 B segment-CRC array)
[228,350)  directory: one layer record (MU=1, PE=1) + 4-byte CRC
[350,384)  pre-trailer pad, 34 bytes  (350 -> next 64 boundary = 384)
[384,448)  trailer, generation 1, F = 448
```

I had to make exactly three judgement calls writing this, and all three are answered in
the text:

1. **Where may the directory sit?** `[R-CNT-05]`: "Writers MUST place the directory so
   that no structure lies between its end and the trailer." Combined with §9.2 steps 2–3
   this forces *every* structure into `[16, dir_offset)`. Not stated as a single
   sentence, but forced.
2. **How big is the pre-trailer pad?** `[R-LIF-02]` step 5, "pads to the next 64-byte
   boundary". §6.2 then says "a longer gap is conforming, and no conforming commit
   produces one" — so the pad length is a conduct property, not a bytes property. That
   sentence saved me from a finding; see §5.2 below.
3. **Edge-tile content.** `[R-SER-05]` fixes every padding position to the channel's
   recorded fill. Tile (1,1) covers coordinates 4–7 on both axes: one real position and
   fifteen `CD AB`. §14.5's example states exactly this.

### 2.3 The smallest file with a layer in it — `file2_emptylayer.tarn`, 192 bytes

`[R-GEO-02]` makes a zero-extent dimension valid, so the smallest layer-carrying file is
a layer with one dimension of extent 0:

```
layer inline payload = 73 bytes:
  01 'a' | 01 | 0100 | 0100 | 0100 | A=0(8) | S=0(8) | Aslab=0(8) | d=1 | C=1
  | 01 'd' E=0(8) T=1(8) | 01 'c' type=6(u8) filllen=1 fill=00
  | idx_enc=1 | entry_count=0(8) | crc_of_crc_array=0(4)
record = 24 + 73 = 97;  directory = 97 + 4 = 101 at [16,117)
pad [117,128) = 11 B;  trailer [128,192);  F = 192
```

Every cross-check lands: N = ∏⌈Eᵢ/Tᵢ⌉ = 0, so entry_count = 0, so `[R-CNT-17]`'s formula
gives extent_length 0, so the extent slot is `(0,0)` (which `[R-CNT-13]` says means "no
extent"), and `crc_of_crc_array = 0` per `[R-CNT-23]`. §15.4's closing example states
this exact configuration, and note that `0` is simultaneously the special-cased value
*and* the CRC-32C of the zero-byte array — the two readings coincide, so there is no
fork. That is a deliberate piece of design and it is worth saying so.

---

## 3. Attacks that failed, with the sentence that forecloses each

I ran these to concrete bytes or to a concrete field assignment. Each is listed with the
text that kills it.

### 3.1 Aliasing: an ignored record's extent over a stored tile — `file3_alias.tarn`

The strongest structural attack I found, and it fails. Build `file1.tarn` and add a
second top-level record:

```
type   = 0x8000   (experimental range, §10.2)
flags  = 0x0000   (MU = 0, PE = 0)
inline_length = 0
extent = (16, 32)  == the extent of layer "img"'s stored tile #0
```

§21.6 declares this record a *defined non-violation*: "A record type this specification
has not assigned, from the experimental range (≥ 0x8000, §10.2), carries MU = 0 |
Ignored, and preserved or dropped per its PE bit". And §2.4 says of **ignore-record**:
"The record is skipped as though absent."

The attack is: if the record is *absent*, its extent is not a claimant, so the coverage
walk sees no overlap and the file certifies — while a verifier that does claim it reports
F33. Two verdicts on one file.

Foreclosed by one clause in `[R-CNT-02]`, §5.2:

> "Every byte of the live committed state belongs to exactly one of: the front signature
> block; or a **structure** — a stored-tile extent, a record extent (the bytes any
> record's extent slot references, **whatever the record's type**, §7.2), the directory,
> or the trailer."

and by `[R-LIF-08]`, §9.7, which enumerates "each record's extent" without exclusion.
Two further sentences confirm the reading rather than merely permitting it: §20.4's
MU=0/PE=1 row obliges an updater to "Retain byte-identical, extent content unmodified",
and `[R-WRT-07]` obliges a compactor to relocate it — neither of which is coherent if the
extent is not a claimed structure. §2.4's "skipped as though absent" is scoped by its own
table heading as a *reader outcome*, and the coverage walk is a verifier check (§5.2's
closing note: "Coverage is checked by verifiers, never by readers").

Verdict: **foreclosed**, and cleanly. `file3_alias.tarn` is nonconforming under F33.

### 3.2 Sparse tile under a slab declaration, and a malformed entry inside a run

Declare S=4, A_slab=1 on a 4-tile interleaved layer; make ordinal 1 an entry with
`offset = S(all-ones), length = 100` (§15.3 row 3 — *structural*, reject-tile) and place
ordinal 2's tile immediately after ordinal 0's. A naive verifier reads offsets in ordinal
order, sees the run "broken", and reports L41 (reject-layer). A careful one does not.

Foreclosed verbatim by `[R-SLB-03]`, §16.2:

> "Sentinel tiles are transparent to run continuity: they occupy no bytes and do not
> break packing. So are the entries §15.3 classifies reject-tile on a *structural*
> ground: they address no usable extent, and the run's stored tiles close over them. An
> entry whose only defect is that its stored bytes fail its crc is not transparent — its
> offset and length stand, and the packing relation reads them as it does any other
> stored tile's — so this invariant stays decidable from index bytes alone."

L41's own Instances cell restates the same split. The complementary case — an entry that
fails *only* its stored bytes' crc, inside an aligned layer — is decided the same way by
§15.3's prose ("its extent stands and it keeps its place in the *verifier* rows, in run
continuity, and in the coverage walk"). This is the tightest-specified corner of the
document; I could not move it.

### 3.3 Structure hidden in the pre-trailer pad

Place a stored tile at `dir_offset + dir_length`, inside the pad. `[R-CNT-05]`: "A
verifier MUST treat a structure in that gap as a validity error at file scope", registered
as F7. Both verifiers reject. **Foreclosed.**

The neighbouring attack — an *oversized* pad (34 + 64 = 98 bytes, keeping F ≡ 0 mod 64)
with nothing in it — is explicitly declared conforming: "a longer gap is conforming, and
no conforming commit produces one." That sentence turns a `[R-LIF-02]` step-5 MUST into a
conduct rule, which `[R-CNF-02]`'s second sentence generalises ("A writer obligation
whose violation this specification expressly declares not to be a file-conformance
violation … binds the actor in the same way"). **Foreclosed.**

### 3.4 The sentinel against `[R-ENC-03]`'s value domain

Entry `(offset = 2^64−1, length = 2^64−1, crc = 5)` is not a sentinel (crc ≠ 0), so
§15.2's exemption ("`[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule apply to
the fields of non-sentinel entries only") withdraws, and the offset is out of domain. But
T11 excludes it — "the value being distinct from the all-ones sentinel" — so it is
recorded against §15.3's row 2 / T6 instead. Same outcome (reject-tile), same detector,
same tier. **Foreclosed**, and the T11 wording is doing real work here.

### 3.5 Degenerate geometry at the domain edge

`d = 1, E = 2^63−2, T = 2^63−1` gives `G = 1`, `N = 1`, `P = 2^63−1`, one uint8 channel
so `Q = 1` and `P·Q = 2^63−1` — no overflow, so `[R-ENC-04]` does not fire. entry_count 1,
one sentinel entry, index region 24 bytes. The layer is **conforming** and declares a
tile whose decoded size is 2^63−1 bytes. `[R-ERR-04]` handles it: the reader "MAY decline
it — at the whole file, or at the narrowest scope whose declarations exceed what it can
serve", reporting it "as a resource limit and not as a validity error". No fork.

Related: `A = 2^62` or `A_slab = 2^62` declared on a layer all of whose tiles are
sentinels is conforming — "A run with no stored tiles imposes nothing" (`[R-SLB-03]`) —
and becomes unsatisfiable the moment any tile is stored, because `offset < 16` is T8.
Decidable, no fork.

### 3.6 Codec 4 on a layer that addresses no tiles

`[R-COD-07]` caps decoded tile size at `0x7E000000` for lz4. An empty layer (E=0) declares
`T` freely, so the cap has nothing to quantify over. The §17.2 note answers this before I
could ask it: "The cap is quantified over the layer's *addressed* tiles, so a layer that
addresses none … satisfies it whatever its tile shape declares… `[R-ENC-04]`'s overflow
rule carries no such quantifier — it binds any sum or product a file yields — so P·Q and
P·Bᶜ are checked in an empty layer even though this cap is not." **Foreclosed**, and this
is the single most precisely-aimed sentence I hit all walk.

### 3.7 Codec/filter/layout combination attacks

- Byte-shuffle on a packed bool plane: `[R-COD-10]` sets `s = 1`, identity. Length
  divisibility (`L divisible by s`) holds in all three cases — planar numeric `P·Bᶜ / Bᶜ`,
  interleaved `P·Q / Q`, packed bool `⌈P/8⌉ / 1`. **Foreclosed.**
- Interleaved bool byte `0x02` at a *real* position → T2 (verifier); the same byte at a
  *padding* position → T4. T2's Instances cell states the split explicitly: "the same byte
  at a padding position is T4's, the two rows together covering `[R-SER-08]`". Neither is a
  reader obligation; `[R-SER-08]` fixes what a reader that returns it must report
  ("0x00 as false and every other byte as true"), so two readers cannot disagree about the
  value either. **Foreclosed** — and this is exactly the gap that would otherwise fork.
- zstd on a tile below 1 KiB: the §17.2 note derives that only a single-segment frame is
  encodable, "and no conforming file turns on which derivation a reader implements".
  **Foreclosed.**
- Metadata encoding 2's frame constraints: `[R-MTA-09]` enumerates precisely which of
  `[R-COD-06]`'s constraints carry over ("the frame magic; no skippable frame and no second
  frame; no nonzero dictionary ID; no content-checksum flag") and which do not (window
  size, content size). **Foreclosed.**

### 3.8 `1e400` in a user-metadata document

`[R-MTA-04]` says a reader "interprets every JSON number as an IEEE 754 binary64 value
**and MAY use a wider representation**", then says the document is unreadable if it holds
"a number whose **binary64 interpretation** is not finite". A reader using binary128 would
find `1e400` finite. But the *test* is pinned to binary64 regardless of the reader's
internal width, so both readers reach R8. **Foreclosed** — the pinning is deliberate and
it is the only thing preventing a fork here.

### 3.9 Register-completeness sweep

I walked every `[R-*]` identifier and asked whether its detectable violations have rows.
`[R-CNT-06]`'s thirteen field gates map onto F8–F19 with none missing; `[R-CNT-23]`'s
fifteen table constraints map onto L27–L36, L39, L43, L45, L30, L29 with none missing;
§4.5's "every field covered by exactly one checksum" holds against §8.1's map for the
entry crc (segment CRC), the segment CRC array (crc_of_crc_array), crc_of_crc_array (the
directory CRC), and the three terminal fields. §10.2's eight numeric spaces agree with
their defining sections and with Appendix C on every boundary. `[R-ERR-02]`'s completeness
claim survived everything I threw at it.

---

## 4. What did not survive

Five findings. Two are verdict-relevant, three are honest gaps that do not fork a
verifier.

---

### adversary-01 — AMBIGUITY — an appender authors a new index region containing an entry it is required to copy verbatim

**Location:** §20.3 `[R-WRT-04]` step 2 and step 4; §2.3 `[R-CNF-05]`, `[R-CNF-06]`;
§20.1 `[R-WRT-01]`; §20.4 `[R-WRT-05]`; §20.5 `[R-WRT-06]`.

**The construction.** `file5_badentry.tarn`, 448 bytes. It is `file1.tarn` with one
change: tile-index entry #2 is `offset = 80, length = 0, crc = 0x82CA39C9` — a
non-sentinel entry with length 0, which §15.3 row 4 classifies *structural*: reject-tile
(register row T10). Crucially **every checksum in the file verifies**: the segment CRC is
computed over the entry bytes as stored (`0x8C456440`), crc_of_crc_array matches, the
directory CRC matches, the trailer CRC matches. §21.7 guarantees such a file exists:
"Checksums are computed over what the writer wrote."

Now hand it to a conforming appender that wants to store a new tile in layer `img`.

- `[R-WRT-03]` fixes its verification depth: "the trailer and the full directory always …
  plus §19.3's layer validation for every layer whose record, index, or extents the commit
  modifies, and the §19.4 index chain for every segment whose entries the commit reuses".
  The index chain is §19.4 step 3 — crc_of_crc_array and the segment CRC — and both pass.
  §19.4 step 4 (entry classification, `[R-IDX-03]`) is not among what `[R-WRT-03]` obliges.
- `[R-WRT-04]` step 2: "The open establishes no tile-scope violation — it consumes the
  trailer and directory only … **and a malformed index entry an appender meets while
  re-emitting a region is carried forward byte-identically at its disk-ordinal position
  under step 4, not repaired to a sentinel.**"
- `[R-WRT-04]` step 4: "Every layer whose stored-tile set or index content this commit
  changes has its tile-index region re-emitted in full — entry_count entries plus the
  segment CRC array — necessarily at a new placement (`[R-LIF-01]`) … and every other
  entry byte-identical at its disk-ordinal position".

So the appender writes, at a fresh offset, an 84-byte region it composes itself: three
entries it computes and one it copies. The output file exhibits T10. It is nonconforming.

**The two permitted readings.**

*(a) Commit anyway.* §20.3 states the carry-forward as a positive requirement and pairs
it only with an advisory — "An appender that carries a violation forward SHOULD report
it" — never with a refusal. §20.5 states a refusal rule for compactors in so many words
("A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails, and MUST
NOT emit a file carrying a violation it has detected"), and states none for appenders,
which reads as a deliberate distinction between the two tiers. `[R-CNF-05]` is then read
as not reaching bytes re-emitted verbatim from the input, generalising §20.3's own
non-authorship principle.

*(b) Refuse the commit.* `[R-CNF-06]`: "An updater MUST satisfy every writer requirement
for the bytes it produces". The 84-byte region is bytes it produces — it is at a new
offset, three of its four entries are new, and its segment CRC is freshly computed. It is
not a re-emitted record, so `[R-WRT-05]`'s carve-out cannot reach it: §20.3 grounds the
carve-out precisely there, "re-emitting it byte-identically is not authorship, **since
`[R-WRT-05]` makes only *a record it modifies* new output under `[R-CNF-05]`**", and
`[R-WRT-05]` speaks only of records — "header, inline payload, and extent slot". Worse,
`[R-WRT-01]` explicitly bounds how far a latent violation may travel: "a violation latent
in a structure they **neither modify nor rely on** travels with it" — and this is a
structure the appender both modifies and relies on. Under (b) the appender must refuse,
on the §20.5 model.

**Which I picked, and why.** (a). §20.3's sentence is written as an instruction about what
the appender *does*, not about what it may do if it commits; and the asymmetry with
§20.5's explicit compactor refusal is too pointed to be accidental. But I had to weigh
three requirements against one sentence to get there, and I do not think the text
compels it.

**What an implementer does wrong without it.** Two conforming appenders handed
`file5_badentry.tarn` and the same "store this tile" request produce different bytes on
disk: implementation A writes generation 2 (a 500-odd-byte append carrying T10 forward),
implementation B writes nothing and errors. A pipeline that chains them diverges on the
first damaged file it meets. The narrower reading also has an operational cost the wider
one does not: under (b), one bad entry in a 10^6-tile layer permanently freezes that
layer against every future append, since no commit can ever re-emit its region — and
§20.4 forbids removing the layer record, so the only exit is a whole-file rewrite.

**Byte-level:** yes, on the "may emit" half of the test. Implementation A (reading §20.3
step 2 literally) emits a generation-2 file; implementation B (reading `[R-CNF-06]` +
`[R-WRT-01]`, on §20.5's precedent) emits nothing. The differing bytes are the whole
appended region — the new payload, the new 84-byte index region, the new directory, pad
and trailer. I record honestly that no *verifier* disagreement follows: both the input and
A's output are nonconforming, and both readings judge them identically. The fork is in
what a conforming updater may write, not in what a verifier decides.

---

### adversary-02 — AMBIGUITY — a conforming file whose user-metadata document no verifier can decode: certify, or *cannot establish*?

**Location:** §21.6 (row: experimental-range document encoding); §2.3 `[R-CNF-11]`;
§18.2 `[R-MTA-03]`, `[R-MTA-09]`; §21.7 `[R-ERR-01]`.

**The construction.** `file4_expenc.tarn` — 128 bytes, the *minimum* conforming size, and
here it is in full:

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00   front signature block
0010  00 01 02 03 04 05 06 07  3B BC 2C 8A               metadata extent [16,28):
                                                          8 opaque bytes + terminal CRC
001C  02 00 02 00 01 00 00 00  10 00 00 00 00 00 00 00   record: type 0x0002,
0024  0C 00 00 00 00 00 00 00  80                        flags MU=0 PE=1, inline_len 1,
                                                          extent (16,12), encoding = 0x80
0039  3E D6 2F AF                                        directory CRC   (dir = [28,57))
003D  00 00 00 00 00 00 00                               pad, 7 bytes
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00   trailer, gen 1
0050  01 00 …                  1C 00 …                   dir_offset = 28
0060  1D 00 …                  80 00 …                   dir_length = 29, F = 128
0070  A5 A5 A5 A5 A5 A5 A5 A5  00 00 00 00 74 B3 BB 69   file_id, reserved, CRC
```

Every gate passes: `F = 128` (a multiple of 64, ≥ 128), `dir_offset = 28 ≥ 16`,
`dir_length = 29 ≥ 4`, `28 + 29 = 57 ≤ F − 64 = 64`, generation 1, file_id ≠ 0, reserved
zero, trailer CRC verifies, directory CRC verifies. The record is type 0x0002 with the
flags §7.3 fixes (MU=0, PE=1), `inline_length` exactly 1 (`[R-MTA-03]`), extent slot
`(16,12)` — not `(0,0)`, `extent_length ≥ 5`, within `[16, F−64)` — and the extent's
terminal CRC verifies. Coverage partitions: `[0,16)` front, `[16,28)` the extent,
`[28,57)` the directory, `[64,128)` the trailer; slack = 7 bytes at `[57,64)`. Nothing
sits between the directory's end and the trailer.

The single interesting byte is at file offset 0x38: the encoding, `0x80` — the first value
of §10.2's experimental range for the metadata-encoding space.

§21.6 is unambiguous about the file:

> "A user-metadata record declares an experimental-range (≥ 0x80) document encoding |
> Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a writer's
> conduct, not the bytes"

and `[R-EXT-03]` agrees: "for the metadata-encoding space of §18.2, ignore-record under
the quarantine (`[R-CNT-25]`), never a scope-level rejection."

**The problem.** No conforming verifier can decode this document — §18.2 assigns no
semantics to 0x80, and "An encoding a reader does not implement is therefore one this
specification does not assign". So `[R-MTA-04]`'s content rules and `[R-MTA-05]`'s
member-ordering requirement — a MUST whose detector §21.3/§21.2 assign to the *verifier*
(F27, L48) — cannot be checked on this file. The document never says what that means.

**The two permitted readings.**

*(a) Certify.* There is no decoded document, so `[R-MTA-04]` and `[R-MTA-05]` have no
witness at all — the same position §21.7 takes about undetectable content: "no file-level
witness exists to check, so nothing about the file is left undetermined and the verdict
is unaffected." §21.6 says the file is conforming, and a verifier "certifies only
violation-free files"; there is no violation; certify.

*(b) Cannot establish.* §2.3 defines the third verdict as "where some requirement is one
it is unable to check on a **capability** … ground", and its list is introduced by "as
when", i.e. illustratively. `[R-MTA-05]` is a requirement about this record's document
that this verifier cannot check, because it does not implement the encoding — a
capability ground on its face. The verifier reports *cannot establish*, names
`[R-MTA-05]`, and "MUST NOT certify a file it reports that way."

**Why the text does not decide it.** The parallel cases are decided, in opposite
directions, and neither reaches this one:

- For codecs, `[R-COD-11]` decides explicitly: "A verifier that cannot execute a layer's
  codec or filter cannot establish that layer's conformance and MUST NOT certify the
  file." But §17.4 also notes that an *unassigned* codec value is a reject-layer violation,
  so the cannot-establish path there is only for assigned codecs.
- For metadata, `[R-MTA-09]` decides one and only one case: "A **verifier** that declines
  to decode a document on the bound above cannot establish that document's conformance and
  MUST NOT certify the file". "The bound above" is the size bound of §21.9's 16 MiB
  guarantee. It is not an unimplemented encoding.
- §2.3's own enumeration of cannot-establish grounds lists "when it declines to decode a
  user-metadata document (`[R-MTA-09]`)" — again only the size decline.

So the metadata space is the one space where an *unassigned* value leaves a **conforming**
file (the quarantine makes it ignore-record, not reject-layer), and that is precisely the
case that falls between `[R-COD-11]` and `[R-MTA-09]`.

**Which I picked:** (a), on §21.7's "no witness" reasoning — but §21.7's closing sentence
is scoped to §21.7's own list, and applying it here is my inference, not the document's.

**What an implementer does wrong without it.** Verifier A stamps `file4_expenc.tarn`
*conforming*. Verifier B reports *cannot establish* and refuses the stamp, naming
`[R-MTA-05]`. A certification pipeline that requires a *conforming* verdict passes the
file through one tool and blocks it at the other, and neither tool is wrong. The same
divergence reaches every file in the corpus that exercises §21.6's experimental-encoding
row, and `[R-VEC-02]` requires each vector's expectation to be recorded — which cannot be
done here without picking a side.

**Byte-level:** no. Both verifiers *accept* the file; neither reports nonconforming, and
`[R-EXT-03]` forecloses that. No byte a writer may emit changes. What changes is which of
the three §2.3 verdicts a verifier reports, and whether a certificate issues. I flag this
plainly rather than inflating it: it is a verdict divergence, not an accept/reject
divergence.

---

### adversary-03 — AMBIGUITY — Appendix G's `file_id` derivation names no hash, no truncation, and no serialization

**Location:** Appendix G, item 2 (and by contrast items 1 and 9).

**Quotation.**

> "2. **`file_id` from a cryptographic hash of the file's own emitted bytes**, computed
> over [0, F − 64) together with the trailer's other fields with the `file_id` field taken
> as zero, then written in. Deterministic, and high-entropy — satisfying §9.3's advice
> rather than contradicting it, which a counter would not."

**The problem.** The profile's whole purpose is stated two paragraphs above: "Applications
that need byte-identical output — content-addressed storage, reproducible builds — can
adopt this profile, which closes the degrees of freedom this format deliberately leaves
open." Item 2 does not close its degree of freedom. It leaves four things open:

1. **Which hash.** Item 1 knows how to pin a producer — "a named codec implementation at
   a named version with fixed encoder settings" — and item 9 repeats the technique — "a
   named JSON writer at a named version … by a named zstd implementation at a named
   version with fixed settings". Item 2 says only "a cryptographic hash". SHA-256 and
   BLAKE3 give different answers.
2. **How to reach 64 bits.** Every cryptographic hash worth the name is wider than 64
   bits. First eight bytes? Last eight? Folded by XOR? Not stated.
3. **Byte order of the result.** `file_id` is a `u64` (§6.2), so the eight selected bytes
   have to be read as an integer, and §4.1's little-endian rule governs the *field's*
   encoding, not which end of a digest becomes the low byte.
4. **What "together with the trailer's other fields" serialises to.** The trailer is 64
   bytes of which `file_id` occupies `[48,56)` and the CRC `[60,64)`; the CRC cannot be an
   input because it depends on `file_id`. "The trailer's other fields" is presumably
   `[0,48)` concatenated with `[56,60)`, or the 60-byte prefix with `[48,56)` zeroed — two
   different byte strings, two different digests.

There is also a small hard edge: nothing says what to do if the derived value is `0`,
which `[R-CNT-06]` and F12 make invalid. Measure-zero, but a profile that "can be refuted
cheaply but confirmed only by reproducing the file" is exactly the kind of thing that has
to say.

**Which I picked.** Writing `file4_expenc.tarn` I chose a fixed literal rather than a
derived id, because I could not implement item 2 as written. If forced I would take
SHA-256 over `bytes[0,48) || bytes[56,60)` of the trailer appended to `bytes[0, F−64)`,
first eight octets read little-endian, re-drawing on zero. Every one of those five
choices is mine.

**What an implementer does wrong without it.** Two build systems both declaring Appendix
G conformance, given identical logical input and identical codec settings, emit files that
differ in the eight bytes at `[F−16, F−8)` and therefore in the trailer CRC at `[F−4, F)`
— the exact failure the profile exists to prevent. Because the difference is in the
`file_id`, it also breaks the `(file_id, range)` cache contract of `[R-LIF-03]` across
the two builds' outputs, which are otherwise byte-identical files.

**Byte-level:** no. Appendix G is labelled non-normative and says of itself "It adds no
requirement to any actor: a writer ignoring it is fully conforming". Both writers emit
conforming files, and every verifier accepts both. The fork is inside the profile, not
inside the format.

---

### adversary-04 — OBSERVATION — `[R-CNT-13]`'s overlap scoping has no branch for two file-scope structures overlapping each other

**Location:** §7.2 `[R-CNT-13]`; §21.2 F33; §2.4 `[R-CNF-08]`; §21.1.

**Quotation.**

> "Extents are owned exactly once: within the live committed state … no two extent slots
> and no two structures overlap; a verifier MUST treat an intra-layer overlap — including
> a stored extent overlapping its own layer's index region or sub-record extents — as
> reject-layer, and any overlap **across layers or touching another scope's structures**
> as reject-file"

**The construction.** Two top-level records of type 0x8001 (experimental, MU=0, PE=0),
both carrying extent `(200, 40)`, in a file where nothing else claims `[200,240)`. Both
records are file-scope structures (§7.3 scopes only 0x0001 and 0x0002; `[R-CNT-13]` says
"the file for other top-level records"). The overlap is neither *intra-layer*, nor
*across layers*, nor *touching another scope's structures* — both belong to the same
scope, and that scope is not a layer. `[R-CNT-13]`'s two-branch enumeration assigns it no
outcome.

It is decidable anyway, by three steps: `[R-CNT-02]` makes it a violation ("a file whose
live state does not partition this way is not a conforming file"); `[R-CNF-07]` requires
every detectable violation to carry exactly one outcome; `[R-CNF-08]` maps file-scope
damage to reject-file. F33's *head* clause reaches it too — "claimed by two structures
that do not belong to the same layer" is true of two structures that belong to no layer —
though F33's own gloss enumerates only the same two branches the rule does. This is the
inverse of the usual §21.1 situation: here the row is broader than the rule it cites, and
§21.1 says "where a row and the rule it cites diverge, **the rule governs**", which points
away from the answer rather than toward it.

**Why it is an OBSERVATION rather than a fork.** The verdict is the same under every
reading a verifier can defend: the file is nonconforming. Only the outcome *class* is at
issue, and no reader obligation turns on it, because "readers are not obligated to detect
overlap, which requires whole-directory knowledge" and `[R-CNF-12]` lets a reader that
does detect it reject the whole file regardless. The cost is that deciding the outcome
takes a three-hop derivation through `[R-CNT-02]` → `[R-CNF-07]` → `[R-CNF-08]` while
§21.1 is actively pointing at the wrong text.

**Byte-level:** no. Every verifier reports nonconforming; every reader is exempt.

---

### adversary-05 — OBSERVATION — Appendix G's emission order is not total over top-level records of one unregistered type

**Location:** Appendix G, item 3.

**Quotation.**

> "That order runs over top-level records first, then, within each layer record, its
> sub-records. **Records are ordered by type, and within type 0x0001 by layer name; a
> layer record's sub-records are ordered by type, and within a type by their encoded bytes
> compared lexicographically** — an order a reader can derive, which a creation order is
> not"

**The problem.** The lexicographic within-type tiebreak is supplied for *sub-records* and
withheld for *top-level* records, where the only within-type rule given is "within type
0x0001 by layer name". `[R-CNT-14]` permits "any number of layer records", at most one
top-level user-metadata record, and states no multiplicity rule at all for unassigned
types — so any number of top-level records of one unregistered type is permitted. Two such
records are unordered by item 3, and since item 3 also fixes where their extents go
("then any record extents in ascending record order"), the ambiguity reaches the byte
layout, not just the directory.

**Scope of the damage.** Narrow. §10.3 bars experimental values from "released software or
published data" and bars reserved values outright, so a *creator* following the profile in
released software can only emit types 0x0001 (ordered by unique layer name) and 0x0002 (at
most one) — for which item 3 is total. The gap bites only private/experimental use, which
is also the only place the profile's byte-identity claim would be exercised against an
unregistered type. It is nonetheless a hole in a clause whose sentence is precisely about
supplying "an order a reader can derive".

**Which I picked.** Extend the sub-record rule: within a type, order by the records'
encoded bytes compared lexicographically. That is the obvious repair and it costs nothing.

**Byte-level:** no. Appendix G is non-normative and both orderings yield conforming files.

---

## 5. Things I deliberately did not report

Recording these so the next round does not re-derive them.

- **§4.7 "In format major 1 `version_minor` is the only descriptive field."** `tarn.stats`
  (§18.4, `[R-MTA-08]`) reads like a descriptive field on §4.7's own definition — its value
  determines nothing a reader does, and its definition states what a reader does when it
  contradicts the data it describes ("MAY be stale after any commit that changes the layer,
  and a reader MUST NOT use it to skip reading data … nor to decide any question of
  correctness"). But this document uses "field" throughout for fields of on-disk
  structures with offsets and widths, and §18.4 registers *keys* inside a document whose
  meaning `[R-MTA-01]` explicitly declines to define. I judge the sweep sound and the
  apparent collision a terminology coincidence.
- **§20.5's compactor version_minor rule** is stated declaratively ("carries the greater of
  `[R-CNT-26]`'s floor and the input's version_minor") where `[R-CNT-26]` states a SHOULD
  for appenders. A stricter rule for one tier is not a contradiction, and no verifier can
  observe either — minors never gate.
- **§6.2's note that a trailer-mimicking payload "is caught at the directory CRC"** is only
  true against accidental collisions; §22.3 and §22.5 already say an adversary recomputes
  checksums, and no conforming file can place a payload at `[F−64, F)` in any case
  (`[R-CNT-13]`, T9). Non-normative note, correct in its intent.
- **§11.2's ceiling-division warning is not repeated at `[R-CNT-17]`**, whose
  `⌈entry_count / 2^16⌉` invites the same `(x + 65535) >> 16` overflow at large
  entry_count. But the *defined* quantity is the whole region-size expression, which L2
  covers, and §11.2's note is general. Not a defect.
- **Overlapping identical extent slots on two layer records** (two layers sharing one
  tile-index region): F33, reject-file. Decided.
- **A layer record with stored flags MU=0/PE=0** fires both L46 and L49 with the same
  outcome, detector and tier; `[R-VEC-02]` already covers multi-row files ("the entry
  records every row the file exercises and says which it was built for").
