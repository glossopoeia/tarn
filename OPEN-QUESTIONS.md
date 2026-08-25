# Open Questions

The living decision ledger for the TARN format. Every entry here ends its life
as an ADR in [docs/decisions/](docs/decisions/); when that happens the entry
is updated to `Resolved → ADR-NNNN` (and eventually pruned).

Entry format: **Question / Why it matters / Options & tradeoffs / What
settles it.** Priorities: **[blocking]** — must be resolved before its spec
section can be finalized (some resolve within that section's drafting
batch); **[shaping]** — affects multiple sections, resolve early;
**[deferrable]** — can be resolved whenever convenient.

Related sub-questions already attached to accepted decisions are listed as
`Confirm:` lines in their ADRs; this ledger holds the genuinely open design
questions plus those Confirm items that need real analysis.

---

## A. Container placement and discovery

### Q-A1. Where does the consolidated metadata directory live? [Resolved → ADR-0018]
**Resolution:** hybrid — 16-byte constant, pointer-free front signature
block plus the authoritative 64-byte trailer at EOF, directory adjacent.
- **Why:** The O(1) round-trip requirement is fixed (ADR-0006); placement is
  not. A front directory gives the best cold read but forces in-place
  rewrites on every append; a tail directory supports cheap append but makes
  discovery a suffix fetch.
- **Options:** (a) Fixed front header + front directory — kills cheap append.
  (b) Fixed-size checksummed trailer + directory at tail — one speculative
  suffix range request; append = write payloads, new directory, new trailer.
  (c) Hybrid: a tiny fixed front signature block (magic, version, and either
  a pointer to the authoritative trailer or a "scan the tail" marker) plus
  the authoritative tail structure — front bytes for sniffing/MIME, tail for
  authority.
- **What settles it:** Decide Q-A2 first; then write out the cold-read
  request sequence and the append sequence for each option and count
  requests and rewritten bytes. Leaning: (c), if the front block stays ≤ 16
  bytes.

### Q-A2. What is the mutability and consistency contract? [Resolved → ADR-0017]
**Resolution:** append-only with atomic trailer swap (committed-prefix
immutability); read-only is the degenerate single-generation case.
- **Why:** This is the highest-leverage open decision: it shapes the trailer,
  directory, integrity story, byte-coverage rule, and privacy section.
  In-place pointer patching inherently has torn-write windows — a crash
  mid-patch can corrupt metadata for data that was not being modified.
  PMTiles' one blunt sentence ("read-only; use a database if you need
  updates") is the honesty bar; Zarr delegates consistency to the store
  layer, but a single-file format has no store to delegate to.
- **Options:** (a) Read-only artifact: updates are whole-file rewrites;
  simplest spec. (b) Append-only with atomic trailer swap: new payloads →
  new complete directory → new fixed-size trailer, in that order; prior
  bytes never modified; the last valid (checksum-verified) trailer is
  authoritative; a torn append leaves the file readable at its prior state.
  Requires: single-writer/multi-reader stated normatively, a generation
  counter for cache revalidation, and a defined scan-back recovery rule.
  (c) In-place mutation: rejected — every in-place scheme needs journaling
  to be crash-safe, which is a database, which is a non-goal.
- **What settles it:** Enumerate the real mutation stories (append a layer,
  amend metadata, compact) and check which ones actual workflows need.
  Leaning: (b), with the torn-append recovery rule written in the same ADR.

### Q-A3. Is there a normative byte budget for the discovery fetch? [Resolved → ADR-0019]
**Resolution:** two-request baseline is normative (trailer, then
exact-range directory); 64 KiB is the writer-SHOULD window that makes the
single-fetch optimization succeed.
- **Why:** PMTiles' "root directory MUST fit in the first 16,384 bytes"
  converts "O(1) round trips" from aspiration into a testable conformance
  property — but cost writers repeated attempts to satisfy it. Whether the
  per-layer tile index counts against the budget decides everything about
  index encoding (Q-E3).
- **Options:** (a) Fixed suffix/prefix window constant (e.g. trailer +
  directory fit in the final 64 KiB) with a spill pointer for oversized
  indexes. (b) Formula-based budget — precise, harder to state and test.
  (c) No byte budget, only a bounded-request guarantee ("directory reachable
  from the trailer in ≤ 1 additional request") — weaker but always
  one-pass-writable.
- **What settles it:** A size model: bytes per directory entry and per
  index entry × realistic layer/tile counts (1-layer thumbnail case through
  a 10⁶-tile case). Pick the strongest budget a one-pass writer can always
  satisfy.

### Q-A4. What indirection depth does the spec guarantee? [Resolved → ADR-0019]
**Resolution:** serial depth — complete metadata ≤ 3 requests, first tile
≤ 4 (≤ 1 / ≤ 2 with the suffix optimization on typical files); per-layer
index fetches parallelize.
- **Why:** An unbounded metadata hierarchy silently destroys the O(1) claim;
  PMTiles normatively bounds leaf-directory depth for exactly this reason.
- **Options:** (a) Everything inline in the directory — one request, but
  bloats discovery for huge layers. (b) Directory inline, per-layer tile
  index spillable exactly one hop — "all metadata in ≤ 2 requests," stated
  normatively. (c) Unbounded — rejected.
- **What settles it:** The Q-A3 size model. The spec then states the
  cold-read accounting ("request 1: discovery window; request 2
  (conditional): spilled tile index; request 3: payload") as a guarantee.

### Q-A5. Is a zero-layer file valid? [Resolved → ADR-0032]
**Resolution:** valid — an empty directory is a conforming generation.
- **Why:** The data model (spec §3.1) deliberately makes no minimum-layer
  claim. The append model creates files generation by generation, and the
  same schema-first reasoning that made zero-extent layers valid
  (ADR-0028) applies one level up: create-and-commit an empty container,
  append layers later. The container section must define what an empty
  directory means either way.
- **Options:** (a) Valid: a directory with zero layer records is a
  conforming generation; readers open it and list nothing. Consistent
  with ADR-0028's empty-things-are-valid principle. (b) Invalid: at
  least one layer per file; writers buffer until the first layer is
  ready. Simpler for readers that assume non-emptiness, at the cost of
  an asymmetry with empty layers.
- **What settles it:** Drafting §5/§7 (Batch 3): whether any container
  invariant actually needs a layer to exist. Leaning: (a).

### Q-A6. Does `[R-LIF-02]`'s write procedure bind a compactor? [Resolved → ADR-0094, reversing ADR-0093]
**Final resolution (ADR-0094): it binds.** A compactor MUST follow
`[R-LIF-02]`'s creation path, as §20.2 obliges a creator: the output has no
prior trailer and stands at generation 1, which is the case that path
states. ADR-0093 decided the opposite and the audit before round 25
falsified it against **five** existing passages — §20.1's `[R-WRT-01]` and
§20.5's own earlier sentence ("a compactor satisfies every writer
requirement for the bytes it produces"), `[R-LIF-02]`'s second paragraph
(stated for *creation*, not for a commit), §6.3's `[R-CNT-08]` (which
classes a compactor as a writer creating a file under this text and carves
out only the flags rule), and Appendix H's writer checklist ("follows the
commit protocol including both barriers"). ADR-0093's own warrant, that
the protocol "is stated for a commit", was false of that second paragraph.

**What the two decisions cost, recorded because the pattern matters more
than the outcome.** Round 23 reported this defect and graded it
design-decision; it was deferred here. Round 24 graded it byte-level. The
first repair chose the reading that required amending five passages, and
the audit caught it before a round did. The reading that required one
sentence was the one the document had already taken in five places.

**Superseded resolution (ADR-0093):** it does not bind.
**Resolution:** it does not. `[R-LIF-02]` is stated for a commit, and
`[R-LIF-01]` makes a compaction a whole-file rewrite under a new `file_id`
rather than a commit, so neither its barrier ordering nor its step 5 pad
reaches that tier. §20.5 now states both consequences as intended: the
output's pre-trailer gap is fixed by nothing, so two conforming compactors
MAY emit outputs of different lengths — §2.3 already named the over-long
gap as no file-conformance violation — and no barrier ordering is owed
within the output, because a compaction leaves its input intact and a torn
output is an unreadable file rather than a damaged one, with a SHOULD to
make the output durable before anything discards the input.

**This entry is also a lesson about deferral.** Round 23's writer walk
reported this defect, round 23's three triage passes graded it
*design-decision*, and it was sent here rather than repaired. Round 24's
three passes graded the identical finding **byte-level**, unanimously. The
text never changed; the grading did. **A design-decision grade is not a
finding that something is not byte-level**, and a byte-level defect sat in
this ledger for a full cycle as a result.
**Question:** §20.2 binds a creator and §20.3 an appender to `[R-LIF-02]`
by name. §20.5 binds a compactor to no write procedure at all.
- **Why it matters.** Two readings are defensible and they differ on
  emitted bytes. (A) It binds: a compactor's output is a generation-1 file
  with no prior trailer, which is exactly §9.2's creation path; §20.1
  lists the compactor as a writer tier and `[R-WRT-01]` says it "satisfies
  every writer requirement for the bytes it produces". Under A it owes
  both barriers and its pre-trailer pad is the minimum to the next 64-byte
  boundary. (B) It does not: `[R-LIF-01]` explicitly contrasts a commit
  with "a whole-file rewrite under a new file_id (compaction, §20)".
  Round 23's writer walk reported it; triage graded it a design decision,
  not byte-level, because no register row fires either way — but a
  compactor's pad length is a byte question.
- **Options:** (a) State that `[R-LIF-02]` binds a compactor, as §20.2 and
  §20.3 state it for their tiers. (b) State that it does not, and say what
  does bind the output's pad and barriers. (c) Leave it, on the ground
  that `[R-WRT-01]`'s blanket already decides it — which is the reading
  round 23 could not confirm from the text.
- **What settles it:** whether any two conforming compactors can differ in
  emitted bytes under (a) and (b); if they can, the silence is a defect
  and not an economy.

## B. Slabs and physical layout

### Q-B1. What exactly is a slab? [Resolved → ADR-0022]
**Resolution:** layout guarantee only — per-layer (S, A_slab) declaration in
the core layer record; index stays per-tile.
- **Why:** "Aligned, contiguous run of tiles treated as one I/O unit" admits
  at least two designs with very different spec surface. Zarr's
  sharding-indexed codec is the closest ancestor (a shard is a chunk of
  chunks with its own offset/length index) but cannot promise physical
  contiguity or alignment; those are exactly what TARN's container can add.
- **Options:** (a) **Layout guarantee only:** a per-layer declaration plus
  invariants ("tiles of a slab are consecutive in linearization order and
  contiguous in the file; slab start honors the layer alignment"); the index
  stays per-tile; readers may coalesce range requests; zero new reader code.
  (b) **Index granularity:** the index stores per-slab offsets plus per-tile
  lengths/checksums within each slab — smaller index, but sentinel/fill
  interactions and partial-slab semantics get harder. (c) **Compression
  context:** rejected outright — cross-tile codec state destroys random
  access (the single-compression-stream failure PNG demonstrates).
- **What settles it:** Index-size arithmetic under (a) vs (b) for large
  layers (does (a) blow the Q-A3 budget?), plus a written O_DIRECT/GPUDirect
  usage sketch showing which invariant consumers actually need. Leaning:
  (a), revisiting (b) only if index size forces it.

### Q-B2. Which linearization order is normative? [Resolved → ADR-0020]
**Resolution:** row-major (last-declared dimension fastest) via a u16 enum
whose only emittable v1 value is 1; Morton/Hilbert IDs reserved without
semantics; in-tile order row-major permanently.
- **Why:** Slabs ("consecutive in linearization order"), index entry order,
  delta-encoded offsets, and range coalescing are all defined against one
  order — it cannot be implementation-defined. The two candidates are
  first-declared-dimension-fastest (Fortran/column-major flavor) and
  last-declared-dimension-fastest (C/row-major flavor, the dominant
  convention in the NumPy/GPU-tensor ecosystem TARN targets).
- **Options:** (a) First-dim-fastest. (b) Last-dim-fastest (C order) — an
  image declared (y, x) gets row-contiguous pixels, matching ecosystem
  expectations. (c) Per-layer enum with one mandatory value now and
  Morton/Hilbert IDs reserved for the future.
- **What settles it:** Name the reference consumers. If they are NumPy-like
  and GPU tensor runtimes, (b) — or (c) defaulting to (b). The ADR carries a
  worked coordinates → tile-ordinal → byte-offset table either way.

### Q-B3. Planar mode: how are per-channel tiles ordered on disk? [Resolved → ADR-0021]
**Resolution:** channel-major — ord(c, s) = c·N + s.
- **Why:** ADR-0012 fixes planar tile order normatively but leaves the choice
  open. Slab semantics must state which grouping contiguity preserves.
- **Options:** (a) Channel-major (all spatial tiles of channel 0, then
  channel 1, …): a whole channel is one natural slab; single-channel scans
  are contiguous. (b) Spatial-major (all channels of tile 0, then tile 1,
  …): full-sample window reads touch adjacent bytes. (c) Free order with the
  index as sole truth — kills slab guarantees for planar layers; rejected
  unless evidence demands it.
- **What settles it:** The dominant planar read pattern (single-channel scan
  vs all-channel window) in target workloads. Leaning: (a) channel-major —
  planar exists to serve channel-wise access.

### Q-B4. Are shared/deduplicated tile extents ever permitted? [Resolved → ADR-0024]
**Resolution:** no — every stored and metadata extent referenced exactly
once; intra-layer overlap → reject-layer, cross-layer/metadata → reject-file.
- **Why:** Two index entries pointing at one payload extent break alignment
  arithmetic, byte-coverage accounting, and verifier simplicity (aliasing is
  also an attack surface). PMTiles uses offset-reuse dedup deliberately —
  but its motivating case (oceans of identical tiles) is handled in TARN by
  the fill sentinel.
- **Options:** (a) Forbid sharing and overlap entirely: every payload extent
  referenced exactly once; coverage becomes checkable. (b) Allow dedup only
  in unaligned layers — two file classes, more spec text. (c) Allow
  generally — rejected.
- **What settles it:** Whether any real N-D dedup case survives once fill
  sentinels exist. Leaning: (a).

### Q-B5. Does TARN adopt a full byte-coverage rule? [Resolved → ADR-0030, rescoped by ADR-0048]
**Resolution:** strict — coverage is file validity; declared padding is
zero bytes; unclaimed bytes make the file nonconforming.
- **Why:** Unreferenced byte ranges are a smuggling channel and an
  ambiguity: PNG both forbids and merely-warns-about trailing data;
  PMTiles cannot certify a file byte-for-byte because sections may sit
  anywhere. Under an append model (Q-A2b), superseded bytes are *normal*, so
  "every byte classified" needs a dead-space category.
- **Options:** (a) Strict: every byte of a valid file is header, directory,
  referenced payload, declared padding, or declared-dead (superseded);
  verifiers can enumerate coverage. (b) Verifier-level only: coverage is a
  check, not file validity. (c) None — rejected given "integrity by
  default."
- **What settles it:** Work the append story under (a): does declaring dead
  ranges cost more than it buys? Either way the spec states that logical
  deletion is not erasure and compaction is the only true removal (privacy
  section).

## C. Integrity

### Q-C1. Which checksum algorithm? [Resolved → ADR-0023]
**Resolution:** CRC-32C (RFC 3720 parameters) everywhere, LE u32.
- **Why:** ADR-0008 recommends one algorithm everywhere; the Confirm is
  which. CRC-32C has hardware support (SSE4.2/ARMv8), 4-byte entries, and
  Zarr precedent; xxHash3-64 is faster in software with 64-bit strength but
  is not an error-detection-designed code and doubles the index column.
- **Options:** (a) CRC-32C everywhere. (b) CRC-32C for metadata + a 64-bit
  fast hash for payloads — faster bulk verify, two algorithms in a
  weekend-implementable spec. (c) CRC-32 (IEEE) — no advantage over
  Castagnoli absent legacy constraints.
- **What settles it:** Throughput measurements at 1–16 MiB tile sizes on
  commodity hardware; stdlib/tiny-dep availability across C, Go, JS,
  Python, and Rust. Leaning: (a).

### Q-C2. Do tile checksums cover stored (wire) bytes or decoded bytes? [Resolved → ADR-0023]
**Resolution:** stored bytes, verified before decompression; decoded-hash
ancillary record type reserved.
- **Why:** ADR-0004 decides *stored bytes* and flags the choice for
  ratification here, because it is a real tradeoff: wire-byte checksums give
  verify-before-decompress, exact-fetch validation, and bomb defense, but do
  not attest the decoded array; decoded-byte checksums do the reverse and
  force decompression before any verification.
- **Options:** (a) Stored bytes only (ADR-0004's decision). (b) Decoded
  bytes only — rejected for the security ordering alone. (c) Both — strongest
  attestation, +4–8 bytes per index entry and doubled verify cost.
- **What settles it:** The security section's threat-model writeup: which
  failures must be caught before allocation/decode. Note the structural
  backstop: decoded size is fully determined by declared geometry regardless
  (ADR-0009), which is what makes (a) sufficient. Leaning: (a) — ratified in
  the same ADR that resolves Q-C1 (checksum algorithm), which records both
  answers.

### Q-C3. Checksum-mismatch severity table. [Resolved → ADR-0031]
**Resolution:** trailer/directory → reject-file; layer index → reject-
layer; tile → reject-tile; user metadata → ignore-record + report.
- **Why:** A checksum whose failure consequence is unspecified is
  documentation, not integrity. The outcome must be per-structure, not
  global: partial-read workflows should survive a single bad tile.
- **Options:** (a) Discovery/directory/index mismatch → reject-file (or fall
  back to the previous valid trailer under Q-A2b); per-layer index → reject-
  layer; tile payload → reject-tile; user-metadata → ignore-record with a
  surfaced warning. (b) Any mismatch → reject-file — hostile to partial
  reads. (c) Reader discretion — rejected (divergence by construction).
- **What settles it:** Mostly a decision to write down; (a) is the leaning.
  Every row of the final table gets a corrupted-file conformance vector.

### Q-C4. Padding determinism: what bytes fill padding, normatively? [Resolved → ADR-0030 + ADR-0037]
**Resolution:** alignment-gap and pre-trailer padding bytes are zero
(ADR-0030; verifier-checked at file scope); edge-tile padding samples
carry the channel's fill encoding, and packed-boolean pad bits the
mapped channel's fill bit (ADR-0037) — the latter half writer-MUST,
verifier-checked, reject-tile.
- **Why:** ADR-0011 requires defined padding; the Confirm is *which*
  definition. Padding participates in compression and checksums, so
  unspecified padding makes identical logical data yield different physical
  bytes — breaking reproducibility and content-addressing.
- **Options:** (a) Edge-tile padding samples = the channel's fill-value
  encoding (every decoded sample is meaningful; naive readers that forget to
  clip see fill, not garbage). (b) All-zero bytes (simplest; but a nonzero
  fill makes padding distinguishable from fill, and interleaved fill tuples
  make "zero" a special case anyway). Alignment-gap bytes between tiles:
  zero, in either option.
- **What settles it:** Whether padding is ever legitimately observable — it
  is exactly when a buggy reader fails to clip, which argues (a). Leaning:
  (a) for edge samples, zero for alignment gaps.

### Q-C5. Must a certificate name an unassigned-type record's extent? [shaping]
**Question:** §22.3 names four residues a certificate cannot vouch for.
The verifier's report reaches three — slack is counted and totalled
(`[R-CNT-21]`), a user-metadata extent under an unassigned encoding is
counted and named (`[R-MTA-10]`), a trailer-mimic in slack is inert. The
fourth is not reached: **the extent of a record of a type this
specification has not assigned.**
- **Why it matters.** Those bytes are live committed state — `[R-CNT-02]`
  names "a record extent (the bytes any record's extent slot references,
  whatever the record's type)" as a claimant class — so they are excluded
  from the slack total and the certificate covers them. §8.1 gives them no
  checksum. `[R-MTA-10]` states the principle for the neighbouring case in
  terms: "bytes a certificate covers without inspecting are counted and
  named, never silent", and §22.3 gives the operational point, "an
  operator who wants no such bytes rejects on that report line". The
  operator has no such line here. Not byte-level — the file certifies as
  conforming either way — but it is what the certificate discloses.
- **Options:** (a) Extend `[R-MTA-10]`'s report duty to any record whose
  type this specification has not assigned, naming the type, the owning
  scope and the extent length. (b) Fold those extents into the slack
  total, which contradicts `[R-CNT-02]`'s claimant classes. (c) Leave it
  and say in §22.3 that this residue is deliberately unreported.
- **What settles it:** whether an operator can distinguish, from a
  certificate alone, a file with no uninspected extents from one with a
  16 MiB extent of an unassigned type. Today they cannot.

## D. Types, fill, statistics

### Q-D1. 8-bit floats: reservation details. [Resolved → ADR-0036]
**Resolution:** both reserved, neither ships — IDs 14 (E4M3) and 15
(E5M2) pinned to bit-exact OCP OFP8 only; no named consumer
materialized.
- **Why:** ADR-0013 keeps fp8 out of v1 with IDs reserved for OCP E4M3/E5M2
  only. The residual questions: are both reserved, and does any near-term
  consumer justify shipping them in v1 after all?
- **Options:** (a) Reserve both E4M3 and E5M2, ship neither. (b) Ship both
  now — two more mandatory types every weekend implementation must handle
  (storage is trivial; fill parsing, NaN rules, and stats ordering are not).
- **What settles it:** A named consumer exchanging OCP FP8 tensors through
  TARN files. Leaning: (a).

### Q-D2. 128-bit integers/floats and an `opaque<N>` escape hatch. [Resolved → ADR-0036]
**Resolution:** all deferred — IDs 16/17/18 (int128/uint128/float128)
and 19 (opaque) reserved without semantics; no v1 corpus materialized,
and opaque's N-in-fill-length encoding would hollow out the
fill-length cross-check.
- **Why:** ADR-0013 drops 128-bit types from v1. The open sliver: does a
  fixed-size raw-bytes type (`opaque<N>`) enter v1 as the pressure valve
  (IDs/UUIDs/hashes as samples), or is it deferred too?
- **Options:** (a) Defer both; revisit on demand. (b) Add `opaque<N>` in v1:
  zero numeric semantics (fill is raw bytes; no stats; shuffle stride = N),
  keeps the numeric list closed. (c) Keep 128-bit ints — rejected absent a
  named consumer.
- **What settles it:** Whether plausible v1 corpora (e.g. content hashes per
  cell) exist. Leaning: (b) if a concrete case shows up during drafting,
  else (a).

### Q-D3. Fill-value edge cases. [Resolved → ADR-0036]
**Resolution:** bool fill is one byte, 0x00 or 0x01, others
reject-layer; interleaved fill composes per channel in declared order.
Packed-form pad bits stay with Q-D6 (serialization).
- **Why:** ADR-0010 fixes fill as raw element bytes; two corners remain.
  Packed booleans: what is the fill *bit*, and what do final-byte pad bits
  contain? Interleaved layers: fill is per-channel and composed into a
  sample tuple — the spec must say so explicitly.
- **Options:** Boolean fill: (a) MUST be 0 or 1 with pad bits = fill bit;
  (b) any byte, LSB governs — rejected (two encodings for one value).
- **What settles it:** Drafting the packed-boolean section; the choice is
  recorded in the same ADR that settles ADR-0012's boolean-packing Confirm
  item, with a paired test vector.

### Q-D4. Unstored-tile sentinel encoding. [Resolved → ADR-0024]
**Resolution:** all-ones offset and length, CRC field 0, with the full
invalid-combination table.
- **Why:** ADR-0010 requires a sentinel; the Confirm is its bit pattern.
  Precedent (Zarr sharding) uses all-ones offset+length but leaves every
  other malformed combination undefined — the gap TARN closes.
- **Options:** (a) offset = 2⁶⁴−1 ∧ length = 2⁶⁴−1, checksum field MUST be
  0 — no valid-offset collision ever, ecosystem-familiar. (b) offset = 0 ∧
  length = 0 — workable only because offset 0 is always the signature, but
  perpetuates "zero means missing" conflation. (c) A per-entry flag bit —
  costs index width for no expressiveness gain.
- **What settles it:** Pick (a) or (b) — leaning (a) — then do the real
  work: enumerate every other invalid entry class (offset past EOF, length
  past EOF, overlap, sentinel-offset with nonzero length, nonzero checksum
  on sentinel) with required outcomes and an invalid vector each.

### Q-D5. Per-channel min/max statistics: keep, and where? [Resolved → ADR-0045]
**Resolution:** standardized user-metadata key `tarn.stats` — advisory
by construction, since metadata cannot affect decoding, so no
staleness rules, verifier obligations, or preserve-on-edit semantics
are needed; NaN excluded from min and max.
- **Why:** Eagerly-maintained stats go stale by construction the moment
  tiles are rewritten, and presence flags do not belong inside type words
  (ADR-0013). If stats exist they must be honest about their reliability.
- **Options:** (a) A distinct, optional, preserve-on-edit ancillary record,
  explicitly *advisory*: readers MUST NOT rely on it for correctness;
  verifiers MAY check it; NaN excluded from min/max, stated. (b) Optional
  fields in the channel record — repeats the flag-smuggling pattern.
  (c) Authoritative stats readers may prune on — imposes
  recompute-on-every-write; rejected. (d) Omit entirely in v1, reserve the
  record type.
- **What settles it:** Whether any planned consumer needs stats for
  correctness (e.g. nodata-aware range scaling) vs convenience. Leaning:
  (a), or (d) if drafting shows the semantics cost more than they give.

### Q-D6. Boolean representation. [Resolved → ADR-0037 + ADR-0038]
**Resolution:** planar bool planes bit-packed LSB-first (bit k mod 8
of byte k div 8), pad bits the plane's fill bit; interleaved bool
values are single bytes 0x00/0x01, strict, verifier-checked —
ADR-0038 lifted ADR-0037's mixed-interleaved prohibition after
maintainer challenge (int8-masquerade type erasure outweighed the
uniformity clause). The outcome is option (c) below, overturning its
inline rejection: ADR-0038 answers the implementer-surprise objection
(representation keys on layout alone, and decode paths branch
entirely on layout regardless).
- **Why:** ADR-0012 requires one uniform boolean representation across both
  layouts; the Confirm is which. Bit-packing is 8× smaller but complicates
  interleaved sample framing; byte-per-bool is simple but bloated, and "any
  nonzero is true" vs "must be 0/1" is a two-encodings trap.
- **Options:** (a) Bit-packed LSB-first in both layouts (bit position =
  in-tile sample index mod 8; pad bits = fill bit); interleaved samples
  place the bool's bit within a per-sample packed field — needs careful
  framing text. (b) One byte per bool everywhere, values restricted to
  0x00/0x01, others invalid. (c) Packed in planar, byte in interleaved —
  the asymmetry maximizes implementer surprise; rejected.
- **What settles it:** Whether bool channels in interleaved layers are a
  real pattern. Leaning: (a), per ADR-0012's recommendation — unless
  interleaved bools prove rare enough that (b)'s simplicity wins. Decide
  during the tile-serialization draft with vectors for both candidates in
  hand.

## E. Codecs and filters

### Q-E1. Codec wrapper pinning. [Resolved → ADR-0039; its zstd half reopened by Q-E4 and re-closed by ADR-0088]
**Resolution:** deflate = raw RFC 1951; zstd = one minimal-strict
RFC 8878 frame (dictionary and content-checksum flag forbidden,
reject-tile; content-size allowed, cross-checked against decoded
size); lz4 = one raw block (decoded size ≤ 0x7E000000). Codec IDs 1–4
sequential; every wrapper field the container already carries was
struck or pinned inert — zstd's default-emitted content-size is
retained on adoption grounds, cross-checked, never an allocation
source.
- **Why:** Each codec must be pinned to one exact external definition
  (ADR-0009); the open choices are at the framing layer, decided by one
  test — does the wrapper add anything the container doesn't already carry?
- **Options:** deflate: raw RFC 1951 vs zlib RFC 1950 (zlib adds an Adler-32
  redundant with index checksums — leaning raw; note DecompressionStream
  supports `deflate-raw`). zstd: RFC 8878 frame with dictionaries forbidden
  vs allowed-by-registry-extension later. LZ4: frame format (self-describing,
  duplicates lengths the index already has) vs raw block with
  spec-declared bounds — leaning raw block.
- **What settles it:** For each codec, enumerate what the wrapper provides
  (length, checksum, magic) and strike it if the container provides it;
  verify the "tile decodable from stored bytes + layer metadata alone"
  sentence still holds.

### Q-E2. Shuffle filter on interleaved layers. [Resolved → ADR-0039]
**Resolution:** permitted — stride = sample stride Q; measured 28–33%
deflate-size reduction on representative interleaved data, comparable
to the planar win. One stride rule (planar = element size, interleaved
= Q); packed bool planes degenerate to the identity, so no forbidden
cell exists.
- **Why:** Byte-shuffle needs an element stride. Planar tiles are
  homogeneous (stride = channel element size — trivially correct).
  Interleaved tiles mix element sizes, so the stride is either the full
  sample tuple (benefit unproven) or the filter is simply not permitted
  there.
- **Options:** (a) Shuffle permitted only on planar layers. (b) Permitted on
  interleaved with stride = sample size. (c) Add bitshuffle as a second
  filter — defer; more surface.
- **What settles it:** Compression-ratio measurements on representative
  interleaved data; if the benefit doesn't materialize, (a) with a
  writer-MUST-NOT / reader-MUST-reject cell in the filter column of
  ADR-0012's validity table.

### Q-E3. Tile-index encoding: raw fixed-size vs columnar-compressed. [Resolved → ADR-0024]
**Resolution:** raw 20 B entries + per-2¹⁶-entry segment CRC array;
columnar reserved via the index-encoding enum.
- **Why:** The single largest afternoon-readability vs efficiency tradeoff
  in the format. Raw fixed-size entries are mmap-able, random-access, and
  trivially specified but large (tens of MB at 10⁶ tiles); PMTiles-style
  struct-of-arrays with delta+varint+compression reaches ~1–2 bytes/tile but
  must be decoded wholesale and adds a second encoding to implement. The
  outcome decides Q-A3's achievable budget.
- **Options:** (a) Raw fixed-size entries (offset u64, length u64, checksum
  u32), no compression. (b) Columnar: separate offset/length/checksum
  columns, delta+varint on offsets/lengths, whole index compressed with the
  internal metadata codec (checksum column left raw — incompressible).
  (c) (a) plus an aligned-layer optimization: implicit offsets
  (`k × stride`), exceptions listed — smallest for aligned layers, but a
  third encoding.
- **What settles it:** The Q-A3 size model with real numbers, and whether
  any consumer needs O(1) *entry* access without decoding the index (vs
  O(1) index *fetch*). Leaning: start with (a) for the draft; adopt (b)
  only if the size model shows (a) breaking the discovery budget at
  realistic scale.

### Q-E4. Are a codec wrapper's pinned fields enforced, ignored, or advised? [Resolved → ADR-0088]
**Resolution:** all four stay normative reader checks; T19–T22 and R4's
sixteen instances are unchanged, and the register holds at 121 conditions
over 277 instances. Two measurements and the cohort decided it. libzstd
already rejects a lying `Frame_Content_Size`, a nonzero `Dictionary_ID`
without a dictionary, and a set `Content_Checksum_flag` over a wrong
checksum, while accepting an oversized `Window_Size` — so the only field
enforcement adds is the one every option kept, and declaring the other
three ignored would make a file conforming that no `ZSTD_decompress()`
reader can serve. **Two lines of the triage table below are wrong and the
measurement is the record:** the content-checksum flag does not "break
nothing", and the content-size field is not "safe to ignore". The adoption
premise is also wrong — one-shot `ZSTD_compress()` emits a conforming
frame at every size tested with no configuration, because
`Single_Segment_Flag` makes `Window_Size` equal `Frame_Content_Size` equal
the decoded size; the measured friction is an unpledged streaming
encoder, which breaks **T21 alone**. The cross-codec reason is that T19,
T20 and T22 are zstd's T15 and T23 — strike the wrapper where it is
separable, pin its fields where it is not. What the entry got right is the
defect class, which the same ADR fixes at its source: §18.2's carry-over
of `[R-COD-06]` was a closed enumeration and is now exhaustive by
construction.

**Question:** Q-E1 struck or pinned every zstd frame-header field the
container already carries. It did not ask *how* the pin is enforced. Today each
is a normative reader check with a register row. Should the hygiene fields
instead be **declared ignored** — a reader MUST NOT act on them, and a
nonconforming value is no violation — with the checks moved to a
recommended-but-optional verifier appendix?

- **Why it matters.** Three costs, one benefit, and a defect class.

  *Adoption.* A TARN writer today cannot use a stock `ZSTD_compress()`: it must
  configure the encoder to suppress the content-checksum flag and control the
  window. Q-E1 already conceded this once in the other direction — zstd's
  content-size is "retained on adoption grounds" — so the principle is
  established, only its reach is open.

  *Spec surface.* §21.4 carries eleven codec rows, the largest cluster in the
  register, plus their instances and vectors. The cost scales with a codec's
  *contradictable header fields*, not with codecs as such — zstd is expensive
  because its header restates four things TARN fixes elsewhere.

  *A defect class.* Two byte-level defects in three rounds came from this
  surface (rounds 21 and 22, ADR-0085 and ADR-0087). Both had the same root:
  a field left **unconstrained** makes file conformance depend on whether *a
  decoder* notices, which `[R-CNF-02]` forbids. "Ignored" removes that
  dependence; "unconstrained" is what creates it. `[R-MTA-10]` already makes
  exactly this move for experimental encodings.

  *What is not on the table.* deflate and lz4 are already headerless — Q-E1
  chose raw RFC 1951 and one raw LZ4 block. zstd's header is not separable in
  practice: `ZSTD_decompressBlock` is an advanced API requiring caller-managed
  window and dictionary state, so mandating headerless zstd would put TARN
  readers outside `ZSTD_decompress()`. The question is only about the fields.

- **The fields do not cost the same.** Any option must triage them:

  | field | character | if unenforced |
  |---|---|---|
  | Dictionary_ID | decoder needs a dictionary it lacks | decode fails anyway — T25 instead of T19, losing diagnostic specificity only |
  | Content_Checksum_flag | redundant with the entry crc | costs a few bytes; breaks nothing |
  | `Frame_Content_Size` | declares decoded length; never an allocation source | **safe to ignore, and better than today** |
  | **Window_Size** | drives decoder **memory allocation** | **not hygiene** — §22.2's decompression-bomb defence rests on it |

- **Options & tradeoffs:**
  (a) **Status quo** — all four enforced, four rows plus R4's instances. Highest
  determinism and best diagnostics; highest adoption cost and the largest
  ongoing defect surface.
  (b) **Ignore the three hygiene fields, keep Window_Size normative.** Removes
  ~3 rows, their instances and vectors; a writer may use a stock encoder;
  the bomb defence is untouched. Costs diagnostic specificity, and Appendix G's
  byte-reproducibility gets harder because "encoder defaults" vary by version.
  (c) **(b) plus a non-normative appendix** of recommended verifier checks.
  `[R-CNF-12]` already supplies the machinery — a SHOULD deviation "does not
  bar certification" and is reported as an advisory — so this needs no new
  concept. It cannot carry Window_Size, since an advisory cannot hold a
  resource-safety guarantee.
  (d) **Ignore all four**, replacing the window rule with a reader-side
  allocation cap. Maximal simplification, but relocates a security check rather
  than removing it, and the cap is itself a rule with a row.

- **What settles it.** Apply Q-E1's own test one level up: for each field, does
  *enforcing* it protect anything the container does not already protect? The
  entry crc covers integrity; the layer's declarations fix decoded size; only
  the window governs an allocation TARN cannot otherwise bound. Then price the
  answer honestly — count the rows, instances and vectors each option removes,
  and check Appendix G still closes its degrees of freedom without pinned
  encoder settings.

- **Scope if adopted:** §17.2 (`[R-COD-06]`), §18.2 (`[R-MTA-09]`), §21.4's
  T-rows, §21.5's R4, §22.2, Appendix G, and the corpus. Reopens Q-E1's zstd
  half and would supersede parts of ADR-0039, ADR-0085 and ADR-0087. Wants its
  own cycle, not a cleanroom round's repair slot.

## F. Metadata and naming

### Q-F1. User-metadata encoding. [Resolved → ADR-0045]
**Resolution:** UTF-8 JSON (RFC 8259), restricted — top-level object,
no NaN/infinities, no duplicate keys, keys sorted by UTF-8 bytes;
byte-identity across writers explicitly not promised, consistent with
R-CNF-05. Granularity was already fixed by ADR-0032.
- **Why:** ADR-0015 (Proposed) needs its Confirm items resolved: JSON vs
  canonical CBOR, and per-layer granularity. JSON is human-inspectable and
  ubiquitous but has no native binary values and needs explicit
  determinism rules; canonical CBOR (RFC 8949 §4.2) has determinism and
  binary values built in but costs afternoon-readability and a dependency.
- **Options:** (a) UTF-8 JSON, sorted keys required, numbers restricted
  (integers + finite doubles; NaN/±Inf forbidden — bit-exact values belong
  in structural fill/stats records, not user metadata). (b) Canonical CBOR.
  (c) Custom TLV — most spec text; rejected unless both fail. Granularity,
  separately: (d) file-level document only vs (e) file + optional per-layer
  documents.
- **What settles it:** Whether "readable in an afternoon" tolerates a
  normative CBOR reference; whether any user-metadata case genuinely needs
  binary values. Granularity: whether per-layer metadata needs appear in
  target workloads (multi-resolution pyramids suggest yes). Leaning: (a)
  with (e).

### Q-F2. Name rules. [Resolved → ADR-0027]
**Resolution:** length-prefixed UTF-8 MUST; names non-empty, ≤ 255 bytes,
no U+0000–U+001F; raw-byte comparison with SHOULD-NFC advisory; uniqueness
per scope MUST. Encoded as spec §4.6.
- **Why:** Names (layers, dimensions, channels, metadata keys) are lookup
  keys in a binary format; duplicate names are pure ambiguity, and
  unvalidated strings are a parser hazard and a terminal-escape hazard.
- **Options / leanings:** Valid UTF-8 MUST (invalid → reject-scope);
  non-empty; byte-length cap (255 proposed); no NUL or C0 controls;
  uniqueness within scope MUST for writers *and* readers (duplicate →
  reject-scope). Open sliver: Unicode normalization — full NFC is heavy;
  leaning raw-byte comparison + a SHOULD-be-NFC advisory, stated
  explicitly so no reader invents case-folding.
- **What settles it:** One consequence-analysis paragraph during drafting;
  the limits land in the spec's limits table (Q-H1).

### Q-F3. Dimension coordinate/unit metadata: core or keys? [Resolved → ADR-0045]
**Resolution:** standardized keys — `tarn.axes` carries the affine
mapping (unit, origin, step) per dimension; the core stays neutral and
the extension mechanism is the promotion path.
- **Why:** Scientific users want axis semantics (units, affine coordinate
  mappings, spectral bands); image users don't. Core fields commit every
  reader to parsing them forever; GeoTIFF and EXIF demonstrate that domain
  semantics thrive as layered registries over a neutral core.
- **Options:** (a) Standardized user-metadata keys (ADR-0015's registry) —
  zero core surface, adequate for affine axes, promotable later via the
  extension mechanism. (b) Core dimension fields — first-class but
  permanent. (c) A registered extension record — middle ground.
- **What settles it:** Concrete demand from a real consumer during drafting.
  Leaning: (a) now; the extension mechanism (Q-G2) is the promotion path.

## G. Extensibility, versioning, identity

### Q-G1. Version mechanism. [Resolved → ADR-0025]
**Resolution:** trailer major/minor with additive-only minors, incompat/
ignore flag lanes, and the cross-major forever clause.
- **Why:** Version fields and capability flags solve different problems.
  PNG evolved for 30 years with no version field at all — per-chunk
  criticality bits carried everything — while formats with version fields
  but no flags ended up forking (BigTIFF). A version field only protects
  anyone if the project actually bumps it, so the mechanism must make
  "when to bump" unambiguous.
- **Options:** (a) Binary major/minor in the discovery structure with a
  hard contract — unknown major ⇒ MUST reject; unknown minor ⇒ MUST
  proceed (minor releases are additive-only by policy) — *plus* per-record
  must-understand flags (Q-G2) for feature-level negotiation; the version
  bump is reserved for outer-framing changes only. (b) Flags only.
  (c) Version only — the fork trap.
- **What settles it:** Essentially decidable now; (a) is the leaning. The
  ADR must include the degradation story for each anticipated feature
  ("an old reader sees X"), plus the companion rule: known fixed structures
  never grow — a size mismatch is a validity error, not a newer version.

### Q-G2. Must-understand / preserve-on-edit flag design. [Resolved → ADR-0026]
**Resolution:** 24-byte record header with MU/PE bits, extent slot,
no-embedded-offsets rule, and per-class semantics table.
- **Why:** The single most load-bearing forward-compat mechanism. PNG's
  property bits are proven but its case-encoding trick misled implementers
  into locale-dependent case tests; the refinement worth adding is a banned
  list — positions that may never be marked ignorable (type, geometry,
  codec, linearization).
- **Options:** (a) Two literal flag bits per directory record —
  MUST_UNDERSTAND and PRESERVE_ON_EDIT, tested bitwise. Unknown record with
  MUST_UNDERSTAND set ⇒ reject exactly the scope it governs (an unknown
  critical record inside layer B makes layer B unreadable, never the file);
  unknown ancillary ⇒ ignore; updaters preserve or drop per the preserve
  flag; ancillary records may not depend on other ancillary records;
  reserved flag bits are ignore-don't-error. (b) A richer four-axis flag
  set — private/experimental concerns are better handled by ID ranges
  (Q-G3).
- **What settles it:** Walk the updater stories (re-tagger, appender,
  compactor) against each design; leaning (a).

### Q-G3. Registry and ID-space design. [Resolved → ADR-0044]
**Resolution:** every numeric space partitioned assigned / reserved /
experimental (≥ 0x8000 for u16, ≥ 0x80 for u8), collected in §10.2;
experimental values carry no collision protection and MUST NOT ship;
registration requires a security review and, for record types, an
MU/PE justification; the registry is a machine-readable file in this
repository.
- **Why:** Extension governance fails in two directions: a registry that
  dies (TIFF's registration mailbox was decommissioned; its "reusable"
  private range guaranteed collisions) or one with so much process nobody
  registers. PNG's balance — registry-governed public space, syntactically
  distinct private lane, and "unregistered public IDs SHALL NOT ship in
  released software" — is the model.
- **Options:** (a) Numeric enums for hot-path IDs (codec, filter, type,
  record type) each with a reserved experimental range (≥ 0x8000);
  string-keyed namespaced user-metadata keys; the registry is a
  machine-readable file in this repo; new registrations get security and
  IPR review; new must-understand record types discouraged unless
  necessary. (b) String keys everywhere — no collisions, but fixed-width
  numeric IDs belong on hot paths.
- **What settles it:** Decidable at drafting; (a) is the leaning.

### Q-G4. Signature bytes, trailer magic, MIME type. [Resolved → ADR-0029]
**Resolution:** front `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes; trailer
magic `8A 4E 52 41 54 0D 0A 1A` ("NRAT"); application/vnd.tarn.
- **Why:** ADR-0002's Confirm: bare ASCII `TARN` vs a hardened 8-byte
  signature. A tail-anchored design (Q-A1) also needs a *distinct* trailer
  magic so a scan-back can never false-positive on the front signature.
- **Options:** Front: `54 41 52 4E` bare, vs `89 54 41 52 4E 0D 0A 1A`
  hardened (high-bit byte catches 7-bit stripping; CR LF catches
  line-ending translation; ctrl-Z stops console display). Trailer: a
  distinct 8-byte constant. MIME: `application/vnd.tarn`.
- **What settles it:** One ADR confirming exact byte values against the
  corruption classes, plus the early-validation chain (signature →
  fixed-field sanity → trailer magic → trailer checksum) before any range
  requests. Leaning: the hardened signature (which still contains ASCII
  "TARN"), per the transport-corruption argument in ADR-0002 and the
  research doc.

## H. Limits and security

### Q-H1. Normative constants vs implementation-declared minimums. [Resolved → ADR-0043]
**Resolution:** minimum guarantees, not caps — rank 32, channels 4096,
entry_count 2³² (the segment-CRC-array knee), layers 65,536, decoded
tile 256 MiB, user-metadata document 16 MiB, zstd window 8 MiB; a file
exceeding any row stays conforming and a reader refusing it MUST say
"resource", not "invalid". Hard caps remain only where a structure,
an external format, or the value domain forces one.
- **Why:** Limits that live only in implementations mean "valid file"
  differs by reader. The alternative pattern (RFC 8259): implementations
  MAY set limits, but the spec names minimum guarantees writers can rely
  on. Overflow is not open: all index math MUST be overflow-checked and
  products validated ≤ 2⁶³−1.
- **Options:** Per limit — {max rank, max tiles/layer, max name length, max
  user-metadata size, max layers}: (a) hard spec constant (testable,
  arbitrary) vs (b) "readers MUST accept at least N" minimums.
- **What settles it:** Decide per-limit during the security-section draft;
  each chosen number gets an at-limit conformance vector.

### Q-H4. Which register rows reach a file declaring a foreign major, and can detection order settle it? [shaping]
**Question:** §21.2's preamble decides which rows reach a file declaring a
format major other than 1 by **procedural priority** — "§6.2 puts the
version gate ahead of every check but the trailer magic and the trailer
CRC, so such a file is refused on capability grounds first." But
`[R-RDR-02]` fixes only the *latest* detection point and then says "A
reader MAY detect any violation earlier (`[R-CNF-12]`)". If detection
order is a reader's option, no row's reach can be established by it.
- **Why it matters.** Round 23 reported that `[R-CNT-27]`'s 128-byte
  floor has no position in §6.2's order, so a short foreign-major file's
  verdict is open. ADR-0090 answered it by adding F5 to the preamble's
  exception list with an ordering warrant — **and the audit before round
  24 falsified that warrant three ways**: `[R-CNT-27]` carries no ordering
  language; the physical claim ("no trailer to read a magic, a CRC or a
  version from") is false for every file of 64 to 127 bytes, the trailer
  being 64 bytes; and `[R-RDR-02]` makes the priority permissive anyway.
  ADR-0091 reverted it. The original question is therefore still open —
  **and the audit showed it reaches the preamble's existing four rows
  too**, since they rest on the same permissive ordering.
- **Options:** (a) Make §6.2's order a MUST for the gates it names, so
  priority is a fact and the preamble's reasoning is sound. Narrowest, but
  it constrains readers `[R-RDR-02]` deliberately leaves free.
  (b) Decide reach by *what a rule's subject is* rather than by when it is
  checked — `[R-CNT-24]`'s across-major fields already supply that test for
  the four, and F5's subject, a physical size, is fixed across majors too.
  (c) State that a file below 64 bytes declares no readable major and is
  outside the premise, as F18 is, leaving 64–127 to the gate.
- **What settles it:** whether two conforming readers can differ on the
  verdict for one short foreign-major file. If they can, the preamble is
  deciding something the document leaves open, and (a) or (b) is owed.

### Q-H2. Does any row bound a *stored* quantity, and do §21.9's rows compose? [shaping]
**Question:** §21.9's table bounds a tile's decoded size (256 MiB), a
document's decoded size (16 MiB) and a frame's `Window_Size` (8 MiB) —
every one a *decoded* or *declared* quantity. **Nothing bounds a stored
extent's length.** Its only constraints are §15.3's `length ≥ 1`,
`length ≤ 2⁶³ − 1` and `offset + length ≤ F − 64`. §19.4 step 5 obliges a
reader to fetch the whole extent and verify its CRC *before* decoding, so
mandatory per-tile I/O is bounded by nothing but the file length. The
table also never says what its rows bound **collectively**.
- **Why it matters.** `[R-CNF-10]` puts every limit affecting which files a
  conforming reader accepts in this specification and never only in an
  implementation. A reader that declines a 4 GiB stored extent for a 1 KiB
  tile has no row to decline it under, and `[R-CNF-03]`'s acceptance duty
  runs to "a conforming file none of whose values exceeds those
  guarantees" — a phrase that ranges over the rows, and the stored length
  is in none of them. Round 23 found this from two directions
  independently (reader-01, adversary-04).
- **Options:** (a) Add a stored-extent row to §21.9, with a figure.
  (b) Leave it, and say in §21.9 that the table bounds decoded and
  declared quantities only, so a reader's I/O budget is its own and no
  refusal on it is a §21.9 refusal. (c) Bound the stored length against
  the decoded size by a ratio, which reintroduces the expansion bound
  §17.2's closing Note deliberately refuses.
- **What settles it:** whether a reader can be made to fetch unbounded
  bytes for a bounded tile — construct it — and whether (b) leaves
  `[R-CNF-10]` satisfied or merely restated.

### Q-H3. Is a user-metadata document's nesting depth bounded? [shaping]
**Question:** RFC 8259 §9 expressly permits an implementation to limit
nesting depth. This specification imports RFC 8259 as the document's
definition and pins four other RFC 8259 freedoms — top-level type,
byte-order mark, number range, duplicate-key identity — and pins key
length at 255 bytes, which §21.9 calls one of only two hard limits
"chosen here". It states no depth bound anywhere.
- **Why it matters.** Round 23's adversary built a conforming 1.14 MiB
  document of `{"a":` ×200,000 + `1` + `}` ×200,000: well-formed JSON, a
  top-level object, one finite number, sorted at every depth, inside
  §21.9's 16 MiB row. A recursive-descent reader meets a stack no
  declaration bounds. All three triage passes and the refute phase agreed
  it is **not** byte-level — R7's condition is "not well-formed JSON",
  and a 200,000-deep object is well-formed — so the emittable set does not
  move. It is a resource question, and `[R-CNF-10]` is the reason it
  cannot simply live in implementations.
- **Options:** (a) A §21.9 minimum-guarantee row for nesting depth, which
  is the shape `[R-CNF-10]` asks for and costs one row and its
  arithmetic. (b) A hard limit in `[R-ERR-05]`, like the 255-byte key.
  (c) Nothing, with a Note recording that depth is a reader's own
  resource bound and its refusal a resource limit under `[R-ERR-04]`.
- **What settles it:** whether a depth refusal is distinguishable from
  the size refusal §21.9 already licenses; if it is not, (c) costs
  nothing and (a) adds a row for a case another row already reaches.

## I. Process

### Q-I4. Does R8 carry two instances or four? [shaping]
**Question:** R8 registers "a non-finite number, in any form", which
`[R-MTA-04]` states as two alternatives — a magnitude whose binary64
interpretation overflows (`1e400` is the ordinary case) and the bare
tokens `NaN`, `Infinity`, `-Infinity`. The row states two instances, one
per placement. Should it state four?
- **Why it matters.** §21.1 enumerates alternatives that "give the
  condition materially different shapes", and these plausibly do: `1e400`
  is syntactically valid JSON needing a decimal-to-binary64 conversion and
  an overflow test, while a bare token is one RFC 8259 does not admit at
  all, which a strict parser rejects before any numeric rule runs.
  §18.2 says so itself — "which RFC 8259 does not admit and some parsers
  accept regardless".
- **What has been tried, and why this is a ledger entry and not a repair.**
  Round 23 reported it (register-01). **Two attempts to justify keeping two
  instances have both been wrong**, each caught by the audit that followed:
  ADR-0090 cited a "§21.1 distinguishability test" §21.1 does not state;
  ADR-0091 cited `[R-VEC-02]`, which resolves non-isolable conditions the
  *opposite* way — "the entry records every row the file exercises and says
  which it was built for". ADR-0092 removed the warrant rather than
  inventing a third. The condition cell now states the two alternatives and
  claims nothing about their instance count.
- **Options:** (a) Split to four instances — 277 → 279, two new vectors,
  each co-attributed to R7 under `[R-VEC-02]`'s non-isolable clause, since
  a bare-token document is not well-formed JSON either. (b) Keep two, with
  a ground that survives audit — which nobody has yet produced. (c) Decide
  that a condition whose second alternative cannot be exhibited in
  isolation states one instance, as a general rule stated in §21.1 rather
  than argued per row, which would also reach L50's held fourth instance.
- **What settles it:** whether `[R-VEC-02]`'s co-attribution clause makes
  the bare-token case buildable as a vector. If it does, (a) follows and
  the register grows by two; if §21.1 needs a general rule instead, (c) is
  the cheaper fix and closes a standing debt with it.

### Q-I3. Does `[R-VEC-04]`'s intact-sibling rule reach ignore-record vectors? [shaping]
**Question:** `[R-VEC-04]` requires an intact sibling for vectors of two of
the four outcome classes — reject-layer and reject-tile — then gives a
rationale that reaches all of them: "Without the sibling a vector cannot
distinguish a reader that scopes its refusal from one that rejects the
file entire, because `[R-CNF-12]` permits the latter for any nonconforming
file and every vector built from §21's register is nonconforming."
- **Why it matters.** "Every vector built from §21's register" includes
  §21.5's ten ignore-record rows, and §21.5 is explicit that they are
  violations. So the rationale covers 48 ignore-record vectors the
  requirement's own range excludes. Either the range is too narrow or the
  rationale overclaims, and this is `[R-VEC-04]`'s recorded
  damaged-scope-content debt seen from the other side.
- **Options:** (a) Widen the requirement to ignore-record, which adds an
  intact sibling to 48 vectors and is corpus work. (b) Narrow the
  rationale, saying why scoping is only testable where a scope narrower
  than the file exists — a record is skipped, not scoped. (c) Leave both
  and record the asymmetry in §24.
- **What settles it:** whether a reader that rejects the file entire on an
  ignore-record violation is distinguishable from one that skips the
  record, *without* an intact sibling. If the record's absence is itself
  the witness, (b) is right and costs nothing.

### Q-I1. Reproducible-writer profile. [Resolved → ADR-0047]
**Resolution:** a non-normative Appendix G — codec 1 or a named codec
build (byte-identity across implementations is unattainable for
compressed tiles), file_id from a content hash, tiles in disk-ordinal
order, records in a fixed order, one generation. Core writer
conformance stays semantic.
- **Why:** Content-addressing and build reproducibility want byte-identical
  output for identical input, but core writer conformance is deliberately
  semantic (ADR-0003) — promising canonical bytes in the core would
  constrain every writer forever.
- **Options:** (a) A non-normative appendix profile: fixed codec parameters,
  defined padding, sorted records, deterministic metadata serialization.
  (b) Nothing in v1.
- **What settles it:** Demand; costs one appendix.

### Q-I2. Cleanroom-test protocol details. [Resolved → ADR-0034]
**Resolution:** four parallel roles (reader/verifier/writer/quiz),
spec-text-only access, finding taxonomy with mandatory disposition;
piloted on the container round.
- **Why:** The drafting process uses fresh-context implementer tests
  (an agent gets only the spec text and must describe a conforming reader,
  answer byte-level questions, and list ambiguities). Batch size, pass
  criteria, and whether the cleanroom agent also writes a toy decoder
  against vectors need pinning before the first round.
- **Options:** Per-section vs per-part batches; pass = zero byte-level
  ambiguities vs scored rubric; toy-decoder round only for the container
  spine.
- **What settles it:** A pilot round on the first drafted part; the refined
  protocol is then recorded in PLAN.md and AGENTS.md.
