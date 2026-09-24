# The TARN Format Specification

**Status: working draft — nothing here is stable.** This document is being
drafted batch by batch under the process in [PLAN.md](../PLAN.md). All
sections are drafted; the document has not yet passed acceptance
review. Decisions encoded here are recorded, with their rationale, in
the ADRs in [docs/decisions/](../docs/decisions/README.md); where an
ADR and this document diverge, this document governs.

License: CC BY 4.0 (see [LICENSE-SPEC](../LICENSE-SPEC)).

---

## Part 0 — Preliminaries

### 1. Introduction

TARN is a single-file container for tiled, N-dimensional arrays. A file
holds a set of named layers; each layer is a grid of samples cut into
tiles, and each tile is stored, checksummed and read as a unit. The
format is designed to be read directly from remote storage by byte range
and to be implemented from this document alone.

Five goals shape the design:

- **Random access without a server.** Opening a file, and reading any
  one tile of it, each take a small fixed number of range requests,
  whatever the size of the file.
- **Integrity by default.** Every structure whose contents this
  specification defines is checksummed, and verification is a reader
  obligation with no flag that disables it. Corruption is detected
  at the finest scope it damages, so one bad tile does not condemn a
  file.
- **Append without rewriting.** A file is updated in place only by
  appending a commit; committed bytes are never modified, so an
  interrupted write cannot damage the state before it. Superseded bytes
  stay in the file until a compaction reclaims them.
- **Defined behavior at the edges.** Every boundary case this document
  names has a stated answer, and every violation it names has a stated
  consequence.
- **A closed core with an open edge.** The sample types, codecs and
  filters are closed lists, and there is no subset of the core a
  conforming reader can decline; the format grows through a fixed set
  of extension vehicles and a registry.

TARN is not a database: it has no transactions, no queries, and one
writer at a time. It is not an image format: it carries no colour model,
orientation, or display semantics. It is not a compression format: its
codecs are references to external specifications. It provides no
confidentiality and no authenticity: its checksums detect accidental
corruption, not tampering.

**How to read this document.** Sections follow a fixed rubric where it
applies: purpose, byte-layout table, writer rules, reader rules, error
handling, worked examples. On-disk structures are presented as layout
tables whose columns suit the structure; §4.7 says what the columns
carry and classifies every field as structural or descriptive.

### 3. Terminology and Data Model

#### 3.1 Terms

The following terms are used throughout this specification with exactly
these meanings.

- **file** — a single TARN artifact: a byte sequence satisfying this
  specification's file-level requirements.
- **front signature block** — the constant 16 bytes at offset 0 (§6).
- **generation** — one committed state of a file (§9). No field
  numbers generations.
- **trailer** — the fixed-size 64-byte structure that commits a
  generation (§6); each commit appends one, and the *live* trailer
  occupies the final 64 bytes of the file.
- **directory** — the consolidated metadata structure through which
  everything else in a generation is reached: a sequence of records
  (§7), including every layer record, followed by its checksum, located
  from the trailer. Each commit appends a *complete* directory;
  unqualified, *the directory* means the live generation's.
- **layer** — a named N-dimensional array within a file. All layers of a
  file are equally first-class.
- **dimension** — one axis of a layer's grid, having a name (§4.6), an
  **extent** (the number of sample positions along the axis), and a
  **tile extent** (the number of sample positions per tile along the
  axis). Dimensions are declared in order, and the declared order fixes
  the sample order on disk: within a tile the last-declared dimension
  varies fastest, and tile ordinals follow the same order (§11.4).
- **rank** — a layer's number of dimensions, written *d*.
- **channel** — a named, typed per-sample value of a layer (§12).
  Channels are declared in order; a channel's **index** is its 0-based
  position in that order, which fixes where the channel's value sits
  within each interleaved sample (§14) and where its tiles fall in a
  planar layer's index (§11.4).
- **channel layout** — whether a layer's channels are stored together
  within each tile (*interleaved*) or each channel is tiled separately
  (*planar*).
- **sample** — the tuple of one value per channel at one coordinate.
- **coordinate** — a *d*-tuple (x₀, …, x_{d−1}), in declared dimension
  order, with 0 ≤ xᵢ < Eᵢ, identifying one sample position of a layer
  with extents (E₀, …, E_{d−1}).
- **tile** — the unit a tile-index entry addresses: in an interleaved
  layer, one cell of the tiling grid carrying all channels; in a planar
  layer, one cell of the grid for one channel. Every tile of a layer has
  the same logical shape, a block of ∏ Tᵢ sample positions (§11.3).
- **addressed tile / stored tile** — a tile is *addressed* in a
  generation if that generation's tile index has an entry for it: the
  tiles of the layer's grid under the geometry that generation declares
  (§11.2, §15). It is *stored in a generation* if and only if that entry
  is not the sentinel (§15); unqualified *stored* means stored in the
  live generation. Superseded payload bytes from earlier generations do
  not make a tile stored. An addressed tile that is not stored reads as
  fill (§13).
- **fill value** — the value that a channel's samples take wherever the
  tile carrying that channel is not stored (§13).
- **slab** — a declared run of consecutive stored tiles kept physically
  contiguous as one I/O unit (§16).
- **tile index** — the per-layer table with one entry per addressed
  tile, locating and checksumming the stored ones and marking the rest
  with the sentinel (§15).
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
> payloads, so appenders, and rewriters that carry a layer forward,
> operate on files whose layers they cannot decode — that
> independence is load-bearing for the updater rules of §7 and §20.

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

The prefixes:

| Prefix | Abbreviates |
|---|---|
| `CNF` | conformance |
| `MDL` | terminology and data model |
| `ENC` | encoding |
| `CNT` | container structures |
| `LIF` | lifecycle and consistency |
| `EXT` | extension points and registry |
| `GEO` | layers, dimensions, and tiling |
| `IDX` | tile index |
| `SLB` | slabs and alignment |
| `TYP` | types and fill |
| `SER` | tile serialization |
| `COD` | codecs and filters |
| `MTA` | user metadata |
| `RDR` | reading |
| `WRT` | writing and updating |
| `ERR` | error register |
| `SEC` | security |
| `PRV` | privacy |
| `VEC` | conformance vectors |

New prefixes are added by ADR when a section needs one; existing
prefixes are never reassigned.

#### 2.3 Conformance classes

Conformance is defined for five classes.

- **Conforming TARN file.** A byte sequence satisfying every file-level
  requirement of this specification. File conformance is a pure predicate
  on bytes: it does not depend on any reader, writer, or environment.
  It is always conformance to a stated format major version. This
  document defines format major 1, and a file declaring another major
  is neither conforming nor nonconforming under it save as to the
  conditions that reach it (`[R-CNF-13]`): a reader refuses such a
  file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is
  not a finding about its bytes, while the failure of a reaching
  condition is.
  A few obligations this specification places on writers govern their
  *conduct* rather than their output — where a value is published,
  which registry version a writer targets (§10.3, §18.3), or the
  barriers a commit performs (§9.2) — and a file
  is never nonconforming by virtue of one: conduct rules bind the
  actor, the predicate binds the bytes. A writer obligation whose
  violation this specification expressly declares not to be a
  file-conformance violation binds the actor in the same way; §6.3's
  flags rules against a set ignore-lane bit (a creator's flags = 0,
  and an updater's copy-forward and set-no-other,
  §20.3 step 6 and §20.5), §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's
  pad, and §20.3 step 4's bar on the fixed declarations of a layer
  that stores a tile are the cases this text states, and each is
  declared where it arises rather than enumerated here. `[R-CNF-02]`
- **Conforming reader.** A reader MUST accept every conforming file of
  a format major version it implements, carrying no top-level record of
  a type it does not implement with MUST_UNDERSTAND = 1 — in a
  conforming file such a type is necessarily from the experimental range, since
  a reserved-range type carrying MU = 1 is itself a violation — and
  none of whose values exceeds the minimum guarantees of §21's
  limits table (§21.9's `[R-ERR-04]` governs a refusal on that last
  ground; §21.6's closing paragraph names the other two),
  and MUST handle every codec and filter that §17 designates as core,
  both channel layouts (§14), every sample type that §12 designates
  as core, every user-metadata encoding §18.2 assigns, and both
  record types §7.3 registers.
  There are no subset profiles: software that declines to support a core
  codec, a core filter, either channel layout, a core sample type, an
  assigned user-metadata encoding, or a registered record type is not
  a conforming reader, even if it reads all other conforming files correctly.
  `[R-CNF-03]` A reader MUST detect every violation the error
  register (§21) assigns to the reader as its detector, and apply the
  outcome class this specification assigns to each; a violation whose
  assigned detector is the verifier imposes no reader obligation
  (§19.2, `[R-RDR-02]`), though a reader detecting one MAY reject the
  file (`[R-CNF-12]`). A reader MUST NOT heuristically repair a
  violating structure or infer values this specification does not
  define. `[R-CNF-04]`
- **Conforming writer.** A writer MUST emit only conforming files.
  `[R-CNF-05]` Writer conformance is semantic: this specification does not
  promise canonical bytes, and two conforming writers given identical
  input MAY produce different conforming files.
- **Conforming updater.** A tool that modifies an existing file, or
  as a rewriter writes a new one from it (§20.1), without
  necessarily understanding all of its content. An updater MUST satisfy
  every writer requirement for the bytes it produces, and additionally
  MUST honor the preservation obligations of §20.4 — which govern every
  record type, not only those it does not understand. Its tiers, the
  appender and the rewriter, are §20.1's. `[R-CNF-06]`
- **Conforming verifier.** A reader that additionally checks every
  file-level requirement — including those ordinary readers are
  exempted from — and certifies conformance. Verifiers and updaters are
  readers of the files they process and inherit every reader
  obligation. A verifier reports one of three verdicts: *conforming*,
  *nonconforming*, or *cannot establish* — the last where some
  requirement is one it is unable to check on a capability or
  resource ground, as when the file names a
  format major version it does not implement, when a record carries
  MUST_UNDERSTAND = 1 with a type it does not implement (§21.6), when
  it cannot execute a codec or filter (`[R-COD-11]`), when it
  declines a layer's or a tile's decode on resource grounds and so
  cannot check §14's decoded-content obligations (`[R-ERR-04]`,
  `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a
  user-metadata document (`[R-MTA-09]`). A user-metadata document
  under an experimental-range encoding — one this specification does
  not assign and a conforming file can carry (§21.6) — is not such a
  ground: no content rule attaches there, so nothing is left
  unchecked, and certification is unaffected (`[R-MTA-10]`); encoding
  0 and a reserved value are violations (§21.5, R1).
  *Cannot establish* is not a finding that the file is nonconforming,
  and a verifier MUST NOT certify a file it reports that way. An
  established violation takes priority: a verifier that has
  established any violation reports *nonconforming*, however many
  requirements it was unable to check, and *cannot establish* is
  available only to a traversal that established no violation. A
  verifier MUST report each requirement it was unable to check on a
  capability or resource ground, naming the requirement and the
  ground, whichever of the three
  verdicts it reports; that per-requirement report constrains the
  report and not the verdict, as *unexamined* does below.
  A verifier MAY stop at the first violation it finds; one that does
  MUST report each scope it did not examine as *unexamined*, which is
  not a finding that the scope is clean. *Unexamined* is neither a
  verdict nor *cannot establish* — it constrains the report, not the
  verdict.
  `[R-CNF-11]`

A **condition** this specification names — one malformed state, as
§21.1 individuates them, and not the requirement that defines it —
**reaches** a file declaring a format major other than 1 when, and
only when, the invariant it violates is one `[R-CNT-24]` fixes in
every format major version. A file whose version_major is 0 declares
no major at all (§6.3): it is not a file declaring a format major
other than 1, no reach question arises for it, and `[R-CNT-07]`
rejects it (§21.2, F18). Reach is per condition because a single
requirement can state several: `[R-CNT-06]` states nine, of which the
trailer magic and the trailer CRC assert invariants `[R-CNT-24]` fixes
and the other seven do not. The test is the invariant asserted, not
the bytes read: a check that consumes bytes a future major is free to
redefine can still assert only a fixed invariant. A reader MUST apply
every reaching condition to a file whatever major it declares — an
exemption the condition's governing requirement grants on a ground
other than the declared major applies unchanged, `[R-CNT-04]`'s
residency exemption among them — and MUST treat its failure as
reject-file on the ground of the requirement stating it rather than on
capability grounds; the distinct diagnostic
`[R-CNT-07]` asks for is owed where every reaching condition is
satisfied and the declared major is one the reader does not implement.
A verifier that establishes such a failure reports *nonconforming*,
whatever major the file declares and whether or not it implements that
major: the invariant broken is one that major shares (`[R-CNT-24]`),
so the finding is not relative to format major 1. Every other
condition this specification names is one of a structure this text
defines for format major 1 alone; it is not assessed against a file
declaring another major, no violation of it is established there, and
no §21 row restating it records such a file. `[R-CNF-13]`

> **Note.** The test is the invariant a condition violates, not the
> fields it reads, and three rows show why the distinction carries the
> weight. §21.2's F14 reaches although the bytes it checksums include
> fields a future major may redefine: it consumes them as CRC input
> and asserts only `[R-CNT-24]`'s CRC-32C at F − 4 over
> [F − 64, F − 4). F5 does not reach although its subject is the
> physical file size, which no major can redefine: the 128-byte floor
> it asserts is derived from a directory of at least 4 bytes at an
> offset of at least 16 and a 64-aligned F (`[R-CNT-27]`), and those
> are format major 1's. F15 does not reach although its Governing rule
> cell cites `[R-CNT-24]`: the trailer bytes it requires be zero are
> inside the 48 that rule lets a future major redefine.

#### 2.4 Outcome classes and owning scope

Every detectable file-conformance violation named by this
specification is assigned exactly one **reader outcome**: reject-file, reject-layer, reject-tile,
or ignore-record. `[R-CNF-07]` The same vocabulary is used for defined
conditions that are not violations (an unknown ancillary record is
*ignored*, not rejected). **preserve-verbatim** names an updater
obligation, orthogonal to reader outcomes: a record a reader ignores can
still be one an updater preserves.

| Outcome | Meaning |
|---|---|
| **reject-file** | The file is not usable; failure is reported for the whole file. A reader MUST NOT rely on any structure in it. |
| **reject-layer** | The affected layer's data and metadata are not usable; all other layers are unaffected. A reader MAY still list the file's layers, including the rejected one's name. The outcome is prospective: it bars further service from the layer, and does not retroactively invalidate content already returned under §19.2's validation timing (`[R-RDR-02]`). |
| **reject-tile** | The affected tile's data is not usable; a read of that tile reports failure. All other tiles, including neighbors in the same layer, are unaffected. |
| **ignore-record** | The record is skipped as though absent. Decoding of all stored data is unaffected. |
| **preserve-verbatim** | Binds updaters: the bytes are carried forward unmodified (relocated only as Part I permits). §20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows. |

Every structure this specification defines has exactly one **owning
scope** — file, layer, or tile — stated in the section that defines the
structure. The phrase "a validity error at the owning scope" means the
reader outcome for that scope: file → reject-file, layer → reject-layer,
tile → reject-tile. `[R-CNF-08]`

A reader MUST NOT return data as valid from a scope this specification
rejects and whose rejection this reader is obliged to detect
(`[R-RDR-02]`); in particular, a read of a rejected tile MUST NOT
silently return fill. `[R-CNF-09]`

A file is conforming only if it satisfies every requirement at every
scope: the outcome classes describe the blast radius of a violation
for readers, never degrees of file conformance, and a verifier
certifies only violation-free files. For a nonconforming file no
acceptance obligation exists — a reader MAY reject it upon detecting
any violation, including violations whose assigned detector is the
verifier. Deviation from a SHOULD is not a violation for this
purpose: §21's register enumerates MUST-level conditions only, and a
verifier reports a SHOULD deviation as an advisory that does not bar
certification. A verifier owes no search for one: §2.3's duty to
check every file-level requirement runs to MUST-level conditions,
and a SHOULD deviation is reported where the verifier observes it
and not hunted for. `[R-CNF-12]`

> **Note.** "Reject" prescribes the scope of unusability, not user
> interface: how failure is reported is implementation technique.

#### 2.5 Implementation limits

Every limit that affects which files are valid or which files a
conforming reader accepts lives in this specification, never only in an
implementation. Readers MAY enforce resource limits, but MUST accept any
conforming file within the minimum guarantees stated in §21's limits
table; writers MAY rely on those minimums; the table is §21.9.
`[R-CNF-10]`

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
offsets, dimension extents, and tile extents are `u64`, as is every
byte length this specification does not give another width where it
defines the field — a record's inline_length is a `u32` (§7.2), and
a name's or fill's length prefix a `u8` (§4.6, §7.4).
The valid range of every offset, length, extent, and count this
specification defines — entry counts and slab run lengths
included — is 0 to 2⁶³ − 1 inclusive; a reader MUST treat a value
above 2⁶³ − 1 in any such field as a validity error at the owning
scope. `[R-ENC-03]`

> **Rationale.** The reduced range costs nothing at realistic scales and
> lets implementations in languages with signed 64-bit integers operate
> without unsigned arithmetic gymnastics.

A reader — including any updater or verifier, which are readers of the
files they process — MUST treat any quantity this specification
**designates** a declaration-derived sum or product of integers obtained
from a file (offsets plus lengths, grid counts, tile counts,
sample-position counts, ordinals) whose mathematical value would exceed
2⁶³ − 1 as a validity error at the owning scope, and MUST NOT act on a
wrapped or truncated value. A designation is express, made by the
section that defines the quantity; an expression this specification
writes only inside a comparison, and names nowhere, is not a designated
quantity and no reader is obliged to form it.
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
`83 92 06 E3`. The CRC-32C of zero bytes is `0x00000000`. An
implementation whose checksum function does not reproduce these values
does not implement this specification's checksum.

A reader MUST verify the checksum covering a field before acting on
that field — where *acting on* means using its value to allocate,
seek, fetch, or select behavior; comparing a field against a constant
for validation is not acting on it, and an explicit validation order
(§6.2) governs where one is stated. `[R-ENC-10]` Every field of every
structure is covered by exactly one checksum, excepting the front
signature block (a constant whose check is equality, §6), the
terminal checksum fields of §8.1's map — the trailer, directory-
region, and user-metadata checksum fields — which are verified by
comparison and covered by no further checksum, and the extent of a
record of a type this specification has not assigned, which §8.1's
map covers by no checksum at all. Interior checksum
fields — each segment CRC array, each tile-index entry's crc field,
and each layer record's crc_of_crc_array — are both
comparison-verified and covered by
exactly one further checksum, as §8.1 maps. Which bytes
each checksum covers, and each
conformance class's verification obligations, are defined with the
structures that carry them (§8).

> **Note.** Checksums detect accidental corruption. They do not
> authenticate: an adversary who can modify bytes can recompute
> checksums. Authenticity requires detached signatures or hashes,
> outside this specification's scope.

#### 4.6 Strings and names

All strings are length-prefixed UTF-8. Each structure's layout table
states its prefix width, and every length prefix counts bytes — never
characters or code points. Writers MUST NOT emit byte sequences that are
not well-formed UTF-8; a reader MUST treat ill-formed UTF-8 in any
string as a validity error at the owning scope — except inside a
user-metadata document, where `[R-CNT-25]`'s quarantine governs and
the outcome is ignore-record. `[R-ENC-11]`

**Names** — the strings that identify layers, dimensions, channels, and
user-metadata keys — satisfy three further constraints. Writers MUST NOT
emit a name that violates any of them; a reader MUST treat such a name
as a validity error at the owning scope — except for a key inside a
user-metadata document, where `[R-CNT-25]`'s quarantine governs and
the outcome is ignore-record. `[R-ENC-12]` A name is:

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

Names are unique within their scope: layer names among a file's
layers, dimension names among a layer's dimensions, and channel names
among a layer's channels. The last two are separate namespaces, so a
dimension and a channel of one layer are permitted to share a name —
the ordinary way to name a channel after the axis it samples. Writers MUST NOT
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

Every field this specification defines is classified by what its
*value* determines. A field is **structural** if its value determines anything a
conforming reader or verifier does with the bytes it reads — where a
byte lies, how it decodes, what a decoded value is, or whether the
file, layer or tile is accepted at all, which is the sense
`[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use. It is
**descriptive** if it determines none of those, and a reader MUST NOT
alter decoding based on it; each descriptive field's definition states
what a reader does when the field contradicts the data it describes. In
format major 1 `version_minor` is the only descriptive field, and
every other field this specification defines is structural.
`[R-ENC-16]`

> **Note.** Layout tables for fixed-layout structures give, per field:
> byte offset within the structure, size, type, name, taxonomy class,
> and valid range, each table giving the columns its structure needs.
> A packed variable-length payload — the layer
> record's inline payload (§7.4) — has no fixed offsets to give; its
> table omits the offset, size and class columns, a field's size
> following from its type or its length prefix and each field's
> class from the definitions above. §6.1's block is a 16-byte
> constant, where a Value column replaces type, name and range, and
> §7.2 folds a field's range into its Field cell where it states one,
> a field's remaining bounds being stated in the rules below the
> table. A name is structural: a duplicate is a validity error at file
> or layer scope (`[R-ENC-15]`, F4, L9), and its length prefix is §7.4's
> framing, not its value. Every non-obvious encoding is followed by a worked numeric
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
regions the file's commits appended — stored-tile payloads,
tile-index regions, record extents (§5.2), the directory each commit
appended, and each prior generation's trailer — with the superseded
among them slack and no structure (§5.2), and slack wherever a
commit left a gap; a commit appends its own directory,
pre-trailer pad, and trailer last, in that order (§6.2,
`[R-LIF-02]` steps 3 and 5). The file size of a conforming file
equals the live trailer's committed file length F, and F is a multiple
of 64 (§6.2). `[R-CNT-01]`

No conforming file is shorter than 128 bytes: the front signature
block, a directory of at least 4 bytes at an offset of at least 16,
and the 64-byte trailer at a 64-aligned offset cannot be satisfied in
fewer. A reader MUST treat a shorter file as a validity error at file
scope. `[R-CNT-27]`

> **Example.** The smallest conforming file is exactly 128 bytes:
> front block [0, 16); an empty directory — zero records, so 4 bytes
> holding the CRC-32C of zero bytes, `0x00000000` — at [16, 20);
> 44 bytes of slack, zeroed by advice; trailer at [64, 128). It
> contains no
> layers (a valid, empty file).

> **Example — a file after three commits.** Regions, not offsets;
> ▓ marks slack.
>
> ```
> ┌───────┬───────────┬───────┬───────────┬───────┬──────┬────┬────────┐
> │ front │  layer A  │▓▓▓▓▓▓▓│  layer B  │▓▓▓▓▓▓▓│ dir₃ │pad │ trail₃ │
> └───────┴───────────┴───────┴───────────┴───────┴──────┴────┴────────┘
>         └tiles+index┘       └tiles+index┘       └──── re-emitted ────┘
> ```
>
> The live committed state is `front`, both layers' structures, dir₃
> and trail₃ (§5.2); the pad and the ▓ runs are slack.
>
> The grouping under the box is illustrative: a layer's structures
> need not be contiguous or ordered (`[R-SLB-05]`), and §20.5's
> figure shows the general case.
>
> The ▓ runs are the directories, pads and trailers of commits 1 and 2,
> superseded when commit 3 wrote its own. Layer A's tiles and index have
> never moved: a layer the commit does not touch keeps its extent slot
> pointing where it always pointed (§20.3, `[R-WRT-05]`), so a commit
> that touches no layer and appends no record extent — a user-metadata
> document lives in one, `[R-CNT-25]` — re-emits the directory, the
> pad and the trailer alone. A commit that changes a layer's stored-tile set or index
> content re-emits that layer's whole tile-index region as well, at a
> new placement (§20.3, `[R-WRT-04]`). The commit that added layer B
> emitted B's index region for the first time; a later commit changing
> B's stored-tile set would re-emit it at a new placement. A commit never relocates a live index region
> otherwise; that is a rewrite's operation (§20.5, `[R-WRT-07]`).
>
> This is what tail-anchored discovery buys. Because the structures that
> must change on every commit are the last ones in the file, a commit
> appends and never rewrites a committed byte (§9.1) — the property
> §9.6's recovery and §9.3's caching both rest on.

#### 5.2 Byte coverage

Coverage is a property of the **live committed state** — the front
signature block, and every structure reachable from the live trailer
through the live directory's records, extent slots, and tile-index
entries, together with the live directory and the live trailer. Every
byte of the live committed state belongs to exactly one of: the front signature block; or a **structure** — a
stored-tile extent, a record extent (the bytes any record's extent
slot references, whatever the record's type, §7.2), the directory, or
the trailer. No two of them overlap, and a file whose live state does
not partition this way is not a conforming file. `[R-CNT-02]`

Every byte the live state does not claim is **slack**: alignment and
slab gaps, the pre-trailer pad, and everything an earlier commit
superseded. Slack has no internal structure this specification
defines, its content is unconstrained, and no conformance requirement
applies to it. A reader MUST NOT interpret it (§9.5); a verifier that
reaches a live state MUST report the total number of slack bytes,
since that number is what tells an operator to compact. Where §6.2's
ordered validation rejects the file before a live trailer is
established there is no F and no live state to walk, so the total is
not owed at all: the verifier reports the trailer failure and
nothing about slack, which is not a partial total but the absence of
one. Where the walk of §9.7 does not
enumerate every region's claimants, the verifier MUST report the
total as partial. The walk is incomplete where a scope-level
rejection ends that scope's enumeration, where the verifier declined
a layer on resource grounds (`[R-ERR-04]`) and so never enumerated
its claimants, or where the verifier elected under `[R-CNF-11]` to
stop at the first violation; a tile's or a document's decode
declined leaves the walk complete, that claimant being enumerated
from its index entry or extent slot. An entry `[R-IDX-03]`
classifies reject-tile on a structural ground leaves it complete
too, and for the opposite reason: it contributes no claimant, the
walk passes over it, and the bytes of the file it nominally addresses
fall to slack where no other claimant claims them (§15.3, §9.7). A
rejected
layer's claimants
are not enumerated, whether or not the rejection impeded reading
them, and where the rejection is one the walk itself established,
L18's overlap or L40 through L42's placement among them, the
claimants it had already enumerated are discarded with the layer,
since the total is a claim about a live state one of whose layers is
not usable. A partial total is F less the bytes claimed by the
claimants the walk did enumerate — an upper bound on the file's true
slack, never an under-count — and a verifier reporting one MUST say
which scope or violation stopped the walk. It is not the file's slack
total but a bound on it, tightening to the exact total when the walk
completes. Only a rewrite (§20.5) reclaims it, compaction being the
rewrite an operator runs for that alone.
`[R-CNT-21]` Slack that holds superseded data is a privacy
consideration (§23).

Writers SHOULD zero the gaps they create — the run before an aligned
tile or slab run, and the pre-trailer pad. A writer that does not
leaves bytes indistinguishable from stale data and forfeits byte
reproducibility (Appendix G); no conformance requirement rides on
slack content either way. `[R-CNT-03]`

> **Rationale.** Slack is the byproduct of committing without
> rewriting and of aligning without packing — not a record anyone
> keeps: this format is not a version store, and an operator paying
> for storage compacts rather than retains. Certifying its content
> would mean deciding which slack bytes *this* commit wrote, which is
> not decidable from the live state — the only thing a reader ever
> walks. So this specification certifies the live state exactly, and
> counts the rest.

> **Note.** Of this rule's two halves, only disjointness is testable.
> The live committed state is *defined* as the front block plus what
> a complete coverage walk reaches, and `[R-LIF-08]` makes every byte
> that walk misses slack — so "belongs to no class" describes nothing,
> and a register row for it would be a row no file could exhibit. A
> partial total (`[R-CNT-21]`) reports what one verifier's incomplete
> walk left unclaimed, which is a fact about that run and not about
> the file's live state. What remains, and what a verifier actually
> checks, is that no two claimants overlap.

> **Note.** Coverage is checked by verifiers, never by readers: a
> reader's obligations never require walking anything but the live
> state. Conforming writers produce partitioned live states by
> construction — the commit protocol (§9.2) appends nothing it does
> not declare.

### 6. Front Signature Block and Trailer

#### 6.1 Front signature block

Bytes [0, 16) of every file, constant in every format major version:

| Offset | Size | Value | Class |
|---|---|---|---|
| 0 | 8 | `89 54 41 52 4E 0D 0A 1A` (`\x89`, "TARN", CR, LF, ctrl-Z) | structural |
| 8 | 8 | zero | structural |

Writers MUST emit exactly these 16 bytes.

A **local reader** is one whose transport serves any byte range at no
per-range round trip — a local file or a memory mapping being the
ordinary cases — and a **remote reader** one whose transport charges a
round trip per range (§6.4). That distinction governs the request
accounting of §6.4, `[R-CNT-10]`'s obligations over the transport size
and what the file size denotes in §6.2's gate (`[R-CNT-06]`); the
obligation over the front
block turns on residency instead, because a transport can be classified
either way at the margin while residency is decidable at any reader's
own open path.

A reader whose open leaves bytes
[0, 16) **resident** — a local file read whole, a memory mapping, a
speculative suffix window that reached offset 0, or any transport
already holding them — MUST verify the full block by byte
equality before other processing, and MUST treat any mismatch as
reject-file. A reader that would have to issue a further range request
to obtain those bytes MAY defer or omit the check: its open path is
anchored at the trailer (§6.2), and the two-request accounting of §6.4
does not include the front block. The test is residency, not transport,
so an implementation decides it at its own open path without having to
classify the network underneath it. `[R-CNT-04]`

> **Rationale.** The signature is engineered against transport
> corruption: the high-bit byte catches 7-bit stripping, CR LF catches
> line-ending translation, ctrl-Z stops accidental console display.

> **Note.** The intended media type for a TARN file is
> `application/vnd.tarn`, registration pending; the customary
> extension is `.tarn`. Content
> sniffers match the 16-byte front block by equality — no other
> prefix of a conforming file is constant.

#### 6.2 Trailer

The trailer occupies the final 64 bytes of the file, beginning at a
64-aligned offset (equivalently: F mod 64 = 0). Its layout:

| Offset | Size | Type | Field | Class | Valid values |
|---|---|---|---|---|---|
| 0 | 8 | bytes | trailer magic | structural | `8A 4E 52 41 54 0D 0A 1A` (`\x8A`, "NRAT", CR, LF, ctrl-Z) |
| 8 | 2 | u16 | version_major | structural | 1 (0 invalid; others: §6.3) |
| 10 | 2 | u16 | version_minor | descriptive | any (see §6.3) |
| 12 | 4 | u32 | flags | structural | bits 0–15 (incompat lane) all zero, a set bit being reject-file (F19); bits 16–31 (ignore lane) 0 from a creator, carried forward unchanged by every updater (appender and rewriter alike), a set bit ignored (§6.3) |
| 16 | 8 | u64 | dir_offset | structural | ≥ 16 |
| 24 | 8 | u64 | dir_length | structural | ≥ 4; dir_offset + dir_length ≤ F − 64 |
| 32 | 8 | u64 | committed_file_length | structural | = F; multiple of 64 |
| 40 | 8 | u64 | file_id | structural | ≠ 0 |
| 48 | 12 | bytes | reserved | structural | zero |
| 60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes [0, 60) |

Writers MUST place the directory so that no structure lies between
its end and the trailer. Those bytes — the **pre-trailer pad** — are
slack (§5.2): a writer that ends its directory on a 64-byte boundary
leaves none, this specification does not constrain their content, and
bounds their number only through step 5 of the commit protocol, which
pads to the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is
conforming, and no conforming commit produces one. A verifier MUST treat a structure in that gap as a
validity error at file scope, and counts the rest as slack; writers
zero it by the advice of `[R-CNT-03]` (readers check neither, their
check being the dir-bounds rule of `[R-CNT-06]`). `[R-CNT-05]`

> **Note.** The trailer magic's first byte differs from the front
> signature's, so a recovery scan (§9.6) never matches the front
> block.

A reader MUST validate, in order: the trailer magic; the trailer CRC;
the version gate (§6.3) — only these touch fields whose positions are
fixed across all majors (`[R-CNT-24]`) — and then, those gates passed,
MUST validate all of the following before acting on the fields
involved: the flag gates (§6.3); committed_file_length equals the
file size (for a remote reader, the size reported by its transport)
and is a multiple of 64; dir_offset ≥ 16; dir_length ≥ 4; dir_offset
+ dir_length ≤ F − 64, that sum being a declaration-derived quantity
under `[R-ENC-04]`; file_id ≠ 0; reserved bytes zero. Any failure is
reject-file. The owning scope of the front signature block and the
trailer is the file. `[R-CNT-06]`

> **Note.** A payload byte-string that mimics a trailer and happens to
> sit at exact physical end of file can pass every check above; it is
> caught at the directory CRC (§7.1) — detection is never silent, per
> §9.2's barrier note.

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
ignore lane (bits 16–31). In this specification's text no flag bits
are defined: a writer creating a file under this text MUST write
flags = 0, but a set ignore-lane bit is not a file-conformance
violation — such bits are defined by later minor versions, and files
carrying them are conforming files this text's readers ignore. A
rewriter, though its output is a new file, carries the input's
unknown ignore-lane bits into its output trailer rather than writing
flags = 0, and sets no other (§20.5, `[R-WRT-06]`). An updater MUST
copy forward unknown ignore-lane bits of its input file, MUST
NOT clear them, and MUST NOT set any other: no writer under this text
originates an ignore-lane bit, this text defining none for it to mean
anything by, so a bit is set only by a writer under the later minor
version that defines it and carried forward by every updater under
this text, appender and rewriter alike. An updater encountering an unknown
incompat-lane bit is a reader first, and therefore rejects the file
before modifying anything. `[R-CNT-08]`

A writer SHOULD emit the lowest version_minor that defines every
feature present in the file — for a file expressible under this text,
0 — and an appender the maximum of that floor and the prior trailer's
minor; a higher minor than needed costs readers nothing (minors never
gate) but misstates the file's feature floor to tooling. `[R-CNT-26]`

#### 6.4 Remote open accounting

The baseline remote open is two requests, each with an exact target:
(1) fetch the final 64 bytes — a suffix range, whose response also
carries the transport-authoritative file size F where the transport
discloses a range response's complete length (`[R-CNT-10]`, which
governs where it does not: a reader that probes separately spends a
third request, and one that cannot fails the open), so that §19.1's first two steps cost one
request between them; validate per
§6.2–§6.3; (2) fetch
[dir_offset, dir_offset + dir_length); verify and decode per §7.1. A
reader MAY instead speculatively fetch a suffix window in one request
and use containment: if the fetched buffer contains the directory
region, request 2 is unnecessary. Writers SHOULD keep dir_length plus
the pre-trailer pad plus 64 within 65,536 bytes so that a 64 KiB
suffix fetch captures trailer and directory together; a larger
directory is conforming and merely costs the second request.
`[R-CNT-09]`

> **Note.** This accounting is a theory of operation, not a budget: no
> request count is a conformance property, and nothing here bounds what
> a reader fetches. A reader speculating a megabyte and one fetching two
> exact ranges are equally conforming, and which is better is a property
> of the transport rather than of the file — high-latency links reward
> fewer, larger requests and metered ones reward the opposite. What the
> open does bind is its *working set*: the trailer and the directory,
> and nothing else, at any file size and layer count (`[R-RDR-01]`).
> That is the invariant this section exists to make legible, and the
> request counts are what it costs a reader that fetches exactly what it
> needs.

A remote reader MUST handle a 200 response to a range request (HTTP's
terms, RFC 9110, where the transport is HTTP; abort or accept the full
body deliberately — never treat the body prefix as the requested
range) and SHOULD fall back to a size probe plus an
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
bytes are a CRC-32C over the preceding dir_length − 4 bytes; those
covered bytes are the record sequence itself — the directory is always
raw, with no codec involvement on the open path. A reader MUST verify
that CRC before any other use of the region (mismatch: reject-file),
then parse records. `[R-CNT-11]` The owning scope of the directory is
the file.

Metadata compression exists only at record granularity. Each
user-metadata record carries its document in its extent — never
inline — and declares the document's encoding in its own inline
payload (u8: 0 invalid, 1 = none, 2 = zstd; §18). An extent of (0, 0)
on a user-metadata record, or one whose extent_length is less than 5
— too short to hold both a document and the terminal CRC-32C §8.1
places in its final 4 bytes — is a validity error at its containing
scope.
An encoding value of 0, or one the reader does not implement, makes
that record unreadable, with the same outcome as a failed CRC —
ignore-record, SHOULD be reported. User metadata is quarantined:
each way a user-metadata record's document can be unreadable once its
framing has been read — a failed extent CRC, an unimplemented or
invalid encoding, a decode failure, or content violating the
document's own rules (ill-formed UTF-8 included, `[R-ENC-11]`) — is
ignore-record with a SHOULD-report, notwithstanding the owning-scope
mapping of `[R-CNF-08]`. Application metadata never obliges a reader
to treat the structural data it annotates as unusable: where a rule
outside this quarantine records a document's defect at the file or
the layer (`[R-MTA-05]`, F27, L48), the verifier records it there and
a reader owes nothing for it, `[R-CNF-12]`'s licence on the
nonconforming file aside (§21.6). A reader that declines a document
on resource grounds MAY decline a scope containing it, which is
`[R-MTA-09]`'s and `[R-ERR-04]`'s subject and not this rule's. The
directory and the tile-index
region are always raw (the index so that it can be range-fetched,
§15); tile payloads use the layer's codec field (§17). `[R-CNT-25]`

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

The sequence MUST parse as zero or more complete records with no
residue. A record whose header or inline payload would extend past
the end of its containing record sequence is a validity error at the
sequence's owning scope: reject-file for the directory's top-level sequence,
reject-layer for a layer record's sub-record sequence (§7.4). Type 0
is not an unknown type: a reader MUST treat a record of type 0 as a
validity error at the same scope. Reserved flag bits: writers MUST
emit zero; readers MUST ignore them. Writers MUST NOT emit the
combination MU = 1 with PE = 0; a reader or updater encountering it
MUST treat the record as PE = 1 (never silently deletable). Both
writer violations make the file nonconforming (`[R-CNF-05]`) while
leaving conforming behavior unchanged, so their detection is a
verifier's: a verifier MUST treat a nonzero reserved flag bit or
the MU = 1 with PE = 0 combination as a validity error at the
record's governing scope. `[R-CNT-12]`

> **Note.** The two flag bits are not orthogonal. `[R-CNT-12]` leaves a
> record three states, not four, and they are §20.4's three rows:
> MU = 1, whose PE bit is read as 1 whatever is stored; MU = 0 with
> PE = 1; and MU = 0 with PE = 0. PE is a choice within MU = 0. An
> updater that does not implement an MU = 1 record's type never drops
> the record, alone or with the scope it governs (§20.4).

The **extent slot** (extent_offset, extent_length): (0, 0) means no
extent. Any other combination with either half zero, an
extent_offset < 16, an extent extending past F − 64, or an
overflowing sum — extent_offset + extent_length is a
declaration-derived quantity under `[R-ENC-04]` — is a validity error
at the scope the record governs
(§7.3): the layer for a layer record and for sub-records, the file for
other top-level records — a malformed slot on a layer record is
therefore reject-layer, consistent with `[R-CNT-17]`. For a record
with MU = 0, the extent slot is its only sanctioned reference to bytes
outside the record sequence: neither its inline payload nor its extent
contents encode offsets or lengths of other file bytes — this is what
lets a rewriter relocate an unknown ancillary's extent without
parsing it (§20). The layer record is the one exception, and this
specification's own: its tile index (§15), whose entries reference
stored-tile extents, is defined here, and every conforming reader and
updater implements the type (`[R-CNF-03]`, `[R-CNF-11]`), so none meets it as an
unknown ancillary. Records with MU = 1 carry further references only
where this specification or registry review (§10) defines them.
Extents are owned exactly once: within the
live committed state — all structures reachable from the live trailer,
whichever generation's commit appended them — no two extent slots and
no two structures overlap; a verifier MUST treat an intra-layer
overlap — including a stored extent overlapping its own layer's index
region or sub-record extents — as reject-layer, any overlap
across layers or touching another scope's structures as reject-file,
and any overlap between two structures neither of which belongs to a
layer as reject-file
(readers are not
obligated to detect overlap, which requires whole-directory
knowledge). `[R-CNT-13]`

Record semantics MUST NOT depend on record order: readers MUST NOT
infer meaning from the position of a record within the sequence, and
multiplicity rules are per type — in format major 1: any number of
layer records (zero is valid: a directory carrying no layer record
is a conforming generation, an empty directory included); at most
one file-scope user-metadata record, a second
being a validity error at the directory's scope (reject-file); and at
most one user-metadata sub-record per layer record, a second being a
validity error at layer scope. `[R-CNT-14]`

An unknown record type at file scope: MU = 1 → reject-file; MU = 0 →
ignore-record. This governs a reader's treatment, not the file's
validity: a record type from the experimental range is conforming
(§10.3's prohibition binds the writer's conduct, not the bytes,
`[R-CNF-02]`), while one from the reserved range is a value this
specification has not assigned — emitting it is a violation, and a
verifier MUST treat a reserved-range record type as a validity error
at the record's governing scope. Readers of both apply the MU rule
above unchanged. Updater obligations for unknown records are §20's
subject. `[R-CNT-15]`

#### 7.3 Record types of format major 1

| Type | Name | Scope | Flags (fixed by registry) |
|---|---|---|---|
| 0x0001 | layer | file (container for layer scope) | MU = 0, PE = 0 |
| 0x0002 | user metadata | file when top-level; layer as sub-record | MU = 0, PE = 1 |

All other type values are unassigned (registry and experimental
ranges: §10).

For the record types this specification registers, writers MUST emit
exactly the flag values fixed in the table above. A reader MUST apply
a known type's specified semantics regardless of its stored MU and PE
bits — a flipped stored bit never changes conforming behavior — and a
verifier MUST treat the mismatch as a validity error at the record's
governing scope; unreported, a writer defect propagates silently to
consumers that do not know the type. Stored
flag bits are authoritative only for record types the consuming tool
does not implement (`[R-CNT-15]`). A stored-flag mismatch on a
registered type makes the file nonconforming (`[R-CNF-05]`);
conforming readers nevertheless process the record under the fixed
semantics, exactly as they do for `[R-CNT-12]`'s reserved-flag and
MU = 1 / PE = 0 violations, whose detection this specification
likewise assigns to the verifier. `[R-CNT-22]`

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
| filter | u16 | 1 = none, 2 = byte-shuffle (0 invalid; others per §17) |
| alignment A | u64 | 0 = none declared; else a power of two, 512 ≤ A ≤ 2⁶² (§16.1) |
| slab S | u64 | 0 = no slab declaration; else run length in tiles, 1 ≤ S ≤ 2⁶³ − 1 (§16.2) |
| slab alignment A_slab | u64 | 0 when S = 0 (`[R-CNT-23]`); else a power of two, 1 ≤ A_slab ≤ 2⁶² (§16.2) |
| rank d | u8 | ≥ 1 |
| channel count C | u16 | ≥ 1 |
| d dimension entries | name (u8 len + bytes) · extent u64 · tile extent u64 | §11.1 |
| C channel entries | name (u8 len + bytes) · type u16 (0 invalid) · fill (u8 len + bytes) | type per §12; fill length equals the type's element size (`[R-CNT-23]`), so fill parses without type knowledge and validates with it |
| index_encoding | u8 | 1 = raw-segmented; any other value — including 0, reserved 2–0x7F, and the experimental range ≥ 0x80 (§10) — is a validity error at layer scope (§15) |
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
0), that expression being a declaration-derived quantity under
`[R-ENC-04]`; a mismatch, or an entry_count that does not equal the
geometry-derived addressed-tile count, is a validity error at layer
scope. `[R-CNT-17]`

The inline payload MUST parse exactly: fields are packed in table
order with no alignment or padding between them; the fixed fields,
the d dimension entries, the C channel entries, and the trailing
fixed fields MUST lie entirely within the inline payload, and the
remaining bytes MUST parse as zero or more complete sub-records under
§7.2's framing with no residue; any overrun, truncation, or residue
is a validity error at layer scope. Sub-records are layer-scope records; a
sub-record MUST NOT itself contain records (nesting depth beyond two
is a validity error at layer scope), and an unknown sub-record type
with MU = 1 is reject-layer, and where the file is otherwise
conforming a reader MUST NOT reject the file for it — on a
nonconforming file `[R-CNF-12]`'s licence to reject on any detected
violation is untouched; with MU = 0 it is ignore-record. A *known* type appearing where §7.3's table does not
scope it — a layer record nested as a sub-record, say — is a
validity error at layer scope, not an unknown type. `[R-CNT-18]`

> **Example — a complete layer record payload.** A rank-1 layer named
> `sst`: dimension `x` with extent 100 and tile extent 32; one
> interleaved float32 channel — §12.3's `temp` entry, byte for byte;
> codec 1 (none), filter 1 (none), no alignment or slab declaration;
> no sub-records. The grid count is ⌈100 / 32⌉ = 4 (§11.2), so
> entry_count = 4. With no tile stored, every index entry is the
> sentinel (§15.2), and the index region is the 80-byte entry array
> followed by its one segment CRC (§15.1): `0x80A34955` over those 80
> bytes, stored `55 49 A3 80`. crc_of_crc_array is the CRC-32C of
> that 4-byte array: `0xC4EE982E`. The inline payload is 81 bytes:
>
> ```
>  0  03 73 73 74                name: length 3, `sst`
>  4  01                         layout 1 = interleaved
>  5  01 00                      linearization 1 = row-major
>  7  01 00                      codec 1 = none
>  9  01 00                      filter 1 = none
> 11  00 ×8                      alignment A = 0: none declared
> 19  00 ×8                      slab S = 0: none declared
> 27  00 ×8                      slab alignment 0, forced by S = 0
> 35  01                         rank d = 1
> 36  01 00                      channel count C = 1
> 38  01 78                      dimension name: length 1, `x`
> 40  64 00 00 00 00 00 00 00    extent 100
> 48  20 00 00 00 00 00 00 00    tile extent 32
> 56  04 74 65 6D 70 0C 00       channel `temp`, type 12 = float32
> 63  04 00 00 C0 7F             fill: length 4, quiet NaN 0x7FC00000
> 68  01                         index_encoding 1 = raw-segmented
> 69  04 00 00 00 00 00 00 00    entry_count = 4
> 77  2E 98 EE C4                crc_of_crc_array = 0xC4EE982E
> ```
>
> Name and the nine scalars from layout through channel count occupy
> 4 + 34 bytes, the dimension entry 18, the channel entry 12, and the
> trailing fixed fields 13 — 81 exactly, with no residue, so the
> sub-record sequence is empty. The record framing this payload
> (§7.2) carries type 0x0001, the registry-fixed flags MU = 0,
> PE = 0 (§7.3), inline_length = 81, and — `[R-CNT-17]`'s
> arithmetic — an extent slot of length 4 × 20 + ⌈4 / 2¹⁶⌉ × 4 = 84
> addressing the index region wherever the writer placed it.

> **Note.** The nesting prohibition binds writers and any type a later
> version registers; in format major 1 it has no reader-detectable
> witness, and so no register row. Detecting nesting means parsing a
> sub-record's payload as records, which a reader does only where this
> specification defines that payload as a record sequence — true of the
> layer record alone, whose appearance as a sub-record §21.3 registers
> in its own right. A user-metadata payload is one byte
> (`[R-MTA-03]`), and an unknown type's payload is opaque by
> `[R-CNT-15]`.

### 8. Integrity

#### 8.1 Coverage map

Every field of every structure is covered by exactly one checksum —
excepting the equality-checked front signature block and this map's
terminal checksum fields, per §4.5, and the extent of a record of a
type this specification has not assigned, in which this specification
defines no fields (§4.7) and whose bytes it leaves opaque (§7.2) — as
this map states. All checksums are CRC-32C over bytes exactly as
stored. `[R-CNT-19]`

| Structure | Checksum location | Covers |
|---|---|---|
| Front signature block | none — checked by byte equality (§6.1) | — |
| Trailer | trailer bytes [60, 64) | trailer bytes [0, 60) |
| Directory region | final 4 bytes of the region | the preceding dir_length − 4 bytes (the raw record sequence) |
| Tile-index region | the per-segment CRC array, itself covered by the layer record's crc_of_crc_array | index entries, per segment (§15) |
| Stored tile | the crc field of its index entry | the tile's stored bytes |
| User-metadata extent | final 4 bytes of the extent | the preceding bytes (the encoded bytes exactly as stored, before decoding) |
| Extent of a record of a type this specification has not assigned | none — the bytes are opaque (§7.2) | — |

#### 8.2 Verification obligations and outcomes

The chain of trust is strictly ordered: trailer → directory → (per
layer) crc_of_crc_array → segment CRC array → index segment → index
entry → stored tile. A reader MUST verify each link before acting on
any field the link covers (`[R-ENC-05]`, `[R-ENC-10]`); failed
verification takes these outcomes: trailer or directory →
reject-file; any of a layer's index cross-checks (`[R-CNT-17]`), CRC
array, or segments → reject-layer; a stored tile's CRC → reject-tile;
a user-metadata extent's CRC → ignore-record, and readers SHOULD
report the loss (silent metadata loss defeats the record's purpose).
`[R-CNT-20]`

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
under a new file_id (a rewrite, §20.5). `[R-LIF-01]` The owning scope
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
(5) append the pad to the next 64-byte boundary — zeroed by advice,
`[R-CNT-03]` — and the new trailer, with committed_file_length equal
to the new end; (6) make the trailer durable. A commit's
committed_file_length is strictly greater than the prior trailer's,
by at least 128, so the committed file length orders a file's
generations (§9.3). `[R-LIF-02]`

Steps 4 and 6 bind a writer's **conduct** rather than its output, and
are declared so here on the model `[R-CNF-02]` states: a barrier
orders writes against power loss and leaves no trace in the bytes, so
a file committed without one can be byte-identical to a file
committed with it. A writer that omits a barrier violates this
requirement as an actor, and the file it produces is never
nonconforming by virtue of it, as `[R-CNF-02]` says of every conduct
rule.

On creation there is no prior trailer: the writer first emits the
front signature block (§6.1) — whose durability the barriers of steps
4 and 6 cover — then performs steps 2–6, writing
beginning at offset 16. There being no prior committed file length,
the strict increase above binds from the second commit onward.

> **Note.** Step 3 is not discharged by a directory an earlier
> generation appended: each commit appends its own complete
> directory, and the trailer of step 5 addresses that one. A writer
> that re-points a new trailer at a prior generation's directory
> region has left step 3 unperformed.

> **Note.** Step 5's strict increase is forced by the steps before
> it, not an extra obligation on the writer. Step 1 begins writing at
> exactly the prior F, and `[R-LIF-01]` holds every byte below it
> immutable, so this commit's directory lies at dir_offset ≥ the
> prior F; the Note above forbids reusing an earlier generation's, so
> there is such a directory; and `[R-CNT-06]` requires dir_length ≥ 4
> and dir_offset + dir_length ≤ the new F − 64. The new F is
> therefore at least the prior F plus 68, and since `[R-CNT-06]`
> makes every committed file length a multiple of 64, at least the
> prior F plus 128. It is `[R-CNT-27]`'s 128-byte floor argument run
> from F rather than from offset 0.

> **Note.** Where barriers are weaker than assumed, safety degrades
> from "torn commits are invisible" to "torn commits are detected":
> §8's chain still catches every inconsistent state loudly — the
> outcome is rejection at the affected scope, never silent corruption.

> **Example — what a crash sees.** ▓ marks bytes outside the live
> committed state: in row 2 the partial write of an interrupted
> commit, in row 3 the structures commit n + 1 superseded.
>
> ```
> committed    │ … │ dirₙ │pad│ trailₙ │
>                                       ↑ F: a reader opens here
>
> mid-commit   │ … │ dirₙ │pad│ trailₙ │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
>                                       ↑ trailₙ intact, but no longer
>                                         at the file's end
>
> committed    │ … │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ … │dirₙ₊₁│pad│ trailₙ₊₁ │
> ```
>
> Mid-commit the physical tail is not a trailer, so a reader on the
> default path reports the file torn and MUST NOT scan backward
> (`[R-LIF-05]`). What makes that recoverable rather than fatal is that
> trailₙ and everything it reaches are still byte-intact: §9.6's
> deliberate scan finds trailₙ and truncating to it restores the file
> exactly. The window is not one in which the old state is *readable* —
> it is one in which the old state is *recoverable*, which is the whole
> return on never modifying a committed byte.

#### 9.3 Generations, file_id, caching

Each commit's trailer carries the committed file length F of the
generation it commits and the file_id chosen at creation (nonzero;
the creating writer SHOULD draw it from a cryptographically random
source — a predictable or reused file_id lets two distinct files
collide in the (file_id, range)-keyed caches this rule licenses,
serving bytes from the wrong file). Within one file_id, F strictly
increases per commit — by at least 128 (`[R-LIF-02]`) — so it orders
that file's generations and identifies each of them. Because
committed bytes are immutable, any byte range fetched under the
generation whose committed file length is F remains byte-correct
under every later generation of the same file_id: caches keyed
(file_id, range) never invalidate, and revalidation is one 64-byte
trailer read — same F, everything cached remains valid; higher F,
refetch the directory; different file_id or lower F, treat as a
different file. `[R-LIF-03]`

> **Note.** The strict increase is what makes that revalidation
> sound, and §9.2's second Note is what makes it checkable: no two
> commits of one file share a committed file length, so where no
> other file has drawn the same file_id, a matching (file_id, F) pair
> names the same committed prefix a cache already holds. Where one
> has, the collision this requirement's randomness advice exists to
> prevent is what the cache serves, and no comparison of F detects
> it. A lower F under a known file_id is not a stale read to retry —
> it is a file that has lost committed bytes, which `[R-LIF-01]`
> forbids — so it is treated as a different file.

> **Note.** The ordering quantity is bounded above, and by two rules
> rather than one: F is a u64 offset under `[R-ENC-03]`, so
> F ≤ 2⁶³ − 1, and `[R-CNT-06]` requires it to be a multiple of 64.
> The reachable ceiling is therefore 2⁶³ − 64, the largest multiple
> of 64 that bound admits, and each commit adds at least 128 bytes,
> so a file there admits no further commit. A rewrite (§20.5) is
> the continuation from there: a fresh file_id whose first commit
> starts F over. The bound is a statement of closure, not an
> operational concern.

> **Note.** F counts bytes, not commits. It orders a file's
> generations and tells a cache which one it holds, but it does not
> number them: how many commits a file has undergone is not
> recoverable from the live trailer, and no field records it — a
> deployment needing that count keeps it out of band or in user
> metadata (§18). The contract above also assumes a conforming
> writer: a file truncated to an earlier commit and re-appended can
> present an already-seen F over different bytes, which is the
> rollback case §9.6 names as needing out-of-band state.

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

> **Note.** Residue past a completed commit carries no register row of
> its own. A reader meets it as a trailer that fails its gates — the
> magic, the CRC, or committed_file_length against the transport size,
> each of which §21.2 already registers — and `[R-LIF-05]` forbids it to
> scan backward, so it cannot tell residue from corruption and is not
> asked to. What the residue violates is `[R-LIF-04]`'s writer
> obligation to truncate or overwrite, and the state a reader can
> observe is already named.

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
to verify and committed_file_length = o + 64 — a match satisfying
both is a **candidate**, and one failing either is not. The
nearest-to-end candidate that survives the whole-file re-verification
below is the last committed state; truncating to it recovers the
file. A recovery tool enumerating a file's commit states continues
the same probe to offset 0; coverage verification does not (§9.7,
`[R-LIF-08]`), and no verdict turns on the probe: a file whose final
64 bytes are not a valid trailer fails `[R-CNT-06]`'s gates on the
bytes handed over (§21.2 rows F8, F14 and F17 — the magic, the
trailer CRC and the length cross-check), and the earlier state the
probe finds is a different artifact, reached only through the
whole-file re-verification below. For a verifier the probe is
diagnosis — which commit state is recoverable — not a finding about
the file it was given. Two cautions are normative for
tools: a tile payload can deliberately contain a byte string that
mimics a valid trailer, so recovery output MUST be re-verified as a
whole file (§8) before being trusted; and truncation of a file to an
earlier commit boundary is indistinguishable in-format from that
earlier version — rollback detection requires out-of-band state, and
no field of this format supplies it. An expected committed file
length is not a substitute: placement within a commit is free
(`[R-SLB-05]`) and slack is unconstrained (`[R-CNT-21]`), so a party
that truncates to an earlier commit and re-appends can bring the file
back to any committed file length at or above the expected one while
serving the rolled-back content. What still works is state the file
cannot manufacture: a detached hash over the committed prefix, or an
append-only transport that refuses a shortened object. A signed
committed file length is not among them — the value is exactly what
the re-append reproduces. The probe begins at the
largest 64-aligned offset o with o + 64 ≤ the physical file length; a
candidate whose whole-file re-verification fails was not a commit
state, so the tool continues the probe past it, and MUST report the
candidate it settled on and how many candidates it rejected on that
re-verification, or, where no candidate survived it, that none did
and how many it rejected. `[R-LIF-06]`

Writers performing very large single commits SHOULD emit intermediate
checkpoint commits (a directory and trailer mid-stream, ~a few KiB
each); the consequence of not doing so is that a torn multi-hour
append is recoverable only by scanning back across its entire length.
`[R-LIF-07]`

#### 9.7 Coverage verification

A verifier checking `[R-CNT-02]`'s partition walks the live state
only. From the live trailer it reads the live directory
and, through its records and their sub-records, reaches the claimants
`[R-CNT-02]` names: the directory itself, each record's extent, and
the stored extent of each non-sentinel tile-index entry (an entry
`[R-IDX-03]` classifies reject-tile on a *structural* ground
contributes no stored extent to the walk; one whose stored bytes
alone fail its crc keeps its extent). A record is not a claimant of
its own — its header and inline payload lie inside the directory
region, which is the claimant covering them — so reaching a record
through the directory is traversal, not a second claim on those
bytes. A layer
record's extent slot addresses that layer's tile-index region (§7.4),
so the region enters the walk once, as that record's extent, and is
not a second claimant beside it. It checks that these occupy disjoint
byte ranges, that
each lies within
[16, F − 64), and that each verifies against the checksum covering
it, where §8.1's map states one (§8.1). The front signature block at
[0, 16) and the live trailer at [F − 64, F) are claimed by the walk as
well, being members of the live committed state (`[R-CNT-02]`); the
[16, F − 64) bound above already
keeps every other claimant disjoint from them. Bytes the walk does not
reach are slack: the verifier sums them and reports the total, and
their content is not its concern. A verifier that certifies decodes
every stored tile, whatever content obligations §14 places on the
layer: §21.4's codec rows are file-conformance violations, and a
verifier MUST NOT certify past a violation it has not looked for;
one that declines a tile's decode on resource grounds reports that
check unmade and cannot certify (`[R-CNF-11]`, `[R-ERR-04]`). A user-metadata
document under an experimental-range encoding asks nothing of this
walk: no
rule attaches to its content (`[R-MTA-10]`), so there is no
violation there to look for, and what the verifier reports instead
is that rule's subject. Where the walk does not complete —
a scope-level rejection blocks enumeration, the verifier declines a
layer on resource grounds and so never enumerates its claimants
(`[R-ERR-04]`), or it stops at the first violation (`[R-CNF-11]`) —
the sum is reported as partial, and
`[R-CNT-21]` governs what such a total counts and what the verifier
reports beside it. An entry `[R-IDX-03]` classifies
reject-tile on a *structural* ground does not make the walk
incomplete: the walk passes over
it, and the bytes of the file it nominally addresses fall to slack
where no other claimant claims them (§15.3).
`[R-LIF-08]`

> **Note.** Nothing here enumerates prior commits. A verifier
> certifies what a reader can reach and counts what it cannot, which
> is decidable from the live trailer in one pass and does not depend
> on reconstructing the file's history — a history the format does
> not promise to keep and a rewrite is expected to discard.

### 10. Extension Points and Registry

#### 10.1 The extension surface

This format grows through exactly four vehicles (`[R-ENC-07]`), and
this section collects them:

1. **New record types** (§7.3), which carry their own scope and
   flags;
2. **New values in the ranges this specification reserves** (§10.2);
3. **New ignore-lane flag bits** in the trailer (§6.3);
4. **New standardized user-metadata keys** (§18.4).

Nothing else extends this format. A new fixed field, a widened
structure, a changed field width, or a reinterpreted assigned value
is a new format major version (`[R-CNT-24]`) — never a minor
revision, and never an implementation's private convention.
`[R-EXT-01]`

#### 10.2 Numeric identifier spaces

Every numeric identifier space is partitioned identically: values
this specification assigns; a **reserved** range only this
specification assigns from; and an **experimental** range for
private use. The spaces, defined in the sections that own them and
collected here:

| Space | Width | Assigned | Reserved | Experimental |
|---|---|---|---|---|
| record type (§7.3) | u16 | 0x0001, 0x0002 | 0x0003–0x7FFF | ≥ 0x8000 |
| channel layout (§14.1) | u8 | 1, 2 | 3–255 | none |
| linearization (§11.4) | u16 | 1 | 2–0x7FFF | ≥ 0x8000 |
| sample type (§12.2) | u16 | 1–13 | 14–0x7FFF | ≥ 0x8000 |
| codec (§17.2) | u16 | 1–4 | 5–0x7FFF | ≥ 0x8000 |
| filter (§17.3) | u16 | 1, 2 | 3–0x7FFF | ≥ 0x8000 |
| index encoding (§7.4) | u8 | 1 | 2–0x7F | ≥ 0x80 |
| metadata encoding (§18.2) | u8 | 1, 2 | 3–0x7F | ≥ 0x80 |

Value 0 is invalid in every space above. One space carries no
experimental range: channel layout, whose `u8` field is too narrow
to spare one, 3 through 255 staying reserved to this specification.
The trailer's flag lanes are not a space of this kind and are not
tabulated above; §6.3 partitions them instead.
`[R-EXT-02]`

#### 10.3 The experimental range

Experimental values are private use and carry **no collision
protection**: two unrelated experiments MAY select the same value,
and nothing in this format distinguishes them. Writers MUST NOT emit
files carrying an experimental value in released software or
published data, and a value from a reserved range MUST NOT be
emitted at all before this specification assigns it — an
unregistered value that escapes into circulation is precisely the
failure the experimental range exists to absorb. A reader
encountering either treats it as its space's rules require: a
validity error at the owning scope for the value sets of §7.4,
§11.4, §12.2, §14.1, §17.2, and §17.3; for record types, the MU-bit
outcome of `[R-CNT-15]` at file scope and `[R-CNT-18]` for layer
sub-records; and for the metadata-encoding space of §18.2,
ignore-record under the quarantine (`[R-CNT-25]`), never a
scope-level rejection. `[R-EXT-03]`

#### 10.4 Registration

A value leaves the reserved range by registration, which requires an
unambiguous specification of its semantics — sufficient for
independent implementation without consulting any implementation — a
security review of what accepting it obliges a reader to do, and, for
a record type, its MU and PE assignment with justification. A type
registers MU = 0 only if ignoring it leaves every stored sample
bit-exact and every geometry identical; sample types, geometry,
channel sets and layout, codecs, filters, linearization, fill, and
index location or encoding are never ignorable, so no record
carrying them registers as ancillary. `[R-EXT-04]`

The registry is `spec/registry.json` in this specification's
repository, versioned with the specification itself; Appendix C is
its snapshot at publication. Its `registry_version` field
increments on every change to an assignment. Where the registry,
§10.2's table, and Appendix C diverge, the section that defines the
space governs — the registry is machine-readable convenience, never
a second authority (§21.1 applies the same principle to the error
register). `[R-EXT-05]`

> **Note.** A registry hosted apart from the specification it serves
> can be decommissioned out from under it, which is how a
> well-designed private range becomes a collision field. Keeping the
> registry in the repository makes it as durable as the document.

---

## Part II — Array Model

### 11. Layers, Dimensions, and Tiling

#### 11.1 Geometry and its validity floor

The owning scope (§2.4) of a layer's geometry and linearization fields
is the layer.

A layer has rank d ≥ 1; each of its d dimensions has a name (§4.6), an
extent Eᵢ ≥ 0, and a tile extent Tᵢ ≥ 1; and the layer has at least one
channel. A tile extent MAY exceed its dimension's extent (where
0 < Eᵢ < Tᵢ the grid is then a single padded tile along that axis;
at Eᵢ = 0 the grid count is 0 and the layer addresses no tile, §11.2). Writers MUST NOT emit a
layer with rank 0, any tile extent 0, or channel count 0; a reader MUST
treat any of these as a validity error at layer scope. `[R-GEO-01]`

A dimension with extent 0 is valid: its grid count is 0, the layer has
zero addressed tiles, its tile index has zero entries, and its reference
array is empty. Readers MUST accept such a layer, and a read of any
region of it returns no samples. `[R-GEO-02]`

> **Rationale.** Empty layers serve schema-first workflows: declare
> layers at creation, grow extents as data arrives. §20.3 states
> normatively, and governs, what a commit may do to a layer that
> already stored tiles in the generation a commit supersedes: its
> extents may grow and not shrink; a planar layer's channel list may
> be extended or shortened at its end, one or the other in a commit;
> its names may change, and a
> slab or alignment declaration may be declared, changed or
> cleared; several of these in one commit, each subject to every rule
> the declarations it produces are under; and every other declaration
> is fixed while the layer stores a tile, a change to one being a new
> layer or a whole-file rewrite. A layer that stored no tile in the
> generation the commit supersedes may be re-declared freely, subject
> to every rule its new declarations are under; a layer the commit
> itself empties does not qualify. A growth that changes no grid count
> ⌈Eᵢ / Tᵢ⌉ (§11.2) moves no entry and adds none, and taken alone
> touches the directory alone; so does one that raises a grid count
> while another stays 0, the product holding at 0 and the index empty
> either way. Any other growth changes the index content — entry_count
> and extent_length with it (`[R-CNT-17]`), and disk ordinals renumber
> wherever `[R-GEO-06]` moves them — so the layer's whole tile-index
> region is re-emitted (§20.3, `[R-WRT-04]`), the growth that raises
> a zero-extent layer's **only remaining** zero grid count included.

#### 11.2 Grid arithmetic

For each dimension, the **grid count** Gᵢ is the ceiling division
⌈Eᵢ / Tᵢ⌉, equal to Eᵢ/Tᵢ plus 1 if Eᵢ mod Tᵢ ≠ 0 (integer division).
The layer's **spatial-tile count** is N = ∏ Gᵢ, and its
**sample-position count per tile** is P = ∏ Tᵢ. The layer's
**addressed-tile count** — the number of its tile-index entries (§15) —
is N for an interleaved layer and C · N for a planar layer, where C is
the channel count, and its **total sample-position count** is N · P.
These products are declaration-derived quantities under
`[R-ENC-04]`: a reader MUST treat one exceeding
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
Where Eᵢ mod Tᵢ ≠ 0 — equivalently, where the grid overhangs the
extent, stated in a form that forms no product (§4.2) — the tiles at
the high edge of dimension i contain **padding positions** — sample
positions whose coordinate along that axis would be ≥ Eᵢ. Padding
positions are serialized like any other
position (byte-level rules and padding content: §14) but are not part
of the reference array (§3.2); a reader MUST NOT return padding
positions as samples. `[R-GEO-04]`

> **Note.** Tile extents are a writer's choice, and this
> specification imposes none: the workable range in practice runs
> from roughly 1 to 16 MiB of decoded tile, large enough to amortize
> a range request and small enough that reading one sample does not
> drag in megabytes. Tiles far outside that range remain conforming.

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

A channel is declared by its layer record's channel entry (§7.4): a
name (§4.6), a sample type (`u16`, structural), and a fill value
(§13). The owning scope (§2.4) of a channel declaration is the layer
(`[R-CNT-23]`); channels are declared in order, and the declared
order fixes each channel's index (§3.1, §11.4).

#### 12.1 Core sample types

This specification defines exactly thirteen sample types, all
**core**: a conforming reader MUST decode every one of them, and
none is skippable (`[R-CNF-03]`). `[R-TYP-01]`

| ID | Name | Element size | Definition |
|---|---|---|---|
| 1 | bool | 1 | logical value: false or true; fill encoding §13.2, in-tile representation §14 |
| 2 | int8 | 1 | signed two's-complement integer |
| 3 | int16 | 2 | signed two's-complement integer |
| 4 | int32 | 4 | signed two's-complement integer |
| 5 | int64 | 8 | signed two's-complement integer |
| 6 | uint8 | 1 | unsigned integer |
| 7 | uint16 | 2 | unsigned integer |
| 8 | uint32 | 4 | unsigned integer |
| 9 | uint64 | 8 | unsigned integer |
| 10 | float16 | 2 | IEEE 754 binary16 |
| 11 | bfloat16 | 2 | defined below |
| 12 | float32 | 4 | IEEE 754 binary32 |
| 13 | float64 | 8 | IEEE 754 binary64 |

float16, float32, and float64 are the IEEE 754-2019 interchange
formats binary16, binary32, and binary64. The twelve types other
than bool are this specification's **numeric types**. A type's
**element size** is the byte length of one encoded value of that
type: it fixes the length of the channel's fill field
(`[R-CNT-23]`) and enters §14's byte-layout arithmetic, except that
a planar bool plane is sized by packing (§14.3). Multi-byte values
are little-endian (`[R-ENC-01]`). The in-tile representation of
bool samples is §14's subject; a bool's element size of 1 governs
its fill field (§13.2) and its interleaved byte (§14.2).

**bfloat16.** A bfloat16 value occupies two bytes. In the numbering
of §4.4, bit 15 is the sign, bits 14–7 the biased exponent, and bits
6–0 the trailing significand. A bfloat16 bit pattern b denotes
exactly the value that the IEEE 754 binary32 bit pattern b × 2¹⁶
(b in the high 16 bits, low 16 bits zero) denotes; subnormals,
infinities, and NaNs follow from that identification. `[R-TYP-02]`

> **Example.** bfloat16 1.0 is `0x3F80` — binary32 1.0 is
> `0x3F800000`, and keeping the high 16 bits leaves `0x3F80` —
> stored as the bytes `80 3F`. The bit pattern `0x7FC0` denotes a
> quiet NaN (binary32 `0x7FC00000`).

#### 12.2 The type field's value set

Field values: 0 is invalid; 1 through 13 are assigned per §12.1;
values 14 through 19 are reserved without semantics; values 20
through 0x7FFF are reserved for future assignment by this
specification; values ≥ 0x8000 are the experimental range (§10).
Writers MUST NOT emit a type value other than 1 through 13; a reader
MUST treat any other value — 0, every reserved value, and the
experimental range included — as a validity error at layer scope
(`[R-CNT-23]`). Type identifiers are pure enumerators: a reader MUST
NOT infer an element size or any semantics for a type value this
specification does not assign, whatever pattern its bits suggest
(`[R-CNF-04]`). `[R-TYP-03]`

> **Note.** The reserved identifiers are pinned: 14 and 15 for 8-bit
> floats — defined, if ever, as bit-exact OCP OFP8 E4M3 and E5M2, and
> no other 8-bit float definition will be considered — 16, 17, and
> 18 for int128, uint128, and float128, and 19 for a fixed-size
> raw-bytes type. Reservation forecloses collision; it is not a
> commitment to assign. Reserved types enter, if ever, through a
> minor version, which an unaware reader handles gracefully: the
> unknown type value makes exactly that layer unreadable
> (reject-layer), never the file.

#### 12.3 Values are bit patterns

A sample value is its bit pattern (§3.2, `[R-MDL-02]`). Writers and
readers MUST NOT alter a value's encoded bytes in storing, decoding,
or returning it: NaN payloads are preserved — never quieted,
canonicalized, or collapsed — and −0.0 and +0.0 are distinct values.
Wherever this specification treats two sample or fill values as the
same value, it means their encoded bytes are identical; this format
defines no numeric equality, no ordering, and no NaN-aware
comparison over sample values. In a conforming file this rule admits
no exception; the one case where a reader resolves a byte to a value
rather than passing it through arises only in a nonconforming file,
and `[R-SER-08]` states it. `[R-TYP-04]`

Every bit pattern of a numeric type's element size is a valid sample
value and a valid fill value — subnormals, infinities, and every NaN
payload included; there is no sample value a reader screens out.
Boolean values are constrained by §13.2 (fill) and §14 (in-tile
representation). `[R-TYP-05]`

> **Example.** A channel entry (§7.4) declaring name `temp`, type
> float32, fill the quiet NaN `0x7FC00000` is the twelve bytes
> `04 74 65 6D 70 0C 00 04 00 00 C0 7F`: name length 4, the name
> bytes, type `0C 00` (12, little-endian), fill length 4, fill bytes
> `00 00 C0 7F`. A fill of `0x7FC00001` — a NaN carrying a payload —
> is equally valid and round-trips bit-exactly (§13.1).

### 13. Fill Values and Sparse Tiles

Fill is what makes sparse layers first-class: an addressed tile that
is not stored (§3.1) occupies no payload bytes, and reading it is
defined behavior — each channel it carries reads as fill at every
sample position (§13.3) — rather than an error. The owning scope of
a fill field is the layer (`[R-CNT-23]`).

#### 13.1 The fill field

Every channel entry records a fill value: exactly the channel's
element size in bytes, holding the little-endian encoding of one
value of the channel's type (§7.4, `[R-CNT-23]`). The field is
always present — §7.4's framing leaves absence unrepresentable — and
it is authoritative: a reader MUST take a channel's fill from its
channel entry, MUST NOT substitute a type-derived default or any
other value, and MUST return fill bit-exactly as recorded
(`[R-TYP-04]`). `[R-TYP-06]`

The fill value is structural (§4.7): it fixes what unstored samples
read as, and a verifier's acceptance of a tile turns on it, since
`[R-SER-05]` fixes every padding position's content to it — though
it never affects how any byte is located or decoded; the field's
length prefix is §7.4's framing, cross-checked against the element
size (`[R-CNT-23]`).

Fill is mandatory-with-default: a writer whose caller does not
choose a fill SHOULD record all-zero bytes. A writer that defaults
differently still emits a conforming file, but its unwritten
regions read back as a value consumers of the conventional zero
default will not expect. `[R-TYP-10]`

> **Note.** Nothing distinguishes the recorded default from a
> deliberately chosen zero — deliberately so: readers never guess,
> and the "field absent, behavior undefined" class of divergence is
> unrepresentable.

#### 13.2 Per-type fill constraints

For the twelve numeric types, every bit pattern of the element size
is a valid fill (`[R-TYP-05]`), NaN payloads and −0.0 included. For
bool, the fill field is one byte and its value is constrained:
`0x00` (false) or `0x01` (true). Writers MUST NOT emit any other
byte; a reader MUST treat any other byte as a validity error at
layer scope. `[R-TYP-07]`

> **Rationale.** One value, one encoding. Admitting "any nonzero
> byte is true" would create 255 encodings of true, and channel
> entries with identical meaning but different bytes — the
> two-encodings trap §4.6 closes for names, closed here for fill.

#### 13.3 Unstored tiles read as fill

For every addressed tile that is not stored in the live generation —
its index entry is the sentinel (§15.2) — a reader that returns any
of the tile's sample positions inside the layer's extents MUST
return, for each channel the tile carries, that channel's fill value
at every such position. In an interleaved layer an unstored tile
yields the full fill sample — each channel's fill, in declared
channel order — at every position; in a planar layer exactly the
entry's channel reads as fill there, and a single sample can mix
decoded and fill channels (§3.2). `[R-TYP-08]`

> **Example.** An interleaved layer with channels `r`, `g`, `b`, all
> uint8, fills `0xFF`, `0x00`, `0x00`: every sample of an unstored
> tile reads as the tuple (255, 0, 0). With the same channels planar
> and, at one spatial ordinal, the tiles for `r` and `g` stored but
> the tile for `b` the sentinel, samples there read decoded `r`,
> decoded `g`, and `b` = 0.

Fill is produced by exactly one condition: a sentinel entry read
from a verified index chain (§8.2, §15.4). A reader MUST NOT return
fill for a tile whose entry is malformed (§15.3), whose index CRC
array or segment failed verification, or whose stored bytes failed
their checksum: those conditions reject their scopes, and a
rejection is never satisfied by returning fill (`[R-CNF-09]`).
`[R-TYP-09]`

> **Rationale.** This rule is what makes sparse semantics safe.
> Because every index byte is checksummed (§8.1), corruption cannot
> silently convert "stored" into "absent, reads as fill": a zeroed
> index region is loudly invalid rather than all-sparse (§15.2), and
> a damaged entry rejects the tile rather than filling it.

> **Note.** Fill governs unstored tiles. The padding positions of
> stored edge tiles (§11.3) are a different mechanism — their stored
> byte content is §14's subject — and a reader never returns padding
> positions in any case (`[R-GEO-04]`).

> **Note — sparse writing.** A writer creates a sparse layer by
> emitting sentinel entries: no payload bytes, and for a full
> segment of sentinels even the segment CRC is a known constant
> (`[R-IDX-05]`). Declare-then-fill workflows append tiles as data
> arrives, generation by generation (§9); each commit that changes a
> layer's stored-tile set or its index content re-emits that layer's
> whole tile-index region (§20.3, `[R-WRT-04]`), and a growth that
> changes no grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) moves no entry and adds
> none, as does one that raises a grid count while another stays 0
> (§11.1).

### 14. Tile Serialization

This section defines the **decoded tile image**: the byte sequence a
stored tile's payload decodes to under §17's codec pipeline, and the
byte sequence a writer presents to that pipeline. The owning scope
of a layer's serialization declarations is the layer; the owning
scope of one tile's decoded content is the tile (§2.4).

#### 14.1 The value sequence

Every tile serializes a **value sequence** — its decoded values in
one fixed order. With P the sample-position count per tile (§11.2),
C the channel count, and in-tile positions ordered by the permanent
row-major in-tile ordinal (§11.4):

- **Planar** — the tile with disk ordinal c · N + s (§11.4) carries
  exactly the values of channel c at the tile's P positions: value
  k of the sequence is channel c's value at in-tile ordinal k, and
  the sequence has V = P values.
- **Interleaved** — the tile at spatial ordinal s carries all C
  channels at the tile's P positions, sample-major: value k of the
  sequence is channel (k mod C)'s value at in-tile ordinal
  k div C — each sample's channel values are adjacent, in declared
  channel order — and the sequence has V = P · C values. `[R-SER-01]`

The layer's layout field (§7.4) selects the mode. Field values: 0 is
invalid; 1 = interleaved and 2 = planar are the only values this
specification defines and the only values a writer MAY emit; values
3 through 255 are reserved without semantics. A reader MUST treat
any value other than 1 or 2 as a validity error at layer scope
(`[R-CNT-23]`). `[R-SER-06]`

#### 14.2 Byte layout and decoded size

In a planar tile of a numeric channel (§12.1), and in every
interleaved tile, the decoded tile image is the value sequence with
each value encoded in sequence order with no padding between
values: a numeric value as its type's element size, little-endian
(`[R-ENC-01]`); a bool value — interleaved layers only, since §14.3
governs planar bool planes — as a single byte, 0x00 = false,
0x01 = true, with element size 1 in the arithmetic below. The
image's byte length — the **decoded size** — and each value's byte
offset follow:

| Layout | Decoded size | Offset of value k |
|---|---|---|
| planar, numeric channel c | P · Bᶜ | k · Bᶜ |
| interleaved | P · Q | (k div C) · Q + F_{k mod C} |

where Bᶜ is channel c's element size (§12.1; 1 for bool), Q = Σ Bᵢ
over all channels (the **sample stride**), and Fᶜ = Σ Bⱼ over
channels j < c (channel c's in-sample offset). These products and
sums are declaration-derived quantities under `[R-ENC-04]`, each for
the layout its row states — a planar layer has no P · Q to form.
`[R-SER-02]`

Writers MUST NOT emit any byte other than 0x00 or 0x01 as an
interleaved bool value. Any other byte makes the file
nonconforming: its assigned detector is the verifier, for which it
is a validity error at tile scope. A reader is not obligated to
screen decoded content, and a reader that does not detect the
violation is not thereby nonconforming; `[R-CNF-12]` governs a
reader that does detect it. A reader that does not reject the
tile and returns the value — whether or not it detected the
violation — MUST return 0x00 as false and every other byte as
true — the value, encoded 0x00 or 0x01 as above, and not the
stored byte. That rule fixes what
such a reader returns; it neither makes the byte conforming nor
relieves the verifier, and it never arises in a conforming file,
where the only bytes present are 0x00 and 0x01. `[R-SER-08]`

> **Rationale.** The writer-side constraint and the reader-side
> interpretation answer different questions, and the earlier text
> answered only the first. One encoding per value is what keeps
> §14.5's padding check, `[R-COD-10]`'s stride detection and
> Appendix G's byte reproducibility working, so the constraint
> stays. But leaving the return value undefined bought nothing: two
> readers handed the same malformed tile could disagree about a
> sample and both be conforming, which is the divergence this
> document exists to prevent. Defining the charitable path costs
> nothing, since a conforming file never exercises it.

> **Note.** The parallel constraint on a bool *fill* byte (§13.2)
> needs no such rule: `[R-TYP-07]` assigns its detection to the
> reader with a defined outcome — reject-layer — so a reader never
> reaches a fill byte it must interpret. Only the in-tile byte,
> whose detector is the verifier, could be met by a reader with no
> obligation to act on it.

> **Example.** An interleaved layer, tile extents (2, 3), P = 6,
> channels `a` (uint8) and `b` (uint16): Q = 3, decoded size 18.
> The position with in-tile coordinates (1, 2) has in-tile ordinal
> 1·3 + 2 = 5; its sample occupies bytes [15, 18) — `a` at byte 15,
> `b` at bytes 16–17, little-endian. The same layer planar: channel
> `b`'s tile is 12 bytes, and ordinal 5's value occupies bytes
> 10–11. With channels `t` (float32) and `m` (bool) interleaved
> instead: Q = 5, decoded size 30, and ordinal 5's sample is bytes
> [25, 30) — `t` at 25–28, `m` the single byte at 29. In general,
> channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ —
> the table's forms with k = u · C + c.

#### 14.3 Packed boolean planes

In a planar tile of a bool channel the decoded tile image is the
tile's P values bit-packed LSB-first: value k occupies bit k mod 8
of byte k div 8 (§4.4), with 0 = false and 1 = true, and the
decoded size is ⌈P/8⌉ bytes. Packing is exclusive to planar bool
planes — an interleaved bool value is a single byte (§14.2). The
final byte's high bits beyond the last value (bit positions
P mod 8 through 7, when P mod 8 ≠ 0) are the tile's **pad bits**;
their content is fixed by `[R-SER-05]` and they never encode
values. Every bit pattern of the value region decodes to a value
sequence — decoding a packed plane never fails over its content;
padding-position content binds writers (§14.5), never a reader's
decode path. `[R-SER-03]`

> **Note.** Pad bits are not padding positions (§11.3). A padding
> position is a whole sample position outside the layer's extents,
> arising in any layout; pad bits are a packed plane's final-byte
> unused high bits, arising only when P is not a multiple of 8. A
> plane can have many padding positions and no pad bits — §14.5
> gives both their content.

> **Example.** A planar bool tile, tile extents (2, 5), P = 10,
> values alternating true, false, … in ordinal order: byte 0 is
> `0x55` (bits 0–7 = values 0–7), byte 1 carries values 8–9 in bits
> 0–1 (`0x01`) and six pad bits. With the channel's fill false the
> tile decodes as `55 01`; with fill true, `55 FD` (pad bits 2–7
> set).

Whichever of §14.2 or §14.3 defines a tile's decoded size, a reader
MUST treat a decoded payload whose byte length is not exactly that
decoded size as a validity error at tile scope: decoded size is a
function of the layer's declarations alone — geometry, layout, and
channel types — never of payload content, and readers allocate from those
declarations, not from stored data. Every decoded size, and the
value count V, is a declaration-derived quantity under
`[R-ENC-04]`. `[R-SER-07]`

#### 14.4 Layout–type validity

Every combination of layout and channel types is defined: planar
layers carry any mix of channel types, each channel's plane
serializing under §14.2 or §14.3 by its type alone, and interleaved
layers carry any mix, numeric values at element size and bool
values as single bytes (§14.2). A reader MUST NOT reject a layer
for its combination of layout and channel types. `[R-SER-09]`

> **Note.** Identifier `[R-SER-04]`, which earlier governed this
> subsection, is withdrawn; per §2.2 it is permanently retired and
> never reassigned.

> **Note.** A single-channel numeric layer produces byte-identical
> tile images under either layout. A single-channel bool layer does
> not, wherever ⌈P/8⌉ ≠ P — ⌈P/8⌉ packed bytes planar versus P bytes
> interleaved — and both forms are valid; writers wanting compact
> masks choose planar. At P = 1 the two are the same length and
> `[R-SER-05]` fixes the planar pad bits to the channel's fill, so
> the images coincide exactly when that fill is false.

> **Rationale.** Bits inside a mixed sample tuple would need
> per-sample packed sub-fields with their own offset arithmetic and
> pad rules; single bytes keep the stride arithmetic uniform, and
> the packed form remains available as a planar plane. A bool
> channel is deliberately expressible in both layouts so that
> co-located mask + value tuples keep their schema type — a format
> that makes the honest type inexpressible gets the dishonest one.

#### 14.5 Padding content

Padding positions (§11.3) are serialized like any other position,
and their content is fixed: at every padding position, a writer
MUST encode, for each channel the position carries, that channel's
fill value — the recorded fill bytes for a numeric channel, the
recorded fill byte for an interleaved bool channel, the fill bit
in a packed plane. Every pad bit (§14.3) MUST carry the plane's
channel's fill bit. A conforming reader never returns this content
(`[R-GEO-04]`) and is not obligated to check it; a verifier MUST
check it, and a violation is a validity error at tile scope.
`[R-SER-05]`

> **Example.** A layer with extents (5, 5), tile extents (4, 4):
> grid 2 × 2, and the edge tile at tile coordinates (1, 1) covers
> coordinates 4–7 along both axes — one real position, (4, 4), and
> 15 padding positions. With one uint16 channel and fill `0xABCD`,
> that decoded tile is 32 bytes: value 0 is the stored sample, and
> values 1–15 are each the bytes `CD AB`.

> **Rationale.** Padding participates in compression and in the
> stored tile's checksum, so its content decides whether identical
> logical data yields identical bytes. Fill-encoded padding keeps
> one invariant everywhere — every stored value outside the layer's
> extents is fill — so a reader that forgets to clip observes fill
> (a defined value, not garbage), content-addressing stays
> deterministic, and padding can never leak writer memory.

> **Note.** This rule governs sample content inside decoded tiles.
> Slack between structures (alignment gaps, the pre-trailer pad,
> §5.2) is a different mechanism: writers zero it by advice, and no
> conformance requirement constrains its content.

### 15. Tile Index

#### 15.1 Region and entry layout

The owning scope of a layer's tile index is the layer; the owning
scope of an individual entry, and of the stored tile it addresses, is
the tile. Under
index_encoding 1 (the only encoding this format major version defines,
§7.4), the tile-index region addressed by the layer record's extent
slot is, contiguously:

> [ entry array: entry_count × 20 bytes ] [ segment CRC array:
> ⌈entry_count / 2¹⁶⌉ × 4 bytes ]

with no padding anywhere inside the region. Each entry is 20 bytes:

| Offset | Size | Type | Field | Class | Valid values |
|---|---|---|---|---|---|
| 0 | 8 | u64 | offset | structural | see §15.3 |
| 8 | 8 | u64 | length | structural | see §15.3 |
| 16 | 4 | u32 | crc | structural | CRC-32C of the stored tile's bytes (§8.1); 0 in a sentinel entry |

The entry for the tile with disk ordinal k (§11.4) is the k-th entry,
at region byte 20·k; entry order is disk-ordinal order, so a planar
layer's entries group channel-major. `[R-IDX-01]`

#### 15.2 The sentinel

An addressed tile that is not stored has the **sentinel entry**:
offset and length both `0xFFFF_FFFF_FFFF_FFFF` and crc 0 — the 20
bytes `FF ×16 00 ×4`. A sentinel tile contributes fill to the
reference array (§3.2, §13). Sentinel entries are a reserved pattern,
not offsets or lengths: `[R-ENC-03]`'s value-domain rule and
`[R-ENC-04]`'s sum rule apply to the fields of non-sentinel entries
only, and an entry with exactly one field at the sentinel value is
§15.3's own row before either rule reads it. `[R-IDX-02]`

> **Rationale.** All-ones was chosen over zero/zero for its failure
> modes: a zeroed index region (uninitialized buffer, filesystem
> hole) parses under this rule as offset 0 / length 0 — loudly
> invalid (§15.3) — rather than as a valid all-sparse index silently
> returning fill; an all-0xFF region (erased flash) is invalid too,
> since a sentinel's crc field is 0. A reader that forgets the
> sentinel test still fails safely: all-ones offsets trip the
> overflow and bounds checks.

#### 15.3 Entry validity

For each entry, with F the committed file length and S denoting the
sentinel value 2⁶⁴ − 1, a reader MUST classify as follows; rows
marked *verifier* require whole-index or whole-file knowledge and
bind verifiers, not ordinary readers. The per-entry outcomes below
govern notwithstanding the general owning-scope mapping of
`[R-ENC-03]`/`[R-ENC-04]`. Six rows are marked *structural*: they
classify an entry whose own 20 bytes yield no usable extent. Such an
entry contributes no stored extent to the *verifier* rows, which bind
over well-formed entries' extents only — `[R-SLB-03]`'s run
continuity closes over it as it does over a sentinel — and none to
`[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed
that no other claimant claims fall to slack. An entry whose only
defect is that its stored bytes fail its crc is well-formed: the
defect lies in the bytes it addresses, not in the entry, so its
extent stands and it keeps its place in the *verifier* rows, in run
continuity, and in the coverage walk. `[R-IDX-03]`

| Entry state | Outcome |
|---|---|
| offset = S ∧ length = S ∧ crc = 0 | valid sentinel — reads as fill |
| offset = S ∧ length = S ∧ crc ≠ 0 | *structural*: reject-tile |
| offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*: reject-tile |
| length = 0 (non-sentinel) | *structural*: reject-tile — absence is spelled sentinel; no codec emits zero bytes |
| offset < 16 (non-sentinel) | *structural*: reject-tile — the front block is never payload |
| offset > 2⁶³ − 1 or length > 2⁶³ − 1, neither field being S (non-sentinel) | *structural*: reject-tile (`[R-ENC-03]`) |
| offset + length overflows, or offset + length > F − 64, each field alone being in domain (non-sentinel) | *structural*: reject-tile — the extent would touch the live trailer or beyond |
| stored bytes fail the entry's crc | reject-tile (§8.2) — the entry itself is well-formed; its extent stands |
| two stored extents of the same layer overlap, or a stored extent overlaps its own layer's index region or sub-record extents | *verifier*: reject-layer (§7.2) |
| a stored extent overlaps any structure outside its own layer | *verifier*: reject-file (§7.2) |
| alignment or slab invariant violated (§16) | *verifier*: reject-layer |

#### 15.4 Segments and verification

Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)); the
s-th u32 of the segment CRC array is the CRC-32C over exactly those
entries' bytes as stored — the final partial segment's CRC covers
only its actual bytes. The segment CRC array is covered by the layer
record's crc_of_crc_array (§7.4, §8.1). To use entry k, a reader MUST
verify, in dependency order, crc_of_crc_array over the fetched CRC
array and the segment CRC over the fetched segment containing k
(both ranges are computable from the layer record alone and MAY be
fetched in parallel); any mismatch or cross-check failure
(`[R-CNT-17]`) is reject-layer. `[R-IDX-04]`

> **Note.** "To use" obliges verification, not re-verification:
> under committed-prefix immutability a reader MAY verify each
> range once and cache the result, keyed as §9.3 licenses
> (`[R-LIF-03]`).

The CRC-32C of a segment consisting of 2¹⁶ sentinel entries is
`0xEECB3BB2`; writers of sparse layers MAY emit this constant for any
**full** segment — one covering exactly 2¹⁶ entries, final or not —
whose entries are all sentinels, without computing
it — a partial segment's CRC MUST be computed. Equality with
the constant licenses nothing for readers: verification is byte
comparison of computed CRCs, never constant matching. `[R-IDX-05]`

> **Example.** A layer with entry_count = 1,000,000: 16 segments (15
> full, the last covering 16,960 entries), a 64-byte segment CRC
> array, index region 20,000,064 bytes. Tile k = 999,999 lives in
> segment 15 at segment-relative byte 20 × 16,959 = 339,180; a reader
> fetches the CRC array at region bytes [20,000,000, 20,000,064) and
> segment 15 at [19,660,800, 20,000,000) in parallel — ~339 KB
> verified to read one cold tile here — and never more than one full
> segment (1.25 MiB) plus the CRC array, at any layer scale. A layer
> with 1 ≤ entry_count ≤ 65,536 has one segment and a 4-byte array:
> fetching the whole region and verifying one CRC is the naive reader,
> unchanged. At entry_count = 0 there is no region at all — zero
> segments, a zero-byte CRC array, extent slot (0, 0) and
> crc_of_crc_array = 0 (§7.4, `[R-CNT-17]`, `[R-CNT-23]`) — so nothing
> is fetched and nothing is verified.

> **Example.** The planar layer of §11.4's example (C = 4, N = 32):
> the tile carrying channel 2 at spatial ordinal 10 has disk ordinal
> 74; its entry occupies region bytes [1,480, 1,500). With every tile
> of channel 3 unstored, entries 96–127 are 32 copies of
> `FF ×16 00 ×4`.

### 16. Slabs and Alignment

A layer that declares neither alignment nor a slab makes no layout
promise: its stored tiles MAY occupy any non-overlapping byte
positions, in any order — a streaming writer places tiles in
acquisition order at no cost to conformance (`[R-CNT-13]`). That
freedom is over *ordering and relative position*, and a byte the live
state does not claim is slack whatever produced it (§5.2). A writer
that scatters structures wastes space rather than violating a rule,
and the verifier's slack total, where its walk completes, is what
surfaces the waste.
`[R-SLB-05]`

#### 16.1 Per-tile alignment

A layer MAY declare alignment A (§7.4): a power of two with
512 ≤ A ≤ 2⁶². Writers MUST NOT emit any other nonzero value; a reader MUST treat
one as a validity error at layer scope (`[R-CNT-23]`). When declared:
every stored tile's offset satisfies offset mod A = 0. The bytes
alignment leaves between structures are slack (§5.2), which writers
SHOULD zero and no conformance requirement constrains. A verifier MUST check the invariant
(violation: reject-layer, §15.3); readers are not obligated to —
offsets are always explicit, so alignment is reader-invisible.
`[R-SLB-01]`

> **Note.** 4096 — the page size and modern physical sector size —
> is the recommended value for writers that align: it satisfies
> O_DIRECT, mmap, and GPU direct-storage paths everywhere. 512 is
> the legacy sector floor.

#### 16.2 The slab declaration

A layer MAY declare a slab run length S ≥ 1 with slab alignment
A_slab, a power of two ≥ 1 (§7.4; mutually exclusive with per-tile
alignment, `[R-CNT-16]`). Runs partition each contiguous block of
disk ordinals independently: for an interleaved layer the single
block [0, N); for a planar layer each channel block [c·N, (c+1)·N) —
runs never span channel blocks, and the final run of a block can
cover fewer than S ordinals. Run r of a block starts at ordinal
block_start + r·S. `[R-SLB-02]`

When declared, for every run: the run's stored tiles are contiguous
and packed in ordinal order — each stored tile's offset equals the
previous stored tile's offset plus that previous tile's length — and
the first stored
tile's offset satisfies offset mod A_slab = 0. The runs themselves
are not mutually ordered or joined: between runs, placement freedom
(`[R-SLB-05]`) governs, and the bytes left between them are slack
(§5.2), which writers SHOULD zero. Sentinel tiles are transparent to run continuity: they
occupy no bytes and do not break packing. So are the entries §15.3
classifies reject-tile on a *structural* ground: they address no
usable extent, and the run's stored tiles close over them. An entry
whose only defect is that its stored bytes fail its crc is not
transparent — its offset and length stand, and the packing relation
reads them as it does any other stored tile's — so this invariant
stays decidable from the index entries alone, given the committed
file length §15.3 already requires to classify any entry. A run with no stored
tiles
imposes nothing. A verifier MUST
check these invariants (violation: reject-layer, §15.3); readers are
not obligated to, and MAY instead detect contiguity arithmetically
from any index segment. `[R-SLB-03]`

A writer or updater whose commit changes the stored-tile set, the
run partition, the byte placement of any run, the disk ordinal of
any tile the new state stores, or the slab declaration itself, of a
layer slab-declared in either the superseded or the new generation,
MUST either
re-establish the invariants for every such run — or clear the declaration in
the new generation; carrying a stale declaration forward is a
validity error at layer scope, detected as the invariant failures
of `[R-SLB-03]` are: by a verifier. `[R-SLB-04]`

> **Note.** Because this rule's detection *is* `[R-SLB-03]`'s, a stale
> declaration carries no register row of its own: every file exhibiting
> one exhibits a run whose tiles are unpacked or whose first stored tile
> is misaligned, which §21.3 registers. The obligation here is the
> writer's, and it is what makes those two rows reachable at all after a
> commit.

> **Note.** The declaration is never copied blindly: tools that
> modify a layer parse its full layer record, with the updater
> obligations detailed in §20.

> **Note — what slabs are, and are not.** A slab guarantees
> *contiguity*: consecutive disk ordinals occupy consecutive bytes.
> Which tiles are ordinal-consecutive is the linearization field's
> job (§11.4); under row-major, a run is a band along the
> last-declared dimension. Rectangular-window locality is therefore
> not a slab property — it belongs to the reserved space-filling-
> curve linearization values, under which the same slab machinery,
> unchanged, would make compact windows contiguous. Slabs are the
> byte-layout half of that future answer. With A_slab = 1 a slab is
> contiguity-only — the right declaration for remote range
> coalescing with no direct-I/O alignment need.

> **Example.** The §11.2 layer (grid 4 × 8, N = 32, interleaved)
> with S = 8, A_slab = 4096: four runs — ordinals [0, 8), [8, 16),
> [16, 24), [24, 32) — each one tile-row, each run's first stored
> byte 4096-aligned, interiors packed. A viewport spanning tile rows
> 1–2 is ordinals 8–23 = exactly runs 1 and 2: two range requests
> regardless of stored-tile sizes. If ordinal 10 is a sentinel, run
> 1's stored tiles are 8, 9, 11…15, packed with no gap where 10
> would have been.

### 17. Codecs and Filters

The owning scope of a layer's codec and filter declarations is the
layer; the owning scope of one stored tile's payload under them is
the tile (§2.4).

#### 17.1 The pipeline

A stored tile's bytes are produced from its decoded tile image
(§14) by two per-tile stages: the layer's **filter** (§17.3), then
its **codec** (§17.2) — the filtered image is the codec's input. A
reader reverses the stages: after the entry's crc verifies (§8.2),
the codec decodes the stored bytes, the filter's inverse is
applied, and the result is the decoded tile image, subject to
`[R-SER-07]`'s exact-size rule. Both stages consume and produce
whole tiles. `[R-COD-01]`

Every stored tile is independently decodable from its stored bytes
and its layer's record alone: neither stage carries state between
tiles, references bytes outside the tile's stored extent, or
requires side data — dictionaries included (§17.2). Slabs (§16)
are an I/O grouping, never a compression context. `[R-COD-02]`

#### 17.2 Codecs

Field values of the layer record's codec field (§7.4): 0 is
invalid; 1 = none, 2 = deflate, 3 = zstd, and 4 = lz4 are assigned
below, and all four are **core** — a conforming reader MUST
implement every one of them (`[R-CNF-03]`); values 5 through
0x7FFF are reserved for future assignment by this specification;
values ≥ 0x8000 are the experimental range (§10). Writers MUST NOT
emit a codec value other than 1 through 4; a reader MUST treat any
other value — 0, every reserved value, and the experimental range
included — as a validity error at layer scope (`[R-CNT-23]`).
`[R-COD-03]`

**Codec 1 — none.** The stored bytes are the filtered image
verbatim. A **non-sentinel** index entry's length therefore MUST equal
the tile's decoded size (§14.2, §14.3); a reader MUST treat a mismatch
as a validity error at tile scope — checkable from the entry and the
layer record alone, before any payload fetch. `[R-COD-04]`

**Codec 2 — deflate.** The stored bytes are exactly one DEFLATE
compressed data stream as defined by RFC 1951 — raw, not a zlib
(RFC 1950) or gzip (RFC 1952) wrapper. `[R-COD-05]`

> **Note.** A raw DEFLATE stream ends on a bit boundary, and RFC 1951
> fixes no value for the unused high bits of its final byte — up to
> seven of them. This specification constrains them nowhere. They lie
> inside the tile's stored extent, so the entry's crc covers them and
> corruption there is detected; but two files differing only in those
> bits decode to the same tile image and are both conforming, which is
> encoder freedom of the kind `[R-CNF-05]` licenses and Appendix G's
> item 1 closes by pinning the encoder. A whole byte after the one
> holding the final bit does trail the stream, and `[R-COD-08]`
> rejects it (§21.4, T24).

**Codec 3 — zstd.** The stored bytes are exactly one Zstandard
compressed frame as defined by RFC 8878: they MUST begin with the
compressed-frame magic (0xFD2FB528, the bytes `28 B5 2F FD`), and
a reader MUST treat a payload whose first four bytes are not that
magic, or that contains a skippable frame anywhere or more than
one frame, as a validity error at tile scope. Three frame
features are excluded. Writers MUST NOT
compress a tile using a dictionary — whether or not the header
discloses one — and MUST NOT emit a nonzero dictionary ID; a
reader MUST treat a frame carrying a nonzero dictionary ID as a
validity error at tile scope. Dictionary use the header does not
disclose is not detectable by inspection and need not decode to
an error: it is a writer violation whose consequence is wrong
decoded content, the same undetectable class as any other writer
that emits wrong bytes (§21). Writers MUST
NOT set the frame's content-checksum flag — the entry's crc
already serves that role — and MUST NOT declare a window size
exceeding the tile's decoded size; a reader MUST treat either as
a validity error at tile scope, both being header-checkable. The
frame content-size field MAY be present; when present it MUST
equal the tile's decoded size, a reader MUST treat a mismatch as
a validity error at tile scope, and a reader MUST NOT allocate or
size any buffer from it — the decoded size comes from the layer's
declarations alone (§14, `[R-SER-07]`). Writers SHOULD keep the
declared window within §21.9's 8 MiB `Window_Size` guarantee even
for a larger tile; a wider window is conforming and merely permits
a conforming reader to decline the tile or the layer on resource
grounds (`[R-ERR-04]`). `[R-COD-06]`

> **Note.** RFC 8878 derives a frame's Window_Size two ways, and for a
> tile this rule they agree: with Single_Segment_Flag set there is no
> Window_Descriptor and Window_Size is the frame content size, which
> this requirement already obliges to equal the decoded size; without
> it, the Window_Descriptor cannot express less than 1 KiB. A tile
> whose decoded size is below 1 KiB — §14.2's worked examples give 18
> and 30 bytes, §14.3's gives 2 — is therefore encodable under codec 3
> only as a single-segment frame, and no conforming file turns on which
> derivation a reader implements.

> **Note.** Whole-buffer zstd decoders that tolerate concatenated
> or skippable frames do not by themselves enforce the
> exactly-one-frame rule: an implementation confirms that the
> single frame spans the full stored extent — a frame-boundary
> query or a streaming decode to end-of-frame, standard API in
> every binding. The minimum window size a conforming reader must
> support is §21's subject.

**Codec 4 — lz4.** The stored bytes are exactly one LZ4 block per
the LZ4 Block Format Description (lz4_Block_format.md, version
1.0; Appendix F pins the exact revision), decoded with the stored
length as the input size and the decoded size as the output
capacity. The LZ4 frame format is not used. Writers MUST NOT
declare this codec for a layer any of whose addressed tiles' decoded
size exceeds 0x7E000000 bytes — the block format's practical
interoperability bound; in a planar layer each channel's plane carries
its own decoded size (§14.2, §14.3), and the largest governs — and a reader MUST treat such a declaration as a validity
error at layer scope, checkable from declarations alone.
`[R-COD-07]`

> **Note.** The cap is quantified over the layer's *addressed* tiles,
> so a layer that addresses none — any dimension extent 0
> (`[R-GEO-02]`, §21.6) — satisfies it whatever its tile shape
> declares, and codec 4 is conforming there. The escape ends exactly
> when the layer's addressed-tile count rises above 0, which takes
> every dimension's extent nonzero (§11.2) — a growth that leaves any
> extent at 0 holds the count at 0 and the escape with it — and the
> same declarations are then measured against the cap.
> `[R-ENC-04]`'s overflow rule carries no such quantifier — it binds
> every quantity it designates, whether or not the layer addresses a
> tile — so the decoded sizes the layout gives, P·Q for an
> interleaved layer and each channel's P·Bᶜ or ⌈P/8⌉ for a planar one,
> are checked in an empty layer even though this cap is not.

For every codec: the stored bytes MUST decode to exactly the
decoded size — no more, no fewer — and the decode MUST consume the
stored bytes exactly, with no trailing bytes past the stream,
frame, or block; a reader MUST treat a malformed stream and either
inexactness as a validity error at tile scope (`[R-SER-07]`).
`[R-COD-08]`

> **Note.** Decoded output is never empty — §14's decoded sizes
> are at least 1 byte — and none of the codecs above emits zero
> bytes for a nonempty input; the index rule that a zero-length
> non-sentinel entry is invalid (§15.3) rests on both facts.

> **Note.** For the compressing codecs (2–4), no bound relates a
> stored length to its decoded size in either direction — codec
> 1's equality is `[R-COD-04]`'s subject. Compression may expand,
> and a reader allocates from declarations, never from stored
> data or embedded size fields. Resource limits are §21's
> subject.

#### 17.3 The filter

Field values of the layer record's filter field (§7.4): 0 is
invalid; 1 = none — the filtered image is the decoded image — and
2 = byte-shuffle, defined below, are assigned, and both are
**core** — a conforming reader MUST implement both
(`[R-CNF-03]`); values 3 through 0x7FFF are reserved
for future assignment by this specification; values ≥ 0x8000 are
the experimental range (§10). Writers MUST NOT emit a filter value
other than 1 or 2; a reader MUST treat any other value as a
validity error at layer scope (`[R-CNT-23]`). `[R-COD-09]`

**Byte-shuffle.** The shuffle stride s is the channel's element
size for a planar tile and the sample stride Q for an interleaved
tile (§14.2); for a packed boolean plane s = 1 and the filter is
the identity. The decoded image's length L is divisible by s in
every case (§14). Viewing the image as n = L/s consecutive groups
of s bytes, the filtered image places byte i of group j at offset
i · n + j — all first bytes in image order, then all second bytes,
and so on; the inverse restores byte i · n + j to offset j · s + i.
Length is unchanged. A writer that filters with any other stride
violates this rule; where the resulting decoded image breaks a
stated content obligation (§14.5's padding, `[R-SER-08]`'s bool
bytes) a verifier detects it as a validity error at tile scope,
and otherwise the consequence is wrong sample content —
undetectable by construction (§21.7). `[R-COD-10]`

> **Example.** Three float32 values 1.0, 2.0, 3.0 decode as
> `00 00 80 3F 00 00 00 40 00 00 40 40` (s = 4, n = 3). Shuffled:
> `00 00 00 00 00 00 80 00 40 3F 40 40` — the three first bytes,
> the three second bytes, then `80 00 40`, then `3F 40 40`.

> **Rationale.** Same-significance bytes are far more self-similar
> than adjacent mixed bytes, and the gain survives interleaving:
> measured on representative interleaved data (float32 triples
> with a class byte; four-channel uint16), stride-Q shuffle
> reduced deflate output by 28–33% — comparable to the planar
> case — which is why interleaved layers are in scope.

#### 17.4 Certification under codecs

The decoded-content obligations of §14 (`[R-SER-05]`,
`[R-SER-08]`) require decoding. A verifier that cannot execute a
layer's codec or filter cannot establish that layer's conformance
and MUST NOT certify the file. That inability is not a finding that
the file is nonconforming, and it fixes the file's verdict as
*cannot establish* only where the verifier established no violation
elsewhere (`[R-CNF-11]`). For a conforming reader that
position arises only at a reserved or experimental value, every
assigned codec and filter being core: it rejects the layer
(`[R-COD-03]`, `[R-COD-09]`);
software unable to execute an assigned codec or filter is not a
conforming reader (`[R-CNF-03]`). `[R-COD-11]` The
metadata-encoding space differs from the codec and filter spaces:
an experimental-range document encoding in a conforming file is not
a violation (§21.6), no document rule attaches to its extent, and
certification is unaffected (`[R-MTA-10]`, §18.2).

### 18. User Metadata

#### 18.1 The document

A file MAY carry one user-metadata document at file scope, and each
layer MAY carry one of its own, each held in a user-metadata
record's extent (§7.1). Its content is application data: this
specification defines its encoding, not its meaning. `[R-MTA-01]`

The owning scope of a user-metadata record is the file when the
record is top-level and the layer when it is a sub-record — but the
outcome of every failure to read its **document** is ignore-record
whatever the scope, because the document is **quarantined**
(`[R-CNT-25]`). The quarantine covers the document only: a
malformed extent slot on such a record, (0, 0) included, is a
validity error at the record's containing scope (`[R-CNT-13]`,
`[R-CNT-25]`), because that failure precedes the document. A
reader MUST NOT let any part of a user-metadata document affect how
a byte is located, decoded, or returned; structural facts live in
structural fields, and a reader that consults metadata to decode has
built a second parser out of untrusted input (§22.4). `[R-MTA-02]`

#### 18.2 Encoding

A user-metadata record's inline payload is exactly one byte:

| Offset | Size | Type | Field | Class | Valid values |
|---|---|---|---|---|---|
| 0 | 1 | u8 | encoding | structural | 1 or 2 assigned; 0 invalid, 3–0x7F reserved, ≥ 0x80 experimental (§10); see below |

A record whose inline_length is not 1 is a validity error at the
record's containing scope — the payload is a fixed structure
(`[R-ENC-07]`), not a growable one. Field values: 0 is invalid;
1 = none and 2 = zstd are assigned; 3 through 0x7F are reserved;
values ≥ 0x80 are the experimental range (§10). Both assigned
encodings are core: a conforming reader MUST be able to decode
encoding 2, whose decoder `[R-COD-11]` already requires of it for
codec 3 (`[R-CNF-03]`). An encoding a reader does not implement is
therefore one this specification does not assign, and is
ignore-record (`[R-CNT-25]`). `[R-MTA-03]`

Encoding 1 stores the document verbatim. Under either encoding a
reader decodes with a bound of its own choosing, no smaller than
§21.9's user-metadata guarantee, and a document exceeding that
bound is ignore-record like any other it cannot read; §21.9's row
is stated over a document's decoded size, which a verbatim
document has as surely as a compressed one. Encoding 2 stores it as
exactly one RFC 8878 compressed frame occupying the extent's bytes
before its terminal CRC, under every frame constraint `[R-COD-06]`
places on a frame, named here or not, save two: what it states
against a tile's declared decoded size, and what it states about
the frame's declared `Window_Size`. This section replaces both,
below. Carried over — named for convenience, not as a closed list —
are the frame magic; no skippable frame and no second frame; no
dictionary use, disclosed or not, and no nonzero dictionary ID; no
content-checksum flag; and the bar on sizing any buffer from a
length the frame itself declares. Two of those fall outside the
register, on the two distinct grounds §21.7 separates, and R4
registers neither: dictionary use the header does not disclose is a
writer violation nothing in the extent shows — an unwitnessed
condition, exactly as `[R-COD-06]` has it for a tile (§21.7) — while
the bar on sizing a buffer binds a reader rather than the document,
and so states no condition a file can exhibit at all.
The decoded-size exception holds because a document has no declared
size,
which is why the bound above is the reader's own and not the
file's. The frame's declared `Window_Size` is unconstrained here
for the same reason, and takes the same
treatment: a reader's window bound is its own, no smaller than
§21.9's guarantee for that quantity, and a frame declaring more
than the reader admits is ignore-record on that ground — the
reader's capability, not a failure to decode within the meaning of
R3, and no violation: the file exceeds a §21.9 guarantee and so
remains conforming while the reader MAY decline it (`[R-ERR-04]`).
Writers SHOULD keep the declared window within §21.9's 8 MiB
`Window_Size` guarantee even for a larger document, as
`[R-COD-06]` asks for a tile. Where the frame sets
Single_Segment_Flag there is no Window_Descriptor and RFC 8878
makes the frame's `Window_Size` its content-size field, which this
section pins below to the decoded document's byte length: a
document larger than that guarantee, framed that way, exceeds a
§21.9 row and so falls outside `[R-CNF-03]`'s acceptance duty,
and a writer that needs one frames it with a Window_Descriptor
instead. §21.9's user-metadata row bounds a document's decoded
size; it does not relieve the frame carrying it of the
`Window_Size` row. The frame's content-size field, unlike the
decoded size and the window, is *not* left to the reader: it MAY
be present, and when
present it MUST equal the byte length of
the decoded document. A mismatch is one of the frame
constraints R4 registers, not a failure to decode under R3: the bytes
decode, and what is wrong is what the header said about them. Routing
it to R4 keeps the condition checkable from the bytes alone rather
than turning on a decoder's tolerance (`[R-CNF-02]`) — the tile rule
of `[R-COD-06]` transposed to the quantity a document does have, its
decoded length, in place of the declared size it does not. A **verifier** that declines to decode a document on
either bound above cannot establish that document's conformance and MUST NOT certify
the file, exactly as `[R-COD-11]` requires of a codec it cannot
execute; the bound is that verifier's capability and not a limit on
validity (`[R-CNF-10]`), so the decline is not a finding that the
file is nonconforming and a verifier MUST NOT report it as one. The
decline is one of the unchecked requirements `[R-CNF-11]` obliges
the verifier to report, and it fixes the file's verdict as *cannot
establish* only where the verifier established no violation
elsewhere; the verifier SHOULD report the bound it applied and the
stored length of the extent it declined, since the report
`[R-CNF-11]` requires names the requirement and the ground but not
the quantities an operator needs to raise the bound and re-run the
check. The
decline presupposes an
encoding this specification assigns, whose document it defines; an
encoding it does not assign leaves no document rule attached and is
`[R-MTA-10]`'s subject, not a decline. Any violation here is
ignore-record, never the tile-scope outcome §17.2 assigns. `[R-MTA-09]`

> **Note.** The 16 MiB figure is a §21.9 minimum guarantee, so the
> two rules compose here as they do elsewhere. A file whose document
> decodes to more than the guarantee stays conforming, and it falls
> outside `[R-CNF-03]`'s acceptance duty, which runs only to a
> conforming file none of whose values exceeds those guarantees. A
> reader whose own bound it exceeds takes ignore-record for that
> record, which is also the narrowest scope at which `[R-ERR-04]` lets
> it decline the document on resource grounds; it MAY instead decline
> any scope containing the record, the whole file included. Either
> refusal is reported as a resource limit, not as corruption.

The decoded document is a JSON text as defined by RFC 8259, encoded
in UTF-8. Four restrictions apply, and a document violating any of
them is unreadable — ignore-record, with the report `[R-CNT-25]`
asks for:

- **A JSON object, unmarked.** The top-level value is an object,
  and the encoding carries no byte-order mark: a leading U+FEFF
  makes the document unreadable.

- **Finite numbers only.** A reader interprets every JSON number as
  the IEEE 754 binary64 value its decimal text converts to under
  IEEE 754's default rounding-direction attribute, roundTiesToEven,
  and MAY hold the value so obtained in a wider representation. A
  document is unreadable if it contains a number whose binary64
  interpretation is not finite — which covers a magnitude that
  overflows on that conversion, `1e400` being the ordinary case — or any
  of the bare tokens `NaN`, `Infinity`, or `-Infinity`, which RFC
  8259 does not admit and some parsers accept regardless. Writers
  SHOULD NOT emit a number binary64 cannot represent exactly; a
  value needing bit-exact representation belongs in a structural
  field (§13.1), not here.
- **No duplicate keys.** Key identity is the *decoded* string, not
  its JSON source bytes: `"a"` and `"\u0061"` are the same key, and
  a document in which any one object carries that key twice is
  unreadable, since which member wins would otherwise be a parser's
  choice. `[R-MTA-05]`'s sort order is likewise over decoded keys'
  UTF-8 bytes.
- **Well-formed UTF-8 throughout** (`[R-ENC-11]`) — including after
  escape resolution: a `\uXXXX` escape denoting an unpaired
  surrogate has no UTF-8 encoding and makes the document unreadable,
  as does an ill-formed byte sequence in the source — and every key
  satisfying §4.6's name rules — non-empty, at most 255 bytes, free
  of U+0000 through U+001F. Key comparison is raw bytes
  (`[R-ENC-13]`), so two keys differing only in Unicode
  normalization are distinct keys.

`[R-MTA-04]`

Writers MUST serialize object members, at every nesting depth, in
ascending order of their keys' UTF-8 bytes, compared lexicographically
as unsigned bytes with a proper prefix ordering first. This makes one
writer's output reproducible for identical content; it does not make
two writers' output identical, and this specification promises no
byte-identity here or anywhere else (`[R-CNF-05]`) — an application
needing content-addressed metadata canonicalizes the decoded document
itself. Readers MUST NOT depend on member order for meaning, and
unsorted members do not make a document unreadable: the file is
nonconforming, a verifier MUST report it, and readers process the
document unchanged. `[R-MTA-05]`

The document rules of this section — the frame constraints of
encoding 2, the decoded-document restrictions above, and
`[R-MTA-05]`'s member ordering — attach to a document only under an
encoding this specification assigns. Under an unassigned encoding
this specification defines no decoding, and for an experimental
value §10.3 lets two unrelated experiments claim the same value with
different meanings, so *the decoded document* names nothing this
specification can test: no content rule attaches to the extent's
bytes, and file conformance — a pure predicate on bytes
(`[R-CNF-02]`) — is decided by the structural checks that precede
the document alone: the record's framing and extent slot
(`[R-CNT-13]`), the encoding byte's own value set (`[R-MTA-03]`),
and the extent's terminal CRC (`[R-CNT-20]`). A verifier meeting
such a record in an otherwise conforming file has no requirement it
is unable to check — the record is not among `[R-CNF-11]`'s
cannot-establish grounds, and at an experimental-range encoding
certification is unaffected, encoding 0 and a reserved value being
R1's violations — and it MUST report each record it ignored on this
ground, naming the
owning scope, the encoding value, and the stored extent length, as
it reports the slack total (`[R-CNT-21]`): bytes a certificate
covers without inspecting are counted and named, never silent.
`[R-MTA-10]`

> **Note.** JSON was chosen over a binary encoding because every
> target language parses it without a dependency, and because a
> document a human can read in a hex dump's tail is one a human can
> debug. The costs are real and priced: no binary values — base64 in
> a string is the escape — and no cross-writer byte-identity, since
> JSON number formatting varies by runtime.

#### 18.3 Keys and namespaces

The key prefix `tarn.` is reserved for keys this specification
registers (§10.4); writers MUST NOT emit a `tarn.`-prefixed key this
specification's registry does not define at the version they target,
and a reader MUST ignore a `tarn.` key it does not recognize rather
than guessing. A file carrying an unrecognized `tarn.` key is
**conforming** — later minor versions register keys, exactly as
they define ignore-lane flag bits (§6.3), and this text's readers
skip both harmlessly. Every other key is application
space: applications SHOULD prefix theirs with a domain they control
in reverse-DNS form, and an application using an unprefixed key
accepts that another application can mean something else by it.
`[R-MTA-06]`

#### 18.4 Standardized keys

This specification registers the following. Each is OPTIONAL and
advisory — being metadata, none can affect decoding
(`[R-MTA-02]`) — and a reader that finds one malformed MUST ignore
that key rather than the document.

| Key | Scope | Value |
|---|---|---|
| `tarn.title` | file, layer | string: a short human-readable label |
| `tarn.description` | file, layer | string: longer prose |
| `tarn.created` | file | string: an RFC 3339 `date-time` |
| `tarn.creator` | file | string: the producing software's name and version |
| `tarn.axes` | layer | array of one object per dimension, in declared order, each with optional `unit` (string), `origin` (number), and `step` (number) |
| `tarn.stats` | layer | object keyed by channel name, each value an object with optional `min` and `max` (numbers) |

A writer SHOULD emit a standardized key only within the scopes its row
lists, and only with a value of the shape its row gives. A reader MUST
ignore a standardized key found outside its listed scope, or whose
value does not match the shape its row gives, rather than rejecting
the document. Neither placement nor value shape bears on validity: the
file stays conforming, exactly as it does for an unrecognized
`tarn.`-prefixed key (§21.6). No reader's behavior turns on either,
since a reader ignores such a key and reads the rest of the document —
and enforcing them would put a verifier to work on the content of
metadata, which §21.6 declares a non-violation rather than a check
any actor owes. `[R-MTA-07]`

`tarn.axes` gives the affine mapping from a dimension's integer
coordinate i to a physical position, `origin + i × step`, in the
stated unit — the convention scientific consumers need, kept out of
the core so that no reader is obliged to parse it and no future
domain convention needs a format revision to exist (§10.1).

`tarn.stats` reports the minimum and maximum finite value observed
per channel, NaN excluded from both. It is a hint for range scaling
and nothing more: it MAY be absent, MAY be stale after any commit
that changes the layer, and a reader MUST NOT use it to skip reading
data it would otherwise read, nor to decide any question of
correctness. `[R-MTA-08]`

> **Note.** Advisory needs no enforcement machinery here. Because
> metadata cannot affect decoding by construction, a stale
> `tarn.stats` misleads a colour ramp and nothing else — which is
> why statistics live here rather than as a structural record whose
> staleness would need rules, verifier obligations, and an
> updater's attention.

---

## Part III — Behavior

### 19. Reading a TARN File

This section consolidates the reader's normative path: the open
algorithm, the validation-timing rule, layer access, and the
tile-read algorithm. It introduces no new structures; each step
cites the requirement whose outcome governs its failure.

Each step names the checks its tier's structures turn on. Those
enumerations are not the complete inventory of what a reader
detects at that tier: §21's register is, and `[R-CNF-04]` binds a
reader to every register row whose detector is the reader, at the
tier that row's *Detected* cell names (§21.1). A row this section
does not restate is due at its own tier all the same, with its
governing rule's own outcome.

#### 19.1 The open algorithm

A conforming reader opens a file by these steps, in order:

1. **End of file.** Obtain the transport-authoritative file size F
   (`[R-CNT-10]`); an F below 128 is a validity error at file scope
   decided from F alone and needing no other byte of the file
   (`[R-CNT-27]`, F5). These steps are
   ordered by dependency, not by
   I/O: where the transport discloses a range response's complete
   length, a remote reader's suffix range for step 2 carries F in its
   own response, so steps 1 and 2 cost one request between them
   (§6.4), and a local reader obtains F without any. A reader
   whose open leaves bytes [0, 16) resident — a speculative suffix
   window that reached offset 0 included — MUST verify the front
   signature block by byte equality before other processing
   (mismatch: reject-file); one that would have to issue a further
   range request for them MAY defer or omit the check
   (`[R-CNT-04]`).
2. **Trailer.** Fetch bytes [F − 64, F) and validate them in
   §6.2's fixed order — magic, trailer CRC, version gate, then the
   remaining field gates (`[R-CNT-06]`, `[R-CNT-07]`,
   `[R-CNT-08]`). The validated trailer is the session's snapshot
   (§9.5, `[R-LIF-05]`); no later step re-reads the file's end.
3. **Directory.** Fetch [dir_offset, dir_offset + dir_length) and
   verify the directory CRC before any other use of the region
   (`[R-CNT-11]`).
4. **Record walk.** Parse the record sequence under §7.2's framing
   (`[R-CNT-12]`), applying the MUST_UNDERSTAND gate for unknown
   top-level types (`[R-CNT-15]`), the per-type multiplicity rules
   (`[R-CNT-14]`), the extent-slot validity rules for non-layer
   top-level records (`[R-CNT-13]`), and the framing rules a
   top-level user-metadata record carries on top of those — no
   (0, 0) slot, extent_length at least 5, inline_length exactly
   1 (`[R-CNT-25]`, `[R-MTA-03]`) — all decidable from the
   resident bytes and F — and build the layer table: each
   layer record's name, parsed and checked per §4.6
   (`[R-ENC-12]`). A duplicate layer name is a validity error at
   file scope, here, at open (`[R-ENC-15]`, §19.2). The layer-name
   namespace is built from the name fields a reader can obtain
   under §7.4's framing: a layer record whose name field does not
   lie entirely within that record's inline_length yields no name
   field to compare, so it contributes no name to the namespace and
   is instead a validity error at layer scope (`[R-CNT-18]`).
   Uniqueness is
   decided first, and over the raw name bytes whether or not each
   name is itself well-formed — `[R-ENC-13]` makes name comparison a
   byte comparison, which needs no valid name — so two layers whose
   name fields are byte-identical are a duplicate even when neither
   name is valid.

Completing these steps is **the open**. It consumes the trailer
and directory only — no extent slot's content, no tile index, no
payload — so its I/O is §6.4's request accounting (`[R-CNT-09]`,
including the suffix speculation that merges steps 1–3) at any
layer count and file size. `[R-RDR-01]`

#### 19.2 Validation timing

A reader MUST detect each violation whose detection this
specification obliges readers to make — a violation whose assigned
detector is the verifier (§2.4, `[R-CNF-12]`) imposes no reader
obligation — no later than the reader's first reliance on the
structure that carries it:

- **at open:** the front signature block, for a reader whose open
  leaves it resident (`[R-CNT-04]`), the trailer, the directory
  region and its record walk, and the layer-name namespace
  (§19.1's steps);
- **at first access to a layer:** the full validation of that
  layer's record (§19.3), before any use of the layer's
  declarations;
- **at use of a tile:** the index-chain, payload, and decode
  checks (§19.4), before any sample of that tile is returned;
- **at use of a record's extent:** that extent's CRC and the
  content rules of the document it carries — those §18.2 attaches
  at its encoding (`[R-MTA-10]`) — before anything the
  extent holds is returned — no earlier, since the open fetches
  no extent (§19.1).

Failure at any point takes the violated rule's own outcome and
scope — in particular, index-chain failures take layer scope
(`[R-IDX-04]`) although their detection point is tile use. A
reader MAY detect any violation earlier (`[R-CNF-12]`); it MUST
NOT return data whose governing structure has not passed the
validation this rule requires at its tier. Structures a request
never relies on impose no detection obligation beyond the open
steps: a violating record in a layer never accessed leaves every
other layer's reads conforming. `[R-RDR-02]`

> **Rationale.** The rule fixes the *latest* detection point, so
> the served-versus-failed boundary is deterministic: no
> conforming reader returns data its tier's validation would have
> refused. Earlier detection stays licensed, so a stricter reader
> can reject a nonconforming file sooner — divergence is only
> ever toward earlier rejection, never toward silent acceptance.
> The open's I/O stays two requests regardless of layer count;
> its one namespace-wide obligation — parsing each record's
> name — runs over bytes already fetched and CRC-verified.

#### 19.3 Layer access

A reader's **first access** to a layer — the first operation using
any of the layer's declarations other than its name, whose parse
§19.1 step 4 places at the open — MUST be preceded by full
validation of the layer record — extent slot and inline payload
both: the slot's validity rules (`[R-CNT-13]`), the §7.4
constraint set (`[R-CNT-23]`, `[R-CNT-16]`), the exact parse,
sub-record walk, and sub-record multiplicity (`[R-CNT-18]`,
`[R-CNT-14]`), dimension- and channel-name rules (`[R-ENC-11]`,
`[R-ENC-12]`, `[R-ENC-15]`), the framing rules a user-metadata
sub-record carries — no (0, 0) slot, extent_length at least 5,
inline_length exactly 1 (`[R-CNT-25]`, `[R-MTA-03]`) — the u64 value
domain of §4.2 (`[R-ENC-03]`), the value sets of §7.4, §11.4, §12.2, §14.1,
§17.2, and §17.3, the per-type fill constraints (§13.2,
`[R-TYP-07]`), the codec declaration bounds (`[R-COD-07]`), the
geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`),
the 2⁶³ − 1 ceiling on every quantity that arithmetic derives
(`[R-ENC-04]`) and on the decoded sizes §14 derives from it
(`[R-SER-02]`, `[R-SER-07]`),
and the index cross-checks computable without I/O
(`[R-CNT-17]`). All are decidable from the resident directory and
F: layer access performs no fetch, and failure takes each cited
rule's own scope. `[R-RDR-03]`

#### 19.4 The tile-read algorithm

A **point request** names a single coordinate (§3.1); a **region
request** names a rectangular range of coordinates, one interval
per dimension, and a range whose every interval holds a single
position is a region request. For a request of either form
against an accessed layer, a conforming reader proceeds as
follows; each step's failure takes the cited rule's outcome:

1. **Domain.** For a point request, verify 0 ≤ xᵢ < Eᵢ for every
   dimension; a coordinate outside the extents addresses nothing
   in the reference array (`[R-MDL-01]`) — the request fails as a
   request, with no verdict on the file. A region request covers
   the region's intersection with the extents: a region wholly
   outside them, or any region of a zero-extent layer, succeeds
   and returns no samples (`[R-GEO-02]`).
2. **Ordinals.** Compute the tile coordinates, in-tile ordinal,
   spatial ordinal s, and the disk ordinal of each needed tile — s
   interleaved; c · N + s per requested channel c planar
   (`[R-GEO-06]`).
3. **Index chain.** Steps 3 through 6 run once per needed entry.
   Verify crc_of_crc_array over the fetched CRC array and the
   segment CRC over the fetched segment containing the entry — the
   two fetches MAY run in parallel and their verifications MAY be
   cached per §15.4's note (`[R-IDX-04]`).
4. **Entry.** Classify per §15.3 (`[R-IDX-03]`). A valid sentinel
   short-circuits steps 5 and 6 for that entry: every requested
   sample position of its tile reads as fill — the entry's
   channel's recorded fill in a planar layer; each carried
   channel's, in declared order, in an interleaved layer —
   bit-exactly and with no payload I/O (`[R-TYP-06]`,
   `[R-TYP-08]`). A malformed entry rejects the tile; a rejected
   tile's read reports failure, and fill is never a failure
   fallback (`[R-CNF-09]`).
5. **Payload.** Fetch [offset, offset + length) and verify the
   entry's crc over the stored bytes before decoding
   (`[R-CNT-20]`).
6. **Decode.** Apply the codec, then the filter's inverse (§17.1,
   `[R-COD-08]`); the decoded payload's length is exactly the
   decoded size (`[R-SER-07]`).
7. **Extract.** Locate each requested value by §14's offset
   arithmetic; padding positions are never returned
   (`[R-GEO-04]`).
8. **Return.** Return the requested values' bit patterns
   unaltered (`[R-MDL-02]`, `[R-TYP-04]`) — for every byte a
   conforming file can carry, the whole of this step
   (`[R-SER-08]` fixes what a reader returns for a byte a
   conforming file cannot carry). Where the request covered several
   entries — a region, or a planar layer's several channels —
   each rejected entry's failure is bounded to the positions that
   entry carries (§2.4): the reader MAY return the validating
   entries' values together with a per-entry report of the failed
   ones, or fail the request as a whole, but MUST NOT stand fill
   in for a rejected tile's positions (`[R-CNF-09]`). That
   bounding is a property of tile scope. A failure inside the same
   request that takes layer scope instead — step 3's index-chain
   failure (`[R-IDX-04]`) — bars the request's remaining entries
   and all further service from the layer; the bar is prospective,
   so values the reader has already returned under §19.2's timing
   stand (§2.4).
   `[R-RDR-04]`

> **Note — planar all-channel reads.** The entries for one spatial
> ordinal lie at disk ordinals c · N + s, spaced N · 20 region
> bytes apart; for N ≥ 2¹⁶ they are guaranteed to fall in
> different segments, each needing its own segment verification —
> the whole-CRC-array verification is shared across all of them.
> Channel-subset reads verify only the segments they touch.

> **Note — region reads.** A rectangular-region read is this
> algorithm applied per covered tile. Readers MAY coalesce the
> payload fetches of ordinal-adjacent stored tiles; a slab
> declaration guarantees contiguity only for stored tiles within
> one run (§16.2) — across runs, and across planar channel
> blocks, placement is unconstrained (`[R-SLB-05]`), so
> coalescing is always driven by the entries' explicit offsets
> and lengths. Nothing obliges coalescing, and sentinel tiles
> cost no I/O wherever they fall.

### 20. Writing and Updating

Every conforming mutation of a file is a commit or a whole-file
rewrite (`[R-LIF-01]`), by one writer at a time (`[R-LIF-05]`).
This section defines the writer tiers and their procedures; like
§19, it consolidates — each step cites the rule whose outcome
governs it.

#### 20.1 Writer tiers

- **creator** — emits a complete file in one commit, its first
  generation: the minimal conforming writer.
- **appender** — extends an existing file by commits (§9.2):
  adding layers or records, superseding tiles, growing extents,
  amending metadata.
- **rewriter** — writes a new file from an existing one under a new
  identity (§20.5), undertaking to preserve it as §20.4 provides, and
  carrying structures forward, re-creating some, or dropping some;
  compaction, which carries every structure forward
  and changes nothing but placement, is the rewrite that reclaims
  slack.

The tiers are shapes of operation and §2.3's classes are the
obligations they carry. A creator is a writer and nothing more: it
emits only conforming files (`[R-CNF-05]`). An appender and a
rewriter are updaters: each satisfies every writer requirement for
the bytes it produces and the preservation obligations of §20.4 for
what it carries forward (`[R-CNF-06]`), and is a reader of every
structure it processes (`[R-CNF-11]`) — a violation latent in a
structure it carries forward unmodified travels with it, seen or
unseen, and certifying the whole file is a verifier's office (§9.7).
The appender's commit extends its input under the input's file_id;
the rewriter's output is a new file under a fresh one (`[R-LIF-01]`).
Every obligation of §20.3 through §20.5 attaches to an operation and
binds whichever writer performs it. A writer that extends an input
file is an appender and an updater, whatever it decodes: the file it
leaves holds every byte of its input. A writer of a new file from an
existing one takes one of two positions, and the choice is its own.
As a **rewriter** it undertakes to preserve its input: §20.4's table
for every record, the unknown ignore-lane bits (`[R-CNT-08]`), and
§20.5 whole; in return it answers for what it carries forward
unmodified only to `[R-WRT-09]`'s depth, a latent violation
travelling with it. As a **creator** it undertakes nothing toward its
input, whatever it read: §20.2 binds it, it writes flags = 0, and it
answers for every byte of its output (`[R-CNF-05]`), bytes it copied
from another file included. `[R-WRT-01]`

#### 20.2 Creation

A creator MUST follow `[R-LIF-02]`'s creation path: the front
signature block; each layer's stored tiles, tile-index region, and
any record extents, in any order satisfying §5.2's coverage
classes (`[R-CNT-02]`, `[R-CNT-03]`) and every declared layout
invariant (`[R-SLB-01]`, `[R-SLB-03]`) — placement is otherwise
free (`[R-SLB-05]`); then the complete directory and its CRC; then
the barrier, the pad, the trailer with a fresh nonzero file_id
(§9.3), and the barrier that makes the trailer durable
(`[R-LIF-02]` steps 4–6 — both barriers, not one).
Content obligations travel with the structures:
fill-encoded edge padding (`[R-SER-05]`), boolean byte values
(`[R-SER-08]`), and gaps zeroed as `[R-CNT-03]` advises. `[R-WRT-02]`

#### 20.3 The append procedure

An updater's verification depth follows reliance
(`[R-RDR-02]`'s principle, which §2.3 extends to updaters as
readers of what they process, `[R-CNF-11]`): the trailer and the
full directory always — re-emission (§20.4) relies on every
directory byte — plus §19.3's layer validation for every layer
whose record, index, or extents the commit modifies, and the
§19.4 index chain for every segment whose entries the commit
reuses (`[R-IDX-04]`). Structures the commit neither modifies nor
relies on impose no further obligation. `[R-WRT-03]`

An appender MUST, in order:

1. **Establish F.** Validate the trailer at the physical end of
   the file (`[R-LIF-04]`). On failure the file is torn: no
   append; recovery (§9.6) is a deliberate, separate operation,
   and an appender resuming from re-verified recovery output
   takes F from that output, then truncates to F or overwrites
   from it per `[R-LIF-04]` — in which case F, never the physical
   end, anchors every step below.
2. **Open.** Perform §19.1's open (`[R-RDR-01]`) — the appender is
   a reader here. A violation the open establishes bars the commits
   its outcome bars and no others: reject-file bars every commit, and
   reject-layer bars a commit that modifies that layer. The open
   establishes no tile-scope violation — it consumes the trailer and
   directory only (`[R-RDR-01]`) — and a malformed index entry an
   appender meets while re-emitting a region is carried forward
   byte-identically at its disk-ordinal position under step 4, not
   repaired to a sentinel. Against any other structure the appender
   carries forward, it MUST NOT repair the defect — `[R-LIF-01]`
   freezes the committed prefix — and MUST NOT drop the record save
   where §20.4 licenses the drop.
   Reproducing a structure's bytes unchanged is not
   authoring them: an appender satisfies its writer obligations for
   the bytes it produces, and a violation latent in a structure it
   carries forward unmodified travels with that structure (§20.1,
   `[R-WRT-01]`) — which is as true of an index entry copied to its
   disk-ordinal position as of a record re-emitted byte-identically
   (`[R-WRT-05]`), and validating either to `[R-WRT-03]`'s depth is
   not authoring it. Certifying the whole file is a
   verifier's office. An appender that carries a violation forward SHOULD
   report it, and a caller that is not told cannot know the file it
   extended was already damaged.
3. **Validate what the commit touches**, per `[R-WRT-03]`.
4. **Write payloads and indexes** (`[R-LIF-02]` steps 1–2):
   writing begins at exactly F; new stored tiles and record
   extents follow, each byte classified under §5.2. Every layer
   whose stored-tile set or index content this commit changes has
   its tile-index region re-emitted in full — entry_count entries
   plus the segment CRC array — necessarily at a new placement
   (`[R-LIF-01]`), with entries for tiles this commit stores or
   supersedes written to their new state, entries for tiles that
   become unstored written as the sentinel, entries new to this
   generation (every entry of a layer this commit adds or re-declares,
   and the tiles a grown extent or an appended channel adds to the
   addressed set) emitted per §15, and every other entry byte-identical at its
   disk-ordinal position (a growth renumbers ordinals wherever
   `[R-GEO-06]` moves them, and nothing else this step permits moves
   one). A layer the new state leaves addressing no tile has no region
   to re-emit and the slot (0, 0) (§15.4, `[R-CNT-17]`). A layer
   whose record alone changes keeps its extent slot, pointing at
   the existing region, as does a layer the commit leaves
   untouched (`[R-WRT-05]`); relocating a live index region is
   a rewriter's operation (§20.5, `[R-WRT-07]`), not an
   appender's.

   A layer that stores a tile **in the generation this commit
   supersedes** keeps its declarations, with these exceptions and no
   other: its name, and its dimension and channel names, MAY change;
   a dimension extent MAY grow, and MUST NOT shrink; a planar layer's
   channel
   list MAY be extended at its end or shortened from its end, but not
   both in one commit; and a slab or alignment declaration MAY be
   declared, changed or cleared as this step provides below.
   A commit MAY make several of these changes at once, an extension
   and a shortening of one channel list excepted: a commit that
   shortens a planar layer's channel list appends no channel to it and
   one that extends it removes none, whatever the counts, so replacing
   the last channel, or any run of channels at the end, is two commits
   or a rewrite. Every other declaration is fixed for as
   long as the layer stores a tile: the layout, the linearization and
   the index encoding, the codec and the filter, the rank and the
   dimension order, every tile extent, every channel's type and fill,
   an interleaved layer's channel list (its names aside), and the
   position of every planar channel the new state keeps. A commit MUST
   NOT change one of
   these; the change is a new layer, or a rewrite that re-declares
   it under a fresh file_id (`[R-LIF-01]`, §20.5). This bar binds the commit as
   an actor: no file is nonconforming by virtue of its violation, and
   no register row records the violation itself, the register
   enumerating file-conformance violations (§21.1) and the bar stating
   no condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`);
   a file such a commit leaves can be nonconforming on its own terms,
   as the paragraph below sets out. Between them the two lists
   reach every declaration field of §7.4, and where a field is on
   both sides — a planar layer's channel list, an interleaved layer's
   channel list — the permitted side states the
   whole of what a commit MAY do to it;
   entry_count and crc_of_crc_array follow the commit, the record's
   extent slot with them (§7.2), and a layer's sub-records are §20.4's
   subject whether or not the layer stores a tile. The tense is the
   prior generation's (§3.1 defines *stored* against a generation),
   so a commit does not earn an empty layer's freedom by emptying the
   layer as it re-declares it: a layer that stored a tile keeps its
   declarations through the commit that empties it. The bar binds a
   layer the commit keeps and nothing else: a commit MAY drop the layer
   (§20.4) and add a new one under its name and other declarations,
   the new layer being new whatever bytes its entries address, the
   dropped layer's former extents included, §5.2's partition being
   over the new state alone. What the bar removes is a re-declaration
   carried as the same layer over the tiles it stored.
   A layer that stores no tile in the generation this commit
   supersedes MAY be re-declared freely, subject to every rule its
   new declarations are subject to, which is what schema-first
   creation needs (§11.1).

   The line is drawn where a stored tile's meaning is fixed. The
   fixed declarations are the ones §14 reads a stored tile under —
   its value sequence, its byte layout, the fill its padding
   positions hold (§14.5) — the ones §11.4 assigns its ordinal and
   its values' coordinates by, as a rule rather than as the numbers
   the rule yields, the one §15 gives the layer's index region its
   shape by, and the ones §17 produces its stored bytes from, its
   filter and its codec. Under new ones the same bytes would denote values,
   coordinates or padding the writer did not store, with every
   checksum in §8 certifying the result and, but for a stored tile's
   decoded size, a padding position or pad bit, or a boolean byte the
   register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails
   outright, or a codec's framing check that precedes it, under a
   changed codec or filter (T17, T24, T25), no check any
   actor owes able to see it (§21.7). The permitted changes
   touch none of that: a name enters no map this specification
   defines, and a commit MAY change several names at once, two
   swapped included, the dimension order and the channel order being
   positional and fixed; a grown extent adds
   positions that held their channel's fill (§14.5), and fill is a
   legal sample value, and where the growth moves an ordinal it
   moves it under the same rule, the re-emission clause above
   following the tile; an appended planar channel adds tiles at
   ordinals after every existing one, a disk ordinal being c · N + s
   with N the spatial-tile count; a channel removed from the end
   takes only its own tiles out of the addressed set, and a tile the
   new state does not address carries no obligation; a slab or
   alignment declaration governs placement (§16), not a value, its
   coordinate or its padding. What the line
   gives up is stated rather than carved around: a shrink, a fill
   change, a re-type, a re-tiling, a change to the dimension order,
   a change of rank, layout, linearization, index encoding, codec or
   filter, any change to an interleaved layer's channel list but a
   channel's name, a planar channel inserted or removed anywhere but
   the end of the list, and a planar channel list both extended and
   shortened in one commit are rewrites even where a particular file
   would survive them in place, because deciding which files would is
   the edge this list exists to remove.

   A permitted change holds provided the declarations and geometry
   it produces stay within every bound they are subject to:
   `[R-COD-07]`'s lz4 decoded-size cap (L44, the largest channel
   plane governing in a planar layer), which an empty layer escapes
   only because that cap is quantified over addressed tiles;
   `[R-ENC-04]`'s 2⁶³ − 1 ceiling on every quantity it designates,
   C · N among them; `[R-GEO-01]`'s floor of one channel; and the name
   rules of §4.6 and `[R-ENC-15]`. These bounds are not offered as
   exhaustive: a permitted change holds exactly where the declarations
   it produces satisfy every rule they are subject to, and which
   changes are permitted is what this step's list of exceptions
   above states. A channel
   removed from the end
   leaves its stored tiles' extents as slack (§5.2) and changes the
   layer's index content, the entries the removed channel held ceasing
   to denote its tiles, so the region is re-emitted under the clause
   above whether or not entry_count changes with it (`[R-CNT-17]`) and
   whether or not a retained ordinal moves;
   a writer SHOULD instead produce a new file wherever a commit would
   strand a large share of a layer's stored bytes, a shortening that
   removes most of them included, and always where a commit would
   supersede every one of them, which duplicates the layer rather
   than editing it. Unstoring a tile (§15.2) is how a
   commit discards data in place; discarding is the caller's
   operation and this specification does not bar it. A file is
   charged for by its length wherever storage is metered, so slack
   that is not data the caller chose to discard is paid for and never
   read. Extents this commit supersedes become slack (`[R-CNT-21]`);
   on a layer this commit modifies, a slab declaration declared,
   changed or kept has its invariants satisfied over every run of the
   new state, the runs this commit adds included, or is cleared
   (`[R-SLB-03]`, `[R-SLB-04]`, `[R-CNF-05]`), and an aligned layer's
   stored tiles, every one the new state holds and those this commit
   adds included, satisfy its invariant or the declaration is cleared
   (`[R-SLB-01]`, `[R-CNF-05]`).
5. **Re-emit the directory** per §20.4, followed by its CRC
   (`[R-LIF-02]` step 3).
6. **Commit** (`[R-LIF-02]` steps 4–6): barrier; pad;
   trailer with the same file_id, committed_file_length equal to
   the new end — necessarily at least 128 above the F step 1
   established, this commit having appended at least a directory and
   a trailer (`[R-LIF-02]`) — unknown ignore-lane flag bits copied
   forward and no other set (`[R-CNT-08]`), and version_minor per
   `[R-CNT-26]`;
   barrier. `[R-WRT-04]`

> **Note.** A commit's cost is dominated by its index, not its data:
> any change to a layer's stored-tile set re-emits that layer's whole
> tile-index region, so editing one sample of a 10⁶-tile layer
> appends about 20 MB of index and leaves as much slack. Writers doing
> many small updates SHOULD batch them into one commit, and compact
> (§20.5) when slack grows — a verifier whose walk completes reports
> its total (§9.7).

> **Example.** Superseding one 100,000-byte stored tile of a
> 32-tile interleaved layer appends: the new payload (100,000
> bytes), the layer's full new index region (32 · 20 + 4 = 644
> bytes — one entry re-pointed, 31 byte-identical), the new
> directory (every record byte-identical except the modified
> layer's), the pad, and the 64-byte trailer. The prior index
> region and the superseded payload become slack, reclaimable
> only by a rewrite (§20.5).

> **Example — the three shapes a commit takes.** Regions, not offsets;
> ▓ marks what the commit turned to slack.
>
> **(a) A new layer.** Nothing existing is rewritten.
>
> ```
> before │front│ A: tiles+index │ dir₁│pad│tr₁│
> after  │front│ A: tiles+index │▓▓▓▓▓▓▓▓▓▓▓▓▓│ B: tiles+index │ dir₂│pad│tr₂│
>               └── untouched ──┘└was dir₁…tr₁┘
> ```
>
> A's record is carried into dir₂ byte-identically, extent slot and
> all, so it still addresses A's original index. The slack is the old
> directory, pad and trailer — sized by the file's *layer count*, never
> by any layer's data. This is the shape a tool that derives layers
> takes: decimation, pyramid levels, an added mask.
>
> **(b) Tiles added to an existing layer.** That layer's index is
> re-emitted whole; a commit that supersedes stored tiles takes the
> same shape, hatching the superseded payloads as well, and so does a re-declaration
> of an empty layer that changes its index content, with no tile
> written (see (c)).
>
> ```
> before │front│ tiles │ index │ dir₁│pad│tr₁│
> after  │front│ tiles │▓index▓│▓▓▓▓▓▓▓▓▓▓▓▓▓│ +tiles │ index′ │ dir₂│pad│tr₂│
>                       └ old ─┘                       └───────┘ every entry, re-emitted
> ```
>
> The whole region moves because it is addressed by one extent slot, so
> a single changed entry costs its whole length — the cost this
> section's note above quantifies. Superseded payloads become slack
> too; retained ones do not move.
>
> **(c) A change confined to the directory** — clearing a slab
> declaration, renaming a layer, or dropping a layer or another
> PE = 0 record where §20.4 licenses the drop, any extent it owned, a
> dropped layer's tiles, index region and sub-records' extents
> included, becoming slack, a
> run the figure below does not draw. Only the directory is re-emitted. A
> change to any fixed declaration of a layer that **stored** a tile in
> the generation the commit supersedes — a fill value, a type, a tile
> extent — is not an appender's operation at all (step 4): it would
> reinterpret or invalidate every stored tile it reaches. A layer that
> stored no tile in the
> generation the commit supersedes is re-declared freely, subject to
> every rule its new declarations are subject to, which is the same step's
> permission — a layer the commit itself empties does not qualify. A
> re-declaration that changes the layer's index content takes shape (b)
> with no tile written, the region re-emitted whole at a new placement
> (step 4, `[R-WRT-04]`), unless the new declarations address no tile:
> then there is no region to emit (`[R-CNT-17]`), the extent slot becomes
> (0, 0), the old region falls to slack, and the commit is shape (c). A
> re-declaration that leaves the index content unchanged is shape (c)
> too. Editing
> user metadata is not shape (c):
> its document lives in an extent (`[R-CNT-25]`), so a new extent is
> appended and the old one becomes slack, as in (b).
>
> ```
> before │front│ A: tiles+index │ dir₁│pad│tr₁│
> after  │front│ A: tiles+index │▓▓▓▓▓▓▓▓▓▓▓▓▓│ dir₂│pad│tr₂│
> ```
>
> In every shape the file grows and no committed byte changes, which is
> what lets a reader hold a generation open while a writer commits
> (§9.5) and a cache keep every range it has already fetched (§9.3).

#### 20.4 Re-emission and preservation

In the new complete directory, an updater MUST re-emit
byte-identically — header, inline payload, and extent slot — every
record it retains and does not logically modify, whether or not it
implements the record's type; a record it modifies is new output
under its writer obligations (`[R-CNF-05]`). `[R-WRT-05]`

Persistence governs every record type; only the authoritative source
of the flags differs. For a type §7.3 registers, the registry's fixed
flags govern rather than the stored ones (`[R-CNT-22]`) — the layer
record carries PE = 0 and is dropped under the table's last row, the
user-metadata record PE = 1, a top-level one never dropped and a
sub-record only with the layer that carries it; implementing a record's type
confers understanding of it, and the permission to drop it is the
bit's alone. For a type the updater implements that this specification does not
register, the definition it implements the type from supplies the
flags, and the stored bits never do (`[R-CNT-22]`, §10.3). For a type
the updater does not implement, the
stored flags are authoritative (§7.3, `[R-CNT-15]`; MU = 1 with
PE = 0 is read as PE = 1, `[R-CNT-12]`). The table states what an
updater owes a record it does not logically modify, read under
whichever flags govern it. Its MU = 1 row reaches only a type the
updater does not implement — an updater implements both registered
types and understands an unregistered type it implements from its
definition, modifying their records as §20.3 and that definition
provide — so for an implemented type only the PE bit bites:

| Governing flags | Updater obligation |
|---|---|
| MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the record governs. At layer scope an unknown critical record blocks modification of that layer, its drop included, leaving other layers editable (`[R-CNT-18]`). At file scope no commit is available at all: the updater is a reader of the file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file — the same treatment §6.3 gives an unknown incompat-lane bit. At either scope a rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground: such a type can define references this specification does not (§7.2), so its bytes cannot be safely relocated. |
| MU = 0, PE = 1 | Retain byte-identical, extent content unmodified. |
| MU = 0, PE = 0 | Retain byte-identical, or drop it — its extent becoming slack. The licence is the bit's own: whoever fixed PE = 0 for the record, the writer that stored it or the definition that governs it, declined preservation across edits, so an appender MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included — and a rewriter MAY drop it in any rewrite. An updater that drops such a record SHOULD report the loss; unreported, application state disappears with no diagnostic. |

A commit MAY therefore drop a layer record, and the drop takes the
layer whole: a sub-record's flags govern it within a layer the updater
keeps, so a dropped layer's sub-records and their extents go with it
whatever their PE bits. One sub-record blocks the drop, a sub-record
of a type the updater does not implement with MU = 1, the drop being
a modification of the scope it governs (the table's first row). A
commit never removes a user-metadata record from a scope it keeps: a
top-level one from the file, or a sub-record from a layer the commit
retains. Dropping a layer by commit
strands its stored tiles, its tile-index region and its sub-records'
extents as slack (§5.2), which
only a rewrite reclaims, so the file is no smaller than before and
the bytes remain in it (§23.1): a writer SHOULD instead rewrite where
a drop would strand a large share of the file's stored bytes, a
rewrite that drops the layer (§20.5) reclaiming what the commit would
strand, and an updater that drops a layer SHOULD report the loss, as
the table says of any record dropped. A dropped layer's name is free to the same commit and
to any later one (§20.3 step 4, §19.1).

An updater MUST NOT re-encode a record whose type it does not
implement, and MUST NOT modify one except by relocating its
extent and re-pointing its slot under §20.5 — the operation the
no-embedded-offsets rule (§7.2) makes safe for MU = 0 records.
`[R-WRT-08]`

> **Rationale.** Complete-directory commits make re-emission the
> preservation mechanism; byte-identity makes preservation
> testable — the directory a commit emits differs from the one it
> supersedes exactly by the records modified, added, or dropped
> (as a multiset: record order carries no meaning, `[R-CNT-14]`) —
> and forecloses re-encode drift: a re-serializer that renormalized
> a name would change the name's identity (`[R-ENC-13]`). Put that
> way the claim is a commit's own and holds whether or not an
> observer can pair the two directories. It cannot, from the
> format: the live state names one generation, and two trailers of
> one file_id are ordered by committed_file_length without being
> counted, so nothing in either says how many commits separate
> them. Adjacency is a fact about a file's history, which §9.7 does
> not reconstruct; a tool that wants the pairing enumerates commit
> states from the physical file (§9.6), and gets only the ones that
> file still carries.

#### 20.5 Rewriting

A rewriter's output is a new file under a fresh file_id, built from
the structures reachable from the input's live trailer — the live
committed state (§7.2) — and carrying no slack. Each structure of the
input is carried forward verbatim, re-created as new output, or
dropped, under the rule for what is done to it, and the output MAY
add what a creator could. This text names three rewrites:
**compaction**, which carries every structure forward and changes
nothing but placement, and is the rewrite that reclaims slack;
**dropping** a layer or another record §20.4's table licenses
dropping, which a commit does by omitting the record and stranding
what it addressed (§20.4) and a rewrite does reclaiming it;
and **re-declaring** a layer that stores a tile in the input, the
rewrite §20.3 step 4 reserves for a change to a fixed declaration. A
rewrite MAY do several of these at once, dropping one layer,
re-declaring another and carrying the rest forward, and is compaction
only where it does nothing but carry. A rewriter satisfies every
writer requirement for the bytes it produces (`[R-CNF-06]`), and a
violation latent in a structure it carries forward verbatim travels
into its output (`[R-WRT-01]`) — its verification depth over what it
carries is `[R-WRT-09]`'s and reaches no decoded content, and what it
re-creates it decodes as a reader (`[R-CNF-11]`) and writes as a
creator (§20.2). Given a conforming input, an output that carries
forward, re-creates and drops as this section provides is a
conforming file. A rewriter MUST refuse to rewrite when any check
`[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a
violation it has detected: it can neither re-emit the structure
corrected (`[R-WRT-05]`), nor keep it and call the output clean.
Dropping is the one disposal that answers, and only where §20.4's
table licenses it: a record dropped, a layer with its sub-records,
its index region and stored tiles among them, is not in the output, so the output
carries no violation and the prohibition — which bites on what the
output carries — is satisfied. Where the table does not license a
drop the rewriter MUST refuse. It MUST mint a fresh file_id for the
output — a new draw under §9.3's randomness advice, not merely a value
compared against the input's: a rewritten file is a whole-file
rewrite under a new file_id by definition (`[R-LIF-01]`), and
reusing the input's would break the (file_id, range) cache contract
of `[R-LIF-03]`, since relocation puts different bytes at the same
ranges. The fresh file_id is the whole of that mechanism: it is
what makes the output a different file rather than a later state of
its input, and `[R-LIF-03]` reaches that verdict on file_id alone,
before any comparison of committed_file_length. What is lost is
smaller and worth naming: nothing in the output's trailer records
that it is a first committed state — no field counts commits — so a
rewritten file and a file appended to a hundred times are
indistinguishable by their live trailers alone. A rewriter MUST follow
`[R-LIF-02]`'s **creation path**, as §20.2 obliges a creator: the
output has no prior trailer, which is the case that path states,
and `[R-WRT-01]` already has a rewriter satisfying every writer
requirement for the bytes it produces. The pad of step 5 and the
barriers of steps 4 and 6 — both, not one — are owed here as they
are of a creator. That a rewrite is not a commit (`[R-LIF-01]`)
fixes what the output *is*, not which rules govern the writing of
it.

The output
trailer MUST copy the input's unknown ignore-lane flag bits forward
and set no other, in place of the flags = 0 §6.3 requires of a file
created under this text (`[R-CNT-08]`). Where the output carries a feature a later minor
defines and this rewriter does not — on a conforming input a carried
ignore-lane bit (§6.3) or an unrecognized `tarn.` key in a record it
never decoded (§18.3), the two of §10.1's four vehicles §21.6 makes
conforming, the other two reaching such a file only as values this
text still registers as reserved-range violations: F36 and L25 for a
record type, and one row for each of the other seven spaces §10.2
tabulates (L31, L33, L34, L36, L43, L45, R1) —
the output's version_minor SHOULD be at least the input's: a rewriter cannot know which minor version defined a
feature it does not implement, and a lower minor understates the
file's feature floor to tooling, the mirror of the overstatement
`[R-CNT-26]` names. Otherwise version_minor follows `[R-CNT-26]`'s
floor. A rewriter MUST refuse to rewrite a file carrying any record
whose type it does not implement with MU = 1: such a type can
define references this specification does not (§7.2), so its
bytes cannot be safely relocated. `[R-WRT-06]`

A rewriter MUST preserve the content of every structure it carries
forward, and preserves no placement — placement is not among the
things it carries forward, and it is free to place structures
anywhere §5.2 admits and every declared layout invariant permits
(`[R-SLB-01]`, `[R-SLB-03]`): every carried stored tile's bytes
verbatim — each index entry's crc is unchanged — and every retained
record per §20.4, except that relocation re-points
extent slots, regenerates each tile-index region any of whose stored
extents the output relocates (entry
offsets new; entry lengths, entry crcs, and sentinel entries
unchanged; segment CRCs recomputed over the entries as
re-emitted), and updates the layer-record fields covering a
regenerated region (crc_of_crc_array). A layer the rewrite
re-creates is new output: its record, its tile-index region and its
stored tiles are written under §20.2's rules from content the
rewriter decoded (§19.3, §19.4), and nothing of the input's copy of
that layer is carried forward.

Regenerating a region means classifying every entry in it: a sentinel
is re-emitted unchanged, and every other entry is re-pointed to where
its stored extent now lies. An entry §15.3 classifies reject-tile on a
structural ground is neither — `[R-IDX-03]` gives it no stored extent
for a re-pointing to target — so regenerating the region cannot
proceed without meeting it, and the violation is thereafter one the
rewriter has detected. `[R-WRT-06]` then leaves it two disposals,
since it can neither reproduce the entry nor invent a replacement:
drop the layer, which §20.4's table licenses and whose loss the
rewriter SHOULD report as that table says, or refuse. That `[R-WRT-09]`'s checks reach the index
chain and the checksum over each extent it copies rather than an
entry's own value domain bounds how far a rewriter goes looking,
not what it owes on what regenerating the region has already put in
front of it.

No other record payload
carries a file offset: MU = 0 records by rule (§7.2), and an
MU = 1 type the rewriter does not implement never reaches this
step (`[R-WRT-06]`). An MU = 1 type it *does* implement is the
remaining case, and §7.2 admits it — such a type carries further
references where this specification or registry review defines
them — so a rewriter implementing one relocates whatever that
registration defines, on the same terms as the tile index. The
reference array of every layer the output carries forward MUST equal
the live generation's bit for bit (`[R-MDL-02]`): a rewrite changes
where bytes live, never what a carried layer denotes, and what a
re-created layer denotes is the rewriter's to declare. `[R-WRT-07]`

> **Example — what compaction reclaims.** Regions, not offsets; ▓ marks
> slack.
>
> ```
> input  │front│ A │▓▓▓▓│ B │▓▓│ A: index │▓▓│ B: index │▓▓▓│ dir │pad│ tr │
>                                                  file_id = X
>
> output │front│ A │ B │ A: index │ B: index′ │ dir │pad│ tr │
>                                                  file_id = Y
> ```
>
> Every stored tile's bytes survive byte-for-byte, as does every
> record extent but a tile-index region any of whose stored extents
> moved — itself a record extent (§5.2), and the one kind this
> operation regenerates rather than copies, since its entries carry
> the offsets that moved. The reference arrays are identical; extent
> slots are re-pointed and each index region any of whose stored
> extents moved is regenerated — the ′ marks B's (`[R-WRT-07]`). In
> this placement A's stored extents happen not to move, so A's index
> is copied and only its slot re-pointed; under a placement that moved
> them it would be regenerated too, placement being the rewriter's
> to choose.
> Placement is what changes, which is why the output is a different
> file rather than a later generation of the same one. The fresh
> file_id is the mechanism, not bookkeeping: a
> cache keyed (file_id, range) is sound precisely because ranges never
> change beneath a file_id (§9.3), and a rewrite is the one operation
> that changes what a range holds. Reusing the input's identifier would serve
> the input's bytes for the output's ranges.
>
> A rewrite is the only operation that reclaims slack; truncation past F
> (`[R-LIF-04]`) and recovery to an earlier commit boundary
> (`[R-LIF-06]`) also shorten a file, but neither reclaims any. Slack
> accumulates a directory, a pad and a trailer per commit, the gaps an
> alignment or slab declaration leaves before the structures it places
> (§16), a whole index region for each layer whose stored-tile set or
> index content a commit changed, and every payload and every other
> record extent a commit supersedes, unstores or drops, with every
> tile a shortening strands (§20.3, §23.1); a verifier
> whose walk completes reports the total (§9.7), and that total is
> what tells an operator when to run this.

A rewriter's verification depth over what it carries follows
reliance (`[R-WRT-03]`): it relies structurally on every
structure it copies, so it MUST verify each link of the chain —
the open (§19.1), each retained layer's record (§19.3) and full
index chain (`[R-IDX-04]`), and the checksum §8.1 states over each
extent it copies, every stored tile's entry crc among them — before
emitting that structure's bytes. The duty follows what the rewriter
carries and not where it places it: an extent the output leaves at
its input offset owes the same check as one it relocates. What it
re-creates it decodes as a reader first, owing every check §19.3 and
§19.4 place at that use (`[R-CNF-11]`).
`[R-WRT-09]`

> **Note.** A rewrite is the only true removal: logical deletion
> supersedes bytes but leaves them in the file as slack
> (`[R-CNT-21]`) — a privacy consideration (§23).

### 21. Error-Handling Register and Limits

#### 21.1 How to read the register

The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates
every detectable file-conformance violation this specification names: each row is one
malformed condition, with the outcome class its scope determines
(§2.4) — except where a rule assigns one expressly, as `[R-CNT-25]`'s
quarantine does for every way a §21.5 row makes the document
unreadable and `[R-MTA-09]` for the frame constraints R4 registers,
whatever the containing scope —
the actor obliged to detect it (`[R-CNF-04]`, `[R-CNF-11]`),
the point by which detection is due (§19.2), and the requirement that
defines it. A Governing rule cell names that requirement first; any
identifiers following it in parentheses are further rules the
condition reads, a finding aid and not the whole of them, or the
section stating what it reads where no
requirement identifier does, a value set (L31) or a registered
type's scope (L26), cited without brackets to keep them distinct
from the governing one. Its **completeness is normative** — a
*detectable* file-conformance violation this specification names and
the register omits is a defect in this document, detectability being the gate
`[R-CNF-07]` already applies and §21.7 states the test for: a
condition is detectable exactly where some file exhibiting it is
separated from every file that does not by some check this
specification obliges a reader or a verifier to perform, not
necessarily the same check for each such file
— but each row *restates* its governing rule, and where a
row and the rule it cites diverge, **the rule governs**. Conditions
attach to the finest structure they damage, and the outcome follows
from that scope — subject to the same exception stated above, a rule
that assigns an outcome expressly — never from the severity of the
corruption. Some
rows are strict specializations of others: where every file
exhibiting one row's condition — at a given instance of it, where the
row enumerates several — necessarily exhibits another's, the file is
recorded against the narrower row, whose detector and detection point
are the ones that apply. F1's front-block instance of F6 and its
trailer-magic instance of F8, F35 of F36, L24 of L25, F21 of F22 and
L10 of L11 stand in that relation; the property decides any pair and
this list is not offered as closed. Rows that merely overlap, each
reachable without the other, do not stand in it. The subsections after §21.5 are not
part of the register and carry no rows: neither this completeness
clause nor the instance arithmetic below reaches §21.6's defined
non-violations, §21.7's test for what no check detects, or
§21.9's limits. §21.6's entries restate their governing rules on
the same terms a row does, each rule its Rule cell lists governing
the part of the entry it states and none first among them, and where
such an entry and a rule it cites diverge, the rule governs there
too.

The **Instances** column enumerates what a conformance corpus builds
for that row (§21.8): the row is the unit a vector is attributed to
(`[R-VEC-02]`), and each instance is one distinguishable file, covered
by at least one vector (`[R-VEC-03]`). An instance names a field the
condition ranges over, a
container it can occur in, one of several alternatives the condition
text states, or any combination of the three — a condition applying
to two alternatives in two containers has four. What a cell
enumerates is the condition's own alternatives and containers: a row
whose check ranges over a family without the condition changing
shape states that range as a single instance (T24's *any codec*),
and one whose members give the condition materially different shapes
enumerates them (T15, T25). Two axes recur often enough to be stated rather than judged each
time. Where the quantity a condition derives varies by layout, the
layout formulas are materially different shapes and the cell
enumerates them. Where the condition compares two **magnitudes**
either of which can be the greater — a *differs from* or *does not
equal* — the two directions are likewise enumerated; where its own
text bounds the comparison in one direction — an *exceeds*, a
*larger than* — there is one. A comparison with no magnitude
ordering enumerates no direction: a stored checksum against a
computed one, or a byte pattern against a constant, is equal or it
is not, and *greater* names nothing. Nor does a field tested only
for being nonzero — an *A ≠ 0*, an *S ≠ 0* — which is a value test
and not a comparison of two quantities at all. Instances within a
cell are separated by semicolons, and a cell reading — is one
instance; the count is therefore mechanical once the cell is
written. One instance is one
*distinguishable* file: where a condition is a single predicate over
several fields — a sum against a bound, a combination of two flag
bits — the fields it reads are not instances, because no two files
could differ. Detection points name §19.2's reader tiers — open,
layer access, tile use, extent use — or *certification* for the rows
a verifier detects, which §19.2 places outside the reader tiers
entirely. For a row whose Detector is *verifier*, the outcome names
the scope at which the damage is recorded, not an obligation on any
reader: the governing rule states what a reader does, and for
several such rows it obliges the reader that serves the structure to
serve it unchanged (`[R-CNT-22]`, whose registered type keeps its
fixed semantics, F28 and L49; and `[R-MTA-05]`, whose unsorted
document readers process as they find it, F27 and L48), `[R-CNF-12]`'s
licence to reject the nonconforming file being untouched in each, as
it is for `[R-CNT-12]`'s reserved-flag rows (F26, L47), whose bits
readers ignore. `[R-SER-08]` is the one rule that goes the other way
for a value a reader returns: it resolves a nonconforming interleaved
boolean byte to a sample value rather than serving it through, which
`[R-TYP-04]` (§12.3) records as the one such case; `[R-CNT-12]`'s
reading of MU = 1 with PE = 0 as PE = 1 (F25, L46) resolves a flag
and returns no data.

#### 21.2 File-scope violations

Outcome: reject-file. 35 conditions. Which rows reach a file declaring
a format major other than 1 is decided by `[R-CNF-13]` (§2.3),
condition by condition. Deriving it there yields F8, F14, F6 and both
of F1's instances — each asserting an invariant `[R-CNT-24]` fixes in
every major — and no other row. F18 is not an exception but a case outside the
premise: version_major = 0 declares no major at all, so `[R-CNF-13]`'s
premise is unmet and `[R-CNT-07]` governs (§21.6).

| # | Condition | Instances | Detector | Detected | Governing rule |
|---|---|---|---|---|---|
| F1 | A signature constant is stored byte-reversed — never to be adapted as a foreign-endian TARN file; the front-block instance binds only a reader holding bytes [0, 16) resident (`[R-CNT-04]`), the trailer-magic instance every reader (`[R-CNT-06]`) | front signature block bytes [0,8); trailer magic at F-64 | reader | open | `[R-ENC-02]` (R-CNT-04, R-CNT-06) |
| F2 | A u64 offset, length, or count field holds a value above 2^63 - 1 | dir_offset; dir_length; committed_file_length; non-layer top-level record extent_offset; extent_length | reader | open | `[R-ENC-03]` (R-CNT-06, R-CNT-13) |
| F3 | A sum of a u64 offset and length taken from the file exceeds 2^63 - 1 although each field alone is in domain | dir_offset + dir_length; non-layer top-level record extent_offset + extent_length | reader | open | `[R-ENC-04]` (R-CNT-06, R-CNT-13) |
| F4 | Two layer records in the live directory carry byte-identical name fields, both obtainable within their records' inline_length (comparison is raw bytes, no normalization) | layer record name | reader | open | `[R-ENC-15]` (R-ENC-13) |
| F5 | File size is below the 128-byte minimum, so the front block, a directory at an offset of at least 16 and the trailer at a 64-aligned offset cannot all fit | F (physical file size); committed_file_length | reader | open | `[R-CNT-27]` (R-CNT-01, R-CNT-06) |
| F6 | The 16-byte front signature block is not byte-identical to the constant; the obligation binds a reader holding those bytes resident, and a reader that would have to fetch them MAY defer or omit the check (`[R-CNT-04]`); a verifier holds no such exemption (§2.3) | magic bytes [0,8); reserved bytes [8,16) | reader | open | `[R-CNT-04]` |
| F7 | A structure occupies bytes between the live directory's end and the live trailer | stored-tile extents; tile-index regions; record extents; sub-record extents | verifier | certification | `[R-CNT-05]` (R-CNT-02) |
| F8 | The 8 bytes at F-64 are not exactly the trailer magic 8A 4E 52 41 54 0D 0A 1A | trailer magic | reader | open | `[R-CNT-06]` |
| F9 | Trailer dir_offset is less than 16, pointing the directory into or before the front signature block | dir_offset | reader | open | `[R-CNT-06]` |
| F10 | Trailer dir_offset + dir_length exceeds F - 64, so the declared directory region runs into or past the live trailer | — | reader | open | `[R-CNT-06]` |
| F12 | Trailer file_id is 0 | file_id | reader | open | `[R-CNT-06]` |
| F13 | Trailer committed_file_length is not a multiple of 64, so the trailer does not begin at a 64-aligned offset | committed_file_length | reader | open | `[R-CNT-06]` (R-CNT-01) |
| F14 | The u32 at trailer offset 60 does not equal the CRC-32C of trailer bytes [0,60) | trailer CRC | reader | open | `[R-CNT-06]` (R-CNT-20, R-ENC-09) |
| F15 | The 12 reserved bytes at trailer offset 48 are not all zero | trailer reserved [48,60) | reader | open | `[R-CNT-06]` (R-CNT-24) |
| F16 | Trailer dir_length is less than 4, too small to hold the directory region's terminal CRC-32C | dir_length | reader | open | `[R-CNT-06]` (R-ENC-07) |
| F17 | Trailer committed_file_length does not equal the transport-authoritative file size (physical file not truncated or extended to it) | committed_file_length, physical file shorter; committed_file_length, physical file longer | reader | open | `[R-CNT-06]` (R-LIF-04, R-CNT-10) |
| F18 | Trailer version_major is 0, which declares no major at all | version_major | reader | open | `[R-CNT-07]` |
| F19 | Any bit of the flags incompat lane (bits 0-15) is set; this text defines no flag bits, so every such bit is unimplemented | flags bits 0-15 | reader | open | `[R-CNT-08]` |
| F20 | The final 4 bytes of the directory region do not equal the CRC-32C of the preceding dir_length - 4 bytes (the raw record sequence) | directory region CRC | reader | open | `[R-CNT-11]` (R-CNT-20, R-ENC-10) |
| F21 | A top-level user-metadata record (type 0x0002) carries extent slot (0, 0) | — | reader | open | `[R-CNT-25]` |
| F22 | A top-level user-metadata record's extent_length is less than 5, too short to hold both a document and the terminal CRC-32C of its final 4 bytes | — | reader | open | `[R-CNT-25]` (R-ENC-07) |
| F23 | A top-level user-metadata record's inline_length is not 1; the encoding field is a fixed structure, not a growable one | inline_length 0, the encoding byte absent; inline_length ≥ 2 | reader | open | `[R-MTA-03]` (R-ENC-07) |
| F24 | A top-level record's type field is 0x0000; type 0 is invalid and is never treated as an unknown type | type | reader | open | `[R-CNT-12]` |
| F25 | A non-layer top-level record's flags carry MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0, a combination no writer emits | — | verifier | certification | `[R-CNT-12]` |
| F26 | Any of a non-layer top-level record's reserved flag bits 2-15 is set | flags bits 2-15 | verifier | certification | `[R-CNT-12]` |
| F27 | A file-scope user-metadata document has object members, at any nesting depth, not in ascending order of their keys' UTF-8 bytes; the document stays readable and readers process it unchanged | — | verifier | certification | `[R-MTA-05]` (R-CNF-05) |
| F28 | A non-layer top-level record of a type §7.3 registers carries a stored MU or PE bit differing from the value the registry fixes; readers apply the type's fixed semantics regardless | flags bit 0; flags bit 1 | verifier | certification | `[R-CNT-22]` (R-CNF-05) |
| F29 | A top-level record's 24-byte header or its inline payload extends past the end of the directory's record sequence (dir_offset + dir_length - 4), or bytes remain after the last complete record | record header; inline_length; trailing residue | reader | open | `[R-CNT-12]` (R-ENC-07) |
| F30 | A non-layer top-level record's extent slot has exactly one half zero (offset 0 with length != 0, or offset != 0 with length 0) | extent_offset; extent_length | reader | open | `[R-CNT-13]` |
| F31 | A non-layer top-level record's nonzero extent slot has extent_offset in 1-15, pointing into the front signature block | extent_offset | reader | open | `[R-CNT-13]` |
| F32 | A non-layer top-level record's extent_offset + extent_length exceeds F - 64, so the extent touches or passes the live trailer | — | reader | open | `[R-CNT-13]` |
| F33 | A byte of the live committed state is claimed by two structures that do not belong to the same layer — across two layers, a layer structure against another scope's structure, or two structures neither of which belongs to a layer; a claimant reaching the front signature block or the live trailer is instead caught by the bounds rows F9/F10, F30/F31/F32, L15/L16/L17 and T8/T9, each at its own tier — the half-zero rows F30 and L15 among them, since a record extent slot of (0, N) with N nonzero reaches the block through its zero offset and is theirs rather than F31's or L16's | stored-tile extents; tile-index regions; record extents; sub-record extents; directory region | verifier | certification | `[R-CNT-13]` (R-CNT-02, R-IDX-03) |
| F34 | The directory's top-level record sequence contains two or more user-metadata records (type 0x0002) | type | reader | open | `[R-CNT-14]` |
| F35 | A top-level record has a reserved-range type value (0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to 1 | — | reader | open | `[R-CNT-15]` |
| F36 | A top-level record carries a type value from the reserved range 0x0003-0x7FFF, which this specification has not assigned; emitting one is a violation whatever its MU bit | — | verifier | certification | `[R-CNT-15]` |

> **Note.** Row label F11 is struck, and the gap it leaves in this
> table is deliberate. A row label is retired on the model §2.2
> states for a withdrawn requirement identifier — never renumbered,
> never reused — so every label here denotes the condition it has
> always denoted (§24, `[R-VEC-02]`).

#### 21.3 Layer-scope violations

Outcome: reject-layer — the named layer is unusable, every other
layer unaffected. 49 conditions.

| # | Condition | Instances | Detector | Detected | Governing rule |
|---|---|---|---|---|---|
| L1 | A u64 offset, length, extent, or count field of a layer record holds a value above 2^63 - 1 | layer record extent_offset; layer record extent_length; sub-record extent_offset; sub-record extent_length; dimension extent Eᵢ; tile extent Tᵢ; entry_count; slab run length S | reader | layer access | `[R-ENC-03]` (R-CNT-13, R-CNT-23) |
| L2 | A declaration-derived sum or product of a layer exceeds 2^63 - 1 although every contributing field is in domain | layer record extent_offset + extent_length; sub-record extent_offset + extent_length; N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ; N·P; planar C·N (which dominates the max disk ordinal (C−1)·N + (N−1)); interleaved P·Q (which dominates V = P·C); planar numeric P·Bᶜ; entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 | reader | layer access | `[R-ENC-04]` (R-GEO-03, R-CNT-13, R-SER-02, R-SER-07) |
| L3 | A layer record's name bytes are not well-formed UTF-8 | — | reader | open | `[R-ENC-11]` |
| L4 | A dimension or channel entry's name bytes are not well-formed UTF-8 | dimension entry name; channel entry name | reader | layer access | `[R-ENC-11]` (R-CNT-23) |
| L5 | A layer record's name has length prefix 0 (empty name) | — | reader | open | `[R-ENC-12]` |
| L6 | A layer record's name contains a code point in U+0000-U+001F | — | reader | open | `[R-ENC-12]` |
| L7 | A dimension or channel entry's name has length prefix 0 (empty name) | dimension entry name; channel entry name | reader | layer access | `[R-ENC-12]` (R-CNT-23) |
| L8 | A dimension or channel entry's name contains a code point in U+0000-U+001F | dimension entry name; channel entry name | reader | layer access | `[R-ENC-12]` (R-CNT-23) |
| L9 | Two dimension entries, or two channel entries, of one layer carry byte-identical name fields | dimension entry name; channel entry name | reader | layer access | `[R-ENC-15]` (R-CNT-23) |
| L10 | A user-metadata sub-record of a layer record carries extent slot (0, 0) | — | reader | layer access | `[R-CNT-25]` |
| L11 | A user-metadata sub-record's extent_length is less than 5, too short to hold both a document and the terminal CRC-32C of its final 4 bytes | — | reader | layer access | `[R-CNT-25]` (R-ENC-07) |
| L12 | A user-metadata sub-record's inline_length is not 1; the encoding field is a fixed structure, not a growable one | inline_length 0, the encoding byte absent; inline_length ≥ 2 | reader | layer access | `[R-MTA-03]` (R-ENC-07) |
| L13 | A sub-record of a layer record has type 0x0000 | — | reader | layer access | `[R-CNT-12]` (R-CNT-18) |
| L14 | A sub-record's 24-byte header is truncated at the layer record's inline payload end, its inline_length runs past that end, or bytes remain after the last complete sub-record | sub-record header; sub-record inline_length; trailing residue | reader | layer access | `[R-CNT-12]` (R-CNT-18, R-ENC-07) |
| L15 | A layer record's or sub-record's extent slot has exactly one of extent_offset and extent_length zero | layer record extent_offset; layer record extent_length; sub-record extent_offset; sub-record extent_length | reader | layer access | `[R-CNT-13]` |
| L16 | A layer record's or sub-record's nonzero extent slot has extent_offset in 1-15, pointing into the front signature block | layer record extent slot; sub-record extent slot | reader | layer access | `[R-CNT-13]` |
| L17 | A layer record's or sub-record's extent reaches the live trailer or beyond: extent_offset + extent_length > F - 64 | layer record extent slot; sub-record extent slot | reader | layer access | `[R-CNT-13]` |
| L18 | Two structures of one and the same layer claim overlapping bytes in the live committed state | stored-tile extents; tile-index region; layer sub-record extents | verifier | certification | `[R-CNT-13]` (R-IDX-03) |
| L19 | A layer record's sub-record sequence contains more than one user-metadata sub-record (type 0x0002) | — | reader | layer access | `[R-CNT-14]` |
| L20 | A layer record declares both a per-tile alignment A ≠ 0 and a slab S ≠ 0 | — | reader | layer access | `[R-CNT-16]` |
| L21 | entry_count does not equal the geometry-derived addressed-tile count (N interleaved, C·N planar) | interleaved N, entry_count larger; interleaved N, entry_count smaller; planar C·N, entry_count larger; planar C·N, entry_count smaller | reader | layer access | `[R-CNT-17]` (R-CNT-20) |
| L22 | Under index_encoding 1, extent_length ≠ entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero slot with entry_count = 0 | extent_length against the formula, extent_length larger; extent_length against the formula, extent_length smaller; slot (0,0) with entry_count > 0; a nonzero slot with entry_count = 0 | reader | layer access | `[R-CNT-17]` (R-ENC-07, R-CNT-20) |
| L23 | A declared region of the layer record's inline payload does not lie entirely within inline_length (overrun or truncation) | leading fixed fields (name … C); d dimension entries; C channel entries; trailing fixed fields (index_encoding, entry_count, crc_of_crc_array) | reader | open (the name field, §19.1 step 4); layer access (every other field and entry) | `[R-CNT-18]` |
| L24 | A layer record's sub-record carries a reserved-range type value (0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to 1 | — | reader | layer access | `[R-CNT-18]` (R-CNT-15) |
| L25 | A layer record's sub-record carries a type value from the reserved range 0x0003-0x7FFF, which this specification has not assigned; emitting one is a violation whatever its MU bit | — | verifier | certification | `[R-CNT-15]` (R-CNT-18) |
| L26 | A record of type 0x0001 (layer) appears inside a layer record's sub-record sequence | — | reader | layer access | `[R-CNT-18]` (§7.3 registry table) |
| L27 | Layer record has entry_count = 0 but a nonzero crc_of_crc_array | — | reader | layer access | `[R-CNT-23]` (R-IDX-04) |
| L28 | Layer record has slab S = 0 but a nonzero slab alignment A_slab | — | reader | layer access | `[R-CNT-23]` (R-SLB-02) |
| L29 | Layer record declares S ≠ 0 with an A_slab that is not a power of two in 1 … 2^62 (A_slab = 0 included) | A_slab = 0; A_slab not a power of two; A_slab above 2^62 | reader | layer access | `[R-CNT-23]` (R-SLB-02) |
| L30 | A channel entry's fill length prefix differs from the element size of the channel's declared type | prefix longer than the element size; prefix shorter than the element size | reader | layer access | `[R-CNT-23]` (R-TYP-06) |
| L31 | Layer record's index_encoding is a value other than 1 — 0, reserved 2–0x7F, or experimental ≥ 0x80 | index_encoding 0; reserved 2-0x7F; experimental >= 0x80 | reader | layer access | `[R-CNT-23]` (§7.4) |
| L32 | A layer geometry field whose floor is 1 is 0 | rank d; channel count C; tile extent Tᵢ | reader | layer access | `[R-GEO-01]` (R-CNT-23) |
| L33 | Layer record's linearization is a value other than 1 — 0, reserved 2–3, reserved 4–0x7FFF, or experimental ≥ 0x8000 | linearization 0; reserved 2-3; reserved 4-0x7FFF; experimental >= 0x8000 | reader | layer access | `[R-GEO-05]` (R-CNT-23) |
| L34 | A channel entry's type is outside 1 … 13 — 0, reserved 14–19, reserved 20–0x7FFF, or experimental ≥ 0x8000 | type 0; reserved 14-19; reserved 20-0x7FFF; experimental >= 0x8000 | reader | layer access | `[R-TYP-03]` (R-CNT-23, R-CNF-04) |
| L35 | A bool channel's one-byte fill holds a byte other than 0x00 or 0x01 | — | reader | layer access | `[R-TYP-07]` (R-CNT-23) |
| L36 | Layer record's layout is a value other than 1 or 2 — 0 or reserved 3–255 | layout 0; reserved 3-255 | reader | layer access | `[R-SER-06]` (R-CNT-23) |
| L37 | The layer record's crc_of_crc_array ≠ CRC-32C over the segment-CRC array as stored at the tail of the tile-index region | — | reader | tile use | `[R-IDX-04]` (R-CNT-20, R-ENC-10) |
| L38 | A segment CRC ≠ CRC-32C over that segment's entry bytes as stored, entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)) — a partial segment covers only its actual bytes, and the all-sentinel constant 0xEECB3BB2 never substitutes for comparison | — | reader | tile use | `[R-IDX-04]` (R-IDX-05, R-CNT-20, R-ENC-10) |
| L39 | Layer record declares a nonzero alignment A that is not a power of two in 512 … 2^62 | A not a power of two; A below 512; A above 2^62 | reader | layer access | `[R-SLB-01]` (R-CNT-23) |
| L40 | Alignment A declared and a stored tile's index-entry offset is not a multiple of A | — | verifier | certification | `[R-SLB-01]` (R-IDX-03) |
| L41 | Inside a slab run, a stored tile's offset ≠ the previous stored tile's offset plus the previous stored tile's length (gap, overlap, or out-of-ordinal placement; sentinels and entries §15.3 classifies reject-tile on a structural ground are transparent, an entry failing only its stored bytes' crc is not) | gap; overlap; out-of-ordinal placement | verifier | certification | `[R-SLB-03]` (R-IDX-03) |
| L42 | A slab run's first stored tile's offset is not a multiple of A_slab | — | verifier | certification | `[R-SLB-03]` (R-IDX-03) |
| L43 | Layer record's codec is a value other than 1 … 4 — 0, reserved 5–0x7FFF, or experimental ≥ 0x8000 | codec 0; reserved 5-0x7FFF; experimental >= 0x8000 | reader | layer access | `[R-COD-03]` (R-CNT-23) |
| L44 | Codec 4 (lz4) declared on a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes — in a planar layer the largest channel plane governs | interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉ | reader | layer access | `[R-COD-07]` |
| L45 | Layer record's filter is a value other than 1 or 2 — 0, reserved 3–0x7FFF, or experimental ≥ 0x8000 | filter 0; reserved 3-0x7FFF; experimental >= 0x8000 | reader | layer access | `[R-COD-09]` (R-CNT-23) |
| L46 | A layer record's or sub-record's flags carry MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0 | layer record; sub-record | verifier | certification | `[R-CNT-12]` (R-CNT-13) |
| L47 | Any of a layer record's or sub-record's reserved flag bits 2-15 is set | layer record flags bits 2-15; sub-record flags bits 2-15 | verifier | certification | `[R-CNT-12]` (R-CNT-13) |
| L48 | A layer sub-record's user-metadata document has object members, at any nesting depth, not in ascending order of their keys' UTF-8 bytes; the document stays readable and readers process it unchanged | — | verifier | certification | `[R-MTA-05]` (R-CNF-05) |
| L49 | A layer record, or a sub-record of a type §7.3 registers, carries a stored MU or PE bit differing from the value the registry fixes; readers apply the type's fixed semantics regardless | layer record flags bit 0; layer record flags bit 1; sub-record flags bit 0; sub-record flags bit 1 | verifier | certification | `[R-CNT-22]` (R-CNF-05) |

#### 21.4 Tile-scope violations

Outcome: reject-tile — that tile's read reports failure, and never
returns fill in place of data, for a rejection the reader is obliged
to detect (`[R-CNF-09]`); where a row's Detector is *verifier* no
reader is obliged to detect the condition, and the governing rule
states what a reader does. 26 conditions.

| # | Condition | Instances | Detector | Detected | Governing rule |
|---|---|---|---|---|---|
| T1 | A stored tile's bytes at [offset, offset + length) do not match the crc field of its non-sentinel tile-index entry | — | reader | tile use | `[R-CNT-20]` (R-IDX-03, R-ENC-10) |
| T2 | In an interleaved tile, a bool channel's single value byte at a real (non-padding) sample position is neither 0x00 nor 0x01; the same byte at a padding position is T4's, the two rows together covering `[R-SER-08]` | — | verifier | certification | `[R-SER-08]` |
| T3 | The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations | interleaved P·Q, payload longer; interleaved P·Q, payload shorter; planar numeric P·Bᶜ, payload longer; planar numeric P·Bᶜ, payload shorter; packed planar bool ⌈P/8⌉, payload longer; packed planar bool ⌈P/8⌉, payload shorter | reader | tile use | `[R-SER-07]` (R-COD-08) |
| T4 | A padding position does not encode, for each channel it carries, that channel's recorded fill value | interleaved numeric fill bytes; interleaved bool fill byte; planar numeric plane fill bytes; packed planar bool plane fill bit | verifier | certification | `[R-SER-05]` |
| T5 | In a packed planar bool plane with P mod 8 ≠ 0, a final-byte pad bit (bit positions P mod 8 through 7) is not the channel's fill bit | — | verifier | certification | `[R-SER-05]` (R-SER-03) |
| T6 | A tile-index entry has offset and length both 0xFFFF_FFFF_FFFF_FFFF but crc ≠ 0 | — | reader | tile use | `[R-IDX-03]` |
| T7 | A tile-index entry sets exactly one of offset and length to the sentinel value 0xFFFF_FFFF_FFFF_FFFF | offset; length | reader | tile use | `[R-IDX-03]` |
| T8 | A non-sentinel tile-index entry has offset < 16, addressing bytes of the front signature block | — | reader | tile use | `[R-IDX-03]` |
| T9 | A non-sentinel tile-index entry's extent ends past F − 64, touching the live trailer or running beyond the committed file length | — | reader | tile use | `[R-IDX-03]` (R-CNT-13) |
| T10 | A non-sentinel tile-index entry has length = 0 | — | reader | tile use | `[R-IDX-03]` (R-COD-08) |
| T11 | A non-sentinel tile-index entry's offset or length exceeds 2⁶³ − 1 (bit 63 set), neither field being the all-ones sentinel | offset; length | reader | tile use | `[R-IDX-03]` (R-ENC-03) |
| T12 | A non-sentinel tile-index entry's offset + length exceeds 2⁶³ − 1 although each field alone is in domain | — | reader | tile use | `[R-IDX-03]` (R-ENC-04) |
| T13 | A stored tile is not independently decodable from its own extent and layer record — the decode needs state or side data outside the extent; the check that detects it is T25's, and this row records the cause rather than a procedure of its own | deflate stream carrying a previous tile's history window; lz4 block whose match offset reaches back into a previous tile's output | reader | tile use | `[R-COD-02]` (R-COD-06, R-COD-08) |
| T14 | Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size | interleaved P·Q, length longer; interleaved P·Q, length shorter; planar numeric P·Bᶜ, length longer; planar numeric P·Bᶜ, length shorter; packed planar bool ⌈P/8⌉, length longer; packed planar bool ⌈P/8⌉, length shorter | reader | tile use | `[R-COD-04]` |
| T15 | Codec 2 (deflate) and the stored bytes carry a wrapper rather than a raw RFC 1951 DEFLATE stream; the check that detects it is T24's or T25's, and this row records the cause rather than a procedure of its own | zlib RFC 1950 (CMF/FLG header + trailing Adler-32); gzip RFC 1952 member (1F 8B, trailing CRC32+ISIZE) | reader | tile use | `[R-COD-05]` |
| T16 | Codec 2 (deflate) and the stored extent holds more than one DEFLATE stream — a second stream begins after the BFINAL block; the check that detects it is T24's, and this row records the cause rather than a procedure of its own | — | reader | tile use | `[R-COD-05]` |
| T17 | Codec 3 (zstd) and the stored bytes do not begin with the compressed-frame magic 28 B5 2F FD | — | reader | tile use | `[R-COD-06]` |
| T18 | Codec 3 (zstd) and the stored extent holds more than the single compressed frame — a second compressed frame, or a skippable frame wherever it sits, the constraint reading the same at every placement | a second concatenated compressed frame; a skippable frame | reader | tile use | `[R-COD-06]` |
| T19 | Codec 3 (zstd) and the frame header carries a nonzero Dictionary_ID | — | reader | tile use | `[R-COD-06]` |
| T20 | Codec 3 (zstd) and the frame header sets the Content_Checksum_flag | — | reader | tile use | `[R-COD-06]` |
| T21 | Codec 3 (zstd) and the frame declares a window size larger than the tile's decoded size | interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉ | reader | tile use | `[R-COD-06]` |
| T22 | Codec 3 (zstd) and the frame's Frame_Content_Size field is present but does not equal the tile's decoded size | interleaved P·Q, declared larger; interleaved P·Q, declared smaller; planar numeric P·Bᶜ, declared larger; planar numeric P·Bᶜ, declared smaller; packed planar bool ⌈P/8⌉, declared larger; packed planar bool ⌈P/8⌉, declared smaller | reader | tile use | `[R-COD-06]` |
| T23 | Codec 4 (lz4) and the stored bytes are an LZ4 frame (magic 04 22 4D 18) instead of exactly one raw LZ4 block; the check that detects it is T25's, and this row records the cause rather than a procedure of its own | — | reader | tile use | `[R-COD-07]` |
| T24 | The decode does not consume the entry's length exactly — bytes remain in the stored extent after the stream, frame, or block ends | any codec | reader | tile use | `[R-COD-08]` |
| T25 | The stored bytes are a malformed stream that fails to decode | deflate block type 3 / invalid Huffman table; corrupt zstd block header; lz4 match offset 0 or match reaching past produced output | reader | tile use | `[R-COD-08]` |
| T26 | Filter 2 applied at a stride other than the mandated one, where the resulting image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes (a wrong stride with no such structural constraint is undetectable, §21.7); the check that detects it is T2's or T4's, and this row records the cause rather than a procedure of its own | planar numeric: channel element size; interleaved: sample stride Q; packed planar bool: identity s = 1 | verifier | certification | `[R-COD-10]` (R-SER-05) |

#### 21.5 Ignored records

Outcome: ignore-record — the record is skipped as though absent and
decoding of stored data is unaffected. Readers SHOULD report the
loss; silent metadata loss defeats the record's purpose. User
metadata is quarantined (`[R-CNT-25]`): every way its document can
be unreadable takes this outcome, whatever the containing scope —
as a violation in the rows below, except at an experimental-range
encoding, where no document rule attaches and §21.6 records the
defined non-violation (`[R-MTA-10]`), and except where a reader or
verifier declines the decode on the size bound or on the frame's
declared window, which `[R-MTA-09]` makes that actor's capability and
not a fact about the file. Encoding 0 and a reserved-range
value are unassigned too, and R1 registers both as violations: what
`[R-MTA-10]` withdraws is the document's content rules, never the
encoding byte's own value set (`[R-MTA-03]`). Every row
here is a violation all the same: the outcome bounds a reader's
blast radius and never makes the file conforming (`[R-CNF-12]`);
§21.6 lists the ignore-record conditions that are not violations.
10 conditions.

| # | Condition | Instances | Detector | Detected | Governing rule |
|---|---|---|---|---|---|
| R1 | A user-metadata record declares a document encoding of 0, or a reserved-range value (3-0x7F) | encoding 0, top-level record; encoding 0, layer sub-record; reserved 3–0x7F, top-level record; reserved 3–0x7F, layer sub-record | reader | open (top-level); layer access (sub-record) | `[R-CNT-25]` (R-MTA-03, R-EXT-03) |
| R2 | A user-metadata extent's final 4 bytes do not equal the CRC-32C of the preceding bytes | top-level extent; layer sub-record extent | reader | extent use | `[R-CNT-20]` (R-CNT-25) |
| R3 | A user-metadata document's stored bytes fail to decode under its declared assigned encoding — under an experimental-range one this specification defines no decoding and §21.6 governs (`[R-MTA-10]`); encoding 0 and a reserved value are unassigned too and R1 registers both; where the encoding is 2 and what fails is one of the frame constraints R4 registers, R4 is the row, whether or not the bytes also fail to decode | top-level extent; layer sub-record extent | reader | extent use | `[R-CNT-25]` |
| R4 | A user-metadata document stored under encoding 2 breaks one of the frame constraints §18.2 states or carries over from `[R-COD-06]` — the single frame occupying the extent's bytes before its terminal CRC included; unlike R3, a constraint of this row is checkable from the extent's bytes without relying on a decoder's tolerance, and a reader that only tries decoding does not establish which of them is broken — several, the content-size field among them, are broken by what the frame declares while the bytes decode; the content-size field breaks its constraint exactly when it is present and does not equal the decoded document's byte length | missing frame magic, top-level extent; missing frame magic, layer sub-record extent; a skippable frame, top-level extent; a skippable frame, layer sub-record extent; a second frame, top-level extent; a second frame, layer sub-record extent; a nonzero dictionary ID, top-level extent; a nonzero dictionary ID, layer sub-record extent; the content-checksum flag set, top-level extent; the content-checksum flag set, layer sub-record extent; bytes remaining after the frame, top-level extent; bytes remaining after the frame, layer sub-record extent; the content-size field declared larger than the decoded length, top-level extent; the content-size field declared larger than the decoded length, layer sub-record extent; the content-size field declared smaller than the decoded length, top-level extent; the content-size field declared smaller than the decoded length, layer sub-record extent | reader | extent use | `[R-MTA-09]` (R-COD-06, R-CNT-25) |
| R5 | A decoded user-metadata document violates the document's own content rules — a key or string value whose UTF-8 is ill-formed in the source bytes, or that resolves a `\uXXXX` escape denoting an unpaired surrogate | ill-formed source bytes in a key, top-level document; ill-formed source bytes in a key, layer sub-record document; ill-formed source bytes in a string value, top-level document; ill-formed source bytes in a string value, layer sub-record document; unpaired-surrogate escape in a key, top-level document; unpaired-surrogate escape in a key, layer sub-record document; unpaired-surrogate escape in a string value, top-level document; unpaired-surrogate escape in a string value, layer sub-record document | reader | extent use | `[R-CNT-25]` (R-MTA-04, R-ENC-11) |
| R6 | A key of a decoded user-metadata document is empty or contains a code point in U+0000 through U+001F | empty key, top-level document; empty key, layer sub-record document; key with a code point in U+0000–U+001F, top-level document; key with a code point in U+0000–U+001F, layer sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25, R-ENC-12) |
| R7 | A decoded user-metadata document is not well-formed JSON, its top-level value is not an object, or it carries a leading U+FEFF byte-order mark | not well-formed JSON, top-level document; not well-formed JSON, layer sub-record document; top-level value not an object, top-level document; top-level value not an object, layer sub-record document; leading U+FEFF, top-level document; leading U+FEFF, layer sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |
| R8 | A user-metadata document contains a non-finite number — a magnitude whose binary64 interpretation overflows (`1e400`), or one of the bare tokens `NaN`, `Infinity` and `-Infinity`, which RFC 8259 does not admit | overflowing magnitude, top-level document; overflowing magnitude, layer sub-record document; bare token, top-level document; bare token, layer sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |
| R9 | Two members of one object in a user-metadata document carry the same key, identity being the decoded string and not the JSON source bytes (`"a"` and `"\u0061"` are the same key) | top-level document; layer sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |
| R10 | A user-metadata document key is longer than 255 bytes | top-level document; layer sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25, R-ENC-12) |

#### 21.6 Conditions that are not violations

These are defined behaviors, not errors. A reader that treats any
of them as a validity failure is the nonconforming party; where an
entry records a resource decline, the decline is licensed and
reported as `[R-ERR-04]` requires.

| Condition | Defined behavior | Rule |
|---|---|---|
| An index entry is the sentinel | The tile is addressed but not stored; every sample position it carries inside the layer's extents reads, for each channel the tile carries, as that channel's fill | `[R-IDX-02]`, `[R-TYP-08]` |
| A requested coordinate lies outside the layer's extents | The request fails as a request, with no verdict on the file; a region request returns the intersection, empty if disjoint | `[R-MDL-01]`, `[R-GEO-02]`, `[R-RDR-04]` |
| A dimension has extent 0 | A valid, empty layer: zero addressed tiles, an empty index, reads returning no samples | `[R-GEO-02]` |
| The file contains zero layers | A conforming file: a directory carrying no layer record is a conforming generation whether or not it carries other records, an empty directory included | `[R-CNT-14]`, `[R-CNT-02]` |
| A record type this specification has not assigned, from the experimental range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped per its PE bit; a *reserved*-range type is read the same way, but emitting one is a violation (F36, L25) | `[R-CNT-15]`, `[R-CNT-18]`, `[R-WRT-08]` |
| An ignore-lane flag bit (16–31) is set | Ignored; the file is conforming — such bits are defined by later minor versions | `[R-CNT-08]` |
| version_minor is higher than this text defines | Accepted; minors never gate | `[R-CNT-07]` |
| Bytes the live state does not claim — alignment gaps, the pre-trailer pad, superseded regions | Slack: unconstrained content, no conformance requirement, counted and reported by a verifier; where its walk did not complete, as a partial total, an upper bound naming what stopped the walk; only a rewrite reclaims it | `[R-CNT-21]` |
| A layer mixes bool and numeric channels, in either layout | Defined: planar bool planes pack, interleaved bool values are single bytes; a reader MUST NOT reject the layer for the combination | `[R-SER-09]` |
| A user-metadata record declares an experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a writer's conduct, not the bytes. No document rule attaches at such an encoding, so a verifier certifies, reporting the record it ignored | `[R-MTA-03]`, `[R-EXT-03]`, `[R-CNF-02]`, `[R-MTA-10]` |
| A user-metadata document carries an unrecognized `tarn.`-prefixed key | Conforming: later minor versions register keys, and this text's readers ignore the key and read the rest of the document | `[R-MTA-06]` |
| A standardized key (§18.4) appears outside its listed scope, or carries a value whose shape its row does not give | Conforming: placement and value shape are writer guidance, and a reader ignores the key and reads the rest of the document, exactly as for an unrecognized key above | `[R-MTA-07]` |
| A user-metadata document's decoded size, or its frame's declared `Window_Size`, exceeds the reader's own bound, which is no smaller than §21.9's guarantee | Ignore-record on resource grounds — the narrowest-scope decline `[R-ERR-04]` names for a document — reported as a resource limit and not as corruption; the file is conforming, and the reader MAY instead decline any scope containing the record, the whole file included | `[R-MTA-09]`, `[R-ERR-04]` |
| A payload contains a byte string that mimics a trailer | Inert: no reader scans backward (`[R-LIF-05]`), the coverage walk claims a live payload's bytes as the extent or region carrying them, a tile's, a record's or the directory's (`[R-LIF-08]`), and enumerates nothing in slack, and a recovery tool re-verifies its output whole (§9.6) — which catches any mimic that is not itself a consistent generation; §9.6's second caution covers the rest | `[R-LIF-05]`, `[R-LIF-06]`, `[R-LIF-08]` |
| Under a compressing codec (2–4), a stored tile's decoded size differs from its stored length | Expected: codecs compress, and can expand — codec 1's equality is `[R-COD-04]`'s subject | `[R-COD-08]` |

Two conditions that once sat in this table are violations and are
registered above: a user-metadata document whose object members are
unsorted (`[R-MTA-05]`), and a registered record type whose stored MU
or PE bit differs from §7.3's registry (`[R-CNT-22]`). Both make the
file nonconforming while leaving every reader behavior unchanged —
readers process the document and apply the type's fixed semantics —
so both carry detector *verifier*, on the precedent `[R-CNT-12]`'s
reserved-flag rows already set. What belongs here is the reader's
obligation, and it is unchanged: neither obliges a reader to reject
anything. What did change is that each now makes the file
nonconforming, so `[R-CNF-12]`'s licence to reject on any detected
violation reaches a reader that detects one, a licence that did not
arise while these sat in the table above.

Two structural cases are **conforming files a reader nevertheless
refuses**. The first is **version_major naming a major this reader
does not implement**: the reader rejects the file (`[R-CNT-07]`), but
the file can be perfectly conforming under that major. The second is
an **experimental-range top-level record type carrying MU = 1**
(§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and
`[R-CNF-02]` makes the file conforming all the same. The qualifier is
load-bearing — the same type as a layer sub-record is reject-layer and
never a ground to refuse the file (`[R-CNT-18]`), so only the
top-level case is a file a reader refuses, since the prohibition on
publishing experimental values binds a writer's conduct and not the
bytes. In both the outcome records a reader's capability, not a defect
in the bytes, and the diagnostic ought to distinguish the two.
Neither is a register row: the register enumerates file-conformance
violations (§21.1); the first is a file this document declines to
judge under format major 1 (§2.3, `[R-CNF-13]`), and the file in the
second carries no violation at all. What is registered in each case
is the neighbouring condition
that *is* a violation — version_major = 0, which declares no major at
all (F18, `[R-CNT-07]`), and a *reserved*-range
type, whose emission `[R-CNT-15]` does make a violation (F35, F36,
L24, L25).

#### 21.7 What no check detects

Stated plainly, because a register invites the opposite assumption:
this format detects *corruption of structure*, not *incorrectness of
content*. A writer that emits well-formed structures carrying wrong
sample values — a mis-strided filter (`[R-COD-10]`), an undisclosed
compression dictionary (`[R-COD-06]`, and `[R-MTA-09]` for a
user-metadata document, whose wrong content is the document's
rather than a tile's samples), or simply wrong data — produces a
file that every checksum in §8 certifies. Checksums are
computed over what the writer wrote. The obligations of §14.5 and
`[R-SER-08]` narrow this only where content is structurally
constrained: padding positions, pad bits, and boolean bytes.
Nothing here authenticates, either (§4.5). None of these is a
requirement a verifier is *unable to check* within the meaning of
`[R-CNF-11]`: no file-level witness exists to check, so nothing about
the file is left undetermined and the verdict is unaffected.

A condition this specification names is **unwitnessed** where, for
every file exhibiting it, some file that does not exhibit it cannot
be told apart from it by any check this specification obliges a
reader or a verifier to perform. It is **detectable** in the
contrary case: where some file exhibiting it is separated from every
file that does not by some such check, which need not be the same
check for every one of those files. The two are stated over the
same subject, and each quantifier is the other's dual, so each is
exactly the negation of the other, and detectability so stated is
the gate `[R-CNF-07]` applies in assigning an outcome and §21.1's
completeness clause turns on. The register carries a row for every
condition that is a detectable file-conformance violation. An
unwitnessed condition is not one, so that clause requires no row for
it, and its absence is not the defect that clause names.

That is the whole of the test, and it decides any condition put to it
without appeal to a list. The instrument is the checks this
specification obliges an actor to perform, and deliberately not the
register's own rows — a test
keyed to the rows would make §21.1's completeness clause vacuous,
every omitted condition being undetectable by construction.

**The subject is the condition and not the requirement**, as
`[R-CNF-13]` individuates them and as `[R-CNT-06]` shows by stating
nine. A single requirement states conditions of both kinds where it
states several, and is classified as a whole by neither. Being unwitnessed bears on
detection and not on permission: the requirement binds its actor as
any other does, and the outcome classes of §2.4 are assigned to
violations a reader or verifier can establish rather than to every
violation this document names.

Distinguish an unwitnessed condition from a requirement that states
**no condition a file can exhibit**. `[R-ENC-06]`'s fixed field widths are not a state a file
can be in — the parse is always at the widths this specification
fixes, and a structure written at any other yields different values
at them — a different file, conforming or not on its own terms.
Nothing is omitted from the register on its account, there being no
condition to omit. `[R-ERR-01]`

#### 21.8 Conformance vector coverage

Every row of §21.2 through §21.5 — 120 conditions over 277
instances — has at least one conformance vector (§24) whose expected
outcome is that row's outcome, and at least one vector per instance. A row without a vector is a
gap in the corpus, not a licence to skip the check. `[R-ERR-02]`

#### 21.9 Implementation limits

Every limit affecting which files are valid, or which files a
conforming reader accepts, lives in this specification and never only
in an implementation (`[R-CNF-10]`); this section collects the ones an
implementer most often needs at hand. The hard limits it restates are
a finding aid rather than an inventory — each is normative where the
structure forcing it is defined. The table
below states **minimum guarantees**, not caps: a conforming reader
MUST accept any conforming file whose quantities lie within these
bounds, and a writer MAY rely on that. `[R-ERR-03]`

| Quantity | A conforming reader MUST accept at least |
|---|---|
| rank d of a layer | 32 |
| channels per layer, C | 4096 |
| addressed tiles per layer (entry_count) | 2³² |
| layers per file | 65,536 |
| size of the directory region, dir_length | 16 MiB |
| decoded size of one tile | 256 MiB |
| decoded size of one user-metadata document | 16 MiB |
| zstd frame `Window_Size` | 8 MiB |

The last three rows are **per-instance**, and are individuated
differently. *Decoded size of one tile* ranges over a layer's
**addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is:
a tile's decoded size is a function of the layer's declarations alone
(`[R-SER-07]`), so an addressed tile has one whether or not its index
entry is the sentinel. A layer addressing no tile (§11.2) therefore
has no tile whose decoded size the table bounds. The other two range
over the user-metadata documents and compressed frames a file
actually contains, neither of which exists except as stored bytes.
Either way a file containing no instance of a kind does not exceed
that row, whatever its declarations would derive. The first five rows
range over declarations, which every file and every layer carries.

A file exceeding any of these remains conforming, and a reader MAY
decline it: at the whole file, or at the narrowest scope whose
stated or derived quantities exceed what it can serve, be that a
layer, a tile, the record carrying a user-metadata document (as
§18.2 assigns), or the file itself where the quantity is the file's,
as layers per file and dir_length are. It MAY also decline at any
scope that contains the
narrowest one, as `[R-COD-06]` provides for a frame's window and
`[R-CNF-11]` presupposes. Software that declines **on that ground** a file whose every quantity lies
within the table is not a conforming reader (`[R-CNF-03]`) — the two
capability refusals §21.6's closing paragraph names, a foreign format
major and an unimplemented top-level MU = 1 type, are not this
ground — the
guarantees are the floor, not a suggestion. In every case, a refusal
on resource grounds MUST be reported as a resource limit and not as
a validity error: the two send a user to opposite remedies, and a
reader that reports "too large" as "corrupt" invites the deletion
of intact data. `[R-ERR-04]`

> **Note.** Where the numbers come from: rank and channel counts
> follow established array-ecosystem ceilings; 2³² addressed tiles
> is the point where the segment-CRC array a reader fetches whole
> before using any entry (§15.4) is still 256 KiB — it reaches 4 MiB
> at 2³⁶; 65,536 layers is roughly a 12.5 MiB directory at the small
> layer records that figure assumed, and the 16 MiB directory row
> states that same budget over the region itself, because the
> region's size is the product of the layer count with each record's
> channel entries and names rather than the layer count alone, and
> §19.1's open fetches and CRCs it whole before any other use
> (`[R-CNT-11]`, `[R-RDR-01]`); 256 MiB is
> an order of magnitude above the tile sizes §11.3 describes as
> ordinary, so the guarantee never binds a typical file; 8 MiB is
> the decoder window support
> RFC 8878 itself recommends, which stock encoder settings stay
> within.

Some limits are instead **hard**: a file violating one is invalid,
not merely large. They are stated where the structures forcing them
are defined — a layer, dimension or channel name at most 255 bytes
(`[R-ENC-12]`, a `u8` length prefix), and a user-metadata key at most
255 bytes by §18.2's folding of §4.6's name rules onto keys, which
carry no such prefix; rank at most 255 and channel count at most 65,535 (§7.4's
`u8` and `u16` fields); a layer declaring codec 4 with every
addressed tile's decoded size at most `0x7E000000`, the largest
channel plane governing in a planar layer (`[R-COD-07]`); every
offset, length,
extent, and count at most 2⁶³ − 1 (`[R-ENC-03]`); a declared
alignment A a power of two with 512 ≤ A ≤ 2⁶², and a declared slab
alignment A_slab a power of two with 1 ≤ A_slab ≤ 2⁶² (§16.1, §16.2,
`[R-SLB-01]`, `[R-CNT-23]`); a slab run length S with
1 ≤ S ≤ 2⁶³ − 1 (§16.2, `[R-CNT-23]`); a directory of at least 4
bytes at an offset of at least 16 (§6.2, `[R-CNT-06]`); and no
conforming file shorter than 128 bytes (§5.1, `[R-CNT-27]`). Most
follow from a field's width, an external format, or the value
domain, and the rest from arithmetic over structures a generation
cannot omit. Some do not: the 512 floor on A is a number chosen
here, fixed at the legacy sector size (§16.1) so that a declared
alignment is worth declaring; the 2⁶² ceilings on A and A_slab, and
the power-of-two shape each takes, are chosen here too rather than
consequences of the u64 domain; and the 255-byte cap on a user-metadata
key is this specification folding §4.6's name rules onto keys, which
carry no length prefix to force it. `[R-ERR-05]`

### 22. Security Considerations

#### 22.1 Threat model

A TARN file is untrusted input. This section assumes an adversary
who fully controls the bytes a reader is given — including files
that validate — and who can control the transport. The defenses
below are structural: they hold because a conforming reader derives
what it allocates and fetches from *declarations it has verified*,
never from payload content. `[R-SEC-01]`

#### 22.2 Resource exhaustion

Three properties bound what a hostile file can make a reader spend.
Decoded tile size is a function of the layer's declarations alone
(§14.2, §14.3), so a reader allocates from geometry and never from
a length embedded in a payload — a compressed stream that expands
beyond the declared decoded size is a tile-scope error
(`[R-COD-08]`), which is this format's decompression-bomb defense
and the reason no codec's embedded size field is ever an allocation
source (`[R-COD-06]`). Every declaration-derived sum and product
`[R-ENC-04]` designates is overflow-checked before use. And nothing is
allocated, sought, or fetched on the strength of a field before the
checksum covering it verifies (`[R-ENC-05]`). A reader MUST
NOT size an allocation, fetch, or index walk in proportion to a
declared magnitude it has not corroborated against the file's actual
length: a layer can declare 2⁶³ − 1 addressed tiles, and the
declaration alone costs nothing to state. `[R-SEC-02]`

> **Note.** The index is the cheapest hostile amplifier: entry_count
> is one `u64`, and `[R-CNT-17]`'s cross-check ties it to the
> region's declared length while `[R-CNT-13]` ties that length to
> the file's actual size — a reader that validates both before
> fetching cannot be induced to read more than the file contains.

#### 22.3 Structural attacks

Extents are owned exactly once (`[R-CNT-13]`): no two structures
overlap, which removes aliasing — two index entries pointing at one
payload, or a payload overlapping a structure that governs it — as
a class. Byte coverage (`[R-CNT-02]`) partitions the *live* state
exactly: every byte a reader can reach is the front signature block or
belongs to exactly one named structure.
It bounds nothing outside that — slack is unconstrained and can
hold anything (§23.1) — so coverage makes bytes reachable by a reader
accounted for, and makes everything else *countable* rather than
absent: a verifier reports the slack total (§9.7), which is the number
that distinguishes a working file from a padded one — a verifier that
stopped early reports it only as partial (`[R-CNT-21]`), so the
distinguishing figure comes from a walk that completes. Both are
verifier-detected: a reader that skips them is still conforming, so a
pipeline accepting files from untrusted sources SHOULD verify rather
than merely read; without that, an
attacker's smuggled bytes travel unexamined. `[R-SEC-03]`

Four residues are stated rather than defended. Slack is covered by no
checksum (§8.1) and constrained by no rule: corruption confined to it
is invisible to reader and verifier alike, and is caught only by the
slack total changing (§9.7) — which is why a writer that zeroes its
gaps (`[R-CNT-03]`) makes its own files easier to reason about, not
because conformance turns on it. The extent of a record of a type this
specification has not assigned is covered by no checksum either
(§8.1), so corruption inside it is equally invisible: §20.4's
byte-identical re-emission (`[R-WRT-05]`) carries such an extent
forward unread, and `[R-WRT-08]` bars re-encoding it, so nothing an
updater does would surface the damage. And a payload can contain a byte string that mimics
a trailer; recovery tooling that scans backward can land on one, which
is why recovery output is re-verified as a whole file before being
trusted (`[R-LIF-06]`): under live-state coverage a mimic in slack
is inert — nothing enumerates it — and one in a live payload is the
bytes of the extent or region the walk claims (`[R-LIF-08]`), but a
recovery tool that
truncates to one produces a different file. And the extent of a user-metadata
record under an experimental-range encoding is covered by its
terminal CRC
but constrained by no content rule (`[R-MTA-10]`): the CRC detects
corruption and authenticates nothing (§4.5), so a certificate
covers those bytes uninspected — which is why `[R-MTA-10]` makes
the verifier's report name each such record, and an operator who
wants no such bytes rejects on that report line, a policy above
conformance. `[R-SEC-04]`

#### 22.4 Content the reader hands onward

Names are length-prefixed and screened for C0 controls
(`[R-ENC-12]`), which removes ESC-introduced escape sequences and
CR/LF injection from the identifiers a tool is most likely to print.
It removes nothing else: U+007F, the C1 range U+0080-U+009F (where
U+009B is CSI to a terminal in 8-bit mode), and bidirectional
overrides such as U+202E are all legal in a conforming name. A
display surface MUST NOT assume a name is safe for its own syntax, and a reader MUST NOT interpret a name
as a filesystem path — nothing in this format names a path, and
treating one as such reintroduces traversal in the consumer.
`[R-SEC-05]` User metadata is application data and is never
structural (§7.1): a reader MUST NOT let it influence how any byte
is located or decoded. `[R-SEC-06]`

#### 22.5 What this format does not provide

Checksums detect accidental corruption. They do not authenticate:
an adversary who can modify bytes can recompute every checksum in
the file, and a file that verifies proves only internal consistency
(§4.5). This format provides no confidentiality, no authenticity, no
signing, and no access control; deployments needing them wrap the
file in a mechanism that does. Committed-prefix immutability (§9.1)
makes that compose well: a detached signature over the committed
prefix [0, F) of one generation, pinned to the file_id its trailer
names and to that F, stays valid over that prefix under every later
append — though it attests that generation, not the file a reader
opens later. `[R-SEC-07]`

### 23. Privacy Considerations

#### 23.1 Deletion is not erasure

The append-only model (§9.1) means that what a commit removes, it
removes only from *reachability*. It removes sample data by making it
unreachable and never by erasing it: superseding a stored tile's
payload, unstoring a tile so its entry becomes the sentinel (§15.2),
and shortening a planar layer's channel list from its end, which takes
the removed channels' tiles out of the addressed set (§20.3 step 4),
all do it, and a record's
extent goes the same way whether a commit drops the record (§20.4) or
supersedes it — editing a user-metadata document appends a new extent
and strands the old one (§20.3 places this with shape (b)), which is
the case most
likely to strand content a caller believes it deleted, and a commit
that drops a layer (§20.4) strands every tile it stored, its
tile-index region and its sub-records' extents, a layer's
user-metadata document among them. **Where the structure carrying the bytes leaves the
live state**, they remain in the file as slack (`[R-CNT-21]`),
readable by anyone with the bytes and a hex editor, and recoverable
by any tool that scans backward for an earlier trailer (§9.6). That
is every case: no commit turns a real position of a stored tile into
padding, a shrink of a layer that stores a tile being a rewrite
(§20.3 step 4), so the bytes a commit makes unreachable always leave
the live state whole; the list
of operations above is not offered as closed. Writers and the tools
built on them MUST NOT represent any commit that makes sample data
unreachable as erasure of it — a channel removal reported as erasure
misleads exactly as a supersede so reported does.
`[R-PRV-01]`

A rewrite (§20.5) is the only operation that removes slack,
and it does so by writing a new file — the input persists,
unmodified, until something outside this specification deletes it,
and a filesystem-level deletion leaves the bytes recoverable on many
media. A deployment whose obligation is erasure MUST treat that
obligation as belonging to its storage layer, not to this format.
`[R-PRV-02]`

#### 23.2 What a file discloses

A conforming file discloses more than its sample values: layer,
dimension, and channel names; declared geometry; the write footprint
of every layer at tile granularity, since a sentinel entry (§15.2)
marks each addressed tile not stored in the live generation — a tile
unstored by a later commit leaves its earlier payload in the file as
slack (§23.1) — so the index
publishes which regions were written without disclosing what is in
them; the user-metadata document,
which is quarantined from structural interpretation (§7.1) but not
hidden; and the shape of its own history — the size of each commit
and the slack it left behind, recoverable by probing backward for
the superseded trailers that committed-prefix immutability keeps in
place (§9.1, §9.6). No field carries a count of the commits that
produced a file, so their number follows only from that probe: it is
unavailable to anyone holding just the live trailer, and absent
altogether from a rewritten file (§20.5), which retains no earlier
trailer to find.
Writers handling sensitive material SHOULD treat names and metadata
as published content, and SHOULD compact before publication when the
history itself is sensitive. `[R-PRV-03]`

The `file_id` (§9.3) is a stable 64-bit identifier that persists
across every generation of a file - high-entropy only when its
writer follows §9.3's randomness advice, which `[R-LIF-03]` states
as a SHOULD. It is what makes
`(file_id, range)` caching sound, and equally what lets an observer
correlate two copies of a file as the same artifact. A rewrite
mints a new one (`[R-WRT-06]`) - the only defined way to break
*file_id* linkage, and not an unlinkability measure: `[R-WRT-07]`
preserves every stored tile's bytes and every index entry's crc bit
for bit, so a compacted file remains trivially correlatable with its
input by content. `[R-PRV-04]`

#### 23.3 Remote access patterns

The remote read path (§6.4, §19.4) issues byte ranges determined by
which layer and which tiles a reader wants. An observer who sees
those ranges — a server operator, a proxy, or anyone on an
unencrypted transport — learns which region of which layer was read,
and the tile grid makes that inference precise. This is a property
of range-based random access, not a defect. A reader that needs to
hide its access pattern MAY fetch whole files or interpose a
private-retrieval layer, and SHOULD read only over an encrypted
transport; over an unencrypted one every range it requests is
visible to anyone on the path. `[R-PRV-05]`

### 24. Conformance Test Vectors

The conformance corpus is a set of TARN files with recorded
expectations, distributed with this specification in `conformance/`
and licensed CC0 so that using it imposes nothing on an
implementation.

The corpus is **derivative**: a conforming implementation is one that
satisfies this specification's requirements, and where a vector's
recorded expectation and this specification disagree, this
specification governs and the vector is corrected. Passing the corpus
is evidence of conformance, never its definition — a corpus exercises
what someone thought to write, and this document states more than any
finite set of files can demonstrate. `[R-VEC-01]`

Each vector is one file plus a manifest entry recording, at minimum:
its identifier; whether the file is **conforming**; the decoded
content a reader is to return from every scope it can read, with each
floating-point value written as a hexadecimal bit pattern so that no
comparison depends on a number formatter; and, for each structure the
file damages, the outcome class (§2.4), the scope, and the §21
register row it exercises together with that row's governing
requirement identifier — a row label is never renumbered and never
reused, so it denotes one condition for the life of format major 1,
exactly as §2.2 makes the identifier permanent, and recording both
ties the vector to the rule as well as to the row.
The two axes are independent: a conforming
file can carry a record a reader ignores (§21.5, §21.6), and a
nonconforming file can still read correctly outside the scope its
violation damages. Naming the row is a constraint on how a vector is
built, not a claim about the file: a vector is constructed so that one
row is the one it exercises, and where a condition cannot be isolated —
§6.2's field gates are validated together, so a file failing two of
them attributes to neither alone — the entry records every row the file
exercises and says which it was built for. A vector whose expectation
cannot be stated in
those terms is testing something this specification has not defined,
which makes it a finding against this document rather than a vector.
`[R-VEC-02]`

Every vector whose recorded outcome is reject-layer or reject-tile is
built inside a file that also carries an **intact sibling** — another
layer, or another tile of the same layer where that layer is one a
reader is still permitted to serve — whose decoded content the
manifest records, and a vector's expectation is therefore a pair.
Where the row's detector is the reader, that pair is the scope no
reader is permitted to serve and the content a reader that serves
anything at all owes. Where it is the verifier, no reader is obliged
to refuse anything (§21.1), so the pair is the scope at which a
verifier confines its finding — carried by the entry's own scope and
detector fields (`[R-VEC-02]`) — and the content a reader owes from
every scope, the damaged one included. Without the sibling a vector cannot
distinguish a reader that scopes its refusal from one that rejects
the file entire, because `[R-CNF-12]` permits the latter for any
nonconforming file and every vector built from §21's register is
nonconforming. A corpus of single-scope vectors would demonstrate
only that a violation was detected, which is the weaker of the two
claims §24 makes. `[R-VEC-04]`

Coverage is the corpus's own obligation, inherited from
`[R-ERR-02]`: every register row has at least one vector for each
instance it names, and every sentinel, every boundary value, and every
hard limit of `[R-ERR-05]` has one at its stated bound. §21.9's
minimum guarantees are exercised where a vector at the bound is
constructible — the tile-count guarantee is not, its index region
alone running to tens of gigabytes of incompressible entries, and is
exercised instead by a scaled vector spanning several segments with
the bound checked arithmetically. A missing vector is a gap in the
corpus and never a licence to skip the check it would have exercised.
`[R-VEC-03]`

> **Note.** A recorded outcome is the *narrowest* scope a reader may
> refuse to serve, not the only one: a vector exercising a
> reject-layer row expects that layer to be unusable, and an
> implementation that instead rejects the whole nonconforming file is
> exercising `[R-CNF-12]`'s licence, not failing the vector. What the
> corpus tests is that no reader serves data from a scope this
> specification rejects — which a corpus checking only "accepted or
> rejected" could not tell you. The distinction is worth reporting
> rather than hiding: an implementation that reads the intact sibling
> and refuses the damaged scope has been tested for scope, and one
> that rejects the file has not, though both pass. `[R-VEC-04]` is
> what keeps the second from being the only outcome the corpus can
> observe.

---

## Appendices

### Appendix A — An annotated minimal file (non-normative)

The smallest conforming TARN file is 128 bytes: a front signature
block, an empty directory, the pre-trailer pad, and a trailer. It
contains no layers, which §21.6 records as valid.

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00
0010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
0050  10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
0060  80 00 00 00 00 00 00 00  EF CD AB 89 67 45 23 01
0070  00 00 00 00 00 00 00 00  00 00 00 00 7E 15 2F 40
```

| Bytes | Value | Meaning |
|---|---|---|
| [0, 8) | `89 54 41 52 4E 0D 0A 1A` | front signature magic (§6.1) |
| [8, 16) | zero | front signature reserved (§6.1) |
| [16, 20) | `00 00 00 00` | the directory region: a record sequence of zero bytes, followed by its CRC-32C — which for zero bytes is 0x00000000 (§7.1, §4.5) |
| [20, 64) | zero | pre-trailer pad, 44 bytes — slack, zeroed as `[R-CNT-03]` advises |
| [64, 72) | `8A 4E 52 41 54 0D 0A 1A` | trailer magic (§6.2) |
| [72, 74) | `01 00` | version_major = 1 |
| [74, 76) | `00 00` | version_minor = 0 |
| [76, 80) | `00 00 00 00` | flags: no incompat bit set, no ignore-lane bit set |
| [80, 88) | `10 00 …` | dir_offset = 16 |
| [88, 96) | `04 00 …` | dir_length = 4 |
| [96, 104) | `80 00 …` | committed_file_length = 128 = the file size |
| [104, 112) | `EF CD AB 89 67 45 23 01` | file_id = 0x0123456789ABCDEF, little-endian (any nonzero value; a real writer draws it randomly, §9.3) |
| [112, 124) | zero | trailer reserved, 12 bytes, zero |
| [124, 128) | `7E 15 2F 40` | trailer CRC-32C = 0x402F157E, over trailer bytes [0, 60) |

A remote reader opens this file in §6.4's two requests: the final 64
bytes, validated per §6.2; then [16, 20), whose CRC it verifies. A
local reader additionally verifies bytes [0, 16) by equality first,
which `[R-CNT-04]` requires of any reader holding them — as a remote
reader does too whenever its speculative suffix window reaches offset
0, which on this 128-byte file means a window of the whole file. A
shorter window can still spare the second request: 112 bytes covering
[16, 128) contains the directory, so §6.4's containment test applies,
while bytes [0, 16) stay non-resident, so §6.1 leaves the front-block
check to the reader. That is §19.1's four-step open
applied to this file; the layer table is empty, and there is nothing
further to read.

### Appendix B — Constants (non-normative)

Every named constant this specification fixes, collected. Each is
normative where it is defined; this table is a finding aid.

| Constant | Value | Defined in |
|---|---|---|
| Front signature block | `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes (16 bytes) | §6.1 |
| Trailer magic | `8A 4E 52 41 54 0D 0A 1A` | §6.2 |
| Trailer size | 64 bytes, at a 64-aligned offset | §6.2 |
| Smallest conforming file | 128 bytes | §5.1 |
| Directory minimums | dir_offset ≥ 16, dir_length ≥ 4 | §6.2, §5.1 |
| User-metadata extent minimum | extent_length ≥ 5 | §7.1 |
| Boolean byte encoding | `0x00` = false, `0x01` = true | §13.2, §14.2 |
| Media type (intended; registration pending) | `application/vnd.tarn` | §6.1 |
| Record header size | 24 bytes | §7.2 |
| Index entry size | 20 bytes | §15.1 |
| Index segment size | 2¹⁶ entries; 4-byte CRC each | §15.1, §15.4 |
| Unstored-tile sentinel | `FF ×16 00 ×4` (offset and length 2⁶⁴ − 1, crc 0) | §15.2 |
| CRC of a full all-sentinel segment | `0xEECB3BB2` | §15.4 |
| Checksum | CRC-32C, polynomial 0x1EDC6F41, reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian | §4.5 |
| CRC check vector | CRC-32C(`"123456789"`) = `0xE3069283`; CRC-32C(zero bytes) = `0x00000000` | §4.5 |
| Value domain | 0 to 2⁶³ − 1 for every offset, length, extent, and count | §4.2 |
| Name length | at most 255 bytes of UTF-8 | §4.6 |
| Rank d, channel count C | at most 255 and 65,535 — the widths of their fields | §7.4 |
| Slab run length S | 1 ≤ S ≤ 2⁶³ − 1 | §7.4, §16.2 |
| Per-tile alignment A | power of two, 512 ≤ A ≤ 2⁶²; 4096 recommended | §7.4, §16.1 |
| Slab alignment A_slab | power of two, 1 ≤ A_slab ≤ 2⁶² | §7.4, §16.2 |
| Discovery window (writer SHOULD) | trailer + pad + directory within 65,536 bytes | §6.4 |
| Tile working range (guidance) | roughly 1–16 MiB decoded | §11.3 |
| zstd frame magic | `28 B5 2F FD` (0xFD2FB528) | §17.2 |
| lz4 decoded tile size cap | `0x7E000000` | §17.2 |
| Reserved metadata key prefix | `tarn.` | §18.3 |
| Reader minimum guarantees | rank 32 · C 4096 · entry_count 2³² · 65,536 layers · 16 MiB directory region · 256 MiB decoded tile · 16 MiB metadata document · 8 MiB zstd window | §21.9 |

### Appendix C — Registry snapshot (non-normative)

The machine-readable registry is `spec/registry.json`, versioned with
this specification; §10.2's table and this snapshot restate it, and
where any of the three diverge the section defining the space governs
(`[R-EXT-05]`).

**Record types** (§7.3): 0x0001 layer (MU = 0, PE = 0); 0x0002 user
metadata (MU = 0, PE = 1).

**Sample types** (§12.1): 1 bool · 2–5 int8/16/32/64 · 6–9
uint8/16/32/64 · 10 float16 · 11 bfloat16 · 12 float32 · 13 float64.
Pinned reservations: 14 float8 E4M3 and 15 float8 E5M2 (OCP OFP8
only) · 16 int128 · 17 uint128 · 18 float128 · 19 opaque.

**Codecs** (§17.2): 1 none · 2 deflate · 3 zstd · 4 lz4.
**Filters** (§17.3): 1 none · 2 byte-shuffle.
**Channel layouts** (§14.1): 1 interleaved · 2 planar.
**Linearizations** (§11.4): 1 row-major.
**Index encodings** (§7.4): 1 raw-segmented.
**Metadata encodings** (§18.2): 1 none · 2 zstd.
**Trailer flags** (§6.3): none assigned; bits 0–15 incompat lane, bits
16–31 ignore lane.

**Standardized metadata keys** (§18.4): `tarn.title` · `tarn.description`
· `tarn.created` · `tarn.creator` · `tarn.axes` · `tarn.stats`.

### Appendix D — Design rationale (non-normative)

Six choices shape everything else, and each has a cost worth naming.

**A tail-anchored trailer.** Discovery lives at the end of the file so
that appending never rewrites a committed byte. The cost is that a
cold remote open begins with a suffix request, which is why §6.4
states the request accounting rather than leaving it to be discovered.

**Append-only, with a complete directory per generation.** Every
commit re-emits the whole directory, so a torn write leaves the prior
state intact. The cost is slack — and the decision that shaped
this specification most is what slack *is not*: not a history to
certify, not a log to audit, just waste awaiting compaction. Coverage
therefore certifies the live state and counts the rest (§5.2, §9.7),
which is why this document has no generation-attribution machinery,
no trailer chain, and no counter in the trailer numbering the
commits.

**Checksums everywhere, with per-scope outcomes.** Integrity is not a
mode. The cost is one CRC per structure and a strictly ordered chain
of trust (§8.2); the benefit is that a corrupt tile costs a tile.

**A closed type list and codec menu.** Every conforming reader opens
every conforming file. The cost is that anyone needing a type or codec
outside the list waits for a minor version, which is the deliberate
price of having no dialects.

**Raw fixed-size index entries.** Twenty bytes per tile, segmented so
that any entry is reachable by fetching one segment and its CRC array.
The cost is size at extreme tile counts; the benefit is that no reader
decodes an index to read one tile, and §21.9's entry_count guarantee
is set where that cost is still bounded.

**Quarantined metadata.** Application metadata can never affect how a
byte is located or decoded, so it can be unbounded, compressible, and
skippable. The cost is that anything structural has to be a
structural field, which is why fill values, geometry, and codecs are not keys.

### Appendix E — Changelog (non-normative)

| Version | Date | Summary |
|---|---|---|
| 1.0 (draft) | unreleased | First complete draft of format major version 1. |

Once this specification is published, every subsequent revision
records here what it changed and which ADR governs the change.
Minor versions are additive only (§6.3); a change that is not additive
is a new format major version.

### Appendix F — Normative references

- **[BCP 14]** RFC 2119 and RFC 8174 — the requirement keywords (§2.1).
- **[RFC 3720]** §12.1 — the CRC-32C polynomial and parameters (§4.5).
- **[IEEE 754]** IEEE 754-2019 — binary16, binary32, and binary64 (§12.1),
  and the conversion from decimal text to binary64 under IEEE 754's
  default rounding-direction attribute, roundTiesToEven (§18.2).
- **[RFC 1950]** ZLIB Compressed Data Format Specification version 3.3 — a wrapper codec 2 excludes (§17.2, T15).
- **[RFC 1951]** DEFLATE Compressed Data Format Specification version 1.3 — codec 2 (§17.2).
- **[RFC 1952]** GZIP file format specification version 4.3 — a wrapper codec 2 excludes (§17.2, T15).
- **[RFC 8878]** Zstandard Compression and the `application/zstd` Media Type — codec 3 and metadata encoding 2 (§17.2, §18.2).
- **[LZ4 Block]** LZ4 Block Format Description, version 1.0 — `doc/lz4_Block_format.md` in the lz4/lz4 repository, as published with lz4 release v1.9.4 — codec 4 (§17.2).
- **[RFC 8259]** The JavaScript Object Notation (JSON) Data Interchange Format — the user-metadata document (§18.2).
- **[RFC 3339]** Date and Time on the Internet: Timestamps — the `tarn.created` key (§18.4).
- **[RFC 9110]** HTTP Semantics — the 200 status code and the range requests `[R-CNT-10]` names for an HTTP transport (§6.4).
- **[Unicode]** The Unicode Standard — UTF-8, and Normalization Form C where §4.6 advises it.

Informative: the OCP OFP8 specification, cited only to pin what
sample-type identifiers 14 and 15 would mean if ever assigned (§12.2).

### Appendix G — Reproducible-writer profile (non-normative)

Core writer conformance is semantic: two conforming writers given the
same input can emit different files (`[R-CNF-05]`). Applications that
need byte-identical output — content-addressed storage, reproducible
builds — can adopt this profile, which closes the degrees of freedom
this format deliberately leaves open. It adds no requirement to any
actor: a writer ignoring it is fully conforming, and conformance to
the profile can be refuted cheaply but confirmed only by reproducing
the file.

1. **Codec 1 (none), or a named codec implementation at a named
   version with fixed encoder settings** — level, strategy, and
   thread count included, since a multithreaded encoder can vary its
   output run to run. This is the profile's real boundary: RFC 1951
   and RFC 8878 constrain what a decoder accepts, not how an encoder
   chooses blocks, matches, or tables, so two conforming encoders
   emit different, equally valid streams for the same input.
   Byte-identity across *implementations* is therefore unattainable
   for codecs 2–4; codec 1 is reproducible by anyone.
2. **`file_id` from a cryptographic hash of the file's own emitted
   bytes**, computed over [0, F − 64) together with the trailer's
   other fields with the `file_id` field taken as zero, then written
   in — the hash a named function at a named version, its input the
   bytes [0, F − 64) followed by the trailer's first 60 bytes with the
   `file_id` field zeroed, and the identifier the digest's **last
   eight bytes in output order** — the eight a named hash emits last,
   read little-endian; naming the end rather than calling them the
   *low* bytes is deliberate, that word being read as a position by
   some and as an arithmetic magnitude by others. The value
   0x0000000000000001 is
   substituted in the measure-zero case that they are all zero
   (§6.2 forbids `file_id` = 0). This is a creator's rule: a rewriter
   adopting the profile takes `[R-WRT-06]`'s fresh draw instead, since
   a derived value is not a draw and re-deriving it on an already-
   compact input would reproduce the input's own `file_id`.
   Deterministic, and high-entropy — satisfying §9.3's advice
   rather than contradicting it, which a counter would not. Hashing
   the bytes rather than an abstract notion of "content" is what
   makes the identifier well defined: this format fixes no canonical
   serialization of logical content, and two files carrying the same
   arrays can legitimately differ in tiling, layout, and codec.
3. **A total emission order, contiguously.** For each layer in
   ascending layer-name byte order, compared as `[R-MTA-05]` compares
   keys: its stored tiles in disk-ordinal
   order, then its tile-index region; then any remaining record
   extents in ascending record order — all of them after every layer's tiles and
   index region, not interleaved with them; then the directory. That
   order runs over top-level records first, then, within each layer
   record, its sub-records; and the directory's own record sequence,
   with each layer record's sub-record sequence, is emitted in that
   same order, so that record placement and record order are pinned
   together rather than one without the other (`[R-CNT-14]` leaves
   order free, which is why the profile fixes it here). Records and a
   layer record's
   sub-records alike are ordered by type; within a type, type 0x0001
   ties by layer name, and every other type by the record's header
   with **extent_offset masked to zero**, then its inline payload,
   then the contents of its extent, compared as `[R-MTA-05]` compares
   keys — the comparison every byte order in this item uses, the
   layer-name tie included.
   extent_offset is masked because this very order is what fixes it:
   a key containing it would depend on its own result, and two
   records of one type could not be placed at all. Every other
   component is a function of content alone, so the key is one a
   reader can derive, which a creation order is not. Two records
   this key does not separate are byte-identical in type, flags,
   lengths, payload and extent content; emitting them in either
   order yields the same file, so the writer chooses. Record order carries no meaning (`[R-CNT-14]`), so it
   is otherwise free to vary, as is structure placement
   (`[R-LIF-02]` step 2). The first structure begins at 16, directly
   after the front signature block, which §5.2 counts as no
   structure — or, where that structure is a stored tile and a declared
   A or A_slab admits none at 16, at the least position above it the
   declaration admits, a structure no declaration constrains beginning
   at 16 like any other; each
   later structure begins where the previous one
   ended, save where alignment forces a gap — a
   declared A or A_slab, or §6.2's 64-byte trailer alignment, the
   pre-trailer pad included — and every byte of every such gap is zero — `[R-CNT-03]`'s advice, taken as a requirement
   here: order alone does not fix bytes while the space between
   structures is free in either extent or content.
4. **One generation**, so that the file is the output of a single
   commit. Appending is reproducible only in the weaker sense that
   the appended bytes are. No field records how many commits a file
   has had, so nothing refutes this item by reading a value: what
   refutes it is §9.6's backward probe finding a superseded trailer
   in the slack that committed-prefix immutability leaves in place.
5. **No declared alignment and no slab**, or fixed declared values —
   both change placement and neither is implied by content. **A fixed
   filter value** likewise: §17.3 leaves the choice to the writer, and no
   content implies it, so two writers agreeing on everything else still
   disagree on bytes without it pinned. The filter is the identity
   exactly where its permutation is — where the stride is 1, as for a
   packed boolean plane, and equally where the decoded image is a
   single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes
   the stored bytes of any tile whose decoded image the permutation
   does not leave unchanged, and where it does, the stored bytes are
   the same under either filter and are no evidence of which was
   declared. **Fixed declared tile
   extents and a fixed layout** likewise, as item 2's closing sentence
   names both:
   §11.3 states that tile extents are a writer's choice and that this
   specification imposes none, and §14.1 leaves the layout to the
   writer. Without both pinned, two writers agreeing on everything
   above still disagree on bytes: the tile extents fix every tile's
   shape and with it the grid count, while the layout fixes how many
   tile-index entries the layer addresses (§11.2) and how each tile's
   values are arranged (§14.2). Where neither effect of the layout reaches the data, as
   §14.4's Note says of a single-channel numeric layer, the layer
   record's own layout field still differs, and the pin is needed for
   that byte.
6. **The sentinel for every all-fill tile**, so that a tile whose
   samples all equal fill is never stored; otherwise two writers
   agreeing on content still disagree on bytes.
7. **The all-zero fill default.** Where a caller chooses no fill,
   the writer records all-zero bytes — `[R-TYP-10]`'s SHOULD, taken
   as a requirement here. This one reaches further than the fill
   field: item 6 stores no tile whose samples all equal fill, so two
   writers that default fill differently disagree about which tiles
   exist, not merely about eight bytes of the layer record.
8. **`version_minor` at the floor** `[R-CNT-26]` states, and
   `flags` = 0. The `flags` half is a creator's rule, as item 2's
   identifier is: a rewriter adopting the profile carries its input's
   unknown ignore-lane bits forward instead, setting no other
   (`[R-CNT-08]`). The
   version_minor floor binds a rewriter too, save where its output
   carries a feature it does not implement, when §20.5's floor governs
   instead (`[R-WRT-06]`). A rewriter's output is therefore
   reproducible only modulo its trailer and the records §20.4 lets it
   drop: `[R-WRT-06]`'s fresh file_id is no function of content, this
   item's floor turns on which features the rewriter implements, and
   a record whose governing flags are MU = 0 and PE = 0 is retained or
   dropped at the rewriter's choice (§20.4), which no item here pins.
   An adopter needing byte-identity
   across rewriters pins the rewriter, as items 1 and 9 pin their
   producers.
9. **User metadata either absent, or serialized by a named JSON
   writer at a named version, at a fixed storage encoding (§18.2) —
   and, where that encoding is 2, by a named zstd implementation at a
   named version with fixed settings, as item 1 pins a tile codec.** `[R-MTA-05]`'s sorted keys make one
   writer's output reproducible but explicitly do not make two
   writers' output identical — number formatting varies by runtime —
   so this degree of freedom closes the same way item 1 does, by
   pinning the producer.

10. **Names normalized to Unicode Normalization Form C**, which
   `[R-ENC-14]` states as a SHOULD. A caller-supplied decomposed name is a
   different name under `[R-ENC-13]`, because its bytes differ — whether or
   not its length differs with them. §4.6's `température` is 12 bytes in NFC
   and 13 in NFD, while a name differing only by canonical reordering is the
   same length in both forms. So a writer that does not normalize emits a
   different layer record.

Everything else the profile needs is already mandatory — fill-encoded
edge padding (`[R-SER-05]`) and explicitly recorded fill
(`[R-TYP-06]`) among them. The items above add what is not, and the
list is not short: gap *content*, which `[R-CNT-03]` only advises;
gap *extent*, which placement freedom (`[R-SLB-05]`) leaves open;
record and sub-record order, which `[R-CNT-14]` leaves free; the fill
a writer records when its caller chooses none (`[R-TYP-10]`, a
SHOULD); the sentinel for every all-fill tile, which no rule requires;
a single generation, which §9 nowhere constrains; the absence or
fixing of a declared alignment and slab, which §16 leaves to the
writer; a fixed filter, which §17.3 leaves to the writer; fixed
declared tile extents, of which §11.3 imposes none; a fixed layout,
which §14.1 leaves to the writer; `version_minor` at its floor, which `[R-CNT-26]` states as a
SHOULD — item 8, binding creator and rewriter alike save §20.5's
carried-feature case, its `flags` half a creator's rule alone; a
derived `file_id`, where §9.3 states only advice; NFC-normalized
names, which `[R-ENC-14]` states as a SHOULD; and the
producer pinning of items 1 and 9. Read the numbered items as the
list; this paragraph names what they are for, not how many there
are.

### Appendix H — Conformance checklists (non-normative)

A summary of each class's obligations, for implementers auditing their
own work. §2.3 defines the classes; each entry's authority is the
requirement or section cited, never this summary.

**Conforming file** — every requirement at every scope holds (§2.4);
bytes partition into the coverage classes (§5.2, `[R-CNT-02]`); every
structure's checksum verifies where §8.1's map states one (§8.1); no
violation row of §21.2–§21.5 applies, though §21.6's defined
conditions can — an experimental-range MU = 0 record being conforming
(`[R-CNT-15]`, §10.2).

**Conforming reader** — validates the trailer in §6.2's order; verifies
each checksum before acting on what it covers (§4.5, §8.2); detects
every reader-assigned violation no later than its tier (§19.2);
implements all four codecs, both filters, both layouts, all
thirteen sample types, both user-metadata encodings, and both
registered record types (`[R-CNF-03]`, §2.3); accepts every conforming
file of a major it implements that carries no top-level MU = 1 record
of a type it does not implement and lies within §21.9's minimum
guarantees, and reports any resource refusal as a limit rather than
as corruption (`[R-ERR-04]`, §21.6); applies
the outcome and scope §21 assigns; never returns padding positions (§11.3) and never returns
fill for a rejected tile (§2.4); returns sample bit patterns unaltered
(§3.2), the sole resolved case (`[R-TYP-04]`, §12.3) being a
nonconforming interleaved boolean byte it chooses to return rather
than reject (`[R-SER-08]`, §14.2).

**Conforming writer** — emits only conforming files (§2.3); records
fill for every channel (`[R-TYP-06]`, §13.1); fill-encodes edge
padding and pad bits (`[R-SER-05]`, §14.5); emits interleaved boolean
values as only 0x00 or 0x01 (`[R-SER-08]`, §14.2); sorts
user-metadata object members by their keys' UTF-8 bytes
(`[R-MTA-05]`, §18.2); follows the commit protocol
including both barriers (§9.2); writes flags = 0 when it creates a
file, a rewriter instead carrying its input's unknown ignore-lane
bits forward and setting no other (`[R-CNT-08]`, §6.3, §20.5); honors
any alignment or slab it declares (§16). Advisory, and not a conformance condition: a writer
SHOULD zero the gaps it creates (`[R-CNT-03]`, §5.2).

**Conforming updater**, an appender or a rewriter (§20.1) — everything
a writer does for the bytes it produces, plus: validates, as an appender, the trailer and full directory, and every
layer it modifies (§20.3), a rewriter's depth being `[R-WRT-09]`'s; as an appender, changes a layer that stores a tile in the
generation its commit supersedes only as §20.3 step 4 permits — its
names, a grown dimension extent, a planar channel list extended at its
end or
shortened from it (not both in one commit), a slab or alignment
declaration declared, changed or cleared —
and makes any other change to it as a new layer or a whole-file
rewrite (§20.3);
re-emits every retained record it does not logically modify
byte-identically, a modified one being new output under its writer
obligations (§20.4, `[R-WRT-05]`); copies forward the input's unknown
ignore-lane flag bits, clears none and sets no other (`[R-CNT-08]`,
§6.3); respects every record's MU and PE bits, the
registry's fixed values governing for a registered type (§20.4,
`[R-CNT-22]`); drops a layer record only under §20.4's PE = 0
licence, its sub-records with it, and never removes a user-metadata
record from a scope it keeps (§20.4); never modifies or drops a layer that carries an unknown critical
sub-record, and rejects outright a file carrying an unimplemented
top-level MU = 1 record (`[R-CNT-15]`, §20.4). A rewriter, in
addition, mints a fresh file_id and follows the creation path
(`[R-WRT-06]`); preserves the content of every structure it carries
forward, re-pointing each extent slot it relocates and regenerating
each tile-index region any of whose stored extents it relocates
(`[R-WRT-07]`); verifies the checksum over every extent it
copies (`[R-WRT-09]`); drops a layer or a PE = 0 record by omitting
it, reclaiming what it addressed, and refuses to rewrite a file
carrying an unimplemented MU = 1 record (§20.5). Advisory, and not a
conformance condition, of an appender and a rewriter alike: an updater
that drops a record SHOULD report the loss (§20.4).

**Conforming verifier** — every reader obligation, plus the checks
readers are exempt from: the live-state coverage partition and the
slack total (§9.7) — reported as partial — an upper bound,
naming the scope or violation that stopped the walk — where its walk
did not complete (`[R-CNT-21]`); extent overlap (§7.2); record flag bits — reserved
bits, MU = 1 with PE = 0, and a registered type's stored bits against
§7.3's registry (`[R-CNT-12]`, `[R-CNT-22]`);
the 16-byte front signature block by byte equality, which
`[R-CNT-04]` lets a reader not holding it resident defer or omit and
§2.3 does not (F1, F6);
no structure between the live directory's end and the live trailer
(`[R-CNT-05]`, F7); a reserved-range record or sub-record type value,
whatever its MU bit (`[R-CNT-15]`, F36, L25);
alignment and slab invariants (§16); decoded-content obligations —
padding samples, pad bits and interleaved boolean bytes (§14.5, §14.3,
§14.2);
user-metadata member ordering (`[R-MTA-05]`, §18.2); certifies only
files with no violation at any scope (§2.4) — a user-metadata
record at an experimental-range encoding is no violation and no bar,
and is instead reported: owning scope, encoding value, stored extent
length (`[R-MTA-10]`) — encoding 0 and the reserved range stay
violations (R1); reports *nonconforming*
whenever it has established a violation, reserving *cannot
establish* for a traversal that established none; and reports each
requirement it was unable to check on a capability or resource
ground, and each scope it did not examine (`[R-CNF-11]`).
