# Quiz taker transcript — quiz-b-on-a

## Disclosure

- I read exactly one file: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md,
  in full (lines 1-4981), in six sequential Read calls (offsets 1, 1201, 1901,
  2601, 3301, 4001, covering to end of file). I read no other project file.
- I ran: `mkdir -p` to create my own scratch directory and the shared output
  directory (creating a directory does not read its contents); `ls -la` on my
  own scratch directory only, to check for a prior attempt's files (it was
  empty — no prior files found); `wc -l` and `wc -c` on the target file only,
  to gauge its size before reading it in chunks.
- I did not list any other directory, did not read docs/, PLAN.md,
  OPEN-QUESTIONS.md, AGENTS.md, README.md, CONTRIBUTING.md, conformance/, or
  spec/registry.json, did not run git commands, and did not open any other
  copy of this specification.
- The path named in the brief matched exactly: the file exists at
  /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md
  with no discrepancy.
- Context I did not ask for appeared in my session before this task began:
  a project CLAUDE.md pointer, a user memory-file index (auto-loaded
  "MEMORY.md" entries), a git status/log block, and environment/model
  identification blocks. I disregarded all of it as not part of, and not
  evidence about, the specification text; I am not repeating its contents
  here beyond naming that it appeared.
- I ran no computation reading any file for this slate other than the
  arithmetic shown per-question below, which reads only values given in the
  question text itself.

## Per-question work

### quizb-q1
Trailer table (§6.2) and the ordered validation of `[R-CNT-06]`: after magic,
CRC, version gate and the flag/committed-length checks all pass, the
remaining gates include `dir_offset + dir_length <= F - 64`. Given F = 320,
dir_offset = 200, dir_length = 60: 200 + 60 = 260; F - 64 = 256. 260 > 256,
so this gate fails. This is exactly register row F10 ("Trailer dir_offset +
dir_length exceeds F - 64"), §21.2, outcome reject-file.

### quizb-q2
§6.1 `[R-CNT-04]`: the front-block equality check binds a reader only when
its open leaves bytes [0,16) resident. A single suffix request for the final
500 bytes of a much larger file does not reach offset 0, so the reader "MAY
defer or omit the check." Answer: No, governed by [R-CNT-04].

### quizb-q3
Record-type space (§10.2 table): assigned = 0x0001, 0x0002; reserved =
0x0003-0x7FFF; experimental >= 0x8000. 0x0050 lies in the reserved range.
Register row F35 (§21.2): "A top-level record has a reserved-range type
value (0x0003-0x7FFF) with MUST_UNDERSTAND (flags bit 0) set to 1" —
detector reader, detected at open, outcome reject-file (§21.2 header).

### quizb-q4
`[R-CNT-08]`: "An updater MUST copy forward unknown ignore-lane bits of its
input file, MUST NOT clear them, and MUST NOT set any other." Input flags =
0x00010000 (bit 16 only); the commit adds no feature needing a flag; incompat
lane (bits 0-15) must stay 0 for this text's writers. New trailer flags MUST
equal 0x00010000.

### quizb-q5
§11.2: Gi = ceil(Ei/Ti). Extents (500, 0, 10), tile extents (64, 8, 4):
G0 = ceil(500/64) = 8, G1 = ceil(0/8) = 0 (extent 0 => grid count 0, §11.1),
G2 = ceil(10/4) = 3. N = 8 * 0 * 3 = 0. Interleaved addressed-tile count =
N = entry_count (§11.2, §7.4). Channel count (5) does not enter an
interleaved layer's entry_count. entry_count = 0.

### quizb-q6
§11.4: spatial ordinal s = sum_i ti * prod_{j>i} Gj. d=2, G=(5,3),
(t0,t1)=(2,1): s = t0*G1 + t1 = 2*3 + 1 = 7. N = G0*G1 = 15. Planar disk
ordinal = c*N + s. c = 3 (channel index 3): 3*15 + 7 = 52.

### quizb-q7
§14.1 interleaved value sequence (C=2): k=0 -> channel a at pos0; k=1 ->
channel b at pos0; k=2 -> channel a at pos1; k=3 -> channel b at pos1.
Little-endian encoding (§4.1): a=0x0102 -> bytes 02 01; b=0xAA -> byte AA;
a=0x0304 -> bytes 04 03; b=0xBB -> byte BB.
§14.2 byte layout, interleaved: offset(k) = (k div C)*Q + F_{k mod C}, Q =
2+1 = 3, F_a=0, F_b=2. Decoded image (6 bytes), by offset:
[0]=02 [1]=01 [2]=AA [3]=04 [4]=03 [5]=BB.
§17.3 byte-shuffle, interleaved stride s=Q=3, n=L/s=6/3=2. Groups of s=3
bytes: group0=[02,01,AA] (image bytes 0-2), group1=[04,03,BB] (bytes 3-5).
Filtered offset = i*n + j for byte i of group j (i in 0..s-1, j in 0..n-1):
 i=0,j=0 -> 02 at offset 0*2+0=0
 i=0,j=1 -> 04 at offset 0*2+1=1
 i=1,j=0 -> 01 at offset 1*2+0=2
 i=1,j=1 -> 03 at offset 1*2+1=3
 i=2,j=0 -> AA at offset 2*2+0=4
 i=2,j=1 -> BB at offset 2*2+1=5
Codec 1 (none): stored bytes = filtered image verbatim.
Stored bytes in offset order: 02 04 01 03 AA BB.

### quizb-q8
`[R-CNT-16]`: "Declaring both A != 0 and S != 0 is a validity error at layer
scope." Register row L20 (§21.3): "A layer record declares both a per-tile
alignment A != 0 and a slab S != 0" — outcome reject-layer (§21.3 header).

### quizb-q9
`[R-CNT-23]` / `[R-TYP-06]`/§7.4: fill length prefix must equal the type's
element size (uint32 -> 4 bytes); here it is 2. Register row L30 (§21.3):
"A channel entry's fill length prefix differs from the element size of the
channel's declared type" — outcome reject-layer.

### quizb-q10
`[R-CNT-17]`: under index_encoding 1, extent_length MUST equal
entry_count*20 + ceil(entry_count/2^16)*4, and 0 when entry_count = 0. Here
entry_count = 12 (nonzero) but extent slot is (0,0), i.e. extent_length = 0,
not the required 12*20 + 1*4 = 244. Register row L22 (§21.3): "extent_length
!= entry_count x 20 + ceil(entry_count/2^16) x 4 — including slot (0,0) with
entry_count > 0" — outcome reject-layer.

### quizb-q11
§15.3's own text: "An entry whose only defect is that its stored bytes fail
its crc is well-formed: the defect lies in the bytes it addresses, not in
the entry, so its extent stands." §20.3 step 4: an appender writes "every
other entry byte-identical at its disk-ordinal position" for entries the
commit does not touch; §20.3 step 2 forbids an appender from repairing a
defect it carries forward. So the appender MUST carry entry E's 20 bytes
forward byte-identically (unchanged). For the reader: register row T1
(§21.4): "A stored tile's bytes at [offset, offset+length) do not match the
crc field of its non-sentinel tile-index entry" — outcome reject-tile
(§21.4 header), per `[R-CNT-20]`.

### quizb-q12
§19.4 step 8 / `[R-RDR-04]`: "Where the request covered several entries — a
region, or a planar layer's several channels — each rejected entry's
failure is bounded to the positions that entry carries... That bounding is
a property of tile scope." The failing entry is specifically the `temp`
channel's entry at one spatial tile (planar layout: each channel/tile pair
has its own entry, §11.4/§15.1). So the bar is narrowest: only `temp`'s data
at that one spatial tile. Answer: (a).

### quizb-q13
§20.5: "Regenerating a region means classifying every entry in it... An
entry §15.3 classifies reject-tile on a structural ground is neither [a
sentinel nor an entry with a stored extent to re-point] — regenerating the
region cannot proceed without meeting it... `[R-WRT-06]` then leaves it two
disposals, since it can neither reproduce the entry nor invent a
replacement: drop the layer, which §20.4's table licenses..., or refuse."
Answer: {Drop the layer; Refuse to rewrite}.

### quizb-q14
§14.1/§14.2: interleaved, P = 128*128 = 16384, Q = 4+4 = 8 (two int32
channels). Decoded size = P*Q = 16384*8 = 131,072 bytes. `[R-COD-06]`:
codec 3 "MUST NOT declare a window size exceeding the tile's decoded size."
Declared Window_Size = 1,048,576 > 131,072 -> violation. Register row T21
(§21.4): "Codec 3 (zstd) and the frame declares a window size larger than
the tile's decoded size" — detector: reader; detected: tile use; outcome:
reject-tile (§21.4 header).

### quizb-q15
§15.4 `[R-IDX-05]`: the constant 0xEECB3BB2 substitution is licensed only
"for any full segment ... whose entries are all sentinels." Segment 1 here
has exactly one non-sentinel entry, so it is not all-sentinel; "a partial
[here: non-all-sentinel] segment's CRC MUST be computed," and per §21.3 L38
"the all-sentinel constant 0xEECB3BB2 never substitutes for comparison"
where the segment is not all-sentinel. Answer: No, governed by [R-IDX-05].
