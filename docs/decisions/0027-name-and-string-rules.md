# 0027. Name and string rules

- Status: Accepted (resolves Q-F2)
- Date: 2026-07-30
- Covers: string encoding; name validity, limits, comparison, uniqueness
- Confirm: none

## Context

Names (layers, dimensions, channels, metadata keys) are lookup keys in a
binary format, so their rules are interoperability surface: unvalidated
strings desynchronize parsers and smuggle terminal-escape sequences (a
hazard PNG's security section names explicitly), duplicate names are pure
ambiguity, and unstated comparison semantics invite readers to invent
normalization or case-folding that writers never promised. Names are keys,
not documentation — descriptions belong in user metadata — which is what
justifies a small cap: 255 bytes is 63–255 characters depending on script,
makes every length prefix a single byte, and bounds worst-case directory
entries (~11 KiB fully maxed) so the discovery-window arithmetic stays
honest.

## Decision

- All strings are length-prefixed UTF-8. Validity is a MUST in both
  directions: writers MUST NOT emit invalid UTF-8; readers MUST treat
  invalid UTF-8 as a validity error at the owning scope (reject-scope,
  never repair).
- Names are non-empty, at most 255 bytes, and MUST NOT contain code points
  U+0000 through U+001F.
- Comparison is raw bytes: two names are the same name if and only if
  their encoded bytes are identical. Readers MUST NOT normalize,
  case-fold, or otherwise transform names for comparison. Writers SHOULD
  emit names in Unicode NFC; the consequence of deviating is that visually
  identical but differently-encoded names may coexist as distinct names.
- Uniqueness within scope is a MUST for writers and readers both: layer
  names unique within a file, dimension and channel names unique within
  their layer, duplicate → reject-scope. (Enforced at the structures that
  define names; the rule is stated once with the string conventions.
  Uniqueness of user-metadata keys is governed by the metadata document's
  own rules, resolved with Q-F1.)

## Consequences

One byte of length prefix everywhere; no Unicode tables required to
implement a conforming reader (validity checking is mechanical UTF-8
well-formedness); the lookalike-names residual is accepted and documented
rather than half-fixed with locale-dependent machinery. Q-F2's four seed
questions (duplicate/invalid names, allowed characters, UTF-8 rules,
length limits) discharge against this one ADR.

## Precedent

- PNG's hostile-control-characters security note and its case-handling
  history ("testing whether a character is uppercase or lowercase is
  inefficient, and even incorrect").
- The general lesson that reader-side name transformation is divergence by
  construction (each reader picks a different Unicode version).
