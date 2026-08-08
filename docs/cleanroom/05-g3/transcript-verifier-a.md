## A. Certification procedure (dependency order)

Rows run top to bottom; a failing row's outcome is recorded and the walk continues only where the failed scope permits. Verifier = every reader check plus the verifier-only rows (§2.3 `[R-CNF-11]`, Appendix H).

| # | Check | Reads | Outcome | Scope | Requirement |
|---|---|---|---|---|---|
|1|Transport-authoritative size; ≥128 bytes|size probe|reject-file|file|`[R-CNT-10]`,`[R-CNT-27]` (F7)|
|2|Front block = 16 constant bytes (equality; never byte-swapped)|[0,16)|reject-file|file|`[R-CNT-04]`,`[R-ENC-02]` (F2)|
|3|Trailer magic at F−64|[F−64,F−56)|reject-file|file|`[R-CNT-06]` (F12)|
|4|Trailer CRC-32C over [0,60)|trailer|reject-file|file|`[R-CNT-06]`,`[R-ENC-09]` (F18)|
|5|version_major = 1 (0 invalid; unimplemented major reported distinctly)|trailer|reject-file|file|`[R-CNT-07]` (F22,F23)|
|6|flags: incompat lane 0–15 clear; ignore lane 16–31 ignored|trailer|reject-file|file|`[R-CNT-08]` (F24)|
|7|committed_file_length = size, mod 64 = 0|trailer|reject-file|file|`[R-CNT-06]` (F17,F21)|
|8|dir_offset ≥ 16; dir_length ≥ 4; dir_offset+dir_length ≤ F−64, no wrap, both ≤ 2⁶³−1|trailer|reject-file|file|`[R-CNT-06]`,`[R-ENC-03/04]` (F3,F4,F13,F14,F20)|
|9|generation ≥ 1; file_id ≠ 0; [56,60) zero|trailer|reject-file|file|`[R-CNT-06]` (F15,F16,F19)|
|10|Directory CRC over dir_length−4 bytes|dir region|reject-file|file|`[R-CNT-11]` (F25)|
|11|Record framing: complete records, no residue, type ≠ 0, header+inline inside sequence|dir region|reject-file|file|`[R-CNT-12]` (F27,F30)|
|12|**V** reserved flag bits 2–15 zero; not MU=1∧PE=0; registered types carry §7.3's fixed flags (SHOULD-report mismatch)|record headers|reject-file / report|file|`[R-CNT-12]`,`[R-CNT-22]` (F28,F29)|
|13|Type space: reserved-range type → error (**V**); unknown MU=1 → reject-file; unknown MU=0 → ignore-record|type,flags|reject-file / ignore-record|file|`[R-CNT-15]` (F36,R10)|
|14|Multiplicity: ≤1 top-level user-metadata record|types|reject-file|file|`[R-CNT-14]`|
|15|Non-layer top-level extent slots: (0,0) or both halves nonzero; offset ≥ 16; end ≤ F−64; no wrap|slots|reject-file|file|`[R-CNT-13]` (F31–F33)|
|16|Layer names: UTF-8, non-empty, ≤255, no U+0000–001F, byte-unique across file|layer records|reject-file (dup) / reject-layer|file/layer|`[R-ENC-11/12/15]` (F6,L4,L6,L7)|
|17|Layer extent slot validity (same tests as 15)|slot|reject-layer|layer|`[R-CNT-13]` (L14–L16)|
|18|Inline payload parses exactly: fixed fields, d dims, C channels, trailing fields, sub-record residue zero, field widths as fixed|inline|reject-layer|layer|`[R-CNT-18]`,`[R-ENC-06]` (L3,L13,L22)|
|19|Enum value sets: layout∈{1,2}; linearization=1; codec∈1..4; filter∈{1,2}; index_encoding=1; channel type∈1..13|inline|reject-layer|layer|`[R-SER-06]`,`[R-GEO-05]`,`[R-COD-03/09]`,`[R-TYP-03]`,`[R-CNT-23]` (L30,L32,L33,L35,L44,L46)|
|20|Geometry floor d≥1, C≥1, Tᵢ≥1; every E,T ≤ 2⁶³−1|inline|reject-layer|layer|`[R-GEO-01]`,`[R-ENC-03]` (L1,L31)|
|21|Derived arithmetic ≤ 2⁶³−1: Gᵢ=⌈Eᵢ/Tᵢ⌉, N, P, N·P, C·N, V, decoded size, index length|inline|reject-layer|layer|`[R-ENC-04]`,`[R-GEO-03]` (L2)|
|22|A≠0 ∧ S≠0 forbidden; A power of two 512..2⁶²; A_slab power of two 1..2⁶², =0 iff S=0|inline|reject-layer|layer|`[R-CNT-16]`,`[R-SLB-01]`,`[R-CNT-23]` (L19,L27,L28,L38)|
|23|fill length = element size; bool fill ∈ {0x00,0x01}|channel entries|reject-layer|layer|`[R-CNT-23]`,`[R-TYP-07]` (L29,L34)|
|24|dim/channel names: UTF-8, non-empty, no C0, unique in layer|inline|reject-layer|layer|`[R-ENC-11/12/15]` (L5,L8–L10)|
|25|codec 4 ⇒ decoded tile size ≤ 0x7E000000|declarations|reject-layer|layer|`[R-COD-07]` (L45)|
|26|entry_count = addressed-tile count (N or C·N); extent_length = entry_count×20+⌈entry_count/2¹⁶⌉×4; slot (0,0) iff entry_count=0; crc_of_crc_array=0 iff entry_count=0|inline+slot|reject-layer|layer|`[R-CNT-17]`,`[R-CNT-23]` (L20,L21,L26)|
|27|Sub-record walk: framing, no nesting, no type 0x0001, ≤1 user-metadata, unknown MU=1 → reject-layer / MU=0 → ignore|inline tail|reject-layer / ignore-record|layer|`[R-CNT-18]`,`[R-CNT-14]` (L12,L18,L23–L25)|
|28|crc_of_crc_array over stored segment-CRC array|index tail|reject-layer|layer|`[R-IDX-04]` (L36)|
|29|Each segment CRC over its entry bytes (computed, never constant-matched)|index region|reject-layer|layer|`[R-IDX-04]`,`[R-IDX-05]` (L37)|
|30|Per entry: §15.3 classification table (sentinel / half-sentinel / len 0 / off<16 / >2⁶³−1 / sum overflow / end > F−64)|entry|reject-tile|tile|`[R-IDX-03]` (T6–T12)|
|31|Codec 1 ⇒ entry length = decoded size|entry+decls|reject-tile|tile|`[R-COD-04]` (T14)|
|32|Stored bytes CRC = entry.crc, before decode|payload|reject-tile|tile|`[R-CNT-20]` (T1)|
|33|Decode: exactly one stream/frame/block, consumed exactly, decoded length = decoded size, codec header rules|payload|reject-tile|tile|`[R-COD-05/06/07/08]` (T13,T15–T25)|
|34|**V** Filter inverse at mandated stride; padding positions and pad bits carry fill; interleaved bool bytes ∈ {0x00,0x01}|decoded image|reject-tile|tile|`[R-SER-05/08]`,`[R-COD-10]` (T2,T4,T5,T26)|
|35|**V** A declared ⇒ every stored offset mod A = 0|entries+decl|reject-layer|layer|`[R-SLB-01]` (L39)|
|36|**V** S declared ⇒ per run: stored tiles packed in ordinal order, first stored offset mod A_slab = 0; sentinels transparent; stale declaration|entries+decl|reject-layer|layer|`[R-SLB-03/04]` (L41–L43)|
|37|**V** Overlap: intra-layer → reject-layer; across layers or scopes → reject-file|all live extents|reject-layer/file|layer/file|`[R-CNT-13]` (L17,F34,F35)|
|38|**V** Live-state partition: every claimed byte in exactly one class, each extent inside [16,F−64)|whole map|reject-file|file|`[R-CNT-02]`,`[R-LIF-08]` (F8–F11)|
|39|**V** No structure between directory end and trailer|map|reject-file|file|`[R-CNT-05]` (F10,F11)|
|40|User-metadata extents: extent CRC, encoding value, decode, JSON object/finite/no-dup-keys/UTF-8/key rules; sorted members (**V** MUST report)|extents|ignore-record|record|`[R-CNT-25]`,`[R-MTA-04/05]` (R1–R9)|
|41|Certify only if no violation at any scope **and** every codec, filter and metadata document was actually executed|all|certify / decline|file|`[R-CNF-12]`,`[R-COD-11]`,`[R-MTA-09]`|

**V** = verifier-only row (no reader obligation, §19.2).

### Figures reported to the operator, and how computed

| Figure | Computation |
|---|---|
|F, generation, file_id, version, flags|trailer fields, after row 4|
|layers, and per layer d, C, N=∏⌈Eᵢ/Tᵢ⌉, entry_count, stored/sentinel split|declarations + entry scan|
|index region bytes|entry_count×20 + ⌈entry_count/2¹⁶⌉×4|
|decoded tile size|P·Q interleaved; P·Bᶜ planar numeric; ⌈P/8⌉ planar bool (§14.2–14.3)|
|payload bytes|Σ length over non-sentinel entries|
|**claimed bytes**|16 + Σ stored-tile lengths + Σ record extents (tile-index regions included) + dir_length + 64|
|**slack total (MUST report, `[R-CNT-21]`,`[R-LIF-08]`)**|F − claimed bytes|
|ignored records + reason|rows 13, 27, 40 (SHOULD report, `[R-CNT-20]`,§21.5)|
|SHOULD/MUST-report defects that do not block certification|stored-flag mismatch `[R-CNT-22]`; unsorted metadata members `[R-MTA-05]`|
|verdict per scope|rows above; certification only under `[R-CNF-12]`|

## B. Worked trace

Constructed file. Layer `a`: interleaved, rank 1, dim `x` E=16384 T=4096 (G=N=4), one uint8 channel `v`, codec 1, filter 1, S=2, A_slab=4096; decoded tile 4096 B; all four tiles stored. Layer `b`: interleaved, rank 2, dims `y` (E=4,T=2), `x` (E=4,T=2) (G=(2,2), N=4), one uint16 channel `w`, codec 1, filter 1, A=512; decoded tile 8 B; all four stored. Layer records are 97 B and 116 B; the unknown record (type 0x8001, MU=0/PE=0, inline_length 0, 32-byte extent) is 24 B.

| Commit | Appends | Layer-record deltas | F |
|---|---|---|---|
|1 (gen 1)|`a` tiles at 4096/8192/12288/16384 (runs [0,2),[2,4), each first stored tile 4096-aligned); `a` index [20480,20564); `b` tiles at 20992/21504/22016/22528 (512-aligned); `b` index [22536,22620); unknown extent [22620,22652); dir 241 B; pad 19; trailer|—|22976|
|2 (gen 2)|new `a` ordinal-1 payload [22976,27072); full `a` index [27072,27156); dir 241 B; pad 59; trailer|`a`: S 2→0, A_slab 4096→0 (`[R-CNT-23]` forces both), new slot, new crc_of_crc_array. `b` and unknown re-emitted byte-identically (`[R-WRT-05]`)|27520|
|3 (gen 3)|full `b` index [27520,27644), 6 entries + 4 B CRC array; dir 241 B; pad 19; trailer|`b`: E_y 4→5, entry_count 4→6, new slot, new crc_of_crc_array. Ordinals are stable: s = t_y·G_x + t_x and G_x is unchanged, so entries 0–3 are byte-identical and 4–5 are sentinels|27968|
|4 (gen 4)|dir 217 B (2 records); pad 39; trailer|unknown record dropped; both layer records byte-identical|28288|

Routine per-check results: rows 1–11 pass (F=28288, 64-multiple, dir_offset 27968 ≥ 16, 27968+217 = 28185 ≤ 28224); rows 18–26 pass for both layers (`a`: entry_count 4 = N, 4×20+4 = 84; `b`: entry_count 6 = 3·2, 6×20+4 = 124); row 31 passes (4096 = P·Q, 8 = P·Q). Row 22 for `a` at gen 4: A=0, S=0 — rows 35–36 are vacuous, so commit 2's clearing is what makes the superseded tile's placement lawful (`[R-SLB-04]`). Row 35 for `b`: 20992, 21504, 22016, 22528 all ≡ 0 mod 512; the two new entries are sentinels and carry no offset. Row 34 for `b`'s stored tiles: E_y=5 creates padding positions only in the t_y=2 tile row, which is unstored, so no padding obligation arises; `a` has none (16384 = 4·4096).

### Byte classification of the certified file (F = 28,288)

| Range | Size | Class |
|---|---|---|
|[0,16)|16|front signature block (claimed)|
|[16,4096)|4080|slack — gap before the first slab run|
|[4096,8192)|4096|`a` stored tile, ordinal 0|
|[8192,12288)|4096|slack — superseded `a` ordinal-1 payload|
|[12288,16384)|4096|`a` ordinal 2|
|[16384,20480)|4096|`a` ordinal 3|
|[20480,20564)|84|slack — superseded `a` index region|
|[20564,20992)|428|slack — 512-alignment gap|
|[20992,21000)|8|`b` ordinal 0|
|[21000,21504)|504|slack — alignment gap|
|[21504,21512)|8|`b` ordinal 1|
|[21512,22016)|504|slack — alignment gap|
|[22016,22024)|8|`b` ordinal 2|
|[22024,22528)|504|slack — alignment gap|
|[22528,22536)|8|`b` ordinal 3|
|[22536,22620)|84|slack — superseded `b` index region|
|[22620,22652)|32|slack — extent of the dropped MU=0/PE=0 record|
|[22652,22893)|241|slack — gen-1 directory|
|[22893,22912)|19|slack — gen-1 pre-trailer pad|
|[22912,22976)|64|slack — gen-1 trailer|
|[22976,27072)|4096|`a` ordinal 1 (live)|
|[27072,27156)|84|`a` tile-index region (live)|
|[27156,27397)|241|slack — gen-2 directory|
|[27397,27456)|59|slack — gen-2 pad|
|[27456,27520)|64|slack — gen-2 trailer|
|[27520,27644)|124|`b` tile-index region (live)|
|[27644,27885)|241|slack — gen-3 directory|
|[27885,27904)|19|slack — gen-3 pad|
|[27904,27968)|64|slack — gen-3 trailer|
|[27968,28185)|217|live directory|
|[28185,28224)|39|slack — live pre-trailer pad|
|[28224,28288)|64|live trailer|

Claimed = 16 + 16384 + 32 + 84 + 124 + 217 + 64 = **16,921**. **Slack = 28,288 − 16,921 = 11,367 B (40.2%)**. The "which generation wrote this slack" column above is *my construction knowledge*, not a certification output — §5.2's rationale states it is not decidable from the live state.

**Certified:** conforming file, no violation at file, layer, or tile scope; live state partitions (row 38); no structure between dir end and trailer (row 39); both layers' full index chains and all eight stored tiles verified and decoded (row 41 satisfied — codec 1 and filter 1 are executable). **Reported:** F=28288; generation 4; version 1.0; flags 0; 2 layers; `a` 4/4 stored, `b` 4 stored + 2 sentinel; slack total 11,367 B with the recommendation to compact; 0 ignored records at gen 4; no SHOULD-report defects.

## C. What I cannot establish, and why

1. **Anything about generations 1–3.** The walk is live-state-only (`[R-LIF-08]`, §9.7 note); slack is uninterpretable (`[R-CNT-21]`). Had the dropped record carried a *reserved*-range type instead of an experimental one, gens 1–3 would have been nonconforming (`[R-CNT-15]`) and gen 4 would still certify identically.
2. **Whether the drop in commit 4 was licensed** (§20.4) — needs the prior directory. Same for **L43** (stale slab declaration): its condition is stated over "the commit changed an affected run", which no live-state walk can evaluate; operationally it collapses into L41/L42.
3. **Writer conduct rules**: §10.3's experimental-value prohibition, §18.3's registry-version targeting. `[R-CNF-02]` puts these outside the byte predicate.
4. **Content correctness**: a mis-strided filter with no structural constraint broken, an undisclosed zstd dictionary, or simply wrong samples all certify (`[R-ERR-01]`, §21.7).
5. **Authenticity** (`[R-SEC-07]`) and **rollback** (`[R-LIF-06]`: truncation to an earlier commit is indistinguishable in-format).
6. **Slack content** — unconstrained and unchecksummed, so corruption or residual sensitive data inside it is invisible (`[R-SEC-04]`, §23.1).

## Findings

### BYTE-LEVEL AMBIGUITY

**1. §20.4's MU=0/PE=0 drop licence is self-satisfying or not, and the text does not say which.**
*Location:* §20.4 `[R-WRT-08]` table, row "MU = 0, PE = 0": droppable by "an appender only in a commit that modifies the scope the record attaches to".
*Reading A:* removing a top-level record *is* modification of file-scope structure — §20.4's MU=1 row defines that scope's modification as "adding, removing, or reordering top-level records" — so the drop satisfies its own precondition and any commit may drop.
*Reading B:* the clause requires a modification independent of the drop (otherwise it is vacuous for every record, top-level or sub-record), so a commit that changes nothing else must retain the record byte-identically.
*Discriminator:* commit 4 of the trace — an appender asked to discard unknown ancillary records, changing nothing else. Reading A emits a 2-record live directory: dir_length = 217 (trailer offset 32 reads `D9 00 …`), [22620,22652) becomes slack, reported slack total 11,367. Reading B forbids the commit; the conforming output for the same request keeps 3 records: dir_length = 241 (`F1 00 …`), directory bytes differ, extent stays live, reported slack total 11,335. Same F (28,288) either way, so the divergence is invisible at the trailer's length field.
*Searched:* §20.4 whole subsection and its rationale; §20.3 steps 4–6; §20.5's compactor clause ("whenever it rewrites the file" — contrasted, not defined); §7.2's MU/PE rules; §21.5 R10; §21.6's row "Ignored, and preserved or dropped per its PE bit" (states the licence without the qualifier); §2.4's preserve-verbatim definition. No sentence defines "a commit that modifies the scope".

### CONTRADICTION

**§9.6 assigns prior-generation enumeration to coverage verification; §9.7 forbids it.**
§9.6 `[R-LIF-06]`: "Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0."
§9.7 `[R-LIF-08]` + note: "A verifier checking `[R-CNT-02]`'s partition walks the live state only… Nothing here enumerates prior commits." §5.2 agrees with §9.7 ("this specification certifies the live state exactly, and counts the rest"). No verdict diverges — append-only placement makes cross-generation overlap impossible and slack is defined by what the *live* state fails to claim — so the §9.6 sentence is a stranded remnant, not a byte-level fork.

### OBSERVATION

1. **§9.7's walk omits two of §5.2's four coverage classes.** §9.7 enumerates the directory, records, record extents, index regions and non-sentinel entries, then says "Bytes the walk does not reach are slack" — the front signature block and the live trailer are not in that enumeration, yet §5.2 names both as claimed. A literal §9.7 implementation reports slack = 11,447 for the traced file; the correct figure under §5.2's definition is 11,367. Not byte-level: §5.2's opening sentence ("the front signature block, and every structure … together with the live directory and the live trailer") resolves it, and §9.7 declares itself an implementation of `[R-CNT-02]`. This is the closest call in the report, because the diverging quantity is one a verifier MUST report.
2. **Three verbatim-duplicate register rows.** F8≡F9 and F10≡F11 and F34≡F35 are identical in condition, instances, detector, detection point and rule. §21.2's "37 conditions" and §21.8's "120 conditions" count them separately, and `[R-ERR-02]` then obliges a distinct vector for each — a corpus obligation with no distinguishing content. Likely intent was an unclaimed/double-claimed pair for F8/F9.
3. **§21.8's instance count appears to be 213, not 214.** Counting mechanically per §21.1 (semicolon-separated cells; "—" counts as one): 69 file + 81 layer + 43 tile + 20 ignored. Off-by-one in either the document or my count of a judgment cell (T18's four skippable-frame positions, L22's four payload regions).
4. **`[R-CNT-27]` appears in no register row.** F7 states the 128-byte-minimum condition but cites `[R-CNT-01]`, which does not contain that rule; §21.1's "the rule governs" then points at a rule that does not define the condition.
5. **`[R-COD-11]` and `[R-MTA-09]` both cite "§9.7(d)".** §9.7 has no lettered clauses.
6. **Extent growth silently reclassifies padding as real samples.** Growing an extent so that a previously-padding position falls inside a stored tile turns fill-encoded padding (`[R-SER-05]`) into a real sample whose value is the fill — legal, unremarked, and worth a note near §11.1's growth rationale. The trace also shows why "first-declared dimension" is the benign growth: under `[R-GEO-06]` the multiplier of t₀ is ∏_{j>0}Gⱼ, so growing E₀ leaves every existing ordinal fixed; growing any later dimension renumbers them and forces §20.3's re-emission to permute entries.

## Verdict
BYTE-LEVEL AMBIGUITIES: 1
CONFIDENCE: medium
