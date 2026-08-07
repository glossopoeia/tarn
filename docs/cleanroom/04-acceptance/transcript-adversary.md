# TARN spec — adversarial read (§1–§24 + appendices)

**Source read:** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in full, and nothing else. Every claim below cites section numbers and requirement IDs from that text. Where I computed a checksum I implemented CRC-32C from §4.5's stated parameters only and validated it against §4.5's own check vector before trusting it.

**Charter:** build a file two competent verifiers disagree about, or a conforming file carrying bytes no rule accounts for. I succeeded once, in the coverage/declared-padding partition. Everything else I tried held, and I list the failed attacks because a failed attack against this document is a result.

---

## 1. The attack that succeeded: the declared-padding constructive test contradicts §16

§5.2 defines declared padding **constructively and exclusively** (`[R-CNT-02]`):

> A maximal run of bytes the live state does not otherwise claim is declared padding **when, and only when**, it is one of:
> - the run immediately preceding a structure whose offset a layer's alignment or slab declaration constrains (§16), **whose length is less than that declaration's modulus** — A for per-tile alignment, A_slab for a slab run — so that the run is **exactly the distance to the next legal offset**; or
> - the pre-trailer pad, of fewer than 64 bytes.

§16 then asserts the opposite as a flat fact, with no length qualification on the antecedent:

- §16.1 `[R-SLB-01]`: "the run of unclaimed bytes immediately preceding each such tile **is** declared padding — zero bytes, shorter than A".
- §16.2 `[R-SLB-03]`: "between runs, **placement freedom (`[R-SLB-05]`) governs**, and the run of unclaimed bytes immediately preceding each run's first stored tile **is** declared padding — zero bytes, shorter than A_slab".

§5.2 makes "is declared padding" a *conclusion* that a length test gates. §16 makes it a *premise*. They disagree exactly when the run is not the shortest legal one — which is not an exotic case: it is what any writer produces that skips an alignment slot, and, under `A_slab = 1`, it is what *every* gap between slab runs is, because "shorter than A_slab = 1" is unsatisfiable by a nonempty run.

The register takes §16's side without qualification. §21.2 **F9** — "A byte of declared padding is nonzero" — names its instances as "per-tile alignment gaps (16.1); slab run-placement gaps (16.2); the pre-trailer pad", detector *verifier*, outcome **reject-file**. A verifier built from the register checks every alignment/slab gap for zero. A verifier built from §5.2 first asks whether the run is short enough to *be* padding, and if it is not, classifies it as dead space — whose "content is unconstrained, and no conformance requirement applies to it" (`[R-CNT-21]`).

The asymmetry that convinces me this is an oversight rather than a subtlety I am missing: the spec *did* handle the analogous over-long-run case for the other padding class. **F12** exists — "The gap between the directory's end and the trailer start is 64 bytes or more, exceeding the sub-64-byte pre-trailer pad bound … verifier … `[R-CNT-05]`". There is no F- or L-row for "the gap preceding an aligned tile is A bytes or more". §21.1 makes the register's completeness normative, so under the §16 reading this is a violation the register omits — which §21.1 itself calls "a defect in this document". Under the §5.2 reading no violation exists and the bytes are dead space. There is no third text to break the tie.

### Discriminator D1 — slab, `A_slab = 1` (the tightest case)

A complete generation-1 file, 320 bytes. Layer `L`: rank 1, dimension `x` with E=4, T=1 (G=4, N=4); interleaved; C=1, channel `v` type 6 (uint8, element size 1), fill `00`; linearization 1; codec 1 (none); filter 1 (none); A = 0; **S = 2, A_slab = 1**; index_encoding 1; entry_count 4. Decoded size per tile = P·Q = 1 byte, so under `[R-COD-04]` every stored length is 1.

Runs partition [0,4) as run 0 = ordinals [0,2), run 1 = [2,4) (`[R-SLB-02]`).

| Range | Content |
|---|---|
| [0,16) | front signature block |
| [16,17), [17,18) | run 0: tiles 0 and 1, packed, first offset 16, 16 mod 1 = 0 ✓ |
| **[18,24)** | **6 unclaimed bytes; byte at offset 20 is `FF`, the rest zero** |
| [24,25), [25,26) | run 1: tiles 2 and 3, packed, first offset 24, 24 mod 1 = 0 ✓ |
| [26,110) | tile-index region: 4×20 + ⌈4/2¹⁶⌉×4 = 84 bytes ✓ `[R-CNT-17]` |
| [110,211) | directory: one 97-byte layer record + 4-byte CRC (dir_offset 110, dir_length 101) |
| [211,256) | pre-trailer pad, 45 zero bytes (< 64 ✓) |
| [256,320) | trailer; F = 320 (mod 64 = 0 ✓), dir_offset+dir_length = 211 ≤ F−64 ✓ |

Every rule outside §5.2/§16 is satisfied: extents own their bytes exactly once (`[R-CNT-13]`), each run is contiguous and ordinal-packed with an A_slab-aligned first tile (`[R-SLB-03]`), no invariant of §15.3 is touched.

- **Verifier A (§5.2 governs).** The run [18,24) is maximal and unclaimed and immediately precedes run 1's first stored tile, but its length 6 is *not* less than A_slab = 1, and 24 is not the next legal offset from 18 (with A_slab = 1 that is 18, distance 0). So it is **not** declared padding. It is therefore dead space, whose content is unconstrained (`[R-CNT-21]`). Verdict: **CERTIFY**; dead-space total **6**.
- **Verifier B (§16.2 + F9 govern).** The run immediately preceding a slab run's first stored tile *is* declared padding; declared padding MUST be zero and "a verifier MUST treat nonzero padding as a validity error at file scope" (`[R-CNT-03]`, F9). Verdict: **REJECT-FILE**; dead-space total **0**.

Same 320 bytes, opposite verdicts. Set offset 20 to `00` instead and the verdicts agree (certify) while the two mandated dead-space totals still differ, 6 versus 0 — `[R-CNT-21]` makes reporting that number a MUST.

The `A_slab = 1` variant is the sharpest because §16.2 *licenses the gap in the same sentence that forbids it*: "between runs, placement freedom governs" — and §16.2's own Note recommends `A_slab = 1` ("the right declaration for remote range coalescing with no direct-I/O alignment need"). Under A_slab = 1 no nonempty gap can satisfy "shorter than A_slab", so the recommended configuration cannot leave a legal gap at all under reading B, while reading A permits gaps of any content.

### Discriminator D2 — per-tile alignment, skipped slot

Same shape, one layer with **A = 512**, S = 0, two stored tiles of 100 bytes: tile 0 at **512** ([512,612)), tile 1 at **1536** ([1536,1636)). Both offsets are multiples of 512, so `[R-SLB-01]`'s stated invariant and register row **L39** are satisfied. The run [16,512) before tile 0 is 496 bytes — less than 512 and exactly the distance from 16 to the next legal offset — so it is declared padding under both readings and is zeroed. The run **[612,1536) is 924 bytes**, ≥ A, and 1536 is not the next legal offset from 612 (that is 1024). Put `FF` at offset 700.

- Verifier A: not declared padding under §5.2's "when, and only when" → dead space → **certify**, dead total 924.
- Verifier B: §16.1 says the run preceding an aligned stored tile is declared padding → F9 → **reject-file**, dead total 0.
- A third competent reading is available and reaches a *third* verdict: §16.1's "A verifier MUST check the invariant (violation: reject-layer, §15.3)" can be read to cover the whole sentence, including "shorter than A", making a ≥A run a **reject-layer** at L39's row rather than a file-scope failure.

D2 is what a slot-based writer emits routinely: reserve 8192 bytes per 4096-aligned tile slot, compress a tile to 1000 bytes, and the gap to the next slot is 7192 ≥ A.

### What I searched before reporting this

Every occurrence of "declared padding", "dead space", "maximal run", "next legal offset", "shorter than A", "placement freedom": §5.2 (`[R-CNT-02]`, `[R-CNT-03]`, `[R-CNT-21]`), §6.2 `[R-CNT-05]`, §9.7 `[R-LIF-08]`, §16 lead-in `[R-SLB-05]`, §16.1 `[R-SLB-01]`, §16.2 `[R-SLB-03]`, §20.2 `[R-WRT-02]`, §21.2 F9/F11/F12, §21.6's dead-space row, §22.3 `[R-SEC-03]`, Appendix G item 5, Appendix H's verifier checklist. §9.7 does not resolve it — its walk enumerates "**the declared padding §5.2 defines**", which is the term in dispute. `[R-SLB-05]` does not resolve it either: "a byte the live state neither claims nor accounts for as declared padding is dead space" is exactly the disputed classification restated. Nothing in the document states what an over-long gap before an aligned structure is.

---

## 2. Attacks that failed (the file held)

These are the interesting ones, with the sentence that refuted each.

**Ignored records' extents as unclaimed bytes.** I built a top-level record of experimental type 0x8001, MU=0, PE=0, whose extent overlaps a stored tile, betting that §2.4's "The record is skipped as though absent" would make the extent unreachable and therefore dead space (no overlap, certify) for one verifier and a live structure (F35, reject-file) for another. **Refuted by §5.2's parenthetical**: a structure includes "a record extent (the bytes any record's extent slot references, **whatever the record's type**, §7.2)". That phrase exists precisely to close this. ignore-record is a reader outcome; coverage "is checked by verifiers, never by readers" (§5.2's Note).

**Trailer mimicry in a live payload.** I placed a live stored tile over a prior generation's trailer bytes at a 64-aligned offset, so §9.6's backward probe lands on a valid-looking commit state inside the live state. **Refuted** by `[R-LIF-06]` ("recovery output MUST be re-verified as a whole file"), §21.6's "A payload contains a byte string that mimics a trailer → Inert", and `[R-SEC-04]`. Deliberately handled.

**Relocating the live directory into a prior generation's bytes.** Blocked by `[R-CNT-05]`/F11/F12: nothing but a sub-64-byte zero pad may lie between the directory's end and the trailer, so the live directory is pinned to the tail regardless of what the commit protocol says.

**Aliasing one tile extent from two entries.** Closed at three levels: `[R-CNT-13]` ("Extents are owned exactly once"), §15.3's two verifier rows, L17/F35 with the intra-layer/cross-layer scope split spelled out.

**Escaping the file bounds via the front block or the trailer.** Every extent-bearing field is independently bounded to [16, F−64): `[R-CNT-06]` for the directory, `[R-CNT-13]` for record and sub-record slots, §15.3 for index entries. F35's naming of the front block and trailer as overlap participants is unreachable belt-and-braces, not a hole.

**Zeroed / all-0xFF index regions.** `[R-IDX-02]`'s rationale is correct on its own terms: an all-zero region parses as offset 0/length 0 → §15.3 reject-tile; an all-0xFF region fails the sentinel's crc = 0 requirement → reject-tile. Neither degrades to silent fill, and `[R-TYP-09]` forecloses fill-as-failure-fallback.

**Constants.** I implemented CRC-32C from §4.5's parameters (poly 0x1EDC6F41, reflected in/out, init and final XOR 0xFFFFFFFF), confirmed it against §4.5's own check vector (`"123456789"` → `0xE3069283`, empty → `0x00000000`), then checked the two derived constants the document asserts: **§15.4's all-sentinel full-segment CRC `0xEECB3BB2` is correct** (2¹⁶ × `FF×16 00×4`), and **Appendix A's trailer CRC `0xE00938D2` over trailer bytes [0,60) is correct**. `[R-CNT-23]`'s "crc_of_crc_array = 0 when entry_count = 0" is consistent rather than special-cased, since CRC-32C of zero bytes is 0.

**Worked examples.** I re-derived every numeric example: §11.2 grids, §11.4 ordinals (spatial 10, planar disk 74, in-tile 11,452), §12.3's 12-byte channel entry, §14.2's three stride cases (18/12/30 bytes and the byte offsets), §14.3's `55 01` / `55 FD` packed plane, §14.5's 32-byte edge tile, §15.4's 1,000,000-entry layout (segment 15 at [19,660,800, 20,000,000), array at [20,000,000, 20,000,064)), §17.3's shuffle output, §20.3's 644-byte index, §21.9's 256 KiB array at 2³² entries, §5.1's 128-byte floor. **All correct.**

**Register arithmetic.** §21.8 claims "121 conditions over 213 named instances". Counting rows: 38 + 47 + 26 + 10 = **121** ✓ (§21.3 runs L1–L48 with L40 absent, giving 47). Counting semicolon-separated instances under §21.1's mechanical rule: 69 + 81 + 43 + 20 = **213** ✓. Exact.

**All-padding tiles.** I looked for a stored tile made entirely of padding positions, where `[R-SER-05]`'s content rule and `[R-GEO-04]`'s never-return rule would leave a tile with no defined observable. Impossible: G = ⌈E/T⌉ guarantees (G−1)·T < E, so every tile holds at least one real position along each axis, and E = 0 yields G = 0 and no tiles at all.

**A conforming file every reader must reject.** A top-level record of experimental type ≥ 0x8000 with MU = 1 is a *conforming* file (`[R-CNT-15]`: "a record type from the experimental range is conforming"; `[R-CNF-02]`) that every reader must reject-file, and F37 lists it in a table titled "File-scope violations". I expected a certify/reject split. **Refuted** by `[R-VEC-02]` ("The two axes are independent: a conforming file can carry a record a reader ignores… and a nonconforming file can still read correctly"), §21.6's closing paragraph applying the same pattern to F24/version_major, and `[R-COD-11]`'s precedent that a verifier which cannot establish conformance MUST NOT certify. Resolvable.

---

## Findings

### BYTE-LEVEL AMBIGUITY

**1. §5.2's constructive declared-padding test vs. §16.1/§16.2's assertion — a gap whose classification, and therefore the file's verdict and the verifier's dead-space total, differ between readings.**

- **Location.** §5.2 `[R-CNT-02]`/`[R-CNT-03]` (the "when, and only when" test and the zero rule); §16.1 `[R-SLB-01]`; §16.2 `[R-SLB-03]`; §16 lead-in `[R-SLB-05]`; §21.2 row **F9** and its instance list; §9.7 `[R-LIF-08]`; §21.6's dead-space row.
- **Reading A.** A maximal unclaimed run preceding an alignment- or slab-constrained structure is declared padding **only** if its length is below the modulus (equivalently, only if the writer took the *nearest* legal offset). A longer run is dead space: unconstrained content, counted in the verifier's mandated dead total, no violation. Certify.
- **Reading B.** The run preceding such a structure **is** declared padding (§16.1, §16.2 state it flatly; F9 names "per-tile alignment gaps (16.1); slab run-placement gaps (16.2)" as instances with no length qualification). It MUST be zero; nonzero is a file-scope validity error. Reject-file. (A third reading takes the ≥-modulus run as an §16 invariant failure → reject-layer.)
- **Discriminator D1.** The 320-byte generation-1 file tabulated in §1 above: one layer, S = 2, **A_slab = 1**, four 1-byte tiles at 16, 17, 24, 25, a 6-byte unclaimed run at [18,24) with byte 20 = `FF`. Reading A: **certify**, dead-space total **6**. Reading B: **reject-file** (F9), dead-space total **0**. With byte 20 = `00` the verdicts agree but the mandated totals still differ, 6 vs 0. Under A_slab = 1 *no* nonempty gap can ever satisfy "shorter than A_slab", while the same sentence says "between runs, placement freedom governs" — so the recommended contiguity-only declaration cannot leave a legal gap under reading B at all.
- **Discriminator D2.** One layer with **A = 512**, stored tiles at 512 (len 100) and **1536** (len 100) — both offsets legal, L39 satisfied — leaving a 924-byte unclaimed run at [612,1536) with `FF` at offset 700. Reading A: certify, dead 924. Reading B: reject-file, dead 0. This is the ordinary output of a writer using fixed aligned slots for variable-length tiles.
- **What I searched.** Every occurrence of "declared padding", "dead space", "maximal run", "next legal offset", "shorter than A", "placement freedom", plus §9.7's walk, §20.2, §22.3, Appendix G item 5 and Appendix H's verifier checklist. §9.7 cannot resolve it — it enumerates "the declared padding §5.2 defines", i.e. the disputed term. `[R-SLB-05]` restates the dispute rather than settling it. The decisive negative evidence: the spec supplies **F12** for exactly this failure mode on the *other* padding class (a pre-trailer gap ≥ 64 is a violation) and supplies **no** counterpart row for a gap ≥ A or ≥ A_slab, so the register cannot arbitrate either.

### CONTRADICTION

**2. `[R-LIF-06]` directs verifiers to enumerate generations for coverage verification; `[R-LIF-08]` and §21.6 say nothing enumerates prior commits.**
§9.6 `[R-LIF-06]`: "Recovery tools and verifiers … probe backward at 64-aligned offsets … **Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0.**" §9.7's Note: "**Nothing here enumerates prior commits.** A verifier certifies what a reader can reach and counts what it cannot … does not depend on reconstructing the file's history." §21.6: a trailer-mimicking payload is "Inert: **nothing enumerates dead space**." These prescribe two different algorithms for the same task, §5.2's coverage verification. The three-to-one weight (plus Appendix D's "no generation-attribution machinery and no trailer chain") resolves it in favor of §9.7, but the §9.6 sentence is live normative text: a verifier that follows it walks dead-space trailer candidates, and any such candidate whose dir CRC fails would be a rejection reading §9.7 never produces.

**3. `[R-CNF-02]` makes file conformance a pure predicate on bytes; `[R-SLB-04]` and register row L43 condition a validity error on what a commit did.**
§2.3: "File conformance is a pure predicate on bytes: it does not depend on any reader, writer, or environment." §16.2 `[R-SLB-04]`: "carrying a stale declaration forward is a validity error at layer scope", where "stale" is defined by whether "the commit changed an affected run's stored-tile set or byte placement" — and L43 restates it as a verifier-detected, certification-time condition. A verifier walking the live state only cannot evaluate that antecedent. Whenever the live state's invariants hold, the declaration is not observably stale; whenever they fail, L41/L42 already fire. L43 is therefore either undecidable from bytes (contradicting `[R-CNF-02]`) or wholly subsumed — and §21.8 promises it a conformance vector that cannot be distinguished from an L41/L42 vector.

**4. §2.3 says "Conformance is defined for four classes" and then defines five.**
The bullets are conforming file (`[R-CNF-02]`), reader (`[R-CNF-03]`), writer (`[R-CNF-05]`), updater (`[R-CNF-06]`), and verifier (`[R-CNF-11]`). Cosmetic on its own, but it reads as a count left stale when the verifier class was added — the same era as the register gaps in finding 5.

**5. §21.1 declares the register's completeness normative; at least six violations the document names have no register row.**
§21.1: "The register below enumerates every violation this specification names: … Its **completeness is normative** — a violation this specification names and the register omits is a defect in this document." Omitted:
- `[R-CNT-25]`: a user-metadata record "whose extent_length is less than 5 … is a validity error at its containing scope". F27 and L11 cover only the (0,0) case; nothing covers extent_length 1–4.
- `[R-MTA-03]`: "A record whose inline_length is not 1 is a validity error at the record's containing scope." No F- or L-row.
- `[R-CNT-15]`: "a verifier MUST treat a **reserved-range** record type as a validity error at the record's governing scope." F37 and L24 cover only unassigned-type-with-MU=1; the reserved-range-with-MU=0 case (reader ignores per R10, verifier must reject) has no row at either scope.
- `[R-MTA-09]`: the metadata-zstd frame constraints (no second or skippable frame, no content-checksum flag) whose violation is ignore-record. R3 covers only "fails to decode"; a content-checksum frame decodes cleanly.
- `[R-MTA-07]`: "A writer MUST NOT emit a standardized key outside the scopes its row lists."
- `[R-MTA-05]` (unsorted members) and `[R-CNT-22]` (stored-flag mismatch on a registered type) both state "the file is nonconforming" yet appear only in §21.6, whose preamble reads "These are defined behaviors, **not errors**."

The consequence is concrete: §21.8's "121 conditions over 213 named instances" is arithmetically exact against the current tables (I verified both totals), so each omission shifts a count the corpus obligation `[R-ERR-02]` is written against, and each leaves a nonconforming file with no vector and no register row for a verifier to hang a refusal on.

### OBSERVATION

**6. §5.2 defines dead space twice, inconsistently, and generation-1 gaps fall in the crack.** "Every other byte of the file is dead space" (extensional, complement of the live state) versus "bytes **an earlier commit wrote** that the live state no longer reaches" (intensional, presupposing an earlier commit). For a generation-1 file with a gap between two live structures the two disagree — the second yields bytes that are neither live nor dead. §9.7's operational rule ("Bytes the walk does not reach are dead space: the verifier sums them and reports the total") resolves the *total* toward the extensional reading, and `[R-CNT-21]`'s "no conformance requirement applies to it" resolves the verdict toward certification, so I do not classify this as byte-level. But it leaves `[R-SLB-05]`'s "a commit that produces dead space it did not supersede is a writer defect" with no home: it names a defect that is not a file violation, has no register row, and — under finding 1's reading A — is committed by every aligning appender on every generation ≥ 2, since the run preceding the first appended aligned tile always subsumes the prior generation's dead trailer.

**7. §9.7's walk enumeration is narrower than §5.2's live state, making the mandated dead-space total implementation-dependent.** `[R-LIF-08]` enumerates "the live directory and its records, each record's extent, each layer's tile-index region and that region's non-sentinel entries, and the declared padding §5.2 defines", then declares everything the walk misses to be dead space. That enumeration omits the **front signature block** (16 bytes), the **live trailer** (64 bytes), and — on a strict reading of "the live directory and *its* records" — **layer sub-record extents**, all three of which §5.2 places inside the live committed state and F35/L17 name as overlap participants. Two verifiers therefore report totals differing by 80 bytes plus the size of every layer-scope user-metadata document, on a file both certify. `[R-CNT-21]` makes reporting that number a MUST and §22.3 makes it security-relevant ("the number that distinguishes a working file from a padded one"). A careful reader reconciles via §9.7's own opening ("walks the live state only"), which is why this is an observation and not finding 1.

**8. §20.5 tells a compactor placement is free without excepting declared layout invariants.** `[R-WRT-07]`: "A compactor preserves content but not placement — placement is not among the things it carries forward, and it is free to place structures anywhere §5.2 admits." A compactor carries the layer record forward, including A or S/A_slab, and `[R-SLB-04]` binds only a writer that "supersedes a stored tile in, or grows the extents of" such a layer — relocation is neither. A compactor following §20.5 literally can emit a slab-declared layer whose runs are no longer contiguous; the output is then nonconforming under `[R-SLB-03]` (L41/L42). "Anywhere §5.2 admits" arguably imports the constraint, so this is resolvable, but §20.5 would be safer stating the compactor's honor-or-clear duty the way `[R-SLB-04]` states the appender's.

**9. §21.3's row identifiers skip L40 with no note.** §2.2 establishes a discipline for retired identifiers, and §14.4 exercises it explicitly for `[R-SER-04]`. L40's silent absence is the one place a reader auditing the register's "47 conditions" cannot tell an omission from a retirement.

**10. `[R-CNT-04]` licenses two conforming readers to reach opposite verdicts on the same bytes.** A file with a corrupt front signature block and everything else valid is reject-file to a local reader and fully readable to a remote one ("a remote reader MAY defer or omit this check"). This is a designed divergence, not an ambiguity — §2.3 makes a verifier check "every file-level requirement", so certification is unaffected — but it is the one place the document lets transport, rather than bytes, decide what a reader returns, and it is worth stating as such next to `[R-CNF-02]`'s "does not depend on any reader … or environment".

---

## Verdict

IMPLEMENTABLE: qualified
BYTE-LEVEL AMBIGUITIES: 1
CONFIDENCE: high

The single byte-level ambiguity is repairable with one sentence: state in §5.2 what a maximal unclaimed run that is *not* below the modulus is (dead space, or a validity error with a register row), and make §16.1 and §16.2 state the padding clause as a writer obligation conditioned on that test rather than as an assertion of fact. Everything else I attacked — extent ownership, the sentinel, index segmentation, the codec pipeline, the reader tiers, the constants, the register arithmetic — held under deliberate assault.
