# Cleanroom round 13 — Verifier implementer transcript

## 0. Disclosure

I opened exactly one file from the repository: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read end to end (4,128 lines, in five `Read` calls). I ran `grep`/`rg` against
that file only. I ran no `git` command, listed no repository directory, opened
no ADR, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`,
no web fetch, no web search.

**One contamination to disclose, with its extent.** My first CRC helper was
written to the shared session scratchpad root as `crc.py`. Between my writing
it and my second invocation, **another agent overwrote that path with its own
`crc.py`**, and my second script imported that file instead of mine. I saw its
output only: six printed lines giving the CRC-32C of `"123456789"`, of zero
bytes, of an 80-byte all-sentinel array, of a 4-byte CRC array, and of a
2^16-entry all-sentinel segment. Those five values are numerically identical to
the ones my own implementation had already produced one call earlier, so no
conclusion of mine derives from it; but I read bytes another round-13 agent
wrote, and that is worth stating plainly. On noticing, I created a private
subdirectory `wk-verifier-priv/` and did every subsequent computation there
with my own `tcrc.py`. I did not read the `round13/` output directory and did
not list it.

Everything else here is computation over bytes I constructed myself:
`tcrc.py` (a CRC-32C implementation), `build.py`, `verify.py`, `adv.py`,
`slab.py`, `gens.py`, `count.py`.

---

## 1. What I built

A conforming verifier, on paper but executable: an ordered certification
procedure, a live-state coverage walk with a slack total, the overlap /
alignment / slab invariant checks, the checksum chain, the decoded-content
checks, and a four-generation lifecycle trace. I built real TARN files
byte-for-byte and ran the verifier against them, including adversarial
variants I constructed to make each verifier-only check fire.

---

## 2. Checksum constants — what I reproduced

Every constant the document states that is locally computable, I computed.

| Constant | Document | Section | My value | Match |
|---|---|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` | §4.5, App B | `0xe3069283` | yes |
| CRC-32C(zero bytes) | `0x00000000` | §4.5, App B | `0x0` | yes |
| CRC-32C of 4 sentinel entries (80 bytes) | `0x80A34955`, stored `55 49 A3 80` | §7.4 example | `0x80a34955`, `55 49 a3 80` | yes |
| crc_of_crc_array of that 4-byte array | `0xC4EE982E` | §7.4 example | `0xc4ee982e` | yes |
| CRC-32C of a full all-sentinel segment (2^16 entries) | `0xEECB3BB2` | §15.4, App B | `0xeecb3bb2` | yes |
| Appendix A trailer CRC over trailer bytes [0,60) | `0xE00938D2` | App A | `0xe00938d2` | yes |

I also re-derived the whole of Appendix A's 128-byte hexdump field by field:
version_major 1, version_minor 0, flags 0, generation 1, dir_offset 16,
dir_length 4, committed_file_length 128 (= file length), file_id
`0x0123456789ABCDEF`, reserved zero, directory region `00 00 00 00` = CRC-32C
of a zero-byte record sequence. Consistent throughout.

**What I could not reproduce:** nothing. Every checksum constant in the
document is locally computable and every one reproduced. The one figure I
could not check by computation is the LZ4 cap `0x7E000000` (§17.2), which is
an external format's interoperability bound, not a checksum; and the zstd
frame magic `28 B5 2F FD`, which is a citation to RFC 8878.

### The §7.4 layer-record example (newly authored — checked byte by byte)

The example is the largest piece of new material in the changed surface, so I
walked it as an implementer rather than reading it.

Offsets I derived independently from §7.4's field table, packed in table order
with no padding:

```
 0  name          1 + 3            = 4     -> [0,4)     03 73 73 74   "sst"
 4  layout        1                        -> [4,5)     01
 5  linearization 2                        -> [5,7)     01 00
 7  codec         2                        -> [7,9)     01 00
 9  filter        2                        -> [9,11)    01 00
11  alignment A   8                        -> [11,19)
19  slab S        8                        -> [19,27)
27  A_slab        8                        -> [27,35)
35  rank d        1                        -> [35,36)   01
36  channel C     2                        -> [36,38)   01 00
38  dim entry     (1+1) + 8 + 8    = 18    -> [38,56)   01 78 | 100 | 32
56  chan entry    (1+4) + 2 + (1+4)= 12    -> [56,68)   "temp", type 12, fill
68  index_encoding 1                       -> [68,69)   01
69  entry_count   8                        -> [69,77)   04
77  crc_of_crc_array 4                     -> [77,81)   2E 98 EE C4
                                              total 81
```

Every offset in the example's annotated dump matches. Its prose accounting
also checks: "Name and the nine scalars from layout through channel count
occupy 4 + 34 bytes" — the nine scalars are layout(1) + linearization(2) +
codec(2) + filter(2) + A(8) + S(8) + A_slab(8) + d(1) + C(2) = 34, and there
are exactly nine of them. Dimension entry 18, channel entry 12, trailing fixed
fields 1+8+4 = 13. 4+34+18+12+13 = 81, no residue, so the sub-record sequence
is empty — which is what `[R-CNT-18]`'s exact-parse rule requires the reader to
conclude.

Grid count ⌈100/32⌉ = 4, so entry_count = 4 (§11.2). `[R-CNT-17]`'s extent
length 4 × 20 + ⌈4/2^16⌉ × 4 = 84. The channel entry is byte-for-byte §12.3's
`temp` entry as claimed. `0x7FC00000` little-endian is `00 00 C0 7F`. Type 12
little-endian is `0C 00`. All correct.

### Other worked numbers I re-derived (all correct)

§11.2 grid example; §11.4 ordinals (300,700) → tile (1,2), s = 10, in-tile
ordinal 11,452, planar disk ordinal 74; §14.2 (Q = 3, size 18, ordinal 5 at
bytes [15,18); planar b's tile 12 bytes at 10–11; Q = 5, size 30, [25,30));
§14.3 packed plane `55 01` / `55 FD`; §14.5 edge tile 32 bytes with 15 padding
positions carrying `CD AB`; §15.4's 1,000,000-entry example (16 segments, last
covering 16,960, array at [20,000,000, 20,000,064), segment 15 at [19,660,800,
20,000,000), 339,200 bytes, one full segment = 1.25 MiB); §15.4's planar
example (ordinal 74 at region bytes [1,480, 1,500); channel-3 entries 96–127);
§16.2's four runs; §17.3's shuffle of 1.0/2.0/3.0 to
`00 00 00 00 00 00 80 00 40 3F 40 40`; §20.3's 32 · 20 + 4 = 644;
§21.9's note (2^32 tiles → 256 KiB CRC array, 2^36 → 4 MiB); §5.1's 128-byte
minimum derivation; §4.6's `température` at 12 bytes NFC / 13 NFD.

### Register arithmetic

I extracted §21.2–§21.5 mechanically and counted rows and semicolon-separated
instances under §21.1's stated criterion (a cell reading `—` is one instance):

```
F  36 rows  56 instances
L  49 rows 110 instances
T  26 rows  54 instances
R  10 rows  44 instances
   121 rows 264 instances
```

§21.2/§21.3/§21.4/§21.5's own headers claim 36/49/26/10, and §21.8 claims
"121 conditions over 264 instances". Exact match. The instance criterion is
mechanically applied.

### Identifier integrity

I extracted every `[R-XXX-NN]` and every bare `R-XXX-NN` (the register's
parenthetical citations). Nineteen prefixes are used; §2.2 declares exactly
those nineteen; none used-but-undeclared, none declared-but-unused. Numbering
is dense per prefix with no gaps (the sole apparent gap, ENC 17–99, is the
`[R-ENC-100]` illustration in §2.2 itself; `[R-SER-04]` is present as its own
withdrawal notice in §14.4, which §2.2's retirement rule requires). I hand-checked
roughly thirty register "Governing rule" citations against the rules they name;
every one lands.

---

## 3. The certification procedure, as an ordered algorithm

This is what I implemented in `verify.py`. Each step names its input, the rows
it can raise, and the outcome.

**Verdict vocabulary (§2.3, `[R-CNF-11]`).** Three verdicts:
*conforming*, *nonconforming*, *cannot establish*. Two report-only qualifiers
that are neither verdicts nor findings: *unexamined* (a scope a
stop-at-first-violation verifier did not look at) and *partial* (a slack total
from an incomplete walk, `[R-CNT-21]`). Plus advisories for SHOULD deviations,
which `[R-CNF-12]` says do not bar certification.

**Availability of each verdict.**
- *nonconforming* — as soon as one violation is established; it has absolute
  priority ("An established violation takes priority ... *cannot establish* is
  available only to a traversal that established no violation").
- *cannot establish* — only when no violation was established **and** at least
  one requirement could not be checked on a capability or resource ground. The
  document names exactly five such grounds (§2.3): an unimplemented format
  major; an MU = 1 record of a type the verifier does not implement; a codec or
  filter it cannot execute (`[R-COD-11]`); a decode declined on resource
  grounds (`[R-ERR-04]`, and so §14's content obligations unchecked); a
  user-metadata document it declines to decode (`[R-MTA-09]`). It explicitly
  excludes a sixth candidate: a document under an unassigned encoding is *not*
  a ground, because no content rule attaches (`[R-MTA-10]`).
- *conforming* — only when the traversal established no violation and was
  unable to check nothing. Note that every named cannot-establish ground
  carries "MUST NOT certify", so *conforming* requires a complete traversal.

**What bars certification:** any established violation; any cannot-establish
ground. What does *not* bar it: a SHOULD deviation (advisory, `[R-CNF-12]`); a
user-metadata record at an unassigned encoding (`[R-MTA-10]` — reported, not a
bar); slack of any size; an experimental-range MU = 0 record; a set ignore-lane
flag bit; a `tarn.` key this text does not register; a standardized key out of
scope or with a wrong-shaped value.

### The ordered algorithm

```
P0  capabilities: codecs/filters implementable, decode resource bound,
    metadata-document decode bound (>= 16 MiB, §21.9 / [R-MTA-09])

P1  OPEN (§19.1)
  1  F := transport-authoritative size ([R-CNT-10]).  F < 128 -> F5 reject-file
  2  bytes [0,16) resident (always, for a verifier) -> byte equality  F6 / F1
  3  fetch [F-64,F); validate in §6.2's fixed order:
        magic F8/F1 ; trailer CRC F14 ; version gate F18 (major != 1 and != 0
        -> CANNOT ESTABLISH, [R-CNT-07]) ;
        then, gates passed: flags F19 ; cfl == F F17 ; cfl % 64 F13 ;
        dir_offset >= 16 F9 ; dir_length >= 4 F16 ;
        dir_offset+dir_length <= F-64 F10 ; generation F11/F2 ;
        file_id != 0 F12 ; reserved zero F15 ; domain/sum F2, F3
  4  fetch directory; verify its terminal CRC before any other use  F20
  5  parse record sequence, no residue  F29 ; type 0 F24 ;
     reserved-range type F36 (+F35 if MU=1) ;
     extent slots of non-layer top-level records F30/F31/F32/F2/F3 ;
     user-metadata framing F21/F22/F23 ; multiplicity F34 ;
     flag bits F25/F26/F28 ;
     layer-name namespace over raw bytes, uniqueness decided first  F4 ;
     layer-record name well-formedness L3/L5/L6
       -- a name field not wholly inside inline_length yields no name,
          contributes nothing to the namespace, and is L23 at layer scope

P2  LAYER ACCESS, every layer (§19.3) -- a verifier accesses all of them
     slot L15/L16/L17/L1/L2 ; §7.4 constraint set L27..L36, L39, L43, L45 ;
     exact parse + sub-record walk L13/L14/L19/L23/L24/L25/L26 ;
     names L4/L7/L8/L9 ; geometry floor + arithmetic L32/L1/L2/L21 ;
     [R-CNT-17] cross-checks L21/L22 ; [R-CNT-16] L20 ; lz4 cap L44 ;
     flag bits (verifier-only) L46/L47/L49

P3  INDEX CHAIN, every layer with entry_count > 0 (§15.4)
     crc_of_crc_array over the stored CRC array  L37
     each segment CRC over exactly its entries' bytes  L38
     (partial final segment covers only its actual bytes; the all-sentinel
      constant is never a substitute for comparison, [R-IDX-05])

P4  ENTRY CLASSIFICATION, every entry (§15.3)
     T6 T7 T8 T9 T10 T11 T12 ; sentinel -> reads as fill, no extent

P5  PER STORED TILE
     entry crc over stored bytes  T1
     codec framing/decode  T14 T17..T25 (+T13/T15/T16/T23 as causes)
     decoded length == declared decoded size  T3
     content: padding positions == fill  T4 ; pad bits == fill bit  T5 ;
     interleaved bool bytes at real positions in {00,01}  T2 ;
     wrong shuffle stride surfaces through T2/T4  T26

P6  RECORD EXTENTS
     user-metadata: terminal CRC R2 ; encoding value R1 ;
     assigned encoding -> decode R3/R4, document rules R5..R10,
     member sort order F27/L48 ;
     unassigned encoding -> no document rule attaches; REPORT owning scope,
     encoding value, stored extent length ([R-MTA-10]); certification unaffected

P7  COVERAGE WALK (§9.7)
     disjointness F33 / L18 ; each non-terminal claimant within [16,F-64)
     dispatched to its own tier's row (F9/F10, F31/F32, L16/L17, T8/T9) ;
     nothing between the live directory's end and the live trailer  F7 ;
     slack total, or partial total naming what stopped the walk

P8  DECLARED LAYOUT INVARIANTS (§16)
     alignment L40 ; slab packing L41 ; slab first-tile alignment L42

P9  VERDICT
     any established violation      -> nonconforming
     else any unchecked requirement -> cannot establish
     else                           -> conforming
     always: report unchecked requirements with their ground; report
     unexamined scopes if the verifier stopped early; report the slack total
     (partial or exact); report each [R-MTA-10] record; report advisories
```

**What the verifier reports when a check cannot be run.** Two distinct
mechanisms, and the document keeps them apart cleanly:
- *cannot run on a capability or resource ground* → the requirement is named
  with its ground, certification is barred, and the verdict is *cannot
  establish* unless a violation was already established.
- *chose not to run it* (stop-at-first-violation) → the scope is reported
  *unexamined*, which "is not a finding that the scope is clean" and
  "constrains the report, not the verdict".
- A third case is neither: §21.7's undetectables (wrong sample content, a
  mis-strided filter with no structural witness, an undisclosed zstd
  dictionary, history-only obligations). §21.7 says outright that "None of
  these is a requirement a verifier is *unable to check* within the meaning of
  `[R-CNF-11]`: no file-level witness exists to check". So they are neither
  reported as unchecked nor do they bar certification. That distinction is
  stated and I needed it.

---

## 4. The coverage walk on a concrete file

I built a file (`build.py`) exercising every claimant class the walk names,
including one deliberately awkward member: an experimental-range record type
whose extent §8.1 covers by no checksum.

Contents:
- **layer `a`** — interleaved, rank 2, extents (4,4), tile extents (2,2), so
  G = (2,2), N = 4 addressed tiles and no padding positions. One `uint8`
  channel `p`, fill `0x00`. Codec 1, filter 1. Declares **alignment A = 512**.
  Tiles at ordinals 0 and 3 stored (4 bytes each, P·Q = 4·1); ordinals 1 and 2
  are sentinels. entry_count = 4, index region 4·20 + 4 = 84 bytes.
- **layer `b`** — planar, rank 1, extent 3, tile extent 3, so G = 1, N = 1;
  channels `m` (bool, fill `0x00`) and `v` (uint16, fill `0xABCD`), so
  addressed tiles = C·N = 2. Disk ordinal 0 is the packed bool plane
  (⌈3/8⌉ = 1 byte); disk ordinal 1 is the uint16 plane (3·2 = 6 bytes).
  entry_count = 2, index region 2·20 + 4 = 44. **No padding positions but five
  pad bits** — the distinction §14.3's Note draws, and the reason I chose these
  extents.
- a file-scope **user-metadata record**, encoding 1, document
  `{"tarn.title":"demo"}` (21 bytes) plus its 4-byte terminal CRC.
- a **type 0x8001 record, MU = 0, PE = 0**, with an 8-byte extent.

Bool plane content: values (true, false, true) → bits 0 and 2 set → `0x05`,
with pad bits 3–7 carrying the channel's fill bit (false = 0). `[R-SER-05]`
fixes those five bits unconditionally, whether or not the plane has padding
positions; my verifier checks them separately from padding positions.

### The partition

```
front signature block         [0, 16)          16
layer a, tile 0               [512, 516)        4
layer a, tile 3               [1024, 1028)      4
layer a, tile-index region    [1028, 1112)     84   (= layer record 0's extent)
layer b, tile 0 (bool plane)  [1112, 1113)      1
layer b, tile 1 (uint16)      [1113, 1119)      6
layer b, tile-index region    [1119, 1163)     44   (= layer record 1's extent)
user-metadata extent          [1163, 1188)     25
type-0x8001 record extent     [1188, 1196)      8
directory region              [1196, 1468)    272
live trailer                  [1472, 1536)     64
                                       claimed 528
F = 1536                                slack  1008
```

Slack runs: [16, 512) = 496 (alignment gap before the first 512-aligned tile),
[516, 1024) = 508 (alignment gap before the second), [1468, 1472) = 4 (the
pre-trailer pad). 496 + 508 + 4 = 1008 = 1536 − 528. The two computations agree,
which is the check that the partition is a partition.

**Verdict: conforming.** No violation, nothing unchecked, exact slack total 1008.

### A mistake the document caught, and it is worth recording

My first walk **double-claimed each layer's tile-index region** — once as "each
record's extent" and once as "the layer's index region" — and my verifier
reported two spurious overlaps and a slack total 128 bytes too low. §9.7
anticipates precisely this:

> "A layer record's extent slot addresses that layer's tile-index region
> (§7.4), so the region enters the walk once, as that record's extent, and is
> not a second claimant beside it."

It also anticipates the symmetric error in the other direction:

> "A record is not a claimant of its own — its header and inline payload lie
> inside the directory region, which is the claimant covering them — so
> reaching a record through the directory is traversal, not a second claim on
> those bytes."

Both sentences are load-bearing. Without the first I would have shipped a
verifier that rejects every conforming file with a layer. This is the single
place in the walk where the document saved me from a defect rather than the
other way round.

### Certified vs counted-but-unconstrained vs neither

- **Certified** (a checksum verifies them, or equality does) — 520 of the 528
  claimed bytes:
  - front block 16, by byte equality (§8.1 row 1: "none — checked by byte equality");
  - trailer 64: [0,60) by the CRC at [60,64), which is terminal and
    comparison-verified;
  - directory 272: the leading 268 by the terminal 4;
  - index regions 84 + 44: entries per segment by the segment CRC array, the
    array itself by `crc_of_crc_array`, which is itself inside the directory
    and so covered by the directory CRC;
  - stored tiles 4 + 4 + 1 + 6 = 15, each by its index entry's `crc` field,
    which is covered by its segment CRC;
  - user-metadata extent 25: the leading 21 by the terminal 4.
- **Claimed but covered by no checksum** — 8 bytes: the type-0x8001 record's
  extent. §8.1's last row: "Extent of a record of a type this specification has
  not assigned | none — the bytes are opaque (§7.2) | —". These bytes are
  *live*, so they are not slack and they are not counted as slack; they are
  inside the certificate and never inspected. §22.3 `[R-SEC-04]` names this
  residue explicitly and says the certificate covers them uninspected.
- **Counted but unconstrained** — 1008 bytes of slack. "Slack has no internal
  structure this specification defines, its content is unconstrained, and no
  conformance requirement applies to it" (§5.2).
- **Neither** — none, and the document argues this is not merely true of my
  file but of every file. §5.2's Note: "The live committed state is *defined*
  as the front block plus what a complete coverage walk reaches, and
  `[R-LIF-08]` makes every byte that walk misses slack — so 'belongs to no
  class' describes nothing, and a register row for it would be a row no file
  could exhibit." So the answer to "can any byte be neither" is: no, by
  construction, and the untestability of that half of `[R-CNT-02]` is stated
  rather than left for an implementer to discover.

**So: is every live structure covered by a checksum? No.** A conforming file
can carry live bytes under no checksum, via an experimental-range record type
with MU = 0 — which §21.6 records as conforming. That is the honest answer, and
the document states it in three places (§4.5's exception list, §8.1's last row,
§22.3's four residues).

### A walk that does not complete

I corrupted one byte of layer `b`'s segment-CRC array (offset 1159). The
verifier detects `crc_of_crc_array` mismatch → **L37, reject-layer**
(`[R-IDX-04]`, `[R-CNT-20]`). Per `[R-CNT-21]`, "a rejected layer's claimants
are not enumerated, whether or not the rejection impeded reading them". Layer
`b` forfeits its index region (44) and both stored tiles (1 + 6) = 51 bytes.

```
enumerated claimants: front 16, trailer 64, directory 272,
                      layer a index 84, layer a tiles 4 + 4,
                      user-metadata extent 25, 0x8001 extent 8   = 477
partial slack total = F - 477 = 1536 - 477 = 1059
true slack (from the intact file)                                = 1008
```

1059 ≥ 1008, so the partial total is an upper bound as `[R-CNT-21]` promises
("an upper bound on the file's true slack, never an under-count"). The verifier
reports it as *partial* and names what stopped the walk: layer `b`, rejected on
L37 / `[R-IDX-04]`. Verdict: **nonconforming** (a violation was established, so
the priority rule fixes it regardless of how much went unchecked).

I confirmed the bound property holds in general: partial = F − enumerated, and
enumerated ⊆ all-live-claimed, so partial ≥ true slack, with equality exactly
when the walk completes.

**Which rejections do and do not make the walk incomplete.** I had to work this
out and it is fully decided by the text:
- **reject-file** — the traversal ends; verdict is nonconforming anyway.
- **reject-layer** — always incomplete for that layer's claimants
  (`[R-CNT-21]`), so always a partial total.
- **reject-tile on a *structural* ground** (T6–T12) — *not* incomplete. §9.7:
  "an entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
  contributes no stored extent to the walk"; and "does not make the walk
  incomplete: the walk passes over it, and the bytes it nominally addressed
  fall to slack". So the total stays exact even though the file is nonconforming.
- **reject-tile on a crc or decode ground** (T1, T3, T14, T17–T25) — *not*
  incomplete either. §9.7: "one whose stored bytes alone fail its crc keeps its
  extent". §15.3 gives the principle: "the defect lies in the bytes it
  addresses, not in the entry, so its extent stands".

That third and fourth bullet are the interesting ones, because `[R-CNT-21]`'s
general clause ("a scope-level rejection ends that scope's enumeration") would
on its own suggest a reject-*tile* also truncates the walk. §9.7's two explicit
carve-outs override it, and they are the more specific text. I read them as
governing and implemented accordingly; §21.1's "where a row and the rule it
cites diverge, the rule governs" is not needed here because these are two rules
at different specificity, not a row and a rule.

---

## 5. Extent overlap, alignment, and slab invariants on adversarial layouts

### Overlap

`[R-CNT-13]`'s taxonomy has three cases, and §15.3's table plus F33/L18
implement them:

| Overlapping pair | Outcome | Row |
|---|---|---|
| both structures of one and the same layer | reject-layer | L18 |
| across two layers, or a layer structure against another scope's | reject-file | F33 |
| two structures neither of which belongs to a layer | reject-file | F33 |

I built case 1: I re-pointed layer `a`'s tile-3 entry at [1026, 1030), which
overlaps layer `a`'s own index region at [1028, 1112), and recomputed the
segment CRC, `crc_of_crc_array` and the directory CRC so that nothing else
would fire first. The verifier reports the overlap (L18 — intra-layer, since
both claimants belong to layer `a`), plus L40, because 1026 is not a multiple
of the declared A = 512. Two independent verifier-only checks firing on one
adversarial layout, at the two different scopes their rules assign.

What made this checkable rather than guesswork is F33's carve-out sentence:

> "a claimant reaching the front signature block or the live trailer is instead
> caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own
> tier"

I checked that carve-out list is exactly complete: the five claimant kinds are
the directory (F9/F10), a non-layer top-level record extent (F31/F32), a layer
record's or sub-record's extent (L16/L17), and a stored-tile extent (T8/T9).
Nothing is left over, so the overlap check never has to decide the front-block
or trailer case itself. That is a real piece of engineering in the document.

One consequence worth stating for implementers, because it is easy to miss and
the text does decide it: **two index entries may not point at the same stored
extent.** "Extents are owned exactly once ... no two extent slots and no two
structures overlap" (§7.2), and §15.3's row "two stored extents of the same
layer overlap" makes identical extents an overlap. So a writer cannot
deduplicate two byte-identical tiles by sharing one payload. Verifier-detected,
reject-layer.

### Alignment

Layer `a` declares A = 512. `[R-SLB-01]`: "every stored tile's offset satisfies
offset mod A = 0" — stored tiles only. I confirmed the index region is *not*
subject to it (it sits at 1028 in my conforming file, which is not a multiple
of 512, and the file certifies). Moving tile 3 to 1025 raises L40. Readers are
explicitly not obliged to check this ("offsets are always explicit, so
alignment is reader-invisible"), which is why it is verifier-only.

### Slabs

I built a separate layer (`slab.py`): interleaved, rank 1, extent 8, tile
extent 2, so G = 4, N = 4, P = 2, Q = 1, decoded size 2 bytes; S = 2,
A_slab = 16. Runs partition [0, N) into [0,2) and [2,4) (`[R-SLB-02]`).

| Layout | Result |
|---|---|
| tiles at 512, 514 \| 528, 530 | conforming |
| tiles at 512, **515** \| 528, 530 (gap inside run 0) | **L41** |
| tiles at 512, 514 \| **530**, 532 (530 mod 16 = 2) | **L42** |
| ordinal 1 sentinel; 512 \| 528, 530 | conforming — sentinel transparent |
| ordinal 0 sentinel; run 0's first *stored* tile is ordinal 1 at 512 | conforming |
| run 0 as t0@514, t1@512 (out of ordinal order) | **L41 + L42** |

Two readings I had to settle and the text settles both:
- "each stored tile's offset equals the previous stored tile's offset plus its
  length" — "its" is the *previous* tile's length; the relation is packing, so
  offset[i] = offset[i−1] + length[i−1]. L41's own gloss ("gap; overlap;
  out-of-ordinal placement") confirms it, and the out-of-ordinal case in my
  table shows the relation catches ordering too.
- "the first stored tile's offset satisfies offset mod A_slab = 0" — the first
  *stored* tile of the run, not the tile at the run's first ordinal. §16.2's
  surrounding sentence is about "the run's stored tiles", and "Sentinel tiles
  are transparent to run continuity" makes the sentinel case behave the same
  way. My fifth row exercises exactly this: ordinal 0 is a sentinel, ordinal 1
  is the first stored tile, and its offset 512 is what A_slab measures. "A run
  with no stored tiles imposes nothing" closes the degenerate case.

The invariant stays decidable from index bytes alone, which is the property
§16.2 asserts, because an entry whose only defect is a failing payload crc is
*not* transparent — "its offset and length stand, and the packing relation
reads them as it does any other stored tile's". That means a verifier can run
P8 before or after P5 and get the same answer. I ran it before, from index
bytes only, and it worked.

---

## 6. Decoded-content obligations

**What a verifier must decode.** §9.7 is categorical: "A verifier decodes every
stored tile, whatever content obligations §14 places on the layer: §21.4's
codec rows are file-conformance violations, and a verifier MUST NOT certify
past a violation it has not looked for." So a layer with no padding positions,
no bool channels and no pad bits still has every tile decoded — T3, T24 and T25
have no other detection path.

It must also decode every **user-metadata document under an assigned
encoding**. That obligation is nowhere stated in the form §9.7 uses for tiles;
I reconstructed it from three places and it converges: §2.3 ("checks every
file-level requirement — including those ordinary readers are exempted from"),
§21.3's L48 and §21.2's F27 (member ordering, detector *verifier*, detected
*certification* — impossible without decoding), and §2.3's fifth
cannot-establish ground, which presupposes that a verifier decodes documents.
Appendix H lists "user-metadata member ordering" among the verifier's checks.
A verifier that skipped documents would certify a file with unsorted members;
that reading is refuted by §21.1's detector column plus `[R-CNF-04]`, so it is
not a live fork — but it is the single obligation in my charter that I had to
assemble rather than read.

**What it compares against.**
- Decoded length must be exactly the declared decoded size (T3), where decoded
  size is P·Q interleaved, P·Bᶜ for a planar numeric plane, ⌈P/8⌉ for a packed
  planar bool plane. "decoded size is a function of the layer's declarations
  alone ... never of payload content" (`[R-SER-07]`).
- Under codec 1, the *stored* length must equal it too (T14), checkable before
  any payload fetch.
- Every padding position must encode, per channel it carries, the recorded fill
  — fill bytes for a numeric channel, the fill byte for an interleaved bool,
  the fill bit in a packed plane (T4).
- Every pad bit must carry the plane's fill bit (T5) — unconditionally, whether
  or not the plane has any padding position.
- Every interleaved bool byte at a *real* position must be `0x00` or `0x01`
  (T2); the same byte at a padding position is T4's, and the two rows together
  cover `[R-SER-08]`. I checked that partition is exhaustive and
  non-overlapping: since `[R-TYP-07]` confines the bool fill byte to
  `0x00`/`0x01`, a rogue byte at a padding position necessarily differs from
  fill and so is T4.
- A wrong shuffle stride is not checked directly; T26 records it as a cause and
  says "the check that detects it is T2's or T4's". I verified that the same
  cause/check pattern is consistent throughout §21.4 — T13 defers to T25, T15
  to T24 or T25, T16 to T24, T23 to T25 — and in every case the cause row's
  Detector matches its detecting row's Detector. That consistency is what makes
  the register implementable as written.

**What it is permitted to skip.** Sample values at real positions ("this format
detects *corruption of structure*, not *incorrectness of content*", §21.7); the
content of slack; the content of an unassigned record type's extent (§8.1);
the content of a user-metadata document under an unassigned encoding
(`[R-MTA-10]` — with a *mandatory report* of scope, encoding value and stored
extent length in its place); the unused high bits of a raw DEFLATE stream's
final byte ("This specification constrains them nowhere", §17.2). And it may
decline a decode on resource grounds, at the cost of *cannot establish*.

I confirmed the shuffle is well defined on all three shapes: §17.3 promises
"The decoded image's length L is divisible by s in every case", and indeed
P·Q / Q, P·Bᶜ / Bᶜ, and ⌈P/8⌉ / 1 all divide.

---

## 7. Multi-generation trace

Four generations, built as real byte sequences and verified independently at
each step (`gens.py`).

| | Operation | F | live bytes | slack | Verdict |
|---|---|---|---|---|---|
| gen 1 | **create** — 2 layers, metadata record, opaque record | 1536 | 528 | 1008 | conforming |
| gen 2 | **append** — store layer `a`'s tile 1 (was sentinel) | 1984 | 532 | 1452 | conforming |
| gen 3 | **update** — supersede layer `a`'s tile 0 with new bytes | 2496 | 532 | 1964 | conforming |
| gen 4 | **compact** — fresh `file_id`, generation 1 | 1920 | 532 | 1388 | conforming |

**gen 2.** Layer `a`'s stored-tile set changes, so `[R-WRT-04]` step 4 requires
its whole tile-index region re-emitted at a new placement (`[R-LIF-01]` freezes
the old one where it lies), with the new entry written to its new state and
"every other entry byte-identical at its disk-ordinal position". The new tile
must be 512-aligned, so it goes at 1536 = F(gen1). Layer `b`'s record, the
user-metadata record and the 0x8001 record are re-emitted byte-identically
(`[R-WRT-05]`), keeping their extent slots. Slack grows by exactly the
superseded index region (84) + the old directory (272) + the old trailer (64),
plus the new pre-trailer pad (24): 1008 + 84 + 272 + 64 + 24 = 1452. The old pad
was already inside gen 1's 1008. The arithmetic closes.

**gen 3.** A supersede: the stored-tile *set* is unchanged, but index *content*
changes, so §20.3 step 4 still re-emits the whole region. Live bytes stay 532;
slack grows by the superseded payload (4) + old index (84) + old directory
(272) + old trailer (64) + new pad (88) = 512, so 1964. Two consequences the
text draws and I checked hold: §20.4's MU = 0 / PE = 0 row says "Superseding a
stored tile's bytes is not such a change ... so a commit whose only change is a
supersede MUST retain the record" — so my 0x8001 record could not be dropped
here even though its flags permit dropping in principle. And §20.3's note
quantifies the shape: the commit's cost is dominated by the index, not the data.

**gen 4, compaction.** `[R-WRT-06]`: a fresh `file_id` ("a new draw under §9.3's
randomness advice, not merely a value compared against the input's") and
generation 1. `[R-WRT-07]`: every stored tile's bytes verbatim, each entry's
crc unchanged, extent slots re-pointed, each relocated index region regenerated
with new entry offsets and recomputed segment CRCs, and `crc_of_crc_array`
updated. The output's reference arrays equal the input's bit for bit.

The instructive part: **compaction cannot drive slack to zero here, and it is
not supposed to.** Layer `a` declares A = 512 and now stores three tiles, so
the compactor must place them at 512, 1024 and 1536, and the directory must
follow the last of them (§6.2 forbids any structure between the directory's end
and the trailer, which effectively pins the directory last). My first attempt
packed the tiles contiguously at 512/516/520 and the verifier correctly
reported two L40 violations — the compactor would have emitted a nonconforming
file, which `[R-WRT-06]` forbids ("MUST NOT emit a file carrying a violation it
has detected"). Placing the other structures into the [16, 512) gap and
honouring the alignment gives F = 1920 and slack 1388: down from 1964, up from
gen 1's 1008 because there are now three aligned tiles rather than two.

§20.5's "so slack is never carried" is about the *input's* slack, not about the
output having none — and the section's own figure shows the output carrying a
`pad`. I had to reason that out but the text supports only that reading, and
§16.1 independently classifies alignment gaps as slack.

**Certification at every generation: conforming**, exact slack total each time
(the walk completes in all four). No generation's verdict depends on any
earlier one, which is §9.7's point: "A verifier certifies what a reader can
reach and counts what it cannot ... and does not depend on reconstructing the
file's history."

---

## 8. Places I had to guess, and how each resolved

Recorded whether or not it produced a finding.

1. **Is the extent of a record the verifier *ignores* still a claimant?**
   §2.4 says an ignored record is "skipped as though absent", which would
   suggest not. Resolved by `[R-CNT-02]`'s parenthetical: "a record extent (the
   bytes any record's extent slot references, **whatever the record's type**)".
   So yes, claimed. Matters for my 0x8001 record's 8 bytes, and for a
   conforming file it is the difference between a slack total of 1008 and 1016.
   Decided.
2. **Does a rejected layer forfeit its *index region* from the partial total,
   given that the region's location comes from fully verified directory bytes?**
   This is the one I could defend two ways. Finding verifier-01.
3. **"the previous stored tile's offset plus its length" — whose length?** The
   previous tile's. Settled by L41's gloss and by the word "packed".
4. **"the first stored tile's offset" — first stored, or the run's first
   ordinal?** First *stored*. Settled by sentinel transparency plus "A run with
   no stored tiles imposes nothing".
5. **Must a verifier decode user-metadata documents?** Yes; assembled from
   §2.3 + §21.1's detector column + F27/L48 + Appendix H. Never stated in the
   direct form §9.7 uses for tiles, but not open.
6. **Does a longer-than-64-byte pre-trailer pad make a file nonconforming?**
   No. §6.2 is explicit: "a longer gap is conforming, and no conforming commit
   produces one." I checked the register for a row and there is none, and
   §21.1's normative completeness makes that absence dispositive. So a
   conforming file exists that no conforming commit produces — deliberately.
7. **Does the directory have to be physically last?** Effectively yes, and by
   an indirect route: §6.2/`[R-CNT-05]` forbids any structure between the
   directory's end and the trailer, so any structure after the directory is F7.
   Appendix G item 3 and §5.1's figure agree. I implemented it as a positional
   check and it is exactly right.
8. **Can `[R-COD-11]`'s cannot-establish branch fire for a *conforming*
   verifier?** No: all four codecs and both filters are core, so the only
   unexecutable values are reserved or experimental, which are themselves
   violations (L43/L45) → nonconforming, and the priority rule takes over.
   §17.4 says this itself. So §2.3's third ground is unreachable for a
   conforming verifier. Harmless, and stated.
9. **Does the verifier detect F33 across a layer it has already rejected?** No —
   the rejected layer's claimants leave the walk, so a cross-layer overlap
   involving it becomes invisible. The verdict is nonconforming either way, and
   §2.3 licenses stopping at the first violation outright, so no verifier ever
   owes a complete violation list. Closed, not a finding.
10. **Encoding 0 and reserved-range (3–0x7F) metadata encodings vs
    `[R-MTA-10]`.** §2.3 says flatly that an unassigned encoding leaves
    "certification unaffected", but encoding 0 and reserved values are
    *violations* (R1) that do bar certification. The two compose correctly:
    `[R-MTA-10]` only says the encoding is not a *cannot-establish ground* and
    that no document rule attaches; whether the file certifies is then decided
    by R1. §21.6's row is scoped to the experimental range only, which is the
    case where the file really is conforming. No fork — both readings give
    nonconforming for encoding 0, conforming for experimental.

---

## 9. Findings

### verifier-01 — AMBIGUITY

**Location.** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`.

**Quotation.** §5.2:

> "Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection ends that scope's enumeration — a rejected
> layer's claimants are not enumerated, whether or not the rejection impeded
> reading them — or because the verifier elected under `[R-CNF-11]` to stop at
> the first violation — the verifier MUST report the total as partial. A
> partial total is F less the bytes claimed by the claimants the walk did
> enumerate"

**The two permitted readings.** The clause "a rejected layer's claimants are not
enumerated" sits inside an em-dash aside explaining *when* a total must be
reported as partial. It can be read as:

(a) **A constraint on the walk.** A verifier meeting a reject-layer must drop
every claimant belonging to that layer, including the tile-index region, and
report the resulting total.

(b) **An explanation of a triggering condition.** The operative MUST is "report
the total as partial"; the aside describes the ordinary case in which a
rejection prevents enumeration. A verifier that *can* still enumerate some of
the layer's claimants may do so, and reports a tighter partial total.

The distinction has teeth specifically for the **tile-index region**, because
it is reached as the layer record's extent slot — a value inside the directory,
already CRC-verified — and so its location is known even when the rejection is
an index-chain failure that makes the *entries* untrustworthy. Under (a) the
region drops; under (b) it stays.

**Which I picked and why.** (a). The clause "whether or not the rejection
impeded reading them" is doing work only under (a): under (b) it would be
vacuous, since a verifier that was not impeded would simply enumerate. So I
implemented "a reject-layer forfeits every claimant of that layer, including
the index region", and my worked example above reports 1059 rather than 1015
for the same corrupted file.

**What an implementer does wrong without it.** Nothing that changes a verdict.
Both readings produce upper bounds on the true slack, both satisfy "never an
under-count", and the document itself says a partial total "is not the file's
slack total but a bound on it". Two conforming verifiers therefore print
different numbers for the same damaged file — 1059 and 1015 in my example — and
an operator comparing verifier outputs across tools, which §22.3 says is how
one distinguishes "a working file from a padded one", would see the disagreement
and have no way to tell which tool is right. The consequence is a report-quality
divergence, not a conformance divergence.

**Byte-level: no.** No accept/reject verdict differs and no byte on disk
differs. For a *conforming* file — the case in which the number is supposed to
be determined — the walk always completes, every claimant is fixed by §9.7's
enumeration, and both readings collapse to the same exact total. I verified
this on my own file: 1008 either way. The ambiguity is confined to files that
are already nonconforming, where the verdict is fixed by the priority rule
before the total is computed.

---

### verifier-02 — OBSERVATION

**Location.** §24 `[R-VEC-02]`; the cross-reference targets §21.1.

**Quotation.** §24:

> "the §21 register row it exercises together with that row's governing
> requirement identifier — row labels are positional and renumber when a row is
> struck (§21.1), while §2.2 makes the identifier permanent, so the pair is
> what survives a renumbering."

**The problem.** §21.1 does not state, anywhere, that register row labels are
positional or that they renumber when a row is struck. I grepped the whole
document: the words "renumber"/"renumbering" occur at lines 119 and 121 (§2.2,
asserting the *opposite* property for requirement identifiers), at 1467 and
2912 (disk ordinals renumbering under a geometry change), and at 3719/3721 —
this passage itself. "positional" occurs exactly once, here. §21.1's actual
content is the completeness clause, the row-versus-rule precedence rule, the
specialization list, the Instances criterion and the Detected vocabulary.

**Permitted readings and which I picked.** Either the citation is meant to point
at §2.2's identifier-stability rule and names the wrong section, or §21.1 is
meant to carry a statement about row-label instability that it does not carry.
I took the proposition as normative where it stands — §24 is normative text and
asserts it directly — and the "(§21.1)" as a pointer that does not land. Nothing
in §21.1 contradicts the proposition; it simply is not there.

**What an implementer does wrong without it.** Nothing, which is why this is an
OBSERVATION and not an AMBIGUITY. A corpus builder reading `[R-VEC-02]` records
the (row, requirement-identifier) pair because `[R-VEC-02]` tells it to; the
parenthetical is the justification, not the rule. The cost is that a reader who
follows the pointer to check the claim finds no such claim, and cannot tell
whether the row-label instability is a real design commitment or an editing
residue — which matters because §21.1's own specialization list ("F1 of F6 and
of F8, F35 of F36, L24 of L25") and §21.8's counts are both stated in terms of
positional labels and would both need revision under any striking, so the
proposition is load-bearing for the document's maintenance even though it binds
no implementation.

**Byte-level: no.** It constrains no file byte and no accept/reject verdict; it
affects only what a conformance manifest's justification cites and where a
reader looks to confirm a claim about label stability.

---

## 10. Confidence

**High** that a verifier built from this document alone interoperates on
accept/reject verdicts. I implemented the certification procedure end to end,
built conforming and adversarial files, and every check I needed had a stated
rule with a stated scope and a stated detector. The two places the document
saved me from shipping a broken verifier — §9.7's "the region enters the walk
once" and its "a record is not a claimant of its own" — are exactly the two
places a careless implementer would go wrong, and both are anticipated in
prose. The register's arithmetic is exact (121/264), its identifier space is
dense and consistent, every locally computable constant reproduces, and every
worked example I re-derived is correct.

The residual risk is not in the verdicts. It is in the *report*: the slack
total for a nonconforming file is a bound whose tightness the document leaves
partly to the verifier, and finding verifier-01 is where that leaves an
implementer with a defensible choice. For conforming files — the only case in
which the number is supposed to be a fact about the file — it is fully
determined, and I verified that on a file of my own construction.
