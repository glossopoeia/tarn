# TARN Format Specification — Acceptance Review

**Charter: VERIFIER.** Sole source: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read in full (3172 lines). No other file, repository, or external source was consulted. Every conclusion below cites section numbers and requirement identifiers from that text.

Two computations were performed locally in a scratchpad, using only parameters stated in the document, to check byte-level constants against their claimed values (§4.5, §15.4, Appendix A). They are reported in §5 below; no other information entered the review.

---

## 1. The certification procedure

A verifier is a reader that additionally checks every file-level requirement, including those ordinary readers are exempted from, and certifies conformance `[R-CNF-11]`. It inherits every reader obligation, including the ordering rules `[R-ENC-05]` (allocate/seek/fetch nothing before the covering checksum verifies) and `[R-ENC-10]` (verify before acting). Certification is total and binary: a file is conforming only if it satisfies every requirement at every scope, and outcome classes describe blast radius for readers, never degrees of file conformance `[R-CNF-12]`. A verifier therefore runs every check below to completion — it may not stop at the first reject-layer and call the remainder unexamined.

Three verdicts are possible and must be kept distinct:

| Verdict | Meaning | Authority |
|---|---|---|
| **certified** | no violation at any scope | `[R-CNF-12]` |
| **nonconforming** | at least one violation, reported with its outcome class and scope | §21.2–§21.5 |
| **cannot establish** | the verifier lacks a capability (codec, resource budget, format major) — a statement about the verifier, not the bytes | `[R-COD-11]`, `[R-ERR-04]`, `[R-CNT-07]`, §9.7(d) |

The last is load-bearing: `[R-ERR-04]` requires a resource refusal be reported *as* a limit and never as a validity error, and §21.6's closing paragraph makes the same point for an unimplemented format major.

### Phase P0 — Preconditions

| # | Check | Outcome | Scope | Rule / row |
|---|---|---|---|---|
| P0.1 | Obtain transport-authoritative size (full-response length, complete range length, or size probe). Never substitute `committed_file_length`. | cannot establish if unobtainable | — | `[R-CNT-10]` |
| P0.2 | size ≥ 128 and size mod 64 = 0 | reject-file | file | `[R-CNT-01]`; F8, F19 |

The 128-byte floor is derivable rather than stated normatively: `[R-CNT-06]` forces dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64, and F ≡ 0 (mod 64); the minimum satisfying all four is 84 rounded up to 128. §5.1's statement of it sits inside an *Example*, which §2.1 makes non-normative. (Observation O8.)

### Phase P1 — Front signature block

| # | Check | Outcome | Scope | Rule / row |
|---|---|---|---|---|
| P1.1 | Bytes [0,16) byte-identical to `89 54 41 52 4E 0D 0A 1A` + 8 zeros | reject-file | file | `[R-CNT-04]`; F11, F2 |

`[R-CNT-04]` lets a *remote* reader defer or omit this. A verifier may not: `[R-CNF-11]` obliges it to check every file-level requirement, and "writers MUST emit exactly these 16 bytes" is a file-level requirement. Transport is not an exemption for certification.

### Phase P2 — Live trailer (fixed order, `[R-CNT-06]`)

The order is normative because only the first three gates touch fields whose positions are fixed across all majors `[R-CNT-24]`.

| # | Check | Outcome | Row |
|---|---|---|---|
| P2.1 | magic at F−64 = `8A 4E 52 41 54 0D 0A 1A` | reject-file | F14, F2 |
| P2.2 | u32 at F−4 = CRC-32C over [F−64, F−4) | reject-file | F20 |
| P2.3 | version_major ≠ 0 | reject-file | F24 |
| P2.4 | version_major implemented | *cannot establish* (not a defect) | F25 |
| P2.5 | incompat lane bits 0–15 all implemented (this text: all clear) | reject-file | F26 |
| P2.6 | committed_file_length = size, ≡ 0 (mod 64) | reject-file | F23, F19 |
| P2.7 | dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64, sum non-wrapping | reject-file | F15, F22, F16, F4 |
| P2.8 | generation ≥ 1; file_id ≠ 0; reserved [56,60) zero | reject-file | F17, F18, F21 |
| P2.9 | every u64 ≤ 2⁶³ − 1 | reject-file | F3 (`[R-ENC-03]`) |

Ignore-lane bits 16–31 are ignored and are *not* a conformance violation `[R-CNT-08]`; §21.6 records this. Nothing from P2.6 onward may be acted on before P2.2 passes.

### Phase P3 — Directory region and pre-trailer pad

| # | Check | Outcome | Detector | Row |
|---|---|---|---|---|
| P3.1 | F − 64 − (dir_offset + dir_length) < 64 | reject-file | verifier | F13 (`[R-CNT-05]`) |
| P3.2 | that gap is all zero and holds no structure | reject-file | verifier | F12, F10 (`[R-CNT-03]`) |
| P3.3 | final 4 bytes of the region = CRC-32C of the preceding dir_length − 4 bytes, **before any parse** | reject-file | reader | F27 (`[R-CNT-11]`) |

P3.1/P3.2 are exactly the checks `[R-CNT-05]` exempts ordinary readers from; a reader's only directory-placement check is the bounds rule of `[R-CNT-06]`.

### Phase P4 — Live record walk (file scope)

The directory is always raw — no codec on the open path `[R-CNT-25]`.

| # | Check | Outcome | Detector | Row |
|---|---|---|---|---|
| P4.1 | each 24-byte header and its inline_length lie inside the sequence | reject-file | reader | F32 |
| P4.2 | type ≠ 0 | reject-file | reader | F29 |
| P4.3 | reserved flag bits 2–15 zero | reject-file | **verifier** | F31 |
| P4.4 | not MU=1 ∧ PE=0 | reject-file | **verifier** | F30 |
| P4.5 | ≤ 1 top-level user-metadata record | reject-file | reader | F37 |
| P4.6 | unknown type with MU=1 | reject-file | reader | F38 |
| P4.7 | unknown type with MU=0 | ignore-record (conforming) | reader | R10, §21.6 |
| P4.8 | non-layer extent slots: not half-zero, offset ≥ 16, offset+length ≤ F−64, non-wrapping, domain-valid | reject-file | reader | F33, F34, F35, F3, F4 |
| P4.9 | user-metadata record extent ≠ (0,0) | reject-file | reader | F28 |
| P4.10 | user-metadata inline_length = 1 | reject-file (containing scope) | reader | `[R-MTA-03]` — **no register row** |
| P4.11 | each layer record's name: well-formed UTF-8, non-empty, ≤ 255 bytes, no U+0000–U+001F | reject-layer, detected at open | reader | L4, L6, L7 |
| P4.12 | no two layer names byte-identical (raw bytes, no normalization) | reject-file | reader | F7 |
| P4.13 | registered types carry the registry's fixed MU/PE | report; blocks certification | verifier | `[R-CNT-22]` — **partially unrowed** |

P4.10 and P4.13 are checks the register does not carry as rows; see Findings.

### Phase P5 — Per-layer record validation (§19.3 `[R-RDR-03]`)

All decidable from the resident directory and F; no I/O. Outcome reject-layer throughout except where noted. A verifier runs this for **every** layer, not only layers it is asked about — §19.2's reliance-based timing bounds a *reader*, and certification relies on everything.

- Exact parse: fixed fields, d dimension entries, C channel entries, trailing fixed fields, then zero or more complete sub-records with no residue `[R-CNT-18]` — L22, L13, L3.
- Sub-records: type ≠ 0 (L12), no nesting beyond two (L23), unknown MU=1 → reject-layer (L24), a layer record nested as a sub-record (L25), ≤ 1 user-metadata sub-record (L18), sub-record extent ≠ (0,0) (L11).
- Extent slots (layer record and sub-records): half-zero (L14), offset < 16 (L15), reaching F−64 (L16), domain (L1), sums (L2).
- Names: UTF-8 (L5), non-empty and C0-free (L8, L9), unique within layer (L10).
- Value sets: layout ∈ {1,2} (L35), linearization = 1 (L32), codec ∈ 1…4 (L44), filter ∈ {1,2} (L46), index_encoding = 1 (L30), channel type ∈ 1…13 (L33).
- Fill: length prefix = element size (L29); bool fill ∈ {0x00, 0x01} (L34).
- Layout declarations: A ≠ 0 ∧ S ≠ 0 (L19), A a power of two in 512…2⁶² (L38), A_slab = 0 when S = 0 (L27), A_slab a power of two in 1…2⁶² when S ≠ 0 (L28).
- Geometry: d ≥ 1, C ≥ 1, every Tᵢ ≥ 1 (L31); Gᵢ = ⌈Eᵢ/Tᵢ⌉ computed as Eᵢ/Tᵢ + [Eᵢ mod Tᵢ ≠ 0] to avoid the overflow of the (E+T−1)/T idiom (§11.2's note); every derived product ≤ 2⁶³ − 1 (L2).
- Index cross-checks: entry_count = N (interleaved) or C·N (planar) (L20); extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4, and (0,0) iff entry_count = 0 (L21); nonzero crc_of_crc_array with entry_count = 0 (L26).
- Codec bound: codec 4 with per-tile decoded size > 0x7E000000 (L45).

Only two of these produce a *file*-scope outcome: a duplicate layer name (F7, by `[R-ENC-15]`) and — for the layer record's own header flags — nothing, because L47/L48 keep header-flag defects at layer scope even though the layer record is a top-level record. That asymmetry against F30/F31 is deliberate and follows "the scope the record governs" `[R-CNT-13]`.

### Phase P6 — Per-layer tile index

Dependency-ordered by §8.2's chain: crc_of_crc_array → segment CRC array → segment → entry.

| # | Check | Outcome | Detector | Row |
|---|---|---|---|---|
| P6.1 | crc_of_crc_array over the segment-CRC array as stored | reject-layer | reader | L36 |
| P6.2 | **every** segment CRC over entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)); partial segments cover only their actual bytes; comparison of computed CRCs, never matching against `0xEECB3BB2` | reject-layer | reader | L37 (`[R-IDX-05]`) |
| P6.3 | classify every entry per §15.3: sentinel with crc ≠ 0 (T6); exactly one half = S (T7); offset < 16 (T8); extent past F−64 (T9); length 0 (T10); field > 2⁶³−1 (T11); sum > 2⁶³−1 (T12) | reject-tile | reader | T6–T12 |
| P6.4 | A declared: every stored offset mod A = 0 | reject-layer | **verifier** | L39 |
| P6.5 | S declared: within each run, stored tiles packed in ordinal order, sentinels transparent; run's first stored offset mod A_slab = 0; runs partitioned per channel block for planar | reject-layer | **verifier** | L41, L42 |
| P6.6 | stale slab declaration carried forward | reject-layer | **verifier** | L43 (not independently testable — see audit) |
| P6.7 | intra-layer overlap (stored extents against each other, against the index region, against sub-record extents) | reject-layer | **verifier** | L17 |
| P6.8 | any overlap crossing layers or touching another scope's structures | reject-file | **verifier** | F36 |

Note the sentinel is a reserved pattern, not an offset: `[R-ENC-03]`'s domain rule and `[R-ENC-04]`'s sum rule apply to non-sentinel entries only `[R-IDX-02]`, and an entry classified reject-tile contributes no extent to the verifier overlap rows `[R-IDX-03]`.

### Phase P7 — Per-stored-tile payload and decoded content

| # | Check | Outcome | Detector | Row |
|---|---|---|---|---|
| P7.1 | codec 1: entry length = decoded size (pre-fetch, from declarations alone) | reject-tile | reader | T14 |
| P7.2 | fetch [offset, offset+length); stored bytes match the entry's crc — **before decoding** | reject-tile | reader | T1 |
| P7.3 | codec 2: raw RFC 1951, no zlib/gzip wrapper (T15); no second stream after BFINAL (T16) | reject-tile | reader | T15, T16 |
| P7.4 | codec 3: frame magic `28 B5 2F FD` (T17); exactly one frame, no skippable frames before/after/between (T18); Dictionary_ID = 0 (T19); Content_Checksum_flag clear (T20); Window_Size ≤ decoded size (T21); Frame_Content_Size, if present, = decoded size (T22) — and never an allocation source | reject-tile | reader | T17–T22 |
| P7.5 | codec 4: raw LZ4 block, not an LZ4 frame (T23) | reject-tile | reader | T23 |
| P7.6 | decode consumes the extent exactly (T24); stream well-formed (T25); independently decodable, no external history or side data (T13) | reject-tile | reader | T24, T25, T13 |
| P7.7 | decoded length = decoded size from declarations: P·Q interleaved, P·Bᶜ planar numeric, ⌈P/8⌉ packed planar bool | reject-tile | reader | T3 |
| P7.8 | apply the filter inverse at the mandated stride (element size planar, Q interleaved, identity for a packed bool plane) | — | — | `[R-COD-10]` |
| P7.9 | every padding position encodes that channel's recorded fill | reject-tile | **verifier** | T4 |
| P7.10 | every pad bit of a packed plane (P mod 8 ≠ 0) carries the fill bit | reject-tile | **verifier** | T5 |
| P7.11 | every interleaved bool byte at a real position ∈ {0x00, 0x01} | reject-tile | **verifier** | T2 |
| P7.12 | mis-strided filter, where P7.9–P7.11 expose it | reject-tile | **verifier** | T26 |

If the verifier cannot execute the layer's codec or filter it MUST NOT certify — §9.7(d)'s rule applied to content `[R-COD-11]`.

### Phase P8 — Record extents (user metadata)

Quarantined: *every* way the document can be unreadable is ignore-record with a SHOULD-report, whatever the containing scope `[R-CNT-25]`, `[R-MTA-02]`. A malformed *slot* is not quarantined — it precedes the document and takes the containing scope (P4.8/P4.9, F28/L11).

R2 (extent CRC) → R1 (encoding ∈ {1,2}) → R3 (decode; encoding 2 = one RFC 8878 frame, magic, no skippable/second frame, no dictionary ID, no content checksum, decoded under a bound ≥ 16 MiB per `[R-MTA-09]` and §21.9) → R6 (JSON, object at top level, no BOM) → R4 (UTF-8) → R5, R9 (key rules) → R7 (finite binary64 numbers; bare `NaN`/`Infinity`/`-Infinity` excluded) → R8 (no duplicate keys within an object).

Then three checks with **no register row**: member ordering by key UTF-8 bytes (`[R-MTA-05]`, "a verifier MUST report it"); `tarn.`-prefixed keys not registered (`[R-MTA-06]`); standardized keys outside their listed scope or of the wrong shape (`[R-MTA-07]`).

### Phase P9 — Byte coverage and multi-generation attribution (§9.7 `[R-LIF-08]`)

The only phase that touches superseded bytes.

**(a) Candidate enumeration.** Probe backward at 64-aligned offsets o from F−64 to 0 for the trailer magic. A candidate qualifies iff its CRC verifies, `committed_file_length` = o + 64, `[R-CNT-06]`'s field validity holds against its own F_k, and its file_id equals the live file_id. (F45's instance list enumerates exactly these gates.)

**(b) Chain selection.** Anchored at the live trailer: exactly one candidate per generation number from g down to 1, committed_file_lengths strictly increasing and each equal to its offset + 64. Off-chain candidates are discarded as payload mimics. No chain → reject-file (F43, F45).

**(c) Attribution.** Generation k owns [F_{k−1}, F_k), F₀ = 16.

**(d) Claim sets.** For each k: structures referenced transitively from generation k's directory (extent slots, tile-index regions, index entries) **that lie within k's range**, plus that directory, its declared padding, and its trailer. Every byte of the range must be claimed exactly once (F9, F41, F44), except that a double claim inside one layer is L17 (certification fails either way).

**(e) Depth.** For every enumerated generation the verifier must be able to verify its trailer, directory, tile index, and every structure those claim — stored-tile extents and record extents included (F42). Failure to verify any of them is "cannot establish coverage" and the file is nonconforming §9.7(d).

**(f) Per-generation padding.** F10's instances name "each generation's pre-trailer pad" and the alignment/slab gaps — so declared padding of superseded generations must also be zero, and F12/F13's gap bound applies per generation.

---

## 2. (a) What a verifier cannot establish

**Content.** §21.7 `[R-ERR-01]` states it plainly: the format detects corruption of *structure*, not incorrectness of *content*. A writer that emits well-formed structures carrying wrong sample values produces a file every checksum in §8 certifies. Three named cases: a mis-strided byte-shuffle where no padding position or bool byte exposes it `[R-COD-10]`; an undisclosed zstd dictionary, which "need not decode to an error" `[R-COD-06]`; and simply wrong data. The narrow exceptions are structurally constrained content — padding positions, pad bits, interleaved bool bytes (§14.5, `[R-SER-08]`).

**Authenticity.** Checksums do not authenticate; an adversary who can modify bytes recomputes them `[R-SEC-07]`, §4.5. A certificate asserts internal consistency and nothing about provenance. Detached signatures over the committed prefix are the composition the format offers, and they attest the generation they name, not the file a later reader opens.

**Rollback.** Truncation of a file to an earlier commit boundary is *indistinguishable in-format* from that earlier version `[R-LIF-06]`. A verifier presented with generation 3 cannot tell whether generations 4 and 5 ever existed. Rollback detection requires out-of-band state — an expected generation number or a detached hash.

**Durability.** `[R-LIF-02]` steps 4 and 6 require storage barriers. Barriers leave no byte trace; a verifier cannot distinguish a properly barriered commit from a lucky one. §9.2's note is honest about the consequence: weak barriers degrade "torn commits are invisible" to "torn commits are detected".

**Updater conformance.** §20.4's preservation obligations are intent-relative: an updater must re-emit byte-identically "every record it retains and does not logically modify" `[R-WRT-05]`. A verifier can see that generation k's directory differs from k−1's, but cannot know which differences were logical modifications. Even the crisp case — a PE = 1 record present in generation k−1 and absent in k — is an *updater*-class violation `[R-CNF-06]`, not a file-level one; the resulting file is a perfectly good state. Only file conformance is certifiable; §2.3's other three classes have no certification procedure.

**Anything depending on writer context.** Two rules make conformance turn on facts not present in the bytes: `[R-MTA-06]` prohibits a `tarn.`-prefixed key "this specification's registry does not define **at the version they target**", and `[R-EXT-03]` prohibits experimental values "**in released software or published data**". Given `tarn.foo`, a verifier cannot decide whether a later minor registered it (conforming — §18.3 says so explicitly) or the writer invented it (nonconforming). version_minor does not settle it, because emitting the correct floor is only a SHOULD `[R-CNT-26]`. See Contradiction C2.

**Files it cannot process.** An unimplemented format major (`[R-CNT-07]`; §21.6's closing paragraph insists the diagnostic distinguish capability from defect); an unimplemented codec or filter `[R-COD-11]`; a file above its own resource budget, which `[R-ERR-04]` requires be reported as a limit, never as corruption. All three are "cannot establish", not "nonconforming".

**Freshness.** §9.5's note: on shared storage a file being appended to may present a transiently invalid tail. A verifier's verdict is about the snapshot it read.

**Meaning.** Dead space is locatable but not judgeable — `[R-SEC-03]` says coverage "makes smuggled bytes locatable, not absent", and a superseded generation's extents "can hold anything". `tarn.stats` may be stale by design `[R-MTA-08]`. Nothing establishes that a file is the file you wanted, or that file_id is unique `[R-PRV-04]`.

---

## 3. (b) Walk-through: two generations, second supersedes one tile

**Construction.** Two layers, both interleaved, codec 1 (none), filter 1 (none), linearization 1, no alignment, no slab.

- Layer `a`: rank 1, dim `x`, E = 4, T = 2 → G = 2, N = 2, P = 2. One channel `v`, uint8, fill 0x00. Decoded size 2 bytes/tile. entry_count = 2; index region = 2 × 20 + ⌈2/2¹⁶⌉ × 4 = **44 bytes** `[R-CNT-17]`.
- Layer `b`: rank 1, dim `x`, E = 3, T = 3 → G = 1, N = 1, P = 3. One channel `w`, uint8, fill 0xFF. Decoded size 3 bytes. entry_count = 1; index region = 20 + 4 = **24 bytes**.

Each layer record's inline payload, packed in §7.4's table order with no padding: name (2) + layout (1) + linearization (2) + codec (2) + filter (2) + A (8) + S (8) + A_slab (8) + d (1) + C (2) + one dimension entry (2 + 8 + 8 = 18) + one channel entry (2 + 2 + 2 = 6) + index_encoding (1) + entry_count (8) + crc_of_crc_array (4) = **73 bytes**; with the 24-byte header, 97 bytes per record. Directory = 2 × 97 + 4 = **198 bytes**.

Generation 1 ends at F₁ = 384; generation 2 supersedes layer `a`'s tile 1 and ends at F₂ = 704. Both are multiples of 64 `[R-CNT-06]`; both pre-trailer pads are under 64 bytes `[R-CNT-05]`.

**Every byte, classified.** Four independent attributes: coverage class (§5.2), owning generation (§9.7(b) — the commit that appended it), liveness (`[R-CNT-21]` — reachability from the live trailer), and the actor obliged to check it.

| Range | Bytes | Coverage class §5.2 | Gen | Live? | Checked by |
|---|---|---|---|---|---|
| [0, 16) | 16 | front signature block | none (F₀ = 16) | live | reader P1 (equality), verifier P9(d) |
| [16, 18) | 2 | stored-tile extent (`a` tile 0) | 1 | **live** — gen 2's re-emitted entry 0 still points here | reader T1 + verifier T4/T2 |
| [18, 20) | 2 | stored-tile extent (`a` tile 1, old) | 1 | **dead** | verifier only, via gen 1's index entry crc (F42) |
| [20, 23) | 3 | stored-tile extent (`b` tile 0) | 1 | **live** | reader T1 + verifier T4 |
| [23, 67) | 44 | tile-index region (`a`, gen 1) | 1 | **dead** | verifier: crc_of_crc_array + segment CRC from gen 1's layer record (F42) |
| [67, 91) | 24 | tile-index region (`b`) | 1 | **live** | reader P6.1/P6.2 |
| [91, 289) | 198 | directory (gen 1) | 1 | **dead** | verifier: directory CRC (F42), record walk to build gen 1's claim set |
| [289, 320) | 31 | declared padding (gen 1 pre-trailer pad) | 1 | unreachable | verifier: zero (F10), gap < 64 (F13), nothing else in it (F12) |
| [320, 384) | 64 | trailer (gen 1) | 1 | **dead** | verifier: qualifying candidate, `[R-CNT-06]` against F₁ = 384 (F45) |
| [384, 386) | 2 | stored-tile extent (`a` tile 1, new) | 2 | **live** | reader T1 + verifier T4/T2 |
| [386, 430) | 44 | tile-index region (`a`, gen 2) | 2 | **live** | reader P6.1/P6.2, verifier P6.7 |
| [430, 628) | 198 | directory (gen 2) | 2 | **live** | reader P3.3/P4 |
| [628, 640) | 12 | declared padding (gen 2 pre-trailer pad) | 2 | live-state padding | verifier F10/F12/F13 |
| [640, 704) | 64 | trailer (live) | 2 | **live** | reader P2 |

**Attribution check.** Generation 1's range is [16, 384). Its claim set: the three stored-tile extents [16,23), both index regions [23,91), its directory [91,289), its padding [289,320), its trailer [320,384) — exactly 368 bytes, each claimed once. Generation 2's range is [384, 704). Its directory references `a` tile 0 at [16,18), `b`'s tile at [20,23), and `b`'s index at [67,91) — all **outside** its range, so all remain claimed by generation 1 and are *not* double-claimed. §9.7's in-range restriction is precisely what makes this decidable, and the note after `[R-LIF-08]` says so. Generation 2's own claim set is [384,430) ∪ [430,628) ∪ [628,640) ∪ [640,704) = 320 bytes, each claimed once. Coverage holds.

**Live vs. attributed are orthogonal.** Five of the file's live structures were appended by generation 1 (the front block plus [16,18), [20,23), [67,91)); five ranges appended by generation 1 are dead ([18,20), [23,67), [91,289), [289,320), [320,384) = 339 bytes, 48% of the file). A verifier must not conflate the axes: dead space is still coverage-attributed and still checksum-verified (F42), and live bytes are not thereby attributed to the live generation.

**Two consequences worth naming.** First, certifying this file requires computing `crc_of_crc_array` over a *superseded* index using the *superseded* layer record's field — so the verifier parses generation 1's directory in full even though `[R-CNT-21]` forbids readers from interpreting it. Second, [289,320) is 31 bytes covered by no checksum anywhere (§8.1 lists no entry for padding); its only protection is the verifier's zero check `[R-CNT-03]`, which `[R-SEC-04]` states rather than defends.

---

## 4. (c) Audit of §21's register against this procedure

### Direction 1 — checks I run that have no row

| Check | Rule | Status |
|---|---|---|
| User-metadata object members not sorted by key UTF-8 bytes | `[R-MTA-05]` — "the file is nonconforming, a verifier MUST report it" | **No row in §21.2–§21.5.** Appears only in §21.6 as a non-violation. By §21.1's own completeness standard ("a violation this specification names and the register omits is a defect in this document") this is a self-declared defect. See Contradiction C1. |
| Registered record type whose stored MU/PE differs from §7.3's fixed values, other than MU=1∧PE=0 | `[R-CNT-22]` | **Partial gap.** F30/L47 cover MU=1∧PE=0 and F31/L48 the reserved bits. A layer record (registry: MU=1, PE=1) stored with **MU=0**, or a user-metadata record (registry: MU=0, PE=1) stored with **MU=1, PE=1**, matches no row, yet `[R-CNT-22]` says the file is nonconforming. |
| `tarn.`-prefixed key the registry does not define | `[R-MTA-06]` | **No row.** And undecidable from bytes (§2 above). |
| Standardized key outside its listed scope, or whose value does not match its row's shape | `[R-MTA-07]` — "A writer MUST NOT emit a standardized key outside the scopes its row lists" | **No row**, and the shape predicate is only sketched (e.g. must `tarn.axes` have exactly d elements? §18.4 says "one object per dimension, in declared order" but assigns no outcome to a wrong count). |
| User-metadata record inline_length ≠ 1 | `[R-MTA-03]` — "a validity error at the record's containing scope" | **No row.** F28/L11 cover the (0,0) extent; nothing covers the inline payload's fixed size. |
| File carries an experimental value that readers tolerate (record type ≥ 0x8000 with MU=0; metadata encoding ≥ 0x80) | `[R-EXT-03]` — writers MUST NOT emit these in released software | **No row as a violation.** R1/R10 record the *reader* outcome (ignore-record), not the writer prohibition. Undecidable from bytes in any case. |

The remaining rows I would run all exist. Coverage of the checks that matter most for certification — F9/F41/F42/F43/F44/F45 (attribution), F36/L17 (overlap), F10/F12/F13 (padding), L39/L41/L42 (layout invariants), T2/T4/T5 (decoded content) — is complete and correctly assigned to the verifier.

### Direction 2 — rows I would test that correspond to no check I can perform

| Row | Problem |
|---|---|
| **F5, L3** ("a fixed structure places its fields at widths other than those the spec fixes, with total size unchanged") | Field width is not observable. Bytes are bytes: a trailer with version_major written as u32 = 1 and version_minor as u32 = 0 shifts every later field, and what a verifier detects is the *consequence* (F23, F20, F16). If the consequence is nil, so is the detection. F1 admits exactly this for endianness ("detectable only through that field's own value or range gate"); F5 and L3 carry no such caveat and cannot. |
| **F1, F2** (big-endian storage, byte-reversed signature) | Aliases. F1 reduces to F3/F17/F18/F19/F23/F24; F2 reduces to F11/F14. There is no byte pattern that means "this was stored big-endian" other than a value that fails its own gate. |
| **T13** (not independently decodable) | Both named instances — a deflate stream expecting a previous tile's history window, an lz4 match reaching before its own output start — surface only as decode failures, i.e. as T25. The condition as stated is not separately testable. |
| **T26** (filter applied at a wrong stride) | The row admits it: detectable only "where the resulting image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes". Even then, a verifier observes a T4/T5/T2 failure and cannot attribute it to stride. A layer with no padding positions and no bool channel makes it undetectable by construction (§21.7). |
| **L43** (stale slab declaration carried forward) | Reduces entirely to L41/L42 on the live generation — `[R-SLB-04]` says so ("detected as the invariant failures of `[R-SLB-03]` are: by a verifier"). If the invariants hold, nothing is stale; if they do not, L41/L42 fire. §21.8 demands a vector per instance (here two: S, A_slab), but no such vector can be distinguished from an L41/L42 vector. |
| **R1**'s "or one the reader does not implement" (from `[R-CNT-25]`) | Reader-relative, not a file property. The row's own text wisely avoids it; `[R-CNT-25]`'s prose does not. |

### Arithmetic audit of §21.8

§21.8 claims "126 conditions over 235 named instances". I counted both mechanically, per §21.1's rule that instances are semicolon-separated and a cell reading "—" is one instance:

- Rows: §21.2 = 43 (F1–F45 with F6 and F39 absent), §21.3 = 47 (L1–L48 with L40 absent), §21.4 = 26, §21.5 = 10. **Total 126.** ✓
- Instances: §21.2 = 91, §21.3 = 81, §21.4 = 43, §21.5 = 20. **Total 235.** ✓

The arithmetic closes exactly, which is meaningful evidence that the register was built rather than asserted. One cell only works by accident: T18's "a second concatenated compressed frame; a skippable frame (magic 0x184D2A5x) before; after; or between frames" reads as a positional list but must be counted as four instances for the total to close — so a corpus builder must produce four T18 vectors (second frame; skippable before; skippable after; skippable between). Recorded as O3.

Row-number gaps (F6, F39, L40) are unexplained. §2.2's retirement rule governs *requirement identifiers*, not register row numbers; a reader is left to infer that the same discipline applies. §14.4's note about withdrawn `[R-SER-04]` shows the document knows how to say this when it wants to.

---

## 5. Constants verified independently

Computed from the parameters stated in §4.5 alone (polynomial 0x1EDC6F41 reflected to 0x82F63B78, init 0xFFFFFFFF, final XOR 0xFFFFFFFF), not from a library:

| Claim | Where | Result |
|---|---|---|
| CRC-32C(`"123456789"`) = 0xE3069283 | §4.5 | **0xE3069283** ✓ |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | **0x00000000** ✓ |
| CRC-32C of a full all-sentinel segment (2¹⁶ × `FF×16 00×4` = 1,310,720 bytes) = 0xEECB3BB2 | `[R-IDX-05]`, Appendix B | **0xEECB3BB2** ✓ |
| Appendix A's trailer CRC over its bytes [0,60) = 0xE00938D2, stored `D2 38 09 E0` | Appendix A | **0xE00938D2**, little-endian `d2 38 09 e0` ✓ |

The Appendix A dump is also internally consistent: 128 bytes, directory at [16,20) holding the CRC of zero record bytes, pad [20,64) all zero, F ≡ 0 (mod 64).

I also re-derived the worked examples in §11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4, §16.2, §17.3, §20.3 and Appendix B's derived figures (2³² entries → 256 KiB CRC array; 2³⁶ → 4 MiB; one full segment = 1.25 MiB; 32-tile index = 644 bytes). All check out. This is the strongest single signal in the document: the numeric examples are load-bearing and they hold.

---

## Findings

### AMBIGUITY

**A1 — Chain selection when several chains exist. §9.7(a), `[R-LIF-08]`. BYTE-LEVEL.**
The text says the verifier "MUST accept a candidate set forming a **chain** … whenever at least one such set exists; candidates outside the selected chain are discarded as payload mimics, and only when *no* consistent chain exists is coverage verification a failure at file scope". It never says how *the selected chain* is selected when more than one qualifies, and steps (b)–(d) can succeed for one chain and fail for another.
*Readings:* (1) select any qualifying chain; if its attribution leaves bytes unclaimed, the file fails (F9). (2) search chains, and fail only if no chain yields a complete partition.
*Constructible discriminator:* a stored tile payload containing a byte string that satisfies P9(a) — trailer magic, valid CRC, `committed_file_length` = its own offset + 64, the live file_id, and a generation number in [1, g]. §9.6 and §22.3 both state that payloads can deliberately mimic trailers, so this is a file a conforming writer may emit. Under reading (1) a verifier that picks the mimic as generation 1 attributes [16, F_mimic) to generation 1 and leaves the real generation 1's directory, pad and trailer unclaimed → reject-file. Under reading (2) the file certifies. That makes conformance verifier-dependent, which `[R-CNF-02]` forbids ("File conformance is a pure predicate on bytes: it does not depend on any reader").
*Picked:* (2), because §21.6's row "A payload contains a byte string that mimics a trailer | Discarded as a mimic during generation enumeration; **never a failure**" can only be true under (2). But §21.1 makes the *rule* govern where a row diverges, and the rule as written does not require the search — so the register row is doing normative work `[R-LIF-08]` does not.
*Fix:* one sentence in §9.7(a) — "if more than one chain qualifies, the verifier MUST use a chain for which steps (b)–(d) succeed if any exists" — plus an acknowledgement of the search cost (O1).

**A2 — Validation depth for superseded generations. `[R-CNT-21]`, §9.7(c)–(d), `[R-CNF-02]`. BYTE-LEVEL.**
Do the requirements of §6–§18 bind structures that are no longer reachable from the live trailer?
*Readings:* (A) superseded generations are subject only to what §9.7 enumerates — `[R-CNT-06]` field validity for their trailers, checksum verification for their directories, indexes and claimed extents (F42), zero declared padding (F10), the gap bound (F12/F13), and the coverage partition. (B) every requirement binds every byte: a writer emitted those bytes, and writer prohibitions ("Writers MUST NOT emit a name that violates any of them" `[R-ENC-12]`) do not expire when a later commit supersedes them.
*Constructible discriminator:* generation 1 declares a layer whose channel name is empty (`[R-ENC-12]`, row L8); generation 2 drops that layer. Generation 1's directory CRC verifies, its index region is delimitable, and coverage closes. Reading (A) certifies; reading (B) rejects.
*Picked:* (A). The evidence is circumstantial but consistent: §19.2's detection tiers (open / layer access / tile use) are live-path tiers and every L-row and T-row is assigned to one of them; `[R-CNT-21]` says verifiers "classify" superseded structures rather than validate them; and §9.7(a) and F10 show the document being explicit exactly where it does want a superseded property checked. Under (B) a verifier would additionally have to decode every superseded tile under its own generation's declarations to run T2/T4/T5 — an obligation nothing in §21 states.
*Fix:* one sentence in §9.7 or `[R-CNT-21]` stating the closed list of properties superseded structures must satisfy, and that no other requirement binds them.

**A3 — Which inter-structure gaps are "declared padding". §16.1 `[R-SLB-01]`, §16.2 `[R-SLB-03]`, §5.2 `[R-CNT-02]`, §16 `[R-SLB-05]`. BYTE-LEVEL.**
Two connected questions.
(i) May a layer that declares neither alignment nor slab leave any gap between its structures? `[R-SLB-05]` says its tiles "MAY occupy any non-overlapping byte positions, in any order" — which reads as unconstrained placement — while `[R-CNT-02]` admits only three coverage classes and the declared-padding class is defined as "the alignment gaps of aligned or slab-declared layers … and each generation's pre-trailer pad". Composing them, an undeclared layer's structures must be **gaplessly packed** against their neighbours: any hole is claimed by no class and the file is nonconforming (F9). That is a significant writer obligation which §16's placement-freedom language actively conceals; I expect writers to get it wrong.
(ii) When A is declared, "unclaimed bytes that **this alignment leaves** between claimed structures are declared padding". Is a gap larger than A − 1 (a writer skipping an alignment slot) still declared padding? Reading (1): only gaps forced by alignment qualify, so a 2A-sized hole is unclaimed → reject-file. Reading (2): no size bound is stated, so any zero gap adjacent to the aligned layer's placement qualifies → conforming.
*Picked:* for (i), gapless packing; for (ii), reading (2) — `[R-CNF-04]` forbids a reader from inferring values this specification does not define, and §16.2's parallel wording for slabs ("unclaimed bytes that a writer's run placement leaves") carries no bound at all. Both took two passes and a cross-section derivation.
*Fix:* state in §5.2 that a structure gap is conforming only as declared padding, and in §16.1/§16.2 that declared padding is any zero-filled unclaimed span within an aligned or slab-declared layer's placement, with no size bound.

**A4 — Must a verifier decode a user-metadata document to certify? §18.2 `[R-MTA-03]`, `[R-MTA-09]`, §17.4 `[R-COD-11]`. Not byte-level.**
`[R-COD-11]` says a verifier that cannot execute a layer's codec or filter MUST NOT certify. Nothing extends that to §18.2's metadata encodings, and `[R-MTA-03]` explicitly tolerates "one the reader does not implement" as ignore-record. So a verifier that does not implement metadata encoding 2 could either (1) certify a file whose zstd-encoded document it never examined, having checked none of R3–R9 or `[R-MTA-05]`, or (2) report "cannot establish". *Picked:* (2), by §9.7(d)'s and §17.4's shared principle. Not byte-level: the conformance predicate on the file is unaffected — only the verifier's competence to decide it.

**A5 — Is a prior generation's declared padding "dead space"? `[R-CNT-21]`, §5.2. Not byte-level.**
`[R-CNT-21]` defines dead space as superseded *structures*, and §5.2 makes declared padding a class distinct from structures. Generation 1's pre-trailer pad in my walkthrough is therefore attributed, unreachable, and — literally — neither live nor dead space. §23.1's prose ("the superseded bytes remain in the file as dead space") assumes the looser reading. *Picked:* treat it as dead space for reporting; no check changes either way.

**Byte-level ambiguities: 3 (A1, A2, A3).** All three are acceptance-side — a verifier produces no bytes, so the operative divergence is that two conforming implementations of this charter would disagree about whether a specific, constructible byte sequence is a conforming file. Each conflicts with `[R-CNF-02]`'s promise that file conformance is a pure predicate on bytes, and each is closable by one sentence.

### CONTRADICTION

**C1 — §21.6's header contradicts three of its own rows, and §21.1's completeness claim contradicts both.**
§21.6 is titled "Conditions that are **not** violations" and opens: "These are defined behaviors, not errors. A reader that treats any of them as a failure is the nonconforming party." Three of its rows then say the opposite of their own section header:
- unsorted user-metadata members — "**The file is nonconforming**, but the document is readable" (`[R-MTA-05]`, whose own text adds "a verifier MUST report it");
- an unrecognized `tarn.` key — "**The file is nonconforming**, but a reader ignores that key";
- a registered type's stored MU/PE differing from the registry — "**The file is nonconforming**, but readers apply the type's fixed semantics" (`[R-CNT-22]`).
These cannot both hold. A condition that makes a file nonconforming is a violation; `[R-CNF-12]` says "a verifier certifies only violation-free files", so all three block certification — yet none appears as a row in §21.2–§21.5, and §21.1 declares the register's completeness normative and names an omitted violation "a defect in this document". Further, `[R-CNF-07]` requires every detectable violation to carry exactly one reader outcome, and these carry none (readers proceed unchanged).
*Effect on my procedure:* I check all three and refuse certification, but I cannot report an outcome class for any of them, which §24 `[R-VEC-02]` requires of every vector ("for each structure the file damages, the outcome class, the scope, and the §21 register row it exercises"). A vector for `[R-MTA-05]` is therefore unstateable in the terms §24 demands — which `[R-VEC-02]`'s last sentence says "makes it a finding against this document rather than a vector".
*Fix:* add a fourth register subsection for verifier-detected, reader-transparent violations (outcome: none; detector: verifier; blocks certification), and move these three rows into it.

**C2 — `[R-CNF-02]` (conformance is a pure predicate on bytes) contradicts `[R-MTA-06]` and `[R-EXT-03]` (conformance depends on writer context).**
`[R-CNF-02]`: "File conformance is a pure predicate on bytes: it does not depend on any reader, writer, or environment." But `[R-MTA-06]` prohibits a `tarn.`-prefixed key "this specification's registry does not define **at the version they target**" while simultaneously declaring that "A file carrying an unrecognized `tarn.` key is **conforming**" — and `[R-EXT-03]` prohibits experimental values "**in released software or published data**". Targeted version, release status, and publication are not properties of the byte sequence. Given a file with version_minor = 0 and a key `tarn.foo`, a verifier cannot decide between "a minor-3 writer emitted a minor-3 key and merely misstated the floor (a SHOULD, `[R-CNT-26]`)" and "a writer invented a reserved-namespace key". The three sentences cannot all hold.
*Fix:* make the predicate byte-local — e.g. an unrecognized `tarn.` key is conforming, full stop (matching §18.3's own conclusion and the ignore-lane flag precedent in `[R-CNT-08]`), and confine `[R-EXT-03]`'s release-context language to a non-normative note, with the byte-level rule being that a reserved-range value is nonconforming and an experimental-range value is conforming-but-rejected-at-its-scope.

### OBSERVATION

**O1 — Certification is a whole-file, whole-decode operation, and the register does not say so.** F42 requires checksum verification of every superseded generation's directory, index, and claimed extents, so certification reads 100% of the file including dead space — in my walkthrough, 48% of the bytes. T2/T4/T5 require decoding every live stored tile, so certification decodes the entire dataset while a reader decodes what it asks for. F36/L17 require interval-overlap detection over every extent of every generation; at §21.9's guaranteed floor of 2³² addressed tiles per layer, that is ≥ 2³² intervals, which forces an external-memory sort (an in-memory interval set at 16 bytes/interval is 64 GiB). And A1's chain search is potentially combinatorial in the number of trailer mimics a hostile file plants. All decidable; all disproportionately expensive, and none of it flagged. A short §21 note giving certification's cost class, and permitting a verifier to report "cannot establish" on resource grounds under `[R-ERR-04]`, would help.

**O2 — Seven rows are not independently performable** (F1, F2, F5, L3, T13, T26, L43); each is an alias for another row's detection or, in F5/L3's case, for a property that leaves no observable trace. §21.8 nonetheless requires a vector per instance — 2 + 2 + 2 + 1 + 2 + 3 + 2 = 14 vectors that will duplicate other rows' expectations. Marking such rows "detected via ⟨row⟩" would make the corpus honest about what it exercises.

**O3 — §21.8's instance arithmetic closes exactly at 126/235 (verified), but T18's cell is the one place where the "mechanical" count is counter-intuitive**: "a skippable frame … before; after; or between frames" must count as three instances, not one, for the total to reach 235. Worth rewording so a corpus builder does not undercount by two.

**O4 — Metadata encoding 2 (zstd) is optional for conforming readers; tile codec 3 (zstd) is mandatory.** `[R-CNF-03]` makes core status a §17 property; §18.2's encodings are outside it, and `[R-MTA-03]` explicitly tolerates "one the reader does not implement". A reader must therefore ship a zstd decoder anyway, and declining to use it for metadata is permitted but pointless. Worth a one-line note; it currently reads like an oversight.

**O5 — No field anywhere in format major 1 is classified *informative*.** §4.7 defines a three-way taxonomy and `[R-ENC-16]` states an obligation for informative fields, but every classified field in §6.1, §6.2, §7.2, §15.1 and §18.2 is structural or semantic. Relatedly, §7.4's layer-record table is the only structure table that gives neither byte offsets nor taxonomy class, contrary to §4.7's stated rubric — the packing rule in `[R-CNT-18]` covers the offsets, but the class column is simply absent, so a verifier auditing "informative fields never affect decoding" has nothing to audit.

**O6 — Updater conformance has no certification procedure**, though it is partly decidable from a multi-generation file (a PE = 1 record present in generation k−1 and absent in k is visible). §20's obligations bind the actor, not the file, so a verifier that notices such a drop has found nothing it may report as a file defect. Worth stating explicitly in §20.4 or §2.3 so implementers do not build the check and then not know what to do with it.

**O7 — §21.5 mixes conformance-blocking rows with a non-violation and gives no marker.** R1–R9 all trace to writer MUSTs and therefore block certification; R10 (unknown type with MU = 0) is conforming, as §21.6 and Appendix H both confirm. The register's columns cannot express the difference, so a verifier must reason row by row — and the natural shortcut ("register membership means violation", licensed by §21.1) gives the wrong answer for R10.

**O8 — The 128-byte minimum is normatively stated only in row F8.** §5.1 states it inside an Example, which §2.1 makes non-normative, and Appendix B is a finding aid. It is derivable from `[R-CNT-06]`'s gates, but `[R-CNT-01]` should say it outright — it is the single most-cited constant in any implementation's test suite.

**O9 — Register row-number gaps (F6, F39, L40) are unexplained.** §2.2's retirement rule governs requirement identifiers; nothing says register row numbers follow the same discipline. §14.4's note on withdrawn `[R-SER-04]` shows the document's own convention for saying so.

**O10 — A positive finding worth recording:** all four fixed byte-level constants reproduce exactly from the parameters the document states, and every worked numeric example I re-derived (§11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4, §16.2, §17.3, §20.3, Appendix A, Appendix B's derived figures) is correct. For a format whose entire contract is byte-level, this is the most important thing an acceptance review can confirm, and it holds.

---

## Verdict

IMPLEMENTABLE: qualified — I can build a conforming verifier from this text alone; the certification procedure above is complete and dependency-ordered, and every phase resolves to a cited requirement. The qualification is that three decisions (A1 chain selection, A2 superseded-generation depth, A3 gap classification) had to be made by inference, and two independent implementers may reasonably decide them differently, which means two conforming verifiers could disagree about specific files — the one property `[R-CNF-02]` promises cannot happen. All five gaps in §21's register (Direction 1) are checks I can perform but cannot report in the register's own vocabulary.

BYTE-LEVEL AMBIGUITIES: 3

CONFIDENCE: high
