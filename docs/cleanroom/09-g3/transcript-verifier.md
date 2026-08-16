# Round 9 — Verifier implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five sequential `Read` calls covering lines 1–3893 (the whole document). I ran
`grep` against that file three times (for `verifier` + MUST/SHOULD/MAY, for
`informative`, and for `| semantic |`). I ran five Python scripts of my own
authorship in a scratch directory, reading no project files: a CRC-32C
implementation, a check of the document's worked numeric examples, a builder that
lays out a TARN file of my own construction and runs the coverage walk on it, a
four-generation trace, and an adversarial-layout checker for extent overlap,
alignment and slab invariants. I also parsed the §21.2–§21.5 register tables out
of the spec text itself to count rows and instances mechanically.

I did not open `docs/`, `conformance/`, `spec/registry.json`, `PLAN.md`,
`AGENTS.md`, `README.md`, `OPEN-QUESTIONS.md`, or any ADR. I ran no `git`
command, no web search, no web fetch, and did not list any directory to discover
what else exists. Prior knowledge of other array/image formats was used only to
generate suspicions (e.g. "does this document pin the DEFLATE final-byte padding
bits?" — it does address it, §17.2's first note); every conclusion below is
sourced to a quotation from this document.

---

## 1. What I set out to build

A conforming verifier, per §2.3's fifth class: "A reader that additionally checks
every file-level requirement — including those ordinary readers are exempted
from — and certifies conformance." So the verifier is a superset of the reader of
§19, plus the twenty register rows whose Detector cell reads *verifier*, plus the
coverage walk of §9.7, plus the slack total of §5.2.

I worked in this order: (a) reproduce the checksum constants, because if my CRC is
wrong nothing else I compute means anything; (b) reproduce every worked numeric
example in the document, as a sanity check on my reading of the geometry and
serialization arithmetic; (c) build a file, walk it, do the slack arithmetic;
(d) break that file three ways and check overlap/alignment/slab; (e) run four
generations through create → append → update → compact; (f) audit the register
mechanically; (g) then go looking for the places where I had had to guess.

---

## 2. The certification procedure, as an ordered algorithm

I derived this from §2.3 (`[R-CNF-11]`), §2.4 (`[R-CNF-07]`–`[R-CNF-12]`), §9.7
(`[R-LIF-08]`), §19.1–§19.4, §5.2 (`[R-CNT-21]`), §17.4 (`[R-COD-11]`) and §18.2
(`[R-MTA-09]`). Every step names the outcome of failure and what happens when the
step cannot be run at all.

**Verdict vocabulary.** Three verdicts, and two report-only labels that are *not*
verdicts:

| Token | Kind | When |
|---|---|---|
| *conforming* | verdict | traversal complete, no violation established, no requirement left unchecked |
| *nonconforming* | verdict | **any** violation established, at any scope, however many requirements went unchecked |
| *cannot establish* | verdict | no violation established, but ≥1 requirement unchecked on a capability or resource ground |
| *unexamined* (per scope) | report | verifier elected to stop at the first violation (§2.3) |
| *partial* (slack total) | report | the §9.7 walk did not enumerate every region's claimants (`[R-CNT-21]`) |

The priority rule is explicit and I leaned on it repeatedly: "An established
violation takes priority: a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check, and *cannot
establish* is available only to a traversal that established no violation."

Two consequences I had to work out rather than read:

* *unexamined* can only ever co-occur with *nonconforming*. It is licensed only by
  "A verifier MAY stop at the first violation it finds", so by construction a
  violation exists. It never accompanies *conforming* or *cannot establish*.
* An **ignore-record** outcome still bars certification. §21.5's preamble: "Every
  row here is a violation all the same: the outcome bounds a reader's blast radius
  and never makes the file conforming (`[R-CNF-12]`)". So a verifier that finds a
  user-metadata document with duplicate keys (R9) reports *nonconforming* even
  though every reader is told to carry on. A naive verifier gets this backwards;
  the document is unambiguous.
* A **SHOULD** deviation is an advisory and does not bar certification
  (`[R-CNF-12]`: "a verifier reports a SHOULD deviation as an advisory that does
  not bar certification"). But `[R-MTA-05]`'s member ordering is a **MUST**, and
  its violation *is* registered (F29/L49) — I initially mis-shelved it as advisory
  because readers process the document unchanged, and had to re-read line 2418:
  "the file is nonconforming, a verifier MUST report it, and readers process the
  document unchanged."

### The algorithm

**Phase 0 — bytes.** Obtain the physical size (transport-authoritative,
`[R-CNT-10]`). Fewer than 128 bytes → F7, reject-file, *nonconforming*
(`[R-CNT-27]`).

**Phase 1 — front block, [0,16).** Byte-equality against
`89 54 41 52 4E 0D 0A 1A` + 8 zero bytes. Mismatch → F8 (F2 if byte-reversed),
reject-file.

> Decision I had to make. `[R-CNT-04]` lets a reader that "would have to issue a
> further range request to obtain those bytes ... defer or omit the check", and F8
> restates that carve-out. Does a *verifier* inherit the exemption? I concluded no.
> §2.3 defines the verifier as checking "every file-level requirement — including
> those ordinary readers are exempted from", and this is precisely such an
> exemption; §9.7 also puts [0,16) in the walk as a member of the live committed
> state. So my verifier makes those bytes resident unconditionally. Appendix H's
> verifier checklist does not name the front block among "the checks readers are
> exempt from" — a summary omission, not a rule, and §2.3 governs.

**Phase 2 — trailer, [F−64, F).** In §6.2's *fixed order*, and the order matters:

1. magic (F10/F2);
2. trailer CRC over [0,60) (F16);
3. version gate (F20 for major 0; unimplemented major → **cannot establish**, not
   nonconforming, per §2.3's first bullet and §21.6's closing paragraph);

only then the rest: flags (F21 incompat lane set → reject-file; ignore lane →
§21.6, conforming, ignored), committed_file_length = size and ≡ 0 mod 64
(F19/F15), dir_offset ≥ 16 (F11), dir_length ≥ 4 (F18), dir_offset + dir_length
≤ F−64 (F12), 1 ≤ generation ≤ 2⁶³−1 (F13/F3), file_id ≠ 0 (F14), reserved zero
(F17).

`[R-CNT-24]` is what makes step 3 safe across majors: only magic, version fields
and the CRC at F−4 have positions fixed in every major, and §6.2 says exactly that
("only these touch fields whose positions are fixed across all majors"). So a
major-2 file with a bad trailer CRC is *nonconforming* (the CRC is judgeable), while
a major-2 file with dir_offset = 8 is *cannot establish* (that field may not be
dir_offset at all under major 2). I checked this pairing carefully; it works.

A torn file — the physical tail is not a valid trailer — is F10/F19, reject-file,
*nonconforming*. §9.6 confirms this is the right reading rather than a recovery
scan: "a file whose final 64 bytes are not a valid trailer fails `[R-CNT-06]`'s
gates on the bytes handed over (§21.2 rows F10 and F19), and the earlier state the
probe finds is a different artifact". The backward probe is *diagnosis* for a
verifier, "not a finding about the file it was given"; no verdict turns on it. My
verifier runs it only to print "recoverable to generation n at offset o".

**Phase 3 — directory region.** Verify the terminal CRC over dir_length − 4 bytes
*before any other use* (F22, `[R-CNT-11]`). Then parse the record sequence: exact
parse, no residue (F31); type 0 (F26); multiplicity (F36); unknown top-level types
by MU bit (F37 reserved+MU=1; reserved-range at all → **F38, verifier-detected**);
extent-slot validity for non-layer top-level records (F32/F33/F34); user-metadata
framing — no (0,0) slot (F23), extent_length ≥ 5 (F24), inline_length exactly 1
(F25). Verifier-only additions here: F27 (MU=1 with PE=0), F28 (reserved flag bits
2–15), F30 (a registered type's stored MU/PE against §7.3's fixed values). Build
the layer-name namespace over *raw bytes*, uniqueness decided first and
independent of well-formedness (§19.1 step 4) → F6.

**Phase 4 — per layer, full record validation** (§19.3, `[R-RDR-03]`), no I/O:
L1–L18, L20–L37, L40, L44–L46 plus verifier-only L47/L48/L50, and L26 for a
reserved-range sub-record type. All decidable from the resident directory and F.

**Phase 5 — per layer, index chain.** crc_of_crc_array (L38), then every segment
CRC (L39). `[R-ENC-05]` forbids seeking on any entry field before the checksum
covering it verifies, so a failure here **blocks** everything downstream for that
layer — this is the case that makes the walk incomplete, and I treat it as such.
Then classify every entry per §15.3 (T6–T12, T27), not just the ones a reader
would use.

**Phase 6 — per stored tile.** Fetch, verify the entry crc (T1), then decode
(T3, T13, T14–T25 by codec), then screen decoded content: T4 (padding positions
carry fill), T5 (pad bits carry the fill bit), T2 (interleaved bool bytes at real
positions), T26 (mis-strided filter, detected through T2/T4).

**Phase 7 — whole-file, verifier-only.** F9 (a structure in the pre-trailer gap),
F35 (cross-scope overlap), L19 (intra-layer overlap), L41 (per-tile alignment),
L42/L43 (slab packing and run-head alignment).

**Phase 8 — extents.** Every user-metadata extent's terminal CRC (R2), decode
(R3/R4), then document rules (R5–R10) and member ordering (F29/L49).

**Phase 9 — report.** Verdict; the slack total (partial or not); every requirement
left unchecked with its ground; every scope left unexamined.

### What bars certification, exhaustively

1. Any established violation → *nonconforming*.
2. Inability to execute a layer's codec or filter → §17.4: "cannot establish that
   layer's conformance and MUST NOT certify the file."
3. Declining a layer's or tile's decode on resource grounds (`[R-ERR-04]`).
4. Declining to decode a user-metadata document (`[R-MTA-09]`), which additionally
   asks the verifier to report the bound it applied and the declined extent's
   stored length.
5. An unimplemented format major.
6. An unimplemented MU = 1 record type (§21.6).

And what does **not** bar it: a SHOULD deviation; a set ignore-lane flag bit; an
experimental-range record type with MU = 0; an experimental-range user-metadata
encoding; an unrecognised `tarn.` key; a standardized key out of scope or
off-shape; slack of any size, including a pre-trailer gap longer than 63 bytes
(`[R-CNT-05]`: "a longer gap is conforming, and no conforming commit produces
one"); and every §21.7 condition, which "is [not] a requirement a verifier is
*unable to check* within the meaning of `[R-CNF-11]`: no file-level witness exists
to check, so nothing about the file is left undetermined and the verdict is
unaffected." That last sentence saved me a wrong answer: I had first supposed a
wrong-sample-value file forced *cannot establish*. It does not.

---

## 3. The coverage walk on a file of my own construction

Layer `L`: interleaved, d = 1, dimension `x` with E = 4, T = 2 → G = 2, N = 2,
P = 2. One channel `v`, uint16 (type 7), fill `00 00`. Codec 1, filter 1,
linearization 1, no alignment, no slab. Q = 2, decoded size P·Q = 4. Tile 0 stored
(`11 11 22 22`), tile 1 the sentinel. entry_count = N = 2; index extent_length =
2×20 + ⌈2/2¹⁶⌉×4 = 44 (`[R-CNT-17]`, which I checked by hand and by script).

Layer-record inline payload, packed in §7.4's table order with no padding:

```
name          1 + 1  = 2      "L"
layout        1             = 1 (interleaved)
linearization 2             = 1
codec         2             = 1
filter        2             = 1
A             8             = 0
S             8             = 0
A_slab        8             = 0
rank d        1             = 1
C             2             = 1
dim entry     1+1 + 8 + 8 = 18    "x", E=4, T=2
chan entry    1+1 + 2 + 1+2 = 7   "v", type 7, fill 00 00
index_encoding 1            = 1
entry_count   8             = 2
crc_of_crc_array 4
sub-records   0
                        total 74
```

Record = 24 + 74 = 98. Directory region = 98 + 4 = 102 at dir_offset 64.

**Layout and walk (generation 1), F = 256:**

```
  [     0,    16)     16  front signature block
  [    16,    20)      4  stored tile L#0
  [    20,    64)     44  L tile-index region  (= the layer record's extent)
  [    64,   166)    102  directory region
  [   166,   192)     26  pre-trailer pad  -> SLACK
  [   192,   256)     64  live trailer
  claimed (union) = 230   F = 256   SLACK = 26
```

Every check in the walk: disjoint ✓; every claimant inside [16, F−64) ✓ (§9.7);
every claimant checksum-verified where §8.1 maps one ✓; nothing in the gap between
directory end and trailer ✓ (F9); F ≡ 0 mod 64 ✓; F = physical size ✓.

Three things I had to settle to do this at all, and where I settled them:

* **The index region is claimed once, not twice.** §9.7: "A layer record's extent
  slot addresses that layer's tile-index region (§7.4), so the region enters the
  walk once, as that record's extent, and is not a second claimant beside it."
  Without that sentence I would have double-claimed 44 bytes and reported slack
  as −18.
* **Records are not a coverage class.** §5.2's classes are front block, stored-tile
  extent, record extent, directory, trailer. The record *headers and inline
  payloads* are claimed by the directory; the walk enumerates them only to reach
  their extents. So a layer record's 98 bytes are not a separate claimant.
* **The front block and the trailer are claimants.** §9.7 says so explicitly, and
  says the [16, F−64) bound on everything else is what keeps them disjoint.

### Which bytes are certified, which are counted-but-unconstrained, and whether any byte can be neither

*Certified*: every byte of the live committed state — 230 of 256 here. Of those,
every byte is covered by exactly one checksum with four stated exceptions (§4.5,
§8.1): the front block (equality, not a checksum); the three terminal checksum
fields (trailer [60,64), the directory's final 4 bytes, a user-metadata extent's
final 4 bytes) which are comparison-verified and covered by nothing further; and
**the extent of a record of a type this specification has not assigned**, which
§8.1's map covers "none — the bytes are opaque (§7.2)".

So the answer to my charter's question "is every live structure covered by a
checksum?" is **no, and the exception is named**: an unassigned-type record's
extent. §22.3 confirms the consequence rather than hiding it: "The extent of a
record of a type this specification has not assigned is covered by no checksum
either (§8.1), so corruption inside it is equally invisible." Those bytes are
certified only for *placement* — in bounds, disjoint, claimed — never for content.

*Counted but unconstrained*: slack. 26 bytes here. "Slack has no internal structure
this specification defines, its content is unconstrained, and no conformance
requirement applies to it."

*Neither*: in a **complete** walk, no byte. §5.2's Note settles this by definition
rather than by check — "The live committed state is *defined* as the front block
plus what a complete coverage walk reaches, and `[R-LIF-08]` makes every byte that
walk misses slack — so 'belongs to no class' describes nothing, and a register row
for it would be a row no file could exhibit." In an **incomplete** walk, yes:
bytes inside unwalked regions are neither certified nor inside the partial total,
and are accounted for only by the separate obligation to "name the regions it did
not walk and report their byte extent." That second accounting is where I ran into
trouble — see §7 below.

An entry that §15.3 classifies reject-tile on a *structural* ground is the one case
where a byte range is nominally addressed and yet falls to slack: §9.7 — "the walk
passes over it, and the bytes it nominally addresses fall to slack (§15.3)" — and
§15.3's own, more careful form, "any bytes it nominally addressed that no other
claimant claims fall to slack." I used §15.3's version; §9.7's shorter phrasing
would, read alone, put front-block bytes into slack when an entry has offset < 16
(T8), which §15.3's qualifier rules out. §21.1's "where a row and the rule it cites
diverge, the rule governs" is about rows, but the same principle plainly applies to
the fuller of two statements of one rule, and §9.7 cites §15.3 for it.

Note the walk stays **complete** in that case. §9.7: "An entry `[R-IDX-03]`
classifies reject-tile on a *structural* ground does not make the walk incomplete."
So the file is *nonconforming* (T6–T12 are violations) but the slack total is a
full total, not a partial one. That pairing is unusual and I checked it twice.

---

## 4. Adversarial layouts: overlap, alignment, slab

Abstract statements of these invariants are cheap; I broke a real layout for each.

### ADV-1 — intra-layer overlap

Same layer `L`, but the extent slot moved to (19, 44) so the index region occupies
[19, 63) while stored tile 0 occupies [16, 20). One byte, 19, has two claimants
inside one layer.

Detected: `[R-CNT-13]` — "a verifier MUST treat an intra-layer overlap — including
a stored extent overlapping its own layer's index region or sub-record extents —
as reject-layer" — and §15.3's row, and L19. Outcome reject-layer, verdict
*nonconforming*. Readers do not detect it: "(readers are not obligated to detect
overlap, which requires whole-directory knowledge)".

Had I instead pointed the tile at the *directory* region, the same byte collision
crosses scopes and becomes F35, reject-file. The split is stated cleanly:
intra-layer → reject-layer, "any overlap across layers or touching another scope's
structures" → reject-file.

Slack under overlap is still well defined: |union| rather than the sum. §5.2 says
slack is "Every byte the live state does not claim", and §9.7 "Bytes the walk does
not reach". Union semantics, so a double-claimed byte is claimed once and slack does
not go negative. I verified this in the script.

### ADV-2 — alignment

`L` declares A = 512 and places its one stored tile at offset 16.
16 mod 512 = 16 ≠ 0 → `[R-SLB-01]` violated, L41, reject-layer, verifier-detected.
"readers are not obligated to — offsets are always explicit, so alignment is
reader-invisible."

The interaction that matters: an entry that is structurally reject-tile is **excluded**
from this check. §15.3 — "Such an entry contributes no stored extent to the
*verifier* rows, which bind over well-formed entries' extents only" — while an entry
whose only defect is a failed crc is *included*, because "the defect lies in the
bytes it addresses, not in the entry, so its extent stands". I built the exclusion
into the classifier before running the alignment and slab checks.

### ADV-3/4/5 — slabs

Layer `B`: planar, C = 2, d = 1, E = 8, T = 2 → G = 4, N = 4, entry_count = C·N = 8.
Channel type uint8, P = 2, planar-numeric decoded size P·B = 2. S = 3, A_slab = 16.

Run partition from `[R-SLB-02]`, which I had to read twice because runs partition
*blocks*, not the whole ordinal space: blocks are [0,4) for channel 0 and [4,8) for
channel 1; run r of a block starts at block_start + r·S; "runs never span channel
blocks, and the final run of a block can cover fewer than S ordinals". So:

```
block 0: run0 = ordinals {0,1,2}   run1 = {3}
block 1: run0 = ordinals {4,5,6}   run1 = {7}
```

Conforming placement (ordinal 1 is a sentinel):

```
run {0,1,2}  stored 0@256 2@258        first 256, 256 mod 16 = 0   packed 256+2=258 ✓
run {3}      stored 3@272              first 272, 272 mod 16 = 0   ✓
run {4,5,6}  stored 4@288 5@290 6@292  first 288, 288 mod 16 = 0   packed ✓
run {7}      stored 7@304              first 304, 304 mod 16 = 0   ✓
```

The sentinel at ordinal 1 is transparent: ordinal 2 sits at 258, immediately after
ordinal 0. "Sentinel tiles are transparent to run continuity: they occupy no bytes
and do not break packing."

Broken version: ordinal 6 moved to 294 (a 2-byte hole after ordinal 5's end at 292)
→ **L42**; ordinal 7 moved to 306, 306 mod 16 = 2 → **L43**. Both reject-layer,
verifier, certification.

Then the subtle one. I made ordinal 5 structurally invalid (length 0 → T10). Now
the run's stored tiles are {4, 6}, and the packing relation demands
offset(6) = offset(4) + length(4) = 290. Ordinal 6 still sits at 292, so **L42
fires as well**. That is exactly what §16.2 prescribes — "So are the entries §15.3
classifies reject-tile on a *structural* ground: they address no usable extent, and
the run's stored tiles close over them" — and it means one corrupt entry yields two
register rows, which §24 anticipates ("where a condition cannot be isolated ... the
entry records every row the file exercises").

The design point I want to record, because it is genuinely well made: the
crc-failing entry is deliberately *not* transparent, "so this invariant stays
decidable from index bytes alone." If crc-failing entries were transparent, a
verifier could not check L42 without fetching every payload. As written it can.

---

## 5. Checksum obligations, and the constants

Coverage map (§8.1), and whether each is verified by comparison, by a further
checksum, or not at all:

| Structure | Checked by | Itself covered by |
|---|---|---|
| front block | byte equality | — (no checksum, by rule) |
| trailer [0,60) | trailer CRC at [60,64) | — (terminal) |
| directory region | its final 4 bytes | — (terminal) |
| tile-index entries, per segment | that segment's u32 in the CRC array | crc_of_crc_array |
| segment CRC array | crc_of_crc_array | the directory CRC (it lives in the layer record) |
| crc_of_crc_array | comparison | the directory CRC |
| stored tile bytes | its entry's crc field | — (entry's crc is covered by the segment CRC) |
| user-metadata extent | its final 4 bytes | — (terminal) |
| unassigned-type record extent | **nothing** | **nothing** |

The chain is acyclic and every interior checksum field is itself covered exactly
once, which I traced end to end: trailer CRC → directory CRC → crc_of_crc_array →
segment CRC → entry crc → tile bytes. §4.5's inventory of exceptions matches this
map exactly.

### Constants reproduced locally

| Constant | Document | Computed |
|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283`, stored `83 92 06 E3` | `0xE3069283`, `83 92 06 E3` ✓ |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` ✓ |
| CRC of a full all-sentinel segment (2¹⁶ × 20 = 1,310,720 bytes) | `0xEECB3BB2` | `0xEECB3BB2` ✓ |
| Appendix A trailer CRC over [0,60) | `0xE00938D2`, hexdump `D2 38 09 E0` | `0xE00938D2`, `D2 38 09 E0` ✓ |
| Appendix A directory region [16,20) | `00 00 00 00` (CRC of zero bytes) | ✓ |
| reflect₃₂(0x1EDC6F41) | implied by "reflected input and output" | `0x82F63B78`, the table I built ✓ |

My CRC was built from the reflected polynomial `0x82F63B78`, init `0xFFFFFFFF`,
final XOR `0xFFFFFFFF`, exactly as §4.5 states, and it reproduces all four. I also
reconstructed the whole 64-byte Appendix A trailer field-by-field from §6.2's
layout table and it matches the appendix hexdump byte for byte.

### Constants I could **not** reproduce locally

* zstd compressed-frame magic `28 B5 2F FD` = 0xFD2FB528 (§17.2, Appendix B) —
  external to this document (RFC 8878). The little-endian relation between the
  scalar and the byte string is self-consistent, which is all I can check.
* LZ4 frame magic `04 22 4D 18` (T23) — external.
* The lz4 decoded-size cap `0x7E000000` (§17.2, `[R-COD-07]`) — external, and
  described as "the block format's practical interoperability bound".
* §17.2's claim that RFC 8878's two Window_Size derivations agree for a conforming
  tile, and that a sub-1-KiB tile is encodable under codec 3 only as a
  single-segment frame. Internally coherent; unverifiable from this document alone.
* The CRC-32C polynomial's identity with RFC 3720 §12.1 — external.

### Every worked example in the document also reproduces

I checked these because a verifier that disagrees with the spec's own examples is
a verifier with a bug: §11.2's grid (4, 8) / N = 32 / P = 65,536; §11.4's ordinals
(tile (1,0) → 8; coordinate (300,700) → s = 10, in-tile ordinal 11,452; planar
channel 2 → disk ordinal 74); §12.1's bfloat16 `0x3F80` and `0x7FC0`; §12.3's
twelve-byte channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F`; §14.2's Q = 3 /
decoded size 18 / bytes [15,18), and Q = 5 / 30 / [25,30); §14.3's packed bool
`55 01` and `55 FD`; §14.5's 32-byte edge tile with 15 padding positions; §17.3's
shuffle `00 00 00 00 00 00 80 00 40 3F 40 40`; §15.4's 1,000,000-entry layer
(16 segments, 64-byte array, region 20,000,064, segment 15 at [19,660,800,
20,000,000), entry at region byte 339,180 within it) and the planar example's disk
ordinal 74 at region bytes [1,480, 1,500); §20.3's 32·20 + 4 = 644; §4.6's
`température` at 12 bytes NFC and 13 NFD; §5.1's 128-byte floor (dir_offset 16 +
dir_length 4 ≤ F−64 forces F ≥ 84, and F ≡ 0 mod 64 forces 128).

Every one matched. That is a good result for a document at this stage and it is
worth saying plainly.

---

## 6. Decoded-content obligations

**What a verifier must decode.** Every stored tile of every layer. This is not
stated as an algorithm anywhere; I derived it. §2.4: "A file is conforming only if
it satisfies every requirement at every scope"; §2.3: the verifier "checks every
file-level requirement". The per-tile requirements that need a decode are T3
(decoded length exactly the declaration-derived decoded size, `[R-SER-07]`), T24/T25
(exact consumption, malformed stream, `[R-COD-08]`), T13 (independent decodability,
`[R-COD-02]`), T4/T5 (padding content and pad bits, `[R-SER-05]` — "a verifier MUST
check it"), T2 (interleaved bool bytes, `[R-SER-08]` — "its assigned detector is the
verifier"), and T26 (mis-strided filter, detected through T2's or T4's check).

It must also decode every user-metadata document, or say it declined: `[R-MTA-09]`
puts the decline on the same footing as `[R-COD-11]`'s inability to run a codec.

**What it must compare against.** Declarations only, never payload content:
decoded size from geometry, layout and channel types (§14.2/§14.3, and `[R-SER-07]`
is emphatic — "decoded size is a function of the layer's declarations alone ...
never of payload content"); fill bytes from the channel entry (`[R-TYP-06]`,
authoritative, no type-derived default); the entry's crc for the stored bytes; and
for zstd, the frame content size against the decoded size (T22) with an explicit
prohibition on using it to size anything.

Determining *which* in-tile positions are padding is pure declaration arithmetic and
determinate: from the disk ordinal k, c = k div N and s = k mod N for planar, s = k
for interleaved; decompose s under row-major into tᵢ; a position (u₀…u_{d−1}) is a
padding position iff tᵢ·Tᵢ + uᵢ ≥ Eᵢ for some i. I confirmed this against §14.5's
example: extents (5,5), tiles (4,4), edge tile s = 3, only (0,0) real, 15 padding
positions, decoded tile 32 bytes with values 1–15 each `CD AB`.

**What it is permitted to skip.**

* Slack content (§5.2, `[R-CNT-03]` is a SHOULD).
* The content of an unassigned-type record's extent (§8.1, opaque).
* Prior generations (§9.7's Note: "Nothing here enumerates prior commits").
* The recovery probe (§9.6: "For a verifier the probe is diagnosis ... not a
  finding about the file it was given").
* Everything in §21.7 — mis-strided filters with no structural witness, undisclosed
  dictionaries, plainly wrong data — and crucially this does **not** yield *cannot
  establish*.
* A user-metadata document under an **experimental** encoding: §21.6 declares that
  file conforming, and this document defines no decoding for such an encoding, so
  there is no obligation to discharge and no unchecked requirement to report.
* Padding content of a sentinel (unstored) tile — there is no serialization.
* All SHOULDs, reported as advisories.

---

## 7. The incomplete walk

Charter asks for the walk arithmetic twice: once complete, once not. The complete
one is §3 above. For the incomplete one I used my generation-2 file (below) and
corrupted layer B's crc_of_crc_array so that L38 fires.

Why this is the case that genuinely blocks enumeration: `[R-ENC-05]` — "A reader
MUST NOT allocate, seek, or issue I/O based on any integer obtained from a file
before the checksum covering it has been verified" — and §8.2's chain puts B's entry
offsets under the segment CRC, which is under crc_of_crc_array. With that link
broken, B's 8 entries are untrusted integers, and the verifier may not follow them.
B's *index region* is still claimed (its extent slot lives in the layer record,
under the directory CRC); B's *stored tiles* are not locatable.

Numbers, on the generation-2 file (F = 768):

```
confirmed claimants (front 16, A tile 4, A index 44,
                     B index 164, dir 205, trailer 64)      union = 497
true live-state union (adds B's 7 stored tiles, 14 bytes)   union = 511
TRUE slack                                                          257
```

Verdict: *nonconforming* (L38 established, reject-layer). Certification barred.
Slack total: **partial**, per `[R-CNT-21]`. And here is where I had to guess. The
rule reads:

> "A partial total counts only the bytes no claimant claims within the regions the
> verifier did walk, and a verifier reporting one MUST also name the regions it did
> not walk and report their byte extent."

Three readings of "the regions the verifier did walk", each defensible, giving
different reports on the same file:

* **(a) region = the whole file, claimants = those confirmed.** Partial total
  = 768 − 497 = **271**, which overstates true slack by exactly 14 bytes — layer B's
  stored payload. Unwalked region named as "layer B's tile-index region [306,470),
  164 bytes, entries not enumerated".
* **(c) region = the byte ranges actually examined, i.e. the claimants themselves.**
  Then no byte inside them is unclaimed and the partial total is **0**. Literal, and
  it would make every partial total 0, which cannot be intended since the clause
  presupposes such bytes exist.
* **(b) region = a maximal span the verifier can certify it accounted for
  exhaustively.** B's tiles could lie anywhere in [16, F−64), so the verifier can
  claim no such span at all: partial total **0**, unwalked extent ≈ 688 bytes.

I picked (a), on the strength of §5.2's Note — "A partial total (`[R-CNT-21]`)
reports what one verifier's incomplete walk left unclaimed" — where "left unclaimed"
reads as *no confirmed claimant claimed it*, over the file, not over some
sub-region. But (a) sits badly with the very words it is meant to implement, and it
makes the second half of the obligation — "report their byte extent" for the regions
not walked — unsatisfiable in the exact case that produced it, since the byte extent
of B's stored tiles is precisely what the verifier could not learn. Naming the index
region and its 164 bytes as "the region not walked" is my workaround; the document
does not authorise it. Reported as **verifier-02**.

A second incomplete-walk shape is much cleaner and I record it for contrast: a torn
file. Nothing is walked, so the partial total is 0 and the unwalked region is the
whole physical file. Determinate, if strange.

And a third, which looks incomplete and is not: an entry that §15.3 classifies
reject-tile on a structural ground. §9.7 says in terms that this "does not make the
walk incomplete". So *nonconforming* with a **full** slack total.

I also note a latitude the document grants deliberately and which I did not treat as
a defect: whether a reject-layer *blocks* enumeration is left to the verifier
("a scope-level rejection blocks enumeration" is descriptive, not a rule that every
reject-layer does). A layer rejected for linearization = 2 still has parseable,
CRC-verified entries, so my verifier walks them and reports a full total; another
verifier could stop and report partial. Different reports, same verdict, and §2.3
explicitly licenses stopping. That is granted latitude, not ambiguity.

---

## 8. The multi-generation trace

Four generations of the file from §3. Verified after each step. All arithmetic
computed, not asserted.

### G1 — creation (`[R-LIF-02]` creation path, `[R-WRT-02]`)

As §3. F = 256, slack 26 (the pre-trailer pad alone). Verdict **conforming**.
Slack total 26, complete.

### G2 — append: add layer `B`

`B`: planar, C = 2, N = 4, entry_count = 8, S = 3, A_slab = 16, codec 1, uint8
channels, decoded size 2 per plane-tile. Writing begins at exactly F = 256
(`[R-LIF-02]` step 1). Ordinal 1 is a sentinel. Placement honours `[R-SLB-03]`, so
run heads are 16-aligned and interiors packed.

```
  [     0,    16)     16  front
  [    16,    20)      4  A tile#0        (untouched, A's extent slot unchanged)
  [    20,    64)     44  A index         (untouched — [R-WRT-05])
  [    64,   256)    192  SLACK           (dir1 102 + pad1 26 + trailer1 64)
  [   256,   258)      2  B t0
  [   258,   260)      2  B t2
  [   260,   272)     12  SLACK           (A_slab gap before run {3})
  [   272,   274)      2  B t3
  [   274,   288)     14  SLACK
  [   288,   294)      6  B t4,t5,t6
  [   294,   304)     10  SLACK
  [   304,   306)      2  B t7
  [   306,   470)    164  B index         (8*20 + 4)
  [   470,   675)    205  dir2            (A's record byte-identical + B's record)
  [   675,   704)     29  SLACK           (pre-trailer pad)
  [   704,   768)     64  trailer2        (generation 2, same file_id)
  claimed 511   F = 768   SLACK = 257
```

Verdict **conforming**. This is exactly §20.3's shape (a) — "A new layer. Nothing
existing is rewritten" — with the added wrinkle that B's own slab declaration
manufactures 36 bytes of fresh slack. The verifier reports 257 and, per §20.3's
note, that number is what tells an operator to compact.

### G3 — update: supersede A's tile 0

`[R-WRT-04]` step 4: A's stored-tile set changes, so A's **whole** index region is
re-emitted, necessarily at a new placement. B is untouched and keeps its extent
slot.

```
  [     0,    16)     16  front
  [    16,   256)    240  SLACK   (old A tile 4 + old A index 44 + dir1 102 + pad1 26 + tr1 64)
  [   256,   306)     50  B tiles + A_slab gaps (36 of those 50 are slack)
  [   306,   470)    164  B index
  [   470,   768)    298  SLACK   (dir2 205 + pad2 29 + trailer2 64)
  [   768,   772)      4  A tile#0 (new)
  [   772,   816)     44  A index (re-emitted whole)
  [   816,  1021)    205  dir3
  [  1021,  1024)      3  SLACK
  [  1024,  1088)     64  trailer3  (generation 3)
  claimed 511   F = 1088   SLACK = 577
```

Verdict **conforming**. Slack 577 against 511 bytes of live state — the file is now
more than half waste, which is §20.3's point about a commit's cost being dominated
by its index. Note the invariant the verifier can lean on: the claimed union is
*still* 511, unchanged across G2→G3, because one tile was superseded by one tile
of equal size.

### G4 — compaction

New file, fresh file_id, generation 1 (`[R-WRT-06]`). Tile bytes verbatim, entry
crcs unchanged, index regions regenerated with new offsets and recomputed segment
CRCs, layer records updated only in crc_of_crc_array and extent slot
(`[R-WRT-07]`).

```
  [     0,    16)     16  front
  [    16,    20)      4  A tile#0     (bytes verbatim)
  [    20,    64)     44  A index'     (offsets new, crcs unchanged)
  [    64,    68)      4  B t0, B t2
  [    68,    80)     12  SLACK        (A_slab gap — forced)
  [    80,    82)      2  B t3
  [    82,    96)     14  SLACK        (forced)
  [    96,   102)      6  B t4,t5,t6
  [   102,   112)     10  SLACK        (forced)
  [   112,   114)      2  B t7
  [   114,   278)    164  B index'
  [   278,   483)    205  dir
  [   483,   512)     29  SLACK        (pre-trailer pad)
  [   512,   576)     64  trailer      (file_id Y, generation 1)
  claimed 511   F = 576   SLACK = 65
```

Verdict **conforming**. 577 → 65.

The residual 65 is not compactor sloppiness and I want that on the record: 36 bytes
are forced by B's own A_slab = 16 declaration, which the compactor must honour —
`[R-WRT-05]` re-emits B's record byte-identically except for the two fields
`[R-WRT-07]` names, so S and A_slab survive, and `[R-SLB-03]`'s run-head alignment
then dictates the gaps. The other 29 are the pre-trailer pad. "Compaction reclaims
slack" does not mean slack reaches zero, and a verifier that reported 65 as a defect
would be wrong.

Slack by generation: **26 → 257 → 577 → 65**.

---

## 9. Mechanical audit of the register

I parsed §21.2–§21.5 out of the document and counted rows and instances by §21.1's
stated rule ("Instances within a cell are separated by semicolons, and a cell
reading — is one instance; the count is therefore mechanical once the cell is
written").

```
F rows= 38 instances= 60      (§21.2 declares "38 conditions")
L rows= 50 instances=103      (§21.3 declares "50 conditions")
T rows= 27 instances= 46      (§21.4 declares "27 conditions")
R rows= 10 instances= 44      (§21.5 declares "10 conditions")
TOTAL   125            253    (§21.8 declares "125 conditions over 253 instances")
```

Exact. Also: every row whose Detector is *verifier* has Detected = *certification*,
and no row with Detector *reader* does — 20 verifier rows, 105 reader rows, no
exceptions. Detection points used are exactly §19.2's four tiers plus
*certification*, with one composite cell (R1, "open (top-level); layer access
(sub-record)"), which is correct since the containing scope differs.

I spot-checked §21.1's "distinguishable file" rule against the cells that could
break it and it holds: F27/L47 (MU = 1 ∧ PE = 0, one predicate over two bits) is
one instance; F30/L50 (MU *or* PE differing from the registry) is two, because two
files differ. F28/L48 state "flags bits 2-15" as a single instance, matching the
T24 "any codec" precedent. L16 has 4 = two alternatives × two containers, exactly
as §21.1's worked sentence says.

I then cross-checked Appendix H's verifier checklist against the 20 verifier rows.
All 20 are covered: coverage/slack (§9.7), extent overlap (F35, L19), record flag
bits (F27/F28/F30, L47/L48/L50), the pre-trailer gap (F9), reserved-range type
values (F38, L26), alignment and slab (L41, L42, L43), decoded content (T2, T4, T5,
and T26 through them), member ordering (F29, L49). Nothing verifier-assigned is
missing from the checklist.

This is the strongest single signal I have about the document's state, and it is
why my finding list is short. Somebody has been doing the arithmetic.

---

## 10. Findings

### verifier-01 — CONTRADICTION — §20.1 / §20.5: a compactor cannot simultaneously copy tiles verbatim, emit a conforming file, and let latent violations travel

**Location.** §20.1 `[R-WRT-01]`; §20.5 `[R-WRT-06]`, `[R-WRT-07]`, `[R-WRT-09]`;
§2.3 `[R-CNF-06]`; §14.2 `[R-SER-08]`.

§20.1 grants an escape for latent violations and extends it to compactors by name:

> "An appender and a compactor satisfy every writer requirement for the bytes they
> produce and the preservation obligations of §20.4 for what they carry forward
> (`[R-CNF-06]`), and are readers of every structure they process (`[R-CNF-11]`) —
> a violation latent in a structure they neither modify nor rely on travels with
> it, and certifying the whole file is a verifier's office (§9.7)."

§20.5 then closes the escape for a compactor specifically:

> "A compactor's verification depth follows reliance over everything it carries
> (`[R-WRT-03]`): it relies on every structure it copies, so it MUST verify each
> link of the chain — the open (§19.1), each retained layer's record (§19.3) and
> full index chain (`[R-IDX-04]`), and each relocated extent's checksum, including
> every stored tile's entry crc — before emitting that structure's bytes."

If a compactor "relies on every structure it copies", then no structure it carries
falls under "neither modify nor rely on", and §20.1's escape clause is empty for a
compactor. Meanwhile §20.5 opens with a flat obligation on the output:

> "A compactor emits a new conforming file containing only the structures reachable
> from the input's live trailer"

and forbids changing tile bytes:

> "every stored tile's bytes verbatim — each index entry's crc is unchanged"

Now take an input whose only defect is a verifier-detected content violation — a
padding position not carrying fill (T4, `[R-SER-05]`), or an interleaved bool byte
of `0x02` (T2, `[R-SER-08]`: "Writers MUST NOT emit any byte other than 0x00 or
0x01 as an interleaved bool value"). `[R-WRT-09]`'s enumerated depth does not
include decoding, so the compactor does not detect it. Three obligations then
collide: copy the tile verbatim; emit a conforming file; satisfy every writer
requirement for the bytes it produces — and a compactor produces every byte of its
output, unlike an appender, whose violating bytes were written by an earlier
generation and are frozen by `[R-LIF-01]`. That asymmetry is why §20.1's joint
sentence works for appenders and fails for compactors.

**Permitted readings.** (i) `[R-WRT-06]`'s "emits a new conforming file" governs, so
a conforming compactor must decode and screen every stored tile — i.e. must have a
verifier's depth, not `[R-WRT-09]`'s — and must refuse an input carrying any latent
violation. (ii) `[R-WRT-09]`'s enumeration is the whole depth, §20.1's "travels with
it" governs, and the compactor emits a nonconforming output without itself being
nonconforming.

**What I picked.** (ii), on the strength of §20.1's closing clause "certifying the
whole file is a verifier's office (§9.7)" and of §2.3's "Verifiers and updaters are
readers of the files they process and inherit every reader obligation" — *reader*
obligations, and T2/T4 are not reader-detected. But (ii) requires reading
`[R-WRT-06]`'s "emits a new conforming file" as conditional on a conforming input,
which the text does not say, and requires §20.1's escape clause to be inert for the
one actor it names second.

**What an implementer does wrong without it.** Builds a compactor that either
refuses a large class of compactable files, or silently launders a nonconforming
input into a fresh file_id at generation 1 — the more damaging error, because the
output looks new.

**Byte-level.** No. Both readings emit the same bytes when they emit at all
(`[R-WRT-07]` fixes the tile bytes verbatim), and the output file is nonconforming
under both. What differs is whether the compactor that emitted it is a conforming
compactor, and whether it should have refused. Actor conformance, not file
conformance.

---

### verifier-02 — AMBIGUITY — §5.2 `[R-CNT-21]`: "the regions the verifier did walk" is undefined, and the byte extent of the unwalked ones is unreportable in the case that produces them

**Location.** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`.

> "A partial total counts only the bytes no claimant claims within the regions the
> verifier did walk, and a verifier reporting one MUST also name the regions it did
> not walk and report their byte extent."

"Region" is used nowhere else as a defined term for a span of the walk; §7.1 and
§15.1 use "region" for the directory region and the tile-index region, which are
claimants, not walk units.

**Permitted readings**, on my worked case (generation-2 file, F = 768, layer B's
crc_of_crc_array corrupted so `[R-ENC-05]` forbids following B's entry offsets;
true slack 257):

* (a) the region is the file and the claimants are the confirmed ones →
  partial total **271** (overstating true slack by exactly the 14 bytes of B's
  unlocatable payload);
* (b) a region is a span the verifier can certify it accounted for exhaustively;
  B's tiles may lie anywhere in [16, F−64), so no such span exists → partial total
  **0**, unwalked extent ≈ 688;
* (c) most literally, the regions walked are the byte ranges actually examined,
  i.e. the claimants themselves, inside which nothing is unclaimed → partial
  total **0** always, which cannot be intended.

**What I picked.** (a), on §5.2's Note — "A partial total (`[R-CNT-21]`) reports
what one verifier's incomplete walk left unclaimed" — reading "left unclaimed" over
the file. But (a) does not satisfy the clause's own words, and it leaves the second
obligation unsatisfiable: the byte extent of the regions not walked is exactly what
the broken checksum chain denied the verifier. I reported "layer B's tile-index
region, [306,470), 164 bytes, entries not enumerated" as the named unwalked region,
which is a stand-in the document does not authorise — that region *was* walked as a
claimant; what was not walked is the set of extents reachable through it.

**What an implementer does wrong without it.** Two verifiers hand an operator 271
and 0 for the same damaged file, and the number §22.3 calls "the number that
distinguishes a working file from a padded one" becomes unusable across tools.

**Byte-level.** No. §2.3 puts the partial total on the report side: it "constrains
the report, not the verdict". Both readings yield *nonconforming* and bar
certification identically, and no byte on disk turns on it.

---

### verifier-03 — AMBIGUITY — §2.3 `[R-CNF-11]`: whether a verifier must keep traversing past a capability-ground reject-file, which forks the verdict between *cannot establish* and *nonconforming*

**Location.** §2.3 `[R-CNF-11]`; §21.6's closing paragraphs; §7.2 `[R-CNT-15]`.

> "*cannot establish* is available only to a traversal that established no
> violation."

and

> "Two structural cases are **conforming files a reader nevertheless refuses**. ...
> The second is an **experimental-range record type carrying MU = 1** (§10.2,
> §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the
> file conforming all the same"

Take a file with (i) a top-level record of experimental type 0x8001 with MU = 1,
which the verifier does not implement, and (ii) a layer declaring linearization = 2
(L34, reject-layer, a real violation). The verifier is a reader first and
`[R-CNT-15]` obliges it to reject-file on (i) — which is not a violation. Does it
stop there, or keep going and establish (ii)?

**Permitted readings.** (A) It stops: `[R-CNT-15]` says reject-file, §2.4 says "A
reader MUST NOT rely on any structure in it", the traversal establishes no
violation, verdict *cannot establish*. (B) It continues: a verifier "checks every
file-level requirement", establishes L34, and "An established violation takes
priority" → *nonconforming*.

Nothing licenses the stop. §2.3's only stopping licence is "A verifier MAY stop at
the first violation it finds", and this is not a violation — so a verifier stopping
here is also not obliged by the accompanying clause to "report each scope it did
not examine as *unexamined*", and the report loses that signal too. The parallel
case, version_major naming an unimplemented major, is clean by contrast: §2.3 says
such a file "is neither conforming nor nonconforming under it", so there is nothing
to establish anywhere and *cannot establish* is forced.

**What I picked.** (B). My verifier continues past the capability refusal, records
it as an unchecked requirement with its ground, and reports *nonconforming* if it
establishes anything. I chose it because it produces the more informative report and
because §2.3's priority sentence reads as a rule about the union of what was found,
not about how far to look.

**What an implementer does wrong without it.** Two conforming verifiers label the
same file *cannot establish* and *nonconforming*, and a conformance manifest under
`[R-VEC-02]` — which records "whether the file is conforming" — cannot state a
unique expectation for such a vector.

**Byte-level.** No. Both readings bar certification (`[R-CNF-11]`: "a verifier
MUST NOT certify a file it reports that way"), so the accept/reject decision is
identical; only the label differs.

---

### verifier-04 — OBSERVATION — §21.9 `[R-ERR-03]` / `[R-ERR-05]`: the hard-limit collection omits validity-affecting limits it promises to hold

**Location.** §21.9 `[R-ERR-03]`, `[R-ERR-05]`; §2.5 `[R-CNF-10]`; §17.2
`[R-COD-06]`; §7.1 `[R-CNT-25]`.

> "Every limit affecting which files are valid, or which files a conforming reader
> accepts, lives here (`[R-CNF-10]`)."

and then

> "Some limits are instead **hard**: a file violating one is invalid, not merely
> large. They are stated where the structures forcing them are defined — a name at
> most 255 bytes ...; a layer declaring codec 4 at decoded tile size at most
> `0x7E000000` (`[R-COD-07]`); ... a directory of at least 4 bytes at an offset of
> at least 16 (§6.2, `[R-CNT-06]`); and no conforming file shorter than 128 bytes"

At least two hard limits of exactly that character are absent from the enumeration:

* **A zstd frame's declared window size, capped at the tile's decoded size**
  (`[R-COD-06]`: "MUST NOT declare a window size exceeding the tile's decoded size;
  a reader MUST treat either as a validity error at tile scope"; register row T21).
  This is precisely parallel to the lz4 `0x7E000000` cap, which *is* listed, and it
  is paired in §21.9's own table with a minimum guarantee ("zstd frame
  `Window_Size` | 8 MiB") exactly as the tile-size guarantee is paired with the lz4
  cap — so the omission is visible from within §21.9 itself.
* **A user-metadata extent's length floor of 5 bytes** (§7.1 `[R-CNT-25]`: "one
  whose extent_length is less than 5 — too short to hold both a document and the
  terminal CRC-32C ... — is a validity error at its containing scope"; rows F24 and
  L12). This is the same shape as the listed "a directory of at least 4 bytes".

The closing sentences read as an exhaustive account — "Most follow from a field's
width, an external format, or the value domain, and the rest from arithmetic over
structures a generation cannot omit. One does not: the 512 floor on A" — which
classifies the provenance of everything listed and singles out the sole exception.
An incomplete enumeration presented that way is what makes this reportable rather
than merely terse. Note also that §21.1 explicitly holds §21.9 outside the register's
normative-completeness clause, so `[R-ERR-03]` is the only thing carrying the
completeness claim here, and it carries it alone.

**What an implementer does wrong without it.** A verifier author who builds the
limit table from §21.9 — the section that tells them everything lives there — omits
the T21 window check and the F24/L12 length floor, and certifies files it should
reject. Recovering them costs a full sweep of every MUST in Parts I–III against
this list, which is why this is an observation rather than an ambiguity: it is
decidable, and expensively so.

**Byte-level.** No. `[R-COD-06]` and `[R-CNT-25]` state both rules unambiguously and
T21/F24/L12 register them; §21.1 makes the rule govern over any summary. Two
implementations reading the whole document reject the same bytes.

---

### verifier-05 — AMBIGUITY — Appendix G item 2: the hash is not pinned, and a zero digest yields an invalid `file_id`

**Location.** Appendix G, item 2 (non-normative).

> "**`file_id` from a cryptographic hash of the file's own emitted bytes**,
> computed over [0, F − 64) together with the trailer's other fields with the
> `file_id` field taken as zero, then written in. Deterministic, and high-entropy"

The appendix's whole purpose is cross-run byte identity, and it closes producer
freedom explicitly wherever it appears — item 1 requires "a named codec
implementation at a named version with fixed encoder settings", item 9 requires "a
named JSON writer at a named version". Item 2 requires no named hash and no named
rule for reducing a digest to 64 bits, so two adopters of the profile produce
different `file_id`s and therefore different trailers and different files, for the
same input, while both following item 2.

**Permitted readings.** (i) The hash and the 64-bit reduction are the adopter's
choice, and item 2 is complete because the profile is adopted per-application, as
items 1 and 9 also are; (ii) item 2 is incomplete by the standard items 1 and 9 set,
and needs "a named hash function at a named digest truncation" to deliver what it
claims. Two smaller residues resolve on their own: "the trailer's other fields"
cannot include the trailer CRC (which is a function of `file_id`, so including it is
circular), leaving trailer bytes [0,60) with [48,56) zeroed as the only consistent
serialization; and F is known before `file_id` is chosen, so the definition is not
circular in F.

**What I picked.** (ii). The profile states its own method — pin the producer — twice
elsewhere and does not apply it here.

Separately, and unhandled under either reading: `[R-CNT-06]` requires `file_id ≠ 0`,
and item 2 gives no fallback for a digest whose selected 64 bits are all zero. The
probability is 2⁻⁶⁴, but item 2 is a stated procedure with an output the format
forbids, in an appendix that elsewhere reasons carefully about what its items
guarantee.

**What an implementer does wrong without it.** Two teams both claim the profile,
compare hashes of their output files, and find they differ in eight bytes plus the
trailer CRC — the exact failure the profile exists to prevent.

**Byte-level.** No. Appendix G is explicitly non-normative and "adds no requirement
to any actor: a writer ignoring it is fully conforming"; both readings emit
conforming files, and file conformance does not turn on the choice.

---

### verifier-06 — OBSERVATION — Appendix G's closing count of "Four things" undercounts the freedoms its own items close

**Location.** Appendix G, closing paragraph (non-normative).

> "Everything else the profile needs is already mandatory — fill-encoded edge
> padding (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among them.
> Four things are not, and the items above are where the profile adds them: gap
> *content*, which `[R-CNT-03]` only advises; gap *extent*, which placement freedom
> (`[R-SLB-05]`) leaves open; sub-record order within a layer record's inline
> payload, which `[R-CNT-14]` leaves free; and the fill a writer records when its
> caller chooses none, which `[R-TYP-10]` states as a SHOULD."

Items in the list above close at least three further freedoms the format genuinely
leaves open, none of which appears among the four:

* **Item 6, "The sentinel for every all-fill tile."** Nothing in the format requires
  a writer to sentinel a tile whose samples all equal fill; storing it is fully
  conforming. Item 7's gloss treats item 6 as machinery serving the default-fill
  item, but two writers agreeing on fill still disagree on bytes if one stores
  all-fill tiles and the other does not — an independent freedom.
* **Item 8, "`version_minor` at the floor `[R-CNT-26]` states."** `[R-CNT-26]` is a
  SHOULD ("A writer SHOULD emit the lowest version_minor that defines every feature
  present in the file"), so this is the same category as `[R-TYP-10]`'s default
  fill, which *is* one of the four.
* **Item 3's top-level record order.** The four name only "sub-record order within
  a layer record's inline payload", but `[R-CNT-14]` — "Record semantics MUST NOT
  depend on record order" — leaves the *directory's* record order free too, and item
  3 pins it ("Records are ordered by type, and within type 0x0001 by layer name").

**What I picked.** I read the paragraph as an intended-exhaustive accounting, because
it is written as one ("Everything else ... is already mandatory. Four things are
not") and because that accounting is the appendix's argument that the profile is
minimal. Under the alternative reading — that "four" counts only *document-level*
degrees of freedom as opposed to producer-level ones — items 6 and 8 and item 3's
record order are still document-level and still missing.

**What an implementer does wrong without it.** Trusts the closing paragraph as the
audit of what the profile adds, and omits item 6 or item 8 from an implementation
built to the summary; the resulting writer is profile-conforming by the paragraph and
not by the items.

**Byte-level.** No. The appendix is non-normative and adds no requirement to any
actor; the items themselves, not the closing count, are what an adopter implements.

---

## 11. Things I checked and decided were **not** defects

Recorded because a reader of this transcript should be able to see what I rejected,
not only what I kept.

* **§4.7's informative class is empty in format major 1.** `grep -n informative`
  returns three hits: §1's non-normative reading guide and §4.7's own two
  sentences. No field anywhere carries the class, so `[R-ENC-16]`'s second clause
  ("each informative field's definition states what a reader does when it
  contradicts the data it describes") is vacuous. Not a defect: a normative rule
  with no witness is exactly what §5.2's Note describes as "a row no file could
  exhibit", and the document does not claim the class is populated.
* **The layer record's `A`, `S`, `A_slab` have no stated taxonomy class.** §4.7's
  Note delegates: the inline payload's "table omits the offset and class columns,
  and each field's class follows from the definitions above." By elimination they
  are informative (they affect neither byte location nor decoded meaning —
  `[R-SLB-01]`: "offsets are always explicit, so alignment is reader-invisible").
  The derivation is available and has no behavioural consequence I could construct,
  since `[R-ENC-16]` constrains only informative fields and the constraint is
  satisfied.
* **A pre-trailer pad longer than 63 bytes.** `[R-LIF-02]` step 5 says pad to the
  next 64-byte boundary, yet `[R-CNT-05]` says "a longer gap is conforming, and no
  conforming commit produces one." Covered by `[R-CNF-02]`'s general clause: "A
  writer obligation whose violation this specification expressly declares not to be
  a file-conformance violation ... binds the actor in the same way." My verifier
  certifies such a file and counts the gap as slack.
* **`[R-CNT-04]`'s residency exemption vs `[R-CNF-04]`'s "MUST detect every
  violation the register assigns to the reader".** F8's own Condition cell restates
  the exemption, so row and rule agree; no divergence.
* **Whether a reject-layer forces a partial slack total.** §9.7's "a scope-level
  rejection blocks enumeration" is descriptive of a case, not a rule that every
  reject-layer is that case. A layer rejected for linearization = 2 still has
  CRC-verified, parseable entries. Deliberate latitude, and §2.3 grants stopping
  latitude explicitly.
* **§21.7's second paragraph enumerates only three witness-free obligations** and
  omits §20.4's re-emission rules and §9.2's commit ordering. §21.1 describes §21.7
  as "the account, **by class**, of what fails [detectability]", and both classes
  are present; the enumerations inside them read as examples.
* **§21.6's "Two structural cases" covers only the top-level MU = 1 record**, not
  `[R-CNT-18]`'s layer sub-record variant. §2.3's statements of both the reader and
  verifier consequence say "a record", generically, so nothing is left open.
* **The experimental-value asymmetry** — experimental record types and metadata
  encodings leave a file conforming, experimental linearization/type/layout/codec/
  filter/index-encoding values do not. Deliberate and stated in terms by
  `[R-EXT-03]`, which routes each space separately.
* **`0x00000000` as a `crc_of_crc_array` when entry_count = 0.** `[R-CNT-23]` fixes
  it at 0, and CRC-32C of zero bytes is 0, so the constant is the honest value
  rather than a sentinel. Verified.
* **A stored tile whose entry crc field is 0.** Nothing forbids it; a 4-byte payload
  can legitimately CRC to zero. Only *sentinel* entries pair crc 0 with all-ones
  offset and length.

## 12. Confidence

I would build this verifier from this document and expect it to interoperate on
byte-level verdicts. Everything my charter asked me to compute — the walk, the
slack arithmetic, the overlap/alignment/slab invariants, the checksum chain, the
decoded-content obligations, the four-generation trace — came out determinate, and
every constant and worked example I could compute reproduced exactly. The three
places where I had to guess are all on the **report** side of the verifier's output
(verifier-02, verifier-03) or on the **actor**-conformance side (verifier-01), not
on which files are conforming.
