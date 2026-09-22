# Cleanroom round 37 — quiz-answerer transcript

Access discipline followed: read exactly one file,
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4981 lines), in full, via ordinary `Read` (not line-oriented `grep`,
except one header-listing `grep -n "^#"` used only to build a section
map, and one `grep -n "R-WRT-"` / `grep -n "F19"` / `grep -n "the change
is a new layer"` used only to locate line numbers of passages I had
already read in full, never to decide an answer from a hit/miss
count). Every substantive answer below is derived from reading the
surrounding prose in full, not from a grep hit count, so the
hard-wrap/blockquote grep hazard the brief warns about does not apply
to how I reached these answers.

Local computation: one Python script,
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/scratch/quiz-answerer/crc32c.py`,
implementing CRC-32C from arithmetic alone (no file reads). It
reproduces the spec's own two stated check values before I trusted it:
CRC-32C("123456789") = 0xE3069283 (matches §4.5's check vector
exactly) and the all-sentinel full-segment constant 0xEECB3BB2
(matches §15.4/`[R-IDX-05]` exactly). Only after both self-checks
passed did I use it to compute Q01's answer.

Contamination disclosure: before this brief's text ever reached me,
my context already contained this project's CLAUDE.md pointer, the
user's MEMORY.md index (a list of note titles about this project's
TARN work), and a git-status/log block naming recent commits (round
36/37, ADR-0131, etc.). None of that is part of the specification and
none of it is evidence about the specification. I did not open,
search, or otherwise consult any of it while answering, and no answer
below rests on it — every citation traces to a passage of
`spec/tarn.md` quoted below. I am naming that it appeared, per the
brief's instruction, without repeating its contents beyond the
one-line description above.

Scratch directory: empty when I began (no prior attempt's files
found). Files I wrote there: `crc32c.py` (the CRC tool) and this
transcript draft, which is copied verbatim to the mandated output path.

---

## Q01

§15.1: entry is 20 bytes; §15.4: "Segment s covers entries
[s·2¹⁶, min((s+1)·2¹⁶, entry_count))". entry_count = 70000, so segment
0 = entries [0, 65536) — exactly 65536 entries, a **full** segment —
and segment 1 = entries [65536, 70000) — 4464 entries, a **partial**
segment.

§15.4/`[R-IDX-05]`: "The CRC-32C of a segment consisting of 2¹⁶
sentinel entries is `0xEECB3BB2`; writers of sparse layers MAY emit
this constant for any **full** segment — one covering exactly 2¹⁶
entries, final or not — whose entries are all sentinels, without
computing it — **a partial segment's CRC MUST be computed**."

Segment 1 is partial (4464 ≠ 65536), so the constant is not available
for it regardless of every entry being a sentinel; the writer MUST
compute the actual CRC-32C over the 4464 × 20 = 89,280 stored sentinel
bytes (`FF ×16 00 ×4` repeated 4464 times).

Arithmetic (crc32c.py, self-checked against the spec's two published
CRC-32C values first):
```
sentinel_entry = FF*16 + 00*4     # 20 bytes
partial_segment = sentinel_entry * 4464   # 89,280 bytes
CRC-32C(partial_segment) = 0xE6E3E4F3
```

**Answer: `0xE6E3E4F3`**

---

## Q02

§7.4 dimension order: y (extent 10, tile 4) then x (extent 10, tile 4).
§11.4/`[R-GEO-06]`: "the last-declared dimension varies fastest";
in-tile ordinal of (u₀,…,u_{d-1}) = Σᵢ uᵢ·∏_{j>i}Tⱼ.

y=7 → t_y = 7 div 4 = 1, u_y = 7 mod 4 = 3.
x=7 → t_x = 1, u_x = 3.

d=2, dims (y,x): ordinal = u_y·T_x + u_x·1 = 3·4 + 3 = 15.

§14.2/`[R-SER-02]`, interleaved row: "channel c's value at in-tile
ordinal u sits at byte u·Q + Fᶜ", Q = Σ Bᵢ over all channels, Fᶜ = Σ Bⱼ
over channels j<c.

Channels: a (uint16, B=2) then b (uint8, B=1). Q = 2+1 = 3.
F_b = B_a = 2.

offset(b, ordinal 15) = 15·3 + 2 = 47.

**Answer: `47`**

---

## Q03

§7.4 channel entries: p (float64, B=8), q (uint8, B=1); layer is
planar. P = 300,000,000 per tile (given).

§17.2/`[R-COD-07]` (codec 4, lz4): "Writers MUST NOT declare this
codec for a layer any of whose addressed tiles' decoded size exceeds
0x7E000000 bytes … in a planar layer each channel's plane carries its
own decoded size (§14.2, §14.3), and the largest governs — and a
reader MUST treat such a declaration as a validity error at layer
scope, checkable from declarations alone."

Cap = 0x7E000000 = 2,113,929,216.
Channel p's plane decoded size = P·B_p = 300,000,000 × 8 =
2,400,000,000 > cap.
Channel q's plane decoded size = 300,000,000 × 1 = 300,000,000 < cap
(irrelevant — "the largest governs").

So the codec-4 declaration violates `[R-COD-07]`. The rule states the
outcome directly: "a reader MUST treat such a declaration as a
validity error at layer scope" — i.e. reject-layer (register row L44,
§21.3, whose Outcome is "reject-layer — the named layer is unusable,
every other layer unaffected").

**Answer: reject-layer; no other layer is affected (§21.3's
owning-scope rule: "every other layer unaffected").**

---

## Q04

§6.2 trailer layout row for flags: "bits 0–15 (incompat lane) all
zero, a set bit being reject-file (F19)".
§6.3/`[R-CNT-08]`: "a reader MUST reject-file on any set bit it does
not implement in the incompat lane (bits 0–15) … In this
specification's text no flag bits are defined."
§21.2 F19: "Any bit of the flags incompat lane (bits 0-15) is set;
this text defines no flag bits, so every such bit is unimplemented" —
Detector: reader; Detected: open; Governing rule `[R-CNT-08]`. F19 is
listed in §21.2 ("File-scope violations … Outcome: reject-file"), so
its presence is a genuine file-conformance violation, not merely a
capability gap on an otherwise-conforming file — unlike the
ignore-lane bits, which §6.3 and `[R-CNF-02]` treat as conduct-only /
non-violating.

flags = 0x00000004 sets bit 2, which is in the incompat lane
(bits 0–15). No incompat bit is defined by this text, so bit 2 is
"unimplemented" under F19: the flags field fails its own stated valid
range, independent of version_major or any other field's validity.

**Answer: conformance = no (the file is nonconforming, F19); reader
outcome = reject-file.**

---

## Q05

§7.4: "Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is
0)" (`[R-CNT-17]`).

entry_count = 200,000.
200,000 × 20 = 4,000,000.
⌈200,000 / 65,536⌉: 65,536 × 3 = 196,608 < 200,000, so ceiling = 4.
4 × 4 = 16.
Total = 4,000,000 + 16 = 4,000,016.

**Answer: `4000016` bytes.**

---

## Q06

§16.2/`[R-SLB-02]`: "Runs partition each contiguous block of disk
ordinals independently: for an interleaved layer the single block
[0, N) … the final run of a block can cover fewer than S ordinals.
Run r of a block starts at ordinal block_start + r·S."

N = 20, S = 6. Full runs: r=0 → [0,6); r=1 → [6,12); r=2 → [12,18);
remainder: 20 − 18 = 2 ordinals → run 3 = [18, 20), covering 2
ordinals. 20 mod 6 = 2 ≠ 0, so this final run is indeed the
"necessarily shorter" one the question describes. A_slab affects only
where the first stored tile of a run must land (§16.2, alignment
invariant), not how many ordinals each run spans.

**Answer: `2`**

---

## Q07

§7.4 inline-payload field list, computed field by field (all widths
per §7.4/§4.6/§4.2):

| Field | Bytes |
|---|---|
| name `z` (1-byte len + 1-byte content) | 2 |
| layout (u8) | 1 |
| linearization (u16) | 2 |
| codec (u16) | 2 |
| filter (u16) | 2 |
| alignment A (u64) | 8 |
| slab S (u64) | 8 |
| slab alignment A_slab (u64) | 8 |
| rank d (u8) | 1 |
| channel count C (u16) | 2 |
| dim `u` (name 1+1, extent 8, tile-extent 8) | 18 |
| dim `v` (name 1+1, extent 8, tile-extent 8) | 18 |
| channel `p`: type 6=uint8 (§12.1, B=1); name 1+1, type u16=2, fill 1-len+1-byte=2 | 6 |
| channel `q`: type 7=uint16 (§12.1, B=2); name 1+1, type u16=2, fill 1-len+2-byte=3 | 7 |
| index_encoding (u8) | 1 |
| entry_count (u64) | 8 |
| crc_of_crc_array (u32) | 4 |
| sub-records (zero of them) | 0 |

Sum: 2+1+2+2+2+8+8+8+1+2+18+18+6+7+1+8+4+0 = **98**.

(§7.4: "fields are packed in table order with no alignment or padding
between them" — confirms no hidden padding bytes.)

**Answer: `98` bytes.**

---

## Q08

§20.3 step 4 (`[R-WRT-04]`): "A layer that stores a tile **in the
generation this commit supersedes** keeps its declarations, with
these exceptions and no other: its name … MAY change; a dimension
extent MAY grow … a planar layer's channel list MAY be extended … a
slab or alignment declaration MAY be declared, changed or cleared …
Every other declaration is fixed for as long as the layer stores a
tile: … every channel's type **and fill** … A commit MUST NOT change
one of these; **the change is a new layer, or a rewrite that
re-declares it under a fresh file_id** (`[R-LIF-01]`, §20.5)."

And explicitly, later in the same step: "A change to any fixed
declaration of a layer that **stored** a tile in the generation the
commit supersedes — a fill value, a type, a tile extent — is not an
appender's operation at all (step 4): it would reinterpret or
invalidate every stored tile it reaches."

A fill-value change on a channel of a layer that stored a tile in the
superseded generation is exactly this case: fill is not on the
permitted-change list, so it is barred.

**Answer: No, not permitted as an ordinary appender's commit to layer
`L` under its existing name. The two named alternatives: (1) making
the change under a new layer (i.e., adding a differently-named/newly
declared layer rather than editing this one in place), or (2) a
rewrite that re-declares the layer under a fresh file_id (§20.5).**

---

## Q09

§20.4 table (governing which sub-records block a drop):

- Row "MU = 1": "Retain byte-identical. The updater MUST NOT modify
  the scope the record governs. At layer scope an unknown critical
  record blocks modification of that layer, its drop included,
  leaving other layers editable."
- Row "MU = 0, PE = 1" (user metadata's fixed flags, §7.3): "Retain
  byte-identical, extent content unmodified" — no block-the-drop
  language.

§20.4 body, directly on point: "A commit MAY therefore drop a layer
record, and the drop takes the layer whole … **One sub-record blocks
the drop, a sub-record of a type the updater does not implement with
MU = 1**, the drop being a modification of the scope it governs (the
table's first row)." And: "a dropped layer's sub-records and their
extents go with it whatever their PE bits" — i.e. the user-metadata
sub-record (MU=0, PE=1) does *not* block the drop; it simply goes with
the layer.

**Answer: No, the drop is not permitted. The blocking sub-record is
the unassigned-type sub-record stored with MUST_UNDERSTAND = 1 (the
one this updater does not implement) — not the user-metadata
sub-record, which is carried away with the layer if the drop is
otherwise possible, but here the drop cannot proceed at all because of
the unimplemented MU=1 sub-record.**

---

## Q10

Two independent things are true of this record simultaneously, and
the question's numbers hit both:

1. §10.3/`[R-EXT-03]` and §7.2/`[R-CNT-15]`: a record type from the
   experimental range (≥ 0x8000) is, by itself, conforming: "a record
   type from the experimental range is conforming (§10.3's prohibition
   binds the writer's conduct, not the bytes, `[R-CNF-02]`)". So the
   type value alone does not make the file nonconforming.
2. But §7.2/`[R-CNT-12]`: "Writers MUST NOT emit the combination
   MU = 1 with PE = 0 … Both writer violations make the file
   nonconforming (`[R-CNF-05]`) while leaving conforming behavior
   unchanged, so their detection is a verifier's: a verifier MUST
   treat a nonzero reserved flag bit or the MU = 1 with PE = 0
   combination as a validity error at the record's governing scope."
   This is registered at file scope as §21.2 row F25: "A non-layer
   top-level record's flags carry MUST_UNDERSTAND = 1 with
   PRESERVE_ON_EDIT = 0, a combination no writer emits" — Detector:
   verifier; Outcome: reject-file (§21.2's heading).

The question's record is stored with exactly MU=1, PE=0 — the
forbidden combination — so by F25/`[R-CNT-12]` the **file is
nonconforming**, independent of the type's range.

Separately, what an *ordinary* (non-verifying) reader does at open:
§7.2/`[R-CNT-15]`: "An unknown record type at file scope: MU = 1 →
reject-file." The type is unassigned (no reader implements it) and
MU=1, so an ordinary reader rejects the whole file at open — it is not
obliged to detect the MU=1/PE=0 combination itself (that is the
verifier's row, F25), but it still reject-files on the plain
unknown-type-with-MU=1 rule, which fires regardless of the stored PE
bit (`[R-CNT-12]` already tells any reader that meets that
combination to treat PE as 1, which does not change the MU=1 outcome).

**Answer: file conformance = no (nonconforming, per F25/`[R-CNT-12]`);
required reader outcome at open = reject-file (per `[R-CNT-15]`).**

---

## Q11

§14.1/§14.2, interleaved, sample-major, decoded tile image (P=2,
channels a int8(1B), b int16(2B), LE):
pos0: a=01; b=0203 stored LE → bytes 03,02.
pos1: a=04; b=0506 stored LE → bytes 06,05.

Decoded image (order): `01 03 02 04 06 05` (L=6).

§17.3/`[R-COD-10]`: shuffle stride s = sample stride Q for an
interleaved tile = 1+2 = 3. n = L/s = 2. "Viewing the image as
n = L/s consecutive groups of s bytes, the filtered image places byte
i of group j at offset i·n + j."

group0 (image[0:3]) = [01,03,02]; group1 (image[3:6]) = [04,06,05].

i=0: group0[0]=01→offset 0; group1[0]=04→offset 1.
i=1: group0[1]=03→offset 2; group1[1]=06→offset 3.
i=2: group0[2]=02→offset 4; group1[2]=05→offset 5.

(Verified the formula itself against the spec's own float32 worked
example in §17.3, which reproduces exactly with this same procedure.)

**Answer: `01 04 03 06 02 05`**

---

## Q12

§17.2/`[R-COD-06]` (codec 3, zstd): "Writers … MUST NOT declare a
window size exceeding the tile's decoded size; a reader MUST treat
either as a validity error at tile scope, both being header-checkable."
Register row T21 (§21.4): "Codec 3 (zstd) and the frame declares a
window size larger than the tile's decoded size" — Detector: reader;
Detected: tile use; Outcome (§21.4 heading): reject-tile.

Given: decoded size 500,000 bytes; frame uses a Window_Descriptor
declaring Window_Size = 8,388,608 bytes (8 MiB) — far larger than the
decoded size. Everything else about the frame (magic, no dictionary,
no content-checksum, single frame, no Frame_Content_Size) is stated as
conforming, but the oversized declared window alone is dispositive
under T21/`[R-COD-06]`, checkable from the header alone.

**Answer: `reject-tile`**

---

## Q13

§20.5, the paragraph closed by `[R-WRT-06]`: "… its verification depth
over what it carries is `[R-WRT-09]`'s and reaches no decoded content,
and **what it re-creates it decodes as a reader (`[R-CNF-11]`) and
writes as a creator (§20.2)**." And earlier, §20.1: a rewriter "is a
reader of every structure it processes (`[R-CNF-11]`)" — and
`[R-CNF-11]`/§2.3 makes plain a reader must implement every core
sample type (`[R-CNF-03]`) to decode at all; a type it does not
implement is one it cannot decode.

The scenario stipulates the rewriter does not implement the layer's
sample type, so it cannot perform the decode that re-creation
requires. Re-declaring/re-tiling/re-coding while merely *asserting*
bit-for-bit equivalence, without decoding, is exactly the shortcut
`[R-WRT-06]` forecloses: re-creation is defined as "decodes as a
reader … writes as a creator," not as a copy-with-relabeled-metadata
operation.

**Answer: No. The governing rule is `[R-WRT-06]` (§20.5): a rewriter
that re-creates a layer must decode its input tiles as a reader before
writing the new ones as a creator, so a rewriter that cannot decode
the layer's sample type cannot conformingly re-create it — its only
remaining options are to carry the layer forward verbatim (not
re-create it), drop it where §20.4 licenses a drop, or refuse to
rewrite the file.**

---

## Q14

§7.2/`[R-CNT-13]`: "Records with MU = 1 carry further references only
where this specification or registry review (§10) defines them" — the
general vehicle the question's hypothetical type Z uses.

§20.5, in the region closed by `[R-WRT-07]`: "No other record payload
carries a file offset: MU = 0 records by rule (§7.2), and an MU = 1
type the rewriter does not implement never reaches this step
(`[R-WRT-06]`). **An MU = 1 type it *does* implement is the remaining
case, and §7.2 admits it — such a type carries further references
where this specification or registry review defines them — so a
rewriter implementing one relocates whatever that registration
defines, on the same terms as the tile index.**"

Type Z is exactly this remaining case: MU=1, fully implemented by this
rewriter, and its registration explicitly defines an offset/length
reference to another region — the specification-or-registry-defined
exception §7.2 carves out. The tile index is this specification's own
worked instance of the same mechanism (§20.5: a rewriter regenerates a
tile-index region and re-points the layer record's extent slot when it
relocates the region).

**Answer: May relocate and re-point the reference (governed by
`[R-CNT-13]`'s MU=1-registered-reference exception together with
`[R-WRT-07]`'s "on the same terms as the tile index" rule).**

---

## Q15

§20.1: "A writer of a new file from an existing one takes one of two
positions, and the choice is its own. As a **rewriter** it undertakes
to preserve its input: §20.4's table for every record, the unknown
ignore-lane bits (`[R-CNT-08]`), and §20.5 whole … As a **creator** it
undertakes nothing toward its input, whatever it read: §20.2 binds it,
**it writes flags = 0**, and it answers for every byte of its output
(`[R-CNF-05]`), bytes it copied from another file included."
(`[R-WRT-01]`)

The tool's stipulated behavior matches "creator" on every discriminant
the spec gives:
- flags = 0, not the input's carried-forward ignore-lane bits — the
  literal creator behavior `[R-WRT-01]`/§20.2 describe, and the
  opposite of `[R-WRT-06]`'s rewriter obligation to "copy the input's
  unknown ignore-lane flag bits forward and set no other."
- It omits the input's file-scope user-metadata record outright
  (neither retained byte-identically nor re-emitted modified). A
  rewriter could not do this: user metadata is MU=0/PE=1 by registry
  (§7.3), and §20.4's table for that row is "Retain byte-identical,
  extent content unmodified" with no drop license (drop is licensed
  only for MU=0/PE=0 records, §20.4's third row); §20.4 states flatly,
  "A commit never removes a user-metadata record from a scope it
  keeps: a top-level one from the file." Only a tool undertaking
  nothing toward the input — a creator — can simply not emit it.
- A fresh file_id is common to both tiers and so is not
  discriminating here.

The layer's reference array being bit-for-bit unchanged does not make
this a rewriter: `[R-WRT-01]` says a creator "answers for every byte
of its output … bytes it copied from another file included" — nothing
bars a creator from happening to reproduce the same reference array
via its own fresh encode/decode.

**Answer: creator. It owes no preservation obligations toward the
input's records ("no" to owing them) — `[R-WRT-01]`: "As a creator it
undertakes nothing toward its input, whatever it read."**
