# Cleanroom round 1 — findings and disposition

**Verdict: PASS with findings.** All four fresh-context implementers
produced correct, citation-grounded implementations of the container
from the spec text alone. The quiz scored **15/15** against the
independently derived answer key, including the deliberate trick
questions (the two-actor 92-byte-gap split; the transport-size
mismatch whose end-of-file trailer is also a §9.6 mimic; the
validation-order rationale). The reader confirmed the codec-free
implementability claim from the text; the writer produced a correct
128-byte minimum file and torn-recovery walk; the verifier's worked
generation-3 trace matched the intended attribution semantics exactly.
Every reported confusion was treated as a spec bug per PLAN §6.

## Findings fixed in the spec (this round)

| Finding (reporter) | Fix |
|---|---|
| "Verifier" used normatively but never defined as a class (verifier) | §2.3 gains the verifier class; verifiers/updaters inherit reader obligations `[R-CNF-11]` |
| Whether any-scope violations defeat file conformance; whether a reader may reject a nonconforming file on verifier-level checks (verifier, quiz) | §2.4: conformance = violation-free at every scope; outcome classes are reader blast radius; readers MAY reject nonconforming files `[R-CNF-12]` |
| CRC of empty input only derivable, never stated (reader, verifier) | §4.5 states `CRC-32C(zero bytes) = 0x00000000` normatively |
| `[R-ENC-10]` vs magic-before-CRC ordering: "acting on" undefined (quiz) | §4.5 defines *acting on* (allocate/seek/fetch/branch; validation comparison excluded; explicit orders govern) |
| "Sole exception" false for checksum fields themselves (quiz, verifier) | `[R-CNT-19]`/§4.5 wording: checksum fields verified by comparison, covered by no further checksum |
| Trailer/front-block owning scope never stated (writer) | §6.2 states it (file scope) |
| EOF payload-mimic passes trailer checks — caught later, never said (writer) | §6.2 Note: caught at the directory CRC; detection never silent |
| Ignore-lane bits vs "MUST write flags = 0": file conformance unclear (quiz) | `[R-CNT-08]`: set ignore-lane bits are later-minor-defined, files carrying them conforming |
| version_minor writer rule missing entirely (quiz, writer) | `[R-CNT-26]`: lowest-defining-minor SHOULD, appender max rule, consequence stated |
| Stored-flag mismatch on a known type: conformance status unstated (quiz, verifier) | `[R-CNT-22]`: file nonconforming; readers still process under fixed semantics |
| User-metadata encoding 0 / unassigned outcome; inline-vs-extent placement (verifier) | `[R-CNT-25]`: document lives in the extent, (0,0) invalid; encoding 0 or unimplemented → ignore-record + report |
| index_encoding experimental range carve-out ambiguous (reader, verifier) | §7.4 row: any value ≠ 1, including reserved and experimental ranges, → reject-layer |
| Channel type had no parse-time floor (reader) | §7.4: type u16 (0 invalid) |
| Field packing only inferable (reader) | `[R-CNT-18]`: packed, no inter-field padding, stated |
| Normative sentences cited ADRs unreadable in cleanroom (reader) | ADR citations removed from `[R-CNT-11]`/`[R-CNT-20]` normative text |
| §9.7 chain rule flunks conforming files containing trailer mimics with duplicated generation numbers (verifier — contradiction) | `[R-LIF-08]`(a): chain selection anchored at the live trailer; failure only when no consistent chain exists |
| Intra-layer overlap: reject-layer (`[R-CNT-13]`) vs file-scope coverage failure (§9.7) (verifier — contradiction) | `[R-LIF-08]`(c): intra-layer double claims carved out to `[R-CNT-13]`'s outcome |
| Dead-generation candidates' validation bounds and file_id continuity unstated (verifier) | `[R-LIF-08]`(a): candidates validated per `[R-CNT-06]` against their own F_k; same file_id across the chain |
| Dead payload/extent verification depth unstated (verifier) | `[R-LIF-08]`(d): claimed stored-tile and record extents included |
| Front block's durability unowned at creation (writer) | §9.2: covered by the step-4/6 barriers |

## Findings deferred, with owners

- Eager-vs-lazy validation timing → §19 (Batch 8; PLAN row updated).
- Byte-identical re-emission of retained records; appender
  verification depth for untouched layers; compaction renumbers
  generations from 1 → §20 (Batch 9; PLAN row updated).
- Codec, channel-type, element-size, sentinel, and segment-layout
  value sets → correctly identified as forward references into
  reserved §12/§15/§17 (Batches 4–7).
- Generation-count arithmetic bound (g ≤ (F−16)/64) as a cheap sanity
  check → limits-table candidate (Batch 11).
- The §5.1 minimum file and the quiz's byte answers → conformance-
  vector candidates (Batch 13).

## Implementer notes (no spec change)

The reader implemented no §9.6 machinery at all ("the reader has no
fallback path by design") — the intended simplification, observed
working. The writer independently derived that a zero-*stored*-tile
layer still carries a 24-byte index region when it has one addressed
tile, and that structures must pack exactly when no alignment is
declared — both correct and intended.
