# Lessons from Reference Formats

This document distills what five reference specifications — W3C PNG (Third Edition), TIFF 6.0, Zarr v3 (with its sharding-indexed codec), PMTiles
v3, and QOI together with RFC 2119/8174 (BCP 14) — teach about designing and writing a single-file, tiled, N-dimensional array format. It is
**non-normative**: nothing here binds a TARN implementation. Its purpose is to serve as the shared evidence base that TARN's ADRs and spec sections
cite, so that design decisions ("why little-endian only?", "why checksums in the tile index?") can point at concrete precedent instead of re-arguing
from scratch. Each lesson is stated as *lesson → application to TARN*, with spec-section citations where the source material provides them.

---

## W3C PNG (Third Edition) — the gold standard

PNG is the most complete model of how a binary container spec should be *written*: chunk model, criticality semantics, conformance classes, security
analysis, and an extensibility story that has survived thirty years without a version field.

### Chunk model and criticality

- **Forward compatibility is machine-decidable from the record itself.** Every PNG chunk type carries four property bits — ancillary, private,
  reserved, safe-to-copy (PNG §5.4) — so a reader knows what to do with an unknown chunk without any registry lookup. → TARN should give every
  directory record and metadata field explicit handling flags (at minimum MUST_UNDERSTAND and PRESERVE_ON_EDIT) as literal bits in the record
  header. This is the mechanism that lets TARN add codecs, index types, and tag structures without breaking old readers.
- **But don't copy the case-bit trick.** Encoding flags in identifier letter case was elegant; in practice implementers reached for locale-dependent
  case functions and the spec had to warn "testing whether a character is uppercase or lowercase is inefficient, and even incorrect" (PNG §13.5).
  Use boring, bitwise-testable flag bits.
- **Unknown-thing behavior is specified normatively, per class, per role.** Unknown ancillary chunks are safely ignored; unknown critical chunks
  must be reported; reserved-bit chunks are explicitly *not* errors, because "some future version could define a meaning" (PNG §5.4, §13.2). → TARN
  needs an explicit table: for each extension point × each role (reader, verifier, updater), a SHALL-level outcome — reject-file, reject-layer,
  reject-tile, ignore-record, or preserve-verbatim. Reserved-but-set values are unknown, never corruption.
- **Criticality is task-relative.** PNG admits its critical/ancillary split targets "extracting a viewable image" and is "not necessarily relevant
  to every conceivable decoder" (PNG §4.10, §13.1). → Scope must-understand to data the reader actually touches: an unknown codec on layer B must
  not prevent reading layer A, and a metadata-only tool must be able to list layers in a file whose payloads it cannot decode.

### Editors as a first-class role

- **Tools that modify files they don't fully understand need precise rules.** PNG's safe-to-copy bit, the mandate that editors terminate on
  unrecognized critical chunks, and the rule that "it is not permissible for ancillary chunks to depend on other ancillary chunks" (PNG §14.2) make
  editing well-defined. → TARN files will be appended to, compacted, and retagged; define an *updater* conformance class with explicit preserve/drop
  rules, and forbid optional records from depending on other optional records.
- **Ordering freedom is what makes editing sound.** "Decoders shall not assume more about the positioning of any ancillary chunk than is specified
  by the chunk ordering rules" (PNG §14.3.2). → Make TARN's metadata directory order-independent by fiat; enumerate every positional guarantee
  explicitly. This keeps append-in-place and compaction sound.
- **Don't over-trust editors either.** PNG's machinery is sound, but real-world image editors discard unrecognized information anyway. Keep
  preservation rules few and simple, so naive rewriters produce valid (if stripped) files rather than corrupt ones.

### Integrity and its limits

- **PNG's CRC excludes the length field, and the spec documents the consequence:** a decoder that skips CRC checks can "get out of step and
  misinterpret subsequent data" on a bad length (PNG §5.3, §13.2), and there is no whole-file checksum at all. → No TARN offset or length field may
  sit outside checksum coverage. Tile checksums live in the index; the index and headers are themselves checksummed, so framing metadata is verified
  before any payload I/O — including by partial HTTP-range readers.
- **Checksums are anti-corruption, not security.** PNG keeps transport integrity and content trustworthiness as distinct concepts (PNG §13.3, §5.5).
  → TARN's "integrity by default" claim needs a threat-model paragraph: CRCs detect accidental corruption, not tampering; recommend detached signing
  for authenticity. Geometry fields (dims, tile sizes, offsets) must be checksum-verified before being used for allocation or seeks.
- **Engineer the magic signature against real transport-corruption classes.** PNG's eight bytes detect 7-bit stripping, CRLF/LF translation, and DOS
  ctrl-Z truncation (PNG §5.2), and §13.1 chains signature → header sanity checks. → TARN's magic should include a high-bit byte, embedded CR LF,
  and ctrl-Z — not just ASCII — and the spec should state the early-validation chain a reader performs before issuing range requests.

### Conformance, errors, extensibility

- **A real conformance section with per-role checklists.** PNG §15 gives a blanket normativity rule ("all authoring guidelines, diagrams, examples,
  and notes... are non-normative. Everything else is normative"), BCP 14 boilerplate, stated objectives ("eliminating arbitrary subsets of, or
  extensions to, this specification"), and testable conditions for four classes: datastream, encoder, decoder, editor. → Copy this structure
  wholesale: file, writer, reader, updater. The "no arbitrary subsets" objective is what prevents ecosystem fragmentation — a conforming TARN reader
  handles *all* mandatory codecs and layouts or it isn't a TARN reader.
- **Error handling gets its own normative section with a taxonomy.** PNG splits transmission errors from syntax errors, mandates early detection and
  graceful failure, and distinguishes fatal from recoverable per situation (PNG §13.1, §13.2). → TARN needs the same: taxonomy (corruption /
  structural / semantic), earliest-detection points, and fatal-vs-recoverable per case.
- **Known structures never grow.** "Future extensions... will not add new fields to existing chunks; instead, new chunk types will be added" — so an
  unexpected chunk length is an error, not a newer version (PNG §13.2). → Fixed TARN structures have exact sizes; readers reject size mismatches;
  all growth flows through new keyed records with handling flags.
- **Enumerate extension points exhaustively and briefly.** PNG §4.11 lists exactly three; everything else is closed. → A one-page "Extension points"
  section (codec IDs, filter IDs, channel data types, record types, tag keys) tells an implementer the complete forward-compat surface.
- **Registry with an anti-squatting rule and a private lane.** Public chunk types "SHALL not be used in publicly available software or datastreams
  until defined"; private chunks get a syntactic namespace and a companion registry (PNG §5.4, §12.10.1, §14.1). → Even a small format needs: a
  registry file in the spec repo, syntactically distinct private/experimental ID ranges, the no-shipping-unregistered-IDs rule, and "new
  must-understand record types are discouraged unless necessary."
- **Security and privacy considerations are concrete, not generic.** PNG names chunk payloads as arbitrary content, data after IEND, hostile control
  characters in text, out-of-file Exif pointers, and 2^31-byte allocation risks (PNG §13.3); privacy separately documents crop-by-header-rewrite and
  alpha-zero "redaction" leaving recoverable data (PNG §13.4). → TARN's analogs: tile offsets aliasing or escaping the file; decompression bombs
  (TARN's structural advantage: decompressed tile size is fully determined by declared geometry — mandate allocate-from-geometry); dimension-product
  overflow; unreferenced byte ranges as smuggling channels; and the privacy trap that logical deletion (shrinking a layer, dropping a directory
  entry) is not erasure — define compaction as the only true removal.

### PNG's weaknesses confirm TARN's bets

- **No random access:** all IDAT chunks form one continuous zlib stream, so partial decode means sequential decompression from the start; Adam7
  interlacing is the bolted-on workaround (PNG §10). → Validates independently compressed tiles addressed by an index. Guard the property jealously:
  any cross-tile compression state reintroduces sequential dependencies. Slabs are an I/O grouping, never a compression context.
- **Metadata accretion when orthogonal properties are baked into type identity:** tEXt/zTXt/iTXt triplication; the gAMA→sRGB→iCCP→cICP
  color-description pile-up with retrofitted precedence rules (PNG §11.3). → Design TARN's tags once — UTF-8 always, structure always available,
  compression orthogonal to identity — and give any two overlapping optional records a normative precedence rule on day one.
- **Versionless evolution works:** PNG has no version field anywhere; the Third Edition added APNG, cICP, and eXIf while 1996-era decoders still
  display every conforming file. → Prefer capability flags over a monolithic version integer, and design a per-feature degradation story: what does
  an old reader see when a new feature is present?

## TIFF 6.0 — the cautionary tale: a catalog of ambiguity classes

TIFF is the indispensable negative example: a format whose flexibility, frozen spec, and missing error model produced thirty years of "works in
Photoshop, breaks in libtiff." Its failures sort into named ambiguity classes, each with a rule TARN must follow.

### Class 1: Optional-everything with no enforced baseline

TIFF splits into Baseline and Extensions, but a file carries no capability marker — a tiled, LZW-compressed, planar file is fully spec-legal and
fully baseline-unreadable, with no way to know before parsing. "Where there are options, TIFF writers can use whichever they want. Baseline TIFF
readers must be able to handle all of them": writer freedom systematically converted into reader burden. **Rule:** exactly one mandatory conformance
profile; any feature a reader may legitimately lack must be advertised in the metadata directory with must-understand semantics, so a lacking reader
fails with a defined error *before* returning data.

### Class 2: Underspecified field interactions

TIFF defines tags individually and leaves the cross-product to inference: PlanarConfiguration × SamplesPerPixel edge cases; RGB with 4 samples and
no ExtraSamples tag (is sample 4 alpha? associated?); CCITT data that "is self-photometric" while PhotometricInterpretation "also purports to define
what is white" — two sources of truth; an outright internal contradiction on old-JPEG tile height (one MCU vs. multiple of 16); strips and tiles
both present with no precedence rule. **Rule:** for every interacting field set (channel layout × channel count × codec × tile geometry × fill), a
normative validity table over the full cross-product — each combination defined with one meaning or forbidden with writer-MUST-NOT /
reader-MUST-reject. One source of truth per property: codec payloads never restate what layer metadata declares. TARN's planar-vs-interleaved choice
is exactly the PlanarConfiguration trap.

### Class 3: No reader error model

TIFF states writer obligations (IFD entries "must be sorted in ascending order") but almost never says what a reader does on violation. Duplicate
pointers: readers are "under no obligation to detect this condition." Missing StripByteCounts led libtiff to invent estimation heuristics that other
writers then targeted — the most tolerant reader became the de facto spec. **Rule:** a normative reader-conformance section enumerating every
malformation class (bad magic, bad checksum, out-of-range offset, overlapping extents, unknown enum, duplicate entry, count mismatch) and assigning
exactly one outcome: MUST-reject, MUST-ignore, or MUST-use-default. Recovery tools may guess; conforming readers must not.

### Class 4: Multiple encodings of the same thing

SHORT-or-LONG field widths; WhiteIsZero vs BlackIsZero for the same bilevel image; NewSubfileType "replaces" SubfileType yet both stay legal;
ColorMap defined as 16-bit but written 8-bit so often that libtiff sniffs the value range. **Rule:** one canonical encoding per concept — one
integer width per field (64-bit offsets everywhere), one on-disk representation per value, never deprecate-but-keep. Where two layouts are genuinely
necessary (planar/interleaved), that is one explicit enumerated mode, never two overlapping field sets.

### Class 5: Endianness duality

"TIFF readers must be able to handle both byte orders. TIFF writers can do whichever is most convenient" — writer convenience purchased with a
permanent byte-swapping path only half the test matrix exercises. TIFF even defines LZW output byte-oriented specifically so compressed data is
identical in II and MM files — the spec engineering around its own choice. **Rule:** little-endian only, stated once in the header definition; no
byte-order mark (a BOM invites a second value); big-endian-looking magic is MUST-reject, not a fallback.

### Class 6: Address exhaustion and fork-instead-of-version

32-bit offsets capped files at 4 GB with no in-band way to negotiate more; the fix, BigTIFF (magic 43, 8-byte offsets), was specified by the libtiff
community, never ratified by Adobe, rejected by classic readers, and took a decade to reach niche adoption. A default also hid an exhaustion bug:
RowsPerStrip defaulting to 2^32−1 ("effectively infinity") produced whole-image strips libtiff must chop in memory. **Rule:** 64-bit offsets from
day one, plus a format major/minor with defined reject semantics and per-record criticality flags, so growth is an upgrade inside the
format, not a community fork. Defaults must never encode "unbounded."

### Class 7: Registry rot

Private tags ≥ 32768 were allocated by mailing the Aldus Developers Desk — an address that no longer exists — and the spec blessed a "reusable"
65000–65535 range for tags that would "never escape your private environment" (they escaped). Ecosystems that thrived (EXIF, GeoTIFF) did so by
building sub-registry escape hatches to flee the broken namespace. **Rule:** never gate extension identity on a human-staffed mailbox or a small
numeric space. Namespaced identifiers, a machine-readable registry file in the spec repo, a criticality bit per extension, and defined editor
behavior for unrecognized extensions.

### Class 8: Required-but-ignored fields, and dangerous defaults

XResolution/YResolution are required even for screen-only images — so they're universally filler. Orientation defines 8 values but baseline readers
need only support 1, so a legal file can display mirrored. The inverse trap: SampleFormat defaults to unsigned integer, so float data written
without the tag is silently read as garbage. **Rule:** a field may be required only if the spec states what a reader MUST do with it; anything that
changes sample interpretation or geometry (data type, fill, layout) is mandatory, defaultless-or-safely-defaulted, and binding on readers.

### Class 9: Codec state woven into container metadata

Old-style JPEG (Compression=6) is the canonical disaster: tables stored as pointers-to-elsewhere, duplicate pointers, ambiguous restart markers, the
tile-height contradiction — implementers ignored the aux fields and dumped raw JPEG streams, and the fix (TIFF Technical Note 2's Compression=7) had
to abandon the design entirely: each strip/tile a complete self-contained datastream. libtiff never supported the 6.0 design at all. **Rule:** the
codec boundary is exactly "tile payload bytes in, sample bytes out." No codec parameters or tables as separate container fields; no metadata
pointers into payload interiors; every tile independently decodable; each codec pinned by normative reference to an exact external spec (e.g. RFC
1951, RFC 8878) with test vectors, options pinned rather than inherited.

### Class 10: Unbounded pointer-chasing, no locality

"Readers must follow the pointers wherever they may lead"; multi-image files are a linked list of IFDs; "a Baseline TIFF reader is not required to
read any IFDs beyond the first one," so multi-page files silently lost pages. Remote metadata discovery is O(images) round trips — the problem
Cloud-Optimized GeoTIFF spent years addressing by *convention* rather than by spec (until later OGC standardization). **Rule:** the consolidated
metadata directory is a spec requirement with a
normative reachability guarantee (all layer/dimension/channel metadata in O(1) requests from one well-known location); only the tile index carries
file offsets; all layers are equally first-class.

### Class 11: Soft normative register

Word alignment "is expected"; RowsPerStrip should target "about 8K bytes... fairly arbitrary, but seems to work well"; key interop rules hide in
"Beware of..." advice lists and worked examples. Untestable verbs, decades before RFC 2119 discipline. **Rule:** BCP 14 keywords with a
conformance-language clause up front; rationale and advice typographically separated from normative rules; alignment either a declared, checked
property or absent — never "expected."

### What TIFF got right — keep the bones

The self-describing field entry (tag + type + count + value) let 1986 readers skip 1992 data; that forward-compat bone is why TIFF survived at all.
The Baseline/Extensions split and the earlier TIFF 5.0 Classes were the right instinct — profiles and a small core — failing only because the file
never declared which profile it needed. → Keep typed, sized, skippable metadata elements; add the missing half: a criticality bit and a file-level
feature declaration.

Finally, the structural lessons: TIFF froze in 1992 and every defect was patched by satellite documents of unclear authority (TTN2 is still labeled
DRAFT and is the de facto JPEG-in-TIFF standard); and TIFF has no checksum anywhere, so corruption, truncation, and vendor bugs are
indistinguishable from content — guaranteeing readers compete on guessing. Resolve every known ambiguity before 1.0; keep errata in-repo with
declared normative status; make "this file is broken" a detectable, defined state.

### TARN must nail down (consolidated checklist)

- One mandatory conformance profile; every optional feature declared in-file with must-understand semantics.
- A validity table over every interacting-field cross-product; one source of truth per property.
- An assigned reader outcome (reject / ignore / default) for every malformation class.
- One canonical encoding per concept; one integer width; no deprecate-but-keep.
- Little-endian only; no BOM; wrong-order magic is MUST-reject.
- Format major/minor with defined reject semantics plus per-record criticality flags; no "unbounded" defaults; stated bounds for tile and slab
  sizes.
- Namespaced string keys for user metadata and numeric enums with an experimental lane for hot-path IDs, in an in-repo machine-readable registry.
- No required-but-ignorable fields; no dangerous defaults for interpretation-changing values.
- Codec boundary = tile bytes in, samples out; no shared cross-tile state; codecs pinned to exact external specs with test vectors.
- Normative O(1) metadata reachability; offsets only in the tile index; all layers first-class; defined updater semantics.
- RFC 2119/8174 discipline; rationale separated from requirements; every constraint testable.
- Checksums over headers, metadata, and payloads, with reader verification obligations (see Zarr below).

## Zarr v3 (+ sharding-indexed codec) — modern array vocabulary

Zarr is not a rival design so much as a different, legitimate point in the design space: it targets arbitrary key-value stores and pays for that
generality; TARN targets one file and collects a simplification dividend. Zarr supplies the vocabulary — chunk grid, codec chain, fill value,
must_understand — and its sharding codec is the direct ancestor of TARN's slab.

- **Normativity and versioning stated up front.** Zarr opens with "all of the text of this specification is normative except sections explicitly
  marked as non-normative, examples, and notes," uses lowercase RFC 2119 keywords, and declares a MAJOR.MINOR contract where minor versions are
  additive-only. → Adopt the demarcation sentence; put format major.minor in the TARN header and make the policy a byte-level reader obligation:
  unknown minor → proceed, unknown major → refuse.
- **must_understand is the critical/ancillary switch — with a forbidden-ancillary list.** Unknown metadata defaults to must-fail unless explicitly
  `must_understand: false`, and ancillary is *banned* for data type, chunk grid, and chunk key encoding — points where ignoring is never safe. This
  was retrofitted into v3. → Copy both halves in v1.0: default-critical unknowns, plus a normative list of positions (dtype, tile geometry, codec
  ID) where "ignore if unknown" is never allowed.
- **The typed codec chain is good pedagogy; TARN gets to delete the machinery.** Zarr's array→array / exactly-one array→bytes / bytes→bytes typing
  makes invalid pipelines unrepresentable and explains why shuffle precedes compression and where checksums sit. → Borrow the mental model in prose;
  ship a fixed pipeline (optional byte-shuffle → one compressor) as two enum fields. Likewise, endianness in Zarr is a codec configuration; TARN's
  little-endian-only rule replaces that codec with one sentence — but keep Zarr's discipline of normatively pinning tile serialization (element
  order, edge-tile padding) in one dedicated section.
- **Fill values: mandatory, recorded, and bit-exact.** Zarr requires even a defaulted fill value to be recorded, and had to retrofit a hex
  bit-pattern representation (PR #236) because JSON numbers cannot carry NaN payloads or reliably −0.0. → Store per-channel fill as raw
  little-endian element bytes — exact bits, no textual encoding — and state explicitly that fill is bit-exact (NaN payloads and −0.0 preserved) and
  never absent.
- **"No chunk present" is a semantic, not an error.** A missing Zarr chunk implicitly reads as fill, and resizing needs no data writes. → Same for
  TARN, but TARN has no absent-key concept, so the tile index must carry the missing-marker itself; and state explicitly that growing a layer is a
  metadata-only operation.
- **Sharding-indexed is the slab's direct ancestor — improve on it.** A shard is one stored object of inner chunks with a uint64-LE (offset, nbytes)
  index at start or end, fixed-size and fetchable blind because its size is computable a priori; empty inner chunks are the sentinel (2^64−1,
  2^64−1). → This validates TARN's tile index design: fixed-size entries, checksummed index, index covering the full padded grid. TARN improves by
  putting the CRC per-entry *in the index* rather than appended to each chunk (keeping payloads contiguous and alignable — impossible in Zarr where
  crc32c is a per-chunk bytes codec), and by normatively classifying every malformed index-entry combination (offset=MAX with nbytes=0, ranges past
  EOF, overlapping ranges) — which Zarr leaves undefined. Describe the slab as "sharding's guarantees, promoted into the container": the same index
  idea plus contiguity and alignment invariants sharding cannot promise.
- **Bytes-meaning vs writer policy.** Zarr forbids persisting write-strategy knobs; within a shard, chunk order is unfixed and gaps are allowed. →
  The litmus test for whether a field belongs in a TARN file: persist it only if it states a *reader-checkable guarantee* ("all tiles of a slab MUST
  be contiguous in index order; first tile offset MUST be a multiple of A"), never a writer preference.
- **What Zarr delegates to the store, TARN must define itself.** Zarr's store interface mandates no consistency, atomicity, or even listability —
  which is why consolidated metadata exists as an add-on and concurrent shard read-modify-write is unsafe by default. → The single-file checklist:
  (a) enumeration — the consolidated directory *is* the listing; (b) a commit protocol — payloads, then directory, footer last — and defined reader
  behavior on a torn or truncated file; (c) a stated concurrency model (e.g. single-writer / multiple-reader). One section titled "File lifecycle
  and consistency" covers all three.
- **The crc32c codec defines encoding only** — no normative text says verification is mandatory or what a reader does on mismatch. → The most
  important negative lesson for "integrity by default": TARN must write the verifier's contract — which exact bytes each CRC covers, that readers
  MUST verify before returning data (with any opt-out explicit), and how failure is surfaced. A checksum whose verification is optional-by-omission
  is documentation, not integrity.
- **No optional core data types.** Zarr's float16 is "optionally supported" and bfloat16/float8 live in the extensions registry — so two conforming
  readers can disagree on whether a file opens. → Keep TARN's dtype list closed with zero optional members; every addition is a permanent obligation
  on all implementations, which is the principled argument for a small list.
- **Structural vs user metadata, cleanly separated.** Zarr's free-form `attributes` object never mixes with structural fields; dimension names are
  optional with null-for-unnamed. → Copy the separation (structural metadata in fixed binary sections; user metadata in one distinct, checksummed,
  ancillary, preserve-don't-interpret region), but tighten name uniqueness for layers/channels/dimensions to MUST — in a binary index, duplicate
  names are pure ambiguity.
- **The simplification dividend is real and worth stating.** chunk_key_encoding and storage_transformers exist only because chunks live under store
  keys; the sharding codec exists to fight per-chunk object overhead. In TARN, byte offsets replace keys and the container replaces the store — none
  of these need an analog. State this in the design rationale, as interop framing rather than point-scoring.
- **Spec modularity, inverted.** Zarr is a core spec plus many small independently versioned extension specs, each following one template with a
  changelog-and-PR-links habit. → For afternoon readability, invert the packaging but keep the template: one document, every section written to the
  same rubric — purpose, layout table, normative reader rules, normative writer rules, error handling — with an auditable changelog.
- **The recurring gap shape: happy path normative, malformed path unspecified.** Unrecognized node_type, invalid shard-index states, the fill-value
  ambiguity fixed only after the fact. → Budget spec pages for the error register, not just layout tables; a format promising integrity-by-default
  is judged on exactly that register.

## PMTiles v3 — single-file, range-request-native design

PMTiles is the closest existing thing to TARN's delivery model: one file, one fixed-size bootstrap structure, bounded round trips over HTTP ranges,
and an honest one-sentence mutability contract. It is also instructive for what it omits — integrity, error handling, forward compatibility.

- **A tiny fixed-size header at a known offset makes discovery deterministic.** 127 bytes at offset 0 — magic, version, u64 offset/length pairs for
  every section — so a reader issues one spec-constant range request with zero prior knowledge. → TARN wants appendability, so the pattern inverts:
  a small fixed-size *trailer* at end-of-file (magic + version + checksummed pointer to the directory) lets a reader issue one speculative suffix
  request ("last N KiB") the way PMTiles readers fetch the first 16 KiB. Enumerate it field-by-field in an offset/size/type table — that table is
  the most-referenced page of the PMTiles spec.
- **The prefetch budget is a normative contract, not a hint.** "The root directory MUST be contained in the first 16,384 bytes," with the derived
  constant (16,257 bytes) spelled out; changing the window required a major version. → Give TARN an explicit byte budget or formula for the suffix
  fetch, with derived constants stated. A budget the writer MUST meet converts "O(1) round trips" from aspiration into a testable conformance
  property — but note PMTiles' cost ("a sophisticated writer might need several attempts"): choose a budget achievable in one pass or specify a
  spill/overflow pointer.
- **Bounded indirection depth is what keeps the round-trip guarantee true.** Root entries point to tiles or to leaf directories; more than one leaf
  level is normatively discouraged ("please open an issue"), yielding at most 1 fixed request + 1 leaf + 1 payload. → Write TARN's cold-read
  sequence as a normative, enumerated accounting (suffix; spilled per-layer index if any; payload) and hard-bound the indirection depth — an
  unbounded hierarchy silently destroys the O(1) claim. The "discouraged, open an issue" register is itself a lesson: a feedback channel lets a
  small spec avoid hard-forbidding what it hasn't seen.
- **Columnar directory encoding wins by a factor of three.** Entries are stored struct-of-arrays (TileIDs, RunLengths, Lengths, Offsets),
  delta-encoded, varint-packed, then compressed: 981 MB raw → 92 MB, roughly 1.3 bytes per addressed tile. → If index size forces compression
  (the open index-encoding question), store TARN's tile index struct-of-arrays under the metadata codec. Critically, CRC columns are incompressible
  noise — separating them into their own column (free with SoA) keeps the delta-encoded offset/length columns compressible. For aligned layers,
  offsets are an arithmetic sequence; TARN can go further than PMTiles and make them implicit (offset = index × stride), storing only exceptions.
- **Addressed vs stored is crisp vocabulary.** RunLength entries let one content serve N consecutive tiles; the header separately counts addressed
  tiles, tile entries, and tile contents. → Adopt the addressed-vs-stored distinction as spec vocabulary; an unwritten fill tile is the degenerate
  case (addressed, no content) encoded by a reserved index sentinel. The slab is the dual of RunLength: RunLength collapses N tiles sharing one
  content; a slab collapses N adjacent tiles into one contiguous I/O extent with one index granule.
- **Layout properties become machine-checkable flags.** The `clustered` flag means payloads are ordered by TileID, so clients can coalesce adjacent
  range requests — a guarantee, not folklore. Dedup and contiguity are in tension (a deduped entry points at a lesser offset; an aligned layer
  cannot). → Make alignment and slab contiguity explicit per-layer flags with exact invariants ("aligned implies no shared offsets; offset mod A =
  0"), so readers can rely on them for O_DIRECT/GPU paths and validators can check them.
- **Two-tier metadata with two declared codecs.** Machine-critical facts live in the fixed binary header; everything else is one compressed,
  offset-addressed JSON document with a few standardized keys and conditional MUSTs ("If Tile Type = MVT: MUST include vector_layers"). Internal
  compression (directories + metadata) and tile compression are separate single-byte enums from one shared table. → Keep TARN's split: binary
  structures for dtype/dimensions/tiling/codec/fill; one structured, compressed, unbounded user-metadata document; a file-level metadata/index codec
  declared in the trailer so request 1 is self-decoding; never cap metadata implicitly by placement (PMTiles v2's 300 KB cap was the lesson).
- **Fix the linearization order normatively.** PMTiles' 64-bit Hilbert TileID buys delta-friendly directories and spatially-coalescing range
  requests, taught with a worked example table. → TARN must pick and fix a per-layer tile linearization (row-major as the GPU-friendly default;
  curves as future enum values). Linearization is what makes "slab = contiguous run of tiles" well-defined — don't leave it implementation-defined.
  Copy the pedagogy: one worked coordinates→ordinal→slab table is worth a page of prose.
- **State the mutability contract in one blunt sentence.** "PMTiles is a read-only format... if you need transactional updates, use a database."
  Immutability is why a front header and absolute offsets are safe; cache consistency is outsourced to HTTP ETags. → TARN's contract is harder —
  append-friendly — which flips placement to a trailer and obliges TARN to define what PMTiles could skip: which trailer is authoritative (the last
  valid one), torn-append recovery (scan back to the last checksummed trailer), and an in-file generation token for cache revalidation, noting ETags
  as the transport-level complement.
- **Section-relative offsets enable relocation — but demand a coverage rule.** PMTiles sections can be relocated arbitrarily; entry offsets are
  relative to section starts. Nothing, however, forbids overlapping sections or unreachable garbage, so validators cannot certify a file
  byte-for-byte. → Use section-relative offsets (appending a layer never perturbs existing indexes; compaction rewrites one base pointer) *plus* the
  rule PMTiles lacks: every byte of a TARN file is inside exactly one declared, checksummed extent or declared padding, making full-file
  verification well-defined.
- **The gaps are the differentiation.** PMTiles has no checksums anywhere, no error-handling text, enum value 0x00 = "Unknown" with no obligations,
  a version byte "always 0x03" with no rule for other values, and no normative tile-lookup algorithm — resolution must be inferred from reference
  code, and sentinel overloads (Offset+1-or-0; RunLength=0 flips an entry into a leaf pointer) are stated in single dense sentences without
  examples. → TARN keeps checksums out of the hot path (CRCs in the index, payloads contiguous), writes the per-structure on-failure table, defines
  version semantics up front, allows no emittable "Unknown" enum value, includes a short normative "Reading a tile" algorithm (numbered steps,
  including the fill path and the checksum-verification step), gives every sentinel a worked byte-level example plus test vectors, and collects all
  constants into one normative table rather than burying them in prose.
- **Writer-effort tiers, named honestly.** Optional statistics fields with an explicit 0 = unknown state let minimal streaming writers and
  optimizing writers coexist. → Adopt for expensive-to-know facts (tile counts, value ranges) — but be stricter than PMTiles: anything a reader
  needs for correctness must never have an "unknown" state. Naming the tiers ("minimal writer" / "optimizing writer") and stating which requirements
  bind which keeps "implementable in a weekend" honest.

## QOI + RFC 2119/8174 (BCP 14) — radical brevity, disciplined language

QOI proves a spec can fit on one page and be implemented in a sitting — and demonstrates precisely where brevity-by-silence fragments an ecosystem.
BCP 14 supplies the language discipline that QOI lacked.

### What transfers from QOI

- **Brevity comes from a fixed pipeline with zero options, not terse writing.** Six ops, one hash, one seed state, one end marker; ~100 lines per
  direction. Every option multiplies spec text and test matrix. → TARN cannot be option-free, so spend the complexity budget deliberately: exactly
  one container structure (one header form, one directory form, one index-entry form), all variability confined to enumerated leaf values. Never two
  structural ways to express one thing.
- **The op-table technique:** every wire structure gets a boxed byte/bit diagram with field positions, widths, valid ranges, and bias/encoding,
  immediately followed by worked numbers ("−2 is stored as 0 (b00)"; "1 − 2 will result in 255"). QOI never states an encoding rule without a
  concrete number attached. → Every TARN on-disk structure gets an offset/size/type/name/valid-range table plus a worked example with real bytes,
  and the spec ships one complete annotated hex dump of a tiny valid file (one layer, 2×2 tiles) as an appendix.
- **Specify initial state, completion, and boundaries — then test them.** QOI nails its seed state and completion predicate, yet the one boundary
  left implicit (first op is a RUN against the seed pixel) is exactly where real decoders diverged. → Enumerate TARN's boundary states explicitly —
  unwritten tile reads as fill; edge-tile padding content pinned normatively (checksum determinism demands *some* fixed rule); empty layer;
  zero-length compressed tile; zero-layer file — and ship a reference file exercising each, with expected values and checksum verdicts.
- **Label informative fields and state their non-effect.** QOI's channels/colorspace are "purely informative," yet implementers assumed channels=3
  masks alpha. → Classify every TARN field as structural, semantic, or informative; for informative fields state that readers MUST NOT let them
  alter decoding, and what happens when they contradict the data.
- **Name illegal values created by encoding overlaps and state precedence** (QOI: 8-bit tags beat 2-bit tags; run lengths 63/64 are illegal). →
  Design TARN structures so no bytes have two valid parses; wherever ranges have reserved values, name them and mandate the reader response.
- **Silence on errors is the main fragmentation vector in small specs.** QOI says nothing about truncation, trailing data, or dimension limits, so
  the reference implementation invented a 400M-pixel limit that exists nowhere in the spec — "a valid QOI file" differs by implementation. → Every
  limit lives in the spec (max rank, dimensions, tile size, name length, directory size); a normative invalid-input section assigns each violation
  an outcome class (reject-file, reject-layer, reject-tile, ignore-record, or preserve-verbatim).
- **Non-canonical encoding means byte-diff conformance testing of writers is impossible — say how conformance IS tested.** → Writer conformance:
  every produced file MUST be a conforming TARN file (the RFC 8259 generator pattern). Reader conformance: decode-based tests against a published
  corpus with expected array contents and expected checksum verdicts, including deliberately corrupted files. Optionally define a non-normative
  "reproducible writer" profile (pinned codec params, defined padding, sorted directory) for byte-identical output.
- **A reference implementation is an adoption asset and a divergence risk.** qoi.h doubles as executable specification, and everywhere it adds
  behavior it silently forks the de facto spec. → TARN will keep any reference implementation outside the spec repo (the corpus lives here), with
  the rule that no implementation may enforce a constraint the spec does not state; legitimate implementation limits get blessed generically
  ("implementations MAY set limits on..." with named minimum guarantees).
- **Freezing bought QOI its brevity — TARN can't buy it that way.** QOI has a magic, no version field, no extension points, and no v1.1 escape
  hatch. A format that intends to evolve must pay for explicit extension rules at 1.0: per-category unknown-value behavior, and flag space split
  into must-ignore and must-reject halves at birth.
- **A free, readable, self-contained spec is itself an adoption engine.** QOI's CC0 one-pager plus reference code plus test images produced dozens
  of ports within weeks. → Treat "readable in an afternoon, implementable in a weekend" as an acceptance test: before 1.0, have someone implement a
  reader from the spec alone, and fix the spec wherever they had to peek at reference code — that is exactly where QOI leaked.

### What BCP 14 adds

- **Keywords are normative only in ALL CAPITALS** (RFC 8174); QOI's lowercase "must" sentences are formally non-normative — the exact ambiguity the
  boilerplate fixes. → Include the RFC 8174 paragraph verbatim in Terminology, and lint the spec so must/should/may never appear lowercase in
  normative sections (rewrite as "needs to," "can," "might").
- **Every requirement names its actor; every writer-MUST states the reader counterpart.** QOI's consecutive-INDEX ban is a writer-only rule with no
  statement of whether decoders accept violating files — textbook actor ambiguity. → House style: "Writers MUST NOT emit X; readers MUST treat files
  containing X as invalid" (or "MUST nevertheless accept X"). Consider separate writer-requirements and reader-requirements subsections per chapter.
- **Imperatives constrain observable bytes and behavior, never implementation technique** (RFC 2119 §6): "tile payloads MUST decompress to exactly
  tile_byte_length bytes," not "writers MUST use streaming compression."
- **Every MAY carries a reciprocity obligation** (RFC 2119 §5): omitting and including implementations MUST still interoperate. The cheapest options
  are *reader-invisible* ones — alignment and slabs change writer output but need zero reader code because offsets are explicit — prefer these;
  reader-visible options (new codecs) create conformance surface, so all core codecs are reader-MUST and a writer MAY never creates reader dialects.
  Every SHOULD gets a stated consequence of deviating.
- **Conformance via named roles with asymmetric obligations** (RFC 8259 parser/generator; PNG's four classes): a one-page section defining
  conforming TARN *file* (a pure predicate on bytes), *reader* (accepts every conforming file within declared limits; detects and reports the
  enumerated violations; verification default stated here), *writer* (produces only conforming files), and *updater* (preserves
  unknown-but-well-formed content, keeps checksums valid). All later requirements phrase themselves against these classes.
- **Spell out security consequences of non-compliance** (RFC 2119 §7): bounds-check untrusted offsets and lengths before use; check
  dimension-product overflow; treat declared uncompressed size as the authoritative allocation bound; state plainly that CRCs detect corruption, not
  tampering.

## Cross-cutting lessons

Five themes recur across three or more of the sources; these are the closest thing this research produced to laws.

1. **Unspecified reader behavior fragments ecosystems.** TIFF's missing error model bred per-reader heuristics that writers then targeted; Zarr's
   crc32c codec never obliges verification; PMTiles has no error-handling text at all; QOI's silence on malformed input let its reference
   implementation define validity. PNG is the counterexample that proves the cure: a normative error taxonomy with per-case required outcomes.
   TARN's rule: every detectable violation is assigned exactly one outcome class — reject-file, reject-layer, reject-tile, ignore-record, or
   preserve-verbatim — and conforming readers never guess. (The TIFF-section "MUST-use-default" idea is subsumed by mandatory recorded fill rather
   than becoming an outcome class.)
2. **Checksums without verifier obligations are documentation, not integrity.** PNG admits non-verifying decoders get out of step (and leaves the
   length field uncovered); Zarr defines CRC layout but not decode-time behavior; TIFF and PMTiles have no integrity mechanism and therefore cannot
   distinguish corruption from content. TARN must specify which bytes each checksum covers (including all framing metadata), that readers verify
   before returning data, and how failure is surfaced — scoped so one bad tile never silently reads as fill.
3. **Boundary cases without test vectors diverge.** QOI's first-op-RUN gap, Zarr's undefined invalid-index states and retrofitted fill
   representation, PMTiles' example-free sentinel overloads, TIFF's internal contradictions surviving to publication. Every sentinel, seed state,
   edge-tile, and empty case gets a worked byte-level example in the spec and a file in the published corpus — including deliberately corrupted
   files with expected verdicts.
4. **Registries need machine-readable homes, not mailboxes — plus a private lane.** TIFF's dead registration address and blessed collision range
   produced registry rot; PNG pairs a companion registry with a syntactic private namespace and an anti-squatting rule; Zarr moved from churning URI
   names to a central registry repo with an experimental escape valve. TARN: a registry file in the spec repo, syntactically distinct experimental
   ID ranges per ID space, and no shipping unregistered public IDs.
5. **Writer freedom is reader tax — unless the option is reader-invisible.** TIFF converted every writer convenience (byte orders, field widths,
   redundant encodings) into permanent reader burden; Zarr's optional core dtypes let conforming readers disagree on whether a file opens; QOI
   stayed implementable precisely by having no options. The disciplined middle: one canonical encoding per concept, a closed dtype list with no
   optional members, all core codecs reader-MUST, and a preference for options (alignment, slabs) that change bytes written but require zero reader
   code because offsets are explicit.

Two further patterns appear often enough to note: **declared guarantees beat conventions** (Cloud-Optimized GeoTIFF's convention-first years vs
PMTiles' normative budget vs TARN's in-spec reachability rule; Zarr's litmus test that persisted fields state reader-checkable invariants, never
writer preferences), and **evolution must be designed at 1.0** (PNG's versionless per-chunk criticality vs TIFF's BigTIFF fork vs QOI's permanent
freeze — TARN's choice: version fields with defined reject semantics *and* per-record criticality flags, with a stated degradation story for every
future feature).
