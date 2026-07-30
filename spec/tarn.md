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

Prefixes: `CNF` (conformance), `ENC` (encoding), `CNT` (container
structures), `LIF` (lifecycle and consistency), `EXT` (extension points
and registry), `IDX` (tile index), `SLB` (slabs and alignment), `TYP`
(types and fill), `SER` (tile serialization), `COD` (codecs and filters),
`MTA` (user metadata), `RDR` (reading), `WRT` (writing and updating),
`ERR` (error register), `SEC` (security), `PRV` (privacy). New prefixes
are added by ADR when a section needs one; existing prefixes are never
reassigned.

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

*[Reserved — Batch 2: noun set per ADR-0002, including addressed vs
stored tiles; the reference array as conformance target.]*

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
files they process — MUST treat any computation over integers obtained
from a file (sums of offsets and lengths, products of extents, index
computations) whose mathematical result would exceed 2⁶³ − 1 as a
validity error at the owning scope, and MUST NOT act on a wrapped or
truncated result. `[R-ENC-04]` A reader MUST NOT allocate, seek, or
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

*[Reserved — Batch 2: grid math, uniform tiles, linearization per
ADR-0011/0020.]*

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
