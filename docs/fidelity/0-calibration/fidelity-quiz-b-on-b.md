# Quiz-taker transcript — quiz-b-on-b

## Disclosure

**Access rule compliance.** I read exactly one document file for this
exercise: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md`
(confirmed to exist at that path; 302,125 bytes, 4,977 lines). I read it via
my Read tool in several offset/limit chunks (it exceeded my single-call
token budget), covering: lines 1-900, 1655-1993 (§11-§12 start),
1993-2332 (§14-§16 start), 2425-2634 (§17), 922-967 (§6.4) and 1120-1234
(§7.4), 3187-3476 (§20.3), 3547-3731 (§20.4/20.5), 3830-3978 (§21.2-§21.4
register), 1561-1655 (§10), 2654-2843 (§18.2). I did not read any other
file: no ADRs, no PLAN.md/OPEN-QUESTIONS.md/AGENTS.md/README.md/
CONTRIBUTING.md, no conformance/ tooling or vectors, no spec/registry.json,
no git history, no other copy of the specification, no web search or
fetch. I did not list any directory other than my own scratch directory
(and a heading-only `grep -n "^###"`/`grep -n "^####"` over the one target
file to map its own internal structure, plus one `wc -l`/`ls -la` on the
target file itself — no other files were touched by these).

**Prior-attempt check.** My scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/quiz-b-on-b/`)
was empty (only `.` and `..`) when I created/checked it — no previous
attempt's files were present.

**Unsolicited context disclosure.** My runtime placed material in context
before I began that is not part of the specification and is not evidence
about it: a project `CLAUDE.md` pointer file, a user memory index of prior
TARN-project notes/lessons, and a git-status/recent-commit-subjects block.
I have disregarded all of it for the purposes of answering the slate below
and am not repeating its contents here beyond this notice. I also note the
harness's own framing text (an "ACCESS RULE" preamble, a relayed top-level
user instruction "Accept ADR-0133 and run the calibration round," and this
computed brief itself) is script/harness output, not something inside the
target document, and I have treated it as the task specification for this
subagent role, not as evidence about the document's contents.

**Path check.** The file was present exactly at the path given in the
brief (`scratch/cleanroom/editions/b/tarn.md`); no discrepancy to report.

**Hard-wrap caveat applied.** I used the Read tool (which reflows nothing
but does present the file's actual line breaks) rather than line-oriented
`grep` for locating passages, and cross-checked candidate zero-result
concerns by reading full surrounding context rather than relying on
single-line pattern matches. Where I quote decisive sentences below they
are copied from the rendered text as read (hyphenation/line-wrap artifacts
removed for readability, content unchanged).

**Local computation.** All arithmetic below was verified with a local
Python computation reading no files (shown inline per question, and run
once via Bash as an offline check — no file I/O, no network).

---

## Answers

### quizb-01

Layer: planar, rank 3, one channel, float64 (element size 8), dims all
equal to tile extents (1024, 1024, 256) — exactly one tile.

- §14.2 table, planar/numeric row: decoded size = P·Bᶜ, where P = ∏Tᵢ.
- P = 1024 × 1024 × 256 = 268,435,456.
- Decoded size = 268,435,456 × 8 = **2,147,483,648 bytes**.

Codec 4 (lz4), §17.2 `[R-COD-07]`: "Writers MUST NOT declare this codec
for a layer any of whose addressed tiles' decoded size exceeds
0x7E000000 bytes ... a reader MUST treat such a declaration as a
validity error at layer scope, checkable from declarations alone."
0x7E000000 = 2,113,929,216. Our tile's decoded size (2,147,483,648)
exceeds that cap, so declaring codec 4 here is a **validity error**.
Outcome class: **reject-layer** (register row L44, §21.3: "Codec 4
(lz4) declared on a layer any of whose addressed tiles' decoded size
exceeds 0x7E000000 bytes ... Outcome: reject-layer"). Owning scope:
**layer**.

**Answer:** 2,147,483,648 bytes; validity error — reject-layer, layer scope.

---

### quizb-02

§6.1 `[R-CNT-04]`: "A reader whose open leaves bytes [0, 16) resident —
a local file read whole, a memory mapping, a speculative suffix window
that reached offset 0, or any transport already holding them — MUST
verify the full block by byte equality before other processing... A
reader that would have to issue a further range request to obtain those
bytes MAY defer or omit the check."

The reader's single request is the suffix range [9700, 10000) of a
10,000-byte file — it does not reach offset 0, so bytes [0, 16) are not
in the fetched buffer.

**Answer:** (a) not resident; (b) MAY defer or omit.

---

### quizb-03

§7.4 `[R-CNT-17]`: "Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0)
... a mismatch ... is a validity error at layer scope."

entry_count = 1: correct extent_length = 1×20 + ⌈1/65536⌉×4 = 20 + 4 = 24.

Declared extent_length is 40 ≠ 24.

Register row: §21.3 L22 — "Under index_encoding 1, extent_length ≠
entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 ... " Governing rule
`[R-CNT-17]`.

**Answer:** No; correct extent_length = 24; row L22.

---

### quizb-04

Layer: interleaved, rank 2, dims declared (y: extent 500, tile 128),
then (x: extent 500, tile 128); channels declared (a: int16), then
(b: uint8). Linearization 1 (row-major, last-declared dimension varies
fastest) — §11.4.

Coordinate (y, x) = (130, 260):
- tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ (§11.4): u_y = 130 mod 128 = 2;
  u_x = 260 mod 128 = 4.
- In-tile sample ordinal = Σᵢ uᵢ·∏_{j>i}Tⱼ = u_y·T_x + u_x
  = 2×128 + 4 = 260.

§14.2 table, interleaved row: "Offset of value k = (k div C)·Q + F_{k mod C}",
and the worked-example restatement: "channel c's value at in-tile
ordinal u sits at byte u · Q + Fᶜ."
- Q (sample stride) = size(a) + size(b) = 2 + 1 = 3.
- F_b (channel b's in-sample offset) = size(a) = 2 (sum of element
  sizes of channels before b, i.e. just `a`).
- Offset = u·Q + F_b = 260×3 + 2 = **782**.

**Answer:** 782.

---

### quizb-05

Layer: 2 dims, extents (7,7), tile extents (5,5); one uint16 channel,
fill 0xBEEF. Tile (1,1) — high edge on both axes.

§11.2: grid count Gᵢ = ⌈Eᵢ/Tᵢ⌉ = ⌈7/5⌉ = 2 per axis. Tile (1,1) covers
coordinates [5,10) along each axis; only coordinates < 7 are real, so 2
real positions per axis (5,6), 3 padding positions per axis (7,8,9-slots,
i.e. local indices 2,3,4 of the tile). Tile P = 5×5 = 25 total sample
positions; real (in-extents) positions = 2×2 = 4; padding positions =
25 − 4 = **21**.

§14.5 `[R-SER-05]`: "at every padding position, a writer MUST encode,
for each channel the position carries, that channel's fill value — the
recorded fill bytes for a numeric channel..." §4.1 `[R-ENC-01]`: all
multi-byte values little-endian. uint16 fill 0xBEEF encodes
little-endian as low byte then high byte: 0xEF, 0xBE.

**Answer:** 21 padding positions; stored bytes **EF BE**.

---

### quizb-06

Planar layer, channels r (uint8, fill 10), g (uint8, fill 20), b
(uint8, fill 30). At the given spatial ordinal: r's tile stored,
decodes to 200; g's tile at that ordinal is the sentinel (unstored); b's
tile stored, decodes to 5.

§3.2 `[R-MDL-01]` / §13.3 `[R-TYP-08]`: "in a planar layer exactly the
entry's channel reads as fill there, and a single sample can mix decoded
and fill channels." g is unstored at this ordinal, so g reads as its
fill value (20); r and b are stored and decoded normally.

**Answer:** (200, 20, 5).

---

### quizb-07

Planar bool channel whose tile is a packed boolean plane (§14.3), filter
2 (byte-shuffle) declared.

§17.3: "Byte-shuffle. The shuffle stride s is the channel's element size
for a planar tile and the sample stride Q for an interleaved tile
(§14.2); for a packed boolean plane s = 1 and the filter is the
identity." — stated explicitly and directly for exactly this case.

**Answer:** stride s = 1; effect: identity — the bytes are unchanged.

---

### quizb-08

A verifier declines one stored tile's decode purely on resource grounds
during its coverage walk, and establishes no other violation anywhere.

§2.3 `[R-CNF-11]`: a verifier reports *cannot establish* "where some
requirement is one it is unable to check on a capability or resource
ground, as when ... it declines a layer's or a tile's decode on resource
grounds and so cannot check §14's decoded-content obligations
(`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`) ... Cannot establish is not a
finding that the file is nonconforming ... available only to a traversal
that established no violation." No other violation was established here,
so the verdict is **cannot establish**.

On the slack total: §5.2 `[R-CNT-21]`: "a tile's or a document's decode
declined leaves the walk complete, that claimant being enumerated from
its index entry or extent slot." A declined single-tile decode does not
make the walk incomplete (unlike declining a whole layer on resource
grounds, or a scope-level rejection). So the slack total is reported as
**complete**.

**Answer:** cannot establish; complete.

---

### quizb-09

Tile-index entry: offset = sentinel (0xFFFF...FFFF), length = 100
(non-sentinel), crc = 0.

§15.3 entry-validity table, row: "offset = S ∧ length ≠ S, or
offset ≠ S ∧ length = S | *structural*: reject-tile" — this is exactly
this entry's state (exactly one field at the sentinel value). Register
row T7 (§21.4): "A tile-index entry sets exactly one of offset and
length to the sentinel value ... `[R-IDX-03]`."

§15.3 preamble: "Six rows are marked *structural*: they classify an
entry whose own 20 bytes yield no usable extent. Such an entry
contributes no stored extent to the *verifier* rows ... and none to
`[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed that
no other claimant claims fall to slack."

**Answer:** outcome class **reject-tile**; **structural**; the bytes it
nominally addresses **fall to slack** (it contributes no claimant to the
coverage walk).

---

### quizb-10

Planar layer stored ≥1 tile in the superseded generation, channels
(p, q, r). Commit's only change: insert new channel 's' between q and r
(not at the end).

§20.3 step 4, the fixed-declarations paragraph: "a planar layer's
channel list MAY be extended at its end or shortened from its end, but
not both in one commit... Every other declaration is fixed for as long
as the layer stores a tile ... A commit MUST NOT change one of these;
the change is a new layer, or a rewrite." And explicitly, in the "What
the line gives up" paragraph: "a planar channel inserted or removed
anywhere but the end of the list ... are rewrites even where a
particular file would survive them in place, because deciding which
files would is the edge this list exists to remove."

Inserting a channel in the middle of the list is exactly this excluded
case.

**Answer:** not permitted as an appender commit — requires a new layer
or a rewrite.

---

### quizb-11

Rewriter performing pure compaction: every stored tile's bytes, every
index entry's offset/length/crc, and every retained record's content
carried forward completely unchanged; only byte placement differs.

§20.5 `[R-WRT-07]` (and surrounding text): "It MUST mint a fresh file_id
for the output — a new draw under §9.3's randomness advice, not merely a
value compared against the input's: a rewritten file is a whole-file
rewrite under a new file_id by definition (`[R-LIF-01]`), and reusing
the input's would break the (file_id, range) cache contract of
`[R-LIF-03]`, since relocation puts different bytes at the same ranges."
This applies even to compaction, which the same section names as one of
the three named rewrite operations and which still relocates bytes
("carries every structure forward and changes nothing but placement").
Byte-for-byte identical decoded content does not exempt a rewrite from
minting a fresh file_id.

**Answer:** False.

---

### quizb-12

Directory region's final 4 bytes correctly equal CRC-32C of the
preceding dir_length − 4 bytes. Trailer declares version_major = 2
(not implemented, and not 0).

§6.2 `[R-CNT-06]`: "A reader MUST validate, in order: the trailer magic;
the trailer CRC; the version gate (§6.3) — only these touch fields whose
positions are fixed across all majors (`[R-CNT-24]`) — and then, those
gates passed, MUST validate all of the following before acting on the
fields involved: the flag gates (§6.3); committed_file_length ... ;
dir_offset ...; dir_length ...; ... " The version gate is validated
before dir_offset/dir_length are acted on, and long before the directory
region itself is fetched (§7.1). §6.3 `[R-CNT-07]`: "A reader MUST
reject-file when version_major is 0 (invalid) or is a major it does not
implement."

Since version_major = 2 is a major this reader does not implement, the
reader rejects at the version gate and never proceeds to validate
dir_offset/dir_length, let alone fetch and verify the directory region's
CRC. The directory region's own correctness is irrelevant — the reader
never gets there.

**Answer:** No; the reader stops at the version gate (§6.3,
`[R-CNT-07]`), during trailer validation, before the directory step.

---

### quizb-13

Slab, run length S = 8, run covers disk ordinals [40, 48). Ordinal 42's
entry: length = 0 (non-sentinel), classified structural (§15.3: "length
= 0 (non-sentinel) | *structural*: reject-tile"). Ordinal 44: valid
sentinel. All others (40,41,43,45,46,47): normal, well-formed, stored.

§16.2 `[R-SLB-03]`: "Sentinel tiles are transparent to run continuity:
they occupy no bytes and do not break packing. So are the entries
§15.3 classifies reject-tile on a *structural* ground: they address no
usable extent, and the run's stored tiles close over them." Also §15.3
preamble: such structural entries "contribute no stored extent to the
*verifier* rows, which bind over well-formed entries' extents only —
`[R-SLB-03]`'s run continuity closes over it as it does over a
sentinel."

Ordinal 42's structurally-invalid entry is therefore transparent to run
continuity, exactly like a sentinel — it does not, by itself, break the
invariant.

**Answer:** No.

---

### quizb-14

Appender's commit supersedes one stored tile in a layer whose tile
index has >1 CRC segment (entry_count > 65,536); the superseded tile's
entry is in segment 2; segment 0 is untouched in value/position but the
whole tile-index region (all segments) is re-emitted, with segment 0's
entries copied forward byte-identically.

§20.3 `[R-WRT-03]`: "An updater's verification depth follows reliance
... the §19.4 index chain for every segment whose entries the commit
reuses (`[R-IDX-04]`). Structures the commit neither modifies nor
relies on impose no further obligation."

Segment 0's entries are reused — they are read and copied forward
byte-identically into the new tile-index region — so the appender
relies on them, and `[R-WRT-03]` obliges verifying "the §19.4 index
chain" for that segment, i.e. §15.4 `[R-IDX-04]`'s crc_of_crc_array
cross-check and the segment's own CRC, before re-emitting it.

**Answer:** Yes.

---

### quizb-15

§10.2 table and its note: "Every numeric identifier space is
partitioned identically: values this specification assigns; a
**reserved** range only this specification assigns from; and an
**experimental** range for private use... One space carries no
experimental range: channel layout, whose `u8` field is too narrow to
spare one, 3 through 255 staying reserved to this specification."

Channel layout: Assigned {1,2}; Reserved {3–255}; Experimental: none.

A writer's channel layout field holding 200 falls in 3–255, which is
entirely the **reserved** range (there being no experimental range to
compete for it).

**Answer:** channel layout; reserved.

---

## Arithmetic verification (local computation, no file I/O)

```
P (Q1) = 1024*1024*256 = 268435456
decoded (Q1) = P*8 = 2147483648
cap (Q1) = 0x7E000000 = 2113929216
2147483648 > 2113929216  → True (exceeds cap)

Q3: entry_count=1 → 1*20 + ceil(1/65536)*4 = 20 + 4 = 24

Q4: u_y = 130 % 128 = 2; u_x = 260 % 128 = 4
    in_tile_ordinal = 2*128 + 4 = 260
    Q = 2 (int16) + 1 (uint8) = 3
    F_b = 2 (size of channel a, which precedes b)
    offset = 260*3 + 2 = 782

Q5: G = ceil(7/5) = 2
    valid_per_axis = 7 - (2-1)*5 = 2
    valid = 2*2 = 4; P_tile = 5*5 = 25; padding = 25-4 = 21
    fill 0xBEEF little-endian bytes: 0xEF, 0xBE
```
