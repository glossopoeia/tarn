# 0075. Document rules attach only under assigned encodings

- Status: Accepted
- Date: 2026-08-19
- Covers: verifier verdict at an experimental user-metadata encoding;
  `[R-MTA-10]`; the scope of §18.2's document rules
- Confirm: none

## Context

Cleanroom round 12 escalated a case no rule decides: the verdict a
conforming verifier reports for a **conforming** file whose user-metadata
document is stored under an encoding the verifier does not implement.

The case has exactly one shape. Encodings 1 and 2 are core — software
that cannot decode them is not a conforming reader (`[R-CNF-03]`), and
verifiers inherit every reader obligation — and encoding 0 or a
reserved value 3–0x7F in a file is already a violation (row R1). What
remains is an experimental value (≥ 0x80), which §21.6 and `[R-EXT-03]`
make conforming: the metadata-encoding space is the only identifier
space where an experimental value in a file is not a violation, so it
is the only place a conforming verifier can meet a conforming file it
cannot fully decode.

The two texts nearest the case pull in opposite directions, and neither
reaches it. `[R-MTA-09]` fixes *cannot establish* for a verifier that
declines a decode **on the size bound** — an assigned encoding, a
spec-defined document, a verifier merely under-resourced. §17.4's
`[R-COD-11]` fixes *cannot establish* for a codec the verifier cannot
execute — but an unknown codec value is itself a layer-scope violation
(L43/L45), so that verdict never actually governs a conforming file.
Meanwhile §21.7 holds that a requirement with no file-level witness is
not one a verifier is "unable to check," and §9.7 holds that a verifier
must not certify past a violation it has not looked for. Nothing
arbitrated.

## Decision

**The document rules of §18.2 — the frame constraints, the
decoded-document restrictions, and `[R-MTA-05]`'s member ordering —
attach to a document only under an encoding this specification
assigns.** Under an unassigned encoding this specification defines no
decoding, and §10.3 lets two unrelated experiments claim the same
value with different meanings, so "the decoded document" names nothing
this specification can test. File conformance is a pure predicate on
bytes (`[R-CNF-02]`); a predicate whose truth depends on which private
decoder one holds is not one. What remains checkable is everything
structural, and it all still applies: the record's framing and extent
slot, the encoding byte's own value set, and the extent's terminal CRC.

**A verifier meeting such a record in an otherwise conforming file
certifies.** It has no requirement it is unable to check — the case is
not among `[R-CNF-11]`'s cannot-establish grounds — **and it MUST
report each record it ignored on this ground**: owning scope, encoding
value, stored extent length. The report is the counterpart of the
slack total: bytes a certificate covers without inspecting are counted
and named, never silent. New requirement `[R-MTA-10]`.

The design was already committed to this answer in three places. The
user-metadata record type is registry-fixed MU = 0 — a writer cannot
declare a file not understandable without its metadata — where the one
precedent for *cannot establish* on a conforming file, the
experimental MU = 1 record, is precisely the writer declaring the
opposite. The quarantine (`[R-MTA-02]`) guarantees the document cannot
affect where any byte lives or how it decodes, so the verifier vouches
for everything the file's structure means without it. And slack
(`[R-CNT-21]`) is the standing template: unconstrained bytes inside a
certified file, priced by a mandatory report.

## Alternatives rejected

**Cannot establish** (extend `[R-MTA-09]`'s pattern). Rejected on three
grounds. It is permanent and universal: no capability upgrade cures it,
because §10.3's no-collision-protection means no decoder is ever
authoritative, so the verdict would stop recording a verifier's limits
and start recording a property of the file — every other ground varies
by verifier. It reclassifies a no-witness case as unable-to-check,
which §21.7 expressly refuses for the content-correctness class, so
§21.7 would need re-scoping to survive it. And it prices a ~30-byte
record at permanent uncertifiability of arbitrarily large valid data.
The honest cost of rejecting it: a conservative verifier that
generalized "cannot decode → cannot establish" from `[R-COD-11]` and
`[R-MTA-09]` is now nonconforming on this file, and the certificate
covers a live extent no conforming implementation can inspect —
mitigated, not removed, by the mandatory report.

**Close the space** (make experimental metadata encodings a violation,
as every other value space does). Rejected because it reverses
`[R-EXT-03]`'s deliberate carve-out — "ignore-record under the
quarantine, never a scope-level rejection" — one release after twelve
cleanroom rounds validated it, and because it makes every trial file
of a private encoding experiment nonconforming, which is exactly the
use the experimental range exists to absorb. It was the only option
that removes the uninspected-extent residue entirely, and that residue
is instead priced in §22.3's inventory.

## Consequences

`[R-MTA-10]` lands in §18.2, and the rule it states is swept through
every restatement surface: `[R-CNF-11]`'s ground list gains the
contrast, §21.6's row cites the new rule, register row R3's condition
is scoped to assigned encodings, §21.5's quarantine preamble routes
the unassigned case to §21.6, §9.7's certify-past-a-violation sentence
gains the nothing-to-look-for gloss, §17.4 names the one space that
differs from its codec rule, §22.3's residue inventory grows from
three to four, and Appendix H's verifier checklist carries the report.

The register is unchanged: no new row, because the rule creates no new
file condition — the experimental encoding stays §21.6's defined
non-violation, and the report is verifier conduct, on the same
`[R-CNF-02]` footing as every other conduct rule. Corpus unchanged:
121 conditions over 248 instances, 300 vectors; TV-0504/0505 already
pin the conforming files, and their expected verdict is what
`conforming: true` has always meant. The manifest records no verdict
or report axis today; if one is ever added, these two vectors are
where the `[R-MTA-10]` report expectation lands.

Priced knowingly. A certified file can carry a reachable extent whose
content only its private experiment can read, guarded by a CRC that
detects corruption but authenticates nothing (§4.5), and a pipeline
that treats *conforming* as *inspected* inherits that gap — §22.3 now
says so where the residues are inventoried. An operator who wants no
such bytes rejects on the verifier's `[R-MTA-10]` report line, which
is policy above conformance, where it belongs.

## Precedent

- Slack (`[R-CNT-21]`): certification coexisting with
  unconstrained-by-design bytes, priced by a mandatory count-and-report.
- The unknown experimental MU = 0 record (`[R-CNT-15]`, §21.6): payload
  content unconstrained, file conforming, certificate unaffected — the
  same shape one layer down.
- PNG's ancillary chunks: a checker certifies a file whose private
  ancillary chunks it cannot interpret, and prints them; interoperable
  content rules bind only what the specification itself defines.
