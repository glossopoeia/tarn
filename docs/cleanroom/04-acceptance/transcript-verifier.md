# TARN Verifier Charter — Certification Procedure, Worked Trace, and Findings

Source read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (3235 lines) and nothing else. Section and requirement citations are to that text.

---

## Part 1 — The complete certification procedure

A verifier is a reader first (`[R-CNF-11]`, §2.3), so it inherits every reader obligation and adds the checks readers are exempted from. It certifies only violation-free files (`[R-CNF-12]`, §2.4); outcome classes describe blast radius for *readers*, so for certification any violation at any scope is fatal to the verdict while still being *reported* at its own scope. Order below is dependency order: no step acts on a field before the checksum covering it verifies (`[R-ENC-05]`, `[R-ENC-10]`, §8.2's chain trailer → directory → crc_of_crc_array → segment CRC array → segment → entry → stored tile).

### Phase 0 — Preconditions on the verifier itself
- Its CRC-32C must reproduce §4.5's check vector (`"123456789"` → `0xE3069283`; zero bytes → `0x00000000`), else it does not implement this specification's checksum.
- It must be able to execute every layer's codec and filter, or it MUST NOT certify (`[R-COD-11]`, §17.4) — because §14's decoded-content obligations (`[R-SER-05]`, `[R-SER-08]`) require decoding.

### Phase 1 — Envelope (file scope; every failure reject-file)
1. Obtain the transport-authoritative size (`[R-CNT-10]`). Reject if < 128 (`[R-CNT-27]`; register **F7**).
2. Byte-equality on [0,16) (`[R-CNT-04]`; **F10**, **F2**).
3. Trailer at [F−64, F), validated in §6.2's fixed order — magic (**F13**), trailer CRC over [0,60) (**F19**), version gate (**F23**, **F24**) — these three first because only their positions are fixed across all majors (`[R-CNT-24]`).
4. Gates passed, then the remaining fields before acting on any of them (`[R-CNT-06]`): incompat-lane flag bits (**F25**), ignore lane ignored (`[R-CNT-08]`); `committed_file_length` = transport size (**F22**, **F38**) and a multiple of 64 (**F18**); `dir_offset` ≥ 16 (**F14**); `dir_length` ≥ 4 (**F21**); `dir_offset + dir_length` ≤ F−64 (**F15**, with the sum rule **F4** and the domain rule **F3**); `generation` ≥ 1 (**F16**); `file_id` ≠ 0 (**F17**); reserved [56,60) zero (**F20**).
5. *Verifier-only:* the pre-trailer gap — nothing but a zero pad, fewer than 64 bytes, between the directory's end and the trailer (`[R-CNT-05]`; **F11**, **F12**). Readers are explicitly exempt.

### Phase 2 — Directory (file scope)
6. Verify the region's terminal CRC over the preceding `dir_length − 4` bytes *before any other use* (`[R-CNT-11]`; **F26**).
7. Parse the record sequence: complete 24-byte-header records, no residue (**F31**); type ≠ 0 (**F28**) (`[R-CNT-12]`).
8. *Verifier-only per record:* reserved flag bits 2–15 zero (**F30**/**L48**), MU = 1 with PE = 0 forbidden (**F29**/**L47**) (`[R-CNT-12]`); a reserved-range type is a validity error at the record's governing scope (`[R-CNT-15]` — no register row, see Findings); a registered type whose stored MU/PE differ from §7.3's fixed values SHOULD be reported (`[R-CNT-22]`).
9. Unknown types: MU = 1 → reject-file (**F37**); MU = 0 → ignore-record (**R10**), but the record's extent is still a *structure* for coverage (`[R-CNT-02]`).
10. Multiplicity: at most one top-level user-metadata record (**F36**) (`[R-CNT-14]`).
11. Extent slots of non-layer top-level records (`[R-CNT-13]`): (0,0) or both halves nonzero (**F32**), offset ≥ 16 (**F33**), offset+length ≤ F−64 (**F34**), no overflow (**F4**). A user-metadata record with (0,0), or `extent_length` < 5, is a validity error at its containing scope (**F27**, §7.1).
12. Layer-name namespace, at open: each layer record's name parsed per §4.6 (**L4**, **L6**, **L7**) and globally unique (**F6**, `[R-ENC-15]`).

### Phase 3 — Per layer, from resident bytes only (layer scope; §19.3, no I/O)
13. Layer-record extent slot (**L14**, **L15**, **L16**, **L1**, **L2**).
14. Exact parse of the inline payload: leading fixed fields, *d* dimension entries, *C* channel entries, trailing fixed fields, then sub-records with no residue (**L22**, **L3**, **L13**) (`[R-CNT-18]`).
15. Value sets: layout (**L35**), linearization (**L32**), codec (**L44**), filter (**L46**), `index_encoding` (**L30**), channel type (**L33**) — reserved and experimental values are errors, not features (`[R-EXT-03]`).
16. Names: dimension/channel UTF-8 well-formed (**L5**), non-empty, no U+0000–U+001F (**L8**, **L9**), unique within the layer (**L10**).
17. Fill: length prefix equals the type's element size (**L29**); a bool fill is `0x00` or `0x01` (**L34**).
18. Layout declarations: A a power of two in [512, 2⁶²] (**L38**); A ≠ 0 with S ≠ 0 forbidden (**L19**); S = 0 → A_slab = 0 (**L27**); S ≠ 0 → A_slab a power of two in [1, 2⁶²] (**L28**).
19. Geometry floor and arithmetic: d ≥ 1, C ≥ 1, Tᵢ ≥ 1 (**L31**); Gᵢ = ⌈Eᵢ/Tᵢ⌉, N = ∏Gᵢ, P = ∏Tᵢ; every derived sum and product overflow-checked (**L2**, `[R-ENC-04]`).
20. Index cross-checks: `entry_count` = addressed-tile count, N interleaved / C·N planar (**L20**); `extent_length` = `entry_count`×20 + ⌈`entry_count`/2¹⁶⌉×4, including the (0,0) ↔ zero-entry equivalence (**L21**); `entry_count` = 0 → `crc_of_crc_array` = 0 (**L26**) (`[R-CNT-17]`, `[R-CNT-23]`).
21. Codec declaration bound: codec 4 requires decoded tile size ≤ `0x7E000000` (**L45**).
22. Sub-records: type ≠ 0 (**L12**), no nesting (**L23**), unknown MU = 1 → reject-layer never reject-file (**L24**), a layer record nested as a sub-record (**L25**), at most one user-metadata sub-record (**L18**), slot (0,0) on one (**L11**).

### Phase 4 — Index chain (layer scope)
23. Verify `crc_of_crc_array` over the fetched segment-CRC array (**L36**), then each segment CRC over exactly entries [s·2¹⁶, min((s+1)·2¹⁶, `entry_count`)) as stored (**L37**). A verifier does *every* segment, not just the ones a read would touch. The all-sentinel constant `0xEECB3BB2` never substitutes for comparison (`[R-IDX-05]`).
24. Classify every entry per §15.3 (`[R-IDX-03]`): sentinel with crc ≠ 0 (**T6**); half-sentinel (**T7**); non-sentinel offset < 16 (**T8**), extent past F−64 (**T9**), length 0 (**T10**), field > 2⁶³−1 (**T11**), overflowing sum (**T12**). Entries classified reject-tile here contribute no extent to the whole-file rows of step 30.

### Phase 5 — Per stored tile (tile scope)
25. Fetch [offset, offset+length); verify the entry's crc before decoding (**T1**).
26. Declaration-only pre-checks: codec 1 length = decoded size (**T14**); codec 2 raw RFC 1951, one stream (**T15**, **T16**); codec 3 magic (**T17**), exactly one frame with no skippable frame (**T18**), Dictionary_ID 0 (**T19**), no Content_Checksum flag (**T20**), window ≤ decoded size (**T21**), Frame_Content_Size = decoded size when present (**T22**); codec 4 is a raw block, not a frame (**T23**).
27. Decode, then the filter's inverse (§17.1): exact consumption (**T24**), no malformed stream (**T25**), independent decodability (**T13**), decoded length exactly the declaration-derived decoded size (**T3**, `[R-SER-07]`).
28. *Verifier-only decoded content:* every padding position encodes its channel's fill (**T4**), every pad bit of a packed bool plane carries the fill bit (**T5**), every interleaved bool byte at a real position is `0x00`/`0x01` (**T2**), and a mis-strided filter wherever it breaks either (**T26**) (`[R-SER-05]`, `[R-SER-08]`, `[R-COD-10]`).

### Phase 6 — Record extents (ignore-record scope; SHOULD-report)
29. User-metadata extents: terminal CRC (**R2**); encoding byte 1 or 2 and implemented (**R1**); decode (**R3**); JSON object, no BOM (**R6**); finite numbers (**R7**); no duplicate decoded keys (**R8**); UTF-8 well-formed including after escape resolution (**R4**); keys non-empty, no C0 (**R5**), ≤ 255 bytes (**R9**); and — verifier-only — members sorted by their keys' UTF-8 bytes, which `[R-MTA-05]` says a verifier MUST report and which makes the file nonconforming. Unknown MU = 0 record extents are opaque: no content check, but they are structures for coverage.

### Phase 7 — Whole-file cross-structure checks (verifier-only)
30. Build the live-state range set: front block; the directory; the trailer; every top-level record extent; every layer's tile-index region; every layer sub-record extent; every non-sentinel entry's stored extent; and the declared-padding runs. Check disjointness — intra-layer overlap → reject-layer (**L17**), cross-layer or against another scope's structure → reject-file (**F35**) — and that every structure lies in [16, F−64) (`[R-LIF-08]`).
31. Compute declared padding *constructively* per §5.2: the sub-modulus run immediately preceding an alignment- or slab-constrained structure, and the sub-64-byte pre-trailer pad. Every live byte must land in exactly one class or **F8** fires. Declared padding must be all-zero or **F9** fires (`[R-CNT-03]`).
32. Layout invariants: stored-tile offset mod A = 0 (**L39**); within each slab run, contiguity and ordinal packing with sentinels transparent (**L41**), first stored tile aligned to A_slab (**L42**), and no stale declaration carried forward (**L43**, which `[R-SLB-04]` reduces to the live-state failures of **L41**/**L42**).
33. Dead space is the residue: sum and report the total (`[R-CNT-21]`, `[R-LIF-08]`). Its content is unconstrained and no conformance requirement applies to it.

### Phase 8 — Verdict
Certify only if nothing above fired. Report, per §24's vocabulary: for each damaged structure the outcome class, the scope, and the register row; plus the dead-byte total always; plus SHOULD-level findings (stored-flag mismatch, unsorted metadata keys, ignored records). A refusal on resource grounds is reported as a limit, never as a validity error (`[R-ERR-04]`).

**Constants verified computationally** from the spec's own text: CRC-32C(`"123456789"`) = `0xE3069283`; CRC-32C(∅) = `0x00000000`; CRC-32C of 2¹⁶ sentinel entries = `0xEECB3BB2` (`[R-IDX-05]`); Appendix A's trailer CRC over bytes [0,60) = `0xE00938D2`, stored `D2 38 09 E0`. All four match. §21.8's claim of "213 named instances" over §21.2–§21.5 also verifies by mechanical count (F 69 + L 81 + T 43 + R 20 = 213), and the row counts 38/47/26 are exact.

---

## Part 2 — Worked trace

**The file.** One layer `img`: interleaved (layout 1), linearization 1, codec 1 (none), filter 1 (none), A = 0, S = 0, A_slab = 0, d = 2, C = 1. Dimensions `y` (E=3, T=2) and `x` (E=4, T=2) → G = (2,2), N = 4, P = 4. One channel `v`, type 6 (uint8, element size 1), fill `0x00`. Interleaved ⇒ Q = 1, decoded size = P·Q = 4 bytes per tile; `entry_count` = N = 4; index region = 4×20 + ⌈4/2¹⁶⌉×4 = **84 bytes**. The layer record's inline payload is 38 (leading fixed) + 36 (two dimension entries) + 6 (one channel entry) + 13 (trailing fixed) + 25 (one user-metadata sub-record: 24-byte header + 1-byte encoding) = **118**, so the record is 142 bytes and each generation's directory is **146** bytes.

Because G_y·T_y = 4 > E_y = 3, the tiles at t_y = 1 — spatial ordinals s = 2t_y + t_x = 2 and 3 — carry padding positions at in-tile ordinals 2 and 3 (`[R-GEO-04]`, §11.3). Four padding bytes in the file must equal fill `0x00` (`[R-SER-05]`).

**Generation 1** (F₁ = 384): front block [0,16); tiles at [16,20), [20,24), [24,28), [28,32); index region [32,116); user-metadata extent [116,141) (21-byte document `{"tarn.title":"demo"}` + 4-byte CRC); directory [141,287); pad [287,320), 33 zero bytes; trailer [320,384).

**Generation 2** — supersedes tile ordinal 2. Writing begins at exactly F₁ (`[R-LIF-02]`): new payload [384,388); the layer's **whole** index region re-emitted [388,472) with entry 2 re-pointed and entries 0, 1, 3 byte-identical (`[R-WRT-04]` step 4); directory [472,618) carrying a modified layer record (extent slot now (388,84), `crc_of_crc_array` updated, sub-record slot still (116,25)); pad [618,640), 22 bytes; trailer [640,704). F₂ = 704.

**Generation 3** — amends the layer's user-metadata sub-record. New extent [704,730) (22-byte document `{"tarn.title":"demo2"}` + CRC); the layer's index does not change, so the layer record keeps its extent slot (388,84) (`[R-WRT-04]`: "A layer whose record alone changes keeps its extent slot"); directory [730,876) with the sub-record slot re-pointed to (704,26); pad [876,896), 20 bytes; trailer [896,960). F₃ = 960 = 64×15.

### Every byte, classified

| Range | Bytes | Class (§5.2) | Written by |
|---|---|---|---|
| [0,16) | 16 | front signature block | gen 1 |
| [16,20) | 4 | structure — stored-tile extent, ordinal 0 | gen 1 |
| [20,24) | 4 | structure — stored-tile extent, ordinal 1 | gen 1 |
| [24,28) | 4 | **dead** — superseded payload of ordinal 2 | gen 1 |
| [28,32) | 4 | structure — stored-tile extent, ordinal 3 | gen 1 |
| [32,116) | 84 | **dead** — superseded tile-index region | gen 1 |
| [116,141) | 25 | **dead** — superseded user-metadata extent | gen 1 |
| [141,287) | 146 | **dead** — generation-1 directory | gen 1 |
| [287,320) | 33 | **dead** — generation-1 pre-trailer pad | gen 1 |
| [320,384) | 64 | **dead** — generation-1 trailer | gen 1 |
| [384,388) | 4 | structure — stored-tile extent, ordinal 2 | gen 2 |
| [388,472) | 84 | structure — record extent (tile-index region) | gen 2 |
| [472,618) | 146 | **dead** — generation-2 directory | gen 2 |
| [618,640) | 22 | **dead** — generation-2 pre-trailer pad | gen 2 |
| [640,704) | 64 | **dead** — generation-2 trailer | gen 2 |
| [704,730) | 26 | structure — record extent (user-metadata document) | gen 3 |
| [730,876) | 146 | structure — the directory | gen 3 |
| [876,896) | 20 | **declared padding** — pre-trailer pad, must be zero | gen 3 |
| [896,960) | 64 | structure — the trailer | gen 3 |

Live 372 + dead 588 = 960 ✓ — the partition of `[R-CNT-02]` holds, and nothing overlaps.

Three points the trace makes concrete. First, **generation attribution is not a verifier concept**: three of the four live payloads were written by generation 1, are located through an index written by generation 2, which is pointed at by a layer record written by generation 3 — exactly what `[R-CNT-13]`'s "whichever generation's commit appended them" licenses, and the walk of §9.7 never needs to know which. Second, **the prior generations' pre-trailer pads are dead space now, not declared padding**: §5.2 admits only the run preceding the *live* trailer, so [287,320) and [618,640) lose their zero-content obligation the moment a later commit lands, even though the writer wrote them zero. Third, **only [876,896) carries the zero obligation** (**F9**); a single nonzero byte there is reject-file, while a nonzero byte anywhere in the 588 dead bytes is nothing at all.

### What the operator is told

```
VERDICT     CERTIFIED CONFORMING  (format major 1, minor 0, flags 0x00000000)
            generation 3, file_id <64-bit>, committed_file_length 960 = physical size
COVERAGE    live-state partition verified: 372 bytes in 10 disjoint ranges,
            each within [16, 896) except the front block and the trailer;
            declared padding: 1 run, [876,896), 20 bytes, all zero
DEAD SPACE  588 bytes (61.3% of the file) — compaction recommended (§20.5)
LAYERS      1 — "img": 4 addressed tiles, 4 stored, 0 sentinel;
            index chain verified (crc_of_crc_array + 1 segment CRC over 4 entries);
            4 stored-tile CRCs verified; 4 decoded images at exactly 4 bytes;
            4 padding positions checked against fill 0x00 — pass
METADATA    1 layer-scope document, encoding 1, extent CRC verified,
            JSON object, keys sorted, no duplicates — pass
ADVISORIES  none
```

### What certification does and does not establish

**Establishes.** That every byte a conforming reader can reach is accounted for exactly once; that every structure in the live state verifies against the one checksum covering it (§8.1); that every declaration is in its defined value set and every derived quantity is in domain; that the decoded content obeys the only content rules the format states (fill-encoded padding, pad bits, interleaved bool bytes); that the file's own committed length matches the transport's; and the dead-byte total.

**Does not establish.** That the sample values are *correct* — a well-formed file carrying wrong data is certified by every checksum in §8 (`[R-ERR-01]`, §21.7), including an undisclosed compression dictionary (`[R-COD-06]`) and a mis-strided filter that happens to break no structural constraint (**T26**'s exclusion). That the file is authentic — checksums detect accidental corruption, not tampering (`[R-SEC-07]`, §4.5, §22.5). That the file has not been rolled back — truncation to an earlier commit boundary is indistinguishable in-format, and detection needs out-of-band state (`[R-LIF-06]`). Which generation wrote a live byte, or what the 588 dead bytes were — dead space has no structure this specification defines, its content is unconstrained, and nothing enumerates prior commits (`[R-CNT-21]`, `[R-LIF-08]`). Whether a sentinel tile was ever written, as against never having been (§23.2 notes the index publishes only *which* regions were written). Whether the writer honored the commit protocol's two barriers, targeted the right registry version, or avoided experimental values in released software — those bind conduct, not bytes (`[R-CNF-02]`, §10.3). And nothing about the meaning of names or metadata, which §22.4 hands onward as untrusted display content.

---

## Findings

### BYTE-LEVEL AMBIGUITY 1 — §5.2 `[R-CNT-02]`/`[R-CNT-03]` vs `[R-CNT-21]` (with §16.1 `[R-SLB-01]`): the declared-padding run reaches backward into dead space

**Location.** §5.2, "A maximal run of bytes the live state does not otherwise claim is declared padding when, and only when, it is one of: the run immediately preceding a structure whose offset a layer's alignment or slab declaration constrains (§16), whose length is less than that declaration's modulus"; and §16.1, "the run of unclaimed bytes immediately preceding each such tile is declared padding — zero bytes, shorter than A".

**Reading A (literal).** The run is maximal over bytes the *live state* does not claim. Superseded bytes from earlier generations are not claimed by the live state, so the run extends backward through them. If the resulting maximal run is shorter than the modulus, the whole run — dead bytes included — is declared padding and MUST be zero (`[R-CNT-03]`, register **F9**, verifier, file scope).

**Reading B.** Dead space is defined in the same subsection as "bytes an earlier commit wrote that the live state no longer reaches — superseded payloads and index regions, and every prior generation's directory, padding, and trailer" (`[R-CNT-21]`). Bytes an earlier commit wrote are therefore dead by definition and can never be declared padding; the padding run begins at the previous generation's committed length F_prev, where §9.2 step 1 says writing begins.

**Discriminator.** File D. Generation 1 is Appendix A's 128-byte file verbatim (no layers), F₁ = 128 — its trailer at [64,128) begins `8A 4E 52 41 54 0D 0A 1A`. Generation 2 appends one layer declaring alignment **A = 4096**, one dimension (E = 4, T = 4), one uint8 channel with fill `0x00`, `entry_count` = 1, decoded size 4, index region 24 bytes. The commit writes 3968 zero bytes at [128, 4096), the stored tile at [4096, 4100) (4096 mod 4096 = 0 ✓), the index region at [4100, 4124), then directory, pad, trailer. Every byte generation 2 wrote as padding is zero.

- Reading A: the maximal unclaimed run preceding the aligned tile is **[16, 4096)** — 4080 bytes, less than A = 4096, and exactly the distance from 16 to the next legal offset. It is declared padding. Bytes [64,128) hold generation 1's trailer, which is not zero. Verdict: **F9, reject-file, NOT CERTIFIED** — and, because §9.1 makes [0, F₁) immutable, no writer can ever repair it, so a natural append pattern becomes unconstructible.
- Reading B: declared padding = [128, 4096), 3968 zero bytes; dead space = [16,128), 112 bytes. Verdict: **CERTIFIED CONFORMING**, dead-space total 112.

**What I searched to refute.** I looked for any bound on where a padding run may start: §9.2's "begin writing at exactly F" (constrains the writer, not the verifier's classification); §16.1 and §16.2, which repeat "the run of unclaimed bytes immediately preceding" with the same maximality and add only "shorter than A"/"shorter than A_slab" — both satisfied by the 4080-byte run; `[R-SLB-05]`, which says only that a byte "the live state neither claims nor accounts for as declared padding is dead space" — i.e. padding is classified *first*; and §9.7, whose walk enumerates "the declared padding §5.2 defines" without further qualification. §5.2's instruction that padding is "defined constructively, so a verifier computes it rather than infers it" pushes an implementer toward the literal biconditional. Nothing bounds the run's start. Note that the pre-trailer-pad limb of the rule is immune, because `[R-CNT-05]` forces the live directory to immediately precede it; only the alignment/slab limb can reach into dead space.

### BYTE-LEVEL AMBIGUITY 2 — §18.2 `[R-MTA-09]` vs §2.3 `[R-CNF-11]`/§17.4 `[R-COD-11]`: may a verifier certify a file whose user-metadata document it declined to decode?

**Location.** `[R-MTA-09]`: "a reader instead decodes with a bound of its own choosing, no smaller than §21.9's user-metadata guarantee, and a document exceeding that bound is ignore-record like any other it cannot read." Against §2.3's conforming verifier — "checks every file-level requirement — including those ordinary readers are exempted from — and certifies conformance" — and §17.4's closed analogue for codecs: "A verifier that cannot execute a layer's codec or filter cannot establish the layer's conformance and MUST NOT certify the file."

**Reading A.** The quarantine of `[R-CNT-25]` makes every way a document can be unreadable a defined, non-fatal ignore-record outcome. A verifier that cannot decode the document reports the ignored record and certifies the file.

**Reading B.** Certification requires establishing every file-level requirement. A document the verifier never decoded leaves `[R-MTA-04]`'s content rules and `[R-MTA-05]`'s sort rule unestablished, so by §17.4's principle the verifier MUST NOT certify.

**Discriminator.** File E: fully conforming in every structural respect, carrying one top-level user-metadata record with **encoding 2 (zstd)** whose decoded document is 20 MiB of well-formed JSON whose object members are **not** sorted by their keys' UTF-8 bytes. `[R-MTA-05]` states flatly: "the file is nonconforming, a verifier MUST report it". §21.9 confirms a 20 MiB document leaves the file conforming as to size, and `[R-ERR-03]`'s guarantee is 16 MiB.

- Verifier A picks the minimum licensed bound, 16 MiB. The document exceeds it → ignore-record by the express words of `[R-MTA-09]` (not a resource refusal). Nothing about the document is ever seen. Verdict: **CERTIFIED CONFORMING**.
- Verifier B picks 32 MiB. It decodes, finds unsorted members, and must report a violation. Verdict: **NOT CERTIFIED** (file nonconforming per `[R-MTA-05]`).

Both verifiers act exactly as `[R-MTA-09]` licenses; the file's conformance is a fixed predicate on bytes (`[R-CNF-02]`), yet certification of it is not. A second route to the same divergence: `[R-MTA-03]` says an encoding "the reader does not implement" is ignore-record, so a verifier may decline metadata encoding 2 outright — even though `[R-COD-03]` makes tile codec 3 (zstd) core.

**What I searched to refute.** I searched §18 (all of §18.1–§18.4), §7.1's quarantine paragraph, §2.3's class definitions, §9.7, §21.5, §21.9, §24, and Appendix H for a metadata analogue of `[R-COD-11]`. §17.4 is the only "cannot establish → MUST NOT certify" rule in the document and is scoped to "a layer's codec or filter". Appendix H's verifier checklist enumerates coverage, dead-space total, overlap, declared-padding content, alignment/slab, and decoded tile content — and does not mention the metadata document at all.

### CONTRADICTION 1 — §9.6 `[R-LIF-06]` vs §9.7 `[R-LIF-08]`: does coverage verification enumerate generations?

- §9.6 `[R-LIF-06]`: "Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0."
- §9.7 `[R-LIF-08]`: "A verifier checking `[R-CNT-02]`'s partition walks the live state only." Reinforced by §9.7's Note ("Nothing here enumerates prior commits") and §5.2's Rationale ("this specification certifies the live state exactly, and counts the rest").

Both are normative sentences in requirements. §9.6 states that a backward trailer probe to offset 0 *is* the coverage-verification procedure; §9.7 states the coverage walk is live-state-only. §9.6 reads as residue from a superseded model of coverage. No verdict diverges, because no requirement attaches consequences to an enumerated prior generation — but a verifier implementer reading §9.6 will build a backward scan the rest of the document has no use for, and will do so on payload bytes that §9.6 itself warns can mimic trailers.

### CONTRADICTION 2 — §21.5 row R10 vs §21.6, same condition in both tables

- §21.5, row **R10**: "An unknown record type carries MU = 0 | … | reader | open (top-level); layer access (sub-record) | `[R-CNT-15]` (R-CNT-18)" — inside the register that §21.1 introduces as enumerating "every violation this specification names", whose "completeness is normative".
- §21.6, "Conditions that are **not** violations. These are defined behaviors, not errors": "An unknown record type carries MU = 0 | Ignored, and preserved or dropped per its PE bit | `[R-CNT-15]`, `[R-WRT-08]`".

Byte-identical condition, opposite classifications. `[R-CNT-15]` resolves it in favor of §21.6 for the experimental range ("a record type from the experimental range is conforming"), so I do not score it byte-level — but the resolution requires declaring an R-row of the normatively-complete register mis-filed, and it undermines Appendix H's summary rule that a conforming file is one to which "no violation row of §21.2–§21.5 applies" (which §24 `[R-VEC-02]` also contradicts: "a conforming file can carry a record a reader ignores (§21.5, §21.6)").

### OBSERVATION — §9.7's walk omits the front block and the trailer while calling unreached bytes dead

`[R-LIF-08]` enumerates "the live directory and its records, each record's extent, each layer's tile-index region and that region's non-sentinel entries, and the declared padding §5.2 defines", then says "Bytes the walk does not reach are dead space". The front signature block and the live trailer appear in neither list, yet §5.2 puts both squarely in the live committed state. Read literally, every file — including Appendix A's minimal 128-byte one — reports 80 dead bytes instead of 0. §5.2's explicit enumeration resolves it, so this is not byte-level, but the walk's clause list should name both bookends.

### OBSERVATION — `[R-COD-11]`'s "§9.7(d)" is a dangling cross-reference

§17.4: "MUST NOT certify the file — the rule of §9.7(d) applied to content." §9.7 is a single paragraph plus a Note; it has no lettered clauses. The rule is stated in full in the sentence itself, so nothing is lost, but the pointer resolves to nothing.

### OBSERVATION — register omissions, against §21.1's own completeness claim

§21.1 makes the register's completeness normative ("a violation this specification names and the register omits is a defect in this document"), and `[R-ERR-02]`/`[R-VEC-03]` tie the conformance corpus to it row by row. Three named violations have no row in §21.2–§21.5:

1. `[R-CNT-15]`: "a verifier MUST treat a reserved-range record type as a validity error at the record's governing scope" — reject-file at top level, reject-layer as a sub-record. **F37** covers only *unassigned type with MU = 1, reader-detected*; **R10** covers only the reader's ignore outcome. No row carries the verifier's reserved-range check, so the corpus will contain no vector for it.
2. `[R-CNT-22]`: a registered type whose stored MU/PE bits differ from §7.3's fixed values — "makes the file nonconforming", verifier SHOULD report. Filed in §21.6 under "not violations", where the cell itself says "The file is nonconforming".
3. `[R-MTA-05]`: unsorted user-metadata object members — "the file is nonconforming, a verifier MUST report it". Also filed in §21.6 under "not violations", with the same self-contradicting cell.

Items 2 and 3 give §21.6 two rows that assert the file is nonconforming inside a table whose heading says these are not violations — which is what makes the second reading of BYTE-LEVEL AMBIGUITY 2 live.

### OBSERVATION — §21.3 skips L40 with no retirement note

Rows run L1–L39, then L41–L48; the stated count of 47 is consistent with the omission, so it is deliberate. But §2.2's retirement discipline (and the explicit precedent set for withdrawn `[R-SER-04]` in §14.4's Note) suggests the gap should be annotated, or the corpus tooling will read it as a transcription loss.

### OBSERVATION — `[R-SLB-05]`'s "writer defect" has no outcome, detector, or row

"a commit that produces dead space it did not supersede is a writer defect (`[R-CNT-02]`, `[R-LIF-02]`)". `[R-CNT-02]`'s predicate is over the live state only, so freshly-created dead space breaks no partition; **F8** covers only live bytes in no class; and no register row names the condition. §22.3 confirms the intent — coverage "makes everything else *countable* rather than absent … the number that distinguishes a working file from a padded one" — so a padded file is conforming and merely reported. The phrase "writer defect" carries no conformance consequence and should not be read as one.

### OBSERVATION — L43's cross-generation phrasing is reducible

L43 ("A new generation carries a slab declaration forward although the commit changed an affected run's stored-tile set or byte placement…") reads as requiring history, which §9.7's live-state-only walk forbids. `[R-SLB-04]` reduces it correctly — "detected as the invariant failures of `[R-SLB-03]` are: by a verifier" — so it collapses into L41/L42 over the live index. No divergence, but the row's phrasing invites a verifier author to attempt generation reconstruction.

### OBSERVATION — arithmetic and constants check out

Every worked example I could evaluate is correct: §11.2/§11.4's ordinals (s = 10, in-tile 11,452, planar disk ordinal 74), §15.4's segmentation (16 segments, segment 15 at [19,660,800, 20,000,000), entry at relative byte 339,180), §15.4's second example (entry 74 at [1,480, 1,500); channel-3 block = entries 96–127), §14.2's offsets (Q = 3 → bytes [15,18); Q = 5 → [25,30)), §14.3's packing (`55 01` / `55 FD`), §14.5's edge tile (32 bytes, values 1–15 = `CD AB`), §17.3's shuffle (`00 00 00 00 00 00 80 00 40 3F 40 40`), and §12.1's bfloat16 (`0x3F80` → bytes `80 3F`). All four fixed CRC constants and §21.8's instance count reproduce exactly.

---

## Verdict

**IMPLEMENTABLE: qualified**

A conforming verifier is buildable from this document alone: the check set, its dependency order, the outcome class and scope of each check, and the split between reader-detected and verifier-detected conditions are all stated with unusual precision, and every constant and worked example I could evaluate is exact. Two gaps block a *deterministic* verdict. BYTE-LEVEL AMBIGUITY 1 makes a routine append pattern — a per-tile-aligned or slab-aligned layer added after an earlier generation — either conforming or unrepairably reject-file depending on where the declared-padding run is taken to begin; a one-clause fix ("the run begins no earlier than the end of the previous generation's committed length" or, equivalently, "dead bytes are never declared padding") closes it. BYTE-LEVEL AMBIGUITY 2 leaves certification of a file whose metadata a verifier declined to decode undefined, where the codec case has an explicit rule; extending `[R-COD-11]`'s form to §18 closes it. Both are additions of a sentence, not redesigns.

**BYTE-LEVEL AMBIGUITIES: 2**

**CONFIDENCE: high**
