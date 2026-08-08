# TARN differential-writer run — layer "s", two commits

All CRC-32C values below were computed with an implementation self-tested against the spec's own constants: CRC-32C(`"123456789"`) = `0xE3069283` and CRC-32C(zero bytes) = `0x00000000` (§4.5), the all-sentinel full-segment constant `0xEECB3BB2` (`[R-IDX-05]`), and Appendix A's trailer CRC `0xE00938D2`. All four reproduce.

## 0. Derived geometry (identical for both writers — nothing free here)

`[R-GEO-03]`: G_t = ⌈2/1⌉ = 2, G_u = ⌈5/2⌉ = 3, **N = 6**, **P = ∏Tᵢ = 2**, C = 2, layout planar ⇒ **entry_count = C·N = 12**.
`[R-GEO-06]`: disk ordinal = c·N + s; v is channel 0 (do 0–5), ok is channel 1 (do 6–11). "ok at spatial ordinal 2" = **disk ordinal 8** — the sentinel.
`[R-CNT-17]`: index extent_length = 12×20 + ⌈12/2¹⁶⌉×4 = **244**.
Decoded sizes (§14.2, §14.3): v plane = P·B = **8 bytes**; ok plane packs = ⌈P/8⌉ = **1 byte**. Codec 1 ⇒ entry length must equal these (`[R-COD-04]`).
Edge padding (§11.3): G_u·T_u = 6 > E_u = 5, so in-tile ordinal 1 of spatial tiles s=2 and s=5 is a padding position; `[R-SER-05]` forces fill there. `[R-SER-03]`/`[R-SER-05]`: bits 2–7 of every ok plane byte are pad bits carrying the fill bit (fill = `0x01` ⇒ 1).

**Samples I chose** (stated as required). v(t,u), float32: row t=0 → 1.0, 2.0, 3.0, 4.0, 5.0; row t=1 → 6.0, 7.0, 8.0, 9.0, 10.0. Commit 2 supersedes the v tile at spatial ordinal 4 (do 4), changing v(1,2)→8.5 and v(1,3)→9.5. ok(t,u), bool: t=0 → T, F, T, T, **(0,4) is in the unstored tile so it reads fill = true, `[R-TYP-08]`)**; t=1 → F, T, F, F, T.

**Stored tile bytes — byte-identical in both files, and forced.** Filter 2 stride is the channel element size for a planar numeric tile and identity (s=1) for a packed bool plane (`[R-COD-10]`); filter runs before codec (`[R-COD-01]`); codec 1 stores the filtered image verbatim (`[R-COD-04]`). Shuffle verified against `[R-COD-10]`'s own worked example.

| do | decoded image | stored bytes |
|---|---|---|
| 0 | `00 00 80 3F 00 00 00 40` | `00 00 00 00 80 00 3F 40` |
| 1 | `00 00 40 40 00 00 80 40` | `00 00 00 00 40 80 40 40` |
| 2 | `00 00 A0 40` + fill `00 00 00 00` | `00 00 00 00 A0 00 40 00` |
| 3 | `00 00 C0 40 00 00 E0 40` | `00 00 00 00 C0 E0 40 40` |
| 4 (gen 2) | `00 00 08 41 00 00 18 41` | `00 00 00 00 08 18 41 41` |
| 5 | `00 00 20 41` + fill | `00 00 00 00 20 00 41 00` |
| 6 | `FD` (T,F + 6 fill pad bits) | `FD` |
| 7 | `FF` | `FF` |
| 8 | — | **sentinel** `FF×16 00×4` |
| 9 | `FE` | `FE` |
| 10 | `FC` | `FC` |
| 11 | `FF` (T + fill padding position + fill pad bits) | `FF` |

Layer-record inline payload is 101 bytes, identical in both files except the final `crc_of_crc_array`:
`01 73 | 02 | 01 00 | 01 00 | 02 00 | 00 02 00 00 00 00 00 00 | 00×8 | 00×8 | 02 | 02 00 | 01 74 <E=2> <T=1> | 01 75 <E=5> <T=2> | 01 76 0C 00 04 00 00 00 00 | 02 6F 6B 01 00 01 01 | 01 | 0C 00 00 00 00 00 00 00 | <crc_of_crc>`

---

## 1. FILE A (after commit 2) — F = 6656

Gen 1 placed the index at 16 and packed tiles at consecutive 512-boundaries; gen 2 appended from F=5888, taking the first legal 512-aligned offset (6144).

| range | size | content |
|---|---|---|
| [0,16) | 16 | front block `89 54 41 52 4E 0D 0A 1A` + 8 zeros |
| [512,520) [1024,1032) [1536,1544) [2048,2056) [3072,3080) | 8 ea | v do 0,1,2,3,5 (gen-1 bytes, still live) |
| [3584,3585) [4096,4097) [4608,4609) [5120,5121) [5632,5633) | 1 ea | ok do 6,7,9,10,11 |
| [6144,6152) | 8 | **v do 4, superseding** `00 00 00 00 08 18 41 41` |
| [6152,6396) | 244 | tile-index region (below) |
| [6396,6418) | 22 | metadata extent: `7B 22 74 61 72 6E 2E 74 69 74 6C 65 22 3A 22 73 22 7D` + CRC `62 A4 AD 8B` |
| [6418,6572) | 154 | directory (below) |
| [6572,6592) | 20 | pre-trailer pad (`[R-CNT-05]`: < 64) |
| [6592,6656) | 64 | trailer |

Index region (entries in disk-ordinal order, `[R-IDX-01]`; offsets little-endian):
```
0200000000000000 0800000000000000 777EC438   1000..? do0 @512
0004000000000000 0800000000000000 9641C512   do1 @1024
0006000000000000 0800000000000000 3AA9BAF6   do2 @1536
0008000000000000 0800000000000000 64F34466   do3 @2048
0018000000000000 0800000000000000 EF523A6D   do4 @6144  <-- new
000C000000000000 0800000000000000 72F8B8B7   do5 @3072
000E000000000000 0100000000000000 F7703B1E   do6 @3584
0010000000000000 0100000000000000 000000FF   do7 @4096
FFFFFFFFFFFFFFFF FFFFFFFFFFFFFFFF 00000000   do8 SENTINEL
0012000000000000 0100000000000000 03836B0D   do9 @4608
0014000000000000 0100000000000000 F4F350EC   do10 @5120
0016000000000000 0100000000000000 000000FF   do11 @5632
segment CRC array: 7F E0 0D DE
```
`crc_of_crc_array` = `AB 02 55 20`.

Directory — A emits the metadata record first (order carries no meaning, `[R-CNT-14]`):
```
02 00 02 00 01 00 00 00  FC 18 00 00 00 00 00 00  16 00 00 00 00 00 00 00  01
01 00 03 00 65 00 00 00  08 18 00 00 00 00 00 00  F4 00 00 00 00 00 00 00  <101-byte inline>
directory CRC: 00 02 21 C6
```
Trailer:
`8A 4E 52 41 54 0D 0A 1A | 01 00 | 00 00 | 00 00 00 00 | gen=2 | dir_offset=6418 | dir_length=154 | F=6656 | file_id=0x9E3779B97F4A7C15 | 00×4 | CRC 5B E3 37 6A`

All slack zero-filled (`[R-CNT-03]` SHOULD).

---

## 2. FILE B (after commit 2) — F = 50432

B wrote tiles first at 4096-boundaries (4096 mod 512 = 0, so the declared A=512 invariant holds a fortiori), put the index after them at a round offset, left deliberate gaps, and pretty-printed the JSON.

| range | size | content |
|---|---|---|
| [0,16) | 16 | front block |
| [4096,…) [8192,…) [12288,…) [16384,…) [24576,…) | 8 ea | v do 0,1,2,3,5 |
| [28672,…) [32768,…) [36864,…) [40960,…) [45056,…) | 1 ea | ok do 6,7,9,10,11 |
| [49152,49160) | 8 | **v do 4, superseding** — same 8 bytes as A |
| [49664,49908) | 244 | tile-index region |
| [50000,50027) | 27 | metadata extent: `7B 0A 20 20 22 74 61 72 6E 2E 74 69 74 6C 65 22 3A 20 22 73 22 0A 7D` + CRC `A6 14 55 E1` |
| [50176,50330) | 154 | directory |
| [50330,50368) | 38 | pre-trailer pad |
| [50368,50432) | 64 | trailer |

Index region: same 12 entries in the same order, same **lengths, same crcs, same sentinel**; only the offset fields differ (`0010…`=4096, `0020…`=8192, `0030…`, `0040…`, `00C0…`=49152, `0060…`, `0070…`, `0080…`, sentinel, `0090…`, `00A0…`, `00B0…`). Segment CRC array `9D D1 B0 8A`; `crc_of_crc_array` = `3C 28 B8 68`.

Directory — layer record first, then metadata:
```
01 00 03 00 65 00 00 00  00 C2 00 00 00 00 00 00  F4 00 00 00 00 00 00 00  <101-byte inline>
02 00 02 00 01 00 00 00  50 C3 00 00 00 00 00 00  1B 00 00 00 00 00 00 00  01
directory CRC: 01 D9 F2 A7
```
Trailer: gen=2, dir_offset=50176, dir_length=154, F=50432, file_id=2, CRC `78 5B 89 6E`.

---

## 3. Difference table

Column (b) — "a place one of you must be wrong" — is **empty**. Every difference is a granted freedom or a forced consequence of one.

| # | What differs | A | B | Class | Rule |
|---|---|---|---|---|---|
| 1 | Offset of each of the 11 live stored tiles | 512…6144 | 4096…49152 | **(a) freedom** | `[R-SLB-05]` placement free; `[R-SLB-01]` only constrains `offset mod A = 0`, satisfied by both |
| 2 | Offset of the tile-index region | 6152 | 49664 | **(a)** | `[R-SLB-05]`; `[R-CNT-13]` bounds only (≥16, ≤F−64, no overlap). Alignment A binds *stored tiles*, not the index (`[R-SLB-01]`) |
| 3 | Offset of the metadata extent | 6396 | 50000 | **(a)** | `[R-CNT-13]`, `[R-SLB-05]` |
| 4 | dir_offset | 6418 | 50176 | **(a)** | `[R-CNT-06]` (≥16, +len ≤ F−64) and `[R-CNT-05]` (gap < 64) are the only constraints |
| 5 | Pre-trailer pad size | 20 | 38 | **(a)** | `[R-CNT-05]` "fewer than 64 bytes" |
| 6 | committed_file_length / F | 6656 | 50432 | **(a)** consequence of 1–5 | `[R-CNT-01]` only requires F = file size, multiple of 64 |
| 7 | file_id | `9E37…7C15` | `2` | **(a)** | `[R-LIF-03]`'s randomness is a SHOULD *and* undecidable from bytes ⇒ conduct, not predicate, `[R-CNF-02]`; trailer table requires only ≠0 |
| 8 | Order of the two records in the directory | meta, layer | layer, meta | **(a)** | `[R-CNT-14]` "Record semantics MUST NOT depend on record order" |
| 9 | Metadata document bytes (18 vs 23) | `{"tarn.title":"s"}` | pretty-printed | **(a)** | `[R-MTA-04]` imposes only object/no-BOM/finite/no-dup/UTF-8; `[R-MTA-05]` fixes member order only and states "does not make two writers' output identical"; `[R-CNF-05]` |
| 10 | Metadata record extent_length (22 vs 27) | — | — | **(a)** consequence of 9 | `[R-CNT-25]` requires only ≥5 and (≠0,≠0) |
| 11 | Slack size and distribution (6103 vs 49874 bytes) | — | — | **(a)** | `[R-CNT-21]`, `[R-SLB-05]` "wastes space rather than violating a rule" |
| 12 | Index entry **offset** fields (11 of 12) | — | — | forced consequence of 1 | `[R-IDX-01]`; given placement, no freedom remains |
| 13 | Segment CRC array (`7FE00DDE` vs `9DD1B08A`) | — | — | forced consequence of 12 | `[R-IDX-04]`, partial segment MUST be computed `[R-IDX-05]` |
| 14 | `crc_of_crc_array` (`AB025520` vs `3C28B868`) | — | — | forced consequence of 13 | `[R-CNT-23]`, §8.1 |
| 15 | Layer-record header `extent_offset` | 6152 | 49664 | forced consequence of 2 | §7.4 |
| 16 | Metadata extent terminal CRC | `62A4AD8B` | `A61455E1` | forced consequence of 9 | §8.1, `[R-CNT-19]` |
| 17 | Directory CRC | `000221C6` | `01D9F2A7` | forced consequence of 8/14/15 | `[R-CNT-11]` |
| 18 | Trailer CRC | `5BE3376A` | `785B896E` | forced consequence | `[R-CNT-06]` |

**Byte ranges that are identical and could not legitimately have differed:** front block [0,16) (`[R-CNT-04]`); every stored tile's *content*, including the shuffle permutation and every fill-encoded padding position and pad bit (`[R-SER-01]`–`[R-SER-03]`, `[R-SER-05]`, `[R-COD-04]`, `[R-COD-10]`); all 12 index-entry **length** and **crc** fields and the sentinel's exact 20 bytes (`[R-IDX-02]`); entry ordering, channel-major (`[R-GEO-06]`, `[R-IDX-01]`); index extent_length = 244 (`[R-CNT-17]`); 97 of the 101 layer-inline bytes; both record headers' type/flags/inline_length (`[R-CNT-22]` fixes layer = MU1/PE1 = `0003`, user metadata = MU0/PE1 = `0002`; `[R-MTA-03]` fixes inline_length = 1); dir_length = 154 both; trailer magic, version_major = 1, version_minor = 0 (`[R-CNT-26]`), flags = 0 (`[R-CNT-08]`), generation = 2 (`[R-LIF-02]` step 5), reserved zeros.

---

## 4. Coverage partition and the verifier's figure

Both live states were audited for disjointness and exhaustiveness against §5.2's classes; both **satisfy the partition of `[R-CNT-02]`**, and each enumerated structure lies within [16, F−64) as `[R-LIF-08]` requires.

**File A.** live-claimed = 16 (front block) + 53 (11 stored tiles: 6×8 + 5×1) + 244 (index region) + 22 (metadata extent) + 154 (directory) + 64 (trailer) = **553**.
Slack = 6656 − 553 = **6103 bytes**. (Cross-check by enumeration: 496 after the index + 1016 + 504×2 + 1016 + 504 + 511×5 + 511 + 20 = 6103, and it contains the superseded gen-1 v-do-4 tile at [2560,2568), the gen-1 index at [16,260), the gen-1 directory at [5633,5762), and the gen-1 trailer at [5824,5888).)

**File B.** live-claimed = 16 + 53 + 244 + **27** + 154 + 64 = **558**.
Slack = 50432 − 558 = **49874 bytes**.

**Do the figures differ, and does the spec determine that they should?** They differ by 43,771 bytes, and **the specification determines nothing about their equality — it licenses the difference.** `[R-CNF-05]`: two conforming writers given identical input MAY produce different conforming files. `[R-SLB-05]`: placement is free, and "a writer that scatters structures wastes space rather than violating a rule, and the verifier's slack total is what surfaces the waste." `[R-CNT-21]` requires a verifier to *report* the total, not to bound it. The 5-byte difference in live-claimed bytes is likewise licensed, by `[R-MTA-05]`'s explicit disclaimer of cross-writer byte identity. Both figures are correct reports about two conforming files.

---

## Findings

### BYTE-LEVEL AMBIGUITY
None. Every byte of both files is classifiable as a granted freedom or a forced value.

The three places I expected to bite, and the sentences that close them (searches stated):
- **Shuffle stride on the packed bool plane.** I searched §17.3 for the planar/bool interaction. `[R-COD-10]`'s "for a packed boolean plane s = 1 and the filter is the identity" closes it *twice over* — even a reader who stops at the first clause ("the channel's element size for a planar tile") gets s = 1, because §12.1 gives bool element size 1. Two readings, same bytes.
- **Whether alignment A constrains the tile-index region or only stored tiles.** I searched §16.1 and §7.4. `[R-SLB-01]`: "every stored tile's offset satisfies offset mod A = 0" — stored tiles only. B's index at 49664 and A's at 6152 (not 512-aligned) are both legal.
- **Pad bits vs. padding positions in ok's disk ordinal 11, where both occur in one byte.** I searched §14.3, §14.5 and §14.3's Note. `[R-SER-05]` covers both explicitly ("the fill bit in a packed plane" / "Every pad bit … MUST carry the plane's channel's fill bit"), and §14.3's worked `55 FD` example confirms the encoding. Byte is forced to `FF`.

### CONTRADICTION
**Is a verifier obliged to check that slack/pad bytes are zero?** Two normative sentences answer oppositely.
- §22.3 `[R-SEC-04]`: "Declared padding is covered by no checksum (§8.1): corruption confined to padding is invisible to a reader and **caught only by a verifier's zero check** (`[R-CNT-03]`)."
- §5.2 `[R-CNT-03]`: "Writers **SHOULD** zero the gaps they create — the run before an aligned tile or slab run, and the pre-trailer pad. … **no conformance requirement rides on slack content either way**." Reinforced by §5.2 `[R-CNT-21]` ("its content is unconstrained, and no conformance requirement applies to it"), §16.1 `[R-SLB-01]` ("which writers SHOULD zero and no conformance requirement constrains"), and §21.6's row ("Slack: unconstrained content, no conformance requirement").

`[R-SEC-04]` asserts a verifier check that the very requirement it cites denies exists. Non-normative Appendix H repeats it ("**Conforming verifier** — … declared-padding content (§5.2)"), citing a section that says the opposite. Not byte-level: four explicit statements against one, and `[R-SEC-04]`'s own citation refutes it, so a careful reader concludes no such check exists — which is what I did when both files' pads are zeroed only by SHOULD.

### OBSERVATION
1. **§9.7's walk omits the front block and the trailer, and over-counts slack by 80 bytes if read alone.** `[R-LIF-08]` enumerates "the live directory and its records, each record's extent, and each layer's tile-index region together with that region's non-sentinel entries", checks "that each lies within [16, F − 64)" — a bound that excludes both fixed-position structures — then says "Bytes the walk does not reach are slack." Taken literally the figure would be 6183 / 49954 rather than 6103 / 49874. Resolved by §5.2, which I searched first: `[R-CNT-02]` names the front signature block and the trailer as coverage classes, `[R-CNT-21]` defines slack as "every byte the live state does not claim", and §9.7's own opening clause subordinates the walk to `[R-CNT-02]`. Since the task turns on this number, the omission is worth an editorial fix — §9.7 should name the front block and trailer as reached.
2. **"Declared padding" is an undefined term with no coverage class.** It appears in §5.1's list of what lies between front block and trailer, in §22.3, and in Appendix H, but §5.2's partition has no class for it and no field anywhere declares padding. Under §5.2 any such bytes are simply slack. Reads as vestigial.
3. **`[R-LIF-03]`'s file_id randomness cannot be a file-level requirement.** No predicate on a 64-bit value decides whether it was randomly drawn, so B's `file_id = 2` is a conforming file by `[R-CNF-02]`'s conduct/predicate split, though the trailer table's "≠ 0" is the only byte-level constraint. Worth making explicit in §9.3, since §2.3's list of conduct rules cites only §10.3 and §18.3.
4. **Slack is not monotone, and nothing says so.** `[R-LIF-01]` forbids *modifying* committed bytes, not *referencing* them: commit 2 could legally have pointed the new metadata record's extent slot at bytes that generation 1 committed and generation 1's directory no longer reaches, pulling previously-slack bytes back into the live state. Neither writer did, and no rule forbids it; the verifier's slack total would simply fall. Harmless but unstated.
5. **`[R-CNT-26]`'s version_minor is a SHOULD with a stated consequence, and the trailer table's valid range for version_minor is "any".** A writer emitting minor = 3 for this file is conforming-but-discouraged; both writers emitted 0, so no divergence arose. Mentioned only because it is the one remaining trailer field whose value the spec does not pin.
6. **The commit-2 index shows entry 4 pointing forward past entry 5** (offset 6144 vs 3072 in A; 49152 vs 24576 in B). This is correct — no ordering rule applies absent a slab declaration (`[R-SLB-05]`) — and it is the visible fingerprint of the append model. Worth a conformance vector under `[R-ERR-02]`, since a naive verifier could mistake it for `[R-SLB-03]`-style disorder in a layer that declares no slab.

## Verdict
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: high
