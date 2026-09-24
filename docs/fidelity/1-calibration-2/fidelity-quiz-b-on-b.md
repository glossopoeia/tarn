# Quiz taker transcript — quiz-b-on-b

## Disclosure

**What I read.** Exactly one file, as instructed:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md`
(4,885 lines / ~289.6 KB). The Read tool's per-call size/token caps meant I could
not read it in a single call; I read it in five sequential chunks by line offset
(1–1000, 1000–1700, 1700–2400, 2400–2900, 2900–3400ish, 3520–3650, 3650–4050),
all from this same single file and no other. I did not open any other copy of
this specification, under this or any other path.

**What I ran.** One `wc -l` on the target file (to plan chunked reads), and one
`grep -n "20.5\|rewrite\|Rewrit" tarn.md` run from inside
`scratch/cleanroom/editions/c/` against `tarn.md` only, to locate the rewrite
(§20.5) material efficiently before reading it in full. No other file was read
or grepped. I did not list any directory's contents (not the repo root, not
docs/, not conformance/, not the scratch or out directories). I did not run git
commands, web search, or web fetch.

**Scratch/output directories.** My scratch directory
(`/private/tmp/claude-501/.../fidelity-2/scratch/quiz-b-on-b/`) was empty when
I started — no prior attempt's files were present. I created the output
directory (`/private/tmp/claude-501/.../fidelity-2/out/`) with `mkdir -p` only
so I could write this transcript; I did not read or list its contents at any
point, so I don't know what else is being written there by other agents.

**Path/edition note.** The computed task brief's prose calls me a "quiz taker
... answering from edition B of the document," but the one file path it
authorizes is `.../scratch/cleanroom/editions/c/tarn.md` — i.e., edition "c" by
its path, not "b". I am flagging this discrepancy rather than silently
resolving it either way. I read exactly the file at the given path and answered
from its contents alone; I draw no inference from the letter in the path (or
from the word "B" in the prose) about what any other edition's text says. I
did not go looking for an "edition b" directory to check, since the brief
forbids listing directories or opening any other copy of the spec.

**Unsolicited context.** Before this task began, my context already contained:
a pointer from this repository's `CLAUDE.md` to an `AGENTS.md`; the contents of
a personal `MEMORY.md` file (a bulleted index of past-session topic notes,
mostly about a "TARN" project's harness/process concerns); and a git-status
block naming the current branch, a "Main branch," and five recent commit
subjects. None of this was requested by me for this task, none of it is part
of the specification, and none of it is evidence about the specification's
content. I have disregarded all of it in answering the slate below, and I am
not repeating its substance here beyond identifying that it appeared. I did
not open AGENTS.md, any ADR, PLAN.md, OPEN-QUESTIONS.md, or any file the
memory notes reference.

**Method.** For each question I located the governing rule(s) in the one
file I read, quoted the decisive sentence(s), did any arithmetic by hand
(shown below), and answered strictly in the form each question asked, with
the answer field holding only the bare answer.

---

## Working notes per question

### quizb-q1 — trailer dir bounds
Trailer field table (§6.2): `dir_offset + dir_length ≤ F − 64`.
F = committed_file_length = 320. dir_offset=200, dir_length=60.
200 + 60 = 260. F − 64 = 320 − 64 = 256. 260 > 256 → fails.
Register row: F10 "Trailer dir_offset + dir_length exceeds F - 64, so the
declared directory region runs into or past the live trailer" — outcome
reject-file (governing `[R-CNT-06]`).
**Answer: fail; F10; reject-file.**

### quizb-q2 — front block residency
`[R-CNT-04]` (§6.1): "A reader that would have to issue a further range
request to obtain those bytes MAY defer or omit the check." A single
suffix-range request for the final 500 bytes of a much larger file does not
reach offset 0, so the front block is not resident; obtaining it needs a
further request. Not obligatory.
**Answer: No; [R-CNT-04].**

### quizb-q3 — unassigned type 0x0050, MU=1
Assigned types are only 0x0001, 0x0002 (§7.3); reserved range is
0x0003–0x7FFF (§10.2). 0x0050 falls in reserved range, MU=1.
Register row F35: "A top-level record has a reserved-range type value
(0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to 1" —
detector reader, outcome reject-file, governing `[R-CNT-15]`.
**Answer: reject-file; F35.**

### quizb-q4 — appender and an unknown ignore-lane bit
`[R-CNT-08]`: "An updater MUST copy forward unknown ignore-lane bits of its
input file, MUST NOT clear them, and MUST NOT set any other." Input flags =
0x00010000 (bit 16), incompat lane all zero. No new feature requires a bit.
Output flags must equal the input's ignore-lane bits, unchanged, nothing else
set.
**Answer: 0x00010000.**

### quizb-q5 — entry_count for rank-3 interleaved layer, one zero extent
§11.2: Gi = ⌈Ei/Ti⌉; interleaved addressed-tile count = N = ∏Gi.
G0 = ⌈500/64⌉ = 8. G1: E1 = 0 → by `[R-GEO-02]`, "A dimension with extent 0
is valid: its grid count is 0, the layer has zero addressed tiles" → G1 = 0.
G2 = ⌈10/4⌉ = 3.
N = 8 × 0 × 3 = 0.
**Answer: 0.**

### quizb-q6 — disk tile ordinal, planar, channel 3
§11.4: spatial ordinal s = Σ tᵢ·∏_{j>i}Gⱼ; disk ordinal (planar) = c·N + s.
s = t0·G1 + t1 = 2·3 + 1 = 7. N = G0·G1 = 5·3 = 15.
disk ordinal = 3·15 + 7 = 45 + 7 = 52.
**Answer: 52.**

### quizb-q7 — byte-shuffle on an interleaved two-channel tile
§14.2 offset table (interleaved): offset of value k = (k div C)·Q + F_{k mod C};
C=2, Q = Ba+Bb = 2+1 = 3, F_a=0, F_b=2.
Decoded image (P=2 positions):
- k=0 (a, pos0): bytes 02 01 (LE of 0x0102) at offsets [0,2)
- k=1 (b, pos0): byte AA at offset 2
- k=2 (a, pos1): bytes 04 03 (LE of 0x0304) at offsets [3,5)
- k=3 (b, pos1): byte BB at offset 5

Decoded image = 02 01 AA 04 03 BB (L=6).

§17.3 byte-shuffle: stride s = Q = 3 (interleaved). n = L/s = 2.
Groups of s=3 bytes: group0 = [02,01,AA], group1 = [04,03,BB].
Filtered[i·n + j] = byte i of group j:
- i=0,j=0 → offset0 = 02 (group0 byte0)
- i=0,j=1 → offset1 = 04 (group1 byte0)
- i=1,j=0 → offset2 = 01 (group0 byte1)
- i=1,j=1 → offset3 = 03 (group1 byte1)
- i=2,j=0 → offset4 = AA (group0 byte2)
- i=2,j=1 → offset5 = BB (group1 byte2)

Codec 1 (none): stored bytes = filtered image verbatim.
**Answer: 02 04 01 03 AA BB.**

### quizb-q8 — alignment A≠0 together with slab S≠0
`[R-CNT-16]`: "Declaring both A ≠ 0 and S ≠ 0 is a validity error at layer
scope: the per-tile alignment and slab declarations are mutually exclusive."
Register row L20 matches exactly, outcome reject-layer.
**Answer: fail; L20; reject-layer.**

### quizb-q9 — fill length prefix ≠ element size (uint32, prefix 2)
`[R-CNT-23]`: "a fill whose byte length differs from its type's element
size ... [is] a validity error at layer scope." Register row L30: "A channel
entry's fill length prefix differs from the element size of the channel's
declared type" — reject-layer.
**Answer: fail; L30; reject-layer.**

### quizb-q10 — index_encoding 1, entry_count=12, extent slot (0,0)
`[R-CNT-17]`: extent_length must equal entry_count×20 + ⌈entry_count/2¹⁶⌉×4;
slot (0,0) gives extent_length 0, but the formula for entry_count=12 gives
12×20+4=244 ≠ 0 → mismatch. Register row L22 explicitly: "including slot
(0,0) with entry_count > 0" — reject-layer.
**Answer: fail; L22; reject-layer.**

### quizb-q11 — untouched, well-formed entry whose stored bytes fail crc
§20.3 step 2: "a malformed index entry an appender meets while re-emitting a
region is carried forward byte-identically at its disk-ordinal position
under step 4, not repaired to a sentinel." §20.3 step 4 confirms untouched
entries are "byte-identical at its disk-ordinal position." §15.3 table: "stored
bytes fail the entry's crc | reject-tile (§8.2) — the entry itself is
well-formed; its extent stands." Register row T1 matches (detector reader,
tile use).
**Answer: carry the entry's 20 bytes forward byte-identically (unchanged) at
its disk-ordinal position; reject-tile.**

### quizb-q12 — planar region read, one entry fails crc
`[R-RDR-04]`: "each rejected entry's failure is bounded to the positions
that entry carries ... That bounding is a property of tile scope." In a
planar layer, one tile = one channel at one spatial tile, so the bound is
exactly that channel's data at that one spatial tile — not the other
channel, not other spatial tiles of the same channel.
**Answer: a.**

### quizb-q13 — rewriter meets a structurally reject-tile entry while regenerating a region
§20.5: "An entry §15.3 classifies reject-tile on a structural ground is
neither [a sentinel nor a re-pointable stored extent] ... `[R-WRT-06]` then
leaves it two disposals, since it can neither reproduce the entry nor invent
a replacement: drop the layer, which §20.4's table licenses ... or refuse."
**Answer: Drop the layer; Refuse to rewrite.**

### quizb-q14 — zstd window size vs. decoded size
Decoded size = P·Q; P = 128×128 = 16,384; Q = 4+4 = 8 (two int32 channels).
Decoded size = 16,384 × 8 = 131,072 bytes.
Declared Window_Size = 1,048,576 bytes > 131,072 bytes.
`[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's
decoded size; a reader MUST treat ... as a validity error at tile scope."
Register row T21: "Codec 3 (zstd) and the frame declares a window size
larger than the tile's decoded size" — Detector: reader; outcome
reject-tile.
**Answer: fail; T21; reject-tile; reader.**

### quizb-q15 — segment-CRC shortcut with one non-sentinel entry present
`[R-IDX-05]`: "writers of sparse layers MAY emit this constant for any
**full** segment ... whose entries are all sentinels, without computing it."
Segment 1 has exactly one non-sentinel entry, so it is not all-sentinel —
the shortcut does not apply; the real CRC-32C over the segment's actual
bytes MUST be computed and stored.
**Answer: No; [R-IDX-05].**

---

## Files I wrote

- This transcript: `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/out/transcript-quiz-b-on-b.md`
- No other files were written. My scratch directory
  (`.../fidelity-2/scratch/quiz-b-on-b/`) was left empty — all work here was
  simple enough to do in-line without intermediate script files.
