# Cleanroom round 9 — Adversary transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,892 lines; the brief said 3,857, which I note only because it told me the
document had moved under me). I read it end to end in five `Read` calls, then
ran `grep` against that same file only.

I ran local Python that reads no project file: a CRC-32C implementation, a TARN
writer I wrote from the document, and a small parser over register-table rows
that I fed by `grep`ping the one permitted file. I wrote scratch files
(`crc.py`, `tarn.py`, `t1.py`, `t2.py`, `t3.py`, `count.py`, and four `.tarn`
attack files) into my own scratchpad and read those back.

I did not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `CONTRIBUTING.md`, `conformance/`, or `spec/registry.json`. I did
not run `git log`, `git diff`, or `git show`. I did not list any project
directory. I did not search the web. Where I used prior knowledge of other
formats (DEFLATE bit padding, zstd frame headers, IEEE 754 decimal conversion)
I used it only to *generate* suspicions and then settled each one against this
document's own text — except IEEE 754 and RFC 8878, which this document cites
normatively in Appendix F and which I therefore treated as incorporated.

---

## 0. Method

The charter asks for a file two conforming verifiers judge differently. Reading
§2.4 `[R-CNF-12]` first told me most of the obvious attacks are pre-absorbed:

> For a nonconforming file no acceptance obligation exists — a reader MAY
> reject it upon detecting any violation, including violations whose assigned
> detector is the verifier.

That single sentence kills every "reader A rejects the layer, reader B rejects
the file" divergence, because for any nonconforming file both are licensed. And
§2.3's three-verdict scheme (*conforming* / *nonconforming* / *cannot
establish*) absorbs every capability- and resource-grounded divergence.

So the only forks that survive are forks in the **file predicate itself**: a
byte sequence about which this document permits both "conforming" and
"nonconforming". I spent my effort there, and on the register, which is where
the file predicate is enumerated.

I therefore did three things:

1. Built a working writer from the document alone and reproduced Appendix A
   byte-for-byte, to establish that I was reading the layout correctly.
2. Re-derived every worked numeric example in the document.
3. Attacked the file predicate, section by section, with concrete byte
   layouts, weighted toward the sections the brief named.

---

## 1. Grounding: I implemented the container

I wrote CRC-32C from §4.5's parameters (Castagnoli 0x1EDC6F41, reflected in and
out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it against §4.5's own
check vector:

```
CRC32C("123456789") = 0xe3069283      §4.5 says 0xE3069283   ✓
CRC32C("")          = 0x00000000      §4.5 says 0x00000000   ✓
CRC32C(sentinel × 2^16) = 0xeecb3bb2  §15.4 says 0xEECB3BB2  ✓
```

The all-sentinel constant is the interesting one: it only comes out right if
you agree with me that a sentinel entry is `FF ×16 00 ×4` (§15.2) and that a
"full segment" is exactly 2¹⁶ × 20 = 1,310,720 bytes. It matched on the first
try, which is a good sign for §15.1/§15.2/§15.4 being mutually consistent.

Then I built Appendix A's file from scratch — front block, empty directory
(4 bytes: the CRC of zero bytes), 44 bytes of pad, trailer — and compared:

```
minimal file len 128, dir_offset 16, dir_length 4
matches Appendix A: True
trailer CRC over [0,60) = 0xe00938d2   Appendix A says D2 38 09 E0  ✓
```

So Appendix A is byte-correct, and §5.1's claim that 128 is the floor holds:
F ≡ 0 (mod 64) forces F ∈ {64, 128, …}; at F = 64 the trailer is [0,64) which
would have to carry the trailer magic where the front block's magic lives
(`89 54 …` ≠ `8A 4E …`, F10), and independently dir_offset ≥ 16 with
dir_length ≥ 4 gives a sum ≥ 20 against a bound of F − 64 = 0 (F12). Both
gates fire; 128 is right.

I then built a real layered file: one interleaved layer, 1-D with E = 2,
T = 1, one uint8 channel, codec 1, filter 1, tile 0 stored (`2A`), tile 1
sentinel. G = (2), N = 2, P = 1, Q = 1, decoded size 1, index region
2 × 20 + ⌈2/2¹⁶⌉ × 4 = 44 bytes — which `[R-CNT-17]`'s formula predicts
exactly. The file came out at F = 256:

```
89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00   front block
2a                                                 stored tile, [16,17)
ff×16 00×4  (entry 0 is actually 10 00 .. 01 00 .. b7 f5 22 19)
                                                   index region [17,61)
… layer record … dir CRC                           directory [61,162)
00 × 30                                            pre-trailer pad [162,192)
8a 4e 52 41 54 0d 0a 1a …                          trailer [192,256)
```

Nothing in §7.4's inline-payload table was ambiguous enough to stop me. The
packing order — name, layout, linearization, codec, filter, A, S, A_slab, d,
C, d dimension entries, C channel entries, index_encoding, entry_count,
crc_of_crc_array, sub-records — parses exactly, and `[R-CNT-18]`'s "no
alignment or padding between them" left nothing to guess. A reader can locate
`index_encoding` only by walking d and C variable-length entries first, which
is fine because d and C precede them.

**Where I had to guess:** nowhere in Part I's layout. That is a real result and
I want it on the record before the findings.

---

## 2. Every worked example re-derived

I recomputed all of them because a drifting example is the cheapest evidence of
a drifting rule. All agreed:

| Where | Claim | My computation |
|---|---|---|
| §11.2 | (1024,2048)/(256,256) → G=(4,8), N=32, P=65,536 | ✓ |
| §11.2 | E_y = 1000 → G_y = ⌈1000/256⌉ = 4 | ✓ (3.906→4) |
| §11.4 | (300,700) → tile (1,2), s = 10, u = (44,188), ordinal 11,452 | ✓ 44·256+188 |
| §11.4 | planar C=4, channel 2 at s=10 → disk ordinal 74 | ✓ 2·32+10 |
| §12.3 | `temp`/float32/NaN 0x7FC00000 → `04 74 65 6D 70 0C 00 04 00 00 C0 7F` | ✓ 12 bytes |
| §4.6 | `température` NFC = 12 bytes, NFD = 13 | ✓ 4+2+6 |
| §14.2 | T=(2,3), a:uint8 b:uint16 → Q=3, size 18, ordinal 5 at [15,18) | ✓ |
| §14.2 | same planar: b's tile 12 bytes, ordinal 5 at [10,12) | ✓ |
| §14.2 | t:float32 m:bool interleaved → Q=5, size 30, ordinal 5 at [25,30) | ✓ |
| §14.3 | T=(2,5), P=10, alternating → `55 01`; fill true → `55 FD` | ✓ pad bits 2–7 |
| §14.5 | E=(5,5) T=(4,4), tile (1,1): 1 real + 15 padding, 32 bytes | ✓ |
| §15.4 | entry_count 10⁶ → 16 segments, last 16,960; region 20,000,064 | ✓ |
| §15.4 | tile 999,999 at segment-relative 339,180; segment 15 = 339,200 B | ✓ |
| §15.4 | full segment 1.25 MiB | ✓ 65,536·20 |
| §15.4 | planar C=4 N=32: ordinal 74 at [1480,1500); ch-3 entries 96–127 | ✓ |
| §16.2 | N=32, S=8 → runs [0,8),[8,16),[16,24),[24,32) | ✓ |
| §17.3 | 1.0,2.0,3.0 float32 shuffled → `00 00 00 00 00 00 80 00 40 3F 40 40` | ✓ byte-for-byte |
| §20.3 | 32-tile index = 32·20 + 4 = 644 | ✓ |
| §21.9 note | 2³² tiles → 256 KiB CRC array; 2³⁶ → 4 MiB | ✓ |

The shuffle example was the one I most expected to be wrong (the offset formula
`i·n + j` inverts as `j·s + i`, which is easy to write backwards) and it is
exactly right.

I also mechanically counted the register:

```
F rows= 38 instances= 60
L rows= 50 instances= 103
T rows= 27 instances= 46
R rows= 10 instances= 44
TOTAL rows 125  TOTAL instances 253
```

§21.2 says 38, §21.3 says 50, §21.4 says 27, §21.5 says 10, §21.8 says
"125 conditions over 253 instances". The arithmetic is internally correct
under §21.1's "the count is therefore mechanical once the cell is written".
Whether the cells were *written* mechanically is finding **adversary-02**.

---

## 3. Attacks, in the order I tried them

### 3.1 Attack: the codec-1 sentinel — nearly the whole corpus, nonconforming

This is the attack I got most excited about and then had to give up.

`[R-COD-04]`:

> **Codec 1 — none.** The stored bytes are the filtered image verbatim. The
> index entry's length therefore MUST equal the tile's decoded size (§14.2,
> §14.3); a reader MUST treat a mismatch as a validity error at tile scope —
> checkable from the entry and the layer record alone, before any payload
> fetch.

§21.4 T24's neighbour, T14, restates it with no sentinel qualifier at all:

> | T14 | Codec 1 (none) declared and the index entry's length differs from the tile's decoded size | — | reader | tile use | `[R-COD-04]` |

A sentinel entry's `length` field is `FF FF FF FF FF FF FF FF` = 18,446,744,073,709,551,615.
That differs from every decoded size. So T14 read literally condemns **every
sparse layer that declares codec 1** — which is the most ordinary sparse layer
there is.

I built the file:

```
X2_codec1_sentinel.tarn — F = 256
layer "S": interleaved, lin 1, codec 1, filter 1, A=0 S=0 A_slab=0
           d=1, dim x: E=1 T=1  →  G=(1), N=1, P=1
           C=1, channel v: uint8, fill 00  →  Q=1, decoded size 1
           entry_count = 1, extent slot = (16, 24)
index region [16,40): ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 00 00 00 00
                      3d 9d 38 e5          ← the one-segment CRC array
```

Verdict A: reject-tile (T14, `[R-COD-04]`), file nonconforming.
Verdict B: valid sentinel, reads as fill (§15.3 row 1, `[R-TYP-08]`), file
conforming.

**Foreclosed, and I think decisively.** Three sentences do it, in this order:

- §19.4 step 4: "A valid sentinel short-circuits steps 5 and 6 for that entry."
  `[R-COD-04]` is checked "before any payload fetch", i.e. between steps 4 and
  5, and step 4 has already short-circuited past it.
- `[R-IDX-02]`: "Sentinel entries are a reserved pattern, **not offsets or
  lengths**" — so there is no "index entry's length" for `[R-COD-04]` to
  compare.
- `[R-COD-04]`'s own derivation: "The stored bytes are the filtered image
  verbatim. The index entry's length **therefore** MUST equal…". A sentinel
  addresses no stored bytes, so the premise the "therefore" rests on is absent.

Plus §21.1's tiebreak — "where a row and the rule it cites diverge, the rule
governs" — points at `[R-COD-04]`, which is the sentinel-silent one, so the
tiebreak alone would not have saved it. `[R-IDX-02]` is what saves it. I report
this as **adversary-03** because the row text as written reads on the sentinel
and the consequence of getting it wrong is disproportionate, but I do not
believe two competent implementations land on opposite sides of it.

### 3.2 Attack: the reader/verifier seam, made concrete

The charter asks for a file sitting exactly on the seam. I built one.

`X3_tile_in_pretrailer_gap.tarn`, F = 256:

```
front  [0,16)
index  [16,40)     one entry: offset 191, length 1, crc = CRC32C(2A)
dir    [40,141)    the layer record + CRC
pad    [141,191)   slack
TILE   [191,192)   the stored tile — ends exactly at F − 64 = 192
trailer[192,256)
```

The entry passes every §15.3 row: offset ≥ 16 ✓; length ≠ 0 ✓; neither field
is the sentinel ✓; neither exceeds 2⁶³−1 ✓; and

```
offset + length = 192 ;  F − 64 = 192 ;  192 > 192 is False
```

so the "extent would touch the live trailer or beyond" row does **not** fire —
§15.3 says `> F − 64`, and equality is in bounds. A conforming reader fetches
[191,192), verifies the crc, decodes under codec 1, and returns the sample.
It is obliged to detect nothing here.

A verifier must reject the file, at file scope, on `[R-CNT-05]`:

> Writers MUST place the directory so that no structure lies between its end
> and the trailer. … A verifier MUST treat a structure in that gap as a
> validity error at file scope

The directory ends at 141; the trailer begins at 192; the tile occupies
[191,192), which is inside that gap. F9.

This is the seam working as designed — the reader serves a sample from a file a
verifier calls nonconforming — and it is *not* a defect. I record it because it
demonstrates that §15.3's `>` and §6.2's gap rule have coincident boundaries
that a careless reading would have made disagree: if §15.3 had said `≥ F − 64`
the tile could never end where I put it, and if `[R-CNT-05]` had bounded the
pad by length rather than by "no structure", this file would be conforming.
Both boundaries are stated exactly once and they line up.

### 3.3 Attack: version_major stored big-endian — this one survives

§21.2 row F1:

> | F1 | A multi-byte field is stored big-endian rather than little-endian,
> detectable only through that field's own value or range gate | **trailer
> version_major**; dir_offset; dir_length; committed_file_length; generation |
> reader | open | `[R-ENC-01]` (R-CNT-07) |

I tried to build the vector this row demands — a file exhibiting the condition
whose expected verdict is §21.2's outcome, reject-file — and could not.

version_major is a `u16`. Little-endian 1 is `01 00`; the same value stored
big-endian is `00 01`, which the fixed little-endian parse reads as **256**.

```
X1_vmajor_bigendian.tarn — trailer:
8a 4e 52 41 54 0d 0a 1a  00 01  00 00  00 00 00 00 …  fe f6 4f 7d
                         ^^^^^ version_major field reads 256
trailer CRC verifies: True
```

There is no byte-swapped version_major that trips a *validity* gate. The field
has exactly one invalid value, 0, and `BE(0) == LE(0) == 00 00` — the byte swap
is unobservable at 0. Every other byte-swapped value reads as a nonzero major
this reader does not implement. I checked this exhaustively: it is a property
of the field having one and only one forbidden value, and that value being a
byte-swap fixed point.

And a nonzero major this reader does not implement is precisely what §2.3 and
§21.6 declare **not** to be a violation:

§2.3 `[R-CNF-02]`:

> This document defines format major 1, and a file declaring another major is
> neither conforming nor nonconforming under it: a reader refuses such a file
> on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding
> about its bytes.

§21.6, closing paragraph:

> Two structural cases are **conforming files a reader nevertheless refuses**.
> The first is **version_major naming a major this reader does not implement**:
> the reader rejects the file (`[R-CNT-07]`), but the file can be perfectly
> conforming under that major. … **Neither is a register row**: the register
> enumerates file-conformance violations (§21.1), and a file this document
> declines to judge is not one. What is registered in each case is the
> neighbouring condition that *is* a violation — version_major = 0, permanently
> invalid in every format major version (F20, `[R-CNT-07]`) …

So §21.6 says the only registered version_major condition is F20, and §21.2
registers a second one in F1's instance list. Two verifiers reading the same
64 bytes:

- Verifier A follows §2.3 + §21.6: version_major = 256, a major I do not
  implement, *cannot establish*, no finding about the bytes.
- Verifier B follows F1: a big-endian multi-byte field, `[R-ENC-01]` violated,
  **nonconforming**, reject-file at open.

§21.1's tiebreak does not settle this. It settles row-versus-rule; here the row
and the §21.6 entry cite the same rule, `[R-CNT-07]`, and the other rule F1
cites — `[R-ENC-01]`, "all multi-byte values … are little-endian" — has no byte
witness. A file carrying `00 01` at F−56 is byte-identical to a legitimate
format-major-256 file. §2.3 says conformance "is a pure predicate on bytes",
and no predicate on these bytes distinguishes the two.

The document even supplies the escape hatch that names this as a finding.
`[R-VEC-02]`:

> A vector whose expectation cannot be stated in those terms is testing
> something this specification has not defined, which makes it a finding
> against this document rather than a vector.

An F1/version_major vector must record "conforming: no; outcome reject-file;
row F1" for a file §2.3 says is *neither* conforming nor nonconforming.

I checked F1's other four instances and they are all fine — they are
constructible as genuine violations for at least some values:

| Instance | Byte-swapped value | Gate that fires |
|---|---|---|
| dir_offset = 16 | 0x1000000000000000 | F12 (sum > F−64) ✓ |
| dir_length = 4 | 0x0400000000000000 | F12 ✓ |
| committed_file_length | large | F19 / F15 ✓ |
| generation = 0x80 | 0x8000000000000000 | F3 (> 2⁶³−1) ✓ |

Note that `generation` only works for values whose low byte has bit 7 set —
a big-endian generation of 1 reads as 0x0100000000000000, which passes every
gate and leaves no witness at all. That is fine: the row says "detectable only
through that field's own value or range gate", which concedes that the vector
builder picks a value that trips. For version_major there is no such value.

This is **adversary-01**, and I flag it byte-level.

### 3.4 Attack: instance arithmetic on the flag rows

The brief warned that the dominant over-claim is a register row contradicting
its rule. This one is different: it is the register contradicting §21.1's own
counting rule, and it is not about verdicts at all — it is about how many
files the corpus owes.

§21.1:

> An instance names a field the condition ranges over, **a container it can
> occur in**, one of several alternatives the condition text states, or any
> combination of the three — a condition applying to two alternatives in two
> containers has four.

Now compare rows that share the identical phrase "A layer record's or
sub-record's":

```
L16 | …extent slot has exactly one of extent_offset and extent_length zero
    | layer record extent_offset; layer record extent_length;
      sub-record extent_offset; sub-record extent_length          → 4
L17 | …nonzero extent slot has extent_offset < 16
    | layer record extent slot; sub-record extent slot            → 2
L18 | …extent reaches the live trailer or beyond
    | layer record extent slot; sub-record extent slot            → 2
L47 | …flags carry MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0
    | —                                                           → 1
L48 | Any of a layer record's or sub-record's reserved flag bits 2-15 is set
    | flags bits 2-15                                             → 1
```

L16/L17/L18 count the layer-record/sub-record split as two containers. L47/L48
do not, and their condition text is drawn from the same template.

L50 splits the difference in the opposite direction from its file-scope twin:

```
F30 | A non-layer top-level record of a type §7.3 registers carries a stored
      MU or PE bit differing from the value the registry fixes
    | flags bit 0; flags bit 1                                    → 2
L50 | A layer record, or a sub-record of a type §7.3 registers, carries a
      stored MU or PE bit differing from the value the registry fixes
    | layer record flags; sub-record flags                         → 2
```

Identical condition. F30 treats "MU or PE" as two alternatives in one
container → 2. L50 treats it as one alternative in two containers → 2. Under
§21.1's stated rule ("two alternatives in two containers has four") L50 is 4.

L47 is arguably right at 1 *per container* — §21.1 says explicitly that "a
combination of two flag bits" is a single predicate whose fields are not
instances — but that gives 1 × 2 containers = 2, not 1.

Under the L16/L17/L18/F30 convention the totals are L47 = 2, L48 = 2, L50 = 4,
and §21.8's 253 becomes 257. Under the L47/L48 convention several of L16's four
collapse. §21.1's rule as written yields the first; the cells as written yield
neither consistently.

Nothing about any file's verdict changes. What changes is how many files the
corpus is obliged to contain under `[R-ERR-02]` and `[R-VEC-03]` — four
missing vectors, all of them verifier-detected flag-bit conditions on layer
sub-records, which is exactly the family least likely to be covered by
accident. This is **adversary-02**, not byte-level.

### 3.5 Attack: the ignored record's extent — does it claim bytes?

§2.4:

> | **ignore-record** | The record is skipped as though absent. Decoding of all
> stored data is unaffected. |

If the record is "absent", its extent claims nothing. Then:

- a verifier's slack total (a MUST-report under `[R-CNT-21]`) is larger by the
  extent's length; and
- an ignored record's extent overlapping a layer's stored tile is **not** an
  overlap, so F35 does not fire and the file is conforming.

I built the shape mentally rather than in bytes because the byte layout adds
nothing: a top-level record of experimental type 0x8001, MU = 0, PE = 0,
inline_length 0, extent slot (1000, 1000), in a file where layer A has a stored
tile at [1500, 1600). Verifier A: F35, reject-file, nonconforming. Verifier B:
the record is absent, no claimant, conforming.

**Foreclosed** by §5.2 `[R-CNT-02]`, which anticipates exactly this:

> Every byte of the live committed state belongs to exactly one of: the front
> signature block; or a **structure** — a stored-tile extent, a record extent
> (the bytes any record's extent slot references, **whatever the record's
> type**, §7.2), the directory, or the trailer.

"whatever the record's type" is the operative clause, and §9.7's walk
enumerates "each record's extent" without exception, and §8.1 gives an
unassigned type's extent its own map row ("none — the bytes are opaque"), and
§22.3 says such an extent is "carrie[d] … forward unread" by re-emission. Four
places agree that an ignored record's extent is live state.

I still report it — **adversary-05** — because §2.4's "skipped as though
absent" is the first sentence a verifier implementer reads when deciding what
the coverage walk enumerates, and the outcome-class table is where they will
look, not §5.2's parenthetical. Not byte-level: §5.2 decides it.

### 3.6 Attack: compaction over a corrupt user-metadata extent

Three rules converge and none of them names the outcome.

`[R-WRT-09]`: a compactor "MUST verify each link of the chain … and each
relocated extent's checksum … **before emitting that structure's bytes**".

§20.4: "For a type §7.3 registers, the registry's fixed flags govern rather
than the stored ones (`[R-CNT-22]`) — **both registered types carry PE = 1, so
neither can be dropped**".

`[R-CNT-20]`: a user-metadata extent's failed CRC is ignore-record — a
violation row (R2), so the input file is nonconforming.

So: the compactor must verify (it fails), must not drop (PE = 1), must not
re-encode into a corrected form (that would not be the byte-identical
re-emission `[R-WRT-05]` demands of a record it retains and does not logically
modify), and must emit only conforming files (`[R-CNF-05]`) — and any output
carrying that extent verbatim exhibits R2 and is nonconforming.

Refusing is the only surviving option, and it is licensed indirectly:
`[R-CNF-12]` lets a reader — and a compactor is a reader of everything it
carries, `[R-WRT-01]` — reject a nonconforming file on detecting any
violation. But nothing states it, and the reasoning to get there crosses five
requirements in four sections.

Not byte-level: the compactor that emits anyway is not a conforming writer, so
there is no divergence *among conforming implementations*. **adversary-04**,
an observation.

### 3.7 Attacks I tried and the sentence that foreclosed each

These are the ones that died cleanly. I list them because "empty is a real
result, but only if the attacks were good."

**A layer whose sample-position count P overflows in an empty layer.**
E = (0,), T = (2⁶²,2) → P = 2⁶³ > 2⁶³−1, N = 0. Does `[R-ENC-04]` reach a
quantity of a layer with no addressed tiles? §17.2's note answers explicitly:
"`[R-ENC-04]`'s overflow rule carries no such quantifier — it binds any sum or
product a file yields — so P·Q and P·Bᶜ are checked in an empty layer even
though this cap is not." Reject-layer. Foreclosed.

**A layer at the exact overflow boundary.** 2⁶³−1 = 7 × 1,317,624,576,693,539,401,
so d = 2 with T = (7, 1317624576693539401) gives P = 2⁶³−1 exactly, and
`[R-ENC-04]` says "exceed", so equality is in domain. With E = (1,1), N = 1,
entry_count = 1, index region 24 bytes, one uint8 channel and the single tile
sentinel, the whole file fits in a few hundred bytes and declares a tile of
decoded size 2⁶³−1 that is never stored. Conforming. A reader may decline the
layer under `[R-ERR-04]` because the decoded size exceeds §21.9's 256 MiB
guarantee, and reports it as a resource limit, not corruption. Both behaviours
licensed. Foreclosed by §21.9 + §2.3's *cannot establish*.

**lz4 on a layer that addresses no tiles.** `[R-COD-07]` caps decoded size at
0x7E000000 "for a layer any of whose addressed tiles' decoded size exceeds"
it. E = (0,), T = (2⁴⁰,) addresses none, so the cap is vacuous however large
the tile shape. §17.2's note states this outright and notes the escape is not
durable across a growth commit. Foreclosed.

**Duplicate-and-ill-formed layer names.** Two layer records whose name fields
are both `FF FF FF` (byte-identical, both ill-formed UTF-8). If UTF-8 is
checked first the outcome is two reject-layers and the file's other layers stay
servable; if uniqueness is checked first the outcome is reject-file and nothing
is servable. §19.1 step 4 forecloses it: "Uniqueness is decided first, and over
the raw name bytes whether or not each name is itself well-formed". Foreclosed
by a sentence that exists for exactly this.

**A long pre-trailer pad.** `[R-LIF-02]` step 5 pads "to the next 64-byte
boundary", so a 900-byte pad means the writer did not follow the protocol. Is
the file conforming? §6.2: "a longer gap is conforming, and no conforming
commit produces one." Foreclosed, explicitly.

**A second trailer, appended without a directory.** Take a valid generation-5
file, append 64 bytes (the old trailer becoming slack), pad, and a re-emitted
generation-5 trailer pointing at the *existing* directory. `[R-LIF-02]`'s note
says "A writer that re-points a new trailer at a prior generation's directory
region has left step 3 unperformed" — but the resulting bytes partition
correctly, the old trailer is superseded and therefore slack (§5.2), nothing is
in the gap that is a *structure*, and §21.7 puts the generation sequence in the
history class with no single-file witness. §6.2's "a longer gap is conforming"
settles it: conforming. Foreclosed, though it took me three passes to be sure.

**A trailer mimic in a stored tile.** §21.6 lists it as inert. I note in
passing that the row's condition says "A **payload** contains a byte string
that mimics a trailer" while its behaviour cell explains "nothing enumerates
**slack**" — a payload is a claimed structure, not slack. The conflation is
harmless (a reader looks only at [F−64, F), and §9.6's re-verification
requirement covers recovery tools either way), so I am not reporting it.

**A record extent inside the directory region.** Overlap → F35, verifier,
reject-file; the reader is explicitly not obliged ("readers are not obligated
to detect overlap, which requires whole-directory knowledge", `[R-CNT-13]`).
Designed seam, foreclosed.

**Big-endian everywhere else.** I walked F1's non-version_major instances,
F2's two signature instances (both constructible: reversed front magic
`1A 0A 0D 4E 52 41 54 89`, reversed trailer magic `1A 0A 0D 54 41 52 4E 8A`),
and F5/L3/T27's fixed-width-shift rows. All fine; the "records the cause
rather than a procedure of its own" framing is honest about what actually
fires.

**Reserved vs experimental in every position.** Record types (F37/F38 at file
scope, L25/L26 at layer scope, with §21.1's specialization note handling the
MU = 1 overlap), layouts (L37), linearizations (L34), sample types (L35),
codecs (L44), filters (L46), index encodings (L32), metadata encodings (R1 for
reserved, §21.6 for experimental). Every space is covered in every position it
can occupy, and the reserved/experimental asymmetry — reserved is a violation,
experimental is conforming-but-prohibited-conduct — is stated consistently in
§10.3, `[R-CNT-15]`, `[R-CNF-02]`, and §21.6. I found no gap.

**Flag-bit combinations.** MU/PE ∈ {00, 01, 10, 11} on registered types
(F30/L50), on unknown types (`[R-CNT-15]`, `[R-CNT-18]`, §20.4's table), and
the writer-prohibited 10 combination read as PE = 1 (`[R-CNT-12]`). Reserved
bits 2–15 (F28/L48). All assigned outcomes; the only defect I found is the
instance arithmetic of §3.4 above.

**The zero-length and degenerate family.** Zero records in a directory
(dir_length = 4, the minimal file) ✓; zero layers ✓; zero addressed tiles with
extent slot (0,0) and crc_of_crc_array = 0 ✓; zero-extent dimension ✓; a
24-byte experimental record with inline_length 0 and no extent ✓; a
zero-length structure — foreclosed everywhere (dir_length ≥ 4; extent slot
halves both zero or both nonzero; index length = 0 is T10; §17.2's note
establishes that no decoded size is below 1 byte, since P ≥ 1 and Q ≥ 1 and
⌈P/8⌉ ≥ 1).

**§8.1's coverage map completeness.** I checked every field of every structure
against the map and found exactly one checksum covering each, with the stated
exceptions. The chain trailer → directory → crc_of_crc_array → segment CRC
array → segment → entry → tile closes, and the pre-trailer pad, slack, and an
unassigned type's extent are the three uncovered regions, all three named.

**§18.2's number rule.** See adversary-06 below — the only place I found where
the *decision procedure* for a file's conformance is expensive rather than
ambiguous.

---

## 4. What I could not determine

Two things.

First, whether F1's `version_major` instance is an error in the cell or a
deliberate position that §21.6 then contradicts. I cannot tell from the
document which of the two was meant, only that they cannot both stand.

Second, whether §21.1's instance rule was intended to make the
layer-record/sub-record split a container. L16/L17/L18 say yes and L47/L48 say
no, and §21.1's text supports "yes" but its T24 "family" carve-out could be
stretched to support "no". I picked "yes" because L16 is the closest structural
analogue and because F30 already treats the MU/PE disjunction as two
alternatives.

## 5. Ranking of surviving attacks by plausibility

1. **adversary-01** (version_major byte-swap). High. A corpus builder hits it
   the moment they try to construct the vector `[R-VEC-03]` demands, and a
   verifier author hits it the moment they decide whether an unimplemented
   major is a nonconformity. The two answers are in adjacent sections of the
   same chapter.
2. **adversary-02** (instance arithmetic). High for a corpus builder, nil for a
   reader or verifier. It is a counting defect, not a semantic one.
3. **adversary-06** (binary64 finiteness). Low as a fork, moderate as a cost:
   any verifier that delegates to its host JSON parser inherits that parser's
   overflow behaviour rather than IEEE 754's.
4. **adversary-03** (T14 on sentinels). Low as a fork — three sentences
   foreclose it — but the blast radius if an implementation got it wrong is
   every sparse codec-1 layer in existence.
5. **adversary-05** (ignored record's extent). Low. §5.2's "whatever the
   record's type" is unambiguous once found.
6. **adversary-04** (compactor over a corrupt extent). Low. The reasoning
   converges on one answer; it is just never stated.

## 6. Files I produced

In my scratchpad, all built by a writer implemented from this document alone:

- `A_conforming.tarn` (256 B) — one layer, one stored tile, one sentinel
- `X1_vmajor_bigendian.tarn` (128 B) — adversary-01
- `X2_codec1_sentinel.tarn` (256 B) — adversary-03
- `X3_tile_in_pretrailer_gap.tarn` (256 B) — the reader/verifier seam, §3.2
