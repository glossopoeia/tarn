# 0047. A non-normative reproducible-writer profile

- Status: Accepted (resolves Q-I1)
- Date: 2026-08-06
- Covers: what byte-identical output requires of a writer; where the
  profile lives and why it is not core conformance
- Confirm: none

## Context

Content-addressing and reproducible builds want identical input to
yield identical bytes, but core writer conformance is deliberately
semantic (ADR-0003): promising canonical bytes would constrain every
writer forever, and `[R-CNF-05]` says outright that two conforming
writers may produce different conforming files. Drafting the profile
surfaced a harder limit than the ledger anticipated — cross-
*implementation* reproducibility is unattainable for compressed
tiles, because two conforming DEFLATE encoders emit different, equally
valid streams for the same input. A profile can therefore promise
reproducibility only under codec 1, or under a named codec
implementation at a named version.

It also has a real conflict to resolve. §9.3 asks writers to draw
`file_id` from a cryptographically random source, precisely what a
reproducible build cannot do.

## Decision

A non-normative **Appendix G** states the profile. A writer claiming
it fixes every degree of freedom this format leaves open:

- **Codec 1 (none), or a named codec implementation and version** —
  the honest boundary, stated rather than papered over.
- **`file_id` derived from a cryptographic hash of the file's logical
  content**, which is deterministic *and* high-entropy, satisfying
  §9.3's advice rather than contradicting it.
- **Tiles emitted in disk-ordinal order; records in a fixed order**
  (layer records by layer name, sub-records by type), since record
  order carries no meaning (`[R-CNT-14]`) and is therefore free to
  vary without the profile.
- Everything else the profile needs is already mandatory: zero
  declared padding (`[R-CNT-03]`), fill-encoded edge padding
  (`[R-SER-05]`), explicitly recorded fill (`[R-TYP-06]`), sorted
  metadata keys (`[R-MTA-05]`).

The profile is not a conformance class: a writer that ignores it is
fully conforming, and a reader cannot tell whether a file was
produced under it except by reproducing it.

## Consequences

Reproducible-build and content-addressing users get one profile
instead of inventing several incompatible ones, and the format keeps
its semantic writer conformance. The appendix is short because the
specification had already fixed most of the non-determinism —
writing it was largely an audit confirming that. Foreclosed: nothing;
the profile adds no requirement to any actor.

## Precedent

- ADR-0003's semantic writer conformance, which the profile is
  scoped around rather than against.
- Reproducible-builds practice: pin the toolchain, derive identifiers
  from content, order what is otherwise unordered.
- `[R-CNF-05]`'s explicit refusal to promise canonical bytes, which
  is why this is an appendix and not a requirement.
