# TARN Specification Plan

How this specification is being built: what "done" means, in what order the
work happens, and the process rules that keep the result honest.

## 1. Purpose and success criteria

TARN 1.0 ships when these gates pass — each is testable, none is marketing:

- **G1 — Afternoon-readable.** A competent engineer reads the entire
  normative spec in one sitting.
- **G2 — Weekend-implementable.** A minimal conforming reader (no
  compression, no slabs) can be written from the spec alone, without
  consulting any reference implementation.
- **G3 — Cleanroom-clean.** The final cleanroom round (§6) yields zero
  byte-level ambiguities.
- **G4 — O(1) remote open.** The spec's normative cold-read accounting is
  demonstrated against a dumb HTTP server, with request counts matching the
  stated guarantee.
- **G5 — Every error has a vector.** Every row of the spec's error register
  has a conformance vector with an expected verdict.

## 2. Scope and non-goals

Deliverables of this repository: the specification, the ADR trail
([docs/decisions/](docs/decisions/)), the ID registries, and the conformance
test-vector corpus. Explicitly out of scope: implementation code (a reference
implementation will live in a separate repository), and any new format
feature that has not first appeared in
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) as a proposal.

Two rules keep spec and implementations honest:

- The spec repo never depends on any implementation.
- A reference implementation MUST NOT enforce constraints the spec does not
  state — divergence between "valid per spec" and "valid per the reference
  reader" is a spec bug (see the QOI case study in
  [docs/research/reference-format-lessons.md](docs/research/reference-format-lessons.md)).

## 3. Design inputs

- [docs/research/reference-format-lessons.md](docs/research/reference-format-lessons.md)
  — distilled lessons from PNG, TIFF, Zarr v3, PMTiles v3, and QOI/BCP 14,
  cited throughout the ADRs.
- The seeded decision set: ADRs
  [0001](docs/decisions/0001-record-architecture-decisions.md)–[0016](docs/decisions/0016-licensing.md).
- The open-decision ledger: [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).

## 4. Decision process

ADR lifecycle: Proposed → Accepted → Superseded (never edited in substance).
Every OPEN-QUESTIONS entry resolves into exactly one ADR. Spec text may only
encode Accepted decisions. After the first draft exists, every spec change
lands via a pull request that links its governing ADR, and the changelog
records the link.

## 5. Phase 2: drafting order

**Step 0 — resolve the structure-shaping subset of the ledger in dependency
order:** Q-A2 (mutability) → Q-A1/A3/A4 (placement, budget, depth) → Q-B2
(linearization) → Q-B1/B3/B4 (slabs, planar order, dedup) → Q-C1/C2
(checksum algorithm and domain) → Q-D4 (sentinel) → Q-E3 (index encoding) →
Q-G1/G2 (versioning, flags). The remaining [blocking] and [shaping] entries
resolve in or before the batch that drafts their section, per each entry's
"What settles it"; no section is finalized with one of its entries open.

Then draft the single normative document (`spec/tarn.md`), one batch at a
time, each batch followed by conformance vectors and — at the marked points —
a cleanroom round (§6):

| # | Batch | Contents |
|---|-------|----------|
| 1 | Conventions & conformance skeleton | BCP 14 boilerplate, normative/non-normative demarcation, conformance classes (file / reader / writer / updater), actor-naming house rules, requirement IDs |
| 2 | Data model | Layers, dimensions, tiles, linearization, the noun set (channels and fill introduced as vocabulary, specified in Batch 5); the *reference array* defined as the conformance target |
| 3 | Container | Signature, discovery structure, directory, byte-coverage rule, mutability/consistency contract |
| 4 | Tile index and slabs | Entry layout, sentinels, alignment invariants, exhaustive invalid-state enumeration; §16's non-normative scoping note (slabs guarantee contiguity; linearization defines adjacency; rectangle locality is the reserved curve door); discharge ADR-0005's alignment-values Confirm |
| — | **Cleanroom round 1** | Container + index text only |
| 5 | Sample types and fill encodings | Closed type list, bit-exact fill, boolean packing |
| 6 | Tile serialization | Both layouts, worked byte examples, edge-tile padding |
| — | **Cleanroom round 2** | Byte-level quiz: planar offsets, edge tiles, unstored-tile reads |
| 7 | Codecs and filters | Pinned external references, independence rule, shuffle; the verifier's conformance class facing an unimplemented-but-assigned codec, and stored-size bounds (cleanroom round 2) |
| 8 | Reading a TARN file | The normative numbered read algorithm, including fill and checksum-failure paths; fixes eager-vs-lazy validation timing (cleanroom gate 1, reader ambiguity 4), duplicate-name detection timing, and multi-segment planar-read accounting (round 2) |
| 9 | Writing and updating | Writer tiers, updater obligations, append procedure; byte-identical re-emission of retained records, appender verification depth, and compaction generation-renumbering-from-1 (cleanroom gate 1 findings) |
| 10 | Error-handling register | The consolidated violation × outcome table |
| 11 | Security and privacy considerations | Named threat classes; deletion ≠ erasure; compaction; the limits table (Q-H1) — entry_count bound for CRC-array growth, the checksum-uncovered-padding note (round 2), and the zstd minimum-supported-window row (Batch 7) |
| 12 | Extensibility and registries; user metadata | Flags, ID spaces, version semantics, the enumerated extension surface; the user-metadata document (ADR-0015, Q-F1/F3) |
| 13 | Conformance checklists, vectors, appendices | Per-class checklists; annotated hex dump of a minimal file; constants table; normative references |
| — | **Cleanroom round 3 (acceptance)** | Full spec; G1–G3 evaluated as pass/fail |

Cross-cutting obligation: the undefined-behavior worklist below is tracked as
a table, each item mapped to the section that must discharge it, so none is
silently dropped.

### Undefined-behavior worklist

Truncated files and short reads · torn writes and partial appends (detection
and recovery) · checksum mismatch per structure · unknown codec/field values
and forward-compatibility rules · duplicate/invalid names, allowed
characters, UTF-8 rules, length limits · zero-size dimensions, zero
channels, empty layers · integer overflow in index math and mandatory
reader-side limits (decompression bombs, allocation caps from untrusted
headers) · overlapping or out-of-bounds tile offsets in hostile files ·
fill-value representation per type, NaN and −0.0 semantics, statistics
semantics · bit order for packed booleans · padding byte contents · version
negotiation.

## 6. Cleanroom protocol

A fresh-context agent receives ONLY the spec text drafted so far — no
conversation history, no ADRs, no this-file. It must (a) describe how it
would implement a conforming reader, (b) answer a fixed slate of byte-level
questions, and (c) list every ambiguity it hit. Every ambiguity is treated as
a spec bug and fixed before the next batch. Artifacts (prompt, transcript,
findings, resulting spec diffs) land in `docs/cleanroom/`. The full
protocol — four parallel roles, the access rule, finding taxonomy, pass
criteria — is pinned in ADR-0034, as piloted on the container round
(docs/cleanroom/01-container/).

## 7. Conformance vectors

Vectors are authored *alongside* each section, not after the fact: valid
files with expected decoded contents (float values as hex bit patterns), and
invalid files with required verdicts drawn from the outcome classes of
[ADR-0003](docs/decisions/0003-spec-conventions-and-conformance.md). Every
sentinel, boundary, and error-register row gets at least one vector.

## 8. Risks

- **Ambiguity debt at freeze** (the satellite-technote failure mode) →
  gate G3.
- **Spec/reference-implementation drift** (limits living in code) → the §2
  rules plus vectors as the contract.
- **Scope creep in codecs and types** → closed-list discipline; additions
  require an ADR and a registry entry.
- **Single-maintainer bus factor** → everything lives in-repo; no
  out-of-band state.

## 9. Milestones

- **M1** — Phase 1 scaffolding merged. *(Reached.)*
- **M2** — The structure-shaping subset (§5 Step 0) resolved as ADRs.
  *(Reached.)*
- **M3** — Batches 1–4 drafted; cleanroom round 1 passed. *(Reached;
  round 2 passed after Batch 6.)*
- **M4** — Full draft; all vectors authored. *(Draft complete: all 24
  sections and Appendices A–H are written, and the decision ledger is
  fully resolved into ADRs 0001–0047. Vectors outstanding — §24 fixes
  the corpus contract, the corpus itself is the remaining work.)*
- **M5** — Gates G1–G5 pass → 1.0-rc. *(Next: cleanroom round 3
  evaluates G1–G3; G4 and G5 follow the corpus.)*
