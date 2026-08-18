# 0069. Byte order is not a file state

- Status: Accepted
- Date: 2026-08-16
- Covers: the cause-row family (F1, F5, L3, T27); L50's instance arithmetic;
  `[R-WRT-06]`'s voice and the compactor's refusal; the third field class
- Confirm: resolves the tension between ADR-0057 and ADR-0065/ADR-0067

## Context

Cleanroom round 9 left four decisions. Working them up turned the first one
inside out, and the maintainer's question is what did it: *the format is
little-endian only, so how can byte order be history?*

It cannot. `[R-ENC-01]` reads *"All multi-byte values in a TARN file … **are**
little-endian"* — the definition of the encoding, not a constraint a file can
fail. There is no big-endian variant, so *"this field is stored big-endian"*
is not a state a file can be in. A writer that byte-swaps `E₀ = 2` does not
emit "a big-endian 2"; it emits the value 2⁵⁷, and the mandatory
little-endian parse reads exactly that. Nothing distinguishes it from a writer
that meant 2⁵⁷.

The prohibition lives in the next requirement — `[R-ENC-02]`, *"writers MUST
NOT emit big-endian values"* — and `[R-CNF-02]` already governs that shape:
*"conduct rules bind the actor, the predicate binds the bytes."*

Field width is the same. `[R-ENC-06]` fixes every width, so *"fields at other
widths"* is not a state either: the parse is always at the fixed widths, and a
mis-widthed write simply yields different values at them.

## Decision

**The cause-row family is retired: F1, F5, L3 and T27 leave the register.**

Each registered a *writer's mistake* as a file-scope condition, which is the
category error ADR-0067 struck as F21 one commit earlier — F21 registered a
reader *capability*, these register writer *conduct*. Neither is a
file-conformance violation, and §21.1's completeness clause — qualified by
ADR-0066 to *"every detectable **file-conformance** violation"* — therefore
never obliged them. Nothing is missing from the register; the values these
writers produce are caught by the rows for the fields that hold them, each of
which already carries its own vectors.

**This settles a contradiction that has stood since ADR-0057**, which held
that *"a register row must describe a state a detector can observe, not the
history that produced it"* and deleted three rows on that ground, while
ADR-0065 kept F5/L3 and ADR-0067 added T27. ADR-0057 was right, and its rule
now applies uniformly. T13 and T26 survive it: a deflate stream with an
over-large history window and a mis-strided filter image whose result breaks
§14.5 are observable states, merely observed through another row's procedure.

**F2 survives.** A signature is a *fixed constant*, so byte-reversed magic is
observably not the magic — a real state, with a real reader outcome in
`[R-ENC-02]`.

**L50 — now L49 — splits four ways.** The instance held back in round 9 is
constructible after all: §7.3 fixes the layer record at MU = 1, PE = 1, and
`flags = 0x0000` clears both bits, exhibiting L49 twice and no other row.
`[R-VEC-02]`'s isolation clause is stated over *rows* — *"a vector is
constructed so that one row is the one it exercises"* — not instances.

**`[R-WRT-06]` is restated in the conduct voice** §20.1 already uses, and the
compactor's refusal is named. §20.1 had settled this: creators carry the flat
`[R-CNF-05]`, while an appender and a compactor satisfy writer requirements
*"for the bytes they produce"* and *"a violation latent in a structure they
neither modify nor rely on travels with it."* `[R-WRT-06]`'s opening was the
one sentence written as a predicate on output, asserting a property no
available conduct guarantees, since `[R-WRT-09]`'s depth is structural and
never decodes.

**The third field class is populated and renamed `descriptive`.** It was never
empty — its one member was mislabelled. `version_minor` is the only field
whose valid-range cell reads *"any"*, the only one `[R-CNT-07]` forbids a
reader to reject on (*"all feature gating is structural"*), and the one
`[R-CNT-26]` says *"misstates the file's feature floor to tooling"* — which is
the class definition's second clause almost verbatim. `[R-ENC-16]` is rewritten
as a disjoint cascade over what a field's *value* determines, since the old
"never affects decoding" was satisfied by every semantic field too. The rename
also clears the collision with Appendix F's IETF sense of *informative*, and
was free only while no table cell carried the label.

## Consequences

The register goes to **121 conditions over 248 instances** and the corpus to
**300 vectors**, 100% row and per-instance coverage: −4 conditions and −8
instances from the retirement, +2 instances from L49's split.

Eight vectors retire with their rows (TV-0101–TV-0104, TV-0114, TV-0115,
TV-0210, TV-0953); TV-0955 and TV-0956 are new. **Two corpus defects found in
passing are repaired**: TV-0929 claimed L50 while built on an experimental
0x8001 sub-record the registry does not reach — it now builds on the 0x0002
seed — and TV-0954, added in round 9, served a layer `[R-CNT-18]` obliges a
reader to refuse.

**F- and L-rows renumber**: F1 and F5 leave, compacting 36 rows; L3 leaves,
compacting 47. T27 was last, so T-rows do not move. 641 references shifted in
a single pass across the spec and eight vector-definition modules. Earlier
ADRs and the round 1–9 cleanroom findings keep their old numbers, per
ADR-0002's supersede-never-rewrite rule.

Priced knowingly. This is the second row renumbering in four commits, and it
reverses T27, added two commits ago on the reasoning this ADR overturns. The
corpus loses eight files that exercised realistic writer errors — each reached
a gate that keeps its own vectors, so no *condition* loses coverage, but the
byte-swap and mis-width recipes are gone as recipes. `[R-ENC-01]` and
`[R-ENC-06]` now carry no register row and are dispositioned in the
completeness heuristic instead, which is the honest place for a rule no file
can exhibit.

## Precedent

- ADR-0057's shape rule, applied uniformly for the first time.
- ADR-0067's strike of F21, whose reasoning this extends from reader
  capability to writer conduct.
- `[R-CNF-02]`'s conduct-versus-predicate split, which supplies the test.
- ADR-0046: the specification governs and a disagreeing vector is corrected —
  the authority for retiring eight vectors and rebuilding TV-0929.
