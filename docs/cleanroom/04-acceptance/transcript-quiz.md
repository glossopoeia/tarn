# TARN spec review — quiz charter

Source read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (3235 lines), in full, and nothing else. Checksum constants were recomputed from §4.5's stated parameters (polynomial 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF); my implementation reproduces §4.5's own check vector, `CRC-32C("123456789") = 0xE3069283`, so it is the spec's checksum by §4.5's test.

**Layer Q, derived once and used throughout.** d = 2; dims (y: E=3, T=2), (x: E=4, T=2); interleaved; linearization 1; channels a (uint16, B=2, fill `FF FF`), f (bool, B=1, fill `00`); codec 1 (none), filter 1 (none).
G_y = ⌈3/2⌉ = 2, G_x = ⌈4/2⌉ = 2 → N = 4 (§11.2 `[R-GEO-03]`). P = 2·2 = 4. C = 2. Sample stride Q = B_a + B_f = 2 + 1 = 3, in-sample offsets F_a = 0, F_f = 2 (§14.2 `[R-SER-02]`). Decoded tile size = P·Q = 12 bytes.

---

## Q1 — Smallest conforming file

**128 bytes.** `[R-CNT-27]` (§5.1) states the floor and Appendix B pins it as a named constant.

Arithmetic: front block occupies [0, 16) (§6.1); dir_offset ≥ 16 and dir_length ≥ 4 (§6.2 table), so the directory cannot end before 20; the trailer is 64 bytes at a 64-aligned offset with only a zero pre-trailer pad of fewer than 64 bytes between the directory's end and it (`[R-CNT-05]`), so the earliest legal trailer start is 64; F = 64 + 64 = 128, and 128 mod 64 = 0 (`[R-CNT-01]`, `[R-CNT-06]`).

**[16, 20) is the entire directory region** — dir_offset = 16, dir_length = 4. Its final 4 bytes are a CRC-32C over the preceding dir_length − 4 = 0 bytes (`[R-CNT-11]`), so the whole 4 bytes *are* that CRC, and the CRC-32C of zero bytes is `0x00000000` (§4.5's check vector): the bytes `00 00 00 00`. The record sequence it covers is empty — zero records, a conforming generation with no layers (`[R-CNT-14]`, §21.6). Appendix A's annotation agrees exactly.

Confidence: **high**.

## Q2 — What coverage certifies, and what a verifier does about the rest

**Certifies: the live committed state, exactly** (§5.2 `[R-CNT-02]`) — the front signature block, every structure reachable from the live trailer through the live directory's records, extent slots, and tile-index entries, together with the live directory, its declared padding, and the live trailer. Every byte of that state belongs to exactly one of {front signature block; structure (stored-tile extent, record extent, directory, trailer); declared padding}, with no two overlapping; a file whose live state does not partition this way is not conforming. Declared padding is defined constructively, not inferred: only an alignment/slab gap shorter than its modulus, or the sub-64-byte pre-trailer pad — and it MUST be zero bytes (`[R-CNT-03]`, verifier-detected, file scope).

**The rest is dead space** (`[R-CNT-21]`): no internal structure this specification defines, unconstrained content, **no conformance requirement applies to it**, and a reader MUST NOT interpret it. The verifier's obligation is arithmetic, not structural: §9.7 `[R-LIF-08]` walks the live state only, checks disjointness, containment in [16, F − 64), and each covering checksum (§8.1); "Bytes the walk does not reach are dead space: the verifier sums them and reports the total, and their content is not its concern." `[R-CNT-21]` makes that report mandatory — "since that number is what tells an operator to compact." Only compaction (§20.5) reclaims it. Nothing enumerates prior generations (§9.7's note); §23.1 `[R-PRV-01]` adds that dead space is not erasure.

Confidence: **high**.

## Q3 — Q's addressed-tile count and index-region size

**Addressed tiles = 4.** Interleaved, so the addressed-tile count is N, not C·N (§11.2 `[R-GEO-03]`); C = 2 is irrelevant here. entry_count MUST equal it (§7.4, `[R-CNT-17]`).

**Index region = 84 bytes.** `[R-CNT-17]`: entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 = 4 × 20 + 1 × 4 = 80 + 4 = 84. Layout, contiguous with no padding anywhere inside (§15.1 `[R-IDX-01]`): entry array [0, 80), 20 bytes per entry at region byte 20·k in disk-ordinal order; segment CRC array [80, 84), one u32. The single segment is *partial* (4 < 2¹⁶), so its CRC MUST be computed — the all-sentinel constant `0xEECB3BB2` is licensed only for full segments (`[R-IDX-05]`).

Confidence: **high**.

## Q4 — A file that is 90% superseded bytes

**Conforming.** Dead space carries no conformance requirement (`[R-CNT-21]`), and §21.6 lists "Superseded bytes of earlier commits sit in the file" among conditions that are *not* violations. `[R-CNT-02]`'s partition binds the live state only, and the live state of such a file partitions normally.

Obligations that do attach:

- **Verifier:** MUST report the total dead-byte count (`[R-CNT-21]`, `[R-LIF-08]`). Its content is not checked and not certified.
- **Reader:** MUST NOT interpret it; the default read path is trailer-at-end-or-fail with no backward scan (`[R-LIF-05]`). A trailer mimic inside it is inert (§21.6, `[R-SEC-04]`).
- **File-level:** the bytes still lie inside [0, F); F equals the transport-authoritative size and is a multiple of 64 (`[R-CNT-06]`, `[R-LIF-04]`).
- **Compactor:** carries none of it forward (`[R-WRT-06]`, `[R-WRT-07]`); compaction is the only reclamation.
- **Privacy:** writers MUST NOT represent a superseding commit as erasure (`[R-PRV-01]`); erasure belongs to the storage layer (`[R-PRV-02]`); writers SHOULD compact before publication when the history is sensitive (`[R-PRV-03]`).
- **Advisory:** batch small updates and compact when dead space grows (§20.3's note); a pipeline taking untrusted files SHOULD verify rather than merely read, since dead space can carry smuggled bytes (`[R-SEC-03]`).

Confidence: **high**.

## Q5 — Growing y's extent 3 → 5

- **Addressed tiles: 6.** G_y = ⌈5/2⌉ = 3, G_x = 2 (unchanged), N = 3·2 = 6; interleaved → 6 entries, entry_count = 6 (`[R-GEO-03]`, `[R-CNT-17]`).
- **Existing ordinals do not change.** Under linearization 1, s = Σᵢ tᵢ·∏_{j>i} Gⱼ = t_y·G_x + t_x (`[R-GEO-06]`). Only G_x enters, and G_x is unchanged, so (0,0)→0, (0,1)→1, (1,0)→2, (1,1)→3 all persist; the new tiles (2,0), (2,1) take 4 and 5. This is the lucky axis: growth along the *last-declared* dimension would change G_x and renumber every ordinal, which is what `[R-WRT-04]` step 4 means by "a geometry change renumbers ordinals."
- **Payload bytes appended by the growth itself: 0.** Extent growth is a metadata-only operation (§11.1's rationale; §13's sparse-writing note). The two new addressed tiles are not stored: their entries are sentinels, `FF ×16 00 ×4`, occupying no payload bytes and reading as fill (`[R-IDX-02]`, `[R-TYP-08]`). Nor does the pre-existing edge tile at ordinal 3 need rewriting: its y = 3 positions were fill-encoded padding (`[R-SER-05]`) and simply become real positions whose value is that same fill — the stored bytes and the entry's crc are unchanged.

What the commit must nonetheless append (`[R-LIF-02]`, `[R-WRT-04]`): the layer's **full new index region, 6 × 20 + 4 = 124 bytes** (entries 0–3 byte-identical at their positions, 4–5 sentinels, segment CRC recomputed), the new complete directory and its CRC (the layer record changes: E_y, entry_count, extent_offset, extent_length 84→124, crc_of_crc_array), the zero pad, and the 64-byte trailer. The old 84-byte index region, old directory, old pad and old trailer become dead.

Confidence: **high**.

## Q6 — Decoded image of Q's tile at tile coordinates (1, 1)

```
02 01 01  02 01 01  FF FF 00  FF FF 00
```

**12 bytes.** Justification, byte group by byte group:

- **Size.** Interleaved decoded size = P·Q = 4·3 = 12 (`[R-SER-02]`); it is a function of declarations alone (`[R-SER-07]`). Codec 1 stores the filtered image verbatim and filter 1 is the identity (`[R-COD-09]`, §17.3), so the *stored* bytes are these same 12 bytes and the entry's length MUST equal 12 (`[R-COD-04]`).
- **Which positions.** Tile coordinates are in declared order (§11.4), so t_y = 1, t_x = 1 covers y ∈ [2, 4), x ∈ [2, 4). E_y = 3 → y = 2 real, y = 3 is a **padding position** (§11.3 `[R-GEO-04]`). E_x = 4 → x = 2 and x = 3 both real. So two real positions and two padding positions.
- **Order.** In-tile ordinal = Σᵢ uᵢ·∏_{j>i} Tⱼ = u_y·2 + u_x, row-major for every linearization, permanently (§11.4 `[R-GEO-06]`). Ordinal 0 = (y2,x2) real; 1 = (y2,x3) real; 2 = (y3,x2) padding; 3 = (y3,x3) padding. Interleaved is sample-major: the sample at ordinal u occupies [u·3, u·3+3), a at u·3 (2 bytes), f at u·3+2 (1 byte) (`[R-SER-01]`, `[R-SER-02]`).
- **Bytes 0–2 and 3–5.** a = 0x0102 as uint16 little-endian → `02 01` (`[R-ENC-01]`, §12.1); f = true as an interleaved bool value is the single byte `01`, and 0x00/0x01 are the only legal bytes (`[R-SER-08]`, §14.2).
- **Bytes 6–8 and 9–11.** Padding positions are serialized like any other position and their content is fixed: each channel's recorded fill — `FF FF` for a, the recorded fill byte `00` for the interleaved bool f (`[R-SER-05]`). A reader never returns them (`[R-GEO-04]`); a verifier MUST check them, tile scope.

(No pad bits here: pad bits arise only in packed *planar* bool planes, §14.3's note.)

Confidence: **high**.

## Q7 — That sentinel tile becomes stored

Disk ordinal of (1,1) is s = 1·2 + 1 = **3**. The tile must become stored; a writer emits, in this order (`[R-LIF-02]`, `[R-WRT-04]`):

0. **Establish F** by validating the trailer at the physical end (`[R-LIF-04]`); on failure, no append — recovery is a separate operation (§9.6). Perform §19.1's open and §19.3's layer validation, and verify the index chain for the segment it reuses (`[R-WRT-03]`, `[R-IDX-04]`). Nothing in [0, F) may be modified (`[R-LIF-01]`).
1. **At exactly F, the tile payload: 12 bytes.** Both pipeline stages consume and produce *whole tiles* (`[R-COD-01]`, `[R-COD-02]`) — you cannot emit only the changed sample. Under filter 1 / codec 1 the stored bytes are the decoded image itself: the changed sample's values, the tile's other real position(s) carrying whatever the writer intends (the fill bytes, if unchanged), and both padding positions carrying `FF FF 00` (`[R-SER-05]`).
2. **Immediately after, with no gap** — Q declares neither alignment nor slab, so §5.2 admits no declared padding here and any gap would be unsuperseded dead space, a writer defect (`[R-SLB-05]`) — **the layer's complete new tile-index region, 84 bytes**: entries 0, 1, 2 byte-identical at their disk-ordinal positions; entry 3 = {offset = the payload's offset, length = 12, crc = CRC-32C of those 12 stored bytes} (§15.1, §8.1, `[R-WRT-04]` step 4); then the 4-byte segment CRC array = CRC-32C over the 80 entry bytes, **computed** (partial segment, `[R-IDX-05]`). Partial re-emission is not permitted: any change to a layer's index content re-emits the whole region.
3. **The new complete directory, then its CRC** (`[R-LIF-02]` step 3, `[R-WRT-05]`): the layer record re-emitted with a new extent_offset (the new region), extent_length still 84, entry_count still 4, and a **new crc_of_crc_array** = CRC-32C over the new 4-byte segment CRC array; every other record byte-identical, header, inline payload and extent slot alike. For Q with a one-byte name and no sub-records the layer record is 24 + 98 = 122 bytes (inline: 2 + 1 + 2 + 2 + 2 + 8 + 8 + 8 + 1 + 2 = 36 fixed, + 18 + 18 dims, + 7 + 6 channels, + 1 + 8 + 4 trailing = 98), so a single-layer directory is 126 bytes.
4. **A durability barrier** (fdatasync or equivalent) — `[R-LIF-02]` step 4.
5. **The zero pad** to the next 64-byte boundary (fewer than 64 bytes, none if already aligned, `[R-CNT-05]`, `[R-CNT-03]`) **and the 64-byte trailer**: generation one greater, same file_id, committed_file_length = the new end (multiple of 64), unknown ignore-lane flag bits copied forward and incompat bits absent (`[R-CNT-08]`), reserved zero, version_minor per `[R-CNT-26]`, trailer CRC over trailer bytes [0, 60).
6. **A second barrier** (`[R-LIF-02]` step 6), with the physical file length equal to committed_file_length (`[R-LIF-04]`).

Dead space produced: the old 84-byte index region, the old directory, old pad, old trailer — and **no superseded payload**, since the tile was previously unstored. (Had Q declared a slab or alignment, `[R-SLB-04]`/`[R-SLB-01]` would additionally require re-establishing the invariant or clearing the declaration.)

Confidence: **high**.

## Q8 — A tile payload that looks exactly like a valid trailer

**Nothing happens; it is inert, and the file stays conforming.** §21.6 records this verbatim as a defined non-violation: "A payload contains a byte string that mimics a trailer → Inert: nothing enumerates dead space, and a recovery tool re-verifies its output whole (§9.6)", governing rule `[R-LIF-06]`.

Mechanically: a reader's open is anchored at [F − 64, F) and it MUST NOT scan backward (`[R-LIF-05]`, `[R-RDR-01]`); the payload is live state reached only through its index entry, whose crc covers it (§8.1). §9.6 makes two cautions normative for *tools*: a tile payload can deliberately contain such a string, so recovery output MUST be re-verified as a whole file (§8) before being trusted. §6.2's note covers the sharpest case — a mimic that happens to sit at exact physical end of file can pass every trailer gate, and is then caught at the directory CRC (`[R-CNT-11]`), "detection is never silent." `[R-SEC-04]` states the residue rather than defending it.

Confidence: **high**.

## Q9 — A = 512 with a 4096-byte zero gap

**The file is conforming. The gap is dead space, not declared padding.**

Arithmetic: §5.2 admits a pre-structure run as declared padding *only* when its length is **less than that declaration's modulus** — A for per-tile alignment — "so that the run is exactly the distance to the next legal offset." 4096 ≥ 512, so the run fails the test by construction (the distance to the next 512-multiple is always ≤ 511). It therefore falls to §5.2's residual clause and `[R-CNT-21]`: dead space, unconstrained, **no conformance requirement applies to it**. `[R-LIF-08]` gives the operational consequence: the verifier's live-state walk does not reach those 4096 bytes, so it sums them into the dead-byte total it MUST report.

No register row fires. F8 binds "a byte of the **live committed state** claimed by no coverage class" — a gap is not live state. F9 binds *nonzero* declared padding; these bytes are zero and are not declared padding anyway. F35 is overlap, not gaps.

The one shadow: `[R-SLB-05]` says "a commit that produces dead space it did not supersede is a writer defect." It assigns no outcome class and has no register row — principled, because a verifier generally cannot distinguish a fresh gap from superseded bytes (§9.7's note: "Nothing here enumerates prior commits"), and §2.4 `[R-CNF-07]` scopes outcome assignment to *detectable* violations. See Observation 2 for the generation-1 corner where it *is* decidable.

Confidence: **high** on the verdict; **medium** on whether the author intends generation-1 files to be certifiable in this state.

## Q10 — committed_file_length = 128, file on disk = 192

**reject-file**, reported as torn or invalid. Which trailer is even consulted is fixed by §19.1 steps 1–2: the reader obtains the *transport-authoritative* size (192) and fetches [size − 64, size) = [128, 192). Two placements, one verdict:

- If the trailer carrying committed_file_length = 128 is the one at [128, 192): it fails the gate "committed_file_length equals the file size" (`[R-CNT-06]`) — register **F22**, and equally **F38** ("Bytes were appended past a completed commit and never truncated"), reader-detected at open.
- If the 128-claiming trailer is the older one at [64, 128): the reader reads [128, 192), finds no trailer magic / no valid CRC there, and rejects (**F13**/**F19**, `[R-CNT-06]`).

Prohibitions that bite here: the reader MUST NOT scan backward for an earlier trailer (`[R-LIF-05]`), and MUST NOT substitute committed_file_length for the transport size (`[R-CNT-10]`). It MAY retry once before concluding "torn" on shared filesystems with attribute-cache staleness (§9.5's note). Truncating back to 128 is §9.6's deliberate recovery operation — a recovery tool's job, never a reader's — and its output MUST be re-verified as a whole file (`[R-LIF-06]`). A writer opening this file for append MUST NOT append (`[R-LIF-04]`).

Confidence: **high**.

## Q11 — A compacted file's identity; when a compactor must refuse

**Identity** (`[R-WRT-06]`): a **fresh file_id** — "a new draw under §9.3's randomness advice, not merely a value compared against the input's" — and **generation 1**, since a compacted file is a whole-file rewrite under a new file_id by definition (`[R-LIF-01]`). Reusing the input's file_id would break the (file_id, range) cache contract of `[R-LIF-03]`, because relocation puts different bytes at the same ranges. The output trailer copies the input's unknown ignore-lane flag bits forward (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the input's version_minor — a compactor cannot know which minor defined a bit it does not implement, so it never lowers the floor beneath one.

**Content identity** (`[R-WRT-07]`): the output's reference arrays MUST equal the live generation's bit for bit (`[R-MDL-02]`) — every stored tile's bytes verbatim, each index entry's crc and every sentinel unchanged; only entry *offsets* change, with segment CRCs recomputed over the entries as re-emitted and each layer record's crc_of_crc_array updated; retained records re-emitted per §20.4, with relocation re-pointing extent slots. Only the live committed state is carried, less any record §20.4 permits dropping; dead space is never carried. Note `[R-PRV-04]`: the new file_id is not an unlinkability measure — the preserved bytes make the output trivially correlatable with its input.

**MUST refuse:** when the input carries **any record whose type it does not implement with MU = 1** (`[R-WRT-06]`) — such a type can define references this specification does not (§7.2), so its bytes cannot be safely relocated. Two adjacent constraints: it is a reader of everything it copies and MUST verify each link of the chain — open, each retained layer's record and full index chain, each relocated extent's checksum including every stored tile's entry crc — *before* emitting that structure's bytes (`[R-WRT-09]`, `[R-CNF-11]`), so any failed link stops it; and an MU = 0, PE = 0 record it drops SHOULD be reported (`[R-WRT-08]`). It need not decode tiles — Part I/II independence, §3.3.

Confidence: **high**.

## Q12 — Exactly which bytes are dead after superseding one stored tile of Q

Five runs, per §5.2's enumeration ("superseded payloads and index regions, and every prior generation's directory, padding, and trailer", `[R-CNT-21]`) and `[R-WRT-04]` step 4:

| # | Bytes | Size |
|---|---|---|
| 1 | the superseded tile's old payload extent [old_offset, old_offset + old_length) | old_length |
| 2 | the layer's **entire** previous tile-index region | **84** (4 × 20 + 4) |
| 3 | the previous generation's directory region, its terminal CRC included | prior dir_length |
| 4 | the previous generation's pre-trailer pad | 0–63 |
| 5 | the previous generation's trailer | 64 |

Total = old_length + 84 + prior_dir_length + prior_pad + 64.

**Not dead:** the front signature block (§5.2 — live in every generation), and the other three tiles' payloads. Their entries are re-emitted byte-identically at their disk-ordinal positions and still reach the same bytes, so those payloads stay live even though the *index region* holding those entries died. The whole 84 bytes go dead for one changed entry — this is §20.3's note ("A commit's cost is dominated by its index, not its data") at Q's scale.

Confidence: **high**.

## Q13 — Rank 32; rank 40

**Rank 32: yes, MUST accept.** §21.9's minimum-guarantee table gives rank d = 32; `[R-CNF-10]` and `[R-ERR-03]` make acceptance of any conforming file within the table mandatory, and `[R-ERR-04]` is blunt: "Software that declines a file whose every quantity lies within the table is not a conforming reader (`[R-CNF-03]`) — the guarantees are the floor, not a suggestion."

**Rank 40: no obligation.** The table states minimums, not caps: "A file exceeding any of these remains conforming, and a reader MAY decline it" (`[R-ERR-04]`). Rank 40 is well inside the *hard* limit of 255 imposed by §7.4's u8 rank field (`[R-ERR-05]`), so the file is conforming. Refusal may be at the whole file **or at the narrowest scope whose declarations exceed what it can serve — a layer or a tile.**

**If it declines:** the refusal MUST be reported **as a resource limit, not as a validity error** (`[R-ERR-04]`) — "the two send a user to opposite remedies, and a reader that reports 'too large' as 'corrupt' invites the deletion of intact data." (Structurally parallel to `[R-CNT-07]`'s demand that an unimplemented major be diagnosed distinctly from both "not a TARN file" and "corrupt", and to §21.6's closing paragraph.)

Confidence: **high**.

## Q14 — `1e400` in a user-metadata document

**Outcome: ignore-record.** §18.2's "Finite numbers only" restriction names this case explicitly: a document is unreadable if it contains "a number whose binary64 interpretation is not finite — which covers a magnitude that overflows on conversion, `1e400` being the ordinary case" (`[R-MTA-04]`). Register row **R7**, reader-detected, detection point **extent use** (`[R-RDR-02]`, §19.2's fourth tier — the open fetches no extent).

**Scope, two senses:**

1. *What is lost:* the **whole document**, not that number or its member. Contrast `[R-MTA-07]`, where a standardized key outside its listed scope or of the wrong shape is ignored *individually* rather than condemning the document. Here the containing record is skipped as though absent (§2.4's table), and decoding of all stored data is unaffected. The reader SHOULD report the loss (§21.5, `[R-CNT-25]`).
2. *Which scope rejects:* **none**. The user-metadata document is **quarantined** (`[R-CNT-25]`, `[R-MTA-02]`): every way its document can be unreadable is ignore-record "whatever the containing scope … notwithstanding the owning-scope mapping of `[R-CNF-08]`". So a top-level (file-scope) record and a layer sub-record behave identically — the file is not rejected, the layer is not rejected, and no sample read changes. (Had the *extent slot* been malformed instead, that failure precedes the document and would take the containing scope: reject-file or reject-layer, `[R-MTA-02]`.)

**File conformance:** the file is nonconforming — §21.5's rows are violations (§21.1: the register "enumerates every violation this specification names"), and §2.4 makes conformance conjunctive over every scope. Readers nonetheless proceed, ignoring only that record.

Confidence: **high** on the reader outcome and its scope; **medium** on the nonconforming label, since §18.2 frames the restrictions as readability conditions and only its *inexact-number* advice is phrased as a writer SHOULD NOT.

## Q15 — Appendix A's trailer CRC and its coverage

**Value: `0xE00938D2`**, stored little-endian as the bytes `D2 38 09 E0` at file offset **[124, 128)** = trailer bytes [60, 64) (§6.2's layout table; Appendix A's annotation).

**Covered bytes: trailer bytes [0, 60) = file bytes [64, 124)** — magic (8), version_major (2), version_minor (2), flags (4), generation (8), dir_offset (8), dir_length (8), committed_file_length (8), file_id (8), reserved (4) = 60 bytes. The CRC field itself is excluded. `[R-CNT-24]` states the same permanently and positionally: "a CRC-32C at F − 4 covering bytes [F − 64, F − 4)" — with F = 128, that is [64, 124). Per §4.5 and §8.1 it is a terminal checksum: verified by comparison, covered by no further checksum.

**Independently recomputed** over those exact 60 bytes with §4.5's parameters: `0xE00938D2` → `D2 38 09 E0`. Matches Appendix A byte for byte.

Confidence: **high** (recomputed, not read off).

---

# Findings

## BYTE-LEVEL AMBIGUITY

**None.** Every candidate I developed collapsed under a located sentence. The four I pushed hardest, with what refuted each:

- *Gap-vs-declared-padding classification (Q9).* Refuted by §5.2's explicit "less than that declaration's modulus" test plus `[R-LIF-08]`'s constructive walk. Searched: §5.2, §16.1–§16.2, §9.7, §21.2 rows F8/F9/F11/F12.
- *Whether a fresh unsuperseded gap makes a file nonconforming.* Refuted by `[R-CNT-21]` ("no conformance requirement applies to it") plus §2.4's *detectable* qualifier in `[R-CNF-07]`. See Observation 2 for the residue.
- *User-metadata `extent_length` of 4 — reject-file or ignore-record?* Refuted by §7.1's explicit clause and §18.1's "that failure precedes the document." Searched: §7.1, §18.1, §18.2, §21.2, §21.5.
- *Whether writing a previously-sentinel tile permits a partial payload or a partial index re-emission.* Refuted by `[R-COD-01]`/`[R-COD-02]` ("Both stages consume and produce whole tiles") and `[R-WRT-04]` step 4 ("re-emitted in full — entry_count entries plus the segment CRC array").

## CONTRADICTION

**None.** The one place two sentences classify the same byte differently is §5.2's dead-space appositive against §16's `[R-SLB-05]` — reported as Observation 2 rather than as a contradiction, because §5.2's main clause ("Every other byte of the file is dead space") is already total and `[R-LIF-08]` states the classification constructively, so no obligation resolves differently under either reading.

## OBSERVATION

**O1 — Two reader-detected, scope-level rejections have no row in the error register.** §21.1 makes register completeness normative ("a violation this specification names and the register omits is a defect in this document"), and `[R-ERR-02]`/`[R-VEC-03]` hang the conformance corpus off the row/instance inventory. Missing:
- `[R-MTA-03]` (§18.2): "A record whose inline_length is not 1 is a validity error at the record's containing scope" → reject-file top-level, reject-layer as a sub-record. No F- or L-row states it.
- `[R-CNT-25]` (§7.1): a user-metadata record "whose extent_length is less than 5 … is a validity error at its containing scope." F27 covers only the (0, 0) slot; L11 only the sub-record (0, 0).

Both resolve correctly from their defining sections, so neither is byte-level — but §21.8's inventory is short by (at least) two rows and four instances. I verified the stated inventory is otherwise exact: §21.2 = 38 rows / 69 instances, §21.3 = 47 / 81, §21.4 = 26 / 43, §21.5 = 10 / 20 → **121 rows, 213 instances**, matching §21.8 exactly. That precision is what makes the two omissions worth fixing rather than shrugging at. *Searched: §7.1, §18.1, §18.2, and every register row mentioning `inline_length` or user metadata.*

**O2 — `[R-SLB-05]`'s "writer defect" is the one named defect with no outcome class, no register row, and — at generation 1 — a decidable detector.** §2.4 `[R-CNF-07]` assigns exactly one reader outcome to every *detectable* violation, which normally excuses this one: a verifier cannot distinguish a fresh gap from superseded bytes, since nothing enumerates prior commits (§9.7's note). **But at generation 1 there are no prior commits**, so any byte outside the live state was necessarily produced by the commit that wrote the file, and the condition becomes fully decidable from the live trailer alone. A verifier certifying a generation-1 file with a 4096-byte unclaimed run therefore has to choose between `[R-CNT-21]` ("no conformance requirement applies to it" → certify, count 4096 dead bytes) and `[R-SLB-05]`'s defect language, which cites `[R-CNT-02]` and `[R-LIF-02]` as if it were a coverage violation. I resolve it toward certification — `[R-CNT-21]` is explicit, `[R-SLB-05]` uses no MUST-NOT and carries none of the paired reader-side clause §2.1's phrasing note promises for writer prohibitions, and `[R-LIF-08]` defines the dead total constructively so the reported number is the same either way. The adjacent imprecision: §5.2 defines dead space by provenance ("bytes an earlier commit wrote that the live state no longer reaches") while `[R-SLB-05]` and `[R-LIF-08]` define it structurally ("a byte the live state neither claims nor accounts for as declared padding"); those diverge exactly on the generation-1 case. Worth one sentence in §5.2 aligning the two, and a decision on whether gen-1 unsuperseded dead space is certifiable.

**O3 — Register row F7 cites the wrong rule for the 128-byte floor.** F7 restates `[R-CNT-27]`'s minimum but names `[R-CNT-01]` as governing. `[R-CNT-27]` occurs exactly once in the whole document — its own definition at §5.1 — so the register never cites it, and §21.1's tiebreak ("where a row and the rule it cites diverge, the rule governs") points at a rule that does not state the floor. Cosmetic; same detector, same point, same outcome.

**O4 — §21.3 skips row number L40 silently.** Rows run L1–L39, then L41–L48: 47 rows, matching the stated "47 conditions," so the count is right. But the document elsewhere makes retirement explicit (§14.4's note on the withdrawn `[R-SER-04]`), so an unexplained numbering gap in a table whose completeness is normative invites the reader to hunt for a missing condition. One note would close it.

**O5 — Codec 3 is unusable on small tiles without single-segment mode, and the spec never says so.** `[R-COD-06]` requires that a writer "MUST NOT declare a window size exceeding the tile's decoded size," reader-enforced at tile scope (row T21). RFC 8878's `Window_Descriptor` cannot express a `Window_Size` below 1 KiB (exponent 0 → 1024 bytes), so for any tile whose decoded size is under 1024 bytes — layer Q's 12-byte tiles, for instance — the only conforming encoding is a frame with `Single_Segment_Flag` set, where `Window_Size` = `Frame_Content_Size`. A writer using stock zstd settings on small tiles therefore emits payloads every conforming reader must reject. Not an ambiguity — the verdict on given bytes is determinate — but the one place where following the spec's own §11.3 tile guidance (1–16 MiB) is what saves an implementer, and stepping outside it silently does not. A one-line note beside `[R-COD-06]`'s window rule would earn its keep.

**O6 — Positive verification (no action needed; recorded as evidence).** Every checksum constant and every worked example I could mechanize is correct:
- `CRC-32C("123456789") = 0xE3069283` ✓ and `CRC-32C(∅) = 0x00000000` ✓ (§4.5), from the polynomial as stated.
- Appendix A's trailer CRC `0xE00938D2` / `D2 38 09 E0` over [0, 60) ✓ — recomputed from the annotated field values.
- `[R-IDX-05]`'s all-sentinel full-segment constant `0xEECB3BB2` ✓ — recomputed over all 1,310,720 bytes of 2¹⁶ sentinel entries. This one matters: a writer taking the constant on faith would otherwise produce files every reader rejects.
- §17.3's byte-shuffle example, §14.2's three offset examples, §14.3's `55 01` / `55 FD` packing example, §11.4's ordinal example (s = 10, in-tile 11,452, planar disk 74), §15.4's segment arithmetic (16 segments, region 20,000,064 bytes, segment 15 at [19,660,800, 20,000,000), 1.25 MiB per full segment), §21.9's note (2³² tiles → 256 KiB CRC array; 2³⁶ → 4 MiB), and §20.3's 644-byte index example all check out.

---

# Verdict

**IMPLEMENTABLE: yes**
**BYTE-LEVEL AMBIGUITIES: 0**
**CONFIDENCE: high**

The container and array model are pinned to the byte: all six checksum scopes are unambiguous, the decoded tile image is fully determined by declarations alone (order, offsets, endianness, bool encoding, packing, padding content, pad bits), the index geometry and sentinel are exact, and the six spec-stated constants I could recompute are all correct. The residual defects are register bookkeeping (O1, O3, O4), one under-specified corner of dead-space classification that changes no obligation as written (O2), and one external-format sharp edge worth a note (O5).
