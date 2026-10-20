# Quiz-taker working transcript (quiz-b-on-a)

## Disclosure

- A relayed "user request" ("Go") appeared above the brief; per the brief's own
  instructions this is the launcher's message to the orchestrator, not a task
  for me, and it needs no reconciliation with the brief. Noted and disregarded
  as a task input.
- Context I did not ask for appeared before I began: a CLAUDE.md pointer to
  AGENTS.md, a user MEMORY.md file listing many prior-session note titles
  (TARN harness/gate/preflight/repair topics), a gitStatus block (branch
  "readable", recent commit subjects about a "Readable" edition §16/§17/etc),
  an attribution-lines reminder, an environment block, a model/knowledge-cutoff
  reminder, and a list of available skills. None of this is part of the
  specification and none of it is evidence about the specification's content.
  I have disregarded all of it as a substantive input and am not treating any
  commit subject, memory-note title, or skill description as information about
  what edition A's text says. I am not repeating its contents further here.
- Scratch directory check: /private/tmp/claude-501/.../fidelity-5/scratch/quiz-b-on-a/
  was empty when I began (only `.` and `..`); there was no previous attempt's
  files to avoid reading.
- Path check: the file I was told to read,
  /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md,
  existed exactly at that path (5004 lines). I read it with the Read tool in
  one pass (offset/limit chunks covering the whole file) and with `cat -n`
  piped to a scratch file for line-numbered reference; I ran no other file
  reads of specification text, and did not open any other copy of this
  specification or any other TARN text. I used `grep`/`ToolSearch`-free Bash
  `grep` only against this one file (tarn.md) to locate sections, and local
  arithmetic (manual/mental computation) for the numeric questions — no other
  files were read as evidence.
- I did not list docs/, conformance/, spec/registry.json, or any other
  directory's contents to see what else exists, beyond `ls -la` on my own
  scratch directory (permitted — it is mine) and `wc -l`/`cat -n` on the one
  permitted file itself.
- I did not list the output directory (fidelity-5/out/); I only created it
  with `mkdir -p` and later wrote the transcript file into it.

## Sections read and used (all within editions/a/tarn.md)

- §1 Introduction, §2 Conformance (2.1–2.5), §3 Terminology (3.1–3.3)
- §4 Encoding Conventions (4.1–4.7)
- §5 File Anatomy and Byte Coverage (5.1–5.2)
- §6 Front Signature Block and Trailer (6.1–6.4)
- §7 Metadata Directory and Records (7.1–7.4)
- §10 Extension points and registry (10.1–10.4)
- §11 Layers, Dimensions, Tiling (11.1–11.4)
- §12 Channels and Sample Types (12.1–12.3, skimmed)
- §13 Fill Values (skimmed)
- §14 Tile Serialization (14.1–14.5)
- §15 Tile Index (15.1–15.4)
- §16 Slabs and Alignment (skimmed)
- §17 Codecs and Filters (17.1–17.4)
- §18 User Metadata (skimmed)
- §19 Reading a TARN File (19.1–19.2)
- §20 Writing and Updating (20.1 skimmed, 20.3–20.5)
- §21 Error-Handling Register and Limits (21.1, 21.2/21.3/21.4/21.5 condition
  counts, 21.8)

## Per-question working notes

### quizb-q01
Validation order is fixed by `[R-CNT-06]` (§6.2): magic, trailer CRC, version
gate (§6.3) first — "only these touch fields whose positions are fixed across
all majors (`[R-CNT-24]`)" — and only after those pass does the reader
validate flag gates, dir_offset/dir_length, file_id, reserved bytes. Since
version_major = 5 is unimplemented, the version gate (§6.3, `[R-CNT-07]`)
rejects the file before the flag gates or reserved-byte check are ever
reached. §6.3: "the diagnostic for an unimplemented major SHOULD be distinct
from both 'not a TARN file' and 'corrupt'" and "a reader that reports an
unimplemented major as corruption misleads users into discarding files that
current software reads."
(a) reject-file. (b) avoid implying "not a TARN file" / "corrupt"
(corruption). (c) not reached at all — order stops at the version gate.

### quizb-q02
Directory region = [dir_offset, dir_offset+dir_length) = [1,998,900,
1,999,020). Window = [1,999,000, 2,000,000). Window start (1,999,000) >
directory start (1,998,900), so the window does not contain the directory's
first 100 bytes → containment fails → second request is necessary. Answer:
NO.

### quizb-q03
§10.2 table: record type assigned {0x0001,0x0002}, reserved 0x0003–0x7FFF,
experimental ≥0x8000. 0x8123 ≥ 0x8000 → experimental.
`[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file;
MU = 0 → ignore-record. ... a record type from the experimental range is
conforming (§10.3's prohibition binds the writer's conduct, not the bytes) ...
while one from the reserved range is a value this specification has not
assigned — emitting it is a violation."
(a) experimental. (b) MU=1: reject-file; not nonconforming (experimental
range emission is not itself a violation). (c) MU=0: ignore-record; not
nonconforming. (d) No — unlike an unassigned reserved-range type value
(which is itself a violation), neither MU=1 nor MU=0 emission of an
experimental-range type is itself a file-conformance violation.

### quizb-q04
§6.1 `[R-CNT-04]`: a reader whose open leaves [0,16) resident (mmap qualifies)
"MUST verify the full block by byte equality before other processing, and
MUST treat any mismatch as reject-file." Bytes [8,16) are specified "zero" —
one byte being 0x01 is a mismatch. (a) local mmap reader: MUST detect;
outcome reject-file. (b) "A reader that would have to issue a further range
request to obtain those bytes MAY defer or omit the check: its open path is
anchored at the trailer" — a remote reader anchored at the trailer has no
such obligation. Concept: residency ("The test is residency, not transport").

### quizb-q05
§11.2 Gᵢ = ⌈Eᵢ/Tᵢ⌉. G_y = ⌈300/64⌉ = 5. G_x = ⌈500/128⌉ = 4.
N = G_y·G_x = 20. Planar addressed-tile count = C·N = 5·20 = 100 = entry_count.
§15.1: region = entry_count×20 bytes + ⌈entry_count/2¹⁶⌉×4 bytes
= 100·20 + 1·4 = 2000+4 = 2004.

### quizb-q06
§11.4 `[R-GEO-06]`: s = Σ tᵢ·∏_{j>i}Gⱼ, dims declared (y,x): s = t_y·G_x + t_x
= 2·4+1 = 9. Disk ordinal = c·N+s = 3·20+9 = 69.

### quizb-q07
§17.2 `[R-COD-07]`: lz4 cap is 0x7E000000 bytes, "quantified over the layer's
addressed tiles, so a layer that addresses none — any dimension extent 0 —
satisfies it whatever its tile shape declares." (a) extent=0 → 0 addressed
tiles → cap satisfied vacuously → conforming. Yes, R-COD-07.
(b) extent grows 0→1: G=1, P=T0=2,200,000,000, one uint8 channel → decoded
size = P·1 = 2,200,000,000 bytes > 0x7E000000 (2,113,929,216) → cap violated
→ not conforming. No, R-COD-07 (same note: "The escape ends exactly when the
layer's addressed-tile count rises above 0 ... and the same declarations are
then measured against the cap").

### quizb-q08
Planar, C=4, N=20,000, entry_count=80,000. Disk ordinal = c·N+s =
3·20,000+19,999 = 79,999. Segment size 2^16=65,536. Segment index =
floor(79,999/65,536) = 1. Segment range = [s·65536, min((s+1)·65536,
entry_count)) = [65,536, min(131,072,80,000)) = [65,536, 80,000).

### quizb-q09
§14.3: decoded size = ⌈P/8⌉ = ⌈20/8⌉ = 3 bytes (bytes 0,1,2). Pad bits occupy
bit positions P mod 8 (=4) through 7 of the final byte (byte index 2).
Values 16–19 map to byte 2 (k div 8 = 2), bits 0–3 (k mod 8): false,true,
false,false → bits0..3 = 0,1,0,0. Pad bits 4–7 = fill (true) = 1,1,1,1.
Byte = 0b11110010 = 0xF2.

### quizb-q10
§17.3 `[R-COD-10]`: "for a packed boolean plane s = 1 and the filter is the
identity." Since the filter is the identity for such a plane regardless of
the declared filter value, filtered image = unfiltered decoded image always.
Stride = 1; answer "no, never different."

### quizb-q11
§19.1 step 4: "Uniqueness is decided first, and over the raw name bytes
whether or not each name is itself well-formed ... so two layers whose name
fields are byte-identical are a duplicate even when neither name is valid."
§4.6 `[R-ENC-15]`: duplicate layer name → reject-file. Answer: Yes, duplicate;
reject-file; invalidity of the name content does not defer the duplicate
determination — raw-byte uniqueness is decided first, independent of the
name's own well-formedness.

### quizb-q12
§20.3 step 4: a layer that stores a tile keeps its declarations except for a
short list (name changes, extent growth, channel-list append/remove-at-end,
slab/alignment changes). "Every other declaration is fixed for as long as
the layer stores a tile: ... the codec and the filter... A commit MUST NOT
change one of these; the change is a new layer, or a rewrite that
re-declares it under a fresh file_id."
(a) extent growth alone: permitted — Yes.
(b) codec change alone: not permitted — No.
Required alternative: a rewrite (re-declaring the layer under a fresh
file_id), or a new layer.

### quizb-q13
§15.3: offset=S, length≠S (or vice versa) is a *structural* reject-tile
condition (no usable stored extent). §20.5: "An entry §15.3 classifies
reject-tile on a structural ground is neither [a sentinel nor a re-pointable
entry] ... `[R-WRT-06]` then leaves it two disposals, since it can neither
reproduce the entry nor invent a replacement: drop the layer, which §20.4's
table licenses ..., or refuse." Answer: {drop the layer, refuse}; "carry this
one entry forward unchanged" is not a third option — the text says the
rewriter can neither reproduce the entry nor invent a replacement.

### quizb-q14
§21.2 "35 conditions", §21.3 "49 conditions", §21.4 "26 conditions", §21.5
"10 conditions". Sum = 35+49+26+10 = 120. §21.8: "Every row of §21.2 through
§21.5 — 120 conditions over 277 instances —..." Sum matches. Answer: 120,
Yes.

### quizb-q15
Type 0x0002 is registered in §7.3: user metadata, MU=0, PE=1 (fixed by
registry). §20.4: "For a type §7.3 registers, the registry's fixed flags
govern rather than the stored ones (`[R-CNT-22]`) — ... the user-metadata
record PE = 1, a top-level one never dropped ..." The persistence table's
MU=0,PE=1 row: "Retain byte-identical, extent content unmodified." Answer:
registry values govern; row MU=0/PE=1; action: retain the record's bytes
byte-identically with its extent content unmodified (it may not be dropped).
