# Quiz A-on-A — working transcript

## Disclosure

I read exactly one file, in full, via five paginated Read calls (offsets
1-1000, 1001-2000, 2001-3000 [truncated by a tool-size limit, then re-read
as 3001-3500 and 3501-4000], and 4001-4981):
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
(4981 lines total, confirmed by `wc -l`). I did not read, list, or open any
other file or directory. I ran `wc -l` on the target file only (to plan
pagination) and local `python3` arithmetic that read no files (to check my
own computations). I did not grep; ordinary sequential Read calls covered
the whole document, including the register tables in §21.2-21.5, so no
line-wrap search was needed.

Context that appeared in my runtime before I began, which I disregarded as
not being part of the specification and not evidence about it: a
CLAUDE.md pointer to an AGENTS.md file; a user memory file listing many
note titles about a "TARN" project (harness/spec paths, gates, repair
history, etc.); a git-status block naming recent commit subjects about
ADR-0133 and ADR-0132; and various environment/tool-list boilerplate. I
did not open AGENTS.md or any ADR, and none of that material influenced
any answer below — every answer below cites only the one file I read.

The path I was given exists exactly where the brief said it would; no
path discrepancy to report.

My scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/quiz-a-on-a/`)
was empty when I began (verified with `ls -la`), so there is no earlier
attempt to report.

## Answers

### quiza-01 — minimum file size for the described layout

Front block [0,16). One user-metadata top-level record: inline_length=1,
extent_length=5 (extent_offset=16 is the smallest legal placement, ≥16),
so the extent occupies [16,21). dir_offset is placed immediately after,
at 21. The directory's record sequence is one record: 24-byte header +
1-byte inline payload = 25 bytes, plus its own terminal 4-byte CRC-32C =
dir_length 29 (§7.2, §7.1: "final 4 bytes are a CRC-32C over the
preceding dir_length − 4 bytes"). Directory occupies [21,50).

The trailer must begin at a 64-aligned offset F−64, with
dir_offset+dir_length ≤ F−64 (`[R-CNT-06]`). The smallest F−64 that is a
multiple of 64 and ≥ 50 is 64 itself, giving F = 128. Pre-trailer pad =
64 − 50 = 14 bytes (legal: any pad ≥ 0 up to the next boundary is
conforming, `[R-CNT-05]`).

Arithmetic (verified in Python, no file I/O):
extent_end = 16+5 = 21; dir_end = 21 + (24+1+4) = 21+29 = 50;
smallest F with F mod 64 = 0 and F−64 ≥ 50 is F = 128.

**Answer: 128**

### quiza-02 — version_major = 0 and the reach analysis

§2.3: "A file whose version_major is 0 declares no major at all (§6.3):
it is not a file declaring a format major other than 1, no reach
question arises for it, and `[R-CNT-07]` rejects it (§21.2, F18)."

**Answer: no; reject-file, F18**

### quiza-03 — appender and an ignore-lane bit

§6.3: "An updater MUST copy forward unknown ignore-lane bits of its
input file, MUST NOT clear them, and MUST NOT set any other." Bit 20 is
already set in the live trailer being extended, so it must be copied
forward as 1. Bit 25 is a different, currently-0 ignore-lane bit; the
appender MUST NOT set any bit other than what it copies forward.

**Answer: (a) 1; (b) not permitted**

### quiza-04 — smallest second-generation committed_file_length

Prior F = 128 (smallest conforming file, per §5.1's Example and
Appendix A). `[R-LIF-02]`'s Note: "The new F is therefore at least the
prior F plus 68, and since `[R-CNT-06]` makes every committed file
length a multiple of 64, at least the prior F plus 128." 128 + 128 =
256. Checked directly: dir_offset ≥ prior F = 128 (a new commit cannot
reuse an earlier generation's directory, §9.2's first Note), minimal
dir_length = 4 (empty directory), so dir_offset+dir_length = 132; new
F − 64 ≥ 132 ⇒ new F ≥ 196; smallest multiple of 64 that is ≥ 196 is
256.

**Answer: 256**

### quiza-05 — extent_offset = 0, extent_length = 40

§7.2's extent-slot rule: "(0, 0) means no extent. Any other combination
with either half zero... is a validity error." Here extent_offset = 0
(zero) and extent_length = 40 (nonzero) — exactly one half zero. §21.2
row F30: "A non-layer top-level record's extent slot has exactly one
half zero (offset 0 with length != 0, or offset != 0 with length 0)."
This is not F31 (which requires a *nonzero* extent_offset in 1-15).
Outcome for all of §21.2 is reject-file.

**Answer: F30; reject-file**

### quiza-06 — unstoring every tile of a layer while changing its fill

§20.3 step 4 lists the only permitted changes to a layer that "stores a
tile in the generation this commit supersedes": name changes, extent
growth, planar channel-list extension/shortening (not both), and
slab/alignment declare/change/clear. Fill value is explicitly *not*
among them, and is named in the "what the line gives up" paragraph as a
change requiring a new layer or a rewrite. Critically: "The tense is the
prior generation's... so a commit does not earn an empty layer's
freedom by emptying the layer as it re-declares it: a layer that stored
a tile keeps its declarations through the commit that empties it." So
changing fill in the very commit that unstores every tile is barred —
it cannot be done as an in-place edit of the existing layer.

However, §20.3 step 4 also states: "a commit MAY drop the layer (§20.4)
and add a new one under its name and other declarations, the new layer
being new whatever bytes its entries address... A dropped layer's name
is free to the same commit and to any later one." Dropping is licensed
because the layer record's registry-fixed flags are MU=0, PE=0
(§7.3), so §20.4's table permits the drop. This drop-and-recreate is an
ordinary appender operation, not a whole-file rewrite — the rewrite
path is reserved for re-declaring a layer's fixed declarations *in
place* while it keeps its identity and existing tile bytes
(`[R-WRT-06]`/§20.5), which is not what's needed here since every tile
is being unstored anyway.

**Answer: requires declaring a new layer** (achievable within an
appender's commit by dropping the old layer and adding a new one under
the same name; not a whole-file rewrite).

### quiza-07 — slab run index 2's starting disk ordinal

Interleaved layer, rank 2, extents (1200, 2000), tile extents (300,
250): Gy = ceil(1200/300) = 4, Gx = ceil(2000/250) = 8, N = 32. For an
interleaved layer, runs partition the single block [0, N) (§16.2).
Run r starts at block_start + r·S = 0 + 2·5 = 10.

**Answer: 10**

### quiza-08 — interleaved tile bytes under codec 1 / filter 2

Channels in order: x (float32, 4 bytes), y (uint8, 1 byte). Q = 5
(sample stride). Decoded (unfiltered) tile image, sample-major
(§14.1/§14.2), little-endian per value:

- position 0: x=0x01020304 → LE bytes `04 03 02 01`; y=0xAA → `AA`
- position 1: x=0x05060708 → LE bytes `08 07 06 05`; y=0xBB → `BB`

Decoded image (10 bytes): `04 03 02 01 AA 08 07 06 05 BB`

Byte-shuffle filter (§17.3): stride s = Q = 5 (interleaved), L = 10, n
= L/s = 2. Groups of 5 bytes: group0 = `04 03 02 01 AA` (position 0's
sample), group1 = `08 07 06 05 BB` (position 1's sample). Filtered
image places byte i of group j at offset i·n + j (n=2):

- i=0: group0 byte0=04→offset0; group1 byte0=08→offset1
- i=1: group0 byte1=03→offset2; group1 byte1=07→offset3
- i=2: group0 byte2=02→offset4; group1 byte2=06→offset5
- i=3: group0 byte3=01→offset6; group1 byte3=05→offset7
- i=4: group0 byte4=AA→offset8; group1 byte4=BB→offset9

Codec 1 (none) means the stored bytes are the filtered image verbatim
(`[R-COD-04]`).

**Answer: 04 08 03 07 02 06 01 05 AA BB**

### quiza-09 — planar layer, C=3, N=70,000

Addressed-tile count (entry_count) for a planar layer is C·N (§11.2) =
3 × 70,000 = 210,000.

Tile-index region length under index_encoding 1 (`[R-CNT-17]`,
§15.1): entry_count × 20 + ceil(entry_count / 2^16) × 4.
210,000 × 20 = 4,200,000. ceil(210,000/65,536) = ceil(3.2043...) = 4.
4 × 4 = 16. Total = 4,200,000 + 16 = 4,200,016.

**Answer: entry_count = 210000; region length = 4200016 bytes**

### quiza-10 — lz4 declaration with a 2.4 GB float64 plane

`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of
whose addressed tiles' decoded size exceeds 0x7E000000 bytes... in a
planar layer each channel's plane carries its own decoded size, and the
largest governs." 0x7E000000 = 2,113,929,216 bytes. The largest
channel plane here (channel a, float64) is 2,400,000,000 bytes, which
exceeds the cap.

**Answer: no**

### quiza-11 — mid-region reject-layer after some tiles already served

§2.4 (reject-layer): "The outcome is prospective: it bars further
service from the layer, and does not retroactively invalidate content
already returned under §19.2's validation timing." `[R-RDR-04]` step 8:
"A failure inside the same request that takes layer scope instead —
step 3's index-chain failure (`[R-IDX-04]`) — bars the request's
remaining entries and all further service from the layer; the bar is
prospective, so values the reader has already returned... stand."

**Answer: (a) no; (b) barred (reject-layer)**

### quiza-12 — MU=1, PE=0 on a stored record

`[R-CNT-12]`: "Writers MUST NOT emit the combination MU = 1 with PE =
0; a reader or updater encountering it MUST treat the record as PE = 1
(never silently deletable). Both writer violations make the file
nonconforming... while leaving conforming behavior unchanged, so their
detection is a verifier's: a verifier MUST treat a nonzero reserved
flag bit or the MU = 1 with PE = 0 combination as a validity error at
the record's governing scope."

**Answer: verifier, 1**

### quiza-13 — rewriter meeting a structurally reject-tile entry while regenerating an index

§20.5: "Regenerating a region means classifying every entry in it... An
entry §15.3 classifies reject-tile on a structural ground is neither [a
sentinel nor a well-formed pointer] — `[R-IDX-03]` gives it no stored
extent for a re-pointing to target — so regenerating the region cannot
proceed without meeting it... `[R-WRT-06]` then leaves it two
disposals, since it can neither reproduce the entry nor invent a
replacement: drop the layer, which §20.4's table licenses..., or
refuse." Only an output that omits the layer entirely reclaims that
layer's slack (a refusal produces no new file at all, so nothing is
reclaimed).

**Answer: drop the layer; refuse to rewrite — dropping the layer is the
one that reclaims slack**

### quiza-14 — two register rows

File X: valid magic, valid length-adjacent gate, but the trailer
CRC-32C at [60,64) does not match CRC-32C of [0,60) — this is exactly
row F14: "The u32 at trailer offset 60 does not equal the CRC-32C of
trailer bytes [0,60)," governed by `[R-CNT-06]`.

File Y: correct CRC but dir_offset = 10, which is < 16 — this is
exactly row F9: "Trailer dir_offset is less than 16, pointing the
directory into or before the front signature block," governed by
`[R-CNT-06]`.

**Answer: X: F14; Y: F9**

### quiza-15 — verifier stopping after layer C's reject-layer, before enumerating D and E

`[R-CNF-11]`: "A verifier MAY stop at the first violation it finds; one
that does MUST report each scope it did not examine as *unexamined*,
which is not a finding that the scope is clean. *Unexamined* is neither
a verdict nor *cannot establish* — it constrains the report, not the
verdict."

**Answer: unexamined; no**
