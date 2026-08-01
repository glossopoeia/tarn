# The TARN Format Specification

**Status: working draft — nothing here is stable.** This document is being
drafted batch by batch under the process in [PLAN.md](../PLAN.md); sections
marked *[Reserved]* have agreed scope but no text yet. Decisions encoded
here are governed by the ADRs in
[docs/decisions/](../docs/decisions/README.md).

License: CC BY 4.0 (see [LICENSE-SPEC](../LICENSE-SPEC)).

> **How to read this document** *(non-normative).* Sections follow a fixed
> rubric where applicable: purpose, byte-layout table, writer rules, reader
> rules, error handling, worked examples. On-disk structures are presented
> as offset/size/type/name/valid-range tables. Every field is classified as
> **structural** (affects how bytes are located or decoded), **semantic**
> (affects what decoded values mean), or **informative** (never affects
> decoding — the normative rule is §4.7). Normative requirements carry
> stable identifiers like `[R-IDX-03]`; test vectors and conformance
> checklists cite identifiers, never prose positions.

---

## Part 0 — Preliminaries

### 1. Introduction

*[Reserved — non-normative; drafted last.]*

### 2. Conformance

#### 2.1 Normative language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be interpreted as described in BCP 14
[RFC 2119] [RFC 8174] when, and only when, they appear in all capitals, as
shown here.

All text in this document is normative except: §1 (Introduction); any text
labeled *Note*, *Example*, or *Rationale*; and appendices identified as
non-normative. `[R-CNF-01]`

> **Note.** Requirements in this document follow a fixed phrasing
> discipline: every requirement names the actor it binds (writer, reader,
> updater, verifier, or file); every writer-side prohibition is paired
> with an explicit reader-side clause stating what a reader does with a
> violating file; every SHOULD states the consequence of deviation; and
> requirements constrain bytes and observable behavior, never
> implementation technique.

#### 2.2 Requirement identifiers

Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`.
Identifiers are stable: they are never renumbered or reused, a withdrawn
requirement leaves its identifier permanently retired, and numbers above
99 extend naturally (`[R-ENC-100]`) without renumbering. Identifier order
carries no meaning.

Prefixes: `CNF` (conformance), `MDL` (terminology and data model), `ENC`
(encoding), `CNT` (container structures), `LIF` (lifecycle and
consistency), `EXT` (extension points and registry), `GEO` (layers,
dimensions, and tiling), `IDX` (tile index), `SLB` (slabs and
alignment), `TYP` (types and fill), `SER` (tile serialization), `COD`
(codecs and filters), `MTA` (user metadata), `RDR` (reading), `WRT`
(writing and updating), `ERR` (error register), `SEC` (security), `PRV`
(privacy). New prefixes are added by ADR when a section needs one;
existing prefixes are never reassigned.

#### 2.3 Conformance classes

Conformance is defined for four classes.

- **Conforming TARN file.** A byte sequence satisfying every file-level
  requirement of this specification. File conformance is a pure predicate
  on bytes: it does not depend on any reader, writer, or environment.
  `[R-CNF-02]`
- **Conforming reader.** A reader MUST accept every conforming file none
  of whose values exceeds the minimum guarantees of §21's limits table,
  and MUST handle every codec that §17 designates as core, both channel
  layouts (§14), and every sample type that §12 designates as core.
  There are no subset profiles: software that declines to support a core
  codec, either channel layout, or a core sample type is not a conforming
  reader, even if it reads all other conforming files correctly.
  `[R-CNF-03]` A reader MUST detect the violations enumerated in the
  error register (§21) and apply the outcome class this specification
  assigns to each; a reader MUST NOT heuristically repair a violating
  structure or infer values this specification does not define.
  `[R-CNF-04]`
- **Conforming writer.** A writer MUST emit only conforming files.
  `[R-CNF-05]` Writer conformance is semantic: this specification does not
  promise canonical bytes, and two conforming writers given identical
  input MAY produce different conforming files.
- **Conforming updater.** A tool that modifies an existing file without
  necessarily understanding all of its content. An updater MUST satisfy
  every writer requirement for the bytes it produces, and additionally
  MUST honor the preservation obligations of Part I for records it does
  not understand. `[R-CNF-06]`

#### 2.4 Outcome classes and owning scope

Every detectable violation named by this specification is assigned
exactly one **reader outcome**: reject-file, reject-layer, reject-tile,
or ignore-record. `[R-CNF-07]` The same vocabulary is used for defined
conditions that are not violations (an unknown ancillary record is
*ignored*, not rejected). **preserve-verbatim** names an updater
obligation, orthogonal to reader outcomes: a record a reader ignores can
still be one an updater preserves.

| Outcome | Meaning |
|---|---|
| **reject-file** | The file is not usable; failure is reported for the whole file. A reader MUST NOT rely on any structure in it. |
| **reject-layer** | The affected layer's data and metadata are not usable; all other layers are unaffected. A reader MAY still list the file's layers, including the rejected one's name. |
| **reject-tile** | The affected tile's data is not usable; a read of that tile reports failure. All other tiles, including neighbors in the same layer, are unaffected. |
| **ignore-record** | The record is skipped as though absent. Decoding of all stored data is unaffected. |
| **preserve-verbatim** | Binds updaters: the bytes are carried forward unmodified (relocated only as Part I permits). |

Every structure this specification defines has exactly one **owning
scope** — file, layer, or tile — stated in the section that defines the
structure. The phrase "a validity error at the owning scope" means the
reader outcome for that scope: file → reject-file, layer → reject-layer,
tile → reject-tile. `[R-CNF-08]`

A reader MUST NOT return data as valid from a scope this specification
rejects; in particular, a read of a rejected tile MUST NOT silently
return fill. `[R-CNF-09]`

> **Note.** "Reject" prescribes the scope of unusability, not user
> interface: how failure is reported is implementation technique.

#### 2.5 Implementation limits

Every limit that affects which files are valid or which files a
conforming reader accepts lives in this specification, never only in an
implementation. Readers MAY enforce resource limits, but MUST accept any
conforming file within the minimum guarantees stated in §21's limits
table; writers MAY rely on those minimums. `[R-CNF-10]` *(The limits
table is drafted with Batch 11, per Q-H1.)*

### 3. Terminology and Data Model

#### 3.1 Terms

The following terms are used throughout this specification with exactly
these meanings.

- **file** — a single TARN artifact: a byte sequence satisfying this
  specification's file-level requirements.
- **layer** — a named N-dimensional array within a file. All layers of a
  file are equally first-class.
- **dimension** — one axis of a layer's grid, having a name (§4.6), an
  **extent** (the number of sample positions along the axis), and a
  **tile extent** (the number of sample positions per tile along the
  axis). Dimensions are declared in order; the declared order is
  load-bearing (§11.4).
- **rank** — a layer's number of dimensions, written *d*.
- **channel** — a named, typed per-sample value of a layer (§12).
  Channels are declared in order; a channel's **index** is its 0-based
  position in that order, and the order is load-bearing (§11.4, §14).
- **channel layout** — whether a layer's channels are stored together
  within each tile (*interleaved*) or each channel is tiled separately
  (*planar*); the two-value enum is specified in §14.
- **sample** — the tuple of one value per channel at one coordinate.
- **coordinate** — a *d*-tuple (x₀, …, x_{d−1}), in declared dimension
  order, with 0 ≤ xᵢ < Eᵢ, identifying one sample position of a layer
  with extents (E₀, …, E_{d−1}).
- **tile** — the unit a tile-index entry addresses: in an interleaved
  layer, one cell of the tiling grid carrying all channels; in a planar
  layer, one cell of the grid for one channel. Every tile of a layer has
  the same logical shape, a block of ∏ Tᵢ sample positions (§11.3).
- **addressed tile / stored tile** — every tile of a layer is
  *addressed*. A tile is additionally *stored* if and only if its
  tile-index entry in the live generation is not the sentinel (§15);
  superseded payload bytes from earlier generations do not make a tile
  stored. An addressed tile that is not stored reads as fill (§13).
- **fill value** — the per-channel value that a channel's samples take
  wherever the tile carrying that channel is not stored (§13).
- **slab** — a declared run of consecutive stored tiles kept physically
  contiguous as one I/O unit (§16).
- **tile index** — the per-layer table locating and checksumming stored
  tiles (§15).
- **directory** — the consolidated metadata structure describing every
  layer and carrying all records (§7).
- **trailer** — the fixed-size structure occupying the final 64 bytes of
  a file, anchoring discovery and commits (§6).
- **front signature block** — the constant 16 bytes at offset 0 (§6).
- **generation** — the commit counter distinguishing successive
  committed states of a file (§9).
- **user metadata** — the structured document carrying non-structural,
  application-level information (§18).

#### 3.2 The reference array

Each layer of a conforming file denotes exactly one **reference array**:
the *d*-dimensional array with the layer's extents whose element at each
coordinate is the sample at that coordinate, determined per channel. If
the tile carrying that channel at that coordinate is stored, the
channel's value is the one decoded from that tile under Part II's rules;
otherwise it is that channel's fill value (§13). In an interleaved layer
one tile carries every channel, so a coordinate's channel values are
stored or fill together; in a planar layer each channel's storedness is
independent, and a single sample can mix decoded and fill values.
Sample positions that exist only as edge-tile padding (§11.3) have
coordinates outside the layer's extents and are not part of the
reference array. `[R-MDL-01]`

The reference array is this specification's conformance target: a
conforming reader that reads any portion of a layer MUST return exactly
the corresponding portion of the reference array, bit-for-bit — sample
values are bit patterns, and decoding MUST NOT alter them (floating-
point payloads included; type semantics are §12's subject). `[R-MDL-02]`

#### 3.3 Container and array model

> **Note.** Part I (container) is independent of Part II (array model)
> by construction: no Part I structure requires decoding sample
> payloads, so verifiers, appenders, and compactors operate on files
> whose layers they cannot decode — that independence is load-bearing
> for the updater rules of §7 and §20.

### 4. Encoding Conventions

#### 4.1 Byte order

All multi-byte values in a TARN file — integers, floating-point sample
values, and every multi-byte field of every structure — are
little-endian. `[R-ENC-01]` There is no byte-order mark and no big-endian
variant; writers MUST NOT emit big-endian values, and a reader
encountering what appears to be a byte-swapped signature (§6) MUST treat
the file as invalid (reject-file), never as a foreign-endian file to be
adapted. `[R-ENC-02]`

#### 4.2 Integer types and domains

This specification uses the types `u8`, `u16`, `u32`, and `u64` for
unsigned little-endian integers of 1, 2, 4, and 8 bytes. All file
offsets, byte lengths, dimension extents, and tile extents are `u64`.
The valid range of every offset, length, and extent is 0 to 2⁶³ − 1
inclusive; a reader MUST treat a value above 2⁶³ − 1 in any such field
as a validity error at the owning scope. `[R-ENC-03]`

> **Rationale.** The reduced range costs nothing at realistic scales and
> lets implementations in languages with signed 64-bit integers operate
> without unsigned arithmetic gymnastics.

A reader — including any updater or verifier, which are readers of the
files they process — MUST treat any quantity this specification defines
as a sum or product of integers obtained from a file (offsets plus
lengths, grid counts, tile counts, sample-position counts, ordinals)
whose mathematical value would exceed 2⁶³ − 1 as a validity error at
the owning scope, and MUST NOT act on a wrapped or truncated value.
`[R-ENC-04]` A reader MUST NOT allocate, seek, or
issue I/O based on any integer obtained from a file before the checksum
covering it has been verified (§4.5, §8). `[R-ENC-05]`

No field's width is ever a writer choice: every field's width is fixed
by this specification, and a structure whose fields appear at any other
width is invalid at its owning scope. `[R-ENC-06]`

#### 4.3 Fixed-size structures

Structures this specification defines with a fixed size have exactly
that size in every conforming file of a given format major version; for
structures whose size is a function of a declared encoding (the tile
index), the fixed size is per encoding. A reader that encounters a known
structure at any other size MUST treat it as a validity error at the
structure's owning scope; an unexpected size is never evidence of a
newer format version. `[R-ENC-07]` All format growth happens through
four vehicles: new record types (§7), new enum values in ranges this
specification reserves, new ignore-lane flag bits (§6), and new
standardized user-metadata keys (§18).

#### 4.4 Bit numbering

Within a byte or a flags field, bit 0 is the least significant bit, and
flag tests are bitwise. `[R-ENC-08]`

> **Note.** This rule fixes bit numbering in flags and packed fields
> generally; the mapping of boolean *samples* to bits is defined in §14.

#### 4.5 Checksums

The checksum used throughout this specification is CRC-32C: the 32-bit
cyclic redundancy check with the Castagnoli polynomial 0x1EDC6F41
(RFC 3720 §12.1), reflected input and output, initial value 0xFFFFFFFF,
and final XOR 0xFFFFFFFF, stored as a little-endian `u32`. `[R-ENC-09]`

**Check vector.** The CRC-32C of the nine ASCII bytes `"123456789"`
(`31 32 33 34 35 36 37 38 39`) is `0xE3069283`, stored as the bytes
`83 92 06 E3`. An implementation whose checksum function does not
reproduce this value does not implement this specification's checksum.

A reader MUST verify the checksum covering a field before acting on that
field. `[R-ENC-10]` Every field of every structure is covered by exactly
one checksum, except the fields of the front signature block, which is a
constant whose check is equality (§6); which bytes each checksum covers,
and each conformance class's verification obligations, are defined with
the structures that carry them (§8).

> **Note.** Checksums detect accidental corruption. They do not
> authenticate: an adversary who can modify bytes can recompute
> checksums. Authenticity requires detached signatures or hashes,
> outside this specification's scope.

#### 4.6 Strings and names

All strings are length-prefixed UTF-8. Each structure's layout table
states its prefix width, and every length prefix counts bytes — never
characters or code points. Writers MUST NOT emit byte sequences that are
not well-formed UTF-8; a reader MUST treat ill-formed UTF-8 in any
string as a validity error at the owning scope. `[R-ENC-11]`

**Names** — the strings that identify layers, dimensions, channels, and
user-metadata keys — satisfy three further constraints. Writers MUST NOT
emit a name that violates any of them; a reader MUST treat such a name
as a validity error at the owning scope. `[R-ENC-12]` A name is:

- non-empty;
- at most 255 bytes of UTF-8 (so every name's length prefix is a single
  byte);
- free of code points in the range U+0000 through U+001F.

Name comparison is raw bytes: two names are the same name if and only if
their encoded byte sequences are identical. Readers MUST NOT normalize,
case-fold, or otherwise transform names for comparison. `[R-ENC-13]`
Writers SHOULD emit names in Unicode Normalization Form C; a writer that
does not risks visually identical but byte-distinct names coexisting,
which conforming readers will treat as distinct. `[R-ENC-14]`

Names are unique within their scope: layer names within a file,
dimension names and channel names within their layer. Writers MUST NOT
emit duplicates; a reader MUST treat a duplicate name as a validity
error at the owning scope — a duplicate layer name is a file-scope error
(reject-file); a duplicate dimension or channel name is a layer-scope
error (reject-layer). `[R-ENC-15]` Uniqueness of user-metadata keys is
defined by the user-metadata document (§18).

> **Example.** The name `température` in NFC encodes as 12 bytes
> (`74 65 6D 70 C3 A9 72 61 74 75 72 65`), length prefix 12. The same
> word with `é` in NFD (`65 CC 81`) is 13 bytes and is a *different
> name* under `[R-ENC-13]` — which is why `[R-ENC-14]`'s NFC advisory
> exists.

#### 4.7 Field taxonomy and presentation

Every field this specification defines is classified **structural**,
**semantic**, or **informative**. A field classified informative MUST
NOT affect how any byte is located or decoded, and a reader MUST NOT
alter decoding based on it; each informative field's definition states
what a reader does when it contradicts the data it describes.
`[R-ENC-16]`

> **Note.** Layout tables in this document give, per field: byte offset
> within the structure, size, type, name, taxonomy class, and valid
> range. Every non-obvious encoding is followed by a worked numeric
> example, and every sentinel or overloaded encoding additionally has a
> paired conformance vector. All named constants appear once in
> Appendix B.

---

## Part I — Container

### 5. File Anatomy and Byte Coverage

*[Reserved — Batch 3: overall layout; every-byte-classified coverage rule
per ADR-0017/Q-B5.]*

### 6. Front Signature Block and Trailer

*[Reserved — Batch 3: 16-byte constant front block; 64-byte trailer field
table, version fields, and flag lanes per ADR-0018/0025; signature byte
values per Q-G4.]*

### 7. Metadata Directory and Records

*[Reserved — Batch 3: 24-byte record header, MU/PE flags, scope binding,
extent slot per ADR-0026; layer records.]*

### 8. Integrity

*[Reserved — Batch 3 (index-segment coverage lands with Batch 4):
per-structure checksum coverage and verification obligations per
ADR-0008/0023/0024.]*

### 9. Lifecycle and Consistency

*[Reserved — Batch 3: commit protocol, torn-append recovery, generations,
single-writer/multi-reader per ADR-0017.]*

### 10. Extension Points and Registry

*[Reserved — Batch 12: enumerated extension surface, ID spaces,
experimental ranges per ADR-0025/0026/Q-G3.]*

---

## Part II — Array Model

### 11. Layers, Dimensions, and Tiling

#### 11.1 Geometry and its validity floor

The owning scope (§2.4) of a layer's geometry and linearization fields
is the layer.

A layer has rank d ≥ 1; each of its d dimensions has a name (§4.6), an
extent Eᵢ ≥ 0, and a tile extent Tᵢ ≥ 1; and the layer has at least one
channel. A tile extent MAY exceed its dimension's extent (the grid is
then a single padded tile along that axis). Writers MUST NOT emit a
layer with rank 0, any tile extent 0, or channel count 0; a reader MUST
treat any of these as a validity error at layer scope. `[R-GEO-01]`

A dimension with extent 0 is valid: its grid count is 0, the layer has
zero addressed tiles, its tile index has zero entries, and its reference
array is empty. Readers MUST accept such a layer, and a read of any
region of it returns no samples. `[R-GEO-02]`

> **Rationale.** Empty layers serve schema-first workflows: declare
> layers at creation, grow extents as data arrives — extent growth is a
> metadata-only operation under this specification's commit model.

#### 11.2 Grid arithmetic

For each dimension, the **grid count** Gᵢ is the ceiling division
⌈Eᵢ / Tᵢ⌉, equal to Eᵢ/Tᵢ plus 1 if Eᵢ mod Tᵢ ≠ 0 (integer division).
The layer's **spatial-tile count** is N = ∏ Gᵢ, and its
**sample-position count per tile** is P = ∏ Tᵢ. The layer's
**addressed-tile count** — the number of its tile-index entries (§15) —
is N for an interleaved layer and C · N for a planar layer, where C is
the channel count. These products, like all geometry arithmetic, are
subject to `[R-ENC-04]`: a reader MUST treat a product exceeding
2⁶³ − 1 as a validity error at layer scope. `[R-GEO-03]`

> **Note.** The stated form of the ceiling division avoids the idiom
> (Eᵢ + Tᵢ − 1)/Tᵢ, whose intermediate sum can exceed 2⁶³ − 1 — the
> declared valid domain (§4.2) and the range of signed 64-bit
> integers — for large extents, even though it fits an unsigned 64-bit
> integer.

> **Example.** A layer declared (y, x) with extents (1024, 2048) and
> tile extents (256, 256): G = (4, 8), N = 32 spatial tiles,
> P = 65,536 sample positions per tile. With extents (1000, 2048)
> instead, G_y = ⌈1000/256⌉ = 4 still — the last row of tiles is
> padded (§11.3).

#### 11.3 Uniform tiles and edge padding

Every tile of a layer has the same logical shape (T₀, …, T_{d−1}).
Where Gᵢ · Tᵢ > Eᵢ, the tiles at the high edge of dimension i contain
**padding positions** — sample positions whose coordinate along that
axis would be ≥ Eᵢ. Padding positions are serialized like any other
position (byte-level rules and padding content: §14) but are not part
of the reference array (§3.2); a reader MUST NOT return padding
positions as samples. `[R-GEO-04]`

#### 11.4 Linearization

Each layer carries a **linearization** field (`u16`, structural)
selecting the rule that orders tiles within the grid and entries within
the tile index. It does not govern sample order inside a tile: in-tile
sample order is row-major for every linearization value, in every
version of this format. Field values: 0 is invalid; **1 = row-major** —
the last-declared dimension varies fastest — is the only value this
format major version defines for writers, and writers MUST NOT emit any
other value; values 2 and 3 are reserved without semantics; values 4
through 0x7FFF are reserved for future assignment by this
specification; values ≥ 0x8000 are the experimental range (§10). A
reader MUST treat any linearization value other than 1 as a validity
error at layer scope — this includes 0, all reserved values, and the
experimental range, which no conforming writer of format major
version 1 emits. `[R-GEO-05]`

With grid counts (G₀, …, G_{d−1}) and tile extents (T₀, …, T_{d−1}),
all in declared dimension order, and the convention that an empty
product is 1 (so at d = 1 the ordinals below reduce to u₀ and t₀):

- A coordinate (x₀, …, x_{d−1}) lies in the tile with **tile
  coordinates** tᵢ = xᵢ div Tᵢ, at **in-tile position** uᵢ = xᵢ mod Tᵢ.
- The **in-tile sample ordinal** of (u₀, …, u_{d−1}) is
  Σᵢ uᵢ · ∏_{j>i} Tⱼ — for every linearization value, permanently.
- Under linearization 1, the **spatial tile ordinal** of
  (t₀, …, t_{d−1}) is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ.
- The **disk tile ordinal**, which orders tile-index entries (§15), is
  s for an interleaved layer, and **c · N + s** for a planar layer
  (§14), where c is the channel's index (§3.1) — channel-major
  grouping. `[R-GEO-06]`

> **Example.** The layer of §11.2's example, grid (G_y, G_x) = (4, 8).
> Spatial ordinals: tile (0, 0) → 0; tile (0, 1) → 1; tile (1, 0) →
> 1·8 + 0 = 8. The coordinate (y, x) = (300, 700) lies in tile
> (1, 2) → s = 1·8 + 2 = 10, at in-tile position (44, 188) → in-tile
> ordinal 44·256 + 188 = 11,452. If the same layer is planar with
> C = 4 channels, the tile carrying channel 2 at that spatial position
> has disk ordinal 2·32 + 10 = 74.

> **Note.** Linearization fixes the mapping from *declared dimension
> order* to bytes; it says nothing about axis direction or orientation
> (whether y points up or down is semantics, carried in user metadata,
> §18). Column-major ecosystems (Fortran, Julia, MATLAB) write
> zero-copy by declaring dimensions in reversed order — the same
> convention their HDF5 and netCDF bindings already apply.

### 12. Channels and Sample Types

*[Reserved — Batch 5: closed type list per ADR-0013.]*

### 13. Fill Values and Sparse Tiles

*[Reserved — Batch 5: bit-exact fill and unstored-tile reads per
ADR-0010.]*

### 14. Tile Serialization

*[Reserved — Batch 6: interleaved and planar byte layouts, boolean
representation, edge padding per ADR-0012/0021 and Q-C4/Q-D6.]*

### 15. Tile Index

*[Reserved — Batch 4: 20-byte entries, segment CRC array, sentinel and
invalid-combination table per ADR-0024.]*

### 16. Slabs and Alignment

*[Reserved — Batch 4: slab declaration (S, A_slab) and per-tile alignment
per ADR-0005/0022.]*

### 17. Codecs and Filters

*[Reserved — Batch 7: codec menu, wrapper pinning, shuffle filter,
boundary contract per ADR-0009 and Q-E1/E2.]*

### 18. User Metadata

*[Reserved — Batch 12: structured document, determinism, key uniqueness,
standardized keys per ADR-0015 and Q-F1/F3.]*

---

## Part III — Behavior

### 19. Reading a TARN File

*[Reserved — Batch 8: normative open and tile-read algorithms per
ADR-0019/0024.]*

### 20. Writing and Updating

*[Reserved — Batch 9: writer tiers, append procedure, updater stories per
ADR-0017/0026.]*

### 21. Error-Handling Register and Limits

*[Reserved — Batch 10: consolidated violation × outcome table.
Batch 11: the limits table per Q-H1.]*

### 22. Security Considerations

*[Reserved — Batch 11.]*

### 23. Privacy Considerations

*[Reserved — Batch 11: superseded bytes, deletion vs erasure, compaction
per ADR-0017.]*

### 24. Conformance Test Vectors

*[Reserved — Batch 13: corpus contract.]*

---

## Appendices

*[Reserved — Batch 13: A annotated hex dump · B constants table ·
C registry snapshot · D design rationale (non-normative) · E changelog ·
F normative references.]*
