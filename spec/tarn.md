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
  (*planar*); encoded in the layer record (§7.4), byte-layout semantics
  in §14.
- **sample** — the tuple of one value per channel at one coordinate.
- **coordinate** — a *d*-tuple (x₀, …, x_{d−1}), in declared dimension
  order, with 0 ≤ xᵢ < Eᵢ, identifying one sample position of a layer
  with extents (E₀, …, E_{d−1}).
- **tile** — the unit a tile-index entry addresses: in an interleaved
  layer, one cell of the tiling grid carrying all channels; in a planar
  layer, one cell of the grid for one channel. Every tile of a layer has
  the same logical shape, a block of ∏ Tᵢ sample positions (§11.3).
- **addressed tile / stored tile** — every tile of a layer is
  *addressed*. A tile is *stored in a generation* if and only if that
  generation's tile-index entry for it is not the sentinel (§15);
  unqualified *stored* means stored in the live generation. Superseded
  payload bytes from earlier generations do not make a tile stored. An
  addressed tile that is not stored reads as fill (§13).
- **fill value** — the per-channel value that a channel's samples take
  wherever the tile carrying that channel is not stored (§13).
- **slab** — a declared run of consecutive stored tiles kept physically
  contiguous as one I/O unit (§16).
- **tile index** — the per-layer table locating and checksumming stored
  tiles (§15).
- **directory** — the consolidated metadata structure describing every
  layer and carrying all records (§7).
- **trailer** — the fixed-size 64-byte structure that commits a
  generation (§6); each commit appends one, and the *live* trailer
  occupies the final 64 bytes of the file.
- **front signature block** — the constant 16 bytes at offset 0 (§6).
- **generation** — one committed state of a file, and the counter,
  carried in its trailer, that numbers it (§9).
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

#### 5.1 Anatomy

A TARN file is written generation by generation (§9). Byte 0 begins the
constant 16-byte **front signature block** (§6.1). The final 64 bytes of
the file are the live **trailer** (§6.2). Between them lie the
structures of every generation — stored-tile payloads, tile-index
regions, record extents (§5.2), each generation's directory, declared
padding, and each prior generation's trailer — appended generation by
generation; within each generation the directory, pre-trailer pad, and
trailer come last (§6.2, §9.2). The file size of a conforming file
equals the live trailer's committed file length F, and F is a multiple
of 64 (§6.2). `[R-CNT-01]`

> **Example.** The smallest conforming file is 128 bytes:
> front block [0, 16); an empty directory — zero records under
> metadata-codec *none*, so 4 bytes holding the CRC-32C of zero bytes,
> `0x00000000` — at [16, 20); 44 bytes of zero padding; trailer at
> [64, 128). It contains no layers (a valid, empty file).

#### 5.2 Byte coverage

Every byte of a conforming file belongs to exactly one of: the front
signature block; a structure — stored-tile extent, tile-index region,
record extent (bytes referenced by a record's extent slot, §7.2 — in
format major 1, tile-index regions and user-metadata extents),
directory, or trailer — of exactly one generation (the generation whose
commit appended it); or **declared padding** of exactly one generation.
A file containing bytes claimed by no class is not a conforming file.
`[R-CNT-02]` Declared padding — the alignment gaps of aligned or
slab-declared layers (§16) and each generation's pre-trailer pad — MUST
be zero bytes; writers MUST NOT emit nonzero padding, and a verifier
MUST treat nonzero padding as a validity error at file scope.
`[R-CNT-03]`

**Superseded structures** — structures of prior generations no longer
reachable from the live trailer via the live directory's records,
extent slots, and tile-index entries — are **dead space**: readers MUST
NOT interpret them on the default read path (§9.5), verifiers classify
them via generation enumeration (§9.7), and only compaction (§20)
reclaims them. `[R-CNT-21]` Dead space is a privacy consideration
(§23).

> **Note.** Coverage is checked by verifiers, never by readers: a
> reader's obligations never require enumerating prior generations.
> Conforming writers produce partitioned files by construction — the
> commit protocol (§9.2) appends nothing it does not declare.

### 6. Front Signature Block and Trailer

#### 6.1 Front signature block

Bytes [0, 16) of every file, constant in every format major version:

| Offset | Size | Value | Class |
|---|---|---|---|
| 0 | 8 | `89 54 41 52 4E 0D 0A 1A` (`\x89`, "TARN", CR, LF, ctrl-Z) | structural |
| 8 | 8 | zero | structural (reserved) |

Writers MUST emit exactly these 16 bytes. A local reader or content
sniffer MUST verify the full block by byte equality before other
processing and MUST treat any mismatch as reject-file; a remote reader
MAY defer or omit this check (its open path is anchored at the trailer,
§6.2, and the two-request accounting of §6.4 does not include the front
block). `[R-CNT-04]`

> **Rationale.** The signature is engineered against transport
> corruption: the high-bit byte catches 7-bit stripping, CR LF catches
> line-ending translation, ctrl-Z stops accidental console display.

#### 6.2 Trailer

The trailer occupies the final 64 bytes of the file, beginning at a
64-aligned offset (equivalently: F mod 64 = 0). Its layout:

| Offset | Size | Type | Field | Class | Valid values |
|---|---|---|---|---|---|
| 0 | 8 | bytes | trailer magic | structural | `8A 4E 52 41 54 0D 0A 1A` (`\x8A`, "NRAT", CR, LF, ctrl-Z) |
| 8 | 2 | u16 | version_major | structural | 1 (0 invalid; others: §6.3) |
| 10 | 2 | u16 | version_minor | structural | any (see §6.3) |
| 12 | 4 | u32 | flags | structural | bits 0–15 incompat lane; bits 16–31 ignore lane (§6.3) |
| 16 | 8 | u64 | generation | semantic | ≥ 1 |
| 24 | 8 | u64 | dir_offset | structural | ≥ 16 |
| 32 | 8 | u64 | dir_length | structural | ≥ 4; dir_offset + dir_length ≤ F − 64 |
| 40 | 8 | u64 | committed_file_length | structural | = F; multiple of 64 |
| 48 | 8 | u64 | file_id | semantic | ≠ 0 |
| 56 | 1 | u8 | metadata_codec | structural | 1 = none, 2 = zstd (0 invalid) |
| 57 | 3 | bytes | pad | structural | zero |
| 60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes [0, 60) |

Writers MUST place the directory so that only the zero pre-trailer pad
— fewer than 64 bytes — lies between the directory's end and the
trailer; a verifier MUST treat a violation as a validity error at file
scope (readers are not obligated to check the gap bound; their check
is the dir-bounds rule of `[R-CNT-06]`). `[R-CNT-05]`

> **Note.** The trailer magic's first byte differs from the front
> signature's, so a recovery scan (§9.6) never matches the front
> block.

A reader MUST validate, in order: the trailer magic; the trailer CRC;
the version gate (§6.3) — only these touch fields whose positions are
fixed across all majors (`[R-CNT-24]`) — and then, those gates passed,
MUST validate all of the following before acting on the fields
involved: the flag gates (§6.3); committed_file_length equals the file
size (for a remote reader, the size reported by its transport) and is
a multiple of 64; dir_offset ≥ 16; dir_length ≥ 4; dir_offset +
dir_length ≤ F − 64; generation ≥ 1; file_id ≠ 0; metadata_codec is a
defined value; pad bytes zero. Any failure is reject-file.
`[R-CNT-06]`

#### 6.3 Version and flag gates

A reader MUST reject-file when version_major is 0 (invalid) or is a
major it does not implement, and the diagnostic for an unimplemented
major SHOULD be distinct from both "not a TARN file" and "corrupt"
(e.g. "TARN format major N; this reader supports major 1") — a reader
that reports an unimplemented major as corruption misleads users into
discarding files that current software reads. A reader MUST NOT reject
a file for its version_minor: minor releases are additive-only, and
all feature gating is structural (records, enums, flags). `[R-CNT-07]`

In every format major version, permanently: the final 64 bytes of a
file contain the trailer magic at F − 64, version_major and
version_minor at F − 56, and a CRC-32C at F − 4 covering bytes
[F − 64, F − 4); and the front signature block (§6.1) is constant. A
future major MAY redefine only the remaining 48 trailer bytes and MUST
NOT grow the trailer; additional space comes from structures placed
before it. The format-major-1 trailer has zero slack: every byte is
assigned. `[R-CNT-24]`

Flags: a reader MUST reject-file on any set bit it does not implement
in the incompat lane (bits 0–15), and MUST ignore all bits in the
ignore lane (bits 16–31). In format major 1 no flag bits are defined:
a writer creating a file MUST write flags = 0. An updater MUST copy
forward unknown ignore-lane bits of the file it modifies and MUST NOT
clear them; an updater encountering an unknown incompat-lane bit is a
reader first, and therefore rejects the file before modifying
anything. `[R-CNT-08]`

#### 6.4 Remote open accounting

The baseline remote open is two requests, each with an exact target:
(1) fetch the final 64 bytes; validate per §6.2–§6.3; (2) fetch
[dir_offset, dir_offset + dir_length); verify and decode per §7.1. A
reader MAY instead speculatively fetch a suffix window in one request
and use containment: if the fetched buffer contains the directory
region, request 2 is unnecessary. Writers SHOULD keep dir_length plus
the pre-trailer pad plus 64 within 65,536 bytes so that a 64 KiB
suffix fetch captures trailer and directory together; a larger
directory is conforming and merely costs the second request.
`[R-CNT-09]`

A remote reader MUST handle a 200 response to a range request (abort
or accept the full body deliberately — never treat the body prefix as
the requested range) and SHOULD fall back to a size probe plus an
absolute range on transports without suffix-range support — without
the fallback, remote open fails outright on such transports. The size
a remote reader compares against committed_file_length MUST be
transport-authoritative (a full-response content length, the complete
length of a range response, or a size probe); a reader that cannot
obtain one MUST probe separately or fail the open, and MUST NOT
substitute the trailer's committed_file_length for the transport size.
`[R-CNT-10]`

### 7. Metadata Directory and Records

#### 7.1 Directory region

The directory region is dir_length bytes at dir_offset. Its final 4
bytes are a CRC-32C over the preceding dir_length − 4 bytes exactly as
stored. A reader MUST verify that CRC before any other use of the
region (mismatch: reject-file, ADR-0031), then decode the covered
bytes per the trailer's metadata_codec (*none*: the bytes are the
record sequence; *zstd*: exactly one RFC 8878 frame whose decoded
output is the record sequence), then parse records. A decode failure —
covered bytes that are not exactly one well-formed frame of the
declared codec, or bytes of the covered region remaining after the
frame — is a validity error at the directory's owning scope
(reject-file). `[R-CNT-11]` The owning scope of the directory is the
file.

metadata_codec governs exactly two structure kinds: the directory
region and user-metadata extents (§18). It never applies to the
tile-index region, which is always stored raw so that it can be
range-fetched (§15), nor to tile payloads, whose codec is the layer's
codec field (§17). `[R-CNT-25]`

#### 7.2 Record framing

The record sequence is zero or more records, concatenated. Each record
is a 24-byte header followed by inline_length bytes of inline payload:

| Offset | Size | Type | Field | Class |
|---|---|---|---|---|
| 0 | 2 | u16 | type (0 invalid) | structural |
| 2 | 2 | u16 | flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved | structural |
| 4 | 4 | u32 | inline_length | structural |
| 8 | 8 | u64 | extent_offset | structural |
| 16 | 8 | u64 | extent_length | structural |

A record whose header or inline payload would extend past the end of
its containing record sequence is a validity error at the sequence's
owning scope: reject-file for the directory's top-level sequence,
reject-layer for a layer record's sub-record sequence (§7.4). Type 0
is not an unknown type: a reader MUST treat a record of type 0 as a
validity error at the same scope. Reserved flag bits: writers MUST
emit zero; readers MUST ignore them. Writers MUST NOT emit the
combination MU = 1 with PE = 0; a reader or updater encountering it
MUST treat the record as PE = 1 (never silently deletable).
`[R-CNT-12]`

The **extent slot** (extent_offset, extent_length): (0, 0) means no
extent. Any other combination with either half zero, an
extent_offset < 16, an extent extending past F − 64, or an
overflowing sum is a validity error at the scope the record governs
(§7.3): the layer for a layer record and for sub-records, the file for
other top-level records — a malformed slot on a layer record is
therefore reject-layer, consistent with `[R-CNT-17]`. For a record
with MU = 0, the extent slot is its only sanctioned reference to bytes
outside the record sequence: neither its inline payload nor its extent
contents encode offsets or lengths of other file bytes — this is what
lets a compactor relocate an unknown ancillary's extent without
parsing it (§20). Records with MU = 1 carry further references only
where this specification or registry review (§10) defines them; the
layer record's tile index (§15), whose entries reference stored-tile
extents, is such a case. Extents are owned exactly once: within the
live committed state — all structures reachable from the live trailer,
whichever generation's commit appended them — no two extent slots and
no two structures overlap; a verifier MUST treat an intra-layer
overlap as reject-layer and any other overlap — across layers, or
touching any metadata structure — as reject-file (readers are not
obligated to detect overlap, which requires whole-directory
knowledge). `[R-CNT-13]`

Record semantics MUST NOT depend on record order: readers MUST NOT
infer meaning from the position of a record within the sequence, and
multiplicity rules are per type — in format major 1: any number of
layer records (zero is valid: an empty directory is a conforming
generation); at most one file-scope user-metadata record, a second
being a validity error at the directory's scope (reject-file); and at
most one user-metadata sub-record per layer record, a second being a
validity error at layer scope. `[R-CNT-14]`

An unknown record type at file scope: MU = 1 → reject-file; MU = 0 →
ignore-record. Updater obligations for unknown records are §20's
subject. `[R-CNT-15]`

#### 7.3 Record types of format major 1

| Type | Name | Scope | Flags (fixed by registry) |
|---|---|---|---|
| 0x0001 | layer | file (container for layer scope) | MU = 1, PE = 1 |
| 0x0002 | user metadata | file when top-level; layer as sub-record | MU = 0, PE = 1 |

All other type values are unassigned (registry and experimental
ranges: §10).

For the record types this specification registers, writers MUST emit
exactly the flag values fixed in the table above. A reader MUST apply
a known type's specified semantics regardless of its stored MU and PE
bits — a flipped stored bit never changes conforming behavior — and a
verifier SHOULD report the mismatch; unreported, a writer defect
propagates silently to consumers that do not know the type. Stored
flag bits are authoritative only for record types the consuming tool
does not implement (`[R-CNT-15]`). `[R-CNT-22]`

#### 7.4 The layer record

A layer record's extent slot addresses the layer's tile-index region
(§15); a layer with zero addressed tiles has extent (0, 0). Its inline
payload is, in order:

| Field | Type | Constraint |
|---|---|---|
| name | u8 len + bytes | §4.6 name rules; unique per `[R-ENC-15]` |
| layout | u8 | 1 = interleaved, 2 = planar (0 invalid; others reserved); semantics §14 |
| linearization | u16 | §11.4 |
| codec | u16 | §17 (0 invalid) |
| filter | u16 | 1 = none, 2 = byte-shuffle (0 invalid; others reserved; §17) |
| alignment A | u64 | 0 = none declared; else a power of two (§16) |
| slab S | u64 | 0 = no slab declaration; else run length in tiles (§16) |
| slab alignment A_slab | u64 | 0 when S = 0 (`[R-CNT-23]`); else a power of two (§16) |
| rank d | u8 | ≥ 1 |
| channel count C | u16 | ≥ 1 |
| d dimension entries | name (u8 len + bytes) · extent u64 · tile extent u64 | §11.1 |
| C channel entries | name (u8 len + bytes) · type u16 · fill (u8 len + bytes) | type per §12; fill length equals the type's element size (`[R-CNT-23]`), so fill parses without type knowledge and validates with it |
| index_encoding | u8 | 1 = raw-segmented (0 invalid; 2 reserved; ≥ 0x80 experimental; §15) |
| entry_count | u64 | equals the addressed-tile count (§11.2, `[R-CNT-17]`) |
| crc_of_crc_array | u32 | CRC-32C over the index's segment-CRC array (§15); 0 when entry_count = 0 (`[R-CNT-23]`) |
| sub-records | zero or more records (§7.2 framing) to the end of the inline payload | layer scope by containment |

The owning scope of a layer record's inline payload is the layer.
Writers MUST NOT emit a field violating a constraint in the table
above; a reader MUST treat any such violation — including a reserved
or unassigned layout, codec, filter, index_encoding, or channel-type
value (the value sets are §14, §17, §15, and §12's subjects), a
nonzero A_slab with S = 0, a fill whose byte length differs from its
type's element size, or a nonzero crc_of_crc_array with
entry_count = 0 — as a validity error at layer scope, except where
another rule assigns a different scope (a duplicate layer name is file
scope, `[R-ENC-15]`). `[R-CNT-23]`

Declaring both A ≠ 0 and S ≠ 0 is a validity error at layer scope: the
per-tile alignment and slab declarations are mutually exclusive
(§16). `[R-CNT-16]` Under index_encoding 1, extent_length MUST equal
entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is
0); a mismatch, or an entry_count that does not equal the
geometry-derived addressed-tile count, is a validity error at layer
scope. `[R-CNT-17]`

The inline payload MUST parse exactly: the fixed fields, the d
dimension entries, the C channel entries, and the trailing fixed
fields MUST lie entirely within the inline payload, and the remaining
bytes MUST parse as zero or more complete sub-records under §7.2's
framing with no residue; any overrun, truncation, or residue is a
validity error at layer scope. Sub-records are layer-scope records; a
sub-record MUST NOT itself contain records (nesting depth beyond two
is a validity error at layer scope), and an unknown sub-record type
with MU = 1 is reject-layer — never reject-file — and with MU = 0 is
ignore-record. `[R-CNT-18]`

### 8. Integrity

#### 8.1 Coverage map

Every field of every structure is covered by exactly one checksum —
the equality-checked front signature block being §4.5's sole exception
— per this map. All checksums are CRC-32C over bytes exactly as
stored. `[R-CNT-19]`

| Structure | Checksum location | Covers |
|---|---|---|
| Front signature block | none — checked by byte equality (§6.1) | — |
| Trailer | trailer bytes [60, 64) | trailer bytes [0, 60) |
| Directory region | final 4 bytes of the region | the preceding dir_length − 4 bytes (the encoded bytes exactly as stored, before decoding) |
| Tile-index region | the per-segment CRC array, itself covered by the layer record's crc_of_crc_array | index entries, per segment (§15) |
| Stored tile | the crc field of its index entry | the tile's stored bytes |
| User-metadata extent | final 4 bytes of the extent | the preceding bytes (the encoded bytes exactly as stored, before decoding) |

#### 8.2 Verification obligations and outcomes

The chain of trust is strictly ordered: trailer → directory → (per
layer) crc_of_crc_array → segment CRC array → index segment → index
entry → stored tile. A reader MUST verify each link before acting on
any field the link covers (`[R-ENC-05]`, `[R-ENC-10]`); failed
verification takes the outcome of ADR-0031's table: trailer or
directory → reject-file; any of a layer's index cross-checks
(`[R-CNT-17]`), CRC array, or segments → reject-layer; a stored tile's
CRC → reject-tile; a user-metadata extent's CRC → ignore-record, and
readers SHOULD report the loss (silent metadata loss defeats the
record's purpose). `[R-CNT-20]`

Verification is not optional: no in-file flag disables it, and a
reader that skips it is not a conforming reader.

> **Note.** Implementations are free to offer explicitly labeled
> non-verifying modes for trusted storage; such modes are outside this
> specification's conformance classes. Checksums detect corruption,
> not tampering (§4.5).

### 9. Lifecycle and Consistency

#### 9.1 Committed-prefix immutability

A TARN file changes only by **commit**: an append-only transaction
that extends the file and never modifies a committed byte. Bytes in
[0, F) — F being the live trailer's committed file length — are
immutable: a writer MUST NOT modify them, and every conforming
mutation of a file is either a commit (§9.2) or a whole-file rewrite
under a new file_id (compaction, §20). `[R-LIF-01]` The owning scope
of the structures this section defines is the file.

#### 9.2 The commit protocol

A writer performing a commit MUST, in order: (1) begin writing at
exactly F (§9.4); (2) append new stored-tile payloads and tile-index
regions for the layers it changes, and any new record extents
(file-scope or layer-scope), in any order satisfying §5.2's coverage
classes; (3) append the new complete directory — re-emitting every
retained record per §20's preservation rules — followed by its CRC;
(4) make steps 1–3 durable (a storage barrier such as fdatasync, or
the platform equivalent needed to order writes against power loss);
(5) append the zero pad to the next 64-byte boundary and the new
trailer, with generation one greater than the prior trailer's and
committed_file_length equal to the new end; (6) make the trailer
durable. `[R-LIF-02]`

On creation there is no prior trailer: the writer first emits the
front signature block (§6.1), then performs steps 2–6 beginning at
offset 16, with generation 1.

> **Note.** Where barriers are weaker than assumed, safety degrades
> from "torn commits are invisible" to "torn commits are detected":
> §8's chain still catches every inconsistent state loudly — the
> outcome is rejection at the affected scope, never silent corruption.

#### 9.3 Generations, file_id, caching

Each commit's trailer carries generation g ≥ 1, increasing by exactly
1 per commit, and the file_id chosen at creation (nonzero; the
creating writer SHOULD draw it from a cryptographically random source
— a predictable or reused file_id lets two distinct files collide in
the (file_id, range)-keyed caches this rule licenses, serving bytes
from the wrong file). Because committed bytes are immutable, any byte range fetched under generation g remains
byte-correct under every later generation of the same file_id: caches
keyed (file_id, range) never invalidate, and revalidation is one
64-byte trailer read — same generation, everything cached remains
valid; higher generation, refetch the directory; different file_id or
lower generation, treat as a different file. `[R-LIF-03]`

#### 9.4 Recovery before re-append

A writer beginning a commit against an existing file MUST establish F
by validating the trailer in the final 64 bytes of the physical file
(§6.2). If that validation fails, the file is torn: the writer MUST
NOT append, and locating the last committed state is the deliberate
recovery operation of §9.6 — never an implicit step of opening for
append. Once F is established (directly, or by recovery whose output
has been re-verified), a writer whose physical file is longer than F
MUST either truncate to F before step 1 of `[R-LIF-02]`, or overwrite
from F and truncate the physical file to the new
committed_file_length no later than step 6 — so that after any commit
completes, the physical file length equals committed_file_length, and
bytes beyond a committed length never survive into any committed
state. `[R-LIF-04]`

#### 9.5 Concurrency and the default read path

One writer at a time, any number of concurrent readers: this
specification defines no multi-writer coordination, and external
locking is the deployment's responsibility. A reader opening a file
takes the trailer at the current end of file as its snapshot: the
generation it validates is immutable, so its entire read session is
consistent without further coordination. The default read path is
trailer-at-end-or-fail: a reader that finds no valid trailer in the
final 64 bytes MUST report the file torn or invalid and MUST NOT scan
backward. `[R-LIF-05]`

> **Note.** On shared filesystems with attribute-cache staleness, a
> reader may retry a failed trailer validation before concluding the
> file is torn — a fresh size with stale tail pages is transient. A
> file being appended to is not guaranteed remotely openable until its
> commit completes; publishers serving live files should commit
> quickly, use checkpoint commits, or publish by copy-then-swap.

#### 9.6 Recovery scan (not a reader behavior)

Recovery tools and verifiers — never conforming readers on the default
path — locate commit states as follows: probe backward at 64-aligned
offsets o for the trailer magic; on a match, require the trailer CRC
to verify and committed_file_length = o + 64. The nearest-to-end valid
candidate is the last committed state; truncating to it recovers the
file. Generation enumeration for coverage verification (§5.2) is the
same probe continued to offset 0. Two cautions are normative for
tools: a tile payload can deliberately contain a byte string that
mimics a valid trailer, so recovery output MUST be re-verified as a
whole file (§8) before being trusted; and truncation of a file to an
earlier commit boundary is indistinguishable in-format from that
earlier version — rollback detection requires out-of-band state (an
expected generation or a detached hash). `[R-LIF-06]`

Writers performing very large single commits SHOULD emit intermediate
checkpoint commits (a directory and trailer mid-stream, ~a few KiB
each); the consequence of not doing so is that a torn multi-hour
append is recoverable only by scanning back across its entire length.
`[R-LIF-07]`

#### 9.7 Coverage verification

A verifier checking `[R-CNT-02]`'s partition proceeds as follows.
(a) Enumerate trailer candidates by §9.6's probe continued to offset
0, and accept only the set forming a **chain**: exactly one candidate
per generation number from the live generation g down to 1, with
committed_file_lengths strictly increasing, each equal to its
candidate's offset + 64, and each candidate's directory bounds inside
its own committed length. A candidate outside the chain is discarded
as a payload mimic; a duplicate or missing generation number in the
chain is a coverage-verification failure at file scope. (b) Attribute
to generation k the byte range [F_{k−1}, F_k), with F₀ = 16 (the front
block belongs to no generation). (c) For each generation k, the
claimed set is: the structures referenced transitively from generation
k's directory — extent slots, tile-index regions, and index entries —
that lie within [F_{k−1}, F_k), plus that directory, its declared
padding, and its trailer. Every byte of [F_{k−1}, F_k) MUST be claimed
exactly once. (d) A verifier that cannot verify an enumerated
generation's trailer, directory, or tile index cannot establish
coverage and MUST treat the file as nonconforming (ADR-0030).
`[R-LIF-08]`

> **Note.** Step (c)'s in-range restriction is what makes attribution
> decidable: a generation's directory may reference structures
> appended by earlier commits (retained layers), but those bytes are
> claimed by the generation that appended them, not by the generation
> that retains them.

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
