# 0063. Standardized key placement and value shape are advisory

- Status: Accepted
- Date: 2026-08-11
- Covers: whether a standardized key outside its listed scope, or carrying a
  wrongly shaped value, makes a file nonconforming
- Confirm: none

## Context

`[R-MTA-07]` declared that *"A file carrying a standardized key outside its
listed scope is nonconforming, and a verifier detects it"* — while §21 carried
no row for the condition, which cleanroom round 7 reported as its most
substantive finding. §21.1 makes register completeness normative, so the
document named a detectable violation and then omitted it from the register
that claims to enumerate every one.

The obvious repair was to add the missing rows: two of them, file-scope and
layer-scope twins of the pattern F30/L49 already uses for the same documents,
taking the register to 127 conditions over 246 named instances and owing four
new vectors. Three things argued against it, and the strongest is in §18.4
itself.

## Decision

**Placement and value shape are writer guidance, not validity.**

- A writer **SHOULD** emit a standardized key only within the scopes its row
  lists, and only with a value of the shape its row gives.
- A reader **MUST** ignore a key outside its listed scope, or whose value does
  not match its row's shape, rather than rejecting the document — unchanged.
- Neither bears on validity. The file stays conforming, exactly as it does for
  an unrecognized `tarn.`-prefixed key, and §21.6 gains one row saying so.

Round 7's finding is therefore resolved by removing the violation rather than
registering it. That is legitimate on the register's own terms: §21.1's
completeness binds the *detectable violations this specification names*, so a
condition the document declines to name owes no row.

**Why relax rather than register.**

*§18.4's own Note asks for it.* The Note explains that statistics live in
metadata *"rather than as a structural record whose staleness would need rules,
verifier obligations, and an updater's attention."* Material is placed in
metadata precisely to escape verifier obligations; attaching one to a metadata
key cuts against the reason the material is there.

*The register already carried the asymmetry.* §21.6 blesses an unrecognized
`tarn.`-prefixed key as conforming — readers ignore it and read on. So
`tarn.wibble` at any scope was fine while `tarn.axes` at file scope was
nonconforming, meaning the specification knowing *more* about a key made the
file worse, though a reader's behavior is identical in both cases.

*§21.7 excludes the work.* *"This format detects corruption of structure, not
incorrectness of content."* A standardized key in the wrong document is
incorrectness of content. Enforcing value shape would be more so — `tarn.axes`
is *"array of one object per dimension, in declared order, each with optional
`unit` (string), `origin` (number), and `step` (number)"*, and validating that
is a verifier walking arbitrary JSON against six hand-written shape
descriptions.

## Consequences

The register stays at **125 conditions over 242 named instances** and the
corpus stays at 125/125 with 287 vectors. No vector is owed. The alternative
cost 2 conditions, 4 instances, and 4 vectors to detect a condition no reader
can observe.

One class of file changes verdict: a file carrying `tarn.created` in a layer
document was nonconforming and is now conforming. That is the safe direction —
no file that was conforming becomes nonconforming, so no existing corpus vector
or reader changes behavior, and `[R-MTA-07]` is cited nowhere else in the
document, so nothing else propagates.

Foreclosed: a verifier that reports on the *content* of user metadata. After
this, the only metadata conditions a verifier judges are structural — framing,
encoding, decode, JSON well-formedness, key rules, member ordering — and none
of them looks at what a key means.

Priced knowingly: tooling loses a lint a verifier could have delivered. A
writer that puts `tarn.axes` at file scope now produces a conforming file that
no conformance tool complains about. That lint is worth having and belongs in a
linter, which is free to be stricter than the format.

Left open, deliberately: whether `tarn.stats` should become typed fields in the
layer record rather than metadata. The argument for it is access cost, not
correctness — reading statistics today costs a range request, a possible zstd
decode, and a JSON parse on top of §19.1's two-request open, where structural
fields would be resident already. The argument against is that a verifier
cannot confirm min/max without decoding every tile (§21.7 again), so structural
statistics would still be advisory and still go stale, with an updater
obligation added. That is an ADR-0045 revisit, not a consequence of this
decision.

## Precedent

- §21.6's unrecognized-key row and `[R-MTA-06]`, which had already decided the
  neighbouring case the same way.
- §21.7's structure-versus-content line, and ADR-0043's principle that limits
  and guidance bound implementations rather than validity.
- ADR-0045, which put conventions in keys rather than in structure; this keeps
  the consequence — that conventions are advisory all the way down.
- PNG (ISO/IEC 15948): `tEXt` keywords are conventional, and a decoder ignores
  a keyword it does not recognize. No PNG validator rejects an image because a
  text keyword sits somewhere unusual.
