# Cleanroom round 16 — Adversary transcript

## Disclosure

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read end to end (4,282 lines) in five `Read` calls. I ran `grep` and `wc` against
that file and nothing else. I wrote and ran five Python scripts of my own in the
scratchpad (`crc.py`, `mini.py`, `build.py`, `build2.py`, `build3.py`, `read.py`)
and read back only files those scripts created (`file3.tarn`, `file4.tarn`,
`file7.tarn`, `appA.tarn`). I did not open `docs/`, `PLAN.md`, `AGENTS.md`,
`README.md`, `OPEN-QUESTIONS.md`, `conformance/`, `spec/registry.json`, any ADR,
any prior round's findings, or the round-16 output directory. I ran no `git`
command, no web search, no web fetch. I did not list any directory except to
`mkdir -p` my own scratch path.

I used prior knowledge of other array/image formats only to *generate*
suspicions; every suspicion was settled against this document's text.

## Method

I read the whole document first, then did three things:

1. **Built a writer.** Emitted three complete TARN files from the field tables
   alone — the 128-byte minimal file, a one-layer file with four stored tiles
   under codec 1 / filter 2 with edge padding, and a file carrying a top-level
   user-metadata record plus a zero-extent layer.
2. **Built a verifier.** An independent parser implementing the open algorithm
   (§19.1), the trailer gates (§6.2), the record walk (§7.2), the layer-record
   parse (§7.4), the geometry (§11), the index chain (§15.4), entry
   classification (§15.3), the byte-shuffle inverse (§17.3), codec 1, the
   padding-content check (§14.5), the coverage walk with overlap detection and
   slack total (§9.7). It reproduces every verdict the document asks for on the
   files above.
3. **Attacked.** Boundary values, zero-length structures, aliasing, the
   reader/verifier seam, every reserved/experimental value in every position,
   feature interactions, and the degenerate-but-legal file.

Where I could not test something (deflate/zstd/lz4 bitstreams, the JSON
document's full rule set) I read the rules and reasoned; I say so below.

---

## Part 1 — What I built, and whether the document sufficed

### 1.1 The checksum

§4.5 fixes CRC-32C by polynomial, reflection, init, final XOR and storage order,
and gives a check vector. I implemented it and got:

```
CRC-32C("123456789") = 0xE3069283   (§4.5 says 0xE3069283)   ✓
CRC-32C(zero bytes)  = 0x00000000   (§4.5 says 0x00000000)   ✓
```

Every other constant the document states, recomputed from that implementation:

```
CRC-32C of 4 sentinel entries (80 bytes) = 0x80A34955   (§7.4 example)  ✓
crc_of_crc_array over `55 49 A3 80`      = 0xC4EE982E   (§7.4 example)  ✓
CRC-32C of 2^16 sentinel entries         = 0xEECB3BB2   (§15.4, App. B) ✓
Appendix A trailer CRC over bytes [0,60) = 0xE00938D2   (App. A)        ✓
```

All four match. This is the strongest single signal in the document: the
sentinel constant, the segment constant and the appendix's trailer CRC were all
reproducible from §4.5's parameters with no guessing.

### 1.2 The minimal file (§5.1, Appendix A)

I derived the 128-byte floor independently before reading Appendix A: front block
[0,16); dir_offset ≥ 16 and dir_length ≥ 4 put the directory's end at ≥ 20;
`dir_offset + dir_length ≤ F − 64` gives F ≥ 84; F mod 64 = 0 gives F ≥ 128.
That is exactly `[R-CNT-27]`'s reasoning. Appendix A's 128 bytes then parse
cleanly under my verifier: trailer CRC matches, directory region is four bytes
holding CRC-32C(∅) = 0, record sequence is empty, coverage partitions as
front(16) + directory(4) + trailer(64) with 44 bytes of slack.

Nothing here needed a guess.

### 1.3 The §7.4 worked layer-record payload

I built the 81-byte inline payload for the `sst` example *from the field table
only* — name, layout, linearization, codec, filter, A, S, A_slab, rank, C, one
dimension entry, one channel entry, index_encoding, entry_count,
crc_of_crc_array — and compared it byte for byte against the hex dump in §7.4.

```
7.4 payload len 81 (doc says 81)
matches doc hex dump: True
```

Every offset in the dump's left column is reproduced by packing the table in
order with no padding. The arithmetic sentence under the dump ("4 + 34 bytes …
the dimension entry 18, the channel entry 12, and the trailing fixed fields 13 —
81 exactly") is correct: 1+2+2+2+8+8+8+1+2 = 34 for the nine scalars.
`[R-CNT-17]`'s extent length 4·20 + ⌈4/2^16⌉·4 = 84 is correct.

This example is doing real work. Without it I would have had to guess whether
`linearization` precedes `codec` and whether the fill length prefix precedes the
fill bytes; the table order plus the dump settles both.

### 1.4 A file with real tiles, padding and a filter

Layer `p`: rank 2, dims `y` (E=5, T=4) and `x` (E=5, T=4); interleaved; one
`uint16` channel `v` with fill `0xABCD`; codec 1, filter 2, linearization 1.

Derived: G = (2,2), N = 4, P = 16, Q = 2, decoded size = P·Q = 32 bytes.
Tile at spatial ordinal 3 = tile coords (1,1) covers y,x ∈ [4,8): one real
position (4,4) and fifteen padding positions. That is §14.5's worked example,
and my independently built tile agrees with it: value 0 is the sample, values
1–15 are `CD AB`.

Filter 2 with s = Q = 2 and n = 16 gives, for that tile:

```
2C CD CD CD CD CD CD CD CD CD CD CD CD CD CD CD 00 AB AB AB AB AB AB AB AB AB AB AB AB AB AB AB
```

— all group-byte-0 first, then all group-byte-1, exactly as §17.3 states. I
verified the inverse restores the image, and I verified §17.3's own float32
example (`00 00 00 00 00 00 80 00 40 3F 40 40`) independently: correct.

Full file layout, all placement free under `[R-SLB-05]`:

```
front [0,16) | tiles [16,144) | index [144,228) | dir [228,348) | pad [348,384) | trailer [384,448)
F = 448 (448 mod 64 = 0), slack = 36
```

My verifier's output:

```
claimants: front(0,16) tile#0(16,48) tile#1(48,80) tile#2(80,112) tile#3(112,144)
           index:p(144,228) directory(228,348) trailer(384,448)
slack total = 36
ERRORS: none — file certifies
```

Every check in §19.1–§19.4 and §9.7 is decidable from the document. The one
place I paused was **which channel a planar disk ordinal belongs to**: §11.4
gives the forward map `c·N + s` but never states the inverse. `c = k div N`,
`s = k mod N` is forced (0 ≤ s < N), so this is not a guess so much as an
inversion the reader has to perform silently; it matters because §14.2's decoded
size and §17.3's shuffle stride both depend on `c`. I would have preferred one
sentence, but the text is not ambiguous.

### 1.5 A file with user metadata and a zero-extent layer

Top-level user-metadata record, encoding 1, document
`{"tarn.creator":"cleanroom16","tarn.title":"probe"}` (members ascending by
UTF-8 bytes, `[R-MTA-05]`), extent = document + terminal CRC-32C. Plus a layer
`L` with one dimension of extent 0, so G = 0, N = 0, entry_count = 0, extent
slot (0,0), crc_of_crc_array = 0. Both certify.

The zero-extent layer is the cleanest degenerate case in the format and it is
fully decided: `[R-GEO-02]` for validity, `[R-CNT-17]` for the extent-length
formula at 0, `[R-CNT-23]` for the forced crc_of_crc_array, §15.4's example for
"nothing is fetched and nothing is verified", §19.4 step 1 for the read
behaviour, and §17.2's Note for how the lz4 cap and `[R-ENC-04]`'s overflow rule
diverge over it. That last is a genuinely well-closed boundary — see 2.9.

### 1.6 Register arithmetic

§21.8 states "121 conditions over 275 instances" as a normative coverage
obligation. I extracted every register row's Instances cell and applied §21.1's
own counting rule ("Instances within a cell are separated by semicolons, and a
cell reading — is one instance"):

```
F: 36 rows,  58 instances
L: 49 rows, 116 instances
T: 26 rows,  57 instances
R: 10 rows,  44 instances
    121 rows, 275 instances
```

Both figures are exactly right, and the per-subsection row counts stated in
§21.2 (36), §21.3 (49), §21.4 (26) and §21.5 (10) are right too. Whatever the
instance criterion's problems (adversary-03), the arithmetic over it is sound.

---

## Part 2 — Attacks, and the sentence that forecloses each

Ordered roughly by how close each came.

### 2.1 A structure in the pre-trailer gap (F7)

**Construction.** File 4 rebuilt with the user-metadata extent moved to offset
200; directory ends at 197; trailer at 256. So a record extent occupies bytes
between the live directory's end and the live trailer.

**Two verdicts?** A *reader* serves this file without complaint —
`[R-CNT-05]` says so in terms: "readers check neither, their check being the
dir-bounds rule of `[R-CNT-06]`". A *verifier* must reject-file (F7). But that
is a reader/verifier asymmetry the document licenses, not two verifiers
disagreeing.

**Foreclosed by** `[R-CNT-05]`: "A verifier MUST treat a structure in that gap as
a validity error at file scope, and counts the rest as slack."

I also checked the neighbouring trap — a *longer-than-necessary* pre-trailer
gap with nothing in it. `[R-CNT-05]`: "a longer gap is conforming, and no
conforming commit produces one", and §2.3 names "§6.2's pre-trailer gap longer
than `[R-LIF-02]` step 5's pad" as one of the two cases where a writer
obligation binds conduct and not bytes. Both verifiers certify. Closed.

### 2.2 A tile-index region that overlaps the directory region

**Construction.** Point a layer record's extent slot at 84 bytes *inside* the
directory's own record sequence, arranging those bytes to be four sentinel
entries plus their segment CRC (a layer record's inline payload can be made to
contain them). Now the directory CRC verifies, the record sequence parses with
no residue, crc_of_crc_array and the segment CRC verify, and a reader serves the
layer normally — it never needs whole-directory knowledge.

**Two verdicts?** Reader accepts, verifier rejects. Again the licensed
asymmetry, not a verifier fork: `[R-CNT-13]` classifies "any overlap across
layers or touching another scope's structures as reject-file" (F33 instance
"directory region"), and both verifiers land there.

**Foreclosed by** `[R-CNT-13]`'s parenthetical: "(readers are not obligated to
detect overlap, which requires whole-directory knowledge)".

### 2.3 A trailer that points at a *previous* generation's directory

**Construction.** Take a valid generation-n file; append a pad and a trailer with
generation n+1 whose `dir_offset` still points at dir_n. Every gate passes: the
magic, the trailer CRC, the version gate, F, the dir bounds, the directory CRC,
the record walk. Coverage partitions — the superseded trailer_n and pad are
slack, not structures (§5.2: "everything an earlier commit superseded").

**Two verdicts?** No — both verifiers certify. §9.2's Note says the writer "has
left step 3 unperformed", but nothing in the live state witnesses which commit
wrote the directory bytes.

**Foreclosed by** `[R-CNF-02]` ("File conformance is a pure predicate on bytes")
together with §9.7's Note: "Nothing here enumerates prior commits." I record
below (2.11) that §21.7's list of witness-free obligations does not name this
one; that is an accounting question, not a fork.

### 2.4 Every reserved and experimental value in every position it may occupy

I walked §10.2's eight identifier spaces against the register and §21.6:

| space | reserved value | experimental value |
|---|---|---|
| record type (top level) | violation F36; +F35 if MU=1 | **conforming**; ignored if MU=0, reject-file if MU=1 |
| record type (sub-record) | violation L25; +L24 if MU=1 | **conforming**; ignored if MU=0, reject-layer if MU=1 |
| channel layout | L36 | (no experimental range) |
| linearization | L33 | L33 |
| sample type | L34 | L34 |
| codec | L43 | L43 |
| filter | L45 | L45 |
| index encoding | L31 | L31 |
| metadata encoding | violation R1 (ignore-record) | **conforming** (§21.6), ignore-record |

The two spaces where an experimental value is conforming (record type, metadata
encoding) and the six where it is a validity error are exactly the split §10.3
draws: "A reader encountering either treats it as its space's rules require: a
validity error at the owning scope for the value sets of §11.4, §12.2, §14.1,
§15.1, §17.2, and §17.3; for record types, the MU-bit outcome of `[R-CNT-15]` at
file scope and `[R-CNT-18]` for layer sub-records; and for the
metadata-encoding space of §18.2, ignore-record under the quarantine". No gap.

**Near miss worth recording.** §18.2's layout table gives the encoding field's
Valid values as "1 or 2; see below", and §4.7 calls that column the field's
"valid range". Read alone, that cell would make an experimental encoding
(≥ 0x80) an out-of-range structural field — which §21.6 says is *conforming*.
I convinced myself this is foreclosed, four times over: the cell's own "see
below"; `[R-MTA-03]`'s full value set immediately under it; §21.5's preamble,
which says every row there is a violation "except at an experimental-range
encoding, where no document rule attaches and §21.6 records the defined
non-violation"; R1's Instances cell, which deliberately lists only "encoding 0"
and "reserved 3–0x7F"; and §10.3's routing quoted above. No verifier that reads
past the table reaches a different verdict. Closed — but it is the one place
where a layout table's range column and the register disagree on its face.

### 2.5 Every combination of the record flag bits, in every position

- MU=1/PE=0 on an unknown type: read as PE=1 (`[R-CNT-12]`), verifier-detected
  (F25/L46). Both verifiers reject.
- Reserved flag bits 2–15 set: writers must zero, readers must ignore,
  verifier-detected (F26/L47). Reader behaviour unchanged, so no reader fork.
- A *registered* type carrying wrong stored flags (a layer record with PE=0, a
  user-metadata record with MU=1): `[R-CNT-22]` — readers apply the fixed
  semantics regardless, verifier records F28/L49.
- Experimental type + MU=1 at file scope: the file is conforming, every reader
  must reject it, and a verifier that does not implement the type reports
  *cannot establish* (§2.3). Two verifiers *can* differ here — one implementing
  the type certifies, one not implementing it cannot — but that is a capability
  difference the document constructs deliberately, and *cannot establish* is
  expressly "not a finding that the file is nonconforming".

**Foreclosed by** §21.6's closing paragraphs, which name both structural cases of
"conforming files a reader nevertheless refuses" and say why neither is a
register row.

### 2.6 The tile-index entry state space (§15.3)

I enumerated the corner entries and checked that exactly one outcome results:

| offset | length | crc | classification |
|---|---|---|---|
| S | S | 0 | valid sentinel |
| S | S | ≠0 | structural reject-tile (T6). T11 excluded by its own text ("distinct from the all-ones sentinel") |
| S | 5 | 0 | structural reject-tile (T7). T11 again excluded for the offset |
| 2^63 | S | 0 | T7 *and* T11 — both reject-tile, §24 licenses multi-row vectors |
| 1000 | 0 | 0 | structural reject-tile (T10), even though CRC-32C(∅)=0 "verifies" |
| 10 | 2 | x | T8 — extent lies wholly inside the front block, offset < 16 catches it |
| o | l | x with o+l = F−64 | legal; the bound is strict ("> F − 64") |

The `S/S/≠0` versus `T11` interaction is the sharpest edge in the table and it is
closed by T11's own parenthetical. The zero-length entry with crc 0 is the one
that could have slipped past a compactor (see 2.7).

### 2.7 A compactor over a structurally-invalid index entry

**Construction.** A layer with a non-sentinel entry whose offset is in range and
whose length is 0, with crc field 0 — so the "extent's checksum" a compactor is
told to verify (`[R-WRT-09]`) trivially passes, because CRC-32C of zero bytes is
0.

**Why this looked live.** `[R-WRT-07]` asserts "an entry §15.3 classifies
reject-tile on a structural ground never reaches this step, `[R-WRT-06]` having
obliged the compactor to refuse", and `[R-WRT-06]`'s *first* clause is about
"any check `[R-WRT-09]` obliges". `[R-WRT-09]`'s enumeration — the open, the
layer record, the index chain, each relocated extent's checksum — does not
mention `[R-IDX-03]`'s entry classification, and for length 0 the checksum check
does not fail.

**Foreclosed by** `[R-WRT-06]`'s *second* clause — "and MUST NOT emit a file
carrying a violation it has detected" — combined with §2.3 ("Verifiers and
updaters are readers of the files they process and inherit every reader
obligation") and `[R-CNF-04]` (a reader MUST detect every register row whose
detector is the reader; T10's detector is the reader). The compactor relies
structurally on every structure it copies (§20.5), so it reaches T10 and must
refuse. The chain holds, but it holds through three rules rather than the one
`[R-WRT-07]` cites.

### 2.8 A slab-declared layer under compaction

**Construction.** Input declares S = 8, A_slab = 4096. A compactor relocates
every tile. `[R-SLB-04]` says a writer changing "the byte placement of any run"
must "re-establish the invariants for every such run — or clear the declaration
in the new generation" — but `[R-WRT-07]` lets a compactor change only extent
slots, index regions and crc_of_crc_array, never the slab fields. So the escape
hatch ("clear the declaration") is unavailable to it.

**Not a defect.** `[R-WRT-07]`'s round-15 wording closes this explicitly: it is
"free to place structures anywhere §5.2 admits **and every declared layout
invariant permits (`[R-SLB-01]`, `[R-SLB-03]`)**". Re-establishing is always
possible (pack each run in ordinal order from an A_slab-aligned start), so the
compactor is never stuck. I note only that the citation "§5.2 admits" is
under-inclusive — §5.2 says nothing about `[R-CNT-05]`'s no-structure-after-the-
directory rule, which the output must also satisfy — and that
"Given a conforming input the output is a conforming file" covers it.

### 2.9 Empty layers under limits

**Construction A.** A layer with one dimension of extent 0, tile extent 2^40, one
uint8 channel, codec 4 (lz4). Decoded size P·Q = 2^40 ≫ 0x7E000000.
**Verdict:** conforming. `[R-COD-07]` quantifies over "any of whose *addressed*
tiles", and the layer addresses none. §17.2's Note states this outright, and
§20.3 step 4 confirms the escape "is not durable".

**Construction B.** Same, but tile extent 2^62 and a float64 channel, so
P·Q = 2^65. **Verdict:** reject-layer. The same Note draws the line:
"`[R-ENC-04]`'s overflow rule carries no such quantifier — it binds any sum or
product a file yields — so P·Q and P·Bᶜ are checked in an empty layer even
though this cap is not." L2's Instances cell lists both P·Q and P·Bᶜ.

This is a two-feature interaction (an empty layer under a limit) where the two
features are individually well-specified and the interaction is *also*
specified, in the same sentence. It is the best-closed boundary I found.

### 2.10 Alignment and the value domain

A is a `u64` bounded 512 ≤ A ≤ 2^62; A_slab 1 ≤ A_slab ≤ 2^62; S 1 ≤ S ≤ 2^63−1.
Is A subject to `[R-ENC-03]`'s 0…2^63−1 domain? §4.2's round-15 wording says
"every offset, length, extent, and count this specification defines — **entry
counts and slab run lengths included**". An alignment is none of those, and L1's
Instances cell confirms it: it lists entry_count and S but *not* A or A_slab,
which get their own rows L39 and L29. A = 2^63 is caught by L39 ("A above 2^62")
rather than by L1, and there is no gap. The parenthetical in §4.2 is doing real
work — without it, "slab run length" would have been arguable either way.

### 2.11 Attacks that produced findings

Four attacks produced things I am reporting rather than closing; they are stated
in full in Part 3. In summary:

- §21.7's account of what witnesses a §20.3 step-4 violation is narrower than the
  §21.4 rows that actually fire (adversary-01).
- §20.3's shrink permission and its prior-generation tense rule can be read two
  ways when a single commit de-addresses every stored tile *and* changes a
  declaration (adversary-02).
- §21.1's instance criterion is applied oppositely to the same zstd frame
  constraint in T18 and in R4 (adversary-03).
- §11.1's Rationale says a grid-count-raising growth renumbers disk ordinals; for
  an interleaved layer grown along its first-declared dimension, it does not
  (adversary-04).
- Two duplicated clauses, one of them in a section round 15 rewrote
  (adversary-05).

### 2.12 Attacks that produced nothing at all

Recorded briefly, because an empty result is only worth something if the attacks
were real:

- **Zero-length structures.** Record with inline_length 0 and extent (0,0):
  conforming (an unknown MU=0 type). Directory of exactly 4 bytes: conforming.
  Index region of 0 bytes: forced by `[R-CNT-17]` at entry_count 0. Tile extent
  of 0 bytes: T10. Extent slot with one half zero: F30/L15. All decided.
- **Two structures claiming the same bytes.** Every pairing routes to F33
  (reject-file) or L18 (reject-layer) by `[R-CNT-13]`'s three-way split, and
  claimants reaching the front block or trailer are diverted to the bounds rows
  F9/F10, F31/F32, L16/L17, T8/T9 — a diversion F33's Condition cell spells out
  and which I checked is complete (F31's "extent_offset in 1-15" covers an
  extent lying wholly inside the front block; F30 covers offset 0).
- **A structure claiming bytes outside the file.** F10/F32/L17/T9, each with the
  same strict `> F − 64` bound. Consistent across all four.
- **Foreign major version.** §21.2's preamble decides which rows reach such a
  file: only F1, F6, F8, F14 (the fields `[R-CNT-24]` fixes across majors), with
  F18 outside the premise. I tried to break this with a 100-byte file declaring
  major 2 — would a verifier say "nonconforming (F5)" or "cannot establish"? The
  preamble answers: F5's subject is the file's geometry, so it does not reach.
  And for F < 64 there is no trailer to gate on, so F5 fires and the file
  declares no major. No fork.
- **Boundary values everywhere.** entry_count 0 / 1 / 65,536 / 65,537 / 2^32
  (the §21.9 guarantee, giving a 256 KiB CRC array exactly as its Note claims);
  dir_length 4; extent_length 5 for user metadata; A at 512 and 2^62; A_slab at
  1; generation at 1 and 2^63−1 (§9.3's Note closes the counter); F at 128.
  I recomputed §15.4's 1,000,000-entry example (16 segments, last covering
  16,960; region 20,000,064 bytes; segment 15 at [19,660,800, 20,000,000);
  entry 999,999 at segment byte 339,180; one full segment = 1.25 MiB) — every
  figure correct.
- **The seam between reader and verifier.** Four places where a condition binds
  one and not the other: coverage/overlap (`[R-CNT-13]`), alignment and slab
  invariants (`[R-SLB-01]`, `[R-SLB-03]`), decoded-content obligations
  (`[R-SER-05]`, `[R-SER-08]`), and the front block for a non-resident reader
  (`[R-CNT-04]`). In each the document says which actor owes what and
  `[R-CNF-12]` licenses a reader that detects anyway to reject. I could not
  build a file sitting *on* the seam in a way two verifiers judge differently,
  because in each case both verifiers owe the check.
- **Sparse tile under a filter chain.** A sentinel entry short-circuits steps 5
  and 6 (§19.4 step 4), so no filter or codec is ever applied to an unstored
  tile; `[R-TYP-09]` forbids fill as a failure fallback. Interaction closed.
- **Packed bool plane under byte-shuffle.** s = 1, the filter is the identity, so
  filter 1 and filter 2 produce byte-identical files. Both conforming
  (`[R-CNF-05]`), and §20.3 step 4 names exactly this case as one a commit may
  change: "a filter whose mandated stride makes it the identity".
- **`[R-SER-08]`'s resolved byte.** Two readers handed a nonconforming
  interleaved bool byte of 0x02 — one rejects the tile under `[R-CNF-12]`, one
  returns `true` — differ observably. Licensed, and the Rationale under
  `[R-SER-08]` says why the alternative was worse.

---

## Part 3 — Findings

### adversary-01 — CONTRADICTION — §21.7 (`[R-ERR-01]`) vs §21.4 T14/T17/T25

§21.7 says of §20.3 step 4:

> "§20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — the §21.4 rows
> firing there and nowhere else"

**Counter-example, concrete.** Generation *n*: layer `L`, interleaved, one
`uint16` channel, one dimension with E = 4 and T = 4 (so G = 1, N = 1,
entry_count = 1, **no padding positions**, and **no bool channel**), codec 1,
filter 1. One stored tile, 8 bytes, entry length 8, entry crc matching.

Generation *n+1*: a commit that changes the layer record's `codec` field from 1
to 3 and touches nothing else. Grid counts are unchanged, so entry_count and
extent_length are unchanged and the index region is not even re-emitted — this
is §20.3's shape (c), "a change confined to the directory". §20.3 step 4 bars
it: the change alters "the codec and filter that produced the stored bytes" for
a tile the layer stored in the superseded generation.

In the resulting file the eight stored bytes must now be one RFC 8878 frame.
They are not, so **T17** fires ("the stored bytes do not begin with the
compressed-frame magic 28 B5 2F FD"; if by accident they did, **T25** fires on
the malformed frame). A §21.4 row fires, and the change reached no padding
position, no pad bit, and no boolean byte. The same holds for a change that
alters the decoded size while leaving grid counts alone — **T14** ("Codec 1
(none) declared and a non-sentinel index entry's length differs from the tile's
decoded size") — and for a codec-2 or codec-4 declaration over raw bytes.

So §21.7's "only where … the change reaches a byte §14 structurally constrains"
and its "the §21.4 rows firing there and nowhere else" are both false. The
correct statement is that a declaration change over a still-stored tile is
witnessed wherever it makes the stored bytes inconsistent with the new
declarations — which includes the codec, filter and decoded-size rows, not just
T2/T4/T5.

**Which reading I picked, and why it matters.** I take the §21.4 rows to govern:
§21.1 says the register's "completeness is normative" and that "where a row and
the rule it cites diverge, the rule governs", and T17's governing rule
`[R-COD-06]` is unconditional. An implementer who trusted §21.7's sentence would
conclude that a codec change over stored tiles leaves the live state clean and
that no §21.4 row need fire there — and would build a verifier that skips the
zstd magic check on a tile whose layer record it believes was only edited. The
harm is to a verifier's *coverage*, not to any single file's verdict.

**Byte-level: no.** The counter-example file is rejected at tile scope by T17
under either reading of §21.7, because T17's own rule says nothing about how the
file came to be. §21.7 creates and removes no obligation; it accounts for what
the register omits. Two competent verifiers reach the same verdict on every file
I can construct.

### adversary-02 — AMBIGUITY — §20.3 step 4 (`[R-WRT-04]`), the shrink permission against the prior-generation tense

Two sentences in the same step:

> "A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode … The tense is the prior
> generation's (§3.1 defines *stored* against a generation), so a commit does not
> escape this by unstoring in the same breath: superseding every tile of a layer
> and re-declaring it are one operation, and this bars it."

and

> "An extent MAY also **shrink**. … but where it drops a tile out of the
> addressed set entirely (§11.2's grid count falls), nothing is altered for a
> tile the new state stores, and the commit is permitted"

**The file that sits on it.** Generation *n*: layer `L`, rank 1, E = 4, T = 4,
one `uint16` channel, codec 1, one stored tile. Commit *n+1* does two things at
once: shrinks E to 0 (so G = 0, N = 0, entry_count = 0, extent slot (0,0),
crc_of_crc_array = 0, and the stored tile's extent becomes slack) **and** changes
codec to 3.

**Reading A (the one I picked).** The first sentence's test ranges over tiles
stored in the *superseded* generation. The stored tile was one. Changing codec
alters how its bytes decode. "A commit does not escape this by unstoring in the
same breath" reaches de-addressing as much as it reaches sentinel-writing —
`[R-GEO-02]`'s "the layer has zero addressed tiles" is precisely a way of
unstoring. The shrink paragraph licenses *the shrink*, not whatever else is
bundled with it, and its justification is about what "the new state stores".
Likewise "A layer that stores no tile MAY be re-declared freely" reads, under
§3.1's "unqualified *stored* means stored in the live generation", as a layer
that stored nothing *already* — which this one did not. So the commit is barred
and the writer must do it in two commits.

**Reading B.** The shrink paragraph states its own sufficient condition —
"nothing is altered for a tile the new state stores, and the commit is
permitted" — which is trivially satisfied when the new state stores nothing.
De-addressing is not "unstoring" in the first sentence's sense (that sentence's
example is "superseding every tile", i.e. writing sentinels while the tiles stay
addressed); when the grid count falls, §14 fixes nothing for the vanished tiles
at all, so there is nothing for the change to alter. §11.1's Rationale supports
this framing: "a shrink is barred wherever it alters what §14 fixes for **a tile
the new state still stores**, and permitted where it drops tiles out of the
addressed set". On Reading B the one-commit form is permitted.

**What an implementer does wrong without it.** An appender written to Reading B
emits one commit; one written to Reading A emits two. The files differ in
length, in generation number, and in how much slack they carry. A tool audited
against the wrong reading is either needlessly refusing a legal edit or
performing an illegal one.

**Byte-level: no**, and this is the closest call in my list. It *does* change
which byte sequences a conforming writer may emit — Reading B lets an appender
produce a file Reading A forbids it to produce. But both outputs are conforming
*files*: §21.7 is right that §20.3 step 4 has no single-file witness once the
affected tiles are gone from the live state, and §9.7 does not reconstruct
history. No verifier examining either file can tell them apart on this ground,
so no accept/reject verdict forks. I flag it as a writer-conduct ambiguity and
say plainly that the divergence is in what a writer emits, not in what a reader
must accept.

### adversary-03 — OBSERVATION — §21.1's instance criterion applied oppositely in T18 and R4

§21.1:

> "What a cell enumerates is the condition's own alternatives and containers: a
> row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them (T15,
> T25)."

The same zstd constraint from `[R-COD-06]` — "contains a skippable frame anywhere
or more than one frame" — is enumerated two different ways:

T18 (tile side), four instances:

> "a second concatenated compressed frame; a skippable frame before the frame; a
> skippable frame after the frame; a skippable frame between two frames"

R4 (metadata side), which §18.2 carries the same constraints over to
("no skippable frame and no second frame"), gives *one* instance for the
skippable frame and one for the second frame, times two containers:

> "missing frame magic, top-level extent; missing frame magic, layer sub-record
> extent; a skippable frame, top-level extent; a skippable frame, layer
> sub-record extent; a second frame, top-level extent; a second frame, layer
> sub-record extent; …"

Per container: T18 counts four shapes, R4 counts two. Either the three skippable
positions are "materially different shapes" — in which case R4 should hold 16
instances, not 12, and §21.8's normative total is 279 rather than 275 — or they
are not, in which case T18 should hold two and the total is 273. The document
cannot have it both ways, and §21.1 concedes that the judgement lives in the cell
("the count is therefore mechanical once the cell is written"), so nothing in
§21.1 arbitrates.

I checked the rest of the register against the criterion and found no other
inconsistency: the magnitude-direction rule is applied uniformly (L21, L22, L30,
T3, T14, T22, F17, F23, L12 all enumerate two directions; L44, T21, F5, F10
enumerate one), the layout-formula axis is applied uniformly (T3, T14, T21, T22,
L44, T4, T26), containers are applied uniformly (every R-row doubles for
top-level versus sub-record; L4/L7/L8/L9 double for dimension versus channel),
and single-predicate rows correctly enumerate one (F25, L20, L27, L28). My
mechanical count over all 121 cells reproduces §21.8's 275 exactly, so this is
the only cell pair that misapplies the criterion.

**What an implementer does wrong without it.** A corpus builder following §24's
"one vector per instance" builds either 12 or 16 files for R4 and cannot tell
which discharges `[R-VEC-03]`.

**Byte-level: no.** The corpus size changes; no file's verdict does. A
skippable frame in a metadata extent is ignore-record under R4 wherever it sits,
and a skippable frame in a tile payload is reject-tile under T18 wherever it
sits. This is the register-row class the calibration warns about.

### adversary-04 — OBSERVATION — §11.1's Rationale over-claims ordinal renumbering

> "growth that raises one changes entry_count and with it extent_length
> (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted and disk
> ordinals renumber (§20.3, `[R-WRT-04]`, `[R-GEO-06]`) — the first growth of a
> zero-extent layer included."

Under `[R-GEO-06]` the spatial ordinal is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ. Growing the
**first-declared** dimension raises G₀ but leaves every ∏_{j>i} Gⱼ for i ≥ 0
untouched (the product for i = 0 runs over j > 0), so every existing tile keeps
its ordinal. Concretely: a rank-2 interleaved layer with E = (4, 8), T = (4, 4),
G = (1, 2), N = 2. Grow E₀ to 8: G becomes (2, 2), N becomes 4, and the existing
tiles at (0,0) and (0,1) keep ordinals 0 and 1; entries 2 and 3 are new
sentinels. Nothing renumbers. Renumbering happens when a *non-first* dimension's
grid count rises, or in a planar layer for any c ≥ 1 (since c·N + s moves with
N).

The normative text is correct — §20.3 step 4 says "a geometry change renumbers
ordinals **wherever** `[R-GEO-06]` moves them" — so the defect is confined to the
Rationale, which §2.1 excludes from normative text.

**What an implementer does wrong without it.** An appender that trusted the
Rationale would recompute and rewrite every entry on a first-dimension growth
instead of appending sentinels — wasteful but not incorrect, since the entries
it writes are byte-identical to the ones it would have copied.

**Byte-level: no.** Non-normative text; the normative rule carries the correct
qualifier, and the bytes are identical either way.

### adversary-05 — OBSERVATION — duplicated clauses in `[R-WRT-06]` and `[R-SEC-04]`

§20.5, `[R-WRT-06]`:

> "it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and
> call the output clean — and a record §20.4 does let it drop is no exception,
> dropping being available only where that table licenses it — nor re-emit it
> corrected (`[R-WRT-05]`)."

The first and last limbs of the "neither … nor … nor" are the same prohibition
with the same citation. §20.5 is one of the sections round 15 rewrote, and this
reads as an edit collision: an inserted parenthetical left the original tail in
place.

§22.3, `[R-SEC-04]` carries the same shape:

> "which is why recovery output is re-verified as a whole file before being
> trusted (`[R-LIF-06]`) before any use."

"before being trusted … before any use" is one adverbial phrase written twice.

**What an implementer does wrong without it.** Nothing — both sentences are
readable and neither limb contradicts the other. I report it because a
requirement that lists three prohibitions and delivers two is the kind of thing
a later reader counts, and because §21.1's own "claimed to enumerate cases and
did not" failure mode is what this document has been repairing.

**Byte-level: no.** Pure redundancy; the normative content is unchanged.

---

## Part 4 — Honest limits of this walk

- I did not implement DEFLATE, Zstandard or LZ4. T15–T25 and R4 were read, not
  executed, so any defect that lives inside a bitstream constraint would have
  escaped me. I did check the *interface* rules against the external formats I
  know — the single-segment/Window_Size reasoning in §17.2's Note is correct as
  stated, and the "1 KiB Window_Descriptor floor" claim matches RFC 8878.
- I did not implement the JSON document rules; R5–R10 were read, not executed.
- I could not construct a file two conforming *verifiers* certify differently.
  Every candidate I built resolved to one of three things the document
  constructs on purpose: a reader/verifier asymmetry (`[R-CNT-13]`,
  `[R-CNT-05]`, `[R-SLB-01]`, `[R-SER-05]`), a capability difference reported as
  *cannot establish* rather than as a verdict on the bytes (§2.3, `[R-COD-11]`,
  `[R-MTA-09]`), or a writer-conduct rule expressly declared not to be a
  file-conformance violation (§2.3's enumeration, §10.3, §18.3, §6.3, §6.2).
  That enumeration is unusually disciplined and it is what closed most of my
  attacks.
- The single place I had to infer rather than read: the inverse of §11.4's
  planar disk-ordinal map (c = k div N, s = k mod N), which §14.2's decoded-size
  table and §17.3's shuffle stride both need. It is forced, not ambiguous, but
  it is unstated.
