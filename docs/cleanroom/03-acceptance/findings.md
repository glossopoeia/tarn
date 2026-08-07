# Cleanroom round 3 — findings, disposition, and gate verdicts

**Verdict: G2 PASS · G3 FAIL-then-fixed, re-run required · G1 evidence
positive, judgment reserved.**

Five fresh-context roles worked the complete document from
`spec/tarn.md` alone. The quiz scored **15/15** against a key derived
independently and verified computationally before the round —
including the whole-document probes added for acceptance (the
metadata quarantine's `1e400` case, the experimental-codec scope, the
unknown-MU-record split across file and layer scope, the
rank-32/rank-40 acceptance boundary, and Appendix A's actual trailer
CRC). The reader and writer both reported **IMPLEMENTABLE: yes** at
high confidence with zero byte-level ambiguities; the verifier and
navigator reported **qualified**, with three and two respectively.

## Gate G2 — weekend-implementable: PASS

The reader role produced a complete byte-precise plan for a minimal
conforming reader (codec 1, no slabs, no alignment) and confirmed it
could be built from the text alone. Its most useful observation is
one the drafters had counted on without stating: because sample
values are bit patterns a reader must not alter (`[R-MDL-02]`,
`[R-TYP-04]`), the thirteen sample types collapse on the read path
into a thirteen-entry element-size table — no IEEE 754 arithmetic, no
NaN logic. That is what keeps the type system free for a reader.

The writer role produced a byte-exact one-layer file, an append, and
a compaction, also at **yes**/high.

## Gate G3 — zero byte-level ambiguities: FAIL as run; all five fixed

Five distinct byte-level ambiguities were found — each one a case
where two permitted readings accept or produce different bytes. All
five are now fixed, but **G3 cannot be claimed from this round**: the
gate asks for a round that finds none, and a re-run against the
amended text is required before it passes.

| Byte-level ambiguity (reporter) | Fix |
|---|---|
| §9.7(a): when several candidate sets form a chain, which one is *the* selected chain? Steps (b)–(d) can succeed for one and fail for another, so a payload that mimics a trailer could make certification verifier-dependent — contradicting `[R-CNF-02]` (verifier) | §9.7(a) now states the search explicitly: coverage is established if *any* qualifying chain yields the complete partition, and fails only when none does |
| Do §6–§18's requirements bind structures in superseded generations? Reachable-only vs. every-generation readings differ on whether a file certifies (verifier) | New `[R-LIF-09]`: superseded structures are checked to §9.7's stated depth and no further; a malformed record in a generation no reader is permitted to consult does not make the file nonconforming |
| May a layer declaring neither alignment nor slab leave gaps between its structures? `[R-SLB-05]`'s placement freedom reads as absolute; `[R-CNT-02]`'s coverage classes admit declared padding only where alignment or a slab creates it (verifier, writer) | `[R-SLB-05]` now scopes the freedom to ordering and relative position, and states that such a layer leaves no gap |
| Is `generation` bounded? §6.2 gives "≥ 1" with no ceiling; `[R-ENC-03]` caps every *count* at 2⁶³ − 1 and §3.1 calls generation a counter (navigator) | §6.2's trailer table now states 1 ≤ generation ≤ 2⁶³ − 1 |
| A user-metadata extent of length < 5 passes every `[R-CNT-13]` slot test but makes §8.1's "final 4 bytes … the preceding bytes" decomposition impossible (navigator) | `[R-CNT-25]` now makes extent_length < 5 on a user-metadata record a validity error at its containing scope |

## Contradictions found and fixed

| Contradiction | Fix |
|---|---|
| `[R-MTA-06]` says a file carrying an unrecognized `tarn.` key is **conforming**; §21.6's register row said the file is **nonconforming** (writer, quiz) — introduced by Batch 12's own fix | The register row now reads *conforming*, matching the rule |
| `[R-CNF-02]` makes conformance a pure predicate on bytes, but `[R-EXT-03]` and `[R-MTA-06]` condition writer obligations on context — "in released software", "the registry version they target" (verifier) | §2.3 now distinguishes conduct rules, which bind the actor, from the predicate, which binds the bytes; a file is never nonconforming by virtue of a conduct rule |

## Further findings fixed

- **Compactor `version_minor` was unassigned** — `[R-CNT-26]` gives a
  writer floor and an appender maximum; a compactor is neither
  (writer). Now: the greater of the floor and the input's minor,
  since a compactor cannot know which minor defined an ignore-lane
  bit it does not implement.
- **Scope of a resource refusal** was undefined — may a reader
  decline the whole file over one over-guarantee layer? (quiz). Now
  stated: the file, or the narrowest scope that exceeds it.
- **"At file scope blocks file-scope modification entirely"** left
  unclear whether an appender may commit at all to a file carrying an
  unknown top-level MU = 1 record (quiz). Now: file-scope *structure*
  is blocked; a commit changing only a layer's own tiles, index, or
  record remains permitted.
- **"A new file_id"** — fresh draw, or merely provably different?
  (quiz). Now: a fresh draw under §9.3.
- **The 128-byte minimum lived only in an Example**, while register
  row F8 cites it as a violation (writer). Now normative,
  `[R-CNT-27]`.
- **§16.1 restated alignment A's constraint without its 2⁶² ceiling**
  (navigator). Now complete.
- **"A compactor preserves content, never placement"** parses as a
  prohibition on preserving placement (writer). Reworded.
- **The top-level record sequence lacked the explicit no-residue
  clause its sub-record sequences have** (quiz). Added for parity.
- **The pre-trailer pad's length when the directory already ends on a
  64-byte boundary** — zero-length or a full 64? (writer). Now
  stated: none at all.

## Gate G1 — afternoon-readable: evidence positive, judgment reserved

Measured: **23,279 normative words** (excluding §1, quoted
Note/Example/Rationale blocks, and the non-normative appendices),
158 requirements, 24 tables, across 24 sections and 8 appendices —
roughly two hours at technical-prose pace, longer with the tables.

The navigator found the spine coherent and the three lookup questions
an implementer actually asks — *what happens when X is malformed*,
*how big is this structure*, *what does this enum value mean* —
answerable without linear reading, via §21's register, Appendix B,
and §10.2 respectively. It flagged the densest passages as §9.7's
coverage verification, §15.3's entry-validity table, and §14's
layout arithmetic.

A final G1 verdict is the maintainer's: it is a claim about a human
reading, and no agent can make it. What this round establishes is
that the document is the right *size* for the claim and is navigable
enough that a reader need not hold it all at once.

## Implementer notes (no spec change)

The reader independently recomputed all four fixed CRC constants from
§4.5's stated parameters and reproduced every one, and re-derived
every worked example in the document. The verifier's audit of §21's
register against its own procedure found the register's coverage
claim holding in both directions. Two roles independently observed
that the specification has no worked example of a *complete layer
record's* bytes — the minimal file in Appendix A has none — and
suggested one; that is recorded as a corpus obligation (§24) rather
than a spec change, since the vectors will supply it.
