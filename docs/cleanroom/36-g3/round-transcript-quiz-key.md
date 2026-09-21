# Cleanroom round 36 — quiz keyer transcript

## Disclosure of process

**File read.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(confirmed present at the path the brief named — no path discrepancy; 4,981 lines, ~302 KB).
I read it in full, sequentially, via the Read tool in ~500-line windows, and used `grep`
against that same file once, only to locate the appendix section headers (a structural
navigation aid, not a content search whose zero I relied on). I ran no other `grep`/`rg`
searches that returned zero and no conclusion in this transcript rests on an unconfirmed
zero-result search — every substantive citation below is anchored to text I read directly
in the numbered-line windows.

**Scratch directory.** I created `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-round/scratch/quiz-keyer/`
myself; it was empty when I began (verified with `ls -la` before writing anything), so there
is no earlier attempt's files to disclose. I wrote two files there: `crc32c.py` (a
CRC-32C implementation used for Q1/Q3/Q4, validated against this specification's own
§4.5 check vectors — CRC-32C("123456789") = 0xE3069283 and CRC-32C(zero bytes) =
0x00000000 — before use, and additionally cross-checked by reproducing Appendix A's
stated trailer CRC 0x402F157E exactly) and `notes.md` (scratch arithmetic for Q2/Q8/Q9).
These scripts read no files; all input bytes are hard-coded from the question text and
from spec passages I had already read. I did not read or execute any file that might
already have been in that directory (there were none), and I did not write to its parent
or to any shared directory. I also wrote nothing to the round's `out/` directory except
this transcript, and I did not list or read the `out/` directory's other contents.

**Context I did not ask for.** Before this task began, my context already contained: (1)
a `CLAUDE.md` project-instructions stub pointing to `AGENTS.md` (I did not read `AGENTS.md`
— it is out of scope under the access rule); and (2) a personal memory file
(`MEMORY.md`) listing roughly twenty short bullet-point titles about prior TARN rounds —
things like a "harness spec path" note, a claim that a "lineage gate word list" file is
missing, a note about "repair prose vs rules," "subagents on Opus," "no nested em-dash
phrases," and similar titles referencing earlier rounds' findings and process quirks.
I did not open, follow, or rely on any of the linked memory files behind those bullets,
and no answer below was chosen, adjusted, or double-checked because of anything in that
list — I disregarded it entirely, per the brief's instruction, and note here only that it
appeared, not what it said beyond the bullet titles already quoted to me. Also present were
routine harness/tooling system reminders (git status, environment paths, available skills,
attribution footer instructions) which are operational, not evidentiary about the
specification, and are likewise disregarded as evidence about the document's content.

**Paths.** The one file I was told to read was exactly where the brief said it would be;
no discrepancy to report.

---

## Q01 — Trailer CRC with file_id = all-ones

Trailer layout (§6.2): magic(8) · version_major(2) · version_minor(2) · flags(4) ·
dir_offset(8) · dir_length(8) · committed_file_length(8) · file_id(8) · reserved(12) ·
CRC(4), CRC-32C over bytes [0,60). Appendix A gives the baseline 128-byte file's trailer
bytes explicitly, including file_id `EF CD AB 89 67 45 23 01` (= 0x0123456789ABCDEF LE)
and trailer CRC `7E 15 2F 40` (= 0x402F157E), "over trailer bytes [0, 60)".

I reproduced the Appendix A trailer's 60 covered bytes exactly (magic `8A 4E 52 41 54 0D
0A 1A`; version_major=1; version_minor=0; flags=0; dir_offset=16; dir_length=4;
committed_file_length=128; file_id=0x0123456789ABCDEF; reserved=12 zero bytes) and ran
them through a CRC-32C implementation built to §4.5's exact definition (Castagnoli
polynomial 0x1EDC6F41, reflected in/out, init/final XOR 0xFFFFFFFF). It produced
0x402F157E, i.e. stored bytes `7E 15 2F 40` — matching Appendix A byte for byte. This
both validates the implementation and confirms the field layout used.

Substituting file_id = 0xFFFFFFFFFFFFFFFF (all other trailer fields unchanged, per the
question) and recomputing CRC-32C over the resulting 60 bytes gives 0xD5AAC65C.

**Arithmetic (from script):**
```
trailer[0:60] = 8A 4E 52 41 54 0D 0A 1A  01 00  00 00  00 00 00 00
                10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
                80 00 00 00 00 00 00 00  FF FF FF FF FF FF FF FF
                00 00 00 00 00 00 00 00 00 00 00 00
CRC32C(trailer[0:60]) = 0xD5AAC65C
stored little-endian: 5C C6 AA D5
```

**Answer: `5C C6 AA D5`**
Citations: §6.2 (trailer layout, "trailer CRC | structural | CRC-32C over trailer bytes
[0, 60)"); §4.5 (`[R-ENC-09]`, CRC-32C definition and check vectors); Appendix A (baseline
bytes and CRC, used as the validated starting point).
Confidence: high.

---

## Q02 — Planar layer tile-index entry: disk ordinal, segment, byte offset

Planar, rank 1, one dimension extent 200,000, tile extent 1 ⇒ grid count G = 200,000 = N
(spatial-tile count, §11.2). Channel count C = 2, so addressed-tile count = C·N = 400,000
= entry_count, consistent with the question. index_encoding 1.

§11.4 (`[R-GEO-06]`): "The disk tile ordinal, which orders tile-index entries (§15), is s
for an interleaved layer, and **c · N + s** for a planar layer (§14), where c is the
channel's index." For channel c = 1, spatial ordinal s = 150,000:

(a) disk ordinal = 1 × 200,000 + 150,000 = **350,000**.

§15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))" — the fixed
2¹⁶ = 65,536 entries-per-segment rule.

(b) segment number = ⌊350,000 / 65,536⌋. 65,536 × 5 = 327,680 ≤ 350,000 < 393,216 =
65,536 × 6, so segment = **5**.

§15.1 (`[R-IDX-01]`): "The entry for the tile with disk ordinal k (§11.4) is the k-th
entry, at region byte 20·k."

(c) byte offset from the start of the entry array = 20 × 350,000 = **7,000,000**.

**Arithmetic:**
```
disk ordinal = 1*200000 + 150000 = 350000
segment = 350000 // 65536 = 5  (327680 <= 350000 < 393216)
offset  = 20 * 350000 = 7,000,000
```

**Answer: 350000, 5, 7000000**
Citations: §11.4 `[R-GEO-06]` (disk ordinal formula c·N+s); §15.4 `[R-IDX-04]`/segment
definition (2¹⁶ entries per segment, "the s-th u32 of the segment CRC array"); §15.1
`[R-IDX-01]` (entry k at region byte 20·k).
Confidence: high.

---

## Q03 — All-sentinel 3-entry index: segment CRC and crc_of_crc_array

§15.2: sentinel entry is the 20 bytes `FF ×16 00 ×4` (offset=length=2⁶⁴−1, crc=0).
Three sentinel entries concatenated = 60 bytes, still inside a single, non-full segment
(3 < 2¹⁶), so §15.4's "a partial segment's CRC MUST be computed" — the all-sentinel
constant 0xEECB3BB2 applies only to a **full** (2¹⁶-entry) all-sentinel segment
(`[R-IDX-05]`), which this is not.

(a) CRC-32C of the 60-byte entry array (three sentinels back to back):
```
entry_array = (FF*16 + 00*4) * 3   # 60 bytes
CRC32C(entry_array) = 0xD171D122
stored LE: 22 D1 71 D1
```
This is the layer's one segment CRC (§8.1: "Tile-index region | the per-segment CRC
array... | index entries, per segment").

(b) crc_of_crc_array (§7.4): "CRC-32C over the index's segment-CRC array (§15)." With
only one segment, the segment-CRC array as stored is exactly those same 4 bytes
(`22 D1 71 D1`):
```
CRC32C(22 D1 71 D1) = 0x34C74AFB
stored LE: FB 4A C7 34
```

**Answer: (a) `22 D1 71 D1`  (b) `FB 4A C7 34`**
Citations: §15.2 (sentinel bit pattern); §15.4 (`[R-IDX-04]`, `[R-IDX-05]`, per-segment
CRC and the full-segment-constant carve-out that does not apply here); §7.4 (crc_of_crc_array
definition); §8.1 (coverage map row for the tile-index region and its segment-CRC array).
Confidence: high.

---

## Q04 — Interleaved byte layout and byte-shuffle

§14.1 (`[R-SER-01]`): interleaved value sequence is sample-major, C=2 channels (a:int16,
b:uint8), Q = Σ Bᵢ = 2+1 = 3 (§14.2). Value k's offset = (k div C)·Q + F_{k mod C}, with
F_a=0, F_b=2. At ordinal 0: a-bytes `34 12`, b-byte `AB`; at ordinal 1: a-bytes `78 56`,
b-byte `CD`.

(a) Decoded tile image (6 bytes, byte order): position 0 occupies bytes [0,3) = a(2) + b(1),
position 1 occupies bytes [3,6):
```
34 12 AB 78 56 CD
```

§17.3 (`[R-COD-10]`): "The shuffle stride s is ... the sample stride Q for an interleaved
tile" ⇒ s = Q = 3, L = 6, n = L/s = 2. "the filtered image places byte i of group j at
offset i · n + j."

(b) Grouping the 6-byte decoded image into n=2 groups of s=3 bytes: group0 = `34 12 AB`,
group1 = `78 56 CD`. Filtered[i·n+j] = decoded[j·s+i]:
```
i=0: filtered[0]=decoded[0]=34 ; filtered[1]=decoded[3]=78
i=1: filtered[2]=decoded[1]=12 ; filtered[3]=decoded[4]=56
i=2: filtered[4]=decoded[2]=AB ; filtered[5]=decoded[5]=CD
```
Filtered (stored) bytes: `34 78 12 56 AB CD`.

**Answer: (a) `34 12 AB 78 56 CD`  (b) `34 78 12 56 AB CD`**
Citations: §14.1 `[R-SER-01]` (value sequence, sample-major interleaved order); §14.2
`[R-SER-02]` (byte-layout table, Q and offset formula); §17.3 `[R-COD-10]` (byte-shuffle
stride = Q for interleaved, and the i·n+j placement rule).
Confidence: high.

---

## Q05 — Local reader, front-block reserved bytes nonzero

§6.1: front signature block bytes [8,16) are "zero," class structural. "A reader whose
open leaves bytes [0, 16) resident ... MUST verify the full block by byte equality before
other processing, and MUST treat any mismatch as reject-file." (`[R-CNT-04]`) A
memory-mapped/local-file reader is squarely the example given for "resident." The magic
[0,8) is correct here, but the reserved bytes [8,8+8) are not all zero, so the 16-byte
block as a whole is "not byte-identical to the constant."

§21.2 row F6: "The 16-byte front signature block is not byte-identical to the constant;
the obligation binds a reader holding those bytes resident... Detector: reader; Detected:
open; Governing rule: `[R-CNT-04]`." This is the general "block mismatch" row; F1 is
narrower (a *byte-reversed* signature specifically, an endian-swap scenario), which does
not describe this case (bytes are not reversed, just not all zero in the reserved half).

**Answer: verdict = `reject-file`, register row = `F6`**
Citations: §6.1 (front block layout and `[R-CNT-04]`'s residency-triggered equality
check); §21.2 row F6.
Confidence: high.

---

## Q06 — Stored-tile extent overlapping the directory region

Trailer: F=1,000,000, dir_offset=999,800, dir_length=136 ⇒ directory occupies
[999,800, 999,936) and 999,800+136 = 999,936 = F−64 exactly (bound satisfied, §6.2).
A layer's stored-tile index entry addresses [999,780, 999,850) — the question stipulates
every per-entry bound of §15.3 (offset≥16, offset+length≤F−64, etc.) is independently
satisfied, so the entry is a *well-formed* (non-structural-defect) entry whose extent
"overlaps the directory region on bytes [999,800, 999,850)."

§15.3's verifier rows: "a stored extent overlaps its own layer's index region or
sub-record extents | *verifier*: reject-layer" (intra-layer) vs. "a stored extent overlaps
any structure outside its own layer | *verifier*: reject-file." The directory is not part
of any layer — it is a file-scope structure (§5.2's structure classes: "a stored-tile
extent, a record extent..., the directory, or the trailer"). So this is the *outside-its-
own-layer* case: reject-file.

§21.2 row F33 states exactly this pairing: "A byte of the live committed state is claimed
by two structures that do not belong to the same layer — across two layers, a layer
structure against another scope's structure, or two structures neither of which belongs
to a layer... | verifier | certification | `[R-CNT-13]`." The stored-tile extent (a layer
structure) against the directory (another scope's structure) is exactly "a layer
structure against another scope's structure."

**Answer: verdict = `reject-file`, register row = `F33`**
Citations: §5.2 (`[R-CNT-02]`, structure classes: directory is not a layer structure);
§7.2 (`[R-CNT-13]`, extent-ownership rule, "any overlap across layers or touching another
scope's structures as reject-file"); §15.3 (verifier row: overlap outside own layer ⇒
reject-file); §21.2 row F33.
Confidence: high.

---

## Q07 — One commit: shorten then extend a planar channel list

§20.3 step 4 (`[R-WRT-04]`), on what a layer that stored a tile in the superseded
generation may have changed in one commit: "a planar layer's channel list MAY be
extended at its end or shortened from its end, but not both in one commit." And more
explicitly: "A commit MAY make several of these changes at once, an extension and a
shortening of one channel list excepted: a commit that shortens a planar layer's channel
list appends no channel to it and one that extends it removes none, whatever the counts,
**so replacing the last channel, or any run of channels at the end, is two commits or a
rewrite**."

The question's scenario — remove the last channel, then append one new channel, net
count unchanged, all in one commit — is exactly "replacing the last channel ... in one
commit," which this passage names directly as *not* a single-commit operation.

**Answer: `not permitted`; the two named alternatives are `two commits` and `a rewrite`.**
Citation: §20.3 step 4 (`[R-WRT-04]`), decisive sentence quoted above.
Confidence: high.

---

## Q08 — Interleaved lz4 layer: decoded size and cap conformance

Interleaved, rank 3, tile extents 1024×1024×1024 and dimension extents identical ⇒
G=1 in each dim, N=1. P = ∏Tᵢ = 1024³ = 1,073,741,824 (§11.2). Two uint32 channels,
each element size 4 ⇒ Q = ΣBᵢ = 8 (§14.2).

(a) §14.2 table, interleaved decoded size = P·Q = 1,073,741,824 × 8 = **8,589,934,592
bytes**.

(b)/(c) §17.2 (`[R-COD-07]`), codec 4 (lz4): "Writers MUST NOT declare this codec for a
layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes... and a
reader MUST treat such a declaration as a validity error at layer scope." 0x7E000000 =
2,113,929,216. 8,589,934,592 > 2,113,929,216, so the declaration is **not conforming**
(answer: no). §21.3 row L44 names this exact condition: "Codec 4 (lz4) declared on a
layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes... | reader |
layer access | `[R-COD-07]`."

**Arithmetic:**
```
P = 1024^3 = 1,073,741,824
Q = 4 + 4 = 8
decoded_size = P*Q = 8,589,934,592
cap = 0x7E000000 = 2,113,929,216
8,589,934,592 > 2,113,929,216  -> violates cap
```

**Answer: (a) 8589934592  (b) no  (c) L44**
Citations: §11.2 (grid/P arithmetic); §14.2 `[R-SER-02]` (interleaved decoded size = P·Q);
§17.2 `[R-COD-07]` (lz4 cap 0x7E000000); §21.3 row L44.
Confidence: high.

---

## Q09 — Spatial tile ordinal under row-major linearization

Dimensions declared z, y, x with extents 4,4,4 and tile extents 1,1,1 ⇒ Gz=Gy=Gx=4
(§11.2). §11.4 (`[R-GEO-06]`): "Under linearization 1, the spatial tile ordinal of
(t₀, …, t_{d−1}) is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ" with dimensions in declared order (index 0=z,
1=y, 2=x — "the last-declared dimension varies fastest").

For (t_z,t_y,t_x) = (1,2,3):
```
s = t_z*(G_y*G_x) + t_y*(G_x) + t_x*1
  = 1*(4*4) + 2*4 + 3
  = 16 + 8 + 3
  = 27
```

**Answer: 27**
Citation: §11.4 `[R-GEO-06]` (spatial tile ordinal formula and its worked example
pattern, e.g. "tile (1, 0) → 1·8 + 0 = 8").
Confidence: high.

---

## Q10 — Verifier declines a 20 MiB zstd user-metadata document at a 16 MiB bound

§18.2 (`[R-MTA-09]`): "a reader decodes with a bound of its own choosing, no smaller than
§21.9's user-metadata guarantee" (16 MiB, §21.9), and "A **verifier** that declines to
decode a document on either bound above cannot establish that document's conformance and
MUST NOT certify the file... the decline is not a finding that the file is
nonconforming... Any violation here is ignore-record, never the tile-scope outcome §17.2
assigns." The verifier here set its bound at exactly 16 MiB (the §21.9 minimum, no
larger — a permitted choice, "no smaller than," and 16 MiB itself is not smaller) and the
document is 20 MiB, so it declines. The document itself is otherwise fully valid, so
nothing here is a file-conformance violation — it is a resource decline.

(1) §2.4's outcome-class vocabulary for "the record is skipped as though absent" is
**ignore-record** — exactly the term `[R-MTA-09]` names ("Any violation here is
ignore-record").

(2) §2.3 (`[R-CNF-11]`): a verifier reports one of three verdicts — *conforming*,
*nonconforming*, or *cannot establish* — "the last where some requirement is one it is
unable to check on a capability or resource ground... [including] when it declines to
decode a user-metadata document (`[R-MTA-09]`)... An established violation takes
priority... *cannot establish* is available only to a traversal that established no
violation." The question stipulates the verifier "establishes no other violation
anywhere else in the file," so the decline (a resource ground, not a violation) fixes the
verdict as **cannot establish**.

**Answer: (1) `ignore-record`  (2) `cannot establish`**
Citations: §18.2 `[R-MTA-09]` (resource-bound decline is ignore-record, verifier "MUST
NOT certify"); §21.9 (16 MiB minimum guarantee for user-metadata decoded size); §2.3
`[R-CNF-11]` (three verdicts; cannot-establish only absent an established violation).
Confidence: high.

---

## Q11 — Registered layer record re-emitted byte-identically with mismatched MU/PE

§7.3 registers layer records (type 0x0001) with fixed flags MU=0, PE=0. §7.3
(`[R-CNT-22]`): "For the record types this specification registers, writers MUST emit
exactly the flag values fixed in the table above... A stored-flag mismatch on a
registered type makes the file nonconforming (`[R-CNF-05]`); conforming readers
nevertheless process the record under the fixed semantics... whose detection this
specification likewise assigns to the verifier."

(a) Because the stored MU=1/PE=1 differs from the registry-fixed MU=0/PE=0, and
`[R-CNT-22]` states this "makes the file nonconforming," the file after the
byte-identical re-emission is **not conforming** — re-emitting it unchanged (§20.4,
`[R-WRT-05]`: an updater re-emits byte-identically a record it does not logically modify)
carries the pre-existing violation into the new generation; "a violation latent in a
structure it carries forward unmodified travels with it" (§20.1, `[R-WRT-01]`).
Answer: **no**.

(b) "A reader MUST apply a known type's specified semantics regardless of its stored MU
and PE bits — a flipped stored bit never changes conforming behavior" (§7.3,
`[R-CNT-22]`). A conforming reader is *not* obligated to refuse the layer's data on this
ground; it serves the layer exactly as if MU=0/PE=0 had been stored. Answer: **no**.

(c) §21.3 row L49: "A layer record, or a sub-record of a type §7.3 registers, carries a
stored MU or PE bit differing from the value the registry fixes; readers apply the
type's fixed semantics regardless | verifier | certification | `[R-CNT-22]`." This is
exactly the condition described.

**Answer: (a) no  (b) no  (c) L49**
Citations: §7.3 `[R-CNT-22]` (registered-type flag mismatch: file nonconforming, reader
behavior unchanged); §20.1 `[R-WRT-01]`, §20.4 `[R-WRT-05]` (byte-identical re-emission
of an unmodified record, and that a latent violation travels forward); §21.3 row L49.
Confidence: high.

---

## Q12 — Coverage-map bytes for an unassigned reserved-range record type

§8.1's coverage map explicitly rows: "Extent of a record of a type this specification
has not assigned | none — the bytes are opaque (§7.2) | —." §8.1 preamble likewise:
"the extent of a record of a type this specification has not assigned, in which this
specification defines no fields (§4.7) and whose bytes it leaves opaque (§7.2)." Type
0x1234 lies in the reserved range 0x0003–0x7FFF (§10.2), which this specification "has
not assigned" — so this row applies regardless of the record's MU bit (MU is about
reader accept/reject behavior, not about checksum coverage).

**Answer: 0**
Citations: §8.1 (coverage map row for an unassigned record type's extent, and preamble
"whose bytes it leaves opaque, §7.2"); §10.2 (reserved range 0x0003–0x7FFF is
unassigned).
Confidence: high.

---

## Q13 — dir_offset + dir_length exceeds F − 64

F=1,000,000, dir_offset=999,900, dir_length=140. F−64 = 999,936. dir_offset+dir_length =
1,000,040 > 999,936 — violates §6.2's bound "dir_offset + dir_length ≤ F − 64" among the
ordered gates `[R-CNT-06]` requires a reader to validate at open. (All other trailer
fields validate correctly per the question, so this is the sole failing gate.)

§21.2 row F10: "Trailer dir_offset + dir_length exceeds F - 64, so the declared directory
region runs into or past the live trailer | reader | open | `[R-CNT-06]`." This matches
exactly (1,000,040 runs 104 bytes past F−64).

**Answer: verdict = `reject-file`, register row = `F10`**
Citations: §6.2 (`[R-CNT-06]`, ordered validation list including "dir_offset + dir_length
≤ F − 64"); §21.2 row F10.
Confidence: high.

---

## Q14 — Appender renames a layer only, no other change

§20.3 step 4 permits "its name, and its dimension and channel names, MAY change" for a
layer that stored a tile in the superseded generation, and states: "A layer whose record
alone changes keeps its extent slot, pointing at the existing region, as does a layer
the commit leaves untouched (`[R-WRT-05]`); relocating a live index region is a
rewriter's operation (§20.5, `[R-WRT-07]`), not an appender's." Renaming touches only the
name field of the layer record; geometry, channels, codec/filter, and the stored-tile set
and index content are unchanged by hypothesis — so nothing here changes the layer's
index content, and the extent slot (hence the tile-index region's placement) is
untouched.

§20.3's worked example enumerates three shapes, and explicitly places "renaming a layer"
under shape (c): "**(c) A change confined to the directory** — clearing a slab
declaration, renaming a layer, or dropping a layer or another PE = 0 record ... Only the
directory is re-emitted." Shape (c)'s figure shows the layer's tiles+index region
untouched across the commit, with only the directory (dir/pad/trailer) re-emitted.

**Answer: `no`; shape `c`.**
Citations: §20.3 step 4 (`[R-WRT-04]`/`[R-WRT-05]`, permitted rename and unchanged extent
slot for a record-only change); §20.3's worked example, shape (c) (explicitly names
"renaming a layer").
Confidence: high.

---

## Q15 — Byte-shuffle applied at the wrong stride, no padding, no boolean channel

Filter=2 byte-shuffle, interleaved, channels a,b both uint16 (element size 2 each) ⇒
mandated stride s = Q = 4 (§17.3). Writer applies the filter at stride 2 instead — a
violation of §17.3 (`[R-COD-10]`): "A writer that filters with any other stride violates
this rule; where the resulting decoded image breaks a stated content obligation (§14.5's
padding, `[R-SER-08]`'s bool bytes) a verifier detects it as a validity error at tile
scope, and otherwise the consequence is wrong sample content — undetectable by
construction (§21.7)."

The tile in question has *no* padding positions at all (tile extent evenly divides the
corresponding dimension extents) and neither channel is boolean, so neither of the two
structural tripwires — §14.5's fixed padding content or `[R-SER-08]`'s fixed
interleaved-bool byte values — is engaged; there is no other structural constraint this
specification places on ordinary (non-padding, non-boolean) sample bytes (§21.7: "this
format detects corruption of structure, not incorrectness of content... Checksums are
computed over what the writer wrote"). §21.3 row T26 states the same disjunction
directly: "Filter 2 applied at a stride other than the mandated one, where the resulting
image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes (**a wrong stride with
no such structural constraint is undetectable, §21.7**)."

§21.7 is the section that states this class of condition escapes every check: it defines
"unwitnessed" conditions ("for every file exhibiting it, some file that does not exhibit
it cannot be told apart from it by any check this specification obliges a reader or a
verifier to perform") and states plainly that "this format detects corruption of
structure, not incorrectness of content... produces a file that every checksum in §8
certifies."

**Answer: `undetectable`, §21.7**
Citations: §17.3 `[R-COD-10]` (wrong-stride rule and its "undetectable by construction,
§21.7" clause); §21.3 row T26 (same disjunction, explicit "no such structural constraint
is undetectable" parenthetical); §21.7 (the section stating the general test and the
"detects corruption of structure, not incorrectness of content" principle).
Confidence: high.

---

## Summary table

| Q | Answer |
|---|---|
| 1 | `5C C6 AA D5` |
| 2 | 350000, 5, 7000000 |
| 3 | (a) `22 D1 71 D1`  (b) `FB 4A C7 34` |
| 4 | (a) `34 12 AB 78 56 CD`  (b) `34 78 12 56 AB CD` |
| 5 | reject-file, F6 |
| 6 | reject-file, F33 |
| 7 | not permitted; two commits or a rewrite |
| 8 | (a) 8589934592  (b) no  (c) L44 |
| 9 | 27 |
| 10 | (1) ignore-record  (2) cannot establish |
| 11 | (a) no  (b) no  (c) L49 |
| 12 | 0 |
| 13 | reject-file, F10 |
| 14 | no, c |
| 15 | undetectable, §21.7 |

No question in this slate struck me as textually underdetermined: each resolved to a
single reading from the sections and rows cited. I record that as an observation, not a
target — per the brief, an honest "the text permits two readings" would have been
preferred over a manufactured single answer had one of these actually been ambiguous.
