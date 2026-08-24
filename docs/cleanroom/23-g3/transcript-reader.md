# Round 23 — Reader implementer, working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,426 lines), in four `Read` passes covering lines 1–4426 with no gaps. I ran
`wc -l` and one `grep` against that file. Everything else I ran was local
computation over data I typed in myself: a CRC-32C implementation, a mechanical
count of the §21 register tables (parsed out of the markdown I had already read),
a TARN file builder, and a reader that walks the file it built. I opened no ADR,
no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `registry.json`, no git
history, no network resource. I did not list or read the output directory.

Context I did not ask for did appear before I began: a project instruction file
pointing at `AGENTS.md`, and an index of the maintainer's memory notes naming
several topics. I did not open any of the files it named and I did not use
anything in it. Naming it here as the brief requires; I am not repeating its
contents.

Where I use knowledge of zstd/deflate/lz4 or of other array formats below, I use
it only to generate a suspicion and I say so; nothing is settled that way.

## 1. What I built

I implemented, on paper and then concretely in Python, a conforming reader:
open path, layer access, tile read, and the degradation branches. Then I built a
small conforming file from the document alone and ran the reader over it. Files
in scratch: `crc.py`, `appa.py`, `build.py`, `reader.py`, `reader2.py`,
`count.py`.

## 2. Checking the document's own arithmetic first

Before implementing anything I checked every constant I could compute, because
§4.5 gives a check vector and a wrong constant would be the cheapest finding
available.

CRC-32C, Castagnoli reflected (poly 0x82F63B78 reflected form), init 0xFFFFFFFF,
final XOR 0xFFFFFFFF, stored little-endian (`[R-ENC-09]`):

| Claim | Section | Computed | Verdict |
|---|---|---|---|
| CRC-32C("123456789") = 0xE3069283 | §4.5 | 0xE3069283 | ✓ |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | 0x00000000 | ✓ |
| CRC of 4 sentinel entries (80 B) = 0x80A34955, stored `55 49 A3 80` | §7.4 ex. | 0x80A34955 | ✓ |
| crc_of_crc_array over `55 49 A3 80` = 0xC4EE982E | §7.4 ex. | 0xC4EE982E | ✓ |
| CRC of a full 2¹⁶-sentinel segment = 0xEECB3BB2 | §15.4, App. B | 0xEECB3BB2 | ✓ |
| Appendix A trailer CRC = 0xE00938D2 over trailer [0,60) | App. A | 0xE00938D2 | ✓ |

Appendix A parsed field by field: magic `8A 4E 52 41 54 0D 0A 1A`,
version_major 1, version_minor 0, flags 0, generation 1, dir_offset 16,
dir_length 4, committed_file_length 128 = the file length, file_id
0x0123456789ABCDEF, reserved zero, CRC correct. The directory region [16,20) is
`00 00 00 00`, which is the CRC-32C of the zero-byte record sequence. Every
annotation in Appendix A's table is right, the file is exactly 128 bytes, and
128 mod 64 = 0. No defect.

Non-CRC arithmetic I re-derived and confirmed:

- §7.4's worked layer record: name 4 B + nine scalars 34 B + one dimension entry
  18 B + one channel entry 12 B + trailing fixed fields 13 B = 81 B, matching
  the stated `inline_length = 81` and every offset in the hex block (0, 4, 5, 7,
  9, 11, 19, 27, 35, 36, 38, 40, 48, 56, 63, 68, 69, 77). Index extent
  4·20 + ⌈4/2¹⁶⌉·4 = 84 ✓.
- §11.2: G=(4,8), N=32, P=65,536; with extents (1000,2048), G_y = ⌈1000/256⌉ = 4 ✓.
- §11.4: (300,700) → tile (1,2) → s = 10; in-tile (44,188) → ordinal
  44·256+188 = 11,452; planar C=4, channel 2 → 2·32+10 = 74 ✓.
- §14.2: interleaved (2,3), uint8+uint16 → Q=3, size 18, ordinal 5 at [15,18) ✓;
  planar `b` plane 12 B, ordinal 5 at [10,12) ✓; float32+bool → Q=5, size 30,
  ordinal 5 at [25,30) ✓.
- §14.3: P=10 alternating from true → `55 01` with fill false, `55 FD` with fill
  true ✓ (I packed the bits LSB-first and set bits 2–7 of the last byte).
- §14.5: extents (5,5)/tiles (4,4) → edge tile (1,1) has 1 real and 15 padding
  positions, 32 decoded bytes, values 1–15 each `CD AB` ✓.
- §15.4: entry_count 1,000,000 → 16 segments (last 16,960), 64-B array, region
  20,000,064 B; k=999,999 in segment 15 at relative byte 339,180; array at
  [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000) = 339,200 B;
  a full segment is 1,310,720 B = 1.25 MiB ✓. Planar example: disk ordinal 74 →
  region bytes [1,480, 1,500); channel 3's entries 96–127 ✓.
- §17.3: shuffling `00 00 80 3F | 00 00 00 40 | 00 00 40 40` at s=4, n=3 gives
  `00 00 00 00 00 00 80 00 40 3F 40 40` exactly as printed, and the stated
  inverse restores it ✓.
- §12.1: bfloat16 1.0 = high 16 bits of binary32 1.0 = 0x3F80 ✓.
- §4.6: `température` NFC = 12 bytes `74 65 6D 70 C3 A9 72 61 74 75 72 65`, NFD =
  13 ✓.
- §20.3's example: 32·20 + 4 = 644 ✓.
- §21.9's note: segment-CRC array at entry_count 2³² is 2¹⁶·4 = 256 KiB, and
  2²⁰·4 = 4 MiB at 2³⁶ ✓.
- `0x7E000000` = 2,113,929,216 ✓ (the lz4 block-format interoperability bound).

**Every stated constant, offset, checksum and worked example in the document is
correct.** I found no arithmetic defect anywhere.

## 3. The register's stated total (§21.8)

§21.8 asserts "121 conditions over 277 instances". I parsed the four register
tables mechanically out of the markdown and counted each Instances cell as its
semicolon-separated item count, with a cell reading `—` counting 1, which is the
rule §21.1 states ("Instances within a cell are separated by semicolons, and a
cell reading — is one instance; the count is therefore mechanical once the cell
is written").

Result: 121 rows, 277 instances. By section: F 36 rows / 58 instances,
L 49 / 116, T 26 / 55, R 10 / 48. §21.2 declares 36, §21.3 declares 49, §21.4
declares 26, §21.5 declares 10 — all four match, and 36+49+26+10 = 121.
**§21.8's total is exactly right.**

I then audited the Instances cells against §21.1's stated individuation axes,
because a stated total is only as good as the cells it sums:

- *Layout formulas enumerated where the derived quantity varies by layout*:
  L44 (3), T3 (3×2), T14 (3×2), T21 (3×1), T22 (3×2), T26 (3). All correct.
- *Two directions where either magnitude can be the greater; one where the text
  bounds the comparison*: F17 (2), L21 (2 layouts × 2 directions = 4), L22 (4),
  L30 (2), T3/T14/T22 (×2), R4's content-size pair (2 × 2 containers). And
  one-direction rows: F5, F10, F32, L1, L2, L17, L44, T9, T11, T21 — all single.
  Correct.
- *No direction for a checksum-vs-computed or byte-vs-constant comparison*:
  F14, F20, L37, L38, T1, R2 all 1. Correct.
- *No instance for a nonzero test*: L20, L27, L28 all 1. Correct.
- *One instance is one distinguishable file*: T12 (offset+length as a single
  predicate over two fields) = 1, while F30 and T7 (exactly one half zero /
  exactly one half sentinel) = 2, because those two are distinguishable files.
  Correct.
- Enum-band rows track the value sets exactly: L31 (3 bands), L33 (4), L34 (4),
  L36 (2, channel layout having no experimental range per §10.2), L43 (3),
  L45 (3), R1 (2 bands × 2 containers). Correct.

I also cross-checked Detector against Detected for all 121 rows: every
`verifier` row is `certification` and no `reader` row is; the only compound cell
is R1's "open (top-level); layer access (sub-record)", which is right because
the encoding byte lives in a record's inline payload and a sub-record's payload
is not parsed until layer access (§19.3). No mismatch.

The one soft spot I found: **R7's Condition cell names two alternatives** ("not
well-formed JSON, or its top-level value is not an object") **while its
Instances cell enumerates three** (adding "leading U+FEFF"). §21.1 says an
instance may name "one of several alternatives *the condition text states*", and
the BOM alternative is stated in `[R-MTA-04]`'s first bullet rather than in R7's
own condition text. Since §21.1 makes the count mechanical from the cell as
written, the total is unaffected, and §21.1 already says the rule governs where
row and rule diverge. I judged this too small to report as a finding: it costs
an implementer nothing and moves no byte.

## 4. The open path, implemented

I wrote the open exactly as §19.1 orders it, with a transport shim that logs
every range it serves so I could produce the byte-exact accounting the charter
asks for.

**Step 1 — end of file.** Obtain F transport-authoritatively (`[R-CNT-10]`). For
a remote reader this is not a separate request: the suffix range for step 2
carries F in its own response (§6.4), and `[R-CNT-10]` forbids substituting
committed_file_length for it. What bounds this range before I have read
anything: nothing but the constant 64, which `[R-CNT-24]` fixes permanently
across every format major. That is what makes a cold open possible at all.

Also at step 1: if my open leaves bytes [0,16) resident I MUST verify the front
block by equality (`[R-CNT-04]`); if I would have to issue a further range for
them I MAY skip it. The test is residency, not transport. My local reader
verifies; my two-exact-ranges remote reader does not. Both are conforming, and
the two therefore reach different verdicts on a file with a corrupted front
block. That divergence is licensed three times over (§6.1's rationale, §19.1
step 1, F6's own Condition cell) and the file in question is nonconforming
anyway, so `[R-CNF-12]` already permits either. Not a defect — but it is the one
place in the reader where two conforming implementations legitimately disagree
about accept/reject, and I wanted it on the record.

**Step 2 — trailer.** Fetch [F−64, F). Validate in §6.2's fixed order: magic
(F8), trailer CRC (F14), version gate (F18, and reject-file on an unimplemented
major with a *distinct* diagnostic per `[R-CNT-07]`). Only those three touch
fields whose positions §6.2 guarantees across majors. Then, those gates passed,
validate together: flag gates (F19 — every incompat bit is unimplemented since
this text defines none), committed_file_length = transport size and a multiple
of 64 (F17, F13), dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16),
dir_offset + dir_length ≤ F − 64 (F10), 1 ≤ generation ≤ 2⁶³−1 (F11, F2),
file_id ≠ 0 (F12), reserved bytes zero (F15). Also the 128-byte floor (F5,
`[R-CNT-27]`). Any failure is reject-file.

Note that these last gates are explicitly *unordered among themselves* — §24
relies on that ("a file failing two of them attributes to neither alone"), so a
vector cannot isolate them. I implemented them as a single conjunction.

I checked that file_id is correctly *not* subject to `[R-ENC-03]`'s 2⁶³−1
domain: it is an identifier, not an offset/length/extent/count, and F2's
instance list correctly omits it while listing dir_offset, dir_length,
committed_file_length and generation.

**Step 3 — directory.** Fetch [dir_offset, dir_offset + dir_length). Verify the
terminal 4 bytes against the CRC-32C of the preceding dir_length − 4 (F20)
*before any other use of the region* — this is where `[R-ENC-05]`'s "do not
seek or allocate on an unverified integer" bites, and the chain closes: the
extent slots I am about to act on are covered by this CRC.

**Step 4 — record walk.** Parse 24-byte headers plus inline_length payloads to
exactly the end of the sequence, no residue (F29). Type 0 is a violation, never
an unknown type (F24). Multiplicity: at most one top-level user-metadata record
(F34); any number of layer records including zero. Unknown top-level types:
MU = 1 → reject-file, MU = 0 → ignore (`[R-CNT-15]`). Extent-slot rules for
*non-layer* top-level records only (F30/F31/F32) — a layer record's slot is
deferred to layer access, which the register confirms (L15–L17 are "layer
access"). The extra framing a top-level user-metadata record carries: no (0,0)
slot (F21), extent_length ≥ 5 (F22), inline_length exactly 1 (F23). Plus R1 —
the encoding byte's own value set — which §19.1 does not restate but §19's
preamble expressly covers ("Those enumerations are not the complete inventory of
what a reader detects at that tier: §21's register is"). That preamble is what
makes §19 safe to implement from; without it I would have had to guess whether
§19.1's list was closed.

Then build the layer table. Two subtleties the document nails down and I would
otherwise have guessed at:

1. Uniqueness is decided **first**, over **raw bytes**, whether or not either
   name is itself well-formed — because `[R-ENC-13]` makes comparison a byte
   comparison, which needs no valid name. So two layers with byte-identical
   ill-formed names are a duplicate (F4, reject-file), not two separate
   reject-layers.
2. A layer record whose name field does not lie within its inline_length yields
   **no name at all**: it contributes nothing to the namespace and is
   reject-layer (L23 via `[R-CNT-18]`), not reject-file.

I coded both. Note that L3/L5/L6 (the layer name's own UTF-8, emptiness and C0
rules) are reject-**layer** but detected at **open**, so my open must record a
per-layer verdict rather than raise — the file still opens and its other layers
are still readable. §19.2's tier list and the register agree on this.

### Byte-exact cold remote open

I built a file (below) and instrumented the transport. Cold open against a
ranged server:

```
request 1: bytes=-64          →  64 bytes   (trailer; response carries F)
request 2: bytes=194-341      → 148 bytes   (directory region)
                                 ---
                                 212 bytes, 2 requests
```

Generalised: **2 requests, 64 + dir_length bytes.** What bounds each range
before it is read: request 1 by the permanent 64-byte trailer size
(`[R-CNT-24]`); request 2 by dir_offset and dir_length taken from a
CRC-verified trailer and already checked against `dir_offset ≥ 16`,
`dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64`. Nothing else is fetched:
no extent, no index, no payload (`[R-RDR-01]`). The alternative is one
speculative suffix window plus containment (§6.4), which also picks up the
front-block check for free if the window reaches offset 0.

## 5. Validation timing by tier — what I implemented

Reading §19.2 with §2.3 and `[R-CNF-12]`, the reader's obligations sort as:

**Checked at open (latest):** front block *if resident*; the whole trailer; the
directory CRC and the record walk; the layer-name namespace, including each
layer record's own name validity.

**Checked at first access to a layer (latest):** the layer record entire —
extent slot (`[R-CNT-13]`), the §7.4 constraint set (`[R-CNT-23]`,
`[R-CNT-16]`), exact parse and sub-record walk (`[R-CNT-18]`), sub-record
multiplicity (`[R-CNT-14]`), dimension and channel name rules, the six enum
value sets (§11.4, §12.2, §14.1, §15.1, §17.2, §17.3), bool fill constraint
(§13.2), lz4 decoded-size cap (`[R-COD-07]`), the geometry floor and its
products (`[R-GEO-01]`–`[R-GEO-03]`, `[R-ENC-04]`), and the two index
cross-checks computable without I/O (`[R-CNT-17]`). §19.3 says explicitly that
all of these are decidable from the resident directory and F, and **layer access
performs no fetch**. I verified that claim by implementing it: my
`read_point`'s first I/O is the segment-CRC array.

**Checked at use of a tile (latest):** index chain (crc_of_crc_array, then the
segment CRC), entry classification, payload CRC, decode exactness, decoded size.

**Checked at use of a record's extent (latest):** the extent's terminal CRC and
the document content rules §18.2 attaches at that encoding. Never earlier, since
the open fetches no extent.

**Permitted never to check (as a reader):** every row whose Detector is
*verifier* — 21 of the 121 rows by my count: F7, F25, F26, F27, F28, F33, L18,
L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26. Plus live-state coverage and
the slack total (§9.7), which §5.2's Note says readers never walk. A reader that
detects one of these MAY reject (`[R-CNF-12]`) but owes nothing.

**When a verdict becomes a verdict:** for a reader, at the tier above, and
"reject" prescribes blast radius, not UI. Reject-layer is *prospective* — it
bars further service and does not retroactively invalidate what §19.2's timing
already let the reader return (§2.4). That is the one piece of timing that is
easy to get wrong and the document states it twice (§2.4's table and §19.4 step
8).

## 6. A file built from the document alone, and the reader run over it

I built a conforming file with:

- front block, 16 B at 0;
- one layer `grid`: rank 2, dims `y` (extent 5, tile 4) and `x` (extent 5, tile
  4), interleaved, one uint16 channel `v` with fill `0xABCD`, codec 1, filter 1,
  no alignment, no slab;
- G = (2,2), N = 4, P = 16, Q = 2, decoded size 32; entry_count = 4;
- tiles at disk ordinals 0 and 3 stored, 1 and 2 sentinel;
- index region 4·20 + 4 = 84 B at offset 80;
- a top-level user-metadata record, encoding 1, document
  `{"tarn.title":"grid demo"}` in a 30-byte extent (26 B document + 4 B CRC);
- directory at 194, dir_length 148, pad 42, trailer at 384, F = 448.

Tile 3 is the edge tile covering coordinates 4–7 on both axes: one real position
(4,4) and 15 padding positions, each carrying the fill bytes `CD AB` per
`[R-SER-05]`. Its decoded image is
`2C 00 CD AB CD AB … CD AB` — 32 bytes, which is §14.5's worked example with a
different fill, and my builder produced it independently of that example.

Reader output:

```
(0,0) → stored, 0x0000        (tile 0, in-tile ordinal 0)
(4,4) → stored, 0x002C = 44   (tile 3, in-tile ordinal 0)
(2,3) → stored, 0x0017 = 23   (tile 0, in-tile ordinal 11 = 2·4+3)
(0,4) → fill,   0xABCD        (tile 1 is the sentinel)
(4,0) → fill,   0xABCD        (tile 2 is the sentinel)
(5,0) → request fails as a request, no verdict on the file
```

Sample values were encoded as `10·y + x`, so 44 and 23 are correct, and the two
sentinel tiles return the recorded fill bit-exactly with no payload I/O — which
is `[R-TYP-08]` and §19.4 step 4's short-circuit.

Cold cost of one tile read after open: segment-CRC array (4 B), the segment
(80 B), the payload (32 B) — 3 requests, 116 bytes, the first two parallelisable
(`[R-IDX-04]`). At scale the only term that grows with the layer is the
segment-CRC array, which is §1's claim and §21.9's tile-count guarantee is sized
against it (256 KiB at 2³²).

### The tile-read algorithm as I coded it

1. **Domain.** Point request: 0 ≤ xᵢ < Eᵢ for all i, else the request fails as a
   request with no verdict on the file. Region request: intersect with extents;
   wholly-outside or any region of a zero-extent layer succeeds and returns no
   samples. Note the deliberate asymmetry — a single-position *region* request
   outside the extents succeeds empty, a *point* request at the same coordinate
   fails — and §19.4's opening sentence makes it turn on the request's form, not
   its content. I would have guessed wrong here without that sentence.
2. **Ordinals.** tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; in-tile ordinal
   Σ uᵢ·∏_{j>i} Tⱼ (row-major for *every* linearization, permanently); spatial
   ordinal s = Σ tᵢ·∏_{j>i} Gⱼ under linearization 1; disk ordinal s
   interleaved, c·N + s planar. Empty product is 1, so d = 1 reduces correctly.
3. **Index chain.** CRC array at region byte entry_count·20, length
   ⌈entry_count/2¹⁶⌉·4; verify against crc_of_crc_array (L37). Segment
   sg = k div 2¹⁶ covers entries [sg·2¹⁶, min((sg+1)·2¹⁶, entry_count)) at region
   bytes 20× those; verify against the sg-th u32 of the array (L38). Both ranges
   are computable from the layer record alone, so both fetches can be issued at
   once; both verifications may be cached under committed-prefix immutability.
   Failure at either is **reject-layer**, though the detection point is tile use
   — §19.2 calls this out explicitly and it is the one place where the tier and
   the scope come apart.
4. **Entry.** Classify per §15.3's eight reader rows. Sentinel (S,S,0) → fill,
   short-circuit. Any of the six *structural* rows → reject-tile. The
   sentinel-vs-domain interaction is well handled: `[R-IDX-02]` exempts sentinel
   entries from `[R-ENC-03]`/`[R-ENC-04]`, so all-ones is a reserved pattern and
   not a 2⁶⁴−1 offset, and T11's Condition cell correctly says "the value being
   distinct from the all-ones sentinel". A reader that forgets the sentinel test
   still fails safely, which §15.2's rationale claims and which my
   implementation confirms — all-ones trips both the domain and the bounds
   checks.
5. **Payload.** Fetch [offset, offset+length), verify the entry's crc *before
   decoding* (T1).
6. **Decode.** Codec, then filter inverse (§17.1). `[R-COD-08]` fixes the codec
   output length at exactly the decoded size, and since byte-shuffle preserves
   length, the length check can sit either side of the inverse. In practice I
   check it immediately after the codec, because the inverse shuffle needs L
   divisible by s and §17.3 only guarantees that for a *correct* length. §19.4
   step 6 orders the check after the inverse; that ordering is a presentation
   choice and `[R-COD-08]` decides the substance, so I did not treat it as a
   defect.
7. **Extract.** Interleaved: channel c at in-tile ordinal u sits at byte
   u·Q + Fᶜ. Planar numeric: k·Bᶜ. Planar bool: bit k mod 8 of byte k div 8.
   Padding positions are never returned.
8. **Return.** Bit patterns unaltered. Per-entry failure bounding for
   multi-entry requests: return the good entries plus a per-entry failure
   report, or fail the request whole — but never stand fill in for a rejected
   tile. A step-3 failure takes layer scope and bars the rest of the request
   prospectively.

### Where I had to make a choice the document did not force

Only two, and both are explicitly licensed rather than underdetermined:

- Whether to verify the front block (residency, §6.1/`[R-CNT-04]`).
- Whether a multi-entry request returns partial results or fails whole (§19.4
  step 8's MAY).

Everything else in the reader — every offset, every ordinal, every
classification, every outcome, every tier — came straight out of the text. I did
not have to invent a single value.

## 7. Degradation walks, traced end to end

**(a) Unknown record type, top level, MU = 0, PE = 0.** Type 0x8003 (experimental).
Open: framing parses, type is unknown, MU bit clear → ignore-record
(`[R-CNT-15]`). But its extent slot is *still* validated at open, and a malformed
slot on it is reject-**file** (`[R-CNT-13]`: "the file for other top-level
records"), which surprised me until I saw that §5.2's coverage partition needs
every slot to be a real claimant whether or not anyone reads it. Its extent is
covered by no checksum at all (§8.1's last row), so corruption inside it is
invisible — §22.3 states this as one of its four undefended residues. Still
served: everything. The file is conforming (§21.6), because §10.3's prohibition
on publishing experimental values binds conduct, not bytes.

**(b) Unknown record type, top level, MU = 1.** Reject-file. Nothing served —
`[R-CNF-07]`'s reject-file bars relying on *any* structure. §21.6 records this
as the second of exactly two "conforming files a reader nevertheless refuses",
and stresses that the top-level qualifier is load-bearing: the same type as a
*sub*-record is reject-layer and "never a ground to refuse the file"
(`[R-CNT-18]`). I checked this against §2.3's acceptance clause, which carves
out "carrying no record of a type it does not implement with MUST_UNDERSTAND =
1" without naming a scope. Read alone, §2.3 would let a reader refuse a file
over an experimental MU = 1 *sub*-record. `[R-CNT-18]`'s "a reader MUST NOT
reject the file for it" and §21.6's "the qualifier is load-bearing" both close
it, and §2.3 points at §21.6's closing paragraph. Determined; not a finding.

**(c) Unknown codec value.** Cannot arise for an assigned value — all four
codecs and both filters are core, so software that cannot run one is simply not
a conforming reader (`[R-CNF-03]`, `[R-COD-11]`). A reserved or experimental
codec value → reject-**layer** (L43), detected at layer access from
declarations alone, before any I/O. Still served: every other layer, and the
rejected layer's *name* may still be listed (§2.4). A *verifier* that cannot
execute a codec reports *cannot establish*, not *nonconforming* (`[R-COD-11]`).

**(d) Unrecognized flag / enum value.** Trailer ignore-lane bit (16–31) set:
ignored, file conforming, and an updater must copy it forward (§21.6,
`[R-CNT-08]`). Incompat-lane bit: reject-file (F19). Record flags bits 2–15 set:
readers MUST ignore, verifier records F26/L47. A registered type whose stored MU
or PE differs from the registry: reader applies the *fixed* semantics and serves
the record unchanged; verifier records F28/L49. This is one of the three rows
§21.1 calls out where a verifier-detected violation still obliges the reader to
serve the structure through.

**(e) Truncated tail.** Physical file longer than committed_file_length (the
mid-commit picture in §9.2's crash example): the physical tail is not a trailer,
so the magic or CRC fails → reject-file, and `[R-LIF-05]` forbids scanning
backward. The reader reports the file torn and serves nothing. Recovery is a
separate, deliberate operation (§9.6) that a reader never performs, and its
output must be re-verified as a whole file before use. If the tail *is* a valid
trailer but committed_file_length disagrees with the transport size, F17 fires
in both directions. §9.5's Note explains why residue past a completed commit has
no register row of its own: the reader meets it as one of the trailer gates
already registered, and cannot tell residue from corruption.

**(f) Checksum mismatch, by scope.** Trailer CRC → reject-file. Directory CRC →
reject-file. crc_of_crc_array or a segment CRC → reject-**layer** (detected at
tile use). A stored tile's crc → reject-**tile**; neighbours in the same layer
are unaffected and I confirmed that in my implementation — a bad tile 0 does not
disturb the read of tile 3. A user-metadata extent's CRC → **ignore-record**,
SHOULD be reported; decoding of stored data is unaffected. Crucially, none of
these ever returns fill: `[R-TYP-09]` makes fill the product of exactly one
condition, a sentinel entry read from a verified chain, and `[R-CNF-09]` forbids
standing fill in for a rejection. I coded the sentinel test and the malformed
tests as disjoint branches for exactly that reason.

**(g) Limit exceeded.** A file whose rank is 200, or whose one tile decodes to
1 GiB: still conforming (the hard limits are 255 and none respectively), but it
exceeds a §21.9 minimum guarantee, so a reader MAY decline it — at the whole
file, or at the narrowest scope whose declarations exceed what it can serve, a
layer or a tile — and the refusal MUST be reported *as a resource limit and not
as a validity error*. Conversely, declining on that ground a file whose every
table quantity is within bounds makes the software non-conforming. See finding
reader-01 for what this does and does not reach.

**(h) Format major it does not implement.** version_major = 7: reject-file on
capability grounds, and the diagnostic SHOULD be distinct from both "not a TARN
file" and "corrupt". The file is neither conforming nor nonconforming under this
text; the refusal is not a finding about its bytes. §21.2's preamble is careful
about which file-scope rows still reach such a file: only F8, F14, F6 and F1's
two instances, because their subjects are fields §6.2 validates before the
version gate or `[R-CNT-24]` fixes across all majors. I checked the count: F1,
F6, F8, F14 — four rows, as stated. F18 (version_major = 0) is outside the
premise rather than an exception, and the text says so.

## 8. Where I went looking after the five flagged passages

Per the brief I read §18.2, §21.5, §21.7, §21.8 and §21.9 first and hardest,
then spent the bulk of the walk elsewhere. Things I checked and found sound,
recorded so the next round does not redo them:

**Checksum coverage is complete.** I enumerated every field of every structure
against §8.1's map and §4.5's exceptions. Trailer fields ← trailer CRC.
Directory record sequence ← directory CRC. Index entries ← segment CRCs. Segment
CRC array ← crc_of_crc_array. crc_of_crc_array (living in the layer record's
inline payload) ← directory CRC. Stored tile bytes ← the entry's crc field.
User-metadata encoded bytes ← the extent's terminal CRC. Terminal checksums
themselves and the front block are the stated exceptions; an unassigned type's
extent is the stated hole. Nothing is uncovered that the text does not name.

**The register is complete.** I walked all ~110 requirement identifiers and
asked for each whether it names a detectable file-conformance violation and, if
so, which row carries it. Every one resolves: to a row, to a SHOULD (outside the
register by `[R-CNF-12]`), to a conduct rule (§2.3, §10.3, §18.3), to reader
behaviour with no file state, or to §21.7's unwitnessed classes. I found no
missing row.

**The chain of trust closes.** `[R-ENC-05]` forbids acting on an unverified
integer. Every integer I act on is covered: dir_offset/dir_length by the trailer
CRC; the layer record's extent slot and entry_count by the directory CRC; the
segment CRC array's location by entry_count (directory-covered); an index
entry's offset/length by its segment CRC (which is covered by
crc_of_crc_array, which is directory-covered). There is no point in the open or
the tile read where I must seek on an unchecked value.

**Degenerate-but-legal files I constructed on paper and found determined:** a
zero-extent dimension (N = 0, entry_count = 0, extent slot (0,0),
crc_of_crc_array = 0, index region absent entirely — §15.4's last example says
so); entry_count exactly 2¹⁶ (one full segment, the constant `0xEECB3BB2`
usable) and 2¹⁶+1 (a partial second segment whose CRC MUST be computed);
A = 2⁶² (legal, but only satisfiable with zero stored tiles — and
`[R-SLB-03]`'s "a run with no stored tiles imposes nothing" makes the analogous
slab case vacuous rather than broken); S > N (one run per block, the final run
short); dir ending exactly at F − 64 (zero pre-trailer pad, explicitly
conforming); an empty directory (Appendix A). Each is determined, and §17.2's
Note about codec 4's cap in an empty layer is the sharpest example of the
document having already thought about this class: it distinguishes the cap
(quantified over addressed tiles, so vacuous) from `[R-ENC-04]`'s overflow rule
(unquantified, so still binding on P·Q in an empty layer).

**Argument-by-analogy audit.** I put the governing verbs side by side for every
"exactly as", "the same way", "for the same reason", "transposed", "likewise",
"on the same terms" in the document (18 sites). The two that carry weight:
§18.2's "exactly as `[R-COD-11]` requires of a codec it cannot execute" — and
`[R-COD-11]` does say "cannot establish that layer's conformance and MUST NOT
certify the file", so the transposition to a document holds; and §21.9's "ranges
over a layer's **addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap
is" — and `[R-COD-07]` does say "any of whose **addressed** tiles' decoded
size", so that one holds too. Neither analogy is unsound for a member of its
set.

**§21.7's second-paragraph asymmetry.** §21.7's first paragraph ends with an
explicit disclaimer that none of its items is a requirement a verifier is
"unable to check" within `[R-CNF-11]`'s meaning; the second paragraph carries no
such sentence. I chased whether that could force *cannot establish* on every
file, and it cannot: `[R-CNF-11]` triggers only on inability "on a capability or
resource ground", and the second paragraph's obligations fail for a different
reason (no witness exists). The qualifier appears three times in §2.3 and is
load-bearing. Sound.

**Reader-facing arithmetic that could have forked and does not.** Q includes
bool at element size 1; the shuffle stride is Bᶜ planar, Q interleaved, and 1
(identity) for a packed bool plane, and L is divisible by s in all three cases;
decoded size is ⌈P/8⌉ only for a *planar bool* tile and every other case is the
§14.2 table; the in-tile ordinal is row-major for every linearization
permanently. All determined, and §14.4's note about a single-channel bool layer
producing different bytes under the two layouts is the check that the two
formulas are meant to differ.

## 9. Findings

Three. None byte-level, and I say so honestly rather than reaching: I could not
construct a case where two competent implementations reading this text disagree
about a byte on disk or an accept/reject verdict. The calibration says the base
rate is not zero, so I want to be clear that this is a result and not a shrug —
I built the reader, ran it, checked every constant, counted the register
mechanically, and walked eight degradation paths, and the document determined
all of it.

---

### reader-01 — AMBIGUITY

**§21.9 (limits table and its individuation paragraph), `[R-ERR-03]`,
`[R-ERR-04]`, `[R-CNF-10]`; §17.2's Note under `[R-COD-08]`; §18.2
(`[R-MTA-09]`)**

**The table bounds a stored structure's *decoded* size and its frame's window
but nothing bounds the *stored* byte length a reader must fetch and checksum to
get at either, and §17.2 points at §21 for exactly that bound.**

Quoted, §17.2's Note under `[R-COD-08]`:

> For the compressing codecs (2–4), no bound relates a stored length to its
> decoded size in either direction — codec 1's equality is `[R-COD-04]`'s
> subject. Compression may expand, and a reader allocates from declarations,
> never from stored data or embedded size fields. **Resource limits are §21's
> subject.**

Quoted, §21.9:

> The last three rows are **per-instance**, and are individuated differently.
> […] The other two range over the user-metadata documents and compressed frames
> a file actually contains, **neither of which exists except as stored bytes**.

Quoted, §21.9 `[R-ERR-04]`:

> A file exceeding any of these remains conforming, and a reader MAY decline
> it — at the whole file, or at the narrowest scope whose declarations exceed
> what it can serve, a layer or a tile. Software that declines **on that ground**
> a file whose every quantity lies within the table is not a conforming reader
> (`[R-CNF-03]`) […]

Take the structure and list what it can carry. A **stored tile** carries a
stored extent of some *length* and decodes to a *decoded size*. §21.9 bounds the
decoded size (256 MiB) and the zstd frame's `Window_Size` (8 MiB); nothing
bounds the stored length. The only constraints on it anywhere are §15.3's
`length ≥ 1`, `length ≤ 2⁶³−1` and `offset + length ≤ F − 64`. §19.4 step 5
obliges the reader to fetch the whole extent and verify its crc *before*
decoding, so the mandatory per-tile I/O is unbounded by anything except F. A
deflate stream of arbitrary length decoding to a few hundred bytes is trivially
constructible (empty stored blocks), and §21.6 already records "under a
compressing codec, a stored tile's decoded size differs from its stored length"
as an *expected* condition, so this is a shape the document contemplates.

The **user-metadata record** is the same shape and sharper, because §18.2 gives
the reader an explicit bound-of-its-own for two of the three quantities and
floors each at a §21.9 row —

> Under either encoding a reader decodes with a bound of its own choosing, **no
> smaller than §21.9's user-metadata guarantee** […] a reader's window bound is
> its own, **no smaller than §21.9's guarantee for that quantity**

— and says nothing about the third, the extent's stored length, even though
§18.2 elsewhere treats that length as a reportable quantity ("the verifier
SHOULD report the bound it applied and **the stored length of the extent it
declined**"). §8.2's ordered chain forces the extent CRC before any decode, so a
reader that surfaces metadata at all must read every byte of the extent before
its decoded-size bound can even come into play.

**Permitted readings.** (i) The reader's only sanctioned bounds are the two
§18.2 names; `[R-ERR-04]`'s "declines on that ground a file whose every quantity
lies within the table" makes any resource decline on a within-table file
non-conforming, so a conforming reader may not cap stored-extent length at all.
(ii) `[R-CNF-10]`'s "Readers MAY enforce resource limits" and §18.2's
"ignore-record like any other **it cannot read**" together let a reader treat an
over-large stored extent as unreadable and take ignore-record, since §21.9's
table cannot measure a quantity it has no row for.

**Which I picked and why.** (i). §21.9's licence to decline attaches to
"exceeding any of these", and §2.5's `[R-CNF-10]` says a reader "MUST accept any
conforming file within the minimum guarantees stated in §21's limits table" —
"within the guarantees" reads most naturally as "exceeding no row". So my reader
enforces no cap on a stored tile's extent and streams the CRC and the decode.
For the metadata half I still take reading (i) but with less confidence, because
"like any other it cannot read" is genuinely open-ended.

**What an implementer does wrong without it.** A reader that caps how many bytes
it will fetch for one tile — the first resource limit any real implementation
adds — is non-conforming under reading (i), and it will fail a corpus vector
built at any stored length above its cap. §17.2's Note sends that implementer to
§21 for the bound, and §21 has no row for it. On the metadata side the two
readings differ in whether the record is served or ignored.

**Byte-level: no.** Under either reading the file is *accepted*; only whether a
quarantined metadata record is served differs, and `[R-MTA-02]` makes that
incapable of moving any sample byte. For the tile half the text determines the
answer (must serve), so competent implementations should not diverge. What
resolving it would change is which resource limits a conforming reader is
allowed to have — a real cost, but not the emittable set and not a verdict.

---

### reader-02 — OBSERVATION

**§21.7 (`[R-ERR-01]`), read against §20.5 (`[R-WRT-06]`) and §2.3
(`[R-CNF-02]`)**

**§21.7 accounts for two of `[R-WRT-06]`'s four obligations on a compacted
file's trailer and leaves the other two — both MUSTs, both equally unwitnessed —
in neither of the document's two buckets.**

Quoted, §21.7:

> §20.5's **two** obligations on a compacted file's trailer (`[R-WRT-06]`) — the
> unknown ignore-lane bits it MUST carry forward, and the floor its
> version_minor SHOULD take — are unwitnessed for that same reason, the output
> carrying no record of its input's flags or its input's minor

Quoted, §20.5 `[R-WRT-06]`:

> It MUST mint a fresh file_id for the output — a new draw under §9.3's
> randomness advice, not merely a value compared against the input's — and
> generation 1

`[R-WRT-06]` places four obligations on the output's **trailer**: a fresh
file_id, generation 1, the input's unknown ignore-lane bits carried forward, and
a version_minor floor. All four are unwitnessed in the output alone — a
compacted file at generation 7 carrying its input's file_id passes every check
in §6.2, and nothing in the file records that it is a compaction output at all.
§21.7 names the last two and calls them "two obligations on a compacted file's
trailer", which reads as the complete set for that trailer.

§2.3 supplies the other bucket: obligations that "govern their *conduct* rather
than their output […] and a file is never nonconforming by virtue of one",
declared "where [they arise] rather than enumerated here". §20.5 does not declare
the file_id or generation obligations to be conduct rules. So an implementer
asking "is a compacted file that reuses its input's file_id nonconforming?"
finds no answer: not in §21.7's account (which passes over it while accounting
for the adjacent obligations), and not in §2.3's conduct list (which §20.5 never
opts into).

§21.1 calls §21.7 "the account, by class, of what fails" detectability, and
§21.7's own framing — "A second set of obligations is omitted from the register
because a single file exhibits no witness of their violation" — reads as an
enumeration. Where it enumerates by identifier (as it does for §20.5) rather
than by class, omitting a sibling MUST of the same structure and the same
character is a gap in the account.

**Byte-level: no.** Nothing about either obligation is checkable from a single
file, so no verdict moves under either classification, and `[R-CNF-11]` limits
*cannot establish* to capability and resource grounds, which neither is. What is
at stake is whether a verifier's report and a compactor's self-audit should treat
a reused file_id as a violation of the output or as misconduct by the tool.

---

### reader-03 — OBSERVATION

**§18.2 (`[R-MTA-09]`) and §21.5 row R4, against `[R-COD-06]`**

**The content-size constraint is justified as "checkable from the bytes alone"
and "not a failure to decode", but establishing it requires the decoded
document's byte length, which the extent's bytes do not carry — so the routing
rests on the very decoder tolerance it says it avoids depending on.**

Quoted, §18.2:

> The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal
> the byte length of the decoded document. A mismatch is one of the frame
> constraints R4 registers, not a failure to decode under R3: **the bytes
> decode**, and what is wrong is what the header said about them. Routing it to
> R4 **keeps the condition checkable from the bytes alone rather than turning on
> a decoder's tolerance** (`[R-CNF-02]`) — the tile rule of `[R-COD-06]`
> transposed to the quantity a document does have, its decoded length, in place
> of the declared size it does not.

Quoted, §21.5 row R4:

> unlike R3, a constraint of this row is broken by what the frame declares
> rather than by whether the bytes decode, so **a reader that only tries
> decoding establishes none of them**

The transposition from `[R-COD-06]` is not like-for-like, and the analogy is
where it slips. For a tile, `[R-COD-06]` compares the frame's declared content
size against *the layer's declarations* — the decoded size "comes from the
layer's declarations alone", so the check is pure header inspection and
`[R-COD-06]` can fairly call it "header-checkable" and place it before any
decode. For a document there is no declaration to compare against; §18.2 pins
the field to "the byte length of the decoded document", a quantity that exists
only once the frame has been decompressed. So the condition is *not* checkable
from the extent's bytes alone in the sense the tile rule uses, and a reader that
"only tries decoding" is in fact the only kind of reader that can obtain the
comparand at all.

The premise "the bytes decode" is doing the load-bearing work, and it is an
assertion about decoder behaviour that the document supplies rather than
Appendix F's normative reference. (My suspicion — offered as a suspicion only,
since I could not consult RFC 8878 — is that a decoder which refuses a frame
whose produced size disagrees with a present Frame_Content_Size is the ordinary
case rather than an intolerant outlier. If so, "the bytes decode" is false for a
typical implementation, and a reader following R4's instruction not to rely on
decoding has no other route to the comparand.) Either way the justification is
self-undercutting on its own terms: it claims independence from decoder
tolerance for a check that cannot be performed without a successful decode.

**Permitted readings I can defend.** (a) The reader must obtain the decoded
length by whatever means — an FCS-ignoring or streaming decode — and report R4.
(b) A reader whose decoder refuses the frame has a decode failure and reports
R3, §18.2's "the bytes decode" simply not describing its decoder. I picked (a),
because §18.2 states the routing in the imperative and R4's Detector is *reader*,
so `[R-CNF-04]` obliges the check; I noted in my implementation that this means
the metadata path needs a decode mode that does not abort on FCS mismatch.

**What an implementer does wrong without it.** Nothing observable, which is why
I grade this low: R3 and R4 are both ignore-record, both reader-detected, both
at extent use, and both make the file nonconforming, so a verifier's verdict is
the same either way. The cost is corpus attribution (a vector built for an R4
content-size instance may be reported as R3 by a strict-decoder reader) and a
non-obvious constraint on which zstd API a reader may use for metadata.

**Byte-level: no.** The two candidate rows carry the identical outcome, detector
and detection tier, so no accept/reject verdict and no byte moves. The
divergence is confined to which row a report names.

## 10. Confidence

High that an implementation built from this text alone would interoperate on the
reader path. I built one and it read a file I built from the same text, with
every offset, ordinal, sentinel, fill and checksum agreeing on the first try,
and only two choices left open to me — both explicitly licensed. The
document's own constants, offsets and worked examples are without error, and
§21.8's stated total of 121 conditions over 277 instances is mechanically
correct against the register as written.
